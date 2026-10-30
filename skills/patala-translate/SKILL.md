---
name: patala-translate
description: "The Pāṭala A3 autonomous translation agent. Reads NEXT_VALID_ACTION from the corpus ledger, takes a BATCH of raw Sanskrit verses + the full context packet (school/period/companions/term-senses), produces L0 glosses AND close English translations for the WHOLE batch in ONE context/API call (as many as fit), validates each deterministically, stamps MACHINE_PROPOSED provenance, commits the immutable L0, updates the ledger, and advances to the next eligible work — fail-closed, all night, unattended."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [sanskrit, translation, l0, factory, agent3, patala, autonomous, batch]
    related_skills: [raw-l0, validate-passage, use-api]
    checkpoint: CP1 (source floor) → the autonomous A3 translation factory
---

# PATALA-TRANSLATE — the autonomous translation agent loop

## The one thing to get right
**MAX CONTEXT, MINIMAL CALLS.** Process as many verses as fit your context in ONE response —
the whole batch + its school/period/companion/term-sense context is one prompt; you return one JSON
for every verse (L0 glosses + close translation). The more context you hold, the better the senses.
Do NOT do one verse per call.

## Files this agent reads (context engineering — READ before proposing)
- **The ledger (what to do next):** `GET /api/corpus/state` → `NEXT_VALID_ACTION(work)`. Pick the top
  eligible `RAW_SANSKRIT` work (e.g. kramasadbhava). Its `source_ref` gives the raw Sanskrit.
- **The batch translator (your tool):** `pipeline/batch_translate.py` — takes `--work <id> --verses N`,
  builds the Vidyut token lists + the term-context packet, and returns L0 glosses + close translations
  for the whole batch in ONE `hermes -z` call. Call this for the batch.
- **The L0 contract:** `translations/_stack/ipvv/specs/l0_schema.json` (15 fields, id `.+:L\d+:T\d+$`).
- **The deterministic core + validator:** `pipeline/raw_l0.py`, `pipeline/validate_l0_spec.py` (schema +
  P0 + abstraction-honesty + gloss — the un-cheatable gate), `pipeline/verify_l0.py` (P0 proof).
- **The immutable registry:** `pipeline/l0_registry.py` (commit a NEW version, never edit in place).
- **The context packet:** `pipeline/agentic_gloss.py::_term_packet_for(work_id)` — school, period,
  companion guides, translation neighbourhood, semantic-shift term-senses from `docs/corpus/canonical_reference_map.md`
  + `pipeline/sivaqueue_targets.py`.

## The loop (each run — autonomous, unattended)
```
1. LEDGER      query /api/corpus/state → NEXT_VALID_ACTION; pick top eligible RAW_SANSKRIT work
2. CONTEXT     load the work's context packet (school/period/companions/term-senses) + raw Sanskrit
3. BATCH       run pipeline/batch_translate.py on a batch of verses → L0 glosses + close translations
               for the WHOLE batch in ONE call (max context)
4. VALIDATE    per verse: pipeline/validate_l0_spec.py (schema + P0 + abstraction-honesty + gloss).
               FAIL → halt that verse + log; do NOT fabricate, do NOT let it poison the work.
               AMBIGUOUS / uncertain → mark honestly (empty gloss + uncertain list), never a confident guess.
5. STAMP       MACHINE_PROPOSED provenance (origin=machine, never ACCEPTED).
6. COMMIT      pipeline/l0_registry.py commit → a NEW immutable version.
7. LEDGER      update the corpus ledger → next eligible work. Repeat until queue empty or hard failure.
8. REPORT      summarize: work, batch size, calls used, committed/failed/abstained, review queue.
```

## Accuracy doctrine (non-negotiable)
- **Wrong translation is worse than none.** Validation is the gate; never let the factory outrun it.
- **Proof dimensions stay separate:** source_span PROVED · morphology SUPPORTED (Vidyut witness) ·
  lexical_sense MACHINE_PROPOSED. Never collapse into a confidence number.
- **Abstain, don't invent.** Unanalyzable → empty + `uncertain`. False-certainty is the failure metric.
- **L0 is immutable + versioned.** A fix is a new version, never an in-place edit.
- **AI proposes ≠ Pāṭala asserts.** Output is always `origin=machine`.
- **Context correctness:** the same lemma means different things in different schools/periods — `vimarśa`
  in Pratyabhijñā = "reflexive awareness", NOT "reflection"; `pāśa` in early Siddhānta ≠ late Kaula;
  `kula` in Kubjikā = mantra-body. Use the term-context packet, never a flat dictionary.

## Fail-closed
- One bad verse → halt that verse + log; continue the clean ones; a work with too many failures stops.
- A hung model call → fail after the timeout (model.py defaults to 120s); do not block the whole queue.
