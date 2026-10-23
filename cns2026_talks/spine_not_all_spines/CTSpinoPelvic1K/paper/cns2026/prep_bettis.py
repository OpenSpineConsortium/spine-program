"""paper/cns2026/prep_bettis.py — Bettis et al. 2026 Figure 1 (National Practitioner Data Bank malpractice payment
reports for surgical never events by code, 1991-2025) redrawn with slide-size legend and axis titles. The article
page carries no data table, so the curves are read off the published PNG: pixels are classed by hue (blue, orange,
green, purple) or as black (the pooled line), the axes are calibrated from the tick-label positions, one value is
taken per report year, and the four codes are checked against the pooled line. The fitted trend is omitted.
Writes figs_v2/chart_bettis_redrawn.png and figs_cited/bettis2026_fig1_digitised.csv.

    python paper/cns2026/prep_bettis.py
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import rgb_to_hsv  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
CITED = HERE / "figs_cited"

src = np.asarray(Image.open(CITED / "bettis2026_fig1.png").convert("RGB")).astype(float) / 255.0
H, W, _ = src.shape
hsv = rgb_to_hsv(src)
dark = src.max(axis=2) < 0.28
sat = hsv[..., 1] > 0.35
hue = hsv[..., 0]

# axes
col_counts = dark[100:1050, 100:400].sum(axis=0)
axis_x = 100 + int(np.argmax(col_counts))
row_counts = dark[900:1100, 200:1400].sum(axis=1)
axis_y = 900 + int(np.argmax(row_counts))
# the dotted 2004 line: the other column with many dark pixels
cc = dark[150:900, :].sum(axis=0)
dark_cols = [int(x) for x in np.where(cc > 120)[0] if x > axis_x + 20 and x < W - 20]   # the dotted 2004 line
print("axes x", axis_x, "y", axis_y, "dark vertical columns", dark_cols)


def clusters(idx, gap=3):
    idx = sorted(int(i) for i in idx)
    out, cur = [], [idx[0]] if idx else []
    for i in idx[1:]:
        if i - cur[-1] <= gap:
            cur.append(i)
        else:
            out.append(cur); cur = [i]
    if cur:
        out.append(cur)
    return [(float(np.mean(c)), len(c)) for c in out]


# y tick labels: text blobs left of the axis (columns 60..axis_x-20)
band = dark[:, 60:axis_x - 20]
rows = np.where(band.sum(axis=1) >= 3)[0]
ylab = [c for c, n in clusters(rows, gap=4) if n >= 8 and 30 < c < axis_y + 20]
print("y label rows", [round(v) for v in ylab])
# x tick labels: text blobs under the axis (rows axis_y+15 .. axis_y+70)
band = dark[axis_y + 15:axis_y + 70, :]
cols = np.where(band.sum(axis=0) >= 3)[0]
xlab = [c for c, n in clusters(cols, gap=6) if n >= 20 and c > axis_x]
print("x label cols", [round(v) for v in xlab])
assert len(ylab) >= 5 and len(xlab) >= 5, "label detection failed"
ylab = sorted(ylab)                       # the topmost blob is the "800" label; zero sits on the x-axis line
y0 = float(axis_y)
ysp = (y0 - ylab[0]) / 8.0                 # px per 100 reports
xlab = sorted(xlab)                       # 1995 .. 2025
pxpy = (xlab[-1] - xlab[0]) / (5 * (len(xlab) - 1))
x1995 = xlab[0]
print("px per 100:", round(ysp, 2), "px per year:", round(pxpy, 2), "y0 row", round(y0, 1), "axis_y", axis_y)

plot = np.zeros((H, W), bool)
plot[40:axis_y - 3, axis_x + 9:W - 10] = True     # clear of the axis line's anti-aliased edge
plot[0:215, 920:W] = False                 # legend
plot[30:125, 560:800] = False              # the "2004 format transition" text
for xd in dark_cols:
    plot[:, xd - 3:xd + 4] = False
hue_bins = {"322 retained foreign body": (0.50, 0.66), "330 wrong body part": (0.03, 0.13),
            "333 wrong patient": (0.28, 0.48), "334 wrong procedure or treatment": (0.68, 0.82)}
# line-core colours: the median of the strongly saturated pixels of each hue bin; then nearest-colour classification,
# so the blends where two lines cross (orange over purple reads as green by hue) are assigned to neither
cores = {}
for k, (lo, hi) in hue_bins.items():
    sel = plot & (hsv[..., 1] > 0.6) & (hue >= lo) & (hue < hi)
    cores[k] = np.median(src[sel], axis=0)
    print("core", k, np.round(cores[k] * 255).astype(int))
dist = {k: np.sqrt(((src - c) ** 2).sum(axis=2)) for k, c in cores.items()}
nearest = min(dist.values()) if False else None
masks = {}
for k in hue_bins:
    others = np.min(np.stack([dist[o] for o in hue_bins if o != k]), axis=0)
    masks[k] = plot & sat & (dist[k] < 0.22) & (dist[k] < others)
masks["all four codes, pooled"] = plot & dark & ~sat
years = list(range(1991, 2026))
data = {}
for name, mask in masks.items():
    vals = []
    for yr in years:
        x = int(round(x1995 + (yr - 1995) * pxpy))
        best = None
        for half in (3, 6, 9):
            win = mask[:, max(x - half, 0):x + half + 1]
            counts = win.sum(axis=1)
            rows_ = np.where(counts > 0)[0]
            if not len(rows_):
                continue
            # the line is the largest contiguous run of rows; tick marks and stray dots are small runs
            runs, start = [], rows_[0]
            for a, b in zip(rows_[:-1], rows_[1:]):
                if b - a > 2:
                    runs.append((start, a)); start = b
            runs.append((start, rows_[-1]))
            r0, r1 = max(runs, key=lambda r: counts[r[0]:r[1] + 1].sum())
            rr = np.arange(r0, r1 + 1)
            best = float((rr * counts[r0:r1 + 1]).sum() / counts[r0:r1 + 1].sum())
            break
        vals.append(float((y0 - best) / ysp * 100) if best is not None else np.nan)
    data[name] = vals
blue_cols = np.where(masks["322 retained foreign body"].any(axis=0))[0]
print("blue spans columns", blue_cols.min(), "-", blue_cols.max(), "-> years", round(1995 + (blue_cols.min() - x1995) / pxpy, 1),
      "to", round(1995 + (blue_cols.max() - x1995) / pxpy, 1))
data["333 wrong patient"] = [0.0 if np.isnan(v) else v for v in data["333 wrong patient"]]
codes = [k for k in data if not k.startswith("all four")]
dev = []
for i, yr in enumerate(years):
    vals = [data[k][i] for k in codes]
    p = data["all four codes, pooled"][i]
    if not np.isnan(p) and all(not np.isnan(v) for v in vals):
        dev.append((yr, sum(vals), p, abs(sum(vals) - p) / p))
print("pooled check over %d years: median |sum-pooled|/pooled %.3f, max %.3f (%s)" %
      (len(dev), float(np.median([d[3] for d in dev])), max(d[3] for d in dev), max(dev, key=lambda d: d[3])[0]))
for yr, s, p, r in dev[:3] + dev[-3:]:
    print("   ", yr, "sum", round(s), "pooled", round(p))
with open(CITED / "bettis2026_fig1_digitised.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year"] + list(data.keys()))
    for i, yr in enumerate(years):
        w.writerow([yr] + [("" if np.isnan(data[k][i]) else round(data[k][i])) for k in data])

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
ax.text(2004.4, 800, "2004 report-format\ntransition", fontsize=15, color="#333333", va="top")
first = min(yr for yr, v in zip(years, data["all four codes, pooled"]) if not np.isnan(v))
ax.set_xlim(first, 2025)
ax.set_ylim(0, 830)
ax.set_xticks([1995, 2000, 2005, 2010, 2015, 2020, 2025])
ax.tick_params(labelsize=18)
ax.set_xlabel("report year", fontsize=21)
ax.set_ylabel("malpractice payment reports, n", fontsize=21)
ax.legend(loc="upper right", fontsize=17, frameon=False, title="NPDB surgical never-event code", title_fontsize=16)
fig.tight_layout()
fig.savefig(OUT / "chart_bettis_redrawn.png", dpi=220, bbox_inches="tight", pad_inches=0.08, facecolor="white")
with Image.open(OUT / "chart_bettis_redrawn.png") as im2:
    print("chart_bettis_redrawn", im2.size, "first year", first)
