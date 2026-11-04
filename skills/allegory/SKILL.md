---
name: allegory
description: "Render a verse or song as story that carries doctrine — upgraded eli5, parable, or myth mode. Use when asked for allegory, parable, myth, story-explanation, or a C2 in story voice. Every symbol maps to a stated proposition; the analogy's limit is stated; no new doctrine. Grounded on L2 + C1 essence + rasa. Not a translation, not a commentary."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [allegory, parable, myth, eli5, c2, story, transmission, svread]
    related_skills: [render-c2, literal, c2-voice-corpus, write-commentary]
    checkpoint: CP4 (grounded story only — nothing unvetted enters a lane)
---

# Allegory — doctrine carried by story

## Purpose

Some propositions do not stick as propositions. *"Slow and steady wins the
race" alone on a blank page has no depth — it is the tortoise and the hare
that give the punchline meaning.* The story is what the memory keeps. This
skill renders a verse or song as a story that carries the doctrine: the
reader keeps the story, and the story keeps the claim.

Three modes, one grounding. Pick by the verse, not by taste:

- **eli5** (upgraded prose): the argument retold plainly, one honest analogy,
  its limit stated. For frame verses and summaries.
- **parable**: a short human scene that runs parallel to the doctrine. For
  verses about the seeker, practice, bondage, grace. Human characters, tacit
  analogy, stated at the end.
- **myth**: the tradition's own cosmic images worked at full size. For verses
  about the Lord, manifestation, recognition. Never invent cosmology — work
  the images the text gives (crystal, mirror, moon, egg, wheel).

Why myth belongs here: philosophy already teaches by story (Cave, Chariot,
Myth of Er), and Trika speaks in mythic images itself. Allegory does not
import foreign material. It works the tradition's own images until they
carry.

## What the community proved (borrowed, MIT, credited)

- **One analogy, and its limit** (`mblode/agent-skills/eli5`): use an analogy
  only when it clarifies the mechanism; say where it breaks. A limit stated
  is what keeps allegory honest.
- **Separate source from speculation** (`companion-inc/feynman/eli5`): one
  good analogy beats several weak ones; mark what the verse shows versus
  what the story adds. Shape: summary → idea → how → why it matters →
  what to be skeptical of → three things to keep.
- **Packaging, never facts** (`rcosteira79/eli5`): simplify the wrapping,
  never the claim. Walk, don't sprint — one new idea per step. End with
  2–3 deeper branches so nothing is lost, just not all now.
- **Mechanism before name; say when it won't simplify**
  (`guicortei/feynman-technique`): explain the working first, name it
  after. Ladder from kitchen-table to specialist. Some verses do not
  simplify — say so rather than fake a story.

## Grounding — every symbol maps to a proposition

A story without a map is decoration. Every allegory ships its map:

1. **Map table.** Each story element points at the L2 proposition or C1
   essence index it carries. Same discipline as C2 `paragraphs[].maps_to`:
   story paragraphs map to essence indices, so the render stays
   pipeline-compatible with `data/*.c2.json`.
2. **Work the text's images first.** If the verse already gives an image
   (crystal taking colors, face in a mirror, moon on water), the story
   extends *that image* — never a shinier invented one. The text's image
   is already authorized; yours is not.
3. **The Sanskrit is the world-building.** Collect the song's whole
   image-set first (song 1: caves, wheel, egg, crystal, moon-water, Rāhu,
   mirror) — that set IS the story's furniture. A parable or myth built
   from the verse's own images needs no imports and smuggles nothing in.
   Reach outside the set only for the frame (a ferryman, a flood), never
   for the doctrine.
3. **No new doctrine.** The story may not assert what the verse does not:
   no new cosmology in myth mode, no new morals in parable mode, no new
   causes in eli5 mode. When the verse is silent, the story is silent.
4. **Limit stated, in the open.** One line naming where the analogy breaks.
   (The crystal is passive; the Lord is not. The mirror needs no grace;
   the mind does.) The limit is part of the render, not a footnote.
5. **Rasa carried.** Name the verse's rasa (C1) and let the story land it:
   refuge, wonder, settled peace — the reader must *feel* the arrival,
   not just parse it.
6. **BLOCKED refuses.** No story for unpassed verses. Sanskrit only.

## Output format

Default: the story (2–8 short paragraphs), then the map, then the limit.
No preamble about the skill.

```
<story, mode-appropriate voice>

MAP
- <story element> → <proposition / essence index>
- ...

LIMIT
<where the analogy breaks, one line>

BRANCHES (eli5 mode only)
<2–3 deeper things to read next>
```

## Worked example (paramarthasara song 1, essence-led, parable mode)

Essence: refuge in all-abiding Śambhu; whirled student asks, teacher
answers; fourfold egg by power-weight; embodied enjoyer is Śiva fettered;
Lord holds forms as crystal takes colors; self moves with world-mass as
moon with water; everywhere-self shows in mind-mirror; grace-pure mind
mirrors the light-formed self.

> A man caught in a flood clings to a rock and shouts for the ferryman.
> The ferryman does not throw him a new river. He calls back across the
> water, telling him what holds him already.
>
> The rock is not one stone but four ledges, laid by the same hand that
> laid the river. The man on the ledge is the ferryman's own brother,
> holding on so tight he has forgotten his name.
>
> A clear stone takes the color of whatever cloth it rests on — red cloth,
> red stone — yet the stone never changes. So the brother on the ledge:
> god on festival days, beast on hungry days, and the stone underneath
> unaltered throughout.
>
> The moon rides the river. When the water runs, the moon runs; when the
> water stills, the moon stills — yet the moon never entered the water.
> So the man moves with the flood and mistakes the moving for himself.
>
> There is a dark shape that crosses the moon some nights and is seen only
> because the moon is bright behind it. So the man knows himself only
> where things strike his mind — the brightness is his, the shapes are
> visitors.
>
> Wipe a mirror and a face appears in it. The face was never absent; the
> dirt was. The wiping is not the man's work. Rain does it — what the
> verses call grace descending. What remains is light, shaped as seeing,
> knowing, doing: the brother remembering his name.

MAP
- flood / rock / ferryman → v1–v3: sorrow-wheel, refuge in Śambhu, the
  teacher answering in verses [essence 0]
- four ledges, one hand → v4: fourfold egg by power-weight [essence 1]
- brother who forgot his name → v5: embodied enjoyer is Śiva fettered
  [essence 1]
- clear stone on colored cloth → v6: crystal takes colors, Lord holds all
  forms [essence 2]
- moon on running/still water → v7: self moves/rests with world-mass
  [essence 2]
- dark shape seen by moonlight → v8: everywhere-self shows in mind-mirror
  by resorting to objects [essence 3]
- wiped mirror, rain, remembered name → v9–v10: grace-pure mind mirrors
  the light-formed self, will-knowing-acting replete [essence 3]

LIMIT
The ferryman and the brother are two men; the Lord and the fettered one
are not two. The story borrows separateness to show identity — do not
keep the separateness after the showing.

## Boundaries

**Will:** carry doctrine in story; map every symbol; state the limit;
ladder from plain to specialist; refuse what will not simplify.
**Will not:** invent cosmology, morals, or causes; keep the separateness
after the showing; mix registers (parables stay human, myths stay cosmic);
certify anything — story is MACHINE_DRAFT until a human promotes it.
