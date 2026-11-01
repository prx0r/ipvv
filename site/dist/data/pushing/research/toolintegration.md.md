The dev plan should now be **integration-first, product-shaped, and aggressively stop infrastructure creep**. `25ee670` already freezes the right S0.1→S0.4 sequence and the six-item hard stop.

I would make the execution plan below the authoritative one.

# S0 — Source Evidence Substrate

## S0.0 — Freeze the contract

Before touching more code, define one minimal end-to-end contract:

```text
RawSource
→ BibliographicRecord
→ Witness
→ SourceSpan
→ SourceAssertion
→ CorroborationEvent
→ downstream consumer
```

Pāṭala owns only:

```text
pt:source_id
pt:witness_id
pt:span_id
SourceAssertion
CorroborationEvent
resolver()
```

External systems own the rest where possible.

Acceptance criterion:

> replacing Zotero/GROBID/OpenAlex later must not invalidate Pāṭala IDs or epistemic objects.

---

# S0.1 — External-tool pilot

Use **5–10 deliberately ugly real sources**, not nice examples.

Recommended fixture set:

```text
A. clean born-digital Ratié article
B. Sanderson PDF with complex footnotes
C. same publication duplicated under another filename
D. preprint/final or reprint case
E. book/chapter
F. OCR-heavy source
G. publication without DOI
H. source with Sanskrit passages
I. source with figure/table
J. one French-language source
```

Run:

```text
PDF
↓
GROBID
↓
bibliographic metadata
↓
Zotero identity / external IDs
↓
Crossref/OpenAlex/OpenCitations enrichment
↓
pt:source_id
↓
pt:witness_id
↓
stable pt:span_id
```

### S0.1 tests

#### Identity test

Same publication imported twice:

```text
foo.pdf
copy-of-foo.pdf
```

Expected:

```text
same pt:source_id
different or duplicate witness relationship
```

Not two publications.

#### Rename test

```text
/path/a/ratie.pdf
→
/another/place/who-cares.pdf
```

Expected:

```text
pt:source_id unchanged
pt:witness_id unchanged if bytes unchanged
all span refs still resolve
```

This directly tests hard-stop criterion 6.

#### Extraction determinism

Same file + same GROBID version:

```text
→ same extraction witness hash
```

If GROBID changes:

```text
grobid@x
→ grobid@y
```

create a new derivation version rather than silently replacing old extraction.

#### External metadata disagreement

Inject:

```text
GROBID title = A
OpenAlex title = A'
Crossref title = A
```

Expected:

```text
metadata witnesses preserved
canonical decision deterministic
disagreement recorded
```

Never silently majority-vote metadata.

#### API failure

Simulate:

```text
OpenAlex 429
Crossref timeout
OpenCitations unavailable
```

Expected:

```text
local source ingest still succeeds
enrichment = PENDING / UNKNOWN
no canonical object lost
```

External enrichment must never be required for basic source identity.

---

# S0.2 — Missing semantics only

Now implement the two genuinely Pāṭala-native objects.

## `SourceAssertion`

Minimum:

```json
{
  "assertion_id": "...",
  "source_span_ref": "...",
  "attributed_to": "...",
  "proposition": "...",
  "commitment": "ASSERTS",
  "status": "MACHINE_PROPOSED",
  "derivation": {...}
}
```

Critical distinction:

```text
span exists
≠
paraphrase is faithful
≠
claim is true
```

Those must remain separate states.

## `CorroborationEvent`

```json
{
  "target_proposition_ref": "...",
  "source_assertion_ref": "...",
  "relation": "DIRECT_SUPPORT",
  "semantic_alignment": "...",
  "scope_alignment": "...",
  "independence": "...",
  "defeaters": []
}
```

Relations:

```text
DIRECT_SUPPORT
PARTIAL_SUPPORT
CONTRADICTION
ALTERNATIVE_READING
BACKGROUND_ONLY
NON_EQUIVALENT
```

### S0.2 tests

This is where adversarial testing matters.

#### Attribution trap

Scholar writes:

> “Some Naiyāyikas argue X, but this is mistaken.”

Machine extracts:

```text
Scholar ASSERTS X
```

Expected: **FAIL**.

Correct commitment:

```text
ATTRIBUTES_TO_OPPONENT
```

This test is mandatory.

#### Quotation laundering

Scholar quotes another scholar asserting X.

Expected:

```text
quoted_author ASSERTS X
current_author QUOTES / DISCUSSES X
```

not:

```text
current_author ASSERTS X
```

#### Scope mismatch

Pāṭala proposition:

```text
All cognition is reflexive.
```

Source:

```text
Certain cognitions are reflexive.
```

Expected:

```text
PARTIAL_SUPPORT / NON_EQUIVALENT
```

never `DIRECT_SUPPORT`.

#### Modality mismatch

```text
may → must
possible → necessary
often → always
```

must fail direct corroboration.

#### Negation

Classic:

```text
X
vs
not X
```

No lexical-overlap shortcut.

#### Empty evidence

No relevant passage exists.

Expected:

```text
UNDERDETERMINED
```

not nearest-neighbor support.

#### Multiple scholar disagreement

```text
Ratié → A
Sanderson → B
```

Expected:

```text
two CorroborationEvents
CONTESTED state
```

not a synthetic compromise.

---

# S0.2b — Lineage and independence

Keep this tiny.

Relations already frozen in the plan are sufficient:

```text
SAME_PUBLICATION
DERIVED_FROM
REPRINT_OF
PREPRINT_OF
EXCERPT_FROM
UNKNOWN
```

Testing should specifically prevent false multiplication.

Fixture:

```text
Sanderson paper
same paper as Academia PDF
same paper in collected volume
OCR text of same PDF
```

Expected:

```text
one intellectual source lineage
```

not four independent corroborators.

Then:

```text
Sanderson + Ratié independently support X
```

may count as multiple scholarly witnesses.

Do **not** turn this into numerical Bayesian scoring yet.

---

# S0.2c — Rights

Keep rights deliberately crude:

```text
KNOWN_OPEN
KNOWN_RESTRICTED
UNKNOWN
```

plus:

```text
license
source_url
redistributable
asset_reproduction_allowed
attribution
```

Test:

```text
rights UNKNOWN
```

must still allow:

```text
metadata
citation
private scholarly analysis
```

but block any downstream behavior requiring redistribution unless specifically allowed.

In other words:

```text
unknown rights
≠
source unusable
```

but:

```text
unknown rights
→
do not assume redistribution permission
```

---

# S0.3 — Product proof

This is the most important S0 stage because it stops the team treating the substrate itself as success.

Choose **one existing IPVV proposition**.

Build this exact vertical:

```text
IPVV Proposition P
        │
        ├── Primary evidence
        │     Sanskrit
        │     L0
        │     L2
        │     L200
        │     C1
        │
        └── Scholarly evidence
              Ratié/Sanderson/etc.
                 ↓
              SourceSpan
                 ↓
              SourceAssertion
                 ↓
            CorroborationEvent
```

Then prove the same identifiers work in five consumers.

### A. Bibliography

```text
resolve(pt:source:X)
→ formatted citation
```

Ideally delegated to Zotero/CSL.

### B. Scholar assistant

Prompt:

> Why is proposition P considered warranted?

Expected output assembled from:

```text
primary evidence
scholarly corroboration
counterevidence
status
unresolved cruxes
```

### C. Argument graph

The argument should resolve the same `CorroborationEvent`.

### D. Site

Claim card:

```text
Claim
Primary evidence
Scholarly evidence
Status
View exact sources
```

### E. Education

A lesson references the **same proposition and source IDs**, not duplicated text citations.

---

# S0.3 testing

## Resolver contract

For every consumer:

```text
resolve(id)
```

must return semantically identical canonical metadata.

No consumer-specific source copies.

## Dependency test

Change:

```text
SourceAssertion v1 → superseded by v2
```

Expected:

```text
CorroborationEvent depending on v1 becomes stale/review-required
```

and downstream product can discover that state.

This test is extremely valuable because it proves the substrate participates in the Pāṭala DAG rather than merely existing as bibliography.

## Broken-file test

Temporarily remove the PDF.

Expected:

```text
publication metadata still resolves
assertion metadata still resolves
witness availability changes
```

not total graph failure.

---

# S0 HARD STOP

Use the six criteria in `25ee670` literally.

S0 is finished when:

```text
1. PDF → stable publication identity               PASS
2. exact passage resolves reproducibly             PASS
3. passage → attributed SourceAssertion            PASS
4. assertion → support/oppose proposition          PASS
5. all products resolve same IDs                   PASS
6. path rename/move breaks nothing                 PASS
```

Then freeze this subsystem.

**Do not standardize 213 PDFs.**

---

# S0.4 / F1 — Corroboration capability experiment

Now the question becomes empirical:

> Can the system accurately map Pāṭala propositions to published scholarship?

Use the existing Argument Gold/Reference propositions, but keep evaluation separate from source construction.

I would make a small benchmark first:

```text
30–50 proposition/evidence pairs
```

balanced across:

```text
DIRECT_SUPPORT
PARTIAL_SUPPORT
CONTRADICTION
ALTERNATIVE_READING
BACKGROUND_ONLY
UNDERDETERMINED
```

Include hard negatives.

## Critical test split

Do not evaluate on the exact same examples used to tune prompts.

Use:

```text
development set
held-out test set
```

Even tiny is better than no separation.

## Primary F1 metrics

Not ordinary F1 alone.

Track:

```text
DIRECT_SUPPORT precision
false corroboration rate
contradiction precision
UNDERDETERMINED accuracy
evidence-span precision
attribution error rate
scope-error rate
```

Most important:

[
FalseCorroborationRate =
\frac{\text{unsupported claims labeled supported}}
{\text{all support labels}}
]

This should be very low.

For Pāṭala, I'd optimize:

```text
precision > coverage
```

A system that corroborates 40% safely is preferable to one that “finds support” for everything.

---

# Add the process benchmark immediately

This is the strongest idea from the guiding docs.

For each failed claim:

```text
SOURCE_EXISTS
↓
SPAN_SUPPORTS
↓
ATTRIBUTION_CORRECT
↓
SCOPE_MATCH
↓
WARRANT_SUPPORTED
↓
CONCLUSION_SUPPORTED
```

The benchmark label is the **first failing layer**.

Example:

```text
SOURCE_EXISTS          PASS
SPAN_SUPPORTS          PASS
ATTRIBUTION_CORRECT    PASS
SCOPE_MATCH            FAIL
WARRANT_SUPPORTED      N/A
CONCLUSION_SUPPORTED   FAIL
```

Then the benchmark doesn't just tell you:

```text
wrong
```

It tells you:

> **where epistemic conservation broke.**

That should eventually become the core TantraFact innovation.

---

# Testing hierarchy overall

I'd structure tests into five levels.

```text
T0 — UNIT
schemas, resolver, hash/ID behavior

T1 — CONTRACT
external adapter → canonical internal object

T2 — ADVERSARIAL
attribution, scope, quotation, negation, duplicates

T3 — VERTICAL
PDF → assertion → corroboration → product

T4 — BENCHMARK
held-out corroboration / TantraFact metrics
```

Never promote a capability because only T0/T1 pass.

---

# Suggested test tree

```text
source-evidence/
  tests/
    unit/
      test_ids.py
      test_resolver.py
      test_spans.py
      test_rights.py

    adapters/
      test_grobid.py
      test_zotero.py
      test_crossref.py
      test_openalex.py
      test_opencitations.py

    adversarial/
      test_attribution.py
      test_quotation.py
      test_scope.py
      test_modality.py
      test_negation.py
      test_lineage.py

    vertical/
      test_scholar_vertical.py
      test_rename_replay.py
      test_supersession.py

    benchmark/
      test_corroboration_benchmark.py
```

For public APIs, record/replay fixtures rather than hammering APIs in every test.

Tests should run offline by default.

Real integration/API tests can be opt-in:

```bash
pytest -m integration
```

This also avoids CI failures from rate limits.

---

# External-tool testing rule

Every integration must have **three modes**:

```text
LIVE
RECORDED
UNAVAILABLE
```

and Pāṭala must behave sensibly in all three.

Example:

```text
Crossref unavailable
```

must not crash source resolution.

Likewise OpenAlex.

GROBID failure should affect extraction but not erase already registered witnesses.

This makes external infrastructure truly replaceable.

---

# What I would build immediately

The next implementation sequence:

```text
1. source-evidence/adapters/grobid.py
2. source-evidence/adapters/zotero.py
3. source-evidence/adapters/crossref.py
4. source-evidence/adapters/openalex.py

5. source-evidence/resolver.py

6. SourceAssertion schema + validator
7. CorroborationEvent schema + validator

8. fixtures/ 5–10 ugly documents

9. test_scholar_vertical.py

10. one product proof
```

OpenCitations can come after the basic vertical because independence analysis is not needed to prove source→assertion.

RO-Crate, ORKG and OpenReview should remain deferred adapters during S0.

---

# Parallel relationship to Agent 2

One thing I would **not** do is block Agent 2's L0/L200 factory on S0.

They are separate foundational tracks:

```text
TRACK A — TEXT FACTORY
L0 certificate
→ L200 certificate
→ C1

TRACK B — SCHOLAR EVIDENCE
S0.1
→ S0.3
→ F1 corroboration
```

They converge later:

```text
PRIMARY TEXT
L0→L2→L200→C1
         \
          Proposition
         /
SCHOLARSHIP
Span→SourceAssertion
```

So both can progress independently.

---

## Definition of success

The test I care about most is one executable command eventually producing something like:

```text
$ patala explain PROP-IPVV-017
```

and resolving:

```text
PRIMARY BASIS
✓ IPVV Sanskrit span
✓ L2 reading
✓ L200 derivation

SCHOLARLY BASIS
✓ Ratié p. X — DIRECT_SUPPORT
✓ Sanderson p. Y — PARTIAL_SUPPORT

COUNTEREVIDENCE
✓ Torella p. Z — ALTERNATIVE_READING

STATUS
SCHOLARLY_CORROBORATED
REVIEW_STATUS: NOT_INDEPENDENTLY_REVIEWED

CRUX
scope of reflexivity claim
```

If the same graph powers the scholar assistant, benchmark, peer-review adversary, site and education layer, then S0 has done its job.

After that, stop building source infrastructure and move aggressively into the products.
