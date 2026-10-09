# SPINEPS id census: every vertebra-mask tree on the grid

2026-09-23, task F2. Tool `tools/spineps_id_census.py`, driver `slurm/spineps_id_census.sh`. Grid jobs: find 40424772,
which listed 17,172 files (10,685 masks) in 25 trees; census 40424914 (48 tasks) and aggregate 40424915; id-component
diagnostics 40424893 (id 26) and 40424894 (id 25). The first pass, 40424774 and 40424775, used an earlier rule; see "Rule
changes" at the end. Grid outputs are in `/rs/rs_grp_oschome/go2432/data/or_ready/spineps_ids/`, local copies are here:
`census.json`, `census_rows.jsonl.gz` (one row per mask), `files.tsv` (the find list), `components_id2{5,6}.json`. This
file comes from `CENSUS_reading.md` (hand-written) and the tables below it, which are generated. To regenerate:
`python tools/spineps_id_census.py report --census census.json --preamble CENSUS_reading.md --out-md CENSUS.md`.

**Scope.** `find` searched every top-level entry of `$HOME` (except `mambaforge`, `.cache`, `.conda`, `.local`, `.nv`
and `.triton`) and of `/rs/rs_grp_oschome/go2432`, for `*seg-vert*`, `*ctd*.json`, `*body_msk*` and `*_poi*.json`.
Some locations named in the task hold no mask: `spineps/ts_diagnose` has only json, and `carmlspine/nifti` has only
CBCT volumes. One set of masks falls outside the pattern: the 12 relabelled copies
`rare_class/ts_stage/TS_*/TS_*_msk.nii.gz`, written by `tools/rare_class_ts_fixids.py`. `TS12_VERIFY.md` checked them
(280 of 280 vertebra points agree).

## Summary

**Whether a SPINEPS mask's ids are VerSe names depends on how it was harvested, not on which tree it sits in.** The
count below is of distinct files (symlinks resolved; `tmp/` and the 10 VerSe expert masks excluded). There are 4,751
SPINEPS seg-vert files:

| harvest | files | ids are VERIDAH's names | ids are a raw enumeration |
|---|---:|---|---|
| with a `_harvest.json` (the fixed `_rank` in `benchmark/run_spineps_cases.py`, commit 147428d, written 2026-09-21 18:28 onward) | 2,314 | 2,206 ctd-confirmed. The other 108: 50 VerSe-named with no usable ctd test, 42 that differ from their ctd at 1-2 levels, 10 VERIDAH order errors, 2 where VERIDAH put 'S' on a cervical or thoracic body, 2 empty, and 2 whose only id is 80 | **0** |
| without a harvest record (the old "last file whose name holds seg-vert" rule, runs of 2026-09-09 to 2026-09-21 18:04) | 2,437 | 0 | **2,437**: every one has ids exactly {1..N}. 2,421 are confirmed by the ctd test. The remaining 16 hold 1-3 instances, too few for the test to decide. |

A raw id read as a VerSe id produces a plausible name that is wrong, and nothing checks it. Some examples:
`TS_s0224` ids 1..25 run top to bottom as L5, L3, C5, C2, C1, C7, T6… VERIDAH's own ctd for that CT lands in the instance
of the same name for 1 of 24 centroids. The COBRA Elekta mask `A002` holds ids 1..5, which read as C1..C5, while its ctd
says L3, L4, L5, S. The median volume of those "cervical" instances is 49.5 ml, which is lumbar-sized.

**The ctd files were never the problem.** 4,749 of the 4,751 masks have one. In 4,723 of them VERIDAH's names are in S
order. In the 26 exceptions VERIDAH named the column itself out of order: 17 TotalSegmentator v3 (TS v3) fields, 7
masks in `bench_ts` (5 TS v2, 2 VerSe) and the 2 SpineSAC phantoms (inverted by more than 5 mm). Most put 'S' above a lumbar or thoracic name, or invert
two neighbours near the cervicothoracic junction (TS_s0396 C7/T1 by 18 mm).

## Per tree

| tree | what it is | raw / scrambled | VerSe-named, ctd-confirmed |
|---|---|---|---|
| `~/bench/spineps/native` | CTSpinoPelvic1K (CTSP) competitor benchmark, 2026-09-09/10 | **800 / 800** | 0 |
| `~/bench_ts/spineps/native` | TS v2 (1,144) + VerSe (374), 2026-09-19 | **1,468 raw of the 1,484 with no record** | 31 of the 34 re-run on 2026-09-23 |
| `/rs/.../spineps/tsv3` | TS v3 | **all 1,116 symlinks into bench_ts** (made by `tools/ts_v3_link_reused.py`). 1,100 are confirmed raw; the other 16 hold 1-3 instances. | 416 of the 500 fresh runs, 0 raw |
| `/rs/.../spineps/ctsp` | CTSP, post-fix | 0 | 791 of 801 (10 differ at one level) |
| `/rs/.../cobra2026/seg/spineps` | COBRA Elekta v1 | **146 / 141** | 0 |
| `/rs/.../or_ready/crossdev/levels/spineps_v1_relabel` | symlinks to the above, plus `_veridah` relabels | the 146 plain masks are raw | 144 of the 145 `_veridah` |
| `/rs/.../cobra2026/seg/spineps_v2`, `/rs/.../cobra2026/lstv/seg`, `/rs/.../spineps/cobra_varian` | COBRA, post-fix | 0 | 288/290, 575/580, 101/101 |
| `/rs/.../carmlspine/spineps` (+ `spineps_retry134`) | C-ArmLSpine, post-fix | 0 | 296/297 (case134 is VERIDAH's own C1-C5 + S) |
| `realxray_work/deepfluoro`, `geneva_hip` | pre-fix, then POI relabel | the plain masks are raw (6 + 1) | every `_veridah` mask |
| `~/VerSeFusion/.../derivatives` | VerSe **expert** masks (not SPINEPS), the positive control | 0 | all 10 S-ordered and VerSe-coded; their legacy ctd has no world origin, so it cannot be tested |

## Body masks

**Each body takes its source instance id verbatim.** `tools/body_masks.py` keeps the instance id wherever the semantic
mask is 49 or 50. It uses no ctd and no position matching. Every body id is a subset of its source's ids (0
exceptions). The `_body.json` records the source path but not the naming. Bodies whose source mask is raw:

| body tree | source | bodies | from a raw source |
|---|---|---:|---:|
| `spineps/bodies` | CTSP (`spineps/ctsp`) | 801 | **0** |
|  | TS v2 (`bench_ts`) | 1,144 | **1,102** |
|  | TS v3 (`tsv3`, 1,116 via links into bench_ts) | 1,616 | **1,100** |
|  | VerSe (`bench_ts`) | 374 | **366** |
| `spineps/bodies_cobra` | Elekta (`cobra2026/seg/spineps`, A004 from `cobra_varian`) | 147 | **146** |
|  | Varian F, G (`cobra_varian`) | 99 | 0 |

That makes 2,714 body masks carrying raw instance ids. The only body naming that holds up against this is the one in
`bodybox_rescore`. It bridges each TotalSegmentator (TS) vertebra to a SPINEPS body **by world-space overlap**
(`bodybox_rescore/grid/truth_build.json`: A053 L5 → instance 6, L4 → instance 1), so the COBRA body truth there is
unaffected. `make_drr_dataset.body_boxes` bridges **by name**. If a TS or VerSe case is rendered with `--body-mask-dir
.../bodies` (the G4 corpus rebuild), its "L3" body box goes to whichever instance got id 22.

## Defects that remain after a correct harvest (checked against sources outside VERIDAH where one exists)

1. **L6 (id 25) is often a sliver.** In post-fix masks, id 25 holds under 5 ml in 10 of the 24 CTSP masks that carry
   it, 14 of 44 in COBRA `lstv/seg`, 18 of 25 in the fresh TS v3 runs, 3 of 6 in COBRA v2 and 1 of 7 in Varian. The ctd's L6 centroid then lies in the sacrum or L5 instance
   (`components_id25.json`: CTSP_1009's L6 is 4.6 ml between L5 and the sacrum; CTSP_0133's is 0.02 ml in 5 pieces).
   **Outside check** against the CTSP release (`benchmark/cases.csv` `has_l6`, 18 release L6 among 801 matched):
   - SPINEPS id 25 appears in 10 of the 18. It is vertebra-sized (20 ml or more) in 6.
   - It also appears in 14 of the 783 release non-L6 (7 slivers, 7 vertebra-sized).
   - "id 25 present" therefore has a positive predictive value (PPV) of 10/24 = 42 % and a sensitivity of 10/18. With
     a 20 ml floor they are 6/13 = 46 % and 6/18.

   **Even with correct ids, a VERIDAH L6 call is weak pseudo-truth.** Across all 2,314 post-fix masks, the ctd
   names an L6 exactly when the mask holds id 25 (113 masks) and a T13 exactly when it holds id 28 (139), so the ctd is
   no better. This bears on `ts12_ctd_subtypes.json` and on any
   L6 count taken from a ctd.
2. **Id 26 turns up in two places.** Id 26 has a detached component in 46 of 801 CTSP masks, 31 of 500 fresh TS v3
   runs, 16 of 580 COBRA `lstv/seg`, 5 of 146 COBRA v2, 9 of 149 C-ArmLSpine and 2 of 101 Varian masks (all post-fix).
   The detached component measures 0.2-4.6 ml and sits a median 170-270 mm above
   the sacrum, usually at the topmost, field-of-view (FOV)-cut vertebra (`components_id26.json`: CTSP_0795 carries a
   1.2 ml piece of the cut T10; TSV3_s1574 a 3.4 ml piece of T9). Any extent or box drawn around id 26 then spans the
   whole column, and the ctd centroid of the cut vertebra lands in id 26. The body masks carry no id 26, and the
   C-ArmLSpine sacrum box comes from TotalSegmentator, so neither is affected.
3. **Id 80.** 590 otherwise VerSe-named masks carry id 80, which is outside the alphabet. The median is 14 voxels, and
   30 masks hold 5 ml or more. Two masks, TS_s1148 and TSV3_s1148, hold only id 80. TPTBox's *Location* enum has `Metal = 80`, but this census did not establish that id
   80 means that in an instance mask. It is reported, and kept out of the naming tests.
4. **VERIDAH naming errors** (`veridah_order_error`): 10 post-fix masks, all TS v3 paediatric or neck fields plus the
   phantoms. The mask copies the ctd faithfully, and the ctd names 'S' above L5 or on a cervical body.

## Counts by VERIDAH ctd versus by mask id (what the anomalous inventory should have read)

| source | subjects | ctd names L6 | ctd names T13 | mask id 25 present |
|---|---:|---:|---:|---:|
| TS v2 (`bench_ts`, TS_*) | 1,144 | 41 | 56 (1 has both) | 13 (a raw enumeration of 25 or more instances, plus s0109) |
| VerSe (`bench_ts`, VERSE_*) | 374 | 42 | 26 | 6 |
| TS v3 (`tsv3`) | 1,616 | 65 | 83 (7 both) | 37 |
| CTSP (`ctsp`) | 801 | 24 | 52 | 24 |

These are VERIDAH counts. By item 1 above, their L6 column has a PPV near 42 % on CTSP, the one dataset checked here against a release read. VerSe's expert masks would give a second check; they were not read.

## What must change (named, not edited; these belong to other workflows)

- `SchwingNet/results/anomalous_inventory.{json,md}`, TS row `12 | 12 | 0`. This comes from
  `tools/anomalous_inventory.py` l.84-94 (`L6 in ids` on raw masks).
- `SchwingNet/tables/tab4_transitional.tex`:
  - "L6, mobile … 83 (18 / 50 / **12** / 3)"
  - "T13 … 6 (0 / 6 / **0** / 0)"
  - "Any transitional subtype … 198 (48 / 135 / **12** / 3)"
  - footnote c, "The count-changing subtypes (L6 and T13) total **89** persons; **65** of them…"
  - the "37 projected" test persons that rest on it

  The TS column is id-25 presence on raw masks.
- `SchwingNet/results/rare_class/transitional_subtypes.csv` (all 12 listed as L6).
- `~/bench/spineps/score/{report.txt,summary.json,per_case.csv,decode.csv}` (2026-09-10). The SPINEPS+VERIDAH row of
  the CTSP competitor benchmark reads Dice 0.000 on every class, with a count error of −5 in 769 of 800 cases. That
  was computed on raw ids and is void. No document found in this repo quotes it.
- `spineps/bodies` (2,568 TS/TSV3/VerSe bodies) and `spineps/bodies_cobra` (146 Elekta) must be rebuilt from relabelled
  instance masks before any `--body-mask-dir` render reads them.
- `tools/ts_v3_link_reused.py` linked 1,116 raw masks into `tsv3`.
- `tools/cobra_lstv_screen.py` calls L6 on id 25 with at least 150 voxels. 14 of the 44 L6 masks in `cobra2026/lstv/seg`
  hold under 5 ml.
- `CONSUMERS.md` (task F3, in this directory) quotes first-pass verdict counts. Under the current rule:

  | tree | CONSUMERS.md says | current rule |
  |---|---|---|
  | ctsp | "686 verse_ok, 105 ctd-concordant non-monotonic" | 791 verse_ok, 10 one-level |
  | cobra lstv | "392 verse_ok, 182 ctd-concordant, 1 scrambled (D034, stray id 80)" | 575 verse_ok, 5 one-level, 0 scrambled |
  | cobra_varian | "74 verse_ok, 27 ctd-concordant" | 101 verse_ok |
  | tsv3 | "259 verse_ok" | 416 |
  | bench_ts | "1,434 scrambled; 26 verse_ok" | 1,433 scrambled, 32 ordered-not-names, 31 verse_ok |

  Its "raw" counts are unchanged in substance.

## Re-running

The repair itself is outside F2. One route relabels by ctd (`tools/spineps_relabel_from_poi.py` or
`tools/rare_class_ts_fixids.py`). The other re-runs through the fixed harvest. Either way, once the repair lands, re-run
this census:

`sbatch -D /rs/rs_grp_oschome/go2432/tmp --export=ALL,ROWS=rows3 --array=0-47 slurm/spineps_id_census.sh census`, then
`aggregate` with the same `ROWS`. Re-run `find` first if new trees were written.

It will change this file's tables and `census.json`. The harvest dichotomy above is the claim to re-test: it holds if
the "with record" row still shows 0 raw.

## Not known

- What id 80 is.
- Whether VERIDAH's T13 calls agree with any reader. The CTSP case table has no T13 flag, and the release labels were
  not read here.
- Why VERIDAH's order errors in TS v3 (17 ctd files out of S order, 8 masks classed `veridah_order_error`) cluster in
  what look like paediatric fields. A small lumbar volume (L1 8-14 ml) is the only signal looked at; age was not read.

## Rule changes (so older quotes can be traced)

- First pass (jobs 40424774/5) counted id 80 as a vertebra outside the VerSe alphabet. That sent 530 masks with correct
  VerSe names and ctd confirmation into a "ctd-concordant non-monotonic" bin (CTSP 105, COBRA lstv 182, …).
- The current rule sets id 80 aside. It separates a raw enumeration (at least 30 % of ctd centroids in another id; the
  observed rate is chance level, e.g. 22 of 23) from a VerSe-named mask that differs at 1-2 levels, and adds the
  detached-fragment count.
- `aggregate` re-derives every verdict from the stored rows, so it needs no mask re-read.
