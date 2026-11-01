# Voice corpus — index

Everything the C2 renderings stand on, in one folder. Registers kept separate:
US gen-z vs UK roadman. Same rule as the glossary: payload or ban.

## dictionaries/ — what words mean, who says them
- `turnitgenz.json` (54) — current gen-z terms + definitions + examples. Start here for gen-z voice.
- `roadman-az.json` (40) — London roadman A–Z with examples. Start here for roadman voice.
- `newsweek-topboy.json` (14) — Top Boy glossary with sentence use. Second opinion on roadman terms.
- `toronto-shared.json` (84) — Toronto lexicon rows flagged `shared_with_mle`: cross-dialect proof a term is really shared (not a Toronto-only lookalike). Use to validate: if your term isn't here or in MLE-core, treat as unvetted.
- `value-sae-aave.json` (1,050 pairs) — VALUE project's SAE→AAVE meaning-preserving mappings, fluent-speaker validated. Use for US-side payload checks.
- `toronto-slang.csv` (287 rows) — full Toronto lexicon with register/origin/offensiveness/core flags. Use `toronto_status` to separate shared vs Toronto-only vs performed-meme.
- `gen_z_slangs_translation.csv` (139 pairs) — older plain↔slang pairs. Normalization direction only; dated for generation.

## transcripts/ — the voice in the wild
- `cench-chickenshop.json` (13KB) — full Chicken Shop Date transcript. Cench cadence: circular honesty, "it's a lie until it's really real", motto-flips ("time will tell" → "time already told").

## parallels/ — sustained sacred renderings to study
- `genz-matthew6.json` (34 parallel verses, KJV beside) — proof a register holds across a chapter. Study "lowkey for secrecy".
- `magnificat-genz.json` (11 verses) — devotional-scholarly team method; independent bussin-for-nectar convergence.
- `baeble-pairs.json` (10 verses) — labeled AI paraphrase beside canon. The labeling precedent.

## doctrine/ — what counts as what
- `mle-core-47.json` — Ilbury/Grieve/Hall validated London core vocabulary. Authority list: if a roadman term isn't here or in toronto-shared, it's unvetted.
- `kym2025.json` (9 entries) — newest wave (chopped, TS PMO, SYBAU). Trend watch, not canon — slang dates fast.

## Worked lookups
1. "Can I use *leng* for bliss?" → roadman-az says weapon/dangerous person; turnitgenz-adjacent use says attractive; Toronto-shared lists leng=attractive/synonym of peng. Verdict: graded-only (lengest), never bare near power. (This exact check is filed in the glossary.)
2. "Is *bless up* real?" → newsweek-topboy: "leave the conversation on a positive note / wish well." Verdict: validated, salutation payload.
3. "Roadman or US import?" → check toronto_status (shared_with_mle vs toronto_only) + mle-core-47. Shared in both = safest ground.
4. "How does sustained sacred gen-z read?" → genz-matthew6 full chapter, then magnificat for the devotional register.
