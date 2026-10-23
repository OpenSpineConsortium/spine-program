"""paper/cns2026/make_cns_deck_v7.py — the SchwingNet talk on the official 2026 CNS Annual Meeting speaker template,
version 7 (Greg 2026-09-26, second list). Results restructured against the goal:

  Result 1  it names the level from one exposure without counting from C2 or registering to the CT, on a C-arm it
            never saw: 96.4 % zero-shot, 98.2 % coupled, in the same table as the published methods (surgeons with
            the LevelCheck overlay 97.6 %); different test sets, so parity is suggested, not proven.
  Result 2  when the shape reading and the count from the sacrum disagree it stops: the six-lumbar case; 23 of 233
            frames stopped, holding five of the six errors and all four L6 calls.
  Data      how many people it takes and which views (Figure 5); kept as in v6.
  Result 3  transitional naming on real exposures is not yet tested; what the census would let the talk claim.
  Then limitations, conclusions written as answers to the three goals, thanks.

Other changes: overview item 3 says what the count is (from the sacrum when it is in view; no mapping to CT);
sweep cartoon regenerated to the bottom of the column; cost slide carries Machin 2018 Figure 2 (spinal-surgery
claims by cause, wrong site/level in red) redrawn with slide type; LevelCheck slide is a bigger figure plus a
method / accuracy / error table; hypothesis slide shows the same transitional anatomy on CT and on film; the
learned slide shows the level map with its L6 window and a modality table; find / name / check each with a figure,
the naming column showing the occlusion map (red = what the name draws on). Text taken off a slide is in its
speaker notes. ACCME items as before; Greg sole author.

    python paper/cns2026/prep_v11_figs.py && python paper/cns2026/make_cns_deck_v7.py --session "..."
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
from make_cns_deck_v4 import (BLUE, BODY, BOTTOM, CAP, GAP, GREY, L, NAVY, R, REFS_TOP, TEMPLATE, TOP, WHITE, add_text, arrow,
                              content_slide, fig_left, fig_top, flow_box, navy_bar, picture, refs)
from make_cns_deck_v6 import notes

C_BLUE = RGBColor(0x1F, 0x77, 0xB4)
C_ORANGE = RGBColor(0xE8, 0x71, 0x0A)
C_TEAL = RGBColor(0x2C, 0xA0, 0x89)
C_BLACK = RGBColor(0x20, 0x20, 0x20)
C_MID = RGBColor(0x7F, 0x7F, 0x7F)


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
    t.left, t.top, t.width, t.height = Emu(5185558), Emu(1350000), Emu(6500000), Emu(1800000)
    t.text_frame.word_wrap = True
    t.text_frame.text = "SchwingNet: Naming a Vertebral Level From One C-arm Exposure, Without Counting From C2"
    for p in t.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(28); r.font.bold = True; r.font.color.rgb = WHITE
    sub = ph[1]
    sub.left, sub.top, sub.width, sub.height = Emu(5185558), Emu(3250000), Emu(6500000), Emu(1200000)
    sub.text_frame.word_wrap = True
    sub.text_frame.text = "Gregory J. Schwing, MD, PhD"
    for p in sub.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(20); r.font.color.rgb = WHITE
    body = ph[10]
    body.left, body.top, body.width, body.height = Emu(5185558), Emu(4550000), Emu(6500000), Emu(1600000)
    body.text_frame.word_wrap = True
    body.text_frame.text = "Department of General Surgery, Detroit Medical Center and Wayne State University, Detroit, MI"
    p = body.text_frame.add_paragraph()
    p.text = "CNS 2026 Annual Meeting  ·  Washington, DC  ·  " + session
    for p in body.text_frame.paragraphs:
        p.space_after = Pt(4)
        for r in p.runs:
            r.font.size = Pt(13); r.font.color.rgb = WHITE

    # ---- 2 where this is going
    s = content_slide(prs, "Where this is going")
    img = FIGS2 / "sn_fig4_b_img.png"
    w, h = fit(img, 3300000, BOTTOM - TOP - 500000)
    picture(s, img, R - w, TOP, w, h)
    add_text(s, R - w, TOP + h + 60000, w, 450000, ["A real lateral C-arm exposure; each body named from its shape, with its probability."], size=CAP, color=GREY, gap=0)
    items = [
        ("Surgeons count vertebrae on the C-arm. On a transitional spine the count is wrong", 820000),
        ("Today's tools map a position on the spine to the preoperative CT to help the surgeon count. Humans still make mistakes", 1000000),
        ("SchwingNet reads the level from the shape of the bones in a limited field of view; with the sacrum in view it also counts, and checks the two against each other. Nothing is mapped to the CT", 1350000),
        ("Tested on real intraoperative C-arm exposures: how often it is right, and when it stops", 900000),
        ("What is missing: enough transitional patients' scans to feed the model", 800000),
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

    # ---- 3 the level is counted (Strong figure; text; the sweep cartoon)
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
    add_text(s, left, TOP + 2600000 + ch + 50000, R - left, 600000,
             ["The C-arm steps up the prone spine, each exposure overlapping the last, and the level is counted from the sacrum. Cartoon from the SchwingNet manuscript."],
             size=CAP, color=GREY, gap=0)
    refs(s, "1. Mody MG, et al. Spine 2008;33:194.   2. Groff MW, et al. World Neurosurg 2013;79:585.   3. Furuya M, et al. Bone Joint J 2026;108-B:673.   4. Dablouk MO, et al. Br J Neurosurg 2019.   5. Ammerman JM, et al. Surg Neurol 2006.   6. Longo UG, et al. J Bone Joint Surg Br 2012;94-B:1546.")

    # ---- 4 transitional anatomy changes the count
    fig_top(prs, "Transitional anatomy changes the count", FIGS2 / "big_fig1_ct_row.png", [
        "8.8 % of 3,147 full-length radiographs lack 24 presacral segments (Sabri 2025); in 550 lumbar operations the count was wrong in 38 of 71 patients with a transitional vertebra (Nakagawa 2017)",
        "The truth is on CT. No public radiograph or C-arm frame carries a human-read T13 or Castellvi grade"],
        max_h=3550000, size=14,
        caption="Labelled CT, public de-identified records (CTSpinoPelvic1K). Bar, 20 mm.",
        refs_text="7. Sabri SA, et al. Neurosurg Focus 2025;58(6):E13.   8. Nakagawa T, et al. 2017.   9. Castellvi AE, et al. Spine 1984;9:493.   Figure: SchwingNet manuscript (in preparation), Figure 1.")

    # ---- 5 what a wrong level costs: spinal-surgery claims by cause
    fig_left(prs, "What a wrong level costs, and what avoiding it costs", FIGS2 / "chart_machin_redrawn.png", [
        "978 spinal-surgery negligence claims in England over five years, £535.5 million: wrong site or level is a small share of them (Machin 2018)",
        "17 % of self-reported wrong-level events lead to legal action; 81 % of litigated cases are paid; median never-event payment $75,220 (Mody 2008; Goodkin 2004; Bettis 2026)",
        "Avoiding it: a gold fiducial placed the day before, 52 min and 183 mGy per patient (AJNR 2023)"],
        img_w=6100000, size=14,
        caption="Redrawn from Machin et al. 2018, Figure 2: NHS spinal-surgery negligence claims 2012–2017 by cause, number and estimated cost; values read from the published figure (Eur Spine J, open access).",
        note="Derived, unpublished: roughly 420–1,900 US wrong-level operations a year; indemnity alone about $8–37 million.",
        refs_text="10. Machin JT, et al. Eur Spine J 2018;27:2693.   11. Goodkin R, Laska LL. Surg Neurol 2004;61:323.   12. Bettis T, et al. Patient Saf Surg 2026.   13. AJNR Am J Neuroradiol 2023;44:618.   14. Childers CP, Maggard-Gibbons M. JAMA Surg 2018;153:e176233.")

    # ---- 6 the label on the film: bigger figure, a table of methods
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

    # ---- 7 the planning read fails where the count fails
    fig_left(prs, "The planning read fails where the count fails", FIGS2 / "nas_gt_vs_ts.png", [
        "An open-source whole-body segmenter, unmodified, on 1,152 public CTs (Wasserthal 2023)",
        "Normal anatomy: L5 Dice 0.94. Lumbarization: every label slides one level, L5 Dice 0.29",
        "L6 emitted: 0 of 1,152. Confident, well formed, one level off, no error signal",
        "Not All Spines Are Created Equal, NeurIPS 2026"],
        img_w=5600000,
        caption="A lumbarization case with a true L6. Left, ground truth; right, the segmenter's output.",
        refs_text="21. Wasserthal J, et al. Radiol Artif Intell 2023;5:e230024.   22. Schwing GJ, et al. Not All Spines Are Created Equal. NeurIPS 2026 Datasets and Benchmarks (accepted; retrospective).   23. CTSpinoPelvic1K, doi.org/10.5281/zenodo.22139642.")

    # ---- 8 hypothesis and purpose: the same anatomy on CT and on film
    fig_top(prs, "Hypothesis and purpose", FIGS2 / "big_fig1_ct_vs_film.png", [
        "Hypothesis: each transitional vertebra has a local shape a network can learn from labelled CT and find on a film",
        "Purpose: name the level from one exposure, and outperform surgeons using registration at level identification. Targets set before scoring: 90 % naming, 85 % variant sensitivity, 97 % detection"],
        max_h=3350000, size=15,
        caption="A sixth lumbar and a four-lumbar spine on labelled CT and on another patient's real film (SchwingNet manuscript, Figure 1; public, de-identified).",
        note="Investigational. Decision support beside the surgeon's count, never a replacement for the check film.")

    # ---- 9 what it learned: the level map with its L6 window, and the data by modality
    s = content_slide(prs, "What it learned from public data: one shape per level")
    img = FIGS2 / "big_fig2_ab_side.png"
    w, h = fit(img, 6600000, BOTTOM - TOP - 700000)
    picture(s, img, L, TOP, w, h)
    add_text(s, L, TOP + h + 40000, w, 700000,
             ["The level model's embedding of 13,009 crops from 1,612 people, coloured by level (left, C1 to sacrum; right, the lumbosacral window: triangles L6, stars the contested L6 of never-seen patients). Manuscript Figure 2a–b."],
             size=CAP, color=GREY, gap=0)
    tb = FIGS2 / "table_corpus.png"
    x2 = L + w + GAP
    tw_, th_ = fit(tb, R - x2, 3000000)
    picture(s, tb, x2, TOP, tw_, th_)
    add_text(s, x2, TOP + th_ + 120000, R - x2, BOTTOM - (TOP + th_ + 120000), [
        "All public and de-identified. The transitional truth is on CT; no released film or C-arm frame carries a human-read T13 or Castellvi grade",
        "The intraoperative set (148 cases, cone-beam CT truth, 2023) is in no training set"], size=13, color=BLUE, gap=6)
    notes(s, ["All public and de-identified; retrospective, analysed April–September 2026. 194 transitional persons across the sources, 191 of them on CT; no released film or C-arm frame carries a human-read T13 or Castellvi grade. The intraoperative C-arm set (148 cases, cone-beam CT truth, 2023) is in no training set.",
              "The nearest crop from another person is the same level in 74.9 % and within one level in 93.8 %. L6 separates from L5 (silhouette 0.35) as far as L1 from T12 (0.32); 75 of 98 L6 crops were named L6. Preliminary: ten L6 persons, on the split that chose the checkpoint."])

    # ---- 10 find, name, check: each with its figure
    s = content_slide(prs, "What SchwingNet does: find, name, check")
    colw = 3200000
    gapc = (R - L - 3 * colw) // 2
    xs = [L, L + colw + gapc, L + 2 * (colw + gapc)]
    heads = ("1 · Find", "2 · Name", "3 · Check")
    subs = (["bodies and sacrum boxed;", "no level name yet"],
            ["each body named from its shape;", "red, what the name draws on"],
            ["against the count from the sacrum:", "agree, a name; disagree, a stop"])
    imgs = (FIGS2 / "sn_fig4_a_img.png", FIGS2 / "occlusion_grid.png", FIGS2 / "big_fig4_d.png")
    fig_top_y = TOP + 1250000
    for x, head, sub, img in zip(xs, heads, subs, imgs):
        flow_box(s, x, TOP, colw, 520000, head, sub)
        w, h = fit(img, colw, BOTTOM - fig_top_y)
        picture(s, img, x + (colw - w) // 2, fig_top_y, w, h)
    for x in xs[:2]:
        arrow(s, x + colw + 30000, TOP + 100000)
    notes(s, ["One exposure in. Out, for every body in the field: a level name with its probability; when the sacrum is in the field, the count from it; and a flag when the two disagree. Neither end of the spine is needed, and no label is imported from another study.",
              "Middle: occlusion maps for L4, L5, L6 and the sacrum; red, the parts of the image whose removal changes the name most (manuscript Figure 2d). Per unit area the attribution is densest on the target body; for L4 to L6 more of it falls on the body below than on the target.",
              "Trained on renders of labelled CT and on annotated radiographs; the intraoperative C-arm is in no training set. The architecture, how the two readings are combined and when the read stops are withheld pending the university invention review. Figures: manuscript Figure 4a, 2d and 4d."])

    # ---- 11 how it was tested
    s = content_slide(prs, "How it was tested: real exposures, cone-beam CT truth")
    img = FIGS2 / "big_gallery_trio.png"
    w, h = fit(img, R - L, BOTTOM - TOP - 350000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    add_text(s, L, TOP + h + 60000, R - L, 330000,
             ["Real lateral frames, calls by the cross-validated model; green right, red wrong, orange unscored (the two truth labellers disagree). Needle tip on the named L4. C-ArmLSpine, public, 2023."],
             size=CAP, color=GREY, gap=0)
    notes(s, ["148 intraoperative cases, public, acquired November–December 2023; truth from each patient's cone-beam CT, read by two automatic labellers; 814 of 910 vertebrae agreed and kept.",
              "Three readings of the same frames: never trained on this C-arm; fine-tuned by case-grouped folds; fine-tuned by acquisition-day folds.",
              "Scored per detected body as exact level; intervals clustered by case; paired differences with exact sign tests, Holm-adjusted over the comparisons named before scoring. Every number in the paper is read by the build from a result file; a patient-keyed gate swept 563 quoted numbers against checkpoint lineages.",
              "Retrospective study of public collections, analysed April–September 2026."])

    # ---- 12 Result 1: naming without counting or registration, against the published methods
    s = content_slide(prs, "Result 1: it names the level without counting or registration")
    img = FIGS2 / "table_result1.png"
    w, h = fit(img, R - L, BOTTOM - TOP - 380000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    add_text(s, L, TOP + h + 60000, R - L, 360000,
             ["SchwingNet on 148 real intraoperative cases of a C-arm it never saw, lateral view, scored against cone-beam CT; the published methods on their own test sets. Parity with the overlay is suggested, not proven: the paired comparison is a separate study."],
             size=CAP, color=GREY, gap=0)
    notes(s, ["Zero-shot lateral: 595 of 617 detected bodies exact (96.4 %; 95 % CI 92.3, 98.4). Anteroposterior zero-shot 43.7 %; fine-tuned on other cases of the same C-arm 96.4 %. With three bodies in view 93.1 %; with one body 74.8 %: a name where there is nothing to count.",
              "The published accuracies are scored against different truths: LevelCheck against the labels it imported from the planning CT; the surgeon reading with the overlay against the same; the registration-free methods against their own test sets. No study is on a transitional spine."])

    # ---- 13 Result 2: the stop, on the six-lumbar case
    fig_left(prs, "Result 2: when shape and count disagree, it stops", FIGS2 / "render_case42_L6.png", [
        "A patient one CT labeller reads six-lumbar, the other five. Shape names bodies 5 to 2 as L2–L5 (0.89–1.00); the count says L1–L4. Body 1: shape none (0.02), count L5",
        "The call is L6 for the column; body 1 is left unnamed and the read stops",
        "Over all anchored frames: count 97.0 %, shape 97.7 %, together 98.2 % (1,009 bodies). Stopped on 23 of 233 frames, holding five of the six errors and all four L6 calls",
        "A disagreement is reported, not hidden"],
        img_w=5600000, size=15,
        caption="C-ArmLSpine case 42, public; manuscript Figure 4d with the probabilities the system printed on each box; cross-validation fold.",
        refs_text="How the two readings are combined and when the read stops are withheld pending the invention review. No accuracy on this slide is a wrong-level surgery rate.")

    # ---- 14 frames and angles
    fig_left(prs, "Where the frames sat mattered more than how many", FIGS2 / "big_fig5_cd.png", [
        "Unseen device: 80.5 % of bodies found; 93.9 % on truth boxes inside the field",
        "Its own frames: a plateau from 24 (c). One view buys that view only",
        "Renders at two poses find 53 % between them; the same count spread over the arc, 77 % (d)"],
        img_w=7400000, size=15,
        caption="SchwingNet manuscript, Figure 5c–d; render sweep on 40 unseen subjects.")

    # ---- 15 persons and views
    legend = [[("●  NHANES II", C_BLUE)], [("●  BUU-LSPINE", C_ORANGE)], [("▲  CSXA", C_TEAL)],
              [("●  C-arm, lateral", C_BLACK)], [("■  C-arm, anteroposterior", C_MID)],
              [("○  lateral-trained, read on anteroposterior", C_BLACK)], [("✕  both views, all persons", C_BLACK)]]
    fig_left(prs, "How many people it takes, and which view they were shot in", FIGS2 / "big_fig5_b.png", [
        "Film naming rose with training persons: NHANES II 78 → 93 %, BUU-LSPINE 65 → 97 %, CSXA 94 → 99.8 %",
        "C-arm lateral: 93.7 % with no C-arm person. Anteroposterior: 33.8 % with none, 90.8 % with five",
        "Training both views cost neither (98.1 and 97.0 %)"],
        img_w=4700000, legend=legend,
        caption="Exact level against training persons; SchwingNet manuscript, Figure 5b.")

    # ---- 16 Result 3: transitional naming is not yet tested; what the census would let the talk claim
    cl = json.load(open(FIGS2 / "claims.json"))
    r_l6 = next(r for r in cl["rows"] if r["label"].startswith("sixth"))
    r_all = next(r for r in cl["rows"] if r["label"].startswith("all three"))
    s = content_slide(prs, "Result 3: transitional naming is not yet tested; what the census supplies")
    img = FIGS2 / "table_claims.png"
    w, h = fit(img, R - L, 2750000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    y = TOP + h + 120000
    add_text(s, L, y, R - L, BOTTOM - y, [
        f"Scored so far: three L6 patients, in cross-validation only; a description, not a test. Today there are {cl['today']['n']} candidates on real exposures, none verified.",
        f"n: the transitional persons a screen of every collection in the census should find, from published prevalence; a case counts only where a film exists. Each cell: the lowest accuracy the data would still support at 95 % confidence at that share of errors (Wilson bound).",
        f"{cl['levelcheck_pct']} % is what surgeons scored with the LevelCheck overlay (Manbachi 2018). With {r_l6['n']} L6 persons the network may miss {r_l6['errors_allowed_levelcheck']} and still sit above it; with all {r_all['n']:,} transitional persons, {r_all['errors_allowed_levelcheck']}; the {cl['screened_now_L6']['n']} L6 of the screen running now allow {cl['screened_now_L6']['errors_allowed_levelcheck']}.",
        "Beating it outright needs the paired comparison on the same persons, a separate study."],
        size=13, gap=5)

    # ---- 17 limitations
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
    notes(s, ["Limitations. One intraoperative device; its truth is two automatic labellers agreeing, which removes the thoracolumbar junction and cannot settle a transitional count. Whether 148 cases are 148 people cannot be established; every intraoperative interval is too narrow if they are not. Real frames sit at two poses; one patient's rotational acquisition is the only real arc, and on it the held-out detector found about half the bodies. The posterior is uncalibrated; the embedding is of the selection split. Retrospective, public data; nothing prospective; not a cleared device.",
              "Next steps. Verify the transitional candidates by two human readers and run the pre-stated test: 35 persons, zero errors. A second C-arm, with obliques, added to the corpus and held out; the paired comparison with registration on verified at-risk persons. Phantom, cadaver, then human series, in that order, before any operating-room use."])

    # ---- 18 conclusions, against the three goals
    s = content_slide(prs, "Conclusions: three goals, where each stands")
    img = FIGS2 / "chart_headline.png"
    w, h = fit(img, 4000000, 3300000)
    picture(s, img, R - w, TOP, w, h)
    add_text(s, R - w, TOP + h + 40000, w, 300000, ["Exact level on the unseen C-arm."], size=CAP, color=GREY, gap=0)
    add_text(s, L, TOP, R - w - GAP - L, 3400000, [
        [("Name the level from one exposure, no count, no registration: ", NAVY), ("met on ordinary anatomy", C_TEAL), (" — 96.4 % zero-shot, 98.2 % coupled, beside 97.6 % for surgeons with the overlay (different test sets)", NAVY)],
        [("Name it on a transitional spine: ", NAVY), ("not yet shown", RGBColor(0xEF, 0x46, 0x27)), (" — three cross-validation patients; 35 error-free persons needed; the census should supply about 870 L6", NAVY)],
        [("Outperform surgeons using registration: ", NAVY), ("needs the paired study", RGBColor(0xEF, 0x46, 0x27)), (" — the census makes the size of that claim possible", NAVY)]],
        size=17, gap=12)
    navy_bar(s, L, TOP + 3550000, R - L, 850000,
             "A name from shape, checked against the count, with a stop where they disagree", size=20)
    add_text(s, L, TOP + 4500000, R - L, 400000, [
        "Evidence status: investigational; retrospective, public de-identified data; no prospective evaluation; not a cleared device."],
        size=13, color=BLUE, gap=0)

    # ---- 19 acknowledgments and data availability
    s = content_slide(prs, "Acknowledgments and data availability")
    add_text(s, L, TOP, 6300000, BOTTOM - TOP, [
        "With thanks to Patrick Schwing (LSU Health Sciences Center New Orleans); Miraziz Ismoilov and Nizar Alnabahneh (Radiology) and Loren Schwiebert (Computer Science), Wayne State University; and the annotators Ashley Schehr, [student A], [student B], [student C], [student D], [student E], [student F], [student G], [student H], [student I] and [student J]",
        "Data: CTSpinoPelvic1K (doi.org/10.5281/zenodo.22139642) and the public C-arm, radiograph and CT collections under their own licences; all de-identified",
        "Code and weights: github.com/OpenSpineConsortium",
        "Funding: NIH NIGMS F30GM147909. No commercial support."], size=15, gap=8)
    img = FIGS2 / "fig_anchors.png"
    w, h = fit(img, 3500000, 1300000)
    picture(s, img, R - w, TOP, w, h)
    navy_bar(s, R - 3500000, TOP + h + 300000, 3500000, 1300000,
             ["Questions", "gregory.schwing@med.wayne.edu", "openspineconsortium.com"], size=18)

    prs.save(str(out))
    print("wrote", out, "slides:", len(prs.slides))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default="[session and date pending]")
    ap.add_argument("--out", default=str(Path.home() / "OneDrive/Desktop/CNS2026_Schwing_SchwingNet_CNStemplate.pptx"))
    a = ap.parse_args()
    build(a.session, Path(a.out))
