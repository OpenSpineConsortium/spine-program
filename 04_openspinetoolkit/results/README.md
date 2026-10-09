# results/

- `ostk_level_morphometry_0097_reference_90a27a7.csv`: the header and the six case-0097 rows (T12, L1-L5)
  of `CTSpinoPelvic1K/morphometrics/ostk_level_morphometry.csv` at commit 90a27a7 (2026-09-10; 4,744 rows,
  802 cases), the pre-regression reference `TODO.md` step 1 is tested against: T12 VBHp 28.88, EPDl 34.80,
  SCD 18.72. The whole file lives in `05_ct_morphometry_parity/results/morphometrics/` and in the repository.
  Columns: `case, level, VBHa, VBHp, EPWu, EPWl, EPDu, EPDl, SCW, SCD, PDW_l, PDW_r, PDW, plate_rms_mm`;
  PDW empty (G.4).
- `grid_run_2026-09-10/`: the records of the day the committed CSV was made, read from the grid on
  2026-10-09 00:12 UTC (its own README has the timeline).

No result file in this folder was produced by running ostk during the build; the baseline table in
`../STATUS.md` was computed read-only from the committed CSV.
