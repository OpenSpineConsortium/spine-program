# Coupling the morphology classifier to the count from the sacrum: C-ArmLSpine folds and the anomalous renders

Generated 2026-09-23 01:48. Numbers: `SchwingNet/results/coupling.json` (this file quotes it; every table cell is a key there). Tools: `tools/alphabet_couple.py` (the coupler; `--self-test` passes on synthetic posteriors: ordinary, L6 with the sixth body called L5, the same upside down and scrambled, one confident error, no sacrum, the sacrum boxed as a vertebra, variant truth, the confidence floor and the named-sacrum switch), `tools/level_prototype.py --dump-posterior --sacrum-detector`, `SchwingNet/tools/coupling_report.py`, `SchwingNet/tools/sweep_variant_calls.py`; jobs `SchwingNet/slurm/coupling.sh` (GPU array, one fold per task) then `SchwingNet/slurm/coupling_eval.sh` (CPU). Jobs: verifier dedupe re-pool.

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

Variants: **det** = keypoint-detector boxes; LODO sacrum, conf >= 0.25; std alphabets; **det74** = keypoint-detector boxes; LODO sacrum, conf >= 0.74 (cross-device operating point); std alphabets; **oracle** = truth body boxes; truth sacrum; std alphabets; **oracle_dd** = oracle with a vertebra box duplicating an earlier one (IoU > 0.9) dropped before counting (--dedupe-boxes); std alphabets.

Per-frame coupler outputs (every ordinal, candidate score and name): `/rs/rs_grp_oschome/go2432/data/carmlspine/proto_post/cv_fold<K>/<det|oracle>/k<full|5>/<couple|couple_c74|couple_ns|couple_ext>/couple_all.json` and one `<stem>.couple.json` per frame; prototype JSONs with the 27-vectors beside them. Shipped CV outputs the classifier numbers are checked against: `/rs/rs_grp_oschome/go2432/data/carmlspine/proto/cv_fold<K>/<arm>_score_k<k>.json`.

## The classifier did not move

`--dump-posterior` and `--sacrum-detector` add fields; they must change no name. Exact-level accuracy of the re-run against the shipped CV output, per fold:

| cell | shipped (scored, exact) | re-run (scored, exact) | identical |
|---|---|---|---|
| cv_fold0/det/kfull | 291, 0.9416 | 291, 0.9416 | yes |
| cv_fold0/det/k5 | 272, 0.9632 | 272, 0.9632 | yes |
| cv_fold0/oracle/kfull | 312, 0.9038 | 312, 0.9038 | yes |
| cv_fold0/oracle/k5 | 299, 0.9064 | 299, 0.9064 | yes |
| cv_fold1/det/kfull | 203, 0.9655 | 203, 0.9655 | yes |
| cv_fold1/det/k5 | 228, 0.9605 | 228, 0.9605 | yes |
| cv_fold1/oracle/kfull | 216, 0.9861 | 216, 0.9861 | yes |
| cv_fold1/oracle/k5 | 250, 0.968 | 250, 0.968 | yes |
| cv_fold2/det/kfull | 225, 0.9822 | 225, 0.9822 | yes |
| cv_fold2/det/k5 | 273, 0.9451 | 273, 0.9451 | yes |
| cv_fold2/oracle/kfull | 256, 0.957 | 256, 0.957 | yes |
| cv_fold2/oracle/k5 | 309, 0.9094 | 309, 0.9094 | yes |
| cv_fold3/det/kfull | 306, 0.9869 | 306, 0.9869 | yes |
| cv_fold3/det/k5 | 326, 0.954 | 326, 0.954 | yes |
| cv_fold3/oracle/kfull | 333, 0.9459 | 333, 0.9459 | yes |
| cv_fold3/oracle/k5 | 363, 0.9063 | 363, 0.9063 | yes |
| cv_fold4/det/kfull | 223, 1.0 | 223, 1.0 | yes |
| cv_fold4/det/k5 | 256, 0.9805 | 256, 0.9805 | yes |
| cv_fold4/oracle/kfull | 232, 0.944 | 232, 0.944 | yes |
| cv_fold4/oracle/k5 | 270, 0.863 | 270, 0.863 | yes |

## The thresholds (chosen on the other four folds, applied to the fifth)

| variant / field / fold | tau on margin_next | frames it was chosen on |
|---|---|---|
| det/kfull/fold0 | 1.7051 | 197 |
| det/kfull/fold1 | 1.6117 | 212 |
| det/kfull/fold2 | 1.7236 | 202 |
| det/kfull/fold3 | 2.3011 | 189 |
| det/kfull/fold4 | 2.0487 | 208 |
| det/k5/fold0 | 1.9538 | 99 |
| det/k5/fold1 | 1.9481 | 104 |
| det/k5/fold2 | 1.9834 | 107 |
| det/k5/fold3 | 2.1105 | 101 |
| det/k5/fold4 | 2.1105 | 101 |
| det74/kfull/fold0 | 1.7077 | 178 |
| det74/kfull/fold1 | 1.6 | 190 |
| det74/kfull/fold2 | 1.6524 | 179 |
| det74/kfull/fold3 | 2.2842 | 168 |
| det74/kfull/fold4 | 2.0217 | 185 |
| det74/k5/fold0 | none (too few frames) | 5 |
| det74/k5/fold1 | none (too few frames) | 5 |
| det74/k5/fold2 | none (too few frames) | 4 |
| det74/k5/fold3 | none (too few frames) | 2 |
| det74/k5/fold4 | none (too few frames) | 4 |
| oracle/kfull/fold0 | 0.5272 | 191 |
| oracle/kfull/fold1 | 0.5312 | 206 |
| oracle/kfull/fold2 | 0.5456 | 200 |
| oracle/kfull/fold3 | 0.5481 | 183 |
| oracle/kfull/fold4 | 0.5674 | 204 |
| oracle/k5/fold0 | 0.503 | 35 |
| oracle/k5/fold1 | 0.291 | 37 |
| oracle/k5/fold2 | 0.2537 | 32 |
| oracle/k5/fold3 | 0.6105 | 37 |
| oracle/k5/fold4 | 0.306 | 39 |
| oracle_dd/kfull/fold0 | 0.7749 | 212 |
| oracle_dd/kfull/fold1 | 0.8631 | 233 |
| oracle_dd/kfull/fold2 | 0.8996 | 224 |
| oracle_dd/kfull/fold3 | 0.8376 | 209 |
| oracle_dd/kfull/fold4 | 0.8866 | 230 |
| oracle_dd/k5/fold0 | 0.555 | 39 |
| oracle_dd/k5/fold1 | 0.3328 | 42 |
| oracle_dd/k5/fold2 | 0.291 | 37 |
| oracle_dd/k5/fold3 | 0.6232 | 41 |
| oracle_dd/k5/fold4 | 0.3209 | 41 |

## C-ArmLSpine, five test folds pooled (truth = the two CBCT labellers agree)

k = full is the whole frame; k = 5 a crop holding five truth vertebrae (the sacrum is in the crop only when its centre falls inside). Bodies are scored where a call matches a truth body with an agreed level; a det frame with no detected sacrum is `no anchor` (names unchanged, flagged).

| cell | quantity | value [95 % CI, case bootstrap] (k/n) |
|---|---|---|
| det/kfull | frames | 290 (145 cases); anchored 266; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det/kfull | (i) classifier alone, all scored bodies | 97.4 % [95.3, 99.2] (1216/1248) |
| det/kfull | (ii) coupled names, all scored bodies | 96.7 % [94.7, 98.5] (1207/1248); paired difference -0.7 pp [-2.4, +1.0] |
| det/kfull | (iii) coupled names, anchored frames only | 97.5 % [95.7, 99.0] (1123/1152); classifier on the same bodies 98.3 % [96.5, 99.6] (1132/1152); paired difference -0.8 pp [-2.6, +1.2] |
| det/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 96.1 % [93.5, 98.3] (1104/1149); coupled on the same bodies 97.5 % [95.7, 99.0] (1120/1149); classifier 98.3 % [96.5, 99.6] (1129/1149); coupled minus count +1.4 pp [+0.0, +3.4] |
| det/kfull | classifier on un-anchored frames | 87.5 % [73.3, 100.0] (84/96) |
| det/kfull | frame-exact (every scored body right), anchored frames | classifier 97.7 % [95.7, 99.2] (256/262); coupled 96.2 % [93.8, 98.5] (252/262) |
| det/kfull | disagreement | bodies 4.4 % [2.2, 6.8] (53/1214); frames with any 6.8 % [3.5, 10.2] (18/266) |
| det/kfull | accuracy when the two agree | coupled = classifier 99.8 % [99.5, 100.0] (1107/1109) |
| det/kfull | accuracy when they disagree | coupled 32.5 % [0.0, 60.5] (13/40); classifier 55.0 % [26.8, 84.2] (22/40); neither 5 of 40 |
| det/kfull | the count vs the classifier (counted bodies with truth, n = 1149) | corrects a classifier error 13 of 20; introduces an error 22 of 1129 classifier-correct bodies; both wrong 7 |
| det/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 18.3 % [13.5, 23.4] (53/290) of all frames, 10.9 % [7.1, 15.1] (29/266) of anchored; reasons {'no_anchor': 21, 'disagreement': 18, 'low_margin': 11, 'no_vertebra': 3} |
| det/kfull | stop signal on anchored frames with truth | fires on 90.0 % [70.0, 100.0] (9/10) of frames with a coupled error; on 7.1 % [3.9, 10.8] (18/252) of fully correct frames; coupled accuracy unflagged 99.9 % [99.7, 100.0] (1040/1041) vs flagged 74.8 % [58.8, 87.3] (83/111) |
| det/kfull | variant calls (anchored frames) | {'ordinary': 260, 'L6': 6}; on the non-ordinary calls: coupled 72.0 % [33.2, 100.0] (18/25), classifier 84.0 % [40.0, 100.0] (21/25), count 4.2 % [0.0, 15.0] (1/24); 6 of 6 flagged; cases ['case106', 'case139', 'case19', 'case44', 'case9'] |
| det/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 6 / 0 |
| det/k5 | frames | 321 (135 cases); anchored 157; truth sacrum in frame 52; anchored without a truth sacrum 125; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det/k5 | (i) classifier alone, all scored bodies | 96.0 % [93.2, 98.5] (1301/1355) |
| det/k5 | (ii) coupled names, all scored bodies | 91.7 % [88.2, 94.9] (1243/1355); paired difference -4.3 pp [-6.0, -2.7] |
| det/k5 | (iii) coupled names, anchored frames only | 90.1 % [86.2, 93.6] (627/696); classifier on the same bodies 98.4 % [95.8, 100.0] (685/696); paired difference -8.3 pp [-11.8, -5.4] |
| det/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.5 % [83.9, 92.6] (587/663); coupled on the same bodies 89.9 % [85.8, 93.5] (596/663); classifier 98.6 % [96.5, 100.0] (654/663); coupled minus count +1.4 pp [-1.0, +4.0] |
| det/k5 | classifier on un-anchored frames | 93.5 % [87.6, 98.0] (616/659) |
| det/k5 | frame-exact (every scored body right), anchored frames | classifier 98.1 % [94.8, 100.0] (154/157); coupled 81.5 % [75.0, 87.6] (128/157) |
| det/k5 | disagreement | bodies 10.7 % [7.0, 15.0] (74/692); frames with any 19.8 % [13.6, 26.6] (31/157) |
| det/k5 | accuracy when the two agree | coupled = classifier 99.3 % [98.0, 100.0] (596/600) |
| det/k5 | accuracy when they disagree | coupled 0.0 % [0.0, 0.0] (0/63); classifier 92.1 % [78.1, 100.0] (58/63); neither 5 of 63 |
| det/k5 | the count vs the classifier (counted bodies with truth, n = 663) | corrects a classifier error 0 of 9; introduces an error 58 of 654 classifier-correct bodies; both wrong 9 |
| det/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 62.9 % [56.0, 69.1] (202/321) of all frames, 24.2 % [17.3, 31.9] (38/157) of anchored; reasons {'no_anchor': 161, 'disagreement': 31, 'low_margin': 7, 'no_vertebra': 3} |
| det/k5 | stop signal on anchored frames with truth | fires on 100.0 % [100.0, 100.0] (29/29) of frames with a coupled error; on 7.0 % [2.5, 12.2] (9/128) of fully correct frames; coupled accuracy unflagged 100.0 % [100.0, 100.0] (545/545) vs flagged 54.3 % [42.2, 65.6] (82/151) |
| det/k5 | variant calls (anchored frames) | {'ordinary': 144, 'L6': 13}; on the non-ordinary calls: coupled 54.7 % [40.0, 67.3] (29/53), classifier 90.6 % [70.6, 100.0] (48/53), count 13.2 % [0.0, 39.5] (5/38); 13 of 13 flagged; cases ['case125', 'case139', 'case38', 'case4', 'case5', 'case60', 'case65', 'case67', 'case69', 'case77', 'case88', 'case9'] |
| det/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 4 / 0 |
| det74/kfull | frames | 290 (145 cases); anchored 233; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 53; anchor rejected by the confidence floor 34 |
| det74/kfull | (i) classifier alone, all scored bodies | 97.4 % [95.3, 99.2] (1216/1248) |
| det74/kfull | (ii) coupled names, all scored bodies | 97.6 % [95.8, 99.1] (1218/1248); paired difference +0.2 pp [-1.3, +1.7] |
| det74/kfull | (iii) coupled names, anchored frames only | 98.6 % [97.2, 99.7] (995/1009); classifier on the same bodies 98.4 % [96.8, 99.7] (993/1009); paired difference +0.2 pp [-1.7, +2.1] |
| det74/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.0 % [94.2, 99.2] (979/1009); coupled on the same bodies 98.6 % [97.2, 99.7] (995/1009); classifier 98.4 % [96.8, 99.7] (993/1009); coupled minus count +1.6 pp [+0.0, +3.8] |
| det74/kfull | classifier on un-anchored frames | 93.3 % [86.3, 98.7] (223/239) |
| det74/kfull | frame-exact (every scored body right), anchored frames | classifier 97.8 % [96.0, 99.6] (225/230); coupled 97.8 % [95.7, 99.6] (225/230) |
| det74/kfull | disagreement | bodies 3.2 % [1.4, 5.4] (34/1066); frames with any 5.1 % [2.5, 8.7] (12/233) |
| det74/kfull | accuracy when the two agree | coupled = classifier 99.9 % [99.7, 100.0] (982/983) |
| det74/kfull | accuracy when they disagree | coupled 50.0 % [15.4, 84.0] (13/26); classifier 42.3 % [10.7, 81.8] (11/26); neither 2 of 26 |
| det74/kfull | the count vs the classifier (counted bodies with truth, n = 1009) | corrects a classifier error 13 of 16; introduces an error 11 of 993 classifier-correct bodies; both wrong 3 |
| det74/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 27.2 % [21.4, 33.5] (79/290) of all frames, 9.4 % [5.6, 13.9] (22/233) of anchored; reasons {'no_anchor': 54, 'disagreement': 12, 'low_margin': 10, 'no_vertebra': 3} |
| det74/kfull | stop signal on anchored frames with truth | fires on 80.0 % [40.0, 100.0] (4/5) of frames with a coupled error; on 7.6 % [4.0, 11.6] (17/225) of fully correct frames; coupled accuracy unflagged 99.9 % [99.7, 100.0] (921/922) vs flagged 85.1 % [69.5, 96.7] (74/87) |
| det74/kfull | variant calls (anchored frames) | {'ordinary': 229, 'L6': 4}; on the non-ordinary calls: coupled 100.0 % [100.0, 100.0] (16/16), classifier 100.0 % [100.0, 100.0] (16/16), count 0.0 % [0.0, 0.0] (0/16); 4 of 4 flagged; cases ['case106', 'case139', 'case44'] |
| det74/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 6 / 0 |
| det74/k5 | frames | 321 (135 cases); anchored 6; truth sacrum in frame 52; anchored without a truth sacrum 3; truth sacrum but no anchor 49; anchor rejected by the confidence floor 152 |
| det74/k5 | (i) classifier alone, all scored bodies | 96.0 % [93.2, 98.5] (1301/1355) |
| det74/k5 | (ii) coupled names, all scored bodies | 96.0 % [93.2, 98.5] (1301/1355); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iii) coupled names, anchored frames only | 82.8 % [62.5, 100.0] (24/29); classifier on the same bodies 82.8 % [62.5, 100.0] (24/29); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 100.0 % [100.0, 100.0] (29/29); coupled on the same bodies 82.8 % [62.5, 100.0] (24/29); classifier 82.8 % [62.5, 100.0] (24/29); coupled minus count -17.2 pp [-37.5, +0.0] |
| det74/k5 | classifier on un-anchored frames | 96.3 % [93.4, 98.8] (1277/1326) |
| det74/k5 | frame-exact (every scored body right), anchored frames | classifier 83.3 % [62.5, 100.0] (5/6); coupled 83.3 % [62.5, 100.0] (5/6) |
| det74/k5 | disagreement | bodies 3.5 % [0.0, 7.5] (1/29); frames with any 16.7 % [0.0, 37.5] (1/6) |
| det74/k5 | accuracy when the two agree | coupled = classifier 85.7 % [67.6, 100.0] (24/28) |
| det74/k5 | accuracy when they disagree | coupled 0.0 % (0/1); classifier 0.0 % (0/1); neither 1 of 1 |
| det74/k5 | the count vs the classifier (counted bodies with truth, n = 29) | corrects a classifier error 0 of 5; introduces an error 0 of 24 classifier-correct bodies; both wrong 5 |
| det74/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 98.4 % [97.0, 99.7] (316/321) of all frames, 16.7 % [0.0, 37.5] (1/6) of anchored; reasons {'no_anchor': 312, 'no_vertebra': 3, 'disagreement': 1} |
| det74/k5 | stop signal on anchored frames with truth | fires on 100.0 % (1/1) of frames with a coupled error; on 0.0 % [0.0, 0.0] (0/5) of fully correct frames; coupled accuracy unflagged 100.0 % [100.0, 100.0] (24/24) vs flagged 0.0 % (0/5) |
| det74/k5 | variant calls (anchored frames) | {'ordinary': 5, 'L6': 1}; on the non-ordinary calls: coupled 0.0 % (0/5), classifier 0.0 % (0/5), count 100.0 % (5/5); 1 of 1 flagged; cases ['case125'] |
| det74/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 1 / 0 |
| oracle/kfull | frames | 290 (145 cases); anchored 286; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle/kfull | (i) classifier alone, all scored bodies | 94.4 % [91.7, 96.9] (1274/1349) |
| oracle/kfull | (ii) coupled names, all scored bodies | 95.6 % [93.7, 97.4] (1290/1349); paired difference +1.2 pp [-0.9, +3.6] |
| oracle/kfull | (iii) coupled names, anchored frames only | 95.9 % [94.1, 97.5] (1275/1329); classifier on the same bodies 94.7 % [91.8, 97.0] (1259/1329); paired difference +1.2 pp [-1.0, +3.7] |
| oracle/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.7 % [96.7, 98.5] (1298/1329); coupled on the same bodies 95.9 % [94.1, 97.5] (1275/1329); classifier 94.7 % [91.8, 97.0] (1259/1329); coupled minus count -1.7 pp [-3.3, -0.4] |
| oracle/kfull | classifier on un-anchored frames | 75.0 % [50.0, 100.0] (15/20) |
| oracle/kfull | frame-exact (every scored body right), anchored frames | classifier 87.6 % [82.6, 91.8] (247/282); coupled 87.2 % [82.6, 91.1] (246/282) |
| oracle/kfull | disagreement | bodies 5.5 % [3.3, 7.9] (80/1455); frames with any 9.1 % [5.9, 12.6] (26/286) |
| oracle/kfull | accuracy when the two agree | coupled = classifier 97.3 % [95.7, 98.6] (1239/1273) |
| oracle/kfull | accuracy when they disagree | coupled 64.3 % [35.3, 85.1] (36/56); classifier 35.7 % [14.9, 64.7] (20/56); neither 0 of 56 |
| oracle/kfull | the count vs the classifier (counted bodies with truth, n = 1329) | corrects a classifier error 36 of 70; introduces an error 20 of 1259 classifier-correct bodies; both wrong 34 |
| oracle/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 15.5 % [10.7, 20.7] (45/290) of all frames, 14.3 % [10.1, 19.2] (41/286) of anchored; reasons {'no_anchor': 4, 'disagreement': 26, 'low_margin': 15} |
| oracle/kfull | stop signal on anchored frames with truth | fires on 50.0 % [31.6, 67.7] (18/36) of frames with a coupled error; on 8.9 % [4.9, 13.4] (22/246) of fully correct frames; coupled accuracy unflagged 98.4 % [97.6, 99.2] (1121/1139) vs flagged 81.0 % [70.8, 89.9] (154/190) |
| oracle/kfull | variant calls (anchored frames) | {'ordinary': 281, 'L6': 5}; on the non-ordinary calls: coupled 0.0 % [0.0, 0.0] (0/23), classifier 43.5 % [0.0, 83.3] (10/23), count 100.0 % [100.0, 100.0] (23/23); 5 of 5 flagged; cases ['case132', 'case133', 'case19', 'case54', 'case92'] |
| oracle/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 3 / 0 |
| oracle/k5 | frames | 321 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle/k5 | (i) classifier alone, all scored bodies | 91.0 % [86.8, 94.7] (1356/1491) |
| oracle/k5 | (ii) coupled names, all scored bodies | 92.1 % [88.1, 95.3] (1373/1491); paired difference +1.1 pp [-0.3, +2.8] |
| oracle/k5 | (iii) coupled names, anchored frames only | 92.6 % [82.7, 99.2] (238/257); classifier on the same bodies 86.0 % [75.1, 95.4] (221/257); paired difference +6.6 pp [-1.9, +16.2] |
| oracle/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 98.4 % [96.3, 100.0] (253/257); coupled on the same bodies 92.6 % [82.7, 99.2] (238/257); classifier 86.0 % [75.1, 95.4] (221/257); coupled minus count -5.8 pp [-15.9, +0.0] |
| oracle/k5 | classifier on un-anchored frames | 92.0 % [88.1, 95.1] (1135/1234) |
| oracle/k5 | frame-exact (every scored body right), anchored frames | classifier 82.7 % [71.2, 92.7] (43/52); coupled 86.5 % [74.0, 96.2] (45/52) |
| oracle/k5 | disagreement | bodies 14.8 % [6.8, 22.9] (42/283); frames with any 23.1 % [10.9, 35.9] (12/52) |
| oracle/k5 | accuracy when the two agree | coupled = classifier 95.1 % [85.4, 100.0] (213/224) |
| oracle/k5 | accuracy when they disagree | coupled 75.8 % [42.9, 100.0] (25/33); classifier 24.2 % [0.0, 57.1] (8/33); neither 0 of 33 |
| oracle/k5 | the count vs the classifier (counted bodies with truth, n = 257) | corrects a classifier error 25 of 36; introduces an error 8 of 221 classifier-correct bodies; both wrong 11 |
| oracle/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 88.2 % [83.9, 92.0] (283/321) of all frames, 26.9 % [12.5, 41.7] (14/52) of anchored; reasons {'no_anchor': 269, 'disagreement': 12, 'low_margin': 2} |
| oracle/k5 | stop signal on anchored frames with truth | fires on 85.7 % [40.0, 100.0] (6/7) of frames with a coupled error; on 17.8 % [6.8, 31.1] (8/45) of fully correct frames; coupled accuracy unflagged 99.5 % [98.3, 100.0] (186/187) vs flagged 74.3 % [50.0, 96.8] (52/70) |
| oracle/k5 | variant calls (anchored frames) | {'ordinary': 49, 'L6': 3}; on the non-ordinary calls: coupled 0.0 % [0.0, 0.0] (0/15), classifier 33.3 % [0.0, 100.0] (5/15), count 100.0 % [100.0, 100.0] (15/15); 3 of 3 flagged; cases ['case132', 'case92'] |
| oracle/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 6 / 0 |

### Sensitivity variants (same folds; only the rows that change)

| cell | quantity | value |
|---|---|---|
| oracle_dd/kfull | frames | 290 (145 cases); anchored 286; truth sacrum in frame 286; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_dd/kfull | (i) classifier alone, all scored bodies | 94.4 % [91.7, 96.8] (1239/1312) |
| oracle_dd/kfull | (ii) coupled names, all scored bodies | 98.2 % [96.4, 99.6] (1288/1312); paired difference +3.7 pp [+1.7, +6.1] |
| oracle_dd/kfull | (iii) coupled names, anchored frames only | 98.5 % [97.0, 99.7] (1273/1292); classifier on the same bodies 94.7 % [91.9, 97.0] (1224/1292); paired difference +3.8 pp [+1.5, +6.2] |
| oracle_dd/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 99.6 % [98.8, 100.0] (1287/1292); coupled on the same bodies 98.5 % [97.0, 99.7] (1273/1292); classifier 94.7 % [91.9, 97.0] (1224/1292); coupled minus count -1.1 pp [-2.4, +0.0] |
| oracle_dd/kfull | the count vs the classifier (counted bodies with truth, n = 1292) | corrects a classifier error 56 of 68; introduces an error 7 of 1224 classifier-correct bodies; both wrong 12 |
| oracle_dd/kfull | variant calls (anchored frames) | {'ordinary': 283, 'L6': 3}; on the non-ordinary calls: coupled 0.0 % [0.0, 0.0] (0/14), classifier 35.7 % [0.0, 100.0] (5/14), count 100.0 % [100.0, 100.0] (14/14); 3 of 3 flagged; cases ['case132', 'case19', 'case54'] |
| oracle_dd/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 2 / 0 |
| oracle_dd/k5 | frames | 321 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_dd/k5 | (i) classifier alone, all scored bodies | 90.8 % [86.5, 94.4] (1304/1436) |
| oracle_dd/k5 | (ii) coupled names, all scored bodies | 92.6 % [88.7, 95.7] (1330/1436); paired difference +1.8 pp [+0.5, +3.4] |
| oracle_dd/k5 | (iii) coupled names, anchored frames only | 96.0 % [87.3, 100.0] (240/250); classifier on the same bodies 85.6 % [74.9, 95.4] (214/250); paired difference +10.4 pp [+2.8, +18.8] |
| oracle_dd/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 100.0 % [100.0, 100.0] (250/250); coupled on the same bodies 96.0 % [87.3, 100.0] (240/250); classifier 85.6 % [74.9, 95.4] (214/250); coupled minus count -4.0 pp [-12.7, +0.0] |
| oracle_dd/k5 | the count vs the classifier (counted bodies with truth, n = 250) | corrects a classifier error 26 of 36; introduces an error 0 of 214 classifier-correct bodies; both wrong 10 |
| oracle_dd/k5 | variant calls (anchored frames) | {'ordinary': 50, 'L6': 2}; on the non-ordinary calls: coupled 0.0 % (0/10), classifier 0.0 % (0/10), count 100.0 % (10/10); 2 of 2 flagged; cases ['case132'] |
| oracle_dd/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 6 / 0 |

### Same cells, with the three VERIDAH-L6 patients scored under their L6 truth

| cell | quantity | value |
|---|---|---|
| det/kfull | (i) classifier alone, all scored bodies | 95.9 % [93.2, 98.3] (1224/1276) |
| det/kfull | (ii) coupled names, all scored bodies | 95.0 % [92.0, 97.4] (1212/1276); paired difference -0.9 pp [-2.8, +1.0] |
| det/kfull | (iii) coupled names, anchored frames only | 95.9 % [93.3, 98.2] (1128/1176); classifier on the same bodies 96.9 % [94.8, 98.9] (1140/1176); paired difference -1.0 pp [-3.0, +0.9] |
| det/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 94.1 % [90.5, 97.3] (1104/1173); coupled on the same bodies 95.9 % [93.3, 98.2] (1125/1173); classifier 96.9 % [94.8, 98.9] (1137/1173); coupled minus count +1.8 pp [+0.2, +3.9] |
| det/kfull | the count vs the classifier (counted bodies with truth, n = 1173) | corrects a classifier error 14 of 36; introduces an error 26 of 1137 classifier-correct bodies; both wrong 22 |
| det/kfull | variant calls (anchored frames) | {'ordinary': 264, 'L6': 7}; on the non-ordinary calls: coupled 76.7 % [40.0, 100.0] (23/30), classifier 83.3 % [48.0, 100.0] (25/30), count 3.5 % [0.0, 12.5] (1/29); 7 of 7 flagged; cases ['case106', 'case139', 'case19', 'case42', 'case44', 'case9'] |
| det/k5 | (i) classifier alone, all scored bodies | 94.7 % [91.5, 97.5] (1309/1383) |
| det/k5 | (ii) coupled names, all scored bodies | 90.2 % [86.5, 93.8] (1248/1383); paired difference -4.4 pp [-6.1, -2.8] |
| det/k5 | (iii) coupled names, anchored frames only | 88.3 % [83.5, 92.3] (632/716); classifier on the same bodies 96.8 % [93.3, 99.2] (693/716); paired difference -8.5 pp [-12.0, -5.5] |
| det/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 85.9 % [79.9, 90.8] (587/683); coupled on the same bodies 88.0 % [83.0, 92.1] (601/683); classifier 96.9 % [93.7, 99.4] (662/683); coupled minus count +2.1 pp [-0.5, +4.9] |
| det/k5 | the count vs the classifier (counted bodies with truth, n = 683) | corrects a classifier error 1 of 21; introduces an error 62 of 662 classifier-correct bodies; both wrong 20 |
| det/k5 | variant calls (anchored frames) | {'ordinary': 148, 'L6': 15}; on the non-ordinary calls: coupled 58.6 % [44.1, 72.6] (34/58), classifier 89.7 % [71.4, 100.0] (52/58), count 11.6 % [0.0, 34.9] (5/43); 15 of 15 flagged; cases ['case125', 'case136', 'case139', 'case38', 'case4', 'case42', 'case5', 'case60', 'case65', 'case67', 'case69', 'case77', 'case88', 'case9'] |
| det74/kfull | (i) classifier alone, all scored bodies | 95.9 % [93.2, 98.3] (1224/1276) |
| det74/kfull | (ii) coupled names, all scored bodies | 95.9 % [92.9, 98.1] (1223/1276); paired difference -0.1 pp [-1.8, +1.6] |
| det74/kfull | (iii) coupled names, anchored frames only | 97.2 % [94.5, 99.2] (1000/1029); classifier on the same bodies 97.3 % [95.0, 99.2] (1001/1029); paired difference -0.1 pp [-2.1, +1.9] |
| det74/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 95.1 % [91.1, 98.4] (979/1029); coupled on the same bodies 97.2 % [94.5, 99.2] (1000/1029); classifier 97.3 % [95.0, 99.2] (1001/1029); coupled minus count +2.0 pp [+0.3, +4.4] |
| det74/kfull | the count vs the classifier (counted bodies with truth, n = 1029) | corrects a classifier error 14 of 28; introduces an error 15 of 1001 classifier-correct bodies; both wrong 14 |
| det74/kfull | variant calls (anchored frames) | {'ordinary': 232, 'L6': 5}; on the non-ordinary calls: coupled 100.0 % [100.0, 100.0] (21/21), classifier 95.2 % [84.2, 100.0] (20/21), count 0.0 % [0.0, 0.0] (0/21); 5 of 5 flagged; cases ['case106', 'case139', 'case42', 'case44'] |
| det74/k5 | (i) classifier alone, all scored bodies | 94.7 % [91.5, 97.5] (1309/1383) |
| det74/k5 | (ii) coupled names, all scored bodies | 94.7 % [91.5, 97.5] (1309/1383); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iii) coupled names, anchored frames only | 82.8 % [62.5, 100.0] (24/29); classifier on the same bodies 82.8 % [62.5, 100.0] (24/29); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 100.0 % [100.0, 100.0] (29/29); coupled on the same bodies 82.8 % [62.5, 100.0] (24/29); classifier 82.8 % [62.5, 100.0] (24/29); coupled minus count -17.2 pp [-37.5, +0.0] |
| det74/k5 | the count vs the classifier (counted bodies with truth, n = 29) | corrects a classifier error 0 of 5; introduces an error 0 of 24 classifier-correct bodies; both wrong 5 |
| det74/k5 | variant calls (anchored frames) | {'ordinary': 5, 'L6': 1}; on the non-ordinary calls: coupled 0.0 % (0/5), classifier 0.0 % (0/5), count 100.0 % (5/5); 1 of 1 flagged; cases ['case125'] |
| oracle/kfull | (i) classifier alone, all scored bodies | 93.4 % [90.3, 96.1] (1288/1379) |
| oracle/kfull | (ii) coupled names, all scored bodies | 95.1 % [93.1, 96.9] (1312/1379); paired difference +1.7 pp [-0.4, +4.1] |
| oracle/kfull | (iii) coupled names, anchored frames only | 95.4 % [93.4, 97.2] (1297/1359); classifier on the same bodies 93.7 % [90.5, 96.4] (1273/1359); paired difference +1.8 pp [-0.4, +4.2] |
| oracle/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 95.5 % [92.6, 97.8] (1298/1359); coupled on the same bodies 95.4 % [93.4, 97.2] (1297/1359); classifier 93.7 % [90.5, 96.4] (1273/1359); coupled minus count -0.1 pp [-2.4, +2.6] |
| oracle/kfull | the count vs the classifier (counted bodies with truth, n = 1359) | corrects a classifier error 45 of 86; introduces an error 21 of 1273 classifier-correct bodies; both wrong 41 |
| oracle/kfull | variant calls (anchored frames) | {'ordinary': 282, 'L6': 10}; on the non-ordinary calls: coupled 45.8 % [10.3, 73.5] (22/48), classifier 50.0 % [17.1, 72.9] (24/48), count 47.9 % [16.7, 87.2] (23/48); 10 of 10 flagged; cases ['case121', 'case132', 'case133', 'case136', 'case19', 'case42', 'case54', 'case92'] |
| oracle/k5 | (i) classifier alone, all scored bodies | 90.1 % [85.8, 93.9] (1370/1521) |
| oracle/k5 | (ii) coupled names, all scored bodies | 91.7 % [87.9, 95.1] (1395/1521); paired difference +1.6 pp [+0.1, +3.5] |
| oracle/k5 | (iii) coupled names, anchored frames only | 90.6 % [81.9, 97.9] (260/287); classifier on the same bodies 81.9 % [70.4, 92.1] (235/287); paired difference +8.7 pp [+0.4, +17.4] |
| oracle/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.1 % [76.0, 98.6] (253/287); coupled on the same bodies 90.6 % [81.9, 97.9] (260/287); classifier 81.9 % [70.4, 92.1] (235/287); coupled minus count +2.4 pp [-9.8, +14.3] |
| oracle/k5 | the count vs the classifier (counted bodies with truth, n = 287) | corrects a classifier error 34 of 52; introduces an error 9 of 235 classifier-correct bodies; both wrong 18 |
| oracle/k5 | variant calls (anchored frames) | {'ordinary': 50, 'L6': 8}; on the non-ordinary calls: coupled 55.0 % [13.3, 90.0] (22/40), classifier 47.5 % [14.3, 77.5] (19/40), count 37.5 % [0.0, 83.3] (15/40); 8 of 8 flagged; cases ['case121', 'case132', 'case136', 'case42', 'case92'] |

### Per truth level (all scored bodies; classifier / coupled exact, %)

- **det/kfull**: L1 n=157 98.1/98.1; L2 n=256 96.9/95.3; L3 n=282 97.2/95.7; L4 n=283 97.2/96.5; L5 n=269 98.1/98.5; T12 n=1 100.0/100.0
- **det/k5**: L1 n=194 94.3/92.3; L2 n=289 95.5/90.0; L3 n=314 95.9/87.9; L4 n=312 96.5/93.9; L5 n=245 98.0/95.9; T12 n=1 0.0/0.0
- **det74/kfull**: L1 n=157 98.1/98.1; L2 n=256 96.9/96.9; L3 n=282 97.2/97.2; L4 n=283 97.2/97.2; L5 n=269 98.1/98.9; T12 n=1 100.0/100.0
- **det74/k5**: L1 n=194 94.3/94.3; L2 n=289 95.5/95.5; L3 n=314 95.9/95.9; L4 n=312 96.5/96.5; L5 n=245 98.0/98.0; T12 n=1 0.0/0.0
- **oracle/kfull**: L1 n=209 93.8/92.3; L2 n=284 89.8/90.8; L3 n=286 96.2/97.9; L4 n=286 95.8/97.5; L5 n=278 97.5/98.9; T12 n=6 50.0/83.3
- **oracle/k5**: L1 n=271 87.5/88.2; L2 n=320 87.2/88.4; L3 n=320 92.8/94.1; L4 n=317 92.4/93.7; L5 n=251 97.2/98.0; T12 n=12 50.0/58.3

## The three real L6 patients, frame by frame

**What the truth is here, plainly.** case42, case121 and case136 are the C-ArmLSpine CBCTs SPINEPS/VERIDAH read as L2-L6 and TotalSegmentator read as L1-L5 (TotalSegmentator has no L6 class). Both saw the same lumbar-only CBCT; neither saw the thoracolumbar junction or the ribs, so neither could count. The L6 rests on VERIDAH's morphology read of the CT, not on a count from a junction. Below, `VERIDAH truth` is that naming read from the truth sacrum by the L6 alphabet and `TS read` the same bodies under TotalSegmentator's naming. A coupled call of L6 agrees with VERIDAH; ordinary agrees with TotalSegmentator; the frames alone cannot say which is right. Each frame shows FIVE bodies above the sacrum (the top body is boxed twice in the truth, once per labeller; the duplicate is dropped). `count` is the ordinary alphabet at the ordinal, which cannot name an L6.

| case view | field | variant | anchor | classifier names (top to bottom) | ordinals | count | candidate scores | call (margin, margin_next, tau) | coupled | VERIDAH truth | TS read | coupled = VERIDAH | classifier = VERIDAH | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| case42 AP | k5 | det | none | L2 L3 L4 L5 sacrum | - - - - - | - - - - - | {} | no anchor (None, None, 1.9834) | L2 L3 L4 L5 sacrum | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | det | sacrum_detector 0.734 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.3932, 'L6': -2.1009} | ordinary (0.0, 0.7077, 1.9834) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case42 AP | k5 | det74 | none | L2 L3 L4 L5 sacrum | - - - - - | - - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 sacrum | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | det74 | none (rejected 0.734) | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case42 AP | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.2537) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -3.1751, 'T13': -3.2353, 'L6': -2.0881} | L6 (1.087, 1.087, 0.2537) | L2 L1 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | yes | no | disagreement |
| case42 AP | kfull | det | sacrum_detector 0.877 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.313, 'L6': -2.2011} | ordinary (0.0, 0.8881, 1.7236) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case42 AP | kfull | det74 | sacrum_detector 0.877 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.313, 'L6': -2.2011} | ordinary (0.0, 0.8881, 1.6524) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case42 AP | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -3.2419, 'T13': -3.2695, 'L6': -2.0154} | L6 (1.2265, 1.2265, 0.5456) | L2 L1 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.9834) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case42 LAT | k5 | det | sacrum_detector 0.32 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -2.373, 'L6': -0.886} | L6 (1.4869, 1.4869, 1.9834) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case42 LAT | k5 | det74 | none (rejected 0.32) | L2 L3 L4 L5 sacrum | - - - - - | - - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 sacrum | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case42 LAT | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.2537) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -4.5533, 'T13': -4.8429, 'L6': -1.8745} | L6 (2.6788, 2.6788, 0.2537) | L1 L2 L3 L4 L5 L6 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | det | sacrum_detector 0.857 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -2.7851, 'L6': -0.755} | L6 (2.0301, 2.0301, 1.7236) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | det74 | sacrum_detector 0.857 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -2.7851, 'L6': -0.755} | L6 (2.0301, 2.0301, 1.6524) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -4.6364, 'T13': -4.8825, 'L6': -2.0631} | L6 (2.5733, 2.5733, 0.5456) | L1 L2 L3 L4 L5 L6 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | yes | no | disagreement |
| case121 AP | k5 | det | sacrum_detector 0.362 | L1 L2 L3 L4 | - 1 2 3 | - L5 L4 L3 | {'ordinary': -4.556, 'L6': -6.2932} | ordinary (0.0, 1.7372, 1.9481) | L1 L5 L4 L3 | None None None None | None None None None | no | no | disagreement |
| case121 AP | k5 | det | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.9481) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | k5 | det74 | none (rejected 0.362) | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 | None None None None | None None None None | no | no | no_anchor |
| case121 AP | k5 | det74 | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | k5 | oracle | none | T12 L1 L2 L3 L4 | - - - - - | - - - - - | {} | no anchor (None, None, 0.291) | T12 L1 L2 L3 L4 | None None None None None | None None None None None | no | no | no_anchor |
| case121 AP | k5 | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.4267, 'T13': -3.6915, 'L6': -3.2282} | L6 (0.1985, 0.1985, 0.291) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case121 AP | kfull | det | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.6117) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | kfull | det74 | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.6) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | kfull | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.0876, 'T13': -3.3597, 'L6': -3.0218} | L6 (0.0658, 0.0658, 0.5312) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case121 LAT | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.9481) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.1664, 'L6': -4.2216} | ordinary (0.0, 3.0552, 0.291) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case121 LAT | kfull | det | sacrum_detector 0.569 | L2 L3 L4 L5 | 4 3 2 1 | L2 L3 L4 L5 | {'ordinary': -1.0162, 'L6': -2.8747} | ordinary (0.0, 1.8585, 1.6117) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | quiet |
| case121 LAT | kfull | det74 | none (rejected 0.569) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.6) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.9793, 'L6': -3.7549} | ordinary (0.0, 2.7756, 0.5312) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case136 AP | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 2.1105) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 AP | k5 | det | sacrum_detector 0.375 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.8436, 'L6': -2.4155} | ordinary (0.0, 0.5719, 2.1105) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 AP | k5 | det74 | none (rejected 0.375) | L2 L3 L4 L5 sacrum | - - - - - | - - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 sacrum | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case136 AP | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.6105) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case136 AP | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -4.0447, 'T13': -3.9828, 'L6': -3.5047} | L6 (0.5399, 0.4781, 0.6105) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | det | sacrum_detector 0.835 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.7722, 'L6': -2.7854} | ordinary (0.0, 1.0133, 2.3011) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | det74 | sacrum_detector 0.835 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.7722, 'L6': -2.7854} | ordinary (0.0, 1.0133, 2.2842) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -4.0836, 'T13': -4.0456, 'L6': -3.3977} | L6 (0.6859, 0.6479, 0.5481) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case136 LAT | k5 | det | sacrum_detector 0.477 | L2 L3 L4 L5 | 2 1 - - | L4 L5 - - | {'ordinary': -10.7017, 'L6': -10.4451} | L6 (0.2567, 0.2567, 2.1105) | L5 L6 L4 L5 | None None None None | None None None None | no | no | disagreement |
| case136 LAT | k5 | det | sacrum_detector 0.672 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.816, 'L6': -2.1992} | ordinary (0.0, 1.3832, 2.1105) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | k5 | det74 | none (rejected 0.477) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 LAT | k5 | det74 | none (rejected 0.672) | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case136 LAT | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.6105) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case136 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -2.4532, 'T13': -3.303, 'L6': -2.4237} | L6 (0.0296, 0.0296, 0.6105) | L2 L1 L3 L4 L5 L6 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 LAT | kfull | det | sacrum_detector 0.79 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.9461, 'L6': -2.2537} | ordinary (0.0, 1.3076, 2.3011) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | kfull | det74 | sacrum_detector 0.79 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.9461, 'L6': -2.2537} | ordinary (0.0, 1.3076, 2.2842) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 5 6 4 3 2 1 | L1 T12 L2 L3 L4 L5 | {'ordinary': -2.5955, 'T13': -3.3558, 'L6': -2.4326} | L6 (0.1629, 0.1629, 0.5481) | L2 L1 L3 L4 L5 L6 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | no | no | disagreement |

- **det, whole frames with an anchor: 5 of 6**; coupled names equal VERIDAH's on 1, TotalSegmentator's on 4; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 3; calls {'ordinary': 4, 'L6': 1}; flagged 4 ({'low_margin': 2, 'disagreement': 2}).
- **det74, whole frames with an anchor: 4 of 6**; coupled names equal VERIDAH's on 1, TotalSegmentator's on 3; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 2; calls {'ordinary': 3, 'L6': 1}; flagged 4 ({'low_margin': 2, 'disagreement': 2}).
- **oracle, whole frames with an anchor: 6 of 6**; coupled names equal VERIDAH's on 2, TotalSegmentator's on 1; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 1; calls {'L6': 5, 'ordinary': 1}; flagged 5 ({'disagreement': 5}).

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
