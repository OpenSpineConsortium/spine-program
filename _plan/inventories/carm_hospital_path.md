# INVENTORY 6 — From SchwingNet as it stands to a model tested on real fluoroscopy at the hospital

Written 2026-10-08 for the `spine-program` seed (project family `carm_detection`, the 01_ folder). Every
number, date and path below names the file it was read from. "Not recorded" means no file on the laptop or
the grid records it. The grid was read with `ls`, `head -c` and `squeue` only, through `wsl -e bash -lc 'ssh grid ...'`,
on 2026-10-08; nothing was written there. Hospital = Wayne State University School of Medicine / Detroit Medical
Center, Department of General Surgery (`HANDOFF/README.md` §10; never Neurosurgery).

Repository prefixes: `ssn:` = `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet` (private, branch `L6_Class`,
HEAD 097933a 2026-10-08, "HANDOFF: the handoff for a new student or a fresh Claude project"; `git log -1`);
`sn:` = `ssn:SchwingNet/`; `ctsp:` = `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1` (public, master 7ddfe38);
`HOME` = `/wsu/home/go/go24/go2432`; `CEPH` = `/rs/rs_grp_oschome/go2432`.

## 0. The answer in one paragraph

The model exists as four weight files on the grid plus two parameter-free rules, verified by `ls` today, and it has
one held-out real-C-arm number worth repeating: 595 of 617 lateral vertebrae named exactly on an intraoperative C-arm
it never saw (96.4 %, Wilson on effective n [92.3, 98.4]; `HANDOFF/RESULTS_CATALOG.md` A2.1, file
`sn:results/eval_gate/leaks/zeroshot_v9.json`). Everything a hospital test needs beyond that is missing or unmeasured:
the hospital's C-arm model is **not recorded** anywhere; no DICOM or video capture path from a C-arm exists in code;
the one deployable container (`ssn:service/`) serves an older, weaker release and omits the sacrum count, the coupling
and the abstain rule; the end-to-end latency of the reported stack has never been measured on an uncontended machine
(`ssn:docs/MODEL_CARD.md` §6.3, §6.6); no human has ever read a level on any real intraoperative frame in this
programme (`MODEL_CARD.md` §5.1); the only IRB determinations on disk cover public de-identified data (HPR 2026-269)
and one public MRI challenge set (HPR 2026-144), so a DMC study needs its own protocol, of which three drafts exist and
none is recorded as submitted (`ctsp:proposals/irb/`, `C:/Users/grego/OneDrive/Desktop/IRB/spine_study_protocol.pdf`,
`ctsp:IRB_ADDENDUM.md` edit 3). The pre-stated endpoint and its sample size exist and are frozen (exact level on
transitional persons, Wilson lower bound at or above 90 %: 35 error-free persons; variant sensitivity at or above
85 %: 22 carriers; `sn:results/power/power.json#n_needed_zero_errors`), and today 0 verified and 7 unverified real
at-risk persons exist in the whole holding (`sn:packet_src/persons_available_2026-09-24.json`). The ordered plan is in
§3. The single most decisive cheap step is a header census of ten archived exposures from the hospital's own C-arm,
because every downstream choice (card, adapter, fine-tune, latency target) depends on which machine it is.

## 1. The model as it stands (2026-10-08)

### 1.1 The reported stack ("the SchwingNet model", `HANDOFF/DATASET_USAGE.md` §1; `HANDOFF/RESULTS_CATALOG.md` Part A preamble)

| piece | what | grid path | bytes, date | verified | registered |
|---|---|---|---|---|---|
| naming detector `detector_v5z_final` | YOLO11m-pose, one class "vertebra", four corner keypoints, imgsz 1024, confidence 0.35 (`ssn:docs/CINE_DEMO_RECON_2026-09-26.md` reader 0 §1) | `HOME/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` (same file as `HOME/FluoroCap/detect_v5z_final_best.pt`) | 42,233,939 B, 2026-09-14 | `ls` 2026-10-08 | yes (registry alias `detector_v5z_final`) |
| sacrum / vertebra detector `rx_lodo_carmlspine_1024` | YOLO11m, classes 0 vertebra / 1 sacrum, whole-vertebra boxes, confidence 0.74 ("cross-device") or 0.25; trained on real COBRA Elekta (110 + 8 cases) and DeepFluoro (238 + 24 frames) frames, 3,094 frames, C-ArmLSpine never seen (`DATASET_USAGE.md` §1 table) | `HOME/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt` | 40,601,637 B, 2026-09-22 | `ls` 2026-10-08 | **no** sha256 in the registry (`MODEL_CARD.md` §1.3) |
| level encoder `allspine_v9` | ResNet-18, two-channel stem (image + target-marker), 27 classes C1-C7, T1-T13, L1-L6, sacrum; 2 x 320 x 320 crop, target body 96 px, rung 1 | `HOME/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` | 44,824,746 B, 2026-09-23 | `ls` 2026-10-08 | yes, alias `allspine_v9_fov96_ctx_rung_1_aug2`, sha256 prefix 188f9fcbfa3c6de1 (`CINE_DEMO_RECON` reader 0 §1) |
| recurrent head | `recurrent_order.RunLabeller`: Linear(512 to 256) + GELU, two-layer BiGRU(256), Linear(512 to 27); runs of 2-9 bodies; no alphabet loss | `HOME/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` (+ `.arch.json`) | 8,473,727 B, 2026-09-23 | `ls` 2026-10-08 | not stated |
| count from the sacrum | ordinals counted up from the detected sacrum | `ssn:tools/count_from_sacrum_eval.py` | code | repo 097933a | no parameters |
| alphabet coupling and stop signal | classifier posteriors scored over the count's ordinals under the ordinary / L6 / T13 / both / four-lumbar alphabets; disagreement or low margin = stop | `ssn:tools/alphabet_couple.py` | code | repo 097933a | no parameters |
| fold models (fine-tuned numbers only) | five case-grouped and three day-grouped C-ArmLSpine fold encoders re-initialised from v9, with their heads | `HOME/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt`; `HOME/model_night/heads_carm/head_cv{k}_v9init.pt` | cv0 listed 2026-10-08 | `ls` | aliases exist (`carm_cvmix0_fov96_ctx_rung_1_ft_cv0_v9init_aug2`, `head_cv0_v9init` in `HOME/model_registry/aliases/`) |

The registry ledger `HOME/model_registry/registry.jsonl` has 106 lines (`wc -l` 2026-10-08); its aliases directory
lists the v9 encoder, the v9init fold encoders and heads, `detector_v5z_final`, `detector_v5z_epoch25`, `detector_v6f`
and others (listing 2026-10-08). The pooled all-device detector `dc_P_pooled` now has weights
(`HOME/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt`, 40,601,765 B, 2026-09-23; `ls` 2026-10-08) and
local scores (`sn:results/dc_P_pooled_scores.json`), which `sn:README.md` "What is not in the manuscript" still
records as unfinished.

**Un-suffixed fold files** `model_rung_1_ft_cv{k}_aug2.pt` / `head_cv{k}.pt` start from `allspine_v2_r1`, whose bank
was deleted; the evaluation gate refuses them as held out (`CINE_DEMO_RECON` reader 0 §1). Do not use them.

### 1.2 Inputs and outputs

- **Input.** One 8-bit exposure. Real frames are converted to attenuation (`-log`), then windowed by the field's
  1/5/50/95/99th percentiles onto 27/47/126/216/239, bone bright, head-up by quarter turns
  (`ssn:docs/REAL_XRAY_DATASETS_SPEC.md` "Display"; implemented in `ssn:tools/carmlspine_labels.py` ~L250-260 and
  `deepfluoro_anchor.window_or`). The prototype then histogram-matches to the mean of `HOME/films_drr/img/*.npy`
  (9,109 files; default on), detects at imgsz 1024 conf 0.35, cuts 320 px context crops with the target at 96 px,
  averages a horizontal flip (`CINE_DEMO_RECON` reader 0 §3). The models expect bone bright; raw fluoroscopy is
  usually bone dark and the prototype does not invert (reader 0 §4 "Intensity"). C-ArmLSpine exports are 1024 px at
  0.1915 mm object-plane pixel (header PixelSpacing 1.0 is a placeholder; true detector pitch 0.150 mm;
  `HANDOFF/context/carmlspine-level-experiment.md`).
- **Output per vertebra.** box, four corners (detector), `level`, `level_prob`, `single_crop`, `top3`, `entropy`,
  `region`, `abstain` (decoded name differs from the single-crop name, or probability below 0.5;
  `ssn:tools/level_prototype.py` docstring; rule cited at L355 by `MODEL_CARD.md` §2.2); optional 27-vector posterior.
  Per frame: sacrum box, ordinals from the sacrum, chosen alphabet, stop flag; optional LSTV/TLTV flags
  (`CINE_DEMO_RECON` reader 3 §2 output schema).
- **Service contract** (`ssn:service/app.py`): `POST /infer` (multipart `image`, `conf` 0.35, `imgsz` 640) returns
  `dets[{conf, x0, y0, x1, y1, kpts[4]{name, x, y, v}, level, level_conf, level_single, level_single_conf, level_run,
  top3}]`, `levels`, `run`, `ms`, `width`, `height`, `device`, `model{level_model, release}`; `GET /health` returns
  the registry entry served. The website client that consumes it is
  `C:/Users/grego/OneDrive/Desktop/openspineconsortium.github.io/pacs/remote.js` (`SERVICE_DEFAULT`
  `https://level-id.openspineconsortium.org`, recorded as not live on 2026-09-14 in
  `HANDOFF/context/level-service-serving.md`; not re-checked, no network).

### 1.3 The numbers in hand, with their status

All C-ArmLSpine naming truth is two automatic CBCT labellers scored where they agree (814 of 910 vertebrae, 89.5 %;
T11 0 of 3, T12 6 of 63 named); **no level truth in the study was set by a human** (`MODEL_CARD.md` §5.1). Every
row below therefore carries [AUTO-TRUTH] (`RESULTS_CATALOG.md` Part A preamble).

| quantity | value | status | file |
|---|---|---|---|
| zero-shot lateral whole frame, unseen C-arm (Surgio-B51) | 595 / 617 = 96.4 %, 141 cases, 6 with an error; Wilson on n_eff [92.3, 98.4]; answered 83.0 %, exact on answered 97.7 % | CURRENT, HELD OUT | `RESULTS_CATALOG.md` A2.1; `sn:results/eval_gate/leaks/zeroshot_v9.json` |
| zero-shot AP whole frame | 276 / 631 = 43.7 % (a one-level cranial shift) | CURRENT, HELD OUT | A2.2, A2.8 |
| zero-shot counting the 59 undetected bodies as wrong | 595 / 676 = 88.0 % | CURRENT | A2.6 |
| naming-detector recall of agreed lateral bodies | 617 / 676 = 91.3 % | CURRENT | A2.7 |
| fine-tuned, case-grouped five folds, lateral / AP whole frame | 601 / 617 = 97.4 % [93.2, 99.0]; 608 / 631 = 96.4 % [92.5, 98.3] | CURRENT, HELD OUT | A3.1, A3.2 |
| three / one vertebrae in the field, lateral | 93.1 % [89.2, 96.2]; 74.8 % [70.9, 78.7] | CURRENT | A3.3 |
| day-grouped three folds, lateral whole frame | 568 / 617 = 92.1 % [87.5, 96.0] | CURRENT | A3.5 |
| count from the detected sacrum on anchored fold frames at 0.74 | 979 / 1,009 = 97.0 % [94.2, 99.2] | CURRENT | A4.7 |
| classifier / count / coupled on 1,009 counted bodies | 97.7 / 97.0 / 98.2 %; coupled minus count +1.2 [0.0, 3.2] | CURRENT, HELD OUT | A5.1, A5.2 |
| stop signal | fires on 23 / 233 frames (9.9 %), catches 5 of 6 erring frames | CURRENT | A5.3 |
| detection on the held-out device at 0.74 | vertebra 231 / 287 = 80.5 % [74.1, 86.8]; sacrum 43 / 56 = 76.8 % [64.3, 89.3]; "short of the pre-stated 97 %" | CURRENT, HELD OUT [THR] | A6.1 |
| detection at 0.25 | 90.6 % [84.3, 94.5]; sacrum 83.9 % [73.2, 92.9] | CURRENT | A6.2 |
| detection on the repaired denominator | 201 / 214 = 93.9 % [90.4, 97.1]; clean subset 96.9 % | CURRENT (both printed) | A6.5; `HANDOFF/context/carm-plateau-is-the-denominator.md` |
| same-device detection plateau | 81.7 % LAT / 85.3 % AP asymptote at 0.74, 95 % of it reached by about 10-12 frames | CURRENT | `sn:results/indomain/INDOMAIN.md` §8, T1 |
| styled synthetic corpus, device held out | Cios 91.6-94.0 % vertebra; Elekta 30-33 %; Surgio 14-15 %; pre-stated 97 % criterion not met | CURRENT (not met) | `MODEL_CARD.md` §4.6; A6.13 |
| COBRA Elekta never seen, detection | 6.2 % at 0.74, 18.5 % at 0.25 | CURRENT | A6.9 |
| transitional naming on any real frame with a verified read | **none** | gap | `HANDOFF/OPEN_QUESTIONS.md` C1 |
| the three real L6 patients (one labeller's read) | classifier 0 / 5, coupled 1 / 5 | CURRENT [AUTO-TRUTH] | A5.5 |
| posterior calibration | T13: 0 % right at mean top posterior 0.804; no reliability diagram, ECE or Brier anywhere | gap | `MODEL_CARD.md` §5.3; OPEN_QUESTIONS C12 |
| the 98.22 % lateral CV | v2 lineage, bank deleted | SUPERSEDED; still printed in `sn:tables/tab3_naming.md` and `sn:atlas/model.json` | A2.9, A3.11 |
| selective prediction 99 % at 35.7 % coverage | leaked v2 bank, own test half | LEAKED, not quotable | `HANDOFF/context/INDEX.md`; OPEN_QUESTIONS C13 |

### 1.4 Latency: what is recorded and what is not

| measurement | hardware | numbers | caveat | file |
|---|---|---|---|---|
| `HOME/bench/latency.json`, 2026-09-13 | Tesla V100 (host voh4) and CPU 1/4/8 threads | GPU: detector at 1024 px 22.9 ms median; level model batch 1 2.3 ms; head over a run of 9 0.68 ms. CPU 8 threads: detector 331 ms, level model 18.3 ms | measured on the **older** `films_ann` level model and `detect_v3`, not the reported stack | `head -c` 2026-10-08 |
| `MODEL_CARD.md` §6.3, 2026-09-22 | Windows workstation, 8 physical cores, no GPU, no ultralytics, **contended** | crop 211 ms; encoder 3,350 ms (4 crops x 2 TTA); head 124 ms; link as implemented 422,633 ms per pair, reduced to WORK_PITCH 575 ms; 3-exposure sweep 12.6 s reduced / 856 s as implemented; 7-exposure 27.2 s / 2,562 s; detector **not measured**; synthetic exposures | upper bound; the 734x reduction has no accuracy result behind it on real frames and "must not be shipped on the timing" | `MODEL_CARD.md` §6.3; `HOME/bench/runtime_cost_workstation.json` (`head -c` 2026-10-08, code_sha edf0801) |
| the uncontended GPU job of `MODEL_CARD.md` §6.6 | would be a Slurm GPU job | would give the detector stage and every GPU figure | **never run**: no `HOME/bench/runtime_cost.json` (listing 2026-10-08) and no `ssn:slurm/runtime_cost.sh` (listing of `ssn:slurm/` 2026-10-08) | — |
| `ssn:tools/cine_latency.py` (per-frame, parity-gated against `level_prototype`) | pinned to one GPU type | would give per-stage per-frame latency on a cine | written 2026-09-26, **untracked** at 097933a (`git status`), **never run**: `CEPH/data/or_ready/cine/` does not exist (`ls` 2026-10-08) | docstring |
| level service on the grid login node, 2026-09-14 | 8 old CPUs; V100 | 1.6-2.3 s per 2048 px film end to end, about 0.9 s fixed overhead; V100 detector 23 ms + 2.3 ms per crop | the service's older release | `HANDOFF/context/level-service-serving.md` |
| comparator | — | LevelCheck registration 4.7 s per image (2012 card) and 17-72 s per registration in theatre; surgeons would wait 20 s to one minute, more than a minute in 60.6 % (305 / 503) of helpful cases | literature as recorded | `MODEL_CARD.md` §6 (citing `paper/focused/main.tex`) |

Plain reading: **the end-to-end latency of the reported stack on named, uncontended hardware is not measured.**
The QI manuscript's "the encoder takes 17 ms per frame" (`ssn:paper/qi_universal_protocol/main.tex`, "What the engine
does") has no result file named beside it in `HANDOFF/MANUSCRIPTS.md` §5 and must not be repeated until one exists.

### 1.5 The deployable shape that exists: `ssn:service/`

Six files (`README.md`, `app.py`, `model_defs.py`, `Dockerfile`, `requirements.txt`, `modal_app.py`; 41 KB; last
touched 2026-09-14). It is self-contained (detector, crops, ResNet-18 + BiGRU, contiguous-run decode), pulls weights at
start-up from the private Hugging Face repo `gregoryschwingmdphd/level-id-weights` with a read token, runs CPU by
default and GPU when present, and the same container targets a Hugging Face Docker Space, Modal, Fly.io, EC2 or a
workstation behind a tunnel (`service/README.md`). What it serves is **not the reported stack**: `detector.pt =
detect_v5z_epoch25`, `level_model.pt = M19 films_all2 rung1`, `recurrent_head.pt` (`level-service-serving.md`;
`CINE_DEMO_RECON` reader 0 "Not found"). It has no sacrum detector, no count, no coupling, no abstain flag, no
attenuation/window conversion for raw fluoroscopy, and no hosting is live (Hugging Face returned 402 for both
accounts; Modal, Fly.io, EC2 and a tunnel were options; `level-service-serving.md`). `ssn:tools/deploy_service.py`
hashes the three weights, writes `registry.json`, uploads to the private repo and refuses a public one.

### 1.6 Beyond one frame: what the code can do and what it has only done on renders or a phantom

- **The sweep and chain** (`ssn:tools/sweep_map.py`, `needle_confirm.py`): overlapping exposures from the sacrum
  linked by correlation restricted to about 0.6 body of the commanded step; held-out CTSP renders 2-body frame
  72.1 to 95.2 %, chains 100 % under the end rule; 25 real lumbar films 21 of 25 chains; TotalSegmentator bench
  522 CTs 98.5 % (`HANDOFF/context/sweep-map-replaces-registration.md`, sweep_v3 only). Every sweep number uses
  truth boxes (`MODEL_CARD.md` §5.5). The link costs seven minutes per pair at full resolution (§6.2-6.3).
- **The guided-acquisition loop and the digital fiducial** (`ssn:tools/acquisition.py`, `validate_guided.py`,
  `guided_console.py`, `tests/test_acquisition.py`, `slurm/guided_validate.sh`): built, unit-tested, geometry recovered
  to 1.2 mm **on a synthetic phantom only**; corpus job 40376577 was running at the last record and "any corpus
  number: none is trustworthy yet. Do not quote one." (`ssn:docs/GUIDED_ACQUISITION.md` STATUS). The grid holds
  `HOME/model_night/guided/{calib,far,main,near,rot,sloppy}` and `HOME/model_night/fiducial/` (listing 2026-10-08;
  contents not opened). Private: invention aspects A and E (`HANDOFF/MANUSCRIPTS.md` §15, §17).
- **The radiographer's protocol** for the sweep is written for a technologist (`ssn:docs/SWEEP_PROTOCOL.md`; private).
- **Cine / video**: a causal tracker with frozen constants (`sn:results/cine/tracker_config.json`, frozen 2026-09-26
  before any Bournemouth frame was seen; untracked), the scorer `ssn:tools/cine_eval.py` and the timer
  `cine_latency.py` (both untracked); the Bournemouth cervical quantitative-fluoroscopy release is on the grid as raw
  only (`CEPH/data/realxray/bournemouth_qf/raw/Cervical_Database.mat`, 24,380,812 B, 2026-09-26; no `meta/`,
  `images/`; `ls` 2026-10-08) and "no model has run on a Bournemouth frame" (`ssn:docs/BOURNEMOUTH_QF_HARNESS.md`).
  Public fluoroscopy clips were screened and cut (`CEPH/data/external/fluoro_video/clips/` with `REPORT.md`,
  `manifest.json`, `clips.csv` and about 20 clip folders; `ls` 2026-10-08) by `ssn:tools/fluoro_video/` (untracked);
  none scored. The 301-frame C-ArmLSpine CBCT spin of case134 is exported detection-only
  (`CEPH/data/realxray/carmlspine_sweep/`, pooled body recall 0.936 at 0.25; `CINE_DEMO_RECON` reader 3 §6); case39's
  spin is not exported.
- **Fourteen cine data requests, SX-Stitch and Balgrist**: drafted, verified addresses, **none sent**
  (`HANDOFF/MANUSCRIPTS.md` §16; `ssn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`; `ssn:docs/fluoro_requests_eml/`).

### 1.7 Lineage defects that a hospital submission would be asked about

- Fold encoders, fold heads and the sacrum detector have no sha256 in the registry; `devcorpus_train.py` and the CV
  scorer write no `code_sha` or `seed` (`MODEL_CARD.md` §1.2-1.3; "What this card asks for next" items 1-2).
- The fold banks behind the fine-tuned numbers hold 2,632 VinDr crops and 2,100 FluoroCap crops and both NHANES
  copies; VinDr is outside HPR 2026-269 (`DATASET_USAGE.md` §3.2, §5). The clean equivalent exists as the 250
  `name_fill` cells (v9 base, no VinDr or FluoroCap): lateral 98.1 %, AP 97.0 % on REP truth per protocol cell
  (`RESULTS_CATALOG.md` A9.4; `HANDOFF/RECIPES.md` §7.2). The VinDr determination request was drafted and sent to Greg
  2026-09-25; its number is not recorded (`OPEN_QUESTIONS.md` A5).
- Whether the 148 C-ArmLSpine cases are 148 people is unknowable from the files (`OPEN_QUESTIONS.md` E1).
- `ssn:tools/level_prototype.py`, `carmlspine_eval.py`, `patient_keys.py`, `pipeline_state.py` and
  `test_patient_keys.py` carry **uncommitted working-tree edits** at 097933a (`git status --short` 2026-10-08).

## 2. What a hospital test needs, item by item

| need | what exists (file) | what does not exist | gate before the next step | who decides |
|---|---|---|---|---|
| **the hospital's C-arm make, model, software version** | nothing. Searched `HANDOFF/*.md`, `ssn:docs/*.md`, `ssn:paper/`, `ctsp:proposals/irb/*`, `ctsp:COMMERCIALIZATION.md`, `ctsp:IRB_ADDENDUM.md`, `C:/Users/grego/OneDrive/Desktop/IRB/*.pdf`, the memory notes, "C-Arm Validation Research Plan.pdf" for OEC, Cios, Ziehm, Zenition, Pulsera, Arcadis, Harper, Sinai-Grace, DMC + C-arm: no hit names the hospital's machine | **not recorded** | a DICOM header census (`ssn:tools/device_census.py`, output format `ssn:docs/devices/census/*_headers.md`) of ten archived exposures from each OR C-arm in use: Manufacturer, ManufacturerModelName, SoftwareVersions, ImagerPixelSpacing, SID, Rows/Columns, BitsStored, PixelIntensityRelationship, PositionerType, Modality (XA/RF/SC) | Greg with Radiology informatics and the OR; the Neurosurgery co-investigator the Protocol 1 draft lists as "[Dr To]" (`ctsp:proposals/irb/PROTOCOL_1_eProtocol_draft_2026-09-15.md` Personnel; a memory note spells the name differently and says "spelling to confirm": `HANDOFF/context/learned-formation-refuted-calibrate-instead.md`) |
| **image capture from the C-arm** | (a) PACS/DICOM: "DMC archives intraoperative fluoroscopy to PACS for at least one neurosurgical service" (PROTOCOL_1 draft a(ii)); the draft asks Radiology whether OR C-arm saves and navigation screenshots land in PACS or a separate archive (item 152, 162); DICOM readers exist for C-ArmLSpine (`ssn:tools/carmlspine_io.py`, `inspect_dicom_tree.py`) and the display conversion is specified (`REAL_XRAY_DATASETS_SPEC.md`); (b) live video: the external-box route is cleared precedent (NuVasive/Globus Pulse with LessRay, K180038; `ssn:docs/CARM_DEPLOYMENT_EVIDENCE.md` §7) and the frame-grabber architecture is described in the external roadmap (`ctsp:C-Arm Validation Research Plan.pdf` Phase III, up to 60 frames per second); (c) on-device: Siemens Cios Alpha/Flow/Spin via Cios OpenApps is the only vendor-sanctioned route, with unknown compute and unknown live-frame access (`CARM_DEPLOYMENT_EVIDENCE.md` §1-6) | no adapter from an RF/XA/Secondary-Capture object of an unknown device to the runtime's attenuation-and-window input (`PixelIntensityRelationship`, VOI LUT, inversion, orientation); no frame-grabber code (`tools/fluoro_video/` reads files, not a capture card); no hardware | ten archived exposures of the hospital device pass through `level_prototype.py` bone-bright and head-up, **rendered and looked at** (the "render the mask" rule, `ctsp:CLAUDE.md`), with the orientation net's up/down flag recorded | Greg; Radiology (export path); Biomedical engineering for any video tap |
| **a device card for the hospital C-arm** | the recipe: `ssn:tools/device_fit.py` fits nine image-formation terms leave-one-group-out on up to 40 real frames **with exact geometry and attenuation** (CT + pose) (`HANDOFF/RECIPES.md` §6); cards on disk for Cios Fusion, Elekta XVI, BV Pulsera, PIXIUM 4600 (`ssn:docs/devices/*.json`), and on the grid also `surgio_b51_dr/raw/display` and `varian_halcyon` (`CEPH/data/or_ready/devices/`, `ls` 2026-10-08); the unpaired-path validation is `device_style.py stats` (real-vs-styled distance against a real-vs-real floor; `HANDOFF/context/k-devices-one-network.md`) | a hospital C-arm will have no paired CT + pose frames, so a fitted card in the DeepFluoro sense is not obtainable there; and the styled-corpus detectors failed their pre-stated criterion on two of three devices (`MODEL_CARD.md` §4.6), so a card is not the route that worked | decide the route from the census: if real frames can be exported, skip the card and fine-tune on real frames (§2 row "sample size"); a card only if styled renders are wanted for the arc of oblique poses (`HANDOFF/context/oblique-angles-and-sweep-vision.md`) | Greg |
| **a runtime** | the gated reference `ssn:tools/level_prototype.py` (grid GPU, env `fluorogen`; `CINE_DEMO_RECON` reader 0 §2 gives the exact command and the sbatch pattern); the container `ssn:service/` and `tools/deploy_service.py`; the parity gate in `cine_latency.py` (boxes equal, names identical, posterior difference below 1e-5 on 50 frames) | a packaged runtime of the **reported** stack (naming detector + sacrum detector + v9 encoder + head + count + coupling + abstain) with `registry.json` and sha256 for every file; a measured uncontended latency; a decision on hardware (edge GPU in theatre, workstation, or vendor sandbox; "no CPU, GPU or RAM figure surfaced for any C-arm examined", `CARM_DEPLOYMENT_EVIDENCE.md` §6) | parity with `level_prototype` on 50 C-ArmLSpine frames; `latency.json` written on named hardware with the detector stage present; the per-exposure figure read against the 20 s to one minute the surgeons stated (`MODEL_CARD.md` §6) | Greg |
| **a reference standard and reader protocol** | three routes written down: (1) registration of the intraoperative image to the same patient's CT, labels projected, agreement with the operative note at or above 98 % (PROTOCOL_1 draft H2, procedures item 94); (2) operative note plus postoperative imaging, blinded radiologist (`ssn:paper/qi_universal_protocol/main.tex` "Phase 1"; `ctsp:IRB_ADDENDUM.md` edit 3 "Ground truth is free"); (3) a human read on CT through the two-stage review tree, with an automated reference admissible only where its per-subtype PPV lower bound is at or above 0.90, which no rule reaches for L6, T13 or four-lumbar (`sn:LEVELCHECK_MODEL.md` §14; `RESULTS_CATALOG.md` B.3); the naming convention for a human read (`ssn:docs/STUDENT_FLUORO_CORRECTION_GUIDE.md`); the endpoint unit "per person, every reference-named body correct" (`LEVELCHECK_MODEL.md` §4) | no human-read level truth on any real intraoperative frame anywhere in the programme; no DMC reader named (the stage-2 confirmer "Dr Tech" is recorded by nickname only, `OPEN_QUESTIONS.md` A18); no frozen DMC reading protocol | `PREREG.md` with rule, success number and inputs, signed by Greg and hashed before the first frame is scored (`HANDOFF/README.md` §8 day 5; `LEVELCHECK_MODEL.md` §9 freeze) | Greg; two readers and an adjudicator |
| **IRB and institutional approvals** | WSU HPR 2026-269, memo 2026-09-02, tool filed 2026-08-28: "Open Spine Consortium: Secondary Analysis of Publicly Available, De-Identified Imaging Datasets and the Derived Annotations, Software, and Models Produced From Them": not human participant research; scope limited by its item 7 to datasets downloadable "without an application, request for permission, eligibility review, or data use agreement" (`ctsp:IRB_VinDr_2026-09-25/00_cover_note_to_IRB.md`; memo `ctsp:2026 269 Schwing IRB Not HPR Determination 9.2.26.pdf`, 14 scanned pages with no text layer; tool `ctsp:OSC_HPR_Determination_public_datasets.pdf`). WSU HPR 2026-144, 2026-04-21, "Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection", RSNA 2024 Lumbar Spine Degenerative Classification data only (`ctsp:IRB Not HPR Determination 4.21.26.pdf`). Drafts for DMC patient data: Protocol 1 retrospective imaging and records study, Exempt Category 4 with HIPAA waiver, intraoperative fluoroscopy-CT pairs as a named source (`ctsp:proposals/irb/PROTOCOL_1_eProtocol_draft_2026-09-15.md`, 2026-09-15); Protocol 2 prospective silent evaluation, Expedited (`ctsp:proposals/irb/IRB_two_protocols_summary.pdf`, September 2026); Protocol 3, prospective passive capture of intraoperative C-arm images, minimal risk, waiver, "longest lead time of the three, start it first" (`ctsp:IRB_ADDENDUM.md` edit 3, 2026-09-10); the earlier DMC retrospective multimodal spine dataset protocol with a named faculty sponsor (`C:/Users/grego/OneDrive/Desktop/IRB/spine_study_protocol.pdf`, `Data_Collection_Tool.pdf`, March 2026); CITI completion (`Desktop/IRB/GREG/`, personal, not copied); the DMC research review process documents (`Desktop/IRB/dmc-research*.pdf`) | no record that any DMC protocol was submitted; faculty sponsor, co-investigators and the records count are placeholders in the Protocol 1 draft; the VinDr determination number; the de-identification plan for C-arm objects (no burned-in-text header flag; OCR screen every frame, PROTOCOL_1 draft item 174); a data use agreement track with DMC/Tenet legal if anything is to leave the research track (`IRB_ADDENDUM.md` edit 2; Greg-only) | WSU IRB approval and DMC Research Compliance for Protocol 1 (retrospective) before any PACS pull; Protocol 3 before any prospective capture; one records number identical on the WSU form, the protocol and the DMC application (PROTOCOL_1 draft item 164) | Greg (PI, resident: needs a faculty sponsor), the sponsor, WSU IRB, DMC Research Compliance, Radiology and Neurosurgery letters of support |
| **a pre-registered endpoint** | paper 1's targets: exact level on transitional real frames with Wilson lower bound at or above 90 %, variant sensitivity lower bound at or above 85 % (`ssn:docs/FLAGSHIP_PLAN.md` G6 item 4; `sn:results/power_table.json#targets_pct`); paper 2's frozen comparator: H1 superiority over 82.2 % (Peh 1999), H2 over 97.6 % (Manbachi 2018), H6 ordinary non-inferiority at 92.6 % with margin 5 (`sn:LEVELCHECK_MODEL.md` §3, §5, frozen by commits ecae75f to d0403de; `RESULTS_CATALOG.md` B.2); endpoint per person, all reference-named bodies correct, detector confidence 0.74, whole frame, coupled call (§4); the stop signal F1 and the mechanism test M1 as pre-specified secondaries (§12); the QI protocol's primary outcome: disagreement between the surgeon's count and the fiducial at the time-out, adjudicated against postoperative imaging (`qi_universal_protocol/main.tex`) | a DMC-specific PREREG; a decision whether the hospital study scores naming (paper 1 frame), the comparison (paper 2 frame) or the process (QI frame) | the PREREG signed and hashed before the first scored frame; the paper 2 ledger must carry "H1 seen" before any G3 test transitional person is scored (`sn:PAPER1_SCOPE.md`; `HANDOFF/context/paper-split-2026-09-24.md`) | Greg |
| **sample size** | Wilson lower bound with zero errors: 88.65 % at n 30, 92.13 at 45, 93.98 at 60, 95.42 at 80, 96.30 at 100, 97.13 at 130; with one error 83.33 / 88.43 / 91.14 / 93.25 / 94.55 / 95.77; two errors 78.68 / 85.17 / 88.64 / 91.34 / 93.00 / 94.56; five errors 66.44 / 76.50 / 81.93 / 86.19 / 88.82 / 91.31 (`sn:results/power_table.json#lower_bound_pct_by_k_then_n`, every cell checked against scipy, `sn:NUMBERS.md` L231). Smallest n for the 90 % bound: 35 / 53 / 69 / 113 persons at 0 / 1 / 2 / 5 errors; for 85 % sensitivity 22 / 34 / 45 / 74 carriers (`sn:results/power/power.json#panel_a`, `#n_needed_zero_errors`; `RESULTS_CATALOG.md` E.2). Power: 80 % power for the 90 % bound needs 99 persons at a true 97 %, 69 at 98 % (E.4). Paper 2: n_min 19 / 48 / 152 for 82.2 / 92.6 / 97.6 %; the 97.6 % comparator "cannot be exceeded at any reachable n" (152 error-free persons give power 0.22 at a true 99 %; E.6; `LEVELCHECK_MODEL.md` §7). Detection on a new device: about 12 patients, 24 frames in both views, reach 95 % of the same-device plateau; naming whole-frame AP 97 % needs about 68 persons of the device; collimated fields have not flattened by 88 persons (`sn:results/indomain/INDOMAIN.md` §8). Protocol 1 draft: 1,500 verified vertebrae per stratum, 6,000 in four strata, 1,500-2,500 intraoperative images from 800-1,500 patients, records request placeholder 40,000 studies (item 80). QI protocol: "powered to estimate, not to detect a change in wrong-level events, which at 0.12 % would need tens of thousands of cases" (L229-231; E.10). **Derived here, from recorded rates, not from a file:** at the 12.9 % transitional prevalence recorded in `sn:LEVELCHECK_CLAIM.md` §2 (Nakagawa 2017; `RESULTS_CATALOG.md` B.8), 35 transitional persons are expected among about 270 consecutive lumbar patients (35 / 0.129 = 271); at the about 9 % count-changing rate recorded there (Hanhivaara 2020), 22 carriers among about 245 (22 / 0.09 = 244) | the person-level intraclass correlation for transitional endpoints (needed for any two-proportion power; `OPEN_QUESTIONS.md` C10); any power calculation for device-level differences (E.13) | the n is written into the PREREG with the error allowance stated; the planning accuracies of 95-99 % "rest on no transitional measurement" and must be labelled planning values (`HANDOFF/literature_state/power.md` §6; E.14) | Greg |
| **data and licence constraints on what may be used at the hospital** | the two-track rule: research track (WSU, grid, students, NC-licensed data) and commercial track never cross; CTSpine1K and everything derived (CTSpinoPelvic1K) is CC BY-NC-SA and can never train a commercial model; DeepFluoro and COBRA are NC; BUU is "No License Provided" plus an EULA and "no weight trained with BUU laterals leaves until Greg has read the licence" (`ctsp:COMMERCIALIZATION.md` §2-3, Greg-only; `HANDOFF/RESEARCH_DIRECTIONS.md` §6 "Three things run through the whole order") | a licence decision on BUU; a written statement of which track the hospital test is on (a research study at the hospital on the research track is consistent with the rule) | Greg's BUU decision before any weight leaves the grid; nothing in a public or student-facing document names the commercial goal (`HANDOFF/context/commercialization` is Greg-only) | Greg |

## 3. The ordered plan: engineering and regulatory, each step with its gate

The order follows two constraints: regulatory lead time is longer than engineering time (IRB_ADDENDUM edit 3 "start it
first, not last"), and nothing should be scored at the hospital before the stack, the runtime and the reading
protocol are frozen (the recurring failure here is a number that is wrong but plausible, `ctsp:CLAUDE.md`).

| step | what | pre-stated success number or gate | depends on | who decides |
|---|---|---|---|---|
| S0 | **Freeze and register the reference stack.** `python tools/model_registry.py register` for `rx_lodo_carmlspine_1024`, the five v9init fold encoders and heads and the pooled `dc_P_pooled`, with `--metrics`; add `seed` and `code_sha` to `devcorpus_train.py` and the CV scorer; commit the five edited tools and the three untracked ones (`cine_eval.py`, `cine_latency.py`, `tools/fluoro_video/`) or copy them into the seed's `code/` | every weight the paper quotes has a line in `HOME/model_registry/registry.jsonl` with a sha256; `git status` clean for the C-arm tools | nothing | none (engineering); Greg commits when he asks |
| S1 | **Measure the uncontended latency** of the reported stack: write the `§6.6` script as a file (not `--wrap`), run `eval_runtime_cost.py --selftest` then the job with `--frames CEPH/data/realxray/carmlspine/images --bodies 6 --threads 1 4 16`; run `cine_latency.py` on the case134 spin once its prototype outputs exist | `HOME/bench/runtime_cost.json` with the detector stage measured and `machine_load_*` empty; per-exposure time stated beside the 20 s to one minute the surgeons stated (`MODEL_CARD.md` §6) | S0 | none |
| S2 | **Package the reported stack** into the service container: replace `detect_v5z_epoch25` + M19 with `detector_v5z_final` + v9 encoder + v9 head, add the sacrum detector, the count, the coupling, the abstain flag and the attenuation/window conversion of `REAL_XRAY_DATASETS_SPEC.md`; `deploy_service.py` writes `registry.json`; keep weights in the private repo only | parity with `level_prototype.py` on 50 evenly spaced C-ArmLSpine frames: boxes equal, decoded names and abstain flags identical, largest posterior difference below 1e-5 (the gate `cine_latency.py` already defines) | S0 | none; hosting choice is Greg's (`level-service-serving.md`) |
| S3 | **Discover the hospital device**: which OR C-arms the co-investigating service uses; whether their exposures reach PACS as XA/RF/SC or sit in the C-arm's own archive; a header census of ten archived exposures per device (`device_census.py`) under whatever access the retrospective protocol grants; record make, model, software version, pixel spacing, bit depth, `PixelIntensityRelationship` | the census files exist and the make/model line is written into the seed's `MANIFEST_GRID.md` and `README.md` ("not recorded" becomes a name) | S4 for PACS access (or a letter allowing a technical pilot on fully de-identified exports) | Greg; Radiology informatics; the Neurosurgery co-investigator |
| S4 | **Regulatory**: fill the Protocol 1 placeholders (faculty sponsor, co-investigators, one records number consistent across the WSU form, the document and the DMC application, item 164), submit Protocol 1 and Protocol 2 together as the summary states, and submit Protocol 3 (prospective passive capture of the intraoperative C-arm images) with them; obtain the Radiology letter on the export path and the Neurosurgery letter; file the DMC Research Compliance application with the same names; disclose the commercial interest in the eProtocol and COI (Greg-only, `IRB_ADDENDUM.md`); obtain the VinDr determination number and print it or retrain without VinDr (`DATASET_USAGE.md` §5) | approval letters; the de-identification plan accepted (OCR screen of every frame; C-arm objects carry no burned-in-text flag) | the drafts above; a faculty sponsor | Greg; the sponsor; WSU IRB; DMC Research Compliance |
| S5 | **Freeze the DMC reading protocol and PREREG** before the first frame: reference standard = same-patient CT registration where a CT exists (H2: labels agree with the operative note in at least 98 % of vertebrae), otherwise operative note plus postoperative imaging adjudicated blind; every transitional person read by a human on CT; endpoint per person, all bodies correct, lateral and AP separately, at detector confidence 0.74 with the 0.25 curve beside it; abstention and stop rates printed beside every accuracy; intervals clustered by person | `PREREG.md` signed by Greg and hashed; the two readers and the adjudicator named (in the private seed, not in student material) | S4 | Greg; the readers |
| S6 | **Retrospective in-domain test (zero-shot, no fine-tune)** on the hospital device's archived exposures: run the S2 runtime on every exported lateral and AP exposure with a reference; stratify ordinary / transitional, instrumented / not (Protocol 1 H3 strata) | pre-stated: naming per person on ordinary spines reported with its interval against the 96.4 % zero-shot and 97.4 % fine-tuned C-ArmLSpine figures as context only; transitional: 35 error-free persons for the 90 % bound, 22 carriers for 85 % sensitivity, or the sentence "not at parity" with the number (`HANDOFF/RESEARCH_DIRECTIONS.md` §2.8 stop rule); detection recall at 0.74 and 0.25 with the curve; the first 12 patients (24 frames) tell whether the device sits near the 81.7 / 85.3 % plateau | S2, S4, S5 | Greg (PREREG) |
| S7 | **Fine-tune on the hospital device** only if S6 detection or AP naming falls short: the recipe of `ssn:slurm/carmlspine_cv_v9init.sh` on a person-disjoint split (`tools/patient_keys.py`, `eval_gate.py`), case-grouped and acquisition-day-grouped folds both reported, pooled never quoted without the device-held-out arm beside it (`HANDOFF/context/pooled-vs-lodo-device-designs.md`) | paired bootstrap of fine-tuned minus zero-shot with a CI excluding zero before any "improves" sentence (`BENCHMARK_PROTOCOL.md` rule 3); about 68 persons for 97 % whole-frame AP naming (`INDOMAIN.md` §8) | S6 | Greg |
| S8 | **Prospective silent evaluation** (Protocol 2 / 3): the frozen runtime runs on incoming cases with no output to anyone treating the patient; disagreements with the CT-verified level and the operative note adjudicated afterwards; the QI process measures recorded per case (anchor used, exposures, minutes, dose, needles, disagreements) | the QI protocol's four-month baseline then eight-month assisted phase, primary outcome the surgeon-count versus fiducial disagreement rate with its interval and every case listed; near-miss rate as the proxy (`qi_universal_protocol/main.tex`) | S4 (Protocols 2-3), S6 | WSU IRB; Greg |
| S9 | **Phantom and cadaver bench for live capture, in parallel**: register any X-ray machine used outside a clinical service with WSU OEHS (`C:/Users/grego/OneDrive/Desktop/x-ray_machine_registration_form.doc`, the State of Michigan registration; the Application for Use of Ionizing Radiation is a separate form); a frame grabber on the auxiliary video output; an anthropomorphic lumbar phantom; then a whole-body cadaver through the Anatomical Gift Program and the Institutional Biosafety Committee (`ctsp:C-Arm Validation Research Plan.pdf` Phases III-IV, an external roadmap, reference only per `HANDOFF/MANUSCRIPTS.md` §17); the guided loop's corpus arms read first, and only if the `frame` control lands near 85 % (`GUIDED_ACQUISITION.md`) | the capture adapter produces frames that pass the S3 render check; the commanded-step error on a physical gantry measured (the roadmap cites about 16 mm manual repositioning error against a 21 mm search half-width); geometry recovered on a physical phantom, replacing the synthetic-phantom 1.2 mm | S2; Radiation Safety approval | Greg; WSU OEHS; Anatomical Gift Program |
| S10 | **Reader study and the comparison** (paper 2; a fourth MRMC protocol later, `IRB_ADDENDUM.md` edit 5): the frozen LevelCheck comparator with human-read transitional persons; fix `sn:tools/fig6_score.py` (`T1/blinded/meta_ref/` to `T1/open/meta_ref/`) and re-score the open gate first (`OPEN_QUESTIONS.md` F3); never release the blinded gate before `CEPH/data/fig6/unblinding/RELEASE_v2.json` is written by a person (`RESULTS_CATALOG.md` B.6) | at least 19 verified at-risk persons with a frame for H1; today 7 unverified | S5, S6 | Greg; the TTO answer on disclosure timing (`HANDOFF/README.md` §7) |

What not to carry forward (so a reader does not rediscover it): the 98.22 % v2-lineage CV; the 99 % at 35.7 %
coverage; the "100 % sacrum on DeepFluoro" (a same-device number, `ssn:docs/or_ready_audit_track_2026-09-22.json`);
any styled-corpus "design B beats A" sentence (seed spread of the same order, `MODEL_CARD.md` §4.6); the R + C = 22
rule; any guided-loop corpus number; the 734x linker speed-up as a shipped timing; CycleGAN / CUT / ADDA / SDXL
translation (no gain in any arm, `RESEARCH_DIRECTIONS.md` §2.2).

## 4. The folders, file by file: dates, git state, best files, what supersedes what, what is lost if dropped

### 4.1 `ssn:service/` and `ssn:tools/deploy_service.py`
Six small files, 2026-09-14, tracked at 097933a. Best files: `model_defs.py` (the crop transform that must match
training: `TGT_PX` on a `SIZE` canvas, band of 2 x rung + 1 heights, marker channel; `contiguous_run` decode) and
`app.py` (the contract). Superseded in content (older weights) but not in shape. Lost if dropped: the only
container-ready inference and the website contract.

### 4.2 `ssn:docs/` (the C-arm and hospital subset; 20 MB, 90 files, 2026-04 to 2026-09-27)
Best: `MODEL_CARD.md` (2026-09-22, 43 KB; §6 runtime), `CARM_DEPLOYMENT_EVIDENCE.md` (2026-09-20; the two deployment
routes, with the two refuted claims recorded), `GUIDED_ACQUISITION.md` and `SWEEP_PROTOCOL.md` (private invention
aspects), the four verified evidence briefs (`WRONG_LEVEL_COST_EVIDENCE.md`, `WRONG_SITE_BURDEN_EVIDENCE.md`,
`SWEEP_TIME_EVIDENCE.md`, `COUNTING_EVIDENCE.md`; three refutation votes per claim), `FLAGSHIP_PLAN.md` (gates G0-G7),
`BENCHMARK_PROTOCOL.md` (the registration ceiling arm), `REAL_XRAY_DATASETS_SPEC.md` (the input convention),
`CINE_DEMO_RECON_2026-09-26.md` and `CINE_DEMO_BUILD_PLAN_2026-09-26.md` and `BOURNEMOUTH_QF_HARNESS.md` (the cine
path), `devices/` (cards, 1.1 MB; the census format), `grid_records/JOBS_RECORD_2026-09-27_1544.md` (every job and
how to continue it, written before the 2026-09-27 cancellation), `or_ready_audit_track_2026-09-22.json` (the split
audit), the prior-art files (`PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md`: the human naming number 69.6 % unassisted and
97.6 % with LevelCheck; `research_registration_free_search_2026-09-22.md`: Rao EMBC 2024 recall 0.964-0.982 on 578
C-arm images, class-agnostic). Superseded: `RSNAI_PLAN.md` (checklist for `paper/rsnai/main_v2.tex`, stopped
2026-09-22), the eight `carmlspine_*_2026-09-21/22.json` (v2 lineage), `RESUME_2026-09-22_PM.md` (367 KB history),
`PATENT_PACKAGE.md`. Private and not for the student seed: `INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md`,
`provisional/`, `research_patent_2026-09-18.json`, `disclosure_*`, `CREDENTIALS_SETUP.md`. Contact data to redact on
copy: `FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`, `FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md`, `fluoro_requests_eml/`
(11 drafts), `outreach/balgrist_data_request_2026-09-21.md`, `data_requests/SX-Stitch_request.md`,
`IRB/HPR_determination_VinDr-SpineXR_draft.md` (a phone number). Lost if dropped: the deployment evidence, the
runtime measurement method, the radiographer protocol and the input convention; none of these is in a paper.

### 4.3 `sn:` = `ssn:SchwingNet/` (2.1 GB; manuscript 2026-09-22 to 2026-09-27)
Paper 1 "SchwingNet: a convolutional-recurrent network for level naming in spine surgery" (`sn:TITLE.md`; the
transitional clause removed 2026-09-24); complete in review and camera-ready copies; held from submission by Greg;
one placeholder, the VinDr determination number (`HANDOFF/README.md` §7). Best: `main.tex` + `sections/` +
`supplement.tex` + `tables/` + `refs.bib`; `NUMBERS.md` (every number with its file); `CLAIMS_LEDGER.md`;
`CLAIM_CHECKLIST.md` (30 satisfied, 12 gap on 2026-09-24); `atlas/model.json` and `dataset.json` (RSNA ATLAS cards;
`model.json` still prints the superseded 96.3 / 37.9 zero-shot and 98.2 % CV rows, `RESULTS_CATALOG.md` A2.9: fix
before submission); `LEVELCHECK_MODEL.md` and `paper2_levelcheck/` (the frozen comparator and the reader protocol;
never edit); `results/` (1.5 GB: `power/power.json`, `power_table.json`, `eval_gate/{EVALUATORS,EVAL_LEAKS,LINEAGE,
VERIFY}.md`, `indomain/INDOMAIN.md` §8 collection guidance, `coverage/`, `cine/tracker_config.json`,
`dc_P_pooled_scores.json`, `a1`-`a9.json`, `RIGOR_FIXES.md`, `DATA_CONTRIBUTION.md`; `eval_gate/touched.json` is 55 MB
and reference-only); `figures/` (210 MB; PNG/PDF with caption and record sidecars; the `.tif` files are 3.5-39 MB each
and regenerable); `packet_build/` (253 MB; the 2026-09-27 camera-ready and review PDFs are the latest, 12.6 MB each;
17 earlier packets superseded; `reference.docx` carries an uncommitted edit); `packet_src/persons_available_2026-09-24.json`
(the 7 at-risk persons with a frame). Lost if dropped: the manuscript and every traceable number behind it.

### 4.4 `ssn:paper/qi_universal_protocol/` (the QI protocol manuscript, 2026-09-22, 9 pages)
"The Universal Protocol with a level in it: site marking and time-out for spine surgery assisted by a fluoroscopic
level map: evidence, and a quality-improvement protocol", target The Joint Commission Journal on Quality and Patient
Safety, SQUIRE 2.0, about 2,400 words, two tables; draft, never submitted; affiliation line reads "Department of
Neurosurgery" (wrong); the sweep and the persistent digital fiducial are invention aspects, so private until filing;
the "17 ms per frame" and "about fifteen minutes of fluoroscopic counting" sentences are unverified
(`HANDOFF/MANUSCRIPTS.md` §5). Copy `main.tex`, `main.pdf`, `build.sh`; its bibliography is `../rsnai/refs.bib`.
This is the hospital process-measurement protocol: the per-case form (anchor, exposures, minutes, dose, needles,
disagreement, confidence, level reached, transitional anatomy) is the reader-protocol scaffold S5 and S8 need.

### 4.5 `ssn:HANDOFF/` (2026-10-08, tracked at 097933a except `GREG_ONLY/`)
`RESULTS_CATALOG.md` Parts A, B, E (every quoted number with status), `RESEARCH_DIRECTIONS.md` §2 (the anomaly-aware
fluoroscopy classifier: what was tried, the design, the first experiment, the stop rule) and §6 (the ranked list),
`OPEN_QUESTIONS.md` (A5, A18, C1, C10, C12-C14, E1, F3), `RECIPES.md` §6-7, `DATASET_USAGE.md`, `LEAKAGE.md`,
`INFRASTRUCTURE.md` §6, `MANUSCRIPTS.md` §2-5, §15-17, `literature_state/power.md` (the full power inventory, with
`power_calc.py`), `context/` (the redacted memory notes with statuses in `INDEX.md`). `GREG_ONLY/` holds credential
locations, personal data and the commercial stance: excluded from the seed. Lost if dropped: the only
cross-checked map of what is quotable.

### 4.6 The memory notes
The eight named notes plus the related C-arm notes are copied from `HANDOFF/context/` with the `INDEX.md` statuses:
CURRENT: `level-service-serving`, `k-devices-one-network`, `pooled-vs-lodo-device-designs`,
`carm-plateau-is-the-denominator`, `detection-is-the-binding-constraint`, `carmlspine-level-experiment`,
`sweep-map-replaces-registration`, `oblique-angles-and-sweep-vision`, `acquisition-space-saturation`,
`lstv-tltv-detection-goal`, `registration-free-prior-art`, `film-fluoro-boundary-not-transferable`,
`paper-split-2026-09-24`, `schwingnet-manuscript`, `fluorocap-repo-private`, `model-registry`,
`learned-formation-refuted-calibrate-instead` (redacted copy only; the live note carries a staff contact's details),
`pacs-demo-and-ostk-params`; DATED: `guided-acquisition-loop`, `flagship-program`, `engine-swap-architecture`,
`rsnai-paper-endpoint`, `rigor-audit-findings`, `level-model-bank-coverage`, `recurrent-head-restored-2026-09-16`;
PARTLY SUPERSEDED: `flagship-paper-frame`, `six-figure-paper-plan`, `figure-preferences-schwingnet`; SUPERSEDED
numbers: `two-mechanisms-thesis` (its 98.2 / 72.9 / 44.9 are v2 lineage; current 97.4 and 74.8 per A3.1, A3.3);
LEAKED: `mixed-length-head-and-sota`, `selective-prediction-the-honest-99`, `remedies-refuted-2026-09-17`; RECORD ONLY
[LEAK]: `feasibility-claims-measured`, `level-id-2d-results-2026-09-13`. Greg-only, not copied: `commercialization-stance`,
`schwingnet-disclosure-scrub`, the three credential notes.

### 4.7 The regulatory documents
`ctsp:2026 269 Schwing IRB Not HPR Determination 9.2.26.pdf` (670,187 B; its twin `2026_269 ...` is byte-identical in
size, a duplicate); `ctsp:IRB Not HPR Determination 4.21.26.pdf` (2,088,991 B; HPR 2026-144; the tool inside lists
Orthopedic Surgery and a chair as sponsor, and Greg's phone: redact); `ctsp:OSC_HPR_Determination_public_datasets.pdf`
(556,822 B; the tool as filed 2026-08-28; byte-identical in size to `IRB_VinDr_2026-09-25/03_HPR_tool_as_filed_2026-08-28.pdf`);
`ctsp:IRB_VinDr_2026-09-25/` (cover note md and docx, the filled tool, the 2026-269 memo, the tool as filed; the `.zip`
beside it is a duplicate); `ctsp:hpr_determination_tool_revised_11_2021.pdf` and
`ctsp:hpr-guidance-activities-that-are-not-hpr-ada-update-4726.docx` (WSU forms); `ctsp:proposals/irb/` (gitignored:
`PROTOCOL_1_eProtocol_draft_2026-09-15.md`, `IRB_two_protocols_summary.pdf/.docx`; the draft names DMC/WSU staff with
work e-mail addresses, which `IRB_ADDENDUM.md` itself says to remove: copy with roles kept and addresses cut);
`ctsp:proposals/FluoroCap_HPR_attachment.md`; `Desktop/IRB/spine_study_protocol.{docx,pdf}` and
`Data_Collection_Tool.{docx,pdf}` (March 2026); the DMC process PDFs and the WSU IRB FAQ and CITI pages in
`Desktop/IRB/`; `Desktop/x-ray_machine_registration_form.doc` (WSU OEHS "NEW Radiation Machine Registration Form";
its document metadata names two staff: strip). Not copied: `ctsp:[faculty-surname]_IRB.pdf` and `Desktop/IRB/Retrospective IRB
PROTOCOL.pdf` (other investigators' protocols used as format templates), `ctsp:IRB_ADDENDUM.md` and
`ctsp:COMMERCIALIZATION.md` (Greg-only; reference by path), `Desktop/IRB/co-investigators.xlsx`, `GREG/`, `HAZEM/`
(personal), `ctsp:IRB_2024 Tenet Resident Benefits Guide.pdf`, `ctsp:IRB_IndContract_GSchwing_24926.pdf` (personal and
administrative, not research).

### 4.8 Other laptop folders bearing on this path
`C:/Users/grego/OneDrive/Desktop/spine-detector/`: the local folder is **not a git clone** (`git log` fails;
listing 2026-10-08); the memory note says private GitHub `OpenSpineConsortium/spine-detector` and grid
`HOME/spine-detector` (`HANDOFF/context/xray-corner-detector-status.md`); `src/manifest.py::canonical_slots` fixes the
corner slot order a runtime must respect (`CINE_DEMO_RECON` reader 0 §4), `src/normalize.py::detect_facing` has a
code/docstring disagreement; `dist/` holds the superseded detect_v3/v4 ONNX exports (42-84 MB each; the website
copies were removed 2026-09-14). `C:/Users/grego/OneDrive/Desktop/openspineconsortium.github.io/pacs/` (public,
master c1800f8 2026-10-02): `remote.js` is the client of the service contract. `ctsp:C-Arm Validation Research
Plan.pdf` (279,029 B, 2026-09-20): an externally generated 13-page roadmap, reference only; its usable content is the
frame-grabber architecture, the veterinary C-arm lab and cadaver routes, and the 16 mm manual repositioning error
against the 21 mm search half-width. `ctsp:Feasibility_FOV.docx` and `MULTI_XR.docx`: external reports whose claims
were tested and partly overturned (`HANDOFF/context/feasibility-claims-measured.md`); reference only.
`Desktop/FluoroCap_reading/`, `FluoroCap_screening/`: review pages for the FluoroCap test set (dropped from training).

### 4.9 The grid (verified by `ls` 2026-10-08 unless stated)
Weights: §1.1 table. Real-frame data: `CEPH/data/realxray/` holds `carmlspine` (299 frames, 149 cases, splits
train 106 / val 15 / test 28, boxes per level L1 267 ... sacrum 295, T12 63, T11 3; `summary.json`),
`carmlspine_sweep`, `carmlspine_cv*`, `carmlspine_pre_repair_2026-09-23*`, `cobra_elekta` and `_v2/_v3/_ap45/_g3test/_smoke`,
`deepfluoro`, `geneva_hip`, `bournemouth_qf/raw` only, `pelvis_landmarks`, `view_census.json`. Results:
`CEPH/data/or_ready/` (devices with eight cards, `lodo/`, `audit/`, `eval_gate/`, `indomain/`, `lcurve/`, `arc/`,
`coverage/`, `crossdev/`, `devlodo/`, `devpool/`, `fig3_detection*`, `fig4_pairs*`, `film_ncurve/`, `learning*`;
no `cine/`). Device corpus: `CEPH/data/devcorpus/{lists,poses,render,styled}`. Public clips:
`CEPH/data/external/fluoro_video/`. Paper 2 gate: `CEPH/data/fig6/` with `HOLD_README.txt`. COBRA: `CEPH/data/cobra2026/`
(692 of 692 cases, 771 GB per `DATASET_USAGE.md` §2.3). Bench: `HOME/bench/latency.json`, `runtime_cost_workstation.json`,
`fig_runtime_workstation.{png,pdf}`; no `runtime_cost.json`. Guided loop: `HOME/model_night/guided/*`, `HOME/model_night/fiducial/*`
(not opened). Queue: 7 jobs of go2432 at the time of the check (`squeue -u go2432 -h | wc -l`). Migration: the
`~/carm_*` banks are batch B10 to `CEPH/data/carmlspine/derived/` (`ssn:data_platform/LAYOUT.md` L306-324), FluoroCap
is B09, `~/spine-detector/data/*` is B04 (L248-263, L291-300); whether B10 has run is not recorded in the files read
here (per-batch truth is `plan/runs/<B>/STATUS` on the grid, `HANDOFF/README.md` §3). The private weights repo
`gregoryschwingmdphd/level-id-weights` was not checked (no network).

## 5. Unknowns

1. The hospital's C-arm make, model and software version: not recorded in any file.
2. Whether the hospital C-arm's exposures reach PACS, and as which object class (XA, RF, Secondary Capture), or stay
   in the device archive: the Protocol 1 draft asks Radiology; no answer on disk.
3. The end-to-end latency of the reported stack on uncontended, named hardware: not measured.
4. Whether any DMC protocol (Protocol 1, 2, 3 or the March 2026 multimodal draft) was submitted: not recorded.
5. The VinDr-SpineXR HPR determination number and date: not recorded (`OPEN_QUESTIONS.md` A5).
6. The identity of the stage-2 clinical reader "Dr Tech" and the full name of the Neurosurgery co-investigator
   (two spellings): not recorded; confirm before any protocol is filed.
7. Whether the 148 C-ArmLSpine cases are 148 people (`OPEN_QUESTIONS.md` E1).
8. Whether the guided-loop corpus arms (`HOME/model_night/guided/*`) ever produced a `guided.json`, and whether the
   `frame` control read near 85 %: not opened here; the last record says nothing is quotable.
9. Whether migration batch B10 (the `~/carm_*` banks) has run: read `plan/runs/B10/STATUS` on the grid.
10. The live state of the private weights repo and of `level-id.openspineconsortium.org`: no network used.
11. The person-level intraclass correlation for transitional endpoints, needed for any two-proportion power
    (`OPEN_QUESTIONS.md` C10).
12. The body of the 2026-269 memo itself (scanned, no text layer; the cover note of 2026-09-25 quotes its title,
    number and date).

## 6. Flags for the seed builder

- `ssn:tools/cine_eval.py`, `tools/cine_latency.py`, `tools/fluoro_video/` and `sn:results/cine/` are untracked at
  097933a: copy them into the project's `code/` with the path and the date, or they exist on one laptop only.
- `ssn:tools/level_prototype.py`, `carmlspine_eval.py`, `patient_keys.py`, `pipeline_state.py`, `test_patient_keys.py`
  have uncommitted edits; `SchwingNet/packet_build/reference.docx` and `reference_single.docx` too.
- `C:/Users/grego/OneDrive/Desktop/spine-detector/` has no `.git`; the commit the ONNX exports came from is unknown.
- The service serves an older release than the paper reports; a reader who deploys `service/` as is will ship
  `detect_v5z_epoch25` + M19 and no abstain flag.
- Contact data to redact on copy: the request drafts, the VinDr draft and cover note (phone), the HPR 2026-144 tool
  (phone), the Protocol 1 draft (staff e-mails), the X-ray registration form metadata (two staff names), the full
  `learned-formation-refuted-calibrate-instead.md` (use the redacted copy).
- Private, never student-facing: `COMMERCIALIZATION.md`, `IRB_ADDENDUM.md`, `INVENTION_DISCLOSURE.md`,
  `DISCLOSURE_MEMO.md`, `provisional/`, `GUIDED_ACQUISITION.md`, `SWEEP_PROTOCOL.md`, `CARM_DEPLOYMENT_EVIDENCE.md`,
  the QI manuscript (sweep and fiducial), `paper/focused/main.tex` (`HANDOFF/MANUSCRIPTS.md` §4, §15, §17).
- The QI manuscript and `paper/rsnai/main_v2.tex` carry the wrong affiliation (Neurosurgery); every copy must say
  General Surgery (`OPEN_QUESTIONS.md` A14).
- Three stale numbers still print in files that look authoritative: `sn:tables/tab3_naming.md` and the three
  `atlas/model.json` copies (A2.9, A3.11); the "17 ms per frame" in the QI manuscript (no file).
- `sn:tools/fig6_score.py` reads the wrong path (`T1/blinded/meta_ref/`); the open gate's reference score was never
  written (`RESULTS_CATALOG.md` B.5; `OPEN_QUESTIONS.md` F3).
