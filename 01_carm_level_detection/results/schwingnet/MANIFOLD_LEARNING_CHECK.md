# Adversarial check: fig_manifold (stream A) and fig_learning (stream B)

2026-09-23. Every number below was re-read from the JSON/CSV files on disk
(`results/manifold/probes.json`, `results/manifold/pairwise_deep_svm.csv`, `results/manifold/embedding.csv`,
`results/learning/analysis.json`, `results/learning/lateral/gradcam_summary.json`,
`results/learning/gradient_regression.json`), not from any summary. Both PNGs were rendered
open and inspected at full page and in crops.

## Stream A — fig_manifold

| # | Item | Verdict |
|---|---|---|
| A1 | Panel (b) probe numbers match probes.json | **PASS** — `film_vs_fluoro/stats/svm/film_vs_carm_and_kv/leave_one_source_out`: acc 0.6341 [0.5765, 0.6925]; deep/svm 0.8496 [0.7938, 0.9000]; chance 0.6441; n 5,797 = 3,734 film + 2,063 C-arm/kV. Panel text and record.json agree to every digit shown. |
| A2 | Chance = class balance | **PASS** — probes.json in-probe sets: film 3,734, fluoroscopy 1,064 + kV 999 = 2,063; majority 3,734/5,797 = 0.6441. embedding.csv `in_probe` rows give the same modality counts. |
| A3 | Panel (c) transfer cells match probes.json | **PASS** — all 12 record cells equal `transfer/<device>/results/<cell>/deep/svm` (acc, bacc, chance, n, both CIs, sides). Chance equals the majority share of the two sides in all 12 cells (range 0.5005–0.6472); n range 666–999 as printed. |
| A4 | Panel (c) footer numbers | **PASS** — vanilla vs styled 1.000 on all three devices; styled vs real 0.9896 (Elekta) – 1.000 (Cios), i.e. 99.0–100.0 %; those three cells: chance 0.5027 / 0.5556 / 0.6472 (= 50.3–64.7 %), n 736 / 666 / 771 — footer says 666–771, correct. |
| A5 | Panel (a) counts vs embedding.csv | **PASS** — `in_figure == 1` rows: 12,138 over 31 sets; minus Mendeley's 500 = 11,638 plotted, in 18 source groups (BUU AP+LA = 1,000; "NHANES II" = NHANES II full 500; "CSXA" = CSXA raw 499; unstyled 3×500 = 1,500; styled 3,500). Matches record.json `frames_per_source` exactly. |
| A6 | Every embedding.csv set accounted for | **PASS** — 38 sets total; the 7 not drawn are the documented duplicates (BUU-LSPINE, CSXA, NHANES II, Mendeley raw) and retired render generations (calibrated Cios render, physics rare, physics render), all listed in probes.json meta. Note: embedding.csv's `in_figure` flag still marks Mendeley 1 — the flag predates the exclusion, which lives in fig_manifold.py and is recorded in fig_manifold.record.json `excluded_from_scatter`. |
| A7 | Panel (d) pairwise matrix | **PASS** — upper triangle of pairwise_deep_svm.csv: 136 pairs = C(17,2); min 0.823 DRR TS vs DRR VerSe; BUU vs Mendeley 0.9185; BUU vs VinDr 0.9455; DRR CTSP vs DRR VerSe 0.9542. The four boxed numbers on the panel (82, 92, 95, 95) sit in exactly those cells. Colourbar chance 50 % = probes pairwise meta chance 0.5. Geneva and Ljubljana absent (one cluster each, listed as dropped). Right edge not clipped. |
| A8 | Mendeley only in (d); FluoroCap nowhere | **PASS** — Mendeley appears in the matrix and in no scatter; FluoroCap is in probes.json `excluded_sets` and in none of the 38 embedded sets, so it cannot appear in any panel. |
| A9 | Caption ≤ 60 words | **PASS** — 58 words. |
| A10 | Exactly four components | **PASS** — a, b, c, d on the rendered PNG. |
| A11 | No identifier in any panel | **PASS** — labels are source names only; no path/case/frame text anywhere on the page. |
| A12 | Banned word | **PASS** — absent from caption, record.json, MANIFOLD.md, fig_manifold.py. |
| A13 | Page geometry | **PASS** — PNG 2100×2715 px = 7.0×9.05 in at 300 dpi; PDF and 600-dpi LZW TIF present. |
| A14 | Cosmetic note | **NOTE** — in the BUU-LSPINE row the boxed "95" (VinDr) and "92" (Mendeley) sit in adjacent columns and nearly touch; separate boxes are visible at print zoom, but the row can read as "9592" at a glance. |

## Stream B — fig_learning

| # | Item | Verdict |
|---|---|---|
| B1 | Outputs on disk | **PASS** — results/learning/ holds LEARNING.md, analysis.json, gradient_regression.json, zones.json, l6_confound.json, census.json, bank_census.json, gradcam_summary.{json,npz}, gradcam.npz, exemplars.npz, embeddings.npz, embeddings_cpu_replicate.npz, map.npz, and lateral/ (the lateral-pool Grad-CAM/occlusion pass); figures/fig_learning.{pdf,png,tif,caption.txt} present. |
| B2 | Panel (a) numbers match analysis.json | **PASS** — Spearman(PC1, level) 0.3543 [0.3113, 0.3982] → "0.35 [0.31, 0.40]"; nearest other-person neighbour within one level 0.9335 [0.9241, 0.9424] → "93.3 % [92.4, 94.2]"; n bank-val 15,898, real 520, L6 150; T13 n = 0 and the legend says "no held-out crop", as required. |
| B3 | Panel (b) matches lateral/gradcam_summary.json | **PASS** — occlusion zone shares (above/target/below/lateral, ×100): T12 19/27/43/11, L3 19/42/33/6, L4 19/28/46/7, L5 20/26/46/9, L6 27/26/34/13, sacrum 40/30/11/19; "named right" 90/90/80/80/90/100 % = exact 0.9/0.9/0.8/0.8/0.9/1.0 on n = 10 crops per level. Caveat: the TOP-LEVEL gradcam_summary.json (random pool) differs (e.g. T12 25/25/34/16, exact 0.8); fig_learning.py prefers `lateral/` when present, so the lateral files are the ones to audit against — this check did. |
| B4 | Panel (d) matches gradient_regression.json | **PASS** — ρ printed per row: +0.99, +0.93, +1.00, +1.00, +1.00, +0.61, −0.23 = spearman_pc1 for body height ant. / TP span / wedge / end-plate width / canal width / body height post. / canal depth; R² 0.961, 0.946, 0.904, 0.816, 0.812, 0.631, 0.019 and Q² 0.906, 0.891, 0.841, 0.589, 0.541, 0.030 at the plotted positions; atlas_check agrees on every level's median and n. |
| B5 | Canal-depth Q² clipped off-axis | **WARN** — canal depth Q² = −1.249 [−1.433, −0.968] lies left of the axis limit (−0.5) and its marker is silently clipped: the row shows only the R² dot, so a reader cannot tell the Q² exists and is deeply negative. The number is in LEARNING.md's table; the panel should either widen the axis, draw an off-scale arrow, or state it. |
| B6 | Chance beside every accuracy | **WARN** — panel (b)'s "named right" percentages carry the denominator (10 crops) but not the chance level (uniform 1/27 = 3.7 %, majority shares in analysis.json); it is stated in LEARNING.md but not on the page. Panel (a)'s within-one-level statistic likewise has no baseline beside it. The manifold figure meets this rule everywhere; the learning figure does not. |
| B7 | No record.json | **NOTE** — there is no fig_learning.record.json; the manifold figure ships one. The on-page numbers were verified against the source JSONs directly (B2–B4), but the per-figure number ledger is missing for stream B. |
| B8 | Caption ≤ 60 words; four components; identifiers; banned word | **PASS** — caption 59 words; panels a–d exactly; crop thumbnails carry no path/case/frame text; the banned word is absent from caption, LEARNING.md and fig_learning.py. |
| B9 | Held-out cross-check | **PASS** — fc on v9_val 0.7837 [0.7636, 0.8040] (n 15,898, majority 0.098, chance 0.037) equals the trainer's own validation 0.7837, the stated proof the crops were fed as trained. Real frames: C-ArmLSpine 0.548 [0.490, 0.605] (n 228, majority 0.237); COBRA 0.226 [0.153, 0.285] (n 292, majority 0.425 — below the majority baseline, which LEARNING.md reports rather than hides). |

## Headline numbers, re-read from the JSONs

- Modality probe (LOSO, n = 5,797; chance 64.4 %): image statistics 63.4 % [57.6, 69.2] — at chance; deep features 85.0 % [79.4, 90.0].
- Styling: vanilla vs styled 100.0 % on all three devices; styled vs real 99.0–100.0 % (chance 50.3–64.7 %; n 666–771 per pair).
- Pairwise separability (deep/svm, 136 pairs, chance 50 %): min 82.3 % (DRR TS vs DRR VerSe), median 99.9 %; BUU-LSPINE vs Mendeley 91.9 % — the duplicate-exclusion evidence.
- Level space (held-out): Spearman(PC1, level) 0.35 [0.31, 0.40] over 15,898 crops; nearest other-person neighbour within one level 93.3 % [92.4, 94.2]; single-crop fc 78.4 % [76.4, 80.4] (chance 3.7 %).
- Gradients: PC1 explains anterior body height R² 0.96 (Q² 0.91), TP span 0.95 (0.89), wedge ratio 0.90 (0.84); canal depth R² 0.02, Q² −1.25 — not tracked.

**Overall: stream A PASS (one cosmetic note). Stream B PASS on every number, with two WARNs (clipped canal-depth Q², missing chance levels on panel b) and one NOTE (no per-figure record file).**
