# Pushing-as-a-service — the method pointed at any text

## Inputs
- Method: `specs/pushing/` (guide, agent spec, questionnaires) + `/pushing/` hub.
- Worked example: 73 probes (IPVV 10, Tantraloka 63) in display format.
- Corpus Hermetica was the original next mountain (sources on volume
  `source-library/hermetica/`; render packs exist, pushing prose does not — yet).

## Behavior
- Input: any text. Output: Q→GEM truth-packets in the site's probe format,
  indexed on the pushing page, appended to `corpus.jsonl` as seed questions
  (feeds the embeddings loop).
- Same grain contract as IPVV: verse/chunk scope, quoted spans, no free-floating claims.

## Phases
1. Package the agent spec + guide as a runnable (no new data).
2. First external run (Hermetica) → probes → site section.
3. Every run feeds the corpus back (embeddings-loop seed growth).
