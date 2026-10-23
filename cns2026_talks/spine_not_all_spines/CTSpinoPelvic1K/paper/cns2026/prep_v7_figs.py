"""paper/cns2026/prep_v7_figs.py — (1) the manuscript's Figure 5a drawn by the manuscript's own code
(SchwingNet/tools/fig_power.py: panel_a, style, Wilson) at slide type sizes, with the transitional persons the whole
CT census should supply marked on its n-axis; (2) a pictogram of those persons by class, one square per five
persons (Greg 2026-09-26: "use the exact power chart from the supplementals with the n = estimated if I screen the
entire CT corpus ... just visually represent the quantity of each ... mostly figure"). Writes into figs_v2/.

Whole-census expectations (spinesurg-ct-nnunet/docs/CENSUS_TABLE_2026-09-25.md, sections 1 + 2 + 3): L6 322 + 5 +
543 = 870; four lumbar 161 + 2 + 272 = 435; T13 38-119 + 130-405 + 203-633 = 371-1,157 (midpoint 764); Castellvi
II-IV 907-1,813 + 13-26 + 1,528-3,056 = 2,448-4,895 (midpoint 3,672; it includes the L6 and four-lumbar persons).

    python paper/cns2026/prep_v7_figs.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
sys.path.insert(0, str(SN / "tools"))
import fig_power as fp  # noqa: E402  (the manuscript's Figure 5 tool)

NAVY, BLUE, PALE, RED, GOLD, GREY = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#9A9A9A"
CENSUS = {"L6": (322, 870), "four lumbar": (161, 435), "T13": (78, 764), "Castellvi II-IV": (1360, 3672)}   # (screened, whole census)
TODAY = {"real-frame candidates": 7, "L6 called by both labellers": 21}


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size)


# ------------------------------------------------------------ 1. Figure 5a by the manuscript's code, slide type sizes
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial"]
plt.rcParams["axes.unicode_minus"] = True
fp.FS = 18.0                      # the manuscript prints at 12 pt; the slide needs more
fig, ax = plt.subplots(figsize=(15.0, 6.9))
info = fp.panel_a(ax, 90.0, 85.0)
for line in ax.get_lines():       # the manuscript's 1.6 pt curves, thickened for the room
    if line.get_linestyle() == "-" and len(line.get_xdata()) > 10:
        line.set_linewidth(2.8)
for line in ax.get_lines():
    if len(line.get_xdata()) == 1:
        line.set_markersize(11)
leg = ax.get_legend()
leg._set_loc(8)                   # lower centre, under the curves; the census labels take the lower right
leg.set_bbox_to_anchor((0.42, 0.0))
for h in leg.legend_handles:
    try:
        h.set_linewidth(2.8)
        h.set_markersize(11)
    except AttributeError:
        pass
ax.set_xlabel("transitional test persons, n", fontsize=20, color=fp.INK)
ax.set_ylabel("95 % lower bound on exact naming, %", fontsize=20, color=fp.INK)
ax.tick_params(labelsize=17)

# today, on real exposures
n7 = TODAY["real-frame candidates"]
y7 = fp.wilson(n7, n7)[0] * 100
ax.plot([n7], [y7], "v", ms=14, color=RED, mec="white", mew=1.2, zorder=6)
ax.annotate(f"today: {n7} candidates with a real frame, {y7:.0f} %", xy=(n7, y7), xytext=(12, -6), textcoords="offset points",
            ha="left", va="top", fontsize=16, color=RED)
n21 = TODAY["L6 called by both labellers"]
y21 = fp.wilson(n21, n21)[0] * 100
ax.plot([n21], [y21], "*", ms=20, color=NAVY, mec="white", mew=1.0, zorder=6)

# the whole census, on the zero-error curve, labels stacked in the empty lower right
stack = [("Castellvi II–IV", 3672, BLUE, "D"), ("T13", CENSUS["T13"][1], GOLD, "o"),
         ("L6", CENSUS["L6"][1], NAVY, "o"), ("four lumbar", CENSUS["four lumbar"][1], BLUE, "o"),
         ("L6 called by both labellers so far", n21, NAVY, "*")]
ytxt = 80
for name, n, col, mk in stack:
    n_plot = min(n, 1000)
    y = fp.wilson(n_plot, n_plot)[0] * 100
    if n <= 1000:
        ax.plot([n], [y], mk, ms=20 if mk == "*" else 13, color=col, mec="white", mew=1.2, zorder=6)
        txt = f"{name}: ≈ {n:,} persons, {y:.1f} %" if mk != "*" else f"{n} {name}: {y:.1f} %"
    else:
        ax.annotate("", xy=(1000, y), xytext=(760, y), arrowprops=dict(arrowstyle="->", color=col, lw=2.2), zorder=6)
        txt = f"{name}: ≈ {n:,} persons, beyond the axis"
    ax.annotate(txt, xy=(n_plot, y), xytext=(120, ytxt), textcoords="data", ha="left", va="center", fontsize=16, color=col,
                arrowprops=dict(arrowstyle="-", color=col, lw=0.9, shrinkA=0, shrinkB=5), zorder=7)
    ytxt -= 6.5
ax.text(120, 82.5, "if the whole CT census is screened", fontsize=15, color=fp.SOFT, ha="left", va="bottom")
fig.tight_layout()
save(fig, "chart_fig5a_census.png")

# ------------------------------------------------------------ 2. the quantities as a pictogram, one square = 5 persons
PER = 5
COLS = 50
rows = [("sixth lumbar (L6)", CENSUS["L6"], NAVY),
        ("four lumbar (sacralised L5)", CENSUS["four lumbar"], BLUE),
        ("thirteenth thoracic (T13)", CENSUS["T13"], GOLD),
        ("any lumbosacral transitional, Castellvi II–IV\n(includes the two lumbar classes above)", CENSUS["Castellvi II-IV"], "#8A93B8")]
fig, ax = plt.subplots(figsize=(13.0, 7.4))
ax.set_axis_off()
y = 0
gap = 1.6
for name, (scr, tot), col in rows:
    n_sq = round(tot / PER)
    n_scr = round(scr / PER)
    nrows = -(-n_sq // COLS)
    for i in range(n_sq):
        r, c = divmod(i, COLS)
        face = col if i < n_scr else "white"
        edge = col
        if name.startswith("sixth") and i < round(21 / PER):
            face, edge = RED, RED
        ax.add_patch(Rectangle((c, -(y + r) - 1), 0.85, 0.85, facecolor=face, edgecolor=edge, lw=0.9))
    ax.text(-1.2, -(y + nrows / 2) - 0.5, f"≈ {tot:,}", ha="right", va="center", fontsize=30, fontweight="bold", color=col)
    ax.text(COLS + 1.0, -(y + nrows / 2) - 0.5, name, ha="left", va="center", fontsize=17, color=NAVY)
    if name.startswith("sixth"):
        ax.plot([0, 35 / PER], [-(y) + 0.35, -(y) + 0.35], color=RED, lw=3)
        ax.text(35 / PER / 2, -(y) + 0.55, "35: the zero-error test", ha="center", va="bottom", fontsize=15, color=RED)
    y += nrows + gap
ax.set_xlim(-14, COLS + 24)
ax.set_ylim(-(y) - 0.5, 2.2)
ax.text(-14, -(y) - 0.2,
        "one square, five persons  ·  filled, from the 16,898 CTs being screened  ·  open, from the five collections under agreement  ·  "
        "red, the 21 L6 both labellers have called",
        ha="left", va="top", fontsize=14, color=fp.SOFT)
fig.tight_layout()
save(fig, "pictogram_census.png")
print("done")
