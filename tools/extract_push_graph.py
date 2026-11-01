#!/usr/bin/env python3
"""Extract pushing knowledge graph from session .md files.

Reads site/data/pushing/*/*.md with the standard structure
(title / ROUND 0..N / PENETRATION / claim statuses / HONEST LIMIT / BRANCHES)
and emits graph.jsonl: session, question, claim, penetration, branch nodes
with follows-from / instantiates / branches-to edges.

Deterministic: same bytes in -> same JSON out. Never hand-edit the output;
fix the session and re-run. Verify with verify_push_graph.py.
"""
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUSH = os.path.join(ROOT, 'site', 'data', 'pushing')
OUT = os.path.join(ROOT, 'site', 'data', 'pushing-graph', 'graph.jsonl')


def sha12(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:12]


def parse_session(path: str, sub: str) -> list:
    raw = open(path, encoding='utf-8', errors='replace').read()
    stem = os.path.splitext(os.path.basename(path))[0]
    recs = []

    m = re.search(r'^# LOGICVID SESSION [—-] (.*)$', raw, re.M)
    question = m.group(1).strip() if m else stem
    work = sub if sub not in ('ipvv', 'tantraloka', 'research', 'rasa') else None
    # work guess: scaffold files name it; sessions inherit sub unless bodha-style dir
    if sub == 'bodhapancadasika':
        work = 'bodhapancadasika'
    elif sub in ('ipvv', 'tantraloka'):
        # sessions in these dirs may cover multiple works; leave work null
        # unless the scaffold table says otherwise (filled by scaffold parse)
        work = sub

    sid = f"pt:session:{work or sub}:{stem.lower().replace('_', '-')[:60]}"
    rounds = len(re.findall(r'^## ROUND \d+', raw, re.M))
    pens = re.findall(r'> \*\*PENETRATION (\d+)(.*?)\*\*', raw, re.S)
    has_r0 = bool(re.search(r'^## ROUND 0', raw, re.M))
    has_limit = bool(re.search(r'HONEST LIMIT', raw))
    branches = re.findall(r'> \*\*Branch ([A-Z0-9]+) [—-] (.*?)(?:\*\*|$)', raw)
    verdict = None
    vm = re.search(r'verdict[:\s]+([A-Z/ \-]+)', raw, re.I)
    if vm:
        verdict = vm.group(1).strip()[:60]

    shape = None
    sm = re.search(r'[Cc]hain shape:\s*([^\n)]+)', raw)
    if sm:
        shape = sm.group(1).strip()

    recs.append({
        'id': sid, 'kind': 'push-session',
        'work': work, 'sub': sub, 'file': stem,
        'question': question[:500],
        'shape': shape, 'rounds': rounds,
        'has_round0': has_r0, 'has_limit': has_limit,
        'verdict': verdict,
        'branches': [b[0] for b in branches],
        'immutable_id': 'sha256:' + hashlib.sha256(raw.encode('utf-8')).hexdigest(),
        'gate': 'pushing/graph-extract-v1', 'status': 'MACHINE_DRAFT',
    })
    for i, p in enumerate(pens):
        recs.append({
            'id': f'{sid}:penetration-{p[0]}',
            'kind': 'penetration', 'session': sid,
            'n': int(p[0]), 'text': p[1].strip()[:1000],
        })
    for code, title in branches:
        recs.append({
            'id': f'{sid}:branch-{code}',
            'kind': 'open-branch', 'session': sid,
            'code': code, 'title': title.strip()[:300],
            'status': 'UNASKED',
        })
    return recs


def main() -> int:
    out = []
    for sub in sorted(os.listdir(PUSH)):
        sdir = os.path.join(PUSH, sub)
        if not os.path.isdir(sdir):
            continue
        for f in sorted(glob.glob(os.path.join(sdir, '*.md'))):
            # scaffold files (PUSHING-*.md) get a session-table parse instead
            if os.path.basename(f).startswith('PUSHING-'):
                continue
            try:
                out.extend(parse_session(f, sub))
            except Exception as e:
                print(f'  SKIP {f}: {e}', file=sys.stderr)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n')
    print(f'graph: {len(out)} records -> {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
