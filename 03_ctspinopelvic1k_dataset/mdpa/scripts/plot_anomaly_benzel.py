"""Benzel-style morphometry by level, broken out by anomaly class.

    python plot_anomaly_benzel.py                    # end-plate width
    python plot_anomaly_benzel.py --measure canal_w

THE CONVENTION, kept deliberately: vertebral body class on the y axis, cranial at the top,
the measurement on the x axis. That is how the textbook plates read, and it is the axis order
the violin figure beside this one uses, so the two can be shown in sequence without the
audience re-learning the plot.

ONE PANEL PER ANOMALY CLASS. The typical column is drawn behind every panel in grey, the same
distribution each time, so a class is read against it rather than against the panel before it.
Each anomalous case is a point, because there are ten to eighteen of them: a violin over n=14
draws a smooth curve through almost nothing and would imply a density the data cannot support.

Panjabi's cadaveric interval is drawn where his tables reach, mean +/- 1.96 SD, the SD
recovered as sem*sqrt(12). It is a POPULATION interval, which is what makes its width
comparable with the spread of a cohort; his confidence interval would be 3.5x narrower and
would make every cohort look aberrant for an arithmetic reason.

The accuracy printed on each panel is the shape-based junction's, from anomaly_classes.py:
the share of that class whose predicted junction is the labelled T12/L1 interspace.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anomaly_classes import ORDER, PRETTY, classify
from junction_vs_labels import _offset, anomaly_flags
from plot_thoracolumbar_violins import (DATA, LEVELS, MEASURES, PANJABI_N, REF_K,
                                        WITHHOLD_L5, build_with_levels,
                                        out_of_fold_scores, read_panjabi)

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(HERE), "talk_figures")


def per_case_values(column):
    """{case: {level: value}} for one measure."""
    out = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(DATA, "level_gradients.csv"))):
        for l in LEVELS:
            try:
                v = float(r[column.format(l)])
            except (TypeError, ValueError, KeyError):
                continue
            if v > 0:
                out[r["case"]][l] = v
    return out


def junction_accuracy():
    """{class: (n, correct)} on the cases where the junction is in the field of view."""
    flags = anomaly_flags()
    cls = classify(flags)
    X, y, groups, lv = build_with_levels(os.path.join(DATA, "level_gradients.csv"))
    s = out_of_fold_scores(X, y, groups)
    per_case = defaultdict(dict)
    for g, l, p in zip(groups, lv, s >= 0.5):
        per_case[g][l] = bool(p)
    order = {l: i for i, l in enumerate(LEVELS)}
    acc = defaultdict(lambda: [0, 0])
    for c, d in per_case.items():
        if "T12" not in d or "L1" not in d:
            continue
        present = sorted(d, key=lambda l: order[l])
        seq = [d[l] for l in present]
        n = sum(seq)
        ok = (seq[:n] == [True] * n and not any(seq[n:]) and _offset(d, order) == 0)
        a = acc[cls.get(c, "typical")]
        a[0] += 1
        a[1] += int(ok)
    return {k: tuple(v) for k, v in acc.items()}, cls


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", default="endplate", choices=sorted(MEASURES))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                         "font.size": 9})

    column, xlabel = MEASURES[a.measure]
    vals = per_case_values(column)
    refs = read_panjabi(a.measure)
    acc, cls = junction_accuracy()
    withheld = a.measure in WITHHOLD_L5
    levels = [l for l in LEVELS if not (withheld and l == "L5")]
    ys = list(range(len(levels), 0, -1))

    groups = [k for k in ORDER if k != "typical"]
    typical = [c for c, k in cls.items() if k == "typical"]
    base = {l: np.array([vals[c][l] for c in typical if l in vals.get(c, {})], float)
            for l in levels}

    fig, axes = plt.subplots(1, len(groups), figsize=(3.05 * len(groups), 4.9),
                             sharex=True, sharey=True, constrained_layout=True)
    lo = min(np.percentile(v, 0.5) for v in base.values() if len(v))
    hi = max(np.percentile(v, 99.5) for v in base.values() if len(v))
    pad = 0.08 * (hi - lo)

    for ax, key in zip(np.atleast_1d(axes), groups):
        # the typical column, behind everything, identical in every panel
        keep = [(base[l], p) for l, p in zip(levels, ys) if len(base[l]) > 1]
        parts = ax.violinplot([v for v, _ in keep], positions=[p for _, p in keep],
                              vert=False, widths=0.85, showextrema=False,
                              showmedians=True)
        for b in parts["bodies"]:
            b.set_facecolor("0.72")
            b.set_alpha(0.55)
            b.set_edgecolor("none")
        parts["cmedians"].set_color("0.35")
        parts["cmedians"].set_linewidth(1.0)

        # Panjabi, where his tables reach
        for l, p in zip(levels, ys):
            if l in refs and len(base[l]):
                m, sd = refs[l]
                ax.plot([m - REF_K * sd, m + REF_K * sd], [p + 0.40] * 2,
                        color="#b2182b", linewidth=1.6, solid_capstyle="butt", zorder=5)

        # this class, one point per case
        sel = [c for c, k in cls.items() if k == key]
        for l, p in zip(levels, ys):
            v = [vals[c][l] for c in sel if l in vals.get(c, {})]
            if not v:
                continue
            jit = (np.random.default_rng(7).random(len(v)) - 0.5) * 0.30
            ax.scatter(v, np.full(len(v), p) + jit, s=15, color="#1f4e79",
                       edgecolor="white", linewidth=0.4, zorder=7)

        n, ok = acc.get(key, (0, 0))
        rate = ("%.0f%%" % (100.0 * ok / n)) if n else "--"
        ax.set_title("%s\n$n$=%d   junction correct %s" % (PRETTY[key], len(sel), rate),
                     fontsize=9, pad=6)
        ax.set_yticks(ys)
        ax.set_yticklabels(levels)
        ax.set_ylim(0.4, len(levels) + 0.75)
        ax.set_xlim(lo - pad, hi + pad)
        ax.set_xlabel(xlabel)
        ax.grid(True, color="0.88", linewidth=0.5)
        ax.set_axisbelow(True)

    # OUTSIDE the panels: inside, the legend sat on the L4 row of the first class and hid
    # the very points the panel exists to show. "outside lower center" reserves the strip,
    # so the note below cannot collide with the x-axis labels either.
    handles = [
        Patch(facecolor="0.72", alpha=0.55, label="typical column, $n$=%d" % len(typical)),
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#1f4e79",
               markeredgecolor="white", markersize=6, label="this class, one per case"),
        Line2D([0], [0], color="#b2182b", linewidth=1.6,
               label="Panjabi 1992, mean $\\pm$ 1.96 SD ($n$=12)")]
    if withheld:
        handles.append(Line2D([0], [0], color="none",
                              label="L5 withheld: transverse processes fall in front "
                                    "of the body cut"))
    fig.legend(handles=handles, loc="outside lower center", ncol=len(handles),
               fontsize=7.5, frameon=False)

    os.makedirs(OUTDIR, exist_ok=True)
    out = a.out or os.path.join(OUTDIR, "anomaly_benzel_%s.png" % a.measure)
    fig.savefig(out, dpi=200)
    print("wrote " + out)
    for k in groups:
        n, ok = acc.get(k, (0, 0))
        print("  %-30s cases %3d   junction correct %d/%d"
              % (PRETTY[k], sum(1 for c, v in cls.items() if v == k), ok, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
