"""paper/cns2026/prep_cited_figs.py — composites and crops of the published figures used on the SchwingNet talk slides
(Greg 2026-09-25: "pull a figure from the citation and I'll get the attribution rights"). Sources downloaded by
scratchpad fetch_cited.sh from PubMed Central / BMC into figs_cited/; the manuscript's own supplement figures and
Table 3 page from spinesurg-ct-nnunet/SchwingNet/. Writes into figs_v2/.

    python paper/cns2026/prep_cited_figs.py
"""
from pathlib import Path

import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
CITED = HERE / "figs_cited"
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
DOCS = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "docs"


def side_by_side(paths, out, gap=40, height=None):
    ims = [Image.open(p).convert("RGB") for p in paths]
    h = height or min(im.height for im in ims)
    ims = [im.resize((int(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    w = sum(im.width for im in ims) + gap * (len(ims) - 1)
    comp = Image.new("RGB", (w, h), "white")
    x = 0
    for im in ims:
        comp.paste(im, (x, 0))
        x += im.width + gap
    comp.save(OUT / out)
    print(out, comp.size)


def stacked(paths, out, gap=40, width=None):
    ims = [Image.open(p).convert("RGB") for p in paths]
    w = width or max(im.width for im in ims)
    ims = [im.resize((w, int(im.height * w / im.width)), Image.LANCZOS) for im in ims]
    h = sum(im.height for im in ims) + gap * (len(ims) - 1)
    comp = Image.new("RGB", (w, h), "white")
    y = 0
    for im in ims:
        comp.paste(im, (0, y))
        y += im.height + gap
    comp.save(OUT / out)
    print(out, comp.size)


# slide 4: Strong 2022 Figure 3 (MRI + intraoperative fluoroscopy with needle localisation at T10)
Image.open(CITED / "strong2021_fig3.jpg").convert("RGB").save(OUT / "cited_strong2022_fig3.png")
# slide 6: Bettis 2026 Figure 1 (NPDB never-event payment reports 1991-2025) beside AJNR 2023 Figure 1 (fiducial at T4)
side_by_side([CITED / "bettis2026_fig1.png", CITED / "ajnr2023_fig1.jpg"], "cited_cost_composite.png", height=1100)
# slide 7: De Silva 2016 Figure 1 (LevelCheck pipeline with overlay) over Manbachi 2018 Figure 6 (labels on a 13th rib and a lumbarised S1)
stacked([CITED / "desilva2016_fig1.jpg", CITED / "manbachi2018_fig6.jpg"], "cited_levelcheck_composite.png", width=1600)
# slide 10: supplement Figure S1 a-b (corpus manifold, every source)
im = Image.open(SN / "figures" / "figS1.png")
print("figS1", im.size)
im.crop((0, 0, 2100, 1380)).save(OUT / "sn_figS1_ab.png")
# slide 12: the C-ArmLSpine gallery (docs figure) at print resolution
d = fitz.open(DOCS / "figures_carmlspine_gallery.pdf")
d[0].get_pixmap(dpi=200).save(OUT / "sn_carmlspine_gallery.png")
d = fitz.open(DOCS / "figures_carmlspine_results.pdf")
d[0].get_pixmap(dpi=220).save(OUT / "sn_carmlspine_results.png")
# slide 15: Table 3 page, rotated upright (the table is set landscape on a portrait page)
t = Image.open(SN / "tables" / "main_p20.png").convert("RGB").rotate(-90, expand=True)
t.save(OUT / "sn_table3_rotated.png")
print("table3 rotated", t.size)
# slide 18: Figure 5 panel a (Wilson lower bound against transitional test persons)
f5 = Image.open(SN / "figures" / "figure5.png")
f5.crop((0, 0, 1060, 1330)).save(OUT / "sn_fig5_a.png")
# slide 19: Figure S5 (figS4 file) panels a-c with legend
s4 = Image.open(SN / "figures" / "figS4.png")
s4.crop((0, 0, 2100, 1500)).save(OUT / "sn_figS5_abc.png")
print("done")
