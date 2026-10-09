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

## Per-tree counts (generated 2026-09-23 18:36 by `tools/spineps_id_census.py`; 10685 masks, 6487 ctd files found)

Columns: **n** masks; **VerSe-mono** = ids all in the VerSe alphabet, cranio-caudal as VerSe names, no ctd centroid in another id; **ctd-ok** = of those, confirmed by >= 2 ctd centroids (verdict verse_ok); **scrambled** = ids are not VERIDAH's names (>= 30 % of ctd centroids in another id, not S-ordered; + scrambled_no_ctd); **ordered-not-names** = >= 30 % disagreement but S-ordered; **VERIDAH order** = the mask copies the ctd and the ctd's own names are out of S order; **1-2 lvl** = VerSe-named, S-ordered, ctd differs at 1-2 levels; **raw** = ids exactly 1..N and contradicted by the ctd (or size); **ctd** = masks with a ctd file (ctd names S-ordered / tested against the mask); **pre-fix** = seg-vert masks with no harvest record written before commit 147428d (2026-09-21 18:20); **harvest** = masks with a harvest record (of which the record says a raw file was chosen).

| tree | kind | n | VerSe-mono | ctd-ok | scrambled | ordered-not-names | VERIDAH order | 1-2 lvl | raw | ctd (mono/tested) | pre-fix | harvest (raw) | links | mtime |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `/rs/.../data/spineps/bodies` | body:3935 | 3935 | 1317 | 1254 | 2489 | 73 | 3 | 16 | 2458 | 3926 (3897/3835) | 0 | 0 (0) | 0 | 2026-09-23..2026-09-23 |
| `/rs/.../data/spineps/tsv3` | seg-vert:1616 | 1616 | 467 | 416 | 1066 | 33 | 8 | 24 | 1100 | 1614 (1592/1547) | 1116 | 500 (0) | 1116 | 2026-09-19..2026-09-23 |
| `~/bench_ts/spineps/native` | seg-vert:1518 | 1518 | 37 | 31 | 1433 | 32 | 0 | 1 | 1468 | 1518 (1511/1497) | 1484 | 34 (0) | 0 | 2026-09-19..2026-09-23 |
| `/rs/.../data/spineps/ctsp` | seg-vert:801 | 801 | 791 | 791 | 0 | 0 | 0 | 10 | 0 | 801 (801/801) | 0 | 801 (0) | 0 | 2026-09-23..2026-09-23 |
| `~/bench/spineps/native` | seg-vert:800 | 800 | 0 | 0 | 800 | 0 | 0 | 0 | 800 | 800 (800/800) | 800 | 0 (0) | 0 | 2026-09-09..2026-09-10 |
| `/rs/.../data/cobra2026/lstv/seg` | seg-vert:580 | 580 | 575 | 575 | 0 | 0 | 0 | 5 | 0 | 580 (580/580) | 0 | 580 (0) | 0 | 2026-09-23..2026-09-23 |
| `/rs/.../data/carmlspine/spineps` | seg-vert:149,seg-vert-veridah:148 | 297 | 296 | 296 | 0 | 0 | 0 | 1 | 0 | 297 (297/297) | 0 | 297 (0) | 0 | 2026-09-21..2026-09-21 |
| `/rs/.../data/or_ready/crossdev/levels/spineps_v1_relabel` | seg-vert:146,seg-vert-veridah:145 | 291 | 145 | 144 | 141 | 4 | 0 | 0 | 146 | 291 (291/289) | 146 | 0 (0) | 146 | 2026-09-21..2026-09-22 |
| `/rs/.../data/cobra2026/seg/spineps_v2` | seg-vert:146,seg-vert-veridah:144 | 290 | 288 | 288 | 0 | 0 | 0 | 2 | 0 | 290 (290/290) | 0 | 290 (0) | 0 | 2026-09-22..2026-09-22 |
| `/rs/.../data/spineps/bodies_cobra` | body:246 | 246 | 100 | 100 | 141 | 4 | 0 | 0 | 137 | 246 (246/245) | 0 | 0 (0) | 0 | 2026-09-23..2026-09-23 |
| `/rs/.../data/cobra2026/seg/spineps` | seg-vert:146 | 146 | 0 | 0 | 141 | 4 | 0 | 0 | 146 | 146 (146/145) | 146 | 0 (0) | 0 | 2026-09-21..2026-09-21 |
| `/rs/.../data/spineps/cobra_varian` | seg-vert:101 | 101 | 101 | 101 | 0 | 0 | 0 | 0 | 0 | 101 (101/101) | 0 | 101 (0) | 0 | 2026-09-23..2026-09-23 |
| `/rs/.../tmp/bodyspot_40416661/in` | seg-vert:13 | 13 | 7 | 0 | 5 | 0 | 0 | 0 | 2 | 0 (0/0) | 5 | 0 (0) | 13 | 2026-09-19..2026-09-23 |
| `/rs/.../tmp/bodyspot_40416661/out` | body:13 | 13 | 7 | 0 | 5 | 0 | 0 | 0 | 2 | 0 (0/0) | 0 | 0 (0) | 0 | 2026-09-23..2026-09-23 |
| `/rs/.../data/realxray_work/deepfluoro/spineps` | seg-vert:6,seg-vert-veridah:6 | 12 | 6 | 6 | 5 | 1 | 0 | 0 | 6 | 12 (12/12) | 6 | 0 (0) | 0 | 2026-09-21..2026-09-21 |
| `/rs/.../tmp/isoctrl_40416665/iso` | seg-vert:6 | 6 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 6 (6/6) | 0 | 6 (0) | 0 | 2026-09-23..2026-09-23 |
| `/rs/.../tmp/isoctrl_40416665/native` | seg-vert:5 | 5 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 5 (5/5) | 0 | 5 (0) | 0 | 2026-09-23..2026-09-23 |
| `/rs/.../data/realxray_work/geneva_hip/spineps` | seg-vert:1,seg-vert-veridah:1 | 2 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 2 (2/2) | 1 | 0 (0) | 0 | 2026-09-21..2026-09-21 |
| `/rs/.../data/spineps/spinesac` | seg-vert:2 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 2 (0/2) | 0 | 2 (0) | 0 | 2026-09-23..2026-09-23 |
| `~/VerSeFusion/data/raw/verse19/dataset-verse19training/derivatives` | seg-vert:2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0/0) | 2 | 0 (0) | 0 | 2026-05-12..2026-05-12 |
| `~/VerSeFusion/data/raw/verse19/dataset-verse19validation/derivatives` | seg-vert:2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0/0) | 2 | 0 (0) | 0 | 2026-05-12..2026-05-12 |
| `~/VerSeFusion/data/raw/verse20/01_training/derivatives` | seg-vert:2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 (2/0) | 2 | 0 (0) | 0 | 2026-05-12..2026-05-12 |
| `~/VerSeFusion/data/raw/verse20/02_validation/derivatives` | seg-vert:2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 (2/0) | 2 | 0 (0) | 0 | 2026-05-12..2026-05-12 |
| `~/VerSeFusion/data/raw/verse20/03_test/derivatives` | seg-vert:2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 (2/0) | 2 | 0 (0) | 0 | 2026-05-12..2026-05-12 |
| `/rs/.../data/carmlspine/spineps_retry134` | seg-vert:1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 (1/1) | 0 | 1 (0) | 0 | 2026-09-23..2026-09-23 |

## Defects that survive a correct harvest (counted in every tree)

**id25 <5 ml** = an L6 id holding under 5 ml (a sliver, not a vertebra); **id25/id28 >=20 ml** = an L6 / T13 id holding a vertebra-sized instance; **frag** = masks in which some id also occupies a detached component >= 0.2 ml more than 30 mm (in S) from its main one (of which id 26); **id 80** = masks carrying the non-VerSe id 80 (of which >= 5 ml). These read on raw trees too, where the id is an instance number and the column says nothing about L6.

| tree | n | id25 <5 ml | id25 >=20 ml | id28 >=20 ml | frag (id 26) | id 80 (>=5 ml) |
|---|---|---|---|---|---|---|
| `/rs/.../data/spineps/bodies` | 3935 | 32 | 15 | 56 | 6 (0) | 0 (0) |
| `/rs/.../data/spineps/tsv3` | 1616 | 21 | 7 | 13 | 56 (31) | 203 (20) |
| `~/bench_ts/spineps/native` | 1518 | 4 | 5 | 1 | 3 (3) | 7 (0) |
| `/rs/.../data/spineps/ctsp` | 801 | 10 | 13 | 52 | 46 (46) | 106 (1) |
| `~/bench/spineps/native` | 800 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `/rs/.../data/cobra2026/lstv/seg` | 580 | 14 | 30 | 41 | 19 (16) | 184 (6) |
| `/rs/.../data/carmlspine/spineps` | 297 | 0 | 6 | 0 | 18 (18) | 11 (0) |
| `/rs/.../data/or_ready/crossdev/levels/spineps_v1_relabel` | 291 | 1 | 4 | 13 | 0 (0) | 0 (0) |
| `/rs/.../data/cobra2026/seg/spineps_v2` | 290 | 5 | 6 | 26 | 10 (10) | 45 (0) |
| `/rs/.../data/spineps/bodies_cobra` | 246 | 1 | 6 | 3 | 0 (0) | 0 (0) |
| `/rs/.../data/cobra2026/seg/spineps` | 146 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `/rs/.../data/spineps/cobra_varian` | 101 | 1 | 6 | 4 | 3 (2) | 27 (3) |
| `/rs/.../tmp/bodyspot_40416661/in` | 13 | 1 | 0 | 1 | 0 (0) | 1 (0) |
| `/rs/.../tmp/bodyspot_40416661/out` | 13 | 1 | 0 | 1 | 0 (0) | 0 (0) |
| `/rs/.../data/realxray_work/deepfluoro/spineps` | 12 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `/rs/.../tmp/isoctrl_40416665/iso` | 6 | 0 | 0 | 0 | 0 (0) | 1 (0) |
| `/rs/.../tmp/isoctrl_40416665/native` | 5 | 0 | 0 | 0 | 0 (0) | 2 (0) |
| `/rs/.../data/realxray_work/geneva_hip/spineps` | 2 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `/rs/.../data/spineps/spinesac` | 2 | 0 | 0 | 0 | 0 (0) | 2 (0) |
| `~/VerSeFusion/data/raw/verse19/dataset-verse19training/derivatives` | 2 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `~/VerSeFusion/data/raw/verse19/dataset-verse19validation/derivatives` | 2 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `~/VerSeFusion/data/raw/verse20/01_training/derivatives` | 2 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `~/VerSeFusion/data/raw/verse20/02_validation/derivatives` | 2 | 0 | 0 | 0 | 0 (0) | 0 (0) |
| `~/VerSeFusion/data/raw/verse20/03_test/derivatives` | 2 | 0 | 2 | 0 | 0 (0) | 0 (0) |
| `/rs/.../data/carmlspine/spineps_retry134` | 1 | 0 | 0 | 0 | 1 (1) | 1 (0) |

## Body-mask trees: where each body's ids came from

**`/rs/.../data/spineps/bodies`** (3935 bodies). Naming: inherits the SOURCE instance id verbatim (tools/body_masks.py: instance id where the semantic mask is 49/50); no ctd, no position match.

| source instance tree | bodies |
|---|---|
| `/rs/.../data/spineps/tsv3` | 1616 |
| `~/bench_ts/spineps/native` | 1518 |
| `/rs/.../data/spineps/ctsp` | 801 |

Verdict of the source instance mask behind each body: scrambled 2499, verse_ok 1238, verse_monotonic_no_ctd 86, ordered_but_not_names 65, misnamed_1_2_levels 35, veridah_order_error 8, empty 2, non_verse_ids 2. Bodies with no source record: 0; bodies whose ids are not a subset of their source's: 0.

**`/rs/.../data/spineps/bodies_cobra`** (246 bodies). Naming: inherits the SOURCE instance id verbatim (tools/body_masks.py: instance id where the semantic mask is 49/50); no ctd, no position match.

| source instance tree | bodies |
|---|---|
| `/rs/.../data/cobra2026/seg/spineps` | 146 |
| `/rs/.../data/spineps/cobra_varian` | 100 |

Verdict of the source instance mask behind each body: scrambled 141, verse_ok 100, ordered_but_not_names 4, verse_monotonic_no_ctd 1. Bodies with no source record: 0; bodies whose ids are not a subset of their source's: 0.

**`/rs/.../tmp/bodyspot_40416661/out`** (13 bodies). Naming: inherits the SOURCE instance id verbatim (tools/body_masks.py: instance id where the semantic mask is 49/50); no ctd, no position match.

| source instance tree | bodies |
|---|---|
| `/rs/.../tmp/bodyspot_40416661/in` | 13 |

Verdict of the source instance mask behind each body: verse_monotonic_no_ctd 7, scrambled_no_ctd 5, non_verse_ids 1. Bodies with no source record: 0; bodies whose ids are not a subset of their source's: 0.

## Three example offenders per tree

- `/rs/.../data/spineps/bodies`:
  - **VERSE_verse607** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]; top-to-bottom as VerSe names ['L4', 'T9', 'T3', 'T2', 'T6', 'T7', 'T8', 'T12', 'L2', 'T10', 'C7', 'C6', 'C5', 'C4', 'C3', 'C2', 'C1', 'T4', 'T5', 'L3', 'L1', 'T11', 'T1', 'L5']; ctd top-to-bottom ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd agree/disagree 0/24 (ctd C2 lands in id 23, ctd C3 lands in id 16, ctd C4 lands in id 10, ctd C5 lands in id 9); inverted adjacent: C2 sits 28.4 mm above C1; C3 sits 26.3 mm above C2; C4 sits 23.9 mm above C3; median ml named cervical 16.1, lumbar 35.1; body source `/wsu/home/go/go24/go2432/bench_ts/spineps/native/VERSE_verse607_seg-vert_msk.nii.gz`
  - **TSV3_s1194** ordered_but_not_names RAW: ids [1, 2, 3]; top-to-bottom as VerSe names ['C1', 'C2', 'C3']; ctd top-to-bottom ['C2', 'C3', 'C4']; ctd agree/disagree 0/3 (ctd C2 lands in id 1, ctd C3 lands in id 2, ctd C4 lands in id 3); median ml named cervical 3.5, lumbar None; body source `/rs/rs_grp_oschome/go2432/data/spineps/tsv3/TSV3_s1194_seg-vert_msk.nii.gz`
  - **TSV3_s0947** verse_monotonic_no_ctd RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L5', 'S']; ctd agree/disagree 0/1 (ctd L5 lands in id 2); median ml named cervical 20.9, lumbar None; body source `/rs/rs_grp_oschome/go2432/data/spineps/tsv3/TSV3_s0947_seg-vert_msk.nii.gz`
- `/rs/.../data/spineps/tsv3`:
  - **TSV3_s1321** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]; top-to-bottom as VerSe names ['L5', 'L4', 'L2', 'L1', 'T12', 'T10', 'T8', 'T7', 'T6', 'T11', 'T9', 'T4', 'C1', 'C6', 'C3', 'C5', 'T3', 'C7', 'C2', 'T2', 'T5', 'T1', 'C4', 'L3']; ctd top-to-bottom ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/23 (ctd C2 lands in id 23, ctd C3 lands in id 21, ctd C4 lands in id 20, ctd C5 lands in id 19); inverted adjacent: C3 sits 114.2 mm above C2; C5 sits 227.5 mm above C4; C6 sits 52.4 mm above C5; median ml named cervical 37.6, lumbar 16.5
  - **TSV3_s0741** ordered_but_not_names RAW: ids [1, 2, 3]; top-to-bottom as VerSe names ['C1', 'C2', 'C3']; ctd top-to-bottom ['L5', 'L6', 'S']; ctd agree/disagree 0/3 (ctd L5 lands in id 1, ctd L6 lands in id 2, ctd S lands in id 3); median ml named cervical 33.4, lumbar None
  - **TSV3_s1246** verse_monotonic_no_ctd RAW: ids [1, 2, 3]; top-to-bottom as VerSe names ['C1', 'C2', 'C3']; ctd top-to-bottom ['L5', 'S']; ctd agree/disagree 0/1 (ctd L5 lands in id 1); median ml named cervical 58.7, lumbar None
- `~/bench_ts/spineps/native`:
  - **VERSE_verse607** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]; top-to-bottom as VerSe names ['L6', 'L4', 'T9', 'T3', 'T2', 'T6', 'T7', 'T8', 'T12', 'L2', 'T10', 'C7', 'C6', 'C5', 'C4', 'C3', 'C2', 'C1', 'T4', 'T5', 'L3', 'L1', 'T11', 'T1', 'L5']; ctd top-to-bottom ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd agree/disagree 0/24 (ctd C2 lands in id 23, ctd C3 lands in id 16, ctd C4 lands in id 10, ctd C5 lands in id 9); inverted adjacent: C2 sits 27.8 mm above C1; C3 sits 26.8 mm above C2; C4 sits 25.5 mm above C3; median ml named cervical 28.9, lumbar 39.3
  - **TS_s0741** ordered_but_not_names RAW: ids [1, 2, 3]; top-to-bottom as VerSe names ['C1', 'C2', 'C3']; ctd top-to-bottom ['L5', 'L6', 'S']; ctd agree/disagree 0/3 (ctd L5 lands in id 1, ctd L6 lands in id 2, ctd S lands in id 3); median ml named cervical 33.4, lumbar None
  - **TS_s0506** verse_monotonic_no_ctd RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L5', 'S']; ctd agree/disagree 0/1 (ctd L5 lands in id 2); median ml named cervical 50.6, lumbar None
- `/rs/.../data/spineps/ctsp`:
  - **CTSP_0795** misnamed_1_2_levels: ids [17, 18, 19, 20, 21, 22, 23, 24, 26]; top-to-bottom as VerSe names ['T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd top-to-bottom ['T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 8/1 (ctd T10 lands in id 26); median ml named cervical None, lumbar 80.8
  - **CTSP_1009** misnamed_1_2_levels: ids [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]; top-to-bottom as VerSe names ['T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd top-to-bottom ['T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd agree/disagree 10/1 (ctd L6 lands in id 26); median ml named cervical None, lumbar 69.1
  - **CTSP_0097** misnamed_1_2_levels: ids [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]; top-to-bottom as VerSe names ['T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd top-to-bottom ['T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd agree/disagree 10/1 (ctd L6 lands in id 26); median ml named cervical None, lumbar 53.9
- `~/bench/spineps/native`:
  - **COLONOG_93** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]; top-to-bottom as VerSe names ['T6', 'T4', 'C5', 'C4', 'C1', 'C2', 'C3', 'C6', 'T3', 'T2', 'T1', 'C7', 'T5']; ctd top-to-bottom ['T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/13 (ctd T5 lands in id 13, ctd T6 lands in id 11, ctd T7 lands in id 5, ctd T8 lands in id 4); inverted adjacent: C4 sits 82.2 mm above C3; C5 sits 26.0 mm above C4; T1 sits 35.0 mm above C7; median ml named cervical 43.3, lumbar None
  - **COLONOG_117** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]; top-to-bottom as VerSe names ['T6', 'T2', 'C6', 'C4', 'C3', 'C2', 'C1', 'C5', 'T1', 'T3', 'T4', 'C7', 'T5', 'T7']; ctd top-to-bottom ['T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/13 (ctd T4 lands in id 13, ctd T5 lands in id 9, ctd T6 lands in id 6, ctd T7 lands in id 4); inverted adjacent: C2 sits 27.7 mm above C1; C3 sits 26.4 mm above C2; C4 sits 25.7 mm above C3; median ml named cervical 41.7, lumbar None
  - **COLONOG_127** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]; top-to-bottom as VerSe names ['T6', 'T4', 'C5', 'C1', 'C3', 'C2', 'C4', 'C7', 'T1', 'T3', 'T2', 'C6', 'T5']; ctd top-to-bottom ['T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/13 (ctd T5 lands in id 13, ctd T6 lands in id 11, ctd T7 lands in id 5, ctd T8 lands in id 1); inverted adjacent: C3 sits 25.6 mm above C2; C5 sits 102.6 mm above C4; C7 sits 139.3 mm above C6; median ml named cervical 45.5, lumbar None
- `/rs/.../data/cobra2026/lstv/seg`:
  - **A297** misnamed_1_2_levels: ids [20, 21, 22, 23, 24, 25, 26]; top-to-bottom as VerSe names ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd top-to-bottom ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd agree/disagree 6/1 (ctd L6 lands in id 26); median ml named cervical None, lumbar 89.9
  - **D071** misnamed_1_2_levels: ids [18, 19, 20, 21, 22, 23, 24, 26]; top-to-bottom as VerSe names ['T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'S']; ctd top-to-bottom ['T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 7/1 (ctd L5 lands in id 26); median ml named cervical None, lumbar 76.4
  - **G171** misnamed_1_2_levels: ids [23, 24, 25, 26]; top-to-bottom as VerSe names ['L4', 'L5', 'L6', 'S']; ctd top-to-bottom ['L4', 'L5', 'L6', 'S']; ctd agree/disagree 3/1 (ctd L6 lands in id 26); median ml named cervical None, lumbar 87.8
- `/rs/.../data/carmlspine/spineps`:
  - **case134** misnamed_1_2_levels: ids [1, 2, 3, 4, 5, 26]; top-to-bottom as VerSe names ['C1', 'C2', 'C3', 'C4', 'C5', 'S']; ctd top-to-bottom ['C1', 'C2', 'C3', 'C4', 'C5', 'S']; ctd agree/disagree 5/1 (ctd C5 lands in id 26); median ml named cervical 60.5, lumbar None
- `/rs/.../data/or_ready/crossdev/levels/spineps_v1_relabel`:
  - **B038** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]; top-to-bottom as VerSe names ['T4', 'T2', 'C5', 'C3', 'C1', 'C2', 'C4', 'C6', 'C7', 'T1', 'T3']; ctd top-to-bottom ['T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/10 (ctd T8 lands in id 9, ctd T9 lands in id 5, ctd T10 lands in id 3, ctd T11 lands in id 1); inverted adjacent: C3 sits 45.8 mm above C2; C5 sits 94.0 mm above C4; T2 sits 198.5 mm above T1; median ml named cervical 37.1, lumbar None
  - **A181** ordered_but_not_names RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L4', 'L5', 'S']; ctd agree/disagree 0/2 (ctd L4 lands in id 1, ctd L5 lands in id 2); median ml named cervical 72.3, lumbar None
  - **A212** verse_monotonic_no_ctd RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L4', 'L5', 'S']; ctd agree/disagree 0/1 (ctd L5 lands in id 2); median ml named cervical 66.2, lumbar None
- `/rs/.../data/cobra2026/seg/spineps_v2`:
  - **D071** misnamed_1_2_levels: ids [18, 19, 20, 21, 22, 23, 24, 26]; top-to-bottom as VerSe names ['T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'S']; ctd top-to-bottom ['T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 7/1 (ctd L5 lands in id 26); median ml named cervical None, lumbar 76.4
  - **D134** misnamed_1_2_levels: ids [17, 18, 20, 21, 22, 23, 24, 25, 26, 80]; top-to-bottom as VerSe names ['T10', 'T11', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd top-to-bottom ['T10', 'T11', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd agree/disagree 8/1 (ctd L6 lands in id 24); median ml named cervical None, lumbar 84.3
- `/rs/.../data/spineps/bodies_cobra`:
  - **B038** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]; top-to-bottom as VerSe names ['T4', 'T2', 'C5', 'C3', 'C1', 'C2', 'C4', 'C6', 'C7', 'T1', 'T3']; ctd top-to-bottom ['T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/10 (ctd T8 lands in id 9, ctd T9 lands in id 5, ctd T10 lands in id 3, ctd T11 lands in id 1); inverted adjacent: C3 sits 45.7 mm above C2; C5 sits 94.0 mm above C4; T2 sits 203.9 mm above T1; median ml named cervical 19.9, lumbar None; body source `/rs/rs_grp_oschome/go2432/data/cobra2026/seg/spineps/B038_seg-vert_msk.nii.gz`
  - **A158** ordered_but_not_names RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L5', 'L6', 'S']; ctd agree/disagree 0/2 (ctd L5 lands in id 1, ctd L6 lands in id 2); median ml named cervical 44.3, lumbar None; body source `/rs/rs_grp_oschome/go2432/data/cobra2026/seg/spineps/A158_seg-vert_msk.nii.gz`
  - **A212** verse_monotonic_no_ctd RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L4', 'L5', 'S']; ctd agree/disagree 0/1 (ctd L5 lands in id 2); median ml named cervical 43.7, lumbar None; body source `/rs/rs_grp_oschome/go2432/data/cobra2026/seg/spineps/A212_seg-vert_msk.nii.gz`
- `/rs/.../data/cobra2026/seg/spineps`:
  - **B038** scrambled RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]; top-to-bottom as VerSe names ['T4', 'T2', 'C5', 'C3', 'C1', 'C2', 'C4', 'C6', 'C7', 'T1', 'T3']; ctd top-to-bottom ['T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/10 (ctd T8 lands in id 9, ctd T9 lands in id 5, ctd T10 lands in id 3, ctd T11 lands in id 1); inverted adjacent: C3 sits 45.8 mm above C2; C5 sits 94.0 mm above C4; T2 sits 198.5 mm above T1; median ml named cervical 37.1, lumbar None
  - **A158** ordered_but_not_names RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L5', 'L6', 'S']; ctd agree/disagree 0/2 (ctd L5 lands in id 1, ctd L6 lands in id 2); median ml named cervical 69.3, lumbar None
  - **A212** verse_monotonic_no_ctd RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L4', 'L5', 'S']; ctd agree/disagree 0/1 (ctd L5 lands in id 2); median ml named cervical 66.2, lumbar None
- `/rs/.../data/spineps/cobra_varian`: none.
- `/rs/.../tmp/bodyspot_40416661/in`:
  - **TSV3_s0004** scrambled_no_ctd: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]; top-to-bottom as VerSe names ['T10', 'T4', 'C7', 'T3', 'T5', 'C1', 'C5', 'C3', 'C6', 'T1', 'T2', 'T7', 'T6', 'C2', 'C4', 'T8', 'T9', 'T11']; ctd top-to-bottom None; ctd agree/disagree None/0; inverted adjacent: C3 sits 156.5 mm above C2; C5 sits 210.7 mm above C4; C7 sits 131.1 mm above C6; median ml named cervical 23.6, lumbar None
  - **TSV3_s0003** scrambled_no_ctd: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; top-to-bottom as VerSe names ['T3', 'T2', 'C6', 'C1', 'C2', 'C3', 'C4', 'C7', 'C5', 'T1']; ctd top-to-bottom None; ctd agree/disagree None/0; inverted adjacent: C6 sits 92.6 mm above C5; T2 sits 122.5 mm above T1; T3 sits 15.6 mm above T2; median ml named cervical 8.5, lumbar None
  - **TSV3_s0002** scrambled_no_ctd: ids [1, 2, 3, 4, 5, 6, 7, 8]; top-to-bottom as VerSe names ['T1', 'C7', 'C5', 'C2', 'C1', 'C4', 'C3', 'C6']; ctd top-to-bottom None; ctd agree/disagree None/0; inverted adjacent: C2 sits 12.9 mm above C1; C4 sits 13.2 mm above C3; C5 sits 38.7 mm above C4; median ml named cervical 9.3, lumbar None
- `/rs/.../tmp/bodyspot_40416661/out`:
  - **TSV3_s0004** scrambled_no_ctd: ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]; top-to-bottom as VerSe names ['T10', 'T4', 'C7', 'T3', 'T5', 'C1', 'C5', 'C3', 'C6', 'T1', 'T2', 'T7', 'T6', 'C2', 'C4', 'T8', 'T9', 'T11']; ctd top-to-bottom None; ctd agree/disagree None/0; inverted adjacent: C3 sits 153.5 mm above C2; C5 sits 205.8 mm above C4; C7 sits 125.0 mm above C6; median ml named cervical 12.2, lumbar None; body source `/rs/rs_grp_oschome/go2432/tmp/bodyspot_40416661/in/TSV3_s0004_seg-vert_msk.nii.gz`
  - **TSV3_s0003** scrambled_no_ctd: ids [1, 2, 3, 4, 5, 6, 7, 8, 9]; top-to-bottom as VerSe names ['T2', 'C6', 'C1', 'C2', 'C3', 'C4', 'C7', 'C5', 'T1']; ctd top-to-bottom None; ctd agree/disagree None/0; inverted adjacent: C6 sits 96.8 mm above C5; T2 sits 127.1 mm above T1; median ml named cervical 3.9, lumbar None; body source `/rs/rs_grp_oschome/go2432/tmp/bodyspot_40416661/in/TSV3_s0003_seg-vert_msk.nii.gz`
  - **TSV3_s0010** scrambled_no_ctd RAW: ids [1, 2, 3, 4, 5, 6, 7, 8, 9]; top-to-bottom as VerSe names ['T1', 'C3', 'C1', 'C5', 'C2', 'C7', 'C4', 'C6', 'T2']; ctd top-to-bottom None; ctd agree/disagree None/0; inverted adjacent: C3 sits 83.9 mm above C2; C5 sits 92.8 mm above C4; C7 sits 64.9 mm above C6; median ml named cervical 24.0, lumbar None; body source `/rs/rs_grp_oschome/go2432/tmp/bodyspot_40416661/in/TSV3_s0010_seg-vert_msk.nii.gz`
- `/rs/.../data/realxray_work/deepfluoro/spineps`:
  - **18-2800** scrambled RAW: ids [1, 2, 3, 4, 5]; top-to-bottom as VerSe names ['C5', 'C3', 'C1', 'C2', 'C4']; ctd top-to-bottom ['L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/4 (ctd L2 lands in id 3, ctd L3 lands in id 1, ctd L4 lands in id 2, ctd L5 lands in id 4); inverted adjacent: C3 sits 64.3 mm above C2; C5 sits 114.2 mm above C4; median ml named cervical 66.4, lumbar None
  - **17-1905** ordered_but_not_names RAW: ids [1, 2]; top-to-bottom as VerSe names ['C1', 'C2']; ctd top-to-bottom ['L4', 'L5', 'S']; ctd agree/disagree 0/2 (ctd L4 lands in id 1, ctd L5 lands in id 2); median ml named cervical 66.3, lumbar None
  - **18-2799** scrambled RAW: ids [1, 2, 3, 4]; top-to-bottom as VerSe names ['C3', 'C1', 'C2', 'C4']; ctd top-to-bottom ['L1', 'L2', 'L3', 'L4', 'S']; ctd agree/disagree 0/4 (ctd L1 lands in id 3, ctd L2 lands in id 1, ctd L3 lands in id 2, ctd L4 lands in id 4); inverted adjacent: C3 sits 58.5 mm above C2; median ml named cervical 52.1, lumbar None
- `/rs/.../tmp/isoctrl_40416665/iso`: none.
- `/rs/.../tmp/isoctrl_40416665/native`: none.
- `/rs/.../data/realxray_work/geneva_hip/spineps`:
  - **phantom** scrambled RAW: ids [1, 2, 3, 4, 5, 6]; top-to-bottom as VerSe names ['C4', 'C1', 'C2', 'C3', 'C5', 'C6']; ctd top-to-bottom ['L1', 'L2', 'L3', 'L4', 'L5', 'S']; ctd agree/disagree 0/5 (ctd L1 lands in id 4, ctd L2 lands in id 1, ctd L3 lands in id 2, ctd L4 lands in id 3); inverted adjacent: C4 sits 75.4 mm above C3; median ml named cervical 26.8, lumbar None
- `/rs/.../data/spineps/spinesac`:
  - **SAC_set1_A** veridah_order_error: ids [19, 20, 21, 22, 23, 24, 25, 26, 80]; top-to-bottom as VerSe names ['S', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6']; ctd top-to-bottom ['S', 'T12', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6']; ctd agree/disagree 7/0; inverted adjacent: S sits 201.8 mm above L6; median ml named cervical None, lumbar 70.8
  - **SAC_closed_A** veridah_order_error: ids [1, 2, 3, 26, 80]; top-to-bottom as VerSe names ['C1', 'S', 'C2', 'C3']; ctd top-to-bottom ['S', 'C2', 'C3']; ctd agree/disagree 2/0; inverted adjacent: S sits 83.4 mm above C3; median ml named cervical 2.9, lumbar None
- `~/VerSeFusion/data/raw/verse19/dataset-verse19training/derivatives`: none.
- `~/VerSeFusion/data/raw/verse19/dataset-verse19validation/derivatives`: none.
- `~/VerSeFusion/data/raw/verse20/01_training/derivatives`: none.
- `~/VerSeFusion/data/raw/verse20/02_validation/derivatives`: none.
- `~/VerSeFusion/data/raw/verse20/03_test/derivatives`: none.
- `/rs/.../data/carmlspine/spineps_retry134`:
  - **case134** misnamed_1_2_levels: ids [21, 22, 23, 24, 25, 26, 80]; top-to-bottom as VerSe names ['L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd top-to-bottom ['L2', 'L3', 'L4', 'L5', 'L6', 'S']; ctd agree/disagree 5/1 (ctd L6 lands in id 26); median ml named cervical None, lumbar 60.7

