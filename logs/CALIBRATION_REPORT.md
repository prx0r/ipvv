# IPVV — calibration report: the layer lock, the findings, and the L2 proof

*2026-08-11. Editorial calibration pass over V3-B kārikās 1–7 (the dvitīyo vimarśa). Result: the
architecture survives; the layer *naming* was wrong. The artifact earlier called "L1 readable" is in
fact a **controlled literal rendering** (proposition-faithful, Sanskrit-close syntax) — excellent for
COMPARE/audit, NOT publishable book prose. This report locks the corrected stack, records the four
findings, and proves genuine L2 on two of the hardest paragraphs. T1 golden chunks untouched.*

---

## 1. The locked stack (corrected layer naming)

```
L0  STRUCTURED LITERAL    token/gloss records  (t1_extract.py → *.l0.jsonl)
L1  CONTROLLED TRANSLATION  proposition-faithful, close to Sanskrit syntax; for COMPARE / audit
L2  READ                    real book prose
A1  APPARATUS               material interpretive departures only
SL  SOURCE LAYER            speaker / objection / reply / quoted source
AQ  AUDIT QUEUE             actual research problems
C1  STUDY                   scholarly explanation
```

The earlier "pilot readable + apparatus" files are now classified as **L1 + A1 + SL + AQ** (a complete
controlled layer), NOT as READ. L2 is a separate, deliberate prose pass derived from L1 (never from
the golden chunks, and never overwriting them).

## 2. The four calibration findings

### 2.1 Readable English quality — the current L1 does NOT cross to book-grade
Read straight through as a book, the "readable" output is still a faithful but machine-translational
rendering. It preserves every proposition (a strength for the substrate) but keeps the gloss-syntax:
compounds and `-ness` nominalizations are not dissolved. Examples:

> "with the dealing-mere-param-essence-ness, of the object-distinction even, from its well-sayableness"
> "there is no computation there, because of the dense non-distinction, even of the one-ness, there,
>  from its non-being"

A reader who knows philosophy but not Sanskrit would have to reverse-engineer the syntax. **This is
not the READ view.** The fix is a distinct L2 pass (below), not cosmetic polishing of L1.

### 2.2 Apparatus precision — the entry criterion was too loose
Of the 19 A1 entries, ~2 are noise: B1-008 ("SOV→SVO; proposition preserved") narrates word-order,
not interpretation; B1-012 ("nīla = stock example") is trivia. **The correct entry criterion is:**

> Would removing this transformation potentially alter what a competent reader thinks Abhinavagupta
> is claiming?

If no → no apparatus entry. So: SOV→SVO = NO; splitting a 70-word sentence = NO; supplying a subject
forced by context = usually NO (structural metadata, not apparatus); choosing "manifestation" over
"illumination" for prakāśa = YES if materially relevant; identifying an implied opponent = YES
(APPARATUS / SOURCE-LAYER); expanding a compressed causal relation = YES.

### 2.3 Audit recall — the queue missed non-grammatical opacity
The 6-item queue caught the lexical cruxes but missed three real reader-stalls:
- the **camasa…ṣoḍaśin** Śrauta quotation (an opaque *external-knowledge* fragment);
- the **māṣaka-rakitikā** gold-weight measure (technical realia);
- the dense **anvaya-vyatireka** inference block (S7).
**Lesson: audit risk is not only grammatical/lexical ambiguity. Sometimes a sentence is opaque because
it presupposes an external knowledge system.** Extend AQ with at least:

```
UNRESOLVED_QUOTATION   (quoted fragment not resolvable to a source)
INFERENCE_BLOCK        (dense formal-inference prose)
SOURCE_LAYER_UNCERTAIN (voice/attribution unclear)
TECHNICAL_MEASURE_OR_REALIA  (weights, measures, ritual instruments, etc.)
```

### 2.4 Source-layer accuracy — right in outline, one boundary to verify
Objection/reply/Vṛtti/IPVV boundaries are sound throughout. The one spot to verify against the raw
source is S5's "he investigates whether…" (Abhinava's meta-commentary vs. the commentary proper);
the long nanu/reply runs inside single lines need a voice-audit. Not a systematic failure.

---

## 3. L2 production rules (frozen)

Given L1 + the source line, produce L2 (READ prose) with these constraints:
- preserve every proposition of L1;
- add no new doctrinal content;
- dissolve artificial `-ness` constructions;
- unpack Sanskrit compounds into ordinary philosophical English;
- break impossible sentences where needed;
- recover explicit subjects/referents only when supported by context;
- preserve objection/reply structure;
- any meaningful clarification not recoverable directly from L1/source becomes `SUPPLIED` and enters A1;
- never silently "improve" an unclear argument into one that makes more sense.

**Every L2 sentence carries a link to the L1 span(s) it derives from** (L1 IDs → L0 records →
Sanskrit), so radical readability never sacrifices auditability.

## 4. The two L2 proof samples (difficult paragraphs)

Full L2 renderings are in the companion file `pilot_V3B_L2_proof.md`, with proposition-by-proposition
comparison against L1 and the A1/AQ deltas. Summary of the style target:

**S7 (the anvaya-vyatireka inference block).** L1 keeps the scholastic compression:
> "of the two, the blue, that which is not manifesting while the anvaya and vyatireka both exist,
>  simultaneous with the manifestation, that very one is the cognition-cause…"

L2 re-expresses the same claim as readable inference prose — e.g. that of the blue's presence and
absence, only what is manifest at the same time as the perception and tracks that presence/absence is
its cognitive cause — while a `SUPPLIED` note records the compressed causal relation that was unpacked.

**S9 (the dāntava/līvarda / cow-bull passage).** L1 is opaque because it presupposes an agrarian-lexicon
knowledge system:
> "For with the 'dāntava'-'līvarda'-and-the-rest words alone the Ārya-worldly [people] declare the
>  bulls; but with the 'cow'-word the female-cows alone…"

L2 keeps the point (some words pick out the male class, 'cow' the female) while flagging the two
lexemes as `TECHNICAL_MEASURE_OR_REALIA` / `UNRESOLVED_QUOTATION` in AQ — it does NOT invent their
meaning. This is the correct behavior: preserve the argument, surface the external-knowledge gap.

## 5. Gate for scaling L2

Scale L2 only when a sample "feels like something you would genuinely sit down and read for an hour."
Until then, iterate on style within the rules above. The per-chunk QA scaler (after approval) must
track **two failure modes separately**:

```
FIDELITY QA   lost proposition / added proposition / changed polarity / changed speaker /
              unresolved referent
PROSE QA      literalism / -ness density / left-branching compound leakage / sentence overload /
              unclear antecedent / repetition
```

This stops the model from "fixing readability" by quietly damaging the philosophy.
