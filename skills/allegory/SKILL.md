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
- **Embodied, not explained** (`jwynia/paradox-fables`): let readers
  absorb truth sideways through story rather than argument; no moral
  speech inside; test by removing the doctrine — if the story still
  stands, it wasn't in it.
- **Analogy first, decode second** (parable scholarship): Nathan's sheep
  works by loose analogy, point first — don't decode every pebble; the
  three-point Gospel shape (authority + two contrasting responses, one
  lesson per character) is a ready frame. Zhuangzi's fables are the
  Eastern precedent: lodged words returning to principle.

## Grounding — every symbol maps to a proposition

A story without a map is decoration. Every allegory ships its map. But
map the hinge, not every pebble: the craft warns against decoding every
detail (the bad habit that turned the Good Samaritan into a codebook).
Map the load-bearing elements — the ones the doctrine stands on — and
let the rest be story furniture. Characters must be beings, not walking
allegories: a ferryman with no life of his own preaches instead of
carrying.

1. **Map table.** Each load-bearing story element points at the L2
   proposition or C1 essence index it carries. Same discipline as C2
   `paragraphs[].maps_to`: story paragraphs map to essence indices, so
   the render stays pipeline-compatible with `data/*.c2.json`.
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
4. **No new doctrine.** The story may not assert what the verse does not:
   no new cosmology in myth mode, no new morals in parable mode, no new
   causes in eli5 mode. When the verse is silent, the story is silent.
5. **Limit stated, in the open.** One line naming where the analogy breaks.
   (The crystal is passive; the Lord is not. The mirror needs no grace;
   the mind does.) The limit is part of the render, not a footnote.
6. **Rasa carried.** Name the verse's rasa (C1) and let the story land it:
   refuge, wonder, settled peace — the reader must *feel* the arrival,
   not just parse it.
7. **BLOCKED refuses.** No story for unpassed verses. Sanskrit only.
8. **Embodiment test** (borrowed from `jwynia/paradox-fables`, MIT: remove
   the doctrine — does the story collapse? If it still stands, the
   doctrine wasn't in it. And: no moral speech inside the story, ever.
   The map lives outside; the story never explains itself.

### Parable shapes (pick one per render — never force all three)

- **Three-point** (Gospel shape): an authority figure + two contrasting
  responses (two sons, two debtors, two builders). One lesson per
  character. Best for verses with a teaching and two ways of missing it.
- **Trap-and-turn** (Nathan's sheep): tell the story straight, invite the
  reader's judgment, then turn it — "you are the man." Best for
  recognition verses. Use sparingly; a turned reader trusted you.
- **Seed** (mustard/growing seed): the smallest image, automatic growth,
  "he knows not how." Best for grace verses — what ripens without effort.

### Parable diction (ordinary words only — the Jesus rule)

No doctrine words inside the story. Ever. No Māyā, no tanmātra, no
Sadāśiva, no śakti, no tattva — not even where the verse says them.
The tale uses only ordinary words: pool, cloth, ox, husk, household,
lamp, road. Every technical term lives in the map, never in the tale.
Read the Jesus parables for the vibes: concrete nouns, human-scale
scenes, one turn, end on the turn, never explain. The listener who
knows nothing must follow the whole story; the map is where the
knowing reader finds what each thing was.

### Exemplar shelf (study these, never copy them)

Prodigal Son (three characters, three lessons, ends unresolved on the
older brother — tension kept); Good Samaritan (enemy as hero; question
→ story → "go and do likewise"); Nathan's sheep (analogy that traps:
judge, then "you are the man"); Zhuangzi's butterfly (recognition
structure: which is the dream? — the Eastern precedent for philosophical
story, closer to Trika than Aesop); the Growing Seed (grace as
automaticity); Plato's Cave (our lineage: the story that replaces the
argument). Rule from the shelf: the story carries what argument cannot,
and the best ones end before explaining themselves.

## Output format

Default: the story (2–8 short paragraphs), then the map, then the limit.
No preamble about the skill. Then VISUALS: one vertical frame per beat.

**VISUALS — ONE canonical image per parable (Bob Ross rule).** New look,
new preset: `sleepdraw/lora2-inv.yaml` (inverse of lora2 — black ink on
white paper, vertical 9:16, sketched; locked lora files untouched).
One landscape per parable, rendered while the story is listened to:
the image holds the song's whole world at once (song 4: night fairground
under a vast clean sky, web between poles, row of jars). Image prompt:
"black ink on white paper, [the FINAL snapshot — freedom, not struggle: the story's end-state rendered luminously], hand-sketched linework, breathing white space, vertical 9:16." Rasa encoded in art: stillness as white space, luminosity as densest ink, release as upward motion. All greyscale.
No text in frame, no doctrine symbols, no captions — the landscape
carries the parable the way the parable carries the verse.

**VOICES + IMAGE PROMPTS (shorts container).** Writing and voicing are
separate layers. The parable text is third-person narrative, Jesus-shape
— no dialogue tags, no script formatting, no speakers in the text. Most
parables have no child in them at all.

- Production map ships per parable: GRANNY reads narration (and any
  elder/teacher speech inside the story); KID reads a child's speech
  only where the story has a child — usually silent. Two voices
  available, used as the story requires, never forced into it.
- The shorts container per parable: full narrative text + voice map
  (which lines GRANNY, which KID, if any) + ONE image prompt.
No text in frame, no doctrine symbols, no captions — the landscape
  carries the parable the way the parable carries the verse.
- Image review gate (owner's eye, check against the parable before
  accepting): is the setting the song's set? Is the subject placed
  where the story leaves it (above the web, not in it)? Does the
  composition read release, not capture? A beautiful wrong image is
  rejected like a beautiful wrong line.
- Same container serves roadman shorts: same beats, same frames,
  roadman voiceover on the roadman text instead.

**DELIVERY (tagged script for drama3).** Every parable ships a
performance script, not just a text. Direction comes from rasa,
mechanics from the house guide (`damn/docs/drama-syntax.md`):

- Tag immediately before what it affects; max 3 tags; one emotion per
  sentence. Sounds (`[pause]`, `[sigh]`, `[gasp]`) anywhere — pauses do
  the heaviest work: short pause after the setup, pause before the turn,
  long pause where the verse lands.
- Rasa sets the voice: karuṇa-śānta = low, calm, warm, slowly; wonder =
  lift, not volume; arrival = settle, never swell.
- Speaker turns (`<|speaker:0|>`) only where the story has two speakers;
  single-voice parables stay single-turn.
- Validate on paper before any render: `damn/fish/validate.py` ($0, no
  API calls). PASS = shippable; warnings get read, not ignored.
- Model: drama3 for these shorts (owner call — overrides damn's
  free-only law, which governs damn's channels, not this work).
- Voice chairs: GRANNY is LOCKED to Granny British
  (`614f8afd83f841048c040b2c1` — owner's ear pick 2026-11-04,
  "granny is the best"). KID stays open until the owner ear-checks
  a child's voice. Nothing else locks without the owner's ear.
  Never render on "give me a sample" — tagged text only, render on
  explicit yes.
  No audio generated by agents, ever — direction on paper only.

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

> A man caught in a flood clings to a rock and shouts for the ferryman —
> who has poled that river since before the man was born and knows every
> eddy by its first name.
>
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
> verses call grace. What remains is light, shaped as seeing, knowing,
> doing: the brother remembering his name.

MAP (hinge only — the rest is furniture that breathes)

- flood / rock / ferryman's call → refuge asked and answered [essence 0]
- four ledges, one hand → fourfold egg by power-weight [essence 1]
- brother who forgot his name → fettered Śiva [essence 1]
- clear stone on colored cloth → unstained forms [essence 2]
- moon on running/still water → co-motion with the mass [essence 2]
- dark shape seen by moonlight → known where objects strike [essence 3]
- wiped mirror, rain, remembered name → grace, replete self [essence 3]

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
