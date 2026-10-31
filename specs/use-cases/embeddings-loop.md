# Embeddings loop — seed with pushing, grow with humans (nibbanahelp relay pattern)

## Core insight
Pregenerated pushing Q→GEM pairs **are** what a human is likely to ask. Seed the
index with them; as humans ask more, append the answered pairs. The index converges
on real curiosity instead of guessed coverage.

## Seed data (exists now)
- 73 pushing probes: each is a human-shaped question (Q1–Q28 extracts, full sessions
  with Q→GEM structure) plus the text's own answer.
- 22 essays: long-form Q→thesis pairs (title = question, body = argued answer).
- 100 glossary terms: term → definition + linked passages.
- Index seed records as pseudo-QA: `query = probe question`, `doc = GEM + source spans`.

## Loop
1. Embed seed (bge-m3 multilingual, 1024-dim; task prefixes: `question:` / `passage:`).
2. Retrieve top-20 cosine → rerank to top-5 (bge-reranker-base cross-encoder).
3. Human asks → answered from corpus (gate rules below) → **answered pair appended**
   to the index with its gate label. Index grows along actual use.
4. Periodic review: pairs that required abstention flag corpus gaps (drives translation priority).

## Scoping (chat per text → multi-text)
- **Per-text chat:** namespace filter `work == X` (e.g. only `ipvv`, only `vbt`).
  The bot answers *only* from that text. No leakage by construction (filter, not prompt).
- **Multi-text chat:** union namespaces (`work IN (ipvv, tantraloka, spanda)`).
  User adds texts; retrieval spans exactly those. Answers cite which text each span came from.
- Namespaces are record fields (`work`, `kind`, `ref`) — no re-embedding to rescope.

## Gate rules (apply at retrieval, not generation)
- `en_gate IN (PASS, PUBLISHED, OWNER)` → English admissible.
- `en_gate == BLOCKED` → Sanskrit only + withheld notice. The English field is
  excluded from the embedded text, not just hidden at display.
- Essays/probes (`OWNER`) → admissible, labeled owner-voice (not scripture).

## Cost (free tier, per nibbanahelp relay)
- bge-m3: ~1075 neurons/M tokens (cheapest). Rerank ~0.01 neurons/query.
- Corpus ~454 records: vectors file is trivial. fp16/MRL only past ~100k items.
