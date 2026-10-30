# SPEC — FACTORY QA & PUBLICATION (the toolchain + the editorial loop)

*The ninth layer. The QA/editorial loop that makes a translation defensible, and the deterministic
publication step that puts it on pāṭala. Simple, disciplined — not a giant QA science project.*

---

## 1. The QA toolchain (built)

| tool | layer | what it does | state | exemplar/result |
|---|---|---|---|---|
| v0 scaler | deterministic triage | FILE_ARTIFACT (regex, 100%), TERM_INTRODUCTION | working | `translations/tools/qa_scaler.py`; caught 22 corrupted files |
| v1 Task-1 | READER QA | prose-only: can the prose carry the argument? | gold needs re-grade | `qa_v1_*.py`, `V1_THREE_CONDITION_FINDINGS.md` |
| v2 Task-2 | FIDELITY QA | is L2 licensed by the source stack? | working | `qa_v2_fidelity.py`; canonical 18 PASS/1 flag |
| human stalls | straight-through read | the real editorial read | done Vols 1–3 | `IPVV_STALL_LOG.md` (60 stalls) |

## 2. The two QA jobs (never conflate)

```
TASK 1 — READER QA:       can the published prose carry the argument?   (prose-only)
TASK 2 — FIDELITY QA:     is the L2 reconstruction licensed by the source? (map+L1+L0+Sanskrit)
```
One metric must not serve both.

## 3. The audit queue

```
strict L200  +  Task-2 fidelity flags  +  Task-1 reader flags  +  human read stalls
          →   CORPUS AUDIT QUEUE (per-passage, severity-tagged)
```
Resolve highest-severity with Sanskrit + scholarship. This is where the translation improves.

## 4. The simple editorial loop (per passage)

```
1. source verified
2. L2 readable
3. L2 traced to L0
4. material decisions extracted
5. compare major translations   (high-risk only)
6. check term ledger
7. high-risk issues get scholarship
8. OPEN stays OPEN
9. human review later
```

## 5. Maturity profile (per passage — not a fake numeric score)

```
Source verified       ✓
Paragraph provenance  ✓
Translation decisions ✓
Context aligned       ✓
External comparison   partial
Specialist review     pending
```

## 6. Publication — deterministic bundles

```
sanskritree         canonical research/source artifacts
   ↓ export (schema validation · ID resolution · publication bundle generation)
patala ingest       ingest bundles into data/corpus
   ↓
patala site/API     render READ/STUDY/THEMES/ESSAYS from bundles (no runtime parsing)
```

**Do not parse historical research files at runtime.** Produce deterministic publication bundles at
ingest time.

## 7. Publishing order — progressive, not pristine

Publish the whole work progressively with transparent maturity states:
```
READABLE · TRACEABLE · AUDITED · SCHOLARLY-CHECKED · REVIEWED
```
The canonical chunks can be showcases; the main value is searchable full-corpus access.

---

## 8. EXEMPLARS — the toolchain in action on the IPVV

### v0 — deterministic triage (artifacts + terms)
`translations/tools/qa_scaler.py` caught **literal `EOF` + heredoc remnants in 22 of 33 L2 files**
(Vol 1 H–N, Vol 2 E–S) — a real, systematic corruption class, regex-detectable and cleaned
separately from semantic QA. The tests are in `translations/tools/tests/test_qa_scaler.py` (8/8).

### v1 — the three-condition experiment (the gold was over-logged)
`translations/tools/V1_THREE_CONDITION_FINDINGS.md` shows prose-only vs map-inclusive vs gap-diff.
The decisive finding: **the gold was over-logged** — 4 of the B-bucket positives got STRONG-PASS
from two independent readers (the arguments were in the prose). Re-grade before trusting recall.

### v2 — scholarly fidelity on the canonical chunks
`translations/tools/qa_v2_fidelity.py` checked the 3 canonical L200 chunks:
**V2-O (4 PASS) · V3-B (7 PASS) · V3-C (7 PASS + 1 UNRESOLVED_SOURCE_DEPENDENCY)**.
The 1 flag (V3-C ¶8) marks the per-appearance sūtra content as not-yet-verified — exactly the
honest behavior the factory wants. Verdicts: `l200/TASK2_VERDICTS_CANONICAL.jsonl`.

### human stalls — the straight-through read
`IPVV_STALL_LOG.md` — 60 stalls (Vols 1–3), classified by type/severity, with provenance anchors.
This is the "real editorial read" that no scaler replaces.

---

## 9. VALIDATION — how we know the QA/publication is correct

**Per-passage (the editorial loop, above):**
- [ ] source verified · L2 readable · L2 traced to L0 · decisions extracted · high-risk compared ·
      term ledger checked · OPEN stays OPEN · review state recorded
- [ ] maturity profile is honest (a checkbox profile, not a fake numeric score)

**Factory-wide:**
- [ ] the Task-1 gold is re-graded (over-logged items dropped) before any recall metric is published
- [ ] no passage is surfaced as authoritative until its L200 passes Task-2 and review state ≥ editor
- [ ] the audit queue is assembled from all four sources (L200 + Task-2 + Task-1 + human stalls)
      and highest-severity items are adjudicated with Sanskrit + scholarship
- [ ] publication bundles are deterministic (schema-validated, ID-resolved); the site never parses
      historical research files at runtime
- [ ] the work publishes progressively (READABLE → … → REVIEWED), not as pristine islands
