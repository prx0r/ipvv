# SPEC — THEME (evidence-backed synthesis across C1s)

*The sixth layer. A THEME is not a keyword — it is an evidence-backed synthesis across multiple C1s.
It asks: what recurring structure emerges across these local commentaries?*

---

## 0. THE MECHANISM — discover computationally, adjudicate editorially

The RELEVANT C1s list for a theme is **machine-derived** (see `SPEC_THEME_CLUSTERING.md` for the full
mechanism). Two foundational rules:

1. **Themes overlap — they are not partitions.** A C1 has a `primary_theme` and can be a `member_of`
   several others (Memory, Recognition, Continuity, Agency...). Do not force a C1 into exactly one
   theme.
2. **Clustering is a proposal, not the deterministic floor.** The floor is structural evidence (C1 ids,
   source passages, term links, RELATED relations, quotes, provenance all resolve). Semantic clustering
   proposes; human adjudication accepts — "AI proposes ≠ Pāṭala asserts."

```
C1s → hybrid relation-graph → candidate communities → ThemeProposal → LLM names →
     human merge/split/multi-assign → ACCEPTED THEME (overlapping)
```

The hand-lists below (e.g. "Memory and Recognition = V2-A, V2-C, V2-L...") are **exemplars / training
data**, NOT the mechanism. The mechanism is a hybrid graph (semantic + shared terms + RELATED +
sequence + interlocutor + function) over the C1s, clustered into overlapping proposals, adjudicated
editorially.

## 1. Derivation

```
C1s → THEME DOSSIER → ESSAY
```
A theme is built ONLY from local C1s (and the passages they cite). Never start with a theme and
force passages into it.

## 2. Theme dossier structure

```
CORE QUESTION
RELEVANT C1s           (the local commentaries that ground it)
RECURRING CLAIMS
IMPORTANT TERMS
DEVELOPMENT ACROSS THE WORK
TENSIONS / OPEN QUESTIONS
PRIMARY EVIDENCE        (every claim points down to a C1 → passage → Sanskrit)
THEME BOUNDARY          (included because / not claiming — prevents synthesis inflation)
```

## 3. Example

```
THEME — Memory and Recognition
C1 V2-A · C1 V2-C · C1 V2-L · C1 V2-O · C1 V2-S
```
A theme aggregates these; the essay then argues from it.

## 4. What is NOT a theme

A bare keyword tag, a bibliography, or a modern comparison. Those belong in ESSAY.

## 5. Factory rule

Every theme item must trace to its C1s; synthesis is now expected (unlike C1, which stays local),
but the evidence trail is preserved.

---

## 6. EXEMPLARS — what a THEME looks like in the IPVV + research-library

The IPVV C1s that ground the **Memory / Recognition / Reflexivity** theme:

| C1 | file | the local claim it contributes |
|---|---|---|
| V2-A memory-lord's-power | `translations/_stack/ipvv/c1/c1_V2A-memory-lords-power.md` | memory is the Lord's power |
| V2-C | `translations/_stack/ipvv/c1/` (viśrānti/Ajaḍapramātṛsiddhi) | the awareness has nothing over against it |
| V2-L non-constructed I | `translations/_stack/ipvv/c1/c1_V2L-nonconstructed-I.md` | the "I"-awareness is not a construction |
| V2-O orderless-support | `translations/_stack/ipvv/c1/c1_V2O-orderless-support.md` | the pratibhā / order-less knower |
| V2-S unity-maheśvarya | `translations/_stack/ipvv/c1/c1_V2S-unity-mahesvarya.md` | the unity of the maheśvara |

**The synthesis products** (theme dossiers and cross-work themes) already exist in
`/root/projects/research-library/`:

| file | what it is |
|---|---|
| `CONCORDANCE-Ratie-IPK-Solms.md` | a term/theme concordance across Ratié, IPK, Solms |
| `COMMENTARY-STAGE1-REFLEXIVITY-SYNTHESIS.md` | the reflexivity synthesis (a theme-dossier-level product) |
| `5-STAGE-LENS-ACROSS-SCHOOLS.md` / `7-FOLD-COMPARATIVE-MODEL.md` | cross-school thematic frames |
| `concept-deepdives/whattheheckismemory.md` | a concept dossier ("what is memory?") built from passages |

**How they fit the spec:** the concept-dossiers (e.g. `whattheheckismemory.md`) and the
`COMMENTARY-STAGE1-REFLEXIVITY-SYNTHESIS.md` are exactly the THEME layer — evidence-backed
syntheses that aggregate local passages before an essay is written.

---

## 7. VALIDATION — how we know a THEME is correct

- [ ] every item in the dossier traces to ≥1 C1 (RELEVANT C1s are real, not decorative)
- [ ] RECURRING CLAIMS are present in the cited C1s (no claim introduced that no local commentary
      grounds)
- [ ] it asks "what pattern emerges across passages?" — not "what do I believe about the tradition?"
- [ ] it records DEVELOPMENT ACROSS THE WORK and TENSIONS/OPEN QUESTIONS honestly
- [ ] it is derived from C1s, not from an essay-to-be (no forcing passages into a pre-decided theme)
- [ ] PRIMARY EVIDENCE links resolve to a C1 → passage → Sanskrit
- [ ] it does not collapse into an essay (comparison/modern-application/argument belong in ESSAY)
