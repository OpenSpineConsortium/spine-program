"""paper/cns2026/make_v3_charts.py — figures for the slides of the SchwingNet talk that had none (Greg 2026-09-25:
"I want a figure on every slide"; then "I hate that sideways bar chart. I prefer line graphs or pie charts").
Every share is a donut, every trend a line; no horizontal bars. Every number is one already on the slide, from the
SchwingNet manuscript (results.tex, tab3_naming.md, tab2_detection.md, NUMBERS.md) or from spinesurg
docs/WRONG_LEVEL_COST_EVIDENCE.md and docs/WRONG_SITE_BURDEN_EVIDENCE.md (verified 2026-09-19). Writes PNGs into
paper/cns2026/figs_v2/.

    python paper/cns2026/make_v3_charts.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet" / "figures"

# palette of the 2026 CNS Annual Meeting speaker template (theme1.xml): navy dk1, blue accent4, red accent2, gold accent1
TEAL = "#191D63"          # navy (name kept so the chart code below is unchanged)
TEAL_LIGHT = "#4C70B7"    # blue
TEAL_PALE = "#C9D4EC"     # pale blue
GREY = "#9A9A9A"
GREY_LIGHT = "#E6E6E5"    # lt2
INK = "#191D63"
RED = "#EF4627"
RED_LIGHT = "#F5B3A6"
GOLD = "#FFC42F"

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 20,
    "axes.titlesize": 20,
    "axes.labelsize": 19,
    "xtick.labelsize": 17,
    "ytick.labelsize": 17,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.6,
    "axes.axisbelow": True,
    "figure.dpi": 220,
    "savefig.dpi": 220,
    "savefig.facecolor": "white",
})


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size)


def donut(ax, frac, centre, label, color=TEAL, rest=GREY_LIGHT, sub=None, width=0.36, centre_size=30, label_size=17):
    """One share as a ring: `frac` of the ring in `color`, the rest pale; `centre` printed in the middle, `label` under."""
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    ax.pie([frac, 1 - frac], colors=[color, rest], startangle=90, counterclock=False,
           wedgeprops=dict(width=width, edgecolor="white", linewidth=1.5))
    ax.text(0, 0.04, centre, ha="center", va="center", fontsize=centre_size, fontweight="bold", color=INK)
    if sub:
        ax.text(0, -0.26, sub, ha="center", va="center", fontsize=14, color=GREY)
    ax.set_title(label, fontsize=label_size, pad=10, color=INK)


def nested_donut(ax, outer, inner, centre, label, outer_color=TEAL, inner_color=TEAL_LIGHT, label_size=11.5):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    ax.pie([outer, 1 - outer], colors=[outer_color, GREY_LIGHT], startangle=90, counterclock=False, radius=1.0,
           wedgeprops=dict(width=0.26, edgecolor="white", linewidth=1.5))
    ax.pie([inner, 1 - inner], colors=[inner_color, GREY_LIGHT], startangle=90, counterclock=False, radius=0.72,
           wedgeprops=dict(width=0.26, edgecolor="white", linewidth=1.5))
    ax.text(0, 0.0, centre, ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
    ax.set_title(label, fontsize=label_size, pad=10, color=INK)


def pie_with_legend(ax, values, labels, colors, title, explode=None, legend_title=None):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    total = sum(values)
    wedges, _ = ax.pie(values, colors=colors, startangle=90, counterclock=False, explode=explode,
                       wedgeprops=dict(width=0.55, edgecolor="white", linewidth=1.5))
    legend_labels = [f"{l}: {v:,} ({v / total * 100:.0f} %)" if v / total >= 0.005 else f"{l}: {v:,}" for l, v in zip(labels, values)]
    ax.legend(wedges, legend_labels, loc="upper center", bbox_to_anchor=(0.5, -0.02), frameon=False, fontsize=17, title=legend_title,
              title_fontsize=17)
    ax.set_title(title, fontsize=19, loc="left", color=INK)


# ---------------------------------------------------------------- 1. crops of the C-arm exposures (Figure 4 a, b)
def crops():
    im = Image.open(SN / "figure4.png")
    a = im.crop((75, 87, 654, 847))          # panel a: the exposure with body and sacrum boxes
    b = im.crop((1120, 87, 1972, 847))       # panel b: field b with the names and posteriors
    a.save(OUT / "sn_fig4_a_img.png")
    b.save(OUT / "sn_fig4_b_img.png")
    gap = 40
    comp = Image.new("RGB", (a.width + gap + b.width, a.height), "white")
    comp.paste(a, (0, 0))
    comp.paste(b, (a.width + gap, 0))
    comp.save(OUT / "sn_fig4_ab_img.png")
    print("crops", a.size, b.size, comp.size)


# ---------------------------------------------------------------- 2. slide 4: how often the count is wrong
def chart_rates():
    fig = plt.figure(figsize=(11.0, 4.0))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.6], wspace=0.25)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    donut(ax1, 0.50, "1 in 2", "Surgeons with ≥1 wrong-level\noperation in their career\n(Mody 2008, 207 of 415; Groff 2013)",
          sub="207 of 415")
    nested_donut(ax2, 0.15, 0.043, "4.3–15 %", "Lumbar operations whose first\nexposed level was wrong,\nbefore the check film")
    ax2.set_ylim(-1.5, 1.2)
    ax2.text(0, -1.3, "outer 15 % (Ammerman 2006)\ninner 4.3 % (Dablouk 2019)", ha="center", va="top", fontsize=9.5, color=GREY)
    x = [0, 1, 2]
    y = [5, 13, 42]
    lo = [2, 9, 16]
    hi = [12, 18, 108]
    ax3.plot(x, y, color=TEAL, lw=2.2, marker="o", ms=8, zorder=3)
    ax3.errorbar(x, y, yerr=[[a - b for a, b in zip(y, lo)], [b - a for a, b in zip(y, hi)]], fmt="none", ecolor=INK, elinewidth=1.2, capsize=4, zorder=2)
    for xi, yi in zip(x, y):
        ax3.text(xi + 0.08, yi + 3, str(yi), fontsize=12, color=INK, va="bottom")
    ax3.axhline(12, color=TEAL_LIGHT, lw=1.4, ls="--", label="registry, all regions: 12")
    ax3.axhline(3.2, color=GREY, lw=1.4, ls=":", label="self-report: 3.2 (1 in 3,110; Mody 2008)")
    ax3.legend(loc="upper left", frameon=False, fontsize=10)
    ax3.set_xticks(x)
    ax3.set_xticklabels(["cervical", "lumbar", "thoracic"])
    ax3.set_xlim(-0.35, 2.35)
    ax3.set_ylim(0, 115)
    ax3.set_ylabel("wrong-level operations per 10,000")
    ax3.grid(axis="x", visible=False)
    ax3.set_title("Registry of 34,544 operations (Furuya 2026), 95 % CI", fontsize=11.5, loc="left")
    save(fig, "chart_rates.png")


# ---------------------------------------------------------------- 3. slide 6: what it costs
def chart_costs():
    fig = plt.figure(figsize=(13.6, 4.0))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 2.1], wspace=0.3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[0, 3])
    donut(ax1, 0.17, "17 %", "Self-reported wrong-level\nevents with legal action or\nsettlement (Mody 2008)", label_size=10)
    donut(ax2, 0.20, "20 %", "Spine Section surgeons ever\nsued for wrong-level or wrong-\nside lumbar surgery (Groff 2013)", label_size=10)
    donut(ax3, 0.81, "81 %", "Litigated wrong-disc-level\ncases ending in a payment\n(Goodkin & Laska 2004)", color=RED, label_size=10)
    # dollars: points with their ranges on a log axis
    ax4.set_yscale("log")
    ax4.set_ylim(800, 3e6)
    ax4.set_xlim(-0.6, 2.6)
    ax4.plot([0, 0], [1750, 1950], color=GREY, lw=6, solid_capstyle="round")
    ax4.text(0, 2300, "$1,750–1,950", ha="center", va="bottom", fontsize=11.5, color=INK)
    ax4.plot([1, 1], [28847, 215003], color=TEAL_LIGHT, lw=6, solid_capstyle="round")
    ax4.plot(1, 75220, "o", color=TEAL, ms=11, zorder=3)
    ax4.text(1.09, 75220, "$75,220\nmedian", ha="left", va="center", fontsize=11.5, color=INK)
    ax4.text(1.1, 30000, "IQR $28,847–215,003", ha="left", va="center", fontsize=9.5, color=GREY)
    ax4.plot(2, 136453, "o", color=TEAL, ms=11, zorder=3)
    ax4.text(2, 170000, "$136,453\nmean", ha="center", va="bottom", fontsize=11.5, color=INK)
    ax4.set_xticks([0, 1, 2])
    ax4.set_xticklabels(["fiducial\nplacement", "NPDB\nnever event", "wrong-site\nclaim"], fontsize=10)
    ax4.set_xlabel("AJNR 2023 with Childers 2018  ·  Bettis 2026  ·  Tan 2023 (n = 68)", fontsize=9, color=GREY)
    ax4.set_ylabel("US dollars, log scale")
    ax4.grid(axis="x", visible=False)
    ax4.set_title("Per event: avoiding one, and paying for one", fontsize=11.5, loc="left")
    save(fig, "chart_costs.png")


# ---------------------------------------------------------------- 4. slide 7: prior art, each against its own truth
def chart_priorart():
    fig, axes = plt.subplots(1, 5, figsize=(12.6, 3.6), gridspec_kw={"wspace": 0.35})
    items = [
        (1.00, "100 %", "LevelCheck label\nplacement, against the\nimported labels\n(De Silva 2016)", GREY),
        (0.976, "97.6 %", "Surgeons with the\nLevelCheck overlay,\n62 difficult films\n(Manbachi 2018)", GREY),
        (0.883, "88.3 %", "Long-length cadaver\nimages, region CNN\n(Huang 2022)", TEAL_LIGHT),
        (0.80, "77.9–82.2 %", "Lumbar MRI localiser,\nno count from C2\n(Peh 1999)", TEAL_LIGHT),
        (0.733, "73.3 %", "Real C-arm images,\nidentity imported from\na preoperative film\n(Zhang 2023)", TEAL_LIGHT),
    ]
    for ax, (f, c, l, col) in zip(axes, items):
        donut(ax, f, c, l, color=col, centre_size=15 if len(c) < 8 else 11.5, label_size=10)
    axes[0].text(0, -1.3, "truth = the planning read", ha="center", fontsize=10, color=GREY)
    axes[1].text(0, -1.3, "truth = the planning read", ha="center", fontsize=10, color=GREY)
    fig.suptitle("Each number is scored against its own truth; none is tested on a transitional spine", fontsize=12.5, x=0.02, ha="left", y=1.02)
    save(fig, "chart_priorart.png")


# ---------------------------------------------------------------- 5. slide 10: the corpus
def chart_corpus():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 7.6), gridspec_kw={"wspace": 0.2})
    pie_with_legend(ax1, [4093, 9108, 3498, 778],
                    ["CT renders", "Films with levels", "Real exposures, fixed", "Real exposures, mobile C-arm"],
                    [TEAL_PALE, TEAL_LIGHT, TEAL, RED], "(a) 17,477 images, all public", explode=[0, 0, 0, 0.08])
    pie_with_legend(ax2, [110, 31, 28, 14, 7, 4],
                    ["Sixth lumbar (L6)", "Castellvi I/II", "Sacralised L5", "Lumbar rib", "T13", "Unassigned"],
                    [TEAL, TEAL_LIGHT, TEAL_PALE, GOLD, RED, GREY], "(b) 194 transitional persons")
    save(fig, "chart_corpus.png")


# ---------------------------------------------------------------- 6. slide 12: the test set
def chart_testset():
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 5.4))
    donut(axes[0], 814 / 910, "89.5 %", "Vertebrae both labellers\nagree on (814 of 910)", sub="96 not scored")
    donut(axes[1], 617 / 676, "91.3 %", "Lateral bodies boxed\n(617 of 676)", sub="59 not boxed")
    donut(axes[2], 631 / 673, "93.8 %", "Anteroposterior bodies\nboxed (631 of 673)", sub="42 not boxed")
    fig.subplots_adjust(wspace=0.35)
    save(fig, "chart_testset.png")


# ---------------------------------------------------------------- 7. slide 15: count, shape, coupled; the stop
def chart_coupling():
    fig, axes = plt.subplots(2, 3, figsize=(12.5, 9.0))
    donut(axes[0, 0], 979 / 1009, "97.0 %", "Count from the sacrum", color=TEAL_LIGHT, rest=RED, sub="30 wrong")
    donut(axes[0, 1], 986 / 1009, "97.7 %", "Shape alone", color=TEAL_LIGHT, rest=RED, sub="23 wrong")
    donut(axes[0, 2], 991 / 1009, "98.2 %", "Both together", color=TEAL, rest=RED, sub="18 wrong")
    donut(axes[1, 0], 23 / 233, "23 of 233", "All anchored frames", color=RED, rest=TEAL_PALE, centre_size=26)
    donut(axes[1, 1], 5 / 6, "5 of 6", "Frames with an error", color=RED, rest=TEAL_PALE, centre_size=26)
    donut(axes[1, 2], 1.0, "4 of 4", "Six-lumbar calls", color=RED, rest=TEAL_PALE, centre_size=26)
    fig.text(0.02, 0.985, "(a) Exact level on 1,009 bodies; red, the errors", fontsize=20, ha="left", va="top", color=INK)
    fig.text(0.02, 0.47, "(b) Frames the read declined to name (red)", fontsize=20, ha="left", va="top", color=INK)
    fig.subplots_adjust(top=0.88, bottom=0.03, hspace=0.6, wspace=0.25)
    save(fig, "chart_coupling.png")


# ---------------------------------------------------------------- 8. slide 18: the test owed and the census
def chart_census():
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 5.6))
    donut(axes[0], 7 / 35, "7 of 35", "Real-frame candidates,\nof the 35 that certify 90 %", color=RED, centre_size=26)
    donut(axes[1], 3 / 22, "3 of 22", "Carriers scored (cross-\nvalidation), of 22 needed", color=RED, centre_size=26)
    donut(axes[2], 21 / 322, "21 of 322", "L6 found by both labellers,\nof the 322 the census holds", color=TEAL, centre_size=26)
    fig.subplots_adjust(wspace=0.35)
    save(fig, "chart_census.png")


# ---------------------------------------------------------------- 9. slide 19: one device, two poses
def chart_coverage():
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    x = [0, 1, 2, 3, 4]
    y = [148, 0, 0, 15, 133]
    ax.fill_between(x, y, color=TEAL_PALE, alpha=0.8)
    ax.plot(x, y, color=TEAL, lw=2.4, marker="o", ms=8, zorder=3)
    for xi, yi in zip(x, y):
        ax.text(xi, yi + 6, str(yi), ha="center", va="bottom", fontsize=17, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(["0–10°\nanteroposterior", "10–30°", "30–60°", "60–90°", "≥ 90°\nlateral"])
    ax.set_ylabel("real frames")
    ax.set_ylim(0, 180)
    ax.set_xlim(-0.2, 4.2)
    ax.grid(axis="x", visible=False)
    ax.set_title("296 real frames: 3 of 18 angle bins occupied", loc="left", fontsize=19)
    save(fig, "chart_coverage.png")


# ---------------------------------------------------------------- 10. slide 20: the headline numbers
def chart_headline():
    fig, axes = plt.subplots(2, 2, figsize=(8.4, 8.0))
    donut(axes[0, 0], 595 / 617, "96.4 %", "Lateral, zero-shot", sub="595 of 617", centre_size=28)
    donut(axes[0, 1], 601 / 617, "97.4 %", "Lateral, fine-tuned", color=TEAL_LIGHT, sub="601 of 617", centre_size=28)
    donut(axes[1, 0], 979 / 1009, "97.0 %", "Count from the sacrum", color=TEAL_LIGHT, sub="979 of 1,009", centre_size=28)
    donut(axes[1, 1], 991 / 1009, "98.2 %", "Coupled call", sub="991 of 1,009", centre_size=28)
    fig.subplots_adjust(hspace=0.35, wspace=0.05, top=0.94, bottom=0.02)
    save(fig, "chart_headline.png")


# ---------------------------------------------------------------- 11. slide 2: public and withheld
def diagram_disclosure():
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.grid(False)

    def column(x, title, items, face, edge, tcolor):
        ax.add_patch(FancyBboxPatch((x, 0.4), 4.5, 9.2, boxstyle="round,pad=0.02,rounding_size=0.25", fc=face, ec=edge, lw=1.5))
        ax.text(x + 2.25, 9.0, title, ha="center", va="center", fontsize=11.5, fontweight="bold", color=tcolor)
        yy = 7.9
        for it in items:
            ax.text(x + 0.3, yy, "•  " + it, ha="left", va="top", fontsize=10.5, color=INK, wrap=True)
            yy -= 1.55
    column(0.2, "Public", ["CTSpinoPelvic1K dataset\n(Zenodo, arXiv)", "Not All Spines Are Created\nEqual (NeurIPS 2026)",
                           "Two-labeller CT census\n(AACA 2026)", "This talk: what the system\ndid, and how it was tested",
                           "Weights, device parameters\nand code with the paper"], "#EAF2F0", TEAL, TEAL)
    column(5.3, "Withheld, under review", ["The network architecture", "How the shape reading and\nthe count are combined",
                                           "When the read stops", "The device image-formation\nmodels", "Invention disclosure on file,\nWayne State University"],
           "#F6ECE9", RED, RED)
    save(fig, "diagram_disclosure.png")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    crops()
    chart_rates()
    chart_costs()
    chart_priorart()
    chart_corpus()
    chart_testset()
    chart_coupling()
    chart_census()
    chart_coverage()
    chart_headline()
    diagram_disclosure()
