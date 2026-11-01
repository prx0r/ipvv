# PĀṬALA INTEGRATION — how the factory weaves in (FROZEN PRODUCT MODEL)

*2026-08-11. **Frozen.** The product model is now fixed; no new top-level primitives will be
invented. Every factory output (translation, decision, alternative, C1, theme, essay) is a
FIRST-CLASS, interwoven object on pāṭala from the moment it is produced — never "done separately
then imported." The principle: **the site is not a render of finished artifacts; it is the workspace
where they are born, and every layer is queryable and navigable in place.***

---

## 0. The frozen product model

The user-facing product is exactly these modes:

```
TEXT        read the passage
COMMENTARY  understand the passage          (C1)
AUDIT       inspect why it was translated   (decisions + evidence)
COMPARE     see rival translations          (version selector)
CONCEPT     follow an idea through the corpus
RELATED     move through textual relationships
ESSAY       see higher-order synthesis
EVIDENCE    drop from any claim back to the source   (resolve)
```

Nothing else is added at the top level. Everything below elaborates these modes.

> **The endgame above all of these is `CHOOSE YOUR DEPTH`** — ORIGINAL / READ / GUIDE / STUDY /
> CRITICAL, where GUIDE is a plain-language pedagogical projection of the scholarship (progressive
> disclosure: HOOK → PLAIN READING → DON'T MISS THIS → TERMS → CONTEXT → GO DEEPER), and every unit
> resolves back to the canonical passage. The truth-layer rule: GUIDE may simplify a supported
> claim but never introduce a claim absent from the evidence. See
> [`VISION_CHOOSE_YOUR_DEPTH.md`](VISION_CHOOSE_YOUR_DEPTH.md).

---

## 1. Alternative translations = a SELECTOR over one source passage

One canonical source span, multiple target-span sets. Same passage, rival readings — comparability
preserved, disagreement inspectable.

```
passage
├── current_reading
├── T1 literal
├── T2 rival
├── Pandey
├── Torella
├── Ratié
└── historical/versioned readings
```

**Correction (adopted):** decisions/evidence do NOT stay identical when switching translations.
Some evidence is global to the source passage, but **translation-specific decisions and rationales
attach to that reading** — otherwise the apparatus would falsely appear to explain Torella's choice.
Model:
- **passage-global evidence** (source, manuscript, variant) — shared across readings;
- **reading-specific decisions** (that translation's rationales) — attached to the target-span set.

**Public labels (adopted — do not call T2 "opposing"):**
```
ALTERNATIVE READING   historically/scholarly defensible
ADVERSARIAL TEST      deliberately constructed to stress the chosen interpretation
```
The factory's T2 may be either; the UI must not imply false scholarly parity.

---

## 2. `/api/resolve` = the citation backbone (THE key piece)

Every scholarly object resolves through stable identifiers:

```
ref
↓ work
↓ structural location
↓ passage
↓ source spans
↓ translation(s)
↓ decisions
↓ C1
↓ related claims/themes
```

**ID-based first, human-readable alias second.** A locator like `ipvv:V2-S:14` may change when
segmentation improves; internally resolve to an **immutable passage ID**:

```
ipvv:V2-S:14            (human alias, mutable)
→ pt:passage:7f...      (immutable passage ID)
```

The immutable ID layer lives immediately beside resolve, so mutable locators never get baked into
the system.

---

## 3. Concept page = occurrence map (with kinds, not grep)

A concept page is NOT concordance search. It distinguishes:

```
OCCURRENCE         the term literally occurs
DOCTRINAL_INSTANCE concept present without the exact term
DEFINITION         passage explicitly defines it
ARGUMENT           passage argues about it
CROSS-REFERENCE    later/earlier development
```

`vimarśa` becomes a real intellectual map, not a grep result.

---

## 4. Recommender = passage-level, DETERMINISTIC from typed relations

Not an opaque recommendation engine. Deterministic from typed relations:

```
ROOT_TEXT            the passage comments on this
COMMENTARY_OF        this comments on that
CONTINUES_ARGUMENT   next step of the same argument
PRIMARY_PARALLEL     direct parallel
DOCTRINAL_PARALLEL   conceptual parallel elsewhere
OPPOSING_POSITION    an adversary's position
QUOTATION_SOURCE     a quoted source
SCHOLARLY_DISCUSSION a scholar's discussion
```

The UI renders "Related" intelligently from these; no opaque recommender logic.

---

## 5. Essays — two claim classes (adopted), deterministic first

**Deterministic synthesis FIRST** — prove the chain works:

```
theme → relevant passages → C1s → comparison data → evidence-backed outline → essay
```

**Claim classes (adopted — replaces the too-strict rule):**
```
EVIDENCED CLAIM   directly supported by resolvable sources
SYNTHETIC CLAIM   derived from ≥2 evidenced claims, explicitly marked as synthesis
UNANCHORED CLAIM  no evidence path → REJECT
```

The essay object stores per-claim:
```
claim_id
text
type: EVIDENCED | SYNTHETIC
supports: [ passage…, decision…, C1… ]
derivation_note
```

**SHOW EVIDENCE works at sentence/claim level.** Once deterministic synthesis works reliably,
on-demand generation becomes merely a query interface over the same machinery.

---

## 6. What this needs from the factory (the enabling atoms)

| capability | factory source | status |
|---|---|---|
| stable immutable passage IDs + aliases | SOURCE spec (§4) | **to build (with resolve)** |
| source spans + resolve | pāṭala schema | exists (schema has source_spans) |
| reading-specific decision alternatives (T2/R2) | pipeline T2/R2 versions | in schema; not surfaced as selector |
| term occurrence map (with kinds) | term packs | `data/terms.json` exists; occurrence map to build |
| C1 per passage | C1 spec | exists (`c1/`) |
| comparison packs | SPEC_ESSAY §6 | partial (research-library) |
| typed relations (the 8 kinds) | pāṭala relations graph | exists; extend kinds |
| resolve/citation kernel | §2 | **to build** |

---

## 7. The interweaving principle (the anti-import)

> An essay or alternative translation is not "finished elsewhere then imported." It is born inside
> the site as a view over the evidence graph. Writing a comparative essay = selecting passages +
> writing prose over their `resolve`-able claims. Producing an alternative translation = adding a
> target-span set to the same source spans. Both are *edits to the graph*, instantly navigable and
> queryable.

---

## 8. The frozen build order (adopted)

```
1. Resolve kernel
2. Canonical passage-ID / alias system      (beside resolve — never bake in mutable locators)
3. Version-selector
4. Typed relation graph + related rail
5. Concept occurrence map
6. Deterministic theme synthesis
7. Claim-level essay generation
8. On-demand essays
```

The ID layer belongs immediately beside resolve, so mutable locators are never baked into the
system.

---

## 9. Sequencing rationale

Because these are interdependent, the order that unblocks the most:
1. **Resolve kernel + immutable IDs** — the citation backbone; everything else hangs on it.
2. **Version-selector** — surfaces alternatives as buttons (the clearest "interwoven" win).
3. **Related rail** — deterministic from typed relations.
4. **Concept occurrence map** — turns term packs into navigation.
5. **Deterministic essay synthesis** — then claim-level essays — then on-demand.


---

## 0. The shift in framing

Today the pāṭala reader shows **one published translation** with READ/AUDIT toggle, span→decision
hover, and Commentary ON/OFF. The user's vision is richer: the site becomes a **research substrate**
where:

- a new translation's **alternative readings** are a **clickable button** (not a separate doc);
- a reader can **query exact referenced lines** and jump to them;
- a reader can **enter via a concept** ("I want everything about vimarśa") and walk the passages;
- a work shows **related works** (Netflix-style: "because you read the IPVV on reflexion…");
- once enough passages are granularly tracked, **comparative essays write themselves** — and can be
  **generated on demand by the user's own prompt**, with every claim resolving to the passages.

This is all **downstream of the factory's granular passage tracking** (stable IDs, spans, decisions,
source anchors). The factory produces the atoms; pāṭala is where they assemble and where the reader
navigates them. Brainstorm below.

---

## 1. The reader grows views, not new pages

The existing `/read/[work]/[locator]` route is the hub. Extend it with **view toggles** that are
already latent in the data:

| view | today | vision | data already has it? |
|---|---|---|---|
| READ | ✓ | clean English | yes (L2) |
| AUDIT | ✓ | show decisions/evidence inline | yes (span→decision) |
| COMPARE | — | Sanskrit + controlled (L1) beside L2 | yes (source_spans + L1) |
| **ALTERNATIVES** | — | **clickable buttons** to switch the reading (PREFERRED / R1 / T2 / R2 / Pandey / Torella / Ratié) | **partial** — `decision.alternatives` exists; the *alternate full translations* (T2/R2) are not surfaced |
| COMMENTARY | ✓ toggle | the C1 | yes (C1) |
| **CONTEXT** | — | root kārikā + Vṛtti + IPV parallel + interlocutors in a side rail | yes (`/api/context`) |
| **RELATED** | — | Netflix-style "because you read X…" rail | **partial** — relations graph exists, not surfaced |

**Key design choice:** *Alternative translations are NOT separate documents.* They are **alternate
`target_span` sets** over the SAME source spans — so switching the reading re-links the same
alignments/decisions. The `translation_versions` concept in the schema (`versions`, never-overwrite)
already supports this: T1, T2 (the opposing reading), R2 (the synthesis) are versions of the same
passage. The reader needs a **version/reading selector** that swaps `target_span.text` while keeping
source + decision provenance identical.

This is exactly the factory's T2 (the opposing alternative) — the anti-cheat. It should be a button:
**"See the alternative reading (T2)"** → the same passage re-rendered with the opposing
interpretation, same decisions, same evidence, flagged as the deliberate alternative.

---

## 2. Query exact referenced lines — the citation kernel

The factory's stable passage IDs + spans make every claim addressable. The API should expose a
**resolution query** so any tool (or the user) can resolve a citation to lines:

```
GET /api/resolve?ref=ipvv:V2-S:14            → { passage, spans, source_range, L0, decisions, C1 }
GET /api/resolve?ref=ipvv:V2-S:14&span=L34T7 → that exact token/gloss
GET /api/resolve?ref=gretil:ipk:1.5.11       → the root kārikā + Vṛtti
```

Then **an essay's SHOW EVIDENCE link is a `resolve` call**, not a hand-maintained href. A claim
"memory is the Lord's power (IPVV V2-A)" → `resolve` → the passage, the Sanskrit, the decision, the
C1. The citation kernel is the load-bearing piece that makes everything interwoven.

---

## 3. Read via concept — the concept-first entry point

pāṭala has `app/concepts/[slug]` (concept pages) but no **concept-driven reading path**. The vision:

- A concept page (e.g. `vimarśa`) shows **not just a definition** but a **map of its occurrences**:
  every passage where vimarśa is at stake, each with its local C1, grouped by development.
- From the concept page the reader **enters the text at any of those passages** (a passage becomes a
  node in a concept-graph, not just a line in a book).
- This is the **THEME layer** made navigable: a theme dossier *is* the set of passages + their C1s;
  the concept page *is* the theme's front door.

Data needed: the **term-ledger occurrence index** (lemma → passages) that the factory's term packs
produce. `data/terms.json` + the occurrences endpoint already exist; the concept page needs to
render the occurrence map, not just the sense.

---

## 4. Related works — the Netflix rail

The relations graph (`data/corpus/relations.ts`, typed + confidence + evidence) is the raw material.
Make it a **recommendation rail** on every passage/work page:

```
"Because you read IPVV 2.4 (the reflexion claim)…"
  · IPK 1.5.11  (root kārikā)          [ROOT_TEXT_CONTEXT]
  · IPV (parallel commentary)          [SAME_ARGUMENT_CONTINUATION]
  · Tantrāloka (the one light)         [CONCEPTUAL_PARALLEL]
  · Ratié, Otherness in the Pratyabhijñā [SCHOLARSHIP]
```

Rules: the rail ranks by **relation type × confidence × shared terms**, not by flat tags. It should
distinguish "same argument continues here" (read this next) from "conceptual parallel elsewhere"
(browse this for comparison) from "scholarship" (read this to adjudicate).

The netflix analogy is exact: a **passage-level collaborative/feature recommender** over the
relations + shared-concept graph. "Readers of this passage also engaged these," where "engaged" =
same shared concept, same tradition, same interlocutor, same term at stake.

---

## 5. The self-writing comparative essay + on-demand generation

Once enough passages carry granular tracking, the **comparative essay writes itself** — because the
comparison packs + themes already structure the evidence:

```
ESSAY = THEME dossiers + COMPARISON packs + SOURCE context
```
With every claim pointing to a passage via `resolve`, an essay is a **structured selection +
prose over the evidence graph**, not a hand-written thing that then gets footnoted.

Two modes:

### (a) Deterministic synthesis (the baseline)
Given a topic ("reflexivity across IPVV + IPK + Ratié"):
1. gather the relevant passages (via term/theme occurrence index);
2. pull their C1s and comparison packs;
3. assemble a draft essay with SHOW EVIDENCE links that already resolve;
4. a human/editor polishes the prose.

### (b) On-demand generation (the user's prompt → a new essay)
Because the evidence graph is complete, a user can ask:
> "Write me a comparison of how memory is treated in the IPVV vs the Spandakārikā"

and the system can:
1. resolve both works' memory passages (term index);
2. pull each passage's L2 + C1 + comparison pack;
3. generate an essay that is **grounded** (every claim cites a resolved passage) and clearly marks
   its own interpretive moves as synthesis, not as what the text says (per C1 §9 discipline).

The **anti-hallucination rule** is the load-bearing one: the generator may only assert what it can
anchor to a `resolve`-able passage or an explicitly-flagged interpretive claim. This is the C1/ESSAY
discipline (§7 of SPEC_ESSAY) enforced at generation time, not after.

---

## 6. What this needs from the factory (the enabling atoms)

These are the pieces that make the interweaving possible; several already exist:

| capability | factory source | status |
|---|---|---|
| stable passage IDs | SOURCE spec (§4) | to freeze |
| source spans + resolve | SOURCE spec + pāṭala schema | exists (schema has source_spans) |
| decision alternatives (T2/R2 versions) | pipeline T2/R2 (never-overwrite versions) | exists in schema; not surfaced as buttons |
| term occurrence index | term packs (SPEC_L0/L1 §2, term ledger) | `data/terms.json` exists; occurrence map to build |
| C1 per passage | C1 spec | exists (`c1/`) |
| comparison packs | SPEC_ESSAY §6 | partial (research-library) |
| typed relations | pāṭala relations graph | exists |
| resolve/citation kernel | §2 above | **to build** |
| passage-level recommender | §4 above | **to build** |

---

## 7. The interweaving principle (the anti-import)

> **An essay or alternative translation is not "finished elsewhere then imported." It is born inside
> the site as a view over the evidence graph.** Writing a comparative essay = selecting passages +
> writing prose over their `resolve`-able claims. Producing an alternative translation = adding a
> `target_span` version to the same source spans. Both are *edits to the graph*, instantly navigable
> and queryable.

This is what makes the whole system tradition-agnostic and self-compounding: every new passage or
essay strengthens the graph, and the graph makes the next essay cheaper.

---

## 8. Open questions for the design

1. **Alternative translation UI:** confirm the vision is a **version/reading selector** (T1 / T2 /
   R2 / Pandey / Torella / Ratié as selectable `target_span` sets over one source), not separate
   pages. (I believe selector.)
2. **Resolve kernel:** confirm `/api/resolve` is the single citation-resolution endpoint every
   essay/claim uses (the SHOW EVIDENCE backbone).
3. **Concept-first entry:** confirm the concept page should show an **occurrence map** (passages
   where the term is at stake, grouped by development) as the primary entry, not just a definition.
4. **Recommender scope:** confirm the related-works rail is **passage-level** (recommend the next
   passage / the root / the parallel) rather than only work-level.
5. **On-demand essays:** confirm you want the **user-prompt → grounded-essay** mode now (with the
   anti-hallucination anchor rule), or first the deterministic synthesis baseline.

---

## 9. Sequencing suggestion (for when we build)

Because these are interdependent, the order that unblocks the most is:

1. **Resolve kernel** (§2) — the citation backbone; everything else hangs on it.
2. **Version/reading selector** (§1) — surfaces the factory's T2/R2 alternatives as buttons (the
   clearest "interwoven not imported" win).
3. **Related-works rail** (§4) — cheap, uses the existing relations graph.
4. **Concept occurrence map** (§3) — turns term packs into navigation.
5. **Deterministic essay synthesis** (§5a) — then **on-demand generation** (§5b) with the anchor rule.
