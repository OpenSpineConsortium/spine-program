#!/usr/bin/env bash
# The required check "check" (.github/workflows/ci.yml runs this script), and the same run on a
# laptop. It holds what this repository's own code does: the claim protocol's copy under
# tools/sdlc_protocol to its record tools/VENDORED, and to the library's own files where
# SDLC_PROTOCOL names a clone of OpenSpineConsortium/symphony-protocol, as CI names one; every
# Python file of tools/, scripts/ and tests/ parses; the tests under tests/; and, on a pull
# request, the claim protocol (tools/check_protocol.py) and the review record
# (tools/review_record.py, CONTRIBUTING.md). Outside a pull request event the last two pass.
#
# The numbered folders' code is salvaged from the repositories MANIFEST_CODE.md names and is
# kept as the record, unrefactored: its tests need the grid, its data and libraries this
# repository does not install, so they run where that code lives, not here.
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
step() { echo "== $1"; }

step "the claim protocol's copy against tools/VENDORED"
PYTHONPATH=tools python3 -m sdlc_protocol verify-vendored tools || fail=1

if [ -n "${SDLC_PROTOCOL:-}" ]; then
  step "the copy against the library's own files at the recorded commit"
  commit=$(awk 'NR == 1 { print $3 }' tools/VENDORED)
  if ! git -C "$SDLC_PROTOCOL" cat-file -e "$commit^{commit}" 2>/dev/null; then
    echo "FAIL: $SDLC_PROTOCOL has no commit $commit"; fail=1
  else
    while read -r sum path; do
      theirs=$(git -C "$SDLC_PROTOCOL" show "$commit:sdlc_protocol/$path" | sha256sum | cut -d' ' -f1)
      [ "$theirs" = "$sum" ] || { echo "FAIL: tools/sdlc_protocol/$path is not the library's at $commit"; fail=1; }
    done < <(tail -n +2 tools/VENDORED)
  fi
fi

step "every Python file of tools/, scripts/ and tests/ parses"
python3 - <<'PY' || fail=1
import ast, pathlib, sys
bad = 0
for path in sorted(p for d in ("tools", "scripts", "tests") for p in pathlib.Path(d).rglob("*.py")):
    try:
        ast.parse(path.read_text(encoding="utf-8"), str(path))
    except SyntaxError as error:
        print(f"FAIL: {error}")
        bad = 1
sys.exit(bad)
PY

step "the tests"
python3 -m unittest discover -s tests -p "test_*.py" || fail=1

step "the claim protocol (a claude/<issue> pull request)"
python3 tools/check_protocol.py || fail=1

step "the review record (a pull request marked ready)"
python3 tools/review_record.py || fail=1

if [ "$fail" = 0 ]; then echo "check: passed"; else echo "check: FAILED"; fi
exit "$fail"
