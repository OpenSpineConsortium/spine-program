# Bournemouth cervical quantitative fluoroscopy: the cine harness

Written 2026-09-26. The build plan is `docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md` (sections 1b and 2). The images have
not arrived: the corner truth is exported, and the harness has been tested on it and on painted and synthetic-DICOM
stand-ins. No model has run on a Bournemouth frame, and no Bournemouth score exists.

What a score here will mean: **agreement with the authors' semi-automatic template tracker**, frame by frame and over
time, on 252 lateral flexion and extension sequences of 63 people. It is not accuracy against independent hand
labels.

## 1. Where things are

| what | where |
|---|---|
| the release (`Cervical Database.mat`, CC BY 4.0, doi 10.18746/bmth.data.00000385), md5 `aec3d16d031f62c4a4b7725cd5e0a0be` | local `laptop:data\bournemouth_qf\raw\` (outside git, with `README.pdf`); grid `/rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf/raw/` |
| dataset module: loader, `export`, `frames`, `align`, `self-test` | `tools/bournemouth_qf_eval.py` |
| the harness: `score`, `track`, `video`, `self-test` | `tools/cine_eval.py` |
| the tracker's frozen constants | `SchwingNet/results/cine/tracker_config.json` (committed before any Bournemouth frame is seen: stage `cine_tracker_frozen`) |
| grid jobs | `slurm/cine_eval.sh` (CPU `reqp --qos=requeue`; the model-running modes need the GPU flags on the command line) |
| truth, frames | `realxray/bournemouth_qf/{meta/, images/, images_faceL/, meta_faceL/, splits.json, sequences.json, summary.json, frames_summary_<face>.json}` |
| results | `or_ready/cine/bournemouth_qf/<arm>/{pred/<seq>/, track.json, score.json, score_items.jsonl.gz, video/, align.json}`, `<arm>` = `primary` or `faceL` |

`tools/pipeline_state.py` stages: `bournemouth_qf_export` then `bournemouth_qf_frames`, `cine_infer_bournemouth` and
`cine_score_bournemouth`. `bournemouth_qf_frames` waits on `cine_tracker_frozen`.

## 2. What the truth is

`Database.Templates[i, j]` is a 9 x 4 cell array: rows C0 ... C7, T1, four points each, and each cell an
(n_frames, 2) array of (x, y) pixels with y pointing down. `j = 0` is flexion and `j = 1` is extension. The points
are **anatomical, not image-based**: 0/1/2/3 = anterior-superior, anterior-inferior, posterior-inferior,
posterior-superior. On 226 of 226 L sequences and 25 of 26 R sequences, the corners put the anterior wall on the side
the file's `orientation` says. The exception is `HV09a_ext`, which the export records as disagreeing and does not
correct.

Counts, re-checked by the self-test on every load:

| level | sequences | role in every truth meta | why |
|---|---:|---|---|
| C0 | 48 | ignore | the McGregor line plus two arbitrary points |
| C1 | 249 | ignore | the points mark marrow cavities, not a body |
| C2 | 252 | caudal_only | points 2 and 3 (anatomical 1, 2) are the caudal corners; 1 and 4 are arbitrary |
| C3-C6 | 251 / 252 / 251 / 247 | score | four-corner body templates: **the primary number** (`--level-group primary=C3,C4,C5,C6`) |
| C7 | 50 | score, reported apart (`c7`) | may be an estimated caudal corner under the shoulder |
| T1 | 7 | ignore | estimated caudal corners |

- **Scale.** 126 events (HV01a ... P##b), 63 people, 252 sequences, 73,305 template rows (181-339 per sequence).
  `tools/patient_keys.py` keys HV01a and HV01b to one patient, HV01.
- **Missing levels.** An absent level is an empty cell, `(0, 0) uint8` or `(1, 0) float64`, so the loader tests
  `c.size == 0`. No level is ever partly empty.
- **Failed frames.** 472 of 467,369 level-frames (0.10 %) are NaN rows. Each is a whole level on one frame, and no
  two fall on the same frame, so 472 of 73,305 frames (0.64 %) lack one level. The plan's "0.09 % of frames" is the
  level-frame rate. On such a frame the level becomes an `ignore` region, placed at the level's nearest tracked row
  (`missing: "nan_template_row"`, `box_from_row`). A detection there is neither rewarded nor charged, and the level
  is not counted in that frame's temporal ground truth.
- **Truth box** = min/max of the four corners, the same convention as the detector's box (min/max of its predicted
  corners).
- **Coordinates.** `--coord-origin matlab1` (the default) subtracts 1 from x and y. The README does not give the
  origin, and the data request asks.

## 3. Running it

Everything runs through `sbatch -D ~/logs ... ~/spinesurg-ct-nnunet/slurm/cine_eval.sh`, never on the login node. The
header of that script lists every mode.

1. **`export` (can run now).** Use `-J bqf_export`. It writes a copy of the `.mat` to `raw/`, one `meta/<event>_<flex|ext>_f####.json` per
   template row in the cine schema, `splits.json` (every event is test), `sequences.json` and `summary.json`.
   - Per frame: `view LAT`, `px_mm null`, `template_row k`, `frame = k + offset`, `machine_angle_deg` (MachineAngle
     row `frame`), `orientation`, `facing` (from the corners), `offset_status "unverified"`.
   - A local test export (2026-09-26, into scratch, not kept) wrote 73,305 metas and reproduced every count above.
2. **`frames`, when the DICOM arrives.** Run with `-J bqf_frames --export=ALL,DICOM=<dir>[,DICOM_MAP=<csv>]`. It needs pydicom
   (fluorogen env).
   - **Mapping.** Each file maps to a sequence through a `--map` CSV (`path,event,motion`) or, failing that, the
     event id and `flex`/`ext` found in its relative path.
   - **Window.** One window per sequence, never per frame, so nothing flickers. The default is `or`, the realxray
     display ladder (p1/5/50/95/99 -> 27/47/126/216/239), taken over the central 3/4 of 16 frames spread across the
     sequence. The alternative, `pct`, is linear from p0.5 to p99.5.
   - **Polarity** (`--polarity auto`). The displayed brightness is the stored value, negated for MONOCHROME1. Then,
     on up to 5 frames per device (Manufacturer | Model), the mean inside the C4 quad is compared with a prevertebral
     band 0.25-0.75 endplate lengths anterior to it. The polarity is decided once for the dataset and never per
     frame. A split vote is refused: look at the frames and pass `--polarity asis|invert`. The votes are recorded in
     `frames_summary_<face>.json`.
   - **Identity.** Every string in the DICOM identity tags (`carmlspine_io.ID_TAGS`) is checked against every text
     byte written, and only the count is reported. A tag value equal to a public event id is exempt. Any hit exits 3.
   - **Recorded per sequence.** Only numeric and encoding header fields: PixelSpacing, ImagerPixelSpacing, FrameTime,
     CineRate, PhotometricInterpretation, the frame counts. These answer data-request questions. A frame that is not
     1024 x 1024 is skipped unless `--allow-size-mismatch` is passed, because the truth is not rescaled.
3. **Inference.** Use `-J cine_infer_bqf --array=0-251%16` with the GPU flags. It runs one sequence per task:
   `level_prototype.py --no-orient --flag --dump-posterior --dump-corners --conf 0.35` with the three v9 weights, into
   `pred/<seq>/`. It is gated, with no `--not-held-out`: the frames key to `bournemouth:<person>`, so the gate has to
   prove that no model saw them.
4. **Scoring.** Use `-J cine_score_bqf` (CPU). It runs three steps in order:
   - `track` with the committed config;
   - `score --track --corpus-hint bournemouth --bins machine_angle`, with the level groups `primary`, `c7` and `c2`;
   - `video --fps 15`. Set `VIDEO_SEQS="HV01a_flex ..."` to render only some sequences.
5. **`align` (diagnostic only).** For the 87 sequences whose MachineAngle has 1-59 more rows than their templates,
   it reports the mean truth-to-detection IoU at every candidate offset 0 ... (n_ma - n_t). **The applied offset
   stays 0, or becomes the authors' answer** (`--offsets <json>` to `export`/`frames`, which sets
   `offset_status "authors"`). An offset fitted to the detector's own boxes would make the truth agree with the
   prediction by construction.
6. **Secondary arm: facing.** First run `frames --face L` (`--export=ALL,DICOM=...,FACE=L`). It writes the 26 R
   sequences mirrored to `images_faceL/`, with the truth mirrored alongside into `meta_faceL/`. Then run infer and
   score with `ARM=faceL --array=0-25`. Report it beside the as-is numbers for the same 26 sequences, never instead
   of them.

## 4. What `score` reports, and two places where it departs from the plan's wording

The full rules are in the `cine_eval.py` docstring and in every `score.json` (`rules`).

**Matching.** Matching follows the paper scorer: the prediction's centre lies inside the truth box and IoU >= 0.3,
one to one, greedy by IoU. The secondary arm uses IoU >= 0.5. An unmatched prediction whose centre lies in an ignore
box is dropped; any other unmatched prediction is a false positive.

**Metrics.**
- recall per level and precision overall;
- IoU;
- centre error, in px and relative to the truth endplate;
- corner error per slot;
- naming: exact, within one, abstain, exact among answered, frame-exact;
- a confusion list.

Every metric is also reported per `machine_angle` bin (10 degrees wide) and per level group. With `--track` the
temporal metrics are added: CLEAR-MOT identity switches, fragmentation, MOTA, IDF1, and name switches per 100 frames
for the independent and the tracked names.

**Departure 1: the caudal-only (C2) rule.** The plan matches C2 when the predicted inferior edge lies within 0.25
body heights of *the mean y* of the two caudal corners. The C2 caudal endplate drops a median 0.32 body heights
across its width, so under that wording **a perfect C2 box (min/max of its own four points) fails on 13,005 of 73,305
frames (17.7 %)**. It then counts as a miss plus a false positive. In a 4-sequence end-to-end run with 2 px noise,
72 of 73 false positives were correct C2 boxes. The reference is therefore the *lower* caudal corner, which is the
inferior edge a min/max box of the true corners has, and there a perfect box fails on no frame. The plan's version
remains available as `--caudal-ref mean`, and every score records `caudal_ref`.

**Departure 2: a second corner reading.** The plan compares corners slot to slot after re-sorting both sides through
`canonical_slots`, which splits top from bottom by y. That stays the primary number.
- **The problem.** 11.5 % of C3-C7 truth quads have the anterior wall as their two topmost points, and 11.7 % lie
  within 5 px of that split (it is 0.9 % on HV01a flexion, so the problem sits in particular sequences). There, a few
  px of prediction error can hand a corner to the other endplate's slot and charge an error the size of a body edge.
- **The second reading.** `corners.assigned` is the one-to-one pairing of truth and predicted corners with the least
  summed distance.
- **Reported with it.** `corners.slot_vs_assignment_disagree` counts the bodies where the two readings differ, and
  `corners.truth_split_margin_px` gives how close the truth quads sit to the split.
- **Anatomical names** (`corners.anatomical_px`) come from the pairing, because a slot's anatomical meaning is
  itself ambiguous on such a quad.

**The tracker** runs on `tracker_config.json`, with the constants exactly as the plan states them.
- **The gates.** With these values the two association gates reduce to IoU >= 0.1: `cost <= 0.9` is `IoU >= 0.1`,
  so the centre-distance alternative never admits a pair by itself.
- **Age.** A confirmed track dies after round(0.33 x fps) misses, which is 5 frames at 15 fps.
- **Naming.** Every confirmed track, detected or coasting, is sorted by y and its pooled `softmax(logp)` is decoded
  by `fluorocap_anchor.decode`.
- **Caution on the tracked `p`.** It is a pooled score, not a calibrated probability. `logp` sums about ten frames of
  log posteriors, so a steady 0.9 posterior shows as `p = 1.00` (seen in tier 2). The abstain rule's `p < 0.5` limb
  will therefore rarely fire on tracked names; the "decoded differs from the pooled argmax" limb still can.

## 5. Self-test results, 2026-09-26 (Windows, local `.mat`)

`python tools/bournemouth_qf_eval.py self-test --tier 1,2` and `python tools/cine_eval.py self-test` both reported
ALL PASSED.

**Loader.** The md5 matches. The counts are 252 sequences, 126 events and 63 people; per level C0 48, C1 249, C2 252,
C3 251, C4 252, C5 251, C6 247, C7 50, T1 7; orientation L 226 and R 26; 87 sequences with extra MachineAngle rows
(1-59); corner-derived facing agrees with the file on L 226/226 and R 25/26; 472 NaN level-frames.

**Tier 1: metric unit tests.** Predictions were made from HV01a flexion's real truth (316 frames) with known
perturbations. The mirror test uses HV06b flexion (R, 267 frames).

| perturbation | expected | actual |
|---|---|---|
| none | recall 1.0, precision 1.0, FP 0, corner error 0.000, C2 caudal recall 1.0 | same |
| none, oracle track ids | IDSW 0, frag 0, MOTA 1.0, IDF1 1.0 | same |
| every corner shifted by (3, 4) px | corner error 5.000 slot to slot and order-free; C2 on slots 2 and 3 only | 5.000, 5.000 (max deviation 0.0); C2 slots [2, 3] |
| 1.5 px noise | order-free <= slot to slot on every body, and equal where the two pair alike | 0 violations, equal; the slot pairing flipped on 1 of 1,580 bodies |
| drop C5 on frames 10-19 | C5 recall (n-10)/n = 0.9684 (n = 316), frag 1 | 0.9684, frag 1 |
| swap the track ids of C4 and C5 from frame 50 | IDSW 2 | 2 |
| rename every level one step caudal | exact 0.0, within-1 1.0 | 0.0, 1.0 |
| a false box in the C1 ignore region (all 316 frames) | FP 0 | 0 (316 dropped as ignored) |
| a false box below the lowest level, outside any ignore region | FP 1 | 1 |
| HV06b (R) as-is vs mirrored | slot-mapped (k <-> [1,0,3,2][k]) and anatomical corner errors identical | max difference 1.1e-13 over 5,874 errors |
| the real tracker, unperturbed | IDSW 0, frag 0, FN 5 (frame 0: 2-hit confirmation), MOTA 0.9968 | same |
| the real tracker, C5 dropped for 10 frames (max_age 5) | C5 IDSW 1, frag 1 | 1, 1 |

**Tier 2: render smoke test.** The truth quads of HV01a flexion were painted from the `.mat` arrays onto noise at
1024 x 1024, and the overlays drawn through the whole path (metas -> predictions -> tracker -> `video`) were encoded
with the bundled ffmpeg 7.1 (libx264).
- **Checked numerically, on frames 0, 158 and 315.** Every truth box centre lies on a painted quad, every box's top
  edge carries overlay colour in the *decoded* video, and every box centre still shows the quad.
- **Checked by eye.** On the three extracted PNGs the boxes sit on the quads. Frame 0 shows only tentative (white)
  boxes, which is the 2-hit confirmation rule; frames 158 and 315 show track-coloured boxes labelled `t01 C2 1.00` ...
  `t05 C6 1.00`. The HUD shows `frame 158  +59.8 deg`, and the C1 ignore region is drawn grey.

**Tier 2b: the DICOM path.** Two synthetic 6-frame MONOCHROME2 cines, with bone painted dark, went through `frames`:
- **Polarity** `auto` voted 0 of 2 bone-brighter and so inverted; the written PNG has C4 at 239 against a frame
  median of 125.
- **Frames.** All 12 frames were written.
- **Identity.** A fake PatientName reached no text file: 0 hits, and the public event id in PatientID was exempt.
- **Facing.** `--face L` wrote only the R sequence; its image equals the mirrored as-is image, and its C4 box
  satisfies x0' = 1023 - x1.

**Tier 3 (grid only, not yet run).** `slurm/cine_eval.sh smoke` animates CSXA film 0001035 (LabelMe corners: C3-C7
score, C2 caudal-only) through a known +-10 degree rotation plus translation, 150 frames at 15 fps. It then runs
`level_prototype`, `track`, `score` and `video`, declared `--not-held-out` because CSXA patients are in detector and
encoder training. It is the only test of the real detector on cervical anatomy before the images arrive.

## 6. What is not known, and where each answer goes

| unknown (asked in the data request) | the harness until answered | when answered |
|---|---|---|
| is template row 1 cine frame 1; why 87 sequences have 1-59 extra MachineAngle rows | offset 0, `offset_status "unverified"`; `align` shows the IoU per offset without applying one | `--offsets <json>` to `export` and `frames` |
| coordinate origin | `matlab1` (x - 1, y - 1) | `--coord-origin zero` if 0-based |
| pixel spacing; distortion correction | `px_mm null`: errors in px and relative to the endplate | `score --mm-per-px` |
| polarity | `auto`, decided once, a split vote refused | `--polarity asis|invert` |
| facing the detector expects | as-is is primary; mirrored R is a secondary arm | see "not done" |
| the images | none | `frames` |

## 7. Not done

- **The trained-facing check.** The plan says to render 5 training labels from `data/yolo_v4z` before choosing a
  facing default. It was not done (the data is on the grid), so the default stays as-is and the mirrored arm is
  secondary.
- **The ROI-crop 2x secondary arm.** No crop-and-upsample code exists; it needs its own frame directory and stage.
- **Grid export and tier 3.** The export has not been run on the grid (only the local test into scratch), and
  tier 3 has not run.
- **Latency.** `tools/cine_latency.py` is a separate part. `video --latency` reads its `per_frame`.
- **The DICOM layout is unknown.** `frames` was tested only on synthetic single-file multi-frame cines. A real
  delivery as one file per frame is handled (ordered by InstanceNumber) but untested.
