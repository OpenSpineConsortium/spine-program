# Human Participant Research determination — VinDr-SpineXR (draft for submission)

Drafted 2026-09-24. This is the separate submission that determination 2026-269 promised for any dataset
governed by a data use agreement. It is written to be pasted into the WSU "Human Participant Research
Determination Tool" (form 11/2021 HP) and e-mailed to IRBQuestions@wayne.edu with the attachments listed at
the end. Text marked `[FILL: ...]` must be completed by Greg before sending. Everything else is ready to paste.

Where an answer is unchanged from the tool filed 08/28/2026 (determination 2026-269), it is reused verbatim
and marked "(as filed on 2026-269)". Where the answer is specific to VinDr-SpineXR it is new.

---

## Part 1 — Cover note to the IRB Administration Office

To: IRBQuestions@wayne.edu
From: Gregory Schwing, Resident, General Surgery, DMC/WSU (go2432@wayne.edu)
Subject: HPR determination request — one dataset obtained under a data use agreement (follow-up to 2026-269)

Dear IRB Administration Office,

On 2 September 2026 your office issued a Notice of IRB Administrative Determination (WSU IRB HPR Number
2026-269) that the project "Open Spine Consortium: Secondary Analysis of Publicly Available, De-Identified
Imaging Datasets and the Derived Annotations, Software, and Models Produced From Them" does not constitute
human participant research under 45 CFR 46 or the FDA regulations.

The tool I submitted for that determination limited its scope, in item 7, to datasets meeting five criteria.
Criterion 2 read:

> "(2) it can be downloaded by any member of the public without an application, request for permission,
> eligibility review, or data use agreement;"

and the same item stated:

> "If a dataset does NOT meet all five criteria -- in particular if it is restricted-use, requires a
> proposal or application to obtain, or is governed by a data use agreement -- it falls outside this
> determination and a separate IRB submission will be made before that dataset is used."

This is that separate submission. It covers ONE dataset:

**VinDr-SpineXR** (version 1.0.0), a de-identified collection of 10,466 spine radiographs from 5,000
studies, deposited on PhysioNet by its authors (Pham HH, Nguyen Trung H, Nguyen HQ, 2021;
https://doi.org/10.13026/q45h-5h59) and served under the "PhysioNet Restricted Health Data License 1.5.0"
and the corresponding "PhysioNet Restricted Health Data Use Agreement 1.5.0". PhysioNet's access policy for
this dataset reads: "Only registered users who sign the specified data use agreement can access the files."

The facts I ask the office to weigh are these.

1. **The data are de-identified by the depositor before release.** The depositors state that DICOM
   de-identification proceeded in three steps — "(1) removing protected health information in DICOM tags,
   (2) removing patient information in the pixel data of the image, and (3) revising" — that "all the scans
   were examined manually to spot DICOM images that have textual information", and that "de-identified images
   were manually reviewed to ensure that patient information was removed correctly." The depositors' own
   study "was approved by the Institutional Review Board of Hospital 108 (H108) and Hanoi Medical University
   Hospital (HMUH)", and "the patient informed consent was waived since this study did not impact the
   clinical care of these hospitals, and patient-identifiable information has been removed from the data."
   The depositors state that "these scans were created in the period from 2011 to 2020"; the investigators
   have no relationship with either hospital.

2. **No re-identification or contact is possible.** The investigators receive no key, code, or linkage. The
   release carries no name, date of birth, medical record number or free-text field; the only per-image
   attributes are the DICOM study and image identifiers assigned by the depositors and the lesion
   annotations they released.

3. **The data use agreement's restrictions are honoured.** The licence binds the individual account holder
   to use the data "for the sole purpose of lawful use in scientific research and no other", not to "attempt
   to identify any individual or institution referenced in PhysioNet restricted data", not to "share access
   to PhysioNet restricted data with anyone else", and to report any identifying information found to
   PHI-report@physionet.org. In this project the files reside only on WSU-managed computing resources under
   the account holder's own storage; no VinDr-SpineXR image, crop or derived frame is redistributed, mirrored
   or included in any released dataset (the released code rebuilds derived frames locally from a user's own
   PhysioNet download); no re-identification is attempted; and no external data are linked to it.

4. **The dataset has already been downloaded and used, and I disclose that plainly.** The files were
   downloaded from PhysioNet to the WSU High Performance Computing Grid on 7 September 2026 — after the
   determination tool was completed (28 August 2026) and after determination 2026-269 was issued
   (2 September 2026) — and 2,071 of its 10,466 films were used, in cropped form, as pseudo-labelled training
   data for a subset of the machine-learning models (the "fold models" of one cross-validation experiment)
   in a manuscript now under preparation. No VinDr-SpineXR image was used for testing, reporting of
   per-dataset accuracy, or any figure. The separate submission promised in item 7 of the 2026-269 tool
   should have preceded that use and did not. I am submitting it now, and I ask the office to determine
   whether this secondary analysis of a de-identified, agreement-governed dataset is human participant
   research. If the office determines that it is, the models trained on it will be withdrawn from the
   manuscript and retrained without it, and I will follow whatever further instruction the office gives.

The completed determination tool follows (Part 2), with the five criteria from the 2026-269 tool answered
one by one for this dataset. Attached are the PhysioNet project page, the licence and data use agreement
text, the depositors' de-identification statement, the 2026-269 memo and the tool as filed.

Sincerely,

Gregory Schwing, MD, PhD
Resident, Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center
Faculty sponsor: Loren Schwiebert, PhD, Professor, Department of Computer Science

---

## Part 2 — Determination Tool answers

### Section A: Project Staff and Location Information

| Field | Answer |
|---|---|
| Project Title | Open Spine Consortium: Secondary Analysis of a De-Identified Radiograph Dataset (VinDr-SpineXR) Obtained Under the PhysioNet Restricted Health Data Use Agreement — supplement to HPR 2026-269 |
| Name of person conducting the project | Gregory Schwing (as filed on 2026-269) |
| Title | Resident-General Surgery, DMC/WSU (as filed on 2026-269) |
| Date | `[FILL: date of submission]` |
| Email Address | go2432@wayne.edu (as filed on 2026-269) |
| Phone | [phone withheld] (as filed on 2026-269) |
| Status | Resident/Fellow/Trainee (as filed on 2026-269) |
| Division or College / Department | `[FILL: as filed on 2026-269 the form reads Division "Engineering", Department "Computer Science" (the faculty sponsor's unit); confirm this is what the office wants repeated, or give School of Medicine / Department of Surgery]` |
| Campus Address | 5057 Woodward Ave, Detroit, MI 48202 (as filed on 2026-269) |
| Faculty Sponsor/Supervisor | Loren Schwiebert, Professor, Department of Computer Science (as filed on 2026-269; the filed form's Title field is cut off after "Professor, Department of", and the sponsor's phone field was left blank) |
| Form completed by | Gregory Schwing, go2432@wayne.edu |
| Check all that apply | Medical study (as filed on 2026-269) |

### Section B: Location and Study Data Details

**1. Describe the location(s) where activities will take place.**

(as filed on 2026-269, with one addition)

All activities are computational and take place at Wayne State University. No activity occurs at a clinical
site, and no participant is contacted, recruited, observed, or enrolled at any location.

Data are downloaded over the internet from public archives to WSU-managed computing resources, including the
WSU High Performance Computing Grid and WSU-managed workstations. Analysis, annotation, model training, and
manuscript preparation are performed on those resources. Derived annotations and software are published to
public repositories (e.g. Zenodo, GitHub, Hugging Face) under open licences.

Addition for this dataset: the VinDr-SpineXR files are held only on the WSU High Performance Computing Grid
under the storage of the PhysioNet account holder named in Part 3. Under the data use agreement they are not
copied to any public repository, not shared with any person outside the agreement, and no image or derived
frame from them is included in any published dataset.

**2. Select the type of data being collected.**

Secondary or retrospective data collection (existing data that was originally generated for reasons
unrelated to this project). (as filed on 2026-269)

Not checked: Identifiable Protected Health Information (PHI); Prospective Data; bio-specimens.

**3. Will you require access to, or the use of any identifiable information pertaining to participants
during the process of collecting data?**

No. (as filed on 2026-269)

**4. Will data being obtained include individually identifiable information?**

No. (as filed on 2026-269) None. No individually identifiable information is obtained, used, generated, or
retained. Datasets are de-identified by the source before public release, and the investigators receive no
key or code permitting re-identification.

For this dataset specifically: the depositors removed protected health information from the DICOM tags,
removed patient information burned into the pixel data after manual inspection of every scan, and manually
reviewed the de-identified images. The released per-image fields are the depositors' own study and image
identifiers and their lesion annotations.

**5. Could the identities of participants be known to, or be readily ascertained by the investigators?**

No. (as filed on 2026-269) The images were acquired at Hospital 108 (H108) and Hanoi Medical University
Hospital (HMUH), according to the depositors; the investigators have no relationship with either institution,
no access to their records, and no linkage of any kind.

**6. Select the source of data collection.**

Data Repository; Other. Describe: PhysioNet (physionet.org), a research data repository operated by the MIT
Laboratory for Computational Physiology, serving the dataset VinDr-SpineXR v1.0.0 under the PhysioNet
Restricted Health Data License 1.5.0 to registered users who sign the PhysioNet Restricted Health Data Use
Agreement 1.5.0. This differs from the sources covered by 2026-269, which were described there as "Public
data archives that release de-identified imaging under open licences without application or data use
agreement".

**6a. Institution(s) (Covered Entity) you will be reviewing and collecting medical record data from.**

N/A — Project does not involve the review of or collection of data from a medical record. (box as filed on
2026-269; the Describe text below is adapted from the filed "All imaging is obtained from public archives that
de-identified it before public release.") No medical records at any covered entity are accessed. All imaging
is obtained from the repository, which received it already de-identified from the depositors.

**7. Describe how the data will be obtained.**

By direct download from PhysioNet, after registering an individual PhysioNet account and accepting the
PhysioNet Restricted Health Data Use Agreement 1.5.0 online. No data are collected from participants, and no
records at any covered entity are accessed.

The dataset was downloaded on 7 September 2026 by the account holder named in Part 3. The download was
verified against the depositors' published SHA-256 checksums (10,466 images, 0 mismatches).

The five criteria stated in item 7 of the 2026-269 tool, applied to this dataset:

| # | Criterion in the 2026-269 tool | VinDr-SpineXR | Met? |
|---|---|---|---|
| 1 | "the dataset is already publicly available and was de-identified by the source before public release" | Publicly listed on PhysioNet since 24 August 2021 with a DOI; de-identified by the depositors before deposit (DICOM tags, pixel data, manual review — their statement is attached). | Yes |
| 2 | "it can be downloaded by any member of the public without an application, request for permission, eligibility review, or data use agreement" | Any member of the public may register a PhysioNet account, but download requires accepting the PhysioNet Restricted Health Data Use Agreement 1.5.0. PhysioNet's "restricted access" tier is defined as "Accessible by registered users who sign a Data Use Agreement"; it does not require the credentialing process or the CITI training that PhysioNet's "credentialed access" tier requires. There is no application, proposal, or eligibility review. | **No — a data use agreement is involved. This is why the dataset is outside 2026-269 and why this submission is made.** |
| 3 | "it is not designated restricted-use by the source" | The source names its licence the "Restricted Health Data License" and its access tier "restricted access". The restriction consists of the agreement's terms (research use only, no re-identification, no sharing), not of an eligibility review. Stated plainly so the office can weigh it. | **No, by the source's own word** |
| 4 | "the investigators receive no key, code, or other means of re-identification, and hold no relationship with the source enabling re-identification" | No key or code is provided; the investigators have no relationship with PhysioNet beyond the account, nor with Hospital 108 or Hanoi Medical University Hospital. | Yes |
| 5 | "no attempt is made to re-identify any individual, and no external data are linked to the dataset for the purpose of, or with the effect of, re-identification" | No re-identification is attempted; the agreement forbids it; no external data are linked. The only use is as training images for a vertebra-naming model. | Yes |

### Section C: Description of the Project

**8. Describe the purpose of this project.**

(first two paragraphs as filed on 2026-269)

The Open Spine Consortium develops open, reproducible methods for analysing spinal and pelvic anatomy on
computed tomography and radiographs. Its projects share one design: existing, publicly released,
de-identified imaging is re-analysed to produce annotations, measurements, software, and machine-learning
models, which are then released openly for others to use and check.

The clinical problem motivating this work is that vertebral level is conventionally established by counting
down from C2. An abdominal CT does not contain C2, so at the thoracolumbar junction a transitional vertebra,
a rib borne by a lumbar vertebra, and a stump rib produce overlapping appearances, and the correct label
depends on a count the field of view cannot support. Mislabelling a level has direct consequences for
surgical planning. These datasets and tools are built to make that determination reproducible, and to state
plainly where it cannot be made.

The purpose of THIS determination is narrower than 2026-269. It asks whether the secondary analysis of one
additional de-identified dataset, VinDr-SpineXR, which is governed by a data use agreement and therefore
falls outside the scope 2026-269 defined for itself, constitutes human participant research. The dataset's
role in the project is as additional training images of the lumbar and thoracic spine on plain radiographs
for a model that names vertebral levels on intraoperative C-arm images.

**9. Describe the objectives or aims for the project.**

(as filed on 2026-269)

Across current and planned Open Spine Consortium projects:

1. Produce and openly release expert-reviewed anatomical annotations of existing public imaging datasets
   (vertebrae by level, sacrum, pelvis, femurs, ribs by level, and surgical instrumentation where present).
2. Characterise anatomical variation in these cohorts, particularly lumbosacral transitional anatomy and its
   effect on vertebral level assignment.
3. Develop, train, and evaluate segmentation and measurement algorithms on those annotations, and release the
   software and trained models under open licences.
4. Compute spinopelvic parameters (pelvic incidence, pelvic tilt, sacral slope and related measures)
   reproducibly from segmentations, and evaluate agreement against established methods.
5. Report methods and results in peer-reviewed publications, with the underlying annotations and code
   archived publicly so results can be independently reproduced.

No objective requires the identity of any individual, and none is served by knowing it.

For this dataset, objective 3 is the only one engaged: VinDr-SpineXR images serve as training data. No
annotation of VinDr-SpineXR is released (the vertebral levels assigned to its images were generated
automatically and are not distributed), and no VinDr-SpineXR image appears in any released dataset, figure
or accuracy table.

**10. Describe how the results will be used/applied.**

(as filed on 2026-269)

Results are used to advance scientific and clinical understanding of spinal anatomy and its measurement, and
are disseminated as:
- peer-reviewed journal articles and conference papers;
- openly licensed datasets of derived annotations, archived with a DOI;
- open-source software and trained models;
- educational and reference material for clinicians and researchers.

Findings are not applied to the care of any individual whose images appear in these datasets. No individual
is contacted, and no result is returned to any individual, because no individual can be identified from the
data.

Software released by the consortium is provided for research use only and is not offered for clinical
diagnosis or treatment. Should the consortium later seek FDA clearance for any device, data supporting that
application would fall under question 3.4 of this tool and a separate determination would be obtained
beforehand.

Addition for this dataset: the PhysioNet licence also requires the licensee "to contribute code associated
with publications arising from this data to a repository that is open to the research community"; the
project's code is released under an open licence, which satisfies this. Trained model weights that learned
from VinDr-SpineXR images do not contain, and cannot reproduce, any source image.

**11. Describe the participants for the project.**

(first two paragraphs as filed on 2026-269; the filed tool's third and fourth paragraphs, on per-study
technical and demographic attributes and on the 802-record CT scale, are replaced by the dataset-specific
paragraph below)

There are no participants in this project as the term is used in 45 CFR 46.

The project analyses imaging studies that were acquired previously, for clinical or research purposes
unrelated to this work, and that were de-identified and released publicly by their source archives before
the investigators obtained them. The investigators have no contact of any kind with the individuals whose
images these were, have no means of identifying them, and receive no key or code that would permit
re-identification.

For this dataset: VinDr-SpineXR comprises 10,466 spine radiographs from 5,000 studies (4,000 training studies
with 8,389 images; 1,000 test studies with 2,077 images), collected retrospectively by the depositors at
Hospital 108 and Hanoi Medical University Hospital over the period 2011 to 2020, under those hospitals' IRB
approval with a waiver of informed consent, de-identified, and deposited on PhysioNet in 2021.
The per-image information available to the investigators is the image itself, the depositors' study and
image identifiers, and their lesion annotations. Of the 10,466 images, 2,071 were used in this project.

### Section D: Determination Tool

**Step 1 — Research (45 CFR 46).**
1.1 checked; both sub-boxes checked; 1.2 checked. (as filed on 2026-269) The project meets the regulatory
definition of research.

**Step 2 — Human participants (45 CFR 46).**
2.1 Does the research involve collecting data through intervention or interaction with the individuals? —
**No.** (as filed on 2026-269)
2.2 Will you obtain, use, study, analyze, or generate identifiable private information or identifiable
bio-specimens from individuals? — **No.** (as filed on 2026-269) The data use agreement governs the terms
of use; it does not supply any identifier, key or linkage, and the identity of no individual is or can be
readily ascertained by the investigators.

**Step 3 — FDA (21 CFR 50).**
3.1, 3.2, 3.3, 3.4 — none checked. (as filed on 2026-269)

**Requested WSU IRB Determination.** The investigator's own reading, submitted for the office's concurrence
or correction: Not Human Participant Research, category "De-Identified Private Information and/or Human
Biological Specimens" — the category under which 2026-269 was issued. The investigator notes that the form's
"Public Use Datasets" category carries the note "IRB approval is required for the use of restricted use
data, if a proposal is required to obtain the dataset, or if a data use agreement is involved", and that this
dataset involves a data use agreement and is named "restricted" by its source; this submission exists so that
the office, not the investigator, decides which category and which note govern.

---

## Part 3 — The PhysioNet account holder

The PhysioNet Restricted Health Data License binds "the LICENSEE", the individual registered user who accepted
it; it cannot be accepted on behalf of a group. The office should be told who that individual is, and that
person's name should match the person conducting the project or be explained.

| Item | Value |
|---|---|
| Name of the registered PhysioNet account holder who accepted the Restricted Health Data Use Agreement 1.5.0 for VinDr-SpineXR | `[FILL: full name]` |
| PhysioNet username | `[FILL]` |
| Date the agreement was accepted (visible in the PhysioNet account's "Data Use Agreements" page) | `[FILL: date]` |
| Date of download to the WSU HPC Grid | 7 September 2026 (file creation time of `LICENSE.txt` and `SHA256SUMS.txt` in the downloaded tree; the download-complete marker is dated 10 September 2026) |
| CITI "Data or Specimens Only Research" training | `[FILL: completed on ... / not completed]` — note: PhysioNet does not require credentialing or CITI training for its restricted-access tier, only for its credentialed tier; state the fact either way, because the office may ask |
| Storage location | WSU High Performance Computing Grid, the account holder's own storage; not on any shared or public location |

If the account holder is not Gregory Schwing, add a sentence to the cover note stating the relationship
(e.g. a co-investigator at WSU) and that the files have not left that person's storage.

---

## Part 4 — Manuscript Ethics sentence (to be used once the number is issued)

The manuscript's Ethics paragraph currently ends the VinDr-SpineXR clause with a placeholder. Once the office
issues a determination number, the clause reads:

> VinDr-SpineXR was obtained under its PhysioNet data use agreement, which determination 2026-269 does not
> cover (it is limited to data obtainable without an application or agreement); its secondary analysis was
> separately determined by the same office not to be human participant research (determination
> `[FILL: 2026-NNN]`, `[FILL: date]`), and it trained the intraoperative fold models only (Table 1).

If instead the office determines that the analysis is human participant research, the clause is not written;
the fold models are retrained without VinDr-SpineXR and the Ethics paragraph drops the dataset (see
REVIEW2_RSNA.md Fix 2 and REVISION_LOG2.md row 77 for the two paths).

The same number goes into `SchwingNet/packet_src/statements.md` at the two `[[CONFIRM: ...]]` markers on the
VinDr-SpineXR sentences (both in the Ethics wordings, lines 57 and 61; the Data availability wordings at lines
33 and 45 name the agreement without a marker and need no number).

---

## Attachments to send with the tool

1. This cover note (Part 1) and the completed tool (Part 2), as PDF or Word — not handwritten.
2. `2026_269 Schwing IRB Not HPR Determination 9.2.26.pdf` (the memo).
3. `OSC_HPR_Determination_public_datasets.pdf` (the tool as filed 08/28/2026).
4. Printouts (PDF) of, read 2026-09-24:
   - https://physionet.org/content/vindr-spinexr/1.0.0/ (project page: access policy, de-identification and
     IRB statements, citation);
   - https://physionet.org/content/vindr-spinexr/view-license/1.0.0/ (PhysioNet Restricted Health Data
     License 1.5.0);
   - https://physionet.org/about/database/ (definition of the restricted and credentialed tiers).
5. The depositors' article, as the PhysioNet page cites it: Hieu T Nguyen, Hieu H Pham, Nghia T Nguyen,
   Ha Q Nguyen, Thang Q Huynh, Minh Dao, Van Vu. VinDr-SpineXR: A deep learning framework for spinal lesions
   detection and classification from radiographs. International Conference on Medical Image Computing and
   Computer Assisted Intervention (MICCAI), 2021.
   Dataset citation: Pham HH, Nguyen Trung H, Nguyen HQ. VinDr-SpineXR: a large annotated medical image
   dataset for spinal lesions detection and classification from radiographs (version 1.0.0). PhysioNet; 2021.
   https://doi.org/10.13026/q45h-5h59

---

## Source facts behind this draft (for the file, not for the office)

| Fact | Where it comes from |
|---|---|
| Criterion 2 wording; "falls outside this determination and a separate IRB submission will be made before that dataset is used" | `OSC_HPR_Determination_public_datasets.pdf`, Section B item 7 |
| Memo date 2 September 2026, HPR Number 2026 269, category "De-Identified Private Information and/or Human Biological Specimens", reviewer comment "analyzing de-identified data in a manner that will make it impossible to ascertain the identity" | `2026_269 Schwing IRB Not HPR Determination 9.2.26.pdf` (a 14-page scan, no text layer): memo page 1; category ticked on page 12 (tool page 11); reviewer comment and signature dated 9.2.2026 on page 13 (tool page 12); page 14 blank |
| Tool completed 08/28/2026; as-filed title "Resident-General Surgery, DMC/WSU", division "Engineering", department "Computer Science", campus address 5057 Woodward Ave, phone [phone withheld] | the memo's copy of the tool, page 3 (tool page 2). Note: the local text PDF `OSC_HPR_Determination_public_datasets.pdf` (page 2) carries an earlier draft of Section A reading Title "Resident, Department of Surgery" and Division "School of Medicine / Department of Surgery"; the filed version in the memo is the one quoted above |
| Section B ticks (2: secondary only; 3, 4, 5: No; 6: Data Repository + Other; 6a: N/A) and Section D ticks (1.1 with both sub-boxes, 1.2; 2.1 No, 2.2 No; 3.1-3.4 none) | the memo's copy of the tool, pages 4, 5, 9, 10, 11 |
| Criteria 1-5 wording; item 6 source description; items 1, 4, 6a, 8-11 text reused verbatim | `OSC_HPR_Determination_public_datasets.pdf` text layer: page 5 lines 33-45 (criteria), page 4 lines 56-58 (item 6), page 3 lines 64-74, page 4 lines 61-63, pages 5-7 (items 8-11) |
| Acquisition period "created in the period from 2011 to 2020"; original article author list (seven authors) | PhysioNet project page, read 2026-09-24 |
| Download 2026-09-07 17:49 (`LICENSE.txt`, `SHA256SUMS.txt` ctime); `.download_complete` 2026-09-10 | `SchwingNet/results/g0_facts.md` section 2 and 3 |
| No determination covers VinDr; 2,071 films as 2,632 crops in the intraoperative fold banks only; 0 in the film bank | `g0_facts.md` section 3; `docs/DATASHEET.md` section 2.6; `SchwingNet/tables/tab_corpus.tex` row VinDr-SpineXR and footnote f |
| 10,466 images / 5,000 studies; 8,389 + 2,077; SHA-256 verified, 0 mismatches; 192 images never pseudo-labelled; the release's test split was consumed for training pseudo-labels | `docs/DATASHEET.md` section 2.6 |
| Licence "PhysioNet Restricted Health Data License 1.5.0"; DUA "PhysioNet Restricted Health Data Use Agreement 1.5.0"; access policy "Only registered users who sign the specified data use agreement can access the files"; de-identification three steps; manual inspection and review; IRB of Hospital 108 and Hanoi Medical University Hospital; consent waived; published 24 August 2021; DOI 10.13026/q45h-5h59 | PhysioNet project page, read 2026-09-24 |
| Licence clauses: research only; no re-identification attempt; no sharing; report PHI to PHI-report@physionet.org; contribute code; binds "the LICENSEE" | PhysioNet view-license page, read 2026-09-24 |
| Restricted tier = "registered users who sign a Data Use Agreement"; credentialed tier = "complete the credentialing process and sign a Data Use Agreement"; CITI course "Data or Specimens Only Research" via "Massachusetts Institute of Technology Affiliates" is the credentialing course | https://physionet.org/about/database/ and https://physionet.org/about/citi-course/, read 2026-09-24 |

One correction to the working assumption in the project's records: `slurm/reproduce_all.sh` and the task
brief describe VinDr-SpineXR as "credentialed access". PhysioNet lists it as **restricted** access (registered
account plus the data use agreement; no credentialing, no CITI requirement). REVIEW2_RSNA.md Fix 2 and
`packet_src/statements.md` line 25 already have this right. The draft above uses the source's wording.
