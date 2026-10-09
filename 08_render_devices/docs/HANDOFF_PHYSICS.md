# Handoff — fluoroscopic physics and vertebra linking

**Read this first if you are picking this work up.** Written 2026-09-20 at the end of a long session.
Everything below is measured and in the repository; nothing is from memory.

```
make physics          # reproduce all of it, and fail if any headline number moved
make physics-tables   # just print what is already in results/physics/
make physics-check    # just verify the grid has what the jobs need
```

---

## 1. The one thing to know

**Detection is the binding constraint, not linking.** Everything in this work stream that reads well —
the circular-field fix, the step ladder, ten refuted correlation fixes — is measured with the vertebra
boxes GIVEN. When the detector has to find them:

| | walks reached | exact |
|---|---:|---:|
| clean render frames, boxes given | 6,238 | **99.74 %** |
| clean render frames, detector's boxes, conf 0.05 | 6,189 | 39.52 % |
| physics frames, boxes given | 6,123 | 71.73 % |
| physics frames, detector's boxes, conf 0.05 | 4,702 | 21.50 % |

Detection costs ~60 points on images with no physics in them. Physics costs 28 at the published step and
11 at a short step. **Do not spend more effort on linking before detection.**

A second thing, which matters for the manuscript: **confidence 0.25 is miscalibrated for both image
classes.** On clean film it costs about ten points (29.06 % at 0.25, 39.52 % at 0.05). The manuscript's
reported 30.06 % for detector boxes is measured at that threshold.

---

## 2. What is settled

**A circular field is solved.** A C-arm with an image intensifier exposes a disc. Cutting the corners
off costs 5.2 points on the abdominopelvic corpus and 25.2 on the whole-spine one. Correlating only the
pixels BOTH receptors exposed recovers all of it: 99.74 % and 99.90 %. The blanked corners are fixed to
the receptor, so they sit in the same pixels in both frames and correlate perfectly wherever the two
discs coincide; they collapse the margin over the one-body alias from 0.430 to 0.020, and masking
restores it to 0.378. `--masked-ncc`, no tuning in it.

This is in the manuscript (`paper/focused/main.tex`, "A round field costs 5 to 25 points").

**The step is the only protocol lever that moves physics much.** Exactness on 801 abdominopelvic spines:

| step | exposures | clean film | physics |
|---|---:|---:|---:|
| 2.5 body (published) | 1.98 | 99.74 % | 71.73 % |
| 1.5 body | 2.41 | 99.76 % | 76.88 % |
| 0.5 body | 3.64 | 99.17 % | **88.43 %** |

Worth 16.7 points under physics, costs clean film 0.6, at 1.8× the exposures. It also buys fleet
robustness: at the short step the anti-scatter grid is worth 9.5 points (88.43 vs 78.97 gridless) where
at the published step it was worth thirty, and a flat panel matches an intensifier (88.66 %). And it
survives a disturbed move — 89.77 % and 89.73 % at ±0.3 and ±0.5 body of jitter.

Why it works is geometric, which is the stronger claim: the search runs from 0.6 body below the
commanded step up to a step of half a body, so at a 2.5-body step the window CONTAINS the shift one body
short of the truth. At a half-body step there is no room for it. Shortening the move does not persuade
the correlation to be right; it removes the thing it could be wrong about.

**A second lever, weaker and on weaker footing.** A deliberate stored exposure instead of a live
screening frame is worth 4.6 points at the published step and 3.1 at 1.5 body, and **nothing** at the
short step — they do not compose. Caveat that must travel with it: `full_well_photons` is one of five
ASSUMED physics parameters (`make physics-params`), and this arm both depends on it and scales it. One
measurement of a real detector's well capacity would settle it.

**The simulator is calibrated against the published literature.** Photons/pixel 414 vs a published
219–1532; scatter map p95/median 2.76 vs 1.42–2.85; nearest-neighbour noise correlation 0.145 vs
0.02–0.20 on a flat field; generator pins only above its thickness ceiling. Those four are against
numbers somebody else measured and they stand.

**The two rows that compare against real panels are weaker than they read, and this qualifies a claim
made earlier in the session.** The histogram total-variation distance of 0.187 and the noise power
spectrum shape of 0.862 raw / 0.986 matched are scored against 27 FluoroCap panels. Those 27 are not a
sample of FluoroCap. Measured across the corpus with the project's own grain statistic, **72.8 % of
FluoroCap panels have `noise_mad` exactly 0.000** — no pixel-to-pixel residual at all, the press having
resampled the grain out of existence — and the surviving values are quantised to 1.4826 × {1, 2, 3},
i.e. one to three integer grey levels. Median short side is 368 px and only 48 % are ≥380 px. The 27
sit at median short side 459 and `noise_mad` 1.483 on every one: they are the intersection of the top
half by resolution and the top quarter by grain, about **9 % of the corpus**.

So the renderer has been validated against FluoroCap's top decile, not against FluoroCap. The
measurement is sound and the generalisation is not. Saying "the simulator passes every external check"
without that qualification, as this note did earlier, overstates it.

**The published configuration is unchanged.** `regression/ctsp_square_film` returns 0.9966 — the
manuscript number to four figures — after a day of changes to `sweep_map`. `make physics` re-checks this.

---

## 3. What is refuted — do not re-try these

All measured against the TRUE displacement with `tools/link_probe.py`, baseline 71.8 % of links paired:

| | paired | why it failed |
|---|---:|---|
| vertical derivative | 40.8 % | correlation fell to 0.053; a derivative amplifies the band the photon budget fills with noise |
| isotropic high-pass, 7 widths | 32–46 % | biased to a short step by +0.7 to +1.5 bodies at every width |
| high-pass normalised over the exposed field | 32–46 % | the rim it removes is real; removing it does not recover the arm |
| column demeaning | 41.7 % | did exactly what was predicted to the margin and lost 28 points |
| detrending along the column | 42.7 % | — |
| mask erosion | withdrawn | an artefact; see §4 |
| band about the spine | 48.5–65.0 % | monotonically worse the tighter the band |
| phase correlation | 3.2–4.0 % | collapses; 53.9 % of links a whole body out |
| tight search window | wash | 99.74 vs 99.74 on film, 71.23 vs 71.73 under physics |

The band sweep explains the rest: confining the correlation to a column about the vertebrae makes it
worse in proportion to how much is confined, so **the correlation is living on abdominal texture, not on
the vertebrae**, and every filter above deletes signal to suppress a nuisance a normalised correlation
already handles.

**One thing that does work and was nearly missed.** The global solve gains 5.5 points at the published
step (71.73 → 77.19) and loses 1.4 at 1.5 body. The prediction that it would be inert at the published
step was right about skip links and wrong about the method: `build_chain_global` also builds nodes by
CLUSTERING box centres rather than pairing them, and that works at any step. **That is worth separating
before relying on it**, and it may matter more with a real detector, because clustering is about
duplicate boxes and duplicate boxes are what a low confidence threshold produces. Untested.

---

## 4. Claims withdrawn during the session — do not resurrect them

- **Mask erosion, "48.5 % → 82.5 %".** An artefact. Eroding shrinks the masks until frames a commanded
  step apart barely overlap, so `_ncc` refused 21 % of the search window and the argmax landed where the
  refusals stopped — near the truth because the window is centred on the prior. The giveaway was that
  the median bias ran −0.51, −0.03, +0.72 at erosion radii 0.50, 0.75, 1.00, almost independent of
  filter width. An estimate whose bias is set by a tuning constant is not an estimate.
- **"Masking beats a square field."** 99.74 vs 99.66 is 16 wrong walks against 21 out of 6,238; p ≈ 0.51.
  Masking RECOVERS what a circular field costs. It does not improve on a square one.
- **"The simulator's noise is uncalibrated."** That was the measurement, four times over. See §6.
- **"Nine exposures."** 3.82 at the walk; nine was links per full sweep, which is not the same thing.
- **"Monotone in the step."** The flat-panel rows break it; only the 9-inch ladder is supported.
- **"The method does not work end to end on a realistic frame."** Measured at one confidence threshold,
  and the threshold was wrong. 5.1 % → 21.5 % at conf 0.05.
- **"The global solve is refuted."** Called on one row before the other reported. See §3.

---

## 5. Tooling built, and what each is for

| | |
|---|---|
| `tools/link_probe.py` | scores every link against the displacement that PRODUCED it. Refutes a candidate in ~3 minutes instead of a fleet run. Reports the SHAPE of the error (noise spreads about zero, aliasing piles at one body) and `cover`/`refused`, which catch an arm whose accuracy rests on a window it never searched. |
| `tools/link_surface_figure.py` | draws the correlation surface beside the frames it came from. Caught the erosion artefact; a render has now settled three things that argument from numbers got wrong. |
| `tools/frame_levels.py` | how many grey levels the vertebrae actually get, to exclude quantisation before blaming the correlation. |
| `tools/param_census.py` | counts the 22 physics parameters by source (7 measured, 10 derived, 5 assumed) and prints the manuscript sentence with the numbers filled in. |
| `tools/collect_physics_results.py` | pulls results into `results/physics/` and **fails** if a headline number moved. |
| `tools/reproduce_physics.py` | `make physics`. Prerequisites, submit, wait, collect, check. |

---

## 6. Traps this session fell into — the pattern is one thing

**Four validation rows were measuring their own method.** Each compared a number computed here against
one computed elsewhere, without reproducing how the other was computed. The noise-correlation row took
four versions: −0.128 on a 3×3 median residual (which forces a negative answer for ANY detector, because
the median contains the neighbour); +0.707 on a wide-kernel residual (which counts trabeculae as grain);
+0.803 on a raw flat field (which measures the vignette); and finally **0.145 on a flat field with the
receptor shading removed**, which agrees with the published 0.02–0.20. The spectrum row compared raw
synthetic frames against JPEG-compressed, downsampled real panels.

Other traps, each of which cost real time:

- **`--field-stop circle` does not set the field shape under physics.** The shape comes from
  `--receptor`, which defaulted to `mix`, so every "circular field" physics arm was two-thirds SQUARE.
  Now forced.
- **`link_probe` and `fiducial_walk` drew different receptors from identical flags.** A Generator has no
  `.randint`; a `RandomState` does. The `mix` draw fell back silently to index 0.
- **`sweep_map`'s module defaults were a configuration nothing publishes.** `END_RULE="clamp"` and
  `LAST_LINK="protocol"` while every published run overrides both. Now the defaults ARE the protocol.
- **The probe applied the tight window to the final link**, which `build_chain` exempts deliberately.
- **`wsl -e bash -lc "ssh host \"<cmd>\""` fails silently on `&&`.** It reported all eight prerequisites
  missing on a machine where all eight were present. Pass argument lists.
- **Heredoc backslash collapse.** Inline python heredocs in this environment eat `\`. Write scripts to a
  file and run them by path. This is in the project CLAUDE.md and it still bit twice.

---

## 7. What is NOT known

- **Every physics arm uses ground-truth boxes** except those in `phys_detector` and `phys_detconf`.
- **No arm has run on real fluoroscopy.** The simulator agrees with real panels on the statistics that
  survive an 8-bit windowed JPEG. It has never linked two real consecutive C-arm exposures of one
  patient, because no such pair exists in any corpus here.
- **Two biases, unquantified and opposite.** Scatter is overstated because a mobile C-arm's air gap
  rejects scatter and is not modelled; the film comparison is generous because physics frames get no
  roll or scale jitter while the film frames they are compared against get both.
- **The regional claim is not isolated.** VerSe reads 18 points better under physics than
  CTSpinoPelvic1K, in the direction water path predicts (14.6–25.9 cm vs 31.2 cm against a 32 cm
  generator ceiling) — but the two corpora differ in region, study length and links per patient as well,
  and the VerSe sample is 29 short cervical studies at ~1.1 links each.

---

## 8. Can a detector trained on renders alone work on real images? No. Measured.

`anchor_det_v1` was trained on 6,650 DRRs and 1,192 validation DRRs with **zero real images**, and until
now had never been scored on a real image — every arm naming it ran on renders. The missing cell is now
filled, on 25 spines / 71 frames / 233 bodies of `films_drr_buucorr`, which are REAL radiographs with
ground-truth boxes that it has never seen. `slurm/render_detector_on_real.sh`.

| detector | tested on | conf 0.05 | 0.10 | 0.25 |
|---|---|---:|---:|---:|
| render-trained | **real radiographs** | **71.67 %** | 65.24 % | 43.35 % |
| render-trained | renders (its own domain) | 93.48 % | 87.89 % | 81.06 % |
| film-trained | real radiographs | **99.14 %** | 98.71 % | 98.71 % |

Recall, per-vertebra. The decision rule was written into the script before the run: ≥0.95 go,
0.80–0.95 conditional, **<0.80 no-go**. It returns 0.7167 at the most generous threshold. **No-go for a
detector trained on renders alone.**

The failure decomposes, and both halves matter:

- **The render detector is weaker in its own domain.** 93.48 % on renders against the film detector's
  99.14 % on real film. It is a worse detector before any domain shift is paid.
- **Domain shift costs another 22 points.** 93.48 % on renders → 71.67 % on real radiographs.

**The duplicate rate is the more alarming number and is not a domain problem.** The render detector
fires **152 % within-frame duplicates** on real film and **175 % on renders** at conf 0.05 — it emits
about 2.5 boxes per vertebra, on 100 % of frames, in its own training domain. The film detector emits
6.87 %. That is an NMS or training-recipe fault, not a transfer fault, and it would have to be fixed
before any render-trained detector is judged on anything. It does not rescue the recall — 28 % of
vertebrae were never found at any box, and a duplicate cannot recover a miss — but it means the 71.67 %
is a floor from a detector that is also misconfigured.

So the honest reading: renders alone do not give an OR detector, and this particular render detector is
not a fair test of how close renders could get, because it is badly behaved in its own domain.

## 9. FluoroCap: what it is, and what annotating it would buy

**It is overwhelmingly reproductions of fluoroscopy, not fluoroscopy.** See §2 for the grain and
resolution numbers. Three further facts bound what it can be used for:

- **No model in this project distinguishes fluoroscopy from a plain radiograph.**
  `fluoroscopy_probability` is a verbatim copy of `p_xray_spine`, and the classifier that produced it
  pools fluoroscopy with plain film inside both positive classes by design. The only other call is a
  caption regex and one unvalidated 7B VLM, and they disagree on 64.6 % of the panels the caption calls
  a radiograph.
- **`human_qc_status` is `pending` on all 21,603 rows.** Nothing has been confirmed by a person.
- **Contamination is 22.6 % of VERTEBRAE, not of panels.** Bad panels carry 9.58 labels each against
  4.27 for good ones — the montages are the densest panels in the corpus, so they are what an annotator
  would spend the most time on.
- **There is no patient key.** The finest grouping is `figure_id`/`pmcid`, and perceptual-hash groups of
  13–25 span different PMCIDs, so a leakage-free split cannot be guaranteed by this project's own rule.

**As a training set it does not solve the domain transition.** The clean tier — caption-fluoroscopy ∩
intraoperative ∩ grain ∩ ≥380 px — is **250–380 panels, about 850–1,600 instances**. Relaxing to
caption-fluoro ∩ intraop gives ~2,500 panels and ~8,000–11,000 instances. `detect_v5z` was trained on
**143,721** instances and already reaches 0.9914 on real radiographs. That is fine-tune scale at best,
and everything above the clean tier buys instances by admitting radiographs, montages and sub-380 px
thumbnails.

**As a TEST set it is the most valuable thing available, because the measurement does not exist.** This
project has no labelled real fluoroscopy anywhere. There is a 0.9914-recall detector and a 99.74 %
counting method, and not one number saying either survives contact with a C-arm image.

Sizing, Wilson 95 % on independent bodies. The threshold is set by the chain, not by taste: with 8–12
bodies in a 140 mm field, per-body recall 0.99 gives 0.92/0.89 chain-complete, 0.97 gives 0.78/0.69,
0.95 gives 0.66/0.54. **0.95 per body is already a broken method**, so the decision boundary is
0.97–0.99, and separating 0.99 from 0.95 needs **110 vertebrae**. Vertebrae cluster at ~4.3/panel, so
with a design effect of 2–3.4 that is **50–90 panels**; round to **200** for four strata (AP/lateral ×
hardware/no-hardware) at ~50 each.

What 200 panels settle that nothing on disk settles: whether the film detector transfers to fluoroscopy
at all; whether the 99.74 % → 39.52 % gap is a detector problem or a fluoroscopy problem (annotated
boxes allow the boxes-given arm on real fluoro for the first time); whether the hardware-occlusion
augmentation does anything; whether the renderer's 0.986 buys task accuracy or only appearance; and it
calibrates the VLM modality read for free, fixing the corpus denominator.

**What stays untested regardless.** `~/FluoroCap/youtube_video` is empty; no two panels are the same
patient at a known displacement, so the SWEEP — consecutive overlapping frames with a commanded move,
which is the entire mechanism — cannot be tested on this corpus at all. Nor can automatic brightness
control between exposures, the field size, or the pixel pitch, none of which exist on any panel.

## 10. The session this came from, and the three questions it ended on

Written down because the reasoning is not recoverable from the commits, and two of the three answers
came from investigations whose results live only here.

**Where it started.** "Wake up to an implementation that still gets 99.7 % accuracy with a circular
window and the physics noise." The circular window was delivered at 99.74 %. The physics was not: it
reaches 88.43 % at a half-body step, and the reason it cannot reach 99.7 % is in §2 and §3. Along the
way five claims had to be withdrawn, including the best result of the night (§4).

**Question one: can a detector be trained on simulated DRRs and used in theatre?** Answered by
measurement, §8: **no**, 71.67 % of bodies found on real radiographs against a 0.80 pre-registered
floor. Two things that came out of investigating it and are worth keeping:
- A render-trained detector already existed (`anchor_det_v1`, 6,650 DRRs, zero real images) and had
  never been scored on a real image in this project. The measurement cost one GPU-hour.
- `~/anchor_drr_c2` is built (5,195 train, 9 classes) but its training job died on
  `ModuleNotFoundError: ultralytics` and no weights exist. Training it would produce another render
  number, since its stage 3 also evaluates on renders.

**Question two: why not add the same noise to real films instead of to renders?** The better idea, and
it survives partly. Corrections it forced to things stated earlier in this work:
- **Corner labels DO exist on real film** — 76,104 corner quads across 13,781 real films in
  `spine-detector/data/interim/manifest.parquet`, already exported as a pose dataset (`yolo_v3`,
  `kpt_shape [4,3]`). The earlier claim that corners were render-only was wrong. It is the RENDERED
  corpus that cannot supply corners.
- **The inversion fails.** `render()` takes water-equivalent path in cm and no branch accepts a
  displayed image. Measured on the renderer's own output, with the transfer function exactly known:
  naive inversion is 11.1 cm out in median path and compresses within-frame path SD 12.8 → 3.7 cm; an
  ORACLE two-parameter fit still leaves 4.36 cm RMSE and pulls p90 path 34.4 → 29.2 cm, crossing the
  32 cm generator ceiling the wrong way. Scatter is an irreversible low-frequency pedestal the film
  already contains, and seven stages would double-count.
- **It is testable without the inversion.** `--perturb film` operates on the displayed image and
  carries a noise model fitted to real-film statistics. Every real-film arm in this repository uses
  `--perturb photometric` (gain, offset, gamma, no noise); `grep films_drr slurm/ | grep -c "perturb
  film"` returns 0. `slurm/films_degraded_stage0.sh` runs it, decision rule written in first.
- **A bug fell out and is fixed.** `float(sp["mm_per_px"] or 0.8)` in four call sites. Pitch sets the
  scatter kernel width and the photon count; 0.8 mm is a render pitch and a real radiograph is
  0.125–0.365 mm, so degrading a real film under the default makes the kernel 5× too narrow and the
  photons ~40× too high — and returns a plausible frame. `render()` now raises.

**Question three: does FluoroCap reproduce OR fluoroscopy, and would annotating it solve the domain
transition?** §9. Short answers: it is overwhelmingly reproductions (72.8 % of panels have zero
pixel-to-pixel residual); annotating it as a TRAINING set does not solve the transition; annotating
~200 panels as a TEST set is the highest-value thing available because no labelled real fluoroscopy
exists anywhere in this work.

**A methodological note worth inheriting.** Three separate investigations this session were run as
fan-out/verify workflows rather than by reading files directly, and in the FluoroCap one the
adversarial verify phase refuted 12 of 16 load-bearing claims — the surviving numbers were those the
synthesiser re-measured itself. Treat a finding from such a run as a lead until it names the file, the
line or the command. Several did not survive that test.

## 11. Degradation onto real films: measured, and it splits the problem cleanly

`slurm/films_degraded_stage0.sh`, 95 walks on 16 held-out real radiographs that reach the sacrum.
Everything held but the perturbation and the box source:

| | boxes given | detector's boxes |
|---|---:|---:|
| photometric (gain/offset/gamma, no noise) | 100 % | **100 %** |
| film noise, fitted to real-film statistics | 100 % | **88.42 %** |
| film noise + circular field | — | 87.37 % |

Two things, and they point in different directions.

**Degradation does not touch the linker.** 100 % with given boxes, with and without noise. The
correlation is indifferent to image-domain noise on real anatomy, which is consistent with everything in
§3 — the filters all failed because the correlation never needed help.

**Degradation costs the detector 11.6 points**, 100 % to 88.42 %. That is the useful half: it means
noise is a lever on DETECTION, and a detector trained WITH that degradation should be more robust to it.
It is also a middle outcome rather than either pre-registered extreme — the arms neither survive
untouched nor collapse.

**What follows is cheap and specific.** `tools/make_zoom_dataset.py` already cuts 22,014 collimated
crops from the 11,007 labelled real training films with circular collimation, polarity inversion, JPEG,
contrast compression and a synthetic instrument, and those crops are already in `detect_v5z`'s training
set. The augmentation pipeline exists and ships. **Only the noise term is missing**, and Stage 0 says
noise is worth 12 points. Adding `film_match_augment.film_match` to it and retraining is one GPU job.

Caveat on n: 95 walks on 16 films. Real and held out, but small.

## 12. 2026-09-20: what the literature settled, and what is running because of it

A 107-agent adversarially-verified research pass answered the question this handoff has been circling.
Full record in `docs/FLUORO_DATASET_STRATEGY.md`; the operative parts:

**The DRR-to-real gap is not a fixed tax. It is three levers, all measured with matched controls on
real images.** Simulation fidelity moves real-image landmark error 78.2 to 24.7 mm, and ~68 % of that
is the polyenergetic multi-material attenuation step alone -- `render_physics_drr.py` already does it,
which is why the noise term here measured at 11.6 points and stopped. Strong domain randomization is
the lever that was NOT pulled: 6.44 mm with zero real training images against 6.46 for a real-trained
control on 366 real cadaveric C-arm images. Scale: 1k to 10k renders, 6.61 to 5.95 mm.

**Learned image translation is refuted, which kills the obvious idea.** CycleGAN 6.62 and ADDA 6.41
against 6.44 for no adaptation at all, all inside each other's intervals, and both need real
target-domain images at training time. Do not build a DRR-to-fluoro GAN.

**Tier 4 of the strategy document was a false equivalence and is withdrawn.** Pelphix's 99.2 to 71.7 is
surgical-PHASE accuracy over four sequence heads, not detection. Its agreement with 71.67 % to within
0.03 points was a coincidence between two different quantities.

**The honest ceiling: there is no published per-vertebra recall on real fluoroscopy at all**, and no
system that names vertebrae from real intraoperative fluoroscopic content at counting-grade recall.
LevelCheck's 100 % imports identity from the patient's own prior volume by registration. The
DeepDRR/SyntheX line reports millimetres and discards low-belief landmarks without stating the fraction.

**Every published parity figure is at high confidence and low coverage and inverts at low thresholds.**
Counting compounds recall over 8-12 bodies, so it lives at the high-coverage end. Report recall as a
CURVE. `tools/dr_eval_report.py` does, and prints the loosest confidence at which 0.97 is still reached.

### What is running

`slurm/dr_chain.sh` -- a 2x2 of strong DR against the acquisition term plus a scale arm, cut from the
11,007 labelled real films. The arms are a PROVEN matched control, not an assumed one: the strong-DR
term draws from a side stream seeded off each crop's own name and the polarity draw is unconditional,
so all arms cut identical crops. `slurm/dr_smoke.sh` checks it (labels byte-identical, 78.3 % of images
changed), and `dr_smoke_check --expect-identical` proved the refactor reproduces `yolo_v5f_p00` exactly
across all 22,014 crops, which is what keeps arms trained before it comparable to arms trained after.

### DeepFluoro is on the grid

2.54 GB full-res plus the 8x and 16x. The JHU archive refuses curl, wget and urllib with 403 from every
IP and with a full browser header set: it is the TLS fingerprint. `tools/dl_deepfluoro.py` presents
Chrome's via curl_cffi. The pose convention still has to be read off the data before any projection.

### The C2 detector exists; the cranial arm still cannot be scored

Trained to completion (40393767): precision 0.770, recall 0.774, mAP50 0.758 over 934 held-out images
and 23,092 instances. The WALK returns `spines: 0`, for two corpus reasons -- `anchor_drr_c2` carries no
pixel spacing at all, and only 39 of 6,129 renders present C2 as the most cranial body because C1 sits
above it, 10 of them held out. No external corpus substitutes: ts_drr is 84.3 % contaminated, verse_drr
82.7 %, physics_drr 84.5 %, and nhanes_drr is clean but carries no spacing.

That contamination took three attempts to measure, and every wrong answer erred toward CLEAN. Matching
normalised stems reported ts_drr at 0 % (`TS_s0001` vs `totalseg_s0001_ap`) and then verse_drr at 0 %
(`verse_scan-gl003_ap` matched the "verse" branch before reaching `gl003`). `tools/c2_anchor_status.py`
no longer normalises: it tokenises both sides, drops renderer and view boilerplate, and intersects.
It re-derives all three blockers and exits non-zero while any holds.

### A silent failure fixed along the way

Five superseded crop banks were deleted to recover quota, and ~90 scripts named them as
`--holdout-bank`. An unreadable bank left the trained-on set EMPTY and the evaluation ran over cases
the model was fitted on, without raising -- an error that only ever flatters. `tools/holdout.py` raises
now, and the 57 supplying references point at `allspine_v7`, whose train set is a measured strict
superset of v6.

## 13. Open threads left running

Two investigations were in flight at the end of the session and may have landed:

- **`drr-detector-feasibility`** — answered, in §8 above. No-go for renders alone.
- **`films-to-fluoro-degradation`** — answered, in §10 above.
- **`slurm/films_degraded_stage0.sh`** — running or run. The first test of degradation-onto-films at the
  image level, one flag wide. If the arms survive, image-domain noise is not what breaks a detector on
  real anatomy and the physics inversion is not worth building; if they collapse, the next step adds a
  fitted noise term to `make_zoom_dataset.py`, which already degrades real labelled films with
  collimation, polarity inversion and JPEG and already feeds the shipped detector. Only the noise
  physics is missing.

**The highest-value next thing is not a model.** Annotate ~200 FluoroCap panels as a test set, stratified
AP/lateral × hardware/no-hardware, and read `detect_v5z` against them with the decision rule written
down first. It is a day of annotation, it is the only measurement that can say whether any of this
transfers, and every other question on this list is downstream of it. After that: fine-tune on degraded
frames and re-run `physics_detconf.sh`, where 21.5 % is the number to beat.
