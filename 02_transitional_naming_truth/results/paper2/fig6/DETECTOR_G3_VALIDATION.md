# The s15 primary detector: VALIDATION-side recall per device

`det_g3_primary_s0` (LEVELCHECK_MODEL.md section 15): one YOLO11m at 1024 px, classes vertebra (body box, A28) and
sacrum (whole bone), trained on the G3 TRAIN side of every device and corpus (real frames + styled renders of TRAIN
persons under TRAIN pose donors), checkpoint selected on the G3 VALIDATION side (best epoch 36 of 50, patience 15).
Weights `~/spine-detector/runs/g3/det_g3_primary_s0/weights/best.pt`, sha256
`fe00a1732032e81a3f892e91a3bf51105e4822d0cf624ac71fedd15a8652f92f`; registry parent `public:ultralytics/yolo11m.pt`
(COCO release, verified). Training job 40436991; post stage 40437708 (COMPLETED 16:52 EDT, `G3DET_POST_OK`).

**Every number below is on the G3 VALIDATION persons -- the detector's own checkpoint-selection set.** No G3 test
person, and no Figure 6 T1/T2/T3 person, is in any of it: `tools/eval_gate.py` on the checkpoint against all 2,887 G3
test + hold persons gives overlap 0 (POST.json `eval_gate_test_persons`; T1 42, T2 159, T3 13 persons all HELD OUT),
and the validation files themselves carry `held_out: false` with the reason "G3 VALIDATION persons: the
checkpoint-selection set of this detector; reported as validation recall, never as a held-out number". These are
development measurements. They do not choose anything on test data, and they are not results.

Source: `/rs/rs_grp_oschome/go2432/data/fig6/detector_g3/post/det_g3_primary_s0/POST.json` (`validation_recall`) and
`val_<root>_g3body_c{0.25,0.74}.json` (tools/realxray_eval.py, one call per root and confidence; 95 % intervals are a
case bootstrap). Recall = truth boxes matched by a detection of the same class; k/n = matched / truth boxes.

## Recall, k/n, by device and confidence floor

| device (validation root) | frames | persons | conf | vertebra k/n | vertebra recall (95 % case boot) | sacrum k/n | sacrum recall (95 %) | sacrum found on frame |
|---|---:|---:|---:|---:|---|---:|---|---:|
| C-ArmLSpine (`carmlspine_g3body`) | 20 | 10 | 0.25 | 87/100 | 87.0 % (81.7-92.1) | 18/20 | 90.0 % (70.0-100) | 18/20 |
| C-ArmLSpine (`carmlspine_g3body`) | 20 | 10 | **0.74** | 84/100 | 84.0 % (79.4-88.9) | 18/20 | 90.0 % (70.0-100) | 18/20 |
| COBRA Elekta v1 window (`cobra_elekta_g3body`) | 216 | 9 | 0.25 | 284/303 | 93.7 % (81.8-100) | 205/206 | 99.5 % (98.5-100) | 205/206 |
| COBRA Elekta v1 window (`cobra_elekta_g3body`) | 216 | 9 | **0.74** | 250/303 | 82.5 % (57.0-96.8) | 199/206 | 96.6 % (92.5-99.5) | 199/206 |
| COBRA Elekta v3 body window (`cobra_elekta_v3_g3body`) | 216 | 9 | 0.25 | 283/303 | 93.4 % (80.0-100) | 206/206 | 100 % (100-100) | 206/206 |
| COBRA Elekta v3 body window (`cobra_elekta_v3_g3body`) | 216 | 9 | **0.74** | 248/303 | 81.8 % (56.4-97.3) | 201/206 | 97.6 % (94.7-99.5) | 201/206 |
| DeepFluoro (`deepfluoro_g3body`) | 105 | 1 | 0.25 | 95/125 | 76.0 % (one person: no interval) | 101/101 | 100 % | 101/101 |
| DeepFluoro (`deepfluoro_g3body`) | 105 | 1 | **0.74** | 58/125 | 46.4 % (one person: no interval) | 98/101 | 97.0 % | 98/101 |

C-ArmLSpine by view (vertebra): AP 45/50 at 0.25 and 43/50 at 0.74; LAT 42/50 at 0.25 and 41/50 at 0.74.
The COBRA v1 and v3 rows are the SAME 216 frames of the same 9 persons under two export windows (both windows were in
the training lists, x1 each); they are not independent. DeepFluoro validation is one specimen (105 frames), so its
interval is degenerate and the number says little. The ultralytics validation over all 341 frames pooled (the
checkpoint-selection metric) was P 0.921, R 0.921, mAP50 0.945, mAP50-95 0.690.

## What follows for the Figure 6 configuration (written before any test person is scored)

- The sacrum anchor at conf >= 0.74 (the primary operating point fixed in s4) finds the sacrum on 96.6-97.6 % of
  COBRA validation frames and 90 % of C-ArmLSpine validation frames. The LODO sacrum detector the held jobs carried
  found it on 3.4 % of COBRA2026 development frames (s15), which is why s15 replaced it.
- Vertebra (body) recall falls 11-12 points on COBRA and 30 points on DeepFluoro between conf 0.25 and 0.74. A body
  with no detection makes the frame wrong under the s4 endpoint. The primary variant therefore takes BODY boxes from
  this detector at its default floor 0.25 (`--box-conf 0.25`, the c0.25 validation operating point) and applies the
  0.74 floor to the SACRUM ANCHOR through the coupler (`--sacrum-min-conf 0.74`, det74), exactly as the pre-G3 G5
  draft manifest split the two thresholds (`vertebra_boxes.conf` 0.35 for the keypoint detector; `sacrum_anchor_min_conf`
  0.74). det25 (anchor at 0.25) is the labelled secondary. Both floors are named in `results/fig6/G5_MANIFEST.json`.
  This choice is made on validation numbers only; nothing here was seen on a test person.
- The comparison the held-out analysis cannot make is between these validation numbers and test recall: the test
  numbers do not exist yet and will be reported as what they are when the jobs are released.

Written 2026-09-24 by the Figure 6 resubmission step; the source files above are unchanged.
