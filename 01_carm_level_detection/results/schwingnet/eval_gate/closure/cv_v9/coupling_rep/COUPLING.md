# Coupling the morphology classifier to the count from the sacrum: C-ArmLSpine folds and the anomalous renders

Generated 2026-09-24 09:08. Numbers: `SchwingNet/results/coupling.json` (this file quotes it; every table cell is a key there). Tools: `tools/alphabet_couple.py` (the coupler; `--self-test` passes on synthetic posteriors: ordinary, L6 with the sixth body called L5, the same upside down and scrambled, one confident error, no sacrum, the sacrum boxed as a vertebra, variant truth, the confidence floor and the named-sacrum switch), `tools/level_prototype.py --dump-posterior --sacrum-detector`, `SchwingNet/tools/coupling_report.py`, `SchwingNet/tools/sweep_variant_calls.py`; jobs `SchwingNet/slurm/coupling.sh` (GPU array, one fold per task) then `SchwingNet/slurm/coupling_eval.sh` (CPU). Jobs: carmcv9i 40431706 carmcvday9i 40431707 prerep 40436575 carmcv9pre 40436580.

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

Per-frame coupler outputs (every ordinal, candidate score and name): `/rs/rs_grp_oschome/go2432/data/carmlspine/proto_post_v9init/cv_fold<K>/<det|oracle>/k<full|5>/<couple|couple_c74|couple_ns|couple_ext>/couple_all.json` and one `<stem>.couple.json` per frame; prototype JSONs with the 27-vectors beside them. Shipped CV outputs the classifier numbers are checked against: `/rs/rs_grp_oschome/go2432/data/carmlspine/proto_v9init/cv_fold<K>/<arm>_score_k<k>.json`.

## The classifier did not move

`--dump-posterior` and `--sacrum-detector` add fields; they must change no name. Exact-level accuracy of the re-run against the shipped CV output, per fold:

| cell | shipped (scored, exact) | re-run (scored, exact) | identical |
|---|---|---|---|
| cv_fold0/det/kfull | 291, 0.9278 | 291, 0.9278 | yes |
| cv_fold0/det/k5 | 274, 0.9161 | 274, 0.9161 | yes |
| cv_fold0/oracle/kfull | 311, 0.9293 | 311, 0.9293 | yes |
| cv_fold0/oracle/k5 | 299, 0.9532 | 299, 0.9532 | yes |
| cv_fold1/det/kfull | 206, 0.9903 | 206, 0.9903 | yes |
| cv_fold1/det/k5 | 234, 0.9444 | 234, 0.9444 | yes |
| cv_fold1/oracle/kfull | 216, 0.9676 | 216, 0.9676 | yes |
| cv_fold1/oracle/k5 | 250, 0.984 | 250, 0.984 | yes |
| cv_fold2/det/kfull | 228, 0.9693 | 228, 0.9693 | yes |
| cv_fold2/det/k5 | 276, 0.9565 | 276, 0.9565 | yes |
| cv_fold2/oracle/kfull | 256, 0.9609 | 256, 0.9609 | yes |
| cv_fold2/oracle/k5 | 309, 0.9288 | 309, 0.9288 | yes |
| cv_fold3/det/kfull | 308, 0.9838 | 308, 0.9838 | yes |
| cv_fold3/det/k5 | 329, 0.9149 | 329, 0.9149 | yes |
| cv_fold3/oracle/kfull | 327, 0.9388 | 327, 0.9388 | yes |
| cv_fold3/oracle/k5 | 363, 0.8981 | 363, 0.8981 | yes |
| cv_fold4/det/kfull | 223, 0.9821 | 223, 0.9821 | yes |
| cv_fold4/det/k5 | 254, 0.9488 | 254, 0.9488 | yes |
| cv_fold4/oracle/kfull | 232, 0.9871 | 232, 0.9871 | yes |
| cv_fold4/oracle/k5 | 270, 0.9296 | 270, 0.9296 | yes |

## The thresholds (chosen on the other four folds, applied to the fifth)

| variant / field / fold | tau on margin_next | frames it was chosen on |
|---|---|---|
| det/kfull/fold0 | 1.588 | 196 |
| det/kfull/fold1 | 1.5792 | 211 |
| det/kfull/fold2 | 1.8403 | 202 |
| det/kfull/fold3 | 2.0784 | 188 |
| det/kfull/fold4 | 2.043 | 207 |
| det/k5/fold0 | 1.3832 | 106 |
| det/k5/fold1 | 1.287 | 111 |
| det/k5/fold2 | 1.4103 | 113 |
| det/k5/fold3 | 1.3599 | 103 |
| det/k5/fold4 | 1.2982 | 111 |
| det74/kfull/fold0 | 1.5874 | 177 |
| det74/kfull/fold1 | 1.5687 | 189 |
| det74/kfull/fold2 | 1.583 | 179 |
| det74/kfull/fold3 | 2.0763 | 167 |
| det74/kfull/fold4 | 2.0701 | 184 |
| det74/k5/fold0 | none (too few frames) | 5 |
| det74/k5/fold1 | none (too few frames) | 5 |
| det74/k5/fold2 | none (too few frames) | 6 |
| det74/k5/fold3 | none (too few frames) | 3 |
| det74/k5/fold4 | none (too few frames) | 5 |
| oracle/kfull/fold0 | 0.359 | 195 |
| oracle/kfull/fold1 | 0.3613 | 213 |
| oracle/kfull/fold2 | 0.3499 | 208 |
| oracle/kfull/fold3 | 0.3542 | 191 |
| oracle/kfull/fold4 | 0.3642 | 209 |
| oracle/k5/fold0 | 0.2275 | 36 |
| oracle/k5/fold1 | 0.1411 | 39 |
| oracle/k5/fold2 | 0.1498 | 34 |
| oracle/k5/fold3 | 0.1411 | 39 |
| oracle/k5/fold4 | 0.1211 | 36 |
| det_ns/kfull/fold0 | 1.9608 | 195 |
| det_ns/kfull/fold1 | 1.9237 | 211 |
| det_ns/kfull/fold2 | 2.0719 | 202 |
| det_ns/kfull/fold3 | 2.1473 | 188 |
| det_ns/kfull/fold4 | 2.1473 | 208 |
| det_ns/k5/fold0 | 1.5807 | 104 |
| det_ns/k5/fold1 | 1.594 | 108 |
| det_ns/k5/fold2 | 1.9793 | 110 |
| det_ns/k5/fold3 | 1.4876 | 102 |
| det_ns/k5/fold4 | 1.9504 | 108 |
| oracle_ns/kfull/fold0 | 0.3587 | 194 |
| oracle_ns/kfull/fold1 | 0.3613 | 212 |
| oracle_ns/kfull/fold2 | 0.3495 | 207 |
| oracle_ns/kfull/fold3 | 0.3542 | 191 |
| oracle_ns/kfull/fold4 | 0.3638 | 208 |
| oracle_ns/k5/fold0 | 0.2263 | 34 |
| oracle_ns/k5/fold1 | 0.1278 | 37 |
| oracle_ns/k5/fold2 | 0.13 | 32 |
| oracle_ns/k5/fold3 | 0.1344 | 38 |
| oracle_ns/k5/fold4 | 0.1144 | 35 |
| det_ext/kfull/fold0 | 1.3945 | 198 |
| det_ext/kfull/fold1 | 1.2503 | 213 |
| det_ext/kfull/fold2 | 1.1576 | 204 |
| det_ext/kfull/fold3 | 1.3661 | 191 |
| det_ext/kfull/fold4 | 1.2893 | 210 |
| det_ext/k5/fold0 | 1.2789 | 109 |
| det_ext/k5/fold1 | 1.1728 | 114 |
| det_ext/k5/fold2 | 1.3572 | 114 |
| det_ext/k5/fold3 | 1.2668 | 106 |
| det_ext/k5/fold4 | 1.1659 | 113 |
| oracle_ext/kfull/fold0 | 0.3581 | 192 |
| oracle_ext/kfull/fold1 | 0.3571 | 209 |
| oracle_ext/kfull/fold2 | 0.3354 | 204 |
| oracle_ext/kfull/fold3 | 0.3375 | 187 |
| oracle_ext/kfull/fold4 | 0.3555 | 204 |
| oracle_ext/k5/fold0 | 0.2269 | 35 |
| oracle_ext/k5/fold1 | 0.1344 | 38 |
| oracle_ext/k5/fold2 | 0.1399 | 33 |
| oracle_ext/k5/fold3 | 0.1411 | 39 |
| oracle_ext/k5/fold4 | 0.1144 | 35 |

## C-ArmLSpine, five test folds pooled (truth = the two CBCT labellers agree)

k = full is the whole frame; k = 5 a crop holding five truth vertebrae (the sacrum is in the crop only when its centre falls inside). Bodies are scored where a call matches a truth body with an agreed level; a det frame with no detected sacrum is `no anchor` (names unchanged, flagged).

| cell | quantity | value [95 % CI, case bootstrap] (k/n) |
|---|---|---|
| det/kfull | frames | 289 (145 cases); anchored 265; truth sacrum in frame 285; anchored without a truth sacrum 0; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1217/1256) |
| det/kfull | (ii) coupled names, all scored bodies | 96.4 % [94.3, 98.3] (1211/1256); paired difference -0.5 pp [-2.2, +1.4] |
| det/kfull | (iii) coupled names, anchored frames only | 97.2 % [95.5, 98.8] (1127/1159); classifier on the same bodies 97.8 % [95.9, 99.2] (1133/1159); paired difference -0.5 pp [-2.4, +1.5] |
| det/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 96.1 % [93.5, 98.3] (1111/1156); coupled on the same bodies 97.2 % [95.5, 98.8] (1124/1156); classifier 97.8 % [95.9, 99.2] (1130/1156); coupled minus count +1.1 pp [-0.1, +3.0] |
| det/kfull | classifier on un-anchored frames | 86.6 % [71.8, 100.0] (84/97) |
| det/kfull | frame-exact (every scored body right), anchored frames | classifier 97.0 % [94.7, 98.9] (254/262); coupled 95.8 % [93.4, 98.1] (251/262) |
| det/kfull | disagreement | bodies 4.6 % [2.6, 6.9] (56/1209); frames with any 6.8 % [3.7, 10.2] (18/265) |
| det/kfull | accuracy when the two agree | coupled = classifier 99.6 % [98.9, 100.0] (1108/1113) |
| det/kfull | accuracy when they disagree | coupled 37.2 % [9.8, 65.3] (16/43); classifier 51.2 % [22.7, 79.6] (22/43); neither 5 of 43 |
| det/kfull | the count vs the classifier (counted bodies with truth, n = 1156) | corrects a classifier error 16 of 26; introduces an error 22 of 1130 classifier-correct bodies; both wrong 10 |
| det/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 19.0 % [13.8, 24.5] (55/289) of all frames, 11.7 % [7.5, 16.3] (31/265) of anchored; reasons {'no_anchor': 21, 'disagreement': 18, 'no_vertebra': 3, 'low_margin': 13} |
| det/kfull | stop signal on anchored frames with truth | fires on 90.9 % [72.7, 100.0] (10/11) of frames with a coupled error; on 7.6 % [4.0, 11.6] (19/251) of fully correct frames; coupled accuracy unflagged 99.9 % [99.7, 100.0] (1039/1040) vs flagged 74.0 % [58.3, 87.2] (88/119) |
| det/kfull | variant calls (anchored frames) | {'ordinary': 260, 'L6': 5}; on the non-ordinary calls: coupled 68.2 % [22.2, 100.0] (15/22), classifier 81.8 % [29.4, 100.0] (18/22), count 4.8 % [0.0, 18.8] (1/21); 5 of 5 flagged; cases ['case139', 'case19', 'case44', 'case9'] |
| det/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 5 / 0 |
| det/k5 | frames | 321 (135 cases); anchored 159; truth sacrum in frame 52; anchored without a truth sacrum 129; truth sacrum but no anchor 22; anchor rejected by the confidence floor 0 |
| det/k5 | (i) classifier alone, all scored bodies | 93.5 % [89.5, 97.1] (1278/1367) |
| det/k5 | (ii) coupled names, all scored bodies | 91.1 % [86.8, 94.9] (1245/1367); paired difference -2.4 pp [-4.3, -0.5] |
| det/k5 | (iii) coupled names, anchored frames only | 92.2 % [88.5, 95.2] (652/707); classifier on the same bodies 96.9 % [93.6, 99.5] (685/707); paired difference -4.7 pp [-8.3, -1.1] |
| det/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.8 % [83.9, 92.8] (603/679); coupled on the same bodies 92.2 % [88.4, 95.1] (626/679); classifier 97.0 % [93.9, 99.4] (659/679); coupled minus count +3.4 pp [+0.9, +6.7] |
| det/k5 | classifier on un-anchored frames | 89.8 % [83.0, 95.9] (593/660) |
| det/k5 | frame-exact (every scored body right), anchored frames | classifier 96.2 % [92.4, 99.4] (153/159); coupled 85.5 % [79.8, 90.5] (136/159) |
| det/k5 | disagreement | bodies 11.4 % [7.3, 16.2] (81/710); frames with any 19.5 % [13.4, 26.5] (31/159) |
| det/k5 | accuracy when the two agree | coupled = classifier 100.0 % [100.0, 100.0] (612/612) |
| det/k5 | accuracy when they disagree | coupled 20.9 % [0.0, 40.5] (14/67); classifier 70.2 % [50.0, 91.7] (47/67); neither 6 of 67 |
| det/k5 | the count vs the classifier (counted bodies with truth, n = 679) | corrects a classifier error 14 of 20; introduces an error 47 of 659 classifier-correct bodies; both wrong 6 |
| det/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 61.1 % [54.5, 67.2] (196/321) of all frames, 21.4 % [15.0, 28.5] (34/159) of anchored; reasons {'no_anchor': 161, 'disagreement': 31, 'low_margin': 3, 'no_vertebra': 1} |
| det/k5 | stop signal on anchored frames with truth | fires on 100.0 % [100.0, 100.0] (23/23) of frames with a coupled error; on 8.1 % [4.2, 13.0] (11/136) of fully correct frames; coupled accuracy unflagged 100.0 % [100.0, 100.0] (570/570) vs flagged 59.9 % [47.4, 71.3] (82/137) |
| det/k5 | variant calls (anchored frames) | {'ordinary': 149, 'L6': 10}; on the non-ordinary calls: coupled 73.0 % [51.2, 90.0] (27/37), classifier 100.0 % [100.0, 100.0] (37/37), count 2.9 % [0.0, 10.3] (1/34); 10 of 10 flagged; cases ['case138', 'case38', 'case4', 'case44', 'case5', 'case53', 'case63', 'case66', 'case88'] |
| det/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 9 / 0 |
| det74/kfull | frames | 289 (145 cases); anchored 233; truth sacrum in frame 285; anchored without a truth sacrum 0; truth sacrum but no anchor 52; anchor rejected by the confidence floor 33 |
| det74/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1217/1256) |
| det74/kfull | (ii) coupled names, all scored bodies | 97.3 % [95.4, 99.0] (1222/1256); paired difference +0.4 pp [-1.1, +1.9] |
| det74/kfull | (iii) coupled names, anchored frames only | 98.3 % [96.7, 99.5] (999/1016); classifier on the same bodies 97.8 % [96.1, 99.2] (994/1016); paired difference +0.5 pp [-1.5, +2.4] |
| det74/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.0 % [94.1, 99.2] (986/1016); coupled on the same bodies 98.3 % [96.7, 99.5] (999/1016); classifier 97.8 % [96.1, 99.2] (994/1016); coupled minus count +1.3 pp [+0.0, +3.4] |
| det74/kfull | classifier on un-anchored frames | 92.9 % [85.8, 98.4] (223/240) |
| det74/kfull | frame-exact (every scored body right), anchored frames | classifier 97.0 % [94.7, 98.7] (223/230); coupled 97.4 % [95.2, 99.2] (224/230) |
| det74/kfull | disagreement | bodies 3.9 % [1.8, 6.5] (42/1066); frames with any 5.6 % [2.6, 9.2] (13/233) |
| det74/kfull | accuracy when the two agree | coupled = classifier 99.6 % [98.8, 100.0] (983/987) |
| det74/kfull | accuracy when they disagree | coupled 55.2 % [15.4, 87.5] (16/29); classifier 37.9 % [9.7, 74.2] (11/29); neither 2 of 29 |
| det74/kfull | the count vs the classifier (counted bodies with truth, n = 1016) | corrects a classifier error 16 of 22; introduces an error 11 of 994 classifier-correct bodies; both wrong 6 |
| det74/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 27.3 % [21.4, 33.6] (79/289) of all frames, 9.9 % [5.7, 14.5] (23/233) of anchored; reasons {'no_anchor': 53, 'disagreement': 13, 'no_vertebra': 3, 'low_margin': 10} |
| det74/kfull | stop signal on anchored frames with truth | fires on 83.3 % [50.0, 100.0] (5/6) of frames with a coupled error; on 7.1 % [3.5, 11.5] (16/224) of fully correct frames; coupled accuracy unflagged 99.9 % [99.7, 100.0] (928/929) vs flagged 81.6 % [63.7, 95.3] (71/87) |
| det74/kfull | variant calls (anchored frames) | {'ordinary': 230, 'L6': 3}; on the non-ordinary calls: coupled 100.0 % [100.0, 100.0] (13/13), classifier 100.0 % [100.0, 100.0] (13/13), count 0.0 % [0.0, 0.0] (0/13); 3 of 3 flagged; cases ['case139', 'case44'] |
| det74/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 5 / 0 |
| det74/k5 | frames | 321 (135 cases); anchored 6; truth sacrum in frame 52; anchored without a truth sacrum 4; truth sacrum but no anchor 50; anchor rejected by the confidence floor 154 |
| det74/k5 | (i) classifier alone, all scored bodies | 93.5 % [89.5, 97.1] (1278/1367) |
| det74/k5 | (ii) coupled names, all scored bodies | 93.5 % [89.5, 97.1] (1278/1367); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iii) coupled names, anchored frames only | 100.0 % [100.0, 100.0] (26/26); classifier on the same bodies 100.0 % [100.0, 100.0] (26/26); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.5 % [59.1, 100.0] (23/26); coupled on the same bodies 100.0 % [100.0, 100.0] (26/26); classifier 100.0 % [100.0, 100.0] (26/26); coupled minus count +11.5 pp [+0.0, +40.9] |
| det74/k5 | classifier on un-anchored frames | 93.4 % [89.1, 97.0] (1252/1341) |
| det74/k5 | frame-exact (every scored body right), anchored frames | classifier 100.0 % [100.0, 100.0] (6/6); coupled 100.0 % [100.0, 100.0] (6/6) |
| det74/k5 | disagreement | bodies 3.6 % [0.0, 10.7] (1/28); frames with any 16.7 % [0.0, 50.0] (1/6) |
| det74/k5 | accuracy when the two agree | coupled = classifier 100.0 % [100.0, 100.0] (26/26) |
| det74/k5 | accuracy when they disagree | coupled n/a; classifier n/a; neither 0 of 0 |
| det74/k5 | the count vs the classifier (counted bodies with truth, n = 26) | corrects a classifier error 0 of 0; introduces an error 0 of 26 classifier-correct bodies; both wrong 0 |
| det74/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 98.4 % [96.9, 99.7] (316/321) of all frames, 16.7 % [0.0, 50.0] (1/6) of anchored; reasons {'no_anchor': 314, 'disagreement': 1, 'no_vertebra': 1} |
| det74/k5 | stop signal on anchored frames with truth | fires on n/a of frames with a coupled error; on 16.7 % [0.0, 50.0] (1/6) of fully correct frames; coupled accuracy unflagged 100.0 % [100.0, 100.0] (23/23) vs flagged 100.0 % (3/3) |
| det74/k5 | variant calls (anchored frames) | {'L6': 1, 'ordinary': 5}; on the non-ordinary calls: coupled 100.0 % (3/3), classifier 100.0 % (3/3), count 0.0 % (0/3); 1 of 1 flagged; cases ['case138'] |
| det74/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 1 / 0 |
| oracle/kfull | frames | 289 (145 cases); anchored 285; truth sacrum in frame 285; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle/kfull | (i) classifier alone, all scored bodies | 95.4 % [92.8, 97.4] (1280/1342) |
| oracle/kfull | (ii) coupled names, all scored bodies | 96.8 % [95.2, 98.2] (1299/1342); paired difference +1.4 pp [-0.7, +3.9] |
| oracle/kfull | (iii) coupled names, anchored frames only | 97.1 % [95.7, 98.4] (1284/1322); classifier on the same bodies 95.7 % [93.5, 97.7] (1265/1322); paired difference +1.4 pp [-0.8, +3.8] |
| oracle/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 98.2 % [97.3, 99.0] (1298/1322); coupled on the same bodies 97.1 % [95.7, 98.4] (1284/1322); classifier 95.7 % [93.5, 97.7] (1265/1322); coupled minus count -1.1 pp [-2.3, +0.0] |
| oracle/kfull | classifier on un-anchored frames | 75.0 % [50.0, 100.0] (15/20) |
| oracle/kfull | frame-exact (every scored body right), anchored frames | classifier 89.7 % [85.4, 93.6] (252/281); coupled 90.4 % [86.2, 94.0] (254/281) |
| oracle/kfull | disagreement | bodies 6.3 % [3.8, 8.9] (91/1448); frames with any 11.2 % [7.1, 15.4] (32/285) |
| oracle/kfull | accuracy when the two agree | coupled = classifier 98.7 % [97.7, 99.4] (1245/1262) |
| oracle/kfull | accuracy when they disagree | coupled 65.0 % [40.9, 84.4] (39/60); classifier 33.3 % [13.8, 57.8] (20/60); neither 1 of 60 |
| oracle/kfull | the count vs the classifier (counted bodies with truth, n = 1322) | corrects a classifier error 39 of 57; introduces an error 20 of 1265 classifier-correct bodies; both wrong 18 |
| oracle/kfull | stop signal (no anchor, any disagreement, or margin below tau) | flagged 16.3 % [11.5, 21.2] (47/289) of all frames, 15.1 % [10.8, 19.7] (43/285) of anchored; reasons {'no_anchor': 4, 'disagreement': 32, 'low_margin': 11} |
| oracle/kfull | stop signal on anchored frames with truth | fires on 55.6 % [34.6, 76.0] (15/27) of frames with a coupled error; on 10.2 % [6.5, 14.4] (26/254) of fully correct frames; coupled accuracy unflagged 98.9 % [98.2, 99.6] (1121/1133) vs flagged 86.2 % [76.8, 93.2] (163/189) |
| oracle/kfull | variant calls (anchored frames) | {'ordinary': 281, 'L6': 3, 'T13': 1}; on the non-ordinary calls: coupled 26.3 % [0.0, 75.0] (5/19), classifier 79.0 % [29.4, 100.0] (15/19), count 100.0 % [100.0, 100.0] (19/19); 4 of 4 flagged; cases ['case132', 'case19', 'case54', 'case9'] |
| oracle/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 3 / 0 |
| oracle/k5 | frames | 321 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle/k5 | (i) classifier alone, all scored bodies | 93.6 % [90.6, 96.1] (1395/1491) |
| oracle/k5 | (ii) coupled names, all scored bodies | 94.0 % [91.1, 96.5] (1402/1491); paired difference +0.5 pp [-0.8, +2.0] |
| oracle/k5 | (iii) coupled names, anchored frames only | 94.9 % [89.4, 99.2] (244/257); classifier on the same bodies 92.2 % [85.0, 98.1] (237/257); paired difference +2.7 pp [-5.2, +10.8] |
| oracle/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 98.4 % [96.3, 100.0] (253/257); coupled on the same bodies 94.9 % [89.4, 99.2] (244/257); classifier 92.2 % [85.0, 98.1] (237/257); coupled minus count -3.5 pp [-8.9, +0.0] |
| oracle/k5 | classifier on un-anchored frames | 93.8 % [90.6, 96.5] (1158/1234) |
| oracle/k5 | frame-exact (every scored body right), anchored frames | classifier 90.4 % [82.0, 96.5] (47/52); coupled 88.5 % [76.9, 96.4] (46/52) |
| oracle/k5 | disagreement | bodies 10.2 % [3.6, 18.0] (29/283); frames with any 15.4 % [5.9, 26.9] (8/52) |
| oracle/k5 | accuracy when the two agree | coupled = classifier 97.9 % [94.0, 100.0] (229/234) |
| oracle/k5 | accuracy when they disagree | coupled 65.2 % [19.2, 96.3] (15/23); classifier 34.8 % [3.7, 80.8] (8/23); neither 0 of 23 |
| oracle/k5 | the count vs the classifier (counted bodies with truth, n = 257) | corrects a classifier error 15 of 20; introduces an error 8 of 237 classifier-correct bodies; both wrong 5 |
| oracle/k5 | stop signal (no anchor, any disagreement, or margin below tau) | flagged 86.9 % [82.4, 91.1] (279/321) of all frames, 19.2 % [7.8, 32.2] (10/52) of anchored; reasons {'no_anchor': 269, 'disagreement': 8, 'low_margin': 2} |
| oracle/k5 | stop signal on anchored frames with truth | fires on 83.3 % [40.0, 100.0] (5/6) of frames with a coupled error; on 10.9 % [2.1, 22.2] (5/46) of fully correct frames; coupled accuracy unflagged 99.5 % [98.4, 100.0] (207/208) vs flagged 75.5 % [47.6, 95.5] (37/49) |
| oracle/k5 | variant calls (anchored frames) | {'ordinary': 50, 'L6': 2}; on the non-ordinary calls: coupled 0.0 % [0.0, 0.0] (0/9), classifier 55.6 % [0.0, 100.0] (5/9), count 100.0 % [100.0, 100.0] (9/9); 2 of 2 flagged; cases ['case132', 'case54'] |
| oracle/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 3 / 0 |

### Sensitivity variants (same folds; only the rows that change)

| cell | quantity | value |
|---|---|---|
| det_ns/kfull | frames | 289 (145 cases); anchored 265; truth sacrum in frame 285; anchored without a truth sacrum 0; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det_ns/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1217/1256) |
| det_ns/kfull | (ii) coupled names, all scored bodies | 96.4 % [94.3, 98.2] (1211/1256); paired difference -0.5 pp [-2.1, +1.1] |
| det_ns/kfull | (iii) coupled names, anchored frames only | 97.2 % [95.5, 98.9] (1127/1159); classifier on the same bodies 97.8 % [95.9, 99.2] (1133/1159); paired difference -0.5 pp [-2.2, +1.3] |
| det_ns/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.2 % [95.5, 98.8] (1124/1156); coupled on the same bodies 97.2 % [95.5, 98.9] (1124/1156); classifier 97.8 % [95.9, 99.2] (1130/1156); coupled minus count +0.0 pp [-0.3, +0.3] |
| det_ns/kfull | the count vs the classifier (counted bodies with truth, n = 1156) | corrects a classifier error 12 of 26; introduces an error 18 of 1130 classifier-correct bodies; both wrong 14 |
| det_ns/kfull | variant calls (anchored frames) | {'ordinary': 263, 'L6': 2}; on the non-ordinary calls: coupled 22.2 % [0.0, 40.0] (2/9), classifier 55.6 % [0.0, 100.0] (5/9), count 12.5 % [0.0, 25.0] (1/8); 2 of 2 flagged; cases ['case19', 'case9'] |
| det_ns/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 6 |
| det_ns/k5 | frames | 321 (135 cases); anchored 159; truth sacrum in frame 52; anchored without a truth sacrum 129; truth sacrum but no anchor 22; anchor rejected by the confidence floor 0 |
| det_ns/k5 | (i) classifier alone, all scored bodies | 93.5 % [89.5, 97.1] (1278/1367) |
| det_ns/k5 | (ii) coupled names, all scored bodies | 90.0 % [85.9, 94.0] (1231/1367); paired difference -3.4 pp [-5.0, -2.0] |
| det_ns/k5 | (iii) coupled names, anchored frames only | 90.2 % [86.0, 94.0] (638/707); classifier on the same bodies 96.9 % [93.6, 99.5] (685/707); paired difference -6.7 pp [-9.5, -4.2] |
| det_ns/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 90.1 % [85.8, 93.9] (610/677); coupled on the same bodies 90.4 % [86.2, 94.1] (612/677); classifier 97.3 % [94.5, 99.5] (659/677); coupled minus count +0.3 pp [-0.3, +0.9] |
| det_ns/k5 | the count vs the classifier (counted bodies with truth, n = 677) | corrects a classifier error 0 of 18; introduces an error 47 of 659 classifier-correct bodies; both wrong 18 |
| det_ns/k5 | variant calls (anchored frames) | {'ordinary': 154, 'L6': 5}; on the non-ordinary calls: coupled 37.5 % [25.0, 47.4] (6/16), classifier 100.0 % [100.0, 100.0] (16/16), count 7.7 % [0.0, 20.0] (1/13); 5 of 5 flagged; cases ['case38', 'case44', 'case5', 'case66', 'case88'] |
| det_ns/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 11 |
| oracle_ns/kfull | frames | 289 (145 cases); anchored 285; truth sacrum in frame 285; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ns/kfull | (i) classifier alone, all scored bodies | 95.4 % [92.8, 97.4] (1280/1342) |
| oracle_ns/kfull | (ii) coupled names, all scored bodies | 96.2 % [94.2, 97.9] (1291/1342); paired difference +0.8 pp [-1.1, +3.1] |
| oracle_ns/kfull | (iii) coupled names, anchored frames only | 96.5 % [94.8, 98.1] (1276/1322); classifier on the same bodies 95.7 % [93.5, 97.7] (1265/1322); paired difference +0.8 pp [-1.1, +3.0] |
| oracle_ns/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 97.4 % [96.1, 98.6] (1286/1320); coupled on the same bodies 96.7 % [95.0, 98.1] (1276/1320); classifier 95.8 % [93.7, 97.7] (1265/1320); coupled minus count -0.8 pp [-1.9, +0.0] |
| oracle_ns/kfull | the count vs the classifier (counted bodies with truth, n = 1320) | corrects a classifier error 31 of 55; introduces an error 20 of 1265 classifier-correct bodies; both wrong 24 |
| oracle_ns/kfull | variant calls (anchored frames) | {'ordinary': 282, 'T13': 1, 'L6': 2}; on the non-ordinary calls: coupled 33.3 % [0.0, 100.0] (5/15), classifier 100.0 % [100.0, 100.0] (15/15), count 100.0 % [100.0, 100.0] (15/15); 3 of 3 flagged; cases ['case132', 'case19', 'case9'] |
| oracle_ns/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 3 |
| oracle_ns/k5 | frames | 321 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ns/k5 | (i) classifier alone, all scored bodies | 93.6 % [90.6, 96.1] (1395/1491) |
| oracle_ns/k5 | (ii) coupled names, all scored bodies | 93.4 % [90.5, 96.0] (1393/1491); paired difference -0.1 pp [-1.2, +1.0] |
| oracle_ns/k5 | (iii) coupled names, anchored frames only | 91.4 % [84.3, 97.3] (235/257); classifier on the same bodies 92.2 % [85.0, 98.1] (237/257); paired difference -0.8 pp [-6.9, +5.8] |
| oracle_ns/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 93.8 % [87.9, 98.5] (240/256); coupled on the same bodies 91.8 % [85.0, 97.4] (235/256); classifier 92.6 % [85.7, 98.3] (237/256); coupled minus count -1.9 pp [-6.1, +0.0] |
| oracle_ns/k5 | the count vs the classifier (counted bodies with truth, n = 256) | corrects a classifier error 6 of 19; introduces an error 8 of 237 classifier-correct bodies; both wrong 13 |
| oracle_ns/k5 | variant calls (anchored frames) | {'ordinary': 51, 'L6': 1}; on the non-ordinary calls: coupled 0.0 % (0/5), classifier 100.0 % (5/5), count 100.0 % (5/5); 1 of 1 flagged; cases ['case132'] |
| oracle_ns/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 0 / 3 |
| det_ext/kfull | frames | 289 (145 cases); anchored 265; truth sacrum in frame 285; anchored without a truth sacrum 0; truth sacrum but no anchor 20; anchor rejected by the confidence floor 0 |
| det_ext/kfull | (i) classifier alone, all scored bodies | 96.9 % [94.6, 98.7] (1217/1256) |
| det_ext/kfull | (ii) coupled names, all scored bodies | 97.0 % [94.7, 98.9] (1218/1256); paired difference +0.1 pp [-1.1, +1.4] |
| det_ext/kfull | (iii) coupled names, anchored frames only | 97.8 % [96.1, 99.2] (1134/1159); classifier on the same bodies 97.8 % [95.9, 99.2] (1133/1159); paired difference +0.1 pp [-1.2, +1.6] |
| det_ext/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 96.1 % [93.5, 98.3] (1111/1156); coupled on the same bodies 97.8 % [96.1, 99.2] (1131/1156); classifier 97.8 % [95.9, 99.2] (1130/1156); coupled minus count +1.7 pp [-0.4, +4.0] |
| det_ext/kfull | the count vs the classifier (counted bodies with truth, n = 1156) | corrects a classifier error 10 of 26; introduces an error 9 of 1130 classifier-correct bodies; both wrong 16 |
| det_ext/kfull | variant calls (anchored frames) | {'ordinary': 250, 'L4': 11, 'L6': 4}; on the non-ordinary calls: coupled 65.3 % [37.7, 88.7] (32/49), classifier 71.4 % [41.5, 93.3] (35/49), count 19.6 % [0.0, 45.5] (9/46); 10 of 15 flagged; cases ['case129', 'case139', 'case146', 'case148', 'case17', 'case19', 'case34', 'case43', 'case44', 'case77', 'case8', 'case83', 'case84', 'case9'] |
| det_ext/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 5 / 0 |
| det_ext/k5 | frames | 321 (135 cases); anchored 159; truth sacrum in frame 52; anchored without a truth sacrum 129; truth sacrum but no anchor 22; anchor rejected by the confidence floor 0 |
| det_ext/k5 | (i) classifier alone, all scored bodies | 93.5 % [89.5, 97.1] (1278/1367) |
| det_ext/k5 | (ii) coupled names, all scored bodies | 92.0 % [87.8, 95.5] (1257/1367); paired difference -1.5 pp [-3.2, +0.1] |
| det_ext/k5 | (iii) coupled names, anchored frames only | 93.9 % [90.7, 96.6] (664/707); classifier on the same bodies 96.9 % [93.6, 99.5] (685/707); paired difference -3.0 pp [-6.3, +0.1] |
| det_ext/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.8 % [83.9, 92.8] (603/679); coupled on the same bodies 94.0 % [90.8, 96.5] (638/679); classifier 97.0 % [93.9, 99.4] (659/679); coupled minus count +5.1 pp [+2.1, +8.9] |
| det_ext/k5 | the count vs the classifier (counted bodies with truth, n = 679) | corrects a classifier error 14 of 20; introduces an error 35 of 659 classifier-correct bodies; both wrong 6 |
| det_ext/k5 | variant calls (anchored frames) | {'ordinary': 134, 'L6': 9, 'L4': 16}; on the non-ordinary calls: coupled 60.4 % [45.6, 74.3] (58/96), classifier 91.7 % [76.1, 100.0] (88/96), count 2.7 % [0.0, 7.0] (2/73); 19 of 25 flagged; cases ['case102', 'case103', 'case106', 'case107', 'case115', 'case133', 'case135', 'case138', 'case19', 'case38', 'case4', 'case44', 'case5', 'case53', 'case58', 'case6', 'case63', 'case66', 'case70', 'case73', 'case77', 'case88', 'case9'] |
| det_ext/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 9 / 0 |
| oracle_ext/kfull | frames | 289 (145 cases); anchored 285; truth sacrum in frame 285; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ext/kfull | (i) classifier alone, all scored bodies | 95.4 % [92.8, 97.4] (1280/1342) |
| oracle_ext/kfull | (ii) coupled names, all scored bodies | 95.2 % [92.8, 97.2] (1277/1342); paired difference -0.2 pp [-1.7, +1.3] |
| oracle_ext/kfull | (iii) coupled names, anchored frames only | 95.5 % [93.3, 97.3] (1262/1322); classifier on the same bodies 95.7 % [93.5, 97.7] (1265/1322); paired difference -0.2 pp [-1.7, +1.3] |
| oracle_ext/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 98.2 % [97.3, 99.0] (1298/1322); coupled on the same bodies 95.5 % [93.3, 97.3] (1262/1322); classifier 95.7 % [93.5, 97.7] (1265/1322); coupled minus count -2.7 pp [-4.9, -1.1] |
| oracle_ext/kfull | the count vs the classifier (counted bodies with truth, n = 1322) | corrects a classifier error 17 of 57; introduces an error 20 of 1265 classifier-correct bodies; both wrong 40 |
| oracle_ext/kfull | variant calls (anchored frames) | {'ordinary': 275, 'L4': 6, 'L6': 3, 'T13': 1}; on the non-ordinary calls: coupled 12.2 % [0.0, 39.5] (5/41), classifier 36.6 % [8.4, 71.4] (15/41), count 100.0 % [100.0, 100.0] (41/41); 7 of 10 flagged; cases ['case104', 'case132', 'case146', 'case148', 'case19', 'case54', 'case79', 'case83', 'case9'] |
| oracle_ext/kfull | bodies the classifier named 'sacrum' that were counted / excluded | 3 / 0 |
| oracle_ext/k5 | frames | 321 (135 cases); anchored 52; truth sacrum in frame 52; anchored without a truth sacrum 0; truth sacrum but no anchor 0; anchor rejected by the confidence floor 0 |
| oracle_ext/k5 | (i) classifier alone, all scored bodies | 93.6 % [90.6, 96.1] (1395/1491) |
| oracle_ext/k5 | (ii) coupled names, all scored bodies | 93.6 % [90.6, 96.3] (1396/1491); paired difference +0.1 pp [-0.9, +1.2] |
| oracle_ext/k5 | (iii) coupled names, anchored frames only | 92.6 % [85.8, 98.0] (238/257); classifier on the same bodies 92.2 % [85.0, 98.1] (237/257); paired difference +0.4 pp [-5.9, +7.5] |
| oracle_ext/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 98.4 % [96.3, 100.0] (253/257); coupled on the same bodies 92.6 % [85.8, 98.0] (238/257); classifier 92.2 % [85.0, 98.1] (237/257); coupled minus count -5.8 pp [-12.4, +0.0] |
| oracle_ext/k5 | the count vs the classifier (counted bodies with truth, n = 257) | corrects a classifier error 9 of 20; introduces an error 8 of 237 classifier-correct bodies; both wrong 11 |
| oracle_ext/k5 | variant calls (anchored frames) | {'ordinary': 49, 'L6': 2, 'L4': 1}; on the non-ordinary calls: coupled 0.0 % [0.0, 0.0] (0/15), classifier 33.3 % [0.0, 100.0] (5/15), count 100.0 % [100.0, 100.0] (15/15); 3 of 3 flagged; cases ['case118', 'case132', 'case54'] |
| oracle_ext/k5 | bodies the classifier named 'sacrum' that were counted / excluded | 3 / 0 |

### Same cells, with the three VERIDAH-L6 patients scored under their L6 truth

| cell | quantity | value |
|---|---|---|
| det/kfull | (i) classifier alone, all scored bodies | 95.4 % [92.6, 97.8] (1225/1284) |
| det/kfull | (ii) coupled names, all scored bodies | 94.7 % [91.6, 97.2] (1216/1284); paired difference -0.7 pp [-2.5, +1.2] |
| det/kfull | (iii) coupled names, anchored frames only | 95.7 % [93.1, 98.1] (1132/1183); classifier on the same bodies 96.5 % [94.1, 98.5] (1141/1183); paired difference -0.8 pp [-2.7, +1.3] |
| det/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 94.2 % [90.6, 97.4] (1111/1180); coupled on the same bodies 95.7 % [93.0, 98.1] (1129/1180); classifier 96.4 % [94.1, 98.5] (1138/1180); coupled minus count +1.5 pp [+0.0, +3.7] |
| det/kfull | the count vs the classifier (counted bodies with truth, n = 1180) | corrects a classifier error 17 of 42; introduces an error 26 of 1138 classifier-correct bodies; both wrong 25 |
| det/kfull | variant calls (anchored frames) | {'ordinary': 264, 'L6': 6}; on the non-ordinary calls: coupled 74.1 % [36.4, 100.0] (20/27), classifier 81.5 % [42.9, 100.0] (22/27), count 3.9 % [0.0, 14.3] (1/26); 6 of 6 flagged; cases ['case139', 'case19', 'case42', 'case44', 'case9'] |
| det/k5 | (i) classifier alone, all scored bodies | 92.3 % [88.1, 96.1] (1287/1394) |
| det/k5 | (ii) coupled names, all scored bodies | 90.0 % [85.7, 94.0] (1254/1394); paired difference -2.4 pp [-4.2, -0.4] |
| det/k5 | (iii) coupled names, anchored frames only | 91.0 % [87.2, 94.4] (661/726); classifier on the same bodies 95.6 % [91.9, 98.6] (694/726); paired difference -4.5 pp [-7.9, -0.9] |
| det/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 87.0 % [81.3, 91.8] (607/698); coupled on the same bodies 91.0 % [87.2, 94.3] (635/698); classifier 95.7 % [92.2, 98.6] (668/698); coupled minus count +4.0 pp [+1.3, +7.5] |
| det/k5 | the count vs the classifier (counted bodies with truth, n = 698) | corrects a classifier error 14 of 30; introduces an error 47 of 668 classifier-correct bodies; both wrong 16 |
| det/k5 | variant calls (anchored frames) | {'ordinary': 154, 'L6': 11}; on the non-ordinary calls: coupled 76.2 % [57.1, 92.2] (32/42), classifier 100.0 % [100.0, 100.0] (42/42), count 2.6 % [0.0, 8.8] (1/39); 10 of 11 flagged; cases ['case138', 'case38', 'case4', 'case42', 'case44', 'case5', 'case53', 'case63', 'case66', 'case88'] |
| det74/kfull | (i) classifier alone, all scored bodies | 95.4 % [92.6, 97.8] (1225/1284) |
| det74/kfull | (ii) coupled names, all scored bodies | 95.6 % [92.6, 97.9] (1227/1284); paired difference +0.2 pp [-1.5, +1.8] |
| det74/kfull | (iii) coupled names, anchored frames only | 96.9 % [94.0, 99.0] (1004/1036); classifier on the same bodies 96.7 % [94.3, 98.7] (1002/1036); paired difference +0.2 pp [-1.9, +2.3] |
| det74/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 95.2 % [91.1, 98.5] (986/1036); coupled on the same bodies 96.9 % [94.0, 99.0] (1004/1036); classifier 96.7 % [94.3, 98.7] (1002/1036); coupled minus count +1.7 pp [+0.0, +4.0] |
| det74/kfull | the count vs the classifier (counted bodies with truth, n = 1036) | corrects a classifier error 17 of 34; introduces an error 15 of 1002 classifier-correct bodies; both wrong 17 |
| det74/kfull | variant calls (anchored frames) | {'ordinary': 233, 'L6': 4}; on the non-ordinary calls: coupled 100.0 % [100.0, 100.0] (18/18), classifier 94.4 % [80.0, 100.0] (17/18), count 0.0 % [0.0, 0.0] (0/18); 4 of 4 flagged; cases ['case139', 'case42', 'case44'] |
| det74/k5 | (i) classifier alone, all scored bodies | 92.3 % [88.1, 96.1] (1287/1394) |
| det74/k5 | (ii) coupled names, all scored bodies | 92.3 % [88.1, 96.1] (1287/1394); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iii) coupled names, anchored frames only | 100.0 % [100.0, 100.0] (26/26); classifier on the same bodies 100.0 % [100.0, 100.0] (26/26); paired difference +0.0 pp [+0.0, +0.0] |
| det74/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.5 % [59.1, 100.0] (23/26); coupled on the same bodies 100.0 % [100.0, 100.0] (26/26); classifier 100.0 % [100.0, 100.0] (26/26); coupled minus count +11.5 pp [+0.0, +40.9] |
| det74/k5 | the count vs the classifier (counted bodies with truth, n = 26) | corrects a classifier error 0 of 0; introduces an error 0 of 26 classifier-correct bodies; both wrong 0 |
| det74/k5 | variant calls (anchored frames) | {'L6': 1, 'ordinary': 5}; on the non-ordinary calls: coupled 100.0 % (3/3), classifier 100.0 % (3/3), count 0.0 % (0/3); 1 of 1 flagged; cases ['case138'] |
| oracle/kfull | (i) classifier alone, all scored bodies | 93.7 % [90.6, 96.3] (1286/1372) |
| oracle/kfull | (ii) coupled names, all scored bodies | 95.3 % [92.6, 97.4] (1307/1372); paired difference +1.5 pp [-0.5, +3.9] |
| oracle/kfull | (iii) coupled names, anchored frames only | 95.6 % [93.1, 97.6] (1292/1352); classifier on the same bodies 94.0 % [90.8, 96.6] (1271/1352); paired difference +1.6 pp [-0.4, +4.0] |
| oracle/kfull | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 96.0 % [93.1, 98.3] (1298/1352); coupled on the same bodies 95.6 % [93.1, 97.6] (1292/1352); classifier 94.0 % [90.8, 96.6] (1271/1352); coupled minus count -0.4 pp [-1.9, +0.9] |
| oracle/kfull | the count vs the classifier (counted bodies with truth, n = 1352) | corrects a classifier error 41 of 81; introduces an error 20 of 1271 classifier-correct bodies; both wrong 40 |
| oracle/kfull | variant calls (anchored frames) | {'ordinary': 285, 'L6': 5, 'T13': 1}; on the non-ordinary calls: coupled 44.8 % [13.3, 76.7] (13/29), classifier 72.4 % [42.9, 93.3] (21/29), count 65.5 % [31.0, 100.0] (19/29); 6 of 6 flagged; cases ['case132', 'case136', 'case19', 'case42', 'case54', 'case9'] |
| oracle/k5 | (i) classifier alone, all scored bodies | 92.4 % [89.1, 95.2] (1405/1521) |
| oracle/k5 | (ii) coupled names, all scored bodies | 92.7 % [89.6, 95.4] (1410/1521); paired difference +0.3 pp [-1.0, +1.8] |
| oracle/k5 | (iii) coupled names, anchored frames only | 87.8 % [78.2, 96.0] (252/287); classifier on the same bodies 86.1 % [75.5, 95.1] (247/287); paired difference +1.7 pp [-5.4, +9.1] |
| oracle/k5 | (iv) the count alone (ordinary alphabet at the ordinal), counted bodies | 88.1 % [76.8, 98.2] (253/287); coupled on the same bodies 87.8 % [78.2, 96.0] (252/287); classifier 86.1 % [75.5, 95.1] (247/287); coupled minus count -0.4 pp [-6.5, +5.5] |
| oracle/k5 | the count vs the classifier (counted bodies with truth, n = 287) | corrects a classifier error 17 of 40; introduces an error 12 of 247 classifier-correct bodies; both wrong 23 |
| oracle/k5 | variant calls (anchored frames) | {'ordinary': 54, 'L6': 4}; on the non-ordinary calls: coupled 42.1 % [0.0, 80.0] (8/19), classifier 57.9 % [17.6, 90.0] (11/19), count 47.4 % [0.0, 100.0] (9/19); 4 of 4 flagged; cases ['case132', 'case136', 'case42', 'case54'] |

### Per truth level (all scored bodies; classifier / coupled exact, %)

- **det/kfull**: L1 n=159 96.9/97.5; L2 n=262 96.6/95.4; L3 n=282 96.5/95.4; L4 n=283 96.5/96.1; L5 n=269 98.1/98.1; T12 n=1 100.0/100.0
- **det/k5**: L1 n=198 89.9/88.9; L2 n=295 92.9/89.5; L3 n=314 93.6/88.8; L4 n=313 93.9/92.7; L5 n=246 96.8/95.9; T12 n=1 0.0/0.0
- **det74/kfull**: L1 n=159 96.9/97.5; L2 n=262 96.6/97.0; L3 n=282 96.5/96.8; L4 n=283 96.5/96.8; L5 n=269 98.1/98.5; T12 n=1 100.0/100.0
- **det74/k5**: L1 n=198 89.9/89.9; L2 n=295 92.9/92.9; L3 n=314 93.6/93.6; L4 n=313 93.9/93.9; L5 n=246 96.8/96.8; T12 n=1 0.0/0.0
- **oracle/kfull**: L1 n=207 93.7/93.7; L2 n=283 91.9/94.0; L3 n=285 96.8/98.6; L4 n=285 96.5/97.9; L5 n=277 97.5/99.3; T12 n=5 100.0/80.0
- **oracle/k5**: L1 n=271 89.3/88.9; L2 n=320 90.9/91.6; L3 n=320 95.3/95.9; L4 n=317 95.0/95.6; L5 n=251 98.4/99.2; T12 n=12 75.0/75.0

## The three real L6 patients, frame by frame

**What the truth is here, plainly.** case42, case121 and case136 are the C-ArmLSpine CBCTs SPINEPS/VERIDAH read as L2-L6 and TotalSegmentator read as L1-L5 (TotalSegmentator has no L6 class). Both saw the same lumbar-only CBCT; neither saw the thoracolumbar junction or the ribs, so neither could count. The L6 rests on VERIDAH's morphology read of the CT, not on a count from a junction. Below, `VERIDAH truth` is that naming read from the truth sacrum by the L6 alphabet and `TS read` the same bodies under TotalSegmentator's naming. A coupled call of L6 agrees with VERIDAH; ordinary agrees with TotalSegmentator; the frames alone cannot say which is right. Each frame shows FIVE bodies above the sacrum (the top body is boxed twice in the truth, once per labeller; the duplicate is dropped). `count` is the ordinary alphabet at the ordinal, which cannot name an L6.

| case view | field | variant | anchor | classifier names (top to bottom) | ordinals | count | candidate scores | call (margin, margin_next, tau) | coupled | VERIDAH truth | TS read | coupled = VERIDAH | classifier = VERIDAH | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| case42 AP | k5 | det | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 1.4103) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | det | sacrum_detector 0.727 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.6685, 'L6': -2.4564} | ordinary (0.0, 1.7879, 1.4103) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case42 AP | k5 | det74 | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | det74 | none (rejected 0.727) | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case42 AP | k5 | oracle | none | T12 L1 L2 L3 L4 | - - - - - | - - - - - | {} | no anchor (None, None, 0.1498) | T12 L1 L2 L3 L4 | None None None None None | None None None None None | no | no | no_anchor |
| case42 AP | k5 | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -1.7651, 'T13': -2.0636, 'L6': -2.3031} | ordinary (0.0, 0.2985, 0.1498) | T12 L1 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | quiet |
| case42 AP | kfull | det | sacrum_detector 0.877 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.8078, 'L6': -2.7948} | ordinary (0.0, 1.987, 1.8403) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case42 AP | kfull | det74 | sacrum_detector 0.877 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.8078, 'L6': -2.7948} | ordinary (0.0, 1.987, 1.583) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case42 AP | kfull | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -1.7506, 'T13': -1.9963, 'L6': -2.2634} | ordinary (0.0, 0.2457, 0.3499) | T12 L1 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | low_margin |
| case42 LAT | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.4103) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case42 LAT | k5 | det | sacrum_detector 0.257 | L2 L3 L4 L5 L6 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -3.2201, 'L6': -0.4465} | L6 (2.7735, 2.7735, 1.4103) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | yes | quiet |
| case42 LAT | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case42 LAT | k5 | det74 | none (rejected 0.257) | L2 L3 L4 L5 L6 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | yes | no_anchor |
| case42 LAT | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.1498) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case42 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.6316, 'T13': -4.4211, 'L6': -1.5203} | L6 (2.1113, 2.1113, 0.1498) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case42 LAT | kfull | det | sacrum_detector 0.857 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -3.0579, 'L6': -1.1065} | L6 (1.9514, 1.9514, 1.8403) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | det74 | sacrum_detector 0.857 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -3.0579, 'L6': -1.1065} | L6 (1.9514, 1.9514, 1.583) | L2 L3 L4 L5 L6 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | yes | no | disagreement |
| case42 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.5676, 'T13': -4.1892, 'L6': -1.7416} | L6 (1.826, 1.826, 0.3499) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case121 AP | k5 | det | sacrum_detector 0.286 | L2 L3 L4 L5 | - 1 2 3 | - L5 L4 L3 | {'ordinary': -5.0749, 'L6': -6.9635} | ordinary (0.0, 1.8886, 1.287) | L2 L5 L4 L3 | None None None None | None None None None | no | no | disagreement |
| case121 AP | k5 | det | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.287) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | k5 | det74 | none (rejected 0.286) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case121 AP | k5 | det74 | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | k5 | oracle | none | T12 L1 L2 L3 L4 | - - - - - | - - - - - | {} | no anchor (None, None, 0.1411) | T12 L1 L2 L3 L4 | None None None None None | None None None None None | no | no | no_anchor |
| case121 AP | k5 | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -2.9957, 'T13': -3.6557, 'L6': -3.4252} | ordinary (0.0, 0.4295, 0.1411) | T12 L1 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | quiet |
| case121 AP | kfull | det | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.5792) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | kfull | det74 | none | L1 L2 L3 L4 | - - - - | - - - - | {} | no anchor (None, None, 1.5687) | L1 L2 L3 L4 | L2 L3 L4 L5 | L1 L2 L3 L4 | no | no | no_anchor |
| case121 AP | kfull | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -2.5508, 'T13': -3.2017, 'L6': -3.7881} | ordinary (0.0, 0.651, 0.3613) | T12 L1 L2 L3 L4 L5 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | quiet |
| case121 LAT | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.287) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.3685, 'L6': -3.8131} | ordinary (0.0, 3.4447, 0.1411) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case121 LAT | kfull | det | sacrum_detector 0.569 | L2 L3 L4 L5 | 4 3 2 1 | L2 L3 L4 L5 | {'ordinary': -0.9891, 'L6': -2.4066} | ordinary (0.0, 1.4176, 1.5792) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | low_margin |
| case121 LAT | kfull | det74 | none (rejected 0.569) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.5687) | L2 L3 L4 L5 | L3 L4 L5 L6 | L2 L3 L4 L5 | no | no | no_anchor |
| case121 LAT | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.4225, 'L6': -3.5556} | ordinary (0.0, 3.1331, 0.3613) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | quiet |
| case136 AP | k5 | det | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, 1.3599) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 AP | k5 | det | sacrum_detector 0.294 | L2 L3 L4 L5 | 4 3 2 1 | L2 L3 L4 L5 | {'ordinary': -0.6533, 'L6': -5.4296} | ordinary (0.0, 4.7763, 1.3599) | L2 L3 L4 L5 | L2 L3 L4 L5 | L1 L2 L3 L4 | yes | yes | quiet |
| case136 AP | k5 | det74 | none | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 AP | k5 | det74 | none (rejected 0.294) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | L2 L3 L4 L5 | L1 L2 L3 L4 | yes | yes | no_anchor |
| case136 AP | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.1411) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case136 AP | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.7561, 'T13': -3.8851, 'L6': -3.3248} | L6 (0.4313, 0.4313, 0.1411) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | det | sacrum_detector 0.835 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.9481, 'L6': -2.2949} | ordinary (0.0, 0.3468, 2.0784) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | det74 | sacrum_detector 0.835 | L2 L3 L4 L5 sacrum | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.9481, 'L6': -2.2949} | ordinary (0.0, 0.3468, 2.0763) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 AP | kfull | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -3.8561, 'T13': -3.9739, 'L6': -3.0791} | L6 (0.777, 0.777, 0.3542) | L1 L2 L3 L4 L5 L6 | L2 None L3 L4 L5 L6 | L1 None L2 L3 L4 L5 | no | no | disagreement |
| case136 LAT | k5 | det | sacrum_detector 0.488 | L2 L3 L4 L5 | - 1 2 3 | - L5 L4 L3 | {'ordinary': -6.8169, 'L6': -6.8901} | ordinary (0.0, 0.0732, 1.3599) | L2 L5 L4 L3 | None None None None | None None None None | no | no | disagreement |
| case136 LAT | k5 | det | sacrum_detector 0.63 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -1.3308, 'L6': -1.7216} | ordinary (0.0, 0.3909, 1.3599) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | k5 | det74 | none (rejected 0.488) | L2 L3 L4 L5 | - - - - | - - - - | {} | no anchor (None, None, None) | L2 L3 L4 L5 | None None None None | None None None None | no | no | no_anchor |
| case136 LAT | k5 | det74 | none (rejected 0.63) | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, None) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | no_anchor |
| case136 LAT | k5 | oracle | none | L1 L2 L3 L4 L5 | - - - - - | - - - - - | {} | no anchor (None, None, 0.1411) | L1 L2 L3 L4 L5 | None None None None None | None None None None None | no | no | no_anchor |
| case136 LAT | k5 | oracle | truth_meta 1.0 | L1 L2 L3 L4 L5 sacrum | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -2.1713, 'T13': -3.3324, 'L6': -2.6134} | ordinary (0.0, 0.4421, 0.1411) | T12 L1 L2 L3 L4 L5 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | no | no | disagreement |
| case136 LAT | kfull | det | sacrum_detector 0.79 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.9717, 'L6': -2.7212} | ordinary (0.0, 1.7495, 2.0784) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | kfull | det74 | sacrum_detector 0.79 | L1 L2 L3 L4 L5 | 5 4 3 2 1 | L1 L2 L3 L4 L5 | {'ordinary': -0.9717, 'L6': -2.7212} | ordinary (0.0, 1.7495, 2.0763) | L1 L2 L3 L4 L5 | L2 L3 L4 L5 L6 | L1 L2 L3 L4 L5 | no | no | low_margin |
| case136 LAT | kfull | oracle | truth_meta 1.0 | T12 L1 L2 L3 L4 L5 | 6 5 4 3 2 1 | T12 L1 L2 L3 L4 L5 | {'ordinary': -1.3513, 'T13': -2.3346, 'L6': -2.8584} | ordinary (0.0, 0.9833, 0.3542) | T12 L1 L2 L3 L4 L5 | None L2 L3 L4 L5 L6 | None L1 L2 L3 L4 L5 | no | no | quiet |

- **det, whole frames with an anchor: 5 of 6**; coupled names equal VERIDAH's on 1, TotalSegmentator's on 4; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 3; calls {'ordinary': 4, 'L6': 1}; flagged 4 ({'disagreement': 2, 'low_margin': 2}).
- **det74, whole frames with an anchor: 4 of 6**; coupled names equal VERIDAH's on 1, TotalSegmentator's on 3; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 2; calls {'ordinary': 3, 'L6': 1}; flagged 3 ({'disagreement': 2, 'low_margin': 1}).
- **oracle, whole frames with an anchor: 6 of 6**; coupled names equal VERIDAH's on 0, TotalSegmentator's on 2; classifier alone equals VERIDAH's on 0, TotalSegmentator's on 2; calls {'ordinary': 4, 'L6': 2}; flagged 3 ({'low_margin': 1, 'disagreement': 2}).

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
