# 08_render_devices: working context

Image formation for every 2-D model in the programme: the DRR banks, the nine-term device cards, the DeepFluoro
calibration, the styled device corpus, PolyPose morphology augmentation and the record of the refuted
synthetic-to-real routes. Read this file first, then `README.md`, `STATUS.md` and `TODO.md`. Built 2026-10-08
from the spine-program plan (`../_plan/PLAN.md` section 3, project 08) and the handoff of the same day
(`docs/handoff/`, spinesurg-ct-nnunet commit 097933a).

## The goal in one paragraph

Produce, keep honest and hand to projects 01, 02, 05 and 07 the rendered side of the level-identification
work: the physics renders of CTSpinoPelvic1K, VerSe and TotalSegmentator (`physics_drr` 7,045 annotations;
`physics_rare` 1,482 annotations of 81 transitional subjects, the only labelled L6 and T13 at scale;
`docs/handoff/DATASET_USAGE.md` section 3.1), the device cards that turn a render into a frame of a named C-arm
(four on disk in `results/devices/`, two more on the grid), the calibration that replaced learned formation
(exact geometry plus attenuation explains 80.9 % of a real DeepFluoro frame, nine device terms add +4.3 held out;
`docs/DEEPFLUORO_FORMATION.md` section 2 and 5), the styled corpus with its pooled and leave-one-device-out
designs, PolyPose used generatively within published ranges of motion (`results/polypose/`), and the written
record of what was tried and failed (CycleGAN, CUT, ADDA, SDXL img2img: no gain in any arm;
`memory/drr-to-fluoro-levers.md`, `memory/fluorogen-synthetic.md`). The one claim this folder could make on its
own, that a styled synthetic corpus reaches counting-grade detection on a device it never saw, was pre-stated at
97 % and met on none of three devices (`docs/handoff/RESULTS_CATALOG.md` A6.13). As support it is indispensable:
renders raise scarce-N film naming by 6 to 22 points (A10.6, A10.7), they are the only route by which
TotalSegmentator reaches the level bank, and the oblique arc is the only route to angles no real set covers.

## Reader

Greg-only for claiming and hand-outs (`../_plan/PLAN.md` section 3, project 08 "Reader"): the sweep and physics
documents describe invention aspects, the render banks derive from NC-licensed data, and one memory note was
redacted by hand (`memory/learned-formation-refuted-calibrate-instead.md`: two clinicians' names struck, a staff
member and a faculty member named by their roles, a staff contact withheld; `MANIFEST_LOCAL.md` section 3). The whole `spine-program` repository is private; "Greg-only" is about hand-outs. Every Write holder may read this folder, and a student takes an issue here only after Greg hands it out, with a comment naming the student's login or by removing the label `greg-first` (Greg's answer of 2026-10-12, issue #68).

## Where things are

- **This folder.** `docs/` the physics, device and formation records and the research notes; `docs/handoff/` the
  whole 2026-10-08 handoff (catalog, recipes, open questions, directions, literature state, working notes);
  `results/devices/` the fitted cards and the DICOM header census; `results/manifold/` the corpus manifold;
  `results/polypose/` the PolyPose reproduction, sampling spec and cohort files; `figures/` the device parameter
  figures; `memory/` 40 dated notes with their status (index `MEMORY.md`); `MANIFEST_GRID.md`,
  `MANIFEST_CODE.md`, `MANIFEST_LOCAL.md` the three inventories; `STATUS.md` the results in hand; `TODO.md` what
  remains. No code is copied here: every script lives in a repository (`MANIFEST_CODE.md`). The seven inventories
  of 2026-10-08 that the manifests, `MEMORY.md` and `../_plan/PLAN.md` cite by short name (`grid_manifest`,
  `carm_hospital_path`, `memory_and_handoff_map`, `spinesurg_ct_nnunet`, `inventory3_other_spine_folders`,
  `ctsp_repo_root_and_sibling_folders`, `desktop_root_loose_files`, each as `.md` and `.tsv`) are at
  `../_plan/inventories/`; the grid listing and census of 2026-10-08 are in project 10
  (`../10_data_platform_grid/docs/grid_read_2026-10-08/`).
- **The grid.** HOME `/wsu/home/go/go24/go2432` (the single-source render banks, `~/spine-detector/runs/devcorpus`,
  the two TotalSegmentator releases while B07 copies) and Ceph `/rs/rs_grp_oschome/go2432` (`data/versefusion/derived`,
  `data/polypose`, `data/devcorpus`, `data/or_ready/devices*`). Every path, with what it holds, its size where a
  file records one and its migration state, is in `MANIFEST_GRID.md`.
- **The repositories.** `spinesurg-ct-nnunet` (private, branch `L6_Class`, commit 097933a) holds all the tools and
  job scripts named here; `CTSpinoPelvic1K` (public, `master`, 7ddfe38); `OpenSpineToolkit` (public, `main`,
  cb43197); `XRSpinoPelvic1K` (private, `main`, 4f22935). URLs, branches, commits and the files that matter are in
  `MANIFEST_CODE.md`.
- **Prefixes in the copied documents.** The handoff and research records under `docs/` use the prefixes of their
  time: `ssn:` means the spinesurg-ct-nnunet repository at 097933a, `sn:` its `SchwingNet/` folder, `ctsp:` the
  CTSpinoPelvic1K repository at 7ddfe38, `ostk:` OpenSpineToolkit at cb43197, `xrsp:` XRSpinoPelvic1K at 4f22935,
  `context/` or `mem:` a memory note (copied here under `memory/` when it belongs to this project, otherwise listed
  in `docs/handoff/context_INDEX.md`), `~` the grid HOME above, `$RS` the Ceph volume above, `Desktop/` the laptop
  folder that held every checkout on 2026-10-08, `bth:` the Beethoven repository (project 11), `np:` the NextPaper
  folder (projects 03 and 05), `students:` `ctsp:Student_Projects/` (project 11). The full key in its laptop spelling
  is `docs/handoff/README.md` section 0, and every copied handoff file opens with a banner line that points back here.
  A laptop spelling inside a copied document is history, not a dependency; `MANIFEST_LOCAL.md` records where each
  copy came from, and its section 3 names the three result JSONs that keep laptop paths as data.

## The standing rules, in this folder's words

1. **Words.** Never the French-derived word for where data came from; write origin, lineage, source, where it
   came from. No fractional version numbers: a change folds into the next integer version. Figure captions at
   most 60 words; the argument goes in the text. Plain sentences. The affiliation is the Department of General
   Surgery, Wayne State University School of Medicine / Detroit Medical Center, never Neurosurgery. Ashley Schehr
   is a person, never a product name.
2. **Every number carries its file.** A count, a date, a path, a claim names the file it came from. What no file
   records is written "not recorded". An unexplained result is recorded as unexplained, not given a guess.
3. **Check outside the computation.** The recurring failure in this programme is a number that is wrong but
   plausible. Compare with a published value, an independent implementation, the spread of the distribution
   rather than its median, a published prevalence; render the image. In this folder that rule has already paid
   twice: the clipped kVp histogram showed the sampler defect that the numbers hid (`memory/device-sampling-audit.md`),
   and a Dice of 0.000 on an unwarped CT exposed the PolyPose pose convention (`results/polypose/REPRODUCTION.md`).
4. **Labels and orientation.** Two label schemes exist and mixing them does not raise: call
   `ostk.labels.labels_for(volume)`, never import a fixed map. In release v11 identifier 29 (the carved S1) is
   retired and any code that gates on 29 goes with it. Zero-pad case ids with `zfill(4)`. Canonicalise to RAS to
   analyse; never reorient a label when writing it. Renders inherit these rules: a render is made from a labelled
   CT and a wrong map projects wrong boxes without raising.
5. **Held out means the person was never seen.** A render inherits its CT's person. An item is held out for a
   checkpoint only if its patient key is in neither the training nor the validation set of that checkpoint or any
   ancestor. Every quoted score goes through `tools/eval_gate.py` of spinesurg-ct-nnunet. Never quote from the
   leaked banks (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`). `ts_drr` is not held out from the v9
   encoder (`memory/ts-bench-inside-v9-bank` is in project 07; the fact is in `docs/handoff/LEAKAGE.md` section 3).
6. **Pre-register, then score.** Write the rule and its success number before the run; a number produced before
   the freeze is calibration. Manuscript numbers enter through a manifest key, never typed.
7. **The login node runs nothing.** Every render, fit, score and plot is an `sbatch` job; warrior kills python,
   rsync and others by name; no container command on warrior and nothing of ours under its `/tmp`. Use
   `sbatch -D <dir>` (a relative `--output` resolves against the submit directory), `afterany` not `afterok`,
   `/dev/shm` for IPC, Ceph for large outputs, bash 4.2 syntax (a quoted replacement in `${var/pat/"$new"}` keeps
   its quotes). Record a job before cancelling it.
8. **Privacy.** SchwingNet and all level-identification code, text, figures and weights stay private; so do the
   spinesurg-ct-nnunet and XRSpinoPelvic1K repositories. Nothing from this folder goes public until Greg says so.
9. **Data.** Use all of a public dataset; fix or justify in writing every truncation before a rerun; a leaked
   initialisation is fixed by retraining, never disclosed as a caveat; identity comes from metadata first and the
   file name last; FluoroCap is out of training.
10. **Network, tokens, git.** On Greg's laptop, network goes through `wsl -e bash -lc '...'`. Tokens are read from
    files, never echoed, never on a command line or in `sbatch --export`; nothing under the vendor key folder is read.
    In the code repositories this folder names, commit only when Greg asks; in spine-program itself the account doing
    the work pushes only its claim branch `claude/<issue>` and Greg merges (root `CLAUDE.md` rule 10). Write scripts as files and run them by path (heredocs collapse backslashes).

## Traps that bind this project

- **The A-P voxel size was once written as the S-I row spacing.** Every sweep before `sweep_v3` rendered the wrong
  field size; `ctsp_drr` was respaced 2026-09-19; 181 of 374 `verse_soft_drr` renders still carry the defect
  (`memory/drr-row-spacing-defect.md`; `docs/handoff/DATASET_USAGE.md`).
- **Physics-perturbed sweeps once rendered with no bone.** Anything measured under `--perturb physics` before the
  bone-path fix is not quotable; use `make_drr_dataset --paths2-only` (`memory/sweep-physics-no-bone.md`;
  `docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md`). The causal reading of that note is superseded by
  `memory/physics-three-defects-measured.md`: only the AEC extrapolation changed an image.
- **DeepFluoro.** Frames were once converted as a log of a log; the fix is `DF_CONVERSION=linear`, and whether the
  cards were refitted afterwards is not confirmed in any file read (`docs/handoff/RESULTS_CATALOG.md` C4.3;
  `docs/handoff/OPEN_QUESTIONS.md` B9). 160 of 366 frames were stored upside down. The focal length -5257.7 px
  stays signed; the volume is indexed (z, y, x) (`memory/deepfluoro-convention.md`). The H5 release, the vendor
  deposit and the Hugging Face re-host are one dataset in three copies: key by specimen across all three.
- **The exposure clip saturates.** `device_style.SPREAD = 0.2` reaches 1.7 to 5.1 % of each device's joint
  distribution and pins a term on 94.9 to 98.3 % of styled frames; the typicality gate is written and tested but
  the clip is still the default until an A/B on real frames decides (`docs/DEVICE_SPREAD_SWEEP.md`;
  `memory/device-sampling-audit.md`). Gate in normal-score space, never through the quantile table.
- **Cards are written in the grid repository copy.** A refit overwrites `docs/devices/<device>.json` in the grid
  checkout; copy the shipped card aside first (`docs/handoff/RECIPES.md` section 6). The Surgio-B51 and Varian
  Halcyon cards exist only on the grid (`STATUS.md`).
- **`make physics` hard-resets the grid checkout**, which is at 4e3fe93 and cannot fetch; ship by
  `git archive | ssh tar`; only `make physics-tables` is safe (`docs/handoff/RECIPES.md` section 0 and 6).
- **Bank names lie.** `ctsp_drr_obl` and `ctsp_drr_obl2` are VerSe renders under a CTSP prefix; `verse_drr` holds
  13 byte-identical `glgl*` duplicates; `ts_drr`'s path maps were computed from the v3 root; `ts_drr_v3` is read
  by nothing; `anchor_drr`'s own split puts 301 of 801 people on both sides; `vf_813` maps C1 to T9 to ignore, so
  whole-spine work reads the raw VerSeFusion masks (`MANIFEST_GRID.md`; `memory/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md`).
- **Two counts for one bank.** `physics_drr` is 7,045 annotations in `contents.items` and 7,048 in the location
  notes of the same card (`docs/handoff/OPEN_QUESTIONS.md` B12, G1); a listing of `~/physics_drr` settles it.
- **TotalSegmentator's `sacrum` excludes S1**; the whole sacrum is the union (`memory/ts-sacrum-excludes-s1.md`).
  The device corpus calls its source "v2" while the path is v3 (`docs/handoff/OPEN_QUESTIONS.md` F6).
- **Pooled and LODO device designs.** Only design P's list builder refuses a subject on two sides; designs A and B
  do not run that refusal (`docs/handoff/LEAKAGE.md` section 3; OQ C15). Design A renders every card under the
  Cios Fusion pose pool, which includes DeepFluoro test specimen 18-1109.
- **PolyPose's six traps** (`memory/polypose-generator-build.md`): measure through the cohort path
  (`tools/polypose/measure_sagittal.measure_image`, canonical RAS, release plate fits; the old ostk-primitive path
  read PI 3.6 on a case whose truth is 53); the release S1 plate sits in the lowest lumbar footprint; diffdrr's
  `RigidTransform.inverse()` is wrong for voxel affines; cupy cannot take a CUDA bool tensor; grid data files go
  stale silently (sha-compare every synced file; strip CR); every packaged pose needs the diag(-1,-1,1,1) flip or
  the renderer returns zeros (`results/polypose/REPRODUCTION.md`). Fused junctions get zero motion; the pelvis is
  fixed so pelvic incidence is invariant (`memory/polypose-decision.md`).
- **Do not repeat the refuted routes.** CycleGAN and ADDA (parity with no adaptation at 366 real frames), SDXL
  img2img at every strength, CUT v2 (the render-trained model dropped), a learned formation refiner (won on 21 % of
  frames), bespoke CT warps (`memory/drr-to-fluoro-levers.md`, `memory/fluorogen-synthetic.md`,
  `memory/morphology-deformation-feasibility.md`).
- **The synthetic:real ratio was never swept here** (about 1:1 by rows in every cell, `real_share` 0.5) and no
  DRR paper has swept it either (`docs/handoff/RESULTS_CATALOG.md` A10.11; `memory/synthetic-real-ratio-evidence.md`).
  A ratio sentence must say whether it belongs to joint mixing or to pretrain-then-fine-tune.

## How to be useful here

Say plainly what is not known. The honest state of this folder is: the calibration decision stands and its
numbers are a record; the styled corpus did not reach its pre-stated number and the primary criterion was never
tested; the clip defect is known and not repaired; PolyPose is reproduced and not validated. Each of those has a
step with a gate in `TODO.md`. Before any new render arm, read `docs/handoff/RECIPES.md` section 0 (how work
reaches the grid), then section 5 and 6.
