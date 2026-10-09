# COBRA2026 Varian axis map — adversarial check

Verified 2026-09-23 ~03:30 EDT from the files and the grid, not from the report. Every number below was
recomputed from the raw per-map `scores` arrays in `/rs/rs_grp_oschome/go2432/data/cobra2026/varian/geom/*.json`,
not read out of the tool's own verdict fields.

**Verdict: the geometry answer is CONFIRMED and is the strongest part of this repair. The repair as a whole is
NOT finished: the job the verification criterion names has not run, the export still refuses every Varian case,
and three quoted ranges are narrower than the data they come from.**

---

## PASS

**P1. The map itself — CONFIRMED, independently recomputed.**
43 case files on disk (41 Varian, 2 Elekta controls). Ranking the 16 candidates myself by `edge_sim`:

| | winner | n |
|---|---|---|
| Varian (centres F, G) | `[[1,0,0],[0,0,-1],[0,-1,0]]` | 41 / 41 |
| Elekta controls A002, A004 | `[[0,1,0],[0,0,-1],[1,0,0]]` (MAP0) | 2 / 2 |

Zero errors, zero exclusions. Ranking instead by `edge_real` gives the **same winner on all 43** — 0 cases where
the two targets disagree. Winner `edge_sim` 0.9127–0.985, `log_sim` 0.9655–0.9984; smallest sim margin over the
runner-up 0.1932, i.e. every case clears the stated 0.10 by a factor of ~2 or better. The positive control is
real: the identical procedure returns a *different* map for the Elekta cases.

**P2. The 90° reading — exact, not approximate.**
`V·E⁻¹ = [[0,0,1],[0,1,0],[-1,0,0]]`, determinant **+1**, trace 1, rotation angle **90.000°**, eigenvector for
λ=1 is **(0,1,0)** — the RTK rotation axis. Both maps have determinant −1. The claim holds literally.

**P3. The convention is checked before the search, and the check is in the code.**
`check_rtk_convention` (tools/cobra_varian_geometry.py:136) solves each matrix's camera centre and requires it at
`SID·(sin g, 0, cos g)`; `solve_case` returns `status: excluded` with a reason if it fails (lines 218–223).
`source_at_sid_sin_cos: true` on 43/43, `max_source_error_mm 0.0` on all. (Caveat in N1.)

**P4. The criterion fix is a measurement and is really in the code, not a relaxed threshold.**
Lines 253–258 compute `RX.exposed_rows(...)` per probe frame; both score calls pass `bands[k]`. Lines 296–314
implement exactly the stated rule: sim decides by `--margin`, `agree` requires the real frames to rank the same
map first, real margin is recorded but not gating. `RX.ncc_pair(..., rows=)` and `RX.exposed_rows` already
existed in `tools/realxray_cobra_export.py` (lines 160, 181, file unmodified since 2026-09-21) — so the Elekta
path did band this way already, as claimed, and the re-run will not crash on a missing function.

**P5. Job 40416618's numbers reproduce exactly.** From `geom/F011_confirm.json`, winner by block size:
`edge_real` 0.164 / 0.193 / 0.234 whole frame vs `edge_real_banded` **0.598 / 0.721 / 0.810** at down 4 / 8 / 16;
runner-up banded 0.155 / 0.243 / 0.418. F010 (PaxScan, `exposed_rows` = [0, 768], i.e. no blades) 0.613 → 0.735,
runner-up 0.238 → 0.437. The report's "runner-up stays at 0.418" is the down-16 banded figure — the runner-up in
fact *rises* from 0.155 to 0.418 with block size; the separation still holds, the wording does not.

**P6. NIfTI conversion — done, and the round trip is actually asserted.**
101 files, 5.1 GB, `VARIAN_NIFTI_DONE` on every shard, `VNIFTI_RC=0`, job 40416564 COMPLETED. `cmd_nifti`
(line 375–380) re-reads each output and raises if origin, spacing, direction or size moved, and deletes the bad
file. SimpleITK read→write, no `as_closest_canonical`, nothing reoriented. `tools/body_masks.py` likewise writes
on the instance's own affine (line 55) and documents the rule.

**P7. Scope discipline.** `cobra_varian_spineps.sh` → `/rs/.../spineps/cobra_varian`, `cobra_varian_bodies.sh` →
`/rs/.../spineps/bodies_cobra`; job 40416510's `bodies` and job 40416509's `ctsp` are untouched. Both scripts are
resumable and log a marker with a count (`VBODIES_RC`, `VGEOM_RC`, `VARIAN_NIFTI_DONE`). All do-not-touch jobs
alive and unmodified: 40416315 R, 40416316 PD, 40416509 R, 40416510 PD, 40416378 R. Commits 4e53dc9 / 10e828e
touch no `main.tex`, `sections/`, `tables/` or `figures/`.

**P8. Documentation.** `docs/DATA_COMPLETENESS_AUDIT.md` carries the dated Repairs entry (line 1392) naming the
jobs and how to verify; `SchwingNet/results/JOBS_data_repairs.txt` was appended, not rewritten. No PatientID or
any patient field appears in any geom JSON, preview, audit line or commit — the JSONs carry only the dataset case
id, the imaging chain and geometry.

**P9. `varian_halcyon.json` — the "noticed, not repaired" item is real.** Read on the grid: `pixel_pitch_mm`
0.388, `panel_mm` [298, 397.3], `image_size` [768, 1024] (the PaxScan) against `SID_mm: 1540` (the RTI8643iL's;
the PaxScan cases report SDD 1500 in their own headers). `orientation_convention` still reads "the patient→RTK
map settled on Elekta is used first". Both halves of the claim check out.

---

## FAIL / NOT YET TRUE

**F1. The stated verification marker does not exist, and cannot yet.**
`40416639` is **PENDING**, `Reason=Dependency, afterany:40416546_*(unfulfilled)`; 40416546 is still **RUNNING**
(12/12 shards). No `VARIAN_GEOM_DONE solved=N` has been emitted by any job. `VARIAN_GEOMETRY.json` does not exist
anywhere under `/rs/.../cobra2026/varian/`. It is also not written by the geom job at all — `cmd_report`
(line 604) writes it and runs only under `slurm/cobra_varian_proof.sh` (40416620 / 40416642), so the stated
criterion conflates two jobs and will not be satisfiable until the proof job runs *after* the re-run.

**F2. Every number in the report was produced under the criterion the report says was wrong.**
None of the 43 geom JSONs contains the `criterion` or `exposed_rows` keys the corrected code writes, and 15 of
43 still carry `status: "unsolved"` with the old reason string ("no map wins on the real frames by 0.1"),
including cases whose sim margin is 0.78 and whose two targets agree (F009). So nothing on disk has yet been
scored under the rule the repair claims to have adopted. The *map* is unaffected — it is decided by the
simulation target, which did not change, and it is unanimous under both rankings (P1) — but the solved/unsolved
counts, and any "0 errors, N solved" statement, are not yet evidence for the new rule.

**F3. The gap in the audit row is not closed. `realxray_cobra_export.py` is unmodified.**
Line 286 still returns `manufacturer Varian: Varian geometry not solved (out of scope)`; line 296 still returns
`anisotropic detector pixels`. Nothing in the repo reads `VARIAN_GEOMETRY.json` or the solved `axis_map`; the
export still hard-codes `MAP0` (lines 345, 490, 635). The audited row — *"225 public, 0 exported, 0 in any
model"* — is still literally true. The audit entry says the exclusion "must go" but stops short of saying the
row remains open; it should say so.

**F4. `ImagerSizeX over the 225 public cases: 122 / 26 / 77` is not reproducible from anything on disk.**
`metadata.yaml` exists for **156** of the 225 F/G cases (the COBRA fetch, 40416315, is still running), and the
on-disk distribution is **83 / 26 / 47**. No file under `/rs/.../cobra2026/` carries `ImagerSizeX` for all 225,
and the overviews archive holds PNGs only (0 metadata.yaml). The "225" itself does check out
(`centre_F_cases_full.txt` 92 + `centre_G_cases_full.txt` 133 after their header lines). The derived
"4:1 pixels on 103 of 225 cases" inherits the same problem. This is precisely the project's named failure
mode — a plausible number with nothing outside the computation holding it up. Either name the source or restate
it as 83 / 26 / 47 of the 156 fetched so far.

**F5. Coverage is 99 of 225, and the case list is frozen while the fetch is still running.**
`varian_cases.txt` has 101 lines = **99 Varian + A002 + A004**, so "all 101 Varian planning CTs" and
"101 cases queued" overstate by two; the two Elekta controls are also being handed to SPINEPS in
`cobra_varian_spineps.sh` (it globs the nifti dir), although they already have SPINEPS under
`cobra2026/seg/spineps` (146 distinct case ids, verified). Meanwhile **155** F/G case directories are already on
disk, 153 with `ct_def.mha` + `geometry.xml` + `projections.mha` complete; **56** complete-or-nearly-complete
Varian cases are not in the list. 40416639, 40416565, 40416566 and the proof job all read that same frozen file
and nothing regenerates it. The list must be rebuilt and the chain resubmitted after 40416315 finishes, or this
repair silently settles for 99 of 225 — a download snapshot used as a criterion.

**F6. Three quoted ranges are narrower than the data.**

| quoted | report | audit | actual over 41 Varian cases |
|---|---|---|---|
| Elekta map's rank on the real frames | 5th–14th of 16 | 5th–14th | **5th–16th** (rank 16 on 2 cases, 15 on 3) |
| winner edge NCC vs the authors' sim | 0.93–0.985 | 0.93–0.97 | **0.9127**–0.985 |
| runner-up edge NCC vs the authors' sim | 0.25–0.57 | 0.29–0.55 | 0.191–**0.7756** (F015) |

The conclusion survives all three (min margin 0.1932), and the rank error runs in the repair's favour. But F015's
runner-up at 0.776 is the one case a reader would want named, and it is the one omitted — the same selective-range
pattern the rigor audit already flagged twice.

**F7. `agree_on_both_targets == solved` is near-tautological and is not a test.**
`cmd_report` (line 592) counts `two_targets_agree` over the `ok` records only, and `solve_case` sets
`status: unsolved` whenever the targets disagree. For any case with a `projections_simulated.mha`, the equality is
enforced by construction and can never fail. It is a useful invariant, not evidence. The real evidence is the
per-case recomputation in P1 — keep that, and state the criterion as "the map histogram holds one map and no case
is `unsolved` for disagreement".

**F8. The picture does not separate the maps at every frame, and the anisotropic proof on disk is unreadable.**
I looked at three of the proof images rather than trusting the description.
- `A002_0089_bone.png` (Elekta control, near-AP): the winner's red contour sits on the sacrum, pelvic brim, iliac
  crests and both femoral heads — **and so does the runner-up's cyan contour**, near-indistinguishably. That is
  physically expected on a near-symmetric AP pelvis, but it means "the runner-up runs through soft tissue" holds
  only at the obliques the report names, and should say so.
- `F010_0224_bone.png` (PaxScan): winner traces femoral head, neck, trochanter and the pelvic outline and sits on
  them; the runner-up differs, but modestly at this frame.
- `F017_0203_bone.png` (RTI8643iL): written at the native 4:1 pixel aspect, 3072 × 192 — a letterbox in which no
  anatomy is judgeable. `cmd_bone` has no isotropic rescale, so the "rescaled to isotropic mm" image the report
  describes for F017 is **not** what the committed tool produces. Add the rescale to `cmd_bone`, or the wide-chain
  picture cannot be checked by anyone else.

---

## NOTES

**N1.** `check_rtk_convention` returns `max_source_error_mm 0.0` on all 43 cases, both vendors. It confirms the
file is IEC/RTK, but with an error that small it is confirming a convention the file was written in, so it cannot
fail in practice and should not be described as a filter that rejected anything.

**N2.** `CP.signed_perms()` enumerates **16 of the 48** signed permutations, pinning patient z onto the RTK
rotation axis (cobra_pairs.py:104–115). Documented, and the winner's 0.91–0.985 NCC against the authors' own DRR
is external evidence that the right family was searched — but a setup whose long axis is off the rotation axis is
outside the search by construction, and the search alone would not say so.

**N3.** The exposed band is taken from the *real* frame and then applied to the *simulated*-frame score as well.
Harmless, but the re-run's sim numbers will not equal the ones quoted here or in the audit.

**N4.** PaxScan frame count quoted as "~894"; 4 of the 11 PaxScan cases scored so far report 500 projections.
RTI4343iL quoted "~499"; two cases report 884/885. The three chains themselves are solidly confirmed by three
independent fields (`.mha` spacing, `metadata.yaml`, detector model name) — it is only the frame counts that are
one-chain-one-number when they are not.

**N5.** Commit 4e53dc9 also carries `docs/DATASHEET.md`, `docs/MANIFEST_DATA_MODELS_RESULTS.md` and
`tools/film_corpus_inventory.py` — outside this repair, none on the do-not-touch list, but not mentioned in the
report.

---

## What would close this

1. Let 40416546 finish, confirm `VARIAN_GEOM_DONE solved=N` in `vgeom_40416639_*.out`, then run the report job and
   check `VARIAN_GEOMETRY.json` holds one map, zero disagreement-unsolved, and the two Elekta controls on MAP0.
2. Rebuild `varian_cases.txt` from disk after 40416315 finishes and rerun the chain — 225, not 99.
3. Wire the solved map into `realxray_cobra_export.py` (drop the manufacturer refusal and the anisotropic
   exclusion, resample x and y separately) or the audited row stays open.
4. Restate 122 / 26 / 77 with its source, or as 83 / 26 / 47 of 156.
5. Widen the three quoted ranges to their actual extremes and name F015.
6. Add an isotropic rescale to `cmd_bone` and re-emit the wide-chain proof.
