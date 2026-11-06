"""TransitionReceipt: the ONE canonical output (northstar §3).

Everything meaningful emits the same artifact: canonical JSON, hashed,
signed (signature field carried; key management lives above the kernel).
`transition()` is the ONLY path from proposal to canonical state:

    S[t+1] = T(S[t], P)  iff  ALL gates PASS  (northstar §1)

No gate pass, no transition. No prose anywhere in the artifact
(invariant 8). Receipts carry proof_level V0..V12 (northstar §5);
authority maps capability -> minimum level.

Protocol versions (in-toto/SLSA-style versioned envelope; old receipts
stay readable under their original protocol, never silently
reinterpreted):
  acom/0.1 — legacy: truncated 16-hex id over body, evidence_root over
    evidence IDs, signature (if any) over the truncated id, unsigned
    receipts verify integrity-only.
  acom/0.2 — hardened: same legacy `id` (display/compat) PLUS
    `digest_full` (64-hex sha256 over the full body); evidence_root over
    canonical evidence BYTES; per-gate `program_hash` pinned at execution;
    signature binds the full digest; empty/unknown gate sets FAIL closed.

Layering (Sigstore analogy: signature check ≠ policy check):
  verify_receipt() = INTEGRITY only (id/digest recompute; signature
    valid IF present). An unsigned receipt can verify — that never
    authorizes anything.
  authorize_receipt() = AUTHORITY boundary (required gate set from
    trusted versioned policy, program_hash pins, authorized signer role,
    evidence-root match, replay store). Publishing routes must call this.
  settle() = integrity + gate replay + evidence-root comparison, with
    optional authority checks. FAIL-closed on every mismatch.
"""

from . import gates
from .canonical import PROTOCOL, canonical, sha256_hex

PROTOCOL_V2 = "acom/0.2"
LEGACY_PROTOCOLS = ("acom/0.1",)

# Fields introduced in 0.2. The digest is computed over the body WITHOUT
# itself (a hash cannot include itself); id/signature/signer are also
# outside the hashed body. Stripped when verifying legacy receipts so a
# 0.1 body is never reinterpreted as 0.2 (and vice versa).
_V2_FIELDS = ("digest_full",)
_HASH_SKIP = ("id", "signature", "signer", "digest_full")

# Transition types that MUST NOT run with an empty gate set even when no
# policy is configured. `all([]) is True` used to pass these; now FAIL.
# A configured POLICY (below) overrides per type with a required set.
_NONEMPTY_TYPES = frozenset({
    "RESOLVE", "CHUNK-DISPLAY", "ARGUMENT-DISPLAY",
})

# Trusted versioned mandatory-gate policy: transition_type -> required
# gate ids. Resolved from HERE (never caller choice) when set. Empty
# default = caller supplies gates, but they must still be non-empty and
# all known. Publishing routes SHOULD configure this (set_policy) and
# verifiers MUST check it via authorize_receipt().
POLICY = {}


def set_policy(policy: dict) -> None:
    """Configure the mandatory-gate policy (authority layer only)."""
    POLICY.clear()
    POLICY.update(policy)


def required_gates(transition_type: str) -> list:
    return list(POLICY.get(transition_type, []))


def _gate_record(gate_id: str, inputs: dict) -> dict:
    """Execute one gate and pin its exact predicate version (SLSA
    provenance analog: the receipt binds WHAT ran, not just its name)."""
    r = gates.execute(gate_id, inputs)
    try:
        r["program_hash"] = gates.program_hash(gate_id)
    except KeyError:
        r["program_hash"] = "unknown:unregistered-gate"
    return r


def transition(state_before: dict, proposal: dict, evidence: list,
               gate_ids: list, run: dict, proof_level: int = 0,
               transition_type: str = "RESOLVE",
               apply=None) -> dict:
    """Evaluate gates; on all-PASS compute post-state via apply().

    apply(state_before, proposal, evidence) -> state_after dict.
    Returns the receipt in ALL cases (FAIL receipts are first-class:
    they record exactly what did not pass).

    Fail-closed rules (new in 0.2, REQUIRED even without a policy):
      - empty/omitted gate list on a non-empty type -> FAIL, no apply.
      - unknown gate id -> that gate FAILs (kernel registry already does
        this) AND the receipt records program_hash unknown.
      - policy-required gates missing from gate_ids -> FAIL, no apply.
    """
    assert 0 <= proof_level <= 12
    gate_ids = list(gate_ids or [])
    inputs = {"claim": proposal.get("claim", proposal),
              "evidence": evidence}
    problems = []
    if not gate_ids and transition_type in _NONEMPTY_TYPES:
        problems.append("empty gate set: no ungated transitions")
    required = required_gates(transition_type)
    missing = [g for g in required if g not in gate_ids]
    if missing:
        problems.append(f"policy-required gates missing: {missing}")
    results = [_gate_record(g, inputs) for g in gate_ids]
    unknown = [r["id"] for r in results
               if r.get("program_hash") == "unknown:unregistered-gate"]
    if unknown:
        problems.append(f"unknown gate ids: {unknown}")
    passed = (not problems
              and bool(results)
              and all(r["result"] == "PASS" for r in results))
    if problems:
        passed = False
    state_after = (apply(state_before, proposal, evidence)
                   if (passed and apply) else dict(state_before))
    receipt = {
        "protocol": PROTOCOL_V2,
        "transition_type": transition_type,
        "proof_level": proof_level,
        "subject": proposal.get("id", proposal.get("target", "?")),
        "state_before": state_before,
        "proposal": proposal,
        "evidence_root": _root_of(evidence),
        "gates": results,
        "grant": proposal.get("grant"),
        "run": run,
        "state_after": state_after,
        "passed": passed,
    }
    if problems:
        receipt["problems"] = problems
    receipt["digest_full"] = sha256_hex(_hash_body(receipt))
    receipt["id"] = "receipt:" + receipt["digest_full"][:16]
    receipt["signature"] = ""  # authority layer signs; kernel never forges
    return receipt


def _root_of(evidence: list) -> str:
    """Merkle root over canonical evidence BYTES (0.2). The old 0.1 root
    hashed evidence IDs; that let swapped content with stable IDs pass."""
    from .canonical import merkle_root
    return merkle_root([sha256_hex(canonical(e)) for e in evidence])


def _root_of_legacy(evidence: list) -> str:
    from .canonical import merkle_root
    return merkle_root([e.get("id", "?") for e in evidence])


def _body_for(receipt: dict) -> dict:
    """Hash-excluded envelope for LEGACY (0.1) receipts only. 0.2 uses
    _hash_body (which additionally excludes digest_full itself)."""
    return {k: v for k, v in receipt.items()
            if k not in ("id", "signature", "signer")}


def _hash_body(receipt: dict) -> bytes:
    return canonical({k: v for k, v in receipt.items()
                      if k not in _HASH_SKIP})


def _want_id(receipt: dict) -> str:
    proto = receipt.get("protocol", PROTOCOL)
    if proto == PROTOCOL_V2:
        return "receipt:" + (receipt.get("digest_full") or "")[:16]
    return "receipt:" + sha256_hex(canonical(_body_for(receipt)))[:16]


def sign_receipt(secret: bytes, receipt: dict) -> dict:
    """Authority signs the FULL digest (0.2) or legacy id (0.1).
    `signer` (pubkey hex) rides OUTSIDE the hashed body: the digest
    commits to content, the signature commits the signer to the digest.
    Kernel never calls this itself."""
    from . import crypto as _crypto
    out = dict(receipt)
    _sec, pub = _crypto.keypair(secret)
    out["signer"] = pub.hex()
    if out.get("protocol") == PROTOCOL_V2:
        target = out.get("digest_full") or _want_id(out)
    else:
        target = out["id"]
    out["signature"] = _crypto.sign_id(secret, target)
    return out


def _sig_target(receipt: dict) -> str:
    if receipt.get("protocol") == PROTOCOL_V2:
        return receipt.get("digest_full") or ""
    return receipt.get("id") or ""


def verify_receipt(receipt: dict) -> dict:
    """INTEGRITY only: recompute id/digest + check signature IF present.

    An unsigned receipt CAN verify here — that is a statement about
    bytes, never an authorization. Publishing routes must call
    authorize_receipt() (or settle with authorized_signers) instead.
    """
    proto = receipt.get("protocol", PROTOCOL)
    if proto not in (PROTOCOL_V2, PROTOCOL) + LEGACY_PROTOCOLS:
        return {"ok": False, "reason": "protocol mismatch"}
    if _want_id(receipt) != receipt.get("id"):
        return {"ok": False, "reason": "receipt id mismatch (tampered?)"}
    if proto == PROTOCOL_V2:
        if sha256_hex(_hash_body(receipt)) != receipt.get("digest_full"):
            return {"ok": False, "reason": "full digest mismatch (tampered?)"}
    if receipt.get("signer"):
        from . import crypto as _crypto
        if not _crypto.verify_id(receipt["signer"], _sig_target(receipt),
                                 receipt.get("signature", "")):
            return {"ok": False, "reason": "bad receipt signature"}
        return {"ok": True, "reason": "id recomputes; signature valid; "
                "re-run gates to settle PASS (integrity only, not authority)"}
    return {"ok": True, "reason": "id recomputes; UNSIGNED — integrity only, "
            "not authority; re-run gates to settle PASS"}


def authorize_receipt(receipt: dict, evidence: list,
                      authorized_signers: set,
                      required: list = None) -> dict:
    """AUTHORITY boundary for publishing routes. ALL must hold:
      1. integrity verifies;
      2. receipt passed AND gates non-empty;
      3. required gate set (explicit arg, else POLICY for the receipt's
         transition_type) is a subset of executed gates;
      4. every executed gate's program_hash matches the CURRENT registry
         (changed gate code -> FAIL; mint a new gate id, never silent edit);
      5. evidence_root recomputed from SUPPLIED canonical evidence bytes
         equals the receipt's root (swapped/altered evidence -> FAIL);
      6. signer present, signature valid, signer in authorized_signers
         (role check inputs; signature alone never proves role).
    Replay prevention is the authority layer's seen-id store duty: do not
    settle the same receipt id twice for state-changing transitions.
    """
    v = verify_receipt(receipt)
    if not v["ok"]:
        return v
    if not receipt.get("passed"):
        return {"ok": False, "reason": "receipt did not pass; nothing to authorize"}
    exec_gates = receipt.get("gates", [])
    if not exec_gates:
        return {"ok": False, "reason": "empty gate set: no ungated transitions"}
    req = list(required) if required is not None else required_gates(
        receipt.get("transition_type", ""))
    executed = [g.get("id") for g in exec_gates]
    missing = [g for g in req if g not in executed]
    if missing:
        return {"ok": False, "reason": f"required gates not executed: {missing}"}
    for g in exec_gates:
        try:
            current = gates.program_hash(g.get("id"))
        except KeyError:
            return {"ok": False, "reason": f"unknown gate at verify time: {g.get('id')}"}
        if g.get("program_hash") and g["program_hash"] != current:
            return {"ok": False, "reason": f"gate code changed since receipt: "
                    f"{g.get('id')} (mint a new gate id)"}
    if _root_of(evidence) != receipt.get("evidence_root"):
        # Legacy receipts hashed IDs: try the legacy root before failing,
        # so old receipts stay readable under their original protocol.
        if not (receipt.get("protocol") in LEGACY_PROTOCOLS
                and _root_of_legacy(evidence) == receipt.get("evidence_root")):
            return {"ok": False, "reason": "evidence mismatch: supplied "
                    "evidence does not reproduce evidence_root (swapped/altered?)"}
    signer = receipt.get("signer", "")
    if not signer:
        return {"ok": False, "reason": "unsigned receipt: no authority"}
    from . import crypto as _crypto
    if not _crypto.verify_id(signer, _sig_target(receipt),
                             receipt.get("signature", "")):
        return {"ok": False, "reason": "bad receipt signature"}
    if signer not in set(authorized_signers or ()):
        return {"ok": False, "reason": "signer not in authorized role set"}
    return {"ok": True, "reason": "authorized: gates, pins, evidence, role all hold"}


def settle(receipt: dict, evidence: list, authorized_signers: set = None) -> dict:
    """Full independent settlement: integrity + evidence-root match +
    every gate re-executed with identical result + program_hash recheck.
    With authorized_signers given, also enforces the authority boundary.
    FAIL-closed on every mismatch; empty gate sets never settle PASS."""
    v = verify_receipt(receipt)
    if not v["ok"]:
        return v
    exec_gates = receipt.get("gates", [])
    if not exec_gates:
        return {"ok": False, "reason": "empty gate set: no ungated transitions"}
    if _root_of(evidence) != receipt.get("evidence_root"):
        if not (receipt.get("protocol") in LEGACY_PROTOCOLS
                and _root_of_legacy(evidence) == receipt.get("evidence_root")):
            return {"ok": False, "reason": "evidence mismatch: supplied "
                    "evidence does not reproduce evidence_root (swapped/altered?)"}
    inputs = {"claim": receipt["proposal"].get("claim", receipt["proposal"]),
              "evidence": evidence}
    for g in exec_gates:
        r = gates.execute(g["id"], inputs)
        if r["result"] != g["result"]:
            return {"ok": False,
                    "reason": f"gate {g['id']} disagrees on replay"}
        try:
            current = gates.program_hash(g["id"])
        except KeyError:
            return {"ok": False, "reason": f"unknown gate at settle time: {g['id']}"}
        if g.get("program_hash") and g["program_hash"] != current:
            return {"ok": False, "reason": f"gate code changed since receipt: "
                    f"{g['id']} (mint a new gate id)"}
    if authorized_signers is not None:
        a = authorize_receipt(receipt, evidence, authorized_signers)
        if not a["ok"]:
            return a
    passed = all(g["result"] == "PASS" for g in exec_gates)
    return {"ok": passed, "reason": "all gates replay identically"
            + ("; authority holds" if authorized_signers is not None and passed else "")}
