---
name: translate-work
description: "Run a tantric work through the full audited translation stack (bibliography → source → T1 → R1 → T2 → R2 → T3 → T3.1) as a state machine with validation and review passes. Produces the per-work stacked artifact. Use when asked to translate a work, advance a work's pipeline, or produce a C1-capable audited stack."
version: 2.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [translation, sanskrit, tantra, pipeline, patala, audited, state-machine]
    related_skills: [validate-passage, assemble-stack, use-api]
    checkpoint: CP1 (the audited work stack, the source floor)
---

> **⚠️ NAMING NOTE (2026-08-13):** this skill's stage name "T1" is the **LEGACY** meaning — a "best
> constructive reading" (close English translation). In the **canonical layer stack**
> (`handover/agent-2-integration/CANONICAL-LAYER-STACK.md`) the canonical **T1 = the transliteral
> word-gloss** (`[and]-GLOSS (IAST)`), and this skill's "close translation" maps to the canonical **L2**
> (readable) layer. This skill is the retired/earlier pipeline; the canonical stack is authoritative.
> Do not use this skill's "T1" as the canonical T1.

# Translate a Work (the audited stack)

## The core unit

The **audited work stack** is the fundamental unit of Pāṭala — not a PDF, not a
translation, not a bibliography record. Every floor reinforces the others, and the
whole thing is the auditable provenance chain.

```
WORK
├── bibliography (identity, sources, coverage, rights, verification)
├── source (edition / witness / source span)
├── translation stack
│     T1 → R1 → T2 → R2 → T3 → T3.1
├── commentary (C1 — a separate workflow, the capstone)
├── AUDIT.md (validation, derived from actual checks — never hard-coded PASS)
└── structured claims feed back into the corpus (terms, parallels, assertions)
```

## The flow (a state machine, not a rigid loop)

Advance the work by its CURRENT STATE. Inspect what floors exist; run ONLY the next
missing floor. Do not re-run completed floors.

```
bibliography (translation-ready contract)
   → source identity
   → T1  best constructive reading
   → R1  crux discovery / prosecution (crux_id, type, assumption, rivals, evidence-needed)
   → T2  strongest defensible rival (sees T1+R1; difference budget; CONSTRAINED markers)
   → R2  decision-level adjudication (CONSTRAINED / PREFERRED / OPEN / RECONSTRUCTED)
   → T3  current resolved translation
   → T3.1 reader rendering
   → [C1 — separate workflow]
   → AUDIT (derived from checks)
   → structured claims feed back into corpus
```

## Reference implementation

The pipeline modules (`pipeline/`) are the toolkit the agent calls. The state
machine (`pipeline/state_machine.py`) implements the inspect → advance → audit →
write loop. The agent may use it or drive the floors directly.

- `pipeline/schema.py` — the record structure, stage constructors, versioning.
- `pipeline/prompts.py` — the house prompts per stage.
- `pipeline/audit.py` — structural validation (schema, ordering, [X] honesty).
- `pipeline/state_machine.py` — `next_missing()`, `run_floor()`, `advance_work()`.
- `pipeline/stack.py` — assembles `translations/_stack/{work}/` + writes `AUDIT.md`.

## The three independent dimensions (never conflate)

```
pipeline_stage     where in the flow (T1 → ... → C1)   — set by each stage
origin             who produced it (machine / human)   — machine stages write machine
editorial_status   proposed / reviewed / accepted      — set ONLY by a real ReviewEvent
```

So `pipeline_stage = R2, origin = machine, editorial_status = proposed` is honest.
Machine stages NEVER promote editorial_status. Only `set_review` does.

## Stage rules

### T1 — best constructive reading
Close translation, IAST, technical terms retained (śakti, kula, krama, spanda,
vimarśa, prakāśa, visarga, khecarī, āveśa, uccāra, śūnya, mātṛkā, saṃvit, parāmarśa,
svātantrya, tattva). Notes with [G]/[P]/[C]/[S]/[A]/[R]. `[X]` flags. Time-place-context.

### R1 — crux discovery (NOT peer review — it's a machine adversarial pass)
Map the genuine cruxes: id, type (LEXICAL/GRAMMATICAL/TEXTUAL/REFERENTIAL/DOCTRINAL/
CONTEXTUAL), the T1 assumption, the alternative candidates, the evidence needed.
Verdicts (RIGHT/ERROR/FORK/OPEN) + commentary stubs. Challenge genuinely; don't
manufacture doubts on secure verses.

### T2 — strongest defensible rival
SEES T1 + R1. Differ ONLY where it changes syntax, referent, technical sense,
doctrinal implication, textual reading, or meaningful interpretation (the difference
budget). Do NOT introduce differences for style. Address R1's cruxes. Mark
source-constrained readings CONSTRAINED.

### R2 — decision-level adjudication
Adjudicate BY DECISION, not just sentence. Hard-core = agreement + source-constrained.
Classify each decision: CONSTRAINED / PREFERRED / OPEN / RECONSTRUCTED. Reasoning,
school/period-context research, EXPAND the commentary, equal alternates, open questions.

### T3 — current resolved translation
The resolved reading under this review state. Not "truth forever" — T3 v2 is possible.

### T3.1 — reader rendering
Natural English derived from T3, in lock-step. Flowing, defensible, no meaning change.

### C1 — separate workflow (the capstone)
Reviews the whole stack, does its own research, produces a full commentary that is
itself a referenceable document. May CHALLENGE T3 (→ RevisionProposal → T3 v2) but
never mutates it. Should emit STRUCTURED proposals (TermHistoryAssertion,
ParallelAssertion, DoctrinalAssertion, TextRelation, BibliographicClaim,
TranslationChallenge, CommentaryClaim, ResearchQuestion) that feed back into the corpus.

## Validation (run the audit after each floor)

```bash
python3 pipeline/audit.py            # structural audit (via the module)
python3 pipeline/validate.py --report
python3 pipeline/validate_trajectories.py
```

Every PASS in `AUDIT.md` must be DERIVED from an actual check — never hard-coded.
Anything not computed is `NOT_CHECKED`.

## Invariants (never break)

1. Stable IDs never depend on mutable wording.
2. Work ≠ witness ≠ digital representation ≠ canonical passage.
3. Annotations are independent from the base text and independently addressable.
4. Machine output always enters as a proposal, never authority.
5. Every meaningful scholarly judgment can carry evidence and review history.
6. Translation prose and interpretive decisions have independent version histories.
7. Convenient API bundles are projections over normalized scholarly data, not the
   canonical data model.

## The vertical-slice discipline (build one work fully, then scale)

Do NOT deepen all bibliography records first. Take ONE work (e.g. Kramasadbhāva,
Śivasūtra, Kubjikāmata) through the FULL stack to a real C1, then ask: *what did C1
need that wasn't in the BibliographyRecord?* That drives the schema. Only after one
or two works are C1-complete does scaling the bibliography become justified.
