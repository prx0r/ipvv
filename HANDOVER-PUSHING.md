# HANDOVER — continue the pushing work

*2026-10-31. Read this before pushing anything. Companion: process/PUSHING-QUESTION-CRAFT.md
(how to ask), logs/AUDIT-2026-10-31.md (what exists), specs/use-cases/PLAN-v2.md (the arc).*

## Where pushing stands (per work)

| Work | Pushing state | What's next |
|---|---|---|
| **IPVV** | 12 probes (10 thematic + 2 Bhairavastava sessions). Strongest corpus. | Deeper ROUND 2-3 on the 10 thematic probes (currently single-round). |
| **Bhairavastava** | DONE — full 10-question probe (4732w, claim statuses, ROUND 2 on Q1/Q3/Q5/Q7) + logicvid voice session (3 penetrations + honest limit). The reference. | Done. Use as template. |
| **Tantraloka** | 63 probes (Q1-Q28 extracts + LOGICVID sessions with multi-round penetrations). Gold standard for depth. | New sessions in user's voice (see craft doc). |
| **43 other works** | ZERO pushing coverage. | Pick one, immerse, push. |

## The method (read before starting)

1. **Read process/PUSHING-QUESTION-CRAFT.md first.** It's the recipe for good questions.
   Formal/seminar phrasing dies. Conversational + one-question + prior-session-derived lives.
2. **Read the 3 formats** (all in site/data/pushing/):
   - `tantraloka/PUSHING-TANTRALOKA.md` — question → stored passage → text's reasoning chain → verdict
   - `ipvv/PUSHING-IPVV.md` — sessions table with GEM/CORRECTION/RESOLVED verdicts
   - `research/truthagent.md` — claim statuses (stated → established → unstated premise → rival → unresolved)
3. **Use ALL THREE.** The best session has: stored passages (exact Sanskrit + line refs),
   text-first reasoning (ROUND 0 quotes before asking), multi-round penetrations
   (ROUND 1 → 2 → 3), claim statuses, and an honest limit.

## What makes a good pushing session (quality bar)

- **ROUND 0:** the text's own words, quoted, not paraphrased. Material BEFORE question.
- **One question per session.** Not a list of tensions.
- **The question is in YOUR voice.** "then what the hell do I do?" not "what is the
  devotee's soteriological role?"
- **Each penetration surprises you.** If you already know the answer before ROUND 1,
  you're not pushing — you're confirming.
- **Honest limit at the end.** "The text doesn't address this" is a valid, valuable
  verdict.
- **Verdict in the sessions table.** GEM / CORRECTION / RESOLVED / PARTIAL / STATED.

## Where the sessions live

- `site/data/pushing/ipvv/` — IPVV + Bhairavastava sessions
- `site/data/pushing/tantraloka/` — Tantrāloka sessions (63)
- `site/data/pushing/research/` — truth/agency dossiers (19)
- `site/data/pushing/rasa/` — rasa quote-audit (2)
- Pushing hub: `/ipvv/pushing.html` (auto-indexes all files)
- Method specs: `specs/pushing/` (5 files: PUSHING_GUIDE, agent spec, questionnaires)

## Suggested next pushing targets (pick one)

1. **IPVV thematic probes deepening** — the 10 existing probes are single-round.
   Add ROUND 2-3 penetrations the way Bhairavastava got them. Highest value: these
   are the crown's arguments.
2. **Kramastotra** (30 chunks, 11 PASS) — has T1-full + L0 done. Immersion-ready.
3. **Tantrasara** (51 chunks, 7 PASS) — large, argument-dense. Needs immersion first.
4. **Stavacintamani** (12 chunks) — devotional like Bhairavastava, same genre skills apply.

## Rules (from AGENTS.md + audit)

- Never edit frozen T1 (Law #1).
- BLOCKED chunks get no English in any field, any style, any context.
- Pushing reveals; it never asserts. MACHINE_PROPOSED until a human promotes it.
- Every claim status must be honest: STATED only when the text says it; ESTABLISHED
  only when the argument validly derives it; "requires unstated premise" when it
  doesn't; "rival unresolved" when there's a live alternative.
- The user asks the questions. Read their logicvid voice before writing yours.

## Done 2026-10-31 — bodhapancadasika (user's questions)

5-session arc (forget → terror → grace → necessity → dissolution), all PASS-English + Sanskrit, chain shapes labeled, scaffold + table. Comparison doc + transferable arc + 6 chain shapes saved. Graph extractor/verifier/gate live (322 records, 71 sessions). Worker upgraded (Qwen primary, template match, diverse pick, 2 bugs fixed) and tested live on both IPVV + bodha questions — chain context + OWNER labels + grounded follow-ups all working.
Next: IPVV thematic ROUND 2-3 (shapes #2 + #3), comparative sessions (B13/B14/B15), stavacintamani or spanda when gates pass.
