# REVIEW — PĀṬALA ML IDEAS vs WHAT WE HAVE

*2026-08-12. A point-by-point review of the 20 ideas in `PATALAML.md` against the actual pāṭala +
Sanskritree codebase, with honest justification of what already exists, what is partially there,
and what is genuinely new. This corrects the record: **several ideas are already substantially
implemented** in the existing data model — they are not greenfield.*

---

## The framing correction

The ML roadmap was written as forward-looking ("where Pāṭala can become interesting"). The review
shows that **the data model already anticipates most of it** — the graph primitives, evidence roles
(incl. `contradicts`), crosswalks (`derived_from`/`version_of`), assertions, translation decisions
with alternatives/evidence/review, term trajectories, gold fixtures, and the resolve kernel. So many
of the 20 ideas are about **exposing + learning over** existing structure, not building it.

---

## The verdicts

| # | Idea | What we have | Status |
|---|---|---|---|
| 1 | Typed hypergraph | `TranslationDecision` already IS an n-ary object (source_span_ids + target_span_ids + alternatives + evidence[] + review_events + method + status). `Annotation` has target + type + payload + evidence + review. These are higher-order, not pairwise triples. | **substantially built** — but as JSON objects, not a hypergraph engine |
| 2 | Multi-resolution retrieval | The layered stack IS the resolution ladder (token/span → passage → C1 → theme → work → cross-work → tradition). `canonical-spines.ts` gives cross-work structure. | **structure built** — retrieval is not query-adaptive yet |
| 3 | Late-interaction (ColBERT) | No late-interaction index. Single-vector or none. | **new** (retrieval infra) |
| 4 | Graph representation learning | `SPEC_THEME_CLUSTERING.md` specifies the hybrid relation graph (7 edges) + ThemeProposal. No GNN/embeddings yet. | **spec built, model new** |
| 5 | Relation motifs | Argument-map data exists (per chunk). No motif discovery. | **data present, model new** |
| 6 | Derivation DAG + VeriTrail | The whole stack IS a derivation DAG (Sanskrit→L0→L2→C1→theme→essay). `derived_from`/`version_of`/`witness_of` crosswalk relationships model provenance. The resolve kernel resolves any node back to source. | **architecture built** — no VeriTrail-style backward verifier service |
| 7 | Atomic claims | `assertions.ts` + `/api/assertions` — claims as first-class (subject/predicate/value + status + certainty + evidence + review). `primitives.ts` is literally "Identity/Assertion/Evidence/Provenance/Review/Rights." | **substantially built** |
| 8 | Counterevidence retrieval | Evidence `role: "contradicts"` is first-class in `primitives.ts`, `trajectories.ts`, `translation.ts`. | **data model built** — no `/find-counterevidence` service |
| 9 | Entailment lattice | No entailment classification. `DecisionStatus` (CONSTRAINED/PREFERRED/OPEN/RECONSTRUCTED) is the closest existing grain. | **new** (semantic layer) |
| 10 | Minimal evidence sets | Evidence[] is first-class on decisions/annotations. No minimality computation. | **data built, algorithm new** |
| 11 | Vertical fidelity | `SPEC_THEME_CLUSTERING.md` §4 THEME BOUNDARY + the C1 BOUNDARY/OPEN + the depth-fidelity idea are specced. No classifier. | **spec built, classifier new** |
| 12 | Misconception transformations | `trajectories.ts` (term sense-history) + `concepts.ts` (semantic-shift dossiers: kula/krama) model sense evolution. No distortion-modeling. | **data built, model new** |
| 13 | Hyperbolic embeddings | No embeddings at all yet. | **new** |
| 14 | Cross-tradition alignment | `canonical-spines.ts` (12 works across 4 traditions) + the relations graph + bibliography give the substrate. No relation-predictor. | **data built, predictor new** |
| 15 | Dynamic themes/trajectories | `trajectories.ts` is exactly term-trajectory data (diachronic sense-history). `SPEC_THEME_CLUSTERING` adds cross-work. | **substantially built** |
| 16 | Executable argument graph | Argument-map data exists per chunk (premises/objection/reply). `AnnotationType` lacks a formal "argument" node type. | **data present, formalization new** |
| 17 | Counterfactual graph analysis | No dependency-resolution engine to remove-and-trace. `derived_from`/`version_of` is the seed. | **new** |
| 18 | Epistemic PageRank | No ranking. Evidence roles + `tier` (A–E) in bibliography give the weighting seed. | **new (algorithm)** |
| 19 | Community reports | `SPEC_THEME_CLUSTERING` ThemeProposal + `concepts.ts` dossiers + the canonical-spines are community-like reports. | **substantially built** |
| 20 | Pāṭala benchmark | `gold.ts` (gold fixtures) + the v0/v1/v2 QA toolchain + the stall-log are an embryonic eval set. No formal benchmark. | **seed exists, benchmark new** |

---

## Detailed review of the big ones

### #1 Typed hypergraph — already substantially built (JSON form)
The `TranslationDecision` is **not** a binary edge; it is an n-ary scholarly object:
```ts
interface TranslationDecision {
  source_span_ids: string[];   // Sanskrit
  target_span_ids: string[];   // English
  alternatives: string[];      // rival readings
  status: DecisionStatus;
  evidence_state: EvidenceState;
  editorial_status: EditorialStatus;  // derived from review events
  method: DerivationMethod;
  evidence: EvidenceUse[];     // EvidenceItem ids
  review_events: string[];     // ReviewEvent ids
}
```
That is exactly the `TRANSLATION_DECISION` hyperedge in idea #1. Likewise `Annotation` (target +
type + payload + evidence + review + supersedes) and `Argument`-shaped data live in the argument
maps. **What's missing is a hypergraph query/embedding engine** — the ontology is already
higher-order. Verdict: the "graph→hypergraph" step is partly *already done*; the ML engine is new.

### #6 Derivation DAG + VeriTrail — architecture built, verifier service new
The entire stack is a derivation DAG, and the crosswalk relationship enum already has
`derived_from`/`version_of`/`witness_of`. The `/api/resolve` kernel resolves any node back to its
source. So "trace essay claim ← theme ← C1 ← L2 ← source span" is **structurally present**. What's
missing is the *service* that walks it backward and reports where support breaks. Verdict: the DAG
is real; the VeriTrail-style *backward verifier* is a thin service on top.

### #7 Atomic claims — already built
`data/corpus/assertions.ts` + `/api/assertions` implement exactly the `CLAIM-729` object:
subject/predicate/value + status + certainty + evidence + review_events. `primitives.ts` is titled
"Identity/Assertion/Evidence/Provenance/Review/Rights." So claim-level citations, contradiction
search, and essay-auditing **already have their substrate**. Verdict: substantially done.

### #8 Counterevidence retrieval — data model built, service new
The evidence role `contradicts` is first-class in three files (`primitives.ts`, `trajectories.ts`,
`translation.ts`). So "retrieve SUPPORT / QUALIFY / CONTRADICT" has its *data*. Missing: a
`/find-counterevidence` endpoint that returns them. Verdict: thin service on existing data.

### #15 Dynamic themes / trajectories — substantially built
`trajectories.ts` is literally diachronic sense-history (kula: lineage → body → totality), which is
idea #15's "concept trajectories through a work." `SPEC_THEME_CLUSTERING` adds cross-work. Verdict:
this is the most *already-done* idea.

### #19 Community reports — substantially built
ThemeProposal (SPEC_THEME_CLUSTERING) + concept dossiers (`concepts.ts`) + canonical spines are
scholarly community reports. Verdict: built in domain form.

---

## What is genuinely NEW (build, not reuse)

Only these require net-new infrastructure rather than "expose existing data":

1. **Late-interaction / vector retrieval** (#3) — no embedding index at all. Greenfield.
2. **Graph/hypergraph representation learning** (#4, #5) — the hybrid graph + motifs need GNNs.
3. **Entailment lattice** (#9) — no semantic entailment classification.
4. **Vertical-fidelity classifier** (#11) — specced, no model.
5. **Hyperbolic embeddings** (#13) — greenfield.
6. **Cross-tradition relation predictor** (#14) — data present, no model.
7. **Counterfactual/dependency analysis engine** (#17) — no remove-and-trace.
8. **Epistemic PageRank** (#18) — no ranking algorithm.
9. **Minimal-evidence-set algorithm** (#10) — data present, no minimality solver.
10. **The Pāṭala benchmark** (#20) — seed exists, needs formalization.

Everything else (#1, #2, #6, #7, #8, #12, #15, #16, #19) is **substantially built as data/ontology**
and needs *services + models over existing structure*, not new foundations.

---

## The recommended ordering (given what exists)

Since the data model already carries most of the substrate, the highest-leverage sequence is:

1. **Expose the existing primitives as services first** (cheap, high value):
   - `/find-counterevidence` (over the existing `contradicts` role) — idea #8
   - `/verify-claim` + `/trace-dependency` (over the DAG + resolve) — ideas #6, #7
   - `/minimal-evidence` — idea #10
2. **Then the vector layer** (late-interaction for Sanskrit) — idea #3 — unblocks semantic
   retrieval, embeddings for #4, #13.
3. **Then graph representation learning** (hybrid C1 graph → GNN) — idea #4 — the flagship experiment.
4. **Then the semantic layers** (entailment #9, vertical fidelity #11).
5. **Finally the benchmark** (#20) to make it empirical.

---

## Bottom line

**Most of Pāṭala-ML is not greenfield.** The existing `data/corpus/` model (assertions, evidence
roles incl. contradicts, crosswalk provenance, translation decisions as n-ary objects, term
trajectories, gold fixtures, the resolve kernel, the canonical spines, and the theme-clustering
spec) already implements the *ontology* behind at least 10 of the 20 ideas. The real work is
**twofold**:

1. **Expose** the existing primitives as services (`/find-counterevidence`, `/verify-claim`,
   `/trace-dependency`, `/minimal-evidence`) — thin, high-value, mostly done.
2. **Learn over** the existing structure (late-interaction retrieval, graph/hypergraph embeddings,
   entailment, vertical fidelity) — the genuinely new ML.

The meta-insight holds: the *layered supervision* (source · decision · commentary · theme · claim ·
essay · pedagogy) is the ML gold, and we already hold most of it as structured data.
