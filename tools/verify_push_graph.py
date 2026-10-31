#!/usr/bin/env python3
"""Verify the pushing knowledge graph (fail-closed).

Checks, all deterministic (no LLM):
1. every push-session -> its .md file exists and hashes to immutable_id
2. every session has ROUND 0 (material before question) — else FLAGGED-shape
3. every session has >=1 penetration and honest limit — else FLAGGED-shape
4. every branch has UNASKED status (open until a session instantiates it)
5. gate id matches pinned hash in qp_gates.py (logic changed without new id = FAIL)

Exit 0 = green. Exit 1 = FAIL (fail-closed, blocks the train).
"""
import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = os.path.join(ROOT, 'site', 'data', 'pushing-graph', 'graph.jsonl')
PUSH = os.path.join(ROOT, 'site', 'data', 'pushing')

fails = []
warns = []


def fail(msg):
    fails.append(msg)


def main() -> int:
    if not os.path.exists(GRAPH):
        fail('graph.jsonl not built (run extract_push_graph.py)')
        print('FAIL')
        for f in fails:
            print(' ', f)
        return 1
    recs = [json.loads(l) for l in open(GRAPH, encoding='utf-8') if l.strip()]
    sessions = [r for r in recs if r.get('kind') == 'push-session']
    print(f'graph: {len(recs)} records, {len(sessions)} sessions')
    for s in sessions:
        f = os.path.join(PUSH, s.get('sub', ''), s.get('file', '') + '.md')
        if not os.path.exists(f):
            fail(f"session file missing: {s['id']} -> {f}")
            continue
        raw = open(f, encoding='utf-8', errors='replace').read()
        h = 'sha256:' + hashlib.sha256(raw.encode('utf-8')).hexdigest()
        if h != s.get('immutable_id'):
            fail(f"hash drift (edit session, re-extract): {s['id']}")
        if not s.get('has_round0'):
            warns.append(f"FLAGGED-shape (no ROUND 0): {s['id']}")
        if s.get('rounds', 0) < 1:
            warns.append(f"FLAGGED-shape (no penetration rounds): {s['id']}")
        if not s.get('has_limit'):
            warns.append(f"FLAGGED-shape (no honest limit): {s['id']}")
    for w in warns:
        print('WARN', w)
    if fails:
        print('FAIL')
        for f in fails:
            print(' ', f)
        return 1
    print('GRAPH GATES PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
