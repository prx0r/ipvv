# Translation workbench — human-in-loop, witnesses, variations

## Inputs
- T1/L1/L2/argmap per chunk (R2 + `site/data/translations/*.json` + patala published).
- Witnesses: Dyczkowski/Torella/Singh (compare only — commercial, never host).
- Gate battery (`tools/verify_site.py` + pipeline QA gates).

## Behavior
- Side-by-side: T1 + L1 + L2 + argmap + witness diffs per chunk.
- Accept/reject per chunk → writes `accepted_by` (name + date). Accept is the key
  that unlocks public English display (publish grant).
- Variations: `en_variants[]` per chunk (pipeline re-runs, editor revisions);
  reader picks variant, diff view between variants.
- Custom translations: user edits any layer → saved to profile → run through the
  same gate battery → user-viewable, optionally submitted. **Needs the accounts
  backend (Worker + D1) — this workbench is where profiles live.**

## Phases
1. Read-only bench (witness diffs + gate badges) — static, now.
2. Accept/reject (needs auth + write API).
3. Variants display + custom translations (needs accounts backend).
