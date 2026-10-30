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

def esc(s): return html.escape(str(s or ""))

def build_ipvv():
    src = sorted((PATALA / "data/published/ipvv").glob("pt-passage-*.json"))
    items = [json.loads(p.read_text()) for p in src]
    out = DIST / "ipvv"; out.mkdir(parents=True, exist_ok=True)
    argdir = ROOT / "data/ipvv/argmaps"
    pmap = {"chunkA":"pilot_V1A","chunkB":"pilot_V1B","chunkC":"pilot_V1C","chunkD":"pilot_V1D",
        "chunkE":"pilot_V1E","chunkF":"pilot_V1F","chunkG":"pilot_V1G","chunkH":"pilot_V1H",
        "chunkI":"pilot_V1I","chunkJ":"pilot_V1J","chunkK":"pilot_V1K","chunkL":"pilot_V1L",
        "chunkM":"pilot_V1M","chunkN":"pilot_V1N","chunkV2-A":"pilot_V2A","chunkV2-B":"pilot_V2B",
        "chunkV2-C":"pilot_V2C","chunkV2-D":"pilot_V2D","chunkV2-E":"pilot_V2E","chunkV2-F":"pilot_V2F",
        "chunkV2-G":"pilot_V2G","chunkV2-H":"pilot_V2H","chunkV2-I":"pilot_V2I","chunkV2-J":"pilot_V2J",
        "chunkV2-K":"pilot_V2K","chunkV2-L":"pilot_V2L","chunkV2-M":"pilot_V2M","chunkV2-N":"pilot_V2N",
        "chunkV2-O":"pilot_V2O","chunkV2-P":"pilot_V2P","chunkV2-Q":"pilot_V2Q","chunkV2-R":"pilot_V2R",
        "chunkV2-S":"pilot_V2S","chunkV3-A":"pilot_V3A","chunkV3-C":"pilot_V3C","chunkV3-D":"pilot_V3D",
        "chunkV3-E":"pilot_V3E","chunkV3-F":"pilot_V3F","chunkV3-G":"pilot_V3G","chunkV3-H":"pilot_V3H",
        "chunkV3-I":"pilot_V3I","chunkV3-J":"pilot_V3J","chunkV3-K":"pilot_V3K","chunkV3-L":"pilot_V3L",
        "chunkV3-M":"pilot_V3M","chunkV3-N":"pilot_V3N","chunkV3-O":"pilot_V3O","chunkV3-P":"pilot_V3P"}
    links = []
    for d in items:
        pid = d["id"].split(":")[-1].replace(".md", "")
        chunk = (d.get("chunk") or "").replace(".md", "")
        src_txt = (d.get("source") or {}).get("text", "") if isinstance(d.get("source"), dict) else ""
        l2 = d.get("l2_text") or ""
        c1 = d.get("c1") or {}
        c1b = c1.get("body", "") if isinstance(c1, dict) else str(c1)
        # argmap + pilot L2 from R2 cache (full, pristine)
        am, l2p = "", ""
        pp = pmap.get(chunk)
        if pp:
            pa, pl = argdir / f"{pp}_ARGUMENT_MAP.md", argdir / f"{pp}_L2_read.md"
            if pa.exists(): am = pa.read_text()
            if pl.exists(): l2p = pl.read_text()
        if chunk == "chunkV3-B-kriya-dvitiyo-k1-7":
            v3b_extra = ""
            for fn, label in [("pilot_V3B_K6_ARGUMENT_MAP.md", "K6 argmap"),
                              ("pilot_V3B_S7_ARGUMENT_MAP.md", "S7 argmap"),
                              ("pilot_V3B_S9_ARGUMENT_MAP.md", "S9 argmap"),
                              ("pilot_V3B_full_L2.md", "full L2"),
                              ("pilot_V3B_k1_L1_apparatus.md", "k1 L1 apparatus"),
                              ("pilot_V3B_k2-7_L1_apparatus.md", "k2-7 L1 apparatus")]:
                p = argdir / fn
                if p.exists():
                    v3b_extra += f'<hr/><div class="sub">{label} (full)</div><div class="en">{esc(p.read_text())}</div>'
            am = (am + v3b_extra) if am else v3b_extra
        extra_l2 = f'<hr/><div class="sub">Pilot L2 (argument-derived, full)</div><div class="en">{esc(l2p)}</div>' if l2p and l2p.strip() != l2.strip() else ""
        body = tabs([
            ("ORIGINAL", f'<div class="dev">{esc(src_txt)}</div><div class="sub">vol {esc(d.get("vol",""))} · {esc(chunk)} · lines via source.start/end</div>', bool(src_txt)),
            ("READ", f'<div class="en">{esc(l2)}</div>{extra_l2}', bool(l2)),
            ("ARGMAP", f'<div class="en">{esc(am)}</div>', bool(am)),
            ("STUDY", f'<div class="en">{esc(c1b)}</div>', bool(c1b)),
            ("GUIDE", None, False),
            ("CRITICAL", f'<div class="en">immutable {esc(d.get("immutable_id",""))} · T1 chunk <i>sanskritree/{esc(chunk)}.md</i> via <i>tools/fetch.sh</i> · L200 8-section audit per <i>specs/C1_SPEC + l200 spec</i> · L1 apparatus: V3B pilot in <i>samples/</i></div>', True),
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

ATmpl = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title><style>""" + CSS + """.wrap{{display:flex;gap:1.5rem;align-items:flex-start}}
.side{{min-width:210px;max-width:240px;border-right:1px solid #ddd;padding-right:1rem;font-size:.9rem}}
.side a{{display:block;padding:.3rem 0;color:#222;text-decoration:none}}
.side a:hover{{text-decoration:underline}}.side .hd{{color:#888;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;margin:.8rem 0 .3rem}}
.side .sub a{{padding-left:.8rem;color:#555}}
.main{{flex:1;min-width:0}}
@media(max-width:640px){{.wrap{{flex-direction:column}}.side{{max-width:none;border-right:none;border-bottom:1px solid #ddd;padding-bottom:.6rem}}}}
.tl{{border-left:2px solid #c9a227;margin:1rem 0 1rem .5rem;padding-left:1rem}}
.tl .ev{{margin:.5rem 0}}.dot{{display:inline-block;width:.6em;height:.6em;border-radius:50%;background:#c9a227;margin-right:.4em}}
</style></head><body>
<header><h1>{h1}</h1><div class="sub">{sub}</div></header>
<div class="nav"><a href="/index.html">works</a><a href="/abhinavagupta/index.html">Abhinavagupta</a></div>
<div class="wrap"><div class="side">{sidenav}</div><div class="main">{body}</div></div></body></html>"""

def sidenav(active=""):
    works = json.loads((ROOT / "data/works.json").read_text())
    items = "".join(f'<a href="/abhinavagupta/{w["id"]}.html">{"› " if w["id"]==active else ""}{esc(w["title"])}</a>' for w in works)
    return ('<div class="hd">Abhinavagupta</div>'
        f'<a href="/abhinavagupta/index.html">{"› " if active=="bio" else ""}Bio</a>'
        f'<a href="/abhinavagupta/works.html">{"› " if active=="works" else ""}Works map</a>'
        '<div class="hd">Works (chronological)</div><div class="sub">' + items + "</div>")

STOTRA = {"bodhapanacadasika": "clean_bodhapanchadashika.txt", "anuttarastika": "clean_anuttarashtika.txt",
    "bhairavastava": "clean_bhairavastava.txt", "dehastha": "clean_dehastha.txt"}

def build_author():
    out = DIST / "abhinavagupta"; out.mkdir(parents=True, exist_ok=True)
    author = json.loads((ROOT / "data/author.json").read_text())
    works = json.loads((ROOT / "data/works.json").read_text())
    lin = "".join(f'<div class="panel">{esc(l.get("relation",""))} <b>{esc(l.get("who",""))}</b></div>' for l in author.get("lineage", []))
    (out / "index.html").write_text(ATmpl.format(title="Abhinavagupta", h1=esc(author["name"]),
        sub=f'{esc(author["dates"]["flourished"])} · {esc(author["place"])}', sidenav=sidenav("bio"),
        body=f'<div class="panel">{esc(author["summary"])}</div><h3>Lineage</h3>{lin}'
             f'<div class="sub">dates {esc(author["dates"]["note"])} · <a href="/data/author.json">machine-readable JSON</a></div>'))
    tl = "".join(f'<div class="ev"><span class="dot"></span><b>{esc(w["title"])}</b> — {esc(w["date"])} · {esc(w["status"])}<br/><a href="/abhinavagupta/{w["id"]}.html">open →</a></div>' for w in works)
    links = "".join(f'<a href="/abhinavagupta/{w["id"]}.html"><b>{esc(w["title"])}</b> — {esc(w["date"])} · {esc(w["status"])}</a>' for w in works)
    (out / "works.html").write_text(ATmpl.format(title="Works map", h1="Works map",
        sub="chronological — click any title for the full translation", sidenav=sidenav("works"),
        body=f'<div class="tl">{tl}</div><h3>List</h3><div class="idx">{links}</div>'
             f'<div class="sub"><a href="/data/works.json">machine-readable JSON</a></div>'))
    for w in works:
        wid = w["id"]
        if wid in STOTRA:
            txt = (Path("/root/deitybody/corpus/stotra") / STOTRA[wid]).read_text()
            body = tabs([("ORIGINAL", f'<div class="dev">{esc(txt)}</div>', True),
                ("READ", None, False), ("GUIDE", None, False),
                ("STUDY", f'<div class="en">{esc(w["title"])} — full Sanskrit above; English READ next via pipe.</div>', True),
                ("CRITICAL", f'<div class="en">deitybody corpus/stotra/{STOTRA[wid]} · {esc(w["date"])} · status {esc(w["status"])}</div>', True)])
        elif wid == "ipvv":
            body = ('<div class="panel">Full translation: <b><a href="/ipvv/index.html">49 passages, all depths</a></b> (ORIGINAL/READ/ARGMAP/STUDY/CRITICAL).</div>'
                '<div class="panel">Thesis: recognition — the self re-cognises itself as the Lord; vimarśa = parā-vāc = the throb. Honest limit: universalization is the wager.</div>')
        elif wid == "tantrasara":
            body = ('<div class="panel">Full display: <b><a href="/tantrasara/index.html">6 essay-0 units</a></b> (verbatim → plain). Philological T1/L0 next via pipe; start Ahnika 11.</div>')
        elif wid == "tantraloka":
            body = ('<div class="panel">37 ahnikas on volume (01+04 1.7MB each) + 6-variant texts-clean + 7 pre-split ahnika-1 chunks. No T1 yet — first SOURCE cut. Run <i>tools/chunker.py</i> on ahnika-1 chunk-1.</div>')
        elif wid == "kramastotra":
            body = ('<div class="panel">GRETIL + volume Appendix F (Sanskrit + Dyczkowski English). Next: cut as first T1 pilot for stotra track.</div>')
        elif wid == "ipv":
            body = ('<div class="panel">Mukhabodha M00019 + Pandey Bhaskari English (complete). Next: align as parallel for IPVV passages.</div>')
        elif wid == "ptv":
            body = ('<div class="panel">Local: <i>deitybody/corpus/primary/paratrisika_jaideva_singh_text.pdf</i> (Singh/Baumer). Madhyama-vac + Malini order, Singh pp.148-156. Next: cut PTv 1-4.</div>')
        elif wid == "mvv":
            body = ('<div class="panel">Stockpile pointer. Next: locate critical text (Vasudeva ed.) then cut.</div>')
        elif wid == "dehastha":
            dp = Path("/root/deitybody/corpus/stotra") / STOTRA[wid]
            txt = dp.read_text() if dp.exists() else ""
            if txt:
                body = tabs([("ORIGINAL", f'<div class="dev">{esc(txt)}</div>', True),
                    ("READ", None, False), ("GUIDE", None, False),
                    ("STUDY", '<div class="en">ATTRIBUTION DISPUTED — listed, flagged, never taught as Abhinavagupta\'s.</div>', True),
                    ("CRITICAL", f'<div class="en">status {esc(w["status"])}</div>', True)])
            else:
                body = f'<div class="panel">status {esc(w["status"])}</div>'
        else:
            body = f'<div class="panel">status {esc(w["status"])}</div>'
        (out / f"{wid}.html").write_text(ATmpl.format(title=w["title"], h1=esc(w["title"]),
            sub=f'{esc(w["date"])} · {esc(w.get("verses",""))} · {esc(w["status"])}', sidenav=sidenav(wid), body=body))
    # ship machine-readable data with the site
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    (DIST / "data" / "author.json").write_text((ROOT / "data/author.json").read_text())
    (DIST / "data" / "works.json").write_text((ROOT / "data/works.json").read_text())
    return len(works)

def main():
    DIST.mkdir(parents=True, exist_ok=True)
    want = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ipvv", "vbt", "tantrasara", "author"]
    done = {}
    if "ipvv" in want: done["ipvv"] = build_ipvv()
    if "vbt" in want: done["vbt"] = build_vbt()
    if "tantrasara" in want: done["tantrasara"] = build_tantrasara()
    if "author" in want: done["abhinavagupta"] = build_author()
    idx = ('<div class="idx"><a href="/abhinavagupta/index.html"><b>Abhinavagupta</b> — bio · works map · click-in translations</a></div>'
        + "".join(f'<a href="/{w}/index.html"><b>{w}</b> — {n} items · Sanskrit → READ → STUDY · GUIDE soon</a>' for w, n in done.items() if w != "abhinavagupta"))
    (DIST / "index.html").write_text(TMPL.format(title="Translations", h1="Abhinavagupta · Translations",
        sub="display only what is formally done", work="abhinavagupta", body=idx))
    print("built", done)

if __name__ == "__main__":
    main()
