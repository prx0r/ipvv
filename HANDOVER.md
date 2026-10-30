# HANDOVER — ipvv (live)

## State (2026-10-30)

- Repo: `prx0r/ipvv` (this, clean). Bulk: `sanskritree/ipvv-translations/` (229 objects).
- T1 golden: 28 Vol-1 + 35 Vol-2/3 = 63 chunks, immutable.
- L0: 102,157 tokens (96.4% PARSED), + Vol-1 v1 22,064. Tool: `tools/t1_extract.py`.
- Pilot: 109 files (ARGMAP + L2 READ for V1A–N, V2A–S, V3A–P + V3B deep dive).
- L200: 63 audits (spec frozen, 8 sections). C1: 63 read + 63 source.
- Published: 49 pt-passages in `patala/public/published/ipvv/` (pointer in `manifests/`).
- Tests PASS deterministic: L0, T1, integration. Model-dependent: L2, C1, ARGMAP (Hermes).
- Gaps: 3 NEEDS_MAPPING legacy V1, Vol-3 L1 only V3B pilot, SYNTHESIS/ESSAY/EDUCATION = 0 in factory.

## R2 pointers (no bytes in git)

- `sanskritree/ipvv-translations/t1-vol1/` (28) + `t1-golden/` (35)
- `sanskritree/ipvv-translations/pilot/` (109) + `l0/` (tarballs + audit + reports)
- `sanskritree/ipvv-translations/artifacts/` (manifest, chunk map, Vol-3 mined)
- `patala/public/published/ipvv/` (30 incl. index, essays, clusters)
- Fetch: `bash tools/fetch.sh <key> <out>` (uses `/root/.r2-env`).

## Next

1. Tantrasāra Āhnika 11 (śaktipāta) as first upload→translate test.
2. Full-IPVV READ site from 49 passages (fix `pt:passage` vs `tantra:text` ID mismatch).
3. Backfill 3 legacy mappings, extend Vol-3 L1 beyond V3B.
