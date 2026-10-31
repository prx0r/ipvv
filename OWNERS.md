# OWNERS — who owns what in prx0r/ipvv (two-agent rule)

Two agents push to master. No branches, no PRs — lanes + rebase discipline instead.
If lane conflicts start, switch to worktrees (one branch per agent, merge by the owner).

## Lanes (exclusive write access)

| Lane | Owner | Paths |
|------|-------|-------|
| PIPELINE (translations) | pipeline agent | `works/<work>/`, `samples/<work>/`, R2 `batch-t1/` drafts |
| SITE (display) | site agent | `site/build.py`, `site/dist/`, `site/data/sanskrit/` |
| SCHEMA (contracts) | site agent (proposal) → owner decides | `specs/`, `tools/validate*.py`, `tools/verify.sh` |
| PEOPLE (masters/scholars) | site agent | `site/data/authors/`, `site/data/scholars.json`, `site/data/works_*.json` |
| DOCS (notes) | whoever did the work | `process/SESSION-*.md` (append-only, own section), root `HANDOVER.md`/`README.md` (coordinate first) |

## Rules (both agents, no exceptions)

1. `git pull --rebase` before every push. Never `--force` (no lease, no exceptions).
2. Commit small, push often. One concern per commit, message names the lane.
3. Never edit the other lane's files. Need a change across the lane line? Note it in `process/CLAIMS.md` and let the owning agent (or owner) do it.
4. `site/dist/` is GENERATED. Only the site agent rebuilds/commits it, always from a fresh full `python3 site/build.py` + `verify.sh` green. Pipeline output lands via `site/data/works_*.json` + `site/data/sanskrit/` (site agent imports on request, never edits pipeline sources).
5. `process/CLAIMS.md` is the shared whiteboard: check it before starting, write your claim before working.
6. Root docs (`README.md`, `HANDOVER.md`, `AGENTS.md`, this file): coordinate in CLAIMS before editing.
7. Conflicts on push: rebase, keep both sides' lane files, NEVER resolve by deleting the other lane's work. If a rebase looks wrong, stop and ask the owner.

## Release train (the workflow)

Pipeline pushes translation work (`works/*/`, `samples/*/`). Site agent ships it live:

```
git pull --rebase → import new/changed works output into site inputs
→ python3 site/build.py (full) → verify.sh green → wrangler pages deploy
→ commit → push
```

Site never edits pipeline sources; it only reads them. If a work's output isn't yet in a shape the display contract consumes (`specs/schema/site-item.json`), the site agent notes it in CLAIMS and ships everything else — never blocks the train, never fakes the missing car.

## Current state (2026-10-31)

- Pipeline agent: running T1→GATE→L200→C1 per work (stotra set done: Bhairavastava/Bodha/Krama/Paryanta/Stavacintamani/Paramarthasara/PHrdaya/Sivasutra/Spanda/Sivastotravali), R2 batch-t1 drafts.
- Site agent: display shell, 16 masters + 23 scholars, Sanskrit ingestion, schemas, gates.
