# SPEC — L0 / L1 (literal substrate + controlled translation)

*The second layer. L0 is the structured literal substrate (token + IAST + gloss); L1 is the
controlled, Sanskrit-close translation. Both sit under the readable L2 and above the audit L200.*

---

## 1. L0 — the literal substrate

Structured records, one per token/gloss, with full provenance:

```text
id            chunk:line:token
chunk_id      the T1 chunk
line_id       the source line
lemma_iast    the Sanskrit lemma (IAST)
literal_gloss the word-for-word English gloss
raw_fragment  the exact original inline expression (re-checkable)
source_text   the containing line
quoted        whether it is a verbatim quotation
status        PARSED / AMBIGUOUS / FAILED
```

Extracted by `translations/tools/t1_extract.py` into `*.l0.jsonl` (Vols 1–3 present).

**The parsing contract (t1_extract.py token grammar):**
```
[and]-GLOSS (IAST)        normal lemma+gloss
[and]-"GLOSS (IAST)"      quoted (verbatim pratīka / root-text quotation)
[and]-and                 bare supplied connective, no IAST
[and]-and (ca)            "and" with a lemma
```
Every record keeps `raw_fragment` = the exact original inline expression, so any later format error
re-checks against the untouched chunk. **The T1 chunks are immutable; L0 is a pure derivation.**

## 2. L1 — the controlled translation

A Sanskrit-close, proposition-faithful controlled translation — the intermediate between L0 and L2.
It is what the audit compares L2 against for fidelity.

The L1 pilot produces, per passage:
```
L1_READABLE    continuous idiomatic English preserving every proposition of the literal
A1_APPARATUS   structural TranslationApparatus entries — only where interpretation actually moved
SOURCE-LAYER   who speaks / what is commented on
AUDIT_QUEUE    open cruxes surfaced by the transform
```

## 3. The chain

```
L0 (literal, token-level)  →  L1 (controlled, Sanskrit-close)  →  L2 (readable)
```
L2 must be traceable to L1, L1 to L0, L0 to the Sanskrit source span. The L200 audit records that
trace (§2 derivation map).

---

## 4. EXEMPLARS — what it looks like in the IPVV

### L0 (structured literal)

`l0/chunkV3-C-kriya-trtiyo-k1-2.l0.jsonl` (4111 records) — one token/gloss per line. A real record:
```json
{"id": "chunkV3-C-kriya-trtiyo-k1-2:L34:T7", "chunk_id": "...V3-C...",
 "line_id": 34, "lemma_iast": "yad vaśāt", "literal_gloss": "through-whose-force",
 "raw_fragment": "[and]-through-whose-force (yad vaśāt)", "status": "PARSED"}
```
And the L0 report confirms the round-trip count matches (PARSED/AMBIGUOUS/FAILED per chunk) —
`l0/chunkV3-C-kriya-trtiyo-k1-2.l0.report.txt`.

### T1 (the immutable source of L0)

`02_t1/chunkV3-C-kriya-trtiyo-k1-2.md` — the hyper-literal glosses the L0 parses. Immutable.

### L1 + apparatus (controlled + source-layer + audit queue)

`pilot/pilot_V3B_k1_L1_apparatus.md` — the V3-B kārikā 1 pilot. It shows the full L1 pipeline:
- **Scope / discourse segments** (S1 root kārikā · S2 commentary · S3 "Caitra is walking" ← Ratié
  overlap · S4 quotation vi. bhai. 106 · S5 ābhāsamānataiva · S6 quotation · S7 nanu/reply · S8
  quotation 2.2.4 · S9 saṃvṛti/bhrānti) — source-layer segmentation in practice.
- **L1_READABLE** — the controlled translation per segment, proposition-preserving.
- **External benchmark**: Ratié, *Otherness in the Pratyabhijñā* (JIPh 2007) on the same
  "Caitra is walking" passage — used to test whether our transform preserves propositions and
  identifies the same cruxes, NOT as an authority to imitate.

`pilot/pilot_V3B_k2-7_L1_apparatus.md` — the continuation.

---

## 5. VALIDATION — how we know L0/L1 are correct

**L0 (deterministic — machine-verifiable):**
- [ ] round-trip reconstruction matches the T1 source (the extractor's count: PARSED + AMBIGUOUS +
      FAILED = total tokens; verified against the chunk)
- [ ] `raw_fragment` is preserved verbatim for every record (re-checkable against the immutable T1)
- [ ] every IAST lemma has a gloss; FAILED records are visible (not silently dropped)
- [ ] the extractor never edits the T1 (immutability enforced)

**L1 (controlled — proposition-fidelity):**
- [ ] every proposition of the L0/literal is preserved in the L1 (no lost/added content)
- [ ] the L1 is Sanskrit-close (not yet the free L2)
- [ ] the apparatus (A1) records every genuine interpretation-move as a structured entry; it does
      not claim an explanatory summary is a translation intervention (the SUPPLIED-vs-IA rule)
- [ ] source-layer segmentation (S1..Sn) is complete: speaker/commentary/quotation are tagged
- [ ] open cruxes surfaced in the audit queue are preserved, not hidden

**Factory-wide:**
- [ ] every L2 proposition is traceable to an L1 segment, an L0 record, and a source span
- [ ] the V3-B L1 pilot is the reference standard for all future L1 work (no weaker standard)

---

## 6. Factory notes

- L0 is **machine-extracted** from T1 (deterministic, no interpretation).
- L1 is **controlled** (a human/agent produces it under a tight contract; it is the fidelity
  baseline, not the published prose).
- The full L2→L0 traceability is enforced via L200 derivation maps + provenance footers.
- The V3-B L1 pilot demonstrates the exact level of detail required: discourse-segment scoping,
  proposition-preserving controlled prose, a structured apparatus, source-layer tags, and an audit
  queue — with an external benchmark used as a test, not an authority.
