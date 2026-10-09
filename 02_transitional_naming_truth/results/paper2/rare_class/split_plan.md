# G3 split plan -- people per side, per subtype, per corpus

Written by `tools/make_split.py` (plan 2026-09-23 20:02:12, apply 2026-09-23 20:18:48), seed 0. Generated; do not edit by hand. Re-run: `sbatch -D $HOME/spinesurg-ct-nnunet --export=ALL,STAGE=all SchwingNet/slurm/g3_split.sh`.

Inputs: `transitional_subtypes.csv` (sha256 65751ac53ec3, 196 rows); COBRA screen 692 jsons over 692 cases (digest a16aa3c784b1); keys `/wsu/home/go/go24/go2432/patient_keys_final.json`; prior SchwingNet/results/rare_class/stratify.json (2026-09-23 19:48:08) frozen.

**Leak audit: PASS.**

## The rule

- Unit: the person key, after the alias folds (implant -> source CT, VinDr image -> study, VerSe series -> subject, TotalSegmentator v201<->v300 by CT md5 and shape+affine, the spec's declared duplicates).
- G1 transitional people (not real): 50/10/40 train/val/test by exact allocation within each subtype. The G1 inventory holds 194 transitional persons (>= 150), so the small-inventory rule (test 50 %) does not apply. Read on the whole G1 inventory (194 persons), because its own arithmetic is inventory-level (150 x 0.4 = the 60-person test target); every single subtype is below 150, so a per-subtype reading would make the rule the default.
- Small cells: exact largest-remainder allocation per subtype, ties to test then val; 2+ people -> >=1 test, 3+ -> >=1 val (taken from train). Within a subtype: (corpus, stratum, hash) dealt in a stride pattern.
- Real transitional subjects: test, outside the quotas.
- COBRA: a held case whose hash side is test is in test now; otherwise it is on no side until the screen calls it, then test (transitional / re-read) or side_if_released. A later screen call can only add a person to test or release a held person; it cannot move anyone who has a side now.
- Everyone else: u = int(sha256('g3|<seed>|<key>').hexdigest()[:13], 16) / 16**13; train u<0.8, val u<0.9, else test. It depends on the key alone: adding a root or a person moves nobody.
- Corpus policies: spinalai train, geneva test, geneva_hip test, ljubljana test, fluorocap excluded, fluorocap_video excluded, mendeley excluded; DeepFluoro exact {'train': 4, 'val': 1, 'test': 1}.
- Merged groups: test > hold > val > train (a merged group takes its most held-out member's side).

## Transitional people per side, per subtype (G1 table, verified)

`in v8/v9 train` counts val/test people that a level encoder trained on; a model descending from those banks cannot score them (docs/DATA_ACCOUNTING.md s5.2), so for such a model they are not evidence.

| subtype | people | train | val | test | per corpus (train/val/test) | val+test people in v8 or v9 train |
|---|---:|---:|---:|---:|---|---:|
| L6 | 107 | 53 | 11 | 43 | ctsp 9/2/7, ts 1/0/2, verse 43/9/34 | 49 of 54 |
| T13 | 7 | 3 | 1 | 3 | ts 0/0/1, verse 3/1/2 | 4 of 4 |
| sacralised_L5_fused | 28 | 14 | 3 | 11 | ctsp 6/1/5, verse 8/2/6 | 14 of 14 |
| castellvi_I_II | 31 | 16 | 3 | 12 | ctsp 2/0/2, verse 14/3/10 | 15 of 15 |
| lumbar_rib | 14 | 7 | 1 | 6 | ctsp 7/1/6 | 7 of 7 |
| unassigned | 4 | 1 | 1 | 2 | ctsp 1/1/2 | 3 of 3 |
| both_L6_T13 | 0 | 0 | 0 | 0 | no spine carries both in any truth table | |
| four_lumbar (primary) | 0 | 0 | 0 | 0 | a modifier of sacralised_L5_fused in G1; COBRA calls below | |

Mask strata inside the subtypes (train/val/test): L6/audit_only 18/4/14; L6/audit_only+raw_mask 1/0/1; L6/raw_mask 24/5/19; L6/release_id_25 9/2/7; L6/verified_count 1/0/2; sacralised_L5_fused/four_lumbar_unchecked 1/1/1; sacralised_L5_fused/merged_into_sacrum 4/1/4; sacralised_L5_fused/own_id 9/1/6.

## Real transitional subjects (all in test)

- C-ArmLSpine (CBCT labels, real intraoperative frames): carmlspine:case121, carmlspine:case136, carmlspine:case42 -- L6 test, L6 test, L6 test.
- COBRA screen transitional calls (SPINEPS+VERIDAH on the deformed planning CT, **unverified**): 91 -- L6 38, T13 45, four_lumbar 8.
  Of the L6 calls, 27 see no L1 (e.g. 'lumbar seen: L5+L6'): the field of view cuts the lumbar spine, so the count behind the call cannot be made -- the screen types the same field 'unreadable' when no 25 is named. 7 T13 calls name only L1-L4 above the sacrum: by VERIDAH's own names that is 13 + 4 = 17 thoracolumbar vertebrae, the ordinary count, so the call is a naming shift at the thoracolumbar junction, not an extra vertebra. Both kinds are in test, which is safe; neither may be counted as a transitional test person until verified.

## COBRA -- every case of the catalogue

| screen status | train | val | test | hold | what a later call does |
|---|---:|---:|---:|---:|---|
| transitional_call | 0 | 0 | 91 | 0 | nothing (test) |
| reread_candidate | 0 | 0 | 3 | 0 | nothing (test) |
| ordinary_call | 259 | 44 | 41 | 0 | nothing |
| fov_limited | 186 | 27 | 23 | 0 | nothing |
| not_screened | 0 | 0 | 0 | 0 | held -> test (transitional) or its drawn side |
| not_named_from_ctd | 0 | 0 | 0 | 11 | same as not_screened |
| screen_failed | 0 | 0 | 1 | 6 | same as not_screened |

## Every person, per corpus (after the folds)

| corpus | train | val | test | hold | excluded |
|---|---:|---:|---:|---:|---:|
| aasce | 178 | 14 | 25 | 0 | 0 |
| buu | 2926 | 331 | 341 | 0 | 0 |
| carmlspine | 123 | 13 | 13 | 0 | 0 |
| cobra | 445 | 71 | 159 | 17 | 0 |
| csxa | 3979 | 485 | 499 | 0 | 0 |
| ctsp | 636 | 73 | 93 | 0 | 0 |
| deepfluoro | 4 | 1 | 1 | 0 | 0 |
| fluorocap | 0 | 0 | 0 | 0 | 1616 |
| fluorocap_video | 0 | 0 | 0 | 0 | 337 |
| geneva | 0 | 0 | 19 | 0 | 0 |
| lat236 | 193 | 22 | 21 | 0 | 0 |
| mendeley | 0 | 0 | 0 | 0 | 51 |
| nhanes | 7673 | 969 | 939 | 0 | 0 |
| spinalai | 44 | 0 | 0 | 0 | 0 |
| ts | 1469 | 193 | 205 | 0 | 0 |
| verse | 252 | 35 | 68 | 0 | 0 |
| vindr | 4019 | 475 | 487 | 0 | 0 |

## Leak checks (docs/DATA_ACCOUNTING.md s5)

| check | status | count | what it tests |
|---|---|---:|---|
| CHK-1 | PASS | 0 | item disjointness: no (root, case) item carries two sides |
| CHK-1b | PASS | 0 | a consumer of the flat {case: key} in ~/patient_keys_final.json gets every ann item's own side (case-name collisions between roots, and raw keys a fold changes, spec s5.4) |
| CHK-2 | PASS | 0 | alias closure: 62 alias edges (TS md5 26 groups, TS shape+affine 27 groups, spec s3 declared 7) on one side; 20 of them would straddle without the merge |
| CHK-3 | PASS | 0 | patient closure: no person (after every fold) has items on two sides, over every root |
| CHK-3b | PASS | 0 | patient closure seen through tools/leak_check.RULES (175749 items keyed by it, 53564 not): no leak_check person has items on two sides of this split. A hit is an identity the two keyers disagree on -- read it before trusting either |
| CHK-4 | PASS | 0 | derivation closure: every derived item (implant variant, pose-donor render, PolyPose variant, VerSe series, VinDr image, Dataset813 token) is keyed to its source person, so it sits on that person's side; 9634 of them would have drawn another side under their raw key. By fold: {'supp.implant (folded)': 6339, 'patient_keys (folded)': 6036, 'supp.verse_view (folded)': 594, 'supp.vindr (folded)': 15417, 'supp.pose_donor': 33564} |
| CHK-4b | WARN | 8082 | training renders drawn under the POSE (C-arm geometry, no anatomy) of a val/test/held real subject -- reported, not failed: {'deepfluoro test': 1143, 'deepfluoro val': 4415, 'cobra test': 992, 'cobra val': 299, 'cobra hold': 159, 'carmlspine test': 585, 'carmlspine val': 489} |
| CHK-5 | PASS | 0 | held out whole: every real transitional subject (C-ArmLSpine CBCT-label L6, COBRA calls, re-read candidates) has every item in test; no held COBRA case has an item on train/val; single-object corpora (geneva, ljubljana) wholly test, spinalai wholly train. Device hold-outs are the LODO arms' business, not this split's |
| CHK-6 | NOT RUN |  | near-duplicates across splits (pixel NCC ladder; slurm/data_accounting.sh) |
| CHK-7 | NOT RUN |  | undeclared alias by store/pixel key (needs the ledger of slurm/data_accounting.sh); the TS md5 and shape+affine folds are the only content keys read here |
| CHK-8 | WARN | 17 | coverage: every item of every root keyed (the unkeyed are named per root; a bank must refuse them) |
| CHK-8b | PASS | 0 | every stratified person has at least one item in some root |

CHK-8 detail (first 20):

- `/wsu/home/go/go24/go2432/aasce_drr: 17 (e.g. ['AASCE_sunhl-1th-20-Jul-2016-coronal1', 'AASCE_sunhl-1th-20-Jul-2016-coronal10', 'AASCE_sunhl-1th-20-Jul-2016-coronal11'])`

## Roots keyed

| root | kind | items | keyed | unkeyed |
|---|---|---:|---:|---:|
| `/rs/rs_grp_oschome/go2432/data/devcorpus/render/cios_fusion` | npz | 1679 | 1679 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/render/elekta_xvi` | npz | 1264 | 1264 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/render/surgio_b51_dr` | npz | 1657 | 1657 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/cios_fusion__cios_fusion` | images | 3074 | 3074 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/cios_fusion__cios_fusion__typicality` | images | 3074 | 3074 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/cios_fusion__elekta_xvi` | images | 3074 | 3074 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/cios_fusion__elekta_xvi__typicality` | images | 3074 | 3074 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/cios_fusion__surgio_b51_dr` | images | 3074 | 3074 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/cios_fusion__surgio_b51_dr__typicality` | images | 3074 | 3074 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/elekta_xvi__elekta_xvi` | images | 2244 | 2244 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/elekta_xvi__elekta_xvi__typicality` | images | 2244 | 2244 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/surgio_b51_dr__surgio_b51_dr` | images | 3016 | 3016 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus/styled/surgio_b51_dr__surgio_b51_dr__typicality` | images | 3016 | 3016 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep/elekta_xvi` | meta | 969 | 969 | 0 |
| `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep/surgio_b51_dr` | meta | 969 | 969 | 0 |
| `/rs/rs_grp_oschome/go2432/data/polypose/validation/bank_gravity` | ann | 0 | 0 | 0 |
| `/rs/rs_grp_oschome/go2432/data/polypose/validation/bank_invdf1` | ann | 0 | 0 | 0 |
| `/rs/rs_grp_oschome/go2432/data/polypose/validation/kernel_exp` | ann | 0 | 0 | 0 |
| `/rs/rs_grp_oschome/go2432/data/polypose/validation/kernel_exp_cpu` | ann | 0 | 0 | 0 |
| `/rs/rs_grp_oschome/go2432/data/polypose/validation/smoke` | ann | 0 | 0 | 0 |
| `/rs/rs_grp_oschome/go2432/data/rare_class/carmlspine_cbct_drr` | ann | 396 | 396 | 0 |
| `/rs/rs_grp_oschome/go2432/data/rare_class/ctsp_drr` | ann | 2834 | 2834 | 0 |
| `/rs/rs_grp_oschome/go2432/data/rare_class/totalsegmentator_drr` | ann | 933 | 933 | 0 |
| `/rs/rs_grp_oschome/go2432/data/rare_class/verse_drr` | ann | 3920 | 3920 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine` | meta | 299 | 299 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_multi` | images | 5212 | 5212 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_pre_repair_2026-09-23` | meta | 296 | 296 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep` | meta | 301 | 301 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta` | meta | 3480 | 3480 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta_ap45` | meta | 1634 | 1634 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta_smoke` | meta | 24 | 24 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta_v2` | meta | 3480 | 3480 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta_v2_ap45` | meta | 1634 | 1634 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta_v3` | meta | 3480 | 3480 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/deepfluoro` | meta | 366 | 366 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/geneva_hip` | meta | 116 | 116 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/pelvis_landmarks/cobra_elekta` | meta | 3120 | 3120 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/pelvis_landmarks/deepfluoro` | meta | 342 | 342 | 0 |
| `/rs/rs_grp_oschome/go2432/data/realxray/pelvis_landmarks/geneva_hip` | meta | 116 | 116 | 0 |
| `/wsu/home/go/go24/go2432/aasce_drr` | ann | 457 | 440 | 17 |
| `/wsu/home/go/go24/go2432/anchor_drr` | ann | 7844 | 7844 | 0 |
| `/wsu/home/go/go24/go2432/anchor_drr_c2` | ann | 6131 | 6131 | 0 |
| `/wsu/home/go/go24/go2432/carm_cv0_drr` | ann | 226 | 226 | 0 |
| `/wsu/home/go/go24/go2432/carm_cv1_drr` | ann | 246 | 246 | 0 |
| `/wsu/home/go/go24/go2432/carm_cv2_drr` | ann | 240 | 240 | 0 |
| `/wsu/home/go/go24/go2432/carm_cv3_drr` | ann | 224 | 224 | 0 |
| `/wsu/home/go/go24/go2432/carm_cv4_drr` | ann | 248 | 248 | 0 |
| `/wsu/home/go/go24/go2432/carm_cvday0_drr` | ann | 164 | 164 | 0 |
| `/wsu/home/go/go24/go2432/carm_cvday1_drr` | ann | 210 | 210 | 0 |
| `/wsu/home/go/go24/go2432/carm_cvday2_drr` | ann | 218 | 218 | 0 |
| `/wsu/home/go/go24/go2432/carm_drr` | ann | 240 | 240 | 0 |
| `/wsu/home/go/go24/go2432/ctsp_drr` | ann | 802 | 802 | 0 |
| `/wsu/home/go/go24/go2432/ctsp_drr_film` | ann | 802 | 802 | 0 |
| `/wsu/home/go/go24/go2432/ctsp_drr_obl` | ann | 1256 | 1256 | 0 |
| `/wsu/home/go/go24/go2432/ctsp_drr_obl2` | ann | 2511 | 2511 | 0 |
| `/wsu/home/go/go24/go2432/cut_physics` | ann | 3000 | 3000 | 0 |
| `/wsu/home/go/go24/go2432/cut_physics_v2` | ann | 3000 | 3000 | 0 |
| `/wsu/home/go/go24/go2432/cut_rare` | ann | 1482 | 1482 | 0 |
| `/wsu/home/go/go24/go2432/cut_rare_v2` | ann | 1482 | 1482 | 0 |
| `/wsu/home/go/go24/go2432/exp3_fluoro` | ann | 1058 | 1058 | 0 |
| `/wsu/home/go/go24/go2432/exp3_radiograph` | ann | 1058 | 1058 | 0 |
| `/wsu/home/go/go24/go2432/films_ap_drr` | ann | 3600 | 3600 | 0 |
| `/wsu/home/go/go24/go2432/films_drr` | ann | 9109 | 9109 | 0 |
| `/wsu/home/go/go24/go2432/films_drr_buucorr` | ann | 9109 | 9109 | 0 |
| `/wsu/home/go/go24/go2432/films_smoke` | ann | 3 | 3 | 0 |
| `/wsu/home/go/go24/go2432/fluorocap_drr` | ann (excluded) | 2385 | 2385 | 0 |
| `/wsu/home/go/go24/go2432/fluorocap_drr_smoke` | ann (excluded) | 137 | 137 | 0 |
| `/wsu/home/go/go24/go2432/fluorogen/synth_rare` | ann | 12929 | 12929 | 0 |
| `/wsu/home/go/go24/go2432/fluorogen/synth_rare_lowstrength` | ann | 566 | 566 | 0 |
| `/wsu/home/go/go24/go2432/fluorogen/synth_v1` | ann | 0 | 0 | 0 |
| `/wsu/home/go/go24/go2432/lateral236_pseudo` | ann | 236 | 236 | 0 |
| `/wsu/home/go/go24/go2432/lstv_eval/renders60` | ann | 60 | 60 | 0 |
| `/wsu/home/go/go24/go2432/lstv_flag/renders` | ann | 9624 | 9624 | 0 |
| `/wsu/home/go/go24/go2432/lstv_flag/renders_ctrl` | ann | 644 | 644 | 0 |
| `/wsu/home/go/go24/go2432/lstv_flag/renders_verse` | ann | 3456 | 3456 | 0 |
| `/wsu/home/go/go24/go2432/lstv_flag/smoke` | ann | 36 | 36 | 0 |
| `/wsu/home/go/go24/go2432/mendeley_drr` | ann (excluded) | 584 | 584 | 0 |
| `/wsu/home/go/go24/go2432/model_night/vindr_smoke` | ann | 12 | 12 | 0 |
| `/wsu/home/go/go24/go2432/nhanes_drr` | ann | 543 | 543 | 0 |
| `/wsu/home/go/go24/go2432/nhanes_pseudo` | ann | 16234 | 16234 | 0 |
| `/wsu/home/go/go24/go2432/physics_drr` | ann | 7048 | 7048 | 0 |
| `/wsu/home/go/go24/go2432/physics_drr_film` | ann | 7048 | 7048 | 0 |
| `/wsu/home/go/go24/go2432/physics_rare` | ann | 1482 | 1482 | 0 |
| `/wsu/home/go/go24/go2432/physics_rare_film` | ann | 1482 | 1482 | 0 |
| `/wsu/home/go/go24/go2432/physics_smoke` | ann | 14 | 14 | 0 |
| `/wsu/home/go/go24/go2432/postop_render` | ann | 45 | 45 | 0 |
| `/wsu/home/go/go24/go2432/pseudo_filtered/lateral236_pseudo_anchored` | ann | 203 | 203 | 0 |
| `/wsu/home/go/go24/go2432/pseudo_filtered/nhanes_pseudo_anchored` | ann | 10087 | 10087 | 0 |
| `/wsu/home/go/go24/go2432/pseudo_filtered/vindr_pseudo_anchored` | ann | 5131 | 5131 | 0 |
| `/wsu/home/go/go24/go2432/render_smoke/fluoro` | ann | 9 | 9 | 0 |
| `/wsu/home/go/go24/go2432/render_smoke/radiograph` | ann | 9 | 9 | 0 |
| `/wsu/home/go/go24/go2432/spinalai_drr` | ann | 8358 | 8358 | 0 |
| `/wsu/home/go/go24/go2432/ts_drr` | ann | 1170 | 1170 | 0 |
| `/wsu/home/go/go24/go2432/ts_drr_v3` | ann | 1735 | 1735 | 0 |
| `/wsu/home/go/go24/go2432/verse_drr` | ann | 387 | 387 | 0 |
| `/wsu/home/go/go24/go2432/verse_drr_film` | ann | 374 | 374 | 0 |
| `/wsu/home/go/go24/go2432/verse_drr_obl` | ann | 1494 | 1494 | 0 |
| `/wsu/home/go/go24/go2432/verse_drr_obl2` | ann | 2989 | 2989 | 0 |
| `/wsu/home/go/go24/go2432/verse_soft_drr` | ann | 374 | 374 | 0 |
| `/wsu/home/go/go24/go2432/vindr_det_drr` | ann | 2328 | 2328 | 0 |
| `/wsu/home/go/go24/go2432/vindr_pseudo` | ann | 10274 | 10274 | 0 |
| `/wsu/home/go/go24/go2432/vindr_pseudo_drr` | ann | 744 | 744 | 0 |

~/patient_keys_final.json itself lists 80165 unmatched cases (tools/patient_keys.py); the table above re-keys every item per (root, case) with the supplementary forms of the identity spec and names what is still unkeyed. Folds applied: implant->source (by name) 8859, verse series->subject 1038, vindr image->study 18489. Unresolved: none.

Alias groups whose members drew different sides: 10 (each takes its most held-out member's side; `split_leak_report.json` lists them).

## Model exposure (v8 / v9 level banks)

- v8: trained on 9893 people, of whom 1040 are G3 test and 953 G3 val. A checkpoint from this bank (or any descendant) cannot be the initialisation of a model scored on G3 test.
- v9: trained on 9878 people, of whom 1046 are G3 test and 945 G3 val. A checkpoint from this bank (or any descendant) cannot be the initialisation of a model scored on G3 test.

Real-frame roots' own `splits.json` against G3 (their split -> G3 side, cases):

- `carmlspine`: test->test 4, test->train 21, test->val 3, train->test 7, train->train 89, train->val 10, val->test 2, val->train 13
- `carmlspine_pre_repair_2026-09-23`: test->test 4, test->train 21, test->val 3, train->test 7, train->train 89, train->val 9, val->test 2, val->train 13
- `carmlspine_sweep`: test->val 1
- `cobra_elekta`: test->test 6, test->train 21, train->hold 7, train->test 24, train->train 69, train->val 10, val->test 5, val->train 3
- `cobra_elekta_ap45`: test->test 6, test->train 21, train->hold 7, train->test 24, train->train 69, train->val 10, val->test 5, val->train 3
- `cobra_elekta_smoke`: val->train 1
- `cobra_elekta_v2`: test->test 6, test->train 21, train->hold 7, train->test 24, train->train 69, train->val 10, val->test 5, val->train 3
- `cobra_elekta_v2_ap45`: test->test 6, test->train 21, train->hold 7, train->test 24, train->train 69, train->val 10, val->test 5, val->train 3
- `cobra_elekta_v3`: test->test 6, test->train 21, train->hold 7, train->test 24, train->train 69, train->val 10, val->test 5, val->train 3
- `deepfluoro`: loso->? 6, test->train 1, train->test 1, train->train 2, train->val 1, val->train 1
- `geneva_hip`: test->? 1
- `cobra_elekta`: test->test 6, test->train 21, train->hold 7, train->test 24, train->train 69, train->val 10, val->test 5, val->train 3
- `deepfluoro`: loso->? 6, test->train 1, train->test 1, train->train 2, train->val 1, val->train 1
- `geneva_hip`: test->? 1

## Rendered anns whose subtype disagrees with the split's subtype (relabel or exclude)

- totalsegmentator_drr: ts:s1088 ann=T13 stratified=L6: 89 anns
- totalsegmentator_drr: ts:s1123 ann=T13 stratified=L6: 80 anns
- totalsegmentator_drr: ts:s1178 ann=L6 stratified=ordinary: 84 anns

## What a bank builder must do

- Read `~/split_final.json` `item_side` (or `side_of_person` via `group_of`) and never redraw. `tools/make_context_crops.py --stratify-json` refuses this format: it draws its own two-way split.
- Drop `hold` and `excluded` items, and refuse every unkeyed item named above.
- Re-run this after the COBRA screen finishes: held cases are released or added to test; nobody moves.
