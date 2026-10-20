# Invention disclosure package — Gregory J. Schwing, MD, PhD — 25 September 2026

To: Wayne State University Office for Technology Commercialization (inventiondisclosures@wayne.edu)
From: Gregory John Schwing, MD, PhD — Resident physician, Department of Surgery, Detroit Medical Center / Wayne State University School of Medicine — gregory.schwing@med.wayne.edu — 504-994-0403

Title of the disclosure: **Automated detection of transitional vertebral anatomy for wrong-level spine surgery prevention:
(A) a segmenter-agnostic classifier that flags transitional vertebrae on preoperative CT, and (B) a neural network that names
vertebral levels from a single intraoperative C-arm exposure without registration to a preoperative scan.**

Sole inventor. Federal support: NIH/NIGMS F30GM147909 (individual predoctoral fellowship; ended 31 May 2026; the earliest
work, April–May 2026, fell inside it). No industrial sponsor. WSU resources: Grid high-performance computing (compute and
storage). Employer: Detroit Medical Center (Graduate Medical Education Agreement, no intellectual-property clause).

## Contents

| # | File | What it is | Status |
|---|---|---|---|
| 01 | `01_WSU_Invention_Disclosure_Form.docx` | The completed disclosure form (blue entries), MOU and royalty pages unsigned | for signature |
| 02 | `02_CONFIDENTIAL_Part_B_manuscript_Radiology_AI.pdf` | **Unpublished** manuscript describing Part B (the C-arm level-naming network) with its supplement; intended for Radiology: Artificial Intelligence; **held from submission pending your advice** — this is the first disclosure of Part B | confidential, unpublished |
| 03 | `03_NeurIPS2026_camera_ready_Not_All_Spines.pdf` | Accepted paper, NeurIPS 2026 Evaluations & Datasets Track (poster): audit of TotalSegmentator's one-level label shift on transitional spines; the CTSpinoPelvic1K dataset; a merge-based CT segmenter released with weights. Discloses the CT-side finding and the dataset, not Part A's name-free classifier nor Part B | accepted 24 Sep 2026; OpenReview public; proceedings ~November 2026 |
| 04 | `04_MDPA_dataset_article_main.pdf`, `04_MDPA_dataset_article_supporting_information.pdf` | Dataset article on CTSpinoPelvic1K for Medical Physics (dataset and label scheme only; no method of this disclosure) | preprint public on arXiv (2609.22760, 19 Sep 2026); journal submission in progress |
| 05 | `05_AACA_TechFair_2026-06-13_slides.pptx` | Slides of the Tech Fair presentation, 43rd AACA annual meeting, Mayo Clinic, Rochester MN, Saturday 13 June 2026: a separate, earlier LSTV screening pipeline assembled from third-party open-source segmenters (TotalSpineSeg, SPINEPS/VERIDAH) whose level disagreement flags the phenotype; listed for completeness; discloses neither Part A nor Part B, and neither claim relies on it | presented publicly 13 Jun 2026 |
| 06 | `06_disclosure_timeline.md` | Dated list of every public disclosure and planned disclosure relevant to grace periods | — |

## What has not been disclosed

- Part B in full: level naming from local morphology on a single C-arm exposure, the coupling of the morphology classifier
  with a count from the detected sacrum through candidate vertebral sequences with visible abstention, and the per-device
  image-formation models that let one network serve several C-arms from rendered CT with few real frames.
- Part A as claimed: the segmenter-agnostic, name-free per-vertebra feature classifier with plain-language reasons.

## Timing that matters

- The Part B manuscript (item 02) is complete; it will be submitted only after this office advises. Publication before a
  provisional filing would start the U.S. grace period on Part B and forfeit absolute-novelty jurisdictions.
- Public dates already on record: AACA Tech Fair 13 Jun 2026; Zenodo dataset v10 7 Sep 2026 and v11 18 Sep 2026; arXiv
  2609.22760 19 Sep 2026; NeurIPS acceptance 24 Sep 2026 (OpenReview page public). Upcoming: NeurIPS proceedings
  (~November 2026); CNS 2026 mini-oral 2 November 2026 (CT-side count anomalies; slides not yet submitted).

## Data-licence note for any commercial plan

The research prototypes were trained on datasets carrying non-commercial licences (CTSpinoPelvic1K inherits CC BY-NC-SA 4.0
from CTSpine1K; VinDr-SpineXR under a PhysioNet data use agreement; COBRA2026 CC BY-NC 4.0; DeepFluoro CC BY-NC-SA 4.0).
A commercial model must be retrained on commercially licensed data; the methods, the device image-formation approach and
the evaluation protocol — not the research weights — are the assets.
