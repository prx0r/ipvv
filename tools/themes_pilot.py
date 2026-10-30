#!/usr/bin/env python3
"""
THEMES PILOT v2 — the controlled experiment (corrected).

FIX from v1: shared BODY terms create a near-complete graph (noise). The structured
signal must be (a) curated "See also" edges + (b) shared KEY TERMS (the Terms: field),
NOT shared body words. This version:
  - semantic: Jaccard on KEY TERMS + body (the lexical affinity)
  - structured: curated See-also edges (1.0) + shared KEY TERMS (0.7)
  - hybrid: weighted combination
And it outputs the EXPECTED-RELATIONS reference sheet + runs the three-way ablation
for blind review.
"""
import re, glob, os
from collections import defaultdict

C1DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "c1", "read")

PILOT = ['V1D','V2A','V2B','V2C','V2L','V2O','V2S','V1K','V1E','V2D','V2E','V3C',
         'V3D','V3E','V3B','V3I','V3G','V3H','V3A','V2H','V2I','V2K','V2F','V2G','V3M']

# the curated See-also edges (manually verified from the files above)
CURATED = {
 'V1D':['V2A','V2B'], 'V2A':['V2B','V2P'], 'V2B':['V2A','V2C','V1L'],
 'V2C':['V1L','V2B'], 'V2L':['V2C','V2O'], 'V2O':['V2P','V2S'],
 'V2S':['V2O','V2P'], 'V1K':['V1L','V2C'], 'V1E':['V1D','V2L'],
 'V2D':['V2E','V1E'], 'V2E':['V2D','V2F'], 'V3C':['V3D','V2D'],
 'V3D':['V3C','V3E','V2M'], 'V3E':['V3D','V3I'], 'V3B':['V3C','V3D'],
 'V3I':['V3G','V2S'], 'V3G':['V3H','V3I'], 'V3H':['V3G','V3I'],
 'V3A':['V3G','V3I'], 'V2H':['V2I','V2S'], 'V2I':['V2H','V2J'],
 'V2K':['V2J','V2H'], 'V2F':['V2G','V1L'], 'V2G':['V2F','V2D'],
 'V3M':['V3L','V2M'],
}

def parse_c1s():
    c1s = {}
    for f in sorted(glob.glob(os.path.join(C1DIR, "c1_V*.md"))):
        t = open(f).read()
        base = os.path.basename(f).replace("c1_", "").replace(".md", "")
        cid = base.split("-")[0]
        body = " ".join(re.findall(r"\n> ?(.*)", t))
        terms = re.search(r"\*\*Terms:\*\* ?(.*?)(?=\n\n|\Z)", t, re.S)
        c1s[cid] = {"body": body, "terms": terms.group(1) if terms else ""}
    return c1s

def toks(s):
    return set(w.lower() for w in re.findall(r"[a-zā-ḥ]+", s))

def jaccard(a, b):
    u = a | b
    return len(a & b) / max(1, len(u))

def main():
    c1s = parse_c1s()
    termset = {c: toks(c1s[c]["terms"]) for c in PILOT}
    bodytok = {c: toks(c1s[c]["body"]) for c in PILOT}
    # key terms are in the Terms field; use them for shared-term edges
    # (Jaccard on key terms = semantic; explicit curated = structured)

    print("="*70)
    print("THEMES PILOT v2 — expected-relations reference (NOT a partition)")
    print("="*70)
    expectations = [
        ("EXPECT", "V2A ↔ V2O", "continuity / recognition (memory + orderless support)"),
        ("EXPECT", "V2L ↔ V2C", "non-objectified I-awareness"),
        ("EXPECT", "V2L ↔ V2O", "the non-constructed self / its support"),
        ("EXPECT", "V3G ↔ V3H ↔ V3I", "causality as the knower's agency (the causal cluster)"),
        ("EXPECT", "V2A ↔ V2B ↔ V2C", "memory / self-cognition cluster"),
        ("EXPECT", "V2D ↔ V2E ↔ V3C", "pramāṇa / manifestation cluster"),
        ("EXPECT", "V2H ↔ V2I ↔ V2K", "vimarśa / language cluster"),
        ("EXPECT OVERLAP", "V2O", "→ recognition, → continuity, → subjectivity (multi-theme)"),
        ("EXPECT OVERLAP", "V2L", "→ self-awareness, → recognition (multi-theme)"),
        ("EXPECT SEPARATION", "V3B vs V2B", "similar 'one-and-many' vocabulary, different doctrinal move (action vs cognition)"),
        ("EXPECT CONTRAST", "V3I vs V2S", "difference-real vs unity — the same material read oppositely"),
    ]
    for t, pair, reason in expectations:
        print(f"{t:16} {pair:<22} {reason}")

    print("\n" + "="*70)
    print("THREE-WAY ABLATION — candidate neighborhoods (blind review)")
    print("="*70)
    for mode in ["semantic", "structured", "hybrid"]:
        print(f"\n--- MODE: {mode} ---")
        print(f"{'C1':6} top-5 neighbors")
        for c in PILOT:
            scores = []
            for o in PILOT:
                if o == c: continue
                s = jaccard(termset[c], termset[o])          # key-term Jaccard
                if mode == "semantic":
                    w = s
                elif mode == "structured":
                    e = 1.0 if (o in CURATED.get(c, []) or c in CURATED.get(o, [])) else 0.0
                    w = 0.8*e + 0.2*round(s,1)               # curated edges dominate
                else: # hybrid
                    e = 1.0 if (o in CURATED.get(c, []) or c in CURATED.get(o, [])) else 0.0
                    w = 0.4*e + 0.6*s
                scores.append((o, round(w,2)))
            top = ", ".join(f"{o}({w})" for o,w in sorted(scores, key=lambda x:-x[1])[:5])
            print(f"{c:6} {top}")

    # the hybrid-graph edges with weights (for the explainability test)
    print("\n=== HYBRID GRAPH edges (V2A, V2L, V2O — the overlap test) ===")
    for c in ['V2A','V2L','V2O','V2S']:
        print(f"{c}: curated→{CURATED.get(c,[])}")

if __name__ == "__main__":
    main()
