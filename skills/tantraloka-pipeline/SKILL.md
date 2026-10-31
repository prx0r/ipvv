---
name: tantraloka-pipeline
description: "Run a Tantrāloka ahnika through the full audited translation pipeline (extract → T1 via beam-free → L0 → ARGMAP/L1/L2/L200/C1 → publish) and batch-process multiple ahnikas in parallel."
version: 1.0.0
---

# Tantrāloka Pipeline

## Inputs
- Source: /root/ipvv/site/data/sanskrit/tantraloka.txt
- Work dir: /root/translation-work/tantraloka-aNN
- Repo: /root/ipvv

## Steps (per ahnika)
1. Extract ahnika text: `python3 /tmp/extract_ahnika.py N > source.txt`
2. Generate T1 with beam-free: prompt model "Do not run any commands. Output only T1 markdown..." with source. Save T1.md.
3. L0: `mkdir -p translations/_stack/ipvv/l0 && python3 /root/ipvv/tools/t1_extract.py T1.md --out T1`
4. Derived layers: run `/tmp/gen_derived.py N` (ARGMAP, L1, L2, L200, C1, STATUS, GATE, publish to ipvv samples/works).
5. Quality pass (high-level agent): refine ARGMAP questions/inferences, L2 prose, C1 boundary, term ledger.
6. Verify: `bash /root/ipvv/tools/verify.sh`

## Batch parallel
Launch 3 at a time:
```
nohup /tmp/process_one.sh N1 > /tmp/log_aN1.txt 2>&1 &
nohup /tmp/process_one.sh N2 > /tmp/log_aN2.txt 2>&1 &
nohup /tmp/process_one.sh N3 > /tmp/log_aN3.txt 2>&1 &
```
Use model `opencode-go/beam-free`. Monitor logs; re-run if T1 contains command output.

## Remaining ahnikas
3,4,6,8,9,10,13,15,16,28,29,31 (verse counts in WORK-PLAN.md).

## Quality pass checklist
- T1 tokens PARSED (L0 report 0 FAILED)
- ARGMAP has speaker/question/premises/inference/conclusion/unresolved per passage
- L2 readable, Dyczkowski-mode, bracketed SUPPLIED
- C1 100-450 words, passage-local
- Gate blocks recorded as heuristic

## Lessons learned (2026-10-31)
- Use `/tmp/nocode/opencode.json` with `"permission": {"*": "deny"}` to prevent tool contamination.
- Strip ANSI escapes from T1.md before derived generation.
- If T1 contains command output, regenerate with nocode config.
- Launch max 3 parallel jobs; monitor logs.

## Chunked generation (for large ahnikas)
- Split source into 20-verse chunks.
- Call opencode run per chunk in /tmp/nocode.
- Assemble T1.md with headings per chunk.
- Then run gen_derived.py.

## Quality status (2026-10-31)
- T1: 100% PARSED for completed ahnikas.
- Derived (ARGMAP/L2/L200/C1): machine-compressed; ARGMAP questions generic; needs high-quality polish.
- Gate: 0 PASS / N BLOCKED (heuristic).

## Kashaudio targets needing T1/C1
- anubhavanivedana (4 verses) — not yet in works/
- bodhavilasa, bhairavanukarana, ajadapramatrsiddhi — already translated (works/ + samples/)
- shivastotravali stotra 1 rest (25 verses) — pending ipvv
