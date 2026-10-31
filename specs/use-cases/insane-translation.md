# Insane translation — re-roll, pick-best, own style, render everything

## The loop
1. **Re-roll.** Any chunk gets N variant rolls. Each roll is a qprivately processor
   RUN (run receipt: model, cost, prompt root, inputs/outputs roots). Variants that
   break the gate battery (esp. CITATION_GROUNDING) can't win — speculation runs
   free, truth stays gated.
2. **Pick-best.** Human accepts one variant per chunk (`accepted_by` + date).
   Selection pressure = human taste + gate battery. This is the `cg` evo loop
   (`cogym_kernel/evo/loop.py`) with `reasoning_styles.py` as the variant generator
   and `eval/gates.py` as the fitness floor: evolve freely above the floor.
3. **Own style.** User translates K verses themselves → those accepted pairs ARE the
   style profile (few-shot exemplars + a style card). No training needed for v1.
4. **Render everything.** A style is an acom-style module: inputs (T1+L1+argmap) →
   components (translate-with-exemplars, gate battery) → acceptance (gates pass)
   → outputs (`en_variants[style]`). Run it across the corpus; every chunk gains
   a `<style>` variant. **Flagship: Gen Z Tantraloka** — second-person, contractions,
   concrete analogies, zero thee/thou, same doctrine.
5. **ML method (phase 2).** Accepted pairs accumulate into SFT data; train a style
   LoRA per style; rolls get cheaper and closer. The style registry records method
   lineage: exemplars → accepted corpus → LoRA checkpoint. Method versioned +
   content-addressed like everything else.

## Data model (implemented forward-compatibly)
- Chunk records carry `en_variants: [{style, text, model, date, run_id, accepted}]`
  and `styles: [applied style ids]`. Ingest preserves them (never wiped by re-ingest).
- `site/data/styles/*.json`: style cards `{id, owner, register notes, exemplars[],
  method lineage}`. Seed: `gen-z` (flagship, exemplars pending owner input).

## Display (later, needs workbench)
- Variant switcher per chunk (PASS variants only; BLOCKED chunks roll Sanskrit-side
  paraphrases? No — BLOCKED means no English at all, any style).
- Owner's translation shown as `style: owner` variant; community styles namespaced
  by owner (style ids are `owner:style`).

## Rules that don't bend
- Every variant runs the FULL gate battery. A beautiful wrong translation loses to
  an ugly right one — then gets re-rolled.
- Accepted English is per-variant (`accepted_by` on the variant, not the chunk).
- Commercial witnesses never train styles (license firewall).

## Methods (surveyed Oct 2026 — concrete, current)
Pipeline position first: style applies to finished English (L2 READ), never to
Sanskrit parsing. Base translation = default weights (our gated pipeline output);
style = filter/adapter on top. (Not after C1 — C1 is commentary, a separate
register that keeps its own voice.)

1. **AuthorMix (EMNLP Oct 2026) — the scholar-style engine.** Modular LoRA library
   from high-resource authors + RL-learned layer-wise mixing for a new target from
   a handful of examples; <1hr adaptation; no target examples needed at inference.
   Ranks first on joint style–meaning score (beats GPT-5.1); meaning preservation
   is the headline metric — exactly the translation constraint. Mapping: base
   library = our house voices (Dyczkowski-mode L2, plain, gen-z seed); scholar's
   5–10 own verse translations → mixed adapter = their style.
2. **Hypernetwork LoRA (arXiv Oct 2026) — cold-start alternative.** Predicts LoRA
   adapters from author embeddings; best style–quality tradeoff; no per-author
   training. Use when exemplars <5 or instant onboarding matters.
3. **A3S aspect-aware steering (Sep 2026) — training-free instant try.** Multi-aspect
   (tone/perspective/structure/figurative) contrastive directions, interference-aware
   merge. Zero training: preview any style before committing to an adapter.
4. **CAUSAL-STEER / StyliTruth (ICLR 2026) — English filters as dials.** LoRA-as-
   intervention extracts stable style vectors (CAUSAL-STEER: continuous control,
   no parallel corpora); StyliTruth SVD-disentangles style subspace from truth
   subspace — stylized YET truthful, i.e. our "punch from diction, not dilution"
   rule as linear algebra. Filters (formality, second-person, concreteness) ride
   on top of any style adapter.
5. **InMyStyle pattern — per-scholar local adapters.** Rank-8 LoRA on small Qwen
   (0.5–7B), 3 epochs, response-only loss; small models sufficient; privacy-first
   (scholar's unpublished translations never leave their machine).

## Scholar flow (concrete)
Scholar translates 5–10 verses → A3S instant preview (seconds) → AuthorMix adapter
(<1hr) → generate rest in their style → gate battery runs every variant (meaning
floor) → human picks → `accepted_by` on winners → accepted pairs accumulate to
SFT/LoRA v2. Style card records method lineage throughout.
