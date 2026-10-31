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
