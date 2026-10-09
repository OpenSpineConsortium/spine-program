# Which source carries the detector, and why: the contribution matrix

> **Corrections after the check (2026-09-22, assembly).** The prose below was written from the 20:27 matrix
> run (job 40415588) and was not regenerated after the 21:24 rerun (job 40415691) added the equal-count and
> rerun-D arms. `contribution_matrix.json` is authoritative; the manuscript reads only from it. Where the
> text disagrees with the JSON: (i) the self-check covers **85** cells, not 75 (§8 is right, the preamble
> is not); (ii) §3's Spearman values (0.86 / 0.70 / 0.86 / 0.86 / −0.44 / −0.44 / −0.51 "over ten cells")
> come from the earlier run; the JSON holds 0.73 / 0.58 / 0.73 / −0.19 / 0.73 / −0.19 / −0.27 over 14 cells,
> **and those 14 include the equal-count arm entered with the full Elekta covariates** (2,640 frames /
> 110 patients), a defect in `tools/contribution_matrix.py` fixed in the tool on 2026-09-22 but not yet
> re-run, so neither set of correlations is quoted anywhere; (iii) §3(a) mean single-source held-out recall
> "E 89.8" is 69.8 in the JSON (six cells, again including the cut arm), and the target-difficulty means
> "65.7 / 70.2 / 21.8" are 62.2 / 61.4 / 23.3; (iv) the equal-count arm kept **240** frames, not 238 (the
> list tag is `eq238`); (v) §3(d)'s Elekta angle shares 32 / 31 / 37 % are computed over all 3,480 COBRA
> frames, not the 2,640 training frames; (vi) §2's "own poses win once outside the interval" understates
> the table: both C-ArmLSpine design-B-minus-A pairings exclude zero (+3.1 [+0.3, +7.1] and +7.3
> [+3.5, +11.5]), sharing one B seed; (vii) the marginal-contribution rows whose base is the equal-count arm
> (+45.6 / +41.5 and +71.1 pp) are not source contributions and are excluded from the manuscript; (viii) the
> two submitted jobs (40415584, 40415585) exited non-zero after writing `scores.json` (a naming-summary print
> in `devcorpus_train.py` line 383 raises on a None), so their cells are real and their logs end in a
> traceback; (ix) `docs/devices/surgio_b51_dr.json` (card R² 0.584, typicality 0.925) exists only on the
> grid, so the Surgio covariates are not quoted. Every number the manuscript uses is listed with its JSON
> path in `SchwingNet/NUMBERS.md`.

Written 2026-09-22 from the arms on disk. Every number below is read from a file named beside it; the matrix, the
intervals and the figure are produced by `SchwingNet/tools/contribution_matrix.py` (grid job 40415588 and reruns), which
recomputes every cell from the per-frame raw predictions that `tools/realxray_eval.py --dump-raw` keeps, at ONE
operating point (confidence 0.25, IoU 0.5, greedy one-to-one matching), and reproduces every pooled number in the
arms' `scores.json` to four decimals (self-check: 75 cells, max |difference| 0.0000). Intervals are 2,000-resample
case-cluster bootstraps (a case = a specimen, a patient or a phantom; frames of one case are one cluster). A cell
with one cluster carries no interval and says so. Nothing here is quoted from a bank with a known split leak.

`D` = DeepFluoro / Siemens Cios Fusion (six cadaveric pelves, 366 frames, poses shipped). `S` = C-ArmLSpine /
Surgio-B51 (148 intraoperative cases, AP + lateral, our own 2D/3D registration to the CBCT). `E` = COBRA2026 /
Elekta XVI (145 radiotherapy patients, kV CBCT projections, scanner geometry). `G` = the Geneva hip phantom /
Philips BV Pulsera (test only, one phantom). Files: `SchwingNet/results/contribution_matrix.{json,md}`,
`SchwingNet/figures/fig_contribution.png`.

---

## 0. The answer in five sentences

1. **DeepFluoro is not the source that carries the detector in general. COBRA / Elekta is.** With Elekta as the
   only training device the held-out C-ArmLSpine reads **86.8 % [81.1, 91.8]** outline recall and the held-out
   DeepFluoro test specimen **92.8 %** (one cluster); adding Elekta to a DeepFluoro-only arm moves C-ArmLSpine by
   **+71.8 pp [+63.4, +79.6]**, and adding it to a Surgio-only arm moves DeepFluoro (all six specimens) by
   **+54.7 pp [+40.9, +64.1]**. Adding DeepFluoro to an Elekta arm moves C-ArmLSpine by **−2.1 pp [−6.0, +1.4]**
   (seed 0) and **−6.3 pp [−9.8, −2.9]** (seed 1): nil or slightly negative.
2. **DeepFluoro is the carrier on exactly one target, COBRA / Elekta held out**, and there it is the best source on
   the sheet: DeepFluoro alone **38.1 % [32.3, 44.5]**, above the D+S pairs (30.2 / 31.4 / 32.7) and far above
   Surgio alone (7.5 / 12.2). Adding Surgio to it costs **−7.8 pp [−12.5, −3.9]**. The `k = 1 → k = 2` gain the
   model card quotes for Elekta (0.122 → 0.302) is real, but it is DeepFluoro being added to a Surgio base; the
   reverse addition is a loss.
3. **The mechanism is angular coverage of the real frames, and it is visible in every held-out cell.** DeepFluoro's
   real frames lie within 45° of AP (228 / 79 / 38 / 21 frames at 0–10 / 10–20 / 20–30 / 30–45°, none beyond);
   Surgio's are exactly AP and exactly lateral; Elekta's are spread over 0–90° (542–731 frames per 15° bin). On
   held-out COBRA every arm collapses in the 60–90° third (≤ 13 %) and the arms with DeepFluoro content reach
   63–71 % in the 0–30° third; on held-out C-ArmLSpine the DeepFluoro-only arm finds the sacrum on **100 % of AP
   frames and 0 % of laterals**, and only Elekta-containing arms reach the laterals (76–88 %).
4. **No pixel-statistics, card-quality or registration covariate explains the matrix; each predicts the wrong
   ranking somewhere.** The manifold overlap is symmetric while the transfer is not (E→S 86.8 vs S→E 7.5–12.2 on
   the same pair, overlap 0.071); registration is exact for DeepFluoro and COBRA and weakest for Surgio, yet
   DeepFluoro and Surgio are the two weak sources; the DeepFluoro card has the worst typicality (0.101) and is the
   best source on COBRA.
5. **Count is a lever and content is a lever, and the confirmatory arm measured both.** The Elekta-only arm with its
   real frames cut from 2,640 (110 patients) to 240 (10 patients), everything else fixed, falls on held-out
   C-ArmLSpine from 86.8 % to **39.0 % [33.2, 44.7]**: a paired **−47.7 pp [−53.7, −41.8]**. At that equal count it
   still beats the DeepFluoro-only arm of the same size by **+26.1 pp [+18.2, +33.6]** (39.0 vs 12.9), and the loss
   sits almost entirely on the laterals (AP 95.1 → 64.3, LAT 78.5 → 13.9). So the small sources are small for a
   reason that matters (DeepFluoro's 238 frames and Surgio's 210 sit where a 240-frame Elekta sits, or below), and
   what to add is distinct frames at the missing angles — real ones where they exist, styled renders under
   coverage-spanning poses where they do not — not a weight on a card-quality score. Whether plain repetition of
   the few frames recovers any of the 47.7 pp is the next arm, written and costed in §5, not submitted.

---

## 1. What is on the matrix

Arms with a `scores.json` under `~/spine-detector/runs/devcorpus/` (design A: every card rendered under the Cios
Fusion pose pool; design B: each card under its own device's poses; both mixed with the training devices' real
frames at ×2), plus the real-frame-only arms of `tools/or_recall_curves.py` under `or_ready/lodo/sweeps/`. A
device is held out when no frame of it, styled or real, was in training; for a single-device arm that is both the
device named in the run and the third device it never saw, which is why the S-only and D-only arms carry cells the
model card did not (§4.6 listed only the named device).

Held-out vertebra recall, % (IoU 0.5, conf 0.25). C-ArmLSpine under the outline convention, which is the
convention COBRA and DeepFluoro truth use and the one the manuscript's 90.6 % is on; the body-convention number
sits in the table for reference and is 5–22 % for every held-out arm, which is the convention mismatch, not a
failure. Full rows with files: `contribution_matrix.md`.

| training set | DeepFluoro test (18-1109, one specimen) | DeepFluoro all six specimens | COBRA Elekta test (27 patients) | C-ArmLSpine test, outline (28 cases) |
|---|---:|---:|---:|---:|
| styled+real **D** only (`dc_A_held_surgio_b51_dr_1dev_cios_fusion`; the rerun `dc_A_held_elekta_xvi_1dev_cios_fusion`, job 40415584, came out bit-identical) | in training | — | **38.1 [32.3, 44.5]** | 12.9 [8.3, 18.1] |
| styled+real **E** only, real frames cut to 240 / 10 patients (`..._1dev_elekta_xvi_eq238`, job 40415585) | in training | — | in training | **39.0 [33.2, 44.7]** |
| styled+real **E** only (`dc_A_held_*_1dev_elekta_xvi`, one model, two run directories) | **92.8** | **75.3 [60.1, 95.0]** | in training | **86.8 [81.1, 91.8]** |
| styled+real **S** only (two runs, `held_cios` / `held_elekta`) | 31.3 / 26.5 | 17.4 [2.1, 40.4] / — | 7.5 [3.5, 12.1] / 12.2 [8.0, 16.0] | in training |
| A: styled+real **D+S** (seeds 0 / 1) | in training | — | 30.2 [26.3, 34.2] / 31.4 [26.6, 35.4] | in training |
| A: styled+real **D+E** (seeds 0 / 1) | in training | — | in training | 84.7 [77.7, 90.7] / 80.5 [72.5, 87.6] |
| A: styled+real **S+E** (seeds 0 / 1) | 91.6 / 91.6 | 72.1 [59.1, 86.1] / 77.7 [64.8, 87.9] | in training | in training |
| B: **D+S** (own poses) | in training | — | 32.7 [28.4, 36.2] | in training |
| B: **D+E** (own poses, seed 1 only; seed 0 died at a missing label cache, job 40414090) | in training | — | in training | 87.8 [81.7, 93.2] |
| B: **S+E** (own poses, seeds 0 / 1) | 94.0 / 94.0 | 78.6 [68.8, 92.0] / 75.3 [63.6, 90.9] | in training | in training |
| real frames only **D+E** (`lodo_carm`) | in training | — | in training | 90.6 [85.4, 95.2] |
| real frames only **D+S** (`lodo_cobra`) | in training | — | 18.5 [13.7, 22.8] | in training |
| real frames only **S+E** (`lodo_df`) | 95.2 | — | in training | in training |
| real frames only **S** (`only_carm`) | 10.8 | — | 8.8 [5.0, 12.2] | in training |
| renders only, no real frame (`render`, CTSpinoPelvic1K under DeepFluoro poses) | 59.0 | — | 37.8 [33.9, 42.1] | 31.7 [27.1, 36.1] |
| P: pooled, every device (job 40415009) | pending | pending | pending | pending |

The Geneva column (one phantom, 116 frames, 37 vertebra boxes all L5, 87 sacrum boxes) is on the figure as
sacrum-found and is not in this table: it is one cluster, its vertebra count is tiny, and the same arm swings by
37.8 pp between seeds on it (`dc_A_held_cios_fusion` 8.1 vs 45.9 vertebra recall). It is a hip field on an image
intensifier; nothing trained here sees more than 57.5 % of its sacra (`dc_B_held_cios_fusion`). It is a different
task and is reported as one.

**Two reading rules the table needs.** (i) The DeepFluoro test split is ONE specimen, 18-1109, so its column has no
interval and is the easiest specimen for these detectors, not the hardest: over all six specimens (the device is
absent from those arms' training, so every specimen is held out) the same arms read 72–79 % with per-specimen
values from 46 % (18-2799) to 100 % (18-2800); `contribution_matrix.md` lists them. The one-specimen column
overstates every DeepFluoro number by 14–20 pp. (ii) Two directories, `dc_A_held_cios_fusion_1dev_elekta_xvi` and
`dc_A_held_surgio_b51_dr_1dev_elekta_xvi`, are the same training list at the same seed and produced bit-identical
scores on every dataset; they are one model, counted once. The two S-only directories are also one list at one
seed and did NOT come out identical (COBRA 7.5 vs 12.2, DeepFluoro test 31.3 vs 26.5), which is the run-to-run
variation of the smallest arms at a fixed seed.

---

## 2. Marginal contribution of each source

Paired case bootstrap of the difference between two arms on the same frames (`marginal_contributions[]` in the
JSON). Add-one delta = (pair with the source) − (the other source alone); leave-one-out is its negative.

| held-out target | adding | to a base of | delta (pp) | 95 % CI | clusters |
|---|---|---|---:|---|---:|
| C-ArmLSpine (outline) | **E** | D | **+71.8** / +67.6 (seeds 0 / 1 of the pair) | [+63.4, +79.6] / [+57.6, +76.8] | 28 |
| C-ArmLSpine (outline) | D | E | −2.1 / −6.3 | [−6.0, +1.4] / [−9.8, −2.9] | 28 |
| DeepFluoro, six specimens | **E** | S | **+54.7** / +60.2 | [+40.9, +64.1] / [+40.9, +73.9] | 6 |
| DeepFluoro, six specimens | S | E | −3.3 / +2.3 | [−17.5, +3.5] / [−16.1, +12.6] | 6 |
| COBRA Elekta | **D** | S | **+18.0 … +23.9** (two pair seeds × two S-only runs) | narrowest [+13.2, +23.4], widest [+18.1, +29.3] | 27 |
| COBRA Elekta | S | D | **−7.8** / −6.7 | [−12.5, −3.9] / [−12.5, −1.8] | 27 |

Read plainly: **Elekta's marginal contribution is large on both other devices (+55 to +72 pp) and its removal is
the only removal that breaks an arm. DeepFluoro's marginal contribution is large on one device only, COBRA (+18 to
+24 pp), and nil elsewhere. Surgio's is nil or negative everywhere** (−7 pp on COBRA, within noise on
DeepFluoro; it cannot be measured on C-ArmLSpine, where it is the target).

Design B (own poses) versus design A (one pose pool) on the same frames: DeepFluoro six specimens +6.5 [−0.2,
+16.7] to −2.3 [−12.5, +8.8] across the four seed pairings; COBRA +2.5 [−0.9, +5.6] and +1.3 [−2.2, +4.7];
C-ArmLSpine +3.1 [+0.3, +7.1] and +7.3 [+3.5, +11.5]. Own poses never lose and win once outside the interval, on
the device whose own poses are two views (Surgio) — consistent with §3(d), and not yet a claim: one B seed.

**Seed spread, honestly.** The same arm across seeds 0 and 1 moves 1.1 pp on held-out COBRA (30.2 / 31.4), 4.2 pp
on held-out C-ArmLSpine (84.7 / 80.5), 5.6 pp on DeepFluoro over six specimens (72.1 / 77.7), and up to 7.2 pp on
the one-specimen DeepFluoro test even for in-training arms. The design A-versus-B difference (1.3–7.3 pp) is the
same order. The source contributions above are an order of magnitude larger than the seed spread; the design
differences are not.

**A caution the paired intervals need.** Two runs of the S-only list at the same seed differ on COBRA by
+4.7 pp with a paired interval of [+2.0, +7.5] (`named_paired_comparisons`), while two runs of the D-only list
are identical to the last decimal. The paired case bootstrap measures sampling over cases; it does not see
training noise, so "the interval excludes zero" is necessary for a claim and not sufficient when the difference
is under about 5 pp. Every source contribution in the table above clears that by an order of magnitude; the
design A-versus-B differences and the −2.1 / −6.3 pp DeepFluoro-onto-Elekta deltas do not, and are reported as
what they are.

---

## 3. Candidate explanations, each as a number

Spearman rank correlations of the ten single-source held-out cells with each source covariate are in the JSON
(`correlations`), but two of the ten cells are the same model and the covariates take only three values (one per
source), so these rank, they do not test: real train frames ρ = 0.86, real train clusters 0.70, card R²_held-out
0.86, pose-pool size 0.86, typicality_99 −0.44, pose |lat| p90 −0.44, pair Bhattacharyya overlap −0.51. What
follows is the per-covariate reading against the matrix, which is the honest form at this size.

**(a) Real-frame count per device** — Elekta 2,640 train frames, DeepFluoro 238, Surgio 210 (`realxray/<set>/images/train`,
`splits.json`). Ranks the sources E ≫ D ≈ S, which matches the source strength (mean single-source held-out recall
E 89.8, D 25.5, S 19.4). **Consistent, and confounded with (d)**: the source with the most frames is also the only
one with continuous angular coverage. This is the confound the equal-count arm (§5) removes.

**(b) Specimens / patients** — Elekta 110 train patients, Surgio 105 cases, DeepFluoro 4 specimens. Predicts
S ≈ E ≫ D. **Wrong**: Surgio, with 105 patients, is the weakest source, and DeepFluoro with four cadavers is the best
source on COBRA. Patient count does not track.

**(c) Card fit quality** — `fit.R2_held_out`: Elekta 0.974, Cios Fusion 0.905, Surgio 0.584 (`docs/devices/<device>.json`);
`distribution.coverage.typicality_99`: Surgio 0.925, Elekta 0.848, Cios Fusion 0.101. R² ranks E > D > S, which
matches the strength ordering only if D and S are read as close (25.5 vs 19.4), and it would predict D well above
S on C-ArmLSpine, where they read 12.9 (D) and — as target — nothing. Typicality ranks S > E > D: **wrong** in both
directions (the worst-typicality card is the best source on COBRA; the best-typicality card is the weakest source).
And the styled corpora do not land in their own device's real region at all: `or_ready/manifold/overlap.json`
`styled_inside_real` puts 4.1 % of `cios_fusion__cios_fusion` styled frames inside Cios Fusion's real 95 % region,
4.4 % of `elekta_xvi__elekta_xvi` inside Elekta's, 4.1 % of `surgio_b51_dr__surgio_b51_dr` inside Surgio's (the
C6 failure in `docs/RSNAI_PLAN.md`). The cards are not doing device-specific work in the image statistics; the
real frames are. Card quality does not track.

**(d) Pose pool and angular coverage** — pose pools (`devcorpus/poses/<device>.json`): Cios Fusion 366 poses over
six specimens, |lat| median 7.4°, p90 19.7°, max 36.5°; Surgio 296 poses over 148 cases at exactly 0° or 90°;
Elekta 8,418 poses over 152 cases, |lat| median 29.8°, p10–p90 6–54°, capped at 60° by the export. In design A
every card is rendered under the Cios Fusion pool, so within design A the styled poses do not differ between
sources and the covariate that differs is the angular coverage of each source's REAL frames: DeepFluoro
95 % / 5 % / 0 % of train frames at 0–30 / 30–60 / 60–90° from AP; Surgio 50 / 0 / 50; Elekta 32 / 31 / 37
(`realxray/deepfluoro/summary.json per_view_bin`, `cobra_elekta/summary.json per_view_angle_bin_lat_from_ap_deg`).
Against the targets' own angle bands the matrix reads as a coverage map (`by_view` in every held-out cell):

| held-out target, band (frames) | D only | S only (two runs) | D+S (A s0 / A s1 / B) | E only | D+E (A s0 / A s1 / B) | real D+E | renders only |
|---|---:|---:|---:|---:|---:|---:|---:|
| COBRA 0–30° (208) | 63.1 | 19.9 / 30.3 | 71.1 / 73.5 / 69.3 | — | — | — | 67.2 |
| COBRA 30–60° (202) | **41.0** | 3.5 / 6.7 | 19.8 / 21.2 / 31.1 | — | — | — | 39.9 |
| COBRA 60–90° (238) | 13.3 | 0.0 / 0.9 | 3.1 / 2.8 / 1.5 | — | — | — | 9.9 |
| C-ArmLSpine AP (28), outline | 16.1 (sacrum **100**) | — | — | 95.1 | 89.5 / 84.6 / 92.3 | 93.0 | 57.3 |
| C-ArmLSpine LAT (28), outline | 9.7 (sacrum **0**) | — | — | 78.5 | 79.9 / 76.4 / 83.3 | 88.2 | 6.2 |
| DeepFluoro test 0–30° (95) | — | 31.2 / 25.0 | — | 92.5 | — | — | 60.0 |

Three things in that table are the explanation. Every arm fails COBRA's lateral third, because no training device
except Elekta itself has frames there and the arms that hold Elekta out therefore have none. The DeepFluoro-only
arm is the only held-out arm with recall in COBRA's oblique band (41 %), because DeepFluoro's frames reach 45°;
adding Surgio, whose frames are two views, halves that band (41 → 20–31) while lifting the AP band (63 → 69–74),
which is the −7.8 pp net. And the DeepFluoro-only arm on C-ArmLSpine finds the sacrum on every AP frame and on no
lateral. **Angular coverage of the source's real frames is the covariate that tracks the matrix cell by cell**,
including its asymmetry; it is the only one that does. Pose-pool SIZE does not: design A holds it fixed and the
sources still separate.

**(e) Image-statistics distance** — Bhattacharyya overlap of real-frame densities in the 3-D space
(`or_ready/manifold/overlap.json`): D|E 0.0176, D|S 0.0401, E|S 0.0709; the corpus-level embedding
(`or_ready/corpus_manifold/overlap.json`) puts DeepFluoro–Geneva at 0.005 and COBRA–Geneva at 0.675. Overlap is
symmetric; transfer is not: the E–S pair has the largest overlap and transfers 86.8 one way and 7.5–12.2 the
other; the D–E pair has the smallest and transfers 92.8 (E→D) and 38.1 (D→E), the two best cross-device cells on
the sheet. Overlap ranks against the outcome (ρ = −0.51). **Does not track.** (The same file says why: what these
statistics separate is the corpus, not what a detector needs.)

**(f) Registration quality of the CT–X-ray pairs** — DeepFluoro: poses shipped, 14 landmarks reproject at 0.00 px on
all six specimens (`docs/DEEPFLUORO_FORMATION.md`), exact by construction. COBRA: the projections are the CBCT's own
raw data and `geometry.xml` is the scanner's calibration; per-case axis map confirmed at edge NCC median 0.847
(margin ≥ 0.1; four cases excluded for a margin below 0.1 and one, B000, because its CT never covers its frames),
frame log NCC median 0.991
(`realxray/cobra_elekta/summary.json pose_qc`) — exact by construction too. C-ArmLSpine: our own 2D/3D
registration, edge NCC median 0.370 AP and 0.207 LAT (`realxray/carmlspine/summary.json`), and the pose QC in
`or_ready/audit/addendum.md` bounds the box offset at a median 0.01 body heights with one frame beyond 0.25.
Ranking D = E > S. It predicts DeepFluoro as a strong source everywhere; DeepFluoro reads 12.9 on C-ArmLSpine.
**Does not track on its own.** Registration quality sets a floor on what a source's boxes can teach; it does not
decide what the source teaches, which is its coverage.

**Target difficulty is a separate axis and COBRA owns it.** Mean held-out recall across every arm: DeepFluoro 65.7
(range 8.4–95.2), C-ArmLSpine 70.2 (12.9–90.6), COBRA 21.8 (1.1–38.1). COBRA is a 40 cm field at 0.8 mm pitch,
120 kVp, half-fan, 2,980 of 3,480 frames with saturated air, over 0–90°; no other source has frames past 45°
except Surgio's exact laterals. Its difficulty is the lateral and oblique bands, and the "renders only" arm —
CTSpinoPelvic1K rendered under DeepFluoro poses with no real frame — reads 37.8 [33.9, 42.1] there, level with
the DeepFluoro-only arm and above every pair: on this target the real frames of the narrow-angle devices add
nothing that renders under near-AP poses did not.

---

## 4. Why DeepFluoro looked like the carrier

Three reasons, all in the files. The model card's `k = 1 → k = 2` point (Elekta 0.122 → 0.302) is DeepFluoro
added to Surgio on the one target where DeepFluoro has content Surgio lacks (the 30–60° band), so it is the
largest single-step gain on the sheet — and the model card recorded no single-device arm with Elekta alone,
because those two jobs (40414103, 40414104) failed at 14:12 with `tools/devcorpus_build.py` not yet on the grid.
The one-specimen DeepFluoro test column reads 92–95 % for every arm that contains Elekta, which reads as "easy
to reach" and is; over six specimens the same arms read 72–79 %. And the renders-only detector, the
initialisation of every real-frame arm, was rendered under DeepFluoro's poses with device terms fitted on
DeepFluoro's pixels (`or_ready/audit/addendum.md`), so DeepFluoro's geometry is in every arm's starting point and in
every design-A styled corpus, including the arms that hold DeepFluoro out (§7).

---

## 5. Proposal, with the evidence for each part

**Per-source weighting: not by card quality, registration quality or pixel distance** — none of those tracks the
matrix (§3 c, e, f). **By count, the case is now measured and it is real**: the equal-count arm (§8) shows that a
source's held-out value falls by 47.7 pp [41.8, 53.7] when its real frames go from 2,640 / 110 patients to
240 / 10, so the two small sources (DeepFluoro 238 frames / four specimens, Surgio 210 / 105 cases) are
under-represented in a way that costs recall. `real_rep = 2` gives every source the same multiplier; whether a
larger multiplier on the small sources recovers anything is exactly what the next arm tests
(`SchwingNet/slurm/contrib_eqcount_rep11.sh`, written, not submitted: the same 240 frames repeated ×11 so the
real entries equal the full Elekta arm's 5,280; about two GPU-hours). If repetition recovers most of the 47.7 pp,
up-weight the small sources; if it recovers little, only distinct frames help, and they must be made.

**Expand synthetically: angular coverage, not draws.** More styled draws per render cannot help while 4 % of styled
frames land in their device's real region (§3 c); the styling is not where the device lives. What the matrix
rewards is distinct frames at the angles the target will show: the equal-count arm lost 65 pp on the laterals and
31 pp on the AP frames of C-ArmLSpine, and the DeepFluoro-only arm has no laterals at all. Concretely: render every
card under the Elekta pose pool (8,418 poses spanning 0–60°, the only pool with obliques) or under a synthetic
AP-to-lateral sweep, and re-score held-out COBRA and C-ArmLSpine by band; the D-only arm's 41 % in COBRA's 30–60°
band from 5 % of its real frames says a band is learnable from little. Design B already shows own-pose renders
never losing and winning by +3.1 to +7.3 pp on C-ArmLSpine.

**Exclude: nothing, on this evidence.** Surgio's marginal contribution is nil or negative on the two devices where
it can be measured, but it is the only source with real laterals of a lumbar field, and the C-ArmLSpine target is
half laterals. Dropping it would be acting on a −7 pp cell on one target. The Geneva phantom is excluded from
training already by design (test only) and should stay so. The DeepFluoro card (typicality 0.101) is the one card
whose styled corpus is drawn from a distribution its own frames do not occupy; fix that card before weighting
anything, but that is a card defect, not a reason to drop the source.

**The one confirmatory experiment (submitted and read): the equal-count Elekta arm, job 40415585, 58 minutes.**
`dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238`: the Elekta-only arm (C-ArmLSpine held out) with COBRA's real
training frames subsampled BY PATIENT to DeepFluoro's count — 240 frames from 10 of 110 patients, seed 0, styled
corpus, validation frames and epochs unchanged (`SchwingNet/tools/make_lists_eqcount.py`,
`SchwingNet/slurm/contrib_eqcount.sh`; lists at `devcorpus/lists/A_held_surgio_b51_dr_1dev_elekta_xvi_eq238/`). It
is also matched in size (3,184 entries) to the DeepFluoro-only arm (3,180), so that comparison holds the number
of gradient steps fixed. The reading was pre-stated (near 86.8 %: count is not the lever; toward 12.9 %: it is)
and the result is in between and closer to the second: **39.0 % [33.2, 44.7]**, §8. Each COBRA patient's frames
sweep the whole arc, so the subsample kept its angular coverage by construction; what it lost was patients and
frames, and the laterals paid for it.

**Also submitted and read: the missing sixth single-device arm, job 40415584, 57 minutes**
(`dc_A_held_elekta_xvi_1dev_cios_fusion`), a second run of the DeepFluoro-only training list at seed 0. It came
out **bit-identical** to the first (38.1 % COBRA, 12.9 % C-ArmLSpine outline, 92.8 % DeepFluoro test; paired
difference +0.0 [+0.0, +0.0]), so it confirms the cell without being an independent seed; the S-only list at the
same seed did not reproduce (+4.7 pp [+2.0, +7.5] on COBRA), so the determinism is not guaranteed.

**Pending, not quotable yet: the pooled design P, job 40415009** (`dc_P_pooled/scores.json`; epoch 26 of 60 at
21:25 EDT, about eight minutes per epoch, so about 02:00 EDT). It is in-training on every device except Geneva;
rerun `SchwingNet/slurm/contrib_matrix_cpu.sh` when it lands and the matrix picks it up.

---

## 6. "Wasn't a data audit going to be one of the claims for rigor?"

**Stated, in two places; evidenced in part; not in the claims ledger; not run over the training lists that this
matrix is built on.**

- `docs/RSNAI_PLAN.md`, "Rules of accountability — Data": every dataset in `docs/RSNAI_DATA_MANIFEST.json` with
  source, licence, download date, file count, bytes and a SHA-256 over the file list; splits by case; "no test case
  of any device appears in any training list (`tools/or_audit_splits.py`, `or_audit_dupes.py`)". Box **E1** (the
  manifest) is ticked: 12 roots, e.g. `carmlspine` 59,609 files / 23.3 GB, `cobra2026` 988 / 42.2 GB,
  `deepfluoro_vendor` 94,626 / 72.7 GB, each with a list hash. Box **E3**, "leakage audit re-run over every training
  list used in C7–C11 (`or_audit_splits.py` extended to devcorpus lists)", is **not run**.
- `paper/rsnai/main_v2.tex` says it: "Splits are by case; no test case of any device is in any training list
  (audited by script)" (line 63) and "the data manifest (file-list hashes), the claims ledger … are released with
  the code" (line 34).
- `docs/RSNAI_CLAIMS.json` has 54 claims and **none is a data-audit claim**: no entry keys a leak count, a
  manifest hash or an audit verdict to a file. The manuscript sentence is therefore a claim without a ledger row.

What the evidence on disk does give it:

- `or_ready/audit/AUDIT.md` (2026-09-22 00:47, `or_audit_splits.py` + `or_audit_dupes.py`): split disjointness
  by case is clean on all four real-frame sets (0 cases in more than one split, 0 image/meta mismatches), the
  C-ArmLSpine five-fold banks and fine-tune banks put 0 test cases in training, no real test frame is within
  NCC 0.97 of any of 37,165 film images, 29,484 FluoroCap panels or 1,445 detector images, and the 74,364 COBRA
  cross-split near-duplicate pairs are same-gantry-angle laterals of different patients (a positional prior on
  COBRA sacra, read per angle bin — which §3(d) does). **That audit covers the real-frame splits and the level
  banks; it does not cover the devcorpus training lists**, which is E3.
- `docs/DATA_ACCOUNTING.md` is the contract for the full chain — content keys (`sha256`, `pix_sha256`,
  `vol_sha256`), alias classes, patient keys, lineage, and checks CHK-1 to CHK-8 (item disjointness, alias
  closure, patient closure, derivation closure, held-out-whole, near-duplicates, undeclared alias, orphans). Its
  §7 tables are generated and are empty in the repo by design; the chain (`slurm/data_accounting.sh`) writes
  `$OUT/DATA_ACCOUNTING.filled.md` and `leak_report.json` under `or_ready/data_accounting/`, and **that directory
  does not exist on the grid tonight**: the chain has been proved on a planted-leak synthetic corpus
  (`tools/diagnostics/make_fake_corpus.py`) and has not been run on the real corpus.
- `docs/PATIENT_IDENTITY_SPEC.md` (56-agent audit, 9 claims survived adversarial verification) gives the identity
  rules the chain needs and three live leaks it found: VerSe series keyed as subjects in the "clean" v8 bank (five
  people on both sides, 10.5 % of VerSe validation), `anchor_drr` seeded on the implant-variant stem (301 of 801
  people on both sides; `anchor_det_v1` trained on it), and VinDr keyed per image (77.8 % of validation). None of
  those banks feeds this matrix, and they are the reason the standing rule forbids quoting them.

What this matrix adds to the audit, two findings that belong in E3 when it runs:

1. **Design A is not a device hold-out by the plan's own definition.** The plan's rule: a held-out device is absent
   from training frames, training renders' POSES, and the initialisation's calibration terms. Design A renders
   every card under the Cios Fusion pool — 366 DeepFluoro poses over all six specimens, including the test
   specimen 18-1109 (render stems such as `s0224_01_18-1109-098`) — so every design-A arm that "holds DeepFluoro
   out" trained on renders under the test specimen's own poses. Design B does not, and reads higher (94.0 vs 91.6
   on the test specimen; 78.6 / 75.3 vs 72.1 / 77.7 over six specimens), so the exposure did not inflate design A;
   it still has to be stated. The renders-only initialisation carries DeepFluoro's device terms into every arm
   for the same reason (`or_ready/audit/addendum.md`).
2. **The pooled list builder is the only one that refuses.** `devcorpus_build.py lists --design P` raises if a CT
   subject or a real specimen is on two sides; designs A and B write their lists without that check (the held-out
   device's absence is by construction, the styled corpora's shared 17 validation subjects are checked only in P).
   E3 should run the same refusal over every A/B list.

---

## 7. Limits, stated

- One seed for most single-device cells; two seeds for the pairs; two runs at one seed for the S-only list that
  differ by 5 pp. The source contributions (+55 to +72 pp) are far outside that; the design differences (1–7 pp)
  are not.
- The DeepFluoro test split is one specimen. Every one-specimen number here is labelled and none carries an
  interval; the six-specimen row exists only for arms that never trained on the device.
- C-ArmLSpine is scored under the outline convention because that is what every other truth and every render box
  is; the body-convention numbers are in the table and are the mismatch, not the method. The plan's C7 pass
  criterion (≥ 97 % on both) fails on every held-out device under either convention.
- The covariate correlations are over ten cells with three distinct source values; they rank, they do not test.
  The reading in §3 rests on the per-band table, which is a mechanism, not a correlation.
- The pooled design P is not on the sheet yet; the sampling A/B (clip vs typicality corpora) is not on it either,
  so the styled corpora here are the clip-sampled ones with the defect `docs/DEVICE_SPREAD_SWEEP.md` describes.
- Nothing here bears on naming; it is detection recall, which the project's own note calls the binding
  constraint.

---

## 8. The submitted arms, read (21:18 EDT; matrix rerun on 24 arms, 85 cells, self-check 0.0000)

`named_paired_comparisons` in `contribution_matrix.json`; every cell in `contribution_matrix.md` with its file.

| comparison (same frames, same case resamples) | A | B | A − B (pp) | 95 % CI | clusters |
|---|---:|---:|---:|---|---:|
| equal-count E (240 real frames, 10 patients) vs E full (2,640 / 110), held-out C-ArmLSpine outline | 39.0 [33.2, 44.7] | 86.8 [81.1, 91.8] | **−47.7** | [−53.7, −41.8] | 28 |
| equal-count E vs D only at the same training size (3,184 vs 3,180 entries), held-out C-ArmLSpine outline | 39.0 | 12.9 [8.3, 18.1] | **+26.1** | [+18.2, +33.6] | 28 |
| D only, second run vs first run (same list, same seed), held-out COBRA | 38.1 | 38.1 | +0.0 | [+0.0, +0.0] | 27 |
| S only, second run vs first run (same list, same seed), held-out COBRA | 12.2 | 7.5 | +4.7 | [+2.0, +7.5] | 27 |

By angle on held-out C-ArmLSpine (outline; 28 AP, 28 LAT): equal-count E reads **AP 64.3 / LAT 13.9** vertebra
recall and sacrum found 71.4 / 3.6, against the full Elekta arm's AP 95.1 / LAT 78.5 and sacrum 89.3 / 67.9. The
count cut cost 31 pp on the AP frames and 65 pp on the laterals; sacrum on laterals went from 68 % to 4 %. The
DeepFluoro-only arm at the same size: AP 16.1 / LAT 9.7, sacrum 100 / 0. On its own device (in training, 240
frames of 10 patients) the equal-count arm reads 48.5 % on COBRA test against 97.0 % for the full arm, so the
cut hurt in-domain recall by the same order.

What this settles, and what it does not. Count of real frames (and of patients; the two moved together) is a lever
worth about 48 pp on a held-out device, so the small sources' size is a defect of the corpus, not a detail. Content
at equal count is worth about 26 pp in Elekta's favour over DeepFluoro on a lumbar C-arm target, which is the
coverage argument of §3(d) surviving the count confound. What it does not settle is whether repeating the few
frames (a weight) recovers any of the count loss or whether only distinct frames do; `contrib_eqcount_rep11.sh`
is the arm that answers it, about two GPU-hours, not submitted.

**Recommendation, revised on these numbers.** (1) Do not weight by any quality score. (2) The small sources are
under-represented by an amount that costs recall; run the ×11 repetition arm before choosing between a weight and
synthetic expansion. (3) Whichever wins, what must be added is frames at the angles the target shows — laterals
above all — and only the Elekta pose pool or a synthetic sweep supplies them for DeepFluoro and Surgio. (4) Exclude
nothing; the DeepFluoro card's typicality (0.101) is a card defect to fix, and Surgio's −7 pp on COBRA is one cell
on one target against its being the only source of real lumbar laterals.
