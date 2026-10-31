"""Project gate registry on the vendored qprivately kernel (tools/qp_acom/).

Each gate is a versioned pure predicate: same inputs ALWAYS give the same
verdict. New logic means a new gate id — never a silent edit (kernel invariant).
Evidence items are plain dicts with a "metric" key (kernel EVIDENCE shape where
practical). Run `python3 tools/qp_gates.py --list` to audit the registry.
"""
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from qp_acom.gates import gate  # noqa: E402  (vendored kernel, single module object)


def _ev(inputs, metric):
    for e in inputs.get("evidence", []):
        if isinstance(e, dict) and e.get("metric") == metric:
            return e.get("value")
    return None


@gate("ipvv/has-source-v1")
def _has_source(inputs):
    f = _ev(inputs, "source_file")
    ln = _ev(inputs, "source_lines")
    ok = bool(f) and ln is not None
    return ok, f"source_file={f} lines={ln}"


@gate("ipvv/has-license-v1")
def _has_license(inputs):
    lic = _ev(inputs, "source_license")
    ok = isinstance(lic, str) and lic.startswith("CC BY-NC")
    return ok, f"source_license={lic}"


@gate("ipvv/has-immutable-id-v1")
def _has_immutable(inputs):
    v = _ev(inputs, "immutable_id")
    ok = isinstance(v, str) and len(v) > 0
    return ok, f"immutable_id={'present' if ok else 'MISSING'}"


@gate("ipvv/gate-consistent-v1")
def _gate_consistent(inputs):
    gate = _ev(inputs, "gate")
    has_en = bool(_ev(inputs, "has_english"))
    if gate == "PASS":
        return has_en, "PASS requires English"
    if gate in ("BLOCKED", "PUBLISHED"):
        return True, f"{gate} (display rule handled downstream)"
    return False, f"unknown gate value: {gate}"


@gate("ipvv/checks-pass-v1")
def _checks_pass(inputs):
    gate = _ev(inputs, "gate")
    if gate == "PUBLISHED":
        return True, "published corpus path (checks predate gate battery)"
    checks = _ev(inputs, "gate_checks") or {}
    if not isinstance(checks, dict) or not checks:
        return False, "no gate.checks evidence"
    bad = [k for k, v in checks.items()
           if not (isinstance(v, (list, tuple)) and v and v[0] is True)]
    return (not bad), ("all checks true" if not bad else f"failing: {bad}")


GATE_IDS = [
    "ipvv/has-source-v1",
    "ipvv/has-license-v1",
    "ipvv/has-immutable-id-v1",
    "ipvv/gate-consistent-v1",
    "ipvv/checks-pass-v1",
]


if __name__ == "__main__":
    import json
    from qp_acom.gates import REGISTRY, program_hash
    print(json.dumps({g: program_hash(g) for g in REGISTRY}, indent=1))
