# Existing frameworks for argumentation and IR

Recent research has produced mature tools covering most of the Pāṭala pipeline.  For structured reasoning, **py-aspic** is a Python library implementing the ASPIC+ framework (strict/defeasible rules, preferences, contraries).  For interchange, **xAIF** provides JSON-based import/export of argument components and relations.  For argument mining, the **Open Argument Mining Framework (oAMF)** offers modular, xAIF-compatible pipelines and GUI interfaces.  For abstract semantics, **ALIAS** implements Dung’s AF with Python APIs for computing extensions.  These projects align directly with the 12 IR objects.  For example, an `InferenceApplication` in Pāṭala can be converted to a py-aspic rule (e.g. using `Rule.from_string`), or to an xAIF JSON rule node.  The epistemic regime and evaluation logic can be handled by invoking ASPIC+ and ALIAS: Pāṭala’s `Argument` graphs can be fed into py-aspic (for structured reasoning) and ALIAS (for abstract acceptability) rather than reimplementing them.

Recent papers also describe exactly this split.  Freedman *et al.* (AAAI’25) propose **Argumentative LLMs (ArgLLMs)**: LLMs construct explicit argumentation frameworks and then formal reasoning yields contestable outputs.  In other words, they “augment LLMs with argumentative reasoning” so that “arguments frameworks … then serve as the basis for formal reasoning” and outputs can be “explained and contested”.  This mirrors Pāṭala’s principle that **“AI proposes ≠ Pāṭala asserts”** – the LLM may suggest structure but only the formal layer carries weight.  Bhattacharjee & Anand (2025) similarly present an **Argument Knowledge Graph (AKG)** pipeline: text → annotated components → KB graph → inferred arguments via modus ponens → final graph with explicit undercuts and attacks.  They show how adding metadata (inference-rule premises, attack types, etc.) reveals hidden inferences, exactly as Pāṭala plans.  In fact, their AKG construction enriches argument nodes with attributes and finds undercut attacks that simple mining misses. 

Epistemic perspective is also emerging in argumentation literature.  For instance, **Epistemic Argumentation Frameworks** (EAF) explicitly model a reasoner’s beliefs and preferences when evaluating an AF.  Sakama & Son (2020) show how different agents can have different labellings on the same argument graph based on their constraints.  This supports Pāṭala’s idea of “evaluation under multiple regimes”: e.g. an argument can be accepted in a Śaiva regime but not in a Buddhist one, and the system should represent both.  No extant tool captures this out of the box, but the formal concept is known and can be layered on top of an argumentation solver.  

# Mapping tools to the 12-object IR

Our **12 IR objects** now match well with external systems:

- **`Proposition` / `Commitment`**: Represented in text and annotation.  Commitments (asserts/denies/quotes) have no off-the-shelf engine, but they flow through the pipeline.  
- **`ArgumentScheme` / `InferenceRule`**: Py-aspic handles rules and can be driven by a library of scheme templates or formulas.  
- **`InferenceApplication`**: Encoded as py-aspic rules + facts. For example, Pāṭala would generate a rule like `"d,e=>f"` and call `pyaspic.Rule.from_string(...)`.  
- **`Argument`**: A collection of inference steps. Feed each assembled `Argument` as an ASPIC+ theory into py-aspic to compute defeat relations.  
- **`Attack`**: Mapped to py-aspic’s contraries and attack generation, or to AIF edges (undermine/rebut).  
- **`Preference`**: Py-aspic supports rule-preference orders.  
- **`DebateFrame` / `ResearchQuestion` / `Position`**: High-level metadata linking arguments. Lacking direct library support, they organize which arguments to compare.  
- **`SemanticAlignment`**: Outside existing APIs; would annotate concept-level matches between arguments before running formal checks.  
- **`EpistemicRegime`**: Also outside core engines. We can simulate this by configuring different py-aspic knowledge bases or constraint sets (akin to multi-agent labellings).  
- **`Crux`**: Not provided by any library; it’s a novel analysis on top of the argument graph (see below).

As references, we note: py-aspic is explicitly for **“creating and evaluating ASPIC+ theories”**.  xAIF enables rich JSON interchange (so Pāṭala can export/import IR objects).  oAMF natively uses xAIF and even offers drag-and-drop pipeline construction.  ALIAS handles pure abstract arguments with attacks, so it can cross-check acceptability after flattening our IR graph to an AF.  Lean or Z3 can optionally verify any parts that reduce to first-order logic or arithmetic. 

# Annotating IPVV “gold” arguments

A critical next step is **encoding several exemplar IPVV disputes by hand**, to ground-test our IR.  We should select cases illustrating different schemes: a transcendental argument, a reductio, a conceptual distinction example, and a clear objection/reply dialogue.  For each, we extract the *propositions* (in natural language and formal form), label what Abhinavagupta *asserts* vs. reports or grants to an opponent, mark speaker `Commitments`, identify the `DebateFrame` (question, level, scope), and specify any `InferenceRules` used.  For example, a crude sketch:

- **Example 1 (Transcendental):** Proposition P: “If cognition were only successive, consciousness would be exhausted by time.” Inference W: “But we experience non-exhaustion.” Conclusion C: “Therefore there must be a non-successional aspect.” We’d encode P, W, C as Propositions, mark W as a transcendental warrant.  
- **Example 2 (Reply vs. opponent’s claim):** Abhinavagupta asserts “No permanent self can be known by cognition” (P), while quoting a Buddhist (Q: “Memory implies a permanent knower”). We mark Abhinavagupta’s commitment (denying Q, attributing Q as opponent), identify their semantic frame (“What is required for memory?”), etc.

Each case yields a small IR graph.  By comparing our IR to the gold editorial understanding, we verify all needed distinctions are captured.  Bhattacharjee & Anand’s example pipeline provides a model: annotate premises and infer hidden rules, then build argument graph with undercuts. We would do similarly, but preserving provenance (link back to Sanskrit). This manual “phase 0” alignment ensures our schema is truly fit-for-purpose. 

# Prototyping adapters and evaluation

Once the IR for each gold case is in place, we build **adapter code** to run existing engines over it.  For example:

- **xAIF Exporter**: A function `export_xaif(IR)` writes out JSON nodes/edges in xAIF format. The IR’s arguments become AIF `RA` and `CA` nodes, propositions become `I` nodes, etc. This can then be loaded into oAMF or other tools.  
- **ASPIC Adapter**: Compile each `InferenceRule` and `InferenceApplication` into a py-aspic `Rule` and add premises to a `KnowledgeBase`. For instance, IR’s rule “[r1]: d,e=>f” becomes `Rule.from_string("[r1]", "d,e=>f")`, and premises “d,e” go into the KB.  Contraries and preferences are added via py-aspic APIs.  Then we run py-aspic’s `Theory` to check for acceptable arguments.  
- **ALIAS Adapter**: From the same IR, construct a Dung AF: each IR argument (set of premises -> conclusion) is an abstract argument, attacks as edges. Write this to ALIAS and compute extensions to see which propositions survive under different semantics. This serves as a consistency check against the structured result.  
- **Lean/Z3 Adapter** (optional): For any inference schema that can be formalized (e.g. modality logic for “must” vs “possible”), translate selected Premises+Warrant into a logical formula and ask a solver if Conclusion follows. This verifies “inference validity,” though we remember validity ≠ truth (Smith’s logic principle).  

Running these adapters on the gold cases lets us compare: do these formal engines accept the intended conclusions? Where discrepancies occur, we examine whether the fault is in our IR capture or in the choice of semantics.  This exposes any missing IR nuance (e.g. did we forget to mark a premise as an “assumption” vs. established fact?) and validates the deterministic pieces of the pipeline.

# Crux extraction & counterfactuals

Finally, we must operationalize the **crux analysis**.  Informally, a **crux** is a minimal assumption or inference whose change flips the debate outcome.  Algorithmically: 

- Given two opposing argument subgraphs for conclusion Q, identify all disputed elements (propositions, warrants, alignments) that feed into Q.  For each candidate element X, simulate “counterfactually” removing or inverting X (e.g. reject an assumption, weaken a warrant) and re-evaluate the graph.  
- Track which conclusions change status. A set K of elements is a candidate crux if toggling all of K changes whether Q is accepted. Then minimize K (remove extraneous parts) to get a minimal crux set.  

This is related to *counterfactual argumentation* in formal models. For example, Sakama *et al.* (COMMA 2014) show how to ask “what if an accepted argument were rejected?” in an abstract AF. Pāṭala will do the analogous thing with our IR: “what if Proposition P were false?” or “what if term sense S2 applied instead of S1?” That will generate the candidate K sets. 

We can prototype this by brute force on our gold cases: systematically disable each premise or rule and note the impact on the target conclusion, using py-aspic or ALIAS to recompute.  Then use a minimal hitting-set algorithm (or simply try all combinations if the set is small) to isolate minimal K’s.  These K’s become CRUX records, e.g. *“CRUX-1: is “numerical identity of the self” required for recognition? (Depends on whether Abhinavagupta’s warrant or the Buddhist assumption holds.)”* 

The output of a Pāṭala query should then highlight these cruxes. For example, if Abhinavagupta and Dharmakīrti disagree on Q: “Memory requires a permanent knower,” Pāṭala might report **“UNDERDETERMINED: The dispute hinges on W7 (numerical identity vs. causal continuity for recognition). If W7 holds, Abhinavagupta’s conclusion stands; if not, the Buddhist position stands. No winner is forced.”** This is the scientific output we aim for, not a numeric “strength” score. 

# Roadmap integration

In summary, our research plan is:

- **Survey & tools:** Leverage py-aspic, xAIF, oAMF, ALIAS and learn from ArgLLMs and AKG papers. 
- **Gold encoding (Phase 0):** Manually annotate 5–10 representative IPVV arguments into the IR, covering diverse inference types. Use that to finalize the 12-object schema.  
- **Adapters (Phase 1):** Implement converters to run py-aspic, ALIAS, xAIF on the gold IR, verifying each layer against the intended outcome. 
- **Verification (Phase 2):** Build the initial Pāṭala API endpoints (`search_passages`, `read_passage`, `verify_quote`, etc.) on top of the static IR/graph. No ML yet. 
- **Benchmark tasks:** Derive 8 core tasks (passage segmentation, proposition extraction, commitment classification, relation classification, semantic alignment, inference labeling, counterfactual trace, crux identification) from these gold cases. This will seed a Pāṭala Benchmark (200+ items) to measure progress. 
- **Crux experiments (Phase 3):** Develop the minimal-crux algorithm outlined above and test on the gold cases. 
- **Iterate:** Use benchmark results to guide ML improvements (e.g., train a model to predict alignment or premise roles), always comparing to the gold baseline. 

Throughout, we adopt “**expose not infer**”: use deterministic outputs where possible (ASPIC+, AIF, Nyāya audits) and only apply learned models to tasks that genuinely require inference (e.g., initial proposition extraction, semantic parsing). The ultimate goal is a scholar-facing system that transparently lets users drill from a philosophical conclusion down through frames→propositions→passage, highlighting exactly where and why disagreement arises (the minimal crux). 

The vision is ambitious but grounded in existing work.  We stand on the shoulders of these argumentation frameworks and mining tools, repurposing them for *text-plus-provenance*. The **missing pieces** are precisely our IR-layer algorithms: alignment, commitment decoding, multi-regime logic, and especially crux extraction.  By building those on top of proven libraries, we can rapidly deliver on the promise of a provenance-rich, queryable philosophical argument engine. 

**Sources:** The above plan draws on the cited literature and existing projects, especially py-aspic, xAIF, oAMF, ALIAS, ArgLLMs, AKG conversion, and research on multi-perspective argumentation and counterfactual argumentation.