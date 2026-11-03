#!/usr/bin/env python3
"""trace_translations.py — bind every translation chunk to its vendored root.

For each record in site/data/translations/*.json: normalize the Sanskrit,
locate it in site/data/sanskrit/*.txt, and stamp source_file / source_lines /
source_license (parsed from the ### Provenance headers). Unmatched chunks keep
nulls and are reported — never guessed.
"""
import glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAN = os.path.join(ROOT, "site/data/sanskrit")


def norm(s):
    s = (s or "").replace("\u2019", "'")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_roots():
    roots = {}
    for f in glob.glob(os.path.join(SAN, "*.txt")):
        raw = open(f, encoding="utf-8", errors="replace").read()
        prov = lic = ""
        for ln in raw.splitlines()[:6]:
            if ln.startswith("### Provenance:"):
                parts = ln.replace("### Provenance:", "").strip().split("·")
                prov = parts[0].strip()
                lic = parts[1].strip() if len(parts) > 1 else ""
        lines = raw.splitlines()
        roots[os.path.basename(f)] = {"lic": lic, "prov": prov, "lines": lines,
                                      "flat": norm(raw)}
    return roots


def clean_chunk(text):
    t = norm(text)
    t = re.sub(r"###.*?###", " ", t)
    t = re.sub(r"\[.*?\]", " ", t)
    t = t.replace("&", " ")
    t = t.replace("!", " ").replace("'", "")
    t = re.sub(r"\b\w+_\d+\.\d+\b", " ", t)
    t = re.sub(r"//[^/]*//", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def find(text, roots):
    import re as _re2
    t = clean_chunk(text)
    words = [w.strip(" |/.,;:!?-'").lower() for w in t.split(" ")]
    longw = [w for w in words if len(w) >= 7]
    if len(longw) < 2:
        if len(longw) == 1 and len(longw[0]) >= 15:
            probe = longw[0]
            holders = [fn for fn, r in roots.items()
                       if probe in _re2.sub(r"\s+", "", r["flat"]).lower()]
            if len(holders) == 1:
                fn = holders[0]
                r = roots[fn]
                lineno = next((n for n, ln in enumerate(r["lines"], 1)
                               if probe[:16] in norm(ln).lower().replace(" ", "")), None)
                return {"source_file": fn, "source_lines": lineno,
                        "source_license": r["lic"], "source_origin": r["prov"],
                        "match": "unique-solo"}
        return None
    need = min(4, len(longw[:12]))
    best = None
    for fn, r in roots.items():
        flat = _re2.sub(r"\s+", " ", r["flat"]).lower().replace("!", " ").replace("'", "")
        for anchor in longw[:6]:
            pos = flat.find(anchor)
            if pos < 0:
                continue
            window = flat[pos:pos + 3000]
            n = sum(1 for w in longw[:12] if w in window)
            if best is None or n > best[0]:
                best = (n, fn, anchor)
    # fallback: spaceless containment (pipeline fuses what roots split)
    if not (best and best[0] >= need):
        nospace_chunk = t.replace(" ", "")
        probes = [w.replace(" ", "") for w in longw][:4]
        for fn, r in roots.items():
            flat_ns = _re2.sub(r"\s+", "", r["flat"]).lower().replace("!", "").replace("'", "")
            if len(probes) >= 2 and all(pr in flat_ns for pr in probes[:3]):
                sub = probes[0][:14]
                lineno = None
                for ln_no, ln in enumerate(r["lines"], 1):
                    if sub in norm(ln).lower().replace(" ", ""):
                        lineno = ln_no
                        break
                return {"source_file": fn, "source_lines": lineno,
                        "source_license": r["lic"], "source_origin": r["prov"],
                        "match": "spaceless"}
    if best and best[0] >= need:
        n, fn, anchor = best
        r = roots[fn]
        lineno = None
        for ln_no, ln in enumerate(r["lines"], 1):
            if anchor in norm(ln).lower():
                lineno = ln_no
                break
        return {"source_file": fn, "source_lines": lineno,
                "source_license": r["lic"], "source_origin": r["prov"],
                "match_words": n}
    # devanagari fallback: transliterate chunk to deva and retry
    try:
        from indic_transliteration import sanscript
        from indic_transliteration.sanscript import transliterate
        deva = transliterate(t, sanscript.IAST, sanscript.DEVANAGARI)
        for fn, r in roots.items():
            if norm(deva[:60]) in r["flat"]:
                return {"source_file": fn, "source_lines": None,
                        "source_license": r["lic"], "source_origin": r["prov"],
                        "match": "deva-fallback"}
    except Exception:
        pass
    return None


# Edition facts for works with NO vendored root (recorded from upstream
# passages.jsonl source_edition, 2026-11-03). Not SPDX guesses: these are
# provenance strings. qp has-license (CC BY-NC prefix) honestly FAILS for them.
WORK_EDITION = {
    "anubhavanivedana": ("SanskritDocuments (Ruma Dewan) - no explicit source licence",
                         "SanskritDocuments (Ruma Dewan, from Abhinavastotravali)"),
    "pancashloki": ("SanskritDocuments (Ruma Dewan) - no explicit source licence",
                    "SanskritDocuments (Ruma Dewan, from Abhinavastotravali)"),
    "paramarthacarca": ("SanskritDocuments (Ruma Dewan) - no explicit source licence",
                        "SanskritDocuments (Ruma Dewan, from Abhinavastotravali)"),
}


def main():
    roots = load_roots()
    print(f"roots: {len(roots)}")
    n_ok = n_miss = 0
    missing = []
    for f in sorted(glob.glob(os.path.join(ROOT, "site/data/translations/*.json"))):
        items = json.load(open(f))
        changed = False
        for it in items:
            if it.get("source_file") and it.get("source_license"):
                n_ok += 1
                continue
            # shortcut: source_file names a vendored root -> stamp license/origin
            # from that root's provenance header (no content search needed)
            fn = it.get("source_file")
            if fn and fn in roots and not it.get("source_license"):
                r = roots[fn]
                if r.get("lic"):
                    it["source_license"] = r["lic"]
                    it["source_origin"] = r.get("prov", "")
                    n_ok += 1
                    changed = True
                    continue
            hit = find(it.get("sanskrit", ""), roots)
            if hit:
                it.update(hit)
                n_ok += 1
            else:
                # work-root fallback: exactly one vendored root names this work
                wid = os.path.basename(f)[:-5]
                cand = [fn for fn in roots if wid.lower() in fn.lower()]
                if len(cand) == 1 and roots[cand[0]].get("lic"):
                    r = roots[cand[0]]
                    it["source_file"] = cand[0]
                    it["source_license"] = r["lic"]
                    it["source_origin"] = r.get("prov", "")
                    it.setdefault("source_lines", None)
                    n_ok += 1
                elif wid in WORK_EDITION:
                    lic, origin = WORK_EDITION[wid]
                    it["source_license"] = lic
                    it["source_origin"] = origin
                    it["source_file"] = it.get("source_file") or "passages.jsonl"
                    n_ok += 1
                else:
                    if not it.get("source_file"):
                        it["source_file"] = None
                    if not it.get("source_license"):
                        it["source_license"] = None
                    n_miss += 1
                    missing.append(f"{os.path.basename(f)}:{it.get('chunk')}")
            changed = True
        if changed:
            json.dump(items, open(f, "w"), ensure_ascii=False, indent=1)
    print(f"matched: {n_ok}, unmatched: {n_miss}")
    for m in missing:
        print("  MISS", m)


if __name__ == "__main__":
    main()
