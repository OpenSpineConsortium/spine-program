# MANIFEST_LOCAL: every file copied into this folder, and every valuable file deliberately not copied

**The laptop paths in this file are a record of where each copy came from on 2026-10-08. They are history, not a
dependency: nothing in this folder reads them, and the folder is complete without them.** The only outside references of
this project are the grid (`MANIFEST_GRID.md`) and the code repositories (`MANIFEST_CODE.md`). Laptop paths appear in no
other file of this folder; where a copied document once carried one it now carries a marker prefix (section 4).

Built from the 288 rows of `../_plan/DISPOSITION.tsv` whose `project_folder` is `01_carm_level_detection` (197 copy, 87 reference,
4 exclude) under the copy rules of `../_plan/PLAN.md` section 2 rule 6, by the interrupted build of 2026-10-08 (run
wf_e27ebb09-038, which copied the files and wrote six documents) and the completing build of the same day (this file,
`MEMORY.md`, the remaining redactions, the removal in section 7) and the fix pass of the same day (the five real-frame
PNGs removed, section 2.1; `REGISTRY.md` and `CALIBRATION.md` added, section 2.2; one caption trimmed, section 8).
Totals counted over this folder after the fix pass: **1,993 files, 397,096,049 bytes without this file (1,994 with
it)**, of which 1,981 are copies (396,915,510 bytes) and 13 were written for this folder (this file included).

Source prefixes used below (history only): `ssn` = the laptop clone of the private repository `spinesurg-ct-nnunet` at
097933a (`C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/`), `sn` = `ssn/SchwingNet`, `ctsp` = the laptop clone of `CTSpinoPelvic1K` at 7ddfe38
(`C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/`), `Desktop` = `C:/Users/grego/OneDrive/Desktop/`.

## 1. What was copied, by folder

| folder | files | bytes | content |
|---|---:|---:|---|
| `(root)` | 7 | 144,732 | the eight documents of this folder (CLAUDE, README, MEMORY, STATUS, TODO, the three manifests) |
| `code/` | 88 | 1,469,162 | the 19 pipeline scripts and the two latency tools, `deploy_service.py`; each with a source header (`code/README.md`) |
| `docs/` | 45 | 1,160,402 | the model card, datasheet, deployment evidence, physics and linking line, sweep / count / guided documents, prior art, cine harness, the `spinesurg-ct-nnunet` CLAUDE and README, usage and claims JSONs |
| `docs/claim/` | 4 | 235,784 | the CLAIM 2020 and 2024 checklist forms |
| `docs/data_requests/` | 4 | 62,602 | the fluoroscopy data requests (e-mail addresses withheld) |
| `docs/external_reports/` | 7 | 1,598,745 | externally generated reports kept for reference (the C-arm validation roadmap, the FOV feasibility report, MULTI_XR, the dataset landscape PDFs, the 2D-3D-GS user guide) and their README |
| `docs/grid_records/` | 2 | 120,747 | the 2026-09-27 job record and the grid listing extracts this project relies on |
| `docs/handoff/` | 177 | 2,040,619 | the 2026-10-08 handoff: README, RESULTS_CATALOG, RECIPES, OPEN_QUESTIONS, RESEARCH_DIRECTIONS, DATASET_USAGE, LEAKAGE, INFRASTRUCTURE, MANUSCRIPTS, LITERATURE_STATE, GLOSSARY, CONTEXT_EXPORT (everything but `GREG_ONLY/`) |
| `docs/research/` | 18 | 2,742,116 | the verified deep-research dumps behind the prior-art and dataset documents (JSON and md) |
| `figures/` | 96 | 46,143,804 | the C-ArmLSpine gallery, results, survey and preview figures and the paired-sets figure |
| `manuscripts/schwingnet/` | 115 | 35,695,645 | paper 1 sources, sections, tables, atlas cards, claims ledger, revision logs, the review and camera-ready packets of 2026-09-27 and `packet_src/` |
| `manuscripts/superseded/` | 142 | 35,927,152 | the earlier C-arm drafts `rsnai/` and `focused/` (sources, PDFs, figures) with a README on their lineage |
| `manuscripts/talks/` | 1 | 13,608,289 | the private CNS 2026 deck v10 (never public) |
| `memory/` | 78 | 222,005 | the 78 memory notes with a status line (`MEMORY.md`) |
| `regulatory/` | 35 | 11,702,429 | the determinations, protocol drafts, forms and policies (`regulatory/README.md`) |
| `results/carmlspine_v2_lineage_2026-09-21/` | 8 | 151,073 | the v2-lineage cross-validation record (SUPERSEDED; kept so the 98.22 % is never quoted as current) |
| `results/physics/` | 86 | 557,066 | the physics-linking reproduction results (defects, recovery, regression, figures) |
| `results/schwingnet/` | 1,080 | 243,513,677 | the result files of paper 1: counting, coupling, eval gate, in-domain, coverage, arcs, learning curves, power, figure inputs, repairs, rigor fixes (the per-run coverage JSONs over 2 MB removed, section 7; the five window-probe input frames removed as imaging data on the fix pass, section 2.1; `transitional_registry/REGISTRY.md` and `auto_reference/CALIBRATION.md` added on the fix pass, section 2.2) |

The `(root)` row counts the seven documents that existed when this file was written; this file is the eighth. Files were copied with Python `shutil.copy2` (no symlink or junction followed; none exists in the folder). Three README files
under the copies (`docs/external_reports/README.md`, `manuscripts/superseded/README.md`,
`manuscripts/schwingnet/packet/packet_src/README.md`) were written for this folder, not copied.

## 2. Valuable material deliberately NOT copied, with the reason

### 2.1 Laptop-only files and folders (reference by path; the disposition's reason verbatim)

| source (history) | reason (`../_plan/DISPOSITION.tsv`) |
|---|---|
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/fluoro_requests_eml/ (11 .eml drafts)` | [carm r21; inventory: carm_detection/reference] Outlook drafts duplicating the markdown; carry recipient addresses |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_*.json (verified research dumps, 0.2 to 1.3 MB each)` | [carm r40; inventory: archive/reference] raw deep-research outputs behind the prior-art and dataset documents \|\| decision: same files as ssn r107 (copied once into 01/docs/research/) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/ {packet_src/, packet/, packet_cameraready/}` | [carm r47; inventory: carm_detection/reference] regenerable submission packets (89 MB each for packet and packet_cameraready) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/*.tif` | [carm r50,ssn r46; inventory: carm_detection/reference] TIFF exports 3.5 to 39 MB each (figure1.tif 39 MB over the 25 MB limit); regenerable from the PDFs |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/touched.json` | [carm r52,ssn r54; inventory: carm_detection/reference] 55 MB evaluation-gate touch record |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/ (main.tex, main_v2.tex, claims.tex, refs.bib, graveyard.tex, figures/)` | [carm r58; inventory: archive/reference] superseded drafts; main_v2 title page says Neurosurgery; refs.bib is shared by the QI paper \|\| decision: same folder as ssn r178-179 (copied once) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/VAIDYAS_IRB.pdf` | [carm r78,ctsp r41; inventory: exclude/exclude] another investigator's approved eProtocol export (IRB-21-10-4123) used only as the format template for the Protocol 1 draft \|\| decision: same file as ctsp r41; by path only |
| `C:/Users/grego/OneDrive/Desktop/IRB/Retrospective IRB PROTOCOL.pdf` | [carm r88; inventory: exclude/exclude] another investigator's arthroplasty quality protocol used as a template \|\| decision: another investigator's protocol used as a template; by path, consistent with VAIDYAS_IRB.pdf |
| `CTSpinoPelvic1K-1/hpr_determination_tool_revised_11_2021.pdf, hpr-guidance-activities-that-are-not-hpr-ada-update-4726.docx` | [ctsp r43; inventory: carm_detection/reference] blank WSU HPR tool and guidance; public forms |
| `CTSpinoPelvic1K-1/2D-3D-GS.zip (79 MB: CT .raw/.sta, Documents/Dejan_Tomazevic_MSc.pdf, Miccai2002_paper.pdf, 157 files)` | [ctsp r51; inventory: carm_detection/reference] registration benchmark data; over 25 MB |
| `CTSpinoPelvic1K-1/PIG/PIG_LEVELCHECK.pdf` | [ctsp r52; inventory: carm_detection/reference] Goswami 2020 IEEE Access (projection-based pose tracking, IOERT) - third-party literature |
| `CTSpinoPelvic1K-1/PIG/*.zip (CBCT_NOSoftTissue 46 MB, CBCT_SoftTissue 44 MB, CTscan_Applicator 43 MB, CTscan_Pig 48 MB, PlanarImages* 12 MB each, MatricesSoftTissue 5 KB)` | [ctsp r53; inventory: carm_detection/reference] pig CBCT/CT/planar data from the Goswami study; data |
| `C:/Users/grego/OneDrive/Desktop/2026 144 Schwing IRB Not HPR Determination 4.21.26.pdf` | [desk r1; inventory: carm_detection/copy] WSU IRB Not-HPR determination 2026-144 dated 2026-04-21 (13 pages); the hospital-testing plan needs it \|\| decision: byte-identical twin of 'IRB Not HPR Determination 4.21.26.pdf' in the CTSpinoPelvic1K-1 root (md5 38f5c700a1...), which is the copy taken under carm r74 / ctsp r39; recorded as a second path |
| `C:/Users/grego/OneDrive/Desktop/IRB Not HPR Determination 4.21.26.pdf` | [desk r32; inventory: carm_detection/reference] byte-identical duplicate of '2026 144 Schwing IRB Not HPR Determination 4.21.26.pdf' (md5 38f5c700a1...) \|\| decision: byte-identical twin; the copy is taken from the CTSpinoPelvic1K-1 root (carm r74) |
| `C:/Users/grego/OneDrive/Desktop/spine_study_protocol.pdf` | [desk r38; inventory: carm_detection/reference] 3-page protocol draft 2026-03-30 'Development of a Publicly Accessible, Deep Learning-Ready Clinical and Radiographic Dataset for Spine Surgery Outcomes' (PI Schwing, co-I Eltahawy); superseded by Desktop/IRB/spine_study_protocol.pdf (134943 B; retitled 'Creation of a Secure Multimodal Clinical and Radiographic Spine Surgery Dataset for Case-Control Research and Locally Hosted AI Development', sponsor Edelman) \|\| decision: the 2026-03-30 root draft; superseded by Desktop/IRB/spine_study_protocol.pdf (retitled, sponsor named), which ctsp r149 copies |
| `spinesurg-ct-nnunet:HANDOFF/RECIPES.md` | [grid r230; inventory: carm_detection/reference] how each result was produced on the grid, section 0 rules first |
| `spinesurg-ct-nnunet:HANDOFF/DATASET_USAGE.md` | [grid r231; inventory: carm_detection/reference] which weights are the SchwingNet model and their grid paths (section 1); what each dataset does |
| `spinesurg-ct-nnunet:docs/MODEL_REGISTRY.md` | [grid r233; inventory: carm_detection/reference] the registry design, commands, environment, the sixteen backfilled models |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet/` | [ssn r82; inventory: carm_detection/reference] Word packet of the review copy built 2026-09-25 15:42 (manuscript.docx, supplement.docx, cover letter, title pages, claim checklist, figures as TIFF) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/INVENTION_DISCLOSURE.md` | [ssn r120; inventory: carm_detection/reference] engineering disclosure (2026-09-18): five aspects A-E, claim scope, freedom to operate |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/{DISCLOSURE_MEMO,PATENT_PACKAGE}.md + provisional/ + disclosure_audit.json + disclosure_forensics.json + disclosure_evidence/ + research_patent_2026-09-18.json + research_registration_free_2026-09-18.json` | [ssn r121; inventory: carm_detection/reference] counsel memo, superseded patent package, the provisional package (SPECIFICATION 54 KB, CLAIMS, COVER_SHEET, FILING_CHECKLIST; FIG. 1-13 not drawn), the public-surface audit and its evidence |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tmp/` | [ssn r170; inventory: carm_detection/reference] 653 TRACKED scratch files (40 MB): coupling_check/ (job 40416411/38/41 outputs, meta_cv, proto_post), lcurve_local_census.py, lcurve_probe*.sh |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/age_sex_cache/` | [ssn r80; inventory: carm_detection/exclude] 19 cached per-source age/sex tables (35 MB); age_sex_by_source.json is the product |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_cameraready/` | [ssn r83; inventory: carm_detection/exclude] gitignored derived twin of packet/ with the name printed |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_build/ (other PDFs, logs, md, csl, reference.docx)` | [ssn r85; inventory: carm_detection/exclude] 16 earlier dated PDFs (09-24 to 09-25e), make_packet_*.log, pandoc csl files, manuscript.md/supplement.md intermediates |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/{main.pdf,supplement.pdf,main.log,supplement.log,schwingnet_tex-40416671.out,grep.exe.stackdump,logs/}` | [ssn r87; inventory: carm_detection/exclude] 2026-09-24 local compiles (7.1 + 4.9 MB) and build logs; superseded by packet_build 2026-09-27 |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/corpus/rs/rs_grp_oschome/go2432/data/realxray/carmlspine/images/test/case100_AP.png` (546,470 B) | [carm r51; fix pass 2026-10-08] a real radiograph frame of C-ArmLSpine (the first Surgio B51 set; 149 cases), the window probe's input mirrored from the grid under `corpus/`; copied by the build and removed on the fix pass because imaging data is never copied; on the grid at `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine/images/test/case100_AP.png` (`MANIFEST_GRID.md`, the `CEPH/data/realxray/` row); the probe's `REPORT.txt` and its 30 exported field/body strips stay in `results/schwingnet/window_probe/` |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/corpus/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta/images/train/A002_0000.png` (49,421 B) | [carm r51; fix pass 2026-10-08] a real radiograph frame of COBRA 2026 Elekta, the window probe's input mirrored from the grid under `corpus/`; copied by the build and removed on the fix pass because imaging data is never copied; on the grid at `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta/images/train/A002_0000.png` (`MANIFEST_GRID.md`, the `CEPH/data/realxray/` row); the probe's `REPORT.txt` and its 30 exported field/body strips stay in `results/schwingnet/window_probe/` |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/corpus/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta/images/train/A002_0089.png` (70,371 B) | [carm r51; fix pass 2026-10-08] a real radiograph frame of COBRA 2026 Elekta, the window probe's input mirrored from the grid under `corpus/`; copied by the build and removed on the fix pass because imaging data is never copied; on the grid at `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta/images/train/A002_0089.png` (`MANIFEST_GRID.md`, the `CEPH/data/realxray/` row); the probe's `REPORT.txt` and its 30 exported field/body strips stay in `results/schwingnet/window_probe/` |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/corpus/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta/images/train/A002_0178.png` (44,053 B) | [carm r51; fix pass 2026-10-08] a real radiograph frame of COBRA 2026 Elekta, the window probe's input mirrored from the grid under `corpus/`; copied by the build and removed on the fix pass because imaging data is never copied; on the grid at `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta/images/train/A002_0178.png` (`MANIFEST_GRID.md`, the `CEPH/data/realxray/` row); the probe's `REPORT.txt` and its 30 exported field/body strips stay in `results/schwingnet/window_probe/` |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/corpus/rs/rs_grp_oschome/go2432/data/realxray/deepfluoro/images/test/18-1109_004.png` (66,238 B) | [carm r51; fix pass 2026-10-08] a real radiograph frame of DeepFluoro, the window probe's input mirrored from the grid under `corpus/`; copied by the build and removed on the fix pass because imaging data is never copied; on the grid at `/rs/rs_grp_oschome/go2432/data/realxray/deepfluoro/images/test/18-1109_004.png` (`MANIFEST_GRID.md`, the `CEPH/data/realxray/` row); the probe's `REPORT.txt` and its 30 exported field/body strips stay in `results/schwingnet/window_probe/` |

### 2.2 Named in the plan or in the copied READMEs, never in a project folder

| source (history) | reason | where it lives |
|---|---|---|
| `ctsp/VAIDYAS_IRB.pdf` | another investigator's approved eProtocol export (IRB-21-10-4123), used only as the format template for the Protocol 1 draft | the laptop; the WSU IRB |
| `Desktop/IRB/Retrospective IRB PROTOCOL.pdf` | another investigator's arthroplasty quality protocol used as a template | the laptop |
| `Desktop/IRB/co-investigators.xlsx`, `Desktop/IRB/GREG/`, `Desktop/IRB/HAZEM/` | a co-investigators sheet and personal CITI completion records (personal and administrative) | the laptop |
| `ctsp/COMMERCIALIZATION.md` | the two-track commercial rule; Greg-only, never in a project folder (`../_plan/PLAN.md` section 2) | the public repository's clone (untracked) |
| `ssn/docs/INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md`, `PATENT_PACKAGE.md`, `provisional/`, `disclosure_*`, `research_patent_2026-09-18.json`, `research_registration_free_2026-09-18.json` | Greg's private filing material (invention disclosure, counsel memo, provisional package, public-surface audit) | the private repository at 097933a |
| `Desktop/private_ip/` | the signed invention-disclosure forms and the private filing package | the laptop |
| `Desktop/CTSP1K_private/proposals_backup_20260911/irb/EMAIL.md` | an e-mail draft carrying staff addresses; the plan beside it (`IRB_PLAN_2026-09-11.md`, `PROPOSAL_SHORT_2026-09-11.md`) is copied | the laptop |
| `Desktop/CTSpinoPelvic1K_coauthor_signoff.xlsx` | the dataset article's sign-off sheet: student names | the laptop |
| `ctsp/Untitled_Message.zip` | the zip itself; its four documents are extracted into `regulatory/carm_validation_plan_2026-09-21/` and its roadmap PDF is `docs/external_reports/C-Arm_Validation_Research_Plan_2026-09-20.pdf` (as the `ctsp` root copy) | the laptop |
| `ctsp/IRB_VinDr_2026-09-25.zip` | a zip of the folder copied as `regulatory/vindr_2026-09-25/` | the laptop |
| `ssn/docs/fluoro_requests_eml/` (11 `.eml`) | Outlook drafts duplicating the markdown requests; they carry recipient addresses | the private repository |
| `sn/figures/*.tif` | TIFF exports 3.5 to 39 MB each (`figure1.tif` 39 MB is over the 25 MB limit); regenerable from the PDFs copied in `figures/schwingnet/` | the private repository |
| `sn/packet/`, `sn/packet_cameraready/`, the rest of `sn/packet_build/` | the Word packets (89 MB each) and sixteen earlier dated PDFs, logs and pandoc files; the two final PDFs of 2026-09-27 and `packet_src/` are copied | the private repository (`packet_cameraready/` gitignored) |
| `sn/main.pdf`, `supplement.pdf`, `*.log`, `logs/`, `schwingnet_tex-40416671.out` | 2026-09-24 local compiles and build logs, superseded by the 2026-09-27 packets | the private repository |
| `sn/results/age_sex_cache/` (19 files, 35 MB) | cached per-source age and sex tables; `results/schwingnet/age_sex_by_source.{json,md}` is the product | the private repository |
| `sn/results/eval_gate/touched.json` (55 MB) | over the 25 MB limit; the evaluation-gate touch record | the private repository |
| `ssn/tmp/` (653 tracked scratch files, 40 MB) | scratch outputs of the coupling check and lcurve probes; the results they fed are in `results/schwingnet/` | the private repository |
| `ssn/paper/rsnai/web/index.html` and every LaTeX build product (`.aux`, `.bbl`, `.fdb_latexmk`, `.fls`, `.log`, `.out`, `.toc`) | project 99 by path; regenerable with the copied `build.sh` | the private repository |
| `Desktop/spine-detector/dist/*.onnx` (84, 84, 42, 42 MB) | model exports (weights) and over 25 MB | the laptop; the private `OpenSpineConsortium/spine-detector` |
| `ctsp/2D-3D-GS.zip` (79 MB), `ctsp/PIG/*.zip`, `ctsp/PIG/PIG_LEVELCHECK.pdf` | imaging data over 25 MB; third-party literature | the laptop; the Ljubljana server; Ceph `data/ljubljana` |
| `ctsp/hpr_determination_tool_revised_11_2021.pdf`, `hpr-guidance-activities-that-are-not-hpr-ada-update-4726.docx` | listed by the disposition as reference; the same two public forms are copied once into `regulatory/wsu_dmc_forms/` under shorter names | the laptop; the WSU IRB site |
| `ssn/HANDOFF/GREG_ONLY/` | never copied into `spine-program` (`../_plan/PLAN.md` section 2 rule 3) | the laptop only |
| the live memory folder `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/` | the redacted `HANDOFF/context/` copies were used instead, as the plan requires | the laptop |
| every `.pt`, `.npz`, `.npy`, `.nii.gz`, `.h5`, `.dcm` the disposition names | weights and imaging data are never copied; each is a grid row of `MANIFEST_GRID.md` | the grid |
| `sn/results/transitional_registry/` (`REGISTRY.md`, `registry.csv`, `registry.json`, the seven per-stream folders, `contact_sheets/`) | named by the copy row [carm r51] but routed to project 06 by rows [ssn r68, r69] (the one transitional registry of 2026-09-24: 6,131 rows, 6,108 persons); the build copied none of it; the fix pass copied `REGISTRY.md` alone (57,857 B, tracked at 097933a, last changed 8d6a4f4 2026-09-24) into `results/schwingnet/transitional_registry/` because step S6 stratifies by transitional status | `../06_transitional_ct_census/results/transitional_registry/`; the private repository at 097933a |
| `sn/results/auto_reference/` (`CALIBRATION.md`, `calibration.json`, `lists/`, `readerC/`, `readersAB/`) | named by the copy row [carm r51] but routed to project 02 by row [ssn r74] (the automated reference standard's calibration and its reader lists; readers A, B and C are programs); the build copied none of it; the fix pass copied `CALIBRATION.md` alone (18,447 B, tracked at 097933a, last changed 6b25ea5 2026-09-24) into `results/schwingnet/auto_reference/` | `../02_transitional_naming_truth/results/paper2/auto_reference/`; the private repository at 097933a |
| `Desktop/CTSP1K_private/proposals_backup_20260911/irb/CTSpinoPelvic1K_preprint.pdf` (1,168,984 B, 2026-09-11) | named by the copy row [ctsp r112] beside `IRB_PLAN.md`; a 2026-09-11 copy of the dataset article's preprint, which is project 03's (posted as arXiv 2609.22760 v1 on 2026-09-19, `../03_ctspinopelvic1k_dataset/manuscripts/arxiv_final_draft_9_19_2026.pdf`); not a C-arm document, so not copied here | the laptop; arXiv 2609.22760; project 03 |

### 2.3 Repository files referenced, not copied (the files that matter are named in `MANIFEST_CODE.md`)

| source (history) | reason |
|---|---|
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/level_prototype.py` | [carm r3; inventory: carm_detection/reference] the gated reference inference the latency parity gate is defined against |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ {sweep_map.py, needle_confirm.py, acquisition.py, validate_guided.py, guided_console.py, alphabet_couple.py, count_from_sacrum_eval.py, eval_gate.py, patient_keys.py, eval_runtime_cost.py, fluorocap_infer.py, fluorocap_anchor.py, carmlspine_*.py, case134_sweep.py, drr_register.py, realxray_eval.py, or_recall_curves.py, stats_compare.py, model_registry.py, device_fit.py, device_style.py, device_census.py, device_physics.py, devcorpus_build.py, devcorpus_train.py, bournemouth_qf_eval.py, inspect_dicom_tree.py, pipeline_state.py}` | [carm r4; inventory: carm_detection/reference] live in the private repo at 097933a; name them in MANIFEST_CODE.md rather than copying |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/slurm/ {cine_eval.sh, cine_latency.sh, carmlspine_*.sh, devcorpus*.sh, device_*.sh, guided_validate.sh}` | [carm r8; inventory: carm_detection/reference] job scripts in the private repo |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/ {tools/, slurm/}` | [carm r54; inventory: carm_detection/reference] figure and table builders, compile and check scripts, in the private repo |
| `HF private repo gregoryschwingmdphd/level-id-weights (detector.pt = detect_v5z_epoch25, level_model.pt = M19, recurrent_head.pt, registry.json; registry/<name>/<sha> mirror)` | [carm r108; inventory: carm_detection/reference] the off-cluster weight mirror and the service's weight source |
| `C:/Users/grego/OneDrive/Desktop/spine-detector/dist/detect_v3_640_fp32.onnx; detect_v4_1024_fp32.onnx; v11m_1024_v4_fp16.onnx; v11m_640_v4_fp16.onnx` | [inv3 r52; inventory: carm_detection/reference] ONNX exports of 2026-09-12 (84, 84, 42, 42 MB) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/Makefile` | [ssn r3; inventory: carm_detection/reference] make targets for nnU-Net stages, physics reproduction, polypose checks |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/.gitattributes` | [ssn r10; inventory: carm_detection/reference] declares SchwingNet/results/fig6/frozen/** and verification/** -text (byte-exact frozen truth files, CRLF) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tools/` | [ssn r48; inventory: carm_detection/reference] 80 scripts: results_macros.py (the \RESULT build), figure1..5 builders, figS_supplement.py, make_supp_*_table.py, make_packet.py, check_limits.py, gen_claim_checklist.py, contribution_matrix.py, fig6_* (paper-2 gate), reader_e_* (reader E), stats_review*_recompute.py, verification_worklist.py |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/slurm/` | [ssn r49; inventory: carm_detection/reference] 101 grid scripts: compile.sh (texlive 2020, flock), contrib_*, coverage_arms_*, lcurve_*, name_fill_*, film_ncurve_*, fig6_*, reader_e_*, rare_*, rc_*, g3_split.sh, tables_check.sh |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/carmlspine_*.py (30 files) + case134_*.py + carm_sweep.py + carm_denominator_repair.py + carm_miss_diagnostic.py + carm_variant_survey.py` | [ssn r123; inventory: carm_detection/reference] C-ArmLSpine (148 cases, FIRST Surgio-B51): reading, CBCT->NIfTI, pose by registration, projected level truth, fold dirs, eval, census, QC panels, the 302-frame CBCT spin as a real oblique set, the denominator repair and miss diagnostic |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/realxray_*.py (12) + lcurve_*.py (5) + indomain_*.py (9) + or_crossdev_*.py (7) + or_lodo_rescore_outline.py + or_recall_curves.py + or_position_prior.py + g3_detector.py + g3_leak_intersect.py + g3_split_verify.py + make_split.py + consolidate_splits.py + make_fold_banks.py` | [ssn r124; inventory: carm_detection/reference] real-frame detector training/scoring on COBRA2026, DeepFluoro, Geneva, C-ArmLSpine; the learning curves of Figure 5; cross-device naming; the G3 person split and its adversarial checks |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/{arc_angle_set,arc_curve_compare,arc_prior_check,arc_recall_eval,arc_unseen_subjects,pose_arc,pose_arc_proof,pose_pool_audit}.py` | [ssn r125; inventory: carm_detection/reference] recall against C-arm angle on unseen subjects; synthetic AP->lateral arcs per device |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/{make_context_crops,train_level_backbone,train_level_classifier,recurrent_order,head_mixed_length,head_dual,stc_head,train_stc_head,message_fusion,ordinal_spine_decode,decode_sequence}.py` | [ssn r127; inventory: carm_detection/reference] the level encoder and recurrent head training harness; the crop builder that draws ONE split over people and refuses unkeyed cases |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/{detect_films,detector_chain_report,detector_failures,detector_quality,detector_robustness,build_sacrum_dataset,make_zoom_dataset,check_fluoro_degrade,wholespine_build,wholespine_train,wholespine_eval,wholespine_figures,wholespine_panels,wholespine_survey,thoracic_xr_eval,thoracic_xr_prep,thoracic_xr_report,thoracic_xr_fetch,draw_film_boxes,zoom_crop_figure}.py` | [ssn r128; inventory: carm_detection/reference] the vertebra / sacrum / C2 detectors on films and real frames; failure anatomy; AASCE thoracic test |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/{needle_confirm,fiducial_walk,acquisition,guided_console,validate_guided,link_probe,test_masked_link,link_surface_figure,sweep_by_region,sweep_coverage,sweep_declined,sweep_per_level,sweep_spacing_curve,counting_brief,recovery_brief,reproduce_physics,collect_physics_results,physics_figures,physics_validate,fluoro_physics,render_physics_drr,param_census,path_census,frame_levels,window_probe}.py` | [ssn r129; inventory: carm_detection/reference] the sweep / count / confirm / guided-acquisition line and the physics-linking reproduction |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/{claims_check,claims_fill,rsnai_table1,bib_audit,bib_apply_resolved,wordcount_tex,disclosure_audit,disclosure_forensics}.py` | [ssn r130; inventory: carm_detection/reference] manuscript machinery of the superseded main_v2 draft; bibliography audit; the public-surface audit |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fig*.py (about 45 files: fig1_style, fig1a_problem_lateral, fig1d_algorithm_panorama, fig2_pipeline, fig6_arch, fig3_panorama, fig2_heldout_embed, fig2_occlusion_clean, fig3_detection_grid, fig3_example_cobra_v3, figure1_panels, fig_carmlspine_*, fig_data_flow, fig_dataset, fig_detector_arch, fig_learning, fig_manifold, fig_modality_vs_device, fig_network, fig_separation_hd, fig_row*, fig_story*) + gallery_figure.py + gallery_panels.py + make_formation_figure.py + render_feature_cartoon.py + contact_sheet.py + render_*.py + _figfit.py` | [ssn r131; inventory: carm_detection/reference] figure builders for SchwingNet (fig1*, fig2_*, fig3_*, gallery_*, fig_learning, fig_manifold) and for the superseded Figure-1 story rows of main/main_v2 |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/slurm/{allspine_v9_bank,allspine_v9_keys,allspine_v9_train,allspine_v9_a5,allspine_v9_submit,allspine_v8_*,recurrent_head,head_mixed,ctx_*,carmlspine_cv_v9init,carmlspine_cv_v9init_prerepair,carmlspine_cv_day_v9,carmlspine_*(28),realxray_*(16),or_*(16),arc_*(5),lcurve*,d1_*,g3_detector,sacrum_detector,wholespine_*,thoracic_xr_*,cine_eval,cine_latency,carm_sweep_case39,carm_sweep_regress134,case134_*,eval_gate,eval_leaks,eval_leaks_gpu,gate_recheck,checkpoint_lineage,claims_check,claims_now,common_test,eval_calibration,eval_error_taxonomy,level_selective}.sh` | [ssn r148; inventory: carm_detection/reference] the jobs behind the shipped model (v9 bank/keys/train), the C-ArmLSpine CV and repairs, the real-frame detectors, the arcs and learning curves, the evaluation gate runs, the cine jobs (untracked) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/slurm/{sweep_*(16),count_*(5),needle_*,fiducial_walk,physics_*(9),link_ab,link_probe,step_jitter,story_rows*(8),guided_validate,repair_at_operating_point,reproduce_feasibility,reproduce_all,feas_claims,field_ablation,field_recover,strict_fov,surgeon_benefit,window_ablation,window_probe,resolution_ladder,geometry_sweep,recover_matrix,report_final,status_arms}.sh + paths2_cases.txt + l6_cases.txt` | [ssn r149; inventory: carm_detection/reference] the sweep / count / confirm / physics jobs (sweep_v3 is the only sweep on the right field size) |

### 2.4 Grid paths referenced (each is a row of `MANIFEST_GRID.md`)

| path | what (disposition) |
|---|---|
| `grid:HOME /wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` | [carm r91; inventory: carm_detection/reference] the naming detector of the reported stack (YOLO11m-pose, four corners, conf 0.35) |
| `grid:HOME /wsu/home/go/go24/go2432/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` | [carm r92; inventory: carm_detection/reference] the v9 level encoder (ResNet-18, two-channel stem, 27 classes) |
| `grid:HOME /wsu/home/go/go24/go2432/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt (+ .arch.json)` | [carm r93; inventory: carm_detection/reference] the recurrent head of the reported stack (BiGRU over 2-9 bodies, no alphabet loss) |
| `grid:HOME /wsu/home/go/go24/go2432/spine-detector/runs/realxray/ {rx_lodo_carmlspine_1024, rx_pooled_1024}/weights/best.pt` | [carm r94; inventory: carm_detection/reference] the sacrum/vertebra detector (C-ArmLSpine never seen) and its pooled twin |
| `grid:HOME /wsu/home/go/go24/go2432/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt and /wsu/home/go/go24/go2432/model_night/heads_carm/head_cv{k}_v9init.pt (+ cvday)` | [carm r96; inventory: carm_detection/reference] the fine-tuned fold models behind Table 3 (v9init); the un-suffixed v2-init files beside them are refused by the gate |
| `grid:HOME /wsu/home/go/go24/go2432/model_registry/ (registry.jsonl 106 lines, aliases/, <sha>/ store) and /wsu/home/go/go24/go2432/mlflow/mlflow.db` | [carm r97; inventory: carm_detection/reference] the content-addressed weight store and ledger; the HF mirror is gregoryschwingmdphd/level-id-weights (private) |
| `grid:CEPH /rs/rs_grp_oschome/go2432/data/realxray/ (carmlspine, carmlspine_sweep, carmlspine_crops, carmlspine_cv*, carmlspine_pre_repair_2026-09-23*, cobra_elekta + _v2 _v3 _ap45 _g3test _smoke, deepfluoro, geneva_hip, bournemouth_qf/raw, pelvis_landmarks, view_census.json)` | [carm r99; inventory: carm_detection/reference] the real-frame banks behind every C-arm number; carmlspine summary.json: 299 frames, 149 cases, test 28, boxes per level L1 267 to sacrum 295, T12 63, T11 3 |
| `grid:CEPH /rs/rs_grp_oschome/go2432/data/or_ready/ (devices/ with 8 cards incl. surgio_b51_dr/raw/display and varian_halcyon, lodo/, audit/, eval_gate/, indomain/, lcurve/, arc/, coverage/, crossdev/, devlodo/, devpool/, fig3_detection*, fig4_pairs*, film_ncurve/, learning*, corpus_manifold/, auto_reference/)` | [carm r100; inventory: carm_detection/reference] the OR-readiness result tree; lodo/rescore_outline.md is the 90.6 / 83.9 % source; no cine/ subfolder exists |
| `grid:CEPH /rs/rs_grp_oschome/go2432/data/external/fluoro_video/ (clips/ with REPORT.md, manifest.json, clips.csv, about 20 clip folders; youtube/, pmc/, commons/, vimeo/, github/, ajr/, dysphagiabank_unm/, work/)` | [carm r102; inventory: carm_detection/reference] the public fluoroscopy clip screening set produced by tools/fluoro_video; never scored |
| `grid:CEPH /rs/rs_grp_oschome/go2432/data/cobra2026/ (cases/, COBRA_COMPLETE.md, overviews)` | [carm r104; inventory: carm_detection/reference] COBRA2026 692 of 692 cases (771 GB per DATASET_USAGE 2.3); 145 Elekta cases in banks, 225 Varian never exported |
| `grid:HOME /wsu/home/go/go24/go2432/bench/ {latency.json, runtime_cost_workstation.json, fig_runtime_workstation.png/.pdf}` | [carm r105; inventory: carm_detection/reference] the only latency records: latency.json 2026-09-13 (V100 detector 22.9 ms, level model 2.3 ms; older models) and the contended workstation run of 2026-09-22; no runtime_cost.json |
| `grid:HOME /wsu/home/go/go24/go2432/model_night/guided/ {calib, far, main, near, rot, sloppy} and model_night/fiducial/ {ctsp_clamp, ctsp_skip_open, ctsp_skip_open_ext, ts_skip_open, ts_skip_open_ext}` | [carm r106; inventory: carm_detection/reference] the guided-loop corpus arms (job 40376577) and the fiducial-walk runs the QI paper quotes |
| `grid:CEPH /rs/rs_grp_oschome/go2432/data/or_ready/cine/` | [carm r107; inventory: carm_detection/reference] ABSENT (ls 2026-10-08): records that no cine inference, tracking or latency run has ever happened |
| `/rs/rs_grp_oschome/go2432/data/deepfluoro_h5/raw/deepfluoro` | [grid r29; inventory: carm_detection/reference] DeepFluoro H5 release (6 cadaver specimens, 366 frames) plus ann/ img/ |
| `/rs/rs_grp_oschome/go2432/data/deepfluoro_vendor` | [grid r30; inventory: carm_detection/reference] vendor DICOM deposit, 2,659 frames + 19 CT |
| `/rs/rs_grp_oschome/go2432/data/carmlspine` | [grid r31; inventory: carm_detection/reference] C-ArmLSpine, the real intraoperative test set of paper 1 |
| `/rs/rs_grp_oschome/go2432/data/realxray` | [grid r32; inventory: carm_detection/reference] 23 real-frame banks with projected labels (device banks, folds, sweeps) |
| `/rs/rs_grp_oschome/go2432/data/realxray_work` | [grid r33; inventory: carm_detection/reference] export work dirs geneva_hip and deepfluoro |
| `/rs/rs_grp_oschome/go2432/data/cobra2026` | [grid r34; inventory: carm_detection/reference] COBRA2026, 692 cases, 375,618 projections, Elekta + Varian |
| `/rs/rs_grp_oschome/go2432/data/geneva_hip_src` | [grid r35; inventory: carm_detection/reference] the unseen-device test (BV Pulsera phantom, 116 frames) |
| `/rs/rs_grp_oschome/go2432/data/ljubljana` | [grid r36; inventory: carm_detection/reference] 2D-3D-GS gold standard, 18 frames, PIXIUM 4600 |
| `/rs/rs_grp_oschome/go2432/data/spinesac` | [grid r37; inventory: carm_detection/reference] sawbone C-arm frames with no bone truth and no licence |
| `/rs/rs_grp_oschome/go2432/data/external` | [grid r40; inventory: carm_detection/reference] fluoro_video public clips |
| `/rs/rs_grp_oschome/go2432/data/or_ready` | [grid r42; inventory: carm_detection/reference] the OR-readiness results root behind paper 1 |
| `/rs/rs_grp_oschome/go2432/data/fig6` | [grid r43; inventory: carm_detection/reference] paper-2 (LevelCheck) Figure 6 material |
| `/rs/rs_grp_oschome/go2432/data/figure1` | [grid r44; inventory: carm_detection/reference] Figure 1 material |
| `/rs/rs_grp_oschome/go2432/model_night` | [grid r46; inventory: carm_detection/reference] DeepFluoro anchor rounds of 2026-09-21 |
| `/rs/rs_grp_oschome/go2432/data/outline_conv` | [grid r77; inventory: carm_detection/reference] C-ArmLSpine outline conversions |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` | [grid r113; inventory: carm_detection/reference] the private repository checkout, L6_Class at 4e3fe93862673e28613f7521d4c146c03a9dd405 |
| `/wsu/home/go/go24/go2432/spine-detector/runs/realxray/rx_lodo_carmlspine_1024` | [grid r136; inventory: carm_detection/reference] the SchwingNet sacrum/vertebra detector weights/best.pt, C-ArmLSpine never seen |
| `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` | [grid r139; inventory: carm_detection/reference] the level bank rung_1.npz 5,449,315,625 B, meta.json 73,837 B, runs/model_rung_1_aug2.pt 44,824,746 B (the SchwingNet encoder) |
| `/wsu/home/go/go24/go2432/allspine_v7_fov96_ctx` | [grid r141; inventory: carm_detection/reference] v7 bank, the base of the fold banks and of 57 holdout references |
| `/wsu/home/go/go24/go2432/carm_cvmix0_fov96_ctx` | [grid r169; inventory: carm_detection/reference] fold bank k=0 plus runs/model_rung_1_ft_cv0(_v9init)_aug2.pt and result JSONs |
| `/wsu/home/go/go24/go2432/carm_cvdaymix0_fov96_ctx` | [grid r170; inventory: carm_detection/reference] day-grouped fold banks k=0..2 and carm_cvdaymix0_v9_fov96_ctx |
| `/wsu/home/go/go24/go2432/carm_mix_fov96_ctx` | [grid r171; inventory: carm_detection/reference] mixed C-ArmLSpine bank; with carm_fov96_ctx carm_cv0..4_{drr,fov96_ctx} carm_cvday0..2_{drr,fov96_ctx} carm_drr |
| `/wsu/home/go/go24/go2432/carm_base_cache` | [grid r172; inventory: carm_detection/reference] regenerable cache; carm_base_cache_v9 beside it |
| `/wsu/home/go/go24/go2432/model_registry` | [grid r173; inventory: carm_detection/reference] the content-addressed weight store, registry.jsonl 106 lines, 79 aliases, mlflow_runs.jsonl |
| `/wsu/home/go/go24/go2432/mlflow` | [grid r174; inventory: carm_detection/reference] MLflow SQLite mlflow.db 1,028,096 B and artifacts/ |
| `/wsu/home/go/go24/go2432/model_night` | [grid r175; inventory: carm_detection/reference] the HOME results root: PIPELINE_STATE.md RESULTS.md CHAIN_LEDGER.tsv XRAY_DATASET_USAGE.md anomaly_manifest/ heads_carm/ (36 files) competitors/ benchmark_cina/ count_*/ detector_* json logs/ |
| `/wsu/home/go/go24/go2432/model_night/heads_carm` | [grid r176; inventory: carm_detection/reference] fold heads head_cv{0..4}(_v9init).pt head_cvday{0..2}(_v9init).pt head_mix.pt head_realonly.pt with .arch.json and mixed_cv*.json |
| `/wsu/home/go/go24/go2432/scaling` | [grid r181; inventory: carm_detection/reference] subset banks s000_r100 s025_r100 s050_r100 s100_r000 s100_r025 s100_r050 s100_r100 cut from the deleted v2 bank |
| `/wsu/home/go/go24/go2432/scaling_curves` | [grid r182; inventory: carm_detection/reference] cross/ fig_scaling_curves.pdf fig_scaling_curves.png scaling_devices.json scaling_fewshot.json |
| `/wsu/home/go/go24/go2432/COBRA_dataset_paper.pdf` | [grid r212; inventory: carm_detection/reference] the COBRA dataset paper (7,084,212 B, 2026-09-21) and bpex_ad2baa.pdf 1,916,673 B |
| `grid HOME ~/spine-detector` | [inv3 r91; inventory: carm_detection/reference] live detector tree: .git 2026-09-12, data/ 2026-09-20, runs/ 2026-09-24, dist, onnx_out, weights, logs, yolo11m-pose.pt; 382 GB per the 2026-09-19 du |
| `grid Ceph /rs/rs_grp_oschome/go2432/data/realxray` | [inv3 r97; inventory: carm_detection/reference] carmlspine (+crops, cv, cv_prerepair, cvday, cvday_prerepair, cvfill, multi, sweep, pre_repair_2026-09-23 and its crops), cobra_elekta (+ap45, g3test, smoke, v2, v2_ap45, v3), deepfluoro, geneva_hip, pelvis_landmarks, bournemouth_qf, view_census.json |

## 3. Redactions made in the copies (by kind, never by value)

What was changed, file by file, is in the note column of section 8; this section groups it. Nothing personal remains: the
final sweep of the folder (2026-10-08) finds no personal mail domain, no roster student name or username, no phone number
other than DOI fragments, and no address of a researcher or staff member. Institutional addresses kept on purpose:
`go2432@wayne.edu` and `go2432@grid.wayne.edu` (Greg's grid account), `IRBQuestions@wayne.edu`, `hpc@wayne.edu`,
`PHI-report@physionet.org`, and the public information addresses of two vendors and one foundation in the fluoroscopy
source scan.

### 3.1 E-mail addresses, phone numbers, names and account ids withheld in text copies

| copy | withheld (count) |
|---|---|
| `docs/DATASHEET.md` | [e-mail withheld] x1 |
| `docs/FLUORO_VIDEO_SOURCES_2026-09-26.md` | [e-mail withheld] x3 |
| `docs/FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md` | [e-mail withheld] x43, [phone withheld] x25 |
| `docs/data_requests/FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md` | [e-mail withheld] x2 |
| `docs/data_requests/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md` | [e-mail withheld] x34, [phone withheld] x8 |
| `docs/data_requests/balgrist_data_request_2026-09-21.md` | [e-mail withheld] x3 |
| `docs/handoff/INFRASTRUCTURE.md` | [accessid withheld] x1 |
| `docs/handoff/LITERATURE_STATE.md` | [e-mail withheld] x23 |
| `docs/handoff/MANUSCRIPTS.md` | withheld x3, [student x2 |
| `docs/handoff/RECIPES.md` | [student x1 |
| `docs/handoff/RESEARCH_DIRECTIONS.md` | [e-mail withheld] x1 |
| `docs/handoff/context/grid-access-list-gate.md` | [accessid withheld] x1, withheld x1, [student x1 |
| `docs/handoff/context/grid-ceph-volume-oschome.md` | [accessid withheld] x1 |
| `docs/handoff/context/learned-formation-refuted-calibrate-instead.md` | [name withheld] x2, withheld x1 |
| `docs/handoff/context/panjabi-1991-page-892.md` | [phone withheld] x1 |
| `docs/handoff/context/rib-qc-gates-never-block-lstv.md` | two students x1 |
| `docs/handoff/context/wsu-library-access-cutoff.md` | [e-mail withheld] x1, [phone withheld] x3 |
| `docs/handoff/context/xray-corner-detector-status.md` | a student x1 |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | [e-mail withheld] x1 |
| `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md` | [student x1 |
| `docs/handoff/working_notes/topic4_manuscripts.md` | withheld x3, [student x2 |
| `docs/handoff/working_notes/topic5_operating_here.md` | [accessid withheld] x1 |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | withheld x1 |
| `docs/research/BIB_RESOLVE_2026-09-22.json` | [e-mail withheld] x1, withheld x1 |
| `docs/research/research_datasets_fourth_pass_verified_2026-09-22.json` | [e-mail withheld] x64, [phone withheld] x1 |
| `docs/research/research_datasets_missed_verified_2026-09-21.json` | [e-mail withheld] x8 |
| `docs/research/research_datasets_third_pass_verified_2026-09-21.json` | [e-mail withheld] x4 |
| `docs/research/research_paired_ct_projection_verified_2026-09-21.json` | [e-mail withheld] x4 |
| `manuscripts/schwingnet/atlas/README.md` | [e-mail withheld] x2 |
| `manuscripts/schwingnet/atlas/dataset.json` | [e-mail withheld] x3 |
| `manuscripts/schwingnet/atlas/model.json` | [e-mail withheld] x3 |
| `manuscripts/schwingnet/atlas/update_cards.py` | [e-mail withheld] x5 |
| `manuscripts/schwingnet/packet/packet_src/build/cover_letter.md` | [e-mail withheld] x1 |
| `manuscripts/schwingnet/packet/packet_src/build/full_title_page.md` | [e-mail withheld] x1, [phone withheld] x1 |
| `manuscripts/schwingnet/packet/packet_src/front_matter.json` | [e-mail withheld] x1, [phone withheld] x1 |
| `manuscripts/superseded/focused/_drafts/deployment.tex` | [e-mail withheld] x1 |
| `manuscripts/superseded/rsnai/main.tex` | [e-mail withheld] x1 |
| `manuscripts/superseded/rsnai/main.tex.pre-restructure` | [e-mail withheld] x1 |
| `memory/grid-ceph-volume-oschome.md` | [accessid withheld] x1 |
| `memory/learned-formation-refuted-calibrate-instead.md` | [phone withheld] x1, [name withheld] x2, withheld x3 |
| `memory/wsu-library-access-cutoff.md` | [e-mail withheld] x1, [phone withheld] x3 |
| `memory/xray-corner-detector-status.md` | a student x1 |
| `regulatory/protocols_2026-09/IRB_PLAN_2026-09-11.md` | [e-mail withheld] x8 |
| `regulatory/vindr_2026-09-25/00_cover_note_to_IRB.md` | [phone withheld] x1 |
| `regulatory/vindr_2026-09-25/HPR_determination_VinDr-SpineXR_draft.md` | [phone withheld] x2 |

Kinds, as the earlier pass applied them: researcher and vendor contact addresses in the data-request drafts, the fluoroscopy
source scans, the literature state and the research dumps; Greg's personal e-mail (the datasheet owner line, the atlas cards,
the superseded drafts' corresponding-author lines, `main.tex.pre-restructure`); Greg's phone number in the packet front
matter and the VinDr cover note; a WSU library staff contact; a Panjabi reprint source's phone; one C&IT administrator's
access id (`grid-ceph-volume-oschome`, `grid-access-list-gate`); a DMC neurosurgeon's name and the Anatomical Gift Program
contact in `learned-formation-refuted-calibrate-instead` (both copies); a student's first name in
`xray-corner-detector-status` (both copies); two students' usernames in `rib-qc-gates-never-block-lstv`.

### 3.2 Student names and usernames withheld by the completing pass

| copy | edits | what |
|---|---:|---|
| `docs/handoff/MANUSCRIPTS.md` | 1 | Schwing; Schehr; [10 student co-author names withheld; `ctsp:paper/mpda/title_pa |
| `docs/handoff/working_notes/topic4_manuscripts.md` | 1 | Schwing; Schehr; [10 student co-author names withheld; `ctsp:paper/mpda/title_pa |
| `docs/handoff/MANUSCRIPTS.md` | 1 | \| Digital Only \| [student authors withheld] \| |
| `docs/handoff/MANUSCRIPTS.md` | 1 | \| Digital Only \| [student author withheld] \| |
| `docs/handoff/working_notes/topic4_manuscripts.md` | 1 | \| Digital Only \| [student authors withheld] \| |
| `docs/handoff/working_notes/topic4_manuscripts.md` | 1 | \| Digital Only \| [student author withheld] \| |
| `docs/research/BIB_RESOLVE_2026-09-22.json` | 1 | (Schwing, Schehr, [10 student names withheld], Ismoilov, Alnabahneh) |
| `docs/research/BIB_RESOLVE_2026-09-22.json` | 1 | Schwing, Gregory and Schehr, Ashley and others |
| `manuscripts/schwingnet/refs.bib` | 2 | Schwing, Gregory and Schehr, Ashley and others |
| `manuscripts/schwingnet/refs_corrections.bib` | 2 | Schwing, Gregory and Schehr, Ashley and others |
| `manuscripts/superseded/rsnai/refs.bib` | 1 | Schwing, Gregory and Schehr, Ashley and others |
| `manuscripts/schwingnet/atlas/dataset.json` | 1 | Schwing G, Schehr A, et al. |
| `manuscripts/schwingnet/atlas/model.json` | 1 | Schwing G, Schehr A, et al. |
| `manuscripts/schwingnet/atlas/update_cards.py` | 1 | Schwing G, Schehr A, et al. |
| `manuscripts/schwingnet/packet/packet_src/front_matter.json` | 1 | Schwing G, Schehr A, et al. |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 1 | ([per-student usernames and counts withheld; the private ledgers hold them: 11 r |

The ten student annotators of the dataset article (`ctsp:morphometrics/annotator_names.csv`; the two radiology residents,
Ashley Schehr, Greg and the faculty sponsor are not students and are kept) were withheld from the 14-author lists, the
CNS abstract rows, the Zenodo creator lists in the bibliography files (`author = {Schwing, Gregory and Schehr, Ashley and
others}`; the full creator list is the Zenodo record 10.5281/zenodo.22797014 and the repository's `SchwingNet/refs.bib` at
097933a) and the atlas citation strings, and the per-student annotation tally of `topic6` was replaced by a bracketed note.

### 3.3 Binary copies re-written on copy

| copy | source bytes | copy bytes | what changed (checked by text extraction on 2026-10-08) |
|---|---:|---:|---|
| `manuscripts/superseded/focused/_drafts/deployment.pdf` | 114,475 | 138,063 | Greg's personal e-mail on the title page removed; phones found are DOI fragments |
| `manuscripts/superseded/rsnai/main.pdf` | 258,798 | 293,411 | Greg's personal e-mail on the title page removed |
| `regulatory/wsu_dmc_forms/dmc-research-review-process-and-instructions-revised-2022.pdf` | 732,103 | 747,011 | two DMC staff e-mail addresses removed; the office phone numbers (institutional) kept |
| `regulatory/protocol_2026-03/Data_Collection_Tool.docx` | 18,271 | 17,066 | document information (creator, last modified by) cleared; text unchanged |
| `regulatory/protocol_2026-03/spine_study_protocol.docx` | 30,760 | 28,558 | document information cleared; text unchanged |
| `regulatory/vindr_2026-09-25/00_cover_note_to_IRB.docx` | 13,038 | 13,820 | one personal phone number removed; the institutional addresses kept |
| `regulatory/hpr_2026-144/HPR_2026-144_determination_2026-04-21.pdf` | 2,088,991 | 2,212,767 | two personal phone numbers struck in the page text and form fields of the bound-in determination tool; the IRB office phone and Greg's institutional address kept |
| `regulatory/hpr_2026-269/HPR_tool_filled_2026-05-31.pdf` (source 437,030 B, copy 532,178 B), `regulatory/vindr_2026-09-25/01_HPR_Determination_Tool_VinDr-SpineXR_2026-09-25.pdf` (560,189 to 522,962 B) | see section 8 | see section 8 | personal phone numbers struck in page text and form-field values (two in the filled tool, one in the VinDr tool); no personal e-mail address was in either source by text extraction, only Greg's institutional one, kept. `HPR_tool_as_filed_2026-08-28.pdf` is byte-identical to its source |
| `regulatory/carm_validation_plan_2026-09-21/WSU_Body_Bequest_contact_page.pdf` | inside a zip | 2,051,761 | the named contact withheld (`regulatory/README.md`) |
| `regulatory/wsu_dmc_forms/x-ray_machine_registration_form.docx, 01-05_flexible_review_and_oversight.docx` | `.doc` originals | 72,268; 34,783 | converted from `.doc`; document information stripped |
| `docs/external_reports/Fluoroscopic_AI_Dataset_Author_Contacts.pdf, Spine_Fluoroscopy_Image_Datasets_landscape.pdf` | see section 8 | see section 8 | the plan said author addresses were struck; by text extraction on 2026-10-08 neither the copies nor the sources carry any e-mail address or phone number in their text layer (author names and institutions only), so nothing was struck |

### 3.4 The banned word

The manifest field of the spine-detector snapshot that names where an image came from was renamed `lineage` in seven files
(`code/spine_detector_src_snapshot/src/{build_dataset,export_yolo,manifest}.py`, `src/converters/{buu,mendeley,nhanes}.py`,
`tests/test_manifest.py`; the repository keeps its original field name), one phrase in `docs/RSNAI_PLAN.md` was reworded,
`memory/writing-preferences.md` is the handoff version that states the rule without spelling the word, and
`memory/two-mechanisms-thesis.md` carries one substitution. A grep of the finished folder for the word returns nothing.

### 3.5 Kept as copied, flagged (affiliation)

Five copies say Neurosurgery where the affiliation is General Surgery (Wayne State University School of Medicine / Detroit
Medical Center): the title pages of the superseded drafts `manuscripts/superseded/rsnai/main_v2.tex` (line 29),
`manuscripts/superseded/focused/main.tex` (line 42), `manuscripts/superseded/focused/_drafts/clinical.tex` (line 31) and
`_drafts/methods.tex` (line 36), and the placeholder "[a neurosurgery resident; confirm title]" in
`docs/data_requests/balgrist_data_request_2026-09-21.md` (line 7). They are superseded or unsent and were left as the record;
`TODO.md` A14 corrects any document before it is used.

## 4. Laptop paths rewritten to markers

Every laptop path in a text copy was replaced by a marker so that no file here depends on a laptop. The markers and what
they stood for:

| marker | stood for (history) | what a reader uses instead |
|---|---|---|
| `spinesurg-ct-nnunet:` (also `ssn:` in the handoff copies) | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/` | the private repository at 097933a (`MANIFEST_CODE.md` section 1) |
| `CTSpinoPelvic1K:` (also `ctsp:`) | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/` | the public repository at 7ddfe38 (`MANIFEST_CODE.md` section 2) |
| `OpenSpineToolkit:` (also `ostk:`) | `C:/Users/grego/OneDrive/Desktop/OpenSpineToolkit/` | the public repository at cb43197 |
| `XRSpinoPelvic1K:` | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/` | the private repository at 4f22935 |
| `openspineconsortium.github.io:` | `C:/Users/grego/OneDrive/Desktop/openspineconsortium.github.io/` | the public repository at c1800f8 |
| `memory:` | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/` | `docs/handoff/context/` and `memory/` here |
| `laptop-session:` | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/<session id>/` | nothing; a swept session folder, named only as history |
| `laptop-scratchpad:` | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/<session id>/scratchpad/` | nothing; swept temporary folders, named only as history |
| `laptop:Desktop/` | `C:/Users/grego/OneDrive/Desktop/` | a laptop-only folder (`spine-detector`, `ashley-bridge`, `Student_Projects`, the Desktop root files), named as history |
| `laptop:` | `C:/Users/grego/` | a laptop-only path outside the Desktop (`.ssh`, `model_night`), named as history |
| `<laptop project slug>` | `c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1` | the Claude Code project name of the laptop, inside a swept path |
| `<another author's local path>` | `C:/Users/srira/...` | a path quoted from a third-party dataset's `roi_config.json` |

Files in which markers replaced laptop paths (count per marker, measured as occurrences present in the copy and absent in
the source):

| copy | markers |
|---|---|
| `code/bournemouth_qf_eval.py` | laptop: x1 |
| `code/handoff_builders/build_context_export.py` | spinesurg-ct-nnunet: x1, laptop-scratchpad: x1, memory: x2 |
| `code/handoff_builders/check_paths.py` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x3 |
| `code/handoff_builders/copy_context.py` | spinesurg-ct-nnunet: x1, laptop-scratchpad: x1, memory: x1 |
| `code/handoff_builders/patch_helper.py` | spinesurg-ct-nnunet: x1 |
| `code/handoff_builders/refresh_context.py` | memory: x1 |
| `docs/BOURNEMOUTH_QF_HARNESS.md` | laptop: x1 |
| `docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md` | spinesurg-ct-nnunet: x22, OpenSpineToolkit: x1, laptop:Desktop/ x1, laptop-scratchpad: x1 |
| `docs/CINE_DEMO_RECON_2026-09-26.md` | spinesurg-ct-nnunet: x16, laptop:Desktop/ x2, laptop-scratchpad: x1 |
| `docs/CONTINUANCE_2026-09-19.md` | laptop: x2, <laptop project slug> x1 |
| `docs/FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md` | laptop-session: x2 |
| `docs/MANIFEST_DATA_MODELS_RESULTS.md` | spinesurg-ct-nnunet: x3 |
| `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` | spinesurg-ct-nnunet: x2 |
| `docs/REAL_XRAY_DATASETS_SPEC.md` | spinesurg-ct-nnunet: x1 |
| `docs/data_requests/FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md` | laptop: x1 |
| `docs/handoff/CONTEXT_EXPORT.md` | laptop-scratchpad: x1, memory: x1 |
| `docs/handoff/INFRASTRUCTURE.md` | laptop:Desktop/ x1, laptop: x2 |
| `docs/handoff/LITERATURE_STATE.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1 |
| `docs/handoff/MANUSCRIPTS.md` | laptop: x1, laptop-scratchpad: x1 |
| `docs/handoff/README.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x3, laptop: x1, memory: x1 |
| `docs/handoff/RECIPES.md` | spinesurg-ct-nnunet: x1, laptop: x1 |
| `docs/handoff/RESEARCH_DIRECTIONS.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x2, laptop-scratchpad: x1, memory: x1 |
| `docs/handoff/RESULTS_CATALOG.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop-scratchpad: x1 |
| `docs/handoff/context/COPIED_AT.txt` | memory: x1 |
| `docs/handoff/context/cns-deck-v2-2026-09-25.md` | laptop:Desktop/ x6 |
| `docs/handoff/context/lab-recipe-and-board.md` | laptop:Desktop/ x1 |
| `docs/handoff/context/pacs-demo-and-ostk-params.md` | OpenSpineToolkit: x1 |
| `docs/handoff/context/student-onboarding-structure.md` | laptop:Desktop/ x1 |
| `docs/handoff/context/sweep-map-replaces-registration.md` | laptop: x1 |
| `docs/handoff/context/windows-junction-worktree-trap.md` | laptop:Desktop/ x1, laptop: x1 |
| `docs/handoff/context/windows-ssh-to-grid.md` | laptop: x1 |
| `docs/handoff/context/wsl-for-network.md` | CTSpinoPelvic1K: x1 |
| `docs/handoff/literature_state/assemble.py` | spinesurg-ct-nnunet: x1 |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1 |
| `docs/handoff/literature_state/join_ranking.py` | spinesurg-ct-nnunet: x1 |
| `docs/handoff/literature_state/power.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1 |
| `docs/handoff/literature_state/topic1_bibliography.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1 |
| `docs/handoff/literature_state/topic3_size_relative_to_studies.md` | memory: x1 |
| `docs/handoff/working_notes/topic1_schwingnet_carm_results.md` | spinesurg-ct-nnunet: x1, memory: x1 |
| `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, laptop-scratchpad: x1, memory: x1 |
| `docs/handoff/working_notes/topic3_dataset_usage_leakage_rsna.md` | spinesurg-ct-nnunet: x1, memory: x1 |
| `docs/handoff/working_notes/topic4_manuscripts.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, laptop: x1, laptop-scratchpad: x2, memory: x1 |
| `docs/handoff/working_notes/topic5_operating_here.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x3, laptop: x3, memory: x2 |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, openspineconsortium.github.io: x1, laptop:Desktop/ x5, memory: x1 |
| `docs/or_ready_audit_track_2026-09-22.json` | spinesurg-ct-nnunet: x4, laptop-scratchpad: x5 |
| `docs/research/BIB_RESOLVE_2026-09-22.json` | spinesurg-ct-nnunet: x5 |
| `docs/research/research_carm_datasets_verified_2026-09-22.json` | CTSpinoPelvic1K: x2 |
| `docs/research/research_datasets_fourth_pass_verified_2026-09-22.json` | spinesurg-ct-nnunet: x2, CTSpinoPelvic1K: x1, laptop-scratchpad: x3, <another author's local path> x1 |
| `docs/research/research_datasets_third_pass_verified_2026-09-21.json` | spinesurg-ct-nnunet: x2 |
| `docs/research/research_rsnai_intro2_partial_2026-09-22.json` | laptop-scratchpad: x1 |
| `docs/research/research_rsnai_intro_verified_2026-09-22.json` | laptop-scratchpad: x5 |
| `manuscripts/schwingnet/DRIVE_CHECK.md` | spinesurg-ct-nnunet: x1, laptop: x1 |
| `manuscripts/schwingnet/packet/packet_src/build/cover_letter.md` | CTSpinoPelvic1K: x2 |
| `manuscripts/schwingnet/packet/packet_src/front_matter.json` | CTSpinoPelvic1K: x1 |
| `manuscripts/schwingnet/sections/SOURCES.md` | spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x2 |
| `manuscripts/superseded/rsnai/figures/fig1_row3_crops.json` | laptop-scratchpad: x1 |
| `memory/pacs-demo-and-ostk-params.md` | OpenSpineToolkit: x1 |
| `memory/sweep-map-replaces-registration.md` | laptop: x1 |
| `memory/windows-junction-worktree-trap.md` | laptop:Desktop/ x1, laptop: x1 |
| `memory/wsl-for-network.md` | CTSpinoPelvic1K: x1 |
| `results/schwingnet/age_sex_by_source.json` | spinesurg-ct-nnunet: x19, CTSpinoPelvic1K: x1 |
| `results/schwingnet/age_sex_by_source.md` | spinesurg-ct-nnunet: x17, CTSpinoPelvic1K: x1 |
| `results/schwingnet/corpus_census.json` | spinesurg-ct-nnunet: x1, laptop-scratchpad: x1 |
| `results/schwingnet/corpus_census.md` | spinesurg-ct-nnunet: x1 |
| `results/schwingnet/coverage/pooled_fit.json` | spinesurg-ct-nnunet: x4 |
| `results/schwingnet/coverage/sensitivity/pooled_fit_conf074.json` | spinesurg-ct-nnunet: x4 |
| `results/schwingnet/coverage/sensitivity/pooled_fit_trained_only.json` | spinesurg-ct-nnunet: x4 |
| `results/schwingnet/eval_gate/closure/verify/lineage_check.py` | spinesurg-ct-nnunet: x1 |
| `results/schwingnet/eval_gate/lineage_seed.json` | spinesurg-ct-nnunet: x3 |
| `results/schwingnet/eval_gate/verify/verify_arc_lists.py` | spinesurg-ct-nnunet: x1 |
| `results/schwingnet/eval_gate/verify/verify_trust.py` | spinesurg-ct-nnunet: x1 |
| `results/schwingnet/g0_facts.md` | CTSpinoPelvic1K: x11, laptop-scratchpad: x1 |
| `results/schwingnet/indomain/fit.json` | spinesurg-ct-nnunet: x1 |

A grep of the finished folder (every text file except this one) for `C:/Users`, `C:\Users`, `/mnt/c/Users`, `/c/Users`,
`OneDrive`, `AppData` and `c--Users` returns nothing. Binary files (PDF, Word, PowerPoint) were not searched; the
`manuscript.docx` note in `manuscripts/schwingnet/DRIVE_CHECK.md` records that Word packets carry build paths in their
custom properties, which is one reason the Word packets were not copied.

## 5. The memory notes (`memory/`)

78 notes with a status line from `docs/handoff/context/INDEX.md`: the 22 standing-rule notes every folder carries, 46 of
the carm cut list's 47 listed notes (the inventory's summary table counts 48; `fluorocap-dataset` is referenced, not copied),
and 10 added for this project. `MEMORY.md` lists each with its status and the reason it is here. Copied from the redacted
handoff copies `ssn/HANDOFF/context/<name>.md`; three carry redactions of their own (section 3.1).

## 6. The code copies (`code/`)

Every `.py`, `.sh`, `.sbatch`, YAML, Dockerfile and README under `code/` carries a prepended source header naming its
repository path and its state at 097933a (tracked, working-tree edit, or untracked laptop copy of 2026-10-08);
`code/README.md` is the table. The repository copy is the one to edit and run (on the grid, in a job). 6 code files carry
marker prefixes where their defaults or comments held laptop paths (section 4); the detector snapshot's seven renamed-field
files are in section 3.4.

## 7. Per-run evaluation files removed from the copy (reference by repository)

The disposition copied `sn/results/coverage/experiment/runs/` whole (157 files). The 29 files over 2 MB (the per-arm
`eval_*.json` and `unseen/matches.json`) were compared byte for byte with the repository tree at 097933a (sha256 equal in
every case) and deleted here on 2026-10-08; every summary, table, figure, `ARM_DONE_*` marker and markdown of the folder
stays. All 97 files of that folder are tracked in the private repository (`git ls-files`; last commit touching it
c0a3d7f9, 2026-09-25, "Coverage arms collected and the pooled fit run"). Total removed: 154,258,881 bytes.

| removed from this folder | bytes | sha256 | repository path at 097933a |
|---|---:|---|---|
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_cobra_elekta_test.json` | 9,112,509 | `5fc88c6e9c8279fa39220d7974cd06640a6f59be3fc8735172bb598d7be237ed` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_deepfluoro_test.json` | 2,118,497 | `4dfde5aa6ea1761932c2535e361a48be9c1640fe6f207029656703e32f98de06` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_deepfluoro_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_geneva_hip_test.json` | 3,011,944 | `ec956af34461b3848476a478bdffa7e89e53c66b141ebf0f4083ea8c55888338` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_geneva_hip_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/unseen/matches.json` | 6,112,525 | `0b0ac691232c876af044c8dd1a66fbc22102256e0e0a687049338eb656074e7e` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_cobra_elekta_test.json` | 8,188,894 | `abedc6f48d35444917ad251a6b64c3d3cfc9678c6c912cf572945d032ed13461` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_deepfluoro_test.json` | 2,404,793 | `41073d6896e4618ecd3c8f59cc43eafa035032660bc71ead51ae7cb8d887fb06` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_deepfluoro_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_geneva_hip_test.json` | 2,400,303 | `1e0ecef267d693076c2115ee0d78ff0a9b334b81f3337c9fe4b0caaa2cebf914` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_geneva_hip_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/unseen/matches.json` | 6,130,201 | `3a72b7e6e3d37146922b7c0374d28222f93016f741dab362cb19f6b3642a69e3` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_cobra_elekta_test.json` | 7,877,521 | `906e06a87ea023a72aece51b24d903953222de70095e93d8abff73883f152934` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_geneva_hip_test.json` | 2,362,644 | `cfbadd37ad020c23ae72eca15bf21f9598b290b4fae3c91f80ab432380d3f545` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_geneva_hip_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/unseen/matches.json` | 6,166,105 | `89f3df26afffba62954f60f7f5f29861000d08073fe59f6b53a24ccc960e231f` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_cobra_elekta_test.json` | 7,339,183 | `44488c1b0f2fc97dd975560c1d3097b8adc669b4d47f964e864ffa1eb5e74613` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/unseen/matches.json` | 6,178,080 | `aa229f130f50460c26582612b66abc474f469eaff4365bdd0633b8998be72d03` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_cobra_elekta_test.json` | 8,575,605 | `b1074b1b9a13f28b2b45d82b91f2f6aeb319203a486e5b1b9a2b1a1a63e75f86` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/unseen/matches.json` | 6,048,622 | `cb8877154685d494019213b9a7ce2f86b48ecf92b5d588937309ff91f7baa177` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_cobra_elekta_test.json` | 9,096,014 | `a4bb25e246640c5eafb5ac63b2eedc54bdfa62759ac1fcece4d17819aed60ce7` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_geneva_hip_test.json` | 2,835,498 | `b13e2d10f658deaff0f8711778dbd47a3270d538b2cb75edb188ae06d99574fb` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_geneva_hip_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/unseen/matches.json` | 6,083,516 | `b429ad447774b78d4fb787f753a643ed8ad7fe179bfba9ad19e4612acd31385d` | `SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_cobra_elekta_test.json` | 2,875,957 | `a16717b587381df783e5476a09b24ca2e0db375284b3098d920687fbc2ef6d47` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/unseen/matches.json` | 6,184,466 | `08c32084d43aad68b3c8599775b11f8c57b2951ecec0487d1c369fdef84484b8` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_cobra_elekta_test.json` | 4,267,077 | `f2e95ed1375a8568ecc2c443e86c7a92d18f3f1372828e66ff6cf7409bdcc694` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/unseen/matches.json` | 6,255,899 | `566a85f65790004c4689f4e17e5f72c48d8c9ae266dc3c1048dcee7065c731c2` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_cobra_elekta_test.json` | 2,728,086 | `9ded23cde7ce9c471b2e1aec5533d0f7a7147e8a1814ad3df787fd059cd22e3d` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/unseen/matches.json` | 6,189,189 | `43c872b39c2a4176e4fe188d3023a237412d7ad18284ffb475c6788f9b1844a0` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/unseen/matches.json` | 6,176,889 | `32a1a56d1c7de3bb5d10be2de2623f66ca4d403d08bf926145ca3af0d84e0af5` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_cobra_elekta_test.json` | 2,678,979 | `2b9ef50349ee5493369f9213cc4b08106c01075b199bd023e593feee905761a4` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/unseen/matches.json` | 6,128,696 | `6e6f50a41cab1ca399f7877a55d885f6a08f8b6aed0d9940093764ef046b5161` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/unseen/matches.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_cobra_elekta_test.json` | 2,608,707 | `622374448db6fcdcac30b4b7a4ec7f3daab88330d72fe9abe82cb76ff86f6355` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_cobra_elekta_test.json` |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/unseen/matches.json` | 6,122,482 | `273a5c67a10b05bc64ccde4c37cf8364cf0acf1bb5662ed481f78fefc6c556d5` | `SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/unseen/matches.json` |

## 8. Every file in this folder (1,993 rows; this file is the 1,994th)

State: "same bytes" = byte-identical to the source; "modified on copy" = header, marker or redaction applied (the note says
which); "renamed on copy" = the disposition row named a folder or a set and the file was renamed on the way in (the row text
is the source); "written here" = authored for this folder. Sources are history, not dependencies.

| path | bytes | state | source (history) | note |
|---|---:|---|---|---|
| `CLAUDE.md` | 13,303 | written here |  | written for this folder on 2026-10-08 |
| `MANIFEST_CODE.md` | 16,953 | written here |  | written for this folder on 2026-10-08 |
| `MANIFEST_GRID.md` | 14,447 | written here |  | written for this folder on 2026-10-08 |
| `MEMORY.md` | 32,498 | written here |  | written for this folder on 2026-10-08 |
| `README.md` | 14,193 | written here |  | written for this folder on 2026-10-08 |
| `STATUS.md` | 29,271 | written here |  | written for this folder on 2026-10-08 |
| `TODO.md` | 24,067 | written here |  | written for this folder on 2026-10-08 |
| `code/README.md` | 3,982 | written here |  | written for this folder on 2026-10-08 |
| `code/alphabet_couple.py` | 38,184 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/alphabet_couple.py` | source header prepended |
| `code/bournemouth_qf_eval.py` | 54,336 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/bournemouth_qf_eval.py` | source header prepended; laptop paths rewritten to markers (laptop: x1) |
| `code/checkpoint_lineage.py` | 121,143 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/checkpoint_lineage.py` | source header prepended; the banned word replaced |
| `code/cine_eval.py` | 92,682 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/cine_eval.py` | source header prepended |
| `code/cine_latency.py` | 69,846 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/cine_latency.py` | source header prepended |
| `code/count_from_sacrum_eval.py` | 31,334 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/count_from_sacrum_eval.py` | source header prepended |
| `code/deploy_service.py` | 4,695 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/deploy_service.py` | source header prepended |
| `code/device_census.py` | 23,552 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/device_census.py` | source header prepended |
| `code/eval_calibration.py` | 118,421 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/eval_calibration.py` | source header prepended |
| `code/eval_gate.py` | 79,999 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/eval_gate.py` | source header prepended |
| `code/eval_runtime_cost.py` | 73,304 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/eval_runtime_cost.py` | source header prepended |
| `code/excluded_sources.py` | 5,286 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/excluded_sources.py` | source header prepended |
| `code/fluoro_video/README.md` | 27,771 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/README.md` | source header prepended |
| `code/fluoro_video/__init__.py` | 274 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/__init__.py` | source header prepended |
| `code/fluoro_video/cli.py` | 9,601 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/cli.py` | source header prepended |
| `code/fluoro_video/common.py` | 7,825 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/common.py` | source header prepended |
| `code/fluoro_video/config.yaml` | 12,690 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/config.yaml` | source header prepended |
| `code/fluoro_video/decode.py` | 5,945 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/decode.py` | source header prepended |
| `code/fluoro_video/environment.yml` | 1,060 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/environment.yml` | source header prepended |
| `code/fluoro_video/explicit_lock.txt` | 18,856 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/explicit_lock.txt` | source header prepended |
| `code/fluoro_video/inventory.py` | 9,669 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/inventory.py` | source header prepended |
| `code/fluoro_video/layouts.py` | 9,285 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/layouts.py` | source header prepended |
| `code/fluoro_video/ocr.py` | 7,122 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/ocr.py` | source header prepended |
| `code/fluoro_video/overrides.yaml` | 984 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/overrides.yaml` | source header prepended |
| `code/fluoro_video/panels.py` | 18,976 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/panels.py` | source header prepended |
| `code/fluoro_video/pipeline.py` | 37,027 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/pipeline.py` | source header prepended |
| `code/fluoro_video/qc.py` | 14,451 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/qc.py` | source header prepended |
| `code/fluoro_video/report.py` | 12,091 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/report.py` | source header prepended |
| `code/fluoro_video/slurm/determinism.sbatch` | 871 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/slurm/determinism.sbatch` | source header prepended |
| `code/fluoro_video/slurm/env.sh` | 1,112 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/slurm/env.sh` | source header prepended |
| `code/fluoro_video/slurm/inventory.sbatch` | 592 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/slurm/inventory.sbatch` | source header prepended |
| `code/fluoro_video/slurm/make_env.sbatch` | 1,067 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/slurm/make_env.sbatch` | source header prepended |
| `code/fluoro_video/slurm/report.sbatch` | 577 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/slurm/report.sbatch` | source header prepended |
| `code/fluoro_video/slurm/run_array.sbatch` | 840 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/slurm/run_array.sbatch` | source header prepended |
| `code/fluoro_video/slurm/tests.sbatch` | 937 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/slurm/tests.sbatch` | source header prepended |
| `code/fluoro_video/sourcetext.py` | 7,980 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/sourcetext.py` | source header prepended |
| `code/fluoro_video/synth.py` | 10,758 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/synth.py` | source header prepended |
| `code/fluoro_video/tests/__init__.py` | 175 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/__init__.py` | source header prepended |
| `code/fluoro_video/tests/conftest.py` | 2,124 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/tests/conftest.py` | source header prepended |
| `code/fluoro_video/tests/test_determinism_synth.py` | 1,127 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/tests/test_determinism_synth.py` | source header prepended |
| `code/fluoro_video/tests/test_pipeline_synth.py` | 4,570 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/tests/test_pipeline_synth.py` | source header prepended |
| `code/fluoro_video/tests/test_units.py` | 6,316 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/tests/test_units.py` | source header prepended |
| `code/fluoro_video/timing.py` | 15,756 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/timing.py` | source header prepended |
| `code/handoff_builders/build_context_export.py` | 12,326 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/build_context_export.py` | source header prepended; laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, laptop-scratchpad: x1, memory: x2) |
| `code/handoff_builders/build_context_index.py` | 7,707 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/build_context_index.py` | source header prepended |
| `code/handoff_builders/check_paths.py` | 9,633 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/check_paths.py` | source header prepended; laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x3) |
| `code/handoff_builders/check_refs.py` | 2,127 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/check_refs.py` | source header prepended |
| `code/handoff_builders/copy_context.py` | 5,137 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/copy_context.py` | source header prepended; laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, laptop-scratchpad: x1, memory: x1) |
| `code/handoff_builders/patch_helper.py` | 1,736 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/patch_helper.py` | source header prepended; laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `code/handoff_builders/refresh_context.py` | 6,872 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/refresh_context.py` | source header prepended; laptop paths rewritten to markers (memory: x1) |
| `code/holdout.py` | 5,658 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/holdout.py` | source header prepended |
| `code/latency_bench.py` | 5,701 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/latency_bench.py` | source header prepended |
| `code/level_flags.py` | 12,635 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/level_flags.py` | source header prepended |
| `code/level_prototype.py` | 36,259 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/level_prototype.py` | source header prepended |
| `code/level_selective.py` | 12,722 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/level_selective.py` | source header prepended |
| `code/model_registry.py` | 21,472 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/model_registry.py` | source header prepended |
| `code/patient_keys.py` | 30,822 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/patient_keys.py` | source header prepended |
| `code/publish_checkpoints.py` | 9,299 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/publish_checkpoints.py` | source header prepended |
| `code/service/Dockerfile` | 755 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/service/Dockerfile` |  |
| `code/service/README.md` | 1,297 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/service/README.md` | source header prepended |
| `code/service/app.py` | 3,703 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/service/app.py` | source header prepended |
| `code/service/modal_app.py` | 2,039 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/service/modal_app.py` | source header prepended |
| `code/service/model_defs.py` | 6,791 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/service/model_defs.py` | source header prepended |
| `code/service/requirements.txt` | 285 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/service/requirements.txt` | source header prepended |
| `code/spine_detector_src_snapshot/.gitignore` | 94 | same bytes | `C:/Users/grego/OneDrive/Desktop/spine-detector/.gitignore` |  |
| `code/spine_detector_src_snapshot/src/__init__.py` | 244 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/__init__.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/build_dataset.py` | 10,857 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/build_dataset.py` | source header prepended; the banned word replaced |
| `code/spine_detector_src_snapshot/src/check_fp16_films.py` | 6,088 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/check_fp16_films.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/check_fp16_pck.py` | 5,144 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/check_fp16_pck.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/converters/__init__.py` | 255 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/__init__.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/converters/buu.py` | 6,849 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/converters/buu.py` | source header prepended; the banned word replaced |
| `code/spine_detector_src_snapshot/src/converters/mendeley.py` | 5,983 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/converters/mendeley.py` | source header prepended; the banned word replaced |
| `code/spine_detector_src_snapshot/src/converters/nhanes.py` | 6,940 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/converters/nhanes.py` | source header prepended; the banned word replaced |
| `code/spine_detector_src_snapshot/src/evaluate.py` | 6,040 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/evaluate.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/export_onnx.py` | 5,446 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/export_onnx.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/export_yolo.py` | 6,513 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/export_yolo.py` | source header prepended; the banned word replaced |
| `code/spine_detector_src_snapshot/src/ignore.py` | 6,386 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/ignore.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/manifest.py` | 8,417 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/manifest.py` | source header prepended; the banned word replaced |
| `code/spine_detector_src_snapshot/src/normalize.py` | 6,119 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/normalize.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/render_prediction.py` | 5,652 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/render_prediction.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/run_eval.py` | 5,547 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/run_eval.py` | source header prepended |
| `code/spine_detector_src_snapshot/src/train.py` | 4,359 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/src/train.py` | source header prepended |
| `code/spine_detector_src_snapshot/tests/__init__.py` | 246 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/fluoro_video/__init__.py` | source header prepended |
| `code/spine_detector_src_snapshot/tests/test_manifest.py` | 7,016 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spine-detector/tests/test_manifest.py` |  |
| `code/stats_compare.py` | 66,493 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/stats_compare.py` | source header prepended |
| `code/sweep_map.py` | 135,815 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/sweep_map.py` | source header prepended |
| `code/unseen_cases.py` | 2,490 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/unseen_cases.py` | source header prepended |
| `docs/BOURNEMOUTH_QF_HARNESS.md` | 17,338 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/BOURNEMOUTH_QF_HARNESS.md` | laptop paths rewritten to markers (laptop: x1) |
| `docs/CARM_DEPLOYMENT_EVIDENCE.md` | 6,256 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/CARM_DEPLOYMENT_EVIDENCE.md` |  |
| `docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md` | 35,264 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x22, OpenSpineToolkit: x1, laptop:Desktop/ x1, laptop-scratchpad: x1) |
| `docs/CINE_DEMO_RECON_2026-09-26.md` | 64,170 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/CINE_DEMO_RECON_2026-09-26.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x16, laptop:Desktop/ x2, laptop-scratchpad: x1) |
| `docs/CONTINUANCE_2026-09-19.md` | 9,715 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/CONTINUANCE_2026-09-19.md` | laptop paths rewritten to markers (laptop: x2, <laptop project slug> x1) |
| `docs/COUNTING_EVIDENCE.md` | 10,690 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/COUNTING_EVIDENCE.md` |  |
| `docs/DATASHEET.md` | 25,068 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/DATASHEET.md` | redacted ([e-mail withheld] x1) |
| `docs/FEASIBILITY_REPRODUCE.md` | 9,624 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/FEASIBILITY_REPRODUCE.md` |  |
| `docs/FLAGSHIP_PLAN.md` | 13,647 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/FLAGSHIP_PLAN.md` |  |
| `docs/FLUORO_DATASET_STRATEGY.md` | 16,990 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/FLUORO_DATASET_STRATEGY.md` |  |
| `docs/FLUORO_VIDEO_SOURCES_2026-09-26.md` | 28,867 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/FLUORO_VIDEO_SOURCES_2026-09-26.md` | redacted ([e-mail withheld] x3) |
| `docs/FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md` | 332,466 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md` | laptop paths rewritten to markers (laptop-session: x2); redacted ([e-mail withheld] x43, [phone withheld] x25) |
| `docs/GUIDED_ACQUISITION.md` | 20,857 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/GUIDED_ACQUISITION.md` |  |
| `docs/HANDOFF_PHYSICS.md` | 30,048 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/HANDOFF_PHYSICS.md` |  |
| `docs/MANIFEST_DATA_MODELS_RESULTS.md` | 101,947 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/MANIFEST_DATA_MODELS_RESULTS.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x3) |
| `docs/MODEL_CARD.md` | 43,214 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/MODEL_CARD.md` |  |
| `docs/PHYSICS_LINKING.md` | 36,601 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PHYSICS_LINKING.md` |  |
| `docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md` | 8,206 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md` |  |
| `docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md` | 5,216 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md` |  |
| `docs/PIPELINE_RESUME.md` | 6,961 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PIPELINE_RESUME.md` |  |
| `docs/PIPELINE_SWEEP_LOST_COMPONENTS.md` | 68,760 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PIPELINE_SWEEP_LOST_COMPONENTS.md` |  |
| `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` | 22,038 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x2) |
| `docs/PRIOR_ART_LEVEL_ID_XRAY.md` | 2,618 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PRIOR_ART_LEVEL_ID_XRAY.md` |  |
| `docs/PRIOR_ART_SYNTHETIC_AND_SELF_TRAINING.md` | 17,912 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PRIOR_ART_SYNTHETIC_AND_SELF_TRAINING.md` |  |
| `docs/PRIOR_ART_WEAK_SUPERVISION.md` | 8,906 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PRIOR_ART_WEAK_SUPERVISION.md` |  |
| `docs/PRIOR_ART_WRONG_LEVEL_SCAN.md` | 7,188 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PRIOR_ART_WRONG_LEVEL_SCAN.md` |  |
| `docs/REAL_XRAY_DATASETS_SPEC.md` | 6,626 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/REAL_XRAY_DATASETS_SPEC.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `docs/RSNAI_CLAIMS.json` | 22,147 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/RSNAI_CLAIMS.json` |  |
| `docs/RSNAI_DATA_MANIFEST.json` | 8,799 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/RSNAI_DATA_MANIFEST.json` |  |
| `docs/RSNAI_PLAN.md` | 33,982 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/RSNAI_PLAN.md` | the banned word replaced |
| `docs/RSNAI_TABLE1_DATASETS.md` | 3,100 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/RSNAI_TABLE1_DATASETS.md` |  |
| `docs/SIMULATION_FIDELITY.md` | 8,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/SIMULATION_FIDELITY.md` |  |
| `docs/STUDENT_FLUORO_CORRECTION_GUIDE.md` | 7,000 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/STUDENT_FLUORO_CORRECTION_GUIDE.md` |  |
| `docs/SWEEP_PROTOCOL.md` | 9,274 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/SWEEP_PROTOCOL.md` |  |
| `docs/SWEEP_TIME_EVIDENCE.md` | 13,961 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/SWEEP_TIME_EVIDENCE.md` |  |
| `docs/WRONG_LEVEL_AND_TRANSITIONAL.md` | 7,055 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/WRONG_LEVEL_AND_TRANSITIONAL.md` |  |
| `docs/WRONG_LEVEL_COST_EVIDENCE.md` | 19,631 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/WRONG_LEVEL_COST_EVIDENCE.md` |  |
| `docs/WRONG_SITE_BURDEN_EVIDENCE.md` | 18,122 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/WRONG_SITE_BURDEN_EVIDENCE.md` |  |
| `docs/XRAY_DATASET_USAGE.json` | 6,252 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/XRAY_DATASET_USAGE.json` |  |
| `docs/XRAY_DATASET_USAGE.md` | 4,065 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/XRAY_DATASET_USAGE.md` |  |
| `docs/claim/CLAIMChecklist-6142024.docx` | 30,905 | modified on copy | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/CLAIMChecklist-6142024.docx` |  |
| `docs/claim/CLAIM_2020_checklist.docx` | 42,496 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/CLAIM+-+Checklist+for+AI+in+Medical+imaging.docx` |  |
| `docs/claim/CLAIM_2024_update.pdf` | 144,384 | modified on copy | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/checklist-for-artificial-intelligence-in-medical-imaging-(claim)-2024-update.pdf` |  |
| `docs/claim/CLAIM_checklist.docx` | 17,999 | modified on copy | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/CLAIM_checklist.docx` |  |
| `docs/data_requests/FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md` | 11,467 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md` | laptop paths rewritten to markers (laptop: x1); redacted ([e-mail withheld] x2) |
| `docs/data_requests/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md` | 45,677 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md` | redacted ([e-mail withheld] x34, [phone withheld] x8) |
| `docs/data_requests/SX-Stitch_request.md` | 2,864 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/data_requests/SX-Stitch_request.md` |  |
| `docs/data_requests/balgrist_data_request_2026-09-21.md` | 2,594 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/outreach/balgrist_data_request_2026-09-21.md` | redacted ([e-mail withheld] x3) |
| `docs/external_reports/2D-3D-GS_user_guide.pdf` | 707,342 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/2D-3D-GS_UG.pdf` |  |
| `docs/external_reports/C-Arm_Validation_Research_Plan_2026-09-20.pdf` | 279,029 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/C-Arm Validation Research Plan.pdf` |  |
| `docs/external_reports/Feasibility_FOV_2026-09-17.docx` | 35,077 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Feasibility_FOV.docx` |  |
| `docs/external_reports/Fluoroscopic_AI_Dataset_Author_Contacts.pdf` | 248,247 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Fluoroscopic AI Dataset Author Contacts - Google Gemini.pdf` |  |
| `docs/external_reports/MULTI_XR_2026-09-18.docx` | 32,731 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/MULTI_XR.docx` |  |
| `docs/external_reports/README.md` | 2,286 | written here |  | written for this folder on 2026-10-08 |
| `docs/external_reports/Spine_Fluoroscopy_Image_Datasets_landscape.pdf` | 294,033 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Spine Fluoroscopy Image Datasets.pdf` |  |
| `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | 104,820 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` |  |
| `docs/grid_records/JOBS_RECORD_2026-09-27_1544.tsv` | 15,927 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/grid_records/JOBS_RECORD_2026-09-27_1544.tsv` |  |
| `docs/handoff/CONTEXT_EXPORT.md` | 34,493 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/CONTEXT_EXPORT.md` | laptop paths rewritten to markers (laptop-scratchpad: x1, memory: x1) |
| `docs/handoff/DATASET_USAGE.md` | 37,254 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/DATASET_USAGE.md` |  |
| `docs/handoff/GLOSSARY.md` | 25,368 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GLOSSARY.md` |  |
| `docs/handoff/INFRASTRUCTURE.md` | 48,530 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/INFRASTRUCTURE.md` | laptop paths rewritten to markers (laptop:Desktop/ x1, laptop: x2); redacted ([accessid withheld] x1) |
| `docs/handoff/LEAKAGE.md` | 25,299 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LEAKAGE.md` |  |
| `docs/handoff/LITERATURE_STATE.md` | 170,588 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LITERATURE_STATE.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1); redacted ([e-mail withheld] x23) |
| `docs/handoff/MANUSCRIPTS.md` | 67,480 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/MANUSCRIPTS.md` | laptop paths rewritten to markers (laptop: x1, laptop-scratchpad: x1); redacted (withheld x3, [student x2); student names withheld (3 edits) |
| `docs/handoff/OPEN_QUESTIONS.md` | 28,532 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/OPEN_QUESTIONS.md` |  |
| `docs/handoff/README.md` | 42,328 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/README.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x3, laptop: x1, memory: x1) |
| `docs/handoff/RECIPES.md` | 73,535 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RECIPES.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, laptop: x1); redacted ([student x1) |
| `docs/handoff/RESEARCH_DIRECTIONS.md` | 133,359 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESEARCH_DIRECTIONS.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x2, laptop-scratchpad: x1, memory: x1); redacted ([e-mail withheld] x1) |
| `docs/handoff/RESULTS_CATALOG.md` | 110,219 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESULTS_CATALOG.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop-scratchpad: x1) |
| `docs/handoff/context/COPIED_AT.txt` | 7,200 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/COPIED_AT.txt` | laptop paths rewritten to markers (memory: x1) |
| `docs/handoff/context/INDEX.md` | 25,948 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/INDEX.md` |  |
| `docs/handoff/context/acquisition-space-saturation.md` | 2,936 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/acquisition-space-saturation.md` |  |
| `docs/handoff/context/annotator-roster.md` | 1,166 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/annotator-roster.md` |  |
| `docs/handoff/context/anomaly-harvest-directive.md` | 2,030 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/anomaly-harvest-directive.md` |  |
| `docs/handoff/context/anomaly-manifest-sources.md` | 2,782 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/anomaly-manifest-sources.md` |  |
| `docs/handoff/context/anomaly-rule-rc22-evaluated.md` | 3,512 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/anomaly-rule-rc22-evaluated.md` |  |
| `docs/handoff/context/bash-heredoc-backslashes.md` | 1,009 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/bash-heredoc-backslashes.md` |  |
| `docs/handoff/context/canonical-rib-triage.md` | 1,433 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/canonical-rib-triage.md` |  |
| `docs/handoff/context/carm-plateau-is-the-denominator.md` | 2,532 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/carm-plateau-is-the-denominator.md` |  |
| `docs/handoff/context/carmlspine-level-experiment.md` | 2,970 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/carmlspine-level-experiment.md` |  |
| `docs/handoff/context/chart-preferences.md` | 2,862 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/chart-preferences.md` |  |
| `docs/handoff/context/cloudflare-tls-fingerprint.md` | 1,579 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/cloudflare-tls-fingerprint.md` |  |
| `docs/handoff/context/cns-deck-v2-2026-09-25.md` | 13,247 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/cns-deck-v2-2026-09-25.md` | laptop paths rewritten to markers (laptop:Desktop/ x6) |
| `docs/handoff/context/commit-directly-to-master.md` | 829 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/commit-directly-to-master.md` |  |
| `docs/handoff/context/competitor-benchmark.md` | 4,456 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/competitor-benchmark.md` |  |
| `docs/handoff/context/context-ladder-2d-level-experiment.md` | 1,840 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/context-ladder-2d-level-experiment.md` |  |
| `docs/handoff/context/ct-benchmark-covers-all-collections.md` | 2,027 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-benchmark-covers-all-collections.md` |  |
| `docs/handoff/context/ct-volumes-are-pir-not-ras.md` | 2,001 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-volumes-are-pir-not-ras.md` |  |
| `docs/handoff/context/ctspine1k-selection-code-deleted.md` | 2,219 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ctspine1k-selection-code-deleted.md` |  |
| `docs/handoff/context/data-audit-99-gaps.md` | 3,089 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-audit-99-gaps.md` |  |
| `docs/handoff/context/data-directives-2026-09-23.md` | 2,133 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-directives-2026-09-23.md` |  |
| `docs/handoff/context/data-platform-migration-2026-10.md` | 7,451 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-platform-migration-2026-10.md` |  |
| `docs/handoff/context/dataset813-image-links-are-container-paths.md` | 1,430 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/dataset813-image-links-are-container-paths.md` |  |
| `docs/handoff/context/deepfluoro-convention.md` | 3,119 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/deepfluoro-convention.md` |  |
| `docs/handoff/context/detection-is-the-binding-constraint.md` | 1,758 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/detection-is-the-binding-constraint.md` |  |
| `docs/handoff/context/device-sampling-audit.md` | 3,368 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/device-sampling-audit.md` |  |
| `docs/handoff/context/diagnostics-graph-required.md` | 1,453 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/diagnostics-graph-required.md` |  |
| `docs/handoff/context/drr-row-spacing-defect.md` | 2,312 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/drr-row-spacing-defect.md` |  |
| `docs/handoff/context/drr-to-fluoro-levers.md` | 3,196 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/drr-to-fluoro-levers.md` |  |
| `docs/handoff/context/engine-swap-architecture.md` | 1,670 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/engine-swap-architecture.md` |  |
| `docs/handoff/context/feasibility-claims-measured.md` | 14,681 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/feasibility-claims-measured.md` |  |
| `docs/handoff/context/figure-captions-terse.md` | 1,277 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/figure-captions-terse.md` |  |
| `docs/handoff/context/figure-preferences-schwingnet.md` | 3,969 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/figure-preferences-schwingnet.md` |  |
| `docs/handoff/context/film-fluoro-boundary-not-transferable.md` | 1,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/film-fluoro-boundary-not-transferable.md` |  |
| `docs/handoff/context/film-ncurve-ablation-result.md` | 1,747 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/film-ncurve-ablation-result.md` |  |
| `docs/handoff/context/flagship-paper-frame.md` | 2,565 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/flagship-paper-frame.md` |  |
| `docs/handoff/context/flagship-program.md` | 2,563 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/flagship-program.md` |  |
| `docs/handoff/context/fluoro-panel-gap-diagnosed.md` | 3,848 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluoro-panel-gap-diagnosed.md` |  |
| `docs/handoff/context/fluorocap-dataset.md` | 16,516 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-dataset.md` |  |
| `docs/handoff/context/fluorocap-is-reproductions-not-fluoroscopy.md` | 2,225 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-is-reproductions-not-fluoroscopy.md` |  |
| `docs/handoff/context/fluorocap-pipeline-resume.md` | 2,252 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-pipeline-resume.md` |  |
| `docs/handoff/context/fluorocap-prototype-and-lstv-arm.md` | 13,651 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-prototype-and-lstv-arm.md` |  |
| `docs/handoff/context/fluorocap-repo-private.md` | 1,422 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-repo-private.md` |  |
| `docs/handoff/context/fluorogen-synthetic.md` | 4,230 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorogen-synthetic.md` |  |
| `docs/handoff/context/grid-access-list-gate.md` | 2,075 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access-list-gate.md` | redacted ([accessid withheld] x1, withheld x1, [student x1) |
| `docs/handoff/context/grid-access.md` | 1,342 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access.md` |  |
| `docs/handoff/context/grid-apptainer-module-works.md` | 1,654 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-apptainer-module-works.md` |  |
| `docs/handoff/context/grid-ashley-deletion-2026-09-28.md` | 1,728 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ashley-deletion-2026-09-28.md` |  |
| `docs/handoff/context/grid-bash-4-2-quoting.md` | 1,380 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-bash-4-2-quoting.md` |  |
| `docs/handoff/context/grid-ceph-volume-oschome.md` | 1,296 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ceph-volume-oschome.md` | redacted ([accessid withheld] x1) |
| `docs/handoff/context/grid-ct-0533-truncated.md` | 3,105 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ct-0533-truncated.md` |  |
| `docs/handoff/context/grid-local-singularity-is-broken.md` | 2,368 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-local-singularity-is-broken.md` |  |
| `docs/handoff/context/grid-quota-and-deleted-banks.md` | 2,255 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-quota-and-deleted-banks.md` |  |
| `docs/handoff/context/grid-slurm-inside-apptainer.md` | 1,545 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-slurm-inside-apptainer.md` |  |
| `docs/handoff/context/grid-ssh-second-factor.md` | 1,902 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ssh-second-factor.md` |  |
| `docs/handoff/context/guided-acquisition-loop.md` | 2,446 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/guided-acquisition-loop.md` |  |
| `docs/handoff/context/hf-identity.md` | 644 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/hf-identity.md` |  |
| `docs/handoff/context/hf-mirror-is-v10.md` | 1,606 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/hf-mirror-is-v10.md` |  |
| `docs/handoff/context/identity-audit-findings.md` | 4,160 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/identity-audit-findings.md` |  |
| `docs/handoff/context/journal-figure-and-style-rules.md` | 2,192 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/journal-figure-and-style-rules.md` |  |
| `docs/handoff/context/k-devices-one-network.md` | 4,478 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/k-devices-one-network.md` |  |
| `docs/handoff/context/key-patients-from-metadata-not-filenames.md` | 2,159 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/key-patients-from-metadata-not-filenames.md` |  |
| `docs/handoff/context/l6-sample-count-and-counting-decoder.md` | 1,992 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/l6-sample-count-and-counting-decoder.md` |  |
| `docs/handoff/context/lab-recipe-and-board.md` | 2,731 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/lab-recipe-and-board.md` | laptop paths rewritten to markers (laptop:Desktop/ x1) |
| `docs/handoff/context/label-scheme-v4-vs-ostk.md` | 2,423 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/label-scheme-v4-vs-ostk.md` |  |
| `docs/handoff/context/learned-formation-refuted-calibrate-instead.md` | 19,049 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/learned-formation-refuted-calibrate-instead.md` | redacted ([name withheld] x2, withheld x1) |
| `docs/handoff/context/level-id-2d-results-2026-09-13.md` | 2,269 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/level-id-2d-results-2026-09-13.md` |  |
| `docs/handoff/context/level-model-bank-coverage.md` | 3,005 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/level-model-bank-coverage.md` |  |
| `docs/handoff/context/level-service-serving.md` | 3,057 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/level-service-serving.md` |  |
| `docs/handoff/context/local-level-identity-thesis.md` | 1,743 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/local-level-identity-thesis.md` |  |
| `docs/handoff/context/lstv-data-landscape.md` | 6,433 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/lstv-data-landscape.md` |  |
| `docs/handoff/context/lstv-oneshot-training-run.md` | 6,495 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/lstv-oneshot-training-run.md` |  |
| `docs/handoff/context/lstv-reread-queue.md` | 1,336 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/lstv-reread-queue.md` |  |
| `docs/handoff/context/lstv-tltv-detection-goal.md` | 3,295 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/lstv-tltv-detection-goal.md` |  |
| `docs/handoff/context/mixed-length-head-and-sota.md` | 3,727 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/mixed-length-head-and-sota.md` |  |
| `docs/handoff/context/model-registry.md` | 1,810 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/model-registry.md` |  |
| `docs/handoff/context/morphology-deformation-feasibility.md` | 2,267 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/morphology-deformation-feasibility.md` |  |
| `docs/handoff/context/never-reorient-when-writing-labels.md` | 1,892 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/never-reorient-when-writing-labels.md` |  |
| `docs/handoff/context/nhanes-double-inclusion.md` | 1,487 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/nhanes-double-inclusion.md` |  |
| `docs/handoff/context/nninteractive-colab-versions.md` | 3,907 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/nninteractive-colab-versions.md` |  |
| `docs/handoff/context/no-jobs-on-login-node.md` | 2,148 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-jobs-on-login-node.md` |  |
| `docs/handoff/context/no-unexplained-subsets-fix-not-disclose.md` | 2,097 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` |  |
| `docs/handoff/context/oblique-angles-and-sweep-vision.md` | 2,552 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/oblique-angles-and-sweep-vision.md` |  |
| `docs/handoff/context/ostk-canal-closing-regression.md` | 2,323 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ostk-canal-closing-regression.md` |  |
| `docs/handoff/context/pacs-demo-and-ostk-params.md` | 1,974 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/pacs-demo-and-ostk-params.md` | laptop paths rewritten to markers (OpenSpineToolkit: x1) |
| `docs/handoff/context/pacs-website-latency-root-cause.md` | 1,632 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/pacs-website-latency-root-cause.md` |  |
| `docs/handoff/context/panjabi-1991-page-892.md` | 2,991 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/panjabi-1991-page-892.md` | redacted ([phone withheld] x1) |
| `docs/handoff/context/paper-split-2026-09-24.md` | 1,979 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/paper-split-2026-09-24.md` |  |
| `docs/handoff/context/physics-three-defects-measured.md` | 1,859 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/physics-three-defects-measured.md` |  |
| `docs/handoff/context/polypose-decision.md` | 2,881 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/polypose-decision.md` |  |
| `docs/handoff/context/polypose-generator-build.md` | 2,338 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/polypose-generator-build.md` |  |
| `docs/handoff/context/pooled-vs-lodo-device-designs.md` | 2,127 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/pooled-vs-lodo-device-designs.md` |  |
| `docs/handoff/context/postop-jaggedness-future.md` | 1,333 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/postop-jaggedness-future.md` |  |
| `docs/handoff/context/postop-spine-synthesis.md` | 2,961 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/postop-spine-synthesis.md` |  |
| `docs/handoff/context/prone-supine-flexibility-future.md` | 1,245 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/prone-supine-flexibility-future.md` |  |
| `docs/handoff/context/publication-roadmap.md` | 4,105 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/publication-roadmap.md` |  |
| `docs/handoff/context/push-both-github-remotes.md` | 986 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/push-both-github-remotes.md` |  |
| `docs/handoff/context/recurrent-head-restored-2026-09-16.md` | 3,260 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/recurrent-head-restored-2026-09-16.md` |  |
| `docs/handoff/context/registration-free-prior-art.md` | 2,098 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/registration-free-prior-art.md` |  |
| `docs/handoff/context/remedies-refuted-2026-09-17.md` | 1,976 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/remedies-refuted-2026-09-17.md` |  |
| `docs/handoff/context/review-space-repos.md` | 1,909 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/review-space-repos.md` |  |
| `docs/handoff/context/rib-approach-ts-trust.md` | 2,925 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/rib-approach-ts-trust.md` |  |
| `docs/handoff/context/rib-auto-engulf-post-correction-only.md` | 1,749 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/rib-auto-engulf-post-correction-only.md` |  |
| `docs/handoff/context/rib-qc-gates-never-block-lstv.md` | 1,737 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/rib-qc-gates-never-block-lstv.md` | redacted (two students x1) |
| `docs/handoff/context/rigor-audit-findings.md` | 3,281 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/rigor-audit-findings.md` |  |
| `docs/handoff/context/rsnai-author-instructions.md` | 2,365 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/rsnai-author-instructions.md` |  |
| `docs/handoff/context/rsnai-paper-endpoint.md` | 4,764 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/rsnai-paper-endpoint.md` |  |
| `docs/handoff/context/ruleclass-super-detector-run.md` | 3,134 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ruleclass-super-detector-run.md` |  |
| `docs/handoff/context/s1-carve-changed-spinopelvic.md` | 3,026 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/s1-carve-changed-spinopelvic.md` |  |
| `docs/handoff/context/scheme-bone-hardware-only.md` | 2,592 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/scheme-bone-hardware-only.md` |  |
| `docs/handoff/context/schwingnet-manuscript.md` | 2,531 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/schwingnet-manuscript.md` |  |
| `docs/handoff/context/scratchpad-shadows-stdlib.md` | 1,364 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/scratchpad-shadows-stdlib.md` |  |
| `docs/handoff/context/selective-prediction-the-honest-99.md` | 2,521 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/selective-prediction-the-honest-99.md` |  |
| `docs/handoff/context/six-figure-paper-plan.md` | 2,047 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/six-figure-paper-plan.md` |  |
| `docs/handoff/context/spine-data-review-and-ts-bench.md` | 3,719 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/spine-data-review-and-ts-bench.md` |  |
| `docs/handoff/context/spineps-ids-can-be-scrambled.md` | 2,262 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/spineps-ids-can-be-scrambled.md` |  |
| `docs/handoff/context/split-leak-cross-naming.md` | 1,894 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/split-leak-cross-naming.md` |  |
| `docs/handoff/context/splits-origin-and-v3-resplit.md` | 2,077 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/splits-origin-and-v3-resplit.md` |  |
| `docs/handoff/context/spondylolysis-and-border-anomaly-findings.md` | 2,038 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/spondylolysis-and-border-anomaly-findings.md` |  |
| `docs/handoff/context/stc-does-not-transfer.md` | 3,061 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/stc-does-not-transfer.md` |  |
| `docs/handoff/context/student-onboarding-structure.md` | 2,446 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/student-onboarding-structure.md` | laptop paths rewritten to markers (laptop:Desktop/ x1) |
| `docs/handoff/context/students-see-no-internals.md` | 1,037 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/students-see-no-internals.md` |  |
| `docs/handoff/context/submit-and-sleep-orchestration.md` | 1,888 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/submit-and-sleep-orchestration.md` |  |
| `docs/handoff/context/sweep-map-replaces-registration.md` | 4,280 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/sweep-map-replaces-registration.md` | laptop paths rewritten to markers (laptop: x1) |
| `docs/handoff/context/sweep-physics-no-bone.md` | 2,369 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/sweep-physics-no-bone.md` |  |
| `docs/handoff/context/synthetic-real-ratio-evidence.md` | 3,092 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/synthetic-real-ratio-evidence.md` |  |
| `docs/handoff/context/tables-black-not-colour.md` | 1,152 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/tables-black-not-colour.md` |  |
| `docs/handoff/context/thoracic-gt-fov-limited.md` | 1,109 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/thoracic-gt-fov-limited.md` |  |
| `docs/handoff/context/ts-bench-inside-v9-bank.md` | 1,719 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ts-bench-inside-v9-bank.md` |  |
| `docs/handoff/context/ts-sacrum-excludes-s1.md` | 1,530 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ts-sacrum-excludes-s1.md` |  |
| `docs/handoff/context/two-mechanisms-thesis.md` | 3,052 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/two-mechanisms-thesis.md` |  |
| `docs/handoff/context/user-affiliation-general-surgery.md` | 1,516 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/user-affiliation-general-surgery.md` |  |
| `docs/handoff/context/versefusion-t13-flag-wrong.md` | 1,882 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/versefusion-t13-flag-wrong.md` |  |
| `docs/handoff/context/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` | 1,483 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` |  |
| `docs/handoff/context/windows-junction-worktree-trap.md` | 1,465 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-junction-worktree-trap.md` | laptop paths rewritten to markers (laptop:Desktop/ x1, laptop: x1) |
| `docs/handoff/context/windows-ssh-to-grid.md` | 1,456 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-ssh-to-grid.md` | laptop paths rewritten to markers (laptop: x1) |
| `docs/handoff/context/writing-preferences.md` | 788 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/writing-preferences.md` |  |
| `docs/handoff/context/wsl-for-network.md` | 1,402 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsl-for-network.md` | laptop paths rewritten to markers (CTSpinoPelvic1K: x1) |
| `docs/handoff/context/wsu-library-access-cutoff.md` | 1,491 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsu-library-access-cutoff.md` | redacted ([e-mail withheld] x1, [phone withheld] x3) |
| `docs/handoff/context/xr-benchmark-and-robustness-2026-09-13.md` | 2,812 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/xr-benchmark-and-robustness-2026-09-13.md` |  |
| `docs/handoff/context/xray-corner-detector-status.md` | 1,755 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/xray-corner-detector-status.md` | redacted (a student x1) |
| `docs/handoff/context/zenodo-deposit.md` | 2,352 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/zenodo-deposit.md` |  |
| `docs/handoff/literature_state/assemble.py` | 2,201 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/assemble.py` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `docs/handoff/literature_state/biblio_sorted.py` | 2,213 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/biblio_sorted.py` |  |
| `docs/handoff/literature_state/calc_addendum.json` | 308 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_addendum.json` |  |
| `docs/handoff/literature_state/calc_addendum.py` | 1,589 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_addendum.py` |  |
| `docs/handoff/literature_state/calc_review.json` | 1,381 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_review.json` |  |
| `docs/handoff/literature_state/calc_review.py` | 3,098 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_review.py` |  |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | 61,430 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/dataset_landscape_by_task.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1); redacted ([e-mail withheld] x1) |
| `docs/handoff/literature_state/join_ranking.py` | 4,288 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/join_ranking.py` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `docs/handoff/literature_state/power.md` | 36,450 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/power.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1) |
| `docs/handoff/literature_state/power_calc.json` | 14,819 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/power_calc.json` |  |
| `docs/handoff/literature_state/power_calc.py` | 8,151 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/power_calc.py` |  |
| `docs/handoff/literature_state/ranking_joined.csv` | 23,589 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/ranking_joined.csv` |  |
| `docs/handoff/literature_state/t3_ratios.py` | 3,918 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/t3_ratios.py` |  |
| `docs/handoff/literature_state/topic1_bibliography.md` | 91,935 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/topic1_bibliography.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, memory: x1) |
| `docs/handoff/literature_state/topic3_size_relative_to_studies.md` | 41,424 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/topic3_size_relative_to_studies.md` | laptop paths rewritten to markers (memory: x1) |
| `docs/handoff/working_notes/t2_wilson_check.py` | 905 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/t2_wilson_check.py` |  |
| `docs/handoff/working_notes/topic1_schwingnet_carm_results.md` | 87,237 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic1_schwingnet_carm_results.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, memory: x1) |
| `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md` | 97,146 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic2_scaling_samples_anomaly_power.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, laptop-scratchpad: x1, memory: x1); redacted ([student x1) |
| `docs/handoff/working_notes/topic3_dataset_usage_leakage_rsna.md` | 59,351 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic3_dataset_usage_leakage_rsna.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, memory: x1) |
| `docs/handoff/working_notes/topic4_manuscripts.md` | 87,050 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic4_manuscripts.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, laptop: x1, laptop-scratchpad: x2, memory: x1); redacted (withheld x3, [student x2); student names withheld (3 edits) |
| `docs/handoff/working_notes/topic5_operating_here.md` | 85,836 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic5_operating_here.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, laptop:Desktop/ x3, laptop: x3, memory: x2); redacted ([accessid withheld] x1) |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 95,965 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x1, OpenSpineToolkit: x1, openspineconsortium.github.io: x1, laptop:Desktop/ x5, memory: x1); redacted (withheld x1); student names withheld (1 edits) |
| `docs/or_ready_audit_track_2026-09-22.json` | 12,934 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/or_ready_audit_track_2026-09-22.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x4, laptop-scratchpad: x5) |
| `docs/pipeline.md` | 10,032 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/pipeline.md` |  |
| `docs/research/BIB_AUDIT_2026-09-22.json` | 45,753 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/BIB_AUDIT_2026-09-22.json` |  |
| `docs/research/BIB_AUDIT_2026-09-22.md` | 5,642 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/BIB_AUDIT_2026-09-22.md` |  |
| `docs/research/BIB_AUDIT_2026-09-22b.json` | 48,246 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/BIB_AUDIT_2026-09-22b.json` |  |
| `docs/research/BIB_AUDIT_2026-09-22b.md` | 3,892 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/BIB_AUDIT_2026-09-22b.md` |  |
| `docs/research/BIB_RESOLVE_2026-09-22.json` | 269,189 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/BIB_RESOLVE_2026-09-22.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x5); redacted ([e-mail withheld] x1, withheld x1); student names withheld (2 edits) |
| `docs/research/research_carm_datasets_verified_2026-09-22.json` | 200,756 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_carm_datasets_verified_2026-09-22.json` | laptop paths rewritten to markers (CTSpinoPelvic1K: x2) |
| `docs/research/research_datasets_fourth_pass_verified_2026-09-22.json` | 1,320,395 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_datasets_fourth_pass_verified_2026-09-22.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x2, CTSpinoPelvic1K: x1, laptop-scratchpad: x3, <another author's local path> x1); redacted ([e-mail withheld] x64, [phone withheld] x1) |
| `docs/research/research_datasets_missed_verified_2026-09-21.json` | 33,431 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_datasets_missed_verified_2026-09-21.json` | redacted ([e-mail withheld] x8) |
| `docs/research/research_datasets_third_pass_verified_2026-09-21.json` | 39,411 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_datasets_third_pass_verified_2026-09-21.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x2); redacted ([e-mail withheld] x4) |
| `docs/research/research_localisation_cost_2026-09-22.json` | 55,683 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_localisation_cost_2026-09-22.json` |  |
| `docs/research/research_paired_ct_projection_unverified_2026-09-21.md` | 11,147 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_paired_ct_projection_unverified_2026-09-21.md` |  |
| `docs/research/research_paired_ct_projection_verified_2026-09-21.json` | 41,733 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_paired_ct_projection_verified_2026-09-21.json` | redacted ([e-mail withheld] x4) |
| `docs/research/research_registration_free_search_2026-09-22.md` | 61,952 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_registration_free_search_2026-09-22.md` |  |
| `docs/research/research_rsnai_author_instructions_2026-09-22.md` | 18,479 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_rsnai_author_instructions_2026-09-22.md` |  |
| `docs/research/research_rsnai_intro2_partial_2026-09-22.json` | 179,144 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_rsnai_intro2_partial_2026-09-22.json` | laptop paths rewritten to markers (laptop-scratchpad: x1) |
| `docs/research/research_rsnai_intro_nav_verified_2026-09-22.json` | 191,981 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_rsnai_intro_nav_verified_2026-09-22.json` |  |
| `docs/research/research_rsnai_intro_verified_2026-09-22.json` | 186,437 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_rsnai_intro_verified_2026-09-22.json` | laptop paths rewritten to markers (laptop-scratchpad: x5) |
| `docs/research/research_sim_real_mixing_verified_2026-09-21.json` | 28,845 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/research_sim_real_mixing_verified_2026-09-21.json` |  |
| `docs/spinesurg_ct_nnunet_CLAUDE.md` | 1,101 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/CLAUDE.md` |  |
| `docs/spinesurg_ct_nnunet_README.md` | 13,558 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/README.md` |  |
| `docs/troubleshooting.md` | 3,540 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/troubleshooting.md` |  |
| `figures/figures_carmlspine_gallery.pdf` | 515,727 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_carmlspine_gallery.pdf` |  |
| `figures/figures_carmlspine_gallery.png` | 2,380,698 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_carmlspine_gallery.png` |  |
| `figures/figures_carmlspine_preview.png` | 4,612,338 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_carmlspine_preview.png` |  |
| `figures/figures_carmlspine_results.pdf` | 24,356 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_carmlspine_results.pdf` |  |
| `figures/figures_carmlspine_results.png` | 243,373 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_carmlspine_results.png` |  |
| `figures/figures_carmlspine_survey.png` | 186,340 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_carmlspine_survey.png` |  |
| `figures/figures_handoff_ljubljana_im004.png` | 127,075 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_handoff_ljubljana_im004.png` |  |
| `figures/figures_paired_sets_properties.png` | 276,798 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/figures_paired_sets_properties.png` |  |
| `figures/schwingnet/FIGURES.md` | 7,822 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/FIGURES.md` |  |
| `figures/schwingnet/SUPPLEMENT_FIGURES.md` | 15,196 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/SUPPLEMENT_FIGURES.md` |  |
| `figures/schwingnet/fig1a_problem.caption.txt` | 316 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1a_problem.caption.txt` |  |
| `figures/schwingnet/fig1a_problem.pdf` | 18,014 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1a_problem.pdf` |  |
| `figures/schwingnet/fig1a_problem.png` | 43,839 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1a_problem.png` |  |
| `figures/schwingnet/fig1c_arch.caption.txt` | 359 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1c_arch.caption.txt` |  |
| `figures/schwingnet/fig1c_arch.pdf` | 54,074 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1c_arch.pdf` |  |
| `figures/schwingnet/fig1c_arch.png` | 175,299 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1c_arch.png` |  |
| `figures/schwingnet/fig1d_algorithm.caption.txt` | 356 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1d_algorithm.caption.txt` |  |
| `figures/schwingnet/fig1d_algorithm.pdf` | 23,327 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1d_algorithm.pdf` |  |
| `figures/schwingnet/fig1d_algorithm.png` | 155,814 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig1d_algorithm.png` |  |
| `figures/schwingnet/fig2_flow.caption.txt` | 248 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig2_flow.caption.txt` |  |
| `figures/schwingnet/fig2_flow.pdf` | 42,572 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig2_flow.pdf` |  |
| `figures/schwingnet/fig2_flow.png` | 719,720 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig2_flow.png` |  |
| `figures/schwingnet/fig2_pipeline.caption.txt` | 376 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig2_pipeline.caption.txt` | one word trimmed on the fix pass of 2026-10-08 ("(NCC)" dropped) so the caption counts 60 words; the source sidecar is 61 (`TODO.md` F4) |
| `figures/schwingnet/fig2_pipeline.pdf` | 36,266 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig2_pipeline.pdf` |  |
| `figures/schwingnet/fig2_pipeline.png` | 105,853 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig2_pipeline.png` |  |
| `figures/schwingnet/fig3_detection.caption.txt` | 419 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig3_detection.caption.txt` |  |
| `figures/schwingnet/fig3_detection.numbers.json` | 24,115 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig3_detection.numbers.json` |  |
| `figures/schwingnet/fig3_detection.pdf` | 177,490 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig3_detection.pdf` |  |
| `figures/schwingnet/fig3_detection.png` | 1,100,346 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig3_detection.png` |  |
| `figures/schwingnet/fig3_naming.pdf` | 32,922 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig3_naming.pdf` |  |
| `figures/schwingnet/fig3_naming.png` | 236,895 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig3_naming.png` |  |
| `figures/schwingnet/fig4_detection.pdf` | 37,983 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig4_detection.pdf` |  |
| `figures/schwingnet/fig4_detection.png` | 376,869 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig4_detection.png` |  |
| `figures/schwingnet/fig4_formation.caption.txt` | 397 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig4_formation.caption.txt` |  |
| `figures/schwingnet/fig4_formation.pdf` | 164,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig4_formation.pdf` |  |
| `figures/schwingnet/fig4_formation.png` | 1,138,079 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig4_formation.png` |  |
| `figures/schwingnet/fig4_formation.record.json` | 14,617 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig4_formation.record.json` |  |
| `figures/schwingnet/fig5_confirm_fluoro.caption.txt` | 257 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_confirm_fluoro.caption.txt` |  |
| `figures/schwingnet/fig5_confirm_fluoro.pdf` | 274,640 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_confirm_fluoro.pdf` |  |
| `figures/schwingnet/fig5_confirm_fluoro.png` | 271,432 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_confirm_fluoro.png` |  |
| `figures/schwingnet/fig5_contribution.caption.txt` | 307 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_contribution.caption.txt` |  |
| `figures/schwingnet/fig5_contribution.pdf` | 39,537 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_contribution.pdf` |  |
| `figures/schwingnet/fig5_contribution.png` | 520,611 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_contribution.png` |  |
| `figures/schwingnet/fig5_naming.caption.txt` | 395 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_naming.caption.txt` |  |
| `figures/schwingnet/fig5_naming.pdf` | 93,885 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_naming.pdf` |  |
| `figures/schwingnet/fig5_naming.png` | 1,013,692 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig5_naming.png` |  |
| `figures/schwingnet/fig6_claim.caption.txt` | 442 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig6_claim.caption.txt` |  |
| `figures/schwingnet/fig6_claim.pdf` | 44,396 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig6_claim.pdf` |  |
| `figures/schwingnet/fig6_claim.png` | 465,237 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig6_claim.png` |  |
| `figures/schwingnet/figS1.caption.txt` | 407 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS1.caption.txt` |  |
| `figures/schwingnet/figS1.pdf` | 1,083,727 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS1.pdf` |  |
| `figures/schwingnet/figS1.png` | 813,753 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS1.png` |  |
| `figures/schwingnet/figS1.record.json` | 10,585 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS1.record.json` |  |
| `figures/schwingnet/figS2.caption.txt` | 369 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS2.caption.txt` |  |
| `figures/schwingnet/figS2.pdf` | 1,632,335 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS2.pdf` |  |
| `figures/schwingnet/figS2.png` | 997,845 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS2.png` |  |
| `figures/schwingnet/figS2.record.json` | 21,001 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS2.record.json` |  |
| `figures/schwingnet/figS3.caption.txt` | 419 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS3.caption.txt` |  |
| `figures/schwingnet/figS3.pdf` | 65,672 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS3.pdf` |  |
| `figures/schwingnet/figS3.png` | 445,039 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS3.png` |  |
| `figures/schwingnet/figS3.record.json` | 36,538 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS3.record.json` |  |
| `figures/schwingnet/figS4.caption.txt` | 362 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS4.caption.txt` |  |
| `figures/schwingnet/figS4.pdf` | 2,225,669 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS4.pdf` |  |
| `figures/schwingnet/figS4.png` | 1,112,817 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS4.png` |  |
| `figures/schwingnet/figS4.record.json` | 23,108 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figS4.record.json` |  |
| `figures/schwingnet/fig_contribution.png` | 554,081 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_contribution.png` |  |
| `figures/schwingnet/fig_learning.caption.txt` | 377 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_learning.caption.txt` |  |
| `figures/schwingnet/fig_learning.pdf` | 271,455 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_learning.pdf` |  |
| `figures/schwingnet/fig_learning.png` | 2,119,782 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_learning.png` |  |
| `figures/schwingnet/fig_manifold.caption.txt` | 403 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_manifold.caption.txt` |  |
| `figures/schwingnet/fig_manifold.pdf` | 159,514 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_manifold.pdf` |  |
| `figures/schwingnet/fig_manifold.png` | 1,217,336 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_manifold.png` |  |
| `figures/schwingnet/fig_manifold.record.json` | 8,885 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_manifold.record.json` |  |
| `figures/schwingnet/fig_transitional_gallery.caption.txt` | 428 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_transitional_gallery.caption.txt` |  |
| `figures/schwingnet/fig_transitional_gallery.pdf` | 1,776,149 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_transitional_gallery.pdf` |  |
| `figures/schwingnet/fig_transitional_gallery.png` | 2,373,649 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/fig_transitional_gallery.png` |  |
| `figures/schwingnet/figure1.caption.txt` | 420 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure1.caption.txt` |  |
| `figures/schwingnet/figure1.pdf` | 4,082,300 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure1.pdf` |  |
| `figures/schwingnet/figure1.png` | 2,037,310 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure1.png` |  |
| `figures/schwingnet/figure1.record.json` | 28,453 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure1.record.json` |  |
| `figures/schwingnet/figure2.caption.txt` | 478 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure2.caption.txt` |  |
| `figures/schwingnet/figure2.pdf` | 1,575,719 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure2.pdf` |  |
| `figures/schwingnet/figure2.png` | 1,369,688 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure2.png` |  |
| `figures/schwingnet/figure2.record.json` | 28,040 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure2.record.json` |  |
| `figures/schwingnet/figure3.caption.txt` | 418 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure3.caption.txt` |  |
| `figures/schwingnet/figure3.pdf` | 67,629 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure3.pdf` |  |
| `figures/schwingnet/figure3.png` | 339,322 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure3.png` |  |
| `figures/schwingnet/figure3.record.json` | 22,073 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure3.record.json` |  |
| `figures/schwingnet/figure4.caption.txt` | 380 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure4.caption.txt` |  |
| `figures/schwingnet/figure4.pdf` | 1,508,624 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure4.pdf` |  |
| `figures/schwingnet/figure4.png` | 1,612,927 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure4.png` |  |
| `figures/schwingnet/figure4.record.json` | 37,562 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure4.record.json` |  |
| `figures/schwingnet/figure5.caption.txt` | 406 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure5.caption.txt` |  |
| `figures/schwingnet/figure5.pdf` | 53,377 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure5.pdf` |  |
| `figures/schwingnet/figure5.png` | 596,623 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure5.png` |  |
| `figures/schwingnet/figure5.record.json` | 34,574 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/figures/figure5.record.json` |  |
| `manuscripts/schwingnet/.gitignore` | 307 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/.gitignore` |  |
| `manuscripts/schwingnet/CLAIMS_LEDGER.md` | 44,857 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/CLAIMS_LEDGER.md` |  |
| `manuscripts/schwingnet/CLAIM_CHECKLIST.md` | 26,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/CLAIM_CHECKLIST.md` |  |
| `manuscripts/schwingnet/DRIVE_CHECK.md` | 16,211 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/DRIVE_CHECK.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, laptop: x1) |
| `manuscripts/schwingnet/FINAL_CHECK.md` | 16,108 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/FINAL_CHECK.md` |  |
| `manuscripts/schwingnet/NUMBERS.md` | 114,508 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/NUMBERS.md` |  |
| `manuscripts/schwingnet/PAPER1_SCOPE.md` | 6,774 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/PAPER1_SCOPE.md` |  |
| `manuscripts/schwingnet/README.md` | 14,885 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/README.md` |  |
| `manuscripts/schwingnet/REFS_AUDIT.md` | 27,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REFS_AUDIT.md` |  |
| `manuscripts/schwingnet/RESULTS_BUILD.md` | 4,227 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/RESULTS_BUILD.md` |  |
| `manuscripts/schwingnet/REVIEW2_RSNA.md` | 53,791 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REVIEW2_RSNA.md` |  |
| `manuscripts/schwingnet/REVIEW2_STATS.md` | 47,318 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REVIEW2_STATS.md` |  |
| `manuscripts/schwingnet/REVIEW_RSNA.md` | 20,983 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REVIEW_RSNA.md` |  |
| `manuscripts/schwingnet/REVIEW_STATS.md` | 36,962 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REVIEW_STATS.md` |  |
| `manuscripts/schwingnet/REVISION_LOG.md` | 32,879 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REVISION_LOG.md` |  |
| `manuscripts/schwingnet/REVISION_LOG2.md` | 44,164 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REVISION_LOG2.md` |  |
| `manuscripts/schwingnet/REVISION_LOG3.md` | 111,772 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/REVISION_LOG3.md` |  |
| `manuscripts/schwingnet/RSNA_AI_REQUIREMENTS.md` | 12,574 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/RSNA_AI_REQUIREMENTS.md` |  |
| `manuscripts/schwingnet/TEMPLATE_NOTES.md` | 4,847 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/TEMPLATE_NOTES.md` |  |
| `manuscripts/schwingnet/TITLE.md` | 4,970 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/TITLE.md` |  |
| `manuscripts/schwingnet/atlas/README.md` | 16,236 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/atlas/README.md` | redacted ([e-mail withheld] x2) |
| `manuscripts/schwingnet/atlas/VALIDATION.md` | 6,688 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/atlas/VALIDATION.md` |  |
| `manuscripts/schwingnet/atlas/dataset.json` | 42,804 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/atlas/dataset.json` | redacted ([e-mail withheld] x3); student names withheld (1 edits) |
| `manuscripts/schwingnet/atlas/model.json` | 26,429 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/atlas/model.json` | redacted ([e-mail withheld] x3); student names withheld (1 edits) |
| `manuscripts/schwingnet/atlas/update_cards.py` | 40,541 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/atlas/update_cards.py` | redacted ([e-mail withheld] x5); student names withheld (1 edits) |
| `manuscripts/schwingnet/atlas/validate_cards.py` | 10,915 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/atlas/validate_cards.py` |  |
| `manuscripts/schwingnet/claim_checklist.json` | 30,111 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/claim_checklist.json` |  |
| `manuscripts/schwingnet/generated/numbers.tex` | 17,588 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/generated/numbers.tex` |  |
| `manuscripts/schwingnet/generated/numbers_audit.md` | 20,152 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/generated/numbers_audit.md` |  |
| `manuscripts/schwingnet/generated/pending.json` | 2,273 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/generated/pending.json` |  |
| `manuscripts/schwingnet/latexmkrc` | 931 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/latexmkrc` |  |
| `manuscripts/schwingnet/lit/CITABLE_CLAIMS.md` | 67,981 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/lit/CITABLE_CLAIMS.md` |  |
| `manuscripts/schwingnet/lit/acquisition_space_review_2026-09-24.pdf` | 227,165 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/lit/acquisition_space_review_2026-09-24.pdf` |  |
| `manuscripts/schwingnet/lit/acquisition_space_review_2026-09-24.txt` | 39,963 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/lit/acquisition_space_review_2026-09-24.txt` |  |
| `manuscripts/schwingnet/lit/refs_additions.bib` | 20,104 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/lit/refs_additions.bib` |  |
| `manuscripts/schwingnet/main.tex` | 21,935 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/main.tex` |  |
| `manuscripts/schwingnet/nejm.bbx` | 2,249 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/nejm.bbx` |  |
| `manuscripts/schwingnet/nejm.cbx` | 522 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/nejm.cbx` |  |
| `manuscripts/schwingnet/numbers_manifest.json` | 35,281 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/numbers_manifest.json` |  |
| `manuscripts/schwingnet/packet/SchwingNet_cameraready_main_and_supplement_2026-09-27.pdf` | 12,576,360 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_build/SchwingNet_cameraready_main_and_supplement_2026-09-27.pdf` |  |
| `manuscripts/schwingnet/packet/SchwingNet_review_main_and_supplement_2026-09-27.pdf` | 12,575,097 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_build/SchwingNet_review_main_and_supplement_2026-09-27.pdf` |  |
| `manuscripts/schwingnet/packet/packet_src/README.md` | 21,376 | written here |  | written for this folder on 2026-10-08 |
| `manuscripts/schwingnet/packet/packet_src/build/BUILD_REPORT.md` | 11,326 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build/BUILD_REPORT.md` |  |
| `manuscripts/schwingnet/packet/packet_src/build/CLAIM_CHECKLIST_2024.md` | 25,041 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build/CLAIM_CHECKLIST_2024.md` |  |
| `manuscripts/schwingnet/packet/packet_src/build/claim_checklist_2024.docx` | 42,376 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build/claim_checklist_2024.docx` |  |
| `manuscripts/schwingnet/packet/packet_src/build/claim_checklist_2024.json` | 34,970 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build/claim_checklist_2024.json` |  |
| `manuscripts/schwingnet/packet/packet_src/build/cover_letter.docx` | 40,961 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build/cover_letter.docx` |  |
| `manuscripts/schwingnet/packet/packet_src/build/cover_letter.md` | 7,670 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/cover_letter.md` | laptop paths rewritten to markers (CTSpinoPelvic1K: x2); redacted ([e-mail withheld] x1) |
| `manuscripts/schwingnet/packet/packet_src/build/full_title_page.docx` | 40,339 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build/full_title_page.docx` |  |
| `manuscripts/schwingnet/packet/packet_src/build/full_title_page.md` | 5,687 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build/full_title_page.md` | redacted ([e-mail withheld] x1, [phone withheld] x1) |
| `manuscripts/schwingnet/packet/packet_src/build_packet_src.py` | 37,035 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/build_packet_src.py` |  |
| `manuscripts/schwingnet/packet/packet_src/claim2024/extract_items.py` | 4,889 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/claim2024/extract_items.py` |  |
| `manuscripts/schwingnet/packet/packet_src/claim2024/items.json` | 8,007 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/claim2024/items.json` |  |
| `manuscripts/schwingnet/packet/packet_src/claim2024/map.json` | 33,877 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/claim2024/map.json` |  |
| `manuscripts/schwingnet/packet/packet_src/cover_letter.md` | 6,691 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/cover_letter.md` |  |
| `manuscripts/schwingnet/packet/packet_src/front_matter.json` | 26,142 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/front_matter.json` | laptop paths rewritten to markers (CTSpinoPelvic1K: x1); redacted ([e-mail withheld] x1, [phone withheld] x1); student names withheld (1 edits) |
| `manuscripts/schwingnet/packet/packet_src/numbers.json` | 13,279 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/numbers.json` |  |
| `manuscripts/schwingnet/packet/packet_src/overlap/arXiv_2609.22760v1_CTSpinoPelvic1K.pdf` | 1,535,970 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/overlap/arXiv_2609.22760v1_CTSpinoPelvic1K.pdf` |  |
| `manuscripts/schwingnet/packet/packet_src/persons_available_2026-09-24.json` | 20,148 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/persons_available_2026-09-24.json` |  |
| `manuscripts/schwingnet/packet/packet_src/statements.md` | 17,216 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/statements.md` |  |
| `manuscripts/schwingnet/packet/packet_src/supplement_technical.tex` | 8,844 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/supplement_technical.tex` |  |
| `manuscripts/schwingnet/packet/packet_src/texcheck/check.sh` | 1,540 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck/check.sh` |  |
| `manuscripts/schwingnet/packet/packet_src/texcheck/p1.png` | 97,071 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck/p1.png` |  |
| `manuscripts/schwingnet/packet/packet_src/texcheck/p2.png` | 47,316 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck/p2.png` |  |
| `manuscripts/schwingnet/packet/packet_src/texcheck/p3.png` | 60,845 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck/p3.png` |  |
| `manuscripts/schwingnet/packet/packet_src/texcheck/supp_technical_check.pdf` | 23,842 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck/supp_technical_check.pdf` |  |
| `manuscripts/schwingnet/packet/packet_src/texcheck/supp_technical_check.tex` | 310 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck/supp_technical_check.tex` |  |
| `manuscripts/schwingnet/packet/packet_src/title_page.md` | 1,779 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/packet_src/title_page.md` |  |
| `manuscripts/schwingnet/refs.bib` | 34,323 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/refs.bib` | student names withheld (2 edits) |
| `manuscripts/schwingnet/refs_corrections.bib` | 30,687 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/refs_corrections.bib` | student names withheld (2 edits) |
| `manuscripts/schwingnet/rsnaresults.sty` | 4,784 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/rsnaresults.sty` |  |
| `manuscripts/schwingnet/rsnastyle.tex` | 7,493 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/rsnastyle.tex` |  |
| `manuscripts/schwingnet/sections/SOURCES.md` | 10,018 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/SOURCES.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, CTSpinoPelvic1K: x2) |
| `manuscripts/schwingnet/sections/discussion_limits.tex` | 2,526 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/discussion_limits.tex` |  |
| `manuscripts/schwingnet/sections/discussion_motivation.tex` | 5,731 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/discussion_motivation.tex` |  |
| `manuscripts/schwingnet/sections/introduction.tex` | 4,195 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/introduction.tex` |  |
| `manuscripts/schwingnet/sections/methods.tex` | 11,442 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/methods.tex` |  |
| `manuscripts/schwingnet/sections/methods_sources.md` | 13,536 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/methods_sources.md` |  |
| `manuscripts/schwingnet/sections/refs_used.bib` | 12,028 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/refs_used.bib` |  |
| `manuscripts/schwingnet/sections/results.tex` | 12,585 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/sections/results.tex` |  |
| `manuscripts/schwingnet/supplement.tex` | 30,993 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/supplement.tex` |  |
| `manuscripts/schwingnet/tables/main_p18.png` | 651,490 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/main_p18.png` |  |
| `manuscripts/schwingnet/tables/main_p19.png` | 581,145 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/main_p19.png` |  |
| `manuscripts/schwingnet/tables/main_p20.png` | 502,646 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/main_p20.png` |  |
| `manuscripts/schwingnet/tables/main_p21.png` | 594,074 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/main_p21.png` |  |
| `manuscripts/schwingnet/tables/tab2_detection.md` | 10,348 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab2_detection.md` |  |
| `manuscripts/schwingnet/tables/tab2_detection.sources.md` | 13,992 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab2_detection.sources.md` |  |
| `manuscripts/schwingnet/tables/tab2_detection.tex` | 9,509 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab2_detection.tex` |  |
| `manuscripts/schwingnet/tables/tab3_naming.md` | 12,302 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab3_naming.md` |  |
| `manuscripts/schwingnet/tables/tab3_naming.sources.md` | 11,868 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab3_naming.sources.md` |  |
| `manuscripts/schwingnet/tables/tab3_naming.tex` | 12,293 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab3_naming.tex` |  |
| `manuscripts/schwingnet/tables/tab4_transitional.md` | 5,834 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab4_transitional.md` |  |
| `manuscripts/schwingnet/tables/tab4_transitional.sources.md` | 5,340 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab4_transitional.sources.md` |  |
| `manuscripts/schwingnet/tables/tab4_transitional.tex` | 9,431 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab4_transitional.tex` |  |
| `manuscripts/schwingnet/tables/tabS1_device_terms.tex` | 3,102 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tabS1_device_terms.tex` |  |
| `manuscripts/schwingnet/tables/tabS3_age_sex.md` | 2,875 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tabS3_age_sex.md` |  |
| `manuscripts/schwingnet/tables/tabS3_corpus.md` | 5,129 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tabS3_corpus.md` |  |
| `manuscripts/schwingnet/tables/tabS3_corpus.tex` | 6,237 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tabS3_corpus.tex` |  |
| `manuscripts/schwingnet/tables/tabS4_ablation.tex` | 2,736 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tabS4_ablation.tex` |  |
| `manuscripts/schwingnet/tables/tabS4_census.md` | 5,056 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tabS4_census.md` |  |
| `manuscripts/schwingnet/tables/tab_corpus.caption.txt` | 182 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab_corpus.caption.txt` |  |
| `manuscripts/schwingnet/tables/tab_corpus.md` | 7,395 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab_corpus.md` |  |
| `manuscripts/schwingnet/tables/tab_corpus.sources.md` | 14,769 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab_corpus.sources.md` |  |
| `manuscripts/schwingnet/tables/tab_corpus.tex` | 10,808 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tab_corpus.tex` |  |
| `manuscripts/schwingnet/tables/tables.check.p1.png` | 665,226 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check.p1.png` |  |
| `manuscripts/schwingnet/tables/tables.check.p2.png` | 458,906 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check.p2.png` |  |
| `manuscripts/schwingnet/tables/tables.check.p3.png` | 485,283 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check.p3.png` |  |
| `manuscripts/schwingnet/tables/tables.check.p4.png` | 507,932 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check.p4.png` |  |
| `manuscripts/schwingnet/tables/tables.check.pdf` | 42,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check.pdf` |  |
| `manuscripts/schwingnet/tables/tables.check_sans.p1.png` | 705,193 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check_sans.p1.png` |  |
| `manuscripts/schwingnet/tables/tables.check_sans.p2.png` | 488,307 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check_sans.p2.png` |  |
| `manuscripts/schwingnet/tables/tables.check_sans.p3.png` | 509,297 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check_sans.p3.png` |  |
| `manuscripts/schwingnet/tables/tables.check_sans.p4.png` | 535,890 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check_sans.p4.png` |  |
| `manuscripts/schwingnet/tables/tables.check_sans.pdf` | 37,790 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables.check_sans.pdf` |  |
| `manuscripts/schwingnet/tables/tables_check.tex` | 1,941 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/tables/tables_check.tex` |  |
| `manuscripts/superseded/README.md` | 1,875 | written here |  | written for this folder on 2026-10-08 |
| `manuscripts/superseded/focused/_drafts/build.sh` | 1,201 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/build.sh` |  |
| `manuscripts/superseded/focused/_drafts/build_clinical.sh` | 1,266 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/build_clinical.sh` |  |
| `manuscripts/superseded/focused/_drafts/clinical.pdf` | 139,635 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/clinical.pdf` |  |
| `manuscripts/superseded/focused/_drafts/clinical.tex` | 31,430 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/clinical.tex` |  |
| `manuscripts/superseded/focused/_drafts/deployment.pdf` | 138,063 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/deployment.pdf` |  |
| `manuscripts/superseded/focused/_drafts/deployment.tex` | 31,201 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/deployment.tex` | redacted ([e-mail withheld] x1) |
| `manuscripts/superseded/focused/_drafts/methods.pdf` | 170,585 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/methods.pdf` |  |
| `manuscripts/superseded/focused/_drafts/methods.tex` | 32,309 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/_drafts/methods.tex` |  |
| `manuscripts/superseded/focused/build.sh` | 1,375 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/build.sh` |  |
| `manuscripts/superseded/focused/figures/dataset_profile.json` | 2,727 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/dataset_profile.json` |  |
| `manuscripts/superseded/focused/figures/fig1_pipeline.png` | 51,890 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig1_pipeline.png` |  |
| `manuscripts/superseded/focused/figures/fig2_stitch.png` | 827,054 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig2_stitch.png` |  |
| `manuscripts/superseded/focused/figures/fig3_step.png` | 157,726 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig3_step.png` |  |
| `manuscripts/superseded/focused/figures/fig4_confirm.png` | 412,335 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig4_confirm.png` |  |
| `manuscripts/superseded/focused/figures/fig_anchor_real.png` | 523,221 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_anchor_real.png` |  |
| `manuscripts/superseded/focused/figures/fig_best_synthetic.png` | 1,472,408 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_best_synthetic.png` |  |
| `manuscripts/superseded/focused/figures/fig_boxes_films.png` | 514,439 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_boxes_films.png` |  |
| `manuscripts/superseded/focused/figures/fig_dataset_levels.pdf` | 20,718 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_dataset_levels.pdf` |  |
| `manuscripts/superseded/focused/figures/fig_dataset_levels.png` | 62,861 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_dataset_levels.png` |  |
| `manuscripts/superseded/focused/figures/fig_detector.pdf` | 49,818 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_detector.pdf` |  |
| `manuscripts/superseded/focused/figures/fig_detector.png` | 351,161 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_detector.png` |  |
| `manuscripts/superseded/focused/figures/fig_formation.png` | 216,770 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_formation.png` |  |
| `manuscripts/superseded/focused/figures/fig_network.pdf` | 38,246 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_network.pdf` |  |
| `manuscripts/superseded/focused/figures/fig_network.png` | 224,202 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_network.png` |  |
| `manuscripts/superseded/focused/figures/fig_path_census.png` | 85,858 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_path_census.png` |  |
| `manuscripts/superseded/focused/figures/fig_physics_chain.png` | 897,257 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_physics_chain.png` |  |
| `manuscripts/superseded/focused/figures/fig_physics_overlap.png` | 40,865 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/fig_physics_overlap.png` |  |
| `manuscripts/superseded/focused/figures/figure_meta.json` | 228 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/figure_meta.json` |  |
| `manuscripts/superseded/focused/figures/tab_all_results.csv` | 22,770 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/tab_all_results.csv` |  |
| `manuscripts/superseded/focused/figures/tab_all_results.json` | 52,765 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/tab_all_results.json` |  |
| `manuscripts/superseded/focused/figures/tab_all_results.tex` | 20,161 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/tab_all_results.tex` |  |
| `manuscripts/superseded/focused/figures/tab_all_results_encoders.tex` | 1,064 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/tab_all_results_encoders.tex` |  |
| `manuscripts/superseded/focused/figures/tab_all_results_headline.tex` | 1,387 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/tab_all_results_headline.tex` |  |
| `manuscripts/superseded/focused/figures/tab_dataset.tex` | 1,494 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/figures/tab_dataset.tex` |  |
| `manuscripts/superseded/focused/main.pdf` | 4,830,125 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/main.pdf` |  |
| `manuscripts/superseded/focused/main.tex` | 86,353 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/main.tex` |  |
| `manuscripts/superseded/focused/wordcount.py` | 1,586 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/focused/wordcount.py` |  |
| `manuscripts/superseded/rsnai/build.sh` | 1,126 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/build.sh` |  |
| `manuscripts/superseded/rsnai/claims.tex` | 11,696 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/claims.tex` |  |
| `manuscripts/superseded/rsnai/figures/dataset_profile.json` | 2,727 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/dataset_profile.json` |  |
| `manuscripts/superseded/rsnai/figures/fig10_ablation.png` | 166,623 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig10_ablation.png` |  |
| `manuscripts/superseded/rsnai/figures/fig11_filmmatch.png` | 156,338 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig11_filmmatch.png` |  |
| `manuscripts/superseded/rsnai/figures/fig12_windows_by_class_interior.png` | 100,381 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig12_windows_by_class_interior.png` |  |
| `manuscripts/superseded/rsnai/figures/fig13_feature_cartoon.pdf` | 35,714 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig13_feature_cartoon.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig13_feature_cartoon.png` | 208,286 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig13_feature_cartoon.png` |  |
| `manuscripts/superseded/rsnai/figures/fig15_spacing.pdf` | 20,248 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig15_spacing.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig15_spacing.png` | 136,776 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig15_spacing.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_problem.pdf` | 33,197 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_problem.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_problem.png` | 202,621 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_problem.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row1_pipeline.png` | 244,430 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row1_pipeline.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row2_anatomy.pdf` | 43,840 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row2_anatomy.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row2_anatomy.png` | 805,255 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row2_anatomy.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row2_stitch.png` | 362,570 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row2_stitch.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_confirm.png` | 276,230 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_confirm.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_confirm_fs.json` | 231 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_confirm_fs.json` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_confirm_fs.png` | 310,465 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_confirm_fs.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_crops.json` | 1,344 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_crops.json` | laptop paths rewritten to markers (laptop-scratchpad: x1) |
| `manuscripts/superseded/rsnai/figures/fig1_row3_crops.pdf` | 228,077 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_crops.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_crops.png` | 650,188 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_crops.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_overlap.json` | 935 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_overlap.json` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_overlap.pdf` | 76,140 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_overlap.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row3_overlap.png` | 639,820 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row3_overlap.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row4_fluorohash.json` | 2,101 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row4_fluorohash.json` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row4_fluorohash.pdf` | 101,951 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row4_fluorohash.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row4_fluorohash.png` | 582,032 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row4_fluorohash.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row4_manifold.png` | 935,073 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row4_manifold.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row5_corpus.png` | 652,581 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row5_corpus.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row5_corpus_arch.png` | 544,251 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row5_corpus_arch.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row6_arch.pdf` | 47,232 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row6_arch.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row6_arch.png` | 560,961 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row6_arch.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row6_confirm_fluoro.png` | 271,432 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row6_confirm_fluoro.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row_architectures.pdf` | 49,502 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row_architectures.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row_architectures.png` | 529,464 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row_architectures.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row_data_inventory.pdf` | 47,618 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row_data_inventory.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row_data_inventory.png` | 509,285 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row_data_inventory.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row_spine_states.pdf` | 230,023 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row_spine_states.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_row_spine_states.png` | 1,353,654 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_row_spine_states.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_story.pdf` | 173,385 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_story.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_story.png` | 1,032,112 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_story.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_story2.pdf` | 1,059,631 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_story2.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_story2.png` | 1,293,463 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_story2.png` |  |
| `manuscripts/superseded/rsnai/figures/fig1_story_tall.pdf` | 432,300 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_story_tall.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig1_story_tall.png` | 2,209,408 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig1_story_tall.png` |  |
| `manuscripts/superseded/rsnai/figures/fig2_breakthrough.pdf` | 22,990 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig2_breakthrough.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig2_breakthrough.png` | 263,243 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig2_breakthrough.png` |  |
| `manuscripts/superseded/rsnai/figures/fig3_along_spine.pdf` | 15,602 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig3_along_spine.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig3_along_spine.png` | 123,356 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig3_along_spine.png` |  |
| `manuscripts/superseded/rsnai/figures/fig4_error_structure.pdf` | 15,995 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig4_error_structure.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig4_error_structure.png` | 140,251 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig4_error_structure.png` |  |
| `manuscripts/superseded/rsnai/figures/fig5_fov_curve.pdf` | 23,040 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig5_fov_curve.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig5_fov_curve.png` | 213,507 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig5_fov_curve.png` |  |
| `manuscripts/superseded/rsnai/figures/fig6_geometry.pdf` | 28,083 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig6_geometry.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig6_geometry.png` | 237,550 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig6_geometry.png` |  |
| `manuscripts/superseded/rsnai/figures/fig7_cooccurrence.pdf` | 33,150 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig7_cooccurrence.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig7_cooccurrence.png` | 160,325 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig7_cooccurrence.png` |  |
| `manuscripts/superseded/rsnai/figures/fig8_data.pdf` | 22,183 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig8_data.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig8_data.png` | 243,240 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig8_data.png` |  |
| `manuscripts/superseded/rsnai/figures/fig_dataset_levels.pdf` | 20,718 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig_dataset_levels.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig_dataset_levels.png` | 62,861 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig_dataset_levels.png` |  |
| `manuscripts/superseded/rsnai/figures/fig_network.pdf` | 38,246 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig_network.pdf` |  |
| `manuscripts/superseded/rsnai/figures/fig_network.png` | 224,202 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/fig_network.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_film_ii_none1_x1_wide_none_e0.png` | 283,526 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_film_ii_none1_x1_wide_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_physics_fpd_none1_x10_tight_colmean+detrend_e0.png` | 215,926 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_physics_fpd_none1_x10_tight_colmean+detrend_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_physics_ii_circle0.55_x10_tight_colmean+detrend_e0.15.png` | 102,257 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_physics_ii_circle0.55_x10_tight_colmean+detrend_e0.15.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_physics_ii_circle0.55_x10_tight_none_e0.png` | 101,112 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_physics_ii_circle0.55_x10_tight_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_physics_ii_none1_x10_tight_colmean+detrend_e0.png` | 181,713 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_physics_ii_none1_x10_tight_colmean+detrend_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_physics_ii_none1_x10_tight_none_e0.png` | 171,281 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_physics_ii_none1_x10_tight_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_physics_ii_none1_x1_tight_none_e0.png` | 213,163 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_physics_ii_none1_x1_tight_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe/p_probe_physics_ii_none1_x1_wide_none_e0.png` | 213,458 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe/p_probe_physics_ii_none1_x1_wide_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-bv_pulsera_ii_none1_x1_tight_none_e0.png` | 297,970 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-bv_pulsera_ii_none1_x1_tight_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-bv_pulsera_ii_none1_x1_wide_none_e0.png` | 298,122 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-bv_pulsera_ii_none1_x1_wide_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-cios_fusion_ii_none1_x1_tight_none_e0.png` | 214,768 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-cios_fusion_ii_none1_x1_tight_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-cios_fusion_ii_none1_x1_wide_none_e0.png` | 214,959 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-cios_fusion_ii_none1_x1_wide_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-elekta_xvi_ii_none1_x1_tight_none_e0.png` | 218,051 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-elekta_xvi_ii_none1_x1_tight_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-elekta_xvi_ii_none1_x1_wide_none_e0.png` | 218,491 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-elekta_xvi_ii_none1_x1_wide_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-pixium_4600_ii_none1_x1_tight_none_e0.png` | 319,079 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-pixium_4600_ii_none1_x1_tight_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/probe2/p_probe_card-pixium_4600_ii_none1_x1_wide_none_e0.png` | 319,256 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/probe2/p_probe_card-pixium_4600_ii_none1_x1_wide_none_e0.png` |  |
| `manuscripts/superseded/rsnai/figures/tab1_claims.csv` | 1,704 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab1_claims.csv` |  |
| `manuscripts/superseded/rsnai/figures/tab1_claims.tex` | 1,928 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab1_claims.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab2_sources.csv` | 1,186 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab2_sources.csv` |  |
| `manuscripts/superseded/rsnai/figures/tab2_sources.tex` | 1,372 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab2_sources.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab3_geometry.csv` | 3,094 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab3_geometry.csv` |  |
| `manuscripts/superseded/rsnai/figures/tab4_arms.tex` | 889 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab4_arms.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab7_per_level.tex` | 1,737 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab7_per_level.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab_all_results.csv` | 32,270 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_all_results.csv` |  |
| `manuscripts/superseded/rsnai/figures/tab_all_results.json` | 74,398 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_all_results.json` |  |
| `manuscripts/superseded/rsnai/figures/tab_all_results.tex` | 27,892 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_all_results.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab_all_results_encoders.tex` | 1,086 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_all_results_encoders.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab_all_results_headline.tex` | 1,976 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_all_results_headline.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab_all_results_protocol.tex` | 1,375 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_all_results_protocol.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab_dataset.tex` | 1,494 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_dataset.tex` |  |
| `manuscripts/superseded/rsnai/figures/tab_datasets_kdevices.tex` | 1,918 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/figures/tab_datasets_kdevices.tex` |  |
| `manuscripts/superseded/rsnai/graveyard.pdf` | 302,206 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/graveyard.pdf` |  |
| `manuscripts/superseded/rsnai/graveyard.tex` | 134,779 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/graveyard.tex` |  |
| `manuscripts/superseded/rsnai/main.pdf` | 293,411 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/main.pdf` |  |
| `manuscripts/superseded/rsnai/main.tex` | 51,597 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/main.tex` | redacted ([e-mail withheld] x1) |
| `manuscripts/superseded/rsnai/main.tex.pre-restructure` | 135,906 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/main.tex.pre-restructure` | redacted ([e-mail withheld] x1) |
| `manuscripts/superseded/rsnai/main_kdevices_skeleton.tex` | 4,365 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/main_kdevices_skeleton.tex` |  |
| `manuscripts/superseded/rsnai/main_v2.pdf` | 450,488 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/main_v2.pdf` |  |
| `manuscripts/superseded/rsnai/main_v2.tex` | 22,279 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/main_v2.tex` |  |
| `manuscripts/superseded/rsnai/refs.bib` | 56,982 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/paper/rsnai/refs.bib` | student names withheld (1 edits) |
| `manuscripts/talks/CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx` | 13,608,289 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx` |  |
| `memory/acquisition-space-saturation.md` | 3,001 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/acquisition-space-saturation.md` |  |
| `memory/anomaly-rule-rc22-evaluated.md` | 3,577 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/anomaly-rule-rc22-evaluated.md` |  |
| `memory/bash-heredoc-backslashes.md` | 1,074 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/bash-heredoc-backslashes.md` |  |
| `memory/carm-plateau-is-the-denominator.md` | 2,597 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/carm-plateau-is-the-denominator.md` |  |
| `memory/carmlspine-level-experiment.md` | 2,996 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/carmlspine-level-experiment.md` |  |
| `memory/chart-preferences.md` | 2,927 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/chart-preferences.md` |  |
| `memory/ct-volumes-are-pir-not-ras.md` | 2,066 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/ct-volumes-are-pir-not-ras.md` |  |
| `memory/data-audit-99-gaps.md` | 3,152 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/data-audit-99-gaps.md` |  |
| `memory/data-directives-2026-09-23.md` | 2,198 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/data-directives-2026-09-23.md` |  |
| `memory/deepfluoro-convention.md` | 3,184 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/deepfluoro-convention.md` |  |
| `memory/detection-is-the-binding-constraint.md` | 1,823 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/detection-is-the-binding-constraint.md` |  |
| `memory/device-sampling-audit.md` | 3,433 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/device-sampling-audit.md` |  |
| `memory/drr-row-spacing-defect.md` | 2,377 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/drr-row-spacing-defect.md` |  |
| `memory/drr-to-fluoro-levers.md` | 3,261 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/drr-to-fluoro-levers.md` |  |
| `memory/engine-swap-architecture.md` | 1,733 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/engine-swap-architecture.md` |  |
| `memory/feasibility-claims-measured.md` | 14,897 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/feasibility-claims-measured.md` |  |
| `memory/figure-captions-terse.md` | 1,342 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/figure-captions-terse.md` |  |
| `memory/figure-preferences-schwingnet.md` | 4,097 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/figure-preferences-schwingnet.md` |  |
| `memory/film-fluoro-boundary-not-transferable.md` | 1,722 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/film-fluoro-boundary-not-transferable.md` |  |
| `memory/film-ncurve-ablation-result.md` | 2,124 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/film-ncurve-ablation-result.md` |  |
| `memory/flagship-paper-frame.md` | 2,681 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/flagship-paper-frame.md` |  |
| `memory/flagship-program.md` | 2,626 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/flagship-program.md` |  |
| `memory/fluorocap-is-reproductions-not-fluoroscopy.md` | 2,325 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/fluorocap-is-reproductions-not-fluoroscopy.md` |  |
| `memory/fluorocap-pipeline-resume.md` | 2,317 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/fluorocap-pipeline-resume.md` |  |
| `memory/fluorocap-repo-private.md` | 1,487 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/fluorocap-repo-private.md` |  |
| `memory/grid-access.md` | 1,458 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/grid-access.md` |  |
| `memory/grid-bash-4-2-quoting.md` | 1,606 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/grid-bash-4-2-quoting.md` |  |
| `memory/grid-ceph-volume-oschome.md` | 1,361 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/grid-ceph-volume-oschome.md` | redacted ([accessid withheld] x1) |
| `memory/grid-local-singularity-is-broken.md` | 2,433 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/grid-local-singularity-is-broken.md` |  |
| `memory/grid-quota-and-deleted-banks.md` | 2,320 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/grid-quota-and-deleted-banks.md` |  |
| `memory/guided-acquisition-loop.md` | 2,509 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/guided-acquisition-loop.md` |  |
| `memory/identity-audit-findings.md` | 4,225 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/identity-audit-findings.md` |  |
| `memory/k-devices-one-network.md` | 4,543 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/k-devices-one-network.md` |  |
| `memory/key-patients-from-metadata-not-filenames.md` | 2,224 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/key-patients-from-metadata-not-filenames.md` |  |
| `memory/label-scheme-v4-vs-ostk.md` | 2,488 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/label-scheme-v4-vs-ostk.md` |  |
| `memory/learned-formation-refuted-calibrate-instead.md` | 19,223 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/learned-formation-refuted-calibrate-instead.md` | redacted ([phone withheld] x1, [name withheld] x2, withheld x3) |
| `memory/level-id-2d-results-2026-09-13.md` | 2,447 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/level-id-2d-results-2026-09-13.md` |  |
| `memory/level-model-bank-coverage.md` | 3,030 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/level-model-bank-coverage.md` |  |
| `memory/level-service-serving.md` | 3,082 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/level-service-serving.md` |  |
| `memory/local-level-identity-thesis.md` | 1,808 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/local-level-identity-thesis.md` |  |
| `memory/lstv-tltv-detection-goal.md` | 3,360 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/lstv-tltv-detection-goal.md` |  |
| `memory/mixed-length-head-and-sota.md` | 4,111 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/mixed-length-head-and-sota.md` |  |
| `memory/model-registry.md` | 1,875 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/model-registry.md` |  |
| `memory/morphology-deformation-feasibility.md` | 2,332 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/morphology-deformation-feasibility.md` |  |
| `memory/never-reorient-when-writing-labels.md` | 1,957 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/never-reorient-when-writing-labels.md` |  |
| `memory/no-jobs-on-login-node.md` | 2,213 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/no-jobs-on-login-node.md` |  |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | 2,162 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/no-unexplained-subsets-fix-not-disclose.md` |  |
| `memory/oblique-angles-and-sweep-vision.md` | 2,617 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/oblique-angles-and-sweep-vision.md` |  |
| `memory/pacs-demo-and-ostk-params.md` | 2,039 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/pacs-demo-and-ostk-params.md` | laptop paths rewritten to markers (OpenSpineToolkit: x1) |
| `memory/paper-split-2026-09-24.md` | 2,044 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/paper-split-2026-09-24.md` |  |
| `memory/physics-three-defects-measured.md` | 1,924 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/physics-three-defects-measured.md` |  |
| `memory/pooled-vs-lodo-device-designs.md` | 2,192 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/pooled-vs-lodo-device-designs.md` |  |
| `memory/recurrent-head-restored-2026-09-16.md` | 3,372 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/recurrent-head-restored-2026-09-16.md` |  |
| `memory/registration-free-prior-art.md` | 2,163 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/registration-free-prior-art.md` |  |
| `memory/remedies-refuted-2026-09-17.md` | 2,195 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/remedies-refuted-2026-09-17.md` |  |
| `memory/rigor-audit-findings.md` | 3,344 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/rigor-audit-findings.md` |  |
| `memory/rsnai-author-instructions.md` | 2,430 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/rsnai-author-instructions.md` |  |
| `memory/rsnai-paper-endpoint.md` | 4,868 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/rsnai-paper-endpoint.md` |  |
| `memory/schwingnet-manuscript.md` | 2,596 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/schwingnet-manuscript.md` |  |
| `memory/scratchpad-shadows-stdlib.md` | 1,429 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/scratchpad-shadows-stdlib.md` |  |
| `memory/selective-prediction-the-honest-99.md` | 2,858 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/selective-prediction-the-honest-99.md` |  |
| `memory/six-figure-paper-plan.md` | 2,150 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/six-figure-paper-plan.md` |  |
| `memory/spine-data-review-and-ts-bench.md` | 3,782 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/spine-data-review-and-ts-bench.md` |  |
| `memory/split-leak-cross-naming.md` | 1,959 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/split-leak-cross-naming.md` |  |
| `memory/stc-does-not-transfer.md` | 3,126 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/stc-does-not-transfer.md` |  |
| `memory/submit-and-sleep-orchestration.md` | 1,953 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/submit-and-sleep-orchestration.md` |  |
| `memory/sweep-map-replaces-registration.md` | 4,345 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/sweep-map-replaces-registration.md` | laptop paths rewritten to markers (laptop: x1) |
| `memory/sweep-physics-no-bone.md` | 2,434 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/sweep-physics-no-bone.md` |  |
| `memory/synthetic-real-ratio-evidence.md` | 3,157 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/synthetic-real-ratio-evidence.md` |  |
| `memory/tables-black-not-colour.md` | 1,217 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/tables-black-not-colour.md` |  |
| `memory/ts-bench-inside-v9-bank.md` | 1,784 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/ts-bench-inside-v9-bank.md` |  |
| `memory/two-mechanisms-thesis.md` | 3,438 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/two-mechanisms-thesis.md` | the banned word replaced |
| `memory/user-affiliation-general-surgery.md` | 1,581 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/user-affiliation-general-surgery.md` |  |
| `memory/windows-junction-worktree-trap.md` | 1,530 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/windows-junction-worktree-trap.md` | laptop paths rewritten to markers (laptop:Desktop/ x1, laptop: x1) |
| `memory/writing-preferences.md` | 853 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/writing-preferences.md` |  |
| `memory/wsl-for-network.md` | 1,467 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/wsl-for-network.md` | laptop paths rewritten to markers (CTSpinoPelvic1K: x1) |
| `memory/wsu-library-access-cutoff.md` | 1,556 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/wsu-library-access-cutoff.md` | redacted ([e-mail withheld] x1, [phone withheld] x3) |
| `memory/xray-corner-detector-status.md` | 1,818 | modified on copy | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/xray-corner-detector-status.md` | redacted (a student x1) |
| `regulatory/DUA_advisory_text.pdf` | 108,127 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/DUA.pdf` |  |
| `regulatory/README.md` | 6,288 | written here |  | written for this folder on 2026-10-08 |
| `regulatory/carm_validation_plan_2026-09-21/AIDaS_Seed_Grant_Program.pdf` | 66,001 | extracted from a zip | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Untitled_Message.zip (inside the zip; the zip itself not copied)` |  |
| `regulatory/carm_validation_plan_2026-09-21/C-Arm_Validation_Research_Plan.docx` | 30,865 | extracted from a zip | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Untitled_Message.zip (inside the zip; the zip itself not copied)` |  |
| `regulatory/carm_validation_plan_2026-09-21/WSU_Body_Bequest_contact_page.pdf` | 2,051,761 | extracted from a zip | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Untitled_Message.zip (inside the zip; the zip itself not copied)` |  |
| `regulatory/carm_validation_plan_2026-09-21/WSU_OEHS_X-ray_Generating_Machine_Safety.pdf` | 1,828,401 | extracted from a zip | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/Untitled_Message.zip (inside the zip; the zip itself not copied)` |  |
| `regulatory/hpr_2026-144/HPR_2026-144_determination_2026-04-21.pdf` | 2,212,767 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/IRB Not HPR Determination 4.21.26.pdf` (2,088,991 B) | two personal phone numbers struck in page text and form fields (checked by text extraction on 2026-10-08); renamed; byte-identical twins at the Desktop root were not copied again |
| `regulatory/hpr_2026-269/HPR_2026-269_memo_2026-09-02.pdf` | 670,187 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/2026 269 Schwing IRB Not HPR Determination 9.2.26.pdf` |  |
| `regulatory/hpr_2026-269/HPR_tool_as_filed_2026-08-28.pdf` | 556,822 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/OSC_HPR_Determination_public_datasets.pdf` |  |
| `regulatory/hpr_2026-269/HPR_tool_filled_2026-05-31.pdf` | 532,178 | modified on copy | `C:/Users/grego/OneDrive/Desktop/hpr_determination_tool_revised_11_2021_SCHWING_FILLED.pdf` (437,030 B) | two personal phone numbers struck in page text and form fields (checked by text extraction on 2026-10-08); renamed |
| `regulatory/protocol_2026-03/Data_Collection_Tool.docx` | 17,066 | modified on copy | `C:/Users/grego/OneDrive/Desktop/IRB/Data_Collection_Tool.docx` |  |
| `regulatory/protocol_2026-03/Data_Collection_Tool.pdf` | 84,456 | same bytes | `C:/Users/grego/OneDrive/Desktop/IRB/Data_Collection_Tool.pdf` |  |
| `regulatory/protocol_2026-03/IRB-26-03-8648_SubmitPreApproval_receipt_2026-03-30.pdf` | 1,994 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K/IRB_IRB-26-03-8648_SubmitPreApproval.pdf` |  |
| `regulatory/protocol_2026-03/spine_study_protocol.docx` | 28,558 | modified on copy | `C:/Users/grego/OneDrive/Desktop/IRB/spine_study_protocol.docx` |  |
| `regulatory/protocol_2026-03/spine_study_protocol.pdf` | 134,943 | same bytes | `C:/Users/grego/OneDrive/Desktop/IRB/spine_study_protocol.pdf` |  |
| `regulatory/protocols_2026-09/FluoroCap_HPR_attachment.md` | 4,815 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/proposals/FluoroCap_HPR_attachment.md` |  |
| `regulatory/protocols_2026-09/IRB_ADDENDUM_2026-09-10.md` | 6,748 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/IRB_ADDENDUM.md` |  |
| `regulatory/protocols_2026-09/IRB_PLAN_2026-09-11.md` | 5,117 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSP1K_private/proposals_backup_20260911/irb/IRB_PLAN.md` | redacted ([e-mail withheld] x8) |
| `regulatory/protocols_2026-09/IRB_two_protocols_summary.docx` | 15,511 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/proposals/irb/IRB_two_protocols_summary.docx` |  |
| `regulatory/protocols_2026-09/IRB_two_protocols_summary.pdf` | 41,155 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/proposals/irb/IRB_two_protocols_summary.pdf` |  |
| `regulatory/protocols_2026-09/PROPOSAL_SHORT_2026-09-11.md` | 7,585 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSP1K_private/proposals_backup_20260911/irb/PROPOSAL_SHORT.md` |  |
| `regulatory/protocols_2026-09/PROTOCOL_1_eProtocol_draft_2026-09-15.md` | 27,331 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/proposals/irb/PROTOCOL_1_eProtocol_draft_2026-09-15.md` |  |
| `regulatory/vindr_2026-09-25/00_cover_note_to_IRB.docx` | 13,820 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/IRB_VinDr_2026-09-25/00_cover_note_to_IRB.docx` |  |
| `regulatory/vindr_2026-09-25/00_cover_note_to_IRB.md` | 4,991 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/IRB_VinDr_2026-09-25/00_cover_note_to_IRB.md` | redacted ([phone withheld] x1) |
| `regulatory/vindr_2026-09-25/01_HPR_Determination_Tool_VinDr-SpineXR_2026-09-25.pdf` | 522,962 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/IRB_VinDr_2026-09-25/01_HPR_Determination_Tool_VinDr-SpineXR_Schwing_2026-09-25.pdf` (560,189 B) | one personal phone number struck in page text and form fields (checked by text extraction on 2026-10-08); renamed |
| `regulatory/vindr_2026-09-25/HPR_determination_VinDr-SpineXR_draft.md` | 29,910 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/IRB/HPR_determination_VinDr-SpineXR_draft.md` | redacted ([phone withheld] x2) |
| `regulatory/wsu_dmc_forms/01-05_flexible_review_and_oversight.docx` | 34,783 | modified on copy | `C:/Users/grego/OneDrive/Desktop/IRB/01-05_flexible_review_and_oversight.doc` |  |
| `regulatory/wsu_dmc_forms/dmc-research-review-process-and-instructions-revised-2022.pdf` | 747,011 | modified on copy | `C:/Users/grego/OneDrive/Desktop/IRB/dmc-research-review-process-and-instructions-revised-2022.pdf` |  |
| `regulatory/wsu_dmc_forms/dmc-researchreviewprocess-2022.pdf` | 188,650 | same bytes | `C:/Users/grego/OneDrive/Desktop/IRB/dmc-researchreviewprocess-2022.pdf` |  |
| `regulatory/wsu_dmc_forms/hpr-guidance-activities-that-are-not-hpr.docx` | 102,390 | modified on copy | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/hpr-guidance-activities-that-are-not-hpr-ada-update-4726.docx` |  |
| `regulatory/wsu_dmc_forms/hpr_determination_tool_revised_11_2021_blank.pdf` | 412,781 | same bytes | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/hpr_determination_tool_revised_11_2021.pdf` |  |
| `regulatory/wsu_dmc_forms/wsu_irb_frequently_asked_questions.pdf` | 708,273 | modified on copy | `C:/Users/grego/OneDrive/Desktop/IRB/IRB Frequently Asked Questions - Institutional Review Board.pdf` |  |
| `regulatory/wsu_dmc_forms/wsu_irb_mandatory_citi_training.pdf` | 352,583 | modified on copy | `C:/Users/grego/OneDrive/Desktop/IRB/Mandatory CITI training - Institutional Review Board.pdf` |  |
| `regulatory/wsu_dmc_forms/wsu_patent_policy.pdf` | 73,331 | same bytes | `C:/Users/grego/OneDrive/Desktop/wsu_patent_policy.pdf` |  |
| `regulatory/wsu_dmc_forms/x-ray_machine_registration_form.docx` | 72,268 | modified on copy | `C:/Users/grego/OneDrive/Desktop/x-ray_machine_registration_form.doc` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_cv5_mixed_2026-09-21.json` | 22,030 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_cv5_mixed_2026-09-21.json` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_ft_mix_test_2026-09-21.json` | 20,848 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_ft_mix_test_2026-09-21.json` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_ft_realonly_test_2026-09-21.json` | 21,269 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_ft_realonly_test_2026-09-21.json` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_ftdet_multi_test_2026-09-22.json` | 10,713 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_ftdet_multi_test_2026-09-22.json` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_ftdet_pooled_test_2026-09-22.json` | 10,436 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_ftdet_pooled_test_2026-09-22.json` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_zeroshot2_pooled_all_2026-09-21.json` | 22,160 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_zeroshot2_pooled_all_2026-09-21.json` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_zeroshot2_test_2026-09-21.json` | 21,428 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_zeroshot2_test_2026-09-21.json` |  |
| `results/carmlspine_v2_lineage_2026-09-21/carmlspine_zeroshot_pooled_2026-09-21.json` | 22,189 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/carmlspine_zeroshot_pooled_2026-09-21.json` |  |
| `results/physics/link_probe/ctsp.json` | 3,356 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/link_probe/ctsp.json` |  |
| `results/physics/link_probe/ctsp_band.json` | 3,992 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/link_probe/ctsp_band.json` |  |
| `results/physics/link_probe/ctsp_cover.json` | 4,025 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/link_probe/ctsp_cover.json` |  |
| `results/physics/link_probe/ctsp_hpsweep.json` | 5,707 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/link_probe/ctsp_hpsweep.json` |  |
| `results/physics/link_probe/ctsp_mhp.json` | 4,355 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/link_probe/ctsp_mhp.json` |  |
| `results/physics/link_probe/ctsp_tight.json` | 4,354 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/link_probe/ctsp_tight.json` |  |
| `results/physics/link_probe/levels.json` | 642 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/link_probe/levels.json` |  |
| `results/physics/phys_best/ctsp_phys_ov2_exp10.json` | 6,850 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_best/ctsp_phys_ov2_exp10.json` |  |
| `results/physics/phys_best/ctsp_phys_ov2_exp4.json` | 6,845 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_best/ctsp_phys_ov2_exp4.json` |  |
| `results/physics/phys_best/ctsp_phys_ov3_exp4.json` | 6,845 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_best/ctsp_phys_ov3_exp4.json` |  |
| `results/physics/phys_best/ctsp_phys_ov4_gridnone.json` | 6,871 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_best/ctsp_phys_ov4_gridnone.json` |  |
| `results/physics/phys_best/verse_phys_ov4.json` | 6,507 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_best/verse_phys_ov4.json` |  |
| `results/physics/phys_detconf/film_conf0.05.json` | 7,011 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/film_conf0.05.json` |  |
| `results/physics/phys_detconf/film_conf0.25.json` | 7,009 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/film_conf0.25.json` |  |
| `results/physics/phys_detconf/phys_conf0.02.json` | 7,007 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/phys_conf0.02.json` |  |
| `results/physics/phys_detconf/phys_conf0.05.json` | 7,002 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/phys_conf0.05.json` |  |
| `results/physics/phys_detconf/phys_conf0.05_norepair.json` | 7,017 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/phys_conf0.05_norepair.json` |  |
| `results/physics/phys_detconf/phys_conf0.10.json` | 6,976 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/phys_conf0.10.json` |  |
| `results/physics/phys_detconf/phys_conf0.25.json` | 6,447 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/phys_conf0.25.json` |  |
| `results/physics/phys_detconf/phys_exp4_conf0.05.json` | 6,767 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detconf/phys_exp4_conf0.05.json` |  |
| `results/physics/phys_detector/ctsp_film_ov2_det.json` | 7,014 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detector/ctsp_film_ov2_det.json` |  |
| `results/physics/phys_detector/ctsp_film_ov2_gt.json` | 6,244 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detector/ctsp_film_ov2_gt.json` |  |
| `results/physics/phys_detector/ctsp_phys_ov2_det.json` | 6,452 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detector/ctsp_phys_ov2_det.json` |  |
| `results/physics/phys_detector/ctsp_phys_ov2_exp4_det.json` | 6,727 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detector/ctsp_phys_ov2_exp4_det.json` |  |
| `results/physics/phys_detector/ctsp_phys_ov2_gt.json` | 6,875 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detector/ctsp_phys_ov2_gt.json` |  |
| `results/physics/phys_detector/ctsp_phys_ov4_det.json` | 6,232 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_detector/ctsp_phys_ov4_det.json` |  |
| `results/physics/phys_global/ctsp_phys_ov2_global.json` | 6,889 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_global/ctsp_phys_ov2_global.json` |  |
| `results/physics/phys_global/ctsp_phys_ov3_global.json` | 6,889 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_global/ctsp_phys_ov3_global.json` |  |
| `results/physics/phys_global/ctsp_phys_ov3_pairwise.json` | 6,882 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_global/ctsp_phys_ov3_pairwise.json` |  |
| `results/physics/phys_global/ctsp_phys_ov4_pairwise.json` | 6,861 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_global/ctsp_phys_ov4_pairwise.json` |  |
| `results/physics/phys_global/verse_phys_ov4_global.json` | 6,522 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_global/verse_phys_ov4_global.json` |  |
| `results/physics/phys_jitter/ctsp_film_ov2_jit0.3.json` | 5,875 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_film_ov2_jit0.3.json` |  |
| `results/physics/phys_jitter/ctsp_film_ov2_jit0.5.json` | 6,450 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_film_ov2_jit0.5.json` |  |
| `results/physics/phys_jitter/ctsp_film_ov4_jit0.3.json` | 6,589 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_film_ov4_jit0.3.json` |  |
| `results/physics/phys_jitter/ctsp_film_ov4_jit0.5.json` | 6,583 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_film_ov4_jit0.5.json` |  |
| `results/physics/phys_jitter/ctsp_phys_ov2_jit0.3.json` | 6,847 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_phys_ov2_jit0.3.json` |  |
| `results/physics/phys_jitter/ctsp_phys_ov2_jit0.5.json` | 6,875 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_phys_ov2_jit0.5.json` |  |
| `results/physics/phys_jitter/ctsp_phys_ov4_jit0.3.json` | 6,867 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_phys_ov4_jit0.3.json` |  |
| `results/physics/phys_jitter/ctsp_phys_ov4_jit0.5.json` | 6,864 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_jitter/ctsp_phys_ov4_jit0.5.json` |  |
| `results/physics/phys_overlap/ctsp_film_ov2.json` | 6,150 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_film_ov2.json` |  |
| `results/physics/phys_overlap/ctsp_film_ov3.json` | 6,349 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_film_ov3.json` |  |
| `results/physics/phys_overlap/ctsp_film_ov4.json` | 6,372 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_film_ov4.json` |  |
| `results/physics/phys_overlap/ctsp_phys_ov2.json` | 6,829 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_phys_ov2.json` |  |
| `results/physics/phys_overlap/ctsp_phys_ov3.json` | 6,850 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_phys_ov3.json` |  |
| `results/physics/phys_overlap/ctsp_phys_ov4.json` | 6,853 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_phys_ov4.json` |  |
| `results/physics/phys_overlap/ctsp_phys_ov4_fpd.json` | 6,864 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_phys_ov4_fpd.json` |  |
| `results/physics/phys_overlap/ctsp_phys_ov4_grid_low.json` | 6,858 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_phys_ov4_grid_low.json` |  |
| `results/physics/phys_overlap/ctsp_phys_ov4_grid_none.json` | 6,875 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/ctsp_phys_ov4_grid_none.json` |  |
| `results/physics/phys_overlap/verse_film_ov4.json` | 10,044 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/verse_film_ov4.json` |  |
| `results/physics/phys_overlap/verse_phys_ov3.json` | 6,519 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/verse_phys_ov3.json` |  |
| `results/physics/phys_overlap/verse_phys_ov4.json` | 6,510 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_overlap/verse_phys_ov4.json` |  |
| `results/physics/phys_tightlast/ctsp_film_ov2_tight.json` | 6,184 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_tightlast/ctsp_film_ov2_tight.json` |  |
| `results/physics/phys_tightlast/ctsp_phys_ov2_tight.json` | 6,866 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_tightlast/ctsp_phys_ov2_tight.json` |  |
| `results/physics/phys_tightlast/ctsp_phys_ov3_tight.json` | 6,864 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/phys_tightlast/ctsp_phys_ov3_tight.json` |  |
| `results/physics/physics_figs/path_census.json` | 2,055 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/physics_figs/path_census.json` |  |
| `results/physics/physics_figs/validation.json` | 3,290 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/physics_figs/validation.json` |  |
| `results/physics/physics_figs/validation_flat.json` | 4,911 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/physics_figs/validation_flat.json` |  |
| `results/physics/physics_figs/validation_flat2.json` | 2,744 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/physics_figs/validation_flat2.json` |  |
| `results/physics/physics_figs/validation_matched.json` | 4,639 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/physics_figs/validation_matched.json` |  |
| `results/physics/physics_figs/validation_nps.json` | 3,291 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/physics_figs/validation_nps.json` |  |
| `results/physics/recover/ctsp_circ_all.json` | 6,483 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_circ_all.json` |  |
| `results/physics/recover/ctsp_circ_hp.json` | 6,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_circ_hp.json` |  |
| `results/physics/recover/ctsp_circ_mask.json` | 6,059 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_circ_mask.json` |  |
| `results/physics/recover/ctsp_circ_mask_hp.json` | 6,662 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_circ_mask_hp.json` |  |
| `results/physics/recover/ctsp_circ_none.json` | 6,664 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_circ_none.json` |  |
| `results/physics/recover/ctsp_circ_span.json` | 6,676 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_circ_span.json` |  |
| `results/physics/recover/ctsp_phys_hp.json` | 6,678 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_phys_hp.json` |  |
| `results/physics/recover/ctsp_phys_none.json` | 6,690 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_phys_none.json` |  |
| `results/physics/recover/ctsp_physcirc_all.json` | 6,738 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_all.json` |  |
| `results/physics/recover/ctsp_physcirc_all124.json` | 6,687 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_all124.json` |  |
| `results/physics/recover/ctsp_physcirc_grid_high.json` | 6,690 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_grid_high.json` |  |
| `results/physics/recover/ctsp_physcirc_grid_low.json` | 6,718 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_grid_low.json` |  |
| `results/physics/recover/ctsp_physcirc_grid_none.json` | 6,769 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_grid_none.json` |  |
| `results/physics/recover/ctsp_physcirc_hp.json` | 6,741 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_hp.json` |  |
| `results/physics/recover/ctsp_physcirc_mask.json` | 6,732 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_mask.json` |  |
| `results/physics/recover/ctsp_physcirc_none.json` | 6,733 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_none.json` |  |
| `results/physics/recover/ctsp_physcirc_worst.json` | 6,733 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_physcirc_worst.json` |  |
| `results/physics/recover/ctsp_square_film.json` | 6,392 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/ctsp_square_film.json` |  |
| `results/physics/recover/verse_circ_all.json` | 9,851 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/verse_circ_all.json` |  |
| `results/physics/recover/verse_circ_hp.json` | 9,837 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/verse_circ_hp.json` |  |
| `results/physics/recover/verse_circ_mask.json` | 8,474 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/verse_circ_mask.json` |  |
| `results/physics/recover/verse_circ_mask_hp.json` | 9,833 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/verse_circ_mask_hp.json` |  |
| `results/physics/recover/verse_circ_none.json` | 9,825 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/verse_circ_none.json` |  |
| `results/physics/recover/verse_square_film.json` | 8,475 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/recover/verse_square_film.json` |  |
| `results/physics/regression/ctsp_square_film.json` | 6,574 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/regression/ctsp_square_film.json` |  |
| `results/physics/regression/verse_square_film.json` | 8,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/results/physics/regression/verse_square_film.json` |  |
| `results/schwingnet/ALPHABET_LOSS.md` | 43,922 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/ALPHABET_LOSS.md` |  |
| `results/schwingnet/COUNTING.md` | 35,282 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/COUNTING.md` |  |
| `results/schwingnet/COUNTING_CHECK.md` | 13,875 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/COUNTING_CHECK.md` |  |
| `results/schwingnet/COUPLING.md` | 83,596 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/COUPLING.md` |  |
| `results/schwingnet/COUPLING_CHECK.md` | 19,276 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/COUPLING_CHECK.md` |  |
| `results/schwingnet/DATA_CONTRIBUTION.md` | 36,297 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/DATA_CONTRIBUTION.md` |  |
| `results/schwingnet/GROUNDWORK_CHECK.md` | 5,898 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/GROUNDWORK_CHECK.md` |  |
| `results/schwingnet/JOBS.txt` | 1,287 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/JOBS.txt` |  |
| `results/schwingnet/JOBS_cobra.txt` | 2,150 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/JOBS_cobra.txt` |  |
| `results/schwingnet/JOBS_data_repairs.txt` | 49,261 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/JOBS_data_repairs.txt` |  |
| `results/schwingnet/MANIFOLD_LEARNING_CHECK.md` | 8,405 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/MANIFOLD_LEARNING_CHECK.md` |  |
| `results/schwingnet/RIGOR_FIXES.md` | 45,134 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/RIGOR_FIXES.md` |  |
| `results/schwingnet/a1.json` | 68,404 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a1.json` |  |
| `results/schwingnet/a2.json` | 8,757 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a2.json` |  |
| `results/schwingnet/a3.json` | 31,998 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a3.json` |  |
| `results/schwingnet/a3a_rows.csv` | 31,059 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a3a_rows.csv` |  |
| `results/schwingnet/a3a_rows_meta.json` | 532 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a3a_rows_meta.json` |  |
| `results/schwingnet/a4.json` | 39,213 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a4.json` |  |
| `results/schwingnet/a5.json` | 64,334 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a5.json` |  |
| `results/schwingnet/a5_rows.csv` | 5,978,680 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a5_rows.csv` |  |
| `results/schwingnet/a5_rows_meta.json` | 3,643 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a5_rows_meta.json` |  |
| `results/schwingnet/a6.json` | 14,047 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a6.json` |  |
| `results/schwingnet/a7.json` | 277,024 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a7.json` |  |
| `results/schwingnet/a9.json` | 12,872 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/a9.json` |  |
| `results/schwingnet/age_sex_by_source.json` | 19,392 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/age_sex_by_source.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x19, CTSpinoPelvic1K: x1) |
| `results/schwingnet/age_sex_by_source.md` | 10,723 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/age_sex_by_source.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x17, CTSpinoPelvic1K: x1) |
| `results/schwingnet/alpha_0.3_seed0/a5.json` | 64,190 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed0/a5.json` |  |
| `results/schwingnet/alpha_0.3_seed0/a5_rows.csv` | 5,780,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed0/a5_rows.csv` |  |
| `results/schwingnet/alpha_0.3_seed0/a5_rows_meta.json` | 3,661 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed0/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_0.3_seed0/head_allspine_v9_mixed_kmax4_alpha0.3_seed0.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed0/head_allspine_v9_mixed_kmax4_alpha0.3_seed0.arch.json` |  |
| `results/schwingnet/alpha_0.3_seed0/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed0.json` | 16,993 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed0/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed0.json` |  |
| `results/schwingnet/alpha_0.3_seed1/a5.json` | 64,353 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed1/a5.json` |  |
| `results/schwingnet/alpha_0.3_seed1/a5_rows.csv` | 5,780,674 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed1/a5_rows.csv` |  |
| `results/schwingnet/alpha_0.3_seed1/a5_rows_meta.json` | 3,662 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed1/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_0.3_seed1/head_allspine_v9_mixed_kmax4_alpha0.3_seed1.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed1/head_allspine_v9_mixed_kmax4_alpha0.3_seed1.arch.json` |  |
| `results/schwingnet/alpha_0.3_seed1/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed1.json` | 16,985 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed1/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed1.json` |  |
| `results/schwingnet/alpha_0.3_seed2/a5.json` | 64,260 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed2/a5.json` |  |
| `results/schwingnet/alpha_0.3_seed2/a5_rows.csv` | 5,780,761 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed2/a5_rows.csv` |  |
| `results/schwingnet/alpha_0.3_seed2/a5_rows_meta.json` | 3,663 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed2/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_0.3_seed2/head_allspine_v9_mixed_kmax4_alpha0.3_seed2.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed2/head_allspine_v9_mixed_kmax4_alpha0.3_seed2.arch.json` |  |
| `results/schwingnet/alpha_0.3_seed2/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed2.json` | 16,999 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed2/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed2.json` |  |
| `results/schwingnet/alpha_0_seed0/a5.json` | 64,281 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed0/a5.json` |  |
| `results/schwingnet/alpha_0_seed0/a5_rows.csv` | 5,780,625 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed0/a5_rows.csv` |  |
| `results/schwingnet/alpha_0_seed0/a5_rows_meta.json` | 3,655 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed0/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_0_seed0/head_allspine_v9_mixed_kmax4_alpha0_seed0.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed0/head_allspine_v9_mixed_kmax4_alpha0_seed0.arch.json` |  |
| `results/schwingnet/alpha_0_seed0/mixed_allspine_v9_mixed_kmax4_alpha0_seed0.json` | 13,808 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed0/mixed_allspine_v9_mixed_kmax4_alpha0_seed0.json` |  |
| `results/schwingnet/alpha_0_seed1/a5.json` | 64,282 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed1/a5.json` |  |
| `results/schwingnet/alpha_0_seed1/a5_rows.csv` | 5,780,704 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed1/a5_rows.csv` |  |
| `results/schwingnet/alpha_0_seed1/a5_rows_meta.json` | 3,659 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed1/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_0_seed1/head_allspine_v9_mixed_kmax4_alpha0_seed1.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed1/head_allspine_v9_mixed_kmax4_alpha0_seed1.arch.json` |  |
| `results/schwingnet/alpha_0_seed1/mixed_allspine_v9_mixed_kmax4_alpha0_seed1.json` | 13,799 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed1/mixed_allspine_v9_mixed_kmax4_alpha0_seed1.json` |  |
| `results/schwingnet/alpha_0_seed2/a5.json` | 64,287 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed2/a5.json` |  |
| `results/schwingnet/alpha_0_seed2/a5_rows.csv` | 5,780,754 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed2/a5_rows.csv` |  |
| `results/schwingnet/alpha_0_seed2/a5_rows_meta.json` | 3,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed2/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_0_seed2/head_allspine_v9_mixed_kmax4_alpha0_seed2.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed2/head_allspine_v9_mixed_kmax4_alpha0_seed2.arch.json` |  |
| `results/schwingnet/alpha_0_seed2/mixed_allspine_v9_mixed_kmax4_alpha0_seed2.json` | 13,820 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_0_seed2/mixed_allspine_v9_mixed_kmax4_alpha0_seed2.json` |  |
| `results/schwingnet/alpha_1.0_seed0/a5.json` | 63,938 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed0/a5.json` |  |
| `results/schwingnet/alpha_1.0_seed0/a5_rows.csv` | 5,780,691 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed0/a5_rows.csv` |  |
| `results/schwingnet/alpha_1.0_seed0/a5_rows_meta.json` | 3,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed0/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_1.0_seed0/head_allspine_v9_mixed_kmax4_alpha1.0_seed0.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed0/head_allspine_v9_mixed_kmax4_alpha1.0_seed0.arch.json` |  |
| `results/schwingnet/alpha_1.0_seed0/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed0.json` | 16,976 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed0/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed0.json` |  |
| `results/schwingnet/alpha_1.0_seed1/a5.json` | 64,019 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed1/a5.json` |  |
| `results/schwingnet/alpha_1.0_seed1/a5_rows.csv` | 5,780,638 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed1/a5_rows.csv` |  |
| `results/schwingnet/alpha_1.0_seed1/a5_rows_meta.json` | 3,660 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed1/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_1.0_seed1/head_allspine_v9_mixed_kmax4_alpha1.0_seed1.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed1/head_allspine_v9_mixed_kmax4_alpha1.0_seed1.arch.json` |  |
| `results/schwingnet/alpha_1.0_seed1/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed1.json` | 16,981 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed1/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed1.json` |  |
| `results/schwingnet/alpha_1.0_seed2/a5.json` | 64,235 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed2/a5.json` |  |
| `results/schwingnet/alpha_1.0_seed2/a5_rows.csv` | 5,780,747 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed2/a5_rows.csv` |  |
| `results/schwingnet/alpha_1.0_seed2/a5_rows_meta.json` | 3,663 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed2/a5_rows_meta.json` |  |
| `results/schwingnet/alpha_1.0_seed2/head_allspine_v9_mixed_kmax4_alpha1.0_seed2.arch.json` | 668 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed2/head_allspine_v9_mixed_kmax4_alpha1.0_seed2.arch.json` |  |
| `results/schwingnet/alpha_1.0_seed2/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed2.json` | 16,988 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alpha_1.0_seed2/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed2.json` |  |
| `results/schwingnet/alphabet_loss.json` | 634,439 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alphabet_loss.json` |  |
| `results/schwingnet/alphabet_loss_inputs/allspine_v8_bank_index.csv` | 1,910,891 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alphabet_loss_inputs/allspine_v8_bank_index.csv` |  |
| `results/schwingnet/alphabet_loss_inputs/allspine_v8_persons.json` | 3,682,333 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alphabet_loss_inputs/allspine_v8_persons.json` |  |
| `results/schwingnet/alphabet_loss_inputs/allspine_v9_bank_index.csv` | 1,911,049 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alphabet_loss_inputs/allspine_v9_bank_index.csv` |  |
| `results/schwingnet/alphabet_loss_inputs/allspine_v9_persons.json` | 3,681,848 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/alphabet_loss_inputs/allspine_v9_persons.json` |  |
| `results/schwingnet/anomalous_inventory.json` | 18,484 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/anomalous_inventory.json` |  |
| `results/schwingnet/anomalous_inventory.md` | 1,124 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/anomalous_inventory.md` |  |
| `results/schwingnet/arc/ARC_CHECK.md` | 11,050 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/ARC_CHECK.md` |  |
| `results/schwingnet/arc/audit/pose_pools.json` | 37,567 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/audit/pose_pools.json` |  |
| `results/schwingnet/arc/audit/pose_pools.md` | 1,085 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/audit/pose_pools.md` |  |
| `results/schwingnet/arc/audit/pose_pools.png` | 133,018 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/audit/pose_pools.png` |  |
| `results/schwingnet/arc/case134_sweep.json` | 21,400 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/case134_sweep.json` |  |
| `results/schwingnet/arc/case134_sweep.md` | 6,924 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/case134_sweep.md` |  |
| `results/schwingnet/arc/fig_case134_recall_vs_angle.png` | 164,348 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/fig_case134_recall_vs_angle.png` |  |
| `results/schwingnet/arc/frame_00_truth.png` | 643,950 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/frame_00_truth.png` |  |
| `results/schwingnet/arc/frame_45_truth.png` | 573,982 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/frame_45_truth.png` |  |
| `results/schwingnet/arc/frame_90_truth.png` | 522,803 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/frame_90_truth.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+000.jpg` | 168,446 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+000.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+000_boxes.png` | 511,428 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+000_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+010.jpg` | 164,650 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+010.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+010_boxes.png` | 504,899 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+010_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+020.jpg` | 147,500 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+020.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+020_boxes.png` | 467,873 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+020_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+030.jpg` | 127,277 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+030.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+030_boxes.png` | 427,423 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+030_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+040.jpg` | 158,791 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+040.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+040_boxes.png` | 512,495 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+040_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+050.jpg` | 145,882 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+050.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+050_boxes.png` | 483,257 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+050_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+060.jpg` | 132,477 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+060.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+060_boxes.png` | 450,060 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+060_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+070.jpg` | 115,630 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+070.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+070_boxes.png` | 405,948 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+070_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+080.jpg` | 123,257 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+080.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+080_boxes.png` | 427,212 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+080_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat+090.jpg` | 148,453 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+090.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat+090_boxes.png` | 495,632 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat+090_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-010.jpg` | 167,096 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-010.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-010_boxes.png` | 509,358 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-010_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-020.jpg` | 153,909 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-020.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-020_boxes.png` | 487,387 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-020_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-030.jpg` | 134,615 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-030.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-030_boxes.png` | 453,791 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-030_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-040.jpg` | 139,365 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-040.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-040_boxes.png` | 467,793 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-040_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-050.jpg` | 132,106 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-050.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-050_boxes.png` | 449,557 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-050_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-060.jpg` | 153,289 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-060.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-060_boxes.png` | 506,683 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-060_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-070.jpg` | 145,546 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-070.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-070_boxes.png` | 485,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-070_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-080.jpg` | 124,221 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-080.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-080_boxes.png` | 427,885 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-080_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/lat-090.jpg` | 132,336 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-090.jpg` |  |
| `results/schwingnet/arc/proof_surgio/lat-090_boxes.png` | 452,351 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/lat-090_boxes.png` |  |
| `results/schwingnet/arc/proof_surgio/proof.json` | 10,032 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/proof_surgio/proof.json` |  |
| `results/schwingnet/arc/recall_vs_angle_selection_leaked/README.md` | 4,990 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_selection_leaked/README.md` |  |
| `results/schwingnet/arc/recall_vs_angle_selection_leaked/fig_recall_vs_angle.png` | 444,038 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_selection_leaked/fig_recall_vs_angle.png` |  |
| `results/schwingnet/arc/recall_vs_angle_selection_leaked/recall_vs_angle.json` | 280,075 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_selection_leaked/recall_vs_angle.json` |  |
| `results/schwingnet/arc/recall_vs_angle_selection_leaked/recall_vs_angle.md` | 20,074 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_selection_leaked/recall_vs_angle.md` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/fig_old_vs_new.png` | 317,965 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/fig_old_vs_new.png` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/fig_recall_vs_angle.png` | 417,232 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/fig_recall_vs_angle.png` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/indep_check/grid_indep.py` | 8,996 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/indep_check/grid_indep.py` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/indep_check/indep_check.json` | 84,232 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/indep_check/indep_check.json` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/indep_check/sheet_new_elekta_xvi_lat+000.png` | 1,651,511 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/indep_check/sheet_new_elekta_xvi_lat+000.png` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/indep_check/sheet_new_surgio_b51_dr_lat-090.png` | 2,589,647 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/indep_check/sheet_new_surgio_b51_dr_lat-090.png` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/prior_check.json` | 198,348 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/prior_check.json` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/recall_vs_angle.json` | 305,739 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/recall_vs_angle.json` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/recall_vs_angle.md` | 53,987 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/recall_vs_angle.md` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/subjects.json` | 133,407 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/subjects.json` |  |
| `results/schwingnet/arc/recall_vs_angle_unseen/subjects.txt` | 240 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/arc/recall_vs_angle_unseen/subjects.txt` |  |
| `results/schwingnet/auto_reference/CALIBRATION.md` | 18,447 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/auto_reference/CALIBRATION.md` | added on the fix pass of 2026-10-08 (section 2.2); the rest of `auto_reference/` is project 02's |
| `results/schwingnet/bodybox_rescore/DONE` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/DONE` |  |
| `results/schwingnet/bodybox_rescore/MANIFEST.txt` | 7,021 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/MANIFEST.txt` |  |
| `results/schwingnet/bodybox_rescore/RESCORE.md` | 27,845 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/RESCORE.md` |  |
| `results/schwingnet/bodybox_rescore/RESCORE_CHECK.md` | 8,791 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/RESCORE_CHECK.md` |  |
| `results/schwingnet/bodybox_rescore/RESCORE_CHECK_rederivation.json` | 4,678 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/RESCORE_CHECK_rederivation.json` |  |
| `results/schwingnet/bodybox_rescore/check/rescore_check_verify.py` | 8,440 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/check/rescore_check_verify.py` |  |
| `results/schwingnet/bodybox_rescore/check/rescore_check_verify.sh` | 444 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/check/rescore_check_verify.sh` |  |
| `results/schwingnet/bodybox_rescore/check/verify_out.json` | 4,678 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/check/verify_out.json` |  |
| `results/schwingnet/bodybox_rescore/counting/lodo_cobra__cobra_test__bodytruth__0.25.json` | 480,551 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/counting/lodo_cobra__cobra_test__bodytruth__0.25.json` |  |
| `results/schwingnet/bodybox_rescore/counting/lodo_cobra__cobra_test__bodytruth__0.74.json` | 427,923 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/counting/lodo_cobra__cobra_test__bodytruth__0.74.json` |  |
| `results/schwingnet/bodybox_rescore/failures.txt` | 410 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/failures.txt` |  |
| `results/schwingnet/bodybox_rescore/grid/DONE` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/DONE` |  |
| `results/schwingnet/bodybox_rescore/grid/MANIFEST.txt` | 7,021 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/MANIFEST.txt` |  |
| `results/schwingnet/bodybox_rescore/grid/counting/lodo_cobra__cobra_test__bodytruth__0.25.json` | 480,551 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/counting/lodo_cobra__cobra_test__bodytruth__0.25.json` |  |
| `results/schwingnet/bodybox_rescore/grid/counting/lodo_cobra__cobra_test__bodytruth__0.74.json` | 427,923 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/counting/lodo_cobra__cobra_test__bodytruth__0.74.json` |  |
| `results/schwingnet/bodybox_rescore/grid/failures.txt` | 410 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/failures.txt` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` | 22,714 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` | 21,586 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion__cobra_test.json` | 22,733 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` | 22,696 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` | 22,531 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` | 21,548 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` | 22,807 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` | 22,879 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` | 22,540 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` | 22,720 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` | 22,776 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` | 22,758 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` | 22,696 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_cios_fusion__cobra_test.json` | 22,743 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` | 22,747 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` | 22,871 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` | 22,745 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/devcorpus__dc_P_pooled__cobra_test.json` | 22,594 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/devcorpus__dc_P_pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` | 22,723 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` | 22,760 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` | 22,755 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` | 22,760 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` | 22,757 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` | 22,738 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` | 22,789 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/sweeps__lodo_carm__cobra_test.json` | 22,699 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/sweeps__lodo_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/sweeps__lodo_cobra__cobra_test.json` | 22,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/sweeps__lodo_cobra__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/sweeps__lodo_df__cobra_test.json` | 22,685 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/sweeps__lodo_df__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/sweeps__only_carm__cobra_test.json` | 21,240 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/sweeps__only_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/sweeps__only_carm_multi__cobra_test.json` | 20,772 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/sweeps__only_carm_multi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/sweeps__pooled__cobra_test.json` | 22,631 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/sweeps__pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_body/sweeps__render__cobra_test.json` | 22,445 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_body/sweeps__render__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` | 8,485 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` | 8,115 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion__cobra_test.json` | 8,444 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` | 8,442 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` | 8,509 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` | 8,097 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` | 8,466 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` | 8,476 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` | 8,518 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` | 8,491 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` | 8,523 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` | 8,455 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` | 8,445 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_cios_fusion__cobra_test.json` | 8,451 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` | 8,457 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` | 8,497 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` | 8,461 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/devcorpus__dc_P_pooled__cobra_test.json` | 8,378 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/devcorpus__dc_P_pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` | 8,444 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` | 8,447 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` | 8,453 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` | 8,451 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` | 8,448 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` | 8,438 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` | 8,465 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/sweeps__lodo_carm__cobra_test.json` | 8,403 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/sweeps__lodo_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/sweeps__lodo_cobra__cobra_test.json` | 8,460 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/sweeps__lodo_cobra__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/sweeps__lodo_df__cobra_test.json` | 8,395 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/sweeps__lodo_df__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/sweeps__only_carm__cobra_test.json` | 7,931 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/sweeps__only_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/sweeps__only_carm_multi__cobra_test.json` | 7,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/sweeps__only_carm_multi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/sweeps__pooled__cobra_test.json` | 8,383 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/sweeps__pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/scored_wv/sweeps__render__cobra_test.json` | 8,406 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/scored_wv/sweeps__render__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/grid/truth_build.json` | 25,946 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/truth_build.json` |  |
| `results/schwingnet/bodybox_rescore/grid/truth_build.stamp` | 15 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/grid/truth_build.stamp` |  |
| `results/schwingnet/bodybox_rescore/rescore.json` | 59,903 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/rescore.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` | 22,714 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` | 21,586 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion__cobra_test.json` | 22,733 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` | 22,696 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` | 22,531 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` | 21,548 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` | 22,807 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` | 22,879 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` | 22,540 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` | 22,720 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` | 22,776 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` | 22,758 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` | 22,696 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_B_held_cios_fusion__cobra_test.json` | 22,743 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_B_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` | 22,747 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` | 22,871 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` | 22,745 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/devcorpus__dc_P_pooled__cobra_test.json` | 22,594 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/devcorpus__dc_P_pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` | 22,723 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` | 22,760 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` | 22,755 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` | 22,760 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` | 22,757 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` | 22,738 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` | 22,789 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/sweeps__lodo_carm__cobra_test.json` | 22,699 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/sweeps__lodo_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/sweeps__lodo_cobra__cobra_test.json` | 22,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/sweeps__lodo_cobra__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/sweeps__lodo_df__cobra_test.json` | 22,685 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/sweeps__lodo_df__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/sweeps__only_carm__cobra_test.json` | 21,240 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/sweeps__only_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/sweeps__only_carm_multi__cobra_test.json` | 20,772 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/sweeps__only_carm_multi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/sweeps__pooled__cobra_test.json` | 22,631 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/sweeps__pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_body/sweeps__render__cobra_test.json` | 22,445 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_body/sweeps__render__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` | 8,485 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` | 8,115 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion__cobra_test.json` | 8,444 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` | 8,442 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` | 8,509 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` | 8,097 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi_1dev_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` | 8,466 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` | 8,476 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_elekta_xvi_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` | 8,518 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` | 8,491 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` | 8,523 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` | 8,455 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` | 8,445 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_A_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_B_held_cios_fusion__cobra_test.json` | 8,451 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_B_held_cios_fusion__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` | 8,457 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_B_held_cios_fusion_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` | 8,497 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_B_held_elekta_xvi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` | 8,461 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_B_held_surgio_b51_dr_s1__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/devcorpus__dc_P_pooled__cobra_test.json` | 8,378 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/devcorpus__dc_P_pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` | 8,444 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N0_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` | 8,447 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N100_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` | 8,453 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N100_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` | 8,451 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N200_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` | 8,448 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N400_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` | 8,438 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N400_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` | 8,465 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/lcdumps__lc_elekta_xvi_N50_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/sweeps__lodo_carm__cobra_test.json` | 8,403 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/sweeps__lodo_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/sweeps__lodo_cobra__cobra_test.json` | 8,460 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/sweeps__lodo_cobra__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/sweeps__lodo_df__cobra_test.json` | 8,395 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/sweeps__lodo_df__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/sweeps__only_carm__cobra_test.json` | 7,931 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/sweeps__only_carm__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/sweeps__only_carm_multi__cobra_test.json` | 7,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/sweeps__only_carm_multi__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/sweeps__pooled__cobra_test.json` | 8,383 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/sweeps__pooled__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/scored_wv/sweeps__render__cobra_test.json` | 8,406 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/scored_wv/sweeps__render__cobra_test.json` |  |
| `results/schwingnet/bodybox_rescore/truth_build.stamp` | 15 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/bodybox_rescore/truth_build.stamp` |  |
| `results/schwingnet/carmlspine_day_groups.json` | 3,075 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/carmlspine_day_groups.json` |  |
| `results/schwingnet/cine/tracker_config.json` | 1,891 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cine/tracker_config.json` |  |
| `results/schwingnet/cobra_lstv_screen.json` | 3,643 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_lstv_screen.json` |  |
| `results/schwingnet/cobra_lstv_screen.md` | 2,847 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_lstv_screen.md` |  |
| `results/schwingnet/cobra_window/CHECK.md` | 8,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/CHECK.md` |  |
| `results/schwingnet/cobra_window/DIAGNOSIS.md` | 7,594 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/DIAGNOSIS.md` |  |
| `results/schwingnet/cobra_window/FIX.md` | 9,646 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/FIX.md` |  |
| `results/schwingnet/cobra_window/aggregates.json` | 2,091 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/aggregates.json` |  |
| `results/schwingnet/cobra_window/frames_shard00.csv` | 110,139 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard00.csv` |  |
| `results/schwingnet/cobra_window/frames_shard01.csv` | 101,352 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard01.csv` |  |
| `results/schwingnet/cobra_window/frames_shard02.csv` | 101,225 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard02.csv` |  |
| `results/schwingnet/cobra_window/frames_shard03.csv` | 102,049 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard03.csv` |  |
| `results/schwingnet/cobra_window/frames_shard04.csv` | 100,475 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard04.csv` |  |
| `results/schwingnet/cobra_window/frames_shard05.csv` | 101,912 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard05.csv` |  |
| `results/schwingnet/cobra_window/frames_shard06.csv` | 100,974 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard06.csv` |  |
| `results/schwingnet/cobra_window/frames_shard07.csv` | 102,301 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard07.csv` |  |
| `results/schwingnet/cobra_window/frames_shard08.csv` | 100,986 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard08.csv` |  |
| `results/schwingnet/cobra_window/frames_shard09.csv` | 101,199 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard09.csv` |  |
| `results/schwingnet/cobra_window/frames_shard10.csv` | 102,063 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard10.csv` |  |
| `results/schwingnet/cobra_window/frames_shard11.csv` | 100,542 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/frames_shard11.csv` |  |
| `results/schwingnet/cobra_window/panel.json` | 32,666 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/panel.json` |  |
| `results/schwingnet/cobra_window/panel_geometry.csv` | 10,084 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/panel_geometry.csv` |  |
| `results/schwingnet/cobra_window/r2_body_vs_field.csv` | 86,407 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/r2_body_vs_field.csv` |  |
| `results/schwingnet/cobra_window/r2_body_vs_field.json` | 2,618 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/r2_body_vs_field.json` |  |
| `results/schwingnet/cobra_window/strips/strip_A_ap.png` | 188,124 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/strips/strip_A_ap.png` |  |
| `results/schwingnet/cobra_window/strips/strip_A_lat.png` | 155,068 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/strips/strip_A_lat.png` |  |
| `results/schwingnet/cobra_window/strips/strip_A_obl45.png` | 158,389 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/strips/strip_A_obl45.png` |  |
| `results/schwingnet/cobra_window/strips/strip_B_ap.png` | 174,914 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/strips/strip_B_ap.png` |  |
| `results/schwingnet/cobra_window/strips/strip_B_lat.png` | 87,593 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/strips/strip_B_lat.png` |  |
| `results/schwingnet/cobra_window/strips/strip_B_obl45.png` | 120,326 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/strips/strip_B_obl45.png` |  |
| `results/schwingnet/cobra_window/strips/strips.json` | 1,686 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/strips/strips.json` |  |
| `results/schwingnet/cobra_window/v3_eval/lodo_cobra_v1_minvis0.0.json` | 230,942 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/lodo_cobra_v1_minvis0.0.json` |  |
| `results/schwingnet/cobra_window/v3_eval/lodo_cobra_v1_minvis0.5.json` | 230,942 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/lodo_cobra_v1_minvis0.5.json` |  |
| `results/schwingnet/cobra_window/v3_eval/lodo_cobra_v1_minvis0.75.json` | 230,892 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/lodo_cobra_v1_minvis0.75.json` |  |
| `results/schwingnet/cobra_window/v3_eval/lodo_cobra_v3_minvis0.0.json` | 230,940 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/lodo_cobra_v3_minvis0.0.json` |  |
| `results/schwingnet/cobra_window/v3_eval/lodo_cobra_v3_minvis0.5.json` | 230,940 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/lodo_cobra_v3_minvis0.5.json` |  |
| `results/schwingnet/cobra_window/v3_eval/lodo_cobra_v3_minvis0.75.json` | 230,878 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/lodo_cobra_v3_minvis0.75.json` |  |
| `results/schwingnet/cobra_window/v3_eval/pooled_v1_minvis0.0.json` | 230,768 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/pooled_v1_minvis0.0.json` |  |
| `results/schwingnet/cobra_window/v3_eval/pooled_v1_minvis0.5.json` | 230,768 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/pooled_v1_minvis0.5.json` |  |
| `results/schwingnet/cobra_window/v3_eval/pooled_v1_minvis0.75.json` | 230,753 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/pooled_v1_minvis0.75.json` |  |
| `results/schwingnet/cobra_window/v3_eval/pooled_v3_minvis0.0.json` | 230,758 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/pooled_v3_minvis0.0.json` |  |
| `results/schwingnet/cobra_window/v3_eval/pooled_v3_minvis0.5.json` | 230,758 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/pooled_v3_minvis0.5.json` |  |
| `results/schwingnet/cobra_window/v3_eval/pooled_v3_minvis0.75.json` | 230,757 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/pooled_v3_minvis0.75.json` |  |
| `results/schwingnet/cobra_window/v3_eval/render_v1_minvis0.0.json` | 230,841 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/render_v1_minvis0.0.json` |  |
| `results/schwingnet/cobra_window/v3_eval/render_v1_minvis0.5.json` | 230,841 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/render_v1_minvis0.5.json` |  |
| `results/schwingnet/cobra_window/v3_eval/render_v1_minvis0.75.json` | 230,813 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/render_v1_minvis0.75.json` |  |
| `results/schwingnet/cobra_window/v3_eval/render_v3_minvis0.0.json` | 230,851 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/render_v3_minvis0.0.json` |  |
| `results/schwingnet/cobra_window/v3_eval/render_v3_minvis0.5.json` | 230,851 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/render_v3_minvis0.5.json` |  |
| `results/schwingnet/cobra_window/v3_eval/render_v3_minvis0.75.json` | 230,810 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/cobra_window/v3_eval/render_v3_minvis0.75.json` |  |
| `results/schwingnet/contribution_matrix.json` | 233,679 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/contribution_matrix.json` |  |
| `results/schwingnet/contribution_matrix.md` | 43,261 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/contribution_matrix.md` |  |
| `results/schwingnet/corpus_census.json` | 127,088 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/corpus_census.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1, laptop-scratchpad: x1) |
| `results/schwingnet/corpus_census.md` | 39,033 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/corpus_census.md` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `results/schwingnet/corpus_manifold/embedding.csv` | 2,176,792 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/corpus_manifold/embedding.csv` |  |
| `results/schwingnet/corpus_manifold/overlap.json` | 18,399 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/corpus_manifold/overlap.json` |  |
| `results/schwingnet/counting.json` | 170,520 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting.json` |  |
| `results/schwingnet/counting/dc_A_held_cios_fusion__df_all6__body__0.25.json` | 426,812 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_cios_fusion__df_all6__body__0.25.json` |  |
| `results/schwingnet/counting/dc_A_held_cios_fusion__df_test__body__0.25.json` | 110,321 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_cios_fusion__df_test__body__0.25.json` |  |
| `results/schwingnet/counting/dc_A_held_cios_fusion_s1__df_all6__body__0.25.json` | 442,197 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_cios_fusion_s1__df_all6__body__0.25.json` |  |
| `results/schwingnet/counting/dc_A_held_cios_fusion_s1__df_test__body__0.25.json` | 116,116 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_cios_fusion_s1__df_test__body__0.25.json` |  |
| `results/schwingnet/counting/dc_A_held_elekta_xvi__cobra_test__body__0.25.json` | 604,324 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_elekta_xvi__cobra_test__body__0.25.json` |  |
| `results/schwingnet/counting/dc_A_held_elekta_xvi_s1__cobra_test__body__0.25.json` | 577,897 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_elekta_xvi_s1__cobra_test__body__0.25.json` |  |
| `results/schwingnet/counting/dc_A_held_surgio_b51_dr__carm_test__outline__0.25.json` | 142,436 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_surgio_b51_dr__carm_test__outline__0.25.json` |  |
| `results/schwingnet/counting/dc_A_held_surgio_b51_dr_s1__carm_test__outline__0.25.json` | 148,008 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_A_held_surgio_b51_dr_s1__carm_test__outline__0.25.json` |  |
| `results/schwingnet/counting/dc_B_held_cios_fusion__df_all6__body__0.25.json` | 445,892 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_B_held_cios_fusion__df_all6__body__0.25.json` |  |
| `results/schwingnet/counting/dc_B_held_cios_fusion__df_test__body__0.25.json` | 112,958 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_B_held_cios_fusion__df_test__body__0.25.json` |  |
| `results/schwingnet/counting/dc_B_held_cios_fusion_s1__df_all6__body__0.25.json` | 444,479 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_B_held_cios_fusion_s1__df_all6__body__0.25.json` |  |
| `results/schwingnet/counting/dc_B_held_cios_fusion_s1__df_test__body__0.25.json` | 115,797 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_B_held_cios_fusion_s1__df_test__body__0.25.json` |  |
| `results/schwingnet/counting/dc_B_held_elekta_xvi__cobra_test__body__0.25.json` | 610,168 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_B_held_elekta_xvi__cobra_test__body__0.25.json` |  |
| `results/schwingnet/counting/dc_B_held_surgio_b51_dr_s1__carm_test__outline__0.25.json` | 153,547 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/dc_B_held_surgio_b51_dr_s1__carm_test__outline__0.25.json` |  |
| `results/schwingnet/counting/lodo_carm__carm_test__body__0.25.json` | 135,983 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/lodo_carm__carm_test__body__0.25.json` |  |
| `results/schwingnet/counting/lodo_carm__carm_test__body__0.74.json` | 123,783 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/lodo_carm__carm_test__body__0.74.json` |  |
| `results/schwingnet/counting/lodo_carm__carm_test__outline__0.25.json` | 151,963 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/lodo_carm__carm_test__outline__0.25.json` |  |
| `results/schwingnet/counting/lodo_carm__carm_test__outline__0.74.json` | 136,924 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/lodo_carm__carm_test__outline__0.74.json` |  |
| `results/schwingnet/counting/lodo_cobra__cobra_test__body__0.25.json` | 476,589 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/lodo_cobra__cobra_test__body__0.25.json` |  |
| `results/schwingnet/counting/lodo_df__df_test__body__0.25.json` | 114,051 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/lodo_df__df_test__body__0.25.json` |  |
| `results/schwingnet/counting/pooled__carm_test__outline__0.25.json` | 146,234 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting/pooled__carm_test__outline__0.25.json` |  |
| `results/schwingnet/counting_check_hand.json` | 19,327 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting_check_hand.json` |  |
| `results/schwingnet/counting_example_case100_AP.png` | 766,084 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting_example_case100_AP.png` |  |
| `results/schwingnet/counting_example_case139_AP.png` | 752,780 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting_example_case139_AP.png` |  |
| `results/schwingnet/counting_outside_check.json` | 1,469 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/counting_outside_check.json` |  |
| `results/schwingnet/coupling.json` | 543,851 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling.json` |  |
| `results/schwingnet/coupling_c74/cv_fold0_det_kfull_couple_all.json` | 261,986 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_c74/cv_fold0_det_kfull_couple_all.json` |  |
| `results/schwingnet/coupling_c74/cv_fold1_det_kfull_couple_all.json` | 187,708 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_c74/cv_fold1_det_kfull_couple_all.json` |  |
| `results/schwingnet/coupling_c74/cv_fold2_det_kfull_couple_all.json` | 213,011 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_c74/cv_fold2_det_kfull_couple_all.json` |  |
| `results/schwingnet/coupling_c74/cv_fold3_det_kfull_couple_all.json` | 275,640 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_c74/cv_fold3_det_kfull_couple_all.json` |  |
| `results/schwingnet/coupling_c74/cv_fold4_det_kfull_couple_all.json` | 190,445 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_c74/cv_fold4_det_kfull_couple_all.json` |  |
| `results/schwingnet/coupling_check_dd/COUPLING.md` | 73,176 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_check_dd/COUPLING.md` |  |
| `results/schwingnet/coupling_check_dd/coupling.json` | 372,891 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_check_dd/coupling.json` |  |
| `results/schwingnet/coupling_check_split.json` | 8,330 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_check_split.json` |  |
| `results/schwingnet/coupling_check_v8_mixed.json` | 15,243 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coupling_check_v8_mixed.json` |  |
| `results/schwingnet/coverage/COVERAGE.md` | 71,371 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/COVERAGE.md` |  |
| `results/schwingnet/coverage/DICOM_VARIABLES.md` | 3,436 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/DICOM_VARIABLES.md` |  |
| `results/schwingnet/coverage/N_VS_COVERAGE_PLAN.md` | 7,967 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/N_VS_COVERAGE_PLAN.md` |  |
| `results/schwingnet/coverage/PENDING_JOBS.json` | 10,175 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/PENDING_JOBS.json` |  |
| `results/schwingnet/coverage/PER_LEVEL_DOMAIN_ANGLE.md` | 21,481 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` |  |
| `results/schwingnet/coverage/POOLED_FIT.md` | 6,137 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/POOLED_FIT.md` |  |
| `results/schwingnet/coverage/coverage.json` | 1,178,839 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/coverage.json` |  |
| `results/schwingnet/coverage/dimension/film_vs_fluoro_dimension.json` | 53,748 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/dimension/film_vs_fluoro_dimension.json` |  |
| `results/schwingnet/coverage/dimension/film_vs_fluoro_dimension.png` | 489,302 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/dimension/film_vs_fluoro_dimension.png` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_elekta_xvi_high_s0` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_elekta_xvi_high_s0` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_elekta_xvi_high_s1` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_elekta_xvi_high_s1` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_elekta_xvi_low2n_s0` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_elekta_xvi_low2n_s0` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_elekta_xvi_low2n_s1` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_elekta_xvi_low2n_s1` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_elekta_xvi_low_s0` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_elekta_xvi_low_s0` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_elekta_xvi_low_s1` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_elekta_xvi_low_s1` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_high_s0` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_high_s0` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_high_s1` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_high_s1` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low2n_s0` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low2n_s0` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low2n_s1` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low2n_s1` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low_s0` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low_s0` |  |
| `results/schwingnet/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low_s1` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/ARM_DONE_cov_surgio_b51_dr_low_s1` |  |
| `results/schwingnet/coverage/experiment/EXPERIMENT.md` | 2,055 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/EXPERIMENT.md` |  |
| `results/schwingnet/coverage/experiment/RENDER_DONE_elekta_xvi_arc` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/RENDER_DONE_elekta_xvi_arc` |  |
| `results/schwingnet/coverage/experiment/RENDER_DONE_elekta_xvi_low2` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/RENDER_DONE_elekta_xvi_low2` |  |
| `results/schwingnet/coverage/experiment/RENDER_DONE_surgio_b51_dr_arc` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/RENDER_DONE_surgio_b51_dr_arc` |  |
| `results/schwingnet/coverage/experiment/RENDER_DONE_surgio_b51_dr_low2` | 0 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/RENDER_DONE_surgio_b51_dr_low2` |  |
| `results/schwingnet/coverage/experiment/arms.json` | 16,393 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/arms.json` |  |
| `results/schwingnet/coverage/experiment/lists_elekta_xvi_s0.json` | 3,853 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/lists_elekta_xvi_s0.json` |  |
| `results/schwingnet/coverage/experiment/lists_elekta_xvi_s1.json` | 3,853 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/lists_elekta_xvi_s1.json` |  |
| `results/schwingnet/coverage/experiment/lists_surgio_b51_dr_s0.json` | 3,937 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/lists_surgio_b51_dr_s0.json` |  |
| `results/schwingnet/coverage/experiment/lists_surgio_b51_dr_s1.json` | 3,937 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/lists_surgio_b51_dr_s1.json` |  |
| `results/schwingnet/coverage/experiment/poses_elekta_xvi.json` | 984 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/poses_elekta_xvi.json` |  |
| `results/schwingnet/coverage/experiment/poses_surgio_b51_dr.json` | 984 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/poses_surgio_b51_dr.json` |  |
| `results/schwingnet/coverage/experiment/runs/.gitignore` | 30 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/.gitignore` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/args.yaml` | 1,840 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/case134/case134_sweep.json` | 9,067 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/case134/case134_sweep.md` | 3,710 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_carmlspine_test.json` | 1,318,706 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/results.csv` | 5,165 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/scores.json` | 17,573 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/scores_refused_40437813.json` | 2,283 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/unseen/recall_vs_angle.json` | 79,546 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s0/unseen/recall_vs_angle.md` | 8,046 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s0/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/args.yaml` | 1,840 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/case134/case134_sweep.json` | 9,067 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/case134/case134_sweep.md` | 3,710 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_carmlspine_test.json` | 1,484,411 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/results.csv` | 5,145 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/scores.json` | 17,573 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/scores_refused_40437813.json` | 2,283 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/unseen/recall_vs_angle.json` | 79,546 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_high_s1/unseen/recall_vs_angle.md` | 8,046 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_high_s1/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/args.yaml` | 1,843 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/case134/case134_sweep.json` | 9,076 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/case134/case134_sweep.md` | 3,714 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_carmlspine_test.json` | 644,796 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_deepfluoro_test.json` | 1,456,342 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/results.csv` | 5,150 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/scores.json` | 17,689 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/scores_refused_40437813.json` | 2,285 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/unseen/recall_vs_angle.json` | 81,910 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/unseen/recall_vs_angle.md` | 8,072 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s0/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/args.yaml` | 1,843 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/case134/case134_sweep.json` | 9,100 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/case134/case134_sweep.md` | 3,714 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_carmlspine_test.json` | 754,721 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_deepfluoro_test.json` | 1,171,499 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_geneva_hip_test.json` | 1,735,228 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/results.csv` | 5,126 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/scores.json` | 17,670 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/scores_refused_40437813.json` | 2,285 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/unseen/recall_vs_angle.json` | 82,402 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/unseen/recall_vs_angle.md` | 8,072 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low2n_s1/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/args.yaml` | 1,837 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/case134/case134_sweep.json` | 9,058 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/case134/case134_sweep.md` | 3,706 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_carmlspine_test.json` | 870,258 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_deepfluoro_test.json` | 1,486,155 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_geneva_hip_test.json` | 1,364,095 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/results.csv` | 5,161 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/scores.json` | 17,568 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/scores_refused_40437813.json` | 2,274 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/unseen/recall_vs_angle.json` | 79,538 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s0/unseen/recall_vs_angle.md` | 8,020 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s0/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/args.yaml` | 1,837 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/case134/case134_sweep.json` | 9,058 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/case134/case134_sweep.md` | 3,706 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_carmlspine_test.json` | 1,097,650 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_deepfluoro_test.json` | 2,065,683 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/results.csv` | 5,156 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/scores.json` | 17,570 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/scores_refused_40437813.json` | 2,274 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/unseen/recall_vs_angle.json` | 79,538 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_elekta_xvi_low_s1/unseen/recall_vs_angle.md` | 8,020 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_elekta_xvi_low_s1/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/args.yaml` | 1,849 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/case134/case134_sweep.json` | 9,154 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/case134/case134_sweep.md` | 3,723 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_carmlspine_test.json` | 452,994 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_deepfluoro_test.json` | 578,372 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_geneva_hip_test.json` | 695,978 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/results.csv` | 5,159 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/scores.json` | 18,222 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/scores_refused_40437813.json` | 2,314 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/unseen/recall_vs_angle.json` | 91,333 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/unseen/recall_vs_angle.md` | 8,120 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s0/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/args.yaml` | 1,849 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/case134/case134_sweep.json` | 9,138 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/case134/case134_sweep.md` | 3,723 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_carmlspine_test.json` | 798,547 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_deepfluoro_test.json` | 1,126,903 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_geneva_hip_test.json` | 1,035,118 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/results.csv` | 5,161 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/scores.json` | 18,220 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/scores_refused_40437813.json` | 2,314 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/unseen/recall_vs_angle.json` | 90,762 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/unseen/recall_vs_angle.md` | 8,119 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_high_s1/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/args.yaml` | 1,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/case134/case134_sweep.json` | 9,146 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/case134/case134_sweep.md` | 3,726 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_carmlspine_test.json` | 189,902 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_deepfluoro_test.json` | 271,825 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_geneva_hip_test.json` | 641,581 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/results.csv` | 5,148 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/scores.json` | 18,263 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/scores_refused_40437813.json` | 2,316 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/unseen/recall_vs_angle.json` | 93,403 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/unseen/recall_vs_angle.md` | 8,150 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s0/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/args.yaml` | 1,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/case134/case134_sweep.json` | 9,157 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/case134/case134_sweep.md` | 3,726 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_carmlspine_test.json` | 175,373 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_cobra_elekta_test.json` | 2,036,606 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_cobra_elekta_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_deepfluoro_test.json` | 242,240 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_geneva_hip_test.json` | 776,788 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/results.csv` | 5,138 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/scores.json` | 18,246 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/scores_refused_40437813.json` | 2,316 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/unseen/recall_vs_angle.json` | 93,472 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/unseen/recall_vs_angle.md` | 8,150 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low2n_s1/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/args.yaml` | 1,846 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/case134/case134_sweep.json` | 9,142 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/case134/case134_sweep.md` | 3,718 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_carmlspine_test.json` | 454,492 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_deepfluoro_test.json` | 518,251 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_geneva_hip_test.json` | 892,410 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/results.csv` | 5,143 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/scores.json` | 18,226 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/scores_refused_40437813.json` | 2,305 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/unseen/recall_vs_angle.json` | 90,760 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/unseen/recall_vs_angle.md` | 8,097 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s0/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/args.yaml` | 1,846 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/args.yaml` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/case134/case134_sweep.json` | 9,136 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/case134/case134_sweep.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/case134/case134_sweep.md` | 3,718 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/case134/case134_sweep.md` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_carmlspine_test.json` | 650,336 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_carmlspine_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_deepfluoro_test.json` | 420,039 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_deepfluoro_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_geneva_hip_test.json` | 611,664 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/eval_geneva_hip_test.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/results.csv` | 5,164 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/results.csv` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/scores.json` | 18,208 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/scores.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/scores_refused_40437813.json` | 2,305 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/scores_refused_40437813.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/unseen/recall_vs_angle.json` | 89,463 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/unseen/recall_vs_angle.json` |  |
| `results/schwingnet/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/unseen/recall_vs_angle.md` | 8,098 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/runs/cov_surgio_b51_dr_low_s1/unseen/recall_vs_angle.md` |  |
| `results/schwingnet/coverage/experiment/scores.json` | 41,923 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/scores.json` |  |
| `results/schwingnet/coverage/experiment/subjects.txt` | 852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/experiment/subjects.txt` |  |
| `results/schwingnet/coverage/fig_density.png` | 376,576 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/fig_density.png` |  |
| `results/schwingnet/coverage/fig_density_training.png` | 251,057 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/fig_density_training.png` |  |
| `results/schwingnet/coverage/film_ncurve/FILM_NCURVE.md` | 3,361 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/FILM_NCURVE.md` |  |
| `results/schwingnet/coverage/film_ncurve/ablation/READ.md` | 5,943 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/ablation/READ.md` |  |
| `results/schwingnet/coverage/film_ncurve/ablation/ablation_read.json` | 1,946 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/ablation/ablation_read.json` |  |
| `results/schwingnet/coverage/film_ncurve/ablation/filmonly/FILM_NCURVE.md` | 3,302 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/ablation/filmonly/FILM_NCURVE.md` |  |
| `results/schwingnet/coverage/film_ncurve/ablation/filmonly/film_ncurve.json` | 173,550 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/ablation/filmonly/film_ncurve.json` |  |
| `results/schwingnet/coverage/film_ncurve/ablation/imagenet/FILM_NCURVE.md` | 3,411 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/ablation/imagenet/FILM_NCURVE.md` |  |
| `results/schwingnet/coverage/film_ncurve/ablation/imagenet/film_ncurve.json` | 212,540 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/ablation/imagenet/film_ncurve.json` |  |
| `results/schwingnet/coverage/film_ncurve/film_ncurve.json` | 217,709 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/film_ncurve/film_ncurve.json` |  |
| `results/schwingnet/coverage/items.csv.gz` | 661,121 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/items.csv.gz` |  |
| `results/schwingnet/coverage/points_coverage.csv` | 132,741 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/points_coverage.csv` |  |
| `results/schwingnet/coverage/pooled_fit.json` | 307,417 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/pooled_fit.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x4) |
| `results/schwingnet/coverage/sensitivity/POOLED_FIT.md` | 6,330 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/sensitivity/POOLED_FIT.md` |  |
| `results/schwingnet/coverage/sensitivity/coverage_fit_conf074.json` | 318,337 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/sensitivity/coverage_fit_conf074.json` |  |
| `results/schwingnet/coverage/sensitivity/coverage_fit_trained_only.json` | 320,521 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/sensitivity/coverage_fit_trained_only.json` |  |
| `results/schwingnet/coverage/sensitivity/pooled_fit_conf074.json` | 302,359 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/sensitivity/pooled_fit_conf074.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x4) |
| `results/schwingnet/coverage/sensitivity/pooled_fit_trained_only.json` | 303,992 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/sensitivity/pooled_fit_trained_only.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x4) |
| `results/schwingnet/coverage/training_sets.csv` | 16,637 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/coverage/training_sets.csv` |  |
| `results/schwingnet/dc_P_pooled_scores.json` | 4,929 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/dc_P_pooled_scores.json` |  |
| `results/schwingnet/eval_gate/EVALUATORS.md` | 91,666 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/EVALUATORS.md` |  |
| `results/schwingnet/eval_gate/EVAL_LEAKS.md` | 179,344 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/EVAL_LEAKS.md` |  |
| `results/schwingnet/eval_gate/LINEAGE.md` | 105,814 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/LINEAGE.md` |  |
| `results/schwingnet/eval_gate/VERIFY.md` | 27,176 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/VERIFY.md` |  |
| `results/schwingnet/eval_gate/bounds.json` | 207,317 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/bounds.json` |  |
| `results/schwingnet/eval_gate/build_inventory.py` | 83,252 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/build_inventory.py` |  |
| `results/schwingnet/eval_gate/chk9/CHK9_REPORT.md` | 84,553 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/chk9/CHK9_REPORT.md` |  |
| `results/schwingnet/eval_gate/chk9/chk9_report.json` | 1,255,808 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/chk9/chk9_report.json` |  |
| `results/schwingnet/eval_gate/closure/MANUSCRIPT_CORRECTIONS.md` | 92,390 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/MANUSCRIPT_CORRECTIONS.md` |  |
| `results/schwingnet/eval_gate/closure/MANUSCRIPT_CORRECTIONS_ORDERED.md` | 9,644 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/MANUSCRIPT_CORRECTIONS_ORDERED.md` |  |
| `results/schwingnet/eval_gate/closure/VERIFY.md` | 11,268 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/VERIFY.md` |  |
| `results/schwingnet/eval_gate/closure/bypass/eval_sets.json` | 126,199 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/eval_sets.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/grid_jobs/closure_evalsets.sh` | 1,191 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_evalsets.sh` |  |
| `results/schwingnet/eval_gate/closure/bypass/grid_jobs/closure_install.sh` | 1,403 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_install.sh` |  |
| `results/schwingnet/eval_gate/closure/bypass/grid_jobs/closure_repro.py` | 13,803 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_repro.py` |  |
| `results/schwingnet/eval_gate/closure/bypass/grid_jobs/closure_repro.sh` | 8,481 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_repro.sh` |  |
| `results/schwingnet/eval_gate/closure/bypass/grid_jobs/closure_samefile.py` | 1,880 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_samefile.py` |  |
| `results/schwingnet/eval_gate/closure/bypass/grid_jobs/closure_samefile.sh` | 530 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_samefile.sh` |  |
| `results/schwingnet/eval_gate/closure/bypass/grid_jobs/closure_setup.sh` | 1,275 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_setup.sh` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/C_lcurve.json` | 25,599 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/C_lcurve.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/C_rx.json` | 122,359 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/C_rx.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/C_transplant.json` | 2,516 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/C_transplant.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/G1c_heldout_census.json` | 6,029 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/G1c_heldout_census.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/G1c_heldout_l6.npz.eval_gate.json` | 2,371 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/G1c_heldout_l6.npz.eval_gate.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/R1c_recall_vs_angle.json` | 310,116 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/R1c_recall_vs_angle.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/R1d_i/recall_vs_angle.json` | 309,676 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/R1d_i/recall_vs_angle.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/R1d_i/recall_vs_angle.md` | 20,491 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/R1d_i/recall_vs_angle.md` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/R1d_i_cells.json` | 447 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/R1d_i_cells.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/R2_carry.json` | 2,935 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/R2_carry.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/R3_keys.json` | 2,433 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/R3_keys.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/eval_sets_diff.json` | 7,539 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/eval_sets_diff.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/existing_blocks_audit.json` | 3,390 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/existing_blocks_audit.json` |  |
| `results/schwingnet/eval_gate/closure/bypass/out/samefile_lodo_carm.json` | 2,597 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/bypass/out/samefile_lodo_carm.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/case134_sweep.json` | 29,426 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/case134_sweep.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/case134_sweep.md` | 7,280 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/case134_sweep.md` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/fig_case134_recall_vs_angle.png` | 163,318 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/fig_case134_recall_vs_angle.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/frame_00_truth.png` | 643,950 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/frame_00_truth.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/frame_45_truth.png` | 573,982 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/frame_45_truth.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/frame_90_truth.png` | 522,803 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/frame_90_truth.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/gate_check_lodoA.json` | 1,808 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/gate_check_lodoA.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/gate_check_lodoB.json` | 1,811 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/gate_check_lodoB.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/gate_check_pooled.json` | 1,796 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/gate_check_pooled.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep/gate_check_real_lodo.json` | 1,906 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep/gate_check_real_lodo.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/case134_sweep.json` | 30,701 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/case134_sweep.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/case134_sweep.md` | 7,294 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/case134_sweep.md` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/fig_case134_recall_vs_angle.png` | 163,318 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/fig_case134_recall_vs_angle.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/frame_00_truth.png` | 643,950 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/frame_00_truth.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/frame_45_truth.png` | 573,982 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/frame_45_truth.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/frame_90_truth.png` | 522,803 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/frame_90_truth.png` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/gate_check_lodoA.json` | 2,031 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/gate_check_lodoA.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/gate_check_lodoB.json` | 2,034 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/gate_check_lodoB.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/gate_check_pooled.json` | 2,019 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/gate_check_pooled.json` |  |
| `results/schwingnet/eval_gate/closure/case134_sweep_eg2/gate_check_real_lodo.json` | 2,129 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/case134_sweep_eg2/gate_check_real_lodo.json` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/CHK9_DIFF.md` | 13,482 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/CHK9_DIFF.md` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/after/CHK9_REPORT.md` | 46,420 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/after/CHK9_REPORT.md` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/after/chk9_report.json` | 1,229,977 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/after/chk9_report.json` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/before/CHK9_REPORT.md` | 88,723 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/before/CHK9_REPORT.md` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/before/chk9_report.json` | 1,573,412 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/before/chk9_report.json` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/chk9_cv_v9.sh` | 3,935 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/chk9_cv_v9.sh` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/chk9_diff.json` | 29,036 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/chk9_diff.json` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/chk9_diff.py` | 5,288 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/chk9_diff.py` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/make_quoted_cv_v9.py` | 12,591 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/make_quoted_cv_v9.py` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/quoted_results_before.json` | 1,209,718 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/quoted_results_before.json` |  |
| `results/schwingnet/eval_gate/closure/chk9_cv_v9/quoted_results_cv_v9.json` | 1,277,936 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/chk9_cv_v9/quoted_results_cv_v9.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/CV_V9.md` | 80,999 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/CV_V9.md` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/MANUSCRIPT_CORRECTIONS_cv_v9.md` | 41,015 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/MANUSCRIPT_CORRECTIONS_cv_v9.md` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/carmlspine_cv5_v9init_pre.json` | 20,863 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/carmlspine_cv5_v9init_pre.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/carmlspine_cv5_v9init_rep.json` | 20,804 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/carmlspine_cv5_v9init_rep.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/carmlspine_cvday_v9init_pre.json` | 20,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/carmlspine_cvday_v9init_pre.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/carmlspine_cvday_v9init_rep.json` | 20,828 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/carmlspine_cvday_v9init_rep.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/closure_cv_v9.py` | 25,209 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/closure_cv_v9.py` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/closure_only.sh` | 1,688 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/closure_only.sh` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/collect_cv_v9.sh` | 3,464 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/collect_cv_v9.sh` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/coupling_pre/COUPLING.md` | 83,232 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/coupling_pre/COUPLING.md` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/coupling_pre/coupling.json` | 2,042,862 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/coupling_pre/coupling.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/coupling_rep/COUPLING.md` | 83,407 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/coupling_rep/COUPLING.md` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/coupling_rep/coupling.json` | 2,033,280 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/coupling_rep/coupling.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/cv_v9.json` | 825,801 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/cv_v9.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/cv_v9_extras.py` | 9,350 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/cv_v9_extras.py` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/cv_v9_extras.sh` | 807 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/cv_v9_extras.sh` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/cv_v9_extras_pre.json` | 33,117 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/cv_v9_extras_pre.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/cv_v9_extras_rep.json` | 32,705 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/cv_v9_extras_rep.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold0/det/kfull/couple_c74/couple_all.json` | 289,036 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold0/det/kfull/couple_c74/couple_all.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold1/det/kfull/couple_c74/couple_all.json` | 213,279 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold1/det/kfull/couple_c74/couple_all.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold2/det/kfull/case42_LAT.json` | 9,681 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold2/det/kfull/case42_LAT.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold2/det/kfull/couple_c74/couple_all.json` | 239,004 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold2/det/kfull/couple_c74/couple_all.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold3/det/kfull/case11_LAT.json` | 9,737 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold3/det/kfull/case11_LAT.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold3/det/kfull/couple_c74/couple_all.json` | 302,838 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold3/det/kfull/couple_c74/couple_all.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold4/det/kfull/couple_c74/couple_all.json` | 215,849 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold4/det/kfull/couple_c74/couple_all.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det/k3/case11_LAT_k3_1.json` | 4,693 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det/k3/case11_LAT_k3_1.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det/k3/prototype_meta.json` | 13,858 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det/k3/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det_score_k3.json` | 172,796 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det_score_k3.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det_score_kfull.json` | 87,832 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/prerepair_dirs.sh` | 915 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/prerepair_dirs.sh` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/prerepair_fold_dirs.json` | 11,046 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/prerepair_fold_dirs.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/prerepair_fold_dirs.py` | 6,903 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/prerepair_fold_dirs.py` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/rigor_pre/a4.json` | 298,704 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/rigor_pre/a4.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/rigor_pre/a7.json` | 402,197 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/rigor_pre/a7.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/rigor_pre/a9.json` | 427,578 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/rigor_pre/a9.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/rigor_rep/a4.json` | 296,888 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/rigor_rep/a4.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/rigor_rep/a7.json` | 400,228 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/rigor_rep/a7.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/rigor_rep/a9.json` | 425,071 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/rigor_rep/a9.json` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/wait_for.sh` | 766 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/wait_for.sh` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/write_cv_v9_md.py` | 20,245 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/write_cv_v9_md.py` |  |
| `results/schwingnet/eval_gate/closure/cv_v9/zs_v9_kfield.sh` | 2,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9/zs_v9_kfield.sh` |  |
| `results/schwingnet/eval_gate/closure/jobs/closure_case134.sh` | 3,139 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/jobs/closure_case134.sh` |  |
| `results/schwingnet/eval_gate/closure/jobs/closure_case134_eg2.sh` | 5,204 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/jobs/closure_case134_eg2.sh` |  |
| `results/schwingnet/eval_gate/closure/jobs/closure_v8.sh` | 1,296 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/jobs/closure_v8.sh` |  |
| `results/schwingnet/eval_gate/closure/v8_overlap/v8_overlap.json` | 269,196 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/v8_overlap/v8_overlap.json` |  |
| `results/schwingnet/eval_gate/closure/v8_overlap/v9_overlap.json` | 225,793 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/v8_overlap/v9_overlap.json` |  |
| `results/schwingnet/eval_gate/closure/v8_overlap_cause.py` | 16,007 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/v8_overlap_cause.py` |  |
| `results/schwingnet/eval_gate/closure/verify/cv0_row_sections.txt` | 2,827 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/cv0_row_sections.txt` |  |
| `results/schwingnet/eval_gate/closure/verify/lineage_check.json` | 4,493 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/lineage_check.json` |  |
| `results/schwingnet/eval_gate/closure/verify/lineage_check.py` | 3,093 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/lineage_check.py` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `results/schwingnet/eval_gate/closure/verify/lineage_rows.txt` | 45,387 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/lineage_rows.txt` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold0/det/kfull/prototype_meta.json` | 13,868 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold0/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold0/det_score_kfull.json` | 84,902 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold0/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold1/det/kfull/prototype_meta.json` | 13,868 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold1/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold1/det_score_kfull.json` | 62,164 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold1/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold2/det/kfull/prototype_meta.json` | 13,868 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold2/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold2/det_score_kfull.json` | 68,258 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold2/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold3/det/kfull/prototype_meta.json` | 13,868 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold3/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold3/det_score_kfull.json` | 87,832 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold3/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold4/det/kfull/prototype_meta.json` | 13,868 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold4/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold4/det_score_kfull.json` | 66,039 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cv_fold4/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold0/det/kfull/prototype_meta.json` | 13,912 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold0/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold0/det_score_kfull.json` | 158,257 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold0/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold1/det/kfull/prototype_meta.json` | 13,907 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold1/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold1/det_score_kfull.json` | 102,419 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold1/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold2/det/kfull/prototype_meta.json` | 13,907 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold2/det/kfull/prototype_meta.json` |  |
| `results/schwingnet/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold2/det_score_kfull.json` | 88,290 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/raw/proto_v9init_prerepair/cvday_fold2/det_score_kfull.json` |  |
| `results/schwingnet/eval_gate/closure/verify/verify_coupled.py` | 2,149 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/verify_coupled.py` |  |
| `results/schwingnet/eval_gate/closure/verify/verify_cv9.py` | 5,954 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/verify_cv9.py` |  |
| `results/schwingnet/eval_gate/closure/verify/verify_cv9_rederived.json` | 22,815 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/verify/verify_cv9_rederived.json` |  |
| `results/schwingnet/eval_gate/eval_sets.json` | 126,199 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/eval_sets.json` |  |
| `results/schwingnet/eval_gate/leaks/a3a_unseen/a3a_rows.csv` | 21,493 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/a3a_unseen/a3a_rows.csv` |  |
| `results/schwingnet/eval_gate/leaks/a3a_unseen/a3a_rows_meta.json` | 8,077 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/a3a_unseen/a3a_rows_meta.json` |  |
| `results/schwingnet/eval_gate/leaks/anchor_descendants.json` | 15,499 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/anchor_descendants.json` |  |
| `results/schwingnet/eval_gate/leaks/anchor_descendants.py` | 3,378 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/anchor_descendants.py` |  |
| `results/schwingnet/eval_gate/leaks/arc_old_vs_new.json` | 9,196 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/arc_old_vs_new.json` |  |
| `results/schwingnet/eval_gate/leaks/arc_old_vs_new.py` | 2,954 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/arc_old_vs_new.py` |  |
| `results/schwingnet/eval_gate/leaks/build_eval_leaks.py` | 16,503 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/build_eval_leaks.py` |  |
| `results/schwingnet/eval_gate/leaks/card_gain_unseen.json` | 1,935 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/card_gain_unseen.json` |  |
| `results/schwingnet/eval_gate/leaks/fig4_pairs_heldout.json` | 209,565 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/fig4_pairs_heldout.json` |  |
| `results/schwingnet/eval_gate/leaks/gate_arc_unseen.json` | 6,585 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/gate_arc_unseen.json` |  |
| `results/schwingnet/eval_gate/leaks/gate_lodo_cobra_test.json` | 12,259 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/gate_lodo_cobra_test.json` |  |
| `results/schwingnet/eval_gate/leaks/gate_lodo_df_test.json` | 2,420 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/gate_lodo_df_test.json` |  |
| `results/schwingnet/eval_gate/leaks/gate_v9_carm_test.json` | 1,638 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/gate_v9_carm_test.json` |  |
| `results/schwingnet/eval_gate/leaks/gate_v9_cobra_test.json` | 1,635 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/gate_v9_cobra_test.json` |  |
| `results/schwingnet/eval_gate/leaks/render_vs_film_unseen.json` | 16,598 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/render_vs_film_unseen.json` |  |
| `results/schwingnet/eval_gate/leaks/render_vs_film_unseen_rerun.json` | 6,157 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/render_vs_film_unseen_rerun.json` |  |
| `results/schwingnet/eval_gate/leaks/rescore_card_gain.py` | 4,538 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/rescore_card_gain.py` |  |
| `results/schwingnet/eval_gate/leaks/rescore_fig4_pairs_heldout.py` | 7,146 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/rescore_fig4_pairs_heldout.py` |  |
| `results/schwingnet/eval_gate/leaks/rescore_render_vs_film.py` | 5,251 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/rescore_render_vs_film.py` |  |
| `results/schwingnet/eval_gate/leaks/rescore_zeroshot_v9.py` | 6,202 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/rescore_zeroshot_v9.py` |  |
| `results/schwingnet/eval_gate/leaks/stats_render_vs_film_rerun.py` | 2,163 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/stats_render_vs_film_rerun.py` |  |
| `results/schwingnet/eval_gate/leaks/zeroshot_v9.json` | 47,610 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/leaks/zeroshot_v9.json` |  |
| `results/schwingnet/eval_gate/lineage_seed.json` | 160,894 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/lineage_seed.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x3) |
| `results/schwingnet/eval_gate/quoted_results.json` | 1,209,718 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/quoted_results.json` |  |
| `results/schwingnet/eval_gate/smoke_gate/arc17.json` | 17,241 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/smoke_gate/arc17.json` |  |
| `results/schwingnet/eval_gate/smoke_gate/fold0_carm_cv0.json` | 2,510 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/smoke_gate/fold0_carm_cv0.json` |  |
| `results/schwingnet/eval_gate/smoke_gate/lodo_carm_test.json` | 1,819 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/smoke_gate/lodo_carm_test.json` |  |
| `results/schwingnet/eval_gate/smoke_gate/lodo_cobra_test.json` | 12,126 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/smoke_gate/lodo_cobra_test.json` |  |
| `results/schwingnet/eval_gate/smoke_gate/rx_lodo__carm_test.json` | 21,786 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/smoke_gate/rx_lodo__carm_test.json` |  |
| `results/schwingnet/eval_gate/touched_run.json` | 44,136 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/touched_run.json` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/out/C01.json` | 1,840 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/out/C01.json` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/out/G23_foldgate.json` | 1,039 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/out/G23_foldgate.json` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/out/K1_implant_keys.json` | 2,361 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/out/K1_implant_keys.json` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/out/L6_rows.json` | 2,128 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/out/L6_rows.json` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_foldgate.py` | 2,388 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_foldgate.py` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_gate.sh` | 9,401 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_gate.sh` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_gate2.sh` | 2,792 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_gate2.sh` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_gate3.sh` | 6,044 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_gate3.sh` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_implant_keys.py` | 2,947 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_implant_keys.py` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_l6_rows.py` | 2,756 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_l6_rows.py` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_setup.py` | 4,407 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_setup.py` |  |
| `results/schwingnet/eval_gate/verify/grid_jobs/verify_v9_sources.py` | 935 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/grid_jobs/verify_v9_sources.py` |  |
| `results/schwingnet/eval_gate/verify/matches_bypass_demo.json` | 2,182 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/matches_bypass_demo.json` |  |
| `results/schwingnet/eval_gate/verify/verify_arc_lists.json` | 7,653 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/verify_arc_lists.json` |  |
| `results/schwingnet/eval_gate/verify/verify_arc_lists.py` | 9,177 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/verify_arc_lists.py` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `results/schwingnet/eval_gate/verify/verify_clean_rows.json` | 8,845 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/verify_clean_rows.json` |  |
| `results/schwingnet/eval_gate/verify/verify_clean_rows.py` | 9,361 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/verify_clean_rows.py` |  |
| `results/schwingnet/eval_gate/verify/verify_trust.json` | 2,333 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/verify_trust.json` |  |
| `results/schwingnet/eval_gate/verify/verify_trust.py` | 4,727 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/verify/verify_trust.py` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `results/schwingnet/fig3_detection/examples/bv_pulsera.json` | 2,453 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/bv_pulsera.json` |  |
| `results/schwingnet/fig3_detection/examples/bv_pulsera.png` | 40,353 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/bv_pulsera.png` |  |
| `results/schwingnet/fig3_detection/examples/cios_fusion.json` | 2,098 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/cios_fusion.json` |  |
| `results/schwingnet/fig3_detection/examples/cios_fusion.png` | 71,629 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/cios_fusion.png` |  |
| `results/schwingnet/fig3_detection/examples/elekta_xvi.json` | 2,965 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/elekta_xvi.json` |  |
| `results/schwingnet/fig3_detection/examples/elekta_xvi.png` | 126,004 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/elekta_xvi.png` |  |
| `results/schwingnet/fig3_detection/examples/surgio_b51_dr.json` | 3,274 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/surgio_b51_dr.json` |  |
| `results/schwingnet/fig3_detection/examples/surgio_b51_dr.png` | 390,186 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/examples/surgio_b51_dr.png` |  |
| `results/schwingnet/fig3_detection/manifest.json` | 2,726 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/manifest.json` |  |
| `results/schwingnet/fig3_detection/scored/lodo_carm__carm_test.json` | 22,753 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/lodo_carm__carm_test.json` |  |
| `results/schwingnet/fig3_detection/scored/lodo_carm__geneva_all.json` | 8,631 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/lodo_carm__geneva_all.json` |  |
| `results/schwingnet/fig3_detection/scored/lodo_cobra__cobra_test.json` | 8,553 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/lodo_cobra__cobra_test.json` |  |
| `results/schwingnet/fig3_detection/scored/lodo_cobra__geneva_all.json` | 7,497 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/lodo_cobra__geneva_all.json` |  |
| `results/schwingnet/fig3_detection/scored/lodo_df__df_test.json` | 8,107 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/lodo_df__df_test.json` |  |
| `results/schwingnet/fig3_detection/scored/lodo_df__geneva_all.json` | 8,344 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/lodo_df__geneva_all.json` |  |
| `results/schwingnet/fig3_detection/scored/pooled__carm_test.json` | 22,431 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/pooled__carm_test.json` |  |
| `results/schwingnet/fig3_detection/scored/pooled__cobra_test.json` | 8,502 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/pooled__cobra_test.json` |  |
| `results/schwingnet/fig3_detection/scored/pooled__df_test.json` | 8,038 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/pooled__df_test.json` |  |
| `results/schwingnet/fig3_detection/scored/pooled__geneva_all.json` | 8,555 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/pooled__geneva_all.json` |  |
| `results/schwingnet/fig3_detection/scored/render__carm_test.json` | 21,976 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/render__carm_test.json` |  |
| `results/schwingnet/fig3_detection/scored/render__cobra_test.json` | 8,553 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/render__cobra_test.json` |  |
| `results/schwingnet/fig3_detection/scored/render__df_test.json` | 8,545 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/render__df_test.json` |  |
| `results/schwingnet/fig3_detection/scored/render__geneva_all.json` | 7,605 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig3_detection/scored/render__geneva_all.json` |  |
| `results/schwingnet/fig4_frames/case11_LAT_cvfull.png` | 366,429 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case11_LAT_cvfull.png` |  |
| `results/schwingnet/fig4_frames/case11_LAT_k3_0.json` | 912 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case11_LAT_k3_0.json` |  |
| `results/schwingnet/fig4_frames/case11_LAT_k3_0.png` | 100,982 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case11_LAT_k3_0.png` |  |
| `results/schwingnet/fig4_frames/case11_LAT_k3_1.json` | 1,167 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case11_LAT_k3_1.json` |  |
| `results/schwingnet/fig4_frames/case11_LAT_k3_1.png` | 145,101 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case11_LAT_k3_1.png` |  |
| `results/schwingnet/fig4_frames/case11_LAT_k3_2.json` | 957 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case11_LAT_k3_2.json` |  |
| `results/schwingnet/fig4_frames/case11_LAT_k3_2.png` | 144,999 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case11_LAT_k3_2.png` |  |
| `results/schwingnet/fig4_frames/case42_LAT.couple.json` | 3,587 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case42_LAT.couple.json` |  |
| `results/schwingnet/fig4_frames/case42_LAT_cvfull.png` | 427,710 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case42_LAT_cvfull.png` |  |
| `results/schwingnet/fig4_frames/post/case11_LAT.json` | 9,719 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/post/case11_LAT.json` |  |
| `results/schwingnet/fig4_frames/post/case11_LAT_overlay.png` | 525,888 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/post/case11_LAT_overlay.png` |  |
| `results/schwingnet/fig4_frames/post/case42_LAT.json` | 9,656 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/post/case42_LAT.json` |  |
| `results/schwingnet/fig4_frames/post/case42_LAT_overlay.png` | 654,140 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/post/case42_LAT_overlay.png` |  |
| `results/schwingnet/fig4_frames/pred_k3/case11_LAT_k3_0.json` | 3,713 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/pred_k3/case11_LAT_k3_0.json` |  |
| `results/schwingnet/fig4_frames/pred_k3/case11_LAT_k3_0_overlay.png` | 163,009 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/pred_k3/case11_LAT_k3_0_overlay.png` |  |
| `results/schwingnet/fig4_frames/pred_k3/case11_LAT_k3_1.json` | 4,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/pred_k3/case11_LAT_k3_1.json` |  |
| `results/schwingnet/fig4_frames/pred_k3/case11_LAT_k3_1_overlay.png` | 236,814 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/pred_k3/case11_LAT_k3_1_overlay.png` |  |
| `results/schwingnet/fig4_frames/pred_k3/case11_LAT_k3_2.json` | 4,655 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/pred_k3/case11_LAT_k3_2.json` |  |
| `results/schwingnet/fig4_frames/pred_k3/case11_LAT_k3_2_overlay.png` | 235,290 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/pred_k3/case11_LAT_k3_2_overlay.png` |  |
| `results/schwingnet/fig4_frames/v9init_pre/a4.json` | 298,704 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/a4.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/carmlspine_cv5_v9init_pre.json` | 20,863 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/carmlspine_cv5_v9init_pre.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/case11_LAT_cvfull.png` | 366,429 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/case11_LAT_cvfull.png` |  |
| `results/schwingnet/fig4_frames/v9init_pre/case11_LAT_k3_1.json` | 1,167 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/case11_LAT_k3_1.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/case11_LAT_k3_1.png` | 156,474 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/case11_LAT_k3_1.png` |  |
| `results/schwingnet/fig4_frames/v9init_pre/case42_LAT.png` | 427,710 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/case42_LAT.png` |  |
| `results/schwingnet/fig4_frames/v9init_pre/coupling.json` | 2,042,862 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/coupling.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/coupling_c74/cv_fold0_det_kfull_couple_all.json` | 289,036 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/coupling_c74/cv_fold0_det_kfull_couple_all.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/coupling_c74/cv_fold1_det_kfull_couple_all.json` | 213,279 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/coupling_c74/cv_fold1_det_kfull_couple_all.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/coupling_c74/cv_fold2_det_kfull_couple_all.json` | 239,004 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/coupling_c74/cv_fold2_det_kfull_couple_all.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/coupling_c74/cv_fold3_det_kfull_couple_all.json` | 302,838 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/coupling_c74/cv_fold3_det_kfull_couple_all.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/coupling_c74/cv_fold4_det_kfull_couple_all.json` | 215,849 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/coupling_c74/cv_fold4_det_kfull_couple_all.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/cv_fold3_det_score_k3.json` | 172,796 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/cv_fold3_det_score_k3.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/cv_v9.json` | 744,309 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/cv_v9.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/post/case11_LAT.json` | 9,737 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/post/case11_LAT.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/post/case42_LAT.json` | 9,681 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/post/case42_LAT.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/post/cv_fold2_prototype_meta.json` | 15,873 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/post/cv_fold2_prototype_meta.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/post/cv_fold3_prototype_meta.json` | 15,873 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/post/cv_fold3_prototype_meta.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/pred_k3/case11_LAT_k3_1.json` | 4,693 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/pred_k3/case11_LAT_k3_1.json` |  |
| `results/schwingnet/fig4_frames/v9init_pre/pred_k3/prototype_meta.json` | 13,858 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/v9init_pre/pred_k3/prototype_meta.json` |  |
| `results/schwingnet/fig4_pairs/bv_pulsera.json` | 6,744 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/bv_pulsera.json` |  |
| `results/schwingnet/fig4_pairs/bv_pulsera_real.png` | 41,880 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/bv_pulsera_real.png` |  |
| `results/schwingnet/fig4_pairs/bv_pulsera_styled.png` | 76,978 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/bv_pulsera_styled.png` |  |
| `results/schwingnet/fig4_pairs/cios_fusion.json` | 15,960 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/cios_fusion.json` |  |
| `results/schwingnet/fig4_pairs/cios_fusion_real.png` | 65,222 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/cios_fusion_real.png` |  |
| `results/schwingnet/fig4_pairs/cios_fusion_styled.png` | 70,589 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/cios_fusion_styled.png` |  |
| `results/schwingnet/fig4_pairs/elekta_xvi.json` | 28,177 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/elekta_xvi.json` |  |
| `results/schwingnet/fig4_pairs/elekta_xvi_real.png` | 79,942 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/elekta_xvi_real.png` |  |
| `results/schwingnet/fig4_pairs/elekta_xvi_styled.png` | 91,600 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/elekta_xvi_styled.png` |  |
| `results/schwingnet/fig4_pairs/fig4_pairs.json` | 4,838 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/fig4_pairs.json` |  |
| `results/schwingnet/fig4_pairs/pixium_4600.json` | 3,237 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/pixium_4600.json` |  |
| `results/schwingnet/fig4_pairs/pixium_4600_real.png` | 21,496 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/pixium_4600_real.png` |  |
| `results/schwingnet/fig4_pairs/pixium_4600_styled.png` | 30,190 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/pixium_4600_styled.png` |  |
| `results/schwingnet/fig4_pairs/pixium_blob_diag.json` | 1,941 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig4_pairs/pixium_blob_diag.json` |  |
| `results/schwingnet/fig5_frames/case42_LAT.meta.json` | 8,951 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig5_frames/case42_LAT.meta.json` |  |
| `results/schwingnet/fig5_frames/case42_LAT.png` | 427,710 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig5_frames/case42_LAT.png` |  |
| `results/schwingnet/fig5_naming_data.json` | 9,653 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/fig5_naming_data.json` |  |
| `results/schwingnet/figure1/figure1_panel_facts.json` | 45,317 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/figure1_panel_facts.json` |  |
| `results/schwingnet/figure1/panels/four_0760_drr.png` | 196,615 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/four_0760_drr.png` |  |
| `results/schwingnet/figure1/panels/four_0760_slice.png` | 296,947 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/four_0760_slice.png` |  |
| `results/schwingnet/figure1/panels/l6_0244_drr.png` | 346,422 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/l6_0244_drr.png` |  |
| `results/schwingnet/figure1/panels/l6_0244_slice.png` | 499,614 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/l6_0244_slice.png` |  |
| `results/schwingnet/figure1/panels/sac5_0021_drr.png` | 158,364 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/sac5_0021_drr.png` |  |
| `results/schwingnet/figure1/panels/sac5_0021_surface.png` | 171,452 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/sac5_0021_surface.png` |  |
| `results/schwingnet/figure1/panels/t13_verse547_drr.png` | 149,335 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/t13_verse547_drr.png` |  |
| `results/schwingnet/figure1/panels/t13_verse547_slab_p16_s24_acc.png` | 190,461 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure1/panels/t13_verse547_slab_p16_s24_acc.png` |  |
| `results/schwingnet/figure2/bank_person_census.json` | 982,464 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/bank_person_census.json` |  |
| `results/schwingnet/figure2/figure2_metrics.json` | 50,739 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/figure2_metrics.json` |  |
| `results/schwingnet/figure2/figure2_transitional.json` | 8,989 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/figure2_transitional.json` |  |
| `results/schwingnet/figure2/heldout_census.json` | 3,775 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/heldout_census.json` |  |
| `results/schwingnet/figure2/occlusion_clean/gradcam_summary.json` | 29,908 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/occlusion_clean/gradcam_summary.json` |  |
| `results/schwingnet/figure2/v9_keys_snapshot.json` | 172,917 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/v9_keys_snapshot.json` |  |
| `results/schwingnet/figure2/zones_lateral.json` | 24,068 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/zones_lateral.json` |  |
| `results/schwingnet/figure2/zones_lateral_clean.json` | 10,163 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/figure2/zones_lateral_clean.json` |  |
| `results/schwingnet/g0_facts.md` | 18,030 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/g0_facts.md` | laptop paths rewritten to markers (CTSpinoPelvic1K: x11, laptop-scratchpad: x1) |
| `results/schwingnet/gallery/GALLERY_CHECK.md` | 8,748 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/GALLERY_CHECK.md` |  |
| `results/schwingnet/gallery/GALLERY_SOURCES.md` | 10,140 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/GALLERY_SOURCES.md` |  |
| `results/schwingnet/gallery/candidates.md` | 3,035 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/candidates.md` |  |
| `results/schwingnet/gallery/gallery_spec.json` | 4,487 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/gallery_spec.json` |  |
| `results/schwingnet/gallery/panel_facts.json` | 117,837 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panel_facts.json` |  |
| `results/schwingnet/gallery/panels/buu_l4_0233_film.png` | 1,195,018 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/buu_l4_0233_film.png` |  |
| `results/schwingnet/gallery/panels/buu_l6_2580_film.png` | 774,785 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/buu_l6_2580_film.png` |  |
| `results/schwingnet/gallery/panels/carm_case136_frame.png` | 373,380 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/carm_case136_frame.png` |  |
| `results/schwingnet/gallery/panels/four_0760_drr.png` | 196,615 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/four_0760_drr.png` |  |
| `results/schwingnet/gallery/panels/four_0760_slice.png` | 296,947 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/four_0760_slice.png` |  |
| `results/schwingnet/gallery/panels/four_0760_styled_cios_fusion_s11.png` | 145,005 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/four_0760_styled_cios_fusion_s11.png` |  |
| `results/schwingnet/gallery/panels/four_0760_styled_cios_fusion_s7.png` | 191,700 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/four_0760_styled_cios_fusion_s7.png` |  |
| `results/schwingnet/gallery/panels/l6_0244_drr.png` | 346,422 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/l6_0244_drr.png` |  |
| `results/schwingnet/gallery/panels/l6_0244_slice.png` | 499,614 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/l6_0244_slice.png` |  |
| `results/schwingnet/gallery/panels/l6_0244_styled_cios_fusion_s11.png` | 205,105 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/l6_0244_styled_cios_fusion_s11.png` |  |
| `results/schwingnet/gallery/panels/l6_0244_styled_cios_fusion_s7.png` | 262,253 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/l6_0244_styled_cios_fusion_s7.png` |  |
| `results/schwingnet/gallery/panels/l6_0244_surface.png` | 328,220 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/l6_0244_surface.png` |  |
| `results/schwingnet/gallery/panels/sac5_0008_drr.png` | 234,651 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/sac5_0008_drr.png` |  |
| `results/schwingnet/gallery/panels/sac5_0008_styled_cios_fusion_s11.png` | 196,141 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/sac5_0008_styled_cios_fusion_s11.png` |  |
| `results/schwingnet/gallery/panels/sac5_0008_styled_cios_fusion_s7.png` | 235,330 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/sac5_0008_styled_cios_fusion_s7.png` |  |
| `results/schwingnet/gallery/panels/sac5_0008_surface.png` | 191,258 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/sac5_0008_surface.png` |  |
| `results/schwingnet/gallery/panels/t13_verse547_drr.png` | 149,335 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/t13_verse547_drr.png` |  |
| `results/schwingnet/gallery/panels/t13_verse547_styled_cios_fusion_s11.png` | 138,802 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/t13_verse547_styled_cios_fusion_s11.png` |  |
| `results/schwingnet/gallery/panels/t13_verse547_styled_cios_fusion_s7.png` | 187,812 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/t13_verse547_styled_cios_fusion_s7.png` |  |
| `results/schwingnet/gallery/panels/t13_verse547_surface.png` | 123,591 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/gallery/panels/t13_verse547_surface.png` |  |
| `results/schwingnet/indomain/DENOMINATOR_REPAIR.md` | 14,173 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/DENOMINATOR_REPAIR.md` |  |
| `results/schwingnet/indomain/FIT_N.md` | 13,831 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/FIT_N.md` |  |
| `results/schwingnet/indomain/INDOMAIN.md` | 59,303 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/INDOMAIN.md` |  |
| `results/schwingnet/indomain/INVENTORY.md` | 43,432 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/INVENTORY.md` |  |
| `results/schwingnet/indomain/RESULTS_PARAGRAPH.tex` | 1,135 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/RESULTS_PARAGRAPH.tex` |  |
| `results/schwingnet/indomain/denominator_repair.json` | 459,834 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/denominator_repair.json` |  |
| `results/schwingnet/indomain/det_fill.json` | 1,355,523 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/det_fill.json` |  |
| `results/schwingnet/indomain/detfill/convention_check_case100_LAT.jpg` | 154,528 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/convention_check_case100_LAT.jpg` |  |
| `results/schwingnet/indomain/detfill/grid/boxstyle.json` | 116,472 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/boxstyle.json` |  |
| `results/schwingnet/indomain/detfill/grid/done_list.txt` | 1,098 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/done_list.txt` |  |
| `results/schwingnet/indomain/detfill/grid/done_rc.txt` | 1,209 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/done_rc.txt` |  |
| `results/schwingnet/indomain/detfill/grid/heldout.json` | 51,564 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/heldout.json` |  |
| `results/schwingnet/indomain/detfill/grid/label_delta.json` | 1,444 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/label_delta.json` |  |
| `results/schwingnet/indomain/detfill/grid/manifest.txt` | 903 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/manifest.txt` |  |
| `results/schwingnet/indomain/detfill/grid/manifest_outline.txt` | 195 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/manifest_outline.txt` |  |
| `results/schwingnet/indomain/detfill/grid/outline_labels.json` | 421 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/outline_labels.json` |  |
| `results/schwingnet/indomain/detfill/grid/percase.json` | 1,277,308 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/percase.json` |  |
| `results/schwingnet/indomain/detfill/grid/plan.json` | 152,833 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/plan.json` |  |
| `results/schwingnet/indomain/detfill/grid/views_fill.json` | 976,881 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/grid/views_fill.json` |  |
| `results/schwingnet/indomain/detfill/manifest.txt` | 903 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/manifest.txt` |  |
| `results/schwingnet/indomain/detfill/manifest_outline.txt` | 195 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/manifest_outline.txt` |  |
| `results/schwingnet/indomain/detfill/manifest_retry.txt` | 32 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/manifest_retry.txt` |  |
| `results/schwingnet/indomain/detfill/plan.json` | 152,833 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/plan.json` |  |
| `results/schwingnet/indomain/detfill/plan_before_outline_control.json` | 138,428 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/detfill/plan_before_outline_control.json` |  |
| `results/schwingnet/indomain/fill/FILL_CHECK.json` | 3,379 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fill/FILL_CHECK.json` |  |
| `results/schwingnet/indomain/fill/lcurve_cases_2026-09-23T0136.json` | 3,273 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fill/lcurve_cases_2026-09-23T0136.json` |  |
| `results/schwingnet/indomain/fill/lcurve_fill_manifest.txt` | 356 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fill/lcurve_fill_manifest.txt` |  |
| `results/schwingnet/indomain/fill/naming_fill_manifest.txt` | 530 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fill/naming_fill_manifest.txt` |  |
| `results/schwingnet/indomain/fill/naming_subsets.json` | 57,564 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fill/naming_subsets.json` |  |
| `results/schwingnet/indomain/fill/protocol_fill_manifest.txt` | 274 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fill/protocol_fill_manifest.txt` |  |
| `results/schwingnet/indomain/fill/subsets_fill.json` | 32,134 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fill/subsets_fill.json` |  |
| `results/schwingnet/indomain/fit.json` | 333,368 | modified on copy | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fit.json` | laptop paths rewritten to markers (spinesurg-ct-nnunet: x1) |
| `results/schwingnet/indomain/fit/coverage_fit.json` | 323,403 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fit/coverage_fit.json` |  |
| `results/schwingnet/indomain/fit/coverage_grid.json` | 1,178,839 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fit/coverage_grid.json` |  |
| `results/schwingnet/indomain/fit/fit_check.png` | 193,192 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fit/fit_check.png` |  |
| `results/schwingnet/indomain/fit/name_percase.json` | 1,037,765 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fit/name_percase.json` |  |
| `results/schwingnet/indomain/fit/tables.md` | 31,618 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fit/tables.md` |  |
| `results/schwingnet/indomain/fit_N.json` | 82,959 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/fit_N.json` |  |
| `results/schwingnet/indomain/grid/census.json` | 1,269,283 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/grid/census.json` |  |
| `results/schwingnet/indomain/grid/scaling_curve_2026-09-17.json` | 4,565 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/grid/scaling_curve_2026-09-17.json` |  |
| `results/schwingnet/indomain/grid/views.json` | 773,874 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/grid/views.json` |  |
| `results/schwingnet/indomain/grid/views_pre_repair.json` | 215,283 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/grid/views_pre_repair.json` |  |
| `results/schwingnet/indomain/miss_diagnostic/MISS_DIAGNOSTIC.md` | 34,832 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/miss_diagnostic/MISS_DIAGNOSTIC.md` |  |
| `results/schwingnet/indomain/miss_diagnostic/always_hit_sample.png` | 1,229,879 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/miss_diagnostic/always_hit_sample.png` |  |
| `results/schwingnet/indomain/miss_diagnostic/miss_diagnostic.json` | 373,117 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/miss_diagnostic/miss_diagnostic.json` |  |
| `results/schwingnet/indomain/miss_diagnostic/never_hit_body074_sheet1.png` | 909,010 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/miss_diagnostic/never_hit_body074_sheet1.png` |  |
| `results/schwingnet/indomain/miss_diagnostic/never_hit_body074_sheet2.png` | 811,702 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/miss_diagnostic/never_hit_body074_sheet2.png` |  |
| `results/schwingnet/indomain/name_fill.json` | 851,760 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/name_fill.json` |  |
| `results/schwingnet/indomain/namefill/cells.json` | 425,125 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/namefill/cells.json` |  |
| `results/schwingnet/indomain/namefill/finalize.py` | 10,116 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/namefill/finalize.py` |  |
| `results/schwingnet/indomain/points.csv` | 497,522 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/points.csv` |  |
| `results/schwingnet/indomain/spec.json` | 142,919 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/spec.json` |  |
| `results/schwingnet/indomain/views_selfcheck.json` | 15,966 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/indomain/views_selfcheck.json` |  |
| `results/schwingnet/inputs/cases.csv` | 11,266 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cases.csv` |  |
| `results/schwingnet/inputs/curves.json` | 823,939 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/curves.json` |  |
| `results/schwingnet/inputs/cv_fold0/det_score_k1.json` | 128,973 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold0/det_score_k1.json` |  |
| `results/schwingnet/inputs/cv_fold0/det_score_k2.json` | 149,985 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold0/det_score_k2.json` |  |
| `results/schwingnet/inputs/cv_fold0/det_score_k3.json` | 152,990 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold0/det_score_k3.json` |  |
| `results/schwingnet/inputs/cv_fold0/det_score_k4.json` | 126,074 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold0/det_score_k4.json` |  |
| `results/schwingnet/inputs/cv_fold0/det_score_k5.json` | 70,579 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold0/det_score_k5.json` |  |
| `results/schwingnet/inputs/cv_fold0/det_score_kfull.json` | 75,658 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold0/det_score_kfull.json` |  |
| `results/schwingnet/inputs/cv_fold1/det_score_k1.json` | 94,905 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold1/det_score_k1.json` |  |
| `results/schwingnet/inputs/cv_fold1/det_score_k2.json` | 111,985 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold1/det_score_k2.json` |  |
| `results/schwingnet/inputs/cv_fold1/det_score_k3.json` | 112,241 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold1/det_score_k3.json` |  |
| `results/schwingnet/inputs/cv_fold1/det_score_k4.json` | 95,956 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold1/det_score_k4.json` |  |
| `results/schwingnet/inputs/cv_fold1/det_score_k5.json` | 60,241 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold1/det_score_k5.json` |  |
| `results/schwingnet/inputs/cv_fold1/det_score_kfull.json` | 53,409 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold1/det_score_kfull.json` |  |
| `results/schwingnet/inputs/cv_fold2/det_score_k1.json` | 107,320 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold2/det_score_k1.json` |  |
| `results/schwingnet/inputs/cv_fold2/det_score_k2.json` | 126,486 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold2/det_score_k2.json` |  |
| `results/schwingnet/inputs/cv_fold2/det_score_k3.json` | 129,290 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold2/det_score_k3.json` |  |
| `results/schwingnet/inputs/cv_fold2/det_score_k4.json` | 111,488 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold2/det_score_k4.json` |  |
| `results/schwingnet/inputs/cv_fold2/det_score_k5.json` | 71,974 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold2/det_score_k5.json` |  |
| `results/schwingnet/inputs/cv_fold2/det_score_kfull.json` | 59,003 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold2/det_score_kfull.json` |  |
| `results/schwingnet/inputs/cv_fold3/det_score_k1.json` | 137,094 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold3/det_score_k1.json` |  |
| `results/schwingnet/inputs/cv_fold3/det_score_k2.json` | 160,323 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold3/det_score_k2.json` |  |
| `results/schwingnet/inputs/cv_fold3/det_score_k3.json` | 163,598 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold3/det_score_k3.json` |  |
| `results/schwingnet/inputs/cv_fold3/det_score_k4.json` | 139,612 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold3/det_score_k4.json` |  |
| `results/schwingnet/inputs/cv_fold3/det_score_k5.json` | 85,082 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold3/det_score_k5.json` |  |
| `results/schwingnet/inputs/cv_fold3/det_score_kfull.json` | 78,790 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold3/det_score_kfull.json` |  |
| `results/schwingnet/inputs/cv_fold4/det_score_k1.json` | 96,554 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold4/det_score_k1.json` |  |
| `results/schwingnet/inputs/cv_fold4/det_score_k2.json` | 115,270 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold4/det_score_k2.json` |  |
| `results/schwingnet/inputs/cv_fold4/det_score_k3.json` | 118,941 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold4/det_score_k3.json` |  |
| `results/schwingnet/inputs/cv_fold4/det_score_k4.json` | 103,392 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold4/det_score_k4.json` |  |
| `results/schwingnet/inputs/cv_fold4/det_score_k5.json` | 65,674 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold4/det_score_k5.json` |  |
| `results/schwingnet/inputs/cv_fold4/det_score_kfull.json` | 56,765 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/cv_fold4/det_score_kfull.json` |  |
| `results/schwingnet/inputs/ensemble.json` | 11,286 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/ensemble.json` |  |
| `results/schwingnet/inputs/film_det_on_real_films.json` | 1,092 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/film_det_on_real_films.json` |  |
| `results/schwingnet/inputs/head_allspine_v8_mixed_kmax4_seed0.arch.json` | 621 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/head_allspine_v8_mixed_kmax4_seed0.arch.json` |  |
| `results/schwingnet/inputs/headers_dossier.json` | 1,863,754 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/headers_dossier.json` |  |
| `results/schwingnet/inputs/mixed_allspine_v2_fov96_ctx_mixed_kmax4_seed0.json` | 11,792 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/mixed_allspine_v2_fov96_ctx_mixed_kmax4_seed0.json` |  |
| `results/schwingnet/inputs/mixed_allspine_v8_mixed_kmax4_seed0.json` | 11,466 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/mixed_allspine_v8_mixed_kmax4_seed0.json` |  |
| `results/schwingnet/inputs/overlap.json` | 18,399 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/overlap.json` |  |
| `results/schwingnet/inputs/pooled_lodo_det.json` | 8,814 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/pooled_lodo_det.json` |  |
| `results/schwingnet/inputs/render_det_on_real_films.json` | 1,072 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/render_det_on_real_films.json` |  |
| `results/schwingnet/inputs/render_det_on_renders.json` | 1,056 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/render_det_on_renders.json` |  |
| `results/schwingnet/inputs/rescore_outline.json` | 42,828 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/rescore_outline.json` |  |
| `results/schwingnet/inputs/rescore_outline.md` | 2,476 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/rescore_outline.md` |  |
| `results/schwingnet/inputs/splits.json` | 1,860 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/splits.json` |  |
| `results/schwingnet/inputs/summary.json` | 535 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/summary.json` |  |
| `results/schwingnet/inputs/table.md` | 10,570 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/table.md` |  |
| `results/schwingnet/inputs/zeroshot2_det_test/score_kfull.json` | 61,821 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/zeroshot2_det_test/score_kfull.json` |  |
| `results/schwingnet/inputs/zeroshot2_det_train/score_kfull.json` | 228,670 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/zeroshot2_det_train/score_kfull.json` |  |
| `results/schwingnet/inputs/zeroshot2_det_val/score_kfull.json` | 32,598 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/inputs/zeroshot2_det_val/score_kfull.json` |  |
| `results/schwingnet/lcurve/JOBS.txt` | 1,876 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/JOBS.txt` |  |
| `results/schwingnet/lcurve/cells/lc_cios_fusion_N0_s0__deepfluoro_test.json` | 9,045 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_cios_fusion_N0_s0__deepfluoro_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_cios_fusion_N100_s0__deepfluoro_test.json` | 8,688 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_cios_fusion_N100_s0__deepfluoro_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_cios_fusion_N100_s1__deepfluoro_test.json` | 9,048 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_cios_fusion_N100_s1__deepfluoro_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_cios_fusion_N200_s0__deepfluoro_test.json` | 9,146 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_cios_fusion_N200_s0__deepfluoro_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_cios_fusion_N200_s1__deepfluoro_test.json` | 9,018 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_cios_fusion_N200_s1__deepfluoro_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_cios_fusion_N50_s0__deepfluoro_test.json` | 9,128 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_cios_fusion_N50_s0__deepfluoro_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_elekta_xvi_N0_s0__cobra_elekta_test.json` | 8,812 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_elekta_xvi_N0_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_elekta_xvi_N100_s0__cobra_elekta_test.json` | 8,878 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_elekta_xvi_N100_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_elekta_xvi_N100_s1__cobra_elekta_test.json` | 8,884 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_elekta_xvi_N100_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_elekta_xvi_N200_s0__cobra_elekta_test.json` | 8,922 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_elekta_xvi_N200_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_elekta_xvi_N400_s0__cobra_elekta_test.json` | 9,010 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_elekta_xvi_N400_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_elekta_xvi_N400_s1__cobra_elekta_test.json` | 9,000 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_elekta_xvi_N400_s1__cobra_elekta_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_elekta_xvi_N50_s0__cobra_elekta_test.json` | 8,874 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_elekta_xvi_N50_s0__cobra_elekta_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N0_s0__carm_transitional.json` | 23,364 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N0_s0__carm_transitional.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N0_s0__carmlspine_test.json` | 23,099 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N0_s0__carmlspine_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N100_s0__carm_transitional.json` | 24,297 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N100_s0__carm_transitional.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N100_s0__carmlspine_test.json` | 23,513 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N100_s0__carmlspine_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N100_s1__carm_transitional.json` | 24,307 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N100_s1__carm_transitional.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N100_s1__carmlspine_test.json` | 23,519 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N100_s1__carmlspine_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N200_s0__carm_transitional.json` | 24,950 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N200_s0__carm_transitional.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N200_s0__carmlspine_test.json` | 24,225 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N200_s0__carmlspine_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N200_s1__carm_transitional.json` | 24,797 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N200_s1__carm_transitional.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N200_s1__carmlspine_test.json` | 24,060 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N200_s1__carmlspine_test.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N50_s0__carm_transitional.json` | 23,842 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N50_s0__carm_transitional.json` |  |
| `results/schwingnet/lcurve/cells/lc_surgio_b51_dr_N50_s0__carmlspine_test.json` | 23,293 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/cells/lc_surgio_b51_dr_N50_s0__carmlspine_test.json` |  |
| `results/schwingnet/lcurve/fig_lcurve.png` | 319,612 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/fig_lcurve.png` |  |
| `results/schwingnet/lcurve/lcurve.json` | 310,305 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/lcurve.json` |  |
| `results/schwingnet/lcurve/lcurve.md` | 19,852 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/lcurve.md` |  |
| `results/schwingnet/lcurve/subsets.json` | 15,897 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/lcurve/subsets.json` |  |
| `results/schwingnet/power/inputs/cobra_lstv_screen.grid.json` | 3,643 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/power/inputs/cobra_lstv_screen.grid.json` |  |
| `results/schwingnet/power/inputs/cobra_lstv_screen.grid.md` | 2,847 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/power/inputs/cobra_lstv_screen.grid.md` |  |
| `results/schwingnet/power/power.json` | 119,647 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/power/power.json` |  |
| `results/schwingnet/power_table.json` | 1,679 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/power_table.json` |  |
| `results/schwingnet/realxray_lists_audit.json` | 25,926 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/realxray_lists_audit.json` |  |
| `results/schwingnet/repairs/carm-cases_CHECK.md` | 16,095 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/repairs/carm-cases_CHECK.md` |  |
| `results/schwingnet/repairs/cobra-dup-leak_CHECK.md` | 9,572 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/repairs/cobra-dup-leak_CHECK.md` |  |
| `results/schwingnet/repairs/ct0533_CHECK.md` | 11,840 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/repairs/ct0533_CHECK.md` |  |
| `results/schwingnet/repairs/ds815-spinesac_CHECK.md` | 11,099 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/repairs/ds815-spinesac_CHECK.md` |  |
| `results/schwingnet/repairs/nhanes-vindr_CHECK.md` | 15,755 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/repairs/nhanes-vindr_CHECK.md` |  |
| `results/schwingnet/repairs/varian_CHECK.md` | 13,408 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/repairs/varian_CHECK.md` |  |
| `results/schwingnet/rigor_fixes.json` | 560,424 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/rigor_fixes.json` |  |
| `results/schwingnet/stats_review/recompute.json` | 8,136 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/stats_review/recompute.json` |  |
| `results/schwingnet/stats_review2/recompute.json` | 18,173 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/stats_review2/recompute.json` |  |
| `results/schwingnet/supplement_figs/README.md` | 1,178 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/README.md` |  |
| `results/schwingnet/supplement_figs/card_refit/constrained/elekta_xvi.refit.json` | 1,571 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/card_refit/constrained/elekta_xvi.refit.json` |  |
| `results/schwingnet/supplement_figs/card_refit/constrained/surgio_b51_dr.refit.json` | 1,585 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/card_refit/constrained/surgio_b51_dr.refit.json` |  |
| `results/schwingnet/supplement_figs/card_refit/full/cios_fusion.refit.json` | 1,579 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/card_refit/full/cios_fusion.refit.json` |  |
| `results/schwingnet/supplement_figs/card_refit/full/elekta_xvi.refit.json` | 1,587 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/card_refit/full/elekta_xvi.refit.json` |  |
| `results/schwingnet/supplement_figs/card_refit/full/surgio_b51_dr.refit.json` | 1,573 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/card_refit/full/surgio_b51_dr.refit.json` |  |
| `results/schwingnet/supplement_figs/case134/frames.csv` | 16,648 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames.csv` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw054.json` | 2,438 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw054.json` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw054.png` | 403,325 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw054.png` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw129.json` | 2,433 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw129.json` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw129.png` | 457,657 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw129.png` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw205.json` | 2,438 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw205.json` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw205.png` | 513,525 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw205.png` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw280.json` | 2,437 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw280.json` |  |
| `results/schwingnet/supplement_figs/case134/frames/case134_sw280.png` | 448,791 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/frames/case134_sw280.png` |  |
| `results/schwingnet/supplement_figs/case134/summary.json` | 1,261 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/supplement_figs/case134/summary.json` |  |
| `results/schwingnet/sweep_variant_calls.json` | 838,414 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/sweep_variant_calls.json` |  |
| `results/schwingnet/transitional_registry/REGISTRY.md` | 57,857 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/transitional_registry/REGISTRY.md` | added on the fix pass of 2026-10-08 (section 2.2); the rest of `transitional_registry/` is project 06's |
| `results/schwingnet/v9_a5_seeds.json` | 4,869 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_a5_seeds.json` |  |
| `results/schwingnet/v9_seed0/a5.json` | 64,276 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed0/a5.json` |  |
| `results/schwingnet/v9_seed0/a5_rows.csv` | 5,780,625 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed0/a5_rows.csv` |  |
| `results/schwingnet/v9_seed0/a5_rows_meta.json` | 3,641 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed0/a5_rows_meta.json` |  |
| `results/schwingnet/v9_seed0/mixed_allspine_v9_mixed_kmax4_seed0.json` | 11,214 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed0/mixed_allspine_v9_mixed_kmax4_seed0.json` |  |
| `results/schwingnet/v9_seed1/a5.json` | 64,277 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed1/a5.json` |  |
| `results/schwingnet/v9_seed1/a5_rows.csv` | 5,780,704 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed1/a5_rows.csv` |  |
| `results/schwingnet/v9_seed1/a5_rows_meta.json` | 3,645 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed1/a5_rows_meta.json` |  |
| `results/schwingnet/v9_seed1/mixed_allspine_v9_mixed_kmax4_seed1.json` | 11,213 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed1/mixed_allspine_v9_mixed_kmax4_seed1.json` |  |
| `results/schwingnet/v9_seed2/a5.json` | 64,282 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed2/a5.json` |  |
| `results/schwingnet/v9_seed2/a5_rows.csv` | 5,780,754 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed2/a5_rows.csv` |  |
| `results/schwingnet/v9_seed2/a5_rows_meta.json` | 3,642 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed2/a5_rows_meta.json` |  |
| `results/schwingnet/v9_seed2/mixed_allspine_v9_mixed_kmax4_seed2.json` | 11,224 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/v9_seed2/mixed_allspine_v9_mixed_kmax4_seed2.json` |  |
| `results/schwingnet/window_probe/A002_f0000_exported_field_body.png` | 150,498 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A002_f0000_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A002_f0060_exported_field_body.png` | 140,121 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A002_f0060_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A002_f0120_exported_field_body.png` | 132,937 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A002_f0120_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A002_f0180_exported_field_body.png` | 103,180 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A002_f0180_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A002_f0240_exported_field_body.png` | 135,301 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A002_f0240_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A002_f0300_exported_field_body.png` | 111,343 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A002_f0300_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A004_f0000_exported_field_body.png` | 124,673 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A004_f0000_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A004_f0060_exported_field_body.png` | 138,408 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A004_f0060_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A004_f0120_exported_field_body.png` | 151,440 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A004_f0120_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A004_f0180_exported_field_body.png` | 129,422 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A004_f0180_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A004_f0240_exported_field_body.png` | 152,169 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A004_f0240_exported_field_body.png` |  |
| `results/schwingnet/window_probe/A004_f0300_exported_field_body.png` | 156,881 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/A004_f0300_exported_field_body.png` |  |
| `results/schwingnet/window_probe/B013_f0000_exported_field_body.png` | 143,952 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/B013_f0000_exported_field_body.png` |  |
| `results/schwingnet/window_probe/B013_f0060_exported_field_body.png` | 154,695 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/B013_f0060_exported_field_body.png` |  |
| `results/schwingnet/window_probe/B013_f0120_exported_field_body.png` | 169,204 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/B013_f0120_exported_field_body.png` |  |
| `results/schwingnet/window_probe/B013_f0180_exported_field_body.png` | 171,321 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/B013_f0180_exported_field_body.png` |  |
| `results/schwingnet/window_probe/B013_f0240_exported_field_body.png` | 148,828 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/B013_f0240_exported_field_body.png` |  |
| `results/schwingnet/window_probe/B013_f0300_exported_field_body.png` | 127,425 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/B013_f0300_exported_field_body.png` |  |
| `results/schwingnet/window_probe/C045_f0000_exported_field_body.png` | 126,089 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/C045_f0000_exported_field_body.png` |  |
| `results/schwingnet/window_probe/C045_f0060_exported_field_body.png` | 126,193 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/C045_f0060_exported_field_body.png` |  |
| `results/schwingnet/window_probe/C045_f0120_exported_field_body.png` | 152,380 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/C045_f0120_exported_field_body.png` |  |
| `results/schwingnet/window_probe/C045_f0180_exported_field_body.png` | 128,607 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/C045_f0180_exported_field_body.png` |  |
| `results/schwingnet/window_probe/C045_f0240_exported_field_body.png` | 138,454 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/C045_f0240_exported_field_body.png` |  |
| `results/schwingnet/window_probe/C045_f0300_exported_field_body.png` | 109,588 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/C045_f0300_exported_field_body.png` |  |
| `results/schwingnet/window_probe/F011_f0000_exported_field_body.png` | 141,043 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/F011_f0000_exported_field_body.png` |  |
| `results/schwingnet/window_probe/F011_f0060_exported_field_body.png` | 131,310 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/F011_f0060_exported_field_body.png` |  |
| `results/schwingnet/window_probe/F011_f0120_exported_field_body.png` | 127,133 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/F011_f0120_exported_field_body.png` |  |
| `results/schwingnet/window_probe/F011_f0180_exported_field_body.png` | 121,509 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/F011_f0180_exported_field_body.png` |  |
| `results/schwingnet/window_probe/F011_f0240_exported_field_body.png` | 131,240 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/F011_f0240_exported_field_body.png` |  |
| `results/schwingnet/window_probe/F011_f0300_exported_field_body.png` | 137,515 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/F011_f0300_exported_field_body.png` |  |
| `results/schwingnet/window_probe/REPORT.txt` | 3,622 | same bytes | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/window_probe/REPORT.txt` |  |



## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Duplicates removed (PLAN.md section 2 rule 2d: one copy, in the owning folder)

The critic found these eight files byte for byte in this folder and in the folder the plan names as their owner, with no shared-copy note on either side. Rule 2d allowed only `PHYSICS_LINKING.md` and `or_ready_audit_track` into both 01 and 08. The copies here were removed; the rows of section 1 that list them are history. Citations in `STATUS.md` and `MANIFEST_GRID.md` now point at the owning folder; the files are also tracked in spinesurg-ct-nnunet at 097933a (`docs/` and `docs/grid_records/`), named in `MANIFEST_CODE.md`.

| removed from this folder | bytes | sha1 | the one copy that remains |
|---|---:|---|---|
| `docs/HANDOFF_PHYSICS.md` | 30,048 | 04ad77c355acc0ce | `../08_render_devices/docs/HANDOFF_PHYSICS.md` (byte-identical, verified by sha1 before removal) |
| `docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md` | 8,206 | 563fea0482001589 | `../08_render_devices/docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md` (byte-identical, verified by sha1 before removal) |
| `docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md` | 5,216 | 6f39fc98995acffc | `../08_render_devices/docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md` (byte-identical, verified by sha1 before removal) |
| `docs/SIMULATION_FIDELITY.md` | 8,656 | 5dd86f23e1ff0406 | `../08_render_devices/docs/SIMULATION_FIDELITY.md` (byte-identical, verified by sha1 before removal) |
| `docs/WRONG_LEVEL_COST_EVIDENCE.md` | 19,631 | 4cddf115021d8406 | `../09_wrong_level_clinical_qi/docs/WRONG_LEVEL_COST_EVIDENCE.md` (byte-identical, verified by sha1 before removal) |
| `docs/WRONG_SITE_BURDEN_EVIDENCE.md` | 18,122 | f234fb976fbb9344 | `../09_wrong_level_clinical_qi/docs/WRONG_SITE_BURDEN_EVIDENCE.md` (byte-identical, verified by sha1 before removal) |
| `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | 104,820 | ef728ddf3ca5db61 | `../10_data_platform_grid/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` (byte-identical, verified by sha1 before removal) |
| `docs/grid_records/JOBS_RECORD_2026-09-27_1544.tsv` | 15,927 | 80e372bc3bf21611 | `../10_data_platform_grid/docs/grid_records/JOBS_RECORD_2026-09-27_1544.tsv` (byte-identical, verified by sha1 before removal) |

### Shared copies kept, recorded as such

| file here | twin | owner | why both exist |
|---|---|---|---|
| `results/schwingnet/corpus_manifold/overlap.json` | `results/schwingnet/inputs/overlap.json` (same bytes) and `../08_render_devices/results/manifold/overlap.json` | this folder (a SchwingNet result) | `inputs/` is the frozen input set of the reported run and keeps its own copy; 08 keeps one because the corpus manifold is its topic; all three are the tracked file `SchwingNet/results/corpus_manifold/overlap.json` at 097933a |
| `results/schwingnet/auto_reference/CALIBRATION.md`, `results/schwingnet/figure2/figure2_transitional.json` | `../02_transitional_naming_truth/results/paper2/auto_reference/CALIBRATION.md`, `.../learning/figure2_transitional.json` | this folder | 02's PREREG reads them; 02 records them as shared (its final-pass section) |

### Laptop paths rewritten to markers (self-containment)

The critic's tree-wide scan still found laptop spellings in copied files of this folder outside `MANIFEST_LOCAL.md`. They are now the markers the other folders use: `<laptop:Desktop>` for the Desktop root that held every repository checkout (`<laptop:Desktop>/spinesurg-ct-nnunet` = spinesurg-ct-nnunet at 097933a, `<laptop:Desktop>/CTSpinoPelvic1K-1` = CTSpinoPelvic1K at 7ddfe38, `<laptop:Desktop>/OpenSpineToolkit` = OpenSpineToolkit at cb43197, `<laptop:Desktop>/XRaySpinoPelvic1K` = XRSpinoPelvic1K at 4f22935), `<laptop:Temp scratchpad>` for the swept session scratchpad (nothing there is a dependency), `<laptop memory folder>` for the live memory notes (copied redacted into `memory/`), `<laptop vendor folder, never read>` and `<laptop home>`. The marker is a spelling of where the file came from, not a path to resolve; the repository and commit are the dependency. Scripts among these copies (`.py`, `.sh`) hard-coded laptop roots and did not run anywhere else before this change either; they are records of how a document was built.

| file | laptop spellings rewritten | left |
|---|---:|---:|
| `code/stats_compare.py` | 1 | 0 |

### Bulk per-run files removed for size (reference by repository)

The folder was 385 MB by `du` on 2026-10-08 against the 150 MB cap for a folder pushed to GitHub. The rule for shedding size allows only bulk per-run files over 2 MB that are byte-identical to a file tracked in a repository, and keeps every summary, table, figure, markdown and manuscript. The files below met the rule (sha1 compared against the tracked file at spinesurg-ct-nnunet 097933a, branch `L6_Class`, private) and were removed: 16 files, 84,887,986 bytes. Each is one `git show 097933a:<path>` away; the summaries that quote them (`a5.json`, `a5_rows_meta.json`, the `mixed_*.json` and `head_*.arch.json` beside them, `LEARNING.md`, `STATUS.md`) stay. The folder's own documents cite these files by their SchwingNet result path, which is the repository path.

| removed | bytes | sha1 | repository file (spinesurg-ct-nnunet 097933a) |
|---|---:|---|---|
| `results/schwingnet/a5_rows.csv` | 5,978,680 | 51caf96db4a55339 | `SchwingNet/results/a5_rows.csv` |
| `results/schwingnet/alpha_0.3_seed0/a5_rows.csv` | 5,780,656 | f0f4e773374618d9 | `SchwingNet/results/alpha_0.3_seed0/a5_rows.csv` |
| `results/schwingnet/alpha_0.3_seed1/a5_rows.csv` | 5,780,674 | fd118f58cdced2bb | `SchwingNet/results/alpha_0.3_seed1/a5_rows.csv` |
| `results/schwingnet/alpha_0.3_seed2/a5_rows.csv` | 5,780,761 | da17e24c5e316d1d | `SchwingNet/results/alpha_0.3_seed2/a5_rows.csv` |
| `results/schwingnet/alpha_0_seed0/a5_rows.csv` | 5,780,625 | 2e20f1c9f7ce9289 | `SchwingNet/results/alpha_0_seed0/a5_rows.csv` |
| `results/schwingnet/alpha_0_seed1/a5_rows.csv` | 5,780,704 | 95212fa520d84b40 | `SchwingNet/results/alpha_0_seed1/a5_rows.csv` |
| `results/schwingnet/alpha_0_seed2/a5_rows.csv` | 5,780,754 | ec874d0f1bd27e67 | `SchwingNet/results/alpha_0_seed2/a5_rows.csv` |
| `results/schwingnet/alpha_1.0_seed0/a5_rows.csv` | 5,780,691 | 44fc223d2a4a1170 | `SchwingNet/results/alpha_1.0_seed0/a5_rows.csv` |
| `results/schwingnet/alpha_1.0_seed1/a5_rows.csv` | 5,780,638 | 0c9d5d342eb26a8c | `SchwingNet/results/alpha_1.0_seed1/a5_rows.csv` |
| `results/schwingnet/alpha_1.0_seed2/a5_rows.csv` | 5,780,747 | 2be6fadb78646239 | `SchwingNet/results/alpha_1.0_seed2/a5_rows.csv` |
| `results/schwingnet/alphabet_loss_inputs/allspine_v8_persons.json` | 3,682,333 | e1a9094e7cb546a8 | `SchwingNet/results/alphabet_loss_inputs/allspine_v8_persons.json` |
| `results/schwingnet/alphabet_loss_inputs/allspine_v9_persons.json` | 3,681,848 | 09ef124c2c650a71 | `SchwingNet/results/alphabet_loss_inputs/allspine_v9_persons.json` |
| `results/schwingnet/corpus_manifold/embedding.csv` | 2,176,792 | 3409a101c039952a | `SchwingNet/results/corpus_manifold/embedding.csv` |
| `results/schwingnet/v9_seed0/a5_rows.csv` | 5,780,625 | 2e20f1c9f7ce9289 | `SchwingNet/results/v9_seed0/a5_rows.csv` |
| `results/schwingnet/v9_seed1/a5_rows.csv` | 5,780,704 | 95212fa520d84b40 | `SchwingNet/results/v9_seed1/a5_rows.csv` |
| `results/schwingnet/v9_seed2/a5_rows.csv` | 5,780,754 | ec874d0f1bd27e67 | `SchwingNet/results/v9_seed2/a5_rows.csv` |

What the rule does not allow to remove, and why the folder stays above the cap: the SchwingNet figures (`figures/`, 45 MB; PNG and PDF, regenerable from their `.record.json` sidecars but figures are kept by the rule), the two packet PDFs of 2026-09-27 (12.0 MB each; manuscripts, and untracked in the working tree so no commit holds them), the private CNS deck v10 (13.0 MB; the only copy outside the Desktop and the TTO package), the IRB determination letter (2.1 MB), and about 1,100 result files under 2 MB each. The next lever, named in `../_plan/PLAN.md` section 8, is the figure PNGs by path; that is Greg's call (`../_plan/BUILD_RECORD.md`).

### Student presenters withheld in the CNS 2026 abstract table

The abstract table (section 12 of `MANUSCRIPTS.md` and its twin in topic 4) still named student presenters in four rows; each author cell now reads `[n student names withheld]` as 02's copy already did. Files: `docs/handoff/MANUSCRIPTS.md`, `docs/handoff/working_notes/topic4_manuscripts.md`.
