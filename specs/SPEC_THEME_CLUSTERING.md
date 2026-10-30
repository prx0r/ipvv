# SPEC — THEME CLUSTERING (the machine-discovery mechanism for THEMES)

*2026-08-12. The mechanism that proposes THEME groupings from C1s. It is the discovery primitive
for the THEMES layer (SPEC_THEME.md). Two foundational corrections are baked in from the start:*

---

## 0. The two foundational fixes (front and center)

1. **Themes overlap, they do not partition.** A C1 has a `primary_theme: Memory` PLUS `member_of:
   [Recognition, Continuity, Subjectivity]`. No forced single assignment. A passage genuinely lives
   in several thematic structures at once.
2. **Clustering is a proposal, not the deterministic floor.** The deterministic floor is *structural
   evidence*: C1 IDs, source passages, term links, RELATED relations, quotes, provenance — all must
   resolve. Semantic clustering / LLM naming = **proposal**; human adjudication = **acceptance**.
   Consistent with the global rule "**AI proposes ≠ Pāṭala asserts**."

```
C1s → hybrid relation-graph → candidate communities → ThemeProposal → LLM names →
      human merge/split/multi-assign → ACCEPTED THEME (overlapping)
```

---

## 1. Why hybrid (not just prose similarity)

Pure prose-similarity clustering misses the real structure of scholarship. The hybrid relation-graph
weights **seven** edge types, so discovery exploits the structured scholarship, not just how the C1s
sound:

| edge weight | what it captures |
|---|---|
| **semantic** | embedding similarity of the C1s (SUMMARY/FUNCTION/KEY TERMS) |
| **shared Sanskrit terms** | two C1s cite the same technical lemma (vimarśa, māyā, …) |
| **concept IDs** | both point at the same concept node (data/atlas/concepts.ts) |
| **RELATED relations** | the C1s' RELATED PASSAGES overlap (a structural link) |
| **argument sequence** | adjacency / continuation in the argument (vimarśa order) |
| **interlocutor** | both engage the same opponent (the Buddhist, the Vaiśeṣika…) |
| **doctrinal function** | both serve the same function (DEFINES / ESTABLISHES / QUALIFIES…) |

**Why it matters:** this can find *diachronic identity* from structural relations — a later C1 and an
earlier C1 that share terms/interlocutor/function even if their prose is not similar — not just
sound-alike passages.

---

## 2. Membership ≠ evidence

Cluster membership alone is NOT evidence. A proposed theme carries per-C1 membership with a strength
and a role:

```text
C1 V2-A   primary_theme: Memory      strength 0.95   role DEFINES
C1 V1-D   member_of: Memory          strength 0.68   role ESTABLISHES
C1 V3-O   member_of: Memory          strength 0.30   role CONTRASTS
```

Membership levels:
```text
CORE       the C1 is definitionally about this theme
SUPPORTING the C1 contributes to it
CONTRAST   the C1 explicitly opposes / qualifies it
TANGENTIAL the C1 touches it incidentally
```

Roles (what the C1 *does* for the theme):
```text
DEFINES · ESTABLISHES · DEVELOPS · APPLIES · QUALIFIES · CONTRASTS
```

---

## 3. ThemeProposal — the first-class object

Every proposed theme is a reviewable object, not a loose label:

```text
ThemeProposal {
  id
  working_label        (LLM-named, provisional)
  clustering_run       (which clustering config produced it)
  member_C1s           [{c1_id, strength, role}]
  edge_evidence        (which relations justified each membership — answerable:
                        "why is V2-O in Memory-and-Recognition?" → because shared term vimarśa +
                        RELATED V2-A + argument-sequence adjacency, strength 0.9)
  status: MACHINE_PROPOSED
}
```

Status lifecycle:
```text
MACHINE_PROPOSED → EDITOR_REVIEWED → ACCEPTED | REJECTED | SUPERSEDED
```

---

## 4. THEME BOUNDARY — the guard against synthesis inflation

Every accepted theme carries a boundary, so a reader knows its exact scope:

```text
included because:  the member C1s and their evidence (C1 ids, passages, terms)
not claiming:      the essay-level thesis, cross-tradition claims, modern application
```

This is the theme-level analogue of the C1's BOUNDARY/OPEN: it prevents a theme from inflating into
an essay.

---

## 5. Cross-work themes

Discovery runs **intra-work first, then cross-work** — one tooling:

```text
intra-work:  IPVV C1s → IPVV themes
cross-work:  IPVV + IPV + Tantrāloka + Spanda + Kubjikā C1s → cross-tradition themes
```

The hybrid graph generalizes: a shared concept ID or Sanskrit term links C1s across works with no
prose similarity. One mechanism, any corpus.

---

## 6. The decision rule

> **Discover computationally; adjudicate editorially.**

- The machine proposes candidate communities + evidence.
- The human merges, splits, multi-assigns, and names the accepted themes.
- **An expert adding a missed theme is a feature, not a failure** — the machine discovers the
  obvious and the structurally-linked; the human catches what the graph's weights under-weight.

---

## 7. Validation (how we know a proposed theme is sound)

- [ ] every `member_C1s` entry traces to a real C1 id that resolves
- [ ] every membership has a strength + role (not just "in the cluster")
- [ ] edge_evidence is recorded — "why is C1 in this theme?" is answerable
- [ ] no forced single-assignment: overlapping member_of is allowed and expected
- [ ] the status is honest (MACHINE_PROPOSED until an EDITOR_REVIEWED event promotes it)
- [ ] THEME BOUNDARY is present (included because / not claiming)
- [ ] structural evidence (C1 ids, passages, terms, RELATED, provenance) all resolve — this is the
      deterministic floor; clustering is proposal on top

---

## 8. Relationship to the rest

- **Upstream:** C1s (SPEC_C1) → this mechanism → THEME dossiers (SPEC_THEME) → ESSAYS.
- **The floor:** provenance-resolvable structural evidence. Clustering/LLM naming never overrides it.
- **Consistent with:** "AI proposes ≠ Pāṭala asserts" — every ThemeProposal is reviewable and every
  accepted theme is overlapping, evidence-backed, and boundary-scoped.
