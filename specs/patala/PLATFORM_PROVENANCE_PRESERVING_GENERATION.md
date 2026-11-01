# THE PLATFORM — PROVENANCE-PRESERVING GENERATION & VALIDATION AS FIRST-CLASS APIS

*2026-08-12. Frozen vision. FoJin's lesson: **grounding enforcement should be deterministic wherever
possible, and model judgment should only operate above that floor.** Pāṭala's leap: from "grounded
answers over texts" to **"grounded scholarly transformations over texts, with provenance-preserving
generation."** A dependency-aware scholarly publishing system — and a platform whose validation
primitives are first-class APIs any tool can call.*

---

## The shift

> "grounded answers over texts" → "**grounded scholarly transformations over texts, with
> provenance-preserving generation.**"

That is a materially stronger system.

---

## 1. Generalize FoJin's mechanisms

### Citation whitelist guard → CLAIM-SUPPORT GUARD
Don't just verify a cited passage exists. Verify each generated claim points to allowed support
objects:

```text
claim
→ passage
→ source span
→ C1 / decision / evidence
```

If a claim has no valid support path, either reject it or explicitly mark it as synthesis.

### Quote verifier → TRANSLATION-QUOTE VERIFIER
- Primary-text quotes: verify exact substring after normalization.
- Translated quotes: verify the quote exactly matches a registered target span/version.
- Prevents the model from fabricating "cleaner" quotations from your own edition.

### Citation correctness → RELATION CORRECTNESS
If the model says "This passage comments on IPK 1.5.11", verify the relation type exists:

```text
COMMENTARY_OF
ROOT_TEXT_CONTEXT
PARALLEL
```

If it only has `DOCTRINAL_PARALLEL`, the system must not let the prose upgrade that to direct
commentary.

### Eval regression → SCHOLARLY INVARIANT REGRESSION
Every build tests hard invariants, not just retrieval metrics:

```text
no target span without source span
no accepted decision without provenance
no quote without verified source
no C1 claim without local passage support or explicit inference label
no essay claim with dangling evidence
no silently changed published reading
```

A far more meaningful regression suite than generic RAG faithfulness.

---

## 2. Provenance-preserving derivation (the core innovation)

Every downstream artifact knows exactly what it depends on:

```text
L2 sentence
depends on: source spans · translation decisions

C1 paragraph
depends on: L2 passage · selected decisions · local context

Theme claim
depends on: C1-A · C1-B · C1-C

Essay claim
depends on: Theme-1 · passage-X · scholarship-Y

GUIDE sentence
depends on: C1 claim
```

If you revise a source reading, the system computes **what became stale**:

```text
CHANGE IMPACT

Translation decision MT-031 revised
↓ affects
C1 V2-L
Theme: Non-constructed I
Essay: Recognition and Subjectivity
Guide: What is the I?
Audio overview episode 4
Video script: Is the Self Constructed?
```

Pāṭala becomes not merely a corpus, but a **dependency-aware scholarly publishing system** — one of
the strongest things you can build that FoJin likely does not have.

---

## 3. Argument verification, not just citation verification

Use the argument maps. If an essay says "Abhinavagupta concludes X because A and B", the verifier
checks:

```text
Does argument map contain: A · B · A+B→X ?
```

Classify:
```text
DIRECTLY_LICENSED
REASONABLE_SYNTHESIS
UNLICENSED_INFERENCE
```

Much stronger than RAG faithfulness — it checks **inferential structure**, not semantic similarity.

**The C1 rule:** a C1 may paraphrase a local argument, but may **not strengthen its conclusion
beyond the mapped inference boundary**. (This directly prevents the V2-L problem.)

---

## 4. Negative retrieval (counter-evidence)

Normally RAG asks "what supports this claim?" For scholarship, also ask "**what evidence creates
tension with this claim?**" Every major theme/essay claim carries:

```text
SUPPORTING    passage A · passage B
QUALIFYING    passage C
CONTRADICTING passage D
OPEN          unresolved textual issue E
```

The model cannot generate a falsely smooth doctrinal synthesis. Expose:

> **What would falsify this reading?**

for every interpretive assertion — closer to scholarly adversarial review.

---

## 5. Translation disagreement mining

Once Pandey / Torella / Ratié / your version are aligned:

```text
source span → translation A · translation B · translation C
```

automatically detect divergence in:
```text
negation · agent/patient · technical term · referent · modality · causality · speaker · supplied content
```
Prioritize as cruxes. Not "who is right?" but **"where is interpretation happening?"** — a scholarly
discovery tool.

## 6. Term-drift detection

Across a work:
```text
vimarśa → rendering A 54x · rendering B 17x · rendering C 3x
```
Does contextual variation justify the drift? Even stronger signals:
```text
same Sanskrit phrase → different English rendering
different Sanskrit terms → collapsed into the same English term
```
Exactly the kinds of problems translators miss.

---

## 7. Explanation fidelity across depth levels (a novel QA task)

You have CRITICAL / C1 / GUIDE / GEN-Z. Verify transformations **vertically**. For each GUIDE claim:

```text
Does it preserve: polarity · agency · scope · modality · epistemic status · uncertainty ?
```

Example:
- Critical: "This passage does not by itself establish the universal Self."
- Bad GUIDE: "Abhinavagupta proves that your consciousness is the universal Self."
- System catches: **SCOPE_STRENGTHENING**.

Define a **semantic conservation test** across explanatory depth.

Allowed:
```text
simplify vocabulary · expand implicit context · add analogy · split sentences
```
Forbidden:
```text
strengthen claim · erase uncertainty · collapse distinction · invent causal relation · attribute synthesis to primary text
```
This makes "choose your depth" trustworthy.

---

## 8. Citation-preserving media generation

A video script isn't just a bibliography. Every scene/claim retains provenance:

```text
00:42–00:57
claim_id: CLM-123
supports: IPVV V2-L · C1 V2-L
```
The published video page exposes "Sources for this sentence." Same for audio. Rigorous public
scholarship.

## 9. Living essays

Not PDFs frozen forever. An essay is a graph-backed artifact:

```text
essay version 1.3
↓
claim 7 changed because translation decision MT-18 changed
↓
revision note
```
A reader inspects "What changed since v1.2?"

---

## 10. Scholarly coverage metrics (not gamified)

For a text:
```text
source coverage       100%
L2 coverage           100%
C1 coverage            42%
decision-audited       67%
context-linked         51%
external-reviewed       8%
```
For a concept:
```text
vimarśa
occurrences identified  112
sense-reviewed           76
C1-covered               44
cross-text linked        31
```
Tells you where the corpus is weak without pretending a single quality score.

---

## 11. The epistemic compiler

Like a compiler rejects invalid code, Pāṭala rejects:

```text
citation doesn't resolve
quote doesn't match
claim exceeds evidence
synthesis presented as quotation
reading lacks provenance
modern comparison presented as historical claim
```

> **Scholarship as typed transformations over evidence.**

Formalize claim "types":
```text
TextualClaim
InterpretiveClaim
ComparativeClaim
SyntheticClaim
HistoricalClaim
PedagogicalAnalogy
```
each with required evidence. For instance:
```text
HistoricalClaim     requires: primary source OR scholarship citation
InterpretiveClaim   requires: passage support + derivation note
ComparativeClaim    requires: support from both traditions
PedagogicalAnalogy  requires: explicit NON-LITERAL flag
```
Agents cannot silently blur categories.

---

## 12. THE STRATEGIC SHIFT — validation primitives as first-class APIs

> **Make validation primitives first-class APIs, not just internal checks.**

```text
/resolve
/verify-quote
/verify-claim
/verify-relation
/trace-dependency
/find-counterevidence
/compare-readings
/check-term-consistency
/check-depth-fidelity
```

Then every future agent, essay generator, tutor, audio generator, or external researcher uses the
same scholarly guardrails. **That is where the architecture becomes a platform rather than a single
product.**

---

## The deepest principle

One evidence graph, multiple controlled projections — and every projection is **verified against the
graph by deterministic primitives** before it is served. Grounding enforcement is deterministic
wherever possible; model judgment operates only above that floor.
