# IPVV — translate from scratch

Live site: **https://ipvv-a8u.pages.dev** (Cloudflare Pages, `site/dist/`, 208 pages).

Abhinavagupta's **Īśvarapratyabhijñāvivṛtivimarśinī** (IPVV), Vols 1–3 (~34,000 lines). No complete English exists. This repo is the **pure process** to make one: upload Sanskrit → frozen T1 → auditable English.

Bulk bytes live in R2 (`sanskritree/ipvv-translations/`, 229 objects). This repo holds process + specs + skills + logs + samples + manifests. Fetch bytes on demand with `tools/fetch.sh`.

## Read order (10 min)

1. `AGENTS.md` — laws, read order
2. `VISION.md` — what done looks like
3. `HANDOVER.md` — live state + counts
4. `process/UPLOAD-RUNBOOK.md` — translate any work from zero
5. `process/KNOWLEDGE-CORE.md` — the philosophy in one page

## The pipe (frozen)

```
SOURCE → T1 (immutable) → L0 (free) → ARGMAP (lateral) → L2 → L200 → C1 → THEME → ARGUMENT
```

Spec: `specs/CANONICAL-DAG.yaml`. Build index: `process/IPVV-BUILD.md`.

## Layout

```
AGENTS.md · VISION.md · HANDOVER.md
process/    pure routine (UPLOAD-RUNBOOK + stage docs 00-08)
specs/      frozen contracts (DAG, L0 schema, C1, L2, THEME, storage)
tools/      t1_extract.py + chunker.py + fetch.sh + verify.sh
skills/     patala-translate · raw-l0 · translate-passage/work · write-commentary · validate-passage
logs/       calibration + freestyle lessons + stall log + FAILS + next steps
samples/    T1/L0/L1/L2/ARGMAP heads (full bytes in R2)
manifests/  R2 inventory + chunk maps + published index (pointers, no 145MB in git)
sources/    landing zone for new uploads (gitignored bytes)
```

## Translate from scratch (one command per stage)

See `process/UPLOAD-RUNBOOK.md`. Short version: drop IAST/DOC in `sources/`, chunk to SOURCE passages, draft T1, freeze, `t1_extract.py` → L0, argmap, L2, L200, C1, publish 4 views.

## Honesty

Machine proposes, human disposes. `MACHINE_PROPOSED ≠ ACCEPTED`. L0/T1/integration tests PASS deterministic; L2/C1/ARGMAP need Hermes + review. SYNTHESIS/ESSAY/EDUCATION = 0 in factory — declared, not built. Full fail list: `logs/FAILS.md`.
