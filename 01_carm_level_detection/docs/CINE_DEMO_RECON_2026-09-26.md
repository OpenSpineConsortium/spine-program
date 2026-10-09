## reader 0

The best model for arbitrary frames is the manuscript's zero-shot SchwingNet stack. That is the `allspine_v9` level encoder with its plain mixed-length head, fed boxes from the `detector_v5z_final` corner detector. It runs through `tools/level_prototype.py` on a grid GPU. It has never been tested on a cervical fluoroscopy frame; the cervical evidence is from plain films and renders. Everything below was read from files or the grid; nothing was edited or submitted.

## 1. Which model is "best" (v9 lineage; the manuscript was re-run on it)

| piece | grid path | how it is identified |
|---|---|---|
| Corner (body) detector | `/wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` (same file as `~/FluoroCap/detect_v5z_final_best.pt`) | registry alias `detector_v5z_final`. YOLO11m-pose, one class "vertebra", 4 keypoints, imgsz 1024, confidence 0.35 |
| Level encoder | `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` | alias `allspine_v9_fov96_ctx_rung_1_aug2`, sha256 prefix 188f9fcbfa3c6de1. ResNet-18 with a two-channel stem, 27 classes (C1–C7, T1–T13, L1–L6, sacrum) |
| Recurrent head | `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` (sidecar `.arch.json`, base_model = the v9 encoder) | two-layer BiGRU trained on mixed runs of 2–9 bodies, no alphabet loss |

- **Its headline:** zero-shot C-ArmLSpine lateral 595/617 = 96.4 % (`SchwingNet/results/eval_gate/leaks/zeroshot_v9.json`, gate HELD OUT); AP 276/631 = 43.7 %.
- **Other v9 heads:** `..._alpha0.3_seed{0,1,2}.pt` add the alphabet loss for counting from the sacrum. The CNS sweep used them. They are not the zero-shot head and are irrelevant without a sacrum.
- **C-ArmLSpine fold models** (lumbar C-arm fine-tunes): `~/carm_cvmix{k}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt` with `~/model_night/heads_carm/head_cv{k}_v9init.pt`, k = 0–4; the test fold is `md5(case) % 5 == k`. The case-grouped five-fold scored lateral 601/617 (97.4 %).
  - The un-suffixed `ft_cv{k}_aug2.pt` / `head_cv{k}.pt` start from `allspine_v2_r1`, whose training bank was deleted. The gate refuses them as held out. Don't use them.
- **Sacrum detector (lumbar only):** `~/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt`. YOLO11m boxes, classes 0 vertebra / 1 sacrum, whole-vertebra boxes, confidence 0.74, C-ArmLSpine held out. Useless for cervical.
- **The "detect_v2 AP50 0.970" figure:** that is detect_v2, an earlier corner detector. `docs/MANIFEST_DATA_MODELS_RESULTS.md` says the memory's "AP50 0.970" is a different quantity from detect_v2's box mAP50 of 0.9907.
  - The lineage runs v2 → v3 → v4 → v5z_final (fine-tuned 60 epochs from v3; pose mAP50 0.9929 on its training-time validation).
  - `detector_v6f` is newer (self-trained) but did not raise the box rate. The website service ships an intermediate epoch, `detect_v5z_epoch25`.
- **No weights are on this workstation.** The only local files are old ONNX exports (`spine-detector/dist/detect_v4_1024_fp32.onnx` etc.), so inference has to run on the grid.

## 2. How to run it

```
PY=~/mambaforge/envs/fluorogen/bin/python   # torch 2.6+cu124, ultralytics 8.4.138, opencv 5.0, pydicom, scipy, ffmpeg binary
$PY -u tools/level_prototype.py --image <dir|glob> --out <dir> --no-orient \
   --model ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt \
   --head ~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt \
   [--conf 0.35] [--dump-posterior] [--flag] [--boxes-dir <meta dir> for oracle boxes] [--not-held-out "<reason>"]
$PY -u tools/carmlspine_eval.py score --pred <out> --meta <meta dir> --out score.json --tag ...
```

- **sbatch pattern** (`slurm/carmlspine_cv_v9init.sh`): `--partition=gmsap,gvohp,galhp --qos=gpu --gres=gpu:1 --cpus-per-task=8 --mem=96G`, `export PYTHONNOUSERSITE=1`, `TMPDIR=/dev/shm/...`, `set -u` (never `-e`), submitted with `sbatch -D ~/logs`. The `spinedet` env has the same ultralytics.
- **The defaults are wrong.** Without `--model` and `--head`, the prototype loads `allspine_v2_r1` and the `allspine_v2` head set. It then runs single-crop only, and the gate raises UnresolvedLineage.
- **Flags:** pass `--flag` with no paths to skip the LSTV/TLTV flag models; on cervical frames they would only abstain.

## 3. The pipeline inside the prototype (`tools/level_prototype.py`)

1. **Load:** 16-bit input is scaled by the 0.5–99.5 percentiles to 8-bit grey. Colour input is converted to grey.
2. **Optional orientation net.**
3. **Histogram match** to the mean histogram of `~/films_drr/img/*.npy` (default on; 9,109 files).
4. **Detection:** `YOLO.predict(rgb, imgsz=1024, conf=0.35)`. Each box is the tight min/max of the 4 predicted corners, sorted top to bottom. The corner coordinates themselves are thrown away.
5. **Crops** (`fluorocap_infer.crops_for_run`, rung 1): the image is rescaled so the box height is 96 px, a band of about 3 bodies is kept, and a 320×320 window is cut around the target body. Channel 2 is the target box mask. Horizontal-flip test-time averaging is on.
6. **Naming:** single-crop softmax plus the head over the whole run of boxes. Then `fluorocap_anchor.decode` gives the run a contiguous level sequence, top = cranial when direction is known (T13/L6 allowed, rare penalty 1.0).
7. **Abstain** when the decoded name differs from the single-crop name, or when its probability is below 0.5.

**Output per image:** `<stem>.json`, `<stem>_overlay.png` and `prototype_results.json`.
- Per vertebra: `box` [x0,y0,x1,y1] in input pixels (unchanged with `--no-orient`), `det_conf`, `level`, `level_prob`, `single_crop`, `single_crop_prob`, `top3`, `entropy`, `region`, `abstain`. With `--dump-posterior`, also 27-vectors ordered as `meta.level_order`.
- `prototype_meta.json` records every weight's sha256 and the eval_gate verdict.

## 4. What breaks

**The gate on new data.**
- `level_prototype` calls `eval_gate.assert_unseen_all`. An image stem that `tools/patient_keys.key_any` cannot key (e.g. Bournemouth `HV01a`) raises UnkeyedEvalItem unless `--not-held-out "<reason>"` is passed. The proper fix is a `bournemouth` corpus rule in `patient_keys.py`.
- `carmlspine_eval.py score` hard-codes `hint="carmlspine"` when it carries the verdict (line ~119), so it has to be generalised before it can score another dataset.

**The scorer is not enough for a cine.**
- A call matches truth only if its centre falls inside the truth box and IoU ≥ 0.3, one to one, greedy by IoU.
- Each truth meta needs `case`, `view` (per-view summaries exist only for "AP" and "LAT"), and `boxes: [{cls:0, level, box}]`. A box with `level: null` is left out of the naming score.
- It computes no corner error, no identity switches and no temporal metric. It does already order C1–C7.

**Corners need a direct YOLO call.**
- Call YOLO yourself and read `res.keypoints.xy` (N,4,2) and `.conf`.
- The training slot order is geometric (`spine-detector/src/manifest.py::canonical_slots`): 0 = superior, smaller x; 1 = superior, larger x; 2 = inferior, larger x; 3 = inferior, smaller x. Image y points down.
- Training used `fliplr=0.0` (confirmed in `detect_v5z/args.yaml`). Training laterals were normalised to one facing, "left" as BUU ships them.
  - The facing heuristic's code and docstring in `spine-detector/src/normalize.py::detect_facing` disagree, so check facing visually.
  - Mapping slots to anterior/posterior depends on facing. Re-sort predicted corners geometrically before matching them to truth corners.
  - Boxes seemed to survive either facing: 617/676 = 91.3 % of agreed lateral bodies were boxed on C-ArmLSpine, whose frames are only turned head-up, never flipped.

**Intensity.**
- The models expect bone bright. The prototype does not invert (`prepare_panel` is called with `auto_invert=False`). Raw fluoroscopy and XA are usually transmission-like, with bone dark.
- The real-frame convention (`docs/REAL_XRAY_DATASETS_SPEC.md`, "Display"): `-log` to attenuation, then `window_or` (field percentiles 1/5/50/95/99 mapped onto 27/47/126/216/239), then head-up by rot90. This is implemented in `tools/carmlspine_labels.py` (around lines 250–260) and `deepfluoro_anchor.window_or`.
- CLAHE was used only for NHANES in detector training.

**Scale and pixel spacing.**
- The encoder is scale-normalised to the box height (96 px), so a box drawn around the whole vertebra rather than the body skews the crop scale.
- The detector trained at imgsz 1024 with scale augmentation 0.85 and zoom variants. mm spacing matters only for reporting errors in mm.
- C-ArmLSpine exports are 1024² at 0.1915 mm in the object plane. The raw cone-beam sweep XA is 1024 rows (`carmlspine_io.py`).

**The decoder.**
- It forces one contiguous level run across all boxes in a frame. A missed body in the middle, or a false box (occiput, hardware), shifts every name after it. With `direction_known=False` it also tries the run reversed.
- Frames are named independently, so a tracker should pool posteriors per track (from `--dump-posterior`) before decoding.
- `ultralytics model.track` needs `lap`, which is not installed; `scipy.optimize.linear_sum_assignment` is available instead.
- `sweep_map.ncc_shift` links frames at full resolution and takes about 7 minutes per pair (`docs/MODEL_CARD.md` §6.2), so it is unusable for cine.

**Speed.** On a contended CPU the encoder took 3.35 s per frame for 4 bodies with flip averaging. Use a GPU.

## 5. Cervical lateral coverage: film yes, fluoroscopy never tested

**Detector.**
- It trained on 3,971 CSXA lateral cervical films (7,942 with zoom variants in `data/yolo_v4z`), alongside BUU 5,763, NHANES 443, Mendeley 453 and AASCE 377 films.
- CSXA supplies full quads only for C3–C7. C2 was deliberately dropped (`src/converters/csxa.py`). C1 and T1 never appear on a lateral cervical film in training.
- So expect C3–C7 to be boxed, and C2 and T1 to be unreliable. Bournemouth's C0 has no class; C1 has no body.

**Encoder** (v9 validation, which is the split that chose the checkpoint, so not held out; single crop, all sources pooled):

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | T1 |
|---|---|---|---|---|---|---|---|
| 92.1 % (n 114) | 90.6 % (n 160) | 95.3 % | 92.9 % | 90.5 % | 92.8 % | 90.1 % | 77.8 % (n 153) |

C3–C7 each have about 920 crops.

- CSXA alone: 99.2 % single crop. With the head: 99.8 % (3,629/3,635), 99.6 % at three bodies (`results/a5.json`). Every CSXA patient is in training or selection, so none of this is held out.

**Untested.** The model card's limitation (10) lists cervical and thoracic intraoperative frames as untested; no cervical fluoroscopy frame has ever been scored. No C2 anchor has been shown on a real intraoperative frame. The alphabet coupling and count need a sacrum and do not apply.

**Option not measured:** `films_all2` (alias `films_all2_rung1_aug2`) is cervical+lumbar film only, but its bank has the NHANES double-inclusion leak. It is not the manuscript's model.

## 6. For the C-ArmLSpine demo (b)

- **Held-out models:**
  - `case39` falls in CV fold 2 (`md5 % 5`) and `case134` in fold 3; only those folds' fine-tuned models are held out for them.
  - The zero-shot v9 stack, `detector_v5z_final` and `rx_lodo_carmlspine_1024` are held out for both.
  - In the realxray split (`md5 % 10`) both cases are train (2 and 3), so any same-device detector trained on that split saw them.
- **case134 cannot be scored for naming.** VERIDAH misnamed its CBCT as C1–C5, so it has no agreed level; `tools/case134_sweep.py` exports it detection-only to `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep/`.
- **Identity:** `case134/ori` carries a real PatientID and name. Never print it and never add it to a bank.

## Not found

- No packaged video or cine inference, no tracker, and no corner-level scorer exist in the repository.
- The service (`service/app.py`, `POST /infer`) does return 4 corners per body, but it serves an older release (detector epoch25, older level model).
- The fold encoders and heads have no registered sha256 (model card §1.3). The v9 encoder does.

Key files (absolute):
- spinesurg-ct-nnunet:tools\level_prototype.py
- spinesurg-ct-nnunet:tools\carmlspine_eval.py
- spinesurg-ct-nnunet:tools\fluorocap_infer.py
- spinesurg-ct-nnunet:tools\fluorocap_anchor.py
- spinesurg-ct-nnunet:tools\eval_gate.py
- spinesurg-ct-nnunet:tools\patient_keys.py
- spinesurg-ct-nnunet:tools\carmlspine_labels.py
- spinesurg-ct-nnunet:slurm\carmlspine_cv_v9init.sh
- spinesurg-ct-nnunet:SchwingNet\atlas\model.json
- spinesurg-ct-nnunet:SchwingNet\NUMBERS.md
- spinesurg-ct-nnunet:docs\MODEL_CARD.md
- spinesurg-ct-nnunet:docs\REAL_XRAY_DATASETS_SPEC.md
- laptop:Desktop/spine-detector\src\manifest.py
- laptop:Desktop/spine-detector\src\normalize.py

## reader 1

# C-ArmLSpine sweeps (case39/CBCT and case134/ori): map for demo (b)

Everything below was read from disk on the grid and in the local repo. Nothing was edited, created in a repo, or submitted. The local tool files are byte-identical to the grid clone (md5 checked). No C-ArmLSpine image data is stored on Windows; only reports and figures in `spinesurg-ct-nnunet/docs/`.

**Bottom line:** case134 already has a per-frame pose and projected body boxes for all 301 frames, but no trustworthy level names. case39 has usable level names (L2–L5 and sacrum) but no poses and no export yet.

## 1. Where the data lives (grid)

- **Release:** `/rs/rs_grp_oschome/go2432/data/carmlspine/unpacked/C-ArmLSpine/case<N>/`, 149 cases. Zip at `.../carmlspine/C-ArmLSpine.zip`.
- **case39:**
  - `C-arm/` holds 3 spot frames (AP 0°, LAT 90°, LAT2 90°), 2048², `.dcm` names.
  - `CBCT/` holds 696 files: 394 CT slices, 301 sweep projections (XA, 1024²) and one 698-byte stub.
- **case134:**
  - `C-arm/` is empty. Its AP and LAT spot frames (2048²) sit inside `CBCT/` (396 files = 394 CT + 2 XA).
  - `ori/` holds 302 files: 301 XA at 1024² plus a 788-byte stub.
- **The stubs:** both carry private (0037,0101) = "rebuild Template ZIP FILE" with an empty (0037,0102). The vendor reconstruction/geometry template was not shipped. **No projection matrices exist anywhere.**
- **Header catalogues** (small JSON, safe to read):
  - `.../carmlspine/headers_dossier.json` → `sweeps.case39` / `sweeps.case134`: one row per file with InstanceNumber, angles, SID/SOD, AcquisitionTime, kVp.
  - `.../carmlspine/catalogue.json` → `cbct.<case>`.
  - `.../carmlspine/sweep/HEADERS.md` and `headers.json` (case134 only).
- **CBCT NIfTI:** `.../carmlspine/nifti/case39_cbct.nii.gz` and `case134_cbct.nii.gz`.
  - 394³ at 0.5 mm, identity direction, origin (−98.25, −98.25, −98.25), so centred on (0,0,0) in LPS mm.
  - Written by SimpleITK from `tools/carmlspine_io.read_cbct`, which assembles slices by position (a GDCM series read returns one slice).
  - DICOM facts: PatientPosition FFS, RescaleIntercept −1024. The 197 mm field covers roughly L1/L2 to S1.
- **Labels:**
  - TotalSegmentator: `.../carmlspine/ts/<case>/vertebrae_{T9..L5}.nii.gz`, `sacrum.nii.gz`, plus hip and femur masks.
  - `.../carmlspine/ts_s1/<case>/vertebrae_S1.nii.gz`. TS `sacrum` excludes S1; the whole sacrum is the union.
  - SPINEPS: `.../carmlspine/spineps/<case>_seg-vert_msk[_veridah].nii.gz`, `_seg-spine_msk.nii.gz` (subregions 49/50 = vertebral body), `_ctd.json`. These sit on SPINEPS's own cropped grid, so join to TS masks by world coordinates.
  - Level agreement between the two labellers: `.../carmlspine/levels.json` (`cases.<case>.vertebrae[]`, fields ts / spineps / dice / agree / level).
  - Registered spot-frame poses: `.../carmlspine/pose/case39_{AP_ref,LAT_ref2,LAT2_ref2}.json`, `case134_{AP_ref,LAT_ref2}.json`, and `consensus.json`.

## 2. Sweep structure (both cases the same)

- **Files and order:** 301 XA frames, InstanceNumber 0–300. Sorted file-name order equals InstanceNumber order for both cases.
- **Series UIDs:**
  - case39 was re-anonymised: every file has its own random-UUID SeriesInstanceUID, which is an invalid UI value.
  - case134 has one series.
  - Order frames by InstanceNumber; never group by series.
- **Frames:** 1024² uint16, MONOCHROME2, transmission-like (bone dark). PixelIntensityRelationship is empty.
- **Exposure:** 111 kVp, 12–13 mA, ExposureTime 10.
- **Geometry tags:** SID 1140, SOD 745 on every frame. Tilt (PositionerSecondaryAngle) is 0.7/0.9 for case39 and 0.4/0.6 for case134.
- **Angles (PositionerPrimaryAngle):** case39 runs 122.0 → −54.3, case134 122.0 → −51.5.
  - Only 58 distinct readings, never increasing. The reading holds for runs of 5–6 frames, then steps by about 3.2°.
  - So the per-frame header angle is stale for up to one run.
- **Timing and frame rate:** 301 frames over 29 s (case39 15:04:10–15:04:39, case134 15:12:31–15:13:00), about 10.3 fps.
  - This is derived; there is no FrameTime or CineRate tag, and AcquisitionTime has only 1 s resolution.
- **Pixel spacing (the brief's "~0.15 mm" is wrong for the sweeps):**
  - DICOM PixelSpacing 1.0 is a placeholder, and there is no ImagerPixelSpacing.
  - The panel is 307.2 mm (iRay Jupi1212X, 150 µm × 2048), so the 1024-pixel sweep frames are 0.30 mm at the detector (2×2 binned) and 0.196 mm at the isocentre (magnification 1.530).
  - 0.1465 mm is correct only for the 2048-pixel spot frames.
- **The CBCT is reconstructed from its own sweep:**
  - Private (0037,0014) names the profile `FICBCT_3DC_110kv_300_FDK_noSC_AutoMAR`, and (0037,0010) = 300.
  - The CBCT slices are timestamped 15 s after each sweep ends (case39 15:04:54, case134 15:13:15).
  - The spot frames were taken about 40–106 s before the sweep, so the patient may have moved between spot and sweep, but sweep and CBCT belong to one acquisition.
- **Private raw twin (0037,0020):** a 2 MB near-raw frame, stored rotated 180° relative to the main image.
  - case134: proper VRs (OW, US, FD).
  - case39: the anonymiser re-encoded the private tags as LO, so `ds[tag].value` comes back as a decoded string. `device_fit.read_sweep_frame` therefore skipped all 301 case39 frames with "no private raw twin" (log `~/model_night/logs/devfit_40411907.out`).
  - The bytes are intact: `ds.get_item(0x00370020).value` returns 2,097,152 bytes, which reshapes to 1024² uint16 (tested). A detection demo does not need it; the main pixel data is the display frame.

## 3. Poses and projection code

- **Pinhole camera model** (`tools/drr_register.py`):
  - `p_cam = R·p_LPS + t`, `uv = K·p_cam`. Rays are cast at pixel centres (col+0.5, row+0.5).
  - The mirrored detector is carried by a negative `K[0,0]`.
- **Device convention** (`pose/consensus.json`):
  - AP: `dir(0,-1,0)_rot180_m-1`.
  - LAT: `dir(1,0,0)_rot180_m-1`. The source sits at the patient's right, which is lat −90 in `pose_arc`.
- **Header-only start pose for any sweep frame** (identical constructions):
  - `carmlspine_pose.oblique_starts(angle, base_hypothesis(key,"AP",centre,sod), centre, sod)` (both angle senses).
  - `device_fit.sweep_start(theta, sign, centre, sod)`.
- **Refinement:** `drr_register.register(mu, A, att, px_mm, sdd, sad, starts=[...], tc_bound=(bx,by,bz), rot_bound_deg=r, device="cuda", work=384, topk=2)`.
  - Uses a homegrown torch ray-march DRR and edge NCC.
  - Returns K (full resolution), R, t, `edge_ncc`, `margin`, `_drr`, `_img`.
- **Projection helpers** in `tools/carmlspine_labels.py`:
  - `world_points(nii, select, rng, max_pts)` returns LPS points via SimpleITK.
  - `project(K,R,t,pts)`, `box_of(uv,S)` (2nd–98th percentile, visible fraction), `hull()`, `rot_pts`, `upright_turns`.
  - `levels_for(case, levels)`, `window_or` (the OR percentile window).
  - The `VERSE` map is VerSe-native: 20–24 = L1–L5, 25 = L6, 26 = sacrum, 28 = T13. **Not the legacy ostk map.**
- **DiffDRR** is used only in `tools/reg_level_harness.py`, `reg_deepfluoro*.py` and `polypose_*`, all on CTSpinoPelvic1K or DeepFluoro. It has never been run on C-ArmLSpine.
- **Not geometry, despite the names you listed:**
  - `~/model_night/deepfluoro/calibration_best.json` holds DeepFluoro intensity/formation terms (kb, s, σ…).
  - The device cards (`~/spinesurg-ct-nnunet/docs/devices/surgio_b51_dr.json` on the grid) hold appearance terms plus SID/SOD, pitch and the orientation string.
  - `tools/carm_miss_diagnostic.py` is a scoring diagnostic on the spot-frame test split.
  - `tools/pose_arc.py` (`angles_of`, `arc_pose`) is useful for signed lat/tilt/roll and for synthetic arcs, not for real sweep truth.

## 4. What already exists for case134 (`tools/case134_sweep.py`, hard-coded to case134)

- **CLI:** `headers | pose --shard i --n-shards 4 --skip-done --bounds 40,40,80,10 | export [--window-region field|body] | score --weights name=/path/best.pt [--imgsz 1024] [--not-held-out-role ROLE=REASON]`.
- **Jobs and runtime:** headers 40419722, pose 40419723 (array of 4, GPU, about 11–19 min per 75 frames, roughly 15 s per frame), export 40419724 then 40424655 / 40424661.
- **Poses:** `/rs/rs_grp_oschome/go2432/data/carmlspine/sweep/pose/<frame_key>.json` (301 files). `frame_key` = first 12 hex characters of sha1(basename).
- **Export:** `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep/`
  - `images/test/case134_sw###.png`: 1024² 8-bit, −log then OR window, windowed per frame over the central field, bone bright, head-up (0 quarter turns on all 301).
  - `labels/test/*.txt`: YOLO format, class 0 = vertebra, 1 = sacrum.
  - `meta/*.json`: angle, lat/tilt/roll signed, pose K/R/t at 1024 (K00 = −3800, cx = cy = 511.5), edge NCC, `from_header`, and boxes with `level_ts`, `level_spineps`, `level` (null), `visible_frac`, `complete`, `kept`, `box_source`.
  - Also `summary.json`, `qc/contact_sheet.png`, and an identifier scan result of 0 hits.
- **What each frame's truth contains:**
  - Exactly 4 vertebral-body boxes (SPINEPS body instance, axis-aligned). No sacrum: the TS sacrum is a 1,431-voxel fragment on this clipped field.
  - No corners and no outlines. On lateral views the axis-aligned box of a tilted body takes in disc wedges.
- **Registration quality:**
  - Edge NCC median 0.33 (IQR 0.22–0.46). 14 of 301 frames are below 0.15; the far-oblique bin (−130° to −100°) has median 0.19.
  - The refined pose sits 4.4° (median) from the header start; the 58.5 mm median source shift is mostly that rotation.
- **Angle relations I measured on the 301 metas:**
  - Registered `lat_signed_deg = 0.5983·InstanceNumber − 122.45` (residual SD 0.74°, maximum 3.98°).
  - Equivalently `lat_signed ≈ −PositionerPrimaryAngle − 4.2°` (5th–95th percentile of the offset: 2.1–5.9°).
  - Registered tilt median 0.17°, roll median −0.2°.
  - Header angles alone are not truth; interpolating over InstanceNumber is better, and registration is still needed.
- **I looked at the overlays** (`or_ready/arc/case134_sweep/frame_{00,90}_truth.png` and the contact sheet): the boxes sit on the four bodies at AP and oblique angles. On the laterals the lower two boxes include disc wedges.
- **Existing scores:**
  - `/rs/.../or_ready/arc/case134_sweep/case134_sweep.{json,md}`: an older, ungated run (pooled 93.6% body recall at confidence 0.25).
  - Gated coverage-arm runs: `SchwingNet/results/coverage/experiment/runs/*/case134/`.
  - Scoring is detection only; `score` has no naming path.

## 5. What does not exist yet for case39

- No sweep poses, no export and no raw-pair twins. The corpus census records "the second sweep is in no root."
- **Truth available:**
  - `levels.json` agrees on L2, L3, L4, L5 and sacrum (dice 0.95 / 0.80). case39 has `_seg-vert_msk_veridah.nii.gz`.
  - The TS "L1" is a fragment at the top edge of the field with no SPINEPS body. In the spot frames it is exported as a `whole_vertebra` box overlapping L2 on AP and sitting posterior on LAT. Drop it or mark it ignored.
  - The sacrum is present but `complete=False`.
- **Adapting `case134_sweep.py` requires:**
  - Parameterising `CASE`, `ORI`, and the shared `SW=.../carmlspine/sweep`, whose `headers.json` and `pose/` are case134's.
  - Reading XA frames with Rows == 1024 from `case39/CBCT` in InstanceNumber order (`device_fit.sweep_frames` does exactly this) instead of `sweep_files()`, which lists `case134/ori` only.
  - Keeping the sacrum gate (under 20,000 voxels means drop) and the duplicate-instance check in `build_structs`.

## 6. Things that will break or mislead

1. **case134 has no level names.**
   - VERIDAH read the bodies as C1–C5, and TS L1 and L2 both resolve to one SPINEPS body. After the duplicate drop the TS names are "L1", L3, L4, L5 with a gap.
   - Counting up from the sacrum in the AP overlay suggests the top body is L2, and a SPINEPS re-run (`.../carmlspine/spineps_retry134/`, job 40416621) gave ids 21–24 and 26 (L2–L5, sacrum) with `ok: False`. That run was never merged into `levels.json`.
   - Treat case134 names as unknown until a human reads them. Only case39 can score naming.
2. **Neither sweep is held out** for any model fine-tuned on the C-ArmLSpine train split: both cases have `split: "train"` in `realxray/carmlspine/meta` (md5 split). Use render-only weights, or the cross-validation fold that held these cases out, through `tools/eval_gate.py` `assert_unseen_all`.
3. **Identity:** case134's `ori/` and CBCT still carry a real PatientID. Never copy basenames, header text or private strings into outputs, video overlays or burned-in labels. Key frames by `frame_key` or `case134_sw###`, and run the `CIO.identifiers` scan the export already performs.
4. **Two panel pitches in stored spot poses:** case39 AP and LAT poses were made with the old 300 mm panel (K00 −3891.2 at 1024), while case39 LAT2 and all case134 poses use 307.2 mm (K00 −3800). That is a 2.4% scale mismatch; the sweep poses are all 307.2.
5. **Coordinates:** poses use LPS mm from SimpleITK. A nibabel read of the same NIfTI gives RAS, so negate x and y. `carmlspine_labels.VERSE` is VerSe-native; resolve names through it, not a fixed ostk map.
6. **Corners:** no corner truth exists for C-ArmLSpine. Four corners per level would need 3-D endplate corners, for example OpenSpineToolkit's `ostk.morphometry.level_morphometry`, projected through K/R/t. Beware the ostk canal-closing regression (commit 1b7005c). On obliques, 2-D corners are ill-defined.
7. **Window flicker:** each frame is windowed by its own percentiles. A cine or overlay video may flicker, so consider a fixed per-sequence window.
8. **Pose smoothness:** poses are independent per frame with no temporal smoothing. Expect about 0.7° of jitter around a linear orbit, and more at the lateral extremes. Fitting a smooth orbit would give steadier truth for identity-switch scoring.

## 7. Not found or unknown

- A vendor geometry or projection-matrix file (the template ZIP element is empty).
- The meaning of (0037,0011): 0.69 on case134, 0.86 on case39.
- The cause of the roughly 4° header-to-registered angle offset.
- The case39 TS and SPINEPS voxel counts; I did not load masks on the login node.
- Whether the patients were living or cadaveric.
- Any corner or keypoint annotations.

## reader 2

# Map of the PolyPose generator, the DRR renderers, and what a synthetic flexion-extension cine would need

## Bottom line

- **No renderer exists for flexion-extension or cine.** The parts are there, and a new driver about 150 lines long could join them for a lumbar sequence from a CTSP v11 source:
  - PolyPose warp (`polypose_sample.build_transforms` + `polypose_warp.warp_volumes`);
  - perspective C-arm ray-cast (`deepfluoro_render.raycast`);
  - box projection (`spine_project.project_mask`);
  - frame styling (`device_style.style`).
- **The generator cannot do a cervical sequence.** Every step of it is tied to the pelvis and S1, to CTSP v11 labels, and to a table of lumbar and thoracolumbar range of motion. No label anywhere carries C0 (the occiput).
- **The pipeline has never run from warp to rendered frame.** No PolyPose output has passed the checker. The validation chain was cancelled on 2026-09-23 at 19:24, and its render stage never ran.
- **No code projects vertebral corners from CT.** Every renderer emits boxes only.

## 1. PolyPose generator (repo `spinesurg-ct-nnunet:`, branch L6_Class)

### `tools/polypose_sample.py` (sampler and generator)

CLI (global `--spec`, default `SchwingNet/results/polypose/sampling_spec.json` v2):
- `self-test`, `check-cohort`, `envelope-vs-cohort`
- `draw --case --variant [--collection ctsp]`
- `plan --out [--variants 4]`
- `generate --case --variant --subtype --ct --label --body --bank [--target auto|lo|mid|hi] [--flag-table] [--weights-frame moved|source] [--kernel gravity|invdf:<eps>] [--tag] [--device auto|cuda|cpu] [--sampler-commit] [--polypose-commit]`
  - Exit 0 means a pending row was written; exit 3 means the source was refused.
- `finalize --row --bank`
- `head --bank`

What `draw_variant` produces:
- One static standing/supine sagittal profile per call. It is not a motion arc.
- Segment deltas come from `sampling_spec.rom_deg`, which holds only T10-T11 through L5-S1. Those caps are in vitro (Yamamoto 1989 and Oxland 1992, at 7.5–10 N·m); the spec notes that in vivo motion is about 14° per lumbar joint (Pearcy 1984).
- The table is also at `docs/polypose_segmental_rom.csv`.
- There are no cervical rows.

Reusable functions:
- `plan_from_levels(spec, levels)` gives the mobile segments.
- `multipliers_for(spec, plan, castellvi)` returns `(mults, junction_seg, fused_segments)`. Castellvi III/IV gives exactly 0.0; II gives 0.45.
- `_seg_caps(spec, seg)` returns `{flex, ext, lb, ar}`.
- `rekey_body_mask(body, label, LMAP)` re-keys SPINEPS bodies to release ids by overlap.
- `centroid_S1_slab(label, affine, LMAP)` finds the hinge at the top of the sacrum.

`build_transforms(label, affine, LMAP, chain, segments, fused_names, debris_ids)` returns `(T{label_id: 4x4}, bodies[(ids, T, name)], facts)`:
- `segments` has the form `{"L4-L5": {"flex_ext_deg","lat_bend_deg","axial_rot_deg"}}`.
- Each segment is one rotation vector about world +x/+y/+z. World here is the file's RAS mm from the nibabel affine.
- The hinge is the midpoint of the two vertebral centroids; for a segment ending at S1 it is the S1 slab centroid.
- The chain is composed from the fixed pelvis upward.
- Positive `flex_ext` means extension (lordosis-increasing).
- Ribs move with T_n, lumbar ribs with L1, debris with the nearest body.
- Hardware ids 62–68, or any unknown id, cause a refusal.

What `cmd_generate` refuses:
- A label scheme that is not v10/v11, or one where id 29 is present.
- Hardware labels.
- A source whose PI/SS/LL are unmeasured.
- A source failing `plate_sane`.
- A lumbar chain that is not contiguous.
- A declared subtype that disagrees with the chain the labels make.
- A fused read where the fused vertebra has no label of its own.
- A body mask whose grid or affine differs from the label's.

What `cmd_generate` writes, under `<bank>/`:
- `volumes/<rid>_{ct,label,body_msk}.nii.gz`: on the source grid with the source affine, never reoriented. The CT is rounded to integer HU when the source is integer.
- `fields/<rid>_field.npz`: `disp` (3,X,Y,Z) in voxels, a pull-back where source_voxel = output_voxel + disp.
- `drr/<rid>_{ap,lat}.png`: parallel projections only.
- `pending/<rid>.json`: includes `applied_transforms` and `bodies`.
- `rid` is `pp_<coll>_<case>_v<NNN>`.

### `tools/polypose_warp.py`

- `centred_affine(ct_path)` returns `(A_c, iso)` via torchio.
- `warp_volumes(ct_np, label_np, body_np, affine, A_c, spacing, bodies=[(ids, T_world)], frame="moved", chunk=1<<22, device="cuda", kernel="gravity")` returns `{ct, label, body, disp, fov_out, facts}`.
  - It is scheme-agnostic and is the reusable core.
  - The CT is sampled with a cubic B-spline; labels and masks by nearest neighbour.
  - Anything pulled from outside the source grid becomes -1024 HU / label 0.
- `verify_equivalence(ct_path, label_path, bodies_T, affine, crop_centre_vox, size=64, device, tmpdir, kernel)` gates at 1e-3 voxel against the real `polypose.warp.PolyRigid` class.

### Checker v4: `tools/polypose_invariants.py` (`CHECKER_VERSION = "polypose-invariants/4"`)

CLI:
- `--self-test [--keep DIR]`
- `check --bank|--manifest [--shard --n-shards --out --skip-sha]`
- `merge`
- `measure --label`
- `row --row --out`

Fixes introduced in v4:
- Measurement goes through `tools/polypose/measure_sagittal.measure_image`.
- Pairs use the source S1 corridor (`s1_corridor_reference`).
- Endpoints cut by the field of view, and fragments, are excluded.
- Label ids under 200 voxels are treated as debris.

Two limits:
- `drr_contrast()` is a parallel projection on a canonical RAS copy, not a C-arm render.
- The checker is shaped around a manifest row (`seed_policy`, `profile_in_envelope`, `lordosis_target` against the request). A sequence frame is not a sampler draw, so only the geometric checks carry over: `label_rigidity`, `jacobian_positive`, `pelvis_fixed`, `fused_junction_*`, `field_matches_transforms`.

### diffdrr traps

- **Rigid inverse:** `RigidTransform.inverse()` is the closed-form rigid inverse (Rᵀ, −Rᵀt). It is wrong for a voxel affine that carries spacing and the PIR permutation; on case 0874 it put the field 27 voxels off. `polyrigid_coords` now uses `torch.linalg.inv`.
- **cupy and CUDA bool:** cupy 13.6 cannot take a CUDA bool torch tensor. Pass uint8 (see `polyrigid_weights` EDT and `sample_cubic`).
- **Half-voxel offset:** PolyRigid normalises coordinates as 2x/size−1 with `align_corners=False`, which is a half-voxel offset (`polypose_forward_test.py` T0).
- **Negative focal:** the DeepFluoro packaged pose has a negative focal length, so diffdrr's positive-sdd camera renders behind the source, mirrored (`polypose_drr_diag2/3.py`).
- **Zero padding:** `grid_sample` pads with 0, which is 0 HU, i.e. soft tissue. `render_physics_drr` shifts HU by +1000 to avoid this.
- **Scope:** diffdrr is not used by any training-data renderer. It appears only inside `polypose_warp` and the `reg_*` / `polypose_drr_diag*` tools.

### State on the grid (`/rs/rs_grp_oschome/go2432/data/polypose/`)

- **Container and env:** `sif/polypose_base.sif` and `env/venv`, run through `slurm/polypose_env.sh` `pp_run --nv $PP_PY`.
- **`validation/bank_gravity`:** 36 volume files (12 outputs), 7 pending rows, 0 filed.
- **`validation/bank_invdf1`:** 33 volume files, pending rows, 0 filed.
- **`smoke/manifest_failed/pp_ctsp_0874_v000.jsonl`:** failed 5 checks under the checker before v4.
- **Validation chain:** gen 40425419 / fin 40425420 / render 40425421 / collect 40425422. The gen tasks were cancelled 2026-09-23 19:24, and `validation/render/` does not exist.
- **Timing per output:** 192 s on GPU (0874), 427–475 s for 0244/1065.

## 2. DRR renderers

### (a) Parallel lateral: `tools/make_drr_dataset.py`

CLI: `--src <dir with scan-*/*_msk.nii.gz + *_ct.nii.gz, or labelsTr/imagesTr> --dst <dir> [--scheme verse|ds813] [--body-mask-dir] [--png] [--prefix] [--cases] [--resume] [--hu-floor] [--path|--path-only|--paths2-only] [--ct-root] [--respace]`

Behaviour:
- Reorients to PIR in memory (`to_pir`).
- Renders bone only (150–1800 HU); the tool itself says this is not what a radiograph looks like.
- Produces the lateral view only.

Outputs:
- `img/<case>.npy`: uint8, rows run superior to inferior, columns anterior to posterior, so anterior is on the left.
- `ann/<case>.json`: `{case, shape, axcodes, mm_per_px_row_si_col_ap, levels{id:{name, box[x0,y0,x1,y1], pixels, centroid, outline_box?, box_convention}}, overlap_px, union_px, box_convention, n_levels_with_body_box}`.
- `--paths2-only` writes `path2/<case>.npz` with `water_cm` and `bone_cm` (float16), which are the inputs to `device_style`.

Schemes:
- `--scheme verse` uses VerSe ids (C1–7 = 1–7, T1–12 = 8–19, L1–6 = 20–25, sacrum 26, T13 28). This equals CTSP v11 for vertebrae.
- `ds813` is the old Dataset813 map.

### (b) Perspective C-arm, used for the training corpora

`deepfluoro_render.raycast(d, down=4, step_mm=1.0)`:
- Input `d = {K, ext, T, nr, nc, vol(z,y,x) HU in patient LPS, org(x0,y0,z0), sp}`.
- Returns `(trans, water_cm, bone_cm, hit, trunc)`.
- Runs on CPU with scipy, trilinear sampling, polyenergetic with 6 energies.

`spine_project`:
- `load_lps(path)` does `as_closest_canonical` and flips x/y to LPS.
- `centroid_mm(mask, org, sp)`.
- `project_mask(mask, org, sp, M, K, down, nr, nc, step=2)` returns `{box (min/max of projected voxels inside the detector, downsampled px), inside}`, with `M = ext @ inv(T)` and `uv = K·p / z / down`.

`pose_arc`:
- `arc_pose(anchor, lat, tilt, roll, jitter_mm)` rotates about the isocentre and reads the angles back.
- `angles_of(pose)`: lat 0 = AP (source posterior); −90 = the real Surgio lateral, with the source at the patient's right.

Pose pools:
- `/rs/.../data/devcorpus/poses/{cios_fusion,surgio_b51_dr,elekta_xvi}.json`, plus the `*_arc` / `*_low2` variants, and `devcorpus_arc/poses/`.
- Surgio: 296 real registered poses (148 cases × AP/LAT), 2048², 0.15 mm, K fx = −7782.4. Keep the sign.

`tools/devcorpus_build.py`:
- CLI `poses|render|style|lists`; `render` draws a random pose and target per subject.
- It uses TotalSegmentator v3 subjects from `~/model_night/ts_clean_subjects.txt` (142).
- Its `LEVELS` list is T1–L6 plus sacrum: **no cervical**.
- It skips any subject without a sacrum or with fewer than 6 masks.

`device_style` (the styling step):
- `sample_terms(dev, n, rng, cond={"thickness_cm"})`.
- `style(water, bone, hit, dev, t, rng, pitch_mm, field=None, RP=None, window_region="field")` returns `(uint8, field)`.
- Cards live in `docs/devices/`. **`surgio_b51_dr.json` and `varian_halcyon.json` exist only in the grid working tree**, not in git or the local checkout.

### (c) `tools/render_physics_drr.py`

A GPU ray-march that gives exact perspective silhouettes (maximum along the ray). The pose is drawn at random inside `render()`, so it cannot drive a sequence without editing.

## 3. How labels reach 2-D

Names:
- From label ids through the VerSe map (`make_drr_dataset.LEVEL_NAMES`, `make_anchor_drr.VERSE`), or from TotalSegmentator filenames.
- The string forms differ: `"L3"` in the `ann` files, `"vertebrae_L3"` in the devcorpus and arc meta files.

Boxes:
- Parallel: the silhouette via `any()` along the beam.
- Perspective: the min/max of projected voxel points (`spine_project`), or 2nd–98th percentiles (`carmlspine_labels.box_of`).
- Body boxes (the convention set on 2026-09-23) come only through `--body-mask-dir` (SPINEPS bodies) and through `carmlspine_labels` / `case134_sweep`.
- **`devcorpus_build` and `arc_angle_set` box the whole vertebra** from TotalSegmentator masks.
- YOLO class ids: 0 = vertebra, 1 = sacrum.

Body masks:
- `/rs/.../data/spineps/bodies/{CTSP,TS,TSV3,VERSE}_<case>_body_msk.nii.gz` plus `_body.json`.
- Roughly 801 CTSP, 1,144 TS, 1,616 TSV3 and 374 VerSe (half the file counts on disk).

Corners:
- No code projects CT-side corners.
- The detector in `level_prototype.py` (`detector_v5z_final`) is keypoint-to-box, trained on film corners with slots x1..x4 / y1..y4. The slot order is defined outside this repo.

## 4. Existing sweeps and sequences

1. **Angle sweep** (`tools/arc_angle_set.py`), output at `/rs/.../devcorpus_arc/anglesweep_unseen/`:
   - 40 held-out TotalSegmentator subjects × lat −90..+90 in 10° steps × tilt {−15, 0, 15}.
   - Cards surgio_b51_dr and elekta_xvi, 2,280 frames per card, anchor `case29/AP`, L3 at the isocentre.
   - Each frame's meta holds `{subject, lat_deg, tilt_deg, roll_deg, card, target, rot180, thickness_cm, trunc_frac, img_px, boxes[{cls, name, box, inside}]}`, with no K and no pixel spacing.
   - The spine is rigid; only the C-arm rotates.
   - Style terms and `rot180` are redrawn for every frame, so as a cine it flickers and can flip 180°.
2. **case134 spin** (`tools/case134_sweep.py`, `headers|pose|export|score`):
   - Output at `/rs/.../realxray/carmlspine_sweep`: 302 real XA frames, each posed by header plus 2-D/3-D registration.
   - Truth is body boxes; `level` is null on every vertebra and the sacrum was dropped, so this scores detection only.
   - case39 is not covered by any tool.
3. **Serial sweep** (`tools/sweep_map.py`, "sweep_v3"): frames stepped craniocaudally and cut from one long parallel DRR. There is no pose change and no parallax.
4. **Oblique banks** (`make_oblique_drr.py`, which made `~/verse_drr_obl{,2}` and `~/ctsp_drr_obl{,2}`): **the tool is lost.** It is not in git history and is no longer in the grid working tree; only its outputs remain.
5. **`tools/polypose/validation_render.py`** (driven by `slurm/polypose_validate_render.sh`): renders a source and its warped copies with one card and one exposure (terms fixed, `rot180` False, field all ones, a fixed noise seed). It is the template for rendering many frames of one case consistently, and it has never been run.

## 5. Labelled CT on the grid

| Set | Location | What it holds | Cervical |
|---|---|---|---|
| CTSP v11 | `~/data/CTSpinoPelvic1K/{ct,labels}/NNNN_{ct,label}.nii.gz` (802); map in `dataset_labels.json` | Abdominopelvic field; thoracic starts around T8–T10; no T13 labels | None |
| TotalSegmentator v3 | `~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300/<sid>/{ct.nii.gz, segmentations/*.nii.gz}` | Per-structure masks, including `vertebrae_C1..C7`, `skull`, `sacrum` | Of 1,170 renders: 219 have C2, 618 have C7 |
| VerSe raw | `~/VerSeFusion/data/unified/scan-*/<id>_{ct,msk}.nii.gz` (375 scans), VerSe ids | Whole-spine or regional | Of 387 renders: 89 have C1/C2, 142 have C7, 193 have T1; none have C0 |

- **Leakage:** most TotalSegmentator, CTSP and VerSe renders were seen by the level encoder. The held-out subject list is `/rs/.../or_ready/eval_gate/arc_unseen/subjects.txt`; `tools/unseen_cases.py` and `tools/eval_gate.py` do the checking.

## 6. Minimal code path for (c): lumbar, from a CTSP v11 source

1. **Inputs**, as in `slurm/polypose_validate_gen.sh`:
   - `CT=~/data/CTSpinoPelvic1K/ct/<c>_ct.nii.gz`
   - `LAB=.../labels/<c>_label.nii.gz`
   - `BODY=/rs/.../spineps/bodies/CTSP_<c>_body_msk.nii.gz`
2. **Setup inside the container.** Reuse `cmd_generate` steps 1–3 and 5–6: the scheme and hardware checks, chain and debris, the flag-table Castellvi read, `plan_from_levels`, `multipliers_for`, `_seg_caps`, and `rekey_body_mask`.
3. **Replace `draw_variant` with a deterministic phase** a_k in [−1, 1] for each frame:
   - `segs[s] = {"flex_ext_deg": (a_k*ext if a_k > 0 else a_k*flex) * m * frac, "lat_bend_deg": 0, "axial_rot_deg": 0}`.
   - A fused segment stays exactly 0.0.
4. **Per frame:**
   - `build_transforms(...)` to get `T` and `bodies`.
   - `PW.warp_volumes(ct, lab, body_rk, affine, A_c, zooms, [(b[0], b[1]) for b in bodies], frame="moved", device="cuda")`.
   - Run `verify_equivalence` once per sequence.
   - Write the result with the source affine.
5. **Render in the fluorogen env:**
   - Load the warped CT the way `spine_project.load_lps` does.
   - Pose: the Surgio `*/LAT` pose, or `PA.arc_pose(AP_anchor, -90)`.
   - Compute `org_new` once from frame 0's target centroid and hold it fixed across frames; re-centring each frame would make the pelvis appear to move.
   - `DR.raycast(d, down=2)`.
   - `DS.style` with `t`, `field` and `rot180` fixed per sequence.
6. **Ground truth per frame:**
   - Body boxes from `project_mask` on the warped body mask. The exact alternative: move the source body-mask points by `T[id]` (RAS), convert to LPS, then project through M and K.
   - Record names, `inside`, K, M, and the pixel spacing after the resize to 1024.
   - Corners need new code, e.g. body corners from `ostk.spine.endplate_from_label`, projected the same way.
7. **Cost:** the warp takes about 3–8 min per frame; the ray-cast about 1 min per frame per view on CPU (`arc_angle_set` needs about an hour per subject). A 60-frame cine (4 s at 15 fps) is therefore about 3–8 h.

**Cervical has no path.** It is blocked by:
- the v11-only scheme check;
- the chain hinged on S1;
- a range-of-motion table with no cervical rows;
- `plate_sane` and the CTSP-only flag table;
- the devcorpus `LEVELS` list and the sacrum requirement, which drop cervical subjects;
- the absence of any C0 label;
- VerSe having no skull label, so the head would be smeared by the blend rather than moved rigidly. TotalSegmentator does have `skull.nii.gz`.

## 7. Things that will break

- **VerSe masks through ostk:** `ostk.labels.detect_scheme` on a raw VerSe mask returns **"v4"** whenever T2–T5 are labelled, because ids 9–12 are the v4 hip and femur ids. T3 would then read as "left_hip". Use the fixed VerSe map for VerSe masks.
- **Frames:**
  - PolyPose works in RAS (nibabel).
  - `spine_project`, `devcorpus` and `pose_arc` work in patient LPS with arrays indexed (z,y,x).
  - `carmlspine` uses SimpleITK LPS.
  - `load_lps` drops any obliquity in the affine.
- **Image orientation:**
  - `make_drr_dataset` lateral: anterior on the left.
  - Checker PNG lateral: anterior on the right.
  - Device frames: flipped by the card's `rot180` share.
  - `carmlspine`: turned by `rot90` to put the head up.
- **Pixel spacing:**
  - `make_drr_dataset` spacing is at the isocentre, with no magnification.
  - The perspective `px_mm` is at the detector (SID/SOD of about 1.2–1.5) and is rescaled by the resize to 1024.
  - The arc meta files have no spacing at all.
- **Styling:** `style()` draws the window jitter, black level and noise from one rng. It cannot give independent quantum noise per frame with a fixed window without a code change; the fixed-seed approach gives frozen noise instead.
- **Field of view:** voxels pulled from outside the source grid become air, which puts a wedge at the top of a flexed CTSP volume. In the smoke row, AP spine contrast fell from 1.52 to 0.90.
- **Pelvis:** the pelvis is fixed by construction, so there is no lumbopelvic rhythm.
- **Body-mask guard:** `make_drr_dataset.body_mask_for` calls `spineps_ids.body_source_ok`. For a staged or warped body mask with no `<stem>_body.json`, `find_ctd` returns None and a `SpinepsIdError` is raised and not caught, so the run aborts. This is predicted from the code; the render stage that would hit it has never run.
- **Inconsistent box conventions:** whole vertebra versus body, min/max versus percentile, `MIN_PIX` 60 versus `inside` of at least 2% or 50%.

## 8. Not found

- Any flexion-extension, cine or tracking renderer.
- Any CT-side corner projection.
- A cervical range-of-motion table, or any C0 label.
- `make_oblique_drr.py`, which is lost.
- Any certified PolyPose output.
- Any tool for case39's CBCT sweep.

## reader 3

**Existing evaluation code to reuse for the cine harness and both demos (spinesurg-ct-nnunet, branch L6_Class, read-only survey, 2026-09-26)**

## Summary
- **Bournemouth file:** no code in the repo reads the BORDaR `.mat`. The only copy is in this session's scratchpad: `laptop-scratchpad:bournemouth\Cervical_Database.mat`, next to `README.pdf`, plus `..\scratchpad\bordar385_README.rtf`. It is not on the grid.
  - `spinesurg-ct-nnunet:docs\BOURNEMOUTH_DATA_REQUEST_DRAFT_2026-09-26.md` says "the corner tracks are already on disk; see the harness README". That README does not exist.
- **Matching, metrics, overlays and demo (b):** these largely exist, but each script has its own copy. There is no shared module; `iou()` is re-implemented in about 30 files.
- **Temporal tracking:** none exists. There is no Kalman, ByteTrack, identity-switch or MOT code, and no `model.track` call. Nothing in the repo writes video; ffmpeg is used only to extract frames from YouTube.
- **Demo (b):** already built for case134 by `tools/case134_sweep.py`, for detection only. case39's sweep has never been posed or exported, but case39 has agreed level names, so naming can be scored on it.
- **Demo (c):** the pieces exist (sampler, warp, renderers, style, the validation scorer), but there is no motion-trajectory code. The PolyPose validation banks have **0 finalised manifest rows**.

## 1. BORDaR `Cervical Database.mat` (loaded here with scipy)
- **Format:** v5 MAT (`MATLAB 5.0 MAT-file ... 2024-06-27`). Read it with `scipy.io.loadmat(p, squeeze_me=False, struct_as_record=False)`; h5py and mat73 are not needed.
- **Fields:** `Database[0,0]` has `ImageEvent, Sex, Age, PatientOrControl` (126×1), and `Templates, MachineAngle, Dose, orientation` (126×2). Column 0 is flexion (angle about −0.2 to +51°), column 1 is extension (0 to about −57°).
- **Templates:** `Templates[i,j]` is a 9×4 object array: levels C0, C1, …, C7, T1 × 4 points, each `(n_frames, 2)` float64 of (x, y) pixels. x runs 57–955 and y 68–957.
  - y points down: C1 sits near y 390 and C6 near y 700.
  - Every level of one sequence has the same `n_frames` (181–339, median 301).
- **Empty levels are not all `(0,0)`.** Some are `(0,0) uint8` and some `(1,0) float64`, so test `c.size == 0`.
- **Failed frames:** NaN rows are 0.09% of frames, and 0.25% of tracks contain any NaN.
- **Point order (README):** 1 top-left, 2 bottom-left, 3 bottom-right, 4 top-right, defined with the anterior side on the left.
  - `orientation` is L (anterior on the image left) on 226 sequences and R on 26.
  - The data shows the order is anatomical, not image-based: on 25 of the 26 R sequences, points 1–2 are at the larger x. One R sequence does not follow this.
  - So index 0/1/2/3 means anterior-superior, anterior-inferior, posterior-inferior, posterior-superior.
- **Only C3–C6 (and C7 when not hidden by the shoulder) are true four-corner body templates:**
  - C0 is the McGregor line plus two arbitrary points.
  - C1 points mark the marrow cavities, not a body.
  - C2: points 2 and 3 are the caudal corners; points 1 and 4 are arbitrary superior points.
  - T1 (and an obscured C7) have estimated caudal corners.
  - The earlier "score C2–C6" plan should become: C3–C6 full boxes and corners, C2 caudal corners only, C0 and C1 excluded.
- **Frame alignment is not guaranteed.** On 87 of 252 sequences, `MachineAngle` is 1 to 59 frames longer than the templates. Template row k is therefore not provably cine frame k, which is question 2 in the email.
- **Other unknowns:** pixel spacing is not in the file (C3 endplate length median 54 px). The coordinates are probably MATLAB 1-based, a 0.5–1 px offset; the README does not say.
- **Patient keys:** `ImageEvent` HV01a and HV01b are the same person (a = baseline, b = 4-week follow-up). There are 63 people over 126 events.

## 2. The detector and level namer to run
- **Entry point:** `spinesurg-ct-nnunet:tools\level_prototype.py` (one image in, every vertebra named).
  - `--image <file|dir|glob> --out DIR [--detector PT] [--model PT] [--head PT] [--no-orient] [--boxes-dir METAS] [--box-detector YOLO] [--dump-posterior] [--flag] [--conf 0.35] [--abstain-below 0.5] [--hist-match ~/films_drr]`
  - Output per frame: `<stem>.json` = `{image, preprocess{rotation_k, rotated, hist_matched}, direction_known, boxes, det_conf, hw_boxes, width, height, sacrum_box, vertebrae:[{box, det_conf, level, level_prob, single_crop, single_crop_prob, top3, entropy, region, abstain, posterior?}], transitional_flags}`
  - Also writes `<stem>_overlay.png`, `prototype_meta.json` (the eval-gate verdict) and `prototype_results.json`.
- **Models the paper reports** (all present on the grid):
  - Detector: `~/FluoroCap/detect_v5z_final_best.pt` (sha 797de71a…, conf 0.35).
  - Encoder: `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt`.
  - Heads: `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha0.3_seed{0,1,2}.pt`, each with an `.arch.json`. `slurm/sweep_cns.sh` uses these.
  - For C-arm frames there are also YOLO box detectors (pooled, lodoA, lodoB, real_lodo, used in the case134 score).
- **Traps in running it on a cine:**
  - The defaults are **wrong for this work**. `--model` resolves to `allspine_v2_r1` (a deleted, leaky bank per NUMBERS.md) and `--head-set allspine_v2`. Pass the v9 encoder and head explicitly, and pass `--flag` with no paths to skip the transitional flags.
  - **Corners are discarded.** Keypoints are reduced to a box at `level_prototype.py:357-362`; `sweep_map.detect_boxes` does the same. Corner error needs a small patch or a second `predict` call.
    - The keypoint order I infer is image-frame TL, TR, BL, BR: `flip_idx: [1, 0, 3, 2]` in `tools/make_zoom_dataset.py:245`, and the AASCE converter's docstring. I did not confirm it on detect_v5z's source labels, so match corners by geometry, not by index.
  - The orientation net can rotate a frame (`rotate(expand=True)`), and the boxes then come back in the rotated frame. Decisions could flip mid-cine. Use `--no-orient`, or back-rotate with `rot_box` in `tools/lstv_eval_score.py`.
  - `load_image` cannot read DICOM. For 16-bit PNG it windows each frame at its own 0.5–99.5 percentiles, so brightness can flicker between frames. The detector expects bone-bright images.
    - The C-arm export used `carmlspine_pose.stored_to_atten` → `carmlspine_labels.window_or`.
    - `prepare_panel` runs with crop and invert off, so geometry is preserved.
  - `--boxes-dir` takes oracle boxes (metas with cls-0 boxes). This scores naming apart from detection.
  - Windows-local Python has no ultralytics (torch is CPU-only), so inference runs on the grid in `~/mambaforge/envs/fluorogen` (ultralytics 8.4.138, pydicom 3.0.2).

## 3. Matching and metrics code to reuse (all in `spinesurg-ct-nnunet:tools\`)
| rule | where | notes |
|---|---|---|
| call centre inside the truth body box and IoU ≥ 0.3, one-to-one, best IoU first | `carmlspine_eval.py cmd_score` | naming scored on agreed levels only. Reports recall_named, exact, within1, region, answered, exact_answered, frame_exact, false_calls, per_level, confusions. Closest template for the per-frame scorer. |
| greedy by descending confidence, IoU ≥ 0.5 per class; not-kept or low-visibility truth ignored and predictions on them removed | `realxray_eval.py` (`sweep_matches`, `load_truth(min_vis)`), `case134_sweep.py cmd_score`, `arc_recall_eval.py` | "prefix-consistent" trick: match once at conf 0.01 and read recall at any threshold |
| greedy by confidence, IoU ≥ 0.5 | `count_from_sacrum_eval.match_pairs` | |
| centre inside and vertical 1-D IoU ≥ 0.4 | `polypose/validation_render.py score_frame`, `lstv_eval_score.score_b` | `score_b` handles rotated prototype outputs |
| centre containment only | `sweep_map.assign_gt` | |
| count-from-sacrum naming with gap abstention | `realxray_eval.name_levels` | |

- **Level orders:** `ORDER`/`REGION` in `carmlspine_eval.py` (T13 = 19.5, L6 = 24.5); `LEVEL_ORDER` in `make_context_crops`.
- **Eval gate** (`tools/eval_gate.py`): every scorer must carry it — `EG.add_args(ap)`, `EG.assert_unseen_all(items, {role: weights}, where, eval_set=...)`, `EG.block`, `EG.stamp`, `EG.carry_proto(pred_dir, ...)`.
  - A new corpus raises `UnkeyedEvalItem`. Add a `bournemouth` keying rule in `tools/patient_keys.py` (`_REALXRAY_ROOT_CORPUS`, `_REALXRAY_PREFIX`, `PERSON_FORMAT`), with person = ImageEvent minus its trailing a/b.

## 4. Multi-frame and tracking code
- **`tools/sweep_map.py`:**
  - `Namer(model_p, head_p, dev).run(img_u8, boxes)` returns `(emb, p_single, p_blend)`. The per-body embeddings could serve as an appearance cue for re-identification across frames.
  - `repair_boxes(boxes)` merges duplicate boxes and fills interior gaps using the local pitch.
  - `link_pair(...)` pairs bodies between frames using the shift and the embedding cosine.
  - **`ncc_shift` cannot be reused for a cine:** it clamps `dy_hi ≤ -0.2·pitch` (line 1000), a sweep's forced cranial step, so near-zero inter-frame motion is outside its search window. Only `_ncc` and `_ncc_table` carry over.
- **`tools/acquisition.py`:**
  - `GuidanceEngine.ingest(frame)` assumes discrete commanded steps along a sweep.
  - `FiducialBoard.project(frame)` re-projects a marked level through a panorama registration with stale and ambiguous flags. Its "does not blink out" policy is a useful model for track persistence.
- **Other sweep tools:** `tools/fiducial_walk.py`, `tools/validate_guided.py`, `tools/guided_console.py` are all sweep-protocol simulations, not cine.
- **Solvers:** ultralytics trackers are shipped (`cfg/trackers/bytetrack.yaml`, `botsort.yaml`, …), but **`lap` is not installed** in fluorogen, so `model.track` would try a pip install at run time. `scipy.optimize.linear_sum_assignment` (scipy 1.17.1) is available and used nowhere in the repo.

## 5. Overlays and video
- **Overlay code:**
  - `level_prototype.py:437-463`: green boxes, red for abstained, "L4 0.93?" label and flag lines, saved as `<stem>_overlay.png`.
  - `realxray_eval.py --draw N --draw-dir D [--needle L4]`: truth in thin green, calls in red.
  - `case134_sweep.overlays` and `sheet` (contact sheet).
  - `render_level_overlay.py` and `drr_register.overlay_png`.
- **Video tools by location:**
  - **Local (Windows):** no ffmpeg on PATH. Python 3.12 has imageio 2.37.3 and imageio_ffmpeg 0.6.0 (bundled `...\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe`), and cv2 5.0.0.
  - **WSL:** `/usr/bin/ffmpeg` 6.1.1.
  - **Grid:** `~/mambaforge/envs/fluorogen/bin/ffmpeg` 8.1.2 with libx264, libopenh264, libvpx-vp9 and gif, plus cv2 5.0.0 built with FFMPEG. imageio is present but imageio_ffmpeg is missing.
    - The login PATH has `/wsu/el7/pre-compiled/python/3.7/bin/ffmpeg` 4.0.2.
    - The spineps env has imageio only, no cv2.
  - **Recommendation:** pipe frames to the fluorogen ffmpeg, or use `cv2.VideoWriter`.

## 6. Demo (b): C-arm CBCT spins
- **case134 is done:** `tools/case134_sweep.py headers | pose --shard i --n-shards n | export [--window-region] | score --weights name=pt ...`.
  - Outputs: `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep/{images/test, labels/test, meta, qc, summary.json}` (301 frames, 1,204 kept body boxes); poses in `/rs/rs_grp_oschome/go2432/data/carmlspine/sweep/pose`; scores in `/rs/rs_grp_oschome/go2432/data/or_ready/arc/case134_sweep/` (pooled body recall 0.936 at conf 0.25).
  - The score JSON lacks the `weights` and `held_out_by_arm` fields, so it predates the current gate. case134 entered the carmlspine train split on 2026-09-23, so pooled may not be held out; re-score it.
  - It is **detection only**: levels are null because VERIDAH read C1–C5 on this lumbar CBCT. The sacrum was dropped as a 1,431-voxel fragment, and the TS L1/L2 duplicate was dropped.
  - Each meta records `angle, lat_signed_deg, px_mm_detector 0.3, pose{K, R, t, edge_ncc, margin, from_header}`. K's `fx` is −3800 (a mirrored x); leave the sign alone.
  - Truth boxes are the 2nd–98th percentile of the projected points (`carmlspine_labels.box_of`), not min/max.
  - The headers are not an exact mapping: `PositionerPrimaryAngle` is quantised and not monotone (step median 0), and refined poses differ from the header start by a median 4.4° and 58.5 mm. Registration places each frame (edge NCC median 0.33).
- **case39 is not done.**
  - Its 301 projections sit in `.../unpacked/C-ArmLSpine/case39/CBCT/` as UID-named `.dcm` files interleaved with the CT slices. `sweep_files()` keeps only `Modality == "XA"`, but a basename sort is not trustworthy here; order by the DICOM instance number or acquisition time (I did not verify which tags exist).
  - What exists: `nifti/case39_cbct.nii.gz`, TS masks (T9–L5, sacrum), SPINEPS and VERIDAH masks, spot-frame poses, and `pose/consensus.json`.
  - `levels.json` gives agreed L2–L5 and S (L1 disagrees), so naming is scorable.
  - `case134_sweep.py` hardcodes `CASE`, `ORI`, `SW`, `OUT` and `OR` at module level. Parameterise it rather than copying it; the pose stage needs a GPU.

## 7. Demo (c): synthetic flexion-extension cine
- **Sampler:** `tools/polypose_sample.py draw | plan | generate --collection ctsp --case --variant --subtype --ct --label --body --bank | finalize`.
  - It draws static standing profiles (targets lo/mid/hi); there is no time trajectory.
  - It is **ctsp-only** (`patient_key ctsp_release/<case>`) and thoracolumbar only, so no cervical cine.
  - Segmental flexion/extension caps are in `SchwingNet/results/polypose/sampling_spec.json:rom_deg`.
- **Warp:** `tools/polypose_warp.py warp_volumes(...)` runs about 3 min per output on an L40S and about 10 min on CPU. A 150-frame cine with a full warp per frame is about 7.5 GPU-hours.
- **Renderers:**
  - `tools/make_drr_dataset.py`: **parallel, lateral only** (sum along L-R); boxes are silhouette extents with no corners.
  - `drr_register.Renderer(mu, A, dev).render(K, R, t, H, W)`, `deepfluoro_render.raycast`, `render_physics_drr.render`: perspective.
  - Projection: `spine_project.project_mask`, or `carmlspine_labels.project(K, R, t, pts)` + `box_of`.
  - Style: `device_style.load_device`, `sample_terms` and `style`.
  - Arc poses: `pose_arc.arc_pose`.
- **Template chain:** `tools/polypose/validation_render.py stage | style | score`, driven by `slurm/polypose_validate_render.sh`.
- **Exact corners:** no code emits these yet. The route is 3-D body corners (ostk morphometry) moved by each body's rigid transform, then projected.
- **Banks are not finalised:** `/rs/rs_grp_oschome/go2432/data/polypose/validation/bank_gravity` has 36 volumes, 7 pending and 0 manifest rows; `bank_invdf1` has 33 volumes, 2 pending and 0 rows. There is no `render_scores.json`.
- **Held-out source:** only **1 of 802 CTSP** cases is unseen by the v9 chain, `CTSP_COLONOG_378` (`~/model_night/sweep_v3/cns/unseen_v9.txt`). The detector's own lineage also needs gating.

## 8. Where new files should go
- `tools/bournemouth_qf.py` (`export`, `self-test`): writes the shared real-X-ray layout (`docs/REAL_XRAY_DATASETS_SPEC.md`: `images/`, `labels/`, `meta/`, `splits.json`, `qc/`, `summary.json`) under `/rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf/`.
  - Meta per frame should carry corners, boxes, level, template row, event, flexion/extension, orientation and the `MachineAngle` offset. Copy the `.mat` to the grid first.
- `tools/cine_eval.py` (`score`, `track`, `video`): reads `level_prototype` outputs plus a meta directory, stamps the eval-gate block, and uses scipy for assignment.
- case39: parameterise `tools/case134_sweep.py` (or add `tools/carm_sweep.py`).
- `tools/polypose/cine_render.py` for the synthetic cine.
- `slurm/cine_eval.sh`, `slurm/carm_sweep_case39.sh`, `slurm/polypose_cine.sh`:
  - Submit with `sbatch -D ~/spinesurg-ct-nnunet`, fluorogen env.
  - GPU partitions `gmsap`/`gvohp`/`galhp` with `--qos=gpu`; CPU work on `reqp` with `--qos=requeue`; TMPDIR under `/dev/shm`.
- Register the new stages in `tools/pipeline_state.py`, as the repo's CLAUDE.md requires.
- Put the harness README under `docs/`.
- `SchwingNet/tools` only if the work becomes a paper figure.

## Not found or unknown
- Bournemouth pixel spacing, and whether template row 1 is DICOM frame 1.
- DICOM polarity of the Bournemouth cine.
- detect_v5z's keypoint order, not confirmed on its own labels.
- The DICOM tag that orders case39's frames.
- Whether the v9 namer is accurate on cervical cine; nothing measured was found.
- Whether case39 or case134 are held out for v9 or for the C-arm detectors; the gate decides this at run time.
- No MOT or identity-switch metric code exists anywhere in the repo.