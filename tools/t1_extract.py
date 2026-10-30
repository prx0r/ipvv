#!/usr/bin/env python3
"""T1 strip-script extractor: parse the IPVV golden T1 chunks into structured L0 records.

The T1 chunks are IMMUTABLE. This tool only *reads* them and emits a derived L0
JSON/TSV layer (never edits the chunk). Each inline gloss token:

    [and]-GLOSS (sanskrit)          normal lemma+gloss
    [and]-"GLOSS (sanskrit)"        quoted (verbatim pratīka / root-text quotation)
    [and]-and                       bare supplied connective, no IAST
    [and]-and (ca)                  "and" with a lemma

becomes a record carrying full provenance (chunk_id, line_id, source_text,
raw_fragment, char_start/end, speaker/discourse context) plus a parse status:

    PARSED      -> gloss + IAST both recovered cleanly
    AMBIGUOUS   -> recoverable but not clean (e.g. no lemma, or unexpected shape)
    FAILED      -> token present but not parseable; raw_fragment preserved

Every record keeps `raw_fragment` = the exact original inline expression, so any
later format error can be re-checked against the untouched chunk.

Usage:
  python3 t1_extract.py <chunk.md> [--out <prefix>] [--format json|tsv|both]
  python3 t1_extract.py --all  (runs over every chunkV*.md in 02_t1/)

Outputs (per chunk, prefix default = chunk basename):
  <prefix>.l0.jsonl   one JSON record per token
  <prefix>.l0.tsv     terse tab-separated (id, status, iast, gloss)
  <prefix>.l0.roundtrip.md  reconstructed text for visual diff vs original
  <prefix>.l0.report.txt    parse-status summary + validation numbers

This tool performs NO translation or interpretation. It only tokenizes and
extracts; the gloss strings are carried through verbatim.
"""

import json
import re
import sys
from pathlib import Path

# --- token grammar -----------------------------------------------------------
# Each gloss token begins with [and]- ; then an optional ", then the English gloss
# (which may contain letters, spaces, apostrophes, hyphen-joins, / ), then an
# optional parenthesized IAST, then an optional closing ", then a terminator.
# Terminators: , ; | : " newline, or the verse marker  — (N).
#
# GLOSS stops at: an opening '(' (then IAST until the matching ')'), or at any
# separator ( , ; | : ) or an en/em dash or a '"' or the next "[and]-" — whichever
# comes first. A running `in_quotes` state (toggled on '"') marks quoted spans.

def tokenize_line(text: str, line_id: int, chunk_id: str, line_kind: str):
    """Split one T1 line into gloss-token records with running quote state."""
    records = []
    n = len(text)
    starts = [m.start() for m in re.finditer(r'\[and\]-', text)]
    if not starts:
        return records
    in_quotes = False
    # establish quote state before the first token
    prefix = text[:starts[0]]
    in_quotes = (prefix.count('"') % 2 == 1)
    for idx, s in enumerate(starts):
        q_at_start = in_quotes
        body_start = s + len('[and]-')
        # scan from body_start, skipping newlines, blockquote markers at line
        # starts ("> "), and a single opening quote (wrapped tokens like
        # `[and]-\n> "gloss (iast)"` or `[and]-\n"gloss (iast)"` start on the
        # next line)
        j = body_start
        while j < n:
            if text[j] in "\n \t":
                j += 1
                continue
            if text.startswith("> ", j):
                j += 2
                continue
            break
        if j < n and text[j] == '"':
            j += 1
        # find '(' before any separator
        po = -1
        k = j
        while k < n:
            ch = text[k]
            if ch == '(':
                po = k
                break
            if ch in ',;|:—\u2013">':
                break
            if text[k:k + len('[and]-')] == '[and]-':
                break
            k += 1
        if po != -1:
            co = text.find(')', po)
            if co != -1:
                iast = text[po + 1:co]
                gloss = text[j:po].strip()
                # find trailing quote / terminator to set raw end
                raw_end = co + 1
                if raw_end < n and text[raw_end] == '"':
                    raw_end += 1
                raw = text[s:raw_end]
                status = "PARSED"
                # update running quote state for the chars we consumed
                seg = text[body_start:raw_end]
                in_quotes = (seg.count('"') % 2 == 1) ^ q_at_start if False else None
                # simpler: recount quotes globally up to raw_end
                in_quotes = (text[:raw_end].count('"') % 2 == 1)
                records.append({
                    "id": f"{chunk_id}:L{line_id}:T{idx}",
                    "chunk_id": chunk_id,
                    "line_id": line_id,
                    "line_kind": line_kind,
                    "source_text": text,
                    "raw_fragment": raw,
                    "char_start": s,
                    "char_end": raw_end,
                    "lemma_iast": iast.strip(),
                    "literal_gloss": gloss,
                    "quoted": q_at_start,
                    "status": status,
                })
                continue
        # bare gloss: stop at separator, dash, quote, or next [and]- ;
        # newlines inside a wrapped token are skipped so `[and]-\n"gloss..."`
        # is captured as one token.
        j2 = j
        while j2 < n:
            ch = text[j2]
            if ch == "\n":
                j2 += 1
                continue
            if ch in ',;|:—\u2013">':
                break
            if text[j2:j2 + len('[and]-')] == '[and]-':
                break
            j2 += 1
        gloss = text[j:j2].strip().replace("\n", " ")
        raw_end = j2
        raw = text[s:raw_end].replace("\n", " ")
        in_quotes = (text[:raw_end].count('"') % 2 == 1)
        status = "AMBIGUOUS" if gloss else "FAILED"
        records.append({
            "id": f"{chunk_id}:L{line_id}:T{idx}",
            "chunk_id": chunk_id,
            "line_id": line_id,
            "line_kind": line_kind,
            "source_text": text,
            "raw_fragment": raw,
            "char_start": s,
            "char_end": raw_end,
            "lemma_iast": "",
            "literal_gloss": gloss,
            "quoted": q_at_start,
            "status": status,
        })
    return records


def reconstruct(records):
    """Best-effort reconstruction of the line from tokens (for round-trip check)."""
    # join with ", " as the source did
    out = []
    for r in records:
        gloss = r["literal_gloss"]
        if r["lemma_iast"]:
            token = f"[and]-{gloss} ({r['lemma_iast']})"
        else:
            token = f"[and]-{gloss}"
        if r["quoted"]:
            token = token.replace(f"[and]-{gloss}", f'[and]-"{gloss}"', 1)
        out.append(token)
    return ", ".join(out)


def classify_line(text):
    if text.lstrip().startswith(">"):
        return "verse_blockquote"
    if text.lstrip().startswith("#"):
        return "heading"
    if text.lstrip().startswith("---"):
        return "rule"
    if text.strip() == "":
        return "blank"
    return "prose"


def process_chunk(path: Path, out_prefix: Path, fmt="json", all_mode=False):
    chunk_id = path.stem
    records = []
    n_tokens = 0
    n_failed = 0
    n_ambig = 0
    n_parsed = 0
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    # Tokenize over the whole chunk as one continuous text so tokens wrapped
    # across newlines are captured, then map each token's char range back to
    # its line_id and line_kind via the line-offset table.
    offsets = []  # (line_no, start_char_in_joined, end_char_in_joined)
    acc = 0
    full = "\n".join(lines)
    for ln, text in enumerate(lines, 1):
        start = acc
        end = acc + len(text)
        acc = end + 1  # +1 for the '\n' separator
        offsets.append((ln, start, end))

    def line_of(pos):
        # find which line contains absolute char pos (allow pos at line end)
        for (ln, s, e) in offsets:
            if s <= pos < e:
                return ln
        return None

    # Reuse tokenize_line on the full text as a single "line", then remap line ids.
    recs_all = tokenize_line(full, 0, chunk_id, "prose")
    for r in recs_all:
        # remap
        ln = line_of(r["char_start"]) or 0
        if ln:
            r["line_id"] = ln
            r["line_kind"] = classify_line(lines[ln - 1])
            r["source_text"] = lines[ln - 1]  # keep only the containing line, not whole file
            r["id"] = f"{chunk_id}:L{ln}:T{r['id'].split(':T')[-1]}"
        n_tokens += 1
        if r["status"] == "PARSED":
            n_parsed += 1
        elif r["status"] == "AMBIGUOUS":
            n_ambig += 1
        else:
            n_failed += 1
        records.append(r)

    # write outputs
    if fmt in ("json", "both"):
        with open(str(out_prefix) + ".l0.jsonl", "w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    if fmt in ("tsv", "both"):
        with open(str(out_prefix) + ".l0.tsv", "w", encoding="utf-8") as fh:
            fh.write("id\tstatus\tlemma_iast\tliteral_gloss\tquoted\tline_id\tline_kind\n")
            for r in records:
                fh.write(f"{r['id']}\t{r['status']}\t{r['lemma_iast']}\t{r['literal_gloss']}\t{r['quoted']}\t{r['line_id']}\t{r['line_kind']}\n")

    # round-trip reconstruction is provided by raw_fragment + source_text per record;
    # a per-line reconstruction file is emitted only for the *single-chunk* debug run
    # (skipped in --all mode to save space).
    if not all_mode:
        with open(str(out_prefix) + ".l0.roundtrip.md", "w", encoding="utf-8") as fh:
            cur_line = None
            buf = []
            for r in records:
                if r["line_id"] != cur_line:
                    if buf:
                        fh.write(", ".join(buf) + "\n")
                    cur_line = r["line_id"]
                    buf = [f"{r['raw_fragment']}"]
                else:
                    buf.append(r["raw_fragment"])
            if buf:
                fh.write(", ".join(buf) + "\n")

    with open(str(out_prefix) + ".l0.report.txt", "w", encoding="utf-8") as fh:
        fh.write(f"chunk: {chunk_id}\n")
        fh.write(f"tokens: {n_tokens}\n")
        fh.write(f"  PARSED: {n_parsed}\n")
        fh.write(f"  AMBIGUOUS: {n_ambig}\n")
        fh.write(f"  FAILED: {n_failed}\n")
        fh.write(f"lines: {len(lines)}\n")
    return dict(chunk=chunk_id, tokens=n_tokens, parsed=n_parsed,
                ambiguous=n_ambig, failed=n_failed)


def main():
    args = sys.argv[1:]
    fmt = "json"
    if "--format" in args:
        fmt = args[args.index("--format") + 1]
    if "--all" in args:
        base = Path("translations/_stack/ipvv/02_t1")
        outdir = Path("translations/_stack/ipvv/l0")
        outdir.mkdir(exist_ok=True)
        total = dict(tokens=0, parsed=0, ambiguous=0, failed=0, chunks=0)
        for p in sorted(base.glob("chunkV*.md")):
            res = process_chunk(p, outdir / p.stem, fmt, all_mode=True)
            total["tokens"] += res["tokens"]
            total["parsed"] += res["parsed"]
            total["ambiguous"] += res["ambiguous"]
            total["failed"] += res["failed"]
            total["chunks"] += 1
            print(f"{p.stem}: {res['parsed']}P/{res['ambiguous']}A/{res['failed']}F "
                  f"({res['tokens']} tokens)")
        print("=" * 50)
        print(f"TOTAL: {total['parsed']}P/{total['ambiguous']}A/{total['failed']}F "
              f"({total['tokens']} tokens across {total['chunks']} chunks)")
        return
    # single chunk
    if not args or args[0].startswith("-"):
        print(__doc__)
        return
    path = Path(args[0])
    outdir = Path("translations/_stack/ipvv/l0")
    outdir.mkdir(exist_ok=True)
    res = process_chunk(path, outdir / path.stem, fmt, all_mode=False)
    print(f"{res['chunk']}: {res['parsed']}P/{res['ambiguous']}A/{res['failed']}F "
          f"({res['tokens']} tokens)")
    print(f"report: {outdir}/{path.stem}.l0.report.txt")


if __name__ == "__main__":
    main()
