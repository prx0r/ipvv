# CLAIMS — active-work whiteboard (check before starting, write before working)

Format: `- [agent/lane] what (paths) — since YYYY-MM-DD`

## Active

- [site] display shell + masters/scholars + Sanskrit ingestion + schemas/gates — `site/`, `specs/`, `tools/`, `site/data/{authors,scholars.json,works_*.json,sanskrit/}`, `site/dist/`, `process/SESSION-2026-10-30.md` — since 2026-10-30
- [pipeline] T1→GATE→L200→C1 per-work translations — `works/*/`, `samples/*/` — since 2026-10-30

## Requested (needs owning agent or owner)

- (none open — add here, don't cross lanes)

## Done (log when lane work completes)

- 2026-10-31: site — 16 masters, 23 scholars, 46 Sanskrit texts, canonical person schema, hero images, live deploy
- 2026-10-31: pipeline — stotra set T1→GATE→L200→C1 (10 works incl. 450-verse Stotravali)

## Requested (needs owning agent or owner)

- [site→pipeline] Grouped-L2 gate leak (2026-10-31): 4 translation records whose PASS `l2` spans BLOCKED sibling chunks, publishing BLOCKED-verse English under a PASS record: `bodhapancadasika:bod-p12` (covers BLOCKED p14), `kramastotra:kram-p01` (covers p02,p03,p05), `kram-p11` (covers p12,p13,p15), `kram-p16` (covers p18,p19). Fail-closed violation in live data (`site/data/translations/*.json` → dist → site). Fix: split groups per-chunk or gate the group by its most restrictive member. — `site/data/translations/`
- [site→pipeline] `work_id: "tantrasara"` hardcoded in 41/43 `site/data/translations/*.json` (only tantrasara.json + anuttarastika.json correct). Latent (display + Worker use filename/URL, nothing reads the field) but wrong data served. Fix: `tools/ingest_batch.py:52` — derive from batch key/work, re-ingest. — `site/data/translations/`
- [site→pipeline] kramastotra argmap p07–p29 is a noun-swapped template (23 identical premises/inference/conclusion; `question` fields don't match verses). Verified via grep (28 distinct premises only because the noun differs). Needs rewrite from Sanskrit. — `samples/kramastotra/ARGMAP-full.md`
- [site→pipeline] kramastotra T1 gloss↔Sanskrit mispaired in multiple passages (verified p04: gloss=sārvajña/vāci/stotra vs sa=vidhunvāno/bandha; p06: gloss=śivaikātmya/prāyaścitta vs sa=jvaladrūpa/vahni). L0 parsed the tokens but pairing is wrong. Needs re-pairing against GRETIL verse order. — `samples/kramastotra/T1-full.md`
