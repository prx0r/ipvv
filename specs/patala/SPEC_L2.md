# SPEC — L2 (the readable published prose)

*The third layer. L2 is what the reader reads — clean, flowing, readable English. It is the
published surface of the whole stack. Everything below it (L0/L1/L200/Sanskrit) is the evidence it
rests on.*

---

## 1. What L2 is

The READ view: "clean English." It is:
- readable as a book (a reader follows it straight through);
- faithful (every proposition traceable to the source stack);
- close enough that a scholar can verify it (span → decision → Sanskrit);
- never silently smoothed over an obscure passage into false clarity.

## 2. The register (Dyczkowski-mode)

Dense, reasoned, flowing commentary prose with parentheses carrying glosses; technical terms
transliterated + explained; reason, don't report; keep the argument's motion; keep the term-ledger
consistent.

## 3. Term-ledger (Pratyabhijñā register)

```
prakāśa = light/luminosity (manifestation)   vimarśa = reflexive awareness
saṃvit = consciousness                        svātantrya = freedom
pramātṛ = the knower/subject                  pramāṇa/prameya/pramiti = means/object/result
viśrānti = resting (in consciousness)         ābhāsa = appearance
pratyabhijñā = recognition                    pratyavamarsa = re-cognition
ahaṃ/idam = I / this                          unmeṣa/nimeṣa = opening/closing
jñāna/icchā/kriyā = knowledge/will/action
```

## 4. Task-1 (READER QA)

L2 is judged by the **prose-only** condition (the reader has no map): can the prose carry the
argument as a book? The v1 Task-1 toolchain evaluates this. Note: the gold was over-logged; re-grade
before trusting any recall number (see `V1_THREE_CONDITION_FINDINGS.md`).

## 5. L2 → source resolvability

Every L2 sentence resolves: L2 ¶ → argument-map segment → L0 record range → source range. This is
the L200 derivation map, surfaced to the reader (the COMPARE view).

---

## 6. EXEMPLARS — what it looks like in the IPVV

### L2 READ (the published prose)

`pilot/pilot_V3C_L2_read.md` — the "one light" passage as readable prose. It shows the register in
practice: continuous, reasoned, parenthetical glosses, term-ledger applied. It is produced **from**
`pilot/pilot_V3C_ARGUMENT_MAP.md` (reconstruct the argument, not the sentence).

`pilot/pilot_V2O_L2_read.md` — the saptamo vimarśa (the one support) — a canonical-model L2.

### The argument map it derives from

`pilot/pilot_V3C_ARGUMENT_MAP.md` — the reconstruction (speaker, question, premises, inference,
conclusion, unresolved terms) that the L2 writes from. The L1 lesson: **reconstruct the argument,
not the sentence** (see `IPVV_FREESTYLE_LESSONS.md`).

### The fidelity note (how L2 declares what it did)

Every L2 read ends with a **Fidelity note**: Preserved / Added (SUPPLIED, recoverable) / NOT
resolved. Example — `pilot/pilot_V3C_L2_read.md`'s note separates what the prose preserved, what
it supplied (marked recoverable), and what it left unresolved (the upādhi-contraction detail,
the pā. vā. citation).

---

## 7. VALIDATION — how we know L2 is correct

**Per-paragraph (Task-1, prose-only — the reader condition):**
- [ ] the paragraph reads coherently as a book, WITHOUT the map (the prose-only evaluator)
- [ ] every proposition is traceable to the argument map + L0 (no invented content)
- [ ] the term-ledger is applied consistently (vimarśa = reflexive awareness, etc.)
- [ ] SUPPLIED content is marked (bracketed or in the fidelity note) and recoverable
- [ ] the fidelity note records Preserved / Added / NOT-resolved honestly

**Per-paragraph (Task-2, fidelity — the source condition):**
- [ ] no LOST/ADDED proposition, polarity, speaker, referent, or term-sense defect against the
      source stack (see SPEC_FACTORY_QA §1 v2)

**Factory-wide:**
- [ ] the prose-only gold is re-graded (over-logged items dropped) before any recall metric is
      published
- [ ] every L2 ¶ has a derivation-map entry in its L200 (L2 ¶ → argmap → L0 range → source range)

---

## 8. The READ / COMPARE / LITERAL / CRITICAL views

L2 is the READ view. The same passage is shown as:
```
READ      L2 prose
COMPARE   L2 ∥ L1/T1 (Sanskrit + controlled)
LITERAL   L0 records + IAST + glosses
CRITICAL  L200 derivation + decisions + source-layer + C1
```
The reader resolves any L2 sentence to its evidence. See the pāṭala reader
`app/read/[work]/[locator]/page.tsx` for the live implementation.
