# HANDOVER-PLANS — the full roadmap for what's next
*2026-08-12. Everything a future agent needs to continue from where this session stopped, in execution
order, with the WHY for each step. Read this alongside `HANDOVER-IPVV-LAYERS-2026-08-12.md` (what exists)
and `README.md` (the layer stack). This is the forward-looking plan; the other handover is the
backward-looking record.*

> **NEW-AGENT ENTRY PROTOCOL:** read these IN ORDER before doing anything —
> `IPVV-KNOWLEDGE-CORE.md` (the deep WHY: the philosophy + editorial discipline) → `README.md`
> (the architecture) → `HANDOVER-IPVV-LAYERS-2026-08-12.md` §9 (the entry protocol + what exists) →
> this file (the roadmap). Then pick the relevant spec in §9 of that handover for your task.

---

## 0. WHERE WE ARE (the state of the stack)

```
SOURCE (M00020/21/22 + Torella's IPK)          ✅ translated
L0/L1 token-level + controlled                   ✅ (l0/, l0_v1/)
L2 READ (book prose)                            ✅ (63, in pilot/)
L200 AUDIT (how each reading was derived)       ✅ (63 audits, all editor-reviewed)
C1 COMMENTARY (what each passage means)         ✅ (63 read + 10 source records)
THEMES (what pattern emerges)                   🔶 PILOTED, not built (see §1)
PARALLELS (cross-textual witnesses)             ⬜ not started (see §2)
ESSAYS (what larger argument follows)           ✅ (22 essays in research-library)
EDUCATION (how we teach it)                     ⬜ not started (see §4)
```

**The two live plans for immediate next work are THEMES and PARALLELS.** The pilot proved the THEMES
mechanism works; the full build is the natural next step. PARALLELS follows it. This document orders
everything.

---

## 1. THEMES — build the full layer (the immediate next step)

### Why now
The C1 layer is done (63), and the pilot (`THEMES_PILOT_REPORT.md`) proved the mechanism: the hybrid
relation-graph recovers the known IPVV themes, keeps multi-theme overlap, and separates
lexically-similar-but-doctrinally-different passages. **The next step is to scale the pilot into the
full 63-C1 run** — the same machinery, production-grade.

### The mechanism (from `SPEC_THEME_CLUSTERING.md`, the corrected spec)
```
C1s
  ↓
hybrid relation graph (semantic + shared terms + curated RELATED + sequence + interlocutor + function)
  ↓
community detection (Louvain/Leiden) over the graph    ← NOT HDBSCAN (the pilot favored graph community detection)
  ↓
overlapping candidate neighborhoods
  ↓
ThemeProposal (members + edge evidence + proposed name)   ← the first-class object
  ↓
LLM names + synthesizes each proposal
  ↓
human merge / split / multi-assign / add-missed
  ↓
ACCEPTED THEME (overlapping; memberships carry strength + role; THEME BOUNDARY)
```

### The concrete steps (in order)
1. **Build the hybrid graph over all 63 C1s.**
   - Semantic edge: embed the C1s (sentence-transformers or API). The pilot used key-term Jaccard as a
     proxy; production should use real embeddings.
   - Structured edges: pull the curated `See also` relations (the pilot has them as `CURATED`); add the
     shared-KEY-TERMS edges; add concept/sequence/interlocutor/function when available.
   - **Weight the edges** (the pilot used semantic 0.4 + curated 0.4 + shared-term 0.2; tune).
   - ⚠️ **Do NOT use shared body-words** — the pilot proved they over-connect everything (noise). Use
     curated `See also` + KEY TERMS only.
2. **Run community detection (Louvain/Leiden)**, not HDBSCAN. The C1s are already linked by curated
   relations, so the graph is the natural substrate. Allow **overlapping communities** (Louvain
   variants support overlap; or run the graph + then multi-assign borderline nodes).
3. **Create ThemeProposals** — each with `clustering_run`, `members` (id + strength + role),
   `edge evidence` (which edges justify each membership), `proposed_name`, `proposed_core_question`,
   `status: MACHINE_PROPOSED`.
4. **LLM synthesizes a draft dossier** per proposal, grounded ONLY in its members (CORE QUESTION /
   RELEVANT C1s / RECURRING CLAIMS / IMPORTANT TERMS / DEVELOPMENT / TENSIONS / PRIMARY EVIDENCE /
   THEME BOUNDARY).
5. **Human adjudicates**: merge / split / multi-assign / add a theme the machine missed / set
   membership roles (DEFINES/ESTABLISHES/DEVELOPS/APPLIES/QUALIFIES/CONTRASTS). Accept →
   `status: ACCEPTED`.
6. **Run the validator**: every member C1 exists; every claim traces to a C1→passage; every theme
   records its provenance (proposal → run → members).
7. **Save separately**: `themes/proposals/` (the machine output) and `themes/accepted/` (the editorial
   result). Never overwrite the original run.
8. **Expose via MCP/API**: query by theme → its C1s → passages; query a C1 → all its themes.

### The expected outcome (from the pilot, scaled)
- ~8–12 theme proposals; most ACCEPTED with light editing; a few merged/split.
- **2+ novel themes** the essays didn't pre-anticipate (the pilot already surfaced
  "order-less support / non-constructed self" and "difference-as-contrast-to-unity").
- The ThemeProposal lifecycle answers "why is V2-O in this theme?" from the edge evidence.

### Why this order (and why not the other way)
THEMES first because it's the layer directly above C1 — it's the "what pattern emerges" step, and the
PARALLELS and ESSAYS layers both consume it. Don't do PARALLELS before THEMES (a theme is needed to know
which cross-text witnesses matter). Don't do ESSAYS-new before THEMES (the essays should cite themes).

---

## 2. PARALLELS — the cross-textual witnesses (after THEMES)

### Why
Dyczkowski's Spandakārikā model — for each passage, the witnesses from other works that support /
qualify / contradict it. This is the "comparison pack + negative retrieval" layer. It's separate from
C1 (C1 stays passage-local; the spec records this). It feeds the essays' comparative dimension.

### The mechanism
```
ACCEPTED THEMES (and their C1s)
  ↓
for each C1, gather cross-textual witnesses (same author's other works, adjacent traditions, opponents)
  ↓
type each: supports · qualifies · contradicts   ← the existing evidence roles
  ↓
cross-work thematic graph
  ↓
essay hypotheses
```

### The concrete steps
1. For each theme's core C1s, list the candidate witnesses:
   - **same author**: the Tantrāloka, the Spandakārikā-commentary, the Parātriṃśikā — "the same move,
     stated differently."
   - **adjacent traditions**: the Spanda's pulse, the Śivasūtra's Fourth, the Vijñānabhairava's ways.
   - **opponents**: the Buddhist apoha, the Advaitin's ignorance — as `contradicts`.
2. Type each witness (supports/qualifies/contradicts) and record the shared move.
3. Build the **cross-work thematic graph**: a theme across IPVV + IPV + Tantrāloka + Spanda + Kubjikā
   (intra-work first, then cross-work; reuse the same clustering tooling).
4. The PARALLELS feed the ESSAYS — an essay cites its theme → its C1s → its cross-text witnesses.

### The comparative corpus (already on disk)
`/root/projects/tantraloka/texts-original/` — Tantrāloka (11 vols), Spandakārikā, Śivasūtra,
Vijñānabhairava, GRETIL (Nyāyasūtra, Nyāyabindu, Vākyapadīya). The essays already established the
comparative frame (see `ESSAY-SPANDA-IPVV`, `ESSAY-TWO-ABHINAVAGUPTAS`, etc.) — PARALLELS systematizes
it.

### Why after THEMES
The witnesses matter per-theme: "which cross-text parallels bear on recognition?" is answerable only
after the recognition theme exists. And the cross-work graph needs the intra-work themes first.

---

## 3. THE c1/source/ STRUCTURED RECORDS — complete the machine surface

### Why
Only 10 of 63 C1s have the structured `c1/source/` records (the machine-friendly SUMMARY/FUNCTION/KEY
TERMS/.../BOUNDARY/RELATED). The read/ renderings exist for all 63, but the structured records are what
the API/MCP and the embedding should use. Completing them improves both the THEMES input (better
features) and the machine access.

### The step
Generate the `c1/source/` record for each of the remaining 53 C1s — derive it from the read/ body (the
SUMMARY ≈ body; FUNCTION/LOCAL CONTEXT from the argument map; KEY TERMS from the Terms: field; BOUNDARY
from the body's boundary sentence; RELATED from the See also). This is a mechanical-but-verified
derivation, not hand-writing from scratch.

---

## 4. EDUCATION — the pedagogy layer (after THEMES + PARALLELS)

### Why
The final layer: how we teach the result. Only meaningful once READ/COMMENTARY/AUDIT/THEMES/ESSAYS are
populated. The spec exists (`SPEC_EDUCATION.md`).

### The step
Lessons/explainers per theme, building from the C1s (which explain the passages) up to the essays (which
argue the synthesis). The "progressive disclosure" the Dyczkowski review identified — READ/GUIDE/STUDY/
CRITICAL.

---

## 5. THE PATALA SITE — deepen the machine-facing layer

### Why
The IPVV is registered in patala (the work, text entity, 1.5.11 published unit, overview page, concept,
learning block). The site is the machine-access point — and the MCP server (`patala/mcp/index.mjs`) is
how any model reaches the corpus.

### The steps
1. **Add more IPVV passages** to patala — the V2/V3 generated units exist (`data/corpus/units/
   *-generated.ts`); wire the read/commentary/audit in.
2. **Extend the MCP toolset** from the current `resolve_ref` to the roadmap: `search_passages`,
   `read_passage`, `verify_quote` (the citation guard), `verify_claim` (the claim-support floor),
   `trace_dependency`. This is the provenance-preserving-generation machine access.
3. **Expose the THEMES + PARALLELS + C1 layers** via the API once built.
4. **The `specs/` folder** at `sanskritree/translations/_stack/ipvv/specs/` already contains
   `PATALA_INTEGRATION_BRAINSTORM.md`, `PLATFORM_PROVENANCE_PRESERVING_GENERATION.md`, `REVIEW_FOJIN.md`,
   `CONNECTIVITY_REVIEW.md`, `EXECUTION_ORDER.md`, `VISION_CHOOSE_YOUR_DEPTH.md` (parallel-session work)
   — read these before extending the site.

---

## 6. THE VERIFICATION / QA LAYER (ongoing)

### The floor (deterministic, not model-dependent)
- **L200 validator**: `l200_validate.py` — run after any L200 change (structure, L0 ranges, crossrefs,
  review meta, no-stray, non-empty).
- **The citation guard + quote verifier + claim-support** (from `SPEC_FACTORY_QA.md` and
  `PLATFORM_PROVENANCE_PRESERVING_GENERATION.md`) — the floor below which model judgment never operates.
- **The THEMES validator**: every theme's members exist; every claim traces to a C1→passage; every theme
  records its provenance.

---

## 7. THE CROSS-CUTTING RULES (do not regress)

1. **C1 is compact and local** — no modern comparison, no essays as evidence, no PARALLELS inside C1.
   The `_essay-material-legacy/` C1s are assets for THEMES/ESSAYS, not C1.
2. **Themes overlap** — a C1 has a primary_theme + multiple member_of. Not a partition.
3. **Clustering is a proposal, not the deterministic floor** — the floor is structural evidence.
4. **Discover computationally; adjudicate editorially.**
5. **Never overwrite the canonicals** (`l200_migrate.py`/`l200_standardize.py` skip V2-O/V3-B/V3-C and
   the hand-authored V3-I..P); never overwrite the original theme proposals.
6. **The originals are the provenance** — `l200_legacy/`, `c1/_essay-material-legacy/`, `themes/proposals/`.

---

## 8. THE PRIORITY ORDER (what to do, and why)

| Priority | Task | Why |
|---|---|---|
| **1** | **Build THEMES over all 63** (community detection, ThemeProposal lifecycle) | the layer directly above C1; everything else consumes it; the pilot proved it |
| **2** | **Complete the c1/source/ records** (53 remaining) | better THEMES input + the machine surface |
| **3** | **Build PARALLELS** (cross-textual witnesses per theme) | the comparative layer; feeds the essays |
| **4** | **Extend the MCP toolset** (verify-quote/claim, trace-dependency) | the machine access + the deterministic floor |
| **5** | **Build the cross-work thematic graph** (IPVV + IPV + TĀ + Spanda + Kubjikā) | the tradition-agnostic, multi-work value |
| **6** | **Build EDUCATION** | the final layer, once the lower layers are settled |
| **7** | **Deepen patala** (more passages + the API exposure) | the machine-facing delivery |

**The single highest-value next action:** build THEMES over all 63 C1s using community detection over
the hybrid graph, producing ThemeProposals → human-adjudicated ACCEPTED THEMES, with the edge-evidence
provenance. The pilot already proved the mechanism and surfaced 2 novel themes; scaling it is the
natural completion.

---

*This is the forward plan. THEMES (community detection over the hybrid graph) is the immediate next
build, having been piloted and proven; PARALLELS and the c1/source completion follow; then the MCP
toolset, the cross-work graph, EDUCATION, and deeper patala integration. The cross-cutting rules —
overlap not partition, clustering as proposal not floor, discover-computationally-adjudicate-
editorially, never overwrite the canonicals/originals — govern all of it. Read `HANDOVER-IPVV-LAYERS-
2026-08-12.md` (what exists) + this plan (what's next) + `README.md` (the stack) + the specs/ to resume
anywhere.*
