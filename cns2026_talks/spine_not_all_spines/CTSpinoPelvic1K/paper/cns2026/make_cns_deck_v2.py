"""paper/cns2026/make_cns_deck_v2.py — the CNS 2026 spine talk, version 2 (2026-09-25): one arc across the three
papers, results only.

    Not All Spines Are Created Equal (NeurIPS 2026 D&B)  ->  CTSpinoPelvic1K (dataset article)  ->  SchwingNet (RSNA AI)

Greg's framing: transitional anatomy is easier to confirm on CT than on a radiograph, hence the order in which the
work was done and is presented: label on CT, test what CT segmenters do with it, then carry the name to the C-arm.

"Show what, not how": every SchwingNet slide states what the system did on public exposures and how it was tested;
no architecture, no decoder, no coupling rule, no abstention rule, no device model. The SchwingNet figure panels
that draw the mechanism (Figure 3; Figure 4c, d; Figure 2c, d) are not on any slide. The invention disclosure is
named on the disclosures slide.

Built on the lab's CNS template exactly as make_cns_deck.py builds the first version: the template's section-header
slides are duplicated, their section tag, title, footer and logo kept, the body replaced. Titles are kept to one
line (about 60 characters) because a second title line runs under the section icon at the top right; wide text
under a figure stops at 5.65M EMU and left-hand figures at 5.70M because the WSU shield sits at the bottom left.

    python paper/cns2026/make_cns_deck_v2.py --abstract "Abstract NNN" --session "..." --out CNS2026_Schwing_Spine_v2.pptx
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt

from make_cns_deck import (INK, TEAL, content_slide, dup_slide, picture, remove, set_text, shape, textbox)  # noqa: F401

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TEMPLATE = ROOT / "CNS2026_Schwing_Abstract418.pptx"
FIGS = HERE / "figs"          # version-1 figures (fov, ...)
FIGS2 = HERE / "figs_v2"      # rasterised dataset-article figures, SchwingNet crops, NeurIPS panel

LEFT = 256032
RIGHT = 11935968          # LEFT + 11,679,936
TOP = 1371600
BOTTOM = 6200000          # the footer band starts at 6,341,806 (right-hand text columns may run to here)
BOTTOM_WIDE = 5650000     # full-width text must stop above the WSU shield (Group 1: x 0.59-1.18M, y from 5.74M)
IMG_BOTTOM = 5700000      # left-aligned figures likewise


def img_size(path):
    with Image.open(path) as im:
        return im.size


def fit(path, max_w, max_h):
    """Width and height (EMU) that fit the image inside max_w x max_h, aspect kept."""
    w, h = img_size(path)
    scale = min(max_w / w, max_h / h)
    return int(w * scale), int(h * scale)


def set_para(shp, lines, size=None, gap=6):
    """set_text, then the same spacing on every paragraph (the template's first paragraph carries space-after that
    add_paragraph does not copy, which left one wide gap and then none)."""
    set_text(shp, lines, size=size)
    for p in shp.text_frame.paragraphs:
        p.space_before = Pt(0)
        p.space_after = Pt(gap)


def fig_left(prs, proto, section, title, img, lines, footer, img_w=7000000, size=14):
    """Picture on the left (at most img_w wide, stopping above the shield), text column on the right."""
    s = content_slide(prs, proto, section, title)
    remove(s, "Picture 24", "TextBox 26", "Table 26", "TextBox 27")
    w, h = fit(img, img_w, IMG_BOTTOM - TOP)
    picture(s, img, LEFT, TOP, width=w, height=h)
    tb = shape(s, "TextBox 25")
    tb.left = Emu(LEFT + w + 300000)
    tb.top = Emu(TOP)
    tb.width = Emu(RIGHT - (LEFT + w + 300000))
    tb.height = Emu(BOTTOM - TOP)
    set_para(tb, lines, size=size)
    set_text(shape(s, "TextBox 23"), footer)
    return s, h


def fig_top(prs, proto, section, title, img, lines, footer, max_h=3300000, size=14, note=None):
    """Picture across the top, text underneath. proto = the background text slide (TextBox 24, footnote TextBox 31)."""
    s = content_slide(prs, proto, section, title)
    remove(s, "Oval 25", "Oval 26", "Oval 27", "TextBox 28", "TextBox 29", "TextBox 30")
    w, h = fit(img, RIGHT - LEFT, max_h)
    picture(s, img, LEFT + (RIGHT - LEFT - w) // 2, TOP, width=w, height=h)
    tb = shape(s, "TextBox 24")
    tb.left = Emu(LEFT)
    tb.top = Emu(TOP + h + 160000)
    tb.width = Emu(RIGHT - LEFT)
    tb.height = Emu(BOTTOM_WIDE - (TOP + h + 160000))
    set_para(tb, lines, size=size)
    if note:
        set_text(shape(s, "TextBox 31"), note)
    else:
        remove(s, "TextBox 31")
    set_text(shape(s, "TextBox 23"), footer)
    return s


def two_boxes(prs, proto, section, title, left_head, left_lines, right_head, right_lines, bar, refs, footer, size=None):
    s = content_slide(prs, proto, section, title)
    set_text(shape(s, "Rounded Rectangle 24"), left_head)
    set_para(shape(s, "TextBox 25"), left_lines, size=size)
    set_text(shape(s, "Rounded Rectangle 26"), right_head)
    set_para(shape(s, "TextBox 27"), right_lines, size=size)
    set_text(shape(s, "Rounded Rectangle 28"), bar)
    set_text(shape(s, "TextBox 29"), refs)
    set_text(shape(s, "TextBox 23"), footer)
    return s


# ---------------------------------------------------------------------- content
def build(abstract: str, session: str, out: Path):
    prs = Presentation(str(TEMPLATE))
    T = list(prs.slides)
    footer = f"CNS 2026  ·  Washington, DC  ·  {abstract}"

    # ---- 1 title (edited in place)
    s = T[0]
    set_text(shape(s, "TextBox 1030"),
             "Naming a Lumbar Level Without Counting From C2: From the CT Label to the C-arm Exposure")
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

    # ---- 2 disclosures
    s = T[1]
    set_para(shape(s, "TextBox 24"), [
        "The authors have no relevant financial relationships to disclose.",
        "All imaging is public and de-identified; the Wayne State University IRB determined the work is not human-participant research (2 September 2026). Funding: NIH NIGMS F30GM147909.",
        "An invention disclosure covering the level-naming system is on file with Wayne State University. This talk shows what the system does and how it was tested; its methods are withheld until that review is complete.",
        "Nothing shown is a medical device. The C-arm results are retrospective, on public exposures, and have not been evaluated prospectively."])
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 3 overview
    s = T[2]
    set_text(shape(s, "Title 11"), "One question, three papers, in the order the anatomy allows")
    set_text(shape(s, "TextBox 23"), footer)
    items = [
        "The problem — a lumbar level is named by counting from C2, and the study a lumbar case is planned on has no C2",
        "CT first — transitional anatomy can be confirmed on CT, so that is where the labels were made: CTSpinoPelvic1K, 802 records, every anomaly a class of its own",
        "What today's CT segmenters do with it — the most deployed tool reproduces the pattern of a one-level miscount on lumbarization (Not All Spines Are Created Equal, NeurIPS 2026)",
        "The same name on the image the surgeon looks at — a network names lumbar levels on one exposure of a C-arm it never saw (SchwingNet)",
        "What is still owed — the transitional test persons that certify it, and the CT census being built to find them",
    ]
    for name, txt in zip(("TextBox 25", "TextBox 27", "TextBox 29", "TextBox 31", "TextBox 33"), items):
        set_text(shape(s, name), txt)

    proto_text = T[3]        # text column (+ ovals to remove), footnote TextBox 31
    proto_two = T[4]         # two headed boxes + bar + refs
    proto_flow = T[6]        # three boxes with arrows + big text
    proto_fig = T[7]         # picture left, text right
    proto_concl = T[14]
    proto_limits = T[15]
    proto_thanks = T[16]

    # ---- 4 background: the count
    s = content_slide(prs, proto_text, "Background", "The count fails exactly where the anatomy is transitional")
    remove(s, "Oval 25", "Oval 26", "Oval 27", "TextBox 28", "TextBox 29", "TextBox 30")
    set_para(shape(s, "TextBox 24"), [
        "Wrong-level spine surgery runs at about one in 3,100 spinal procedures, and the cause most often cited is transitional anatomy.¹",
        "A lumbosacral transitional vertebra is present in roughly one patient in ten; a thoracolumbar variant (a stump twelfth rib, a lumbar rib, a thirteenth thoracic vertebra) in more.",
        "The gold standard names a level by counting caudally from C2 on whole-spine imaging. A lumbar case is planned on a lumbar study, T12 to S1. C2 is never in it.",
        "So the name rests on local morphology, and the question is whether morphology is enough."], gap=10)
    shape(s, "TextBox 24").width = Emu(6000000)
    picture(s, FIGS / "fig_fov.png", 6500000, TOP, width=5300000)
    set_text(shape(s, "TextBox 31"), "1. Epstein NE. Surg Neurol Int 2021;12:286.   Field of view of 802 abdominopelvic CTs: the thoracic column enters from above; C2 never.")
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 5 background: same count, three anatomies
    fig_top(prs, proto_text, "Background", "The same count, three anatomies", FIGS2 / "fig_phenotypes.png", [
        "Four rib-free bodies above the sacrum: an L1 that carries a lumbar rib and is counted thoracic (b), or an L5 assimilated to the sacrum (c). Same count, opposite surgical anatomy.",
        "Six rib-free bodies (d): a true sixth lumbar vertebra, a T12 whose ribs are aplastic and is counted lumbar, or a first sacral segment that separated.",
        "The origin of the border vertebra decides where the mobile junction is, which root exits beneath it, and which end plate the pelvic parameters were measured on.²"],
        footer, max_h=2800000, size=13,
        note="2. Konin GP, Walz DM. AJNR 2010;31:1778–1786.   Records 0704, 0428, 0094 and 0005 of CTSpinoPelvic1K, aligned on the sacrum.")

    # ---- 6 why CT first (the arc)
    s = content_slide(prs, proto_flow, "Background", "Why CT came first: confirmable on CT, only inferred on film")
    set_text(shape(s, "Rounded Rectangle 24"), "1 · Confirm and label on CT")
    set_text(shape(s, "TextBox 25"), ["CTSpinoPelvic1K, 802 records:", "every anomaly a class of its own"])
    set_text(shape(s, "Rounded Rectangle 27"), "2 · Test the tools that read CT")
    set_text(shape(s, "TextBox 28"), ["Not All Spines: a deployed segmenter", "at the lumbosacral junction"])
    set_text(shape(s, "Rounded Rectangle 30"), "3 · Carry the name to the C-arm")
    set_text(shape(s, "TextBox 31"), ["SchwingNet: the level from shape", "on one exposure, nothing to count"])
    set_para(shape(s, "TextBox 32"), [
        "On CT the evidence that makes a vertebra transitional is in the volume: the rib on the lowest thoracic body, the transverse process meeting the sacral ala, the disc or its absence beneath the last free body, the number of sacral segments. A reader can confirm it and a label can record it.",
        "On a radiograph or a C-arm frame those structures overlap, the field holds neither end of the spine, and no released radiograph anywhere carries a human-read T13 or Castellvi grade. The transitional truth exists on CT and nowhere else.",
        "So the work ran in that order. Label the anatomy where it can be confirmed; measure what CT tools do with it; then carry the name to the image the surgeon looks at, and count what it will take to certify it there."], size=14)
    set_text(shape(s, "TextBox 33"), "3. Castellvi AE, et al. Spine 1984;9:493–495.   4. Carrino JA, et al. Radiology 2011;259:196–202.")
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 7 CTSpinoPelvic1K: the dataset
    fig_top(prs, proto_text, "The dataset", "Two anchors on every record, and a class for every anomaly", FIGS2 / "fig_anchors.png", [
        "802 abdominopelvic CT records (TCIA CT COLONOGRAPHY): CTSpine1K's vertebrae and CTPelvic1K's pelvis joined on one series, plus per-level ribs, femora, a separate S1 and surgical hardware on every record.",
        "Levels are anchored on the lowest rib-bearing vertebra and on S1, never on a count. L6, T13, lumbar ribs and stump ribs are recorded as themselves: 18 six-lumbar spines, 16 lumbar ribs, 98 stump twelfth ribs, 33 two-reader Castellvi grades (κ 0.74).",
        "Validated before any number was believed: 802 of 802 pass the geometric invariants; 5,753 ribs, 0.035 % offset; spinopelvic measures match published values. Zenodo 10.5281/zenodo.22139642; dataset article submitted to Medical Physics."],
        footer, max_h=2550000, size=13)

    # ---- 8 CTSpinoPelvic1K: prior art
    fig_top(prs, proto_text, "The dataset", "The only CT collection whose labels can say what is there", FIGS2 / "fig_priorart.png", [
        "CTSpine1K and VerSe number the vertebrae but hold no pelvis; CTPelvic1K and RibSeg hold no lumbar count; TotalSegmentator's scheme has no L6, no lumbar rib and no transitional grade. VerSe graded Castellvi and used the grade to exclude.",
        "CTSpinoPelvic1K is not the largest, but it is the only public CT collection whose label scheme can represent every reading at the junction: the count, L6, sacrum and S1, pelvis, per-level ribs, a lumbar rib, the femora and a transitional grade."],
        footer, max_h=3100000, size=13)

    # ---- 9 CTSpinoPelvic1K: what the labels say without a count
    fig_top(prs, proto_text, "The dataset", "What 802 labelled spines say when nothing is counted from C2", FIGS2 / "fig_countfree.png", [
        "(a) Rib-free bodies above the sacrum: 29 records with four, 744 with five, 28 with six.   (b) The lowest rib's length is bimodal: a stump twelfth rib in 98 of 788 (12.4 %), a lumbar rib in 16 of 802 (2.0 %), against 12.6 and 1.5 % in the published series.",
        "(c) In the six-lumbar spines (orange) the lowest body's transverse process sits nearer the ilium than any ordinary L5 in a subset. Read from the labels alone: 11 are a true L6, 4 a separated first sacral segment, 1 a rib-less T12, 2 carry evidence at both ends.",
        "Shape separates levels inside a patient: eleven size-normalised features, cross-validated by patient, give T12 against L1 at AUC 0.990 and 97.3 % over 1,485 vertebrae. Identity is local; the count is a convention laid over it."],
        footer, max_h=2500000, size=13)

    # ---- 10 Not All Spines: the audit
    s, h = fig_left(prs, proto_fig, "Not All Spines", "What the most deployed CT segmenter does with an L6",
                    FIGS2 / "nas_gt_vs_ts.png", [
        "TotalSegmentator (the default back end of 3D Slicer), zero-shot at full resolution, on all 1,152 CTSpinoPelvic1K records: on normal anatomy it performs at its published level (L5 DSC 0.94).",
        "Lumbarization, 14 patients: the lumbar labels slide one level caudally, L1 0.88 → L4 0.39 → L5 0.29; junction DSC 0.82 → 0.36 (three scorable). L5 DSC falls below 0.5 in 10 of 14, and in 9 of 9 count-style sacralizations, against 9 of 750 normals.",
        "L6 emitted: 0 of 1,152 records. The scheme has no such class, so the output is confident, well formed and one level off: the pattern of a wrong-level count, with no error signal for anyone downstream.",
        "No existing CT benchmark surfaces this, because none is stratified by transitional phenotype."],
                    footer, img_w=6300000, size=14)
    textbox(s, LEFT, TOP + h + 60000, 6300000, 500000,
            ["A lumbarization case with a true L6. Left, the ground truth; right, the segmenter's output: L4, L5 and sacrum DSC 0.00."], size=11)

    # ---- 11 Not All Spines: the fix and its limit
    two_boxes(prs, proto_two, "Not All Spines", "The junction gap closes; voxel labelling then hits its limit",
              "Trained on CTSpinoPelvic1K, released", [
                  "The last lumbar body is one class whatever the count; five patient-grouped, LSTV-stratified folds; weights released.",
                  "Junction DSC on held-out lumbarization: 0.357 → 0.946 (+58.9 points; one case with a scorable junction, three cases non-degenerate).",
                  "Sacrum 0.817 → 0.969 on 113 held-out records: the best openly released dual spinopelvic CT segmenter."],
              "Where semantic segmentation stops", [
                  "Same data, same folds, an explicit L6 class instead of the merge: most ground-truth L6 voxels are still labelled L5.",
                  "Count-style sacralization: 82.7 % of L4 voxels labelled as the last lumbar body.",
                  "A voxel labeller cannot notice that its own sequence does not fit twelve, five and a sacrum. Naming the sequence is a different task, and it needs a reader."],
              "Any CT segmenter claiming readiness for surgical planning should report per-class DSC and L5/S1 confusion on a transitional cohort, with each stratum's n beside the number.",
              "5. Schwing GJ, Schwing P, Ismoilov M, Alnabahneh N, Schwiebert L. Not All Spines Are Created Equal. NeurIPS 2026 Datasets & Benchmarks.",
              footer, size=14)

    # ---- 12 SchwingNet: the corpus and its transitional phenotypes
    fig_left(prs, proto_fig, "SchwingNet", "To the C-arm: what exists to learn from, and what does not",
             FIGS2 / "sn_figure1.png", [
        "Public sources only: 4,093 renders of labelled CT, 9,108 level-annotated radiographs from four corpora, 4,276 real exposures with three-dimensional truth, 778 of them from mobile C-arms.",
        "194 transitional persons across the sources: 110 with an L6 (three intraoperative), seven with a T13, 28 with a sacralised L5 (12 four-lumbar), 31 Castellvi I/II, 14 with a lumbar rib.",
        "No released radiograph or C-arm frame anywhere carries a human-read T13 or Castellvi grade (hatched). The transitional truth exists only on CT, which is why CT came first, and why the renders of labelled CT are the only labelled source of the rare classes.",
        "Rows: labelled CT; its render; another patient's real film. Bar, 20 mm."],
             footer, img_w=4600000, size=14)

    # ---- 13 SchwingNet: what it learns about a vertebra's shape
    fig_left(prs, proto_fig, "SchwingNet", "A sixth lumbar vertebra has a shape of its own",
             FIGS2 / "sn_fig2_ab.png", [
        "A level model trained to name a vertebra from its own appearance, with nothing to count from. Its embedding of 13,009 validation crops from 1,612 people: the nearest crop from another person is the same level in 74.9 % and within one level in 93.8 %.",
        "L6 separates from L5 (silhouette 0.35; 95 % CI 0.31, 0.39) more than L5 from L4 (0.23) and as far as L1 from T12 (0.32).",
        "It named 75 of 98 L6 crops L6, and 111 of 1,012 L5 crops L6. In three never-seen patients one CT labeller reads six-lumbar (stars), the contested body sat nearer the L6 cluster only under whole-vertebra boxes.",
        "(a) Every level, C1 to sacrum; (b) the lumbosacral window. No T13 was held out to embed."],
             footer, img_w=6900000, size=14)

    # ---- 14 SchwingNet: reading a real C-arm exposure
    fig_left(prs, proto_fig, "SchwingNet", "One lateral exposure of a C-arm the network never saw",
             FIGS2 / "sn_fig4_ab.png", [
        "C-ArmLSpine: 148 intraoperative cases, truth from cone-beam CT, a C-arm outside every training set.",
        "First the bodies and the sacrum are boxed without any level name (a): 617 of 676 agreed lateral bodies (91.3 %).",
        "Then each body is named from its shape alone (b). Never trained on this C-arm: 595 of 617 lateral bodies named exactly (96.4 %; 92.3, 98.4); anteroposterior 43.7 %.",
        "Fine-tuned on other cases of the same C-arm: lateral 97.4 %, anteroposterior 96.4 %.",
        "With three bodies in view 93.1 %; with one body 74.8 %. A field that holds nothing to count from still yields a name, with a posterior beside it."],
             footer, img_w=7300000, size=14)

    # ---- 15 SchwingNet: shape and count together, and knowing when to stop
    two_boxes(prs, proto_two, "SchwingNet", "Two readings of one frame, and a stop where they disagree",
              "Shape and count, each alone and together", [
                  "Count from the detected sacrum in the ordinary five-lumbar alphabet, no shape used: 979 of 1,009 bodies exact (97.0 %).",
                  "Shape alone, the fine-tuned model: 986 of 1,009 (97.7 %).",
                  "Both together: 991 of 1,009 (98.2 %; 96.5, 99.5), 1.2 points over the count alone."],
              "It knows when to stop", [
                  "The read declined to name 23 of 233 anchored frames.",
                  "Those 23 hold five of the six frames carrying an error, and all four six-lumbar calls.",
                  "On the frame one CT labeller reads as six-lumbar, the output is a stop, not a verdict: the two readings are reported as disagreeing rather than resolved."],
              "On the one exposure the surgeon has, the level is named from shape, checked against the count from the sacrum, and a disagreement between them is reported, not hidden.",
              "How the two readings are combined and when the read stops are withheld under the Wayne State University invention disclosure; every number here is from public exposures scored against cone-beam CT.",
              footer, size=14)

    # ---- 16 SchwingNet: persons and views
    fig_left(prs, proto_fig, "SchwingNet", "How many people it takes, and which view they were shot in",
             FIGS2 / "sn_fig5_ab.png", [
        "(a) Certifying 90 % naming on transitional anatomy at zero errors needs 35 at-risk test persons; 85 % sensitivity to the variant needs 22 carriers. No real-exposure transitional person is verified yet; seven candidates exist.",
        "(b) Naming rose with training persons on every film corpus: NHANES II 77.8 → 92.7 %, BUU-LSPINE 65.0 → 96.9 %, CSXA 94.2 → 99.8 %.",
        "On the C-arm it rose by view rather than by count: lateral 93.7 % with no C-arm person and 98.1 % with 50; anteroposterior 33.8 % with none, 90.8 % with five, 98.1 % with all. A lateral-trained model read anteroposterior bodies at 54.7 %; training both views cost neither."],
             footer, img_w=7300000, size=14)

    # ---- 17 SchwingNet: frames and angles
    fig_left(prs, proto_fig, "SchwingNet", "Where the frames sat mattered more than how many there were",
             FIGS2 / "sn_fig5_cd.png", [
        "(c) Finding the vertebrae on a new C-arm: 7 % with none of its frames, a plateau from 24 frames (84 %). On the truth boxes that are complete and inside the field, 95.6 %: the plateau is the truth at the edge of the field, not the detector. Trained on one view, it found 0–40 % of the other view's bodies.",
        "(d) Detectors trained on renders at anteroposterior and lateral poses only: 82 % at those angles, 53 % over the arc between them. Doubling those frames: 94 and 65 %. The same number of frames spread over the arc: 81 and 77 %.",
        "More of the same frames buys little; a frame from an angle or a view not yet seen buys a great deal."],
             footer, img_w=6700000, size=14)

    # ---- 18 what is still owed: the transitional test and the census
    two_boxes(prs, proto_two, "What is owed", "The test still owed, and the CT census that will supply it",
              "The test that certifies it", [
                  "Pre-stated: 35 error-free at-risk persons on real exposures certify 90 %; 22 carriers certify 85 % on the variant.",
                  "Verified today: none on real exposures. The three L6 patients on the intraoperative C-arm are scored only in cross-validation.",
                  "Seven at-risk persons with an exported real frame exist; error-free they would bound 64.6 %."],
              "Where they will come from: a CT census", [
                  "22 public CT collections screened by two independent automatic labellers: 18,873 CTs listed, 16,898 on disk, 12,123 with both lumbosacral references in the field.",
                  "Expected from published prevalence: about 320 six-lumbar spines, 160 four-lumbar, 900–1,800 Castellvi II–IV, 40–120 T13.",
                  "Called so far: 21 L6 by both labellers, 16 T13 by one; 84 disagreements await a human reader."],
              "Every transitional case confirmed on CT becomes a labelled render for the C-arm model and, where a radiograph exists, a test person for it.",
              "Two-labeller screening of public CT for transitional anatomy: presented at AACA 2026.",
              footer, size=14)

    # ---- 19 conclusions
    s = content_slide(prs, proto_concl, "Conclusions", "Conclusions")
    set_para(shape(s, "TextBox 24"), [
        "Transitional anatomy can be confirmed on CT, so the labels were made there. CTSpinoPelvic1K records every anomaly at the lumbar borders as itself: 802 records, two anchors, no count.",
        "The most deployed CT segmenter reproduces a one-level miscount on lumbarization and never emits an L6. A segmenter built on these labels closes the junction gap by 58.9 points and shows where voxel labelling stops: a sequence has to be read, not labelled.",
        "The name carries to the C-arm. On a C-arm it never saw, the network named 96.4 % of lateral bodies exactly from shape alone, 98.2 % with the count coupled, and stopped where the two disagreed. What is owed is the transitional test on real exposures; the census is being built to supply it."], gap=10)
    set_text(shape(s, "Rounded Rectangle 25"),
             "Identity by local shape, checked against the count, with a stop where they disagree: what a wrong-level safeguard needs and a count alone cannot give.")
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 20 limitations and next steps
    s = content_slide(prs, proto_limits, "Limitations", "Limitations and next steps")
    set_para(shape(s, "TextBox 24"), [
        "Limitations",
        "No scan contains C2: the CT readings are morphological consistency, not developmental truth.",
        "33 Castellvi grades, two residents' consensus; 7 transitional cases in the segmenter's held-out split; every stratified number carries its n.",
        "One intraoperative C-arm, 148 cases, ordinary anatomy; transitional naming on real exposures rests on three cross-validation patients.",
        "Retrospective, public data. Nothing has been evaluated prospectively; nothing shown is a device."], gap=8)
    set_para(shape(s, "TextBox 25"), [
        "Next steps",
        "Finish the census; two readers verify each transitional candidate; run the pre-stated test: 35 persons, zero errors.",
        "A second C-arm added to the corpus and held out.",
        "Bench, phantom and cadaver evaluation before any operating-room use.",
        "Data and weights: Zenodo, GitHub and Hugging Face under OpenSpineConsortium; one command onboards a new annotator (openspineconsortium.com/onboarding)."], gap=8)
    set_text(shape(s, "TextBox 23"), footer)

    # ---- 21 thanks
    s = content_slide(prs, proto_thanks, "Thank you", "Acknowledgments and data availability")
    shape(s, "TextBox 24").width = Emu(7000000)
    set_para(shape(s, "TextBox 24"), [
        "Coauthors and annotators: Patrick Schwing; Miraziz Ismoilov and Nizar Alnabahneh (Radiology, DMC/WSU); Loren Schwiebert (Computer Science, WSU); Ashley Schehr, [student A], [student B], [student C], [student D], [student E], [student F], [student G], [student H], [student I], [student J] (WSU School of Medicine).",
        "Data: CTSpinoPelvic1K, doi.org/10.5281/zenodo.22139642 (CC BY-NC-SA 4.0); imaging from TCIA CT COLONOGRAPHY; annotations derive from CTSpine1K and CTPelvic1K.",
        "Code and weights: github.com/OpenSpineConsortium; huggingface.co/OpenSpineConsortium.",
        "Papers: Not All Spines Are Created Equal (NeurIPS 2026 Datasets & Benchmarks); CTSpinoPelvic1K dataset article (Medical Physics, submitted); SchwingNet (in preparation).",
        "Funding: NIH NIGMS F30GM147909. Compute: Wayne State University Grid."], size=15, gap=4)
    set_text(shape(s, "Rounded Rectangle 25"), ["Questions", "gregory.schwing@med.wayne.edu", "openspineconsortium.com"])
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
    ap.add_argument("--out", default=str(Path.home() / "OneDrive/Desktop/CNS2026_Schwing_Spine_v2.pptx"))
    a = ap.parse_args()
    build(a.abstract, a.session, Path(a.out))
