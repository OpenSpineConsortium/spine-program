# Adversarial check — CTSpinoPelvic1K record 0533 (truncated CT in the public release)

Checked 2026-09-23 from the grid and from the code, not from the report.
Verdict: **PASS on every substantive claim.** Four documentation/consistency defects and one
concurrency hazard are recorded below; none of them touches the repaired volume.

---

## 1. The job exists, ran, and left its marker — PASS

| Job | Script | `sacct` state | Marker found in `~/model_night/logs/` |
|---|---|---|---|
| 40416624 | `slurm/ctsp0533_repair.sh` | COMPLETED 0:0, 00:01:07 | `CTSP0533_REPAIR_RC=0 swapped=1 count=802` |
| 40416604 | `slurm/ctsp0533_bone_check.sh` | COMPLETED 0:0, 00:05:42 | `BONE_CHECK_DONE rows=11 controls=10 closest=v11_vertebrae_pct case_inside=True` |
| 40416617 | `slurm/ctsp0533_series_check.sh` | COMPLETED 0:0 | `SERIES_CHECK_0533 all_agree=True fields=7` |
| 40416626 | `slurm/ctsp0533_renders.sh` | COMPLETED 0:0, 00:01:14 | `CTSP0533_RENDERS_RC=0 ctsp_drr=802 anchor=7844 anchor_c2=6131 case0533_ann=1/2/2` |
| 40416625 | `slurm/ctsp0533_spineps.sh` | **PENDING (Resources)** | not yet |
| 40416627 | `slurm/ctsp0533_physics.sh` | **PENDING** | not yet |
| 40416638 | `slurm/ctsp0533_lstvflag.sh` | **PENDING** | not yet |

The report describes exactly this state (three GPU jobs queued behind the lcurve array and
`spineps_ctsp`). The failed earlier attempts it names (`CTSP0533_REPAIR_RC=3`, `RC=1`,
`CTSP0533_RENDERS_RC=4`) are all present in the logs, so the failures were not hidden.

## 2. The outputs are where the report says, at the size claimed — PASS

- `gzip -t ~/data/CTSpinoPelvic1K/ct/0533_ct.nii.gz` -> **clean**.
- `ls ~/data/CTSpinoPelvic1K/ct/*_ct.nii.gz | wc -l` -> **802**.
- The file is **250,067,995 B**, dated 23 Sep 03:03, mode 644 — matches the claim byte for byte.
- The truncated original is retained at
  `/rs/rs_grp_oschome/go2432/data/ctsp0533_repair/0533_ct.TRUNCATED.20e673dc6c2a.nii.gz`,
  **17,301,504 B**, original mtime 25 Jun preserved (`cp -p`).
- `logs/verify_0533.json` exists, `"all_pass": true`, **nine** gates, all `pass: true`.
- `logs/sha256_0533.txt`, `logs/bone_check_0533.json`, `logs/series_check_0533.json` all present.
- Render banks counted independently of the job's own report: `~/ctsp_drr/ann` **802**,
  `~/anchor_drr/ann` **7844**, `~/anchor_drr_c2/ann` **6131**. The 0533 entries exist:
  `ctsp_drr/ann/CTSP_COLONOG_378.json`, and `ctsp_0533_ap.json` + `ctsp_0533_lat.json` in both
  anchor banks (2 each, as claimed).
- Not yet on disk, consistent with the three PENDING jobs: no `0533` under
  `/rs/.../data/spineps/ctsp`, `/rs/.../data/spineps/bodies` is empty, `~/physics_drr/ann`
  has 0 `ctsp_0533_*`, `~/lstv_flag/renders` has 0. The report says so; it does not claim them.

## 3. The fix does what it claims — PASS (code read, not the summary)

`slurm/ctsp0533_repair.sh`:
- Downloads the SeriesInstanceUID that `manifest.json` gives for 0533 via the NBIA `getImage`
  API on a compute node, and re-tests the DICM magic at offset 128 on every file, so the
  LICENSE the zip ships beside the images cannot enter the conversion. 577 files, which is the
  slice dimension of the label.
- The dcm2niix selection actually **executes** each candidate and rejects a GLIBC link failure.
  The `works()` helper captures output first and then judges it, so the `set -o pipefail`
  inversion the report describes is genuinely fixed in the code, not just in the narrative.
- Rebuild runs the release's own `fetch_from_tcia.py`, with a pydicom + `reconstruct_ct.py`
  fallback. Resumable at every stage (DICOMs, conversion, rebuild), and an already-clean release
  file short-circuits to verify-only with `ALREADY=1`.
- **The swap is gated**: `mv -f` happens only when `VRC -eq 0 && ALREADY -eq 0`, after the old
  file is copied aside with its sha in the name. `cp` to a dotfile then `mv -f` on the same
  filesystem — genuinely atomic, no reader sees a half file. Both sha256s are appended (`>>`)
  to the log, not overwritten.

`tools/ctsp0533_verify.py` — the gate that decided it is sound and is **not** vacuous:
- `bone_fraction_matches_release` compares against `spine_bone_pct` restricted to the vertebra
  identifiers, with a 1.0-point tolerance, and prints the all-label figure beside it.
- I recomputed the control table from `bone_check_0533.json` myself. Per-record delta of
  `v11_vertebrae_pct` minus `manifest_spine_bone_pct` over the ten intact controls:
  0001 +0.25, 0005 +0.23, 0008 +0.20, 0010 +0.22, 0012 +0.27, 0014 +0.26, 0021 +0.25,
  0025 +0.25, 0027 **+0.12**, 0045 +0.23. **0533 rebuilt: +0.22.** Inside the range.
- This is a real external control, not a post-hoc rationalisation: the ten controls span
  manifest values 50.0 to 88.6, so reproducing a specific value to two-tenths of a point is not
  achievable by accident, and a wrong acquisition of the same patient would not sit on the label
  mask at all. The 1.0-point tolerance is about four times the observed control spread and would
  still reject the 9.4-point gap that the all-label figure produced.
- `n_voxels_fg` is advisory (a `[note]`), not a gate — as claimed. The defect is real: manifest
  2,094,598 against 3,167,246 in the released mask.
- The orientation gate confirms PIR on both sides; `affine_max_abs_diff` is exactly 0.0. Nothing
  was reoriented on write.

`tools/ctsp0533_series_check.py` reads and prints only scanner, acquisition and demographic
fields; its header states no patient identifier is read out or written, and the JSON on the grid
contains none.

## 4. Nothing else was broken — PASS

- `tools/make_anchor_drr.py` is the only shared tool this repair modified. The `--cases` flag is
  additive, and the write of `data.yaml` is now guarded by
  `if si == 0 and not (a.cases and (dst / "data.yaml").exists())`. Verified on the grid:
  `~/anchor_drr/data.yaml` is still dated **14 Sep 15:48** and all 22 original
  `build_stats_*.json` keep their September dates. The new stats went to a separate stem,
  `build_stats_ctsp_0_cases_0533.json`, in both anchor banks. The finished bank's record of how
  the other 801 were made is intact.
- `git status`: `SchwingNet/main.tex` is modified, but `git diff SchwingNet/main.tex` contains no
  `0533` and is +13 lines of another agent's work. `sections/`, `tables/`, `figures/` are
  untouched by this repair. The DO-NOT-TOUCH jobs (40416315/16, 40416509, 40416510, 40416378)
  are all still in their own states; 40416509 has 151 CTSP cases done and is still running.
- `docs/DATASHEET.md`, `docs/DATA_ACCOUNTING.md` and the memory note
  `grid-ct-0533-truncated.md` are corrected and now say "truncated in the public release, not
  locally". `SchwingNet/atlas/dataset.json` still carries three "truncated" mentions — the report
  declares this openly as left to the atlas workflow.

## 5. The audit document was updated — PASS

`docs/DATA_COMPLETENESS_AUDIT.md` carries a dated section under `## Repairs`
("2026-09-23 — CTSpinoPelvic1K record 0533, the truncated CT in the public release", around line
1322) naming all seven job ids, the work tree, the failed attempts, the sha pair, the gate that
failed first and why it was the gate, the second defect found and not repaired, the banks, how to
verify, and the un-run HF push. `SchwingNet/results/JOBS_data_repairs.txt` was appended to, not
rewritten. `KNOWN_ISSUES.md` section 10 exists in the deposit at
`CTSpinoPelvic1K-1/data/zenodo_deposit/KNOWN_ISSUES.md` and gives a consumer a one-command repair.

## 6. No identifier leaked — PASS

Grepped every script and tool this repair wrote for PatientID-shaped content and for the
`case134` / `ori` C-ArmLSpine tokens: nothing. The only identifier in the scripts is the TCIA
**SeriesInstanceUID** `1.3.6.1.4.1.9328.50.4.422576`, which is the public archive's own series key
and is already the value `manifest.json` publishes for this record; it appears in the private
repo's slurm script and in neither the audit nor `KNOWN_ISSUES.md`.

---

## Defects found in this repair

**D1 — FAIL (documentation). The audit misstates the control range.** The audit section says the
ten controls "reproduce it to between **+0.20 and +0.27** of a point". The actual range from
`bone_check_0533.json` is **+0.12 to +0.27** — record 0027 is +0.12. The report headline states
+0.12 to +0.27 correctly, so this is an inconsistency inside the repair's own paperwork, not a
claim that fails. It matters only because that sentence is the written justification for the
tolerance. One-word fix in `docs/DATA_COMPLETENESS_AUDIT.md`.

**D2 — concurrency hazard, not yet triggered.** `slurm/ctsp0533_spineps.sh` runs
`tools/body_masks.py --shard 0 --n-shards 1` over the *entire* SPINEPS CTSP directory, while the
DO-NOT-TOUCH array job **40416510** (8 shards) will do the same over the same output directory.
`body_masks.py` skips a case whose `<case>_body_msk.nii.gz` exists (line 93) but writes without a
tmp-then-rename, so two simultaneous runs on one case could leave a partial file that the other
run then skips as "done". Not triggered: `/rs/.../data/spineps/bodies` is empty and 40416510 is
PENDING. Worth narrowing the 0533 job to its one case, or giving `body_masks.py` an atomic write,
before both land on a GPU at once.

**D3 — minor, stale count.** The report says "SPINEPS has 131 of 802 done". At check time the
directory holds **151** completed cases (`grep -c seg-vert`). The job is running, so this is a
time-of-writing figure rather than an error, but it should not be quoted as a state.

**D4 — cosmetic.** The marker line reads `SERIES_CHECK_0533 all_agree=True fields=7` while the
report and audit say "all **eight** fields agree". Both are true — seven DICOM fields plus the
series identifier, which the JSON carries as a separate key `series_uid_matches_manifest`. The
marker and the prose should use the same number.

## One caveat on the strength of the identity evidence

The series check is weaker than it reads for the specific failure mode it is aimed at. It compares
the downloaded series against the manifest on manufacturer, model, kernel, slice thickness, kVp,
sex and age band — but the same patient's *other* acquisition would match most of those too, and
the series UID match is near-tautological because the UID is what was requested. The check that
actually discriminates is the bone fraction under the label mask, and it does discriminate: a
misaligned acquisition cannot sit under this label to 0.22 of a point. The report is right to lean
on the control table; the series table is corroboration, not proof.

## What is genuinely still open

1. **The public release is still broken.** `slurm/ctsp0533_hf_push.sh` is written, uploaded to the
   grid (`~/spinesurg-ct-nnunet/slurm/`, 2,596 B) and confirmed **not submitted** — no HF job
   appears in `sacct` for 2026-09-23. The script refuses unless the local sha256 is
   `478a74e9…a164d5` and `gzip -t` passes, and reads the object back to confirm the stored
   identifier is not `20e673dc…d6e23`. That refusal logic is correct as written. It needs Greg.
2. **The box convention is not yet satisfied for 0533.** Greg's directive is that boxes are
   vertebral **bodies**, via SPINEPS. The banks re-rendered here (`ctsp_drr`, `anchor_drr`,
   `anchor_drr_c2`) box whole vertebrae; the report states this plainly rather than claiming the
   directive is met. Job **40416625** is the one that satisfies it and is still PENDING. Until it
   lands, the body-box corpus covers 801 of 802 CTSP records, not 802.
3. `manifest.json`'s `n_voxels_fg` is broken for the whole release (0 in 340 of 802) and was not
   rebuilt. Correctly scoped out as a manifest regeneration.
4. The working tree is left dirty and uncommitted, by design, because parallel agents are
   appending to the same audit and jobs files.
