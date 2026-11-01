---
name: c2-voice-corpus
description: "Navigate the C2 voice corpus (site/data/c2/corpus/): dictionaries, transcripts, parallels, doctrine. Use when choosing slang for a rendering, validating a term's payload or register, finding exemplar phrasing, or checking whether a term is really shared MLE vs a lookalike."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [c2, corpus, slang, roadman, gen-z, validation, exemplars]
    related_skills: [render-c2]
    checkpoint: CP4 (grounded voice material only — nothing unvetted enters a rendering)
---

# C2 voice corpus — how to use it

All voice material lives in `site/data/c2/corpus/`, indexed in `INDEX.md`.
Rule of the corpus: **payload or ban, and registers never blend.** US gen-z and
UK roadman stay in their own files; a term crosses only with a written reason.

## Which part to reach for

| Need | Go to |
|------|-------|
| A gen-z word with definition + example | `dictionaries/turnitgenz.json` |
| A roadman word with definition + example | `dictionaries/roadman-az.json`, cross-check `dictionaries/newsweek-topboy.json` |
| Is this term really shared (not Toronto-only, not a meme)? | `dictionaries/toronto-shared.json` (`toronto_status`) + `doctrine/mle-core-47.json` |
| US-side meaning preservation for a slang mapping | `dictionaries/value-sae-aave.json` (fluent-speaker validated) |
| Full Toronto row (register, origin, offensiveness) | `dictionaries/toronto-slang.csv` |
| How Cench actually talks (cadence, honesty tics, motto-flips) | `transcripts/cench-chickenshop.json` |
| Sustained sacred gen-z across a chapter | `parallels/genz-matthew6.json` |
| Devotional-scholarly register, team-made | `parallels/magnificat-genz.json` |
| Labeled-paraphrase-beside-canon precedent | `parallels/baeble-pairs.json` |
| Newest wave (trend watch, not canon) | `doctrine/kym2025.json` |
| Old pairs for normalization only | `dictionaries/gen_z_slangs_translation.csv` (dated for generation) |

## Worked examples

**1. "Can I use *leng* for bliss?"**
roadman-az says weapon/dangerous person; Toronto-shared lists leng = attractive,
synonym of peng. Both true — it's polysemous. Verdict filed in the glossary:
graded-only (`lengest`, `proper leng`), never bare near power verses. This is the
workflow: two dictionary hits + one shared-status check = a verdict with reasons.

**2. "Is *bless up* real?"**
newsweek-topboy: leave the conversation on a positive note, wish well. Payload:
salutation. Used in v5 (roadman) as the entire defense — one greeting that ends
the fight. Validated before use, not after.

**3. "I need roadman cadence, not just words."**
Don't open a dictionary — open `transcripts/cench-chickenshop.json`: circular
honesty ("I don't know man"), sincerity tics ("I swear", "God knows"), motto
material ("time will tell", "it's a lie until it's really real"). Cadence lives
in transcripts; payloads live in dictionaries. You need both.

**4. "Does sustained sacred gen-z actually hold?"**
Read `parallels/genz-matthew6.json` end to end (34 verses), then
`parallels/magnificat-genz.json` for the devotional register. If the voice can't
survive a chapter, it can't carry a stotra. New coinages must pass the same test:
draft three verses in the voice before trusting it with one.

## Adding to the corpus

New material lands in the matching folder with source + date in the file's top-level
`source`/`note` fields, then gets one line in `INDEX.md` (worked lookups grow, never
shrink). Trend-watch (KYM-style) never promotes to doctrine without a second source.
Validation chain, strongest first: MLE-core-47 membership → toronto-shared status →
two-dictionary agreement → single-source (unvetted, do not render from it).
