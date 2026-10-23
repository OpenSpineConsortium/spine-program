"""paper/cns2026/make_cns_deck_v10.py — the CNS 2026 talk on the official speaker template, version 10 (Greg
2026-09-26: Result 1 and Result 2 looked like identical slides, two navy tables with one highlighted row).

Changes from v9: Result 1 is a line chart (chart_fov_lines.png, prep_v15_figs.py), exact level against what is in
the field, lateral and anteroposterior, tuned and never-trained-on-this-C-arm, with the surgeons-with-a-registration-
overlay 97.6 % as a dashed reference; the published-methods table is gone from the slides and its numbers sit in that
slide's notes. Result 2 is a new result from the paper, the sixth lumbar vertebra (chart_l6.png): L6 named from shape
on the selection split, on renders of ten L6 spines, on renders of three never-seen real L6 patients, and on the
real C-arm frames where L6 was called, flagged and coupled. Everything else as v9.

    python paper/cns2026/prep_v14_figs.py && python paper/cns2026/prep_v15_figs.py && python paper/cns2026/chart_level_sweep.py ...
    python paper/cns2026/make_cns_deck_v10.py
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt

from make_cns_deck_v2 import FIGS2, fit
from make_cns_deck_v4 import (BLUE, BOTTOM, CAP, GAP, GREY, L, NAVY, R, REFS_TOP, TEMPLATE, TOP, WHITE, add_text, arrow,
                              content_slide, fig_left, fig_top, flow_box, navy_bar, picture, refs)
from make_cns_deck_v6 import notes

C_BLUE = RGBColor(0x1F, 0x77, 0xB4)
C_ORANGE = RGBColor(0xE8, 0x71, 0x0A)
C_TEAL = RGBColor(0x2C, 0xA0, 0x89)
C_BLACK = RGBColor(0x20, 0x20, 0x20)
C_MID = RGBColor(0x7F, 0x7F, 0x7F)
OSC_URL = "https://openspineconsortium.com/"
TITLE = "Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model For Preoperative Detection Of Lumbar And Thoracic End Anomalies"
SESSION = "Mini Podium 4, Spine Session 1 (MP4SP1)  ·  Monday 2 November 2026, 5:21–6:00 PM  ·  Podium 4, Ballroom ABC"


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
    for line in (session, "The paper of the same title is accepted at NeurIPS 2026, Datasets and Benchmarks track"):
        p = body.text_frame.add_paragraph()
        p.text = line
    for p in body.text_frame.paragraphs:
        p.space_after = Pt(5)
        for r in p.runs:
            r.font.size = Pt(12); r.font.color.rgb = WHITE

    # ---- 2 where this is going
    s = content_slide(prs, "Where this is going")
    img = FIGS2 / "sn_fig4_b_img.png"
    w, h = fit(img, 3300000, BOTTOM - TOP - 500000)
    picture(s, img, R - w, TOP, w, h)
    add_text(s, R - w, TOP + h + 60000, w, 450000, ["A real lateral C-arm exposure; each body named from its shape, with its probability."], size=CAP, color=GREY, gap=0)
    items = [
        ("Surgeons count vertebrae on the C-arm. On a transitional spine the count is wrong", 820000),
        ("Today's tools map a position on the spine to the preoperative CT to help the surgeon count. Humans still make mistakes", 1000000),
        ("SchwingNet reads the level from the shape of the bones in a limited field of view; with the sacrum in view it also counts, and checks the two against each other; from a sweep of overlapping exposures it reconstructs the spine. Nothing is mapped to the CT", 1450000),
        ("Tested on real intraoperative C-arm exposures: how often it is right, and when it stops", 850000),
        ("What is missing: enough transitional patients' scans to feed the model", 750000),
    ]
    y = TOP
    tw = R - w - GAP - (L + 600000)
    for i, (txt, dy) in enumerate(items, 1):
        box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(L), Emu(y), Emu(460000), Emu(460000))
        box.fill.solid(); box.fill.fore_color.rgb = NAVY; box.line.color.rgb = NAVY; box.shadow.inherit = False
        tf = box.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(i); r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = WHITE
        add_text(s, L + 600000, y - 20000, tw, dy, [txt], size=17, gap=0)
        y += dy

    # ---- 3 the level is counted
    s = content_slide(prs, "The level is counted, and the count is often wrong")
    img = FIGS2 / "cited_strong2022_fig3.png"
    w, h = fit(img, 4300000, 3350000)
    picture(s, img, L, TOP, w, h)
    add_text(s, L, TOP + h + 80000, w, 1200000,
             ["Strong et al. 2022, Figure 3: intraoperative fluoroscopy, needle at the T10 pedicle, counted from the sacrum. J Neurosurg Spine 36:792 (PMC10193475); permission pending."],
             size=CAP, color=GREY, gap=0)
    left = L + w + GAP
    add_text(s, left, TOP, R - left, 2500000, [
        "Half of spine surgeons report a wrong-level operation in their career (Mody 2008; Groff 2013)",
        "Registry of 34,544 operations: 0.12 %, thoracic 0.42 % (Furuya 2026)",
        "The first exposed level is wrong in 4–15 % before the check film; verification protocols miss a third (Ammerman 2006; Dablouk 2019; Longo 2012)",
        "The remedy on offer is another count"], size=15, gap=8)
    cart = FIGS2 / "cartoon_sweep.png"
    cw, ch = fit(cart, R - left, 1250000)
    picture(s, cart, left, TOP + 2600000, cw, ch)
    add_text(s, left, TOP + 2600000 + ch + 50000, R - left, 700000,
             ["A sweep: the C-arm steps up the prone spine, each exposure overlapping the last, and the surgeon counts from the sacrum.",
              "SchwingNet reads the same sweep: a proprietary algorithm reconstructs the spine from the overlapping exposures, so the count is checked at every level in it. Cartoon from the SchwingNet manuscript."],
             size=CAP, color=GREY, gap=2)
    refs(s, "1. Mody MG, et al. Spine 2008;33:194.   2. Groff MW, et al. World Neurosurg 2013;79:585.   3. Furuya M, et al. Bone Joint J 2026;108-B:673.   4. Dablouk MO, et al. Br J Neurosurg 2019.   5. Ammerman JM, et al. Surg Neurol 2006.   6. Longo UG, et al. J Bone Joint Surg Br 2012;94-B:1546.")

    # ---- 4 transitional anatomy changes the count
    fig_top(prs, "Transitional anatomy changes the count", FIGS2 / "big_fig1_ct_row.png", [
        "8.8 % of 3,147 full-length radiographs lack 24 presacral segments (Sabri 2025); in 550 lumbar operations the count was wrong in 38 of 71 patients with a transitional vertebra (Nakagawa 2017)",
        "The truth is on CT. No public radiograph or C-arm frame carries a human-read T13 or Castellvi grade"],
        max_h=3550000, size=14,
        caption="Labelled CT, public de-identified records (CTSpinoPelvic1K). Bar, 20 mm.",
        refs_text="7. Sabri SA, et al. Neurosurg Focus 2025;58(6):E13.   8. Nakagawa T, et al. 2017.   9. Castellvi AE, et al. Spine 1984;9:493.   Figure: SchwingNet manuscript (in preparation), Figure 1.")

    # ---- 5 what a wrong level costs: the board
    s = content_slide(prs, "What a wrong site costs, and what avoiding it costs")
    img = FIGS2 / "board_wrongsite_cost.png"
    w, h = fit(img, R - L, REFS_TOP - 100000 - TOP)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    refs(s, "Mehtsun WT, et al. Surgery 2013;153:465.   Tan et al. Jt Comm J Qual Patient Saf 2023;49:265.   Bettis T, et al. Patient Saf Surg 2026.   Goodkin R, Laska LL. Surg Neurol 2004;61:323.   Mody MG, et al. Spine 2008;33:194.   Groff MW, et al. World Neurosurg 2013;79:585.   Machin JT, et al. Eur Spine J 2018;27:2693.   Harrison WD, et al. Ann R Coll Surg Engl 2015.   AJNR Am J Neuroradiol 2023;44:618.   Childers CP, Maggard-Gibbons M. JAMA Surg 2018;153:e176233.")
    notes(s, ["Every number is from a verified primary source except the four marked derived: the wrong-site share of the NPDB total (one quarter of paid never-event claims are wrong site), the yearly cost of the fiducial series (179 patients over 38.4 months at $34–37 per operating-room minute, 2014 dollars), and the US wrong-level operation and indemnity estimates (the two published per-procedure rates applied to 1.3–1.6 million spine operations a year, with the published litigation and payment fractions).",
              "The $1.3 billion is all surgical never events (retained objects, wrong site, wrong procedure, wrong patient) over 1990–2010; no published wrong-site-only total exists."])

    # ---- 6 the label on the film
    s = content_slide(prs, "The label on the film is only as right as the planning read")
    img = FIGS2 / "cited_levelcheck_composite.png"
    w, h = fit(img, 4900000, REFS_TOP - 80000 - TOP - 650000)
    picture(s, img, L, TOP, w, h)
    add_text(s, L, TOP + h + 60000, w, 650000,
             ["Top: De Silva et al. 2016, Figure 1 (Spine; PMC5045321). Bottom: Manbachi et al. 2018, Figure 6, labels on a 13th rib and a lumbarised S1 (Ann Biomed Eng; PMC9107073). Permission pending."],
             size=CAP, color=GREY, gap=0)
    left = L + w + GAP
    tb = FIGS2 / "table_levelcheck.png"
    tw_, th_ = fit(tb, R - left, 3300000)
    picture(s, tb, left, TOP, tw_, th_)
    add_text(s, left, TOP + th_ + 150000, R - left, 1200000, [
        "Registration scores against the labels it imported. On a transitional spine the label is only as right as the planning read",
        "Nothing published names a level from one exposure alone, and nothing is tested on a transitional spine"], size=13, color=BLUE, gap=6)
    refs(s, "15. Otake Y, et al. Phys Med Biol 2012;57:5485.   16. De Silva T, et al. Spine 2016.   17. Manbachi A, et al. Ann Biomed Eng 2018;46:1548.   18. Peh WCG, et al. 1999.   19. Zhang R, et al. J Xray Sci Technol 2023.   20. Huang Y, et al. Comput Methods Programs Biomed 2022.")

    # ---- 7 the planning read fails where the count fails (the NeurIPS paper)
    fig_left(prs, "The planning read fails where the count fails", FIGS2 / "nas_gt_vs_ts.png", [
        "An open-source whole-body segmenter, unmodified, on 1,152 public CTs (Wasserthal 2023)",
        "Normal anatomy: L5 Dice 0.94. Lumbarization: every label slides one level, L5 Dice 0.29",
        "L6 emitted: 0 of 1,152. Confident, well formed, one level off, no error signal",
        "Published under this talk's title: Not All Spines Are Created Equal, NeurIPS 2026 Datasets and Benchmarks (accepted)"],
        img_w=5600000,
        caption="A lumbarization case with a true L6. Left, ground truth; right, the segmenter's output.",
        refs_text="21. Wasserthal J, et al. Radiol Artif Intell 2023;5:e230024.   22. Schwing GJ, et al. Not All Spines Are Created Equal. NeurIPS 2026 Datasets and Benchmarks (accepted; retrospective).   23. CTSpinoPelvic1K, doi.org/10.5281/zenodo.22139642.")

    # ---- 8 hypothesis and purpose
    fig_top(prs, "Hypothesis and purpose", FIGS2 / "big_fig1_ct_vs_film.png", [
        "Hypothesis: each transitional vertebra has a local shape a network can learn from labelled CT and find on a film",
        "Purpose: name the level from one exposure, and outperform surgeons using registration at level identification. Targets set before scoring: 90 % naming, 85 % variant sensitivity, 97 % detection"],
        max_h=3250000, size=15,
        caption="A sixth lumbar and a four-lumbar spine on labelled CT and on another patient's real film (SchwingNet manuscript, Figure 1; public, de-identified).",
        refs_text="Investigational. Decision support beside the surgeon's count, never a replacement for the check film.")

    # ---- 9 what it learned: level map + modality table
    s = content_slide(prs, "What it learned from public data: one shape per level")
    img = FIGS2 / "fig2_wide.png"
    tb = FIGS2 / "table_modalities.png"
    tw_, th_ = fit(tb, R - L, 1400000)
    w, h = fit(img, R - L, BOTTOM - TOP - th_ - 120000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    picture(s, tb, L + (R - L - tw_) // 2, TOP + h + 120000, tw_, th_)
    notes(s, ["Top: the level model's embedding of 13,009 crops from 1,612 people, coloured by level (a, C1 to sacrum; b, the lumbosacral window: triangles the validation L6, stars the contested L6 of never-seen patients, diamonds the last free vertebra above a fused L5, rings those patients' other vertebrae). Manuscript Figure 2a–b, rendered from the same map file.",
              "The nearest crop from another person is the same level in 74.9 % and within one level in 93.8 %. L6 separates from L5 (silhouette 0.35) as far as L1 from T12 (0.32); 75 of 98 L6 crops were named L6. Preliminary: ten L6 persons, on the split that chose the checkpoint.",
              "Bottom: the training data by modality. CT rendered as radiographs: 802 + 1,935 + 374 scans from three collections, 191 transitional persons. Plain films with levels: 4,963 + 3,600 + 364 persons, none human-read transitional. Mobile C-arm fluoroscopy: 148 intraoperative cases (cone-beam CT truth), 6 cadaver pelves, 1 phantom, 778 frames, 3 transitional cases. Radiotherapy kV imager: 145 patients, 3,498 frames, planning CT truth, 91 screen calls unread.",
              "All public and de-identified. The transitional truth is on CT; no released film or C-arm frame carries a human-read T13 or Castellvi grade. The intraoperative set (148 cases, 2023) is in no training set. Retrospective, analysed April–September 2026."])

    # ---- 10 find, name, check (figures rendered at slide size)
    s = content_slide(prs, "What SchwingNet does: find, name, check")
    heads = ("1 · Find", "2 · Name", "3 · Check")
    subs = (["bodies and sacrum boxed, no name yet"],
            ["named from its shape; red, what the name draws on"],
            ["shape against the count: where they disagree, the read stops"])
    imgs = (FIGS2 / "render_case42_find.png", FIGS2 / "occlusion_2x2.png", FIGS2 / "render_case42_check.png")
    fig_y = TOP + 1150000
    fh = BOTTOM - fig_y
    gapc = 360000
    widths = [fit(im, R - L, fh)[0] for im in imgs]
    scale = min(1.0, (R - L - 2 * gapc) / sum(widths))
    widths = [int(w_ * scale) for w_ in widths]
    xs = [L, L + widths[0] + gapc, L + widths[0] + widths[1] + 2 * gapc]
    for x, cw, head, sub, img in zip(xs, widths, heads, subs, imgs):
        flow_box(s, x, TOP, cw, 480000, head, sub)
        w, h = fit(img, cw, int(fh * scale))
        picture(s, img, x + (cw - w) // 2, fig_y, w, h)
    for x, cw in zip(xs[:2], widths[:2]):
        arrow(s, x + cw + (gapc - 320000) // 2, TOP + 80000)
    notes(s, ["One exposure in. Out, for every body in the field: a level name with its probability; when the sacrum is in the field, the count from it; and a flag when the two disagree. Neither end of the spine is needed, and no label is imported from another study.",
              "Left: the detectors' body boxes (blue) and sacrum box (dashed) on a real lateral frame, no names yet. Middle: occlusion maps for T12, L4, L5, L6 and the sacrum; red, the parts of the crop whose removal changes the name most (manuscript Figure 2d); per unit area the attribution is densest on the target body. Right: the same frame as the left panel with the shape name and its probability, the count from the sacrum and the call on each box; body 1 red, where they disagree and the read stops.",
              "Trained on renders of labelled CT and on annotated radiographs; the intraoperative C-arm is in no training set. The architecture, how the two readings are combined and when the read stops are withheld pending the university invention review. C-ArmLSpine case 42, public, 2023."])

    # ---- 11 how it was tested
    s = content_slide(prs, "How it was tested: real exposures, cone-beam CT truth")
    img = FIGS2 / "big_gallery_trio.png"
    w, h = fit(img, R - L, BOTTOM - TOP - 350000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    add_text(s, L, TOP + h + 60000, R - L, 330000,
             ["Real lateral frames, calls by the cross-validated model; green right, red wrong, orange unscored (the two truth labellers disagree). Needle tip on the named L4. C-ArmLSpine, public, 2023."],
             size=CAP, color=GREY, gap=0)
    notes(s, ["148 intraoperative cases, public, acquired November–December 2023; truth from each patient's cone-beam CT, read by two automatic labellers; 814 of 910 vertebrae agreed and kept. The set is lumbar: the truth withholds T11 and most of T12.",
              "Three readings of the same frames: never trained on this C-arm; fine-tuned by case-grouped folds; fine-tuned by acquisition-day folds. Limited fields of view were cut from the same frames: five, three or one body, with no sacrum in them.",
              "Scored per detected body as exact level; intervals clustered by case; paired differences with exact sign tests, Holm-adjusted over the comparisons named before scoring. Every number in the paper is read by the build from a result file; a patient-keyed gate swept 563 quoted numbers against checkpoint lineages. Retrospective study of public collections, analysed April–September 2026."])

    # ---- 12 Result 1: with nothing to count from (line chart)
    s = content_slide(prs, "Result 1: no sacrum in view, the shape names the level")
    img = FIGS2 / "chart_fov_lines.png"
    w, h = fit(img, 7000000, BOTTOM - TOP - 380000)
    picture(s, img, L, TOP, w, h)
    add_text(s, L, TOP + h + 60000, w, 360000,
             ["Exact level per body against what is in the field; no sacrum in the one-, three- and five-body fields. 148 real intraoperative cases, cone-beam CT truth (manuscript Table 3)."],
             size=CAP, color=GREY, gap=0)
    left = L + w + GAP
    add_text(s, left, TOP, R - left, BOTTOM - TOP, [
        "Three lumbar bodies and nothing else in the field: 93 of 100 named exactly; one body alone, 75. No count is possible there; the name comes from shape",
        "The whole lateral frame reads 97.4 %, at the level of surgeons reading a registration overlay (97.6 %, dashed)",
        "Never trained on this C-arm the lateral view loses one to eleven points; the anteroposterior view needs the C-arm's own cases (43.7 to 96.4 %)"], size=15, gap=12)
    notes(s, ["Case-grouped folds: five bodies in the field 647 of 667 (97.0 %); three bodies 1,079 of 1,159 (93.1 %; 95 % CI 89.2, 96.2); one body 451 of 603 (74.8 %). Never trained on this C-arm: three bodies 970 of 1,159 (83.7 %), one body 385 of 603 (63.8 %). Whole frame, lateral: 601 of 617 fine-tuned (97.4 %), 595 of 617 zero-shot (96.4 %; 92.3, 98.4). Anteroposterior whole frame: 608 of 631 fine-tuned (96.4 %), 276 of 631 zero-shot (43.7 %); three bodies 1,015 of 1,176 (86.3 %).",
              "The published methods, each scored against its own truth (the table that was on the next slide in v9): LevelCheck registration 100 % against the labels it imported from the planning CT; surgeons reading the LevelCheck overlay 97.6 % (Manbachi 2018), the dashed line; registration-free naming Huang 88.3 %, Peh 77.9 to 82.2 %, Zhang 73.3 %. No study is on a transitional spine. Parity with the overlay is suggested, not proven: the paired comparison is a separate study."])

    # ---- 13 Result 1, continued: which levels
    s = content_slide(prs, "Which levels it names: cervical to sacrum, thoracic included")
    sw = json.load(open(FIGS2 / "sweep_curve.json"))
    img = FIGS2 / "chart_level_sweep.png"
    w, h = fit(img, R - L, BOTTOM - TOP - 900000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    add_text(s, L, TOP + h + 60000, R - L, 900000, [
        "Navy: one exposure, exact level by level on the level model's development validation split (rendered CT and films, 15,898 crops, bands of two to nine bodies; the split that chose the checkpoint, not held out).",
        sw["caption"]],
        size=12.5, color=GREY, gap=4)
    notes(s, ["Navy, per-level exact accuracy, mean of three seeds: C1–C7 95–99 %; T1–T4 75–81 %; T5–T9 60–70 %; T10–T12 76–80 %; L1–L5 86–88 %; L6 63 % (150 crops); sacrum 100 %. Source: results/alpha_0.3_seed*/mixed_allspine_v9 head runs, per_level of the random-band row. A development number, not a held-out test; the film sources have no thoracic annotation, so thoracic accuracy is on renders.",
              sw["notes"],
              "The sweep is simulated from CT renders: it has never been run on real C-arm sweeps. The C-ArmLSpine truth removes the thoracolumbar junction, so no real-C-arm thoracic accuracy exists; a thoracic C-arm set, and a real sweep, are the next data need. How the reconstruction is done is withheld pending the university invention review."])

    # ---- 14 Result 2: the sixth lumbar vertebra
    s = content_slide(prs, "Result 2: the sixth lumbar vertebra, named from shape")
    img = FIGS2 / "chart_l6.png"
    w, h = fit(img, R - L, BOTTOM - TOP - 1000000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    add_text(s, L, TOP + h + 60000, R - L, 950000, [
        "On the split that chose the checkpoint, 75 of 98 L6 crops from ten people are named L6, and 111 of 1,012 L5 crops are mis-named L6. Rendered from the CT of three real patients read six-lumbar by one labeller and never seen in training, 84 of 180 crops are named L6 with no label imported from anywhere.",
        "On the real C-arm, L6 was called on three anchored frames of two patients and every call was flagged for the surgeon; shape and count together named all 12 bodies exactly where the count alone named none."],
        size=13, color=GREY, gap=4)
    refs(s, "Selection split of the training bank (not held out); CBCT renders of C-ArmLSpine cases 42, 121 and 136 (never seen); real frames, case-grouped folds. A transitional test set does not exist yet: Result 4. Manuscript Figure 2 and Results.")
    notes(s, ["Every L6 number the manuscript reports, on one chart. Selection split: 75 of 98 L6 crops named L6 (76.5 %), 111 of 1,012 L5 crops mis-named L6 (11.0 %). Ten L6 spines on renders, three seeds: body-level recall 56.1 to 72.4 % (validation split, seen before the freeze). Three never-seen real L6 patients (C-ArmLSpine 42, 121, 136), CBCT renders under six device cards: 84 of 180 crops named L6 (46.7 %); the two-cluster silhouette of their L6 against L5 is 0.10 to 0.16 against 0.34 for the validation L6. Real C-arm, coupled fold models at confidence 0.74: L6 called on 3 of 233 anchored frames (case 139 AP and lateral, case 44 lateral), all flagged; coupled exact on their 12 bodies 12 of 12, the count 0 of 12.",
              "Say plainly: L6 is the rare class, ten people in training, and every real L6 read is on three patients. That is why Result 4 is about collecting enough transitional scans."])

    # ---- 15 Result 3: the stop
    fig_left(prs, "Result 3: when shape and count disagree, it stops", FIGS2 / "render_case42_L6.png", [
        "A patient one CT labeller reads six-lumbar, the other five. Shape names bodies 5 to 2 as L2–L5 (0.89–1.00); the count says L1–L4. Body 1: shape none (0.02), count L5",
        "The call is L6 for the column; body 1 is left unnamed and the read stops",
        "Over all anchored frames: count 97.0 %, shape 97.7 %, together 98.2 % (1,009 bodies). Stopped on 23 of 233 frames, holding five of the six errors and all four L6 calls",
        "A disagreement is reported, not hidden"],
        img_w=5600000, size=15,
        caption="C-ArmLSpine case 42, public; manuscript Figure 4d with the probabilities the system printed on each box; cross-validation fold.",
        refs_text="How the two readings are combined and when the read stops are withheld pending the invention review. No accuracy on this slide is a wrong-level surgery rate.")

    # ---- 16 frames and angles
    fig_left(prs, "Where the frames sat mattered more than how many", FIGS2 / "big_fig5_cd.png", [
        "Unseen device: 80.5 % of bodies found; 93.9 % on truth boxes inside the field",
        "Its own frames: a plateau from 24 (c). One view buys that view only",
        "Renders at two poses find 53 % between them; the same count spread over the arc, 77 % (d)"],
        img_w=7400000, size=15,
        caption="SchwingNet manuscript, Figure 5c–d; render sweep on 40 unseen subjects.")

    # ---- 17 persons and views
    legend = [[("●  NHANES II", C_BLUE)], [("●  BUU-LSPINE", C_ORANGE)], [("▲  CSXA", C_TEAL)],
              [("●  C-arm, lateral", C_BLACK)], [("■  C-arm, anteroposterior", C_MID)],
              [("○  lateral-trained, read on anteroposterior", C_BLACK)], [("✕  both views, all persons", C_BLACK)]]
    fig_left(prs, "How many people it takes, and which view they were shot in", FIGS2 / "big_fig5_b.png", [
        "Film naming rose with training persons: NHANES II 78 → 93 %, BUU-LSPINE 65 → 97 %, CSXA 94 → 99.8 %",
        "C-arm lateral: 93.7 % with no C-arm person. Anteroposterior: 33.8 % with none, 90.8 % with five",
        "Training both views cost neither (98.1 and 97.0 %)"],
        img_w=4700000, legend=legend,
        caption="Exact level against training persons; SchwingNet manuscript, Figure 5b.")

    # ---- 18 Result 4: transitional naming not yet tested; the census claims table alone
    s = content_slide(prs, "Result 4: transitional naming is not yet tested; what the census supplies")
    img = FIGS2 / "table_claims.png"
    w, h = fit(img, R - L, BOTTOM - TOP - 300000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    add_text(s, L, TOP + h + 60000, R - L, 300000,
             ["Wilson 95 % lower bound at the class sums of the whole CT census; green, above the surgeon-assisted overlay's 97.6 %; blue, above the pre-stated 90 %."],
             size=CAP, color=GREY, gap=0)
    notes(s, ["Scored so far: three L6 patients, in cross-validation only; a description, not a test. Today there are 7 candidates on real exposures, none verified.",
              "n: the transitional persons a screen of every collection in the census should find, from published prevalence (Sun 2025; Hanhivaara 2020; Nardo 2012); a case counts only where a film exists. Each cell: the lowest accuracy the data would still support at 95 % confidence at that share of errors. 157 error-free persons are the fewest that clear 97.6 %.",
              "With 870 L6 persons the network may miss 12 and still sit above the overlay's 97.6 %; with all 2,069 transitional persons, 36; the 322 L6 of the screen running now allow 2. Beating it outright needs the paired comparison on the same persons, a separate study."])

    # ---- 19 limitations
    s = content_slide(prs, "Limitations and next steps")
    grid = FIGS2 / "big_figS5_a_grid.png"
    gw, gh = fit(grid, 5300000, BOTTOM - TOP - 450000)
    picture(s, grid, L, TOP, gw, gh)
    add_text(s, L, TOP + gh + 60000, gw, 450000,
             ["The only real rotational acquisition: one patient, 301 frames from lateral to anteroposterior (supplement Figure S5a; bar, 50 mm). Every other real frame sits at one of two poses."],
             size=CAP, color=GREY, gap=0)
    fr = FIGS2 / "gallery_case83.png"
    fx = L + gw + GAP
    fw, fh = fit(fr, R - fx, BOTTOM - TOP - 450000)
    picture(s, fr, fx + (R - fx - fw) // 2, TOP, fw, fh)
    add_text(s, fx, TOP + fh + 60000, R - fx, 450000,
             ["A frame whose truth the two automatic labellers disagree on (orange): unscored. The test's truth is their agreement, not a human read."],
             size=CAP, color=GREY, gap=0)
    notes(s, ["Limitations. One intraoperative device, lumbar; its truth is two automatic labellers agreeing, which removes the thoracolumbar junction and cannot settle a transitional count. Whether 148 cases are 148 people cannot be established; every intraoperative interval is too narrow if they are not. Real frames sit at two poses; one patient's rotational acquisition is the only real arc. The posterior is uncalibrated; the per-level chart is a development split. Retrospective, public data; nothing prospective; not a cleared device.",
              "Next steps. Verify the transitional candidates by two human readers and run the pre-stated test: 35 persons, zero errors. A thoracic C-arm set. A second C-arm, with obliques, held out; the paired comparison with registration on verified at-risk persons. Phantom, cadaver, then human series, in that order, before any operating-room use."])

    # ---- 20 conclusions
    s = content_slide(prs, "Conclusions: three goals, where each stands")
    img = FIGS2 / "chart_headline.png"
    w, h = fit(img, 4000000, 3300000)
    picture(s, img, R - w, TOP, w, h)
    add_text(s, R - w, TOP + h + 40000, w, 300000, ["Exact level on the unseen C-arm."], size=CAP, color=GREY, gap=0)
    add_text(s, L, TOP, R - w - GAP - L, 3400000, [
        [("Name the level with nothing to count from: ", NAVY), ("met on ordinary lumbar anatomy", C_TEAL), (" — 93 % with three bodies in view, 96.4 % zero-shot on the whole frame; thoracic levels named on renders, untested on a real C-arm", NAVY)],
        [("Name it on a transitional spine: ", NAVY), ("not yet shown", RGBColor(0xEF, 0x46, 0x27)), (" — three cross-validation patients; 35 error-free persons needed; the census should supply about 870 L6", NAVY)],
        [("Outperform surgeons using registration: ", NAVY), ("needs the paired study", RGBColor(0xEF, 0x46, 0x27)), (" — 98.2 % coupled beside 97.6 % for surgeons with the overlay, on different test sets", NAVY)]],
        size=16, gap=12)
    navy_bar(s, L, TOP + 3550000, R - L, 850000,
             "A name from shape, checked against the count, with a stop where they disagree", size=20)
    add_text(s, L, TOP + 4500000, R - L, 400000, [
        "Evidence status: investigational; retrospective, public de-identified data; no prospective evaluation; not a cleared device."],
        size=13, color=BLUE, gap=0)

    # ---- 21 acknowledgments, data, the consortium
    s = content_slide(prs, "Acknowledgments and data availability")
    add_text(s, L, TOP, 6300000, BOTTOM - TOP, [
        "With thanks to Patrick Schwing (LSU Health Sciences Center New Orleans); Miraziz Ismoilov and Nizar Alnabahneh (Radiology) and Loren Schwiebert (Computer Science), Wayne State University; and the annotators Ashley Schehr, [student A], [student B], [student C], [student D], [student E], [student F], [student G], [student H], [student I] and [student J]",
        "Data: CTSpinoPelvic1K (doi.org/10.5281/zenodo.22139642) and the public C-arm, radiograph and CT collections under their own licences; all de-identified",
        "Papers: Not All Spines Are Created Equal, NeurIPS 2026 Datasets and Benchmarks (accepted); the CTSpinoPelvic1K dataset article (Medical Physics, submitted); SchwingNet (in preparation)",
        "Funding: NIH NIGMS F30GM147909. No commercial support."], size=14, gap=8)
    logo = FIGS2 / "osc_logo.png"
    lw, lh = fit(logo, 3600000, 1100000)
    pic = picture(s, logo, R - 3600000 + (3600000 - lw) // 2, TOP + 100000, lw, lh)
    pic.click_action.hyperlink.address = OSC_URL
    tb = add_text(s, R - 3600000, TOP + lh + 250000, 3600000, 900000,
                  ["Data, code, weights and the annotator onboarding:", "openspineconsortium.com", "github.com/OpenSpineConsortium"], size=13, gap=3, align=PP_ALIGN.CENTER)
    for p in tb.text_frame.paragraphs:
        for r in p.runs:
            if "openspineconsortium.com" in r.text:
                r.hyperlink.address = OSC_URL
                r.font.bold = True
            if "github.com" in r.text:
                r.hyperlink.address = "https://github.com/OpenSpineConsortium"
    navy_bar(s, R - 3600000, TOP + lh + 1300000, 3600000, 1100000,
             ["Questions", "gregory.schwing@med.wayne.edu"], size=18)

    prs.save(str(out))
    print("wrote", out, "slides:", len(prs.slides))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default=SESSION)
    ap.add_argument("--out", default=str(Path.home() / "OneDrive/Desktop/CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx"))
    a = ap.parse_args()
    build(a.session, Path(a.out))
