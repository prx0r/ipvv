# CLAIMS — active-work whiteboard (check before starting, write before working)

Format: `- [agent/lane] what (paths) — since YYYY-MM-DD`

## Active

- [scholar-recovery] Review and harden Scholar auth and account workflow in isolated branch `codex/scholar-recovery` — `worker/`, Scholar tests — since 2026-11-03
- [site] display shell + masters/scholars + Sanskrit ingestion + schemas/gates — `site/`, `specs/`, `tools/`, `site/data/{authors,scholars.json,works_*.json,sanskrit/}`, `site/dist/`, `process/SESSION-2026-10-30.md` — since 2026-10-30
- [pipeline] T1→GATE→L200→C1 per-work translations — `works/*/`, `samples/*/` — since 2026-10-30

## Done (log when lane work completes)

- 2026-10-31: site — 16 masters, 23 scholars, 46 Sanskrit texts, canonical person schema, hero images, live deploy
- 2026-10-31: pipeline — stotra set T1→GATE→L200→C1 (10 works incl. 450-verse Stotravali)
- 2026-11-03: CLOSED grouped-L2 gate leak — evidence: 0 multi-verse PASS groups exist after the verse-grained reshape (scan of all `site/data/translations/*.json`: no PASS chunk with verses-span ≥2 and l2>600). The shapes that leaked no longer exist; reopen if a passage-grained emitter regresses.
- 2026-11-03: CLOSED kramastotra argmap template (PR ipvv#2) — evidence: `samples/kramastotra/ARGMAP-full.md` now 30/30 sections with 30 distinct premise-sets (p07–p29: 23/23 distinct, 0 dup groups); site packets 29/29 distinct questions (e.g. p07 = verse-specific fire-question).
- 2026-11-03: CLOSED work_id hardcode — root-fixed `tools/ingest_batch.py` (work_id now = batch group key, never the record's stamp) + mechanical backfill of 259 chunks across 32 files; rescan: 0 wrong (files without the field untouched). Full rebuild + SITE GATES PASS.
- 2026-11-03: CLOSED kramastotra T1 mispairing — evidence: p04 gloss no longer carries sārvajña/vāci/stotra (those now sit correctly in p03); p04 surface = vidhunvāno bandhābhimata… matching the root verse; p06 likewise clean (sanskrit probe vs samples/kramastotra/T1-full.md).

## Requested (needs owning agent or owner)

