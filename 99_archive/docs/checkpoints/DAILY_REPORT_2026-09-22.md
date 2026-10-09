# Daily report, 2026-09-21 → 22

## Done in the last day
- **Real intraoperative fluoroscopy, with truth.** C-ArmLSpine (149 cases, AP + lateral C-arm frames + CBCT) was
  found, downloaded, registered frame to CBCT, labelled by two independent labellers, and turned into the first
  real-OR level-identification test with anatomical truth. Five-fold cross-validation over all 148 usable cases:
  lateral whole frame 98.2 % exact level, three vertebrae in the field 92.9 %, one vertebra 72.8 %; AP 96.7 % whole.
  Errors at three vertebrae or more are almost all a single level. Figures and JSON in `docs/`.
- **Sacrum-anchored counting works on real frames of a device the detector was trained on:** sacrum found on 98 %
  of C-ArmLSpine test frames, 98.8 % of counted vertebrae named correctly.
- **The transfer problem was measured, not assumed.** Detectors fine-tuned on real frames of one device family
  collapse on other machines (1–43 % sacrum), while the render-only detector transfers partially (77–81 %).
  Two traps were caught before they reached a paper: COBRA laterals carry no bone (a same-device detector was
  scoring 98 % on blank frames from position alone), and TotalSegmentator's sacrum omits S1.
- **Data:** four verified dataset searches (about 400 agents); the finds that matter are C-ArmLSpine, COBRA
  (145 living pelves with poses), SpineSAC (five real C-arms, phantoms), and the pelvic-landmark set (PI on real
  laterals within 0.55° of CT). A fifth search on every C-arm dataset in existence is running.
- **Manuscript:** detector architecture figure added; the log-image finding got its outside check (COBRA).
- **Overnight program running:** per-device formation parameters fitted as distributions (border and penumbra
  included, physics defaults beside every fitted term, an unpaired-device path), a header + image census of every
  device, a multi-device synthetic corpus with leave-one-device-out training in two designs, the five-track
  adversarial readiness program (leakage audit, whole-spine detector to C2, device-held-out curves, corruption
  suite, cross-device naming), SpineSAC and a real thoracic radiograph test.

## Next, with likelihood and impact
| Goal | Likelihood | Impact if it works |
|---|---|---|
| Level naming on real OR frames holds up under the adversarial program (leakage clean, robust to exposure, hardware, collimation) | High: cross-validated, truth independent of the model, single device is the stated limit | The first real-OR level-identification result with CBCT truth: a paper on its own |
| Per-device parametric styling gets a detector to counting grade (≥97 % sacrum) on a device held out entirely | Moderate within the fitted span (the literature says measured randomization matches real training); low for a never-seen device family in one night with only 4 paired + 5 phantom devices | The "one network for any C-arm" claim, which is the product claim; each new device then costs a parameter fit, not a dataset |
| Every vertebra C2 to sacrum detected on real X-ray | High for cervical and lumbar (film corpus exists); uncertain for thoracic (renders only, real test pending) | Counting from either anchor anywhere in the spine |
| Pelvic incidence live in the OR | Moderate: hips are absent from C-ArmLSpine, present in COBRA/DeepFluoro; landmark set built, model untrained | A second product measurement from the same frames |

The binding constraint remains detection on machines outside the training set; every other component is now measured at or near counting grade on real frames.

## 06:20 EDT correction
The per-device parameter fitting, the device census and the multi-device corpus with leave-one-device-out training did
NOT run overnight: the fitting code was written but never reached the grid, and the other two never started. Fits and
pair-building were launched at 05:40. Everything else in "Overnight program running" finished and is summarised at
https://claude.ai/artifact/TUNtAawdAQh2vvRT9kWNf2 . Two results changed on inspection: the 5.2 % held-out vertebra
recall on C-ArmLSpine is a box-convention artefact (unmeasured, not 5 %), and C2 detection on real images is not shown.
