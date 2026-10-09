"""paper/cns2026/prep_v6_figs.py — two figures for deck v6 (Greg 2026-09-26): (1) the power chart with the census's
projected transitional persons placed on its n-axis, so one figure says what a test needs and what the corpus should
supply; (2) a map of the CT census itself: every collection by size and by the share of scans with the lumbosacral
junction in view, the bubble sized by the transitional persons it should hold.

Power curves: SchwingNet/results/power/power.json#panel_a (Wilson 95 % lower bound against n at 0, 1, 2 and 5
errors), the arrays Figure 5a draws. Census: spinesurg-ct-nnunet/docs/CENSUS_TABLE_2026-09-25.md (expected persons =
CTs with both lumbosacral references in view x published prevalence: L6 3.2 %, four lumbar 1.6 %, Castellvi II-IV
9-18 %; T13 = CTs with the rib cage in view x 0.64-2.0 %). Writes into figs_v2/.

    python paper/cns2026/prep_v6_figs.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"

NAVY, BLUE, PALE, RED, GOLD, GREY, INK = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#9A9A9A", "#191D63"
plt.rcParams.update({"font.family": "Arial", "font.size": 17, "axes.labelsize": 18, "xtick.labelsize": 16, "ytick.labelsize": 16,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#DDDDDD",
                     "figure.dpi": 220, "savefig.dpi": 220, "savefig.facecolor": "white"})


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size)


# ------------------------------------------------------------------ 1. power chart with the projections on its n-axis
p = json.load(open(SN / "results" / "power" / "power.json"))
curves = p["panel_a"]["curves"]


def lb_at(n, k="0"):
    ns = curves[k]["n"]
    i = min(range(len(ns)), key=lambda j: abs(ns[j] - n))
    return curves[k]["lower_bound_pct"][i]


fig, ax = plt.subplots(figsize=(13.0, 7.0))
shades = {"0": INK, "1": "#4A4F6E", "2": "#7A7F96", "5": "#A9ADBD"}
for k, lab in (("0", "no error"), ("1", "1 error"), ("2", "2 errors"), ("5", "5 errors")):
    ax.plot(curves[k]["n"], curves[k]["lower_bound_pct"], color=shades[k], lw=2.6 if k == "0" else 1.8, label=lab, zorder=2)
ax.axhline(90, color=RED, ls="--", lw=1.6, zorder=1)
ax.axhline(85, color=RED, ls=":", lw=1.6, zorder=1)
ax.text(2900, 90.5, "90 % target: 35 persons at zero errors", color=RED, fontsize=14, va="bottom", ha="right")
ax.text(2900, 85.5, "85 % target: 22 carriers at zero errors", color=RED, fontsize=14, va="bottom", ha="right")

# today, on real exposures (labels beside the points, lower left is empty)
for n, lab, dx, dy, va in ((7, "7 real-frame candidates today", 10, -4, "top"), (3, "3 L6 scored, cross-validation only", 10, -4, "top")):
    y = lb_at(n)
    ax.plot([n], [y], marker="v", ms=12, color=RED, markeredgecolor="white", markeredgewidth=1.2, zorder=5)
    ax.annotate(f"{lab}: {y:.1f} %", xy=(n, y), xytext=(dx, dy), textcoords="offset points", ha="left", va=va, fontsize=12.5, color=RED)

# the census, projected: a stacked list in the empty lower right with a leader to each point
stack = [(865, "L6 with the five gated collections", NAVY, "D"),
         (322, "L6 expected from the screened CTs", NAVY, "o"),
         (161, "four lumbar expected", BLUE, "o"),
         (78, "T13 expected (38–119)", GOLD, "o"),
         (21, "21 L6 called by both labellers so far", NAVY, "*")]
x_text = 190
y0 = 78
for i, (n, lab, col, mk) in enumerate(stack):
    y = lb_at(n)
    yt = y0 - 5.5 * i
    ax.plot([n], [y], marker=mk, ms=18 if mk == "*" else 12, color=col, markeredgecolor="white", markeredgewidth=1.2, zorder=5)
    ax.annotate(f"{lab}: {y:.1f} %", xy=(n, y), xytext=(x_text, yt), textcoords="data", ha="left", va="center",
                fontsize=13, color=col, arrowprops=dict(arrowstyle="-", color=col, lw=0.9, shrinkA=0, shrinkB=4), zorder=6)
ax.axvspan(907, 1813, color=PALE, alpha=0.6, zorder=0)
ax.text(1280, 41.5, "Castellvi II–IV expected\nfrom the screened CTs:\n907–1,813", ha="center", va="bottom", fontsize=12.5, color=BLUE)
ax.set_xscale("log")
ax.set_xlim(3, 3000)
ax.set_ylim(40, 100.5)
ax.set_xticks([3, 10, 30, 100, 300, 1000, 3000])
ax.set_xticklabels(["3", "10", "30", "100", "300", "1,000", "3,000"])
ax.set_xlabel("transitional test persons, n")
ax.set_ylabel("95 % lower bound on exact naming, %")
ax.legend(loc="upper left", frameon=False, fontsize=14, title="errors among the n", title_fontsize=13)
fig.tight_layout()
save(fig, "chart_power_with_census.png")

# ------------------------------------------------------------------ 2. the census as a map of collections
# (name, CTs on disk, expected L6, expected four-lumbar, expected T13 midpoint, status); share in view = L6 / 0.032 / CTs
screened = [("AbdomenAtlas", 7650, 144, 72, 39.0, "run"), ("IDC tier 1", 3500, 62, 31, 23.5, "run"), ("FDG-PET-CT", 901, 19, 10, 8.4, "run"),
            ("AMOS22", 724, 19, 9, 0, "done"), ("PANORAMA", 2026, 52, 26, 0, "run"), ("NLST pilot", 501, 0, 0, 4.6, "done"),
            ("WAW-TACE", 229, 6, 3, 0, "run"), ("Kidney", 216, 4, 2, 1.3, "run"), ("Barts CRL", 213, 5, 3, 0, "run"),
            ("PENGWIN", 341, 1, 1, 0, "done"), ("CTPelvic1K", 173, 1, 0, 0, "done"), ("CURVAS-PDAC", 102, 3, 1, 0, "done"),
            ("CURVAS", 71, 2, 1, 0, "done"), ("TS v2 val", 71, 2, 1, 0.4, "done"), ("AortaSeg60", 56, 1, 1, 0.6, "done"),
            ("Deep-PSMA", 54, 1, 1, 0.5, "done"), ("QUADRA-HC", 49, 1, 1, 0.45, "done"), ("CSI 2014", 21, 0, 0, 0.05, "done")]
gated = [("Merlin", 18317, 447, 224, 4.5, 0.763), ("RATIC trauma", 3147, 80, 40, 33, 0.794), ("CADS", 753, 16, 8, 7, 0.665),
         ("CT-RATE", 21304, 0, 0, 196, 0.0), ("INSPECT", 19402, 0, 0, 178, 0.0)]
# label placement: (dx points, dy points, ha, va); default above the bubble
place = {"PANORAMA": (-10, 0, "right", "center"), "RATIC trauma": (12, 4, "left", "bottom"), "CADS": (-10, -2, "right", "top"),
         "FDG-PET-CT": (10, 2, "left", "bottom"), "CT-RATE": (0, 14, "center", "bottom"), "INSPECT": (0, -16, "center", "top"),
         "CURVAS": (-8, 0, "right", "center"), "TS v2 val": (8, 0, "left", "center"), "CURVAS-PDAC": (0, 8, "center", "bottom"),
         "Deep-PSMA": (-8, 2, "right", "bottom"), "AortaSeg60": (8, -2, "left", "top"), "Kidney": (0, 8, "center", "bottom"),
         "QUADRA-HC": (0, 8, "center", "bottom"), "CTPelvic1K": (-8, 0, "right", "center"), "PENGWIN": (8, 0, "left", "center"),
         "NLST pilot": (8, 0, "left", "center"), "CSI 2014": (8, 0, "left", "center"), "Merlin": (0, 0, "center", "center"),
         "AbdomenAtlas": (0, 6, "center", "bottom"), "IDC tier 1": (0, -6, "center", "top"), "INSPECT": (10, -4, "left", "top")}
inside = {"AbdomenAtlas", "IDC tier 1", "Merlin"}      # the expected count printed inside these bubbles
fig, ax = plt.subplots(figsize=(13.0, 7.2))
col = {"done": NAVY, "run": BLUE}
K = 4.5
for name, cts, l6, four, t13, st in screened:
    share = min(1.0, l6 / 0.032 / cts) * 100 if l6 else 0.0
    if name == "CSI 2014":
        share = 29
    tot = l6 + four + t13
    s_ = max(40, tot * K)
    ax.scatter([cts], [share], s=s_, color=col[st], alpha=0.8, edgecolor="white", lw=1.2, zorder=3)
    dx, dy, ha, va = place.get(name, (0, 6, "center", "bottom"))
    r = (s_ ** 0.5) / 2
    if name in inside:
        ax.annotate(f"{tot:.0f}", (cts, share), ha="center", va="center", fontsize=11, color="white", zorder=4)
    ax.annotate(name, (cts, share), xytext=(dx + (r if ha == "left" else -r if ha == "right" else 0), dy + (r if va == "bottom" else -r if va == "top" else 0)),
                textcoords="offset points", ha=ha, va=va, fontsize=11.5, color=INK, zorder=4)
for name, cts, l6, four, t13, pin in gated:
    tot = l6 + four + t13
    s_ = max(40, tot * K)
    ax.scatter([cts], [pin * 100], s=s_, facecolor="none", edgecolor=GREY, lw=2.2, zorder=3)
    dx, dy, ha, va = place.get(name, (0, 6, "center", "bottom"))
    r = (s_ ** 0.5) / 2
    if name in inside:
        ax.annotate(f"{name}\n{tot:.0f}", (cts, pin * 100), ha="center", va="center", fontsize=10.5, color=GREY, zorder=4)
    else:
        ax.annotate(name, (cts, pin * 100), xytext=(dx + (r if ha == "left" else -r if ha == "right" else 0), dy + (r if va == "bottom" else -r if va == "top" else 0)),
                    textcoords="offset points", ha=ha, va=va, fontsize=11.5, color=GREY, zorder=4)
handles = [Line2D([], [], marker="o", ls="", ms=11, color=NAVY, label="screened, calls made"),
           Line2D([], [], marker="o", ls="", ms=11, color=BLUE, label="screening now"),
           Line2D([], [], marker="o", ls="", ms=11, markerfacecolor="none", markeredgecolor=GREY, markeredgewidth=2, label="under agreement")]
ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=13,
          title="bubble area: expected transitional persons\n(L6 + four lumbar + T13); number inside the largest", title_fontsize=12)
ax.set_xscale("log")
ax.set_xlim(12, 60000)
ax.set_ylim(-8, 104)
ax.set_xticks([10, 100, 1000, 10000])
ax.set_xticklabels(["10", "100", "1,000", "10,000"])
ax.set_xlabel("CT scans in the collection")
ax.set_ylabel("scans with the lumbosacral junction in view, %")
fig.tight_layout()
save(fig, "chart_census_map.png")
print("done")
