"""Where the classifier puts the thoracolumbar junction, against where the labels put it.

    python junction_vs_labels.py

WHAT "TRUE T12/L1 DISC SPACE" MEANS HERE, AND WHAT IT CANNOT MEAN. The release carries no
measured T12/L1 disc height: `degenerative.csv` and `level_atlas.csv` both start at L1L2,
and `transition_morphometrics.csv`'s `disc_above_mm` / `disc_low_mm` are the lumbosacral
pair. The true junction is therefore the LABELLED one, the interspace between the vertebra
a reader named T12 and the one named L1. Every number below is against that, not against a
measured disc.

THE SCORES ARE OUT OF FOLD, folds grouped by case, so no vertebra is scored by a model that
saw its patient. The features and the model are imported from
test_morphometric_separability.py, so this and the article's separation share one definition.

WHAT A DISAGREEMENT IS, AND IS NOT. The classifier is trained on these same labels, so it
cannot find an anomaly the labels do not already encode. A disagreement means only this: the
vertebra's SHAPE is atypical for the name it carries. That is worth looking at, and it is not
independent evidence that the name is wrong.
"""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plot_thoracolumbar_violins import (DATA, LEVELS, build_with_levels,
                                        out_of_fold_scores)
from test_morphometric_separability import THORACIC


LUMBAR_COUNT = {"L4": 4, "L5": 5, "L6": 6}


def anomaly_flags():
    """Per case, the flags the release records, split by which border they sit at."""
    out = {}
    path = os.path.join(DATA, "transition_morphometrics.csv")
    for r in csv.DictReader(open(path)):
        t = (r.get("lstv_label") or "").strip().lower()
        g = (r.get("castellvi_type") or "").strip()
        out[r["case"]] = {
            # thoracolumbar border
            "lumbar_rib": (r.get("has_lumbar_rib") or "0") not in ("0", "", "False"),
            # lumbosacral border
            "l6": (r.get("has_l6") or "0") not in ("0", "", "False"),
            "lstv": t not in ("", "normal"),
            "castellvi": g not in ("", "None"),
            # how many vertebrae the labels put between the junction and the sacrum
            "n_lumbar": LUMBAR_COUNT.get((r.get("lowest_lumbar") or "").strip()),
            "lowest_rib_bearing": (r.get("lowest_rib_bearing") or "").strip(),
        }
    return out


def main() -> int:
    X, y, groups, lv = build_with_levels(os.path.join(DATA, "level_gradients.csv"))
    s = out_of_fold_scores(X, y, groups)
    pred_thor = s >= 0.5

    per_case = defaultdict(dict)
    for g, l, p in zip(groups, lv, pred_thor):
        per_case[g][l] = bool(p)

    flags = anomaly_flags()
    order = {l: i for i, l in enumerate(LEVELS)}

    offsets, nonmono, usable = Counter(), [], []
    for case, d in per_case.items():
        present = sorted(d, key=lambda l: order[l])
        if "T12" not in present or "L1" not in present:
            continue                      # the junction is not in the field of view
        usable.append(case)
        seq = [d[l] for l in present]
        n_pred = sum(seq)
        # a clean call is a run of thoracic at the top and nothing below it
        if seq[:n_pred] != [True] * n_pred or any(seq[n_pred:]):
            nonmono.append(case)
            continue
        n_true = sum(1 for l in present if l in THORACIC)
        offsets[n_pred - n_true] += 1

    print("CASES")
    print("  scored                                  %4d" % len(per_case))
    print("  with both T12 and L1 in the field       %4d" % len(usable))
    print("  predictions not a clean top-down run    %4d" % len(nonmono))
    agree = offsets.get(0, 0)
    decided = sum(offsets.values())
    print("\nWHERE THE PREDICTED JUNCTION FALLS, against the labelled T12/L1 interspace")
    print("  (of the %d cases with a clean call)" % decided)
    for off in sorted(offsets):
        tag = {0: "at the labelled T12/L1 disc"}.get(
            off, "%+d level%s %s" % (off, "" if abs(off) == 1 else "s",
                                     "caudal" if off > 0 else "cranial"))
        print("  %+d  %4d  %5.1f%%   %s" % (off, offsets[off],
                                            100.0 * offsets[off] / decided, tag))
    print("\n  agreement with the labelled junction: %d/%d = %.1f%%"
          % (agree, decided, 100.0 * agree / decided))

    # per-vertebra, at the two levels that define the junction
    print("\nPER-VERTEBRA at the boundary (out of fold)")
    for l in ("T11", "T12", "L1", "L2"):
        m = lv == l
        if not m.any():
            continue
        want = l in THORACIC
        print("  %-4s n=%4d   called thoracic %5.1f%%   (label says %s)"
              % (l, int(m.sum()), 100.0 * pred_thor[m].mean(),
                 "thoracic" if want else "lumbar"))

    # does disagreement concentrate in the records the release flags?
    print("\nDISAGREEMENT AGAINST THE RELEASE'S OWN FLAGS")
    print("  a case 'disagrees' if its predicted junction is not the labelled one,")
    print("  or its predictions are not a clean top-down run.")
    bad = set(nonmono) | {c for c in usable
                          if c not in nonmono and _offset(per_case[c], order) != 0}
    rows = [("lumbar rib (thoracolumbar border)", "lumbar_rib"),
            ("L6", "l6"), ("LSTV label", "lstv"), ("Castellvi grade", "castellvi")]
    print("\n  %-36s %7s %9s %9s" % ("flag", "cases", "disagree", "rate"))
    for name, key in rows:
        sel = [c for c in usable if flags.get(c, {}).get(key)]
        n = len(sel)
        k = sum(1 for c in sel if c in bad)
        print("  %-36s %7d %9d %8s" % (name, n, k,
                                       ("%.1f%%" % (100.0 * k / n)) if n else "--"))
    none_sel = [c for c in usable
                if not any(flags.get(c, {}).get(k) for _, k in rows)]
    k = sum(1 for c in none_sel if c in bad)
    print("  %-36s %7d %9d %8s" % ("no flag of any kind", len(none_sel), k,
                                   "%.1f%%" % (100.0 * k / len(none_sel))))
    print("\n  disagreeing cases in total: %d of %d (%.1f%%)"
          % (len(bad), len(usable), 100.0 * len(bad) / len(usable)))
    flagged_bad = sum(1 for c in bad if any(flags.get(c, {}).get(k) for _, k in rows))
    print("  of those, carrying any flag:  %d (%.1f%%)"
          % (flagged_bad, 100.0 * flagged_bad / len(bad) if bad else 0.0))

    # DIRECTION, because a rate alone would not distinguish the tidy reading (a ribbed L1
    # looks thoracic, so the thoracic block runs one level caudal) from noise either way.
    print("\nDIRECTION of the offset, per flag")
    print("  %-24s %6s  %s" % ("flag", "cases", "offsets"))
    for name, key in rows + [("no flag of any kind", None)]:
        sel = [c for c in usable if (flags.get(c, {}).get(key) if key
                                     else not any(flags.get(c, {}).values()))]
        off = Counter()
        for c in sel:
            off["ragged" if c in nonmono else _offset(per_case[c], order)] += 1
        pretty = ", ".join("%s:%d" % (k, v) for k, v in sorted(off.items(), key=str))
        print("  %-24s %6d  %s" % (name, len(sel), pretty))

    # ---- COUNT DOWN TO THE SACRUM -----------------------------------------------------
    # The second test, and the one that needs no name at the border: how many vertebrae lie
    # between the predicted junction and the sacrum. A column with the usual count has five.
    # The labels give the count below the LABELLED junction; the model's offset moves the
    # junction, so the count below the PREDICTED one is that minus the offset.
    print("\nCOUNT FROM THE PREDICTED JUNCTION DOWN TO THE SACRUM")
    print("  five is the usual count; anything else is an anomalous column.")
    tab = Counter()
    for c in usable:
        n = flags.get(c, {}).get("n_lumbar")
        if n is None or c in nonmono:
            continue
        off = _offset(per_case[c], order)
        tab[(n, n - off)] += 1
    print("\n  %-18s %-20s %6s" % ("labels say", "predicted junction", "cases"))
    for (n_lab, n_pred), k in sorted(tab.items()):
        mark = "" if n_pred == 5 else "   <- flagged anomalous by count"
        print("  %-18s %-20s %6d%s" % ("%d to the sacrum" % n_lab,
                                       "%d to the sacrum" % n_pred, k, mark))
    pred_anom = sum(k for (n_l, n_p), k in tab.items() if n_p != 5)
    lab_anom = sum(k for (n_l, n_p), k in tab.items() if n_l != 5)
    both = sum(k for (n_l, n_p), k in tab.items() if n_p != 5 and n_l != 5)
    tot = sum(tab.values())
    print("\n  anomalous by the labels' count    %3d / %d" % (lab_anom, tot))
    print("  anomalous by the predicted count  %3d / %d" % (pred_anom, tot))
    print("  both                              %3d" % both)
    print("  the predicted count adds %d record(s) the labels' count alone does not call"
          % (pred_anom - both))

    # ---- THE CLASSES EITHER SIDE OF THE PREDICTED POINT -------------------------------
    print("\nTHE TWO VERTEBRAE EITHER SIDE OF THE PREDICTED JUNCTION")
    side = Counter()
    for c in usable:
        if c in nonmono:
            continue
        d = per_case[c]
        present = sorted(d, key=lambda l: order[l])
        n = sum(d[l] for l in present)
        above = present[n - 1] if n >= 1 else None
        below = present[n] if n < len(present) else None
        side[(above, below)] += 1
    for (a_, b_), k in side.most_common():
        ok = "  <- T12 / L1 as expected" if (a_, b_) == ("T12", "L1") else ""
        print("  above %-5s below %-5s %5d%s" % (a_, b_, k, ok))

    # ---- AGAINST THE RIBS, WHICH ARE NOT A COUNT AND NOT A NAME ----------------------
    # The lowest rib-bearing vertebra is a morphological fact the classifier never sees:
    # its features are body and canal measures, no rib among them. If the disagreements
    # are anomalous spines rather than noise, they should sit where the rib says the
    # border vertebra carries the opposite phenotype, AND in the matching direction.
    print("\nTHE OFFSET AGAINST THE LOWEST RIB-BEARING VERTEBRA")
    tab = Counter()
    for c in usable:
        off = "ragged" if c in nonmono else _offset(per_case[c], order)
        tab[(off, flags.get(c, {}).get("lowest_rib_bearing"))] += 1
    print("  %-8s %-24s %6s" % ("offset", "lowest rib-bearing", "cases"))
    for (off, rb), k in sorted(tab.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        note = ""
        if off == -1 and rb == "T11":
            note = "   T12 bears no rib: it looks lumbar"
        if off == 1 and rb == "L1":
            note = "   L1 bears a rib: it looks thoracic"
        print("  %-8s %-24s %6d%s" % (off, rb, k, note))
    anom = [c for c in usable
            if flags.get(c, {}).get("lowest_rib_bearing") not in ("T12", "", None)]
    hit = [c for c in anom if c in bad]
    norm = [c for c in usable if flags.get(c, {}).get("lowest_rib_bearing") == "T12"]
    fp = [c for c in norm if c in bad]
    print("\n  rib-anomalous at this border (lowest rib-bearing is not T12): %d" % len(anom))
    print("    the classifier disagrees on %d of them        sensitivity %.1f%%"
          % (len(hit), 100.0 * len(hit) / len(anom) if anom else 0))
    print("  rib-normal (lowest rib-bearing is T12): %d" % len(norm))
    print("    the classifier disagrees on %d of them        specificity %.1f%%"
          % (len(fp), 100.0 * (1 - len(fp) / len(norm)) if norm else 0))
    print("    of all %d disagreements, %d are rib-anomalous  precision %.1f%%"
          % (len(bad), len(hit), 100.0 * len(hit) / len(bad) if bad else 0))

    rib = sorted(c for c in usable if flags.get(c, {}).get("lumbar_rib"))
    sc = {(g, l): v for g, l, v in zip(groups, lv, s)}
    print("\n  the lumbar-rib cases, P(thoracic) by level:")
    for c in rib:
        print("    %s  T12 %.2f  L1 %.2f  L2 %.2f  %s"
              % (c, sc.get((c, "T12"), float("nan")), sc.get((c, "L1"), float("nan")),
                 sc.get((c, "L2"), float("nan")),
                 "<- L1 called thoracic" if per_case[c].get("L1") else ""))
    return 0


def _offset(d, order):
    present = sorted(d, key=lambda l: order[l])
    return sum(d[l] for l in present) - sum(1 for l in present if l in THORACIC)


if __name__ == "__main__":
    sys.exit(main())
