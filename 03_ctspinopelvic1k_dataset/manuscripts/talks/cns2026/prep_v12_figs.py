"""paper/cns2026/prep_v12_figs.py — figures for deck v8 (Greg 2026-09-26, third list):
  * board_wrongsite_cost.png: every verified wrong-site / wrong-level economic number on one board, big numerals
    (spinesurg docs/WRONG_LEVEL_COST_EVIDENCE.md and WRONG_SITE_BURDEN_EVIDENCE.md, verified 2026-09-19), with the
    52-minute fiducial placement priced per patient, per year and per series;
  * render_case42_find.png: the case-42 frame with the detector's body boxes and the sacrum box, no names (the
    "find" panel, rendered from results/fig4_frames/case42_LAT.couple.json at 1024 px, not cropped from the paper);
  * occlusion_grid.png: the occlusion maps of T12, L4, L5, L6 and the sacrum rendered from
    results/figure2/occlusion_clean/gradcam.npz (representative validation crop, mean occlusion in red, the target
    box in white), with slide-size labels; the "name" panel;
  * chart_level_accuracy.png: exact-level naming by level on the level model's checkpoint-selection split (renders
    and films, not held out; results/alpha_0.3_seed*/...json, mixed bands of two to nine bodies, three seeds).
Writes into figs_v2/.

    python paper/cns2026/prep_v12_figs.py
"""
import glob
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from PIL import Image, ImageDraw, ImageFont, ImageOps  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
NAVY, BLUE, PALE, RED, GOLD, GREY, INK, LIGHT = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#8A8A8A", "#191D63", "#EEF1F8"
plt.rcParams["font.family"] = "Arial"


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size)


# ------------------------------------------------------------------ 1. the cost board
tiles = [
    ("$1.3 billion", "malpractice payments for all surgical never events,\nNational Practitioner Data Bank, 1990–2010 (21 years)", "Mehtsun 2013", NAVY),
    ("about $15 million a year", "the wrong-site share of it: one quarter of paid\nnever-event claims are wrong site", "Mehtsun 2013, derived", NAVY),
    ("$136,453", "mean closed wrong-site claim at one US carrier,\n2013–2020; spine the commonest procedure (22 %)", "Tan 2023, n = 68", NAVY),
    ("$75,220", "median never-event payment, 1991–2025\n(IQR $28,847–$215,003)", "Bettis 2026", NAVY),
    ("81 % paid", "of litigated wrong-disc-level cases; surgeons\nprevailed in 42 % of jury trials", "Goodkin & Laska 2004, n = 68", RED),
    ("17 %  ·  1 in 5", "of wrong-level events reach legal action;\nSpine Section surgeons ever sued for wrong level or side", "Mody 2008; Groff 2013", RED),
    ("23 claims, £7 million", "wrong site or level among 978 English spinal-surgery\nclaims worth £535.5 million, 2012–2017", "Machin 2018", NAVY),
    ("111 claims, £4.8 million", "NHS orthopaedic wrong-site claims 1995–2010,\n23 of them wrong spinal level; mean £43,596; 89 % paid", "Harrison 2015", NAVY),
    ("$1,750–1,950 per patient", "52 minutes of operating-room time to place a gold\nfiducial the day before, at $34–37 per minute", "AJNR 2023; Childers 2018", GOLD),
    ("about $100,000 a year", "179 fiducial patients over 38 months at one centre:\n56 a year, 155 staffed hours, about $350,000 in all", "AJNR 2023, derived", GOLD),
    ("420–1,900 operations a year", "US wrong-level spine operations, from 1 in 3,110\nself-reported and 0.12 % registry rates", "derived, unpublished", GREY),
    ("$8–37 million a year", "US indemnity for those alone, before reoperation,\nadded stay and disability", "derived, unpublished", GREY),
]
cols_, rows_ = 3, 4
fig = plt.figure(figsize=(14.0, 8.6))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, cols_); ax.set_ylim(0, rows_); ax.set_axis_off()
for i, (num, lab, src, col) in enumerate(tiles):
    r_, c_ = divmod(i, cols_)
    x, y = c_, rows_ - 1 - r_
    ax.add_patch(FancyBboxPatch((x + 0.03, y + 0.04), 0.94, 0.92, boxstyle="round,pad=0,rounding_size=0.03", fc=LIGHT, ec="none"))
    ax.add_patch(FancyBboxPatch((x + 0.03, y + 0.84), 0.94, 0.12, boxstyle="round,pad=0,rounding_size=0.03", fc=col, ec="none"))
    ax.text(x + 0.5, y + 0.9, src, ha="center", va="center", fontsize=11.5, color="white")
    ax.text(x + 0.5, y + 0.6, num, ha="center", va="center", fontsize=22 if len(num) < 22 else 18, fontweight="bold", color=col if col != GREY else INK)
    ax.text(x + 0.5, y + 0.28, lab, ha="center", va="center", fontsize=11.5, color=INK, linespacing=1.25)
save(fig, "board_wrongsite_cost.png")

# ------------------------------------------------------------------ 2. the "find" panel from the case-42 boxes
d = json.load(open(SN / "results" / "fig4_frames" / "case42_LAT.couple.json"))
fr = Image.open(SN / "results" / "fig5_frames" / "case42_LAT.png").convert("L")
fr = ImageOps.autocontrast(fr, cutoff=0.5).convert("RGB")
X0 = 300
crop = fr.crop((X0, 0, 1024, 1024))
dr = ImageDraw.Draw(crop)
for b in d["bodies"]:
    x0, y0, x1, y1 = b["box"]
    dr.rectangle([x0 - X0, y0, x1 - X0, y1], outline=(0x4C, 0x70, 0xB7), width=6)
ax0, ay0, ax1, ay1 = d["anchor"]["box"]
for k in range(0, 2000, 28):   # dashed sacrum box
    pass
def dashed_rect(dr, box, color, width=6, dash=22):
    x0, y0, x1, y1 = box
    for (xa, ya, xb, yb) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x0, y1, x1, y1), (x0, y0, x0, y1)):
        L_ = max(abs(xb - xa), abs(yb - ya)); n = max(1, int(L_ / dash))
        for i in range(0, n, 2):
            t0, t1 = i / n, min((i + 1) / n, 1)
            dr.line([xa + (xb - xa) * t0, ya + (yb - ya) * t0, xa + (xb - xa) * t1, ya + (yb - ya) * t1], fill=color, width=width)
dashed_rect(dr, (ax0 - X0, ay0, min(ax1, 1024) - X0 - 4, ay1 - 4), (20, 20, 20))
crop.save(OUT / "render_case42_find.png")
print("render_case42_find", crop.size)

# ------------------------------------------------------------------ 3. the occlusion maps, rendered
z = np.load(SN / "results" / "figure2" / "occlusion_clean" / "gradcam.npz", allow_pickle=True)
levels = ["T12", "L4", "L5", "L6", "sacrum"]
FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 54)
tiles_ = []
for lvl in levels:
    img = z[f"v9_val__{lvl}__rep_img"].astype(np.float32) / 255.0
    occ = z[f"v9_val__{lvl}__mean_occlusion"].astype(np.float32)
    occ = np.clip(occ, 0, None); occ = occ / (occ.max() + 1e-9)
    marker = z[f"v9_val__{lvl}__rep_marker"]
    rgb = np.stack([img, img, img], axis=2)
    alpha = (occ ** 0.8)[..., None] * 0.75
    red = np.array([0.94, 0.27, 0.15])[None, None, :]
    rgb = rgb * (1 - alpha) + red * alpha
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize((640, 640), Image.LANCZOS)
    ys, xs = np.where(marker > 0)
    dr = ImageDraw.Draw(im)
    if len(xs):
        s_ = 640 / 320
        dr.rectangle([xs.min() * s_, ys.min() * s_, xs.max() * s_, ys.max() * s_], outline="white", width=5)
    tile = Image.new("RGB", (640, 640 + 90), "white")
    tile.paste(im, (0, 90))
    d2 = ImageDraw.Draw(tile)
    tw = d2.textlength(lvl, font=FONT)
    d2.text(((640 - tw) / 2, 12), lvl, fill=(0x19, 0x1D, 0x63), font=FONT)
    tiles_.append(tile)
# 2 x 3 with the sacrum last; the sixth cell holds the legend
grid = Image.new("RGB", (3 * 640 + 2 * 30, 2 * 730 + 30), "white")
for i, t in enumerate(tiles_):
    r_, c_ = divmod(i, 3)
    grid.paste(t, (c_ * 670, r_ * 760))
d3 = ImageDraw.Draw(grid)
F2 = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 40)
d3.text((2 * 670 + 20, 760 + 150), "red: the parts of the crop\nwhose removal changes\nthe name most\n\nwhite: the body being named", fill=(0x19, 0x1D, 0x63), font=F2, spacing=10)
grid.save(OUT / "occlusion_grid.png")
print("occlusion_grid", grid.size)

# ------------------------------------------------------------------ 4. exact level by level (selection split)
files = sorted(glob.glob(str(SN / "results" / "alpha_0.3_seed*" / "mixed_allspine_v9_mixed_kmax4_alpha0.3_seed*.json")))
order = [f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + [f"L{i}" for i in range(1, 7)] + ["sacrum"]
acc = {l: [] for l in order}; nn = {}
for f in files:
    pl = json.load(open(f))["results"][-1]["per_level"]
    for l in order:
        if l in pl:
            acc[l].append(pl[l]["exact"] * 100); nn[l] = pl[l]["n"]
xs = list(range(len(order)))
mean = [np.mean(acc[l]) for l in order]
lo = [min(acc[l]) for l in order]; hi = [max(acc[l]) for l in order]
fig, ax = plt.subplots(figsize=(14.0, 5.6))
ax.axvspan(6.5, 18.5, color="#FFF4D6", zorder=0)
ax.text(12.5, 30, "thoracic", ha="center", fontsize=18, color=GOLD)
ax.fill_between(xs, lo, hi, color=PALE, alpha=0.8, zorder=1)
ax.plot(xs, mean, color=NAVY, lw=3, marker="o", ms=9, zorder=3)
for x, m_, l in zip(xs, mean, order):
    ax.annotate(f"{m_:.0f}", (x, m_), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=13, color=INK)
ax.set_xticks(xs); ax.set_xticklabels(order, fontsize=15)
ax.set_ylim(20, 105); ax.set_ylabel("exact level, %", fontsize=19); ax.tick_params(axis="y", labelsize=15)
ax.grid(axis="y", color="#DDDDDD"); ax.set_axisbelow(True)
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
ax.text(0.2, 24, f"n per level {min(nn.values()):,}–{max(nn.values()):,} crops; three seeds (band)", fontsize=13, color=GREY)
fig.tight_layout()
save(fig, "chart_level_accuracy.png")
json.dump({l: {"n": nn[l], "exact_mean_pct": round(float(np.mean(acc[l])), 1)} for l in order}, open(OUT / "level_accuracy.json", "w"), indent=1)
print("done")
