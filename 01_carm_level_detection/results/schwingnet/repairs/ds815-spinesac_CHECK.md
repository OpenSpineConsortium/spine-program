# Adversarial check — Dataset815 + SpineSAC revival

Checked 2026-09-23 from the files and the grid, not from the report. Commits `1f1abf1`, `f3f36e0` on `L6_Class`.

**Verdict: PASS with four corrections.** Every job, artifact, count and code change the report names is real and
independently reproduced. Two headline sentences overstate their evidence, one device claim is too strong, and one
stated blocker has since been cleared by a sibling job — so the "not_done" section is stale in the agent's favour.

---

## PASS

| # | Item | How it was checked | Result |
|---|---|---|---|
| 1 | SpineSAC fetch 5,492/5,492 | `wc -l file_list.txt` = 5492; `find drive -type f \| wc -l` = 5492; `find -size 0` returns exactly the two named files (`BMJH/SKANRAY/SCN 6/Output/AP/{DD/AP_icp_2D.txt,PD/AP_2D.txt}`); 3.9 GB on disk; `sacct` 40416585 COMPLETED 0:0; log ends `SPINESAC_FETCH_DONE` | PASS |
| 2 | Dataset815 census L6 = 68, T13 = 6, n = 1,176 | Recounted from the raw shards, not the summary: `cat flags_shard*.jsonl \| grep -c '"has_L6": true'` = **68**, `has_T13` = **6**, `wc -l` = **1176**. Matches `d815_repair.json` and the job log exactly | PASS |
| 3 | The eight misflagged cases | `d815_repair.json.flags_corrected` lists verse522/532/551/571/612/620 (L6 False→True) and verse582/601 (T13 False→True) — the named eight and no others | PASS |
| 4 | Outside check: 50 L6 + 6 T13 on the VerSeFusion side | Independent corroboration in memory `versefusion-t13-flag-wrong` ("manifest says 18, truth is 6 … six carry an L6"), written from the VerSe published table before this job ran | PASS |
| 5 | The resplit refused rather than wrote | `sacct` 40416581 **FAILED 4:0**; log ends `D815_RESPLIT_BLOCKED unreadable images 1 … ['COLONOG_378']` / `D815RESPLIT_RC=4`; `d815_repair.json` carries `"splits_written": false` with the reason. `splits_final.json` and `case_manifest.json` mtimes still **Sep 12 21:10** — untouched | PASS |
| 6 | Smoke test `SMOKE_OK failures=0` | 40416673 COMPLETED 0:0. Log shows body fraction **0.486–0.534** per vertebra on TS_s0001, sacrum fraction **1.000**, discs `[118,120,121,122,123,124,126]` dropped, and the grid guards (shape and affine mismatch both caught) | PASS |
| 7 | Chain 40416582 → 40416583 → 40416584, `afterany` | `squeue` dependency column reads `afterany:40416582_*` on `sac_bodies` and `afterany:40416583` on `sac_truthscore`. All three PENDING behind the GPU queue. A requeue cannot strand them | PASS |
| 8 | rc 4 / rc 5 guards are real | `slurm/spinesac_truth_score.sh` L31–35 exits **4** when `n_usable < 3` ("SPINEPS did not read the plastic phantom"); L47–51 exits **5** when `SAC_TRUTH_VALIDATED_IMAGES < 1` ("the shipped poses do not put the boxes on the bones"). Both print "that is a RESULT … report it and stop" | PASS |
| 9 | The bind tool does what the report says | Read `tools/spinesac_bind_bodies.py`: `vert = np.where(vi < DISC_MIN_ID, vi, 0)` (discs, id ≥ 100, dropped) → `body = np.where(np.isin(si, CORPUS), vert, 0)` (corpus 49/50) → `body = np.where(vert == SACRUM_ID, SACRUM_ID, body)` (sacrum whole). Reads with `nib.load`, writes `nib.Nifti1Image(body, ct_img.affine, hdr)`. **No `as_closest_canonical` anywhere**; `same_grid()` refuses on shape or affine mismatch; render axes from `nib.aff2axcodes`, not assumed | PASS |
| 10 | prep815 singularity pin | L46 `SINGULARITY="${SINGULARITY:-${HOME}/mambaforge/envs/nextflow/bin/singularity}"`, L99 refuses if not executable, L103 prints the version, L127 resume count. No bare `singularity` | PASS |
| 11 | The fetch fix is narrow | `_declared_empty()` returns true **only** when the Drive listing's own `size` field is 0, and all three call sites read `size > 0 or _declared_empty(entry)`. A truncated transfer of a real file still fails loudly | PASS |
| 12 | Grid code in sync, CRLF stripped | Local content md5 (CR-stripped) equals grid raw md5 for `spinesac_bind_bodies.py` (7cb4db9c…), `prep815.sh` (e4075802…), `spinesac_fetch.py` (d8f98133…). Grid copies are LF | PASS |
| 13 | Nothing else broken | `git show --stat` on both commits: 13 + 5 files, all under `tools/`, `slurm/`, `docs/DATA_COMPLETENESS_AUDIT.md`, `SchwingNet/results/JOBS_data_repairs.txt`. **`main.tex`, `sections/`, `tables/`, `figures/` untouched.** The concurrent manuscript edits visible in `git status` are other agents' and were not swept | PASS |
| 14 | Audit and JOBS updated | `docs/DATA_COMPLETENESS_AUDIT.md` L1491 `### 2026-09-23 — the two abandoned assets…`; the diff adds a `###` only, under the existing `## Repairs`. `JOBS_data_repairs.txt` appended, including the explicit `CORRECTION` block | PASS |
| 15 | No identifier leaked | The only matches in the two shared files (`case134`, a SeriesInstanceUID) are **pre-existing sibling-agent lines** — `git show 1f1abf1 f3f36e0 -- …JOBS…` adds none of them. No "origin" in either commit | PASS |
| 16 | Dataset815 adds no imaging | `nnunet/raw/Dataset815_SpineSurgLSTVVerSe/imagesTr` = 1,176 **symlinks**, e.g. `COLONOG_100_0000.nii.gz -> ~/data/CTSpinoPelvic1K/ct/0145_ct.nii.gz`. No claim in `SchwingNet/CLAIMS_LEDGER.md` mentions Dataset815 | PASS |
| 17 | Chain inputs exist | All three phantom CTs present: `or_ready/spinesac/ct/{set1_A,thancopen,closed_A}/ct.nii.gz` (98 MB / 234 MB / 63 MB). `--array=0-2`, shard 0 writes `cases.csv`, others wait up to 600 s. `A_thr150_sag.png` and the rest of `ct_probe/` are on disk as cited | PASS |
| 18 | 0533 sha256 equals the HF LFS oid | Confirmed at source, `ctsp_audit_40416363.out` L4–5: grid sha `20e673dc…` and `HF 0533: … size 17301504 lfs sha256 20e673dc…`. The diagnosis "the published release object is itself truncated" was **right**, and the sibling repair (C1) corroborates it by rebuilding from DICOM rather than re-fetching | PASS |

---

## CORRECTIONS

### C1 — FAIL (stale). CT 0533 was repaired 26 minutes before the report was written; the stated blocker is gone.

The report's `not_done` says Dataset815 is blocked on CT 0533 and lists two commands to run "once the CT-0533
repair concludes". It concluded at **03:03:54**, in sibling job **40416624**
(`~/model_night/logs/ctsp0533_repair_40416624.out`), while the census shards were still running:

- rebuilt from the 577 source DICOM files of the series with `dcm2niix` v1.0.20260416 — **not** from HF, and
  **not** the older-HF volume the report correctly rejected (that one is 276,534,068 B; this is 250,067,995 B);
- nine gates, `VERIFY_0533 all_pass=True gates=9 failed=[]`, including `shape_matches_label: CT (512, 577, 512)
  vs label (512, 577, 512)`, `orientation_matches_label: CT PIR vs label PIR (never reoriented on write)`,
  `affine_matches_label: max |delta| = 0.000e+00`;
- swapped into the release tree, the truncated original kept aside.

Verified on the live file rather than from that log: `~/data/CTSpinoPelvic1K/ct/0533_ct.nii.gz` is now
250,067,995 B, sha256 `478a74e9…`, mtime Sep 23 03:03, and **`gzip -t` is clean**. The `COLONOG_378` unreadable
finding was true when the shard read it and is now stale.

Consequence: the two finishing commands are runnable **now**, in order. `d815_resplit.sh` should be re-run rather
than trusted from cache — the cached flags remain valid (all 1,176 *labels* read fine; only the image gate
failed), but the integrity gate must pass against the new file before the folds are written.

    sbatch -D ~/spinesurg-ct-nnunet slurm/d815_resplit.sh
    sbatch -D ~/spinesurg-ct-nnunet slurm/prep815.sh

The public release is still broken until `slurm/ctsp0533_hf_push.sh` runs; that is the sibling's gap, not this one.

### C2 — PARTIAL. "sha256sum -c SHA256SUMS.txt passes 810/810" is not evidence about any CT.

`~/data/CTSpinoPelvic1K/SHA256SUMS.txt` has 810 lines and **zero of them are `ct/` files** (`grep -c "ct/"`
returns 0); it covers the labels and the top-level docs. Putting it in the same sentence as the 0533 CT checksum
invites the reader to think the CT tree was checksum-verified. It was not. The claim survives because the line
above it does the work — a direct grid-sha against HF-LFS-oid comparison — but this is the project's own failure
mode in miniature: a true number quoted beside a claim it does not support. **Recommend striking the 810/810
clause** from the JOBS block and the audit paragraph, or qualifying it as "labels and docs only".

### C3 — PARTIAL. "SimpleITK REFUSES SPINEPS masks" is overstated in the headline.

The smoke log reads `of 25 SPINEPS masks: SimpleITK opened 24, nibabel opened 25` — **1 of 25** refused, not all.
The commit message states this correctly; headline bullet 3 does not, and the capitalised "REFUSES" implies a
categorical failure. The remedy (read with nibabel, write on the CT's own affine) is still the right call — one
mask in twenty-five is enough to poison a run silently — but the claim should be stated as its own log states it.

### C4 — PARTIAL. The device-attribution finding is real but drawn too strongly.

The audit says "Three of the six device identities therefore rest on a directory name." The inventory contradicts
the *identities* half: `GE MEDICAL SYSTEMS` appears **116** times and `SKANRAY TECHNOLOGIES` **106** times in
`or_ready/spinesac/inventory.json`, and the sheets directory holds `raw_GEMEDICALSYSTEMS_FLUOROSTAR.png`,
`raw_SKANRAYTECHNOLOGIES_?.png` and `raw_ziehmimaging_ZiehmNetPort.png` — all three vendors **do** appear in
native DICOM headers somewhere in the corpus. What rests on the folder name is the **per-scenario** attribution
for the 36 processed-only scenarios, which is a narrower and still worth-reporting claim. Reword to that.

Also unreconciled: `grep -c "folder name only"` over `inventory.json` returns **37**, against the 36 in the audit
(23 + 36 = 59). One of the two is off by one; it cannot be settled from the login node.

---

## NOT YET VERIFIABLE

**The SpineSAC result itself.** 40416582/83/84 are all PENDING behind the 802-case CTSpinoPelvic1K SPINEPS array
(40416509, still RUNNING at about an hour). `or_ready/spinesac/` has no `truth/` directory yet, so
`truth/look/*.png` and `truth/overlays/` do not exist. The report says so plainly and claims no result. Correct as
written — the finding is pending, and under the rc 4 / rc 5 design a negative will be legible rather than silent.

## WORTH ACTING ON, BEYOND THIS REPAIR

Headline 4 is the most valuable thing here and is **unverified because nothing checks it**: `tools/body_masks.py`
applies the same `instance × corpus 49/50` rule to every CT (job 40416510), so any bank built that way is deleting
the sacrum and, if instance ids ≥ 100 survive, carrying intervertebral discs as levels. The smoke test proves the
mechanism on a real SPINEPS pair. It should be pointed at `body_masks.py` output before that bank is used for boxes.

## HOUSEKEEPING

`docs/DATA_COMPLETENESS_AUDIT.md` now has **two** `## Repairs` headings (L969 and L1256). Not caused by this
repair — its diff adds only a `###` — but a reader or a grep will land on the wrong one. Worth one agent merging them.
