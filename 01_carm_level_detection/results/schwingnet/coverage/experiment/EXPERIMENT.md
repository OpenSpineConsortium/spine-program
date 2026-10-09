# Matched-N low- vs high-coverage render arms (generated 2026-09-25T05:42:34; 12 of 12 arms scored)

Numbers only; the comparison and the fit are SchwingNet/results/coverage/N_VS_COVERAGE_PLAN.md and tools/indomain_fit_coverage.py --experiment. Real test = the device's own real TEST split (never trained on); body@0.25 = C-ArmLSpine vertebral-body re-score at conf 0.25.

| arm | device | seed | N train | arc poses | H*_lat | C_lat | H*_tilt | state | real test vert recall | body@0.25 | unseen sweep | case134 |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|---|
| high | elekta_xvi | 0 | 1972 | 1972 | 0.9976 | 1.0 | 0.7273 | scored | 0.0 | None | scored | scored |
| high | elekta_xvi | 1 | 1972 | 1972 | 0.9976 | 1.0 | 0.7273 | scored | 0.0 | None | scored | scored |
| low2n | elekta_xvi | 0 | 3944 | 0 | 0.6186 | 0.3333 | None | scored | 0.015677491601343786 | None | scored | scored |
| low2n | elekta_xvi | 1 | 3944 | 0 | 0.6186 | 0.3333 | None | scored | 0.004479283314669653 | None | scored | scored |
| low | elekta_xvi | 0 | 1972 | 0 | 0.6186 | 0.3333 | None | scored | 0.0 | None | scored | scored |
| low | elekta_xvi | 1 | 1972 | 0 | 0.6186 | 0.3333 | None | scored | 0.0 | None | scored | scored |
| high | surgio_b51_dr | 0 | 2646 | 2646 | 0.9931 | 1.0 | 0.7467 | scored | 0.006968641114982578 | 0.006968641114982578 | scored | scored |
| high | surgio_b51_dr | 1 | 2646 | 2646 | 0.9933 | 1.0 | 0.7468 | scored | 0.010452961672473868 | 0.010452961672473868 | scored | scored |
| low2n | surgio_b51_dr | 0 | 5290 | 0 | 0.2396 | 0.1111 | None | scored | 0.013937282229965157 | 0.013937282229965157 | scored | scored |
| low2n | surgio_b51_dr | 1 | 5290 | 0 | 0.2396 | 0.1111 | None | scored | 0.024390243902439025 | 0.024390243902439025 | scored | scored |
| low | surgio_b51_dr | 0 | 2646 | 0 | 0.2396 | 0.1111 | None | scored | 0.04878048780487805 | 0.04878048780487805 | scored | scored |
| low | surgio_b51_dr | 1 | 2646 | 0 | 0.2396 | 0.1111 | None | scored | 0.09059233449477352 | 0.09059233449477352 | scored | scored |
