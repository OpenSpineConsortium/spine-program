"""paper/cns2026/prep_big_panels.py — single panels cut from the manuscript figures so their lettering scales up on a
slide (Greg 2026-09-25: "what text there is is too small, even the figure legends and axis titles are tiny").
Panel bounds come from the white gutters measured on the PNGs (see the session's gutter scan). Slide-size labels
are drawn with PIL where a figure's own header type would be too small. Writes into figs_v2/.

    python paper/cns2026/prep_big_panels.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
FONT_B = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 52)
FONT_R = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 44)
NAVY = (0x19, 0x1D, 0x63)


def labelled_row(panels, labels, out, gap=36, header=120, font=FONT_B):
    """Panels side by side, each under a big label in the template navy."""
    h = max(p.height for p in panels)
    panels = [p.resize((int(p.width * h / p.height), h), Image.LANCZOS) for p in panels]
    w = sum(p.width for p in panels) + gap * (len(panels) - 1)
    comp = Image.new("RGB", (w, h + header), "white")
    d = ImageDraw.Draw(comp)
    x = 0
    for p, lab in zip(panels, labels):
        comp.paste(p, (x, header))
        lines = lab.split("\n")
        lh = 62
        y0 = (header - lh * len(lines)) / 2
        for i, line in enumerate(lines):
            tw = d.textlength(line, font=font)
            d.text((x + (p.width - tw) / 2, y0 + i * lh), line, fill=NAVY, font=font)
        x += p.width + gap
    comp.save(OUT / out)
    print(out, comp.size)


# Figure 1: the labelled-CT row, four phenotypes (gutters x 551-566, 1085-1100, 1620-1635; row y 148-843)
f1 = Image.open(OUT / "sn_figure1.png").convert("RGB")
cols = [(88, 551), (566, 1085), (1100, 1620), (1635, 2100)]
ct = [f1.crop((x0, 148, x1, 843)) for x0, x1 in cols]
labelled_row(ct, ["Sixth lumbar\n(L6)", "Thirteenth\nthoracic (T13)", "Sacralised L5\n(Castellvi IV)", "Four lumbar\n(Castellvi IIIb)"],
             "big_fig1_ct_row.png", header=170)
real = [f1.crop((x0, 1567, x1, 2260)) for x0, x1 in cols]
labelled_row([ct[0], real[0], ct[3], real[3]], ["L6 on CT", "L6 on film", "Four lumbar\non CT", "Four lumbar\non film"],
             "big_fig1_ct_vs_film.png", header=170)

# Figure 2: panel b, the lumbosacral window with its legend (x 1211-2088, y 41-1340)
f2 = Image.open(OUT / "sn_fig2_ab.png").convert("RGB")
f2.crop((1211, 41, 2088, 1340)).save(OUT / "big_fig2_b.png")
f2.crop((28, 41, 1211, 1115)).save(OUT / "big_fig2_a.png")
print("big_fig2_b", f2.crop((1211, 41, 2088, 1340)).size)

# Figure 5: panel a (Wilson bound, legend inside) and panel b axes (legend drawn on the slide)
f5 = Image.open(OUT / "sn_fig5_ab.png").convert("RGB")
f5.crop((78, 59, 1020, 1050)).save(OUT / "big_fig5_a.png")
f5.crop((1032, 59, 2028, 1027)).save(OUT / "big_fig5_b.png")
print("big_fig5_a/b written")

# Figure 5: panels c and d each with its own legend, side by side at equal height
f5cd = Image.open(OUT / "sn_fig5_cd.png").convert("RGB")
c = f5cd.crop((60, 214, 1030, 1400))
d = f5cd.crop((1045, 214, 2055, 1400))
h = max(c.height, d.height)
c2 = Image.new("RGB", (c.width, h), "white"); c2.paste(c, (0, 0))
d2 = Image.new("RGB", (d.width, h), "white"); d2.paste(d, (0, 0))
labelled_row([c2, d2], ["c  real frames of the device", "d  angle of the render"], "big_fig5_cd.png", header=110)

# Figure 4: panels a and b as pure images with slide-size labels
a = Image.open(OUT / "sn_fig4_a_img.png").convert("RGB")
b = Image.open(OUT / "sn_fig4_b_img.png").convert("RGB")
labelled_row([a, b], ["a  detect", "b  name from shape"], "big_fig4_ab.png", header=110)
print("done")
