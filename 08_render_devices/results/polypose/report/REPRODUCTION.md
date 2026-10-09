# PolyPose reproduction on DeepFluoro (Task A)

Verdict: **REPRODUCED**

Folds, stated in full: per subject {'1': 0.0029, '2': 0.0037, '3': 0.0042, '4': 0.011, '5': 0.0012, '6': 0.0001} %; subject-mean 0.0038 %, SD 0.0038 % — prints as 0.00(0.00) % under the paper's own convention (every Table-1 metric as mean(SD) to two decimals; "we report all metrics as mean(sd)", arXiv:2505.19256v3). The fitted fields are NOT literally fold-free, and the generative bank keeps its own stricter Jacobian>0 gate (`tools/polypose_invariants.py`) regardless of this verdict.

## What was run
- Code: `github.com/eigenvivek/polypose` @ `909a9bb2eeccf05065c7bc1d3703fb99f87b35b9` (uv.lock sha256 `f4d6afb785500d31d49149f3dd0d80b8fbff8ea444b989ce75d1490af22f6df2`), xvr `xvr @ git+https://github.com/eigenvivek/xvr.git@3e0b26eb51ef4a9c37615611bb05e0e200e48092`; env built with `uv 0.12.18 (x86_64-unknown-linux-gnu)`, mode `container-frozen-no-dev`, python 3.10.21, env hash `f94fd57e312465b1dd72cdc60d3f5197713e17684044198dec4b67d6d58ca32d` (`slurm/env/polypose.yml`, `polypose.requirements.lock.txt`, `polypose.freeze.txt`).
- Data: HF `eigenvivek/xvr-data` revision `a17273e3eadbd793bd861f3598a80ce4590c1124`, deepfluoro/subject01..06, sha256 list in env/export/xvr_data_deepfluoro.sha256; jobs ran with HF_HUB_OFFLINE=1.
- Host: CentOS Linux 7 (Core) glibc 2.17 (container: Ubuntu 22.04.3 LTS 2.35 ); GPUs: NVIDIA L40S; seed 42 (run.py).
- Container: module hits `apptainer/ apptainer/1.2.2 singularity/ singularity/3.5.2 singularity/ singularity/2.6.0 singularity/3.2.1 `; binary `/wsu/el7/gnu7/apptainer/1.2.2/bin/apptainer` (apptainer version 1.2.2); pull `ok`, exec of the locked venv inside it `ok`, build --fakeroot `fail: INFO:    User not listed in /etc/subuid, trying root-mapped namespace`.

## The one deviation from the public scripts, and its evidence
- `experiments/deepfluoro/{run,eval}.py` load each packaged pose right-multiplied by diag(-1,-1,1,1): run.py (applied), eval.py (applied). Full diff in `env/export/pose_flip.diff`, record in `env/export/POSE_FLIP_PATCH.json`.
- Why (measured, report/diag{,2,3}): as packaged, every ray meets the CT at alpha in [-0.83, -0.63] — BEHIND the source — so the trilinear renderer (alpha clamped to [0,1]) returns exactly zero, the fit optimises a constant loss and never moves (fitted pose norms ~1e-8), and attempt 1 (jobs 40418510/40418512, archived in report/attempt1_noflip/) read Dice 0.000 on the UNWARPED original CT — the impossible number that exposed it. Of eight 180-degree corrections, only this one puts every intersection inside [0,1] AND matches the real frame (NCC 0.13 -> 0.71/0.65 on two frames, GT outline aligned in report/diag3/drr_diag3.png). Same rot-180 convention DeepFluoro needed in our own formation pipeline.

## Table 1 comparison (PolyPose row; mean(SD) over subjects of the per-subject mean; held-out views per subject in eval summary)

| metric | paper | ours (subject mean(SD)) | ours pooled over views | original CT (no warp) |
|---|---|---|---|---|
| dice_pelvis | 0.99 | 0.992(0.005) | 0.992(0.006) n=184 | 0.994(0.001) |
| dice_lfemur | 0.98 | 0.978(0.009) | 0.980(0.010) n=104 | 0.964(0.017) |
| dice_rfemur | 0.98 | 0.980(0.007) | 0.979(0.012) n=123 | 0.963(0.016) |
| hd95_pelvis | 1.00 | 1.034(0.077) | 1.039(0.153) n=184 | 1.004(0.006) |
| hd95_lfemur | 1.48 | 1.561(0.917) | 1.489(1.089) n=104 | 3.648(2.372) |
| hd95_rfemur | 1.56 | 1.527(0.497) | 1.537(0.966) n=123 | 3.256(1.670) |
| % folds | 0.00 | 1: 0.0029, 2: 0.0037, 3: 0.0042, 4: 0.011, 5: 0.0012, 6: 0.0001 | — | — |

HD95 is in pixels of the 179-px DRR (no spacing is passed to monai in the authors' eval.py); 1 px = 1.556 mm.

## Are the authors' files our specimens? (tools/polypose_hf_vs_h5.py)
- subject01 → `17-1882`: HU identical on 100.00 % of voxels, max |ΔHU| 0.0, segmentation identical on 100.00 %
- subject02 → `18-1109`: HU identical on 100.00 % of voxels, max |ΔHU| 0.0, segmentation identical on 100.00 %
- subject03 → `18-0725`: HU identical on 100.00 % of voxels, max |ΔHU| 0.0, segmentation identical on 100.00 %
- subject04 → `18-2799`: HU identical on 100.00 % of voxels, max |ΔHU| 0.0, segmentation identical on 100.00 %
- subject05 → `18-2800`: HU identical on 100.00 % of voxels, max |ΔHU| 0.0, segmentation identical on 100.00 %
- subject06 → `17-1905`: HU identical on 100.00 % of voxels, max |ΔHU| 0.0, segmentation identical on 100.00 %

## Forward (generative) use, measured on subject 1 (forward_test, grid [398, 197, 341], resample None)
- T0 identity, authors' sampler: label mismatch 0.497 %, femur centroid shift (vox) [0.3966, 0.4385, 0.4639]; corrected sampler: 0.000 %, shift [0.0, 0.0, 0.0]; authors' jacdet mean 0.9999999403953552, independent det min/mean 0.9999923706054688/0.9999999403953552
- T1 left femur 10° + 5 mm: folds (authors) 0.018298249691724777 %, independent frac det<=0 0.00016131537267938256, min det -1.9914911985397339; Dice vs pull-back hypothesis (bone moves by M^-1) 0.9510699516443122, vs push-forward (M) 0.6385848000260906; corrected sampler 0.9772836986812367; centroid distance to M^-1 c 2.0446215550604956 mm, to M c 8.246060859304697 mm; HU corr in moved femur 0.9357630049699786; unmoved hemipelvis Dice 0.959263748352528/0.9893924228130295
- T2 3body_gravity: bone voxels with max weight < 0.9: 2.17 %; worst body [5] own-weight p05 0.821579098701477, min 0.2616024911403656, frac<0.9 0.08726257085800171
- T2 3body_invdf_eps1: bone voxels with max weight < 0.9: 0.75 %; worst body [5] own-weight p05 0.9629184007644653, min 0.6666399836540222, frac<0.9 0.01401421707123518
- T2 3body_invdf_eps0.1: bone voxels with max weight < 0.9: 7.30 %; worst body [5] own-weight p05 0.7774873971939087, min 0.5236448645591736, frac<0.9 0.12234091013669968
- T2 7body_gravity: bone voxels with max weight < 0.9: 2.71 %; worst body [7] own-weight p05 0.42136257886886597, min 0.1055627390742302, frac<0.9 0.26276466250419617
- T2 7body_invdf_eps1: bone voxels with max weight < 0.9: 2.16 %; worst body [7] own-weight p05 0.8301873207092285, min 0.4998495280742645, frac<0.9 0.08033954352140427
- T2 7body_invdf_eps0.1: bone voxels with max weight < 0.9: 20.52 %; worst body [7] own-weight p05 0.5565948486328125, min 0.35408341884613037, frac<0.9 0.29532015323638916
- T3 both femurs ±10°: folds 0.009309768676757812 % (independent 7.069002458592877e-05), Dice femur L/R vs rigid 0.952501811930993/0.9589223383988419, saved affine max diff 0.0, axcodes LPS→LPS
- T4 render: /rs/rs_grp_oschome/go2432/data/polypose/forward_test/subject01_render.png; NCC real vs DRR original 0.9416310144162666, vs warped 0.10196574317139688

## Per-subject runs
- subject 1: job 40419712 on alh2 (NVIDIA L40S, driver 580.105.08), 112 s, training frames [10, 9], % folds 0.0029, mask sha256 `2c744223010044d0…`
- subject 2: job 40419713 on alh2 (NVIDIA L40S, driver 580.105.08), 108 s, training frames [29, 31], % folds 0.0037, mask sha256 `64efe1f4005cff3e…`
- subject 3: job 40419714 on alh3 (NVIDIA L40S, driver 580.119.02), 185 s, training frames [17, 22], % folds 0.0042, mask sha256 `891c5530442e0621…`
- subject 4: job 40419715 on alh3 (NVIDIA L40S, driver 580.119.02), 198 s, training frames [0, 33], % folds 0.011, mask sha256 `8b43be8baa78ef04…`
- subject 5: job 40419716 on alh4 (NVIDIA L40S, driver 580.119.02), 180 s, training frames [2, 47], % folds 0.0012, mask sha256 `786d4cbc7a64f331…`
- subject 6: job 40419709 on alh4 (NVIDIA L40S, driver 580.119.02), 150 s, training frames [9, 7], % folds 0.0001, mask sha256 `e807adbfe2fc0ae4…`
