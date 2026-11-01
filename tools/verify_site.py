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
        # traceability: every chunk resolves to a vendored root + license + immutable id
        if not it.get('source_file'):
            fail(f'{w}/{it.get("chunk")}: no source_file (untraceable Sanskrit)')
        if not it.get('source_license'):
            fail(f'{w}/{it.get("chunk")}: no source_license (unembeddable)')
        if not it.get('immutable_id'):
            fail(f'{w}/{it.get("chunk")}: no immutable_id')

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

# 5b. argmap + C1 integrity (site/data — FAIL)
for d, kind in [('argmaps', 'argmap'), ('c1', 'C1')]:
    base = os.path.join(ROOT, 'site/data', d)
    if not os.path.isdir(base):
        continue
    for f in glob.glob(os.path.join(base, '**/*.md'), recursive=True):
        words = len(open(f, encoding='utf-8', errors='replace').read().split())
        rel = os.path.relpath(f, ROOT)
        if kind == 'C1' and words < 100:
            fail(f'C1 too short ({words}w < 100): {rel}')
        if kind == 'C1' and words > 450:
            fail(f'C1 too long ({words}w > 450): {rel}')
        if kind == 'argmap' and words < 150:
            fail(f'argmap too short ({words}w < 150): {rel}')

# 6. receipts coverage (dist — FAIL)
_rp = os.path.join(ROOT, 'site/dist/data/receipts.jsonl')
if os.path.exists(_rp):
    _rn = sum(1 for _ in open(_rp, encoding='utf-8'))
    _tn = sum(len(json.load(open(f))) for f in glob.glob(os.path.join(ROOT, 'site/data/translations/*.json')))
    _pn = len(glob.glob('/root/patalacheckpoints/data/published/ipvv/pt-passage-*.json'))
    _an = len(glob.glob(os.path.join(ROOT, 'site/data/arguments/*.json')))
    if _rn != _tn + _pn + _an:
        fail(f'receipts.jsonl has {_rn} records, expected {_tn + _pn + _an} (translations + published + arguments)')
else:
    fail('receipts.jsonl not built')
# 6b. kernel verification: gate registry pinned + receipt ids recompute (FAIL)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
try:
    from qp_acom.canonical import canonical, sha256_hex
    from qp_acom.gates import program_hash
    import qp_gates  # noqa: registers ipvv/* gates into the kernel registry
    _pinned = {
        "ipvv/has-source-v1": "sha256:ad16330b14e8b585eea1bd630b2d33e30301b146ac3c9e631961461326c129b5",
        "ipvv/has-license-v1": "sha256:b32a372f4db612425803868f7ef46aec3b069eafb6d0ac6e4e862d066548eced",
        "ipvv/has-immutable-id-v1": "sha256:cb644734619b646c262d7b8b9b578ab2b2f1188bea72d32cf08a3ddfa6200c42",
        "ipvv/gate-consistent-v1": "sha256:bdbf5e44faa8159e40179f5a83762b23ba985519b88a49a82c814a368e6f174c",
        "ipvv/checks-pass-v1": "sha256:dd803a9c03b7bf8243e7817abc34705faeebe48741d78910d0af6968c9a1daef",
        "pushing/graph-extract-v1": "sha256:616dd22c0b65fbdeb60bf4e3e4a433a81cff4729914c077b794d1eb227d53a1b",
    }
    for _g, _h in _pinned.items():
        if program_hash(_g) != _h:
            fail(f'gate logic changed without new id: {_g} (mint a new gate id)')
    _bad = 0
    for _ln in open(_rp, encoding='utf-8'):
        _r = json.loads(_ln)
        _body = {k: v for k, v in _r.items() if k not in ("id", "signature", "signer")}
        _prefix = "receipt:arg:" if str(_r.get("id","")).startswith("receipt:arg:") else "receipt:"
        _suffix_len = 16
        _want = _prefix + sha256_hex(canonical(_body))[:_suffix_len]
        if _r.get("id") != _want:
            _bad += 1
    if _bad:
        fail(f'{_bad} receipts fail id recomputation (tampered or stale kernel)')
except Exception as e:
    fail(f'kernel verification error: {e!r}')
# 7. dist freshness vs build.py (FAIL — rebuild before commit)
bpy = os.path.join(ROOT, 'site/build.py')
dix = os.path.join(ROOT, 'site/dist/index.html')
if os.path.exists(dix) and os.path.getmtime(bpy) > os.path.getmtime(dix):
    fail('site/build.py newer than site/dist — rebuild before commit')

# 8. samples C1 band (pipeline-owned — WARN only)
for f in glob.glob(os.path.join(ROOT, 'samples/*/C1-*.md')):
    txt = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'^## (.+)$', txt, re.M):
        start = m.end()
        nxt = txt.find('\n## ', start)
        words = len(txt[start:nxt if nxt > 0 else len(txt)].split())
        if words and (words < 100 or words > 450):
            warn(f'{os.path.relpath(f, ROOT)} §{m.group(1)[:40]}: {words}w outside 100–450')

# 9a. argument packet integrity (site/data — FAIL)
for f in glob.glob(os.path.join(ROOT, 'site/data/arguments/*.json')):
    pkt = json.load(open(f))
    for req in ('id', 'work_id', 'passage_id', 'title', 'question', 'premises', 'conclusion', 'strength', 'status', 'source_passage'):
        if req not in pkt:
            fail(f'argument packet missing {req}: {os.path.basename(f)}')
    if not pkt.get('premises'):
        fail(f'argument packet has no premises: {os.path.basename(f)}')
    if not pkt.get('source_passage'):
        fail(f'argument packet has no source_passage: {os.path.basename(f)}')
# 9b. argument receipt coverage (dist — FAIL)
_rp = os.path.join(ROOT, 'site/dist/data/receipts.jsonl')
if os.path.exists(_rp):
    _ids = {json.loads(l).get('id','') for l in open(_rp, encoding='utf-8')}
    # argument receipts: check count matches packet count
    _nargs = len(glob.glob(os.path.join(ROOT, 'site/data/arguments/*.json')))
    _nargr = sum(1 for l in open(_rp, encoding='utf-8') if '"ARGUMENT-DISPLAY"' in l)
    if _nargr != _nargs:
        fail(f'argument receipts: {_nargr} found, {_nargs} packets expected')
# 9. WORK.md DONE-vs-gate (pipeline-owned — WARN only)
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
