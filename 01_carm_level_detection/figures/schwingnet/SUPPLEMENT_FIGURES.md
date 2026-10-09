# Supplementary Figures S1–S4

Built 2026-09-24 by `SchwingNet/tools/figS_supplement.py` (`python SchwingNet/tools/figS_supplement.py all`, or
`s1` … `s4`). Nothing is typed in. Every number on a page is read from a results file. Each figure's
`figS<n>.record.json` lists every drawn number with its file and JSON path, the SHA-256 (first 16 hex) of every
input, the text audit, and what was left off and why.

**Production form (all four).** Each page is 7.0 in wide and at most 8.40 in tall, which is 0.90 of the text
height, so `\includegraphics[height=0.90\textheight,width=\linewidth,keepaspectratio]` scales nothing. Text is
Arial only (ArialMT, Arial-BoldMT), embedded TrueType and live in the PDF. The smallest text is 12.0 pt. Panel
letters are bare bold 14 pt. Each figure has at most four components. The files are:

- `figS<n>.pdf`: vector master.
- `figS<n>.tif`: 1,200 dpi, RGB, LZW, rendered from the PDF.
- `figS<n>.png`: 300 dpi, for looking.
- `figS<n>.caption.txt`: LaTeX-ready, at most 60 words.

The builder reads every text span back out of the PDF. It refuses a page if any text is under 12 pt or not Arial,
if two spans collide, or if anything leaves the page. It also runs the same check on the matplotlib artists. The
typography follows Figure 5: regular 12 pt for ticks, axes and keys, and bold for direct labels, device names and
matrix values.

Every page was rendered and inspected after its last change.

| | stem | page (in) | caption words | spans audited |
|---|---|---|---|---|
| S1 | `figS1` | 7.00 × 8.40 | 54 | 100 |
| S2 | `figS2` | 7.00 × 8.22 | 59 | 58 |
| S3 | `figS3` | 7.00 × 8.40 | 58 | 82 |
| S4 | `figS4` | 7.00 × 7.50 | 56 | 40 |

---

## Figure S1. The corpus manifold

**Caption** (`figS1.caption.txt`):

> Corpus manifold, ImageNet features. (a) t-SNE (t-distributed stochastic neighbour embedding) of 11,638 frames from 18 sources, one colour family per modality. (b) The same points by modality; below, a film-versus-C-arm classifier. (c) Each render family against its device's real frames: accuracy, 95\,\% case-cluster interval; diamonds, majority share. (d) Pairwise balanced accuracy; Mendeley only here.

**Components.**
- (a) t-SNE by source, with direct labels.
- (b) The same map by modality, with the modality key, and below it the film-vs-C-arm/kV probe.
- (c) Each render family against its device's real frames (Cios Fusion, Surgio-B51, Elekta XVI).
- (d) Pairwise balanced accuracy, lower triangle.

**Sources.**
- `results/manifold/embedding.csv` (`in_figure == 1`).
- `results/manifold/probes.json`:
  - `film_vs_fluoro/{stats,deep}/svm/film_vs_carm_and_kv/leave_one_source_out`
  - `transfer/<device>/results/<comparison>/deep/svm`
  - `pairwise/deep/svm`
- It is a restyle of `figures/fig_manifold.*`. The builder asserts that its numbers equal
  `figures/fig_manifold.record.json` (frame count, frames per modality, probe accuracies, every (c) cell's accuracy
  and n, and the (d) row order).

**Drawn numbers.**
- 11,638 frames from 18 sources. By modality: film 3,234; fluoroscopy 1,064; kV imager 999; plain render 2,841;
  styled render 3,500.
- Film vs C-arm and kV imager, one source held out, n = 5,797 (3,734 film + 2,063). The majority share is 64.4 %.
  - Image statistics: 63.4 % [57.6, 69.2].
  - Deep features: 85.0 % [79.4, 90.0].
- (d) covers 136 pairs: minimum 82.3 %, median 99.9 %, maximum 100 %. Four cells are below 96 % and are printed:
  - VinDr × BUU-LSPINE 94.55
  - Mendeley × BUU-LSPINE 91.85
  - VerSe × CTSpinoPelvic1K 95.42
  - TotalSegmentator × VerSe 82.30
- Geneva and Ljubljana are one acquisition cluster each, so (d) has no evaluable pair for them.

**Restyle changes.**
- (a) is larger. The modality key sits under (b).
- The (a) labels are placed without collisions. The builder searches 304 placement orders and keeps the one with
  the least squared displacement. A thin leader line joins a label to its median when the label had to move, and
  no leader crosses another leader or a label. The placement is written to the record under `label_placement_a`.
- The in-figure argument sentences of `fig_manifold` are gone.
- (c) is three columns that share one set of row labels.
- (d) is the lower triangle; symmetry is asserted. Each source's name is repeated on its own empty diagonal cell,
  so every column is named. The colour bar sits horizontally in the empty upper triangle.

---

## Figure S2. Device image-formation parameters, and the refit its own gate rejected

**Caption** (`figS2.caption.txt`):

> Image-formation parameters. (a) Real frame per device above its styled render of the same projection; bar, 50 mm; R², body-region fit. (b) Fitted terms within their bounds: fold median, range. (c) Held-out R² gain over uncalibrated physics per fold; bar, six-fold t interval. (d) A refit with image noise in the loss failed its own gate; published parameters stand.

**Components.**
- (a) For each of four devices, a real frame above its styled render.
- (b) The nine fitted terms, each placed inside its fit bounds.
- (c) Held-out R² gain per fold.
- (d) The A32 refit against its acceptance gate.

**Sources.**
- `results/fig4_pairs/fig4_pairs.json` and its PNGs.
- `docs/devices/{bv_pulsera,cios_fusion,elekta_xvi,pixium_4600}.json`, at `physics_terms/fitted/<term>` and
  `physics_defaults/<term>/default`.
- `results/a3.json#comparisons/card_vs_uncalibrated_physics/per_device`.
- `results/stats_review/recompute.json#R2_card`.
- `results/supplement_figs/card_refit/{full,constrained}/<device>.refit.json`, copied from the grid's
  `or_ready/devices_refit*/`. See `results/supplement_figs/README.md`.
- The refit history is in `docs/RESUME_2026-09-22_PM.md`, checkpoint 19:50: "A32 CLOSED NEGATIVE: every refit
  fails its own gate; the published cards stand."

**Drawn numbers.**
- (a) Body-region R² of the pair shown:
  - BV Pulsera 0.973 (116 pairs)
  - Cios Fusion 0.888 (366)
  - Elekta XVI 0.975 (335)
  - PIXIUM 4600 0.655 (18)
- (c) Device mean gain, with its six-fold t interval:
  - BV Pulsera +0.042 [0.028, 0.056]
  - Cios +0.015 [−0.003, 0.034]
  - Elekta +0.023 [−0.006, 0.053]
  - PIXIUM +0.070 [−0.019, 0.159]
- (c) Pooled over 24 folds: +0.038 [0.020, 0.057], with four folds negative.
- (d) The gate accepts a refit only if held-out R² is no lower **and** the statistic distance is lower. Every refit
  was rejected. Values are held-out R² / statistic distance:

  | device | published | free refit | constrained refit | frames fitted / held out |
  |---|---|---|---|---|
  | Cios Fusion | 0.890 / 1.55 | 0.617 / 3.05 | not run (out of memory at 48 GB) | 40 / 40 |
  | Surgio-B51 | 0.560 / 3.76 | 0.455 / 24.3 | 0.477 / 5.02 | 40 / 40 |
  | Elekta XVI | 0.972 / 40.2 | 0.875 / 41.2 | 0.973 / 69.7 | 36 / 35 |

  These match the resume's numbers. The builder asserts that each refit fails its gate, so the caption's claim
  cannot go stale silently.

**Not shown, and why.**
- (a)–(c) leave out the Surgio-B51 and Varian cards. Neither appears in Table S1 or in the 24-fold analysis.
  Surgio-B51 appears in (d) only because the refit was run on it.
- The embedding panel and the angle panel of `fig4_formation` are dropped. The manifold is S1, and angle on real
  frames is S4.

---

## Figure S3. Which training source carries the detector

**Caption** (`figS3.caption.txt`):

> Which training source carries the detector. (a) Held-out vertebra recall per training arm and target: dots, whole-vertebra truth, 95\,\% case-bootstrap interval; diamonds, the same predictions against vertebral-body truth, a box-convention reading, not a retrained score. (b) Recall by view or gantry-angle band. (c) Recall change from adding one source, tested on the third; diamonds, body-truth difference, no interval.

**Components.**
- (a) The contribution matrix: 20 arms by 4 targets, at confidence 0.25.
- (b) Recall by C-ArmLSpine view (AP or lateral, 28 frames each) or by COBRA2026 gantry-angle band (208, 202 and
  238 frames).
- (c) The marginal contribution of one added source.

**Sources.**
- `results/contribution_matrix.json` (`cells`, `cells[].by_view`, `marginal_contributions`).
- COBRA2026 body truth: `results/bodybox_rescore/scored_body/<kind>__<arm>__cobra_test.json#conventions/body/at/0.25/vertebra_recall`.
- The body values are asserted against the rows of `results/bodybox_rescore/RESCORE.md`. The derived body gain
  for adding E to D on C-ArmLSpine reproduces RESCORE D5 (+17.8 points).

**Body-convention values.** Body truth is used wherever it exists: C-ArmLSpine (287 bodies) and COBRA2026 (855 of
893). DeepFluoro and Geneva have no body truth.

**Checks made for this build.**
- Every drawn cell was matched to its row in `results/indomain/points.csv`. All are HELD OUT and all values are
  equal.
- The inventory marks some cells NOT HELD OUT: lodo_df and lodo_cobra on C-ArmLSpine, because their checkpoint was
  chosen on the C-ArmLSpine test split; lodo_carm on COBRA2026 and DeepFluoro; and lodo_cobra on DeepFluoro. Every
  one of these is a target-in-training cell here. It is drawn hatched, never as a value.
- Every real-only arm (`rx_*`) was fine-tuned from `pose/anchor_none_v2_17-1882`, which is the "renders only" arm
  (`results/eval_gate/LINEAGE.md`). The figure's key now says so: "real only: real frames, fine-tuned from the
  renders-only detector".

**Layout change in (c).** The COBRA row "+D to S, on E" holds four contrasts: two D+S seeds, each against both
S-only runs. Its label says "two S-only runs", and it gets the height to show all four without touching. Contrasts
from bit-identical base arms are shown once.

**Not shown, and why.**
- The Geneva phantom column: it is one cluster, with whole-vertebra truth only.
- Design P: it is not an arm of the matrix.

---

## Figure S4. Detection against view angle on the real case134 spin

**Caption** (`figS4.caption.txt`):

> Detection against view angle on one patient's real rotational C-arm acquisition (301 frames; no intervals). (a) Lateral (−90°, source at patient's right) to +45°; boxes, bodies projected from cone-beam CT; bar, 50 mm. (b, c) Bodies found per 10° bin; arm names as in Figure S3; the reported detector's flat 50\,\% is unexplained. (d) Registration quality.

**Components.**
- (a) Four real frames with their truth boxes, at the frames nearest −90°, −45°, 0° and +45°. The frames are at
  −89.8°, −44.9°, +0.4° and +45.3°.
- (b) Recall per 10° bin at confidence 0.25.
- (c) The same at confidence 0.74.
- (d) Per-frame edge correlation of the registered pose. 287 of 301 frames are at or above 0.15, and the median
  is 0.332.

**Sources.**
- `results/arc/case134_sweep.json#detectors/<det>/<conf>`. The per-bin hits are asserted to sum to the pooled
  fields.
- `results/supplement_figs/case134/{frames.csv,summary.json,frames/*}`, copied from the grid's
  `realxray/carmlspine_sweep`. The identifier scan found 0 hits (ARC_CHECK item 5).

**Drawn numbers.** Whole spin, 1,204 vertebral bodies, one patient, **no interval is valid**:

| arm (legend) | checkpoint | 0.25 | 0.74 |
|---|---|---|---|
| D+E+S pooled, S spot frames | `dc_P_pooled` | 93.6 % (1127) | 78.1 % (940) |
| D+E, A, seed 0 (S held out) | `dc_A_held_surgio_b51_dr` | 37.2 % (448) | 29.2 % (351) |
| D+E, B, seed 1 (S held out) | `dc_B_held_surgio_b51_dr_s1` | 29.7 % (357) | 23.5 % (283) |
| reported detector, real only, D+E | `rx_lodo_carmlspine_1024` | 49.5 % (596) | 49.4 % (595) |

**Caveats, all in the record.**
- **The pooled arm is patient-held-out for case134.** `case134_sweep.json#contamination` says it saw case134's two
  spot frames. The list census contradicts that, and the census is used here:
  - `P_pooled/train.txt` and `val.txt` hold 0 case134 entries.
  - `best.pt` was written at 01:46 and the case134 frames at 05:28.
  - Source: `results/indomain/INVENTORY.md`.

  The pooled arm did see spot frames of 105 other C-ArmLSpine patients.
- **The reported detector's curve is flat at exactly 0.500** in 15 of 19 bins at 0.25 and 14 of 19 at 0.74. This
  looks mechanical and is **unexplained**. The caption says so. The per-frame predictions were not re-read.
- The truth is A28 body boxes. Only the pooled arm trained on body-convention boxes, so the level of the other
  three is set as much by box convention as by angle. Read the shape, not the level.
- At oblique and lateral angles, the L4 and L5 boxes run over the pedicles (ARC_CHECK item 6).
- The spin was exposed at 111 kVp and 12 mA; the spot frames at 77–89 kVp and 25–26 mA.
- The bins below −100° hold only 28–72 boxes.
- **The styled-render recall-versus-angle curve is not used** (`results/arc/recall_vs_angle*`). Its 17 subjects
  were the checkpoint-selection subjects of every scored detector (ARC_CHECK item 4).

---

## For the manuscript owner (nothing below was edited; each needs a decision)

1. **`supplement.tex` still includes the old figures.** It has `fig2_flow` as S1, `fig5_contribution` as S2 and
   `fig_manifold` as S3. The new set is:

   ```
   S1 figures/figS1.pdf  (manifold)          S2 figures/figS2.pdf  (image formation)
   S3 figures/figS3.pdf  (contribution)      S4 figures/figS4.pdf  (case134 angle)
   ```

   Captions can be `\input` from `figures/figS<n>.caption.txt`. The flow-of-cases figure (`fig2_flow`, CLAIM item
   33) is not one of S1–S4 and needs a place. Text references to "Figure S3" (manifold) become "Figure S1".
2. **The supplement's film-versus-fluoroscopy sentence does not describe S1(b).** The sentence at
   `supplement.tex` about line 47 says: majority 71.8 %; −0.7 to 9.2 points; "no percentile interval excluding
   zero"; "(Figure S3)". It comes from `results/a2.json#corpus_manifold/excess_over_chance`, which covers 19
   corpora and 7,311 frames. S1(b) draws a different probe from `results/manifold/probes.json`: film vs C-arm
   **and kV imager**, majority 64.4 %. Its deep-feature interval [79.4, 90.0] **does** exclude the majority share.
   The C-arm-only variant is 83.0 % [74.6, 90.9] against 77.8 %. Either cite a2 without pointing at S1, or state
   the S1 probe.
3. **Table S1 names five device terms wrongly.** `tables/tabS1_device_terms.tex` calls α "noise gain", σ_u "noise
   blur", b "display slope", c "display offset" and d "display gamma". In the fit (`tools/device_fit.py`, and the
   cards' `physics_defaults.how`) they are:
   - α: edge-enhancement (unsharp-mask) gain
   - σ_u: its radius
   - b: radial vignette
   - c: anode-heel gradient
   - d: cranio-caudal tilt gradient

   S2(b) uses the fit's meanings. The fix is `TERM_DESC` in `tools/make_supp_device_table.py`.
4. **"Real only" detectors are not from COCO.** Every `rx_*` detector, including the reported one, was fine-tuned
   from the render-trained `anchor_none_v2_17-1882` (`results/eval_gate/LINEAGE.md`). This matches the known
   NUMBERS.md correction. S3 and S4 now say so in their keys and records.
