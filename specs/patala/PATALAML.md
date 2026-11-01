# PĀṬALA ML — the research roadmap (GraphRAG / hypergraph / provenance / claim verification)

*2026-08-12. This is where Pāṭala becomes a genuinely interesting ML/research project rather than
"RAG + a graph." The unusual thing about our dataset is NOT its scale — it's that we have **multiple
explicitly derived epistemic layers over the same ancient source**: source → translation → decision →
commentary → theme → claim → essay → pedagogical rendering. That gives us supervision most corpora
do not have. **That is the ML gold.***

> Every idea below is grounded in the current literature (GraphRAG, HyperGraphRAG, RAPTOR, ColBERTv2,
> graph foundation models, VeriTrail, Claimify, entailment lattices, hyperbolic embeddings). The
> target architecture and the 5 highest-upside experiments are at the end.

---

## 1. Move from a graph to a **typed hypergraph**

Our data is naturally higher-order. A translation decision is not really a binary edge between
"Sanskrit span" and "English span." It connects:

```text
source span
+ reading
+ alternative
+ evidence
+ scholar
+ term sense
+ review
```

That is an **n-ary relation**, which hypergraphs represent directly. HyperGraphRAG argues exactly
that ordinary graphs lose information when real facts involve more than two entities, and reports
gains over ordinary GraphRAG in multi-hop retrieval. Model hyperedges like:

```text
TRANSLATION_DECISION {
  SanskritSpan, EnglishSpan, TermSense, EvidenceSet, AlternativeReading, Reviewer
}

ARGUMENT {
  PremiseA, PremiseB, Conclusion, Passage, Speaker
}

THEME_MEMBERSHIP {
  C1, Theme, Role, Strength, Evidence
}
```

This fits our scholarly ontology better than forcing everything into pairwise triples.

## 2. Build **multi-resolution retrieval**, not one retriever

RAPTOR showed the usefulness of recursively clustering and summarizing a corpus into multiple
abstraction levels; GraphRAG targets both local and global questions through graph/community
structure. We already have perfect natural resolutions:

```text
TOKEN / SOURCE SPAN
↓
PASSAGE
↓
C1
↓
THEME
↓
WORK
↓
CROSS-WORK THEME
↓
TRADITION
```

Retrieval should be query-adaptive:
- "Where does Abhinava use *vimarśa* here?" → spans/passages.
- "What is the argument of this chapter?" → C1/theme.
- "How does recognition develop across IPVV?" → theme graph.
- "How does Trika differ from Spanda?" → cross-work graph.

That is much more powerful than top-k vector search.

## 3. Use **late-interaction retrieval** for Sanskrit and technical concepts

Single-vector embeddings are likely too lossy. ColBERT-style late interaction keeps token-level
representations and scores query↔document token interactions rather than compressing the whole
passage into one vector. ColBERTv2 retained this fine-grained power while reducing storage cost.
Attractive because `pratyavamarśa`, `vimarśa`, `svasaṃvedana`, `ābhāsa` may occur in semantically
close passages where the exact lexical distinction matters enormously.

Eventually benchmark: BM25 · dense embedding · ColBERT/late-interaction · graph retrieval · hybrid —
against a hand-built scholarly retrieval set.

## 4. Turn THEMES into a **graph representation learning problem**

The hybrid graph can go beyond manually weighted edges. Eventually learn a C1 representation from:
text semantics + Sanskrit terms + passage sequence + explicit links + argument roles + shared source
relations + interlocutors. Then compare: hand-weighted graph · GNN embeddings · hypergraph
embeddings · text embeddings. Graph foundation models aim to generalize structural reasoning across
graphs; recent work emphasizes relation-centric and richer motif-based reasoning.

**Longer-term research question:**

> Can a model trained on structural patterns in IPVV discover analogous argumentative structures in
> another Sanskrit work without knowing its vocabulary?

## 5. Learn **relation motifs**, not merely topics

Consider recurring structures:

```text
OBJECTION → distinction → counterexample → reductio → conclusion
```
```text
root kārikā → Vṛtti claim → Vivṛti expansion → Abhinava qualification
```

Recent KG-foundation-model work suggests richer multi-relation motifs improve reasoning over pairwise
relation interactions. Pāṭala could discover **argument motifs** across texts:

```text
MEMORY ARGUMENT:      V2-A, V2-O, ...
REFLEXIVITY ARGUMENT: IPVV ..., Buddhist source ..., Nyāya source ...
```

This is deeper than thematic clustering — it asks:

> "Do these passages perform the same intellectual operation?"

## 6. Build a **scholarly derivation DAG** and run VeriTrail-style backwards verification

Microsoft's VeriTrail treats multi-stage generation as a DAG and verifies final claims backwards
through intermediate nodes toward source material, identifying provenance and where unsupported
material entered. Our DAG:

```text
SANSKRIT → L0 → L2 → C1 → THEME → ESSAY → GUIDE → AUDIO/VIDEO
```

For any generated sentence, trace: essay claim ← theme claim ← C1 claim ← L2 ← source span. If the
support breaks at Theme→C1, we know **where semantic inflation occurred**. That is vastly more
interesting than merely saying "hallucinated."

## 7. Use **atomic claim extraction** everywhere

Claimify decomposes outputs into self-contained, verifiable claims before checking them. Make claims
first-class nodes:

```text
CLAIM-729
  text:   "The I-awareness is not produced by vikalpa."
  type:   INTERPRETIVE
  scope:  IPVV V2-L
  supports: C1-V2-L, L200-V2-L
  status: SUPPORTED
```

Then a paragraph is just a composition of claims. This unlocks claim-level citations, contradiction
search, theme synthesis, essay auditing, and media provenance.

## 8. Build **counterevidence retrieval**, not merely evidence retrieval

One of our strongest potential research contributions. Given a claim, retrieve three sets —
SUPPORT / QUALIFY / CONTRADICT — not just top-k similar passages. Combine semantic retrieval, graph
neighborhood, antonym/negation features, relation roles, NLI-style contradiction scoring.

A scholarly AI should ask:

> **"What is the strongest passage in the corpus that would make this answer less true?"**

## 9. Add an **entailment lattice**

Don't reduce support to true/false. For each derived claim:

```text
ENTAILED · SUPPORTED · PLAUSIBLE_SYNTHESIS · QUALIFIED · TENSION · CONTRADICTED · UNSUPPORTED
```

Claim-verification work combines NLI and knowledge-graph consistency signals to distinguish
unsupported from contradictory claims rather than treating grounding as binary. Perfect for
Themes/Essays.

## 10. Build **minimal evidence sets**

Frontier-level and very valuable. Instead of attaching ten passages to a claim, ask: what is the
*minimum sufficient evidence subgraph* supporting it? For "Abhinavagupta treats memory as dependent
on the recognizer," the system might find V2-A + V2-O are sufficient while five other passages are
redundant. Your SHOW EVIDENCE button can expose the **smallest load-bearing argument**, not a wall
of citations.

## 11. Build **semantic conservation tests** (Vertical Fidelity)

Represent a claim as features: polarity · agent · patient · scope · modality · certainty · causal
direction · temporal relation · speaker. Then test layer-to-layer conservation:

```text
C1:    "This passage does not alone establish universal identity."
GUIDE: "Abhinavagupta proves all consciousness is one."
FAIL:  scope strengthened · certainty strengthened · boundary lost
```

Call it **Vertical Fidelity** — potentially a publishable methodology paper.

## 12. Learn where **misconceptions arise as transformations**

Model the distortion explicitly:

```text
Śiva (source usage) → scholarly translation "Śiva" → ordinary English ontology "a god"
→ reader interpretation: external divine person
```

Then train/measure transformations (technical term → translation → beginner interpretation) and
identify **semantic failure points**. A near-new field: **computational hermeneutics of
misunderstanding**. For `śūnyatā`, `Śiva`, `māyā`, `cakra`, `vimarśa`, the question is: at which
explanatory layer does the concept drift away from its textual function?

## 13. Use **hyperbolic embeddings** for hierarchical intellectual structures

Texts and traditions are deeply hierarchical:

```text
Śaivism → Trika → Pratyabhijñā → recognition → {memory, reflexivity, identity}
```

Euclidean embeddings handle hierarchies awkwardly; hyperbolic representations naturally encode
tree-like growth. Test ordinary vs. hyperbolic concept space for tradition maps, concept
hierarchies, and broad→narrow retrieval.

## 14. Build a **cross-tradition alignment model**

Predict relation type: DIRECT_INFLUENCE · SHARED_TERMINOLOGY · STRUCTURAL_ANALOGY ·
POLEMICAL_RESPONSE · CONTRAST · MODERN_COMPARISON · NO_RELATION. Input: two passage
representations + chronology + vocabulary + known citations + relation graph. Output: candidate
relation + evidence + uncertainty; human accepts/rejects. The system can **discover candidate
intertextual relations** for scholars.

## 15. Make themes temporally/structurally dynamic

Instead of a static theme list, model trajectories:

```text
Theme: recognition — early IPVV (introduced as X) → middle (linked with memory) → later (tied to
agency) → later (universalized)
```

Compute concept trajectories through one work, one author, one tradition, centuries. GraphRAG's
community-style summarization points toward multilevel understanding; our corpus gives it a sharper
historical use-case.

## 16. Represent arguments as executable graph objects

```text
ArgumentNode {
  premises: [A, B]
  inference: REDUCTIO
  conclusion: C
  objections: [...]
  dependencies: [...]
}
```

Then query: "show every reductio in IPVV"; "what breaks if premise P is rejected?"; "which
arguments depend on universal subjecthood?" The text becomes a **computable argument graph** — an AI
tutor can walk the reasoning rather than summarize prose.

## 17. Run **counterfactual graph analysis**

Remove a proposition; observe what downstream doctrine fails. Example: REMOVE "I-awareness is
non-constructed" → AFFECTS recognition, continuity, universal-subject arguments. This is **doctrinal
sensitivity analysis**: calculate centrality, dependency depth, betweenness, fragility — reveal
structurally central claims scholars might overlook.

## 18. Build an **epistemic PageRank**

Weight nodes by evidence role: primary source (high) · explicit definition (high) · direct
commentary (high) · scholarly inference (medium) · cross-tradition analogy (low). Then rank "the 10
most evidentially central passages for vimarśa" — a genuinely useful "start here" ordering for
concept pages, rather than "which passages mention the word most often."

## 19. Use community reports — but make them scholarly

GraphRAG creates community summaries over graph communities for global reasoning. Our Theme
dossiers are a better domain-specific version. Go one step further:

```text
COMMUNITY REPORT — theme · core passages · definitions · argument moves · tensions · open cruxes ·
translation disagreement · scholarship disagreement
```

Global queries retrieve these before diving into raw passages — "what is the IPVV really doing?"
becomes tractable without throwing 500 passages into context.

## 20. Eventually build a **Pāṭala benchmark**

Expert-reviewed tasks:

```text
PASSAGE RETRIEVAL      find the correct passage
THEME DISCOVERY        recover a known relationship
ARGUMENT LINKING       identify premise/conclusion
TERM SENSE             choose the contextual sense
TRANSLATION DIVERGENCE locate the crux
CLAIM SUPPORT          find supporting evidence
COUNTEREVIDENCE        find the strongest qualifying passage
DEPTH FIDELITY         detect semantic strengthening
CROSS-WORK RELATION    classify the relation type
```

Then Pāṭala becomes a dataset for **ML on philology and intellectual history** (cf. BenchmarkQED).

---

## The target architecture

```text
                    PĀṬALA KNOWLEDGE CORE
                            │
              ┌─────────────┴──────────────┐
              │                            │
        Typed hypergraph             Vector spaces
              │                     dense / late interaction
              │                            │
      argument / provenance        semantic neighborhoods
      terms / evidence             hyperbolic hierarchy
              └────────────┬───────────────┘
                           │
                    HYBRID RETRIEVAL
                           │
            ┌──────────────┼─────────────┐
            │              │             │
          local          global       adversarial
        passage          theme       counterevidence
            │              │             │
            └──────────────┼─────────────┘
                           │
                    CLAIM COMPILER
                           │
                    provenance DAG
                           │
                vertical-fidelity checks
                           │
      ┌────────────┬────────────┬───────────────┐
      │            │            │               │
     C1          themes        essays          guide
      │                                         │
      └───────────────── media / tutor ─────────┘
```

---

## The five ML experiments with the highest upside

1. **Hybrid C1 graph vs embeddings-only theme discovery** (tests the hybrid graph §4 + §5).
2. **Hypergraph representation of translation/argument decisions** (§1).
3. **Counterevidence retrieval for interpretive claims** (§8).
4. **Vertical-fidelity classifier across C1 → Theme → Guide** (§11).
5. **Argument-graph dependency analysis across IPVV** (§16–17).

Those five could plausibly produce both product improvements and genuinely interesting research
outputs.

---

## The meta-level insight

The unusual thing about Pāṭala is not scale — there are much larger corpora. It's the **multiple
explicitly derived epistemic layers over the same ancient source**:

```text
source · translation · decision · commentary · theme · claim · essay · pedagogical rendering
```

That layered supervision is the ML gold — most corpora do not have it. It is what makes every one
of the above experiments not only possible but grounded.
