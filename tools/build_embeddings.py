#!/usr/bin/env python3
"""Embed the corpus for RAG. Uses CF Workers AI bge-m3 (free tier).
Stores vectors in R2 as vectors.json for the Worker to read."""
import json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
pass

# Read corpus
corpus = [json.loads(l) for l in open(os.path.join(ROOT, 'site/dist/data/corpus.jsonl'), encoding='utf-8')]
print(f'corpus: {len(corpus)} records')

# We'll use the CF Workers AI REST API
import urllib.request
env = {}
with open('/root/.r2-env') as f:
    for l in f:
        l = l.strip()
        if l and '=' in l and not l.startswith('#'):
            k, v = l.split('=', 1)
            env[k.strip()] = v.strip()

account_id = env.get('CF_ACCOUNT_ID', '')
api_token = env.get('CF_API_TOKEN', '')

def embed_batch(texts):
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/baai/bge-m3'
    data = json.dumps({'text': texts}).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
    return result['result']['data']

# Embed in batches of 10
vectors = []
batch_size = 10
for i in range(0, len(corpus), batch_size):
    batch = corpus[i:i+batch_size]
    # contextual retrieval: prepend question context from argmaps (Anthropic approach)
    argmap_qs = {}
    try:
        import json as _j
        for af in __import__('glob').glob(os.path.join(ROOT, 'site/data/arguments/*.json')):
            pkt = _j.loads(open(af).read())
            argmap_qs[pkt.get('source_passage','')] = pkt.get('question','')[:200]
            argmap_qs[pkt.get('id','').split(':')[-1]] = pkt.get('question','')[:200]
    except Exception:
        pass
    texts = []
    for r in batch:
        ctx = argmap_qs.get(r.get('id',''), '') or argmap_qs.get(r.get('ref',''), '')
        # L3 (final translation) leads where present — it is the quotable text
        en = r.get('l3','') or r.get('en','')
        en = en[:800] or r.get('sa','')[:500]
        if ctx:
            texts.append(f"passage: {ctx} {en}")
        else:
            texts.append(f"passage: {en}")
    # skip empty
    for j, t in enumerate(texts):
        if not t.strip() or t == 'passage: ':
            texts[j] = 'passage: (no text)'
    try:
        embs = embed_batch(texts)
        for j, r in enumerate(batch):
            vectors.append({'id': r['id'], 'work': r['work'], 'kind': r['kind'],
                            'gate': r.get('en_gate', ''), 'ref': r.get('ref', ''),
                            'en': (r.get('en','') or '')[:500],
                            'l3': (r.get('l3','') or '')[:800],
                            'sa': (r.get('sa','') or '')[:500],
                            'vec': [round(x, 4) for x in embs[j]]})  # 4dp keeps vectors.json under Pages' 25MB/file cap
        print(f'  embedded {min(i+batch_size, len(corpus))}/{len(corpus)}')
    except Exception as e:
        print(f'  ERROR at {i}: {str(e)[:100]}')
        time.sleep(2)
    time.sleep(0.5)

# Save
out_path = os.path.join(ROOT, 'site/dist/data/vectors.json')
with open(out_path, 'w') as f:
    json.dump(vectors, f)
print(f'saved {len(vectors)} vectors to {out_path}')
print(f'size: {os.path.getsize(out_path)//1024}KB')
