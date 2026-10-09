# source-of-copy: CTSpinoPelvic1K repository working tree (public, master; head 7ddfe38 on 2026-10-08), path paper/cns2026/make_cns_deck_v12_public.py; kept out of every commit by .git/info/exclude (45df97d stopped tracking the folder); copied 2026-10-08. Project folder 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
# laptop path on line 376: the --out default; pass --out before running (MANIFEST_LOCAL.md section 3.6)
"""paper/cns2026/make_cns_deck_v12_public.py — the CNS 2026 talk cut back to what is already public, version 12
(Greg 2026-09-26: slide 3's closing line was confusing prose; add the dataset article's validation figures).
Changes from v11: slide 3's navy bar says plainly that today's checks are recounts; two slides after the benchmark
show how the dataset was built (MDPA Fig. 1 and Fig. S1) and that its spinopelvic measures match published supine
CT (MDPA Fig. S2 and Table III). Both figures and every number on them are in the public arXiv v1 (2609.22760).
The figures that carry rib-free counts, count-free naming or per-level morphometry are left out.

v11 (Greg
2026-09-26: "make a disclosure friendly set of slides").

Scope is the one the invention disclosure planned for this talk: CT-side count anomalies, as published in the NeurIPS
2026 camera-ready (public since 24 Sep 2026) and the CTSpinoPelvic1K release. Nothing from the intraoperative-imaging
work: no C-arm frame, result, method or name; no sweep; no count-and-check; no product name; no speaker notes except
the literature notes on the cost board. Slides 3-7 are v10's with the flagged lines removed (slide review of
2026-09-26); slides 8-12 are new and every number on them is asserted against the camera-ready text by
prep_v16_public_figs.py (figs_public/public_numbers.json).

Stays out of git: this folder is excluded in .git/info/exclude of the public repository.

    python paper/cns2026/prep_v16_public_figs.py
    python paper/cns2026/make_cns_deck_v12_public.py
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.util import Emu, Pt

from make_cns_deck_v2 import FIGS2, fit
from make_cns_deck_v4 import (BLUE, BOTTOM, CAP, GAP, GREY, L, NAVY, R, REFS_TOP, TEMPLATE, TOP, WHITE, add_text, arrow,
                              content_slide, fig_left, fig_top, flow_box, navy_bar, picture, refs)
from make_cns_deck_v6 import notes

HERE = Path(__file__).resolve().parent
PUB = HERE / "figs_public"
MPDA = PUB / "mpda"
N = json.load(open(PUB / "public_numbers.json", encoding="utf-8"))
TITLE = "Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model For Preoperative Detection Of Lumbar And Thoracic End Anomalies"
SESSION = "Mini Podium 4, Spine Session 1 (MP4SP1)  ·  Monday 2 November 2026, 5:21–6:00 PM  ·  Podium 4, Ballroom ABC"
PAPER = "Not All Spines Are Created Equal, NeurIPS 2026, Evaluations and Datasets track (accepted)"
REPO = "https://github.com/OpenSpineConsortium/spinopelvic-seg"
REF_NEURIPS = "Schwing GJ, et al. Not All Spines Are Created Equal: How CT Segmenters Fail on Lumbosacral Transitional Vertebrae. NeurIPS 2026 (accepted)."
REF_DATA = "CTSpinoPelvic1K, doi.org/10.5281/zenodo.22139642."

FORBIDDEN = ("SchwingNet", "C-arm", "sweep", "proprietary", "exposure", "render", "registration-free", "cone-beam",
             "local shape", "count from the sacrum", "abstain", "origin")


def alt(shape, text):
    """Alt text that describes the picture rather than naming the file it came from."""
    shape._element.nvPicPr.cNvPr.set("descr", text)
    return shape


def build(session: str, out: Path):
    prs = Presentation(str(TEMPLATE))
    sld = prs.slides._sldIdLst
    RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    for e in list(sld):
        sld.remove(e)
        prs.part.drop_rel(e.get(RID))

    # ---- 1 title
    s = prs.slides.add_slide(prs.slide_layouts[0])
    ph = {p.placeholder_format.idx: p for p in s.placeholders}
    t = ph[0]
    t.left, t.top, t.width, t.height = Emu(5185558), Emu(1050000), Emu(6600000), Emu(2200000)
    t.text_frame.word_wrap = True
    t.text_frame.text = TITLE
    for p in t.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(24); r.font.bold = True; r.font.color.rgb = WHITE
    sub = ph[1]
    sub.left, sub.top, sub.width, sub.height = Emu(5185558), Emu(3350000), Emu(6600000), Emu(900000)
    sub.text_frame.word_wrap = True
    sub.text_frame.text = "Gregory J. Schwing, MD, PhD"
    p = sub.text_frame.add_paragraph()
    p.text = "Department of General Surgery, Detroit Medical Center and Wayne State University, Detroit, MI"
    for i, p in enumerate(sub.text_frame.paragraphs):
        for r in p.runs:
            r.font.size = Pt(20 if i == 0 else 13); r.font.color.rgb = WHITE
    body = ph[10]
    body.left, body.top, body.width, body.height = Emu(5185558), Emu(4400000), Emu(6600000), Emu(1800000)
    body.text_frame.word_wrap = True
    body.text_frame.text = "CNS 2026 Annual Meeting, Washington, DC"
    for line in (session, "Results from: " + PAPER):
        p = body.text_frame.add_paragraph()
        p.text = line
    for p in body.text_frame.paragraphs:
        p.space_after = Pt(5)
        for r in p.runs:
            r.font.size = Pt(12); r.font.color.rgb = WHITE

    # ---- 2 where this is going (CT side only)
    s = content_slide(prs, "Where this is going")
    items = [
        "Surgeons count vertebrae. On a transitional spine the count is wrong",
        "The planning CT is read more and more through an automatic segmenter; the most widely used one has no sixth lumbar class",
        "What it does on a transitional spine, measured on a public benchmark built for the purpose: 802 patients, 33 transitional, Castellvi graded",
        "A released single-shot spine-and-pelvis segmenter: what it repairs, and what it does not",
        "What is missing: enough transitional patients' scans",
    ]
    y = TOP + 100000
    for i, txt in enumerate(items, 1):
        box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(L), Emu(y), Emu(520000), Emu(520000))
        box.fill.solid(); box.fill.fore_color.rgb = NAVY; box.line.color.rgb = NAVY; box.shadow.inherit = False
        tf = box.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(i); r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = WHITE
        add_text(s, L + 700000, y, R - L - 700000, 520000, [txt], size=20, gap=0, anchor=MSO_ANCHOR.MIDDLE)
        y += 930000

    # ---- 3 the level is counted (v10 slide 3 without the sweep cartoon and its caption)
    s = content_slide(prs, "The level is counted, and the count is often wrong")
    img = FIGS2 / "cited_strong2022_fig3.png"
    w, h = fit(img, 4800000, 3900000)
    alt(picture(s, img, L, TOP, w, h), "Strong et al. 2022, Figure 3: fluoroscopy with a needle at the T10 pedicle, levels counted from the sacrum.")
    add_text(s, L, TOP + h + 80000, w, 900000,
             ["Strong et al. 2022, Figure 3: intraoperative fluoroscopy, needle at the T10 pedicle, counted from the sacrum. J Neurosurg Spine 36:792 (PMC10193475); permission pending."],
             size=CAP, color=GREY, gap=0)
    left = L + w + GAP
    add_text(s, left, TOP, R - left, 3600000, [
        "Half of spine surgeons report a wrong-level operation in their career (Mody 2008; Groff 2013)",
        "Registry of 34,544 operations: 0.12 %, thoracic 0.42 % (Furuya 2026)",
        "The first exposed level is wrong in 4–15 % before the check film; verification protocols miss a third (Ammerman 2006; Dablouk 2019; Longo 2012)"], size=17, gap=12)
    navy_bar(s, left, TOP + 3550000, R - left, 1000000,
             "Every check in use today counts the levels again, and a recount fails the same way on a transitional spine", size=17)
    refs(s, "1. Mody MG, et al. Spine 2008;33:194.   2. Groff MW, et al. World Neurosurg 2013;79:585.   3. Furuya M, et al. Bone Joint J 2026;108-B:673.   4. Dablouk MO, et al. Br J Neurosurg 2019.   5. Ammerman JM, et al. Surg Neurol 2006.   6. Longo UG, et al. J Bone Joint Surg Br 2012;94-B:1546.")

    # ---- 4 transitional anatomy changes the count
    s = fig_top(prs, "Transitional anatomy changes the count", FIGS2 / "big_fig1_ct_row.png", [
        "8.8 % of 3,147 full-length radiographs lack 24 presacral segments (Sabri 2025); in 550 lumbar operations the count was wrong in 38 of 71 patients with a transitional vertebra (Nakagawa 2017)",
        "The truth is on CT, where the whole column can be counted and the junction graded (Castellvi 1984)"],
        max_h=3550000, size=15,
        caption="Labelled CT, public de-identified records (CTSpinoPelvic1K). Bar, 20 mm.",
        refs_text="7. Sabri SA, et al. Neurosurg Focus 2025;58(6):E13.   8. Nakagawa T, et al. 2017.   9. Castellvi AE, et al. Spine 1984;9:493.   10. " + REF_DATA)

    # ---- 5 what a wrong level costs: the board (literature only; its notes are the derivations)
    s = content_slide(prs, "What a wrong site costs, and what avoiding it costs")
    img = FIGS2 / "board_wrongsite_cost.png"
    w, h = fit(img, R - L, REFS_TOP - 100000 - TOP)
    alt(picture(s, img, L + (R - L - w) // 2, TOP, w, h), "Published costs of wrong-site surgery and of the checks that prevent it.")
    refs(s, "Mehtsun WT, et al. Surgery 2013;153:465.   Tan et al. Jt Comm J Qual Patient Saf 2023;49:265.   Bettis T, et al. Patient Saf Surg 2026.   Goodkin R, Laska LL. Surg Neurol 2004;61:323.   Mody MG, et al. Spine 2008;33:194.   Groff MW, et al. World Neurosurg 2013;79:585.   Machin JT, et al. Eur Spine J 2018;27:2693.   Harrison WD, et al. Ann R Coll Surg Engl 2015.   AJNR Am J Neuroradiol 2023;44:618.   Childers CP, Maggard-Gibbons M. JAMA Surg 2018;153:e176233.")
    notes(s, ["Every number is from a verified primary source except the four marked derived: the wrong-site share of the NPDB total (one quarter of paid never-event claims are wrong site), the yearly cost of the fiducial series (179 patients over 38.4 months at $34–37 per operating-room minute, 2014 dollars), and the US wrong-level operation and indemnity estimates (the two published per-procedure rates applied to 1.3–1.6 million spine operations a year, with the published litigation and payment fractions).",
              "The $1.3 billion is all surgical never events (retained objects, wrong site, wrong procedure, wrong patient) over 1990–2010; no published wrong-site-only total exists."])

    # ---- 6 the label on the film comes from the planning read
    s = content_slide(prs, "The label on the film is only as right as the planning read")
    img = FIGS2 / "cited_levelcheck_composite.png"
    w, h = fit(img, 4900000, REFS_TOP - 80000 - TOP - 650000)
    alt(picture(s, img, L, TOP, w, h), "De Silva 2016 Figure 1 and Manbachi 2018 Figure 6: level labels carried from the planning CT onto the film.")
    add_text(s, L, TOP + h + 60000, w, 650000,
             ["Top: De Silva et al. 2016, Figure 1 (Spine; PMC5045321). Bottom: Manbachi et al. 2018, Figure 6, labels on a 13th rib and a lumbarised S1 (Ann Biomed Eng; PMC9107073). Permission pending."],
             size=CAP, color=GREY, gap=0)
    left = L + w + GAP
    tb = FIGS2 / "table_levelcheck.png"
    tw_, th_ = fit(tb, R - left, 3300000)
    alt(picture(s, tb, left, TOP, tw_, th_), "Published level-checking methods and what each is scored against.")
    add_text(s, left, TOP + th_ + 150000, R - left, 1200000, [
        "Registration scores against the labels it imported. On a transitional spine the label is only as right as the planning read",
        "So the level is decided on the planning CT, and more and more by a segmenter"], size=13, color=BLUE, gap=6)
    refs(s, "11. Otake Y, et al. Phys Med Biol 2012;57:5485.   12. De Silva T, et al. Spine 2016.   13. Manbachi A, et al. Ann Biomed Eng 2018;46:1548.   14. Peh WCG, et al. 1999.   15. Zhang R, et al. J Xray Sci Technol 2023.   16. Huang Y, et al. Comput Methods Programs Biomed 2022.")

    # ---- 7 the planning read fails where the count fails
    s = fig_left(prs, "The planning read fails where the count fails", FIGS2 / "nas_gt_vs_ts.png", [
        "An open-source whole-body segmenter, unmodified, on 1,152 public CTs (Wasserthal 2023)",
        "Normal anatomy: L5 Dice 0.94. Lumbarization: the labels slide one level, L5 Dice 0.29",
        "L6 emitted: 0 of 1,152. Confident, well formed, one level off, no error signal",
        "Published: " + PAPER],
        img_w=5600000,
        caption="A lumbarization case with a true L6. Left, ground truth; right, the segmenter's output.",
        refs_text="17. Wasserthal J, et al. Radiol Artif Intell 2023;5:e230024.   18. " + REF_NEURIPS)

    # ---- 8 the benchmark
    t1 = N["table1"]
    s = fig_left(prs, "A public benchmark, transitional spines graded", PUB / "chart_pub_castellvi.png", [
        f"CTSpinoPelvic1K: {N['records']} CT records of {N['patients']} patients, spine and pelvis in one mask (CTSpine1K and CTPelvic1K, one screening cohort)",
        "33 transitional patients in six phenotypes: 14 lumbarization, 9 four-lumbar sacralization, 6 full, 2 semi, 2 ambiguous",
        "Castellvi graded by two radiology residents: 27 of 33 agreed (κ 0.74), six settled by consensus",
        "16 of 33 are IIIb, all nine four-lumbar spines among them; only 2 are Type I, so this is the conspicuous end"],
        img_w=3900000, size=16,
        caption="Two-reader consensus Castellvi grade, all 33 transitional patients (NeurIPS 2026, Table 4).",
        refs_text="19. Deng Y, et al. CTSpine1K, 2021.   20. Liu P, et al. CTPelvic1K, 2021.   21. Castellvi AE, et al. Spine 1984;9:493.   22. " + REF_DATA)

    # ---- 9 how the benchmark was built (MDPA Fig. 1, Fig. S1)
    s = content_slide(prs, "How the benchmark was built")
    img = MPDA / "fig_pipeline.png"
    w, h = fit(img, 3000000, REFS_TOP - 100000 - TOP)
    alt(picture(s, img, L, TOP, w, h), "Flow of the dataset construction, from the source CT and label sets to 802 released records.")
    left = L + w + GAP
    hw = MPDA / "fig_hardware.png"
    hw_w, hw_h = fit(hw, R - left, 1700000)
    alt(picture(s, hw, left, TOP, hw_w, hw_h), "Surgical hardware labelled as its own classes: hip arthroplasty, femoral-neck screws, sacroiliac screws, interbody cages.")
    add_text(s, left, TOP + hw_h + 60000, R - left, 300000,
             ["Surgical hardware as its own classes, 11 records (MDPA Fig. S1). Bar, 5 cm."], size=CAP, color=GREY, gap=0)
    add_text(s, left, TOP + hw_h + 500000, R - left, REFS_TOP - 100000 - (TOP + hw_h + 500000), [
        "Two public label sets matched to the CT series each was drawn on; neither source recorded which of the two scans it used",
        "112 spine and 13 pelvic corrections to the source labels",
        "Release gates: geometry and sides from the affine, then every measure in its physiological range",
        "802 records, 33 with a consensus Castellvi grade; public on Zenodo"], size=15, gap=8)
    refs(s, "Figures: CTSpinoPelvic1K dataset article (arXiv 2609.22760, Medical Physics, submitted), Fig. 1 and Fig. S1.   " + REF_DATA)

    # ---- 10 the spinopelvic measures match published supine CT (MDPA Fig. S2, Table III)
    s = content_slide(prs, "Its spinopelvic measures match published CT")
    img = MPDA / "fig_validation.png"
    w, h = fit(img, R - L, 2150000)
    alt(picture(s, img, L + (R - L - w) // 2, TOP, w, h), "Distributions of pelvic incidence, sacral slope and pelvic tilt over 756 records with standing and published CT reference lines.")
    add_text(s, L, TOP + h + 40000, R - L, 300000,
             ["756 of 802 records passing the geometric gates. Dashed, standing radiograph (Vialle 2005); dotted, published supine CT (MDPA Fig. S2)."],
             size=CAP, color=GREY, gap=0)
    rows = [("", "This dataset, supine (n = 756)", "Veilleux 2020 (n = 200)", "Hasegawa 2018 (n = 24)"),
            ("Pelvic incidence", "52.1 ± 11.1°", "52.1°", "53.4°"),
            ("Sacral slope", "36.6 ± 10.6°", "36.5°", "34.1°"),
            ("Pelvic tilt", "15.5 ± 7.9°", "15.6°", "19.2°")]
    ty = TOP + h + 420000
    tw = 6300000
    tbl = s.shapes.add_table(len(rows), 4, Emu(L), Emu(ty), Emu(tw), Emu(1300000)).table
    for j, cw in enumerate((1700000, 1800000, 1400000, 1400000)):
        tbl.columns[j].width = Emu(cw)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = tbl.cell(i, j)
            c.text = v
            c.fill.solid()
            c.fill.fore_color.rgb = NAVY if i == 0 else (RGBColor(0xEE, 0xF1, 0xF8) if i % 2 else WHITE)
            for para in c.text_frame.paragraphs:
                para.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
                for run in para.runs:
                    run.font.size = Pt(13)
                    run.font.bold = i == 0 or j == 0
                    run.font.color.rgb = WHITE if i == 0 else NAVY
    add_text(s, L + tw + GAP, ty, R - (L + tw + GAP), REFS_TOP - 100000 - ty, [
        "Pelvic incidence is a fixed property of the pelvis, so it tests the labels: 52.1° here and in Veilleux's automated supine CT series",
        "Sacral slope and tilt, which depend on posture, sit within 0.1° of the same series"], size=14, gap=8)
    refs(s, "Veilleux NJ, et al. J Bone Joint Surg Am 2020;102:e130.   Hasegawa K, et al. BMC Musculoskelet Disord 2018;19:437.   Vialle R, et al. J Bone Joint Surg Am 2005;87:260.   Dataset article: arXiv 2609.22760, Table III and Fig. S2.")

    # ---- 11 the failure by phenotype
    fig_left(prs, "The segmenter fails by phenotype, one level at a time", PUB / "chart_pub_levels.png", [
        f"Normal anatomy ({t1['Normal']['n']} patients): L1–L5 Dice 0.92–0.94, its published level",
        "Lumbarization (14): falls level by level, L3 0.69, L4 0.39, L5 0.29",
        "Four lumbar bodies (9): every label one level off, 0.265 at L1, 0.001 at L4",
        "Per patient, L5 Dice below 0.5 in 10 of 14 lumbarizations and 9 of 9 four-lumbar spines, against 9 of 750 normal"],
        img_w=5200000, size=16,
        note="The mechanism and how often it occurs; no wrong-level event is attributed to a segmenter",
        caption="Per-level Dice of the unmodified whole-body segmenter by phenotype; n is patients (NeurIPS 2026, Table 1).",
        refs_text="17. Wasserthal J, et al. Radiol Artif Intell 2023;5:e230024.   18. " + REF_NEURIPS)

    # ---- 10 the released model
    s = content_slide(prs, "The released model: spine and pelvis in one pass")
    bw, bh, by = 2700000, 900000, TOP + 150000
    xs = [L, L + (R - L - bw) // 2, R - bw]
    heads = ["CT", "One network, one pass", "Nine classes out"]
    subs = [["Abdominopelvic CT at 0.80 × 0.75 × 0.75 mm"],
            ["nnU-Net, 3-D full resolution; a 256 × 320 × 320 patch holds lumbar spine and pelvis (≈100 GB, one H200)"],
            ["L1–L4, last lumbar (L5 and L6 merged), sacrum, both hips"]]
    for x, hd, sb in zip(xs, heads, subs):
        flow_box(s, x, by, bw, bh, hd, sb)
    for i in range(2):
        arrow(s, (xs[i] + bw + xs[i + 1]) // 2 - 160000, by + bh // 2 - 160000)
    add_text(s, L, TOP + 2350000, R - L, 2300000, [
        "The last lumbar body is one class, L5 and L6 together, the merge VERIDAH uses for its classifier (Möller 2026)",
        "Trained on all 1,153 records: unlabelled regions are ignored, so spine-only and pelvis-only records still teach",
        "Transitional records oversampled to a quarter of the training samples; 5-fold cross-validation; 174 records held out, 7 of them transitional",
        "Weights, trainer and inference code are public"], size=17, gap=10)
    refs(s, "23. Isensee F, et al. Nat Methods 2021;18:203.   24. Möller H, et al. VERIDAH, 2026.   25. " + REF_NEURIPS + "   Code: " + REPO.replace("https://", ""))

    # ---- 11 what it repairs
    g = N["gain"]
    fig_left(prs, "What the merge repairs: the junction and the sacrum", PUB / "chart_pub_gain.png", [
        f"Lumbosacral junction on lumbarization: {g['jxn_ts']} (whole-body segmenter, 3 patients) to {g['jxn_ours']} (the one held-out patient whose truth holds L5 and sacrum)",
        "Last lumbar emitted on 3 of 3 held-out lumbarizations and 167 of 167 normal records",
        f"Sacrum: {g['sacrum_ts']} to {g['sacrum_ours']} (113 held-out records with a sacral mask)",
        "Normal L1–L4: 0.95–0.97"],
        img_w=4900000, size=16,
        note="Different test sets: the whole-body segmenter zero-shot on the cohort, ours on the held-out split",
        caption="Dice, the unmodified whole-body segmenter against the released model (NeurIPS 2026, Tables 1, 5 and 6).",
        refs_text="18. " + REF_NEURIPS)

    # ---- 12 what it does not
    fig_left(prs, "What it does not repair", PUB / "chart_pub_l6.png", [
        f"The same network with an explicit L6 class and L6 oversampling still called most true L6 voxels L5; L6 Dice {N['l6_dice']} against {N['l5_dice']} for L5",
        "The merge moves the collision up: on a four-lumbar spine (one held-out patient) 82.7 % of true L4 voxels were called last lumbar",
        "On lumbarization the upper labels still slide: L2 0.61, L3 0.38, L4 0.21"],
        img_w=4700000, size=16,
        note="A patch never holds both ends of the spine: telling four lumbar bodies from five needs a component that sees the whole column",
        caption="The unmerged control: share of true-L6 voxels called L5, mean of the last 100 of 500 epochs (NeurIPS 2026, section 8.1).",
        refs_text="18. " + REF_NEURIPS)

    # ---- 13 limitations and next steps
    s = content_slide(prs, "Limitations and next steps")
    half = (R - L - GAP) // 2
    navy_bar(s, L, TOP, half, 520000, "Limitations", size=20)
    add_text(s, L, TOP + 650000, half, 3900000, [
        "One cohort: US screening CT, ages 45–75",
        "Phenotypes come from the source annotations, not image reads; Castellvi is a two-resident consensus with no senior read; 2 of 33 are Type I",
        "Seven transitional patients held out; the junction is scorable on one lumbarization",
        "A mechanism, not an outcome: no reader study, no planning simulation"], size=16, gap=10)
    x2 = L + half + GAP
    navy_bar(s, x2, TOP, half, 520000, "Next steps", size=20)
    add_text(s, x2, TOP + 650000, half, 3900000, [
        "More transitional patients: VerSe labels L6 in 460 CTs without a pelvis; completing the sacrum with this segmenter gives a 1,613-volume spinopelvic cohort",
        "This segmenter upstream of VERIDAH's sequence predictor",
        "A senior read of all 33, and a screen of the normal cohort for Type I",
        "Released since the paper (v11): one record per patient, per-level ribs and femora, both Castellvi reads and their consensus"], size=16, gap=10)
    refs(s, "18. " + REF_NEURIPS + "   26. Sekuboyina A, et al. VerSe. Med Image Anal 2021;73:102166.   22. " + REF_DATA)

    # ---- 14 conclusions
    s = content_slide(prs, "Conclusions")
    add_text(s, L, TOP, R - L, 3300000, [
        "The most widely used CT segmenter has no L6: on lumbarization it shifts the lumbar labels one level, confidently, with no error signal",
        "CTSpinoPelvic1K makes that failure measurable: 802 patients, 33 transitional, Castellvi graded, public",
        "Merging L5 and L6 in training restores the junction and the sacrum; adding an L6 class does not",
        "Telling four lumbar bodies from five in one pass is still open"], size=19, gap=12)
    navy_bar(s, L, TOP + 3450000, R - L, 800000, "Report any spine model by phenotype, with each stratum's n", size=21)
    add_text(s, L, TOP + 4400000, R - L, 400000, [
        "Evidence status: retrospective, public de-identified data; small transitional strata, each reported with its n; not a cleared device."],
        size=13, color=BLUE, gap=0)

    # ---- 15 acknowledgments and data
    s = content_slide(prs, "Acknowledgments and data availability")
    add_text(s, L, TOP, 6300000, BOTTOM - TOP, [
        "With thanks to Patrick Schwing (LSU Health Sciences Center New Orleans); Miraziz Ismoilov and Nizar Alnabahneh (Radiology) and Loren Schwiebert (Computer Science), Wayne State University; and the annotators Ashley Schehr, [ten student annotator names withheld]",
        "Data: CTSpinoPelvic1K (doi.org/10.5281/zenodo.22139642), built on CTSpine1K, CTPelvic1K and The Cancer Imaging Archive; all de-identified",
        "Paper: " + PAPER,
        "Funding: NIH NIGMS F30GM147909. No commercial support."], size=14, gap=8)
    logo = FIGS2 / "osc_logo.png"
    lw, lh = fit(logo, 3600000, 1100000)
    pic = alt(picture(s, logo, R - 3600000 + (3600000 - lw) // 2, TOP + 100000, lw, lh), "Open Spine Consortium logo.")
    pic.click_action.hyperlink.address = REPO
    tb = add_text(s, R - 3600000, TOP + lh + 250000, 3600000, 1000000,
                  ["Weights and code:", "github.com/OpenSpineConsortium/spinopelvic-seg", "huggingface.co/OpenSpineConsortium"], size=13, gap=3, align=PP_ALIGN.CENTER)
    for p in tb.text_frame.paragraphs:
        for r in p.runs:
            if r.text.startswith("github.com"):
                r.hyperlink.address = REPO; r.font.bold = True
            if r.text.startswith("huggingface.co"):
                r.hyperlink.address = "https://huggingface.co/OpenSpineConsortium/spinopelvic-seg-checkpoints"
    navy_bar(s, R - 3600000, TOP + lh + 1400000, 3600000, 1100000, ["Questions", "gregory.schwing@med.wayne.edu"], size=18)

    # every picture gets alt text that is not a file name
    for sl in prs.slides:
        for sh in sl.shapes:
            if sh.shape_type == 13:
                d = sh._element.nvPicPr.cNvPr.get("descr", "")
                if d.endswith(".png") or d.endswith(".jpg") or not d:
                    sh._element.nvPicPr.cNvPr.set("descr", "Figure; see the caption on the slide.")

    # nothing from the undisclosed work may appear anywhere in the file's text or notes
    txt = []
    for sl in prs.slides:
        for sh in sl.shapes:
            if sh.has_text_frame:
                txt.append(sh.text_frame.text)
            if sh.shape_type == 13:
                txt.append(sh._element.nvPicPr.cNvPr.get("descr", ""))
        if sl.has_notes_slide:
            txt.append(sl.notes_slide.notes_text_frame.text)
    blob = "\n".join(txt).lower()
    hits = [w for w in FORBIDDEN if w.lower() in blob]
    assert not hits, hits
    prs.save(str(out))
    print("wrote", out, "slides:", len(prs.slides))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default=SESSION)
    ap.add_argument("--out", default=str(Path.home() / "<laptop:Desktop>/CNS2026_Schwing_NotAllSpines_public_v12.pptx"))
    a = ap.parse_args()
    build(a.session, Path(a.out))
