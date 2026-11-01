#!/usr/bin/env bash
# verify.sh — gates before any commit.
set -u
cd "$(dirname "$0")/.."
fail=0
echo "== T1 frozen check (no edits to samples/T1* expected in feature branches) =="
echo "== L0 tool present =="
python3 tools/t1_extract.py --help >/dev/null 2>&1 || { echo "FAIL t1_extract"; fail=1; }
echo "== chunker present =="
python3 tools/chunker.py --help >/dev/null 2>&1 || { echo "FAIL chunker"; fail=1; }
echo "== no 145MB in git =="
if find . -path ./.git -prune -o -type f -size +20M -print | grep -q .; then echo "FAIL large file staged"; find . -type f -size +20M; fail=1; fi
echo "== C1 length (samples) =="
python3 -c "from pathlib import Path; [print(p, len(Path(p).read_text().split())) for p in Path('samples').glob('*') if p.is_file()]" 2>&1 | head -n 20
echo "== specs present =="
for f in specs/CANONICAL-DAG.yaml specs/C1_SPEC.md specs/SPEC_L2.md specs/schema/person.json; do [ -f "$f" ] || { echo "FAIL missing $f"; fail=1; }; done
echo "== people validate (masters + scholars vs person schema) =="
python3 tools/validate_people.py 2>&1 | tail -n 3 || fail=1
echo "== site gates (site/data + dist, fail-closed; pipeline paths warn-only) =="
python3 tools/verify_site.py || fail=1
[ "$fail" -eq 0 ] && echo "ALL PASS" || echo "GATES FAILED"
exit "$fail"
