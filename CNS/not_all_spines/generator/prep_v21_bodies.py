"""paper/cns2026/prep_v21_bodies.py -- slide 12's right panel: naming gets surer as more bodies are seen (v21, Greg, 2026-10-31).

bordercall's synthetic columns (records/chain-2026-10-28, chain_accuracy.csv, the rule that links the bodies in view,
all 32 measures, 200 fields a point): the per cent of fields whose middle body is named exactly, against the number of
bodies in view, for typical columns, columns with six lumbar bodies and columns with a thirteenth thoracic. Drawn as
Benzel draws, black on white, closed frame, ticks inward, bold Arial, one line code per type, sized to the box of
slide 5's right panel so it stands where the canal plot stood.

    python paper/cns2026/prep_v21_bodies.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[3] / "bordercall" / "records" / "chain-2026-10-28" / "figures" / "chain_accuracy.csv"
FIG = HERE / "figs_v21_6min"
EMU, DPI = 914400, 300
BOX = (4241275, 3829999)
TYPES = (("typical", "Typical, 24 presacral", "-", "o", "black"),
         ("six_lumbar", "Six lumbar bodies", "--", "s", "white"),
         ("t13", "A thirteenth thoracic", ":", "^", "white"))


def rows():
    out = {}
    for r in csv.DictReader(open(SOURCE, encoding="utf-8")):
        if r["measures"] == "all" and r["rule"] == "chain":
            out.setdefault(r["type"], []).append((int(r["bodies"]), float(r["percent"]), int(r["fields"])))
    return {k: sorted(v) for k, v in out.items()}


def main():
    plt.rcParams.update({"font.family": "Arial", "font.weight": "bold", "axes.labelweight": "bold"})
    data = rows()
    fig, ax = plt.subplots(figsize=(BOX[0] / EMU, BOX[1] / EMU), dpi=DPI)
    fig.subplots_adjust(left=0.16, right=0.965, top=0.965, bottom=0.17)
    for key, label, style, marker, face in TYPES:
        pts = data[key]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], ls=style, color="black", lw=1.6, marker=marker, ms=6.5,
                mfc=face, mec="black", mew=1.4, label=label)
    ax.set_xlim(0.4, 9.6)
    ax.set_ylim(80, 100)
    ax.set_xticks([1, 3, 5, 9])
    ax.set_yticks(range(80, 101, 5))
    ax.tick_params(axis="both", direction="in", length=5, width=1.1, labelsize=11, pad=4, top=True, right=True)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
    ax.set_xlabel("Bodies in View", fontsize=12.5, labelpad=6)
    ax.set_ylabel("Middle Body Named Exactly (%)", fontsize=12.5)
    ax.legend(loc="lower right", fontsize=10, frameon=False, handlelength=2.6, borderaxespad=0.8)
    fig.savefig(FIG / "bodies_benzel.png", dpi=DPI, facecolor="white")
    plt.close(fig)
    n = {k: v[0][2] for k, v in data.items()}
    print({k: [p[1] for p in v] for k, v in data.items()}, n)


if __name__ == "__main__":
    main()
