# Inventory 2: the CTSpinoPelvic1K repository, its root clutter, and 28 sibling folders

Written 2026-10-08. Companion table: `ctsp_repo_root_and_sibling_folders.tsv` (154 rows, one per
homogeneous folder or per file where files differ in value). Sources were read only; nothing was
written outside the scratchpad. The grid was not touched for this inventory.

How things were measured: `git log`, `git ls-files`, `git status --porcelain --ignored` and
`git merge-base` in each repository; `ls -A`, `stat -c %s` and `unzip -l` for the rest;
`pdftotext -l 1` for the first page of a PDF; `unzip -p word/document.xml` for the first lines of
a .docx. Personal and administrative files were classified from their names only; two .docx files
(`RPPR_Accomplishments.docx`, `Sponsor Progress Report Letter 2026.docx`) were opened far enough to
confirm they are the F30 progress report and sponsor letter, then classified admin.

---

## 1. The main repository: `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1`

Public repository `CTSpinoPelvic1K`, branch master, head `7ddfe38` (2026-09-28, "CLAUDE.md: grid
etiquette from C&IT"). Remotes: `origin` = github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K,
`osc` = github.com/OpenSpineConsortium/CTSpinoPelvic1K (`git remote -v`). 1,090 tracked files
(`git ls-files`, summed per top-level directory). `git status` prints 544 lines: six tracked files
modified and uncommitted (`.gitignore`, `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`,
`CAMERA_READY_NEURIPS/src/{bib/references.bib,checklist.tex,neurips_2026.pdf,neurips_2026.tex}`,
`paper/mpda/CTSpinoPelvic1K_reprint_check.pdf`), the rest untracked. A further set of directories
and files is gitignored and therefore invisible to `git status` without `--ignored`: `AASCE19`,
`BUULSPINE_3600`, `CSPINE_ARCHIVE`, `LATERAL_ATLAS`, `MANUAL_REFS`, `IRB_VinDr_2026-09-25(.zip)`,
`COMMERCIALIZATION.md`, `IRB_ADDENDUM.md`, `IRB_IndContract_GSchwing_24926.pdf`, `.env`,
`ckpt_mirror`, `data`, `dist`, `proposals`, `scratchpad`, `_review_0816`, `_verify_0816`,
`rib_fix_work`, `thoracic_fix`, plus ignored files inside `paper`, `results`, `scripts`, `tests`,
`zenodo`, `morphometrics`, `docker`, `review_service`, `reviewtool`, `hardware_review`.
`paper/cns2026/` is kept out through `.git/info/exclude` (stated in
`paper/cns2026/make_cns_deck_v12_public.py`).

The point of that list: the valuable things that exist **only on this laptop** are precisely the
gitignored and excluded ones. They are called out in section 1.3.

### 1.1 Tracked directories and their project family

| directory | what it holds | family | action |
|---|---|---|---|
| `paper/mpda/` (422 tracked) | the Medical Physics dataset article: `main.tex` (last change `70de829` 2026-09-25), `REPRODUCE.md` (the pipeline order and its traps), `PLAN.md` (MPDA policy: DOI before submission, no hypothesis testing), `build.sh`, `make_submission.py`, `make_arxiv.sh`, `make_figures.py`, `make_levelatlas_fig.py`, `page_estimate.py`, bib files, `figures/` (16), `arxiv/`, `overleaf/`, `tools/` (aggregate_spinopelvic.py, digitize_panjabi_fig4a.py, render_pi_construction.py); compiled `CTSpinoPelvic1K_dataset_article.pdf`, `CTSpinoPelvic1K_reprint.pdf`, `reprint_check.pdf`; coauthor-revision workings in `_others/` (114), `_schehr/` (111), `_upd/` (55) | ctsp_dataset | copy text, scripts, figures, final PDFs; reference the three `_*` revision folders (they are Word comment dumps with reviewer names; the one reusable piece is `_schehr/crossref/*.bib`, 37 verified entries) |
| `paper/clinical/` (2) | `main.tex`: "The iliac crest is an unreliable level landmark in transitional lumbosacral anatomy: a morphometric study of 802 screening CT examinations", target SSRR, status "complete draft with real numbers", plus `iliac_crest_landmark.pdf` | qi_wrong_level | copy |
| `paper/cns2026/` (excluded from git) | CNS 2026 talk generators v2 to v12 (`make_cns_deck_v*.py`, `prep_v*_figs.py`), `figs/`, `figs_cited/`, `figs_public/public_numbers.json`, `posterior/*.sbatch`; `abs418_tables.json` belongs to the LITT abstract | archive (talk) | copy all but `abs418_tables.json` |
| `docs/` (61 tracked + 5 untracked) | the working knowledge: `SPINOPELVIC_ESTIMATOR.md`, `LEVEL_MORPHOMETRY.md`, `OSTK_VS_EXTRACTION.md`, `BODY_HEIGHT_INVESTIGATION.md`, `LABELING_GUIDE.md`, `STUDENT_ANNOTATION_PROTOCOL.md`, `RIB_*`, `ANCHOR_ORDINAL_DESIGN.md`, `COUNTING_PRIOR_ART.md`, `CASTELLVI_SCREEN_BLIND_SPOT.md`, `DATASETS_ROADMAP.md`, `ROADMAP.md`, `VERSION_PROGRESSION.md`, `RELEASE_CHECKLIST.md`, `LAB_JOURNAL.md` (one entry, 2026-08-19), castellvi and reread csvs, `annotation/`, `qc/` | ctsp_dataset (morphometry docs also ct_morphometry_parity; Castellvi files also anomaly_scan_census) | copy; redact `castellvi_readers_2026-09-04.csv`, `email_*.md`, `EMAIL_CM_SPINE_REQUEST.md`, `COLLABORATOR_TASKS.md` |
| `docs/HANDOFF_2026-09-21_PM.md` (untracked) | the 2026-09-22 audit-track note for the C-arm work: splits disjoint, detector init exposure from `anchor_none_v2_17-1882`, two generations (76.9 % vs 64.0 % / 54.3 %), LODO: C-ArmLSpine held out sacrum 83.9 % vertebra 5.2 %, DeepFluoro 100 % / 95.2 %, COBRA 13.3 %; 74,364 COBRA near-duplicate laterals | carm_detection | copy; verify every number against `spinesurg-ct-nnunet/HANDOFF/RESULTS_CATALOG.md` before quoting |
| `morphometrics/` (46 tracked) | every measurement table: `level_gradients.csv`, `level_references.csv`, `level_atlas.csv`, `ostk_level_morphometry.csv`, `surgical_morphometrics.csv`, `transition_morphometrics.csv`, `pelvic_shape.csv`, `proximal_femur.csv`, `degenerative.csv`, `opportunistic.csv`, `metal.csv` (550 KB, the largest), `tp_height.csv`, `sacral_ala.csv`, `s1_carve_audit.csv`, `castellvi_grades.csv`, `panjabi_reference.csv`, `pedicle_width_references.csv`, label censuses v7/v9/v10/v11, `anchor_cases.json`, `make_reference_table.py`, 15 tp_height renders; untracked `ctspine1k_pathcsv_agreement.csv` | ct_morphometry_parity and ctsp_dataset | copy; **exclude `annotator_names.csv`** (student names, tracked in a public repository); `.bak`, `.pre0631`, `surgical_morphometrics.v10.csv.bak` are superseded generations |
| `scripts/` (267) | `label_scheme.py` (the scheme contract), the `extract_*.py` chain named in REPRODUCE.md, `qc_*.py`, `build_v3_totalseg.py`, `build_v4_ribs.py`, `build_v6.py`, `build_final_dataset.py`, `benchmark_{totalseg,spineps,moller}.py`, `render_*.py`, `select_anchor_cases.py`, `six_lumbar_readings.py`, `shift_hypothesis_test.py`, `fill_hpr_determination.py`, `adhoc/` | ctsp_dataset | reference by repo and commit |
| `slurm/` (129), `tests/` (25), `zenodo/` (18), `hf/`, `review_service/` (9), `reviewtool/` (4), `configs/`, `containers/`, `docker/` (2 tracked + `Dockerfile.spineps`, `fetch_spineps_weights.py` untracked), `data/README.md` + ITK-SNAP descriptors | pipeline, deposit tooling, the review Space | ctsp_dataset (review tooling also grid_access_students; SPINEPS dockerfile anomaly_scan_census) | reference; copy `zenodo/KNOWN_ISSUES.md`, `zenodo/README.md`, the two untracked docker files and the untracked v5/v6 ITK-SNAP descriptors |
| `results/` (24 tracked + `pelvic_width/` untracked) | `pseudolabel_dice/` (Dataset803 fold Dice), `reading_sheets/`, `rib_qc_v4_vs_release/`, `six_lumbar_readings/` (report.txt, shift_hypothesis.csv, pdf/png), `pelvic_width/` (the student demo study) | ctsp_dataset; six_lumbar_readings also anomaly_scan_census; pelvic_width also grid_access_students | copy |
| `hardware_review/` (5 tracked + ~70 json + ~190 png + `verify/` nii) | the instrumentation review behind hardware classes 62-68 | ctsp_dataset | copy csv/json/README; renders by reference; `verify/*/nii.gz` excluded |
| `qc_final/` (6 tracked + 10 untracked csv), `qc_hardware/` (3) | release QC tables; `version_progression.csv` feeds `docs/VERSION_PROGRESSION.md` | ctsp_dataset | copy |
| `CAMERA_READY_NEURIPS/` (15 tracked + `src/appendix/` 11 untracked tex + `src/figs/fig_app_construction.pdf`) | the NeurIPS 2026 Evaluations & Datasets paper "Not All Spines Are Created Equal: How CT Segmenters Fail on Lumbosacral Transitional Vertebrae" (OpenReview `D8yRWDAGQF`, accepted poster, submission 3474; `CAMERA_READY_CHANGES.md` records the 2026-09-25 camera-ready and the 2026-09-27 corrections after an adversarial audit; `REVIEWER_CRITIQUES.pdf`) | ctsp_dataset | copy the **working tree** (the appendix is untracked and the tex is modified relative to `7ddfe38`) |
| `Student_Projects/` (nested git) | its own repository, remote OpenSpineConsortium/Student_Projects, head `3f1cf04` 2026-09-27 (RECIPE.md, BOARD.md, board.json, GETTING_STARTED.md, IDEAS.md, templates/, tools/, examples/pelvic_width_dimorphism/, `projects/` = clone of the private OpenSpineConsortium/Projects with one proposal) | grid_access_students | reference by repo; `board.json`/`BOARD.md` name students; memory `lab-recipe-and-board` says the last commit was local and not pushed, so check the remote before relying on the URL |
| `assets/` (8) | OSC logo svg/png and `osc_logo.py` | website | copy |
| `mlhc/`, `BIBM/`, `AR/` | journal templates only (MLHC full-paper template, IEEE conference template, elsarticle) | none | exclude; the BIBM and AR manuscripts live under `NextPaper/` |
| root files: `README.md` (the HF card), `CLAUDE.md`, `STATUS.md` (lab notebook, last entry 2026-06-11), `REVIEWERS_*.md` (7 student ITK-SNAP guides), `CITATION.cff`, `LICENSE`, `NOTICE`, `Makefile`, `pyproject.toml`, `requirements.txt`, `_README_hf.md`, `.github/workflows/ci.yml`, six worklist csv/json, `verify_thoracic_edit.py`, `chk_case_lstv.py`, `wedge_renders/wedge_check.png` | ctsp_dataset | copy the md; reference the rest |

### 1.2 Gitignored material of value (exists only on this laptop)

- `proposals/irb/`: `IRB_two_protocols_summary.docx/.pdf` and `PROTOCOL_1_eProtocol_draft_2026-09-15.md`, the plan for two new WSU/DMC protocols (retrospective imaging and records study, Exempt Category 4; prospective silent evaluation), written in the WSU eProtocol order as exported for IRB-21-10-4123. This is the hospital-data path. Family: carm_detection, `regulatory/`.
- `proposals/review/`: the wrong-level-surgery scoping review (`MANUSCRIPT_... v0.4 2026-09-15`, `PROTOCOL_... v1.0`, PRISMA-ScR checklist). The draft says no number has yet passed human charting. Family: qi_wrong_level.
- `proposals/FluoroCap_HPR_attachment.md` (regulatory record of the FluoroCap HPR request), `proposals/student_primer_email.md`, `proposals/cm_spine_request_email.md` (redact names/addresses). `proposals/celebrate_life/` is a community event with contact lists: exclude.
- `COMMERCIALIZATION.md` (draft 2026-09-10): the two-track rule and the product order (A: preoperative CT LSTV flag, 510(k); B: intraoperative C-arm level confirmation). `IRB_ADDENDUM.md` (draft 2026-09-10): disclose commercial intent in the eProtocol and COI, never in the repository; the DMC/Tenet data use agreement is a parallel track. Both bind carm_detection and qi_wrong_level; both stay in a private repository; IRB_ADDENDUM names an IRB office contact (redact).
- `IRB_VinDr_2026-09-25/`: HPR follow-up for VinDr-SpineXR (PhysioNet, data use agreement) under determination 2026-269; `02_HPR_2026-269_memo_2026-09-02.pdf` is the determination memo. Gitignored because the cover note carries a phone number and addresses (commit `ef0474b`). Copy the three PDFs, redact the cover note, drop the zip. Family: plain_film_level_id (and carm regulatory).
- `scratchpad/`: four review reports (`REPORT_final.md`, `REPORT_interim.md`, `SPINE_REVIEW.md`, `CLASSFIX_REVIEW.md`), `results_unified/` (33 BUU-vs-DRR agreement, Bland-Altman and CED figures: plain_film_level_id), `yolo/` + `failures/` + `per_landmark_buu.csv`, `pl_v8l640.csv`, `pl_v8l1024.csv` (corner-detector per-landmark results), measure diagrams `m4..m9/`, `measures*/`; ~120 one-off paper-edit scripts whose effects are already in `main.tex`; label volumes under `brk/`, `gapt/`, `one0631/`, `probecases/`, `case22/` (data, exclude).
- `_review_0816/`, `_verify_0816/`, `thoracic_fix/0068/`: the case 0816 completion and the 0068 renumber, each with scripts and json worth copying and 160-300 MB volumes to exclude. `_verify_0816/va/` duplicates `poster/` (the OSC visual abstract and its build scripts).
- `docker/Dockerfile.spineps`, `docker/fetch_spineps_weights.py`; `data/itksnap_v5_labels.txt`, `data/itksnap_v6_labels.txt`; `data/zenodo_deposit/{manifest.json,splits_5fold.json,dataset_labels.json,SHA256SUMS.txt,KNOWN_ISSUES.md}` (small sidecars of the deposit; the 802 label volumes next to them are data).
- `dist/` is regenerable output of `make_submission.py` (superseded). `ckpt_mirror/` holds the Dataset803 nnU-Net folds (weights; the four ~1.9 MB training logs are text).

### 1.3 Loose files at the repository root, classified by name

**Regulatory (copy to the C-arm project's `regulatory/`):**
`IRB Not HPR Determination 4.21.26.pdf` (WSU IRB HPR 2026-144, 2026-04-21, "Harnessing Algorithmic
Disagreement for Automated Lumbosacral Transitional Vertebrae Detection");
`2026 269 Schwing IRB Not HPR Determination 9.2.26.pdf` and its byte-identical twin
`2026_269 ...` (670,187 bytes each; HPR 2026-269, 2026-09-02, "Open Spine Consortium: Secondary
Analysis of Publicly Available, De-Identified Imaging"; scanned, no text layer, title taken from
`IRB_VinDr_2026-09-25/00_cover_note_to_IRB.md`); `OSC_HPR_Determination_public_datasets.pdf` (the
filled HPR tool behind 2026-269); `[faculty-surname]_IRB.pdf` (eProtocol printout of IRB-21-10-4123
"Improving Outcome in Orthopaedics Trauma Care", printed 2026-09-03, the approved DMC trauma
protocol whose amendment 47 is the students' route to real films; it names the PI, which is a
regulatory fact, not personal data); `DUA.pdf` (advisory text on the DMC/WSU/JHU data-use and IP
matrix for a resident guest researcher; reads as generated advice, not an executed agreement);
`hpr_determination_tool_revised_11_2021.pdf` and `hpr-guidance-activities-that-are-not-hpr-ada-update-4726.docx`
(blank WSU forms, reference only).

**Research documents, C-arm project:** `C-Arm Validation Research Plan.pdf` ("Translational Roadmap
for Exact Intraoperative Vertebral Counting via Overlapping C-Arm Fluoroscopy": Phase I
retrospective PACS baseline and regulatory path, Phase II prototyping and synthetic truth, Phase
III hardware integration and live-animal facility, Phase IV cadaver validation through the
Anatomical Gift Program); `Untitled_Message.zip` (2026-09-21: the same plan as .docx, the AIDaS
seed grant call, the WSU Body Bequest contact page, the X-ray Generating Machine safety guide and
the x-ray machine registration form, five files, 4 MB); `Spine Fluoroscopy Image Datasets.pdf` and
`Fluoroscopic AI Dataset Author Contacts - Google Gemini.pdf` (generated landscape reports; the
second lists author e-mail addresses, redact); `Feasibility_FOV.docx` (registration-free
enumeration under field-of-view truncation; memory `feasibility-claims-measured` tested it claim by
claim) and `MULTI_XR.docx` (serial fluoroscopic mapping, the sweep idea); `2D-3D-GS_UG.pdf` with
`2D-3D-GS.zip` (79 MB, the Ljubljana 2D/3D registration gold standard: data, reference by path);
`PIG/PIG_LEVELCHECK.pdf` (Goswami 2020, IEEE Access) with seven pig CBCT/CT/planar zips (~205 MB,
data).

**Manuscripts, dataset project:** `arxiv_final_draft_9_19_2026.pdf` (arXiv v1 of the dataset
article, 2026-09-19); `3474_Not_All_Spines_Are_Create.pdf` (NeurIPS submission as reviewed);
`MLHC_2026_Research_Track_Paper.pdf` with `_paper_text.txt` and the three rebuttals
`_rebuttal_f65r.txt`, `_rebuttal_r2.txt`, `_rebuttal_r3.txt` (the MLHC 2026 version, score 2.75/4
per `docs/ROADMAP.md`); `TechFair_LSTV_Schwing.pptx`; `LAB_JOURNAL_2026-08-19.pdf`;
`spinopelvic_rotation.mp4`. Superseded builds: `MDPA.pdf` (2026-09-16 anonymized), `MDPA_OL.zip`
(2026-09-06 overleaf), `GPTZero AI Scan ... .pdf`.

**Manuscripts, student program:** `OSC MedEd Manuscript - JEEHP.docx` ("OpenSpineConsortium: an
asynchronous open-source framework for medical student engagement in computational spine imaging
research ... a single-group pre- and post-test study"), `Med_Ed_CNS.pptx`,
`Med_Ed_CNS_visual_abstract.pptx`. Family: grid_access_students.

**Result and QC tables (ctsp_dataset, small, copy):** `Lumbosac.csv` (two-reader Castellvi sheet;
reader initials in the header, rename), `_lstv_phenotypes.csv`, `lumbar_ribs.csv`,
`missing_vertebra.csv`, `stray_vertebrae.csv` (+`.done.txt`), `stump_rib_candidates.csv`,
`spine_pelvis_mixing.csv`, `spine_restored_manifest.csv`, `qc_fail_candidates.csv`,
`rib_qc_fail.csv`, `adjudication_list.csv`, `auto_finalize_manifest.csv`, `rib_worklist.json`,
`Path.csv` (TCIA series paths). `spine_tampering.csv` is keyed by reviewer usernames: exclude or
copy a redacted twin. `cr.json` is a Crossref dump: exclude.

**Ad-hoc code:** `_desc.py`, `_roster5.py`, `_trim1.py`, `chk*.py`, `flag_0068.py`,
`map_tokens.py`, `mk_worklist_add.py` (mostly duplicated in `scripts/adhoc/`); twelve `_w*.sh`
grid watch loops (exclude).

**Beethoven / grid access:** `Browser Extension HPC Orchestration Protocols.pdf`,
`University-Agnostic HPC AI Architecture.pdf`, `openresearch/*.txt` (the prompts that specified
the research-assistant extension). Vendor docs to exclude: `Remote Development FAQ.pdf`,
`WayneStateVSCodeSetupExtension.pdf`, `Publishing Extensions _ VS Code.pdf`,
`Configuring Resend DNS in Spaceship.pdf`, `Claude Setup.exe`.

**Third-party literature (reference by path, cite from the bib files):** `COBRA.pdf`,
`RIBSEG.pdf`, `TS_DS.pdf`, `PANJABI_1991_FULL.pdf` (+`_fixed`), `panjabi_1976.pdf`, `Sun_2021 ...`,
`PG-Net ...`, `Development_and_Evaluation_of_a_Robotic_System ...`,
`CaseReports_T12_hypoplastic_rib.pdf`, `AITR-2002-001.pdf`, `Protocols for Reproducible Machine
Learning Research.pdf`, `Spine chapters.zip` (three Thieme chapters), `sp_978-*.html`,
`docs/ajnr.html`, `docs/ukb.html`, `MANUAL_REFS/` (ACR, NASS, Benzel, Konin-Walz, VERIDAH,
Panjabi 1991/1992). `PANJABI_1991_FULL.pdf` is the source of Table 3 in `level_references.csv`
(memory `panjabi-1991-page-892`).

**Data sets (never copy; reference by path or by public source):** `BUU-LSPINE_400/` (AP 800 +
LA 800 jpg/csv + report xlsx), `BUULSPINE_3600/` (five zips, 9.96 GB, 2026-09-10),
`AASCE19/Archive.zip` (85 MB, 199 jpg), `CSPINE_ARCHIVE/` (2.86 GB JSON+PNG zips, `datasets.xlsx`
8.6 MB, the Scientific Data 2024 paper), `LATERAL_ATLAS/` (1.02 GB zip, 236 lateral full-spine
jpgs), `infobot/images.zip` (288 MB, 2019 pelvic DR + bone-DRR pairs), `ribseg_v2.zip` (608 MB),
`Archive.zip` at the root (182 MB, 2,682 PNGs named `JW_T1_J1_L_*`, origin not recorded),
`ckpt_mirror/` (weights), `data/` (802+802+173+303+12 label volumes), `rib_fix_work/`,
`hardware_review/verify/`, the nii under `scratchpad/`, `_review_0816/`, `_verify_0816/`,
`thoracic_fix/`.

**Personal or administrative (exclude, not opened):** `2017 Summer Research Program Abstract
Book.pdf`, `2026 Neurosurgery Standardized Letter of Recommendation.pdf`,
`PERSONAL_STATEMENT_2026-09-20-*.pdf`, `G Schwing Aug 2026.pdf`, `IRB_2024 Tenet Resident Benefits
Guide.pdf`, `IRB_IndContract_GSchwing_24926.pdf`, `Sponsor Progress Report Letter 2024.docx`,
`Sponsor Progress Report Letter 2026.docx/.pdf`, `RPPR_Accomplishments.docx/.pdf`,
`RPPR_B4_Training.docx/.pdf`, `RPPR_RCR_Instruction.docx`, `~$PR_Accomplishments.docx`,
`T205 2025 RES PROJ GR ... .xlsx`, `ACCME Accreditation Guidelines ... .pdf`, `2026 CNS AM Speaker
Powerpoint Template.pptx`, eleven Citrix `.ica` launch files, `go2432@warrior__.pdf` (a printed
login banner), `cookies.txt` (1 MB, credential-like), three `*.stackdump`, `.env`,
`.claude/settings.local.json`, `.vscode/`, `.pytest_cache/`, `ctspinopelvic1k.egg-info/`,
`CTSpinoPelvic1K-1.code-workspace`. Other studies: `Ablation video_TNN_18Sept26.pptx` (LITT),
`bq_cibersortx-*.html` (U251), `MAN_PREP.pdf` (Neuro-Oncology Advances instructions),
`paper/cns2026/abs418_tables.json` (LITT). Templates: `OUP_General_Template.zip`,
`med_phys_latex_template_v2021.zip`. `2026 AACA_0377.jpg` (10 MB) is an abstract image whose
content was not opened. `radiopedia/` holds one empty folder.

---

## 2. Clones, overleaf exports and the submission package

| folder | date and state | anything not in the main repository? |
|---|---|---|
| `Desktop/CTSpinoPelvic1K` | older clone, master `4fb4a62` 2026-04-28 ("added make"), origin only | **No tracked content**: `git merge-base --is-ancestor 4fb4a62 HEAD` is true in the main repo. Untracked extras: `IRB_IRB-26-03-8648_SubmitPreApproval.pdf` (e-mail receipt 2026-03-30, IRB26038648 assigned for department pre-approval; the first retrospective protocol attempt; copy to regulatory; its outcome is not recorded in any file found), `placed_manifest_orientation_fixed.json` (1.2 MB, April placement manifest), `patch_size_comparison.png` (+ a copy), three `qc_audit_*.png`, 35 `data/lstv_*.png` renders, `data/qc_figures_orifix/`, `qc.tar.gz` (344 MB, data). |
| `Desktop/CTSpinoPelvic1K_overleaf` | 2026-09-04 export (revtex preprint): `main.tex`, `census_table.tex`, `supplementary.tex`, `title_page.tex`, `README.md`, 6 figure PDFs | Nothing unique. 2,398 diff lines against the current `paper/mpda/main.tex`; the repo's `dist/overleaf` is a later build. Its README explains the preprint/reprint page-count trap, already in CLAUDE.md. |
| `Desktop/CTSpinoPelvic1K_MDPA_overleaf` | 2026-09-10 export: `main.tex`, bib, captions, `medphy.bst`, 6 figure PDFs | Nothing unique. 501 diff lines against the repo's own `paper/mpda/CTSpinoPelvic1K_MDPA_overleaf/main.tex` (which is newer) and 1,492 against `main.tex` of 2026-09-25. |
| `Desktop/CTSpinoPelvic1K_submission` | 2026-09-07: `Cover_Letter.md`, `Main_Document_CTSpinoPelvic1K.pdf`, `Supporting_Information_...pdf`, `Title_Page_...pdf`, `LaTeX_source_...zip`, `figures/` | **Yes, as a record**: this is the package as submitted to Medical Physics on 2026-09-07. The repo's `dist/submission/` is a later rebuild and its PDFs differ (diff -rq). Copy it as the as-submitted snapshot. The cover letter states 802 records, concept DOI 10.5281/zenodo.22139642, version DOI 10.5281/zenodo.22642578. |
| `Desktop/CTSP1K_private` | `CTSpinoPelvic1K_prepurge_20260911.bundle` (97.8 MB) and `proposals_backup_20260911/` | **Yes**: the bundle is the full public-repo history before the 2026-09-11 purge of personal material (reference by path, never push). The backup holds what was purged: `irb/IRB_PLAN.md` (the decision for two new protocols; determination 2026-269 covers public data only; a grant due end of October 2026 needs an approved IRB), `irb/PROPOSAL_SHORT.md`, `IRB_two_protocols_summary`, `IRB-21-10-4123_Amendment_Draft.docx` + `irb_amendment_draft.md` and `XR_Fracture_Detector_Proposal.docx` + `xr_fracture_detector.md` (amendment 47: fracture detection and level identification on DMC trauma radiographs; plain_film_level_id and carm regulatory), and six e-mails with student names and addresses (exclude) plus `celebrate_life/` (exclude). |

What a reader loses if the three overleaf/submission folders are dropped: only the 2026-09-07
as-submitted PDFs. Everything else is in git history.

---

## 3. The other sibling folders

| folder | what it is | dates / git | best files | family | if dropped you lose |
|---|---|---|---|---|---|
| `SpineSurg-CT/` | the project's first incarnation: `SpineSurg-CT/SpineSurg-CT` is a git repo (origin Gregory-Schwing-MD-PhD/SpineSurg-CT, `0051074` 2026-04-09, 136 commits) with COLONOG matching/fusion scripts, `metadata_colonog.csv/.xlsx`, `metadata_hnscc.xlsx`, `data_split.txt`, `path.csv`, `tokens/qc_figures`; around it the March 2026 arXiv draft (`SpineSurgCT_arxiv.tex`, `.bib`, two PDFs), `labnotebook/` (progress memos 3/19-3/21/2026 with the clinical case and citations), CLAIM 2024 checklists, `Status_of_dataset.xlsx`, `TODO.docx`, 20 literature PDFs, `viz.tar.gz` (983 MB), an ITK-SNAP tarball (229 MB), `augmentation/`, an empty `wsu/home/go/go24` skeleton, `new_dir/` (two 120 KB repo tarballs) | March-April 2026 | the arXiv draft, labnotebook memos, CLAIM checklists, `metadata_colonog.csv`, `data_split.txt` | ctsp_dataset (CLAIM: carm_detection) | the earliest record of the patient crosswalk and of why the project started (Ishida 54 % miscounting, Hanhivaara CT vs MRI, Kwak 2025 76.4 %) |
| `spinesurg-ct-annotator/` | HF Space annotator app (git, origin Gregory-Schwing-MD-PhD/spinesurg-ct-annotator, `1083c4f` 2026-04-24) | April 2026 | `app.py`, `audit.py`, `sync_manager.py` | grid_access_students, superseded by `review_service/` | nothing that the repo URL does not keep; `assignments.json` may name students |
| `NeurIPS/` | the May 2026 NeurIPS workspace: `main.tex` (2026-05-06), drafts, `bm/` and `audit/` (TotalSegmentator zero-shot benchmark tables, per-case csv, 6-way LSTV subgroups), `ens/` and `pred/` (nnU-Net evaluation outputs), `lstv_review/lstv_review/` (LSTVReviewer tool, install guide, manifest, Mahato 2020), `Lumbosac_Castelvii_Class.csv`, `verse_veridah_labelcorrection.csv/.xlsx` (2026-05-08), renders; also data (0002 CT 299 MB, BUU zip 917 MB), weights (`checkpoint_best.pth` 191 MB), a 61 MB profiler trace, a 60 MB copyrighted handbook, phone photos, and a **Google OAuth client secret json** | April-June 2026 | `bm/`, `audit/`, `ens/`, `pred/`, the lstv_review packet, the VerSe/VERIDAH corrections | ctsp_dataset; the VerSe corrections also anomaly_scan_census | the benchmark tables behind the NeurIPS paper in their raw per-case form and the label-correction list; which checkpoint made `ens/`/`pred/` is not recorded in the folder |
| `CTSpinoPelvic1K-Syn/` | synthetic Castellvi-graded LSTV generator scaffold; local git `7098eb1` 2026-06-11, **no remote**; `fuse_split` built, the generation engine not (STATUS.md 2026-06-11) | June 2026 | `ctspino_syn/{annotation,castellvi,fuse_split,manifest}.py`, `README.md`, tests | anomaly_scan_census | the only copy; README uses the banned word once, rewrite on copy |
| `LDI/` | automated lumbar lordosis and Lordosis Distribution Index from CT+label pairs (L1/L4/S1 endplate corners); no git | 2026-05-26 | `automated_lordosis.py`, `dataset_interface.py`, `run_hf_sample.py`, `README.md` | ct_morphometry_parity | a second, independent lordosis implementation, which is the outside check CLAUDE.md asks for; the only copy |
| `itksnap_review/` | seven-case ITK-SNAP review packet, 2026-08-18/20: 21 CT volumes (data) + `README.md` (the 0008 lumbar-rib-vs-sacralized-L5 reasoning and the house rule "anchor at S1, count up; a rib never renames a vertebra") + `labels_review.txt` | August 2026 | `README.md`, `labels_review.txt`, two png | ctsp_dataset | the written reasoning for the 0008 reclass |
| `rib_review/`, `fov_check/`, `v2_inspect/`, `v3_inspect/`, `new/`, `morphometrics/` (Desktop) | renders and probe volumes from June-August 2026; Desktop `morphometrics/transition_morphometrics.csv` (2026-08-17) is an earlier generation (md5 differs from every repo copy) | June-August 2026 | none essential | ctsp_dataset / superseded | nothing the repo tables do not supersede |
| `IRB/` | March 2026 retrospective spine study protocol (`spine_study_protocol.docx/.pdf`, `Retrospective IRB PROTOCOL.pdf`, `Data_Collection_Tool`), WSU/DMC guidance PDFs, `co-investigators.xlsx` (names), `GREG/` and `HAZEM/` CITI certificates | March 2026 | the protocol and data collection tool | carm_detection regulatory (superseded by `proposals/irb`, September 2026) | the record of the first filing (IRB-26-03-8648) |
| `OpenSpineConsortium-logo/` | 10 logo renders, 2026-09-28 | | all | website | nothing elsewhere in this inventory (assets/ has the svg source) |
| `MANS_Talk/` | August 2026 teaching talk on degenerative cervical myelopathy and lumbar stenosis imaging: `MANS_Schwing.pptx` (12 MB), outlines and a field guide in md/html, 20 literature PDFs | July-August 2026 | the md files | archive (education) | nothing on the level-identification line |
| `new_repo/` | 2026-04-18 scaffold of spinesurg-ct-nnunet (README, docs_pipeline.md, def file, 65 KB tarball) | April 2026 | none | superseded by the private repo | nothing |
| `MANUSCRIPT/`, `MBR_CoAuthor_Review_2026-09-07/`, `bhargav'sabstract/`, `outlier/`, `F30/`, `stepwork/`, `BUUSPINE/` (empty) | a non-spine BMJ case report with consent and salary paperwork; the LITT review package; another student's craniotomy tables; contract prompt-writing for an external LLM vendor plus a CV; fellowship cost-sharing paperwork; personal; empty | | | exclude | nothing spine-related |

---

## 4. What is superseded by what

- `SpineSurg-CT` repo (April 2026) -> `CTSpinoPelvic1K` older clone (`4fb4a62`, 2026-04-28) -> `CTSpinoPelvic1K-1` (`7ddfe38`, 2026-09-28). The first two are ancestors in substance and in git respectively.
- Dataset paper lineage: `SpineSurgCT_arxiv.tex` (March) -> MLHC 2026 submission + rebuttals (April-June) -> Medical Physics MDPA: overleaf 2026-09-04 -> overleaf 2026-09-06/10 -> submitted 2026-09-07 (`CTSpinoPelvic1K_submission`) -> arXiv v1 2026-09-19 -> `paper/mpda/main.tex` at `70de829` 2026-09-25 (current).
- NeurIPS lineage: `NeurIPS/main.tex` (2026-05-06) -> `3474_Not_All_Spines_Are_Create.pdf` (reviewed) -> `CAMERA_READY_NEURIPS/src/neurips_2026.tex` (2026-09-25, corrected 2026-09-27, working tree modified after `7ddfe38`).
- IRB lineage: `IRB/` March drafts and IRB-26-03-8648 pre-approval receipt (2026-03-30) -> HPR 2026-144 (2026-04-21) -> HPR 2026-269 (2026-09-02) -> `CTSP1K_private/.../IRB_PLAN.md` decision for two new protocols (2026-09-11 backup) -> `proposals/irb/PROTOCOL_1_eProtocol_draft_2026-09-15.md` and the VinDr follow-up (2026-09-25). The amendment-47 path on IRB-21-10-4123 runs beside it for the students.
- Morphometrics tables: Desktop `morphometrics/` (2026-08-17) and `scratchpad/transition_morphometrics_OLD.csv` -> `.pre0631` -> `.bak` -> tracked `morphometrics/*.csv` at `7ddfe38`.
- Annotator tooling: `spinesurg-ct-annotator` (April) -> `review_service/` + `reviewtool/` in the main repo.

## 5. Flags

1. **Credential in plain text**: `CTSpinoPelvic1K-1/LATERAL_ATLAS/key.txt` holds an AWS access key id and secret access key. Rotate the key, never copy the file, delete it after rotation. (Its first two lines were printed into this session's tool output while classifying it; treat the key as exposed.)
2. **Credential**: `NeurIPS/client_secret_525812647843-*.apps.googleusercontent.com.json` (Google OAuth client secret). Revoke if unused. `CTSpinoPelvic1K-1/.env` (gitignored, not opened) and `cookies.txt` (1 MB browser cookies) are also credential-like.
3. **Student names in a tracked file of the public repository**: `morphometrics/annotator_names.csv`. Also carrying names or usernames: `spine_tampering.csv`, `Lumbosac.csv` (reader initials), `docs/castellvi_readers_2026-09-04.csv`, `student_vertebra_work.csv` (not opened), `Student_Projects/board.json`, `spinesurg-ct-annotator/assignments.json`, every `*email*.md` under `proposals/` and `CTSP1K_private/proposals_backup_20260911/`, `IRB_VinDr_2026-09-25/00_cover_note_to_IRB.*` (phone number), `IRB_ADDENDUM.md` (IRB office contact), `paper/mpda/_others|_schehr|_upd/word/people.xml`.
4. **Untracked or excluded files of high value with no other copy**: `docs/HANDOFF_2026-09-21_PM.md`, `CAMERA_READY_NEURIPS/src/appendix/` (11 tex) and the modified camera-ready tex, `paper/cns2026/`, `proposals/irb/`, `proposals/review/`, `COMMERCIALIZATION.md`, `IRB_ADDENDUM.md`, `C-Arm Validation Research Plan.pdf`, `Untitled_Message.zip` contents, `CTSpinoPelvic1K-Syn/` (no remote), `LDI/` (no git), `itksnap_review/README.md`, `CTSpinoPelvic1K_submission/` (as-submitted PDFs).
5. **Other-study material mixed into the spine tree**: `paper/cns2026/abs418_tables.json` (LITT), `Ablation video_TNN_18Sept26.pptx`, `bq_cibersortx-*.html` (U251), `MAN_PREP.pdf`, `v2_inspect/Figure1_Letter_NeuroOnc.pdf`, `MBR_CoAuthor_Review_2026-09-07/`.
6. **Banned word**: appears in `CTSpinoPelvic1K-Syn/README.md` ("... manifest"). Rewrite on copy. No other occurrence was searched for in this inventory.
7. **Working tree ahead of the last commit**: the camera-ready tex/pdf, `checklist.tex`, `references.bib`, `CAMERA_READY_CHANGES.md`, `.gitignore` and `paper/mpda/CTSpinoPelvic1K_reprint_check.pdf` are modified and uncommitted in `CTSpinoPelvic1K-1`. Copy from the working tree, and note that `7ddfe38` does not hold these edits.
8. **Duplicate determination PDF**: `2026 269 ...` and `2026_269 ...` are byte-identical (670,187 bytes); keep one.
9. The `osc` remote carries the same history as `origin` only if both were pushed; this inventory did not query the remotes (no network).

## 6. Unknowns (not recorded in any file read)

- Origin of the root `Archive.zip` (2,682 PNGs named `JW_T1_J1_L_*`, dated 2026-02-27).
- Which build produced Desktop `morphometrics/transition_morphometrics.csv` (2026-08-17); its md5 matches none of the four repo copies.
- Which checkpoint produced `NeurIPS/ens/` and `NeurIPS/pred/`.
- The outcome of IRB-26-03-8648 (only the 2026-03-30 pre-approval receipt exists).
- Content of `2026 AACA_0377.jpg` (not opened).
- `paper/mpda/notes.docx` yielded no text on extraction; whether it is empty or image-only.
- Whether `Student_Projects` head `3f1cf04` was pushed to OpenSpineConsortium/Student_Projects (memory says local only on 2026-09-27; not verified).
- Whether `CTSpinoPelvic1K-Syn` was ever pushed anywhere (no remote configured).
- A full file-size sweep (>25 MB) of every subtree was not run because `find` over the OneDrive tree timed out; the large items named above were measured individually with `ls -l`. Subfolders not measured file by file: `Student_Projects/` (223 files), `BUU-LSPINE_400/` (1,603 files), `hardware_review/renders`, `scratchpad/` images.
- `docs/ids.txt` (36 bytes), `data/README.md`, `student_vertebra_work.csv` were not read.
- Author of `DUA.pdf` (reads as generated advice).
