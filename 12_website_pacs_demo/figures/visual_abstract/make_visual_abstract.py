# spine-program copy 2026-10-08: from CTSpinoPelvic1K poster/make_visual_abstract.py (untracked in that repository at head 7ddfe38);
# unchanged. It reads panels/*.png and panels/markers*.json beside it (copied) and writes visual_abstract.png/.pdf.
"""visual_abstract.py -- the centre column of the OSC med-ed poster, as a picture.

Four beats: students meet on a call; they work between ITK-SNAP and Colab; the server
refuses a save that violates anatomy, quoting the real check; the corrected labels turn out
to be the findings. Every number, message and image is real.

TWO FAILURE CLASSES, because the review catches both and they are the same underlying
problem -- level identity:

  RIBS, case 0231. The draft called two ribs the TWELFTH ribs. The anchor check said "rib 12
  not incident on T12 -- check the rib number". It was the number: they articulate with a
  LUMBAR vertebra, so they are rib_left_lumbar / rib_right_lumbar (74/75).

  VERTEBRAE, case 0068. One L1 label covered TWO vertebral bodies, so every level beneath
  was named one too high, and L3's mask had 19% of the bone in a stray blob of another
  class. Renumbered L1-L6 against the twelfth rib, with T10-T12 added. The check even
  predicted it: "add L6 if there is a 6th lumbar" -- and there was.

GEOMETRY, since both are easy to get wrong at poster size:
  * Shapes drawn in axes-fraction units on a 13.6 x 3.9 in axes come out stretched ~3:1.
    The call panel works in INCHES at 1:1 so circles are circles and tiles are 16:9.
  * A portrait CT dropped into a landscape frame with aspect="auto" is squashed anatomy.
    place_image() CROPS to the frame and never scales the axes differently.

Sized for the poster's middle column: 14.5 x 30.8 inches.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Ellipse, FancyArrowPatch, FancyBboxPatch,
                                Polygon, Rectangle)

W, H = 14.5, 30.8
INK = "#14213d"
ACCENT = "#0466c8"
RED = "#c1121f"
GREEN = "#1b7f5c"
MUTED = "#6c757d"
PAPER = "#ffffff"
PANEL = "#f4f6f8"
CHROME = "#dfe4ea"
# Windows 11 window furniture
WIN_BAR = "#f3f3f3"
WIN_EDGE = "#d6d6d6"
WIN_TEXT = "#1f1f1f"

M_RIB = json.loads(Path("panels/markers.json").read_text())
M_VER = json.loads(Path("panels/markers_0068.json").read_text())

fig = plt.figure(figsize=(W, H), dpi=150)
fig.patch.set_facecolor(PAPER)


def ax_at(x, y, w, h):
    a = fig.add_axes([x, y, w, h])
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off")
    return a


def card(a, x, y, w, h):
    a.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.02",
                               fc=PANEL, ec=CHROME, lw=1.6, transform=a.transAxes, zorder=1))


def step_label(a, n, text, y=0.94):
    a.add_patch(Circle((0.037, y), 0.026, fc=ACCENT, ec="none", transform=a.transAxes, zorder=5))
    a.text(0.037, y, str(n), ha="center", va="center", color="white",
           fontsize=19, fontweight="bold", transform=a.transAxes, zorder=6)
    a.text(0.082, y, text, ha="left", va="center", color=INK,
           fontsize=27, fontweight="bold", transform=a.transAxes, zorder=6)


def down_arrow(yc):
    a = ax_at(0.0, yc, 1.0, 0.020)
    a.add_patch(Polygon([[0.5, 0.04], [0.472, 0.62], [0.528, 0.62]],
                        closed=True, fc=ACCENT, ec="none", transform=a.transAxes))
    a.plot([0.5, 0.5], [0.62, 0.99], color=ACCENT, lw=5, transform=a.transAxes)


def place_image(rect, png, bias=0.5):
    """Draw an image in a figure-fraction rect WITHOUT distorting it.

    Returns (axes, to_frac); to_frac maps a pixel of the ORIGINAL raster to axes-fraction
    coordinates, so callouts track the anatomy instead of a hand-tuned guess.
    """
    x, y, w, h = rect
    target = (w * W) / (h * H)
    im = mpimg.imread(png)
    ih, iw = im.shape[:2]
    if iw / ih > target:
        nw, nh, ox, oy = int(round(ih * target)), ih, 0, 0
        ox = int((iw - nw) * 0.5)
    else:
        nw, nh = iw, int(round(iw / target))
        ox, oy = 0, int((ih - nh) * bias)
    a = fig.add_axes(rect)
    a.imshow(im[oy:oy + nh, ox:ox + nw])
    a.axis("off")
    return a, (lambda px, py: ((px - ox) / nw, 1.0 - (py - oy) / nh))


def win_window(ax, x, y, w, h, title, icon):
    """A Windows 11 window: squared-off chrome, caption buttons at the RIGHT."""
    bar = 0.052
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.008",
                                fc="white", ec=WIN_EDGE, lw=1.8,
                                transform=ax.transAxes, zorder=3))
    ax.add_patch(Rectangle((x, y + h - bar), w, bar, fc=WIN_BAR, ec="none",
                           transform=ax.transAxes, zorder=4))
    ax.plot([x, x + w], [y + h - bar, y + h - bar], color=WIN_EDGE, lw=1.2,
            transform=ax.transAxes, zorder=5)
    ax.add_patch(Rectangle((x + 0.011, y + h - bar * 0.72), 0.0125, 0.026, fc=icon,
                           ec="none", transform=ax.transAxes, zorder=5))
    ax.text(x + 0.031, y + h - bar / 2, title, ha="left", va="center", color=WIN_TEXT,
            fontsize=14.5, transform=ax.transAxes, zorder=5)
    for i, g in enumerate(["—", "☐", "✕"]):
        ax.text(x + w - 0.075 + i * 0.024, y + h - bar / 2, g, ha="center", va="center",
                color=WIN_TEXT, fontsize=12.5, transform=ax.transAxes, zorder=5)
    return bar


# ======================================================================== header
a = ax_at(0.03, 0.952, 0.94, 0.045)
a.text(0.5, 0.66, "HOW A MEDICAL STUDENT'S EDIT", ha="center", va="center",
       color=INK, fontsize=40, fontweight="bold", transform=a.transAxes)
a.text(0.5, 0.18, "BECOMES PUBLISHED ANATOMY", ha="center", va="center",
       color=ACCENT, fontsize=40, fontweight="bold", transform=a.transAxes)

# ======================================================== 1. the asynchronous call
PW, PH = 0.94 * W, 0.125 * H
a = fig.add_axes([0.03, 0.818, 0.94, 0.125])
a.set_xlim(0, PW); a.set_ylim(0, PH); a.set_aspect("equal"); a.axis("off")
a.add_patch(FancyBboxPatch((0.02, PH * 0.10), PW - 0.04, PH * 0.90 - 0.02,
                           boxstyle="round,pad=0,rounding_size=0.25",
                           fc=PANEL, ec=CHROME, lw=1.6, zorder=1))
step_label(a, 1, "Meet when you can, not on a schedule")

CARD_LO, CARD_HI = PH * 0.10, PH * 0.90
CAP_Y = CARD_LO + 0.36
GX, GY = 0.26, 0.26
grid_hi, grid_lo = CARD_HI - 0.16, CAP_Y + 0.30
TH = (grid_hi - grid_lo - GY) / 2
TW = TH * 16 / 9
x_left = (PW - (4 * TW + 3 * GX)) / 2
names = ["mentor"] + ["student"] * 7
for k in range(8):
    r, c = divmod(k, 4)
    x = x_left + c * (TW + GX)
    y = grid_hi - r * (TH + GY) - TH
    lead = k == 0
    a.add_patch(FancyBboxPatch((x, y), TW, TH, boxstyle="round,pad=0,rounding_size=0.09",
                               fc="#20304a" if lead else "#2b3d5c",
                               ec=ACCENT if lead else "none", lw=3 if lead else 0, zorder=3))
    cx = x + TW / 2
    a.add_patch(Circle((cx, y + TH * 0.60), TH * 0.20, fc="#cfd8e3", ec="none", zorder=4))
    a.add_patch(FancyBboxPatch((cx - TH * 0.35, y + TH * 0.09), TH * 0.70, TH * 0.28,
                               boxstyle="round,pad=0,rounding_size=0.14",
                               fc="#cfd8e3", ec="none", zorder=4))
    if lead:
        a.add_patch(FancyBboxPatch((x + 0.08, y + 0.07), 0.58, 0.20,
                                   boxstyle="round,pad=0,rounding_size=0.09",
                                   fc="#0b1524", ec="none", alpha=0.85, zorder=5))
        a.text(x + 0.37, y + 0.17, "mentor", color="#cfe0f5", fontsize=10,
               ha="center", va="center", zorder=6)
a.text(PW / 2, CAP_Y,
       "16 contributors  ·  10 sub-projects  ·  senior-trainee mentorship  ·  no lab bench",
       ha="center", va="center", color=MUTED, fontsize=19)

down_arrow(0.796)

# ================================================== 2. the two windows they work in
a = ax_at(0.03, 0.638, 0.94, 0.152)
card(a, 0.0, 0.0, 1.0, 0.90)
step_label(a, 2, "Two free tools, and you go back and forth")

wy, wh, ww = 0.145, 0.63, 0.405
x_snap, x_colab = 0.035, 0.56
bar = win_window(a, x_snap, wy, ww, wh, "ITK-SNAP  —  segment", "#2b6cb0")
win_window(a, x_colab, wy, ww, wh, "Google Colab  —  measure", "#e8710a")

place_image([0.03 + (x_snap + 0.010) * 0.94, 0.638 + (wy + 0.010) * 0.152,
             (ww - 0.020) * 0.94, (wh - bar - 0.020) * 0.152],
            "panels/0231_v4.png", bias=0.12)

cells = [("#f7f7f7", ["!pip install ostk", "from ostk import spinopelvic"]),
         ("#eef5ff", ["p = spinopelvic.measure(", "    '0231_label.nii.gz')",
                      "print(p.pelvic_incidence)"]),
         ("#f7f7f7", ["> PI  52.4 deg", "> SS  38.1 deg", "> PT  14.3 deg"])]
cy = wy + wh - bar - 0.035
for fc, lines in cells:
    ch = 0.033 * len(lines) + 0.020
    a.add_patch(FancyBboxPatch((x_colab + 0.020, cy - ch), ww - 0.040, ch,
                               boxstyle="round,pad=0,rounding_size=0.005",
                               fc=fc, ec="#dde3ea", lw=1, transform=a.transAxes, zorder=5))
    for j, ln in enumerate(lines):
        a.text(x_colab + 0.032, cy - 0.024 - j * 0.031, ln, color="#2b3a4a", fontsize=12,
               family="DejaVu Sans Mono", ha="left", va="center",
               transform=a.transAxes, zorder=6)
    cy -= ch + 0.026

# the loop between them: segment, measure, go back and re-segment
mid = (x_snap + ww + x_colab) / 2
a.add_patch(FancyArrowPatch((x_snap + ww + 0.012, wy + wh * 0.60),
                            (x_colab - 0.012, wy + wh * 0.60),
                            arrowstyle="-|>", mutation_scale=34, lw=4.5,
                            color=ACCENT, transform=a.transAxes, zorder=7))
a.add_patch(FancyArrowPatch((x_colab - 0.012, wy + wh * 0.40),
                            (x_snap + ww + 0.012, wy + wh * 0.40),
                            arrowstyle="-|>", mutation_scale=34, lw=4.5,
                            color=ACCENT, transform=a.transAxes, zorder=7))
a.text(mid, wy + wh * 0.685, "measure", ha="center", va="center", color=ACCENT,
       fontsize=13.5, fontweight="bold", transform=a.transAxes, zorder=8)
a.text(mid, wy + wh * 0.315, "re-segment", ha="center", va="center", color=ACCENT,
       fontsize=13.5, fontweight="bold", transform=a.transAxes, zorder=8)
a.text(0.5, 0.055, "nothing to install  ·  nothing to license  ·  runs on a laptop",
       ha="center", va="center", color=MUTED, fontsize=19, transform=a.transAxes)

down_arrow(0.616)

# ============================================================ 3. the server says no
a = ax_at(0.03, 0.398, 0.94, 0.212)
card(a, 0.0, 0.0, 1.0, 0.92)
step_label(a, 3, "The server checks every save", y=0.955)

a.add_patch(FancyBboxPatch((0.04, 0.135), 0.92, 0.735,
                           boxstyle="round,pad=0,rounding_size=0.012",
                           fc="#1c2431", ec="none", transform=a.transAxes, zorder=3))

GROUPS = [
    ("case 0231  ·  rib review", [
        ("right rib 12 not incident on T12 (gap 16 mm)", "check the rib number"),
        ("one rib bone carries multiple labels: rib_left_8, rib_left_9", ""),
        ("left rib 8: in 2 pieces (13 mm apart)", "CONNECT the pieces"),
    ]),
    ("case 0068  ·  spine review", [
        ("L1 covers TWO vertebral bodies (possible L6)", "do not guess a shift — flag it"),
        ("L3 is split into pieces (largest 80% of the bone)", "one bone must be ONE class"),
        ("L3 (id 22) is split into 2 pieces (19% in a stray blob)", "relabel the stray voxels"),
    ]),
]
yy = 0.815
for gname, items in GROUPS:
    a.text(0.065, yy, gname, color="#8fa3bd", fontsize=14.5, family="DejaVu Sans Mono",
           ha="left", va="center", transform=a.transAxes, zorder=5)
    yy -= 0.048
    for msg, hint in items:
        a.text(0.068, yy, "✗", color="#ff6b6b", fontsize=17, fontweight="bold",
               ha="left", va="center", transform=a.transAxes, zorder=5)
        a.text(0.098, yy, msg, color="#e6edf5", fontsize=14, family="DejaVu Sans Mono",
               ha="left", va="center", transform=a.transAxes, zorder=5)
        if hint:
            a.text(0.098, yy - 0.030, f"→ {hint}", color="#ffd166", fontsize=12.5,
                   family="DejaVu Sans Mono", ha="left", va="center",
                   transform=a.transAxes, zorder=5)
            yy -= 0.030
        yy -= 0.052
    yy -= 0.018

a.add_patch(FancyBboxPatch((0.315, 0.155), 0.37, 0.055,
                           boxstyle="round,pad=0,rounding_size=0.012",
                           fc=RED, ec="none", transform=a.transAxes, zorder=6))
a.text(0.50, 0.1825, "SUBMISSION REJECTED", ha="center", va="center", color="white",
       fontsize=19, fontweight="bold", transform=a.transAxes, zorder=7)
a.text(0.5, 0.045,
       "gated server-side — an edit that still violates anatomy cannot enter the dataset",
       ha="center", va="center", color=MUTED, fontsize=19, transform=a.transAxes)

down_arrow(0.376)

# ================================================== 4. the corrections are the findings
P4Y, P4H = 0.014, 0.356
a = ax_at(0.03, P4Y, 0.94, P4H)
card(a, 0.0, 0.0, 1.0, 0.985)
step_label(a, 4, "The corrections turn out to be the findings", y=0.968)


def pair(y_lo, y_hi, fw, heading, left, right, marks_l, marks_r, ids_l, ids_r,
         tag_l, tag_r):
    a.text(0.5, y_hi + 0.019, heading, ha="center", va="center", color=INK,
           fontsize=20, fontweight="bold", transform=a.transAxes, zorder=6)
    out = []
    for k, (png, ids, tag, col, marks) in enumerate(
            [(left, ids_l, tag_l, RED, marks_l),
             (right, ids_r, tag_r, GREEN, marks_r)]):
        px = (0.5 - 0.009 - fw) if k == 0 else (0.5 + 0.009)
        a.add_patch(FancyBboxPatch((px, y_lo), fw, y_hi - y_lo,
                                   boxstyle="round,pad=0,rounding_size=0.010",
                                   fc="white", ec=col, lw=3.2,
                                   transform=a.transAxes, zorder=3))
        ia, to_frac = place_image(
            [0.03 + (px + 0.008) * 0.94, P4Y + (y_lo + 0.008) * P4H,
             (fw - 0.016) * 0.94, (y_hi - y_lo - 0.016) * P4H], png, bias=0.5)
        src = mpimg.imread(png)
        ih, iw = src.shape[:2]
        for rid in ids:
            m = marks.get(rid)
            if not m:
                continue
            fx, fy = to_frac(m["cx"], m["cy"])
            ia.add_patch(Ellipse((fx, fy), (m["x1"] - m["x0"]) / iw * 1.5,
                                 (m["y1"] - m["y0"]) / ih * 1.5, fill=False, ec=col,
                                 lw=4.0, ls=(0, (5, 3)), transform=ia.transAxes, zorder=8))
        a.add_patch(FancyBboxPatch((px, y_lo - 0.052), fw, 0.042,
                                   boxstyle="round,pad=0,rounding_size=0.010",
                                   fc=col, ec="none", transform=a.transAxes, zorder=9))
        # ~0.72 em per character for this bold face; 0.62 clipped the longest tag
        fs = min(15.0, (fw * W * 0.90) * 72.0 / (len(tag) * 0.72))
        a.text(px + fw / 2, y_lo - 0.031, tag, ha="center", va="center", color="white",
               fontsize=fs, fontweight="bold", transform=a.transAxes, zorder=10)
        out.append(ia)
    return out


pair(0.665, 0.905, 0.226, "RIBS  ·  case 0231",
     "panels/0231_v4.png", "panels/0231_v6.png",
     M_RIB["v4"], M_RIB["v6"], ["45", "57"], ["74", "75"],
     "WRONG:  “rib 12”", "RIGHT:  lumbar rib")

pair(0.205, 0.530, 0.146, "VERTEBRAE  ·  case 0068",
     "panels/0068_v5.png", "panels/0068_v6.png",
     M_VER["v5"], M_VER["v6"], ["20", "22"], ["20", "21"],
     "L1 = TWO BODIES", "L1–L6 + T10–T12")

a.text(0.5, 0.105,
       "rib_left_12 → rib_left_lumbar          L1 split into L1 + L2, column renumbered L1–L6",
       ha="center", va="center", color=INK, fontsize=17, fontweight="bold",
       family="DejaVu Sans Mono", transform=a.transAxes, zorder=6)
a.text(0.5, 0.043,
       "Both are the same problem — which level is this? — and both corrections are now\n"
       "labelled classes in CTSpinoPelvic1K v6 (802 CTs, openly licensed).",
       ha="center", va="center", color=INK, fontsize=18, linespacing=1.5,
       transform=a.transAxes)

fig.savefig("visual_abstract.png", dpi=150, facecolor=PAPER)
fig.savefig("visual_abstract.pdf", facecolor=PAPER)
print("wrote visual_abstract.png / .pdf")
