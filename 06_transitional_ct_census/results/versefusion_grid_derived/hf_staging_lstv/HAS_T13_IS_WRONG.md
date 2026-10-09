# WARNING: `has_T13` in `manifest.csv` / `manifest.json` is WRONG

`manifest.csv` (374 rows) flags `has_T13 = True` on 18 scans. The truth is 6: six of the eighteen carry an L6 instead, and `verse707` is a genuine table-versus-mask conflict (memory note `versefusion-t13-flag-wrong`; docs/handoff/RESULTS_CATALOG.md D.26). The count was re-checked on this copy on 2026-10-08: 18 rows read True for `has_T13`, 44 for `has_L6`. Never read `has_T13` from these tables; read the raw VerSe masks (id 28 = T13, id 25 = L6) and the published Loeffler table instead (docs/handoff/RECIPES.md section 3.5).
