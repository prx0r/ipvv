#!/usr/bin/env python3
"""tools/audio_r2_index.py — commit R2's audio inventory so verify_site can
check the real storage contract offline.

Chant audio lives in R2 (public bucket `svread-audio`, keys `audio/<work>/<id>.mp3`),
NOT in git — see .gitignore. verify_site's mp3 check therefore accepts:
  local static-audio OR local dist/audio OR this index.
Refresh: python3 tools/audio_r2_index.py   (writes site/data/audio-r2.json)
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def main():
    env = {}
    with open(os.path.expanduser("~/.r2-env")) as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    import boto3
    s3 = boto3.client("s3",
        endpoint_url=env.get("NEW_ICY_R2_ENDPOINT") or env.get("R2_ENDPOINT"),
        aws_access_key_id=env.get("NEW_ICY_R2_ACCESS_KEY_ID") or env.get("R2_ACCESS_KEY"),
        aws_secret_access_key=env.get("NEW_ICY_R2_SECRET_ACCESS_KEY") or env.get("R2_SECRET_KEY"),
        region_name="auto")
    keys, tok = [], None
    while True:
        kw = {"Bucket": "svread-audio", "MaxKeys": 1000}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            k = o["Key"]
            if k.startswith("audio/") and k.endswith(".mp3"):
                keys.append(k[len("audio/"):-len(".mp3")])   # "<work>/<id>"
        if not r.get("IsTruncated"):
            break
        tok = r.get("NextContinuationToken")
    out = os.path.join(ROOT, "site/data/r2audio-index.json")
    data = {"bucket": "svread-audio", "count": len(keys), "keys": sorted(keys)}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"indexed {len(keys)} R2 mp3s -> {out}")

if __name__ == "__main__":
    main()
