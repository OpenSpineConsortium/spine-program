<!-- Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/README.md [untracked at 097933a (laptop copy of 2026-10-08)] -->
# tools/fluoro_video: fluoroscopy panels cut out of composite videos, by rule

This package finds the fluoroscopic image inside teaching and journal videos, then cuts it out as frame sequences. The sources are split-screen room cameras, presenter insets, and full-frame C-arm captures.

- **Programmatic.** Every crop box and every segment boundary is computed from the pixels. No coordinate, time or box is typed anywhere in code or config.
- **Reproducible.** One config file holds every parameter, and the environment is pinned. Each output carries hashes of what produced it.
- **Transparent.** Each video gets a QC report showing what was chosen, what was rejected, and why.
- **Timed.** Each extracted frame carries its presentation timestamp. Each clip records its acquisition cadence and its playback speed, together with the evidence for that speed. From these you can compute rates of translation and rotation in real seconds.

Private research evaluation only. Frames and clips are never committed and never uploaded anywhere public.

## Contents

| file | role |
|---|---|
| `config.yaml` | every parameter, each with a one-line reason |
| `overrides.yaml` | the only place a person may state a box, time or decision; empty by default |
| `environment.yml`, `explicit_lock.txt` | pinned environment. `explicit_lock.txt` is the full resolved set (URLs and md5s) |
| `cli.py` | `inventory`, `run`, `report`, `determinism`, `synth` |
| `inventory.py` | which files are input videos, decided by rule |
| `decode.py` | sequential PyAV decoding with per-frame pts; ffprobe; VFR test |
| `panels.py` | per-frame panel detection (greyscale, texture, morphology, box refinement, circle fit, scoring) |
| `layouts.py` | clustering of candidate boxes into stable layouts; coarse segments |
| `pipeline.py` | one video end to end (pass A, segments, pass B, clips, timing, writing) |
| `timing.py` | duplicates, cadence, liveness, cuts, replays (pHash), clock fits (Theil-Sen) |
| `ocr.py` | tesseract discovery and reading of on-screen clocks and angles |
| `sourcetext.py` | rates or speeds stated by the source (info.json, description, PMC captions, Commons) |
| `qc.py`, `report.py` | per-video QC report; top-level REPORT.md, manifest.json, clips.csv |
| `synth.py` | synthetic composite videos with known truth, used by the tests |
| `tests/` | unit tests, end-to-end synthetic tests, synthetic determinism test |
| `slurm/` | grid launchers (`env.sh` is sourced by all of them) |

## Running it on the grid

All compute runs through sbatch (partition `reqp`, `--qos=requeue`). The login node only submits jobs.

```
W=/rs/rs_grp_oschome/go2432/data/external/fluoro_video/work     # code copied to $W/code (tools/fluoro_video + docs/)
C=$W/code/tools/fluoro_video/slurm
sbatch -D $W $C/tests.sbatch                                     # must pass
sbatch -D $W $C/inventory.sbatch                                 # -> $W/inventory.json, $W/source_text/
N=$(grep -c '"include": true' $W/inventory.json)
sbatch -D $W --array=0-$((N-1)) $C/run_array.sbatch              # one video per task -> clips/<video_id>/
sbatch -D $W $C/report.sbatch                                    # -> clips/REPORT.md, manifest.json, clips.csv
sbatch -D $W $C/determinism.sbatch                               # two runs on 3 real videos -> $W/determinism/
```

The environment lives at `/rs/rs_grp_oschome/go2432/envs/fluoroclip`. To recreate it exactly, run `slurm/make_env.sbatch`, which does `conda create --file explicit_lock.txt`.

`slurm/env.sh` sets the following for every job:
- single-threaded BLAS/OpenMP, and `OMP_THREAD_LIMIT=1` for tesseract;
- `PYTHONHASHSEED=0`;
- `TMPDIR` under `/dev/shm`.

## The pipeline, step by step

### 0. Inventory (`inventory.py`)

**Which files are videos.**
- A file under `youtube/`, `pmc/` or `commons/` is a candidate when its extension is in `inputs.include_ext`.
- It is an input video when ffprobe finds a video stream with at least `min_video_frames` packets (5) and at least `min_video_s` of duration (1 s). This rule drops the journal-figure GIF thumbnails, which are one frame each. It keeps the 7-frame Commons GIF.

**Viewer transcodes.** A PMC viewer transcode (`-pmcvs_normal`) is dropped only when a sibling original of the same duration (within 1 s) sits in the same folder. The rule that fired is recorded for every file.

**Recorded per input:**
- the input's sha256;
- ffprobe stream and format fields (codec, size, `r_frame_rate`, `avg_frame_rate`, time base, duration);
- the video-level expected region and view.

**Expected region and view.** These are parsed from `docs/FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md` (its ranked table and raw-candidate JSON) by id, then reduced to coarse classes by keyword. They are labels describing the video as the scan saw it, never boxes, and they are not measured per segment.

**Source texts.** These are fetched once and cached in `work/source_text/` with their sha256:
- the PMC article XML from Europe PMC;
- Commons descriptions.

Runs read only the cache.

### 1. Pass A: sampled panel detection (`pipeline.pass_a`, `panels.detect`)

The whole file is decoded sequentially with PyAV. There is no seek, so both passes see bit-identical frames. Every frame's pts is recorded.

**Sampling.** One frame per `1/sample_hz` s of pts (0.5 s) is analysed. It is block-mean downscaled by an integer factor to at most `analysis_max_side` px (1080p: 1/3).

**Per-pixel maps:**
- `grey`: chroma (max − min of RGB) ≤ `chroma_max`;
- `nonblack`: luma > `black_max`;
- `textured`: local std over `texture_window` ≥ `texture_min`.

**From seed to candidate boxes:**
1. **Seed** = grey ∧ nonblack ∧ textured, opened by `open_px` (removes text strokes).
2. **Core** = the seed closed by `close_px` with holes filled. This bridges smooth soft tissue.
3. **Region** = grey ∧ nonblack within `snap_px` of a core component, with holes filled. Box edges then follow the exact greyscale edge.
4. **XY-cut.** A region box is split recursively along full gutters (at least `gutter_min_px` columns or rows with occupancy ≤ `gutter_occ`). This separates AP and lateral images placed side by side.
5. **Edge peel.** While the outer `trim_band` lines of an edge are less than `trim_support` panel-like, that edge is peeled off. Panel-like means grey and (textured or black). The box is then tightened to the region.
   - This step removes room-camera pixels and flat grey bars or frame lines that the closing had joined to the panel.
   - It is why the synthetic boxes come out exact.

**Features and score.** Each candidate gets:
- `purity`: grey fraction of the box;
- `texture`: median local std;
- `entropy`: 64-bin luma entropy;
- `fill`: region fraction of the box;
- `aspect` and `area_frac`.

Score = the mean of the four main features, each mapped linearly from its gate to a typical-fluoroscopy level (`panel.score`). A candidate is accepted when every gate passes:
- `purity_min`, `texture_box_min`, `entropy_min_bits`, `fill_min`, `aspect_range`, `min_area_frac`.

**Round fields.** When `fill` < `circle_fill_max`, a Kasa least-squares circle is fitted to the region boundary. If its RMS residual / radius ≤ `circle_rms_max`, the field is `circle` (an image intensifier), and a fill ≥ `circle_fill_min` passes the fill gate.

**Non-maximum suppression.** A candidate lying at least `nms_contain` inside a better candidate is suppressed.

The top `max_candidates_kept` candidates of every sample are kept, rejected ones included, for QC.

**Also kept from pass A:**
- a whole-frame 64-px thumbnail difference, for the QC plot;
- `ocr_probe_pool` full-resolution greyscale frames spread over the video, as OCR probes.

### 2. Layouts and coarse segments (`layouts.py`)

**Clustering.** Accepted candidates from all samples are clustered with deterministic leader clustering. The distance is Chebyshev over box coordinates normalised by frame size, with threshold `cluster_eps`. Candidates are visited by decreasing score; this is followed by two median-reassignment passes.

**Layout box.** A layout's crop box is the per-coordinate median of its members at native scale; its spread (median absolute deviation) is reported. Layouts with IoU ≥ `layout_merge_iou` are merged. A layout needs at least `min_layout_members` members.

**Membership.** Every accepted candidate belongs to exactly one layout: the one with the highest IoU, which must be ≥ `member_iou`.

**Segments.** A segment is a run of member samples of one layout:
- runs separated by at most `max_gap_s` are merged;
- a run shorter than `min_segment_s` is dropped;
- a run with a member fraction below `min_member_frac` is dropped.

The rule that fired is recorded for every run. Segment ids (`S000`, …) are ordered by start time, then layout.

### 3. Pass B: native-rate crops (`pipeline.pass_b`)

The file is decoded sequentially again. For every frame inside a kept segment's window (from the sample before its first member to the sample after its last), the following are computed:

- **Fixed-box panel score.** The same features and gates as in pass A, applied to the layout box on this frame, give `panel_score` and `panel_present`.
- **Greyscale crop.** BT.601 luma with integer arithmetic, written as a PNG.
- **`d`.** Mean absolute difference from the previous frame, on a ≤ `thumb_side` block-mean thumbnail. The 99.5th percentile is kept as well.
- **Signature.** A 32×32 signature (PIL box filter), its NCC with the previous frame, and its 64-bit DCT pHash.
- **OCR crops.** Crops of the accepted OCR regions, every `ocr_interval_s` of pts.

Downsized original full frames are kept at the QC sample times.

### 4. Boundaries, gaps and cuts (`pipeline.refine_and_split`)

**Start.** The refined start is the first frame of the run of panel-present frames that ends at the first member sample. It is searched at native frame rate between the neighbouring samples. The end is refined the same way.

**Splits.** Inside the segment, clips are split at two things:
- **gaps:** runs of at least `gap_min_frames` frames without the panel (those frames are dropped);
- **hard cuts:** NCC < `cut_ncc_max` together with `d` ≥ `cut_min_d`.

**Short pieces.** A piece shorter than `min_clip_s` is dropped (recorded).

**Rates.** No rate is ever computed across a cut, because each piece is analysed on its own.

### 5. Duplicates, cadence and liveness (`timing.py`)

**Duplicate classes.** For each piece, Otsu's threshold on log10(`d` + 0.01) splits two classes. The split is accepted when all of these hold:
- the lower median ≤ `dup_abs_max`;
- the upper median ≥ `dup_sep_ratio` × the lower median;
- each class has at least `dup_min_class` frames.

The lower-class median is the noise floor, meaning the re-encoding noise of a repeated image.

**No accepted split.** A piece whose median `d` ≤ `dup_abs_max` is static: only jumps greater than max(`dup_abs_max`, `dup_outlier_k` × median) are updates. Otherwise every frame is a new image.

**Key-frame guard.** An update on a key frame that is smaller than `keyframe_guard` × the threshold is relabelled as a duplicate. This is an I-frame refresh of a held image, not a pulse.

**Cadence.** Computed from the update frames (`is_duplicate_of_previous` = 0):
- the histogram of frames per image and its mode;
- the shortest repeating pattern (for example `4` for 7.5 images/s at 30 fps, or `2,3` for 12 at 30);
- the modal and median intervals in ms;
- images per video second = (updates − 1) / (pts span of the updates). This mean rate is robust to alternating patterns; the rate implied by the median interval is reported beside it.

**Liveness.** Measured as the share of 1-s pts windows that contain at least one update:
- at least `live_window_frac`: `live`;
- at most `held_window_frac`: `held`;
- in between: `mixed`.

### 6. Replays (`timing.find_replays`)

Replay detection works on the update images of the whole video, in time order.

**Matching image pair.** A pair (j, i) with i < j matches when both hold:
- the pHash Hamming distance is ≤ `replay_hamming_max`;
- the signature difference is ≤ `replay_rel_max` × the median difference between successive updates of i's clip.

A replayed image is closer to its first showing than two successive pulses are to each other. So live fluoroscopy of still anatomy, where every pulse carries new noise, does not match itself.

**Replay run.** A replay is at least `replay_min_images` consecutive updates matching consecutive earlier updates at a constant offset, starting at least `replay_min_gap_s` after the original run ends.

**Clips.** Clips are split at replay-run boundaries. A replayed clip is marked `replay.is_replay = true`, `replay.of_clip`, `use_for_rates = false`. Only the first showing is used for rates.

### 7. Playback speed (`pipeline.speed_for_clip`)

**Definition.** `speed_factor` is the real seconds per second of video, that is d(clock)/d(pts):
- 2.0 means the video plays twice as fast as reality;
- `real_time_s = (pts_s − pts_s[first frame of the clip]) × speed_factor`;
- `video_s_per_real_s = 1 / speed_factor` is reported too.

The task text wrote `(pts − pts0) / speed_factor` but also defined the speed factor as the clock-vs-pts slope. Those two statements only agree if the factor is inverted. This implementation uses the slope definition and multiplies, and it states the formula in every clip.json.

**Evidence, in order of preference:**

**(a) `ocr_clock`.** An on-screen clock or timer read by tesseract.
- *Discovery.* Tesseract `--psm 11` runs on up to `ocr_probe_frames` probes, taken inside kept segments first. Words matching `h:mm:ss`, `hh:mm:ss` or `mm:ss` are grouped by location (within `ocr_region_tol` of the frame). A region is accepted with at least `ocr_min_hits` hits and at least 2 distinct values.
- *Reading.* Each region is read every `ocr_interval_s` (capped at `ocr_max_per_clip`): scaled to `ocr_target_h` px, Otsu-binarised, made dark-on-light, then read with `--psm 7` and a digits-and-colon whitelist.
- *Fit.* A Theil-Sen fit of clock seconds against pts seconds, using pairs at least `clock_min_pair_dt_s` apart. It is accepted when all of these hold:
  - at least `clock_min_points` readings;
  - an inlier fraction of at least `clock_min_inlier_frac` within `clock_inlier_s`;
  - at least `clock_min_distinct` distinct values;
  - a clock span of at least `clock_min_span_s`;
  - a slope within `speed_range`.
- *Pooled fit.* A clip too short for its own fit uses the video's pooled fit (`ocr_clock_pooled`). That fit takes within-clip pairs only, with a free intercept per clip.

**(b) `stated_speed` / `stated_rate`.** A statement in the source.
- *`stated_speed`.* An explicit speed statement such as "2x speed" or "played at 2x" gives the factor directly.
- *`stated_rate`, with duplicates.* A single stated acquisition rate R ("7.5 frames/s", "15 fps") is compared with the measured cadence. When the clip has a duplicate pattern, speed = measured images per video second / R.
- *`stated_rate`, every frame distinct.* When every frame is a distinct image and R < 0.9 × the container rate, speed = container rate / R (each acquired image shown once).
- *Plausibility.* The result must lie within `stated_speed_range`.
- *Where statements come from:*
  - PMC captions are attached to their own file through the `xlink:href` of the `<media>` element;
  - article-level rates are attached only when the article states a single rate.

**(c) `none`.** Speed 1.0 with `speed_verified = false`, and the reasons are listed.

**Images per real second** = images per video second / speed_factor.

**C-arm angle.** When the overlay shows an angle (LAO/RAO/CRA/CAU n, or n°), it is read the same way into the per-frame table.

### 8. Outputs

`clips/<video_id>/<clip_id>/` contains:

**`images/<clip_id>_f00000.png …`** Greyscale 8-bit crops, every native frame in order, duplicates included. This matches the cine harness stem rule `^(?P<seq>.+?)_(?:f|sw|p)(?P<frame>\d+)$` (tools/cine_eval.py), so `tools/level_prototype.py --image "<clip>/images/*.png"` and `cine_eval.py video --images <clip>/images` work as is.

**`frames.csv`.** The per-frame table:

| column | meaning |
|---|---|
| `frame_file` | the PNG's file name |
| `clip_frame_index` | frame index within the clip |
| `source_frame_index` | frame index in decode order of the source |
| `pts`, `time_base`, `pts_s` | presentation timestamp: raw, its time base, and in seconds |
| `t_video_s` | pts_s − pts_s of the clip's first frame |
| `real_time_s` | `t_video_s` × speed_factor |
| `key_frame`, `pict_type` | codec frame type |
| `panel_score`, `panel_present` | fixed-box panel score on this frame, and whether it passes the gates |
| `diff_prev_mean`, `diff_prev_p995`, `ncc_prev` | change from the previous frame |
| `is_duplicate_of_previous` | 1 when this frame repeats the previous image |
| `image_update_index` | the index of the distinct image this frame shows |
| `replay_of` | the clip this frame's image first appeared in, if it is a replay |
| `phash` | 64-bit DCT hash of the crop |
| `ocr_clock_text`, `ocr_clock_s`, `ocr_angle_text`, `ocr_angle_deg` | OCR readings, if any |

**`clip.json`.** Contains:
- the box (native pixels, `[x0, y0, x1, y1)`) and its source;
- the field shape and the start reason;
- frames and the pts range;
- `timing`: `r_frame_rate`, `avg_frame_rate`, the measured fps, VFR, the acquisition cadence, `speed_factor`, `speed_verified`, `speed_evidence` and its detail, `images_per_real_s`, and `real_duration_s`;
- `liveness`, `replay` and `use_for_rates`;
- `expected` (region and view);
- `overridden` and `override_reasons`;
- digests: the images-directory sha256, the frames.csv sha256 and the preview sha256.

**`preview.mp4`.** libx264, timed by pts through the concat demuxer, written with bit-exact flags.

`clips/<video_id>/` also contains:
- **`video_manifest.json`**: the input sha256, ffprobe output, the pts/VFR summary, layouts, every segment with its keep/drop rule and refinement, the cuts, gaps and pieces, OCR regions and hits, the pooled clock fit, source statements, replays, overrides applied, config sha256, code identity, software versions and the run timestamp.
- **`qc/QC.md`**, with:
  - (a) `timeseries.png`: per-layout sampled panel score with the refined boundaries drawn, whole-frame change, and in-crop `d` with the duplicate threshold, cuts and replays;
  - (b) `Sxxx.png` per segment: 6–12 original full frames with the chosen box drawn solid green, and every other candidate drawn dashed (yellow if accepted but another layout, red if rejected). Each is labelled with its score and the gate that rejected it;
  - (c) the parameters;
  - (d) why each segment was kept or dropped.

`clips/` itself contains:
- `REPORT.md`: totals by liveness, by expected region and by expected view; per-video and per-clip timing tables; overrides; failures; excluded inputs.
- `manifest.json`: the aggregate, carrying the code identity, config and overrides sha256, software, the input list with the rule for each file, and per-clip timing and digests.
- `clips.csv`.

**Code identity.** This is the git commit when the package is committed and clean. Otherwise it is the sha256 over the tool files (`*.py`, config, overrides, environment files, tests, launchers).

## Reproducibility

- **Decoding and pixels.** Decoding is sequential and bit-exact. Crops, block means and luma use integer arithmetic.
- **No randomness.** The pipeline has no random numbers. The synthetic test videos use fixed seeds.
- **Numerics.** Threads are pinned to one for numerics. JSON floats are rounded to 6 significant digits.
- **Determinism check.** `cli determinism` runs the pipeline twice, in one job, on three real videos: the shortest per source, taken in turn (`auto:3`). It compares every clip digest and every manifest with the volatile keys removed (`common.VOLATILE_KEYS`: timestamps, wall time, host). The synthetic version is `tests/test_determinism_synth.py`.

## Overrides

`overrides.yaml` is empty. An entry must name the video, the action (`reject`, `split`, `merge`, `replace-box`), the exact values, and a reason of at least 10 characters. The pipeline applies it and marks every affected clip `overridden: true` with the reason, which also appears in the manifest and REPORT.md. Fix the algorithm instead where possible, and record the change in the change log below.

## Known limits

- **Tinted fluoroscopy is rejected.** This covers blue-tinted insets, phone films of a monitor under a colour cast, and faded semi-transparent insets: 3fhPb-ZNml4, RIxoyni0cKM, -rWuzfYkd5M and 56Sxu0thpcU. These panels fail the per-pixel grey test (chroma up to 50 on 56Sxu0thpcU) or the `chroma_p90_max` gate, which was added to reject desaturated room scenes.
  - A tint-compensated chroma dispersion was measured and does not separate the two either: tinted fluoroscopy 5.8–10 against room false positives 3.8–16.
  - This is a precision-for-recall choice, recorded here rather than tuned per video.
- **Small overlay clocks are read only sporadically.** On the SSF composites (for example Yme7AxnIRWI, VtmxIlY8S9w), tesseract reads the clock in about one probe of three at 2x. Fewer than `ocr_min_hits` hits then means no clock region, and speed evidence `none`.
- **Expected labels.** Region and view are video-level expectations from the scan document. No per-segment anatomy or view is measured.
- **Grey neighbours.** A panel bordered directly by a textured grey scene with no gutter, colour or flat bar between them can take that scene into its box.
- **Flat edges.** Flat, saturated image edges (for example white air along one whole side) are peeled off with the flat bars.
- **Clock resolution.** A 1-s clock needs at least 4 s of span. The slope error is about ±1 s / span.
- **Clock-less speed.** Speed from a stated rate assumes the stated rate is the acquisition rate of the images shown.
- **Unverified speed.** A clip with no clock and no statement keeps speed 1.0, marked unverified. Rates computed from it are in video seconds, not real seconds.

## Change log

- 2026-09-26: first version.
- 2026-09-26, before the first real run:
  - **Square structuring elements.** Morphology uses square elements (separable running max/min) instead of disks: 1080p detection took 0.86 s per sample with disks.
  - **Strided block means.** Block means are summed as strided slices: the reshape-sum was 0.46 s per frame.
  - **Analysis side 640.** `analysis_max_side` was lowered from 960 to 640 so that a 55-minute video's pass A fits in minutes.
  - **Edge peel added.** The band-support edge peel (`trim_support`, `trim_band`) was added after the synthetic composite showed boxes grown into greyish room pixels and a flat grey bar (y1 348 against the true 320). The region no longer ORs in the closed core, which had carried black gutters into the box.
- 2026-09-26, after the first real run (QC of 51 finished videos):
  - **Smooth fluoroscopy was fragmented.** Five videos gave zero clips, and T3vsvpkRR14's box covered only the shoulder third of the circle. These were full-frame Bern myelography (MOESM1), the facet arthrogram, DDR, the SpineJack phone film, and the cervical cine. The diagnostic measured median local std at the analysis scale of 1.3–2.8 grey levels on these videos, against a `texture_min` of 2.0, so the textured seed broke into fragments.
    - `texture_min` 2.0 → 1.0; `texture_window` 5 → 7; `texture_box_min` 2.0 → 1.2; score texture range [2, 8] → [1.2, 6]; `close_px` 8 → 10.
    - Flat UI and slide backgrounds measure below 0.5, so they stay out.
  - **Fragments won over the whole panel.** A fragment contained in a larger accepted panel could win suppression on score.
    - Suppression now keeps the larger box: `reject = inside`.
  - **One panel split into two layouts.** Bern MOESM2 gave two alternating layouts of one panel ([0,0,800,906] and [0,0,670,887]) and so overlapping clips, because the flat soft-tissue edge was peeled on some frames only.
    - Layout boxes are now the outer envelope of their members (`box_outer_q`) rather than the median.
    - A layout nested in another that it interleaves with in time is merged into it (`layout_nest_contain`, `layout_nest_overlap`).
  - **Stated-rate speed was refused.** A stated acquisition rate was refused whenever it was not below 0.9 × the container rate. Bern states 7.5 f/s with 8 fps containers where every frame is distinct.
    - The condition is now "stated rate ≤ 1.02 × container rate": each acquired image is then shown once, and speed = container rate / stated rate.
  - **QuickTime metadata.** PMC4852439's QuickTime file carried non-UTF-8 metadata that stopped PyAV. It is now opened with `metadata_errors="replace"`.
  - **Overview sheet.** The QC gained an overview sheet: 8 evenly spaced samples with every candidate and its rejection reason. A video with nothing kept now shows why.
  - **Determinism set.** `auto:3` had picked a 7-frame GIF and two videos with no clip. `auto:4` now takes the shortest videos of at least 20 s from each source in turn.
  - **Circle completion.** On T3vsvpkRR14 and the Cureus cervical exam, the round field's box still followed only its textured part: a saturated collimator band and dark soft tissue were left out. The fix fits the region boundary pixels that touch black (the field rim), and the box becomes the disk's bounding box when all of these hold:
    - the rim is round (`circle_rms_max`);
    - it covers at least `circle_min_arc_deg` of arc (at least `circle_min_rim_px` pixels);
    - the disk is at least `circle_disk_nonblack` non-black.

    A unit test (a disk with its left part flat white) checks that the whole disk is recovered within 3 px.
  - **Burned-in titles joined the circle.** On the Cureus exam, burned-in titles beside the circle were joined to it by the closing and widened the box, so the first completion rule (the box must lie inside the disk) refused the disk. The rule is now that at least `circle_region_inside` of the candidate's region lies inside the disk, and the text is then left out.
  - **`repeat_pattern` fixed.** It reported the first run of a clip rather than the typical cycle ('4' for a 2-frame cadence whose first image was held 4 frames). It is now the most frequent cycle, written from its smallest rotation.
- 2026-09-26, after the second real run (QC of 55 finished videos):
  - **Desaturated room scenes accepted as panels.** On E06MD3KnhvE (4K documentary footage), walls, equipment and a chair passed the per-pixel grey test and the gates, giving 30 room clips; there were more on KWwGMIoDrmU. A diagnostic measured the 90th percentile of residual chroma inside accepted boxes:
    - fluoroscopy screen captures: 0–8;
    - phone films of a monitor: 7–14;
    - the room false positives: 15–23.

    New gate `chroma_p90_max` = 14 (feature `chroma_p90`).
  - **On-screen clocks missed.** They were missed on the SSF videos. The diagnostic found tesseract reading the clock at 2x only (VtmxIlY8S9w `14:40`, Yme7AxnIRWI `11:00:44`), often with confidence 0.
    - Discovery now reads probes up to 1080p at 2x (`ocr_upscale_below_h` 2200).
    - It drops the confidence floor (`ocr_min_conf` -1), because the clock pattern, at least 3 hits at one place, and at least 2 distinct values are the filter.
    - It reads 24 probes instead of 16.
  - **Line endings.** Patch scripts run on Windows had written CRLF line endings, and sbatch refused one launcher. All files are LF again.
