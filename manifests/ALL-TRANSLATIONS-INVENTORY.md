# ALL TRANSLATION WORK — master inventory

Generated 2026-10-30 from volume + R2. Bytes stay where they are; this repo holds pointers + samples + process.

## A. IPVV (crown, most advanced)

- R2 `sanskritree/ipvv-translations/` — 229 objects (see `R2-IPVV-ALL.txt`): 28 Vol-1 T1 + 35 golden T1 + 109 pilot + L0 tarballs + artifacts.
- R2 `patala/public/published/` — 57 objects (see `PUBLISHED-ALL.txt`): 30 ipvv passages/essays/clusters + index.
- Local `patalacheckpoints/data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl` — 231 passages.
- Status: T1 frozen, L0 102k (96% PARSED), L2/ARGMAP pilot real, L200 63, C1 63, SYN/ESS/EDU 0.
- Work dir: `works/ipvv/WORK.md`. Samples: `samples/`.

## B. Tantraloka ahnikas (stockpile, chunk-ready)

- Volume `source-library/tantra/abhinavagupta/ahnika-01…37.txt` (01+04 = 1.7MB each, rest 1–15KB) + `gretil_tantraloka.txt` + `tantraloka-complete.txt` + vols 1–11 Dyczkowski.
- Volume `source-library/tantra/texts-clean/` — same ahnikas × 6 variants (CLEAN/COMPLETE/CURATED/DZYKOWSKI/READ/verses) + `chunks/ahnika1-chunk-1…7.txt` (224–264KB each, pre-split).
- Work dir: `works/tantraloka/WORK.md`. Next: run UPLOAD-RUNBOOK on ahnika-1 chunk-1.

## C. Tantrasara (DONE 2026-10-30)

- Volume `source-library/tantra/texts-clean/gretil_tantrasara_clean.txt` (Nirnaya Sagara 1918 via GRETIL).
- GitHub `prx0r/tantrasara` — essay-0 machine (98 spans, essay0.json canonical, rung picks A/B locked).
- Translation: 22 ahnikas, 51 passages, 712 verses, 4,579 L0 tokens, 7 gate PASS / 44 BLOCKED (attributed), 22 L200 + 22 C1 (machine), 14 theme seeds, 22 R2 batch files (byte-verified).
- R2: `s3://sanskritree/batch-t1/2026-10-30-tantrasara-a01..a22-raw.jsonl`.
- Work dir: `works/tantrasara/WORK.md`. Manifest: `manifests/tantrasara/R2-ALL.txt`.
- Next: tantraloka-a01 (per INDEX.json queue).

## D. VBT (technique catalog, not OS)

- Volume `source-library/tantra/lakshmanjoo/` — `vb_lakshmanjoo.json` (145 verses) + 2 epubs.
- Deitybody `site/frameworks/vbt/body-dharanas.json` (25 bodily) + `protocols/vbt_selected.json` + mapping in sanskrithelp RAG.
- Work dir: `works/vbt/WORK.md`.

## E. Krama cluster (furthest passages)

- Local `data/corpus/passages/`: kramasadbhava 563, kulasara 711, cidgaganacandrika 312, timirodghatana 231, maharthamanjari 74, tararahasya 67, kubjikamata 2437 (patala jsonl, not yet in passages/).
- RAW-EN (see `RAW-EN-68.txt`): kramasadbhava, kulasara, kubjika, kubjikamata, mahanayaprakasha, etc.
- Work dir: `works/krama-cluster/WORK.md`.

## F. Agama canon — 68 RAW-EN started

Full list: `manifests/RAW-EN-68.txt` (75 R2 objects incl. dupes) / 68 local jsonl. Highlights: malinivijayottara, netratantra + uddyota, svacchandatantra + uddyota, kiranatantra, matrkabhedatantra, sardhatrisa, mrgendra, pauskara, sivasutra, spandakarika + pradipika, vatulanatha, sivadrsti, tattvatraya, brahmayamala, devikalottara, etc. Plus puranic/vedic fellow-travellers (kurma, linga, kaivalya, etc.).
- R2 `patala/artifacts/translations/` — 75 objects (same set + dupes).
- Work dir: `works/agama-canon/WORK.md`. Next: malinivijayottara first (feeds deitybody MV ch.3).

## G. Spanda/Sutra + style gold (do not translate, use as few-shot)

- Volume `dyczkowski-translations/`: aphorisms 475KB, doctrine-of-vibration 710KB, spandakarika 1.7MB (wait — sizes from user; treat as style gold).
- RAW-EN has sivasutra, spandakarika, spandapradipika, sivadrsti already started — those ARE to translate; Dyczkowski English is the style reference.
- Work dir: `works/spanda-sutra/WORK.md`.

## H. Scholarship (anchors, not translation targets)

- Ratie 22 papers, Sanderson 112 (acquisitions/sanderson), hareesh-blog 199 posts, research-library recognition 22 essays, Timalsina, etc.
- Work dir: `works/scholarship/WORK.md`.

## How to run any of these

`process/UPLOAD-RUNBOOK.md`. One work = one `works/<name>/` folder with WORK.md (sources, counts, status, next). Commit pointers + samples, never bytes.
