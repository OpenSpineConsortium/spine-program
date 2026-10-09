# The alphabet loss: does training the head for the alphabet comparison help it name a transitional spine?

Written 2026-09-23 01:29 by `SchwingNet/tools/alphabet_loss_report.py` from the files listed at the end. Bank `allspine_v9`; heads `tools/head_mixed_length.py --alphabet-loss LAMBDA` (the maths is in that module's docstring); scoring `tools/rigor_fixes.py a5-rows` / `a5`, one row per validation vertebra, five protocols, the same windows for every head at a seed. Jobs: slurm 40416278 (lambda 0), 40416279 (0.3), 40416280 (1.0), each seeds 0-2; bank index 40416335.

Every interval is a case-cluster bootstrap (2,000 resamples, cluster = patient for film, = person for renders), percentile unless marked BCa; `*` marks a paired difference whose interval excludes zero. Paired differences are against lambda = 0 at the SAME seed on the SAME rows.

## Verdict

- **lambda=0.3: NOT SHOWN TO HELP.** L6 recall on the 10 held-out L6 spines (random window) by seed ['67.35', '63.27', '64.29'] %, paired difference vs lambda = 0 [6.1224, 7.1429, 8.1633] pp (interval excludes zero on 1 of 3 seeds); real film ['98.82', '98.89', '98.83'] %, difference [-0.0729, 0.0146, -0.0583] pp, sources degrading: none; false-L6 rate ['0.29', '0.26', '0.27'] % of non-L6 bodies, difference [0.1162, 0.1239, 0.0929] pp (excludes zero on 3 seeds); L5 -> L6 ['3.66', '3.16', '3.36'] %; L6 precision ['63.46', '64.58', '64.29'] %.
- **lambda=1.0: TRADE-OFF: L6 recall up, film held, false-L6 up.** L6 recall on the 10 held-out L6 spines (random window) by seed ['72.45', '69.39', '67.35'] %, paired difference vs lambda = 0 [11.2245, 13.2653, 11.2245] pp (interval excludes zero on 3 of 3 seeds); real film ['98.88', '98.88', '98.85'] %, difference [-0.0146, 0.0, -0.0437] pp, sources degrading: none; false-L6 rate ['0.41', '0.38', '0.40'] % of non-L6 bodies, difference [0.2324, 0.2401, 0.2169] pp (excludes zero on 3 seeds); L5 -> L6 ['5.14', '4.74', '4.94'] %; L6 precision ['57.26', '58.12', '56.41'] %.

Rule: three facts are decided separately, each on the random-window protocol with the paired case-cluster interval against lambda = 0 at the same seed: RECALL (L6 recall on the evidence spines rises with the interval excluding zero on at least two of three seeds), FILM (no film source's interval excludes zero against the loss on two seeds), COST (the false-L6 rate rises with the interval excluding zero on two seeds). HELPS = recall up, film held, no cost shown; TRADE-OFF = recall up, film held, cost shown; HURTS = a film source degrades or recall falls; otherwise NOT SHOWN.

Read it as a trade, not a verdict on a single number: the head with the term names the extra body more often and calls an extra body more often where there is none. Which side costs more is decided where the call is used -- in `sweep_map.decode_alphabets` the L6 alphabet wins a chain only when the whole run scores higher under it, so a body-level false L6 is one vote among several, while a missed L6 is the one error the count cannot see. That coupling is the rule-based coupler's measurement (the other half of this workflow, `tools/alphabet_couple.py`, not built at the time of writing), not this report's.

## The evidence base: transitional spines the head never trained on

a transitional spine counts when its PERSON has films in the validation split and none in training under any alias (release id inside implant_/ctsp_/CTSP_COLONOG_ names, VerSe subject inside verse_scan-/verse names); split read from the bank's own rung_1.npz case/split arrays by SchwingNet/tools/bank_index.py.

- Transitional persons in the bank: 74; by split: {'train': 57, 'train+LEAK': 7, 'validation': 10}.
- **Evidence persons: 10 with an L6, 0 with a T13.** L6 validation films by source: {'ctsp_drr': 3, 'verse_drr': 10, 'physics_drr': 21, 'physics_rare': 100}.
- **T13: no validation film carries one**; in training: {'verse_drr': 6, 'physics_drr': 7, 'physics_rare': 24}. A T13 recall cannot be measured on this bank's validation split; it is not quoted.
- Four-lumbar films (L4 directly above the sacrum) by split: {'train': 10, 'val': 2}.
- Persons on both sides of the split under two names: 164 in the whole bank; transitional ones with validation films, EXCLUDED from the evidence: `ctsp:0097` (2 val films, 23 train films; keys ['ctsp:0097', 'implant:0097_v0', 'implant:0097_v1']), `ctsp:0234` (4 val films, 23 train films; keys ['ctsp:0234', 'implant:0234_v0', 'implant:0234_v1']), `ctsp:0244` (21 val films, 1 train films; keys ['ctsp:0244', 'implant:0244_v1']), `ctsp:0302` (1 val films, 18 train films; keys ['ctsp:0302', 'implant:0302_v1']), `ctsp:0376` (16 val films, 1 train films; keys ['ctsp:0376', 'implant:0376_v1']), `ctsp:0486` (1 val films, 20 train films; keys ['ctsp:0486', 'implant:0486_v0']), `ctsp:0565` (20 val films, 3 train films; keys ['ctsp:0565', 'implant:0565_v0', 'implant:0565_v1']).

| person | source | L6 | T13 | validation films |
|---|---|---|---|---:|
| `verse:verse403` | verse | yes |  | 26 |
| `verse:verse406` | verse | yes |  | 31 |
| `verse:verse509` | verse | yes |  | 17 |
| `verse:verse517` | verse | yes |  | 18 |
| `verse:verse525` | verse | yes |  | 17 |
| `verse:verse540` | verse | yes |  | 22 |
| `verse:verse569` | verse | yes |  | 23 |
| `verse:verse604` | verse | yes |  | 20 |
| `verse:verse614` | verse | yes |  | 1 |
| `verse:verse816` | verse | yes |  | 1 |

## (a) Film naming must not degrade (random window, patient-clustered)

| arm | CSXA | BUU-LSPINE | NHANES | real film pooled | paired vs lambda=0: CSXA | BUU | NHANES |
|---|---|---|---|---|---|---|---|
| lambda=0 seed=0 | 99.92 [99.79, 100.00] (n=3745) | 97.79 [97.07, 98.46] (n=2664) | 96.91 [94.13, 98.93] (n=453) | 98.89 [98.56, 99.22] (n=6862) | -- | -- | -- |
| lambda=0 seed=1 | 99.81 [99.57, 99.97] (n=3745) | 97.79 [97.07, 98.50] (n=2664) | 97.57 [94.88, 99.51] (n=453) | 98.88 [98.51, 99.19] (n=6862) | -- | -- | -- |
| lambda=0 seed=2 | 99.76 [99.52, 99.95] (n=3745) | 97.90 [97.19, 98.54] (n=2664) | 97.57 [95.41, 99.16] (n=453) | 98.89 [98.54, 99.19] (n=6862) | -- | -- | -- |
| lambda=0.3 seed=0 | 99.84 [99.57, 100.00] (n=3745) | 97.60 [96.88, 98.31] (n=2664) | 97.57 [94.94, 99.52] (n=453) | 98.82 [98.46, 99.16] (n=6862) | -0.08 pp [-0.21, +0.00] | -0.19 pp [-0.41, +0.04] | +0.66 pp [+0.00, +1.45] |
| lambda=0.3 seed=1 | 99.84 [99.63, 99.97] (n=3745) | 97.86 [97.15, 98.54] (n=2664) | 97.13 [94.26, 99.15] (n=453) | 98.89 [98.53, 99.20] (n=6862) | +0.03 pp [+0.00, +0.08] | +0.08 pp [-0.11, +0.26] | -0.44 pp [-1.44, +0.00] |
| lambda=0.3 seed=2 | 99.81 [99.63, 99.95] (n=3745) | 97.79 [97.07, 98.50] (n=2664) | 96.91 [93.60, 99.30] (n=453) | 98.83 [98.46, 99.14] (n=6862) | +0.05 pp [-0.05, +0.19] | -0.11 pp [-0.49, +0.26] | -0.66 pp [-2.98, +0.84] |
| lambda=1.0 seed=0 | 99.92 [99.81, 100.00] (n=3745) | 97.71 [96.96, 98.42] (n=2664) | 97.13 [94.39, 99.15] (n=453) | 98.88 [98.53, 99.19] (n=6862) | +0.00 pp [-0.08, +0.08] | -0.08 pp [-0.41, +0.26] | +0.22 pp [-0.49, +0.98] |
| lambda=1.0 seed=1 | 99.81 [99.60, 99.97] (n=3745) | 97.97 [97.30, 98.61] (n=2664) | 96.47 [93.01, 98.96] (n=453) | 98.88 [98.53, 99.19] (n=6862) | +0.00 pp [-0.11, +0.11] | +0.19 pp [-0.08, +0.45] | -1.10 pp [-3.98, +0.64] |
| lambda=1.0 seed=2 | 99.79 [99.60, 99.92] (n=3745) | 97.86 [97.11, 98.54] (n=2664) | 96.91 [93.60, 99.30] (n=453) | 98.85 [98.47, 99.19] (n=6862) | +0.03 pp [-0.08, +0.16] | -0.04 pp [-0.41, +0.38] | -0.66 pp [-2.98, +0.84] |

Band 9 (the whole film in view), same layout:

| arm | CSXA | BUU-LSPINE | NHANES | paired: CSXA | BUU | NHANES |
|---|---|---|---|---|---|---|
| lambda=0 seed=0 | 99.97 [99.92, 100.00] | 99.96 [99.89, 100.00] | 98.68 [96.21, 100.00] | -- | -- | -- |
| lambda=0 seed=1 | 99.95 [99.84, 100.00] | 99.96 [99.89, 100.00] | 98.68 [96.21, 100.00] | -- | -- | -- |
| lambda=0 seed=2 | 99.97 [99.92, 100.00] | 99.96 [99.89, 100.00] | 98.90 [96.54, 100.00] | -- | -- | -- |
| lambda=0.3 seed=0 | 99.89 [99.68, 100.00] | 99.96 [99.89, 100.00] | 98.90 [96.54, 100.00] | -0.08 pp [-0.24, +0.00] | +0.00 pp [+0.00, +0.00] | +0.22 pp [+0.00, +0.73] |
| lambda=0.3 seed=1 | 99.95 [99.84, 100.00] | 99.96 [99.89, 100.00] | 98.23 [95.51, 100.00] | +0.00 pp [+0.00, +0.00] | +0.00 pp [+0.00, +0.00] | -0.44 pp [-1.44, +0.00] |
| lambda=0.3 seed=2 | 99.95 [99.84, 100.00] | 99.96 [99.89, 100.00] | 97.79 [94.21, 100.00] | -0.03 pp [-0.16, +0.05] | +0.00 pp [+0.00, +0.00] | -1.10 pp [-3.60, +0.00] |
| lambda=1.0 seed=0 | 100.00 [100.00, 100.00] | 99.96 [99.89, 100.00] | 98.68 [96.12, 100.00] | +0.03 pp [+0.00, +0.08] | +0.00 pp [+0.00, +0.00] | +0.00 pp [-0.67, +0.66] |
| lambda=1.0 seed=1 | 100.00 [100.00, 100.00] | 99.96 [99.89, 100.00] | 98.01 [94.91, 100.00] | +0.05 pp [+0.00, +0.16] | +0.00 pp [+0.00, +0.00] | -0.66 pp [-3.47, +1.18] |
| lambda=1.0 seed=2 | 99.97 [99.92, 100.00] | 99.96 [99.89, 100.00] | 97.79 [94.21, 100.00] | +0.00 pp [-0.08, +0.08] | +0.00 pp [+0.00, +0.00] | -1.10 pp [-3.60, +0.00] |

## (b) L6 recall on the evidence spines, and what it costs

Recall = the L6 body named L6. Denominator = L6 crops over evidence persons (one crop per L6 body per rendered film/pose). The cost columns: L6 called on a body that is not L6 (all non-L6 validation bodies of non-leaking persons), the L5 -> L6 share in particular, and the naming of the other bodies on the L6 spines.

### random

| arm | L6 recall pooled | VerSe | CTSP | paired vs lambda=0 | false L6 (all non-L6) | L5 -> L6 | paired false-L6 | L6 precision | other bodies on L6 spines | paired |
|---|---|---|---|---|---|---|---|---|---|---|
| lambda=0 seed=0 | 61.22 [44.07, 79.17] (60/98, 10 persons) | 61.22 (60/98) | -- (None/None) | -- | 0.18 (23/12911) | 2.17 (22/1012) | -- | 72.29 | 62.08 (781/1258) | -- |
| lambda=0 seed=1 | 56.12 [40.87, 75.61] (55/98, 10 persons) | 56.12 (55/98) | -- (None/None) | -- | 0.14 (18/12911) | 1.78 (18/1012) | -- | 75.34 | 62.88 (791/1258) | -- |
| lambda=0 seed=2 | 56.12 [41.12, 75.01] (55/98, 10 persons) | 56.12 (55/98) | -- (None/None) | -- | 0.18 (23/12911) | 2.17 (22/1012) | -- | 70.51 | 63.20 (795/1258) | -- |
| lambda=0.3 seed=0 | 67.35 [54.35, 83.34] (66/98, 10 persons) | 67.35 (66/98) | -- (None/None) | +6.12 pp [+0.00, +13.26] | 0.29 (38/12911) | 3.66 (37/1012) | +0.12 pp [+0.06, +0.19] * | 63.46 | 63.51 (799/1258) | +1.43 pp [-0.46, +3.51] |
| lambda=0.3 seed=1 | 63.27 [46.22, 85.51] (62/98, 10 persons) | 63.27 (62/98) | -- (None/None) | +7.14 pp [+0.00, +17.21] | 0.26 (34/12911) | 3.16 (32/1012) | +0.12 pp [+0.06, +0.19] * | 64.58 | 64.39 (810/1258) | +1.51 pp [-2.04, +4.12] |
| lambda=0.3 seed=2 | 64.29 [50.86, 81.32] (63/98, 10 persons) | 64.29 (63/98) | -- (None/None) | +8.16 pp [+3.03, +13.16] * | 0.27 (35/12911) | 3.36 (34/1012) | +0.09 pp [+0.03, +0.16] * | 64.29 | 63.59 (800/1258) | +0.40 pp [-1.36, +1.96] |
| lambda=1.0 seed=0 | 72.45 [57.02, 90.63] (71/98, 10 persons) | 72.45 (71/98) | -- (None/None) | +11.22 pp [+5.56, +21.31] * | 0.41 (53/12911) | 5.14 (52/1012) | +0.23 pp [+0.15, +0.32] * | 57.26 | 64.15 (807/1258) | +2.07 pp [-0.40, +5.10] |
| lambda=1.0 seed=1 | 69.39 [57.14, 85.37] (68/98, 10 persons) | 69.39 (68/98) | -- (None/None) | +13.27 pp [+6.06, +19.35] * | 0.38 (49/12911) | 4.74 (48/1012) | +0.24 pp [+0.16, +0.33] * | 58.12 | 63.04 (793/1258) | +0.16 pp [-1.69, +2.44] |
| lambda=1.0 seed=2 | 67.35 [54.31, 84.21] (66/98, 10 persons) | 67.35 (66/98) | -- (None/None) | +11.22 pp [+6.40, +18.18] * | 0.40 (51/12911) | 4.94 (50/1012) | +0.22 pp [+0.13, +0.31] * | 56.41 | 64.39 (810/1258) | +1.19 pp [-1.47, +3.61] |

### maximal_band9

| arm | L6 recall pooled | VerSe | CTSP | paired vs lambda=0 | false L6 (all non-L6) | L5 -> L6 | paired false-L6 | L6 precision | other bodies on L6 spines | paired |
|---|---|---|---|---|---|---|---|---|---|---|
| lambda=0 seed=0 | 60.20 [40.74, 83.78] (59/98, 10 persons) | 60.20 (59/98) | -- (None/None) | -- | 0.19 (24/12911) | 2.27 (23/1012) | -- | 71.08 | 65.10 (819/1258) | -- |
| lambda=0 seed=1 | 56.12 [37.73, 80.37] (55/98, 10 persons) | 56.12 (55/98) | -- (None/None) | -- | 0.14 (18/12911) | 1.68 (17/1012) | -- | 75.34 | 66.06 (831/1258) | -- |
| lambda=0 seed=2 | 56.12 [39.36, 77.78] (55/98, 10 persons) | 56.12 (55/98) | -- (None/None) | -- | 0.12 (16/12911) | 1.58 (16/1012) | -- | 77.46 | 65.02 (818/1258) | -- |
| lambda=0.3 seed=0 | 64.29 [49.49, 83.59] (63/98, 10 persons) | 64.29 (63/98) | -- (None/None) | +4.08 pp [-4.17, +13.46] | 0.23 (30/12911) | 2.96 (30/1012) | +0.05 pp [+0.01, +0.09] * | 67.74 | 65.26 (821/1258) | +0.16 pp [-1.55, +1.78] |
| lambda=0.3 seed=1 | 60.20 [41.53, 85.37] (59/98, 10 persons) | 60.20 (59/98) | -- (None/None) | +4.08 pp [-1.45, +13.64] | 0.25 (32/12911) | 3.06 (31/1012) | +0.11 pp [+0.06, +0.17] * | 64.84 | 67.33 (847/1258) | +1.27 pp [-2.45, +3.98] |
| lambda=0.3 seed=2 | 63.27 [44.44, 85.92] (62/98, 10 persons) | 63.27 (62/98) | -- (None/None) | +7.14 pp [+1.69, +16.44] * | 0.24 (31/12911) | 3.06 (31/1012) | +0.12 pp [+0.04, +0.19] * | 66.67 | 66.53 (837/1258) | +1.51 pp [-0.47, +3.74] |
| lambda=1.0 seed=0 | 70.41 [54.07, 91.49] (69/98, 10 persons) | 70.41 (69/98) | -- (None/None) | +10.20 pp [+5.32, +18.09] * | 0.33 (43/12911) | 4.15 (42/1012) | +0.15 pp [+0.08, +0.22] * | 61.61 | 66.61 (838/1258) | +1.51 pp [-0.95, +3.79] |
| lambda=1.0 seed=1 | 68.37 [54.25, 86.81] (67/98, 10 persons) | 68.37 (67/98) | -- (None/None) | +12.24 pp [+4.35, +19.10] * | 0.34 (44/12911) | 4.25 (43/1012) | +0.20 pp [+0.13, +0.28] * | 60.36 | 66.22 (833/1258) | +0.16 pp [-2.35, +2.76] |
| lambda=1.0 seed=2 | 67.35 [50.84, 88.31] (66/98, 10 persons) | 67.35 (66/98) | -- (None/None) | +11.22 pp [+4.50, +21.51] * | 0.33 (42/12911) | 4.05 (41/1012) | +0.20 pp [+0.12, +0.29] * | 61.11 | 66.53 (837/1258) | +1.51 pp [-1.44, +4.29] |

### maximal_band3

| arm | L6 recall pooled | VerSe | CTSP | paired vs lambda=0 | false L6 (all non-L6) | L5 -> L6 | paired false-L6 | L6 precision | other bodies on L6 spines | paired |
|---|---|---|---|---|---|---|---|---|---|---|
| lambda=0 seed=0 | 58.16 [40.32, 76.12] (57/98, 10 persons) | 58.16 (57/98) | -- (None/None) | -- | 0.30 (39/12911) | 3.75 (38/1012) | -- | 59.38 | 59.78 (752/1258) | -- |
| lambda=0 seed=1 | 54.08 [34.74, 74.67] (53/98, 10 persons) | 54.08 (53/98) | -- (None/None) | -- | 0.23 (30/12911) | 2.87 (29/1012) | -- | 63.86 | 58.59 (737/1258) | -- |
| lambda=0 seed=2 | 52.04 [33.66, 72.34] (51/98, 10 persons) | 52.04 (51/98) | -- (None/None) | -- | 0.22 (28/12911) | 2.67 (27/1012) | -- | 64.56 | 58.27 (733/1258) | -- |
| lambda=0.3 seed=0 | 65.31 [49.64, 80.87] (64/98, 10 persons) | 65.31 (64/98) | -- (None/None) | +7.14 pp [+1.55, +12.50] * | 0.43 (55/12911) | 5.34 (54/1012) | +0.12 pp [+0.06, +0.19] * | 53.78 | 62.08 (781/1258) | +2.31 pp [+0.36, +4.58] * |
| lambda=0.3 seed=1 | 63.27 [46.24, 80.28] (62/98, 10 persons) | 63.27 (62/98) | -- (None/None) | +9.18 pp [+4.22, +15.58] * | 0.42 (54/12911) | 5.14 (52/1012) | +0.19 pp [+0.11, +0.28] * | 53.45 | 61.05 (768/1258) | +2.46 pp [+1.09, +4.07] * |
| lambda=0.3 seed=2 | 62.24 [44.86, 80.00] (61/98, 10 persons) | 62.24 (61/98) | -- (None/None) | +10.20 pp [+4.94, +15.86] * | 0.39 (50/12911) | 4.84 (49/1012) | +0.17 pp [+0.10, +0.25] * | 54.95 | 60.49 (761/1258) | +2.23 pp [+0.51, +4.04] * |
| lambda=1.0 seed=0 | 70.41 [53.76, 86.67] (69/98, 10 persons) | 70.41 (69/98) | -- (None/None) | +12.24 pp [+7.41, +20.46] * | 0.53 (69/12911) | 6.62 (67/1012) | +0.23 pp [+0.15, +0.32] * | 50.00 | 62.64 (788/1258) | +2.86 pp [-0.77, +7.82] |
| lambda=1.0 seed=1 | 68.37 [52.30, 83.56] (67/98, 10 persons) | 68.37 (67/98) | -- (None/None) | +14.29 pp [+6.98, +20.83] * | 0.57 (73/12911) | 6.92 (70/1012) | +0.33 pp [+0.24, +0.44] * | 47.86 | 62.48 (786/1258) | +3.90 pp [+1.47, +7.16] * |
| lambda=1.0 seed=2 | 68.37 [52.12, 83.52] (67/98, 10 persons) | 68.37 (67/98) | -- (None/None) | +16.33 pp [+7.79, +24.30] * | 0.54 (70/12911) | 6.72 (68/1012) | +0.33 pp [+0.23, +0.43] * | 48.91 | 61.69 (776/1258) | +3.42 pp [+0.50, +7.12] * |

What the head calls the L6 body (random window), by arm: lambda=0 seed=0: {'L5': 36, 'L6': 60, 'L4': 2}; lambda=0 seed=1: {'L5': 42, 'L6': 55, 'L4': 1}; lambda=0 seed=2: {'L6': 55, 'L5': 42, 'L4': 1}; lambda=0.3 seed=0: {'L5': 31, 'L6': 66, 'T5': 1}; lambda=0.3 seed=1: {'L5': 35, 'L6': 62, 'L4': 1}; lambda=0.3 seed=2: {'L6': 63, 'L5': 32, 'L4': 3}; lambda=1.0 seed=0: {'L5': 26, 'L6': 71, 'T13': 1}; lambda=1.0 seed=1: {'L5': 30, 'L6': 68}; lambda=1.0 seed=2: {'L6': 66, 'L5': 30, 'L4': 2}.

NOT evidence, shown only for the size of what was excluded: the L6 spines whose person also trains under another name (the CTSP implant twins). Random window:

| arm | L6 recall over the excluded persons | persons | paired vs lambda=0 |
|---|---|---:|---|
| lambda=0 seed=0 | 53.85 (28/52) | 6 | -- |
| lambda=0 seed=1 | 48.08 (25/52) | 6 | -- |
| lambda=0 seed=2 | 48.08 (25/52) | 6 | -- |
| lambda=0.3 seed=0 | 61.54 (32/52) | 6 | +7.69 pp [+0.00, +19.05] |
| lambda=0.3 seed=1 | 55.77 (29/52) | 6 | +7.69 pp [+4.35, +9.33] * |
| lambda=0.3 seed=2 | 59.62 (31/52) | 6 | +11.54 pp [+7.27, +21.05] * |
| lambda=1.0 seed=0 | 69.23 (36/52) | 6 | +15.38 pp [+8.06, +25.00] * |
| lambda=1.0 seed=1 | 76.92 (40/52) | 6 | +28.85 pp [+8.70, +41.33] * |
| lambda=1.0 seed=2 | 63.46 (33/52) | 6 | +15.38 pp [+6.41, +33.33] * |

### T13

Validation rows with truth T13: 0; evidence persons with a T13: 0. No T13 number is quoted from this bank. The VerSe T13 subjects are all in training (see the evidence base); a T13 recall needs a bank whose split holds one out, which is the rare-class parity bank's job.

## Each evidence spine's own behaviour (random window)

Per person: films in validation, L6 crops, L6 recall, what the L6 was called, accuracy over all its bodies, and how its films were named (`all right`; `L6 called L5, rest right` = the classic miss, the extra body invisible to morphology; `run shifted by one (cranial names)` = every wrong body named one level too cranial, i.e. the run read as an ordinary spine counted up from the sacrum -- the whole-run error the count would catch).

Pooled over the evidence spines' films, by arm (random window):

| arm | films | all right | L6 called L5, rest right | run shifted by one (cranial names) | run shifted by one (caudal names) | off by one, mixed | other |
|---|---:|---:|---:|---:|---:|---:|---:|
| lambda=0 seed=0 | 176 | 54 (31 %) | 2 (1 %) | 47 (27 %) | 10 (6 %) | 23 (13 %) | 40 (23 %) |
| lambda=0 seed=1 | 176 | 56 (32 %) | 2 (1 %) | 49 (28 %) | 9 (5 %) | 23 (13 %) | 37 (21 %) |
| lambda=0 seed=2 | 176 | 55 (31 %) | 1 (1 %) | 46 (26 %) | 9 (5 %) | 28 (16 %) | 37 (21 %) |
| lambda=0.3 seed=0 | 176 | 60 (34 %) | 1 (1 %) | 43 (24 %) | 9 (5 %) | 25 (14 %) | 38 (22 %) |
| lambda=0.3 seed=1 | 176 | 64 (36 %) | 2 (1 %) | 41 (23 %) | 10 (6 %) | 26 (15 %) | 33 (19 %) |
| lambda=0.3 seed=2 | 176 | 66 (38 %) | 3 (2 %) | 34 (19 %) | 10 (6 %) | 24 (14 %) | 39 (22 %) |
| lambda=1.0 seed=0 | 176 | 65 (37 %) | 0 (0 %) | 40 (23 %) | 10 (6 %) | 26 (15 %) | 35 (20 %) |
| lambda=1.0 seed=1 | 176 | 66 (38 %) | 1 (1 %) | 35 (20 %) | 9 (5 %) | 27 (15 %) | 38 (22 %) |
| lambda=1.0 seed=2 | 176 | 67 (38 %) | 3 (2 %) | 31 (18 %) | 9 (5 %) | 25 (14 %) | 41 (23 %) |

### lambda=0 seed=0

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 85.71 | {'L5': 1, 'L6': 6} | 75.82 | {'all right': 15, 'other': 3, 'off by one, mixed': 3, 'run shifted by one (cranial names)': 3, 'run shifted by one (caudal names)': 2} |
| `verse:verse406` | verse | 31 | 11 | 81.82 | {'L5': 2, 'L6': 9} | 44.94 | {'run shifted by one (cranial names)': 10, 'other': 9, 'off by one, mixed': 6, 'all right': 6} |
| `verse:verse509` | verse | 17 | 16 | 81.25 | {'L5': 3, 'L6': 13} | 73.20 | {'L6 called L5, rest right': 1, 'other': 7, 'run shifted by one (cranial names)': 2, 'all right': 7} |
| `verse:verse517` | verse | 18 | 6 | 16.67 | {'L5': 5, 'L6': 1} | 70.29 | {'run shifted by one (cranial names)': 5, 'off by one, mixed': 5, 'run shifted by one (caudal names)': 4, 'all right': 2, 'other': 2} |
| `verse:verse525` | verse | 17 | 22 | 36.36 | {'L6': 8, 'L5': 12, 'L4': 2} | 33.33 | {'other': 3, 'run shifted by one (cranial names)': 11, 'all right': 2, 'off by one, mixed': 1} |
| `verse:verse540` | verse | 22 | 4 | 25.00 | {'L5': 3, 'L6': 1} | 53.79 | {'off by one, mixed': 3, 'other': 8, 'all right': 8, 'run shifted by one (cranial names)': 3} |
| `verse:verse569` | verse | 23 | 13 | 92.31 | {'L6': 12, 'L5': 1} | 75.71 | {'run shifted by one (caudal names)': 4, 'off by one, mixed': 3, 'other': 3, 'all right': 10, 'run shifted by one (cranial names)': 2, 'L6 called L5, rest right': 1} |
| `verse:verse604` | verse | 20 | 17 | 52.94 | {'L6': 9, 'L5': 8} | 45.13 | {'run shifted by one (cranial names)': 10, 'off by one, mixed': 2, 'other': 5, 'all right': 3} |
| `verse:verse614` | verse | 1 | 1 | 0.00 | {'L5': 1} | 70.00 | {'run shifted by one (cranial names)': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |

### lambda=0 seed=1

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 85.71 | {'L5': 1, 'L6': 6} | 79.67 | {'all right': 15, 'off by one, mixed': 5, 'run shifted by one (cranial names)': 2, 'other': 3, 'run shifted by one (caudal names)': 1} |
| `verse:verse406` | verse | 31 | 11 | 63.64 | {'L6': 7, 'L5': 4} | 49.80 | {'run shifted by one (cranial names)': 12, 'other': 7, 'run shifted by one (caudal names)': 1, 'all right': 7, 'off by one, mixed': 4} |
| `verse:verse509` | verse | 17 | 16 | 68.75 | {'L5': 5, 'L6': 11} | 62.09 | {'other': 8, 'run shifted by one (cranial names)': 2, 'all right': 6, 'off by one, mixed': 1} |
| `verse:verse517` | verse | 18 | 6 | 33.33 | {'L6': 2, 'L5': 4} | 72.00 | {'run shifted by one (cranial names)': 7, 'off by one, mixed': 4, 'run shifted by one (caudal names)': 3, 'all right': 3, 'other': 1} |
| `verse:verse525` | verse | 17 | 22 | 27.27 | {'L5': 15, 'L6': 6, 'L4': 1} | 37.33 | {'other': 2, 'run shifted by one (cranial names)': 11, 'L6 called L5, rest right': 1, 'all right': 2, 'off by one, mixed': 1} |
| `verse:verse540` | verse | 22 | 4 | 25.00 | {'L5': 3, 'L6': 1} | 50.34 | {'other': 9, 'off by one, mixed': 1, 'all right': 8, 'run shifted by one (caudal names)': 1, 'run shifted by one (cranial names)': 3} |
| `verse:verse569` | verse | 23 | 13 | 92.31 | {'L6': 12, 'L5': 1} | 75.71 | {'run shifted by one (caudal names)': 3, 'off by one, mixed': 5, 'other': 2, 'all right': 10, 'run shifted by one (cranial names)': 2, 'L6 called L5, rest right': 1} |
| `verse:verse604` | verse | 20 | 17 | 47.06 | {'L6': 8, 'L5': 9} | 44.25 | {'other': 5, 'off by one, mixed': 2, 'run shifted by one (cranial names)': 10, 'all right': 3} |
| `verse:verse614` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |

### lambda=0 seed=2

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 100.00 | {'L6': 7} | 78.57 | {'all right': 14, 'off by one, mixed': 6, 'run shifted by one (cranial names)': 2, 'other': 2, 'run shifted by one (caudal names)': 2} |
| `verse:verse406` | verse | 31 | 11 | 63.64 | {'L5': 4, 'L6': 7} | 50.20 | {'run shifted by one (cranial names)': 9, 'other': 9, 'off by one, mixed': 6, 'all right': 6, 'L6 called L5, rest right': 1} |
| `verse:verse509` | verse | 17 | 16 | 75.00 | {'L5': 4, 'L6': 12} | 71.24 | {'other': 6, 'all right': 8, 'off by one, mixed': 1, 'run shifted by one (cranial names)': 2} |
| `verse:verse517` | verse | 18 | 6 | 33.33 | {'L6': 2, 'L5': 4} | 65.71 | {'run shifted by one (cranial names)': 7, 'off by one, mixed': 1, 'run shifted by one (caudal names)': 5, 'all right': 3, 'other': 2} |
| `verse:verse525` | verse | 17 | 22 | 31.82 | {'L5': 14, 'L6': 7, 'L4': 1} | 32.00 | {'other': 2, 'run shifted by one (cranial names)': 11, 'all right': 2, 'off by one, mixed': 2} |
| `verse:verse540` | verse | 22 | 4 | 25.00 | {'L5': 3, 'L6': 1} | 48.97 | {'off by one, mixed': 2, 'other': 10, 'all right': 8, 'run shifted by one (cranial names)': 2} |
| `verse:verse569` | verse | 23 | 13 | 84.62 | {'L6': 11, 'L5': 2} | 79.35 | {'run shifted by one (caudal names)': 2, 'all right': 11, 'off by one, mixed': 6, 'other': 2, 'run shifted by one (cranial names)': 2} |
| `verse:verse604` | verse | 20 | 17 | 41.18 | {'L5': 10, 'L6': 7} | 46.02 | {'run shifted by one (cranial names)': 10, 'all right': 3, 'other': 4, 'off by one, mixed': 3} |
| `verse:verse614` | verse | 1 | 1 | 0.00 | {'L5': 1} | 80.00 | {'run shifted by one (cranial names)': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 88.89 | {'off by one, mixed': 1} |

### lambda=0.3 seed=0

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 85.71 | {'L5': 1, 'L6': 6} | 75.82 | {'all right': 14, 'other': 2, 'off by one, mixed': 6, 'run shifted by one (cranial names)': 2, 'run shifted by one (caudal names)': 2} |
| `verse:verse406` | verse | 31 | 11 | 81.82 | {'L6': 9, 'L5': 2} | 48.99 | {'run shifted by one (cranial names)': 9, 'other': 10, 'off by one, mixed': 3, 'all right': 8, 'L6 called L5, rest right': 1} |
| `verse:verse509` | verse | 17 | 16 | 75.00 | {'L5': 3, 'L6': 12, 'T5': 1} | 70.59 | {'run shifted by one (cranial names)': 2, 'other': 6, 'off by one, mixed': 2, 'all right': 7} |
| `verse:verse517` | verse | 18 | 6 | 50.00 | {'L5': 3, 'L6': 3} | 73.71 | {'run shifted by one (cranial names)': 4, 'off by one, mixed': 4, 'other': 3, 'all right': 4, 'run shifted by one (caudal names)': 3} |
| `verse:verse525` | verse | 17 | 22 | 45.45 | {'L6': 10, 'L5': 12} | 34.67 | {'other': 1, 'run shifted by one (cranial names)': 11, 'off by one, mixed': 2, 'all right': 3} |
| `verse:verse540` | verse | 22 | 4 | 25.00 | {'L5': 3, 'L6': 1} | 54.48 | {'off by one, mixed': 1, 'other': 9, 'all right': 9, 'run shifted by one (cranial names)': 3} |
| `verse:verse569` | verse | 23 | 13 | 100.00 | {'L6': 13} | 75.30 | {'run shifted by one (caudal names)': 4, 'run shifted by one (cranial names)': 3, 'off by one, mixed': 4, 'other': 3, 'all right': 9} |
| `verse:verse604` | verse | 20 | 17 | 58.82 | {'L6': 10, 'L5': 7} | 53.10 | {'other': 4, 'off by one, mixed': 2, 'run shifted by one (cranial names)': 9, 'all right': 5} |
| `verse:verse614` | verse | 1 | 1 | 100.00 | {'L6': 1} | 90.00 | {'off by one, mixed': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |

### lambda=0.3 seed=1

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 85.71 | {'L5': 1, 'L6': 6} | 71.98 | {'all right': 14, 'off by one, mixed': 6, 'run shifted by one (cranial names)': 2, 'other': 2, 'run shifted by one (caudal names)': 2} |
| `verse:verse406` | verse | 31 | 11 | 90.91 | {'L6': 10, 'L5': 1} | 53.85 | {'run shifted by one (cranial names)': 9, 'other': 7, 'run shifted by one (caudal names)': 1, 'all right': 11, 'off by one, mixed': 3} |
| `verse:verse509` | verse | 17 | 16 | 62.50 | {'L5': 6, 'L6': 10} | 60.78 | {'other': 7, 'off by one, mixed': 2, 'all right': 5, 'run shifted by one (cranial names)': 3} |
| `verse:verse517` | verse | 18 | 6 | 66.67 | {'L6': 4, 'L5': 2} | 74.29 | {'run shifted by one (cranial names)': 5, 'off by one, mixed': 3, 'run shifted by one (caudal names)': 4, 'all right': 6} |
| `verse:verse525` | verse | 17 | 22 | 27.27 | {'L5': 15, 'L6': 6, 'L4': 1} | 40.00 | {'other': 2, 'run shifted by one (cranial names)': 11, 'L6 called L5, rest right': 1, 'all right': 3} |
| `verse:verse540` | verse | 22 | 4 | 50.00 | {'L5': 2, 'L6': 2} | 56.55 | {'other': 9, 'run shifted by one (cranial names)': 2, 'all right': 8, 'off by one, mixed': 2, 'run shifted by one (caudal names)': 1} |
| `verse:verse569` | verse | 23 | 13 | 100.00 | {'L6': 13} | 79.35 | {'run shifted by one (caudal names)': 2, 'off by one, mixed': 7, 'other': 1, 'all right': 11, 'run shifted by one (cranial names)': 2} |
| `verse:verse604` | verse | 20 | 17 | 52.94 | {'L6': 9, 'L5': 8} | 51.33 | {'other': 5, 'off by one, mixed': 3, 'L6 called L5, rest right': 1, 'run shifted by one (cranial names)': 7, 'all right': 4} |
| `verse:verse614` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |

### lambda=0.3 seed=2

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 100.00 | {'L6': 7} | 75.27 | {'all right': 16, 'off by one, mixed': 4, 'run shifted by one (cranial names)': 2, 'other': 2, 'run shifted by one (caudal names)': 2} |
| `verse:verse406` | verse | 31 | 11 | 81.82 | {'L5': 2, 'L6': 9} | 52.23 | {'run shifted by one (cranial names)': 5, 'other': 9, 'off by one, mixed': 6, 'all right': 10, 'L6 called L5, rest right': 1} |
| `verse:verse509` | verse | 17 | 16 | 81.25 | {'L5': 3, 'L6': 13} | 68.63 | {'other': 6, 'run shifted by one (caudal names)': 1, 'all right': 6, 'run shifted by one (cranial names)': 3, 'off by one, mixed': 1} |
| `verse:verse517` | verse | 18 | 6 | 33.33 | {'L6': 2, 'L5': 4} | 66.29 | {'run shifted by one (cranial names)': 4, 'off by one, mixed': 3, 'run shifted by one (caudal names)': 5, 'all right': 3, 'other': 2, 'L6 called L5, rest right': 1} |
| `verse:verse525` | verse | 17 | 22 | 45.45 | {'L5': 10, 'L6': 10, 'L4': 2} | 38.67 | {'other': 3, 'run shifted by one (cranial names)': 9, 'all right': 5} |
| `verse:verse540` | verse | 22 | 4 | 25.00 | {'L5': 2, 'L6': 1, 'L4': 1} | 51.03 | {'other': 10, 'all right': 8, 'off by one, mixed': 1, 'run shifted by one (cranial names)': 3} |
| `verse:verse569` | verse | 23 | 13 | 84.62 | {'L6': 11, 'L5': 2} | 80.57 | {'run shifted by one (caudal names)': 2, 'all right': 12, 'off by one, mixed': 5, 'other': 2, 'run shifted by one (cranial names)': 1, 'L6 called L5, rest right': 1} |
| `verse:verse604` | verse | 20 | 17 | 47.06 | {'L5': 9, 'L6': 8} | 49.56 | {'other': 5, 'run shifted by one (cranial names)': 7, 'all right': 5, 'off by one, mixed': 3} |
| `verse:verse614` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 88.89 | {'off by one, mixed': 1} |

### lambda=1.0 seed=0

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 85.71 | {'L5': 1, 'L6': 6} | 75.27 | {'all right': 13, 'other': 3, 'off by one, mixed': 7, 'run shifted by one (cranial names)': 1, 'run shifted by one (caudal names)': 2} |
| `verse:verse406` | verse | 31 | 11 | 100.00 | {'L6': 11} | 50.61 | {'run shifted by one (cranial names)': 9, 'other': 8, 'off by one, mixed': 3, 'all right': 11} |
| `verse:verse509` | verse | 17 | 16 | 81.25 | {'L5': 2, 'L6': 13, 'T13': 1} | 71.90 | {'run shifted by one (cranial names)': 1, 'other': 7, 'off by one, mixed': 1, 'all right': 8} |
| `verse:verse517` | verse | 18 | 6 | 50.00 | {'L5': 3, 'L6': 3} | 74.29 | {'run shifted by one (cranial names)': 5, 'off by one, mixed': 4, 'other': 2, 'all right': 3, 'run shifted by one (caudal names)': 4} |
| `verse:verse525` | verse | 17 | 22 | 40.91 | {'L6': 9, 'L5': 13} | 37.33 | {'other': 1, 'run shifted by one (cranial names)': 12, 'all right': 4} |
| `verse:verse540` | verse | 22 | 4 | 75.00 | {'L5': 1, 'L6': 3} | 54.48 | {'off by one, mixed': 3, 'run shifted by one (cranial names)': 2, 'other': 8, 'all right': 9} |
| `verse:verse569` | verse | 23 | 13 | 100.00 | {'L6': 13} | 74.90 | {'run shifted by one (caudal names)': 4, 'run shifted by one (cranial names)': 3, 'off by one, mixed': 5, 'other': 2, 'all right': 9} |
| `verse:verse604` | verse | 20 | 17 | 64.71 | {'L6': 11, 'L5': 6} | 58.41 | {'run shifted by one (cranial names)': 7, 'off by one, mixed': 2, 'all right': 7, 'other': 4} |
| `verse:verse614` | verse | 1 | 1 | 100.00 | {'L6': 1} | 90.00 | {'off by one, mixed': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |

### lambda=1.0 seed=1

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 85.71 | {'L5': 1, 'L6': 6} | 76.37 | {'all right': 15, 'off by one, mixed': 3, 'run shifted by one (cranial names)': 2, 'other': 2, 'run shifted by one (caudal names)': 4} |
| `verse:verse406` | verse | 31 | 11 | 90.91 | {'L6': 10, 'L5': 1} | 48.58 | {'run shifted by one (cranial names)': 8, 'other': 9, 'run shifted by one (caudal names)': 1, 'all right': 9, 'off by one, mixed': 4} |
| `verse:verse509` | verse | 17 | 16 | 68.75 | {'L5': 5, 'L6': 11} | 64.71 | {'other': 6, 'off by one, mixed': 3, 'all right': 6, 'run shifted by one (cranial names)': 2} |
| `verse:verse517` | verse | 18 | 6 | 50.00 | {'L6': 3, 'L5': 3} | 74.29 | {'run shifted by one (cranial names)': 4, 'off by one, mixed': 4, 'run shifted by one (caudal names)': 3, 'all right': 5, 'L6 called L5, rest right': 1, 'other': 1} |
| `verse:verse525` | verse | 17 | 22 | 45.45 | {'L5': 12, 'L6': 10} | 41.33 | {'other': 2, 'run shifted by one (cranial names)': 10, 'all right': 5} |
| `verse:verse540` | verse | 22 | 4 | 50.00 | {'L5': 2, 'L6': 2} | 52.41 | {'other': 10, 'all right': 7, 'run shifted by one (cranial names)': 2, 'off by one, mixed': 3} |
| `verse:verse569` | verse | 23 | 13 | 100.00 | {'L6': 13} | 75.30 | {'run shifted by one (caudal names)': 1, 'off by one, mixed': 7, 'other': 3, 'all right': 10, 'run shifted by one (cranial names)': 2} |
| `verse:verse604` | verse | 20 | 17 | 64.71 | {'L6': 11, 'L5': 6} | 53.98 | {'other': 5, 'off by one, mixed': 3, 'all right': 7, 'run shifted by one (cranial names)': 5} |
| `verse:verse614` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |

### lambda=1.0 seed=2

| person | source | films | L6 crops | L6 recall | L6 called | all bodies | film patterns |
|---|---|---:|---:|---:|---|---:|---|
| `verse:verse403` | verse | 26 | 7 | 100.00 | {'L6': 7} | 79.12 | {'all right': 16, 'off by one, mixed': 3, 'run shifted by one (cranial names)': 2, 'other': 3, 'run shifted by one (caudal names)': 2} |
| `verse:verse406` | verse | 31 | 11 | 81.82 | {'L5': 2, 'L6': 9} | 53.44 | {'run shifted by one (cranial names)': 4, 'other': 9, 'off by one, mixed': 7, 'all right': 10, 'L6 called L5, rest right': 1} |
| `verse:verse509` | verse | 17 | 16 | 81.25 | {'L5': 3, 'L6': 13} | 65.36 | {'other': 6, 'off by one, mixed': 1, 'all right': 7, 'run shifted by one (cranial names)': 3} |
| `verse:verse517` | verse | 18 | 6 | 66.67 | {'L6': 4, 'L5': 2} | 71.43 | {'run shifted by one (cranial names)': 5, 'off by one, mixed': 2, 'run shifted by one (caudal names)': 5, 'all right': 5, 'other': 1} |
| `verse:verse525` | verse | 17 | 22 | 40.91 | {'L5': 11, 'L6': 9, 'L4': 2} | 34.67 | {'other': 3, 'run shifted by one (cranial names)': 9, 'L6 called L5, rest right': 1, 'all right': 3, 'off by one, mixed': 1} |
| `verse:verse540` | verse | 22 | 4 | 50.00 | {'L5': 2, 'L6': 2} | 53.10 | {'other': 10, 'all right': 7, 'run shifted by one (cranial names)': 2, 'off by one, mixed': 3} |
| `verse:verse569` | verse | 23 | 13 | 84.62 | {'L6': 11, 'L5': 2} | 78.14 | {'run shifted by one (caudal names)': 2, 'off by one, mixed': 4, 'other': 4, 'all right': 11, 'run shifted by one (cranial names)': 1, 'L6 called L5, rest right': 1} |
| `verse:verse604` | verse | 20 | 17 | 52.94 | {'L5': 8, 'L6': 9} | 53.10 | {'other': 5, 'run shifted by one (cranial names)': 5, 'all right': 6, 'off by one, mixed': 4} |
| `verse:verse614` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |
| `verse:verse816` | verse | 1 | 1 | 100.00 | {'L6': 1} | 100.00 | {'all right': 1} |

## The control reproduces the shipped heads

- seed=0: re-trained lambda=0 vs `SchwingNet/results/v9_seed0/mixed_allspine_v9_mixed_kmax4_seed0.json`: max |difference| over every per-source and overall figure of the trainer's own table 0.0; random-window real film shipped 98.89 vs re-trained 98.89; identical predictions on 79490 of 79490 rows (1.0); exact 0.8683 vs 0.8683.
- seed=1: re-trained lambda=0 vs `SchwingNet/results/v9_seed1/mixed_allspine_v9_mixed_kmax4_seed1.json`: max |difference| over every per-source and overall figure of the trainer's own table 0.0; random-window real film shipped 98.88 vs re-trained 98.88; identical predictions on 79490 of 79490 rows (1.0); exact 0.8666 vs 0.8666.
- seed=2: re-trained lambda=0 vs `SchwingNet/results/v9_seed2/mixed_allspine_v9_mixed_kmax4_seed2.json`: max |difference| over every per-source and overall figure of the trainer's own table 0.0; random-window real film shipped 98.89 vs re-trained 98.89; identical predictions on 79490 of 79490 rows (1.0); exact 0.8674 vs 0.8674.

A difference here is GPU non-determinism in the encoder's embedding pass and the head's training, not a code path: with lambda = 0 no alphabet code runs and no extra random draw is made.

## Did the term have anything to train on?

- lambda=0 seed=0: no alphabet term (lambda = 0); trainer's random-window real film 98.89, L6 {'n': 150, 'exact': 0.5867}.
- lambda=0 seed=1: no alphabet term (lambda = 0); trainer's random-window real film 98.88, L6 {'n': 150, 'exact': 0.5333}.
- lambda=0 seed=2: no alphabet term (lambda = 0); trainer's random-window real film 98.89, L6 {'n': 150, 'exact': 0.5333}.
- lambda=0.3 seed=0: anchored training films by source {'nhanes': 146, 'ctsp_drr': 686, 'verse_drr': 40, 'physics_drr': 36, 'physics_rare': 380}; epoch 0: 3007 anchored windows of 22443, alphabet CE 0.3084; last epoch: 3009 of 22443, alphabet CE 0.0464.
- lambda=0.3 seed=1: anchored training films by source {'nhanes': 146, 'ctsp_drr': 686, 'verse_drr': 40, 'physics_drr': 36, 'physics_rare': 380}; epoch 0: 3007 anchored windows of 22443, alphabet CE 0.3132; last epoch: 3009 of 22443, alphabet CE 0.0445.
- lambda=0.3 seed=2: anchored training films by source {'nhanes': 146, 'ctsp_drr': 686, 'verse_drr': 40, 'physics_drr': 36, 'physics_rare': 380}; epoch 0: 3010 anchored windows of 22443, alphabet CE 0.3065; last epoch: 3008 of 22443, alphabet CE 0.0418.
- lambda=1.0 seed=0: anchored training films by source {'nhanes': 146, 'ctsp_drr': 686, 'verse_drr': 40, 'physics_drr': 36, 'physics_rare': 380}; epoch 0: 3007 anchored windows of 22443, alphabet CE 0.2391; last epoch: 3009 of 22443, alphabet CE 0.0308.
- lambda=1.0 seed=1: anchored training films by source {'nhanes': 146, 'ctsp_drr': 686, 'verse_drr': 40, 'physics_drr': 36, 'physics_rare': 380}; epoch 0: 3007 anchored windows of 22443, alphabet CE 0.2447; last epoch: 3009 of 22443, alphabet CE 0.028.
- lambda=1.0 seed=2: anchored training films by source {'nhanes': 146, 'ctsp_drr': 686, 'verse_drr': 40, 'physics_drr': 36, 'physics_rare': 380}; epoch 0: 3010 anchored windows of 22443, alphabet CE 0.2499; last epoch: 3008 of 22443, alphabet CE 0.0284.

Anchored training films by source, alphabet and whether the thoracolumbar junction is in view (`source|alphabet|junction: films`): ctsp_drr|L4|junction: 10, ctsp_drr|L6|junction: 15, ctsp_drr|ordinary|junction: 659, ctsp_drr|ordinary|no_junction: 2, nhanes|ordinary|junction: 101, nhanes|ordinary|no_junction: 45, physics_drr|L6|junction: 4, physics_drr|L6|no_junction: 32, physics_rare|L6|junction: 60, physics_rare|L6|no_junction: 320, verse_drr|L6|junction: 37, verse_drr|L6|no_junction: 3.

## Seed spread

| lambda | real film random | CSXA | BUU | NHANES | L6 recall random pooled | L6 VerSe | L6 CTSP | false L6 random | L5 -> L6 | L6 precision |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 98.88-98.89 (n=3) | 99.76-99.92 (n=3) | 97.79-97.90 (n=3) | 96.91-97.57 (n=3) | 56.12-61.22 (n=3) | 56.12-61.22 (n=3) | -- | 0.14-0.18 (n=3) | 1.78-2.17 (n=3) | 70.51-75.34 (n=3) |
| 0.3 | 98.82-98.89 (n=3) | 99.81-99.84 (n=3) | 97.60-97.86 (n=3) | 96.91-97.57 (n=3) | 63.27-67.35 (n=3) | 63.27-67.35 (n=3) | -- | 0.26-0.29 (n=3) | 3.16-3.66 (n=3) | 63.46-64.58 (n=3) |
| 1.0 | 98.85-98.88 (n=3) | 99.79-99.92 (n=3) | 97.71-97.97 (n=3) | 96.47-97.13 (n=3) | 67.35-72.45 (n=3) | 67.35-72.45 (n=3) | -- | 0.38-0.41 (n=3) | 4.74-5.14 (n=3) | 56.41-58.12 (n=3) |

## (c) Not done here

The C-ArmLSpine k-curves (`results/a4.json`) are not re-run: they need the per-fold fine-tune (`slurm/carmlspine_cv_v9.sh`) initialised from the chosen head. That is the next step once a lambda is chosen, and it is the only place the real intra-operative frames enter.

## Files

Each arm's `a5.json` was written by `tools/rigor_fixes.py a5`, whose `headline[].label` text is hard-coded to say "v8 head"; the bank, encoder and head it scored are recorded in the same directory's `a5_rows_meta.json` and are allspine_v9. The numbers are read from `per_protocol`, never from that label.

- `SchwingNet/results/alpha_0.3_seed0/a5.json`
- `SchwingNet/results/alpha_0.3_seed0/a5_rows.csv`
- `SchwingNet/results/alpha_0.3_seed0/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed0.json`
- `SchwingNet/results/alpha_0.3_seed1/a5.json`
- `SchwingNet/results/alpha_0.3_seed1/a5_rows.csv`
- `SchwingNet/results/alpha_0.3_seed1/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed1.json`
- `SchwingNet/results/alpha_0.3_seed2/a5.json`
- `SchwingNet/results/alpha_0.3_seed2/a5_rows.csv`
- `SchwingNet/results/alpha_0.3_seed2/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed2.json`
- `SchwingNet/results/alpha_0_seed0/a5.json`
- `SchwingNet/results/alpha_0_seed0/a5_rows.csv`
- `SchwingNet/results/alpha_0_seed0/mixed_allspine_v9_mixed_kmax4_alpha0_seed0.json`
- `SchwingNet/results/alpha_0_seed1/a5.json`
- `SchwingNet/results/alpha_0_seed1/a5_rows.csv`
- `SchwingNet/results/alpha_0_seed1/mixed_allspine_v9_mixed_kmax4_alpha0_seed1.json`
- `SchwingNet/results/alpha_0_seed2/a5.json`
- `SchwingNet/results/alpha_0_seed2/a5_rows.csv`
- `SchwingNet/results/alpha_0_seed2/mixed_allspine_v9_mixed_kmax4_alpha0_seed2.json`
- `SchwingNet/results/alpha_1.0_seed0/a5.json`
- `SchwingNet/results/alpha_1.0_seed0/a5_rows.csv`
- `SchwingNet/results/alpha_1.0_seed0/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed0.json`
- `SchwingNet/results/alpha_1.0_seed1/a5.json`
- `SchwingNet/results/alpha_1.0_seed1/a5_rows.csv`
- `SchwingNet/results/alpha_1.0_seed1/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed1.json`
- `SchwingNet/results/alpha_1.0_seed2/a5.json`
- `SchwingNet/results/alpha_1.0_seed2/a5_rows.csv`
- `SchwingNet/results/alpha_1.0_seed2/mixed_allspine_v9_mixed_kmax4_alpha1.0_seed2.json`
- `SchwingNet/results/alphabet_loss_inputs/allspine_v9_bank_index.csv`
- `SchwingNet/results/alphabet_loss_inputs/allspine_v9_persons.json`
- `SchwingNet/results/anomalous_inventory.json`
- `SchwingNet/results/v9_seed0/a5_rows.csv`
- `SchwingNet/results/v9_seed0/mixed_allspine_v9_mixed_kmax4_seed0.json`
- `SchwingNet/results/v9_seed1/a5_rows.csv`
- `SchwingNet/results/v9_seed1/mixed_allspine_v9_mixed_kmax4_seed1.json`
- `SchwingNet/results/v9_seed2/a5_rows.csv`
- `SchwingNet/results/v9_seed2/mixed_allspine_v9_mixed_kmax4_seed2.json`

JSON: `SchwingNet/results/alphabet_loss.json`.
