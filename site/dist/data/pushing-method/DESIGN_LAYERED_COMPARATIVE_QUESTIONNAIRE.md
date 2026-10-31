# DESIGN — THE LAYERED COMPARATIVE QUESTIONNAIRE (Tantra-agnostic)

*2026-08-12. Brainstorm + working design for making the comparative questionnaire tradition-agnostic,
so Pāṭala can grow beyond Tantra (Buddhism, Greek, Nyāya, Advaita, …) without throwing away the deep
Śaiva layer. The answer is a **layered questionnaire**: a core agnostic spine + pluggable
tradition-modules. The 7-fold/5-stage become ONE module (Śaiva), not the whole system.*

---

## The core principle

> **Ask the deep questions that any tradition must answer (agnostic core), then layer the tradition's
> OWN questions on top. The core is fixed for comparison; the tradition layer is where the text gets
> pushed to its bottom.**

Two axes, kept separate:
- **COMPARABILITY** (the core) — same questions, every text, so answers are directly comparable.
- **PENETRATION** (the tradition layer) — the questions only that tradition's texts can answer.

You need both. A core-only questionnaire never gets to the bottom of a Tantra text; a
tradition-only questionnaire can't compare a Tantra text to a Buddhist one.

---

## THE LAYERS

### L0 — the AGNOSTIC CORE (fixed, every text, every tradition)

Questions ANY serious text about the world must answer, phrased so a ritual text and a
philosophical text and a Greek text and a Buddhist text can each be asked.

```
CORE-01  What is the ultimate / the fundamental? Is there one, and what is it?
CORE-02  What is consciousness / mind? What is its nature?
CORE-03  What is the self / subject? Is there a knower?
CORE-04  What is the world / object? Its relation to subject?
CORE-05  How does cognition / knowledge work? What counts as knowing?
CORE-06  What is agency / freedom? Can the subject act?
CORE-07  What is the cause of suffering / error / bondage?
CORE-08  What is the goal / liberation / salvation? How reached?
CORE-09  What is time? What is change?
CORE-10  What is the body? Its relation to mind/self?
CORE-11  What is language / sound / word? What does it do?
CORE-12  The one and the many: how do they relate?
CORE-13  Knowledge vs ignorance / truth vs error: where does error come from?
CORE-14  Practice / ritual / method: what does it do?
CORE-15  The individual and the ultimate: how do they relate?
```

**These are deliberately neutral** — no "God," no "consciousness-is-fundamental," no "self."
Each gets a PUSHING run + a strength verdict (answered / partial / out-of-scope / silent).

### L1 — the TRADITION MODULES (pluggable, per family)

The deep questions ONLY a family of texts carries. Each module is keyed by a **tradition-family**
(not a single school). Ask a text the modules for its families.

```
ŚAIVA module (the 7-fold / 5-stage — the existing model)
  STAGE-1..7  (Being/Power/Manifestation/Limitation/Cognition/Value/Liberation)
  via its sub-terms: prakāśa/vimarśa, śakti, ābhāsa, pratyabhijñā, spanda, māyā/kañcukas,
  kula/akula, mantra, tattvas, dīkṣā, paśu/pati.

BUDDHIST module (future)
  CORE-agnostic + the Buddhist register: duḥkha, impermanence, no-self (anātman),
  dependent arising (pratītyasamutpāda), emptiness (śūnyatā), the two truths,
  karma/rebirth, the path, nirvāṇa, the mind (citta/vijñāna), meditation.

NYĀYA / analytic module (future)
  the padārthas, pramāṇas (means of knowledge), the categories, inference,
  negation/apoha, the self (ātman), liberation as cessation.

GREEK / PLATONIST module (future)
  being, the Forms, the One, nous, soul, matter, becoming, the good, dialectic,
  the divine, virtue, contemplation.
```

**The 7-fold is Śaiva's module, not the system.** This is the key change from the current spec.

### L2 — the SCHOOL FINE-GRAIN (optional, per school within a family)

The single-school register, for maximum penetration:
```
pratyabhijñā sub-module: recognition, A≢B≢C, the nine operations, memory/freedom.
kubjikā sub-module: the goddess, the phonemes, the mantra-body, ritual topology.
spanda sub-module: the pulse, the wheel of powers, the perceiver-never-deviates.
```
Ask these only if the text's school is known (from the atlas tag).

---

## The QUESTIONNAIRE object (how it's stored)

```ts
interface Questionnaire {
  id: string;
  level: "CORE" | "TRADITION" | "SCHOOL";
  family?: "saiva" | "buddhist" | "nyaya" | "greek";  // for TRADITION/SCHOOL
  questions: { id: string; text: string }[];
}
```

- **CORE** is one fixed questionnaire (id `core-v1`), asked of every text — the comparability spine.
- **TRADITION/SCHOOL** questionnaires are a registry keyed by family/school; a text gets the modules
  for its atlas tags.
- A text's full questionnaire = `CORE + (its families' modules) + (its schools' sub-modules)`.

---

## THE MATRIX (output)

```
QUESTION: CORE-01  What is the ultimate?
  IPVV         → (Śaiva) WELL_SUPPORTED: "the Light (prakāśa) that is self-apprehending…"   [passages]
  Tantrāloka   → (Śaiva) WELL_SUPPORTED: "the Unsurpassed (anuttara)…"                      [passages]
  [future] Heart Sutra → (Buddhist) WELL_SUPPORTED: "form is emptiness (śūnyatā)…"          [passages]
  [future] Parmenides  → (Greek) PLAUSIBLE: "Being is, non-being is not…"                   [passages]
  Nyāya sūtra  → (analytic) OUT_OF_SCOPE: "ultimate" is not a primary register; categories are.
```

Each cell: `{ text, question, answer, passages[], strength, penetrations, branches }`.

**The SAME CORE row is comparable across all four traditions** — "what is the ultimate?" now has a
direct Śaiva/Buddhist/Greek/analytic juxtaposition. The tradition modules then go deep per text.

---

## WHY THIS IS THE RIGHT SHAPE (the growth path)

| Question | Answer |
|---|---|
| "Is this Tantra-only?" | No. CORE is agnostic; Tantra is one module. |
| "How does Buddhism get in?" | Add a `buddhist` TRADITION module (duḥkha, anātman, śūnyatā…). No change to CORE. |
| "How does Greek get in?" | Add a `greek` TRADITION module. No change to CORE. |
| "Does the 7-fold get lost?" | No — it's the Śaiva module (L1), still the deep layer for Tantra texts. |
| "How do I compare Śaiva vs Buddhist?" | The CORE row (e.g. "what is the ultimate?") is the clean comparison; then each text's module gives depth. |
| "What if a text has no tradition tag?" | It gets CORE only (still comparable); its register is mapped by which CORE questions are SILENT/OUT_OF_SCOPE. |

**The silent/out-of-scope map becomes the tradition-mapper**: a text that is SILENT on
CORE-02 (consciousness) but rich on CORE-14 (practice) is a ritual text — regardless of which
tradition module it's tagged with. That is a powerful, data-driven way to place any text in the
intellectual landscape.

---

## What this means for the existing spec

`SPEC_COMPARATIVE_PUSHING.md` should be updated to this **layered** model:
- CORE-01..15 → L0 (the agnostic spine).
- 7-fold/5-stage → L1 Śaiva module (not "the Tantra layer" — it's *a* module).
- TAN sub-terms → the school fine-grain (L2) where the Śaiva schools need more depth.
- Add the `family` key so Buddhist/Greek/Nyāya modules can be added later without touching CORE.

---

## Recommended next steps (todos)

- [ ] Update `SPEC_COMPARATIVE_PUSHING.md` to the L0/L1/L2 layered model (CORE + family modules +
      school fine-grain), with the 7-fold as the Śaiva L1 module.
- [ ] Create `data/corpus/questionnaires.ts` — CORE (fixed) + the `saiva` module (7-fold/5-stage) +
      a stub `buddhist` module to prove extensibility.
- [ ] `data/corpus/comparative.ts` + `/api/comparative` + MCP — the matrix.
- [ ] Seed run: CORE-01..03 + the Śaiva 7-fold on IPVV / Tantrāloka / Spandakārikā.
- [ ] Note the family-extensibility in the docs (Buddhist/Greek modules are future, gated on a
      corpus existing).

This makes Pāṭala's comparative layer **Tantra-agnostic and growth-ready**: a fixed comparable core
plus pluggable tradition depth. The 7-fold is honored as the deep Śaiva layer, not the whole system.
