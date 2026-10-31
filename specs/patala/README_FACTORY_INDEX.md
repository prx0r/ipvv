# THE REPEATABLE TRANSLATION FACTORY — spec index

*2026-08-11. The complete, text-agnostic spec set that turns ANY Sanskrit (or other) source into a
publishable, auditable scholarly resource — the "factory." Every new translation runs the SAME
stages; the text's own kind selects which optional C1 module applies. Each layer has ONE spec; each
is derived from the one below it; provenance is never lost.*

> **The one rule:** every layer is derived from the one below it, and every claim points back down
> the stack. `SOURCE → L0/L1 → L2 → L200 → C1 → THEMES → ESSAYS → EDUCATION`. Do not collapse layers.

---

## The layer specs

| # | Layer | Spec | Responsibility | State |
|---|---|---|---|---|
| 1 | **SOURCE** | [`SPEC_SOURCE.md`](SPEC_SOURCE.md) | acquisition, registration, witnesses, rights, segmentation, stable IDs | new |
| 2 | **L0 / L1** | [`SPEC_L0_L1.md`](SPEC_L0_L1.md) | literal substrate (token/gloss) + controlled translation | new |
| 3 | **L2** | [`SPEC_L2.md`](SPEC_L2.md) | the readable published prose | new |
| 4 | **L200** | `../l200/README-L200-SPEC.md` | the cross-layer audit (how the reading was derived) | canonical |
| 5 | **C1** | [`C1_SPEC.md`](C1_SPEC.md) | passage-local commentary ("what is this passage doing?") | canonical |
| 6 | **THEME** | [`SPEC_THEME.md`](SPEC_THEME.md) | evidence-backed synthesis across C1s | new |
| 7 | **ESSAY** | [`SPEC_ESSAY.md`](SPEC_ESSAY.md) | larger argument from themes + comparison | new |
| 8 | **EDUCATION** | [`SPEC_EDUCATION.md`](SPEC_EDUCATION.md) | teaching the result clearly | new |
| 9 | **QA / FACTORY AUDIT** | [`SPEC_FACTORY_QA.md`](SPEC_FACTORY_QA.md) | the toolchain (v0/v1/v2) + the editorial loop + publication bundles | new |
| 10 | **STORAGE** | [`SPEC_STORAGE_R2.md`](SPEC_STORAGE_R2.md) | R2/S3 asset layer (source scans, media, bundles) + rights | new |
| — | **PĀṬALA INTEGRATION** | [`PATALA_INTEGRATION_BRAINSTORM.md`](PATALA_INTEGRATION_BRAINSTORM.md) | how every factory output becomes an interwoven, queryable, navigable object on the site (alternative-translation buttons, resolve kernel, concept-first reading, related-works rail, self-writing comparative essays) | design |
| — | **VISION — CHOOSE YOUR DEPTH** | [`VISION_CHOOSE_YOUR_DEPTH.md`](VISION_CHOOSE_YOUR_DEPTH.md) | the pedagogical projection layer: ORIGINAL / READ / GUIDE / STUDY / CRITICAL, progressive disclosure, and the truth-layer rule (accessible rendering may simplify a supported claim but never introduce one absent from the evidence). **Part II: the multi-resolution knowledge system** — AI tutoring by depth, misconception maps, semantic-distance model, audio/video projection, conceptual journeys, and the deepest principle (one evidence graph, multiple controlled projections) | vision |
| — | **REVIEW — FOJIN** | [`REVIEW_FOJIN.md`](REVIEW_FOJIN.md) | review of the Buddhist-canon AI platform FoJin: what to borrow (citation whitelist guard, verbatim quote verifier, eval regression gate, MCP-URN) and what we have that it lacks (editorial provenance, version-selector, depth ladder) | review |
| — | **PLATFORM — PROVENANCE-PRESERVING GENERATION** | [`PLATFORM_PROVENANCE_PRESERVING_GENERATION.md`](PLATFORM_PROVENANCE_PRESERVING_GENERATION.md) | the leap to "grounded scholarly transformations with provenance-preserving generation": claim-support guard, translation-quote verifier, relation correctness, scholarly invariant regression, dependency-aware derivation (change impact), argument verification, negative retrieval, disagreement/term-drift mining, depth-fidelity test, citation-preserving media, living essays, and **validation primitives as first-class APIs** (/verify-claim /trace-dependency /find-counterevidence …) | vision |
| — | **CONNECTIVITY — HOW IT MAPS ONTO PĀṬALA** | [`CONNECTIVITY_REVIEW.md`](CONNECTIVITY_REVIEW.md) | the verified map of every spec layer onto the EXISTING pāṭala infra (graph, evidence roles incl. contradicts, crosswalks/derived_from, assertions, trajectories, gold, bibliography, concepts, relations, MCP) — and the true gaps (ingest, validation APIs, source registration, passage-level relations, occurrence map, depth verifier) | review |

> **Corrected understanding:** the existing `data/corpus/` + `data/atlas/` already implement most of
> what the specs describe (scholarly graph, typed evidence incl. contradicts, crosswalks, assertions,
> term trajectories, gold fixtures, bibliography, concept dossiers, MCP). The specs are best read as
> *invariants the existing primitives should enforce* + a *product vision* — not blueprints for new
> subsystems. The true gaps are small and targeted (see CONNECTIVITY_REVIEW.md).

## The depth modes (frozen product model — the five reads)

```
ORIGINAL   Sanskrit
READ       faithful literary translation
GUIDE      plain-language rendering (pedagogical projection of the scholarship)
STUDY      close commentary (C1)
CRITICAL   apparatus / evidence (L200 + decisions + resolve)
```

GUIDE is generated **downward from the serious edition** and resolves every unit to the canonical
passage. It may simplify a supported claim but never introduce a claim absent from C1/Theme
evidence. This is the "choose your depth" endgame: scholar and beginner read the same passage on
the same URL at their own level.

## Cross-cutting specs (also in the factory)

| Spec | Where | Responsibility |
|---|---|---|
| Pāṭala Translation Protocol | `/root/projects/patala/docs/TRANSLATION_PROTOCOL.md` | the versioned per-passage data contract |
| Stacked Artifact | `/root/projects/patala/docs/STACKED_ARTIFACT_SPEC.md` | one dir per work, each stage a floor |
| Scholarly Evidence System | `../IPVV_SCHOLARLY_EVIDENCE_SPEC.md` | the five-pack / PCTS / gold-pack design |
| Universal Agnostic Pipeline | `../UNIVERSAL_AGNOSTIC_PIPELINE.md` | sources → translation → publication → essays |
| Pāṭala schema | `/root/projects/patala/pipeline/schema.py` | the machine passage-record (versioned, never-overwrite) |

---

## The factory loop (every new text)

```
1. SOURCE    acquire + register + witness + segment + stable IDs
2. L0/L1     literal substrate + controlled
3. L2        readable prose
4. L200      audit: anchors, decisions, source-layer, OPEN
5. C1        passage commentary (universal core + passage-type module)
6. THEME     aggregate C1s → dossier
7. ESSAY     synthesize themes + comparison + scholarship
8. EDUCATION teach the result
9. QA        v0/v1/v2 toolchain + human review → publication bundle → pāṭala
```

Any subset may be run (e.g. only SOURCE+ingest for an already-translated corpus like the IPVV).

## The factory index location

This `specs/` dir (`translations/_stack/ipvv/specs/`) is the canonical home for the factory specs.
It complements (does not duplicate) the pāṭala docs (`/root/projects/patala/docs/`) and the
research-library (`/root/projects/research-library/`). The IPVV is the first instantiation and the
gold standard; every subsequent text reuses the whole factory.

| — | **EXECUTION ORDER** | [`EXECUTION_ORDER.md`](EXECUTION_ORDER.md) | the reconciled build sequence across all threads: Phase 1 = ingest the IPVV into the pāṭala graph (the real blocker), Phase 2 = expose the validation/primitive APIs, Phase 3 = the product views (version-selector, related rail, concept map, depth verifier), Phase 4 = the generation layer, Phase 5 = the editorial loop | plan |

| — | **THE COMPANION** | [`THE_COMPANION.md`](THE_COMPANION.md) | the single onboarding doc explaining the whole system from scratch (stack, factory, QA, API, MCP, themes, vision, current state, next steps) — read first | onboarding |

| — | **THEME CLUSTERING** | [`SPEC_THEME_CLUSTERING.md`](SPEC_THEME_CLUSTERING.md) | the machine-discovery mechanism for THEMES: themes overlap (not partition), clustering is a proposal not the floor, the 7-edge hybrid relation graph, ThemeProposal (first-class, MACHINE_PROPOSED→ACCEPTED), THEME BOUNDARY, cross-work discovery, "discover computationally / adjudicate editorially" | spec |

## Phase-1 corpus build (IPVV → pāṭala)

- Process notes: `/root/projects/patala/docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` — how the canonical
  passage corpus was built, agnostically, for any work.
- Tool: `/root/projects/patala/pipeline/phase1_ipvv_corpus.py`
- Result (2026-08-12): 52 passages (49 OK / 3 NEEDS_MAPPING legacy V1), provenance resolves, 0 orphans,
  0 duplicate ids.

| — | **PĀṬALA ML** | [`PATALAML.md`](PATALAML.md) | the ML/research roadmap: typed hypergraph, multi-resolution retrieval, late-interaction (ColBERT), graph representation learning, relation motifs, the derivation DAG + VeriTrail-style verification, atomic claims, counterevidence retrieval, entailment lattice, minimal evidence sets, vertical fidelity, hyperbolic embeddings, cross-tradition alignment, executable argument graph, epistemic PageRank, scholarly community reports, and the Pāṭala benchmark — plus the 5 highest-upside experiments and the target architecture | research |

> **The meta-level insight (from PATALAML.md):** the unusual thing about Pāṭala is not scale — it is
> the **multiple explicitly derived epistemic layers over the same ancient source** (source ·
> translation · decision · commentary · theme · claim · essay · pedagogical rendering). That layered
> supervision is the ML gold.

| — | **REVIEW — PATALAML VS CODEBASE** | [`REVIEW_PATALAML_VS_CODEBASE.md`](REVIEW_PATALAML_VS_CODEBASE.md) | point-by-point review of the 20 ML ideas against the actual codebase: ~10 are substantially built as data/ontology (assertions, evidence roles incl. contradicts, crosswalk provenance, n-ary TranslationDecision, term trajectories, resolve kernel, canonical spines, theme spec), the rest are services + models over existing structure. Only ~10 are genuinely greenfield (vector retrieval, GNNs, entailment, vertical fidelity, hyperbolic, benchmark) | review |
