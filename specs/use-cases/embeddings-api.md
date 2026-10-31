# Embeddings API — versioned, gate-labeled, license-tagged corpus product

## Inputs
- `site/dist/data/corpus.jsonl` — 454 records, stable ids, gate labels.
- `/data/*.json` machine-readable layer (translations, argmaps, C1s, themes evidence, essays).

## Behavior
- Versioned corpus snapshots; gate labels enforced at retrieval (see embeddings-loop).
- Namespaced (per-work, per-kind) for scoped chat.

## Licensing constraint (binding)
- Vendored Sanskrit (GRETIL/Mukhabodha) is CC BY-NC-SA: **non-commercial**.
  License tags must ride the metadata before any commercial API/embeddings play;
  filter or re-license first. Owner essays/probes are ours to license freely.

## Phases
1. Tag every corpus record with license + provenance (small schema addition).
2. Snapshot + publish versions (R2, content-addressed).
