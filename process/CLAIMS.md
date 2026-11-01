# CLAIMS — active-work whiteboard (check before starting, write before working)

Format: `- [agent/lane] what (paths) — since YYYY-MM-DD`

## Active

- [site] display shell + masters/scholars + Sanskrit ingestion + schemas/gates — `site/`, `specs/`, `tools/`, `site/data/{authors,scholars.json,works_*.json,sanskrit/}`, `site/dist/`, `process/SESSION-2026-10-30.md` — since 2026-10-30
- [pipeline] T1→GATE→L200→C1 per-work translations — `works/*/`, `samples/*/` — since 2026-10-30

## Requested (needs owning agent or owner)

- (none open — add here, don't cross lanes)

## Done (log when lane work completes)

- 2026-11-01: registry — `manifests/REGISTRY-BY-MASTER.{json,md}` canonical by-master audit (Abhinavagupta 14 + Ksemaraja 4 + Utpaladeva 5 entries, 0-5 ratings, 11-stage checklist). Update both twins when a stage flips; never mark DONE with 0 PASS.

- 2026-10-31: site — 16 masters, 23 scholars, 46 Sanskrit texts, canonical person schema, hero images, live deploy
- 2026-10-31: pipeline — stotra set T1→GATE→L200→C1 (10 works incl. 450-verse Stotravali)

## 2026-11-01 — translation-work: site data inputs for sivastotravali (site-lane review)
- ADDED `site/data/translations/sivastotravali.json` (127 verse chunks, s01–s05, all proof-PASS) + `site/data/argmaps/sivastotravali/*.md` (127 files). Emitted mechanically by `translation-work/tools/emit_site.py` from canonical `data/*.json`; not hand-written.
- Reader contract honored: per-chunk sanskrit/l1/l2/c1-via-files/gate/model/date; BLOCKED chunks carry no English (none here — all PASS); missing songs absent (greyed, never invented). Renders beyond standard withheld locally (T4).
- No site code touched. Rebuild (`build.py` translations+layers) is site lane's call. — translation-work agent
