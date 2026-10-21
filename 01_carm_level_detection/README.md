# 01 Intraoperative C-arm level detection: from SchwingNet as it stands to a model tested on real fluoroscopy at the hospital

Rank 1 of the spine programme (`../_plan/PLAN.md` section 1). Reader: Greg-only (SchwingNet and level-identification
content, invention aspects, regulatory drafts with staff roles). Built 2026-10-08 from the private repository
`spinesurg-ct-nnunet` (branch `L6_Class`, commit 097933a), the public `CTSpinoPelvic1K` repository (7ddfe38), the 2026-10-08
handoff and the laptop's regulatory documents. Every number below names its file; "not recorded" means no file records it.

## What this project is

SchwingNet names vertebrae on a single C-arm exposure from the shape of each body, without counting from C2 and without a
registration to the preoperative CT. The stack has six pieces: a naming detector (`detector_v5z_final`, YOLO11m-pose, four
corner keypoints, confidence 0.35), a sacrum and vertebra detector (`rx_lodo_carmlspine_1024`, YOLO11m, trained on real
COBRA Elekta and DeepFluoro frames, C-ArmLSpine never seen), a level encoder (`allspine_v9` rung 1, ResNet-18, two-channel
stem, 27 classes C1 to sacrum), a recurrent head (two-layer BiGRU over runs of 2 to 9 bodies), a parameter-free count from
the detected sacrum, and an alphabet coupling that scores the classifier posteriors over the count's ordinals under the
ordinary / L6 / T13 / both / four-lumbar alphabets and stops when they disagree or the margin is low
(`docs/handoff/DATASET_USAGE.md` section 1; `docs/MODEL_CARD.md`). Paper 1, "SchwingNet: a convolutional-recurrent
network for level naming in spine surgery" (Radiology: Artificial Intelligence; `manuscripts/schwingnet/`), is complete in
review and camera-ready copies of 2026-09-27 and held from submission pending the technology-transfer office
(`docs/handoff/MANUSCRIPTS.md` section 2.7).

## Goal

A frozen, registered, latency-measured runtime of the reported stack whose output has been read by humans against a
pre-registered endpoint on exposures from the C-arm actually used at Wayne State / Detroit Medical Center (Department of
General Surgery), under an approved protocol, with the device census, the capture adapter, the reader protocol, the PREREG
and the sample size written before the first frame is scored. The ordered steps S0 to S10 with their gates are `TODO.md`.

## State on 2026-10-08

**What exists.**

| item | state | file |
|---|---|---|
| the four weight files | on the grid, listed 2026-10-08: `detect_v5z_final_best.pt` 42,233,939 B; `rx_lodo_carmlspine_1024/weights/best.pt` 40,601,637 B; `model_rung_1_aug2.pt` 44,824,746 B; `head_allspine_v9_mixed_kmax4_seed0.pt` 8,473,727 B (its folder was not reached by the listing) | `MANIFEST_GRID.md` |
| zero-shot naming on the unseen C-arm, lateral whole frame | 595 / 617 = 96.4 %, 141 cases, Wilson on effective n [92.3, 98.4]; answered 83.0 %, exact on answered 97.7 % | `docs/handoff/RESULTS_CATALOG.md` A2.1; `results/schwingnet/eval_gate/leaks/zeroshot_v9.json` |
| zero-shot AP whole frame | 276 / 631 = 43.7 % (a one-level cranial shift) | A2.2, A2.8 |
| fine-tuned, case-grouped five folds, lateral / AP | 601 / 617 = 97.4 % [93.2, 99.0]; 608 / 631 = 96.4 % [92.5, 98.3] | A3.1, A3.2 |
| count from the detected sacrum, anchored fold frames at 0.74 | 979 / 1,009 = 97.0 % [94.2, 99.2] | A4.7 |
| classifier / count / coupled on 1,009 bodies | 97.7 / 97.0 / 98.2 %; coupled minus count +1.2 [0.0, 3.2] | A5.1, A5.2 |
| stop signal | fires on 23 / 233 frames (9.9 %), catches 5 of 6 erring frames | A5.3 |
| detection on the held-out device at 0.74 (cross-device threshold) | vertebra 231 / 287 = 80.5 % [74.1, 86.8]; sacrum 43 / 56 = 76.8 %; short of the pre-stated 97 %; 93.9 % on the repaired denominator | A6.1, A6.5 |
| same-device detection plateau | 81.7 % lateral / 85.3 % AP at 0.74, 95 % of it by about 10 to 12 frames | `results/schwingnet/indomain/INDOMAIN.md` section 8 |
| the sample size, frozen | 35 error-free at-risk persons for the 90 % exact-level bound; 22 carriers for 85 % variant sensitivity | `results/schwingnet/power/power.json#n_needed_zero_errors`; E.2 |
| real at-risk persons with a frame today | 7, none verified by a human read | `manuscripts/schwingnet/packet/packet_src/persons_available_2026-09-24.json`; A16.6 |
| a deployable container | `code/service/` (FastAPI, Dockerfile, Modal); serves `detect_v5z_epoch25` + M19, not the reported stack; no sacrum count, coupling or abstain flag; no hosting live on 2026-09-14 | `docs/handoff/context/level-service-serving.md` |
| the parity gate for a packaged runtime | defined in `code/cine_latency.py` (boxes equal, names and abstain flags identical, posterior difference below 1e-5 on 50 frames); never run | its docstring |
| regulatory determinations | WSU HPR 2026-269 (public de-identified data, memo 2026-09-02) and HPR 2026-144 (RSNA 2024 lumbar MRI data, 2026-04-21): neither covers hospital data | `regulatory/` |
| protocol drafts for hospital data | Protocol 1 (retrospective, Exempt 4, HIPAA waiver, 2026-09-15), Protocol 2 (prospective silent evaluation), Protocol 3 (prospective passive C-arm capture, "start it first"), the March 2026 multimodal protocol | `regulatory/protocols_2026-09/`, `regulatory/protocol_2026-03/` |

**What does not exist** (each is a step in `TODO.md`).

- The hospital's C-arm make, model and software version: **not recorded** in any file (`../_plan/PLAN.md` section 3, 01).
- Whether its exposures reach PACS, and as which object class (XA, RF, Secondary Capture): not recorded.
- Any capture path from a C-arm (DICOM adapter or frame grabber) in code: none.
- The end-to-end latency of the reported stack on named, uncontended hardware: never measured (`docs/MODEL_CARD.md`
  sections 6.3, 6.6; `HOME/bench/runtime_cost.json` absent on 2026-10-08).
- A sha256 in the registry for the sacrum detector, the fold encoders and the fold heads; `seed` and `code_sha` in
  `devcorpus_train.py` and the CV scorer (`docs/MODEL_CARD.md` sections 1.2, 1.3).
- A human-read level truth on any real intraoperative frame: none anywhere in the programme (`docs/MODEL_CARD.md` 5.1).
- A DMC protocol recorded as submitted: none. The VinDr-SpineXR determination: WSU IRB HPR 2026-330, 29 September 2026 (the notice is on Greg's laptop; spinesurg-ct-nnunet's data platform recorded it 2026-10-10)
  (`docs/handoff/OPEN_QUESTIONS.md` A5).
- A DMC-specific PREREG, reading protocol and named readers: none.
- Posterior calibration (reliability diagram, ECE, Brier): none (`OPEN_QUESTIONS.md` C12).

## Success criteria, pre-stated

| step | the number or gate that counts as done | file that states it |
|---|---|---|
| S0 register | every weight the paper quotes has a `registry.jsonl` line with a sha256; `git status` clean for the C-arm tools | `docs/MODEL_CARD.md` "What this card asks for next" |
| S1 latency | `HOME/bench/runtime_cost.json` with the detector stage present and `machine_load_*` empty; the per-exposure time stated beside the 20 s to one minute the surgeons would wait | `docs/MODEL_CARD.md` section 6 |
| S2 package | parity with `level_prototype.py` on 50 evenly spaced C-ArmLSpine frames: boxes equal, names and abstain flags identical, largest posterior difference below 1e-5 | `code/cine_latency.py` |
| S3 device census | census files for every OR C-arm in use; make, model, software, pixel spacing, bit depth, `PixelIntensityRelationship`, object class written here; ten exposures through the prototype bone-bright and head-up, rendered and looked at | `code/device_census.py`; `docs/REAL_XRAY_DATASETS_SPEC.md` |
| S4 approvals | WSU IRB and DMC Research Compliance letters for Protocols 1 to 3; one records number across the WSU form, the protocol and the DMC application; de-identification plan accepted | `regulatory/protocols_2026-09/PROTOCOL_1_eProtocol_draft_2026-09-15.md` item 164, item 174 |
| S5 PREREG | signed and hashed before the first scored frame; endpoint per person, all reference-named bodies correct, lateral and AP separately, at 0.74 with the 0.25 curve beside it; abstention and stop rates beside every accuracy | `docs/handoff/README.md` section 8; `docs/FLAGSHIP_PLAN.md` G6 |
| S6 retrospective test | ordinary spines: per-person naming with its interval, the 96.4 % and 97.4 % C-ArmLSpine figures as context only; transitional: 35 error-free persons for the 90 % bound and 22 carriers for 85 % sensitivity, or the sentence "not at parity" with the number | `results/schwingnet/power/power.json`; `docs/handoff/RESEARCH_DIRECTIONS.md` section 2.8 |
| S7 fine-tune (only if S6 falls short) | paired bootstrap of fine-tuned minus zero-shot with an interval excluding zero before any "improves"; about 68 persons for 97 % whole-frame AP naming | `results/schwingnet/indomain/INDOMAIN.md` section 8 |
| S8 prospective silent evaluation | the QI primary outcome (surgeon-count versus fiducial disagreement rate) with its interval and every case listed | `../09_wrong_level_clinical_qi/` (the QI protocol) |

## How it relates to the other projects

- **10 data platform**: migration batches B10 (the `~/carm_*` fold banks) and B11 (the identity tables); their state is
  `../10_data_platform_grid/MANIFEST_GRID.md` section 2. The grid checkout is behind the laptop and cannot fetch
  (`MANIFEST_GRID.md`).
- **02 transitional naming truth**: any transitional claim at the hospital, the paper 2 "H1 seen" ledger, and the
  real-frame truth file; `LEVELCHECK_MODEL.md`, `paper2_levelcheck/`, `results/fig6`, `auto_reference/`, `rare_class/`,
  `dual_loss/`, `learning/` live there.
- **08 render devices**: a device card for the hospital C-arm only if the styled route is chosen after S3; `docs/devices/`,
  `results/manifold`, `results/polypose`, the formation documents live there. `PHYSICS_LINKING.md` and
  `or_ready_audit_track_2026-09-22.json` are copied into both 01 and 08 by the plan.
- **09 wrong-level clinical QI**: the QI protocol manuscript (`paper/qi_universal_protocol/`) with the per-case form that
  is the S5 and S8 scaffold lives there.
- **12 website and PACS demo**: `pacs/remote.js` is the client of the `code/service/` contract (`POST /infer`,
  `GET /health`).
- **07 plain-film level identification**: the corner detector's films corpus and `xray-corner-detector-status`; the
  `STUDENT_FLUORO_CORRECTION_GUIDE.md` copied here is the human-read naming convention S5 needs.
- **99 archive**: the superseded resume files and the earlier checkpoints.

## Folder map

| path | holds |
|---|---|
| `CLAUDE.md` | working context: goal, where things are, the standing rules, the traps |
| `STATUS.md` | every result in hand with its id, file and rigor mark; what is superseded and by what |
| `TODO.md` | S0 to S10 with gates, then the open questions, directions and manuscript items that bear on this project |
| `MEMORY.md`, `memory/` | 78 memory notes (22 standing-rule, 46 of the C-arm cut list, 10 added for this project; `MEMORY.md` section 3) with their 2026-10-08 statuses |
| `MANIFEST_GRID.md` | every grid path this project uses or produced, with size, migration state and verification |
| `MANIFEST_CODE.md` | every repository with URL, branch, commit and the files that matter |
| `MANIFEST_LOCAL.md` | every file copied here, where it came from, what was redacted, and what was not copied and why |
| `code/` | `service/`, the 19 pipeline scripts, the cine tools, `fluoro_video/`, `spine_detector_src_snapshot/`, `handoff_builders/` |
| `docs/` | model card, deployment evidence, sweep and guided-acquisition documents (PRIVATE), prior art, input specification, `data_requests/`, `research/`, `external_reports/`, `grid_records/`, `claim/`, `handoff/` |
| `results/` | `schwingnet/` (paper 1 result files, eval gate, power, coverage, in-domain fits, counting, coupling), `physics/`, `carmlspine_v2_lineage_2026-09-21/` (RECORD ONLY) |
| `figures/` | the 2026-09-21 C-ArmLSpine figures; `schwingnet/` main and supplement figures with caption and record sidecars |
| `manuscripts/` | `schwingnet/` (source, ledgers, tables, atlas cards, `packet/` with the two 2026-09-27 PDFs), `superseded/` (rsnai, focused), `talks/` (CNS deck v10, private) |
| `regulatory/` | `hpr_2026-144/`, `hpr_2026-269/`, `vindr_2026-09-25/`, `protocols_2026-09/`, `protocol_2026-03/`, `wsu_dmc_forms/`, `carm_validation_plan_2026-09-21/`, `DUA_advisory_text.pdf`; `README.md` describes each file |
| `grants/aidas_2027/` | the AIDaS SEED 2026-2027 proposal packet of 2026-10-14 (one markdown and its PDF, the Aim 1 execution skeleton, the two figures and their scripts); its `README.md` lists what is left before submission |

## Path prefixes used inside the copied documents

The copied handoff, model card and notes referred to laptop folders by absolute path. Those prefixes were rewritten on
copy so that no text here depends on a laptop: `spinesurg-ct-nnunet:` (the private repository, branch `L6_Class`, 097933a;
also written `ssn:` in the handoff), `CTSpinoPelvic1K:` (the public repository, 7ddfe38; `ctsp:`), `OpenSpineToolkit:`
(cb43197; `ostk:`), `XRSpinoPelvic1K:` (4f22935), `openspineconsortium.github.io:` (c1800f8), `memory:` (the live memory
folder on the laptop; its notes are the copies in `docs/handoff/context/`), `laptop-scratchpad:`, `laptop-session:`, `laptop:Desktop/` and `laptop:`
(laptop-only folders, kept as a record of where something was; `MANIFEST_LOCAL.md` section 4 has the absolute paths), `<laptop project slug>` (the laptop's Claude Code project name inside a swept temporary path) and `<another author's local path>` (a path quoted from a third-party dataset's own file). `~` and
`HOME` mean `/wsu/home/go/go24/go2432`; `$RS` and `CEPH` mean `/rs/rs_grp_oschome/go2432`.

## Size and shape

1,994 files (this folder complete, `MANIFEST_LOCAL.md` included), 397 MB, counted on 2026-10-08 after the fix pass (`MANIFEST_LOCAL.md` section 1): `results/` 244 MB, `manuscripts/` 85 MB, `figures/` 46 MB, `regulatory/` 12 MB, `docs/` 8 MB, `code/` 1.5 MB, `memory/` 0.2 MB (of which `results/schwingnet/coverage/experiment/` is 30 MB after the 29 per-run evaluation JSONs over 2 MB, 154,258,881 B in all, were removed as byte-identical copies of tracked repository files; `MANIFEST_LOCAL.md` section 7 lists each with its sha256). Nothing over 25 MB, no imaging data (the five real radiograph frames the window probe had mirrored from the grid, 776,553 B, were removed on the fix pass and are listed by grid path in `MANIFEST_LOCAL.md` section 2.1), no weights, no `.tif` export, no `.eml` draft (each recorded by path in `MANIFEST_LOCAL.md` section 2).

## On the grid

Since 2026-10-13 (issue #87) `results/`, `figures/`, `manuscripts/` and `regulatory/` of this folder are symlinks to the same path under `/rs/rs_grp_oschome/shared/spine-program/archive/` on the grid, where the files are read through the link; everywhere else they are read from git history at main 5597197. `../ARCHIVE.md` says how, and how a task that must change one of them brings it back into its branch. The counts and sizes in `MANIFEST_LOCAL.md` describe the folder as it was built on 2026-10-08.
