# Extracts of the Greg-only HANDOFF sections assigned to 99_archive

The eight student-readable files of the 2026-10-08 handoff (`README.md`, `GLOSSARY.md`, `RECIPES.md`,
`RESULTS_CATALOG.md`, `DATASET_USAGE.md`, `LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md`) sit whole beside this
file, copied from spinesurg-ct-nnunet `HANDOFF/` at 097933a. The Greg-only files (`MANUSCRIPTS.md`, `LITERATURE_STATE.md`,
`RESEARCH_DIRECTIONS.md`, `CONTEXT_EXPORT.md`, `working_notes/`) are copied whole only into folders 01, 02, 07, 08 and
09; the sections the plan assigns to this folder (DISPOSITION mem r181, r205, r275, r333, r337, r342, r343, r347, r348)
are extracted below in substance, with the file and section they come from. Student surnames in section 13.1 are not
carried (the count of students per abstract is). Prefixes: `ssn:` = spinesurg-ct-nnunet 097933a, `sn:` = its
`SchwingNet/`, `ctsp:` = CTSpinoPelvic1K 7ddfe38, `Desktop/` = a laptop folder recorded in `../../MANIFEST_LOCAL.md`.

## Pointers to sections that are already in the whole copies

- `README.md` section 11, "How the results were reached: a dated timeline" (mem r181): in `README.md` beside this file.
  Its rows from 2026-09-13 to 2026-09-24 are the lineage of every superseded number in `../../SUPERSEDED_NUMBERS.md`.
- `RESULTS_CATALOG.md` Part C header, "The C-arm and film programme before SchwingNet (2026-09-12 to 2026-09-22)" (mem
  r205): in `RESULTS_CATALOG.md` beside this file; restated with the archive's own ids in `../../STATUS.md` section 1.

## MANUSCRIPTS.md section 4: Older C-arm drafts (sources only, private)

| file | state | caution |
|---|---|---|
| `ssn:paper/rsnai/main.tex` "Naming Vertebrae Without an Anchor: Registration-Free Level Identification on Limited-Field Radiographs" | superseded (last commit 6506470, 2026-09-20); built with `paper/rsnai/build.sh`; numbers from `ssn:slurm/reproduce_feasibility.sh` into `~/model_night/repro_feasibility/LEDGER.tsv` (`ssn:docs/FEASIBILITY_REPRODUCE.md`) | uses banks later found leaky; 14 partly supported citing sentences were not corrected (`ssn:docs/RSNAI_PLAN.md` 12:10); a web copy exists as a claude.ai artifact (the link is in `context/feasibility-claims-measured.md`) |
| `ssn:paper/rsnai/graveyard.tex` | material cut from the above, kept for its negative results | — |
| `ssn:paper/focused/main.tex` "Making the Intraoperative Count Exact: Vertebral Level Confirmation from Overlapping C-arm Exposures, With No Learned Component in the Count" | superseded (f61cd72, 2026-09-22); every number transcribed from the evidence briefs `COUNTING_EVIDENCE.md`, `WRONG_LEVEL_COST_EVIDENCE.md`, `WRONG_SITE_BURDEN_EVIDENCE.md`, `SWEEP_TIME_EVIDENCE.md`, `SWEEP_PROTOCOL.md`, `SIMULATION_FIDELITY.md`, `CARM_DEPLOYMENT_EVIDENCE.md`; its Figure 6 cartoon (TikZ lines 876-941) is the model for SchwingNet's numbered panorama | describes the overlapping-exposure sweep, which is in no filing: keep private; the only "latency unmeasured" sentences (`MODEL_CARD.md` section 6) |
| `ssn:paper/rsnai/main_v2.tex` "Navigation from the C-arm alone: naming the vertebral level on any fluoroscope with a physics-parameterised synthetic corpus" + `claims.tex` | superseded the same evening by SchwingNet (c508f5b); 54 / 54 claims verified on the grid (job 40414708); C7 / C8 left as `\todo` | title page says Department of Neurosurgery (wrong); `context/rsnai-paper-endpoint.md` still calls it "THE CULMINATION" (contradiction C2) |
| `ssn:docs/RSNAI_PLAN.md` | the A-E checklist for main_v2 (last status 2026-09-22 15:00) | most boxes never ticked |
| `ssn:docs/research_rsnai_*.json`, `BIB_RESOLVE_2026-09-22.json`, `BIB_AUDIT_2026-09-22*` | verified introduction claims; bibliography resolution (49 entries, workflow wf_387e3e52-e7b) | — |

## MANUSCRIPTS.md section 8: MLHC 2026 (rejected)

`Desktop/MLHC_2026_Research_Track_Paper.pdf` (20 pages, 8 June 2026; text `ctsp:_paper_text.txt`): "CTSpinoPelvic1K: A
Unified CT Benchmark for Lumbosacral Transitional Vertebra Segmentation", 1,137 volumes, 804 patients, 10-class labelmap.
Source `ctsp:mlhc/full-paper-template.tex`; rebuttals `ctsp:_rebuttal_r2.txt`, `_rebuttal_r3.txt`, `_rebuttal_f65r.txt`.
Outcome rejected (`context/publication-roadmap.md`, 2026-07-24); `ctsp:docs/ROADMAP.md` still says "in review, score
2.75/4" (stale, contradiction C8). Where the decision letter is: not recorded. Nothing to redo; never cite it as under
review. (The PDF and source are owned by `03_ctspinopelvic1k_dataset`.)

## MANUSCRIPTS.md section 13: CNS 2026 (Washington DC, 31 October to 4 November 2026)

### 13.1 The twelve OSC abstracts (`contributions/manifest.json` in openspineconsortium.github.io, 2026-05-19)

| CNS id | title (short) | status | students |
|---|---|---|---|
| 66629 | Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model for Preoperative Detection of Lumbar and Thoracic End Anomalies | Mini Oral Poster (Greg; MP4SP1, Monday 2 November, 5:21-6:00 PM) | Greg sole author |
| 66639 | Beyond the Cadaver Lab (OSC med-ed) | Printed Poster | 16 students |
| 68300 | Automated CT-Derived Cobb Angle Measurement | Digital Only | 2 |
| 67525 | Opportunistic Screening for Vertebral Degeneration Using Vertebral Hounsfield Units | Digital Only | 3 |
| 68579 | Sagittal Lumbar Lordosis via a TRALL Angle Pipeline | Digital Only | 3 |
| 69734 | Automated Lumbar Intervertebral Disc Heights | Digital Only | 3 |
| 69093 | Automated CT-Based Pelvic Incidence and Sacral Slope | Digital Only | 2 |
| 68733 | Automated Vertebral Wedging Index | Digital Only | 1 |
| 68460 | Lordosis Distribution Index | "Submitted" (not updated) | 2 |
| 68858 | Lumbar Spinal Stenosis Screening, Normative Torg Ratio L1-L5 | Digital Only | 1 |
| 68779 | Lumbar Spondylolisthesis and Meyerding Classification | "Submitted" (not updated) | 3 |
| 67829 | Automated 3D Vertebral Centroid Trajectory | Digital Only | 1 |

Three more topics are "In preparation" (vertebral spacing, SVA, TPA); the topic list is `Desktop/NextPaper/CNS 2026
ABSTRACT PROJECTS.csv`. The submitted abstract texts are not on disk. Before the posters are shown: the PI / SS abstract
(69093) and the measurement abstracts were computed by May 2026; the spinopelvic-estimator defects and the canal /
end-plate defects were found in August to September; whether the May numbers predate the fixes is not recorded; re-check
each against v11 and the fixed estimators. The talk title promises a single-shot model; no evaluated single-shot model is
recorded on disk (contradiction C17).

### 13.2 Greg's spine deck for 66629

| file | what | disclosure status |
|---|---|---|
| `Desktop/CNS2026_Schwing_NotAllSpines_public_v12.pptx` | the current disclosure-safe deck, 17 slides, CT side only (generator `ctsp:paper/cns2026/make_cns_deck_v12_public.py` + `prep_v16_public_figs.py`); every number asserted against the committed NeurIPS camera-ready; adds the MPDA pipeline, the hardware figure and the spinopelvic table (PI 52.1 against Veilleux 52.1 / Hasegawa 53.4; SS 36.6; PT 15.5) | safe (copied into 03) |
| `Desktop/CNS2026_Schwing_NotAllSpines_public_v11.pptx` | the 15-slide predecessor | safe; superseded (by path, `../../MANIFEST_LOCAL.md`) |
| `Desktop/CNS2026_Schwing_SchwingNet_CNStemplate.pptx` (= `_v10`), `_v9.pptx` | 21-slide C-arm decks on the CNS template | disclose Part B and the sweep; never show publicly (v10 copied into 01; v9 by path) |
| `Desktop/CNS2026_Schwing_SchwingNet.pptx` (v3), `CNS2026_Schwing_Spine_v2.pptx` | earlier arcs | disclose Part B results (by path) |
| `Desktop/CNS2026_Schwing_LSTV.pptx` | the 7 September draft "Naming a Lumbar Level Without Counting From C2" | draft, not presented (copied into 03) |
| generators `ctsp:paper/cns2026/make_cns_deck*.py`, `prep_*`, `figs*` | not tracked (45df97d; `.git/info/exclude`); must never be pushed | copied into 03 |

Deck rules (`context/cns-deck-v2-2026-09-25.md`, in `../../memory/`): CNS template traps (titles about 60 characters;
zero-height text boxes make PowerPoint refuse the file); ACCME rules (no disclosure slide, study design and dates on every
data slide, generic names, no ineligible-company logo, HIPAA statement); render with PowerPoint COM (no LibreOffice on this
machine) and look at every slide; no two consecutive results slides in the same visual form; the NeurIPS track is
"Evaluations and Datasets". Whether the slides were submitted to the meeting, and by what deadline, is not recorded
(`OPEN_QUESTIONS.md` A23).

## MANUSCRIPTS.md section 14: AACA Tech Fair (presented)

`Desktop/TechFair_LSTV_Schwing.pptx` (15 slides; byte-identical copies in `ctsp:` and `NextPaper/`; one copy in
`../../manuscripts/talks/`): "Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae
Detection", 43rd AACA meeting, Mayo Clinic, 13 June 2026; an earlier pipeline built from third-party segmenters; listed in
the TTO package as disclosing neither Part A nor Part B. The title slide says "Department of Neurosurgery" (contradiction
C5). Nothing to redo.

## MANUSCRIPTS.md section 18: Reports to funders

`ctsp:RPPR_Accomplishments.{docx,pdf}` (24 July 2026), `RPPR_B4_Training.*`, `RPPR_RCR_Instruction.docx`, `Desktop/RCR.pdf`,
and `ctsp:Sponsor Progress Report Letter 2026.{docx,pdf}` (the faculty sponsor, 24 July 2026): the NIH F30 year-4 report.
It reports one Cureus paper, five accepted abstracts, NeurIPS under review, and says a single-shot CT model was
"developed and validated" (contradiction C17: no evaluated single-shot model is recorded). Already sent; nothing to redo.
Older: `Desktop/F30_initial.pdf` and `Desktop/Sponsor Progress Report Letter 2024.docx` (classified by name; not opened;
the 2021 F30 was another study).

## MANUSCRIPTS.md section 19: Desktop classification

`Desktop/` top level held 288 entries on 2026-10-08. Several items Greg named were not on the Desktop but in the root of
the public `CTSpinoPelvic1K` working copy, untracked: `MULTI_XR.docx`, `Feasibility_FOV.docx` (external reports, section 17),
`OSC MedEd Manuscript - JEEHP.docx` (section 12), `Med_Ed_CNS.pptx` and `Med_Ed_CNS_visual_abstract.pptx` (section 12),
`BIBM/` (the IEEE template only), `AR/` (one Elsevier template; the AR draft is `Desktop/NextPaper/AR`), `BUU-LSPINE_400/`
(an 800-image data sample). A careless `git add -A` there would publish them (`OPEN_QUESTIONS.md` F11).
`MLHC_2026_Research_Track_Paper.pdf` and `3474_Not_All_Spines_Are_Create.pdf` exist in both places. Personal and
administrative files are not listed one by one. Items classified by name only are marked "(name)".

| item | class | note |
|---|---|---|
| `3474_Not_All_Spines_Are_Create.pdf` | submission (NeurIPS, as reviewed) | section 7 (03) |
| `MLHC_2026_Research_Track_Paper.pdf` | submission (rejected) | section 8 |
| `MDPA.pdf`, `MDPA_FINAL.pdf`, `arxiv_prev.pdf`, `CTSpinoPelvic1K_coauthor_draft.{docx,pdf}`, `CTSpinoPelvic1K_arxiv_preview.pdf`, `CTSpinoPelvic1K_arxiv.tar.gz`, `CTSpinoPelvic1K_overleaf(.zip)`, `CTSpinoPelvic1K_MDPA_overleaf(.zip)`, `CTSpinoPelvic1K_submission(.zip)`, `CTSpinoPelvic1K_coauthor_signoff.xlsx` | manuscript copies and packets (MPDA, v10 era) | section 6 (03); the signoff sheet carries co-author e-mail addresses and is excluded |
| `MDPA_AI.pdf` | AI-text scan of the MPDA | section 6 (03) |
| `cureus.pdf` | published article (med-ed) | section 12 (11) |
| `CNS2026_*.pptx` (8 files) | decks | section 13.2; only `_public_v12` is safe to show |
| `TechFair_LSTV_Schwing.pptx` | deck (presented) | section 14 |
| `SCHWING_PRESENTATION_NSURG.pptx`, `SPINAL_AVM.pptx`, `GREG_PRES.pptx`, `Schwing_Presentations.docx` | decks / presentation list (name) | not opened; not part of the spine-imaging record as far as any file shows (the two spine teaching decks are by path in `../../MANIFEST_LOCAL.md`) |
| a glioma abstract, a reviewed manuscript and a reference | U251 / glioma work | other project |
| `F30_initial.pdf`, `Sponsor Progress Report Letter 2024.docx`, `RCR.pdf` | grant and funder documents (F30 by name) | section 18 |
| `2026 144 Schwing IRB Not HPR Determination 4.21.26.pdf`, `IRB Not HPR Determination 4.21.26.pdf`, `hpr_determination_tool_revised_11_2021_SCHWING_FILLED.pdf` | ethics determinations (2026-144, April 2026) | the dataset work cites 2026-269 (in `ctsp:`); copied into 01's `regulatory/` |
| `spine_study_protocol.pdf` | protocol "Development of a Publicly Accessible, Deep Learning-Ready Clinical and Radiographic Dataset for Spine Surgery Outcomes" (March 2026) | not a manuscript |
| `wsu_patent_policy.pdf` | reference for section 15 | — |
| `2505.01595v2.pdf`, `2505.14338v3.pdf`, `2602.09959v1.pdf`, `2605.10395v1.pdf`, `Panjabi_1976_JBJS_thoracic.pdf`, `STUMP_RIBS.pdf`, `venetti.pdf`, `ACQUIFER.pdf`, `ACQUIFER_2.pdf` (name), `307c4738...pdf` (name) | published papers and references | `../../LITERATURE_BY_PATH.md` |
| `Spine Morphometrics_ Beyond Basic Measurements.pdf` | externally generated research report | verify before citing |
| `Manuscript_Template.docx`, `OUP_General_Template_ID.pdf`, `ama.bst` | templates | — |
| `AI_Imaging_Workshop.{docx,pdf}`, `student_evaluations.xlsx`, `student_evaluations_full_table.docx` (name) | teaching (a 20 June workshop agenda; evaluations) | evaluations may hold names: never commit |
| `QI101.pdf`, `QI102.pdf` | course certificates | section 5 (09) |
| `Lumbosac.csv` | Castellvi grades for 39 cases (older) | data; superseded by the repository copy of 2026-09-04 |
| `Experimental_planning.docx`, `True_PHD.docx` (name) | not opened | not recorded |
| `AshleyBridge-6.0.0-tester-package.zip`, `Ashley Bridge for testers/`, `new_repo.zip`, `new_repo/` | the Beethoven tester package (superseded by release 14.0.0); the 2026-04-18 scaffold of spinesurg-ct-nnunet | Beethoven is owned by 11; the scaffold is by path in `../../MANIFEST_LOCAL.md` |
| `authentication-log-2026-09-27.csv` (name) | not opened | not recorded |
| `x-ray_machine_registration_form.doc` (name) | administrative (the WSU OEHS radiation-machine registration form; copied into 01's `regulatory/`) | — |
| `openapi_key.txt`, `client_secret_*.json`, two `*.ica` files | credential-like files: not read; never commit, copy or upload | `INFRASTRUCTURE.md` section 9 (moved to Greg's private state) |

Research folders on the Desktop (one line each): `CTSpinoPelvic1K-1/` (working copy), `CTSpinoPelvic1K/` (old clone),
`CTSpinoPelvic1K-Syn/` (role not recorded), `CTSP1K_private/` (the pre-purge bundle and the proposals backup),
`spinesurg-ct-nnunet/`, `SpineSurg-CT/`, `spinesurg-ct-annotator/`, `OpenSpineToolkit/`, `openspineconsortium.github.io/`,
a personal site, `NextPaper/`, `NeurIPS/` (camera-ready evidence), `XRaySpinoPelvic1K/` (private), `spine-detector/`,
`lstv-detector/` (older MRI project), `private_ip/`, `FluoroCap_reading/`, `FluoroCap_screening/`, `BUUSPINE/` (data),
`morphometrics/`, `fov_check/`, `itksnap_review/`, `rib_review/`, `v2_inspect/`, `v3_inspect/`, `outlier/` (QC working
folders), `onboarding/`, `MANUSCRIPT/` (a non-spine case report with consent forms: patient material, other project), the
U251 folders, `ashley/`, `ashley-bridge/` (Beethoven), the residency application folder (cite only its CV's publication
list). Where each went is `spine-program/_plan/DISPOSITION.tsv` and `EXCLUDED.md`.

## LITERATURE_STATE.md section 1.7: Spondylolisthesis and pathology (what is held)

| dataset | held n | labels | manifest card |
|---|---|---|---|
| VinDr-SpineXR | 10,466 | lesion classes (fracture, spondylolisthesis, osteophytes, implants; 13 or 8, unreconciled), no levels | `vindr_spinexr` |
| BUU-LSPINE | 3,600 patients | end-plate lines; a spondylolisthesis detection dataset | `buu_lspine_3600` |
| Mendeley 5jdfdgp762 | 714 films; 90 spondylolisthesis films, 33 naming the slipped level in the file name | corners | `mendeley_5jdfdgp762` |
| AASCE 2019 | 609 labelled | scoliosis landmarks | `aasce2019_boostnet` |
| RSNA 2022 cervical fracture CT | 2,019 studies | per-level fracture labels | `rsna_2022_cspine` (the archive this folder records in `../../MANIFEST_GRID.md`; used by nothing) |

The cards are in `ssn:data_platform/DATA_MANIFEST.md` (owned by 10). The status of every number in `LITERATURE_STATE.md`
is governed by its "Status of the numbers quoted here" section, added after `RESULTS_CATALOG.md` was written: where the
two disagree, the catalog wins.

## RESEARCH_DIRECTIONS.md section 5 ("Datasets by project"): the FluoroCap row (line 503 at 097933a)

Added in the fix pass of 2026-10-08 because `../../TODO.md` step 8, `../../STATUS.md` section 4 and `../../MANIFEST_GRID.md`
section 5 cite it for "about 200". The row sits in the section's table of unused data (header: item, n, why unused as
recorded, what would change it, file):

| item | n | why unused, as recorded | what would change it | file |
|---|---|---|---|---|
| FluoroCap | 29,500 panels | dropped by directive D1; the 200-panel test set does not exist | annotate about 200 or write it off | MAN fluorocap; DD23 |

`MAN fluorocap` and `DD23` are the handoff's identifier namespaces (`README.md` section 0 beside this file). The zero itself,
no panel read by a human, is `../fluorocap/FLUOROCAP_QC_2026-09-14.md` section 8, line 166; the 196 / 545 adjudicated panels
it costs for ±5 % / ±3 % around 85 % are on the line after it.
