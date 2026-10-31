# NEXT — ordered queue (site returns, GPU unblocks styles)

## Site-lane (our lane, no backend, do now)
1. **Verify live layout** — screenshot review of homepage, one translation page,
   recite, practices, arguments, essays, pushing. Fix anything ugly.
2. **Meditate page cleanup** — remove duplicate /meditate/ (subsumed by /practices/),
   redirect or merge. Keep one entry point.
3. **Navigation audit** — topnav has 11 items (too wide). Group: Recite·Practices·
   Essays·Pushing·Tools·Support. Master/Scholars/Concepts into a Library dropdown.
4. **Search-index gaps** — verify_site still warns on a few pages (torella ch9 etc).
   Make search walk dist/ recursively at build end.
5. **llm.txt refresh** — add practices, vbt-map, screen, meditate, stylelab sections.
6. **essays-group links** — Essays index group headers should deep-link to anchors.

## Backend-lane (Worker + D1, our account)
7. **Per-text chat UI polish** — work selector chips in the Ask panel (tap to add/remove
   works instead of ?works= URL params).
8. **Variant switcher inline** — show PASS-variant preview inline on translation page,
   not behind a button.
9. **Accept flow** — /api/variants/:id/accept already exists; wire to qprivately grant
   (accepted_by signed receipt) instead of simple UPDATE.
10. **Chat export** — button to download session as JSON (for pushing corpus import).

## GPU lane (style adapters — Colab viable)
11. **Colab for AuthorMix** — yes. Colab free T4 is enough for LoRA r=8 on a 0.5–7B
    base model. Steps:
    a. Build dataset: our accepted pairs (house L2 output) as style exemplars.
    b. Base: Qwen2.5-0.5B or Llama-3.2-1B (both Apache 2.0, both on Colab).
    c. Train: LoRA r=8, 3 epochs, single T4 (free tier, ~30min for 500 pairs).
    d. Export: GGUF Q4 → upload to R2 → serve via llama.cpp on Colab/your box.
    e. Reference: AuthorMix paper (EMNLP 2026) has the mixing recipe.
12. **A3S preview → exemplar** — paste gen-z seed verses into /stylelab/, save
    winners as exemplars to styles/gen-z.json (unblocks AuthorMix dataset).
13. **Style registry → variant render** — once LoRA works: re-render 3 test chunks
    in style → human picks → if gates pass, add as en_variants[gen-z].

## Blocking dependencies
- Colab GPU for #11–13 (free tier is sufficient).
- Owner: 5–10 gen-z exemplar verses (fastest path to any style).
- Owner: Patreon URL (Support page still says "launching soon").
- Owner: CL-3 theme adjudication call (themes layer unblocks).
