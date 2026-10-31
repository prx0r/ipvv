# Completeness audit: pipeline works vs IPVV bar (2026-10-31)

260 pipeline passages total, 34 PASS (deterministic gate only — format checks, not human acceptance).

| Layer | IPVV (reference) | Pipeline works (all 24) |
|---|---|---|
| T1 | 63 frozen chunks WITH inline hyperliteral glosses (human max-effort) | Raw Sanskrit segmentation only (0 PARSED L0 everywhere) |
| L0 | 102,157 token records, 96.4% PARSED | Effectively zero (unparsed; extractor not yet run on batch) |
| ARGMAP | 109 argument maps (human, freestyle method) | Machine only, unverified |
| L1/L2 | 109 human-reviewed READS + COMPARE layer | Machine drafts on 34 passed passages only; rest none |
| L200 | 63 eight-section audits, MT-vs-IA separated | Machine-claimed 8-section, unverified, heads-only in repo |
| C1 | 63 compact (100-450w), human, local | Grouped machine drafts, heads-only in repo |
| Published | 49 full passages, 4 views | 0 published; site shows PASS L1/L2 with gate badge (correct interim) |

Closest to the bar: bhairavastava (8/10 PASS), kramastotra (11/30), tantrasara (7/51).
Furthest: 15 works at 0 PASS (staging only — correctly displayed as Sanskrit + status).

What closes the gap, in order: run t1_extract → L0 on batch files → human L1/L2 pass on the 34 → L200 audits → C1 → publish. Bhairavastava first (smallest complete-ish unit: 10 verses).
Machine proposes, human disposes. No exceptions, no matter how "good enough" a draft reads.
