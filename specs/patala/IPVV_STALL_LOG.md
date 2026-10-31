# IPVV — Stall log (straight-through read, F-pass)

*Use this to record every point where the L2 READ stops you. Each stall becomes a **fixture** for the
QA scaler, so the scaler can search the rest of the corpus for the same failure mode.*

## Stall entry template

| # | location | what confused / bothered me | type | severity |
|---|---|---|---|---|

*Provenance anchors:* each `location` should eventually carry the L2 paragraph id and L0 anchor
(`<chunk>:<L-line>:<T-token>` range), per the provenance layer (see `pilot_V2H_L2PROVENANCE.md`).
For Vol 1, the L2 files don't all have provenance files yet; `location` (chunk + ¶ + line) is the
primary key, and anchors are backfilled once provenance is generated. Record the anchor when available.
| ... | | | | |

## Type tags

- **prose** — the English itself is clunky / broken / machine-translational
- **argument** — the logic doesn't follow; I can't see the inference
  - `MISSING_PREMISE` — the conclusion needs a premise that isn't stated
  - `HIDDEN_REDUCTIO` — a reductio whose absurd-branch isn't visible
  - `UNSTATED_PARTITION` — an exhaustive division is assumed, not argued
  - `LOGIC_INVERSION` — a direction/polarity seems flipped or swapped
  - `REFERENT_DEPENDENCY` — the step needs an unstated doctrine/context to work
  - `INFERENCE_TOO_COMPRESSED` — the words are clear but the inference jumps
- **term** — a technical term appears undefined or inconsistent with the ledger
- **speaker** — I can't tell if it's Abhinava / an objector / a quoted source / Utpaladeva
- **source** — I can't tell what Sanskrit this sentence rests on (provenance gap)
- **technical** — realia / measure / name / quotation I don't recognize
- **polarity** — a negation or direction seems to have flipped (dangerous)
- **FILE_ARTIFACT** — a deterministic formatting/paste corruption (regex-detectable), NOT a
  translation issue. Subtypes: literal `EOF`; heredoc/shell remnants; echoed line-count text. This
  class is caught and cleaned globally by regex; it never belongs in the semantic QA bucket.

## Severity

- **high (S3)** — probably wrong, or cannot responsibly understand; needs correction / apparatus now
- **medium (S2)** — interrupts understanding; needs a note or second look
- **low (S1)** — annoying but intelligible; flag but don't fix yet

## Logged stalls — Volume 1 (F1 pass, 2026-08-11)

| # | location | stall | type (subtag) | severity |
|---|---|---|---|---|
| 1 | V1A ¶3 (L27–31) | time-objection: the leap "no independent time" → "time = the sun's movement" is compressed; the blue-as-yellow analogy helps but the transition isn't explicit | argument (`INFERENCE_TOO_COMPRESSED`) | S1 |
| 2 | V1B ¶5 (L39–40) | "The door is not narrow in the way of the world's ranks; it is narrow only in the way of the heart" — the *door* image is introduced with no antecedent; I follow the dāsya point but the metaphor is orphaned | argument (`REFERENT_DEPENDENCY`) | S1 |
| 3 | V1C ¶2 (L20–24) | the inert's being/non-being reductio is a jumble of quick alternatives ("if it were not, nothing would suffer; if it did its effect, so what; if it shone, what is its own glory?") — I can't see which alternative refutes what | argument (`HIDDEN_REDUCTIO`) | S2 |
| 4 | V1C ¶2 (L23) | "by the perceiver it shines' is a new-fangled reason that would make the white make the yellow white" — inverts the earlier blue/yellow example without saying so | argument (`LOGIC_INVERSION`) | S1 |
| 5 | V1D ¶2 (L25–30) | "the tint of the prior body is distinct from the tint of this body — so the memory-ness, if pinned to the body, would not be clear" — logic seems inverted (a shared tint would *help* memory) | argument (`LOGIC_INVERSION`) | S2 |
| 6 | V1E ¶3 (L22–28) | tension: the pramāṇa "makes a new attainment" for inert objects but the self "has nothing un-attained" — yet the recognition is said to "foreground," which itself seems like a new attainment | argument (`MISSING_PREMISE`) | S2 |
| 7 | V1F ¶3 (L31–32) | "the self is the seer, and the seer is never not seen, for he is the seeing" — asserts rather than argues; aphoristic | argument (`INFERENCE_TOO_COMPRESSED`) | S1 |
| 8 | V1G ¶3 (L38–42) | "the covered thing could not bear another's support" — requires an unstated doctrine (a thing in place must be supported; self-manifest can't be covered) | argument (`REFERENT_DEPENDENCY`) | S2 |
| 9 | V1G ¶4 (L46–47) | "the Sāṃkhya's buddhi" appears with no introduction of what buddhi is | term | S1 |
| 10 | V1H ¶1 (L17–25) | "if it were [metaphorical], then by the infinite division of knowers, the same body could be dealt with at once as fire and water" — why a *metaphorical* enjoyment-account yields contradictory predicates is unstated | argument (`MISSING_PREMISE`) | S2 |
| 11 | V1H ¶3 (L34–36) | "if the conjunction's beginning is not found in the prior dissolutions, then the conjunction, being beginningless, is not distinct from the inherence" — follows only at word level | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 12 | V1I ¶1 (L12–14) | "the action of a body is just the coming-to-be of this or that place; it is not some hidden cause moving it; and it is not one — for order does not belong to a single thing" — the target is asserted, not argued | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 13 | V1J ¶2 (L20–22) | "the established does not expect another — a thing already complete does not reach out for a relation — and the dependence a relation imposes is unfitting" — bearing on *why the relation is absent* unclear | argument (`MISSING_PREMISE`) | S2 |
| 14 | V1K ¶2 (L23–25) | "if the construction, the determination, were all error — then every determination would fall, and the dealing of the world would collapse" — the premise (dealing rests on determination) is unstated | argument (`MISSING_PREMISE`) | S2 |
| 15 | V1L ¶3 (L34–38) | "he experienced, I have experienced" — seems to *assume* the unity at issue (the objection posits separate streams); a compressed reductio | argument (`HIDDEN_REDUCTIO`) | S2 |
| 16 | V1M ¶2 (L24–32) | the two-sided failure of the determination — each side follows, but the *exhaustiveness* of the partition is asserted | argument (`UNSTATED_PARTITION`) | S2 |
| 17 | V1N ¶3 (L30–34) | "by the co-reference (sāmānādhikaraṇya), by the following-ness (anugāmitvena)" — technical grammar terms unglossed | term | S1 |
| 18 | V1H–N (7 files) | literal `EOF` and `echo "V1x L2: … lines"` lines at end of each file (H,I,J,K,L,M,N) | FILE_ARTIFACT (`heredoc-remnant`) | S2 |

## Vol-1 subtag tally (17 content stalls)
- `INFERENCE_TOO_COMPRESSED` ×4 · `MISSING_PREMISE` ×4 · `LOGIC_INVERSION` ×2 · `HIDDEN_REDUCTIO` ×2 ·
  `REFERENT_DEPENDENCY` ×2 · `UNSTATED_PARTITION` ×1 · term ×2

## Notes for the scaler (from this pass)

1. **Argument stalls dominate (11 of 17 content-stalls).** The prose is generally fine; the systematic
   weakness is *compressed inference* — a conclusion asserted, a partition assumed, a reductio hidden.
   This is the single most useful fixture class.
2. **A real defect class exists: paste artifacts.** 7/14 Vol-1 L2 files have literal `EOF`/`echo`
   lines. The scaler should detect `^EOF$` / `echo "V.*lines"` / trailing shell-heredoc remnants as an
   `artifact` type, corpus-wide.
3. **Term-introduction drift (V1G buddhi, V1N sāmānādhikaraṇya):** technical terms appear unglossed.
   The scaler should flag terms that appear in the L2 but are not defined at first occurrence.
4. **The "known" daśaradana issue** is already recorded in the mining dossier (V3-O); it is a
   `technical` high-severity fixture (ten-faced → ten-tusked).

## Rule (unchanged)
Do **not** fix the L2 during the read. Just log. This pass logged 18 stalls (17 content + 1 artifact
class). After ~20–30 more across Vols 2–3, build the scaler skeleton against these as gold fixtures.

## Logged stalls — Volume 2 (F-pass, 2026-08-11)

| # | location | stall | type (subtag) | severity |
|---|---|---|---|---|
| 19 | V2-A ¶2 (L22–23) | "Even the yogin's knowledge of another … is the one awareness continuing" — the yogin case is brought in to support memory's nature, but the connective is unstated | argument (`MISSING_PREMISE`) | S2 |
| 20 | V2-A ¶4 (L38–40) | "As long as the awareness is not touched by time, there is no time-dealing; but when it manifests the jar in its past, present, and future, time appears" — first clause seems to say the opposite of what one expects | argument (`LOGIC_INVERSION`) | S1 |
| 21 | V2-B ¶2 (L23–27) | "time is the order of appearing/not-appearing … the yogin thins the body — and then the other's cognition shines" — how thinning the body removes time-order so the other's cognition shines is a jump | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 22 | V2-D ¶3 (L26–31) | the reflection-inference (blue-form is a reflection → external ground) — seems to contradict V2-C's "the awareness has nothing over against it"; the reconciling premise is missing | argument (`MISSING_PREMISE`) | S2 |
| 23 | V2-E ¶3 (L24–29) | "even this determination, though error, is by its bond to the thing a valid means — 'even the error, being a relation, is a pramā'" — error→valid-means is compressed; compounds the V2-D reflection tension | argument (`MISSING_PREMISE`) | S2 |
| 24 | V2-F ¶2 (L22–28) | the cow/speckled point — I follow the example but not how it licenses the conclusion about "being-gone-to-the-other" (grammar logic does unstated work) | argument (`REFERENT_DEPENDENCY`) | S2 |
| 25 | V2-F ¶4 (L39–43) | "from this follows the refutation of the external (whole or atoms)" — the refutation is *announced*, not shown (it's deferred to V2-G); a cross-chunk coherence gap | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 26 | V2-G ¶2 (L17–21) | the objector's question ("you established the external by the appearance-order; how un-established now?") is posed but the answer is not really given; the pivot to īśvarādvaya doesn't resolve the self-contradiction | argument (`MISSING_PREMISE`) | S2 |
| 27 | V2-H ¶2 (L25–30) | "the re-reflection cannot be only by difference of knower/known — for then swiftness fails … What is and is not separate must be non-separate" — the syllogism's terms aren't shown | argument (`MISSING_PREMISE`) | S2 |
| 28 | V2-I ¶3 (L28–37) | a string of six conclusions (sphurattā, jñeyīkaraṇa, ahantā/idantā, vimarśaśakti, sākṣātkāra) with almost no connective argument — the most compressed paragraph so far | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 29 | V2-J ¶3 (L29–36) | "the determination is beyond name-and-form, the param-Lord's power" — asserted strongly; the why (and the vācya-vācaka/sphoṭa failure) is gestured at, not shown | argument (`INFERENCE_TOO_COMPRESSED`) | S1 |
| 30 | V2-K ¶2 (L22–27) | "If the manifested were not re-recollected, its being-manifested would be impossible … calling it by another similar word would run into the infinite regress" — dense | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 31 | V2-M ¶1 (L10–20) | the descent ordering (space/wind/light/water/earth, "less inert") — the metric for the order is unstated; the elephant-in-mud image carries it | argument (`INFERENCE_TOO_COMPRESSED`) | S1 |
| 32 | V2-M ¶1 (L20) | "puryaṣṭaka (the inner city)" — glossed, but appears 3× before I absorb it | term | S1 |
| 33 | V2-N ¶3 (L31–38) | "creation by unity … knower-distinction not destroyed … appearance is the cognition" — a compressed cluster of three theses run together | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 34 | V2-N ¶2 (L24–26) | the mantreśvara sentence is overloaded (dīkṣā-vow-japa-tapas-concentration-conduct + transmigrating); the point (remain all-knowing) is hard to hold | prose | S1 |
| 35 | V2-P ¶1 (L13–17) | "the five objects … joined by the freedom-wave … the one appearance is the cause-and-effect appearance" — vivid but the mechanism is compressed | argument (`INFERENCE_TOO_COMPRESSED`) | S1 |
| 36 | V2-P ¶1 (L18–19) | "the Mukuta-saṃhitā says" — unfamiliar source name dropped unglossed | term | S1 |
| 37 | V2-Q ¶4 (L31–36) | the piśāca-invisibility vs jar-visibility negation — "every negation culminates in the identity-negation" doesn't obviously resolve the distinction; premise unstated | argument (`MISSING_PREMISE`) | S2 |
| 38 | V2-Q ¶3 (L40) | "arvāgdarśana" appears unglossed (the earlier "arvāk" was glossed) | term | S1 |
| 39 | V2-R ¶2 (L18–25) | the doubt ("what causes the variety") and the answer ("appearances have their own dependence") — the answer restates the phenomenon rather than explains its cause | argument (`MISSING_PREMISE`) | S2 |
| 40 | V2-S ¶3 (L25–30) | the objection ("each cognition rests in its own joining") and the answer (the known's param-essence is manifestation) — the answer doesn't address the objection | argument (`MISSING_PREMISE`) | S2 |
| 41 | V2-S ¶5 (L38–42) | kārikā 11's "fixed (niyata) reflexive-awareness-ness" — what "fixed" adds is asserted, not explained | argument (`INFERENCE_TOO_COMPRESSED`) | S1 |
| 42 | V2-E…S (15 files) | literal `EOF` / `echo "V2x L2: … lines"` at end of each heredoc-written file | FILE_ARTIFACT (`heredoc-remnant`) | S2 |

## Vol-2 subtag tally (23 content stalls)
- `INFERENCE_TOO_COMPRESSED` ×9 · `MISSING_PREMISE` ×8 · `LOGIC_INVERSION` ×1 · `REFERENT_DEPENDENCY`
  ×1 · term ×4

## Cumulative (Vols 1–2): 40 content stalls + 22 FILE_ARTIFACT files
- Vol 1: 17 content (4 × TOO_COMPRESSED, 4 × MISSING_PREMISE, 2 × LOGIC_INVERSION, 2 × HIDDEN_REDUCTIO,
  2 × REFERENT_DEPENDENCY, 1 × UNSTATED_PARTITION, 2 × term) + 7 artifact files
- Vol 2: 23 content (9 × TOO_COMPRESSED, 8 × MISSING_PREMISE, 1 × LOGIC_INVERSION, 1 ×
  REFERENT_DEPENDENCY, 4 × term) + 15 artifact files
- **40 content stalls total** — at the target threshold. Dominant pattern confirmed corpus-wide:
  **compressed inference** (`INFERENCE_TOO_COMPRESSED` + `MISSING_PREMISE` = 25/40 = 63% of content
  stalls). The Vol-1 "quirk" is the main global failure mode.
- **FILE_ARTIFACT is deterministic and regex-detectable** in 22/33 L2 files (7 Vol 1 + 15 Vol 2).

## Logged stalls — Volume 3 (F-pass, 2026-08-11, BLIND)

| # | location | stall | type (subtag) | severity |
|---|---|---|---|---|
| 43 | V3-A ¶2 (L24–25) | "it is precisely because it is one and un-divided that it can show sequence at all" — the leap from oneness to capacity-for-sequence is asserted, not argued; the mirror image carries it | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 44 | V3-A ¶5 (L51–53) | "the knowledge-power is the capacity to reveal; but the reflexive-awareness-power is, in truth, the action" — why vimarśaśakti = kriyā is asserted, not shown | argument (`MISSING_PREMISE`) | S2 |
| 45 | V3-B-K6 ¶6 (L48–49) | "Even separateness is the same: … the appearance of difference whose middle is the un-difference internally conjectured" — the sentence is nearly unintelligible as English | prose | S2 |
| 46 | V3-B-S7 ¶10 (L70–76) | the two-horn exclusion of the double-moon — the exhaustiveness of "either manifest or not" is assumed, and which horn wins is not clearly tied to the prior argument | argument (`UNSTATED_PARTITION`) | S2 |
| 47 | V3-B-S9 ¶5 (L37–43) | "If you remove both the manifestation and the use … on either horn, the conventional-true holds" — the two horns are asserted but their mutual exclusivity + why both favor Abhinava is compressed | argument (`UNSTATED_PARTITION`) | S2 |
| 48 | V3-C ¶5 (L47–57) | "the proof that the fruit is the reflexive-awareness is that the operation is the fruit … and the operation is non-different from the agent being operated" — the means/fruit/operation syllogism's terms are not shown | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 49 | V3-D ¶5 (L45–53) | the fire's heat vs. fuel/smoke dependence, then "established by the one valid means … the glance of the determinative power (niyati)" — the niyati term does unstated work | argument (`REFERENT_DEPENDENCY`) | S2 |
| 50 | V3-E ¶3 (L24–30) | "the distinction is not made by the pramāṇa's being un-contradicted, but by the reflexive-awareness' being un-contradicted" — the shift pramāṇābādhā→vimarśābādhā is asserted; the premise is missing | argument (`MISSING_PREMISE`) | S2 |
| 51 | V3-E ¶4 (L38–48) | the shell-silver: "the reflexive-awareness that posits it is uprooted … by the non-agreement of this place" — the mechanism (why non-agreement uproots) is stated, not argued | argument (`MISSING_PREMISE`) | S2 |
| 52 | V3-F ¶4 (L34–43) | "the prāṇa's being felt as 'I' is nothing other than the supreme self's own free manifestation" — the identity is asserted; the reconciling premise (how the param-ātman can shine as prāṇa-I) is unstated | argument (`MISSING_PREMISE`) | S2 |
| 53 | V3-G ¶4 (L40–50) | the śiṃśapā/tree inference: "the genuine causal relation that requires two distinct things is absent … This is the basis of all inference" — the move from non-otherness to "basis of all inference" is a jump | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 54 | V3-H ¶2 (L15–27) | "That fire-appearance … is what we call the 'cause of the Lord' (adhipatipratyaya)" — the term is dropped unglossed and does the work of the inference | term | S1 |
| 55 | V3-H ¶3 (L28–35) | "the locative 'in fire [there is] heat' … is real, and it is supported by the one knower" — why the grammar-locative is real/synthesis-quickened is asserted, not argued | argument (`MISSING_PREMISE`) | S2 |
| 56 | V3-I ¶2 (L23–34) | the "ignorance is of whom?" turn — "even the revealed teaching too would be ignorance" — the reductio branches are stacked without the connectives between them | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 57 | V3-J ¶5 (L37–43) | "like a picture just unclosed (the pure group) or like the full painted picture (the Īśvara)" — the picture image for Sadāśiva-vs-Īśvara is opaque; the difference it points to is unclear | argument (`REFERENT_DEPENDENCY`) | S1 |
| 58 | V3-N ¶3 (L27–32) | "when consciousness contracts … there arises the un-cognition of its own complete form — and with that, the many persons" — the contraction→many-persons mechanism is asserted, not shown | argument (`INFERENCE_TOO_COMPRESSED`) | S2 |
| 59 | V3-O ¶3 (L26–31) | "the construction-action … is of the breath-form … and it exists precisely to obstruct the bound one's rest" — teleology ("exists to obstruct") asserted without premise | argument (`MISSING_PREMISE`) | S1 |
| 60 | V3-P ¶5 (L45–52) | the seventeen-verse lineage: "Haṭitalakṣmaṇagupta, the maker of the śāstra" — a run of proper names dropped without gloss; I follow the transmission point but the names are opaque | term | S1 |
