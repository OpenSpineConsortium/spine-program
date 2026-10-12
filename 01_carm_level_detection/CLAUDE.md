# 01 C-arm level detection: working context

Project 01 of the spine programme (`../_plan/PLAN.md` section 3, rank 1; reader Greg-only). Built 2026-10-08.
Hospital = Wayne State University School of Medicine / Detroit Medical Center, Department of General Surgery.
Never Neurosurgery: four superseded manuscript drafts and one data-request placeholder in this folder say Neurosurgery; `MANIFEST_LOCAL.md` section 3 names each.

## The goal in one paragraph

Take the reported SchwingNet stack (naming detector `detector_v5z_final`, sacrum and vertebra detector
`rx_lodo_carmlspine_1024`, level encoder `allspine_v9` rung 1, the BiGRU head, the count from the detected sacrum, the
alphabet coupling and the stop signal; `docs/handoff/DATASET_USAGE.md` section 1) from four weight files on the grid and a
container that serves an older release (`code/service/`) to a frozen, registered, latency-measured runtime whose output has
been read by humans against a pre-registered endpoint on exposures from the C-arm actually used at the hospital, under an
approved protocol, with the device census, the capture adapter, the reader protocol, the PREREG and the sample size written
before the first frame is scored. The one number worth repeating today: 595 of 617 lateral vertebrae named exactly on a
C-arm the model never saw (96.4 %, Wilson on effective n [92.3, 98.4]; `docs/handoff/RESULTS_CATALOG.md` A2.1;
`results/schwingnet/eval_gate/leaks/zeroshot_v9.json`). What is missing is in `TODO.md`, in order, with gates.

## Read first

1. `README.md` (state on 2026-10-08, success criteria), `STATUS.md` (every number in hand with its rigor mark),
   `TODO.md` (S0 to S10, then the open questions and directions).
2. `docs/MODEL_CARD.md` (the model as it stands; section 6 is the runtime, section 5.1 the truth; "What this card asks
   for next" is S0).
3. `docs/CINE_DEMO_RECON_2026-09-26.md` reader 0 (the exact `level_prototype.py` command, the sbatch pattern, the
   input conventions and what the service does not serve).
4. `docs/handoff/README.md` section 5 (the ten house rules), `docs/handoff/RECIPES.md` section 0 (how work reaches the
   grid and comes back), `docs/handoff/RESULTS_CATALOG.md` "How to read a row" and Part A.
5. `MANIFEST_GRID.md` (every grid path with its verification state) and `MANIFEST_CODE.md` (every repository, commit
   and the files that matter). Nothing in this folder depends on a laptop path; `MANIFEST_LOCAL.md` records where each
   copy came from as history only.

## Where things are

- **This folder.** `code/` (the service, the 19 pipeline scripts, the untracked cine tools, the fluoro_video panel cutter,
  the spine-detector source snapshot, the handoff builders), `docs/` (the model card, deployment evidence, the sweep and
  guided-acquisition documents marked PRIVATE, prior art, the input specification, the data-request drafts, `handoff/`
  with the whole 2026-10-08 handoff except `GREG_ONLY/`, `research/`, `external_reports/`, `grid_records/`), `results/`
  (`schwingnet/` with every paper-1 result file, `physics/`, the v2-lineage C-ArmLSpine scores kept as a record),
  `figures/`, `manuscripts/` (`schwingnet/` paper 1 with its ledgers and the two 2026-09-27 packets; `superseded/`
  earlier drafts; `talks/` the private CNS deck v10), `regulatory/` (HPR 2026-144, HPR 2026-269 with the filled tools,
  the VinDr follow-up, Protocol 1 to 3 drafts and the addendum, the March 2026 protocol, WSU and DMC forms, the C-arm
  validation plan's paperwork, the DUA advisory text), `memory/` (78 notes with their statuses: 22 standing-rule, 46 of the
  C-arm cut list, 10 added for this project, `MEMORY.md` section 3; `MEMORY.md` is the index).
- **The grid.** HOME `/wsu/home/go/go24/go2432` and Ceph `/rs/rs_grp_oschome/go2432`, spelled in full in
  `MANIFEST_GRID.md`. The four weight files of the stack, the fold models, the registry (`HOME/model_registry`), the
  real-frame banks (`/rs/rs_grp_oschome/go2432/data/realxray`), C-ArmLSpine (`/rs/rs_grp_oschome/go2432/data/carmlspine`),
  the OR-readiness result tree (`/rs/rs_grp_oschome/go2432/data/or_ready`), the bench records (`HOME/bench`), the private
  repository checkout (`HOME/spinesurg-ct-nnunet`, at 4e3fe93, behind the laptop and unable to fetch).
- **Repositories.** `spinesurg-ct-nnunet` (private, branch `L6_Class`, commit 097933a; every tool and job script);
  `OpenSpineConsortium/spine-detector` (private; the grid tree `HOME/spine-detector` has `.git`); `CTSpinoPelvic1K`
  (public, `master`, 7ddfe38); `OpenSpineToolkit` (public, `main`, cb43197); `XRSpinoPelvic1K` (private, `main`, 4f22935);
  `openspineconsortium.github.io` (public, `master`, c1800f8; `pacs/remote.js` is the service client); the private
  Hugging Face weights repository `gregoryschwingmdphd/level-id-weights`. Details in `MANIFEST_CODE.md`.

## The standing rules, in this project's words

- **Words and numbers.** The French-derived word for where data came from is never written; say origin, lineage, source
  or where it came from. No fractional version numbers. Figure captions at most 60 words; the argument goes in the text.
  Plain sentences. Every number carries the file it came from; what no file records is written "not recorded".
- **Check outside the computation.** The recurring failure in this programme is a number that is wrong but plausible:
  three estimators produced finite values from the wrong bone, surface or label map and none raised; the PI = SS + PT
  identity held through a 9 degree error. So compare against published values, an independent implementation, the shape
  of the distribution (the spread, not the median), a published prevalence; and render the mask or the frame and look.
  The 160 of 366 DeepFluoro frames stored upside down and the round-0 white-slab renders were found by looking, not by a
  printed number (`memory/learned-formation-refuted-calibrate-instead.md`).
- **CT labels, where this project touches them** (the C-ArmLSpine CBCT truth and any CTSpinoPelvic1K render): two label
  schemes exist and mixing them does not raise; call `ostk.labels.labels_for(volume)` and never import a fixed map.
  Identifier 29 is retired in v11 and code that gates on it goes with it. Case ids are zero-padded (`zfill(4)`).
  Canonicalise to RAS to analyse; never reorient a label when writing it.
- **Held out means held out.** A person was never seen by the checkpoint or any ancestor; every quoted score goes through
  the evaluation gate (`code/eval_gate.py`, `results/schwingnet/eval_gate/`); the leaked banks (allspine v2, v6, v7, v8 for
  VerSe, `anchor_drr`, `vindrps`) are never quoted. The un-suffixed C-ArmLSpine fold models (`ft_cv{k}_aug2.pt`,
  `head_cv{k}.pt`) start from the deleted v2 bank and the gate refuses them. Pre-register, then score: a number enters a
  manuscript only through a manifest key (`manuscripts/schwingnet/RESULTS_BUILD.md`).
- **The grid.** Nothing runs on the login node (warrior kills python, rsync, md5sum and others by name; no container
  command there; nothing of ours under its `/tmp`). Every computation is an `sbatch` job submitted with `sbatch -D <dir>`;
  chain with `afterany`, never `afterok`; IPC and scratch under `/dev/shm`; large outputs on Ceph, not HOME; the grid runs
  bash 4.2, so test quoting there. Submit, estimate the wall time, write the job ids and the ETA down, stop; do not poll.
  Resume is not reproduce: most arrays skip cells that have a DONE marker.
- **Privacy of the work.** SchwingNet and all level-identification code, text, figures, decks and weights stay private
  (the repository is private since 2026-09-14; the sweep, the digital fiducial and the guided loop are invention aspects;
  paper 1 is held pending the technology-transfer office). The website never serves weights; the service pulls them from
  the private Hugging Face repository with a read token.
- **Data.** Use all of a public dataset; fix or justify every truncation in writing (`docs/handoff/DATASET_USAGE.md`
  section 4). Key patients from DICOM and manifest fields before file names. Network goes through WSL. Tokens are read
  from files only and never echoed or committed. The research track and any commercial track never cross: CTSpine1K
  derivatives, DeepFluoro and COBRA are non-commercial; no weight trained with BUU laterals leaves the grid until Greg has
  read the BUU licence.
- **People.** In the code repositories this folder names, and on Greg's laptop, commit only when Greg asks (then
  directly to the main branch, both remotes where two exist, through WSL); in spine-program itself the account doing
  the work pushes only its claim branch `claude/<issue>` and Greg merges (root `CLAUDE.md` rule 10).
  Ashley Schehr is a person and a published co-author, never a product name. The affiliation is General Surgery (Wayne
  State University School of Medicine / Detroit Medical Center), never Neurosurgery. Student names and usernames,
  researcher e-mail addresses and personal contact details are not written into this repository.

## Traps that bind this project

- **The service is not the reported stack.** `code/service/` serves `detect_v5z_epoch25` + the M19 `films_all2` level
  model, no sacrum detector, no count, no coupling, no abstain flag and no attenuation-and-window conversion. Deploying it
  as it stands ships an older, weaker release (`docs/handoff/context/level-service-serving.md`; TODO S2).
- **No latency of the reported stack exists.** `HOME/bench/latency.json` (2026-09-13) timed older models; the workstation
  run of 2026-09-22 was contended and never timed the detector; the GPU job of `docs/MODEL_CARD.md` section 6.6 was never
  run and `HOME/bench/runtime_cost.json` does not exist (listing 2026-10-08). The QI draft's "17 ms per frame" has no file
  and must not be repeated.
- **The input convention.** Real frames are converted to attenuation, windowed by the field's 1/5/50/95/99th percentiles
  onto 27/47/126/216/239, bone bright, head-up by quarter turns (`docs/REAL_XRAY_DATASETS_SPEC.md`). The models expect
  bone bright; raw fluoroscopy is usually bone dark and `level_prototype.py` does not invert. C-ArmLSpine headers carry
  `PixelSpacing 1.0` as a placeholder (true object-plane pixel 0.1915 mm, detector pitch 0.150 mm;
  `memory/carmlspine-level-experiment.md`). A hospital adapter must reproduce the convention and be rendered and looked at.
- **The truth is automatic.** Every C-ArmLSpine level truth is two CBCT labellers agreeing (814 of 910 bodies); no human
  has read a level on any real intraoperative frame in this programme (`docs/MODEL_CARD.md` section 5.1). Every A-row in
  `STATUS.md` carries [AUTO-TRUTH]. A case is an acquisition, not a known person (`docs/handoff/OPEN_QUESTIONS.md` E1).
- **The detection threshold.** 0.74 is "cross-device", never "pre-stated"; quote it with its curve and the 0.25 point
  beside it (rigor mark [THR]). The pre-stated counting-grade target of 97 % vertebra and sacrum was met by no held-out
  cell (`RESULTS_CATALOG.md` A6.13).
- **Numbers that must not be carried forward.** The 98.22 % v2-lineage cross-validation (still printed in
  `manuscripts/schwingnet/tables/tab3_naming.md` and `atlas/model.json`), the 99 % at 35.7 % coverage, the "100 % sacrum on
  DeepFluoro" (a same-device number), any styled-corpus "design B beats A", the R + C = 22 rule, any guided-loop corpus
  number, the 734x linker speed-up as a timing, CycleGAN / CUT / ADDA / SDXL translation (`../_plan/PLAN.md` section 3,
  01, "Not carried forward").
- **The grid checkout is behind and cannot fetch the private remote.** Ship by `git archive | ssh tar`
  (`docs/handoff/RECIPES.md` section 0 item 2); `make physics`, `make physics-submit` and `make physics-fresh` run
  `git fetch && git reset --hard origin/L6_Class` on the grid and must not be used until fetching works. Five tools carry
  uncommitted edits at 097933a (`level_prototype.py`, `carmlspine_eval.py`, `patient_keys.py`, `pipeline_state.py`,
  `test_patient_keys.py`) and three are untracked (`cine_eval.py`, `cine_latency.py`, `tools/fluoro_video/`): the copies in
  `code/` are the laptop state of 2026-10-08.
- **Two documents in this folder run python on the login node** and must be read with that correction:
  `docs/spinesurg_ct_nnunet_CLAUDE.md` (the `pipeline_state.py` line) and `memory/fluorocap-pipeline-resume.md`. Run them
  as jobs.
- **Only sweep_v3 counts.** Every earlier sweep used the wrong field size (`memory/drr-row-spacing-defect.md`); every
  sweep number uses truth boxes (`docs/MODEL_CARD.md` section 5.5).
- **Case134 headers carry a real PatientID** in `/rs/rs_grp_oschome/go2432/data/carmlspine`: never print a header field.
- **Not verified by any listing:** `HOME/model_night/heads_mixed/` (the folder holding the reported head was not reached
  on 2026-10-08); the fold models have no sha256 in the registry; the live state of the private weights repository and
  of `level-id.openspineconsortium.org` was not checked (no network). `MANIFEST_GRID.md` marks each.

## How to be useful here

The hospital's C-arm make, model and software version are recorded in no file; no capture path from a C-arm exists in
code; no DMC protocol is recorded as submitted; the VinDr determination number is not recorded. When one of these becomes
known, replace "not recorded" with the fact and its source in `README.md` and `MANIFEST_GRID.md`. Say plainly what is not
known rather than guess; the preferred form is `docs/handoff/OPEN_QUESTIONS.md`.
