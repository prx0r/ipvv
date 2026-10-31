# HANDOVER — IPVV LAYERED EDITION: L200 AUDIT + C1 COMMENTARY + RECOGNITION LIBRARY
*2026-08-12. A complete record of this session's work, the files created, and — critically — HOW TO DO
IT AGAIN, so any future agent can reproduce or extend any part of it. Companion to `README.md` (the
layer stack) and the individual specs. Read `README.md` and this handover first.*

---

## 0. THE LAYERED EDITION (the architecture in one screen)

```
SOURCE  (M00020/21/22 + Torella's IPK)
  ↓
L0 / L1      token-level / controlled translation        (l0/, l0_v1/)
  ↓
L2 READ      real book prose                              (pilot/pilot_*_L2_read.md)
  ↓
L200 AUDIT   how each reading was derived                 (l200/, the audit)
  ↓
C1 COMMENTARY what each passage means (compact, local)    (c1/read/ + c1/source/)
  ↓
THEMES       what pattern emerges across passages         (TO BUILD)
  ↓
PARALLELS    cross-textual witnesses (supports/qualifies/contradicts)  (TO BUILD — later)
  ↓
ESSAYS       what larger argument follows                 (research-library/recognition/)
  ↓
EDUCATION    how we teach it                              (TO BUILD)
```

**The whole IPVV (Vols 1–3, ~34,000 lines) is translated.** This session built the L200 audit layer
and the C1 commentary layer on top of that, and produced a recognition essay library.

---

## 1. THE L200 AUDIT LAYER (the derivation ledger)

**What it is:** L200 answers *"how did we get from the Sanskrit to the published English?"* — a strict
8-section audit per chunk: IDENTIFICATION / PUBLISHED READING / DERIVATION MAP / MATERIAL TRANSLATION
DECISIONS / INTERPRETIVE ASSERTIONS / SOURCE LAYER / CROSS-REFERENCES / REVIEW STATE. It is NOT a
commentary (that is C1) and NOT a readable summary (that is L2). The key discipline: **translation
decisions (SUPPLIED/REFERENT_SUPPLY/STRUCTURAL_CONNECTIVE/LEXICAL/GRAMMATICAL) are strictly separated
from interpretive assertions (IA-###), which feed C1.**

### Files
- **`l200/README-L200-SPEC.md`** — the frozen 8-section schema + the decision-type taxonomy (READ THIS).
- **`l200/INDEX-AND-REVIEW-LEDGER.md`** — the full inventory + review priority.
- **`l200/REVIEW-L200.md`** — the audit protocol (what is verifiable vs. not) + the validation steps.
- **`l200/*.md`** (63) — one audit per chunk.
- **`l200_legacy/`** (55) — the ORIGINAL blurred versions (audit+commentary mixed), preserved as
  provenance, never overwritten.
- **`l200_migrate.py`** — the conservative migration (legacy → strict 8-section). Attaches `migration:`
  metadata. **Do not re-run over the canonicals.**
- **`l200_standardize.py`** — fills real L0 ranges + typed crossrefs into the migrated files.
- **`l200_validate.py`** — the runnable validator (structure, L0 ranges, crossrefs, review meta,
  no-stray, non-empty). **Run it after any change:** `python3 l200_validate.py`.

### Status
- **3 canonical models** (hand-authored, the reference standard): V2-O, V3-B, V3-C — with per-paragraph
  SOURCE ANCHORs.
- **8 hand-authored** V3-I..P closes.
- **52 standardized** files (migrated + real L0 ranges + typed crossrefs), all `editor-reviewed`.
- **All 63** carry `review_state: editor-reviewed` (reviewed_by: editor, 2026-08-11).

### How to do L200 again (for a NEW text)
1. For each chunk: read the T1 golden chunk + the argument map + the raw Sanskrit.
2. Write the 8-section audit: anchor each L2 paragraph to its L0 range + source range (the derivation
   map); separate MT from IA; type the crossrefs.
3. Run `l200_validate.py` to enforce structure.

---

## 2. THE C1 COMMENTARY LAYER (passage-local hermeneutics)

**What it is:** C1 answers *"what does this passage actually say/do?"* — intimate and local, NOT an
essay. It has **TWO representations**:

```
c1/source/   the structured record (SUMMARY/FUNCTION/KEY TERMS/LOCAL CONTEXT/EXPLANATION/
             BOUNDARY/RELATED) — for QA + API
c1/read/     the compact continuous commentary (100–450 words) — what sits under the passage
```

**The governing spec:** `c1/C1-SPEC.md` (imported verbatim from `sourcetranslationprompt.md` on R2) —
READ IT FIRST.

### Files
- **`c1/C1-SPEC.md`** — the authoritative spec.
- **`c1/read/`** (63) — the compact commentary for every chunk.
- **`c1/source/`** (10) — the structured records for the critical nodes.
- **`c1/_essay-material-legacy/`** (10) — the EARLIER essay-rich C1s (they had modern comparisons,
  essay citations, synthesis). **Preserved as ASSETS for THEMES/ESSAYS — NOT as C1.**
- **`c1andmore.md`** — the architecture (C1 + themes + parallels + essays + education).
- **`c1context.md`** — the essay-agnostic skill: how to gather context (scholars, comparisons,
  synthesis) before writing C1. The seven-step protocol.

### The hard-won lessons (do NOT regress)
1. **C1 is compact and local** (100–450 words). NOT a mini-essay, NOT a 7-heading form for the reader.
2. **No modern comparison in C1** — no predictive processing, self-model, Ñāṇavīra, etc. Those belong
   in THEMES/ESSAYS. The `_essay-material-legacy/` folder is where that material lives.
3. **No use of our essays as primary evidence** — essays are internal synthesis, not what the text says.
4. **No cross-textual PARALLELS in C1** — Dyczkowski-style witness-chains are a SEPARATE later layer
   (PARALLELS, after THEMES). C1 stays passage-local. (I initially put PARALLELS in C1; this was
   reverted — the spec now records this.)
5. **The editorial test:** *"Could this sit beneath the translated passage in a serious annotated
   edition?"* If it needs a modern comparison or an essay title, it's not C1.

### How to do C1 again (the full protocol — from `c1context.md`)
1. Locate the passage + root source (kārikā/sūtra).
2. Read the argument map (function, presuppositions).
3. Read the L2 + L200 (load-bearing claims + open items).
4. Mine the on-disk scholarship (the specialist — Ratié for the IPVV — their register + vocabulary).
5. Find the comparisons (as SCRATCH for the later PARALLELS layer — NOT in C1).
6. Pull your own synthesis (the essays — as reference, not evidence).
7. Write the compact read/ commentary + the source/ record.
8. Slop-review: no filler ("the point of this passage is..."), no formulaic openings, each specific.

---

## 3. THE RECOGNITION ESSAY LIBRARY (the synthesis + scholarship layer)

Built in `research-library/recognition/`. This is the SCHOLARSHIP/ESSAYS layer — the arguments that
follow from the C1s and themes.

### The essay set (22 files)
**The authoritative statement:**
- `ESSAY-C-RAZOR-IPVV-AUTHORITY.md` — the ~8,700-word thesis argued from the IPVV.

**The proof essays (the argument chain):**
- `ESSAY-ULTIMATE-PROOF-OF-RECOGNITION.md` — the five-step proof.
- `ESSAY-WHY-RECOGNITION-IS-FELT.md` — the σ-flip mechanism.
- `ESSAY-NONCONSTRUCTED-I.md` — the three-kinds proof.
- `ESSAY-FELT-TO-GROUND.md` — the transcendental argument (and its limit).
- `ESSAY-RECOGNITION-AND-FORMAL-PROOFS.md` — AM0/MEPIT/prooof.

**The comparative essays (recognition vs. other schools):**
- `ESSAY-SPANDA-IPVV.md` · `ESSAY-KRAMA-IPVV.md` · `ESSAY-ADVAITA-IPVV.md` ·
  `ESSAY-BUDDHIST-IPVV.md` · `ESSAY-RASA-IPVV-ABHINAVABHARATI.md` ·
  `ESSAY-SIVASUTRA-VB-IPVV.md` · `ESSAY-TWO-ABHINAVAGUPTAS-IPVV-TANTRALOKA.md` ·
  `ESSAY-RECOGNITION-AND-NISARGADATTA.md`.

**The systematic essays:**
- `ESSAY-EPISTEMOLOGY-OF-ACTION.md` · `ESSAY-EXCLUSION-INDIVIDUATION.md` ·
  `ESSAY-SOTERIOLOGY-OF-RECOGNITION.md` · `ESSAY-ABHINAVA-VS-UTPALADEVA.md` ·
  `ESSAY-ABHINAVA-EXTENSIONS.md` · `ESSAY-ONTOLOGY-SOTERIOLOGY.md` ·
  `ESSAY-OTHER-INTERSUBJECTIVITY.md`.

**The supporting docs:**
- `RECOGNITION-THESIS-FULL-VALIDATION.md` — all claims validated against the IPVV, Ñāṇananda, the
  reflexive debate.
- `RECOGNITION-THESIS-TEARAPART-AUDIT.md` — the deep audit (the five cuts, the four commitments, the
  one-word correction).
- `RECOGNITION-LIBRARY-SYNTHESIS.md` — how the library fits together.
- `IPVV-AUTHORITY-DEEPDIVE.md` — the authority comparison (IPVV vs. Ratié vs. IPK).
- `PEER-REVIEW-RECOGNITION-ESSAYS.md` — the review (reference integrity, argument quality).

### Reference arguments (the hounds)
- `pushing-ipvv/` — the deep-dive sessions (reflexion-vs-Ñāṇavīra, felt-to-ground, buddhist-co-opting,
  recognition-formulations, internal-arc, tantraloka-probe). **These were mirrored from
  `/root/projects/tantraloka/notes/pushing-ipvv/`.**
- `pushing-tantraloka/` — the Tantrāloka hounds (35 files), mirrored the same way.

### The core thesis (unifying everything)
> **Recognition is the felt re-cognition of the self: the self, already established, re-cognizes itself
> as the Lord — the removal of a false self-positioning, and nothing added.**
The library's honest limit: the universalization (all order-less supports are one) is the commitment,
not a consequence.

### How to extend the essays
1. Build the THEMES layer from the C1s (the natural next step).
2. A theme aggregates multiple C1s → an essay cites the theme → the C1s → the passages.
3. The `_essay-material-legacy/` C1s are ready-made material for these essays.

---

## 4. THE PATALA SITE INTEGRATION (the machine-facing layer)

The IPVV was registered in the Pāṭala site (`/root/projects/patala`) as a toggleable source.

### Files changed (mine)
- `data/corpus/works.ts` — added the IPVV + IPK `research_roles`.
- `data/atlas/texts.ts` — the IPVV atlas text entity (concepts, resources, dossier).
- `data/corpus/units/isvarapratyabhijnavivrtivimarsini-1.5.11-published.ts` — the auditable published
  unit (the recognition-thesis core).
- `data/corpus/published.ts` — registered the unit.
- `data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl` — the passage record.
- `app/texts/isvarapratyabhijnavivrtivimarsini/page.tsx` — the IPVV overview page.
- `app/read/[work]/[locator]/page.tsx` — generalized the title map.
- `app/bibliography/page.tsx` — added the "Read IPVV" link.
- `data/atlas/concepts.ts` — added the `camatkara` concept.
- `app/learning/page.tsx` — added the "Recognition is felt, nothing added" foundation block.

> **Note:** there is substantial OTHER patala work in `data/corpus/units/*-generated.ts` (V2 chunks)
> and a `specs/` folder at `sanskritree/translations/_stack/ipvv/specs/` — these are from PARALLEL
> sessions, not this one. Do not overwrite them; this handover documents the recognition-integration
> work only.

### How to add more IPVV passages to patala
1. Copy a `data/corpus/units/kramasadbhava-1.8-published.ts`-style unit for the passage.
2. Register it in `data/corpus/published.ts` (both `pt:passage:` and `tantra:text:` keys).
3. Add a passage line to the jsonl.
4. `npm run build` and verify `GET /api/passages/{id}/translation`.

---

## 5. THE CROSS-CUTTING LESSONS (avoid the traps)

1. **The translation is a layered derivation, not a flat file.** L0→L1→L2→L200→C1→THEMES→PARALLELS→
   ESSAYS. Never collapse layers; keep provenance between them.
2. **C1 ≠ essay.** The essay-rich C1s were corrected and preserved as `_essay-material-legacy/`.
3. **PARALLELS ≠ C1.** Cross-textual witnesses are a separate, later layer.
4. **Never overwrite the canonicals.** `l200_migrate.py` skips V2-O/V3-B/V3-C and the hand-authored
   V3-I..P; `l200_standardize.py` also skips them. The first migration run overwrote the canonicals —
   that was a bug, now guarded.
5. **The originals are the provenance.** `l200_legacy/` and `c1/_essay-material-legacy/` are the blurred
   earlier versions, preserved because they show how the audit/commentary evolved.

---

## 6. NEXT STEPS (the roadmap)

1. **Build the THEMES layer** from the C1s — via **clustering over a hybrid relation-graph**, not
   hand-picking. Themes **overlap** (a C1 has a primary_theme + multiple member_of); clustering is a
   **proposal** (the deterministic floor is structural evidence, not embeddings); each cluster becomes
   a **ThemeProposal** (MACHINE_PROPOSED → EDITOR_REVIEWED → ACCEPTED) before any canonical Theme.
   Memberships carry strength + role; dossiers carry a THEME BOUNDARY. **Discover computationally,
   adjudicate editorially.** See `specs/SPEC_THEME_CLUSTERING.md` (the mechanism) + `specs/SPEC_THEME.md`
   (the dossier structure).
2. **Build the PARALLELS layer** (after THEMES): the cross-textual witnesses for each passage —
   supports/qualifies/contradicts — using the `supports|qualifies|contradicts` roles in
   `primitives.ts`. Feeds the essays.
3. **Generate the `c1/source/` structured records** for the remaining 53 chunks (only 10 exist).
4. **Fill PARALLELS + themes into the essays** — close the provenance chain TEXT→C1→THEME→PARALLEL→ESSAY.
5. **Add more IPVV passages to patala** (the V2/V3 generated units exist; the read/commentary/audit can
   be wired in).
6. **The EDUCATION layer** (lessons/explainers) once the above are populated.

---

## 7. QUICK REFERENCE (paths)

| What | Where |
|---|---|
| The layer stack | `sanskritree/translations/_stack/ipvv/README.md` |
| The audit spec | `.../ipvv/l200/README-L200-SPEC.md` |
| The audit validator | `.../ipvv/l200_validate.py` |
| The audit layer | `.../ipvv/l200/` |
| The C1 spec | `.../ipvv/c1/C1-SPEC.md` |
| The C1 read (commentaries) | `.../ipvv/c1/read/` (63) |
| The C1 source (records) | `.../ipvv/c1/source/` (10) |
| The C1 essay-material | `.../ipvv/c1/_essay-material-legacy/` (10) |
| The C1 skill | `.../ipvv/c1context.md` |
| The architecture | `.../ipvv/c1andmore.md` |
| The essays | `research-library/recognition/ESSAY-*.md` (22) |
| The validation + audit | `research-library/recognition/RECOGNITION-*-*.md` |
| The hounds | `research-library/recognition/pushing-ipvv/` + `pushing-tantraloka/` |
| The patala site | `/root/projects/patala` (the IPVV unit + pages) |

---

## 8. THE IPVV REFERENCE INDEX (everything IPVV-related, cross-referenced)

*The complete map of IPVV content — where each layer of the IPVV work lives, what it contains, and how
it connects. Use this to find any IPVV asset.*

### 8.1 The primary sources (the Sanskrit + the base)
| Asset | Path | Role |
|---|---|---|
| IPVV Vol 1–3 (Sanskrit) | `sanskritree/sources/muktabodha-lib/*M0002[0-2]*IAST.txt` | the target text |
| IPK + Vṛtti (Torella) | `research-library/recognition/primary/torella_ipk.txt` | the root kārikās the IPVV comments on |
| IPV (Vimarśinī) | `sources/muktabodha-lib/*M00019*` | the shorter parallel work (has Pandey's translation) |
| Akaumudī | `sources/muktabodha-lib/*M00053*` | Utpaladeva's shorter auto-commentary |
| Īśvarasiddhi | `sources/muktabodha-lib/*M00023*, *M00660*` | Utpaladeva's proof of God |
| The anchor corpus manifest | `sanskritree/corpus/ipvv-anchor/MANIFEST.md` | the target, distinctions, primary sources, specialists |

### 8.2 The translation layers (in `sanskritree/translations/_stack/ipvv/`)
| Layer | Path | Count |
|---|---|---|
| L0 records (Vol 1) | `l0_v1/*.l0.jsonl` | 28 |
| L0 records (Vol 2–3) | `l0/*.l0.jsonl` | 35 |
| T1 golden chunks | `01_t1/` (Vol 1, 28) + `02_t1/` (Vol 2–3, 35) | 63 |
| L2 READs + argument maps | `pilot/pilot_*_L2_read.md`, `pilot/pilot_*_ARGUMENT_MAP.md` | 108 |
| **L200 audits** | `l200/` | **63** |
| **C1 read commentaries** | `c1/read/` | **63** |
| **C1 source records** | `c1/source/` | **10** |
| The C1 essay-material legacy | `c1/_essay-material-legacy/` | 10 |

### 8.3 The scholarship anchors (in `research-library/recognition/`)
**Ratié (the IPVV specialist):**
| Asset | Role |
|---|---|
| `books/Le-Soi-et-l-Autre-Ratie-2011.{pdf,txt}` | the monograph (French) |
| `RATIE-EXCAVATION-EN.md` | the deep English excavation |
| `RATIE-BREAKDOWN.md` | the chapter map |
| `RATIE-LITERATURE-REVIEW.md` | the chapter→IPK→thesis→IPVV synthesis |
| `ratie-chapters/` (CH0–CH10) | per-chapter analysis |
| `Le-Soi-et-l-Autre-TOC.md` | the table of contents |
| The 22 Ratié papers | `sanskritree/corpus/ipvv-anchor/scholarship/` |

**The other IPVV scholarship:**
| Asset | Role |
|---|---|
| `torella_synthesis.md` | Torella/Bäumer volume synthesis (Utpaladeva = the innovator) |
| `torellalogic.md` | the Torella-logic analysis |
| `TRIANGULATION-SCAFFOLD.md` | the four-corner anchor (IPK↔IPVV↔Ratié↔Solms) |
| `IPVV-ANALYSIS-PREP.md` | the operating guide for IPVV translation/analysis |
| `IPVV-PLAIN-ENGLISH-BRIDGE.md` | the readable layer plan |
| `IPVV-PROGRESS-TRACKER.md` | the translation progress tracker |
| `IPVV-AUTHORITY-DEEPDIVE.md` | the authority comparison (IPVV vs. Ratié vs. IPK) |
| `frameworkrecognition.md` | the recognition framework |
| `isvarasiddhi_translation.md`, `sambandhasiddhi_translation.md` | the Siddhitrayī translations |
| `BUDDHISM-AS-RECOGNITION.md` + `buddhism-as-recognition/` | the Buddhist-recognition relation |

### 8.4 The recognition essays (the scholarship/argument layer — 22 in `ESSAY-*.md`)
| Group | Files |
|---|---|
| The authoritative statement | `ESSAY-C-RAZOR-IPVV-AUTHORITY.md` |
| The proof chain | `ULTIMATE-PROOF`, `WHY-RECOGNITION-IS-FELT`, `NONCONSTRUCTED-I`, `FELT-TO-GROUND`, `RECOGNITION-AND-FORMAL-PROOFS` |
| The comparative (vs. schools) | `SPANDA`, `KRAMA`, `ADVAITA`, `BUDDHIST`, `RASA-IPVV-ABHINAVABHARATI`, `SIVASUTRA-VB`, `TWO-ABHINAVAGUPTAS`, `RECOGNITION-AND-NISARGADATTA` |
| The systematic | `EPISTEMOLOGY-OF-ACTION`, `EXCLUSION-INDIVIDUATION`, `SOTERIOLOGY-OF-RECOGNITION`, `ABHINAVA-VS-UTPALADEVA`, `ABHINAVA-EXTENSIONS`, `ONTOLOGY-SOTERIOLOGY`, `OTHER-INTERSUBJECTIVITY` |

### 8.5 The formal / science framework (in `research-library/recognition/`)
| Asset | Role |
|---|---|
| `RECOGNITION-FORMAL-FRAMEWORK.md` | the σ-flip formalization from the IPVV (the axioms + theorems) |
| `RECOGNITION-AND-SCIENCE.md` | the formal bridge (Solms, active inference, MEPIT) |
| `recognition/recognition-framework/` (also `recognition-aperture/`) | MEPIT, aperture-inexternalism, inexternalism-formal |
| `r2-audio-transcripts/recognition-formulation.md`, `am0.md` | the recognition-formulation + the σ-flip |
| `RECOGNITION-THESIS-FULL-VALIDATION.md` | validated against the IPVV, Ñāṇananda, the reflexive debate |
| `RECOGNITION-THESIS-TEARAPART-AUDIT.md` | the deep audit (the five cuts, the four commitments) |
| `RECOGNITION-LIBRARY-SYNTHESIS.md` | how the library fits together |
| `PEER-REVIEW-RECOGNITION-ESSAYS.md` | the review of the essay library |

### 8.6 The hounds (the deep-dive sessions)
| Asset | Path | Role |
|---|---|---|
| IPVV hounds | `research-library/recognition/pushing-ipvv/` (10 files) | reflexion-vs-Ñāṇavīra, felt-to-ground, buddhist-co-opting, recognition-formulations, internal-arc, tantraloka-probe |
| Tantrāloka hounds | `research-library/recognition/pushing-tantraloka/` (35 files) | the Tantrāloka's own cruxes (the Q-sessions, rasa, karma, theodicy) |
| *Originals* | `/root/projects/tantraloka/notes/pushing-{ipvv,tantraloka}/` | the source of the mirrors |

### 8.7 The c1s (the published Kubjikā/Krama units in patala)
`research-library/recognition/c1s/` — the C1 studies (c1_ajadapramatrsiddhi, c1_kramasadbhava_1_8,
c1_maharthamanjari, c1_sivasutra) — the published-unit model for C1.

### 8.8 The key docs (the specs + skills)
| Asset | Path | Role |
|---|---|---|
| The layer stack | `translations/_stack/ipvv/README.md` | the architecture |
| The audit spec | `translations/_stack/ipvv/l200/README-L200-SPEC.md` | L200's schema |
| The C1 spec | `translations/_stack/ipvv/c1/C1-SPEC.md` | C1's schema (imported from R2) |
| The C1 architecture | `translations/_stack/ipvv/c1andmore.md` | C1 + themes + parallels + essays |
| The C1 skill | `translations/_stack/ipvv/c1context.md` | how to gather context + write C1 |
| The process/roadmap | `translations/_stack/ipvv/IPVV_PROCESS_NEXT_STEPS.md` | the options + sequence |
| The calibration | `translations/_stack/ipvv/CALIBRATION_REPORT.md` | the layer lock + L2 rules |
| **This handover** | `translations/_stack/ipvv/HANDOVER-IPVV-LAYERS-2026-08-12.md` | the map of everything |

---

*This is the handover. The IPVV is fully translated; this session built the L200 audit layer (63
chunks), the C1 commentary layer (63 read renderings + 10 source records), and the recognition essay
library (22 essays + validation/audit/synthesis). The specs and skills document how to reproduce each
part. §8 is the complete cross-reference index of all IPVV-related content. **For what to do NEXT
(and why), see `HANDOVER-PLANS.md`** — the forward roadmap (THEMES first, then PARALLELS, the c1/source
completion, the MCP toolset, the cross-work graph, EDUCATION, deeper patala). **For the deep WHY — the
philosophy and the editorial discipline condensed — read `IPVV-KNOWLEDGE-CORE.md`.***

---

## 9. THE NEW-AGENT ENTRY PROTOCOL (read these, in this order)

If you are a new agent resuming this work, read the following files IN ORDER. Each unlocks the next;
skipping one means you'll miss the context it provides.

### The four essential reads (do these first, always)
1. **`IPVV-KNOWLEDGE-CORE.md`** — the deepest understanding, condensed: the recognition thesis, the
   three registers, the five-step proof, the honest boundary, the comparative map, AND the editorial
   discipline (the C1/L200/THEMES rules, the provenance principle). **This tells you WHAT the work is
   about and WHY it's structured this way.** (Fastest way to absorb the philosophy + method.)
2. **`README.md`** — the layer stack (L0→L1→L2→L200→C1→THEMES→PARALLELS→ESSAYS→EDUCATION). **This
   tells you the architecture and where each file lives.**
3. **`HANDOVER-IPVV-LAYERS-2026-08-12.md`** — what exists: the files, the status, the counts, the
   how-to-do-it-again for each layer, the cross-references (§8). **This is your map of what's already
   done.**
4. **`HANDOVER-PLANS.md`** — what to do next, in priority order, with the why. **This is your roadmap.**

### The specs (read the one relevant to your task)
Read the specific spec before doing that layer's work:
- L0/L1: `specs/SPEC_L0_L1.md` · L2: `specs/SPEC_L2.md` · SOURCE: `specs/SPEC_SOURCE.md`
- C1: `c1/C1-SPEC.md` (the governing spec, identical content to `specs/C1_SPEC.md`) + `c1andmore.md`
  (the architecture) + `c1context.md` (the skill for writing C1)
- THEMES: `specs/SPEC_THEME_CLUSTERING.md` (the corrected mechanism) + `specs/SPEC_THEME.md` (the
  dossier structure) + `specs/THEMES_PILOT_REPORT.md` (the proven pilot) + `specs/themes_pilot.py` (the
  runnable pilot)
- ESSAY: `specs/SPEC_ESSAY.md` · EDUCATION: `specs/SPEC_EDUCATION.md`
- QA: `specs/SPEC_FACTORY_QA.md` · Storage: `specs/SPEC_STORAGE_R2.md`
- Provenance/generation: `specs/PLATFORM_PROVENANCE_PRESERVING_GENERATION.md`
- Patala: `specs/PATALA_INTEGRATION_BRAINSTORM.md`, `specs/CONNECTIVITY_REVIEW.md`,
  `specs/REVIEW_FOJIN.md`, `specs/EXECUTION_ORDER.md`, `specs/VISION_CHOOSE_YOUR_DEPTH.md`
  (parallel-session work)
- Companion: `specs/THE_COMPANION.md` · Factory index: `specs/README_FACTORY_INDEX.md`

### How to USE the four essential files (the workflow)
```
1. NEW AGENT, orientation (5 min):    IPVV-KNOWLEDGE-CORE.md  →  README.md
   → you understand the philosophy + the architecture.

2. NEW AGENT, what exists (5 min):    HANDOVER-IPVV-LAYERS-2026-08-12.md (§0–8)
   → you know every file and its status.

3. NEW AGENT, what's next (5 min):    HANDOVER-PLANS.md (§1–8)
   → you know the priority order and why.

4. NEW AGENT, do a task: pick the relevant spec, run the validator, do the work, log progress.
```

### The rules that always apply (from the knowledge-core)
- Layers stay separate; never collapse them.
- C1 is compact and local — no modern comparison, no essays-as-evidence, no PARALLELS inside.
- Themes overlap; clustering is a proposal, not the deterministic floor.
- Discover computationally; adjudicate editorially.
- Never overwrite the canonicals or the originals (the legacy/proposals are the provenance).
- **AI proposes ≠ Pāṭala asserts** — the verification floor is structural evidence.
- Run `l200_validate.py` after any L200 change.

### The command to run first
```bash
cd /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv
python3 l200_validate.py          # confirms the audit layer is intact
cat IPVV-KNOWLEDGE-CORE.md        # the orientation read
```
