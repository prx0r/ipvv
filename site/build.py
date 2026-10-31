#!/usr/bin/env python3
"""site/build.py — static display site for formally-done translation work.

Same shell for every work. Displays only what formally exists.
Missing layers render greyed (planned), never invented.

Usage: python3 site/build.py [--works ipvv,vbt,tantrasara]
Output: site/dist/ (deploy to Cloudflare Pages, like shivastotravali.pages.dev)
"""
import json, html, re, shutil, sys
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
.skt{{white-space:pre-wrap;font-size:1.05rem}}
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

STATUS_LABEL = {"SOURCE_ONLY": "Sanskrit held", "SOURCE_ONLY_DISPUTED": "Sanskrit held · disputed",
    "SOURCE_PLUS_TRANSLATION": "Sanskrit + English", "SOURCE_PLUS_SCHOLARSHIP": "Sanskrit + scholarship",
    "SOURCE_CHUNKED": "chunked, awaiting T1", "ESSAY0": "essay-0", "PUBLISHED_49": "full display (49)",
    "STOCKPILE": "listed", "LOST": "LOST", "REF_ONLY": "ref-only", "FRAGMENT": "fragments",
    "ATTRIBUTED_DISPUTED": "ascription disputed", "STOCKPILE_UNVERIFIED": "listed · unverified",
    "TEACHER_ONLY": "teacher — no independent works", "SOURCE_HELD": "full Sanskrit held"}

def author_paths(aid):
    a = ROOT / "data/authors" / f"{aid}.json"
    if not a.exists() and aid == "abhinavagupta":
        a = ROOT / "data/author.json"
    w = ROOT / "data" / f"works_{aid}.json"
    if not w.exists() and aid == "abhinavagupta":
        w = ROOT / "data/works.json"
    return a, w

def sidenav(aid, active=""):
    author = json.loads(author_paths(aid)[0].read_text())
    works = json.loads(author_paths(aid)[1].read_text())
    items = "".join(f'<a href="/{aid}/{w["id"]}.html">{"› " if w["id"]==active else ""}{esc(w["title"])}</a>' for w in works)
    return ('<div class="hd">Masters</div>'
        + "".join(f'<a href="/{m}/index.html">{"› " if m==aid else ""}{esc(m)}</a>' for m in MASTERS)
        + f'<div class="hd">{esc(author["name"])}</div>'
        f'<a href="/{aid}/index.html">{"› " if active=="bio" else ""}Bio</a>'
        f'<a href="/{aid}/works.html">{"› " if active=="works" else ""}Works map</a>'
        '<div class="hd">Works (canonical list)</div><div class="sub">' + items + "</div>")

MASTERS = ["abhinavagupta", "somananda", "vasugupta", "kallata", "utpaladeva",
           "lakshmanagupta", "sambhunatha", "ksemaraja", "bhutiraja", "jayaratha",
           "yogaraja", "bhattanarayana", "induraja", "sivopadhyaya", "lalla"]

def build_split(aid, wid):
    """Split a big Sanskrit file into per-section pages. Returns section count."""
    import re
    out = DIST / aid
    if wid == "tantraloka":
        txt = (ROOT / "data/sanskrit/tantraloka.txt").read_text()
        parts = re.split(r"(?m)^(?=:C\d+ )", txt)
        heads = re.findall(r"(?m)^:C\d+ .{0,60}", txt)
    elif wid == "tantrasara":
        txt = (ROOT / "data/sanskrit/tantrasara.txt").read_text()
        parts = re.split(r"(?m)^(?=Tantras.+hnikam)", txt)
        heads = re.findall(r"(?m)^Tantras.+hnikam.*$", txt)
    else:
        return 0
    # first chunk is preamble before section 1 (usually tiny); merge into section 1
    if len(parts) == len(heads) + 1:
        parts[1] = parts[0] + parts[1]; parts = parts[1:]
    n = 0
    for i, (h, p) in enumerate(zip(heads, parts), 1):
        n += 1
        prev = f'<a href="/{aid}/{wid}-{i-1}.html">← {i-1}</a>' if i > 1 else ""
        nxt = f'<a href="/{aid}/{wid}-{i+1}.html">{i+1} →</a>' if i < len(heads) else ""
        nav = f'<div class="nav">{prev} <a href="/{aid}/{wid}.html">all {len(heads)}</a> {nxt}</div>'
        body = nav + tabs([("ORIGINAL", f'<div class="dev skt">{esc(p.strip())}</div>', True),
            ("READ", None, False), ("GUIDE", None, False),
            ("STUDY", f'<div class="en">Section {i} of {len(heads)} — English READ next via pipe.</div>', True),
            ("CRITICAL", f'<div class="en">GRETIL/Mukhabodha; section head: {esc(h.strip()[:80])}</div>', True)]) + nav
        (out / f"{wid}-{i}.html").write_text(ATmpl.format(title=f"{wid} §{i}", h1=f"Section {i}",
            sub=esc(h.strip()[:80]), sidenav=sidenav(aid, wid), body=body))
    return n

def author_bio_body(aid, author, lin, spine):
    hero = ""
    if author.get("image"):
        im = author["image"]
        hero = (f'<div class="panel"><img src="{esc(im["src"])}" alt="{esc(author["name"])} — related imagery" loading="lazy" style="max-width:100%;border-radius:8px"/>'
                f'<div class="sub">{esc(im["caption"])} Credit: <a href="{esc(im["credit_url"])}">{esc(im["credit"])}</a> · <a href="{esc(im["licence_url"])}">{esc(im["licence"])}</a></div></div>')
    return (f'<div class="panel">{esc(author["summary"])}</div>' + hero
            + (f'<div class="panel"><b>Bio.</b> {esc(author["bio"])}</div>' if author.get("bio") else "")
            + f'<h3>Lineage</h3>{lin}'
            + f'<div class="sub">dates {esc(author["dates"]["note"])} · canon: {spine} · <a href="/data/authors/{aid}.json">machine-readable JSON</a> · <a href="/data/person-schema.json">bio schema</a></div>')

def build_author(aid="abhinavagupta"):
    out = DIST / aid; out.mkdir(parents=True, exist_ok=True)
    apath, wpath = author_paths(aid)
    author = json.loads(apath.read_text())
    works = json.loads(wpath.read_text())
    lin = "".join(f'<div class="panel">{esc(l.get("relation",""))} <b>{esc(l.get("who",""))}</b></div>' for l in author.get("lineage", []))
    spine = {"abhinavagupta": "Raghavan “Abhinavagupta and His Works” 36 + attested extras",
             "utpaladeva": "Wikipedia/BnF/kashmirhope + GRETIL/Mukhabodha holdings",
             "ksemaraja": "Singh/SUNY + Flood 2020 + kashmirhope + ePustakalay/KSTS holdings"}.get(aid, "")
    (out / "index.html").write_text(ATmpl.format(title=author["name"], h1=esc(author["name"]),
        sub=f'{esc(author["dates"]["flourished"])} · {esc(author.get("place",""))}', sidenav=sidenav(aid, "bio"),
        body=author_bio_body(aid, author, lin, spine)))
    cats = {}
    for w in works:
        cats.setdefault(w.get("category", "?"), []).append(w)
    blocks = []
    for c, ws in cats.items():
        rows = "".join(
            f'<div class="ev"><span class="dot" style="{"background:#ccc" if w.get("extant") is False else ""}"></span>'
            + f'<b>{esc(w["title"])}</b> — {esc(w.get("date",""))} · {esc(STATUS_LABEL.get(w.get("status",""), w.get("status","")))}'
            + f'<br/><a href="/{aid}/{w["id"]}.html">open →</a></div>' for w in ws)
        blocks.append(f"<h3>{esc(c)}</h3>" + rows)
    n_ext = sum(1 for w in works if w.get("extant") is True)
    n_lost = sum(1 for w in works if w.get("extant") is False)
    n_unk = len(works) - n_ext - n_lost
    (out / "works.html").write_text(ATmpl.format(title="Works map", h1="Works map",
        sub=f"canonical list: {len(works)} works ({n_ext} extant, {n_lost} lost/ref-only, {n_unk} unverified) — click any title", sidenav=sidenav(aid, "works"),
        body=f'<div class="tl">{"".join(blocks)}</div>'
             f'<div class="sub">Spine: {spine} · <a href="/data/works_{aid}.json">machine-readable JSON</a></div>'))
    for w in works:
        wid = w["id"]
        label = STATUS_LABEL.get(w.get("status", ""), w.get("status", ""))
        meta = f'{esc(w.get("date",""))} · {esc(label)}'
        if w.get("verses") not in (None, ""): meta += f' · {esc(w["verses"])}'
        # pipeline translation link, if ingested (PASS-gated English lives there)
        trlink = ""
        trfile = ROOT / "data/translations" / f"{wid}.json"
        if trfile.exists():
            import json as _j
            _items = _j.loads(trfile.read_text())
            _np = sum(1 for _i in _items if _i.get("gate") == "PASS")
            trlink = (f'<div class="panel">Pipeline translation: <b><a href="/translations/{wid}.html">open →</a></b> '
                      f'({_np}/{len(_items)} passages passed the gate; English shows for those only)</div>')
        tf = w.get("text_file")
        sf = w.get("sanskrit_file")
        eds = "".join(f'<div class="sub">▪ {esc(e)}</div>' for e in w.get("editions", []))
        src_note = f'<div class="sub">{esc(w.get("sanskrit_source",""))}</div>' if w.get("sanskrit_source") else ""
        if w.get("sanskrit") == "split-ahnika":
            n = build_split(aid, wid)
            body = (f'<div class="panel">Full Sanskrit in <b>{n} sections</b> — click in. {esc(w.get("note",""))}</div>'
                    + "".join(f'<div class="ev"><a href="/{aid}/{wid}-{i}.html">section {i} →</a></div>' for i in range(1, n + 1)))
        elif sf:
            sp = ROOT / "data/sanskrit" / sf
            txt = sp.read_text() if sp.exists() else ""
            if txt and len(txt) > 500000:
                body = (f'<div class="panel">Full Sanskrit ({len(txt)//1024}KB) — <a href="/data/sanskrit/{sf}"><b>read/download full text →</b></a></div>'
                        + (f'<div class="panel">{esc(w.get("note",""))}</div>' if w.get("note") else "")
                        + tabs([("ORIGINAL (head)", f'<div class="dev skt">{esc(txt[:15000])}\n…[continued in full text]</div>', True),
                            ("READ", None, False), ("GUIDE", None, False),
                            ("STUDY", f'<div class="en">{esc(w["title"])} — English READ next via pipe.</div>', True),
                            ("CRITICAL", f'<div class="en">{esc(w.get("sanskrit_source",""))} · {meta}</div>', True)]))
            else:
                body = tabs([("ORIGINAL", f'<div class="dev skt">{esc(txt)}</div>', bool(txt)),
                    ("READ", None, False), ("GUIDE", None, False),
                    ("STUDY", f'<div class="en">{esc(w["title"])} — full Sanskrit above; English READ next via pipe.</div>', True),
                    ("CRITICAL", f'<div class="en">{esc(w.get("sanskrit_source",""))} · {meta}</div>', True)])
        elif tf:
            p = Path("/root/deitybody/corpus/stotra") / tf
            txt = p.read_text() if p.exists() else ""
            body = tabs([("ORIGINAL", f'<div class="dev">{esc(txt)}</div>', bool(txt)),
                ("READ", None, False), ("GUIDE", None, False),
                ("STUDY", f'<div class="en">{esc(w["title"])} — full Sanskrit above; English READ next via pipe.</div>', True),
                ("CRITICAL", f'<div class="en">deitybody corpus/stotra/{tf} · {meta}{eds}</div>', True)])
        elif w.get("link"):
            thesis = '<div class="panel">Thesis: recognition — the self re-cognises itself as the Lord.</div>' if wid == "ipvv" else ""
            vols = ""
            if wid == "ipvv":
                vols = ('<div class="panel">Full Sanskrit vols (Mukhabodha IAST, CC BY-NC 4.0): '
                        '<a href="/data/sanskrit/ipvv-vol1.txt">Vol 1</a> · '
                        '<a href="/data/sanskrit/ipvv-vol2.txt">Vol 2</a> · '
                        '<a href="/data/sanskrit/ipvv-vol3.txt">Vol 3</a></div>')
            body = (f'<div class="panel">Full display: <b><a href="{w["link"]}">open →</a></b></div>'
                    + vols
                    + (f'<div class="panel">{esc(w["note"])}</div>' if w.get("note") else "")
                    + thesis
                    + (eds if w.get("editions") else ""))
        else:
            note = w.get("note", "")
            sfs = "".join(f'<div class="panel">Sanskrit text: <a href="/data/sanskrit/{f}"><b>{esc(f)} →</b></a></div>' for f in w.get("sanskrit_files", []))
            root = ""
            if w.get("sanskrit_root"):
                root = (f'<div class="panel">Related root text (comm. itself undigitized): '
                        f'<a href="/data/sanskrit/{w["sanskrit_root"]}"><b>{esc(w["sanskrit_root"])} →</b></a></div>')
            if w.get("status") in ("LOST", "REF_ONLY", "FRAGMENT", "ATTRIBUTED_DISPUTED", "SOURCE_ONLY_DISPUTED"):
                why = {"LOST": "references in the tradition", "REF_ONLY": "references in the tradition", "FRAGMENT": "quotations in the tradition", "ATTRIBUTED_DISPUTED": "a disputed ascription — verify before teaching as his", "SOURCE_ONLY_DISPUTED": "a disputed ascription — listed, flagged, never taught as his"}[w.get("status")]
                body = (f'<div class="panel missing"><b>{esc(label)}.</b> No text survives; known only from {esc(why)}.</div>'
                    + (f'<div class="panel">{esc(note)}</div>' if note else "")
                    + eds)
            else:
                body = ((f'<div class="panel">{esc(note)}</div>' if note else "")
                    + sfs + root + eds
                    + f'<div class="panel">Status: {esc(label)}. Next via pipe: cut SOURCE → T1 → L0 → argmap → L2 → L200 → C1.</div>')
        (out / f"{wid}.html").write_text(ATmpl.format(title=w["title"], h1=esc(w["title"]),
            sub=meta, sidenav=sidenav(aid, wid), body=trlink + body))
    # ship machine-readable data with the site
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    if aid == "abhinavagupta":
        (DIST / "data" / "author.json").write_text((ROOT / "data/author.json").read_text())
        (DIST / "data" / "works.json").write_text((ROOT / "data/works.json").read_text())
    (DIST / "data" / f"author_{aid}.json").write_text(json.dumps(author, ensure_ascii=False, indent=1))
    (DIST / "data" / f"works_{aid}.json").write_text(json.dumps(works, ensure_ascii=False, indent=1))
    import shutil as _sh2
    _sh2.copy(ROOT.parent / "specs/schema/person.json", DIST / "data/person-schema.json")
    # ship ALL held Sanskrit bytes (research/education use; licence in each header)
    sdir = DIST / "data/sanskrit"; sdir.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "data/sanskrit").glob("*.txt"):
        shutil.copy(f, sdir / f.name)
    if (ROOT / "data/roots.json").exists():
        shutil.copy(ROOT / "data/roots.json", DIST / "data/roots.json")
    return len(works)

def ship_translations():
    # ship ingested pipeline translations (PASS-gated English + gate status)
    tdir = DIST / "data/translations"; tdir.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "data/translations").glob("*.json"):
        shutil.copy(f, tdir / f.name)

def scholar_nav(active=""):
    scholars = json.loads((ROOT / "data/scholars.json").read_text())
    items = "".join(f'<a href="/scholars/{s["id"]}.html">{"› " if s["id"]==active else ""}{esc(s["name"])}</a>' for s in scholars)
    return ('<div class="hd">Masters</div>'
        + "".join(f'<a href="/{m}/index.html">{esc(m)}</a>' for m in MASTERS)
        + '<div class="hd">Scholars</div>'
        f'<a href="/scholars/index.html">{"› " if active=="index" else ""}All scholars</a>'
        '<div class="hd">People (secondary)</div><div class="sub">' + items + "</div>")

ACC_LABEL = {"open": "open access", "login": "free login wall", "metadata": "metadata only — fetch via academia/DOI",
             "print": "print/commercial — cite, never host", "study": "in-repo study material"}

def build_translations():
    """Pipeline translations: PASS passages display L1/L2 with gate badge;
    BLOCKED passages show Sanskrit + withheld notice (never English-as-translation)."""
    import json as _json
    src = ROOT / "data/translations"
    if not src.exists():
        return 0
    out = DIST / "translations"; out.mkdir(parents=True, exist_ok=True)
    links = []
    for f in sorted(src.glob("*.json")):
        items = _json.loads(f.read_text())
        if not items:
            continue
        wid = f.stem
        n_pass = sum(1 for i in items if i.get("gate") == "PASS")
        blocks = []
        for it in items:
            badge = ("PASS" if it["gate"] == "PASS"
                     else "WITHHELD — pending review (" + ", ".join(it.get("blocking", ["review"])) + ")")
            if it["gate"] == "PASS":
                body = tabs([
                    ("ORIGINAL", f'<div class="dev skt">{esc(it["sanskrit"])}</div>', bool(it["sanskrit"])),
                    ("L1", f'<div class="en">{esc(it.get("l1",""))}</div>', bool(it.get("l1"))),
                    ("READ", f'<div class="en">{esc(it.get("l2",""))}</div>', bool(it.get("l2"))),
                    ("CRITICAL", f'<div class="en">gate: PASS · model {esc(it.get("model",""))} · {esc(it.get("date",""))} · machine-proposed, needs human review before doctrine use</div>', True)])
            else:
                body = (f'<div class="panel"><div class="dev skt">{esc(it["sanskrit"])}</div></div>'
                        f'<div class="panel missing"><b>{badge}.</b> English withheld until the gate passes — fail-closed.</div>')
            blocks.append(f'<h3>{esc(it.get("chunk",""))} · verses {esc(it.get("verses",""))} · {badge.split(" — ")[0]}</h3>' + body)
        (out / f"{wid}.html").write_text(ATmpl.format(title=f"Translation: {wid}",
            h1=f"Translation: {wid}", sub=f"{n_pass}/{len(items)} passages passed the gate — only those show English",
            sidenav=sidenav("abhinavagupta", wid), body="".join(blocks)))
        links.append((wid, n_pass, len(items)))
    (out / "index.html").write_text(ATmpl.format(title="Translations", h1="Pipeline translations",
        sub="English shows ONLY for gate-PASS passages; the rest stay Sanskrit + status",
        sidenav=sidenav("abhinavagupta", ""), body='<div class="idx">'
        + "".join([f'<a href="/translations/{w}.html"><b>{w}</b> — {p}/{n} PASS</a>' for w, p, n in links]) + "</div>"))
    return len(links)

def slugify(s):
    import unicodedata as _u
    s = _u.normalize("NFD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "term"

def build_glossary():
    import json as _j
    gl = _j.loads((ROOT / "data/glossary.json").read_text())
    out = DIST / "concepts"; out.mkdir(parents=True, exist_ok=True)
    for e in gl:
        slug = slugify(e["term"])
        links = "".join(f'<div class="ev"><a href="/ipvv/{p}.html">IPVV: {esc(p)}</a></div>' for p in e.get("passages", [])[:20])
        (out / f"{slug}.html").write_text(ATmpl.format(title=e["term"], h1=esc(e["term"]),
            sub="concept · glossary", sidenav=sidenav("abhinavagupta", ""),
            body=f'<div class="panel">{esc(e.get("gloss") or "occurrence only — definition pending curation.")}</div>'
                 + (f"<h3>Occurs in</h3>{links}" if links else "<p><i>No linked passages yet.</i></p>")
                 + f'<div class="sub">source: {esc(e.get("source",""))} · <a href="/data/glossary.json">machine-readable glossary</a></div>'))
    idx = "".join(f'<a href="/concepts/{slugify(e["term"])}.html"><b>{esc(e["term"])}</b> — {esc((e.get("gloss") or "")[:90])}</a>' for e in gl)
    (out / "index.html").write_text(ATmpl.format(title="Concepts", h1="Concepts",
        sub=f"{len(gl)} terms — definitions link to every occurrence", sidenav=sidenav("abhinavagupta", ""),
        body='<input id="q" placeholder="filter terms…" style="width:100%;padding:.6rem;font-size:1rem;margin-bottom:.6rem"/>'
             f'<div class="idx" id="terms">{idx}</div>'
             '<script>q.oninput=()=>{const v=q.value.toLowerCase();document.querySelectorAll("#terms a").forEach(a=>a.style.display=a.textContent.toLowerCase().includes(v)?"":"none")}</script>'
             '<div class="sub"><a href="/data/glossary.json">machine-readable glossary</a> · mined from C1 key-terms + curated core</div>'))
    shutil.copy(ROOT / "data/glossary.json", DIST / "data/glossary.json")
    return len(gl)

def build_tools():
    import json as _j
    out = DIST / "tools"; out.mkdir(parents=True, exist_ok=True)
    entries = []
    for f in (ROOT / "data").glob("works*.json"):
        for w in _j.loads(f.read_text()):
            entries.append({"t": w.get("title", ""), "u": "", "k": "work"})
    for aid in MASTERS:
        ap = ROOT / "data/authors" / f"{aid}.json"
        if not ap.exists() and aid == "abhinavagupta":
            ap = ROOT / "data/author.json"
        if ap.exists():
            a = _j.loads(ap.read_text())
            entries.append({"t": a.get("name", aid), "u": f"/{aid}/index.html", "k": "master"})
    for e in _j.loads((ROOT / "data/glossary.json").read_text()):
        import unicodedata as _u
        slug = _u.normalize("NFD", e["term"]).encode("ascii", "ignore").decode()
        import re as _re
        slug = _re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-") or "term"
        entries.append({"t": e["term"], "u": f"/concepts/{slug}.html", "k": "concept"})
    (DIST / "data/search-index.json").write_text(_j.dumps(entries, ensure_ascii=False))
    (out / "index.html").write_text(ATmpl.format(title="Tools", h1="Tools",
        sub="instant find across masters, works, concepts — runs entirely in your browser",
        sidenav=sidenav("abhinavagupta", ""),
        body='<input id="q" placeholder="search masters, works, concepts…" style="width:100%;padding:.7rem;font-size:1.1rem"/>'
             '<div class="idx" id="hits" style="margin-top:.6rem"></div>'
             '<div class="panel"><b>Verse lookup.</b> Type a passage id (e.g. <i>chunkV2-A-caturtho-vimarsa-aham</i>) — exact matches jump straight to the passage. <input id="v" placeholder="passage id…" style="width:100%;padding:.5rem;margin-top:.4rem"/><div id="vhit" style="margin-top:.4rem"></div></div>'
             '<div class="sub">Index built at deploy time from the same JSON the pages render. No server, no tracking.</div>'
             '<script>let IDX=[];fetch("/data/search-index.json").then(r=>r.json()).then(d=>IDX=d);'
             'q.oninput=()=>{const v=q.value.toLowerCase();const m=v?IDX.filter(e=>e.t.toLowerCase().includes(v)).slice(0,40):[];'
             'hits.innerHTML=m.map(e=>`<a href="${e.u||"/"+e.k+"s/index.html"}"><b>${e.t}</b> <i>${e.k}</i></a>`).join("")||(v?"<i>No matches.</i>":"")};'
             'v.oninput=()=>{const x=v.value.trim();vhit.innerHTML=x?`<a href="/ipvv/${x}.html">Open /ipvv/${x}</a> · <a href="/ipvv/${x.replace(/[^A-Za-z0-9_-]/g,"")}.html">try cleaned</a>`:""};</script>'))
    return 1

def build_scholars():
    out = DIST / "scholars"; out.mkdir(parents=True, exist_ok=True)
    scholars = json.loads((ROOT / "data/scholars.json").read_text())
    links = []
    for s in scholars:
        items = ""
        for it in s.get("items", []):
            acc = ACC_LABEL.get(it.get("access", ""), it.get("access", ""))
            link = f'<a href="{it["link"]}">link →</a>' if it.get("link") else "no public link"
            items += (f'<div class="panel"><b>{esc(it.get("title",""))}</b> {esc(str(it.get("year") or ""))}<br/>'
                      f'<div class="sub">{esc(acc)} · {link}</div>'
                      f'<div class="en">Used for: {esc(it.get("used_for",""))}</div></div>')
        body = (f'<div class="panel">{esc(s.get("summary",""))}</div>'
                + (f'<div class="panel"><b>Bio.</b> {esc(s["bio"])}</div>' if s.get("bio") else "")
                + f'<div class="sub">{esc(s.get("affiliation",""))} · status: {esc(s.get("status",""))} · dates: {esc(s.get("dates",{}).get("flourished",""))} — {esc(s.get("dates",{}).get("note",""))}</div>'
                + f'<div class="sub"><a href="/data/scholars.json">machine-readable JSON</a> · <a href="/data/person-schema.json">bio schema</a></div>'
                + items)
        (out / f'{s["id"]}.html').write_text(ATmpl.format(title=s["name"], h1=esc(s["name"]),
            sub=esc(s.get("affiliation","")), sidenav=scholar_nav(s["id"]), body=body))
        links.append(f'<a href="/scholars/{s["id"]}.html"><b>{esc(s["name"])}</b> — {esc(s.get("affiliation",""))}</a>')
    (out / "index.html").write_text(ATmpl.format(title="Scholars", h1="Scholars",
        sub="secondary witnesses — read and cite, host only what is open", sidenav=scholar_nav("index"),
        body='<div class="idx">' + "".join(links) + "</div>"
             '<div class="panel">Rule: GREEN (OA/GRETIL/Mukhabodha) ships on site. YELLOW (academia/login, HAL metadata, IRIS) is read-and-cited with links, never hosted. RED (pirated scans, commercial PDFs) never touches the repo.</div>'))
    return len(scholars)

def main():
    DIST.mkdir(parents=True, exist_ok=True)
    want = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ipvv", "vbt", "tantrasara", "authors", "scholars", "translations", "concepts", "tools"]
    done = {}
    if "ipvv" in want: done["ipvv"] = build_ipvv()
    if "vbt" in want: done["vbt"] = build_vbt()
    if "tantrasara" in want: done["tantrasara"] = build_tantrasara()
    if "authors" in want:
        for aid in MASTERS: done[aid] = build_author(aid)
    if "scholars" in want: done["scholars"] = build_scholars()
    if "translations" in want: done["translations"] = build_translations()
    if "concepts" in want: done["concepts"] = build_glossary()
    if "tools" in want: done["tools"] = build_tools()
    ship_translations()
    shutil.copy(ROOT / "data/latest.json", DIST / "data/latest.json")
    latest = "".join(f'<div class="ev"><b>{esc(i["date"])}</b> — <a href="{esc(i["url"])}">{esc(i["text"][:110])}</a></div>' for i in json.loads((ROOT / "data/latest.json").read_text()))
    masters = "".join(f'<a href="/{m}/index.html"><b>{m}</b> — bio · works map · click-in translations</a>' for m in MASTERS if m in done)
    rest = "".join(f'<a href="/{w}/index.html"><b>{w}</b> — {n} items · Sanskrit → READ → STUDY</a>' for w, n in done.items() if w not in MASTERS and w not in ("scholars", "translations", "concepts", "tools"))
    sch = '<a href="/scholars/index.html"><b>scholars</b> — secondary witnesses, linked bibliography (read/cite, host only what is open)</a>' if "scholars" in done else ""
    trn = '<a href="/translations/index.html"><b>pipeline translations</b> — English shows ONLY for gate-PASS passages</a>' if "translations" in done else ""
    con = '<a href="/concepts/index.html"><b>concepts</b> — glossary with every occurrence linked</a>' if "concepts" in done else ""
    tls = '<a href="/tools/index.html"><b>tools</b> — instant find, verse lookup (in-browser)</a>' if "tools" in done else ""
    lat = '<h3>Latest</h3>' + latest if latest else ""
    (DIST / "index.html").write_text(TMPL.format(title="Trika Library", h1="Trika Library",
        sub="masters · works · scholars · concepts · tools — display only what is formally done", work="abhinavagupta",
        body='<div class="idx">' + masters + rest + sch + trn + con + tls + "</div>" + lat))
    print("built", done)

if __name__ == "__main__":
    main()
