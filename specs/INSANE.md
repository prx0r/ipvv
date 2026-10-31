# INSANE — what "fully computable Trika" actually takes, mapped to our stack

Read 2026-10-31: patala CORE-BIBLE, CATEGORIES (8 lenses), REVIEWS, essayguide
(six hard problems; EF-ESSAY-0001 traceability failure), V15 Atlas, V06/V07
(adversarial review, new scholar), education lens, V10/V11 (market, expansion).

## Their one sentence (CORE-BIBLE L0)
> One historically-grounded scholarly tradition fully computable: a single evidence
> graph from Sanskrit to scholarship to media, where every claim resolves to its
> source, and the whole thing reproduces across traditions.

## Where we already stand (their words, our artifacts)
- Evidence graph substrate: corpus.jsonl (454, gated) + argmaps + C1s + clusters +
  read-alongside + scholars + receipts pattern. **We have the graph.**
- Essay program: they call essay "a rendering of the graph" and record that their
  compiler produced untraceable sentences (EF-ESSAY-0001). Our 22 essays are
  human-thesis, same failure mode: prose, not linked to spans. **Same gap, smaller.**
- Atlas ("OpenAlex for Sanskrit"): transmission lineage Work→Edition→Witness.
  We hold the endpoints (vendored roots + GRETIL/Mukhabodha provenance + scholars
  + editions in bibliographies) but mint no identity layer. **Substrate without IDs.**
- Review: theirs is adversarial + runnable (aspirational). Ours is human docs
  (logs/qa). **Same direction, manual.**
- Surfaces: they spec multi-surface (V12). We spec'd chatbot/workbench/curriculum.
  **Specs, not builds.**

## The insane moves, ranked
1. **Essay traceability (the differentiator).** Link every essay thesis → argmap
   spans → L0 ranges → source lines. 22 essays × existing argmaps = tractable.
   Nobody has this: the first commentary tradition where every interpretive claim
   resolves to source *by construction*. Directly answers essayguide's six hard
   problems, starting with thesis selection + argument architecture. This is the
   feature that makes scholars cite us.
2. **Atlas identity seed.** Mint Work→Edition→Witness chains for our 84 held roots
   per their source-resolver design (authority ladder, no auto-promotion). Our
   read-alongside + provenance headers are the raw material. "OpenAlex for Sanskrit"
   starts as 84 chains, not a platform.
3. **Adversarial review as gates.** Encode the peer-review checklists (reference
   integrity, verbatim quotes, limits named) as runnable gates in the qprivately
   idiom. New essay/translation displays only on traceability PASS. Their V06,
   our verify_site pattern, one mechanism.
4. **Surfaces from one core.** Build order: chatbot (weekend) → workbench (carries
   accounts) → curriculum. All read corpus.jsonl. (Spec'd in use-cases/.)
5. **Economics + expansion.** Support→Patreon now; scholar incentives/market per
   V10 later — with a real path: Williams (Muktabodha scholar-in-residence) is
   already in our scholars. Corpus expansion per V11 (Śiva-before-Abhinava): we
   already hold wider-canon GRETIL roots; the queue manifest is the intake list.

## What NOT to chase
- Their ARGUMENT/SYNTHESIS compilers read PARTIAL/0 objects — but our argmaps ARE
  argument objects. Feed ours backward into their factory rather than rebuilding it.
- Education engine before traceability: teaching untraced claims at scale is
  EF-ESSAY-0001 with distribution.
