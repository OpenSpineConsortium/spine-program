# Inventory 4: the loose files at the Desktop root

Source: `C:\Users\grego\OneDrive\Desktop\` (files only, not folders). Counted 2026-10-08 with
`Get-ChildItem -File -Force`: **224 files** (93 pdf, 27 docx, 24 lnk, 14 pptx, 10 zip, 10 png,
8 jpg, 6 exe, 5 xlsx, 5 mp4, 4 jpeg, 2 tmp, 2 txt, 2 ica, 2 csv, and one each of mp3, stackdump,
doc, epub, html, tar.gz, json, ini, dll, bst). Inventory: `desktop_root_loose_files.tsv`
(207 rows; the 18 `pkwrap IWA test*.lnk` shortcuts are one row).

Git state: none. Nothing at the Desktop root is inside a repository. Dates below are file
modification times from the directory listing.

How files were classified: by name first; where the name was ambiguous, page 1 of the PDF,
the first paragraphs of the docx, the first two slides of the pptx, the zip entry list, or the
image itself. Personal and administrative files were not opened beyond what the name required;
a few images and two small text files that looked like they might be research were opened and
turned out to be personal; they are marked exclude and their content is not described here.

## Disposition in one line

| action | files | what |
|---|---|---|
| copy | 11 | 5 regulatory or policy documents, 4 manuscripts or decks, 1 GPTZero scan, 1 literature review |
| reference | 30 | duplicates of repository files, superseded builds, third-party literature, one QC figure, one test radiograph |
| exclude | 183 files in 166 rows | by `kind` in the TSV: 80 personal, 42 administrative, 22 environment rows (39 files: installers, shortcuts, lock and temp files, binaries), 9 documents and 4 manuscripts of other studies or side work, 2 code, 1 figure, 6 other (2 plain-text credentials, a bib style, a login note, a site-verification token, a case-report zip) |

## The files worth copying (11)

Regulatory, for the C-arm project's `regulatory/` folder:

- `2026 144 Schwing IRB Not HPR Determination 4.21.26.pdf` (2026-04-21, 13 pages, 2.1 MB) — WSU IRB
  administrative determination 2026-144, "not human participant research". Byte-identical copies:
  `IRB Not HPR Determination 4.21.26.pdf` at the Desktop root and, untracked, in the
  `CTSpinoPelvic1K-1` root (md5 38f5c700a1…). Copy once.
- `hpr_determination_tool_revised_11_2021_SCHWING_FILLED.pdf` (2026-05-31, 12 pages) — the filled
  determination tool. Its text names data "de-identified by the data provider (Radiological Society
  of North America) prior to public release", Detroit Medical Center as a record source, and
  "secondary or retrospective data collection". Which letter this filled copy produced (2026-144 of
  April or 2026-269 of 2026-09-02, the latter in the `CTSpinoPelvic1K-1` root) is not recorded.
- `x-ray_machine_registration_form.doc` (2026-09-18, blank) — WSU OEHS "NEW Radiation Machine
  Registration Form" for registering an x-ray-producing machine with the State of Michigan. Relevant
  the moment a C-arm comes under lab control. Whether any machine was registered is not recorded.
- `wsu_patent_policy.pdf` (2026-09-19, public, 10 pages) — context for the commercialization
  stance; the signed disclosure forms stay in `private_ip/` and are not copied.
- (reference, not copy) `spine_study_protocol.pdf` (2026-03-30, 3 pages) is the earlier draft of
  the DMC data protocol; `Desktop/IRB/spine_study_protocol.pdf` (134,943 B) is the later, retitled
  version with a named sponsor and should be the copy taken by the IRB inventory.

Manuscripts and decks:

- `MDPA_FINAL.pdf` (dated 21 September 2026 in the PDF, 25 pages double-spaced, double-anonymized)
  — the submitted Medical Physics dataset article. No other file of this size exists under the
  Desktop, so this is the only copy of the submitted PDF. The page limit is 10 **published** pages
  and only `build.sh --reprint` measures it; the 25 here is the submission form's count.
- `CNS2026_Schwing_NotAllSpines_public_v12.pptx` (2026-09-26, 17 slides, 6.9 MB) — the current
  public CNS 2026 deck ("Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model For
  Preoperative Detection Of Lumbar And Thoracic End Anomalies"; Mini Podium 4, Spine Session 1,
  2 November 2026). Title slide reads Department of General Surgery. Memory note
  `cns-deck-v2-2026-09-25` names v12_public as the CT-side deck.
- `CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx` (2026-09-26, 21 slides, 13.6 MB) — the full
  deck on the CNS ACCME template that discloses Part B (SchwingNet, the fluoroscopy level-naming
  network) and the unfiled sweep. **Private.** It belongs to the C-arm project folder in the private
  repository and never to the website, HF or Zenodo. `CNS2026_Schwing_SchwingNet_CNStemplate.pptx`
  is byte-identical (md5 aa8df26fb2…).
- `CNS2026_Schwing_LSTV.pptx` (2026-09-07, 17 slides, 2.3 MB) — the draft deck "Naming a Lumbar
  Level Without Counting From C2: CTSpinoPelvic1K and a One-Shot Detector for Transitional
  Anatomy", not presented. The only deck in the lineage framed on the dataset rather than the
  detector.
- `cureus.pdf` (published 2026-07-14, 8 pages, CC-BY) — Schehr et al., "OpenSpineConsortium: An
  Open-Source Framework for Medical Student Engagement", Cureus, DOI 10.7759/cureus.112661. No
  other copy was found under the Desktop by name. This is the published description of the
  student-engagement framework the grid-access project continues.
- `MDPA_AI.pdf` (2026-09-12, 22 pages) — GPTZero scan of the 12 September build (reports 60% AI
  probability). A record of the AI-text check; a second scan of the single-column docx sits
  untracked in the `CTSpinoPelvic1K-1` root.
- `Spine Morphometrics_ Beyond Basic Measurements.pdf` (2026-02-21, 26 pages, Google Docs render,
  no author) — "Comprehensive Radiomorphometric Analysis of Lumbar Spine Pathologies". It reads as
  an AI-assembled literature review; useful as a map of the normative series for the morphometry
  parity work, but every number in it must be checked against the primary paper before use.

## The CNS 2026 deck lineage (all at the Desktop root)

The same decks sit under descriptive names in `private_ip/TTO_package_2026-09-25/followup/`
(matched by byte size; `private_ip/` itself is not copied):

| Desktop file | date | slides | TTO follow-up name | state |
|---|---|---|---|---|
| CNS2026_Schwing_LSTV.pptx | 09-07 | 17 | CNS2026_spine_talk_DRAFT_deck_2026-09-07_not_presented.pptx | copy |
| CNS2026_Schwing_Spine_v2.pptx | 09-25 | 21 | CNS2026_spine_talk_v2_2026-09-25_results_only.pptx | superseded |
| CNS2026_Schwing_SchwingNet.pptx | 09-25 | 21 | CNS2026_spine_talk_v3_2026-09-25_SchwingNet_results_only.pptx | superseded, private |
| CNS2026_Schwing_SchwingNet_CNStemplate_v9.pptx | 09-25 | 21 | CNS2026_spine_talk_v9_2026-09-26_CNS_template_ACCME.pptx | superseded, private |
| CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx (= _CNStemplate.pptx) | 09-26 | 21 | CNS2026_spine_talk_v10_2026-09-26_CNS_template_ACCME.pptx | **copy, private** |
| CNS2026_Schwing_NotAllSpines_public_v11.pptx | 09-26 | 15 | — | superseded |
| CNS2026_Schwing_NotAllSpines_public_v12.pptx | 09-26 | 17 | — | **copy, public** |

The deck generator was untracked from `CTSpinoPelvic1K-1` at commit 45df97d and "kept locally";
whether these files are its output is not verifiable from the root. `TechFair_LSTV_Schwing.pptx`
(AACA 2026 Tech Fair, 2026-07-24, 15 slides) is byte-identical in the `CTSpinoPelvic1K-1` root
(untracked) and in `Desktop/NextPaper`; its title slide says "Department of Neurosurgery" and
"NIH F30 Fellow" — historical, and wrong under the standing affiliation rule (General Surgery).

## Duplicates of files inside repositories

| Desktop root file | copy inside a repository | identical? | tracked? |
|---|---|---|---|
| 3474_Not_All_Spines_Are_Create.pdf | CTSpinoPelvic1K-1/3474_Not_All_Spines_Are_Create.pdf | yes | untracked |
| AI_Imaging_Workshop.pdf | CTSpinoPelvic1K-1/AI_Imaging_Workshop.pdf and mlhc/AI_Imaging_Workshop.pdf | yes | untracked |
| AI_Imaging_Workshop.pdf | openspineconsortium.github.io/AI_Imaging_Workshop.pdf | no (90,116 B vs 90,034 B) | tracked |
| IRB Not HPR Determination 4.21.26.pdf | CTSpinoPelvic1K-1/IRB Not HPR Determination 4.21.26.pdf | yes | untracked |
| MLHC_2026_Research_Track_Paper.pdf | CTSpinoPelvic1K-1/MLHC_2026_Research_Track_Paper.pdf | yes | untracked |
| MLHC_2026_Research_Track_Paper.pdf | SpineSurg-CT/MLHC_2026_Research_Track_Paper.pdf | same size, hash not run | not recorded |
| MDPA.pdf | CTSpinoPelvic1K-1/MDPA.pdf | no (root 2026-09-12; repo 2026-09-16) | untracked |
| arxiv_prev.pdf | CTSpinoPelvic1K-1/arxiv_final_draft_9_19_2026.pdf | yes | untracked |
| CTSpinoPelvic1K_coauthor_draft.pdf / .docx | CTSpinoPelvic1K-1/paper/mpda/ | yes | tracked |
| CTSpinoPelvic1K_arxiv_preview.pdf | CTSpinoPelvic1K-1/paper/mpda/ | no (repo later, larger) | tracked |
| CTSpinoPelvic1K_arxiv.tar.gz | CTSpinoPelvic1K-1/paper/mpda/ | no (repo later, larger) | untracked |
| CTSpinoPelvic1K_MDPA_overleaf.zip | CTSpinoPelvic1K-1/paper/mpda/ | no (repo later, larger) | tracked |
| CTSpinoPelvic1K_overleaf.zip | CTSpinoPelvic1K-1/dist/ | no (repo later, larger) | untracked |
| Lumbosac.csv | CTSpinoPelvic1K-1/Lumbosac.csv | no (root 41 lines, 1 reviewer; repo 47 lines, 3 reviewer columns, 2026-09-04) | untracked |
| TechFair_LSTV_Schwing.pptx | CTSpinoPelvic1K-1/ and NextPaper/ | yes | untracked |
| Sponsor Progress Report Letter 2024.docx | CTSpinoPelvic1K-1/ | yes | untracked (and excluded: other study) |
| googlec3911e7fb095977e.html | openspineconsortium.github.io/ | no (53 vs 54 B; same token) | tracked |
| ama.bst | nsurg/RAJ/ama.bst | yes | not a repo |
| JNS24-1395_…_Annotated.pdf | nsurg/RAJ/ and u251-xenograft-murine-RNASeq-study/manuscript/ | yes | excluded: other study |
| OUP_General_Template_ID.pdf | u251-xenograft-murine-RNASeq-study/manuscript/ | yes | excluded: other study |
| 74_1.3.6.1.4.1.9328.50.4.80461_propagation.png | new/, new/new/, CASE_HIEBER/qc/ | no (three near variants) | not a repo |

Where the repository copy is untracked, "lives in a repo" does not hold: whichever inventory
copies the file must copy it from one place, once, and record both paths.

## Superseded chains

- Medical Physics article PDFs: `MDPA.pdf` (09-12) → `CTSpinoPelvic1K-1/MDPA.pdf` (09-16) →
  `MDPA_FINAL.pdf` (09-21, the submission). arXiv: `CTSpinoPelvic1K_arxiv_preview.pdf` (09-07) →
  `arxiv_prev.pdf` = `arxiv_final_draft_9_19_2026.pdf` (09-19). Source bundles: the three zips and
  the tar.gz at the root (09-06 to 09-10) are all older and smaller than their `paper/mpda` or
  `dist/` counterparts; the unzipped Desktop folders `CTSpinoPelvic1K_overleaf`,
  `CTSpinoPelvic1K_MDPA_overleaf`, `CTSpinoPelvic1K_submission` are inventoried separately.
- `Lumbosac.csv` root (06-08) → `CTSpinoPelvic1K-1/Lumbosac.csv` (09-04). The sheet records
  Castellvi types per CTSP "Token" (ambiguous / lumbarised L6 / sacral count 4 / sacralised /
  semi-sacralised / one normal reference). Whether "Token N" equals the zero-padded release case
  id is not recorded.
- `spine_study_protocol.pdf` root (03-30) → `IRB/spine_study_protocol.pdf` (retitled, sponsor named).
- `AshleyBridge-6.0.0-tester-package.zip` (09-29) → OpenSpineConsortium/beethoven releases; the
  product has been Beethoven since 2026-09-29 and Ashley Schehr is a person.
- `new_repo.zip` (04-18, a scaffold of spinesurg-ct-nnunet) → the private repo at L6_Class 097933a.

## Third-party literature kept by path, not copied

`Panjabi_1976_JBJS_thoracic.pdf` (JBJS 58-A:642, 1976; a different paper from
`CTSpinoPelvic1K-1/panjabi_1976.pdf`, which is the J Biomech flexibility/stiffness paper of the
same year), `STUMP_RIBS.pdf` (Möller et al., arXiv:2505.05004, the rib method of census arm B).
Both are cited by identifier; the Panjabi copy matters because library access was cut 2026-06-30.
The four 2025–2026 arXiv ML-theory PDFs at the root are unrelated to spine (contract side work)
and are excluded.

## Other studies and side work (excluded, 21 files)

LITT / glioblastoma (CNS_SNO abstract docx, JNS24-1395 manuscript, OUP Neuro-Oncology letter
template, two ONC201 papers, FHER.png flowchart, SCHWING_PRESENTATION_NSURG.pptx at 51 MB); the
2021 F30 (Myc inhibitor design with GOMC: F30_initial.pdf, Sponsor Progress Report Letter 2024,
RCR.pdf, Experimental_planning.docx); Neurocheck provisional patent zip and PupillometerPLR zip;
the peritoneal-metastasis case report zip; four arXiv ML papers, a prompt-writing guide and one
screenshot from contract side work; FJP.docx (an ssh login line). Two spine teaching decks
(GREG_PRES.pptx on lumbar stenosis, SPINAL_AVM.pptx) are clinical teaching, not research:
archive, reference only.

## What a reader would lose if the root were dropped

The submitted Medical Physics PDF (`MDPA_FINAL.pdf`), the two IRB documents in their filled and
determined form, the x-ray machine registration form, the published Cureus article, the public v12
and private v10 CNS decks, and the dataset-framed draft deck of 2026-09-07. Everything else at the
root is either a duplicate of a repository or Desktop-folder file, an older build, third-party
literature, or personal.

## Flags

1. Two plain-text credentials sit on the OneDrive-synced Desktop: `openapi_key.txt` and
   `client_secret_….apps.googleusercontent.com.json`. Never copy; move and rotate.
2. The v3, v9 and v10 CNS decks disclose SchwingNet. Private repository only.
3. `CTSpinoPelvic1K_coauthor_signoff.xlsx` carries co-author e-mail addresses — excluded; the
   project needs a redacted authorship-approval record written by Greg.
4. Many personal filenames at the root are sensitive. The `_plan/` exclusion list should summarise
   personal and administrative files by category and count (80 personal and 42 administrative
   rows in the TSV), not reproduce their names.
5. `TEST_XR.png` is a radiograph of unrecorded origin (a lateral lumbar film with pedicle screws);
   not copied and should not enter any repository until its source is known.
6. The TechFair deck's affiliation is wrong under the standing rule; it is historical and is not
   to be re-presented unchanged.
