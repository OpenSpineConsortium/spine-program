# Recall vs C-arm angle (render sweep; held out under tools/eval_gate.py)

Set: `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep_unseen` — 40 TotalSegmentator subjects (held out under tools/eval_gate.py) (s0086, s0139, s0178, s0236, s0243, s0244, s0355, s0370, s0550, s0586, s0657, s0667, s0669, s0733, s0830, s0859, s0869, s0913, s0979, s0983, s1111, s1230, s1294, s1347, s1364, s1395, s1404, s1487, s1540, s1547, s1574, s1741, s1807, s1815, s1868, s1935, s1949, s1973, s2021, s2106), Surgio-B51 geometry (anchor `case29/AP`), lat -90..90° step 10°, tilt [-15, 0, 15], roll 0, styled per card. Frames per card: {'elekta_xvi': 2280, 'surgio_b51_dr': 2280}.

Denominator per cell: projected boxes with >= 25% of the mask inside the panel, pooled over subjects; boxes at 2-25% are ignored (predictions on them are not false positives). Matching: greedy descending-confidence, IoU >= 0.5, per class (realxray_eval conventions). Intervals: subject-clustered bootstrap, 1000 resamples, 2.5-97.5 percentile.

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
| cov_surgio_b51_dr_low_s0 | elekta_xvi | body | -15° | 0.073 | -30° | +10° | 0.008 (+40°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | body | +0° | 0.092 | -40° | +20° | 0.012 (+60°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | body | +15° | 0.115 | -20° | +10° | 0.008 (+70°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (+0°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | sacrum | +0° | 0.048 | -10° | +30° | 0.000 (-40°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | sacrum | +15° | 0.040 | -30° | +50° | 0.000 (-40°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | body | -15° | 0.838 | -20° | +20° | 0.216 (-40°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | body | +0° | 0.792 | -20° | +20° | 0.162 (+40°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | body | +15° | 0.766 | -30° | +20° | 0.190 (-40°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | sacrum | -15° | 0.806 | -10° | +10° | 0.067 (+40°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | sacrum | +0° | 0.905 | -10° | +10° | 0.095 (+50°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | sacrum | +15° | 0.680 | -30° | +40° | 0.083 (+60°) |

## Falloff at conf 0.74 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| cov_surgio_b51_dr_low_s0 | elekta_xvi | body | -15° | 0.000 | never | never | 0.000 (-50°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | body | +0° | 0.008 | -10° | +10° | 0.000 (-70°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | body | +15° | 0.000 | never | never | 0.000 (-80°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_surgio_b51_dr_low_s0 | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | body | -15° | 0.178 | -10° | +10° | 0.000 (-50°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | body | +0° | 0.229 | -10° | +10° | 0.000 (-50°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | body | +15° | 0.160 | -10° | +10° | 0.000 (-50°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | sacrum | +0° | 0.048 | -40° | +20° | 0.000 (-90°) |
| cov_surgio_b51_dr_low_s0 | surgio_b51_dr | sacrum | +15° | 0.080 | -20° | +20° | 0.000 (-90°) |

## Per-angle body recall, tilt 0°, conf 0.25 (denominators in brackets)

### cov_surgio_b51_dr_low_s0 — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.160 | [0.074, 0.258] |
| -80° | 243 | 0.210 | [0.125, 0.308] |
| -70° | 241 | 0.091 | [0.034, 0.162] |
| -60° | 241 | 0.112 | [0.047, 0.183] |
| -50° | 241 | 0.100 | [0.046, 0.154] |
| -40° | 241 | 0.012 | [0.000, 0.033] |
| -30° | 240 | 0.108 | [0.046, 0.189] |
| -20° | 240 | 0.121 | [0.064, 0.186] |
| -10° | 240 | 0.087 | [0.038, 0.149] |
| +0° | 240 | 0.092 | [0.045, 0.146] |
| +10° | 240 | 0.083 | [0.037, 0.139] |
| +20° | 240 | 0.033 | [0.000, 0.079] |
| +30° | 240 | 0.029 | [0.004, 0.063] |
| +40° | 241 | 0.012 | [0.000, 0.026] |
| +50° | 242 | 0.017 | [0.000, 0.037] |
| +60° | 242 | 0.012 | [0.000, 0.032] |
| +70° | 242 | 0.017 | [0.000, 0.042] |
| +80° | 242 | 0.025 | [0.000, 0.063] |
| +90° | 243 | 0.082 | [0.029, 0.148] |

### cov_surgio_b51_dr_low_s0 — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.844 | [0.776, 0.905] |
| -80° | 243 | 0.831 | [0.744, 0.905] |
| -70° | 241 | 0.643 | [0.538, 0.739] |
| -60° | 241 | 0.282 | [0.189, 0.363] |
| -50° | 241 | 0.257 | [0.170, 0.345] |
| -40° | 241 | 0.178 | [0.104, 0.260] |
| -30° | 240 | 0.525 | [0.421, 0.636] |
| -20° | 240 | 0.704 | [0.610, 0.796] |
| -10° | 240 | 0.729 | [0.640, 0.814] |
| +0° | 240 | 0.792 | [0.718, 0.856] |
| +10° | 240 | 0.787 | [0.697, 0.871] |
| +20° | 240 | 0.637 | [0.534, 0.734] |
| +30° | 240 | 0.287 | [0.203, 0.378] |
| +40° | 241 | 0.162 | [0.107, 0.219] |
| +50° | 242 | 0.169 | [0.103, 0.242] |
| +60° | 242 | 0.302 | [0.212, 0.385] |
| +70° | 242 | 0.496 | [0.385, 0.597] |
| +80° | 242 | 0.727 | [0.618, 0.821] |
| +90° | 243 | 0.794 | [0.709, 0.865] |

