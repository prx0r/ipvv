# AGENTS.md — ipvv

You are in **ipvv**: the clean IPVV translation machine. No other repo's rules apply beyond what this file + `specs/CANONICAL-DAG.yaml` say.

## Laws

1. **T1 immutable.** Once frozen, never edited. Fix downstream, never the chunk.
2. **L0 verbatim.** Every record keeps `raw_fragment` = exact source token. Re-checkable by rerun.
3. **Argmap before READ.** No L2 without speaker/question/premises/inference. Reconstruct argument, not sentence.
4. **L1 ≠ L2.** L1 = proposition-faithful, Sanskrit-close (COMPARE). L2 = real book prose (READ, Dyczkowski-mode). Never polish T1 into fake clarity.
5. **MT vs IA separated.** L200: translation decisions (SUPPLIED/LEXICAL/GRAMMATICAL/STRUCTURAL_CONNECTIVE) never mixed with interpretive assertions (IA-###).
6. **C1 local.** 100–450 words, passage-only. No modern comparison, no essays as evidence, no PARALLELS inside. Test: could it sit under the passage in print?
7. **Themes overlap.** Multi-membership allowed. Body-words are noise; KEY TERMS + curated See-also are signal.
8. **Machine proposes, human disposes.** `MACHINE_PROPOSED ≠ ACCEPTED`. No auto-live. `needs_review → verify → live`.
9. **Fail-closed.** Model fail → GENERATION_FAILED, never empty success. Provenance must resolve or the layer is not eligible.
10. **Bytes in R2, truth in git.** 145MB L0 tarballs never commit. Commit specs/process/skills/logs/samples/manifests. Fetch bytes via `tools/fetch.sh`.

## Read order

`README.md` → `VISION.md` → `HANDOVER.md` → `process/UPLOAD-RUNBOOK.md` → `process/KNOWLEDGE-CORE.md` → `specs/CANONICAL-DAG.yaml` → `process/IPVV-BUILD.md`.

## Verify (before any commit)

```bash
python3 tools/t1_extract.py --help
python3 tools/chunker.py --help
bash tools/verify.sh
```

`verify.sh` checks: T1 frozen, L0 counts match, every L2 sentence links to L0, every C1 under 450w, no 145MB in git.
