"""Hardening tests for the qp receipt authority boundary (peer-review P0).

Covers: empty/omitted/unknown gates, swapped/altered evidence, changed
gate code, unsigned/untrusted signer, wrong role, stale input. Run:
  python3 -m unittest tools.qp_acom.test_receipts_hardening -v   (from ipvv/)
or directly: python3 tools/qp_acom/test_receipts_hardening.py
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from qp_acom import gates  # noqa: E402
from qp_acom import objects as O  # noqa: E402
from qp_acom import receipts as R  # noqa: E402


@gates.gate("test/always-pass-v1")
def _always_pass(inputs):
    return True, "test gate passes"


@gates.gate("test/needs-flag-v1")
def _needs_flag(inputs):
    return bool(inputs.get("claim", {}).get("flag")), "needs claim.flag"


def _ev(i=1):
    return [O.make_evidence("source_file", f"f{i}.txt", "path",
                            "2026-11-06", {"chunk": f"c{i}"})]


def _prop(i="t1"):
    return {"id": i, "claim": O.make_claim("s", "d", "UNKNOWN"),
            "target": i}


def _run():
    return O.make_run("task:1", "test", "m")


class HardeningTests(unittest.TestCase):
    def test_empty_gates_fail_closed(self):
        r = R.transition({"s": 0}, _prop(), _ev(), [], _run())
        self.assertFalse(r["passed"])
        self.assertEqual(r["state_after"], {"s": 0})
        self.assertIn("problems", r)
        s = R.settle(r, _ev())
        self.assertFalse(s["ok"])

    def test_unknown_gate_fails_and_pins(self):
        r = R.transition({"s": 0}, _prop(), _ev(), ["nope/missing-v9"],
                         _run(), apply=lambda s, p, e: {"s": 1})
        self.assertFalse(r["passed"])
        self.assertEqual(r["state_after"], {"s": 0})
        self.assertEqual(r["gates"][0]["program_hash"],
                         "unknown:unregistered-gate")

    def test_swapped_evidence_rejected(self):
        r = R.transition({"s": 0}, _prop(), _ev(1), ["test/always-pass-v1"],
                         _run())
        self.assertTrue(r["passed"])
        s = R.settle(r, _ev(2))  # different evidence bytes
        self.assertFalse(s["ok"])
        self.assertIn("evidence mismatch", s["reason"])

    def test_altered_evidence_rejected(self):
        ev = _ev(1)
        r = R.transition({"s": 0}, _prop(), ev, ["test/always-pass-v1"],
                         _run())
        ev2 = [dict(ev[0], value="TAMPERED.txt")]
        s = R.settle(r, ev2)
        self.assertFalse(s["ok"])

    def test_gate_replay_disagreement_rejected(self):
        prop = _prop()
        prop["claim"] = O.make_claim("s", "d", "UNKNOWN")
        prop["claim"]["flag"] = True
        r = R.transition({"s": 0}, prop, _ev(), ["test/needs-flag-v1"],
                         _run())
        self.assertTrue(r["passed"])
        prop2 = dict(prop, claim=dict(prop["claim"], flag=False))
        r2 = dict(r, proposal=prop2)
        s = R.settle(r2, _ev())
        self.assertFalse(s["ok"])

    def test_changed_gate_code_rejected(self):
        r = R.transition({"s": 0}, _prop(), _ev(), ["test/always-pass-v1"],
                         _run())
        self.assertTrue(r["passed"])
        # Simulate a silent gate edit: same id, different predicate source.
        import hashlib
        import inspect
        old = gates.REGISTRY["test/always-pass-v1"]["program_hash"]
        gates.REGISTRY["test/always-pass-v1"]["program_hash"] = (
            "sha256:" + hashlib.sha256(b"edited").hexdigest())
        try:
            a = R.authorize_receipt(r, _ev(), authorized_signers=set())
            self.assertFalse(a["ok"])
            self.assertIn("gate code changed", a["reason"])
        finally:
            gates.REGISTRY["test/always-pass-v1"]["program_hash"] = old
            # sanity: source-derived pin restores
            src = inspect.getsource(
                gates.REGISTRY["test/always-pass-v1"]["fn"])
            self.assertEqual(old, "sha256:" + hashlib.sha256(
                src.encode()).hexdigest())

    def test_unsigned_pass_never_authorizes(self):
        r = R.transition({"s": 0}, _prop(), _ev(), ["test/always-pass-v1"],
                         _run())
        self.assertTrue(r["passed"])
        a = R.authorize_receipt(r, _ev(), authorized_signers={"anyone"})
        self.assertFalse(a["ok"])
        self.assertIn("unsigned", a["reason"])

    def test_wrong_role_rejected(self):
        r = R.transition({"s": 0}, _prop(), _ev(), ["test/always-pass-v1"],
                         _run())
        r = R.sign_receipt(b"0" * 32, r)
        a = R.authorize_receipt(r, _ev(), authorized_signers={"deadbeef"})
        self.assertFalse(a["ok"])
        self.assertIn("not in authorized role set", a["reason"])

    def test_right_role_authorizes(self):
        r = R.transition({"s": 0}, _prop(), _ev(), ["test/always-pass-v1"],
                         _run())
        r = R.sign_receipt(b"0" * 32, r)
        from qp_acom import crypto as C
        _sec, pub = C.keypair(b"0" * 32)
        a = R.authorize_receipt(r, _ev(), authorized_signers={pub.hex()})
        self.assertTrue(a["ok"], a)

    def test_legacy_receipt_stays_readable(self):
        # A 0.1-style body (id-hashed IDs, no digest_full) verifies under
        # its original protocol and never as 0.2 authority.
        from qp_acom.canonical import canonical, sha256_hex
        from qp_acom.canonical import merkle_root
        ev = _ev(1)
        body = {"protocol": "acom/0.1", "transition_type": "RESOLVE",
                "proof_level": 0, "subject": "t1",
                "state_before": {"s": 0}, "proposal": _prop(),
                "evidence_root": merkle_root([e.get("id", "?") for e in ev]),
                "gates": [{"id": "test/always-pass-v1", "result": "PASS",
                           "proof": "x"}],
                "grant": None, "run": _run(), "state_after": {"s": 0},
                "passed": True}
        body["id"] = "receipt:" + sha256_hex(canonical(body))[:16]
        body["signature"] = ""
        v = R.verify_receipt(body)
        self.assertTrue(v["ok"], v)
        a = R.authorize_receipt(body, ev, authorized_signers={"x"})
        self.assertFalse(a["ok"])  # unsigned + no pin + id-root: never authority

    def test_full_digest_binds_content(self):
        r = R.transition({"s": 0}, _prop(), _ev(), ["test/always-pass-v1"],
                         _run())
        self.assertEqual(len(r["digest_full"]), 64)
        r2 = dict(r, state_after={"s": 999})
        v = R.verify_receipt(r2)
        self.assertFalse(v["ok"])


if __name__ == "__main__":
    unittest.main()
