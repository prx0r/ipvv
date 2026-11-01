---
name: render-c2
description: "Render a C2 — a style-parameterized English rendition of one canonical verse (gen-z, plain, poetic, any register). Grounded on the full canonical packet (L0/L1/L2/C1/argmap); style changes diction only, never meaning. Use when asked to render a verse in a style, produce a C2, or preview a register."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [c2, style, register, rendition, tantra, grounding, patala]
    related_skills: [write-commentary, translate-work, validate-passage]
    checkpoint: CP4 (styled renderings over the audited stack)
---

# Render C2 — the styled rendition

## Purpose

C2 is a style-parameterized English rendition of ONE canonical verse. The reader
names any style ("gen z", "plain", "sailor", "bedtime story") and gets that verse
back in that voice.

It is not a new translation, a new commentary, or a new claim. All meaning comes
from the canonical packet. Style changes register and diction only.

```
canonical packet (fixed meaning)
 ├── Sanskrit (source span)
 ├── L1 (close translation — proposition-faithful)
 ├── L2 (reading translation — book prose)
 ├── C1 (commentary — what it means, 100–450 words)
 └── argmap (premises — what the verse argues)
        │
        ▼  style transfer (diction only)
        │
C2 (same claims, new voice)
```

## Inputs

Assemble the packet for the target verse before rendering. Minimum:

- `sanskrit` — the source verse (IAST)
- `l1` — close translation
- `l2` — reading translation
- `c1` — commentary (may be null for early works; render from L1/L2 then)
- `argmap` — argument map markdown (may be null; skip if absent)
- `gate` — PASS required (see rules)

Also carry: `work`, `chunk`, `model`, `date` for the provenance stamp.

## Hard rules (fail-closed)

1. **PASS only.** `gate !== 'PASS'` → refuse with `English withheld — gate <GATE>`.
   Never render BLOCKED/WITHHELD verses. Style is not a way around the gate.
2. **Meaning locked.** Every claim in C2 must be traceable to L1/L2/C1. If the
   style cannot carry a claim (e.g. slang has no word for it), drop to a plainer
   synonym — never substitute a different claim, never add doctrine, never add
   examples or morals the packet does not contain.
3. **No new entities.** No named people, places, texts, or schools unless the
   packet names them. No modern comparisons (no self-model, no neuroscience,
   no pop-culture references beyond diction).
4. **Verse-scale.** One verse in, one short rendition out (2–6 sentences).
   Never summarize the whole work; never continue into the next verse.
5. **Style is a parameter, not a persona.** The voice may joke, but it may not
   preach, flatter the reader, or claim authority ("trust me", "as we all know").
6. **Labeled.** Every C2 ships with `{style, model, work, chunk, date}` and the
   words "machine rendering". C2 is never stored beside L1/L2/C1 as if canonical.

## Prompt shape

Build the model prompt in this order — evidence first, style last, constraints
binding:

```
You render verses into a requested voice. Meaning is FIXED by the packet below.
Change diction and rhythm only.

Sanskrit: <sanskrit>
Close translation (proposition-faithful): <l1>
Reading translation (book prose): <l2>
Commentary (what it means): <c1 or 'none on file — stay inside L1/L2'>
Argument (what the verse claims): <argmap premises trimmed, or 'none'>

Voice: <style, max 60 chars>
Rules: 2–6 sentences. Same claims, new voice. No new doctrine, no new names,
no preaching, no second verse. If a claim won't fit the voice, say it plainly.

Rendition:
```

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

Verse-scale calls only (`max_tokens` ≤ 300). One verse per call — never batch a
whole work through the style endpoint; batch C2 seeding (if ever) goes through
the same skill with the same per-verse prompt, offline, reviewed before it ships.
