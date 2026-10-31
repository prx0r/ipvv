# PUSHING GUIDE — how to formally run a Pushing enquiry (the Logicvid method)

*2026-08-12. The comprehensive, reusable guide to the Logicvid / Pushing method, distilled from the
source files in `pushing/_source/` and the 30+ worked sessions in `research-library/recognition/`.
It answers: how do you mechanically, rigorously, FORMALLY push a text to its bottom — and how do you
turn the resulting logical arguments into auditable truth-packets you can cite in essays?*

> **For an agent told "create a pushing file for <source>":** read
> `AUTONOMOUS_PUSHING_AGENT_SPEC.md` — it is the self-contained instruction (engineer the
> question-asking context first, run the loop to natural endpoints, pivot until repeats, output
> truth-packets, do NOT commit to git). This guide is the *method*; the agent spec is the *operator*.

---

## PART 1 — WHAT PUSHING IS

### 1.1 The one rule

> **Hound the text with "why," and force its OWN reasoning out. Our frameworks only supply the
> questioning; the answers must come from the text.**

The extracted passages are the source of truth. Each question stores the full quoted passage (more
than needed) so the text's own argument can be re-read and re-pushed. Frameworks (aperture, MEPIT,
pure-thesis, Solms/valence) enter ONLY after the text has spoken.

### 1.2 The method is a graph-growth machine

From `logicvidsmethod.md`, the two loops that compose:

```
SANSKRIT → claims → definitions → dependencies → proof-or-boundary → GRAPH     (decomposition)
graph tension → paradox → hidden premises → branches → research → NEW GRAPH   (question-growth)
```

Pushing is the **question-growth** loop on top of the **decomposition** loop. It is not separate
from the formal engine — it is the layer that grows the graph the formal engine then proves over.

### 1.3 The three reliability levels (from logicvidsmethod)

| Level | Feasibility | What it yields |
|---|---|---|
| **1. Structural map** | absolutely feasible | per-āhnika/chunk: problem, primitives, presuppositions, new claim, inferential work, dependencies, tensions |
| **2. Hard metaphysical backbone** | feasible, slower | a minimal claim-chain, each arrow with passages + commentary + hidden premises + objections + confidence |
| **3. Definitive reconstruction** | not from one translation alone | needs the commentarial corpus (Jayaratha, Tantrasāra, Utpaladeva, Pratyabhijñā) |

**Advice:** build Level 1–2 first. Do not attempt Level 3 until the corpus (commentaries +
parallels) is assembled.

---

## PART 2 — THE FORMAL PROCEDURE

### 2.0 Set up the enquiry (the repeatable artifact)

Each enquiry is one folder (from logicvidsmethod):

```text
inquiries/<slug>/
  root.json            the question + source scope + core tension + hidden premises + status
  source-spans.json    the quoted passages (the text speaks)
  reconstruction.md    Pass A: the strongest coherent reconstruction
  prosecution.md       Pass B: destroy it
  provenance.md        Pass C: every claim → a passage
  branches.md          the residual questions
  logicvid.md          the compiled enquiry (the output)
```

`root.json`:
```json
{
  "question": "If I must already be Śiva to recognize myself as Śiva, how can I recognize myself as not-Śiva?",
  "source_scope": ["Tantrāloka", "Tantrasāra", "Īśvarapratyabhijñā"],
  "core_tension": ["identity is invariant", "self-knowledge is presently limited"],
  "hidden_premises": [],
  "status": "seed"
}
```

### 2.1 The three passes (the anti-cheat)

**Pass A — Construct.** Produce the strongest coherent reconstruction from the passages. Output:
primitives · claims · dependency chain · hidden premises · chapter function · tensions · questions.

**Pass B — Destroy.** A separate agent is FORBIDDEN from improving it; its only job is to find:
unsupported entailments · conflated levels · translation dependence · missing intermediate claims ·
passages that resist · rival readings · false formalization · contradictions hidden by vague wording.
The construct agent repairs only what survives.

**Pass C — Provenance audit.** Every explicit claim has a passage · every derived claim lists
premises · every cross-source claim preserves direction · every contradiction survives scope
separation · every Sanskrit term keeps tradition-local meaning.

### 2.2 The round-structure of a session (from the PUSHING transcripts)

Each session is a chain of rounds — question → the text's answer → the deeper question it forces:

```
ROUND N
  The question       (the sharp "why")
  The text's answer  (restated EXACTLY as it argues — no strawman)
  The new deeper question it forces
  > PENETRATION N:   (the exact spot where the text asserts but does not prove)
```

The example (Q1-reflexivity): "If the perceiver is Śiva-universal, why is blue manifest to me and
not everyone?" → the text replies via Sāṁkhya-refutation → the deeper question: "why is the
empirical 'me' a contraction of the Light rather than a recipient of it?" → **PENETRATION 1:** the
text asserts the collapse but does not prove it (the quantifier problem).

---

## PART 3 — THE HONESTY RULES (the discipline that makes it trustworthy)

### 3.1 The licensed-vs-not rule (from logicdog)

Always split what the text **licenses** from what it **does not**. Example ("Is a dog Śiva?"):
- **Ontological recognition** — the text licenses this: a dog enacts aham-vimarśa (contracted
  first-person), so "the dog manifests Śiva's recognitive structure."
- **Explicit liberating recognition** — the text does NOT license this: no reliable passage says a
  dog attains Pratyabhijñā liberation as a dog. State it as unsupported.

### 3.2 The relabelling accusation (from logicdog §5)

The naturalist's cleanest objection: `vimarśa` is "a metaphysical relabelling of multiscale
self-organization" — poetic description, no predictive mechanism. **You must face this head-on**:
Abhinavagupta can *accept every empirical mechanism* and still hold that it does not explain why
manifestation is self-apprehending. The reply is not "add mechanism" but "the mechanism presupposes
the manifest."

### 3.3 Three errors to refuse (from logicvidsmethod)

- **Compression error** — forcing distinct claims into one clean system.
- **Attribution error** — giving Abhinavagupta a later commentator's repair.
- **Bridge error** — treating similar terms as identical (prakāśa = phenomenal consciousness) when
  they are *probes, not identities*.

### 3.4 Never collapse levels (from logicframework)

Use the 6-level frame and never collapse:
```
M → D → B → N → W → R
manifestation → differentiation → bounded embodiment → normative agency → world-model → recognition
```
Science explains D→B→N→W; Pratyabhijñā proposes M→D and interprets R as W→awareness-of-M.
The dispute is whether M is generated by, identical with, or prior to the later levels. **Never
write "consciousness = integration."**

---

## PART 4 — TURNING ARGUMENTS INTO AUDITABLE TRUTH-PACKETS

This is the key idea: **treat a logical argument almost like a translation** — a derived object with
an auditable path, resolvable to source, graded by how well it is proved.

### 4.1 The argument as a first-class, translation-like object

Just as a translation has source_spans → target_spans → decisions → evidence, a logical argument has:

```
pt:argument:<work>:<slug> {
  work_id
  title
  kind            "reductio" | "analogy" | "identity" | "entailment" | "decomposition"
  premises        [ { text, passage_ids } ]
  inference       the typed move
  conclusion      { text, passage_ids }
  tension_id      the PUSHING question it resolves
  provenance      resolved passages (auditable path)
  proof           optional — the truth-engine trace (Lean / Nyāya)
  status          MACHINE_DRAFT → REVIEWED | PROVED | OUTSIDE_FORMAL | HOLLOW
}
```

The **auditable path** mirrors a translation's provenance: conclusion → inference → premises → each
premise resolves to its passage (via `/api/resolve`). You can trace any claim back to the Sanskrit.

### 4.2 Strength-graded claims (the "different strength" idea)

Not all arguments prove equally. Attach a **claim strength** so essays can cite at the right level:

```
PROVED           a formal proof exists (truth engine / Lean)
REVIEWED         human-review has accepted the reconstruction + provenance
WELL_SUPPORTED   premises resolve, inference is sound, no surviving prosecution
PLAUSIBLE        a coherent reconstruction with a live objection (the tension stands)
SPECULATIVE      a probe — explicitly NOT asserted as the text's claim
```

A claim's strength is **derived from the argument object's status + the surviving objections**, not
hand-waved. An essay then says "the text's position (WELL_SUPPORTED, prem. A, B, C)" vs "a possible
reading (SPECULATIVE)" — so the reader knows exactly how load-bearing each claim is.

### 4.3 Why this is like a translation

| Translation | Argument |
|---|---|
| source_spans | premises (each resolves to a passage) |
| target_spans | the claim / conclusion |
| decisions | the inference + hidden-premise choices |
| evidence | the quoted passages |
| review_state | claim strength (PROVED → SPECULATIVE) |
| resolve kernel | trace any claim back to Sanskrit |

This makes the argument a **truth-packet**: a self-contained, auditable, strength-graded object you
can cite in an essay (SHOW EVIDENCE → the argument → its premises → the passages), exactly like citing
a translation.

---

## PART 5 — THE COMPOUNDING PIPELINE (recap)

```
PUSHING enquiry (finds a tension, quotes the passages)
  → resolve passages (/api/resolve + published store)
  → FORMAL LOGICAL ARGUMENT (the truth-packet: premises/inference/conclusion + auditable path)
  → TRUTH ENGINE (nyāya/Lean: PROVED / OUTSIDE_FORMAL / HOLLOW)
  → ESSAY (cites the argument at its correct claim-strength)
  → LEARNING (from the essay)
  → back to PUSHING the next tension
```

Everything is tracked on the source hub (`/api/hub`) — `pt:hub:<work>:<kind>:<slug>` with
`passage_ids`. Nothing is orphaned.

---

## PART 6 — ADVICE (what actually works)

1. **Start at Level 1–2**, not Level 3. Build the structural map + a backbone of a few genuine
   cruxes before attempting the definitive reconstruction.
2. **One enquiry = one folder.** The repeatable artifact shape (§2.0) is the whole method made
   tangible. Get 5–10 excellent enquiries before exposing them via MCP/API.
3. **Face the relabelling accusation on every tension.** It is the strongest objection; meeting it
   is what separates a real penetration from a gloss.
4. **Store more passage than you need.** The text must be re-readable and re-pushable.
5. **Pass B must be a separate agent that cannot improve** — its only job is to destroy. This is
   the anti-cheat that makes the reconstruction trustworthy.
6. **Let the strength be derived, not claimed.** PROVED / REVIEWED / WELL_SUPPORTED / PLAUSIBLE /
   SPECULATIVE comes from the proof status + surviving objections, so no essay overclaims.
7. **Never collapse levels or terms.** The 6-level frame and the term-probes-vs-identities rule keep
   the analysis honest.

---

## PART 7 — THE SEED (what's on disk)

- **Source files:** `pushing/_source/` (logicvidsmethod, logicframework, logicframework2, logicdog,
  logic5/6/7, logicvid3, postmortem, PUSHING-TANTRALOKA, PUSHING-IPVV).
- **Worked sessions:** `recognition/pushing-tantraloka/LOGICVID-session-*.md` (30+) +
  `recognition/pushing-ipvv/LOGICVID-session-*.md`.
- **The hub:** `data/corpus/hub.ts` already tracks `pt:hub:ipvv:pushing:main` and
  `pt:hub:tantraloka:pushing:main`.

This guide is the how-to; the sessions are the evidence it works; the argument-object schema is the
natural next build (Agent 1).
