# F5: adversarial check of the SPINEPS-id repair and the G3 split

2026-09-23, from the files on disk, not from the claims in `IMPACT.md`, `REPAIRS.md` or `split_plan.md`. Nothing
here is committed, and no file owned by another workflow was edited. Numbers come from `verify/` (below) and from
grid job 40427906.

Inputs, pinned:
- `~/split_final.json`: sha256 65a57eb0…, generated 20:18:48, verdict PASS. A copy was read locally.
- `stratify.json`: sha256 ad50e00a…. This equals `split_final.json#stratify_sha256`, and the local, grid and
  `or_ready/spineps_ids/g3_split` copies are identical.
- `transitional_subtypes.csv`: the local copy has CRLF line endings. With them stripped, its sha256 is 65751ac5…,
  the split's recorded input.
- `tools/spineps_ids.py`: md5 cd9c4a0b… on both the grid and local.

## Verdicts

| item | check | verdict |
|---|---|---|
| 1a | C-ArmLSpine truth (Tables 2-3, 814 of 910 agreed) | **PASS** on names |
| 1a | the three C-ArmLSpine "L6 patients" as transitional truth | **FAIL**: the second labeller disagrees on every lumbar bone |
| 1a | "CTSP bodies clean" | **FAIL**: 46 bodies that pass the guard carry lumbar names on the wrong bone |
| 1a | PolyPose | **PASS**: its own outside check would refuse the bad bodies. 9 of its 22 inspected cases are affected |
| 1a | COBRA LSTV screen: raw ids | **PASS**. 3 G3 calls rest on a VERIDAH T12 skip |
| 1b | C4, the CTSP benchmark column (800 of 800 raw, no id ≥ 17) | **PASS**: re-derived exactly |
| 1b | C1, the TotalSegmentator row (12 of 12 raw {1..25}) | **PASS**: re-derived exactly |
| 2 | the guard on real masks: must raise / must pass | **PASS**: 0 failures in 19 cases, plus 17 of 17 unit tests |
| 3 | people per subtype per side, from stratify.json | **PASS**: every cell of split_plan.md matches |
| 3 | no person on two sides across roots (independent keyer) | **PASS** in the 82 item_side roots |
| 3 | every root a bank builder reads is in item_side | **FAIL**: 14 roots (38,776 items) are missing |
| 3 | every known real transitional person is in test | **PASS**. The three C-Arm people are contested (1a) |
| 3 | the TS normals have left the rare-class counts | **PASS** in the inputs and the manuscript. **FAIL** in 7 stale files and in 84 rendered frames |

## 1a. Three consumers IMPACT calls clean

### C-ArmLSpine truth (IMPACT section 3): PASS on names; the three "L6 patients" FAIL as truth

**The skip.** IMPACT does not mention it, but 10 of the 149 post-fix C-ArmLSpine ctds skip T12 at a normal spacing:
case9, 13, 19, 22, 46, 66, 85, 88, 129 and 149 (`verify/f5_checks.json#skips`). In all 10, `levels.json` shows
the same pattern:
- TotalSegmentator calls the top bone T12, and VERIDAH calls it T11 (T10 in case13). That pair is nulled.
- L1-L5 are agreed.

So the skip cost names and put none on a wrong bone. A wrong name survives the gate only where TotalSegmentator
makes the same error, and no third reader exists to check that.

**The three "L6 patients" (case42, case121, case136).** In `levels.json`:
- TotalSegmentator reads the same five mobile bones as **L1-L5**. Its Dice against VERIDAH's L2-L6 is 0.928-0.954.
- TotalSegmentator also has a T12 object above them.
- VERIDAH's ctd starts at **L2**, so its view holds no L1.
- **Every lumbar name disagrees, and no lumbar level is agreed.** Only S is agreed.

The L6 therefore rests on VERIDAH alone. It was called without L1 in view: the defect `split_plan.md` names for 27
of the 38 COBRA L6 calls. The guard cannot see this. `case42` passes as verse_ok, because its ids equal VERIDAH's own
ctd (probe below).

The manuscript already says "one labeller" (methods.tex l.39, results.tex l.24). **`stratify.json`, however, records
all three as `verified: true` with truth `"CBCT labels (SPINEPS+TS agreement)"`. That is false:** the two labellers
disagree on every lumbar body.

### "CTSP bodies and PolyPose" (IMPACT section 3): CTSP bodies FAIL, PolyPose PASS

The guard tests a mask's ids against VERIDAH's own ctd. It never tests them against a reader, so it certifies
VERIDAH's names, not the truth.

**Method.** Against the CTSP reader labels (`repair/rescore/ctsp_postfix/per_case.csv`), a mask whose lumbar names
are shifted has at least 2 of L1-L5 with Dice under 0.5.

**Counts, over the 801 post-fix CTSP masks** (the source of every CTSP body):
- 54 skip T12. The re-guard refuses these.
- Of the other 747, **46 have lumbar names shifted**: 21 of 36 transitional spines and 25 of 711 typical ones.
  They are listed in `verify/f5_checks.json#ctsp_shift`.
- **All 46 bodies are accepted in `bodies_ctd`.** `bodies_ctd_log.jsonl` has them ok with naming verse_ok, and none is
  in `reguard_moved.json`.
- The probe confirms one of them: CTSP_0428 has 4 lumbar vertebrae where the reader has 5, and every L1-L5 Dice is
  under 0.5, yet the guard passes it as verse_ok.

**What this does to the G4 rebuild.** `make_drr_dataset.body_boxes` bridges release name → VerSe id → body id. It
never checks that the body overlaps the release vertebra. So a G4 rebuild on `bodies_ctd` (REPAIRS.md section 4 says
"Use the `_ctd` trees") would draw the Lk body box on the reader's Lk±1 in these 46 cases. That is **58 % of the
transitional CTSP spines the guard lets through**.

The fix: take the body by overlap with the release vertebra, the bodybox_rescore rule, wherever a release label
exists.

**PolyPose** reads the old `bodies/` tree. Of its 22 inspected cases:
- 7 are among the 46 (0008, 0033, 0049, 0376, 0428, 0473, 1004).
- 2 are T12 skips (0302, 0950).

Its `body_mask_consistent` invariant is an outside check: body i must lie inside release label i. It should
therefore refuse all 9, so no wrong PolyPose row can pass silently, but those 9 rows will fail. Not known: whether
PolyPose has generated rows for them. The only row on disk is the pending smoke row for 0874, which is clean.

### COBRA LSTV screen: PASS for raw ids; 3 G3 calls rest on a T12 skip

The screen reads only post-fix trees. For every mask there (580 in `lstv/seg`, 101 in `cobra_varian`), the call made
from the ids equals the call made from the ctd.

The screen does not apply the guard's rule 6, though:
- 56 of the 580 `lstv/seg` ctds skip T12, 4 of them L6 calls.
- **3 of the G3 transitional calls (A270, B015, B041) are L6 calls that see L1 but rest on a skipped ctd.** This is
  the TS_s1178 pattern.

Counting every defect together, re-derived from `stratify.json`:
- 27 of the 38 L6 calls have no L1 in view.
- 7 of the 45 T13 calls name only L1-L4, which is the ordinary 17 thoracolumbar vertebrae.
- 3 L6 calls rest on a skip.

So at most **8 of the 38 L6 calls and 38 of the 45 T13 calls** are free of all three defects. All 91 are on the test
side, which is safe for the split.

## 1b. Two consumers IMPACT calls contaminated, re-derived from the census rows

This uses `census_rows.jsonl.gz`, not `impact_counts.json`. Output: `verify/rederive_census.json`, from
`tools/spineps_ids_rederive_census.py`.

- **C4, `~/bench/spineps/native`: PASS, exact.**
  - 800 masks, 800 raw, with ids exactly 1..N and 5-15 instances each.
  - **The largest id in any of the 800 masks is 15.** No mask has an id of 17 or more, and none has id 26.
  - So a reader of VerSe ids 17-28 finds no class at all, which explains Dice 0.000 everywhere.
  - 7,254 of 7,260 ctd points land in another id, as IMPACT says.
- **C1, the TotalSegmentator row: PASS, exact.**
  - 13 TS v2 masks carry id 25.
  - 12 of them have ids exactly {1..25}. They are raw, dated 09-19, and 0-4 of their 23-24 ctd points agree.
  - The 13th, TS_s0109, is a post-fix mask: 12 of 12 points agree, and VERIDAH calls it L6. It was written on 09-23,
    after the inventory.
  - VERIDAH's calls on the 12: L6 for s1089 and s1178; T13 for s0616, s1088 and s1123; none for the other 7. This is
    as IMPACT states.
- **C6, the size of the raw-body count, depends on the definition.** By source it is 2,714 (CENSUS). By verdict it
  is 2,715 (IMPACT). By each body's own raw-enumeration flag it is 2,599. The headline 2,715 is one definition among
  three, not a disagreement.

## 2. The guard on real masks (grid job 40427906; `tools/spineps_ids_probe.py`; `verify/probe.json`)

| case | expected | got |
|---|---|---|
| raw `TS_s1089` (bench_ts) | raise | raised: raw_or_scrambled, 23 of 24 points in another id |
| raw `COLONOG_1` (bench) | raise | raised: raw_or_scrambled, 9 of 9 |
| raw `VERSE_verse607` (bench_ts) | raise | raised: raw_or_scrambled, 24 of 24 |
| relabelled `VERSE_verse607` (ids 1..25 = C1..L6) | pass | passed: verse_ok, 24 of 24 agree |
| **VerSe expert mask verse607** (ids C3..L6) against VERIDAH's ctd on that CT | pass | **passed**: verse_ok, 23 of 23. This test is not circular, and L6 is included |
| post-fix `CTSP_0001`; post-fix `TS_s0109` (VERIDAH L6) | pass | passed: verse_ok, 10 of 10 and 12 of 12 |
| relabelled `COLONOG_10`; post-fix `CTSP_0016` (same CT, T12 skip) | raise | raised: veridah_skipped_name (30.8 mm gap at a local spacing of 30.5 mm) |
| in-memory faults on relabelled verse607 and on CTSP_0001: permuted ids, every id one level down, raw-style 1..N top-down | raise | raised, 5 of 5 |
| C-ArmLSpine `case42` (TS disagrees on every lumbar name) | limit | passed: verse_ok |
| `CTSP_0428` (lumbar names shifted against the reader) | limit | passed: verse_ok |

A clean VerSe expert mask beside its **legacy VerSe ctd** (no TPTBox header) is **refused by default**. It fails with
verse_ok_no_ctd, because `require_ctd` is True. It passes with `require_ctd=False`. This is safe, but any non-SPINEPS
reader that adopts the guard has to know it.

One fault is a no-op on verse607, and is recorded as such. Renumbering 1..N top-down leaves a C1..L6 whole-spine mask
unchanged, because its VerSe ids already are 1..25. The same fault is caught on CTSP_0001 (10 of 10 points).

Locally, `tools/test_spineps_ids.py` gives ALL PASS (17 of 17).

## 3. The G3 split

**People per subtype per side, re-derived from `stratify.json#people` (non-real): PASS.** Every row of split_plan.md
matches, and so does every per-corpus cell:

| subtype | train / val / test |
|---|---|
| L6 | 53 / 11 / 43 |
| T13 | 3 / 1 / 3 |
| sacralised_L5_fused | 14 / 3 / 11 |
| castellvi_I_II | 16 / 3 / 12 |
| lumbar_rib | 7 / 1 / 6 |
| unassigned | 1 / 1 / 2 |

Each row is the exact 50/10/40 largest-remainder allocation. The 4 unassigned people are the small-cell rule's 1/1/2.
Distinct patients in `transitional_subtypes.csv`:
- L6 110 (112 cases), which is 107 CT plus 3 real;
- T13 7, sacralised L5 28, Castellvi I/II 31, lumbar rib 14, unassigned 4.

`stratify.json` sides equal `split_final.json#side_of_person` for all 291 people and all 692 COBRA cases, with 0
mismatches.

**No person on two sides: PASS where it can be checked** (`tools/g3_split_verify.py`, `verify/g3_split_verify.json`).
The check keys every item independently:
- **Names:** my own per-root regexes, 26 patterns, with nothing taken from make_split's keyer.
- **CTSP:** `CTSP_COLONOG_<token>` is resolved to the release id through the CT path in `benchmark/cases.csv` (802
  tokens).
- **Borrowed:** only the folds a name cannot carry. These are VerSe series → subject, VinDr image → study, SpinalAI,
  and the TotalSegmentator v201/v300 content aliases (`raw_to_group`, `group_of`).

Result:
- 193,643 items in 82 roots.
- 182,179 items keyed. The rest are FluoroCap and Mendeley (excluded) and SpinalAI (train by policy).
- 26,920 persons, of whom 24,969 appear in more than one root.
- **0 persons on two sides**, including hold as a side.
- **0 items whose side differs from `side_of_person`** of the independent key.

**FAIL: the consumer contract.** make_split keys 14 roots but never writes them to `item_side`: **38,776 items** in
`devcorpus/styled/*` (10 roots), `devcorpus/render/*` (3) and `realxray/carmlspine_multi`. The cause is
`tools/make_split.py` l.788, which writes only the ann/meta kinds. split_plan.md tells a bank builder to "read
`item_side`". For the flagship's styled device corpus, and for the multi-frame C-arm set, there is nothing to read.
The builder would have to re-key those items with the pose-donor rule itself. make_split's own CHK-1/3 did cover
these roots; this check could not.

**Real transitional people in test: PASS for everyone the split knows.** Every item of each person below is test in
every root: the 3 C-ArmLSpine people, the 91 COBRA calls and the 3 re-read candidates. No such person has a non-test
item. Two caveats:
- The 3 C-ArmLSpine people are contested (1a).
- The screen's sensitivity is not measured. The COBRA ordinary_call cases (259 / 44 / 41) and fov_limited cases
  (186 / 27 / 23) take their hash sides. On CTSP, VERIDAH's lumbar count was right on only 38.5-46.2 % of
  transitional spines (REPAIRS.md section 4). So **undetected transitional COBRA people are almost certainly on the
  training side. How many is not known.**

**The TS normals have left the rare-class counts: PASS in the inputs and the manuscript.**
- `transitional_subtypes.csv` holds 4 TS rows: s0616 T13; s1088, s1089 and s1123 L6.
- None of the 8 normals is in `stratify.json#people`. They take hash sides: s0224, s0790 and s1171 test; s1124, s1178,
  s1304, s1350 and s1380 train.
- The local `anomalous_inventory.json` has TS 4 (3 L6, 1 T13).
- Table 2 prints 110 L6 with TS 3, and footnote (a) says the eight are not counted.

**Still stale: FAIL.**
- The grid copy `~/spinesurg-ct-nnunet/SchwingNet/results/anomalous_inventory.json` (00:21) still says TS 12 L6.
- `power_table.json#inventory_today` still has TS 12 / 89 / 37.
- `figures/fig6_claim.*` (03:12) was retired from the manuscript but is still on disk.
- `results/polypose/sampling_spec.json` still has `L6_spineps_called` 12, `in_bank` 9 and `N_rare_real_ct` 86.
- `NUMBERS.md` still carries the old values at l.207, 233, 280 and 282 (89 / 37 / 90.6, "L6 83 (18 / 50 / 12 / 3)").
- So do `CLAIMS_LEDGER.md` l.209 and `LEVELCHECK_CLAIM.md` l.128-139.
- **Frames:** 84 rcts2 frames of `TS_s1178` still carry subtype L6. That person is ordinary and on the **train**
  side, so a rare-class bank that reads the ann subtype trains on 84 false L6 frames.
  - s1088 (train, 89 frames) and s1123 (test, 80 frames) are annotated T13 but stratified L6.

The pre-G3 rare-class split `/rs/.../rare_class/split_report.json` (18:29, two-way, val 0.15) disagrees with G3:
- 974 of its train people are G3 test;
- 201 of its val people are G3 test.

Nothing may be built from it.

## Sentences and numbers that must change (owned elsewhere: named, not edited)

- **`stratify.json` people `carmlspine:case42/121/136`** (make_split input): `verified: true` and truth
  "SPINEPS+TS agreement" are false. They should read VERIDAH only, with TotalSegmentator reading L1-L5 on the same five
  bodies and no L1 in VERIDAH's view.
- **results.tex l.19-20 and l.63-66, and Table 2 footnote (c)**: "three intraoperative", "the three intraoperative
  L6", "every real transitional subject on the test side (the three C-ArmLSpine L6)". These are three cases one labeller calls L6 and the other reads L1-L5.
  Without them, the transitional test count has no real person.
- **results.tex l.66**, "with all 83 unread COBRA2026 calls confirmed, 86 persons would allow 95.7 %". By the calls'
  own content, at most 46 of the 83 can be confirmed, because 27 L6 calls have no L1 in view, 7 T13 calls count
  L1-L4 only, and 3 rest on a skip:
  - 46 + 3 = 49 persons gives 92.7 %;
  - 46 persons, without the three contested C-Arm cases, gives 92.3 %.
- **IMPACT.md section 3**, the rows "CTSP bodies and PolyPose" and "the three C-ArmLSpine L6 patients", and
  **REPAIRS.md section 4**, "Use the `_ctd` trees". Both need the 46-case caveat, and the G4 rebuild needs the
  overlap gate above.
- **IMPACT.md section 4 is superseded.** The manuscript now prints 194 / 110 L6 / 43 + 3 / 91.8 % from the built
  split, so 190 / 81 / 34 / 89.8 % are no longer the values to substitute. The stale places are listed in section 3
  above.
- **`tools/make_split.py` l.788**: write `item_side` for the images and npz roots too.

## Files

These are new and uncommitted:
- `tools/spineps_ids_probe.py` (also on the grid, md5 c9a0720b…);
- `tools/spineps_ids_f5_checks.py`, `tools/g3_split_verify.py` and `tools/spineps_ids_rederive_census.py`, which read
  json and csv only;
- `SchwingNet/results/spineps_ids/verify/`: `probe.json`, `probe_40427906.log`, `f5_checks.json`,
  `g3_split_verify.json`, `rederive_census.json`, and `carmlspine_levels_copy.json` (a copy of
  `/rs/rs_grp_oschome/go2432/data/carmlspine/levels.json`, 03:11).

Grid output: `/rs/rs_grp_oschome/go2432/data/or_ready/spineps_ids/verify_f5/`. The first probe run (40427898)
counted the no-op fault as a failure and was superseded by 40427906.

Not done: CHK-6 and CHK-7 (no ledger), and the "in v8/v9 train" column (it needs the bank keys).
