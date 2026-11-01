# Chat copilot — pushing live, every question

*The chat doesn't just answer; it fires a pushing chain per question, records it, and points deeper.
Human-led: human asks + judges + picks branches; copilot retrieves + reconstructs + records.*

## Copilot loop (per question)

```
you ask ("why would Śiva forget?")
  ├─→ retrieve (texts + chains + prior trajectories)
  ├─→ ROUND 0 (quoted material — Sanskrit always, English only if PASS)
  ├─→ your question, sharpened (template match or new node)
  ├─→ ROUND 1 (the text's answer, restated exactly)
  ├─→ PENETRATION (the spot it asserts without proving)
  ├─→ verdict (GEM / PARTIAL / HONEST-LIMIT) + claim statuses
  ├─→ answer you (the chain IS the answer — reasoning-first, not summary-first)
  ├─→ record (session stub + graph nodes + receipt, MACHINE_DRAFT)
  └─→ "push deeper:" 2–3 branches (forced next questions this chain opened)
        → you pick → next round fires on that branch
```

## Earned reactions (tied to chain mechanics, never canned)

- New UNASKED cell opened → "ooh good question — nobody's pushed this yet."
- Penetration lands → "there it is — [text] asserts [X] here, doesn't prove it."
- Honest limit hit → "and that's where [text] stops. doesn't go there."
- Prior GEM contradicted → "huh. [A] said [X] but [B] just said [Y]. live one."
- Re-ask with new sessions → "we did this — [verdict]. [new] landed since, want the update?"
- Dissolution (S5-type) → ":') hahahah" (the laugh IS the verdict).

Never generic praise. Every reaction carries information (which cell, which penetration, which limit).

## "Good" button (the only promotion path)

Tap "good" → PROMOTE receipt → graph grows → next re-embed carries it. Your judgment is the only grant. No auto-promote, no judge model (Phase 4 later).

## Streaming (realtime feel)

DashScope SSE (`stream: true`): first token <1s, chain streams in order (ROUND 0 → question → ROUND 1 → penetration → verdict → branches). Skip rerank when top-1 margin is wide. `ctx.waitUntil()` for D1 writes. ~50 lines total in Worker.
