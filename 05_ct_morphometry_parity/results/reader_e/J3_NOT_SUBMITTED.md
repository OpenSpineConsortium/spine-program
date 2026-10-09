# Reader E J3: not submitted (2026-09-25)

**Rule applied.** `docs/CT_LSTV_CLASSIFIER_PLAN.md` section 8: "If J2's spread check fails on any feature, J3 is not
submitted." J2 (job 40443310, `tools/reader_e_j2_gate.py` at 805331b, COMPLETED rc 0, 45 s, MaxRSS 252 MB, node mdt83)
ran once on the J1 flat table (38,432 instance rows, 3,524 pairs, five families) and returned `pass = false`
(`results/reader_e/j2/J2_GATE.md`, `j2_gate.json`). The renders passed; the numbers did not. No training script, no
Slurm script and no J3 job were written or submitted in this step. Nothing in the manuscript, `LEVELCHECK_MODEL.md` or
`results/fig6/` was touched.

## Failing features

| feature | verdict | worst cell | gate-passing SD | widest published SD | flagged share | what is wrong |
|---|---|---|---|---|---|---|
| SCD | **FAIL** | v11/L1 flagged 46 %, v11/T12 45 %, spineps L1/T12 41 % | 1.36-2.14 mm (after the range bit) | 3.76 (Griffith 2016 L5 M) | 11-46 % | 15.8 % of all J1 instances sit under the 11.07 mm floor against a published prevalence of 2.62 % (6.0x; window <= 2x). Among mask-passing values: v11 L1 20.0 %, L2 16.2 %, T12 16.5 %; spineps L1 14.8 %, T12 13.5 %; ts L1 9.5 %; outside the window at T11-L2 in every family and at L3 on v11/spineps, inside at L4/L5. Cause measured against the release's own `canal_ap`: ostk `canal_dimensions` reads its pedicle slab on `canal_mask`'s solid, which under the ostk 1b7005c ring closing carries the interlaminar pocket sections, so the midsagittal chord collapses onto a pocket wherever the closed-ring column is short (0234 L2-L4 12.0/10.1/12.1 vs 18.8/18.0/18.0; 0244 L2 11.6 vs 20.3; 1138 L1 9.0 vs 20.3) and on 78-100 % of fallback rows. |
| EPWl | **FAIL** | ts/L2 flagged 43 %, ts/L1 41 %; v11 33-36 % | 3.67-5.33 mm | 5.54 (Yadav 2020 L5 M, a superior-plate series) | 15-43 % | Half the flagged share is voids (fallback + plate + merged), half the atlas envelope: the lower plate reads 3-5 mm wider than the release atlas at every level in every family, and the atlas `endplate` row (and every published end-plate series on file, Bonczar L1 41.09) is the SUPERIOR plate. There is no lower-plate yardstick in `level_references.csv`, so EPWl is judged against the wrong plate. Under a published-centred envelope it is 25-26 %. |
| EPDu / EPDl | NO_YARDSTICK (cannot pass; not counted as failing) | ts/L2 flagged 26-27 % | 3.75-5.35 mm | none on file (the "3.5 mm" quoted in `J1_RERUN_AND_COLLECT.json` had no source and is withdrawn) | 6-27 % | The release atlas's own SD (4.9-6.4) carries the displaced ostk corner. |

Passing: VBHa, VBHp, EPWu, SCW (VBHp at L5 only on the published-centred envelope: the atlas row 30.4 sits 6 mm above
every published L5 posterior height, 24.1-25.7, while the gate-passing medians 26.3-26.4 sit inside them).
Rib-keyed cells (versefusion, no plateau): VBHa T11 SD 4.21 > 1.5 x 2.8 and SCD below-floor 7-11 % at L2-L4, information
only (the rib key pools two levels where the trace misses a 12th rib).

## What must change before J3 is submitted

1. **Re-run J1 on features v3** (`tools/reader_e_features.py` 65609fd, `SCHEMA reader_e_features_v3`): SCD/SCW read on the
   closed-ring column with the release recipe (`canal_from_column`), ostk's values kept as `SCD_ostk`/`SCW_ostk`,
   `canal_source`/`canal_n_slab` bits, no canal value without a column; `range_check` applies no atlas level row above T11.
   The fix is verified outside the computation on three CTs (jobs 40443305/6/7, REFCHECK_OK: 0097 23 values, 0234 25,
   1138 16, SCD within 0.36 mm of the release `canal_ap` at every asserted level; self-test 40443308 SELF_TEST_OK). A v3
   re-run changes SCD/SCW on all 31,316 morph instances and their range/floor bits and flips 1,096 level bits above T11;
   every other value is reproduced to the decimal. Until then **the J1 SCD column is not to be trained on.** Cost from
   J1's measured timing: 3,524 pairs at median 34.5 s / mean 54.6 s (max 517 s) -> the same shard plan as `slurm/reader_e_j1.sh`.
2. **Re-run J2 on the v3 table** (`slurm/reader_e_j2.sh`, ~1 min) and require `pass = true` on SCD by both the flagged-share
   rule and the prevalence window (share below 11.07 mm <= 2 x 2.62 % in every plateau-keyed cell with n_pass >= 30).
3. **EPWl needs a lower-plate yardstick**: a published inferior end-plate width series (Panjabi 1992 reports EPWl separately)
   and a published end-plate depth SD (EPDu/EPDl) added to `results/reader_e/level_references.csv` (kept in step with
   `CTSpinoPelvic1K-1/morphometrics`) and `tools/reader_e_ranges.json`, then EPWl/EPDu/EPDl judged against them. Until then
   they enter J3 only with their mask bits and are not judged.
4. **Rib evidence on the families without rib labels** (spineps, versefusion, ctspine1k): the CT-trace rib flag lands on
   5-8 % of L4/L5 bodies and on the cervicothoracic top of whole-spine CTs (verse559), moving the rib-based count by -4/-5 on
   90 of 769 CTSP persons (spineps vs v11); no mask bit carries it. J3 must take the rib evidence from the labelled family
   of the same CT where one exists, or carry the trace-based last rib as a candidate with its chord and level context beside
   it; otherwise the section 6 ii invariance demotion acts on most positives (34 read CTSP records: three-way agreement
   29 %, v11 vs ts 39 % because TS puts the L6 body into its sacrum; 27 known disagreements: 18 %).
5. **Reader C raised on 31 SPINEPS pairs** (`reader_c_blank`; failure text in the JSONs, not diagnosed) and SPINEPS has no
   sacrum instance on some VerSe pairs (verse085/534/544) and swallows part of the transitional body on CTSP L6 (0090, 0097):
   carried by pair flags; diagnose before those pairs are counted as segmenter disagreement.
6. The release atlas VBHa/VBHp rows run 2-6 mm above the published means (L5 posterior 30.4 vs 24.1-25.7): a
   CTSpinoPelvic1K item, recorded and not adjudicated here; the J2 gate judges those cells on the published-centred envelope.

## What is ready for J3 once the gate passes

- Labels: `results/reader_e/j2/labels_j3.csv`, 1,129 persons (read LS-L6 88, LS-SAC 24, LS-II 25, LS-4L 2, ordinary 182;
  presumed ordinary 735; excluded 44; candidate 29; TL-0 95, TL-11 8, TL-13 4, TL-LR 11, TL-H12 17; 21 label-noise rows).
  The G3 test transitional persons of Figure 6 (`results/fig6/frozen/auto_truth.csv`, `g3_side == test` with a transitional
  `frozen_stratum`) must be asserted out of training and evaluation in the J3 script header.
- Mask bits per instance: `readerE/j2/mask_bits_j1.csv.gz` (to be recomputed from the v3 JSONs after the J1 re-run).
- Level context keyed on the plateau position (or absent without a sacrum; 10,476 rows), never the J1 range tag.
- Design as planned: sklearn `HistGradientBoostingClassifier` per head (LS, TL) with `monotonic_cst` (more rib chord ->
  more thoracic, more rib-free bodies -> more lumbar) and a 2-layer 64-unit bidirectional GRU in torch (CPU), grouped
  stratified 5-fold by person with an inner 4-fold for tau, 5 seeds, OOF predictions, Wilson intervals; one reqp node,
  8 cores, 32 GB; no pyarrow/lightgbm/xgboost/shap in the spineps env (CSV/JSONL tables only).
