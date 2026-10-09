# Migration plan: imaging data from HOME to the CephFS layout

Written 2026-10-08. Moves every plain-film, fluoroscopy, C-arm and CT holding on HOME (`/wsu/home/go/go24/go2432`,
Panasas) into the layout of `LAYOUT.md` on `/rs/rs_grp_oschome/go2432` (CephFS), one batch at a time, with a
verified copy before anything on HOME changes and a symlink at every old path afterwards. Nothing in this folder
has been run on the grid; the scripts were tested on a synthetic tree under WSL (VERIFICATION.md).

## 0. Summary

- **Scope**: the HOME rows of `plan/layout_map.csv` with action `move` (batches B00-B11; B12 was dropped on
  2026-10-08 and `~/spinesurg-ct-nnunet/nnunet/raw` stays on HOME, section 6). Entries already on Ceph stay where
  they are and get a README.yaml. Batch B13 (nnU-Net results, ablations, bench: results, not imaging) is listed but
  runs only if Greg says so. Batch B14 holds the entries nobody had named until a grid inspection identified them on
  2026-10-08: six imaging-derived items move in it into the folders of their sources, the entries that are not
  imaging are listed there and stay on HOME, and three entries are still inspect-only (section 5, B14).
- **Size**: the generated table in section 5 gives items and GB per batch. With the sizes on record (2026-09-01 du,
  2026-09-16/19/22/25 manifests and du), B00-B11 and B14 hold the totals printed at the top of that table; the 192.8 GB of CT
  inodes the two B02 trees share are counted once. Those sizes are stale in both directions: some listed folders are
  probably already deleted (a memory note says the reclaim phases A and B ran on 2026-09-07, mem:zenodo-deposit.md;
  no job log is on this laptop) and 157 items have no recorded size at all. The census job 40578909 settles both; regenerate the
  plan from it before the first batch (in a job, section 2 step 1) and use the regenerated table.
- **Method**: `rsync -aH --partial` inside an sbatch job on a compute node (rsync is never run on the login node),
  one job per batch, a log and a verification JSON per item; a batch's hard-link group in one rsync call; DUA/EULA
  items owner-only from the first byte; then a cut-over job that renames the HOME original to `<path>.pre-ceph` and
  leaves a symlink; then, after Greg has checked, a finalize job that compares each `.pre-ceph` copy with the Ceph
  copy again and deletes it only when they are equal. That last step is the one that frees HOME quota.
- **Where Python runs**: never on warrior (it terminates python and rsync by name, memory note
  grid-ssh-second-factor; nothing computes on the login node, memory note no-jobs-on-login-node). Every Python step
  below is either an sbatch job (`--wrap`) or runs on this laptop with its output copied over.
- **Order**: a 6 GB pilot (B00, DeepFluoro, which has a hashed root to check against), then the largest single tree
  (B01, TCIA, about 1 TB, read by nothing current), then source by source.

## 1. What this plan decides, and what it does not

Decided here: the target path of every imaging entry (LAYOUT.md), the batch order, the copy and verification
method, the cut-over with symlinks, and the README.yaml of each source folder.

Not decided here (Greg decides): deleting anything, including duplicates and superseded banks (section 8 lists the
candidates with their reasons; the plan moves them like everything else unless told otherwise); moving results
(B13); the permissions of the DUA and EULA folders beyond owner-only (LAYOUT.md rule 8); what the three entries
B14 still inspects are (two download leftovers and `~/spinopelvic-seg/nnunet/raw`); when `~/s1v11` may be opened to
students (it stays owner-only until its upload scripts are read for a token); renaming any folder that is already on
Ceph.

## 2. Pre-flight (before the first batch, and again before each batch)

1. **Census.** When job 40578909 has written `/rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/`,
   copy `census.tsv` to `plan/` and regenerate the plan, in a job or on this laptop, never on warrior:
   `sbatch -p reqp --qos=requeue -D "$PWD" -o logs/build_plan_%j.out --wrap "python3 build_plan.py --census census.tsv"`
   (from `plan/`). Check that its column names are among those `build_plan.py` accepts (`path` plus `bytes`,
   `size_bytes`, `kb`, `kib` or `gb`); adjust the loader if the census wrote something else. Then read
   `plan/migration_batches.csv` again, and inspect `~/spinopelvic-seg/nnunet/raw` (B14) in `census/depth2.tsv`.
2. **Quotas.** `pan_quota` (HOME; `df` shows the whole volume and says nothing about the user limit, memory note
   grid-quota-and-deleted-banks) and `df-ceph oschome`. Ceph must keep at least 5 TB free after each batch, because
   `tools/acquisition_fetch.py` refuses to start a unit below that (`--floor-tb 5`, `slurm/acquisition_fetch.sh`).
   `migrate_batch.sbatch` prints both at its start.
3. **Running jobs.** `squeue -u go2432`. `plan/preflight.sbatch` writes `preflight/<BATCH>.jobs.txt`: every running or
   pending job whose command line, work directory, logs or batch script (`scontrol write batch_script`) names an item
   in one of its usual spellings (`/wsu/home/...`, `~/`, `$HOME/`, `${HOME}/`, `$H/`). Do not cut over an item a job
   reads. `cutover.sh` refuses an item it finds named the same way, but the check is ADVISORY: a script that builds
   the path at run time (`$H/$bank`, a list read from a file) is not seen, so look at `squeue` yourself before each
   cut-over. Leave `~/model_night` alone while jobs run on it (memory note grid-ceph-volume-oschome); it is not in
   this plan.
4. **Item inventory.** `sbatch -D "$PWD" --export=ALL,BATCH=ALL preflight.sbatch` (in `plan/`) writes
   `preflight/ALL.tsv`: per item whether it exists, its type, apparent and allocated size, file count, symlinks
   (absolute, dangling, and relative ones that leave the item), files with more than one hard link, whether the
   destination already exists, and the item's flags. Items that are absent (already deleted) are reported, not errors.
5. **Hard links.** Every B02 item carries the `hardlink_group` flag (the CTs of `~/data/CTSpinoPelvic1K` are hard
   links of `~/CTSpinoPelvic1K/data/hf_export_osc/ct`, CTSpinoPelvic1K-1 `slurm/archive_build_inputs.sh` line 73, and
   the build tree links files between its folders), and so do the spine-detector `yolo*` banks of B04: each group is
   copied in one rsync call into `_staging/<batch>` and renamed into place. `multilink_files` in the preflight table
   shows where links exist; `verify_transfer.py` fails a file whose link count differs between HOME and Ceph, so a
   partner that was left out shows up (rerun with `ALLOW_NLINK_LOSS=1` only after deciding that partner stays).
6. **Hashed roots.** `plan/remap_manifest.py` (on this laptop, where it was run on 2026-10-08, or in a job) writes
   `plan/RSNAI_DATA_MANIFEST.remapped.json` with the two HOME roots of `docs/RSNAI_DATA_MANIFEST.json`
   (`deepfluoro_h5` in B00 and `ts_subjects` in B07) pointed at their new paths; the other ten roots are on Ceph
   already and do not move.
7. **Permissions.** Decide whether the DUA and EULA folders (VinDr, BUU, and every bank holding their pixels,
   LAYOUT.md rule 8) may be group-readable. By default `migrate_batch.sbatch` copies them owner-only and `cutover.sh`
   checks again; the existing `$RS/data/vindr` is closed only by the one-line job in LAYOUT.md rule 8.

## 3. The procedure for one batch

Run everything from `~/spinesurg-ct-nnunet/data_platform/plan` on the grid (commit and push `data_platform/`, then
pull it there; the scripts are stored with LF endings). Each step is an sbatch job; `-D "$PWD"` makes the logs land
in `plan/logs/` (`#SBATCH --output` resolves against the submit directory and Slurm opens it before the script
runs, so `plan/logs/` must exist: it is committed as `logs/.gitkeep`, and `mkdir -p logs` costs nothing).

```bash
cd ~/spinesurg-ct-nnunet/data_platform/plan && mkdir -p logs
B=B00
# a. inventory and job check (read-only)
sbatch -D "$PWD" --export=ALL,BATCH=$B preflight.sbatch
# b. optional dry run: what rsync would copy
sbatch -D "$PWD" --export=ALL,BATCH=$B,DRY=1 migrate_batch.sbatch
# c. copy + verify every item (never deletes; rerun to resume)
sbatch -D "$PWD" --export=ALL,BATCH=$B,SAMPLE=200 migrate_batch.sbatch
#    -> runs/$B/STATUS (VERIFIED / VERIFY_FAILED / RSYNC_FAILED / ABSENT / DST_EXISTS per item), runs/$B/<n>.verify.json
# d. the hashed roots on the new copy (B00 and B07 only); remap_manifest.py ran on the laptop; its JSON is in plan/
sbatch -p reqp --qos=requeue -D "$PWD" -o logs/manifest_check_%j.out --wrap "python3 ../../tools/data_manifest.py check --manifest RSNAI_DATA_MANIFEST.remapped.json"
# e. cut over: rename each HOME original to <path>.pre-ceph, symlink the old path to the copy
sbatch -D "$PWD" --export=ALL,BATCH=$B cutover.sh
# f. smoke checks (section 4), then place the README.yaml files and index the batch
cp readme_yaml/<folder>.yaml /rs/rs_grp_oschome/go2432/data/<folder>/README.yaml     # per folder the batch filled
sbatch -D ../db --export=ALL,FOLDERS="<folder> ..." ../db/build_index.sbatch
# g. after Greg has looked: compare each .pre-ceph copy with Ceph again, then delete it (frees HOME quota)
sbatch -D "$PWD" --export=ALL,BATCH=$B,FINALIZE=1 cutover.sh
```

**What "verified" means** (`plan/verify_transfer.py`, standard library): the copy has every path of the source;
every file has the same size; every symlink points where it pointed, and every link that resolved at the source
still resolves at the copy (a relative link that leaves its item fails here); every group of hard-linked files in
the source is a group in the copy, and every file has the same hard-link count on both sides; and a stratified
sample of files (one per top-level folder and size bin, then random up to `SAMPLE`, default 200) hashes equal by
SHA-256 on both sides. Before copying an item, `migrate_batch.sbatch` refuses a destination that already exists
and was not written by an earlier run of the same item (`DST_EXISTS`; `runs/markers/` records which source wrote
which destination), because the targets inside folders already on Ceph cannot be confirmed absent from the
listing. Copied directories keep the setgid bit (`--chmod=Dg+s`), so files below them take the group `oschome`. `SAMPLE=0 --all` (edit the call) hashes every file;
that reads both copies in full and is worth it only for small batches or when a sample fails. A second
`rsync -aHn --checksum --itemize-changes` pass is the other full check; `cutover.sh` already reruns a size-and-mtime
dry run and refuses any item that changed after the copy.

**What FINALIZE checks before it deletes a `.pre-ceph` copy**: the HOME path is a symlink to the Ceph path; the Ceph
copy exists (a dangling symlink would otherwise lead to deleting the only copy); `verify_transfer.py` finds the
`.pre-ceph` copy and the Ceph copy equal, hashing every file when the item is flagged `irreplaceable` (the v11
working copy, whose labels are on no public mirror; the FluoroCap harvest; the identity tables) or holds less than
`FULL_HASH_GB` (50); and a size-and-mtime rsync dry run of `.pre-ceph` against the Ceph copy itemizes nothing, so a
file written into `.pre-ceph` after the cut-over (an open handle, a job's working directory) is not lost. Any
difference refuses the item and is logged in `runs/<B>/<n>.finalize.json`.

**Reruns.** `migrate_batch.sbatch` resumes. A hard-link group is re-entered: copies an earlier run already moved
into place are renamed back into `_staging/<batch>`, the one group rsync refreshes them from HOME (with `--delete`
inside the staging tree), and they are moved into place again. The staging tree ends empty and is removed; a rerun
refuses a staging tree that holds anything its `.group_items` record does not name.

**Throughput** is not recorded for this cluster. The pilot's rsync log (`runs/B00/001.rsync.log`, `--info=stats2`)
gives bytes per second; use it to size `--time` for B01 (about 1 TB). `migrate_batch.sbatch` asks reqp for 4 days,
as `slurm/acquisition_fetch.sh` does; the partition's own limit is not recorded here. A batch that runs out of time
resumes when resubmitted.

## 4. Smoke checks after each cut-over

- `ls -la <old path>` shows a symlink to the new path; `ls <old path>/ | head` lists the content.
- The tools that name the batch's paths most often (section 6) still find them, each run in a job
  (`sbatch --wrap`): for example after B02, `tools/patient_keys.py` and one `ctx_build` dry run; after B04,
  `tools/xray_dataset_usage.py` (it reads `~/spine-detector/data/raw`); after B00 and B07, `tools/data_manifest.py
  check` on the ORIGINAL manifest (it walks the symlinked roots); after B06, one `slurm/versefusion_totalseg.sh` case.
- For container jobs, one job that binds the moved HOME tree and `-B /rs/rs_grp_oschome/go2432` reads a file through
  the symlink (LAYOUT.md section 4).
- `pan_quota` shows the expected drop only after FINALIZE.

## 5. Batches (generated)

<!-- BEGIN GENERATED: batches -->
Generated 2026-10-08. Totals over B00-B11 and B14 (B12 dropped and empty; B13 optional, excluded): 219 items to move, 3256.6 GB sized (3.26 TB), 157 items unsized, 1590.3 GB of the sized total are deletion candidates. The `items` column also counts inspect-only entries, which move nothing (3, all in B14); the totals leave them out.

| batch | order | title | items | est_gb_sized | items_unsized | deletion_candidate_gb | depends_on |
|---|---|---|---|---|---|---|---|
| B00 | 0 | pilot: DeepFluoro H5 (small, one source, hashed root) | 1 | 6.2 | 0 | 0.0 |  |
| B01 | 1 | TCIA CT COLONOGRAPHY raw DICOM and reference NIfTI | 5 | 1057.0 | 0 | 336.0 | B00 |
| B02 | 2 | CTSpinoPelvic1K release working copy + build tree (one hard-link group) | 30 | 291.1 | 4 | 64.1 | B00 |
| B03 | 3 | HOME copies of CTSpine1K and CTPelvic1K | 2 | 226.0 | 0 | 226.0 | B02 |
| B04 | 4 | plain-film raw corpora and the spine-detector datasets | 13 | 302.2 | 6 | 159.0 | B00 |
| B05 | 5 | XRSpinoPelvic1K data (BUU-LSPINE 2000, xrsp1k DRRs) | 3 | 4.7 | 2 | 4.7 | B04 |
| B06 | 6 | VerSe / VerSeFusion data and VerSe render banks | 14 | 383.1 | 11 | 187.0 | B00 |
| B07 | 7 | TotalSegmentator v2.0.1 and v3.0.0 and their banks | 5 | 210.8 | 2 | 100.0 | B00 |
| B08 | 8 | RSNA 2022 cervical, RibFrac zips (spondy_landmark, identified 2026-10-08, moves in B14) | 2 | 203.3 | 1 | 203.3 | B00 |
| B09 | 9 | FluoroCap and FluoroGen | 7 | 316.0 | 6 | 181.0 | B00 |
| B10 | 10 | single-source derived banks (CT renders, film banks, C-arm banks) | 64 | 79.7 | 61 | 0.0 | B02 B04 B06 B07 |
| B11 | 11 | banks of several sources, review packs, identity tables | 64 | 176.2 | 59 | 129.2 | B10 |
| B12 | 12 | (dropped 2026-10-08: nnunet/raw stays on HOME, its containers bind no Ceph path) | 0 | 0.0 | 0 | 0.0 |  |
| B13 | 13 | OPTIONAL, not imaging: nnU-Net results, ablations, bench (Greg decides) | 3 | 627.4 | 0 | 0.0 | B11 |
| B14 | 14 | identified 2026-10-08: moved or left (3 entries still to inspect) | 12 | 0.3 | 5 | 0.0 | B02 B04 B05 |
<!-- END GENERATED: batches -->

**Per-batch notes.**

- **B00 (pilot)**: `~/deepfluoro` (6.2 GB): one source, a hashed root (`deepfluoro_h5`, list_sha256 2ccfdf83... in
  docs/RSNAI_DATA_MANIFEST.json) and one inbound symlink (`~/user/diffdrr_data`). If anything in the procedure is
  wrong, it shows here at no cost.
- **B01**: TCIA CT COLONOGRAPHY raw DICOM (721 GB on 2026-09-01) and its dcm2niix NIfTI (336 GB). No current job
  reads them. The NIfTI is regenerable and is a deletion candidate.
- **B02**: the CTSpinoPelvic1K release working copy (`~/data/CTSpinoPelvic1K`, the v11 labels and the 802 CTs;
  HF_EXPORT_DIR of the Dataset810/813/815 containers) together with every build-tree folder under
  `~/CTSpinoPelvic1K/data/` and the three `~/build_archive*` folders in ONE rsync call: every B02 item carries the
  `hardlink_group` flag (2026-10-08; before, only the working copy did, and `hf_export_osc`, whose `ct/` holds the
  same 802 inodes, would have been copied separately and stored twice on Ceph, about 193 GB). The batch total and
  the `hf_export_osc` deletion candidate count the 192,813,331,872 B of shared CTs once. Many of the build-tree
  folders were on the reclaim lists and are presumed absent. The CTs are read by 76 code files
  (plan/path_refs_by_item.csv); the symlink keeps them working.
- **B03**: the HOME copies of CTSpine1K (190 GB) and CTPelvic1K (36 GB), both on reclaim phase A, so probably absent.
  CTSpine1K is also on Ceph, sha256-verified per file (2026-09-23).
- **B04**: the plain-film raw corpora under `~/spine-detector/data/raw/` (keep the `/raw/<name>/` fragments),
  VinDr (DUA; 48 GB, sized from its `1.0.0` child) and BUU (EULA), both owner-only from the copy on, and the
  spine-detector `data/interim` and `data/yolo*` (BUU and VinDr pixels: owner-only; the `yolo*` banks copy as one
  hard-link group because they likely share files, `tools/data_alias.py`).
- **B05**: XRSpinoPelvic1K's data (BUU-LSPINE 2000 and its zip; the xrsp1k DRRs). The `buu_2000` symlink in
  spine-detector keeps resolving through the new symlink.
- **B06**: `~/VerSeFusion/data` as one unit (138.1 GB from its sized children raw 71, canonical 67, unified 0.088;
  unified/ is links into raw/ and canonical/), vf_813, the VerSe render banks and implant_verse (187 GB, synthetic
  and regenerable). Before the cut-over, `slurm/versefusion_totalseg.sh` must bind `/rs/rs_grp_oschome/go2432`
  (added 2026-10-08), or its container sees dangling links.
- **B07**: TotalSegmentator v2.0.1 and v3.0.0 (zips plus unpacked trees), their DRR banks and implant_ts.
  `$RS/data/validation_ts` links point at `$HOME/data/TotalSegmentator/...` and keep resolving through the symlink;
  `slurm/acquisition_validation_prep.sh` can re-link them to the new path later. `ts_subjects` is a hashed root.
- **B08**: the RSNA 2022 zip (203 GB, used by nothing) and the RibFrac zips. `~/data/spondy_landmark` was listed
  here as inspect-only and was never in `B08.tsv`; identified on 2026-10-08 as a second download of Mendeley
  5jdfdgp762, it moves in B14, so B08's item file is unchanged.
- **B09**: `~/FluoroCap` (316 GB, the frozen release is the authoritative copy; `~/.fluorocap` credentials are a
  separate HOME entry and never move) and FluoroGen.
- **B10**: single-source banks (CT renders, film banks, C-arm fold banks); mostly unsized. `~/nhanes_pseudo` is 74 GB
  (2026-09-19 du, docs/CONTINUANCE_2026-09-19.md L27). The VinDr and BUU banks are owner-only.
- **B11**: banks built from several sources, review packs, the render folders of `~/lstv_flag` (its `models/` and
  results stay on HOME) and the identity tables (`patient_keys*.json`, `split_final.json`, flagged irreplaceable).
  Banks whose sources include VinDr or BUU are owner-only (LAYOUT.md rule 8). 57 references that supply a holdout were repointed to `allspine_v7_fov96_ctx` (memory note
  grid-quota-and-deleted-banks), and an unreadable holdout bank once let evaluations run on training cases without
  an error (`tools/holdout.py` now raises), so check it right after the cut-over.
- **B12 (dropped 2026-10-08)**: `~/spinesurg-ct-nnunet/nnunet/raw` stays on HOME. Fifteen slurm scripts bind
  `${PROJECT_ROOT}/nnunet` (or `LOCAL_NNUNET`) into their containers with `nnUNet_raw=/nnunet_nfs/raw` and bind no
  Ceph path (section 6), so a symlinked `nnunet/raw` would dangle inside every one of them, and the tree is only
  symlinks and labelsTr. `nnunet/preprocessed` was deleted (DATA_COMPLETENESS_AUDIT.md lines 103, 404).
- **B14 (identified 2026-10-08: moved or left)**: the entries nobody had named, read on the grid; six move, nine stay,
  three are still inspect-only. Its own section follows.
- **B13 (optional)**: nnU-Net results (348.6 GB, to `$RS/results/nnunet_results`), ablations (234.8 GB), bench
  (44 GB): results, not imaging, to `$RS/results/` if Greg decides.

### B14: the entries identified on 2026-10-08

On 2026-10-07 fifteen HOME entries had no name in either repository or in memory: the fourteen disk-map rows of role
`unknown` and `~/data/spondy_landmark` (inspect-only in B08); `$RS/data/morphdef` on Ceph was a sixteenth. A
read-only job on 2026-10-08 (scratchpad `inspect_unknown.sh`, output `inspect_unknown.out`, session scratch folder, neither preserved: not recorded; Greg: "identify them
based on any metadata or url source data affiliated with them") listed each one's files and dates, git remote,
README and log heads. Thirteen of the fifteen, and `morphdef`, are identified below. A few facts came from the same
day's grid reading and are not in that output (the contents of `url.txt` and `files.json`, the `Train/` and `Test/`
layout, the member names of `qc.tar.gz`, what `~/v` holds); the cards say which. The output's URL search printed
nothing for any entry: its pattern (`[^"' <>)\]]+`) requires a literal `]` after the class, so it matches nothing.

Migration jobs for B00-B09 already read their item files on the grid, so nothing is added to or taken from B00-B11:
what moves is in `batch_items/B14.tsv`, and the item files of B00-B13 are byte-identical to the ones on the grid.
B14 copies into folders that B02, B04 and B05 fill (its `depends_on`); run it like any batch (section 3), then place
the regenerated README.yaml of `ctspinopelvic1k_build_tree`, `mendeley_5jdfdgp762` and `xrspinopelvic1k` again.

**Moved** (6 items, 0.3 GB sized, 2 unsized):

| entry | what it is | target, flags |
|---|---|---|
| `~/data/spondy_landmark` | Mendeley Data 5jdfdgp762 "Spondylolisthesis Vertebral Landmark" (plain film, CC BY 4.0): `Dataset.zip` 43,892,677 B (the release's API size), `url.txt`, `files.json`, an empty `dl.log` and the unpacked `x/Dataset/{Train,Test}` (jpg); folder 2026-09-19 13:03. A second download: `~/spine-detector/data/raw/mendeley_716` (B04) holds the same release. `tools/ct_inventory.py` lists it as a CT root, which it is not | `$RS/data/mendeley_5jdfdgp762/raw/spondy_landmark`, zip and `x/` as one item; candidate (duplicate); the index skips it (`index_skip`) |
| `~/s1v11` | the CTSpinoPelvic1K v11 build workspace, 2026-09-11..18: the S1-merge, carve-audit and comparison scripts, the logs of jobs 40198228, 40198880, 40309073 and 40309160, `out/v11_labels`, `out/s1_carve_audit.csv`, `morphometrics/surgical_morphometrics.csv`, `out/dataset_labels_v11.json` ("S1 (29) retired"), and the Zenodo v11 upload (`labels.zip` 883,912,953 B stored with HTTP 201 on 2026-09-18 22:46) | `$RS/data/ctspinopelvic1k_build_tree/derived/s1v11`; `irreplaceable` (FINALIZE hashes every file); `restricted` until its upload scripts and state files are read for a token |
| `~/pitest`, `~/pdwtest` | ten and two CTSpinoPelvic1K label files (0024 ... 1129; 0010, 0038), dated 2026-09-10 11:38 and 16:09: scratch copies from that day's spinopelvic work; what the names stand for is not recorded | `$RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/{pitest,pdwtest}`; candidates |
| `~/qc.tar.gz` | pelvis-propagation QC PNGs, 196,147,947 B, 2026-06-12; its member names are what `ctsp:scripts/viz_propagation.py` writes (first committed that day). Not the speckle QC. The disk map had it as a result; it is mapped now | `$RS/data/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz` (dated: a bare `qc.tar.gz` says nothing in a shared folder) |
| `~/dis_renders` | five PNGs named by BUU-LSPINE film ids (`0008-M-022Y1` ... `0016-F-023Y1`), 10,869,856 B, 2026-08-11 12:52; what drew them is not recorded (`~/spinesurg-ct-nnunet/disputed_renders` holds VerSe PNGs, not these) | `$RS/data/xrspinopelvic1k/derived/dis_renders`; `restricted` (presumed BUU pixels, EULA); candidate |

**Left on HOME** (one line each in section 7):

| entry | what it is |
|---|---|
| `~/Multi-View-Vertebra` | software: a clone of github.com/ShanghaiTech-IMPACT/Multi-View-Vertebra-Localization-and-Identification-from-CT-Images, the MICCAI 2023 reference code (HEAD c290796, 2024-09-19), cloned 2026-09-13; 15 `.py` and one png |
| `~/docs` | ten documents of 2026-02-12, "Bulletproof Weak Label Generation v4.0, Complete Fix for Spine-Level-AI", from an earlier spine-level project; the script they describe is not in the folder |
| `~/3`, `~/6` | GOMC Gibbs-ensemble output (`out_GEMC_equil.dat`), 2024-03-17 |
| `~/ada` | a GOMC 2.75 Gibbs-ensemble production run (inputs, checkpoint, log), 2024-02-19 |
| `~/output` | CHARMM topology, parameter, structure and restraint files (`output/CHARMM`), 2023-04-24 |
| `~/v` | a gzip file dated 2024-02-17 (GOMC `bd/` outputs, by the grid reading) |
| `~/github` | a plain-text file holding a GitHub personal access token (mode 644 until 2026-10-08, now 600). **Security item: Greg rotates the token and deletes the file.** No job reads, copies or moves it |
| `$RS/data/morphdef` (Ceph) | three empty folders (`logs/`, `out/`, `src/`) made 2026-09-23 02:15: the scaffold of the morphology-deformation work stopped that morning before anything was built (memory note morphology-deformation-feasibility). Nothing to index and no README.yaml; removal candidate (section 8) |

**Still inspect-only** (3):

| entry | why |
|---|---|
| `~/to_greg.zip?origin_team=T5G027G83` (304K, 2022-05-26), `~/view?usp=sharing` (256K, 2022-01-26) | not reached: the inspection's leftover filter matched archive extensions, and both names end in a URL query. Read them in a job from `plan/`: `sbatch -p reqp --qos=requeue -D "$PWD" -o logs/leftovers_%j.out --wrap 'cd ~ && file "to_greg.zip?origin_team=T5G027G83" "view?usp=sharing"'` |
| `~/spinopelvic-seg/nnunet/raw` | unchanged: its README sets `nnUNet_raw=$PWD/nnunet/raw` (Dataset803 imagesTr and labelsTs: imaging-derived); the census decides its size and link type (section 2 step 1) |

**Checks before and after B14.**

- Hard links: `~/s1v11/out/v11_labels`, `~/pitest` and `~/pdwtest` may share inodes with
  `~/data/CTSpinoPelvic1K/labels` (B02); how the v11 labels reached the working copy is not recorded
  (`merge_s1_into_sacrum.py` writes new files with `nib.save`). The preflight's `multilink_files` column shows it. If
  they do, `verify_transfer.py` fails them on the link count; after checking, rerun with `ALLOW_NLINK_LOSS=1` (the
  labels are then stored twice on Ceph, about 1 GB).
- `~/s1v11` stays owner-only (the `restricted` flag) until someone reads `zenodo_v11.py`, `upload_zip.sh`,
  `zenodo_v11_state.json` and `upload_reply.json` for a token. To open it after that check, drop `restricted=True`
  from its rule in `build_plan.py`, regenerate, and rerun `publish_visibility.sh` for `ctspinopelvic1k_build_tree`.
- `~/dis_renders` is owner-only like every BUU bank; `publish_visibility.sh` closes it by path inside the open
  `xrspinopelvic1k` folder.

## 6. Cut-over: the old paths keep working; edit the scripts later

Every moved path is replaced by a symlink, so a script that reads a moved path on the host keeps working. Three kinds
of script do need attention, listed after the table: those that bind a moved tree into a container, those that
delete and rebuild a moved bank by its HOME name, and those whose default is a HOME data path. The scan of both
repositories (family E section 4: 1,358 code files, 6,025 references to 196 grid folders) is joined to the moved
items here.

<!-- BEGIN GENERATED: path_refs -->
Code files (both repositories) that name each moved HOME path, from `plan/path_refs_files.csv` (scan of 2026-10-07). The symlink left at the old path keeps every one of them working; edit them later, one at a time. Full list with file names: `plan/path_refs_by_item.csv`. 104 of 222 moved items are named by at least one file.

| path | batch | files | examples |
|---|---|---|---|
| ~/FluoroCap | B09 | 83 | spinesurg-ct-nnunet:SchwingNet/atlas/update_cards.py spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_repro.sh spinesurg-ct-nnunet:SchwingNet/tools/fig6_manifest.py |
| ~/data/CTSpinoPelvic1K | B02 | 76 | CTSpinoPelvic1K-1:Student_Projects/examples/pelvic_width_dimorphism/measure_pelvic_width.py CTSpinoPelvic1K-1:Student_Projects/templates/get_dataset.sh CTSpinoPelvic1K-1:Student_Projects/tools/grid.sh |
| ~/ctsp_drr | B10 | 53 | spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:SchwingNet/tools/fig6_valset.py spinesurg-ct-nnunet:slurm/allspine_bank.sh |
| ~/VerSeFusion/data | B06 | 41 | spinesurg-ct-nnunet:SchwingNet/tools/fig6_bank_keytest.py spinesurg-ct-nnunet:SchwingNet/tools/fig6_bank_rename_keyable.py spinesurg-ct-nnunet:SchwingNet/tools/figure1.py |
| ~/verse_drr | B06 | 38 | spinesurg-ct-nnunet:slurm/allspine_bank.sh spinesurg-ct-nnunet:slurm/ctx_build.sh spinesurg-ct-nnunet:slurm/ctx_crops.sh |
| ~/bench | B13 | 35 | spinesurg-ct-nnunet:SchwingNet/tools/reader_e_features.py spinesurg-ct-nnunet:SchwingNet/tools/reader_e_j1_pairs.py spinesurg-ct-nnunet:benchmark/collect.py |
| ~/bench_ts | B11 | 31 | spinesurg-ct-nnunet:SchwingNet/slurm/rare_class_ts_drr.sh spinesurg-ct-nnunet:slurm/body_masks.sh spinesurg-ct-nnunet:slurm/body_masks_ts.sh |
| ~/allspine_v9_fov96_ctx | B11 | 30 | spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_repro.sh spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/chk9_cv_v9/make_quoted_cv_v9.py spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/cv_v9/zs_v9_kfield.sh |
| ~/nhanes_drr | B10 | 25 | spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:slurm/allspine_bank.sh spinesurg-ct-nnunet:slurm/allspine_v8_bank.sh |
| ~/films_drr | B11 | 24 | spinesurg-ct-nnunet:SchwingNet/slurm/name_fill_apfilm.sh spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:SchwingNet/tools/fig6_manifest.py |
| ~/deepfluoro | B00 | 18 | spinesurg-ct-nnunet:slurm/deepfluoro_acquire.sh spinesurg-ct-nnunet:slurm/deepfluoro_pairs.sh spinesurg-ct-nnunet:slurm/polypose_identity.sh |
| ~/data/TotalSegmentator | B07 | 17 | spinesurg-ct-nnunet:slurm/acquisition_validation_prep.sh spinesurg-ct-nnunet:slurm/iso_rung_control.sh spinesurg-ct-nnunet:slurm/spineps_ids_repair.sh |
| ~/spine-detector/data/raw/buu_full | B04 | 17 | spinesurg-ct-nnunet:slurm/plainfilm_recount.sh spinesurg-ct-nnunet:slurm/recount_unused_audit.sh spinesurg-ct-nnunet:slurm/reproduce_feasibility.sh |
| ~/spine-detector/data/yolo* | B04 | 17 | spinesurg-ct-nnunet:SchwingNet/tools/figure3_network.py spinesurg-ct-nnunet:slurm/fluorocap_hwdet.sh spinesurg-ct-nnunet:slurm/fluorocap_hwdet2.sh |
| ~/lstv_flag/renders | B11 | 16 | spinesurg-ct-nnunet:slurm/ctsp0533_lstvflag.sh spinesurg-ct-nnunet:slurm/lstv_flag_buudiag.sh spinesurg-ct-nnunet:slurm/lstv_flag_control.sh |
| ~/allspine_v7_fov96_ctx | B11 | 15 | spinesurg-ct-nnunet:slurm/carmlspine_cv.sh spinesurg-ct-nnunet:slurm/carmlspine_cv_day.sh spinesurg-ct-nnunet:slurm/carmlspine_finetune.sh |
| ~/vf_813 | B06 | 15 | spinesurg-ct-nnunet:slurm/harvest_verse_ts.sh spinesurg-ct-nnunet:slurm/merge_vf.sh spinesurg-ct-nnunet:slurm/prep815.sh |
| ~/patient_keys_v9.json | B11 | 14 | spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_repro.py spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/bypass/grid_jobs/closure_repro.sh spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/v8_overlap_cause.py |
| ~/nhanes_pseudo | B10 | 13 | spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:slurm/reproduce_feasibility.sh spinesurg-ct-nnunet:tools/anomaly_manifest.py |
| ~/physics_drr | B11 | 13 | spinesurg-ct-nnunet:SchwingNet/slurm/rare_ctsp_drr.sh spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:slurm/allspine_bank.sh |
| ~/ts_drr | B07 | 13 | spinesurg-ct-nnunet:slurm/render_detector_on_real.sh spinesurg-ct-nnunet:slurm/ts_drr.sh spinesurg-ct-nnunet:slurm/ts_spineps_diagnose.sh |
| ~/data/TotalSegmentator_v3 | B07 | 12 | spinesurg-ct-nnunet:slurm/ts_drr.sh spinesurg-ct-nnunet:slurm/ts_spineps_diagnose.sh spinesurg-ct-nnunet:tools/arc_unseen_subjects.py |
| ~/physics_rare | B11 | 11 | spinesurg-ct-nnunet:SchwingNet/slurm/rare_class_ts_drr.sh spinesurg-ct-nnunet:slurm/reproduce_feasibility.sh spinesurg-ct-nnunet:tools/diagnostics/ctsp_crosswalk_leak.py |
| ~/split_final.json | B11 | 11 | spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:SchwingNet/tools/fig6_bank_check.py spinesurg-ct-nnunet:SchwingNet/tools/fig6_freeze.py |
| ~/films_drr_buucorr | B11 | 8 | spinesurg-ct-nnunet:slurm/render_detector_on_real.sh spinesurg-ct-nnunet:tools/build_reader_study.py spinesurg-ct-nnunet:tools/correct_buu_schema.py |
| ~/verse_ctx | B11 | 8 | spinesurg-ct-nnunet:slurm/ctx_arms.sh spinesurg-ct-nnunet:slurm/ctx_build.sh spinesurg-ct-nnunet:slurm/ctx_crops.sh |
| ~/vindr_pseudo | B10 | 8 | spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:slurm/reproduce_feasibility.sh spinesurg-ct-nnunet:tools/anomaly_manifest.py |
| ~/spine-detector/data/raw/aasce | B04 | 8 | spinesurg-ct-nnunet:slurm/recount_aasce_skips.sh spinesurg-ct-nnunet:slurm/recount_unused_audit.sh spinesurg-ct-nnunet:slurm/thoracic_xr_fetch.sh |
| ~/spine-detector/data/raw/vindr | B04 | 8 | spinesurg-ct-nnunet:SchwingNet/slurm/vindr_age_sex.sh spinesurg-ct-nnunet:slurm/plainfilm_recount.sh spinesurg-ct-nnunet:slurm/plainfilm_recount2.sh |
| ~/anchor_drr | B11 | 6 | spinesurg-ct-nnunet:SchwingNet/results/eval_gate/build_inventory.py spinesurg-ct-nnunet:slurm/ctsp0533_renders.sh spinesurg-ct-nnunet:slurm/fluorocap_v2.sh |
| ~/lateral236_pseudo | B10 | 6 | spinesurg-ct-nnunet:slurm/reproduce_feasibility.sh spinesurg-ct-nnunet:tools/anomaly_manifest.py spinesurg-ct-nnunet:tools/corpus_level_report.py |
| ~/patient_keys.json | B11 | 6 | spinesurg-ct-nnunet:SchwingNet/results/eval_gate/closure/v8_overlap_cause.py spinesurg-ct-nnunet:SchwingNet/tools/bank_index.py spinesurg-ct-nnunet:slurm/eval_scaling_curves.sh |
| ~/lstv_flag/renders_verse | B11 | 6 | spinesurg-ct-nnunet:slurm/lstv_flag_curve.sh spinesurg-ct-nnunet:slurm/lstv_flag_finalise_v2.sh spinesurg-ct-nnunet:slurm/lstv_flag_render_verse.sh |
| ~/aasce_drr | B10 | 5 | spinesurg-ct-nnunet:tools/aasce_to_drr.py spinesurg-ct-nnunet:tools/check_level_naming.py spinesurg-ct-nnunet:tools/pipeline_state.py |
| ~/allspine_v8_fov96_ctx | B11 | 5 | spinesurg-ct-nnunet:slurm/eval_scaling_curves.sh spinesurg-ct-nnunet:tools/anomalous_inventory.py spinesurg-ct-nnunet:tools/eval_scaling_curves.py |
| ~/films_ann_fov96_ctx | B11 | 5 | spinesurg-ct-nnunet:tools/latency_bench.py spinesurg-ct-nnunet:tools/level_heatmap.py spinesurg-ct-nnunet:tools/message_fusion.py |
| ~/lstv_eval | B10 | 5 | spinesurg-ct-nnunet:slurm/lstv_eval_proto.sh spinesurg-ct-nnunet:tools/lstv_eval_physics.py spinesurg-ct-nnunet:tools/lstv_eval_prep.py |
| ~/patient_keys_final.json | B11 | 5 | spinesurg-ct-nnunet:SchwingNet/slurm/g3_split.sh spinesurg-ct-nnunet:SchwingNet/tools/fig6_freeze.py spinesurg-ct-nnunet:SchwingNet/tools/gen_claim_checklist.py |
| ~/ts_drr_v3 | B07 | 5 | spinesurg-ct-nnunet:SchwingNet/tools/figure2.py spinesurg-ct-nnunet:slurm/spineps_ts_v3.sh spinesurg-ct-nnunet:slurm/ts_spineps_diagnose.sh |
| ~/verse_only_ctx | B06 | 5 | spinesurg-ct-nnunet:slurm/ctx_realfilm.sh spinesurg-ct-nnunet:slurm/ctx_tune0.sh spinesurg-ct-nnunet:slurm/vo_eval_nhanes.sh |
| ~/vf_v10 | B06 | 5 | spinesurg-ct-nnunet:slurm/tp_morphology.sh spinesurg-ct-nnunet:slurm/versefusion_qc.sh spinesurg-ct-nnunet:slurm/versefusion_tl_morphometrics.sh |
| ~/data/rsna_cspine | B08 | 5 | spinesurg-ct-nnunet:slurm/audit_unused_data.sh spinesurg-ct-nnunet:slurm/other_ct_fetch.sh spinesurg-ct-nnunet:slurm/rsna_cspine_fetch.sh |
| ~/spine-detector/data/raw/csxa | B04 | 5 | spinesurg-ct-nnunet:slurm/cine_eval.sh spinesurg-ct-nnunet:slurm/plainfilm_recount.sh spinesurg-ct-nnunet:tools/data_alias.py |
| ~/spine-detector/data/raw/nhanes_annotated | B04 | 5 | spinesurg-ct-nnunet:slurm/ctx_contour.sh spinesurg-ct-nnunet:slurm/nhanes_build.sh spinesurg-ct-nnunet:slurm/plainfilm_recount.sh |
| ~/spine-detector/data/raw/mendeley_716 | B04 | 5 | spinesurg-ct-nnunet:slurm/audit_unused_data.sh spinesurg-ct-nnunet:slurm/recount_unused_audit.sh spinesurg-ct-nnunet:tools/film_style_dataset.py |
| ~/allspine_v6_fov96_ctx | B11 | 4 | spinesurg-ct-nnunet:tools/benchmark_cina.py spinesurg-ct-nnunet:tools/build_v6_bank.py spinesurg-ct-nnunet:tools/common_testset_eval.py |
| ~/carm_base_cache_v9 | B10 | 4 | spinesurg-ct-nnunet:SchwingNet/slurm/name_fill_prep.sh spinesurg-ct-nnunet:slurm/carmlspine_cv_day_v9.sh spinesurg-ct-nnunet:slurm/carmlspine_cv_v9.sh |
| ~/carm_cvmix0_fov96_ctx | B11 | 4 | spinesurg-ct-nnunet:SchwingNet/slurm/name_fill_keytest.sh spinesurg-ct-nnunet:slurm/carmlspine_cv_v9init.sh spinesurg-ct-nnunet:slurm/eval_gate.sh |
| ~/fluorogen | B09 | 4 | spinesurg-ct-nnunet:slurm/fluorogen_generate.sh spinesurg-ct-nnunet:slurm/fluorogen_lora.sh spinesurg-ct-nnunet:tools/fluorocap_v2_report.py |
| ~/vindr_pseudo_drr | B10 | 4 | spinesurg-ct-nnunet:slurm/launch_round2.sh spinesurg-ct-nnunet:tools/anomaly_manifest.py spinesurg-ct-nnunet:tools/pseudolabel_films.py |
| ~/spine-detector/data/raw/nhanes_full | B04 | 4 | spinesurg-ct-nnunet:tools/data_alias.py spinesurg-ct-nnunet:tools/film_style_dataset.py spinesurg-ct-nnunet:tools/pseudolabel_real_films.py |
| ~/spine-detector/data/raw/spinal_ai2024 | B04 | 4 | spinesurg-ct-nnunet:slurm/recount_aasce_skips.sh spinesurg-ct-nnunet:slurm/recount_unused_audit.sh spinesurg-ct-nnunet:tools/spinal_ai2024_to_render.py |
| ~/anchor_drr_c2 | B11 | 3 | spinesurg-ct-nnunet:slurm/ctsp0533_renders.sh spinesurg-ct-nnunet:tools/c2_anchor_status.py spinesurg-ct-nnunet:tools/wholespine_build.py |
| ~/buu_yolo | B10 | 3 | spinesurg-ct-nnunet:tools/buu_baseline.py spinesurg-ct-nnunet:tools/excluded_sources.py spinesurg-ct-nnunet:tools/patient_keys.py |
| ~/carm_mix_fov96_ctx | B11 | 3 | spinesurg-ct-nnunet:slurm/carmlspine_finetune.sh spinesurg-ct-nnunet:slurm/or_crossdev_setup.sh spinesurg-ct-nnunet:tools/merge_banks.py |
| ~/films_ap_drr | B10 | 3 | spinesurg-ct-nnunet:SchwingNet/slurm/name_fill_apfilm.sh spinesurg-ct-nnunet:tools/eval_multiview.py spinesurg-ct-nnunet:tools/indomain_name_fill.py |
| ~/fluorocap_drr | B09 | 3 | spinesurg-ct-nnunet:SchwingNet/tools/corpus_census.py spinesurg-ct-nnunet:tools/fluorocap_recount.py spinesurg-ct-nnunet:tools/fluorocap_to_ann.py |
| ~/mendeley_drr | B10 | 3 | spinesurg-ct-nnunet:tools/excluded_sources.py spinesurg-ct-nnunet:tools/mendeley_to_render.py spinesurg-ct-nnunet:tools/xray_dataset_usage.py |
| ~/nhanes_ctx | B10 | 3 | spinesurg-ct-nnunet:slurm/ctx_eval_nhanes.sh spinesurg-ct-nnunet:slurm/vo_eval_nhanes.sh spinesurg-ct-nnunet:tools/render_crops.py |
| ~/scaling | B11 | 3 | spinesurg-ct-nnunet:slurm/eval_scaling_curves.sh spinesurg-ct-nnunet:tools/eval_scaling_curves.py spinesurg-ct-nnunet:tools/subset_bank.py |
<!-- END GENERATED: path_refs -->

**Containers that bind a moved tree.** A container sees a symlink's target only when `/rs/rs_grp_oschome/go2432` is
bound too (LAYOUT.md section 4). `slurm/versefusion_totalseg.sh` binds `~/VerSeFusion/data/unified` (B06): it now
adds the group path to its binds (2026-10-08); smoke-test one case after B06. The fifteen nnU-Net scripts that bind
`${PROJECT_ROOT}/nnunet` are why B12 was dropped: `slurm/convert_hf_to_nnet.sh`, `slurm/eval_fold_checkpoint.sh`,
`slurm/plan_sizes.sh`, `slurm/spine_ablation.sh`, `slurm/spine_ensemble_803_best.sh`, `slurm/spine_eval_803_best.sh`,
`slurm/spine_eval_803_full.sh`, `slurm/spine_eval_single.sh`, `slurm/spine_predict_803_best.sh`,
`slurm/spine_pred_803_best_array.sh`, `slurm/spine_prep.sh`, `slurm/spine_train_array.sh`, `slurm/spine_train_fold.sh`,
`slurm/sync_to_nnunet.sh`, `slurm/regen_lstv_cases.sh`. If `nnunet/raw` is ever moved, add
`--bind /rs/rs_grp_oschome/go2432` to each first. Code that writes links with `Path.resolve()`
(`tools/merge_versefusion_corpus.py` `link_or_copy`) records `/.rs/volumes/...` once its input is on Ceph; build such
links from the `/rs/rs_grp_oschome/...` spelling.

**Scripts that delete a moved bank by its HOME name.** After the cut-over `rm -rf ~/<bank>` removes only the symlink,
and the rebuilt bank lands on HOME again (quota, and VinDr pixels outside the closed folder). Changed on 2026-10-08
to clear the bank's contents through the link (`find -H <bank> -mindepth 1 -delete`): `slurm/nhanes_build.sh`
(`~/nhanes_drr`), `slurm/vindr_pseudolabel.sh` (`~/vindr_det_drr`, `~/vindr_pseudo_drr`), `slurm/launch_dual.sh`
(`~/films_ap_drr`). Their writers create `img/` and `ann/` with `exist_ok`, so an existing empty folder is fine.

Scripts whose DEFAULT is a HOME data path, to change one at a time after the move (each named by the cards):
`slurm/ctx_build_ctsp.sh` (`--ct-root $HOME/data/CTSpinoPelvic1K/ct`), `slurm/ts_drr.sh` (`$H/data/TotalSegmentator`),
`slurm/fluorocap_v2.sh`, `slurm/other_ct_fetch.sh` (`--zips $HOME/data/ribs`), `slurm/thoracic_xr_fetch.sh`
(`--grid-copy ~/spine-detector/data/raw/aasce`), `slurm/acquisition_validation_prep.sh` (`$HOME/data/TotalSegmentator`),
`slurm/film_corpus_inventory.sh` and `tools/film_corpus_inventory.py` (`RAW = H / "spine-detector/data/raw"`),
`tools/xray_dataset_usage.py` (`RAW`, `RENDER_DIRS`), `tools/audit_film_corpora.py`, `slurm/vindr_label.sh`,
`slurm/reproduce_all.sh` (data, renders and pseudo stages), `tools/data_manifest.py` (`ROOTS`: `deepfluoro_h5`,
`ts_subjects`, and the wrong DOI of `deepfluoro_vendor`), and in CTSpinoPelvic1K `slurm/archive_build_inputs.sh`
(`WORKCOPY=$HOME/data/CTSpinoPelvic1K`) and `slurm/reclaim_grid_space.sh` (its 802-CT safety check reads the working
copy; it passes through the symlink). `tools/patient_keys.py` needs no change because the layout keeps its path
fragments. Never `ln -sf` a model; chains use `model_registry.py link` (memory note model-registry).

## 7. What stays on HOME

Code and environments (LAYOUT.md section 3), credentials (never read, never moved), `~/model_night` (logs and
experiment roots, 526 code files name it), `~/u251-xenograft-murine-RNASeq-study` (not imaging, 194 GB),
`~/spinesurg-ct-nnunet/nnunet/raw` (B12 dropped, section 5), `~/lstv_flag/models` and the LSTV flag results, small
scripts and notes in the home root, and the symlinks the cut-over leaves.

Identified on 2026-10-08 and left where they are (section 5, B14), one line each:

- `~/Multi-View-Vertebra`: software, a clone of the MICCAI 2023 multi-view vertebra localization code (ShanghaiTech-IMPACT), cloned 2026-09-13.
- `~/docs`: ten documents of an earlier spine-level project ("Bulletproof Weak Label Generation v4.0"), 2026-02-12.
- `~/3` and `~/6`: GOMC Gibbs-ensemble output (`out_GEMC_equil.dat`), molecular simulation, 2024-03-17.
- `~/ada`: a GOMC 2.75 Gibbs-ensemble production run (inputs, checkpoint, log), molecular simulation, 2024-02-19.
- `~/output`: CHARMM topology, parameter, structure and restraint files, molecular simulation, 2023-04-24.
- `~/v`: a gzip file of GOMC outputs, molecular simulation, 2024-02-17.
- `~/github`: a file holding a GitHub personal access token (2026-01-15); not data. **Security item for Greg: rotate
  the token, then delete the file** (its mode was set to 600 on 2026-10-08). No job of this plan reads, copies or
  moves it, and its content is copied nowhere.
- `$RS/data/morphdef`: three empty folders on Ceph (2026-09-23); nothing to move or index; removal candidate.
- Home-root leftovers that are not imaging: `VerSeFusion.tar.gz` (44,461 B, 2026-05-11, code), `disk_top.txt.part`
  (a partial `du` listing, 2026-09-20), the cmake, gcc, gdrive and git-lfs tarballs, `la101psx.tar` and `orient.tar`
  (2002). The one leftover holding imaging-derived files, `~/qc.tar.gz`, moves in B14.

## 8. Not decided here: deletion candidates for Greg

The plan moves these like everything else. Each could instead be deleted once its copy or its source is verified;
the reason is the one the cards give. Generated from `plan/layout_map.csv` (largest first; unsized rows last).

Added on 2026-10-08 from the B14 identifications (section 5):

- `~/data/spondy_landmark`: a second download of Mendeley 5jdfdgp762, the release `~/spine-detector/data/raw/mendeley_716`
  holds. Delete only after the sha256 its `files.json` records matches that zip; until then the index skips it.
- `~/pitest`, `~/pdwtest`: scratch copies of release label files from 2026-09-10. Compare them with the release labels
  first; they may be hard links of those files (section 5, B14), in which case deleting them frees nothing.
- `~/dis_renders`: five scratch PNGs named by BUU films (10.9 MB); owner-only until then.
- `$RS/data/morphdef`: three empty folders on Ceph; nothing moves. Remove them in a job; `rmdir` refuses a folder
  that is not empty: `sbatch -p reqp --qos=requeue --wrap 'd=/rs/rs_grp_oschome/go2432/data/morphdef; rmdir "$d/logs" "$d/out" "$d/src" "$d"'`.
- Not candidates: `~/s1v11` (the v11 build's audit trail, flagged irreplaceable) and `~/qc.tar.gz` (possibly the only
  copy of the propagation QC renders: `viz_propagation.py` wrote them under `data/placed`, which reclaim phase B lists).

<!-- BEGIN GENERATED: candidates -->
| path | batch | item_gb | candidate_gb | reason |
|---|---|---|---|---|
| ~/CTSpinoPelvic1K/data/tcia_nifti | B01 | 336.0 | 336.0 | regenerable from tcia/ by dcm2niix (336 GB) |
| ~/FluoroCap | B09 | 316.0 | 181.0 | directive D1 dropped FluoroCap from training; youtube/ (181 GB per AUDIT.json, 265 GB per MANIFEST) is the candidate |
| ~/CTSpinoPelvic1K/data/hf_export_osc | B02 | 227.0 | 227.0 | on reclaim phase A; the build archive (Zenodo 22647933) replaces it |
| ~/data/rsna_cspine | B08 | 203.3 | 203.3 | 203 GB zip used by nothing; every study refused by the header census |
| ~/CTSpinoPelvic1K/data/ctspine1k | B03 | 190.0 | 190.0 | duplicate of $RS/data/ctspine1k (152 GB, sha256-verified 2026-09-23); on reclaim phase A |
| ~/implant_verse | B06 | 187.0 | 187.0 | 187 GB synthetic, regenerable by tools/make_implant_ct.py |
| ~/spine-detector/data/raw/nhanes_annotated | B04 | 159.0 | 159.0 | extracted pickles 159 GB regenerate from the 1.0 GB zip |
| ~/scaling | B11 | 129.2 | 129.2 | 129 GB subset banks for the scaling curves (regenerable by tools/subset_bank.py) |
| ~/data/TotalSegmentator_v3 | B07 | 89.8 | 37.4 | keeps both the 37.4 GB zip and the unpacked tree (the zip is the candidate) |
| ~/data/TotalSegmentator | B07 | 82.0 | 23.6 | keeps both the 23.6 GB zip and the unpacked tree (the zip is the candidate) |
| ~/implant_ts | B07 | 39.0 | 39.0 | unfinished: 355 subjects never processed |
| ~/CTSpinoPelvic1K/data/ctpelvic1k | B03 | 36.0 | 36.0 | on reclaim phase A; re-downloadable from Zenodo 4588403 |
| ~/CTSpinoPelvic1K/data/placed | B02 | 6.1 | 6.1 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/XRSpinoPelvic1K/data/dataset2024.zip | B05 | 4.7 | 4.7 | the zip of the extracted BUU-LSPINE (4,023,726,207 B); the same file is on the laptop |
| ~/CTSpinoPelvic1K/data/hf_export_v6 | B02 | 4.6 | 4.6 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hf_export_v5 | B02 | 4.6 | 4.6 | on reclaim phase A; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hf_export_v4 | B02 | 2.8 | 2.8 | on reclaim phase A; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/zenodo_v6 | B02 | 2.3 | 2.3 | on reclaim phase A; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/v5_final | B02 | 2.3 | 2.3 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/zenodo_upload | B02 | 2.2 | 2.2 | on reclaim phase A; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hf_export_v2 | B02 | 2.1 | 2.1 | superseded build intermediate; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/s1_recarve | B02 | 1.6 | 1.6 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hardware_fix | B02 | 0.366 | 0.366 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hf_export_v2_work | B02 | 0.334 | 0.334 | on reclaim phase A; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/fix_0816 | B02 | 0.191 | 0.191 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/fix_0816_v3 | B02 | 0.19 | 0.19 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hip_crossover_backup | B02 | 0.051 | 0.051 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hf_export_v3_work | B02 | 0.039 | 0.039 | on reclaim phase A; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/v5_smoke | B02 | 0.034 | 0.034 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hardware_final_predust | B02 | 0.034 | 0.034 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/hardware_final | B02 | 0.034 | 0.034 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/dis_renders | B14 | 0.015 | 0.015 | scratch from the XRSpinoPelvic1K period: five PNGs named by BUU films (10,869,856 B); what drew them is not recorded |
| ~/pitest | B14 | 0.014 | 0.014 | scratch copies of release label files from the 2026-09-10 spinopelvic work; not yet compared with the release labels |
| ~/CTSpinoPelvic1K/data/hip_transpose_backup | B02 | 0.011 | 0.011 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/fix_0816_pseudo | B02 | 0.004 | 0.004 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/pdwtest | B14 | 0.003 | 0.003 | scratch copies of release label files from the 2026-09-10 spinopelvic work; not yet compared with the release labels |
| ~/CTSpinoPelvic1K/data/thoracic_fix | B02 | 0.003 | 0.003 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/fix_0816_v4 | B02 | 0.003 | 0.003 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/0816_label_v4.nii.gz | B02 | 0.002 | 0.002 | superseded build intermediate; the build archive (Zenodo 22647933) replaces it |
| ~/CTSpinoPelvic1K/data/fix_0816_pseudo_work | B02 | 0.001 | 0.001 | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/allspine_fov96_ctx | B11 |  |  | superseded by allspine_v9 |
| ~/allspine_v6_fov96_ctx | B11 |  |  | superseded by allspine_v9 |
| ~/allspine_v7nofluoro_fov96_ctx | B11 |  |  | FluoroCap ablation only |
| ~/build_archive | B02 |  |  | staging of the published build archive (Zenodo 22647933) |
| ~/build_archive_private | B02 |  |  | staging of the published build archive (Zenodo 22647933) |
| ~/build_archive_stage | B02 |  |  | staging of the published build archive (Zenodo 22647933) |
| ~/carm_base_cache | B10 |  |  | cache (regenerable) |
| ~/carm_base_cache_v9 | B10 |  |  | cache (regenerable) |
| ~/ctsp_drr_obl | B06 |  |  | misnamed VerSe renders; verse_drr_obl replaces them (AUDIT L247-L248) |
| ~/ctsp_drr_obl2 | B06 |  |  | misnamed VerSe renders; verse_drr_obl2 replaces them |
| ~/films_all2_fov128m_ctx | B11 |  |  | empty directory |
| ~/films_smoke | B10 |  |  | 3-film smoke test |
| ~/fluorogen | B09 |  |  | synth_rare (9.0 GB) is in no bank |
| ~/implant_ct_smoke | B11 |  |  | smoke test |
| ~/implant_verse_smoke | B11 |  |  | smoke test |
| ~/physics_smoke | B10 |  |  | smoke test |
| ~/postop_smoke | B10 |  |  | smoke test |
| ~/render_smoke | B10 |  |  | smoke test |
| ~/review_pack_smoke | B11 |  |  | smoke test |
| ~/ts_drr_v3 | B07 |  |  | no bank or arm reads it (AUDIT L360-L363) |
| ~/verse_soft_drr | B06 |  |  | row-spacing defect on 181 of 374; re-render or retire (AUDIT L252-L253) |
| ~/data/spondy_landmark | B14 |  |  | duplicate of ~/spine-detector/data/raw/mendeley_716 (B04): the same Mendeley release file, Dataset.zip 43,892,677 B; compare the sha256 that files.json records before deleting |
| $RS/data/morphdef | B14 |  |  | three empty folders (logs/, out/, src/) made 2026-09-23 02:15, the scaffold of the morphology-deformation work that was stopped that morning before anything was built (memory note morphology-deformation-feasibility); remove |
| ~/spine-detector/data/raw/buu_v1 | B04 |  |  | 38 images byte-identical to buu_full |
| ~/spine-detector/data/raw/cm_spine | B04 | 0.0 | 0.0 | empty directory |
| ~/CTSpinoPelvic1K/data/zenodo_v7 | B02 |  |  | on reclaim phase B; the build archive (Zenodo 22647933) replaces it |
| ~/lstv_flag/smoke | B11 |  |  | smoke test |
<!-- END GENERATED: candidates -->

Also worth a decision, not imaging: `~/singularity_cache` (38 GB on 2026-09-01, deleted once on 2026-09-20 and
rebuilt), `~/.cache` (103.9 GB on 2026-09-20), the B13 result trees. Not a deletion candidate but a security item:
`~/github` holds a GitHub personal access token in plain text (section 7); rotate the token, then delete the file.

## 9. Rollback

- Before FINALIZE: `sbatch -D "$PWD" --export=ALL,BATCH=<B>,ROLLBACK=1 cutover.sh` removes each symlink and renames
  `<path>.pre-ceph` back. The Ceph copy stays; delete it by hand if wanted.
- After FINALIZE: copy back with `rsync -aH --no-g <ceph path>/ <home path>/` in a job (the Ceph copy is the only one).
- A failed copy changes nothing on HOME; fix the cause and resubmit `migrate_batch.sbatch` (it resumes).

## 10. Expected end state

- Every imaging holding of the layout map under `$RS/data/<source>/`, each folder with a README.yaml, indexed in
  `$RS/data/_index/holding.sqlite`; every old HOME path a symlink.
- HOME: 4,050 GB on 2026-10-07 minus what B00-B11 and B14 actually move. The plan's own figures cannot give the end
  state. The sized move total of B00-B11 and B14 is 3,256.6 GB (shared hard-linked bytes counted once; 154 items
  unsized; B14 adds 0.3 GB sized and two unsized items, `~/s1v11` and `~/data/spondy_landmark`). What
  stays on HOME with a recorded size already sums to about 1,018 GB: `~/u251-xenograft-murine-RNASeq-study` 194,
  `nnunet/results` 348.6, `~/ablate` 234.8, `~/bench` 44, `~/.cache` 103.9, `~/singularity_cache` 38,
  `~/spinopelvic-seg` 27, `~/mambaforge` 14, `~/gcc-*` 13.7 (plan/disk_map.csv; section 8). Together that is about
  4,275 GB, more than the 4,050 GB HOME holds, before any unsized entry. So part of the sized move total is not on HOME
  any more. The likely parts are the 2026-09-01 du of the TCIA trees of B01 (1,057 GB; on no delete list, state after
  2026-09-01 not recorded) and the reclaim-listed B02 folders (64.1 GB net of shared bytes) and B03 copies (226 GB),
  which a memory note says were deleted on 2026-09-07. The 2026-10-08 first pass gave '4,050 - 3,189 = 861 GB, under
  1 TB'; that figure was wrong for the same reason. What can be said: after B00-B11 and B14, HOME keeps at least the
  ~1,018 GB listed (about 391 GB if B13 also moves), plus the unsized entries (`~/model_night`, the code checkouts,
  `~/spine-detector/runs`). Rewrite this paragraph from the census (job 40578909) and `build_plan.py --census`.
- Ceph: about 6 TB on 2026-10-07 plus what moves, roughly 9-10 TB of 20 TB, which leaves the 5 TB the acquisition
  fetcher requires.
- Open items that remain after the move: the unknowns tables of DATA_MANIFEST.md section 10, the three entries B14
  still inspects (two download leftovers and `~/spinopelvic-seg/nnunet/raw`), the token file `~/github` (section 7),
  the scripts of section 6, and the questions in VERIFICATION.md.
