# source-of-copy: CTSpinoPelvic1K repository working tree (public, master; head 7ddfe38 on 2026-10-08), path paper/cns2026/make_cns_deck_v5.py; kept out of every commit by .git/info/exclude (45df97d stopped tracking the folder); copied 2026-10-08. Project folder 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
# laptop path on line 353: the --out default; pass --out before running (MANIFEST_LOCAL.md section 3.6)
"""paper/cns2026/make_cns_deck_v5.py — the SchwingNet talk on the official 2026 CNS Annual Meeting speaker template,
version 5 (Greg 2026-09-25 night, after v4):

  * "Where this is going" rewritten in plain words;
  * the cost slide shows the Bettis figure alone, tall;
  * hypothesis slide: bigger figure, two lines;
  * materials slide: the supplement's corpus manifold with every source labelled (Figure S1a), not pie charts;
  * inputs-and-outputs slide: bigger figure, smaller text;
  * test slide: three real intraoperative frames scored against cone-beam CT (from the C-ArmLSpine gallery);
  * two-readings slide: Figure 4c-d (count from the sacrum; six lumbar, both must agree);
  * frames-and-angles slide: Figure 5c-d larger;
  * transitional slide: the real frame of the six-lumbar patient with the shape reading and its probability, the
    count and the call printed on every box (render_case42.py);
  * two new slides: the power calculation (Figure 5a, Wilson bound) and the CT census (cumulative expected
    transitional persons against CTs screened, with the power targets) as the way the missing persons will be found;
  * limitations slide: the supplement's rotational-acquisition plot (Figure S5) instead of a chart of mine.

ACCME items as v4 (no disclosure slide, citations with design and dates, generic names, no logos, HIPAA and
evidence-status lines). Type: titles 30 pt, body 16-20 pt, captions 12 pt, references 10 pt.

    python paper/cns2026/make_v3_charts.py && python paper/cns2026/prep_cited_figs.py && python paper/cns2026/prep_big_panels.py
    python paper/cns2026/prep_v5_figs.py && python paper/cns2026/render_case42.py
    python paper/cns2026/make_cns_deck_v5.py --session "..." --out CNS2026_Schwing_SchwingNet_CNStemplate.pptx
"""
from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt

from make_cns_deck_v2 import FIGS2, fit
from make_cns_deck_v4 import (BLUE, BODY, BOTTOM, CAP, GAP, GREY, L, NAVY, R, REFS_TOP, TEMPLATE, TOP, WHITE, add_text, arrow,
                              content_slide, fig_left, fig_top, flow_box, navy_bar, picture, refs)

C_BLUE = RGBColor(0x1F, 0x77, 0xB4)
C_ORANGE = RGBColor(0xE8, 0x71, 0x0A)
C_GREEN = RGBColor(0x2C, 0xA0, 0x89)
C_PURPLE = RGBColor(0x4B, 0x2C, 0x92)
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
            r.font.size = Pt(28)
            r.font.bold = True
            r.font.color.rgb = WHITE
    sub = ph[1]
    sub.left, sub.top, sub.width, sub.height = Emu(5185558), Emu(3250000), Emu(6500000), Emu(1200000)
    sub.text_frame.word_wrap = True
    sub.text_frame.text = "Gregory J. Schwing, MD, PhD"
    for p in sub.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(20)
            r.font.color.rgb = WHITE
    body = ph[10]
    body.left, body.top, body.width, body.height = Emu(5185558), Emu(4550000), Emu(6500000), Emu(1600000)
    body.text_frame.word_wrap = True
    body.text_frame.text = "Department of General Surgery, Detroit Medical Center and Wayne State University, Detroit, MI"
    for line in ("CNS 2026 Annual Meeting  ·  Washington, DC  ·  " + session,):
        p = body.text_frame.add_paragraph()
        p.text = line
    for p in body.text_frame.paragraphs:
        p.space_after = Pt(4)
        for r in p.runs:
            r.font.size = Pt(13)
            r.font.color.rgb = WHITE

    # ---- 2 where this is going (plain words)
    s = content_slide(prs, "Where this is going")
    img = FIGS2 / "sn_fig4_b_img.png"
    w, h = fit(img, 3900000, BOTTOM - TOP - 500000)
    picture(s, img, R - w, TOP, w, h)
    add_text(s, R - w, TOP + h + 60000, w, 450000, ["A real lateral C-arm exposure; each body named from its shape, with its probability."], size=CAP, color=GREY, gap=0)
    items = [
        "Surgeons count vertebrae on the C-arm. On a transitional spine the count is wrong",
        "Today's tools copy a planning label onto the film. The planning read is wrong on the same spines",
        "SchwingNet reads the level from the shape of the bones in one exposure",
        "Tested on a C-arm it never saw: how often it is right, and when it stops",
        "What is missing: enough transitional patients to prove it, and the CT census that will find them",
    ]
    y = TOP
    tw = R - w - GAP - (L + 600000)
    for i, txt in enumerate(items, 1):
        box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(L), Emu(y), Emu(460000), Emu(460000))
        box.fill.solid()
        box.fill.fore_color.rgb = NAVY
        box.line.color.rgb = NAVY
        box.shadow.inherit = False
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = str(i)
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = WHITE
        add_text(s, L + 600000, y - 20000, tw, 900000, [txt], size=19, gap=0)
        y += 940000

    # ---- 3 the count is wrong often
    fig_left(prs, "A level is counted, not marked, and the count is wrong often", FIGS2 / "cited_strong2022_fig3.png", [
        "Half of spine surgeons report a wrong-level operation in their career (Mody 2008; Groff 2013)",
        "Registry of 34,544 operations: 0.12 %, thoracic 0.42 % (Furuya 2026)",
        "The first exposed level is wrong in 4–15 % before the check film (Ammerman 2006; Dablouk 2019)",
        "No neurophysiological check between T1 and L2; verification protocols miss a third (Longo 2012)"],
        img_w=4600000, max_h=3300000,
        caption="Strong et al. 2022, Figure 3: intraoperative fluoroscopy, needle at the T10 pedicle, counted from the sacrum. J Neurosurg Spine 36:792 (PMC10193475); permission pending.",
        note="The remedy on offer is another count.",
        refs_text="1. Mody MG, et al. Spine 2008;33:194.   2. Groff MW, et al. World Neurosurg 2013;79:585.   3. Furuya M, et al. Bone Joint J 2026;108-B:673.   4. Dablouk MO, et al. Br J Neurosurg 2019.   5. Ammerman JM, et al. Surg Neurol 2006.   6. Kirshblum SC, et al. J Spinal Cord Med 2011.   7. Longo UG, et al. J Bone Joint Surg Br 2012;94-B:1546.")

    # ---- 4 transitional anatomy changes the count
    fig_top(prs, "Transitional anatomy changes the count", FIGS2 / "big_fig1_ct_row.png", [
        "8.8 % of 3,147 full-length radiographs lack 24 presacral segments (Sabri 2025)",
        "The count was wrong in 38 of 71 patients with a transitional vertebra (Nakagawa 2017)",
        "The truth is on CT. No public radiograph or C-arm frame carries a human-read T13 or Castellvi grade"],
        max_h=2900000, size=20,
        caption="Labelled CT, public de-identified records (CTSpinoPelvic1K). Bar, 20 mm.",
        refs_text="8. Sabri SA, et al. Neurosurg Focus 2025;58(6):E13.   9. Nakagawa T, et al. 2017.   10. Castellvi AE, et al. Spine 1984;9:493.   Figure: SchwingNet manuscript (in preparation), Figure 1.")

    # ---- 5 what a wrong level costs (Bettis alone, tall)
    fig_left(prs, "What a wrong level costs, and what avoiding it costs", FIGS2 / "cited_bettis_fig1.png", [
        "17 % of events lead to legal action; one in five Spine Section surgeons has been sued (Mody 2008; Groff 2013)",
        "81 % of litigated cases paid; median never-event payment $75,220 (Goodkin 2004; Bettis 2026)",
        "Avoiding it: a gold fiducial placed the day before, 52 min and 183 mGy per patient, 179 patients at one centre (AJNR 2023)"],
        img_w=6100000, size=17,
        caption="Bettis et al. 2026, Figure 1: National Practitioner Data Bank malpractice payment reports for surgical never events, 1991–2025 (Patient Saf Surg, open access; permission pending).",
        note="Derived, unpublished: roughly 420–1,900 US wrong-level operations a year; indemnity alone about $8–37 million.",
        refs_text="11. Goodkin R, Laska LL. Surg Neurol 2004;61:323.   12. Bettis T, et al. Patient Saf Surg 2026.   13. Machin JT, et al. Eur Spine J 2018;27:2693.   14. AJNR Am J Neuroradiol 2023;44:618.   15. Childers CP, Maggard-Gibbons M. JAMA Surg 2018;153:e176233.")

    # ---- 6 the label on the film
    fig_left(prs, "The label on the film is only as right as the planning read", FIGS2 / "cited_levelcheck_composite.png", [
        "LevelCheck registers preoperative CT labels onto the film: 100 % placement, 97.6 % surgeon reads (De Silva 2016; Manbachi 2018)",
        "Scored against the imported labels. On a transitional spine the label is only as right as the planning read",
        "Registration-free naming on real C-arm images: 73 % (Zhang 2023); cadaver long-length images 88 % (Huang 2022)"],
        img_w=4800000, max_h=3300000,
        caption="Top: De Silva et al. 2016, Figure 1 (Spine; PMC5045321). Bottom: Manbachi et al. 2018, Figure 6, labels on a 13th rib and a lumbarised S1 (Ann Biomed Eng; PMC9107073). Permission pending.",
        note="Nothing published names a level from one exposure alone, and nothing is tested on a transitional spine.",
        refs_text="16. Otake Y, et al. Phys Med Biol 2012;57:5485.   17. Lo SFL, et al. Spine 2015.   18. De Silva T, et al. Spine 2016.   19. Manbachi A, et al. Ann Biomed Eng 2018;46:1548.   20. Peh WCG, et al. 1999.   21. Zhang R, et al. J Xray Sci Technol 2023.   22. Huang Y, et al. Comput Methods Programs Biomed 2022.")

    # ---- 7 the planning read fails where the count fails
    fig_left(prs, "The planning read fails where the count fails", FIGS2 / "nas_gt_vs_ts.png", [
        "An open-source whole-body segmenter, unmodified, on 1,152 public CTs (Wasserthal 2023)",
        "Normal anatomy: L5 Dice 0.94. Lumbarization: every label slides one level, L5 Dice 0.29",
        "L6 emitted: 0 of 1,152. Confident, well formed, one level off, no error signal",
        "Not All Spines Are Created Equal, NeurIPS 2026"],
        img_w=5600000,
        caption="A lumbarization case with a true L6. Left, ground truth; right, the segmenter's output.",
        refs_text="23. Wasserthal J, et al. Radiol Artif Intell 2023;5:e230024.   24. Schwing GJ, et al. Not All Spines Are Created Equal. NeurIPS 2026 Datasets and Benchmarks (accepted; retrospective).   25. CTSpinoPelvic1K, doi.org/10.5281/zenodo.22139642.")

    # ---- 8 hypothesis and purpose (bigger figure, two lines)
    fig_top(prs, "Hypothesis and purpose", FIGS2 / "fig_phenotypes.png", [
        "Hypothesis: each transitional vertebra has a local shape a network reading a few bodies can learn",
        "Purpose: build it, test it on an unseen C-arm, and count the transitional persons a test needs. Targets set before scoring: 90 % naming, 85 % variant sensitivity, 97 % detection"],
        max_h=3050000, size=18,
        caption="Four phenotypes at the lumbar borders, aligned on the sacrum (CTSpinoPelvic1K, public, de-identified).",
        note="Investigational. Decision support beside the surgeon's count, never a replacement for the check film.")

    # ---- 9 materials: the corpus manifold
    fig_left(prs, "What exists to learn from: every source, one map", FIGS2 / "big_figS1_a.png", [
        "11,638 images from 18 public sources, embedded by a general image network and laid out in two dimensions",
        [("Films", C_BLUE), ("  ·  ", GREY), ("C-arm fluoroscopy", C_ORANGE), ("  ·  ", GREY), ("kV imagers", C_GREEN), ("  ·  ", GREY),
         ("CT renders, plain", C_MID), ("  ·  ", GREY), ("CT renders styled to a device", C_BLACK)],
        "4,093 CT renders, 9,108 films with levels, 4,276 real exposures; 194 transitional persons",
        "The intraoperative C-arm set (148 cases, cone-beam CT truth, 2023) is in no training set"],
        img_w=6300000, size=16,
        caption="Supplement Figure S1a: t-SNE of ImageNet features; renders sit apart from every real source. Two kV-imager sources relabelled generically.",
        refs_text="Retrospective study of public collections, analysed April–September 2026; sources, licences and download locations per release in the manuscript. VinDr-SpineXR under a PhysioNet data use agreement.")

    # ---- 10 what SchwingNet does (bigger figure, smaller text)
    s = content_slide(prs, "What SchwingNet does: inputs and outputs")
    bw = 2900000
    bx = [L, L + bw + 600000, L + 2 * (bw + 600000)]
    for x, head, sub in zip(bx, ("1 · Find", "2 · Name", "3 · Check"),
                            (["bodies and sacrum boxed;", "no level name"],
                             ["each body named from its shape,", "probability beside it"],
                             ["against the count from the sacrum:", "agree, a name; disagree, a stop"])):
        flow_box(s, x, TOP, bw, 700000, head, sub)
    for x in bx[:2]:
        arrow(s, x + bw + 140000, TOP + 190000)
    img = FIGS2 / "big_fig4_ab.png"
    w, h = fit(img, 6300000, 2950000)
    picture(s, img, L, TOP + 1600000, w, h)
    add_text(s, L + w + GAP, TOP + 1600000, R - (L + w + GAP), 3000000, [
        "In: one exposure. Out: a name with its probability for every body, the count from the sacrum, a flag when they disagree",
        "No end of the spine needed; no label imported from another study",
        "Method withheld pending university invention review; weights and code with the paper"], size=14, gap=8)

    # ---- 11 how it was tested: three real frames scored against cone-beam CT
    fig_left(prs, "How it was tested", FIGS2 / "big_gallery_trio.png", [
        "148 intraoperative cases, public, acquired November–December 2023; truth from each patient's cone-beam CT",
        "Three readings: never trained on this C-arm; fine-tuned by case-grouped folds; by acquisition-day folds",
        "Exact level per detected body; intervals clustered by case; every number read from a result file by the build"],
        img_w=7100000, size=15,
        caption="Real lateral frames, calls by the cross-validated model; green right, red wrong, orange unscored (labellers disagree on the body). Needle tip on the named L4.")

    # ---- 12 embedding
    fig_left(prs, "A sixth lumbar vertebra has a shape of its own", FIGS2 / "big_fig2_b.png", [
        "13,009 validation crops, 1,612 people: the nearest crop of another person is the same level in 74.9 %",
        "L6 separates from L5 (silhouette 0.35) as far as L1 from T12 (0.32)",
        "75 of 98 L6 crops named L6",
        "Preliminary: ten L6 persons, on the split that chose the checkpoint"],
        img_w=4700000,
        caption="The lumbosacral window of the embedding; SchwingNet manuscript, Figure 2b.")

    # ---- 13 unseen C-arm
    fig_left(prs, "One lateral exposure of a C-arm the network never saw", FIGS2 / "big_fig4_ab.png", [
        "Zero-shot, lateral: 595 of 617 bodies exact (96.4 %; 92.3, 98.4)",
        "Anteroposterior zero-shot 43.7 %; fine-tuned on other cases 96.4 %",
        "Three bodies in view 93.1 %; one body 74.8 %: a name where there is nothing to count"],
        img_w=6400000,
        caption="C-ArmLSpine, public intraoperative exposures, 2023; SchwingNet manuscript, Figure 4a–b.")

    # ---- 14 two readings: Figure 4c-d
    fig_left(prs, "Two readings of one frame, and a stop where they disagree", FIGS2 / "big_fig4_cd.png", [
        "Count from the sacrum 97.0 %, shape alone 97.7 %, together 98.2 % (1,009 bodies)",
        "Stopped on 23 of 233 frames: five of the six errors and all four L6 calls",
        "A disagreement is reported, not hidden"],
        img_w=7000000, size=17,
        caption="Same frame. (c) Ordinals from the detected sacrum, named in the ordinary five-lumbar alphabet. (d) A frame one CT labeller reads six-lumbar: shape and count disagree on body 1; the read stops.",
        note="How the readings are combined and when the read stops are withheld pending the invention review.")

    # ---- 15 frames and angles (larger figure)
    fig_left(prs, "Where the frames sat mattered more than how many", FIGS2 / "big_fig5_cd.png", [
        "Unseen device: 80.5 % of bodies found; 93.9 % on truth boxes inside the field",
        "Its own frames: a plateau from 24 (c). One view buys that view only",
        "Renders at two poses find 53 % between them; the same count spread over the arc, 77 % (d)"],
        img_w=7400000, size=15,
        caption="SchwingNet manuscript, Figure 5c–d; render sweep on 40 unseen subjects.")

    # ---- 16 persons and views
    legend = [[("●  NHANES II", C_BLUE)], [("●  BUU-LSPINE", C_ORANGE)], [("▲  CSXA", C_TEAL)],
              [("●  C-arm, lateral", C_BLACK)], [("■  C-arm, anteroposterior", C_MID)],
              [("○  lateral-trained, read on anteroposterior", C_BLACK)], [("✕  both views, all persons", C_BLACK)]]
    fig_left(prs, "How many people it takes, and which view they were shot in", FIGS2 / "big_fig5_b.png", [
        "Film naming rose with training persons: NHANES II 78 → 93 %, BUU-LSPINE 65 → 97 %, CSXA 94 → 99.8 %",
        "C-arm lateral: 93.7 % with no C-arm person. Anteroposterior: 33.8 % with none, 90.8 % with five",
        "Training both views cost neither (98.1 and 97.0 %)"],
        img_w=4700000, legend=legend,
        caption="Exact level against training persons; SchwingNet manuscript, Figure 5b.")

    # ---- 17 transitional naming on a real exposure: the case itself
    fig_left(prs, "Transitional naming on a real exposure: the one case", FIGS2 / "render_case42_L6.png", [
        "A patient one CT labeller reads six-lumbar, the other five. Lateral frame, cross-validation fold",
        "Shape names bodies 5 to 2 as L2–L5 (0.89–1.00); the count says L1–L4. Body 1: shape none (0.02), count L5",
        "The call is L6 for the column; body 1 is left unnamed and the read stops",
        "Three such patients exist, six frames; scored in cross-validation only. A description, not a test"],
        img_w=5700000, size=15,
        caption="C-ArmLSpine case 42, public; SchwingNet manuscript, Figure 4d, with the probabilities the system printed on each box.",
        refs_text="No accuracy on this slide is a wrong-level surgery rate. Evidence base absent: transitional naming on real exposures is unverified.")

    # ---- 18 what the whole census would let the talk claim, explained
    import json as _json
    cl = _json.load(open(FIGS2 / "claims.json"))
    r_l6 = next(r for r in cl["rows"] if r["label"].startswith("sixth"))
    r_all = next(r for r in cl["rows"] if r["label"].startswith("all three"))
    s = content_slide(prs, "What the census would let me claim")
    img = FIGS2 / "table_claims.png"
    w, h = fit(img, R - L, 2750000)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    y = TOP + h + 120000
    add_text(s, L, y, R - L, BOTTOM - y, [
        f"n: the transitional persons a screen of every collection in the census should find, from published prevalence; a case counts only where a film exists. Today there are {cl['today']['n']} candidates on real exposures, none verified.",
        f"Each cell: the lowest accuracy the data would still support at 95 % confidence if the network named those n persons with that share of errors (Wilson bound). {cl['n_zero_error_for_levelcheck']} error-free persons are the fewest that clear {cl['levelcheck_pct']} %.",
        f"{cl['levelcheck_pct']} % is what surgeons scored reading 62 difficult films with the LevelCheck overlay (Manbachi 2018). With {r_l6['n']} L6 persons the network may miss {r_l6['errors_allowed_levelcheck']} and still sit above it; with all {r_all['n']:,} transitional persons, {r_all['errors_allowed_levelcheck']}. The {cl['screened_now_L6']['n']} L6 of the screen running now allow {cl['screened_now_L6']['errors_allowed_levelcheck']}.",
        "Beating it outright needs the paired comparison on the same persons, a separate study; this slide is the size of the claim the census makes possible."],
        size=13, gap=5)

    # ---- 20 limitations and next steps, with the rotational acquisition
    s = content_slide(prs, "Limitations and next steps")
    colw = 4900000
    add_text(s, L, TOP, colw, BOTTOM - TOP, [
        "Limitations",
        "One device; its truth is two automatic labellers agreeing",
        "148 cases may not be 148 people; intervals may be too narrow",
        "Real frames sit at two poses; one patient's rotational acquisition is the only real arc",
        "Retrospective, public data; nothing prospective; not a cleared device",
        "Next steps",
        "Verify the transitional candidates; run the 35-person, zero-error test",
        "A second C-arm, with obliques, held out; phantom, cadaver, then human series"], size=15, gap=7)
    x2 = L + colw + GAP
    wa, ha = fit(FIGS2 / "big_figS5_a.png", R - x2, 1350000)
    picture(s, FIGS2 / "big_figS5_a.png", x2, TOP, wa, ha)
    wb, hb = fit(FIGS2 / "big_figS5_b.png", 2900000, 2500000)
    picture(s, FIGS2 / "big_figS5_b.png", x2, TOP + ha + 120000, wb, hb)
    add_text(s, x2 + wb + 150000, TOP + ha + 200000, R - (x2 + wb + 150000), 2400000, [
        "Bodies found on one patient's real rotational acquisition, 301 frames:",
        [("●  detector that also saw this device's spot frames", C_BLUE)],
        [("■ ▲  other devices' renders and frames, this one held out", C_PURPLE)],
        [("◆  the reported detector, this one held out", C_GREEN)]], size=12, gap=4)
    add_text(s, x2, TOP + ha + hb + 160000, R - x2, 400000, ["Supplement Figure S5: frames at four angles (bar, 50 mm) and detection against view angle at confidence 0.25."], size=CAP, color=GREY, gap=0)

    # ---- 21 conclusions
    s = content_slide(prs, "Conclusions")
    img = FIGS2 / "chart_headline.png"
    w, h = fit(img, 4200000, 3300000)
    picture(s, img, R - w, TOP, w, h)
    add_text(s, R - w, TOP + h + 40000, w, 300000, ["Exact level on the unseen C-arm."], size=CAP, color=GREY, gap=0)
    add_text(s, L, TOP, R - w - GAP - L, 3400000, [
        "The count fails on transitional anatomy; registered labels and CT segmenters inherit the miscount",
        "SchwingNet: 96.4 % zero-shot on the lateral view, 98.2 % coupled, and a stop on 23 of 233 frames holding five of six errors",
        "Transitional naming on real exposures: unverified. 35 persons needed; the census is under way"], size=20, gap=12)
    navy_bar(s, L, TOP + 3550000, R - L, 850000,
             "A name from shape, checked against the count, with a stop where they disagree", size=20)
    add_text(s, L, TOP + 4500000, R - L, 400000, [
        "Evidence status: investigational; retrospective, public de-identified data; no prospective evaluation; not a cleared device."],
        size=13, color=BLUE, gap=0)

    # ---- 22 acknowledgments and data availability
    s = content_slide(prs, "Acknowledgments and data availability")
    add_text(s, L, TOP, 6300000, BOTTOM - TOP, [
        "With thanks to Patrick Schwing (LSU Health Sciences Center New Orleans); Miraziz Ismoilov and Nizar Alnabahneh (Radiology) and Loren Schwiebert (Computer Science), Wayne State University; and the annotators Ashley Schehr, [ten student annotator names withheld]",
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
    ap.add_argument("--out", default=str(Path.home() / "<laptop:Desktop>/CNS2026_Schwing_SchwingNet_CNStemplate.pptx"))
    a = ap.parse_args()
    build(a.session, Path(a.out))
