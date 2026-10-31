# CONNECTIVITY REVIEW — how the specs map onto the EXISTING pāṭala infra

*2026-08-12. The honest, verified answer: **most of what the specs and visions call for already
exists in the pāṭala codebase.** The specs were partly written as new-architecture because the full
pāṭala data model wasn't in view. This review maps each layer onto what is already implemented,
identifies the TRUE gaps, and corrects the record.*

---

## 0. The headline finding

The existing `data/corpus/` + `data/atlas/` + `app/api/` already implement the majority of the
"platform" vision:

| Spec/vision layer | Already exists in pāṭala | Where |
|---|---|---|
| scholarly graph (objects + annotations) | **yes** — Objects (Work/Witness/Passage/Span/…) + Annotations | `data/corpus/graph.ts` |
| evidence roles incl. **contradicts/parallel/commentary** | **yes** (negative retrieval built-in) | `data/corpus/primitives.ts` |
| **dependency/provenance** (`derived_from`, `version_of`, `witness_of`) | **yes** | `primitives.ts` crosswalk relationship |
| **living revisions** (`supersedes`/`superseded_by`) | **yes** | `graph.ts`, `translation.ts` |
| **disagreement as first-class** (assertions) | **yes** — subject/predicate/value + status + evidence + reviews | `app/api/assertions` |
| **federation/crosswalks** | **yes** — our↔external, resolve-don't-duplicate | `app/api/crosswalks` |
| **semantic-distance / term-drift** | **yes** — term trajectories (diachronic sense-history) | `data/corpus/trajectories.ts` |
| **scholarly regression gate** | **yes** — gold fixtures | `data/corpus/gold.ts` |
| concept dossiers (kula/krama semantic shifts) | **yes** | `data/atlas/concepts.ts` |
| typed relations (related texts) | **yes** — 8 relation types × confidence × evidence | `data/corpus/relations.ts` + `data/atlas/relations.ts` |
| bibliography (sources/translations/scholarship + provenance tiers) | **yes** | `data/atlas/bibliographyTypes.ts` + `bibliographySeed.ts` |
| term ledger + proposals | **yes** | `data/corpus/terms.ts`, `data/terms.json` |
| citation backbone | **partial** — `/api/resolve` + `lib/citation.ts` (we just built) | — |
| MCP server | **yes** | `mcp/index.mjs` |

**Bottom line:** the existing infra is a mature scholarly-graph platform. Our specs are best read as
a *specification of what the existing primitives should enforce*, not a request to build new ones.

---

## 1. Where each spec layer actually lives

### SOURCE (SPEC_SOURCE)
- Works/witnesses/editions/rights → `data/atlas/bibliographyTypes.ts` (`BibSource`, `BibTranslation`,
  rights) + `data/corpus/works.ts` + `manuscripts.ts`.
- Stable IDs / aliases → our new `lib/citation.ts` (immutable `pt:pid` + aliases) + the existing
  `tantra:text:` / `pt:passage:` scheme.
- **Gap:** the per-passage witness record + variant-notes as first-class data (partially in
  bibliography; not yet per-passage in the corpus jsonl).

### L0 / L1 / L2 (SPEC_L0_L1, SPEC_L2)
- `data/corpus/translation.ts` holds the translation object (source spans, target spans, decisions,
  evidence). L0/L1/L2 as *layers* are not yet a first-class enum — the corpus holds
  `close_translation`; L1 exists only in Sanskritree.

### L200 (audit)
- The L200 spec in Sanskritree (`translations/_stack/ipvv/l200/`) is the *editorial* audit. The
  pāṭala graph's **annotations** (translation/lexical/grammar/ambiguity + evidence + review) are the
  *machine* realization of it.
- **Gap:** L200 files (Sanskritree) are not yet ingested into the pāṭala graph as annotations.

### C1 (commentary)
- `data/corpus/graph.ts` has `commentary` as an annotation type. The C1 files are in Sanskritree
  (`translations/_stack/ipvv/c1/`).
- **Gap:** C1 files → commentary annotations (ingest).

### THEME / ESSAY / EDUCATION
- **Concept dossiers** (`data/atlas/concepts.ts`) = the theme layer. **Term trajectories**
  (`trajectories.ts`) = concept development.
- **Gap:** essays/education (research-library) are not linked into the graph as nodes; no
  essay-claim → evidence graph yet.

### QA / validation / provenance-preserving generation (PLATFORM spec)
- **Already there:** evidence roles (`supports`/`contradicts`/`parallel`/`commentary`), crosswalk
  relationships (`derived_from`/`version_of`), `supersedes`/`superseded_by`, gold fixtures, and the
  assertions API (disagreement as first-class).
- **True gaps (what to actually build):**
  1. **verify-claim / verify-relation / verify-quote APIs** — the platform spec's validation
     primitives. Only `/api/resolve` exists so far.
  2. **dependency-impact tracing** — `derived_from` exists as a crosswalk *relationship*, but there's
     no `/trace-dependency` that walks "revise MT-031 → which C1/theme/essay/guide/audio go stale?".
  3. **depth-fidelity check** (semantic conservation across CRITICAL/C1/GUIDE) — not built; the
     concept dossiers give semantic-distance *content* but not a *vertical verifier*.
  4. **negative-retrieval as a served view** — `contradicts` evidence exists as data; there's no
     `/find-counterevidence` endpoint surfacing it per claim.

---

## 2. Related texts / bibliography / concepts — how they connect

### Related texts (the "Netflix rail")
- **Already works:** `data/corpus/relations.ts` (typed × confidence × evidence) powers
  `relationsFor(workId)`, exposed via `/api/relations/:work_id` and the MCP `get_related_works`. The
  context API already returns `related_works`.
- **Gap (per the brainstorm):** the rail is *work-level*, not *passage-level*, and the relation
  kinds are the atlas set (influence/synthesis/parallel) rather than the editorial set
  (COMMENTARY_OF / ROOT_TEXT_CONTEXT / CONTINUES_ARGUMENT / OPPOSING_POSITION / QUOTATION_SOURCE).
  Extending the kinds + surfacing passage-level related would realize the "because you read X"
  rail.

### Bibliography
- **Already rich:** `bibliographyTypes.ts` (sources/translations/scholarship + provenance tiers) +
  `bibliographySeed.ts` (70 texts) + `/api/bibliography` page. The IPVV/IPK/IPV/Vivṛti records exist
  with `statusChecked`/`statusEvidence`.
- **Gap:** the downloaded GRETIL IPK/Vṛtti + IPV sources are in Sanskritree but **not yet registered
  as BibSource records** or wired as crosswalks into the bibliography.

### Concepts
- **Already rich:** concept dossiers with semantic-shift trajectories (kula, krama) — the
  "semantic-distance" idea is substantially implemented in `trajectories.ts` + `concepts.ts`.
- **Gap:** the concept page shows a dossier, not yet the **occurrence map by kind** (OCCURRENCE /
  DOCTRINAL_INSTANCE / DEFINITION / ARGUMENT / CROSS-REFERENCE) from the brainstorm §3.

---

## 3. The TRUE gaps (what to build — small, targeted)

Ranked by leverage, all building ON existing primitives:

1. **Ingest the IPVV corpus into the graph** (M0 — the real blocker). Turn Sanskritree's
   T1/L0/L2/L200/C1 into pāṭala objects+annotations. Everything else assumes this.
2. **Validation APIs** (`/verify-claim`, `/verify-relation`, `/verify-quote`, `/trace-dependency`,
   `/find-counterevidence`) — the platform spec's primitives, layered on the existing evidence
   roles + our resolve kernel.
3. **Register the GRETIL/IPV sources** as BibSource records + crosswalks (connects the downloaded
   sources to the bibliography/related).
4. **Passage-level + editorial relation kinds** for the related rail (extend the relation types).
5. **Concept occurrence map by kind** (extend the concept page with the 5-kind breakdown).
6. **Depth-fidelity verifier** (semantic conservation across CRITICAL/C1/GUIDE).

**Not needed (already exist):** the graph model, evidence roles, crosswalks, assertions, gold
fixtures, trajectories, bibliography schema, term ledger, MCP server, and the base reader.

---

## 4. The corrected relationship between the specs and the infra

The specs (`specs/*.md`) are **not** blueprints for new subsystems. They are:
- a **specification of invariants** the existing primitives should enforce (evidence role
  completeness, no dangling claims, no scope-strengthening);
- a **product vision** (choose-your-depth, multi-resolution, provenance-preserving generation) that
  the existing graph + new validation APIs make possible;
- a **roadmap** that mostly reduces to "**ingest the corpus, then expose the existing primitives as
  the validation APIs.**"

The `data/corpus/graph.ts` comment is the guide: *"The durable model that must survive years, so it
is deliberately small and conservative."* The specs should be reconciled to it, not duplicate it.

---

## 5. Recommended next actions

1. **Reconcile the specs** to the existing graph model (mark which parts are already-implemented vs
   new) — so the docs don't mislead a future agent into rebuilding what exists.
2. **Build the ingest** (Sanskritree IPVV → pāṭala graph objects+annotations) — the single blocker.
3. **Add the validation APIs** on top of the existing evidence roles + resolve kernel.
4. **Wire the GRETIL/IPV sources** into the bibliography + crosswalks.
