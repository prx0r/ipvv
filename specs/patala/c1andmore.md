# C1 AND MORE — the universal scholarly stack

*2026-08-11. The derivation architecture for the IPVV (and every text the project touches: Kubjikā,
Buddhist texts, ritual manuals, goddess texts). C1 is intimate, passage-local interpretation — NOT a
"what big essay can we extract" exercise. The themed essays sit ABOVE it. Each level is derived from the
one below it, and the whole chain stays inspectable.*

---

## THE UNIVERSAL STACK

```
SOURCE
  ↓
L0 / L1           token-level / controlled
  ↓
L2 READ           "what does the text say?"
  ↓
L200 AUDIT        "how was this reading derived?"  (philology)
  ↓
C1 PASSAGE COMMENTARY   "what does this passage mean?"  (hermeneutics)
  ↓
THEME / CONCEPT DOSSIERS   "how does this idea develop across the work?"
  ↓
ESSAYS            "what larger argument follows from all of this?"
  ↓
EDUCATION         lessons / explainers / learning
```

**The four human questions (zoom levels):**
- READ — "What does the text say?"
- STUDY (C1) — "What does this passage mean?"
- THEMES — "How does this idea develop across the work?"
- ESSAYS — "What larger argument follows from all of this?"

**The method:** TEXT → local understanding → recurring structures → thematic synthesis → argument.
You never start with an essay and force passages into it.

---

## C1 — the passage commentary (the hermeneutic layer)

**The C1 question:** What is this passage *doing*, *saying*, *presupposing*, and *implying*?
NOT "what essay can we extract from it." C1 stays very close to the text.

**The governing spec:** `c1/C1-SPEC.md` (imported verbatim). C1 is a **compact commentary paragraph**,
not a form. It has TWO representations:

```
c1/source/   the structured record (SUMMARY / FUNCTION / KEY TERMS / LOCAL CONTEXT /
             EXPLANATION / BOUNDARY / RELATED) — for QA + API + machine processing
c1/read/     the continuous commentary (100–450 words) — what sits beneath the translated
             passage for a reader
```

**The editorial test for C1:** *Could this commentary plausibly sit immediately beneath the translated
verse/passage in a serious annotated edition?* If yes, it's C1. If it needs a modern comparison, an
original argument, or a title-essay, it belongs in THEMES or ESSAYS.

### The universal core (every passage, whatever its kind)

```
SUMMARY            what the passage says in plain terms
FUNCTION           its argumentative / ritual / mythic role
KEY TERMS          the technical terms that matter, with their senses
LOCAL CONTEXT      what precedes / follows; what it presupposes
INTERPRETATION     what it means — the local reading
OPEN QUESTIONS     what remains uncertain
RELATED PASSAGES   nearby passages that clarify it
```

### The optional modules (passage-type specific)

Not every passage is argumentative. A C1 should only use the modules its passage type needs:

```
ARGUMENT    premises / objection / reply        (philosophical exposition)
RITUAL      actor / action / object / sequence / result   (ritual manuals)
DEITY       form / epithets / relations / symbolism        (goddess texts)
MANTRA      structure / deity / ritual use                 (mantra sequences)
COSMOLOGY   entities / hierarchy / correspondences         (cosmologies)
YOGA        body locus / process / result                  (yogic anatomy)
NARRATIVE   characters / event / function                  (mythic narratives)
INITIATION  eligibility / rule / procedure                 (initiatory rules)
```

**Why modules, not a forced argument-schema:** many tantric passages are ritual instructions, deity
visualizations, mantra sequences, mythic narratives, initiatory rules, cosmologies, yogic anatomy — not
arguments. C1 must handle all of them without pretending they are philosophy.

---

## HOW THE LAYERS DERIVE

**L200 → C1.** The IA (interpretive assertion) nodes in L200 **seed** C1 — they are evidence/input, not
C1 themselves. A single IA becomes the hinge of a full C1 explanation of its paragraph.

```
IA-034  "Memory belongs to the Lord's power"
          ↓ (evidence / input)
C1      full passage-commentary of the paragraph
          ↓ (aggregated with other C1s on the same theme)
THEME   Memory / recognition / continuity
          ↓ (synthesized)
ESSAY   Abhinavagupta's account of diachronic subjectivity
```

For a ritual text:

```
IA   "This placement identifies the goddess with the western locus"
          ↓
C1   what this specific ritual placement means here
          ↓
THEME  goddess-space relations
          ↓
ESSAY  ritual geography in the Kubjikā tradition
```

**The IA → C1 → THEME → ESSAY chain is the derivation.** Each level aggregates the one below.

---

## WHY THIS IS TRADITION-AGNOSTIC

Same schema, totally different content:

**IPVV (philosophical):**
> "Abhinavagupta is not merely defining memory here. He is using memory to establish that continuity
> belongs to the recognizer rather than to a latent impression…"

**Kubjikā (ritual/mythic):**
> "The goddess is introduced here not merely as a named deity but as the organizing center of a specific
> ritual topology. Her location, retinue, directional associations, and mantra all determine how the
> practitioner is meant to construe the ritual body…"

Same C1 schema. Different content. Pāṭala can handle radically different kinds of Sanskrit material
without pretending everything is philosophy.

---

## THEMATIC SYNTHESIS (an example)

**KUBJIKĀ C1s** → **THEME DOSSIER** → **ESSAY**

```
K3.14  goddess appears as contracted / crooked power
K3.22  relation to cakra structure
K4.05  retinue and directional placement
K7.11  mantric embodiment
          ↓ (the system synthesizes)
THEME DOSSIER  "Who is Kubjikā?"   (uses C1 K3.14, K3.22, K4.05, K7.11…)
          ↓
ESSAY  "The Goddess as Ritual Topology in Early Kubjikā Tantra"
```

---

## THE LAYER MAP (clean)

| Layer | Discipline | Question | Files |
|---|---|---|---|
| L200 | PHILOLOGY | how was the reading derived? | `l200/` |
| C1 | HERMENEUTICS | what does this passage mean? | `c1/source/` + `c1/read/` |
| THEMES | SYNTHESIS | how does the idea develop across the work? | (to build) |
| PARALLELS | COMPARISON | what other works make the same move? | (to build — later) |
| ESSAYS | SCHOLARSHIP | what larger argument follows? | (the research-library essays) |
| EDUCATION | PEDAGOGY | how do we explain it to a learner? | (to build) |

Each level is derived from the one below it. The text is readable for normal users while the entire
scholarly chain remains inspectable. **C1 is compact and local (a commentary paragraph, two
representations); cross-textual parallels are a SEPARATE layer (PARALLELS) built after THEMES, not a C1
section; the synthetic/comparative material belongs in ESSAYS. The early, essay-rich C1s are preserved
in `c1/_essay-material-legacy/` as assets for those layers.**

## PARALLELS — a separate layer, not part of C1

Dyczkowski's cross-textual witness-chains (other works that support/qualify/contradict the local
claim) are a **distinct layer AFTER THEMES**, NOT a C1 section. Gathering them pulls the commentary
away from the local move and toward synthesis — so they are collected later, once the C1s and themes
are settled.

```text
C1          passage-local commentary (no cross-textual witnesses here)
THEMES      what pattern emerges across passages (within the work)
PARALLELS   cross-textual witnesses (supports · qualifies · contradicts) ← THIS LAYER
ESSAYS      what larger argument follows
```

Each parallel records:
```text
Work / passage      where the parallel occurs (a resolvable source span where possible)
Relation            supports · qualifies · contradicts   (the evidence roles)
Basis               the shared move that makes it a witness
```

The relations map onto the existing evidence roles (`supports | qualifies | contradicts` in
`primitives.ts`). This layer feeds the essays and the comparative research — but it stays out of C1,
so C1 remains a local commentary.

---

*This is the C1-and-more architecture. C1 is intimate, passage-local interpretation (universal core +
passage-type modules); the theme dossiers and essays sit above it. The IA nodes of L200 seed C1. The
chain L200 → C1 → THEMES → ESSAYS → EDUCATION is the derivation, and it is tradition-agnostic: the same
schema serves the IPVV, Kubjikā, Buddhist texts, ritual manuals, and goddess texts.*
