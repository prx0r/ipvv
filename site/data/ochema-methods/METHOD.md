# METHOD — How ochema2 Works

## 1. The status system

Every claim in every ochema2 document carries one of six statuses.
They are mutually exclusive and must be assigned honestly.

| Code | Meaning | Example |
|---|---|---|
| **T** | Textual — explicitly stated in the source | "TĀ 1.54: the Light of consciousness shines at all times" |
| **R** | Reconstructed — the strongest argument recoverable from the source | "Utpaladeva's regress argument, reconstructed from APS" |
| **E** | Empirical — experimentally supported | "Levin: bioelectric states store morphogenetic targets (B-grade science)" |
| **C** | Correspondence — two systems address the same structural problem | "Proclus's participation and the Śaiva reflection model address the same plurality problem" |
| **H** | Hypothesis — possible but unproved | "Quality corresponds to geometry of state space" |
| **X** | Rejected — contradicted, invalid, or no longer required | "Gödel as proof of consciousness" |

**The inheritance rule (binding):** No tradition may inherit another
tradition's conclusion merely because they share a structure. A C is
always a C — it never upgrades to E or T by accumulation.

## 2. The three honesty labels

On top of the status system, every document section gets one of three
labels. This replaces the A–E grading system, which conflated
different things and inflated speculative material:

| Label | Applies to |
|---|---|
| **Established** | Peer-reviewed science; verified text with location; completed argument (R) that survives its strongest objection |
| **Interpretive** | Mappings, correspondences, comparisons, readings — the programme's own work |
| **Speculative** | Metaphysical extensions, the density project's ontological claims, channeled material, untested hypotheses |

A speculative claim is not a defect. It is a label. It says so in the
first sentence: "SPECULATIVE — the Śaiva identification of
consciousness with camatkāra, considered as a hypothesis..."

## 3. The claim file (the unit of work)

Every claim studied in ochema2 gets a file:

```
# CLAIM: <the claim, in the source's words>

STATUS: T / R / E / C / H / X
LABEL: established / interpretive / speculative

SOURCE:
  Text: <name>
  Location: <volume/chapter/verse/line>
  Translation: <who, and any caveats>

WHAT IT SAYS:
  <plain-language statement, checked against scholarship>

MAPPING:
  Grid cell: <one of the nine operations, or "no mapping found">
  Scientific terms: <existing theory's terms, cited>
  Alignment: <accommodated by existing theory / contradicted by it /
               science silent>

ROOM FOR RESEARCH:
  <yes/no> — <what question this opens that science hasn't settled>
```

## 4. The mapping grid (the standardised vocabulary)

The nine operations from ĪPK 1.3.7, with scientific counterparts used
for MAPPING ONLY (never as identity claims):

| # | Operation | Sanskrit | Function | Science (mapping only) |
|---|---|---|---|---|
| 1 | Manifestation | jñāna/prakāśa | appearing | perception, state estimation |
| 2 | Retention | smṛti | past remains available | memory, attractors |
| 3 | Determination | apohana | this rather than that | selection, exclusion |
| 4 | Stream integration | anusandhāna | temporal/personal connection | integration, ΦID |
| 5 | Counterfactual generation | vikalpa | novel forms | generative models |
| 6 | Value weighting | rāga | what matters | semantic information, homeostasis |
| 7 | Finite possibility space | kañcukas | what is possible | embodiment, constraints |
| 8 | Cross-stream boundary | deha-bheda | where synthesis stops | bioelectric closure |
| 9 | Inter-stream influence | pratibimba | other fields affect mine | social coupling |

Three extra grid cells for claims that don't fit the nine:

| A | Ground | what precedes/underlies manifestation | — |
| B | Transformation | change across scales (the density project's home) | — |
| C | Practice | what the tradition says must be done | — |

## 5. The honesty rule

> **No shared vocabulary counts as convergence without a shared
> constraint or prediction.**

Applied mechanically:
- "Both use exclusion" → C (correspondence), nothing more.
- "X in the text resembles Y in the theory" → C, nothing more.
- "The tradition's claim imposes a condition the theory did not
  assume" → now it earns attention.
- "The theory predicts a result the tradition's interpretation
  discriminates" → now it earns attention.

## 6. The comparison protocol (for Line 2)

When comparing traditions:

1. State each tradition's claim IN ITS OWN WORDS first (T), with
   location.
2. Map each onto the grid separately.
3. Only then compare grid positions. Same cell = C. Different cells =
   no correspondence, say so.
4. Never merge the traditions' vocabularies into one. The grid is the
   only common language, and it is a mapping tool, not a metaphysics.

## 7. The alignment protocol (for Line 3)

When checking a mapped claim against science:

1. Cite the scientific result (published, peer-reviewed).
2. State what it establishes, in its own terms.
3. State the correspondence, if any (C).
4. State the divergence, if any.
5. Verdict: accommodated / contradicted / science silent.
6. If "accommodated" — the mapping is a legitimate translation.
   If "contradicted" — the claim is X or H, say which.
   If "silent" — this is where the frontier files live.

## 8. The frontier file (for Line 4)

```
# FRONTIER: <name of the open question>

WHAT IS ESTABLISHED:
  <what we know, with statuses>

WHAT IS INTERPRETIVE:
  <the mappings and readings, labelled>

WHAT IS SPECULATIVE:
  <the hypotheses, labelled in the first sentence>

WHAT RESEARCH WOULD MOVE IT:
  <specific, doable, falsifiable where possible>
  <intervention → measurement → predicted result>
  <rival model predicting something different>
```

## 9. Versioning and correction

- Every document is dated and versioned.
- Corrections are made in place, with the correction noted, and the
  version bumped.
- An error found is a successful use of the method. It is logged, not
  hidden.
- The append-only log of the project's history lives in
  `checkpoints/` — each checkpoint is a compact, source-grounded
  record of conclusions that survived scrutiny.

## 10. What we never do

- Never claim a mapping is an identity.
- Never claim a correspondence is a convergence without a shared
  constraint or prediction.
- Never present a speculative claim as established.
- Never invent terminology. The nine operations are the vocabulary.
- Never let the programme's claims exceed the text's claims or the
  science's claims.
- Never discard the old work — it is reclassified, not deleted.
