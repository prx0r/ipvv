#!/usr/bin/env python3
"""Authored chant audio -> site: wav to mp3 + per-work recitation JSON.

Reads kashaudio renders (AI chant, the deliverable voice — never trad recordings,
which are ear-reference only) + word timings, emits:
  site/static-audio/<work>/<id>.mp3   (committed; build copies to dist/audio/)
  site/data/audio-<work>.json          (verses + padas + iast + timings)

Works configured below must have: shard stotras/<shard>.json, wavs dir, word_timings.json.
English is merged later at page build from translations JSON (PASS only) — never here.
"""
import json, subprocess, sys
from pathlib import Path

KASH = Path("/root/kashaudio")
ROOT = Path(__file__).resolve().parent.parent  # /root/ipvv
OUT_AUDIO = ROOT / "site/static-audio"
OUT_DATA = ROOT / "site/data"

WORKS = {
    # site-work: (shard, wavdir, id-prefix, wav-suffix)
    "bhairavastava": ("bhairavastava.json", "bhairavastava", "bhairava_", {10: "bhairava_10_phala"}),
    "anuttarashtika": ("anuttarashtika.json", "anuttarashtika", "anuttara_", {}),
}

def main():
    for work, (shard_fn, wavdir, prefix, special) in WORKS.items():
        shard = json.loads((KASH / "stotras" / shard_fn).read_text())
        wt = json.loads((KASH / wavdir / "word_timings.json").read_text())
        wtmap = {v["id"]: v for v in wt}
        adir = OUT_AUDIO / work
        adir.mkdir(parents=True, exist_ok=True)
        verses = []
        for n, v in enumerate(shard, 1):
            vid = v["id"]
            wavname = special.get(n, f"{prefix}{n:02d}")
            wav = KASH / wavdir / f"{wavname}.wav"
            if not wav.exists():
                print(f"SKIP {work} {vid}: no wav {wav}", file=sys.stderr)
                continue
            mp3 = adir / f"{vid}.mp3"
            if not mp3.exists() or wav.stat().st_mtime > mp3.stat().st_mtime:
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav),
                                "-codec:a", "libmp3lame", "-b:a", "128k", str(mp3)], check=True)
            tw = wtmap.get(vid, {})
            words = [{"w": w["w"], "on": w["t_on"], "off": w["t_off"], "pada": w.get("pada", 0)}
                     for w in tw.get("words", [])]
            # iast per pada from word romans
            padas_iast = []
            for pi in range(len(v["padas"])):
                padas_iast.append(" ".join(w["r"] for w in tw.get("words", []) if w.get("pada", 0) == pi))
            verses.append({"id": vid, "n": n, "meter": v.get("meter", ""),
                           "padas": v["padas"], "iast": padas_iast,
                           "mp3": f"/audio/{work}/{vid}.mp3",
                           "dur": tw.get("dur", 0), "words": words,
                           "mms": round(sum(w.get("mms", 0) for w in tw.get("words", [])) / max(1, len(tw.get("words", []))), 3)})
        (OUT_DATA / f"audio-{work}.json").write_text(
            json.dumps({"work": work, "verses": verses}, ensure_ascii=False, indent=1))
        nbytes = sum((OUT_AUDIO / work / f"{v['id']}.mp3").stat().st_size for v in verses)
        print(f"{work}: {len(verses)} verses, mp3 {nbytes//1024}KB total")

if __name__ == "__main__":
    main()
