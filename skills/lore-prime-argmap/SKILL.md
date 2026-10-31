---
name: lore-prime-argmap
description: "Before mapping any text's argument, get immersed in its scholarly lore via web search so you know what the argument is. Then build per-passage IPVV-style argmaps. Use when starting argument-map work on any text, or when an argmap feels flat."
version: 1.0.0
author: ipvv-pipeline
metadata:
  hermes:
    tags: [argmap, scholarship, research, ipvv, translation]
    related_skills: [translate-work, raw-l0, write-commentary]
    checkpoint: ARG (a text's argument understood before prose)
---

# Lore-Prime, Then Map (one text at a time)

## When to use
- Starting argument-map work on any text.
- An existing argmap feels flat (gloss dumps, "conclusion: see L2").
- Asked to "know what the argument is" before translating.

## Law
No argmap without lore. If you cannot state the text's opponent, its ally, and its stakes in two sentences, you are not ready to map. Go read.

## The flow — one text at a time

### 1. Claim the text
One text. Not the corpus. Name it, note its work dir, T1 status, L0 report.

### 2. Web search — get immersed
Search for the text + author + school + central problem. You are priming for the *argument*, so hunt:
- **Opponent:** who is being refuted? (e.g. Dharmakīrti's Sambandhaparīkṣā vs. Utpala)
- **Ally/resource:** whose tools are borrowed? (e.g. Bhartṛhari's Sambandhasamuddeśa)
- **Stakes:** what falls if the argument fails? (e.g. transaction, scripture, recognition)
- **Key secondary literature:** the live scholarly reads (MacCracken, Berger, Ratié, Torella…) and their distinctive claims (e.g. "retorsive transcendental argument").
- **Famous lines:** the verses/quotes scholarship orbits (e.g. *amiśrāḥ svayaṃ bhāvās tān yojayati kalpanā*).

Log the haul in the argmap header (who you read, what you took). Scholarship primes; it never substitutes for the Sanskrit.

### 3. Read the T1 + Sanskrit
Read the frozen T1 straight through with the lore in mind. Mark: where the opponent speaks, where the turn happens (*tatrocyate* moments), where the seal is.

### 4. Build per-passage argmaps (IPVV shape, never a singular md)
One file per passage: `<work>/argmaps/<passage>.md`. Each file:

```markdown
# <Work> <passage> — ARGUMENT MAP (<short gloss of what's at stake>)
*Date. Source: T1 <chunk> = edition <pp>. Lore: <who you read, 1 line>.*
## 1. What is at issue
<Opponent / ally / stakes, 1 paragraph. The question the passage answers.>
## 2. The argument, reconstructed step by step
**Step 0 — <name> (<ref>):**
> <Sanskrit maxim, verbatim>
[i.e. <plain unpacking>.]
**Objection (nanu):** <staged in their voice>
**Reply (naca):** <staged in ours>
## 3. Unresolved / uncertain (not invented)
<Numbered philological cruxes: variants, scope ambiguities, cited-but-absent texts.>
## 4. Decision for L2
<The doctrinal spine in one paragraph: what the prose must carry.>
```

### Shape rules (from the IPVV pilots)
- Steps carry source refs (line/page numbers) — every claim re-checkable.
- Sanskrit maxims quoted verbatim with `>` + `[i.e. …]` unpacking.
- Stage the dialectic: nanu/naca labels, opponent audible, turn marked.
- Unresolved = specific cruxes with scholar refs, never "none" on a hard text.
- Decision for L2 = the spine, not a summary.
- Argmaps are a *family* (per passage/chunk), plus L1 apparatus where the reasoning is dense. Never one flat md per work.

## Invariants
1. T1 immutable; L0 verbatim — map from them, never rewrite them.
2. Machine proposes, human disposes. Argmaps enter as `MACHINE_PROPOSED`.
3. Lore informs the map; the Sanskrit decides it. When they conflict, say so in §3.
4. Pushing flow reads these files — keep them sharp or keep them out.
