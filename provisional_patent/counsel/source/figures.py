"""Figures for the inventor's responses to counsel (WSU 26-1902).

Every plotted number is copied from the file named in the figure's caption in the
Word document; schematics are labelled as illustrative.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import numpy as np

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "text.color": INK,
    "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
    "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, ec=INK2, size=9, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                fc=fc, ec=ec, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            weight=weight, wrap=True)


def arrow(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=12,
                                 color=INK2, lw=1))


def three_framings():
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    cols = [
        ("IDF Part A\n(25 Sep 2026)", "Preoperative CT:\nname-free, segmenter-\nagnostic classifier of the\ntransitional phenotype,\nwith a plain-language reason",
         "Design only.\nFeatures extracted;\nno classifier trained\n(CLASSIFIERS.md R33)", "#f6e3a8"),
        ("IDF Part B\n(25 Sep 2026)", "One C-arm exposure:\nlevel named from local\nmorphology, coupled to a\ncount from the sacrum,\nwith abstention",
         "Reduced to practice on\nreal C-arm frames\n(automated truth);\nconfidential manuscript", "#cfe3f7"),
        ("Draft provisional\n(18 Sep 2026)", "Several overlapping\nexposures linked into a\nchain; alphabets; confidence\nand a commanded move;\npersistent digital marker",
         "Implemented and tested\non renders and real films;\nnot on real overlapping\nintraoperative series", "#cdeedd"),
    ]
    for i, (title, what, status, fc) in enumerate(cols):
        x = 0.2 + i * 3.3
        box(ax, x, 3.85, 3.0, 0.95, title, fc, size=10, weight="bold")
        box(ax, x, 1.95, 3.0, 1.7, what, "white")
        box(ax, x, 0.25, 3.0, 1.5, status, "#f2f1ee", size=8.5)
    save(fig, "fig1_three_framings.png")


def acquisition_geometry():
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ax.set_xlim(-0.5, 13.2); ax.set_ylim(-0.5, 11.5); ax.axis("off")
    names = ["S1", "L5", "L4", "L3", "L2", "L1", "T12", "T11", "T10", "T9"]
    p = 1.05
    for i, n in enumerate(names):
        y = 0.3 + i * p
        ax.add_patch(Rectangle((1.0, y), 1.1, 0.75, fc="#e9e7e1", ec=INK2, lw=0.8))
        ax.text(0.85, y + 0.37, n, ha="right", va="center", fontsize=8, color=INK2)
    fields = [(0.0, BLUE, "Image 1 (landmark: sacrum)"), (2.1, ORANGE, "Image 2"),
              (4.2, AQUA, "Image 3")]
    S = 4.2
    for k, (y0, c, label) in enumerate(fields):
        x = 2.5 + k * 0.55
        ax.add_patch(Rectangle((x, y0), 0.4, S, fc=c, alpha=0.25, ec=c, lw=1.5))
        ax.text(x + 0.5 + (2 - k) * 0.0, y0 + S - 0.25, "", fontsize=8)
        ax.text(4.4, y0 + S / 2 + k * 0.0, "", fontsize=8)
        ax.annotate(label, xy=(x + 0.4, y0 + S / 2), xytext=(4.6, 1.0 + k * 2.6),
                    fontsize=8.5, color=INK, arrowprops=dict(arrowstyle="-", color=c, lw=1))
    def span(x, y0, y1, text):
        ax.annotate("", xy=(x, y0), xytext=(x, y1), arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
        ax.text(x + 0.15, (y0 + y1) / 2, text, fontsize=8.5, va="center")
    span(8.9, 0.0, 2.1, "step = S - O x p")
    span(8.9, 2.1, 4.2, "overlap O = 2 bodies")
    span(12.6, 0.0, 4.2, "S")
    ax.text(7.2, 8.6, "S = field at the spine\n(about 140 mm, 9-inch C-arm)\n"
                      "p = observed vertebral spacing\n(19 / 27 / 34 mm cervical /\nthoracic / lumbar medians)",
            fontsize=8.5, va="center", color=INK2)
    save(fig, "fig2_acquisition_geometry.png")


def asymmetric_window():
    fig, ax = plt.subplots(figsize=(8.0, 3.4))
    dy = np.linspace(-1.6, 2.6, 800)
    true = 1.0
    sim = 0.55 + 0.30 * np.cos(2 * np.pi * (dy - true)) * np.exp(-0.18 * (dy - true) ** 2)
    sim += 0.10 * np.exp(-((dy - true) ** 2) / 0.02)
    lo, hi = true - 0.5, true + 0.6
    ax.axvspan(lo, hi, color=BLUE, alpha=0.12, lw=0)
    ax.plot(dy, sim, color=BLUE, lw=2)
    ax.axvline(true, color=INK2, lw=1, ls="--")
    for alias in (true - 1, true + 1):
        ax.annotate("aliased peak\n(one vertebra off)", xy=(alias, 0.55 + 0.30 * np.cos(0) * np.exp(-0.18)),
                    xytext=(alias + (-0.55 if alias < true else 0.15), 1.02), fontsize=8, color=INK2,
                    arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.text(true, 1.13, "commanded step", ha="center", fontsize=8.5)
    ax.text((lo + hi) / 2, 0.12, "search window:\n-0.5 p near, +0.6 p far", ha="center", fontsize=8.5,
            color=BLUE)
    ax.set_xlabel("candidate displacement, in vertebral spacings (p)")
    ax.set_ylabel("similarity (NCC)")
    ax.set_ylim(0.05, 1.22); ax.set_yticks([])
    ax.set_title("Asymmetric search window about the commanded step (illustrative curve, not data)",
                 fontsize=10.5, weight="bold", loc="left")
    save(fig, "fig3_asymmetric_window.png")


def alphabets():
    rows = [
        ("Ordinary", ["T11", "T12", "L1", "L2", "L3", "L4", "L5", "S"], None),
        ("T13", ["T11", "T12", "T13", "L1", "L2", "L3", "L4", "L5", "S"], "T13"),
        ("L6", ["T11", "T12", "L1", "L2", "L3", "L4", "L5", "L6", "S"], "L6"),
        ("T13 and L6", ["T11", "T12", "T13", "L1", "L2", "L3", "L4", "L5", "L6", "S"], "both"),
        ("Four lumbar (ext)", ["T11", "T12", "L1", "L2", "L3", "L4", "S"], "four"),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    ax.set_xlim(-2.6, 10.5); ax.set_ylim(-0.6, len(rows) + 0.4); ax.axis("off")
    for r, (name, seq, var) in enumerate(rows):
        y = len(rows) - 1 - r
        ax.text(-0.3, y + 0.35, name, ha="right", va="center", fontsize=9)
        for j, lev in enumerate(seq):
            extra = lev in ("T13", "L6") or (var == "four" and lev == "L4")
            fc = "#fde3d6" if extra else ("#e9e7e1" if lev != "S" else "#cfe3f7")
            ec = ORANGE if extra else INK2
            ax.add_patch(FancyBboxPatch((j * 1.0, y + 0.05), 0.85, 0.6,
                                        boxstyle="round,pad=0.01,rounding_size=0.08", fc=fc, ec=ec, lw=1))
            ax.text(j * 1.0 + 0.425, y + 0.35, lev, ha="center", va="center", fontsize=8.5)
    ax.text(4.0, len(rows) + 0.2, "Alternative alphabets near the thoracolumbar and lumbosacral junctions",
            ha="center", fontsize=10.5, weight="bold")
    ax.text(4.0, -0.45, "S = sacrum, the declared landmark pinning the caudal end. Orange: the segment that "
                        "distinguishes the alphabet. One output space; no extra class.",
            ha="center", fontsize=8, color=INK2)
    save(fig, "fig4_alphabets.png")


def remedy_flow():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
    box(ax, 3.4, 5.25, 3.2, 0.7, "Confidence = a x clip(b / tau, 0, 1)", "#cfe3f7", size=9.5)
    box(ax, 0.1, 3.6, 3.0, 1.0, "a low (appearance)\nlowest per-vertebra probability", "#f2f1ee")
    box(ax, 3.5, 3.6, 3.0, 1.0, "b low (geometry)\nweakest link's margin", "#f2f1ee")
    box(ax, 6.9, 3.6, 3.0, 1.0, "both pass the threshold", "#f2f1ee")
    arrow(ax, 4.2, 5.25, 1.6, 4.6); arrow(ax, 5.0, 5.25, 5.0, 4.6); arrow(ax, 5.8, 5.25, 8.4, 4.6)
    box(ax, 0.1, 1.75, 3.0, 1.35, "Full step toward the landmark\nstep = S - O x p, in mm\n(extend the chain)", "#cdeedd")
    box(ax, 3.5, 1.75, 3.0, 1.35, "Move to the midpoint of the\nweak link (measured position);\nraise overlap", "#cdeedd")
    box(ax, 6.9, 1.75, 3.0, 1.35, "Emit the level;\nplace the persistent marker;\nreturn to the operative field", "#cdeedd")
    arrow(ax, 1.6, 3.6, 1.6, 3.1); arrow(ax, 5.0, 3.6, 5.0, 3.1); arrow(ax, 8.4, 3.6, 8.4, 3.1)
    box(ax, 3.5, 0.15, 3.0, 1.1, "Bound reached\n(no new vertebra would enter):\nrefuse, naming the weak link", "#fde3d6")
    arrow(ax, 5.0, 1.75, 5.0, 1.25)
    save(fig, "fig5_remedy_flow.png")


def overlap_ladder():
    o = [0.5, 1, 1.5, 2, 2.5, 3, 4]
    acc = [81.7, 95.8, 91.7, 97.5, 96.7, 90.8, 82.5]
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.plot(o, acc, color=BLUE, lw=2, marker="o", ms=6, zorder=3)
    for x, y in zip(o, acc):
        if x in (1, 2, 4, 0.5):
            ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center",
                        fontsize=8.5, color=INK)
    ax.set_xlabel("overlap O between successive exposures (vertebral bodies)")
    ax.set_ylabel("chains completed (%)")
    ax.set_ylim(75, 100); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.set_title("Overlap is not monotone: two bodies is the operating point\n"
                 "120 held-out CT renders, 9-inch field, sweep_v3 (RECORD ONLY)",
                 fontsize=10, weight="bold", loc="left")
    save(fig, "fig6_overlap_ladder.png")


def window_ablation():
    widths = ["0.6 p\n(protocol)", "1.2 p", "2.1 p"]
    ctsp = [21, 52, 67]
    verse = [0, 8, 3]
    x = np.arange(3); w = 0.36
    fig, ax = plt.subplots(figsize=(7.6, 3.4))
    b1 = ax.bar(x - w / 2 - 0.01, ctsp, w, color=BLUE, label="801 CT renders from the sacrum (6,255 walks)")
    b2 = ax.bar(x + w / 2 + 0.01, verse, w, color=ORANGE, label="76 whole spines from C2 (834 walks)")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1, str(int(b.get_height())),
                    ha="center", fontsize=8.5)
    ax.set_xticks(x, widths); ax.set_xlabel("half-width of the search window either side of the step")
    ax.set_ylabel("wrong walks (count)")
    ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("Window ablation: counting stays 98.9-100% exact; the window removes the last errors",
                 fontsize=10, weight="bold", loc="left")
    save(fig, "fig7_window_ablation.png")


def chain_gain():
    groups = ["CT renders,\nsacrum (120)", "Real lumbar\nfilms (25)", "VerSe from\nC2 (12)",
              "TotalSeg.,\nsacrum (522)", "TotalSeg.,\nC2 (203)"]
    alone = [72.1, 78.7, 9.5, 51.2, 18.9]
    chain = [95.2, 93.6, 100.0, 94.3, 94.0]
    x = np.arange(len(groups)); w = 0.36
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    b1 = ax.bar(x - w / 2 - 0.01, alone, w, color="#9ec5f4", label="image alone")
    b2 = ax.bar(x + w / 2 + 0.01, chain, w, color=BLUE, label="registered onto the chain")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, f"{b.get_height():.1f}",
                    ha="center", fontsize=8)
    ax.set_xticks(x, groups, fontsize=8.5); ax.set_ylabel("frames named correctly (%)")
    ax.set_ylim(0, 125); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", ncol=2)
    ax.set_title("Two-body frames named alone versus on the chain (held out, sweep_v3, RECORD ONLY)",
                 fontsize=10, weight="bold", loc="left")
    save(fig, "fig8_chain_gain.png")


for f in (three_framings, acquisition_geometry, asymmetric_window, alphabets, remedy_flow,
          overlap_ladder, window_ablation, chain_gain):
    f()
print("ok")
