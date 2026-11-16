#!/usr/bin/env python3
"""build_svread_vectors.py — rebuild RAG vectors from the svread reader bundles.

Why: the chat worker filters candidates to gate PASS/PUBLISHED/OWNER and to the
requested work. vectors.json (built 2026-11-02 from ipvv's own corpus) covered
only 13 of 87 svread works and marked stale gates (e.g. paramarthasara PASS
chunks stored as BLOCKED), so chat answered from other texts.

This script:
  1. keeps the non-svread records (ipvv passages/C1s, essays, pushing probes);
  2. replaces the svread-work records with a fresh read of /root/svread/data/*.json
     (gate taken from the bundle, English from l2/l1/l3, Sanskrit from sanskrit);
  3. honours data/holds.json (a held work is never embedded as answerable);
  4. embeds only records that are new or whose text changed (bge-m3, 1024d);
  5. writes vectors.json (default: <ipvv>/site/dist/data/vectors.json).

Usage: python3 tools/build_svread_vectors.py [--out PATH] [--dry-run]
Env: CF_ACCOUNT_ID + CF_API_TOKEN (read from /root/.r2-env if not exported).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVRED = pathlib.Path('/root/svread')
OUT_DEFAULT = ROOT / 'site' / 'dist' / 'data' / 'vectors.json'
KEEP_WORKS = {'ipvv', 'pushing', 'essays'}
EMBED_MODEL = '@cf/baai/bge-m3'
# Non-work JSON files in svread/data that must never be read as bundles.
SKIP_FILES = {'biblio', 'library', 'c1sum', 'formal', 'holds', 'layers-index',
              'mcp-registry', 'openers', 'sources', 'release-manifest', 'biblio-mirror',
              'ipk-vrtti'}


def load_env() -> dict:
    env = {}
    try:
        for line in open('/root/.r2-env'):
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    except OSError:
        pass
    for k in ('CF_ACCOUNT_ID', 'CF_API_TOKEN'):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def embed_batch(env: dict, texts: list[str]) -> list[list[float]]:
    url = f"https://api.cloudflare.com/client/v4/accounts/{env['CF_ACCOUNT_ID']}/ai/run/{EMBED_MODEL}"
    data = json.dumps({'text': texts}).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f"Bearer {env['CF_API_TOKEN']}",
        'Content-Type': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    if not result.get('success', True):
        raise RuntimeError(f"embed failed: {str(result)[:300]}")
    return result['result']['data']


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(OUT_DEFAULT))
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    existing: list[dict] = []
    if out.exists():
        existing = json.loads(out.read_text())
        print(f'existing vectors: {len(existing)}')

    keeps = [v for v in existing if v.get('work') in KEEP_WORKS]
    old_by_id = {}
    for v in existing:
        if v.get('work') in KEEP_WORKS or not v.get('id'):
            continue
        v = dict(v)
        v['_th'] = text_hash(v['id'] + '|' + (v.get('en') or '') + '|' + (v.get('l3') or '') + '|' + (v.get('sa') or ''))
        old_by_id[v['id']] = v
    print(f'kept non-svread records: {len(keeps)}')

    holds = set()
    try:
        hdoc = json.loads((SVRED / 'data' / 'holds.json').read_text())
        holds = {h.get('work') for h in hdoc.get('holds', []) if isinstance(h, dict) and h.get('work')}
    except (OSError, ValueError):
        pass
    if holds:
        print(f'held works (never answerable): {sorted(holds)}')

    fresh: list[dict] = []
    for f in sorted((SVRED / 'data').glob('*.json')):
        if f.stem in SKIP_FILES:
            continue
        try:
            d = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        if not isinstance(d, dict) or 'chunks' not in d:
            continue
        work = d.get('work') or f.stem
        if work in holds:
            continue
        for c in d.get('chunks', []):
            if not isinstance(c, dict):
                continue
            # Truncate for the Worker payload: 34 MB of full prose blows the
            # isolate memory/CPU budget. Context + citation only need ~600 chars.
            en = (c.get('l2') or c.get('l1') or '').strip()[:900]
            l3 = (c.get('l3') or '').strip()[:900]
            sa = (c.get('sanskrit') or c.get('sa') or '').strip()[:300]
            if not (en or l3 or sa):
                continue
            gate = c.get('gate') or 'BLOCKED'
            # Only answerable content needs an embedding; blocked rows are kept
            # as Sanskrit-only context (they never pass the candidate filter).
            # Only answerable rows are ever selected by the chat filter; skip
            # the rest before embedding (saves API calls and payload).
            if gate not in ('PASS', 'PUBLISHED', 'OWNER'):
                continue
            cid = c.get('chunk') or c.get('id') or ''
            rec = {
                'id': f'{work}:{cid}', 'work': work, 'kind': 'translation', 'gate': gate,
                'ref': cid, 'en': en, 'l3': l3, 'sa': sa,
            }
            rec['_th'] = text_hash(rec['id'] + '|' + en + '|' + l3 + '|' + sa)
            fresh.append(rec)

    print(f'fresh svread records: {len(fresh)} across {len(set(r["work"] for r in fresh))} works')

    # Reuse embeddings whose text is unchanged (same id + same text hash).
    to_embed = []
    for rec in fresh:
        old = old_by_id.get(rec['id'])
        if old and old.get('_th') == rec['_th'] and isinstance(old.get('vec'), list):
            rec['vec'] = old['vec']
        else:
            to_embed.append(rec)
    print(f'need embedding: {len(to_embed)} (reused {len(fresh) - len(to_embed)})')

    if args.dry_run:
        print('dry-run: not embedding, not writing')
        return 0

    if to_embed:
        env = load_env()
        if not env.get('CF_ACCOUNT_ID') or not env.get('CF_API_TOKEN'):
            print('ERROR: CF_ACCOUNT_ID/CF_API_TOKEN missing', file=sys.stderr)
            return 2
        B = 20
        for i in range(0, len(to_embed), B):
            batch = to_embed[i:i + B]
            texts = []
            for r in batch:
                body = (r.get('l3') or r.get('en') or '')[:600]
                texts.append(f"{r['work']} {r.get('ref', '')}: {body}".strip() or (r.get('sa') or '')[:300])
            vecs = embed_batch(env, texts)
            for r, v in zip(batch, vecs):
                r['vec'] = v
            if (i // B) % 5 == 0:
                print(f'  embedded {i + len(batch)}/{len(to_embed)}')

    def slim(r):
        out = {k: v for k, v in r.items() if k != '_th'}
        # Full-precision floats are ~17 bytes/number → 34 MB. Cosine is
        # unaffected by rounding to 6 dp; this keeps the Worker payload small.
        if isinstance(out.get('vec'), list):
            out['vec'] = [round(float(x), 6) for x in out['vec']]
        return out

    # Drop records the chat can never select: the candidate filter keeps only
    # PASS/PUBLISHED/OWNER, and the lexical fallback applies the same gate.
    # Blocked/MACHINE_DRAFT rows are ~45% of the payload and unused.
    ANSWERABLE = {'PASS', 'PUBLISHED', 'OWNER'}
    final = [slim(r) for r in keeps + fresh if r.get('gate') in ANSWERABLE]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(final, ensure_ascii=False))
    works = sorted({r.get('work') for r in final})
    answerable = sorted({r.get('work') for r in final if r.get('gate') in ('PASS', 'PUBLISHED', 'OWNER')})
    print(f'wrote {out} — {len(final)} records, {len(works)} work names, '
          f'{len(answerable)} answerable')
    print('answerable works:', ', '.join(answerable))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
