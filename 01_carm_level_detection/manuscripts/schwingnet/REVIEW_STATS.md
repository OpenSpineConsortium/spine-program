# Statistical review: SchwingNet, *Radiology: Artificial Intelligence* (Original Research)

Reviewer role: the journal's statistical consultant. Reviewed on 2026-09-23 against `main.pdf` (27 pages, built 17:11,
text identical to `main.tex` + `sections/*.tex` + `tables/*.tex` at 13:57) and the result files under `results/`.
**The manuscript was not edited.** One tool and one result file were added so that every number proposed below has a
file behind it: `tools/stats_review_recompute.py` writes `results/stats_review/recompute.json` (2,000 resamples, seed 0;
run with `python SchwingNet/tools/stats_review_recompute.py`). Other proposed numbers are already in the named result
files.

**Verdict: 11 PASS, 22 FAIL.** No FAIL comes from a wrong number: every printed value I traced is in its file. The
failures are in how intervals and tests are chosen and labelled, which denominators are shown, and how the design
and pre-specification are described. Four of them change what the paper can claim:

- **F6.** The pre-stated device-card criterion is not met under any interval suited to six folds.
- **F9.** The primary endpoint is conditional on a detector that the Methods never name. Counting undetected vertebrae as failures, the rate is 87.9 %.
- **F16.** The words "pre-specified" and "fixed beforehand" do not match the repository's dated history.
- **F17.** The "power" statement gives at most 46 % power at a true accuracy of 97 %.

**Word budget.** The body is at 2,999 of 3,000 words and the abstract at 250 of 250. Most corrections below add words.
Each gives the replacement text and the approximate net change. The coordinator decides the offsetting cuts, and
`tools/check_limits.py` has to be re-run after every edit.

---

## 1. Recomputations from the JSON files (five required, six done)

| # | Quantity as printed in main.pdf | Source file | Recomputed here (recompute.json key) | Verdict |
|---|---|---|---|---|
| R1 | Count from the detected sacrum, whole-vertebra boxes, confidence 0.74: 95.4 % = 188/197 (89.4, 99.5); 81.0 % = 188/232; defined on 46/56 frames | `counting/lodo_carm__carm_test__outline__0.74.json` (per frame, 28 cases) | 188/197 (89.2, 99.5); 188/232 (73.7, 87.6); 46/56 (71.4, 92.9); also **188/287 = 65.5 % (53.5, 76.9)** of all truth bodies on the 56 frames (`R1_counting_074`) | PASS. The numerators and denominators are exact, and the intervals agree to within Monte-Carlo error of a separate resampling stream. |
| R2 | Card gain in held-out R² +0.038 (0.021, 0.057), 24 folds, 4 negative, sign-flip P = .0002 | `a3.json#comparisons/card_vs_uncalibrated_physics` (24 fold values) | Mean 0.0376, percentile (0.0205, 0.0573): identical. **Exact** sign-flip over 24 folds P = .00023, so the printed .0002 is the Monte-Carlo floor 1/5,001. Frame-weighted mean **0.025**. Device-level sign-flip over the 4 device means **P = .125**. t interval over the 4 device means **(−0.001, 0.077)** (`R2_card`) | Arithmetic PASS; inference FAIL (F6) |
| R3 | Exact cluster tests and Holm: lateral vs AP 86 vs 2 cases; film vs render 23 vs 0 spines; same-device vs held-out sacrum 8 vs 0 cases | `a3.json#primary_with_holm` | P = 2.5e−23, 2.4e−7 and .0078. Holm-adjusted: 1.0e−22, 7.2e−7, .0078, and card .00046 (`R3_tests`) | Arithmetic PASS; the printed "P = .002 each" is not among these values (F1) |
| R4 | Wilson lower bounds: n = 60 gives 94.0 / 91.1; n = 37 gives 90.6 / 86.2 | `power_table.json` | 93.98 / 91.14 and 90.59 / 86.18 (`R4_wilson.lower_bound_pct`) | PASS (for power, see F17) |
| R5 | 98.2 % = 606/617 (95.7, 100.0); Methods: "Wilson intervals on the design-effect-adjusted count" | `a4.json#cells/det~1LAT~1kfull` (design effect 4.18) | Wilson with the Kish adjustment **(94.6, 99.4)**; BCa (95.0, 99.5). Zero-shot 594/617: Wilson with the Kish adjustment **(92.0, 98.3)**, BCa (92.3, 98.5) (`R5_ceiling`) | Arithmetic PASS; interval choice FAIL (F3) |
| R6 | Coupling at confidence 0.74 (Figure 5d): classifier 993, count 979, coupled 995 of 1,009 bodies; 12 of 233 frames disagree | `coupling_c74/cv_fold{0..4}_det_kfull_couple_all.json` (per frame) | 993 / 979 / 995 of 1,009 in 130 cases; 12/233; coupled − count +1.6 (0.0, 4.0); coupled − classifier +0.2 (−1.7, 2.2) (`R6_coupling_074`) | PASS. It matches `coupling.json#cells/det74~1kfull`. |

The following were also traced to their files and PASS as printed. Detector (`a1.json`): 231/287, 43/56, 260/287,
47/56. Renders only: 91/287 and 1/287. Per-source arms (`contribution_matrix.json`): 249/287, 37/287, +71.8 (63.4, 79.6),
−2.1 (−6.0, 1.4), −47.7, seed spread 1.1–5.6. Image-formation classifier (`a2.json`): −0.7 (−10.1, 8.6). Card per device (`a6.json`): Cios Fusion BCa (−0.0005, 0.027).
Naming (`a7.json`, `a4.json`, `a9.json`, `a3.json`): 594/617, 239/631, +57.7 (48.9, 66.4) on 593/140, 610/631,
647/667, 440/604, 571/617, 513/617 and 505/513. Films (`a5.json`): 3,629/3,635, 2,671/2,744, 441/445. Coupling at 0.25
(`coupling.json`): 1,129 / 1,104 / 1,120 of 1,149, 18/266, 9/10, 18/252, 1,040/1,041. Inventory
(`anomalous_inventory.json`, `rare_class/…`): 198, 89, 65, 37. Denominators (`docs/DATASHEET.md` §2.3,
`docs/carmlspine_cv5_mixed_2026-09-21.json`): 814/910, 676 in 143. Two numerators that coincide were checked and are
genuine: the case-grouped and zero-shot abstention rules both answer 513 of 617. They are different computations (71 against 70
error clusters; exact on answered 505 against 500).

---

## 2. Intervals, denominators and tests, item by item

### F1. P values: the bootstrap floor is printed as a P value. **FAIL**
The Results print "all four pre-listed comparisons survive Holm adjustment (P = .002 each)" (results.tex:25), which
is 4 × 1/2,000, the resolution floor of a 2,000-resample bootstrap. It is not an estimate. The Methods (methods.tex:92–93)
say paired comparisons use "an exact sign test over clusters", and those tests give other values (R3). The same
comparison is then printed twice with different P values: "P = .002" in the detection paragraph and "sign-flip P = .0002" in
the formation paragraph. Journal style prints P < .001, not .0002.
**Correction.** results.tex:24–25: replace "The same-device control found the sacrum on 98.2\,\% (55 of 56), a paired
difference of 14.3 points (5.4, 23.2); all four pre-listed comparisons survive Holm adjustment ($P=.002$ each)." with
"At the default point the same-device control found the sacrum on 98.2\,\% (55 of 56), 14.3 points more (5.4, 23.2;
$P=.008$)." (about −6 words).
results.tex:37: "(sign-flip $P=.0002$)" becomes "(sign-flip $P<.001$)".
results.tex:49, after "(48.9, 66.4)": insert "; $P<.001$".
results.tex:27, the film-versus-render difference: add "$P<.001$" (see F11).
methods.tex:94: "significance was two-sided $P<.05$" becomes "$P$ values are Holm-adjusted exact cluster tests; significance was two-sided $P<.05$" (+6 words).

### F2. The abstract gives no indication of statistical significance. **FAIL**
The journal requires "indicators of statistical significance" in the abstract Results. The abstract (main.tex:48) has none.
**Correction.** After "(0.021, 0.057)" insert "; $P<.001$". After "239 of 631 anteroposterior (37.9\,\%)" insert "($P<.001$)".
In the Materials and Methods sentence, "paired differences carry Holm adjustment" becomes "$P$ values are Holm-adjusted
exact cluster tests" (net about +6 words).

### F3. Percentile intervals at the ceiling: an upper limit of 100 % despite observed errors. **FAIL**
With 11 errors in 3 of 141 cases, about 5 % of case resamples draw no erring case, so the 97.5th percentile is exactly
100 %. That is outside any valid interval for a rate with observed errors. The same failure appears in six other places:

- Key Point 1: "(98.2 %; 95.7, 100)".
- Results, results.tex:51.
- Table 3, lateral case-grouped row [95.7, 100.0] and CSXA [99.6, 100.0].
- Table 3, five-in-field classifier [96.5, 100.0].
- Table 2, sacrum controls [94.6, 100.0], [85.7, 100.0] and [89.3, 100.0].
- Figure 5a, which draws the same cell.

The result files already flag these cells (`ceiling_regime: true`). The Methods promise Wilson intervals on the
design-effect-adjusted count, but none is printed.
**Correction.** methods.tex:91: replace "cluster shares carry Wilson intervals on the design-effect-adjusted count" with
"where errors fall in few clusters (flagged in the result files), the Wilson interval on the design-effect-adjusted
count replaces the percentile interval" (+8 words).
Then print these values:

- 98.2 % → (94.6, 99.4) in Key Point 1, results.tex:51 and Table 3 (`R5_ceiling.cv5_lateral.wilson_kish`).
- CSXA → BCa (99.5, 99.9) from `a5.json`, or the Kish-adjusted Wilson interval.
- Table 2 sacrum controls 55/56, 54/56 and 53/56 → Wilson (90.6, 99.7), (87.9, 99.0) and (85.4, 98.2) (`R5_ceiling.table2_sacrum_wilson`). The design effect is about 1.06, so the unadjusted Wilson interval is adequate.
- The five-in-field coupling cell has no per-frame file locally. Recompute it on the grid, or print "--".
- Redraw Figure 5a with the same rule.

**Recommended but not required: the primary endpoint.** The zero-shot 96.3 % (594/617) is also flagged as ceiling
regime: all 23 errors fall in 6 cases, each wrong on every vertebra. Its percentile interval (93.1, 98.7) is narrower at
the lower end than the BCa interval (92.3, 98.5) and the Kish-adjusted Wilson interval (92.0, 98.3). Under the rule
above, print (92.0, 98.3) in Key Point 1, the abstract, the Results and Table 3. The case-level rate, 135 of 141 cases
entirely right (91.0, 98.0), is the most transparent companion.

### F4. A zero-width "confidence interval". **FAIL**
Table 2, "Cios Fusion only" row: sacrum at 0.25 is 50.0 (28/56) [50.0, 50.0]. In every case the anteroposterior frame
found the sacrum and the lateral frame missed it (`contribution_matrix.json` `by_view`: AP 100 %, lateral 0 %), so every
resample returns 50 %. That is not an interval.
**Correction.** Replace the cell with "AP 28/28, lateral 0/28; no interval".

### F5. Bootstraps over six clusters. **FAIL**
Two sets of intervals rest on six clusters:

- Table 2, the DeepFluoro six-specimen rows: 78.6 (338/430) [68.8, 92.0] and 95.0 (321/338) [78.5, 99.8].
- The per-device card intervals, which bootstrap six folds.

Percentile bootstraps over six units undercover. The narrowness bias alone is a factor of about sqrt(5/6), before skew.
**Correction.** Table 2 footnote e: append "six-specimen intervals rest on six clusters and are descriptive". For the card
intervals, see F6.

### F6. The device-card inference treats 24 folds as independent units. **FAIL** (substantive)

- **Unit and dependence.** The folds are nested in 4 devices. Within a device they are leave-one-group-out fits whose training sets overlap. Counting every fold as independent (P < .001 over folds) overstates the evidence: over device means, 4 of 4 are positive, P = .125, and the t interval is (−0.001, 0.077) (R2).
- **Weighting.** The 0.038 is an unweighted fold mean. Two PIXIUM folds hold one frame each (+0.175, +0.128). Weighted by frames the gain is 0.025, and the median is 0.034 (R2).
- **The pre-stated criterion** (docs/RSNAI_PLAN.md C3, committed 2026-09-22 06:47): "gain > 0 on every device with the CI excluding 0". It holds only on the six-fold percentile bootstrap. On six-fold t intervals, only BV Pulsera excludes zero: Cios Fusion (−0.003, 0.034), Elekta XVI (−0.006, 0.053), PIXIUM 4600 (−0.019, 0.159). The exact sign-flip test rejects on BV Pulsera alone (a6.json `verdict`).

**Correction.**

- results.tex:37: "raised held-out $R^2$ over uncalibrated physics by 0.038 (0.021, 0.057) over 24 folds, four negative (sign-flip $P=.0002$)" becomes "raised held-out $R^2$ over uncalibrated physics by 0.038 (0.021, 0.057; frame-weighted 0.025) over 24 folds nested in four devices, four negative (sign-flip over folds $P<.001$; all four device means positive, $P=.13$)".
- results.tex:37–40: "held on percentile intervals and failed on the BCa interval for the Cios Fusion (0.015; $-0.0005$, 0.027)" becomes "was not met: it held only on six-fold percentile bootstraps, and on six-fold $t$ intervals only the BV Pulsera gain excluded zero (Cios Fusion 0.015; $-0.003$, 0.034)".
- Key Point 3 (main.tex:36): after "(0.021, 0.057) across 24 folds" add "of four devices, the pre-stated every-device criterion not met". Also correct "on 40 real exposures" to "on up to 40 real exposures": PIXIUM 4600 was fitted on 14 of 18 (Table 1).
- Discussion (discussion_motivation.tex:27–28): "their gain small and failing the stricter interval on one device" becomes "their gain small, and the pre-stated every-device criterion not met".
- Net about +35 words.

### F7. The abstract's counting denominator is conditional twice. **FAIL**
"Counting placed 188 of 197 matched bodies at the right ordinal (95.4 %)" (main.tex:48) counts only bodies that were
both on the 46 of 56 frames with a detected sacrum and matched by the detector. Of the truth bodies on the defined
frames, 188 of 232 (81.0 %) were named right. On all 56 frames the figure is 188 of 287 (65.5 %; 53.5, 76.9). "Denominators everywhere" requires
the conditioning to be visible.
**Correction.** In the abstract: "Counting, defined on 46 of 56 frames, placed 188 of 197 matched bodies (95.4\,\%) and 188 of
232 truth bodies (81.0\,\%) at the right ordinal." (+10 words).
Discussion (discussion_motivation.tex:13–14): "placed 95.4\,\% of matched bodies at the right ordinal" becomes "placed 95.4\,\% of
matched and 81.0\,\% of all truth bodies on frames with a detected sacrum at the right ordinal".

### F8. "misses at the field edge" is not what the file says. **FAIL**
results.tex:58 says the misses are at the field edge. `fig5_naming_data.json#b` shows 16 of 35 missed truth boxes within 6 px of the border; the other 19
are interior. Twenty-five of the 35 misses are at ordinals five and six (`counting.json` `by_truth_ordinal`).
**Correction.** "81.0\,\% of all 232 truth bodies, misses at the field edge" becomes "81.0\,\% of all 232 truth bodies; 25 of
the 35 misses were at ordinals five and six, 16 within 6 pixels of the frame border" (+12 words).

### F9. The primary endpoint is conditional on an unnamed detector. **FAIL** (substantive)
Naming is scored only on vertebrae that a detector boxed: 617 of the 676 agreed lateral vertebrae, 91.3 %.

- In `slurm/carmlspine_cv.sh` that detector is the film keypoint detector `detector_v5z_final`, run at the `tools/level_prototype.py` default confidence of 0.35. It is not the YOLO11m detector that the Methods describe.
- The Methods never say which detector finds the bodies that are named ("each detected body", methods.tex:68).
- Scored against every agreed vertebra, with undetected ones counted wrong, zero-shot naming is 594/676 = **87.9 %** and case-grouped naming is 606/676 = 89.6 % (`R5_ceiling`).
- "Full coverage" in the Methods refers to abstentions, not to detection.

**Correction.**

- methods.tex:67–68: "around each detected body" becomes "around each body boxed by a film-trained keypoint detector that never saw C-ArmLSpine (confidence 0.35)" (+12 words). Confirm that the zero-shot run (`zeroshot2`) did not override `--conf`.
- results.tex:47–48, after "six of 141 cases erring)" insert "; 87.9\,\% of all 676 agreed, undetected vertebrae counted wrong" (+10 words).
- Keep "617" as the stated denominator in Key Point 1 and the abstract. It is honest only once the Methods sentence exists.

### F10. The coupling results in the text use a different operating point from the figure they cite, and one difference has the wrong denominator. **FAIL**

- **Operating point.** results.tex:58–64 quote the coupled call at confidence 0.25: 1,149 bodies, 18/266 frames, 9 of 10 errors flagged. The sentence cites "(Figure 5c, d)", but Figure 5 is drawn at 0.74: 1,009 counted bodies, 12/233 frames, 4 of 5 errors flagged. It is also odd that 0.74, the pre-stated point everywhere else, is not the point used for this secondary outcome.
- **Sign.** The difference between coupled call and classifier changes sign between the two points: −0.7 at 0.25 and +0.2 at 0.74. Both intervals include zero.
- **Denominator.** In "0.7 below the classifier (−2.4, 1.0)" the point and interval are from `coupling.json#…/coupled_minus_classifier`, which is computed over all 1,248 scored bodies in 143 cases. The sentence is about the 1,149 counted bodies, on which the difference is (1,120 − 1,129)/1,149 = −0.8 points.

**Correction** (recommended: quote the pre-stated point). Replace results.tex:58–64 from "On 1,149 counted bodies" to
"(Figure~\ref{fig:safety}c, d)." with:
"At confidence 0.74, on 1,009 counted bodies of 130 cases the classifier was exact on 98.4\,\% (993), the count on
97.0\,\% (979) and the coupled call on 98.6\,\% (995), 1.6 points above the count (0.0, 3.8) and 0.2 above the classifier
($-1.7$, 2.1); the mechanisms disagreed on 5.2\,\% of anchored frames (12 of 233), the flag fired on four of five frames
with an error and 17 of 225 without, and the coupled call was exact on 921 of 922 unflagged bodies
(Figure~\ref{fig:safety}c, d)."
Sources: `coupling.json#cells/det74~1kfull`, keys `classifier_exact_counted`, `count_exact_counted`,
`coupled_exact_counted`, `coupled_minus_count_counted`, `coupled_minus_classifier_anchored` (n = 1,009),
`disagreement_frames` and `flags`. R6 reproduces them. The replacement is about word-neutral.
Add the 0.74 rows to Table 3's coupled block. They are in its Markdown twin.

### F11. The film-versus-render detector comparison is in-sample, and neither its operating point nor that status is stated in the text. **FAIL**
results.tex:26–27: "a film-trained detector beat a render-trained one by 27.5 points (20.5, 35.2)".

- The film detector trained on the spines behind 196 of these 233 bodies (a3.json `caveat`). Its 99.1 % is not a held-out number.
- The difference is at confidence 0.05, not at either reported operating point. At 0.25 it is 55.4 points.
- The comparison is still one of the four in the Holm family.

Table 2 footnote f discloses this; the sentence does not.
**Correction.** Replace with "a film-trained detector, in-sample for 196 of them, found 27.5 points more than a render-trained one
at confidence 0.05 (20.5, 35.2; $P<.001$)" (+9 words).

### F12. The formation classifier: one cell quoted selectively, and a null result read as evidence. **FAIL**
results.tex:40–42 quotes −0.7 (−10.1, 8.6), the features/logistic cell. That is the only one of six pooled
leave-one-corpus-out cells below chance. The others run to +9.2 (−0.5, 19.7), and two of six BCa intervals exclude zero:
+9.2 (1.4, 23.4) and +8.4 (0.6, 21.6) (`a2.json#corpus_manifold/excess_over_chance`; RIGOR_FIXES.md A2 says so).
The sentence also concludes "so a detector must be held out by device, not modality" from an interval that allows a
gain of 8.6 points. Absence of evidence is not evidence of equivalence.
Methods (methods.tex:94–95): "of 120 film-versus-fluoroscopy cells, six" [quoted]. The text quotes one.
**Correction.**

- results.tex:41–42: "exceeded the majority-class share of 71.8\,\% by $-0.7$ points ($-10.1$, 8.6), so a detector must be held out by device, not modality" becomes "differed from the majority-class share of 71.8\,\% by $-0.7$ to 9.2 points across three feature spaces and two classifiers, no percentile interval excluding zero (two BCa intervals did); transfer across modality was not shown, so detectors are held out by device" (+14 words).
- methods.tex:94–95: "of 120 film-versus-fluoroscopy cells, six" becomes "of 120 film-versus-fluoroscopy cells, the six pooled cells are summarised".

### F13. A confounded source contrast is written as a cause, and one of two seeds is quoted. **FAIL**

- "Transfer followed angular coverage" (results.tex:28), "the training source whose exposures span the gantry arc carried the transfer" (Key Point 2, abstract Results) and "set by the angular coverage of training exposures" (abstract Conclusion) all attribute the +71.8 to angular coverage.
- Adding the radiotherapy source changes device, anatomy (110 patients against 4 specimens), frame count (2,640 against 238) and angle together.
- The only control is the equal-count arm. At equal size it still exceeds the cadaver source by 26.1 points (18.2, 33.6) (`contribution_matrix.json#named_paired_comparisons`). No arm isolates angle.
- The marginal contributions quote the seed-0 pair only. With the seed-1 pair, adding the cadaver source is −6.3 (−9.8, −2.9), which excludes zero, against −2.1 (−6.0, 1.4) printed.

**Correction.**

- results.tex:28: "Transfer followed angular coverage:" becomes "Transfer tracked the source whose frames span the arc:".
- After "(63.4, 79.6)" add "(second training seed 67.6; 57.6, 76.8)".
- After "($-6.0$, 1.4)" add "(second seed $-6.3$; $-9.8$, $-2.9$)".
- Key Point 2 and abstract Results: "carried the transfer" becomes "carried most of the transfer".
- Abstract Conclusion: "set by the angular coverage of training exposures" becomes "and depended on which source's exposures were in training".
- Net about +15 words.

### F14. The leakage-robust estimate is missing from the abstract and Key Point 1. **FAIL**
The case-grouped cross-validation may put one person in two folds: cases are acquisition sessions, and 66 of them fall
on one date (`carmlspine_day_groups.json`). The repository's own rule for that risk is in docs/RESUME_2026-09-22_PM.md
A9: "if it moves, that is the number". It moved: day-grouped folds give 92.5 % (571/617; 87.7, 96.4), against 98.2 %
case-grouped. The abstract and Key Point 1 quote only 98.2 %.
**Correction.**

- Abstract: "with case-grouped folds, 606 of 617 (98.2\,\%)" becomes "fine-tuned with folds grouped by case, 606 of 617 (98.2\,\%), by acquisition day, 571 (92.5\,\%)" (+7 words).
- Key Point 1: after "after case-grouped fine-tuning" add ", 571 (92.5 %) with folds grouped by acquisition day".

### F15. Clustering by case where a case may not be a person. **FAIL**
All C-ArmLSpine intervals bootstrap over cases: the primary endpoint over 141, and the held-out detector test and the
counting over 28. The Limitations say that whether 148 cases are 148 people "cannot be established". They do not say
what that does to the intervals. If cases share persons, every C-ArmLSpine interval is too narrow. The day-grouped
analysis addresses leakage, not variance: its interval is still over cases.
**Correction.** In discussion_limits.tex:5, after "both groupings are reported, their gap unexplained;" add "every
intraoperative interval treats cases as independent and is too narrow if they are not;" (+14 words).
Every other source is clustered at the right unit:

- COBRA2026: patient.
- DeepFluoro: specimen.
- Films: patient key.
- Formation classifier: corpus.
- Transitional power: person.

### F16. Wording of pre-specification, checked against the repository's dated history. **FAIL** (substantive)

| Claim in main.pdf | Evidence | Verdict |
|---|---|---|
| "The pre-specified primary outcome" (methods.tex:79) | The zero-shot lateral result had been scored and plotted by 2026-09-21 22:58 (commit ef4c583). The phrase "pre-specified primary" first appears at 2026-09-23 02:58 (commit 27f3863). No dated protocol names it earlier. | FAIL |
| 0.74 "fixed beforehand" (methods.tex:51; Key Point 2), "pre-stated operating point" (abstract M&M; results.tex:21, 26; Table 2 caption; discussion_motivation.tex:13, 19) | The rule reads no C-ArmLSpine frame, which is legitimate. But (i) it pools the detector's sweeps on three other devices, including the **Geneva phantom**, not "the two training devices" (`tools/or_recall_curves.py:220–223`; a1.json `how_chosen`); (ii) it was computed in the same run as the test curve and adopted as the headline by the rigor audit on 2026-09-22 21:12, after the 0.25 result (90.6 / 83.9) had been quoted in docs/RSNAI_PLAN.md at 06:47. The choice was the conservative one. | FAIL (wording) |
| "Holm adjustment over four pre-listed comparisons" (methods.tex:93) | The family was named by the analysis audit (a3.json `holm_note`), which ran after the data were seen. | FAIL (wording) |
| 97 % counting grade "pre-stated" (Introduction, Methods, Results) | docs/RSNAI_PLAN.md C7, 2026-09-22 06:47. That is before designs A and B were scored, and after the reported detector's 0.25 result. | PASS |
| C3 card criterion "pre-stated" | docs/RSNAI_PLAN.md C3, 06:47. That is before any device fit was reported: the first status line, with BV Pulsera and Cios Fusion done, is dated 09:00. | PASS |
| Wilson 90 % / 85 % transitional bounds "pre-stated" | docs/FLAGSHIP_PLAN.md G6, 2026-09-23 01:50. Gate G6 has not been run. | PASS |
| Abstention threshold 0.5 "a default never tuned"; coupling margin threshold | `tools/level_prototype.py` default; threshold cross-fitted on the other four folds (`coupling.json#definitions/tau`) | PASS |

**Correction.**

- methods.tex:79: "The pre-specified primary outcome was" becomes "The primary outcome, designated after the zero-shot run was first scored, was" (+6 words).
- methods.tex:50–51: "and the training devices' pooled F1 threshold (0.74), fixed beforehand;" becomes "and 0.74, the best pooled F1 of its sweeps on the three other devices (COBRA2026, DeepFluoro, Geneva), a rule that reads no C-ArmLSpine frame;" (+10 words).
- Key Point 2: "at an operating point fixed beforehand" becomes "at an operating point chosen without its frames".
- Abstract M&M: "at a pre-stated operating point" becomes "at an operating point set on other devices".
- results.tex:21: "at the pre-stated operating point" becomes "at the cross-device operating point".
- results.tex:26: "at the pre-stated point" becomes "at 0.74".
- Table 2 caption: "the pre-stated (0.74)" becomes "the cross-device (0.74)".
- Table 2 footnote b: "0.74 = best pooled F1 on the reported detector's two training devices, fixed before its test frames were read" becomes "0.74 = best pooled vertebra F1 of the reported detector over its sweeps on COBRA2026, DeepFluoro and the Geneva phantom; no C-ArmLSpine frame enters the rule, adopted after the 0.25 result was reported".
- discussion_motivation.tex:13: "at the pre-stated operating point" becomes "at the cross-device operating point".
- discussion_motivation.tex:19: "and a pre-stated operating point" becomes "and an operating point set without the test device".
- methods.tex:93: "four pre-listed comparisons" becomes "the four comparisons named before adjustment (lateral versus anteroposterior naming, same-device versus held-out sacrum, film- versus render-trained detector, fitted versus default formation)" (+17 words). This also fixes the problem that the Results announce "all four" before two of them have been introduced.

### F17. The "sample size" paragraph is not a power calculation. **FAIL** (substantive)
"60 test persons give 94.0 % with no error and 91.1 % with one" (methods.tex:88–89) is arithmetically right (R4). It is
the bound obtained if the result is perfect or nearly so. It is not the probability of meeting the target.

- At n = 60 the ≥ 90 % criterion allows at most one error. The chance of passing is 46 % if the true accuracy is 97 %, 66 % at 98 % and 88 % at 99 %.
- At the 37 projected persons no error is allowed, and the chance of passing is 32 %, 47 % and 69 % (`R4_wilson.probability_bound_met`).
- 80 % power needs 99 persons at a true 97 % and 69 at a true 98 % (`R4_wilson.smallest_n_for_80pct_power`).
- Per subtype, the ≥ 85 % sensitivity bound needs at least 22 carriers with no miss (`min_n_zero_errors`). Under the 50/10/40 rule only the mobile L6 row (83 persons, about 33 test) can reach it. The T13 row (6 persons), the four-lumbar row (11) and the fused L5 row (16) cannot, whatever the result. The per-subtype criterion as written in Table 4's caption and Methods is infeasible for them.
- The primary endpoint has no sample-size statement beyond "no sample size was set for naming".

**Correction.** Replace methods.tex:88–89 from "No sample size was set" to "(90.6\,\%, 86.2\,\%)." with:
"Naming used every available case; at 617 vertebrae the 95\,\% interval half-width is about three points. The
transitional criteria are Wilson lower bounds; 60 test persons give 94.0\,\% with no error and 91.1\,\% with one, and
pass with 46\,\% probability if the true accuracy is 97\,\% (66\,\% at 98\,\%); the 89 on hand give 37 test persons,
which must be error-free (90.6\,\%). The 85\,\% sensitivity bound applies to the pooled count-changing group; per
subtype it needs 22 carriers without a miss, so per-subtype rates are descriptive." (about +35 words).
Mirror the pooled-versus-per-subtype statement in the Table 4 caption and in Figure 6d's legend. Note also that
"count-changing = mobile L6 + T13" leaves out 45 persons whose presacral count also differs: 34 L6 fused to the sacrum
and 11 sacralised L5 with four lumbar vertebrae. State the definition where the 89 first appears.

### F18. Multiplicity outside the Holm family. **FAIL**
The Results quote several paired contrasts and intervals from the 24-arm contribution matrix: +71.8, −2.1 and −47.7,
the equal-count +26.1 (via F13), and the seed spread. They also quote the coupled-minus-count difference. None is
adjusted, and none is labelled as exploratory. The Methods sentence "Of 1,440 detector rescoring cells five are quoted" is
stale. That family was counted before the 0.74 cells from a1.json and the body-convention 5.2 % cell were added, and
Table 2 now prints about 60 cells.
**Correction.** methods.tex:94: replace "Of 1,440 detector rescoring cells five are quoted" with "Detector arms were scored over a
confidence sweep and up to three box conventions; Table~\ref{tab:detection} prints every arm at the two operating points,
and contrasts outside the four adjusted comparisons are exploratory and unadjusted" (+18 words).

### F19. Software named without manufacturer; the statistical code not named. **FAIL** (minor)
The journal asks for the statistical software with version and manufacturer. Python, NumPy and SciPy carry no
manufacturer, and the code that computed every interval (`tools/rigor_fixes.py`, revision 6e1cf8d) is not named.
**Correction.** methods.tex:95–96: "Python 3.11" becomes "Python 3.11 (Python Software Foundation, Wilmington, Del)". "NumPy 2.2.6 and
SciPy 1.15.3" becomes "NumPy 2.2.6 and SciPy 1.15.3 (open source); intervals and tests by the released rigor tool
(revision 6e1cf8d)".

### F20. Film validation is scored on the split that chose the checkpoint, from a single seed. **FAIL** (wording)
`tools/train_level_classifier.py:466–472` keeps the epoch with the best accuracy on the bank's validation split, and
`a5.json` scores the patient-keyed films on that same split. The 97.3–99.8 % is therefore validation accuracy with a
small optimism, not an independent test. Five window protocols were scored. The quoted "random" protocol is not the
clinical field size of three to four bodies: at three bodies the rates are BUU-LSPINE 95.0 % and NHANES II 94.6 %.
Three seeds of the later v9 bank give NHANES II 96.9–97.6 % (`v9_a5_seeds.json`).
**Correction.** results.tex:55: "patient-keyed film validation read 97.3\,\%--99.8\,\% exact across the three annotated
releases" becomes "on the patient-keyed validation split that also chose the encoder checkpoint, films read 97.3\,\%--99.8\,\%
exact (random windows of two to nine bodies; 94.6\,\%--99.6\,\% at three)" (+14 words). The three-body values are from
`a5.json` `maximal_band3`: BUU 94.97, CSXA 99.64, NHANES II 94.61.

### F21. Traceability: result-file paths are stale after the box-convention move (A28). **FAIL** (the journal may recalculate)
NUMBERS.md and `tables/tab2_detection.sources.md` cite `lcurve.json#devices/surgio_b51_dr/points[0]/at/0.74/vertebra_recall`
for the design-B cell 63.1 % (181/287). After A28 that path holds the **body** convention, 12.5 % (36/287). The printed
181/287 is at `…/points[0]/alt/outline/0.74`. The same applies to:

- the PR-AUC 0.890, at `alt/outline/pr_auc_vertebra`; the top-level key is 0.067;
- the C-ArmLSpine control rows 116/119/115/117 of 287 and PR-AUC 0.367/0.385, at `all_real[i]/alt/outline`, while `at` now holds 241/258/235/260;
- Figure 3's NUMBERS rows for these cells.

`tools/fig_detection.py:115` reads the right key, so the figure is correct; the ledger is not.
**Correction.** Change those paths to `alt/outline/...` in NUMBERS.md and `tab2_detection.sources.md`.
Change "`alt/body` for the body-convention reading" to "`at` (body since A28)".

### F22. Abstract Materials and Methods: case count. **FAIL** (minor)
"named vertebrae on 148 lumbar cases" (main.tex:46), but the primary denominator spans 141 cases: 143 carry agreed lateral truth
and 141 have a detected vertebra.
**Correction.** "on 148 lumbar cases" becomes "on 148 lumbar cases (141 with scored lateral vertebrae)" (+4 words), or
drop the number and let the Results carry 617 of 141.

---

## 3. Items that pass

- **P1.** Every printed interval is a 95 % bootstrap of 2,000 cluster resamples at the stated unit, and the BCa interval is in Table 3 and the twins.
- **P2.** Every percentage in the abstract, Key Points, Results and Tables 2–4 carries a numerator and denominator, either in the text or in the table it cites. This holds subject to F7, F9 and F22.
- **P3.** Paired designs are analysed as paired: same items, same cases, exact cluster sign tests, McNemar tests in the files. No unpaired test is applied to paired data.
- **P4.** Holm is applied correctly (R3), in both bootstrap and exact forms.
- **P5.** "Significant" appears only in the statistics sentence, and no difference is called significant without a test.
- **P6.** The one-specimen DeepFluoro test column carries no interval and says so (Table 2 footnote e).
- **P7.** The whole-vertebra box convention is stated in every detector caption and footnote, and each quoting sentence survives the G5 recompute.
- **P8.** The selective-quoting counts are disclosed. They are corrected by F12 and F18.
- **P9.** The abstention results are at full coverage with the answered share beside them, and the untuned threshold is disclosed.
- **P10.** The film-detector comparison's in-sample status is disclosed in Table 2 footnote f. The text is corrected by F11.
- **P11.** The Wilson bounds and Figure 6d arithmetic are correct (R4 reproduces the quoted cells; NUMBERS.md records a 30-of-30 check against `scipy.stats.binomtest`).

---

## 4. The "Top 10 list of statistical errors" (Radiology 2009;253:288–290)

The repository holds only the requirement file's transcription of the list: denominators, P values with estimates,
"significant" only with a test, sample-size justification, clustered data. Those five items are checked first; the
rest are the consultant's standard items.

| Item | Status | Where |
|---|---|---|
| Numerators and denominators for every percentage | FAIL until F7, F9 and F22 are applied | Abstract counting; primary endpoint conditional on detection |
| P values reported with the estimates, in journal format | FAIL | F1, F2 (bootstrap floor as P; ".0002"; none in the abstract) |
| "Significant" only with a test | PASS | P5 |
| Sample-size justification or power | FAIL | F17 |
| Correct handling of clustered data | FAIL | F6 (folds in devices), F15 (case against person). The other units are right. |
| Confidence intervals valid for the estimate | FAIL | F3 (upper limit 100 % with errors), F4 (zero width), F5 (six clusters) |
| Multiple comparisons | FAIL (partly) | Holm family correct (P4); its wording and scope are F16 and F18 |
| Paired data analysed as paired | PASS | P3 |
| Non-significance read as equivalence | FAIL | F12 ("must be held out by device"), F6 (criterion said to hold) |
| Pre-specification and selective reporting | FAIL | F16, F12, F13 (seed 0 only), F20 (protocol choice) |

---

## 5. What the corrections do to the claims

- **Held without change:** the detector result (80.5 % and 76.8 % at 0.74), the lateral-versus-anteroposterior contrast, the zero-shot lateral result, which becomes (92.0, 98.3) if F3's rule is applied, and the counting ordinal accuracy.
- **Weakened, and to be said:**
  - the device-card criterion (F6);
  - the modality-boundary conclusion (F12);
  - the angular-coverage attribution (F13);
  - the fine-tuned 98.2 %, which appears only beside the day-grouped 92.5 % (F14);
  - the unconditional naming rate, 87.9 % zero-shot (F9);
  - the transitional design, which has under 50 % power at plausible accuracies (F17).
- **New numbers.** Every number these corrections introduce is either in `results/stats_review/recompute.json` or already in `a2.json`, `a5.json`, `a6.json`, `coupling.json`, `contribution_matrix.json` or `fig5_naming_data.json`. Add each to NUMBERS.md with its key when it enters the manuscript.
