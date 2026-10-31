# HANDOVER — ipvv, complete state for next agent

*Updated 2026-10-31. Read: HANDOVER-PUSHING.md (pushing method) → logs/AUDIT-2026-10-31.md
(what exists per layer) → process/SESSION-2026-10-30.md (full history) → specs/use-cases/
PLAN-v2.md (the arc). AGENTS.md has the laws. OWNERS.md has the lane rules.*

## 0. What this repo IS

Trika Śaivism translation + argument + essay platform. One text at a time, done properly.
Sanskrit → T1 → L0 → argmap → C1 → pushing → L200 → essay. Every layer gated, every
chunk traceable to source. Live: https://ipvv-a8u.pages.dev. GitHub: prx0r/ipvv master.

## 1. What's LIVE and GREEN (don't break)

- **Site:** 855+ pages. 49 IPVV + 44 translations + 145 VBT + 6 Tantrasara + 43
  Abhinavagupta works + 36 scholars + 100 concepts + 22 essays + 83 argument packets +
  112 VBT practices + 97 pushing probes + 16 contentions + 52 source-metaphysics +
  40 info-packets + 11 Ratié chapters + 11 Torella volume + 5 recognition-framework
  + 19 research files + 9 workbooks + 6 sfx sounds.
- **Backend:** Cloudflare Worker `ipvv-api.tradesprior.workers.dev` — RAG chat
  (Qwen3.8-Omni-Flash via DashScope + bge-m3 embed + rerank + graph traversal),
  per-text/multi-text (comma-separated works), proactive suggestions, question storage
  (D1), profiles/variants/bookmarks, theme adjudication, A3S style preview, MCP server
  (8 tools), SFX player. D1 db `ipvv` (aaefcfe9-5901-43a5-8a0f-4954356ae634).
- **Data:** corpus.jsonl (692 records), receipts.jsonl (546, kernel-verified),
  vectors.json (692, bge-m3, in R2 + Pages), essay-links (151), style_dataset
  (638 records/259 with output), llms.txt + 44 per-work files.
- **Gates:** verify.sh ALL PASS (60 warnings, all pipeline-lane). verify_site.py
  fail-closes on: gate leaks, missing mp3s, broken links, unindexed pages, unfilled
  templates, stale dist, receipt coverage + id-recomputation, argmap <150w,
  C1 outside 100-450w, argmap/C1 missing source.
- **qprivately kernel:** tools/qp_acom/ (vendored), 5 versioned gates (hashes pinned
  in verify_site), 546 transition() receipts, deterministic byte-reproducible.
- **Secrets:** DASHSCOPE_API_KEY in wrangler secret (not in git). .r2-env not in repo.
  Nothing sensitive committed — verified with git grep.

## 2. What's DONE per layer (the crown + reference work)

### IPVV (49 passages — the crown)
- T1 golden: complete in R2 (63 files), never lost.
- L2 + argmaps: 51 legacy argmaps in site/data/ipvv/argmaps/, embedded in pages.
- C1: 49/49 embedded in published records (body+terms+see_also+verse_commentary).
- Sanskrit roots: vendored (ipvv-vol{1,2,3}.txt), traceable.
- **L200: LOST** (63 files). Specs survive in specs/patala/. Regeneration = re-audit
  from T1+argmap+L2, starts at MACHINE_DRAFT. Pipeline lane job.
- **Standalone c1/read/ + c1/source/: LOST.** Embedded copies survive.

### Bhairavastava (10 verses — THE REFERENCE WORK, fully done)
- T1-full: 36 gloss units, 10 chunks, 102 tokens, 100% L0 parse (samples/).
- L0-report.txt saved. t1_extract.py now has --outdir flag.
- 10 argmaps (320-473w) — 6 carry Dyczkowski Bhairava Stava lecture insights
  (transcript: /root/tantraessays/transcripts/Bhairava_Stava_lecture.txt).
- 10 C1s (212-324w) — same 6 lecture additions.
- Pushing: full 10-question probe (4732w, ROUND 2 on Q1/Q3/Q5/Q7, claim statuses)
  + logicvid voice session (BHAIRAVASTAVA-session-grace.md, 3 penetrations + honest limit).
- 8 PASS / 2 BLOCKED (v2, v9 — argmaps written from Sanskrit, HOLD decisions).
- 10 studio chants with karaoke (kashaudio). Wired to recitation + chat.

### Other 43 works (the gap)
- 35 PASS total across 7 works (incl. bhairavastava 8 + kramastotra 11 + tantrasara 7).
- 379 BLOCKED. 414/414 Sanskrit-traced.
- 30 T1-full, 23 T1-head only. 10 L0 at 100% parse.
- **0 argmaps, 0 C1s, 0 pushing** outside bhairavastava + IPVV.
- Audit: logs/AUDIT-2026-10-31.md (the definitive gap list).

## 3. What to do NEXT (priority order)

1. **Push the next text** — kramastotra (30 chunks, T1-full+L0 done) or tantrasara (51).
   Follow Bhairavastava as template: immerse → argmap → C1 → pushing → L200 stub.
   Read HANDOVER-PUSHING.md + process/PUSHING-QUESTION-CRAFT.md first.
2. **L200 regeneration** — pipeline lane: 63 stubs from surviving T1+argmap+L2.
3. **Theme adjudication** — CL-3 packet ready at /themes/adjudicate.html (human decision).
4. **Unsloth Colab** — style_dataset-hf.jsonl (259 pairs) ready; training guide in
   specs/use-cases/embeddings-v2.md. Free tier sufficient (3B LoRA, <30min T4).
5. **Essay traceability** — essays → argument packets → source spans (spec'd, 151 links exist).
6. **Accept → grant** — wire /api/variants/:id/accept to signed qprivately receipt.
7. **Multi-text chat UI** — work-selector chips (backend supports comma-separated works).

## 4. Key files (find fast)

| What | Where |
|---|---|
| Laws + lane rules | AGENTS.md, OWNERS.md, process/CLAIMS.md |
| Pushing method | HANDOVER-PUSHING.md, process/PUSHING-QUESTION-CRAFT.md |
| Layer status | logs/AUDIT-2026-10-31.md |
| Session history | process/SESSION-2026-10-30.md (14 sections) |
| The plan | specs/use-cases/PLAN-v2.md, NEXT.md |
| Argmap/C1 reference | site/data/argmaps/bhairavastava/, site/data/c1/bhairavastava/ |
| Pushing corpus | site/data/pushing/{ipvv,tantraloka,research,rasa}/ |
| qprivately kernel | tools/qp_acom/, tools/qp_gates.py |
| Site gates | tools/verify.sh, tools/verify_site.py |
| Worker | worker/src/index.js (deploy: cd worker && wrangler deploy) |
| Embeddings | tools/build_embeddings.py → site/dist/data/vectors.json → R2 |
| Style dataset | tools/export_style_dataset.py → style_dataset-hf.jsonl |
| Session log | process/SESSION-2026-10-30.md (append §15 when you start) |

## 5. Rules that don't bend

- One text at a time, done properly. Quality from immersion, not batch generation.
- Frozen T1 never edited (Law #1). BLOCKED = no English, ever (fail-closed).
- Gates are fail-closed: verify_site.py FAIL blocks commits. Don't weaken gates.
- Machine proposes, human disposes. Argmaps/C1s/pushing are MACHINE_DRAFT until a
  human promotes.
- Secrets in wrangler secret or .r2-env only, never in git.
- Lane rules: site owns site/+specs/+tools/+process; pipeline owns works/+samples.
  git pull --rebase before every push; never force-push.
- Disk: 75G box, keep below 95%. Clean /tmp periodically.
- Push questions in the USER's voice (read logicvid sessions before writing yours).
