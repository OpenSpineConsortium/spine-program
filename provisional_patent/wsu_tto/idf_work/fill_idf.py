r"""Fill the WSU Invention Disclosure Form (unpacked at idf_work/unpacked) in place.

Answers are written in the form's own blue Calibri answer style; anything only Greg knows is a visible [FILL: ...] or
[CONFIRM: ...] marker. Yes/No boxes get an "X" in the empty cell beside the word. Paragraph-indexed edits (the funding
blanks and the submitter lines) run FIRST because the multi-line answer boxes add paragraphs and shift the indices.
"""
import re, html
from pathlib import Path

DOC = Path(__file__).resolve().parent / "unpacked" / "word" / "document.xml"
x = DOC.read_text(encoding="utf-8")

RPR_ANS = '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Arial"/><w:color w:val="0000FF"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
RPR_X = '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Arial"/><w:b/><w:color w:val="0000FF"/><w:sz w:val="20"/><w:szCs w:val="22"/></w:rPr>'
RPR_LINE = '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:color w:val="0000FF"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'

def esc(t):
    return html.escape(t, quote=False)

def run(text, rpr=RPR_ANS):
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def para_like(template_p, text):
    head = re.match(r"<w:p[^>]*>", template_p).group(0)
    ppr = re.search(r"<w:pPr>.*?</w:pPr>", template_p, flags=re.S)
    return head + (ppr.group(0) if ppr else "") + run(text) + "</w:p>"

def tables():
    return list(re.finditer(r"<w:tbl>.*?</w:tbl>", x, flags=re.S))

def _cell_span(ti, ri, ci):
    t = tables()[ti]; tbl = t.group(0)
    rows = list(re.finditer(r"<w:tr[ >].*?</w:tr>", tbl, flags=re.S)); r = rows[ri]
    cells = list(re.finditer(r"<w:tc>.*?</w:tc>", r.group(0), flags=re.S)); c = cells[ci]
    start = t.start() + r.start() + c.start()
    return start, start + (c.end() - c.start())

def set_cell(ti, ri, ci, lines):
    """Replace the paragraphs of a cell with one paragraph per line (template = the cell's first paragraph)."""
    global x
    a, b = _cell_span(ti, ri, ci); cell = x[a:b]
    tcpr = re.match(r"<w:tc>(<w:tcPr>.*?</w:tcPr>)", cell, flags=re.S).group(1)
    first_p = re.search(r"<w:p[ >].*?</w:p>", cell, flags=re.S).group(0)
    x = x[:a] + "<w:tc>" + tcpr + "".join(para_like(first_p, ln) for ln in lines) + "</w:tc>" + x[b:]

def set_cell_raw(ti, ri, ci, runs_xml):
    global x
    a, b = _cell_span(ti, ri, ci); cell = x[a:b]
    p = re.search(r"<w:p[ >].*?</w:p>", cell, flags=re.S)
    new_p = p.group(0)[:-len("</w:p>")] + runs_xml + "</w:p>"
    x = x[:a] + cell[:p.start()] + new_p + cell[p.end():] + x[b:]

def mark(ti, ri, yes):
    set_cell_raw(ti, ri, 1 if yes else 3, run("X", RPR_X))

def paras():
    return list(re.finditer(r"<w:p[ >].*?</w:p>", x, flags=re.S))

def append_to_para(pi, text):
    global x
    p = paras()[pi]
    x = x[:p.start()] + p.group(0)[:-len("</w:p>")] + run(text, RPR_LINE) + "</w:p>" + x[p.end():]

def replace_label_text(pi, old_label, new_text):
    global x
    p = paras()[pi]; s = p.group(0)
    m = re.search(r"<w:t(?: [^>]*)?>" + re.escape(old_label) + r"</w:t>", s)
    assert m, (pi, old_label)
    x = x[:p.start()] + s[:m.start()] + '<w:t xml:space="preserve">' + esc(new_text) + "</w:t>" + s[m.end():] + x[p.end():]

# ================================================================= 1. paragraph-indexed edits (original indices)
# Funding blanks (paragraphs 220-233)
append_to_para(220, "  National Institutes of Health, National Institute of General Medical Sciences")
append_to_para(221, "  5F30GM147909 (Ruth L. Kirschstein NRSA individual predoctoral MD/PhD fellowship; ended 31 May 2026)")
append_to_para(223, "  Gregory John Schwing (fellow, PI of record)        504-994-0403")
append_to_para(224, "  None")
append_to_para(229, "  Wayne State University Grid high-performance computing (compute and storage allocation); no other sponsor")
# Resources follow-ups
append_to_para(242, "  Yes. (i) VinDr-SpineXR radiographs were obtained under the PhysioNet Restricted Health Data Use Agreement 1.5.0 "
                    "(research use only) and were used to train evaluation fold models only. (ii) The research prototype's training data "
                    "carry non-commercial licences: CTSpinoPelvic1K inherits CC BY-NC-SA 4.0 from CTSpine1K; COBRA2026 CC BY-NC 4.0; DeepFluoro "
                    "CC BY-NC-SA 4.0; Ljubljana CC BY-NC-ND; VerSe share-alike; permissive: C-ArmLSpine CC BY 4.0, TCIA CT Colonography, "
                    "NHANES II (public domain), TotalSegmentator dataset CC BY 4.0. Any commercial model must be retrained from commercially "
                    "licensed data; the research weights are not the commercial asset. Copies of the PhysioNet agreement and the licences "
                    "can be attached.")
append_to_para(248, "  Yes: the lead inventor is a salaried resident physician of the Detroit Medical Center (Tenet Healthcare Corporation), "
                    "Department of Surgery, from 1 July 2026 under a Graduate Medical Education Agreement (the earliest work, April-June 2026, "
                    "preceded that appointment, during the final months of medical school and the F30 fellowship). The agreement carries no "
                    "invention-assignment clause.")
append_to_para(250, "  WSU Grid high-performance computing (GPU and CPU allocations, CephFS storage), WSU library access, faculty sponsorship "
                    "(Department of Computer Science). The inventor performed all of the work himself; WSU's contribution was compute and storage on "
                    "the Grid. No WSU salary support; no TDI/MTRAC funding.")
# Submitter 1 (paragraphs 352-360)
replace_label_text(352, "Name                                                                                     Citizenship:                            ",
                   "Name  Gregory John Schwing                                    Citizenship: United States (born in the U.S.)   ")
append_to_para(353, "  not applicable (U.S. citizen)")
replace_label_text(355, "Job Title or", "Job Title or  Resident physician, General Surgery (Detroit Medical Center / Wayne State University School of Medicine)")
replace_label_text(356, "Student Status                                                                    ", "Student Status  Resident physician (WSU School of Medicine affiliate; employed by DMC)     ")
replace_label_text(356, "Degree                ", "Degree  MD, PhD (Wayne State University, May 2026)")
replace_label_text(357, "Department                                                                        ", "Department  Surgery                                   ")
replace_label_text(357, "College/Division          ", "College/Division  School of Medicine")
replace_label_text(358, "WSU Address                                                                      ", "WSU Address  Department of Surgery, Wayne State University School of Medicine, Detroit, MI 48201  ")
replace_label_text(358, "Phone                 ", "Phone  504-994-0403")
replace_label_text(359, "Home Address                                                                    ", "Home Address  206 Josephine Ave, Royal Oak, MI 48067-2217, United States  ")
replace_label_text(359, "Phone                 ", "Phone  504-994-0403")
replace_label_text(360, "E-mail ", "E-mail  gregory.schwing@med.wayne.edu   ")

# ================================================================= 2. table fills
TITLE = ("Automated detection of transitional vertebral anatomy for wrong-level spine surgery prevention: (A) a segmenter-agnostic "
         "classifier that flags transitional vertebrae on preoperative CT, and (B) a neural network that names vertebral levels from a "
         "single intraoperative C-arm exposure without registration to a preoperative scan")
set_cell(1, 0, 0, [TITLE])

set_cell(2, 1, 0, ["Gregory John Schwing, MD, PhD"])
set_cell(2, 1, 1, ["Conceived both parts; designed and trained the networks; built the training corpus (rendered CT + real C-arm frames), "
                   "the per-device image-formation models, the evaluation protocol and the software; sole inventor."])
set_cell(3, 1, 0, ["None. The sole inventor is the WSU-affiliated submitter above; co-authors of the related papers contributed data annotation, "
                   "manuscript review or mentorship, not to the inventive concept."])

mark(4, 0, True)
set_cell(4, 1, 1, ["Detroit Medical Center (employer of record: Detroit Education and Research; Tenet Healthcare Corporation): the inventor is a "
                   "resident physician in the Department of Surgery under a Graduate Medical Education Agreement (effective 1 July 2026). "
                   "That agreement contains no intellectual-property or invention-assignment clause; its section 10 is a confidentiality "
                   "clause covering the agreement's terms and proprietary information provided by the employer. No DMC resource, data or "
                   "patient information was used for the invention."])
set_cell_raw(4, 2, 1, run("100 ", RPR_LINE))
set_cell_raw(4, 2, 3, run("0 ", RPR_LINE))

set_cell(5, 0, 0, [
 "Problem. Wrong-level spine surgery is a never event whose largest anatomic driver is a transitional vertebra (a sixth lumbar vertebra, "
 "a thirteenth thoracic vertebra, or a fifth lumbar vertebra fused to the sacrum; 5-35 % of people). Planning is done on lumbar-only CT "
 "without a count from C2, and intraoperative confirmation is counting vertebral bodies on fluoroscopy; both fail on transitional spines, "
 "and registration-based aids (LevelCheck-type systems) project the labels of the preoperative read and inherit its counting error. "
 "Current CT segmenters (TotalSegmentator, SPINEPS) shift the lumbar labels one level on such spines without warning.",
 "Part A -- preoperative CT flag (near-term product). A classifier that takes the output of ANY CT segmenter, discards the segmenter's level "
 "names, and computes name-free per-vertebra features (rib presence traced in the CT image, rib-free body count above the sacral plateau, "
 "transverse-process-to-sacral-ala contact area, disc and end-plate geometry, iliac crest line), then flags the transitional phenotype "
 "(L6, sacralised L5 by Castellvi grade, T13, lumbar rib, four lumbar) with a plain-language reason, an abstention when the junction is "
 "outside the field of view, and an 'unusual spine' score.",
 "Part B -- intraoperative level naming. A convolutional-recurrent network reads a single C-arm exposure, detects the vertebral bodies and "
 "the sacrum, and names each level from LOCAL MORPHOLOGY rather than from a count, so a transitional vertebra is recognised as what it is; "
 "the classifier is coupled with a count from the detected sacrum through a set of candidate vertebral sequences ('alphabets', ordinary "
 "and transitional) and abstains visibly when they disagree. No registration, fiducials or navigation hardware. It is trained on "
 "digitally reconstructed radiographs rendered from labelled CT through per-device image-formation models (fitted physics parameters per "
 "C-arm model; free geometric labels by projection, including the bicoxofemoral point) plus few real frames per device. Measured: on a "
 "C-arm never seen in training it named 96.4 % of detected lateral vertebrae zero-shot (595 of 617) and 97.4 % after case-grouped "
 "fine-tuning; in its feature space a sixth lumbar vertebra separates from the fifth more than the fifth from the fourth (silhouette 0.35 "
 "vs 0.23).",
 "Novel or unexpected: level identity learned from local morphology instead of counting or registration; the alphabet coupling with "
 "visible abstention; per-device image-formation models that let one network serve several C-arms from renders with few real frames; a "
 "segmenter-agnostic, name-free CT flag. Unexpected: naming accuracy on an unseen C-arm "
 "reached its plateau before any real frame of that device was used for training -- the limit is coverage of acquisition geometry, not "
 "the number of real images.",
])
set_cell(6, 0, 0, ["Combination: new processes/methods (name-free transitional-phenotype classification from segmentations; level "
                   "naming from local morphology coupled with a count and abstention; render-based per-device training) embodied in "
                   "software (trained neural-network weights, training and inference code, per-device image-formation parameters)."])
set_cell(7, 0, 0, ["Improvement of existing processes: preoperative CT planning (a flag on the planning scan) and intraoperative "
                   "fluoroscopic level confirmation. New use of any vendor's CT segmenter output as the input of a transitional-anatomy flag."])
set_cell(8, 0, 0, ["(A) Software as a medical device that flags suspected transitional anatomy on preoperative CT and notifies the reader -- "
                   "radiology/PACS workflow, Class II 510(k) anticipated (product codes QIH/MYN), the near-term product. (B) Intraoperative "
                   "level confirmation on the C-arm exposure -- decision support beside the surgeon's count, integrated with C-arm consoles "
                   "or navigation platforms (harder regulatory path; later). (C) Licensable assets: per-device image-formation parameters, "
                   "the evaluation protocol and reference standard, trained weights retrained on commercially licensed data."])
set_cell(9, 0, 0, ["Part A (name-free transitional-phenotype classifier on CT segmentations): the CT-side count-anomaly work began spring 2026; the "
                   "name-free, segmenter-agnostic classifier as claimed was designed on 24-25 September 2026. Part B (level naming from local morphology on a "
                   "single C-arm exposure): 24 August 2026; the alphabet coupling and abstention: September 2026; per-device image-"
                   "formation models: 21-23 September 2026."])
set_cell(10, 0, 0, ["Version-controlled repositories with dated commits: spinesurg-ct-nnunet (private, GitHub: Part B, the CT classifier, "
                    "training and evaluation pipelines), CTSpinoPelvic1K (public) and OpenSpineToolkit (public); the WSU Grid high-performance "
                    "computing account (job records, trained checkpoints, model registry, results under /rs/rs_grp_oschome/go2432); Zenodo "
                    "deposits of the dataset (concept DOI 10.5281/zenodo.22139642); the inventor's dated laboratory journal (PDF); the "
                    "manuscripts in preparation with their result ledgers."])
set_cell(11, 0, 0, ["Functioning research prototypes: trained weights exist for Part B and are evaluated on public intraoperative datasets "
                    "(C-ArmLSpine C-arm frames with cone-beam CT truth; COBRA2026 kV frames) and on rendered CT; Part A's feature extractor "
                    "runs on 3,500 CT-segmenter pairs and its classifier is in training; a manuscript on Part B is in preparation; no "
                    "prospective or clinical evaluation; no regulatory submission. The prototypes are trained on non-commercially licensed "
                    "research data (see Resources); a commercial model must be rebuilt from commercially licensed data."])

set_cell(12, 0, 0, ["Every spine operation confirms its level under fluoroscopy and is planned on CT or MRI; over one million spine "
                    "procedures are performed each year in the United States. Wrong-level surgery is a reportable never event (half of "
                    "responding spine surgeons report having performed one; registry rate about 0.1 %, higher in the thoracic spine), and "
                    "transitional vertebrae (5-35 % prevalence) are its largest anatomic cause. Customers: radiology groups and PACS/AI "
                    "platform vendors (Part A); hospitals and ambulatory surgery centres, C-arm and navigation manufacturers (Part B). Unmet "
                    "need: a check that does not fail on exactly the anatomy that causes the error, works on the limited fields of view "
                    "actually acquired, and needs no registered preoperative scan."])
set_cell(13, 0, 0, ["Manual counting on fluoroscopy with a marker and a check film; intraoperative navigation (registration of the "
                    "preoperative CT/CBCT to the patient; hardware, fiducials, time); LevelCheck-type research systems (Johns Hopkins) that "
                    "register the preoperative scan and project its labels -- accurate on ordinary spines, dependent on the planning read; "
                    "CT segmenters and vendor spine-labelling tools (TotalSegmentator/3D Slicer, MSKai-type products) that mislabel "
                    "transitional spines by one level without warning. No product today flags a transitional vertebra on the planning CT "
                    "or names one from a single C-arm exposure."])
set_cell(14, 0, 0, ["Medtronic (StealthStation, Mazor), Globus Medical (ExcelsiusGPS), Stryker, Brainlab, Siemens Healthineers (Cios), GE "
                    "HealthCare (OEC), Ziehm Imaging, Philips; radiology AI platforms (Aidoc, Viz.ai, Avicenna CINA, Nuance/Microsoft); "
                    "open-source segmenters (TotalSegmentator/3D Slicer, SPINEPS)."])
set_cell(15, 0, 0, ["Built for the transitional anatomy on which counting, registration and current segmenters fail; segmenter-agnostic and "
                    "name-free, so it audits any vendor's output without retraining it; registration-free intraoperative naming from one "
                    "exposure with visible abstention; one network serves several C-arm models through per-device image-formation "
                    "parameters, so adapting to a new device needs few real frames; every call carries a plain-language reason."])
set_cell(16, 0, 0, ["No commercial interest has been solicited or received to date."])
set_cell(17, 0, 0, ["Interested in forming a company to commercialise the technology; none formed."])

mark(18, 0, True)
set_cell(18, 1, 1, [
 "Partial. Neither the name-free CT classifier (Part A as claimed) nor Part B (level naming from a single C-arm exposure by local "
 "morphology, the alphabet coupling, the per-device image-formation models) has been publicly disclosed; Part B's manuscript is in "
 "preparation. Disclosed so far, all research-track:",
 "(a) 'Not All Spines Are Created Equal: How CT Segmenters Fail on Lumbosacral Transitional Vertebrae', NeurIPS 2026 Evaluations and "
 "Datasets Track, submission 3474, accepted 24 Sep 2026 (OpenReview D8yRWDAGQF, public): the TotalSegmentator one-level label shift on "
 "transitional spines, the dataset, and a merge-based CT segmenter released with weights (transitional-aware oversampling is used there).",
 "(b) Abstracts accepted to the 2026 Congress of Neurological Surgeons annual meeting (Washington, DC), including the single-shot CT "
 "detection of count anomalies ('Not All Spines Are Created Equal', mini-oral, scheduled 2 November 2026; slides not yet submitted; "
 "accepted abstracts are published in the meeting's abstract supplement).",
 "(c) 'Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection', Tech Fair presentation and "
 "hands-on demonstration, 43rd AACA annual meeting, Mayo Clinic, Rochester MN, Saturday 13 June 2026 (slides attached): a separate, "
 "earlier project -- an LSTV screening pipeline assembled from third-party open-source segmenters (TotalSpineSeg, SPINEPS/VERIDAH) whose "
 "level disagreement flags the phenotype, with Castellvi heuristics -- released as open source. It is listed for completeness; it does "
 "not disclose Part A's name-free classifier or Part B, neither of which existed then, and neither claim relies on that mechanism.",
 "(d) CTSpinoPelvic1K dataset: public Zenodo releases (v10 on 7 Sep 2026, v11 on 18 Sep 2026); arXiv preprint 2609.22760 (19 Sep 2026) of a "
 "dataset article under review at Medical Physics -- the CT resource and its label scheme, not a method.",
 "(e) openspineconsortium.com: public website with a spinopelvic-measurement demonstration and the open OpenSpineToolkit; neither the "
 "CT classifier nor the level-naming network is served there.",
])
set_cell(18, 2, 1, ["Planned: (1) the Part B manuscript (Radiology: Artificial Intelligence) is complete and is being HELD from submission until this "
                    "office advises -- it is the first disclosure of Part B (a copy accompanies this form); (2) the NeurIPS 2026 camera-ready will be "
                    "published in the proceedings about one month before the December conference (~November 2026) -- dataset and segmenter audit, "
                    "as in (a); (3) CNS 2026 mini-oral, 2 November 2026, CT-side count anomalies; (4) the dataset article (Medical Physics) is "
                    "being submitted -- dataset only, no method of this disclosure."])
mark(19, 0, True)
set_cell(19, 1, 1, ["The NeurIPS 2026 paper released its CT segmenter code and weights under an open licence (public GitHub "
                    "OpenSpineConsortium/spinopelvic-seg; Hugging Face) -- that segmenter is not the claimed invention. For Part A's "
                    "classifier and Part B's network no open-source release of weights is planned before the office's assessment; the journal "
                    "targeted (Radiology: AI) expects code availability, which can be met with a gated or on-request release."])
mark(20, 0, True); mark(20, 1, True); mark(20, 2, True); mark(20, 3, True)
set_cell(20, 4, 1, ["Draft: the Part B manuscript, unsubmitted. Submitted: the dataset article (Medical Physics, under review; dataset "
                    "only). Accepted: the NeurIPS 2026 E&D paper (24 Sep 2026). Published: the arXiv preprint of the dataset article (19 Sep "
                    "2026); conference abstracts as listed above."])
mark(21, 0, False)
set_cell(21, 1, 1, ["None planned before assessment."])
mark(21, 2, False)
set_cell(21, 3, 1, ["Not offered for sale, sold or used publicly."])
mark(22, 0, True)
mark(23, 0, True)
mark(24, 0, True)
set_cell(27, 0, 0, ["Gregory John Schwing (sole inventor)"])
set_cell_raw(27, 0, 1, run("100", RPR_LINE))

DOC.write_text(x, encoding="utf-8")
print("filled; document.xml", len(x), "chars")
