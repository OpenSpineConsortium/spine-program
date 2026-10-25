"""bordercall: measure a corpus of label volumes, then name a vertebral border from shape.

    # 1. measure (writes the wide per-level table). Full spine by default.
    python run.py measure --labels /path/to/labels --out levels.csv
    BORDERCALL_LEVELS=T11,T12,L1,L2,L3,L4,L5 python run.py measure --labels ... --out ...

    # 2. ask whether the shape carries a border
    python run.py border --levels levels.csv --above T12 --below L1
    python run.py border --levels levels.csv --above C7  --below T1

    # 3. check the package against a corpus whose answer is known
    python run.py selftest --levels /path/to/level_gradients.csv

`selftest` is the one to run first on a new machine. It re-derives the two CTSpinoPelvic1K
numbers from the released table and fails loudly if they have moved, which is how you know
the port did not quietly change the model.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from border import Border, Corpus          # noqa: E402

# the released CTSpinoPelvic1K answers, to three decimals; see HANDOFF.md
KNOWN = {"auc_adjacent": 0.988, "auc_whole": 0.998, "junction": 0.951}
TOL = 0.004


def cmd_measure(a) -> int:
    script = os.path.join(HERE, "measure_levels.py")
    cmd = [sys.executable, script, "--labels", a.labels, "--out", a.out]
    if a.jobs:
        cmd += ["--jobs", str(a.jobs)]
    print("running: " + " ".join(cmd))
    return subprocess.call(cmd)


def cmd_border(a) -> int:
    c = Corpus.from_csv(a.levels, case_key=a.case_key)
    print("levels found: %s" % ", ".join(c.levels))
    r = Border(a.above, a.below).evaluate(c, folds=a.folds, seed=a.seed)
    print(r.report())
    return 0


def cmd_selftest(a) -> int:
    c = Corpus.from_csv(a.levels)
    print("levels found: %s" % ", ".join(c.levels))
    r = Border("T12", "L1").evaluate(c)
    print(r.report())
    bad = []
    for key, want, got in (("auc_adjacent", KNOWN["auc_adjacent"], r.auc_adjacent),
                           ("auc_whole", KNOWN["auc_whole"], r.auc_whole),
                           ("junction", KNOWN["junction"], r.junction_accuracy)):
        d = abs(got - want)
        flag = "ok " if d <= TOL else "OFF"
        print("  %s %-13s want %.3f  got %.4f  (%+.4f)" % (flag, key, want, got, got - want))
        if d > TOL:
            bad.append(key)
    if bad:
        print("\nSELFTEST FAILED on %s. The model or the features have changed; do not"
              % ", ".join(bad))
        print("trust results from this copy until the difference is explained.")
        return 1
    print("\nselftest passed: this copy reproduces the published CTSpinoPelvic1K numbers.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("measure", help="label volumes -> wide per-level table")
    m.add_argument("--labels", required=True)
    m.add_argument("--out", required=True)
    m.add_argument("--jobs", type=int, default=0)
    m.set_defaults(fn=cmd_measure)

    b = sub.add_parser("border", help="can the shape name this border?")
    b.add_argument("--levels", required=True)
    b.add_argument("--above", default="T12")
    b.add_argument("--below", default="L1")
    b.add_argument("--folds", type=int, default=5)
    b.add_argument("--seed", type=int, default=0)
    b.add_argument("--case_key", default="case")
    b.set_defaults(fn=cmd_border)

    s = sub.add_parser("selftest", help="reproduce the known CTSpinoPelvic1K answers")
    s.add_argument("--levels", required=True)
    s.set_defaults(fn=cmd_selftest)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
