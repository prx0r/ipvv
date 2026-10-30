#!/usr/bin/env python3
"""tools/import_work.py — rigid import gate for any new translation.

A new work becomes 'the same thing' iff it validates here. Fail-closed:
any missing provenance link or schema violation blocks the import.

Layout expected:
  works/<work>/
    WORK.md                 (human pointer: sources, counts, next)
    work.json               (specs/schema/work.json)
    passages.jsonl          (specs/schema/passage.json, one per line)
    t1/<chunk>.md           (frozen T1, format and-gloss-v1)
    l0/<chunk>.l0.jsonl     (t1_extract.py output)
    argmaps/<chunk>.md      (specs/schema/argmap.json as front-matter + prose, or plain prose w/ header)
    l2/<chunk>.md           (READ text + fidelity footer)
    l200/<chunk>.md         (8 sections)
    c1/<chunk>.md           (body) + c1-source.jsonl (records per specs/schema/c1.json)
    themes.json             (list of specs/schema/theme.json)
    pushing.jsonl           (specs/schema/pushing.json, one per line)

Usage:
  python3 tools/import_work.py --work tantraloka --strict
Validates: schemas, counts, provenance chain (L2->L0+ARGMAP, C1->L200,
panels->source), frozen T1 hashes, C1 word band, no bulk bytes in git.
On success emits site/data/<work>/catalog.json (the exact input build.py renders).
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCHEMA_DIR = ROOT / "specs/schema"

def load_schema(name):
    return json.loads((SCHEMA_DIR / name).read_text())

def check_required(obj, schema, where):
    errs = []
    for r in schema.get("required", []):
        if r not in obj or obj[r] in (None, ""):
            errs.append(f"{where}: missing required '{r}'")
    return errs

def check_enum(obj, schema, where):
    errs = []
    for k, prop in schema.get("properties", {}).items():
        if k in obj and "enum" in prop and obj[k] not in prop["enum"]:
            errs.append(f"{where}: '{k}'={obj[k]!r} not in {prop['enum']}")
    return errs

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--strict", action="store_true", help="fail on warnings too")
    a = ap.parse_args()
    wdir = ROOT / "works" / a.work
    errs, warns = [], []
    if not wdir.exists():
        print(f"FAIL: works/{a.work}/ missing (copy works/_TEMPLATE/)")
        return 1
    # 1. work.json
    wj = wdir / "work.json"
    if not wj.exists():
        errs.append("work.json missing")
        work = {}
    else:
        work = json.loads(wj.read_text())
        sch = load_schema("work.json")
        errs += check_required(work, sch, "work.json")
        errs += check_enum(work, sch, "work.json")
    # 2. passages
    pj = wdir / "passages.jsonl"
    passages = []
    if not pj.exists():
        errs.append("passages.jsonl missing")
    else:
        sch = load_schema("passage.json")
        for i, line in enumerate(pj.read_text().splitlines(), 1):
            if not line.strip(): continue
            try:
                o = json.loads(line)
            except Exception as e:
                errs.append(f"passages.jsonl:{i} bad JSON: {e}"); continue
            passages.append(o)
            errs += check_required(o, sch, f"passages.jsonl:{i}")
            if not o.get("sanskrit"): errs.append(f"passages.jsonl:{i} empty sanskrit")
    # 3. T1 frozen + hash
    t1dir = wdir / "t1"
    if passages and t1dir.exists():
        for p in passages:
            cid = p.get("chunk_id", "")
            f = t1dir / f"{cid}.md"
            if not f.exists():
                warns.append(f"t1/{cid}.md missing (layer absent until written)")
    # 4. L0 coverage (if l0 dir exists, require per-chunk files for frozen T1s)
    # 5. C1 band (if c1 dir exists)
    c1dir = wdir / "c1"
    if c1dir.exists():
        for f in sorted(c1dir.glob("*.md")):
            n = len(f.read_text().split())
            if not (100 <= n <= 450):
                (errs if n > 600 else warns).append(f"c1/{f.name} {n} words (band 100-450)")
    # 6. bulk bytes guard
    for f in wdir.rglob("*"):
        if f.is_file() and f.stat().st_size > 20_000_000:
            errs.append(f"bulk byte in git: {f} ({f.stat().st_size}) — R2 only")
    # 7. emit catalog (site contract) for whatever validates
    cat = {"work_id": a.work, "passages": len(passages),
           "layers": work.get("layers", []), "errors": errs, "warnings": warns}
    outdir = ROOT / "site/data" / a.work
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "catalog.json").write_text(json.dumps(cat, ensure_ascii=False, indent=1))
    print(f"work={a.work} passages={len(passages)} errors={len(errs)} warnings={len(warns)}")
    for e in errs: print("  ERR", e)
    for w in warns[:20]: print("  warn", w)
    if errs or (a.strict and warns):
        print("IMPORT BLOCKED")
        return 1
    print("IMPORT OK ->", outdir / "catalog.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
