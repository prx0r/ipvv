# Argument extraction process — from translated text to truth-packet

## The pipeline (per work, per chunk)

```
Sanskrit root (vendored, licensed)
  → T1/L0/L1/L2 (translated, gated, receipts)
    → Argmap (explicit argument: question, premises, inference, conclusion, unresolved)
      → Pushing (implicit commitments, tensions, deepest "why")
        → ArgumentTruthPacket (formalized, citable, strength-graded)
          → Essay (narration that resolves to Sanskrit at every sentence)
```

## Step 1: Argmap extraction

For works WITH argmaps (IPVV): parse the argmap markdown into:
  - title (from first ## header)
  - question (from **The question:**)
  - issue (from ## 1. What is at issue)
  - premises (bolded sub-headers in ## 2. The argument)
  - inference (the typed move)
  - conclusion (from the argument)
  - unresolved (from ## 3. Unresolved)

For works WITHOUT argmaps (stotras, tantraloka, tantrasara): derive from L2 text:
  - question = the chunk's central claim (extracted from L2 SUMMARY or first paragraph)
  - premises = the argument's supporting points (extracted from L2 EXPLANATION)
  - conclusion = the chunk's thesis (extracted from L2 FUNCTION or SUMMARY)
  - unresolved = any BOUNDARY/OPEN notes

## Step 2: Pushing (hounding)

For each chunk, ask:
  - What does the text assume but not say?
  - Where does it pull two ways?
  - What is the deepest "why"?
Seed tensions from existing pushing files where they map to chunks.

## Step 3: Formalize (ArgumentTruthPacket)

```json
{
  "id": "pt:argument:<work>:<chunk>",
  "work_id": "<work>",
  "passage_id": "<immutable_id>",
  "title": "<from argmap or L2>",
  "kind": "reductio|analogy|identity|entailment|decomposition",
  "question": "<central question>",
  "issue": "<what is at issue>",
  "premises": [{"text": "...", "label": "...", "passage_id": "..."}],
  "inference": "<typed move>",
  "conclusion": {"text": "...", "passage_id": "..."},
  "unresolved": "<open questions>",
  "argument_text": "<full argmap or L2>",
  "tension_id": "<pushing file stem or null>",
  "strength": "MACHINE_DRAFT",
  "status": "MACHINE_DRAFT",
  "source_passage": "<immutable_id>",
  "sanskrit": "<vendored root text>"
}
```

## Step 4: Strength grading (derived, not hand-waved)

- PROVED: formal proof exists (Lean/truth engine)
- REVIEWED: human review accepted reconstruction + provenance
- WELL_SUPPORTED: premises resolve, inference sound, no surviving prosecution
- PLAUSIBLE: coherent reconstruction with a live objection
- SPECULATIVE: a probe — explicitly NOT asserted as the text's claim
- MACHINE_DRAFT: extracted by machine, not yet reviewed (current state for all)

## Step 5: qprivately compliance

Each packet gets a receipt via transition():
  - claim: "{work}:{chunk} displays its entitled state"
  - evidence: source_file, source_lines, license, immutable_id, gate, has_english, gate_checks, model
  - gates: has-source, has-license, has-immutable-id, gate-consistent, checks-pass
  - FAIL receipts are first-class (BLOCKED chunks record what did not pass)

## Step 6: Embedding readiness

Each packet is a record in corpus.jsonl with:
  - stable id, work, kind, passage_id
  - sa (Sanskrit), en (English, gate-filtered), en_gate
  - license, source_file, source_lines
  - immutable_id, checks
  - tension_id, strength, status (new fields)

## Rules that don't bend
- Every packet resolves downward: conclusion → premises → passage_id → Sanskrit
- BLOCKED chunks get no English in any field (sa only)
- Strength is DERIVED, never hand-waved
- MACHINE_DRAFT until human review promotes it
- No silent gate edits (new id or it didn't happen)
