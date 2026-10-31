#!/usr/bin/env python3
"""tools/build_glossary.py — glossary from C1 key_terms + curated core terms.

Reads published IPVV passages' c1_source.key_terms, cleans markdown fragments,
merges hand-written core definitions (site/data/glossary_core.json),
writes site/data/glossary.json: [{term, gloss, passages[], source}]
Usage: python3 tools/build_glossary.py
"""
from __future__ import annotations
import json, re, glob
from pathlib import Path

ROOT = Path(__file__).parent.parent

def clean(raw: str):
    t = re.sub(r"\*+", "", raw).strip()
    t = re.sub(r"^[-–—•\d.)\]]+\s*", "", t).strip()
    # split term from gloss at first — : ( ;
    m = re.split(r"\s+[—–-]\s*|\s*:\s*|\s+\(", t, maxsplit=1)
    term = m[0].strip().lower()
    gloss = m[1].strip() if len(m) > 1 else ""
    term = re.sub(r"^(the|a|an)\s+", "", term)
    term = term.strip(" .,;:'\"")
    if (len(term) < 3 or len(term) > 60 or not re.search(r"[a-z\u0101\u012b\u016b\u1e5b\u1e5d\u1e37\u1e39\u1e43\u1e47\u1e25\u1e62\u1e63]", term)
            or any(c in term for c in ")·\"“”(") or len(term.split()) > 4):
        return None, None
    return term, gloss[:220]

def main() -> None:
    entries: dict[str, dict] = {}
    for f in sorted(glob.glob("/root/patalacheckpoints/data/published/ipvv/pt-passage-*.json")):
        d = json.load(open(f))
        pid = d["id"].split(":")[-1].replace(".md", "")
        kt = (d.get("c1_source") or {}).get("key_terms", [])
        if isinstance(kt, str):
            kt = re.split(r"[,;\n]", kt)
        for raw in kt:
            if not isinstance(raw, str):
                continue
            for part in re.split(r"\n", raw):
                term, gloss = clean(part)
                if not term:
                    continue
                e = entries.setdefault(term, {"term": term, "gloss": "", "passages": [], "source": "c1-keyterms"})
                if gloss and len(gloss) > len(e["gloss"]):
                    e["gloss"] = gloss
                if pid not in e["passages"]:
                    e["passages"].append(pid)
    core_path = ROOT / "site/data/glossary_core.json"
    core = json.loads(core_path.read_text()) if core_path.exists() else []
    for c in core:
        t = c["term"].lower()
        e = entries.setdefault(t, {"term": c["term"], "gloss": "", "passages": [], "source": "curated"})
        e["gloss"] = c.get("gloss", e["gloss"])
        e["source"] = "curated"
        for p in c.get("passages", []):
            if p not in e["passages"]:
                e["passages"].append(p)
    out = sorted(entries.values(), key=lambda e: e["term"])
    (ROOT / "site/data/glossary.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"glossary: {len(out)} terms")

if __name__ == "__main__":
    raise SystemExit(main())
