# Coupling the morphology classifier to the count from the sacrum: C-ArmLSpine folds and the anomalous renders

Generated 2026-09-24 09:05. Numbers: `SchwingNet/results/coupling.json` (this file quotes it; every table cell is a key there). Tools: `tools/alphabet_couple.py` (the coupler; `--self-test` passes on synthetic posteriors: ordinary, L6 with the sixth body called L5, the same upside down and scrambled, one confident error, no sacrum, the sacrum boxed as a vertebra, variant truth, the confidence floor and the named-sacrum switch), `tools/level_prototype.py --dump-posterior --sacrum-detector`, `SchwingNet/tools/coupling_report.py`, `SchwingNet/tools/sweep_variant_calls.py`; jobs `SchwingNet/slurm/coupling.sh` (GPU array, one fold per task) then `SchwingNet/slurm/coupling_eval.sh` (CPU). Jobs: carmcv9i 40431706 carmcvday9i 40431707 prerep 40436575 carmcv9pre 40436580.

## What was coupled

- **classifier**: the prototype's reported `level` (anchored decode over the blended single-crop + recurrent-head posterior, flip-TTA), the same name every shipped C-ArmLSpine number scores
- **coupled**: A*(n_i) for bodies with an ordinal from the sacrum, the classifier's name otherwise (no anchor -> unchanged)
- **count**: the ordinary alphabet at the ordinal (L5 at 1, L4 at 2, ...): the count alone, no classifier; wrong by construction on an L6 spine
- **score**: S(A) = mean_i log p_i(A(n_i)) over counted bodies, p floored at 1e-9; alphabets sweep_map.alphabet (std: ordinary, L6, T13, both); identical namings are one candidate
- **margin**: S(A*) - S(ordinary), 0 when ordinary wins; margin_next = S(A*) - S(runner-up)
- **anchor**: det: the LODO box detector's class-1 box (rx_lodo_carmlspine_1024, C-ArmLSpine never seen), run on the raw frame, conf >= 0.25 (det) or >= 0.74 (det74); oracle: the truth meta's class-1 box
- **ordinal**: rank of the box centre's projection on the principal axis of all centres, away from the sacrum; a box with IoU > 0.5 to the sacrum box or on its far side has none
- **truth**: carmlspine_eval.py's match (centre inside the truth body box, IoU >= 0.3, one to one); bodies whose two CBCT labellers disagree carry no level and are not scored, except the three VERIDAH-L6 patients, scored separately under `truth_source = variant_alphabet:L6`
- **intervals**: 2000-resample percentile bootstrap clustered by case, seed 0
- **tau**: 5th percentile of margin_next over the other four folds' anchored, fully correct frames of the same variant and field; at least 20 such frames or no margin threshold

Variants: **det** = keypoint-detector boxes; LODO sacrum, conf >= 0.25; std alphabets; **det74** = keypoint-detector boxes; LODO sacrum, conf >= 0.74 (cross-device operating point); std alphabets; **oracle** = truth body boxes; truth sacrum; std alphabets; **det_ns** = det, a body the classifier names 'sacrum' takes no ordinal; **oracle_ns** = oracle, a body the classifier names 'sacrum' takes no ordinal; **det_ext** = det, ext alphabets (four-lumbar pair added); **oracle_ext** = oracle, ext alphabets (four-lumbar pair added).

Per-frame coupler outputs (every ordinal, candidate score and name): `/rs/rs_grp_oschome/go2432/data/carmlspine/proto_post_v9init_prerepair/cv_fold<K>/<det|oracle>/k<full|5>/<couple|couple_c74|couple_ns|couple_ext>/couple_all.json` and one `<stem>.couple.json` per frame; prototype JSONs with the 27-vectors beside them. Shipped CV outputs the classifier numbers are checked against: `/rs/rs_grp_oschome/go2432/data/carmlspine/proto_v9init_prerepair/cv_fold<K>/<arm>_score_k<k>.json`.

## The classifier did not move

`--dump-posterior` and `--sacrum-detector` add fields; they must change no name. Exact-level accuracy of the re-run against the shipped CV output, per fold:

| cell | shipped (scored, exact) | re-run (scored, exact) | identical |
|---|---|---|---|
| cv_fold0/det/kfull | 291, 0.9278 | 291, 0.9278 | yes |
| cv_fold0/det/k5 | 267, 0.9326 | 267, 0.9326 | yes |
| cv_fold0/oracle/kfull | 312, 0.9038 | 312, 0.9038 | yes |
| cv_fold0/oracle/k5 | 294, 0.9218 | 294, 0.9218 | yes |
| cv_fold1/det/kfull | 203, 0.9901 | 203, 0.9901 | yes |
| cv_fold1/det/k5 | 228, 0.9474 | 228, 0.9474 | yes |
| cv_fold1/oracle/kfull | 216, 0.9676 | 216, 0.9676 | yes |
| cv_fold1/oracle/k5 | 250, 0.984 | 250, 0.984 | yes |
| cv_fold2/det/kfull | 225, 0.9644 | 225, 0.9644 | yes |
| cv_fold2/det/k5 | 273, 0.9304 | 273, 0.9304 | yes |
| cv_fold2/oracle/kfull | 256, 0.957 | 256, 0.957 | yes |
| cv_fold2/oracle/k5 | 309, 0.9256 | 309, 0.9256 | yes |
| cv_fold3/det/kfull | 306, 0.9869 | 306, 0.9869 | yes |
| cv_fold3/det/k5 | 326, 0.9233 | 326, 0.9233 | yes |
| cv_fold3/oracle/kfull | 333, 0.9279 | 333, 0.9279 | yes |
| cv_fold3/oracle/k5 | 363, 0.9174 | 363, 0.9174 | yes |
| cv_fold4/det/kfull | 223, 0.9821 | 223, 0.9821 | yes |
| cv_fold4/det/k5 | 256, 0.9492 | 256, 0.9492 | yes |
| cv_fold4/oracle/kfull | 232, 0.9871 | 232, 0.9871 | yes |
| cv_fold4/oracle/k5 | 270, 0.9333 | 270, 0.9333 | yes |

## The thresholds (chosen on the other four folds, applied to the fifth)

| variant / field / fold | tau on margin_next | frames it was chosen on |
|---|---|---|
| det/kfull/fold0 | 1.588 | 196 |
| det/kfull/fold1 | 1.5792 | 211 |
| det/kfull/fold2 | 1.8408 | 202 |
| det/kfull/fold3 | 2.079 | 188 |
| det/kfull/fold4 | 2.0436 | 207 |
| det/k5/fold0 | 1.2444 | 100 |
| det/k5/fold1 | 1.2197 | 105 |
| det/k5/fold2 | 1.2291 | 108 |
| det/k5/fold3 | 1.2457 | 101 |
| det/k5/fold4 | 1.2486 | 102 |
| det74/kfull/fold0 | 1.5874 | 177 |
| det74/kfull/fold1 | 1.5687 | 189 |
| det74/kfull/fold2 | 1.583 | 179 |
| det74/kfull/fold3 | 2.0769 | 167 |
| det74/kfull/fold4 | 2.0708 | 184 |
| det74/k5/fold0 | none (too few frames) | 6 |
| det74/k5/fold1 | none (too few frames) | 6 |
| det74/k5/fold2 | none (too few frames) | 5 |
| det74/k5/fold3 | none (too few frames) | 2 |
| det74/k5/fold4 | none (too few frames) | 5 |
| oracle/kfull/fold0 | 0.3328 | 194 |
| oracle/kfull/fold1 | 0.3527 | 209 |
| oracle/kfull/fold2 | 0.354 | 203 |
| oracle/kfull/fold3 | 0.3042 | 184 |
| oracle/kfull/fold4 | 0.3534 | 206 |
| oracle/k5/fold0 | 0.2296 | 38 |
| oracle/k5/fold1 | 0.0199 | 38 |
| oracle/k5/fold2 | 0.019 | 33 |
| oracle/k5/fold3 | 0.0197 | 37 |
| oracle/k5/fold4 | 0.2144 | 38 |
| det_ns/kfull/fold0 | 1.961 | 195 |
| det_ns/kfull/fold1 | 1.9241 | 211 |
| det_ns/kfull/fold2 | 2.0727 | 202 |
| det_ns/kfull/fold3 | 2.1471 | 188 |
| det_ns/kfull/fold4 | 2.1472 | 208 |
| det_ns/k5/fold0 | 1.3249 | 98 |
| det_ns/k5/fold1 | 1.3333 | 102 |
| det_ns/k5/fold2 | 1.5145 | 105 |
| det_ns/k5/fold3 | 1.3262 | 99 |
| det_ns/k5/fold4 | 1.4265 | 100 |
| oracle_ns/kfull/fold0 | 0.3271 | 192 |
| oracle_ns/kfull/fold1 | 0.3527 | 207 |
| oracle_ns/kfull/fold2 | 0.3528 | 201 |
| oracle_ns/kfull/fold3 | 0.3042 | 184 |
| oracle_ns/kfull/fold4 | 0.3532 | 204 |
| oracle_ns/k5/fold0 | 0.2807 | 36 |
| oracle_ns/k5/fold1 | 0.0196 | 36 |
| oracle_ns/k5/fold2 | 0.0186 | 31 |
| oracle_ns/k5/fold3 | 0.0196 | 36 |
| oracle_ns/k5/fold4 | 0.203 | 37 |
| det_ext/kfull/fold0 | 1.3943 | 198 |
| det_ext/kfull/fold1 | 1.2499 | 213 |
| det_ext/kfull/fold2 | 1.1574 | 204 |
| det_ext/kfull/fold3 | 1.3658 | 191 |
| det_ext/kfull/fold4 | 1.2891 | 210 |
| det_ext/k5/fold0 | 1.1283 | 104 |
| det_ext/k5/fold1 | 0.979 | 111 |
| det_ext/k5/fold2 | 1.2342 | 112 |
| det_ext/k5/fold3 | 1.2198 | 107 |
| det_ext/k5/fold4 | 1.1392 | 106 |
| oracle_ext/kfull/fold0 | 0.3214 | 190 |
| oracle_ext/kfull/fold1 | 0.3526 | 204 |
| oracle_ext/kfull/fold2 | 0.3528 | 198 |
| oracle_ext/kfull/fold3 | 0.2946 | 180 |
| oracle_ext/kfull/fold4 | 0.3528 | 200 |
| oracle_ext/k5/fold0 | 0.2233 | 37 |
| oracle_ext/k5/fold1 | 0.0197 | 37 |
| oracle_ext/k5/fold2 | 0.0188 | 32 |
| oracle_ext/k5/fold3 | 0.0197 | 37 |
| oracle_ext/k5/fold4 | 0.203 | 37 |

## C-ArmLSpine, five test folds pooled (truth = the two CBCT labellers agree)

k = full is the whole frame; k = 5 a crop holding five truth vertebrae (the sacrum is in the crop only when its centre falls inside). Bodies are scored where a call matches a truth body with an agreed level; a det frame with no detected sacrum is `no anchor` (names unchanged, flagged).

| cell | quantity | value [95 % CI, case bootstrap] (k/n) |
|---|---|---|
| det/kfull | frames | 290 (145 cases); anchored 266; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1209/1248) |
| det/kfull | (ii) coupled names, all scored bodies | 96.4 % [94.3, 98.3] (1203/1248); paired difference -0.5 pp [-2.2, +1.4] |
| det/kfull | (iii) coupled names, anchored frames only | 97.1 % [95.3, 98.8] (1119/1152); classifier on the same bodies 97.7 % [95.8, 99.2] (1125/1152); paired difference -0.5 pp [-2.5, +1.5] |
| det/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 96.1 % [93.5, 98.3] (1104/1149); coupled on the same bodies 97.1 % [95.3, 98.8] (1116/1149); classifier 97.7 % [95.8, 99.2] (1122/1149); coupled minus count +1.0 pp [-0.1, +2.9] |
| det/kfull | classifier on un-anchored frames | 87.5 % [73.3, 100.0] (84/96) |
| det/kfull | frame-exact (every scored body right), anchored frames | classifier 97.0 % [94.7, 98.9] (254/262); coupled 95.8 % [93.4, 98.1] (251/262) |
| det/kfull | disagreement | bodies 5.0 % [2.8, 7.6] (61/1214); frames with any 7.1 % [3.8, 10.8] (19/266) |
| det/kfull | accuracy when the two agree | coupled = classifier 99.5 % [98.6, 100.0] (1100/1106) |
| det/kfull | accuracy when they disagree | coupled 37.2 % [9.8, 65.3] (16/43); classifier 51.2 % [22.7, 79.6] (22/43); neither 5 of 43 |
| det/kfull | the count vs the classifier (counted bodies with truth, n = 1149) | corrects a classifier error 16 of 27; introduces an error 22 of 1122 classifier-correct bodies; both wrong 11 |
| det/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 19.3 % [14.1, 24.8] (56/290) of all frames, 12.0 % [7.9, 16.7] (32/266) of anchored; reasons {'no_anchor': 21, 'disagreement': 19, 'no_vertebra': 3, 'low_margin': 13} |
| det/kfull | stop signal on anchored frames with truth | fires on 90.9 % [72.7, 100.0] (10/11) of frames with a coupled error; on 7.6 % [4.0, 11.6] (19/251) of fully correct frames; coupled accuracy unflagged 99.9 % [99.7, 100.0] (1032/1033) vs flagged 73.1 % [57.3, 86.5] (87/119) |
| det/kfull | variant calls (anchored frames) | {'ordinary': 261, 'L6': 5}; on the non-ordinary calls: coupled 66.7 % [20.0, 100.0] (14/21), classifier 81.0 % [29.4, 100.0] (17/21), count 5.0 % [0.0, 18.8] (1/20); 5 of 5 flagged; cases ['case139', 'case19', 'case44', 'case9'] |
| det/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 5 / 0 |
| det/k5 | frames | 320 (135 cases); anchored 157; truth sacrum in frame 52; anchored without a truth sacrum 125; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det/k5 | (i) classifier alone, all scored bodies | 93.6 % [89.7, 97.0] (1263/1350) |
| det/k5 | (ii) coupled names, all scored bodies | 90.4 % [86.2, 93.8] (1220/1350); paired difference -3.2 pp [-5.2, -1.2] |
| det/k5 | (iii) coupled names, anchored frames only | 90.5 % [86.7, 93.9] (630/696); classifier on the same bodies 96.7 % [93.4, 99.3] (673/696); paired difference -6.2 pp [-10.0, -2.1] |
| det/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.5 % [83.9, 92.6] (587/663); coupled on the same bodies 90.3 % [86.3, 93.8] (599/663); classifier 96.8 % [93.7, 99.4] (642/663); coupled minus count +1.8 pp [+0.1, +4.2] |
| det/k5 | classifier on un-anchored frames | 90.2 % [83.7, 95.8] (590/654) |
| det/k5 | frame-exact (every scored body right), anchored frames | classifier 96.2 % [92.3, 99.3] (151/157); coupled 82.2 % [75.8, 88.3] (129/157) |
| det/k5 | disagreement | bodies 12.4 % [8.3, 17.1] (86/692); frames with any 20.4 % [14.0, 27.2] (32/157) |
| det/k5 | accuracy when the two agree | coupled = classifier 99.3 % [97.9, 100.0] (586/590) |
| det/k5 | accuracy when they disagree | coupled 17.8 % [0.0, 36.1] (13/73); classifier 76.7 % [57.6, 94.2] (56/73); neither 4 of 73 |
| det/k5 | the count vs the classifier (counted bodies with truth, n = 663) | corrects a classifier error 13 of 21; introduces an error 56 of 642 classifier-correct bodies; both wrong 8 |
| det/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 62.2 % [55.6, 68.2] (199/320) of all frames, 22.9 % [16.0, 30.3] (36/157) of anchored; reasons {'no_anchor': 160, 'disagreement': 32, 'low_margin': 4, 'no_vertebra': 3} |
| det/k5 | stop signal on anchored frames with truth | fires on 96.4 % [88.5, 100.0] (27/28) of frames with a coupled error; on 7.0 % [2.4, 12.2] (9/129) of fully correct frames; coupled accuracy unflagged 99.3 % [97.7, 100.0] (549/553) vs flagged 56.6 % [45.1, 66.9] (81/143) |
| det/k5 | variant calls (anchored frames) | {'ordinary': 148, 'L6': 9}; on the non-ordinary calls: coupled 60.0 % [42.4, 74.4] (21/35), classifier 100.0 % [100.0, 100.0] (35/35), count 3.7 % [0.0, 12.5] (1/27); 9 of 9 flagged; cases ['case38', 'case4', 'case5', 'case60', 'case65', 'case69', 'case82', 'case88'] |
| det/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 6 / 0 |
| det74/kfull | frames | 290 (145 cases); anchored 233; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 53; anchor rejected by the confidence floor 34 |
| det74/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1209/1248) |
| det74/kfull | (ii) coupled names, all scored bodies | 97.3 % [95.4, 99.0] (1214/1248); paired difference +0.4 pp [-1.1, +1.9] |
| det74/kfull | (iii) coupled names, anchored frames only | 98.2 % [96.5, 99.5] (991/1009); classifier on the same bodies 97.7 % [95.9, 99.2] (986/1009); paired difference +0.5 pp [-1.5, +2.4] |
| det74/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.0 % [94.2, 99.2] (979/1009); coupled on the same bodies 98.2 % [96.5, 99.5] (991/1009); classifier 97.7 % [95.9, 99.2] (986/1009); coupled minus count +1.2 pp [+0.0, +3.2] |
| det74/kfull | classifier on un-anchored frames | 93.3 % [86.3, 98.7] (223/239) |
| det74/kfull | frame-exact (every scored body right), anchored frames | classifier 97.0 % [94.7, 98.7] (223/230); coupled 97.4 % [95.2, 99.2] (224/230) |
| det74/kfull | disagreement | bodies 3.9 % [1.8, 6.5] (42/1066); frames with any 5.6 % [2.6, 9.2] (13/233) |
| det74/kfull | accuracy when the two agree | coupled = classifier 99.5 % [98.5, 100.0] (975/980) |
| det74/kfull | accuracy when they disagree | coupled 55.2 % [15.4, 87.5] (16/29); classifier 37.9 % [9.7, 74.2] (11/29); neither 2 of 29 |
| det74/kfull | the count vs the classifier (counted bodies with truth, n = 1009) | corrects a classifier error 16 of 23; introduces an error 11 of 986 classifier-correct bodies; both wrong 7 |
| det74/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 27.6 % [21.7, 33.8] (80/290) of all frames, 9.9 % [5.7, 14.5] (23/233) of anchored; reasons {'no_anchor': 54, 'disagreement': 13, 'no_vertebra': 3, 'low_margin': 10} |
| det74/kfull | stop signal on anchored frames with truth | fires on 83.3 % [50.0, 100.0] (5/6) of frames with a coupled error; on 7.1 % [3.5, 11.5] (16/224) of fully correct frames; coupled accuracy unflagged 99.9 % [99.7, 100.0] (921/922) vs flagged 80.5 % [61.3, 95.3] (70/87) |
| det74/kfull | variant calls (anchored frames) | {'ordinary': 230, 'L6': 3}; on the non-ordinary calls: coupled 100.0 % [100.0, 100.0] (12/12), classifier 100.0 % [100.0, 100.0] (12/12), count 0.0 % [0.0, 0.0] (0/12); 3 of 3 flagged; cases ['case139', 'case44'] |
| det74/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 5 / 0 |
| det74/k5 | frames | 320 (135 cases); anchored 6; truth sacrum in frame 52; anchored without a truth sacrum 3; truth sacrum but no anchor 49; anchor rejected by the confidence floor 152 |
| det74/k5 | (i) classifier alone, all scored bodies | 93.6 % [89.7, 97.0] (1263/1350) |
| det74/k5 | (ii) coupled names, all scored bodies | 93.9 % [90.0, 97.3] (1268/1350); paired difference +0.4 pp [+0.0, +1.2] |
| det74/k5 | (iii) coupled names, anchored frames only | 100.0 % [100.0, 100.0] (29/29); classifier on the same bodies 82.8 % [62.5, 100.0] (24/29); paired difference +17.2 pp [+0.0, +37.5] |
| det74/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 100.0 % [100.0, 100.0] (29/29); coupled on the same bodies 100.0 % [100.0, 100.0] (29/29); classifier 82.8 % [62.5, 100.0] (24/29); coupled minus count +0.0 pp [+0.0, +0.0] |
| det74/k5 | classifier on un-anchored frames | 93.8 % [89.7, 97.3] (1239/1321) |
| det74/k5 | frame-exact (every scored body right), anchored frames | classifier 83.3 % [62.5, 100.0] (5/6); coupled 100.0 % [100.0, 100.0] (6/6) |
| det74/k5 | disagreement | bodies 17.2 % [0.0, 37.5] (5/29); frames with any 16.7 % [0.0, 37.5] (1/6) |
| det74/k5 | accuracy when the two agree | coupled = classifier 100.0 % [100.0, 100.0] (24/24) |
| det74/k5 | accuracy when they disagree | coupled 100.0 % (5/5); classifier 0.0 % (0/5); neither 0 of 5 |
| det74/k5 | the count vs the classifier (counted bodies with truth, n = 29) | corrects a classifier error 5 of 5; introduces an error 0 of 24 classifier-correct bodies; both wrong 0 |
| det74/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 98.4 % [97.0, 99.7] (315/320) of all frames, 16.7 % [0.0, 37.5] (1/6) of anchored; reasons {'no_anchor': 311, 'no_vertebra': 3, 'disagreement': 1} |
| det74/k5 | stop signal on anchored frames with truth | fires on n/a of frames with a coupled error; on 16.7 % [0.0, 37.5] (1/6) of fully correct frames; coupled accuracy unflagged 100.0 % [100.0, 100.0] (24/24) vs flagged 100.0 % (5/5) |
| det74/k5 | variant calls (anchored frames) | {'ordinary': 6}; on the non-ordinary calls: coupled n/a, classifier n/a, count n/a; 0 of 0 flagged; cases [] |
| det74/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 1 / 0 |
| oracle/kfull | frames | 290 (145 cases); anchored 286; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle/kfull | (i) classifier alone, all scored bodies | 94.4 % [91.7, 96.6] (1274/1349) |
| oracle/kfull | (ii) coupled names, all scored bodies | 96.7 % [95.2, 97.9] (1304/1349); paired difference +2.2 pp [+0.1, +4.8] |
| oracle/kfull | (iii) coupled names, anchored frames only | 97.0 % [95.7, 98.2] (1289/1329); classifier on the same bodies 94.7 % [92.3, 96.9] (1259/1329); paired difference +2.3 pp [+0.0, +4.7] |
| oracle/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.7 % [96.7, 98.5] (1298/1329); coupled on the same bodies 97.0 % [95.7, 98.2] (1289/1329); classifier 94.7 % [92.3, 96.9] (1259/1329); coupled minus count -0.7 pp [-1.7, +0.0] |
| oracle/kfull | classifier on un-anchored frames | 75.0 % [50.0, 100.0] (15/20) |
| oracle/kfull | frame-exact (every scored body right), anchored frames | classifier 87.6 % [83.0, 91.8] (247/282); coupled 88.3 % [83.7, 92.2] (249/282) |
| oracle/kfull | disagreement | bodies 5.8 % [3.5, 8.3] (85/1455); frames with any 9.8 % [6.6, 13.3] (28/286) |
| oracle/kfull | accuracy when the two agree | coupled = classifier 98.0 % [97.0, 98.9] (1244/1269) |
| oracle/kfull | accuracy when they disagree | coupled 75.0 % [50.0, 90.2] (45/60); classifier 25.0 % [9.8, 50.0] (15/60); neither 0 of 60 |
| oracle/kfull | the count vs the classifier (counted bodies with truth, n = 1329) | corrects a classifier error 45 of 70; introduces an error 15 of 1259 classifier-correct bodies; both wrong 25 |
| oracle/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 14.1 % [10.0, 18.3] (41/290) of all frames, 12.9 % [9.1, 17.1] (37/286) of anchored; reasons {'no_anchor': 4, 'disagreement': 28, 'low_margin': 9} |
| oracle/kfull | stop signal on anchored frames with truth | fires on 36.4 % [20.0, 54.5] (12/33) of frames with a coupled error; on 9.6 % [5.9, 13.8] (24/249) of fully correct frames; coupled accuracy unflagged 98.2 % [97.3, 99.0] (1138/1159) vs flagged 88.8 % [80.2, 95.5] (151/170) |
| oracle/kfull | variant calls (anchored frames) | {'ordinary': 282, 'L6': 2, 'T13': 2}; on the non-ordinary calls: coupled 52.6 % [0.0, 100.0] (10/19), classifier 79.0 % [29.4, 100.0] (15/19), count 100.0 % [100.0, 100.0] (19/19); 4 of 4 flagged; cases ['case103', 'case19', 'case54', 'case9'] |
| oracle/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 3 / 0 |
| oracle/k5 | frames | 320 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle/k5 | (i) classifier alone, all scored bodies | 93.4 % [90.5, 95.9] (1388/1486) |
| oracle/k5 | (ii) coupled names, all scored bodies | 94.3 % [91.7, 96.5] (1401/1486); paired difference +0.9 pp [-0.2, +2.2] |
| oracle/k5 | (iii) coupled names, anchored frames only | 95.3 % [88.0, 99.6] (245/257); classifier on the same bodies 90.3 % [80.7, 98.0] (232/257); paired difference +5.1 pp [-1.2, +12.7] |
| oracle/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 98.4 % [96.3, 100.0] (253/257); coupled on the same bodies 95.3 % [88.0, 99.6] (245/257); classifier 90.3 % [80.7, 98.0] (232/257); coupled minus count -3.1 pp [-9.8, +0.0] |
| oracle/k5 | classifier on un-anchored frames | 94.1 % [91.4, 96.4] (1156/1229) |
| oracle/k5 | frame-exact (every scored body right), anchored frames | classifier 86.5 % [75.0, 96.1] (45/52); coupled 88.5 % [76.0, 98.0] (46/52) |
| oracle/k5 | disagreement | bodies 9.2 % [2.9, 16.5] (26/283); frames with any 17.3 % [6.0, 30.2] (9/52) |
| oracle/k5 | accuracy when the two agree | coupled = classifier 96.2 % [88.6, 100.0] (229/238) |
| oracle/k5 | accuracy when they disagree | coupled 84.2 % [46.2, 100.0] (16/19); classifier 15.8 % [0.0, 53.8] (3/19); neither 0 of 19 |
| oracle/k5 | the count vs the classifier (counted bodies with truth, n = 257) | corrects a classifier error 16 of 25; introduces an error 3 of 232 classifier-correct bodies; both wrong 9 |
| oracle/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 87.5 % [83.1, 91.5] (280/320) of all frames, 23.1 % [9.6, 37.0] (12/52) of anchored; reasons {'no_anchor': 268, 'disagreement': 9, 'low_margin': 3} |
| oracle/k5 | stop signal on anchored frames with truth | fires on 83.3 % [40.0, 100.0] (5/6) of frames with a coupled error; on 15.2 % [4.8, 27.3] (7/46) of fully correct frames; coupled accuracy unflagged 99.5 % [98.4, 100.0] (198/199) vs flagged 81.0 % [54.7, 100.0] (47/58) |
| oracle/k5 | variant calls (anchored frames) | {'ordinary': 50, 'L6': 2}; on the non-ordinary calls: coupled 0.0 % (0/8), classifier 0.0 % (0/8), count 100.0 % (8/8); 2 of 2 flagged; cases ['case54'] |
| oracle/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 4 / 0 |

### Sensitivity variants (same folds; only the rows that change)

| cell | quantity | value |
|---|---|---|
| det_ns/kfull | frames | 290 (145 cases); anchored 266; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det_ns/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1209/1248) |
| det_ns/kfull | (ii) coupled names, all scored bodies | 96.4 % [94.3, 98.2] (1203/1248); paired difference -0.5 pp [-2.1, +1.1] |
| det_ns/kfull | (iii) coupled names, anchored frames only | 97.1 % [95.3, 98.8] (1119/1152); classifier on the same bodies 97.7 % [95.8, 99.2] (1125/1152); paired difference -0.5 pp [-2.2, +1.3] |
| det_ns/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.1 % [95.4, 98.8] (1116/1149); coupled on the same bodies 97.1 % [95.3, 98.8] (1116/1149); classifier 97.7 % [95.8, 99.2] (1122/1149); coupled minus count +0.0 pp [-0.3, +0.3] |
| det_ns/kfull | the count vs the classifier (counted bodies with truth, n = 1149) | corrects a classifier error 12 of 27; introduces an error 18 of 1122 classifier-correct bodies; both wrong 15 |
| det_ns/kfull | variant calls (anchored frames) | {'ordinary': 264, 'L6': 2}; on the non-ordinary calls: coupled 22.2 % [0.0, 40.0] (2/9), classifier 55.6 % [0.0, 100.0] (5/9), count 12.5 % [0.0, 25.0] (1/8); 2 of 2 flagged; cases ['case19', 'case9'] |
| det_ns/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 6 |
| det_ns/k5 | frames | 320 (135 cases); anchored 157; truth sacrum in frame 52; anchored without a truth sacrum 125; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det_ns/k5 | (i) classifier alone, all scored bodies | 93.6 % [89.7, 97.0] (1263/1350) |
| det_ns/k5 | (ii) coupled names, all scored bodies | 89.3 % [85.2, 93.1] (1206/1350); paired difference -4.2 pp [-5.9, -2.7] |
| det_ns/k5 | (iii) coupled names, anchored frames only | 88.5 % [84.2, 92.3] (616/696); classifier on the same bodies 96.7 % [93.4, 99.3] (673/696); paired difference -8.2 pp [-11.5, -5.2] |
| det_ns/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 87.9 % [83.4, 91.9] (582/662); coupled on the same bodies 88.4 % [83.9, 92.2] (585/662); classifier 97.0 % [94.1, 99.4] (642/662); coupled minus count +0.4 pp [-0.2, +1.1] |
| det_ns/k5 | the count vs the classifier (counted bodies with truth, n = 662) | corrects a classifier error 0 of 20; introduces an error 57 of 642 classifier-correct bodies; both wrong 20 |
| det_ns/k5 | variant calls (anchored frames) | {'ordinary': 151, 'L6': 6}; on the non-ordinary calls: coupled 43.5 % [28.6, 50.0] (10/23), classifier 100.0 % [100.0, 100.0] (23/23), count 5.9 % [0.0, 17.6] (1/17); 6 of 6 flagged; cases ['case38', 'case5', 'case65', 'case69', 'case82', 'case88'] |
| det_ns/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 12 |
| oracle_ns/kfull | frames | 290 (145 cases); anchored 286; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ns/kfull | (i) classifier alone, all scored bodies | 94.4 % [91.7, 96.6] (1274/1349) |
| oracle_ns/kfull | (ii) coupled names, all scored bodies | 96.0 % [94.1, 97.5] (1295/1349); paired difference +1.6 pp [-0.4, +3.9] |
| oracle_ns/kfull | (iii) coupled names, anchored frames only | 96.3 % [94.6, 97.8] (1280/1329); classifier on the same bodies 94.7 % [92.3, 96.9] (1259/1329); paired difference +1.6 pp [-0.4, +3.9] |
| oracle_ns/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 96.8 % [95.2, 98.0] (1285/1328); coupled on the same bodies 96.4 % [94.7, 97.8] (1280/1328); classifier 94.8 % [92.4, 97.0] (1259/1328); coupled minus count -0.4 pp [-1.1, +0.0] |
| oracle_ns/kfull | the count vs the classifier (counted bodies with truth, n = 1328) | corrects a classifier error 36 of 69; introduces an error 15 of 1259 classifier-correct bodies; both wrong 33 |
| oracle_ns/kfull | variant calls (anchored frames) | {'ordinary': 283, 'T13': 2, 'L6': 1}; on the non-ordinary calls: coupled 66.7 % [0.0, 100.0] (10/15), classifier 100.0 % [100.0, 100.0] (15/15), count 100.0 % [100.0, 100.0] (15/15); 3 of 3 flagged; cases ['case103', 'case19', 'case9'] |
| oracle_ns/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 3 |
| oracle_ns/k5 | frames | 320 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ns/k5 | (i) classifier alone, all scored bodies | 93.4 % [90.5, 95.9] (1388/1486) |
| oracle_ns/k5 | (ii) coupled names, all scored bodies | 93.7 % [91.1, 96.0] (1392/1486); paired difference +0.3 pp [-0.4, +1.2] |
| oracle_ns/k5 | (iii) coupled names, anchored frames only | 91.8 % [83.1, 98.4] (236/257); classifier on the same bodies 90.3 % [80.7, 98.0] (232/257); paired difference +1.6 pp [-2.3, +6.8] |
| oracle_ns/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 92.2 % [83.8, 98.4] (236/256); coupled on the same bodies 92.2 % [83.8, 98.4] (236/256); classifier 90.6 % [81.2, 98.1] (232/256); coupled minus count +0.0 pp [+0.0, +0.0] |
| oracle_ns/k5 | the count vs the classifier (counted bodies with truth, n = 256) | corrects a classifier error 7 of 24; introduces an error 3 of 232 classifier-correct bodies; both wrong 17 |
| oracle_ns/k5 | variant calls (anchored frames) | {'ordinary': 52}; on the non-ordinary calls: coupled n/a, classifier n/a, count n/a; 0 of 0 flagged; cases [] |
| oracle_ns/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 4 |
| det_ext/kfull | frames | 290 (145 cases); anchored 266; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det_ext/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1209/1248) |
| det_ext/kfull | (ii) coupled names, all scored bodies | 97.0 % [94.7, 98.9] (1210/1248); paired difference +0.1 pp [-1.1, +1.4] |
| det_ext/kfull | (iii) coupled names, anchored frames only | 97.7 % [96.0, 99.2] (1126/1152); classifier on the same bodies 97.7 % [95.8, 99.2] (1125/1152); paired difference +0.1 pp [-1.2, +1.6] |
| det_ext/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 96.1 % [93.5, 98.3] (1104/1149); coupled on the same bodies 97.7 % [96.0, 99.2] (1123/1149); classifier 97.7 % [95.8, 99.2] (1122/1149); coupled minus count +1.7 pp [-0.4, +3.8] |
| det_ext/kfull | the count vs the classifier (counted bodies with truth, n = 1149) | corrects a classifier error 10 of 27; introduces an error 9 of 1122 classifier-correct bodies; both wrong 17 |
| det_ext/kfull | variant calls (anchored frames) | {'ordinary': 251, 'L4': 11, 'L6': 4}; on the non-ordinary calls: coupled 64.6 % [37.0, 88.5] (31/48), classifier 70.8 % [40.9, 93.2] (34/48), count 20.0 % [0.0, 46.0] (9/45); 10 of 15 flagged; cases ['case129', 'case139', 'case146', 'case148', 'case17', 'case19', 'case34', 'case43', 'case44', 'case77', 'case8', 'case83', 'case84', 'case9'] |
| det_ext/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 5 / 0 |
| det_ext/k5 | frames | 320 (135 cases); anchored 157; truth sacrum in frame 52; anchored without a truth sacrum 125; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det_ext/k5 | (i) classifier alone, all scored bodies | 93.6 % [89.7, 97.0] (1263/1350) |
| det_ext/k5 | (ii) coupled names, all scored bodies | 91.7 % [87.7, 95.1] (1238/1350); paired difference -1.8 pp [-3.5, -0.2] |
| det_ext/k5 | (iii) coupled names, anchored frames only | 93.1 % [89.8, 96.0] (648/696); classifier on the same bodies 96.7 % [93.4, 99.3] (673/696); paired difference -3.6 pp [-6.9, -0.3] |
| det_ext/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.5 % [83.9, 92.6] (587/663); coupled on the same bodies 93.1 % [89.8, 96.0] (617/663); classifier 96.8 % [93.7, 99.4] (642/663); coupled minus count +4.5 pp [+1.9, +7.7] |
| det_ext/k5 | the count vs the classifier (counted bodies with truth, n = 663) | corrects a classifier error 13 of 21; introduces an error 38 of 642 classifier-correct bodies; both wrong 8 |
| det_ext/k5 | variant calls (anchored frames) | {'ordinary': 133, 'L6': 7, 'L4': 17}; on the non-ordinary calls: coupled 60.9 % [47.8, 73.8] (56/92), classifier 93.5 % [80.6, 100.0] (86/92), count 3.0 % [0.0, 7.6] (2/66); 16 of 24 flagged; cases ['case102', 'case103', 'case115', 'case133', 'case135', 'case139', 'case38', 'case4', 'case44', 'case5', 'case6', 'case60', 'case65', 'case67', 'case69', 'case73', 'case74', 'case77', 'case82', 'case88', 'case9'] |
| det_ext/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 6 / 0 |
| oracle_ext/kfull | frames | 290 (145 cases); anchored 286; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ext/kfull | (i) classifier alone, all scored bodies | 94.4 % [91.7, 96.6] (1274/1349) |
| oracle_ext/kfull | (ii) coupled names, all scored bodies | 94.6 % [92.1, 96.6] (1276/1349); paired difference +0.1 pp [-1.3, +1.6] |
| oracle_ext/kfull | (iii) coupled names, anchored frames only | 94.9 % [92.6, 97.0] (1261/1329); classifier on the same bodies 94.7 % [92.3, 96.9] (1259/1329); paired difference +0.1 pp [-1.4, +1.6] |
| oracle_ext/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.7 % [96.7, 98.5] (1298/1329); coupled on the same bodies 94.9 % [92.6, 97.0] (1261/1329); classifier 94.7 % [92.3, 96.9] (1259/1329); coupled minus count -2.8 pp [-5.0, -1.0] |
| oracle_ext/kfull | the count vs the classifier (counted bodies with truth, n = 1329) | corrects a classifier error 17 of 70; introduces an error 15 of 1259 classifier-correct bodies; both wrong 53 |
| oracle_ext/kfull | variant calls (anchored frames) | {'ordinary': 275, 'L4': 7, 'L6': 2, 'T13': 2}; on the non-ordinary calls: coupled 21.3 % [0.0, 52.1] (10/47), classifier 31.9 % [9.1, 65.2] (15/47), count 100.0 % [100.0, 100.0] (47/47); 8 of 11 flagged; cases ['case103', 'case104', 'case118', 'case146', 'case148', 'case19', 'case54', 'case79', 'case83', 'case9'] |
| oracle_ext/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 3 / 0 |
| oracle_ext/k5 | frames | 320 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ext/k5 | (i) classifier alone, all scored bodies | 93.4 % [90.5, 95.9] (1388/1486) |
| oracle_ext/k5 | (ii) coupled names, all scored bodies | 93.9 % [91.1, 96.4] (1395/1486); paired difference +0.5 pp [-0.3, +1.4] |
| oracle_ext/k5 | (iii) coupled names, anchored frames only | 93.0 % [84.9, 99.2] (239/257); classifier on the same bodies 90.3 % [80.7, 98.0] (232/257); paired difference +2.7 pp [-1.7, +8.8] |
| oracle_ext/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 98.4 % [96.3, 100.0] (253/257); coupled on the same bodies 93.0 % [84.9, 99.2] (239/257); classifier 90.3 % [80.7, 98.0] (232/257); coupled minus count -5.5 pp [-13.4, +0.0] |
| oracle_ext/k5 | the count vs the classifier (counted bodies with truth, n = 257) | corrects a classifier error 10 of 25; introduces an error 3 of 232 classifier-correct bodies; both wrong 15 |
| oracle_ext/k5 | variant calls (anchored frames) | {'ordinary': 49, 'L6': 2, 'L4': 1}; on the non-ordinary calls: coupled 0.0 % [0.0, 0.0] (0/14), classifier 0.0 % [0.0, 0.0] (0/14), count 100.0 % [100.0, 100.0] (14/14); 3 of 3 flagged; cases ['case118', 'case54'] |
| oracle_ext/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 4 / 0 |

### Same cells, with the three VERIDAH-L6 patients scored under their L6 truth

| cell | quantity | value |
|---|---|---|
| det/kfull | (i) classifier alone, all scored bodies | 95.4 % [92.5, 97.8] (1217/1276) |
| det/kfull | (ii) coupled names, all scored bodies | 94.7 % [91.6, 97.2] (1208/1276); paired difference -0.7 pp [-2.6, +1.2] |
| det/kfull | (iii) coupled names, anchored frames only | 95.6 % [93.0, 98.0] (1124/1176); classifier on the same bodies 96.3 % [94.0, 98.5] (1133/1176); paired difference -0.8 pp [-2.7, +1.3] |
| det/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 94.1 % [90.5, 97.3] (1104/1173); coupled on the same bodies 95.6 % [92.9, 98.0] (1121/1173); classifier 96.3 % [94.0, 98.5] (1130/1173); coupled minus count +1.5 pp [+0.0, +3.5] |
| det/kfull | the count vs the classifier (counted bodies with truth, n = 1173) | corrects a classifier error 17 of 43; introduces an error 26 of 1130 classifier-correct bodies; both wrong 26 |
| det/kfull | variant calls (anchored frames) | {'ordinary': 265, 'L6': 6}; on the non-ordinary calls: coupled 73.1 % [33.3, 100.0] (19/26), classifier 80.8 % [40.9, 100.0] (21/26), count 4.0 % [0.0, 14.3] (1/25); 6 of 6 flagged; cases ['case139', 'case19', 'case42', 'case44', 'case9'] |
| det/k5 | (i) classifier alone, all scored bodies | 92.6 % [88.6, 96.2] (1276/1378) |
| det/k5 | (ii) coupled names, all scored bodies | 89.2 % [85.1, 93.0] (1229/1378); paired difference -3.4 pp [-5.5, -1.3] |
| det/k5 | (iii) coupled names, anchored frames only | 88.7 % [83.9, 92.7] (635/716); classifier on the same bodies 95.2 % [91.3, 98.4] (682/716); paired difference -6.6 pp [-10.5, -2.7] |
| det/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 85.9 % [79.9, 90.8] (587/683); coupled on the same bodies 88.4 % [83.3, 92.5] (604/683); classifier 95.3 % [91.5, 98.3] (651/683); coupled minus count +2.5 pp [+0.4, +5.1] |
| det/k5 | the count vs the classifier (counted bodies with truth, n = 683) | corrects a classifier error 13 of 32; introduces an error 60 of 651 classifier-correct bodies; both wrong 19 |
| det/k5 | variant calls (anchored frames) | {'ordinary': 153, 'L6': 10}; on the non-ordinary calls: coupled 65.0 % [47.1, 80.4] (26/40), classifier 100.0 % [100.0, 100.0] (40/40), count 3.1 % [0.0, 10.3] (1/32); 9 of 10 flagged; cases ['case38', 'case4', 'case42', 'case5', 'case60', 'case65', 'case69', 'case82', 'case88'] |
| det74/kfull | (i) classifier alone, all scored bodies | 95.4 % [92.5, 97.8] (1217/1276) |
| det74/kfull | (ii) coupled names, all scored bodies | 95.5 % [92.5, 97.9] (1219/1276); paired difference +0.2 pp [-1.6, +1.8] |
| det74/kfull | (iii) coupled names, anchored frames only | 96.8 % [93.8, 98.9] (996/1029); classifier on the same bodies 96.6 % [94.2, 98.7] (994/1029); paired difference +0.2 pp [-2.0, +2.3] |
| det74/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 95.1 % [91.1, 98.4] (979/1029); coupled on the same bodies 96.8 % [93.8, 98.9] (996/1029); classifier 96.6 % [94.2, 98.7] (994/1029); coupled minus count +1.7 pp [+0.0, +3.9] |
| det74/kfull | the count vs the classifier (counted bodies with truth, n = 1029) | corrects a classifier error 17 of 35; introduces an error 15 of 994 classifier-correct bodies; both wrong 18 |
| det74/kfull | variant calls (anchored frames) | {'ordinary': 233, 'L6': 4}; on the non-ordinary calls: coupled 100.0 % [100.0, 100.0] (17/17), classifier 94.1 % [80.0, 100.0] (16/17), count 0.0 % [0.0, 0.0] (0/17); 4 of 4 flagged; cases ['case139', 'case42', 'case44'] |
| det74/k5 | (i) classifier alone, all scored bodies | 92.6 % [88.6, 96.2] (1276/1378) |
| det74/k5 | (ii) coupled names, all scored bodies | 93.0 % [89.1, 96.5] (1281/1378); paired difference +0.4 pp [+0.0, +1.1] |
| det74/k5 | (iii) coupled names, anchored frames only | 100.0 % [100.0, 100.0] (29/29); classifier on the same bodies 82.8 % [62.5, 100.0] (24/29); paired difference +17.2 pp [+0.0, +37.5] |
| det74/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 100.0 % [100.0, 100.0] (29/29); coupled on the same bodies 100.0 % [100.0, 100.0] (29/29); classifier 82.8 % [62.5, 100.0] (24/29); coupled minus count +0.0 pp [+0.0, +0.0] |
| det74/k5 | the count vs the classifier (counted bodies with truth, n = 29) | corrects a classifier error 5 of 5; introduces an error 0 of 24 classifier-correct bodies; both wrong 0 |
| det74/k5 | variant calls (anchored frames) | {'ordinary': 6}; on the non-ordinary calls: coupled n/a, classifier n/a, count n/a; 0 of 0 flagged; cases [] |
| oracle/kfull | (i) classifier alone, all scored bodies | 93.2 % [90.1, 95.7] (1285/1379) |
| oracle/kfull | (ii) coupled names, all scored bodies | 95.2 % [92.8, 97.2] (1313/1379); paired difference +2.0 pp [-0.1, +4.5] |
| oracle/kfull | (iii) coupled names, anchored frames only | 95.5 % [93.1, 97.4] (1298/1359); classifier on the same bodies 93.5 % [90.4, 96.2] (1270/1359); paired difference +2.1 pp [-0.1, +4.5] |
| oracle/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 95.5 % [92.6, 97.8] (1298/1359); coupled on the same bodies 95.5 % [93.1, 97.4] (1298/1359); classifier 93.5 % [90.4, 96.2] (1270/1359); coupled minus count +0.0 pp [-1.3, +1.3] |
| oracle/kfull | the count vs the classifier (counted bodies with truth, n = 1359) | corrects a classifier error 47 of 89; introduces an error 19 of 1270 classifier-correct bodies; both wrong 42 |
| oracle/kfull | variant calls (anchored frames) | {'ordinary': 286, 'L6': 4, 'T13': 2}; on the non-ordinary calls: coupled 65.5 % [31.0, 96.7] (19/29), classifier 75.9 % [48.1, 96.7] (22/29), count 65.5 % [31.0, 100.0] (19/29); 6 of 6 flagged; cases ['case103', 'case136', 'case19', 'case42', 'case54', 'case9'] |
| oracle/k5 | (i) classifier alone, all scored bodies | 92.3 % [89.1, 95.1] (1399/1516) |
| oracle/k5 | (ii) coupled names, all scored bodies | 93.0 % [90.0, 95.5] (1410/1516); paired difference +0.7 pp [-0.4, +2.1] |
| oracle/k5 | (iii) coupled names, anchored frames only | 88.5 % [77.6, 96.7] (254/287); classifier on the same bodies 84.7 % [74.0, 93.7] (243/287); paired difference +3.8 pp [-2.1, +10.8] |
| oracle/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.1 % [76.0, 98.6] (253/287); coupled on the same bodies 88.5 % [77.6, 96.7] (254/287); classifier 84.7 % [74.0, 93.7] (243/287); coupled minus count +0.4 pp [-7.1, +6.9] |
| oracle/k5 | the count vs the classifier (counted bodies with truth, n = 287) | corrects a classifier error 18 of 44; introduces an error 7 of 243 classifier-correct bodies; both wrong 26 |
| oracle/k5 | variant calls (anchored frames) | {'ordinary': 54, 'L6': 4}; on the non-ordinary calls: coupled 50.0 % [0.0, 100.0] (9/18), classifier 38.9 % [0.0, 80.0] (7/18), count 44.4 % [0.0, 100.0] (8/18); 4 of 4 flagged; cases ['case136', 'case42', 'case54'] |

### Per truth level (all scored bodies; classifier / coupled exact, %)

- **det/kfull**: L1 n=157 97.5/98.1; L2 n=256 96.1/94.9; L3 n=282 96.5/95.4; L4 n=283 96.5/96.1; L5 n=269 98.1/98.1; T12 n=1 100.0/100.0
- **det/k5**: L1 n=193 91.2/91.2; L2 n=288 92.4/88.2; L3 n=313 93.0/86.3; L4 n=311 93.9/92.0; L5 n=244 97.5/95.9; T12 n=1 0.0/0.0
- **det74/kfull**: L1 n=157 97.5/98.1; L2 n=256 96.1/96.5; L3 n=282 96.5/96.8; L4 n=283 96.5/96.8; L5 n=269 98.1/98.5; T12 n=1 100.0/100.0
- **det74/k5**: L1 n=193 91.2/91.7; L2 n=288 92.4/92.7; L3 n=313 93.0/93.3; L4 n=311 93.9/94.2; L5 n=244 97.5/98.0; T12 n=1 0.0/0.0
- **oracle/kfull**: L1 n=209 93.8/93.8; L2 n=284 89.8/91.9; L3 n=286 96.2/99.0; L4 n=286 95.8/98.6; L5 n=278 96.8/99.3; T12 n=6 83.3/100.0
- **oracle/k5**: L1 n=270 90.0/90.4; L2 n=319 89.7/90.6; L3 n=319 95.3/96.2; L4 n=316 94.9/95.9; L5 n=250 98.4/99.2; T12 n=12 75.0/83.3

## The three real L6 patients, frame by frame

**What the truth is here, plainly.** case42, case121 and case136 are the C-ArmLSpine CBCTs SPINEPS/VERIDAH read as L2-L6 and TotalSegmentator read as L1-L5 (TotalSegmentator has no L6 class). Both saw the same lumbar-only CBCT; neither saw the thoracolumbar junction or the ribs, so neither could count. The L6 rests on VERIDAH's morphology read of the CT, not on a count from a junction. Below, `VERIDAH truth` is that naming read from the truth sacrum by the L6 alphabet and `TS read` the same bodies under TotalSegmentator's naming. A coupled call of L6 agrees with VERIDAH; ordinary agrees with TotalSegmentator; the frames alone cannot say which is right. Each frame shows FIVE bodies above the sacrum (the top body is boxed twice in the truth, once per labeller; the duplicate is dropped). `count` is the ordinary alphabet at the ordinal, which cannot name an L6.

| case view | field | variant | anchor | classifier names (top to bottom) | ordinals | count | candidate scores | call (margin, margin_next, tau) | coupled | VERIDAH truth | TS read | coupled = VERIDAH | classifier = VERIDAH | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| case42 AP | k5 | det | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 1.2291) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | det | sacrum_detector 0.734 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.6288, 'L6': -2.2641} | ordinary (0.0, 1.6353, 1.2291) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case42 AP | k5 | det74 | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | det74 | none (rejected 0.734) | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case42 AP | k5 | oracle | none | T12 L1 L2 L3 L4 | - - - - - | - - - - - | {} | no anchor (None, None, 0.019) | T12 L1 L2 L3 L4 | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -1.9573, 'T13': -2.2119, 'L6': -2.2529} | ordinary (0.0, 0.2546, 0.019) | L1 T12 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case42 AP | kfull | det | sacrum_detector 0.877 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.8078, 'L6': -2.7948} | ordinary (0.0, 1.987, 1.8408) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case42 AP | kfull | det74 | sacrum_detector 0.877 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.8078, 'L6': -2.7948} | ordinary (0.0, 1.987, 1.583) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case42 AP | kfull | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -1.8377, 'T13': -1.9776, 'L6': -2.0514} | ordinary (0.0, 0.1399, 0.354) | L1 T12 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case42 LAT | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.2291) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case42 LAT | k5 | det | sacrum_detector 0.32 | L2 L3 L4 L5 L6 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -3.4001, 'L6': -0.568} | L6 (2.8321, 2.8321, 1.2291) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | yes | quiet |
| case42 LAT | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case42 LAT | k5 | det74 | none (rejected 0.32) | L2 L3 L4 L5 L6 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | yes | no_anchor |
| case42 LAT | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.019) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.3915, 'T13': -4.195, 'L6': -1.6252} | L6 (1.7663, 1.7663, 0.019) | L1 L2 L3 L4 L5 L6 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | det | sacrum_detector 0.857 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -3.0579, 'L6': -1.1065} | L6 (1.9514, 1.9514, 1.8408) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | det74 | sacrum_detector 0.857 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -3.0579, 'L6': -1.1065} | L6 (1.9514, 1.9514, 1.583) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.4254, 'T13': -4.0472, 'L6': -1.7454} | L6 (1.6799, 1.6799, 0.354) | L1 L2 L3 L4 L5 L6 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | yes | no | disagreement |
| case121 AP | k5 | det | sacrum_detector 0.362 | L1 L2 L3 L4 | - 1 2 3 | - L5 L4 L3 | {'ordinary': -5.0334, 'L6': -7.2506} | ordinary (0.0, 2.2171, 1.2197) | L1 L5 L4 L3 | None None None None | None None None None | no | no | disagreement |
| case121 AP | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.2197) | L2 L3 L4 L5 | L2 L3 L4 L5 | L1 L2 L3 L4 | yes | yes | no_anchor |
| case121 AP | k5 | det74 | none (rejected 0.362) | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 | None None None None | None None None None | no | no | no_anchor |
| case121 AP | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | L2 L3 L4 L5 | L1 L2 L3 L4 | yes | yes | no_anchor |
| case121 AP | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.0199) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case121 AP | k5 | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -2.9916, 'T13': -3.668, 'L6': -3.4206} | ordinary (0.0, 0.429, 0.0199) | T12 L1 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | quiet |
| case121 AP | kfull | det | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.5792) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | kfull | det74 | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.5687) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | kfull | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -2.5431, 'T13': -3.1272, 'L6': -3.82} | ordinary (0.0, 0.5841, 0.3527) | T12 L1 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | quiet |
| case121 LAT | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.2197) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.3624, 'L6': -4.1623} | ordinary (0.0, 3.7999, 0.0199) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case121 LAT | kfull | det | sacrum_detector 0.569 | L2 L3 L4 L5 | 4 3 2 1 | L2 L3 L4 L5 | {'ordinary': -0.9847, 'L6': -2.402} | ordinary (0.0, 1.4173, 1.5792) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | low_margin |
| case121 LAT | kfull | det74 | none (rejected 0.569) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.5687) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.4177, 'L6': -3.7268} | ordinary (0.0, 3.3091, 0.3527) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case136 AP | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.2457) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 AP | k5 | det | sacrum_detector 0.375 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.9911, 'L6': -2.4169} | ordinary (0.0, 0.4258, 1.2457) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 AP | k5 | det74 | none (rejected 0.375) | L2 L3 L4 L5 sacrum | - - - - - | - - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 sacrum | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case136 AP | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.0197) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case136 AP | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.5965, 'T13': -3.7068, 'L6': -3.2646} | L6 (0.3319, 0.3319, 0.0197) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | det | sacrum_detector 0.835 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.9456, 'L6': -2.3306} | ordinary (0.0, 0.3849, 2.079) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | det74 | sacrum_detector 0.835 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.9456, 'L6': -2.3306} | ordinary (0.0, 0.3849, 2.0769) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.7955, 'T13': -3.9083, 'L6': -3.0082} | L6 (0.7872, 0.7872, 0.3042) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case136 LAT | k5 | det | sacrum_detector 0.477 | L2 L3 L4 L5 | 2 1 - - | L4 L5 - - | {'ordinary': -9.9472, 'L6': -10.6811} | ordinary (0.0, 0.7338, 1.2457) | L4 L5 L4 L5 | None None None None | None None None None | no | no | disagreement |
| case136 LAT | k5 | det | sacrum_detector 0.672 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.4041, 'L6': -1.6231} | ordinary (0.0, 0.219, 1.2457) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | k5 | det74 | none (rejected 0.477) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 LAT | k5 | det74 | none (rejected 0.672) | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case136 LAT | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.0197) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case136 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -2.2885, 'T13': -3.401, 'L6': -2.5466} | ordinary (0.0, 0.2581, 0.0197) | L1 T12 L2 L3 L4 L5 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 LAT | kfull | det | sacrum_detector 0.79 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.9717, 'L6': -2.7208} | ordinary (0.0, 1.7492, 2.079) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | kfull | det74 | sacrum_detector 0.79 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.9717, 'L6': -2.7208} | ordinary (0.0, 1.7492, 2.0769) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -1.6083, 'T13': -2.6137, 'L6': -2.8717} | ordinary (0.0, 1.0054, 0.3042) | L1 T12 L2 L3 L4 L5 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | no | no | disagreement |

- **det, whole frames with an anchor: 5 of 6**; coupled names equal VERIDAH's on 1, TotalSegmentator's on 4; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 3; calls {'ordinary': 4, 'L6': 1}; flagged 4 ({'disagreement': 2, 'low_margin': 2}).
- **det74, whole frames with an anchor: 4 of 6**; coupled names equal VERIDAH's on 1, TotalSegmentator's on 3; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 2; calls {'ordinary': 3, 'L6': 1}; flagged 3 ({'disagreement': 2, 'low_margin': 1}).
- **oracle, whole frames with an anchor: 6 of 6**; coupled names equal VERIDAH's on 1, TotalSegmentator's on 2; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 1; calls {'ordinary': 4, 'L6': 2}; flagged 4 ({'disagreement': 4}).

## Anomalous renders: the sweep decoder's variant calls already on disk (sweep_v3, not recomputed)

Source: `/wsu/home/go/go24/go2432/model_night/sweep_v3/<group>/<tag>/sweep.json` (62 arms), collected by `SchwingNet/tools/sweep_variant_calls.py` into `SchwingNet/results/sweep_variant_calls.json`. Truth class from the chain's truth names (L6 present, T13 present, both, L4 directly above the sacrum). `own call` = the decoder's variant_call names the spine's own class (L6 or both for an L6 spine; T13 or both for a T13 spine); `anchor` = the sacrum (or C2) was in the chain, which the alphabet call needs. Chain naming accuracy: count (ordinary alphabet from the anchor), morph (the head's anchored decode), variant (the winning alphabet's names). These arms are sweeps over rendered CTs with the sweep decoder, not single frames with this coupler; they show what the same alphabet rule does on a chain that reaches the sacrum.

| arm | sources / anchor / alphabets / held out | class | spines | anchor in chain | own call (all / anchored) | calls | chain count | chain morph | chain variant |
|---|---|---|---|---|---|---|---|---|---|
| end/fixed_ctl | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| end/fixed_ctl | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.0667 (1/15) | 0.2667 | 0.0667 (1/15) |
| end/fixed_ctl | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'T13': 2, 'L6': 1} | 0.993 (996/1003) | 0.993 | 0.993 (996/1003) |
| end/fixed_open | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| end/fixed_open | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| end/fixed_open | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1013/1015) | 0.998 | 0.998 (1013/1015) |
| end/fixed_skip | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| end/fixed_skip | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| end/fixed_skip | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1012/1014) | 0.998 | 0.998 (1012/1014) |
| end/fixed_skip_open | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| end/fixed_skip_open | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| end/fixed_skip_open | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1012/1014) | 0.998 | 0.998 (1012/1014) |
| end/jit_open | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| end/jit_open | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| end/jit_open | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1013/1015) | 0.998 | 0.998 (1013/1015) |
| end/jit_skip_open | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| end/jit_skip_open | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| end/jit_skip_open | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1012/1014) | 0.998 | 0.998 (1012/1014) |
| fix/ctsp_o2_det_local | None / None / None / NOT held out | L4 | 5 | 5 | 0/5 / 0/5 | {'T13': 1, 'ordinary': 4} | 0.3684 (14/38) | 0.3684 | 0.3158 (12/38) |
| fix/ctsp_o2_det_local | None / None / None / NOT held out | L6 | 1 | 0 | 0/1 / 0/0 | {'ordinary': 1} | 0.0 (0/7) | 0.5714 | 0.5714 (4/7) |
| fix/ctsp_o2_det_local | None / None / None / NOT held out | ordinary | 114 | 47 | 95/114 / 40/47 | {'ordinary': 95, 'T13': 11, 'L6': 4, 'both': 4} | 0.242 (213/880) | 0.4636 | 0.4955 (436/880) |
| fix/ctsp_o2_det_merge | None / None / None / NOT held out | L4 | 5 | 5 | 0/5 / 0/5 | {'T13': 1, 'ordinary': 4} | 0.3684 (14/38) | 0.3684 | 0.3158 (12/38) |
| fix/ctsp_o2_det_merge | None / None / None / NOT held out | L6 | 1 | 0 | 0/1 / 0/0 | {'ordinary': 1} | 0.0 (0/7) | 0.5714 | 0.5714 (4/7) |
| fix/ctsp_o2_det_merge | None / None / None / NOT held out | ordinary | 114 | 47 | 94/114 / 39/47 | {'ordinary': 94, 'T13': 10, 'L6': 4, 'both': 6} | 0.2567 (219/853) | 0.483 | 0.5018 (428/853) |
| fix/ctsp_o2_gt_local | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| fix/ctsp_o2_gt_local | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.0667 (1/15) | 0.2667 | 0.0667 (1/15) |
| fix/ctsp_o2_gt_local | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'T13': 2, 'L6': 1} | 0.993 (996/1003) | 0.993 | 0.993 (996/1003) |
| fix/ctsp_o2_jit_local | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| fix/ctsp_o2_jit_local | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| fix/ctsp_o2_jit_local | None / None / None / NOT held out | ordinary | 115 | 115 | 113/115 / 113/115 | {'ordinary': 113, 'T13': 2} | 0.9941 (1004/1010) | 0.996 | 0.997 (1007/1010) |
| fix/ctsp_o4_jit_local | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| fix/ctsp_o4_jit_local | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| fix/ctsp_o4_jit_local | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'T13': 5, 'L6': 1} | 0.9464 (972/1027) | 0.9494 | 0.9523 (978/1027) |
| fix/films_det | None / None / None / NOT held out | ordinary | 25 | 23 | 24/25 / 22/23 | {'ordinary': 24, 'L6': 1} | 0.9615 (150/156) | 0.9551 | 0.9551 (149/156) |
| fix/films_det_local | None / None / None / NOT held out | ordinary | 25 | 23 | 24/25 / 22/23 | {'ordinary': 24, 'L6': 1} | 0.9615 (150/156) | 0.9551 | 0.9551 (149/156) |
| fix/films_det_merge | None / None / None / NOT held out | ordinary | 25 | 23 | 24/25 / 22/23 | {'ordinary': 24, 'L6': 1} | 0.9615 (150/156) | 0.9551 | 0.9551 (149/156) |
| fix/films_det_merge_local | None / None / None / NOT held out | ordinary | 25 | 23 | 24/25 / 22/23 | {'ordinary': 24, 'L6': 1} | 0.9615 (150/156) | 0.9551 | 0.9551 (149/156) |
| fix/films_gt | None / None / None / NOT held out | ordinary | 25 | 25 | 25/25 / 25/25 | {'ordinary': 25} | 1.0 (159/159) | 1.0 | 1.0 (159/159) |
| fix/films_gt_local | None / None / None / NOT held out | ordinary | 25 | 25 | 25/25 / 25/25 | {'ordinary': 25} | 1.0 (159/159) | 1.0 | 1.0 (159/159) |
| fix/films_gt_merge | None / None / None / NOT held out | ordinary | 25 | 25 | 25/25 / 25/25 | {'ordinary': 25} | 1.0 (159/159) | 1.0 | 1.0 (159/159) |
| fix/verse_gt_local | None / None / None / NOT held out | ordinary | 12 | 12 | 12/12 / 12/12 | {'ordinary': 12} | 1.0 (169/169) | 1.0 | 1.0 (169/169) |
| holdout/ctsp_collim_o1_gt | None / None / None / NOT held out | L4 | 3 | 3 | 0/3 / 0/3 | {'T13': 1, 'ordinary': 2} | 0.1739 (4/23) | 0.1739 | 0.1304 (3/23) |
| holdout/ctsp_collim_o1_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.0714 (1/14) | 0.0714 | 0.0714 (1/14) |
| holdout/ctsp_collim_o1_gt | None / None / None / NOT held out | ordinary | 114 | 114 | 111/114 / 111/114 | {'ordinary': 111, 'T13': 2, 'L6': 1} | 0.9861 (992/1006) | 0.9881 | 0.9771 (983/1006) |
| holdout/ctsp_ii12_o1_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'T13': 1, 'ordinary': 3} | 0.129 (4/31) | 0.129 | 0.1613 (5/31) |
| holdout/ctsp_ii12_o1_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| holdout/ctsp_ii12_o1_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1013/1015) | 0.998 | 0.998 (1013/1015) |
| holdout/ctsp_ii9_o05_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2188 (7/32) | 0.2188 | 0.2188 (7/32) |
| holdout/ctsp_ii9_o05_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| holdout/ctsp_ii9_o05_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'T13': 3} | 0.8759 (854/975) | 0.8779 | 0.879 (857/975) |
| holdout/ctsp_ii9_o15_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| holdout/ctsp_ii9_o15_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| holdout/ctsp_ii9_o15_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'L6': 1, 'T13': 2} | 0.985 (985/1000) | 0.99 | 0.984 (984/1000) |
| holdout/ctsp_ii9_o1_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2581 (8/31) | 0.2581 | 0.2581 (8/31) |
| holdout/ctsp_ii9_o1_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| holdout/ctsp_ii9_o1_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 114/115 / 114/115 | {'ordinary': 114, 'T13': 1} | 0.9921 (1001/1009) | 0.9941 | 0.9941 (1003/1009) |
| holdout/ctsp_ii9_o25_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| holdout/ctsp_ii9_o25_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| holdout/ctsp_ii9_o25_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.9854 (1010/1025) | 0.9854 | 0.9854 (1010/1025) |
| holdout/ctsp_ii9_o2_det | None / None / None / NOT held out | L4 | 5 | 5 | 0/5 / 0/5 | {'T13': 1, 'ordinary': 4} | 0.3684 (14/38) | 0.3684 | 0.3158 (12/38) |
| holdout/ctsp_ii9_o2_det | None / None / None / NOT held out | L6 | 1 | 0 | 0/1 / 0/0 | {'ordinary': 1} | 0.0 (0/7) | 0.5714 | 0.5714 (4/7) |
| holdout/ctsp_ii9_o2_det | None / None / None / NOT held out | ordinary | 114 | 47 | 95/114 / 40/47 | {'ordinary': 95, 'T13': 11, 'L6': 4, 'both': 4} | 0.242 (213/880) | 0.4636 | 0.4955 (436/880) |
| holdout/ctsp_ii9_o2_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| holdout/ctsp_ii9_o2_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| holdout/ctsp_ii9_o2_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 113/115 / 113/115 | {'ordinary': 113, 'T13': 2} | 0.9941 (1004/1010) | 0.996 | 0.997 (1007/1010) |
| holdout/ctsp_ii9_o3_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| holdout/ctsp_ii9_o3_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| holdout/ctsp_ii9_o3_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 114/115 / 114/115 | {'ordinary': 114, 'T13': 1} | 0.9773 (989/1012) | 0.9792 | 0.9792 (991/1012) |
| holdout/ctsp_ii9_o4_gt | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| holdout/ctsp_ii9_o4_gt | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| holdout/ctsp_ii9_o4_gt | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'T13': 5, 'L6': 1} | 0.9464 (972/1027) | 0.9494 | 0.9523 (978/1027) |
| holdout/verse_ii9_o1_gt | None / None / None / NOT held out | ordinary | 12 | 12 | 12/12 / 12/12 | {'ordinary': 12} | 1.0 (169/169) | 1.0 | 1.0 (169/169) |
| improve/base_o3 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/base_o3 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| improve/base_o3 | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'T13': 3} | 0.983 (983/1000) | 0.984 | 0.986 (986/1000) |
| improve/base_o4 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 3, 'both': 1} | 0.1667 (6/36) | 0.1667 | 0.25 (9/36) |
| improve/base_o4 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| improve/base_o4 | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'T13': 6} | 0.9698 (962/992) | 0.9738 | 0.9768 (969/992) |
| improve/e_o2 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/e_o2 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.0667 (1/15) | 0.2667 | 0.0667 (1/15) |
| improve/e_o2 | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'T13': 2, 'L6': 1} | 0.993 (996/1003) | 0.993 | 0.993 (996/1003) |
| improve/g_o2 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/g_o2 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.3 | 0.3 (3/10) |
| improve/g_o2 | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'L6': 2, 'T13': 2, 'both': 2} | 0.9733 (986/1013) | 0.9783 | 0.9733 (986/1013) |
| improve/g_o3 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/g_o3 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| improve/g_o3 | None / None / None / NOT held out | ordinary | 115 | 115 | 108/115 / 108/115 | {'ordinary': 108, 'T13': 5, 'both': 2} | 0.9714 (985/1014) | 0.9763 | 0.9694 (983/1014) |
| improve/g_o4 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/g_o4 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| improve/g_o4 | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'both': 1, 'T13': 5} | 0.9722 (981/1009) | 0.9792 | 0.9722 (981/1009) |
| improve/gpe_o2 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/gpe_o2 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| improve/gpe_o2 | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'L6': 2, 'T13': 2, 'both': 2} | 0.9684 (982/1014) | 0.9773 | 0.9694 (983/1014) |
| improve/gpe_o4 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/gpe_o4 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| improve/gpe_o4 | None / None / None / NOT held out | ordinary | 115 | 115 | 110/115 / 110/115 | {'ordinary': 110, 'both': 1, 'T13': 4} | 0.9751 (981/1006) | 0.9811 | 0.9742 (980/1006) |
| improve/p_o2 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| improve/p_o2 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| improve/p_o2 | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'T13': 2, 'L6': 1} | 0.99 (992/1002) | 0.992 | 0.99 (992/1002) |
| l4/ctsp_fixed_skip_ext | None / None / None / NOT held out | L4 | 4 | 4 | 2/4 / 2/4 | {'ordinary': 2, 'L4': 2} | 0.2121 (7/33) | 0.2121 | 0.6364 (21/33) |
| l4/ctsp_fixed_skip_ext | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| l4/ctsp_fixed_skip_ext | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1012/1014) | 0.998 | 0.998 (1012/1014) |
| l4/ctsp_o2_jit_ext | None / None / None / NOT held out | L4 | 4 | 4 | 2/4 / 2/4 | {'ordinary': 2, 'L4': 2} | 0.2121 (7/33) | 0.2121 | 0.6364 (21/33) |
| l4/ctsp_o2_jit_ext | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| l4/ctsp_o2_jit_ext | None / None / None / NOT held out | ordinary | 115 | 115 | 113/115 / 113/115 | {'ordinary': 113, 'T13': 2} | 0.9941 (1004/1010) | 0.996 | 0.997 (1007/1010) |
| l4/ctsp_o4_jit_ext | None / None / None / NOT held out | L4 | 4 | 4 | 1/4 / 1/4 | {'ordinary': 3, 'L4': 1} | 0.2121 (7/33) | 0.2121 | 0.4242 (14/33) |
| l4/ctsp_o4_jit_ext | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| l4/ctsp_o4_jit_ext | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'T13': 5, 'L6': 1} | 0.9464 (972/1027) | 0.9494 | 0.9523 (978/1027) |
| l4/ts_fixed_skip_ext | None / None / None / NOT held out | L4 | 10 | 9 | 7/10 / 7/9 | {'ordinary': 2, 'L4': 6, 'L4T13': 1, 'T13': 1} | 0.1829 (30/164) | 0.3171 | 0.7561 (124/164) |
| l4/ts_fixed_skip_ext | None / None / None / NOT held out | ordinary | 512 | 510 | 480/512 / 479/510 | {'ordinary': 480, 'T13': 13, 'L6': 6, 'L4': 11, 'both': 1, 'L4T13': 1} | 0.9815 (7441/7581) | 0.9578 | 0.9466 (7176/7581) |
| protocol/o2_adet_fixed_8 | None / None / None / NOT held out | ordinary | 8 | 3 | 3/8 / 0/3 | {'L6': 1, 'both': 4, 'ordinary': 3} | 0.0741 (8/108) | 0.2685 | 0.2407 (26/108) |
| protocol/o2_filmdet_fixed_8 | None / None / None / NOT held out | ordinary | 8 | 4 | 6/8 / 3/4 | {'ordinary': 6, 'T13': 2} | 0.2879 (19/66) | 0.4545 | 0.4545 (30/66) |
| protocol/o2_gt_fixed | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| protocol/o2_gt_fixed | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.0667 (1/15) | 0.2667 | 0.0667 (1/15) |
| protocol/o2_gt_fixed | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'T13': 2, 'L6': 1} | 0.993 (996/1003) | 0.993 | 0.993 (996/1003) |
| protocol/o2_gt_fixed_8 | None / None / None / NOT held out | L4 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.4444 (4/9) | 0.4444 | 0.4444 (4/9) |
| protocol/o2_gt_fixed_8 | None / None / None / NOT held out | ordinary | 7 | 7 | 7/7 / 7/7 | {'ordinary': 7} | 1.0 (62/62) | 1.0 | 1.0 (62/62) |
| protocol/o2_gt_jit | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| protocol/o2_gt_jit | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| protocol/o2_gt_jit | None / None / None / NOT held out | ordinary | 115 | 115 | 113/115 / 113/115 | {'ordinary': 113, 'T13': 2} | 0.9941 (1004/1010) | 0.996 | 0.997 (1007/1010) |
| rib/ctsp_fixed_skip_rib2 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| rib/ctsp_fixed_skip_rib2 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| rib/ctsp_fixed_skip_rib2 | None / None / None / NOT held out | ordinary | 115 | 115 | 115/115 / 115/115 | {'ordinary': 115} | 0.998 (1012/1014) | 0.998 | 0.998 (1012/1014) |
| rib/ctsp_o2_jit_rib2 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| rib/ctsp_o2_jit_rib2 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| rib/ctsp_o2_jit_rib2 | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'L6': 1, 'T13': 2} | 0.9941 (1004/1010) | 0.996 | 0.9891 (999/1010) |
| rib/ctsp_o2_jit_rib5 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| rib/ctsp_o2_jit_rib5 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'T13': 1} | 0.1 (1/10) | 0.4 | 0.4 (4/10) |
| rib/ctsp_o2_jit_rib5 | None / None / None / NOT held out | ordinary | 115 | 115 | 112/115 / 112/115 | {'ordinary': 112, 'L6': 1, 'T13': 2} | 0.9941 (1004/1010) | 0.996 | 0.9891 (999/1010) |
| rib/ctsp_o4_jit_rib2 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| rib/ctsp_o4_jit_rib2 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| rib/ctsp_o4_jit_rib2 | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'T13': 5, 'L6': 1} | 0.9464 (972/1027) | 0.9494 | 0.9523 (978/1027) |
| rib/ctsp_o4_jit_rib5 | None / None / None / NOT held out | L4 | 4 | 4 | 0/4 / 0/4 | {'ordinary': 4} | 0.2121 (7/33) | 0.2121 | 0.2121 (7/33) |
| rib/ctsp_o4_jit_rib5 | None / None / None / NOT held out | L6 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.1 (1/10) | 0.4 | 0.1 (1/10) |
| rib/ctsp_o4_jit_rib5 | None / None / None / NOT held out | ordinary | 115 | 115 | 109/115 / 109/115 | {'ordinary': 109, 'T13': 4, 'L6': 2} | 0.9464 (972/1027) | 0.9494 | 0.9503 (976/1027) |
| rib/ts_o2_fixed_skip | None / None / None / NOT held out | L4 | 10 | 9 | 0/10 / 0/9 | {'ordinary': 8, 'T13': 2} | 0.1829 (30/164) | 0.3171 | 0.2927 (48/164) |
| rib/ts_o2_fixed_skip | None / None / None / NOT held out | ordinary | 512 | 510 | 492/512 / 491/510 | {'ordinary': 492, 'T13': 13, 'L6': 6, 'both': 1} | 0.9815 (7441/7581) | 0.9578 | 0.9581 (7263/7581) |
| rib/ts_o2_fixed_skip_open | None / None / None / NOT held out | L4 | 10 | 9 | 0/10 / 0/9 | {'ordinary': 8, 'T13': 2} | 0.1829 (30/164) | 0.3171 | 0.2927 (48/164) |
| rib/ts_o2_fixed_skip_open | None / None / None / NOT held out | ordinary | 512 | 510 | 492/512 / 491/510 | {'ordinary': 492, 'T13': 13, 'L6': 6, 'both': 1} | 0.9817 (7445/7584) | 0.9579 | 0.9582 (7267/7584) |
| rib/ts_o2_fixed_skip_rib2 | None / None / None / NOT held out | L4 | 10 | 9 | 0/10 / 0/9 | {'ordinary': 8, 'T13': 2} | 0.1829 (30/164) | 0.3171 | 0.2927 (48/164) |
| rib/ts_o2_fixed_skip_rib2 | None / None / None / NOT held out | ordinary | 512 | 510 | 493/512 / 492/510 | {'ordinary': 493, 'T13': 13, 'L6': 5, 'both': 1} | 0.9815 (7441/7581) | 0.9578 | 0.9612 (7287/7581) |
| rib/ts_o2_fixed_skip_rib5 | None / None / None / NOT held out | L4 | 10 | 9 | 0/10 / 0/9 | {'ordinary': 8, 'T13': 2} | 0.1829 (30/164) | 0.3171 | 0.2927 (48/164) |
| rib/ts_o2_fixed_skip_rib5 | None / None / None / NOT held out | ordinary | 512 | 510 | 493/512 / 492/510 | {'ordinary': 493, 'T13': 13, 'L6': 5, 'both': 1} | 0.9815 (7441/7581) | 0.9578 | 0.9614 (7288/7581) |
| ts/ts_c2_ii9_o1_gt | None / None / None / NOT held out | L4 | 1 | 1 | 0/1 / 0/1 | {'ordinary': 1} | 0.6667 (16/24) | 0.6667 | 0.6667 (16/24) |
| ts/ts_c2_ii9_o1_gt | None / None / None / NOT held out | ordinary | 202 | 202 | 169/202 / 169/202 | {'ordinary': 169, 'L6': 29, 'both': 3, 'T13': 1} | 0.9498 (2686/2828) | 0.9378 | 0.9402 (2659/2828) |
| ts/ts_ii9_o2_adet | None / None / None / NOT held out | L4 | 28 | 28 | 0/28 / 0/28 | {'ordinary': 3, 'none': 18, 'both': 6, 'L6': 1} | 0.1144 (89/778) | 0.3458 | 0.3419 (266/778) |
| ts/ts_ii9_o2_adet | None / None / None / NOT held out | ordinary | 490 | 127 | 59/490 / 13/127 | {'ordinary': 59, 'none': 186, 'L6': 40, 'both': 176, 'T13': 29} | 0.0462 (495/10712) | 0.3262 | 0.3155 (3380/10712) |
| ts/ts_ii9_o2_det | None / None / None / NOT held out | L4 | 8 | 7 | 0/8 / 0/7 | {'ordinary': 7, 'T13': 1} | 0.3099 (22/71) | 0.2676 | 0.2676 (19/71) |
| ts/ts_ii9_o2_det | None / None / None / NOT held out | ordinary | 364 | 82 | 266/364 / 60/82 | {'ordinary': 266, 'both': 15, 'T13': 68, 'L6': 15} | 0.1003 (332/3310) | 0.3495 | 0.3704 (1226/3310) |
| ts/ts_ii9_o2_gt | None / None / None / NOT held out | L4 | 10 | 9 | 0/10 / 0/9 | {'ordinary': 9, 'T13': 1} | 0.1726 (29/168) | 0.25 | 0.25 (42/168) |
| ts/ts_ii9_o2_gt | None / None / None / NOT held out | ordinary | 512 | 510 | 478/512 / 478/510 | {'ordinary': 478, 'T13': 22, 'L6': 10, 'both': 2} | 0.964 (7364/7639) | 0.9314 | 0.9334 (7130/7639) |
| ts/ts_ii9_o2_gt_fixed | None / None / None / NOT held out | L4 | 10 | 9 | 0/10 / 0/9 | {'ordinary': 9, 'T13': 1} | 0.179 (29/162) | 0.2593 | 0.2593 (42/162) |
| ts/ts_ii9_o2_gt_fixed | None / None / None / NOT held out | ordinary | 512 | 510 | 484/512 / 483/510 | {'ordinary': 484, 'T13': 19, 'L6': 4, 'both': 2, 'none': 3} | 0.9641 (7377/7652) | 0.9399 | 0.9422 (7210/7652) |

## Read this before quoting

- The threshold never saw the fold it is applied to; the disagreement flag has no threshold at all.
- `det` frames without a detected sacrum are `no anchor`: names unchanged, flagged. Their share is in the frames row; the un-anchored classifier accuracy is reported beside the anchored one so the coupled number is never read as the number on every frame.
- An anchored frame whose truth has no sacrum (`anchored without a truth sacrum`) is a false sacrum from the LODO detector; the count then starts from the wrong place. det74 shows what the pre-stated cross-device confidence floor does to that.
- The `_ns` variants were added after inspecting fold 0 (the keypoint detector boxed S1 as a vertebra in case44_LAT and the count named it L6). They are a sensitivity analysis, not the primary result.
- The three L6 patients are a VERIDAH-versus-TotalSegmentator disagreement on a lumbar-only CBCT, not a counted truth. If the coupler calls L6 on them it agrees with VERIDAH; that is all it shows.
- Nothing here was recomputed for the renders: the sweep_v3 calls are whatever the decoder wrote when those arms ran.
