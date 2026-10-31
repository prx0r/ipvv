# SPEC — COMPARATIVE PUSHING (the same core questions asked of every text)

*2026-08-12. An agnostic comparative-pushing protocol: every primary source is asked the SAME core
fundamental questions, so the answers build a **cross-text comparative study matrix** — one question
across many texts. The Tantra-specialized layer is **already built**: the **7-fold comparative model**
and the **5-stage lens** (in `research-library/`) ARE the deep Śaiva comparative questionnaire. This
spec operationalizes them into the pushing protocol, so the comparative matrix is grounded in the
existing model rather than a parallel invention. The method is the PUSHING method; the new thing is
the FIXED QUESTIONNAIRE that makes the outputs directly comparable.*

---

## 1. The vision

> Ask every text the same deep questions. The text may not answer them fully — that is fine and
> itself a result (an "unanswered / out of scope" is comparative data). Over time, build a matrix:
> **question × text → answer (strength-graded, passage-anchored)**. That is a genuine comparative
> study of the Śaiva tradition (and beyond), grown from the texts themselves rather than imposed.

The value:
- **Direct comparison** — "What is consciousness in IPVV vs Tantrāloka vs Spandakārikā?" becomes a
  row lookup, not a re-reading.
- **The unanswered is data** — a text that does not treat a question tells you its scope/register.
- **Compounds** — each new text fills a column; the matrix grows without re-asking.

---

## 2. The two question layers

### Layer A — the AGNOSTIC CORE (question-SHAPES from the real DNA)

**The core is NOT an abstract "what is X" list.** It is the **question-shapes** the user actually
uses in the Logicvids and the PUSHING sessions (see `QUESTIONNAIRE_REAL_DNA.md`): mechanism-gap,
crux, subversion, quantifier, register, root — in tradition-neutral form. Every text is asked these
same shapes so the answers are comparable:

```
MECHANISM-GAP (why is X necessarily Y?)
  CORE-M1  Why must the fundamental be self-related (self-grounding / self-apprehending)?
  CORE-M2  Why must cognition be active, not merely receptive? (what does knowing ADD?)
  CORE-M3  Why does the one become the many at all? (what forces differentiation?)
  CORE-M4  Why is there a gap between what the subject is and what it experiences?

CRUX / theodicy (the hardest seam)
  CORE-C1  Why does suffering / error / impurity arise from a ground that is good / whole?
  CORE-C2  Is the tradition's own central example really what it claims? (the mother's-grief test)

SUBVERSION (assumptions attacked)
  CORE-S1  Does every cognition / state know itself? (or is self-knowledge occasional?)
  CORE-S2  Is the subject really universal, or merely the particular it experiences?

QUANTIFIER (the universal-from-particular gap)
  CORE-Q1  How does "I am not X" become "I am the consciousness of all X"?

REGISTER (what is it to experience this?)
  CORE-R1  What is the FELT of the teaching? (not just the doctrine)
  CORE-R2  What does one actually DO? (the practice, not the metaphysics)

ROOT (the same question, repeatedly deepened)
  CORE-RT1 What is time? — asked until it becomes "is time itself X's activity?"
  CORE-RT2 What is the one-and-many? — asked until it becomes a specific mechanism
```

These are the **same shapes** as the Śaiva Q1–Q25, in neutral form. A Buddhist text gets the same
shapes at its own seams (emptiness, dependent arising); a Greek text at its own (Being, the One,
participation). The answer may be partial / out-of-scope / silent — that is data.

> **The ground truth:** the actual questions are in
> `QUESTIONNAIRE_REAL_DNA.md` (the Q1–Q25 from PUSHING-TANTRALOKA + the Logicvid penetrations).
> The CORE above is their abstraction to neutral shapes; the Śaiva Q1–Q25 are the concrete seed.

### Layer B — the TRADITION MODULE (the empirical Q1–Q25, not just the 7-fold)

**The Śaiva module is the empirical master-question set grown by pushing the Tantrāloka** — Q1–Q25 in
`QUESTIONNAIRE_REAL_DNA.md` (reflexivity, the powers, the upāyas, recognition-not-attainment, time,
grace, the theodicy, mother's-grief, love-as-root, rasa-as-felt…). These are the deep questions the
text forced.

The **7-fold / 5-stage model** (`research-library/7-FOLD-COMPARATIVE-MODEL.md`,
`5-STAGE-LENS-ACROSS-SCHOOLS.md`) is the *organizing frame* over these — it names the stages each
question belongs to (Being/Power/Manifestation/Limitation/Cognition/Value/Liberation) and which
school foregrounds which. So:

```
ŚAIVA MODULE = the empirical Q1–Q25 (the real questions) ORGANIZED BY the 7-fold/5-stage frame
  STAGE-1 Being          ← Q1 (reflexivity), Q16 (difference real at Śiva)
  STAGE-2 Power          ← Q2 (the powers), Q9/Q11 (grace)
  STAGE-3 Manifestation  ← Q10 (direction as felt), Q13 (rasa alaukika)
  STAGE-4 Limitation     ← Q17 (māyā line), Q5 (time)
  STAGE-5 Cognition      ← Q4 (recognition), Q6 (apoha)
  STAGE-6 Value          ← Q19-Q23 (suffering-as-rasa, love-as-root, fear)
  STAGE-7 Liberation     ← Q14 (the practical ladder), Q18 (theodicy dissolved)
```

The Q1–Q25 are the **content**; the 7-fold is the **frame**. A future Buddhist module would be grown
the same way (push a Buddhist text until its own Q1–Qn emerge), then organized by its own frame.

---

## 3. The output — the comparative matrix

Per text, the pushing run fills a questionnaire row-set. Across texts, a question becomes a column.

```
QUESTION: CORE-01  What is consciousness?
  IPVV         → WELL_SUPPORTED: "manifestation that is self-apprehending (prakāśa-vimarśa)…"  [passages]
  Tantrāloka   → WELL_SUPPORTED: "the Light (prakāśa) whose essence is reflective awareness…"   [passages]
  Spandakārikā → PLAUSIBLE: "the pulse (spanda), the vibratory dynamism of consciousness…"      [passages]
  Kubjikāmata  → PARTIAL / out-of-scope: "consciousness" is not the primary register; sound is.   [silent or oblique]
  Nyāya sūtra  → (if included) OUT-OF-SCOPE: treats cognition technically, not phenomenally.
```

Each cell:
```
{ text, question, answer_summary, passages[], strength: PROVED|REVIEWED|WELL_SUPPORTED|PLAUSIBLE|PARTIAL|SILENT|OUT_OF_SCOPE,
  penetrations[], branches[] }
```

**The strength "SILENT" and "OUT_OF_SCOPE" are as valuable as an answer** — they map the register of
each text (where it operates, where it is silent).

---

## 4. The comparative study it enables

- **Row-to-row**: "how does each text treat the one-and-many?" → direct juxtaposition.
- **The unanswered map**: which questions each tradition foregrounds vs ignores → a map of each
  school's problem-space.
- **Register comparison**: a ritual text vs a philosophical text — different questions are in-scope.
- **Argument truth-packets** still extract (the best answers get formalized per
  `SPEC_ARGUMENT_TRUTH_PACKET.md`).
- **Later**: a "one-and-many" comparative essay is *derived* from the matrix column, not re-researched.

---

## 5. How it runs (per text, agnostic)

For a new source:
1. Assemble the text (T1/L2/L200/C1 + the spine + the hub).
2. Run the **CORE question-shapes** (CORE-M/C/S/Q/R/RT — the agnostic DNA shapes) — each a PUSHING run.
3. Run the **Śaiva module** (the empirical Q1–Q25) organized by the **7-fold frame** — all 7 stages,
   noting which the text's tradition foregrounds and how it answers the others.
4. For each question: answer + passages + strength (+ penetrations/branches for the juicy ones).
   **Also record the NEW questions the text forces** (branches) — these are the grown layer.
5. Append the row-set to the comparative matrix (`data/corpus/comparative.ts`).
6. The matrix is queryable: question → all texts' answers; text → all its answers.

The text may "not answer properly" — record the strength honestly and move on. The matrix is the
asset.

**The question source (the real DNA — read first):**
- `QUESTIONNAIRE_REAL_DNA.md` — the CORE question-shapes + the empirical Śaiva Q1–Q25.
- `research-library/7-FOLD-COMPARATIVE-MODEL.md` — the frame (7 stages + school×stage map).
- `research-library/comparative/7-fold-across-schools.md` — the Patala-aligned version.
- `research-library/5-STAGE-LENS-ACROSS-SCHOOLS.md` — the consciousness 5-stage lens.
- `recognition/pushing-tantraloka/PUSHING-TANTRALOKA.md` — where the Q1–Q25 actually came from.

---

## 6. Wiring

- **Data**: `data/corpus/comparative.ts` — the matrix (text × question × answer-cell).
- **API**: `/api/comparative?question=CORE-01` → all texts' answers; `?text=<work>` → its row-set.
- **MCP**: `comparative_pushing` / `get_comparative_answers` tools.
- **Hub**: comparative-pushing is a kind on the source hub (`pt:hub:<work>:comparative`).
- **Question banks**: the CORE + TAN questionnaires live as data (`data/corpus/questionnaires.ts`),
  versioned, so a new text is asked the exact same questions as the others (the comparability
  guarantee).

---

## 7. Immediate next steps (todos)

- [ ] **Questionnaires data** (`data/corpus/questionnaires.ts`) — the CORE question-shapes (from
      `QUESTIONNAIRE_REAL_DNA.md`) + the Śaiva module (the empirical Q1–Q25) organized by the 7-fold
      frame, versioned for comparability.
- [ ] **Comparative matrix** (`data/corpus/comparative.ts`) + `/api/comparative` + MCP.
- [ ] **Seed one run**: run the CORE shapes + the Śaiva Q1–Q25 on 2–3 works (IPVV, Tantrāloka,
      Spandakārikā) to prove the matrix and the "silent/out-of-scope is data" claim — and to confirm
      the 7-fold school×stage predictions.
- [ ] **Wire the hub** comparative kind.

This is the highest-leverage comparative primitive: **ask every text the same deep question-SHAPES,
let the unanswered map the tradition, and grow each text's own branches — grounded in the real
Q1–Q25 the PUSHING sessions produced.**
