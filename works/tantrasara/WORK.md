# works/tantrasara — DONE (T1→GATE + L200 + C1 + themes)

## Sources

- Volume `source-library/tantra/texts-clean/gretil_tantrasara_clean.txt` (Nirnaya Sagara 1918, GRETIL, CC BY-NC-SA 4.0).
- `explained-hareesh/tantrasara/` + `hareesh-blog/by-topic/tantrasara/` (readable refs).
- GitHub `prx0r/tantrasara` — essay-0 machine: 98 spans (lines 2436–9842 verified), essay0.json 6 units canonical, rung picks A 18.7m / B 51.8m locked, audio pending narrator pick.
- Chakravarty/Marjanovic (Rudra 2012) = gold-standard English for style calibration (study only, never batch input).

## Status (2026-10-30)

T1 coverage phase COMPLETE. All 22 ahnikas translated T1→GATE, L200+C1 produced, themes seeded.
Refinement layers (L200/C1) machine-draft; full close passes done for 8 condensed passages.

- Ahnikas: 22/22
- Passages: 51
- Verses: 712 (abhts_1.1–22.54)
- L0 tokens: 4,579 (all PARSED except 10 legitimate AMBIGUOUS; 0 FAILED)
- Gate: 7 PASS / 44 BLOCKED (all attributed to glossary heuristics, not translation errors)
- R2: 22 batch files under `s3://sanskritree/batch-t1/2026-10-30-tantrasara-aNN-raw.jsonl`, all byte-verified
- L200: 22/22 (8 sections, MT/IA split, typed crossrefs, review_state: machine)
- C1: 22/22 (7-part structure, passage-local, no modern comparison, 270–629w/passage)
- THEMES: 14 candidate themes (seed→promoted; needs editor blind-review)
- c1 JSON field: 51/51 passages (IPVV-compatible body/terms/see_also)

## R2 pointers (no bytes in git)

- `s3://sanskritree/batch-t1/2026-10-30-tantrasara-a01..a22-raw.jsonl` (22 files, ~500KB total)
- `s3://source-library/tantra/texts-clean/gretil_tantrasara_clean.txt` (source, 130KB)
- Fetch: `bash tools/fetch.sh <r2-key> <out>` (uses `/root/.r2-env`)

## Manifests

- `manifests/tantrasara/R2-ALL.txt` — per-ahnika R2 inventory (passages/verses/tokens/keys/sizes)
- `manifests/ALL-TRANSLATIONS-INVENTORY.md` — master inventory (updated: Tantrasāra DONE)

## Samples

- `samples/tantrasara/gretil-head.txt` — source head

## Next (for scaling to new works)

Follow `process/UPLOAD-RUNBOOK.md`:
1. Drop source in `sources/<work>/` (gitignored bytes)
2. `tools/chunker.py` → passages.jsonl
3. Draft T1 → freeze → `tools/t1_extract.py` → L0
4. ARGMAP (mandatory before READ)
5. L1 (COMPARE) → L2 (READ, Dyczkowski-mode)
6. L200 (8 sections) + C1 (250–600w) + THEMES (after ≥20 C1s)
7. Gate + upload to R2 + register in OpenPāṭala (adapter TBD)

## Notes

- CONDENSED close passes done for 8 passages (A06 P3, A09 P2/P3, A13 P3/P4, A20 P4, A22 P2/P3).
- Glossary hardening (AQ-1…4) queued: citation/term/abstention heuristics over-broad; blocks are data, not failures.
- OpenPāṭala `translations` ingest NOT done (no adapter; 0 rows). Stop point per owner.
- Full run log: `translation-notes/runs/2026-10-30-tantrasara-FULL.md` (in /root, not in this repo).
EOF
echo "WORK.md updated"