# Adversarial verification of the s15 detector resubmission (read-only)

Verified 2026-09-24 21:27-21:35 UTC (17:27-17:35 EDT) from the grid login node (`scontrol`, `squeue`, `sacct`,
`ls`, `cat`, `grep`, `sha256sum`, `git rev-parse`/`merge-base` in `~/spinesurg-ct-nnunet`) and from the local tree
at `[repo:spinesurg-ct-nnunet]` (branch `L6_Class`, HEAD `f9e52d10a634...`, dirty).
Nothing was submitted, released, written or deleted on the grid. No model ran. The eight `val_*.json` and
`POST.json` were copied to a local scratch directory to recompute the numbers.

Verdict: **all five items PASS**. One condition outside the five items must be met before the blinded gate is
released (section 9 ancestry of the recorded HEAD), stated under "Release" below.

## (1) The held jobs' stored script uses det_g3_primary_s0 as primary and the LODO detectors only as a secondary variant -- PASS

- `scontrol write batch_script 40438004 -` and `... 40438005 -`: identical (diff empty), 231 lines, sha256
  `5eae5ea22c3eb7fe99af29a4dc33c5bf1d94a5e98fcc06f4c6b9ddeca91667ba` = the deployed
  `~/spinesurg-ct-nnunet/SchwingNet/slurm/fig6_eval.sh` = the local file with CRLF stripped = the sha256 written in
  `G5_MANIFEST.json` (`scripts_sha256`) and `EVAL_SUBMITTED.json`.
- In that stored script: `DET_G3=$H/spine-detector/runs/g3/det_g3_primary_s0/weights/best.pt` with
  `DET_G3_SHA=fe00a173...` checked against `sha256sum` at start (`DETECTOR_MISMATCH` exit 5 otherwise);
  `BODY_CONF=0.25`; the `det` variant passes `--box-detector $DET_G3 --box-conf $BODY_CONF` to the prototype (line
  180) and the coupler runs it at `--sacrum-min-conf 0.74` (det74) and `0.25` (det25) (lines 205-206). The LODO
  sacrum detectors `rx_lodo_cobra_elekta_1024` / `rx_lodo_carmlspine_1024` appear only as `SAC_T2`/`SAC_T3` and
  are passed only in the `lodo` variant (`--sacrum-detector $SAC`, line 181), whose outputs go to `det74_lodo/` and
  `det25_lodo/` (`SFX=_lodo`, line 199). The keypoint detector `detect_v5z_final_best.pt` is loaded and gated but
  supplies bodies only in `lodo`. Every set runs `det`, `lodo`, `oracle` for the primary head; secondary heads run
  the set's primary variant (lines 213-219).
- The manifest gate in the script (lines 94-101) asserts `primary.detector.sha256 == fe00a173...`,
  `primary.detector.body_boxes.conf == 0.25` and `primary.detector.sacrum_anchor_min_conf_primary == 0.74`. Replayed
  against the local `G5_MANIFEST.json`: all three hold (it would print `manifest names detector fe00a1732032 body
  conf 0.25 commit None`). The grid copies of the manifest are byte-identical to the local file (sha256
  `4104ed2d...` at both `~/spinesurg-ct-nnunet/SchwingNet/results/fig6/` and `/rs/rs_grp_oschome/go2432/data/fig6/`).
- The grid `tools/level_prototype.py` has `--box-detector` (line 145), `--box-conf` (148, default 0.25),
  `--sacrum-detector` (157); the grid `tools/alphabet_couple.py` has `--sacrum-from-meta`, `--truth-variant`,
  `--sacrum-min-conf`, `--dedupe-boxes`; the grid `tools/eval_gate.py` is `eval_gate/1`. Every file the script
  requires at start exists: encoder, primary head, both detectors, both LODO detectors, `sets_v2/READY`,
  `frozen_v1/strata.json` (sha256 `c7199d2d...` = manifest), `~/mambaforge/envs/fluorogen/bin/python`,
  `SchwingNet/tools/fig6_truth_join.py` (sha256 `a584f809...` = manifest), `SchwingNet/tools/fig6_score.py`
  (`f57bcd48...` = manifest), the three frozen reference files (below).

## (2) The new jobs are HELD and 40431765/66 are gone -- PASS

- `scontrol show job`: 40438004 `JobName=f6eval JobState=PENDING Reason=JobHeldUser Priority=0 Dependency=(null)`,
  submitted 2026-09-24T17:23:34, `--export` gate open; 40438005 `PENDING Reason=JobHeldUser Priority=0
  Dependency=afterany:40438004(unfulfilled)`, same submit time. Both `-D ~/spinesurg-ct-nnunet`, partition
  `gmsap,gvohp,galhp`, QOS gpu, 8 CPU, 12 h. `squeue -u go2432` lists exactly these two `f6eval` rows, both
  `JobHeldUser`.
- 40431765 and 40431766: `scontrol show job` -> `Invalid job id specified`; `sacct` ->
  `CANCELLED by 7152432` at 2026-09-24T17:23:31, `Start=None`, `Elapsed=00:00:00`, `NodeList=None assigned`. They
  never started.

## (3) unblinding/ is empty and no eval-type job ran on a test frame today -- PASS

- `/rs/rs_grp_oschome/go2432/data/fig6/unblinding/`: `total 0`, directory mtime Sep 23 20:28, no entries.
- No `eval_v2*` root exists under `/rs/rs_grp_oschome/go2432/data/fig6/` (`ls -d .../eval*` -> no such file); no
  `RUN_CONFIG_*`, `AUTO_REFERENCE_USED_*` or `UNBLINDING.json` anywhere under fig6.
- `sacct -u go2432 -S 2026-09-24T00:00 -X`, every job name today, filtered on `f6eval|fig6|score|eval|proto|couple|blind`:
  one `f6eval` (40427984, FAILED, 04:25:46-04:25:48, 2 s, node voh7), two `eval_gate`, six `eval_leaks*`, one
  `gate_evalsets`; no name matching `fig6` or `score`. The `f6eval` log (`~/logs/f6eval-40427984.out`, 141 bytes)
  is two lines: `F6EVAL_START gate=open V=v1 voh7 2026-09-24T08:25:48Z` then
  `MISSING /rs/rs_grp_oschome/go2432/data/fig6/bank_g3_v1/runs/model_rung_1_ft_g3_aug2.pt` -- it exited at the
  file-existence check before any model or frame was loaded. `eval_gate`, `gate_evalsets`, `f6gate` (40436274,
  40436579) and `f6keytest` (40436051) logs are key/overlap checks over person lists (`HELD OUT ... overlap 0` per
  set; no image path, no model output). Nothing today read a G3 test frame with a SchwingNet model.
- The HOLD_README.txt at the fig6 root still names the earlier held job 40429882; it is stale text, not a live job
  (40429882 is not in the queue), and does not affect the chain.

## (4) G5_MANIFEST.json sha256s match the files -- PASS

| manifest entry | manifest sha256 | file on disk | match |
|---|---|---|---|
| `primary.detector.path` `~/spine-detector/runs/g3/det_g3_primary_s0/weights/best.pt` (40,600,101 B) | `fe00a173...8652f92f` | grid `sha256sum` | yes |
| `primary.detector.registry.store_path` `~/model_registry/fe00a1732032e81a/best.pt` | same | grid | yes |
| `frozen_reference_sha256.auto_reference.json` | `57782cad...a3d04229` | local file and grid `~/spinesurg-ct-nnunet/SchwingNet/results/fig6/frozen/` | yes (both) |
| `frozen_reference_sha256.auto_truth.csv` | `aa306deb...df7321d` | local and grid | yes (both) |
| `auto_reference.sha256_file_sha256` | `52797eef...42258ce7d` | local and grid | yes; the file's own two lines carry the two digests above |
| `strata.json (frozen_v1)` | `c7199d2d...4d13e50` | grid `/rs/.../fig6/frozen_v1/strata.json` | yes |
| `primary.encoder` `bank_g3_v2/runs/model_rung_1_g3clean_aug2.pt` | `629f0e05...` | grid | yes |
| `primary.head` `heads_v2/head_fig6_g3clean_lam0_seed0.pt` | `5e1e4c3b...` | grid | yes |
| `keypoint_detector_still_loaded` `FluoroCap/detect_v5z_final_best.pt` | `797de71a...` | grid | yes |
| LODO `rx_lodo_carmlspine_1024` / `rx_lodo_cobra_elekta_1024` | `f6fe6b97...` / `65fc01de...` | grid | yes |
| `detector_exclusions.json` | `5277d17b...` | grid | yes |
| `scripts_sha256` (fig6_eval.sh, fig6_score.py, fig6_truth_join.py) | as above | grid deployed copies and local LF | yes |

`POST.json` independently records `sha256 fe00a173...`, `split_sha256 65a57eb0...` (= manifest `split_final.json`),
registry parents `["public:ultralytics/yolo11m.pt"]`, `eval_gate_test_persons.overlap 0`, `pose_donor_overlap 0`.
Note that `/rs/rs_grp_oschome/go2432/data/fig6/frozen/` does not exist; the script's `RES/frozen` points at the
home-directory copy, which is the one that exists and matches.

## (5) DETECTOR_G3_VALIDATION.md numbers re-derive from the val json k/n -- PASS

Recomputed from the per-frame records of each `val_<root>_g3body_c{0.25,0.74}.json` (`sum det["0"].tp / sum
det["0"].truth` for vertebra, class 1 for sacrum, frames = list length, persons = distinct `case`), and, as an
independent check, re-matched greedily from the `raw` detections against the `truth` boxes at IoU >= 0.5 with the
file's confidence floor:

| root | conf | frames / persons | vertebra k/n (sum) | vertebra (IoU rematch) | sacrum k/n (sum) | sacrum (rematch) | sacrum found | md row |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| carmlspine_g3body | 0.25 | 20 / 10 | 87/100 | 87 | 18/20 | 18 | 18 | same |
| carmlspine_g3body | 0.74 | 20 / 10 | 84/100 | 84 | 18/20 | 18 | 18 | same |
| cobra_elekta_g3body | 0.25 | 216 / 9 | 284/303 | 284 | 205/206 | 205 | 205 | same |
| cobra_elekta_g3body | 0.74 | 216 / 9 | 250/303 | 250 | 199/206 | 199 | 199 | same |
| cobra_elekta_v3_g3body | 0.25 | 216 / 9 | 283/303 | 283 | 206/206 | 206 | 206 | same |
| cobra_elekta_v3_g3body | 0.74 | 216 / 9 | 248/303 | 248 | 201/206 | 201 | 201 | same |
| deepfluoro_g3body | 0.25 | 105 / 1 | 95/125 | 95 | 101/101 | 101 | 101 | same |
| deepfluoro_g3body | 0.74 | 105 / 1 | 58/125 | 58 | 98/101 | 98 | 98 | same |

C-ArmLSpine by view re-derives too: AP 45/50 and LAT 42/50 at 0.25; AP 43/50 and LAT 41/50 at 0.74. The
percentages in the md (87.0, 84.0, 93.7, 82.5, 93.4, 81.8, 76.0, 46.4; sacrum 90.0, 99.5, 96.6, 100, 97.6, 100,
97.0) are these fractions. Every val json carries `eval_gate.held_out: false` with the stated reason (G3 VALIDATION
persons, overlap 10 / 9 / 1 = the validation persons themselves), and `weights` = the primary detector path. The
validation persons (C-ArmLSpine case114 124 134 138 144 47 65 79 91 92; COBRA A126 A136 B038 B057 C012 C076 C166
D111 D439; DeepFluoro 17-1882) share no key with `sets_v2` T2 (32 open + 75 blinded) or T3 (10 open + 3 blinded),
by a direct set intersection here, independent of POST.json's gate. The local and grid copies of
`DETECTOR_G3_VALIDATION.md` are identical (sha256 `1abffbb937dfe5ceef1387c6ddc4a4f8685c34f35a751008828e5f4881ce3ca7`).

## Release: what the coordinator runs and records (LEVELCHECK_MODEL.md section 9)

**Condition found outside the five items, and it binds the blinded gate.** The grid checkout `~/spinesurg-ct-nnunet`
that both jobs run from (`-D`) is at HEAD `6e1cf8d21b08e238f30fa1d2b9a2672318abef2a` (2026-09-20), 362 commits
behind the local `L6_Class` HEAD, and **does not contain the pre-specification commit
`ecae75f42ce9a2f446feffc8f6df61bb8fca5934`** (`git merge-base --is-ancestor` -> not an ancestor; `git cat-file`
cannot see it). `SchwingNet/`, `tools/alphabet_couple.py` and `tools/eval_gate.py` are untracked there and
`tools/level_prototype.py` is modified; the deployed files were copied, not pulled. The script records
`git rev-parse HEAD` from that checkout at `F6EVAL_START` and in `RUN_CONFIG_<gate>.json`. Section 9: "The G6
evaluator must record the UTC time and `git rev-parse HEAD` at that moment. The commit that adds this file must be
an ancestor of that HEAD and earlier than that time. If it is not, the analysis is reported as not pre-specified."
As it stands the blinded job would record a HEAD of which `ecae75f` is not an ancestor. The open gate (ordinary
persons only) is not unblinding under section 9's definition, but it writes the same record, so the same fix is
worth applying before it too. Locally, `ecae75f` IS an ancestor of `f9e52d1`, and `6e1cf8d` is an ancestor of
`f9e52d1`, so a fast-forward of the grid checkout to the commit that carries the G5 manifest resolves it (the
untracked `SchwingNet/` tree and the two untracked tools will collide with a plain checkout and must be moved aside
or reconciled first; the three deployed fig6 scripts are byte-identical to the local ones, so nothing is lost).
This does not require touching the held jobs: `-D` points at the directory, not a commit.

Sequence, in order:

1. Commit locally (not done by this step): `G5_MANIFEST.json`, `fig6_eval.sh`, `fig6_score.py`,
   `fig6_truth_join.py`, `DETECTOR_G3_VALIDATION.md`, `EVAL_SUBMITTED.json` (and this file). Write the resulting
   40-hex hash into `"commit"` of all three manifest copies (local, `~/spinesurg-ct-nnunet/SchwingNet/results/fig6/`,
   `/rs/rs_grp_oschome/go2432/data/fig6/`). Changing `commit` changes the manifest's sha256; that is expected, the
   job hashes whatever is there at start and the gate checks only the detector fields. Push (`wsl -e bash -lc`).
2. Bring the grid checkout `~/spinesurg-ct-nnunet` to that commit (fetch + checkout/fast-forward of `L6_Class`),
   then confirm on the login node: `git -C ~/spinesurg-ct-nnunet merge-base --is-ancestor ecae75f42ce9a2f446feffc8f6df61bb8fca5934 HEAD && echo ok`
   and that `SchwingNet/slurm/fig6_eval.sh` still hashes to `5eae5ea2...` (or to the committed version, if the
   commit changed it -- then re-check the stored batch script is what you want; the stored script is a copy taken
   at submit time and will NOT follow a changed file).
3. Release the open gate:

       scontrol release 40438004

   Record at that moment (in the release note / EVAL_SUBMITTED.json): UTC time of the release, `git rev-parse HEAD`
   of the grid checkout, the manifest commit hash, and the sha256 of `G5_MANIFEST.json` as released.
   `RUN_CONFIG_open.json` and `AUTO_REFERENCE_USED_open.json` under `/rs/rs_grp_oschome/go2432/data/fig6/eval_v2_g3/`
   will hold the job's own record; check that its `git_head` descends from the manifest commit and that
   `truth_join_open.json` reports the expected assignment counts before going further.
4. Decide and freeze the human truth (`SchwingNet/results/fig6/verification/truth_frozen.csv` + `.sha256`, via
   `tools/verification_pages.py freeze`), copy both to `~/spinesurg-ct-nnunet/SchwingNet/results/fig6/verification/`
   on the grid (the directory does not exist there yet). Without it the blinded run scores every transitional
   stratum as empty under the reference standard and T3 only under the labelled harvest names, as the resubmission
   stated; the script will refuse a `truth_frozen.csv` that arrives without its `.sha256` (exit 8).
5. Write `/rs/rs_grp_oschome/go2432/data/fig6/unblinding/RELEASE_v2.json` with exactly:
   `g5_manifest_commit` (the 40-hex hash from step 1), `truth_file` (absolute path of the truth file the blinded
   run will use: `truth_frozen.csv` if frozen, else `.../frozen/auto_truth.csv`), `truth_sha256` (its sha256; the
   job recomputes and refuses on mismatch), `prespec_commit_is_ancestor: true` (only after step 2 proves it),
   `released_by`, and (not checked by the job but required by section 9) `released_utc` and `git_head` of the grid
   checkout. Then, and only then:

       scontrol release 40438005

   The job writes `eval_v2_g3/UNBLINDING.json` (`unblinded_utc`, `slurm_job`, `node`, the release record,
   `truth_sha256_checked`) before the first model runs; that file plus `RUN_CONFIG_blinded.json` is the section 9
   record. The `afterany:40438004` dependency means the blinded job also waits for the open job to finish, whatever
   its exit state, so it will not start early once released; releasing it before RELEASE_v2.json exists would make
   it exit 6 (`UNBLINDING_REFUSED`) after the open job ends, which consumes the job.

Nothing is to be released on the strength of this note alone; item 1 of the pending list (commit + manifest
`commit` field) and the grid-checkout ancestry above come first.

Observations that are not failures: `sets_v2` T2 holds 107 persons (32 + 75), whereas the resubmission text and
POST.json speak of 159 T2 persons in the G3 test stratum; the 159 is the eval-gate person count, the 107 the
persons with exported real kV frames. The COBRA v1-window validation frames are not in `val.txt` (which carries the
v3 window only, 216 of its 341 entries); they are the same 216 frames of the same nine validation persons under
another export window, as the validation note says. The grid `tools/eval_gate.py` is `eval_gate/1` while the local
tree has `/2`; the resubmission recorded this as its owner's to deploy.
