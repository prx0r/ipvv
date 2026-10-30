#!/usr/bin/env python3
"""chunker.py — SOURCE passage cutter for any Sanskrit work.

Splits GRETIL/Muktabodha plain text into immutable SOURCE passages.
Default: split on āhnika/verse markers; override with --pattern.

Usage:
  python3 tools/chunker.py --in sources/X/raw.txt --work tantrasara --split ahnika --out sources/X/passages.jsonl
  python3 tools/chunker.py --in sources/Y/raw.txt --work ipvv --split verse --pattern "^abhts_" --out sources/Y/passages.jsonl
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

SPLITS = {
    "ahnika": r"(?=tantras[āa]ra,?\s+\S+\s+ahnika|abhts_\d+\.1\b)",
    "verse": r"(?=\n[^\n]{0,200}?\/\/\s*(?:abhts_|$))",
    "para": r"\n\n+",
}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--split", default="ahnika", choices=list(SPLITS))
    ap.add_argument("--pattern", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    text = Path(a.inp).read_text(encoding="utf-8", errors="replace")
    pat = a.pattern or SPLITS[a.split]
    parts = re.split(pat, text)
    parts = [p.strip() for p in parts if p.strip()]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for i, p in enumerate(parts):
            rec = {"work_id": a.work, "order": i, "locator": f"{a.split}-{i:03d}",
                   "sanskrit": p[:8000], "char_len": len(p), "source_edition": Path(a.inp).name}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"chunked {len(parts)} passages -> {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
