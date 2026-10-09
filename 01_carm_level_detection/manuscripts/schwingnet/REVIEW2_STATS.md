# Second statistical review: SchwingNet, the six-figure wrap (*Radiology: Artificial Intelligence*, Original Research)

Reviewer role: the journal's statistical consultant. Reviewed on 2026-09-24 against the wrapped draft: `main.tex` and
`sections/*.tex` as saved 06:17–06:20, `tables/*.tex` as saved 06:20–06:29, `supplement.tex` (06:14), and `main.pdf`
built at 06:33 by grid job 40430741. **The manuscript was not edited and nothing was committed.** One tool and one
result file were added so that every number proposed below has a file behind it:

- `tools/stats_review2_recompute.py` writes `results/stats_review2/recompute.json`. Run it with
  `python SchwingNet/tools/stats_review2_recompute.py` (about 20 s). It reads only local result files and the frozen
  Figure 6 split snapshot (`results/fig6/frozen/v1/`).
- Keys are cited below as `S<n>` (for example `S6_coupling_074`).

**Verdict.**

- Of the 22 earlier FAILs, **16 are resolved, 5 are partly resolved, and 1 minor one remains** (§1).
  F6, F9 and F16 are resolved. F17 is only partly resolved, and it is the one that matters now (N1).
- Every printed power, `n_min` and Wilson number reproduces exactly from `results/power/power.json` and from
  LEVELCHECK_MODEL.md §5/§7/§11 (§2).
- The manuscript's description of the LevelCheck plan matches the frozen file, with three wording conditions (§3).
- There are **21 new findings**. Five of them change what the paper can claim:

**N1. As frozen, the confirmatory analysis will fail for reasons that have nothing to do with naming.** The power
paragraph hides this.

- The power statement assumes a person-level accuracy of 95 %. No transitional measurement supports that number.
- The frozen endpoint (LEVELCHECK_MODEL.md §4) scores a person wrong for any of these:
  - a missed body;
  - a frame with no sacrum anchor;
  - an abstention.
- **Ordinary development frames.** Scored by that endpoint, ordinary C-ArmLSpine frames were right on 162 of 284
  (57.0 %). With the prototype's abstentions counted as well, they were right on 54 of 284 (19.0 %).
- **COBRA2026.** The pre-specified COBRA2026 sacrum detector at 0.74 found the sacrum on 21 of 609 frames (3.4 %),
  and on no frame at all for 19 of 27 patients. Every candidate real-frame at-risk person is a COBRA2026 patient, and
  so are 41 of the at most 51 ordinary ones.
- **Outcome.** H1 and H6 cannot pass as specified, however well the network names vertebrae.
- **What can be done.** This can still be addressed before unblinding (§9 of the frozen file). The decision belongs to
  the author; §5 lists what must happen before unblinding.

**N2. Fine-tuned numbers are presented as if the network had never seen the device.**

- The Discussion and Key Point 2 give 92.9 % with three bodies in view in the setting where the network was never
  trained on the device.
- Zero-shot, it named 86.9 % (1,010 of 1,162). With day-grouped folds it named 87.6 %. The 92.9 % is the case-grouped
  fine-tuned figure.
- The 98.6 % coupled call also comes from the case-grouped fine-tuned fold models.

**N3. Coupling's gain over counting rests entirely on three cases and is not significant.**

- The +1.6 points over counting are 16 bodies on four frames, in three cases.
- On those frames the coupled call chose the L6 alphabet on spines that both labellers read as five-lumbar. The exact
  sign test over cases gives P = .25.
- Against the shape classifier alone the coupled call gains nothing: 995 against 993, three cases better and three
  worse. The abstract and Key Point 2 leave the classifier out.

**N5. The L6 classifier's sensitivity is printed without its false positives.**

- It called 111 of 1,012 validation L5 crops L6, as well as 75 of the 98 true L6 crops.
- So among L5 and L6 crops, an L6 call was right 75 times in 186 (40.3 %).
- The journal requires specificity or predictive value beside sensitivity.

**N7. The best-case 93.7 % leans on screen calls that the labeller's own track record does not support.**

- The labeller's T13 calls matched readers in 0 of 52 on CTSpinoPelvic1K.
- Yet 38 of the 57 "supported" COBRA2026 calls are T13 calls.

**Word budget.** The body is at 2,985 of 3,000 words and the abstract at 248 of 250. The corrections required below
add about 122 body words. The cut menu in §6 removes about 123, so the result is word-neutral. Its cuts fall on the
three weakest analyses in the paper, which is a statistical argument as well as a budget one. The abstract rewrite
comes to 250 words. `tools/check_limits.py` must be re-run after the edits.

---

## 1. The 22 FAILs of REVIEW_STATS.md, one by one

| # | Topic | Status now | Evidence in the wrapped draft | Residual action |
|---|---|---|---|---|
| F1 | Bootstrap floor printed as P | **RESOLVED** | The main text gives only P<.001 (lateral against AP, results.tex:47). The supplement gives exact sign-test Ps (.008; P<.001). Methods:109–112 names exact sign tests with Holm. | None, but see N9 on the Holm family. |
| F2 | No significance indicator in the abstract | **RESOLVED** | Abstract: "(37.9 %; P<.001)". | None. Optionally write "paired P<.001" if a word is free. |
| F3 | Percentile interval reaching 100 % despite errors | **RESOLVED** in the main text | Methods:107–109 states the rule. The four ceiling cells in Table 4 carry Kish-adjusted Wilson intervals. Table S2 sacrum controls are Wilson. | The mirror case, a lower limit of 0 despite successes, remains in Table S2 (N18). |
| F4 | Zero-width interval | **RESOLVED** | Table S2: "AP 28/28, lateral 0/28". | None. |
| F5 | Six-cluster bootstraps | **RESOLVED** | Table S2 footnote e: "their six-cluster intervals descriptive". | The same problem now sits in Figure 2's ten-person intervals (N6). |
| F6 | Card inference over 24 folds | **RESOLVED** | Supplement "Image-formation terms": frame-weighted 0.025, device-level P=.13, criterion "was not met". Methods:59–60: "missed their pre-stated criterion". | The Holm family still carries the fold-level test (N9). |
| F7 | Abstract counting denominator conditional twice | **PARTLY** | The 188/197 sentence has left the abstract. It was replaced by "the count named 979 of 1,009 bodies", which covers only the 233 of 290 frames with a sacrum anchor. Of all 1,248 scored bodies the count named 979 (78.4 %) (`S6`). | Say "on anchored frames" (abstract, Key Point 2; §4). |
| F8 | "Misses at the field edge" | **RESOLVED** | The sentence is gone. | None. |
| F9 | Primary endpoint conditional on an unnamed detector | **RESOLVED** | Methods:63–64 names the YOLO11m-pose film detector at 0.35. Results:45–46 gives 87.9 % of all 676. | The abstract still says "594 of 617 lateral vertebrae"; add "detected" (§4). |
| F10 | Coupling operating point; denominator | **PARTLY** | The operating point (0.74) and the denominator (1,009) are fixed. **But the "0.2 above the classifier (−1.7, 2.1)" that F10's replacement text carried was dropped.** Without it the reader cannot see that coupling adds nothing over shape alone (N3). | Reinstate it (§4, N3). |
| F11 | Film vs render detector in-sample | **RESOLVED** | Supplement: "in-sample for 196 of them … at confidence 0.05 … P<.001". Table S2 footnote f. | None. |
| F12 | Formation classifier quoted selectively | **RESOLVED** | Supplement "Corpus manifold": −0.7 to 9.2, two BCa intervals exclude zero, "no claim rests on the modalities being indistinguishable". | None. |
| F13 | Angular-coverage attribution; one seed | **RESOLVED** | Supplement: "tracked the source whose frames span the gantry arc", second seed, "no arm isolates angle". The abstract no longer attributes cause. | None. |
| F14 | Day-grouped estimate missing | **PARTLY** | Resolved for the primary endpoint (abstract, Key Point 1, Results). **Not applied to the field-size results, which moved more**: three in view, 92.9 % case-grouped against 87.6 % day-grouped. The A9 rule "if it moves, that is the number" applies to them too (N2). | Add the day-grouped and zero-shot field rows (§4). |
| F15 | Case against person as the cluster | **RESOLVED** | discussion_limits.tex:3–5. | None. |
| F16 | "Pre-specified" wording | **RESOLVED** | Methods:77–78 "designated after the zero-shot run was first scored". The 0.74 rule is described (Methods:66–67; Table S2 footnote b). "Named before adjustment" (Methods:110) makes no pre-specification claim. Every remaining "pre-stated" or "frozen" traces to a dated commit (ecae75f, 1897772, 2993f40, b511985) or to docs/RSNAI_PLAN.md and FLAGSHIP_PLAN.md. | Two "fixed before unblinding" statements are true only once uncommitted files are committed (N16). |
| F17 | "Power" paragraph not a power calculation | **PARTLY** | Methods:103–106 now gives exact-test power against the frozen values, and every number in it reproduces (§2). The per-subtype criterion is now pooled. **But the 95 % planning accuracy is unsupported, and the power does not reflect the frozen endpoint's detection, anchor and abstention failures (N1).** "Count-changing" is still undefined (N12). The feasibility of H6 is not stated (N8). | §4, N1, N8, N12. |
| F18 | Multiplicity outside the Holm family | **RESOLVED** | Methods:111: "other contrasts are exploratory". The stale "1,440 cells" sentence is gone. | None. |
| F19 | Software and code identification | **PARTLY** | Manufacturers are added. **The rigor tool's revision (6e1cf8d) is not given.** The power numbers were computed with SciPy 1.18.1 under Python 3.12 (`power.json` was generated locally; LEVELCHECK_MODEL.md §11 says "scipy 1.18"), not with the stated 1.15.3 under 3.11. Exact binomial values do not depend on the version, but the statement is inaccurate (N17). | §4. |
| F20 | Film validation is the selection split | **RESOLVED** for films | Table 4 rows "selection split", footnote f. | **The same issue applies to the Figure 2 embedding in the abstract and Key Point 3**, where it is not said (N8b). |
| F21 | Stale result-file paths | **RESOLVED** | NUMBERS.md:293–294 and 326–330, and tab2_detection.sources.md line 6, cite `alt/outline/...`. | None. |
| F22 | Abstract "148 cases" | **OPEN (minor)** | Unchanged. The primary endpoint spans 141 cases. | Acceptable while the Results carry 617 of 141. Change it if words allow. |

Count: 16 resolved (F1–F6, F8, F9, F11–F13, F15, F16, F18, F20, F21), 5 partly resolved (F7, F10, F14, F17,
F19), 1 open (F22).

---

## 2. Power and sample-size statements against `results/power/power.json`

Every value is recomputed independently in `S1_power_checks`. The test is the one-sided exact binomial
P(X ≥ k | n, p0) at α = 0.025, and power is enumerated for n = 1…2,000.

| Printed claim (where) | power.json | Recomputed (`S1`) | Verdict |
|---|---|---|---|
| The exact test needs 19 at-risk persons against 82.2 % and 152 against 97.6 % (Results:61–62; Key Point 3; Discussion; Table 3) | `n_needed_zero_errors` 19, 152 | 19, 152. Holm steps: 23/25/28 and 181/198/226 | **PASS** as a minimum. The wording must be "at least" (N11). |
| With no error, a Wilson lower bound of 90 % needs 35 persons, and above 97.6 % needs 157 (Results:61) | 35; panel a crossing 157 | 35; 157 (156 gives 97.597) | **PASS** |
| 85 % bound: 22 carriers (Table 2 footnote f) | 22 | 22 | **PASS** |
| Against 82.2 %, 80 % power at 55; 71 at Holm α/3 (Methods:104–105) | `first_n_power_80` 55, 71 | 55 and 71. Monotone from there on (from_n 55, 71) | **PASS**, but see N1 on the 95 % assumption |
| Against 97.6 %, power below 0.1 % at any size (Methods:105) | `97.6@95` power_at 152 = 0.0004 | Maximum over n ≤ 2,000 is 0.00041, at n = 152 | **PASS** |
| At a true 99 %, 80 % first reached at 708 (Methods:106; Figure 5b) | 708; from 763 | 708; from 763 | **PASS**. Power exceeds 80 % always from 763 onward; the curve is sawtoothed. |
| If all 57 calls were confirmed, the lower bound would be 93.7 % (Results:65; abstract; Figure 5d) | panel d 93.69 | 93.7 | **PASS** as arithmetic. The best case is implausible (N7). |
| Table 2 best-case bounds 91.8 / 74.1 / 43.9 / 90.8 / 56.6 / 67.6 / 61.0 / 75.8 / 61.0 / 93.7 | panel d | identical (`S1.wilson_lower_zero_error_pct`) | **PASS** |
| 57 CT test persons (L6 43, T13 3, sacralised L5 11); 48 in the encoder lineage (Results:66–67) | `panel_c_available` | as printed | **PASS**, but at most 57 are at risk (N7) |

**What §2 does not settle.** The arithmetic is right. The assumption behind it is the problem, and N1 addresses it.

---

## 3. The LevelCheck comparison plan in the manuscript against LEVELCHECK_MODEL.md

The frozen file is unchanged in §1–§11 since ecae75f. The only diffs are the additions in §12 (1897772, efab8dd), §13
(2993f40) and §14 (b511985).

| Element | Frozen file | Manuscript | Verdict |
|---|---|---|---|
| p0 values and sources | §3, §11: 0.822 (Peh), 0.976 (Manbachi), 0.926 (non-inferiority, 5-point margin) | Methods:88–94; Table 3 | **PASS**. The margin is disclosed as chosen knowing the ordinary results. |
| At-risk rule; naming unaffected | §3 | Methods:90–92; Table 3 footnote b | **PASS** |
| Unit, frame, draw | §4: person; ≥ 4 reference-named bodies; fixed seed | Methods:94–95; Table 3 footnote c | **PASS** |
| "Correct" | §4: missed, unnamed, abstained or unanchored = not correct | Table 3 footnote c, **yes**. Methods:95 "correct only if every body gets its reference name", **without the failure modes** | **FAIL** (N1). The failure modes decide the result, so the Methods must say them. |
| Test, α, Holm, eligibility | §5 | Methods:95–97; Table 3 footnotes c and d | **PASS** |
| Primary frames real; renders secondary; the three C-ArmLSpine L6 excluded | §4 | Methods:97; Table 2 footnote c; Table 3 footnote b | **PASS** |
| Scored configuration "fixed before unblinding" | §4: named in the G5 manifest and **committed before unblinding** | Methods:98–100 (ImageNet initialisation, coupled call, 0.74, whole frame, seed 0) | **CONDITIONAL** (N16). `results/fig6/` (RUN_v2.json) and `slurm/fig6_*.sh` are untracked. The held blinded job refuses to start without a G5-manifest commit, so the claim will be true if that gate is used. **But the open gate scores H6 persons before that commit** (U3 in §5). |
| Automated reference "fixed before unblinding" | §14: rule and PPV written with SHA-256 **before any test person is scored** | Methods:43–46 | **CONDITIONAL** (N16). §14's selection criterion is committed (b511985). The rule is not yet frozen: `results/auto_reference/` holds only `readerC/`. |
| Comparator values are constants | power.json `what`: "the comparator is a fixed modelled value, so its own sampling error is not modelled" | not said | **FAIL (minor)** (N10) |
| Pre-stated Wilson targets (90 %, 85 %) | §5 last paragraph: "separate from this comparator" | Methods:84–85, "on pooled count-changing test persons" | **FAIL (minor)** (N12). The population is undefined, and the manuscript does not say that the targets sit outside the Holm family. |
| §6 "always stated" (modelled; ceiling where the read counted correctly; not a wrong-level rate) | §6 | Figure 6 caption "Modelled, not measured"; Discussion:22–27 | **PASS** |
| §7 plain answer on 97.6 % | "reported beside the interval, not beaten" | Discussion:26–27 | **PASS** |
| §7 sweep and break-even p* | "Marked: p\* and the frozen p0" | The Figure 6 caption marks the frozen values and anchors, not p\*. It gives 10–100 % but not the 90–100 % range for ordinary spines. | **Note for the Figure 6 owner** when the figure lands. |
| §13 coverage beside accepted accuracy | "must print coverage beside every accepted-accuracy number" | pending (G6) | Check at G6. |
| Significance level | one-sided 0.025 | Methods:111–112 "significance was two-sided P<.05" (the frozen paragraph above it does say one-sided) | **Minor** (N13) |

---

## 4. New findings, with replacement text

Line numbers refer to the files as saved at 06:17–06:29. LaTeX is given as it should be pasted. "Words" is the change
in the `check_limits.py` count for the body (Introduction to Discussion) unless marked otherwise.

### N1. The frozen endpoint, the detectors fixed for Figure 6, and the 95 % planning accuracy. **FAIL** (substantive)

**The assumption.**

- Methods:103 gives transitional power "at a planning accuracy of 95 %".
- LEVELCHECK_MODEL.md §7 lists 90, 95 and 97 % as planning values. It also says (§8) that "the closest development
  measurements of transitional naming … are all below the frozen 82.2 %". The Figure 5 record says the same.
- At any true accuracy at or below 0.822, the test's power cannot exceed 0.025 (`S2`). At 0.90, 80 % power needs
  162 persons (`S1.H1_true90`).

**The endpoint.** §4 counts as not correct a truth body with no detection, a detected body with no name, an abstention
or low-margin stop, and a frame without an anchor. The detectors that will be used are fixed in `slurm/fig6_eval.sh`:

- the keypoint body detector `detect_v5z_final`;
- the sacrum anchors `rx_lodo_cobra_elekta_1024` (T2, COBRA2026) and `rx_lodo_carmlspine_1024` (T3, C-ArmLSpine).

On development data, these are:

| Development measurement | Result | Key |
|---|---|---|
| §4 endpoint on ordinary C-ArmLSpine frames with ≥ 4 agreed bodies: anchored at 0.74, every named body boxed, every name right (case-grouped fine-tuned classifier) | **162 of 284 frames (57.0 %; 50.4, 63.4)**. Lateral 68/142 (47.9 %); AP 94/142 (66.2 %). Failures: no anchor 55, a body not boxed 66, **a name wrong 1** | `S11` |
| The same, with the prototype's per-body abstention counted as §4 "abstention" | **54 of 284 (19.0 %; 14.1, 24.3)** | `S11.also_no_abstention` |
| COBRA2026 sacrum found by the T2 anchor (COBRA never seen) at 0.74 | **21 of 609 frames (3.4 %; 1.3, 5.9)**. 22 sacrum boxes over 648 frames. **19 of 27 patients have no frame with the sacrum found.** At 0.25: 81/609 (13.3 %); 9 of 27 have none | `S12` |
| C-ArmLSpine sacrum found by the T3 anchor at 0.74 | 43 of 56 (76.8 %) | `S12` |

**What follows.**

- Every candidate real-frame at-risk person is a COBRA2026 patient (the 57 supported calls). On COBRA2026 the primary
  configuration is correct at most on the frames it anchors, about 3.4 %. H1 (82.2 %) and H2 (97.6 %) will therefore
  not be rejected, whatever the network's naming ability.
- For H6 (ordinary spines, non-inferiority at 92.6 %), at most 51 real-frame test persons exist: COBRA2026 41 and
  C-ArmLSpine 10 (`S3`). At 51 persons no error is allowed.
- An illustrative expected accuracy is 0.14. That is 41 persons × 3.4 % plus 10 × 57.0 %, over 51 (`S12`). Power
  is 0.
- Naming failed on 1 of 284 frames. The endpoint is decided by detection, anchoring and abstention. **The manuscript
  must say so.** Otherwise a Figure 6 "not rejected" will be read as a naming failure, and the 95 % power statement
  will be read as a plausible expectation.

**Correction (manuscript).** methods.tex:103–106. Replace "Transitional power is exact binomial enumeration against
the frozen values at a planning accuracy of 95\,\%: … at 708 (Figure~\ref{fig:power}b)." with:

> Transitional power is exact binomial enumeration against the frozen values at an assumed accuracy of 95\,\%,
> which no transitional measurement supports: against 82.2\,\%, 80\,\% power needs 55 at-risk persons (71 at the
> Holm step of three hypotheses); against 97.6\,\% power stays below 0.1\,\% at any size, and at a true 99\,\% it
> first reaches 80\,\% at 708 (Figure~\ref{fig:power}b). The frozen endpoint also fails a person for a missed body,
> an unanchored frame or an abstention; on ordinary development frames it held on 162 of 284 (57.0\,\%) before
> abstentions, and the frozen sacrum detector anchored 21 of 609 COBRA2026 frames (3.4\,\%).

Words: +47. Source: `results/stats_review2/recompute.json#S11_frozen_endpoint_on_ordinary_development_frames/both_views`
and `#S12_anchor_on_test_devices/cobra_at_074`. Add both to NUMBERS.md.

**Correction (before unblinding; the author's decision, not the manuscript's).** See §5, U1 and U2. §9 of the frozen
file allows a change only by a new commit, made before unblinding, that lists the old value, the new value and the
reason; the manuscript then reports both. I do not choose among the options:

- keep the plan as frozen and report the bound above;
- clarify what "abstention" means in §4;
- use a sacrum anchor for COBRA2026 trained on G3-train COBRA persons, which is person-disjoint but not
  device-held-out;
- move the anchor requirement to a secondary analysis.

Any of these must be committed before `RELEASE_v2.json` exists.

### N2. Fine-tuned results carried into sentences about the device the network never saw. **FAIL** (substantive)

| Field (lateral) | Zero-shot | Case-grouped fine-tuned | Day-grouped fine-tuned | Key |
|---|---|---|---|---|
| whole frame | 594/617 = 96.3 % | 606 = 98.2 % | 571 = 92.5 % | `S5.kfull` |
| three in view | **1,010/1,162 = 86.9 % (83.1, 90.3)** | 1,079 = 92.9 % (89.6, 95.6) | **1,018 = 87.6 % (83.3, 91.6)** | `S5.k3` |
| one in view | **381/604 = 63.1 % (58.5, 67.6)** | 440 = 72.8 % (69.0, 76.2) | **402 = 66.6 % (62.6, 70.6)** | `S5.k1` |

The coupling analysis (993/979/995 of 1,009) uses the case-grouped fold models, with AP and lateral frames pooled
(`coupling.json` `classifier_exact` 1,216/1,248 = 606 + 610).

- discussion_motivation.tex:11–13 reads "Never shown the intraoperative C-arm, it named … 92.9 % with three bodies in
  view …; coupling … was exact on 98.6 %". Both numbers are fine-tuned.
- discussion_motivation.tex:29–30, "here three sufficed for 92.9 %", compares a fine-tuned figure with registration-free
  prior work.
- Key Point 2 follows Key Point 1's "Never trained on the intraoperative C-arm" with the fine-tuned 92.9 %.
- The day-grouped figures for field size exist (a9.json; the Markdown twin of Table 4) but are not in the text.

**Corrections.**

- discussion_motivation.tex:11–13: "and 92.9\,\% with three bodies in view and no sacrum to count from; coupling shape
  to a count from the detected sacrum was exact on 98.6\,\% of anchored bodies." becomes "and 86.9\,\% with three
  bodies in view and no sacrum to count from; fine-tuned, shape alone was exact on 98.4\,\% of anchored bodies and
  shape coupled with the count on 98.6\,\%." (+2)
- discussion_motivation.tex:30: "here three sufficed for 92.9\,\% on ordinary spines." becomes "here three sufficed
  for 86.9\,\% on ordinary spines without fine-tuning." (+2)
- results.tex:49–50: "it named 92.9\,\% (1,079 of 1,162; 89.6, 95.6); with one, 72.8\,\% (440 of 604)" becomes "it
  named 92.9\,\% (1,079 of 1,162; 89.6, 95.6; day-grouped 87.6\,\%; zero-shot 86.9\,\%); with one, 72.8\,\% (440 of
  604; zero-shot 63.1\,\%)". (+6)
- Key Point 2 (main.tex:56) becomes: "\item With three vertebrae in view and no sacrum to count from, it named 1,010
  of 1,162 exactly (86.9\,\%), and 1,079 (92.9\,\%) once fine-tuned; on frames with a detected sacrum, counting named
  979 of 1,009 bodies (97.0\,\%), the fine-tuned shape classifier 993 (98.4\,\%) and the two coupled 995 (98.6\,\%)."
- Table 4: add the row "no C-ArmLSpine frame in training | lateral; three in field | exact level | 86.9 (1,010/1,162)
  | 142 (45) | [83.1, 90.3] | [82.9, 90.1]". Source: `a7.json#cells/zeroshot2~1det~1LAT~1k3`.
- Table 4 footnote d: append "Classifier = the case-grouped fine-tuned fold models; AP and lateral frames pooled."
- Figure 4 (owner): panel (b) draws the case-grouped 1,079/1,162 (`figure4.record.json`), under a caption that begins
  "boxed by detectors never trained on this C-arm". The caption should say that the level model in (b) was
  fine-tuned. This needs 2 words at the 60-word limit, so another word must be trimmed.

### N3. Coupling: the gain over the count is three cases, and there is no gain over shape. **FAIL** (substantive)

**Recomputed per case from the fold files** (`S6.per_case_sign_tests`, 130 cases, 1,009 bodies):

- Coupled against count: **3 cases better, 0 worse, 127 tied; exact sign test P = .25.**
- The 16 bodies of difference (995 − 979) are exactly the 16 bodies on the four frames called L6 (cases 106, 139 and
  44). The count was wrong on all 16 and the coupled call right on all 16 (`coupling.json` `non_ordinary_calls`).
  So the whole of the coupling's measured advantage over counting comes from a false L6 alphabet call on five-lumbar
  spines that happened to repair a miscount. The Results report those four frames as L6 calls "each with a stop".
- Coupled against classifier: **3 better, 3 worse; P = 1.0.** The transitions are 13 corrected and 11 introduced.
- On all 1,248 scored bodies (anchored or not):
  - coupled 1,218 (97.6 %; 95.8, 99.1);
  - classifier 1,216 (97.4 %);
  - count 979 (78.4 %), because the count names nothing on unanchored frames.

**Corrections.**

- results.tex:50–55, from "At confidence 0.74, on 1,009 bodies" to "unflagged bodies." becomes:

  > At confidence 0.74, on the 1,009 bodies of anchored frames (130 cases) the count was exact on 97.0\,\% (979;
  > 94.2, 99.2), the case-grouped classifier on 98.4\,\% (993) and the coupled call on 98.6\,\% (995), 1.6 points
  > above the count (0.0, 3.8; all on the four frames called L6 below, $P=.25$) and 0.2 above the classifier
  > ($-1.7$, 2.1) (Figure~\ref{fig:exposure}c); the mechanisms disagreed on 12 of 233 anchored frames (5.2\,\%), the
  > stop signal fired on 22 (9.4\,\%), on four of five frames with an error and 17 of 225 without, and the coupled
  > call was exact on 921 of 922 unflagged bodies.

  Words: +23. Sources: `coupling.json#cells/det74~1kfull/coupled_minus_classifier_anchored`, `#flags`, and
  `S6.per_case_sign_tests.coupled_vs_count`.
- Abstract and Key Point 2: add the classifier alone. The text is in the abstract rewrite below and in N2.

### N4. The stop signal: definition and denominators. **FAIL**

- The Methods (methods.tex:70) define the stop as "a classifier name differing from the call".
- The tool (`coupling.json#definitions`, `#flags.reasons`) stops on any of four reasons:
  - disagreement (12 frames);
  - a margin below a threshold cross-fitted on the other folds (10);
  - no anchor (54);
  - no vertebra (3).
- Table 4 labels "disagreement frames (the stop signal) 5.2 (12/233)". The stop actually fired on 22 of 233 anchored
  frames (9.4 %; 5.6, 13.9) and on 79 of all 290 frames (27.2 %; 21.4, 33.5).
- The sensitivity of four of five rests on five frames: Wilson 37.6–96.4 (`S6.flags`).

**Corrections.**

- methods.tex:70: "a classifier name differing from the call stops the read." becomes "a classifier name differing
  from the call, or a low margin, stops the read." (+4)
- The Results replacement in N3 gives "fired on 22 (9.4 %)".
- Table 4:
  - relabel the row as "disagreement frames";
  - add "stop signal (disagreement or low margin), anchored frames | 9.4 (22/233) | 132 | [5.6, 13.9]";
  - add "stop signal, all frames (no anchor stops the read) | 27.2 (79/290) | 145 | [21.4, 33.5]".
  Sources: `coupling.json#cells/det74~1kfull/flags/frames_flagged_anchored` and `frames_flagged_all`.
- If the text keeps "four of five", add "(Wilson 37.6, 96.4)" (+3, optional).

### N5. L6 sensitivity reported without false positives. **FAIL**

- `figure2_metrics.json#validation_neighbours_and_calls`: the classifier called 75 of 98 L6 crops L6 (76.5 %;
  person-cluster 59.5, 94.4; ten persons).
- It also called 111 of 1,012 L5 crops L6 (11.0 %).
- Among L5 and L6 crops, where L6 is 8.8 %, an L6 call was right in 75 of 186 (40.3 %) (`S7`).
- The journal requires numerators and denominators for sensitivity, specificity and predictive values.
- **Correction** (with N6a below): add "and 111 of 1,012 L5 crops L6".

### N6. Figure 2: comparisons, small-cluster intervals, single crops. **FAIL** (wording)

- **(a) "More than any lumbar level from the one above" (results.tex:30–31).**
  - The range 0.16–0.23 leaves out L1 from T12: 0.32 (0.29, 0.35), which overlaps L6 from L5 (0.31, 0.39).
  - L6|L5 − L1|T12 = 0.026, approximately −0.022 to 0.074.
  - L6|L5 − L5|L4 = 0.122 (0.078, 0.166).
  - Both differences use a normal approximation from the printed percentile intervals over independent persons
    (`S7`). They are descriptive; per-crop values are on the grid only.
  - The Discussion's "more than ordinary neighbours from each other" (discussion_motivation.tex:16) is therefore
    true of lumbar neighbours only.
- **(b) Ten persons.** The L6 intervals resample ten persons. The same undercoverage as F5 applies. A t(9)
  correction widens the interval by about 1.22, giving L6|L5 0.30–0.40 and a difference from L5|L4 of 0.070–0.173.
  The conclusion survives, but the interval is descriptive.
- **(c) The fused L5.** The two negative values (−0.13, −0.18) are each a single crop (`figure2.record.json`
  per_person).
- **(d) Occlusion.** "Concentrated on the target body at every level" quotes the sacrum (4.51). For L5 the target
  (1.39; 1.15, 1.63) and the body below (1.26; 1.09, 1.45) overlap. No paired interval can be computed from the saved
  summaries.

**Corrections.**

- results.tex:30–32: "than any lumbar level from the one above (0.16--0.23; L5 from L4, 0.23; 0.21, 0.25), and the
  classifier named 75 of 98 L6 crops L6;" becomes "than any lumbar level from the one above (0.16--0.23; L5 from L4,
  0.23; 0.21, 0.25) but not than L1 from T12 (0.32; 0.29, 0.35); the classifier named 75 of 98 L6 crops L6 and 111 of
  1,012 L5 crops L6;" (+15).
- discussion_motivation.tex:16: "ordinary neighbours" becomes "ordinary lumbar neighbours" (+1).
- If the fused-L5 sentence stays (see cut C2 in §6), results.tex:37 becomes "($-0.13$, $-0.18$, one crop each; ordinary
  L4, 0.24, 70 of 1,066 crops below zero)" (+3).
- Optional (+4): results.tex:39 becomes "Occlusion enrichment was highest on the target body at every level (L4--L6,
  1.39--1.69; sacrum, 4.51; ten crops each)".
- Figure 2 caption (owner, optional): "(c) Silhouette; CI, confidence interval; ten L6 persons."

### N7. The 57 COBRA2026 calls and their best case. **FAIL** (substantive, wording)

**The labeller's measured positive predictive value** (`results/spineps_ids/IMPACT.md` §5; TS12_VERIFY.md):

| Call | Where measured | Result | Wilson 95 % |
|---|---|---|---|
| L6 | CTSpinoPelvic1K | 10 of 24 | 24.5–61.2 |
| **T13** | **CTSpinoPelvic1K** | **0 of 52** | **0–6.9** |
| L6 | VerSe | 34 of 42 | 66.7–90.0 |
| T13 | TotalSegmentator | 1 of 3 | 6.1–79.2 |

- COBRA2026 is abdominopelvic planning CT. In coverage it is closer to CTSpinoPelvic1K than to VerSe.
- 38 of the 57 supported calls are T13.
- Illustration only (`S4.scenarios`): confirmation is not the same as eligibility or at-risk membership, and both of
  those can only lower the count further. The probability that at least 19 of the 57 are confirmed is:
  - **0.00007** at the CTSpinoPelvic1K point values, with every four-lumbar call confirmed;
  - **0.30** at their upper Wilson limits;
  - **0.9999** only at the VerSe L6 and TotalSegmentator T13 values.
- The Results print the 10 of 24 in the phenotype paragraph and the 93.7 % best case in another, and never connect
  them. The Figure 5 record notes the L6 PPV but not the 0 of 52.
- The pooled 57 CT test persons include up to six sacralised L5 that keep their own label. The frozen rule counts
  those as naming unaffected, not at risk (figure5.record.json `discrepancies_stated`).

**Corrections.**

- results.tex:64–65: "(L6 11, T13 38, four-lumbar eight); if all 57" becomes "(L6 11, T13 38, four-lumbar eight),
  though on CTSpinoPelvic1K the labeller's L6 calls matched readers in 10 of 24 and its T13 calls in none of 52; if
  all 57" (+21).
- results.tex:25–26: "; on CTSpinoPelvic1K its L6 call matched the readers in 10 of 24." becomes "." This removes
  the duplicate (−12).
- Table 2 footnote e: after "matched the readers in 10 of 24" add "and its T13 call in 0 of 52".
- Table 2 footnote f: append "the pooled CT count includes up to six sacralised L5 keeping their own label, which the
  frozen rule counts as naming unaffected".

### N8. H6 feasibility, and the embedding in the abstract. **FAIL** (minor)

- **(a) H6.** The built split holds at most 51 ordinary real-frame test persons (COBRA2026 41, C-ArmLSpine 10;
  `S3`) against `n_min` 48.
  - At 51, the test passes only with no error.
  - Power is 0.07, 0.21, 0.36 and 0.60 at true accuracies of 95, 97, 98 and 99 %, before N1.
  - LEVELCHECK_MODEL.md §7's "145 persons" row no longer describes the design.
  - **Correction:** Table 3 footnote d: append "the built split holds at most 51 ordinary real-frame test persons
    (COBRA2026 41, C-ArmLSpine 10), so H6 passes only without error".
- **(b) The embedding.** The abstract's first Results sentence and Key Point 3 present the silhouette without saying
  that it comes from the split that chose the checkpoint. The Results, Methods and Limitations do say so. The
  corrections are in the abstract rewrite and in Key Point 3 below.

### N9. The Holm family carries the fold-level card test. **FAIL** (minor; supplement)

- The fourth member of the family is the card comparison, tested over 24 folds. F6 established that the device is the
  unit, and at the device level the exact sign-flip test gives P = .125.
- With that member, the Holm-adjusted P values become (`S8`):
  - lateral against AP, 1.0e−22;
  - film against render, 7.2e−7;
  - **same-device against held-out sacrum, .016 (printed .008)**;
  - card, .13.
- **Correction** (supplement "Which source carries the detector"): "Holm-adjusted exact sign test $P=.008$" becomes
  "$P=.016$". In "Image-formation terms", say that the device-level P = .13 is the Holm member.

### N10. The comparator is a constant; say so. **FAIL** (minor)

- The frozen values are literature estimates, and the test ignores their sampling error.
- This is stated in `power.json#what` but not in the manuscript.
- Sensitivity illustration (`S9`), assuming Peh's 82.2 % is 106 of 129 patients (the abstract gives no numerator):
  - the Wilson interval is 74.7–87.8 %;
  - at the upper limit, `n_min` would be 29 rather than 19;
  - power at 55 persons would fall to 0.23.
- **Correction** (Table 3 footnote c, no body words): append "The frozen values are fixed constants; their own sampling
  error is not modelled."

### N11. "Needs 19" is a minimum. **FAIL** (minor)

- 19 is `n_min` at α = 0.025. Under Holm, the first step needs 23, 25 or 28 for two, three or six eligible
  hypotheses.
- Needing 19 is necessary, not sufficient: power at 19 is 0.38 at a true 95 %.
- **Corrections:**
  - results.tex:62: "exact test needs 19 at-risk" becomes "exact test needs at least 19 at-risk" (+2).
  - discussion_limits.tex:14: "that needs 19 verified" becomes "that needs at least 19 verified" (+2).
  - Abstract and Key Point 3: "152 error-free persons" becomes "152 error-free at-risk persons".

### N12. "Count-changing" and the two decision rules. **FAIL** (minor; carried over from F17)

- methods.tex:84–85 applies the pre-stated Wilson targets to "pooled count-changing test persons". That term is not
  defined in the manuscript and is not the frozen "at risk".
- The targets are a second decision rule on the same persons, outside the Holm family.
- **Correction:** "The pre-stated transitional criteria are … on pooled count-changing test persons
  (Figure~\ref{fig:power})." becomes "The pre-stated transitional targets, Wilson 95\,\% lower bounds of 90\,\% for the
  exact level and 85\,\% for variant sensitivity on pooled at-risk test persons, sit outside the frozen tests'
  multiplicity control (Figure~\ref{fig:power})." (+6)

### N13. Significance level. **Minor.**

- methods.tex:111–112 says "significance was two-sided $P<.05$". The frozen tests are one-sided at .025, as the
  paragraph above states.
- Optional (+6): "…two-sided $P<.05$, one-sided .025 for the frozen comparison."

### N14. Percentages without numerators (check_limits warnings). **FAIL** (minor)

- results.tex:30: "74.9\,\% (95\,\% confidence interval [CI]: 72.2, 77.6)" becomes "9,740 (74.9\,\%; 95\,\% confidence
  interval [CI]: 72.2, 77.6)" (+1).
- results.tex:38: "6.6\,\% of 1,066 crops" becomes "70 of 1,066 crops" (0).
- Source: `S7`.

### N15. Sacrum denominator. **FAIL** (minor)

- results.tex:43–44 gives "the sacrum on 233 of 290 frames (80.3 %)". Four of the 290 frames show no sacrum, and no
  frame without one was anchored (`coupling.json` `frames_anchored_no_truth_sacrum` 0).
- **Correction:** "233 of 286 frames showing one (81.5\,\%)" (+2).

### N16. "Fixed before unblinding" needs the commits. **CONDITIONAL**

- methods.tex:98–100 and Table 3 footnote c: the ImageNet initialisation and the configuration are in the untracked
  `results/fig6/RUN_v2.json` and `slurm/fig6_eval.sh`.
- methods.tex:43–46: the automated-reference rule is not yet frozen (`results/auto_reference/` holds `readerC/` only).
- Both sentences become true once the G5 manifest and `auto_reference.json` (with SHA-256) are committed before
  `RELEASE_v2.json`. If that order is not kept, the wording must change to "was fixed by commit on <date>", or the
  analysis is reported as not pre-specified (§9).
- See U3 in §5 for the open gate.

### N17. Software. **Minor** (F19 residual)

- methods.tex:112–114: "Python 3.11 … SciPy 1.15.3" becomes "Python 3.11 and 3.12 … SciPy 1.15.3 and 1.18.1
  (power)".
- Name the revision of the rigor tool (6e1cf8d).
- If numbers from this review enter the text, add `stats_review2_recompute.py`.

### N18. Lower limits of 0 despite successes (Table S2). **Minor** (the mirror of F3)

- "0.3 (1/287) [0.0, 1.1]" becomes "[0.1, 1.9]$^g$".
- "5.4 (3/56) [0.0, 12.5]" becomes "[1.8, 14.6]$^g$".
- Footnote g: "where the percentile one reached 100 % with errors" becomes "where the percentile one reached 0 or 100 %
  against the data". Source: `S10`, unclustered Wilson.

### N19. The abstract's interval label. **Minor**

- "Intervals: clustered bootstraps" is not accurate: the headline interval (92.0, 98.3) is a design-effect-adjusted
  Wilson interval.
- It is fixed in the abstract rewrite ("Intervals were cluster-adjusted").

### N20. Abstract: "594 of 617 lateral vertebrae". **Minor** (F9 residual)

- Add "detected". This is included in the abstract rewrite.

### N21. The never-seen "L6" patients: crops are not persons. **Note**

- "84 of its 180 crops" are the crops of three patients under six device cards. The effective sample is 3.
- The negative L3–L5 values (−0.09 to −0.01) are what the TotalSegmentator reading (L2–L4) predicts. So the panel
  does not discriminate between the two readings, apart from the disputed body.
- Cut C1 below shortens the sentence accordingly.

### The abstract rewrite (N3, N7, N8b, N11, N19, N20)

**Results** (main.tex:69). Replace everything up to "The LevelCheck comparison is" with:

> On the checkpoint-selection split, the sixth lumbar vertebra separated from the fifth (silhouette 0.35; 95\,\%
> confidence interval [CI]: 0.31, 0.39) more than the fifth from the fourth (0.23; 0.21, 0.25). Zero-shot, the
> network named 594 of 617 detected lateral vertebrae (96.3\,\%; 92.0, 98.3) and 239 of 631 anteroposterior
> (37.9\,\%; $P<.001$); fine-tuned, 606 (98.2\,\%) case-grouped and 571 (92.5\,\%) day-grouped, and with three bodies
> in view 1,079 of 1,162 (92.9\,\%); on anchored frames the count named 979 of 1,009 (97.0\,\%), the classifier 993,
> the coupled call 995 (98.6\,\%). No real-exposure transitional test person was verified; 57 unread screen calls, if
> confirmed, allow a best-case bound of 93.7\,\%; exceeding 97.6\,\% needs 152 error-free at-risk persons.

This adds 10 words.

**Materials and Methods** (main.tex:67):

- "A residual encoder (embedding measured by silhouette) and recurrent head" becomes "A residual encoder and recurrent
  head".
- "Wilson bounds and exact binomial power set transitional sample size;" becomes "Exact binomial power set transitional
  sample size;".
- "Intervals: clustered bootstraps; $P$ values: Holm-adjusted exact tests." becomes "Intervals were cluster-adjusted;
  $P$ values, Holm-adjusted exact tests."

This removes 7 words.

**Conclusion** (main.tex:71): "awaits verified transitional exposures" becomes "awaits verified exposures", removing
1 word.

**Net +2, so the abstract comes to 250 of 250.**

**Key Point 3** (main.tex:57) becomes: "\item On the split that chose its checkpoint, its embedding separated the sixth
lumbar vertebra from the fifth (silhouette 0.35; 10 persons) more than the fifth from the fourth (0.23); no
real-exposure transitional test person is yet verified, and exceeding the published 97.6\,\% accuracy of surgeons
using registration needs at least 152 error-free at-risk transitional persons."

---

## 5. Before unblinding (time-sensitive; for the author and the Figure 6 owner, not the manuscript)

- **U1. COBRA2026 anchoring (N1).**
  - As frozen, H1 and H6 are decided by a sacrum detector that finds the COBRA2026 sacrum on 3.4 % of frames.
  - The file permits a documented pre-unblinding change (§9); after unblinding nothing can change.
  - Decide before `RELEASE_v2.json` is written.
- **U2. "Abstention" in §4 is ambiguous.** It could mean the prototype's per-body abstain flag (development endpoint
  19.0 %) or only the coupled call's low-margin stop (up to 57.0 %). Fix it by a clarifying commit before unblinding,
  or the scorer's choice becomes an analysis decision made after the fact.
- **U3. The open gate scores the H6 stratum before the configuration is committed.**
  - `slurm/fig6_eval.sh` with `GATE=open` (job 40429882, chained afterany on the heads) scores the frames of
    ordinary G3 test persons, and those persons are H6.
  - It does so before the G5 manifest is committed; the heads job writes only `G5_MANIFEST_v2.draft.json`.
  - §9's definition of unblinding covers transitional strata only, so this is allowed by the letter of the file. But
    §4 says "No configuration, checkpoint, threshold or seed is chosen on test persons".
  - **Commit the draft manifest and `slurm/fig6_*.sh` before anyone reads `fig6_score_open.json`**, or report H6 as
    analysed after its data were seen.
- **U4. The automated reference.** Freeze `results/fig6/frozen/auto_reference.json`, with its SHA-256, before any
  test person is scored (§14 R2). Only reader C exists locally.

---

## 6. Word budget

**Body, required corrections.** Measured with `check_limits.words()` on each old/new pair.

| Correction | Words |
|---|---|
| N1 | +47 |
| N4 | +4 |
| N12 | +6 |
| N14 | +1 |
| N5/N6a | +15 |
| N15 | +2 |
| N2 (Results) | +6 |
| N3 | +23 |
| N7 | +21 −12 |
| N11 | +2 +2 |
| N2 (Discussion) | +2 +2 |
| N6 (Discussion) | +1 |
| **Total** | **+122** |

N6b (+3) is dropped if cut C2 is taken.

**Cut menu.** The body is at 2,985, with 15 words spare. Each cut below removes an analysis the statistics do not
support at the length it is given.

| Cut | Where | Replacement text | Words |
|---|---|---|---|
| C1 | results.tex:33–36, the never-seen patients (N21; three patients, contested truth, the effect vanishes under the second box convention) | "In three never-seen patients whose sixth lumbar vertebra only one labeller reads, the disputed body sat nearer the L6 than the L5 cluster (0.10--0.16) under whole-vertebra boxes only." | −29 |
| C2 | results.tex:36–38, the fused L5 (four persons, single crops; the record itself says four persons "cannot separate a junction effect from a person-level shift") | "Four validation persons with a fused L5 (one to five crops each) could not separate a junction effect from a person-level shift." | −29 |
| C3 | discussion_motivation.tex:17–20 | "The evidence is thin: ten validation persons on a split that chose the checkpoint, an order reversed within one render source, and a disputed L6 in three never-seen patients." | −28 |
| C4 | methods.tex:56–57, the fused-L5 method, if C2 is taken | "Validation persons with a fused, unlabelled L5 were read the same way, their L3 as control." | −21 |
| C8 | results.tex:61, the Wilson sample sizes, which Figure 5a and Table 2 footnote f already carry | Drop "a Wilson lower bound of 90\,\% needs 35 test persons and one above 97.6\,\% needs 157; the frozen", so the sentence reads "With no error, the frozen exact test needs at least 19 …" | −16 |
| **Total** | | | **−123** |

**Net about −1, giving about 2,984 of 3,000.** Optional additions (N4 Wilson +3, N6 occlusion +4, N13 +6) fit only
with further cuts. The coordinator makes the final choice and re-runs `tools/check_limits.py`.

**Words not counted.** The tables, Key Points and captions carry the rest: Table 2 footnotes e and f; Table 3
footnotes c and d; Table 4 rows and footnote d; Table S2; the supplement's Holm P; the Figure 4 caption.

---

## 7. Items that pass (new or re-checked)

| # | What passes |
|---|---|
| P1 | Every number in the abstract, Key Points, Results and Tables 2–4 traces to its file. The recomputed numerators check: 571 = round(0.92545 × 617), 1,018, 402, 9,740, 70, 111, 75. `S5`, `S7` and the earlier recompute.json agree with the printed values. |
| P2 | The power arithmetic is exact (§2). |
| P3 | The frozen plan is transcribed faithfully into Table 3 (§3). |
| P4 | Paired comparisons are analysed as paired. The one new comparison added here (N3) is an exact sign test over cases. |
| P5 | "Significant" is not used without a test. |
| P6 | The pre-stated counting grade (97 %) and the card criterion are reported as not met. |
| P7 | The three real C-ArmLSpine L6 patients are described as "agreement with one reading, not correctness", consistently. |
| P8 | The case-cluster caveat (F15) is in the Limitations. |
| P9 | The frozen `n_min` table of §5 reproduces cell for cell (`S1.n_min`). |

---

## 8. What the corrections do to the claims

**Held without change:**

- the zero-shot lateral result (96.3 % of detected, 87.9 % of all agreed);
- the lateral against AP contrast;
- the detector result;
- the arithmetic of every sample-size and power number.

**Weakened, and to be said:**

- Naming with three bodies in view on an unseen device is 86.9 %, not 92.9 % (N2).
- Coupling adds nothing measurable over shape alone. Its gain over counting is four frames in three cases, all false
  L6 alphabets (N3).
- The L6 call is right in about 40 % of the L5/L6 crops it names L6 (N5).
- L6 separates from L5 about as much as L1 from T12 (N6).
- The best-case 93.7 % rests mostly on T13 calls whose measured positive predictive value is 0 of 52 (N7).

**Changed in kind (N1).** As frozen, the Figure 6 comparison is expected to fail on detection, anchoring and
abstention, not on naming. The paper must say this in the Methods now. Whether to amend the plan before unblinding is
the author's decision (§5).

**New numbers.** Every number this review proposes is either in `results/stats_review2/recompute.json` (keys S1–S12)
or already in `a4.json`, `a7.json`, `a9.json`, `coupling.json`, `figure2_metrics.json`, `power.json`,
`fig3_detection/scored/*.json`, `results/fig6/frozen/v1/FROZEN.md` or `results/spineps_ids/IMPACT.md`. Each needs a
NUMBERS.md row when it enters the manuscript.
