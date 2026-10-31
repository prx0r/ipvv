# QA vs witness — sivasutra

## 1. Coverage
- root: `site/data/sanskrit/sivasutra-root.txt` (55376 bytes, 75 verse markers: ['1.1', '1.2', '1.3'] ... ['3.43', '3.44', '3.45'])

## 2. Sanskrit match
- batch: `batch-t1/2026-10-30-sivasutra-raw.jsonl` — 8/8 passages match held root (OK)
- all matched

## 3. Ledger vs witness renderings
- witness: dyczkowski-aphorisms (SUNY commercial — compare only, quote <=25w); covers: 77 sutras + Bhaskara varttika
- `caitanya` → witness: BRAHMA. The first sutra—CAITANYAMATMA: Consciousness is the Self—displays the original and multidimensional
- `jJAna` → witness: consciousness (jfianasphara) is withdrawn and recedes (nimijjana), there emerges a clear vision of the extending chain of
- `bandha` → witness: jnanambandhah
- `mAtRkA` → witness: 4. The ground of knowledge is Matrka.
- `udyoga` → witness: (and perfect) in all respects. 'Exertion' (udyoga), 'expansion'
- `bhairava` → witness: 5. Bhairava is upsurge.
- `zAkta` → witness: grace (tivramadhya), by a knowledge of (Siva's) power (saktavijnana) and those whose grace is weak (manda) by a knowledge of the individual
- `Anava` → witness: The contracted, individual Self (anavatman) is made
- `zAmbhavopAya` → witness: Means (sambhavopaya) and so, without having to meditate or
- `vimarza` → witness: vimarsa. This is the stance of the great cosmic dreamer who is
- `pratyabhijJA` → witness: — no hit —

## 4. Sample claim spot-checks
- L200-head.md: keywords [] — in witness: NONE; unsupported here: none
- C1-head.md: keywords [] — in witness: NONE; unsupported here: none
- T1-head.md: keywords [] — in witness: NONE; unsupported here: none

## 5. Gate re-verification
- WORK.md gate: 0 PASS / 8 BLOCKED (abstention — heuristic, not translation errors)
- block/fail mentions: 2

## Verdict: HOLD (pipeline gate correctly blocking (0 PASS) — staging verified sound, full translation not yet shippable; samples display only)

_Witness is comparison only (fair use, <=25-word quotes). Licensed status recorded above; nothing hosted._