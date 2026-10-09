
---

## 7. C-ArmLSpine naming re-established on the v9 lineage (EVAL_LEAKS U1): every quoted row, old beside new

Written 2026-09-24 11:00 by the U1-closure item. **No manuscript file was edited.** Every number below is read from
`results/eval_gate/closure/cv_v9/` (`CV_V9.md` is the machine-written row-by-row table; `cv_v9.json` its source), and
the text as it stands is copied verbatim from the files at 10:30 today. Where the manuscript carries a
`\PENDING{G5}{C-ArmLSpine CV on the v9 lineage...}` macro, the replacement is the sentence or cells to put in its place.

### 7.0 What ran, and what the gate says

57 of the 58 UNRESOLVED quoted rows traced to `allspine_v2_r1`, whose training bank was deleted (U1). The fold models
were re-trained with **one change, the initialisation**: `slurm/carmlspine_cv_v9init.sh` (job 40431706, folds 0-4) and
`slurm/carmlspine_cv_day_v9init.sh` (40431707, day folds 0-2) fine-tune from the lineage-complete `allspine_v9` encoder
on the shipped folds' own merged banks (`~/carm_cvmix<K>_fov96_ctx`, `~/carm_cvdaymix<K>_fov96_ctx`, written before the
shipped models), with the shipped epochs (15), learning rate (1e-4), augmentation (2), seeds, mixed-length head and
prototype defaults, then score the shipped fold directories; per case fold they also run the coupling prototype
(`--dump-posterior`, the held-out sacrum detector) and zero-shot `allspine_v9` on the fold's whole frames.

**Two truths.** The shipped fold directories are symlinks into the C-ArmLSpine export, which was rewritten on
2026-09-23 (case118's oblique frame renamed, case134 added) after every quoted number was scored. So
`closure/cv_v9/prerepair_fold_dirs.py` (job 40436575) mirrored every fold directory link for link onto the kept
pre-repair export, and `slurm/carmlspine_cv_v9init_prerepair.sh` (40436580, tasks 0-7) scored the same new models on
it, with the shipped models re-run beside them as declared controls. **"pre"** (the export as it was) is the
like-for-like replacement: old and new differ by the initialisation alone. **"rep"** (the export as it stands) is
reported beside every pre number in `CV_V9.md`. The k-vertebra crops had to be regenerated for the mirror; they
match the shipped crops except that case13_LAT is one crop short at every k (case fold 0, day fold 2), so the
k = 1..5 denominators are a few items smaller than the old ones (662 against 667 at five in field, and so on).

**Collect.** `closure/cv_v9/collect_cv_v9.sh` (40436581) ran the four coupler passes and `coupling_report.py` over
both truths and the `rigor_fixes.py a4 / a7 / a9` twins, then died in `closure_cv_v9.py` on a list-valued JSON;
`closure_only.sh` re-ran that one step (40436862, and 40436983 after the zero-shot ladder), `zs_v9_kfield.sh`
(40436982) scored zero-shot `allspine_v9` at k = 1..5 on every fold, and `cv_v9_extras.sh` (40436901) computed the
count-versus-classifier matrix and the paired zero-shot-versus-fine-tuned reading.

**The gate.** Every new score file was written behind `tools/eval_gate.py` inside `level_prototype.py` with no
declaration; every family in `cv_v9.json` reads **held out, overlap 0, unresolved 0** (150 checks for the case folds,
90 for the day folds, 25 for zero-shot). The old families are refused by the strict gate (`UnresolvedLineage`, 60
and 36 unresolved links) and were read for the "old" column only under a declared reason. One caveat, not a leak:
the grid clone's `tools/eval_gate.py` is still eval_gate/1 (md5 0b00cccc; it is held there for the Figure 6 chain,
§5.4), so the new dumps carry eval_gate/1 blocks without `weights_sha256`; a scorer under eval_gate/2 will refuse them
until the evaluators are re-run under it or the read is declared. The verdicts themselves are the same under both.

**Controls (`CV_V9.md` §7).** The shipped fold models re-run with today's code on the pre-repair mirror reproduce the
shipped whole-frame score files item for item in 7 of 8 folds (day fold 0: 587 of 588 items, one call flipped,
floating-point nondeterminism across nodes); at k = 1..5 they differ by case13_LAT's missing crop and a handful of
regenerated-crop items. On the repaired export the shipped models move by 3-4 items per fold: the truth moved, the
models did not.

**Code.** `closure_cv_v9.py` imports the shipped estimators (`rigor_fixes.prop_ci`, `paired_ci`,
`cluster_level_wilson`, `carmlspine_pool_scores.boot`): case-clustered bootstrap, 2,000 resamples, seed 0. The
interval to print follows Table 4 note g: Wilson on the design-effect-adjusted n where the cell is flagged
`ceiling_regime`, the percentile interval otherwise; both are given below.

### 7.1 What moves, and which claim changes

| quantity (pre-repair truth) | old (allspine_v2_r1, UNRESOLVED) | new (allspine_v9, HELD OUT) | moves? |
|---|---|---|---|
| lateral, whole frame, case-grouped | 98.2 % (606/617); 3 of 141 cases erring; Wilson on n_eff [94.6, 99.4] | **97.4 % (601/617)**; 4 cases; Wilson on n_eff [93.2, 99.0]; percentile [94.5, 99.5]; BCa [93.2, 99.4] | inside the old interval; 5 more errors, 3 of them to thoracic names (L4→T3, L5→T4, L3→T2) |
| AP, whole frame, case-grouped | 96.7 % (610/631); Wilson [92.7, 98.5] | **96.4 % (608/631)**; 7 of 142 cases; Wilson [92.5, 98.3]; percentile [93.3, 98.6]; BCa [92.8, 98.4] | no |
| lateral, five / four / three / two / one in field | 97.0 / 95.7 / 92.9 / 89.5 / 72.8 % | **95.8 (634/662) / 94.8 (999/1,054) / 93.1 (1,079/1,159) / 89.9 (870/968) / 74.8 % (451/603)** | five-in-field −1.2, one-in-field +2.0; all inside the old intervals |
| lateral, day-grouped, whole frame | 92.5 % (571/617); [87.7, 96.4] | **92.1 % (568/617)**; 12 of 141 cases; percentile [87.5, 96.0]; BCa [86.7, 95.6] | no; **still below zero-shot 96.4 %** (paired −4.4 pp [−9.1, +0.2]; 4 cases better, 10 worse) |
| AP, day-grouped, whole frame | 96.7 % (610/631) | **94.8 % (598/631)**; 9 cases; Wilson [90.1, 97.3]; percentile [91.0, 98.0] | −1.9 pp, inside the old interval |
| lateral, day-grouped, three / one in field | 87.6 / 66.6 % | **87.7 (1,016/1,159) / 71.8 % (433/603)** | one-in-field +5.2 |
| zero-shot, lateral, three / one in field (Table 4's pending zero-shot row) | first run (zeroshot2): 86.9 (1,010/1,162) / 63.1 % (381/604) | **v9: 83.7 % (970/1,159)** [79.6, 87.5], 59 of 142 cases erring; **63.8 % (385/603)** [59.8, 67.9], 118 cases; the whole-frame 96.4 % (595/617) is reproduced | new cells (the manuscript quoted none); the v9 zero-shot is 3.2 points weaker than the first run with three bodies in view |
| fine-tuned minus zero-shot, lateral, same 617 vertebrae | not computed on a clean lineage | **+1.0 pp [−1.9, +4.0]**; 4 cases better, 2 worse; exact sign p 0.69 | **the claim that fine-tuning improves lateral naming is not supported**; what fine-tuning adds is the AP view: **+52.6 pp [+44.1, +61.3]**, 78 : 2 cases, p 5e-21 |
| abstention, lateral whole frame | answered 83.1 %, exact on answered 98.4 % (505/513) | **answered 81.5 % (503/617), exact on answered 98.8 % (497/503) [97.1, 100.0]**; at 0.9 answers 57.5 % at 99.7 %, at 0.95 answers 47.2 % at 100.0 % (291/291) | no |
| truth boxes, lateral whole frame (complete coverage) | 93.6 % (633/676) [90.0, 96.8] | **94.2 % (637/676)** [90.9, 97.0]; within one 99.1 % | no |
| coupling at 0.74, 1,009 counted bodies, 130 cases | classifier 98.4 % (993), count 97.0 % (979), coupled 98.6 % (995); coupled − count +1.6 [0.0, 3.8]; coupled − classifier +0.2 [−1.7, 2.1] | **classifier 97.7 % (986) [95.9, 99.2], count 97.0 % (979) [94.2, 99.2] (identical: the count uses no level model), coupled 98.2 % (991) [96.5, 99.5]; coupled − count +1.2 [0.0, 3.2]; coupled − classifier +0.5 [−1.5, 2.4]** | no: the count is unchanged, the coupled call still sits above the classifier and the count without a significant margin |
| disagreement and the stop signal at 0.74 | 12/233 frames (5.2 %), 34/1,066 bodies; agree 982/983; disagree coupled 13/26, classifier 11/26; flag on 4 of 5 error frames, 17 of 225 correct; unflagged 921/922 | **13/233 (5.6 % [2.6, 9.2]), 42/1,066 (3.9 % [1.8, 6.5]); agree 975/980; disagree coupled 16/29, classifier 11/29, neither 2; flag on 5 of 6 error frames, 16 of 224 correct (7.1 %); unflagged 921/922; flagged anchored 23/233 (9.9 %)** | no |
| L6 calls at 0.74 on anchored agreed five-lumbar frames | 4 of 233 (case106_AP, case139_AP, case139_LAT, case44_LAT), all with a stop | **3 of 233 (case139_AP, case139_LAT, case44_LAT), 2 cases, all with a stop**; case106_AP is now ordinary | one fewer false L6 |
| the three one-labeller L6 patients | coupled agrees with the L6 read on 1 of 5 L6 bodies, classifier 0 of 5; at 0.74 one L6 call on 4 anchored frames (case42 LAT), 2 of 6 frames unanchored | **identical: 1 of 5, 0 of 5; 1 of 4 anchored (case42 LAT, flag "disagreement")** | no |
| Figure 4d (case42 lateral, fold 2, det74) | classifier L2 0.89, L3 1.00, L4 0.96, L5 0.92, sacrum 0.02; ordinary −2.7851, L6 −0.7550; margin 2.0301 vs tau 1.6524; call L6 | **L2 0.93, L3 0.99, L4 1.00, L5 0.66, sacrum 0.01; ordinary −3.0579, L6 −1.1065; margin 1.9514 vs tau 1.583; call L6; 4 of 4 named bodies differ from the count** | the drawn rows do not move; the posteriors and margin do |
| Figure 4b (case11 lateral, fold 3, three in field) | L2 0.99, L3 0.99, L4 0.99, none | **L2 0.99, L3 0.96, L4 0.98, none**; panel count 1,079 of 1,159 (93.1 %) | two drawn posteriors and the denominator |
| Figure 5 "planning accuracy 98.22" (`FIGREC:figure5/03`) | 98.2 % (606/617) | — | already retired: Figure 5 was rebuilt on the frozen exact test (NUMBERS.md:46, SUPERSEDED) |

**Claims that change.** (1) Every fine-tuned number moves by 0-2 points and stays inside the old interval; the
headline "98.2 %" becomes 97.4 %, "606 of 617" becomes 601 of 617. (2) On the lateral view the fine-tuned model is
now one point above the zero-shot one, not significantly (4 : 2 cases); the manuscript must not credit fine-tuning
with better lateral naming. What it adds is the anteroposterior view, 52.6 points. (3) Day-grouped fine-tuning
remains below zero-shot (92.1 against 96.4 %), so REVIEW2_RSNA B4 applies: the limitation belongs in
`discussion_limits.tex` (§7.2, item 8). (4) The zero-shot cells the manuscript already quotes (595/617, 276/631,
+54.3) are reproduced exactly by the closure's own re-score of the same encoder on the pre-repair frames
(`pre:zs_v9head`).

### 7.2 The manuscript: text and cells to replace

Intervals in the sentences below are Wilson on n_eff where Table 4 note g applies (lateral and AP whole frame,
case-grouped; AP whole frame, day-grouped) and percentile otherwise; the BCa twins are in `CV_V9.md`.

**1. `main.tex:69` (Key Point 2).** As it stands:

```
\item Counting up from the detected sacrum named 979 of 1,009 bodies on anchored lateral and anteroposterior frames (97.0\,\%); fine-tuned naming, with three vertebrae in view and coupled with the count, is \PENDING{G5}{C-ArmLSpine cross-validation on the v9 lineage}.
```

Replace with:

```
\item Counting up from the detected sacrum named 979 of 1,009 bodies on anchored lateral and anteroposterior frames (97.0\,\%); fine-tuned on the other cases, SchwingNet named 601 of 617 lateral vertebrae (97.4\,\%), 1,079 of 1,159 with three in view (93.1\,\%), and, coupled with the count, 991 of the 1,009 (98.2\,\%).
```

**2. `main.tex:82` (Abstract, Results).** As it stands (fragment):

```
fine-tuned, \PENDING{G5}{C-ArmLSpine CV on the v9 lineage}. On anchored frames the count from the detected sacrum named 979 of 1,009 bodies (97.0\,\%).
```

Replace with:

```
fine-tuned on the other cases, 601 of 617 lateral (97.4\,\%; 93.2, 99.0) and 608 of 631 anteroposterior (96.4\,\%), and 568 of 617 lateral with whole acquisition days held out (92.1\,\%). On anchored frames the count from the detected sacrum named 979 of 1,009 bodies (97.0\,\%) and the coupled call 991 (98.2\,\%).
```

**3. `sections/results.tex:55-56`.** As it stands:

```
\PENDING{G5}{C-ArmLSpine CV on the v9 lineage: fine-tuned lateral and anteroposterior, case- and day-grouped; three
and one lateral bodies in view, zero-shot and fine-tuned (Figure 4b)}
```

Replace with:

```
Fine-tuned on the other cases (five case-grouped folds), it named 601 of 617 detected lateral vertebrae (97.4\,\%;
93.2, 99.0; four of 141 cases erring) and 608 of 631 anteroposterior (96.4\,\%; 92.5, 98.3): a paired gain over
zero-shot of 1.0 point on the lateral view (\(-1.9\), 4.0; four cases better, two worse) and 52.6 points on the
anteroposterior (44.1, 61.3; 78 better, two worse). With three lateral bodies in view it named 1,079 of 1,159
(93.1\,\%; 89.2, 96.2) against 970 of 1,159 zero-shot (83.7\,\%; 79.6, 87.5), and with one body 451 of 603
(74.8\,\%; 70.9, 78.7) against 385 of 603 (63.8\,\%; 59.8, 67.9) (Figure~\ref{fig:exposure}b). With acquisition days held out instead of cases, fine-tuning named 568 of
617 lateral vertebrae (92.1\,\%; 87.5, 96.0), 4.4 points below zero-shot (\(-9.1\), 0.2; four cases better, ten
worse), and 598 of 631 anteroposterior (94.8\,\%; 90.1, 97.3).
```

**4. `sections/results.tex:58-59`.** As it stands:

```
(Figure~\ref{fig:exposure}c); \PENDING{G5}{C-ArmLSpine CV on the v9 lineage: classifier and coupled call on those
bodies, against the count and the classifier; stop signal; L6 calls (Figure 4d)}.
```

Replace with:

```
(Figure~\ref{fig:exposure}c); the classifier alone named 986 of them (97.7\,\%; 95.9, 99.2) and the coupled call
991 (98.2\,\%; 96.5, 99.5), 1.2 points above the count (0.0, 3.2) and 0.5 above the classifier (\(-1.5\), 2.4).
Classifier and count disagreed on 13 of 233 anchored frames (5.6\,\%; 2.6, 9.2); where they agreed the call was
right on 975 of 980 bodies, where they disagreed the coupled call was right on 16 of 29 and the classifier on 11.
The stop signal fired on five of the six anchored frames with a coupled error and on 16 of 224 fully correct
frames (7.1\,\%); unflagged coupled calls were exact on 921 of 922 bodies. Three of 233 anchored five-lumbar frames
were called L6 (two cases), each with a stop, and on the three patients one CT reading calls six-lumbar the coupled
call agreed with that reading on one of four anchored frames (Figure~\ref{fig:exposure}d).
```

**5. `tables/tab3_naming.tex`.** Each `\PENDING{G5}` cell spans several numbers; the rows below are one table row
per number, in the table's column order (measure; % (k/n); clusters (with an error); 95 % percentile; BCa).

Line 58, as it stands:
```
 & & lateral; three and one in field & exact level & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with (zero-shot, `pre:zs_v9head`):
```
 & & lateral; three in field & exact level & 83.7 (970/1,159) & 142 (59) & [79.6, 87.5] & [79.4, 87.4] \\
 & & lateral; one in field & exact level & 63.8 (385/603) & 142 (118) & [59.8, 67.9] & [59.8, 67.7] \\
```

Line 59, as it stands:
```
 & the same; case-grouped folds\fnm{h} & lateral and AP; whole frame, three and one in field & exact level & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & the same; case-grouped folds\fnm{h} & lateral; whole frame & exact level & 97.4 (601/617) & 141 (4) & Wilson [93.2, 99.0]\fnm{g} & [93.2, 99.4] \\
 & & AP; whole frame & exact level & 96.4 (608/631) & 142 (7) & Wilson [92.5, 98.3]\fnm{g} & [92.8, 98.4] \\
 & & lateral; three in field & exact level & 93.1 (1,079/1,159) & 142 (23) & [89.2, 96.2] & [88.5, 95.9] \\
 & & lateral; one in field & exact level & 74.8 (451/603) & 142 (94) & [70.9, 78.7] & [70.7, 78.5] \\
```

Line 60, as it stands:
```
 & the same; day-grouped folds\fnm{h} & lateral and AP; whole frame, three and one in field & exact level & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & the same; day-grouped folds\fnm{h} & lateral; whole frame & exact level & 92.1 (568/617) & 141 (12) & [87.5, 96.0] & [86.7, 95.6] \\
 & & AP; whole frame & exact level & 94.8 (598/631) & 142 (9) & Wilson [90.1, 97.3]\fnm{g} & [90.2, 97.5] \\
 & & lateral; three in field & exact level & 87.7 (1,016/1,159) & 142 (38) & [83.5, 91.6] & [82.5, 91.1] \\
 & & lateral; one in field & exact level & 71.8 (433/603) & 142 (99) & [67.6, 75.9] & [67.3, 75.7] \\
```

Line 73 (coupled, conf 0.74), as it stands:
```
 & & & classifier alone; coupled; each minus the other and minus the count; disagreement and stop-signal frames; L6 calls on five-lumbar frames & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & & & classifier alone, counted bodies & 97.7 (986/1,009) & 130 & [95.9, 99.2] & -- \\
 & & & coupled, counted bodies & 98.2 (991/1,009) & 130 & [96.5, 99.5] & -- \\
 & & & coupled minus count, percentage points & +1.2 & 130 & [0.0, 3.2] & -- \\
 & & & coupled minus classifier, percentage points & +0.5 & 130 & [$-$1.5, 2.4] & -- \\
 & & & frames where classifier and count disagree & 5.6 (13/233) & 132 & [2.6, 9.2] & -- \\
 & & & anchored frames with a stop signal & 9.9 (23/233) & 132 & [5.7, 14.5] & -- \\
 & & & five-lumbar frames called L6 (each with a stop) & 3 of 233 & 2 & no interval & -- \\
```

Line 75 (coupled, conf 0.25), as it stands:
```
 & & & classifier alone; coupled; disagreement frames & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & & & classifier alone, counted bodies & 97.7 (1,122/1,149) & 139 & [95.8, 99.2] & -- \\
 & & & coupled, counted bodies & 97.1 (1,116/1,149) & 139 & [95.3, 98.8] & -- \\
 & & & frames where classifier and count disagree & 7.1 (19/266) & 142 & [3.8, 10.8] & -- \\
```

Line 78 (the three one-labeller L6 cases), as it stands:
```
 & three C-ArmLSpine cases read as L6 by one labeller\fnm{e} & whole frame; conf 0.25 and 0.74 & agreement with that read on the L6 body (coupled; classifier); anchored frames called L6 & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & 3 & no interval & -- \\
```
Replace with:
```
 & three C-ArmLSpine cases read as L6 by one labeller\fnm{e} & whole frame; conf 0.25 and 0.74 & agreement with that read on the L6 body: coupled 1 of 5, classifier 0 of 5 (both operating points); anchored frames called L6 at 0.74 & 1 of 4 & 3 & no interval & -- \\
```

Footnote h, last sentence, as it stands:
```
The case- and day-grouped fold models, first fine-tuned from that earlier encoder, are being re-run from the latest one.
```
Replace with:
```
The case- and day-grouped fold models are fine-tuned from the latest encoder on the other folds' cases; a first run from the earlier encoder gave 606/617 lateral case-grouped and 571/617 day-grouped and is not used.
```

Footnote d already describes the coupling; no change. The count-from-the-sacrum rows (lines 65-70) and the
"count alone, counted bodies" rows (72, 74: 979/1,009 and 1,104/1,149) are CLEAN and identical in the re-run.

**6. `tables/tab3_naming.md` (twin) and `tab3_naming.sources.md`.** Row 7 `98.2 (606/617) | 141 (3) | Wilson (g)
[94.6, 99.4]; percentile [95.7, 100.0] | [95.0, 99.5]` becomes `97.4 (601/617) | 141 (4) | Wilson (g) [93.2, 99.0];
percentile [94.5, 99.5] | [93.2, 99.4]`; row 21 `92.5 (571/617) | 141 | [87.7, 96.4] | [87.0, 96.1]` becomes
`92.1 (568/617) | 141 (12) | [87.5, 96.0] | [86.7, 95.6]`; row 46 `98.3 (1,129/1,149)` becomes `97.7 (1,122/1,149) |
139 | [95.8, 99.2]`; row 50 `−0.7 | 143 | [−2.4, 1.0]` becomes `−0.5 | 139 | [−2.5, 1.5]`; row 55 `98.4 (993/1,009)`
becomes `97.7 (986/1,009) | 130 | [95.9, 99.2]`; row 61 `+0.2 | 130 | [−1.7, 2.1]` becomes `+0.5 | 130 | [−1.5,
2.4]`; row 65 `98.6 (654/663)` becomes `96.8 (642/663)`; rows 68 (`94.7 (1,259/1,329)`) and 72 (`1 of 5; 0 of 5`)
are unchanged. The remaining twin rows are in `CV_V9.md` §4 cell for cell. In `tab3_naming.sources.md`, A4 → 
`results/eval_gate/closure/cv_v9/rigor_pre/a4.json`, A7 → `.../rigor_pre/a7.json` (cv5 cells; the zero-shot arm is
now `cv_v9.json#families/pre:zs_v9head`), A9 → `.../rigor_pre/a9.json`, CPL → `.../coupling_pre/coupling.json`.

**7. `figures/figure4.record.json` and the drawn figure.** Panel b footer "Three in view: 1,079 of 1,162 bodies
exact (92.9\,%)" becomes "1,079 of 1,159 bodies exact (93.1\,%)"; the drawn names "L2 0.99, L3 0.99, L4 0.99, none"
become "L2 0.99, L3 0.96, L4 0.98, none"; panel d keeps its five rows and "4 of 4", with `p_classifier` 0.925 /
0.9928 / 0.9983 / 0.6561 / 0.0066, candidates ordinary −3.0579 / L6 −1.1065, margin 1.9514 against
`tau_fold2_det74` 1.583, and "4 of 233" becomes "3 of 233 (case139_AP, case139_LAT, case44_LAT)". Panels a and c do
not move (617 of 676; 233 of 290; 979 of 1,009; the ranks are classifier-free). Inputs to re-point: `crop_b_pred` →
`closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det/k3/case11_LAT_k3_1.json`, `score_b` →
`.../cv_fold3/det_score_k3.json`, `proto_a` → `.../proto_post_v9init_prerepair/cv_fold3/det/kfull/case11_LAT.json`,
`proto_d` → `.../cv_fold2/det/kfull/case42_LAT.json`, `couple_f0..f4` / `couple_a` / `couple_d` →
`.../proto_post_v9init_prerepair/cv_fold<K>/det/kfull/couple_c74/couple_all.json`, `coupling` →
`closure/cv_v9/coupling_pre/coupling.json`, `a4` → `closure/cv_v9/rigor_pre/a4.json`, `cv5` →
`closure/cv_v9/carmlspine_cv5_v9init_pre.json` (the drop-in twin of `docs/carmlspine_cv5_mixed_2026-09-21.json`).
The caption carries no number. The `leak_gate` block's "HELD OUT" labels on the b and d rows become true under
CHK-9 once `quoted_results.json` points at these files.

**8. `sections/discussion_limits.tex`, after "only runs from a lineage-complete encoder are reported."** Add
(REVIEW2_RSNA B4, which the file's own comment says to add if the day-grouped result again falls below zero-shot;
it does, 92.1 against 96.4 %):

```
Fine-tuning on the device's own frames added one point to lateral naming and, with acquisition days held out, fell
four points below the model that had never seen the device, so frames from other days did not carry to a new day.
```

**9. `sections/discussion_motivation.tex`.** No fine-tuned number is quoted there by design (its comment); the
zero-shot 96.4 % and the count's 97.0 % stand. If the paper wants one sentence on what fine-tuning bought, it is
the anteroposterior view (43.7 → 96.4 %), not the lateral (96.4 → 97.4 %).

**10. `SchwingNet/NUMBERS.md`** (line numbers as of 10:30 today; the old EVAL_LEAKS ids are in brackets).

| line | as it stands (number) | replace with |
|---|---|---|
| 55 [L46] | 617 of 676 boxed; sacrum on 233 of 290 at 0.74 | unchanged (detector-only); file pointers → `closure/cv_v9/carmlspine_cv5_v9init_pre.json`, `coupling_pre/coupling.json` |
| 56 [L47] | 1 of 5 anchored L6 bodies at 0.25 | unchanged; file → `coupling_pre/coupling.json#cells_with_veridah_l6/det~1kfull/per_level/L6` |
| 84 [L64] | 98.2 % = 606/617, 3 cases with an error; [95.7, 100.0]; BCa [95.0, 99.5]; Wilson on n_eff 147.6 [94.6, 99.4]; within one 100 % | 97.4 % = 601/617, 141 cases, 4 with an error; percentile [94.5, 99.5]; BCa [93.2, 99.4]; Wilson on n_eff [93.2, 99.0] (design effect 4.47); within one 99.2 % — `closure/cv_v9/rigor_pre/a4.json#cells/det~1LAT~1kfull` |
| 85 [L65] | 97.9 % = 138/141, Wilson [93.9, 99.3] | 97.2 % = 137/141, Wilson [92.9, 98.9] |
| 86 [L66] | AP 96.7 % = 610/631 (6 with an error); [93.6, 99.1]; BCa [92.9, 98.7] | 96.4 % = 608/631, 142 cases (7); [93.3, 98.6]; BCa [92.8, 98.4] |
| 87 [L67] | five in field 97.0 % = 647/667, 131 cases; [93.3, 99.8]; BCa [91.7, 99.2] | 95.8 % = 634/662, 131 cases (5); [91.4, 98.8]; BCa [89.9, 98.5] |
| 88 [L68] | three in field 92.9 % = 1,079/1,162; [89.6, 95.6]; BCa [89.1, 95.4] | 93.1 % = 1,079/1,159, 142 cases (23); [89.2, 96.2]; BCa [88.5, 95.9] |
| 89 [L69] | one in field 72.8 % = 440/604; [69.0, 76.2]; BCa [69.0, 76.2] | 74.8 % = 451/603, 142 cases (94); [70.9, 78.7]; BCa [70.7, 78.5] |
| 90 [L70] | day-grouped lateral 92.5 % = 571/617; [87.7, 96.4]; BCa [87.0, 96.1]; within one 95.1 %; answered 74.9 % | 92.1 % = 568/617, 141 cases (12); [87.5, 96.0]; BCa [86.7, 95.6]; within one 93.8 %; answered 72.9 % — `closure/cv_v9/rigor_pre/a9.json#cv/cvday_acquisition_day_folds/cells/det~1LAT~1kfull` |
| 91 [L71] | day-grouped AP 96.7 % = 610/631; [93.7, 99.1]; BCa [92.7, 98.7]; answered 74.2 % | 94.8 % = 598/631 (9); [91.0, 98.0]; BCa [90.2, 97.5]; Wilson on n_eff [90.1, 97.3]; answered 73.5 % |
| 92 [L72] | day-grouped three in field 87.6 % = 1,018/1,162; [83.3, 91.6]; BCa [82.3, 91.2]; answered 73.1 % | 87.7 % = 1,016/1,159 (38); [83.5, 91.6]; BCa [82.5, 91.1]; answered 72.6 % |
| 93 [L73] | day-grouped one in field 66.6 % = 402/604; [62.6, 70.6]; BCa [62.4, 70.4]; answered 69.9 % | 71.8 % = 433/603 (99); [67.6, 75.9]; BCa [67.3, 75.7]; answered 74.3 % |
| 95 [L75] | answered 83.1 % = 513/617 [79.7, 86.3]; exact on answered 98.4 % = 505/513 [96.2, 100.0], BCa [95.0, 99.6]; 3 of 11 errors among the abstained | answered 81.5 % = 503/617 [77.7, 85.0]; exact on answered 98.8 % = 497/503 [97.1, 100.0], BCa [96.2, 99.8]; 10 of 16 errors among the abstained — `rigor_pre/a7.json#cells/cv5~1det~1LAT~1kfull/default_rule` |
| 96 [L76] | 0.9 answers 53.6 % at 99.4 % [98.1, 100.0]; 0.95 answers 42.9 % at 99.6 % | 0.9 answers 57.5 % (355/617) at 99.7 % (354/355) [99.1, 100.0]; 0.95 answers 47.2 % (291/617) at 100.0 % (291/291) |
| 97 [L77] | AP answered 77.3 % [74.2, 80.5]; exact on answered 97.5 % [95.3, 99.4] | answered 73.1 % (461/631) [69.7, 76.6]; exact on answered 97.8 % (451/461) [95.7, 99.4] |
| 98 [L78] | five in field 83.4 % answered = 556/667 [79.6, 86.8]; exact on answered 97.7 % = 543/556 [94.4, 100.0], BCa [92.8, 99.5] | 82.0 % = 543/662 [78.0, 85.7]; exact on answered 97.6 % = 530/543 [94.5, 99.6], BCa [93.0, 99.3] |
| 99 [L79] | three / one in field: 80.0 % answered, 95.6 % [93.0, 97.7]; 74.3 %, 82.9 % [78.9, 86.4] | 79.2 % (918/1,159) answered, 96.4 % (885/918) [93.8, 98.4]; 79.4 % (479/603), 84.8 % (406/479) [81.7, 87.8] |
| 100 [L80] | complete coverage with truth boxes 93.6 % [90.0, 96.8], within one 99.1 % | 94.2 % (637/676) [90.9, 97.0], BCa [89.9, 96.7], within one 99.1 % — `closure/cv_v9/carmlspine_cv5_v9init_pre.json#oracle/LAT/kfull` |
| 101-103 [L81-L83] | the first zero-shot run (594/617, 239/631, +57.7) | superseded by lines 413-415 (v9); the closure's own re-score of that encoder on the pre-repair fold frames gives 595/617, 276/631, +54.3 pp [45.7, 62.4], 79 : 1 cases, identical to `leaks/zeroshot_v9.json` |
| 205 [L185] | ladder 72.8 / 89.5 / 92.9 / 95.7 / 97.0 / 98.2 % | 74.8 (451/603, 142) / 89.9 (870/968, 143) / 93.1 (1,079/1,159, 142) / 94.8 (999/1,054, 142) / 95.8 (634/662, 131) / 97.4 % (601/617, 141); percentile [70.9, 78.7] / [86.9, 92.7] / [89.2, 96.2] / [91.1, 97.7] / [91.4, 98.8] / [94.5, 99.5]; BCa [70.7, 78.5] / [86.6, 92.5] / [88.5, 95.9] / [90.3, 97.3] / [89.9, 98.5] / [93.2, 99.4] |
| 206 [L186] | day-grouped ladder 66.6 / 81.4 / 87.6 / 90.3 / 92.8 / 92.5 % | 71.8 / 84.9 / 87.7 / 90.7 / 92.0 / 92.1 % (433/603; 822/968; 1,016/1,159; 956/1,054; 609/662; 568/617); percentile [67.6, 75.9] / [81.2, 88.4] / [83.5, 91.6] / [86.0, 94.8] / [87.0, 96.6] / [87.5, 96.0] |
| 207 [L187] | zero-shot (zeroshot2) lateral whole frame 96.3 % [93.1, 98.7] (fig5_naming, retired) | the v9 zero-shot ladder: 63.8 / 80.4 / 83.7 / 88.6 / 89.3 / 96.4 % (385/603; 778/968; 970/1,159; 934/1,054; 591/662; 595/617; 142 / 143 / 142 / 142 / 131 / 141 cases); percentile [59.8, 67.9] / [76.4, 84.0] / [79.6, 87.5] / [84.4, 92.4] / [83.7, 93.9] / [93.4, 98.9]; BCa [59.8, 67.7] / [76.4, 83.9] / [79.4, 87.4] / [84.1, 92.2] / [83.3, 93.6] / [92.5, 98.7]; the first run's ladder (zeroshot2, not used) was 63.1 / 82.6 / 86.9 / 88.5 / 90.3 / 96.3 % — `cv_v9.json#families/pre:zs_v9head/cells/LAT/k{1..5,full}` |
| 211 [L191] | case42 lateral, fold 2, det74: classifier L2 (0.89), L3 (1.00), L4 (0.96), L5 (0.92), sacrum (0.02); ordinary −2.7851, L6 −0.7550; margin 2.0301 above the fold's threshold 1.6524; call L6 | classifier L2 (0.93), L3 (0.99), L4 (1.00), L5 (0.66), sacrum (0.01); ordinary −3.0579, L6 −1.1065; margin 1.9514 above the fold's threshold 1.583; call L6; coupled L2..L6; one disagreement, flag `disagreement` — `closure/cv_v9/fig4_inputs_pre/.../cv_fold2/det/kfull/couple_c74/couple_all.json#frames[stem=case42_LAT]` |
| 213 [L193] | 233 anchored; 1,066 counted, 34 disagree = 3.2 % [1.4, 5.4]; 12 of 233 = 5.2 % [2.5, 8.7]; agree 982/983; disagree coupled 13/26, classifier 11/26, neither 2 | 233 anchored; 1,066 counted, 42 disagree = 3.9 % [1.8, 6.5]; 13 of 233 = 5.6 % [2.6, 9.2]; agree 975/980; disagree coupled 16/29, classifier 11/29, neither 2 |
| 214 [L194] | matrix diagonal 1 / 136 / 215 / 221 / 221 / 221; off-diagonal ... (total 1,066; 1,032 on the diagonal) | diagonal T12 1 / L1 136 / L2 214 / L3 220 / L4 220 / L5 220 (total 1,066; 1,011 on the diagonal); off-diagonal L2→L3 6, L3→L4 6, L4→L5 6, L2→L1 6, L3→L2 6, L4→L3 6, L5→L4 6, sacrum→L5 5, L1→L2 4, L6→L5 1, L2→L4 1, L3→L5 1, L1→T12 1 — `closure/cv_v9/cv_v9_extras_pre.json#matrix_det74_kfull`. (The old row quoted "1,032 on the diagonal" = 1,066 − 34 disagreeing bodies while its own diagonal cells summed to 1,015; the new diagonal sums to 1,011 against 1,024 = 1,066 − 42: the coupler's disagreement count does not treat every off-diagonal cell as a disagreement, a body the classifier names "sacrum" abstaining, so the two readings differ by construction, as before) |
| 215 [L195] | flag fires on 4 of 5 error frames and 17 of 225 correct (7.6 %); unflagged 921/922 | on 5 of 6 error frames and 16 of 224 correct (7.1 %); unflagged 921/922; flagged 70 of 87 (80.5 %) |
| 237 [L217] | case-grouped lateral 98.2 % (606/617) Wilson on n_eff [94.6, 99.4] (percentile upper limit 100.0 with 11 errors) | 97.4 % (601/617) Wilson on n_eff [93.2, 99.0] (design effect 4.47; 16 errors) |
| 238 [L218] | case-grouped AP 96.7 % (610/631) Wilson on n_eff [92.7, 98.5] | 96.4 % (608/631) Wilson on n_eff [92.5, 98.3] |
| 240 [L220] | case-grouped 606/676 = 89.6 % | 601/676 = 88.9 % |
| 241 [L221] | cv fold 0 lowest det_conf 0.381 | new cv (all folds) 0.364, zero-shot v9 0.364 (pre) — `cv_v9.json#detector_min_det_conf_pre` |
| 251 [L231] | classifier 993 (98.4 %) [96.8, 99.7], count 979 (97.0 %) [94.2, 99.2], coupled 995 (98.6 %) [97.2, 99.7]; coupled − count +1.6 [0.0, 3.8]; coupled − classifier +0.2 [−1.7, 2.1]; disagreement 12/233 = 5.2 % [2.5, 8.7]; flag 4 of 5 / 17 of 225; unflagged 921/922 | classifier 986 (97.7 %) [95.9, 99.2], count 979 (97.0 %) [94.2, 99.2], coupled 991 (98.2 %) [96.5, 99.5]; coupled − count +1.2 [0.0, 3.2]; coupled − classifier +0.5 [−1.5, 2.4]; disagreement 13/233 = 5.6 % [2.6, 9.2] (132 cases); flag 5 of 6 / 16 of 224; unflagged 921/922 — `coupling_pre/coupling.json#cells/det74~1kfull` |
| 298 [L278] | at 0.25: classifier 98.3 % (1,129/1,149) [96.5, 99.6], count 96.1 %, coupled 97.5 % (1,120/1,149) [95.7, 99.0], +1.4 [0.0, 3.4], −0.7 [−2.4, 1.0], disagreement 6.8 % (18/266) [3.5, 10.2], flag sensitivity 9/10, false alarm 18/252 = 7.1 %, unflagged 1,040/1,041; at 0.74 98.4 / 97.0 / 98.6; five in field at 0.25 98.6 (654/663), 88.5, 89.9 (596/663) [85.8, 93.5]; oracle 94.7 / 97.7 / 95.9 of 1,329 | at 0.25: classifier 97.7 % (1,122/1,149) [95.8, 99.2], count 96.1 % (1,104/1,149), coupled 97.1 % (1,116/1,149) [95.3, 98.8], +1.0 [−0.1, 2.9], −0.5 [−2.5, 1.5], disagreement 7.1 % (19/266) [3.8, 10.8], flag sensitivity 10/11 (90.9 %), false alarm 19/251 (7.6 %), unflagged 1,032/1,033; at 0.74 97.7 / 97.0 / 98.2; five in field at 0.25 96.8 (642/663), 88.5 (587/663), 90.3 (599/663) [86.3, 93.8]; oracle boxes 94.7 (1,259/1,329) / 97.7 (1,298) / 97.0 (1,289) — `coupling_pre/COUPLING.md` §"five test folds pooled" |
| 299 [L279] | 1 of 5 coupled, 0 of 5 classifier | unchanged |
| 301 [L281] | ordinary spines today: 260 of 266 anchored frames ordinary, 6 called L6 in five cases | 261 of 266 ordinary, 5 called L6 in four cases (case139, case19, case44, case9) at 0.25; at 0.74, 230 of 233 ordinary, 3 L6 in two cases |
| 402-403 | "every case- and day-grouped fold cell (606/617, 610/631, 571/617, ...)" UNRESOLVED | resolved by this section: each replaced above |
| 417 | first zero-shot run, not used: 594/617, 239/631 | add: first fold-model runs, not used: 606/617 case-grouped, 571/617 day-grouped lateral (Table 4 note h) |

**11. `CLAIMS_LEDGER.md:211`** ("classifier unchanged in 20 of 20 cells; coupled 90.3 % [79.8, 98.4] vs classifier
86.0 % [75.1, 95.4] on anchored bodies; DEFENSIBLE AFTER a verifier re-runs"): the re-run's report again shows the
classifier unchanged in 20 of 20 cells (`coupling_pre/COUPLING.md` "The classifier did not move"); the oracle
five-in-field cell it quotes (`oracle_ext/k5`) is now coupled 93.0 % (239/257) [84.9, 99.2] against classifier
90.3 % (232/257) [80.7, 98.0]; the verifier's re-run is this closure, with the gate on every input.

**12. Rows that do not move, and rows this closure does not own.** The count from the sacrum (Table 4 lines 65-70,
72, 74; Key Point 2's 979 of 1,009; `FIGREC:figure4/07-12`) uses no level encoder and is identical in the re-run.
The zero-shot whole-frame cells already in the text (595/617, 276/631, +54.3) are reproduced. `RESCORE:G1`, `H1`,
`H2` take the det74/kfull, case-grouped lateral and zero-shot cells above. `FIGREC:figure5/03` is retired. Not this
closure's: `results.tex:72` and Figure 5's in-domain data-case panels (`results/indomain/fit.json`, the
`indomain_name_fill` workflow) and the Flagship cells of `tab2_detection.tex:54-66` (FLAGSHIP_PLAN G5).

### 7.3 Where every number here is read from

| number | file (all under `SchwingNet/results/eval_gate/closure/cv_v9/`) |
|---|---|
| every cell, old and new, both truths | `cv_v9.json#families/<old|pre|rep>:<cv5_det|cv5_oracle|cvday_det|zs_v9head|zs_v9nohead|zeroshot2>/cells/<VIEW>/k<K>` (k, n, clusters, clusters_with_error, percentile, bca, wilson_effective_n, ceiling_regime, answered, exact_on_answered, abstain_sweep, within1, per_level, confusions); tabulated in `CV_V9.md` |
| the pooled twins of `docs/carmlspine_cv5_mixed_2026-09-21.json` | `carmlspine_cv5_v9init_pre.json`, `carmlspine_cvday_v9init_pre.json` (and `_rep`) |
| a4 / a7 / a9 twins of `results/a4.json`, `a7.json`, `a9.json` | `rigor_pre/a4.json`, `a7.json`, `a9.json` (and `rigor_rep/`) |
| coupling | `coupling_pre/coupling.json` (`#cells/det74~1kfull`, `det~1kfull`, `det~1k5`, `oracle~1kfull`, `oracle_ext~1k5`, `#cells_with_veridah_l6`, `#l6_patients`, `#tau`), `coupling_pre/COUPLING.md`; the five det74 coupler records `fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold<K>/det/kfull/couple_c74/couple_all.json` |
| paired zero-shot vs fine-tuned; the matrix | `cv_v9_extras_pre.json#pairs/<LAT|AP>/<comparison>`, `#matrix_det74_kfull` |
| Figure 4 b and d records | `cv_v9.json#figure4/b_pre`, `d_pre`; the input files under `fig4_inputs_pre/` |
| controls | `cv_v9.json#controls`, `prerepair_fold_dirs.json` |
| gate verdicts | `cv_v9.json#families/*/gate`, `#strict_gate_on_old`; each score file's own `eval_gate` block on the grid (`/rs/rs_grp_oschome/go2432/data/carmlspine/proto_v9init_prerepair/`, `proto_post_v9init_prerepair/`) |
| job logs | `grid_pull/` (carmcv9i, carmcvday9i, carmcv9pre, cv9iprerep, cv9icollect, cv9iclosure, cv9iextras, zs9kfield) |

---

## 8. The accuracy-saturation reading (Greg's request of 2026-09-24): what these numbers support

Greg asked that the ideas of the uploaded overview ("Advanced Computational Frameworks for Vertebral Body Detection
and 2D/3D Registration in Intraoperative Fluoroscopy", `3e8e7309-AA_.pdf`) be integrated, "especially the learning
rate accuracy saturation part". The part in question is its §2: a fluoroscopy model that plateaus near 90 % while
standardised radiographs reach 99 % is rarely capacity-limited; the plateau is sampling-density saturation in a
high-dimensional acquisition space (positioner angles, SID, magnification, patient position), so adding randomly
sampled same-device data yields diminishing returns, and the remedy is coverage-driven sampling of the sparse
acquisition bins (a coverage ratio per dimension and a normalised entropy over DICOM tags). This section states what
the closure's held-out numbers say about that reading; the paper workflow owns the text. **The overview is an
unsourced synthesis; the paper cites its primary sources** (its works-cited list: DeepDRR, Unberath 2018; DiffDRR,
Gopalakrishnan 2022; the pairwise domain-adaptation module, Zheng 2018, PMC5767648; LevelCheck, De Silva 2016;
X23D, Jecklin 2022), never the overview.

**What the C-ArmLSpine numbers show (pre-repair truth, all held out; `cv_v9_extras_pre.json`, `CV_V9.md` §6).**

1. *Lateral naming is saturated before any same-device frame is seen.* Zero-shot, trained on renders and
   radiographs only, names 595 of 617 detected lateral vertebrae (96.4 %). Fine-tuning on the other ~118 cases of
   the same device changes 22 calls (14 gained, 8 lost) for 601 of 617 (97.4 %): +1.0 point [−1.9, +4.0], four
   cases better and two worse, exact sign p 0.69. The recurrent head adds +0.8 [−2.4, +4.2] over the encoder alone.
   Same-device data does not move the lateral plateau.
2. *The anteroposterior view is a coverage hole, and same-device data fills it.* Zero-shot names 276 of 631 AP
   vertebrae (43.7 %); fine-tuned, 608 of 631 (96.4 %): +52.6 points [+44.1, +61.3], 78 cases better and 2 worse.
   The AP geometry of this C-arm is not in the render/radiograph training distribution; ~118 cases of it are enough
   to bring AP to the lateral ceiling.
3. *Within one device, acquisition day is a coverage dimension.* With whole acquisition days held out, the
   fine-tuned model names 568 of 617 lateral vertebrae (92.1 %): 4.4 points below zero-shot [−9.1, +0.2], four
   cases better and ten worse, and 5.3 points below the case-grouped fine-tune [+2.1, +9.1], eight cases better and
   none worse (p 0.008). Same-device frames from other days do not transfer to a new day; they move the model off
   the broad prior towards the seen days. On the AP view the day-grouped fine-tune still gains 51.0 points over
   zero-shot, so the hole the AP frames fill is a view, not a day.
4. *Same-device data buys most where the field is smallest, and nothing on the whole frame.* Fine-tuned:
   74.8 / 89.9 / 93.1 / 94.8 / 95.8 / 97.4 % at one to five lateral bodies and the whole frame; zero-shot:
   63.8 / 80.4 / 83.7 / 88.6 / 89.3 / 96.4 %. Paired on the same crops (`cv_v9_extras_pre.json#pairs_by_k`), the
   fine-tuned gain over zero-shot is +10.9 [+6.4, +15.5] at one body (65 : 24 cases), +9.5, +9.4 [+4.5, +14.5],
   +6.2, +6.5 at two to five, and +1.0 [−1.9, +4.0] on the whole frame. The day-grouped fine-tune shows the same
   shape at a lower level: +8.0 [+3.3, +12.5] at one body, +4.0 at three, and −4.4 on the whole frame. So the
   whole-frame lateral plateau is the render-and-radiograph prior's own ceiling; the limited field, where a body
   must be named from its shape with little context, is where the device's own frames add coverage.
5. *What the manuscript cannot yet claim.* The overview's "99 % on standardised radiographs" has no held-out
   counterpart of our own: the plain-film accuracies (97.3-99.8 %) are the encoder's selection split (EVAL_LEAKS
   L4) and no held-out film number exists until the Figure 6 model is scored. The comparison in the paper must be
   lateral (96.4 %, held out, unseen device) against AP (43.7 %), not film against fluoroscopy.

**Proposed use in the paper (for the paper-six-figures workflow).** One sentence in the Results after the
fine-tuned numbers (item 3 of §7.2 already carries the paired gains) and one paragraph in the Discussion, in place of
a second same-device-data claim: the lateral plateau did not respond to same-device data, the anteroposterior view
did, and a held-out day was worse than never having seen the device; so the next data should be chosen by where the
acquisition space is empty (view, day, and, by the DICOM positioner and distance tags, angle and magnification), not
by volume. The Limitations sentence of §7.2 item 8 carries the day-grouped fact.

**A concrete follow-up this closure did not run** (a new analysis, not a re-score): the coverage and normalised
entropy the overview defines can be computed for C-ArmLSpine from the DICOM tags already on the grid
(`/rs/rs_grp_oschome/go2432/data/carmlspine/headers_dossier.json`, `tags_case*.txt`: positioner primary and
secondary angle 0018,1510 / 0018,1511, SID 0018,1110, patient position 0018,5100) over the 148 cases and their
acquisition days, and per fold. It would say whether the held-out days occupy acquisition bins the other days do
not, which is the overview's mechanism stated as a measurement rather than an interpretation; and it would give
Figure 2 of the flagship plan (the sampling chart) a real-device column. It needs a CPU job and a reading of the
per-frame tags; no checkpoint is involved.
