# Build plan: cine evaluation harness, C-ArmLSpine sweep demo, synthetic flexion-extension cine

Nothing was edited, created, committed or submitted. The four reader reports were integrated. I also checked the following myself:

- **Bournemouth `.mat`:** point order, level coverage and event ids.
- **Model choice:**
  - `zeroshot_v9.json` gate block: detector sha `797de71a…`.
  - `slurm/carmlspine_cv_v9init.sh:44` uses head `…mixed_kmax4_seed0.pt`.
  - `level_prototype.py:357-362` discards the corners.
  - `sweep_map.Namer.run` reproduces the prototype's `probs` and `morph` posteriors.
- **CTSP 0533 on the grid:** labels, body mask, repaired CT, and its line in `unseen_v9.txt`.
- **Existing APIs:** `ostk.vertebral_body.endplate_corners_body`, `arc_angle_set._sweep_subject`, and the `eval_gate` and `patient_keys` hooks.

## 0. Decisions that settle conflicts between the readers

- **Head.** The zero-shot head is `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt`: no alphabet loss, and it is what `carmlspine_cv_v9init.sh` pairs with the v9 encoder.
  - The `…alpha0.3_seed{0,1,2}` heads are the CNS count-from-sacrum heads (`sweep_cns.sh`). Don't use them here: there is no sacrum on cervical frames.
- **Primary stack for every arm.** Pass all three weights explicitly; the defaults load `allspine_v2_r1`.
  - `--detector /wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt`
  - `--model ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt`
  - `--head ~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt`
  - Also pass `--no-orient --flag --dump-posterior --conf 0.35`.
  - Keep the histogram match on (the default, `~/films_drr`) and keep flip test-time averaging on. Both are part of the reported pipeline.
- **Corner order.** Never match corners by index.
  - The detector's slots are geometric (`spine-detector/src/manifest.py::canonical_slots`, verified): 0 = superior, smaller x; 1 = superior, larger x; 2 = inferior, larger x; 3 = inferior, smaller x; y points down. `flip_idx [1,0,3,2]` agrees with this.
  - Bournemouth points are anatomical, verified. Index 0/1/2/3 = anterior-superior, anterior-inferior, posterior-inferior, posterior-superior. On all 226/226 L sequences points 0/1 sit left of 2/3; on 25 of 26 R sequences they sit right.
  - So re-sort both truth and prediction through a copy of `canonical_slots`, then compare slot to slot. Report anatomical names through each sequence's `orientation`.
- **Bournemouth scoring levels** (verified counts over 252 sequences): C0 48, C1 249, C2 252, C3 251, C4 252, C5 251, C6 247, C7 50, T1 7.

  | level | treatment |
  |---|---|
  | C3–C6 | full box and corners (primary) |
  | C7 | scored, but reported separately (it may be an estimated caudal corner under the shoulder) |
  | C2 | caudal corners only: anatomical points 1 and 2 → geometric slots 2 and 3; box excluded |
  | C0, C1, T1 | ignore regions: a prediction there is neither a true nor a false positive |

- **Accuracy and latency are measured separately.**
  - Accuracy comes from `tools/level_prototype.py`, the gated and reported pipeline.
  - Latency comes from a new in-process timer on the same weights, which must first pass a parity check against the prototype.
  - Reason: the prototype's per-frame wall time includes JSON and overlay-PNG writes, so it is not latency.

## 1. Shared pieces, built once

### 1a. Patches to existing files (repo `spinesurg-ct-nnunet:`, branch L6_Class)

1. **`tools/level_prototype.py`: add `--dump-corners`.**
   - At lines 357–362, keep a parallel list `corners.append(kp[i].tolist())` and `kpconf.append(res.keypoints.conf[i].tolist())`, appended in the same branch as `boxes.append` so the ≥4 px size filter keeps them aligned.
   - Write `vert[-1]["corners"]` and `vert[-1]["corner_conf"]` next to `posterior`.
   - Corners are `null` when `--box-detector` or `--boxes-dir` is used.
   - With `--no-orient` the coordinates stay in input pixels.
2. **`tools/patient_keys.py`: add a Bournemouth rule.**
   - `_REALXRAY_ROOT_CORPUS["bournemouth_qf"]="bournemouth"`
   - `_REALXRAY_PREFIX += (("bournemouth","bournemouth"),)`
   - `PERSON_FORMAT["bournemouth"]=r"(?:HV|P)\d{2}"`
   - In `_norm_person`, strip a trailing `[ab]` for bournemouth. HV01a and HV01b are one person; there are 63 people over 126 events (verified pattern `HV##[ab]`, `P##[ab]`).
   - Without this rule, `level_prototype` raises `UnkeyedEvalItem`. Do not reach for `--not-held-out`: Bournemouth really is unseen, and the gate should prove it.
3. **`tools/carmlspine_eval.py:140`: add `--corpus-hint`** to replace the hard-coded `hint="carmlspine"`. Only needed if this scorer is reused; `cine_eval` does its own gating.
4. **`tools/pipeline_state.py`:** register every new stage (the repo's CLAUDE.md requires it). The stages are:
   - `bournemouth_qf_export`
   - `carm_sweep_case39_pose` / `_export`
   - `cine_infer_{bournemouth,case39,case134,synth0533}`
   - `polypose_cine_{warp,render,gt}`
   - `cine_score_*`

### 1b. New file `tools/cine_eval.py`

Pure numpy, scipy and PIL, so it runs on Windows for the self-test. No torch.

**Inputs**
- A `level_prototype` output directory (`<stem>.json`: `vertebrae[{box, det_conf, level, level_prob, single_crop, abstain, posterior, posterior_single, corners?}]`, plus `prototype_meta.json`).
- A truth directory `meta/<stem>.json` in one common schema:
  `{case, stem, seq, frame, view, px_mm|null, boxes:[{gt_id, cls, level|null, box[x0,y0,x1,y1], corners|null (anatomical or geometric, declared by corner_order), role: "score"|"caudal_only"|"ignore"}], extras{angle…}}`.
- `gt_id` is a stable per-sequence identity (level name, or SPINEPS instance id for case134). It is what identity-switch scoring needs.

**Subcommand `score`**

*Matching*, per frame:
- Reuse the `carmlspine_eval.cmd_score` rule for comparability with the paper: the predicted centre lies inside the truth box and IoU ≥ 0.3, one to one, greedy by IoU.
- Secondary arm: IoU ≥ 0.5.
- A `caudal_only` truth (C2) matches when the predicted box's inferior edge lies within 0.25 × median body height of the mean y of the two caudal truth corners and the x-ranges overlap.
- An unmatched prediction whose centre lies in an `ignore` box is dropped. Any other unmatched prediction is a false positive.

*Per-frame, per-level metrics:*
- recall per level, precision overall;
- IoU (mean and median);
- centre error in px, and normalised by the truth endplate length or box height;
- corner error per geometric slot in px and normalised (C2: slots 2 and 3 only); mm only when `--mm-per-px` is known;
- naming: exact, within-1 (`ORDER` from `carmlspine_eval`, where T13 = 19.5 and L6 = 24.5), abstain rate, exact among answered, frame-exact;
- confusion matrix by level;
- every metric also broken down by a bin variable (`--bins angle:...`).

*Temporal metrics*, only when `--track` is given:
- CLEAR-MOT identity switches: the matched track id of a `gt_id` changes from its previous matched frame.
- Fragmentation: tracked → untracked → tracked transitions per `gt_id`.
- MOTA = 1 − (FN + FP + IDSW) / GT.
- IDF1: global `linear_sum_assignment` over the track × `gt_id` co-match matrix.
- Name stability: name switches per `gt_id` per 100 frames, for independent per-frame names and for tracked names. This needs no naming truth, so it also runs on case134.

*Gate:* `EG.add_args(ap)`, then `gate = EG.carry_proto(pred_dir, "tools/cine_eval.py score", not_held_out=a.not_held_out, touched=a.touched, items=[dict(case=…, stem=…, hint=<corpus>)])`, then `EG.stamp(out, gate)`.

**Subcommand `track`** (online and causal; no future frames, so it is honest for a real-time claim)
- **Track state:** id, box, corners, centre velocity, hits, misses, `logp` (27-vector over `meta.level_order`), confirmed flag.
- **Prediction:** shift the box by the velocity.
- **Association:**
  - cost = 1 − IoU(predicted track box, detection box);
  - gate: IoU ≥ 0.1 or centre distance ≤ 0.5 × median detection height;
  - solver: `scipy.optimize.linear_sum_assignment`; reject pairs with cost > 0.9.
  - Do not use `model.track`: `lap` is not installed.
- **Update:**
  - the box is replaced by the detection;
  - velocity is an EMA with α 0.5;
  - `logp = λ·logp + log(posterior + 1e-6)` with λ = 0.9, a memory of about 10 frames.
- **Birth, confirmation and death:** every unmatched detection starts a tentative track, confirmed after 2 consecutive hits; a track dies after `max_age` seconds × fps misses, with `max_age` = 0.33 s.
- **Per-frame naming:**
  - Sort confirmed tracks by y and take `softmax(logp)`.
  - Decode with `fluorocap_anchor.decode(probs, set(), {}, None, direction_known=True, w_rare=1.0)`.
  - Abstain with the prototype's rule: decoded name differs from the pooled argmax, or its probability is below 0.5.
- **Fixed settings:** all constants go in `tracker_config.json` (sha recorded) and are fixed before any Bournemouth frame is seen. If tuning is needed, tune on the synthetic cine (c) and freeze.
- **Output:** `track.json`, per frame `[{track_id, det_index, box, name_indep, name_tracked, p, abstain}]`.

**Subcommand `video`**
- Truth drawn as thin green boxes with corner dots. Predictions coloured by track id from a fixed palette, labelled `t07 C4 0.93` with `?` when abstained. False positives in red, ignore regions in grey.
- HUD: frame index, angle (MachineAngle or `lat_signed_deg`), per-frame latency when given.
- Encode by piping raw RGB to ffmpeg: `-f rawvideo -pix_fmt rgb24 -s WxH -r <fps> -i - -c:v libx264 -pix_fmt yuv420p -crf 18`.
  - Grid: `~/mambaforge/envs/fluorogen/bin/ffmpeg` 8.1.2 (libx264). `cv2.VideoWriter` is the fallback.
  - Windows: `imageio_ffmpeg`'s bundled `ffmpeg-win-x86_64-v7.1.exe`.
- Never burn header text or file basenames into a frame.

**Subcommand `self-test`:** see §2.

### 1c. New file `tools/cine_latency.py` (grid GPU, fluorogen env)

- Load the three weights once. Precompute `v1.film_reference_cdf(~/films_drr)`.
- Per frame, time each stage with `torch.cuda.synchronize()`, batch 1, FP32 as shipped. Discard 20 warm-up frames.
  1. `v1.prepare_panel(im, False, False, hist_ref=ref)`
  2. `det.predict(rgb, imgsz=1024, conf=0.35)`
  3. `sweep_map.Namer(model, head, "cuda").run(img_u8, boxes)` → `(emb, p_single, p_blend)`
  4. `anchor_decode` plus the abstain rule
  5. the tracker update
- **Parity gate first:** on 50 frames per dataset, the boxes must equal the prototype's, the decoded names must be identical, and the maximum posterior difference must be below 1e-5. If parity fails, publish no latency number.
- **Output** `latency.json`: p50, p95 and max per stage and end to end, plus `nvidia-smi --query-gpu=name,driver_version`, host, torch and ultralytics versions, frame size, and body count per frame.

**What can honestly be claimed as "real-time":**
- "Per-frame compute on <GPU name>, models resident, batch 1, excluding acquisition, DICOM decode and display: p50 X ms, p95 Y ms."
- "Real-time at 15 fps" only if the end-to-end p95 is under 66.7 ms (under 97 ms for the 10.3 fps C-arm sweep).
- The tracker is causal, so it adds no look-ahead delay; any offline smoothing is not a real-time result.
- **Not claimable:** glass-to-glass latency, operating-room hardware (the grid GPU is a data-centre card), throughput under concurrent acquisition, or CPU performance. The encoder alone took 3.35 s per frame on a contended CPU.
- A half-precision or TensorRT arm changes the outputs, so it needs its own parity and accuracy run.

## 2. (1) `tools/bournemouth_qf_eval.py`: Bournemouth cervical quantitative fluoroscopy

This is a dataset module that imports `cine_eval`.

### Loader

- Read with `scipy.io.loadmat(p, squeeze_me=False, struct_as_record=False)`, then `D = m["Database"][0,0]`.
- `D.Templates[i,j]` is a 9×4 object array; rows are levels C0…C7, T1, and each cell is an `(n_frames, 2)` array of (x, y).
  - j = 0 is flexion; j = 1 is extension.
- Also read `D.MachineAngle[i,j]`, `D.orientation[i,j]` (L/R), `D.ImageEvent[i,0]`, `Sex`, `Age`, `PatientOrControl`.
- **Missing levels:** test `c.size == 0`. Some are `(0,0)` uint8 and some `(1,0)` float64.
- **Failed frames:** NaN rows, 0.09% of frames; these become missing truth for that frame.
- **Coordinates:** `--coord-origin matlab1` (default) converts with x−1, y−1. The README does not say which origin is used, so the flag stays and the email asks.
- **Returns** `Sequence{event, person (event minus a/b), visit, motion, orientation, sex, age, group, machine_angle (n_ma,), n_frames, levels{name: (n,4,2) anatomical}}`.

### Subcommands

**`export --mat M --out /rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf`**
- Writes `raw/Cervical_Database.mat` (a copy), `meta/<event>_<flex|ext>_f####.json` in the §1b schema, `splits.json` (all test), and `summary.json`.
- Per frame: `view "LAT"`, `px_mm null`, `template_row k`, `frame = k + offset`, `machine_angle_deg`, `orientation`, `offset_status "unverified"`.
- Truth box = min/max of the four corners. This is the same convention as the detector's box (min/max of predicted corners), which makes it the best-matched truth of the three demos.

**`frames --dicom <dir> --root <root>`**, run when the images arrive:
- Read the DICOM with pydicom (fluorogen env). `level_prototype.load_image` cannot read DICOM.
- **Window per sequence**, not per frame, to avoid flicker. Write 8-bit PNG at `images/<stem>.png`.
- **Polarity:** `--polarity auto|asis|invert`.
  - `auto` reads `PhotometricInterpretation` and then checks, on 5 frames per device, that the mean inside the C4 truth quad is brighter than a prevertebral band.
  - Decide once per dataset, record the decision, and never decide per frame. The models expect bone bright.
- **Facing:** `--face asis|L`, default asis.
  - The detector trained with `fliplr=0` on laterals normalised to one facing, and `normalize.detect_facing`'s code and docstring disagree.
  - Before choosing a default, render 5 training labels from `data/yolo_v4z` to see the trained facing.
  - Run the 26 R sequences both as-is and flipped, and report both. Flip the truth x with the frame.
- **Identity:** run the identifier scan on every header (as `case134_sweep` export does). Stems are event-based; no header text is copied.

**`align --pred <proto out> --root <root>`**
- 87 of 252 sequences have `MachineAngle` 1–59 frames longer than their templates.
- For each such sequence, report the mean truth-to-detection IoU over candidate offsets 0…(n_ma − n_t).
- This is a diagnostic only. The applied offset is 0, or the authors' answer, never a data-fitted value.

**`self-test [--mat M] [--out D]`**, runnable today on Windows. Three tiers:
1. **Metric unit tests.** Predictions are made from real truth with known perturbations, and each must return its exact answer:

   | perturbation | expected result |
   |---|---|
   | shift every corner by (3, 4) px | corner error 5.000 |
   | drop C5 on frames 10–19 of an n-frame sequence | C5 recall (n−10)/n, fragmentation 1 |
   | swap the track ids of C4 and C5 at frame 50 | IDSW 2 |
   | rename every level one step caudal | exact 0, within-1 1.0 |
   | put a false box in the C1 ignore region | FP 0 |
   | put a false box below T1 outside any ignore region | FP 1 |
   | same R-orientation sequence, as-is and flipped | identical slot-mapped corner errors |

2. **Render smoke test.** Paint the truth quads of one real sequence (e.g. HV01a flexion) as filled polygons on noise at 1024², write the video, and confirm by eye that the overlays sit on the painted quads at frames 0, n/2 and n−1.
3. **End-to-end grid smoke test**, the only test that exercises the real detector on cervical anatomy before the images arrive:
   - animate a real CSXA lateral film that has corner truth, under a known smooth affine trajectory (±10° rotation plus translation, 150 frames at 15 fps), and transform its corners the same way;
   - run `level_prototype`, then `track`, `score` and `video`;
   - declare `--not-held-out "harness smoke test; CSXA patients are in detector/encoder training"`;
   - the CSXA root is hinted as `/raw/csxa/` in `patient_keys._PATH_HINTS`; I did not read the exact path.

### Run command, once the frames exist

Sharded by sequence as an array on `gmsap,gvohp,galhp --qos=gpu`, fluorogen env:

```
$PY -u tools/level_prototype.py --image "$ROOT/images/${SEQ}_f*.png" --out $RES/pred/$SEQ --no-orient --flag --dump-posterior --dump-corners \
    --detector …/797de71a9e0e42f7/detect_v5z_final_best.pt --model ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt \
    --head ~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt --conf 0.35
```

- Then run `cine_eval.py track | score --corpus-hint bournemouth --bins machine_angle | video --fps 15`.
- Results go to `/rs/rs_grp_oschome/go2432/data/or_ready/cine/bournemouth_qf/<tag>/`.
- **Size:** about 75,600 frames. The GPU time is an estimate I have not measured; the real number comes from a first shard.
- **Pre-specified primary arm:** full frame, imgsz 1024, as shipped.
- **Secondary arm:** an ROI crop upsampled 2× (C4 endplate median is 56 px at 1024, verified), reported alongside the primary, never chosen after the fact.
- **What the truth is:** Bournemouth truth is the output of the authors' semi-automatic template tracker. Report agreement with a validated tracker, not accuracy against independent hand labels.

## 3. (2) C-ArmLSpine CBCT projection sweeps

### Frames

All 301 XA frames per case (1024², ~10.3 fps derived), ordered by InstanceNumber through `device_fit.sweep_frames(case_dir)`. It scans `CBCT/` and `ori/`, keeps XA with Rows = 1024, and drops the 2048² spot frames.

**Angle bins.** Use the registered `lat_signed_deg`. For case134 it is 0.5983·InstanceNumber − 122.45; case39 must be refit on its own poses.

| bin | definition | case134 instances |
|---|---|---|
| lateral (primary) | \|lat + 90\| ≤ 15 | about 29–79 |
| oblique | between the two | — |
| AP | \|lat\| ≤ 15 | about 180–230 |

Zero-shot spot-frame naming was 96.4% lateral and 43.7% AP, so expect naming to collapse toward AP, and report it that way.

### case134 (exists; detection and tracking only)

- **Existing data:**
  - Export at `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep/{images/test/case134_sw###.png, meta/, labels/}`.
  - Poses at `/rs/rs_grp_oschome/go2432/data/carmlspine/sweep/pose/<frame_key>.json`.
  - Truth is 4 SPINEPS body boxes per frame with `level: null`.
- **Convert** the metas to the cine schema, with `gt_id` = SPINEPS instance and `level` null.
- **What case134 can score:** detection, IoU, identity switches, fragmentation, MOTA/IDF1, and name stability. It cannot score naming accuracy: VERIDAH read C1–C5, and the retry run (`spineps_retry134/`, `ok: False`) was never merged.
- The existing score (`or_ready/arc/case134_sweep/`) predates the gate. Re-score it.

### case39 (new)

1. **New file `tools/carm_sweep.py`:** a parameterised copy of `tools/case134_sweep.py`. Leave that file untouched: it produced the existing outputs.
   - `--case caseN`.
   - Replace `sweep_files()` with `device_fit.sweep_frames`.
   - Per-case paths: case134 keeps `SW=.../carmlspine/sweep` and `OUT=.../realxray/carmlspine_sweep`; case39 uses `SW=.../carmlspine/sweep_case39` and `OUT=.../realxray/carmlspine_sweep_case39`. The `carmlspine` prefix keeps gate keying working.
   - Keep `sense_fix`, the sacrum drop (< 20,000 voxels), and the `build_structs` duplicate-instance check.
   - **Regression gate:** `carm_sweep.py export --case case134` into a scratch OUT must reproduce the existing case134 metas (boxes and poses identical) before case39 is trusted.
2. **Poses:**
   `sbatch -D ~/logs` array 0–3 on `gmsap,gvohp,galhp --qos=gpu --gres=gpu:1 --cpus-per-task=8 --mem=96G`, running `carm_sweep.py pose --case case39 --shard $SLURM_ARRAY_TASK_ID --n-shards 4 --skip-done --bounds 40,40,80,10`.
   - The ~20 min per shard estimate is extrapolated from case134's measured 11–19 min per 75 frames.
   - Use the sweep panel pitch of 307.2 mm (K00 −3800 at 1024), not the old 300 mm spot-frame calibration.
3. **New subcommand `orbit --case`:**
   - Fit one rigid orbit to the registered poses: a fixed axis and isocentre, angle linear in InstanceNumber, one K. Write `pose_smooth/`.
   - Truth exists in two versions: per-frame registered (primary) and orbit-smoothed. Flag frames where the two truth boxes disagree (IoU < 0.8).
   - Frames with edge NCC < 0.15 (14/301 for case134) are marked `pose_unreliable` and reported separately. The threshold is fixed now.
4. **`export --case case39`:**
   - Each frame goes `carmlspine_pose.stored_to_atten` → `carmlspine_labels.window_or` (per-frame field window, as in the zero-shot export) → head-up turn.
   - Truth: SPINEPS body instances (subregions 49/50), then `world_points`, `project(K,R,t,pts)`, `box_of` (2nd–98th percentile), `rot_pts`/`upright_turns`.
   - Names come from `levels.json` agreed levels: L2–L5 scored, sacrum role `ignore` for detection (`complete=False`; the detector does not box it). The TS "L1" fragment is role `ignore`.
   - The `VERSE` map in `carmlspine_labels` is VerSe-native; resolve names only through it.
   - Optional secondary: `--window-scope sequence` for the video only.

### Inference and scoring

- `level_prototype` as in §2 over `…/carmlspine_sweep{,_case39}/images/test/case*_sw*.png`, results to `/rs/rs_grp_oschome/go2432/data/or_ready/cine/carm_sweep/<case>/`.
- Then `cine_eval.py score --corpus-hint carmlspine --bins lat_signed_deg:-130,-105,-75,-15,15,60`, then `track`, then `video --fps 10`.
- **Held-out status, decided by the gate at run time:**
  - Primary: the zero-shot v9 stack plus `detector_v5z_final`.
  - Optional secondary: the fold model that held each case out. case39 is fold 2: `~/carm_cvmix2_fov96_ctx/runs/model_rung_1_ft_cv2_v9init_aug2.pt` + `~/model_night/heads_carm/head_cv2_v9init.pt`. case134 is fold 3.
  - The fold weights have no registered sha256, so the gate may raise `UnresolvedLineage`. If it does, drop the arm; do not declare it.
  - Never use the un-suffixed `ft_cv{k}_aug2` / `head_cv{k}` weights or any detector trained on the `realxray` md5%10 split: both cases are train there.
- **Corners:** not scored in (b). There is no corner truth, and 2-D corners are ill-defined on obliques. A later step could project `endplate_corners_body` corners on the lateral bin only.
- **Identity:** case134 `ori/` and its CBCT carry a real PatientID. Key only by `case134_sw###` or `frame_key`, re-run the identifier scan, and keep the video overlay free of any text.

## 4. (3) Synthetic lumbar flexion-extension cine (exact truth)

### Source: CTSP 0533 (token COLONOG_378)

This is the only CTSP case unseen by the v9 chain: it is line 71 of `~/model_night/sweep_v3/cns/unseen_v9.txt`, and was unseen because its CT was truncated. Verified on the grid:

- **CT:** `~/data/CTSpinoPelvic1K/ct/0533_ct.nii.gz`, 250,067,995 B, repaired 2026-09-23 03:03.
- **Label:** `…/labels/0533_label.nii.gz`, PIR, 512×577×512, spacing 0.859/0.800/0.859 mm.
  - It is the v11 scheme: ids 14–24 (T7–L5) and 26; no 29; hips/femurs 30–33; ribs 39–45 and 52–58; no hardware.
- **Body mask:** `/rs/rs_grp_oschome/go2432/data/spineps/bodies/CTSP_0533_body_msk.nii.gz` plus `_body.json`, made 2026-09-23 05:21, after the repair.
- **Cohort row** (`SchwingNet/results/polypose/cohort_sagittal.json`): ordinary, Castellvi none, PI 37.07, SS 32.28, PT 4.79, LL 49.49, flags ok, `s1_plate_source sacrum_under_L5`.
- **`plate_sane` is not yet evaluated.** 64 rows flagged ok still fail it. If 0533 fails, no other CTSP case is v9-unseen, and any substitute must carry `--not-held-out`.

### Motion

- Mobile segments: T10-T11 through L5-S1 from `sampling_spec.json:rom_deg`, with multiplier m = 1 (ordinary).
- N = 60 frames = 4 s at 15 fps, with a_k = −sin(2πk/60): frames 0–30 flex, 30–60 extend, frame 0 neutral.
- `segs[s] = {"flex_ext_deg": frac·m·(a_k·ext_s if a_k>0 else a_k·flex_s), "lat_bend_deg":0, "axial_rot_deg":0}`. Positive is extension.
- At frac 1, the L1–S1 totals are −38.7° flexion (5.8+6.5+7.5+8.9+10.0) and +25.9° extension (4.3+4.3+3.7+5.8+7.8).
- External check: the spec's own note says the in-vitro flex + ext sums (10.1–17.8° per joint) bracket Pearcy 1984's ~14° per joint in vivo.
- Run at frac 0.5 first, look at the frames, then run frac 1.0.

### New driver `tools/polypose/cine_render.py`

About 250 lines. Subcommands:

**`plan`** writes `frames.json`: per-frame segments and the transforms.
- Reuse `polypose_sample` pieces: the scheme and hardware refusals, `plan_from_levels`, `multipliers_for`, `_seg_caps`, `rekey_body_mask`, and `build_transforms(label, affine, LMAP, chain, segments, fused_names, debris_ids)` → `T{id: 4×4 RAS→RAS}`, bodies.
- Resolve names with `ostk.labels.labels_for(volume)`; never import a fixed map.

**`warp --frame k`** (polypose container, GPU):
- `PW.warp_volumes(ct, lab, body_rk, affine, A_c, zooms, [(b[0], b[1]) for b in bodies], frame="moved", device="cuda")`.
- Write to `/rs/rs_grp_oschome/go2432/data/polypose/cine/ctsp_0533_fe/volumes/f###_{ct,label,body_msk}.nii.gz` on the source grid and affine, never reoriented.
- Run `verify_equivalence` once, on frame 30, which has the largest flexion.
- Run the geometric subset of `polypose_invariants`: `label_rigidity`, `jacobian_positive`, `pelvis_fixed`, `field_matches_transforms`. The manifest-row checks do not apply to a cine frame.

**`render --frame k`** (fluorogen env, CPU):
- Template: `tools/arc_angle_set._sweep_subject`.
- Pose, fixed for all frames: `PA.arc_pose(anchor, -90.0, 0.0, 0.0)` with anchor `case29/AP` from `/rs/rs_grp_oschome/go2432/data/devcorpus/poses/surgio_b51_dr.json`.
- Load: `SP.load_lps(f###_ct)`.
- Isocentre: `org_new = org − SP.centroid_mm(L3 mask of frame 0) + anchor["anchor"]`, computed once from frame 0 and reused. Re-centring per frame would move the pelvis.
- Ray-cast: `DR.raycast(d, down=2)` → 1024², pitch = `px_mm`·2 (≈0.30 mm at the detector).
- Style: `DS.style(water, bone, hit, load_device("surgio_b51_dr"), t, rng, pitch, RP=DS.rp_tables())`.
  - `t` is drawn once from frame 0's thickness.
  - `rng = default_rng(fixed seed)` on every frame, giving frozen noise; `style()` draws its window jitter and its noise from the same generator.
  - `rot180` False, field fixed.
- Also write an unstyled −log attenuation → `window_or` arm.

**`gt --frame k`:**
- **Boxes:** `SP.project_mask(warped body mask for id, org_new, sp, M=ext@inv(T), K, down=2, nr, nc)`, both min/max and 2nd–98th percentile, plus `inside`.
- **Exact cross-check:** move the source body voxels by `T[id]` (RAS), convert with `diag(-1,-1,1)` to LPS, and project. The per-frame IoU with the warped-mask box should be ≥ 0.95. Treat this as a check, not an assumption.
- **Corners (new code):**
  - `ostk.vertebral_body.endplate_corners_body(label==id, affine, "superior"|"inferior", sup_axis=…, lr=…)` → (anterior, posterior, rms, n) in world mm on the source, with the axes passed explicitly.
  - Move by `T[id]`, convert to LPS, then `uv = K·(M·p)/z/down`, mirroring `project_mask`'s internals (`spine_project.py:72-87`).
  - Drop any level whose plate rms is high. The ostk canal-closing regression (1b7005c) can corrupt about 1 in 7 vertebrae.
  - These are 3-D mid-sagittal corners, while the detector learned 2-D silhouette corners, so there is a definitional gap. Also write the silhouette quad (min-area rectangle of the projected body polygon) as a second corner truth.
- **Names:** T12, L1–L5 from `labels_for`; score levels with `inside ≥ 0.5`. Record K, M, pitch and `org_new` per frame.

**`check`:** contact sheet of frames 0, 15, 30, 45 with the projected truth drawn on the DRR. **Look at it before scoring anything.**

### Jobs (`slurm/polypose_cine.sh`)

| stage | resources | estimate |
|---|---|---|
| warp | `--array=0-59%8`, `gmsap,gvohp,galhp --qos=gpu`, `slurm/polypose_env.sh pp_run --nv $PP_PY` | 3–8 min per frame (0874 took 192 s; 0244/1065 took 427–475 s) |
| render + gt | `--array=0-59` on `reqp --qos=requeue` | about 1 min per frame |
| infer | `level_prototype` (+`--dump-corners`), gated with items `dict(case="0533", stem=…, hint="ctsp")` | minutes |
| score / track / video | CPU | minutes |

- Warped volumes (about 60 × 3 files) go on CephFS, not home.
- Results go to `/rs/rs_grp_oschome/go2432/data/or_ready/cine/synth_fe_0533/`.

### Cervical synthetic cine: not in this build, and why

Every piece of the generator assumes a lumbar spine:
- a v11-only scheme check;
- a chain hinged on S1;
- no cervical rows in the ROM table;
- a CTSP-only flag table;
- the devcorpus `LEVELS` list and its sacrum requirement;
- no C0 label, and VerSe has no skull label.

A future route is a TotalSegmentator v3 unseen subject (`arc_unseen/subjects.txt`, 40 subjects) with `vertebrae_C1..C7` plus `skull`, a new chain hinged at C7-T1, a published cervical ROM table, and the skull rigid with C1.

## 5. Order of work

1. **Now, locally, no grid:**
   - Copy `Cervical_Database.mat` out of the session scratchpad, which is ephemeral, to durable storage outside git and to `/rs/.../realxray/bournemouth_qf/raw/`.
   - Write `cine_eval.py` and `bournemouth_qf_eval.py`; run `self-test` tiers 1–2 on Windows.
   - Apply the §1a patches.
   - Fix `docs/BOURNEMOUTH_DATA_REQUEST_DRAFT_2026-09-26.md`: it cites a harness README that does not exist. Write `docs/BOURNEMOUTH_QF_HARNESS.md` or cut the sentence.
   - The email asks for:
     - the DICOM keyed to event ids;
     - whether template row 1 is cine frame 1, and the reason for the 87 length mismatches;
     - the pixel spacing, and whether distortion correction was applied;
     - the coordinate origin (MATLAB 1-based?);
     - the polarity;
     - the lumbar cine and templates;
     - the data-sharing terms.
2. **Grid:**
   - Commit and push via WSL; `git pull` in the grid clone (never scp).
   - Submit the case39 pose array; the CSXA smoke test (tier 3); the synthetic `plan`, then the warp array at frac 0.5; and the case134 re-inference. Chain with `afterany` and check each output.
   - Record job ids and ETAs in the checkpoint (`docs/PIPELINE_RESUME.md`) and stop until reactivated.
3. **After the poses and warps land:** `orbit`, `export` case39, the regression export for case134, render + gt, the `check` contact sheet, inference, then track, score, video, and `cine_latency` with its parity check.
4. **When the Bournemouth DICOM arrives:** `frames`, `align` (diagnostic), the inference array, then score, track, video and latency.

## 6. Blockers and unknowns

**Blocking or likely to break:**
- The prototype's defaults load the wrong model (`allspine_v2_r1`); always pass `--detector`, `--model` and `--head`.
- Bournemouth frames fail the gate until the `patient_keys` rule exists. `carmlspine_eval` hard-codes its corpus hint.
- Corners are discarded until the `level_prototype` patch lands.
- **Bournemouth:** images not in hand. Pixel spacing, polarity, the template-to-frame offset (87 sequences), the coordinate origin and the licence/data terms are all unknown.
- **Cervical detection:** it trained on C3–C7 of CSXA films only (C2 was dropped; C1 and T1 never appear), and bodies are about 56 px at 1024. No cervical fluoroscopy frame has ever been scored.
- **The decoder** forces one contiguous run: a missed middle body, or a false box at the occiput, C1 or hardware, shifts every name after it.
- **case134:** no level truth.
- **case39:** no poses or export yet. The TS L1 fragment must be ignored; the sacrum is incomplete.
- **Sweep truth** is registration-derived (edge NCC median 0.33 for case134) with about 0.7° of frame-to-frame jitter; there is no vendor geometry file.
- **Synthetic cine:**
  - 0533 `plate_sane` is unevaluated.
  - The `surgio_b51_dr.json` card is only in the grid working tree, not in git.
  - `style()` couples window jitter and noise.
  - Voxels pulled from outside the source grid become air. The ~200 mm isocentre field centred on L3 should keep the top wedge out of view; check `inside` and `hit`.
  - PolyPose has never run end to end to a rendered frame, and no output has passed the v4 checker.
  - Do not route warped masks through `make_drr_dataset.body_mask_for`: it raises `SpinepsIdError`.
  - The ostk corner regression.
- **Coordinate frames:** PolyPose uses RAS (nibabel); `spine_project` and devcorpus use LPS indexed (z,y,x); carmlspine uses SimpleITK LPS. Keep K00's negative sign.
- **Environment:** `lap` is not installed (no `model.track`); Windows Python has no ultralytics and CPU-only torch.

**Unknown, not guessed:**
- The GPU model behind each partition. `latency.json` records it.
- Whether v9 names cervical fluoroscopy frames correctly.
- The cause of the ~4° header-to-registered offset on the sweeps, and the meaning of private tag (0037,0011).
- Whether the fold models' lineage resolves in the gate.
- Whether an obscured C7 can be told apart in the `.mat`.
- Which of the facing heuristic's code and docstring is right.

## Files

**Existing:**
- `spinesurg-ct-nnunet:tools\level_prototype.py`
- `spinesurg-ct-nnunet:tools\sweep_map.py`
- `spinesurg-ct-nnunet:tools\fluorocap_infer.py`
- `spinesurg-ct-nnunet:tools\fluorocap_anchor.py`
- `spinesurg-ct-nnunet:tools\eval_gate.py`
- `spinesurg-ct-nnunet:tools\patient_keys.py`
- `spinesurg-ct-nnunet:tools\carmlspine_eval.py`
- `spinesurg-ct-nnunet:tools\case134_sweep.py`
- `spinesurg-ct-nnunet:tools\device_fit.py`
- `spinesurg-ct-nnunet:tools\carmlspine_labels.py`
- `spinesurg-ct-nnunet:tools\polypose_sample.py`
- `spinesurg-ct-nnunet:tools\polypose_warp.py`
- `spinesurg-ct-nnunet:tools\arc_angle_set.py`
- `spinesurg-ct-nnunet:tools\spine_project.py`
- `spinesurg-ct-nnunet:tools\deepfluoro_render.py`
- `spinesurg-ct-nnunet:tools\device_style.py`
- `spinesurg-ct-nnunet:tools\pose_arc.py`
- `spinesurg-ct-nnunet:slurm\carmlspine_cv_v9init.sh`
- `spinesurg-ct-nnunet:SchwingNet\results\polypose\sampling_spec.json`
- `spinesurg-ct-nnunet:SchwingNet\results\polypose\cohort_sagittal.json`
- `spinesurg-ct-nnunet:docs\BOURNEMOUTH_DATA_REQUEST_DRAFT_2026-09-26.md`
- `laptop:Desktop/spine-detector\src\manifest.py`
- `OpenSpineToolkit:ostk\vertebral_body.py`
- `laptop-scratchpad:bournemouth\Cervical_Database.mat` (ephemeral; copy it)

**New (not created):**
- `tools/cine_eval.py`
- `tools/bournemouth_qf_eval.py`
- `tools/cine_latency.py`
- `tools/carm_sweep.py`
- `tools/polypose/cine_render.py`
- `slurm/cine_eval.sh`
- `slurm/carm_sweep_case39.sh`
- `slurm/polypose_cine.sh`
- `docs/BOURNEMOUTH_QF_HARNESS.md`