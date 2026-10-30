# THE IPVV BUILD — complete index (scholarly layers + factory implementation + golds + tests + results)

*2026-08-14. THE single authoritative reference for the entire IPVV (Īśvarapratyabhijñāvivṛtivimarśinī)
build. It consolidates the two sides that were previously fragmented:
  (1) the SCHOLARLY layers (sanskritree `translations/_stack/ipvv/` — the L0→L200→C1→ESSAY corpus)
  (2) the FACTORY implementation (Pāṭala `pipeline/` — the workers, golds, argmap recovery, tests)
Every layer, every chunk count, every gold, every test, and every result is recorded here so an agent
can find, verify, and reconstruct the whole build. See `FIRST_VERTICAL_IPVV.md` for the vertical, and
`PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` for the corpus-build method.*

---

## 1. THE ONE-LINE BUILD

> The IPVV (Vols 1–3, ~34,000 lines) is **fully translated and layered**: a deterministic floor
> (SOURCE→T1→L0→L200) is REAL and TESTED, the C1 commentary layer is real (63 chunks), the 5 gold
> arguments + the ARGREC pilot recovered a real IPVV argument with NO gold leakage, and the Nyāya gate
> + integration test PASS. The upper layers (SYNTHESIS/ESSAY/EDUCATION in the factory) are declared but 0 objects.

---

## 2. THE LAYERED EDITION (the architecture)

```
SOURCE  (M00020/21/22 + Torella's IPK)
  ↓  L0/L1    token-level + controlled translation     (l0/, l0_v1/, l1_l2_worker)
  ↓  L2       real book prose                          (pilot/pilot_*_L2_read.md)
  ↓  L200     how each reading was derived (8-section audit)  (l200/ — THE proof layer)
  ↓  C1       what each passage means (compact, local)  (c1/read/ + c1/source/)
  ↓  THEMES   what pattern emerges (TO BUILD in factory; pilot proven)
  ↓  PARALLELS cross-textual witnesses (LATER)
  ↓  ESSAYS   the arguments that follow                (research-library/recognition/, 22 essays)
  ↓  EDUCATION how we teach it (0 objects in factory)
```

---

## 3. THE SCHOLARLY LAYERS (sanskritree `translations/_stack/ipvv/`)

| Layer | Path | Count | Status |
|---|---|---|---|
| L0 records (Vol 1) | `l0_v1/*.l0.jsonl` | 28 | real, validated |
| L0 records (Vol 2–3) | `l0/*.l0.jsonl` | 35 | real, validated |
| T1 golden chunks | `01_t1/` + `02_t1/` | 63 | GOLD (hand-authored) |
| L2 READs + argument maps | `pilot/pilot_*_{L2_read,ARGUMENT_MAP}.md` | 108 | real |
| **L200 audits** | `l200/` | **63** | **real — 3 canonical models (V2-O/V3-B/V3-C) + 8 hand-authored + 52 standardized, all `editor-reviewed`** |
| **C1 read commentaries** | `c1/read/` | **63** | real |
| **C1 source records** | `c1/source/` | 63 | real |
| C1 essay-material (legacy) | `c1/_essay-material-legacy/` | 11 | preserved as essay assets, NOT C1 |

**The L200 proof layer** (`l200/`): 8 sections per chunk (IDENTIFICATION / PUBLISHED READING /
DERIVATION MAP / MATERIAL TRANSLATION DECISIONS / INTERPRETIVE ASSERTIONS / SOURCE LAYER /
CROSS-REFERENCES / REVIEW STATE). Decision types strictly separated:
`SUPPLIED · REFERENT_SUPPLY · STRUCTURAL_CONNECTIVE · LEXICAL · GRAMMATICAL` (MT) vs `IA-###` (interpretive).
Validator: `l200_validate.py`. Migration guarded (never overwrite canonicals).

**The C1 layer** (`c1/`): compact (100–450 words), passage-local, TWO representations (`c1/source/`
structured + `c1/read/` continuous). Governed by `C1-SPEC.md`. Hard rules: no modern comparison, no
essays-as-evidence, no PARALLELS inside, compact-not-essay.

---

## 4. THE FACTORY IMPLEMENTATION (Pāṭala `pipeline/`)

The vertical workers (`BUILD-RECORD-2026-08-13-VERTICAL-WORKERS.md`): each layer a worker + a
layer-specific validator, fail-closed.

| Layer | Worker | Validator | Produces |
|---|---|---|---|
| L0 | `l0_worker.py` | `validate_l0_spec` (P0 span-proof) | canonical L0 records |
| L1 | `l1_l2_worker.py` | L1 semantic-fidelity | controlled reading |
| L2 | `l1_l2_worker.py` | L2 semantic-fidelity (lemma-overlap) | readable prose |
| L1L2 | `l1_l2_translate.py` | F4 binding | model L1+L2 |
| **L200** | `l200_worker.py` (**REWRITTEN**) | Task-2 fidelity (8 sections, typed MT, derivation map) | 8-section audit |
| **C1** | `c1_worker.py` (**NEW**) | C1-SPEC §17 quality gate | passage-local commentary |
| THEME/ESSAY/EDU | `generative_worker.py` | deterministic structural | model proposes |

**The two real fixes:** (1) L200 input-binding (was building from empty L2; now resolves committed L2
from registry), (2) CP4 constrained compiler (`_generate_candidates` + `_classify_candidates` with
IGNORE default prior; model failure → GENERATION_FAILED, never empty success).

**The vertical proof** (`prove_vertical.py`): 3 real committed kramasadbhava L0 objects through
`L1→L2→L200→C1`, all committed, provenance-bound (`C1→L200→L2→L1→L0`), fail-closed on bogus upstream.
**VERTICAL PROOF PASS.**

---

## 5. THE GOLD ARGUMENTS (the scholarly evidence)

`machinelearning/research/patala_ml/gold002..005.py` + `gold.py` — **5 hand-constructed, primary-Sanskrit-
grounded arguments**, each a distinct move, each with `real resolvable passage id`:

| Gold | Passage | Move |
|---|---|---|
| ARG-GOLD-001 | (V2-O) | the base argument |
| ARG-GOLD-002 | `chunkV2-L` | **objection→reply** — the "I" is NOT a vikalpa, it's the `dvayākṣepī` self-grasp |
| ARG-GOLD-003 | `chunkV2-O` | **reductio** — ordered-support regress is absurd |
| ARG-GOLD-004 | `chunkV2-H` | **conceptual distinction** — prakāśa vs vimarśa |
| ARG-GOLD-005 | `chunkV3-I` | **ambiguous case** — two defensible reconstructions (kept ambiguous) |

**The review packet** (`benchmarks/v0/ARG-GOLD-REVIEW-PACKET-v2.md` + `.json`): every proposition grounded
**directly to L0/SourceSpan/Sanskrit** (never through L2 — fixes the derivational circularity v1 flagged).
Explicitness labels (`TEXTUALLY_EXPLICIT/SUPPORTED/RECONSTRUCTED_NECESSARY/INTERPRETIVE_EXTENSION`) + the 4
review questions + ACCEPT/REVISE/REJECT/ABSTAIN.

---

## 6. THE ARGREC PILOT (the real recovery result)

`data/evaluation/argrec-pilot-001-freeze.json` + `argmap.json` — **IPVV-ARGREC-PILOT-001**:
- Passage: `ipvv:V2L` (the "I"-recollection is NOT a construction)
- **No gold leakage** (gold is separately frozen, forbidden from generator input)
- Source hashes pinned (5 kārikās, RAW_SANSKRIT)
- The machine recovered the objection/reply/crux with honest `open_items` + `NEEDS_REVIEW` flags
- A `decision_for_l2` (the crux is NOT settled)

---

## 7. THE NYĀYA GATE + TESTS (what's actually verified)

**Nyāya gate** (`machinelearning/research/patala_ml/nyayagate.py`): `gate_claim()`, `check_viruddha_graph()`
(same-title-diff-author / contradiction detection), `GateResult` — implemented, not aspirational.

**The deterministic IPVV test suite — what PASSES (no model needed):**
| Test | Result |
|---|---|
| `test_l0_ipvv` | **PASS** (incl. honest abstention — no fabrication) |
| `test_t1_ipvv` | **PASS** (gold token check) |
| `test_ipvv_integration` | **PASS** (gate + viruddha + golds + pack connected) |
| `test_l200_ipvv` | runs (Task-2 fidelity; gold MT types: GRAMMATICAL/LEXICAL/STRUCTURAL_CONNECTIVE/SUPPLIED) |

**Model-dependent (pass only when the model is reachable — NOT deterministic):** `test_l2_ipvv`,
`test_c1_ipvv`, `test_argmap_ipvv` (they invoke Hermes).

---

## 8. THE RECOGNITION ESSAY LIBRARY (the scholarship/synthesis layer)

`research-library/recognition/` (sanskritree-adjacent): 22 essays. The authoritative statement:
`ESSAY-C-RAZOR-IPVV-AUTHORITY.md` (~8,700 words). Plus the proof chain, comparative essays (vs.
Spanda/Krama/Advaita/Buddhist), systematic essays, the validation/audit/synthesis, and the hounds
(`pushing-ipvv/`, `pushing-tantraloka/`).

---

## 9. THE PUBLISHED IPVV (Pāṭala site)

`data/published/ipvv/` — 49+ passages (`pt:passage:ipvv:chunk*-md.json`). The recognition-thesis unit
(`data/corpus/units/isvarapratyabhijnavivrtivimarsini-1.5.11-published.ts`) + the IPVV overview page
(`app/texts/isvarapratyabhijnavivrtivimarsini/page.tsx`).

---

## 10. THE KEY DOCS (read in this order for a new agent)

| Read | What it gives |
|---|---|
| `IPVV-KNOWLEDGE-CORE.md` | the philosophy + editorial discipline (the WHY) |
| `translations/_stack/ipvv/README.md` | the layer stack (the WHAT/architecture) |
| `HANDOVER-IPVV-LAYERS-2026-08-12.md` | what exists + how-to-again + the cross-reference index (§8) |
| `HANDOVER-PLANS.md` | the roadmap (THEMES → PARALLELS → c1/source → MCP → cross-graph → EDUCATION) |
| `PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` | how the corpus was built (reproducible, text-agnostic) |
| `FIRST_VERTICAL_IPVV.md` | the gold vertical (ARG-002 review loop → audit/benchmark loop) |
| `BUILD-RECORD-2026-08-13-VERTICAL-WORKERS.md` | the factory workers (L200/C1 implementation) |
| `docs/vision/INDEX.md` (CP4) + `endgamebuild/PROGRESS.md` | the engineering checkpoint state |

---

## 11. THE HONEST STATE

- **DETERMINISTIC + PROVEN:** SOURCE→T1→L0→L200 (63 chunks), the C1 layer (63), the 5 golds, the Nyāya
  gate, the ARGREC pilot (no gold leakage), the integration test.
- **MODEL-DEPENDENT (real but not deterministically verifiable):** L2, C1 (factory worker), ARGMAP
  (they invoke Hermes).
- **0 OBJECTS (declared, not built):** SYNTHESIS, ESSAY, EDUCATION in the factory registry.

*This is the complete IPVV build index. The scholarly corpus (sanskritree) + the factory implementation
(Pāṭala) + the golds + the tests + the results are all here. A new agent reading §10 in order can
reconstruct and verify the entire build.*
