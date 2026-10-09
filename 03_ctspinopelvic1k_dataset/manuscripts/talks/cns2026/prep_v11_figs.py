"""paper/cns2026/prep_v11_figs.py — figures for deck v7 (Greg 2026-09-26, second list):
  * cartoon_sweep.png: the chain cartoon down to the bottom of the column, the "step" arrow painted out;
  * occlusion_grid.png: Figure 2d's four occlusion crops (L4, L5, L6, sacrum; red = what the naming draws on) as 2 x 2;
  * big_fig2_ab_side.png: Figure 2a beside its lumbosacral window 2b;
  * chart_machin_redrawn.png: Machin et al. 2018 Figure 2 (NHS spinal-surgery negligence claims 2012-2017 by cause,
    number and estimated cost) read off the published PNG and redrawn with slide-size type, the wrong-level row in red;
  * table_levelcheck.png and table_result1.png: published level-identification methods with their accuracy and
    error, the second with SchwingNet's rows added;
  * table_corpus.png: the training data by modality.
Writes into figs_v2/ (and figs_cited/machin2018_fig2_digitised.csv).

    python paper/cns2026/prep_v11_figs.py
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
CITED = HERE / "figs_cited"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
NAVY, BLUE, PALE, RED, GOLD, GREY, INK, LIGHT = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#8A8A8A", "#191D63", "#EEF1F8"
plt.rcParams["font.family"] = "Arial"


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size)


# ---------------------------------------------------------------- cartoon, occlusion grid, 2a + 2b
c = Image.open(SN / "figures" / "fig1d_algorithm.png").convert("RGB").crop((0, 0, 2028, 362))
ImageDraw.Draw(c).rectangle([985, 318, 1245, 362], fill="white")
c.save(OUT / "cartoon_sweep.png")
f2 = Image.open(SN / "figures" / "figure2.png").convert("RGB")
occ = f2.crop((1280, 1510, 2100, 1790))
col = np.asarray(occ.convert("L")).mean(axis=0) > 250
runs, start = [], None
for i, w_ in enumerate(col):
    if w_ and start is None:
        start = i
    if not w_ and start is not None:
        if i - start >= 4:
            runs.append((start, i))
        start = None
inner = [r for r in runs if r[0] > 10 and r[1] < occ.width - 10]
cuts = [0] + [int((a + b) / 2) for a, b in inner] + [occ.width]
panels = [occ.crop((cuts[i], 0, cuts[i + 1], occ.height)) for i in range(len(cuts) - 1)]
panels = [p for p in panels if p.width > 80]
print("occlusion panels", len(panels), [p.size for p in panels])
if len(panels) == 4:
    pw = max(p.width for p in panels); ph = occ.height
    grid = Image.new("RGB", (2 * pw + 24, 2 * ph + 24), "white")
    for i, p in enumerate(panels):
        r_, c_ = divmod(i, 2)
        grid.paste(p, (c_ * (pw + 24) + (pw - p.width) // 2, r_ * (ph + 24)))
    grid.save(OUT / "occlusion_grid.png")
    print("occlusion_grid", grid.size)
a = f2.crop((28, 41, 1211, 1115))
b = f2.crop((1211, 41, 2088, 1340))
h = a.height
b2 = b.resize((int(b.width * h / b.height), h), Image.LANCZOS)
side = Image.new("RGB", (a.width + 40 + b2.width, h), "white")
side.paste(a, (0, 0)); side.paste(b2, (a.width + 40, 0))
side.save(OUT / "big_fig2_ab_side.png")
print("big_fig2_ab_side", side.size)

# ---------------------------------------------------------------- Machin 2018 Figure 2: digitise and redraw
src = np.asarray(Image.open(CITED / "machin2018_fig2.png").convert("RGB")).astype(int)
H, W, _ = src.shape
blue = np.sqrt(((src - np.array([68, 114, 196])) ** 2).sum(axis=2)) < 60
orange = np.sqrt(((src - np.array([237, 125, 49])) ** 2).sum(axis=2)) < 60
grey_line = (np.abs(src[..., 0] - src[..., 1]) < 8) & (np.abs(src[..., 1] - src[..., 2]) < 8) & (src[..., 0] > 195) & (src[..., 0] < 235)
gl = np.where(grey_line[:H - 120].sum(axis=0) > (H - 120) * 0.6)[0]
gcl, st = [], None
for x in gl:
    if st is None:
        st = [x]
    elif x - st[-1] <= 2:
        st.append(x)
    else:
        gcl.append(float(np.mean(st))); st = [x]
if st:
    gcl.append(float(np.mean(st)))
print("gridlines", [round(g) for g in gcl])
x0, x400 = gcl[0], gcl[-1]
pxu = (x400 - x0) / 400.0
dark = src.max(axis=2) < 90
lab = np.where(dark[:, :int(x0) - 15].sum(axis=1) >= 3)[0]
rows_, st = [], None
for y in lab:
    if st is None:
        st = [y]
    elif y - st[-1] <= 6:
        st.append(y)
    else:
        rows_.append((float(np.mean(st)), len(st))); st = [y]
if st:
    rows_.append((float(np.mean(st)), len(st)))
rows_ = [r for r, n in rows_ if n >= 8]
labels = ["Wrong site / level", "Wrong operation", "Venous thromboembolic events", "Unsatisfactory outcome to surgery", "Tumour / cancer",
          "Tissue damage", "Retained instruments post-operation", "Procedure", "Pressure sores", "Post-operative spinal infection",
          "Post-operative complications", "Pain", "Nerve damage", "Mobility", "Missed spinal tumour", "Missed spinal fracture",
          "Missed spinal infection", "Judgement / timing", "Interpretation of results / clinical picture", "Infection",
          "Inadequate decompression", "Iatrogenic cord damage", "Equipment / implant", "Dislocation", "Death", "Consent",
          "Cauda equina syndrome", "Amputation", "Accidental injury"]
print("label rows found", len(rows_), "expected", len(labels))
vals = []
for yc, name in zip(rows_, labels):
    y0, y1 = int(yc - 22), int(yc + 22)
    bx = np.where(blue[y0:y1, int(x0):].any(axis=0))[0]
    ox = np.where(orange[y0:y1, int(x0):].any(axis=0))[0]
    claims = (bx.max() + 1) / pxu if len(bx) else 0.0
    cost = (ox.max() + 1) / pxu if len(ox) else 0.0
    vals.append((name, round(claims), round(cost, 1)))
with open(CITED / "machin2018_fig2_digitised.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["cause", "claims_n", "estimated_cost_gbp_million"]); w.writerows(vals)
for v in vals[:3] + vals[7:8] + vals[17:19]:
    print("  ", v)
fig, ax = plt.subplots(figsize=(12.5, 9.6))
names = [v[0] for v in vals][::-1]
cl = [v[1] for v in vals][::-1]
co = [v[2] for v in vals][::-1]
yy = np.arange(len(names))
ax.barh(yy + 0.2, cl, height=0.4, color=BLUE, label="claims, n")
ax.barh(yy - 0.2, co, height=0.4, color="#F0913A", label="estimated cost, £ million")
ax.set_yticks(yy)
ax.set_yticklabels(names, fontsize=14)
for t in ax.get_yticklabels():
    if t.get_text().startswith("Wrong site"):
        t.set_color(RED); t.set_fontweight("bold")
i_w = names.index("Wrong site / level")
ax.text(max(cl[i_w], co[i_w]) + 6, i_w, f"{cl[i_w]} claims, £{co[i_w]:.0f} million", va="center", fontsize=14, color=RED, fontweight="bold")
ax.set_xlim(0, 400)
ax.tick_params(axis="x", labelsize=16)
ax.set_xlabel("claims (n) and estimated cost (£ million)", fontsize=18)
ax.grid(axis="x", color="#DDDDDD"); ax.set_axisbelow(True)
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
ax.legend(loc="lower right", fontsize=16, frameon=False)
fig.tight_layout()
save(fig, "chart_machin_redrawn.png")


# ---------------------------------------------------------------- tables as images
def table_image(name, header, rows, colw, figsize, fs=15, hl=None, wrap_col0=None, row_h=0.62):
    """A rendered table: header band, zebra rows, right-aligned numbers; hl = set of row indices to band in pale blue."""
    W = sum(colw)
    HEAD = 0.75
    Hh = HEAD + row_h * len(rows) + 0.1
    fig = plt.figure(figsize=(figsize[0], figsize[0] * Hh / W))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-0.1, W + 0.1); ax.set_ylim(-Hh + 0.05, 0.05); ax.set_axis_off()
    ax.add_patch(Rectangle((0, -HEAD), W, HEAD, facecolor=NAVY, edgecolor="none"))
    x = 0
    for j, (h_, w_) in enumerate(zip(header, colw)):
        ax.text(x + 0.12 if j == 0 else x + w_ - 0.12, -HEAD / 2, h_, ha="left" if j == 0 else "right", va="center",
                fontsize=fs, fontweight="bold", color="white")
        x += w_
    y = -HEAD
    for i, row in enumerate(rows):
        y -= row_h
        if hl and i in hl:
            ax.add_patch(Rectangle((0, y), W, row_h, facecolor=PALE, edgecolor="none"))
        elif i % 2 == 0:
            ax.add_patch(Rectangle((0, y), W, row_h, facecolor="#F7F8FB", edgecolor="none"))
        x = 0
        for j, (cell, w_) in enumerate(zip(row, colw)):
            bold = bool(hl and i in hl)
            if j == 0 and isinstance(cell, tuple):
                ax.text(x + 0.12, y + row_h / 2 + 0.1, cell[0], ha="left", va="center", fontsize=fs, fontweight="bold" if bold else "normal", color=INK)
                ax.text(x + 0.12, y + row_h / 2 - 0.14, cell[1], ha="left", va="center", fontsize=fs * 0.68, color=GREY)
            else:
                ax.text(x + 0.12 if j == 0 else x + w_ - 0.12, y + row_h / 2, cell, ha="left" if j == 0 else "right", va="center",
                        fontsize=fs, fontweight="bold" if bold else "normal", color=INK)
            x += w_
    save(fig, name)


lc_rows = [
    (("LevelCheck label placement", "De Silva 2016; against its own imported labels"), "100 %", "0 %"),
    (("Surgeons reading with the LevelCheck overlay", "Manbachi 2018; 62 difficult films, median of five"), "97.6 %", "2.4 %"),
    (("Cadaver long-length images, region CNN", "Huang 2022"), "88.3 %", "11.7 %"),
    (("Lumbar MRI localiser, no count from C2", "Peh 1999"), "77.9–82.2 %", "18–22 %"),
    (("Real C-arm images, identity from a preoperative film", "Zhang 2023"), "73.3 %", "26.7 %"),
]
table_image("table_levelcheck.png", ["method", "level right", "error"], lc_rows, [4.6, 1.3, 0.9], (7.0, 0), fs=15, row_h=0.7)
r1_rows = [
    (("SchwingNet, never trained on the C-arm, lateral", "148 real intraoperative cases; cone-beam CT truth; 595 of 617"), "96.4 %", "3.6 %"),
    (("SchwingNet, fine-tuned on other cases of the C-arm", "601 of 617"), "97.4 %", "2.6 %"),
    (("SchwingNet, shape and count together", "991 of 1,009 bodies of frames with the sacrum in view"), "98.2 %", "1.8 %"),
] + lc_rows
table_image("table_result1.png", ["method", "level right", "error"], r1_rows, [8.2, 1.5, 1.1], (12.0, 0), fs=16, hl={0, 1, 2}, row_h=0.66)
corpus_rows = [
    (("CT, rendered as radiographs", "802 + 1,935 + 374 scans; 191 transitional persons"), "4,093", "191"),
    (("Plain films with levels", "4,963 + 3,600 + 364 persons; none human-read transitional"), "9,108", "0"),
    (("Fluoroscopy, mobile C-arm, real", "148 intraoperative cases, 6 cadaver pelves, 1 phantom; cone-beam CT or CT truth"), "778", "3"),
    (("Fluoroscopy, radiotherapy kV imager, real", "145 patients; planning CT truth; 91 screen calls unread"), "3,498", "0"),
]
table_image("table_corpus.png", ["modality", "images", "transitional"], corpus_rows, [4.8, 1.0, 1.3], (7.0, 0), fs=14, row_h=0.72)
print("done")
