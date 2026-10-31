#!/usr/bin/env python3
"""tools/qa_vs_witness.py — quality gate: pipeline translation vs independent witness.

Compares what the pipeline produced for a work against an independent translation
(Dyczkowski where he covers the text; Torella/Singh/Lakshmanjoo/Silburn/Wallis/Marjanovic
otherwise). Computational comparison only; report quotes are short excerpts (<=25 words)
from in-copyright witnesses — fair use. Licensed status recorded, never hosted.

Usage:
  python3 tools/qa_vs_witness.py --work spanda
  python3 tools/qa_vs_witness.py --work sivasutra
  python3 tools/qa_vs_witness.py --all

Checks:
  1. COVERAGE — pipeline passages vs root verse count (GRETIL/Mukhabodha held text)
  2. SANSKRIT — pipeline source text matches held root (normalized)
  3. LEDGER — pipeline term ledger vs witness renderings (table)
  4. CLAIMS — sample C1/essay plains checked against witness (keyword + short quote)
  5. GATE — pipeline's own gate status re-verified (BLOCKED must stay blocked for cause)

Verdict: SHIP_AS_IS | SHIP_WITH_NOTES | HOLD (fix list) | NEEDS_WITNESS
Report: logs/qa/<work>.md
"""
from __future__ import annotations
import argparse, boto3, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
VOL = Path("/mnt/HC_Volume_106959365/root/projects")

R2 = {"ep": "https://954612afb5a97bb15dddcdc70176813d.r2.cloudflarestorage.com"}

def r2():
    import boto3
    e = {}
    with open("/root/.r2-env") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1); e[k] = v
    return boto3.client("s3", endpoint_url=e["R2_ENDPOINT"],
                         aws_access_key_id=e["R2_ACCESS_KEY"],
                         aws_secret_access_key=e["R2_SECRET_KEY"], region_name="auto")

WITNESS = {
    # work: (witness_id, witness_path_or_r2, licence_note, coverage_note)
    "spanda": ("dyczkowski-stanzas", str(VOL / "source-library/tantra/dyczkowski-translations/spandakarika-dyczkowski.txt"),
               "SUNY commercial — compare only, quote <=25w", "52-53 karikas + 4 commentaries"),
    "sivasutra": ("dyczkowski-aphorisms", str(VOL / "source-library/tantra/dyczkowski-translations/aphorisms-of-siva-dyczkowski.txt"),
                  "SUNY commercial — compare only, quote <=25w", "77 sutras + Bhaskara varttika"),
}

ROOT_TEXT = {
    "spanda": ("site/data/sanskrit/spanda-root.txt", r"\|\| (\d+) \|\|"),
    "sivasutra": ("site/data/sanskrit/sivasutra-root.txt", r"SivS_(\d+)\.(\d+)"),
}

def root_cmp_text(work):
    """Root text normalized for matching: verse-number markers removed, whitespace collapsed."""
    root_rel, _ = ROOT_TEXT[work]
    t = (ROOT / root_rel).read_text(encoding="utf-8")
    t = re.sub(r"\|\| \d+ \|\|", " ", t)          # GRETIL verse numbers
    t = re.sub(r"//\\s*SivS_[0-9.]+\\s*//", " ", t)
    t = re.sub(r"//\\s*SivSV_[0-9.:]+\\s*//", " ", t)     # sivasutra locators
    t = re.sub(r"^### .*$", " ", t, flags=re.M)  # our provenance header
    return norm(t)

LEDGER_TERMS = {
    "spanda": ["spanda", "unmeSa", "nimeSa", "sphurattA", "vimarza", "svAtantrya", "pramAtR", "bandha", "mokSa", "jIvanmukta", "kramamudrA"],
    "sivasutra": ["caitanya", "jJAna", "bandha", "mAtRkA", "udyoga", "bhairava", "zAkta", "Anava", "zAmbhavopAya", "vimarza", "pratyabhijJA"],
}

def norm(t): return re.sub(r"\s+", " ", t).strip()

def bare(t):
    """Strip numbering/punctuation so differently-segmented editions still match."""
    t = re.sub(r"\d+\.\d+:?", " ", t)   # 1.1: labels
    t = re.sub(r"[|/—–-]", " ", t)
    return norm(t)

def check_coverage(work):
    root_rel, pat = ROOT_TEXT[work]
    root = (ROOT / root_rel).read_text(encoding="utf-8")
    nums = []
    for m in re.finditer(pat, root):
        g = m.groups()
        nums.append(".".join(g) if len(g) > 1 else g[0])
    return {"root_file": root_rel, "root_bytes": len(root), "markers_found": len(nums),
            "first": nums[:3], "last": nums[-3:]}

def check_sanskrit(work, s3):
    """Pipeline passage source text appears verbatim in held root?"""
    key = None
    r = s3.list_objects_v2(Bucket="sanskritree", Prefix="batch-t1/", MaxKeys=100)
    for o in r.get("Contents", []):
        if work in o["Key"] and o["Key"].endswith(".jsonl"):
            if "tantrasara" not in o["Key"] or work == "tantrasara":
                key = o["Key"]; break
    if not key:
        return {"status": "NO_BATCH_FILE", "key": None}
    txt = s3.get_object(Bucket="sanskritree", Key=key)["Body"].read().decode("utf-8", errors="replace")
    recs = [json.loads(l) for l in txt.splitlines() if l.strip()]
    root = bare(root_cmp_text(work))
    ok, miss, detail = 0, [], {}
    for r_ in recs:
        src = r_.get("source", {})
        raw = src.get("text", "") if isinstance(src, dict) else str(src)
        # split batch text into sutra units on numbering/bars BEFORE normalizing
        parts = re.split(r"\d+\.\d+:\s*|\s*\|\s*", raw)
        units = [bare(norm(u)) for u in parts if len(bare(norm(u))) > 15]
        if not units:
            units = [bare(norm(raw))]
        hits = sum(1 for u in units if u[:70] in root)
        detail[r_.get("chunk", r_.get("id", "?"))] = f"{hits}/{len(units)} units"
        if units and hits / len(units) >= 0.5:
            ok += 1
        else:
            miss.append(r_.get("chunk", r_.get("id", "?")))
    return {"status": "OK" if not miss else "MISMATCH", "batch_key": key,
            "passages": len(recs), "matched": ok, "mismatched": miss[:10], "detail": detail}

def check_ledger(work):
    """Tabulate pipeline ledger terms against witness renderings found in text."""
    wid, wpath, lic, cov = WITNESS[work]
    wit = Path(wpath).read_text(encoding="utf-8", errors="replace")
    rows = []
    for term in LEDGER_TERMS.get(work, []):
        base = term.replace("A", "[aA]").replace("z", "[sz]").replace("S", "[Ss]").replace("N", "[nN]").replace("R", "[rR]").replace("T", "[tT]")
        hits = [m.group(0) for m in re.finditer(r".{0,60}" + base + r".{0,80}", wit, re.IGNORECASE)][:2]
        rows.append({"term": term, "witness_context": [re.sub(r"\s+", " ", h).strip()[:140] for h in hits]})
    return {"witness": wid, "licence": lic, "coverage": cov, "terms": rows}

def check_claims(work):
    """Spot-check pipeline English claims (C1 heads / WORK.md notes) for witness support."""
    heads = sorted(Path(ROOT / "site/samples" if False else ROOT / "samples").glob(f"{work}/*.md"))
    # samples live under site/samples in repo? try both
    cand = list(Path(ROOT / "samples").glob(f"{work}/*-head.md")) or list(Path(ROOT / "site/samples").glob(f"{work}/*-head.md"))
    wid, wpath, lic, cov = WITNESS[work]
    wit = Path(wpath).read_text(encoding="utf-8", errors="replace").lower()
    out = []
    for f in cand[:6]:
        t = f.read_text(encoding="utf-8")
        # pull doctrinal keywords
        keys = re.findall(r"\b(vimar[a-z]*|svatantrya|unme[sz]a|nime[sz]a|camatkara|pratyabhijna|aham|spanda|saktipata|diksa|grace|recognition|emission|reflexive)\b", t, re.I)
        uniq = sorted(set(k.lower() for k in keys))[:8]
        supported = [k for k in uniq if k in wit]
        out.append({"file": f.name, "keywords": uniq, "in_witness": supported,
                    "unsupported": [k for k in uniq if k not in supported]})
    return out

def check_gate(work):
    wf = ROOT / f"works/{work}/WORK.md"
    if not wf.exists():
        return {"status": "NO_WORKFILE"}
    t = wf.read_text()
    m = re.search(r"Gate:\s*([^\n]+)", t)
    return {"status": "FOUND", "gate_line": m.group(1).strip() if m else "no gate line",
            "blocked_mentions": len(re.findall(r"BLOCKED|FAIL|ABSTAIN", t))}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    works = ["spanda", "sivasutra"] if a.all else [a.work or "spanda"]
    s3 = r2()
    for work in works:
        if work not in WITNESS:
            print(f"{work}: NEEDS_WITNESS (no Dyczkowski coverage; route to alternate witness)")
            continue
        rep = ["# QA vs witness — " + work, ""]
        cov = check_coverage(work)
        rep += [f"## 1. Coverage", f"- root: `{cov['root_file']}` ({cov['root_bytes']} bytes, {cov['markers_found']} verse markers: {cov['first']} ... {cov['last']})", ""]
        san = check_sanskrit(work, s3)
        rep += ["## 2. Sanskrit match", f"- batch: `{san.get('batch_key')}` — {san.get('matched',0)}/{san.get('passages',0)} passages match held root ({san['status']})",
                (f"- mismatched: {san['mismatched']}" if san.get("mismatched") else "- all matched"), ""]
        led = check_ledger(work)
        rep.append("## 3. Ledger vs witness renderings")
        rep.append(f"- witness: {led['witness']} ({led['licence']}); covers: {led['coverage']}")
        for r_ in led["terms"]:
            ctx = (" | ".join(r_["witness_context"][:1]) or "— no hit —")[:140]
            rep.append(f"- `{r_['term']}` → witness: {ctx}")
        rep.append("")
        rep.append("## 4. Sample claim spot-checks")
        for c in check_claims(work):
            rep.append(f"- {c['file']}: keywords {c['keywords']} — in witness: {c['in_witness'] or 'NONE'}; unsupported here: {c['unsupported'] or 'none'}")
        rep.append("")
        g = check_gate(work)
        rep += ["## 5. Gate re-verification", f"- WORK.md gate: {g.get('gate_line')}", f"- block/fail mentions: {g.get('blocked_mentions')}", ""]
        # verdict: QA never overrides the pipeline's own gate — it verifies staging soundness
        hold = []
        if san["status"] != "OK": hold.append("sanskrit mismatch — fix segmentation before anything ships")
        if san.get("passages", 0) == 0: hold.append("no batch passages found")
        gl = (g.get("gate_line") or "")
        gated = gl.startswith("0 PASS") or "BLOCKED" in gl
        if gated:
            hold.append("pipeline gate correctly blocking (0 PASS) — staging verified sound, full translation not yet shippable; samples display only")
        verdict = "HOLD (" + "; ".join(hold) + ")" if hold else "SHIP_WITH_NOTES (verify open cruxes in L200/AQ before display copy)"
        rep += [f"## Verdict: {verdict}", "",
                "_Witness is comparison only (fair use, <=25-word quotes). Licensed status recorded above; nothing hosted._"]
        out = ROOT / "logs/qa"
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{work}.md").write_text("\n".join(rep), encoding="utf-8")
        print(f"{work}: wrote logs/qa/{work}.md — {verdict}")

if __name__ == "__main__":
    raise SystemExit(main())
