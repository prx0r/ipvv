# QA vs witness — spanda

## 1. Coverage
- root: `site/data/sanskrit/spanda-root.txt` (5767 bytes, 52 verse markers: ['1', '2', '3'] ... ['19', '1', '2'])

## 2. Sanskrit match
- batch: `batch-t1/2026-10-30-spanda-raw.jsonl` — 6/6 passages match held root (OK)
- all matched

## 3. Ledger vs witness renderings
- witness: dyczkowski-stanzas (SUNY commercial — compare only, quote <=25w); covers: 52-53 karikas + 4 commentaries
- `spanda` → witness: The SpandaKarika with Four Commentaries:
- `unmeSa` → witness: ENERGIES BY WHOSE EXPANSION (UNMESA)
- `nimeSa` → witness: AND CONTRACTION (NIMESA) THE UNIVERSE
- `sphurattA` → witness: (sphuratta), 'wave' (urmi), 'strength' (bala),
- `vimarza` → witness: The self-awareness (svavimarsa) in the Heart from
- `svAtantrya` → witness: autonomy of Siva (svatantrya)90 as
- `pramAtR` → witness: Ajadapramatrsiddhi
- `bandha` → witness: Thus the relationship (sambandha) between
- `mokSa` → witness: Other notable examples are the Stanzas on Liberation (Moksakarika) and the Stanzas on Worldly
- `jIvanmukta` → witness: — no hit —
- `kramamudrA` → witness: — no hit —

## 4. Sample claim spot-checks
- L200-head.md: keywords ['spanda'] — in witness: ['spanda']; unsupported here: none
- C1-head.md: keywords ['spanda'] — in witness: ['spanda']; unsupported here: none
- T1-head.md: keywords ['spanda'] — in witness: ['spanda']; unsupported here: none

## 5. Gate re-verification
- WORK.md gate: 0 PASS / 6 BLOCKED (abstention + citation grounding + coverage — heuristic, not translation errors)
- block/fail mentions: 2

## Verdict: HOLD (pipeline gate correctly blocking (0 PASS) — staging verified sound, full translation not yet shippable; samples display only)

_Witness is comparison only (fair use, <=25-word quotes). Licensed status recorded above; nothing hosted._