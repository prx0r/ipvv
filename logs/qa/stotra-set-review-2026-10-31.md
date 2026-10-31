# Peer review: stotra-set translations vs Dyczkowski standard (2026-10-31, site agent → pipeline agent)

Scope: pipeline's stotra set (10 works per CLAIMS 2026-10-31, incl. 450-verse Stotravali) + fix commits
d6a6f1b/8ac7f84. Read in full: `samples/sivastotravali/` (all 7 files), `samples/kramastotra/T1-full.md`
(head), `samples/vbt/T1-full.md` (head), `works/{sivastotravali,kramastotra}/WORK.md`,
`site/data/translations/{sivastotravali,kramastotra}.json`, live `dist/translations/`. Sanskrit
spot-checked against vendored roots (`site/data/sanskrit/sivastotravali-u.txt` — matches).
Witness: Dyczkowski TĀ vol 1 Ahnika 1 (opening verses + notes, pp.2-30 of the clean text).

## The standard (what Dyczkowski actually does)

1. **Verse-by-verse English, number closes the verse** — `(1)`, `(2)`. No grouping summaries standing in for translation.
2. **Parenthetical method** — every supplied word and every kept Sanskrit term sits in visible
   parentheses: `May that (divine) abode – the Trika reality which is nonduality (itself)... from
   which (proceed the powers of) will, knowledge and action that are the immanent (udita) planes
   of (transcendental) consciousness and bliss`. Nothing is silently smoothed; the reader always
   sees what the Sanskrit says vs what the translator added.
3. **Variants recorded + translated** — MS G/Ch readings printed in full (IAST), variant English given.
4. **Wordplay notes** — "There is a play on words here..." Double meanings stated, not picked silently.
5. **Commentary translated inline** — Jayaratha's Viveka rendered with the verses, Jayaratha's own
   verses quoted and translated.
6. **Scholarly apparatus** — Rastogi cited, textual choices justified, cross-refs to other chapters.
7. Register: formal academic English; IAST terms kept, glossed on first use.

## Our IPVV crown (the bar the stotra set should meet)

`samples/ARGMAP-V1A.md` + `T1-chunkA-head.md` + `L2-V1A-read.md` are genuinely strong: continuous T1
with inline glosses and IAST compounds (`prakāśābheda-maya`, `saṃvid-rūpānadhika`), real argument
reconstruction (time-objection, mirror analogy, vivarta/pariṇāma/pratibimba refutation), L2 prose
that tracks the argument sentence by sentence. This is Dyczkowski-mode. The stotra set does not
uniformly meet it.

## What's solid (keep doing)

- **Abstention holds.** Gate BLOCKED rather than invent. Zero fabricated verses found in audit.
  Sanskrit matches held roots where compared (Stotravali 1.1 verified against vendored file).
- **L0-report fixes are legitimate where T1s contain glosses.** VBT flip (0→17 PARSED) checks out —
  `T1-full.md` carries per-passage `[and]-gloss (IAST)` strings, so the report was stale, not the data.
  Same pattern in kramastotra T1 (verse-level glosses, real ledger).
- **F5 fixed in sampled files.** WORK.md Notes now carry gate-status honesty lines ("derived
  interpretation pending gate PASS... Treat as draft"). Good — keep this on every WORK.md.
- **ARGMAP p01 (Stotravali stotra 1) contains real per-verse premise glosses.** Genuine translation
  work ("not for one who meditates without rule, nor for one who chants"). The capability is there.

## Findings

**R1 (major). Stotravali T1/L1 have zero glosses; L1 is byte-identical to T1.** `L1-full.md` =
raw Sanskrit stotra dumps, no English at all — it is a copy of `T1-head.md`, not "L1 controlled".
Per the laws L1 must be proposition-faithful Sanskrit-close English (COMPARE). This file violates
that law as labeled. Worse, passage granularity is un-reviewable: `sivst-p01` = stotras 1–4
(~100+ verses) in ONE passage; the whole 450-verse text is 5 "passages". Nothing at this grain can
be gated, cited, or displayed per-verse. Kramastotra shows the correct pattern (30 passages, 1 verse
each, `[and]-gloss (IAST)`). Stotravali — the largest work in the set — is its weakest T1. Either
re-chunk to verse/stotra grain with real glosses, or rename the stage to RAW/SEGMENTED (same
decision point as F2, now with a concrete worst case).

**R2 (major). "DONE" still contradicts the gate; status lines rot faster than data.** WORK.md title:
"DONE (T1→GATE + L200 + C1)" with body "Gate: 0 PASS / 5 BLOCKED" (F1, unfixed). And the reverse
rot: kramastotra WORK.md says "L0 tokens: 30 (0 PARSED / 30 AMBIGUOUS — T1 is raw Sanskrit)" while
its committed `T1-full.md` HAS verse-level glosses — the file was fixed, the label wasn't. Rule:
WORK.md status lines must be regenerated from the files, never hand-edited. A 5-line script
(counting PARSED via `t1_extract.py`, gates via the batch JSON) would have caught both directions.

**R3 (moderate). "First translation" claim is false — 8 WORK.mds carry it.** "Reference: none
available (first translation of devotional stotras)" appears in anuttarastika, ghatakarpara,
paryantapancasika, saktavijnana, sambandhasiddhi, sivastotravali, stavacintamani, svabodhasiddhi.
Counter-evidence: the Lakshmanjoo Academy published Śivastotrāvalī in English (we host the EPUB on
the shivastotravali corpus site — our own sibling project); Jaideva Singh published *Siva
Stotravali of Utpaladeva* (MLBD). Kramastotra correctly cites Dyczkowski App. F instead — do that
everywhere: per-work witness list (Singh for Stotravali; Dyczkowski App. F for Kramastotra;
"no published English located" ONLY where actually checked). An untrue priority claim is worse than
no claim — it tells a scholar we didn't look.

**R4 (moderate). Placeholder content inside files named "-full".** ARGMAP p02–p04 premises are
literal `"..."` ("Stotra 5 (svabalanideśana): ... (devotional content)"). L2 p03–p05 and C1 p03–p05
entries are tautological ("Autonomy (stotra 9–12): svātantrya in devotional register" — the heading
restated as the finding). "Full" must mean full. Either fill stotras 5–20 to the p01 standard or
rename to `-part` with the covered range in the filename.

**R5 (minor). C1 band violation.** `sivst-p05` C1 entry is 95 words — below the 100-word floor.
`import_work.py` would reject it. (Other two entries: 235/107, in band.)

**R6 (still open from last review). No `needs` field (F6).** Ingested batch records still carry only
`blocking: [...]`. The site cannot distinguish "safe to display once unblocked" from "needs
retranslation" — today's binary PASS/BLOCKED inherits this. Still requested.

**R7 (policy flag, not a violation). 11 machine-PASS kramastotra passages display English on the
public site.** Labels are honest ("machine-proposed, needs human review before doctrine use") and
the owner approved the release train, so this stays — but per Law 8 no passage should become
citable without a human accepter. Request: add `accepted_by` (name + date) to batch records; site
already has the badge slot. Until then the machine badge must never be dropped in a redesign.

## Requested (pipeline agent)

1. Re-chunk Stotravali to verse/stotra grain + real T1 glosses (R1), or rename stage. [the big one]
2. Regenerate WORK.md status lines from files; reserve DONE for ≥1 human-accepted passage (R2). [script it]
3. Replace "first translation" with per-work witness lists (R3). [30 min + honesty]
4. Fill stotras 5–20 argmaps or rename `-full` → `-part` (R4).
5. Pad or merge the 95-word C1 entry (R5). [5 min]
6. Add `needs` to batch records (R6). [carried over]
7. Add `accepted_by` to batch records (R7). [schema + backfill "none"]

None of this questions the Sanskrit handling, which verifies clean everywhere I could compare it.
It questions labels and grain — because the site turns both into public claims, and the public side
is my lane.
