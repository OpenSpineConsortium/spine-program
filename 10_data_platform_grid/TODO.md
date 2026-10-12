# TODO.md: what is not on the grid or not done, in order

Each step names its gate (what must be true before it counts as done), the pre-stated success number where one
exists, what it depends on, and who decides. Sources: `../_plan/PLAN.md` project 10 (steps 1 to 5),
`docs/handoff/OPEN_QUESTIONS.md` (OQ rows), `docs/handoff/extracts/RESEARCH_DIRECTIONS_sections.md` (RD),
`docs/handoff/RECIPES.md` sections 0 and 10, `docs/handoff/extracts/MANUSCRIPTS_sections.md` sections 16 and 21,
`code/data_platform/MIGRATION_PLAN.md` (MP), `code/data_platform/dedup/DEDUP_PLAN.md` (DDP), `code/data_platform/VERIFICATION.md`,
`code/data_platform/DATA_MANIFEST.md` section 10. Every grid command is an `sbatch` job; nothing runs on the login node.

## A. The first five steps (PLAN.md project 10; steps 1 to 3 run in week one)

| step | what | gate | pre-stated number | depends on | who decides |
|---|---|---|---|---|---|
| 1 | B04, B07 and B09 were copied, verified, cut over and finalized on 2026-10-11 (Greg's record, issue #49; `MANIFEST_GRID.md` section 2). What remains: bring the lines of `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/{B04,B07,B09}/STATUS` into this folder; run the smoke checks (MP section 4: after B04 `tools/xray_dataset_usage.py` in a job; after B07 `tools/data_manifest.py check` on the original manifest), place the README.yaml files and index the batches, unless a record shows they were done (none is in this folder) | every item VERIFIED or ABSENT with a written reason, recorded here; every cut-over path a symlink into Ceph; the grid `tools/realxray_banks.json` found to list `cobra_elekta_v3` and `cobra_elekta_g3test` or not (OQ B19) | 0 items RSYNC_FAILED, VERIFY_FAILED or DST_EXISTS | the three jobs: ended; the batches finalized 2026-10-11 | engineering |
| 2 | B05, B10 (64 single-source banks) and B11 (64 multi-source banks and the identity tables). State on 2026-10-12 (issue #65; `MANIFEST_GRID.md` section 2): B05 3/3 VERIFY_OK, cut over, finalized; B10 64/64, cut over, finalized; B11 64/64, cut over, finalize running at 03:30 EDT. Whether `/wsu/home/go/go24/go2432/{split_final.json, patient_keys*.json, bank_splits.json}` were first backed up to `/rs/rs_grp_oschome/go2432/data/multisource_banks/identity_backup_<date>/` with their SHA-256 is not recorded | STATUS VERIFIED with measured sizes, the lines recorded here; the backups' SHA-256 recorded in this file; `tools/holdout.py` still raises on an unreadable bank; `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` never rebuilt in place (`slurm/allspine_v9_bank.sh` line 21 `rm -rf`) | 128 items VERIFIED or ABSENT with a reason | step 1; B11's finalize | engineering |
| 3 | Build the holding index: `sbatch -D "$PWD" code/data_platform/db/build_index.sbatch` from the grid copy of `data_platform/db` (it refuses the login node; indexes only folders with a README.yaml) | `/rs/rs_grp_oschome/go2432/data/_index/holding.sqlite` exists; its per-collection file counts equal the census counts in `docs/grid_read_2026-10-08/census/census_merged_partial.tsv` (job 40580051) for every indexed folder | 0 collections with a count mismatch | steps 1 and 2 | engineering |
| 4 | Greg's decisions, then FINALIZE batch by batch (`cutover.sh` with `FINALIZE=1`; it re-verifies, hashes every file of an `irreplaceable` item or one under 50 GB, refuses any change since the cut-over). Done by 2026-10-12 (issue #65; `MANIFEST_GRID.md` section 2): every batch with data finalized on 2026-10-11, B05 and B10 on 2026-10-12; B11 and B13 cut over with their finalize running (B13: `nnunet/results` 299 GB and `ablate` 202 GB verified; `bench` not recorded); the DUA / EULA folders opened to approved students (Greg, 2026-10-11) and the VinDr and BUU items inside them by visibility jobs 40599886 and 40599867 (2026-10-12). Open: deletions (1,590.3 GB of candidates, MP section 8; from DDP "The totals" 353.7 GB more now and 218.3 GB once a condition is met), the three B14 inspect-only entries (two 2022 download leftovers, `/wsu/home/go/go24/go2432/spinopelvic-seg/nnunet/raw`), when `/wsu/home/go/go24/go2432/s1v11` opens to students (OQ A26; its Ceph copy is owner-only, `drwx--S---`, until Greg reads its Zenodo upload scripts for a token) | each FINALIZE recorded with its job id and `<n>.finalize.json` (none is recorded in this folder); `pan_quota` below 90 % of 4,294.97 GB (below 3,865 GB) after B02 and B06 are finalized: met, HOME 1,334 GB on 2026-10-12 (issue #65) | HOME below 3,865 GB | step 1; Greg | Greg |
| 5 | Repair the records that contradict each other: (a) B01: either `sbatch` `code/data_platform/reacquire/reacquire.sbatch` for `tcia_ct_colonography` (route `tcia_ctsp_download`, 1,057 GB; needs 5 TB free on Ceph per MP section 10) or write the deletion record naming `/wsu/home/go/go24/go2432/cleanup_v1v3_tcia.sh` and the date into `DATA_MANIFEST.md`; (b) CTPelvic1K datasets 1-5 re-download (Zenodo 4588403) in a job; (c) bring the grid checkout to 097933a by archive; (d) replace the login-node instructions in the repository's `CLAUDE.md`, `docs/PIPELINE_RESUME.md`, `docs/MODEL_REGISTRY.md`, `containers/build_container.sh` by `sbatch` forms (OQ F10; `docs/MODEL_REGISTRY_CORRECTION.md` here); (e) `/wsu/home/go/go24/go2432/github` and `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/.token` rotated and deleted; (f) `/rs/rs_grp_oschome/go2432/data/ctsp_april` permissions; (g) the `"\` directory in `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` removed; (h) the content-hash chain run once on the real corpus (OQ C16; RECIPES section 10); (i) the identity tables re-keyed into `tools/identity/` (OQ F14) | OQ B30, B31 and B32 answered in `STATUS.md` with the file or job that answers them; `/rs/rs_grp_oschome/go2432/data/or_ready/data_accounting/` exists with a `DATA_ACCOUNTING_LEAK_CHECK` line in the stage-2 log | the chain exits zero on the real corpus; the fake-leak corpus exits non-zero | Greg for (a) re-acquisition, (b), (e); engineering for the rest | Greg, engineering |

## B. Open questions this folder owns (OQ rows; answer each in `STATUS.md` with its file or job)

| id | question | gate | who |
|---|---|---|---|
| A19 | keep or delete the RSNA 2022 cervical archive (203,321,991,870 B on Ceph after B08; used by nothing); is it covered by HPR 2026-269? | a written decision in `DATA_MANIFEST.md` card `rsna_2022_cspine` | Greg |
| A26 | the migration decisions (step 4) | as step 4 | Greg |
| A29, A30 | confirm the reader split of the handoff and this folder; keep, redact or delete the withheld contact data | Greg's written answer; until then this folder is Greg-only | Greg |
| B16 | whether the nnU-Net ablation array completed and what it found (`/wsu/home/go/go24/go2432/ablate`: `v5_all`, `v5_minus_all`, `v5_minus_extras`, `v5_minus_obl`, `v5_minus_pseudo` exist) | a job that reads the five arms' summaries | engineering |
| B17 | which grid copies of `eval_gate.py`, `patient_keys.py` ran the 2026-09-24 cells | the grid checkout's `SHIPPED_COMMITS.txt` (does not exist yet) or its git log | engineering |
| B18 | whether `slurm/data_accounting.sh` ever ran on the real corpus | step 5 (h); on 2026-10-08 `or_ready/data_accounting/` did not exist (GRIDLS) | engineering |
| B19 | whether the grid `tools/realxray_banks.json` lists `cobra_elekta_v3` and `cobra_elekta_g3test` | step 1 | engineering |
| B21 | whether `/wsu/home/go/go24/go2432/corpus_final/` (G4) exists | answered: it does not (GRIDLS "ls ~/corpus_final") | done |
| B22-B26 | per-source render counts inside `allspine_v9`; the body detector's `yolo_v3`/`yolo_v4z` composition; MODEL_CARD's fold-0 crop counts (31,396 vs 31,446); RSNA 2,022 vs 2,019 studies and what fills 236.8 GB; Spinal-AI2024 20,001 vs 20,000 files | one job per question that reads the bank's `meta.json` or the raw tree and writes the count beside the question | engineering |
| B27, B28 | whether the sacrum-adjacent CSVs were recomputed on v11 under `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/morphometrics/`; whether `data/v5_final` and `data/zenodo_deposit` still exist in the grid CTSP checkout | partly answered: GRIDLS "ls ~/CTSpinoPelvic1K/data" shows json/txt remnants, `qc_dashboard/` and three symlinks only; `03_ctspinopelvic1k_dataset` owns the rest | 03 |
| B30 | the batch state after 2026-10-08; the B01 contradiction; whether the index was built | answered for 22:20 UTC in `STATUS.md`; re-read STATUS after step 1 | engineering |
| B31 | whether `/wsu/home/go/go24/go2432/remote_wait.sh`, `/wsu/home/go/go24/go2432/model_registry`, `/wsu/home/go/go24/go2432/mlflow` still sit at those paths | answered: all three present (GRIDLS) | done |
| B32 | why the grid can no longer fetch the private repository | read the checkout's remote config in a job without printing credentials | engineering |
| B33 | the Docker Hub tag behind `spinesurg-ct.sif`; the GPU model behind `gvohp` | `.sif` metadata in a job; `sinfo` | engineering |
| E4, E5 | what the `cm_spine` Drive file is; why 2,293 DeepFluoro vendor frames, the BUU AP films, the BUU (2000) labels and `synth_rare` are unused | a written criterion or a bank (directives D2-D6) | Greg |
| E16 | visibility and role of `lstv-detector`, `spinesurg-ct-annotator`, `CTSpinoPelvic1K-Syn`; which ostk `projects/` hold working code | a line each in `MANIFEST_CODE.md` | Greg |
| F7 | fix `tools/xray_dataset_usage.py`: rename `buu_2000` (it is the BUU-LSPINE 2000 release, not "AASCE test split"), key raw datasets with `patient_keys.py` not substrings, update the HOME paths after the move | the regenerated `XRAY_DATASET_USAGE.md` (in a job) agrees with `DATA_COMPLETENESS_AUDIT.md` lines 76 and 548 | engineering |
| F10 | the stale login-node instructions (step 5 d) | | engineering |
| F14 | re-key the identity tables into `tools/identity/` (`ctsp_token_map.json`, `ts_alias.json`, `verse_series_to_patient.json`, `vindr_image_to_study.json`, `fluorocap_doc_keys.json`, `deepfluoro_h5_alias.json`, `banks.json`) | `test_patient_keys.py` passes against the tables; the VinDr map (job 40416449) committed | engineering |
| F15 | memory hygiene: the banned word in 10 tracked spinesurg and 29 tracked CTSP files; the three broken wikilinks | `git grep -il` returns nothing | engineering; Greg commits |
| F17 | `tools/test_leak_check.py` fails on the stale Geneva fixture (`phantom_p01_065kv -> geneva:phantom want geneva:phantom_p01`) | Greg approves changing the fixture to `geneva:phantom`, or the test stays a known failure | Greg |
| F23 | whether allspine v5 carried the NHANES twins (48 of 54 measured on v6 and v7 only) | a sentence in `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` naming v5, or "not recorded" | engineering |

## C. Data acquisition this folder records (RD section 5.5, DAT-1; MANUSCRIPTS section 16)

| item | state | step | gate | who |
|---|---|---|---|---|
| the 14 fluoroscopy cine requests of 2026-09-26, SX-Stitch (1,032 intraoperative frames), Balgrist ex-vivo (13 + 6 specimens) | drafted, none sent (`DATA_MANIFEST.md` section 8 cards: "Where it is now: Nowhere"); the Balgrist draft's first sentence still reads "a neurosurgery resident; confirm title" and must read General Surgery | Greg sends; record "sent" with the date in each manifest card | a reply naming a DUA route for at least one set of 100 or more living patients (RD rank 6) | Greg |
| Charters 2024 (UCLA, 527 patients, 2,486 paired kV), LevelCheck cohort (178 patients), Huashan (140 patients) | not drafted | draft (addresses withheld here; the corresponding authors are named in the papers) | as above | Greg |
| TCIA CMB-MML / CMB-AML XA (16 patients), NIT Warangal (9 patients) | open, not fetched | an anonymous NBIA fetch as a Slurm job; a download | on disk with a manifest card | engineering |
| Merlin (Stanford AIMI), CT-RATE, INSPECT, NLST beyond the pilot; the seven gated collections | gated; no form signed | the AIMI DUA; the HF gate form; the tier-1 screen first (stopping rule, `RESULTS_CATALOG.md` D.11) | Greg's signature | Greg |
| the VinDr-SpineXR HPR determination | sent to Greg 2026-09-25; number not recorded (OQ A5) | | | Greg |

## D. The repositories' own open items (MP section 10; DDP; VERIFICATION.md; DATA_MANIFEST.md section 10)

- Rewrite MP section 10's end-state paragraph from the census (job 40578909) and `plan/build_plan.py --census`: the
  plan's sized total (3,256.6 GB) plus what stays (about 1,018 GB) exceeds the 4,050 GB HOME holds, so part of the move
  total is no longer on HOME; the first pass's "861 GB" figure was wrong for the same reason.
- `dedup_apply.sbatch` (symlink only byte-identical copies: A01 VerSe'19 = VerSe'20, 185 files, 8.42 GB; A07 s1v11 build
  labels = release labels, 802 files, 1.19 GB; A09 0533 repair = release) runs only after FINALIZE of the batches
  involved; groups whose batch was copying (B04, B07, B09, B10, B11) come back `not_ready` and are rerun with `GROUP_IDS`.
- The three B14 inspect-only entries; the two 2022 download leftovers (`/wsu/home/go/go24/go2432/to_greg.zip?origin_team=...` 125,527 B,
  `/wsu/home/go/go24/go2432/view?usp=sharing` 67,453 B).
- `DATA_MANIFEST.md` section 10 unknowns (family A 1-2 resolved as ABSENT by the STATUS files; 3-4 settled; family D 29
  open; family E 3 settled).
- `ssn:splits_5fold.json` at the repository root is an empty file (0 bytes, 2026-09-12): delete or regenerate
  (`docs/handoff/LEAKAGE.md` section 7 item 8).
- `Dataset815` never preprocessed (both prep jobs died on a missing singularity path): `sbatch slurm/prep815.sh` where
  singularity resolves (`memory/data-audit-99-gaps.md`; `06_transitional_ct_census` decides the use).
- `ssn:tools/anomaly_manifest.py` defaults `--bank` to the deleted `/wsu/home/go/go24/go2432/allspine_v5_fov96_ctx/rung_1.npz` (OQ F22);
  `ssn:slurm/scaling_sweep.sh` writes to paths that do not depend on `BASE` (OQ F21): fix before any rerun.

## E. Not in scope here (owned elsewhere)

The ruleclass arms and the review tree (06), the real-frame banks and the service (01), the v11 rebuild and the
camera-ready (03), the ostk defects (04), Beethoven and the access list (11).
