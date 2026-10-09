"""paper/cns2026/prep_v13_figs.py — for deck v8: the OpenSpineConsortium logo (the site's own SVG mark rendered with
cairosvg beside its wordmark), the field-of-view naming table (Table 3 of the manuscript: exact level by bodies in
the field, case-grouped folds and zero-shot), and the per-level chart with the L6 label moved off its point.

    python paper/cns2026/prep_v13_figs.py
"""
import glob
import json
from pathlib import Path

import cairosvg
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
NAVY, BLUE, PALE, RED, GOLD, GREY, INK, LIGHT = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#8A8A8A", "#191D63", "#EEF1F8"
plt.rcParams["font.family"] = "Arial"
TEAL = "#0E5F58"


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size)


# ------------------------------------------------------------------ 1. the logo: the site's SVG mark + wordmark
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28" width="560" height="560">
  <g fill="none" stroke="{TEAL}" stroke-width="1.6" stroke-linecap="round">
    <path d="M14 3.5 C 10 6, 18 9, 14 12.5 C 10 16, 18 19, 14 24.5" />
    <line x1="8.5" y1="6.2" x2="19.5" y2="6.2" />
    <line x1="8.5" y1="12.5" x2="19.5" y2="12.5" />
    <line x1="8.5" y1="18.8" x2="19.5" y2="18.8" />
  </g>
</svg>'''
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / "osc_mark.png"), output_width=560, output_height=560)
mark = Image.open(OUT / "osc_mark.png").convert("RGBA")
FB = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 150)
FR = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 150)
FS = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 64)
parts = [("Open", FR, (0x1A, 0x1C, 0x18, 255)), ("Spine", FB, (0x0E, 0x5F, 0x58, 255)), ("Consortium", FR, (0x1A, 0x1C, 0x18, 255))]
tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
tw = sum(tmp.textlength(t, font=f) for t, f, _ in parts)
W = 560 + 60 + int(tw) + 40
logo = Image.new("RGBA", (W, 620), (255, 255, 255, 0))
logo.paste(mark, (0, 30), mark)
d = ImageDraw.Draw(logo)
x = 620
for t, f, col in parts:
    d.text((x, 130), t, font=f, fill=col)
    x += tmp.textlength(t, font=f)
d.text((622, 330), "openspineconsortium.com", font=FS, fill=(0x19, 0x1D, 0x63, 255))
logo.save(OUT / "osc_logo.png")
print("osc_logo", logo.size)


# ------------------------------------------------------------------ 2. the field-of-view table
def table_image(name, header, rows, colw, fig_w, fs=15, hl=None, row_h=0.62):
    W = sum(colw); HEAD = 0.75; Hh = HEAD + row_h * len(rows) + 0.1
    fig = plt.figure(figsize=(fig_w, fig_w * Hh / W))
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


rows = [
    (("Whole frame, sacrum in view", "shape alone, 617 bodies"), "97.4 %", "96.4 %"),
    (("Five bodies in the field, no sacrum", "667 bodies"), "97.0 %", "—"),
    (("Three bodies in the field, no sacrum", "1,159 bodies"), "93.1 %", "83.7 %"),
    (("One body in the field, nothing else", "603 bodies"), "74.8 %", "63.8 %"),
    (("Anteroposterior, whole frame", "631 bodies"), "96.4 %", "43.7 %"),
    (("Anteroposterior, three bodies", "1,176 bodies"), "86.3 %", "—"),
]
table_image("table_fov.png", ["what is in the field (lateral unless stated)", "tuned on other cases", "never saw this C-arm"], rows,
            [5.2, 2.5, 2.5], 10.5, fs=15, hl={1, 2, 3}, row_h=0.66)

# ------------------------------------------------------------------ 3. the per-level chart, L6 label moved
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
    dx, dy = (0, 9) if l != "L6" else (-14, -4)
    ax.annotate(f"{m_:.0f}", (x, m_), xytext=(dx, dy), textcoords="offset points", ha="center" if l != "L6" else "right",
                va="bottom" if l != "L6" else "top", fontsize=13, color=INK)
ax.set_xticks(xs); ax.set_xticklabels(order, fontsize=15)
ax.set_ylim(20, 105); ax.set_ylabel("exact level, %", fontsize=19); ax.tick_params(axis="y", labelsize=15)
ax.grid(axis="y", color="#DDDDDD"); ax.set_axisbelow(True)
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
ax.text(0.2, 24, f"n per level {min(nn.values()):,}–{max(nn.values()):,} crops; three seeds (band)", fontsize=13, color=GREY)
fig.tight_layout()
save(fig, "chart_level_accuracy.png")
print("done")
