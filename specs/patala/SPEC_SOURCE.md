# SPEC — SOURCE LAYER (acquisition, registration, witnesses, segmentation)

*The first stage of the repeatable translation factory. Source is the ground truth: every layer
below it peels back to a verifiable witness. Never let normalized Sanskrit replace the historical
source — preserve the chain `NORMALIZED TEXT ↓ derived from ↓ EDITION / SCAN / WITNESS`.*

---

## 1. What "source" means

For every passage we preserve the textual witnesses actually used:

```
IPK / Vṛtti            (the root verses + author's explanation)
IPV                    (Abhinavagupta's shorter Vimarśinī)
IPVV                   (our target)
Torella text           (critical ed. where relevant)
KSTS scans             (historical)
GRETIL machine text    (machine-readable IAST)
other historical editions
```

Each witness file is registered once, then referenced per-passage by `source_id`.

## 2. The source registry

One record per source file:

```text
source_id            stable id (e.g. "gretil-ipk-vrtti-pu", "ksts-vol60-muktabodha")
edition              edition/print it transcribes (e.g. "KSTS vol 60, ed. M.K. Śāstrī")
license              (e.g. "CC BY-NC 4.0 Muktabodha", "CC BY-NC-SA 4.0 GRETIL")
role(s) per passage  witness / context / comparison  (tagged per passage, not globally)
locator_format       how a location is expressed (chapter.verse / adhikāra / page)
scan_or_page_ref     historical scan/page when it exists
```

## 3. The three roles a source can play (per passage)

A source file may serve DIFFERENT passages in DIFFERENT roles:

| Role | Meaning | Example |
|---|---|---|
| **witness** | the text a passage is read against | Muktabodha IPVV for an IPVV passage |
| **context** | a parallel that aids understanding (root/commentary) | GRETIL IPK+Vṛtti beside an IPVV passage |
| **comparison** | an adversarial reading to audit against | Torella/Pandey/Ratié |

This is why a downloaded GRETIL IPK is not "just an input" — it is context for one passage, a
comparison for another, and sometimes a witness itself.

## 4. Canonical passage IDs (freeze first)

**Paragraph/passage is the primary unit; kārikā is the higher structural container** (IPVV
commentary exceeds verse boundaries). Hierarchy:

```
Work
→ Adhikāra / Vimarśa
→ Kārikā
→ canonical paragraph/passage      ← stable IDs attach here, kārikā-linkage preserved
```

```
pt:passage:ipvv:V2-S:14
IPVV 2.x.x §14
```

Stable, citable, versioned. This is the citation backbone of the whole edition.

## 5. Per-passage witness record

```
canonical passage ID
edition/source
exact locator
machine-readable Sanskrit
scan/page reference
variant note if editions differ   (e.g. Torella vs KSTS vs GRETIL)
```

## 6. Rights

Distinguish clearly:
```
our translation / annotations        → ours
quoted Sanskrit edition (base)       → e.g. Muktabodha CC BY-NC 4.0
third-party translations (comparison)→ © (Pandey, Torella) — never copied as authority
manuscript images                    → custodian's
```
Carry the base-license notice and non-commercial framing on every published view.

---

## 7. EXEMPLARS — what it looks like in the IPVV (real files)

### The witness + context + comparison in action

The IPVV is our **witness target**; the root kārikā and IPV are **context/comparison**. The
exemplar chain for the "one light" passage (V3-C, pramāṇavimarśa, kārikā 1–2):

| role | exemplar | what it shows |
|---|---|---|
| **witness (our base)** | `02_t1/chunkV3-C-kriya-trtiyo-k1-2.md` | the hyper-literal T1 with IAST glosses of the passage |
| **structured witness** | `l0/chunkV3-C-kriya-trtiyo-k1-2.l0.jsonl` | the L0 token/gloss records (4111 records) |
| **context (root kārikā + Vṛtti)** | `corpus/ipvv-anchor/primary/gretil_utipk_pu.txt` (IPK 2.3.1–2) | the root kārikā + Vṛtti the IPVV comments on |
| **context (IPV parallel)** | `corpus/ipvv-anchor/primary/gretil_ipv_clean.txt` | the shorter Vimarśinī parallel |
| **comparison (Torella)** | `corpus/ipvv-anchor/primary/torella_ipk.txt` | the critical ed. + EN translation (adversarial) |
| **audit contract** | `l200/V3C-kriya-trtiyo-k1-2.md` | the derivation map binding L2 → L0 → source range |

### The passage-ID scheme in use

The existing published IPVV passage on pāṭala shows the ID + source format:
`data/corpus/passages/isvarapratyabhijnavivrtivimarsini.jsonl`:
```json
{
  "id": "tantra:text:isvarapratyabhijnavivrtivimarsini:1.5.11",
  "work_id": "isvarapratyabhijnavivrtivimarsini",
  "location": { "chapter": 1, "verse": 5 },
  "sanskrit": "prakāśasya vimarśo vā mukhya ātmā",
  "source_edition": "Torella critical ed., IPK 1.5.11 + Vṛtti; IPVV expansion"
}
```

### Acquisition manifest (the registry in practice)

`corpus/ipvv-anchor/primary/ACQUISITION_MANIFEST.md` records every downloaded source, its license,
role, and state — the concrete form of §2–§3.

---

## 8. VALIDATION — how we know the source layer is correct

**Per-passage:**
- [ ] every passage has ≥1 witness with a resolvable `source_id` + locator
- [ ] normalized Sanskrit is present and traceable to a witness (the ↓ derived-from ↓ chain is not
      broken)
- [ ] variant notes exist where editions differ (Torella vs KSTS vs GRETIL)
- [ ] rights are tagged per source; no third-party translation used as an authority

**Factory-wide:**
- [ ] every source file in the registry has a license; no untagged redistribution
- [ ] `ACQUISITION_MANIFEST.md` is current for every acquired source
- [ ] the passage-ID scheme is frozen and no two passages collide
- [ ] zero text loss: every source span maps to ≥1 passage, and every passage resolves to ≥1 source
      span (the M0 ingestion validation)

## 9. Factory inputs already acquired (IPVV)

| source | role | location |
|---|---|---|
| GRETIL IPK + Vṛtti (plain) | context / comparison / witness | `corpus/ipvv-anchor/primary/gretil_utipk_pu.txt` |
| GRETIL IPK + Vṛtti (pāda) | context / comparison | `corpus/ipvv-anchor/primary/gretil_utipk_au.txt` |
| GRETIL IPV (Vimarśinī) | context / comparison | `corpus/ipvv-anchor/primary/gretil_ipv_clean.txt` |
| KSTS IPVV (Muktabodha M00020-22) | witness (our base) | `sources/muktabodha-lib/...` |
| Torella IPK (ed. + EN) | comparison | `corpus/ipvv-anchor/primary/torella_ipk.txt` |
| 1921 IPV scan | historical citation | `corpus/ipvv-anchor/primary/archive-1921-ipv/` |
| Pandey Bhāskarī III (EN IPV) | comparison only | `corpus/abhinava/ipv/bhaskari3_pandey_english_ipv.pdf` |

See `corpus/ipvv-anchor/primary/ACQUISITION_MANIFEST.md` for full details.
