# STATUS: the results in hand on 2026-10-08

Every row names its catalog id (`docs/handoff/RESULTS_CATALOG.md`, written 2026-10-08 from spinesurg-ct-nnunet
097933a), the file that holds the number, and its status and rigor mark in the catalog's own words. Status words:
CURRENT (printed or the standing value), HELD-OUT NOT QUOTED (passes the gate, not in the text), SUPERSEDED (do not
quote), RECORD ONLY (history), OPEN (a defect or an unfinished item), REFUTED. Rigor marks: [THR] threshold chosen
after a result was seen; [LEAK] trained or selected on a leaked bank; [SEL-SPLIT] scored on the selection split;
[WORDING] a document's sentence disagrees with its own numbers. Prefixes: `ssn:` spinesurg-ct-nnunet 097933a,
`sn:` its `SchwingNet/`, `~` grid HOME `/wsu/home/go/go24/go2432`, `$RS` `/rs/rs_grp_oschome/go2432`.
Nothing here was re-run; a grid file was not re-verified.

**2026-10-12, who reads what.** Greg answered OPEN_QUESTIONS A29 on issue #68, option (a): every Write holder may read all 13 folders; "Greg-only" and the label `greg-first` govern claiming and hand-outs, not reading. The `docs/handoff` copies keep their older wording.

## 1. The render banks (DATASET_USAGE 3.1, 3.3; LITERATURE_STATE 1.6; OQ B12, B22, G1)

| id | claim | file | status |
|---|---|---|---|
| DU 3.1 | `physics_drr` 7,045 annotations: ctsp 2,430 (798 people), totalseg 1,831 (1,121 subjects), verse 1,463, implant 1,321; built by `tools/render_physics_drr.py --per-case 2 --det-px 640` under `STAGE=physics ssn:slurm/fluorocap_v2.sh`; the only route by which TotalSegmentator reaches the v9 level bank | `docs/handoff/DATASET_USAGE.md` 3.1; `ssn:data_platform/sources.json` card `physics_drr` | CURRENT; the same card's location notes say 7,048 (ctsp 3,754, ts 1,831, verse 1,463): unexplained, OQ B12 and G1 |
| DU 3.1 | `physics_rare` 1,482 annotations: 34 CTSP ids (603 renders) + 47 VerSe series (879); 9 of 56 VerSe rare series missing, including 2 of the 6 T13 scans; 14 of 16 lumbar-rib records not included | `docs/handoff/DATASET_USAGE.md` 3.1; `ssn:data_platform/DATA_MANIFEST.md` card `physics_rare` | CURRENT with the gaps recorded |
| RD 2.2 | random-window naming on `physics_rare` 45.1 % against 93.9 % on `ctsp_drr` | `docs/handoff/RESEARCH_DIRECTIONS.md` 2.2 (PLDA Table D) | measured |
| DU 3.3 | `$RS/data/devcorpus`: 142 clean TotalSegmentator v3 whole spines, 17 validation subjects shared by all five styled corpora, ray-cast under each device's real poses and styled by its nine terms; design A with Elekta held out 5,408 synthetic + 896 real training entries; design P 18,906 training entries, 56 test specimens | `docs/handoff/DATASET_USAGE.md` 3.3; `ssn:docs/DATASHEET.md` 2.7 | CURRENT; the corpus and the RSNAI manifest call the source "v2" while the path is v3 (OQ F6) |
| MAN 4 #16 | the row-spacing defect: all 801 `ctsp_drr` renders before the 2026-09-19 respace (median error 7.5 %, more than 1.2x off on 172); 181 of 374 `verse_soft_drr` still | `memory/drr-row-spacing-defect.md`; `ssn:data_platform/DATA_MANIFEST.md` section 4 row 16 | CURRENT defect; only `sweep_v3` numbers count |
| MAN 4 #17-19 | `verse_drr` holds 13 byte-identical `glgl*` duplicates; `ctsp_drr_obl*` are VerSe renders under a CTSP prefix; `anchor_drr`'s split puts 301 of 801 people on both sides; `ts_drr` path maps were computed from the v3 root | `ssn:data_platform/DATA_MANIFEST.md` section 4 | CURRENT defects |
| A18 / OQ F6 | Table 1 of paper 1 counts `ts_drr` and `ts_drr_v3` (never read by v9) and omits `physics_drr` and `physics_rare`; the footnote total 4,093 renders needs recomputing from the v9 build roots | `docs/handoff/OPEN_QUESTIONS.md` F6; `docs/handoff/DATASET_USAGE.md` 6 | OPEN (action F6) |

## 2. Device cards and the sampler (A12; DEVICE_PARAM_AUDIT; DEVICE_SPREAD_SWEEP)

| id | claim | file | status |
|---|---|---|---|
| A12.1 | held-out R^2, card vs uncalibrated physics: Cios Fusion 0.905 vs 0.899 (40 / 366 frames); BV Pulsera 0.952 vs 0.917 (40 / 116); Elekta XVI 0.974 vs 0.964 (40 / 335); PIXIUM 4600 0.679 vs 0.650 (14 / 18) | `results/devices/<device>.json#physics_terms`; each card's `fit` block stamps the fit: `fit.code_sha` 6e1cf8d and `fit.date` 2026-09-22 (06:32 Pulsera, 06:43 Cios, 06:55 PIXIUM, 07:57 Elekta); `docs/handoff/RESULTS_CATALOG.md` A12 header gives the same hash | CURRENT (Table S1, Figure S3) |
| A12.2 | gain on the 12 patient-held-out folds (Cios, Elekta; 701 frames): +0.019 [0.008, 0.033]; frame-weighted 0.023 [0.010, 0.033]; 2 of 12 negative; sign-flip P = .004, Holm .009 | `sn:results/eval_gate/leaks/card_gain_unseen.json` | CURRENT |
| A12.3 | within-subject folds (Pulsera phantom, PIXIUM cadaver): 0.056 [0.025, 0.088], not held out (one object each) | same | CURRENT, labelled |
| A12.4 | criterion C3 (every device's gain > 0 with an interval excluding 0) not met: holds on six-fold percentile intervals only; on t intervals only BV Pulsera excludes 0 | `sn:results/a6.json#verdict`; `sn:results/stats_review/recompute.json#R2_card` | CURRENT (not met) |
| A12.5 | a refit with image noise in the loss failed its own acceptance gate on every device; the published parameters stand | `sn:figures/figS2.record.json` panel d; `sn:results/supplement_figs/card_refit/` | CURRENT |
| A12.6 | the exposure clip: `device_style.SPREAD = 0.2` reaches 1.7 to 5.1 % of each device's joint distribution (Pulsera 5.1, Cios 3.3, Elekta 2.4, PIXIUM 5.0, Surgio 2.8, Varian 1.7 %); 94.9 to 98.3 % of styled frames carry a pinned term (3.2 to 4.4 of 8 to 11 terms); the typicality gate (99 % of the joint) is written and asserted by `tools/test_device_gate.py` but the clip is the default | `docs/DEVICE_SPREAD_SWEEP.md`; `docs/DEVICE_PARAM_AUDIT.md`; `memory/device-sampling-audit.md` | OPEN ("a defect not repaired" in the supplement); A/B = `ssn:slurm/device_spread_arm.sh`, not run |
| audit | 51 of 114 device x parameter pairs are drawn per frame from the copula conditioned on water-equivalent thickness; 54 held at the fitted median; 5 physics defaults; 9 read from DICOM headers; 4 harvested but not consumed; Cios Fusion kVp is recoverable from 2,654 vendor DICOM frames (84 values) | `docs/DEVICE_PARAM_AUDIT.md`; `memory/device-sampling-audit.md` | CURRENT (generated from the cards) |
| A12.7 | the 24-fold gain +0.0376 [0.0205, 0.0573] | older supplement text | SUPERSEDED [LEAK] (two devices have one subject) |
| A12.8 | `docs/devices/surgio_b51_dr.json` exists only on the grid; the C-arm inventory's own `ls` of 2026-10-08 also lists `varian_halcyon` (with `surgio_b51_dr/raw` and `surgio_b51_dr/display`) under `$RS/data/or_ready/devices`; the project 10 listing of the same day shows `devices` with 8 entries and no names | `sn:results/DATA_CONTRIBUTION.md` correction ix; `../_plan/inventories/carm_hospital_path.md` line 186 and `.tsv` rows 24 and 100 (notes column); `../10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` line 1689 | fact; the eight names are `TODO.md` step 25 |
| E.11 | device-level claims cannot be tested with four devices: the smallest two-sided sign-flip P is 0.125 | `docs/handoff/literature_state/power.md` section 6 | CURRENT |

## 3. The DeepFluoro calibration and the physics line (C4, C3.10, C3.11; DEEPFLUORO_FORMATION)

| id | claim | file | status |
|---|---|---|---|
| DFF 1 | the projection convention scores 0.00 px median and p90 over 111 landmark reprojections; volume indexed (z, y, x); focal -5257.7 px kept signed; 1020 mm SID; 160 of 366 frames stored upside down | `docs/DEEPFLUORO_FORMATION.md` section 1; `memory/deepfluoro-convention.md` | CURRENT |
| C4.2 / DFF 2 | exact geometry plus attenuation explains 80.9 % of a real frame's attenuation variance (366 frames, NCC median 0.899); nine terms add +4.1 leave-one-specimen-out, +4.3 in v2 (`calibration_best.json`); ceiling 99.5 %; a learned refiner better on 21 % of frames only | `docs/DEEPFLUORO_FORMATION.md` sections 2 and 5; `memory/learned-formation-refuted-calibrate-instead.md` | the decision stands; numbers RECORD ONLY |
| C4.1 | render-only detector on DeepFluoro real frames, sacrum recall 76.9 % (by specimen 47.8 to 96.2 %; the seed alone moves 26 points); about 40 % before the upside-down fix | same | RECORD ONLY; the audit track reads the v2 generation at 64.0 % pooled with 18-1109 truly held out (`docs/or_ready_audit_track_2026-09-22.json`) |
| C4.3 | DeepFluoro frames were converted as a log of a log; fix `DF_CONVERSION=linear`; whether the cards were refitted afterwards is not confirmed in any file read | same; `docs/handoff/OPEN_QUESTIONS.md` B9 | OPEN |
| C4.4 | learned arms vs none on TotalSegmentator renders: none_v2 64.0 %; rffull 71.7, rfhp 72.2, fda 74.2 %; pairs 90.0 to 95.0 % | `tools/deepfluoro_anchor_report.py`; the memory note | RECORD ONLY |
| C3.10 | linking under physics: boxes given 99.74 % clean / 71.73 % physics; detector boxes 39.52 / 21.50 % at conf 0.05; detection is the binding constraint (about sixty points) where realistic physics costs eleven to twenty-eight | `docs/PHYSICS_LINKING.md`; `docs/HANDOFF_PHYSICS.md`; `ssn:results/physics/` | the finding is CURRENT; numbers RECORD ONLY; nothing measured under `--perturb physics` before the bone-path fix is quotable |
| C3.11 | three physics defects: only the AEC extrapolation changed an image (PIXIUM 4,607 to 103,084 photons/mm^2 once capped); the display window hides the lateral spine | `docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md`; `memory/physics-three-defects-measured.md` | RECORD ONLY |
| SIM | the simulation is checked against five outside numbers; four agree; the fifth disagrees because the real images had been through a printing press | `docs/SIMULATION_FIDELITY.md` | record |
| census | water-path census over 801 CTSP, 30 VerSeFusion and 1,069 TotalSegmentator spines: lumbar path median 31.2 cm (n 5,517), thoracic 25.9 (n 10,897), cervical 17.9 (n 2,044) | `docs/path_census.json` | record |

## 4. The styled device corpus and its detectors (A6.11 to A6.13, A7.8, C4.6; MODEL_CARD 4.6; LEAKAGE 3)

| id | claim | file | status |
|---|---|---|---|
| C4.6 / MC 4.6 | styled-corpus leave-one-device-out, `DEVICE-HELD-OUT` rows: Cios Fusion held out 0.9157 (A), 0.9157 (A seed 1), 0.9398 (B) vertebra recall, sacrum 1.000 (104 frames); Elekta XVI 0.3024, 0.3135, 0.3270 (648 frames; sacrum 0.30 to 0.36); one training device only 0.1221; Surgio-B51 0.1429 (A seed 1), 0.1498 (B seed 1) (56 frames; sacrum 0.82 to 0.86) | `~/spine-detector/runs/devcorpus/*/scores.json`; `ssn:docs/MODEL_CARD.md` 4.6 | SUPERSEDED by the contribution-matrix scoring for the paper; the box convention of these rows is not recorded; `dc_B_held_cios_fusion_s1` has no row (OQ B10) |
| A6.13 | the pre-stated counting-grade target (>= 97 % vertebra and sacrum, `ssn:docs/RSNAI_PLAN.md` C7) is met by no held-out cell; `MODEL_CARD.md` writes "not met on two of the three devices" although its own Cios row (91.6 to 94.0 %) is below 97 %; the primary C7 criterion (paired bootstrap against the LODO baseline) was never run | `ssn:docs/MODEL_CARD.md` 4.6 | CURRENT (not met) [WORDING in MODEL_CARD] |
| A6.11 | design B (styled renders of the other two devices + their real frames): C-ArmLSpine 63.1 % (181 / 287) at 0.74, 87.8 % at 0.25; COBRA 10.1 / 32.7 %; DeepFluoro 69.9 / 94.0 % | `sn:results/a1.json` | CURRENT (Table S2) |
| A6.12 | renders only: C-ArmLSpine 0.3 % (1 / 287) at 0.74, 31.7 % (91 / 287) at 0.25 | `sn:results/a1.json` | CURRENT (supplement) |
| A7.8 | renders plus other devices' real frames (design B) hurt on the C-arm at 0.74 (63.1 vs real-only 80.5) and help on the Elekta kV imager (32.7 vs 18.5 at 0.25) | `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` Table G | HELD-OUT reading |
| MC 4.6 (3) | k = 1 to k = 2 training devices moves Elekta from 0.1221 to 0.3024 vertebra recall: one point, one seed, no interval | `ssn:docs/MODEL_CARD.md` 4.6 | real but uninterval'd |
| C2.3 | the `eval_scaling_curves` devices axis was measured at k = 1 for three held-out devices and k = 2 for Elekta only; one derivable cell (Elekta held out, Cios-only design A, 38.1 % [32.3, 44.5] at 0.25) | foot of `ssn:slurm/eval_scaling_curves.sh` | PARTIAL; superseded |
| LEAK 3 | design A renders every card under the Cios Fusion pose pool, which includes DeepFluoro test specimen 18-1109; design B does not and reads higher; only design P's list builder refuses a subject on two sides | `docs/handoff/LEAKAGE.md` section 3 "Device designs"; `sn:results/DATA_CONTRIBUTION.md` 6 | CURRENT exposure; the audit over every device-corpus training list is OQ C15 |
| A14.1 | 17 NHANES II lumbar spines neither detector saw, conf 0.05: film-trained 99.4 % (160 / 161) vs render-trained (`anchor_det_v1`, 6,650 renders, no real image) 67.7 % (109 / 161), +31.7 points [21.0, 45.4]; at 0.25 98.8 vs 34.8 % | `sn:results/eval_gate/leaks/render_vs_film_unseen_rerun.json` (job 40429839) | CURRENT, HELD OUT |
| A14.2 | the 25-spine version 99.14 vs 71.67 %, +27.5 | older text | SUPERSEDED [LEAK] |

## 5. Angle, coverage and the oblique arc (A11)

| id | claim | file | status |
|---|---|---|---|
| A11.1 | matched-N render-only detectors (Surgio card, 2,646 renders of 125 subjects) scored on 40 unseen TotalSegmentator subjects over 19 lateral bins: `low` 82.1 % at trained angles, 52.8 % over 16 untrained bins, 57.4 % all; `low2n` 94.2 / 64.8 / 69.5 %; `high` (arc poses) 80.7 / 77.1 / 77.7 % | `sn:results/power/power.json#panel_d_angle/summary`; `sn:results/coverage/experiment/EXPERIMENT.md` | CURRENT on renders; caveat: the Surgio card renders thick laterals photon-starved, so the +/-90 degree bins mix geometry with underexposure |
| A11.2 | Elekta XVI arms printed "scored zero"; `EXPERIMENT.md` shows 0.0 for four arms and 1.6 % / 0.4 % for the two low2n seeds | `EXPERIMENT.md`; `sn:generated/numbers_audit.md` | CURRENT [WORDING] |
| A11.3 | the same render-only arms on the real Surgio test: 0.7 to 9.1 % whatever the coverage | `EXPERIMENT.md`; `PER_LEVEL_DOMAIN_ANGLE.md` Table G | HELD-OUT, NOT QUOTED |
| A11.4 | one real 301-frame rotational acquisition (case134): pooled detector 93.6 % of bodies at 0.25; the reported held-out detector 49.5 %, "exactly half of the boxes in 15 of 19 bins" | `sn:figures/figS4.record.json`; `sn:results/arc/case134_sweep.md` | CURRENT; cause OPEN, recorded as unexplained |
| A11.5 | nested pooled fit over 105 points: coverage term g = +19.96 points per unit H*_lat [12.24, 27.69] at conf 0.25; at 0.74 it reverses (g -0.7 [-8.8, +7.4]); g is identified only by the two render-arm corpora | `sn:results/coverage/pooled_fit.json`, `POOLED_FIT.md` | CURRENT [THR] |
| A11.6 | real Surgio pose pool: 148 AP + 148 lateral, none between 10 and 60 degrees; 3 of 18 lateral bins; the case134 spin covers 83 % of lateral bins | `sn:results/coverage/coverage.json`; `sn:results/arc/audit/pose_pools.json` | CURRENT |
| A11.7 | unseen render angle sweep, pooled detector: below 90 % of its AP recall by +/-30 degrees on both cards | `sn:results/arc/recall_vs_angle_unseen/recall_vs_angle.json` (job 40428072) | CURRENT (replaced the leaked curve, EVAL_LEAKS L1) |
| A11.8 | per-angle naming does not exist; detection per angle exists only on case134, the 40-subject render arc and COBRA gantry bands | `PER_LEVEL_DOMAIN_ANGLE.md` | OPEN |

## 6. The corpus manifold (A13; results/manifold)

| id | claim | file | status |
|---|---|---|---|
| A13.1 | film vs fluoroscopy, one corpus held out (19 corpora, 7,311 frames): -0.7 to +9.2 points over the 71.8 % majority share; no percentile interval excludes zero; two knn15 BCa intervals do | `sn:results/a2.json#corpus_manifold/excess_over_chance`; `sn:results/corpus_manifold/` | CURRENT; all three feature spaces reported |
| A13.2 | films vs C-arm + kV frames, one source held out (5,797 frames): image statistics 63.4 % [57.6, 69.2] vs majority 64.4 %; deep features 85.0 % [79.4, 90.0] | `results/manifold/probes.json`; `sn:figures/figS1.record.json` | CURRENT (Figure S2) |
| A13.3 | styled renders vs the device's real frames stay separable: Cios 100 % (n 736), Surgio 99.8 % (666), Elekta 99.0 % [98.1, 99.6] (771) | `results/manifold/probes.json` | CURRENT |
| A13.4 | per-device overlaps, Bhattacharyya 0.005 (DeepFluoro-Geneva) to 0.675 (Elekta-Geneva) | `results/manifold/overlap.json`; `memory/film-fluoro-boundary-not-transferable.md` | HELD-OUT, NOT QUOTED |
| A13.5 | first manifold (37 corpora): every held-out C-arm corpus labelled FILM; LOFO pooled 71.1 % vs chance 71.8 % | `$RS/data/or_ready/corpus_manifold/overlap.json` | SUPERSEDED by A13.1 |
| FG | what the cards do not reproduce (Cohen's d, styled vs real, 2,000 cluster resamples): Cios `field_frac` +14.19 (no term: collimation); Surgio `penumbra_px` -2.03 (no term: focal spot) and the noise-power terms -2.3 to -3.4; Elekta `border_halo` +1.15 (no term: collimator scatter) and `p1` -4.48 | `results/manifold/formation_gap/FORMATION_GAP.md`, `formation_gap.json` | CURRENT diagnosis |

## 7. Renders as support for film naming (A10.6 to A10.12; project 07 quotes these)

| id | claim | file | status |
|---|---|---|---|
| A10.6 | render-only minus film-only at N = 5 persons: NHANES +21.9, BUU +11.1, CSXA +18.7 points, every seed separated | `sn:results/coverage/film_ncurve/ablation/READ.md`, `ablation_read.json` | CURRENT, HELD OUT |
| A10.7 | at N = 25: +12.2, +6.0, +6.2, every seed separated | same | CURRENT |
| A10.8 | at every person: NHANES +0.7, CSXA -0.2, BUU -1.6 separated (renders hurt) | same | CURRENT [ONE-SEED] |
| A10.9 | seven of nine verdict cells separated: six help, one hurts | same | DISPUTED against `memory`'s "all help" (`film-ncurve-ablation-result` is in project 07, SUPERSEDED reading); trust `READ.md` |
| A10.10 | ImageNet init sits between; most of the scarce-N gain is the render rows, 2 to 5 points is pretraining; at 100 and 200 persons nothing separates | same | CURRENT |
| A10.11 | the synthetic:real ratio was about 1:1 by rows in every cell (`ssn:tools/merge_banks.py` line 60, `real_share` 0.5; 15,374 render rows per cell) while the distinct-image ratio ran 615:1 to 0.75:1; never swept | `PER_LEVEL_DOMAIN_ANGLE.md` Table A | CURRENT fact |
| C2.1 | the 2026-09-17 render-fraction sweep (render fraction 0 / 0.25 / 0.5 / 1.0: anomalous 34.0 / 44.7 / 53.2 / 36.2 %) | `sn:results/indomain/grid/scaling_curve_2026-09-17.json` | SUPERSEDED [LEAK] [SEL-SPLIT]: v2 bank, selection split; the only render-ratio sweep ever run, on a superseded line |

## 8. PolyPose (G.6, G.7; results/polypose)

| id | claim | file | status |
|---|---|---|---|
| G.6 | DeepFluoro reproduction REPRODUCED: pelvis Dice 0.992(0.005) against the paper's 0.99; left femur 0.978(0.009), right 0.980(0.007); HD95 pelvis 1.034(0.077) px; folds 0.0001 to 0.011 % per subject; one deviation (every packaged pose right-multiplied by diag(-1,-1,1,1), measured in `report/diag*`); the six HF subjects are byte-identical to the H5 specimens | `results/polypose/REPRODUCTION.md`, `REPRODUCTION.json`, `report/` | REPRODUCED |
| G.6 | `VALIDATION.{json,md}` does not exist (the chain `slurm/polypose_validate_submit.sh` was written; `tools/polypose/validation_report.py` is the reporter); whether any training bank used PolyPose is not recorded | `memory/polypose-generator-build.md`; `docs/handoff/OPEN_QUESTIONS.md` C18 | OPEN |
| validation/ | what the validation chain did produce: `validation/inspect/inspect.json` and 22 sagittal PNGs (the pre-generation inspection of the 22 validation cases: shape, zooms, axcodes PIR, label ids, `retired_29: false`, body-mask alignment), and one generated smoke variant `pp_ctsp_0874_v000` (manifest row 2026-09-23T22:35:26Z on node alh3, 190.5 s, sampler commit 1001a82, label scheme v11, subtype ordinary, bank `$RS/data/polypose/validation/smoke`) with its AP and lateral renders; no report was written from it | `results/polypose/validation/` | started, not reported (TODO step 2) |
| G.6 | the generator commit 1f4418f (2026-09-23): the memory note says "never pushed"; on 2026-10-08 the laptop checkout's `git branch -a --contains 1f4418f` lists `remotes/origin/L6_Class` and `git merge-base --is-ancestor` puts it under both 4e3fe93 (the grid checkout) and 097933a; GitHub's live state was not checked (no network) | `MANIFEST_CODE.md` | the note is outdated on the laptop's evidence |
| SPEC | sampling spec version 2 (2026-09-23): joint draw (SS, LL, TK | PI) with means PI 52.0, LL 57.4, TK 37.4, SS 39.5 and SDs 10.7, 11.3, 10.9, 8.2; segmental ranges of motion from Wilke 2017, Oxland 1992, Yamamoto 1989 (L4-L5 14.7 degrees flexion-extension); the checker recomputes every number and exits non-zero on a mismatch, last clean run 2026-09-23 | `results/polypose/SAMPLING_SPEC.md`, `sampling_spec.json`, `joint_model_numbers.json`; `docs/polypose_segmental_rom.csv`; `docs/polypose_reference_envelope.json` | CURRENT |
| cine | `rom_cine.json` (2026-09-26, untracked on the laptop): per-segment flexion/extension caps for the synthetic flexion-extension cine (`tools/polypose/cine_render.py`, untracked) | `results/polypose/rom_cine.json` | record; commit it (TODO step 2) |
| G.7 | the old ostk-primitive path read PI 3.6 / LL -8.9 on PIR case 0874 (truth 53 / 54); PolyPose measures through the release plate fits | `memory/polypose-generator-build.md` | CURRENT trap |
| A27 | prior art: no published method manufactures a transitional vertebra; the only measured lever for transitional scarcity is real rare cases oversampled (VERIDAH: thoracic-anomaly recall 96.30 to 25.93 % on CT when the anomalous cases are deleted); PolyPose adopted as the one published mechanism | `docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md`; `docs/research_notes/spine synthesis prior art/` | literature record (nothing run) |

## 9. The refuted translation routes and the ratio literature

| id | claim | file | status |
|---|---|---|---|
| C4.11 / RD 1.4 | the three measured sim-to-real levers: simulation fidelity (naive DRR to DeepDRR 78.2 to 24.7 mm), strong domain randomisation (SyntheX 6.44 mm with zero real images vs 6.46 real-trained), scale (1k to 10k renders 6.61 to 5.95 mm); CycleGAN 6.62 and ADDA 6.41 vs 6.44 with no adaptation: refuted | `memory/drr-to-fluoro-levers.md`; `docs/handoff/RESEARCH_DIRECTIONS.md` 1.4 | CURRENT finding (published numbers) |
| FGS | SDXL img2img over DRRs dead at every strength (0.45 to 0.65 destroyed anatomy, 12,896 images; 0.2 unchanged; 0.35 smears end-plates); CUT v2 moved the films-only model 12.1 to 14.1 % on rare renders and the render-trained all-spine model dropped 33.5 to 23.7 and 51.0 to 36.6 held out; registry alias `cut_drr2fluoro_G_v2`; do not train CUT v3 | `memory/fluorogen-synthetic.md`; `~/FluoroCap/cut_eval_{films,allspine}_*_v2.json` | REFUTED (DATED note) |
| RD 2.2 | render-to-fluoro translation, SDXL, CUT, CycleGAN, ADDA: no gain in any arm | `docs/handoff/RESEARCH_DIRECTIONS.md` 2.2 | REFUTED |
| C4.10 | film vs fluoroscopy: devices separate pairwise; the modality boundary does not transfer to an unseen corpus | `memory/film-fluoro-boundary-not-transferable.md` | CURRENT |
| SRE | no DRR paper has swept the synthetic:real ratio; adjacent sweeps flatten at 4:1 to 10:1 with real at 10 to 20 %; in pretrain-then-fine-tune the ratio stops mattering; Barr 2026 synthetic prior worth 2.6 to 4.3x at 100 to 400 real films, gone at 600 to 700; VerSe L6 became learnable with 85 distinct scans, T13 with 6 never stabilised | `docs/Synthetic real ratio X-ray detectors.md` (119 citations); `docs/research_notes/Synthetic real ratio X-ray detectors/`; `memory/synthetic-real-ratio-evidence.md` | CURRENT literature |
| LS 2D | synthetic sets not held (FluoroSAM fluoroseg about 3 M images, PENGWIN Task 2 50,000 DeepDRR renders, Barr 2026 20,063 DDPM radiographs, Huang 2022 10,368 long films, 2D3D-RegQuality, SyntheX deposit not carded): fetch only if a use appears | `docs/handoff/LITERATURE_STATE.md` section 2 D | record |

## 10. What is superseded, and by what

| superseded item | replaced by |
|---|---|
| A12.7 (24-fold card gain +0.0376) | A12.2 (12 patient-held-out folds, +0.019) |
| A13.5 (first manifold, 37 corpora) | A13.1 (19 corpora, three feature spaces) |
| A14.2 (25-spine render vs film detector) | A14.1 (17 unseen spines) |
| C2.1, C2.2 (the 2026-09-17 render-fraction sweep on the v2 bank) | nothing: no clean ratio sweep exists (TODO step 5) |
| C4.6 (`scores.json` LODO rows of MODEL_CARD 4.6) | the contribution-matrix scoring (A7) for the paper; the rows themselves wait on OQ B10 |
| C4.1, C4.2, C4.4, C3.10, C3.11 numbers | record only; the decisions (calibrate, do not learn; detection is the binding constraint) stand |
| `memory/sweep-physics-no-bone.md` causal claim | `memory/physics-three-defects-measured.md` |
| `memory/fluorogen-synthetic.md` grid paths and login-node downloads | DATED; the verdicts stand; downloads run in jobs now (rule 7) |
| the "never pushed" sentence of `memory/polypose-generator-build.md` | section 8 above |
