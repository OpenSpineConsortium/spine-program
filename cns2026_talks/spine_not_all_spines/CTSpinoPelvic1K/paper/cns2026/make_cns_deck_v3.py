"""paper/cns2026/make_cns_deck_v3.py — the CNS 2026 spine talk, version 3 (2026-09-25 evening): the SchwingNet paper
as a talk, with a figure on every slide. Greg: "essentially just do the SchwingNet paper, but you can use the
TotalSegmentator failure as a motivation along with a financial economic motivation"; then "I want a figure on
every slide".

Story: a level is counted, not marked, and the count is wrong often -> transitional anatomy changes the count ->
what a wrong level costs, and what avoiding it costs (docs/WRONG_LEVEL_COST_EVIDENCE.md, verified 2026-09-19) ->
the label on the film is imported and only as right as the planning read (LevelCheck) -> the planning read fails
where the count fails (Not All Spines: TotalSegmentator on an L6) -> hypothesis and purpose -> materials -> what
SchwingNet does (inputs and outputs only) -> how it was tested -> results (embedding; unseen C-arm; count, coupling,
stop; detection, frames and angles; persons and views) -> transitional naming on real exposures, shown and not
shown -> limitations -> conclusions.

Figures: the manuscript's Figure 1, 2a-b, 4a-b, 5a-b, 5c-d (crops in figs_v2/), the NeurIPS ground-truth versus
TotalSegmentator panel, the dataset article's phenotype and anchor renders, and charts drawn by make_v3_charts.py
from numbers already on the slides. "Show what, not how" as in v2: no architecture (Figure 3), no Figure 4c-d, no
Figure 2c-d, no decoder, coupling rule, stop rule or device model. Layout helpers and template rules are v2's.

    python paper/cns2026/make_v3_charts.py
    python paper/cns2026/make_cns_deck_v3.py --abstract "Abstract NNN" --session "..." --out CNS2026_Schwing_SchwingNet.pptx
"""
from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu

from make_cns_deck import TEAL, content_slide, picture, remove, set_text, shape, textbox
from make_cns_deck_v2 import (BOTTOM, FIGS, FIGS2, LEFT, RIGHT, TEMPLATE, TOP, fig_left, fig_top, fit, set_para)

GREY = RGBColor(0x7A, 0x7A, 0x7A)
REFS_TOP = 5989320
NOTE_BOTTOM = 5700000


def tbox(s, left, top, width, height, lines, size, color):
    tb = textbox(s, left, top, width, height, lines, size=size, color=color)
    for p in tb.text_frame.paragraphs:
        for r in p.runs:
            r.font.name = "Arial"
    return tb


def refs_line(s, text):
    tbox(s, 1325880, REFS_TOP, 10424160, 300000, [text], 9, GREY)


def chart_slide(prs, proto, section, title, img, lines, footer, note=None, refs=None, img_w=6500000, size=13, note_size=14,
                max_h=3600000, caption=None, note_under_figure=False):
    """Figure at the left, an optional grey attribution caption and a teal note under it, the text column at the right,
    an optional reference line at the foot."""
    s = content_slide(prs, proto, section, title)
    remove(s, "Picture 24", "TextBox 26", "Table 26", "TextBox 27")
    w, h = fit(img, img_w, max_h)
    picture(s, img, LEFT, TOP, width=w, height=h)
    tb = shape(s, "TextBox 25")
    left = LEFT + w + 300000
    tb.left = Emu(left)
    tb.top = Emu(TOP)
    tb.width = Emu(RIGHT - left)
    tb.height = Emu((REFS_TOP - 80000 if refs else BOTTOM) - TOP)
    set_para(tb, lines, size=size)
    top = TOP + h + 100000
    if caption and not note_under_figure:
        tbox(s, LEFT, top, w, NOTE_BOTTOM - top, [caption], 9.5, GREY)
        if note:
            # the caption takes the column under the figure; the note goes under the text column instead
            tbox(s, left, TOP + 2650000, RIGHT - left, 1300000, [note], note_size, TEAL)
    else:
        if caption:
            tbox(s, LEFT, top, w, 620000, [caption], 9.5, GREY)
            top += 660000
        if note:
            tbox(s, LEFT, top, w, NOTE_BOTTOM - top, [note], note_size, TEAL)
    if refs:
        refs_line(s, refs)
    set_text(shape(s, "TextBox 23"), footer)
    return s


def build(abstract: str, session: str, out: Path):
    prs = Presentation(str(TEMPLATE))
    T = list(prs.slides)
    footer = f"CNS 2026  ·  Washington, DC  ·  {abstract}"

    # ---- 1 title (+ the named exposure, top right)
    s = T[0]
    set_text(shape(s, "TextBox 1030"),
             "SchwingNet: Naming a Vertebral Level From One C-arm Exposure, Without Counting From C2")
    set_text(shape(s, "TextBox 1031"),
             "Gregory J. Schwing, MD, PhD¹   ·   Patrick Schwing²   ·   Miraziz Ismoilov, MD³   ·   Nizar Alnabahneh, MD³   ·   "
             "Loren Schwiebert, PhD⁴   ·   the OpenSpineConsortium annotators⁵")
    set_text(shape(s, "TextBox 1032"), [
        "¹ Department of General Surgery, Detroit Medical Center / Wayne State University, Detroit, MI   ·   "
        "² School of Medicine, LSU Health Sciences Center New Orleans",
        "³ Department of Radiology, Detroit Medical Center / Wayne State University   ·   "
        "⁴ Department of Computer Science, Wayne State University   ·   ⁵ Wayne State University School of Medicine"])
    set_text(shape(s, "TextBox 1033"), [abstract + "   ·   " + session, "CNS 2026, Washington, DC"])
    set_text(shape(s, "TextBox 1034"), footer)
    set_text(shape(s, "Text Placeholder 12"), "Detroit Medical Center / Wayne State University  ·  OpenSpineConsortium")
    w, h = fit(FIGS2 / "sn_fig4_b_img.png", 2400000, 1700000)
    picture(s, FIGS2 / "sn_fig4_b_img.png", RIGHT - w - 120000, 600000, width=w, height=h)

    # ---- 2 disclosures (+ public / withheld diagram)
    s = T[1]
    tb = shape(s, "TextBox 24")
    tb.width = Emu(6500000)
    set_para(tb, [
        "The authors have no relevant financial relationships to disclose.",
        "All imaging is public and de-identified; the Wayne State University IRB determined the work is not human-participant research (2 September 2026). Funding: NIH NIGMS F30GM147909.",
        "An invention disclosure covering the level-naming system is on file with Wayne State University. This talk shows what the system does and how it was tested; its methods are withheld until that review is complete.",
        "Nothing shown is a medical device. The C-arm results are retrospective, on public exposures, and have not been evaluated prospectively."], size=15)
    w, h = fit(FIGS2 / "diagram_disclosure.png", 4800000, 3800000)
    picture(s, FIGS2 / "diagram_disclosure.png", RIGHT - w, TOP, width=w, height=h)
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 3 overview (+ the named exposure)
    s = T[2]
    set_text(shape(s, "Title 11"), "Where this is going")
    set_text(shape(s, "TextBox 23"), footer)
    items = [
        "The problem — a vertebral level is counted, not marked; the count fails on transitional anatomy, and a wrong level is rare per operation, common per career and expensive",
        "What exists — registration imports the planning read onto the film, and the planning read itself fails on transitional anatomy (Not All Spines Are Created Equal, NeurIPS 2026)",
        "The hypothesis — each transitional vertebra carries local morphology that a network reading a few bodies can learn",
        "SchwingNet — what it did on a C-arm it never saw: naming, counting, the coupled call and the stop",
        "What it will take — the transitional persons a test needs, and where they will come from",
    ]
    for name, txt in zip(("TextBox 25", "TextBox 27", "TextBox 29", "TextBox 31", "TextBox 33"), items):
        tb = shape(s, name)
        tb.width = Emu(6350000)
        set_text(tb, txt, size=14)
    w, h = fit(FIGS2 / "sn_fig4_b_img.png", 4300000, 3900000)
    picture(s, FIGS2 / "sn_fig4_b_img.png", RIGHT - w, 1450000, width=w, height=h)

    proto_text = T[3]
    proto_flow = T[6]
    proto_fig = T[7]
    proto_concl = T[14]
    proto_limits = T[15]
    proto_thanks = T[16]

    # ---- 4 the count
    chart_slide(prs, proto_fig, "Background", "A level is counted, not marked, and the count is wrong often",
                FIGS2 / "cited_strong2022_fig3.png", [
        "Half of responding spine surgeons report a wrong-level operation in their career (Mody 2008; Groff 2013). Per operation: 1 in 3,110 by self-report; 0.12 % in a registry of 34,544 consecutive patients, thoracic 0.42 %, three times lumbar and eight times cervical (Furuya 2026). The level first exposed is wrong in 4.3–15 % of lumbar operations before a check film corrects it.",
        "Why: fluoroscopy shows three or four bodies. Surgeons count up from the sacrum or down from C2 across exposures, and disagree on the landmark: pedicle 67 %, spinous process 49 % (Mayer 2014).",
        "No neurophysiological check confirms a thoracic level: the motor examination tests no key muscle between T1 and L2, and screw stimulation cannot separate segments (Kirshblum 2011; Kulik 2013). The only study to assess site-verification protocols found they failed to prevent about a third of cases (Longo 2012)."],
                footer, note="The literature's remedy is imaging after exposure against a marked fixed structure. That is another count.",
                caption="Strong et al. 2022, Figure 3: thoracic stenosis in an 80-year-old woman; intraoperative fluoroscopy with the needle at the T10 pedicle, the level counted from the sacrum. Reproduced from J Neurosurg Spine 36:792 (PMC10193475); permission pending.",
                img_w=4300000, max_h=2550000, note_size=13,
                refs="1. Mody MG, et al. Spine 2008;33:194.   2. Groff MW, et al. World Neurosurg 2013;79:585.   3. Furuya M, et al. Bone Joint J 2026;108-B:673.   4. Dablouk MO, et al. Br J Neurosurg 2019.   5. Ammerman JM, et al. Surg Neurol 2006.   6. Mayer JE, et al. Spine J 2014;14:741.   7. Longo UG, et al. JBJS Br 2012;94-B:1546.")

    # ---- 5 transitional anatomy changes the count (Figure 1)
    fig_left(prs, proto_fig, "Background", "Transitional anatomy changes the count",
             FIGS2 / "sn_figure1.png", [
        "A sixth lumbar vertebra (a), a thirteenth thoracic (b), a fifth lumbar fused to the sacrum (c), or four lumbar bodies (d): each changes what the count means.",
        "8.8 % of 3,147 full-length radiographs lacked 24 presacral segments (Sabri 2025). In 550 lumbar operations the count was wrong in 38 of 71 patients with a lumbosacral transitional vertebra (Nakagawa 2017).",
        "The transitional truth exists on CT, where the rib, the ala and the sacral segments are in the volume. No released radiograph or C-arm frame anywhere carries a human-read T13 or Castellvi grade (hatched).",
        "Rows: labelled CT; its render; another patient's real film. Bar, 20 mm.   8. Sabri SA, et al. Neurosurg Focus 2025.   9. Nakagawa T, et al. 2017."],
             footer, img_w=4600000, size=14)

    # ---- 6 what a wrong level costs
    chart_slide(prs, proto_fig, "Background", "What a wrong level costs, and what avoiding it costs",
                FIGS2 / "cited_cost_composite.png", [
        "After the event: 17 % of self-reported wrong-level events led to legal action or settlement (Mody 2008); nearly one in five Spine Section respondents has been sued for a wrong-level or wrong-side lumbar operation (Groff 2013); 81 % of litigated wrong-disc-level cases ended in a payment, surgeons prevailing in 42 % of jury trials (Goodkin & Laska 2004).",
        "Per paid claim: the median National Practitioner Data Bank payment for a surgical never event is $75,220 (IQR $28,847–$215,003; Bettis 2026). In England, 978 spinal-surgery claims over five years were valued at £535.5 million, 26 of them never events (Machin 2018).",
        "Before it, to avoid it: one centre placed gold fiducials in 179 patients over 38 months, 176 thoracic, solely to mark a level: 51.9 minutes and 183 mGy each (AJNR 2023); at $34–37 per operating-room minute (Childers 2018), about $1,750–1,950 per patient and 155 staffed hours. In theatre, needles every few levels are counted cephalad from the sacrum on lateral fluoroscopy (Strong 2022)."],
                footer, note="Derived, not measured: at 1.3–1.6 million US spine operations a year the two verified rates give roughly 420–1,900 wrong-level operations, and the litigation and payment fractions put indemnity alone on the order of $8–37 million a year, before reoperation, stay and disability.",
                caption="Left: Bettis et al. 2026, Figure 1, National Practitioner Data Bank payment reports for surgical never events by code, 1991–2025 (Patient Saf Surg, open access). Right: AJNR Am J Neuroradiol 2023;44:618, Figure 1, biplane fluoroscopy placing a gold fiducial at T4 and the postprocedural counting images (PMC10171395). Permission pending.",
                img_w=6700000, max_h=2650000, note_under_figure=True,
                refs="10. Goodkin R, Laska LL. Surg Neurol 2004;61:323.   11. Bettis T, et al. Patient Saf Surg 2026.   12. Machin JT, et al. Eur Spine J 2018;27:2693.   13. AJNR Am J Neuroradiol 2023;44:618.   14. Childers CP, Maggard-Gibbons M. JAMA Surg 2018;153:e176233.   15. Tan et al. Jt Comm J Qual Patient Saf 2023;49:265.   16. Strong MJ, et al. J Neurosurg Spine 2022;36:792.",
                size=12, note_size=13)

    # ---- 7 what exists: registration
    chart_slide(prs, proto_fig, "Background", "The label on the film is only as right as the planning read",
                FIGS2 / "cited_levelcheck_composite.png", [
        "Registration: LevelCheck projects a reader's preoperative CT labels onto the radiograph (Otake 2012; Lo 2015). Its published accuracies are scored against those labels: 100 % label placement (De Silva 2016); 97.6 %, five surgeons' median on 62 difficult films with the overlay (Manbachi 2018).",
        "On a transitional spine the imported label is only as right as the planning read. Lumbar MRI localisers read without a count from C2 identified the segment in 77.9–82.2 % (Peh 1999).",
        "Registration-free naming on real C-arm images: identity imported from a preoperative radiograph, 73.3 % (Zhang 2023); long-length images of cadavers, 88.3 % (Huang 2022). Nothing published names a level from one exposure on its own, and nothing is tested on a transitional spine."],
                footer, note="Whatever is imported onto the film inherits the count's error. The level has to be read on the exposure itself.",
                caption="Top: De Silva et al. 2016, Figure 1, the LevelCheck pipeline: preoperative CT labels registered onto the intraoperative radiograph (Spine; PMC5045321). Bottom: Manbachi et al. 2018, Figure 6, LevelCheck labels on a 13th rib at L1 (b) and a lumbarised S1 (c) (Ann Biomed Eng; PMC9107073). Permission pending.",
                img_w=4400000, max_h=2550000, note_size=13,
                refs="17. Otake Y, et al. Phys Med Biol 2012.   18. Lo SFL, et al. Spine 2015.   19. De Silva T, et al. Spine 2016.   20. Manbachi A, et al. Ann Biomed Eng 2018.   21. Peh WCG, et al. 1999.   22. Zhang R, et al. J Xray Sci Technol 2023.   23. Huang Y, et al. Comput Methods Programs Biomed 2022.")

    # ---- 8 the planning read fails where the count fails (Not All Spines)
    s, h = fig_left(prs, proto_fig, "Background", "The planning read fails where the count fails",
                    FIGS2 / "nas_gt_vs_ts.png", [
        "TotalSegmentator, the default back end of 3D Slicer, zero-shot on all 1,152 records of CTSpinoPelvic1K: at its published level on normal anatomy (L5 DSC 0.94).",
        "Lumbarization, 14 patients: the lumbar labels slide one level caudally, L1 0.88 → L4 0.39 → L5 0.29; L5 DSC below 0.5 in 10 of 14, and in 9 of 9 count-style sacralizations, against 9 of 750 normals. L6 emitted: 0 of 1,152. The output is confident, well formed and one level off, with no error signal.",
        "A segmenter trained with the last lumbar body as one class restores the junction (DSC 0.36 → 0.95) but on count-style sacralization still labels 82.7 % of L4 voxels as the last lumbar body: a voxel labeller cannot notice that its own sequence does not fit.",
        "So a label registered onto the film from this read carries the miscount with it. Not All Spines Are Created Equal, NeurIPS 2026 Datasets & Benchmarks."],
                    footer, img_w=6300000, size=14)
    tbox(s, LEFT, TOP + h + 60000, 6300000, 500000,
         ["A lumbarization case with a true L6. Left, the ground truth; right, the segmenter's output: L4, L5 and sacrum DSC 0.00."], 11, GREY)

    # ---- 9 hypothesis and purpose (+ four phenotypes rendered)
    fig_top(prs, proto_text, "Hypothesis", "Hypothesis and purpose", FIGS2 / "fig_phenotypes.png", [
        "Hypothesis: each transitional vertebra carries local morphology that a network reading a few bodies can learn, so a level can be named from one C-arm exposure without counting from C2 or importing a label.",
        "Purpose: build that network, SchwingNet; examine what it learns; test it on a C-arm absent from every training set; and count the transitional persons a test of it needs and the public sources hold.",
        "Targets stated before scoring: 90 % exact naming on transitional persons (Wilson lower bound), 85 % sensitivity to the variant, 97 % vertebra detection on the unseen device."],
        footer, max_h=2600000, size=13,
        note="Four phenotypes at the lumbar borders, aligned on the sacrum (CTSpinoPelvic1K records 0704, 0428, 0094, 0005).   The clinical role sought: decision support that abstains visibly beside the surgeon's count, never a replacement for the check film.")

    # ---- 10 materials
    chart_slide(prs, proto_fig, "Materials", "What exists to learn from",
                FIGS2 / "chart_corpus.png", [
        "All public: renders of labelled CT from CTSpinoPelvic1K (801 patients), TotalSegmentator v2 and v3 (1,935 scans) and VerSe (355 subjects); radiographs with levels from CSXA (4,963 cervical laterals), BUU-LSPINE (3,600 lumbar cases) and NHANES II (364 persons); 4,276 real exposures with three-dimensional truth, 778 of them from mobile C-arms.",
        "The intraoperative set, C-ArmLSpine, is 148 cases on one C-arm with cone-beam CT, held out of every training set.",
        "Not one released radiograph or C-arm frame carries a human-read T13 or Castellvi grade. The renders of labelled CT are the only labelled source of those classes.",
        "Every source is split by person. A patient-keyed evaluation gate checks each quoted number against the training lineage of the checkpoint that produced it; numbers found on a seen patient were re-run held out."],
                footer, note="Median age across the eight releases that give it, 36–66 years; 42.5–64.5 % female. The intraoperative, cadaveric and phantom sets release no age, sex or indication.",
                refs="Sources, licences and download locations are listed per release in the manuscript; VinDr-SpineXR under a PhysioNet data use agreement.",
                max_h=3150000, note_size=13)

    # ---- 11 what SchwingNet does (+ the two exposures)
    s = content_slide(prs, proto_flow, "SchwingNet", "What SchwingNet does: inputs and outputs")
    set_text(shape(s, "Rounded Rectangle 24"), "1 · Find")
    set_text(shape(s, "TextBox 25"), ["the bodies and the sacrum are boxed;", "no level name is attached"])
    set_text(shape(s, "Rounded Rectangle 27"), "2 · Name")
    set_text(shape(s, "TextBox 28"), ["each body is named from its own shape,", "a posterior beside the name"])
    set_text(shape(s, "Rounded Rectangle 30"), "3 · Check")
    set_text(shape(s, "TextBox 31"), ["against the count from the detected sacrum:", "agree, a name; disagree, a stop"])
    w, h = fit(FIGS2 / "sn_fig4_ab_img.png", 4400000, 2250000)
    picture(s, FIGS2 / "sn_fig4_ab_img.png", LEFT, 3450000, width=w, height=h)
    tb = shape(s, "TextBox 32")
    tb.left = Emu(LEFT + w + 300000)
    tb.top = Emu(3400000)
    tb.width = Emu(RIGHT - (LEFT + w + 300000))
    tb.height = Emu(2500000)
    set_para(tb, [
        "One exposure in. Out, for every body in the field: a level name with its posterior, the ordinal counted from the sacrum when a sacrum is in view, and a flag when the two readings disagree. Neither end of the spine is needed, and no label is imported from another study.",
        "Trained on the renders of labelled CT and the annotated radiographs; the intraoperative C-arm is in no training set. Fitted image-formation parameters for each device, the trained weights and the code accompany the paper.",
        "The architecture, how the two readings are combined and when the read stops are withheld under the Wayne State University invention disclosure. What follows is how it was tested and what it did."], size=13)
    set_text(shape(s, "TextBox 33"), "Left: a real lateral exposure, bodies and sacrum boxed. Right: field b named from shape alone, a posterior beside each name.   Nothing shown is a device.")
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 12 how it was tested
    chart_slide(prs, proto_fig, "SchwingNet", "How it was tested",
                FIGS2 / "chart_testset.png", [
        "Test set: C-ArmLSpine, 148 intraoperative cases, anteroposterior and lateral exposures, truth from cone-beam CT. Of 910 cone-beam vertebrae, 814 (89.5 %) were named identically by two automatic labellers and kept: 676 agreed lateral bodies in 143 cases, 673 anteroposterior in 143.",
        "Three readings of the same frames: never trained on this C-arm (zero-shot); fine-tuned by case-grouped folds; fine-tuned by acquisition-day folds.",
        "Scored per detected body as exact level; intervals cluster-adjusted by case; paired differences with exact sign tests, Holm-adjusted over the comparisons named before scoring.",
        "No transitional test person of the built split is scored here: most sat in the current encoder's training lineage, so the three C-ArmLSpine L6 patients are scored only in cross-validation and reported as such."],
                footer, note="Every percentage carries its denominator. Every number in the paper is read by the build from a result file at a named path, and the build fails on a number that is pending or unused; a patient-keyed gate swept 563 quoted numbers against checkpoint lineages.",
                img_w=6000000, size=13, note_size=13)

    # ---- 13 embedding
    fig_left(prs, proto_fig, "Results", "A sixth lumbar vertebra has a shape of its own",
             FIGS2 / "sn_fig2_ab.png", [
        "The embedding of 13,009 validation crops from 1,612 people (the checkpoint-selection split): the nearest crop from another person is the same level in 74.9 % (95 % CI 72.2, 77.6) and within one level in 93.8 %.",
        "L6 separates from L5 (silhouette 0.35; 0.31, 0.39; 98 crops, 10 persons) more than L5 from L4 (0.23) and as far as L1 from T12 (0.32), the rib boundary.",
        "It named 75 of 98 L6 crops L6, and 111 of 1,012 L5 crops L6. In three never-seen patients one CT labeller reads six-lumbar (stars), the contested body sat nearer the L6 cluster only under whole-vertebra boxes; in two of four fused-L5 persons the last free body was named L5, the name a count gives.",
        "(a) Every level, C1 to sacrum; (b) the lumbosacral window. No T13 was held out to embed."],
             footer, img_w=6900000, size=14)

    # ---- 14 unseen C-arm naming
    fig_left(prs, proto_fig, "Results", "One lateral exposure of a C-arm the network never saw",
             FIGS2 / "sn_fig4_ab.png", [
        "First the bodies and the sacrum are boxed without any level name (a): 617 of 676 agreed lateral bodies (91.3 %).",
        "Then each body is named from its shape alone (b). Never trained on this C-arm: 595 of 617 lateral bodies exact (96.4 %; 92.3, 98.4); anteroposterior 276 of 631 (43.7 %); paired difference 54.3 points, P < .001.",
        "Fine-tuned by case-grouped folds: lateral 601 of 617 (97.4 %), anteroposterior 608 of 631 (96.4 %), +1.0 and +52.6 points over zero-shot. By acquisition-day folds: lateral 92.1 %, 4.4 points below zero-shot.",
        "With three bodies in view 1,079 of 1,159 (93.1 %); with one body 451 of 603 (74.8 %). A field that holds nothing to count from still yields a name, with its posterior."],
             footer, img_w=7300000, size=14)

    # ---- 15 count, coupling, stop
    chart_slide(prs, proto_fig, "Results", "Two readings of one frame, and a stop where they disagree",
                FIGS2 / "chart_coupling.png", [
        "On the 1,009 bodies of frames with a detected sacrum: the count from the sacrum in the ordinary five-lumbar alphabet, no shape used, was exact on 979 (97.0 %; 94.2, 99.2); shape alone, the fine-tuned model, on 986 (97.7 %); both together on 991 (98.2 %; 96.5, 99.5), 1.2 points over the count (0.0, 3.2) and 0.5 over shape alone.",
        "The read declined to name 23 of 233 anchored frames. Those 23 hold five of the six frames carrying an error, and all four six-lumbar calls: three on five-lumbar frames, one on the four anchored frames of the three patients one labeller reads six-lumbar.",
        "On that frame the output is a stop, not a verdict: the two readings are reported as disagreeing rather than resolved."],
                footer, note="On the one exposure the surgeon has, the level is named from shape, checked against the count from the sacrum, and a disagreement between them is reported, not hidden.",
                refs="How the two readings are combined and when the read stops are withheld under the invention disclosure; every number here is from public exposures scored against cone-beam CT.",
                max_h=3300000, note_size=13)

    # ---- 16 detection: frames and angles
    fig_left(prs, proto_fig, "Results", "Finding the vertebrae on a new device: frames and angles",
             FIGS2 / "sn_fig5_cd.png", [
        "Detection, not naming, lost most to the unseen device. The held-out detector found 231 of 287 bodies (80.5 %; 74.1, 86.8) at the cross-device operating point, short of the pre-stated 97 %; on the 214 truth boxes that are complete, body-sourced and inside the field, 201 (93.9 %; 90.4, 97.1).",
        "(c) With the device's own frames: 7 % with none, a plateau from 24 frames (84 %; 95.6 % on the repaired denominator). The plateau is the truth cut at the edge of the field, not the detector. Trained on one view, it found 0–40 % of the other view's bodies.",
        "(d) Render-trained detectors that saw only anteroposterior and lateral poses: 82 % at those angles, 53 % over the arc between. Doubling those frames: 94 and 65 %. The same count spread over the arc: 81 and 77 %.",
        "Accuracy followed where the frames sat in acquisition space, not how many there were."],
             footer, img_w=6500000, size=13)

    # ---- 17 persons and views
    fig_left(prs, proto_fig, "Results", "How many people it takes, and which view they were shot in",
             FIGS2 / "sn_fig5_ab.png", [
        "(a) Certifying 90 % naming on transitional anatomy at zero errors needs 35 at-risk test persons; 85 % sensitivity to the variant needs 22 carriers.",
        "(b) Naming rose with training persons on every film corpus: NHANES II 77.8 → 92.7 % (264 persons), BUU-LSPINE 65.0 → 96.9 % (2,967), CSXA 94.2 → 99.8 % (4,114). Transfer between corpora peaked at 74.3 %.",
        "On the C-arm it rose by view rather than by count: lateral 93.7 % with no C-arm person and 98.1 % with 50; anteroposterior 33.8 % with none, 90.8 % with five, 98.1 % with all. A lateral-trained model read anteroposterior bodies at 54.7 %; training both views cost neither (98.1 and 97.0 %)."],
             footer, img_w=7300000, size=14)

    # ---- 18 transitional naming on real exposures
    chart_slide(prs, proto_fig, "Results", "Transitional naming on real exposures: shown and not shown",
                FIGS2 / "chart_census.png", [
        "What was scored: three C-ArmLSpine patients whose sixth lumbar vertebra one labeller reads and the other does not, scored only in cross-validation, agreeing with that read on one of five bodies; all four L6 calls stopped. The embedding places their contested body nearer L6 only under one box convention. That is a description, not a test of transitional naming. No accuracy here is a wrong-level surgery rate.",
        "What a test needs: 35 error-free at-risk persons on real exposures certify 90 %; 22 carriers certify 85 % on the variant. Seven candidates with an exported real frame exist today; error-free they would bound 64.6 %.",
        "Where they will come from: a census of 22 public CT collections, two automatic labellers per scan, 18,873 CTs listed, an expected 320 six-lumbar spines, 160 four-lumbar, 900–1,800 Castellvi II–IV and 40–120 T13; 21 L6 called by both labellers so far. Each confirmed case is a labelled render for the model and, where a radiograph exists, a test person."],
                footer, note="The powered comparison with registration carrying a planning read, on verified at-risk persons, against a comparator fixed before scoring, is a separate study.",
                refs="Two-labeller screening of public CT for transitional anatomy: presented at AACA 2026.", size=12)

    # ---- 19 limitations and next steps (+ the coverage chart)
    s = content_slide(prs, proto_limits, "Limitations", "Limitations and next steps")
    set_para(shape(s, "TextBox 24"), [
        "Limitations",
        "One intraoperative device; its truth is two automatic labellers agreeing, which removes the thoracolumbar junction and cannot settle a transitional count.",
        "Whether 148 cases are 148 people cannot be established; every intraoperative interval is too narrow if they are not. Day-grouped fine-tuning scored below zero-shot laterally.",
        "The embedding is of the split that chose the checkpoint; the posterior is uncalibrated; held-out detector numbers use whole-vertebra boxes.",
        "Retrospective, public data. Nothing has been evaluated prospectively; nothing shown is a device."], size=14, gap=7)
    w, h = fit(FIGS2 / "chart_coverage.png", 5350000, 2300000)
    picture(s, FIGS2 / "chart_coverage.png", 6172200, TOP, width=w, height=h)
    tb = shape(s, "TextBox 25")
    tb.top = Emu(TOP + h + 150000)
    tb.height = Emu(BOTTOM - (TOP + h + 150000))
    set_para(tb, [
        "Next steps",
        "Verify the transitional candidates by two human readers and run the pre-stated test: 35 persons, zero errors.",
        "A second C-arm, with obliques, added to the corpus and held out; the comparison with registration on verified at-risk persons.",
        "Phantom, cadaver and human series, in that order, before any operating-room use."], size=13, gap=5)
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 20 conclusions (+ the headline chart)
    s = content_slide(prs, proto_concl, "Conclusions", "Conclusions")
    tb = shape(s, "TextBox 24")
    tb.width = Emu(6900000)
    set_para(tb, [
        "A vertebral level is counted, not marked. The count fails on transitional anatomy, the label registered onto the film inherits the planning read's miscount, and a deployed CT segmenter reproduces that miscount with no error signal.",
        "SchwingNet names a level from the shapes of the bodies in one exposure. Never trained on the intraoperative C-arm, it named 96.4 % of detected lateral vertebrae exactly; counting from the detected sacrum was exact on 97.0 %; the coupled call on 98.2 %, and it stopped on 23 of 233 frames holding five of the six errors.",
        "Its transitional naming on real exposures is unverified: three cross-validation patients carry the only real transitional exposures scored, certifying 90 % needs 35 error-free at-risk persons, and the census is being built to supply them."], size=15, gap=9)
    w, h = fit(FIGS2 / "chart_headline.png", 4500000, 3300000)
    picture(s, FIGS2 / "chart_headline.png", RIGHT - w, TOP, width=w, height=h)
    set_text(shape(s, "Rounded Rectangle 25"),
             "A name from shape, checked against the count, with a stop where they disagree: decision support beside the surgeon's count, never a replacement for the check film.")
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 21 thanks (+ the dataset's anchors)
    s = content_slide(prs, proto_thanks, "Thank you", "Acknowledgments and data availability")
    shape(s, "TextBox 24").width = Emu(7000000)
    set_para(shape(s, "TextBox 24"), [
        "Coauthors and annotators: Patrick Schwing; Miraziz Ismoilov and Nizar Alnabahneh (Radiology, DMC/WSU); Loren Schwiebert (Computer Science, WSU); Ashley Schehr, [student A], [student B], [student C], [student D], [student E], [student F], [student G], [student H], [student I], [student J] (WSU School of Medicine).",
        "Data: CTSpinoPelvic1K, doi.org/10.5281/zenodo.22139642 (CC BY-NC-SA 4.0); C-ArmLSpine, COBRA2026, DeepFluoro, TotalSegmentator, VerSe, CSXA, BUU-LSPINE, NHANES II and VinDr-SpineXR under their own licences.",
        "Code and weights: github.com/OpenSpineConsortium; huggingface.co/OpenSpineConsortium.",
        "Papers: Not All Spines Are Created Equal (NeurIPS 2026 Datasets & Benchmarks); CTSpinoPelvic1K dataset article (Medical Physics, submitted); SchwingNet (in preparation).",
        "Funding: NIH NIGMS F30GM147909. Compute: Wayne State University Grid."], size=15, gap=4)
    set_text(shape(s, "Rounded Rectangle 25"), ["Questions", "gregory.schwing@med.wayne.edu", "openspineconsortium.com"])
    w, h = fit(FIGS2 / "fig_anchors.png", 4206240, 1500000)
    picture(s, FIGS2 / "fig_anchors.png", 7406640, 3750000, width=w, height=h)
    set_text(shape(s, "TextBox 23"), footer)

    # ---- drop the template's own content slides 4..17 (indices 3..16), keep 1..3
    xml_slides = prs.slides._sldIdLst
    RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    entries = list(xml_slides)
    for idx in range(16, 2, -1):
        r = entries[idx]
        xml_slides.remove(r)
        prs.part.drop_rel(r.get(RID))
    prs.save(str(out))
    print("wrote", out, "slides:", len(prs.slides))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--abstract", default="Abstract [number pending]")
    ap.add_argument("--session", default="[session pending]")
    ap.add_argument("--out", default=str(Path.home() / "OneDrive/Desktop/CNS2026_Schwing_SchwingNet.pptx"))
    a = ap.parse_args()
    build(a.abstract, a.session, Path(a.out))
