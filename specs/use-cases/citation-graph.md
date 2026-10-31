# Citation graph + witness bench — researcher view

## Inputs
- `site/data/scholars.json` (36 bios + bibliographies + links).
- `site/data/read_alongside.json` (master ↔ scholar edges).
- Witness impressions: Dyczkowski/Torella/Singh coverage notes in WORK.mds.
- QA harness `tools/qa_vs_witness.py` (currently Dyczkowski-only).

## Behavior
- Verse → every witness + every modern treatment, side by side.
- Scholar graph: who edited what manuscript, who cites whom, which translation
  covers which verse.
- Generalize the QA harness beyond Dyczkowski (any witness, same protocol).

## Phases
1. Read-alongside already live on master/scholar pages (done).
2. Verse-level witness view (needs witness coverage index — pipeline data).
