---
name: literal
description: "Render literal English — STE-inspired, Karpathy-80% plainness — for the svread LITERAL lane and chat plain mode. Use when asked for literal, plain, word-by-word, or ASD-STE100 output over Trika verses. Grounded on L0/L1, never freelanced. Not a translation, not a commentary, not a C2."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [literal, ste100, plain, translation, grounding, svread]
    related_skills: [render-c2, c2-voice-corpus, write-commentary, lore-prime-argmap]
    checkpoint: CP4 (grounded English only — nothing unvetted enters a lane)
---

# Literal — plain English over the verse

## Purpose

Literal is English with the ambiguity removed: one idea per sentence, plain
words, every proposition from the verse kept, nothing added. It is the floor
other English stands on — C2 renders *from* it, commentary explains *it*. It
carries no style and no rasa work. Flat is the point.

Two consumers, one rulebook:

- **LITERAL lane** (svread `?right=literal`): word-gloss L0 where on file,
  else close L1. Rendered from data, never generated live.
- **Chat `plain:` mode**: the user prefixes a question with `plain:` and the
  worker answers under this constraint (passages first, citations kept).

Karpathy's tip is the mechanism: *"80% of the way to ASD-STE100."*
ASD-STE100 is the aerospace controlled English (about 900 approved words, one
meaning each, short sentences). Models know it well. 80% keeps the clarity
without the stiffness. Credit: Karpathy (Oct 2026); community skill work this
adapts (MIT): `danyuchn/asd-ste100-skill` (structural/lexical split, scan
checklist, output discipline) and `prithivrajmu/asd-ste100` (80%-by-default,
preserve-meaning-first, keep-the-hedge guardrails).

## Grounding — literal never freelances

Literal renders from frozen floors only. This is stricter than C2, because
there is no style step to hide behind:

0. **Sanskrit first, whole stack re-read.** Before writing a word, re-read
   the verse's full stack in order: Sanskrit cite → T1 → L0 → argmap → L2
   → C1 essence. The argmap is the clearest explanation of what is going
   on (speaker, question, premises, inference) — resolve images there
   first, glosses last. Never render from the gloss alone: a gloss is a
   token, the stack is the meaning.
1. **L0 first.** Every content word maps to the T1/L0 gloss for that verse.
   One English word per Sanskrit term *within the verse* (STE one-word-one-
   meaning, mapped onto gloss discipline). Do not rotate synonyms.
2. **L1 carries the propositions.** Every load-bearing proposition in L1 must
   survive in the literal. Drop a proposition and it is a different claim.
3. **Sanskrit names stay.** Proper names and untranslatable terms stay in
   IAST (Bhairava, vimarśa as term-of-art on first use). Translate, never
   transliterate-and-leave, for everything else.
4. **BLOCKED refuses.** If the verse's gate is not PASS, output Sanskrit
   only. No literal, no gloss, no paraphrase — in any lane, any style, any
   chat answer. A model that can produce English must still withhold it.
5. **Add no facts.** Do not supply a cause, agent, or context the floors do
   not state. If the verse is elliptical, keep the ellipsis — short and
   gappy beats smooth and invented.
6. **Nothing downstream flows back.** Allegory, C2, chat answers,
   commentary never feed wording into the literal. The arrow runs
   Sanskrit → exact → story, never story → exact. A beautiful story
   phrase stays in the story.

## Resolve every image before writing a word

A gloss is not a meaning. *Guhāsu* glosses as "in-caves" — but caves of
what? Rock formations, or hearts? The literal must resolve each image
through the stack, in tiers, before rendering:

- **Tier 1 — the stack says it.** C1 essence, argmap premises, or L2 carry
  the referent. Render the referent confidently. (Crystal takes colors =
  the Lord holds all forms: the stack says so, keep both.)
- **Tier 2 — the stack is silent, background knowledge is stable.** A
  standard, uncontested reading exists (guhā = the heart-cave of
  Upaniṣadic/Trika use; Rāhu's eclipse). Render the referent *visibly*:
  "heart-caves" shows its work — image kept, resolution inside it. Never
  silently swap the image for the meaning.
- **Tier 3 — neither.** Keep the bare image. A strange cave beats a
  familiar lie. Never invent a referent to make the line comfortable.

Worked correction (paramarthasara v1): first draft wrote "You entered the
caves in many forms" — mechanically faithful, actually misleading
(English hears rock formations). C1 essence says "all-abiding"; Tier 2
background says heart-caves. Final: "You entered the heart-caves in many
forms." The compound carries both the Sanskrit and its referent.

## 80% rules (structural rules apply; lexical rules are direction of travel)

Resolve first, then write. The order matters: resolution chooses words,
rules shape sentences.

No official ASD dictionary is bundled here — same honest limit as the
community skills. Structural rules are enforced; word-choice rules are
"plainest word available, used the same way every time."

1. One idea in each sentence.
2. 20 words or fewer per sentence. Split above 25 when meaning permits.
   Never cut meaning to meet the count.
3. Active voice when the actor is known. Passive only when the verse does
   not name the actor.
4. Simple tenses. Keep a compound tense when it carries meaning (a hedge,
   current relevance) — and flag the departure.
5. Verbs, not nouns: "bow to Him", not "perform veneration of Him."
6. One name for each thing in the verse. Keep established terms; gloss an
   unfamiliar term once.
7. Plain words: use, start, before, because, to. No phrasal verbs (remove,
   not take off). No semicolons. No noun stacks over 3 words.
8. Keep every hedge at its strength. "May" stays "may". Upgrading a hedge
   to a fact is a different claim — the most common way a literal goes
   wrong, because short sentences tempt you to cut the qualifier.
9. Numbered lines for verse lines, in order. Do not reorder the verse to
   make the English flow.

## Scan checklist (mechanical — point at the exact word)

1. **Synonym rotation** — one thing, several names. Fix: one name.
2. **Hedge stacking or hedge dropping** — qualifiers piled until nothing is
   asserted, or cut until a guess reads as fact. Fix: state the claim at
   its real strength.
3. **Nominalization** — the action frozen into a noun. Fix: use the verb.
4. **Run-ons** — several ideas joined by commas, dashes, colons. Fix: one
   idea per sentence.
5. **Phrasal verbs and slang** — zero in literal. Fix: the single plain verb.
6. **Added connective tissue** — "because", "so", "therefore" the verse
   does not state. Fix: delete the connective; let the lines stand side
   by side.

## Output format

Default: the literal text alone, nothing else. No preamble about the skill,
no rule table, no closing offer. One line per verse line (translation) or
short sentences with citations (chat).

On request ("show the diff", "which rules"): a **Rule | Before | After**
table, then one line on anything deliberately not simplified and why.

## Worked example (bhairavastava §1, real stack)

Source: *vyāptacarācarabhāvaviśeṣaṃ cinmayam ekam anantam anādim
bhairavanātham anāthaśaraṇyaṃ tvanmayacittatayā hṛdi vande*

L1 (close, hyphen-chained): "pervading-the-particular-states-of-moving-
and-unmoving / consisting-of-consciousness / one / endless /
beginningless / Bhairava-Lord / of-helpless-refuge / by-mind-become-
Yours / in-heart / I-venerate"

Literal (this skill):

> He fills all moving and still things.
> He is consciousness only.
> He is one.
> He has no end.
> He has no beginning.
> He is Bhairava, the Lord.
> He shelters those with no shelter.
> My mind has become His.
> In my heart, I bow to Him.

Check: every L1 proposition survives (pervasion, consciousness, oneness,
endlessness, beginninglessness, lordship, refuge, mind-become-His,
heart-bow). *Viśeṣa* (particularity) rides in "all … things". No cause
added, no hedge to upgrade, no connective invented.

## Boundaries

**Will:** render plain English from L0/L1; keep every proposition, hedge,
and qualifier at its strength; refuse BLOCKED verses; show its work on
request.
**Will not:** claim ASD compliance or dictionary approval; smooth an
ellipsis into an invention; transliterate-and-leave; carry style or rasa
(that is C2's job); touch code, identifiers, or quoted text.
