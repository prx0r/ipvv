# qprivately verification — what was adopted, how to check it

Kernel vendored at `tools/qp_acom/` (upstream: prx0r/qprivately, protocol `acom/0.1`).
Project gates in `tools/qp_gates.py`. Check registry any time:
`python3 tools/qp_gates.py --list` (content hashes — new logic MUST mint a new gate id).

## What's live
- **Gates** (`ipvv/*-v1`): has-source, has-license, has-immutable-id, gate-consistent
  (PASS⇒English, BLOCKED⇒no English), checks-pass (R2 gate.checks all true;
  PUBLISHED corpus path exempt with reason recorded).
- **Receipts** (`site/dist/data/receipts.jsonl`, 463): every chunk via kernel
  `transition()` — claim + evidence + per-gate verdicts + evidence merkle root.
  FAIL receipts are first-class (every BLOCKED chunk records what did not pass).
  Byte-deterministic across rebuilds (verified by hash).
- **Verify** (`tools/verify_site.py` §6b): gate program-hashes pinned (registry rot
  fails the commit); every receipt id recomputed from canonical bytes (tamper fails
  the commit); receipts count == translations + published passages.

## Recomputing one receipt by hand
1. Take the receipt's `proposal` + rebuild the evidence list in
   `build_receipts.chunk_receipt` order (metrics: source_file, source_lines,
   source_license, immutable_id, gate, has_english, gate_checks, model).
2. Evidence ids are content-derived (`ev:<12>`); `evidence_root` is their merkle root.
3. Receipt id = `receipt:` + first 16 hex of canonical-JSON sha256 over the body
   minus `id`/`signature`/`signer`.

## Explicitly NOT yet
- **Signatures/grants.** Receipts carry empty `signature` (kernel never forges).
  Display authorization still flows through the build's PASS/human-review logic;
  cryptographic grants (`accepted_by` as signed grant) are the next step and need
  key management above the kernel.
- **ATASK tasks / RUN ledger.** Task objects and run receipts (model/cost) are the
  follow-up (model-quota enforcement).
