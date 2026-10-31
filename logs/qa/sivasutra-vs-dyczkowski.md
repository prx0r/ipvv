# Sivasutra: ours vs Dyczkowski — translation comparison

Date: 2026-10-31. Witness: Dyczkowski, *Aphorisms of Siva* (SUNY; Sivasutras + Bhaskara Varttika + Lakshmanjoo Mahasivaratri lecture transcript, 1992). Commercial — comparison only, excerpts ≤25 words, nothing hosted.

## What each side holds

| | Ours (pipeline, `works/sivasutra`) | Dyczkowski |
|---|---|---|
| Sanskrit | GRETIL Kaul Shastri 1925 (sutras + Varttika), 75 sutras / 8 passages | Same KSTS base + Bhaskara; plus Ksemaraja citations |
| English | T1 segmentation + ledger (no hyperliteral glosses yet); L200/C1 heads; gates 0 PASS / 8 BLOCKED | Full translation + exposition (three voices: root, Bhaskara, Lakshmanjoo lecture) |
| Ksemaraja | Mukhabodha Vimarsini held, untranslated | Cited comparatively (e.g. couples 1.x knowledge with 1.2's conditioned knowledge) |

So this is not two finished translations side by side — it is our *staging* against his *finished book*. The comparison below is therefore asymmetric by design: it checks our direction of travel, not our arrival.

## Agreements (direction correct)

- **1.1** Both: consciousness = self ("Consciousness is the Self" = caitanya=consciousness, atman=self). Dyczkowski adds the Upanishadic resonance (atma eva brahma) and the "inserted is" honesty note — a practice ours should copy in L1 (mark supplied copula).
- **1.2** Both: "Knowledge is bondage." His gloss specifies the mechanism: knowledge "based on the notions 'I' and 'mine', clothed in speech, perception of relative distinctions, rooted in Mayic impurity." Our C1 head says only "knowledge = bondage." Gap, not error: the L2/C1 development step must import exactly this specification.
- **1.4** Both: "The ground of knowledge is Matrka."
- **1.7–1.10** Both: waking = (sensory) knowledge, dream = thought-constructs, deep sleep = non-discrimination/Maya. Match.
- **2.1** Both: "mind = mantra" ("The mind is Mantra").

## Flags (real work items, not failures)

1. **1.3 yonivargaḥ kalāśarīram — genuine crux.** Ours (literal): "womb-class is kala-body." Lakshmanjoo/Dyczkowski lecture: "The group of sources constitutes the body of obscuring energies." *Yoni* spans womb/source/matrix/Mothers/energies; Bhaskara reads the Mothers (Mahesvari etc.) presiding over phoneme classes. Our gloss picks one English ("womb-class"); the lecture picks another ("sources"/energies that obscure). Neither is wrong; the L200 for this sutra must record both and tie the choice to Bhaskara-vs-Ksemaraja. Added to open cruxes.
2. **1.5 udyamo bhairavaḥ — nuance.** Ours: "arising = Bhairava." Lecture: "Bhairava is upsurge." "Upsurge/eruption" carries force that "arising" flattens. Recommend ledger upgrade: udyama = upsurge/eruption (arising kept as gloss-note).
3. **Missing witness file.** WORK.md cites "Dyczkowski + Lakshmanjoo (tier-A)" but Lakshmanjoo's voice survives *inside* Dyczkowski's book (the 1992 lecture transcript), not as a held file. No separate Lakshmanjoo source was ingested. Action: record the lecture transcript (pp. cited) as the Lakshmanjoo witness with location, or downgrade the citation to "via Dyczkowski."
4. **Commentary-layer discipline.** Dyczkowski keeps three voices visibly distinct (root / Bhaskara / Lakshmanjoo oral + Ksemaraja cited comparatively, e.g. his note that one reading "is purely Ksemaraja's suggestion"). Our T1 currently merges root + varttika text in one GRETIL file. When L1 is drafted, source-layer tags (ROOT vs VARTTIKA vs VIMARSINI) must be assigned per token — the file boundary will not do it for us.

## Verdict

Direction of travel confirmed: where both sides have rendered the same sutra, they agree (5/5 sampled, modulo flags 1–2). No ship-blockers beyond what the pipeline gate already enforces (T1 still raw, L0 unparsed → correctly BLOCKED). Flags 1–4 are the exact L200/AQ entries to write when the gate work begins. Do not display full-translation copy for Sivasutra until then; heads + ledger may display as staging (they already do, honestly labeled).
