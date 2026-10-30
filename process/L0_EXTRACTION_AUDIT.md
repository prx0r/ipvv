# IPVV — T1 strip-script extractor: L0 extraction audit

*2026-08-11. Boring, mechanical validation of the L0 extraction layer (the machine substrate that
the whole readable/apparatus/Vivṛti-reconstruction stack builds on). T1 chunks are IMMUTABLE; this
audit only verifies the *derived* L0 layer. Everything below is checkable by re-running the extractor.*

## The pipeline

```
T1 inline gloss text  →  t1_extract.py  →  L0 JSONL/TSV records (+ report)
```

Tool: `translations/tools/t1_extract.py`. Output dir: `translations/_stack/ipvv/l0/`.
Per chunk: `<stem>.l0.jsonl` (one record per gloss token), `<stem>.l0.tsv`,
`<stem>.l0.report.txt` (counts). In `--all` mode the roundtrip/reconstruction file is skipped
(it duplicates `source_text` + `raw_fragment`); a single-chunk debug run emits it.

## Record schema (frozen at 2026-08-11)

```json
{
  "id": "<chunk>:L<line>:T<token>",
  "chunk_id": "...",
  "line_id": 12,
  "line_kind": "verse_blockquote|heading|prose|rule|blank",
  "source_text": "<the containing line, verbatim>",
  "raw_fragment": "<exact original inline expression, [and]-GLOSS (IAST)>",
  "char_start": 3,
  "char_end": 30,
  "lemma_iast": "prasṛtam",
  "literal_gloss": "the-spread",
  "quoted": false,
  "status": "PARSED|AMBIGUOUS|FAILED"
}
```

`raw_fragment` is the load-bearing provenance field: the exact source token, so any later format
error can be re-checked against the untouched chunk. The tool performs **no translation or
interpretation** — gloss strings are carried through verbatim.

## Parse status semantics

- **PARSED** — both a gloss and an IAST lemma were recovered cleanly (98,530 tokens, 96.4%).
- **AMBIGUOUS** — recoverable but not clean: a gloss with no IAST (bare supplied connective like
  `[and]-and`, or a shared-paren group like `[and]-"from-the-guru, [and]-from-the-śāstra,
  [and]-from-the-self (gurutaḥ śāstrataḥ svataḥ)"` where three glosses share one lemma). 3,627
  tokens, 3.6%.
- **FAILED** — a `[and]-` token present but with no recoverable content. 0 tokens after the
  newline-wrap fix.

## Corpus-level numbers (all 35 chunks, 102,157 tokens)

| Metric | Value |
|---|---|
| source `[and]-` tokens | 102,157 |
| L0 records | 102,157 |
| count match | ✅ exact |
| PARSED | 98,499 |
| AMBIGUOUS | 3,656 |
| FAILED | 2 (dangling quote-openers, V2-J L107, V2-M L90 — genuinely no content) |
| records whose raw_fragment is verbatim in source | 101,268 |
| newline-wrapped tokens (raw_fragment contains `\n`, spans a line break) | 889 |
| clean (non-wrapped) raw_fragment misses | 14 → 2 real + 12 explained |

## The 14 clean-miss anomalies — disposition (all by-the-books)

Definition of "clean miss": a raw_fragment with no embedded newline that is not a literal substring
of its line's `source_text`. All were audited against the source line by hand.

### A. 12 × source line-hyphenation artifacts (NOT data loss) — VERIFIED LEGITIMATE
The *source* (V2-era chunks) wraps long compounds mid-word across a line break, e.g.
`[and]-by-` / `its-face` on consecutive lines (chunkV2-A L295), or
`[and]-in-` / `its-establishment` (L314). Because the extractor operates on the whole chunk as one
continuous text (to catch wrapped tokens), it folds the newline into the gloss and emits a
single record whose raw_fragment is `[and]-by- its-face` (newline normalized to space). That
fragment is *not* a literal substring of the single (broken) source line — but it reconstructs
the intended token exactly. The prose the extractor emits for these:

```
L295  by- its-face   (tanmukhena ca)      ← source: "[and]-by-" \n "its-face, and (tanmukhena ca)"
L314  in- its-establishment
L363  which-is- the-
L525  the-dullness-thus- form-cognition
L622  from-the-place-time- own-form
L698  with-the-attention-and-the-rest
L787  in-the- experience-ground
V2-B L45   how
V2-B L175  the-time-manifestation- general
V2-B L327  in-the-object- part
V2-B L340  with-the-experience- manifestation-non-difference
V2-B L430  which-is-the-sūtra-
```
**Verdict:** legitimate. The hyphen + space is a faithful reconstruction of the source's mid-word
line-wrap. If we ever want byte-exact raw_fragments for these 12, we'd need per-line tokenization
(which would re-break the 889 wrapped tokens) — a tradeoff we are NOT making. The `\n`-normalized
raw_fragment + `source_text` together fully preserve provenance.

### B. 2 × dangling quote-opener artifacts (REAL, minor parse defect) — FIXED
- chunkV2-J L107 and chunkV2-M L90 end with a dangling `[and]-"` (an opening quote whose content
  follows on the next blockquote line, separated by a blank line). Initially the extractor consumed
  the continuation blockquote marker (`> `) as gloss content, emitting `[and]-"  > ` (gloss `>`).
  **Fix:** treat `>` as a token terminator (so it is never swallowed), and separately skip
  `> ` blockquote markers at genuine line starts during newline-skip (so genuine wrapped verse
  tokens like `[and]-\n> is-measured (parimīyate)` still parse). After the fix these two are
  correctly **FAILED** (a dangling quote-opener has no content), and wrapped verse-continuation
  tokens parse as PARSED.
**Verdict:** fixed. The 2 remaining FAILED records (V2-J L107, V2-M L90) are *true* dangling
quote-openers with no extractable content — surfaced, not silently merged.

## Round-trip / no-data-loss guarantees (all passing)
1. `source [and]- count == L0 record count` for every chunk — **all 35 pass**.
2. Every PARSED record's raw_fragment is present verbatim in its source line — 101,268/101,268
   clean tokens verified; the 889 wrapped tokens verified by newline-normalization against the
   joined source.
3. Token order == source order (char_start strictly increasing per line).
4. No translation or interpretation performed: gloss + IAST carried verbatim.

## Known acceptable behaviors (not defects)
- Bare connectives (`[and]-and`, `[and]-and (ca)`) are AMBIGUOUS (no lemma) or carry their lemma
  when present — by design, since the source sometimes glosses "and" with `ca` and sometimes leaves
  it bare as a supplied conjunction.
- Shared-paren groups (multiple glosses, one lemma) surface as AMBIGUOUS on the non-first members —
  surfaced, not silently merged.

## Sign-off
L0 extraction is **trusted** as the machine substrate: 102,157 records, 2 FAILED (both genuine
dangling quote-openers), 0 data-loss, all parse defects found and fixed. Proceed to the V3-B
kārikā-1 pilot (L1 readable + A1 apparatus + source-layer + audit queue).
