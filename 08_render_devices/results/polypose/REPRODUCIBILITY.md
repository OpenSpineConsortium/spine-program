# PolyPose bank — the reproducibility frame

What is pinned, what is hashed, what refuses to run, and how any single output is regenerated alone.
Written before any volume is made (Task C of the PolyPose program, 2026-09-23), because three estimators in this
project have produced finite, plausible, wrong numbers without raising, and a generator of warped CTs is that
same risk with more zeros on it. The method is published, not ours: PolyPose (Gopalakrishnan, Dey, Golland,
NeurIPS 2025; arXiv:2505.19256; github.com/eigenvivek/polypose, MIT) supplies the polyrigid, fold-free transform;
ours is only the sampling model (`SchwingNet/results/polypose/sampling_spec.json`), the junction rules and the
checks, and this file records how those are held to account.

## The pieces, and what refuses what

| piece | file | refuses |
|---|---|---|
| manifest schema + validator | `tools/polypose_manifest.py` | any row missing a field of the contract; a profile outside the reference envelope; a seed that is not the policy hash; a tolerance looser than the ceilings (PI 0.5°, Dice 0.98, folds 0.0) |
| invariant checker | `tools/polypose_invariants.py` | any output whose bytes, geometry or angles disagree with its row; a checker that has not just passed its own self-test |
| self-test | `polypose_invariants.py --self-test` | itself: builds a phantom, warps it, requires every check to pass, then injects a fold, a moved fused junction, a shifted pelvis, a tilted sacrum, an over-ROM request, an out-of-envelope profile, a tampered file and a wrong seed, and exits non-zero if ANY fault goes uncaught |
| bank check | `slurm/polypose_check.sh`, `make polypose-check` | the whole bank, re-validated from disk: self-test → manifest validate → per-row invariants (sharded) → merge; a missing shard is a failure, not a silence |
| corpus census | `tools/data_ledger.py` (v2), `tools/data_manifest.py` | nothing — it counts; but every generated volume enters it under its SOURCE patient key with `origin: "polypose"`, so the split builder and the leakage audit see the source person, never a new patient |

The self-test has already paid for itself twice: the checker's first version failed its own clean phantom on
four checks and missed two faults; the second (2026-09-23) failed it on five — boundary resampling deleted the
edge slice of every mask touching the volume face, the rigidity pose read two digitisations' moment noise as a
1.5° pose error, the box sacrum's moment frame was degenerate, and the requested kyphosis delta sat below the
plate fit's own resolution — and crashed on the out-of-envelope scenario. `polypose-invariants/3` is the first
version whose clean phantom passes every check and whose eight injected faults are all caught by their named
checks. That history is why `slurm/polypose_check.sh` refuses to certify anything until the self-test passes on
the node it runs on.

## Seed policy

`seed = int.from_bytes(sha256("polypose|<collection>|<case>|<variant_index>")[:8], "big") & (2^63 - 1)`
(`polypose_manifest.seed_for`; printed by `python tools/polypose_manifest.py seed --collection ctsp --case 0244
--variant 3`). A pure function of the source case and the variant index: any single row regenerates alone,
without its neighbours, on any node, on any day. Python's builtin `hash()` is salted per process and is never
used. The sampler version is recorded BESIDE the seed, not folded into it — a sampler change is a new bank,
stated as such, never a silently different draw. The invariant checker re-derives the seed from the row's own
(collection, case, variant_index) and fails the row if the stored seed differs (`seed_policy` check).

## Environment policy — what is pinned

Built once by `slurm/polypose_setup.sh` (grid job; the 2.0 GB pinned container exists at
`/rs/rs_grp_oschome/go2432/data/polypose/sif/`), and every piece is recorded:

- **Container**: `docker://nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04` pulled to a SIF whose sha256 is
  recorded in the env export. Needed because the grid nodes are CentOS 7 / glibc 2.17 and seven of the locked
  wheels require glibc ≥ 2.24; the environment is built INSIDE the container from the upstream lock.
- **PolyPose**: cloned at a pinned commit (recorded per row in `row.polypose.commit`); its `uv.lock` is the
  package authority — every version comes from it, including the `xvr` pin
  (`3e0b26eb51ef4a9c37615611bb05e0e200e48092`); the lock's sha256 is logged by the setup job.
- **Exports** (written to `slurm/env/` on the grid by the setup job): `polypose.yml` (conda-format view),
  `polypose.requirements.lock.txt` (authoritative, with hashes), `polypose.freeze.txt`, and `ENV_HASH` =
  sha256(freeze + SIF sha256). The env hash is the one number that says "same environment".
- **Per row**: `row.environment.fingerprint` = sha256 over interpreter, platform, every installed
  distribution, torch/CUDA build and the PolyPose commit (`polypose_manifest.environment_fingerprint`) — not a
  lock, but enough to say whether two rows were made in the same environment; plus the container image and its
  sha256, or the stated reason there is none.
- **No network at run time.** The setup job is the only fetch. Generation and checking read only: the source
  CT/label/body mask (sha256 in the row), `docs/polypose_segmental_rom.csv` and
  `docs/polypose_reference_envelope.json` (sha256 of both in the row), the flag table
  (`lstv_flag_labels_v2.csv`, sha256 in the row), and the container.
- **ostk** (OpenSpineToolkit) measures every angle. It is NOT in the grid's spineps env; the job scripts put
  `~/OpenSpineToolkit` on `PYTHONPATH`, and a missing ostk makes the angle checks FAIL, not skip.

## What is hashed

Per row (`polypose_manifest.py schema` prints the full field table): sha256 of the source CT, source label,
source body mask; sha256 of the output CT, output label, output body mask and the displacement field; sha256 of
the ROM table, the reference envelope and the flag table the junction rule was read from; the environment
fingerprint; the PolyPose commit and the sampler commit. `sha256_match` re-hashes source and outputs against the
row on every bank check, so a re-gzipped, repaired or tampered file cannot keep its certification.

## How a single row is regenerated alone

1. `python tools/polypose_manifest.py seed --collection <c> --case <id> --variant <k>` — the row_id and the seed.
2. `python tools/polypose_sample.py draw --case <id> --variant <k>` — the whole sampling block (profile drawn
   jointly from the spec, junction rule from the flag table, per-segment deltas), deterministic in
   (collection, case, variant_index). Same spec sha + same seed → the same numbers, bit for bit.
3. The generator applies exactly `row.applied_transforms` through the PolyPose transform at
   `row.polypose.commit` inside the pinned container, writing CT, label, body mask and field.
4. `python tools/polypose_invariants.py row --row <row.json>` — every invariant on the regenerated bytes.
5. The regenerated outputs' sha256 must equal the manifest row's when the ENV_HASH matches. Under a different
   environment the float path may differ; then the invariants, the re-measured angles and the transforms are
   the identity of the row, and the hashes are re-recorded with the new fingerprint — which is a new bank.

Neighbouring rows are untouched throughout: nothing about row k reads row k−1.

## The junction rule (never relaxed)

A junction the source's own read calls fused — Castellvi III or IV, any stated sacralisation/fusion — is ONE
rigid body: zero relative motion, checked three ways (the manifest transforms at 1e-6; the masks' moment poses;
the end-plate angle at ≤ 0.25° or the plates' own angular resolution). Castellvi I/II are mobile. The rule is
derived from the anomaly table's words by `junction_rule_for`, the reason is written into the row, and the
`config=fused` acquisition column is never read (it means fused SERIES, not a fused junction).

## The census hook

`tools/polypose_manifest.py sidecars` writes one ann JSON per output file stem; `tools/data_ledger.py` (v2)
takes `patient_key` from that ann VERBATIM (rule `ann:verbatim` — regexing 'ctsp_release/0244' through the stem
rules would rename it into a namespace that joins to nobody) and carries the new `origin` column
("acquired" for everything a scanner saw; "polypose" here). The summary prints and stores `records_by_origin`,
and `tools/data_manifest.py` counts the bank as a root. A volume with no sidecar shows up as a no-patient-key
record in `nulls_by_root`, which is the alarm: the generator writes the sidecar in the same transaction as the
volume.

## What this frame does NOT yet cover (stated, not guessed)

- The generator itself (the code that applies the sampled transforms with PolyPose and writes volumes) is the
  generation stage's deliverable; this frame is what it must satisfy before its first volume is kept.
- `profile_in_envelope` currently carries one UNVERIFIED bound (`roussouly_type_by_ss` in
  `docs/polypose_reference_envelope.json`); the check runs and the row records the bound's status. Verify the
  bound against its source before the production bank.
- Windows/dev runs of the tools use the local interpreter, not the container; they are for the self-test and
  the validator only. Nothing generated outside the container enters the bank.

## Status of the frame (2026-09-23, verified by running, not by reading)

- Self-test, local (Python 3.12.4, Windows dev): **PASS**, exit 0, 615 s — every check passes the clean
  phantom, all eight injected faults (fold, moved fused junction, shifted pelvis, tilted sacrum, over-ROM,
  out-of-envelope profile, tampered file, wrong seed) caught by their named checks.
- Self-test, grid compute node (spineps env + ostk, the environment `polypose_check.sh` certifies with):
  **PASS**, job 40424660 on hao1, 2026-09-23T21:24:44Z, ~4 min wall (`slurm/polypose_selftest.sh`,
  `make polypose-selftest-submit`; log `logs/ppselftest_40424660.out` on the grid). Each fault fails on
  exactly its named checks: fold→jacobian_positive; moved_fused→fused_junction_relative_pose (+field,
  rigidity); shifted_pelvis→pelvis_fixed + pelvic_incidence_invariant; tilted_sacrum→pelvis_fixed + PI;
  tampered→sha256_match; wrong_seed→seed_policy; bad_profile→profile_in_envelope.
- Envelope gate, run both ways: PI 50/PT 15/LL 55/TK 40 → `PROFILE_ACCEPTED`, exit 0; PI 80/PT 15/LL 40
  (PI−LL = 40) → `PROFILE_REJECTED` on pi_ll_mismatch, exit 1, every bound printed with its source.
- Junction rule: Castellvi III → `fused_zero_motion` with its reason; Castellvi II → `mobile`.
- Manifest validator: a complete example row → `MANIFEST_OK`, exit 0; the same row with `seed` deleted →
  `PROBLEM ... missing seed`, `MANIFEST_INVALID`, exit 1. The refusal is real, not documented-only.
- Seed policy: `seed --collection ctsp --case 0244 --variant 3` → `pp_ctsp_0244_v003`, 4088025815736193161,
  a pure function of its arguments.
- Grid copies of `polypose_invariants.py`, `polypose_manifest.py`, `polypose_check.sh` are sha256-identical
  to the committed local files (after CRLF strip).
- Census hook, end to end on a scratch bank (one 8³ volume + `sidecars` ann): the ledger records the file
  with `origin: polypose` and `patient_key: ctsp_release/0244` verbatim, 0 no-key records — and with the
  sidecar mislaid (not under `<bank>/ann/`) the same run raises the documented alarm: the record joins to
  nobody and the summary prints the no-key warning. Both behaviors observed, not inferred.
  Layout contract this fixes in words: `sidecars --out <bank>/ann`, volumes under `<bank>/volumes/`.

## Checker v4: what the first real CTs broke (2026-09-23, evening)

Every item below was invisible on the RAS-built phantom and surfaced on the first real, PIR-stored CTSpinoPelvic1K
volume (0874) during the generator smoke tests. Each was fixed at its cause, the self-test re-run to a pass
locally and on the grid node, and no check was loosened.

1. **The ROM table on the grid was stale.** Commit 1facf60 regenerated `docs/polypose_segmental_rom.csv` from the
   spec (T10-T11 3.5, T11-T12 5.1); the grid still held the older table, and the recorded grid self-test pass
   (40424660) ran against it. Against the current table the clean phantom's thoracic request (-4/-5 at
   rom_fraction 0.5) exceeded its own bound. The phantom now asks -2.4/-3.5 at the generator's rom_fraction 0.7,
   and every synced data file (ROM table, envelope, spec, flag table) is sha256-compared against the committed
   blob, not only the three code files.
2. **The checker measured with a second, never-validated path.** `measure()` fitted plates with raw ostk
   primitives on the array as stored, never canonicalised, with ostk's whole-sacrum S1 fallback. On 0874 it read
   PI 3.6 and LL -8.9 where the cohort path reads 53 and 54. It now delegates to
   `tools/polypose/measure_sagittal.measure_image` -- the cohort's path, which is what measure_sagittal's own
   docstring always said the checker should call.
3. **The S1 plate moved with L5.** The release isolates the S1 plate in the footprint of the lowest lumbar body.
   When L5 rotates 3 deg its footprint selects other sacral columns and the fitted plate tilts ~3 deg with the
   sacrum untouched (0874: re-measured PI 52.6 -> 55.2, SS 34.3 -> 37.1, pelvis Dice 1.000), contaminating LL and
   the junction angle by the same amount. A source/output pair now uses the SOURCE's lowest body as the corridor
   for both measurements (`s1_corridor_reference`); a single-volume measurement is unchanged.
4. **Field-of-view truncation.** A vertebra touching a face of the volume, or a label fragment under 25 % of the
   median vertebra, can no longer be a span endpoint (its "plate" is the FOV plane); label and body-mask voxel
   counts are compared with each label's RIGID TARGET (which carries the FOV cut), not the raw source count; a
   segment above the mobile range with no ROM row passes only with exactly zero motion requested and applied;
   `pullback_mask` uses the generator's boundary convention (-0.5 <= c < n - 0.5).
5. **Label debris.** A vertebra id under 200 voxels (0801 carries 3 voxels of L5 under a four-lumbar spine) is
   declared in `source.debris_ids`, moves with its nearest body, creates no motion segment, and the checker
   verifies each claimed id really is under 200 voxels.
6. **The self-test marker is keyed to the checker's bytes** (`selftest_<host>_<sha12>.ok`): a pass by an older
   checker version certifies nothing about a newer one.
