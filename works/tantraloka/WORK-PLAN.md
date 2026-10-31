# works/tantraloka — PREP PLAN (2026-10-30)

## Scale

- Source: GRETIL KSTS 1918-38 (Jayaratha Viveka ed.), 17,642 lines, 5,826 verses.
- 37 ahnikas. Ahnika 1 already DONE (331 verses, 34 passages, R2 uploaded).
- Remaining: 36 ahnikas, ~5,495 verses.

## Ahnika inventory (sorted by verse count, ascending)

| # | Ahnika | Verses | Lines | Priority | Status |
|---|--------|--------|-------|----------|--------|
| 34 | catustriṃśa | 3 | 14 | 1 (tiny) | TODO |
| 18 | aṣṭādaśa | 11 | 36 | 1 (tiny) | TODO |
| 20 | viṃśatitama | 15 | 48 | 1 (tiny) | TODO |
| 36 | ṣaṭtriṃśa | 15 | 50 | 1 (tiny) | TODO |
| 12 | dvādaśa | 24 | 78 | 1 (tiny) | TODO |
| 24 | caturviṃśa | 23 | 72 | 1 (tiny) | TODO |
| 25 | pañcaviṃśa | 28 | 88 | 1 (tiny) | TODO |
| 33 | trayastriṃśa | 32 | 99 | 1 (tiny) | TODO |
| 35 | pañcatriṃśa | 44 | 134 | 1 (tiny) | TODO |
| 19 | ekānnaviṃśa | 56 | 169 | 2 (small) | TODO |
| 27 | saptaviṃśa | 58 | 178 | 2 (small) | TODO |
| 21 | ekaviṃśa | 61 | 185 | 2 (small) | TODO |
| 32 | dvātriṃśa | 67 | 205 | 2 (small) | TODO |
| 7 | saptama | 70 | 214 | 2 (small) | TODO |
| 26 | ṣaḍviṃśa | 75 | 229 | 2 (small) | TODO |
| 37 | saptatriṃśa | 85 | 257 | 2 (small) | TODO |
| 23 | trayoviṃśa | 103 | 310 | 2 (small) | TODO |
| 30 | triṃśa | 123 | 371 | 2 (small) | TODO |
| 11 | ekādaśa | 117 | 354 | 2 (small) | TODO |
| 17 | saptadaśa | 122 | 367 | 2 (small) | TODO |
| 31 | ekatriṃśa | 163 | 493 | 3 (medium) | TODO |
| 2 | dvitīya | 50 | 150 | 3 (medium) | TODO |
| 5 | pañcama | 157 | 480 | 3 (medium) | TODO |
| 29 | ekonatriṃśa | 291 | 877 | 3 (medium) | TODO |
| 9 | navama | 313 | 942 | 3 (medium) | TODO |
| 10 | daśama | 308 | 930 | 3 (medium) | TODO |
| 13 | trayodaśa | 360 | 1086 | 4 (large) | TODO |
| 28 | aṣṭāviṃśa | 433 | 1306 | 4 (large) | TODO |
| 8 | aṣṭama | 451 | 1359 | 4 (large) | TODO |
| 6 | ṣaṣṭha | 250 | 756 | 4 (large) | TODO |
| 16 | ṣoḍaśa | 311 | 935 | 4 (large) | TODO |
| 15 | pañcadaśa | 612 | 1844 | 5 (huge) | TODO |
| 4 | caturtha | 277 | 838 | 5 (huge) | TODO |
| 3 | tṛtīya | 293 | 887 | 5 (huge) | TODO |
| 1 | prathama | 331 | 1008 | DONE |
| 22 | dvāviṃśa | 48 | 145 | 2 (small) | TODO |

## Strategy

### Phase 1: Tiny ahnikas (1-9, 24-25, 33-36) — prove loop at scale
- 12 ahnikas, ~250 verses total.
- Each ahnika: chunk → T1 → L0 → ARGMAP → L1 → L2 → L200 → C1 → gate → upload.
- Estimated: 12 sessions, ~1 day.

### Phase 2: Small ahnikas (7, 11, 17, 19, 21, 23, 26, 27, 30, 31, 32, 37) — build momentum
- 12 ahnikas, ~900 verses.
- Estimated: 12 sessions, ~2 days.

### Phase 3: Medium ahnikas (2, 5, 9, 10, 29) — scale up
- 5 ahnikas, ~1,126 verses.
- Estimated: 5 sessions, ~1.5 days.

### Phase 4: Large ahnikas (6, 8, 13, 16, 28) — heavy lifting
- 5 ahnikas, ~1,719 verses.
- Estimated: 5 sessions, ~2 days.

### Phase 5: Huge ahnikas (3, 4, 15) — overnight runs
- 3 ahnikas, ~1,182 verses.
- Estimated: 3 sessions, ~2 days (overnight setsid runs).

## Chunking strategy

- Use `tools/chunker.py` with `--split verse` (not ahnika) for large ahnikas.
- Target 10-15 verses per passage for small/medium, 20-30 for large.
- Ahnika 1 already done with 10-verse chunks (34 passages, 331 verses).

## Model routing

- Bulk translation: `mimo-v2.5` (free CF) via hermes.
- L2 polish/adjudication: `ox-alpha-free` only.
- Gate: deterministic proof (sanskritbenchy) + TranslationProof vector (patalacheckpoints).

## R2 upload

- Key pattern: `s3://sanskritree/batch-t1/YYYY-MM-DD-tantraloka-aNN-raw.jsonl`
- Byte-verify every upload.

## Total estimate

- 36 ahnikas remaining, ~5,495 verses.
- At ~1 session per ahnika (avg 3-4 hours), ~36 sessions.
- With parallelization (tiny ahnikas batched), ~20-25 sessions.
- Realistic: 2-3 weeks of autonomous work.

## Next action

Start with tiny ahnikas (34, 18, 20, 36, 12) — 5 ahnikas, ~68 verses, 1 session.
