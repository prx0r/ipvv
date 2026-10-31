# IPVV — Process notes & next steps (toward a scholarly resource)

*2026-08-11. What we did, how we did it, what is still missing, and a justified route to making the
full IPVV readable edition a defensible scholarly resource. This records the *process* (the lived
method) and the *gaps* (verified against disk), then lays out options with justifications.*

---

## 1. Process notes — what was done, and how

### 1.1 The layered stack (locked in `CALIBRATION_REPORT.md`)
```
SANSKRIT (M00020/21/22 + Torella)
  → L0  structured literal   : token/gloss records (t1_extract.py → *.l0.jsonl)
  → L1  controlled translation : proposition-faithful, Sanskrit-close (for COMPARE/audit)
  → L2  READ (book prose)
  → A1  APPARATUS (material interpretive departures only)
  → SL  SOURCE LAYER (speaker / objection / reply / quoted source)
  → AQ  AUDIT QUEUE (LEXICAL_CRUX, INFERENCE_BLOCK, SOURCE_LAYER_UNCERTAIN, TECHNICAL_MEASURE_OR_REALIA, …)
  → C1  PASSAGE COMMENTARY (what this passage is saying/doing — compact and local; TWO representations:
        `c1/source/` the structured record + `c1/read/` the continuous 100–450-word commentary.
        Spec: `c1/C1-SPEC.md`)
```
The golden T1 chunks are **immutable**. Everything else is derived; nothing edits them.

### 1.2 The derivation method (the "freestyle" that worked)
For each passage we:
1. Read the **raw Sanskrit source** (M00020/21/22) directly — not just the compressed L1.
2. Wrote an **ARGUMENT MAP**: speaker, the question at issue, premises, inference, conclusion,
   unresolved terms. This was the single biggest fix — see `IPVV_FREESTYLE_LESSONS.md` L1: *reconstruct
   the argument, not the sentence*.
3. Wrote the **L2 READ** from the argument map, Dyczkowski-mode: continuous philosophy, bracketed
   interpolations only where a reader needs them, never smoothing an obscure passage into false
   clarity.
4. Appended a **Fidelity note**: preserved / added (SUPPLIED) / not-resolved.
5. (From Vol 1-G onward) dropped the boilerplate "Verdict: understood and readable" closer — see
   Lesson L11.

### 1.3 Coverage actually on disk (verified 2026-08-11)
| Layer | Vol 1 (M00020) | Vol 2 (M00021) | Vol 3 (M00022) |
|---|---|---|---|
| T1 golden (immutable) | `01_t1/` (28 md) | `02_t1/` (19 md) | `02_t1/` (16 md) |
| L0 records | `l0_v1/` (14 main chunks A–N; ✅ 2026-08-11) | 19 jsonl | 16 jsonl |
| L1 controlled | — | — | V3-B pilot only |
| Argument maps + L2 | A–N (28) | V2-A…S (38) | V3-A…P (32) |
| Backed up to R2 | ✅ | ✅ | ✅ |

**L0 gap CLOSED for Vol 1 (2026-08-11):** ran `t1_extract.py --dir 01_t1 --out l0_v1`. The 14 main
chunks (A–N) extracted cleanly: **21,247 PARSED / 816 AMBIGUOUS / 1 FAILED** (22,064 tokens), with the
round-trip count matching exactly (22,064 = 22,064). Backed up as `l0/ipvv_l0_v1_jsonl.tar.gz`.

**Note on the small Vol-1 files:** the `k1.x`, `purvapaksa-*`, and `upoddhata-*` files (14 of the 28)
use a **different, older T1 format** — `**T1:**` prose glosses + `*[...]*` philological notes, not the
`[and]-GLOSS (IAST)` token format. The extractor correctly finds 0 tokens in them. These are
essentially already-readable prose-format chunks (an older, more fluent register), so they do not need
the L0 tokenization; treat them as early-format readable chunks.

**Remaining gaps (verified):**
- **L1 controlled exists only for V3-B.** The rest of the corpus jumps T1 → (argument map) → L2.
- **L2→L0 linkage: prototyped (V2-H).** The L2 sentences are *derived from* argument maps grounded in
  the Sanskrit, but there is no formal pointer from each L2 sentence back to the L0 record span(s). The
  "auditability" promise (see `CALIBRATION_REPORT.md`) is not yet structurally enforced.
- **The V2/V3 L2 files still carry the old boilerplate "Verdict:" closer** (27 files) — harmless but
  un-polished; the Vol 1 files were stripped.

**Prototype done (2026-08-11):**
- `pilot/pilot_V2H_L2PROVENANCE.md` — paragraph-level L2→L0 provenance for V2-H (the parā-vāk /
  sphaṭika passage). Each L2 block is anchored to (T1 chunk lines = L0 line_id, L0 record-id range,
  source lines). Includes scaler fixtures (term-policy-drift example; speaker/quotation-boundary check).
- `IPVV_STALL_LOG.md` — the straight-through-read (F-pass) stall-log template (location / type /
  severity), which becomes the QA scaler's gold fixtures.

---

## 2. The core question: reconcile the READABLE (L2) with the L0?

The honest answer: **they are already reconciled in *content* (every L2 was argued from the Sanskrit
through the L0/L1 reading), but not in *structure*.** There is no pointer from an L2 sentence to the
L0 record it rests on. For a scholarly resource, that structural trace is the load-bearing feature —
it is what lets a reader *verify* any claim, and what distinguishes a serious edition from a
"black-box AI translation."

The reconciliation has three sub-problems, and they should be solved in order:

### 2.1 Vol-1 L0 gap — **CLOSED (2026-08-11)**
`t1_extract.py` now accepts `--dir`/`--out`; ran it over `01_t1/` → `l0_v1/`. The 14 main chunks
(A–N) extracted cleanly (21,247 P / 816 A / 1 F; count-match verified). The 14 small files
(k1.x, purvapaksa-*, upoddhata-*) use an older prose-format T1 and are exempt (no tokens).

### 2.2 Then, build the L2→L0 link (the real reconciliation)
The scholarly-critical feature. Every L2 sentence gets an anchor to the L0 records it derives from:

```text
L2 sentence
  → argument-map segment
  → L0 record ids (chunk:line:token)
  → Sanskrit
```
Two implementation choices:
- **(a) Lightweight:** add a per-paragraph provenance line to each L2 file (e.g.
  `[L2 §4 ⇠ V3-B S7: L37 T14–T28]`). Manual, cheap, human-readable.
- **(b) Structural:** the argument map already names the source lines. Automate a checker that (i)
  reads the argument map's line refs, (ii) pulls the corresponding L0 records, and (iii) flags L2
  sentences whose content is not derivable from those records (a *fidelity gate*). More work, but it
  operationalizes "readability generates the audit queue."

**Recommendation: do (a) now for the corpus, prototype (b) on one chunk as the QA scaler.**

### 2.3 Then, run the two-axis QA scaler (FIDELITY + PROSE)
Per chunk, produce a compact QA report (as you proposed):
```
FIDELITY QA   lost/added proposition · changed polarity · changed speaker · unresolved referent
PROSE QA      literalism · -ness density · left-branching leakage · sentence overload · unclear antecedent · repetition
```
This is what stops the model from "fixing readability" by quietly damaging the philosophy.

---

## 3. Options — with justifications (goal: a scholarly resource)

### Option A — Close the Vol-1 L0 gap + add L2→L0 provenance lines (the foundation)
**Do this first.** Justification: without Vol-1 L0, a third of the corpus is unverifiable; without
provenance, none of it is *structurally* verifiable. This is the single highest-leverage step: it makes
every L2 sentence checkable, which is the baseline for scholarship. Low effort, unlocks everything
below.

### Option B — Build the QA scaler and audit the whole corpus
After A. Justification: a corpus is only "good" if drift is *measured*. The scaler produces the audit
queue (LEXICAL_CRUX / INFERENCE_BLOCK / SOURCE_LAYER_UNCERTAIN / TECHNICAL_MEASURE_OR_REALIA) that
turns the readable edition from "plausible" into "defensible." It also feeds the term-policy check
(`prakāśa`, `vimarśa`, etc. across all 100+ L2 files).

### Option C — Reconstruct the lost Vivṛti as a separate scholarly layer
The IPVV is Abhinava commenting on Utpaladeva's (partly lost) Vivṛti. Ratié's work shows this is
feasible and is the most original scholarly contribution this project could make. Justification: a
"navigable Vivṛti-reconstruction layer" (each fragment: Sanskrit, translation, basis, certainty,
Ratié/Torella comparison) is more novel than yet another readable IPVV. Build it after A+B, on the
argument maps (which already flag quotation vs. commentary).

### Option D — Publish as four views (READ / COMPARE / LITERAL / CRITICAL)
Build the multi-view renderer from the layered stack. Justification: this is the deliverable shape —
a reader can read the book (L2), or drill to Sanskrit+literal (L0/L1), or see the full apparatus
(A1/SL/AQ/C1). This is what Dyczkowski/Ratié-style editions do, but with the audit layer *underneath*
rather than as 70 footnotes.

### Option E — Cross-check the hardest cruxes against the on-disk scholarship
The mining dossier (`corpus/ipvv-anchor/dossiers/IPVV_VOL3_MINED_TRANSLATIONS.md`) already caught one
real error (daśaradana = ten-tusked). Justification: selectively verify the AQ's OPEN/high-risk items
(measures, universals, the atom-vs-part-possessor, the parā-vāk) against Ratié/Torella/Dyczkowski to
raise the philological floor where it matters most. This is the "audit depth follows risk" principle.

### Option F — The full straight-through human read
Read the whole L2 as a book (Vol 1 → 3), marking anything that stalls. Justification: the real
publication test. Cheap, catches style drift and referent drift that no scaler fully catches.

---

## 4. Recommended sequence (with reasons)

1. **A (Vol-1 L0 + provenance lines)** — the verifiability baseline; cheap; unblocks all traceability.
2. **F (straight-through read)** — cheap; tells us where B's scaler will matter and surfaces drift.
3. **B (QA scaler + full audit)** — turns "readable" into "defensible"; produces the audit queue.
4. **E (scholarship cross-check of the cruxes)** — raises the floor on the hardest passages.
5. **C (Vivṛti reconstruction)** — the most original scholarly contribution; builds on the argument maps.
6. **D (four-view publication)** — the final deliverable shape.

Steps 1–2 are nearly free and should be done immediately. Steps 3–6 are where the project becomes a
*resource* rather than a *draft*.

---

## 5. Immediate next action — **DONE (Vol-1 L0 closed)**

~~Run `t1_extract.py` over `01_t1/` to close the Vol-1 L0 gap, then verify the round-trip.~~
**Done 2026-08-11** — Vol 1 chunks A–N now have L0 in `l0_v1/` (backed up). The next concrete move is
**2.2: build the L2→L0 provenance linkage** (start with the lightweight per-paragraph provenance lines
on one chunk, then prototype the structural fidelity-gate as the QA scaler).
