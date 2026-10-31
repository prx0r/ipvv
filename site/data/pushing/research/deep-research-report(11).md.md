# Executive Summary  
Pāṭala’s architecture aligns with cutting-edge argument-mining research: tools like py-aspic, oAMF and ArgLLM match its ASPIC+, AIF/xAIF, and contestable reasoning components. Recent surveys highlight that LLMs now handle claim/premise detection, relations and stances, suggesting Pāṭala can leverage prompt-based pipelines (e.g. LangGraph) alongside formal engines.  

**Research Gaps:** Semantic‐alignment is nontrivial – word‐sense disambiguation remains an open challenge across languages. “Commitment” annotation (who said what) has no existing NLP solution; it will require custom discourse parsing or manual curation. Multi‐regime semantics (Śaiva vs. Buddhist logics) have been formalized in Epistemic Argumentation Frameworks, but no off‐the‐shelf tool implements them – custom labelings or multi-agent runs will be needed. “Crux extraction” (minimal pivotal premises) is essentially a minimal-hitting-set or abductive inference problem; it is novel and potentially NP-hard. No existing library solves it, so prototype brute-force or graph‐explanation methods must be explored (e.g. related GNN explanation work).  

**Market & Ecosystem:** Primary users are humanities scholars (Indology, Buddhist studies, philosophy) and digital-humanities researchers. Value lies in transparent dialectical analysis, provenance, and cross‐tradition comparison. Potential funders include research foundations (NEH/Mellon/ACLS), Buddhist organizations (Khyentse Foundation, British Library), and universities. No direct competitor offers similar depth (general tools like Carneades or Kialo lack the necessary scholarly grounding). Adoption will require building a critical mass: initial seed data (e.g. via a fellowship or workshop) and open APIs to integrate with scholar workflows. 

**Scholar Impact:** AI tooling will shift scholars’ work from manual exegesis to oversight and interpretation of machine‐extracted arguments. Incentives include co-authorship on critical editions, fellowships for data annotation, and tools for teaching. A cold‐start strategy is to partner with a small expert lab (e.g. digital Indology center), use its disputations as seed data, and demonstrate early wins in professor peer groups.

**Roadmap (12 mo):** Phase 0 (Sept–Dec 2026): *Gold annotation* of 5–10 annotated IPVV debates to finalize the IR schema (propositions, frames, commitments). Simultaneously *pilot semantic alignment* approaches (LLM/WSD suggestions, expert review). Phase 1 (Jan–Apr 2027): *Prototype core engine* – implement py-aspic pipelines on sample arguments; test Commitment extraction with LLMs or rules; run the Nyāya fallacy gate on annotated cases. Conduct *crux-tractability study* on small graphs (try brute-force/minimal explanations). Phase 2 (May–Aug 2027): *Integration and Evaluation* – combine all modules in an oAMF pipeline; evaluate end-to-end on the gold disputes. Prepare a **Beta release** (web demo/API) for early adopters. **Go/No-Go criteria:** If by Month 8 Pāṭala’s inferred argument states match expert judgments on >80% of test cases (including identification of main cruxes) and no gap in core functionality, proceed to community rollout; otherwise, revisit problematic modules (e.g. alignment or commitment).  

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title Pāṭala 12-Month Roadmap
    section Phase 0 – Gold IR
    Gold-Annotation         :crit, 2026-09-01, 60d
    Semantic-Alignment-Pilot: after Gold-Annotation, 45d
    section Phase 1 – Prototyping
    Py-ASPIC-Integration    :2026-12-01, 45d
    Commitment-Extraction   :after Py-ASPIC-Integration, 45d
    Crux-Experiment         :2027-03-01, 30d
    section Phase 2 – Integration
    Beta-Prototype          :2027-04-15, 60d
    ```

```mermaid
flowchart LR
    Text["Scholarly Text"] --> IR["Structured IR (propositions, frames)"]
    IR --> ASPIC["ASPIC+ Reasoner"]
    IR --> Logic["Formal Logic Checker"]
    IR --> Nyaya["Nyāya Fallacy Checker"]
    ASPIC --> Output["Argument State Report"]
    Logic --> Output
    Nyaya --> Output
```

**Recommendation:** Leverage existing tools wherever possible (py-aspic, oAMF, LangGraph pipelines). Prioritize high-leverage experiments: encode gold arguments (to validate modeling), run a py-aspic pilot, and attempt a small-scale crux search. Iterate with domain experts. Commercializing via fellowships or services (annotation sprints, custom analyses) can kickstart data generation.  

**Sources:** Key literature includes recent AM surveys, ASPIC+/AIF resources, ArgLLM code, and new neurosymbolic work. The GNN-for-ABA paper indicates how neural methods may scale reasoning. Together these point a feasible path: don’t build all from scratch, but adapt mature argument tech and LLMs to the Pāṭala framework, guided by scholar-in-the-loop evaluation.