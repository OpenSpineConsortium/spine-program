"""paper/cns2026/prep_v16_public_figs.py — charts for the disclosure-safe CNS deck (v11_public), drawn ONLY from the
public NeurIPS 2026 camera-ready (OpenReview, public since 24 Sep 2026). Every number is typed once below with its
table, and asserted to appear verbatim in the camera-ready's extracted text, so nothing is transcribed wrong.

  chart_pub_levels.png    per-level Dice of the unmodified whole-body segmenter by phenotype (Table 1), lines
  chart_pub_castellvi.png Castellvi consensus grades of the 33 transitional patients (Table 4), donut
  chart_pub_gain.png      segmenter vs released model: sacrum and junction Dice (Results; Table 6), slope lines
  chart_pub_l6.png        unmerged control: share of true-L6 voxels called L5, four folds (Section 8.1), dots

    python paper/cns2026/prep_v16_public_figs.py
"""
import json
from pathlib import Path

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_public"
OUT.mkdir(exist_ok=True)
PDF = HERE.parent.parent / "CAMERA_READY_NEURIPS" / "src" / "neurips_2026.pdf"  # the camera-ready as committed (38b0cb9)
TEXT = "\n".join(p.get_text() for p in fitz.open(PDF))

NAVY, BLUE, RED, GOLD, GREY, INK = "#191D63", "#4C70B7", "#EF4627", "#E0A800", "#8A8A8A", "#191D63"
plt.rcParams.update({"font.family": "Arial", "font.size": 20, "axes.edgecolor": "#BFBFBF", "axes.linewidth": 1.0,
                     "xtick.color": INK, "ytick.color": INK, "figure.dpi": 220, "savefig.dpi": 220})

N = {  # value strings exactly as printed in the camera-ready
    "table1": {"Normal": {"n": "768", "L": ["0.921", "0.918", "0.929", "0.936", "0.938"], "jxn": "0.824"},
               "Lumbarization": {"n": "14", "L": ["0.878", "0.853", "0.690", "0.388", "0.291"], "jxn": "0.357"},
               "Sacralization (count-style)": {"n": "9", "L": ["0.265", "0.100", "0.055", "0.001", "0.000"], "jxn": "0.697"},
               "Any LSTV": {"n": "33", "jxn": "0.534"}, "L6_emit": "0 / 1152"},
    "table4_total": {"Ib": 2, "IIa": 4, "IIb": 6, "IIIa": 1, "IIIb": 16, "IV": 4, "Total": 33},
    "kappa": "κ=0.74", "records": "1,153", "patients": "802",
    "gain": {"sacrum_ts": "0.817", "sacrum_ours": "0.969", "jxn_ts": "0.357", "jxn_ours": "0.946"},
    "l6_to_l5_folds": ["83%", "65%", "66%", "97%"], "l6_dice": "0.01–0.13", "l5_dice": "0.91–0.95",
}
for s in ["0.921", "0.878", "0.265", "0.824", "0.534", "0.357", "0.697", "0 / 1152", "0.817", "0.969", "0.946", "0.01–0.13", "0.91–0.95", "κ=0.74", "1,153"]:
    assert s in TEXT, s
assert "83%, 65%, 66% and 97%" in TEXT
for row in ("Normal", "Lumbarization", "Sacralization (count-style)"):
    for v in N["table1"][row]["L"]:
        assert v in TEXT, (row, v)
json.dump(N, open(OUT / "public_numbers.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def save(fig, name):
    fig.savefig(OUT / name, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print("  ", name)


# ---- per-level Dice by phenotype (Table 1), lines
fig, ax = plt.subplots(figsize=(9.2, 5.6))
x = range(5)
for (row, col, mk) in (("Normal", NAVY, "o"), ("Lumbarization", RED, "s"), ("Sacralization (count-style)", GOLD, "^")):
    ys = [float(v) for v in N["table1"][row]["L"]]
    ax.plot(x, ys, color=col, lw=3.5, marker=mk, ms=12, label=f"{row.replace(' (count-style)', ', count')} (n = {N['table1'][row]['n']})")
ax.set_xticks(list(x)); ax.set_xticklabels(["L1", "L2", "L3", "L4", "L5"], fontsize=22)
ax.set_ylim(-0.03, 1.03); ax.set_ylabel("Dice, whole-body segmenter", fontsize=20)
ax.grid(axis="both", color="#DDDDDD", lw=0.9); ax.set_axisbelow(True)
for sd in ("top", "right"):
    ax.spines[sd].set_visible(False)
ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.55), fontsize=17, frameon=False)
save(fig, "chart_pub_levels.png")

# ---- Castellvi consensus (Table 4), donut
t4 = N["table4_total"]
labels = [k for k in ("Ib", "IIa", "IIb", "IIIa", "IIIb", "IV")]
vals = [t4[k] for k in labels]
cols = ["#C9D4EC", "#9CB1DB", BLUE, "#F5B7A6", RED, NAVY]
fig, ax = plt.subplots(figsize=(6.6, 6.6))
w, _ = ax.pie(vals, colors=cols, startangle=90, counterclock=False, wedgeprops=dict(width=0.36, edgecolor="white", linewidth=2))
for wedge, lab, v in zip(w, labels, vals):
    import math
    ang = math.radians((wedge.theta1 + wedge.theta2) / 2)
    r = 1.22
    ax.text(r * math.cos(ang), r * math.sin(ang), f"{lab}\n{v}", ha="center", va="center", fontsize=19, color=INK, fontweight="bold" if v >= 10 else "normal")
ax.text(0, 0.08, str(t4["Total"]), ha="center", va="center", fontsize=44, fontweight="bold", color=NAVY)
ax.text(0, -0.22, "transitional\npatients", ha="center", va="center", fontsize=17, color=INK, linespacing=1.1)
ax.set_aspect("equal")
save(fig, "chart_pub_castellvi.png")

# ---- the released segmenter against the whole-body one: slope lines
g = N["gain"]
fig, ax = plt.subplots(figsize=(7.6, 5.6))
for (lab, a, b, col, dy) in (("sacrum", g["sacrum_ts"], g["sacrum_ours"], NAVY, 0.045), ("lumbosacral junction,\nlumbarization", g["jxn_ts"], g["jxn_ours"], RED, -0.075)):
    ax.plot([0, 1], [float(a), float(b)], color=col, lw=4, marker="o", ms=14)
    ax.text(-0.06, float(a), a, ha="right", va="center", fontsize=20, color=col, fontweight="bold")
    ax.text(1.08, float(b) + dy, f"{b}  {lab}", ha="left", va="center", fontsize=18, color=col, fontweight="bold", linespacing=1.05)
ax.set_xlim(-0.45, 2.3); ax.set_ylim(0.25, 1.06)
ax.set_xticks([0, 1]); ax.set_xticklabels(["whole-body\nsegmenter", "released\nspinopelvic model"], fontsize=18)
ax.set_ylabel("Dice", fontsize=20); ax.grid(axis="y", color="#DDDDDD", lw=0.9); ax.set_axisbelow(True)
for sd in ("top", "right"):
    ax.spines[sd].set_visible(False)
save(fig, "chart_pub_gain.png")

# ---- the unmerged control: true-L6 voxels called L5, four folds
v = [float(s.rstrip("%")) for s in N["l6_to_l5_folds"]]
fig, ax = plt.subplots(figsize=(7.2, 5.4))
ax.scatter(range(1, 5), v, s=420, color=RED, edgecolor="white", linewidth=2, zorder=3)
for i, y in enumerate(v, 1):
    ax.text(i, y + 5, f"{y:.0f} %", ha="center", va="bottom", fontsize=20, color=INK, fontweight="bold")
ax.set_xticks(range(1, 5)); ax.set_xticklabels([""] * 4); ax.set_xlim(0.4, 4.6)
ax.set_xlabel("the four folds with a lumbarization case in validation", fontsize=17)
ax.set_ylim(0, 112); ax.set_ylabel("true L6 voxels called L5", fontsize=19)
ax.grid(axis="both", color="#DDDDDD", lw=0.9); ax.set_axisbelow(True)
for sd in ("top", "right"):
    ax.spines[sd].set_visible(False)
save(fig, "chart_pub_l6.png")
print("public numbers verified against the camera-ready text")
