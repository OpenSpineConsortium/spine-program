"""The anomaly classes of this corpus, and how the shape-based junction does on each.

    python anomaly_classes.py

Importable: `classify()` gives {case: class name}, so the breakout, the Benzel plot and the
render gallery all name their groups from one definition rather than three.

THE CLASSES ARE THE PHENOTYPES THE SCHEME CAN EXPRESS, not a severity scale. Each case takes
ONE class, most specific first, so the groups are disjoint and a bar chart of them adds up:

  lumbar_rib       a rib on a lumbar body: the lowest rib-bearing vertebra is L1 (ids 60/61)
  no_rib_T12       T12 bears no rib, so the lowest rib-bearing vertebra is T11
  six_lumbar       a sixth lumbar-type vertebra (id 25)
  four_lumbar      only four lumbar identifiers; the fifth is delineated with the sacrum
  castellvi        a two-reader Castellvi grade with the usual count and ribs
  typical          none of the above

A case can carry more than one phenotype -- a lumbar rib AND an L6 -- so the order matters
and is stated rather than left to the reader. The thoracolumbar classes come first because
this is a thoracolumbar classifier; a lumbosacral grade on a column with a normal
thoracolumbar border tells it nothing.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from junction_vs_labels import _offset, anomaly_flags
from plot_thoracolumbar_violins import DATA, LEVELS, build_with_levels, out_of_fold_scores

ORDER = ["lumbar_rib", "no_rib_T12", "six_lumbar", "four_lumbar", "castellvi", "typical"]
PRETTY = {"lumbar_rib": "Rib on a lumbar body (L1)",
          "no_rib_T12": "No rib on T12",
          "six_lumbar": "Six lumbar vertebrae (L6)",
          "four_lumbar": "Four lumbar identifiers",
          "castellvi": "Castellvi grade, usual count",
          "typical": "Typical column"}


def classify(flags=None):
    flags = flags or anomaly_flags()
    out = {}
    for case, f in flags.items():
        rb, n = f.get("lowest_rib_bearing"), f.get("n_lumbar")
        if rb == "L1":
            out[case] = "lumbar_rib"
        elif rb == "T11":
            out[case] = "no_rib_T12"
        elif f.get("l6") or n == 6:
            out[case] = "six_lumbar"
        elif n == 4:
            out[case] = "four_lumbar"
        elif f.get("castellvi") or f.get("lstv"):
            out[case] = "castellvi"
        else:
            out[case] = "typical"
    return out


def main() -> int:
    flags = anomaly_flags()
    cls = classify(flags)
    X, y, groups, lv = build_with_levels(os.path.join(DATA, "level_gradients.csv"))
    s = out_of_fold_scores(X, y, groups)
    per_case = defaultdict(dict)
    for g, l, p in zip(groups, lv, s >= 0.5):
        per_case[g][l] = bool(p)
    order = {l: i for i, l in enumerate(LEVELS)}

    print("ANOMALY CLASSES over the whole corpus")
    whole = Counter(cls.values())
    for k in ORDER:
        print("  %-30s %4d" % (PRETTY[k], whole[k]))
    print("  %-30s %4d" % ("total", sum(whole.values())))

    usable = [c for c, d in per_case.items() if "T12" in d and "L1" in d]
    print("\nHOW THE SHAPE-BASED JUNCTION DOES ON EACH")
    print("  'correct' = the predicted junction is the labelled T12/L1 interspace,")
    print("  i.e. the vertebra above it is T12 and the one below is L1.\n")
    print("  %-30s %6s %8s %9s" % ("class", "cases", "correct", "accuracy"))
    rows = []
    for k in ORDER:
        sel = [c for c in usable if cls.get(c) == k]
        if not sel:
            continue
        ok = 0
        for c in sel:
            d = per_case[c]
            present = sorted(d, key=lambda l: order[l])
            seq = [d[l] for l in present]
            n = sum(seq)
            if seq[:n] == [True] * n and not any(seq[n:]) and _offset(d, order) == 0:
                ok += 1
        acc = 100.0 * ok / len(sel)
        rows.append((k, len(sel), ok, acc))
        print("  %-30s %6d %8d %8.1f%%" % (PRETTY[k], len(sel), ok, acc))
    tot_n = sum(r[1] for r in rows)
    tot_ok = sum(r[2] for r in rows)
    print("  %-30s %6d %8d %8.1f%%" % ("ALL", tot_n, tot_ok, 100.0 * tot_ok / tot_n))

    print("\n  the two thoracolumbar classes are where it fails; the lumbosacral ones")
    print("  sit near the typical column, which is what a thoracolumbar classifier should do.")

    # exemplars for the render gallery: the most ordinary member of each class, by the
    # median of its own class on the measure that defines the border
    print("\nEXEMPLARS for the render gallery (most ordinary member of each class)")
    vals = {}
    for r in csv.DictReader(open(os.path.join(DATA, "level_gradients.csv"))):
        try:
            vals[r["case"]] = float(r["endplate_width_L1_mm"])
        except (TypeError, ValueError):
            pass
    picks = {}
    for k in ORDER:
        sel = sorted(c for c in usable if cls.get(c) == k and c in vals)
        if not sel:
            continue
        med = float(np.median([vals[c] for c in sel]))
        picks[k] = min(sel, key=lambda c: abs(vals[c] - med))
        print("  %-30s %s" % (PRETTY[k], picks[k]))
    print("\n  --cases '" + ";".join("%s:%s" % (picks[k], PRETTY[k])
                                     for k in ORDER if k in picks) + "'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
