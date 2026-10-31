# works/tantraloka — PREP NOTES (scholarly resources + difficulties)

## Scholarly resources (web search 2026-10-30)

### Complete translations
1. **Mark Dyczkowski** (11 vols, Amazon) — THE definitive English translation. 45 years of work.
   Full, minutely accurate translation of both Abhinavagupta's text AND Jayaratha's commentary.
   Worked directly with manuscripts; made improvements to published edition.
   Collected all known unpublished sources Abhinavagupta quotes.
   Extensive detailed notes from Kashmiri masters' works + Swami Lakshmanjoo's teachings.
   **Use as**: style reference + verification, NOT as input (copyright).

2. **Swami Lakshmanjoo** — "Kashmir Shaivism – The Secret Supreme" (1985).
   English translation of first 18 chapters. Oral tradition perspective.
   Refuted Jayaratha's commentary in places (Jayaratha not from oral tradition).
   Emphasized: "without direct experience and connection to the oral tradition,
   it is almost impossible to understand Abhinavagupta's words."
   **Use as**: interpretive guidance for ahnikas 1-18.

3. **Satya Prakash Singh & Swami Maheshvarananda** — "Sri Tantraloka & other works"
   (KSTS edition with translatory notes in English, on archive.org).
   Bilingual Sanskrit-English. Criticized for ungrammatical English but invaluable.
   **Use as**: Sanskrit edition reference + English glosses.

### Partial translations
4. **Christopher Wallis (Hareesh.org)** — Blog posts translating Tantrāloka 1.1-21, 1.22-51,
   1.59-69, 1.68-81, 1.95-100, 1.101-105, 1.106-116, 1.116-123, 1.124-133, 1.135-139, 1.140-151.
   Respected Sanskrit scholar, gifted writer. Excellent style reference.
   **Use as**: style calibration for ahnika 1.

5. **John R. Dupuche** — Translation of Chapter 29 (Kula ritual) with Jayaratha's commentary.
   First English translation of any chapter WITH commentary. Shows structure.
   **Use as**: model for how to handle Jayaratha's commentary.

6. **Raneiro Gnoli** — Italian translation (1972) of text WITHOUT commentary.
   **Use as**: cross-reference for difficult passages.

7. **Lillian Silburn & André Padoux** — French translation of first 5 chapters (1998)
   with comments and extracts from Jayaratha's Viveka.
   **Use as**: cross-reference for ahnikas 1-5.

8. **Gabriel Pradīpaka** — sanskrit-trikashaivism.com: Tantrāloka introduction + some passages.
   **Use as**: orientation.

### Key scholarly observations
- "Abhinavagupta's verses are very terse and often contain several levels of meaning"
- "It is necessary to consult Jayaratha's commentary for a complete understanding"
- "Tantrāloka is essentially a book for masters" (Lakshmanjoo)
- "The structure is not a confused mass of codes but is articulated as finely as an Indian temple" (Dupuche)
- Jayaratha's commentary: "more than 1150 lines of about 18 syllables each" for ahnika 29 alone
- Dyczkowski: "collected all known unpublished sources Abhinavagupta quotes"


## R2 resources found (2026-10-31)

### Source text
- `source-library/tantra/abhinavagupta/ahnika-01…37.txt` — raw ahnika files (01+04 = 1.7MB, rest small)
- `source-library/tantra/gretil_tantraloka.txt` — GRETIL full text (771KB, 17,642 lines, 5,826 verses)
- `source-library/tantra/tantraloka-complete.txt` — complete text (3.9MB)

### Cleaned versions
- `source-library/tantra/texts-clean/ahnika-N-{CLEAN,CURATED,DZYKOWSKI,READ,verses}.txt`
  - CURATED = clean verse text (66KB for ahnika-01, vs 1.6MB COMPLETE)
  - DZYKOWSKI = Dyczkowski's translation (style gold)
  - READ = readable version
  - verses = verse-only extraction
- `source-library/tantra/texts-clean/chunks/ahnika1-chunk-1…7.txt` (226-266KB each — still 50× too big, re-split)

### Scholarly translations (style reference)
- `source-library/tantra/dyczkowski-translations/` — aphorisms-of-siva (474KB), doctrine-of-vibration (710KB), spandakarika (1.6MB)
- `source-library/tantra/explained-hareesh/tantraloka/` — 13 HTML files covering Tantrāloka 1.1-151 (Hareesh/Wallis explained versions)
- `source-library/tantra/hareesh-blog/` — by-topic + hareesh.org (INDEX.md 7.5KB)
- `source-library/tantra/lakshmanjoo/` — lakshmanjoo-vijnana-bhairava.epub (2.3MB), vb_lakshmanjoo.json (44KB)

### Other
- `source-library/tantra/trika/` — Trika materials
- `source-library/tantra/utpaladeva-ipk/` — Utpaladeva's IPK
- `source-library/tantra/source/` — source materials
- `source-library/tantra/matter-of-wonder/` — matter of wonder
- `source-library/tantra/hermeneutics-of-absolute/` — hermeneutics
- `source-library/tantra/blog-sanskritree/` — blog-sanskritree

### Downloaded (local)
- `/root/tantraloka-resources/tantraloka-singh-djvu.txt` (547KB, Singh/Maheshvarananda vol 1, OCR'd)
- `/root/tantraloka-resources/tantraloka-vol2-djvu.txt` (596KB, vol 2)
- `/root/tantraloka-resources/tantraloka-vol3-djvu.txt` (620KB, vol 3)

## Difficulties (quick review of text)

### 1. Scale
- 37 ahnikas, 5,826 verses, 17,642 lines.
- Ahnika 1 alone: 331 verses (already done).
- Largest: ahnika 15 (612v), 8 (451v), 28 (433v), 13 (360v), 1 (331v).
- Smallest: 34 (3v), 18 (11v), 20 (15v), 36 (15v), 12 (24v).

### 2. Jayaratha's Viveka commentary is ESSENTIAL
- Abhinava's verses are extremely terse (often 2-4 words per pāda).
- Jayaratha's commentary is often 10-50x longer than the verse.
- The commentary explains obscure terms, identifies quotations, resolves ambiguities.
- BUT: Jayaratha is sometimes "misleading" per Lakshmanjoo (not from oral tradition).
- Strategy: use Jayaratha for identification/clarification, not as sole authority.

### 3. Extensive quotations from other texts
- Abhinava quotes from: Mālinīvijayottara, Svacchandatantra, Kiraṇatantra,
  Mātṛkābhedatantra, Netratantra, Spandakārikā, Vijñānabhairava, etc.
- Need to identify quotation boundaries and handle them (some are verbatim, some paraphrased).
- Dyczkowski collected unpublished sources — we don't have access to those.

### 4. Technical terminology varies by context
- Same term (e.g., "śakti", "prakāśa", "vimarśa") can mean different things
  in different ahnikas (metaphysical vs ritual vs yogic context).
- Need per-ahnika term ledger, not just global glossary.

### 5. The work covers everything
- Metaphysics (tattvas, pramātṛ levels)
- Ritual (kula ritual, yāga, homa, dīkṣā)
- Yoga (dhāraṇā, samādhi, khecarī)
- Aesthetics (rasa, dhvani)
- Epistemology (pramāṇa, anupalabdhi)
- Cosmology (224 worlds, 36 tattvas)

### 6. Abhinava's style
- Extremely compound-heavy (samāsa).
- Often uses paradox and wordplay (śleṣa).
- Quotes opponents and refutes them.
- Uses "I" voice (first person) in many places.
- Mixes prose and verse (the commentary is in prose, the root text in verse).

### 7. Jayaratha vs. Lakshmanjoo
- Lakshmanjoo: Jayaratha not from oral tradition, sometimes misleading.
- But Jayaratha is the only complete commentary.
- Strategy: use Jayaratha for structure/identification, cross-check with Lakshmanjoo's
  published translations where available.

### 8. Manuscript variations
- Dyczkowski worked with manuscripts and made improvements.
- Our source (GRETIL KSTS) may have errors.
- Strategy: note variants, don't try to resolve (out of scope).


## Dyczkowski Tantrāloka (DOWNLOADED 2026-10-31)

All 11 volumes downloaded to `/root/tantraloka-resources/dyczkowski/`:
- tantraloka-vol1-dyczkowski.txt through tantraloka-vol11-dyczkowski.txt (15MB total)
- Full English translation of both Abhinavagupta's text AND Jayaratha's Viveka commentary
- Extensive explanatory notes from Kashmiri masters + Swami Lakshmanjoo
- Worked directly with manuscripts; made improvements to published edition
- Collected all known unpublished sources Abhinavagupta quotes

**Use as**: THE definitive style reference + verification. Imitate clarity, do not translate those.
**Coverage**: Vol 1 = Chapter 1 (ahnika 1). Vol 2 = Chapters 2-3. Vol 3 = Chapters 4-5. Etc.
**Key advantage**: Jayaratha's commentary is included — essential for understanding Abhinava's terse verses.

## Attack plan (refined)

### Phase 1: Tiny ahnikas (9 ahnikas, ~200v) — PROVE LOOP
Start with: 34(3v), 18(11v), 20(15v), 36(15v), 12(24v), 24(23v), 25(28v), 33(32v), 35(44v)
These are small enough to do in 1 session each.

### Phase 2: Small ahnikas (12 ahnikas, ~900v) — BUILD MOMENTUM
7(70v), 11(117v), 17(122v), 19(56v), 21(61v), 23(103v), 26(75v), 27(58v), 30(123v), 31(163v), 32(67v), 37(85v)

### Phase 3: Medium ahnikas (5 ahnikas, ~1,126v) — SCALE UP
2(50v), 5(157v), 9(313v), 10(308v), 29(291v)

### Phase 4: Large ahnikas (5 ahnikas, ~1,719v) — HEAVY LIFTING
6(250v), 8(451v), 13(360v), 16(311v), 28(433v)

### Phase 5: Huge ahnikas (3 ahnikas, ~1,182v) — OVERNIGHT RUNS
3(293v), 4(277v), 15(612v)

## Per-ahnika pipeline (proven on 24 works)

1. Extract ahnika from tantraloka.txt (line ranges known).
2. Chunk verses with tools/chunker.py (--split verse, 10-15 verses/passage).
3. Draft T1 hyperliteral [and]-GLOSS (IAST), term-ledger locked, then FREEZE.
4. t1_extract.py → L0 (expect ~96% PARSED).
5. ARGMAP per chunk (speaker/question/premises/inference/conclusion/unresolved).
6. L1 (COMPARE, keep compounds) → L2 (READ from ARGMAP+L0, Dyczkowski-mode).
7. L200 8-section audit (MT vs IA strictly separated).
8. C1 100-450w passage-local.
9. Gate (deterministic proof + TranslationProof vector).
10. Upload R2 (byte-verify).
11. Register in OpenPāṭala (translations table).
12. Update STATUS + ipvv WORK.md + git push.

## Cross-references for Tantrāloka

- Tantrasāra (already done) = Abhinava's own summary of Tantrāloka.
- Use Tantrasāra as a "map" for Tantrāloka — the Tantrasāra covers the same topics in abbreviated form.
- Pratyabhijñāhṛdaya (Kṣemarāja) = summary of Pratyabhijñā system (referenced in Tantrāloka).
- Īśvarapratyabhijñāvimarśinī (Abhinava's own commentary on Utpaladeva's ĪPK) = deeper treatment.
- Spandakārikā + Spandakārikānirṇaya (Kṣemarāja) = spanda doctrine.
- Svacchandatantra = major source text for ahnikas 7-8.
- Mālinīvijayottara = major source text for ahnika 3.
- Netratantra = major source text for ahnikas 13-14.
