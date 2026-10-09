# Repairs: one guard, one relabel, new trees beside the old

2026-09-23, task F4 of the SPINEPS-id workflow. What was wrong and where it reached: `IMPACT.md`. Nothing was
overwritten. Every repaired mask is in a NEW tree beside the old one, and the old trees are untouched. Nothing
is committed.

## 1. The guard: `tools/spineps_ids.py`

This is the one module where the rule "a SPINEPS id is a name only once that is shown" lives. Every reader that
turns an id into a level calls it.

- `assert_verse_monotonic(mask, ctd="auto", *, require_ctd=True, strict=False)` (alias `assert_verse_named`)
  **raises `SpinepsIdError`** unless every test below passes:
  1. The vertebra ids are all in the VerSe alphabet (1-28; id 80 is set aside, ids of 100 or more are discs and
     end plates).
  2. The ids run cranio-caudally in WORLD S, measured through the affine and never from an assumed axis order
     (T13 goes between T12 and L1, L6 between L5 and the sacrum).
  3. The ids agree with the ctd beside the mask: each VERIDAH point, taken to world space and back into the mask,
     must land in the instance carrying its own label. If 2 or more points disagree and they are at least 30 % of
     the tested points, the ids are not names.
  4. The ctd's own names run cranio-caudally. VERIDAH sometimes names 'S' above L5, and a mask that copies this is
     wrong however faithfully it copies.
  5. **New today:** VERIDAH's "cervical" vertebrae are not lumbar-sized (median over 40 ml, or 20 ml for a body
     mask). The lumbar floor is not used when a ctd exists, because it would refuse children (TS v3).
  6. **New today:** the ctd does not **skip a mandatory name at a normal spacing** (`veridah_skipped_name`; VERIDAH's
     T12 skip). Every time a reader could check one, the names on one side were one level off. In the 53 CTSP
     benchmark cases it was the thoracic names (section 4); in TS_s1178 it was the lumbar names. A reader whose
     every name is gated by another labeller may pass `allow_skipped_names=True`; only `dual_seg_compare.py` does,
     because its names need TotalSegmentator's agreement. `check_ids` reports the skip
     (`veridah_skipped_names`) without changing its verdict, so the census and the relabel are unaffected.
  - With no ctd the mask is refused. A raw mask of 2-3 instances is monotonic by chance, so without a ctd its ids
    cannot be shown to be names.
- `body_source_ok(body_mask)`: a body mask is tested against the ctd of the instance mask it was cut from (found
  through `<case>_body.json`).
- `check_ids(mask, ctd)`: the same measurement without raising, for tools that record a verdict.
- `find_ctd` now follows a symlink to the ctd beside its target. This covers a COLONOG link to a CTSP mask, and a
  TSV3 link into bench_ts.
- Unit tests: `tools/test_spineps_ids.py`, 15 synthetic cases, all pass. They check that the guard raises on a
  scramble, on a raw 1..3 that happens to run top-down, and without a ctd. They check that the relabel recovers a
  scramble, names C1, takes the semantic sacrum, writes no sacrum without one, refuses two points in one
  instance, refuses an unnamed instance inside the column, and refuses a sacrum point above the column. One checks
  that the guard raises when VERIDAH names lumbar-sized bones C1..C5, and one
  that `compare_masks` does not misread a ring around a core.

### Wired into every reader that names by id

| reader | what it does now | file |
|---|---|---|
| SPINEPS harvest | **refuses a raw-only candidate**: the case fails, and nothing is copied under the seg-vert name. It records the guard's verdict in `<case>_harvest.json` (it does not raise on a VERIDAH order error, because each reader runs the guard itself) | `benchmark/run_spineps_cases.py` `harvest()`; shared by `cobra_lstv_screen`, `other_ct_screen`, `run_spineps_retry` |
| CTSP benchmark composer | a case that fails is **not composed**. It is listed, and the run exits 3 | `benchmark/spineps_to_oneshot.py` |
| Möller rib assignment (rib ids come from the vertebra name) | raises | `benchmark/run_spineps_ribs.py` `measure()` |
| body masks | refuses a source that fails, and records the verdict in `<case>_body.json` (predecessor edit, kept) | `tools/body_masks.py` |
| DRR body boxes | raises. The **affine** is now compared as well as the shape | `tools/make_drr_dataset.py` `body_mask_for()` |
| Varian overlay | raises before it writes a level on a frame | `tools/cobra_varian_geometry.py` `cmd_overlay()` |
| two-labeller levels | a failing mask gives **no names and no L6/T13 flags**, only the reason | `tools/dual_seg_compare.py` |
| COBRA export | `--levels` now defaults to `levels_v2.json`. `load_levels` **refuses** the raw v1 file two ways: byte-identical to `levels_v1_rawinstance_backup.json`, or more than half of its thoracolumbar names cervical. On the grid, `levels.json` has 823 of 858 cervical and `levels_v2.json` has 0 of 900 | `tools/realxray_cobra_export.py` |
| SpineSAC body truth | raises. Both phantom masks now fail (`veridah_order_error`, IMPACT C8) | `tools/spinesac_bind_bodies.py` |
| mask census | the TS rows read the relabelled tree, and a failing mask is recorded as `ids_not_names` with no labels | `tools/transitional_mask_census.py` |
| TS v3 linker | links only subjects whose v2 mask passes, and the refused ones are listed. `--src-dir` should now be `native_ctd` | `tools/ts_v3_link_reused.py` |
| rare-class pass 1 | runs the guard before `assert 25 in ids` | `SchwingNet/slurm/rare_class_ts_drr.sh` |
| rare-class relabel (rcts2) | its output must pass `check_ids` with zero disagreements. It **no longer writes 26** (the raw mask holds no sacrum) | `tools/rare_class_ts_fixids.py` |

Already on the shared helper before this task (other workflows): `tools/acquisition_screen.py`,
`tools/other_ct_screen.py`, `tools/ctsp_registry_census.py`. `tools/cobra_lstv_screen.py` names from the ctd on
its own (another workflow's edit at 18:36; not touched here). `tools/anomalous_inventory.py` no longer reads mask
ids (the owning workflow's edit at 18:52).

**Grid sync.** Every file above was copied to `~/spinesurg-ct-nnunet` on the grid, CRLF stripped and md5-checked.
Each grid copy was first checked to be identical to local HEAD, so no grid-only edit was lost. One exception:
the grid's `tools/make_drr_dataset.py` (09-22 12:52) is **older than HEAD** and lacks the body-mask code
altogether. It was left alone, because other workflows render with it. The guard reaches the grid when HEAD is
synced there.

## 2. The relabel: `tools/spineps_ids.py relabel`

This generalises `tools/rare_class_ts_fixids.py`. It combines two routes to each name and **refuses unless they
agree**:
- **Position:** each ctd point binds to the instance holding it, the method of `spineps_relabel_from_poi.py`.
- **Rank:** the z-rank pairing of fixids.

It also refuses when:
- the ctd is out of order, or has a sacrum point above the column;
- two points fall in one instance;
- a bound centroid lies more than 25 mm in S or 40 mm in 3-D from its point;
- an unnamed vertebra-sized instance sits inside the named column;
- the result would fail the guard with even one disagreement.

What it does at the ends of the column:
- It names C1 only when exactly one vertebra-sized instance sits more than 8 mm above the C2 point (VERIDAH's ctd
  never names C1).
- It **writes a sacrum only from the semantic mask**. A raw SPINEPS semantic mask has no class 26, so **a mask
  relabelled from a raw tree carries no sacrum**. The report says `"sacrum": "absent: ..."`.
- A T12 skipped at a normal spacing (VERIDAH's 11-thoracic call) is **reproduced and flagged**
  (`veridah_skipped_names`), because a post-fix derivative carries it the same way. `--refuse-skipped-names`
  refuses it instead. TS_s1178, where the skip is shown wrong, is refused by name.

A source that already passes the guard is linked through unchanged.

Grid job 40425591 (44 shards), 40425592 (summary), 40425964 (re-run of 4 empty sources that the first pass
recorded as a KeyError). Records: `repair/relabel_records.jsonl.gz`; per-tree summaries:
`repair/relabel_summary_*.json`.

| source tree → NEW tree | masks | relabelled | passed through | refused | VERIDAH call (ctd): L6 / T13 / both | T12 skip kept | C1 named | max \|dz\| p95 |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| `~/bench/spineps/native` → `/rs/.../data/spineps/ctd_relabel/bench_native` (+ link `~/bench/spineps/native_ctd`) | 800 | 796 | 0 | 4 | 20 / 52 / 0 | 53 | 0 | 6.8 mm |
| `~/bench_ts/spineps/native` TS → `/rs/.../ctd_relabel/bench_ts_native` (+ link `~/bench_ts/spineps/native_ctd`) | 1,144 | 1,091 | 23 | 30 | 37 / 53 / 1 | 43 | 186 | 9.9 mm |
| same tree, VerSe | 374 | 361 | 8 | 5 | 41 / 25 / 0 | 34 | 76 | 9.6 mm |
| `/rs/.../spineps/tsv3` → `/rs/.../spineps/tsv3_ctd` | 1,616 | 1,091 | 431 | 94 | 51 / 72 / 3 | 43 | 184 | 9.9 mm |
| `/rs/.../cobra2026/seg/spineps` → `/rs/.../cobra2026/seg/spineps_ctd` | 146 | 144 | 0 | 2 | 5 / 13 / 0 | 8 | 0 | 6.0 mm |
| `realxray_work/deepfluoro/spineps` → `.../spineps_ctd` | 6 | 6 | 0 | 0 | 0 / 0 / 0 | 0 | 0 | 9.0 mm |
| `realxray_work/geneva_hip/spineps` → `.../spineps_ctd` | 1 | 1 | 0 | 0 | — | 0 | 0 | 4.8 mm |

Refusals (135) are loud and have a reason each (`rederived.json#trees.*.refusal_reasons`):
- **TS v3, 94.** 51 have a ctd with fewer than 2 usable points. 17 have VERIDAH's sacrum point above the lowest
  vertebra (its own order error). 12 have a single point binding to an instance. 3 are empty. The remaining 12 reasons (a case can carry two) are order errors, binding mismatches, one unnamed instance inside the column, and s1178 by name.
- **TS v2, 30.** 11 have a single binding point, 9 have too few ctd points, 1 is empty, 1 is s1178 by name, and the
  rest are order errors and binding mismatches.
- **CTSP benchmark, 4** (COLONOG_178, 231, 347, 449). Every one is a VERIDAH L6 call. The L6 point lies in L5's
  instance, or in an instance whose centroid is 41-54 mm away in 3-D. These 4 are why the relabel
  carries 20 L6 calls where the raw run's own ctd makes 24 (`impact_counts.json`, bench: ctd L6 24).
- **COBRA, 2.** A212 has a single binding point. D134 has its L5 and L6 points in one instance.

A refused case has **no** mask in the new tree, so no reader can name it by id.

## 3. The relabel checked against names it did not compute

`tools/spineps_ids_verify.py` compares each relabelled instance with the reference's id at the instance's own
inner voxel, both ways, in world space. The grids differ. Jobs 40425594 and `repair/verify.json`, aggregated
locally from `repair/verify_rows.jsonl`.

| reference (how it got its names) | cases compared | instances: same / different / missing | reference → relabelled: same / different / missing |
|---|---:|---|---|
| **ts12**: `rare_class/ts_stage` masks, relabelled by fixids (z-rank on the CT grid) and checked 280/280 by `ts12_verify_ids.py` | 11 (s1178 refused) | **268 / 0 / 0** | 268 / 0 / 7 |
| **cobra**: `crossdev/levels/spineps_v1_relabel/*_veridah`, relabelled by `spineps_relabel_from_poi.py` (position only) | 144 | **829 / 0 / 0** | 829 / 0 / 0 |
| **ctsp**: `/rs/.../spineps/ctsp/CTSP_<id>`, a **separate post-fix SPINEPS run on the same CT**, named by VERIDAH itself (COLONOG → CTSP joined through the CT path in `benchmark/cases.csv`) | 796 | **7,223 / 15 / 14** (99.6 % same) | 7,249 / 10 / 823 |

Reading the differences:
- **ts12, 7 missing.** These are the 7 sacrum objects that fixids named 26 and the new relabel deliberately drops:
  fragments and S1 pieces.
- **ctsp, 14 of the 15 differences** sit at the lumbosacral junction: the relabelled L5 or L6 lies where the
  post-fix derivative wrote 'S'. Of these, 7 are L5 → S and 7 are L6 → S. The derivative's semantic sacrum
  swallowed a transitional instance that the raw run kept and VERIDAH's ctd named. This is VERIDAH's
  post-processing, not the id mapping.
- **ctsp, the last difference** is one top-of-field vertebra that the old run's VERIDAH called T8 and the new
  run's called T9 (COLONOG_CTC-2394053080).
- **ctsp, 823 reference-side missing.** These are almost all the post-fix sacrum, which a raw-tree relabel does not
  carry (section 2).
- **ctsp, 10 reference-side differences.** These are the post-fix masks' id 80, which is not a vertebra.

**Rendered** (render job 40426542, `tools/spineps_ids_render.py`, `repair/render/*.png`). Each render shows three
panels on the mid-sagittal CT: raw ids read as names, ctd-relabelled names, and the reader's labels.
- **COLONOG_1** (no skip): the relabel reads T9..L5 on the same bones as the CTSP v11 release labels.
- **VERSE_verse607** (VERIDAH L6): C3..L6 on the same bones as the VerSe expert mask, **L6 included**. C1 and C2
  are added above.
- **COLONOG_10 and COLONOG_117** (VERIDAH skipped T12):
  - The relabel's L1..L5 sit on the reader's L1..L5.
  - **Every thoracic name above is one level low: VERIDAH's T11 is the reader's T12, its T10 the reader's T11,
    and so on.** The skip is not an 11-thoracic spine here. It is VERIDAH mis-counting the thoracic column down
    from its top.
  - This differs from TS_s1178, where the skip shifted the lumbar names instead. A relabel carrying
    `veridah_skipped_names` therefore has at least one run of names one level off. **Treat it as unnamed above or
    below the skip, or drop it.**
- **TS_s1089** and **A053** (COBRA, VERIDAH T13) are rendered raw vs relabel, with no reader.
- In every render, the raw panel names the column in an order no spine has, for example C7, C5, C2, C3, C4, C1, C6
  down A053's lumbar spine.

## 4. Re-derived numbers

**The CTSP one-shot benchmark, SPINEPS column** (was Dice 0.000 on every class; IMPACT C4). Re-scored against the
Dataset810 reader labels, vertebrae only, with the benchmark's own scorers (`eval_oneshot.py`, `decode_sequence.py
--onehot`). Two systems were scored: the relabelled raw tree, and the post-fix run on the same CTs. Nothing under
`~/bench` was written. Jobs 40426220 (48-shard composition) and 40426277 (score), in
`/rs/.../or_ready/spineps_ids/repair/rescore/{bench_ctd,ctsp_postfix}/score/`. Local copies are in
`repair/rescore/`, and `repair/rescore_report.json` comes from `tools/spineps_ids_rescore_report.py`.

| system | cases | rib-free lumbar count exact: all / typical / transitional | mean Dice, typical: T10 / T11 / T12 / L1 / L2 / L3 / L4 / L5 | sacrum |
|---|---:|---|---|---|
| old column (raw ids read as names) | 800 | 0.0 / 0.0 / 0.0 % | 0.000 on every class | 0.000 |
| **relabelled raw tree** (`bench_ctd`) | 796 | **93.7 / 96.2 / 46.2 %** | 0.782 / 0.823 / 0.821 / 0.903 / 0.902 / 0.903 / 0.904 / 0.903 | 0.000 (none carried, by design) |
| post-fix run, same CTs (`ctsp_postfix`) | 801 | 93.5 / 96.3 / 38.5 % | — / 0.859 / 0.856 / 0.940 / 0.940 / 0.941 / 0.941 / 0.932 | 0.958 |

- **The relabelled tree scores the way an independent post-fix run of the same model scores.** The count calls agree
  to 0.2 points. Dice is about 0.04 lower on the relabelled tree because its instances are SPINEPS's raw crop-grid
  output, resampled here to the label grid, where the derivative is VERIDAH's cleaned output on the CT grid.
- The void column (0 %) becomes a real one: VERIDAH counts the lumbar spine correctly on **96 % of ordinary
  spines**, but on only **38-46 % of the 39 transitional ones**. It emits a T13 on 52 CTSP spines, and CTSP's
  readers label no T13.
- **VERIDAH's T12 skip is wrong on CTSP every time.** In the 53 benchmark cases whose ctd skips T12 (reproduced by
  the relabel and flagged):
  - the reader's T12 is scored 0 in 53 of 53;
  - T11 scores below 0.2 in 50 of 53, and T10 below 0.2 in 41 of 44;
  - the lumbar names stay right: L1 Dice 0.862 against 0.880 in the other 743, below 0.2 in 4 of 53 against 43 of
    743.
  The skip is a thoracic count off by one, not an 11-thoracic spine. The post-fix run shows the same numbers, so
  this is VERIDAH, carried faithfully by its own derivative. The renders (section 3) show it on COLONOG_10 and
  COLONOG_117. The guard now refuses such masks unless every name is gated by another labeller (section 1).

**The transitional inventory and Figure 6d arithmetic.** `rederived.json#readings` (`tools/spineps_ids_rederive.py`;
json only, run locally) holds the readings table in IMPACT C1. Its Wilson formula reproduces all 30 cells of
`power_table.json`, and the manuscript row reproduces exactly. Under the inventory on disk now (TS 3 L6 + 1 T13), the
test side is 34 and the lower bound at zero errors is 89.8 %.

**TS v2 by VERIDAH over the whole bench:** 37 L6, 53 T13 and 1 both among 1,114 readable masks. This is VERIDAH's
pseudo-truth, not a row for Table 4 (IMPACT C1).

**Body masks rebuilt from the new trees.** `tools/body_masks.py`, now guarded, job 40425593:
- `/rs/.../spineps/bodies_ctd`: TS 1,114, VerSe 369, TSV3 1,522, CTSP 801 (the CTSP sources are the post-fix
  `spineps/ctsp`), **3,806 of 3,806 accepted**. Guard verdicts: 3,765 `verse_ok`, 41 `misnamed_1_2_levels`
  (VERIDAH one-level defects in pass-through post-fix sources). `repair/bodies_ctd_log.jsonl`.
- `/rs/.../spineps/bodies_cobra_ctd`: COBRA Elekta 144 (from `seg/spineps_ctd`) + 1 Elekta case and 99 Varian (from `spineps/cobra_varian`), **244 of 244 accepted, all `verse_ok`**.
- **Re-guarded under rule 6** (job 40427279, mode `reguard`). 249 bodies moved to `<tree>/_refused/` with their
  json; nothing was deleted (`repair/reguard_moved.json`):
  - 241 whose source ctd skips T12: CTSP 54, TS 45, TSV3 106, VerSe 35, COBRA 9. The CTSP 54 are the post-fix
    `spineps/ctsp` masks, VERIDAH's own derivative.
  - 8 TSV3 bodies too small to test against their ctd.
  - Left in place: `bodies_ctd` **3,566**, `bodies_cobra_ctd` **235**, all passing the guard as it stands now.
- The old `bodies/` and `bodies_cobra/` are untouched. **Use the `_ctd` trees**: any `--body-mask-dir` pointed at
  the old ones now raises.
- **Caveat:** bodies built from a raw-tree relabel sit on SPINEPS's crop grid, not the CT grid. `make_drr_dataset`
  refuses them by shape, never by name. The G4 rebuild needs an explicit nearest-neighbour resample to the CT grid
  through the two affines, a step that is not written yet. Those bodies also carry **no sacrum** (section 2).

**Census of the new trees**, the F2 tool unchanged. Jobs 40425597 → 40425598 → 40425599 produced
`repair/census_ctd.json` and `census_ctd_rows.jsonl.gz`; the per-tree summary is `repair/census_ctd_by_tree.json`.
It covers 8,002 masks: 3,952 seg-vert and 4,050 bodies.
- **0 raw and 0 scrambled** in every new tree.
- ctd points landing in another id: **0 of 7,216** (CTSP benchmark), **5 of 13,657** (TS v2), **0 of 4,893** (VerSe),
  **28 of 18,822** (TS v3), **0 of 817** (COBRA), **0 of 17** (DeepFluoro), **0 of 5** (Geneva). In the bodies:
  1 of 7,265 (CTSP), 6 of 18,512 (TSV3), 0 of 13,630 (TS), 0 of 4,879 (VerSe), 0 of 1,227 (COBRA).
- Every residual disagreement is in a pass-through post-fix mask: an S point inside L5, or a one-level VERIDAH
  defect. None is in a relabelled mask.
- Id 26 appears only in pass-through masks (TS 11, VerSe 7, TS v3 273). A relabelled mask has none, as designed.

## 5. Not repaired, and what has to be re-run (by whom, with what, and what it moves)

| item | why not here | what to run | what it moves |
|---|---|---|---|
| Table 4, results.tex l.15-17, NUMBERS.md l.156/229, CLAIMS_LEDGER l.209, LEVELCHECK_CLAIM l.128-139 | owned by the manuscript workflow | substitute from `rederived.json#readings` (IMPACT section 4) | 198→190, 89→81, 83→74 L6, 6→7 T13, 65→60, 37→34, 90.6/86.2 %→89.8/85.1 % |
| Figure 6d + `power_table.json` | derived from the inventory, which is being edited by its owner (18:52) | `python SchwingNet/tools/fig_claim.py` once the inventory is final | the inventory marker moves under the 90 % line |
| PolyPose `sampling_spec.json` `N_rare_real_ct` 86, `L6_spineps_called` 12, `SAMPLING_SPEC.md` l.407 | owned by the PolyPose workflow | re-run its spec builder on the corrected inventory | 86 → 78 (inventory on disk) |
| rcts2 frames of TS_s1178 (84 frames, 309 lumbar boxes one level off, subtype L6); s1088 / s1123 convention (234 boxes) | owned by the rare-class workflow; the frames are VERIDAH-named, not raw | exclude s1178 (`tools/spineps_ids.py relabel` refuses it by name) or relabel it by the rib count; state the s1088 / s1123 convention | rare-class split (`split_report.json`) |
| the sacrum for every raw-tree case (CTSP bench 796, TS v2 558, VerSe 281, COBRA 144) | the raw semantic mask has no sacrum, so it cannot be recovered | take the sacrum from TotalSegmentator or the release labels; or re-run SPINEPS post-fix (`benchmark/run_spineps_cases.py`, harvest now refuses raw) | body-box banks' sacrum class (G4) |
| SpineSAC phantom sacrum truth (0.44 / 0.16 ml specks) | VERIDAH's own error; the guard now refuses the masks | rebuild the sacrum from another labeller, then re-run `spinesac_bind_bodies.py` and the SpineSAC scorer | `or_ready/spinesac/results_table.md` sacrum columns (not quoted) |
| G4 body-box rebuild | not started; needs the CT-grid resample (section 4) | point `--body-mask-dir` at `bodies_ctd` / `bodies_cobra_ctd` after the resample | every body-box bank |
| `mask_census.json` TS rows | no reader | `tools/transitional_mask_census.py` (now reads `native_ctd`) | nothing quoted |
| the 135 refused relabels | unsafe to name | re-run SPINEPS post-fix on those CTs, if they are needed | nothing quoted |
| `realxray_cobra_export.py cmd_tables` still writes `seg/spineps/<c>_seg-vert_msk.nii.gz` (raw) into `compare.csv` | behaviour change for the COBRA workflow | point it at `spineps_v2` (`_veridah`) or `spineps_ctd`. `dual_seg_compare` now refuses the raw path, so a rerun gives errors, not wrong names | nothing quoted |

## 6. Files

New: `tools/spineps_ids.py` (predecessor draft, finished here), `tools/test_spineps_ids.py`,
`tools/spineps_ids_verify.py`, `tools/spineps_ids_impact.py`, `tools/spineps_ids_rederive.py`,
`tools/spineps_ids_rescore_report.py`, `tools/spineps_ids_render.py`, `slurm/spineps_ids_repair.sh`. Edited: `benchmark/run_spineps_cases.py`, `benchmark/spineps_to_oneshot.py`,
`benchmark/run_spineps_ribs.py`, `tools/body_masks.py`, `tools/make_drr_dataset.py`, `tools/cobra_varian_geometry.py`,
`tools/dual_seg_compare.py`, `tools/realxray_cobra_export.py`, `tools/spinesac_bind_bodies.py`,
`tools/transitional_mask_census.py`, `tools/ts_v3_link_reused.py`, `tools/rare_class_ts_fixids.py`,
`SchwingNet/slurm/rare_class_ts_drr.sh`. Results here: `IMPACT.md`, `REPAIRS.md`, `rederived.json`,
`impact_counts.json`, `repair/`.

Re-run everything: `slurm/spineps_ids_repair.sh`. Its header lists the sbatch chain: smoke, relabel (0-43),
summary, fixup, bodies (0-23), verify (0-7), verify_agg, rescore_prep (0-47), rescore_eval (0-1), census_find,
census (0-23), census_agg, render, reguard (0-15). Local readers of the results, json and csv only:
`tools/spineps_ids_rederive.py`, `tools/spineps_ids_rescore_report.py`, `tools/spineps_ids_impact.py`. A mode skips work already done unless `--force` is passed to the relabel.
