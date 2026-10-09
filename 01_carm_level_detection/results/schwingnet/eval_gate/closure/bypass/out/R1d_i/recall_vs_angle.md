# Recall vs C-arm angle (render sweep; held out under tools/eval_gate.py)

Set: `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep_unseen` — 40 TotalSegmentator subjects (held out under tools/eval_gate.py) (s0086, s0139, s0178, s0236, s0243, s0244, s0355, s0370, s0550, s0586, s0657, s0667, s0669, s0733, s0830, s0859, s0869, s0913, s0979, s0983, s1111, s1230, s1294, s1347, s1364, s1395, s1404, s1487, s1540, s1547, s1574, s1741, s1807, s1815, s1868, s1935, s1949, s1973, s2021, s2106), Surgio-B51 geometry (anchor `case29/AP`), lat -90..90° step 10°, tilt [-15, 0, 15], roll 0, styled per card. Frames per card: {'elekta_xvi': 2280, 'surgio_b51_dr': 2280}.

Denominator per cell: projected boxes with >= 25% of the mask inside the panel, pooled over subjects; boxes at 2-25% are ignored (predictions on them are not false positives). Matching: greedy descending-confidence, IoU >= 0.5, per class (realxray_eval conventions). Intervals: subject-clustered bootstrap, 2000 resamples, 2.5-97.5 percentile.

EXPOSURE CONFOUND (looked at, 2026-09-23): the surgio_b51_dr card renders the thick lateral view as photon-starved mottle in which the spine is NOT visible, while REAL C-ArmLSpine laterals show readable bodies -- this is a property of the card's exposure conditioning that the styled TRAINING corpus carries too, so recall at large |lat| conflates geometry with synthetic underexposure. The elekta_xvi card additionally draws the XVI half-fan blades, so part of the panel is black at every angle and boxes under the blades count as misses. The table below quantifies both: mean exposed panel share (pixels above the collimated black level) and mean water-equivalent thickness, per lateral angle.

| card | lat | frames | exposed share | thickness (cm) |
|---|---|---|---|---|
| elekta_xvi | -90° | 120 | 0.68 | 30.4 |
| elekta_xvi | -80° | 120 | 0.69 | 30.1 |
| elekta_xvi | -70° | 120 | 0.69 | 29.4 |
| elekta_xvi | -60° | 120 | 0.70 | 28.1 |
| elekta_xvi | -50° | 120 | 0.71 | 26.6 |
| elekta_xvi | -40° | 120 | 0.68 | 25.3 |
| elekta_xvi | -30° | 120 | 0.69 | 24.0 |
| elekta_xvi | -20° | 120 | 0.71 | 23.0 |
| elekta_xvi | -10° | 120 | 0.69 | 22.2 |
| elekta_xvi | +0° | 120 | 0.68 | 21.9 |
| elekta_xvi | +10° | 120 | 0.68 | 22.3 |
| elekta_xvi | +20° | 120 | 0.68 | 23.0 |
| elekta_xvi | +30° | 120 | 0.67 | 23.9 |
| elekta_xvi | +40° | 120 | 0.70 | 25.2 |
| elekta_xvi | +50° | 120 | 0.69 | 26.6 |
| elekta_xvi | +60° | 120 | 0.69 | 28.1 |
| elekta_xvi | +70° | 120 | 0.68 | 29.4 |
| elekta_xvi | +80° | 120 | 0.69 | 30.4 |
| elekta_xvi | +90° | 120 | 0.70 | 30.6 |
| surgio_b51_dr | -90° | 120 | 1.00 | 30.4 |
| surgio_b51_dr | -80° | 120 | 1.00 | 30.1 |
| surgio_b51_dr | -70° | 120 | 1.00 | 29.4 |
| surgio_b51_dr | -60° | 120 | 1.00 | 28.1 |
| surgio_b51_dr | -50° | 120 | 1.00 | 26.6 |
| surgio_b51_dr | -40° | 120 | 1.00 | 25.3 |
| surgio_b51_dr | -30° | 120 | 1.00 | 24.0 |
| surgio_b51_dr | -20° | 120 | 1.00 | 23.0 |
| surgio_b51_dr | -10° | 120 | 1.00 | 22.2 |
| surgio_b51_dr | +0° | 120 | 1.00 | 21.9 |
| surgio_b51_dr | +10° | 120 | 1.00 | 22.3 |
| surgio_b51_dr | +20° | 120 | 1.00 | 23.0 |
| surgio_b51_dr | +30° | 120 | 1.00 | 23.9 |
| surgio_b51_dr | +40° | 120 | 1.00 | 25.2 |
| surgio_b51_dr | +50° | 120 | 1.00 | 26.6 |
| surgio_b51_dr | +60° | 120 | 1.00 | 28.1 |
| surgio_b51_dr | +70° | 120 | 1.00 | 29.4 |
| surgio_b51_dr | +80° | 120 | 1.00 | 30.4 |
| surgio_b51_dr | +90° | 120 | 1.00 | 30.6 |

## Falloff at conf 0.25 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | body | -15° | 0.834 | -30° | +40° | 0.416 (+90°) |
| Pooled (design P) | elekta_xvi | body | +0° | 0.871 | -30° | +30° | 0.562 (+80°) |
| Pooled (design P) | elekta_xvi | body | +15° | 0.803 | -30° | +40° | 0.204 (+70°) |
| Pooled (design P) | elekta_xvi | sacrum | -15° | 0.806 | -20° | +40° | 0.176 (-40°) |
| Pooled (design P) | elekta_xvi | sacrum | +0° | 0.809 | -30° | +30° | 0.217 (-70°) |
| Pooled (design P) | elekta_xvi | sacrum | +15° | 0.720 | -10° | +20° | 0.125 (+70°) |
| Pooled (design P) | surgio_b51_dr | body | -15° | 0.943 | -30° | +30° | 0.567 (-40°) |
| Pooled (design P) | surgio_b51_dr | body | +0° | 0.921 | -30° | +30° | 0.689 (-50°) |
| Pooled (design P) | surgio_b51_dr | body | +15° | 0.885 | -30° | +30° | 0.421 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | -15° | 0.839 | -30° | +40° | 0.059 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +0° | 0.905 | -30° | +30° | 0.318 (-60°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +15° | 0.880 | -30° | +20° | 0.217 (-60°) |
| LODO A, held Surgio | elekta_xvi | body | -15° | 0.737 | -30° | +40° | 0.169 (+80°) |
| LODO A, held Surgio | elekta_xvi | body | +0° | 0.800 | -30° | +30° | 0.215 (+70°) |
| LODO A, held Surgio | elekta_xvi | body | +15° | 0.779 | -20° | +20° | 0.079 (+90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | -15° | 0.581 | -20° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +0° | 0.619 | -30° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +15° | 0.320 | -50° | +50° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | -15° | 0.425 | -50° | +50° | 0.115 (+60°) |
| LODO A, held Surgio | surgio_b51_dr | body | +0° | 0.412 | -50° | +50° | 0.128 (+60°) |
| LODO A, held Surgio | surgio_b51_dr | body | +15° | 0.377 | -50° | +50° | 0.124 (+70°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | -15° | 0.129 | -50° | +50° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +0° | 0.191 | -50° | +20° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +15° | 0.160 | -50° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | -15° | 0.494 | -40° | +50° | 0.165 (+80°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +0° | 0.667 | -10° | +10° | 0.269 (+80°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +15° | 0.537 | -20° | +20° | 0.080 (+70°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | -15° | 0.065 | -40° | +70° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +0° | 0.191 | -30° | +10° | 0.000 (+60°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +15° | 0.080 | -50° | +10° | 0.000 (-80°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | -15° | 0.506 | -10° | +40° | 0.090 (-70°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +0° | 0.379 | -50° | +50° | 0.145 (+60°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +15° | 0.418 | -10° | +40° | 0.056 (+60°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | -15° | 0.065 | -20° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +0° | 0.048 | -60° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +15° | 0.080 | -10° | +10° | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | -15° | 0.012 | -10° | +10° | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +0° | 0.017 | -10° | +10° | 0.004 (-70°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +15° | 0.008 | -30° | +10° | 0.000 (-80°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-80°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-30°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Falloff at conf 0.74 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | body | -15° | 0.462 | -30° | +40° | 0.148 (+80°) |
| Pooled (design P) | elekta_xvi | body | +0° | 0.629 | -10° | +10° | 0.376 (+70°) |
| Pooled (design P) | elekta_xvi | body | +15° | 0.443 | -10° | +20° | 0.076 (+70°) |
| Pooled (design P) | elekta_xvi | sacrum | -15° | 0.484 | -10° | +10° | 0.000 (+60°) |
| Pooled (design P) | elekta_xvi | sacrum | +0° | 0.476 | -20° | +10° | 0.087 (-70°) |
| Pooled (design P) | elekta_xvi | sacrum | +15° | 0.320 | -10° | +20° | 0.083 (+70°) |
| Pooled (design P) | surgio_b51_dr | body | -15° | 0.680 | -20° | +10° | 0.269 (-40°) |
| Pooled (design P) | surgio_b51_dr | body | +0° | 0.679 | -20° | +20° | 0.398 (-50°) |
| Pooled (design P) | surgio_b51_dr | body | +15° | 0.566 | -20° | +20° | 0.154 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | -15° | 0.613 | -30° | +20° | 0.000 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +0° | 0.619 | -30° | +20° | 0.091 (+70°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +15° | 0.600 | -10° | +20° | 0.000 (+60°) |
| LODO A, held Surgio | elekta_xvi | body | -15° | 0.206 | -30° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | body | +0° | 0.429 | -10° | +10° | 0.025 (+90°) |
| LODO A, held Surgio | elekta_xvi | body | +15° | 0.275 | -10° | +10° | 0.000 (-70°) |
| LODO A, held Surgio | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +0° | 0.143 | -10° | +10° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | -15° | 0.012 | -50° | +60° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | +0° | 0.054 | -20° | +30° | 0.000 (+50°) |
| LODO A, held Surgio | surgio_b51_dr | body | +15° | 0.025 | -10° | +10° | 0.000 (-80°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +0° | 0.048 | -30° | +20° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | -15° | 0.121 | -30° | +10° | 0.004 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +0° | 0.271 | -10° | +10° | 0.070 (-70°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +15° | 0.139 | -10° | +10° | 0.004 (+70°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +0° | 0.048 | -10° | +20° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | -15° | 0.004 | -60° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +0° | 0.013 | -50° | +60° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +15° | 0.016 | -10° | +10° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +0° | 0.004 | -10° | +10° | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Per-angle body recall, tilt 0°, conf 0.25 (denominators in brackets)

### Pooled (design P) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.638 | [0.510, 0.762] |
| -80° | 243 | 0.741 | [0.632, 0.840] |
| -70° | 241 | 0.643 | [0.528, 0.760] |
| -60° | 241 | 0.585 | [0.446, 0.720] |
| -50° | 241 | 0.763 | [0.654, 0.866] |
| -40° | 241 | 0.759 | [0.643, 0.863] |
| -30° | 240 | 0.700 | [0.585, 0.812] |
| -20° | 240 | 0.842 | [0.743, 0.928] |
| -10° | 240 | 0.842 | [0.760, 0.909] |
| +0° | 240 | 0.871 | [0.788, 0.937] |
| +10° | 240 | 0.842 | [0.744, 0.923] |
| +20° | 240 | 0.858 | [0.774, 0.929] |
| +30° | 240 | 0.750 | [0.646, 0.848] |
| +40° | 241 | 0.743 | [0.622, 0.850] |
| +50° | 242 | 0.876 | [0.800, 0.947] |
| +60° | 242 | 0.661 | [0.534, 0.785] |
| +70° | 242 | 0.587 | [0.451, 0.718] |
| +80° | 242 | 0.562 | [0.430, 0.692] |
| +90° | 243 | 0.691 | [0.561, 0.803] |

### Pooled (design P) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.992 | [0.979, 1.000] |
| -80° | 243 | 0.967 | [0.908, 1.000] |
| -70° | 241 | 0.917 | [0.850, 0.968] |
| -60° | 241 | 0.751 | [0.628, 0.860] |
| -50° | 241 | 0.689 | [0.566, 0.810] |
| -40° | 241 | 0.730 | [0.606, 0.843] |
| -30° | 240 | 0.792 | [0.691, 0.883] |
| -20° | 240 | 0.883 | [0.798, 0.952] |
| -10° | 240 | 0.904 | [0.840, 0.958] |
| +0° | 240 | 0.921 | [0.870, 0.963] |
| +10° | 240 | 0.925 | [0.879, 0.966] |
| +20° | 240 | 0.883 | [0.818, 0.945] |
| +30° | 240 | 0.796 | [0.711, 0.869] |
| +40° | 241 | 0.722 | [0.621, 0.816] |
| +50° | 242 | 0.731 | [0.614, 0.841] |
| +60° | 242 | 0.785 | [0.687, 0.870] |
| +70° | 242 | 0.876 | [0.789, 0.946] |
| +80° | 242 | 0.955 | [0.913, 0.988] |
| +90° | 243 | 0.963 | [0.911, 0.996] |

### LODO A, held Surgio — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.412 | [0.307, 0.527] |
| -80° | 243 | 0.395 | [0.297, 0.498] |
| -70° | 241 | 0.402 | [0.310, 0.500] |
| -60° | 241 | 0.394 | [0.293, 0.500] |
| -50° | 241 | 0.564 | [0.465, 0.660] |
| -40° | 241 | 0.627 | [0.520, 0.737] |
| -30° | 240 | 0.608 | [0.494, 0.723] |
| -20° | 240 | 0.792 | [0.702, 0.873] |
| -10° | 240 | 0.767 | [0.661, 0.865] |
| +0° | 240 | 0.800 | [0.703, 0.891] |
| +10° | 240 | 0.796 | [0.690, 0.894] |
| +20° | 240 | 0.767 | [0.654, 0.870] |
| +30° | 240 | 0.629 | [0.496, 0.762] |
| +40° | 241 | 0.544 | [0.411, 0.682] |
| +50° | 242 | 0.496 | [0.380, 0.614] |
| +60° | 242 | 0.260 | [0.165, 0.368] |
| +70° | 242 | 0.215 | [0.130, 0.307] |
| +80° | 242 | 0.293 | [0.192, 0.404] |
| +90° | 243 | 0.296 | [0.203, 0.398] |

### LODO A, held Surgio — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.432 | [0.324, 0.544] |
| -80° | 243 | 0.461 | [0.354, 0.574] |
| -70° | 241 | 0.237 | [0.150, 0.336] |
| -60° | 241 | 0.274 | [0.180, 0.375] |
| -50° | 241 | 0.361 | [0.264, 0.466] |
| -40° | 241 | 0.502 | [0.393, 0.619] |
| -30° | 240 | 0.467 | [0.363, 0.573] |
| -20° | 240 | 0.446 | [0.340, 0.563] |
| -10° | 240 | 0.458 | [0.344, 0.571] |
| +0° | 240 | 0.412 | [0.301, 0.530] |
| +10° | 240 | 0.458 | [0.340, 0.581] |
| +20° | 240 | 0.421 | [0.306, 0.548] |
| +30° | 240 | 0.467 | [0.341, 0.590] |
| +40° | 241 | 0.373 | [0.276, 0.482] |
| +50° | 242 | 0.273 | [0.181, 0.377] |
| +60° | 242 | 0.128 | [0.068, 0.196] |
| +70° | 242 | 0.202 | [0.120, 0.293] |
| +80° | 242 | 0.273 | [0.191, 0.361] |
| +90° | 243 | 0.362 | [0.270, 0.456] |

### LODO B, held Surgio (s1) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.329 | [0.219, 0.448] |
| -80° | 243 | 0.403 | [0.290, 0.518] |
| -70° | 241 | 0.353 | [0.241, 0.473] |
| -60° | 241 | 0.432 | [0.309, 0.556] |
| -50° | 241 | 0.564 | [0.448, 0.689] |
| -40° | 241 | 0.598 | [0.466, 0.724] |
| -30° | 240 | 0.554 | [0.417, 0.698] |
| -20° | 240 | 0.662 | [0.540, 0.780] |
| -10° | 240 | 0.558 | [0.438, 0.671] |
| +0° | 240 | 0.667 | [0.545, 0.785] |
| +10° | 240 | 0.562 | [0.423, 0.697] |
| +20° | 240 | 0.658 | [0.532, 0.773] |
| +30° | 240 | 0.458 | [0.325, 0.600] |
| +40° | 241 | 0.527 | [0.396, 0.663] |
| +50° | 242 | 0.545 | [0.422, 0.660] |
| +60° | 242 | 0.335 | [0.228, 0.451] |
| +70° | 242 | 0.310 | [0.202, 0.425] |
| +80° | 242 | 0.269 | [0.160, 0.393] |
| +90° | 243 | 0.305 | [0.205, 0.412] |

### LODO B, held Surgio (s1) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.177 | [0.106, 0.261] |
| -80° | 243 | 0.198 | [0.122, 0.282] |
| -70° | 241 | 0.170 | [0.101, 0.246] |
| -60° | 241 | 0.203 | [0.123, 0.293] |
| -50° | 241 | 0.290 | [0.196, 0.394] |
| -40° | 241 | 0.394 | [0.292, 0.508] |
| -30° | 240 | 0.400 | [0.301, 0.498] |
| -20° | 240 | 0.483 | [0.381, 0.588] |
| -10° | 240 | 0.467 | [0.360, 0.571] |
| +0° | 240 | 0.379 | [0.270, 0.498] |
| +10° | 240 | 0.508 | [0.389, 0.633] |
| +20° | 240 | 0.475 | [0.365, 0.591] |
| +30° | 240 | 0.442 | [0.329, 0.551] |
| +40° | 241 | 0.456 | [0.348, 0.570] |
| +50° | 242 | 0.289 | [0.193, 0.398] |
| +60° | 242 | 0.145 | [0.081, 0.222] |
| +70° | 242 | 0.165 | [0.097, 0.243] |
| +80° | 242 | 0.207 | [0.125, 0.300] |
| +90° | 243 | 0.337 | [0.244, 0.435] |

### Real-frame LODO (render-initialised) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.029 | [0.000, 0.065] |
| -80° | 243 | 0.021 | [0.004, 0.044] |
| -70° | 241 | 0.004 | [0.000, 0.013] |
| -60° | 241 | 0.017 | [0.000, 0.046] |
| -50° | 241 | 0.008 | [0.000, 0.025] |
| -40° | 241 | 0.041 | [0.012, 0.079] |
| -30° | 240 | 0.021 | [0.000, 0.047] |
| -20° | 240 | 0.017 | [0.004, 0.034] |
| -10° | 240 | 0.004 | [0.000, 0.013] |
| +0° | 240 | 0.017 | [0.004, 0.033] |
| +10° | 240 | 0.013 | [0.000, 0.029] |
| +20° | 240 | 0.042 | [0.016, 0.075] |
| +30° | 240 | 0.029 | [0.004, 0.064] |
| +40° | 241 | 0.021 | [0.000, 0.050] |
| +50° | 242 | 0.066 | [0.029, 0.112] |
| +60° | 242 | 0.012 | [0.000, 0.029] |
| +70° | 242 | 0.021 | [0.000, 0.059] |
| +80° | 242 | 0.050 | [0.008, 0.103] |
| +90° | 243 | 0.058 | [0.020, 0.106] |

### Real-frame LODO (render-initialised) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.016 | [0.004, 0.033] |
| -80° | 243 | 0.000 | [0.000, 0.000] |
| -70° | 241 | 0.004 | [0.000, 0.013] |
| -60° | 241 | 0.000 | [0.000, 0.000] |
| -50° | 241 | 0.000 | [0.000, 0.000] |
| -40° | 241 | 0.004 | [0.000, 0.013] |
| -30° | 240 | 0.000 | [0.000, 0.000] |
| -20° | 240 | 0.004 | [0.000, 0.013] |
| -10° | 240 | 0.000 | [0.000, 0.000] |
| +0° | 240 | 0.000 | [0.000, 0.000] |
| +10° | 240 | 0.000 | [0.000, 0.000] |
| +20° | 240 | 0.004 | [0.000, 0.013] |
| +30° | 240 | 0.000 | [0.000, 0.000] |
| +40° | 241 | 0.000 | [0.000, 0.000] |
| +50° | 242 | 0.004 | [0.000, 0.013] |
| +60° | 242 | 0.008 | [0.000, 0.021] |
| +70° | 242 | 0.004 | [0.000, 0.013] |
| +80° | 242 | 0.012 | [0.000, 0.029] |
| +90° | 243 | 0.012 | [0.000, 0.028] |

