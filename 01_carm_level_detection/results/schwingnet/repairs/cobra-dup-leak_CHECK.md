# CHECK — COBRA counted up to four times in one detector arm

Adversarial verification, 2026-09-23, from the files and the grid rather than the report.
Repair under review: fail-closed bank admission in `tools/realxray_train.py` + census job 40416578.

**VERDICT: PASS on all six required items.** Every headline number reproduced exactly from the
grid. Five defects of my own are recorded below; none invalidates the repair, but one (A) is a
real data gap that this repair newly mis-documents and that should become its own G0 row.

## Required items

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | The job exists and finished with its marker | **PASS** | `sacct 40416578` = COMPLETED, ExitCode 0:0, elapsed 00:01:56. Log `/rs/rs_grp_oschome/go2432/tmp/rxlists_40416578.out` ends `REALXRAY_LIST_AUDIT_DONE arms=7 dirty=1 leaks=0`. Predecessors 40416536 and 40416560 also COMPLETED, and both are recorded in `SchwingNet/results/JOBS_data_repairs.txt` (lines 51, 288, 295) with the crash cause stated rather than hidden. |
| 2 | Outputs where claimed, at the size/count claimed | **PASS** | Grid `/rs/rs_grp_oschome/go2432/tmp/realxray_lists_audit.json` = 25,926 B, written 02:55. Local copy `SchwingNet/results/realxray_lists_audit.json` parses and carries all 7 arms. 7 run directories under `~/spine-detector/runs/realxray` = 7 arms in the report. 9 bank directories hold a `data.yaml`; all 9 are classified in the registry. |
| 3 | The fix does what it claims (read the code, not the summary) | **PASS** | `git diff HEAD -- tools/realxray_train.py` shows the name test `if "smoke" in ds.name or ds.name.endswith("_multi")` *replaced* by a registry lookup that appends to `unregistered` and raises `SystemExit` after the loop, naming every unclassified directory. `assert_disjoint()` reads case ids off disk and is called in the `pooled`/`coco` **and** the `lodo:` branch. `case_ids()` iterates `SPLIT_KEYS` only and raises on a non-string element. `check` is a real subcommand, not a docstring. 10/10 tests pass locally: `REALXRAY_BANKS_TEST PASS failures=0`, including `t_unregistered_bank_is_refused`, `t_two_devices_sharing_a_case_are_refused`, `t_case_ids_reads_only_the_split_keys`. |
| 4 | Nothing else broken | **PASS (with note)** | The diff is additive. The `if n["train"] > 0` gate is **pre-existing and unchanged**, so no bank newly disappeared. `git status` shows 15 modified tracked files, but only `tools/realxray_train.py`, `tools/data_lineage.py`, `docs/DATA_COMPLETENESS_AUDIT.md` and `JOBS_data_repairs.txt` belong to this repair; the other 11 are other agents' rows. Nothing under `SchwingNet/main.tex`, `sections/`, `tables/` or `figures/` was touched. Note: `include_derived=…endswith("_multi")` became `only=<bank>`, which narrows the *scoring* list of an `only:` arm (it no longer scores the three derived COBRA banks). Train directories are unchanged, so `rx_only_carmlspine_multi_1024`'s training is unaffected; only its redundant extra score cells would vanish on a re-run, and no paper number reads them. |
| 5 | The audit document was updated | **PASS (with note)** | `docs/DATA_COMPLETENESS_AUDIT.md`, section "2026-09-23 — COBRA counted up to four times in one detector arm (jobs 40416536, 40416560, 40416578)" at line ~1119, under the `## Repairs` heading at line 969, carrying the date, the job ids, the per-arm table and a "How it will be verified" block. Note: the file now has **two** `## Repairs` headings (969 and 1241); the second belongs to the TotalSegmentator repair, not this one. Worth collapsing before the document is read end to end. |
| 6 | No identifier leaked | **PASS** | `realxray_lists_audit.json` contains 148 C-ArmLSpine ids of the form `case1`…`case148` — the public release labels already used openly in this same audit document (case118, case134) — and no DICOM PatientID, no `case134/ori` export, no raw header string. The audit job is read-only: it opens no image, writes no bank, touches no label, and reorients nothing. |

## Headline numbers, reproduced independently

Every arithmetic relation in the report closes exactly against the grid census:

- COBRA train images `2640 + 1238 + 2568 + 1207 = 7,653` — the figure in the `ready()` docstring, correct and correctly scoped to COBRA (it is not the arm total, and does not contradict 8,101).
- Arm total `7,653 + 210 (carmlspine) + 238 (deepfluoro) = 8,101` train images.
- Distinct frames `2,640 + 210 + 238 = 3,088`.
- Duplicates `8,101 − 3,088 = 5,013`.
- Byte-identical `1,238 (ap45) + 1,207 (v2_ap45) = 2,445` — exactly the two symlink banks, which is what a `realpath` collapse must yield and is therefore a check on the method, not just on the number.
- The four COBRA `splits.json` all md5 `d2ad1ad23e4d006873f1ee26719c58f9`, verified on the grid.
- `check` prints devices `[carmlspine, cobra_elekta, deepfluoro]`, cases `148 / 145 / 6`, verdict PASS.
- The six other arms carry `0 duplicate`, read off their own `data.yaml`.

**"Not a leak" is measured, not asserted.** `audit_realxray_lists.py` computes `shared_cases` between
each arm's train and val lists and accumulates `leaks`; `leaks=0` is an output, not a constant. The
census also keys frames by `(root_bank, stem)` and resolves `realpath` separately, so the duplicate
count is checked against something outside the registry — and the marker files `subset.json` /
`rewindow.json` give it a second, independent parent chain.

**"No reported number is affected" holds.** Every detector weight cited in `SchwingNet/` resolves to
`rx_lodo_carmlspine_1024` (NUMBERS.md 109/113, atlas/model.json 117/121, atlas/dataset.json 160/199,
atlas/README.md, COUNTING_CHECK.md, COUPLING.md, results/counting/*.json), `rx_lodo_cobra_elekta_1024`,
`rx_lodo_deepfluoro_1024` or `rx_pooled_1024` — all four CLEAN in the census. A repo-wide grep for
`init18` finds it in no results file; its only prose mention is `docs/HANDOFF_2026-09-21_PM.md:563`,
exactly as reported. The scored-four-times finding is confirmed in the log line
`ONE TEST SET SCORED 4 TIMES: cobra_elekta/test through [cobra_elekta, cobra_elekta_ap45, cobra_elekta_v2, cobra_elekta_v2_ap45]`.

**The disclosed secondary defect is real.** `cobra_elekta_v2_ap45/subset.json` records
`{"from_dataset": "cobra_elekta_v2", "max_deg_from_ap": 45.0, "frames": {"train": 1238, …}}` while
`ls images/train | wc -l` = **1,207** on the grid. Confirmed, and correctly left to the COBRA row owner.

## Defects found by this check (none blocking)

**A. The `geneva_hip` registry note is false about the code, and it hides a real gap.** The note reads
*"ready() lists it but arm_sets gives it no train dir"*. `ready()` ends with `if n["train"] > 0`, and
`geneva_hip` is `train/val/test 0/0/116`, so it is **not in `avail` at all** — it appears in no arm's
train list *and in no arm's scoring list*. A fourth independent device (Philips BV Pulsera image
intensifier, 116 test frames) is currently invisible to every trained arm. The behaviour is
pre-existing and is not a regression; the wrong sentence is new, and it is exactly the sentence that
stops the next person looking. **Recommend:** correct the note, and raise the unscored 116-frame
device as its own G0 row.

**B. The `carmlspine` registry note says "149 cases".** The bank's `splits.json` on the grid is
`105 + 15 + 28 = 148`, and `check` prints 148. 149 is the released count before the one failed
conversion. Ambiguous as written, in a file whose purpose is to be the one place that says what a bank is.

**C. A residual hole the repair does not close.** `assert_disjoint()` keys on case id only. A
genuinely derived bank registered as `role: device` whose cases were *renamed* during export would
pass both the registry and the disjointness check. The frame-level `(root_bank, stem)` identity used
by `audit_realxray_lists.py` would catch it; `realxray_train.py` does not use that identity.

**D. `data_lineage.realxray_root_bank()` fails OPEN, where `ready()` fails closed.** Its
`except Exception: _cache["_"] = {}` means an unreadable, renamed or moved `realxray_banks.json`
silently reverts every lookup to the directory name — that is, silently restores the exact
10,228-vs-3,480 defect just repaired. One line (re-raise, or a sentinel that makes the section refuse)
would close it, and would match the reasoning given for the registry itself.

**E. The fail-closed claim is narrower than stated.** `ready()` globs `*/data.yaml`, so the four
directories under `realxray/` that carry no `data.yaml` — `carmlspine_crops`, `carmlspine_cv`,
`carmlspine_cvday`, `pelvis_landmarks` — are never tested against the registry. Correct for training
(a bank with no `data.yaml` cannot be trained on), but "ready() REFUSES a directory under realxray/
that has no entry in it" is true only of directories that carry a `data.yaml`.

## Handoff carried forward (G4, vertebral-body boxes)

The report's handoff is correct and is now enforced by the code: when the SPINEPS vertebral-body
masks force a re-export of the realxray banks, each new bank directory needs a line in
`tools/realxray_banks.json` or `ready()` refuses it **by name**. That refusal is the designed
behaviour, not a breakage. `docs/DATA_COMPLETENESS_AUDIT.md:1244` independently places the SPINEPS
masks on the critical path of A28 and gate G4 for the same reason.

The repair holds when a re-run after the full COBRA re-export prints `dirty=0` for every arm trained
from that point, and it fails loudly the first time a new bank appears under `realxray/` without a
line in the registry.
