# PLAN — insane translation program (ordered, gated, owned)

Goal: any chunk re-rollable in any style, human picks, style renderable across the
corpus, everything gated. Each phase ships something real; no phase starts until
the previous phase's gate passes.

## Phase 0 — Foundations (DONE, verify before proceeding)
- [x] 414/414 chunks traceable (source file + line + license + immutable id)
- [x] corpus.jsonl (608 records, gate labels, stable ids)
- [x] receipts.jsonl via qprivately kernel (463, deterministic, tamper-checked)
- [x] style registry + gen-z seed card; `en_variants[]` preserved by ingest
- Gate to Phase 1: `bash tools/verify.sh` green (it is).

## Phase 1 — Re-roll + pick-best UI (site lane, no backend)
- Variant roll runner: given chunk + style card, produce N candidates via CF
  Workers AI free-tier models (llama-3.3-70b primary, mistral/qwen rotation for
  validity), each with run receipt (model, cost, prompt root).
- Gate battery on every variant (existing gates + A3S-style meaning check).
- Display: variant switcher on translation pages (PASS variants only).
- Owner action needed: NONE (all machine). Human picks land in Phase 2 UI.
- Done = 1 work fully rolled (kramastotra: 30 chunks × 3 variants), all receipts green.

## Phase 2 — Human picks + accounts backend (new project: Worker + D1)
- Accept/reject per variant → `accepted_by` (name + date). Accept is the publish grant.
- Profiles: own translations saved per user; custom variants namespaced `owner:style`.
- Human translation input: paste own verse translation → runs gate battery → variant.
- Owner action needed: YOU translate 5–10 Bhairavastava verses (fixes gen-z exemplars).
- Done = gen-z style card has owner exemplars; accept flow live on 1 work.

## Phase 3 — Style adapters (needs GPU: Kaggle quota or Bailian fine-tune)
- A3S instant preview from exemplars (seconds, training-free).
- AuthorMix adapter per style (<1hr RL mixing over house-voice library).
- Render: run style module across corpus → `en_variants[style]` everywhere.
- Flagship: Gen Z Tantraloka (all 37 ahnikas in gen-z voice, gates green).
- Owner action needed: approve flagship before publish (stills-before-renders law).
- Done = gen-z Tantraloka live behind variant switcher, all variants gate-PASS.

## Phase 4 — ML loop + judges (ongoing)
- Accepted pairs → SFT data → style LoRA v2 per style (method lineage recorded).
- Kev-style decision models for gates (fast/cheap PASS/FAIL over chunk-candidate
  pairs) and rerank stage. Judges never write; adapters never judge.
- Done = gate latency/cost down 10× with zero verdict changes (measured, not claimed).

## Lane rules (unchanged)
- Site lane: player, pages, verify, specs, styles registry, workbench UI.
- Pipeline lane: T1/L0/C1 records, gate definitions, adapter training runs.
- Owner: exemplars, accepts, flagship approval, Patreon URL (still pending).
- Never: BLOCKED English in any style; commercial witnesses training styles;
  silent gate edits (new id or it didn't happen).
