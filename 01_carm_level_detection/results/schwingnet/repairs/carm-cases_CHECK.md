# Adversarial check — C-ArmLSpine: case134 not built, case39's third frame dropped, case118's oblique scored as a lateral

Checked 2026-09-23 ~03:20 EDT from the files and the grid, not from the repair report. Nothing below is
taken from the report's own prose; every number was re-derived from disk, from the release census, from the
code, or run locally.

**VERDICT: INCOMPLETE — not yet verifiable as done, and nothing found wrong in what exists.**
The diagnosis is correct and independently confirmed on disk. The code does what it claims. The central
deliverable (the rebuilt bank, `FRAMES_CHECK.md`, the "release minus bank = 0" number and the renders) does
NOT exist: the two GPU jobs are still PENDING on Resources behind three other agents' SPINEPS arrays, and the
two jobs that produce every quoted count are chained behind them. Nine findings below, none of them fatal,
two of which should be fixed before any of this is written into the manuscript.

---

## Per-item PASS/FAIL

| # | Item | Verdict |
|---|------|---------|
| 1 | Jobs exist and are queued/running/finished | **PASS (partial)** — 2 of 6 have run |
| 2 | Outputs where claimed, at the count claimed | **FAIL (not yet)** — the bank, `FRAMES_CHECK.md`, `pose/retired/`, the renders do not exist |
| 3 | The diagnosis is true on disk (case134 ships both frames) | **PASS** — confirmed three independent ways |
| 4 | The fix does what it claims (code read, not summary) | **PASS** |
| 5 | The oblique geometry claim | **PASS**, reproduced locally and on the grid — with one overstatement (F1) |
| 6 | case134's VERIDAH mis-naming | **PASS** — confirmed with dice numbers from the completed job |
| 7 | The split claim (case118 test; case134/case39 train) | **PASS** — recomputed |
| 8 | Nothing else broken | **PASS** — compiles, `bash -n` clean, no carmlspine file left dirty |
| 9 | Audit document updated | **PARTIAL FAIL** — entry present but now stale and cites a cancelled job (F2, F3) |
| 10 | No identifier leaked | **PASS so far**, but the anon gate has not run and does not cover the repo (F8) |

---

## 1. Jobs — what has actually run (sacct, 03:20)

| Job | Name | State | Marker |
|-----|------|-------|--------|
| 40416595 | carmcens | **RUNNING** 21 min | `OBLIQUE_SELFTEST PASS` printed; `CARMCENS_DONE` **not yet** |
| 40416616 | carmlvl | **COMPLETED** 10:21 | `CARMLVL_DONE levels_cases 149` ✔ |
| 40416562 | carmrep2 (poses, GPU) | **PENDING (Resources)** | — |
| 40416563 | carmrep3 (bank, census, anon) | **PENDING (Dependency)** | — |
| 40416603 | carmrepqc (renders) | **PENDING (Dependency)** | — |
| 40416621 | carm134 (2nd SPINEPS reading) | **PENDING (Resources)** | — |
| 40416561 | carmrep1 (superseded) | **CANCELLED** | — |

The GPU pool is full of `spineps_ctsp` (40416509), `spineps_tsv3` (40416540) and `spineps_tsretry` (40416605)
— other agents' arrays, correctly not touched. The report's `not_done` section is accurate.

So: **the repair report's headline count of 299 spot frames is a prediction, not a measurement.** It is
strongly corroborated (§3) but the census that measures it has not printed.

## 2. Outputs that do not exist yet

- `/rs/.../carmlspine/qc/FRAMES_CHECK.md` — absent. `qc/` holds only the six pose contact sheets from 2026-09-21.
- `SchwingNet/results/repairs/CARMLSPINE_CHECK.md` — absent (this file is the only thing in that directory).
- `/rs/.../carmlspine/pose/retired/` — does not exist; the stale `case118_LAT*` poses are still live.
- `/rs/.../realxray/carmlspine_pre_repair_2026-09-23` — not created; the bank backup happens inside 40416563.
- `repair_boxes.png`, `repair_pose_134.png`, `repair_pose_118.png`, `repair_pose_39.png` — absent. **The
  "LOOK, do not stop at the numbers" step has not happened**, and this project has twice been wrong in a way
  only a render showed. Nothing about the box convention on these four frames should be written up until it does.

What DOES exist and is new: `compare_veridah2.csv` (21,746 B, 03:01), `levels.json` rebuilt (03:01),
`levels_pre_repair_2026-09-23.json` kept beside it.

## 3. The diagnosis is true — confirmed three ways, none of them the report

1. **Directory listing.** `case134/CBCT/` holds 396 files: 394 `CT.<uid>` slices and two `XA.<uid>` files of
   8,390,542 and 8,390,548 bytes. 2048 x 2048 x 16 bit = 8,388,608 B of pixels; that is a spot exposure, and it
   is the size every other case's AP/LAT ships.
2. **`release_census.tsv`** (written 01:27, before the repair): 149 cases; `C-arm/` file counts are 2 for 147
   cases, **3 for case39**, **0 for case134**; `CBCT/` is 394 for 147 cases, **396 for case134**, **696 for
   case39**; case134 alone carries an extra `ori/` directory of 302 files. Total `C-arm/` files = **297**.
   297 + case134's 2 = **299**, which is the predicted spot-frame count exactly.
3. **`catalogue.json`** (2026-09-21, the OLD C-arm-only walker): modalities `{CT 58706, XA 901, ? 2}`,
   SOP classes `{CT Image Storage 58706, X-Ray Angiographic Image Storage 903}`. 901 XA = 297 (C-arm) + 301
   (case134/ori) + 301 (case39/CBCT) + **2 (case134/CBCT)**, and the two `?` files are the two non-Modality
   stubs. This independently confirms BOTH the two case134 frames and the 602 sweep projections, and it shows
   the old walker's own catalogue recorded `case134: frames []`, `frame_headers []` — the hole, in its own file.

case118's `0001.dcm` carries `primary "-58.1"` in `catalogue.json`, model `Surgio-B51`. The oblique is real.

## 4. The code does what it claims (read line by line)

- `tools/carmlspine_io.read_frames` walks the whole case tree (`walk_files`) and keeps `Modality == "XA" and
  Rows >= 2048`; it strips a trailing `C-arm` from the path, so **a caller that passes `<case>/C-arm` still
  works for case134, which has no such folder**. Confirmed that is exactly how `tools/device_fit.py:1294` calls it.
- `view_of_angle` is `AP <= 20`, `LAT within 20 of 90`, else `OBL`, and is the only rule that sets a view.
- `spot_frames` tags repeats `LAT2`, `LAT3`…; `carmlspine_labels.build_case` keys its frame dict on that tag,
  so `case39_LAT2` is a separate stem rather than a collision.
- `best_pose` only ever reads `pose/{case}_{view}{tag}.json`, so a file moved to `pose/retired/` is unreachable.
- `stale_stems` **refuses to prune** if the walker raised on any case — a read error cannot silently delete an
  exported frame. Good.
- **Geometric instance selection (commit b4d5caf) is real and correct.** The overlap vote now runs for every
  vertebra; `named` is only cross-checked; the three-way `box_source` is written and counted in `summary.json`
  as `vertebra_box_source` / `vertebra_box_name_disagrees`. The old code's `vid = inv[sp_name]` path, which for
  case134 would have resolved `inv["C1"] = 1` and boxed whatever bone carried instance 1, is gone.
  One behaviour change worth knowing: a vertebra with < 20 voxel hits now gets no body box and falls back to
  `whole_vertebra` where it previously took a name-keyed body box. That is the safer direction and it is counted.
- `carmlspine_frame_census.anon` does split `--bank "A,B"` on commas (so the pose directory really is scanned),
  returns counts only, and `main()` returns 3 on any hit, which `carmlspine_repair_bank.sh` turns into `exit 3`.
- `summary.json` gains `frames_per_view_class`, which the job's final marker line reads — checked, because a
  missing key there would have killed the marker after an 8-hour rebuild. It is written by `finalize`.
- Scripts are resumable (`--skip-done`, `cp -n`, `mv -n`, `FORCE=0` path) and each prints its marker.
- `python -m py_compile` clean on all six tools; `bash -n` clean on all seven slurm scripts; the grid copies of
  `carmlspine_io.py` and `carmlspine_labels.py` are **md5-identical** to the local ones and no file on either
  side has a CR. The jobs will run the code I read.

## 5. The oblique geometry — reproduced, and one overstatement

`python tools/carmlspine_oblique_selftest.py` run **locally on Windows** (numpy + scipy only): PASS, with
max|dR| 0.00e+00, max|dt| 0.00e+00, source shift 0.000e+00 mm at 90 deg; AP convention reproduced at 0 deg;
the two senses give opposite laterals. The grid's own run (40416595) prints the same PASS with 2.2e-16 /
2.7e-15 / 1.7e-13 (float path difference only). The check is not circular: it builds the oblique from the AP
convention and lands on the LAT convention, and the two keys it compares against
(`dir(0, -1, 0)_rot180_m-1`, `dir(1, 0, 0)_rot180_m-1`) are **verbatim the `winner` fields in
`pose/consensus.json`** — I fetched that file and compared.

**F1 (overstatement, fix the wording).** The report calls this "the lateral convention the 296-frame consensus
fitted independently". `consensus.json` says `AP: n 6` and `LAT: n 6` — twelve free registrations, not 296 —
and the LAT winner took **4 of 6 votes, and only 2 of 6 at margin > 0.05**, with `edge_median` 0.218 against
the AP's 0.421. The consensus was then applied to refine 296 frames; it was not fitted from them. The selftest
is still a real, outside-the-computation check, but what it agrees with is a 6-frame majority, and the paper
must not say otherwise.

**F7 (inert, but note it).** `carmlspine_pose.register_frame` passes `view="lat"` to `drr_register.register`
for an OBL frame. Harmless — `view` is only read by `hypotheses()` when `starts is None`, and OBL always
supplies `starts` — but it is a wrong word sitting in the one call the oblique depends on.

## 6. case134's VERIDAH labels — confirmed, with numbers

40416616 completed. `compare_veridah2.csv`: **149 cases, 148 with a VERIDAH relabel, 1 on the plain VerSe-id
mask.** case134 is that one. The rebuilt `levels.json` gives it as a real *disagree* record:

`L1 <-> C1 (dice 0.074)`, `L2 <-> C1 (0.094)`, `L3 <-> C2 (0.336)`, `L4 <-> C3 (0.656)`, `L5 <-> C4 (0.709)`,
`S <-> S (0.003)`, every `level: null`. Summary: 149 cases, 916 vertebrae, 814 agree, 44 disagree, 58
unmatched, 3 `spineps_missing`, 23 variant cases.

So the labeller did not fail to run; it named a lumbar spine cervical, two TotalSegmentator vertebrae were
handed the same SPINEPS name (`C1`), and the old summary really did say 148 while the mask sat on disk
(`spineps/case134_seg-vert_msk.nii.gz` exists; only the `_veridah` variant is absent). The claim about the
name being about to pick the bone is therefore not hypothetical: `inv["C1"] = 1` would have resolved for two
different vertebrae.

## 7. The split — recomputed from the rule, not read from a document

`split_of` = `md5(case) % 10`, `<=6 train / ==7 val / ==8,9 test`:
**case118 → test**, case134 → train, case39 → train. Over 149 cases: 106 train / 15 val / 28 test (the live
bank's `summary.json` reads 105/15/28 over 148 cases — case134 lands in train, and no other case moves).
The mis-typed oblique is in the reported **test** cells, as the report says.

The live bank today: `frames 296, cases 148, per_split {train 105, val 15, test 28}`, and it has **no**
`frames_per_view_class` / `vertebra_box_source` keys — i.e. it is entirely pre-repair. Everything scored on it
must be restated.

## 8. Findings

- **F1** — "296-frame consensus" overstates a 6-frame-per-view consensus with a 4/6 lateral vote (§5).
- **F2 — the audit entry is now stale.** `docs/DATA_COMPLETENESS_AUDIT.md` (the C-ArmLSpine section under
  `## Repairs`) still describes the box rule as *"Where SPINEPS named the level, the instance is chosen by its
  VerSe id as before"* — the rule commit b4d5caf **deleted**. The words "geometric", "name_disagrees" and
  "the name never picks the bone" appear nowhere in the audit. The audit now documents the defect as the fix.
- **F3 — the audit's job list is wrong.** It cites **40416561**, which is **CANCELLED**, and omits 40416595,
  40416616, 40416603 and 40416621. (`JOBS_data_repairs.txt` has all of them, appended, with the cancellation
  recorded — so the JOBS file is right and the audit is not.) The audit also now carries **two separate
  `## Repairs` headings** (lines 969 and 1241), written by different agents.
- **F4 — a docstring generalises from one case.** `carmlspine_io` says "every file in this archive is
  extension-less"; 147 cases name their frames `0001.dcm` / `0002.dcm`, and case134's are `XA.<uid>` /
  `CT.<uid>`. No code depends on it, but it is the kind of sentence that gets quoted into a datasheet.
- **F5 — the sweep count is corroborated but not measured.** 602 = 301 + 301 follows from `catalogue.json`
  (901 XA − 297 C-arm − 2 case134), and both extra directories hold 302 files (301 XA + one stub). The
  census's own `sweep_projections` number is still pending.
- **F6 — the five consumers are named, not fixed.** All five line numbers verified exactly as reported and all
  five still filter `("AP", "LAT")`: `devcorpus_build.py:93`, `device_fit.py:1300`, `carmlspine_eval.py:134`,
  `carmlspine_pool_scores.py:58`, `carmlspine_pose_qc.py:51`; `SchwingNet/tools/fig2_flow.py:52` still draws
  "149 cases released / 1 failed conversion / 148 cases, 296 frames (148 AP + 148 lateral)". One nuance the
  report misses: `carmlspine_eval.py`'s `overall` cell is computed over ALL rows, so OBL and LAT2 will enter
  `overall` while being invisible in the AP/LAT breakdown — the pooled scores (`pool_scores`) drop them from
  every cell. Also confirmed: `device_fit` reaches case134 through the `C-arm`-stripping path, so the
  Surgio-B51 card's input set really does change and no refit job exists.
- **F7** — `view="lat"` passed for an oblique registration; inert (§5).
- **F8 — the anonymity gate's scope.** `anon` covers the frame bank and the pose directory only. It does not
  cover the repository. I checked the repository myself: the only repo file carrying release header values is
  the untracked `SchwingNet/results/inputs/headers_dossier.json` — 746 `PatientID` entries, **all empty**;
  746 `PatientName` entries, 149 distinct, **every one of them literally `caseN`**; one distinct
  `InstitutionName` of three characters. No identifier. No release UID appears in any tracked file. **No leak
  found**, but a green `ANON` line must not be read as a statement about the repo.
  *Note of 2026-10-12.* The text above is as written on 2026-09-23. The copied dossier
  (`results/schwingnet/inputs/headers_dossier.json`, copied 2026-10-08) later carried the case134/ori values: in
  its `dumps` section, the console Patient's Name and Patient ID of that sweep and the private (0029,0016)
  values of the dumped frames; whether that section existed on 2026-09-23 is not recorded. They were redacted to
  `[withheld]` on 2026-10-12 (issue #67), with every other Patient's Name in the file; `MANIFEST_LOCAL.md`
  records the change by kind.
- **F9 — "main.tex's second reason is false" is itself too strong.** `SchwingNet/main.tex:66` says *"One
  C-ArmLSpine directory carrying a residual patient identifier was excluded and reported to the dataset
  authors."* `case134/ori/` is a directory, it is excluded, and the code's own comments say it carries a real
  PatientID — so that sentence can be read as true of `ori/` while the abstract's "148 intraoperative lumbar
  cases" (line 46) is what is false. Both lines need rewriting; only one of them is a false statement.
  main.tex was **not** touched, as required.

## 9. Nothing else broken

`git status`: no `tools/carmlspine_*` or `slurm/carmlspine_repair_*` file is left dirty — the repair is fully
committed in d30ac3b, ed81dff, 156b06d and b4d5caf. `tools/devcorpus_build.py` is modified in the working tree
by a different agent (synthetic pose arcs) and its line-93 filter is untouched. `JOBS_data_repairs.txt` was
appended to, not rewritten. No manifest that this change touches was edited out from under it.

## 10. What must happen before any of this is quotable

1. Wait for `CARMCENS_DONE` (40416595), then `CARMREP2_DONE` → `CARMREP3_DONE … anon_exit 0` → `CARMREPQC_DONE`.
   If 40416562 is still queued in a few hours, the CPU fallback in the report is real work: `register_frame`
   never passes `device`, and `drr_register.register` defaults to `cuda`.
2. Read `release minus bank` in `FRAMES_CHECK.md`. It must be **0**, at 299 / 149 / 149 AP + 149 LAT + 1 OBL.
3. **Open `repair_boxes.png` and the three `repair_pose_*.png`** before anything is said about the body boxes
   on these four frames.
4. Read `vertebra_box_name_disagrees`. A non-zero count is a finding about two labellers, not noise.
5. Fix F2 and F3 in the audit; fix F1's wording wherever "296-frame consensus" was written.
