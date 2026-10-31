#!/usr/bin/env python3
"""Export style training dataset for Unsloth Colab.

Produces a JSONL of instruction-completion pairs:
  instruction: "Translate this Sanskrit into [STYLE] English. Preserve meaning exactly."
  completion:  the target-style English translation

Sources:
  - PASS translations (house L2 as reference style)
  - owner exemplars (styles/*.json)
  - BLOCKED chunks included with Sanskrit-only (for style transfer training)
"""
import json, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site/dist/data/style_dataset.jsonl")

records = []

# 1. PASS translations (L2 as target)
for f in sorted(glob.glob(os.path.join(ROOT, 'site/data/translations/*.json'))):
    for it in json.load(open(f)):
        if it.get('gate') == 'PASS' and (it.get('l2') or it.get('l1')):
            records.append({
                "instruction": "Translate this Sanskrit into clear, scholarly English. Preserve meaning exactly.",
                "output": (it.get('l2') or it.get('l1','')).replace('\n', ' ')[:500],
                "sanskrit": it.get('sanskrit', ''),
                "work": os.path.basename(f)[:-5],
                "source": "pipeline_L2",
                "gate": "PASS"
            })

# 2. Owner exemplars (styles/*.json)
for f in sorted(glob.glob(os.path.join(ROOT, 'site/data/styles/*.json'))):
    style = json.load(open(f))
    sid = style.get('id', os.path.basename(f)[:-5])
    for ex in style.get('exemplars', []):
        if isinstance(ex, dict) and ex.get('sanskrit') and ex.get('english'):
            records.append({
                "instruction": f"Translate this Sanskrit in the {sid} style. Preserve meaning exactly.",
                "output": ex['english'].replace('\n', ' ')[:500],
                "sanskrit": ex['sanskrit'],
                "work": "owner",
                "source": f"style:{sid}",
                "gate": "OWNER"
            })

# 3. BLOCKED chunks (Sanskrit-only, for style transfer conditioning)
for f in sorted(glob.glob(os.path.join(ROOT, 'site/data/translations/*.json'))):
    for it in json.load(open(f)):
        if it.get('gate') == 'BLOCKED' and it.get('sanskrit'):
            records.append({
                "instruction": "Translate this Sanskrit into clear, scholarly English. Preserve meaning exactly.",
                "output": "",
                "sanskrit": it['sanskrit'],
                "work": os.path.basename(f)[:-5],
                "source": "pipeline_BULK",
                "gate": "BLOCKED"
            })

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as fh:
    for r in records:
        fh.write(json.dumps(r, ensure_ascii=False) + '\n')


# 4. Argument packet conclusions (proposition-level English)
for f in sorted(glob.glob(os.path.join(ROOT, 'site/data/arguments/*.json'))):
    pkt = json.load(open(f))
    concl = pkt.get('conclusion', {}).get('text', '')
    sa = pkt.get('sanskrit', '')
    if concl and sa:
        records.append({
            "instruction": "Summarize what this Sanskrit passage argues, in clear English.",
            "output": concl.replace('\n', ' ')[:500],
            "sanskrit": sa[:800],
            "work": "argument",
            "source": "argument_packet",
            "gate": "MACHINE_DRAFT"
        })
    # Also include premises
    for pr in pkt.get('premises', [])[:2]:
        if pr.get('text') and sa:
            records.append({
                "instruction": "Translate this Sanskrit passage into clear English.",
                "output": pr['text'].replace('\n', ' ')[:500],
                "sanskrit": sa[:800],
                "work": "argument",
                "source": "argument_premise",
                "gate": "MACHINE_DRAFT"
            })

# 5. C1 bodies (commentary-style English)
for f in sorted(glob.glob(os.path.join(ROOT, 'site/data/translations/*.json'))):
    for it in json.load(open(f)):
        if it.get('gate') == 'PASS' and it.get('l2'):
            records.append({
                "instruction": "Explain what this passage means in plain English.",
                "output": it['l2'].replace('\n', ' ')[:500],
                "sanskrit": it.get('sanskrit', ''),
                "work": os.path.basename(f)[:-5],
                "source": "commentary_style",
                "gate": "PASS"
            })

# Also produce a HF Trainer-compatible format
hf_out = OUT.replace('.jsonl', '-hf.jsonl')
with open(hf_out, 'w', encoding='utf-8') as fh:
    for r in records:
        if r['output']:
            fh.write(json.dumps({
                "text": f"### Instruction:\n{r['instruction']}\n\n### Sanskrit:\n{r['sanskrit'][:800]}\n\n### Response:\n{r['output']}"
            }, ensure_ascii=False) + '\n')

print(f"records: {len(records)} (with output: {sum(1 for r in records if r['output'])})")
print(f"saved: {OUT}")
print(f"saved: {hf_out}")
