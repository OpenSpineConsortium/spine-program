# Overnight report, 2026-09-14: why the models degrade on published fluoroscopy, and what was done

## 1. The degradation is a scale problem in the detector, not image quality

Evidence, in the order it was gathered:

1. **Synthetic faults on films do not break the detector.** On 300 annotated lateral films with
   ground-truth corners (`tools/detector_robustness.py`, `~/bench/robust/detector_robustness.json`),
   recall at IoU 0.5 stays 0.97–1.00 under downscaling to 300 px, JPEG q30, polarity inversion,
   circular collimation to 0.6 of the field, 25% white page borders, contrast compression,
   gamma, text overlays and a "monitor photo" (rotation + blur + JPEG). Caveat: these films are
   the detector's own training corpus, so this measures fault sensitivity, not generalisation.
2. **Preprocessing the FluoroCap panels does not help.** Auto-inversion (applied to 368 panels)
   and tight cropping to the non-background region (2,188 panels) leave the agreement with the
   caption unchanged (19.5–19.7% loose, 4.7–5.0% strict, versus 19.2% / 4.9% baseline).
3. **Projection is not the explanation.** The pipeline was trained on lateral films only, but
   lateral and frontal FluoroCap panels fail alike (20% no detection in both; loose agreement
   24% lateral vs 20% frontal). Lateral lumbar is the best case at 35%.
4. **Lowering the detector confidence only adds junk.** conf 0.4 → 0.2 → 0.1 raises the loose
   set metric 19 → 30 → 39% by adding boxes (median 3 → 7 → 10 per panel) while contiguous
   runs fall 4.9 → 2.3 → 1.3%.
5. **The overlays show what is happening** (`~/FluoroCap/validate/preds_{lumbar,cervical}_lateral.png`).
   Where a full-length film appears inside FluoroCap, boxes and names are right. On the
   collimated close-ups that make up most intra-operative fluoroscopy, one to three vertebrae
   fill the frame and the detector, trained on films where a vertebra is 3–10% of the image
   height, boxes screw heads and needle tips or nothing. The level model then receives wrong
   crops and answers with cervical names on lumbar frames. Panels are small (median long side
   375 px), which compounds it.

**What was done about it tonight.** `tools/make_zoom_dataset.py` cuts 22,014 zoomed windows
(1–4 consecutive vertebrae, 480–1100 px, with collimation, inversion, instruments, JPEG) out of
the 11,007 labelled training films, with their corner labels transformed, and the detector is
being fine-tuned from detect_v3 on original + zoomed data (`detect_v5z`, job 40233036, 60 epochs).
After epoch 1 the mixed validation set already reads box mAP50 0.977 and pose mAP50 0.978.
When it finishes, the FluoroCap comparison (`benchmark/data/fluorocap_v0.1/infer_comparison.md`)
is rerun with the new weights; the readers' boxes will then give the first true per-box numbers.

### 1b. The second failure is the level model's region confusion under domain shift

With the fine-tuned detector's boxes (epoch 4 of 60, so an early checkpoint) the boxes now sit on
the vertebrae in the collimated close-ups, but the names are wrong in a specific way. Majority
predicted region against the caption's region, 2,815 panels:

| Caption region | → cervical | → thoracic | → lumbar |
|---|---|---|---|
| cervical (n=400) | 79% | 2% | 19% |
| thoracic (n=288) | 56% | 4% | 40% |
| lumbar (n=1,069) | 50% | 3% | 47% |

Half of lumbar fluoroscopy is called cervical, and thoracic is never recognised. The level
model's training set is 17,375 cervical crops against 2,235 annotated lumbar (plus BUU / VinDr),
and the crop construction normalises vertebra size, so under a new appearance (collimated,
inverted, instruments, cement) it falls back to the majority class. Same-scale cervical and
lumbar bodies are separable only by shape and context; on films the model has that, on C-arm
frames it does not transfer.

What was tried tonight and what it says. A region classifier trained on FluoroCap's own
caption regions (`tools/fluorocap_region_classifier.py`, 5 folds grouped by article) reaches
only 63% out of fold from ImageNet-pretrained weights (57% from scratch, against a 56%
majority baseline): cervical 55%, thoracic 45%, lumbar 77% correct. Even a model trained on
fluoroscopy cannot name the region from a 224 px panel reliably, so the `--region-prior`
option in inference exists but is not used: a 63% prior would mask the right region a third of
the time. The physics-augmented level models (aug2, aug3) run with the fine-tuned detector do
not change the confusion either. Read together with the detector result, the conclusion is
that region identity on collimated C-arm close-ups is carried by fine bone detail that both
the 224 px classifier and the 96 px-per-vertebra crops discard, and by context the frame no
longer contains. The reader study is what turns this into numbers: per-box labels on real
fluoroscopy, then fine-tuning the level model on those crops at full resolution.

## 2. 99% on three-vertebra spans, per level, one model

Recurrent head over the single-vertebra model trained on annotated films + BUU + VinDr
(`~/bench/xr_fov/recurrent_all2.json`, held-out real films):

| Span | Exact | Cervical | Thoracic | Lumbar | Sacrum |
|---|---|---|---|---|---|
| 3 vertebrae | 98.84% | 99.3% | 98.5% | 91.2% | 93.5% |
| 5 | 99.13% | 99.5% | 95.5% | 93.2% | 95.7% |
| 7 | 99.42% | 99.7% | 98.5% | 94.9% | 93.5% |
| 9 | 99.38% | 99.6% | 98.5% | 95.6% | 95.7% |

Per level at three vertebrae: C2 100, C3 99.6, C4 99.0, C5 98.6, C6 99.3, C7 99.7, T12 98.3,
L1 86.6, L2 86.6, L3 90.2, L4 96.3, L5 96.3, sacrum 93.5.

Two facts decide the path to 99%:

- The cervical target is met (CSXA, 1,488 held-out films per level). The NHANES cervical films
  are worse (C4–C6 89–94%): older, lower-quality films under-represented in training.
- The lumbar held-out set is 82 films per level (NHANES). One error is 1.2 points; 99% cannot
  even be measured on it. Lumbar training data with real labels is 2,235 crops against 17,375
  cervical. This is a data problem before it is an architecture problem.

Running now for the morning: physics-augmentation arms aug2 and aug3 (the earlier ones died
on a variable-shadowing bug in `augment_physics`, fixed), the all4 arm (annotated + BUU +
VinDr + oblique DRRs, 60 epochs, aug3), a ConvNeXt-tiny three-vertebra arm, and a 128-px
target crop bank. Each writes `result_rung_*.json` and the registry assigns it an id.

What will actually move lumbar to 99%: (a) reader-labelled lumbar films from FluoroCap and
VinDr as held-out test material large enough to resolve 1%; (b) their training-side
counterparts; (c) the detector fix above, because on real fluoro the level model never sees a
correct crop today. Prior art (`docs/PRIOR_ART_LEVEL_ID_XRAY.md`): intraoperative long-length
labelling reports F1 > 96% (Huang 2022); LevelCheck-style 3D–2D registration needs a
preoperative CT; a 2024 L5-identification model reports 95.7% precision; the 2026 systematic
review of level determination reports conventional methods up to 100% but with transitional
vertebrae as the recurring failure. Nothing reports 99% per level from a single fluoroscopic
frame without a CT.

### 2b. Physics augmentation: aug2 buys robustness for almost nothing, aug3 costs too much

Corruption suite on held-out annotated films (`benchmark/data/robustness/all2_*.json`), exact
accuracy at severity 5 (the harshest), single-vertebra model unless noted:

| Model | Clean | Over-exposure | Magnify 0.6x | Rotate 30 deg | Shutters 22% | Inversion |
|---|---|---|---|---|---|---|
| baseline, 1 vertebra | 97.7 | 29.1 | 71.9 | 51.6 | 86.6 | 82.4 |
| aug2, 1 vertebra | 96.0 | 70.2 | 92.2 | 94.9 | 92.3 | 95.6 |
| baseline, 3 vertebrae | 99.1 | 16.9 | 57.6 | 92.1 | 73.6 | 91.6 |
| aug2, 3 vertebrae | 99.0 | 79.2 | 97.6 | 98.1 | 95.3 | 98.7 |
| baseline, 5 vertebrae | 99.0 | 19.1 | 66.1 | 92.1 | 23.2 | 91.7 |
| aug2, 5 vertebrae | 98.8 | 78.3 | 97.8 | 98.5 | 95.4 | 98.7 |
| aug3, 5 vertebrae | 96.6 | 78.6 | 94.1 | 96.6 | 89.8 | 96.2 |

aug2 at three vertebrae keeps 99.0% clean (registry M19) and is the robust model to ship for the three-vertebra claim; at five, 98.8%. It does not, however,
fix the FluoroCap region confusion (aug2 and aug3 with the fine-tuned detector: still ~50% of
lumbar frames called cervical), which confirms that the fluoroscopy gap is anatomy-appearance
domain shift, not the acquisition faults the augmentation simulates.

## 3. FluoroCap

- v0.1 frozen; v0.2 manifest with classifier v3: 2,815 included panels (A), 1,117 clean (B),
  166 in the licence review queue.
- Classifier v3 (films + caption-verified fluoroscopy + 12,000 video-frame negatives):
  held-out 94.0% modality, 99.0% view. On its own it still accepts grey gradients and cloth as
  radiographs inside video frames, so the video window search now uses the vertebra detector
  as the gate (runs after the fine-tune).
- Video route: 905 systematic queries in twelve languages, four workers, 720p, subtitle-aligned
  level cues; ~70,000 frames on the grid, 25 GB under WSL, still growing (one worker alone has
  190 videos / 17,000 frames from the cervical-fusion queries).
- Finding the C-arm image inside a frame took three attempts. The classifier alone, on
  sub-windows, accepted faces and gradients even at p 0.8; the fine-tuned detector alone
  accepted hands and sky; the two together (classifier p >= 0.6 on the window AND the
  detector finding two or more vertebrae at confidence >= 0.7) yield windows that are almost
  all real fluoroscopy: lateral cervical, AP lumbar with needles, cement, myelograms, lead
  placements (`~/FluoroCap/validate/montage_video_panels_strict.png`). The search is running
  over the 51,000 synced frames; the accepted windows enter the manifest as a tier-E route
  with the spoken level cues.
- Student screening pages: `~/FluoroCap/screen` (104 pages of 60, keys Y / P / N / ?), the first
  two on the Desktop under `FluoroCap_screening`. Reading pages (anchor labelling) under
  `~/FluoroCap/annotate` and `FluoroCap_reading`.
- PMC fetching runs from WSL (the grid's IP is captcha-throttled); 2,901 figures merged.

## 4. Rib QC

v4 versus release under identical code, v4 remapped to the release id scheme:
`CTSpinoPelvic1K-1/results/rib_qc_v4_vs_release/README.md` (mixing 151/584 → 0/0; detached
37/40 → 0/0; fragmented 153/510 → 10/13; misnumbered 24/170 → 0/2; no vertebra in reach 38 → 11).

## 5. Hardware as a per-vertebra constraint (added mid-day)

A caption saying "L3-4 fusion with pedicle screws" fixes which two vertebrae are L3 and L4, not just
the level set. Three pieces make that usable (`tools/fluorocap_hardware.py`, `tools/fluorocap_anchor.py`,
`tools/train_orientation.py`, `tools/make_hardware_dataset.py`, `--orient/--hardware/--anchor` in
`fluorocap_infer.py`):

- **Caption parser.** Devices bound to levels within a sentence, by proximity, in eleven languages.
  Kinds: body (screw, cement, trocar, drill, resection), disc (cage, interbody procedure, injection
  needle at an interspace), span (rod, plate, lead, fusion construct). Of the 2,815 included panels,
  946 carry a body-level constraint, 309 name hardware in two or more vertebrae, 453 a disc pair,
  416 a span; 929 have no device at all (`~/FluoroCap/hardware_constraints_stats.json`).
- **Orientation net.** Which way is cranial, learned self-supervised by rotating the 11,007 upright
  films of the detector corpus (4 classes, flips as augmentation, crops down to 30% to mimic
  collimation). Frames arriving upside-down or sideways are rotated to cranial-up before detection;
  below 0.6 confidence the decoder tries both directions. Job 40233228.
- **Hardware detector.** VinDr-SpineXR's "Surgical implant" boxes (429 train, 107 test, merged
  across readers) plus 600 "No finding" negatives train a YOLO11m implant detector; each detected
  vertebra is flagged when an implant box overlaps it (or its 30%-widened outline, since screws run
  past the body). Research-only source, annotation aid only. Job 40233229.
- **Constraint decoder.** Every contiguous run of the column is scored by floored model log-probability
  (a confidently wrong model cannot veto), plus caption agreement, plus hardware agreement (flagged
  boxes on constraint levels count for, off them against, constraint levels without metal half
  against; a disc pair must be adjacent in the run). The record says which term decided.

Prior art on the general question (semi-/weak supervision, pseudo-labelling, model-assisted
annotation, SAM on radiographs) is in `docs/PRIOR_ART_WEAK_SUPERVISION.md`; no paper uses
caption-named hardware as a per-vertebra constraint.

Results (all on the 2,815 included panels, detector `detect_v5z` epoch 25, level model all2 aug2 rung 1,
histogram-matched to the films; `infer_summary_v5z25_hist_r1_anchor*.json`):

| Run | scored | no detection | model run contains caption | anchored run contains caption | decided by hardware |
|---|---|---|---|---|---|
| decoder, caption soft | 1,959 | 856 | 290 (15%) | 923 (47%) | 31 |
| + hard caption containment, orientation rotating every call | 1,864 | 951 | 249 | 1,512 (81%) | 35 |
| + rotate sideways calls only (p ≥ 0.9), 180° = direction unknown | 1,934 | 881 | 268 | 1,566 (81%) | 39 |
| + implant detector, construct-covers-vertebra flag | 1,957 | 858 | 285 | 1,578 (81%) | 78 |

What these mean, honestly: "anchored run contains caption" is an upper bound because the caption is
enforced whenever it fits; it says the decoder can produce a caption-consistent, contiguous per-vertebra
proposal for 81% of scored panels, which is what the readers will correct. The caption-BLIND check (level
set withheld; hardware flags + which vertebrae the caption says carry hardware + contiguity + model) is
consistent on 22 of 51 panels (43%) against the model's 15%, on the panels the implant detector flagged.

- Orientation net: 99.9% on rotated films, but on FluoroCap it called a third of panels rotated and
  rotating them lost more detections than it gained (41 gained, 66 lost among 231 sideways calls at
  p ≥ 0.6). Sideways calls at p ≥ 0.9 are rotated; a 180° call (278 panels) is treated as unknown
  direction and the decoder tries both orders (it chose the reversed order in 173). Montage:
  `~/FluoroCap/validate/orient_montage.png`.
- Implant detector (VinDr implants, mAP50 0.42 on VinDr's test split): precise on FluoroCap (blue boxes
  sit on constructs in `validate/hw_flag_montage.png`) but low recall, 152 of 1,957 scored panels
  flagged where several hundred show metal. It draws one box per construct, hence the
  covers-the-vertebra rule. Next: metal pseudo-labels from FluoroCap itself (saturation blobs inside
  boxes on panels whose caption names hardware) and the CT hardware DRRs (11 cases) to retrain.
- Detector remains the bottleneck: 858 panels with no vertebra found.

## 6. FluoroGen: synthetic C-arm frames with labels (started mid-day)

The DRRs already carry perfect per-vertebra labels; what they lack is the look of fluoroscopy and the
hardware. So the generator is geometry-preserving by construction: each DRR is both the init image and
the Canny-edge ControlNet condition for SDXL, and the fluoroscopy look comes from a LoRA trained on the
FluoroCap panels, the accepted video windows and 1,200 real films with templated captions. Before
synthesis a crude metal template (pedicle screws, screws with rods, a needle, cement) is drawn into the
DRR at chosen levels and rendered as metal by the model; the instrumented levels are written into the
label file. Output is in the DRR directory format so the crop-bank builder and detector export read it
unchanged (`tools/fluorogen_dataset.py`, `tools/fluorogen_generate.py`, `tools/fluorogen_check.py`,
`slurm/fluorogen_lora.sh` on four H200s, `slurm/fluorogen_generate.sh` as a job array).

Checks before any synthetic image enters a training arm: the film detector must still find the labelled
boxes (recall at IoU 0.5 on synthetic versus source DRR), the panel classifier should move towards the
real panels, and the montages get looked at. The only result that counts is a level-model arm trained
with synthetic data added and tested on real films and reader-labelled FluoroCap.

Base model is SDXL 1.0 (CreativeML Open RAIL++-M); FLUX.1-dev and SD3.5 were passed over for their
licence terms.

## 7. Serving: the model leaves the browser

The website had served the corner detector as an ONNX file since August; a file a page loads is a file a
visitor can save. The model files and the vendored runtime are gone from the site, and the X-ray page now
sends the image to a level service and receives boxes, corner landmarks and the model's level names
(`service/` here: FastAPI, self-contained model definitions, CPU container; weights pulled at start-up
from a private repository with a read token; `tools/deploy_service.py` releases a registry model and
refuses a public destination). The page names levels from the run labeller and lets a region choice
override with counting, as before.

Measured on the grid login node (eight old CPU cores): 1.6–2.3 s per 2,048 px film end to end, about
0.9 s of it fixed overhead; on a V100 the detector takes 23 ms and each level crop 2.3 ms. So a CPU host
does not beat the old in-browser WebGPU path on latency; a GPU host does, and either makes the latency
independent of the visitor's device and adds level naming, which the browser demo never did. Hosting is
not yet chosen: Hugging Face Docker Spaces need a paid plan for both the organisation and the personal
account. The ONNX files remain in the site's public git history until that history is rewritten.

Implant detector round two (self-trained from round one's boxes) flagged fewer panels (87 vs 152) and
was caption-blind consistent on 10 of 23; round one stays in use.
