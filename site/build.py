#!/usr/bin/env python3
"""site/build.py — static display site for formally-done translation work.

Same shell for every work. Displays only what formally exists.
Missing layers render greyed (planned), never invented.

Usage: python3 site/build.py [--works ipvv,vbt,tantrasara]
Output: site/dist/ (deploy to Cloudflare Pages, like shivastotravali.pages.dev)
"""
import json, html, sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
PATALA = Path("/root/patalacheckpoints")
VOL = Path("/mnt/HC_Volume_106959365/root/projects")

CSS = """body{{font-family:Georgia,serif;max-width:720px;margin:0 auto;padding:1rem;color:#222}}
header{{text-align:center;border-bottom:1px solid #ddd;margin-bottom:1rem}}
h1{{font-weight:400}}.sub{{color:#666;font-size:.9rem}}
.dev{{font-size:1.4rem;line-height:2}}.iast{{color:#8a6d1b}}.en{{line-height:1.6}}
.depth{{margin:.6rem 0}}.depth button{{margin-right:.4rem;padding:.4rem .8rem;border-radius:999px;border:1px solid #ccc;background:#f7f4ec;cursor:pointer}}
.depth button.on{{background:#222;color:#fff}}
.panel{{border:1px solid #e5e0d0;border-radius:12px;padding:1rem;margin:.6rem 0;background:#fffdf7}}
.missing{{opacity:.4}}.idx a{{display:block;padding:.5rem 0;border-bottom:1px solid #eee;text-decoration:none;color:#222}}
.nav{{margin:1rem 0;font-size:.9rem}}.nav a{{margin-right:1rem}}
"""

TMPL = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title><style>""" + CSS + """</style></head><body>
<header><h1>{h1}</h1><div class="sub">{sub}</div></header>
<div class="nav"><a href="/index.html">works</a><a href="/{work}/index.html">{work}</a>
<a href="/{work}/themes.html">themes</a><a href="/{work}/pushing.html">pushing</a></div>
{body}</body></html>"""

def tabs(panels):
    btns, divs = [], []
    for i, (name, body, ok) in enumerate(panels):
        cls = "" if ok else "missing"
        on = "on" if i == 0 and ok else ""
        btns.append(f'<button class="{on}" data-p="{i}">{name}{"" if ok else " · soon"}</button>')
        divs.append(f'<div class="panel {cls}" data-p="{i}" style="display:{"block" if i==0 else "none"}">{body or "<i>not yet formally done — never invented</i>"}</div>')
    js = """<script>document.querySelectorAll('.depth button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.depth button').forEach(x=>x.classList.remove('on'));b.classList.add('on');document.querySelectorAll('.panel').forEach(p=>p.style.display=p.dataset.p===b.dataset.p?'block':'none')})</script>"""
    return '<div class="depth">' + "".join(btns) + "</div>" + "".join(divs) + js

def esc(s): return html.escape(s or "")

def build_ipvv():
    src = sorted((PATALA / "data/published/ipvv").glob("pt-passage-*.json"))
    items = [json.loads(p.read_text()) for p in src]
    out = DIST / "ipvv"; out.mkdir(parents=True, exist_ok=True)
    links = []
    for d in items:
        pid = d["id"].split(":")[-1].replace(".md", "")
        src_txt = (d.get("source") or {}).get("text", "") if isinstance(d.get("source"), dict) else ""
        l2 = d.get("l2_text") or ""
        c1 = d.get("c1") or {}
        c1b = c1.get("body", "") if isinstance(c1, dict) else str(c1)
        body = tabs([
            ("ORIGINAL", f'<div class="dev">{esc(src_txt[:2000])}</div>', bool(src_txt)),
            ("READ", f'<div class="en">{esc(l2[:4000])}</div>', bool(l2)),
            ("GUIDE", None, False),
            ("STUDY", f'<div class="en">{esc(c1b[:3000])}</div>', bool(c1b)),
            ("CRITICAL", f'<div class="en">vol {esc(d.get("vol",""))} · {esc(d.get("chunk",""))} · {esc(d.get("immutable_id",""))}</div>', True),
        ])
        (out / f"{pid}.html").write_text(TMPL.format(title=pid, h1=pid, sub="IPVV · " + esc(d.get("vol", "")), work="ipvv", body=body))
        links.append(f'<a href="/ipvv/{pid}.html">{esc(pid)}</a>')
    (out / "index.html").write_text(TMPL.format(title="IPVV", h1="Īśvarapratyabhijñāvivṛtivimarśinī",
        sub=f"{len(items)} passages · Sanskrit → READ → STUDY · GUIDE soon", work="ipvv",
        body='<div class="idx">' + "".join(links) + "</div>"))
    # themes
    try:
        cl = json.loads((PATALA / "data/published/ipvv/clusters.json").read_text())
        cls = cl.get("clusters", [])
        tb = "".join(f'<div class="panel"><b>{esc(c.get("cluster_id",""))}</b> · {c.get("size",0)} members · coherence {c.get("coherence","")} <br/>{esc(", ".join(c.get("member_c1_ids",[])[:12]))}</div>' for c in cls)
    except Exception as e:
        tb = f"<i>themes pending: {esc(str(e))}</i>"
    (out / "themes.html").write_text(TMPL.format(title="IPVV themes", h1="Themes", sub="overlapping, never partition", work="ipvv", body=tb))
    # pushing stub (prose scaffolds on volume; parsed records next)
    pb = '<div class="panel">Pushing = hound the text with why, text answers first. Full Q→GEM index parses next via <i>pushing.py</i>. Sources on volume: <i>research-library/recognition/pushing-ipvv/</i>, <i>pushing-tantraloka/</i>.</div>'
    (out / "pushing.html").write_text(TMPL.format(title="IPVV pushing", h1="Pushing", sub="Q→GEM deep-dives at varying depth", work="ipvv", body=pb))
    return len(items)

def build_vbt():
    d = json.load(open(VOL / "source-library/tantra/lakshmanjoo/vb_lakshmanjoo.json"))
    vs = d.get("verses", [])
    bd = json.load(open("/root/deitybody/site/frameworks/vbt/body-dharanas.json"))
    seats = {x.get("v"): x for x in bd.get("dharanas", [])}
    out = DIST / "vbt"; out.mkdir(parents=True, exist_ok=True)
    links = []
    for v in vs[:145]:
        n = v.get("number")
        skt, en = v.get("sanskrit", ""), v.get("english", "")
        seat = seats.get(n, {})
        body = tabs([
            ("ORIGINAL", f'<div class="dev">{esc(skt)}</div>', bool(skt)),
            ("READ", f'<div class="en">{esc(en[:2000])}</div>', bool(en)),
            ("GUIDE", None, False),
            ("STUDY", f'<div class="en">attention-seat: {esc(seat.get("locus","—"))} · do: {esc(seat.get("do","—"))}</div>', bool(seat)),
            ("CRITICAL", f'<div class="en">VBT verse {n} · Lakshmanjoo/KSTS</div>', True),
        ])
        (out / f"v{n}.html").write_text(TMPL.format(title=f"VBT {n}", h1=f"Verse {n}", sub="Vijñānabhairava", work="vbt", body=body))
        links.append(f'<a href="/vbt/v{n}.html">verse {n}</a>')
    (out / "index.html").write_text(TMPL.format(title="VBT", h1="Vijñānabhairava Tantra",
        sub=f"{len(vs)} verses · catalog of entries, not graded course", work="vbt", body='<div class="idx">' + "".join(links) + "</div>"))
    (out / "themes.html").write_text(TMPL.format(title="VBT themes", h1="Themes", sub="by upaya/tattva (sanskrithelp mapping)", work="vbt",
        body='<div class="panel">Breath · Void/gap · Light · Sound/mantra · Senses · Energy/kundalini · Sexual yoga · Direct recognition. Full mapping: <i>sanskrithelp/data/rag/vijnana-bhairava-mapping.md</i>.</div>'))
    (out / "pushing.html").write_text(TMPL.format(title="VBT pushing", h1="Pushing", sub="liminal states, goddess, gaps", work="vbt",
        body='<div class="panel">Start: V75 edge-of-sleep (para devi prakasate), V24 heart↔12-end, V50 any 12-end. Q→GEM index next.</div>'))
    return len(vs)

def build_tantrasara():
    e0 = json.load(open("/tmp/tantrasara/build/canon/essay0.json"))
    units = e0.get("units", {})
    out = DIST / "tantrasara"; out.mkdir(parents=True, exist_ok=True)
    links = []
    for k, u in units.items():
        body = tabs([
            ("ORIGINAL", f'<div class="en">span {esc(u.get("text_span",""))} · lines {esc(str(u.get("text_line_range","")))}<br/>{esc(u.get("text",""))}</div>', bool(u.get("text"))),
            ("READ", f'<div class="en">{esc(u.get("plain",""))}</div>', bool(u.get("plain"))),
            ("GUIDE", None, False),
            ("STUDY", f'<div class="en">Q: {esc(u.get("question",""))}</div>', True),
            ("CRITICAL", f'<div class="en">alternates: {esc(str(u.get("alternates",""))[:500])}</div>', True),
        ])
        (out / f"q{k}.html").write_text(TMPL.format(title=f"TS Q{k}", h1=esc(u.get("question", f"Q{k}")), sub="Tantrasara essay-0", work="tantrasara", body=body))
        links.append(f'<a href="/tantrasara/q{k}.html">{esc(u.get("question",""))}</a>')
    (out / "index.html").write_text(TMPL.format(title="Tantrasara", h1="Tantrasāra",
        sub=f"{len(units)} questions · verbatim → plain · audio pending", work="tantrasara", body='<div class="idx">' + "".join(links) + "</div>"))
    (out / "themes.html").write_text(TMPL.format(title="TS themes", h1="Themes", sub="upaya ladder, saktipata, uccara", work="tantrasara",
        body='<div class="panel">Next: run ahnika-11 through full pipe, cluster C1s like IPVV.</div>'))
    (out / "pushing.html").write_text(TMPL.format(title="TS pushing", h1="Pushing", sub="why-questions per ahnika", work="tantrasara",
        body='<div class="panel">Q→GEM scaffolds next, same pushing.py extractor.</div>'))
    return len(units)

def main():
    DIST.mkdir(parents=True, exist_ok=True)
    want = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ipvv", "vbt", "tantrasara"]
    done = {}
    if "ipvv" in want: done["ipvv"] = build_ipvv()
    if "vbt" in want: done["vbt"] = build_vbt()
    if "tantrasara" in want: done["tantrasara"] = build_tantrasara()
    idx = '<div class="idx">' + "".join(f'<a href="/{w}/index.html"><b>{w}</b> — {n} items · Sanskrit → READ → STUDY · GUIDE soon</a>' for w, n in done.items()) + "</div>"
    (DIST / "index.html").write_text(TMPL.format(title="Translations", h1="Translations", sub="display only what is formally done", work="ipvv", body=idx))
    print("built", done)

if __name__ == "__main__":
    main()
