"""paper/cns2026/prep_v20_spinopelvic.py -- slide 7 of the 6-minute CNS deck redrawn in Benzel's style (v20,
Greg, 2026-10-31, night).

v14's three spinopelvic panels (prep_v14_6min_figs.spinopelvic, after make_figures.fig_validation) as Benzel draws a
figure: true histograms in grey with black edges, a closed black frame, ticks inward, bold Arial, the axis named in
words with its unit, and the published means as black lines told apart by their dash, the standing film's one SD a
grey band. The same rows (morphometrics/surgical_morphometrics.csv, end plates the S1 gate kept), the same ranges
and the same reference means as v14: Veilleux 2020 (supine CT, n = 200), Hasegawa 2018 (n = 24) and Vialle 2005
(standing film, mean and SD).

    python paper/cns2026/prep_v20_spinopelvic.py
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = Path(__file__).resolve().parent
ROWS = HERE.parents[2] / "03_ctspinopelvic1k_dataset" / "mdpa" / "morphometrics" / "surgical_morphometrics.csv"
FIG = HERE / "figs_v20_6min"
W_IN, H_IN, DPI = 11.1, 4.19, 200
BARS, EDGE, BAND = "#C9C9C9", "black", "#E6E6E6"
BIN = 5
# key, name, plotted range, Vialle standing mean and SD, Veilleux supine CT mean, Hasegawa mean (v14's numbers)
SPEC = (("pelvic_incidence_deg", "Pelvic Incidence", 20, 90, 55.0, 10.6, 52.1, 53.4),
        ("sacral_slope_deg", "Sacral Slope", 10, 70, 41.0, 8.4, 36.5, 34.1),
        ("pelvic_tilt_deg", "Pelvic Tilt", -10, 45, 13.0, 6.0, 15.6, 19.2))


def rows():
    kept = [r for r in csv.DictReader(open(ROWS, encoding="utf-8")) if (r.get("s1_plate_rejected") or "0") in ("", "0")]
    return kept, sum(1 for _ in open(ROWS, encoding="utf-8")) - 1


def values(kept, key):
    out = []
    for r in kept:
        try:
            out.append(float(r[key]))
        except (KeyError, ValueError):
            pass
    return out


def panel(ax, vals, name, lo, hi, ref, sd, ct, has, first):
    shown = [v for v in vals if lo <= v <= hi]
    edges = np.arange(np.floor(lo / BIN) * BIN, hi + BIN, BIN)
    ax.axvspan(ref - sd, ref + sd, color=BAND, lw=0, zorder=0)
    ax.hist(shown, bins=edges, color=BARS, edgecolor=EDGE, linewidth=0.7, zorder=2)
    top = ax.get_ylim()[1] * 1.6
    ax.axvline(ct, color="black", ls="--", lw=1.8, zorder=3)
    ax.axvline(ref, color="black", ls=":", lw=2.0, zorder=3)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, top)
    ax.tick_params(axis="both", direction="in", length=5, width=1.1, labelsize=13, pad=4, top=False, right=False)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_linewidth(1.3)
    ax.set_xlabel(f"{name} (degrees)", fontsize=14, fontweight="bold", labelpad=4)
    if first:
        ax.set_ylabel("Number of CTs", fontsize=14, fontweight="bold")
    mean, s = statistics.fmean(vals), statistics.stdev(vals)
    ax.text(0.035, 0.955, f"{mean:.1f} ± {s:.1f}°", transform=ax.transAxes, fontsize=13.5, fontweight="bold",
            va="top")
    ax.text(0.035, 0.84, f"Veilleux {ct:.1f}\nHasegawa {has:.1f}", transform=ax.transAxes, fontsize=11.5, va="top",
            fontweight="normal", linespacing=1.15)
    return len(vals), mean, s


def main():
    plt.rcParams.update({"font.family": "Arial", "font.weight": "bold", "axes.labelweight": "bold"})
    kept, total = rows()
    fig, axes = plt.subplots(1, 3, figsize=(W_IN, H_IN), dpi=DPI)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.97, bottom=0.25, wspace=0.16)
    table = {}
    for i, (ax, (key, name, lo, hi, ref, sd, ct, has)) in enumerate(zip(axes, SPEC)):
        table[key] = panel(ax, values(kept, key), name, lo, hi, ref, sd, ct, has, i == 0)
    fig.legend(handles=[Patch(facecolor=BARS, edgecolor=EDGE, linewidth=0.7, label="This dataset's CTs"),
                        Line2D([], [], color="black", ls="--", lw=1.8, label="Supine CT, Veilleux 2020, mean"),
                        Line2D([], [], color="black", ls=":", lw=2.0, label="Standing film, Vialle 2005, mean"),
                        Patch(facecolor=BAND, lw=0, label="± 1 SD")],
               loc="lower center", ncol=4, frameon=False, fontsize=12.5, bbox_to_anchor=(0.5, -0.025),
               columnspacing=1.3, handlelength=2.2)
    fig.savefig(FIG / "spinopelvic_benzel.png", dpi=DPI)
    plt.close(fig)
    n = min(v[0] for v in table.values())
    caption = (f"{n} of {total} CTs passing the geometric gates; mean ± SD in each panel. Veilleux n = 200, "
               "Hasegawa n = 24, supine CT.")
    json.dump({"caption": caption, "table": {k: [v[0], round(v[1], 1), round(v[2], 1)] for k, v in table.items()}},
              open(FIG / "spinopelvic.json", "w", encoding="utf-8"), indent=1)
    print(caption, table)


if __name__ == "__main__":
    main()
