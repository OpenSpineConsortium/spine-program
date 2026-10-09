# MAXIMIZE: every registry person the recipe allows, rendered

Written 2026-09-24 16:55 by `tools/rare_class_maximize.py` from `registry.csv` (6113 rows), the render roots' ann listings before the pass, and the collect step's files pulled from the grid (`SchwingNet/results/transitional_registry/maximize/after`, written 2026-09-24 16:51). Generated; the numbers below are computed, none typed. The AFTER frame counts are READ FROM DISK (`<root>_VERIFY.json` of `SchwingNet/slurm/rare_max_verify.sh`), and the held / stopped cases are the renderer's own records (`held_all.json`, the task logs).

## The rule applied

- Rendered for training: CT-only persons whose winning tier is `read` or `two-labeller`, one CT per person (the registry's winning case), every pose family (lateral x3, AP x3, arc obliques x4 at +/-35 and +/-50 deg yaw with cranio-caudal tilt) and every device card (bv_pulsera, cios_fusion, elekta_xvi, pixium_4600, surgio_b51_dr, varian_halcyon; DEVICE_SAMPLE_MODE=typicality) plus the raw bone DRR: 70 distinct frames per CT, no duplicates.
- Every ann carries patient_key, subtype, subtype_source, truth_tier, the modifiers (castellvi, four_lumbar, lumbar_rib), fused_mask_representation and mask_scheme, so the split and the stratified evaluation read the stratum and the tier off any frame.
- ID GUARD: a case is rendered only if its mask carries the ids its call names (L6 -> id 25, T13 -> 28, a four-lumbar call with the fused body merged or unlabelled -> exactly four lumbar ids). Otherwise the renderer HOLDS it (`<root>/held/<scheme>_<case>.json`) rather than box bodies under names the registry disputes. Held cases are listed by the collect step and stay in Greg's review queue.
- Waiting: single-labeller and morphology-only persons (adjudication first). Never rendered: COBRA, C-ArmLSpine, DeepFluoro, Ljubljana persons (real frames, TEST only).

## Persons per subtype: rendered before, rendered by this pass, waiting, unavailable

| subtype | source | tier | rendered before | planned by this pass | rendered (disk) | held (ID guard) | stopped (precheck) | unaccounted | waiting (adjudication) | real-frames TEST | unavailable |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| L6 | carmlspine | morphology-only | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| L6 | cobra2026 | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| L6 | cobra2026 | two-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| L6 | ctsp | read | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| L6 | ctsp | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| L6 | ctsp | two-labeller | 1 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 |
| L6 | ctspine1k | read | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| L6 | ctspine1k | two-labeller | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| L6 | ribfrac | morphology-only | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| L6 | totalsegmentator | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 |
| L6 | totalsegmentator | two-labeller | 1 | 12 | 10 | 0 | 2 | 0 | 0 | 0 | 1 |
| L6 | verse | read | 46 | 39 | 0 | 39 | 0 | 0 | 0 | 0 | 0 |
| T13 | ribfrac | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| T13 | totalsegmentator | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| T13 | totalsegmentator | two-labeller | 1 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| T13 | verse | read | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sacralised_L5_fused | ctsp | read | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sacralised_L5_fused | ctspine1k | read | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| sacralised_L5_fused | verse | read | 0 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 |
| castellvi_I_II | ctsp | read | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| castellvi_I_II | verse | read | 0 | 27 | 27 | 0 | 0 | 0 | 0 | 0 | 0 |
| lumbar_rib | ctsp | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 |
| lumbar_rib | ctsp | two-labeller | 0 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| lumbar_rib | verse | read | 0 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |
| unassigned | carmlspine | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| unassigned | cobra2026 | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| unassigned | cobra2026 | two-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| unassigned | ctsp | two-labeller | 3 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| unassigned | ribfrac | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| unassigned | totalsegmentator | single-labeller | 0 | 0 | 0 | 0 | 0 | 0 | 18 | 0 | 0 |
| unassigned | totalsegmentator | two-labeller | 0 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 1 |
| unassigned | verse | read | 0 | 23 | 22 | 1 | 0 | 0 | 0 | 0 | 0 |

Totals: rendered before 87; planned by this pass 165, of which rendered 109, held by the ID guard 54, stopped at the precheck 2, unaccounted 0; waiting 39, real-frame TEST 13, unavailable 2. Rendered transitional CTs now: 196.

## Frames per subtype, before and after, FROM DISK (per source, then summed)

Before = the ann snapshot taken at plan time (`before_frames.json`). New = what `rare_max_verify` counted in each root after the arrays ended. The VerSe pass rendered into the existing `verse_drr` root, so its new frames are the root's count minus the snapshot; the other three sources rendered into fresh `_arc` roots, so their new frames are the root's whole count. Every frame is one ann with one img npy (the verify skips an ann without its image).

| source | subtype | before | new (disk) | after |
|---|---|---:|---:|---:|
| verse | L6 | 3500 | 0 | 3500 |
| verse | T13 | 420 | 0 | 420 |
| verse | sacralised_L5_fused | 0 | 910 | 910 |
| verse | castellvi_I_II | 0 | 1890 | 1890 |
| verse | lumbar_rib | 0 | 840 | 840 |
| verse | unassigned | 0 | 1540 | 1540 |
| **verse** | **all** | **3920** | **5180** | **9100** |
| ctsp | L6 | 1476 | 0 | 1476 |
| ctsp | sacralised_L5_fused | 1021 | 0 | 1021 |
| ctsp | castellvi_I_II | 0 | 280 | 280 |
| ctsp | lumbar_rib | 0 | 630 | 630 |
| ctsp | unassigned | 337 | 0 | 337 |
| **ctsp** | **all** | **2834** | **910** | **3744** |
| totalsegmentator | L6 | 0 | 700 | 700 |
| totalsegmentator | T13 | 0 | 140 | 140 |
| totalsegmentator | unassigned | 0 | 490 | 490 |
| totalsegmentator | L6 (approx: 2 of 12 cases x mean 78) | 156 | 0 | 156 |
| totalsegmentator | T13 (approx: 3 cases) | 233 | 0 | 233 |
| totalsegmentator | none by ctd (approx: 7 cases) | 544 | 0 | 544 |
| **totalsegmentator** | **all** | **933** | **1330** | **2263** |
| ctspine1k | L6 | 0 | 70 | 70 |
| ctspine1k | sacralised_L5_fused | 0 | 140 | 140 |
| **ctspine1k** | **all** | **0** | **210** | **210** |
| carmlspine (real CBCT, TEST) | L6 (real CBCT, TEST) | 396 | 0 | 396 |
| **carmlspine (real CBCT, TEST)** | **all** | **396** | **0** | **396** |

| subtype | frames before | + new (disk) | frames after |
|---|---:|---:|---:|
| L6 | 4976 | 770 | 5746 |
| T13 | 420 | 140 | 560 |
| sacralised_L5_fused | 1021 | 1050 | 2071 |
| castellvi_I_II | 0 | 2170 | 2170 |
| lumbar_rib | 0 | 1470 | 1470 |
| unassigned | 337 | 2030 | 2367 |
| L6 (approx: 2 of 12 cases x mean 78) | 156 | 0 | 156 |
| L6 (real CBCT, TEST) | 396 | 0 | 396 |
| T13 (approx: 3 cases) | 233 | 0 | 233 |
| none by ctd (approx: 7 cases) | 544 | 0 | 544 |
| **all** | **8083** | **7630** | **15713** |

Before, per root (ann count; the TotalSegmentator root's per-subtype split follows the ctd subtypes of its 12 cases, seven of which read as ordinary spines by the ctd): `carmlspine_cbct_drr` 396, `ctsp_drr` 2834, `totalsegmentator_drr` 933, `verse_drr` 3920.

New frames per source, from disk: verse 5180 (74 CTs x 70), ctsp 910 (13 CTs x 70), totalsegmentator 1330 (19 CTs x 70), ctspine1k 210 (3 CTs x 70). Projected at plan time: verse 7980 (114 CTs), ctsp 1750 (25 CTs), totalsegmentator 1470 (21 CTs), ctspine1k 350 (5 CTs).

## What the collect step verified (`rare_class_verify.py` on the grid, one report per root)

| root | cases with frames | frames (raw + styled) | per view | below floor (60) | bad anns | patient_keys unmatched | missing = held + stopped? |
|---|---:|---|---|---|---|---|---|
| `verse_drr` | 130 | 9100 (1300 + 7800) | ap 2730, lat 2730, obl 3640 | none | 0 | 0 | yes |
| `ctsp_drr_arc` | 13 | 910 (130 + 780) | ap 273, lat 273, obl 364 | none | 0 | 0 | yes |
| `totalsegmentator_drr_arc` | 19 | 1330 (190 + 1140) | ap 399, lat 399, obl 532 | none | 0 | 0 | yes |
| `ctspine1k_drr_arc` | 3 | 210 (30 + 180) | ap 63, lat 63, obl 84 | none | 0 | 0 | yes |

Per-class silhouettes worth knowing before anyone reads them as a defect: the TotalSegmentator `unassigned` stratum carries L1-L4 and no L5 in any frame because every one of its cases is a four-lumbar call that the `require_n_lumbar = 4` guard passed with exactly four lumbar ids; the `sacralised_L5_fused` strata carry no L5 because the fused body is merged into the sacrum id; VerSe frames carry no `sacrum` class because the VerSeFusion unified mask has no sacrum id.

## Oversampling weights, from the decided recipe

The recipe (docs/FLAGSHIP_PLAN.md, 'Ratio and oversampling'; docs/RESUME_2026-09-22_PM.md ratio table) fixes four numbers and forbids a fifth:

1. Real transitional frames are repeated **4x per epoch** in the fine-tune stage (VERIDAH 4x; Dushenev recall peaks at 4x). Real transitional people are TEST here, so this weight applies to no training frame of this bank; it is recorded so nobody re-derives it.
2. Variants in **25-35 % of rendered CTs, by choosing which CTs to render**, never by duplicating renders (x12 duplication once bought L6 Dice 0.000).
3. Synthetic per real rare frame capped near **10:1**; real frames 10-20 % of the sampled fine-tune mix.
4. 200-500 renders per CT, transitional CTs first.
5. No parity rebalancing: none (no weighted BCE, no parity resampling); rare recall is reported with PR-AUC.

What that implies for this bank. After this pass the rendered transitional CTs number 196 (rendered before 87 + rendered by this pass from disk 109; the 54 held and 2 stopped cases do not count) (read + two-labeller, CT-only) against ~2404 CTs in the whole render corpus (CTSpinoPelvic1K 802 + TotalSegmentator 1,228 + VerSe 374, every CT rendered under G4), a variant share of 8.2 % by CT. The 25-35 % target is reached in the SAMPLER, not by duplication: draw transitional CTs' frames with weight **w = 3.8 to 6.1** relative to an ordinary CT's frames (w = share/(1-share) x N_ordinary/N_transitional), applied per CT so that no frame is repeated within an epoch (70 distinct frames per transitional CT here; the ordinary bank's per-CT frame count sets how often each is seen). Per subtype the weight is the same w: the recipe balances variant vs ordinary, never subtype vs subtype (parity rebalancing is refused).

| subtype | transitional CTs rendered after this pass | per-CT sampling weight (25 % / 35 % target) |
|---|---:|---|
| L6 | 76 | 3.8 / 6.1 |
| T13 | 9 | 3.8 / 6.1 |
| sacralised_L5_fused | 27 | 3.8 / 6.1 |
| castellvi_I_II | 31 | 3.8 / 6.1 |
| lumbar_rib | 21 | 3.8 / 6.1 |
| unassigned | 32 | 3.8 / 6.1 |

Caveat stated plainly: the TotalSegmentator root's 12 first-pass cases include seven the ctd reads as ordinary spines; they count as rendered CTs above only where the registry still types them positive.

## Not rendered by this pass, and why

Unavailable (no mask or CT the recipe can use):

- `ts:s1974` (L6, two-labeller): v300-only scan: no SPINEPS seg-vert mask in ~/bench_ts/spineps/native_ctd, no v201 CT
- `ts:s2047` (unassigned, two-labeller): v300-only scan: no SPINEPS seg-vert mask in ~/bench_ts/spineps/native_ctd, no v201 CT

Waiting (52 persons; `waiting.csv`):

- carmlspine / L6: 3 (real-frames)
- carmlspine / unassigned: 1 (real-frames)
- cobra2026 / L6: 3 (real-frames)
- cobra2026 / unassigned: 6 (real-frames)
- ctsp / L6: 1 (waits for adjudication (single-labeller / morphology-only))
- ctsp / lumbar_rib: 5 (waits for adjudication (single-labeller / morphology-only))
- ribfrac / L6: 1 (waits for adjudication (single-labeller / morphology-only))
- ribfrac / T13: 4 (waits for adjudication (single-labeller / morphology-only))
- ribfrac / unassigned: 1 (waits for adjudication (single-labeller / morphology-only))
- totalsegmentator / L6: 8 (waits for adjudication (single-labeller / morphology-only))
- totalsegmentator / T13: 1 (waits for adjudication (single-labeller / morphology-only))
- totalsegmentator / unassigned: 18 (waits for adjudication (single-labeller / morphology-only))

### Held by the ID GUARD, from the renderer's own records (`held_all.json`)

The mask cannot carry the call; a review verdict or a mask relabel unblocks each one. Every held case that still needs a verdict is in its source's review queue with the reason `ID guard: mask cannot carry the registry call` (verse `review_queue/queue.csv`, ctsp `review_queue/review_queue.csv`, ctspine1k `other_ct/review_queue/index.csv`; column `id_guard`), no render duplicated. A held case whose PERSON is already in the bank under another scan (the registry's winning case was a scan without the junction in its field) is marked below and kept out of the queue: nothing is lost and nothing needs a verdict.

**verse** (`verse_drr/held/`): 40 of 114 planned

- `verse:verse024` (case verse024; L6, read): mask carries ids [15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse026` (case verse026; L6, read): mask carries ids [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse034` (case verse034; L6, read): mask carries ids [17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse085` (case verse085; L6, read): mask carries ids [20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse088` (case verse088; L6, read): mask carries ids [16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse403` (case verse208; L6, read): mask carries ids [1, 2, 3, 4, 5, 6, 7, 8, 9] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call -- PERSON ALREADY RENDERED under verse255 (this scan's field has no lumbosacral junction); no review needed
- `verse:verse406` (case verse214; L6, read): mask carries ids [1, 2, 3, 4, 5, 6, 7, 8, 9] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call -- PERSON ALREADY RENDERED under verse261 (this scan's field has no lumbosacral junction); no review needed
- `verse:verse502` (case verse502; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse510` (case verse510; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse512` (case verse512; L6, read): mask carries ids [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse513` (case verse513; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse514` (case verse514; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse518` (case verse518; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse526` (case verse526; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse527` (case verse527; L6, read): mask carries ids [15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse529` (case verse529; L6, read): mask carries ids [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse534` (case verse534; L6, read): mask carries ids [17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse535` (case verse535; L6, read): mask carries ids [16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse536` (case verse536; L6, read): mask carries ids [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse544` (case verse544; L6, read): mask carries ids [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse545` (case verse545; L6, read): mask carries ids [18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse554` (case verse554; L6, read): mask carries ids [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse555` (case verse555; L6, read): mask carries ids [16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse556` (case verse556; L6, read): mask carries ids [15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse557` (case verse557; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse559` (case verse559; unassigned, read): mask carries 5 lumbar ids [20, 21, 22, 23, 24] but the call (unassigned, read) needs exactly 4
- `verse:verse572` (case verse572; L6, read): mask carries ids [19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse581` (case verse581; L6, read): mask carries ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse587` (case verse587; L6, read): mask carries ids [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse590` (case verse590; L6, read): mask carries ids [17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse592` (case verse592; L6, read): mask carries ids [17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse599` (case verse599; L6, read): mask carries ids [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse606` (case verse606; L6, read): mask carries ids [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse609` (case verse609; L6, read): mask carries ids [19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse616` (case verse616; L6, read): mask carries ids [16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse618` (case verse618; L6, read): mask carries ids [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse626` (case verse626; L6, read): mask carries ids [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse636` (case verse636; L6, read): mask carries ids [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse765` (case verse765; L6, read): mask carries ids [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call
- `verse:verse814` (case verse814; L6, read): mask carries ids [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24] but the L6 call (read) needs [25]; missing [25]: rendered names would contradict the call

**ctsp** (`ctsp_drr_arc/held/`): 12 of 25 planned

- `ctsp:0090` (case 0090; L6, two-labeller): mask carries ids [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:0105` (case 0105; L6, two-labeller): mask carries ids [18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:0349` (case 0349; unassigned, two-labeller): mask carries 5 lumbar ids [20, 21, 22, 23, 24] but the call (unassigned, two-labeller) needs exactly 4
- `ctsp:0359` (case 0359; L6, two-labeller): mask carries ids [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:0474` (case 0474; L6, two-labeller): mask carries ids [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:0544` (case 0544; L6, two-labeller): mask carries ids [16, 17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:0552` (case 0552; L6, two-labeller): mask carries ids [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:0672` (case 0672; L6, two-labeller): mask carries ids [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:0895` (case 0895; L6, two-labeller): mask carries ids [17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:1000` (case 1000; unassigned, two-labeller): mask carries 5 lumbar ids [20, 21, 22, 23, 24] but the call (unassigned, two-labeller) needs exactly 4
- `ctsp:1151` (case 1151; L6, two-labeller): mask carries ids [17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctsp:1153` (case 1153; L6, two-labeller): mask carries ids [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call

**ctspine1k** (`ctspine1k_drr_arc/held/`): 2 of 5 planned

- `ctspine1k:MSD-T10:liver_119` (case liver_119; L6, two-labeller): mask carries ids [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call
- `ctspine1k:MSD-T10:liver_95` (case liver_95; L6, two-labeller): mask carries ids [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] but the L6 call (two-labeller) needs [25]; missing [25]: rendered names would contradict the call

Holds that wait for a verdict: 52 of 54 (2 are persons already in the bank under another scan).

### Stopped at the stage precheck (never reached the renderer; `precheck_stopped.json`, from the task logs)

- `totalsegmentator:TS_s0077` (L6, two-labeller; task 40437726_2, FAILED 5:0 after 00:00:11): SpinepsIdError [veridah_skipped_name]: VERIDAH's ctd skips T12 between T11 and L1 at a normal spacing (30.7 mm, local 26.6 mm), so the names on one side of the skip are one level off. Name this case from another labeller, or pass allow_skipped_names=True where another labeller gates every name. -- refusal (by design): the SPINEPS mask's ids cannot be read as VerSe names, so the renderer never saw the case; the same guard that caught the raw-id harvests (tools/spineps_ids.py) fired on a skipped name. Not rendered, not held; stays in the TotalSegmentator review queue (already listed at priority 1).
- `totalsegmentator:TS_s0477` (L6, two-labeller; task 40437726_9, FAILED 5:0 after 00:00:11): SpinepsIdError [veridah_skipped_name]: VERIDAH's ctd skips T12 between T11 and L1 at a normal spacing (27.5 mm, local 26.3 mm), so the names on one side of the skip are one level off. Name this case from another labeller, or pass allow_skipped_names=True where another labeller gates every name. -- refusal (by design): same guard, same reason as TS_s0077. The stream's SUMMARY had already predicted s0477 as a 'rib-less T12' kind; the ctd's skipped T12 is the same finding seen from the id side. Not rendered, not held; stays in the TotalSegmentator review queue (already listed at priority 1).

### Planned but neither rendered, held nor stopped

- none: every planned case is accounted for

What the plan expected the guard to hold, for the record (written before the arrays ran):

- CTSpinoPelvic1K two-labeller L6 candidates 'the release did not call' (0090, 0105, 0359, 0474, 0544, 0552, 0672, 0895, 1151, 1153): the v11 release label names five lumbar bodies and a rib-free T12; L6 is by the rib convention (the registry's `1-candidate` queue). Rendering them would box the sixth free body as T12. The mechanical relabel (release 19..24 -> 20..25, thoracic unchanged) is one line once Greg's verdict lands; it is not applied here.
- CTSpinoPelvic1K two-labeller unassigned 0349 and 1000 (four rib-free bodies by SPINEPS and TotalSegmentator against five release lumbar ids): held by `require_n_lumbar = 4`.
- VerSe read L6 persons whose VerSeFusion mask carries no id 25 (the split plan's `L6/audit_only` stratum, 36 persons across sides): held by `require_ids = [25]`; the read is the truth, the mask is not yet, and a rendered frame needs the mask.
- TotalSegmentator two-labeller L6 cases whose SPINEPS ctd names five lumbar (the 'rib-less T12' kind: s0158, s0477, s0683 per the stream's SUMMARY): held by `require_ids = [25]` if the ctd relabel did not write a 25.

## Jobs (all ended; collected from disk 2026-09-24 16:51; collect step = `SchwingNet/slurm/rare_max_verify.sh`)

The table below is the plan-time PENDING list, kept as the record of what was submitted and when. Every array task ended (sacct: COMPLETED, except the two TotalSegmentator tasks that FAILED 5:0 at the precheck in 11 s, listed under 'Stopped at the stage precheck' above) and the verify wrote its reports.

| job id | name | submitted | ETA | output | collected by |
|---|---|---|---|---|---|
| 40437724 | rare_max_verse (array 0-15, reqp) | 2026-09-24 15:46 EDT | ~16:40 EDT (35-60 min after start; reqp had 155 idle nodes, queue wait minutes) | `/rs/rs_grp_oschome/go2432/data/rare_class/verse_drr/{ann,img,qc,held}/ + RENDER_INFO_max_shard*.json; logs ~/logs/rare_max_verse_40437724_*.out` | rare_max_verify 40437728 -> $RC/maximize_after/verse_drr_VERIFY.json |
| 40437725 | rare_max_stage KIND=ctsp (array 0-24, reqp) | 2026-09-24 15:46 EDT | ~16:10 EDT (one CT per task, 5-15 min each, all 25 in parallel) | `/rs/rs_grp_oschome/go2432/data/rare_class/ctsp_drr_arc/{ann,img,qc,held}/ (+ ctsp_stage/); logs ~/logs/rare_max_stage_40437725_*.out` | rare_max_verify 40437728 -> $RC/maximize_after/ctsp_drr_arc_VERIFY.json + held_all.json |
| 40437726 | rare_max_stage KIND=totalsegmentator (array 0-20, reqp) | 2026-09-24 15:46 EDT | ~16:50 EDT (20-60 min per CT; 1.5 mm -> 1 mm upsample triples the voxels) | `/rs/rs_grp_oschome/go2432/data/rare_class/totalsegmentator_drr_arc/{ann,img,qc,held}/ (+ ts_stage_arc/); logs ~/logs/rare_max_stage_40437726_*.out` | rare_max_verify 40437728 -> $RC/maximize_after/totalsegmentator_drr_arc_VERIFY.json + held_all.json |
| 40437727 | rare_max_stage KIND=ctspine1k (array 0-4, reqp) | 2026-09-24 15:46 EDT | ~16:50 EDT (20-60 min per MSD-T10 liver volume) | `/rs/rs_grp_oschome/go2432/data/rare_class/ctspine1k_drr_arc/{ann,img,qc,held}/ (+ ctspine1k_stage/); logs ~/logs/rare_max_stage_40437727_*.out` | rare_max_verify 40437728 -> $RC/maximize_after/ctspine1k_drr_arc_VERIFY.json + held_all.json |
| 40437728 | rare_max_verify (afterany of the four arrays) | 2026-09-24 15:46 EDT | ~17:00 EDT (starts when the slowest array ends; runs ~10 min) | `/rs/rs_grp_oschome/go2432/data/rare_class/maximize_after/{verse_drr,ctsp_drr_arc,totalsegmentator_drr_arc,ctspine1k_drr_arc}_VERIFY.json, held_all.json, render_info/; log ~/logs/rare_max_verify_40437728.out` | NEXT SESSION: scp $RC/maximize_after/ -> SchwingNet/results/transitional_registry/maximize/after/; then `python tools/rare_class_maximize.py --rendered-json <after listing> --before-frames ...` rewrites MAXIMIZE.md with counts from disk; read held_all.json into the review queue |

- rare_max_verse (array 0-15, reqp): 114 cases / 16 shards = 7.1 cases per shard x 75-430 s per case (first pass, 4 CPUs; mean ~280 s) = 9-51 min, typical 35 min; 12 h limit
- rare_max_stage KIND=ctsp (array 0-24, reqp): CTSP volume ~0.8 mm -> 1 mm iso, ~80-120 M voxels: 10 poses x rotate(ct+mask) + 6 stylings, 5-15 min per CT; 12 of the 25 are expected to be HELD by the id guard within the first minute (release mask names five lumbar)
- rare_max_stage KIND=totalsegmentator (array 0-20, reqp): precheck (assert_verse_monotonic + resample + HU proof) 1-3 min, then ~150 M voxels x 10 poses: 20-60 min per CT, 21 in parallel; 8 h limit
- rare_max_stage KIND=ctspine1k (array 0-4, reqp): MSD-T10 abdominal CT ~100 M voxels at 1 mm; 5 tasks in parallel; the two four-lumbar reads (liver_83, liver_93) pass or are held by require_n_lumbar=4 depending on how the CTSpine1K annotation drew the fused body
- rare_max_verify (afterany of the four arrays): rare_class_verify.py reads every ann (~11,000 new + 3,920 old) and dry-runs patient_keys.py per root: ~5-10 min

## Recipes per source (what each array does)

- **verse** -> `$RC/verse_drr`: layout `verse`, scheme `verse`, patient_id `{scheme}_{case}`, mask ids: verse_ids (VerSeFusion unified mask); source `$HOME/VerSeFusion/data/unified`; 114 cases in `rare_max_verse.json`.
- **ctsp** -> `$RC/ctsp_drr_arc`: layout `stage`, scheme `ctsp`, patient_id `{scheme}_{case}`, mask ids: verse_ids (CTSpinoPelvic1K v11 release label, 20..25 lumbar, 26 sacrum); source `$RC/ctsp_stage`; 25 cases in `rare_max_ctsp.json`.
- **totalsegmentator** -> `$RC/totalsegmentator_drr_arc`: layout `stage`, scheme `totalseg`, patient_id `ts_{case}`, mask ids: verse_ids_spineps (SPINEPS seg-vert relabelled by the VERIDAH ctd, ~/bench_ts/spineps/native_ctd); source `$RC/ts_stage_arc`; 21 cases in `rare_max_totalsegmentator.json`.
- **ctspine1k** -> `$RC/ctspine1k_drr_arc`: layout `stage`, scheme `ctspine1k`, patient_id `{scheme}_{case}`, mask ids: verse_ids (CTSpine1K release annotation; no sacrum id); source `$RC/ctspine1k_stage`; 5 cases in `rare_max_ctspine1k.json`.

Staging (rare_max_stage.sh): CTSpinoPelvic1K links `<id>_ct.nii.gz` + `<id>_label.nii.gz` (same grid); TotalSegmentator links the v201 CT and resamples the native_ctd SPINEPS mask onto it by affine (nearest), then proves the alignment by the median HU under the mask (> 100) and the id order by `spineps_ids.assert_verse_monotonic`; CTSpine1K links the HF-mirror volume and its `_seg` annotation. A precheck failure stops that task with a named reason; the renderer's guard then judges the ids.

## Identity note

`tools/patient_keys.py` keys `ctsp_<id>_<view>_p<k>` and `totalseg_<s>_<view>_p<k>` stems today but only for lat/ap views; the oblique stems (`_obl_p<k>`) and the `ctspine1k_<stem>` scheme are NEW and unkeyed until its SCHEMES table gains `(?:lat|ap|obl)` and a ctspine1k rule. Every ann carries `patient_key` explicitly, so the split can key on the ann field; CHK-8 (coverage) will name these roots until the table is extended, and a bank must refuse them until then.
