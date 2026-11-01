# L200 REVIEW — WHAT IT IS, HOW AUDITABLE, HOW VALIDATED
*2026-08-11. A critical self-review of the L200 cross-layer audit layer — what it is, how auditable it
actually is, and how the auditability is validated. This is both the review and the reviewer's guide:
it states the honest state of the layer, what was verified, what remains, and how to validate any L200
going forward.*

---

## 1. WHAT L200 IS (one paragraph)

L200 is the **derivation audit** of the IPVV translation. For each of the 63 chunks it answers exactly
one question: *how was the published L2 reading derived from the source, where did interpretation enter,
and what remains unresolved?* It is NOT a readable summary (that is L2) and NOT a commentary (that is
C1). It is a strict 8-section ledger:

```
0 IDENTIFICATION    1 PUBLISHED READING   2 DERIVATION MAP   3 MATERIAL TRANSLATION DECISIONS
4 INTERPRETIVE ASSERTIONS   5 SOURCE LAYER   6 CROSS-REFERENCES (typed)   7 OPEN/NEEDS_REVIEW
8 REVIEW STATE
```

The single most important discipline: **translation decisions are kept strictly separate from
interpretive assertions.** A `SUPPLIED` (English inserted because Sanskrit leaves it implicit) is a
translation decision; an `EXPLANATORY_RESTATEMENT` ("the one manifests as the many") is an interpretive
assertion that feeds C1, never a translation claim. The audit is stricter than the prose.

---

## 2. THE 63 FILES (what's in the layer)

| Kind | Count | Content |
|---|---|---|
| Canonical models (hand-authored) | 3 | V2-O, V3-B, V3-C — the reference standard; full per-paragraph SOURCE ANCHORs |
| Hand-authored closes | 8 | V3-I..P — strict, with SOURCE ANCHORs |
| Standardized (migrated + structured) | 52 | strict 8-section; chunk-level L0 ranges + typed crossrefs |
| Prose-format chunks (no L0) | 14 | the small V1 k1.x/upoddhāta/pūrvapakṣa files — correctly flagged as no-L0 |
| Originals preserved | 55 | `l200_legacy/`, never overwritten |

**Review state:** all 63 are `editor-reviewed` (reviewed_by: editor, 2026-08-11).

---

## 3. HOW AUDITABLE IT ACTUALLY IS (the honest assessment)

### 3.1 The layer is auditable at three levels of granularity

**Level 1 — the chunk.** Every L200 §0-IDENTIFICATION gives the source (M0002X lines), the T1 chunk,
the L0 file, the argument map, the L2 read. A reader can open all five and see the layer stack for the
chunk.

**Level 2 — the argument-turn (the strongest level).** §2-DERIVATION MAP gives, per L2 paragraph, the
L0 range (`L61:T1204–L67:T1391`) and the source range. For the 11 hand-authored files this is
per-paragraph (SOURCE ANCHOR); for the 52 standardized files it is chunk-level (the full L0 extent).
**This is the real cross-layer trace:** L2 ¶ → argument-map segment → L0 range → source range.

**Level 3 — the token (only where needed).** The canonical models give the key tokens (lemma + gloss)
for the load-bearing claims (e.g. `akramānantacidrūpaḥ pramātā sa maheśvaraḥ`). Token-level alignment
is deliberately reserved for load-bearing claims, disputed decisions, and QA-flagged passages — not
every sentence.

### 3.2 What is and is not verifiable

**Verified (this review):**
- All 63 files have the full 8-section structure.
- All 49 cited L0 ranges fall within the actual L0 file line extents (VALIDATION 2: 0 mismatches).
- All 79 cross-referenced V#-chunks exist (VALIDATION 3: 0 unmatched).
- All 63 carry editor-review metadata (VALIDATION 4).
- The 55 legacy originals are intact (VALIDATION 5).
- No empty/broken files (VALIDATION 6).

**Not verifiable from the L200 alone (the honest boundary):**
- **The semantic fidelity** of the L2 prose to the Sanskrit is NOT proven by the L0 range alone. The L0
  range shows *where* the reading came from; it does not prove the reading is *correct*. That is the
  task of a specialist reviewer reading the L2 against the Sanskrit.
- **The 52 standardized files' per-paragraph anchors** are chunk-level, not paragraph-level (the 11
  hand-authored files have the full per-paragraph anchors). A reader can verify the chunk's provenance
  but not, from the L200 alone, pin each sentence to its exact L0 span.
- **The typed cross-reference relations** in the 52 standardized files are best-effort auto-types
  (ROOT/SAME/DOCTRINAL/COMPARATIVE/SECONDARY), accepted by the editor but not re-verified against the
  full text.
- **The IA interpretations** (99 assertions) are the editor's reading — they feed C1, but they are
  interpretations, not translations, and need specialist confirmation.

---

## 4. HOW TO VALIDATE ANY L200 (the audit protocol)

### 4.1 The derivation is valid if...

1. **The L0 range resolves.** Open `l0/<chunk>.l0.jsonl`, jump to the cited `L{min}:T{start}` —
   `L{max}:T{end}`, and confirm the tokens are there. (Scriptable: `l200_validate.py` does this.)
2. **The load-bearing tokens justify the rendering.** For each `LEXICAL` decision in §3, the Sanskrit
   lemma is present at the cited L0 line and the English rendering is defensible.
3. **The SUPPLIED items are truly supplied, not silent additions.** A `SUPPLIED` item must be either
   (a) an English word inserted because Sanskrit leaves it implicit, or (b) flagged — it must never be
   a doctrine added under the cover of translation.
4. **Every EXPLANATORY_RESTATEMENT is in §4 (IA), not §3.** If a paraphrase of the argument appears as
   a translation decision, the audit has failed its central discipline.

### 4.2 The interpretation is valid if...

5. **The IA is traceable to a basis.** Each IA-### cites the L0 token or the argument-map segment that
   licenses it. An IA with no basis is a guess, not an assertion.
6. **The IA does not contradict a §3 decision.** If §3 says the text renders X literally and §4 says
   it means Y, that is a flagged tension, not a silent conflation.

### 4.3 The layer is valid if...

7. **The chunk-level L0 range is consistent** across the L200, the L0 file, and the source.
8. **The cross-references resolve** to real chunks (VALIDATION 3).
9. **The review state is honest** — `machine` until reviewed, `editor-reviewed` after, `specialist`
   after specialist sign-off. The OPEN items are genuine philological notes, not hidden defects.

---

## 5. THE VALIDATION SCRIPT (`l200_validate.py`)

A validator that enforces the scriptable checks automatically:

```text
l200_validate.py
  1. STRUCTURE    every file has all 8 sections
  2. L0_RANGE     every cited L0 range falls within the actual L0 file line extents
  3. XREF         every cross-referenced V#-chunk exists
  4. REVIEW_META  every file has reviewed_by + reviewed_at (if editor-reviewed)
  5. NO_STRAY     no NEEDS_REVIEW apparatus items remain
  6. NONEMPTY     no file under a size threshold
```

This is the machine part of the audit; the semantic part (steps 1–6 of §4) is the human part. The
validator cannot prove fidelity — it proves the *trace* is well-formed.

---

## 6. WHAT REMAINS (the honest to-do)

The L200 layer is **structured, validated, and editor-reviewed** — it is a well-formed audit. What
remains is the **depth** pass, not the structure:

1. **Per-paragraph SOURCE ANCHORs for the 52 standardized files.** The 11 hand-authored files have
   them; the 52 have chunk-level L0 ranges. Adding the per-paragraph anchors (L2 ¶ → argument-map
   segment → L0 span) would make every sentence pinnable. This is the main upgrade path.
2. **Specialist review of the IA assertions (99).** The editor accepted them; a domain specialist
   should confirm the 99 interpretations (especially the analytical labels like "universality gap").
3. **Re-verify the auto-typed cross-reference relations** against the full text (the 52 files' typed
   relations were accepted on best-effort).
4. **Resolve the OPEN philological items** (citation frames, enumeration details) — these are logged,
   not defects, but a specialist can close them.
5. **Keep the semantic-fidelity check** in mind: L0 ranges prove provenance, not correctness. The final
   assurance is a specialist reading the L2 against the Sanskrit — which is exactly what the essay
   library and the C1 layer are for.

---

## 7. THE VERDICT

L200 is **auditable and validated at the structural level, and its semantic fidelity rests on the
human review that was applied.** It does what a derivation ledger should do: it makes every reading
traceable to its source, separates translation from interpretation, and records its own review state.
It is **not** a proof that the translations are correct — no audit layer can be — but it is a complete,
well-formed, reviewer-signed record of *how they were derived*. The remaining work is depth
(per-paragraph anchors, specialist sign-off on the IAs), not structural repair.

---

*This is the L200 review. The layer is a strict 8-section derivation audit: how each L2 reading was
produced, where interpretation entered, what remains open. It is validated (structure, L0 ranges,
cross-references, review metadata all checked); it is editor-reviewed; and its honest boundary is that
L0 ranges prove provenance, not correctness — the semantic fidelity is the task of the specialist
review and the C1 layer.*
