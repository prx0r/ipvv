# THE COMPANION — how the whole system works (onboard a new agent)

*2026-08-12. This is the single document that explains the entire system from scratch, so a new
agent (or any model) can understand it, extend it, and use it. Read this first, then the linked
specs. It is deliberately non-web-focused — the frontend is a render; the data + APIs + pipeline are
the system.*

---

## 1. The one-line description

We are building a **multi-resolution, provenance-preserving scholarly system for Śaiva Tantra**:
an evidence graph where every translation, decision, C1, theme, and essay resolves to its source
Sanskrit, and where any model (via MCP) can answer from the corpus with deterministic
anti-hallucination guards. The first instantiation is Abhinavagupta's **IPVV**; the architecture is
text-agnostic and generalizes to Kubjikā, Tantrāloka, a Buddhist text, or a ritual manual.

---

## 2. The core pattern (the stack)

```
SOURCE (Sanskrit, edition, witness)
  → L0  literal token/gloss substrate ([and]-gloss (IAST))
  → L1  controlled, Sanskrit-close translation
  → L2  the readable published prose
  → L200 cross-layer audit (how the reading was derived: decisions, source-layer, OPEN)
  → C1  passage-local commentary ("what is this passage doing?")
  → THEME  evidence-backed synthesis across C1s
  → ESSAY  larger argument from themes + comparison + scholarship
  → EDUCATION  teaching the result (GUIDE, lessons)
```

Every layer points **back down** (provenance). The deepest principle:

> One evidence graph, multiple controlled explanatory projections over it.

---

## 3. The two QA jobs (never conflate)

```
TASK 1 — READER QA:   can the published prose carry the argument?        (prose-only)
TASK 2 — FIDELITY QA: is the L2 reconstruction licensed by the source?  (map+L1+L0+Sanskrit)
```
- **v0 scaler** — deterministic triage: FILE_ARTIFACT (regex), TERM_INTRODUCTION. `translations/tools/qa_scaler.py`.
- **v1 Task-1** — prose-only reader QA. Gold was over-logged; re-grade before trusting recall. `qa_v1_*.py`, `V1_THREE_CONDITION_FINDINGS.md`.
- **v2 Task-2** — scholarly fidelity vs the source stack. `qa_v2_fidelity.py`. Canonical chunks: 18 PASS / 1 flag.

---

## 4. The factory (the agnostic translation→publication pipeline)

### 4.1 The source layers live in Sanskritree (`/mnt/HC_Volume_106427611/sanskritree`)
- **T1 chunks** (token-gloss `[and]-gloss (IAST)`): `translations/_stack/ipvv/02_t1/` (Vol 2–3, 35 files) + `01_t1/` (Vol 1).
- **L0 records**: `translations/_stack/ipvv/l0/*.jsonl` (extracted by `translations/tools/t1_extract.py`).
- **L2 reads**: `translations/_stack/ipvv/pilot/pilot_*_L2_read.md`.
- **L200 audit**: `translations/_stack/ipvv/l200/` (64 files; 3 canonical: V2-O, V3-B, V3-C).
- **C1**: `translations/_stack/ipvv/c1/` (the C1_SPEC + exemplars).
- **Sources/witnesses**: `corpus/ipvv-anchor/primary/` (GRETIL IPK+Vṛtti, GRETIL IPV, Torella, KSTS, acquisition manifest).

### 4.2 The ingest bridge lives in pāṭala (`/root/projects/patala/pipeline/`)
The factory converts Sanskritree's token-T1 into pāṭala's published objects. **Agnostic** — any work with token-gloss T1 flows through it:

```
token_t1_to_published.py   token-T1 → PublishedTranslation (source_spans, target_spans, alignments, decisions, evidence)
ingest_t1.py               run the converter across a work's T1 dir → passage index jsonl + generated units
compile_published.py       (legacy, Kramasadbhāva) T3 stack → published objects
gold_from_t1.py / from_t1.py   T1 → schema-valid gold records
audit.py / validate.py / validate_graph.py   invariant checkers
schema.py / model.py / state_machine.py / prompts.py   the versioned T1→C1 pipeline machinery
```

Usage:
```
python3 pipeline/ingest_t1.py --work <work_id> --t1-dir <path> --write
```

The IPVV is already ingested: **231 passages** in `data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl` + 35 generated unit files.

### 4.3 The site data (pāṭala `data/`)
- `data/atlas/` — the knowledge graph: `texts.ts`, `traditions.ts`, `people.ts`, `concepts.ts` (concept dossiers), `relations.ts` (typed+confidence+evidence), `bibliography*.ts` (sources/translations/scholarship + provenance tiers), `resources.ts`.
- `data/corpus/` — the machine model: `graph.ts` (objects + annotations), `primitives.ts` (Identity/Assertion/Evidence/Provenance/Review/Rights + evidence roles incl. contradicts/parallel), `translation.ts` (PublishedTranslation), `passages.ts` (+ `.jsonl`), `terms.ts` + `trajectories.ts` (term sense-history), `gold.ts` (regression fixtures), `relations.ts`, `manuscripts.ts`, `crosswalks`, `published.ts` (the registry).

### 4.4 The API surface (pāṭala `app/api/`)
- `/api/resolve?ref=...` — the citation backbone (immutable ids + aliases) — **the key piece**.
- `/api/passages/:id/translation` — the auditable published object.
- `/api/context/passages/:id` — passage + work + manuscripts + neighbors + tracked terms + related + translations + rights.
- `/api/relations/:work_id`, `/api/terms/*`, `/api/search/passages`, `/api/assertions`, `/api/crosswalks`, `/api/manuscripts`, `/api/decisions/:id`, `/api/concordance`, `/api/works/*`.

---

## 5. Machine access — how ANY model uses the corpus (the "hack" that's a feature)

The **MCP server** (`mcp/index.mjs`) is the machine-access point. It turns the corpus into
callable infrastructure so Claude/ChatGPT/opencode can answer *from* it with provenance. Currently
exposed: `resolve_ref`. The full toolset to build (per the platform vision):

```
search_corpus      semantic search → passages with URNs
read_passage       read a passage's content
get_parallels      cross-canon / rival-reading parallels
lookup_dictionary  term lookup
lookup_entity      knowledge-graph entities
resolve_urn        resolve a reference → immutable passage
verify_quote       open-world verbatim quote check (anti-hallucination)
verify_claim       claim → support-path check
trace_dependency   "revise MT-031 → what goes stale?"
find_counterevidence  what tensions/contradicts this claim?
```

**Yes — this makes any model able to translate/answer grounded in the corpus.** That is the point:
the corpus becomes infrastructure. The difference from raw LLM translation is the **deterministic
verification floor** (citation guard + quote verifier + claim-support) below which model judgment
never operates. See `PLATFORM_PROVENANCE_PRESERVING_GENERATION.md`.

---

## 6. THEMES — the next layer (the advice: don't hand-pick)

**Do NOT hand-assemble themes** from hand-picked passage lists. Use **unsupervised discovery over
the C1s**. The C1 layer is substantially complete (85 files in `c1/`, 10 with the structured
machine-facing `c1/source/` records — SUMMARY/FUNCTION/KEY TERMS/LOCAL CONTEXT/EXPLANATION/
BOUNDARY/RELATED):

```
~60+ C1s (embed the structured ones; the rest can be derived)
  → embed each C1 (SUMMARY/FUNCTION/KEY TERMS/RELATED)
  → cluster (HDBSCAN/k-means)   ← machine proposes groupings
  → LLM names + synthesizes each cluster into a dossier (CORE QUESTION / RELEVANT C1s /
    RECURRING CLAIMS / TERMS / DEVELOPMENT / TENSIONS)
  → human adjudicates the cluster labels/merges
```

Why: it's agnostic (same code for any corpus), discovers emergent structure (themes the essays
didn't pre-anticipate), the evidence trail is automatic (cluster = RELEVANT C1s), and it scales.
The theme dossier is a *derived* view over the cluster — machine-proposed, human-approved. The
essays then cite the theme dossiers, which cite the C1s, which cite the passages — closing
`TEXT → C1 → THEME → ESSAY`.

---

## 7. The product vision (the endgame)

- **Choose your depth**: ORIGINAL / READ / GUIDE / STUDY / CRITICAL — scholar and beginner read the
  same passage on the same URL.
- **Multi-resolution knowledge system**: AI tutoring by depth, misconception maps, semantic-distance
  model, audio/video projection, conceptual journeys — all derived from the one evidence graph.
- **The deepest rule**: accessible renderings may simplify a supported claim but never introduce a
  claim absent from the evidence.

See `VISION_CHOOSE_YOUR_DEPTH.md`, `IPVV_SCHOLARLY_EVIDENCE_SPEC.md`,
`UNIVERSAL_AGNOSTIC_PIPELINE.md`, `PATALA_INTEGRATION_BRAINSTORM.md`.

---

## 8. What the specs/ are (the canonical set)

All in `translations/_stack/ipvv/specs/`:

| doc | what it is |
|---|---|
| `README_FACTORY_INDEX.md` | the index of all specs |
| `SPEC_SOURCE.md` … `SPEC_EDUCATION.md`, `SPEC_FACTORY_QA.md`, `SPEC_STORAGE_R2.md` | the per-layer factory specs |
| `C1_SPEC.md` | the canonical C1 spec (passage commentary) |
| `IPVV_SCHOLARLY_EVIDENCE_SPEC.md` | the five-pack / PCTS / gold-pack design |
| `UNIVERSAL_AGNOSTIC_PIPELINE.md` | sources → translation → publication → essays |
| `PATALA_INTEGRATION_BRAINSTORM.md` | the frozen product model (frozen 2026-08-11) |
| `PLATFORM_PROVENANCE_PRESERVING_GENERATION.md` | validation primitives as first-class APIs |
| `VISION_CHOOSE_YOUR_DEPTH.md` | the multi-resolution vision |
| `CONNECTIVITY_REVIEW.md` | how everything maps onto the existing pāṭala infra + true gaps |
| `EXECUTION_ORDER.md` | the reconciled build order |
| `PATALAML.md` | the ML/research roadmap (hypergraph, multi-res retrieval, claims, counterevidence, vertical fidelity, argument graph, benchmark) |
| `REVIEW_FOJIN.md` | review of the sibling Buddhist-canon project |

---

## 9. The current state (honest) + the recommended next steps

**Done:** resolve kernel + `/api/resolve` + MCP `resolve_ref` · the agnostic `ingest_t1.py` bridge ·
IPVV Vols 2–3 ingested (231 passages) · **Phase-1 canonical corpus (52 passages, 49 OK / 3
NEEDS_MAPPING, provenance resolves — see `PHASE1_IPVV_CORPUS_PROCESS_NOTES.md`)**
· v0/v1/v2 QA toolchain · L200 (64) · C1 spec + exemplars · the spec set (incl. the new
`SPEC_THEME_CLUSTERING.md` for machine-proposed, human-adjudicated themes) ·
**Phase 0A–0C + Phase 2 (this session):** 49 passages published as lazy JSON with C1
(`verse_commentary[]`, V1 multi-C1) + c1_source · 63 c1/source records · `/api/themes` + `get_themes`
MCP · the 4 deterministic verify services (`/api/verify/*`) + MCP tools · `BENCHMARK_HANDOVER.md`.

**Gaps (in order):**
1. **THEME discovery** — build the C1 hybrid relation-graph → clustering → ThemeProposal → human
   adjudication pipeline (`SPEC_THEME_CLUSTERING.md`). The mechanism is specified; build it.
2. **Complete the C1 structured records** — done (63 now; see Phase 0B).
3. **Extend the MCP toolset** — the verify/themes tools are in; search/read/parallels remain.
4. **Ingest the L200 + decisions into the pāṭala graph** as annotations (connect the audit to the
   graph).
5. **The validation APIs** — the 4 verify services are shipped; extend with semantic entailment
   (the ML master's Phase 5).
6. **Finish Phase-1** — the 3 NEEDS_MAPPING legacy V1 chunks are documented (`T1_ONLY_NO_L2`).

**Do NOT touch the web frontend until the data + APIs are complete** — it is a render; data is king.

---

## 10. Key files to open first

- This companion + `README_FACTORY_INDEX.md`
- `data/corpus/graph.ts` + `primitives.ts` (the machine model)
- `pipeline/ingest_t1.py` + `token_t1_to_published.py` (the bridge)
- `lib/citation.ts` + `app/api/resolve/route.ts` (the citation backbone)
- `mcp/index.mjs` (the machine-access point)
- `translations/tools/qa_v2_fidelity.py` (the fidelity QA)
