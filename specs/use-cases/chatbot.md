# Chatbot — gate-aware Trika tutor

## Inputs (all exist)
- `site/dist/data/corpus.jsonl` — 454 records, stable ids, gate labels.
- Argmaps (48 + V3B deep set) + C1 bodies + essays + themes evidence.
- `site/data/scholars.json` — citations that resolve.
- Recitation player + chants (spoken answers).

## Behavior
- RAG over the corpus (bge-m3 or Qwen3-Embedding, rerank stage — relay already
  verified free-tier in nibbanahelp `research/embeddings-2026-10.md`).
- Three registers, one bot: L1 (what it says) / L2 (what it means) / essays (what follows).
- Arguments, not passages: argmaps ground *why* answers (premises → objections → inferences).
- Voice: verse-first Sanskrit, then English — the 4 recitation modes.

## Honesty rules (structural, not prompted)
- Gate label rides every record: PASS/PUBLISHED/OWNER answer; BLOCKED answers
  with Sanskrit + "English withheld" — never translated by the bot.
- Abstention is a data property. No record → "not in the corpus," never invention.
- Every answer links passage page + scholar + witness. No bare claims.

## Phases
1. API over corpus.jsonl (weekend; no new data).
2. Argmap-grounded answers (proof-chains as context blocks).
3. Voice replies (chant/synth pipeline).
