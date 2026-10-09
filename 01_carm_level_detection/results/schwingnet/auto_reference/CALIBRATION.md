# Automated reference: calibration (LEVELCHECK_MODEL.md section 14, R2)

Written 2026-09-24T19:46:05Z at git HEAD `749bc94280e2` (working tree dirty) by `tools/auto_reference_calibrate.py`. Every number here is computed from the inputs in `calibration.json`; no G3 test person's truth was read (test persons in the calibration set: 0, asserted).

## Calibration set

CTSpinoPelvic1K and VerSe persons on the G3 train and val sides with a human read: n = 945 ({'ctsp': 707, 'verse': 238}; sides {'train': 846, 'val': 99}). Truth classes: {'ordinary': 873, 'L6': 63, 'four_lumbar': 5, 'T13': 4}. A sacralised L5 that keeps its own id is scored as `ordinary` (its alphabet is L1..L5; section 3: variant, naming unaffected); the alternative convention, scoring it as `four_lumbar`, gives {'ordinary': 863, 'four_lumbar': 15, 'L6': 63, 'T13': 4} and is tabulated below.
Outside the calibration set: {'ctsp: G3 test person (truth never read here)': 93, 'ctsp: truth unassigned': 2, 'verse: truth no_read': 29, 'verse: G3 test person (truth never read here)': 68, 'verse: truth unassigned': 20}.

Reader calls on the calibration set: A: {'ordinary': 751, 'no_count': 118, 'four_lumbar': 35, 'L6': 32, 'T13': 9}; B: {'ordinary': 684, 'no_count': 200, 'L6': 47, 'four_lumbar': 13, 'T13': 1}; C: {'ordinary': 706, 'no_count': 180, 'L6': 43, 'four_lumbar': 15, 'T13': 1}

## Each reader alone (descriptive)

| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95 %] | sensitivity | class coverage | wrong truths |
|---|---:|---|---:|---:|---:|---|---|---|---|
| A | 0.875 [0.853, 0.895] (827/945) | ordinary | 873 | 751 | 732 | 0.975 [0.961, 0.984] | 0.838 [0.813, 0.861] | 0.877 [0.854, 0.898] | {'L6': 18, 'T13': 1} |
| A | 0.875 [0.853, 0.895] (827/945) | L6 | 63 | 32 | 24 | 0.750 [0.579, 0.867] | 0.381 [0.271, 0.504] | 0.825 [0.714, 0.900] | {'ordinary': 8} |
| A | 0.875 [0.853, 0.895] (827/945) | T13 | 4 | 9 | 3 | 0.333 [0.121, 0.646] | 0.750 [0.301, 0.954] | 1.000 [0.510, 1.000] | {'ordinary': 1, 'L6': 5} |
| A | 0.875 [0.853, 0.895] (827/945) | four_lumbar | 5 | 35 | 5 | 0.143 [0.063, 0.294] | 1.000 [0.566, 1.000] | 1.000 [0.566, 1.000] | {'ordinary': 25, 'L6': 5} |
| B | 0.788 [0.761, 0.813] (745/945) | ordinary | 873 | 684 | 658 | 0.962 [0.945, 0.974] | 0.754 [0.724, 0.781] | 0.789 [0.761, 0.815] | {'L6': 23, 'four_lumbar': 2, 'T13': 1} |
| B | 0.788 [0.761, 0.813] (745/945) | L6 | 63 | 47 | 28 | 0.596 [0.453, 0.724] | 0.444 [0.328, 0.567] | 0.810 [0.696, 0.888] | {'ordinary': 18, 'T13': 1} |
| B | 0.788 [0.761, 0.813] (745/945) | T13 | 4 | 1 | 0 | 0.000 [0.000, 0.793] | 0.000 [0.000, 0.490] | 0.500 [0.150, 0.850] | {'ordinary': 1} |
| B | 0.788 [0.761, 0.813] (745/945) | four_lumbar | 5 | 13 | 1 | 0.077 [0.014, 0.333] | 0.200 [0.036, 0.624] | 0.600 [0.231, 0.882] | {'ordinary': 12} |
| C | 0.810 [0.783, 0.833] (765/945) | ordinary | 873 | 706 | 686 | 0.972 [0.957, 0.982] | 0.786 [0.757, 0.812] | 0.816 [0.788, 0.840] | {'L6': 17, 'T13': 3} |
| C | 0.810 [0.783, 0.833] (765/945) | L6 | 63 | 43 | 29 | 0.674 [0.525, 0.795] | 0.460 [0.343, 0.582] | 0.746 [0.627, 0.837] | {'ordinary': 14} |
| C | 0.810 [0.783, 0.833] (765/945) | T13 | 4 | 1 | 1 | 1.000 [0.207, 1.000] | 0.250 [0.046, 0.699] | 1.000 [0.510, 1.000] | {} |
| C | 0.810 [0.783, 0.833] (765/945) | four_lumbar | 5 | 15 | 2 | 0.133 [0.037, 0.379] | 0.400 [0.118, 0.769] | 0.400 [0.118, 0.769] | {'ordinary': 12, 'L6': 1} |

## The three pre-specified rules (own-id sacralised L5 = ordinary)

| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95 %] | sensitivity | class coverage | wrong truths |
|---|---:|---|---:|---:|---:|---|---|---|---|
| unanimity | 0.605 [0.574, 0.636] (572/945) | ordinary | 873 | 554 | 549 | 0.991 [0.979, 0.996] | 0.629 [0.596, 0.660] | 0.632 [0.600, 0.664] | {'L6': 4, 'T13': 1} |
| unanimity | 0.605 [0.574, 0.636] (572/945) | L6 | 63 | 14 | 14 | 1.000 [0.785, 1.000] | 0.222 [0.137, 0.339] | 0.286 [0.189, 0.407] | {} |
| unanimity | 0.605 [0.574, 0.636] (572/945) | T13 | 4 | 0 | 0 | n/a | 0.000 [0.000, 0.490] | 0.250 [0.046, 0.699] | {} |
| unanimity | 0.605 [0.574, 0.636] (572/945) | four_lumbar | 5 | 4 | 1 | 0.250 [0.046, 0.699] | 0.200 [0.036, 0.624] | 0.200 [0.036, 0.624] | {'ordinary': 3} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | ordinary | 873 | 746 | 729 | 0.977 [0.964, 0.986] | 0.835 [0.809, 0.858] | 0.856 [0.831, 0.877] | {'L6': 16, 'T13': 1} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | L6 | 63 | 32 | 26 | 0.812 [0.647, 0.911] | 0.413 [0.300, 0.536] | 0.667 [0.544, 0.771] | {'ordinary': 6} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | T13 | 4 | 1 | 1 | 1.000 [0.207, 1.000] | 0.250 [0.046, 0.699] | 0.500 [0.150, 0.850] | {} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | four_lumbar | 5 | 14 | 2 | 0.143 [0.040, 0.399] | 0.400 [0.118, 0.769] | 0.400 [0.118, 0.769] | {'ordinary': 12} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | ordinary | 873 | 792 | 769 | 0.971 [0.957, 0.981] | 0.881 [0.858, 0.901] | 0.901 [0.880, 0.920] | {'L6': 22, 'T13': 1} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | L6 | 63 | 29 | 23 | 0.793 [0.616, 0.902] | 0.365 [0.257, 0.489] | 0.730 [0.610, 0.824] | {'ordinary': 6} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | T13 | 4 | 2 | 1 | 0.500 [0.095, 0.905] | 0.250 [0.046, 0.699] | 0.500 [0.150, 0.850] | {'L6': 1} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | four_lumbar | 5 | 14 | 2 | 0.143 [0.040, 0.399] | 0.400 [0.118, 0.769] | 0.400 [0.118, 0.769] | {'ordinary': 12} |

## The same rules, own-id sacralised L5 scored as four_lumbar (sensitivity table)

| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95 %] | sensitivity | class coverage | wrong truths |
|---|---:|---|---:|---:|---:|---|---|---|---|
| unanimity | 0.605 [0.574, 0.636] (572/945) | ordinary | 863 | 554 | 547 | 0.987 [0.974, 0.994] | 0.634 [0.601, 0.665] | 0.636 [0.604, 0.668] | {'four_lumbar': 2, 'L6': 4, 'T13': 1} |
| unanimity | 0.605 [0.574, 0.636] (572/945) | L6 | 63 | 14 | 14 | 1.000 [0.785, 1.000] | 0.222 [0.137, 0.339] | 0.286 [0.189, 0.407] | {} |
| unanimity | 0.605 [0.574, 0.636] (572/945) | T13 | 4 | 0 | 0 | n/a | 0.000 [0.000, 0.490] | 0.250 [0.046, 0.699] | {} |
| unanimity | 0.605 [0.574, 0.636] (572/945) | four_lumbar | 15 | 4 | 2 | 0.500 [0.150, 0.850] | 0.133 [0.037, 0.379] | 0.267 [0.109, 0.520] | {'ordinary': 2} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | ordinary | 863 | 746 | 726 | 0.973 [0.959, 0.983] | 0.841 [0.815, 0.864] | 0.856 [0.831, 0.878] | {'four_lumbar': 3, 'L6': 16, 'T13': 1} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | L6 | 63 | 32 | 26 | 0.812 [0.647, 0.911] | 0.413 [0.300, 0.536] | 0.667 [0.544, 0.771] | {'ordinary': 6} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | T13 | 4 | 1 | 1 | 1.000 [0.207, 1.000] | 0.250 [0.046, 0.699] | 0.500 [0.150, 0.850] | {} |
| two_of_three | 0.839 [0.814, 0.861] (793/945) | four_lumbar | 15 | 14 | 7 | 0.500 [0.268, 0.732] | 0.467 [0.248, 0.699] | 0.667 [0.417, 0.848] | {'ordinary': 7} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | ordinary | 863 | 792 | 765 | 0.966 [0.951, 0.976] | 0.886 [0.864, 0.906] | 0.902 [0.880, 0.920] | {'four_lumbar': 4, 'L6': 22, 'T13': 1} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | L6 | 63 | 29 | 23 | 0.793 [0.616, 0.902] | 0.365 [0.257, 0.489] | 0.730 [0.610, 0.824] | {'ordinary': 6} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | T13 | 4 | 2 | 1 | 0.500 [0.095, 0.905] | 0.250 [0.046, 0.699] | 0.500 [0.150, 0.850] | {'L6': 1} |
| dawid_skene | 0.886 [0.864, 0.904] (837/945) | four_lumbar | 15 | 14 | 7 | 0.500 [0.268, 0.732] | 0.467 [0.248, 0.699] | 0.733 [0.480, 0.891] | {'ordinary': 7} |

## Rule unanimity per corpus

| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95 %] | sensitivity | class coverage | wrong truths |
|---|---:|---|---:|---:|---:|---|---|---|---|
| ctsp | 0.686 [0.651, 0.719] (485/707) | ordinary | 691 | 480 | 480 | 1.000 [0.992, 1.000] | 0.695 [0.659, 0.728] | 0.698 [0.662, 0.731] | {} |
| ctsp | 0.686 [0.651, 0.719] (485/707) | L6 | 11 | 2 | 2 | 1.000 [0.342, 1.000] | 0.182 [0.051, 0.477] | 0.182 [0.051, 0.477] | {} |
| ctsp | 0.686 [0.651, 0.719] (485/707) | four_lumbar | 5 | 3 | 1 | 0.333 [0.061, 0.792] | 0.200 [0.036, 0.624] | 0.200 [0.036, 0.624] | {'ordinary': 2} |
| verse | 0.366 [0.307, 0.428] (87/238) | ordinary | 182 | 74 | 69 | 0.932 [0.851, 0.971] | 0.379 [0.312, 0.451] | 0.385 [0.317, 0.457] | {'L6': 4, 'T13': 1} |
| verse | 0.366 [0.307, 0.428] (87/238) | L6 | 52 | 12 | 12 | 1.000 [0.758, 1.000] | 0.231 [0.137, 0.361] | 0.308 [0.199, 0.443] | {} |
| verse | 0.366 [0.307, 0.428] (87/238) | T13 | 4 | 0 | 0 | n/a | 0.000 [0.000, 0.490] | 0.250 [0.046, 0.699] | {} |
| verse | 0.366 [0.307, 0.428] (87/238) | four_lumbar | 0 | 1 | 0 | 0.000 [0.000, 0.793] | n/a | n/a | {'ordinary': 1} |

## Rule two_of_three per corpus

| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95 %] | sensitivity | class coverage | wrong truths |
|---|---:|---|---:|---:|---:|---|---|---|---|
| ctsp | 0.905 [0.881, 0.925] (640/707) | ordinary | 691 | 619 | 619 | 1.000 [0.994, 1.000] | 0.896 [0.871, 0.916] | 0.913 [0.890, 0.932] | {} |
| ctsp | 0.905 [0.881, 0.925] (640/707) | L6 | 11 | 13 | 7 | 0.538 [0.291, 0.768] | 0.636 [0.354, 0.848] | 0.636 [0.354, 0.848] | {'ordinary': 6} |
| ctsp | 0.905 [0.881, 0.925] (640/707) | four_lumbar | 5 | 8 | 2 | 0.250 [0.071, 0.591] | 0.400 [0.118, 0.769] | 0.400 [0.118, 0.769] | {'ordinary': 6} |
| verse | 0.643 [0.580, 0.701] (153/238) | ordinary | 182 | 127 | 110 | 0.866 [0.796, 0.915] | 0.604 [0.532, 0.673] | 0.637 [0.565, 0.704] | {'L6': 16, 'T13': 1} |
| verse | 0.643 [0.580, 0.701] (153/238) | L6 | 52 | 19 | 19 | 1.000 [0.832, 1.000] | 0.365 [0.248, 0.501] | 0.673 [0.538, 0.785] | {} |
| verse | 0.643 [0.580, 0.701] (153/238) | T13 | 4 | 1 | 1 | 1.000 [0.207, 1.000] | 0.250 [0.046, 0.699] | 0.500 [0.150, 0.850] | {} |
| verse | 0.643 [0.580, 0.701] (153/238) | four_lumbar | 0 | 6 | 0 | 0.000 [0.000, 0.390] | n/a | n/a | {'ordinary': 6} |

## Rule dawid_skene per corpus

| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95 %] | sensitivity | class coverage | wrong truths |
|---|---:|---|---:|---:|---:|---|---|---|---|
| ctsp | 0.955 [0.937, 0.968] (675/707) | ordinary | 691 | 654 | 651 | 0.995 [0.987, 0.998] | 0.942 [0.922, 0.957] | 0.959 [0.942, 0.972] | {'L6': 3} |
| ctsp | 0.955 [0.937, 0.968] (675/707) | L6 | 11 | 13 | 7 | 0.538 [0.291, 0.768] | 0.636 [0.354, 0.848] | 0.909 [0.623, 0.984] | {'ordinary': 6} |
| ctsp | 0.955 [0.937, 0.968] (675/707) | four_lumbar | 5 | 8 | 2 | 0.250 [0.071, 0.591] | 0.400 [0.118, 0.769] | 0.400 [0.118, 0.769] | {'ordinary': 6} |
| verse | 0.681 [0.619, 0.737] (162/238) | ordinary | 182 | 138 | 118 | 0.855 [0.787, 0.904] | 0.648 [0.577, 0.714] | 0.681 [0.610, 0.745] | {'L6': 19, 'T13': 1} |
| verse | 0.681 [0.619, 0.737] (162/238) | L6 | 52 | 16 | 16 | 1.000 [0.806, 1.000] | 0.308 [0.199, 0.443] | 0.692 [0.557, 0.801] | {} |
| verse | 0.681 [0.619, 0.737] (162/238) | T13 | 4 | 2 | 1 | 0.500 [0.095, 0.905] | 0.250 [0.046, 0.699] | 0.500 [0.150, 0.850] | {'L6': 1} |
| verse | 0.681 [0.619, 0.737] (162/238) | four_lumbar | 0 | 6 | 0 | 0.000 [0.000, 0.390] | n/a | n/a | {'ordinary': 6} |

## Selection

A rule qualifies for a subtype when the PPV Wilson lower bound is at least 0.9. Qualifies for every subtype it assigns: {'unanimity': False, 'two_of_three': False, 'dawid_skene': False}.
**Chosen:** mode `per_subtype (no rule reached a PPV lower bound of 0.90 for every subtype it assigns)`; rule per subtype {'ordinary': 'dawid_skene'}; assignable subtypes: ['ordinary']. A person whose call is a subtype outside this list is excluded with the reason written in `auto_truth.csv`.

Dawid-Skene (fitted on the calibration persons only, abstentions as missing, posterior threshold 0.95): prior ordinary 0.923, L6 0.046, T13 0.008, four_lumbar 0.020, both 0.002.

- reader A, P(call | truth): ordinary: ordinary 0.95, four_lumbar 0.03; L6: ordinary 0.49, L6 0.47, T13 0.04; T13: T13 0.98; four_lumbar: ordinary 0.23, four_lumbar 0.76; both: ordinary 0.12, L6 0.08, T13 0.20, four_lumbar 0.59
- reader B, P(call | truth): ordinary: ordinary 0.98; L6: L6 1.00; T13: ordinary 0.53, L6 0.46; four_lumbar: ordinary 0.21, four_lumbar 0.79; both: ordinary 0.14, L6 0.83
- reader C, P(call | truth): ordinary: ordinary 0.99; L6: ordinary 0.05, L6 0.95; T13: ordinary 0.43, L6 0.40, T13 0.17; four_lumbar: four_lumbar 1.00; both: ordinary 0.96

## Real-frame G3 test persons (T2 = COBRA, T3 = C-ArmLSpine) under the frozen rule

n_min (section 5): {'at_risk (H1, H3-H5; p0 0.822)': 19, 'ordinary (H6; p0 0.926)': 48, 'at_risk vs published (H2; p0 0.976)': 152}. Counts are persons; `with_frames` = persons with an exported real frame.

### T2: 159 persons, 107 with real frames

| assigned subtype | persons | with frames | unanimous | unanimous with frames | T13 excluded by an anchored count | withheld: Varian not exported | withheld: no exported frame |
|---|---:|---:|---:|---:|---:|---:|---:|
| excluded | 103 | 63 | 0 | 0 | 1 | 39 | 1 |
| ordinary | 56 | 44 | 9 | 5 | 0 | 10 | 2 |

Excluded, by reason: {"no reader could count (A": 88, "readers disagree or too few counted": 6, "subtype not calibrated to PPV lower bound >= 0.90": 9}

Frozen stratum (stratify.json, VERIDAH-based for COBRA) -> automated assignment: {"L6 -> excluded": 37, "L6 -> ordinary": 1, "T13 -> excluded": 8, "T13 -> ordinary": 37, "four_lumbar -> excluded": 8, "ordinary -> excluded": 23, "ordinary -> ordinary": 18, "unreadable -> excluded": 27}

### T3: 13 persons, 13 with real frames

| assigned subtype | persons | with frames | unanimous | unanimous with frames | T13 excluded by an anchored count | withheld: Varian not exported | withheld: no exported frame |
|---|---:|---:|---:|---:|---:|---:|---:|
| excluded | 13 | 13 | 0 | 0 | 0 | 0 | 0 |

Excluded, by reason: {"no reader could count (A": 13}

Frozen stratum (stratify.json, VERIDAH-based for COBRA) -> automated assignment: {"carmlspine_three_L6 -> excluded": 3, "ordinary -> excluded": 10}

## Transportability of the ordinary PPV (anchored thoracic count or not)

| rule | subset | assigned ordinary | correct | PPV [Wilson 95 %] | wrong truths |
|---|---|---:|---:|---|---|
| unanimity | anchored | 29 | 26 | 0.897 [0.736, 0.964] | {'L6': 2, 'T13': 1} |
| unanimity | unanchored | 525 | 523 | 0.996 [0.986, 0.999] | {'L6': 2} |
| two_of_three | anchored | 60 | 52 | 0.867 [0.758, 0.931] | {'L6': 7, 'T13': 1} |
| two_of_three | unanchored | 686 | 677 | 0.987 [0.975, 0.993] | {'L6': 9} |
| dawid_skene | anchored | 63 | 53 | 0.841 [0.732, 0.911] | {'L6': 9, 'T13': 1} |
| dawid_skene | unanchored | 729 | 716 | 0.982 [0.970, 0.990] | {'L6': 13} |

T2 persons assigned ordinary: 56, of whom 0 had a thoracic count anchored at T1; by frozen (VERIDAH) stratum {'T13': 37, 'ordinary': 18, 'L6': 1}; with frames {'T13': 30, 'ordinary': 13, 'L6': 1}. T13 prevalence in the calibration set is 4/945; an unanchored 'ordinary' call does not exclude T13, so the ordinary PPV measured here bounds the T13 error only at that prevalence. No reader anchored a thoracic count on any COBRA planning CT, so the T2 ordinary assignments rest on the lumbar count alone.

## Assignment counts per corpus (side, status, subtype or exclusion reason)

- **ctsp**: train | assigned_unanimous | ordinary: 435; train | assigned_rule | ordinary: 157; test | assigned_unanimous | ordinary: 47; val | assigned_unanimous | ordinary: 46; test | assigned_rule | ordinary: 20; val | assigned_rule | ordinary: 17; train | excluded | subtype not calibrated to PPV lower bound >= 0.90: 17; train | excluded | readers disagree or too few counted: 14; test | excluded | readers disagree or too few counted: 13; test | excluded | subtype not calibrated to PPV lower bound >= 0.90: 11; train | excluded | no reader could count (A: 8; val | excluded | subtype not calibrated to PPV lower bound >= 0.90: 5; train | excluded | the rule chosen for this subtype does not assign it: 5; val | excluded | readers disagree or too few counted: 3; test | excluded | the rule chosen for this subtype does not assign it: 2; val | excluded | no reader could count (A: 2
- **verse**: train | excluded | no reader could count (A: 75; train | assigned_unanimous | ordinary: 69; train | assigned_rule | ordinary: 68; train | excluded | subtype not calibrated to PPV lower bound >= 0.90: 24; test | assigned_rule | ordinary: 19; test | excluded | subtype not calibrated to PPV lower bound >= 0.90: 16; test | excluded | readers disagree or too few counted: 12; train | excluded | readers disagree or too few counted: 11; val | excluded | no reader could count (A: 10; test | assigned_unanimous | ordinary: 10; test | excluded | no reader could count (A: 9; val | assigned_unanimous | ordinary: 9; val | assigned_rule | ordinary: 8; train | excluded | the rule chosen for this subtype does not assign it: 5; val | excluded | subtype not calibrated to PPV lower bound >= 0.90: 4; val | excluded | the rule chosen for this subtype does not assign it: 2; val | excluded | readers disagree or too few counted: 2; test | excluded | the rule chosen for this subtype does not assign it: 2
- **cobra_ct**: train | excluded | no reader could count (A: 330; test | excluded | no reader could count (A: 88; train | assigned_rule | ordinary: 65; val | excluded | no reader could count (A: 58; train | assigned_unanimous | ordinary: 48; test | assigned_rule | ordinary: 47; hold | excluded | no reader could count (A: 10; test | excluded | subtype not calibrated to PPV lower bound >= 0.90: 9; val | assigned_unanimous | ordinary: 9; test | assigned_unanimous | ordinary: 9; test | excluded | readers disagree or too few counted: 6; hold | assigned_rule | ordinary: 6; val | assigned_rule | ordinary: 3; train | excluded | the rule chosen for this subtype does not assign it: 1; train | excluded | subtype not calibrated to PPV lower bound >= 0.90: 1; val | excluded | readers disagree or too few counted: 1; hold | assigned_unanimous | ordinary: 1
- **carmlspine**: train | excluded | no reader could count (A: 123; test | excluded | no reader could count (A: 13; val | excluded | no reader could count (A: 13
