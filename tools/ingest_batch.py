#!/usr/bin/env python3
"""tools/ingest_batch.py — pull pipeline batch-t1 R2 files into site inputs.

Only PASS-gated passages carry English onto the site. BLOCKED passages ship as
Sanskrit + gate status (never English-as-translation: fail-closed).

Usage: python3 tools/ingest_batch.py [--work bhairavastava] [--all]
Writes: site/data/translations/<work>.json
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).parent.parent

def r2():
    import boto3
    env = {}
    with open("/root/.r2-env") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1); env[k] = v
    import boto3 as _b
    return _b.client("s3", endpoint_url=env["R2_ENDPOINT"],
                     aws_access_key_id=env["R2_ACCESS_KEY"],
                     aws_secret_access_key=env["R2_SECRET_KEY"], region_name="auto")

def work_files(s3):
    r = s3.list_objects_v2(Bucket="sanskritree", Prefix="batch-t1/", MaxKeys=200)
    return sorted(o["Key"] for o in r.get("Contents", []))

def ingest(s3, key, work):
    txt = s3.get_object(Bucket="sanskritree", Key=key)["Body"].read().decode("utf-8", errors="replace")
    out = []
    for line in txt.splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        g = r.get("gate", {})
        passed = (g.get("deterministic_gate") if isinstance(g, dict) else g) == "PASS"
        blocking = g.get("blocking", []) if isinstance(g, dict) else []
        src = r.get("source", {})
        item = {
            "chunk": r.get("chunk", r.get("id", "?")),
            "verses": r.get("verses", ""),
            "sanskrit": src.get("text", "") if isinstance(src, dict) else str(src),
            "gate": "PASS" if passed else "BLOCKED",
            "blocking": blocking,
            "model": r.get("model", ""),
            "date": r.get("date", ""),
            "work_id": r.get("work_id", ""),
            "ahnika": r.get("ahnika", ""),
            "immutable_id": r.get("immutable_id", ""),
            "status": r.get("status", ""),
            "checks": g.get("checks", {}) if isinstance(g, dict) else {},
        }
        if passed:
            item["l1"] = r.get("l1_text", "")
            item["l2"] = r.get("l2_text", "")
        out.append(item)
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=None)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    s3 = r2()
    keys = work_files(s3)
    # group batch files by work: batch-t1/YYYY-MM-DD-<work>-raw.jsonl, tantrasara aXX separate
    groups: dict[str, list[str]] = {}
    for k in keys:
        base = k.split("/")[-1]
        parts = base.replace(".jsonl", "").split("-")
        # 2026-10-30-<work...>-raw  or 2026-10-30-tantrasara-a01-raw
        rest = parts[3:-1] if len(parts) > 4 else parts[3:4]
        # tantrasara-aNN files belong to the tantrasara work
        w = "tantrasara" if rest and rest[0] == "tantrasara" else "-".join(rest)
        groups.setdefault(w, []).append(k)
    if a.work and not a.all:
        groups = {a.work: groups.get(a.work, [])}
    dest = ROOT / "site/data/translations"
    dest.mkdir(parents=True, exist_ok=True)
    for w, ks in sorted(groups.items()):
        if not ks:
            print(f"{w}: no batch files — skip"); continue
        items = []
        for k in sorted(ks):
            items.extend(ingest(s3, k, w))
        (dest / f"{w}.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        n_pass = sum(1 for i in items if i["gate"] == "PASS")
        print(f"{w}: {len(items)} passages, {n_pass} PASS -> site/data/translations/{w}.json")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
