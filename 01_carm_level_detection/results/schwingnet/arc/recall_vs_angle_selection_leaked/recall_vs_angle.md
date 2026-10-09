# Recall vs C-arm angle (held-out render sweep)

Set: `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep` — 17 held-out TotalSegmentator subjects (s0585, s0970, s1045, s1062, s1159, s1384, s1535, s1579, s1700, s1836, s1842, s1872, s1880, s1883, s1902, s2033, s2053), Surgio-B51 geometry (anchor `case29/AP`), lat -90..90° step 10°, tilt [-15, 0, 15], roll 0, styled per card. Frames per card: {'elekta_xvi': 969, 'surgio_b51_dr': 969}.

Denominator per cell: projected boxes with >= 25% of the mask inside the panel, pooled over subjects; boxes at 2-25% are ignored (predictions on them are not false positives). Matching: greedy descending-confidence, IoU >= 0.5, per class (realxray_eval conventions). Intervals: subject-clustered bootstrap, 2000 resamples, 2.5-97.5 percentile.

EXPOSURE CONFOUND (looked at, 2026-09-23): the surgio_b51_dr card renders the thick lateral view as photon-starved mottle in which the spine is NOT visible, while REAL C-ArmLSpine laterals show readable bodies -- this is a property of the card's exposure conditioning that the styled TRAINING corpus carries too, so recall at large |lat| conflates geometry with synthetic underexposure. The elekta_xvi card additionally draws the XVI half-fan blades, so part of the panel is black at every angle and boxes under the blades count as misses. The table below quantifies both: mean exposed panel share (pixels above the collimated black level) and mean water-equivalent thickness, per lateral angle.

| card | lat | frames | exposed share | thickness (cm) |
|---|---|---|---|---|
| elekta_xvi | -90° | 51 | 0.71 | 31.6 |
| elekta_xvi | -80° | 51 | 0.71 | 30.8 |
| elekta_xvi | -70° | 51 | 0.67 | 28.1 |
| elekta_xvi | -60° | 51 | 0.71 | 26.5 |
| elekta_xvi | -50° | 51 | 0.74 | 25.1 |
| elekta_xvi | -40° | 51 | 0.67 | 23.4 |
| elekta_xvi | -30° | 51 | 0.70 | 21.7 |
| elekta_xvi | -20° | 51 | 0.69 | 20.5 |
| elekta_xvi | -10° | 51 | 0.68 | 19.3 |
| elekta_xvi | +0° | 51 | 0.69 | 19.0 |
| elekta_xvi | +10° | 51 | 0.65 | 19.6 |
| elekta_xvi | +20° | 51 | 0.72 | 20.8 |
| elekta_xvi | +30° | 51 | 0.71 | 22.0 |
| elekta_xvi | +40° | 51 | 0.68 | 23.8 |
| elekta_xvi | +50° | 51 | 0.68 | 25.5 |
| elekta_xvi | +60° | 51 | 0.70 | 27.2 |
| elekta_xvi | +70° | 51 | 0.68 | 28.4 |
| elekta_xvi | +80° | 51 | 0.63 | 30.2 |
| elekta_xvi | +90° | 51 | 0.70 | 31.9 |
| surgio_b51_dr | -90° | 51 | 1.00 | 31.6 |
| surgio_b51_dr | -80° | 51 | 1.00 | 30.8 |
| surgio_b51_dr | -70° | 51 | 1.00 | 28.1 |
| surgio_b51_dr | -60° | 51 | 1.00 | 26.5 |
| surgio_b51_dr | -50° | 51 | 1.00 | 25.1 |
| surgio_b51_dr | -40° | 51 | 1.00 | 23.4 |
| surgio_b51_dr | -30° | 51 | 1.00 | 21.7 |
| surgio_b51_dr | -20° | 51 | 1.00 | 20.5 |
| surgio_b51_dr | -10° | 51 | 1.00 | 19.3 |
| surgio_b51_dr | +0° | 51 | 1.00 | 19.0 |
| surgio_b51_dr | +10° | 51 | 1.00 | 19.6 |
| surgio_b51_dr | +20° | 51 | 1.00 | 20.8 |
| surgio_b51_dr | +30° | 51 | 1.00 | 22.0 |
| surgio_b51_dr | +40° | 51 | 1.00 | 23.8 |
| surgio_b51_dr | +50° | 51 | 1.00 | 25.5 |
| surgio_b51_dr | +60° | 51 | 1.00 | 27.2 |
| surgio_b51_dr | +70° | 51 | 1.00 | 28.4 |
| surgio_b51_dr | +80° | 51 | 1.00 | 30.2 |
| surgio_b51_dr | +90° | 51 | 1.00 | 31.9 |

## Falloff at conf 0.25 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | body | -15° | 0.868 | -30° | +40° | 0.305 (+80°) |
| Pooled (design P) | elekta_xvi | body | +0° | 0.894 | -30° | +30° | 0.352 (+90°) |
| Pooled (design P) | elekta_xvi | body | +15° | 0.776 | -40° | +50° | 0.174 (+80°) |
| Pooled (design P) | elekta_xvi | sacrum | -15° | 0.933 | -10° | +30° | 0.125 (-70°) |
| Pooled (design P) | elekta_xvi | sacrum | +0° | 0.889 | -10° | +40° | 0.100 (-80°) |
| Pooled (design P) | elekta_xvi | sacrum | +15° | 0.688 | -60° | +30° | 0.091 (-90°) |
| Pooled (design P) | surgio_b51_dr | body | -15° | 0.972 | -20° | +30° | 0.552 (-50°) |
| Pooled (design P) | surgio_b51_dr | body | +0° | 0.913 | -30° | +40° | 0.606 (-50°) |
| Pooled (design P) | surgio_b51_dr | body | +15° | 0.906 | -40° | +20° | 0.439 (-60°) |
| Pooled (design P) | surgio_b51_dr | sacrum | -15° | 0.800 | -40° | +30° | 0.200 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +0° | 1.000 | -40° | +10° | 0.455 (+60°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +15° | 0.812 | -40° | +30° | 0.133 (-70°) |
| LODO A, held Surgio | elekta_xvi | body | -15° | 0.792 | -10° | +30° | 0.076 (+80°) |
| LODO A, held Surgio | elekta_xvi | body | +0° | 0.779 | -30° | +40° | 0.076 (+80°) |
| LODO A, held Surgio | elekta_xvi | body | +15° | 0.720 | -40° | +30° | 0.018 (+80°) |
| LODO A, held Surgio | elekta_xvi | sacrum | -15° | 0.600 | -10° | +10° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +0° | 0.444 | -20° | +40° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +15° | 0.438 | -10° | +50° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | -15° | 0.170 | -10° | +50° | 0.086 (+70°) |
| LODO A, held Surgio | surgio_b51_dr | body | +0° | 0.260 | -10° | +50° | 0.105 (+70°) |
| LODO A, held Surgio | surgio_b51_dr | body | +15° | 0.196 | -60° | +40° | 0.047 (-70°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | -15° | 0.067 | -40° | +50° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +0° | 0.111 | -10° | +20° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +15° | 0.125 | -50° | +10° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | -15° | 0.613 | -10° | +30° | 0.029 (+90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +0° | 0.538 | -40° | +30° | 0.057 (+80°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +15° | 0.505 | -20° | +10° | 0.028 (+80°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | -15° | 0.067 | -60° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +0° | 0.111 | -70° | +10° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +15° | 0.125 | -20° | +30° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | -15° | 0.207 | -10° | +50° | 0.057 (+60°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +0° | 0.404 | -10° | +20° | 0.057 (+70°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +15° | 0.196 | -50° | +60° | 0.019 (-70°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | -15° | 0.067 | -20° | +40° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | body | -15° | 0.000 | never | never | 0.000 (-80°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | body | +0° | 0.029 | -20° | +50° | 0.000 (-80°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | body | +15° | 0.009 | -20° | +10° | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-70°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-80°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Falloff at conf 0.74 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | body | -15° | 0.547 | -30° | +30° | 0.124 (+90°) |
| Pooled (design P) | elekta_xvi | body | +0° | 0.567 | -30° | +30° | 0.125 (-70°) |
| Pooled (design P) | elekta_xvi | body | +15° | 0.439 | -20° | +10° | 0.046 (+80°) |
| Pooled (design P) | elekta_xvi | sacrum | -15° | 0.600 | -10° | +30° | 0.000 (-70°) |
| Pooled (design P) | elekta_xvi | sacrum | +0° | 0.444 | -40° | +10° | 0.000 (-90°) |
| Pooled (design P) | elekta_xvi | sacrum | +15° | 0.312 | -40° | +50° | 0.000 (-70°) |
| Pooled (design P) | surgio_b51_dr | body | -15° | 0.717 | -30° | +20° | 0.189 (+40°) |
| Pooled (design P) | surgio_b51_dr | body | +0° | 0.788 | -10° | +20° | 0.231 (-50°) |
| Pooled (design P) | surgio_b51_dr | body | +15° | 0.645 | -10° | +10° | 0.056 (-60°) |
| Pooled (design P) | surgio_b51_dr | sacrum | -15° | 0.667 | -10° | +10° | 0.000 (-60°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +0° | 0.667 | -50° | +10° | 0.000 (-60°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +15° | 0.438 | -10° | +40° | 0.000 (-70°) |
| LODO A, held Surgio | elekta_xvi | body | -15° | 0.283 | -10° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | body | +0° | 0.356 | -10° | +10° | 0.000 (-70°) |
| LODO A, held Surgio | elekta_xvi | body | +15° | 0.252 | -10° | +10° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | -15° | 0.067 | -20° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +0° | 0.111 | -40° | +40° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | +0° | 0.010 | -30° | +40° | 0.000 (-60°) |
| LODO A, held Surgio | surgio_b51_dr | body | +15° | 0.019 | -10° | +20° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | -15° | 0.067 | -10° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | -15° | 0.132 | -10° | +40° | 0.000 (-80°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +0° | 0.211 | -20° | +10° | 0.000 (-70°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +15° | 0.084 | -20° | +10° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +0° | 0.019 | -10° | +10° | 0.000 (-80°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-only LODO, no C-ArmLSpine | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Per-angle body recall, tilt 0°, conf 0.25 (denominators in brackets)

### Pooled (design P) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.390 | [0.204, 0.590] |
| -80° | 104 | 0.413 | [0.238, 0.596] |
| -70° | 104 | 0.442 | [0.271, 0.632] |
| -60° | 104 | 0.596 | [0.400, 0.786] |
| -50° | 104 | 0.683 | [0.485, 0.861] |
| -40° | 104 | 0.808 | [0.694, 0.918] |
| -30° | 104 | 0.769 | [0.602, 0.916] |
| -20° | 104 | 0.837 | [0.693, 0.942] |
| -10° | 104 | 0.952 | [0.897, 1.000] |
| +0° | 104 | 0.894 | [0.790, 0.971] |
| +10° | 104 | 0.923 | [0.849, 0.981] |
| +20° | 104 | 0.913 | [0.784, 1.000] |
| +30° | 104 | 0.769 | [0.632, 0.895] |
| +40° | 104 | 0.683 | [0.495, 0.852] |
| +50° | 104 | 0.827 | [0.680, 0.950] |
| +60° | 104 | 0.644 | [0.456, 0.820] |
| +70° | 105 | 0.362 | [0.170, 0.569] |
| +80° | 105 | 0.381 | [0.198, 0.586] |
| +90° | 105 | 0.352 | [0.168, 0.561] |

### Pooled (design P) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.790 | [0.632, 0.933] |
| -80° | 104 | 0.846 | [0.726, 0.943] |
| -70° | 104 | 0.788 | [0.620, 0.932] |
| -60° | 104 | 0.702 | [0.584, 0.830] |
| -50° | 104 | 0.606 | [0.461, 0.748] |
| -40° | 104 | 0.731 | [0.554, 0.889] |
| -30° | 104 | 0.788 | [0.657, 0.914] |
| -20° | 104 | 0.885 | [0.757, 0.981] |
| -10° | 104 | 0.933 | [0.862, 0.990] |
| +0° | 104 | 0.913 | [0.822, 0.972] |
| +10° | 104 | 0.923 | [0.861, 0.981] |
| +20° | 104 | 0.952 | [0.902, 0.991] |
| +30° | 104 | 0.856 | [0.745, 0.951] |
| +40° | 104 | 0.740 | [0.590, 0.868] |
| +50° | 104 | 0.779 | [0.651, 0.891] |
| +60° | 104 | 0.760 | [0.607, 0.885] |
| +70° | 105 | 0.848 | [0.709, 0.952] |
| +80° | 105 | 0.905 | [0.827, 0.971] |
| +90° | 105 | 0.848 | [0.721, 0.961] |

### LODO A, held Surgio — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.190 | [0.056, 0.354] |
| -80° | 104 | 0.308 | [0.167, 0.466] |
| -70° | 104 | 0.163 | [0.067, 0.267] |
| -60° | 104 | 0.375 | [0.234, 0.531] |
| -50° | 104 | 0.413 | [0.269, 0.575] |
| -40° | 104 | 0.538 | [0.355, 0.725] |
| -30° | 104 | 0.596 | [0.430, 0.775] |
| -20° | 104 | 0.817 | [0.663, 0.952] |
| -10° | 104 | 0.808 | [0.663, 0.933] |
| +0° | 104 | 0.779 | [0.602, 0.922] |
| +10° | 104 | 0.846 | [0.739, 0.931] |
| +20° | 104 | 0.875 | [0.709, 1.000] |
| +30° | 104 | 0.712 | [0.534, 0.864] |
| +40° | 104 | 0.404 | [0.221, 0.589] |
| +50° | 104 | 0.404 | [0.272, 0.551] |
| +60° | 104 | 0.154 | [0.055, 0.277] |
| +70° | 105 | 0.124 | [0.038, 0.231] |
| +80° | 105 | 0.076 | [0.000, 0.170] |
| +90° | 105 | 0.190 | [0.066, 0.330] |

### LODO A, held Surgio — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.210 | [0.100, 0.333] |
| -80° | 104 | 0.183 | [0.056, 0.337] |
| -70° | 104 | 0.154 | [0.045, 0.301] |
| -60° | 104 | 0.135 | [0.047, 0.243] |
| -50° | 104 | 0.163 | [0.075, 0.277] |
| -40° | 104 | 0.240 | [0.110, 0.400] |
| -30° | 104 | 0.317 | [0.163, 0.500] |
| -20° | 104 | 0.385 | [0.217, 0.566] |
| -10° | 104 | 0.212 | [0.073, 0.381] |
| +0° | 104 | 0.260 | [0.118, 0.420] |
| +10° | 104 | 0.269 | [0.130, 0.434] |
| +20° | 104 | 0.240 | [0.108, 0.394] |
| +30° | 104 | 0.346 | [0.196, 0.525] |
| +40° | 104 | 0.250 | [0.136, 0.380] |
| +50° | 104 | 0.154 | [0.059, 0.262] |
| +60° | 104 | 0.154 | [0.067, 0.267] |
| +70° | 105 | 0.105 | [0.035, 0.186] |
| +80° | 105 | 0.124 | [0.037, 0.231] |
| +90° | 105 | 0.181 | [0.075, 0.298] |

### LODO B, held Surgio (s1) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.190 | [0.056, 0.360] |
| -80° | 104 | 0.260 | [0.106, 0.434] |
| -70° | 104 | 0.135 | [0.029, 0.257] |
| -60° | 104 | 0.269 | [0.147, 0.400] |
| -50° | 104 | 0.500 | [0.337, 0.667] |
| -40° | 104 | 0.442 | [0.245, 0.657] |
| -30° | 104 | 0.500 | [0.286, 0.723] |
| -20° | 104 | 0.644 | [0.450, 0.811] |
| -10° | 104 | 0.625 | [0.442, 0.804] |
| +0° | 104 | 0.538 | [0.346, 0.723] |
| +10° | 104 | 0.558 | [0.367, 0.738] |
| +20° | 104 | 0.817 | [0.663, 0.951] |
| +30° | 104 | 0.404 | [0.215, 0.613] |
| +40° | 104 | 0.337 | [0.144, 0.539] |
| +50° | 104 | 0.423 | [0.234, 0.634] |
| +60° | 104 | 0.221 | [0.074, 0.406] |
| +70° | 105 | 0.076 | [0.018, 0.158] |
| +80° | 105 | 0.057 | [0.000, 0.144] |
| +90° | 105 | 0.210 | [0.081, 0.356] |

### LODO B, held Surgio (s1) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.133 | [0.038, 0.257] |
| -80° | 104 | 0.115 | [0.050, 0.190] |
| -70° | 104 | 0.087 | [0.027, 0.165] |
| -60° | 104 | 0.058 | [0.010, 0.118] |
| -50° | 104 | 0.144 | [0.047, 0.277] |
| -40° | 104 | 0.269 | [0.133, 0.419] |
| -30° | 104 | 0.356 | [0.188, 0.556] |
| -20° | 104 | 0.423 | [0.259, 0.610] |
| -10° | 104 | 0.346 | [0.206, 0.490] |
| +0° | 104 | 0.404 | [0.236, 0.562] |
| +10° | 104 | 0.423 | [0.269, 0.574] |
| +20° | 104 | 0.279 | [0.149, 0.423] |
| +30° | 104 | 0.442 | [0.284, 0.602] |
| +40° | 104 | 0.240 | [0.112, 0.392] |
| +50° | 104 | 0.144 | [0.056, 0.255] |
| +60° | 104 | 0.154 | [0.051, 0.283] |
| +70° | 105 | 0.057 | [0.000, 0.129] |
| +80° | 105 | 0.133 | [0.036, 0.250] |
| +90° | 105 | 0.162 | [0.037, 0.307] |

### Real-only LODO, no C-ArmLSpine — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.010 | [0.000, 0.029] |
| -80° | 104 | 0.000 | [0.000, 0.000] |
| -70° | 104 | 0.000 | [0.000, 0.000] |
| -60° | 104 | 0.010 | [0.000, 0.030] |
| -50° | 104 | 0.000 | [0.000, 0.000] |
| -40° | 104 | 0.019 | [0.000, 0.059] |
| -30° | 104 | 0.000 | [0.000, 0.000] |
| -20° | 104 | 0.010 | [0.000, 0.030] |
| -10° | 104 | 0.058 | [0.000, 0.130] |
| +0° | 104 | 0.029 | [0.000, 0.060] |
| +10° | 104 | 0.029 | [0.000, 0.071] |
| +20° | 104 | 0.087 | [0.010, 0.204] |
| +30° | 104 | 0.029 | [0.000, 0.061] |
| +40° | 104 | 0.067 | [0.000, 0.160] |
| +50° | 104 | 0.019 | [0.000, 0.050] |
| +60° | 104 | 0.010 | [0.000, 0.030] |
| +70° | 105 | 0.010 | [0.000, 0.029] |
| +80° | 105 | 0.000 | [0.000, 0.000] |
| +90° | 105 | 0.019 | [0.000, 0.049] |

### Real-only LODO, no C-ArmLSpine — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 105 | 0.038 | [0.009, 0.071] |
| -80° | 104 | 0.000 | [0.000, 0.000] |
| -70° | 104 | 0.000 | [0.000, 0.000] |
| -60° | 104 | 0.010 | [0.000, 0.030] |
| -50° | 104 | 0.010 | [0.000, 0.030] |
| -40° | 104 | 0.000 | [0.000, 0.000] |
| -30° | 104 | 0.000 | [0.000, 0.000] |
| -20° | 104 | 0.000 | [0.000, 0.000] |
| -10° | 104 | 0.000 | [0.000, 0.000] |
| +0° | 104 | 0.000 | [0.000, 0.000] |
| +10° | 104 | 0.000 | [0.000, 0.000] |
| +20° | 104 | 0.000 | [0.000, 0.000] |
| +30° | 104 | 0.000 | [0.000, 0.000] |
| +40° | 104 | 0.000 | [0.000, 0.000] |
| +50° | 104 | 0.000 | [0.000, 0.000] |
| +60° | 104 | 0.019 | [0.000, 0.048] |
| +70° | 105 | 0.000 | [0.000, 0.000] |
| +80° | 105 | 0.000 | [0.000, 0.000] |
| +90° | 105 | 0.019 | [0.000, 0.047] |

