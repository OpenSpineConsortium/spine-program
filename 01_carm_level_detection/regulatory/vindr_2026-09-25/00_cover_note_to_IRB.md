To: IRBQuestions@wayne.edu
From: Gregory Schwing, MD, PhD — Resident Physician, General Surgery, Detroit Medical Center / Wayne State University School of Medicine — go2432@wayne.edu — [phone withheld]
Faculty sponsor: Loren Schwiebert, PhD, Professor, Department of Computer Science
Subject: HPR determination request — one dataset obtained under a data use agreement (follow-up to HPR 2026-269)

Dear IRB Administration Office,

On 2 September 2026 your office issued a Notice of IRB Administrative Determination (WSU IRB HPR Number 2026-269) that the project "Open Spine Consortium: Secondary Analysis of Publicly Available, De-Identified Imaging Datasets and the Derived Annotations, Software, and Models Produced From Them" does not constitute human participant research under 45 CFR 46 or the FDA regulations.

The tool I submitted for that determination limited its scope, in item 7, to datasets that "can be downloaded by any member of the public without an application, request for permission, eligibility review, or data use agreement," and stated that a dataset governed by a data use agreement "falls outside this determination and a separate IRB submission will be made before that dataset is used." This is that separate submission. It covers one dataset:

**VinDr-SpineXR** (version 1.0.0): 10,466 de-identified spine radiographs from 5,000 studies, deposited on PhysioNet by its authors (Pham HH, Nguyen Trung H, Nguyen HQ, 2021; https://doi.org/10.13026/q45h-5h59) and served under the PhysioNet Restricted Health Data License 1.5.0 to registered users who accept the PhysioNet Restricted Health Data Use Agreement 1.5.0. This is PhysioNet's restricted-access tier: an individual registered account and the agreement; no credentialing or CITI training is required. The account holder is me (PhysioNet username gschwing, registered with go2432@wayne.edu).

The facts I ask the office to weigh:

1. **The data are de-identified by the depositor before release.** The depositors removed protected health information from the DICOM tags, removed patient information burned into the pixel data after manual inspection of every scan, and manually reviewed the de-identified images. Their own study was approved by the Institutional Review Boards of Hospital 108 and Hanoi Medical University Hospital with a waiver of informed consent (scans from 2011–2020). The investigators have no relationship with either hospital.
2. **No re-identification or contact is possible.** No key, code or linkage is supplied; the released per-image fields are the depositors' study and image identifiers and their lesion annotations.
3. **The agreement's terms are honoured.** Research use only; no re-identification attempt; no sharing of access; any identifying information found is to be reported to PHI-report@physionet.org; code arising from the data is released openly. The files reside only on the WSU High Performance Computing Grid in my own storage; no image, crop or derived frame is redistributed or included in any released dataset.
4. **The dataset has already been downloaded and used, and I disclose that plainly.** It was downloaded on 7 September 2026 — after the 2026-269 tool was completed (28 August) and after the determination issued (2 September) — and 2,071 of its films were used, cropped, as pseudo-labelled training data for a subset of models in a manuscript now in preparation; no VinDr-SpineXR image was used for testing, for any reported accuracy, or in any figure. The separate submission promised in item 7 should have preceded that use and did not. I submit it now and ask the office to determine whether this secondary analysis of a de-identified, agreement-governed dataset is human participant research. If the office determines that it is, the models trained on it will be withdrawn and retrained without it.

My own reading, offered for the office's concurrence or correction: not human participant research, in the category "De-Identified Private Information and/or Human Biological Specimens" under which 2026-269 was issued. I note that the tool's "Public Use Datasets" category carries the note that IRB approval is required where "a data use agreement is involved"; this submission exists so that the office, not the investigator, decides which category governs.

Attached: the completed determination tool (01), the 2026-269 memo (02), the tool as filed on 28 August 2026 (03). The PhysioNet project page (https://physionet.org/content/vindr-spinexr/1.0.0/), the licence and agreement text (https://physionet.org/content/vindr-spinexr/view-license/1.0.0/), and PhysioNet's description of its access tiers (https://physionet.org/about/database/) are public pages; I can supply printouts on request. Dataset article: Nguyen HT, Pham HH, Nguyen NT, Nguyen HQ, Huynh TQ, Dao M, Vu V. VinDr-SpineXR: a deep learning framework for spinal lesions detection and classification from radiographs. MICCAI 2021.

Sincerely,

Gregory Schwing, MD, PhD
