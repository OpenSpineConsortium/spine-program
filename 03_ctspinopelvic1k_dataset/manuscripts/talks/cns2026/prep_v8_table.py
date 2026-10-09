"""paper/cns2026/prep_v8_table.py — the CT census as one rendered table (Greg 2026-09-26: "render all the CT databases'
names, their n's, the predicted number of each class needed for a few of the error rates calculated in the power
graph, and the estimated number based on the prevalence; make it pretty; drop the power chart").

Rows: the collections being screened (the twelve small ones grouped, every name printed), their sum, the planned
chest tier as one row, the five gated collections, their sum, the whole census. Columns: CTs on disk and the persons
each class should hold (scans with the junction in view x prevalence: L6 3.2 %, four lumbar 1.6 %, Castellvi II-IV
9-18 %; T13 = rib cage in view x 0.64-2.0 %). Foot: the persons a test needs from the power chart (Wilson lower
bound, SchwingNet/results/power/power.json#panel_a/crossings_n). Source: docs/CENSUS_TABLE_2026-09-25.md.

    python paper/cns2026/prep_v8_table.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"

NAVY, BLUE, PALE, RED, GOLD, GREY, INK, LIGHT = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#8A8A8A", "#191D63", "#EEF1F8"
CAST = "#8A93B8"
plt.rcParams["font.family"] = "Arial"

cross = json.load(open(SN / "results" / "power" / "power.json"))["panel_a"]["crossings_n"]
need90 = [cross[k]["n_lower_bound_ge_90"] for k in ("0", "1", "2", "5")]
need85 = [cross[k]["n_lower_bound_ge_85"] for k in ("0", "1", "2", "5")]

# (name, sub-line, CTs, L6, four lumbar, T13 range, Castellvi range, kind)
rows = [
    ("AbdomenAtlas 3.0 Mini", "abdomen, a third reaching T1", 7650, 144, 72, "19–59", "406–813", "run"),
    ("IDC tier 1", "39 collections: chest, abdomen, pelvis, whole body", 3500, 62, 31, "11–36", "173–346", "run"),
    ("PANORAMA", "pancreas CT", 2026, 52, 26, "0", "146–292", "run"),
    ("TCIA FDG-PET-CT-Lesions", "whole body", 901, 19, 10, "4–13", "54–108", "run"),
    ("AMOS22", "abdomen; 9 L6 called by both labellers", 724, 19, 9, "0", "52–104", "done"),
    ("Twelve smaller collections", "NLST pilot, PENGWIN, WAW-TACE, Kidney, Barts CRL, CTPelvic1K, CURVAS-PDAC, CURVAS, TotalSegmentator val, AortaSeg60, Deep-PSMA, QUADRA-HC, CSI 2014",
     1897, 26, 13, "4–12", "76–152", "mixed"),
    ("Screened now", "22 collections, two automatic labellers per scan; 21 L6 called by both so far", 16898, 322, 161, "38–119", "907–1,813", "sum"),
    ("Chest tier, planned", "NLST, STOIC, LIDC-IDRI, RibFrac, NSCLC, CPTAC, MIDRC and others: T13 is the only yield", 29479, 5, 2, "130–405", "13–26", "plan"),
    ("Merlin", "abdominopelvic; one research agreement", 18317, 447, 224, "2–7", "1,258–2,516", "gate"),
    ("RATIC abdominal trauma", "chest, abdomen, pelvis", 3147, 80, 40, "16–50", "225–450", "gate"),
    ("CT-RATE", "chest", 21304, 0, 0, "95–297", "0", "gate"),
    ("INSPECT", "chest", 19402, 0, 0, "86–270", "0", "gate"),
    ("CADS", "whole body", 753, 16, 8, "3–11", "45–90", "gate"),
    ("Under agreement", "five collections, a form each", 62923, 543, 272, "203–633", "1,528–3,056", "sum"),
    ("Whole census", "", 109300, 870, 435, "371–1,157", "2,448–4,895", "total"),
]
cols = [("collection", 0.0, 4.9, "left"), ("CT scans", 4.9, 1.35, "right"), ("L6", 6.3, 1.1, "right"), ("four lumbar", 7.4, 1.35, "right"),
        ("T13", 8.75, 1.35, "right"), ("Castellvi II–IV", 10.1, 1.75, "right"), ("status", 11.9, 1.6, "left")]
W = 13.6
RH = 0.42
HEAD = 0.95
FOOT = 0.0            # the test-size band moved to its own slide (prep_v9_claims.py)
H = HEAD + RH * len(rows) + FOOT + 0.1
fig = plt.figure(figsize=(W + 0.4, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-0.2, W + 0.2)
ax.set_ylim(-H + 0.15, 0.15)
ax.set_axis_off()

# header band
ax.add_patch(Rectangle((0, -HEAD), W, HEAD, facecolor=NAVY, edgecolor="none"))
ax.text(6.3 + (10.1 + 1.75 - 6.3) / 2, -0.26, "persons each class should hold (from prevalence)", ha="center", va="center", fontsize=14, color="white")
for name, x, w, al in cols:
    tx = x + 0.12 if al == "left" else x + w - 0.12
    ax.text(tx, -HEAD + 0.28, name, ha=al, va="center", fontsize=16, fontweight="bold", color="white")
ax.plot([6.35, 11.8], [-0.52, -0.52], color="white", lw=1)

status_txt = {"run": ("●", BLUE, "screening"), "done": ("●", NAVY, "called"), "mixed": ("●", NAVY, "called or screening"),
              "plan": ("○", GREY, "planned"), "gate": ("○", GREY, "agreement pending"), "sum": ("", INK, ""), "total": ("", INK, "")}
y = -HEAD
for i, (name, sub, cts, l6, four, t13, cast, kind) in enumerate(rows):
    y -= RH
    if kind in ("sum", "total"):
        ax.add_patch(Rectangle((0, y), W, RH, facecolor=LIGHT if kind == "sum" else PALE, edgecolor="none"))
        ax.plot([0, W], [y + RH, y + RH], color=NAVY, lw=1.2)
    elif i % 2 == 0:
        ax.add_patch(Rectangle((0, y), W, RH, facecolor="#F7F8FB", edgecolor="none"))
    bold = kind in ("sum", "total")
    fs = 15 if not bold else 16
    yc = y + RH / 2
    if sub:
        ax.text(0.12, yc + 0.07, name, ha="left", va="center", fontsize=fs, fontweight="bold" if bold else "normal", color=INK)
        ax.text(0.12, yc - 0.11, sub, ha="left", va="center", fontsize=8.6, color=GREY)
    else:
        ax.text(0.12, yc, name, ha="left", va="center", fontsize=fs, fontweight="bold", color=INK)
    vals = [f"{cts:,}", f"{l6:,}" if l6 else "0", f"{four:,}" if four else "0", t13, cast]
    colors = [INK, NAVY, BLUE, GOLD, CAST]
    for (cname, x, w, al), v, c in zip(cols[1:6], vals, colors):
        ax.text(x + w - 0.12, yc, v, ha="right", va="center", fontsize=fs, fontweight="bold" if bold else "normal", color=c if not bold else INK)
    mk, mc, st = status_txt[kind]
    if st:
        ax.text(11.9 + 0.12, yc, mk, ha="left", va="center", fontsize=15, color=mc)
        ax.text(11.9 + 0.45, yc, st, ha="left", va="center", fontsize=12.5, color=INK)

# foot: what a test needs, from the power chart (off unless FOOT > 0)
y -= 0.25
if FOOT:
  ax.add_patch(Rectangle((0, y - FOOT), W, FOOT, facecolor=NAVY, edgecolor="none"))
  ax.text(0.12, y - 0.32, "persons a test needs, from the Wilson lower bound", ha="left", va="center", fontsize=16, fontweight="bold", color="white")
  ax.text(0.12, y - 0.72, "errors among them", ha="left", va="center", fontsize=13, color="white")
  ax.text(0.12, y - 1.02, "90 % exact naming", ha="left", va="center", fontsize=14, color="white")
  ax.text(0.12, y - 1.32, "85 % sensitivity to the variant", ha="left", va="center", fontsize=14, color="white")
  for j, (k, n90, n85) in enumerate(zip(("none", "1", "2", "5"), need90, need85)):
      x = 5.3 + j * 1.35
      ax.text(x, y - 0.72, k, ha="center", va="center", fontsize=13, color="white")
      ax.text(x, y - 1.02, f"{n90}", ha="center", va="center", fontsize=17, fontweight="bold", color="white")
      ax.text(x, y - 1.32, f"{n85}", ha="center", va="center", fontsize=17, fontweight="bold", color="white")
  ax.text(W - 0.12, y - 0.55, "today, on real exposures: 7 candidates, none verified", ha="right", va="center", fontsize=13, color=GOLD)
  ax.text(W - 0.12, y - 0.9, "screened now: 322 L6 expected, 21 called by both labellers", ha="right", va="center", fontsize=13, color="white")
  ax.text(W - 0.12, y - 1.25, "each case counts as a test person where a film exists", ha="right", va="center", fontsize=13, color="white")
fig.savefig(OUT / "table_census.png", dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
with Image.open(OUT / "table_census.png") as im:
    print("table_census", im.size)
print("need90", need90, "need85", need85)
