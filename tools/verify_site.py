#!/usr/bin/env python3
"""verify_site.py — site-lane gates (fail-closed for site/data + dist).

Pipeline-owned paths (works/*, samples/*) are reported as WARNINGS only —
never fail here; file those to the pipeline lane instead (see logs/qa/).
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails, warns = [], []

def fail(m): fails.append(m)
def warn(m): warns.append("WARN " + m)

# 1. translations gate integrity (site/data — FAIL)
for f in glob.glob(os.path.join(ROOT, 'site/data/translations/*.json')):
    w = os.path.basename(f)[:-5]
    for it in json.load(open(f)):
        g, has_en = it.get('gate'), bool(it.get('l1') or it.get('l2'))
        if g == 'PASS' and not has_en:
            fail(f'{w}/{it.get("chunk")}: PASS with no English')
        if g != 'PASS' and has_en:
            fail(f'{w}/{it.get("chunk")}: {g} with English present (fail-closed breach)')

# 2. audio manifest vs mp3s (site/data + dist — FAIL)
for aj in glob.glob(os.path.join(ROOT, 'site/data/audio-*.json')):
    A = json.load(open(aj))
    for v in A['verses']:
        for base in ('site/static-audio', 'site/dist/audio'):
            p = os.path.join(ROOT, base, A['work'], v['id'] + '.mp3')
            if not os.path.exists(p):
                fail(f'missing mp3: {base}/{A["work"]}/{v["id"]}.mp3')

# 3. read_alongside resolution (site/data — FAIL)
ra = json.load(open(os.path.join(ROOT, 'site/data/read_alongside.json')))
sch = {s['id'] for s in json.load(open(os.path.join(ROOT, 'site/data/scholars.json')))}
for aid, rs in ra.items():
    if not os.path.exists(os.path.join(ROOT, f'site/data/authors/{aid}.json')):
        fail(f'alongside: master file missing: {aid}')
    for r in rs:
        if r['scholar'] not in sch:
            fail(f'alongside: unknown scholar {r["scholar"]} (from {aid})')

# 4. search-index coverage (dist — FAIL)
idx_path = os.path.join(ROOT, 'site/dist/data/search-index.json')
if os.path.exists(idx_path):
    urls = {e.get('u') for e in json.load(open(idx_path))}
    for f in glob.glob(os.path.join(ROOT, 'site/dist/**/*.html'), recursive=True):
        u = '/' + os.path.relpath(f, os.path.join(ROOT, 'site/dist'))
        if u not in urls:
            fail(f'search-index missing: {u}')
else:
    fail('search-index.json not built')

# 5. unfilled placeholders in dist (FAIL)
for f in glob.glob(os.path.join(ROOT, 'site/dist/**/*.html'), recursive=True):
    t = open(f, encoding='utf-8', errors='replace').read()
    for ph in ('{title}', '{body}', '{kicker}', '{subtitle}', '{recitejs}', '{sidenav}'):
        if ph in t:
            fail(f'unfilled {ph} in {os.path.relpath(f, ROOT)}')
            break

# 6. dist freshness vs build.py (FAIL — rebuild before commit)
bpy = os.path.join(ROOT, 'site/build.py')
dix = os.path.join(ROOT, 'site/dist/index.html')
if os.path.exists(dix) and os.path.getmtime(bpy) > os.path.getmtime(dix):
    fail('site/build.py newer than site/dist — rebuild before commit')

# 7. samples C1 band (pipeline-owned — WARN only)
for f in glob.glob(os.path.join(ROOT, 'samples/*/C1-*.md')):
    txt = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'^## (.+)$', txt, re.M):
        start = m.end()
        nxt = txt.find('\n## ', start)
        words = len(txt[start:nxt if nxt > 0 else len(txt)].split())
        if words and (words < 100 or words > 450):
            warn(f'{os.path.relpath(f, ROOT)} §{m.group(1)[:40]}: {words}w outside 100–450')

# 8. WORK.md DONE-vs-gate (pipeline-owned — WARN only)
for f in glob.glob(os.path.join(ROOT, 'works/*/WORK.md')):
    head = open(f, encoding='utf-8', errors='replace').readline()
    body = open(f, encoding='utf-8', errors='replace').read()
    m = re.search(r'Gate:\s*(\d+)\s*PASS', body)
    if 'DONE' in head and m and m.group(1) == '0':
        warn(f'{os.path.relpath(f, ROOT)}: DONE with 0 PASS')

for w in warns:
    print(w)
if fails:
    print(f'SITE GATES FAILED ({len(fails)}):')
    for m in fails:
        print('  FAIL', m)
    sys.exit(1)
print(f'SITE GATES PASS ({len(warns)} warnings)')
