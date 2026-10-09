"""paper/cns2026/prep_v5_figs.py — figures for deck v5 (Greg 2026-09-25 night): supplement Figure S1a (corpus manifold
with source labels) for the materials slide; three real intraoperative frames from the C-ArmLSpine gallery for the
test slide; Figure 4c-d for the two-readings slide; Figure S5 (rotational acquisition against view angle) for the
limitations slide; the Bettis figure alone for the cost slide; a census chart (cumulative expected transitional
persons against CTs screened, with the power targets) for the closing slides. Writes into figs_v2/.

    python paper/cns2026/prep_v5_figs.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
CITED = HERE / "figs_cited"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
FONT_B = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)
NAVY = (0x19, 0x1D, 0x63)
RED = (0xEF, 0x46, 0x27)


def labelled_row(panels, labels, out, gap=36, header=120, font=FONT_B, colors=None):
    h = max(p.height for p in panels)
    panels = [p.resize((int(p.width * h / p.height), h), Image.LANCZOS) for p in panels]
    w = sum(p.width for p in panels) + gap * (len(panels) - 1)
    comp = Image.new("RGB", (w, h + header), "white")
    d = ImageDraw.Draw(comp)
    x = 0
    for i, (p, lab) in enumerate(zip(panels, labels)):
        comp.paste(p, (x, header))
        lines = lab.split("\n")
        lh = 62
        y0 = (header - lh * len(lines)) / 2
        col = (colors[i] if colors else NAVY)
        for j, line in enumerate(lines):
            tw = d.textlength(line, font=font)
            d.text((x + (p.width - tw) / 2, y0 + j * lh), line, fill=col, font=font)
        x += p.width + gap
    comp.save(OUT / out)
    print(out, comp.size)


# 1. Figure S1a: the corpus manifold with every source labelled (panel a of figS1.png, 2100 x 2520)
s1 = Image.open(SN / "figures" / "figS1.png").convert("RGB")
s1.crop((0, 25, 1195, 727)).save(OUT / "big_figS1_a.png")
s1.crop((1210, 430, 2052, 600)).save(OUT / "big_figS1_legend.png")
print("big_figS1_a", s1.crop((0, 25, 1195, 727)).size)

# 2. Three real intraoperative frames from the gallery (2640 x 1420; columns 30-653, 682-1305, 1335-1958, 1987-2610)
g = Image.open(OUT / "sn_carmlspine_gallery.png").convert("RGB")
p1 = g.crop((30, 96, 653, 719))       # case110 lateral, whole frame, 5 right
p2 = g.crop((682, 759, 1305, 1390))   # case119 lateral, 3 vertebrae in field, 3 right
p3 = g.crop((1987, 759, 2610, 1390))  # case83 lateral, 0 right, 4 wrong (one level high)
labelled_row([p1, p2, p3], ["whole frame: 5 of 5 right", "3 in the field: 3 right", "4 wrong, one level high"],
             "big_gallery_trio.png", colors=[NAVY, NAVY, RED])

# 3. Figure 4 c and d (figure4.png 2100 x 2490; c x 0-1060, d x 1060-2100; titles at y 1209, images to 2112)
f4 = Image.open(SN / "figures" / "figure4.png").convert("RGB")
c = f4.crop((0, 1200, 1060, 2112))
d = f4.crop((1060, 1200, 2100, 2112))
comp = Image.new("RGB", (c.width + 40 + d.width, c.height), "white")
comp.paste(c, (0, 0))
comp.paste(d, (c.width + 40, 0))
comp.save(OUT / "big_fig4_cd.png")
print("big_fig4_cd", comp.size)

# 4. Figure S5: panel a (frames at four angles) over panel b (bodies found against view angle, confidence 0.25) + legend
s5 = Image.open(SN / "figures" / "figS4.png").convert("RGB")
a = s5.crop((0, 27, 2100, 571))
b = s5.crop((0, 624, 1060, 1440))          # panel b with its axis labels; the legend is drawn on the slide
a.save(OUT / "big_figS5_a.png")
b.save(OUT / "big_figS5_b.png")
print("big_figS5_a", a.size, "big_figS5_b", b.size)

# 5. Bettis 2026 Figure 1 alone
Image.open(CITED / "bettis2026_fig1.png").convert("RGB").save(OUT / "cited_bettis_fig1.png")

# 6. Census chart: cumulative expected transitional persons against CTs screened, collections in the order screened,
#    with the power targets (22 carriers at 85 %, 35 at-risk persons at 90 %) and what the two labellers have found.
#    Numbers: spinesurg-ct-nnunet/docs/CENSUS_TABLE_2026-09-25.md (screened tier, then the gated collections).
screened = [  # (name, CTs on disk, expected L6, expected four-lumbar, expected T13 low, T13 high)
    ("AbdomenAtlas", 7650, 144, 72, 18.9, 59.0), ("IDC tier 1", 3500, 62, 31, 11.4, 35.5), ("FDG-PET-CT", 901, 19, 10, 4.1, 12.7),
    ("AMOS22", 724, 19, 9, 0, 0), ("PANORAMA", 2026, 52, 26, 0, 0), ("NLST pilot", 501, 0, 0, 2.2, 7.0), ("WAW-TACE", 229, 6, 3, 0, 0),
    ("Kidney", 216, 4, 2, 0.6, 2.0), ("Barts CRL", 213, 5, 3, 0, 0), ("PENGWIN", 341, 1, 1, 0, 0), ("CTPelvic1K", 173, 1, 0, 0, 0),
    ("CURVAS-PDAC", 102, 3, 1, 0, 0), ("CURVAS", 71, 2, 1, 0, 0), ("TS v2 val", 71, 2, 1, 0.2, 0.6), ("AortaSeg60", 56, 1, 1, 0.3, 0.9),
    ("Deep-PSMA", 54, 1, 1, 0.2, 0.8), ("QUADRA-HC", 49, 1, 1, 0.2, 0.7), ("CSI 2014", 21, 0, 0, 0, 0.1)]
gated = [("Merlin", 18317, 447, 224, 2, 7), ("RATIC trauma", 3147, 80, 40, 16, 50), ("CADS", 753, 16, 8, 3, 11),
         ("CT-RATE", 21304, 0, 0, 95, 297), ("INSPECT", 19402, 0, 0, 86, 270)]

plt.rcParams.update({"font.family": "Arial", "font.size": 18, "axes.labelsize": 19, "xtick.labelsize": 16, "ytick.labelsize": 16,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#DDDDDD",
                     "figure.dpi": 220, "savefig.dpi": 220, "savefig.facecolor": "white"})
navy, blue, red, gold, grey = "#191D63", "#4C70B7", "#EF4627", "#FFC42F", "#9A9A9A"
order = sorted(screened, key=lambda r: -r[1]) + sorted(gated, key=lambda r: -r[2])
x, l6, four, t13 = [0], [0], [0], [0]
for n, cts, a6, a4, tl, th in order:
    x.append(x[-1] + cts); l6.append(l6[-1] + a6); four.append(four[-1] + a4); t13.append(t13[-1] + (tl + th) / 2)
n_screened = sum(r[1] for r in screened)
fig, ax = plt.subplots(figsize=(13.0, 6.6))
ax.axvspan(0, n_screened / 1000, color="#EEF1F8", zorder=0)
xs = [max(v, 1) / 1000 for v in x]
ax.plot(xs, [max(v, 1) for v in l6], color=navy, lw=3, marker="o", ms=6, label="sixth lumbar (L6)")
ax.plot(xs, [max(v, 1) for v in four], color=blue, lw=3, marker="o", ms=6, label="four lumbar (sacralised L5)")
ax.plot(xs, [max(v, 1) for v in t13], color=gold, lw=3, marker="o", ms=6, label="thirteenth thoracic (T13), midpoint of the range")
ax.axhline(35, color=red, lw=2, ls="--")
ax.text(x[-1] / 1000, 37, "35 at-risk persons at zero errors: 90 % lower bound", color=red, fontsize=15, va="bottom", ha="right")
ax.axhline(22, color=red, lw=2, ls=":")
ax.text(x[-1] / 1000, 20.5, "22 carriers at zero errors: 85 % sensitivity to the variant", color=red, fontsize=15, va="top", ha="right")
ax.plot([n_screened / 1000], [21], marker="*", ms=24, color=navy, zorder=5)
ax.text(n_screened / 1000 + 0.8, 13, "21 L6 called by both\nlabellers so far", color=navy, fontsize=15, va="center")
ax.text(0.4, 2500, "screened now:\n22 collections, 16,898 CTs", ha="left", va="top", fontsize=16, color=navy)
ax.text(x[-1] / 1000, 2500, "gated, one agreement each:\nMerlin, RATIC, CADS, CT-RATE, INSPECT", ha="right", va="top", fontsize=16, color=grey)
ax.set_yscale("log")
ax.set_ylim(8, 2700)
ax.set_yticks([10, 22, 35, 100, 300, 1000])
ax.set_yticklabels(["10", "22", "35", "100", "300", "1,000"])
ax.set_xlabel("CTs screened, thousands (collections in order of size)")
ax.set_ylabel("expected transitional persons")
ax.set_xlim(0, x[-1] / 1000 + 1)
ax.legend(loc="upper center", frameon=False, fontsize=15, ncol=3, bbox_to_anchor=(0.5, -0.16))
fig.tight_layout()
fig.savefig(OUT / "chart_census_cumulative.png", bbox_inches="tight", pad_inches=0.08)
print("chart_census_cumulative", Image.open(OUT / "chart_census_cumulative.png").size)
print("done")

# 7. ACCME: no trade names on the slide. Two kV-imager sources are labelled by manufacturer in Figure S1a; paint the
#    labels over with generic names at the same weight.
im = Image.open(OUT / "big_figS1_a.png").convert("RGB")
dr = ImageDraw.Draw(im)
font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 44)
for box, text in (((395, 425, 650, 480), "kV imager A"), ((95, 472, 335, 528), "kV imager B")):
    dr.rectangle(box, fill=(255, 255, 255))
    dr.text((box[0] + 4, box[1] + 2), text, font=font, fill=(0, 0, 0))
im.save(OUT / "big_figS1_a.png")
print("figS1a relabelled")
