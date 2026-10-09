# Handoff, 2026-09-21 afternoon: the CT-to-fluoroscopy formation work, where it stands

Written for the next session (a different model). Read `docs/DEEPFLUORO_FORMATION.md` for the full record;
this page says what is running, what was found today, and the exact next commands. Repo
`spinesurg-ct-nnunet`, branch `L6_Class` (private). Grid `go2432@grid.wayne.edu`; run every network command
through `wsl -e bash -lc '...'`; large outputs go to `/rs/rs_grp_oschome/go2432/` (home is 93 % full).

## What Greg wants (his words, 2026-09-21 ~13:30)

"If the final product of my DRR→physics→smooth filter is close enough to real OR fluoroscopy it doesn't
matter if the detector on DeepFluoro fails to detect sacrums across domains; I'm just trying to make the
DRR→physics in the live-person domain a little more fluoro-like." Then: "do whatever you think will improve
the results on real OR", "get the needed parameters to determine if the final product is close enough to
real OR fluoroscopy from FluoroCap", and "look again for 3D-to-2D registration papers with paired
CT/fluoroscopy datasets; are phantom datasets helpful?" The metric is APPEARANCE on real OR frames, not
sacrum recall.

## Running right now (check these first)

| what | where | done marker | then |
|---|---|---|---|
| the whole chain under the LINEAR reading of the real frame (first run 40406698 done; RERUN **40408457** after the synthetic-conversion fix, `slurm/deepfluoro_linear.sh`) | log `~/model_night/logs/dflinear_40406698.out`; outputs `~/model_night/deepfluoro/{calibration_linear,photons_linear,residual_regions_linear,edge_bias_linear,pedestal_linear,transfer_linear}.json`, `fig_best_synthetic_linear.png`; pairs roots `/rs/rs_grp_oschome/go2432/model_night/anchor_pairs_lin_<spec>` | `LINEAR_DONE` (stage markers `LINEAR_CAL_DONE`, `LINEAR_PHOT_DONE`, `LINEAR_ROOTS_DONE`) | read the exponent sweep: if the best gamma is now ≈ 1.0, the linear reading is confirmed; compare `edge_bias_linear.json` with `edge_bias.json` (does the thin-bone deficit survive?); compare `calibration_linear.json` held-out gains with `calibration_best.json` (+4.3); look at the figure |
| deep-research workflow on paired CT + real-projection SPINE datasets (run `wf_bafbbb6b-f9d`, task `wojzfe0qy`) | transcript `[laptop session folder of the day]/subagents/workflows/wf_bafbbb6b-f9d/` (journal.jsonl holds every agent's return) | task notification | relay the ranked table to Greg; the one-to-obtain-first is the deliverable |
| the OPERATING-ROOM WINDOW experiment (job **40408458**; 40408411 cancelled, `slurm/deepfluoro_orwindow.sh`, queued afterany on 40406698) | log `~/model_night/logs/dforwin_40408411.out`; roots `/rs/rs_grp_oschome/go2432/model_night/anchor_{pairs,none}_lin{roi,or}_17-1882`; `~/model_night/deepfluoro/fluorocap_display_stats_lin{roi,or}.json`, `fig_best_synthetic_linor.png` | `DFORWIN_DONE` | the living-CT training frames (`synthetic_training` column) under `or` should match FluoroCap's p1/p50/p99 and white clip; look at the figure |
| Ljubljana pairs build (`tools/ljubljana_pairs.py`, launched with nohup, see below) | `/rs/rs_grp_oschome/go2432/data/ljubljana/pairs/`, log `~/model_night/logs/ljubljana_pairs.log` | "wrote 18 pairs" in the log | LOOK at the previews (`.../ljubljana/preview/im*.png`); NCC median should be high and the handedness margin large; then run the transfer test and the transferred-terms score (commands below) |

## Found today, in order

1. **Figure 3 reordered** (calibrated | real | refined, signed coloured residuals on the outer sides;
   `tools/deepfluoro_best_synthetic.py`); proposal v5 https://claude.ai/artifact/8uhYki72Jf355qdfLM5N96
   (UTF-8 fixed); manuscript detection subsection finally committed with the six-fold arms (64.0 baseline;
   71.7 / 72.2 / 74.2 for full refiner / high-pass / Fourier swap; 90.0 matched control; 92.3 / 95.0 refiners on
   matched renders). 41 pages, declared 8,308 words, builds clean through WSL (`bash build.sh` in
   `paper/focused`; the declared count on the title page must equal `wordcount.py`).
2. **Residual by region** (`tools/deepfluoro_residual_regions.py`, `residual_regions.json`, all 366 held-out
   frames, display domain): cortical-edge band 7 % of the field, 12.5 % of the residual energy, bias +8.7 grey
   (render too dark); flanks 33 % / 50 % / +3.8; enclosed soft tissue 4 % / 1.7 %; a 12-coefficient smooth field
   removes only 22 %; the refiner leaves every number where it was and adds −11 inside the ring.
3. **Thin-bone effect** (`tools/deepfluoro_edge_bias.py`, `edge_bias.json`): edge bias by bone path at the edge
   0–0.5 cm +1.3; 0.5–1 cm **+62**; 1–1.5 cm **+81**; 1.5–2 cm +48; 2–3 cm +7 grey. Thin bone far too faint, thick
   right. Under the OLD reading of the real frame (see 5).
4. **Remedies measured** (attenuation domain, held-out): linear 4-band enhancement fitted three ways → no
   change (refuted); wide scatter pedestal → monotonically worse (refuted); display exponent a^γ → +3.2 points
   at γ ≈ 1.8–2.0, per-fold optimum 1.6–3.0 (`tools/deepfluoro_bandgain.py`, `tools/deepfluoro_pedestal.py`,
   `pedestal.json`).
5. **THE CONVERSION WAS WRONG** (`tools/deepfluoro_transfer.py`, `transfer.json/png`): the stored DeepFluoro
   intensity is a nearly straight, slightly concave DECREASING function of the model attenuation (exp(−B a)
   fits only with B = 0.15; transmission would give B = 1). The device stores a log-compressed display image and
   `raw_to_atten`'s −log of it was a log of a log. Every term, the photons, every real test frame and items 2–4
   were made against that bent target; the exponent of two was the symptom. Fix: `deepfluoro_calibrate.CONVERSION`
   ("log" default so old numbers reproduce; "linear" = (p98 − r)/(p98 − p2)), `real_to_atten` used by
   `load_pair` and by `deepfluoro_anchor` write_real/evaluate; `DF_CONVERSION=linear` switches every tool;
   `--conversion` on the calibration, recorded in its JSON. Synthetic frames still take −log of transmission.
   The chain is being redone (job 40406698).
6. **FluoroCap display statistics** (`tools/fluorocap_display_stats.py`, `fluorocap_display_stats.json`; 572
   licence-clean fluoroscopy panels, 225 radiographs, 366 DeepFluoro real frames as we window them, 366
   calibrated renders, 400 synthetic training frames; medians, 8-bit, inside the exposed field):

   | statistic | OR fluoroscopy (FluoroCap) | DeepFluoro real, our window | calibrated renders | synthetic training frames |
   |---|---|---|---|---|
   | p1 / p5 | 27 / 47 | 12 / 23 | 15 / 29 | 17 / 38 |
   | p50 | 126 | 101 | 104 | **167** |
   | p95 / p99 | 216 / 239 | 255 / 255 | 236 / 255 | 250 / 255 |
   | white clip (≥253) | **0.1 %** | **6.6 %** | 2.9 % | 3.9 % |
   | std | 49 | 65 | 58 | 60 |
   | top spread p99−p50 / bottom p50−p1 | 100 / 89 | 154 / 88 | 150 / 79 | 88 / 146 |

   Reading: real operating-room frames keep bone BELOW white (0.1 % clipped, p99 239) and sit at mid-grey
   126 with symmetric spreads; our writer's window (`deepfluoro_anchor.window`, central ROI) clips 6.6 % of the
   DeepFluoro real frames white and pushes the top; and the synthetic training frames are windowed
   differently again (mid-grey 167, bottom-heavy). These are the parameters Greg asked FluoroCap for: target
   p1/p5/p50/p95/p99 ≈ 27/47/126/216/239, white clip ≤ 0.1 %. NEXT: make `window()` hit those percentiles for
   real and synthetic alike (a percentile-anchored window), rewrite frames, re-measure. The fine/coarse band
   ratio on FluoroCap is a reproduction statistic and must not be read as grain.
7. **Datasets Greg supplied**: KCL cardiac-sheath (phantom, no use); PIG = Goswami 2020 IOERT pig LOWER LIMB on
   an Elekta kV imager (no spine, no use); infobot = Liu 2019 Med Phys MV portal vs bone DRR (megavoltage, no
   use); Sun 2021 CrossModalNet = same group, 2,698 patients DR vs DRR, code only (verify kV/MV in the research
   report); **Ljubljana 2D-3D gold standard** (Tomaževič 2002): one cadaveric L1–L5 in a water tube, CT 8-bit
   crops (water grey 64, bone max 165, no air → HU slope set so bone max = 1,500 HU, kb absorbs the rest), 18
   Trixell flat-panel radiographs 1560² float at 0.286 mm, air ≈ 500–1255 (transmission-like: use the LOG
   reading for this set), poses exact. Copied to `/rs/rs_grp_oschome/go2432/data/ljubljana/` and unpacked.
   It is a DEVICE-TRANSFER test (different detector, no abdomen), not an appearance target.

## Next commands (in this order)

**Greg's rule (2026-09-21): nothing runs on the login node.** Wrap every Python command below in a small slurm
script (template: `slurm/paired_sets_properties.sh`) and `sbatch` it; only sbatch/squeue/scancel/ls/scp/log
reads happen on the login node. Compute nodes have internet, so downloads go in jobs too.

```bash
# 1. the linear chain (wait for LINEAR_DONE)
ssh go2432@grid.wayne.edu 'grep -E "DONE|^across|^  gamma |bone path|^\s+[0-9.]+ - " ~/model_night/logs/dflinear_40406698.out | tail -40'
# 2. Ljubljana: previews, then the transfer curve and the transferred-terms score (LOG reading for this device)
ssh go2432@grid.wayne.edu 'tail -25 ~/model_night/logs/ljubljana_pairs.log'
#    fetch a few /rs/rs_grp_oschome/go2432/data/ljubljana/preview/im*.png and LOOK (real | DRR | hit)
ssh go2432@grid.wayne.edu 'cd ~/spinesurg-ct-nnunet && DF_CONVERSION=log PYTHONNOUSERSITE=1 ~/mambaforge/envs/fluorogen/bin/python tools/deepfluoro_transfer.py --pairs /rs/rs_grp_oschome/go2432/data/ljubljana/pairs --calibration /rs/rs_grp_oschome/go2432/data/ljubljana/pairs/calibration_transferred.json --out ~/model_night/deepfluoro/transfer_ljubljana.json --fig ~/model_night/deepfluoro/transfer_ljubljana.png'
#    transferred terms vs physics alone on the 18 frames: write a 20-line script using deepfluoro_calibrate.explained / baseline_explained
#    with the frames loaded from that pairs dir and theta = calibration_transferred.json folds[0].theta; also C.fit on frames 0,2,4,.. tested on 1,3,5,..
# 3. FluoroCap-anchored window: change deepfluoro_anchor.window() to hit p1/p50/p99 ≈ 27/126/239 on the exposed field for BOTH real and synthetic frames; rewrite real_test/render_test in the lin roots (`build --real-only`), re-run fluorocap_display_stats.py, then Fig 3 again.
# 4. the research report (workflow wf_bafbbb6b-f9d): relay, and obtain the top-ranked set.
# 5. then: memory + docs + manuscript numbers if the linear reading changed them (Methods say the real frame is "transmission-like" — fix that sentence).
```

## Update at the model switch (2026-09-21 ~14:25 EDT)

**Ljubljana pairs built, not yet trustworthy.** `tools/ljubljana_pairs.py` wrote 18 pairs to
`/rs/rs_grp_oschome/go2432/data/ljubljana/pairs/` (log `~/model_night/logs/ljubljana_pairs.log`, previews
`.../ljubljana/preview/im*.png`, real | DRR | hit). NCC of log-DRR against log-real has median 0.838 (0.57–0.88),
but the detector-handedness test could NOT choose: all four sign choices of the detector axes scored 0.874–0.875
(margin 0.001). The NCC is dominated by the water tube and the circular crop fields, which are symmetric, not by
the vertebra. The CT crops cover only ~20 % of each frame and 30–44 % of that is truncated (rays leave the crop
through water). Before any number from this set is used: decide the handedness from something asymmetric
(the six fiducial balls, 1.5 mm metal, sit OUTSIDE the tube and are visible in the X-rays but not in the crops;
or the spinous process side on the ±90° frames), by rendering all four flips of a lateral frame side by side
and looking. The transfer and transferred-terms commands in step 2 above are otherwise ready to run.

Looked at ~14:28 (`docs/figures_handoff_ljubljana_im004.png`, real left, render right, frame 004 zoomed): under the
chosen orientation (n−1, s+1) the end plates of the lower three levels line up between real and render, so that
orientation is plausible. But the real lumbar column spans about 340 rows and the rendered crops about 260: the
CT crops (z 70–228 mm, 158 mm) cover less than the specimen shows, so the top ~80 rows of the real spine have no
CT behind them and are outside `hit` only if the box excludes them (check). The overlapping crops also leave
bright horizontal bands at each crop boundary, because each crop carries its own water cylinder. Before scoring:
restrict every Ljubljana comparison to pixels whose ray passes through bone of the crops plus a few mm, or
rebuild the volume with the tube water filled analytically (a water cylinder of the tube's radius around the
crops) so that the water path is continuous. Confirm the vertical registration with the fiducial balls.

**Research workflow on paired CT + projection sets: most verifiers failed on the usage limit.** 25 claims were
extracted and none verified; they are in the session scratchpad `research_unverified.md` and summarised here.
Treat every item as unverified until a source is read.

- **COBRA2026 (the lead).** Zenodo 10.5281/zenodo.21322350, arXiv 2607.20037: 867 living pelvic-radiotherapy
  patients, six European centres, measured kV CBCT PROJECTIONS with RTK geometry.xml per scan plus planning CT
  registered to the CBCT. 634 on Elekta XVI (120 kV, 504² at 0.8 mm), 283 on Varian OBI (125–140 kV). Projections
  said to be stored as RAW 16-bit detector signal with air scans supplied (not log): a documented second and third
  device for the display-curve question. Training set 692 cases (~748 GB) open under CC BY-NC 4.0 since July 2026
  via the CREATIS tomoradio-warehouse; validation/test embargoed to 2032; code github.com/cobra-challenge-2026/
  preprocessing. Unknown: whether L4–S1/sacrum are inside the pelvic CBCT field. Fixed linac imager, not a C-arm,
  but living soft tissue and known pose. Next: read the arXiv paper, confirm FOV covers the sacrum, download a
  handful of cases (not 748 GB) to the CephFS volume.
- **SPARE** (Sydney, CC BY-NC 4.0, >200 GB zip): mostly Monte Carlo SIMULATED projections from 4D-Lung CTs; only
  two real clinical scans. Too few.
- **TCIA 4D-Lung**: volumes only; the raw projections are not distributed.
- **MSKCC phantom super-resolution set** (PMC12270334): Varian TrueBeam raw XIM of Rando/LUNGMAN/CIRS phantoms,
  gantry angle only, no planning CT, no data release. No use.
- **Phantom value**: the only statement found was qualitative (phantom training "may generalise poorly"); no
  measured phantom-to-patient appearance gap was found before the run failed.
- Not reached: the JHU/Siewerdsen spine cadaver sets, CAMP/Balgrist/Bern phantom sets, porcine spine C-arm sets.
  Re-run the research with those angles only (the workflow script can be resumed: run id `wf_bafbbb6b-f9d`).

**Sun 2021 (CrossModalNet, PMB 66:175002)** that Greg supplied: 2,698 cervical/prostate RT patients, 0° and 90°
DR vs DRR with radiologist delineations, code at github.com/lc82111/crossModalNet, no data release stated; same
group as the Liu 2019 MV paper, so the DRs are probably portal (MV) images — not confirmed.

**Operating-room window, built (~14:32).** `deepfluoro_anchor.window()` now has a second rule behind
`DF_WINDOW=or` (default `roi` unchanged; in `roi` mode no draw is consumed, so earlier datasets reproduce): the
exposed field's 1/5/50/95/99th percentiles mapped piecewise-linearly onto FluoroCap's operating-room grey levels,
test frames onto the medians 27/47/126/216/239, training frames onto the five targets of one randomly drawn real
FluoroCap panel (`~/model_night/deepfluoro/fluorocap_window_targets.json`, 572 panels, written by
`tools/fluorocap_display_stats.py --tuples-out`). Every call site now passes the exposed field. Caveat: FluoroCap
panels are a mixture of bone-dark and bone-white displays; the targets are not separated by polarity.

**The linear refit is in (14:36 EDT, `calibration_linear.json`).** Reading the DeepFluoro frame as the log image it
is raised physics-alone agreement over all frames from 80.0 % to 86.2 %, and the held-out calibrated agreement by
specimen from 86.8/87.9/83.4/77.5/87.8/86.1 % to 90.0/94.3/89.3/78.9/90.9/91.2 %. The bone term kb, pinned at its
2.5 bound in every fold under the old reading, now sits inside its box at 1.97 (spread 0.19 across folds): the
"open item" of reparameterising kb was the conversion. The nine terms now add a median +1.7 points instead of
+4.3, so part of what they fitted before was the misreading. Caveat: the two readings are different targets, so
the explained-variance comparison is not strictly like for like; kb leaving its bound and the transfer curve are
the independent evidence. Photons, roots and the re-measurements are still running in the same job.

**New dataset leads from the relaunched search (verification still running, treat as unverified):**
- **Balgrist lumbar set (Jecklin et al. 2024, Med Image Anal 98:103322, PMID 39197301; follow-up paper).** 13
  fresh-frozen WHOLE-TORSO cadavers, L1–L5, CT on a Siemens SOMATOM Edge Plus at 0.75 mm, real C-arm X-rays from a
  Siemens Cios Spin (flat panel) and, for some specimens, a Ziehm Vision and a Ziehm Vision FD; 1,017 paired
  images, gantry swept in 3° steps to ±102°. Not public (pending patents); "available on reasonable request" from
  [address withheld; the corresponding author of Jecklin et al. 2024, Med Image Anal 98:103322, PMID 39197301, Balgrist University Hospital] (ROCS group, Esfandiari/Fürnstahl). This is the set that fills the gap: lumbar spine,
  intact soft tissue, three mobile C-arms, pose known.
- **DeepFluoro's original vendor DICOMs**: JHU Data Archive doi:10.7281/T1/C304HZ (linked from the DeepFluoro
  README since 2023-03-20). The Siemens Cios DICOM conformance statement (VA20) says the Cios writes the Pixel
  Intensity Relationship (0028,1040: LIN or LOG) into every XA image. Reading that tag settles the log-image finding
  from the source.
- **Hip gold standard (D'Isidoro, Chênes, Ferguson, Schmid, Med Phys 2021, doi:10.1002/mp.15124)**: public on
  Yareta (doi:10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu, 394 MB): a resin hip phantom with lumbar segments, one
  CT, 19 real frames on a Philips BV Pulsera IMAGE-INTENSIFIER C-arm at several kV/mAs. A third device, public now.
- Charters et al. (UCLA): kV radiotherapy setup radiographs of T2–L2 paired with planning-CT DRRs via DICOM REG;
  access unknown. Flepp et al. 2025 (IJCARS): 49 cadaveric distal-femur X-rays with CT (xvr's extra test set).
- DiffDRR/DiffPose/xvr's "Ljubljana" set is the CEREBRAL ANGIOGRAPHY gold standard (10 patients), not Tomaževič's
  spine set; the spine set Greg holds is rarely used.

**14:55 EDT: first linear chain finished, and it exposed a second inconsistency (fixed, rerunning).**
- Attenuation domain (calibration and sweeps use `forward`, plain −log T): the display-exponent sweep now peaks
  at γ = 1.2 with 89.3 % against 89.1 % at 1.0, flat around one (it peaked at 1.8–2.0 with +3.2 under the old
  reading), so the linear reading is confirmed. The thin-bone edge bias in attenuation units nearly vanished.
- Display domain (the 8-bit frames the detector sees): region residual explained 69.3 → 72.3 %, but the thin-bone
  edge bias stayed large: +57/+65/+34 grey at 0.5–1/1–1.5/1.5–2 cm (was +62/+81/+48).
- Cause found by reading the code: every DISPLAYED synthetic frame (render twins, training frames, living-CT
  renders) went through `forward_noisy` → `raw_to_atten`, which subtracts the frame's own 2nd-percentile
  TRANSMISSION before the log: a different conversion from the plain −log T the terms were fitted on. Fix:
  `deepfluoro_calibrate.synth_to_atten` returns −log(max(T, half a count)) under the linear reading (old
  behaviour kept under "log"); the photon fit uses the same. Whether this was the cause of the displayed
  thin-bone deficit is a HYPOTHESIS until the rebuilt frames are measured: a toy check showed the old bend's
  direction depends on which pixels sit near the 2nd percentile.
- Everything made with the bent conversion was moved aside, not deleted: `*_linear_p2bend.json`,
  `fig_best_synthetic_linear_p2bend.png`, roots under `/rs/rs_grp_oschome/go2432/model_night/p2bend/`.
- Rerunning: linear chain **40408457** (skips the calibration, refits photons, rebuilds six roots, re-measures),
  then the window test **40408458** (afterany). The earlier window job 40408411 was cancelled.

**15:20 EDT: the thin-bone finding was an artifact, and it is withdrawn.**
- The rebuilt roots (consistent synthetic conversion) still showed +54/+66/+45 grey at thin-bone edges, so the
  conversion hypothesis was refuted.
- The cause was the measurement: the bone mask was intersected with the exposed field, so the collimator border was
  counted as a bone edge wherever bone crossed it. 23 px inside the field the bias is +5.8/+3.0/+0.8 grey.
- The real mismatch is the collimator border: the outer 23 px ring is 22.5 % of the field and 68.6 % of the residual
  energy, the real frame 23 grey brighter (penumbra fall-off vs the render's hard edge). NEXT formation term to
  model: a collimator penumbra at the field edge.
- Corrected in the manuscript (Results: border finding; a new paragraph on the stored log image; the detection
  results marked as rendered under the original reading; 42 pages, 8,514 words, builds clean), in the proposal, and
  in DEEPFLUORO_FORMATION.md (correction notes on both sections).

**Datasets, verified by the two searches (reports in `docs/research_paired_ct_projection_verified_2026-09-21.json`
and `docs/research_datasets_missed_verified_2026-09-21.json`):**
- COBRA2026 (open): 867 living pelvic RT patients, raw LINEAR uint16 kV CBCT projections (Elekta XVI 120 kV no grid;
  Varian 125–140 kV grid) with RTK geometry and planning CT; CC BY-NC 4.0; spine/sacrum coverage unverified.
  Overview PNGs downloaded to `/rs/rs_grp_oschome/go2432/data/cobra2026/COBRA2026_Train_overviews.zip` (699 files).
- LUMOS (open, Zenodo 18173664, Zhejiang, ACM MM 2025): 803 living patients, 1,620 lumbar AP/LAT diagnostic
  radiographs (Philips DigitalDiagnost), 280 lumbar CTs; ids 1–280 probably paired (unconfirmed); no pose; CC BY-NC.
- On request: Balgrist (email drafted); UCLA Charters 2,486 paired kV setup radiographs of the thoraco-lumbar spine,
  254 living patients, pose from DICOM REG ([address withheld; the UCLA corresponding contact for the Charters paired-radiograph set]); Huashan/Fudan 140 living patients with preop
  lumbar CT and INTRAOPERATIVE AP/LAT films ([address withheld; the Huashan Hospital / Fudan University corresponding contact]); JHU I-STAR real cadaver long films (Huang 2022, 13
  cadavers, 100 labelled; Siewerdsen now at MD Anderson); Siemens/FAU 55-patient thoracolumbar CBCT sweeps
  (Jaganathan, unreleased); SheepSpineX (sheep cervical, image intensifier, [address withheld; the Shanghai Jiao Tong University corresponding contact for SheepSpineX]).
- No public living-patient intraoperative lumbar fluoroscopy with vertebra labels was found.

**COBRA2026 integration (16:00-16:30 EDT).** Greg supplied the dataset paper (`CTSpinoPelvic1K-1/COBRA.pdf`).
- Released volumes are LPS (+x left, +y posterior, +z superior) with origins shifted to the CBCT isocentre; Elekta
  frames are raw linear detector signal, vendor flood-field applied, scalar I0 from the .INI (paper Sec. II.B).
- `tools/cobra_fetch.py` (Girder API of tomoradio-warehouse.creatis.insa-lyon.fr; training folder
  69b93ca75363131190cefb54): six cases on CephFS `/rs/rs_grp_oschome/go2432/data/cobra2026/cases/{A002,A004,A005,
  F011,F041,F051}`; every case's metadata.yaml under `.../meta/` (`--meta-all`).
- `tools/cobra_pairs.py`: renders ct_def.mha under each frame's RTK matrix after searching 16 signed maps from LPS
  to the RTK world. Case A004: best map rtk_x = +pat_y, rtk_y = -pat_z, rtk_z = +pat_x, NCC(log real, log render)
  0.945-0.994 at every gantry angle (12 frames). The runner-up (rtk_z = -pat_x, a left-right mirror) is only 0.009
  behind on the body, so `slurm/cobra_handedness.sh` (job 40409409) scores all maps against the authors' own
  `projections_simulated.mha` (same CT, no bowel motion) by intensity and by edges. DO NOT build pairs at scale
  until that settles the mirror. Then `sbatch slurm/cobra_pairs.sh` (six cases, pairs + transfer test on a device
  documented LINEAR: it must find an exponential with decay near one).
- `tools/paired_sets_properties.py`: DeepFluoro vs COBRA per centre (kV, mAs/frame, frames, pixel pitch, CT slice
  and pixel, age, view angles, a facts table). DeepFluoro's DATA licence is CC BY-NC 4.0 (checked on the GitHub
  README; not SA).
- LUMOS (Zenodo 18173664, checked on the record): 803 patients, 1,620 lumbar AP/LAT radiographs, 280 lumbar CTs,
  CC BY-NC 4.0, 46 GB; labels are DXA values and osteoporosis class only; no pose; CT-radiograph id pairing
  undocumented.

**COBRA orientation settled (job 40409409).** Case A004, four oblique frames, mean NCC of the chosen map
(rtk_x = +pat_y, rtk_y = -pat_z, rtk_z = +pat_x) against its left-right mirror:

| reference | score | chosen | mirror |
|---|---|---|---|
| authors' simulated projections | intensity | 0.996 | 0.982 |
| authors' simulated projections | edges | 0.777 | 0.471 |
| real projections | edges | 0.656 | 0.309 |

Intensity cannot separate the mirror of a near-symmetric pelvis; edges can, so `cobra_pairs.py` now searches on body
edges (warns below a 0.10 margin). Six-case build + transfer test: job 40409822 (`slurm/cobra_pairs.sh`), markers
COBRA_PAIRS_DONE / COBRA_DONE, outputs `/rs/rs_grp_oschome/go2432/data/cobra2026/pairs/`, `transfer_cobra.{json,png}`.
Properties figure: `docs/figures_paired_sets_properties.png`. Third dataset search running (wf_6bbb117b-d0c).

**DeepFluoro's original vendor files (checked through the Dataverse API, 16:55 EDT).** Grupp, Unberath, Gao et al.,
"X-ray computed tomography and fluoroscopy collected during cadaveric periacetabular osteotomy experiments", JHU Data
Archive doi:10.7281/T1/C304HZ, released 2022-03-30, CC BY-NC 4.0, unrestricted, 19 files, 38.3 GB: original DICOM of
19 CT scans (pre- and post-operative, six cadavers) and 2,659 fluoroscopic images (DeepFluoro released 366), plus a
sawbones pelvis and the FTRAC fiducial; 01_Readme.pdf and 02_fluoroscopy_rotations.tab explain them. Plain curl gets
a Cloudflare 403; `tools/jhu_dataverse_info.py` / `tools/jhu_dataverse_fetch.py` use curl_cffi. Download: job
40409951 (`slurm/deepfluoro_vendor_fetch.sh`, resumable) to `/rs/rs_grp_oschome/go2432/data/deepfluoro_vendor`.
First use: read (0028,1040) Pixel Intensity Relationship, kVp and exposure from the headers.

**Geneva hip gold standard: the verifiers refuted the CLAIMS, not the data.** D'Isidoro, Chênes, Ferguson, Schmid,
Med Phys 2021 (doi:10.1002/mp.15124); Yareta doi:10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu, public, no DUA,
CC BY-SA 4.0, 413 MB. Verified by reading the paper, its supplement and the archive: one phantom (female pelvis,
proximal femurs and lumbar segments in soft-tissue-equivalent resin), one CT (Philips Brilliance 64, 140 kV,
0.78x0.78x1.0 mm), a Philips BV Pulsera IMAGE-INTENSIFIER C-arm, 19 poses with 3-10 exposures each at 62-110 kV:
116 real fluoroscopic TIFFs, distortion-corrected (supplement Appendix 1), ~0.29 mm pixels, pose from 21 beads + VICON
(accuracy 0.12-0.29 mm projection distance; the paper's own preferred uTRE is 0.59 mm). Sacrum in the field. The
same pose at several kV is the direct test of the spectrum/bone term.

**C-ArmLSpine (third search, 17:10 EDT; the best open find of the day).** Zenodo 10.5281/zenodo.22768651, published
2026-09-17, CC BY 4.0 (commercial use allowed, no DUA), one 15.6 GB zip (MD5 6bccd47979a2a1c9b200dc427fefeb54).
Southern Medical University (Feng Qianjin; PRSCS-Net, Zhang et al., Med Image Anal 97:103283, 2024;
github.com/ZWC-SMU/C-ArmLSpine). 149 intraoperative spine cases, each a real AP and a real LATERAL C-arm frame
(C-arm/0001.dcm, 0002.dcm) plus a CBCT (CBCT/, ~394 slices) from ONE mobile C-arm model, the FIRST Surgio-B51
(flat panel likely, not verified). Unknown until opened: geometry linking frames to CBCT, levels in the field, sacrum,
labels, intensity form, living vs cadaver. Job 40409970 (`slurm/carmlspine_fetch.sh`): download, MD5, unzip,
`tools/inspect_dicom_tree.py` on six cases → `/rs/rs_grp_oschome/go2432/data/carmlspine/inspect.json`.
Other third-pass finds: PENGWIN Task 2 (Zenodo 10913196, CC BY 4.0) is 50,000 SYNTHETIC pelvis DRRs with sacrum/ilium
masks; FluoroSAM Loop-X full-torso cadaver (JHU, unreleased, ask Killeen/Unberath); Vanderbilt THA 336 labelled AP
intraoperative frames (L5/S1, SI joints; unreleased, no route); RadGS-Reg 10 cases (unreleased); Sina Tehran 300 AP
pelvis radiographs + CT (on request per Frontiers 2024); TCIA CT Colonography localizers (up to 754 patients);
Marques & Pina 2026 printable fluoroscopy phantom STLs (Zenodo 18827666) for per-machine measurements on our own
C-arms. Full report: `docs/research_datasets_third_pass_verified_2026-09-21.json`.

**The log finding passed its outside check (17:30 EDT, job 40409822).** `tools/deepfluoro_transfer.py` on COBRA
(documented LINEAR signal; 154 frames, 3 Elekta + 3 Varian cases): transmission form best on 92 % (calibrated terms)
and 100 % (baseline) of frames, decay B = 0.67-0.68, linear R2 0.83 (worst). DeepFluoro: transmission best on 3-22 %,
B 0.15-0.18, linear R2 0.985. The test discriminates; DeepFluoro stores a log image. Manuscript sentence added.
Varian geometry still weak (log NCC 0.61-0.95, edge 0.15-0.25); Elekta 0.985-0.991.

## Traps met today

- Patch scripts must match the file: `patch_ms12` claimed success but its text never reached the committed
  `main.tex` (the commit did not include the file); verify with `grep` before believing a patch.
- `python` on Windows reads JSON in cp1252 unless `io.open(..., encoding="utf-8")`: that produced the mojibake
  in the proposal.
- `scp` of a tool from a `cd`-relative path silently failed once; use absolute `/mnt/c/...` paths.
- The bandgain fit's per-frame gains scatter ±5 because whole-field least squares is set by flank texture; a
  term that exists for edges must be scored on edges as well as the field.
- Inline python heredocs collapse backslashes; Write the script, run by path.

## C-ArmLSpine is the project now (Greg, ~18:20 EDT)

"I have actual fluoro spine data; if I can run the cropping + detector experiment to identify levels on limited FOV
in the OR fluoroscopic domain, even thoracic, that is all I need." COBRA/DeepFluoro/Geneva/LUMOS are back-burner
(use only for a fluoroscopic pelvis C-ArmLSpine lacks; it has the sacrum, so none needed now).

**What the archive is (read from the files, 2026-09-21):** 149 case folders; 147 = C-arm/ (2 frames) + CBCT/ (394
slices); case134 has no frames; case39 has 3 frames + 696 CBCT files. 38 cases name files by UID. Frames: XA,
Yiying (FIRST) Surgio-B51, station YiYing_3DCarm, 2048^2 uint16, MONOCHROME2, transmission-like (gas bright, bone
dark), PIR empty, "DR"/single-frame, kVp 73-98, 25-27 mA; SID 1140, SOD 745; PositionerPrimaryAngle 0 (AP) / 90
(LAT); private (0029,0033) "30cm" = detector -> 0.1465 mm pixels (DICOM PixelSpacing 1.0 is a placeholder).
CBCT: 394^3 x 0.5 mm centred on (0,0,0) = the detector field at the isocentre (300/1.53 = 196 mm); FFS; frames taken
~1-2 min BEFORE the CBCT. No annotations seen; no FrameOfReferenceUID anywhere (inspect_dicom_tree's "shared: True"
was None == None, fixed). Metal markers/needles visible in several cases. Institution SMU, Nantong (Jiangsu).

**Traps:** (1) every CBCT slice has its own SeriesInstanceUID -> GDCM series grouping returns ONE slice; read with
`tools/carmlspine_io.read_cbct` (by position). (2) SPINEPS runner harvested the RAW instance mask (ids 1..N, no
VERIDAH names) -> fixed `benchmark/run_spineps_cases.py` harvest (prefers non-raw derivative, writes
<case>_harvest.json); `tools/spineps_relabel_from_poi.py` restores names from ctd.json either way. (3) remote logs
piped through grep are block-buffered: use `grep --line-buffered`.

**Pose (tools/carmlspine_pose.py):** header geometry + edge-only registration. Device convention (6-case pilot):
AP dir(0,-1,0)_rot180_m-1 (6/6), LAT dir(1,0,0)_rot180_m-1 (4/6; rival = left/right beam, near-identical
projection). Refine from the consensus: in-plane shift 1-3 mm, depth +7-18 mm (systematic: SOD calibration?),
rotation 1-5 deg; case17/case19 low edge (check). Jobs: pilot 40410317, refine array 40410328.

**Pipeline (all written):** `carmlspine_nifti.py` (array 40410341) -> `slurm/carmlspine_label_chain.sh` (40410342:
TS + SPINEPS arrays + survey) -> `tools/carmlspine_labels.py` (truth: agreed level, SPINEPS corpus body box,
upright turn from pose, OR window) -> `tools/carmlspine_eval.py crops` (k=1..5 windows) -> `slurm/carmlspine_proto.sh`
(level_prototype with detector or `--boxes-dir` oracle boxes, `--no-orient`) -> `carmlspine_eval.py score`.
Frames job 40410355 (images + pose contact sheets in data/carmlspine/qc/). Data: /rs/rs_grp_oschome/go2432/data/
carmlspine, /rs/.../realxray/carmlspine[_crops]. Thoracic reach: CBCT field ~L1/T12-S1; T12/T11 at most.

**C-ArmLSpine, later findings (19:30-20:00 EDT).**
- Detector named: private tag (0037,0014) = `C:/FICBCT/IRayJupi1212X/FICBCT_3DC_110kv_300_FDK_noSC_AutoMA` -> iRay Jupi1212X
  flat panel (30 cm), CBCT = 300 projections, FDK, no scatter correction, 110 kV auto-mA.
- TWO raw CBCT projection sweeps ship: case134/ori (the case with no AP/LAT frames) and 301 XA files inside
  case39/CBCT. 1024^2 uint16, 111 kV, 12-13 mA, PositionerPrimaryAngle +122 -> -52 deg (58 distinct readings, so the
  per-frame angle is quantised). Case39's CBCT is reconstructed from its own sweep: a same-device registration test at
  known angles (not yet run).
- Labeller comparison (fixed): 910 vertebrae, 814 agree, 41 disagree, 55 unmatched fragments, 22 variant cases
  (case136 VERIDAH L2-L6 = six lumbar; case148 one level up; case132 L5 merged into sacrum; case129/149 T12 read T11).
- TotalSegmentator v2 `sacrum` excludes S1 (disjoint `vertebrae_S1`; all 1,228 TS subjects): C-ArmLSpine sacrum truth
  now = sacrum + S1 (job 40410633 segments S1). Box effect small (IoU 0.89-0.92), end-plate effect large.
- No CBCT contains a femoral head (0/31 checked, femur masks empty): PI is not measurable on C-ArmLSpine.
- Pelvic landmark set (agent): /rs/.../realxray/pelvis_landmarks/ (COBRA 130 cases, 519 PI-measurable laterals, 2-D PI
  error median 0.55 deg; femoral heads 2.71 mm median vs DeepFluoro experts; COBRA PI 52.7 +/- 10.4).
- Queue: zero-shot prototype 40410577-82 -> frames2 40410634 (after S1) -> fine-tune mix 40410635 -> realonly 40410636;
  catalogue 40410657 -> survey 40410658. Verified report: docs/research_sim_real_mixing_verified_2026-09-21.json
  (mix, do not pretrain-then-fine-tune, when the real set covers only some levels).

**C-ArmLSpine level results (22:00 EDT).** Scores are exact-level accuracy against CBCT truth (two agreeing labellers),
case-bootstrap CIs, detector boxes unless noted. Files: docs/carmlspine_*_2026-09-21.json.
- Pose: laterals were fixed by BOUNDING registration around the header geometry (5/5/25 mm, 6 deg; tag _ref2): 16/146
  laterals had jumped 8-25 mm to a half-vertebra neighbour optimum; now 1 frame > 0.25 body (detector-box pose QC,
  tools/carmlspine_pose_qc.py). AP was fine throughout.
- Zero-shot (allspine_v2_r1 + head_k3, never trained on C-ArmLSpine), all 148 cases: LAT whole frame 96.3 %
  [92.9, 98.9], frame-exact 95.7 %; 5 vert 90.3, 3 vert 86.9, 1 vert 63.1; AP 37.9 % (one-level cranial shift).
- Test split (28 cases): mixed fine-tune (C-ArmLSpine train crops ~1:1 with allspine_v7 sample; model
  carm_mix_fov96_ctx/runs/model_rung_1_ft_mix_aug2.pt, head heads_carm/head_mix.pt) LAT/AP whole 94.6/95.2, 5 vert
  94.9/93.1, 3 vert 87.4/86.4, 1 vert 70.8/62.7. Real-only fine-tune LOST laterals at 3-5 vertebrae (77.1-83.8) and
  forgot more (NHANES renders 77.3 vs 83.4 mixed) -- as the verified mixing report predicted.
- Running: 5-fold CV of the mixed fine-tune (40411133, all 148 cases, oracle + film detector); box detectors
  fine-tuned on real frames (only:carmlspine 40411128, pooled 40411130) with end-to-end naming (40411129/31).
- Corrections committed for the next rebuild: panel 307.2 mm (iRay Jupi1212X 150 um; the depth shift was compensating
  a 2.4 % pitch error), case134 frames live in CBCT/, case118 is AP + -58 deg oblique (OBL, unlabelled).

**C-ArmLSpine headline (five-fold CV, 23:00 EDT)** -- docs/carmlspine_cv5_mixed_2026-09-21.json, figures
docs/figures_carmlspine_{results,gallery,survey}.png. Film keypoint detector (never trained on C-ArmLSpine) + a
mixed fine-tuned level model and mixed-length head per fold (tools/carmlspine_*; slurm/carmlspine_cv.sh):
- LAT exact: whole 98.2 [95.7, 100] (frame-exact 97.9), 5 vert 97.0, 4 95.7, 3 92.9 [89.6, 95.6], 2 89.5, 1 72.8.
- AP exact: whole 96.7 [93.6, 99.1], 5 95.1, 4 94.0, 3 86.3, 2 79.8, 1 65.1. Within-one ~100 % at >= 3 vertebrae.
- Detection (share of named truth bodies found): LAT 91.3 whole -> 78.2 at 1 vertebra; AP 93.8 -> 80.3.
- Box detector fine-tuned on whole C-ArmLSpine frames (rx_only_carmlspine_1024): sacrum 98.2 %, vertebra recall 89.9 %
  (IoU 0.5), sacrum-anchored counting 93.4 % per vertebra; better recall on whole frames, collapses on crops (42 % at
  1 vertebra) -> crop-augmented detector (rx_only_carmlspine_multi_1024, job 40411213) and pooled (40411130) pending.
- Failure mode (gallery case83): S1 boxed as a vertebra and named L5, shifting the run one level up.
- Thoracic: not testable here (T12 in 12.8 % of CBCTs, 2 % complete; T11 one case).

## 2026-09-22 00:30 EDT -- OR-readiness adversarial program (workflow wf_093f2c0a-dd0)

**Correction on record.** "The pooled detector finds the sacrum on 100 % of DeepFluoro test frames" is a SAME-DEVICE,
held-out-SPECIMEN number: rx_pooled_1024 was fine-tuned on real frames incl. four DeepFluoro cadavers on the same
Cios Fusion. It is NOT the manuscript's render-only method (76.9 %). The out-of-the-box question is answered only by
the device-held-out arms (rx_lodo_*; jobs 40411285-7) and by Geneva (never trained by anyone).

Five parallel agent tracks, outputs under /rs/rs_grp_oschome/go2432/data/or_ready/<track>/ and the scratchpad:
1. audit: split disjointness, cross-split near-duplicates, what each model saw (render-only detector: DeepFluoro
   poses of all specimens + calibration terms; film detector corpus; allspine_v7 sources; CV banks), truth
   construction limits. AUDIT.md + lineage figure.
2. wholespine: 3-class (vertebra, sacrum, c2) box detector, MIXED (real C-arm frames upweighted + film corpus +
   anchor_drr_c2 renders + calibrated renders), arms mixed / real-only / renders-only; tested on held-out cervical
   films (C2), each device's test split, Geneva, FluoroCap panels, and AASCE whole-spine films if fetchable.
3. lodo: recall-vs-confidence curves for every detector x device, held-out status labelled; end-to-end k-crop run
   with the device-held-out detector (TAG lodo_det).
4. robust: fluoro corruption suite + needles + 180-deg flip + collimation on real test frames; curves + heatmap.
5. crossdev: COBRA SPINEPS rerun (fixed harvest) -> levels; C-ArmLSpine-fine-tuned level model on COBRA living
   laterals and DeepFluoro cadavers (oracle + detector boxes); sacrum-anchored counting there.
Then one synthesis agent -> evidence table. Report to Greg as an artifact when it lands.
- First device-held-out number (job 40411286, rx_lodo_cobra_elekta_1024: trained on C-ArmLSpine + DeepFluoro real
  frames, COBRA never seen): COBRA test sacrum found 13.3 %, vertebra recall 18.5 % (AP50 0.20). Same-device pooled
  detector on COBRA test: sacrum 97.9 %, vertebra 97.4 %. Scale confound to check: at imgsz 1024 COBRA is ~0.39 mm/px
  vs C-ArmLSpine ~0.20 and DeepFluoro ~1.2 mm/px.
- POSITION PRIOR on COBRA (tools/or_position_prior.py, or_ready/prior/): the pooled detector's sacrum hit rate is
  98.4 % in the LOWEST-contrast quintile of COBRA test frames (box-region std 3-15 grey, mean grey 205 = near white),
  vs 96.7 % in the highest. It places the sacrum from frame layout. Cause: cobra_elekta was windowed over the exposed
  FIELD (half air on laterals) -> body collapsed into the top grey levels. Re-windowed on the body ->
  cobra_elekta_v2 (jobs 40411348 array, eval 40411349: render-only / COBRA-held-out / pooled on both displays).
  Same-device COBRA detection numbers are NOT evidence of anatomy detection until re-scored on v2.
- Scale at imgsz 1024 (truth vertebra box height): COBRA 140 px median, DeepFluoro 203 px.
- COBRA re-windowed on the body (cobra_elekta_v2, before_after.png): laterals STILL show no vertebral structure -> the
  laterals are photon-starved (40 ms x 64 mA through a full pelvis, no grid), not mis-displayed. COBRA tests
  detection only on views with visible bone. Per view (sacrum-found % / vertebra recall %, test split, v2 display):
    render-only (zero real)      AP<=15: 81/61   15-45: 47/69   45-75: 3/23   LAT: 0/16
    lodo_cobra (C-arm real ft)   AP<=15: 43/58   15-45: 18/32   45-75: 0/4    LAT: 0/5
    pooled (same device)         AP<=15: 100/99  15-45: 98/100  45-75: 97/96  LAT: 98/96   <- position prior beyond 45 deg
  Fine-tuning the render detector on two real C-arm devices made COBRA transfer WORSE than renders alone (43 vs 81 %
  sacrum near-AP): forgetting of render diversity; argues for MIXED training (track 2 tests it).
  Files: or_ready/rewindow/{render,lodo_cobra,pooled}_cobra_elekta{,_v2}_test.json.
- Bone-visible COBRA subsets (tools/realxray_subset_view.py): cobra_elekta_v2_ap45 and cobra_elekta_ap45 (|angle
  from AP| <= 45). Any detector TRAINED on full-orbit COBRA learns a position prior from the blank laterals; track 2
  (wholespine) used full-orbit cobra_elekta train/val -- re-check its COBRA contribution against the ap45 subset.

**Fourth dataset search (wf_b878ce6b-3b6, 134 agents, 344 queries; docs/research_datasets_fourth_pass_verified_2026-09-22.json).**
New and open: SpineSAC (IIT Madras; 58 AP/LAT REAL C-arm pairs of lumbar sawbones phantoms from FIVE devices -- GE OEC
FluoroStar, Skanray, Ziehm EXP8000, Siemens Cios Select, Siemens XA -- with MDCT and per-scenario 3x4 matrices; no
data licence; processed PNGs); RTK public Elekta projections (3 subjects, Kitware); TROG SPARK (960 GB prostate kV,
L5 absent: useless); Giessen canine biplanar (request). Updates: xvr-data on HF re-hosts DeepFluoro/Ljubljana with
poses; UCLA Petragallo 2023 = 429 spine-RT patients with ExacTrac kV + CT (request); TVGH-SpineXR (IEEE DataPort)
= diagnostic full-spine radiographs with vertebra levels (radiograph level-ID only); Balgrist public subset does
not exist (patents); Utrecht gold standard lost. C-ArmLSpine dossier (25 items): the PDF Greg attached (PG-Net) is
unrelated; frames are processed display images; all 149 cases fall on five days ~4 min apart with no
instrumentation ("routine intraoperative" is doubtful; living vs cadaver unknown); raw sweeps carry a second
near-raw frame in private tag (0037,0020); PRSCS-Net's own C-ArmLSpine numbers unread (paywall).
- Two more agents launched 01:40 EDT: SpineSAC five-device C-arm phantom test (or_ready/spinesac/; detectors
  render-only, rx_only/pooled/lodo, film keypoint, anchor_c2, wholespine-mixed when available) and a real
  whole-spine radiograph thoracic test (AASCE/BoostNet or TVGH-SpineXR if openly fetchable; or_ready/thoracic/).
- Crop-trained C-ArmLSpine box detector (rx_only_carmlspine_multi_1024, frames + k-crops) end-to-end on the 28 test
  cases with the mixed level model + head (docs/carmlspine_ftdet_multi_test_2026-09-22.json): LAT exact whole 97.4
  [91.6, 100] / 5 vert 92.2 / 3 vert 89.8 / 1 vert 72.1; AP 95.9 / 92.2 / 90.4 / 66.7; body recall at 1 vertebra
  LAT 84.9 % (whole-frame-trained pooled detector: 11.2 %; film keypoint detector: 74.3 %). SAME-DEVICE ONLY: this
  detector finds 1.1 % of COBRA and 2.2 % of DeepFluoro test vertebrae. Pooled detector end-to-end: LAT whole 93.1,
  AP whole 100 (n 125), but 1-vertebra LAT 17.6 % (docs/carmlspine_ftdet_pooled_test_2026-09-22.json).
  Pattern so far: detectors fine-tuned on real frames of one device family do not transfer (COBRA-held-out 43 % vs
  render-only 81 % sacrum near-AP; C-ArmLSpine-only 2 % on DeepFluoro). Renders transfer; real fine-tuning specialises.

## 2026-09-22 02:10 EDT -- Greg's plan: k devices, one network

Devices are measured domains (one-device real fine-tunes collapse elsewhere; renders transfer). Plan: fit a per-device
formation parameter set (fixed: detector, geometry, transfer curve, processing chain, field; per-exposure: kV/mA/
window sampled from each device's observed range), render whole spines ONCE per geometry family and STYLE per device
on the fly (tools/device_style.py, coming), mix upweighted real frames, train with leave-one-device-out on renders
and test on the held-out device's REAL frames. Launched: deep research on every C-arm dataset in existence (any
anatomy; paired CT+pose ranked first; device-characterisation sets; device census k) = wf_5c6cf903-03a; device-fit
agent (docs/devices/<device>.json, SCHEMA.md, tools/device_fit.py, tools/device_style.py; C-ArmLSpine display stage
from the raw-sweep twins in private tag (0037,0020)). Corpus + LODO training follow when both report.
- Refinement (Greg): each device is fitted as a DISTRIBUTION: per-frame exposure terms; the automatic exposure control
  learned as a conditional (kV, mAs given water-equivalent thickness at field centre from the registered CT);
  empirical joint (copula/KDE) plus documented spec ranges with a margin; device_style --randomize samples the
  conditional; COVERAGE CHECK = share of held-out real frames whose fitted terms fall inside the sampled 1st-99th
  percentiles, per term and jointly, with a sampled-cloud-vs-real figure. Sent to the device-fit agent.
- Refinement 2 (Greg): the style pipeline stays fully PARAMETRIC (no learned filter) so unpaired devices can be
  styled from headers + spec sheet + image statistics. Device-fit agent told to (A) record a physics default next to
  every fitted term (spectrum from kVp via SpekPy/NIST instead of free kb; SPR from thickness/field/grid; MTF from
  scintillator + pitch; photons from mAs/SID/DQE; collimator penumbra; heel effect; II vignetting/glare; display
  chain from edge-halo profile, NPS, histogram), (B) an unpaired-device path validated WITHOUT CT by NPS / histogram
  / edge-halo / gradient distances, demonstrated on a paired device treated as unpaired, (C) keep a new physics term
  only if it raises held-out R2 (penumbra first).
- Device CENSUS agent launched 02:50 EDT (docs/devices/census/<device>.{md,json}, tools/device_census.py,
  or_ready/census/): every DICOM tag incl. decoded private binaries, exposure-field distributions, image statistics
  (NPS, edge halo, histogram, border penumbra, log-vs-linear from noise-vs-mean), spec-sheet lookups, cross-device
  figure. DeepFluoro VENDOR DICOMs: first fetch (40409951) OOM-killed at 4 GB with nothing on disk (curl_cffi queued
  the streamed body); tools/jhu_dataverse_fetch.py now writes through content_callback with Range resume; refetch
  job 40411582 (24 h, 16 GB) -> /rs/.../data/deepfluoro_vendor/, marker DFVENDOR_DONE.

## Overnight 2026-09-22 (Greg asleep from ~03:00 EDT). START HERE IN THE MORNING.
Read, in this order: docs/MORNING_REPORT_2026-09-22.md (corpus + device-held-out training agent; also at
/rs/.../or_ready/devlodo/MORNING_REPORT.md), docs/devices/README.md + docs/devices/<device>.json (fitted parameter
sets with distributions, physics defaults, border/penumbra, coverage checks; marker or_ready/devices/DEVICES_DONE),
docs/devices/census/ (header + image census cards; marker or_ready/census/CENSUS_DONE), then the five-track
synthesis (workflow wf_093f2c0a-dd0 -> or_ready/{audit,wholespine,lodo,robust,crossdev}), SpineSAC
(or_ready/spinesac), thoracic radiographs (or_ready/thoracic), the C-arm dataset deep research
(wf_5c6cf903-03a), the DeepFluoro vendor DICOMs (job 40411582 -> data/deepfluoro_vendor).
Two training designs requested by Greg: (A) fixed geometry, all device noise spectra, leave-one-device-out;
(B) all geometries in one filter. Baselines: render-only detector; real-frames-only lodo detectors.

## 2026-09-22 06:20 EDT — resumed session: what landed, what never ran, what is queued
Evidence page for Greg (every finished track in one place): https://claude.ai/artifact/TUNtAawdAQh2vvRT9kWNf2
(builder: scratchpad build_evidence.py; local copies of or_ready/* under the scratchpad or_ready/collect/).

**Finished on disk:** audit (+addendum), lodo (table.md, recall curves, galleries), robust (408 rows, heatmaps), crossdev
(figures_table.json, COBRA level repair: TS vs SPINEPS agree 818/900, 5 L6, 13 T13), thoracic (tables.md: film keypoint
v5z T1-T12 97.7 %, chain T1..L5 73.2 %; box arms 0-7 % at IoU 0.5 = convention gap), wholespine ws_real + ws_render evals
(ws_mixed training 40411495 -> wseval 40411585 -> wsfig 40411586).

**Findings recorded this morning**
- lodo C-ArmLSpine-held-out vertebra recall 5.2 % is a BOX CONVENTION mismatch: C-ArmLSpine truth = SPINEPS body boxes
  (LAT w/h 1.25, ~128 px at 1024), COBRA/DeepFluoro truth = whole-vertebra outlines (w/h 1.73, ~70 px). The sheet
  or_ready/collect/lodo_carm/sheet_1.png shows red predictions spanning the whole vertebra over green body boxes; naming
  accuracy on named frames is 100 %. The held-out vertebra number for C-ArmLSpine is UNMEASURED until re-scored with a
  matched convention. Sacrum found held-out: 76.8 % (rx_lodo_carmlspine) / 83.9 % (best F1 cell).
- Position prior (or_ready/robust/position_prior.json): a fixed median box hits the truth sacrum at IoU>=0.5 on 85.7 % of
  C-ArmLSpine test frames (median IoU 0.69), 58.5 % COBRA, 13.5 % DeepFluoro. "Sacrum found" on C-ArmLSpine is partly layout.
- Whole spine: ws_real finds 94.5 % of vertebrae on real films but 0-8 % of the 25 labelled C2; render arms 85-88 % C2 on
  renders, ~0 on film. C2 on a real image is NOT demonstrated.
- DeepFluoro truth has two denominators in circulation: realxray_eval.load_truth now keeps only `kept` boxes (83 of 312 in
  the test split); the wholespine curves still used 312. State which one a number uses.
- COBRA fine-tuned level model on COBRA laterals with oracle boxes: 43.5 % vs zero-shot 79.9 % -> fine-tuning the level
  model on one device costs it the others, same as the detectors.

**The device track never ran.** tools/device_fit.py (1,473 lines) + device_physics.py were written by the overnight agent but
never copied to the grid; no docs/devices/, no census, no corpus, no designs A/B, no morning report. This morning: both
tools committed (c7013ca) and copied; slurm/device_fit.sh (CMD/DEVICE/EXTRA); jobs: pairs surgio_b51_dr 40411904,
elekta_xvi 40411905 (B000 NCC 0.195 -- one centre-B case registers badly, watch the fit), bv_pulsera 40411906 (116 pairs,
done), surgio_b51_raw 40411907; fit smoke cios_fusion 40411915 (--limit 200 --max-folds 3; the first smoke 40411903 died in
fold_summary because --limit 24 gave ONE specimen = zero training frames per fold). Markers: or_ready/devices/<dev>/{PAIRS,FIT}_DONE.
Then: full fits per device with --variants, read docs/devices/<device>.json, then the corpus + LODO designs.

**SpineSAC:** fetch done (4.15 GB, 5,490 files; 3 CT series, 915 2-D DICOMs, 902 PNGs). Inventory crashed twice on agent
bugs (duplicate `frames` kwarg; None[:14] in sheet captions) -- both fixed; inventory.json written 05:43; detect 40411909
ran on it; sheets 40411914. TotalSegmentator finds NO bone in the sawbone CTs (0 ml everywhere; the 150 HU fallback keeps
one 8.4 ml blob), so projected truth is unavailable -- judge detections on the contact sheets. or_recall_pool failed because
tools/carmlspine_pool_scores.py had never been copied to the grid (copied now; not re-run).

## 2026-09-22 07:05 EDT — re-score, device fits running, census running
- **Held-out C-ArmLSpine vertebra recall is 90.6 %, not 5.2 %** (tools/or_lodo_rescore_outline.py; or_ready/lodo/rescore_outline.md).
  Same predictions, three truth conventions on the 56 whole test frames (287 vertebrae), conf 0.25: body IoU 5.2 / outline IoU
  90.6 (92.7 best) / mutual-centre 90.9. Control: the same-device pooled arm goes 90.6 body -> 40.8 outline -> 91.6 centre.
  Render-only: 2.4 / 31.7 / 54.7. Crops (parent outline mapped into crop coordinates): lodo_carm k3 20.3 body / 18.7
  outline / 35.9 centre at 0.25 (64.0 at 0.05); k1 10.4 / 11.3 / 18.6 (35.1); pooled control k3 80.9 / 35.7 / 82.5.
  SCALE is a transfer lever of its own: the held-out detector keeps 91 % on whole frames and loses most of a magnified
  3-vertebra field. Ledger updated (same URL).
- **Device fits.** Smoke on cios_fusion (200 pairs, 3 folds, short optimiser) ran end to end after two agent bugs
  (fold_summary on one group; frame_vector on partial rows): held-out gain +0.6 median, term tests base9 90.7 / +penumbra
  90.5 / +scatter_thickness 90.5 / sigma_r_fixed 90.6 (short optimiser, not quotable), per-frame photons median 926
  (p10 82, p90 25,637), s per frame median 0.10, transfer test power r2 0.988; field_border carries 47.7 % of residual
  energy (bias +10.3 grey) -- the penumbra/border term is where the model is worst. COVERAGE "joint" = 0.03 is the product
  of 14 per-term 1-99 % boxes and is meaningless as defined; per-term 82-91 %. Fix: a copula-quantile (Mahalanobis in
  normal scores) coverage. Full fits submitted: cios_fusion 40411938, elekta_xvi 40411939 (376 pairs; B000 NCC 0.195 is
  one bad case), bv_pulsera 40411940 (116 pairs), surgio_b51_dr 40411941 (after pairs 40411904, 149 cases x AP+LAT),
  surgio_b51_raw 40411942 + display stage 40411943 (after pairs 40411907). Outputs docs/devices/<dev>.json + frames.csv in the
  GRID repo copy (rsync back!), figures or_ready/devices/<dev>/, marker FIT_DONE.
- **Census** (tools/device_census.py, slurm/device_census.sh): job 40411936 (C-ArmLSpine headers, SpineSAC headers, image
  stats of every display set), 40411937 = headers over the DeepFluoro vendor DICOMs after dfunpack 40411933 (36 GB, split
  zips joined by cat, python zipfile). Output docs/devices/census/ in the grid repo; marker or_ready/census/CENSUS_DONE.
- **Clean DeepFluoro same-device number**: rx_pooled_1024_init18 (40411934) = pooled real-frame detector from the
  anchor_none_v2_18-1109 init (renders and calibration never saw 18-1109).
- **SpineSAC**: six devices in the headers (Philips Allura Xper 104 raw frames, GE Fluorostar 55, Ziehm NetPort 55, Siemens
  Healthineers ? 38, Skanray 28, Siemens Fluorospot Compact S1 2; 118 processed PNGs). Box counts per device x detector are
  in the ledger §7b; no truth (TS finds no bone in the sawbone CT). only_carm boxes >=3 vertebrae on 83-95 % of Philips/GE/Ziehm
  frames; pooled 4-69 %. Truth would need a threshold segmentation of the phantom CT projected through the shipped poses.
- **C-arm dataset deep research relaunched** (workflow wf_1334ab58-486); save to docs/research_carm_datasets_verified_2026-09-22.json.

## 2026-09-22 07:40 EDT — the k-devices pipeline exists and is queued end to end
Code (all committed, on the grid): tools/device_style.py (draw a styled frame from a card; `demo` = real | draws sheet,
`stats` = real-vs-styled NPS / histogram / halo / gradient distances against a real-vs-real floor), tools/devcorpus_build.py
(`poses` per device, `render` once per geometry, `style` per noise device, `lists` for designs A/B with a held-out device),
tools/devcorpus_train.py (+ slurm/devcorpus_train.sh: lists -> YOLO11m from COCO at 1024 -> realxray_eval on every
device's test split, matched-convention re-score on C-ArmLSpine). Data under /rs/.../data/devcorpus/{poses,render,styled,lists};
runs under ~/spine-detector/runs/devcorpus/dc_<design>_held_<device>/scores.json; markers or_ready/devlodo/<design>_held_<dev>_DONE.

Chain: poses 40411950/52/54 (cios 366 poses, surgio 296; elekta pending) -> renders 40411951 (cios, down 2 = 0.39 mm, 768 px),
40411953 (surgio, 1024 px at 0.30 mm), 40411955 (elekta, 504 px at 0.8 mm), 142 subjects x 11 = ~1,500 each ->
styles 40411956 (cios x cios), 57 (cios x surgio), 58 (cios x elekta), 59 (surgio x surgio), 60 (elekta x elekta), each afterany
its render AND its noise device's full fit -> trainings A: 40411961 (held surgio), 63 (held cios), 65 (held elekta);
B: 40411962, 64, 66. Design A geometry = Cios Fusion poses for every noise device; B = each device on its own poses.
Baselines to compare against: render-only (anchor_none_v2, 73 % sacrum on C-ArmLSpine), lodo real-frame detectors
(83.9 % sacrum / 90.6 % outline vertebrae on C-ArmLSpine held out), pooled same-device.

Smoke card style demo (or_ready/devices/cios_fusion/fig_style_demo.png, style_stats.json): draws are in the right family but
the exposure spread from the 4-iteration smoke fit is far too wide (photons p1 20 .. p99 90k) and the styled statistics sit
~10x the real-vs-real floor (NPS L1 0.157 vs 0.015; hist 3.9 vs 0.14 grey; halo gain 0.62 vs 0.16). Re-run `demo`/`stats`
on the FULL card when 40411938 lands (slurm/device_style.sh CMD=demo|stats DEVICE=...) and look at the sheet before
trusting any styled corpus. Render preview (devcorpus/render/cios_fusion/*_preview.jpg) is the plain -log window: bone
is faint there by construction; judge the styled JPGs, not the previews.

Census: the first two census jobs stalled because every file was a DICOM candidate and pydicom force=True sat on the
100 GB C-ArmLSpine zip; fixed (preamble or listed extension only, files > 400 MB skipped), resubmitted as 40411967
(stage all, vendor DICOMs included: unpacked/<archive>/cadaver_X/{ct,fluoro}). surgio raw-sweep pairs (40411907) run
a CPU registration per frame and may hit the 12 h limit; the DR pairs (40411904, case75/149 at 07:35) feed the fit that matters.

Next after this lands: (1) full-card style sheets per device; (2) read dc_*/scores.json: held-out sacrum / vertebra
(outline) per design vs the baselines; if A or B beats 84 % / 91 % on C-ArmLSpine held out, scale subjects and draws;
(3) the level MODEL side: a mixed-device level model (C-ArmLSpine + COBRA crops with the repaired levels) trained
LODO, since the C-ArmLSpine fine-tune lost 36 points on COBRA laterals against zero-shot; (4) SpineSAC truth via a
threshold segmentation of the phantom CT through the shipped gt poses.

## 2026-09-22 08:15 EDT — C-arm dataset census (deep research, 101 agents, 19 claims survived 3-vote verification)
Saved: docs/research_carm_datasets_verified_2026-09-22.json (result.findings / caveats / refuted / openQuestions).
- **COBRA2026 is six centres, 867 patients, 692 public (~750 GB), NOT four centres / 145 / Elekta-only.** Centres A-D
  Elekta (504x504 at 0.8 mm, 120 kV, 189-734 projections, no grid); centres **F-G Varian** Halcyon / TrueBeam / VitalBeam
  (1024-3072 x 384-768 px at 0.28-0.39 x 0.39-1.12 mm, 125-140 kV, 406-895 projections, scatter grid; air-normalised
  + kernel scatter-corrected signal). Every case = a full gantry sweep with per-frame angle (consecutive overlapping
  frames at known displacement, 692 of them). Our 155 cases: 152 Elekta + 3 F. Varian = a SECOND linac kV device
  family for k -> slurm/cobra_fetch_varian.sh fetches 12 F + 12 G cases; pairs_cobra must then admit
  Manufacturer == Varian (handedness / W map to be re-settled on Varian frames as it was on Elekta).
- Geneva hip: repository licence CC BY-SA 4.0 (paper says BY-NC) -- fitting permitted; 19 frames, 12-bit 1000^2 at 0.29 mm.
- Ljubljana 3D-2D-GS-CA: 10 cerebrovascular patients, 3D-DSA + AP/LAT DSA and 2D-MAX frames 2480x1920 at 0.154 mm with
  4x4 detector pose + source position, CC BY-NC-ND, direct zips; the C-arm is unnamed (Artis-class panel by size). DSA
  frames are subtracted; 2D-MAX may serve a formation fit. Ljubljana 2D-3D-GS lumbar: Trixell PIXIUM 4600 flat panel
  on a turntable (not a C-arm), 18 frames at 20 deg steps -- tools/ljubljana_pairs.py already builds pairs for it.
- Veriserum: ~111k bi-planar image-intensifier knee-implant frames with poses, NO CT, non-commercial; CAMS-Knee is
  request-only (modified BV Pulsera). Struck: ETH tDPF (X-ray never on, 404), Utah Hive Cam-FAIS (no images), Calgary
  biplanar (data unavailable). SPARE: every claim refuted 0-3 -> unverified, not in a tier.
- None of the verified sets ships DICOM with vendor private tags; COBRA distils settings into metadata.yaml (Elekta .INI
  and Varian Scan.xml + Calibrations/ retained). k gains two vendor FAMILIES (Elekta, Varian), no new named mobile C-arm.
- Not covered by any surviving claim (still open): LigaSure / trauma sets, SpineWeb, TCIA kV projections, 4D-CBCT AAPM,
  dental / ENT, veterinary, endovascular.

## 2026-09-22 09:45 EDT — the RSNA AI endpoint, the first device cards, the manifest
- **Endpoint written**: docs/RSNAI_PLAN.md (Greg's directive 08:50: a concise RSNA AI paper, navigation from C-arm shots
  alone; boxes A–E with pre-stated pass criteria, evidence paths, dated status lines; tick only against disk).
  Memory `rsnai-paper-endpoint` points at it. Re-verify and update it every session.
- **Cards** (docs/devices/<dev>.json in the grid repo; local copies in the scratchpad `cards/`):
  cios_fusion: held-out R² 0.899 → 0.905 (+1.3 median; 18-1109 fold −1.3), kb 1.97, s 0.24, sigma_r 0.67 mm, alpha 0.20,
  sigma_u 2.2 mm, b −0.08, penumbra 3.6 mm (physics default 2.9), transfer power form 86 % of frames (gamma 1.06);
  **reproduces the shipped deepfluoro_calibrate folds to 1e-3 per term** (the fit machinery verified). bv_pulsera:
  0.917 → 0.952 (+3.8), s 0.61, b −0.36 (default −0.25), kb and sigma_s AT BOUND (widen for II), iris field radius 1.01,
  penumbra 1.4 mm, typicality_99 0.77. Per-frame photon estimates span three decades on both (p10–p90): the copula
  reproduces that and the first styled draws paired pure grain with pure smear.
- **C6 (styled inside real) FAILS so far**: cios full card NPS L1 0.111 vs floor 0.015, histogram 3.1 vs 0.14, gradient
  0.47 vs 0.11; pulsera NPS 0.20 vs 0.04. Fix in flight: draws clipped to the central quantile band (device_style.SPREAD
  0.2), window jitter 2.5; `device_style.py sweep` (jobs 40412027 cios, 40412028 pulsera) measures spread and single terms
  against the floor. The styled corpus jobs (40411956–60) use the clipped draws automatically.
- **Manifest** built (docs/RSNAI_DATA_MANIFEST.json, job 40412019): 12 roots, hashes of the split files; see plan E1.
- **Manifold** (tools/device_manifold.py, job 40412026): features of 1,864 real frames across six sets running; styled
  draws join when the styled corpora exist (rerun STAGE=all).
- Running: elekta_xvi fit 40411939, pixium_4600 40412003, surgio_b51_dr 40411941 (raw sweeps 40411907 slow: 12 frames/h),
  renders (cios 823+, surgio 363+, elekta 1,033+ of ~1,500), COBRA Varian fetch 40412010 (10 projections.mha so far),
  clean-init retrain 40411934 (15/80 epochs; scoring 40412006 chained after the time limit), census 40411967 (16k/59.6k
  headers read), wholespine figures done (wsfig 40411586).

## 2026-09-22 10:40 EDT — Elekta fit failure and the re-chained corpus jobs
- The Elekta fit (40411939) reached R² ~0.97 in its term tests and then died in the per-frame stage: COBRA case B000
  has 41 pairs with hit_frac 0–0.09 (its NCC was 0.195 in the pairs log — the RTK registration of that case never
  landed on the anatomy), and np.percentile on an empty mask raised. load_frames now drops frames with < 200 fittable
  pixels (and _perframe returns a NaN row as a second guard). Refit: 40412046 → recoverage / demo / stats chained.
  B000 itself should be re-registered or excluded from the pairs (note for pairs_cobra).
- The styling and training chain was rebuilt because two jobs started on a missing card: styles 40411956 (cios×cios),
  40411957 (cios×surgio), 40411959 (surgio×surgio), 40412050 (cios×elekta), 40412051 (elekta×elekta); trainings
  A: 40412052 (held surgio), 40412054 (held cios), 40412056 (held elekta); B: 40412053 / 40412055 / 40412057.
  Results: ~/spine-detector/runs/devcorpus/dc_<A|B>_held_<dev>/scores.json; markers or_ready/devlodo/*_DONE.
- Manifold real side done (job 40412026): devices are separable regions (Bhattacharyya overlaps ≤ 0.29, most < 0.07);
  fig or_ready/manifold/fig_manifold.png. Rerun `STAGE=all` once devcorpus/styled exists to place the styled draws.
- Term sweep (jobs 40412027/28) says the real-vs-styled residual is structural (plan C6); SPREAD 0.2 kept.
- Literature deep research for the introduction launched (workflow wf_9676bec3-cfd): counting procedure, the
  quaternary fiducial cost study, navigation access disparity, RSNA AI author instructions → save to
  docs/research_rsnai_intro_verified_2026-09-22.json when it lands.

## 2026-09-22 12:45 EDT — session ending; the whole remaining chain is queued
`bash slurm/queue_all_2026-09-22.sh` submitted 50 jobs; ids in `/rs/rs_grp_oschome/go2432/data/or_ready/QUEUE_2026-09-22.txt`:
surgio DR fit 40413034 (its first run died on an empty transfer curve in one frame; guarded) → reperframe photons-only
on every card: surgio 40413035, cios 40413036, elekta 40413037, pulsera 40413038, pixium 40413039, varian 40413041 (after
the varian fit 40413040, pairs done: 526) → stats/demo/sweep per card → styles on the refitted cards 40413060 (cios×cios),
61 (cios×surgio), 62 (cios×elekta), 63 (surgio×surgio), 64 (elekta×elekta) → C7 trainings A/B: held surgio 40413065/66,
held cios 40413067/68, held elekta 40413069/70 → C8 single-device arms 40413071–76 → manifold with styled draws
40413077, manifest rebuild 40413078, claims check 40413079. Also running: rx_pooled_1024_init18 (40411934, 8 h limit,
scoring 40412006 chained). Done today: census (docs/devices/census on the grid, CENSUS_END 08:55; local copy pulled at
11:20 — pull again), COBRA Varian fetch (24 cases), Ljubljana card, SpineSAC probe, whole-spine chain (wsfig).
Read first next time: docs/RSNAI_PLAN.md status log (12:45 entry), then QUEUE_2026-09-22.txt, then scores.json of each
dc_* run against the baselines (render-only 73 % sacrum on C-ArmLSpine; lodo real-frame 83.9 % / 90.6 % outline).
The evidence-page artifact URL reported "not found" by the watch at ~12:30; republish from the scratchpad builder if needed.
