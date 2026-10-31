# L200 — CROSS-LAYER AUDIT (frozen spec)
## How a published reading was derived — not a mini-C1

*2026-08-11. L200 is the audit layer. It answers one question precisely: **how was the published L2
reading derived from the source, where did interpretation enter, and what remains unresolved?** It is
NOT a readable summary and NOT a commentary. Commentary is C1; L200 is the ledger of derivation.*

**The layer hierarchy (keep clean):**
```
L2    what the reader reads            (the published prose)
L200  how that reading was produced    (the audit trail)   ← THIS LAYER
C1    what the passage philosophically means   (commentary/study)
```

L200 must never become a dumping-ground for smart observations. Those go to C1 (or to L200 §4 as
explicitly-numbered interpretive assertions, which then feed C1).

---

## The frozen schema (8 sections)

```
0. IDENTIFICATION          work / passage / source / T1 / L0 / L2 / argument-map
1. PUBLISHED READING       the actual L2 paragraphs (verbatim, referenced)
2. DERIVATION MAP          per L2 paragraph: → argument-map segment → L0 range → source range
3. MATERIAL TRANSLATION DECISIONS
     SUPPLIED                 content inserted into the translation (Sanskrit leaves it implicit)
     REFERENT_SUPPLY          an implicit "this/that/he/it" made explicit
     STRUCTURAL_CONNECTIVE    therefore/however/that is/in other words (exposes inference)
     LEXICAL                  a term-rendering decision (lemma → target word)
     GRAMMATICAL              a syntactic decision (case, compound, number, voice)
   (EXPLANATORY_RESTATEMENT does NOT live here — it is an interpretive assertion, §4)
4. INTERPRETIVE ASSERTIONS   what we think the argument means — IA-001, IA-002…
                             (separate from translation; these feed C1 and the essays)
5. SOURCE LAYER              Utpaladeva / Abhinava / objection / reply / quotation
6. CROSS-REFERENCES          typed relations (NOT a flat list)
     ROOT_TEXT_CONTEXT       Abhinava is literally commenting on this (IPK kārikā)
     SAME_ARGUMENT_CONTINUATION   the next/previous chunk of the same argument
     DOCTRINAL_PARALLEL      a conceptually-related passage (V2-D ↔ V3-D)
     COMPARATIVE_PARALLEL    a different text making the same move (TĀ, Spanda, Śivasūtra…)
     SECONDARY_SYNTHESIS     our essay/analysis of the passage (research-library)
7. OPEN / NEEDS_REVIEW       actual unresolved issues (from the chunk's fidelity note + migration)
8. REVIEW STATE              machine / editor / specialist  (+ migration provenance)
```

---

## The decision-type taxonomy (the strict part)

The single most important rule: **the audit is stricter than the prose.** Not every useful phrase is a
translation intervention.

| Type | Meaning | Example | Lives in |
|---|---|---|---|
| `SUPPLIED` | English inserted because Sanskrit leaves it implicit | "the seed precedes the sprout" (spelling out bījāṅkura) | §3 |
| `REFERENT_SUPPLY` | implicit "this/that/he/it" made explicit | "the **knower** who knows the order" for an unstated subject | §3 |
| `STRUCTURAL_CONNECTIVE` | "therefore/that is/in other words" added to expose inference | "that is, the awareness joins them" | §3 |
| `LEXICAL` | a term-rendering decision | vimarśa → "reflexive awareness" (with rivals) | §3 |
| `GRAMMATICAL` | a syntactic decision | compound parse, case, voice | §3 |
| `EXPLANATORY_RESTATEMENT` | editorial paraphrase of the argument — NOT translation | "the one manifests as the many without losing its unity" | §4 (IA) |
| `INTERPRETIVE ASSERTION` | what we think it means philosophically | "this is the functionalist criterion"; "this is the universality gap" | §4 (IA) |

**The rule:** if the phrase is *the translator's paraphrase of the meaning* (not an English word
inserted for a specific Sanskrit gap), it is an EXPLANATORY_RESTATEMENT → §4, not a translation
decision. The apparatus must never claim an explanatory summary is a translation intervention.

---

## The derivation map (the real cross-layer trail)

Each L2 paragraph gets a provenance footer — the actual trace:

```
SOURCE ANCHOR
M00022 2317–2384          (the raw Sanskrit source range)
L0 L61:T1204–L67:T1391    (the L0 record range)
Argument map V3-C.3–V3-C.5
```

A scholar clicking a sentence resolves: **L2 paragraph → argument-map segment → L0 range → source
range.** Token-level alignment is added only where a decision is disputed, an apparatus entry exists,
or the QA scaler flags it — not for ordinary prose.

---

## The migration metadata

Every migrated file carries its provenance:

```
migration:
  source_format: L200_LEGACY_V1
  migrated_by: l200_migrate.py
  migration_status: AUTO_MAPPED | PARTIAL | NEEDS_REVIEW
```

This prevents anyone later mistaking mechanically-classified content for hand-reviewed audit data.
**The originals are preserved in `l200_legacy/` — never overwritten.**

---

## Review states

- `machine` — generated (L200 draft or migration output), not yet reviewed.
- `editor` — a human editor has accepted the derivation map and decisions.
- `specialist` — a domain specialist has accepted the interpretive assertions.

---

## EXEMPLARS — what a complete L200 looks like in the IPVV

The **three canonical models** are the reference standard (full 8 sections, per-paragraph SOURCE
ANCHORS, MT/IA split, typed crossrefs):

| chunk | file | why it is the reference |
|---|---|---|
| **V2-O** | `l200/V2O-saptamo-vimarsa.md` | the one-support (k1) — the contrasting transcendental-argument model; the kārikā-quote voice |
| **V3-B** | `l200/V3B-kriya-dvitiyo-k1-7.md` | the fullest calibrated unit (the L1→L2 publication test) |
| **V3-C** | `l200/V3C-kriya-trtiyo-k1-2.md` | the dense pramāṇavimarśa argument (the blue-to-me, the one light) |

Each shows, concretely: the derivation map (L2 ¶ → argument-map segment → L0 range → source range),
the MT/IA decision tables with SUPPLIED-vs-IA discipline, the source anchors, the typed
cross-references, and the review state. These are the template for every future L200 and for the
editor's review of the 52 MIGRATED_PARTIAL files (see `l200/INDEX-AND-REVIEW-LEDGER.md`).

---

## VALIDATION — how we know an L200 is correct

**Per-chunk (Task-2 fidelity check — see `translations/tools/qa_v2_fidelity.py`):**
- [ ] the derivation map covers every L2 ¶ (L2 ¶ → argmap → L0 range → source range)
- [ ] every translation decision is classified (SUPPLIED / REFERENT_SUPPLY / STRUCTURAL_CONNECTIVE /
      LEXICAL / GRAMMATICAL) and is genuinely a translation intervention, NOT an
      EXPLANATORY_RESTATEMENT (those go in §4 IA)
- [ ] interpretive assertions (§4 IA) are separate from translation decisions (§3 MT)
- [ ] source-layer (§5) tags speaker: kārikā / Vṛtti / Vivṛti / Abhinava / pūrvapakṣa / siddhānta /
      quotation
- [ ] cross-references (§6) are typed (ROOT_TEXT_CONTEXT / SAME_ARGUMENT_CONTINUATION /
      DOCTRINAL_PARALLEL / COMPARATIVE_PARALLEL / SECONDARY_SYNTHESIS), not flat
- [ ] OPEN items (§7) carry a status and a derivation anchor
- [ ] review state (§8) is machine/editor/specialist + migration provenance

**Task-2 result on the 3 canonical chunks (2026-08-11): 18 PASS / 1 flag** — the canonical L200s
are source-licensed. The 1 flag (V3-C ¶8 UNRESOLVED_SOURCE_DEPENDENCY) marks a passage whose claims
need the recovered per-appearance sūtra content before it is trusted.

**Factory-wide:**
- [ ] no passage is surfaced as authoritative until its L200 passes Task-2 and its review state is
      ≥ editor

---

*This is the frozen L200 spec. It is a strict 8-section audit: how the reading was derived, where
interpretation entered, what remains unresolved. Commentary is C1; L200 is the ledger. The decision-type
taxonomy keeps translation decisions strictly separate from interpretive assertions. The originals stay
in `l200_legacy/`.*
