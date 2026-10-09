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
| cov_elekta_xvi_low_s1 | elekta_xvi | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Falloff at conf 0.74 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| cov_elekta_xvi_low_s1 | elekta_xvi | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| cov_elekta_xvi_low_s1 | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Per-angle body recall, tilt 0°, conf 0.25 (denominators in brackets)

### cov_elekta_xvi_low_s1 — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.000 | [0.000, 0.000] |
| -80° | 243 | 0.000 | [0.000, 0.000] |
| -70° | 241 | 0.000 | [0.000, 0.000] |
| -60° | 241 | 0.000 | [0.000, 0.000] |
| -50° | 241 | 0.000 | [0.000, 0.000] |
| -40° | 241 | 0.000 | [0.000, 0.000] |
| -30° | 240 | 0.000 | [0.000, 0.000] |
| -20° | 240 | 0.000 | [0.000, 0.000] |
| -10° | 240 | 0.000 | [0.000, 0.000] |
| +0° | 240 | 0.000 | [0.000, 0.000] |
| +10° | 240 | 0.000 | [0.000, 0.000] |
| +20° | 240 | 0.000 | [0.000, 0.000] |
| +30° | 240 | 0.000 | [0.000, 0.000] |
| +40° | 241 | 0.000 | [0.000, 0.000] |
| +50° | 242 | 0.000 | [0.000, 0.000] |
| +60° | 242 | 0.000 | [0.000, 0.000] |
| +70° | 242 | 0.000 | [0.000, 0.000] |
| +80° | 242 | 0.000 | [0.000, 0.000] |
| +90° | 243 | 0.000 | [0.000, 0.000] |

### cov_elekta_xvi_low_s1 — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.000 | [0.000, 0.000] |
| -80° | 243 | 0.000 | [0.000, 0.000] |
| -70° | 241 | 0.000 | [0.000, 0.000] |
| -60° | 241 | 0.000 | [0.000, 0.000] |
| -50° | 241 | 0.000 | [0.000, 0.000] |
| -40° | 241 | 0.000 | [0.000, 0.000] |
| -30° | 240 | 0.000 | [0.000, 0.000] |
| -20° | 240 | 0.000 | [0.000, 0.000] |
| -10° | 240 | 0.000 | [0.000, 0.000] |
| +0° | 240 | 0.000 | [0.000, 0.000] |
| +10° | 240 | 0.000 | [0.000, 0.000] |
| +20° | 240 | 0.000 | [0.000, 0.000] |
| +30° | 240 | 0.000 | [0.000, 0.000] |
| +40° | 241 | 0.000 | [0.000, 0.000] |
| +50° | 242 | 0.000 | [0.000, 0.000] |
| +60° | 242 | 0.000 | [0.000, 0.000] |
| +70° | 242 | 0.000 | [0.000, 0.000] |
| +80° | 242 | 0.000 | [0.000, 0.000] |
| +90° | 243 | 0.000 | [0.000, 0.000] |

