"""paper/cns2026/prep_v10_figs.py — figures for deck v6 (Greg 2026-09-26, the long list):
  * cartoon_sweep.png: the manuscript's chain cartoon (figures/fig1d_algorithm.png) cropped to the prone column with
    the stepping, overlapping fields; the correlation panel below it (the method) is left out;
  * big_fig4_d.png: Figure 4 panel d alone (the check: shape against count, the call, the stop);
  * gallery_case83.png: the real frame whose two truth labellers disagree (orange boxes), from the C-ArmLSpine gallery;
  * chart_bettis_redrawn.png: Bettis et al. 2026 Figure 1 (NPDB payment reports for surgical never events by code,
    1991-2025) redrawn with slide-size legend and axis titles. The article page carries no data table, so the five
    curves are read off the published PNG by colour (one value per report year); the four codes are checked against
    the pooled line and the deviation printed. The fitted trend is omitted.
Writes into figs_v2/ and figs_cited/bettis2026_fig1_digitised.csv.

    python paper/cns2026/prep_v10_figs.py
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
CITED = HERE / "figs_cited"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"

# ---------------------------------------------------------------- crops
im = Image.open(SN / "figures" / "fig1d_algorithm.png").convert("RGB")
im.crop((0, 0, 2028, 322)).save(OUT / "cartoon_sweep.png")
print("cartoon_sweep", im.crop((0, 0, 2028, 322)).size)
f4 = Image.open(SN / "figures" / "figure4.png").convert("RGB")
f4.crop((1060, 1200, 2100, 2112)).save(OUT / "big_fig4_d.png")
f4.crop((0, 1200, 1060, 2112)).save(OUT / "big_fig4_c.png")
g = Image.open(OUT / "sn_carmlspine_gallery.png").convert("RGB")
g.crop((1987, 759, 2610, 1390)).save(OUT / "gallery_case83.png")
# the four angle frames of the rotational acquisition as a 2 x 2 grid (from the strip, split at its white gutters)
strip = Image.open(OUT / "big_figS5_a.png").convert("RGB")
col = np.asarray(strip.convert("L")).mean(axis=0) > 250
runs, start = [], None
for i, w_ in enumerate(col):
    if w_ and start is None:
        start = i
    if not w_ and start is not None:
        if i - start >= 6:
            runs.append((start, i))
        start = None
inner = [r for r in runs if r[0] > 20 and r[1] < strip.width - 20]
cuts = [0] + [int((a + b) / 2) for a, b in inner] + [strip.width]
panels = [strip.crop((cuts[i], 0, cuts[i + 1], strip.height)) for i in range(len(cuts) - 1)]
panels = [pn for pn in panels if pn.width > 150]
print("strip panels", len(panels), [pn.size for pn in panels])
if len(panels) == 4:
    pw = max(pn.width for pn in panels); phh = strip.height
    grid = Image.new("RGB", (2 * pw + 30, 2 * phh + 30), "white")
    for i, pn in enumerate(panels):
        r_, c_ = divmod(i, 2)
        grid.paste(pn, (c_ * (pw + 30), r_ * (phh + 30)))
    grid.save(OUT / "big_figS5_a_grid.png")
    print("big_figS5_a_grid", grid.size)
print("crops done")

# ---------------------------------------------------------------- Bettis: digitise
src = np.asarray(Image.open(CITED / "bettis2026_fig1.png").convert("RGB")).astype(int)
H, W, _ = src.shape
dark = (src.max(axis=2) < 70)
# axes: the column and row with the most dark pixels
col_counts = dark[100:1050, 100:400].sum(axis=0)
axis_x = 100 + int(np.argmax(col_counts))
row_counts = dark[900:1100, 200:1400].sum(axis=1)
axis_y = 900 + int(np.argmax(row_counts))
print("axes at x", axis_x, "y", axis_y)


def clusters(idx):
    idx = sorted(int(i) for i in idx)
    out, cur = [], [idx[0]] if idx else []
    for i in idx[1:]:
        if i - cur[-1] <= 2:
            cur.append(i)
        else:
            out.append(cur); cur = [i]
    if cur:
        out.append(cur)
    return [float(np.mean(c)) for c in out]


# y ticks: dark pixels just left of the axis line
yt = clusters(np.where(dark[:, axis_x - 14:axis_x - 4].sum(axis=1) >= 4)[0])
yt = [t for t in yt if 40 < t <= axis_y + 3]
ysp = float(np.median(np.diff(sorted(yt))))
print("y ticks", len(yt), "spacing px per 100:", round(ysp, 2))
# x ticks: dark pixels just below the axis line
xt = clusters(np.where(dark[axis_y + 4:axis_y + 14, :].sum(axis=0) >= 4)[0])
xt = [t for t in xt if t > axis_x + 20]
xsp = float(np.median(np.diff(sorted(xt))))
print("x ticks", [round(t) for t in xt], "spacing px per 5 years:", round(xsp, 2))
pxpy = xsp / 5.0
x1995 = min(xt)                      # the first labelled tick is 1995

# series colours from the legend swatches (a column through the swatch lines, upper right)
swatch_col = None
for x in range(900, 1100, 5):
    colm = src[20:200, x]
    nonwhite = [(y + 20, tuple(colm[y])) for y in range(colm.shape[0]) if colm[y].sum() < 700]
    if len(nonwhite) >= 30:
        swatch_col = x
        break
refs = {}
if swatch_col is not None:
    colm = src[20:200, swatch_col]
    rows = [y for y in range(colm.shape[0]) if colm[y].sum() < 700]
    for c in clusters(rows):
        rgb = tuple(int(v) for v in src[int(c) + 20, swatch_col])
        refs[int(c) + 20] = rgb
print("swatches (row: colour):", refs)
names_by_order = ["322 retained foreign body", "330 wrong body part", "333 wrong patient", "334 wrong procedure or treatment", "all four codes, pooled", "fitted trend"]
series = {}
for (row, rgb), name in zip(sorted(refs.items()), names_by_order):
    series[name] = np.array(rgb)
series.pop("fitted trend", None)

plot = np.zeros((H, W), bool)
plot[60:axis_y - 1, axis_x + 3:W - 20] = True
plot[0:210, 930:W] = False           # the legend box
years = list(range(1991, 2026))
data = {}
for name, rgb in series.items():
    dist = np.sqrt(((src - rgb) ** 2).sum(axis=2))
    mask = (dist < 60) & plot
    if name.startswith("all four"):
        mask = mask & (src.max(axis=2) < 70)
    vals = []
    for yr in years:
        x = int(round(x1995 + (yr - 1995) * pxpy))
        ys = np.where(mask[:, max(x - 2, 0):x + 3].any(axis=1))[0]
        vals.append(float((axis_y - ys.mean()) / ysp * 100) if len(ys) else np.nan)
    data[name] = vals
first_col = np.where((np.sqrt(((src - series["322 retained foreign body"]) ** 2).sum(axis=2)) < 60) & plot)[1].min()
print("first blue column", first_col, "-> year", round(1995 + (first_col - x1995) / pxpy, 1))
# fill the wrong-patient line's early years (it lies on the axis, under the axis ink) with 0
wp = data["333 wrong patient"]
data["333 wrong patient"] = [0.0 if np.isnan(v) else v for v in wp]
# check: the four codes against the pooled line
codes = [k for k in data if not k.startswith("all four")]
dev = []
for i, yr in enumerate(years):
    s = sum(data[k][i] for k in codes if not np.isnan(data[k][i]))
    p = data["all four codes, pooled"][i]
    if not np.isnan(p) and p > 0 and all(not np.isnan(data[k][i]) for k in codes):
        dev.append(abs(s - p) / p)
print("pooled check: median |sum-pooled|/pooled = %.3f, max %.3f over %d years" % (np.median(dev), max(dev), len(dev)))
with open(CITED / "bettis2026_fig1_digitised.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year"] + list(data.keys()))
    for i, yr in enumerate(years):
        w.writerow([yr] + [("" if np.isnan(data[k][i]) else round(data[k][i])) for k in data])

# ---------------------------------------------------------------- Bettis: redraw at slide type sizes
plt.rcParams.update({"font.family": "Arial", "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#DDDDDD", "grid.linewidth": 0.6})
colors = {"322 retained foreign body": "#3AB0F4", "330 wrong body part": "#F7943A", "333 wrong patient": "#22C15A",
          "334 wrong procedure or treatment": "#8B5CF6", "all four codes, pooled": "#111111"}
fig, ax = plt.subplots(figsize=(12.5, 7.6))
for name in ["all four codes, pooled", "322 retained foreign body", "334 wrong procedure or treatment", "330 wrong body part", "333 wrong patient"]:
    v = np.array(data[name], float)
    ok = ~np.isnan(v)
    ax.plot(np.array(years)[ok], v[ok], color=colors[name], lw=4.2 if name.startswith("all") else 3.4, label=name, solid_capstyle="round")
ax.axvline(2004, color="#333333", ls=":", lw=2)
ax.text(2004.4, 790, "2004 report-format transition", fontsize=15, color="#333333", va="top")
ax.set_xlim(1991, 2025)
ax.set_ylim(0, 820)
ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2025])
ax.tick_params(labelsize=18)
ax.set_xlabel("report year", fontsize=21)
ax.set_ylabel("malpractice payment reports, n", fontsize=21)
ax.legend(loc="upper right", fontsize=17, frameon=False, title="NPDB surgical never-event code", title_fontsize=16)
fig.tight_layout()
fig.savefig(OUT / "chart_bettis_redrawn.png", dpi=220, bbox_inches="tight", pad_inches=0.08, facecolor="white")
with Image.open(OUT / "chart_bettis_redrawn.png") as im2:
    print("chart_bettis_redrawn", im2.size)
print("done")
