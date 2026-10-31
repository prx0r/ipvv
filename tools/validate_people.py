#!/usr/bin/env python3
"""tools/validate_people.py — every master + scholar bio validates the canonical person schema.

Usage: python3 tools/validate_people.py [--strict]
Checks: specs/schema/person.json required fields, id slug, dates.note present,
kind/status vocab, holdings paths exist (warn), works_<id>.json present for kind=master.
Exit 1 on error (or warning with --strict).
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
KIND = {"master", "scholar", "teacher", "lineage"}
STATUS = {"living", "active", "historical", "lineage", "traditional", "disputed"}

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def main() -> int:
    strict = "--strict" in sys.argv
    errs, warns = [], []
    people = []
    for f in sorted((ROOT / "site/data/authors").glob("*.json")):
        people.append((f.stem, load(f), "authors/"))
    for aid in ("abhinavagupta",):
        f = ROOT / "site/data/author.json"
        if f.exists() and not (ROOT / "site/data/authors/abhinavagupta.json").exists():
            people.append((aid, load(f), ""))
    seen = set()
    for aid, p, where in people:
        tag = f"{where}{aid}"
        for r in ("id", "kind", "name", "status", "summary", "dates"):
            if r not in p or not p[r]:
                errs.append(f"{tag}: missing required '{r}'")
        if p.get("id") != aid and p.get("id"):
            warns.append(f"{tag}: filename/id mismatch ({p.get('id')})")
        if p.get("kind") not in KIND:
            errs.append(f"{tag}: kind '{p.get('kind')}' not in {sorted(KIND)}")
        if p.get("status") not in STATUS:
            errs.append(f"{tag}: status '{p.get('status')}' not in {sorted(STATUS)}")
        d = p.get("dates", {})
        if not d.get("flourished") or not d.get("note"):
            errs.append(f"{tag}: dates need flourished + note (honesty flag)")
        if not p.get("summary"):
            errs.append(f"{tag}: missing summary")
        elif len(p["summary"]) > 300:
            warns.append(f"{tag}: summary {len(p['summary'])} chars (cap 300)")
        for h in p.get("holdings", []):
            if h.startswith(("research-library/", "tantra/", "acquisitions/", "deitybody/", "artifacts/", "texts-clean/")):
                base = Path("/mnt/HC_Volume_106959365/root/projects")
                cand = [base / h, base / "source-library/tantra" / h, base / ("research-library/" + h.split("research-library/", 1)[-1]) if "research-library" in h else None]
                if not any(c and c.exists() for c in cand if c):
                    warns.append(f"{tag}: holding not found on volume: {h}")
        if p.get("kind") == "master":
            w = ROOT / "site/data/works.json" if aid == "abhinavagupta" else ROOT / "site/data" / f"works_{aid}.json"
            if not w.exists():
                errs.append(f"{tag}: master without works file {w.name}")
        if aid in seen:
            errs.append(f"duplicate id {aid}")
        seen.add(aid)
    # scholars file entries validate as persons too (kind=scholar; works file not required)
    S = load(ROOT / "site/data/scholars.json")
    for s in S:
        tag = f"scholars/{s.get('id')}"
        for r in ("id", "kind", "name", "status", "summary", "dates"):
            if not s.get(r):
                errs.append(f"{tag}: missing '{r}'")
        if s.get("kind") != "scholar":
            errs.append(f"{tag}: kind must be scholar")
        if s.get("status") not in STATUS:
            errs.append(f"{tag}: status '{s.get('status')}' not in {sorted(STATUS)}")
        if not s.get("bio"):
            warns.append(f"{tag}: no bio paragraph yet")
    print(f"people={len(people)} scholars={len(S)} errors={len(errs)} warnings={len(warns)}")
    for e in errs: print("  ERR", e)
    for w in warns[:25]: print("  warn", w)
    if errs or (strict and warns):
        print("VALIDATION BLOCKED")
        return 1
    print("PEOPLE OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
