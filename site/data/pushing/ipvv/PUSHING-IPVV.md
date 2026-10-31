# PUSHING-IPVV — hounding the Īśvarapratyabhijñāvivṛtivimarśinī

*The working scaffold for the IPVV (Abhinavagupta's commentary on Utpaladeva's ĪPK). The method is
the same as PUSHING-TANTRALOKA: hound the text with "why," force its own reasoning, extract and
document. But here we focus MORE on the IPVV's own internal structure (the vimarśas, the nanu→āha
dialectical skeleton, the three adhikāras) and LESS on our frameworks — letting Abhinavagupta's
commentary speak on its own terms before we bring anything of ours in.*

---

## The primary material

| Layer | Location |
|-------|----------|
| The T1 golden chunks (all 3 volumes) | `sanskritree/translations/_stack/ipvv/02_t1/` (Vol 2: V2-A…S; Vol 3: V3-A…P) + `01_t1/` (Vol 1) |
| The L2 READ versions (the readable layer) | `sanskritree/translations/_stack/ipvv/pilot/` (V1-A…N, V2-A…S, V3-A…P — each with an ARGUMENT_MAP) |
| The plain-English bridge plan | `research-library/recognition/IPVV-PLAIN-ENGLISH-BRIDGE.md` |
| The progress tracker | `research-library/recognition/IPVV-PROGRESS-TRACKER.md` |
| The freestyle lessons (the method) | `sanskritree/translations/_stack/ipvv/IPVV_FREESTYLE_LESSONS.md` |
| The process notes + roadmap | `sanskritree/translations/_stack/ipvv/IPVV_PROCESS_NEXT_STEPS.md` |

---

## The IPVV's own internal structure (the map we're working from)

**The three adhikāras (books) + the vimarśas (reflexive examinations):**
```
Vol 1 (M00020)  jñānādhikāra  — the knowledge-section: the upoddhāta, the self-as-Lord,
                                 the memory, the reflexion core (chunks A-N)
Vol 2 (M00021)  jñānādhikāra  — the caturtho → aṣṭamo vimarśas: memory/aham, the jñānaśakti
                                 (manifestation), the smṛti/apohana, the one-support
                                 (V2-A … V2-S)
Vol 3 (M00022)  kriyādhikāra  — the action-section (V3-A … V3-I, ending the
                                 kāryakāraṇabhāvavimarśa)
                āgamādhikāra  — the teaching-section (V3-J … V3-M: the śivatattva, the padārthavarga)
                tattvādhikāra — the categories-section (V3-N … V3-P: the closing sum, the ||samāptā||)
```

**The nanu→āha skeleton:** the IPVV's whole texture is dialectical — every passage is an objection
(nanu) met by a reply (āha), usually against the Buddhist, the Vaiśeṣika/Kāṇāda, the Advaitin, or
the Sāṃkhya. The argument maps tag the speaker. This is the IPVV's own internal rhythm.

---

## The sessions (the hounds)

| Session | What it mines | Verdict |
|---------|---------------|---------|
| `IPVV-probe-tantraloka-cruxes.md` | the Tantrāloka's tough cruxes vs the IPVV | RESOLVES 4 better (universality via V2C/V3C; memory→identity via V2L; two-levels→threefold satya/saṃvṛtisatya/asatya; recognition-as-foregrounding V1E); deepens karma-freedom (V3B); SAME WALL on felt→ground |
| `IPVV-reflexion-vs-nanavira.md` | the reflexion core (V1M/V2L) vs Ñāṇavīra + the reflexivity debate | GEM: the "I"-grasp is "not a construction" (V2L) — construction is join/split, the "I" is neither; reconciles structural (Ñāṇavīra) with intrinsic (Abhinavagupta) reflexivity |
| `IPVV-buddhist-co-opting.md` | the Buddhist avenue (V2E/F/G) | GEM: Abhinavagupta CO-OPTS the Buddhist's own tools; the dream-inversion (V2G); the debate is over the VALENCE of the same appearances |
| `IPVV-recognition-formulations-vs-mepit.md` | the recognition formulations (V1E/V1D/V3P) vs the σ-flip/mepit | GEM: foregrounding/"I was never not"/lover-union are the σ-flip at three registers; the lover ties it to rasa; the IPVV supports "internally manifested forms, not the filter" |
| `IPVV-felt-to-ground-argument.md` | the deepest crux: felt→ground (V2O/V2P) | CORRECTION: the IPVV DOES argue the ground (V2O the order-less support; V2P memory-requires-the-one); narrows but does not close the gap — the universalization is still the wager |
| `IPVV-MEMORY-vs-whattheheckismemory.md` | the IPVV's memory doctrine vs the modern essay | both locate the hard problem at pastness/mine-ness/reliving; the IPVV answers the essay's open question (the non-constructed "I") |
| `LOGICVID-session-ipvv-v3i-parallels-counters.md` | the IPVV V3-I (kāryakāraṇatāvimarśa) vs the Tantrāloka | PARALLELS: action = the will; the difference is real (pratibimbavāda); COUNTER resolved: real difference = the self's reflection, impurity = the misreading |
| `IPVV-internal-arc-vimarsas.md` | the vimarśa-arc (the powers' necessary order, jñāna→smṛti→apohana→kriyā) | the powers unfold in a NECESSARY order (manifestation→persistence→self-knowledge→self-expression); the apohana is the pivot; the great-Lordship = self-awareness, NOT an added power (V2S); the unity via the DEALING (V2S); the kriyādhikāra runs parallel |
| `IPVV-internal-method-opponents-agama.md` | the nanu→āha opponent-geography + why the āgamādhikāra comes last | the opponents mirror the doctrine (Buddhist=knowledge, Vaiśeṣika=metaphysics, Sāṃkhya=near-rival, grammarian=word, Advaitin=minor); the āgama supplies what reason can't ("perception isn't omniscient; only the āgama measures the whole"); the Śivatattva is "the body of every category"; the IPVV's method = reason + revelation in sequence |

---

## The open internal-structure threads (the next hounds)

- [x] The vimarśa-level structure: how each vimarśa builds on the last (the jñāna→smṛti→apohana→
      kriyā arc) — the IPVV's own internal logic of the powers. → `IPVV-internal-arc-vimarsas.md`
- [x] The nanu→āha speaker-mapping: which opponents appear where (Buddhist, Vaiśeṣika, Advaitin,
      Sāṃkhya) — the IPVV's internal geography of the debate. → `IPVV-internal-method-opponents-agama.md`
- [x] The āgamādhikāra (V3-J→M): why the teaching-section after the argument-sections — the role of
      āgama/scripture in the IPVV's own method. → `IPVV-internal-method-opponents-agama.md`
- [ ] The tattvādhikāra (V3-N→P): the closing sum — how the whole system is gathered. (V3P read; a
      dedicated session pending)
- [ ] The kārikā-verse mapping: how each ĪPK kārikā is expanded by the commentary — the
      IPVV-as-commentary internal structure.
- [ ] The vimarśa internal rhythm: the nanu→āha dialectical texture per vimarśa — how each vimarśa's
      objections are ordered.

---

*This is the pushing-ipvv scaffold. The sessions mine the IPVV's own internal structure (the
vimarśas, the nanu→āha dialectic, the three adhikāras), with our frameworks entering only after the
commentary has spoken. The material (T1 + L2 + argument maps) is all on disk.*
