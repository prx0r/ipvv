# UPLOAD RUNBOOK — translate any Sanskrit work from scratch

Pure process. Same pipe that made IPVV. Replace IPVV with your work (next: Tantrasāra).

## 0. Drop source

```bash
mkdir -p sources/tantrasara-ahnika11
cp /path/to/gretil_tantrasara_clean.txt sources/tantrasara-ahnika11/
```

Land raw bytes in `sources/` (gitignored). Record edition: GRETIL/Muktabodha + licence + lines.

## 1. Chunk to SOURCE passages

```bash
python3 tools/chunker.py --in sources/tantrasara-ahnika11/gretil_tantrasara_clean.txt \
  --work tantrasara --split ahnika --out sources/tantrasara-ahnika11/passages.jsonl
```

Rule: kārikā/verse/paragraph as unit, container as parent (IPVV: kārikā-¶). Unit IDs immutable once cut.

## 2. Draft T1 (hyperliteral, then FREEZE)

Per passage, write `[and]-GLOSS (IAST)` inline, max-effort, term-ledger locked. Then freeze — never edit again.

```bash
cp sources/tantrasara-ahnika11/passages.jsonl sources/tantrasara-ahnika11/T1-chunkA.md
# edit T1-chunkA.md to inline-gloss format (see samples/T1-chunkA-head.md)
```

## 3. L0 (free, deterministic)

```bash
python3 tools/t1_extract.py sources/tantrasara-ahnika11/T1-chunkA.md --out sources/tantrasara-ahnika11/T1-chunkA.l0
cat sources/tantrasara-ahnika11/T1-chunkA.l0.report.txt
```

Expect ~96% PARSED. 0 FAILED content or fix the chunk format (not the tool). `raw_fragment` must be verbatim in source.

## 4. ARGMAP (mandatory before READ)

One file per chunk: speaker / question / premises / inference / conclusion / unresolved terms. See `samples/ARGMAP-V1A.md`. Name the question the passage answers. Tag Buddhist objection vs own view ruthlessly.

## 5. L1 → L2

- L1: proposition-faithful, Sanskrit-close (COMPARE). Keep compounds/`-ness` if needed for audit.
- L2: READ prose from ARGMAP+L0, Dyczkowski-mode. Dissolve `-ness`, unpack compounds, bracket SUPPLIED. Fidelity note: preserved / added / not-resolved.

Proof bar: `samples/L2-proof-V3B.md` (S7/S9 hardest paras).

## 6. L200 (8-section audit)

IDENTIFICATION / PUBLISHED READING / DERIVATION MAP / MATERIAL DECISIONS / INTERPRETIVE ASSERTIONS / SOURCE LAYER / CROSS-REFS (typed) / REVIEW STATE. MT vs IA strictly separated.

## 7. C1 (compact)

100–450 words, passage-local. Could it sit under the passage in print? If it needs an essay title or modern comparison, it belongs in THEMES/ESSAYS.

## 8. Publish (4 views)

```
READ      L2 only
COMPARE   L1 + L2
LITERAL   Sanskrit + L1
CRITICAL  L2 + A1 + SL + AQ + C1
```

## 9. THEME (after ≥20 C1s)

Hybrid graph only: KEY TERMS + curated See-also. Never body-words (proven noise). Overlap allowed. Blind-review neighborhoods before naming.

## Gates

- `bash tools/verify.sh` green before commit.
- Hermes (optional): `patala-producer` runs workers, `patala-verifier` checks golds, `patala-coordinator` routes. Hermes never decides truth.
- Model routing (broke rule): bulk on free CF (`llama-3.1-8b`, `mimo-v2.5`, `deepseek-v4-flash`), `ox-alpha-free` only for L2 polish/adjudication.
