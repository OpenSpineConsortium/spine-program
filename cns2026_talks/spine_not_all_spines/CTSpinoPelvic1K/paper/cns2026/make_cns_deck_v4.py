"""paper/cns2026/make_cns_deck_v4.py — the SchwingNet talk on the official 2026 CNS Annual Meeting speaker template,
built to the ACCME accreditation guidelines CNS circulated (Greg 2026-09-25: "follow these instructions ... and use
this template"), then cut to a few large lines per slide with figure lettering readable from the room (Greg: "way
too much text and what text there is is too small, even the figure legends and axis titles").

Guideline items applied (against version 3, make_cns_deck_v3.py):
  * no disclosure slide (CNS provides the official list; the invention-review notice is one line on the
    inputs-and-outputs slide);
  * a citation with study design and dates on every data slide (reference line at the foot);
  * generic names, no trade names or (TM)/(R) marks; open-source tools named with their citations; no device
    manufacturer named anywhere, including figure captions;
  * no ineligible-company logo (the CNS template's own marks only; the old lab template's university shield is gone);
  * preliminary evidence flagged: the derived cost figure, the unverified transitional naming, and an
    evidence-status line on the conclusions slide;
  * all images public and de-identified (HIPAA), stated on the materials slide.

Type: titles 30 pt, body 18-20 pt, captions 12 pt, references 10 pt. Charts (make_v3_charts.py) are drawn at 17-30 pt.
Manuscript figures are shown one panel at a time (prep_big_panels.py) so their lettering scales about 2x.

Template geometry (16:9): layout 0 "Title Slide"; layout 2 "1_Title and Content Vertical" (navy band 0..1.52M EMU at
the left, white content area) for every content slide. Theme font New Hero inherited; palette navy 191D63 /
blue 4C70B7 / red EF4627 / gold FFC42F. A text box with zero or negative extent makes PowerPoint refuse the whole
file, so add_text clamps extents.

    python paper/cns2026/make_v3_charts.py && python paper/cns2026/prep_cited_figs.py && python paper/cns2026/prep_big_panels.py
    python paper/cns2026/make_cns_deck_v4.py --session "..." --out CNS2026_Schwing_SchwingNet_CNStemplate.pptx
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TEMPLATE = ROOT / "2026 CNS AM Speaker Powerpoint Template.pptx"

NAVY = RGBColor(0x19, 0x1D, 0x63)
BLUE = RGBColor(0x4C, 0x70, 0xB7)
GOLD = RGBColor(0xFF, 0xC4, 0x2F)
RED = RGBColor(0xEF, 0x46, 0x27)
GREY = RGBColor(0x7A, 0x7A, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

L = 1750000
R = 11900000
TOP = 1420000
BOTTOM = 6250000
REFS_TOP = 6380000
GAP = 300000
BODY = 18
CAP = 12
REF = 10


# ---------------------------------------------------------------- plumbing
def add_text(slide, left, top, width, height, lines, size=BODY, color=NAVY, bold=False, gap=8, align=None, anchor=None):
    height = max(int(height), 250000)
    width = max(int(width), 250000)
    tb = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    if anchor:
        tf.vertical_anchor = anchor
    if isinstance(lines, str):
        lines = [lines]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if isinstance(line, list):          # coloured runs: [(text, colour), ...]
            for text, col in line:
                r = p.add_run()
                r.text = text
                r.font.size = Pt(size)
                r.font.color.rgb = col
                r.font.bold = bold
        else:
            r = p.add_run()
            r.text = line
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
        p.space_before = Pt(0)
        p.space_after = Pt(gap)
        if align:
            p.alignment = align
    return tb


def picture(slide, path, left, top, width, height):
    return slide.shapes.add_picture(str(path), Emu(left), Emu(top), width=Emu(width), height=Emu(height))


def content_slide(prs, title, size=30):
    s = prs.slides.add_slide(prs.slide_layouts[2])
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx != 0:
            ph._element.getparent().remove(ph._element)
    t = s.shapes.title
    t.left, t.top, t.width, t.height = Emu(L), Emu(300000), Emu(R - L), Emu(1000000)
    tf = t.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.BOTTOM
    tf.text = title
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.bold = True
            r.font.color.rgb = NAVY
    return s


def refs(slide, text):
    add_text(slide, L, REFS_TOP, R - L, 420000, [text], size=REF, color=GREY, gap=0)


def fig_left(prs, title, img, lines, img_w=5900000, max_h=None, size=BODY, caption=None, note=None, refs_text=None,
             legend=None):
    """Figure at the left with its caption, a few large lines at the right, an optional blue note under them."""
    s = content_slide(prs, title)
    bottom = (REFS_TOP - 80000) if refs_text else BOTTOM
    reserve = 700000 if caption else 0
    w, h = fit(img, img_w, min(max_h or (bottom - TOP), bottom - TOP - reserve))
    picture(s, img, L, TOP, w, h)
    y = TOP + h + 80000
    if caption:
        add_text(s, L, y, w, bottom - y, [caption], size=CAP, color=GREY, gap=0)
    left = L + w + GAP
    add_text(s, left, TOP, R - left, bottom - TOP, lines, size=size, gap=12)
    if legend:
        add_text(s, left, bottom - 1750000, R - left, 1750000, legend, size=15, gap=3, anchor=MSO_ANCHOR.BOTTOM)
    if note:
        add_text(s, left, bottom - 1100000, R - left, 1100000, [note], size=size - 2, color=BLUE, gap=0, anchor=MSO_ANCHOR.BOTTOM)
    if refs_text:
        refs(s, refs_text)
    return s


def fig_top(prs, title, img, lines, max_h=2600000, size=BODY, caption=None, note=None, refs_text=None):
    s = content_slide(prs, title)
    bottom = (REFS_TOP - 80000) if refs_text else BOTTOM
    w, h = fit(img, R - L, max_h)
    picture(s, img, L + (R - L - w) // 2, TOP, w, h)
    y = TOP + h + 60000
    if caption:
        add_text(s, L, y, R - L, 300000, [caption], size=CAP, color=GREY, gap=0)
        y += 330000
    add_text(s, L, y + 60000, R - L, bottom - y - 60000, lines, size=size, gap=10)
    if note:
        add_text(s, L, bottom - 450000, R - L, 450000, [note], size=size - 2, color=BLUE, gap=0, anchor=MSO_ANCHOR.BOTTOM)
    if refs_text:
        refs(s, refs_text)
    return s


def flow_box(slide, left, top, width, height, head, sub):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(left), Emu(top), Emu(width), Emu(height))
    box.fill.solid()
    box.fill.fore_color.rgb = NAVY
    box.line.color.rgb = NAVY
    box.shadow.inherit = False
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = head
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = WHITE
    add_text(slide, left, top + height + 80000, width, 800000, sub, size=16, color=NAVY, gap=0, align=PP_ALIGN.CENTER)


def arrow(slide, left, top):
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Emu(left), Emu(top), Emu(320000), Emu(320000))
    a.fill.solid()
    a.fill.fore_color.rgb = GOLD
    a.line.color.rgb = GOLD
    a.shadow.inherit = False


def navy_bar(slide, left, top, width, height, text, size=18):
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(left), Emu(top), Emu(width), Emu(height))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.color.rgb = NAVY
    bar.shadow.inherit = False
    tf = bar.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size if i == 0 else size - 4)
        r.font.bold = i == 0
        r.font.color.rgb = WHITE
    return bar


# ---------------------------------------------------------------- content
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
    sub.text_frame.text = ("Gregory J. Schwing, MD, PhD; Patrick Schwing; Miraziz Ismoilov, MD; Nizar Alnabahneh, MD; "
                           "Loren Schwiebert, PhD; and the OpenSpineConsortium annotators")
    for p in sub.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(16)
            r.font.color.rgb = WHITE
    body = ph[10]
    body.left, body.top, body.width, body.height = Emu(5185558), Emu(4550000), Emu(6500000), Emu(1600000)
    body.text_frame.word_wrap = True
    body.text_frame.text = "Department of General Surgery, Detroit Medical Center and Wayne State University, Detroit, MI"
    for line in ("Radiology and Computer Science, Wayne State University; LSU Health Sciences Center New Orleans",
                 "CNS 2026 Annual Meeting  ·  Washington, DC  ·  " + session):
        p = body.text_frame.add_paragraph()
        p.text = line
    for p in body.text_frame.paragraphs:
        p.space_after = Pt(4)
        for r in p.runs:
            r.font.size = Pt(13)
            r.font.color.rgb = WHITE

    # ---- 2 overview
    s = content_slide(prs, "Where this is going")
    img = FIGS2 / "sn_fig4_b_img.png"
    w, h = fit(img, 3900000, BOTTOM - TOP - 500000)
    picture(s, img, R - w, TOP, w, h)
    add_text(s, R - w, TOP + h + 60000, w, 450000, ["A real lateral C-arm exposure; each body named from its shape, with its posterior."], size=CAP, color=GREY, gap=0)
    items = [
        "A level is counted, not marked, and the count fails on transitional anatomy",
        "Registered labels inherit the planning read, and the planning read fails there too",
        "Hypothesis: a transitional vertebra has a shape a network can learn",
        "SchwingNet on a C-arm it never saw: name, count, coupled call, stop",
        "What a transitional test needs, and where the persons will come from",
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
        add_text(s, L + 600000, y - 20000, tw, 900000, [txt], size=20, gap=0)
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

    # ---- 5 what a wrong level costs
    fig_left(prs, "What a wrong level costs, and what avoiding it costs", FIGS2 / "cited_cost_composite.png", [
        "17 % of events lead to legal action; one in five Spine Section surgeons has been sued (Mody 2008; Groff 2013)",
        "81 % of litigated cases paid; median never-event payment $75,220 (Goodkin 2004; Bettis 2026)",
        "Avoiding it: a gold fiducial, 52 min and 183 mGy per patient, 179 patients at one centre (AJNR 2023)"],
        img_w=5900000, max_h=2500000,
        caption="Left: Bettis et al. 2026, Figure 1, National Practitioner Data Bank never-event payments 1991–2025 (open access). Right: AJNR 2023;44:618, Figure 1, fiducial placed at T4 (PMC10171395). Permission pending.",
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

    # ---- 8 hypothesis and purpose
    fig_top(prs, "Hypothesis and purpose", FIGS2 / "fig_phenotypes.png", [
        "Hypothesis: each transitional vertebra has local morphology a network reading a few bodies can learn",
        "Purpose: build it, see what it learns, test it on an unseen C-arm, count the transitional persons a test needs",
        "Pre-stated targets: 90 % transitional naming, 85 % variant sensitivity, 97 % detection"],
        max_h=2300000, size=20,
        caption="Four phenotypes at the lumbar borders, aligned on the sacrum (CTSpinoPelvic1K, public, de-identified).",
        note="Investigational. Decision support beside the surgeon's count, never a replacement for the check film.")

    # ---- 9 materials
    fig_left(prs, "What exists to learn from", FIGS2 / "chart_corpus.png", [
        "Public and de-identified: 4,093 CT renders, 9,108 films with levels, 4,276 real exposures",
        "194 transitional persons. No released film or C-arm frame carries a human-read T13 or Castellvi grade",
        "The intraoperative C-arm set (148 cases, cone-beam CT truth, 2023) is in no training set"],
        img_w=6200000,
        caption="(a) Images by source type; (b) transitional persons by phenotype.",
        refs_text="Retrospective study of public collections, analysed April–September 2026; sources, licences and download locations per release in the manuscript. VinDr-SpineXR under a PhysioNet data use agreement.")

    # ---- 10 what SchwingNet does
    s = content_slide(prs, "What SchwingNet does: inputs and outputs")
    bw = 2900000
    bx = [L, L + bw + 600000, L + 2 * (bw + 600000)]
    for x, head, sub in zip(bx, ("1 · Find", "2 · Name", "3 · Check"),
                            (["bodies and sacrum boxed;", "no level name"],
                             ["each body named from its shape,", "posterior beside it"],
                             ["against the count from the sacrum:", "agree, a name; disagree, a stop"])):
        flow_box(s, x, TOP, bw, 760000, head, sub)
    for x in bx[:2]:
        arrow(s, x + bw + 140000, TOP + 220000)
    img = FIGS2 / "big_fig4_ab.png"
    w, h = fit(img, 5600000, 2500000)
    picture(s, img, L, TOP + 1750000, w, h)
    add_text(s, L + w + GAP, TOP + 1750000, R - (L + w + GAP), 2600000, [
        "In: one exposure. Out: a name with its posterior for every body, the count from the sacrum, a flag when they disagree",
        "No end of the spine needed; no label imported from another study",
        "Method withheld pending university invention review; weights and code with the paper"], size=17, gap=10)

    # ---- 11 how it was tested
    fig_left(prs, "How it was tested", FIGS2 / "chart_testset.png", [
        "Retrospective, public collections, analysed April–September 2026",
        "Truth: two automatic labellers agreeing on cone-beam CT, 148 cases",
        "Three readings: zero-shot; case-grouped folds; acquisition-day folds",
        "Exact level per detected body; intervals clustered by case; Holm-adjusted paired tests"],
        img_w=6400000, max_h=2700000,
        caption="C-ArmLSpine, public intraoperative exposures, acquired November–December 2023; the dark ring is what was scored.",
        note="Every number is read by the build from a result file; a patient-keyed gate swept 563 quoted numbers against checkpoint lineages.")

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

    # ---- 14 count, coupling, stop
    fig_left(prs, "Two readings of one frame, and a stop where they disagree", FIGS2 / "chart_coupling.png", [
        "Count from the sacrum 97.0 %, shape alone 97.7 %, together 98.2 % (1,009 bodies)",
        "Stopped on 23 of 233 frames: five of the six errors and all four L6 calls",
        "A disagreement is reported, not hidden"],
        img_w=5600000,
        caption="C-ArmLSpine, case-grouped folds.",
        note="How the readings are combined and when the read stops are withheld pending the invention review.")

    # ---- 15 detection: frames and angles
    fig_left(prs, "Where the frames sat mattered more than how many", FIGS2 / "big_fig5_cd.png", [
        "Unseen device: 80.5 % of bodies found; 93.9 % on truth boxes inside the field",
        "Its own frames: a plateau from 24 (c). One view buys that view only",
        "Renders at two poses find 53 % between them; the same count spread over the arc, 77 % (d)"],
        img_w=6700000,
        caption="SchwingNet manuscript, Figure 5c–d; render sweep on 40 unseen subjects.")

    # ---- 16 persons and views
    legend = [[("●  NHANES II", RGBColor(0x1F, 0x77, 0xB4))], [("●  BUU-LSPINE", RGBColor(0xE8, 0x71, 0x0A))], [("▲  CSXA", RGBColor(0x2C, 0xA0, 0x89))],
              [("●  C-arm, lateral", RGBColor(0x20, 0x20, 0x20))], [("■  C-arm, anteroposterior", RGBColor(0x7F, 0x7F, 0x7F))],
              [("○  lateral-trained, read on anteroposterior", RGBColor(0x20, 0x20, 0x20))], [("✕  both views, all persons", RGBColor(0x20, 0x20, 0x20))]]
    fig_left(prs, "How many people it takes, and which view they were shot in", FIGS2 / "big_fig5_b.png", [
        "Film naming rose with training persons: NHANES II 78 → 93 %, BUU-LSPINE 65 → 97 %, CSXA 94 → 99.8 %",
        "C-arm lateral: 93.7 % with no C-arm person. Anteroposterior: 33.8 % with none, 90.8 % with five",
        "Training both views cost neither (98.1 and 97.0 %)"],
        img_w=4700000, legend=legend,
        caption="Exact level against training persons; SchwingNet manuscript, Figure 5b.")

    # ---- 17 transitional naming on real exposures
    fig_left(prs, "Transitional naming on real exposures: shown and not shown", FIGS2 / "chart_census.png", [
        "Scored: three L6 patients, in cross-validation only. A description, not a test",
        "Needed: 35 error-free at-risk persons for 90 %. Seven candidates exist",
        "Census: 22 public CT collections, 18,873 CTs, about 320 L6 expected; 21 found so far"],
        img_w=6300000, max_h=2700000,
        caption="Expected counts from published prevalence (Sun 2025; Hanhivaara 2020; Nardo 2012).",
        note="Evidence base absent: transitional naming on real exposures is unverified.",
        refs_text="Two-labeller screening of public CT for transitional anatomy: American Association of Clinical Anatomists, June 2026.")

    # ---- 18 limitations and next steps
    s = content_slide(prs, "Limitations and next steps")
    colw = (R - L - GAP) // 2
    add_text(s, L, TOP, colw, BOTTOM - TOP, [
        "Limitations",
        "One device; its truth is two automatic labellers agreeing",
        "148 cases may not be 148 people; intervals may be too narrow",
        "Posterior uncalibrated; the embedding is of the selection split",
        "Retrospective, public data; nothing prospective; not a cleared device"], size=BODY, gap=10)
    img = FIGS2 / "chart_coverage.png"
    w, h = fit(img, colw, 2400000)
    x2 = L + colw + GAP
    picture(s, img, x2, TOP, w, h)
    add_text(s, x2, TOP + h + 200000, colw, BOTTOM - (TOP + h + 200000), [
        "Next steps",
        "Verify the transitional candidates; run the 35-person, zero-error test",
        "A second C-arm, with obliques, held out",
        "Phantom, cadaver, then human series"], size=BODY, gap=10)

    # ---- 19 conclusions
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

    # ---- 20 acknowledgments and data availability
    s = content_slide(prs, "Acknowledgments and data availability")
    add_text(s, L, TOP, 6300000, BOTTOM - TOP, [
        "Coauthors and annotators: Patrick Schwing; Miraziz Ismoilov, Nizar Alnabahneh, Loren Schwiebert; Ashley Schehr, [student A], [student B], [student C], [student D], [student E], [student F], [student G], [student H], [student I], [student J]",
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
