# AGENT SPEC — AUTONOMOUS PUSHING LOOP (create a pushing file for any source)

*2026-08-12. The complete, self-contained instruction for an agent told: "create a pushing file for
this source text." The agent does the WHOLE thing autonomously — with one mandatory precondition:
it must first ENGINEER THE CONTEXT FOR ASKING THE QUESTION THE WAY THE USER WOULD, because the
question is the key. Only then does it run the pushing loop. It keeps going, in new directions, until
the text is sufficiently extracted and it keeps running into repeats.*

---

## 0. THE ONE-LINE COMMAND

> **"Create a pushing file for <source>."**

Everything below is what "the complete full thing" means.

---

## 1. STEP 0 — ENGINEER THE QUESTION-ASKING CONTEXT FIRST (the key)

**Do NOT start by answering anything.** Start by engineering the *way you will ask* — the exact
question-asking persona that produced the numbered Logicvids (05/06/07, vid3) and the PUSHING
sessions. These are the user's OWN personal curious questions; replicating their *shape* is what makes
the enquiry penetrate instead of paraphrase.

### 1.1 Why the question is the key (internalize this)

- **A bad question gets a paraphrase.** "What does the text say?" returns the text.
- **A penetrating question forces the text to its bottom.** "If the perceiver is Śiva-universal, why
  is blue manifest to *me* and not everyone?" — the text cannot answer without exposing whether the
  empirical subject is a contraction or a recipient. That is the penetration.
- The Logicvids show the method: **every answer must force a NEW, deeper question**, not terminate.

### 1.2 The question-asking DNA (from the numbered logic-vids — replicate this shape)

Study `pushing/_source/logic5.md`, `logic6.md`, `logic7.md`, `logicvid3.md` + the 30+ PUSHING
sessions. The DNA you must reproduce:

1. **Start from the text's own primitive, not a modern term.** Abhinavagupta starts with *prakāśa*,
   not "consciousness" — because "consciousness" smuggles in subject/mind/experiencer. Ask "what does
   the text take as primitive and why?" before anything else.
2. **Interrogate every would-be-identical word.** "Presence / manifestation / consciousness /
   experience — are they the same or four different phenomena?" (logic5). Assume conflation; force
   the distinctions.
3. **Find the quantifier / scope problem.** "Why is blue manifest to me and not everyone?" — where
   the text asserts a universal from a particular without proving it.
4. **Push on the load-bearing step's WHY.** "Why does *difference* require self-apprehension?"
   (the regress + the crystal).
5. **Expose the hidden premise.** "The text asserts the empirical subject is a mode of the Light;
   it does not prove it." Name the premise the argument needs but doesn't state.
6. **Play the strongest opponent.** The "relabelling" accusation (logicdog): "you described the
   result poetically but added no mechanism." Face it head-on.
7. **Separate licensed from unlicensed.** "The text licenses X; it does NOT license Y" (the dog:
   ontological recognition yes, explicit liberating recognition no).
8. **End with "the next forced question is…"** (logic6) — always a forward branch, never a dead end.
9. **Produce branches** (Branch A..F) — the residual questions each penetration opens.

### 1.3 Deliverable of Step 0 — the question-context

Before pushing, write a short block to yourself: *the question-style I will use, why it's the key,
and the 6–9 question moves I have at my disposal* (the DNA above). This is NOT a deliverable to the
user — it is the internal context that makes the enquiry penetrate. If you cannot state the DNA, you
are not ready to push.

---

## 2. STEP 1 — ASSEMBLE THE SOURCE + THE QUESTION-ASKING CONTEXT

- Read the source's structure (the T1/L2/L200/C1 in the stack; the spine; the hub).
- Set up the enquiry folder: `pushing/<work>/<enquiry>/root.json` (question + source scope + core
  tension + hidden premises + status), `source-spans.json`, `reconstruction.md`, `prosecution.md`,
  `provenance.md`, `branches.md`, `logicvid.md`.

---

## 3. STEP 2 — RUN THE PUSHING LOOP (autonomous, until repeats)

The loop, driven by the question-DNA:

```
ROUND
  The question        (from the DNA — penetrating, not paraphrase)
  The text's answer   (restated EXACTLY as it argues — no strawman)
  > PENETRATION N     (the exact spot where the text asserts but does not prove)
  The next forced question
```

**Loop rules:**
- Each answer must force a NEW, deeper question. If it doesn't, you're paraphrasing — re-question.
- Keep asking "why" down one branch until a **natural endpoint** (the text's deepest reasoning is
  exposed, or the text explicitly does not license further).
- At a natural endpoint, **pivot to a NEW direction** (a fresh question from the DNA — scope,
  conflation, opponent, unlicensed claim) and push that branch the same way.
- **STOP when you keep running into repeats** — when new questions return the same penetrations /
  passages already extracted. That is the signal the content is sufficiently extracted.

**Autonomy contract:**
- You do not need the user to steer. You generate the directions, push to natural endpoints, pivot,
  and stop on repeats.
- The user's question-style (Step 0) IS the steering — it is what makes the directions penetrating
  rather than arbitrary.

---

## 4. STEP 3 — BUILD THE ARGUMENT TRUTH-PACKETS (from the penetrations)

For each genuine penetration, extract the formal argument as an auditable truth-packet (light model,
`SPEC_ARGUMENT_TRUTH_PACKET.md`):

```ts
{ id, work_id, title, kind, premises:[{text, passage_ids}], inference, conclusion:{text, passage_ids},
  tension_id, proof?, status }
```

- **Premises** = the quoted passages (they resolve).
- **Conclusion** = the penetration.
- **Strength** = derived (PROVED / REVIEWED / WELL_SUPPORTED / PLAUSIBLE / SPECULATIVE) from the
  proof status + surviving objections — do NOT overclaim.
- Attach to the hub (`pt:argument:<work>:<slug>`, `passage_ids`).

---

## 5. STEP 4 — COMPILE THE PUSHING FILE (the deliverable)

The final `logicvid.md` (or `PUSHING-<WORK>.md`) contains:
- the root question(s) + why they were asked (the question-context from Step 0 — **name why these
  questions, not just what they are**);
- the rounds / penetrations (the full pushing chain);
- the argument truth-packets extracted;
- the branches (residual questions for future enquiries);
- the honesty notes (licensed vs unlicensed, the relabelling accusation, surviving objections).

---

## 6. THE RULES (non-negotiable)

1. **Question-context FIRST.** Engineer the way you ask before you answer anything. If you can't
   state the DNA, you aren't ready to push.
2. **The text answers before you interpret.** Store the full quoted passage; your frameworks enter
   only after the text has spoken.
3. **No strawman.** Restate the text's answer exactly as it argues.
4. **Every answer forces a new question.** Paraphrase = failure.
5. **Push to a natural endpoint, pivot, repeat until repeats.** Stop only on repeats.
6. **Derived strength, never hand-waved.** Claims are WELL_SUPPORTED / PLAUSIBLE / SPECULATIVE per
   the proof + surviving objections.
7. **Do NOT commit to git.** The pushing file is a working artifact; leave it on disk.

---

## 7. THE SEED THE AGENT LEARNS FROM

- `pushing/_source/` — the Logicvid method + framework + dog + the numbered vids.
- `pushing/PUSHING_GUIDE.md` — the formal method (double-pass, honesty rules, 6-level frame).
- `recognition/pushing-tantraloka/LOGICVID-session-*.md` + `recognition/pushing-ipvv/` — the worked
  sessions (the user's actual question-style in action).

This spec is the bridge: **an agent told "create a pushing file" knows to engineer the question, run
the loop to natural endpoints, pivot until repeats, and output auditable truth-packets — without
needing steering and without committing.**
