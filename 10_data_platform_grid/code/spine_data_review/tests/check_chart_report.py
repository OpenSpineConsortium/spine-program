"""Compare a sdr.chart validation report on tests/fixtures/chart_screen with tests/expected_chart_errors.json.

For each fixture: an empty expectation means the record must validate with zero errors; otherwise
every expected substring must appear in at least one error message. The 'probe-ccby3' fixture is
reported as INFO (it documents what the licence table forces for a CC BY 3.0 text).

Usage: ~/sdr_venv/bin/python tests/check_chart_report.py --report tests/_out/chart_report.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="tests/_out/chart_report.json")
    a = ap.parse_args()
    rep = json.loads((ROOT / a.report).read_text(encoding="utf-8"))
    exp = json.loads((HERE / "expected_chart_errors.json").read_text(encoding="utf-8"))
    fails = 0
    for name, want in sorted(exp.items()):
        d = rep["datasets"].get(name)
        if d is None:
            print(f"FAIL {name}: not in report"); fails += 1; continue
        errs = d["errors"]
        if name.startswith("probe-"):
            print(f"INFO {name}: errors={errs} warnings={d['warnings']}")
            continue
        if not want:
            ok = not errs
            print(f"{'PASS' if ok else 'FAIL'} {name}: expected valid; errors={errs} warnings={d['warnings']}")
        else:
            missing = [w for w in want if not any(w in e for e in errs)]
            ok = not missing
            print(f"{'PASS' if ok else 'FAIL'} {name}: expected {want}; got {errs}" + (f"; missing {missing}" if missing else ""))
        fails += not ok
    print(f"n_files={rep['n_files']} n_valid={rep['n_valid']} n_invalid={rep['n_invalid']} keywords_seen={rep['schema_keywords_seen']}")
    print(f"expected_not_charted={rep['expected_not_charted']}\ncharted_without_alias_row={rep['charted_without_alias_row']}")
    print(f"\n{'ALL CHART CHECKS PASS' if not fails else f'{fails} CHART CHECK(S) FAILED'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
