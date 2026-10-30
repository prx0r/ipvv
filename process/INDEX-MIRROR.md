# Pāṭala — Canonical IPVV Stack (mirror)

*2026-08-12. A mirror of the canonical layer-definition docs + specs from the sanskritree mount
(`/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/`) into the patala repo, so the
canonical layer stack is version-controlled and available to skills/agents here. The BULK DATA
(00_source, 01_t1, 02_t1, 03_t2, 05_t3, l0/, l0_v1/, l200 per-chunk files, pilot/) is NOT mirrored —
it lives on the mount. Only DOCS + SPECS + the l0 schema/coverage contracts are here.*

## The canonical layer stack (the authoritative layer definitions)

```
SOURCE
  ↓ L0/L1     token-level / controlled translation
  ↓ L2 READ   "what does the text say?"          (SPEC_L2.md)
  ↓ L200 AUDIT "how was this reading derived?"   (l200/README-L200-SPEC.md — the 8-section audit)
  ↓ C1        "what does this passage mean?"     (sourcetranslationprompt.md / c1/C1-SPEC.md)
  ↓ THEME     "what pattern emerges across passages?"  (SPEC_THEME.md)
  ↓ ESSAY     "what larger argument follows?"    (SPEC_ESSAY.md)
  ↓ EDUCATION "how do we teach it?"              (SPEC_EDUCATION.md)
```

## Key files

| file | what |
|---|---|
| `sourcetranslationprompt.md` | the R2 original source (C1 spec + the whole stack) |
| `c1andmore.md` | the universal stack + the 4 human zoom questions |
| `c1/C1-SPEC.md` | the C1 passage-commentary spec |
| `specs/SPEC_L0_L1.md` · `SPEC_L2.md` · `SPEC_C1` (C1_SPEC.md) · `SPEC_THEME.md` · `SPEC_ESSAY.md` · `SPEC_SOURCE.md` · `SPEC_EDUCATION.md` | the per-layer canonical specs |
| `specs/l0_schema.json` · `l0_coverage.json` | the L0 contract (referenced by `skills/raw-l0` + `patala-translate`) |
| `l200/README-L200-SPEC.md` | the frozen 8-section L200 audit spec |
| `IPVV-KNOWLEDGE-CORE.md` · `HANDOVER-IPVV-LAYERS-2026-08-12.md` | the knowledge core + layer handover |

## Provenance
Source of truth remains the mount (`_stack/ipvv/`). This is a mirror for repo-local availability.
Originals on the mount are never overwritten.
