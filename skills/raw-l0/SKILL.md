---
name: raw-l0
description: "Convert a new RAW Sanskrit work/verse into audited, canonical Pāṭala L0 (the IPVV 15-field schema), validated by verify_l0.p0_proof, and register the progress in the corpus-state ledger. Use when asked to ingest a new raw Sanskrit text, produce RAW-L0 / L0-SOURCE-MODE, or test that a new raw verse yields a successful v0 L0. This is the autonomous Agent 3 factory's Build 1."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [sanskrit, raw-l0, l0, pipeline, factory, agent3, patala, scholarly]
    related_skills: [translate-passage, validate-passage, assemble-stack, use-api]
    checkpoint: CP1 (the source floor) → the autonomous RAW-L0 factory (A3)
---

# RAW-L0 — raw Sanskrit → audited canonical L0

## When to use
- Asked to ingest a NEW raw Sanskrit work or verse (not the IPVV).
- Asked to produce RAW-L0 / L0-SOURCE-MODE / "MODE_B".
- Asked to test whether a raw verse yields a successful v0 L0.
- Asked to advance the autonomous Agent 3 factory on a `RAW_SANSKRIT` work.

## The one thing to get right
**Emit the SAME canonical L0 schema the IPVV uses**, so the existing machinery
(`verify_l0.py` P0 proof, the published store, the C1 chain) consumes it UNCHANGED.
The precedent is `extract_l0_v1.py` (non-standard → canonical L0 that passes `verify_l0`).

## Files this skill reads (READ BEFORE YOU PROPOSE — context engineering, not blind prompting)
Load the relevant ones into context FIRST; never propose a gloss from memory alone.
- **The L0 spec (the contract you must satisfy):** `translations/_stack/ipvv/specs/l0_schema.json`
  — the 15 required fields + the `id` pattern `.+:L\d+:T\d+$` + `status ∈ {PARSED, AMBIGUOUS, FAILED}`.
- **The deterministic core + proof:** `pipeline/raw_l0.py` (builds canonical records via Vidyut),
  `pipeline/verify_l0.py` (`p0_proof`: exact span integrity, 0 unknown, roundtrip),
  `pipeline/validate_l0_spec.py` (the un-cheatable gate: schema + P0 + abstraction-honesty + gloss).
- **The work's term/context packet:** `docs/corpus/canonical_reference_map.md` (the LEMMA→SENSE
  semantic-shift atlas — the translation policy per tradition/text/period) +
  `docs/corpus/TARGETS-INDEX.md` (which work + its priority/tradition) +
  `docs/corpus/SANSKRITREE-IMPORT-MANIFEST.md` (what's ingested vs not).
- **The work's COMPANION / translation-neighbourhood packet (READ THIS BEFORE TRANSLATING — do not skip):**
  `pipeline/sivaqueue_targets.py` → `--sivaqueue-work <work_id>` gives this target's **school
  (tradition), period, genre, translation_status, companion translation-memory guides (G1–G14),
  translation_neighbourhood (the specific companion works to consult), and the semantic-shift
  term-senses** that apply to THIS school/period. Also `data/corpus/sivaqueue-guides.json` (the
  companion-guide definitions) + `data/corpus/sivaqueue-targets.json` (all 100 targets).
- **The goldmine:** `docs/corpus/` + `data/corpus/targets/` (sources/targets/leads/anchors/sivaqueue/index).
- **The doctrine:** `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` (validation first; proof
  dimensions separate; never a collapsed confidence).

**Context engineering rule (MANDATORY — review the companions BEFORE translating, and WHY):**
Do NOT translate a token from the dictionary or from memory. First pull the target's
`--sivaqueue-work` packet: its **school + period** and its **companion translation-memory guides +
translation neighbourhood**. Read the relevant companion guides (the critical-Sanskrit-with-
specialist-English editions) so you translate in the historically-correct register. **WHY:** the same
lemma means different things in different schools/periods — `vimarśa` in Pratyabhijñā = "reflexive
awareness", NOT "reflection"; `pāśa` in early Śaiva Siddhānta ≠ `pāśa` in late Kaula; `kula` in a
Kubjikā text = mantra-body, NOT "family". A companion guide tells you which sense the target's own
tradition actually licenses. **Semantic consistency is the goal, not lexical uniformity.** If a
target's companion guide is not yet downloaded to disk, say so honestly and translate conservatively
(mark uncertain terms `AMBIGUOUS`) rather than guessing a sense from the wrong school.

## The flow (per verse — the atomic unit)

```
RAW SANSKRIT
   ↓  [pipeline/raw_l0.py — DETERMINISTIC, Vidyut]
canonical L0 records (15-field schema; lemma/morphology/segmentation)
   ↓  [CONTEXT ENGINEERING — read the reference map term-packet for this work]
   ↓  [PROPOSE — the gloss per token, the generative layer]
   ↓  [SELF-CHALLENGE — a separate pass tries to falsify: wrong lemma? wrong sense? gloss
       too interpretive? polarity lost? — revise or abstain]
   ↓  [validate_l0_spec.py — the EXISTING un-cheatable .py gate]
P0 proof (source_span PROVED · unknown_chars 0 · PASS) + schema + abstraction + gloss
   ↓  [pipeline/agent3_batch.py]
ledger update (RAW_SANSKRIT/BLOCKED → ELIGIBLE) + batch manifest (progress)
```

## Step 1 — get the raw source
The corpus-state ledger knows each work's `source_ref` (e.g. the Dyczkowski Kramasadbhāva
edition). Load it, or take the verse directly. Use a small text first (e.g. Kramasadbhāva).

## Step 1.5 — REVIEW THE COMPANIONS FIRST (mandatory, do not skip)
Before translating a target, pull its companion/translation-neighbourhood packet:
```bash
python3 pipeline/agent3_queue.py --sivaqueue-work <work_id>
# -> school, period, genre, status, companion_guides (G1-G14), translation_neighbourhood,
#    semantic-shift term-senses for this school/period
```
Then **read the named companion guides** (the critical-Sanskrit + specialist-English editions) so you
translate in the historically-correct register. **WHY:** a companion guide licenses the sense the
target's own tradition actually uses — it stops you rendering `pāśa = "bondage"` or `vimarśa =
"reflection"` from the dictionary alone. **Same lemma ≠ same concept.** If the companion text is not
on disk, say so and mark uncertain terms `AMBIGUOUS` rather than guessing a wrong-school sense.

## Step 2 — context engineering (READ, don't prompt)
Load the files above. For the work's key terms, pull the sense + translation policy from
`docs/corpus/canonical_reference_map.md` (the glossary table) + the `--sivaqueue-work` semantic-shift
term-context. Build the **term-context packet** for this verse before you gloss anything.

## Step 3 — run the deterministic core (no model needed)
```bash
python3 pipeline/raw_l0.py --work <work> --passage <work>:<loc> --sanskrit "<verse>"
```
This uses Vidyut (segmentation + lemma + morphology) to build canonical L0 records, then
runs the EXISTING `verify_l0.p0_proof`. Output: `data/corpus/downloads/raw-l0-canonical.json`.

**Verse locators** (`||1/1`) are stripped as STRUCTURAL (the passage locator, not content) so
P0 sees only the semantic Sanskrit.

**Abstention is honest:** a token Vidyut can't analyze (lemma=null) → `status: AMBIGUOUS`,
never `PARSED`. A lacuna verse (`* * * *`) → FAIL (sent to the review path). Never fabricate.

## Step 4 — propose the gloss (the generative layer) + SELF-CHALLENGE
For each token, produce `literal_gloss` as a word/phrase-level literal meaning, anchored to the
Vidyut lemma + the reference-map sense for this work. Then run a **self-challenge pass**: a
separate read that asks "could this gloss be wrong? wrong lemma? imported a sense from the wrong
tradition? too interpretive? lost negation/polarity?" — revise, or set `AMBIGUOUS` if genuinely
uncertain. Provide via `--gloss-file` (JSON `{token: {literal, compound, supplied}}`; a flat
`{token: literal}` is also accepted) or a model call.

**`supplied: true`** means the English is supplied for readability (auditable), not a direct
translation of the token.

## Step 5 — validate with the un-cheatable .py gate (you CANNOT pass by claiming)
```bash
python3 pipeline/validate_l0_spec.py --records <records.jsonl> --chunk-text <source_chunk.txt>
```
This re-checks, deterministically and independently of the model:
- **SCHEMA** — every record has all 15 fields, correct types, correct `id` pattern, `status` enum.
- **P0 PROOF** — the existing `verify_l0.p0_proof` re-runs (exact spans, 0 unknown, roundtrip).
- **ABSTRACTION HONESTY** — `PARSED` requires BOTH lemma AND gloss; a fabricated PARSED is caught.
- **GLOSS PRESENCE** — non-`FAILED` records must have a non-empty `literal_gloss`.

**The model does not decide if it passed.** This `.py` does. Exit 0 = PASS, 1 = FAIL.

## Step 6 — batch + register
```bash
python3 pipeline/agent3_batch.py --work <work> --max-verses N
```
Splits the raw source into verses, runs RAW-L0 per verse, audits (canonical schema + P0 PASS),
updates the ledger, writes `data/corpus/downloads/agent3-batches/<work>-batch.json`.

## The validation (what makes a v0 L0 "successful")
- [ ] canonical 15-field schema (all records, no missing) — enforced by `validate_l0_spec.py`
- [ ] `verify_l0.p0_proof` PASS (unknown_chars 0) — re-run by the validator
- [ ] lemma=null → AMBIGUOUS (abstain, not fabricated)
- [ ] lacuna/unanalyzable → FAIL → review path (not a fake pass)
- [ ] PARSED records carry BOTH lemma and non-empty gloss (no fabricated certainty)
- [ ] ledger updated + batch manifest written (progress tracked)

## Falsification test
> What would convince you this does NOT work? A verse that claims a PARSED lemma Vidyut never
> produced, or a P0 PASS with unknown_chars>0, or records missing a canonical field, or a
> PARSED record with an empty gloss that `validate_l0_spec.py` still passes.

## Test-drive on a new raw translation
1. Take a fresh raw verse (e.g. another Kramasadbhāva verse, or a new work's verse).
2. Read the reference-map term-packet for that work (context engineering).
3. Run `raw_l0.py` → confirm canonical records + P0 PASS.
4. Propose glosses + self-challenge → pass `--gloss-file` or a model call.
5. Run `validate_l0_spec.py --records ... --chunk-text ...` → must PASS (exit 0).
6. Run `agent3_batch.py` → confirm the ledger + batch manifest update.
7. Inspect the completed record: all 15 fields, honest AMBIGUOUS where Vidyut can't analyze.
