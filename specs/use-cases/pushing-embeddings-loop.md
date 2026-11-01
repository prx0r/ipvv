# Pushing ↔ embeddings loop (growth design)

*Pushing probes are what humans will ask. The index converges on real curiosity.
Human-led: human asks, tree records, chat answers, enquiry grows the seed.*

## The loop

```
human asks ──→ match template ──→ retrieve (texts + chains) ──→ answer
     │                │                       │                      │
     │          hit: link query         graph traversal       store Q&A
     │          miss: new node          + chain context       + gate labels
     │          (UNASKED everywhere)          │                      │
     │                                         ▼                      ▼
     │                                  pushing-style            growth:
     │                                  analysis                 answered pair
     │                                  (ROUND 0→1→2)            → re-embed
     │                                         │
     └──────── human reviews ◄── MACHINE_DRAFT  ┘
              (accept = grant;
               accept grows graph)
```

## Three additions (all small, no new services)

1. **Templates embedded** (build time): portable questions as `kind: question-template`, `question:` prefix, same space as human queries. ~5 now (bondage/liberation arc), grows with sessions.
2. **Template match at query time** (Worker, ~10 lines): cosine vs template vecs; hit → pull sessions + verdicts + claims + honest limits as chain context. Miss → new question node (UNASKED everywhere = pushing TODO).
3. **Answer → graph edge** (D1 + 1 column): store `template` with Q&A. Re-embed picks up new nodes + answered pairs. Abstain → corpus gap flag + UNASKED cell marked NEEDED.

## Why it works

Templates live in question-space; sessions/chains in passage-space with contextual prefixes (`question: {template}` → `passage: {chain summary} {text}`). Retrieval finds reasoning, not just text. Gate-weighting excludes BLOCKED English (fail-closed inherited). Reranker sees question+chain+passage together.

## Trajectories (chats as replayable paths)

Resolved enquiry = trajectory (question → template → sessions → passages → answer → resolution signal). New similar question → match trajectory → replay path with live retrieval (new sessions/gates participate) → better answer than last time. Resolution signal is behavioral (branch-forward = accepted, re-ask = failed), never a judge model.
