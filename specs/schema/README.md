# Schema index — the rigid import contract

One schema per layer (`specs/schema/`). A new translation is "the same thing" iff `tools/import_work.py` passes it.

| File | Layer | One-line rule |
|---|---|---|
| `work.json` | work manifest | id/title/edition/status/layers/counts — status ladder STOCKPILE→PUBLISHED |
| `passage.json` | SOURCE unit | immutable cut; verbatim Sanskrit; locator resolves |
| `t1.json` | T1 chunk | `[and]-GLOSS (iast)` grammar; frozen hash blocks edits |
| `l0_schema.json` | L0 record | `raw_fragment == chunk_text[start:end]`; PARSED/AMBIGUOUS/FAILED |
| `argmap.json` | lateral guide | speaker/question/premises/inference/conclusion; mandatory before L2 |
| `l2.json` | READ | from ARGMAP+L0; SUPPLIED bracketed; fidelity note |
| `l200.json` | audit | 8 sections; MT vs IA strictly separated |
| `c1.json` | STUDY | 100–450w local; derives from L200; See-also edges curated |
| `theme.json` | THEME | overlap allowed; KEY TERMS + See-also signal; body-words noise |
| `pushing.json` | Q→GEM | question_shape typed; passage_ids resolvable; strength labeled |
| `site-item.json` | **display contract** | six fixed panels; `ok=false` renders greyed, never invented |

Chain (enforced by `CANONICAL-DAG.yaml` + `import_work.py`):
```
SOURCE -> T1 (freeze) -> L0 (free) -> ARGMAP -> L2 -> L200 -> C1 -> THEME -> ARGUMENT
```
Every layer carries its upstream ids. Provenance must resolve or the layer is not eligible. `site/build.py` consumes `site-item` only — same renderer, any work.
