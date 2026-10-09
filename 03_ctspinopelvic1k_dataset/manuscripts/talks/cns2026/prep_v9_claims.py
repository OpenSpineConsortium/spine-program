"""paper/cns2026/prep_v9_claims.py — what the whole census would let the talk claim (Greg 2026-09-26: "sum the
expected number of classes across all datasets and give me a few error rates and power thresholds to show what I
should be able to say, and hopefully outperform the surgeon-assisted LevelCheck"; then "only display the n for the
sums and the power rates and the relation to LevelCheck with good clear explanation").

For each class sum across the whole census (CENSUS_TABLE sections 1+2+3) the Wilson 95 % lower bound (the
manuscript's wilson() from SchwingNet/tools/fig_power.py) at 0, 1, 2, 3 and 5 % errors, and the errors the sum can
absorb while the bound stays above the surgeon-assisted overlay's 97.6 % (Manbachi 2018) and above the pre-stated
90 %. Writes figs_v2/table_claims.png and figs_v2/claims.json (the deck's explanation sentences read it).

    python paper/cns2026/prep_v9_claims.py
"""
import json
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
from fig_power import wilson  # noqa: E402

NAVY, BLUE, RED, GOLD, GREY, INK, LIGHT = "#191D63", "#4C70B7", "#EF4627", "#E0A800", "#8A8A8A", "#191D63", "#EEF1F8"
GREEN = "#2E8B57"
plt.rcParams["font.family"] = "Arial"
LEVELCHECK = 97.6
TARGET = 90.0


def lb(n, k):
    return wilson(n - k, n)[0] * 100


def errors_allowed(n, thr):
    k = 0
    while k < n and lb(n, k + 1) >= thr:
        k += 1
    return k


rows = [  # (label, sub, n)
    ("sixth lumbar (L6)", "3.2 % of scans with the junction in view", 870),
    ("four lumbar (sacralised L5)", "1.6 %", 435),
    ("thirteenth thoracic (T13)", "0.64–2.0 % of scans with the rib cage in view; midpoint of 371–1,157", 764),
    ("all three classes together", "", 2069),
    ("Castellvi II–IV, any lumbosacral", "9–18 %; midpoint of 2,448–4,895; includes the L6 and four-lumbar persons", 3672),
]
rates = [0.0, 0.01, 0.02, 0.03, 0.05]
W = 13.6
RH = 0.66
HEAD = 1.1
H = HEAD + RH * len(rows) + 0.15
fig = plt.figure(figsize=(W + 0.4, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-0.2, W + 0.2)
ax.set_ylim(-H + 0.15, 0.15)
ax.set_axis_off()

cols_x = [5.35, 6.55, 7.75, 8.95, 10.15]
cw = 1.2
ax.add_patch(Rectangle((0, -HEAD), W, HEAD, facecolor=NAVY, edgecolor="none"))
ax.text(0.15, -0.3, "persons the whole census should hold", ha="left", va="center", fontsize=15, fontweight="bold", color="white")
ax.text(0.15, -0.72, "transitional class", ha="left", va="center", fontsize=14, color="white")
ax.text(4.55, -0.82, "n", ha="right", va="center", fontsize=17, fontweight="bold", color="white")
ax.text(cols_x[2], -0.3, "lowest accuracy the data would still support (95 %) if the network erred on", ha="center", va="center", fontsize=14, color="white")
for x, r in zip(cols_x, rates):
    ax.text(x, -0.8, f"{r * 100:.0f} %" if r else "none", ha="center", va="center", fontsize=17, fontweight="bold", color="white")
ax.text(12.35, -0.3, "errors allowed to still beat", ha="center", va="center", fontsize=14, color="white")
ax.text(11.75, -0.8, f"{LEVELCHECK} %", ha="center", va="center", fontsize=17, fontweight="bold", color=GOLD)
ax.text(12.95, -0.8, f"{TARGET:.0f} %", ha="center", va="center", fontsize=17, fontweight="bold", color="white")
ax.plot([cols_x[0] - cw / 2, cols_x[-1] + cw / 2], [-0.53, -0.53], color="white", lw=1)
ax.plot([11.2, 13.5], [-0.53, -0.53], color="white", lw=1)

out = {"levelcheck_pct": LEVELCHECK, "target_pct": TARGET, "rows": []}
y = -HEAD
for i, (lab, sub, n) in enumerate(rows):
    y -= RH
    if i % 2 == 0:
        ax.add_patch(Rectangle((0, y), W, RH, facecolor="#F7F8FB", edgecolor="none"))
    if lab.startswith("all three"):
        ax.plot([0, W], [y + RH, y + RH], color=NAVY, lw=1.0)
    yc = y + RH / 2
    ax.text(0.15, yc + (0.11 if sub else 0), lab, ha="left", va="center", fontsize=16, fontweight="bold" if lab.startswith("all") else "normal", color=INK)
    if sub:
        ax.text(0.15, yc - 0.16, sub, ha="left", va="center", fontsize=10.5, color=GREY)
    ax.text(4.55, yc, f"{n:,}", ha="right", va="center", fontsize=18, fontweight="bold", color=INK)
    cells = []
    for x, r in zip(cols_x, rates):
        k = round(n * r)
        v = lb(n, k)
        col = GREEN if v >= LEVELCHECK else (BLUE if v >= TARGET else GREY)
        if col != GREY:
            ax.add_patch(Rectangle((x - cw / 2 + 0.05, y + 0.06), cw - 0.1, RH - 0.12, facecolor=col, alpha=0.14, edgecolor="none"))
        ax.text(x, yc + 0.1, f"{v:.1f}", ha="center", va="center", fontsize=16, fontweight="bold", color=col)
        ax.text(x, yc - 0.18, f"{k} error{'' if k == 1 else 's'}", ha="center", va="center", fontsize=9.5, color=GREY)
        cells.append({"rate": r, "errors": k, "lower_bound_pct": round(v, 2)})
    e97 = errors_allowed(n, LEVELCHECK)
    e90 = errors_allowed(n, TARGET)
    ax.text(11.75, yc + 0.1, f"{e97}", ha="center", va="center", fontsize=18, fontweight="bold", color=GREEN if e97 else RED)
    ax.text(11.75, yc - 0.18, f"({e97 / n * 100:.1f} %)", ha="center", va="center", fontsize=9.5, color=GREY)
    ax.text(12.95, yc + 0.1, f"{e90}", ha="center", va="center", fontsize=18, fontweight="bold", color=INK)
    ax.text(12.95, yc - 0.18, f"({e90 / n * 100:.1f} %)", ha="center", va="center", fontsize=9.5, color=GREY)
    out["rows"].append({"label": lab, "n": n, "cells": cells, "errors_allowed_levelcheck": e97, "errors_allowed_target": e90})
fig.savefig(OUT / "table_claims.png", dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
# context numbers the slide's sentences quote
out["today"] = {"n": 7, "lower_bound_pct": round(lb(7, 0), 1)}
out["screened_now_L6"] = {"n": 322, "lower_bound_pct": round(lb(322, 0), 1), "errors_allowed_levelcheck": errors_allowed(322, LEVELCHECK),
                          "errors_allowed_target": errors_allowed(322, TARGET)}
out["n_zero_error_for_levelcheck"] = next(n for n in range(1, 5000) if lb(n, 0) >= LEVELCHECK)
json.dump(out, open(OUT / "claims.json", "w"), indent=1)
with Image.open(OUT / "table_claims.png") as im:
    print("table_claims", im.size)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}))
for r in out["rows"]:
    print(r["label"], r["n"], "allow>97.6:", r["errors_allowed_levelcheck"], "allow>90:", r["errors_allowed_target"])
