---
name: validate-passage
description: "Validate and track Pāṭala passage records and the corpus: referential integrity, epistemic invariants, per-passage status, and the conformance report. Use when asked to check corpus health, find broken IDs, or produce the audit report."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [validation, audit, integrity, epistemic, patala, corpus]
    related_skills: [translate-passage, assemble-stack]
    checkpoint: CP1 (referential + epistemic integrity of the corpus)
---

# Validate Passages & the Corpus

## When to use
- Asked to check the corpus is healthy / has no broken IDs.
- Asked to audit a passage record or a whole work.
- Asked for the conformance report or "how valid is the corpus?"

## How
Run the validation layer (`pipeline/validate.py`):

```bash
# full conformance report (corpus + gold records)
python3 pipeline/validate.py --report

# audit the gold exemplars
python3 pipeline/exemplars_cli.py --audit
```

## What it checks
- **Referential integrity**: duplicate ids, missing work, missing source, dangling references.
- **Epistemic invariants**: machine output never presented as reviewed; stage ordering
  (T1→…→C1 contiguous); T3 requires a prior R2; `[X]` flags not laundered.
- **Per-passage status**: `valid / needs_review / invalid / pending`.

## Interpreting the tally
- `valid` — no errors, no warnings. Good.
- `needs_review` — warnings only (e.g. missing time-place-context). Flag for human; it's honest signal, not failure.
- `invalid` — error-level findings. **Must be fixed.**
- `pending` — record exists, not yet validated.

## If `invalid` or duplicates appear
1. Find the broken passages in the report.
2. Check the source (the `source_file` + edition).
3. If it's a segmentation bug (e.g. colophon-vs-verse), fix the segmenter
   (`scripts/segment-*.mjs`) and regenerate.
4. Re-run `--report` until integrity is clean.

## Invariants
- Never present machine output as reviewed knowledge.
- Report the real tally, not the flattering one.
