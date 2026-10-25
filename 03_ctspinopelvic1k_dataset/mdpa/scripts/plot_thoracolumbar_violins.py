"""The thoracolumbar transition as violins by ground-truth vertebral class.

    python plot_thoracolumbar_violins.py                      # endplate width
    python plot_thoracolumbar_violins.py --measure canal_w
    python plot_thoracolumbar_violins.py --measure h_post --out /tmp/fig.png

Left panel: one violin per ground-truth level, cranial at the top, drawn from the 802
records in `data/level_gradients.csv`. Panjabi's cadaveric population interval is drawn
behind each level that his tables cover.

Right panel: the same vertebrae scored by the article's T11/T12-vs-lumbar classifier, as
the probability that a vertebra is THORACIC. That is the transition shown as the model
sees it, and where the violins cross 0.5 is the transition point.

TWO THINGS THIS SCRIPT REFUSES TO DO SILENTLY.

The scores are OUT OF FOLD. Every vertebra is scored by a model that never saw that
patient, folds grouped by case, because two vertebrae from one patient are not independent
and a within-sample score would put the transition exactly where the labels already are.
The features and the model are imported from test_morphometric_separability.py rather than
restated, so the picture and the article's reported separation come from one definition.

L5 IS WITHHELD for end-plate and pedicle width. Both are measured on a body isolated by
cutting at the anterior wall of the canal, and at L5 the transverse processes arise in
front of that wall, so the cut keeps them: the L5 median runs about 2 mm wide with an SD
1.58x the levels above. Plotting it would show a spurious widening at the bottom of the
lumbar spine. The level is dropped for those two measures and the panel says so.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_morphometric_separability import BASE, LUMBAR, THORACIC, auc, fit_logreg, num

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # mdpa/, which stands in for the repo root
DATA = os.path.join(ROOT, "morphometrics")
OUTDIR = os.path.join(ROOT, "talk_figures")       # not the article's figures/
LEVELS = list(THORACIC) + list(LUMBAR)          # T11, T12, L1 ... L5, cranial first

# the column in level_gradients.csv that holds each measure, and Panjabi's name for it
MEASURES = {
    "endplate": ("endplate_width_{}_mm", "End-plate width (mm)"),
    "h_ant":    ("body_height_{}_mm", "Anterior body height (mm)"),
    "h_post":   ("body_height_post_{}_mm", "Posterior body height (mm)"),
    "canal_w":  ("canal_width_{}_mm", "Canal width (mm)"),
    "tp_span":  ("tp_span_{}_mm", "Transverse-process span (mm)"),
}
# measures whose L5 value is contaminated by the transverse processes (see the docstring)
WITHHOLD_L5 = {"endplate", "pedicle"}
PANJABI_N = 12          # specimens behind every mean in the 1992 table
REF_K = 1.96            # population interval, mean +/- 1.96 SD, as the article draws it


def read_panjabi(measure):
    """Panjabi's mean and recovered population SD per level, or {} if he has no such row.

    The table reports the STANDARD ERROR, so the SD is sem*sqrt(12). Drawing the SEM band
    instead would be 3.5x too narrow and would make this cohort look aberrant for a reason
    that is arithmetic rather than anatomy.
    """
    path = os.path.join(DATA, "panjabi_reference.csv")
    out = {}
    with open(path) as fh:
        rows = csv.DictReader([l for l in fh if not l.startswith("#")])
        for r in rows:
            if r["measure"] != measure:
                continue
            try:
                mean, sem = float(r["mean"]), float(r["sem"])
            except (TypeError, ValueError):
                continue
            out[r["level"]] = (mean, sem * math.sqrt(PANJABI_N))
    return out


def read_values(column):
    """{level: array of the measure over all records that have it}."""
    path = os.path.join(DATA, "level_gradients.csv")
    vals = {l: [] for l in LEVELS}
    for r in csv.DictReader(open(path)):
        for l in LEVELS:
            v = num(r, column.format(l))
            if v is not None and v > 0:
                vals[l].append(v)
    return {l: np.asarray(v, float) for l, v in vals.items()}


def build_with_levels(path):
    """The separability features, keeping each row's level so it can be plotted.

    Mirrors build() in test_morphometric_separability.py, which drops the level.
    """
    X, y, groups, lv = [], [], [], []
    for r in csv.DictReader(open(path)):
        med = {}
        for b in BASE:
            v = [num(r, b.format(l)) for l in LEVELS]
            v = [x for x in v if x is not None and x > 0]
            if len(v) >= 3:
                med[b] = float(np.median(v))
        if len(med) < len(BASE):
            continue
        for l in LEVELS:
            vals = {b: num(r, b.format(l)) for b in BASE}
            if any(v is None or v <= 0 for v in vals.values()):
                continue
            f = [vals[b] / med[b] for b in BASE]
            ew, bh = vals["endplate_width_{}_mm"], vals["body_height_{}_mm"]
            bhp, cw, tp = (vals["body_height_post_{}_mm"], vals["canal_width_{}_mm"],
                           vals["tp_span_{}_mm"])
            f += [tp / ew, cw / ew, bh / ew, bh / bhp, tp / bh, cw / bh]
            X.append(f)
            y.append(1 if l in THORACIC else 0)
            groups.append(r["case"])
            lv.append(l)
    return (np.asarray(X, float), np.asarray(y, int),
            np.asarray(groups), np.asarray(lv))


def out_of_fold_scores(X, y, groups, folds=5, seed=0):
    """P(thoracic) for every vertebra, from a model that never saw its patient."""
    cases = np.unique(groups)
    rng = np.random.default_rng(seed)
    rng.shuffle(cases)
    assign = {c: i % folds for i, c in enumerate(cases)}
    fold = np.array([assign[g] for g in groups])
    s = np.zeros(len(y))
    for k in range(folds):
        tr, te = fold != k, fold == k
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd[sd == 0] = 1.0
        w = fit_logreg((X[tr] - mu) / sd, y[tr])
        A = np.hstack([(X[te] - mu) / sd, np.ones((te.sum(), 1))])
        s[te] = 1.0 / (1.0 + np.exp(-A @ w))
    return s


def violins(ax, data, color, xlabel, title):
    """Horizontal violins, one row per level, cranial at the top."""
    ys = list(range(len(LEVELS), 0, -1))          # T11 highest on the page
    series = [data.get(l, np.array([])) for l in LEVELS]
    keep = [(v, p) for v, p in zip(series, ys) if len(v) > 1]
    if keep:
        parts = ax.violinplot([v for v, _ in keep], positions=[p for _, p in keep],
                              vert=False, widths=0.82, showextrema=False,
                              showmedians=True)
        for b in parts["bodies"]:
            b.set_facecolor(color)
            b.set_alpha(0.75)
            b.set_edgecolor("black")
            b.set_linewidth(0.6)
        parts["cmedians"].set_color("black")
        parts["cmedians"].set_linewidth(1.3)
    ax.set_yticks(ys)
    ax.set_yticklabels(LEVELS)
    ax.set_ylim(0.4, len(LEVELS) + 0.6)
    ax.set_xlabel(xlabel)
    ax.set_title(title, pad=8)
    ax.grid(True, color="0.85", linewidth=0.6)
    ax.set_axisbelow(True)
    return ys


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--measure", default="endplate", choices=sorted(MEASURES),
                    help="which per-level measure to draw (default: endplate)")
    ap.add_argument("--out", default=None, help="output image (default: alongside this script)")
    ap.add_argument("--folds", type=int, default=5)
    a = ap.parse_args()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                         "font.size": 10})

    column, xlabel = MEASURES[a.measure]
    vals = read_values(column)
    withheld = a.measure in WITHHOLD_L5
    if withheld:
        vals.pop("L5", None)
    refs = read_panjabi(a.measure)

    X, y, groups, lv = build_with_levels(os.path.join(DATA, "level_gradients.csv"))
    scores = out_of_fold_scores(X, y, groups, folds=a.folds)
    by_level = {l: scores[lv == l] for l in LEVELS}
    print("vertebrae scored: %d from %d cases   out-of-fold AUC %.3f"
          % (len(y), len(np.unique(groups)), auc(y, scores)))

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 5.2), constrained_layout=True)

    ys = violins(axL, vals, "#4878a8", xlabel,
                 "%s by ground-truth level" % xlabel.split(" (")[0])
    for l, pos in zip(LEVELS, ys):
        if l in refs and len(vals.get(l, [])) > 1:
            m, sd = refs[l]
            axL.plot([m - REF_K * sd, m + REF_K * sd], [pos + 0.44] * 2,
                     color="#b2182b", linewidth=2.0, solid_capstyle="butt", zorder=5)
            axL.plot([m], [pos + 0.44], marker="|", color="#b2182b",
                     markersize=9, markeredgewidth=2.0, zorder=6)
    if withheld:
        # say it on the empty row itself, not in a footnote that collides with the axis
        axL.text(0.5, ys[LEVELS.index("L5")],
                 "withheld: transverse processes fall in front of the body cut",
                 transform=axL.get_yaxis_transform(), ha="center", va="center",
                 fontsize=8, style="italic", color="0.35")
    axL.legend(handles=[
        Patch(facecolor="#4878a8", alpha=0.75, edgecolor="black",
              label="CT Spinopelvic One-thousand, $n$=802"),
        Line2D([0], [0], color="#b2182b", linewidth=2.0,
               label="Panjabi 1992, mean $\\pm$ 1.96 SD ($n$=12)")],
        loc="upper right", fontsize=8, framealpha=0.95)

    violins(axR, by_level, "#7a9e5b", "P(thoracic), out of fold",
            "Where the classifier puts the transition")
    axR.axvline(0.5, color="black", linewidth=1.0, linestyle="--", zorder=4)
    axR.set_xlim(-0.02, 1.02)
    axR.text(0.5, 0.52, " decision boundary", transform=axR.get_xaxis_transform(),
             fontsize=8, va="bottom", ha="left", color="0.25")

    os.makedirs(OUTDIR, exist_ok=True)
    out = a.out or os.path.join(OUTDIR, "thoracolumbar_violins_%s.png" % a.measure)
    fig.savefig(out, dpi=200)
    print("wrote " + out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
