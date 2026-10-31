# EXECUTION ORDER — the consolidated build sequence (reconciled)

*2026-08-12. Reconciles every open thread into ONE correct order: the ingest-first dev plan, the
frozen integration product-model build order, the platform validation-API vision, and the
connectivity-review finding that most infra already exists.*

---

## The unifying insight

Every thread converges on the same blocker: **the IPVV is not ingested into the pāṭala graph.** The
existing pāṭala infrastructure already provides most of the machinery (graph, evidence roles,
crosswalks, assertions, trajectories, gold, bibliography, concepts, relations, MCP) AND the exporter
(`compile_published.py` + `gold_from_t1.py`) — but that exporter has only been run for
Kramasadbhāva, not the IPVV.

So the correct order is: **get the IPVV in, then expose the primitives, then add the product views.**
The frozen integration build-order (resolve → version-selector → rail → concept → essays) is correct
but its later steps all **presuppose the corpus is in the graph**.

---

## Phase 0 — Foundation (mostly done)

| step | status |
|---|---|
| Resolve kernel (immutable IDs + aliases) `lib/citation.ts` + `/api/resolve` | ✅ built this session |
| `resolve_ref` MCP tool | ✅ |
| Bibliography / relations / concepts / terms / graph schemas | ✅ existing |
| Exporter (`compile_published.py`, `gold_from_t1.py`) | ✅ existing (Kramasadbhāva) |

## Phase 1 — INGEST THE IPVV (the real blocker; do first)

The dev-plan "NOW" and the frozen build-order step 2 both reduce to this.

> **Progress (2026-08-12):** the canonical passage corpus is built. `phase1_ipvv_corpus.py`
> produces `ipvv_passages.jsonl` (52 passages: 49 OK / 3 NEEDS_MAPPING legacy V1) + the ingest
> report, reusing the L200 chunk→source-range structure. Source + L2 prose + L0 provenance all
> resolve; 0 orphans, 0 duplicate ids. Process notes:
> `/root/projects/patala/docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md`.

1. **Segment the IPVV Sanskrit** (M00020/21/22) into canonical passages → produce
   `data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl` (work_id, location, sanskrit,
   source_edition). The T1 chunks give the passage boundaries (kārikā-¶ anchored; paragraph as unit,
   kārikā as container). ✅ **done** (`phase1_ipvv_corpus.py`).
2. **Run the exporter** (`compile_published.py` pointed at IPVV) → published translation objects
   (source_spans, target_spans, alignments, decisions, evidence, provenance) for every passage.
   ✅ **done** (`token_t1_to_published.py` + `ingest_t1.py`, 231 passages ingested).
3. **Ingest L0/L2** — attach our L0 records and L2 prose to the passage records. ✅ **done** in the
   phase-1 records (l0 path + l2_text).
4. **Validate** — zero text loss + provenance resolution. ✅ **done** (ipvv_ingest_report.json).
5. **Publish the full READ view** — the entire IPVV readable + searchable, with maturity states.
   ⚠️ **partial** — passages jsonl is in pāṭala; the READ view registration still needs wiring.

**Remaining in Phase 1:**
- [ ] Resolve the 3 NEEDS_MAPPING legacy V1 chunks (or map them to their L2/embedded prose).
- [ ] Wire the phase-1 records into pāṭala's `published.ts` + passages index so `/read` and
      `/resolve` serve all 49 OK passages (the generated-unit registration script exists; the size
      made the bundle heavy — store as lazy JSON if needed).

**Why first:** nothing downstream (version-selector, related rail, concept map, validation APIs,
essays) is meaningful until the corpus is queryable in the graph.

## Phase 2 — EXPOSE THE PRIMITIVES (the platform layer)

The connectivity review found these primitives exist as *data* but aren't *served as APIs*.

6. **Validation APIs** — `/verify-claim`, `/verify-relation`, `/verify-quote`, `/trace-dependency`,
   `/find-counterevidence` — layered on the existing evidence roles (supports/contradicts/parallel/
   commentary) + crosswalk relationships (derived_from/version_of) + our resolve kernel.
7. **Register the GRETIL/IPV sources** as BibSource records + crosswalks (connects the downloaded
   sources to bibliography/related).
8. **Ingest L200 decisions + C1** as graph annotations (translation/lexical/grammar/ambiguity/
   commentary + review events).

## Phase 3 — THE PRODUCT VIEWS (the frozen build order, now unblocked)

9. **Version-selector** — alternative readings (T1/T2/R2/Pandey/Torella/Ratié) as a button over one
   source; reading-specific decisions attach to that reading; labels ALTERNATIVE vs ADVERSARIAL.
10. **Related rail** — extend relations to editorial kinds (COMMENTARY_OF / ROOT_TEXT_CONTEXT /
    CONTINUES_ARGUMENT / OPPOSING_POSITION / QUOTATION_SOURCE) + make it passage-level.
11. **Concept occurrence map** — extend the concept page to the 5-kind breakdown (OCCURRENCE /
    DOCTRINAL_INSTANCE / DEFINITION / ARGUMENT / CROSS-REFERENCE).
12. **Depth-fidelity verifier** — semantic conservation across CRITICAL/C1/GUIDE (the
    SCOPE_STRENGTHENING check).

## Phase 4 — THE GENERATION LAYER

13. **Deterministic theme synthesis** (theme → passages → C1s → comparison → outline → essay).
14. **Claim-level essay generation** (EVIDENCED / SYNTHETIC / reject-UNANCHORED; SHOW EVIDENCE at
    claim level, backed by the validation APIs).
15. **GUIDE / choose-your-depth** (progressive disclosure; the truth-layer rule enforced by the
    depth-fidelity verifier).
16. **On-demand essays + audio/video projection** (citation-preserving media).

## Phase 5 — THE EDITORIAL LOOP

17. **Human review + maturity profiles** (the review ledger; PCTS as checkbox profile).
18. **Scholarly invariant regression** as a CI gate (no dangling claims, no scope-strengthening, no
    unverified quotes).
19. **Vivṛti reconstruction** (Edition 1.1).

---

## Dependency map (why this order)

```
Phase 1 (ingest) ──────────────► unblocks Phases 2–5
   │
   ├─► Phase 2 (validation APIs) ──► feeds Phase 4 (generation guards)
   │
   └─► Phase 3 (product views)  ──► the reader/related/concept experience
                                    │
Phase 4 (generation) ◄─────────────┘ (needs validation APIs + views)
   │
   └─► Phase 5 (editorial loop) ◄── (needs everything)
```

The **frozen integration build-order** (resolve → version-selector → rail → concept → essays) is
the *product* sequence; the **dev-plan NOW/THEN/LATER** is the *engineering* sequence. They reconcile
as: Phase 1 = NOW, Phase 2–3 = THEN, Phase 4–5 = LATER.

---

## What I'd build next (the single next step)

**Phase 1, step 1–2: segment the IPVV Sanskrit + run the existing exporter.** This is the blocker
that everything else waits on. Concretely:
- parse the IPVV T1 chunks to get passage boundaries + Sanskrit,
- emit `data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl`,
- run `compile_published.py` (parameterized for IPVV) to produce the published units,
- validate zero-loss + provenance.

After that, Phases 2–3 unlock cleanly.
