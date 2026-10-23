"""paper/cns2026/prep_v14_figs.py — figures for deck v9 (Greg 2026-09-26, fourth list):
  * board_wrongsite_cost.png: the cost board re-rendered at slide aspect (4 x 3 tiles, 14 x 6.6 in) with the type
    sized for the slide: numerals 24 pt and labels 12 pt AS DISPLAYED at full slide width, no empty margin;
  * fig2_wide.png: the level map (manuscript Figure 2a) and its lumbosacral window (2b) re-rendered from
    results/figure2/figure2_map.npz at 3:1 so the two panels span the slide, the colour key and the marker legend in
    a third column at slide size; the same sets, window rule and markers as SchwingNet/tools/figure2.py;
  * table_modalities.png: the training data by modality as one wide table, modalities across;
  * occlusion_2x2.png: the occlusion maps of T12, L4, L5 and L6 as a portrait 2 x 2 (the "name" column);
  * render_case42_check.png: the check panel at column size, the frame cropped to the spine, the shape / count / call
    columns and the stop line in 60-px type.
Writes into figs_v2/.

    python paper/cns2026/prep_v14_figs.py
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402
from PIL import Image, ImageDraw, ImageFont, ImageOps  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
NAVY, BLUE, PALE, RED, GOLD, GREY, INK, LIGHT = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#8A8A8A", "#191D63", "#EEF1F8"
plt.rcParams["font.family"] = "Arial"


def save(fig, name, pad=0.03):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", pad_inches=pad, facecolor="white")
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size, round(im.size[0] / im.size[1], 2))


# ------------------------------------------------------------------ 1. the cost board, slide aspect, slide type
tiles = [
    ("$1.3 billion", "malpractice paid for all surgical\nnever events, US National\nPractitioner Data Bank, 1990–2010", "Mehtsun 2013", NAVY),
    ("~$15 million a year", "the wrong-site share of it: one in\nfour paid never-event claims\nis wrong site", "Mehtsun 2013, derived", NAVY),
    ("$136,453", "mean closed wrong-site claim,\none US carrier, 2013–2020;\nspine the commonest (22 %)", "Tan 2023, n = 68", NAVY),
    ("$75,220", "median never-event payment,\n1991–2025\n(IQR \\$28,847 to \\$215,003)", "Bettis 2026", NAVY),
    ("81 % paid", "of litigated wrong-disc-level\ncases; surgeons prevailed in\n42 % of jury trials", "Goodkin & Laska 2004, n = 68", RED),
    ("17 %  ·  1 in 5", "of wrong-level events reach\nlegal action; spine surgeons\never sued for wrong level or side", "Mody 2008; Groff 2013", RED),
    ("£7 million", "23 wrong-site or wrong-level\nclaims among 978 English spinal\nclaims (£535.5 million), 2012–17", "Machin 2018", NAVY),
    ("£4.8 million", "111 NHS orthopaedic wrong-site\nclaims 1995–2010; 23 wrong spinal\nlevel; mean £43,596, 89 % paid", "Harrison 2015", NAVY),
    ("$1,750–1,950", "per patient: 52 minutes of\noperating-room time to place a\ngold fiducial, at $34–37 a minute", "AJNR 2023; Childers 2018", GOLD),
    ("~$100,000 a year", "179 fiducial patients over 38\nmonths at one centre: 56 a year,\n155 staffed hours, ~$350,000", "AJNR 2023, derived", GOLD),
    ("420–1,900 a year", "US wrong-level spine operations,\nfrom 1 in 3,110 self-reported\nand 0.12 % registry rates", "derived, unpublished", GREY),
    ("$8–37 million", "a year, US indemnity for those\nalone, before reoperation, added\nstay and disability", "derived, unpublished", GREY),
]
cols_, rows_ = 4, 3
fig = plt.figure(figsize=(14.0, 6.6))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, cols_); ax.set_ylim(0, rows_); ax.set_axis_off()
for i, (num, lab, src, col) in enumerate(tiles):
    r_, c_ = divmod(i, cols_)
    x, y = c_, rows_ - 1 - r_
    ax.add_patch(FancyBboxPatch((x + 0.02, y + 0.03), 0.96, 0.94, boxstyle="round,pad=0,rounding_size=0.025", fc=LIGHT, ec="none"))
    ax.add_patch(FancyBboxPatch((x + 0.02, y + 0.83), 0.96, 0.14, boxstyle="round,pad=0,rounding_size=0.025", fc=col, ec="none"))
    ax.text(x + 0.5, y + 0.90, src, ha="center", va="center", fontsize=14, color="white")
    fs = 32 if len(num) <= 12 else 27 if len(num) <= 16 else 24
    ax.text(x + 0.5, y + 0.66, num, ha="center", va="center", fontsize=fs, fontweight="bold", color=col if col != GREY else INK)
    ax.text(x + 0.5, y + 0.30, lab, ha="center", va="center", fontsize=15.5, color=INK, linespacing=1.22)
save(fig, "board_wrongsite_cost.png", pad=0.0)

# ------------------------------------------------------------------ 2. the level map, wide
mp = np.load(SN / "results" / "figure2" / "figure2_map.npz", allow_pickle=True)
FT = json.load(open(SN / "results" / "figure2" / "figure2_transitional.json"))
M = json.load(open(SN / "results" / "figure2" / "figure2_metrics.json"))
T, y, g = mp["tsne"], mp["y"].astype(int), mp["group"].astype(str)
classes = list(mp["classes"].astype(str))
HUE = {"cervical": "#2a78d6", "thoracic": "#eb6834", "lumbar": "#1baf7a"}
SACRUM, RING, CONTEXT, GRID, BLACK = "#52514e", "#8a8a8a", "#d4d4d4", "#e3e3e3", "#000000"


def region(n):
    return "cervical" if n.startswith("C") else "thoracic" if n.startswith("T") else "lumbar" if n.startswith("L") else "sacrum"


def level_colour(name):
    if name == "sacrum":
        return to_rgb(SACRUM)
    reg = region(name); base = np.array(to_rgb(HUE[reg]))
    members = [c for c in classes if region(c) == reg]
    t = members.index(name) / max(len(members) - 1, 1)
    col = base + (1.0 - base) * 0.40 * max(0.5 - t, 0.0) * 2.0
    col = col * (1.0 - 0.40 * max(t - 0.5, 0.0) * 2.0)
    return tuple(np.clip(col, 0, 1))


L6 = classes.index("L6"); SAC = classes.index("sacrum")
held = g == "heldout_l6_patients"; val = g == "validation"
lf = np.zeros(len(y), bool); lf[FT["map_rows_last_free"]] = True
assert np.all(val[lf]) and np.all(y[lf] == classes.index(FT["fused_L5"]["target_level"]))
S = {"ring": held & (y != L6), "l6": val & (y == L6), "star": held & (y == L6), "lastfree": lf}


def window_of(sets, aspect, pad=0.06):
    los, his = [], []
    for m, (plo, phi) in sets:
        los.append(np.percentile(T[m], plo, axis=0)); his.append(np.percentile(T[m], phi, axis=0))
    lo, hi = np.min(los, 0), np.max(his, 0)
    span = hi - lo
    lo, hi = lo - pad * span, hi + pad * span
    w, h = hi - lo
    if w / h < aspect:
        grow = (aspect * h - w) / 2; lo[0] -= grow; hi[0] += grow
    else:
        grow = (w / aspect - h) / 2; lo[1] -= grow; hi[1] += grow
    return lo, hi


def draw_marked(ax, s_l6, s_star, s_ring, s_dia):
    m = S["ring"]; ax.scatter(T[m, 0], T[m, 1], s=s_ring, marker="o", facecolors="none", edgecolors=RING, linewidths=0.8, zorder=2)
    m = S["l6"]; ax.scatter(T[m, 0], T[m, 1], s=s_l6, marker="^", c=BLACK, edgecolors="white", linewidths=0.5, zorder=3)
    m = S["star"]; ax.scatter(T[m, 0], T[m, 1], s=s_star, marker="*", facecolors="white", edgecolors=BLACK, linewidths=0.8, zorder=4)
    m = S["lastfree"]; ax.scatter(T[m, 0], T[m, 1], s=s_dia, marker="D", facecolors="white", edgecolors=BLACK, linewidths=1.3, zorder=5)


W, H = 15.2, 5.0
AW, AH = 5.0, 4.75            # panel a axes (in)
BW, BH = 4.3, 4.75            # panel b axes (in)
win = window_of([(val & (y == L6), (2, 98)), (val & (y == SAC), (2, 98)), (S["star"], (10, 90)), (S["lastfree"], (0, 100))], aspect=BW / BH)
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0.15 / W, 0.15 / H, AW / W, AH / H])
cols = np.array([level_colour(c) for c in classes])
o = np.random.default_rng(0).permutation(np.where(val & (y != L6))[0])
ax.scatter(T[o, 0], T[o, 1], s=2.2, c=cols[y[o]], lw=0, alpha=0.85, rasterized=True, zorder=1)
draw_marked(ax, s_l6=16, s_star=44, s_ring=7, s_dia=26)
lo, hi = win
ax.add_patch(Rectangle(lo, hi[0] - lo[0], hi[1] - lo[1], fill=False, ec=BLACK, lw=1.4, zorder=6))
ax.set_aspect("equal", adjustable="datalim"); ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color(GRID)
# panel b
bx = fig.add_axes([(0.15 + AW + 0.25) / W, 0.15 / H, BW / W, BH / H])
L4_TINT = tuple(np.array(to_rgb(HUE["lumbar"])) + (1 - np.array(to_rgb(HUE["lumbar"]))) * 0.55)
shown = {"L4": L4_TINT, "L5": to_rgb(HUE["lumbar"]), "sacrum": to_rgb(SACRUM)}
ctx = val & ~np.isin(y, [classes.index(k) for k in shown] + [L6])
bx.scatter(T[ctx, 0], T[ctx, 1], s=7, c=CONTEXT, lw=0, rasterized=True, zorder=0)
for lev, col in shown.items():
    m = val & (y == classes.index(lev)) & ~S["lastfree"]
    bx.scatter(T[m, 0], T[m, 1], s=9, c=[col], lw=0, rasterized=True, zorder=1)
draw_marked(bx, s_l6=50, s_star=130, s_ring=26, s_dia=70)
bx.set_xlim(lo[0], hi[0]); bx.set_ylim(lo[1], hi[1]); bx.set_xticks([]); bx.set_yticks([])
for sp in bx.spines.values():
    sp.set_color(BLACK); sp.set_linewidth(1.2)


def mode_point(P, r):
    d = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    return P[int(np.argmax((d < r).sum(1)))]


inside = (T[:, 0] > lo[0]) & (T[:, 0] < hi[0]) & (T[:, 1] > lo[1]) & (T[:, 1] < hi[1])
r = 0.06 * float(np.min(hi - lo))
marked_pts = T[(S["l6"] | S["star"] | S["lastfree"]) & inside]
for lev, off, ha in (("L4", (14, 14), "left"), ("L5", (16, -6), "left"), ("L6", (18, 10), "left"), ("sacrum", (-16, 14), "right")):
    m = val & (y == classes.index(lev)) & inside
    if lev == "L4":
        m &= ~S["lastfree"]
    if not m.any():
        continue
    p = mode_point(T[m], r)
    bx.annotate(lev, p, xytext=off, textcoords="offset points", fontsize=20, fontweight="bold", ha=ha, va="center",
                bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.9), zorder=8, annotation_clip=True)
# the third column: colour key, markers, numbers
kx0 = (0.15 + AW + 0.25 + BW + 0.45) / W; kw = (W - 0.15) / W - kx0
present = [c for c in classes if c != "T13"]
sw = kw / len(present); ky = 4.35 / H
for i, c in enumerate(present):
    fig.patches.append(Rectangle((kx0 + i * sw, ky), sw, 0.3 / H, transform=fig.transFigure, fc=level_colour(c), ec="none"))
for c in ("C1", "T1", "L1"):
    i = present.index(c)
    fig.text(kx0 + i * sw, ky - 0.05 / H, c, fontsize=20, fontweight="bold", ha="left", va="top")
fig.text(kx0 + kw, ky + 0.35 / H, "sacrum", fontsize=20, fontweight="bold", ha="right", va="bottom")
n6 = int(len(set(mp["person"][S["l6"]].astype(str)))); nf = FT["fused_L5"]["last_free"]["n_persons"]
nstar_p = int(len(set(mp["person"][S["star"]].astype(str))))
handles = [Line2D([], [], marker="^", ls="none", ms=12, mfc=BLACK, mec="white", label=f"L6, validation ({n6} people)"),
           Line2D([], [], marker="D", ls="none", ms=10, mfc="white", mec=BLACK, mew=1.3, label=f"L4 above a fused L5 ({nf} people)"),
           Line2D([], [], marker="*", ls="none", ms=17, mfc="white", mec=BLACK, label=f"L6 by one labeller, never seen ({nstar_p} patients)"),
           Line2D([], [], marker="o", ls="none", ms=8, mfc="none", mec=RING, label="their other vertebrae")]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(kx0 - 0.01, 3.55 / H), fontsize=18, frameon=False,
           handletextpad=0.4, borderaxespad=0.0, labelspacing=0.55, handlelength=1.4)
nn = M["nearest_other_person"]
fig.text(kx0, 1.35 / H, f"{M['map']['n']['validation']:,} crops of {nn['persons']:,} people, validation split",
         fontsize=17, color=GREY, ha="left", va="top")
fig.text(kx0, 0.95 / H, "nearest crop of another person:", fontsize=17, color=INK, ha="left", va="top")
fig.text(kx0, 0.58 / H, f"same level {100 * nn['same_level']:.1f} %, within one level {100 * nn['within_one']:.1f} %",
         fontsize=17, color=INK, ha="left", va="top")
fig.text((0.15 + 0.06) / W, (0.15 + AH - 0.06) / H, "a", fontsize=22, fontweight="bold", va="top", ha="left")
fig.text((0.15 + AW + 0.25 + 0.06) / W, (0.15 + BH - 0.06) / H, "b", fontsize=22, fontweight="bold", va="top", ha="left",
         bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
save(fig, "fig2_wide.png")
print("window", [round(float(v), 2) for v in lo], [round(float(v), 2) for v in hi], "L6 people", n6, "star patients", nstar_p, "fused", nf)


# ------------------------------------------------------------------ 3. the modality table, wide
def wide_table(name, header, rows, colw, fig_w, fs=17, head_h=1.05, row_h=0.6):
    Wt = sum(colw); Hh = head_h + row_h * len(rows) + 0.06
    fig = plt.figure(figsize=(fig_w, fig_w * Hh / Wt))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, Wt); ax.set_ylim(-Hh, 0); ax.set_axis_off()
    ax.add_patch(Rectangle((0, -head_h), Wt, head_h, facecolor=NAVY, edgecolor="none"))
    x = 0
    for j, (h_, w_) in enumerate(zip(header, colw)):
        if isinstance(h_, tuple):
            ax.text(x + w_ / 2, -head_h / 2 + 0.22, h_[0], ha="center", va="center", fontsize=fs, fontweight="bold", color="white",
                    linespacing=1.1)
            ax.text(x + w_ / 2, -head_h + 0.22, h_[1], ha="center", va="center", fontsize=fs * 0.72, color="#D6DCF0")
        else:
            ax.text(x + 0.15, -head_h / 2, h_, ha="left", va="center", fontsize=fs, fontweight="bold", color="white")
        x += w_
    yy = -head_h
    for i, row in enumerate(rows):
        yy -= row_h
        if i % 2 == 0:
            ax.add_patch(Rectangle((0, yy), Wt, row_h, facecolor="#F4F6FB", edgecolor="none"))
        x = 0
        for j, (cell, w_) in enumerate(zip(row, colw)):
            if j == 0:
                ax.text(x + 0.15, yy + row_h / 2, cell, ha="left", va="center", fontsize=fs, fontweight="bold", color=INK)
            else:
                ax.text(x + w_ / 2, yy + row_h / 2, cell, ha="center", va="center", fontsize=fs, color=INK)
            x += w_
    save(fig, name, pad=0.0)


wide_table("table_modalities.png",
           ["", ("CT, rendered\nas radiographs", "3,111 scans, 3 collections"),
            ("Plain films\nwith levels", "8,927 persons, 3 collections"),
            ("Mobile C-arm\nfluoroscopy, real", "148 cases, 6 cadavers, 1 phantom"),
            ("Radiotherapy kV\nimager, real", "145 patients, planning CT truth")],
           [("images", "4,093", "9,108", "778", "3,498"),
            ("transitional, human-read", "191 persons", "none", "3 cases", "none")],
           [3.4, 3.6, 3.6, 4.0, 3.6], 15.2, fs=18, head_h=1.55, row_h=0.62)

# ------------------------------------------------------------------ 4. the occlusion maps, 2 x 2 portrait
z = np.load(SN / "results" / "figure2" / "occlusion_clean" / "gradcam.npz", allow_pickle=True)
FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 72)
tiles_ = []
for lvl in ["T12", "L4", "L5", "L6"]:
    img = z[f"v9_val__{lvl}__rep_img"].astype(np.float32) / 255.0
    occ = z[f"v9_val__{lvl}__mean_occlusion"].astype(np.float32)
    occ = np.clip(occ, 0, None); occ = occ / (occ.max() + 1e-9)
    marker = z[f"v9_val__{lvl}__rep_marker"]
    rgb = np.stack([img, img, img], axis=2)
    alpha = (occ ** 0.8)[..., None] * 0.75
    rgb = rgb * (1 - alpha) + np.array([0.94, 0.27, 0.15])[None, None, :] * alpha
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize((640, 640), Image.LANCZOS)
    ys, xs = np.where(marker > 0)
    dr = ImageDraw.Draw(im)
    if len(xs):
        s_ = 640 / marker.shape[0]
        dr.rectangle([xs.min() * s_, ys.min() * s_, xs.max() * s_, ys.max() * s_], outline="white", width=6)
    tile = Image.new("RGB", (640, 640 + 100), "white")
    tile.paste(im, (0, 100))
    d2 = ImageDraw.Draw(tile)
    tw = d2.textlength(lvl, font=FONT)
    d2.text(((640 - tw) / 2, 10), lvl, fill=(0x19, 0x1D, 0x63), font=FONT)
    tiles_.append(tile)
grid = Image.new("RGB", (2 * 640 + 30, 2 * 740 + 30), "white")
for i, t in enumerate(tiles_):
    r_, c_ = divmod(i, 2)
    grid.paste(t, (c_ * 670, r_ * 770))
grid.save(OUT / "occlusion_2x2.png")
print("occlusion_2x2", grid.size, round(grid.size[0] / grid.size[1], 2))

# ------------------------------------------------------------------ 5. the check panel at column size
d = json.load(open(SN / "results" / "fig4_frames" / "case42_LAT.couple.json"))
fr = Image.open(SN / "results" / "fig5_frames" / "case42_LAT.png").convert("L")
fr = ImageOps.autocontrast(fr, cutoff=0.5).convert("RGB")
X0, X1 = 330, 960
crop = fr.crop((X0, 0, X1, 1024))
FW = crop.width; TXW = 660; FOOT = 170
panel = Image.new("RGB", (FW + TXW, 1024 + FOOT), "white")
panel.paste(crop, (0, 0))
dr = ImageDraw.Draw(panel)
F = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 58)
FH = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 62)
FS = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 46)
FN = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
NAVY_T, BLUE_T, RED_T, GREY_T, WHITE = (0x19, 0x1D, 0x63), (0x4C, 0x70, 0xB7), (0xEF, 0x46, 0x27), (0x8A, 0x8A, 0x8A), (255, 255, 255)
cx = FW + 24
dr.text((cx, 8), "shape", font=FH, fill=NAVY_T)
dr.text((cx + 320, 8), "count", font=FH, fill=GREY_T)
dr.text((cx + 520, 8), "call", font=FH, fill=NAVY_T)
ax0, ay0, ax1, ay1 = d["anchor"]["box"]
dr.rectangle([ax0 - X0, ay0, min(ax1, X1) - X0 - 4, ay1 - 4], outline=(20, 20, 20), width=7)
dr.rectangle([ax0 - X0 + 6, ay1 - 70, min(ax1, X1) - X0 - 10, ay1 - 10], fill=(20, 20, 20))
dr.text((ax0 - X0 + 16, ay1 - 66), "sacrum, anchor", font=FN, fill=WHITE)
for b in d["bodies"]:
    x0, y0, x1, y1 = b["box"]
    x0 -= X0; x1 -= X0
    bad = b["disagree"]
    col = RED_T if bad else BLUE_T
    dr.rectangle([x0, y0, x1, y1], outline=col, width=7)
    dr.rectangle([x0, y0, x0 + 62, y0 + 56], fill=col)
    dr.text((x0 + 14, y0 + 2), str(b["ordinal"]), font=F, fill=WHITE)
    yc = (y0 + y1) // 2 - 30
    shape = "none" if b["abstain"] else b["classifier"]
    dr.text((cx, yc), f"{shape} {b['p_classifier']:.2f}", font=F, fill=(RED_T if bad else NAVY_T))
    dr.text((cx + 320, yc), b["count"], font=F, fill=GREY_T)
    dr.text((cx + 520, yc), b["coupled"], font=F, fill=(RED_T if bad else NAVY_T))
    dr.line([x1, (y0 + y1) // 2, FW + 12, yc + 30], fill=col, width=3)
dr.text((16, 1024 + 18), f"L6 alphabet {d['candidates']['L6']:.2f} against ordinary {d['candidates']['ordinary']:.2f}: call {d['call']}", font=FS, fill=GREY_T)
dr.text((16, 1024 + 92), "body 1: shape and count disagree, the read stopped", font=ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 50), fill=RED_T)
panel.save(OUT / "render_case42_check.png")
print("render_case42_check", panel.size, round(panel.size[0] / panel.size[1], 2), "call", d["call"], "flag", d["flag_disagree"])
print("done")
