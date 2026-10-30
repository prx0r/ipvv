# IPVV — the translation pack

*Target: Abhinavagupta's Īśvarapratyabhijñāvivṛtivimarśinī (IPVV). This is the working
translation pack for the crown. See `corpus/ipvv-anchor/MANIFEST.md` for the full anchor
corpus (primary sources, the 802-paper scholarship, the term-ledger).*

## The stack

```
00_source/   the base texts
   torella_ipk.txt          Torella's ĪPK critical edition + Vṛtti + English translation
                            (the kārikās the IPVV comments on) — the gold-standard base
   (add: the IPVV Sanskrit vols M00020-22 here, chunked per-passage)
01_t1/       working translations (per passage)
02_r1/       adversarial reviews
03_t2/       opposing readings
04_r2/       adjudications
05_t3/       final resolved translations
06_c1/       commentary
```

## The base text (acquired 2026-08-10)

**Torella, *Īśvarapratyabhijñākārikā of Utpaladeva with the Author's Vṛtti* (critical ed. +
annotated English translation, corrected ed. Delhi 2002).** Text-searchable. The kārikās +
Vṛtti the IPVV comments on. PDF also in `corpus/ipvv-anchor/primary/`.

Also: **B.N. Pandit, *The Īśvara Pratyabhijñā Kārikā of Utpaladeva*** (image-scan, for
page-reference cross-check).

## The method

1. Anchor each IPVV passage on the **kārikā** (Torella's text).
2. Recover the **Vivṛti** layer via Ratié's fragments (the IPVV embeds them).
3. Use the **Dharmakīrti/apoha** papers for the Buddhist opponent.
4. Keep the **term-ledger** at Pratyabhijñā-register throughout.

## The layered edition (the derivation stack)

The T1 golden chunks are the **immutable analytical substrate**. Everything else is *derived*
(never edits the chunks). See `l0/L0_EXTRACTION_AUDIT.md` for the L0 validation and
`pilot/pilot_V3B_k1_readable_apparatus.md` for the frozen four-track pilot format.

```
SANSKRIT  (M00022 + Torella)
   ↓
L0  STRUCTURED LITERAL   = T1 chunks (immutable) + t1_extract.py → l0/*.l0.jsonl records
   ↓
L1  CONTROLLED TRANSLATION = proposition-faithful, close to Sanskrit syntax; for COMPARE / audit
   ↓
L2  READ                   = real book prose (derived from L1; never from/over the golden chunks)
   ↓
L200 CROSS-LAYER AUDIT     = how each L2 reading was derived: L2 ¶ → argument-map segment → L0 range
                            → source range; translation decisions (MT) strictly separated from
                            interpretive assertions (IA); typed cross-references; review state
                            (one file per chunk, `l200/`; originals in `l200_legacy/`)
   ↓
A1  APPARATUS              = material interpretive departures only (the "would a competent reader's
                            view change?" test)
   ↓
SOURCE-LAYER               = who speaks / what is commented (root/Vṛtti/Vivṛti-recon/IPVV/objection/
                             reply/quotation) — the graph that makes IPVV usable
   ↓
AUDIT_QUEUE                = open cruxes surfaced by L1→L2, incl. UNRESOLVED_QUOTATION,
                             INFERENCE_BLOCK, SOURCE_LAYER_UNCERTAIN, TECHNICAL_MEASURE_OR_REALIA
   ↓
C1  PASSAGE COMMENTARY     = what this passage is saying/doing (local, intimate, NOT an essay)
                             two representations (see §C1 below):
                               c1/source/  the structured record (summary/function/terms/context/
                                           explanation/boundary/related) — for QA + API
                               c1/read/    the compact continuous commentary (100–450 words) —
                                           what sits beneath the translated passage for a reader
   ↓
THEMES                    = cross-passage synthesis (what repeatedly emerges across C1s)
   ↓
ESSAYS                    = arguments (comparison, modern application, original synthesis)
   ↓
EDUCATION                 = lessons / explainers / learning
```

**Publication views** — the same passage, four views, no duplicated scholarship:

```
READ      L2 only (book prose)
COMPARE   L1 (Sanskrit-close) + L2
LITERAL   Sanskrit + L1 hyperliteral
CRITICAL  L2 + A1 + SL + AQ + evidence + C1
```

Every L2 sentence links to the L1 span(s) → L0 records → Sanskrit, so readability never sacrifices
auditability. **L2 is a distinct prose pass, not a cosmetic polish of L1**: it dissolves `-ness`,
unpacks compounds, breaks impossible sentences, and surfaces (never invents) external-knowledge gaps.
See `CALIBRATION_REPORT.md` for the layer lock and the L2 production rules; the L2 proof is
`pilot/pilot_V3B_L2_proof.md`. **Audit depth follows risk**; the READ edition must be independently
good.

## C1 — the passage commentary (two representations)

C1 is the **first hermeneutic layer**: what this passage is *saying, doing, presupposing, and
implying* — intimate and local, NOT an essay. **The authoritative governing spec is
`c1/C1-SPEC.md`** (imported verbatim — read it first). It has **two
representations** — the structured record and the public rendering — so the machine object and the
reader's experience are both clean:

```text
c1/source/   the structured editorial object:
             SUMMARY / FUNCTION / KEY TERMS / LOCAL CONTEXT / EXPLANATION / BOUNDARY / RELATED
             — for QA, APIs, and machine processing (never the finished reading)

c1/read/     the compact continuous commentary:
             a continuous 100–450-word explanation of the passage
             [optional Key terms] [optional Note / Open question]
             — what sits directly beneath the translated passage for a reader
```

**The editorial test for C1:** *Could this commentary plausibly sit immediately beneath the translated
verse/passage in a serious annotated edition?* If yes, it's C1. If it needs a title-essay, a modern
comparison, or an original argument, it belongs in THEMES or ESSAYS.

**The layer separation (do not collapse):**

```text
L2         what the text says in readable English
L200       how we justified that translation (philology)
C1         what this passage actually says/does (hermeneutics)
THEMES     what pattern emerges across passages (synthesis)
ESSAYS     what larger argument we can make from that pattern
EDUCATION  how we teach the result clearly
```

**C1 discipline (from `C1-SPEC.md`):** no modern comparison, no use of our essays as primary evidence,
distinguish what the passage *establishes* from stronger conclusions, stay local, and keep it short
(100–250 words ordinary; 250–450 hard; >500 is theme-material leaking down). **The essay-rich,
synthetic C1s written before this correction are preserved** in `c1/_essay-material-legacy/` as assets
for the THEMES/ESSAYS layers — not as C1.

## The pipeline tools- `translations/tools/t1_extract.py` — T1 → L0 records (raw-fragment provenance, PARSED/AMBIGUOUS/
  FAILED). Backed up to R2 (`sanskritree/ipvv-translations/`).
- Layer lock + L2 rules: `CALIBRATION_REPORT.md`.
- Pilots (L1 + A1 + SL + AQ): `pilot/pilot_V3B_k1_L1_apparatus.md`,
  `pilot/pilot_V3B_k2-7_L1_apparatus.md`.
- L2 proof (READ prose on the hard passages): `pilot/pilot_V3B_L2_proof.md`.

## The L200 audit layer

**L200** is the cross-layer audit: it answers "how was the published L2 reading derived, where did
interpretation enter, and what remains unresolved?" It is NOT a commentary (that is C1). Each chunk gets
one `l200/<chunk>.md` in the frozen 8-section schema (see `l200/README-L200-SPEC.md`):

```
0 IDENTIFICATION   1 PUBLISHED READING   2 DERIVATION MAP   3 MATERIAL TRANSLATION DECISIONS
4 INTERPRETIVE ASSERTIONS   5 SOURCE LAYER   6 CROSS-REFERENCES (typed)   7 OPEN/NEEDS_REVIEW
8 REVIEW STATE
```

**The discipline:** translation decisions (SUPPLIED / REFERENT_SUPPLY / STRUCTURAL_CONNECTIVE / LEXICAL /
GRAMMATICAL) are kept strictly separate from interpretive assertions (IA-###), which feed C1. Per-
paragraph SOURCE ANCHOR footers trace each L2 ¶ → argument-map segment → L0 range → source range.
Cross-references are typed (ROOT_TEXT_CONTEXT / SAME_ARGUMENT_CONTINUATION / DOCTRINAL_PARALLEL /
COMPARATIVE_PARALLEL / SECONDARY_SYNTHESIS). The three canonical models (V3-B, V3-C, V2-O) are the
reference standard; the other 60 files were conservatively migrated from `l200_legacy/` (originals
preserved) by `l200_migrate.py`, and are `MIGRATED_PARTIAL` pending editor review. See
`l200/INDEX-AND-REVIEW-LEDGER.md` for the review priority.
