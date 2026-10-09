# Paper 1 scope rule (SchwingNet manuscript, `SchwingNet/main.tex`)

Set 2026-09-24 (evening) on Greg's instruction: "I'd like to move the comparison to neurosurgeons / all the
LevelCheck stuff into a new paper, remove it from the current paper" — "you take care of this". Paper 2 is the
LevelCheck / surgeon comparison; its material lives in `paper2_levelcheck/` (`MOVED_FROM_PAPER1.md`,
`numbers_manifest_moved.json`, `tables/tab_levelcheck.*`) and its pre-specification is `LEVELCHECK_MODEL.md`
sections 1-15, **frozen and untouched** (last commit d0403de).

## What paper 1 reports

1. **Cross-validation and checkpoint-selection results.** The embedding on the encoder's selection split
   (Figure 2); C-ArmLSpine naming zero-shot and by case- and day-grouped folds; the count from the detected sacrum;
   the coupled call and its stop signal; the L6 calls at confidence 0.74 (Figure 4, Table 3 = `tab3_naming.tex`,
   Results "Naming, counting and coupling on the intraoperative C-arm").
2. **The unseen-C-arm test already in the manifest / result files** (`results/eval_gate/leaks/zeroshot_v9.json`,
   `results/eval_gate/closure/cv_v9/`, `results/a1.json`, the same-device learning curve, Table S2, Figures S3-S5).
3. **The open-gate ordinary-person real-frame results, if they land** (COBRA2026 ordinary persons against the
   automated reference). Amended in the fill pass of 2026-09-24 (evening): because no result paper 1 prints rests
   on the automated reference, its supplement paragraph, its `\PENDING{G6}` calibration, the pre-registration
   paragraph, the Methods sentence and the Discussion sentence moved to `paper2_levelcheck/MOVED_FROM_PAPER1.md`
   item 8, where the paragraph is also given filled from the frozen file (`autoref_*` keys in
   `numbers_manifest_moved.json`); if an ordinary-person real-frame result is printed here, those passages return
   from there with it. *Caution recorded here for paper 2's ledger:* those persons are the ordinary stratum of paper 2's
   H6 (non-inferiority at 92.6 %, LEVELCHECK_MODEL.md s3). If paper 1 prints an ordinary-person real-frame accuracy,
   paper 2 must record that H6's stratum was seen before its unblinding; H1-H5 (transitional strata) are unaffected.
   `LEVELCHECK_MODEL.md` is frozen, so the record goes in paper 2's own log, not there.
4. **The data case.** Transitional persons per subtype and source (Table 2), the built person-disjoint split, the
   persons available against the pre-stated Wilson targets (Figure 5a, c, d; Results "Transitional sample size"),
   and the `\PENDING{G5}` data-case paragraph (naming and detection against same-device count and acquisition-space
   coverage; plain-film versus fluoroscopy N curve).

## What paper 1 does NOT do

**No G3 test transitional person is scored or reported in paper 1**, with one already-pre-specified exception:

- The three C-ArmLSpine L6 patients (real, on the test side of the built split by construction) appear in paper 1
  only as cross-validation outputs — agreement with one labeller's read on one of five bodies, one L6 call on four
  anchored frames, their crops' position in the embedding — and `LEVELCHECK_MODEL.md` s4 already excludes them
  from paper 2's primary analysis in advance because those outputs were seen before the freeze. Paper 1 says in the
  Discussion that this is a description, not a test of transitional naming.
- No COBRA2026 transitional candidate (the seven at-risk persons with an exported frame; the 91 screen calls) and
  no CT test person of the split (the 51 at-risk CT test persons) is scored in paper 1. They enter only as counts
  (Table 2, Figure 5c, d).
- No model is scored in paper 1 on the test side of the built split: the split-trained arm (encoder from ImageNet
  weights on the split's training persons) appears only through its development learning curve on the validation
  side (supplement "Development learning curve of a split-trained level model").
- Paper 1 quotes no modelled LevelCheck accuracy (82.2 %, 97.6 %, 92.6 %), no exact-test n (19, 152), no
  hypothesis H1-H6 and no secondary analysis of s12-s13 (M1 McNemar, F1 flag with tau, D1 dual-loss arm, S1
  selective accuracy). Its sample-size statements are the pre-stated Wilson targets (90 % exact level, 85 %
  variant sensitivity: 35 persons and 22 carriers with no error).

Therefore `LEVELCHECK_MODEL.md` s1-s15 and the blinded gate (f6eval jobs held; `results/fig6/HOLD_README.txt`)
stay valid for paper 2: nothing paper 1 prints touches a transitional test person's held-out score.

## The seven things that moved (detail in `paper2_levelcheck/MOVED_FROM_PAPER1.md`)

1. Results paragraph "The LevelCheck comparison" (`\PENDING{G6}` per-stratum result) and the exact-test sentence of
   "Transitional sample size".
2. Figure 6 (`\PENDINGFIG{figures/figure6.pdf}` + caption) and manifest keys `figures.figure6`,
   `fig6_h1_coupled_accuracy_pct`.
3. Table 3 = `tables/tab_levelcheck.tex` (+ `.md`, `.sources.md`; now `paper2_levelcheck/tables/`), its `\input`,
   and the Table 4 row that owed the G6 per-stratum result.
4. Figure 5 panel (b) and the 19 / 152 verticals of (c) (PDF not rebuilt: `fig_power.py` stops by design now that
   `results/fig6/frozen/auto_reference.json` exists; panel (a) stays, re-captioned as persons to certify an
   accuracy) and manifest keys `power_n_min_h1_822`, `power_n_min_h2_976`, `power_n_min_g6_level_90`.
5. Methods paragraph "The LevelCheck comparison" (comparator, strata, unit, s15 detector, s12-s13 secondary
   analyses), the power sentence of "Statistical analysis" and the one-sided .025 clause.
6. Discussion paragraph 3 (seven LevelCheck mentions) and the comparison clauses of the limitations and summary.
7. The "Registration" sentence on the frozen comparator, the Introduction's fourth aim, the abstract's four
   comparison clauses, the summary-statement and key-point clauses, and the title clause "versus
   registration-assisted neurosurgeons".

Stayed, on purpose: the Introduction's prior-art sentences on LevelCheck (`levelcheck2012`, `levelcheck2016`,
`desilva2016`, `manbachi2018`, `peh1999`) — they motivate the problem; the coupled call, the count and the stop
signal as paper 1's own cross-validation results. (The supplement's automated-reference paragraph stayed until the
fill pass of 2026-09-24 and then moved as item 8: no printed result uses it.)

## Standing rules while paper 2 is pending

- Do not edit `LEVELCHECK_MODEL.md`. Do not release or touch the held f6eval jobs.
- Do not add any per-stratum transitional accuracy, any modelled LevelCheck value or any H1-H6 language to paper 1.
- A new paper-1 result on a person of the built split's test side needs a line here first saying which paper-2
  stratum it touches.
