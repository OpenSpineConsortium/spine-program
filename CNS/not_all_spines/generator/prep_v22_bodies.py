"""paper/cns2026/prep_v22_bodies.py -- slide 12's plot: naming as measures are added, and how sure it is (v22, Greg, 2026-11-01).

Greg asked for the smooth figure that reaches 100 and 99 per cent in place of v21's four points: bordercall's build-up
study (records/curve-2026-10-28, curve_accuracy.csv), typical synthetic columns, 2,000 of them, the measures added in
the study's greedy order up to all 32, with 1, 3 and 9 bodies in view. Three panels as the record draws them: the per
cent of fields named exactly, the per cent named at a posterior of 0.99, and the per cent of those that are right,
dotted at 99. The seven SPINEPS measures' crosses are left out, as the slide is about the 32. Drawn as Benzel draws,
black on white, closed frames, ticks inward, bold Arial, one line code per number of bodies, sized to the part of the
fingerprint slide the fingerprint leaves empty.

    python paper/cns2026/prep_v22_bodies.py
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[3] / "bordercall" / "records" / "curve-2026-10-28" / "figures" / "curve_accuracy.csv"
FIG = HERE / "figs_v22_6min"
EMU, DPI = 914400, 300
BOX = (5800000, 1420000, 11272466 - 5800000, 3830000)        # right of the fingerprint, to the canal box's edge
BODIES = ((9, "9 bodies", "-", "o", "black"), (3, "3 bodies", "--", "s", "white"), (1, "1 body", ":", "^", "white"))
PANELS = (("Named exactly", "Named exactly", (0, 104), range(0, 101, 20)),
          ("Named at 0.99", "Named at 99% certainty", (0, 104), range(0, 101, 20)),
          ("Right of those named", "Right when named", (98.93, 100.07), (99.0, 99.5, 100.0)))
MARKS = (1, 4, 8, 12, 16, 20, 24, 28, 32)


def rows():
    out = {}
    for r in csv.DictReader(open(SOURCE, encoding="utf-8")):
        if r["subset"].startswith("prefix") and r["drawn"] == "yes" and not math.isnan(float(r["percent"])):
            out.setdefault((r["panel"], int(r["bodies"])), []).append((int(r["measures"]), float(r["percent"])))
    return {k: sorted(v) for k, v in out.items()}


def style(ax, ylim, yticks, title):
    ax.set_xlim(0, 33)
    ax.set_ylim(*ylim)
    ax.set_xticks([1, 8, 16, 24, 32])
    ax.set_yticks(list(yticks))
    ax.tick_params(axis="both", direction="in", length=4, width=1.0, labelsize=9.5, pad=3, top=True, right=True)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=6)
    ax.set_xlabel("Measures", fontsize=10.5, labelpad=3)


def main():
    plt.rcParams.update({"font.family": "Arial", "font.weight": "bold", "axes.labelweight": "bold"})
    data = rows()
    fig, axes = plt.subplots(1, 3, figsize=(BOX[2] / EMU, BOX[3] / EMU), dpi=DPI)
    fig.subplots_adjust(left=0.085, right=0.99, top=0.91, bottom=0.13, wspace=0.42)
    for ax, (panel, title, ylim, yticks) in zip(axes, PANELS):
        if panel.startswith("Right"):
            ax.axhline(99.0, color="black", lw=0.9, ls=(0, (1, 2)))
        for n, label, line, marker, face in BODIES:
            pts = data[(panel, n)]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            every = [i for i, x in enumerate(xs) if x in MARKS]
            ax.plot(xs, ys, ls=line, color="black", lw=1.5, marker=marker, ms=5, markevery=every, mfc=face,
                    mec="black", mew=1.2, label=label, clip_on=False)
        style(ax, ylim, yticks, title)
        if panel.startswith("Right"):
            ax.set_yticklabels(["99", "99.5", "100"], fontweight="bold")
    axes[0].set_ylabel("Per cent of fields", fontsize=10.5)
    axes[0].legend(loc="lower right", fontsize=9, frameon=False, handlelength=2.4, borderaxespad=0.4)
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / "bodies_curve.png", dpi=DPI, facecolor="white")
    plt.close(fig)
    for panel, *_ in PANELS:
        print(panel, {n: round(data[(panel, n)][-1][1], 2) for n, *_ in BODIES})


if __name__ == "__main__":
    main()
