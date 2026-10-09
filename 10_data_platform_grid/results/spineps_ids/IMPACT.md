# What the raw SPINEPS ids reached, and by how much

2026-09-23, task F4 of the SPINEPS-id workflow ("impact and repair"). This page crosses the census (F2,
`CENSUS.md`, `census_rows.jsonl.gz`) with the consumer map (F3, `CONSUMERS.md`). For every reader that turns a
SPINEPS instance id into a level name and reads a tree with raw or scrambled ids, it says which results are
wrong and by how much. The repair (new trees, the guard, what was re-derived) is in `REPAIRS.md`. Nothing is
committed. No manuscript file, table or `NUMBERS.md` was edited: the sentences and numbers that have to change
are named in section 4.

Every count here comes from a file. `impact_counts.json` is `tools/spineps_ids_impact.py` run over the census
rows. `rederived.json` is `tools/spineps_ids_rederive.py` run over the relabel records and the inventory.
`repair/` holds the relabel summaries and the verification rows from grid jobs 40425591-40426277.

## 0. The answer in one paragraph

The raw ids reached **one manuscript number chain**: the TotalSegmentator row of the transitional inventory,
which feeds Table 4, results.tex lines 15-17, NUMBERS.md lines 156 and 229, `power_table.json` and Figure 6d.
All 12 TotalSegmentator "L6" persons were chosen by "id 25 present" on raw masks. By VERIDAH's own ctd, 2 of
them are L6, 3 are T13 and 7 are ordinary spines, and one of the 2 L6 (s1178) is refuted from outside VERIDAH.
By the independent rib count (TS12_VERIFY.md), 4 are transitional and 8 are not. Re-derived under every
corrected reading, the 40 % test side falls from 37 to 33 or 34 persons, and the Wilson lower bound at zero
errors falls from 90.6 % to **89.6-89.8 %, under the pre-stated 90 % target**. Everything else the raw ids
reached is either unquoted (the CTSP SPINEPS benchmark column, the TS rows of the mask census, the pass-1
rare-class frames, all purged or void) or not built yet (every body-box bank). The **sacrum class** cannot
be wrong by id in a raw mask, because no raw mask carries a sacrum. It is wrong for a different reason in the
SpineSAC phantom truth, where VERIDAH itself put the sacrum label on a speck at the top of the column
(section 2, C8). No detection number, no Table 2 or 3 number, and no C-ArmLSpine truth is affected.

The repair restores VERIDAH's names, and that is all it can do. Against the CTSP readers, the repaired benchmark
column counts the lumbar spine right on 96 % of ordinary spines and on 38-46 % of transitional ones. VERIDAH's T12
skip was wrong on all 53 CTSP cases that carry one: its thoracic names were one level low. The guard now refuses a
skip (REPAIRS.md).

## 1. The raw trees: what an id-as-name reader got

"ctd points wrong" counts VERIDAH's own ordered points (the ctd json beside each mask) that land inside an
instance carrying another id. That is the rate at which a reader naming by id gets a wrong name at a vertebra
VERIDAH did name. Source: `impact_counts.json` (from census rows, jobs 40424914/40424915).

| tree | masks | ids not names | named instances in them | ctd points wrong / tested | masks with every point wrong | id 26 present in a bad mask | ctd names a sacrum |
|---|---:|---:|---:|---:|---:|---:|---:|
| `~/bench/spineps/native` (CTSP one-shot benchmark) | 800 | 800 | 7,738 | 7,254 / 7,260 (99.9 %) | 794 | 0 | 800 |
| `~/bench_ts/spineps/native` TS v2 | 1,144 | 1,103 | 14,020 | 13,142 / 13,529 (97.1 %) | 819 | 0 | 567 |
| `~/bench_ts/spineps/native` VerSe | 374 | 366 | 5,034 | 4,681 / 4,827 (97.0 %) | 260 | 0 | 286 |
| `/rs/.../spineps/tsv3` (1,116 links into bench_ts) | 1,616 | 1,113 | 14,181 | 13,128 / 13,677 (96.0 %) | 819 | 8, none raw (6 VERIDAH order errors, 2 real sacra) | 574 |
| `/rs/.../cobra2026/seg/spineps` (COBRA Elekta v1) | 146 | 146 | 910 | 826 / 826 (100 %) | 146 | 0 | 146 |
| `realxray_work/deepfluoro`, `geneva_hip` (plain) | 7 | 7 | 25 | 22 / 22 | 7 | 0 | 7 |
| `/rs/.../spineps/bodies` TS v2 / TSV3 / VerSe | 3,134 | 2,569 | 32,107 | 30,889 / 31,835 (97.0 %) | 1,898 | 0 | 1,419 |
| `/rs/.../spineps/bodies_cobra` Elekta | 147 | 146 | 838 | 826 / 826 (100 %) | 146 | 0 | 146 |

The 3 % of points a raw mask gets right are coincidences: raw id k happens to sit on VerSe level k (533 points in
390 of the raw TS v2 masks). The post-fix trees (`spineps/ctsp` 801, `cobra2026/lstv/seg` 580,
`spineps_v2` 290, `cobra_varian` 101, `carmlspine` 149 + 148 `_veridah`, `spineps_v1_relabel/*_veridah` 145, CTSP
bodies 801, Varian bodies 99) get 0.0-0.5 % of points wrong. That residue is VERIDAH's own one-level defects: an L6
sliver whose point sits in the sacrum, an id-26 fragment at the top of the field.

**The sacrum class.** A raw enumeration reaches id 26 only with 26 or more instances, and **no raw mask in any tree
carries an id 26** (0 of 800, 1,103, 366, 146). The raw SPINEPS semantic mask has no sacrum class either (labels
41-53, 70-74, 100; smoke job 40425314 on COLONOG_1 and TS_s0224). In 10 of the 853 raw TS v2 masks whose ctd names
a sacrum, the ctd S point lies inside an instance, and that instance is an 8-40 ml S1-level piece. So a reader
that looks for 26 in a raw tree finds **no sacrum**. That gives a miss, never a box on another bone. The 8 id-26
cases in tsv3 are post-fix masks where VERIDAH itself named 'S' above L5/L6 or T12 (`TSV3_s1411`, `s1487`, `s1762`,
`s1890`, `s1917`, `s1947`), plus two whole-spine masks (`s1677`, `s1995`) whose 26 is a real 213-279 ml sacrum. The
census flags those two as raw only because a C1..L6 + S spine is also exactly 1..26.

## 2. Consumers that name by id and read a raw tree: CONTAMINATED

Numbers are per consumer. "Quoted?" means a manuscript number depends on it. Summary first; the evidence follows.

| # | consumer (tree) | what carries a wrong name | sacrum class | quoted? |
|---|---|---|---|---|
| C1 | transitional inventory, TS row (bench_ts raw) | 12 of 12 persons' subtype; 8 of 12 not transitional; 91 VERIDAH-transitional TS subjects never seen | not involved | **yes**: Table 4, results l.15-17, NUMBERS l.156/229, Fig. 6d, power_table |
| C2 | rare-class pass-1 renders (bench_ts raw) | every level name on every frame bar chance coincidences (about 3 %), 12 cases (frames purged) | no id 26 in the masks → no sacrum box (a miss) | no |
| C3 | rare-class rcts2 renders (fixids-relabelled) | 0 from ids; VERIDAH's own: s1178 84 frames subtype L6, 309 boxes one level off; s1088/s1123 234 boxes convention-dependent | 0 of 933 frames carry a sacrum box | no |
| C4 | CTSP benchmark SPINEPS column (bench raw) | 800 of 800 cases: no id ≥ 17 exists, every class scored 0.000 | no id 26 → sacrum Dice 0 (a miss) | no |
| C5 | transitional mask census, TS rows (bench_ts raw) | every TS row | no id 26 | no (nothing reads it) |
| C6 | body masks → DRR body boxes, Varian overlay (bodies, bodies_cobra raw) | 2,715 bodies carry raw ids; 0 results built from them yet | no id 26 in a raw body → the DRR keeps the outline sacrum box | no (G4 exposure) |
| C7 | COBRA v1 levels → COBRA export (seg/spineps raw) | 823 of 858 SPINEPS names; the first v3 build zeroed every agreed level (fixed by the v2 pin) | box class from TotalSegmentator: unaffected; its `level` was null | no |
| C8 | SpineSAC body truth (post-fix, VERIDAH order error) | set1_A "L6" 5.4 ml sliver | **wrong**: the sacrum truth is a 0.44 / 0.16 ml speck at the top of the column; "sacrum found 0 %" everywhere | no |
| C9 | case134 plain mask (post-fix, VERIDAH size error) | C1..C5 on the five bones the retry run calls L2..L6; every name already disagreed with TotalSegmentator → null | not involved | no |

**C1. The transitional inventory, TotalSegmentator row.** `tools/anomalous_inventory.py` `ts_cases` (l.84-94
at 421138c: `l6 = 25 in ids`) → `transitional_subtypes` → Table 4, results.tex l.15-17, NUMBERS.md l.156/229,
`power_table.json`, Figure 6d, PolyPose `N_rare_real_ct`. **Quoted.**
- **12 of 12** subtypes were read from a raw id: every mask had ids exactly {1..25}, the 25 instances of a
  whole-spine field (TS12_VERIFY.md).
- By VERIDAH's ctd (the relabel reproduces it: `rederived.json#ts12_after_relabel`): s1089 L6; s0616, s1088 and
  s1123 T13; seven none; s1178 refused. s1178's ctd skips T12 at a normal spacing, and the 12th ribs meet its "L1"
  (TS12_VERIFY `TS_s1178_axial.png`). So **8 of the 12 are not transitional** by either reader.
- Missed: over the whole TS v2 bench, VERIDAH's ctd calls **37 L6, 53 T13 and 1 both among the 1,114 masks that
  could be relabelled** (30 refused; `rederived.json#trees`). None of these reached the inventory, because the
  reader looked for id 25. CONSUMERS.md section 4 shows why VERIDAH alone is not truth for them: on CTSP, 10 of its
  24 L6 calls are reader L6.
- The inventory file has already been corrected in the working tree by the workflow that owns it:
  `anomalous_inventory.json` now says TS 4 (3 L6 + 1 T13, train 4), from the F1 rib count, modified 18:52. Every
  number derived from it is still the old one: `power_table.json` (03:12) and Figure 6d, results.tex, Table 4,
  NUMBERS.md, CLAIMS_LEDGER.md l.209 and LEVELCHECK_CLAIM.md l.128-139.
- Re-derived (`rederived.json#readings`). The Wilson formula is checked cell by cell against the 30 cells of
  `power_table.json` first, and the manuscript row reproduces exactly (89 / 37 / 90.6 / 86.2):

| reading of the TS row | TS L6 / T13 | count-changing persons | L6 / T13 persons | CT subjects | test persons (40 %) | Wilson lower bound k = 0 / k = 1 | 50 % rule | v8 train half |
|---|---|---:|---:|---:|---:|---|---:|---:|
| manuscript today (id 25 on raw masks) | 12 / 0 | 89 | 83 / 6 | 86 | 37 | 90.6 / 86.2 % | 46 | 65 |
| VERIDAH ctd on the 12, s1178 refuted | 1 / 3 | 81 | 72 / 9 | 78 | 34 | **89.8** / 85.1 % | 42 | 60 |
| independent rib count (the inventory on disk now) | 3 / 1 | 81 | 74 / 7 | 78 | 34 | **89.8** / 85.1 % | 42 | 60 |
| no TotalSegmentator row | 0 / 0 | 77 | 71 / 6 | 74 | 33 | **89.6** / 84.7 % | 40 | 56 |

  Under every corrected reading, the pre-stated exact-level target (lower bound ≥ 90 %) **is not met even with
  zero errors** at the inventory on disk. Table 4 "Any transitional subtype" moves from 198 (48 / 135 / 12 / 3) to
  190 (… / 4 / …) or 186.

**C2. Rare-class renders, pass 1.** `SchwingNet/slurm/rare_class_ts_drr.sh` l.71 (`assert 25 in ids`, then
`--scheme verse` on the raw mask). **Every name on every frame was wrong** bar chance coincidences (about 3 % of
points, section 1), in all 12 cases: the raw id was drawn as the level. The frames were purged when `rare_class_ts_drr2.sh` re-rendered them. Not quoted. The script now
runs the guard before it renders (REPAIRS.md section 1), so a raw mask stops the task.

**C3. Rare-class renders, pass 2 (rcts2: 40424662 / 40424677, 933 frames in
`/rs/.../rare_class/totalsegmentator_drr`).** The names come from `rare_class_ts_fixids.py`, the ctd rank-match,
which `tools/spineps_ids.py relabel` reproduces on 268 of 268 instances (REPAIRS.md section 3). So they are not raw-id names.
What remains wrong is **VERIDAH's**:
- **s1178: 84 frames carry subtype L6, and 309 boxes in 65 frames named L1-L6 are one level off** (VERIDAH's
  L1..L6 are T12, L1..L5 of an ordinary spine).
- s1088 and s1123: 234 boxes in 69 frames named T13 / L1-L6. Whether these names are right depends on a
  convention: the 20th vertebra is rib-less, so it is T13 by VERIDAH and L1 of an L6-pattern spine by ribs.
- **No sacrum box in any of the 933 frames**, so fixids' 26-on-a-fragment (s0790, s1124, s1350) and
  26-on-an-S1-piece (s0224, s1304, s1380) never reached a frame.
- Not quoted; the frames feed the rare-class split (`split_report.json`, 18:29).

**C4. The CTSP one-shot benchmark, SPINEPS column.** `benchmark/spineps_to_oneshot.py` maps VerSe ids 17-28 to
T10..sacrum on `~/bench/spineps/native`: **800 of 800 masks raw**. Those masks hold 5-15 instances, so an
id of 17 or more exists in **none** of them (census rows), and `~/bench/spineps/score/report.txt` reads **Dice 0.000 on every class
and a rib-free count error of -4 to -6 on all 800**. The column was void, not low. Not quoted (`collect.py`
"to write"). Re-scored on the repaired tree (REPAIRS.md section 4): **rib-free lumbar count exact 93.7 % (typical 96.2 %,
transitional 46.2 %)**, with lumbar Dice 0.90 on ordinary spines. An independent post-fix run of the same CTs scores
93.5 %. The sacrum is not carried.

**C5. `tools/transitional_mask_census.py`, TS rows.** It read `~/bench_ts/spineps/native` ids as VerSe names under the
tag `spineps_veridah`, so every TS row's L6/T13/lumbar count is wrong. Nothing reads its output
(`/rs/.../rare_class/mask_census/mask_census.json`). Not quoted. It now reads the relabelled tree and runs the guard.

**C6. Body masks (`tools/body_masks.py` → `/rs/.../spineps/bodies`, `bodies_cobra`).** The ids are copied from the
source instance mask, so **2,715 bodies carry raw ids**: TS v2 1,101, TSV3 1,102, VerSe 366, COBRA Elekta 146
(`impact_counts.json`, by verdict; CENSUS.md's 2,714 counts by its raw-instance flag). Their readers:
- `make_drr_dataset --body-mask-dir` (`body_boxes` bridges name → VerSe id → body id) has **built no bank yet**
  (CONSUMERS #9). Only a shape test stood in the way, and it holds only because raw bodies sit on SPINEPS's crop
  grid. The G4 body-box rebuild would have put every TS and VerSe body box on the wrong vertebra.
- `cobra_varian_geometry overlay` has been run on Varian cases only (clean).
- bodybox_rescore bridges by overlap (clean, CONSUMERS #10).
- PolyPose reads CTSP bodies only (clean, and checked against the release labels).
Contaminated results today: **none**. Exposure: every future body-box bank on TS, TSV3, VerSe or COBRA Elekta.

**C7. COBRA v1 levels (`tools/dual_seg_compare.py` on `cobra2026/seg/spineps` → `seg/levels.json`).** **823 of the
858 SPINEPS names in it are cervical** ("C4" on a sacrum; counted by grep on the grid file). Its reader
`realxray_cobra_export.py` defaulted `--levels` to this file. The first `cobra_elekta_v3` build took the default
and **zeroed every agreed level** (`v3_eval right=0 wrong=0`). It was already fixed by pinning `levels_v2.json` in
`realxray_cobra_export_v3.sh` l.31, and the v3 dataset on disk uses v2. No false L6/T13 flag was possible: no
v1 mask has 25 or more instances (id 25 present in 0 of 146). Not quoted. The default is now `levels_v2.json`,
and the raw file is refused by content (REPAIRS.md section 1).

**C8. SpineSAC phantom truth (NEW; VERIDAH's own error, not raw ids).** `spineps/spinesac` is post-fix and its ids
equal the ctd (7/7 and 2/2). But **VERIDAH named the sacrum at the TOP of the column**:
- set1_A: the id-26 "sacrum" is a 0.44 ml speck 202 mm above L6.
- closed_A: a 0.16 ml speck.
- set1_A's "L6" is a 5.4 ml sliver.
`tools/spinesac_bind_bodies.py` keeps 26 whole and marked both specks **usable sacrum truth**
(`/rs/.../or_ready/spinesac/truth/body_summary.json`, 03:44). `or_ready/spinesac/results_table.md` scores
against that truth and reads **"sacrum found" 0 % (or not computable) and "AP50 sac" 0 % (or not computable) on
every row that has truth, for every detector and device** (grep over the table, 5 detectors). That
is a finite number measured against a sacrum box that sits on no sacrum. Not quoted: the manuscript mentions
SpineSAC only as frames and as a future six-device card source (tab_corpus note (k); CLAIMS_LEDGER l.156).
**Nothing in `results_table.md` about the sacrum means anything until the truth is rebuilt.** The guard now refuses
both masks (`veridah_order_error`).

**C9. case134 plain mask (VERIDAH's own error).** `carmlspine/spineps/case134_seg-vert_msk.nii.gz` names C1..C5 on
54-64 ml bones over an L2-S field (census row). It is read only by `dual_seg_compare` for case134, where every name
disagrees with TotalSegmentator, so the level is null. **No agreed name is wrong.** The retry mask
(`spineps_retry134`, L2..L6 + S) is the one with an L6 call. The guard now refuses the plain mask
(`veridah_size_contradiction`).

## 3. CLEAN, with the evidence

| result | why it is clean | evidence |
|---|---|---|
| C-ArmLSpine truth (Tables 2-3, 814 of 910 agreed, lcurve, counting, coupling) | post-fix masks, and a name is kept only where TotalSegmentator agrees; the bone is chosen by overlap | census: `carmlspine` 148/149 verse_ok, 1 is case134 (C9); `_veridah` 148/148; CONSUMERS #16 |
| the three C-ArmLSpine "L6 patients" | VERIDAH's ctd names exactly these 3, and the ids agree | `impact_counts.json` carmlspine: id 25 present 3, ctd L6 3, both 3 |
| every detection number (Table 2, lcurve, crossdev) | class-only boxes from TotalSegmentator, or bodies chosen by overlap; no SPINEPS id is read | CONSUMERS #17, #23 |
| bodybox_rescore (855 of 893; 35.8 % BODY control) | TotalSegmentator vertebra → SPINEPS body by world-space overlap; the raw id is only a key | `bodybox_rescore/grid/truth_build.json` (A053: L4 = 1, L5 = 6) |
| level banks, learning, the 749-spine anomaly manifest | names come from release labels or films; no SPINEPS path, no `--body-mask-dir` | CONSUMERS #26 |
| CTSP bodies and PolyPose | CTSP bodies trace to post-fix VerSe-coded masks; PolyPose uses body *i* only inside release label *i* | census: bodies CTSP 801/801, 1 wrong point in 7,265 |
| COBRA LSTV screen (104 screened, 6 L6, 4 T13) | reads post-fix trees only; the raw v1 tree is excluded; since 18:36 it names from the ctd (another workflow's edit) | census: lstv/seg 580/580 and cobra_varian 101/101 id call = ctd call |
| COBRA v2 levels (`levels_v2.json`, the v3 export) | post-fix run + POI relabel | 0 of 900 SPINEPS names cervical (grep); `spineps_v2` 290 clean |
| DeepFluoro and Geneva exports | read `_veridah` only | census: every `_veridah` verse_ok |
| rcts2 raw-id names (not VERIDAH's) | fixids rank-match, cross-checked | 268 / 268 instances agree with the new relabel both ways (REPAIRS.md section 3) |

## 4. Numbers and sentences that must change (owned elsewhere: named, not edited)

- **results.tex l.15-17**: "198 (48 CTSpinoPelvic1K, 135 VerSe, 12 TotalSegmentator, three intraoperative), 89
  count-changing (83 sixth lumbar, six thirteenth thoracic), 65 in the training half". Under the inventory on disk
  now: 190 (48 / 135 / 4 / 3), 81 count-changing (74 L6, 7 T13), 60 in the training half. The TS subtype split
  depends on the convention chosen for s1088 and s1123.
- **Table 4** (`tab4_transitional.{tex,md}`):
  - L6 row: 83 (18/50/12/3) → 74 (18/50/3/3).
  - T13 row: 6 → 7 (0/6/1/0).
  - Any row: 198 → 190.
  - "37 projected for the 89" → 34 for the 81.
  - Footnote (c): 89 / 65 → 81 / 60.
  - Footnote (d): 3 + round(0.40 × 86) = 37, 90.6 / 86.2 % → 3 + round(0.40 × 78) = 34, **89.8 / 85.1 %**.
  - The by-mask-representation sentence "L6 own label 83": the 12 TS rows were the false "SPINEPS mask carries L6
    as id 25".
  - The v8 split sentence ("L6 16 validation, 61 train, 3 leaking, 3 absent").
- **NUMBERS.md l.156** (Figure 6d inventory marker) and **l.229** (Table 4 persons): same substitutions.
- **Figure 6d and `power_table.json#inventory_today`**: re-run `python SchwingNet/tools/fig_claim.py` once the
  inventory is final. It reads `anomalous_inventory.json#summary` and draws the marker at n = 34 and 89.8 %,
  **under the 90 % line**.
- **CLAIMS_LEDGER.md l.209** ("TotalSegmentator 12") and **LEVELCHECK_CLAIM.md l.128-139**.
- **`transitional_subtypes.{csv,json,md}`** (the 12 TS rows as L6, `mask_representation = "SPINEPS mask carries
  L6 as id 25"`) and **`stratify.json`** (`ts:s1178` L6). The owning workflow modified both files at 18:53-18:54.
  Check that s1178 is no longer L6.
- **PolyPose** `sampling_spec.json` `real_rare_ct_inventory.totalsegmentator.L6_spineps_called` 12 (`in_bank` 9),
  `N_rare_real_ct` 86 → 78 under the inventory on disk, and `SAMPLING_SPEC.md` l.407.
- **rcts2 frames of TS_s1178** (84 frames, subtype L6, 309 lumbar boxes one level off): relabel or exclude.
  **s1088 / s1123** (234 boxes): state the convention.
- **SpineSAC** `results_table.md` sacrum columns: void until the phantom sacrum truth is rebuilt from another
  labeller (C8).

## 5. UNKNOWN (said, not guessed)

- **Whether VERIDAH's names are right where it is the only labeller.** The repair restores VERIDAH's names; it
  cannot make them true. Measured where readers exist:
  - CTSP (CONSUMERS section 4): 10 of 24 L6 calls are reader L6; 0 of 52 T13 calls are reader T13.
  - VerSe: 34 of 42 L6 calls.
  - Per level against the CTSP reader labels: the re-score in REPAIRS.md section 4.
  - VERIDAH skips T12 in 53 CTSP-benchmark, 43 TS v2, 34 VerSe and 8 COBRA relabels. The relabel reproduces the
    skip and flags it (`veridah_skipped_names`). Where a reader exists, the skip was false every time it was looked at:
    - **All 53 CTSP benchmark skips** (re-score against the release labels, REPAIRS.md section 4): the reader's T12
      scored 0 in 53 of 53, and T11 below 0.2 in 50. The lumbar names are right, and the thoracic names are one level
      low. The renders of COLONOG_10 and COLONOG_117 show it.
    - TS_s1178: the lumbar names are one level off.
    The guard now refuses a skip (REPAIRS.md section 1, rule 6). The TS and COBRA skips (43 and 8) have no reader.
    The 34 VerSe skips do have one (the expert masks), but that comparison was not run. For all of them the
    direction is **not known**: a thoracic shift leaves VERIDAH's lumbar count call (L6 / T13 / none) intact, and a
    lumbar shift, as in s1178, makes a false L6. That matters for every VERIDAH-only subtype call, including the COBRA
    LSTV screen.
- Whether any render or bank outside the repository's scripts used `--body-mask-dir` (CONSUMERS section 6). The
  grid copy of `make_drr_dataset.py` (09-22 12:52) predates the body-mask code, so no grid run could have.
- The bodybox_rescore builder's source (grid-only). Its overlap rule is read from its record, not its code.
- What id 80 is.
