# results/

- `spine_detector_report/`: the detect_v1 field report of 2026-09-02 (`report.txt`, `metrics.json`, `results.csv`,
  `predictions.json`, `manifest.parquet`, `assets.json`, `report.html`, `build_report.py`, `make_assets.py`, `renders/`).
  `report.html` was regenerated on 2026-10-08 from a redacted `assets.json` with the report's own `build_report.py`:
  the two BUU-LSPINE thumbnails are removed (BUU terms forbid redistribution of its images), the Mendeley thumbnail stays.
  `renders/` holds 3 of the 40 detect_v1 renders, kept as figures: `mendeley_2695-F-026Y1.png` (Mendeley lumbar, CC BY),
  `nhanes_cervical_00200.png` (NHANES II cervical, public domain) and `mendeley_N26-Olisthesis-L3-4-F-52-Yrs.png` (an
  olisthesis case). The other 34 Mendeley / NHANES renders (63,406,545 B; removed on 2026-10-08 under the size and
  data-class rule) and the 3 BUU renders (never copied) are recorded by path in `MANIFEST_LOCAL.md` section 3a and
  regenerate from `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1` with `src/render_prediction.py`;
  `make_assets.py` run here would therefore see 3 renders, not 40. Numbers: `STATUS.md` section 1c.
- `corner_detector_buu/`: per-corner errors on the 301 BUU-LSPINE test films for the heatmap model (`per_landmark_buu.csv`),
  YOLOv8l at 640 and 1024 px (`pl_v8l640.csv`, `pl_v8l1024.csv`) and YOLO11n-pose (`yolo/per_landmark.csv`, `yolo/summary.json`);
  columns `case, channel, level, err_px[, err_norm_diag, matched | confidence]`. The best / worst overlay PNGs are BUU film
  pixels and stay by path.
- `lumbar_diag_2026-09-16/`: the mid-lumbar error diagnosis on the allspine_v2 model (RECORD ONLY; `STATUS.md` section 3).
  The four `render/*.png` montages are film pixels and stay by path; `render/crop_stats_summary.json` is here.
- `track5_results/`: the Track 5 band-transfer reports on allspine_v2 and films_all2 (RECORD ONLY [WRONG-BANK]; `STATUS.md` section 3).
