# Embeddings v2 — beyond flat RAG (updated from Oct 2026 research)

## Why flat RAG is the floor, not the ceiling
Basic RAG: embed chunks → cosine → top-k → generate. Works, but treats every
passage as an independent bag of words. We have structured data — arguments with
premises, conclusions, tensions, source passages, gate labels, scholars. Flat RAG
ignores all of that structure.

## What we have that makes us better than flat RAG
1. Argument packets (83): conclusion → premises → passage_id → Sanskrit
2. Contentions (16): claim + source_span + falsifier + support/attack targets
3. Themes (9 proposals): overlapping communities with edge evidence
4. Scholars (36): read-alongside links, bibliographies
5. Gate labels: PASS/BLOCKED/PUBLISHED/OWNER (confidence signal)
6. Pushing probes (73): question-shaped seed data
7. Essays (22): long-form Q→thesis pairs

## Better approaches (ranked by value for our stack)

### 1. Graph traversal over argument packets (NO new model needed)
Instead of embedding flat text and finding similar text:
- Embed the question
- Find the most relevant argument packet (by embedding similarity)
- Traverse the argument graph: premises → related passages → tensions → contentions
- Gather ALL evidence from the traversal, not just the top-k cosine hits
- Generate from the gathered evidence

This uses our existing structure as the retrieval mechanism. The embedding is just
the entry point; the graph does the real retrieval.

### 2. Hybrid retrieval (dense + sparse + structured)
- Dense: bge-m3 or qwen3-embedding-0.6b (already available on CF)
- Sparse: BM25 over Sanskrit terms + IAST + English
- Structured: graph traversal over argument packets
- Combine: reciprocal rank fusion (RRF) of all three signals
- Rerank: bge-reranker-base cross-encoder on top-20

### 3. Contextual retrieval (Anthropic approach)
Before embedding each chunk, prepend context: "This passage is from Abhinavagupta's
IPVV, Vol 2, chunk V2-O, which argues that ordered experience requires an
order-less support. The chunk's premises are: ..."
This dramatically improves retrieval quality. We can generate context from our
argmaps (which already contain the question/issue/premises).

### 4. Multi-hop retrieval
For complex questions ("How does the IPVV argue that recognition is felt?"):
- Hop 1: find chunks mentioning recognition + felt
- Hop 2: find chunks cited by those (via see_also, RELATED relations)
- Hop 3: find chunks sharing terms/concepts
- Gather all, rerank, generate

### 5. Gate-aware confidence weighting
At retrieval time, weight results by gate status:
- PUBLISHED: weight 1.0 (highest trust)
- PASS: weight 0.9
- OWNER: weight 0.7 (essays/probes — owner voice, not scripture)
- BLOCKED: weight 0.0 (excluded entirely — Sanskrit only, no English)

This is already in the data; just needs to be applied at retrieval time.

## Free-tier models available (CF Workers AI)
- bge-m3: 1024-dim, multilingual, 60k context, cheapest (1075 neurons/M tokens)
- qwen3-embedding-0.6b: 1024-dim, SOTA family, same price
- bge-reranker-base: cross-encoder reranker (live in Worker)
- Generation: qwen3.8-omni-flash via DashScope Singapore (live in Worker; deepseek-v4-flash fallback only)

## What NOT to do
- Don't chase MTEB top (Qwen3-8B) — our corpus is ~700 items, bottleneck is
  coverage + structure, not 2 points of retrieval
- Don't store 1024-dim floats forever — MRL/truncation when index passes 100k
- Don't use a single flat vector per chunk — our structure is richer than that

## Recommended implementation
1. Keep bge-m3 for embedding (already done, vectors in R2)
2. Add contextual retrieval: prepend argmap question to each chunk before embedding
3. Add graph traversal: after cosine retrieval, follow argument packet edges
4. Add gate-aware weighting: exclude BLOCKED, weight by gate status
5. Add multi-hop: follow see_also/RELATED edges for complex queries
6. Rerank with bge-reranker-base (already in Worker)
7. Generate with qwen3.8-omni-flash via DashScope (live in Worker; stream SSE for realtime feel)

## What this gives us
- Better retrieval quality without new models (uses existing structure)
- Honest abstention (BLOCKED chunks never surface English)
- Argument-grounded answers (premises → conclusion → source)
- Cross-tradition synthesis (multi-text chat follows edges across works)
