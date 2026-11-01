# FOJIN REVIEW — what we can learn, and what's missing from each side

*2026-08-12. Review of [FoJin 佛津](https://github.com/xr843/fojin) — an AI Q&A platform over the
Buddhist canon (613 sources, 680K+ passages, trilingual cross-canon alignment) — against our
pāṭala / IPVV factory model. Goal: find the gold worth borrowing, and check we're not missing
anything.*

---

## 0. What FoJin is (one line)

**RAG over the aggregated Buddhist canon with deterministic anti-hallucination citation guards** —
every answer links back to a stable URN (`fojin:cbeta/T0001.1`), with a citation drawer, cross-canon
parallels, a knowledge graph, 32 dictionaries, and an MCP server so any AI can answer from the canon.

FoJin and pāṭala are **siblings**: same underlying ambition (grounded, verifiable, scholarly text
AI), different corpus (Buddhist canon vs. Śaiva Tantra) and different emphasis (FoJin = retrieval +
answer-guarding at scale; pāṭala = editorial provenance + deep passage tracking).

---

## 1. What FoJin does GOLD — worth borrowing into pāṭala

### 1.1 The citation guard (deterministic whitelist backstop) ⭐⭐⭐
The single most valuable idea. FoJin's `citation_guard.py` enforces that no answer cites a text
that wasn't in the retrieved context:

- Any `【《title》第N卷】` reference is checked against the **whitelist** (retrieved sources +
  aligned parallels).
- **Hallucinated title** → the clickable citation is stripped to plain prose (no false link).
- **Wrong fascicle** → rewritten to the closest real fascicle (no 404 click-through).
- Every mutation is **logged for drift monitoring** (a model-quality signal).

This is the deterministic backstop to our `UNANCHORED CLAIM → reject` rule (essay generation §5 of
the frozen product model). We designed the rule; FoJin has the working enforcement. **Adopt:** a
`citation-guard` stage over every generated essay/answer.

### 1.2 The quote verifier (open-world verbatim check) ⭐⭐⭐
`quote_verifier.py` catches the *other* hallucination class: a real citation with **invented quoted
text** before it. It:
- only verifies quotes immediately attached to a citation (within a char gap);
- requires a minimum quote length (below ~12 chars, paraphrase noise dominates);
- NFKC-folds + strips whitespace/punctuation, then substring-tests against the cited chunk;
- on a miss, **downgrades** the quote to prose (never *serves* a false verbatim quote — the old
  design only appended a caveat);
- buckets failures (near-miss vs. invented) and logs `QuoteMutation`s as a model-quality signal.

This is exactly the rigor our "SHOW EVIDENCE at claim level" needs — it verifies the *words*, not
just the *reference*. **Adopt:** `quote_verifier` over our L2 prose and essays.

### 1.3 The eval regression gate ⭐⭐⭐
`fojin-eval-regression.sh` + `backend/eval/` run a **daily answer-quality regression gate** (Recall@5,
faithfulness) against a baseline, alerting on regressions. This is the empirical discipline we've
been moving toward (our v0/v1/v2 toolchain) — FoJin has it running as a **CI/cron gate with
baselines**. **Adopt:** our QA toolchain becomes a gated regression harness, not one-off flags.

### 1.4 The MCP server as infrastructure ⭐⭐
`fojin-mcp` turns the corpus into callable infrastructure with URN-addressable read-only tools:
`search_corpus`, `read_passage`, `get_parallels`, `lookup_dictionary`, `lookup_entity`,
`resolve_urn`, `verify_quote`. We built our `resolve_ref` MCP tool in the previous step — FoJin
confirms this is the right shape and adds `verify_quote`.

### 1.5 Master-persona RAG ⭐⭐
15 historical Buddhist masters, each scoped to their tradition's scriptures. This is the "ask in
the voice of X" idea — directly analogous to our "read via concept / choose your depth" vision. A
persona is a **tradition-scoped projection** over the same corpus.

### 1.6 Cross-canon alignment flywheel ⭐⭐
kNN + anchor-expansion → candidates → human review → stored alignments (`alignment_flywheel.py`).
This is the comparison-pack machinery made systematic. Our comparison packs (L2 vs Ratié/Torella/
Pandey) are the same idea at editorial depth.

### 1.7 The knowledge graph + geo map ⭐
110K+ entities, 28K+ relations, 22K+ lineage chains, on a Deck.GL map. This is our concept/
related-works layer at a much larger scale.

---

## 2. What pāṭala has that FoJin LACKS (our gold)

### 2.1 Editorial provenance depth ⭐⭐⭐
FoJin's "verifiable" is **retrieval-verifiable** (the quote exists in the corpus). Pāṭala is
**editorially-verifiable** (the reading was *derived* — L2 → L200 decisions → L0 → Sanskrit, with
material-decisions recorded). FoJin does not have translation decisions, L200 philology, or a
source-layer. **This is our moat.** FoJin answers "is this text real?"; pāṭala answers "is this
reading justified?"

### 2.2 The version-selector / alternative readings ⭐⭐⭐
FoJin has parallel *canon-versions* (Chinese/Pali/Tibetan) but not *rival scholarly readings of the
same passage*. Our T2/R2/Pandey/Torella selector — multiple target-spans over one source — is
genuinely different and more philologically valuable.

### 2.3 Progressive disclosure / choose-your-depth ⭐⭐⭐
FoJin has master personas but not the ORIGINAL/READ/GUIDE/STUDY/CRITICAL **depth ladder** with the
truth-layer rule. This is our differentiator for accessibility.

### 2.4 The editorial loop + gold packs ⭐⭐
PCTS maturity profiles, GOLD PACKS, review ledgers. FoJin trusts retrieval + citation guards; we
trust review events + versioned passage records. Both are needed; they're different trust models.

---

## 3. The verdict — what we're missing (actionable gaps)

| gap | FoJin mechanism | pāṭala action |
|---|---|---|
| **1. Verbatim-quote verification** | `quote_verifier.py` (substring + downgrade) | add `verify_quote` over our L2 prose + essays |
| **2. Citation whitelist guard** | `citation_guard.py` (title/fascicle whitelist) | add `citation-guard` stage over generated answers |
| **3. Eval regression gate** | daily Recall@5/faithfulness gate + baseline | make our v0/v1/v2 a gated regression harness |
| **4. `verify_quote` MCP tool** | in `fojin-mcp` | add to our `resolve_ref` tool surface |
| **5. Alignment flywheel** | candidates → review → stored | systematize our comparison packs the same way |
| **6. Knowledge-graph scale** | 110K entities | grow our concept/related graph toward this |
| **7. Persona/depth RAG** | 15 masters | our GUIDE/persona layer (choose-your-depth) |

**What we should NOT copy:**
- The scale/ops (FoJin is a 6-service Docker stack for a public site; we're an editorial factory).
- Retrieval-as-trust alone (we need editorial provenance ON TOP of retrieval, not instead).

---

## 4. The synthesis — the combined model

The ideal pāṭala inherits FoJin's **verification enforcement** and keeps its own **editorial depth**:

```
                        ┌─ retrieval (FoJin's strength): find the passages, rank, rerank
  query/prompt ────────►├─ editorial (pāṭala's strength): resolve, show decisions, C1, depth
                        └─ guard (FoJin's): citation whitelist + verbatim-quote verify
                                          → any unanchored claim rejected / degraded
```

- **FoJin** proves the answer is *real* (in the canon). **pāṭala** proves the reading is
  *justified* (derived from the source through recorded decisions). Both, combined, are what a
  scholar trusts.
- FoJin's citation-guard + quote-verifier are the **enforcement** of our UNANCHORED→reject rule.
  We designed the rule; FoJin has it working at production scale. Borrow the mechanism.

---

## 5. Bottom line

FoJin is an excellent, mature sibling project. The gold to bring into pāṭala is **the deterministic
verification enforcement** (citation guard + quote verifier + eval gate) and the **MCP-URN pattern**.
Our gold that FoJin lacks is **editorial provenance** (decisions, source-layer, version-selector,
depth ladder). The two are complementary, not competing.

**Recommended next step for pāṭala:** build a `verify_quote` + `citation-guard` stage over the
resolve kernel we just shipped — so that when the self-writing essays and GUIDE renderings arrive,
they are bound by the same anti-hallucination enforcement FoJin proved at scale. This closes the
loop between "we designed the rule" and "the rule actually runs."
