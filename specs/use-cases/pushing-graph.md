# Pushing knowledge graph — qprivately-native design

*The pushing sessions as a machine-readable graph, derived (never edited), verified, receipted.
Seven qprivately objects; one ID grammar; fail-closed verification; no orphans.*

## Node types (all `pt:` namespaced)

| Node | ID pattern | Source |
|---|---|---|
| question (portable template) | `pt:question:{slug}` | extracted from session titles + branch lines |
| session | `pt:session:{work}:{slug}` | one pushing .md file |
| claim | `pt:claim:{work}:{slug}:{n}` | penetration with status |
| penetration | `{session}:penetration-{n}` | ROUND N result |
| open branch | `{session}:branch-{code}` | `> **Branch XX` lines, status UNASKED |
| chain shape | `pt:shape:{slug}` | 6 shapes (extraction-branch, gem-honest-crux, doctrine-first-person, thread-unification, mechanism-theodicy-objections, abstract-felt-bridge) |
| asks edge | `pt:asks:{template}:{work}` | template × work matrix; session or UNASKED |

## Claim mapping (qprivately objects)

- Each session = CLAIM (statement=question, domain=pushing, result from verdict: GEM→TRUE-ish? No — result stays UNKNOWN until PROMOTE; verdict recorded separately).
- Each quoted passage = EVIDENCE (metric=quote, value=text, source=corpus-id or Sanskrit file:lines).
- Each extraction = transition receipt (RESOLVE for GEM, CHALLENGE for honest-crux/prosecution, OBSERVE for STATED, PROMOTE on human accept).
- Strength (PROVED→SPECULATIVE) = proof_level, derived from quote-gate + ref-gate + surviving-objection count. Never asserted.
- Gate: `pushing/graph-extract-v1` (pinned in verify_site.py). New logic = new id.

## Decomposition rule (sanskritree)

Every claim resolves: claim → EVIDENCE → corpus record → translation (source_file + source_lines + immutable_id) → Sanskrit root bytes → R2. BLOCKED stops at Sanskrit (no English field embedded). Fail-closed falls out of structure.

## UNASKED matrix = work queue

`pt:asks:{template}:{work}` with no session = UNASKED = TASK (acceptance: session + gates PASS + receipt). 5 bodha templates × 44 works = 220 cells, 5 filled. Heat = open branches + comparative gaps.

## Files

- Extractor: `tools/extract_push_graph.py` (session .md → graph.jsonl, deterministic).
- Verifier: `tools/verify_push_graph.py` (refs resolve, hashes recompute, gate pinned; wired into verify.sh? No — standalone, run before commits touching pushing/).
- Data: `site/data/pushing-graph/graph.jsonl` (derived, never edited).
