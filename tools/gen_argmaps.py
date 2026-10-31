#!/usr/bin/env python3
"""Batch-generate argument maps for all translation chunks.

For each chunk with Sanskrit + L1/L2, calls Qwen3.8-Omni to produce
a structured argmap in the IPVV format:
  # title
  ## 1. What is at issue
  ## 2. The argument, reconstructed step by step
  ## 3. Unresolved / uncertain (not invented)
  ## 4. Decision for L2

Saves to site/data/argmaps/{work}/{chunk}.md
Gates: every argmap must have all 4 sections, 200+ words, no ungrounded claims.
"""
import json, glob, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

# Load DashScope key from .r2-env
env = {}
with open('/root/.r2-env') as f:
    for l in f:
        l = l.strip()
        if l and '=' in l and not l.startswith('#'):
            k, v = l.split('=', 1)
            env[k.strip()] = v.strip()
API_KEY = env.get('CF_API_TOKEN', '')

def call_qwen(prompt, max_tokens=1500):
    data = json.dumps({
        'model': 'qwen3.8-omni-flash',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': max_tokens,
        'reasoning_effort': 'medium'
    }).encode()
    req = urllib.request.Request(
        'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions',
        data=data,
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
        }
    )
    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read())
    return result['choices'][0]['message'].get('content', '')

ARGMAP_PROMPT = """You are reconstructing the argument of a Sanskrit philosophical text passage.

Given the Sanskrit source and its English translation, produce an argument map in EXACTLY this format:

# <title identifying the work and passage>
## 1. What is at issue
<The central question this passage addresses, 2-4 sentences>
## 2. The argument, reconstructed step by step
<The argument as steps: premise → inference → conclusion. Each step references the Sanskrit terms. 100-300 words.>
## 3. Unresolved / uncertain (not invented)
<What the passage leaves open or ambiguous. If nothing, write "None identified.">
## 4. Decision for L2
<Proceed or hold, with 1-2 sentence justification>

Rules:
- Only reconstruct what the text actually argues. Never invent premises.
- Reference Sanskrit terms in IAST with glosses in parentheses.
- Be specific about the inferential structure (what follows from what).
- If the passage is devotional (not argumentative), say so honestly.

Work: {work}
Chunk: {chunk}
Sanskrit: {sanskrit}
English: {english}
"""

def gate_argmap(text):
    """Gate: must have all 4 sections, 200+ words."""
    sections = ['## 1.', '## 2.', '## 3.', '## 4.']
    for s in sections:
        if s not in text:
            return False, f'missing section {s}'
    words = len(text.split())
    if words < 200:
        return False, f'too short: {words} words'
    return True, f'{words} words'

def main():
    target_work = sys.argv[1] if len(sys.argv) > 1 else None
    out_dir = os.path.join(ROOT, 'site/data/argmaps')
    os.makedirs(out_dir, exist_ok=True)

    works = sorted(glob.glob(os.path.join(ROOT, 'site/data/translations/*.json')))
    if target_work:
        works = [w for w in works if target_work in w]

    total, ok, fail = 0, 0, 0
    for wf in works:
        work = os.path.basename(wf)[:-5]
        if work == 'ipvv':
            continue  # already has argmaps
        work_dir = os.path.join(out_dir, work)
        os.makedirs(work_dir, exist_ok=True)
        items = json.load(open(wf))
        for it in items:
            total += 1
            chunk = it.get('chunk', '?')
            out_path = os.path.join(work_dir, f'{chunk}.md')
            if os.path.exists(out_path):
                ok += 1
                continue
            sa = it.get('sanskrit', '')
            en = it.get('l2') or it.get('l1') or ''
            if not sa or not en:
                fail += 1
                continue
            prompt = ARGMAP_PROMPT.format(
                work=work, chunk=chunk,
                sanskrit=sa[:2000], english=en[:2000]
            )
            try:
                result = call_qwen(prompt)
                passed, reason = gate_argmap(result)
                if passed:
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(result)
                    ok += 1
                    print(f'  OK {work}/{chunk}: {reason}')
                else:
                    fail += 1
                    print(f'  GATE {work}/{chunk}: {reason}')
            except Exception as e:
                fail += 1
                print(f'  ERR {work}/{chunk}: {str(e)[:80]}')
            time.sleep(0.3)

    print(f'\nTotal: {total}, OK: {ok}, Fail: {fail}')

if __name__ == '__main__':
    main()
