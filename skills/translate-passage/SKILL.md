---
name: translate-passage
description: "Run one Sanskrit verse through the full Pāṭala translation flow (T1→R1→T2→R2→T3→T3.1→C1) producing a structured, audited passage record. Use when asked to translate a tantric verse in the house style, or to build a gold exemplar."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [translation, sanskrit, pipeline, patala, tantra, scholarly]
    related_skills: [validate-passage, assemble-stack, write-commentary]
    checkpoint: CP1 (a passage through T1->C1, the source floor)
---

# Translate a Passage (the full flow)

## When to use
- Asked to translate a Sanskrit/IAST verse into the Pāṭala house style.
- Asked to produce a gold exemplar record.
- Asked to advance a text's pipeline (e.g. "produce the R2 for kramasadbhava 1.8").

## The flow
Produce each floor **in order**. Do not skip floors.

```
T1 → R1 → T2 → R2 → T3 → T3.1 → C1
```

### T1 — working translation
- `close_translation` = structurally faithful, IAST, technical terms retained (śakti, kula, krama, spanda, vimarśa, prakāśa, visarga, khecarī, āveśa, uccāra, śūnya, mātṛkā, saṃvit, parāmarśa, svātantrya, tattva).
- Add `[X]`/typed flags (`TXT GRAM LEX DOCT WIT SUP`) where uncertain.
- Add notes with `[G]` grammar / `[P]` parallel / `[A]` anchor / `[R]` reconstruction.
- Provide the `time_place_context` block (PERIOD / PLACE / GENRE / FRAME).

### R1 — peer review of T1
- Review T1 intimately against the Sanskrit + any anchor.
- Per crux: verdict `RIGHT / ERROR / FORK / OPEN` + evidence.
- Leave **short commentary stubs** (the seeds of the final commentary).
- Challenge; don't confirm.

### T2 — the alternative
- A complete alternative that **actively opposes T1** where T1 is wrong or limited.
- Informed by R1. Different reading-strategy; adopt a different interpretation where the Sanskrit allows.
- Where the text is fixed and you land on the same reading, say so (that agreement is the hard core).

### R2 — the synthesis
- Compare T1 vs T2 line by line.
- `hard_core` = where they agree. `divergence` = the difference.
- Adjudicate which is best + why (readability, grammar, evidence).
- Research the school/period context. **Expand the commentary.**
- Note `equal_alternates`. Mark genuinely-interpretable verses `OPEN`.

### T3 — final resolved text
- The settled scholarly reading; carry genuinely-open `[X]` inline + editorial notes.

### T3.1 — reader's edition
- Natural English derived from T3, in lock-step. Flowing, defensible. Don't change meaning.

### C1 — commentary
- Plain-English interpretation for a thoughtful reader.
- You MAY research independently and overturn T3, but say so explicitly.
- Keep it grounded in the Sanskrit.

### The MEGA-CHUNK rule (for long commentaries like the IPVV)
For a long running-commentary (the IPVV's ~34,000 lines), do NOT translate per-kārikā slivers.
Translate in **500+ line continuous swathes** — one file per chunk, the whole block rendered as
one continuous piece. Pass 1 = volume (get the paint on the wall); pass 2 = register polish.
The adversarial work (rival readings + evidence + decisions) is embedded inline in an
`## apparatus` block, not separate files (unless a genuine crux). Track each chunk in the
work's TRANSLATION_PROGRESS.md. See `sanskritree/corpus/abhinava/READ_FIRST.md` §6a.

## The output shape
A passage record (see `pipeline/schema.py`). Populate the `stages` dict floor by floor,
keep the `lineage`, and confirm the record passes `pipeline/audit.py`.

## Invariants (never break)
1. Machine output enters as a proposal, never authority.
2. Translation prose and interpretive decisions have independent version histories.
3. Preserve ambiguity — don't launder `[X]`.
4. Don't copy published translations or prior T-versions.
5. Grammar of the present passage overrides any parallel/commentary.
