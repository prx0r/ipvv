---
name: render-c2
description: "Render a C2 — a style-parameterized English rendition of one canonical verse (gen z, plain, poetic, any register). Grounded on EVERY floor of the translation stack; style changes diction only, never meaning. The end is a compact faithful interpretation that transmits — claim plus rasa, in the requested voice. Use when asked to render a verse in a style, produce a C2, or preview a register."
version: 2.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [c2, style, register, rendition, tantra, grounding, rasa, transmission, patala]
    related_skills: [write-commentary, translate-work, lore-prime-argmap, validate-passage]
    checkpoint: CP4 (styled renderings over the audited stack)
---

# Render C2 — the styled rendition

## Purpose

C2 is a style-parameterized English rendition of ONE canonical verse. The reader
names any style ("gen z", "plain", "sailor", "bedtime story") and gets that verse
back in that voice — as a **compact faithful interpretation that meaningfully
transmits**: the reader of that voice must get both what the verse claims AND
what it feels like (its rasa). Claim without rasa is a summary. Rasa without
claim is a mood. C2 carries both, in 2–6 sentences.

It is not a new translation, a new commentary, or a new claim. Every floor of
the translation stack stands behind it; style changes diction and rhythm only.

## The grounding map — C2 relies on every floor

Assemble the packet for the target verse. Each floor contributes something C2
cannot work without:

```
floor                        what C2 takes from it
───────────────────────────── ──────────────────────────────────────────────
Sanskrit (source span)        the anchor; the verse as uttered, nothing else
L0 / canonical T1 gloss      the technical terms (śakti, spanda, vimarśa…);
                             terms keep their Sanskrit on first use, then voice freely
L1 (close, prop-faithful)    the load-bearing propositions — EVERY one must
                             survive the rendering, in any voice
R1 cruxes / T2 rival         (where present, e.g. IPVV passages) the contested
                             zones — C2 never smuggles a contested reading as
                             certain; hedge in-voice or omit
R2 adjudication              CONSTRAINED readings must be kept exactly;
                             PREFERRED kept by default; OPEN left open
T3 / L2 (resolved reading)   the settled English; C2's fidelity baseline
arguments packet             the claim skeleton: question → premises →
(Q/premises/inference/       inference → conclusion, plus unresolved points.
 conclusion/unresolved)      Never close an unresolved point.
C1 (capstone commentary)     what it means — AND its rasa: the felt sense a
                             reader must get. Rasa is the transmission target.
gate                         permission. PASS renders; anything else refuses.
```

Where a floor is absent for a work (stotra works lean on L1/L2/C1 + gate; the
adversarial floors live fullest on IPVV passages), render from what is present —
never invent the missing floor's content.

## Rasa — the transmission test

Before rendering, read C1 and name the rasa in one line: what the verse wants
the reader to feel or grasp (refuge, vertigo, recognition, hunger, stillness…).
That line is scaffolding — it never ships — but the rendition fails without it.

C2 succeeds iff a reader at home in the requested voice walks away with both:
the claim (checkable against L1) and the savor (checkable against C1). If slang
cannot carry a claim, drop to a plainer synonym — never substitute a different
claim, never add doctrine, never add examples or morals the packet lacks.

## Hard rules (fail-closed)

1. **PASS only.** `gate !== 'PASS'` → refuse with `English withheld — gate <GATE>`.
   Style is never a way around the gate.
2. **Meaning locked.** Every C2 sentence must trace to L1/L2/C1 or the claim
   skeleton. No new entities: no named people, places, texts, or schools the
   packet does not name. No modern comparisons beyond diction itself.
3. **Open stays open.** Unresolved points and OPEN cruxes are hedged in-voice
   ("maybe", "the verse leaves it there") or omitted — never settled.
4. **Terms anchored.** Sanskrit technical terms appear in Sanskrit on first use,
   then in whatever voice fits. Nothing load-bearing is lost to slang.
5. **Verse-scale.** One verse in, one short interpretation out. Never summarize
   the work; never continue into the next verse.
6. **Voice, not persona.** The voice may joke; it may not preach, flatter the
   reader, or claim authority ("trust me", "as we all know").
7. **Labeled.** Every C2 ships `{style, model, work, chunk, date}` and the words
   "machine rendering". C2 is never stored beside L1/L2/C1 as if canonical.

## Prompt shape

Evidence first, rasa second, style last, constraints binding:

```
You render verses into a requested voice. Meaning is FIXED by the canonical
packet below — every floor of the translation stack stands behind it. Change
diction and rhythm only.

Source (Sanskrit): <sanskrit>
Load-bearing propositions (L1 — every one must survive): <l1>
Resolved reading (L2): <l2>
Commentary — what it means (C1): <c1 or 'none on file — stay inside L1/L2'>
Claim skeleton (question → premises → conclusion): <arguments packet, trimmed>
Open points (hedge or omit, never close): <unresolved or 'none listed'>
Contested readings (never present as certain): <R1/T2 where present, else 'none on file'>

First, in one silent line, name this verse's rasa: what must the reader feel.
Then render.

Voice: <style, max 60 chars>
Rules: 2–6 sentences. Same claims, same savor, new voice. Sanskrit terms keep
their Sanskrit on first use. No new doctrine, no new names, no preaching, no
second verse. If a claim won't fit the voice, say it plainly.

Rendition:
```

(The silent rasa line is scaffolding — strip it before shipping. Output shape
below carries no trace of it.)

## Output shape

```json
{
  "c2": "<rendition text>",
  "style": "<style as given>",
  "model": "<model id>",
  "provenance": {"work": "<wid>", "chunk": "<cid>", "gate": "PASS", "date": "<iso>"},
  "label": "machine rendering"
}
```

## Cost discipline

Verse-scale calls only (`max_tokens` ≤ 350). One verse per call — never batch a
work through the style endpoint; batch C2 seeding (if ever) goes through the
same skill with the same per-verse prompt, offline, reviewed before it ships.
