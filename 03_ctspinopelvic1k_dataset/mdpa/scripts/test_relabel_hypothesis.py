"""Are the failures mislabelled? Three label sets, the same classifier, honest and circular.

    python test_relabel_hypothesis.py

THE QUESTION. No scan here contains C2, so the border vertebra's name is a reader's call,
not a count. If the reader is wrong where the shape disagrees, then "failures" are the
reader's, not the model's, and relabelling should fit the data better.

THE TRAP, AND WHY THIS SCRIPT HAS THREE ARMS. Relabel every disagreement to the model's own
call and the AUC rises by construction: the target has been moved to where the model already
points. That is not evidence of anything, and it would be the headline if it were run alone.
It is run here anyway, last, as the control that shows what a circular "improvement" looks
like, so the honest arm can be read against it.

  reader   the released labels, as a radiologist-sourced annotation named them
  rib      the border taken from the LOWEST RIB-BEARING VERTEBRA: that vertebra and
           everything above it is thoracic, everything below is lumbar. The classifier's
           features are end-plate width, two body heights, canal width and
           transverse-process span, each over the case's own median, plus ratios. No rib
           among them. So this arm moves the target using evidence the model cannot see,
           which is what makes it a test rather than a restatement.
  model    every disagreement flipped to the model's call. CIRCULAR. The control.

Each arm RETRAINS from scratch and is scored out of fold with folds grouped by case, so no
arm is scored by a model that saw its patient.
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anomaly_classes import PRETTY, classify
from junction_vs_labels import anomaly_flags
from plot_thoracolumbar_violins import DATA, LEVELS, build_with_levels, out_of_fold_scores
from test_morphometric_separability import THORACIC, auc

ADJACENT = ("T12", "L1")          # the pair the article reports and the border in question


def rib_labels(y, groups, lv, flags):
    """Thoracic iff the vertebra is at or above the lowest RIB-BEARING vertebra."""
    out = y.copy()
    order = {l: i for i, l in enumerate(LEVELS)}
    moved = Counter()
    for i, (g, l) in enumerate(zip(groups, lv)):
        rb = flags.get(g, {}).get("lowest_rib_bearing")
        if rb not in order:
            continue                      # no rib read: leave the reader's call alone
        new = 1 if order[l] <= order[rb] else 0
        if new != out[i]:
            moved[(l, rb)] += 1
        out[i] = new
    return out, moved


def report(name, y, X, groups, lv, note=""):
    s = out_of_fold_scores(X, y, groups)
    a_all = auc(y, s)
    m = np.isin(lv, ADJACENT)
    a_adj = auc(y[m], s[m])
    print("  %-8s whole span AUC %.4f   T12/L1 pair AUC %.4f  (n=%d)  %s"
          % (name, a_all, a_adj, int(m.sum()), note))
    return s, a_all, a_adj


def main() -> int:
    flags = anomaly_flags()
    X, y, groups, lv = build_with_levels(os.path.join(DATA, "level_gradients.csv"))
    print("%d vertebrae, %d cases\n" % (len(y), len(np.unique(groups))))

    print("ARM 1  reader labels, as released")
    s0, a0, p0 = report("reader", y, X, groups, lv)

    print("\nARM 2  rib labels  (independent of every feature the model uses)")
    y_rib, moved = rib_labels(y, groups, lv, flags)
    n_moved = int((y_rib != y).sum())
    print("  moved %d vertebrae of %d (%.2f%%):" % (n_moved, len(y), 100.0 * n_moved / len(y)))
    for (l, rb), k in sorted(moved.items()):
        wastho = "thoracic -> lumbar" if l not in THORACIC else "lumbar -> thoracic"
        d = "%s becomes %s" % (l, "thoracic" if rb != "T11" else "lumbar")
        print("     %-4s (lowest rib-bearing %s)  n=%-3d  %s" % (l, rb, k, d))
    s1, a1, p1 = report("rib", y_rib, X, groups, lv)

    print("\nARM 3  model labels  -- CIRCULAR CONTROL, not evidence")
    y_mod = (s0 >= 0.5).astype(int)
    print("  moved %d vertebrae to the model's own call" % int((y_mod != y).sum()))
    s2, a2, p2 = report("model", y_mod, X, groups, lv, "<- expected to be highest; it is circular")

    print("\nREAD IT LIKE THIS")
    print("  reader -> rib   whole span %+.4f   T12/L1 %+.4f" % (a1 - a0, p1 - p0))
    print("  reader -> model whole span %+.4f   T12/L1 %+.4f   (circular, for scale)"
          % (a2 - a0, p2 - p0))
    if a1 - a0 > 0:
        print("\n  The shape fits the rib-defined border better than the reader's name.")
        print("  The rib is not among the features, so this is evidence and not a restatement;")
        print("  compare the size of the move against the circular arm before calling it large.")
    else:
        print("\n  The shape does NOT fit the rib-defined border better. The failures are not")
        print("  explained by the reader having misnamed the border vertebra.")

    # which cases the two label sets disagree on, by phenotype
    cls = classify(flags)
    per = defaultdict(lambda: [0, 0])
    for i, g in enumerate(groups):
        if y_rib[i] != y[i]:
            per[cls.get(g, "typical")][0] += 1
        per[cls.get(g, "typical")][1] += 1
    print("\n  vertebrae the rib arm moved, by phenotype")
    for k, (a_, b_) in sorted(per.items(), key=lambda x: -x[1][0]):
        if a_:
            print("    %-30s %3d moved of %4d vertebrae" % (PRETTY.get(k, k), a_, b_))

    print("\n  WHAT THIS STILL CANNOT SETTLE. The rib says which vertebra carries a rib. It")
    print("  does not say whether that is a thirteenth thoracic vertebra above five lumbar")
    print("  ones or a rudimentary rib on a true L1, which are different columns with the")
    print("  same rib. Only a count from C2 separates those, and no scan here has C2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
