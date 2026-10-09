# Deduplication plan for the imaging holding

Written 2026-10-08 by `build_dedup_plan.py` (this folder) from files on the laptop only: no grid, no network; revised the same day after a review (section 7). Nothing here deletes or moves anything. The only job that changes a file is `dedup_apply.sbatch`, and it only replaces a byte-identical duplicate on a finalized Ceph copy by a symlink to its canonical copy, hashing both sides again immediately before each swap. Every deletion below is a candidate for Greg, and every one must pass `dedup_guard.sh` first.

## The totals

| | |
|---|---|
| groups | **46**: 23 byte-identical (a; A20 and A21 dropped after the review, so 21 with plan rows), 12 same data in another container or processing (b), 11 same people across releases (c) |
| GB recoverable by symlinking byte-identical copies (a) | at most **95.8 GB** if every candidate hashes equal: 37.3 GB on recorded hashes (A05, A06, A11, A12, A15, A16), 38.6 GB likely (equal sizes, same writer: A14, A17, A18, A19), 19.9 GB possible (A01, A08, A22, A23); plus 0 to 56.1 GB in A03 (0 if the HF staging trees are hard links, as NPR stage 11 says). The largest single figure, A05's 32.3 GB, is the whole v2.0.1 unpacked tree, so the CT share is less (U5). |
| GB that are deletion candidates for Greg | **353.7 GB** now (b: ctsp_drr_obl + ctsp_drr_obl2 1.1; DeepFluoro vendor deposit zips 38.3; TotalSegmentator v2.0.1 + v3.0.0 zips 61.0; build_archive + build_archive_stage 9.3; BUU-LSPINE(2000) dataset2024.zip 4.0; NHANES extracted pickles (nhanes_annotated/extracted) 159.0; allspine v1, v6, v7nofluoro, extra, buu banks 80.9; 2D-3D-GS.zip 0.079), **218.3 GB** once a condition is met (VerSe canonical/ 67.0; labels_v10 1.1; scaling subset banks 129.2; allspine_v8 5.5; C-ArmLSpine.zip 15.6), and 0.46 GB of byte-identical files held for deletion rather than linking (A04 glgl*, A09 0533 work copy, A13 '(1)' files). A07 (1.19 GB) waits for Greg to read ~/s1v11. |
| subjects to alias in the index (c) | **1,631 concrete alias rows over 830 subjects** in `index_aliases.csv` (VerSe 37 series -> 18 subjects; 802 TCIA PatientIDs, 20 of them spelled by rule, and 782 CTSpine1K COLONOG volumes -> 802 CTSP persons, 2 COLONOG volumes kept as their own subjects; 6 DeepFluoro 8x names; 2 BUU byte pairs), 12 rule rows, 0 candidate rows, 29 written-out TotalSegmentator rows that wait for a release-qualified key scheme, and 6 families (about 13,498 rows, the 29 TotalSegmentator rows included) to generate on the grid from named tables (TS fingerprints, VinDr annotations, Mendeley anns, the April manifests, TIERS). |

Four things decide when any of this can run:

1. **Nothing is linked before its batch is FINALIZED.** `plan/verify_transfer.py` records each entry's kind (file or link) and FINALIZE in `plan/cutover.sh` deletes `<src>.pre-ceph` only when that comparison and an rsync dry run show nothing (cutover.sh L25-L28). A file turned into a symlink before then makes FINALIZE keep the HOME copy for ever. The apply job refuses any member whose batch is not VERIFIED, cut over and finalized. No `runs/<B>/STATUS` is on this laptop (`plan/logs/` holds only `.gitkeep`), so whether B06 (VerSe, copied 2026-10-08 per the brief) or any other batch is finalized is not recorded here.

2. **A link keeps a double count.** Where a bank builder reads both names (A04 `glgl*`, A13 `(1)`), a symlink frees the bytes but every later bank still ingests the file twice. Those groups are held for Greg's deletion.

3. **The index sees links in two ways.** The generic and VerSe adapters skip symlinks (`db/build_index.py` L353, L732), so a file replaced by a link would vanish from its source's count; the TotalSegmentator adapter tests `os.path.exists(ct)` (L694), which follows the link, and `item()` stats through it (L210-L226: nlink of the target is 1, so no `duplicate_of`), so a linked v2 CT stays a counted item of its own. `INDEX_ALIASES.md` says what the indexer must read from the ledgers: set `duplicate_of` and `counted = 0` on the dup path, updating the item where the indexer already holds or still walks it, adding it where it does not.

4. **Nothing that a link points at is deleted.** Every canonical root of a plan row was checked here against 77 deletion candidates (the kind-(b) members whose role names a candidate, and the 66 rows of `plan/layout_map.csv` that MIGRATION_PLAN section 8 is generated from): none is a candidate or lies inside one, and `build_dedup_plan.py` refuses to write a plan where one does. Candidates that lie inside a canonical root but can never be one of its group's canonical files: $RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3/Totalsegmentator_dataset_v300.zip in A05 ($RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3); $RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3/Totalsegmentator_dataset_v300.zip in A06 ($RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3); $RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels_v10 in A09 ($RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K). After linking, the ledgers (`applied/<gid>.ledger.tsv` and the copy in `$RS/dedup_ledgers/`) name every canonical file; `dedup_guard.sh <path>` exits 1 while any live link has its canonical in that path. Run it before deleting any candidate in this plan or in MIGRATION_PLAN section 8 (a request to that plan, which this folder does not edit).

What the hash is expected to overturn or confirm, said before it runs: A02 none (canonical/ holds no byte copies by construction); A03 mostly `same_inode` (hard links); A08 nothing (v10 scratch copies have no v11 twin); A22 different (v9 adds a `person` array); A17/A18 identical (npz members carry a fixed 1980 date); A01 CTs may match while VerSe'20 masks and centroids differ.

## 0. Keys used in the citations

`~` = `/wsu/home/go/go24/go2432` (HOME); `$RS` = `/rs/rs_grp_oschome/go2432` (Ceph). AUDIT = `docs/DATA_COMPLETENESS_AUDIT.md`; MDMR = `docs/MANIFEST_DATA_MODELS_RESULTS.md`; PIS = `docs/PATIENT_IDENTITY_SPEC.md`; ACC = `docs/DATA_ACCOUNTING.md`; XDU = `docs/XRAY_DATASET_USAGE.md`; DM = `data_platform/DATA_MANIFEST.md` (card or line); MP = `data_platform/MIGRATION_PLAN.md`; LAY = `data_platform/LAYOUT.md`; BI = `data_platform/db/build_index.py`; PRB = `data_platform/plan/path_refs_by_item.csv` (code files naming the exact HOME path); T2-REFS = code files naming a sub-path anywhere in ssn:, ctsp: and the VerSeFusion clone; T2-VF = a tally of the laptop copy of the grid VerSeFusion metadata; VFR = `NextPaper/VerSeFusion` (the VerSeFusion code); VFG = `NextPaper/VerSeFusion_grid_derived` (laptop copy of the grid tree's metadata); NPR = `NextPaper/README.md`; CEN-H / CEN-C / CEN-J = the 2026-10-08 censuses of HOME after FluoroCap (job 40580052), of Ceph (job 40580051) and of HOME (job 40578909); `mem:` = a memory note; `sd:` = the spine-detector repository; U<n> = an unknown in the topic notes (section 6). Sizes are apparent bytes / 1e9. The topic notes behind this plan (byte-identical groups, same data in other containers, same subjects across releases) were written the same day in the session scratchpad and are condensed here.

## 1. VerSe and VerSeFusion, in full

Every VerSe member in the holding, the kind of duplicate it is, and what happens to it. The detail is in the group sections that follow (A01-A04, B01-B02, C01).

| member | current path | Ceph target (B06 unless said) | GB | kind | rank | action |
|---|---|---|---:|---|---:|---|
| raw/verse20 | `~/VerSeFusion/data/raw/verse20` | `$RS/data/versefusion/raw/VerSeFusion_data/raw/verse20` | not sized | canonical of A01 | 1 | KEEP |
| raw/verse19 | `~/VerSeFusion/data/raw/verse19` | `$RS/data/versefusion/raw/VerSeFusion_data/raw/verse19` | not sized | a (A01): 95 series also in verse20 | 1 | LINK-AFTER-HASH the byte twins; the rest stays |
| raw/ (both) | `~/VerSeFusion/data/raw` | `$RS/data/versefusion/raw/VerSeFusion_data/raw` | 71.000 | origin | 1 | KEEP |
| unified/ | `~/VerSeFusion/data/unified` | `$RS/data/versefusion/raw/VerSeFusion_data/unified` | 0.088 | links only | 2 | KEEP (49 code files) |
| canonical/ | `~/VerSeFusion/data/canonical` | `$RS/data/versefusion/raw/VerSeFusion_data/canonical` | 67.000 | b (B01); a-check (A02); never a canonical root | 3 | KEEP; CANDIDATE 67 GB on four conditions |
| hf_staging* | `~/VerSeFusion/data/hf_staging*` | `$RS/data/versefusion/raw/VerSeFusion_data/hf_staging*` | 56.100 | a (A03), copies or hard links | 4 | LINK-AFTER-HASH plain copies of raw/ and corrected/ files |
| HF repos | `HF gregoryschwingmdphd/VerseFusion(-Sample, -LSTV)` | `(remote)` | not sized | b (B01) | 4 | Greg: public or not (U5) |
| HF copies of the 14 veridah_applied scans | `(inside hf_staging* and the HF repos)` | `-` | not sized | model output, as corrected/ | 5 | rank with corrected/ |
| corrected/ | `~/VerSeFusion/data/corrected` | `$RS/data/versefusion/raw/VerSeFusion_data/corrected` | 0.122 | b (B01): model output (verse559, verse642: manual confirmation claimed, not recorded) | 5 | KEEP, labelled model output |
| manifest/, qc/, lstv/, orientation/ | `~/VerSeFusion/data/...` | `$RS/data/versefusion/raw/VerSeFusion_data/...` | not sized | tables | - | KEEP |
| vf_813 | `~/vf_813` | `$RS/data/versefusion/derived/vf_813` | 58.000 | b (B01): lossy conversion | 6 | KEEP (Dataset815); never whole-spine |
| vf_v10 | `~/vf_v10` | `$RS/data/versefusion/derived/vf_v10` | not sized | b (B01): relabelled vf_813 | 6 | KEEP or CANDIDATE |
| vf_813_probe | `~/vf_813_probe` | `$RS/data/versefusion/derived/vf_813_probe` | not sized | unknown | - | CANDIDATE after one look |
| vf_morphometrics | `~/vf_morphometrics` | `(no layout row)` | not sized | results, not a copy | - | KEEP |
| bench_ts | `~/bench_ts` | `$RS/data/multisource_banks/derived/bench_ts` | 1.511 | second labeller | 7 | KEEP; index as automatic |
| verse_drr | `~/verse_drr` | `$RS/data/versefusion/derived/verse_drr` | not sized | a (A04): 13 glgl + 344 glverse | - | KEEP; Greg deletes the twins |
| verse_drr_obl, _obl2 | `~/verse_drr_obl*` | `$RS/data/versefusion/derived/verse_drr_obl*` | not sized | canonical of B02 | - | KEEP |
| ctsp_drr_obl, _obl2 | `~/ctsp_drr_obl*` | `$RS/data/versefusion/derived/ctsp_drr_obl*` | 1.096 | b (B02): from vf_813, misnamed | - | CANDIDATE after repointing readers |
| verse_drr_film | `~/verse_drr_film` | `$RS/data/versefusion/derived/verse_drr_film` | not sized | styled twin | - | KEEP |
| verse_soft_drr | `~/verse_soft_drr` | `$RS/data/versefusion/derived/verse_soft_drr` | not sized | other physics, defect | - | migration candidate (MP L494), not counted |
| implant_verse | `~/implant_verse` | `$RS/data/versefusion/derived/implant_verse` | 187.000 | synthetic, new content | - | migration candidate (MP L439), not counted |
| anomaly_harvest/verse, rare_class | `(Ceph-native)` | `$RS/data/anomaly_harvest/verse; $RS/data/rare_class` | not sized | derived | - | KEEP |
| series vs subject | `-` | `-` | not sized | c (C01): 374 series, 355 subjects | - | 37 alias rows |

**Quality order** (expert over automatic, complete over partial, corrected over superseded, original bytes over re-encoded, citable over private): raw/ (the VerSe'20 copy over the VerSe'19 copy) > unified/ (no bytes of its own) > canonical/ (the same expert content re-encoded in PIR) > HF staging and repos, except the 14 veridah_applied scans, whose staged masks are VERIDAH output and rank with corrected/ > corrected/ (VERIDAH output on 14 scans; never truth: AUDIT L948; for the two applied label_override scans, verse559 and verse642, NPR L443-L446 claims a manual confirmation that no record shows, and NPR L311-L312 claims it for all 14) > vf_813 (lossy: C1-T9 sent to ignore) > vf_v10 > bench_ts (automatic labels).

**Is canonical/ byte-identical to raw/, only a transpose, and does it add anything?** Not byte-identical: the 315 scans not stored in PIR were reoriented and written again with a new gzip stream and header, and the 59 already in PIR are symlinks to raw/ (VFR `reorient.py` L96-L120; the 59 from `tools/convert_versefusion.py`), by the laptop copy of the code; the grid code that wrote canonical/ is not on the laptop (U1), so A02 hashes it. In content it is a transpose: a permutation and flip of axes, not a resample (VFR `docs/design.md` L58-L60; `utils/nifti.py` L95-L102), which the orientation audit is consistent with (374 of 374 in PIR at their native spacing). Voxel equality with raw/ and the survival of CT scaling are claimed, not measured (U2). It adds PIR arrays and PIR centroids, saves about ten minutes of reorientation for the corpus (NPR L203), and is the input path of corrected/, qc/, orientation/, manifest/ and the HF export; no code file in this repository or CTSpinoPelvic1K names it (T2-REFS). So it is kind (b): kept now, a 67 GB deletion candidate after a voxel-equality job, the repointing of corrected/ and manifest/, the HF-export decision, and `dedup_guard.sh` passing on it. Because it is a deletion candidate, no plan row uses it as a canonical root (A03 no longer does).

## 2. Kind (a): byte-identical copies (symlink candidates)

Same bytes under two paths. `dedup_hash.sbatch` pairs and hashes them on the Ceph copies; `dedup_apply.sbatch` replaces the duplicate by a symlink to the canonical copy. Groups held by the plan (`hold` column) are hashed but not linked until `ALLOW_HOLD=<gid>`. Dropped groups have no plan rows: neither job touches them.

| id | group | status | at most GB | hold | gate |
|---|---|---|---:|---|---|
| A01 | VerSe'19 copies of the 95 series also held as VerSe'20 copies, inside raw/ | POSSIBLE | 14.400 | - | B06 |
| A02 | VerSe canonical/ files that are byte copies of raw/ files (a check) | NOT EXPECTED | 0 | - | B06 |
| A03 | VerSeFusion HF staging trees against raw/ and corrected/ | UNKNOWN | 56.100 | - | B06 |
| A04 | verse_drr doubled-prefix renders: glgl* = gl*, path/glverse* = path/verse* | CONFIRMED | 0.200 | removal_preferred | B06 |
| A05 | TotalSegmentator v2.0.1 ct.nii.gz = v3.0.0 ct.nii.gz (paired by bytes, never by s####) | CONFIRMED | 32.317 | - | B07 |
| A06 | TotalSegmentator v3.0.0 duplicates inside the release: s1446 = s1445, s2109 = s2110 = s2107 | CONFIRMED | 0.080 | - | B07 |
| A07 | CTSpinoPelvic1K v11 build output labels (s1v11/out/v11_labels) = the release labels | LIKELY | 1.189 | greg_review | B02 + B14 |
| A08 | Scratch label copies ~/pitest and ~/pdwtest = release labels (v10 expected) | LIKELY | 0.017 | - | B02 + B14 |
| A09 | CTSpinoPelvic1K CT 0533: the release file = the repair work-tree candidate | LIKELY | 0.250 | record_only | B02 |
| A10 | The April release inputs ($RS/data/ctsp_april) against the v11 release CTs (a check) | UNKNOWN | 0 | record_only | B02 |
| A11 | BUU-LSPINE v1 smoke set (buu_v1) inside buu_full | CONFIRMED | 0.040 | - | B04 |
| A12 | BUU-LSPINE(2000) JPEGs = the buu_full JPEGs | CONFIRMED | 4.000 | - | B04 + B05 |
| A13 | BUU '(1)' unzip collisions inside buu_full | CONFIRMED | 0.007 | removal_preferred | B04 |
| A14 | Mendeley 5jdfdgp762 downloaded twice (spondy_landmark = mendeley_716) | LIKELY | 0.089 | - | B04 + B14 |
| A15 | AASCE grid copy against the open mirror (the 962 identical files) | CONFIRMED | 0.859 | - | B04 |
| A16 | FluoroCap render subsets: fluorocap_drr_smoke and fluorocap_pack inside fluorocap_drr | CONFIRMED (smoke) / UNKNOWN (pack) | 0 | - | B09 |
| A17 | films_all2_fov96_ctx: rung_3, 4, 6, 8 and full = rung_2 | LIKELY | 17.886 | - | B11 |
| A18 | films_ann_fov96_ctx (the headline bank): rung_3, 4, 6, 8 and full = rung_2 | LIKELY | 9.388 | - | B11 |
| A19 | base_val/rung_1.npz in the eight C-arm mix banks = the carm_mix copy | LIKELY | 11.240 | - | B11 |
| A20 | C-ArmLSpine frame .npy in the eight fold banks = carm_drr | DROPPED (review 2026-10-08) | 0 | dropped (no plan rows) | B10 |
| A21 | spine-detector yolo* exports = data/interim/images | DROPPED (review 2026-10-08) | 0 | dropped (no plan rows) | B04 |
| A22 | allspine_v8 rung files against allspine_v9 | UNSETTLED (expected to differ) | 5.494 | - | B11 |
| A23 | cut_physics_v2 and cut_rare_v2 anns against v1 | UNSETTLED | 0.010 | - | B11 |

### A01. VerSe'19 copies of the 95 series also held as VerSe'20 copies, inside raw/

Status: **POSSIBLE**. Gate: B06 finalized. Hold: -. At most 14.400 GB recoverable (estimate; 71.7 KB (two masks) is on record).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `~/VerSeFusion/data/raw/verse20` | `$RS/data/versefusion/raw/VerSeFusion_data/raw/verse20` | not sized | part of raw/ 71 GB (AUDIT L662); 309 series-copies (AUDIT L940) | unified/ links of the 309 scans whose chosen release is verse20 (VFG unified metas, T2-VF section 1) |
| duplicate | `~/VerSeFusion/data/raw/verse19` | `$RS/data/versefusion/raw/VerSeFusion_data/raw/verse19` | 14.400 | estimate for the 95 shared series: 71 GB x 95 / 469 series-copies (AUDIT L662, L940) | unified/ links of the 65 scans whose chosen release is verse19 (55 VerSe'19-only + 10 stand-ins; VFG manifest source_dataset); 1 code file names data/raw (T2-REFS) |

- **Identity evidence.** 469 series-copies on disk for 374 scans: 160 VerSe'19 + 309 VerSe'20 (AUDIT L940); 95 scans carry other_releases = [verse19] with chosen release verse20 (VFG unified metas; T2-VF section 1). For: the two tiny masks verse201_seg (44.9 KB) and verse278_seg (26.8 KB) are byte-identical across releases (AUDIT L959). Against: VerSe'20 images are `<id>_CT-iso.nii.gz`, 'sagittal-iso resampled', and VerSe'20 centroids are in 1 mm iso ASL space (VFR src/verse_pipeline/utils/miccai.py docstring); VerSe'20 re-released overlapping series with corrected labels (AUDIT L952). CTs may match while masks and centroids differ, or nothing may match.
- **Confirm by.** $RS/data/versefusion/raw/VerSeFusion_data/raw/verse19/{*} paired BY BYTES with $RS/data/versefusion/raw/VerSeFusion_data/raw/verse20/{*} (sizes first, then sha256; a shared (verse|gl)[0-9]{3} token required).
- **Canonical:** `$RS/data/versefusion/raw/VerSeFusion_data/raw/verse20`. VerSe'20 is the corrected re-release (AUDIT L952) and unify's PREFERRED_RELEASE (VFR src/verse_pipeline/unify.py L66), so unified/ already reads the VerSe'20 copy of all 95.
- **Action.** LINK-AFTER-HASH, file by file: each VerSe'19 file whose bytes equal a VerSe'20 file becomes a symlink to it. Files without a twin stay. The 10 VerSe'20 series held only as their VerSe'19 copy (AUDIT L952) have no pair and are not touched; refetching them from VerSe'20 is a repair, not a deduplication. Identity: C01.
- unified/ links are absolute HOME spellings written with Path.absolute() (VFR unify.py L286-L291); they point at the VerSe'20 copy for the 95, so linking VerSe'19 files changes nothing they read. The apply job writes links in the $RS spelling (LAY L161-L164).


### A02. VerSe canonical/ files that are byte copies of raw/ files (a check)

Status: **NOT EXPECTED**. Gate: B06 finalized. Hold: -. At most 0 GB recoverable (0 expected by construction).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `~/VerSeFusion/data/raw` | `$RS/data/versefusion/raw/VerSeFusion_data/raw` | 71.000 | du 2026-09-01 (AUDIT L662) | see A01 |
| duplicate | `~/VerSeFusion/data/canonical` | `$RS/data/versefusion/raw/VerSeFusion_data/canonical` | 67.000 | du 2026-09-01 (AUDIT L662) | corrected/ (373 metas point their CT at canonical; T2-VF section 3), qc/ and orientation/ (input_dir), manifest/ and the HF export; 0 code files in ssn: or ctsp: (T2-REFS) |

- **Identity evidence.** By construction no regular file of canonical/ equals a raw/ file: a scan already in PIR is passed through as a symlink to its raw file (VFR src/verse_pipeline/reorient.py L96-L104); every other scan is reoriented with img.as_reoriented (VFR src/verse_pipeline/utils/nifti.py L95-L102) and re-saved by nib.save, a new gzip stream and header (reorient.py L106-L120). raw/ holds 59 scans already in PIR of 374 (ssn:tools/convert_versefusion.py docstring: LAS 216, PSR 67, PIR 59, LPS 31, LSP 1). The code that wrote canonical/ on the grid is not the laptop clone: the clone writes data/reoriented from sub-* folders and `git log -S data/canonical` finds nothing (T2 note, unknown U1).
- **Confirm by.** $RS/data/versefusion/raw/VerSeFusion_data/canonical/{*} paired BY BYTES with $RS/data/versefusion/raw/VerSeFusion_data/raw/{*} (sizes first, then sha256; a shared (verse|gl)[0-9]{3} token required).
- **Canonical:** `$RS/data/versefusion/raw/VerSeFusion_data/raw`. raw/ holds the release bytes; canonical/ is derived from it.
- **Action.** HASH ONLY in practice: expected verdict none. Any twin found is a pass-through written as a copy and may be linked to raw/. Whether canonical/ is a lossless transpose is a voxel question this hash cannot answer: see B01, step 1.


### A03. VerSeFusion HF staging trees against raw/ and corrected/

Status: **UNKNOWN**. Gate: B06 finalized. Hold: -. At most 56.100 GB recoverable (0 if hard links (NPR stage 11), up to the 56.1 GB census gap if copies).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/VerSeFusion/data/hf_staging*` | `$RS/data/versefusion/raw/VerSeFusion_data/hf_staging*` | 56.100 | upper bound: census 194.192 GB for VerSeFusion/data (CEN-H) minus 138.088 GB for raw + canonical + unified (AUDIT L662; layout_map row VerSeFusion/data) | the HF export stage (NPR stage 11); no code file in ssn: or ctsp: |
| canonical | `~/VerSeFusion/data/{raw,corrected}` | `$RS/data/versefusion/raw/VerSeFusion_data/{raw/verse20,raw/verse19,corrected}` | not sized | see A01; corrected/ 0.122 GB (AUDIT L666) | - |

- **Identity evidence.** The laptop copy of the grid tree has hf_staging_sample (10 scans) and hf_staging_lstv (68 scans) (VFG listing); the census counts 1,389 `.metadata` files (CEN-H top_ext), the marker huggingface_hub's large-folder upload writes per file. Staging is 'via copy (default) or symlink' (VFR src/verse_pipeline/hf_export.py docstring) but 'hardlink staging' in the later README (NPR stage 11). Hard links inside one item survive rsync -aH (plan/migrate_batch.sbatch L48-L51), so if they are hard links they share an inode on Ceph and free nothing. Raw VerSe'20 gl series are spelled in capitals (VFG unified/scan-gl003/scan-gl003_meta.json original paths: raw/verse20/01_training/GL003/GL003.nii.gz) while staging spells gl003; the hash job compares key tokens in lowercase, so a gl byte twin pairs instead of falling to key_mismatch.
- **Confirm by.** $RS/data/versefusion/raw/VerSeFusion_data/{hf_staging*/*} paired BY BYTES with $RS/data/versefusion/raw/VerSeFusion_data/raw/verse20 or $RS/data/versefusion/raw/VerSeFusion_data/raw/verse19 or $RS/data/versefusion/raw/VerSeFusion_data/corrected/{*} (sizes first, then sha256; a shared (verse|gl)[0-9]{3} token required).
- **Canonical:** `$RS/data/versefusion/raw/VerSeFusion_data/raw/verse20 | raw/verse19 | corrected (first match)`. raw/ first (original bytes; the VerSe'20 copy before the VerSe'19 copy, as A01 ranks them, so a staged file never pairs with a VerSe'19 file that A01 would replace), then corrected/ (a staged corrected mask exists only there). canonical/ is not a canonical root: it is B01's 67 GB conditional deletion candidate, and a link into it would lose its bytes the day it is deleted (review 2026-10-08).
- **Action.** LINK-AFTER-HASH for plain copies of raw/ and corrected/ files; nothing for hard links (same_inode). A staged copy of a reoriented scan (a canonical/ file) has no raw/ twin and stays a file until B01 decides canonical/. Whether the HF repos stay public is Greg's call (unknown U5).
- Expected 0 GB if NPR stage 11 is right about hard links.
- Rank: for the 14 veridah_applied scans the staged masks are VERIDAH output and rank with corrected/ (rank 5), not with the other HF copies (rank 4); see section 1.


### A04. verse_drr doubled-prefix renders: glgl* = gl*, path/glverse* = path/verse*

Status: **CONFIRMED**. Gate: B06 finalized. Hold: removal_preferred. At most 0.200 GB recoverable (estimate).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/verse_drr/{ann,img,path}/glgl*, path/glverse*` | `$RS/data/versefusion/derived/verse_drr` | 0.200 | estimate: 357 path files at the ctsp_drr/path mean (0.444 GB / 801 files, CEN-H) plus 13 renders | 38 code files name ~/verse_drr (PRB); the v9 bank ingests the 13 twice (AUDIT L958) |

- **Identity evidence.** 13 byte-identical renders glgl003..glgl146 = gl003..gl146 and 344 glverse* path duplicates (AUDIT L240-L243, L668; PIS section 3 row 9).
- **Confirm by.** $RS/data/versefusion/derived/verse_drr/{ann/glgl*|img/glgl*|path/glgl*|path/glverse*} against the same folder with the basename rewritten by glgl=>gl;glverse=>verse.
- **Canonical:** `$RS/data/versefusion/derived/verse_drr (the single-prefix files)`. The 2026-09-19 12h run that made the other 374 renders (AUDIT L668); the glgl* files are a 2026-09-20 re-prefixing that --resume did not recognise (AUDIT L240-L243).
- **Action.** HASH, then Greg deletes the 13 + 344 files (the audit's repair, AUDIT L240-L243) and restates verse_drr as 374. Held (removal_preferred): a symlink frees the bytes but keeps 387 anns for every bank builder, so the double count stays. ALLOW_HOLD=A04 links them if deletion is refused.
- Writers to fix before any rerun, or the twins come back: slurm/reproduce_all.sh L108 still passes `--prefix gl` to tools/make_drr_dataset.py for ~/verse_drr with --resume (the re-prefixing AUDIT L242-L243 names; its repair says 'fix the prefix logic in make_drr_dataset.py'); slurm/path_render.sh L40-L41 writes path files into ~/verse_drr with `--prefix gl --path-only --resume`, which is how a path file becomes `gl` + `verse###` = path/glverse###; slurm/verse_path_missing.sh L19 writes into ~/verse_drr with --resume (prefix empty). tools/make_drr_dataset.py L31's usage example still reads ~/vf_813 (C1-T9 sent to ignore) into ~/verse_drr.


### A05. TotalSegmentator v2.0.1 ct.nii.gz = v3.0.0 ct.nii.gz (paired by bytes, never by s####)

Status: **CONFIRMED**. Gate: B07 finalized. Hold: -. At most 32.317 GB recoverable (upper bound (whole v2 unpacked tree)).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `~/data/TotalSegmentator_v3` | `$RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3` | 89.759 | CEN-H (zip 37.416 + unpacked 52.344: AUDIT L485-L486) | 12 code files (PRB) |
| duplicate | `~/data/TotalSegmentator` | `$RS/data/totalsegmentator_v201/raw/TotalSegmentator` | 32.317 | upper bound: the whole v2 unpacked tree, 55.898 GB (CEN-H) minus the 23.581 GB zip (AUDIT L483); the CT share is not recorded (U5) | 17 code files (PRB); $RS/data/validation_ts/raw/* are links into $HOME/data/TotalSegmentator/<s>/ct.nii.gz (LAY L167) |

- **Identity evidence.** '1,118 of the 1,939 v3 subjects have a ct.nii.gz byte-identical to a v2 CT that already has a mask ... The join is by md5, never by s####' (AUDIT L1311-L1314). Over all CTs, 1,935 distinct scans and all 1,228 v2 folders map in (PIS L120). v2 s1406-s1429 are byte-identical to 24 other v3 ids (s1463, s1504, ... s2139) and the vacated numbers are other people (PIS section 3 row 6). md5, size, shape and affine of all 3,167 CTs: ~/ts_dupscan_out/ct_fingerprints.json (AUDIT L496).
- **Confirm by.** $RS/data/totalsegmentator_v201/raw/TotalSegmentator/{*/ct.nii.gz} paired BY BYTES with $RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3/{*/ct.nii.gz} (sizes first, then sha256).
- **Canonical:** `$RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3/Totalsegmentator_dataset_v300/s####/ct.nii.gz`. v3.0.0 is the corrected, current release (refined segmentations, v2 label mix-ups fixed: DM totalsegmentator_v201 card), holds every v2 CT (PIS L120), and is the hashed root ts_subjects (ssn:tools/data_manifest.py ROOTS).
- **Action.** LINK-AFTER-HASH, file by file: each v2 ct.nii.gz with a v3 twin becomes a link to it. segmentations/ and meta.csv are never touched (refined in v3: AUDIT L479; meta columns differ: PIS L120). The v2 CTs without a twin stay (110 by AUDIT L1311-L1313 if the 1,118 is all; U15). Keep one zip as the re-derivation origin until Greg decides B04.
- The link crosses Ceph source folders (totalsegmentator_v201 -> totalsegmentator_v300): a container that binds only the v2 folder sees it dangle; bind /rs/rs_grp_oschome/go2432 (LAY L154-L160).


### A06. TotalSegmentator v3.0.0 duplicates inside the release: s1446 = s1445, s2109 = s2110 = s2107

Status: **CONFIRMED**. Gate: B07 finalized. Hold: -. At most 0.080 GB recoverable (estimate).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300/{s1446,s2109,s2110}/ct.nii.gz` | `$RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3` | 0.080 | estimate: 3 x the v3 mean of 27 MB per subject (52.344 GB / 1,939; AUDIT L486) | as A05 |

- **Identity evidence.** s1445 = s1446 (and TS's own meta.csv puts them train and test), s2107 = s2109 = s2110; s2093 ~ s2094 is near, not equal (PIS L162).
- **Confirm by.** Totalsegmentator_dataset_v300/s1446/ct.nii.gz => Totalsegmentator_dataset_v300/s1445/ct.nii.gz; Totalsegmentator_dataset_v300/s2109/ct.nii.gz => Totalsegmentator_dataset_v300/s2107/ct.nii.gz; Totalsegmentator_dataset_v300/s2110/ct.nii.gz => Totalsegmentator_dataset_v300/s2107/ct.nii.gz.
- **Canonical:** `$RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3/Totalsegmentator_dataset_v300/{s1445,s2107}/ct.nii.gz`. The lowest id of each group; '1,939 - 4 duplicate ids' already counts the higher ids as repeats (PIS L120).
- **Action.** LINK-AFTER-HASH. s2093/s2094 is not in the group (not equal on record); it is a declared alias candidate in C03.


### A07. CTSpinoPelvic1K v11 build output labels (s1v11/out/v11_labels) = the release labels

Status: **LIKELY**. Gate: B02 + B14 finalized. Hold: greg_review. At most 1.189 GB recoverable (upper bound).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `~/data/CTSpinoPelvic1K/labels` | `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels` | 1.189 | 1,189,127,569 B (AUDIT L620) | 23 code files name CTSpinoPelvic1K/labels (T2-REFS) |
| duplicate | `~/s1v11/out/v11_labels` | `$RS/data/ctspinopelvic1k_build_tree/derived/s1v11/out/v11_labels` | 1.189 | upper bound: one copy of the 802 labels | 0 code files name ~/s1v11 (PRB); the v11 build workspace (MP L428) |

- **Identity evidence.** '389 .gz among the first 400 files listed' (DM ctspinopelvic1k_build_tree card); 'may be hard links of the release labels (not recorded)' (DM section 4 row 42). If they are hard links on HOME, B02 and B14 copy them in two rsync calls, and hard links cannot span two calls (LAY L174-L179), so on Ceph they become two copies.
- **Confirm by.** $RS/data/ctspinopelvic1k_build_tree/derived/s1v11/out/v11_labels/{*} paired BY BYTES with $RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels/{*} (sizes first, then sha256; a shared [0-9]{4} token required).
- **Canonical:** `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels`. The published v11 labels, checked 810 OK against Zenodo v11 SHA256SUMS.txt (AUDIT L620).
- **Action.** HASH; link only after Greg has read ~/s1v11 (flagged irreplaceable and owner-only until read for a token: MP L428, DM section 4 row 42, LAY rule 8). Held (greg_review).


### A08. Scratch label copies ~/pitest and ~/pdwtest = release labels (v10 expected)

Status: **LIKELY**. Gate: B02 + B14 finalized. Hold: -. At most 0.017 GB recoverable (recorded sizes; expected 0 (v10 copies have no v11 twin)).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/pitest` | `$RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pitest` | 0.014 | 13,899,387 B (MP section 8; notes G7) | 0 code files (PRB) |
| duplicate | `~/pdwtest` | `$RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pdwtest` | 0.003 | 2,710,749 B | 0 code files (PRB) |
| canonical | `~/data/CTSpinoPelvic1K/labels` | `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels` | 1.189 | 1,189,127,569 B (AUDIT L620) | 23 code files name CTSpinoPelvic1K/labels (T2-REFS) |

- **Identity evidence.** 'scratch copies of release label files ... may be hard links' (MP L423).
- **Confirm by.** $RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pitest/{*} paired BY BYTES with $RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels/{*} (sizes first, then sha256; a shared [0-9]{4} token required); $RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pdwtest/{*} paired BY BYTES with $RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels/{*} (sizes first, then sha256; a shared [0-9]{4} token required).
- **Canonical:** `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels`. The published v11 labels. labels_v10 is not a canonical root: it is B05's later deletion candidate, and a link into it would lose its bytes the day it is deleted (review 2026-10-08). Dated 2026-09-10, before v11 (2026-09-18, AUDIT L615), so the scratch files are expected to be v10 copies, which differ from v11 in every label file (id 29: AUDIT L913) and so find no twin here; they stay files, and Greg deletes them (MP L423).
- **Action.** LINK-AFTER-HASH what matches the v11 labels (expected: nothing); otherwise Greg deletes them (both are already deletion candidates, MP L423). The hash still answers whether they are copies of v11 files.


### A09. CTSpinoPelvic1K CT 0533: the release file = the repair work-tree candidate

Status: **LIKELY**. Gate: B02 finalized. Hold: record_only. At most 0.250 GB recoverable (recorded size).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `~/data/CTSpinoPelvic1K/ct/0533_ct.nii.gz` | `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/ct/0533_ct.nii.gz` | 0.250 | 250,067,995 B (AUDIT L1345-L1353) | 37 code files name CTSpinoPelvic1K/ct (T2-REFS) |
| duplicate | `(Ceph-native)` | `$RS/data/ctsp0533_repair/ct/0533_ct.nii.gz (or 0533_ct.cast.nii.gz)` | 0.250 | same file | ssn:slurm/ctsp0533_repair.sh |

- **Identity evidence.** The release file was installed by `cp $CAND ... && mv -f` from the work-tree candidate (ssn:slurm/ctsp0533_repair.sh L148-L169).
- **Confirm by.** ct/0533_ct.nii.gz => ct/0533_ct.nii.gz; ct/0533_ct.cast.nii.gz => ct/0533_ct.nii.gz.
- **Canonical:** `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/ct/0533_ct.nii.gz`. The release copy (250,067,995 B, sha256 478a74e9...a164d5; AUDIT L1345-L1353); the release must not depend on a work tree.
- **Action.** RECORD ONLY. The duplicate is Ceph-native work-tree output, which the apply job never replaces; the work-tree copy is a deletion candidate for Greg (0.25 GB). The truncated original (0533_ct.TRUNCATED.20e673dc6c2a.nii.gz) stays as the record of the defect.


### A10. The April release inputs ($RS/data/ctsp_april) against the v11 release CTs (a check)

Status: **UNKNOWN**. Gate: B02 finalized. Hold: record_only. At most 0 GB recoverable (unknown; most April CTs were re-resampled).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `(Ceph-native)` | `$RS/data/ctsp_april` | 86.883 | CEN-C (1,623 files) | 0 code files (T2-REFS); the NeurIPS appendix SPINEPS run (ssn:docs/RESUME_2026-09-22_PM.md L139) |
| canonical | `~/data/CTSpinoPelvic1K/ct` | `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/ct` | 192.813 | 192,813,331,872 B (AUDIT L619) | 37 code files (T2-REFS) |

- **Identity evidence.** The April CTs were re-resampled in part on 27 April (DM ctspinopelvic1k_april card); whether any file equals a v11 CT is not recorded (notes U4).
- **Confirm by.** $RS/data/ctsp_april/{*.nii.gz} paired BY BYTES with $RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/ct/{*.nii.gz} (sizes first, then sha256).
- **Canonical:** `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/ct`. The v11 release CT is the reference form of each person's CT (DM ctspinopelvic1k card).
- **Action.** RECORD ONLY (Ceph-native; feeds the B05 decision on ctsp_april).


### A11. BUU-LSPINE v1 smoke set (buu_v1) inside buu_full

Status: **CONFIRMED**. Gate: B04 finalized. Hold: -. At most 0.040 GB recoverable (estimate).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/spine-detector/data/raw/buu_v1` | `$RS/data/buu_lspine_v1_smoke/raw/buu_v1` | 0.040 | estimate: 38 images at the 1.0 MB mean JPEG of dataset2024.zip | 0 code files (PRB) |
| canonical | `~/spine-detector/data/raw/buu_full` | `$RS/data/buu_lspine_3600/raw/buu_full` | not sized | not in the census | 17 code files (PRB) |

- **Identity evidence.** 'all 77 byte-identical to buu_full' (MDMR L172); '38 images byte-identical to buu_full' (MP L497).
- **Confirm by.** $RS/data/buu_lspine_v1_smoke/raw/buu_v1/{*} paired BY BYTES with $RS/data/buu_lspine_3600/raw/buu_full/{*} (sizes first, then sha256; equal basenames required).
- **Canonical:** `$RS/data/buu_lspine_3600/raw/buu_full`. The complete 3,600-pair release, of which buu_v1 is a subset.
- **Action.** LINK-AFTER-HASH (or Greg deletes: already a candidate, MP L497). Both folders are owner-only (LAY rule 8), so the links stay inside one access class.


### A12. BUU-LSPINE(2000) JPEGs = the buu_full JPEGs

Status: **CONFIRMED**. Gate: B04 + B05 finalized. Hold: -. At most 4.000 GB recoverable (estimate).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/XRSpinoPelvic1K/data/BUU-LSPINE (*.jpg)` | `$RS/data/buu_lspine_2000/raw/BUU-LSPINE` | 4.000 | estimate: dataset2024.zip 4,023,726,207 B holds the 4,000 JPEGs plus 4,000 CSVs and the report (AUDIT L843) | 1 code file (PRB: slurm/plainfilm_recount.sh); ~/spine-detector/data/raw/buu_2000 is a symlink to it (LAY L167) |
| canonical | `~/spine-detector/data/raw/buu_full` | `$RS/data/buu_lspine_3600/raw/buu_full` | not sized | not in the census | 17 code files (PRB) |

- **Identity evidence.** 'all 4,000 JPEGs byte-identical, but 1,337 of 4,000 CSVs differ in column 5' (MDMR L171, L786).
- **Confirm by.** $RS/data/buu_lspine_2000/raw/BUU-LSPINE/{*.jpg} paired BY BYTES with $RS/data/buu_lspine_3600/raw/buu_full/{*.jpg} (sizes first, then sha256; equal basenames required).
- **Canonical:** `$RS/data/buu_lspine_3600/raw/buu_full`. The complete 3,600-pair release; every 2000 JPEG name is in it (AUDIT L843).
- **Action.** LINK-AFTER-HASH for the JPEGs only. The CSVs and the report stay: a different annotation vintage with posture labels (AUDIT L843).
- Both folders are owner-only (LAY rule 8).


### A13. BUU '(1)' unzip collisions inside buu_full

Status: **CONFIRMED**. Gate: B04 finalized. Hold: removal_preferred. At most 0.007 GB recoverable (estimate).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/spine-detector/data/raw/buu_full/**/*(1)*` | `$RS/data/buu_lspine_3600/raw/buu_full` | 0.007 | estimate: 7 JPEGs | 3 reach films_drr (AUDIT L852) |

- **Identity evidence.** Seven '(1)' files are md5-proven copies of their originals (AUDIT L829, L840, L852; PIS section 3 row 18).
- **Confirm by.** $RS/data/buu_lspine_3600/raw/buu_full/{*[(]1[)]*} against the same folder with the basename rewritten by (1)=>.
- **Canonical:** `$RS/data/buu_lspine_3600/raw/buu_full (the name without '(1)')`. The original file name of the release.
- **Action.** HASH, then Greg deletes them (held, removal_preferred): three reach films_drr, and a link would keep the double count.


### A14. Mendeley 5jdfdgp762 downloaded twice (spondy_landmark = mendeley_716)

Status: **LIKELY**. Gate: B04 + B14 finalized. Hold: -. At most 0.089 GB recoverable (census size).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/data/spondy_landmark` | `$RS/data/mendeley_5jdfdgp762/raw/spondy_landmark` | 0.089 | CEN-H (1,416 files) | 1 code file (PRB: tools/ct_inventory.py lists it as a CT root, DM section 4 row 41) |
| canonical | `~/spine-detector/data/raw/mendeley_716` | `$RS/data/mendeley_5jdfdgp762/raw/mendeley_716` | 0.200 | batch estimate (B04.tsv) | 5 code files (PRB) |

- **Identity evidence.** The same release file, Dataset.zip 43,892,677 B (MP L495; DM section 4 row 41); the sha256 that files.json records has not been compared.
- **Confirm by.** $RS/data/mendeley_5jdfdgp762/raw/spondy_landmark/{*} paired BY BYTES with $RS/data/mendeley_5jdfdgp762/raw/mendeley_716/{*} (sizes first, then sha256; equal basenames required).
- **Canonical:** `$RS/data/mendeley_5jdfdgp762/raw/mendeley_716`. The older download and the one the tools read (5 code files, PRB).
- **Action.** LINK-AFTER-HASH (or Greg deletes: already a candidate, MP L495). The index already skips raw/spondy_landmark (README.yaml index_skip).


### A15. AASCE grid copy against the open mirror (the 962 identical files)

Status: **CONFIRMED**. Gate: B04 finalized. Hold: -. At most 0.859 GB recoverable (upper bound).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/spine-detector/data/raw/aasce` | `$RS/data/aasce2019_boostnet/raw/aasce` | 0.859 | upper bound: the whole Ceph thoracic_xr folder is 0.859 GB (CEN-C) | 8 code files (PRB) |
| canonical | `(Ceph-native)` | `$RS/data/thoracic_xr/mirror_zlinzju_ke30_u7_AASCE2019` | not sized | inside thoracic_xr 0.859 GB (CEN-C) | 9 code files name thoracic_xr (T2-REFS) |

- **Identity evidence.** grid_copy_md5.json: 'identical 962, differing 98 = the 01-July-2019-* challenge test set, only in mirror 35' (sources.json aasce2019_boostnet acquired.cite); 'all 481 byte-identical to the mirror's boostnet training set' (AUDIT L570).
- **Confirm by.** $RS/data/aasce2019_boostnet/raw/aasce/{*} excluding *01-July-2019-* paired BY BYTES with $RS/data/thoracic_xr/mirror_zlinzju_ke30_u7_AASCE2019/{*} (sizes first, then sha256; equal basenames required).
- **Canonical:** `$RS/data/thoracic_xr/mirror_zlinzju_ke30_u7_AASCE2019`. The mirror is the superset (609 labelled against 481), pinned by a codeload zip md5 fe9430ab5c064c0d102d44810900e612 (sources.json aasce2019_boostnet), and Ceph-native, so it is never modified: the batch copy is the side that becomes links.
- **Action.** LINK-AFTER-HASH for the identical files. The 98 differing challenge-test files stay files on both sides until someone says which bytes are the original (U20); DM section 4 row 32 says keep both copies.


### A16. FluoroCap render subsets: fluorocap_drr_smoke and fluorocap_pack inside fluorocap_drr

Status: **CONFIRMED (smoke) / UNKNOWN (pack)**. Gate: B09 finalized. Hold: -. At most 0 GB recoverable (not sized (U9/U18)).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/fluorocap_drr_smoke` | `$RS/data/fluorocap/derived/fluorocap_drr_smoke` | not sized | not in the census (137 anns + .npy) | 0 code files (PRB) |
| duplicate | `~/fluorocap_pack` | `$RS/data/fluorocap/derived/fluorocap_pack` | not sized | not in the census (1,500 images) | 1 code file (PRB: tools/build_fluorocap_pack.py) |
| canonical | `~/fluorocap_drr` | `$RS/data/fluorocap/derived/fluorocap_drr` | not sized | not in the census (2,385 panels) | 3 code files (PRB) |

- **Identity evidence.** fluorocap_drr_smoke is a subset of fluorocap_drr: '137, byte-identical ann and .npy' (PIS section 3 row 19); fluorocap_pack shares 939 names with fluorocap_drr and 44 with the smoke set, bytes not recorded (PIS L129).
- **Confirm by.** $RS/data/fluorocap/derived/fluorocap_drr_smoke/{*} against $RS/data/fluorocap/derived/fluorocap_drr at the same relative path (files with no counterpart allowed); $RS/data/fluorocap/derived/fluorocap_pack/{*} paired BY BYTES with $RS/data/fluorocap/derived/fluorocap_drr/{*} (sizes first, then sha256).
- **Canonical:** `$RS/data/fluorocap/derived/fluorocap_drr`. The bank the smoke set was cut from and the review pack overlaps (PIS L129).
- **Action.** LINK-AFTER-HASH, or Greg deletes the FluoroCap banks whole: directive D1 dropped FluoroCap from training (MP L435).


### A17. films_all2_fov96_ctx: rung_3, 4, 6, 8 and full = rung_2

Status: **LIKELY**. Gate: B11 finalized. Hold: -. At most 17.886 GB recoverable (recorded sizes).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/films_all2_fov96_ctx/rung_{3,4,6,8,full}.npz` | `$RS/data/multisource_banks/derived/films_all2_fov96_ctx` | 17.886 | 5 x 3,577,265,632 B (MDMR L231) | 2 code files (PRB: tools/fluorocap_infer.py, tools/model_registry.py); 20 by name (T2-REFS) |

- **Identity evidence.** 'Rungs 2,3,4,6,8,full are the same file six times (3,577,265,632 B each)' (MDMR L231), on exact size equality plus md5 of three sampled 16 MiB blocks, 'not a full md5' (MDMR L795-L798). Equal arrays give equal bytes: np.savez_compressed writes each member through zipfile.ZipFile.open(name, 'w'), whose entries carry the fixed date 1980-01-01, so the write time does not enter the file (checked on the laptop on 2026-10-08 with numpy 2.5.3: two writes 3 s apart were byte-identical).
- **Confirm by.** rung_3.npz => rung_2.npz; rung_4.npz => rung_2.npz; rung_6.npz => rung_2.npz; rung_8.npz => rung_2.npz; rung_full.npz => rung_2.npz.
- **Canonical:** `$RS/data/multisource_banks/derived/films_all2_fov96_ctx/rung_2.npz`. The first saturated rung; the wider rungs of a short-film bank 'are literally the same file' (MDMR L214-L217).
- **Action.** LINK-AFTER-HASH. The canonical rung_2.npz is made read-only: tools/make_context_crops.py rewrites rung_<k>.npz in place (np.savez_compressed, L681-L686) and np.savez follows a symlink, so a rebuild would otherwise overwrite rung_2 through rung_3. The read-only bit turns such a rebuild into a crash (EACCES), so run ROLLBACK=1 for this group before any rebuild of the bank.
- Owner-only bank (holds BUU pixels; LAY rule 8).


### A18. films_ann_fov96_ctx (the headline bank): rung_3, 4, 6, 8 and full = rung_2

Status: **LIKELY**. Gate: B11 finalized. Hold: -. At most 9.388 GB recoverable (recorded sizes).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/films_ann_fov96_ctx/rung_{3,4,6,8,full}.npz` | `$RS/data/multisource_banks/derived/films_ann_fov96_ctx` | 9.388 | 5 x 1,877,620,575 B (MDMR L239) | 5 code files (PRB); 15 by name (T2-REFS) |

- **Identity evidence.** 'THE HEADLINE BANK ... Rungs 2..full all 1,877,620,575 B' (MDMR L239): sizes only.
- **Confirm by.** rung_3.npz => rung_2.npz; rung_4.npz => rung_2.npz; rung_6.npz => rung_2.npz; rung_8.npz => rung_2.npz; rung_full.npz => rung_2.npz.
- **Canonical:** `$RS/data/multisource_banks/derived/films_ann_fov96_ctx/rung_2.npz`. As A17.
- **Action.** LINK-AFTER-HASH; canonical made read-only (as A17). This is the headline bank: tools/make_context_crops.py rewrites every rung_<k>.npz in place (np.savez_compressed, L681-L686), and with rung_2.npz read-only a rebuild crashes on the first rung, so run ROLLBACK=1 for A18 before any rebuild.


### A19. base_val/rung_1.npz in the eight C-arm mix banks = the carm_mix copy

Status: **LIKELY**. Gate: B11 finalized. Hold: -. At most 11.240 GB recoverable (8 x 1.405 GB (CEN-H)).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/carm_cvmix0_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvmix0_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |
| duplicate | `~/carm_cvmix1_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvmix1_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |
| duplicate | `~/carm_cvmix2_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvmix2_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |
| duplicate | `~/carm_cvmix3_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvmix3_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |
| duplicate | `~/carm_cvmix4_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvmix4_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |
| duplicate | `~/carm_cvdaymix0_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvdaymix0_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |
| duplicate | `~/carm_cvdaymix1_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvdaymix1_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |
| duplicate | `~/carm_cvdaymix2_fov96_ctx/base_val/rung_1.npz` | `$RS/data/multisource_banks/derived/carm_cvdaymix2_fov96_ctx/base_val/rung_1.npz` | 1.405 | CEN-H | 0 to 4 code files each (PRB) |

- **Identity evidence.** Written by tools/merge_banks.py only when absent (L72-L75) from the base bank's validation crops; eight banks use --base ~/allspine_v7_fov96_ctx/rung_1.npz --base-cache $HOME/carm_base_cache (slurm/carmlspine_cv.sh L28-L29, slurm/carmlspine_cv_day.sh L38-L39) and carm_mix the same base without the cache (slurm/carmlspine_finetune.sh L28). base_val/meta.json differs per bank (mixed_from; merge_banks.py L77-L81) and is not in the group.
- **Confirm by.** $RS/data/multisource_banks/derived/carm_cvmix0_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path; $RS/data/multisource_banks/derived/carm_cvmix1_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path; $RS/data/multisource_banks/derived/carm_cvmix2_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path; $RS/data/multisource_banks/derived/carm_cvmix3_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path; $RS/data/multisource_banks/derived/carm_cvmix4_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path; $RS/data/multisource_banks/derived/carm_cvdaymix0_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path; $RS/data/multisource_banks/derived/carm_cvdaymix1_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path; $RS/data/multisource_banks/derived/carm_cvdaymix2_fov96_ctx/{base_val/rung_1.npz} against $RS/data/multisource_banks/derived/carm_mix_fov96_ctx at the same relative path.
- **Canonical:** `$RS/data/multisource_banks/derived/carm_mix_fov96_ctx/base_val/rung_1.npz`. The copy slurm/carmlspine_finetune.sh reads by path to score forgetting (L39-L40).
- **Action.** LINK-AFTER-HASH; canonical made read-only.
- carm_mix_fov96_ctx predates the 2026-09-23 C-ArmLSpine repair like every HOME carm_* bank (DM section 4 row 20), so it may be rebuilt. No launch script deletes it: slurm/carmlspine_finetune.sh builds it only when rung_1.npz is absent (L28) and tools/merge_banks.py writes base_val/rung_1.npz only when absent (L72-L75); the scripts that rm -rf are those of carm_drr (carmlspine_finetune.sh L23) and of the fold banks carm_cv*_drr (carmlspine_cv.sh L24, carmlspine_cv_day.sh L34, carmlspine_cv_v9.sh L29, carmlspine_cv_day_v9.sh L28). A rebuild that removes the folder must run ROLLBACK=1 for A19 first; dedup_guard.sh refuses the deletion while the links are live.


### A20. C-ArmLSpine frame .npy in the eight fold banks = carm_drr

Status: **DROPPED (review 2026-10-08)**. No plan rows: neither job hashes or links this group. 1.863 GB at most, by CEN-H, stays as it is.

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate (not linked) | `~/carm_cv0_drr/img` | `$RS/data/carmlspine/derived/carm_cv0_drr/img` | 0.237 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| duplicate (not linked) | `~/carm_cv1_drr/img` | `$RS/data/carmlspine/derived/carm_cv1_drr/img` | 0.258 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| duplicate (not linked) | `~/carm_cv2_drr/img` | `$RS/data/carmlspine/derived/carm_cv2_drr/img` | 0.252 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| duplicate (not linked) | `~/carm_cv3_drr/img` | `$RS/data/carmlspine/derived/carm_cv3_drr/img` | 0.235 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| duplicate (not linked) | `~/carm_cv4_drr/img` | `$RS/data/carmlspine/derived/carm_cv4_drr/img` | 0.260 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| duplicate (not linked) | `~/carm_cvday0_drr/img` | `$RS/data/carmlspine/derived/carm_cvday0_drr/img` | 0.172 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| duplicate (not linked) | `~/carm_cvday1_drr/img` | `$RS/data/carmlspine/derived/carm_cvday1_drr/img` | 0.220 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| duplicate (not linked) | `~/carm_cvday2_drr/img` | `$RS/data/carmlspine/derived/carm_cvday2_drr/img` | 0.229 | whole bank incl. anns (CEN-H) | 0 code files (PRB) |
| canonical (rejected) | `~/carm_drr` | `$RS/data/carmlspine/derived/carm_drr` | 0.252 | CEN-H | 2 code files (PRB) |

- **Identity evidence.** tools/carmlspine_to_bank.py writes img/<stem>.npy as the realxray PNG decoded to uint8 (np.save, L64); fold banks differ only in the ann split (L41-L51). All predate the 2026-09-23 repair (DM section 4 row 20). slurm/carmlspine_finetune.sh L22-L23 runs `rm -rf $HOME/carm_drr; tools/carmlspine_to_bank.py --out $HOME/carm_drr` whenever ~/carm_fov96_ctx/rung_1.npz is absent, and DM section 4 row 20 says every HOME carm_* bank predates the repair (296 frames then, 299 after; case118 relabelled), so a rebuild is expected. A read-only bit does not stop rm -rf. After A20 such a rebuild would leave the eight fold banks' images dangling, or resolving to repaired frames under their old anns; those fold banks are the frozen record of the published C-ArmLSpine CV numbers. The fold banks themselves are rm -rf'd and rebuilt by slurm/carmlspine_cv.sh L24, carmlspine_cv_day.sh L34 and their _v9 copies (L29, L28).
- **Confirm by.** not hashed (no plan rows).
- **Canonical:** `$RS/data/carmlspine/derived/carm_drr/img`. Would have been the bank the folds re-split. Not a safe canonical: a launch script deletes and rebuilds it (identity evidence).
- **Action.** DROPPED: no plan rows, so neither job touches these banks (1.86 GB at most). carm_drr is due for rebuild (DM section 4 row 20); if the fold banks are to be deduplicated later, link them to a frozen snapshot that no script writes, and change carmlspine_finetune.sh to build into a new folder.


### A21. spine-detector yolo* exports = data/interim/images

Status: **DROPPED (review 2026-10-08)**. No plan rows: neither job hashes or links this group. not sized (U15).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate (not linked) | `~/spine-detector/data/yolo/images` | `$RS/data/spine_detector_corpus/derived/yolo/images` | not sized | not in the census (U15) | 17 code files name ~/spine-detector/data/yolo* (PRB) |
| duplicate (not linked) | `~/spine-detector/data/yolo_v2/images` | `$RS/data/spine_detector_corpus/derived/yolo_v2/images` | not sized | not in the census (U15) | 17 code files name ~/spine-detector/data/yolo* (PRB) |
| duplicate (not linked) | `~/spine-detector/data/yolo_v3/images` | `$RS/data/spine_detector_corpus/derived/yolo_v3/images` | not sized | not in the census (U15) | 17 code files name ~/spine-detector/data/yolo* (PRB) |
| duplicate (not linked) | `~/spine-detector/data/yolo_v5f_p00/images` | `$RS/data/spine_detector_corpus/derived/yolo_v5f_p00/images` | not sized | not in the census (U15) | 17 code files name ~/spine-detector/data/yolo* (PRB) |
| duplicate (not linked) | `~/spine-detector/data/yolo_v5f_p05/images` | `$RS/data/spine_detector_corpus/derived/yolo_v5f_p05/images` | not sized | not in the census (U15) | 17 code files name ~/spine-detector/data/yolo* (PRB) |
| duplicate (not linked) | `~/spine-detector/data/yolo_v5f_p08/images` | `$RS/data/spine_detector_corpus/derived/yolo_v5f_p08/images` | not sized | not in the census (U15) | 17 code files name ~/spine-detector/data/yolo* (PRB) |
| duplicate (not linked) | `~/spine-detector/data/yolo_v6f/images` | `$RS/data/spine_detector_corpus/derived/yolo_v6f/images` | not sized | not in the census (U15) | 17 code files name ~/spine-detector/data/yolo* (PRB) |
| canonical (rejected) | `~/spine-detector/data/interim` | `$RS/data/spine_detector_corpus/derived/interim` | not sized | not in the census | 3 code files (PRB) |

- **Identity evidence.** sd:src/export_yolo.py copies data/interim/images/<image_id>.png into <out>/images/<split>/ with shutil.copy2 unless --symlink is given (L102-L128); which exports used --symlink is not recorded. B04 moves the yolo* exports as one hard-link group (MP section 5 B04; LAY L179). yolo_v4z (zoomed windows) and yolo_hw (crops) are not copies and are left out. sd:src/build_dataset.py _save (L40-L43) rewrites data/interim/images/<id>.png in place with cv2.imwrite and never checks its return value; its paths are repo-relative (INTERIM = Path('data/interim'), L36), run from WorkDir ~/spine-detector. After linking, a corpus rebuild either gives every yolo* export new pixels under its old labels (canonical writable) or, with the read-only bit, fails silently on every image while manifest.parquet is rewritten with new transforms, so images and boxes disagree and nothing raises.
- **Confirm by.** not hashed (no plan rows).
- **Canonical:** `$RS/data/spine_detector_corpus/derived/interim/images`. Would have been the export source. Not a safe canonical: it is the working output of the corpus builder, rewritten in place (identity evidence).
- **Action.** DROPPED: no plan rows, so neither job touches the exports. If they are to be deduplicated later, link both the exports and interim/ to a frozen snapshot that no script writes. names_member in dedup_lib.sh now also matches a path relative to a job's WorkDir, but that sees only jobs queued at apply time, not a later rebuild.
- Owner-only folders (LAY rule 8).


### A22. allspine_v8 rung files against allspine_v9

Status: **UNSETTLED (expected to differ)**. Gate: B11 finalized. Hold: -. At most 5.494 GB recoverable (upper bound; expected 0).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/allspine_v8_fov96_ctx` | `$RS/data/multisource_banks/derived/allspine_v8_fov96_ctx` | 5.494 | CEN-H | 5 code files (PRB) |
| canonical | `~/allspine_v9_fov96_ctx` | `$RS/data/multisource_banks/derived/allspine_v9_fov96_ctx` | 5.494 | CEN-H | 30 code files (PRB) |

- **Identity evidence.** v9 is 'v8 identical minus the subject keying' (AUDIT L678); equal sizes and film counts only (CEN-H; XDU). make_context_crops.py adds a person array only under --g3-split or --patient-json (L681-L685), so the files should differ.
- **Confirm by.** $RS/data/multisource_banks/derived/allspine_v8_fov96_ctx/{rung_*.npz} against $RS/data/multisource_banks/derived/allspine_v9_fov96_ctx at the same relative path.
- **Canonical:** `$RS/data/multisource_banks/derived/allspine_v9_fov96_ctx`. v9 is the shipped, subject-keyed bank (XDU header; AUDIT L678).
- **Action.** HASH; link only what matches (expected: nothing). v8 itself is a B09 candidate once its readers move to v9.


### A23. cut_physics_v2 and cut_rare_v2 anns against v1

Status: **UNSETTLED**. Gate: B11 finalized. Hold: -. At most 0.010 GB recoverable (CEN-H).

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| duplicate | `~/cut_physics_v2/ann` | `$RS/data/multisource_banks/derived/cut_physics_v2/ann` | 0.007 | CEN-H | 0 code files (PRB) |
| duplicate | `~/cut_rare_v2/ann` | `$RS/data/multisource_banks/derived/cut_rare_v2/ann` | 0.003 | CEN-H | 0 code files (PRB) |

- **Identity evidence.** 'Label-identical to v1 (pixels not compared)' (MDMR L300, L305, L806). The images come from two CUT generators (~/cut_v1, ~/cut_v2), so img/ should differ and is left out.
- **Confirm by.** $RS/data/multisource_banks/derived/cut_physics_v2/{ann/*} against $RS/data/multisource_banks/derived/cut_physics at the same relative path; $RS/data/multisource_banks/derived/cut_rare_v2/{ann/*} against $RS/data/multisource_banks/derived/cut_rare at the same relative path.
- **Canonical:** `$RS/data/multisource_banks/derived/cut_physics/ann | $RS/data/multisource_banks/derived/cut_rare/ann`. v1, the first of each pair.
- **Action.** HASH; link the anns that match.


## 3. Kind (b): the same data in another container, orientation or processing

Never linked (the bytes differ). Both copies stay when the second adds something; otherwise the lower-quality one is a deletion candidate for Greg. No job deletes any of them.

| id | group | now GB | later or conditional GB |
|---|---|---:|---:|
| B01 | VerSe and VerSeFusion: raw / unified / canonical / corrected / tables / HF staging / vf_813 / vf_v10 / vf_813_probe / vf_morphometrics / bench_ts | - | 67.000 |
| B02 | VerSe render banks rendered again from a worse source or with another physics | 1.096 | - |
| B03 | DeepFluoro: the H5 release, the vendor DICOM deposit, the Hugging Face re-host, the frame export | 38.300 | - |
| B04 | TotalSegmentator: the two release zips beside their unpacked trees, and the v2.0.1 tree beside v3.0.0 | 60.997 | - |
| B05 | CTSpinoPelvic1K: v11 and v10 labels, the HF mirror, the April release, the build archive and its staging | 9.272 | 1.074 |
| B06 | CTSpine1K: the HOME copy (gone) and the Ceph copy | - | - |
| B07 | BUU-LSPINE(2000): dataset2024.zip beside the extracted tree | 4.024 | - |
| B08 | NHANES II: CDC TIFFs, the Zenodo zip and its extracted pickles, and two render writers | 159.000 | - |
| B09 | Crop banks superseded by allspine_v9, and the scaling subset banks | 80.891 | 134.694 |
| B10 | Archives kept beside their unpacked trees (C-ArmLSpine, Ljubljana, Geneva, RibFrac) | 0.079 | 15.582 |
| B11 | FluoroCap stages: raw/ (PMC re-encodes) and raw_hires/ (publisher originals), youtube/ | - | - |
| B12 | COBRA frames counted up to four times (Ceph-native; already links or re-windowed) | - | - |

### B01. VerSe and VerSeFusion: raw / unified / canonical / corrected / tables / HF staging / vf_813 / vf_v10 / vf_813_probe / vf_morphometrics / bench_ts

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical (rank 1) | `~/VerSeFusion/data/raw` | `$RS/data/versefusion/raw/VerSeFusion_data/raw` | 71.000 | du 2026-09-01 (AUDIT L662) | unified/ (all 374 metas point into raw/; T2-VF section 1); 1 code file (T2-REFS) |
| keep: interface (rank 2) | `~/VerSeFusion/data/unified` | `$RS/data/versefusion/raw/VerSeFusion_data/unified` | 0.088 | AUDIT L662 (748 NIfTI links over 374 scan-*) | 49 code files (T2-REFS) |
| keep, later candidate (rank 3) | `~/VerSeFusion/data/canonical` | `$RS/data/versefusion/raw/VerSeFusion_data/canonical` | 67.000 | AUDIT L662 | corrected/ (373 metas), qc/, orientation/, manifest/, HF export; 0 code files in ssn:/ctsp: (T2-REFS); the laptop VerSeFusion clone names data/reoriented in 3 files |
| keep: model output (rank 5) | `~/VerSeFusion/data/corrected` | `$RS/data/versefusion/raw/VerSeFusion_data/corrected` | 0.122 | AUDIT L666 | manifest/ and the HF export (NPR stages 10-11) |
| keep: tables | `~/VerSeFusion/data/{manifest,qc,lstv,orientation}` | `$RS/data/versefusion/raw/VerSeFusion_data/{manifest,qc,lstv,orientation}` | not sized | small | manifest.csv: tools/patient_keys.py --verse-manifest default (L486); 12 code files (T2-REFS) |
| see A03 (rank 4; the 14 veridah_applied scans rank 5) | `~/VerSeFusion/data/hf_staging*` | `$RS/data/versefusion/raw/VerSeFusion_data/hf_staging*` | 56.100 | upper bound, see A03 | - |
| remote (rank 4; the 14 veridah_applied scans rank 5) | `HF gregoryschwingmdphd/VerseFusion, -Sample, -LSTV` | `(remote)` | not sized | '~22 GB' full corpus (NPR) | not carded in DATA_MANIFEST (U5) |
| keep: lossy conversion (rank 6) | `~/vf_813` | `$RS/data/versefusion/derived/vf_813` | 58.000 | MDMR 2.2 (layout_map) | 15 code files (PRB), 21 by name (T2-REFS); Dataset815 |
| keep or candidate (rank 6) | `~/vf_v10` | `$RS/data/versefusion/derived/vf_v10` | not sized | not sized | 5 code files (PRB) |
| candidate after one look | `~/vf_813_probe` | `$RS/data/versefusion/derived/vf_813_probe` | not sized | name and date 2026-09-12 only (layout_map) | 0 code files (PRB) |
| keep: results, no layout row | `~/vf_morphometrics` | `(stays on HOME: no layout row)` | not sized | not sized | 1 code file (T2-REFS: slurm/versefusion_tl_morphometrics.sh) |
| keep: second labeller (rank 7) | `~/bench_ts` | `$RS/data/multisource_banks/derived/bench_ts` | 1.511 | CEN-H | 31 code files (PRB) |
| keep: Ceph-native derived | `(Ceph-native)` | `$RS/data/anomaly_harvest/verse; $RS/data/rare_class` | not sized | not sized | layout_map 'already on CEPH' |

- **What differs.**
  - unified/ holds no pixel data: every meta.json points into raw/ (ct 374, mask 374, preview 224; T2-VF section 1). LAY L156-L159 says its links reach raw/ and canonical/; the metas say raw/ only (U3).
  - canonical/ against raw/:
    - Bytes: not byte copies. 315 scans were reoriented and re-saved (new gzip stream and header) and the 59 scans already in PIR are symlinks to raw/, by the laptop code (VFR reorient.py L96-L120; ssn:tools/convert_versefusion.py docstring for the 59). The grid code that wrote canonical/ is not on the laptop (U1); A02 hashes it.
    - Content: a permutation and flip of voxel axes, not a resample (VFR docs/design.md L58-L60; utils/nifti.py L95-L102 img.as_reoriented). The orientation audit read canonical/ and found 374 of 374 in PIR with native spacing, 74 of them 1 mm isotropic (VFG orientation/orientation_audit.json), so NPR's '1 mm isotropic' (NPR L54) is wrong. Masks are cast back to their source dtype (reorient.py L116-L118). Not measured: voxel equality with raw/ after the recorded transform, and whether CT scaling survived (as_reoriented reads np.asanyarray(dataobj), which applies scl_slope; nib.save re-applies the on-disk dtype) (U2).
    - What it adds: PIR arrays and PIR centroid JSON (the MICCAI'20 centroids are in 1 mm iso ASL space; VFR utils/miccai.py docstring); it saves one reorientation, '~10 min' for the corpus (NPR L203); and it is the input path of corrected/ (373 metas point CT at canonical, 14 keep msk_canonical as the pre-correction mask; T2-VF section 3), qc/ and orientation/ (input_dir), manifest/ and the HF export. The project's own code reorients in memory instead (mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine).
  - corrected/ is VERIDAH output on 14 scans (12 t13_shift, 2 label_override), 360 pass through (VFG corrected/veridah_manifest.json); the manifest's has_T13 = 18 counts the corrected tree, the release masks give 6 (AUDIT L948; DM section 4 row 10). The two applied label_override scans are verse559 and verse642 (veridah_applied true); verse606 also carries a label_override entry that was not applied (error length_mismatch:mask=18,override=19) (VFG corrected/veridah_manifest.json). NPR L443-L446 says the 2 label_override corrections 'were further confirmed by manual review'; NPR L311-L312 says all 14 'were also confirmed by independent visual inspection'. The two statements disagree and neither names a review record, so all 14 stay model output here, with a manual confirmation claimed, not recorded, for verse559 and verse642.
  - The HF export stages the corrected masks (NPR stage 11 ships veridah_manifest.json; A03: a staged corrected mask exists only in corrected/), so for the 14 veridah_applied scans the HF staging copies and the HF repos hold model output and rank with corrected/ (rank 5), not with the other HF copies (rank 4).
  - vf_813 is a second PIR copy of every CT cast to int16, with C1-T9 and the coccyx sent to ignore and TotalSegmentator rib pseudolabels (ssn:tools/convert_versefusion.py docstring and L190-L198; DM versefusion card): 'fatal for anything needing C2' (mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine). Whether the int16 cast is lossless is U8.
  - vf_v10 maps vf_813 labels to the CTSP v10 ids for measurement only (ssn:tools/ds813_to_v10.py docstring). bench_ts is SPINEPS+VERIDAH output over 1,228 TS v2 + 374 VerSe CTs, a second labeller, not a copy (AUDIT L489).
- **Canonical:** `$RS/data/versefusion/raw/VerSeFusion_data/raw`. The release bytes and the expert masks, and the origin every other member is rebuilt from (DM verse19_20 and versefusion re-acquisition recipes). Within raw/, the VerSe'20 copy of a series ranks above its VerSe'19 copy (A01).
- **Quality order / why.** Quality order: raw (VerSe'20 > VerSe'19) > unified (no bytes of its own) > canonical (re-encoded; voxel equality claimed, not measured) > HF staging and repos (except the 14 veridah_applied scans, whose staged masks rank with corrected/) > corrected (model output; manual confirmation claimed, not recorded, for verse559 and verse642) > vf_813 (lossy) > vf_v10 (relabelled) > bench_ts (automatic labels).
- **Action.** raw/, unified/, corrected/ (labelled model output), tables, vf_813 (never a whole-spine source), bench_ts (indexed as an automatic labeller): KEEP. canonical/: KEEP now; CANDIDATE for Greg (67 GB) once (1) the voxel-equality job passes on all 374, (2) corrected/ and manifest/ are repointed to raw/ or re-derived (373 corrected metas name canonical paths), (3) the HF export's fate is decided (U5), and (4) dedup_guard.sh passes on canonical/: no dedup ledger has a live link into it (A03 no longer uses canonical/ as a canonical root, so none is expected; the guard checks rather than assumes). vf_v10: KEEP or CANDIDATE (regenerable with one command). vf_813_probe: CANDIDATE after one look (U9). Writers to fix so the vf_813 renders and the verse_drr twins are not recreated: see A04's note (slurm/reproduce_all.sh L108, slurm/path_render.sh L40-L41, slurm/verse_path_missing.sh L19, tools/make_drr_dataset.py L31).
- **Deletion candidates for Greg.** VerSe canonical/ 67.000 GB (conditional: after the voxel-equality job, the repointing of corrected/ and manifest/, the HF-export decision, and dedup_guard.sh passing on canonical/).


### B02. VerSe render banks rendered again from a worse source or with another physics

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `~/verse_drr` | `$RS/data/versefusion/derived/verse_drr` | not sized | not sized | 38 code files (PRB); glgl* in A04 |
| canonical | `~/verse_drr_obl, verse_drr_obl2` | `$RS/data/versefusion/derived/verse_drr_obl, verse_drr_obl2` | not sized | not sized (1,494 / 2,989 renders: AUDIT L670) | 12 and 10 code files (T2-REFS) |
| candidate | `~/ctsp_drr_obl, ctsp_drr_obl2` | `$RS/data/versefusion/derived/ctsp_drr_obl, ctsp_drr_obl2` | 1.096 | 0.366 + 0.730 (CEN-H) | PRB 1 for the exact path (slurm/fluorogen_generate.sh); 18 code files contain the name (T2-REFS): repoint them first |
| keep: styled twin | `~/verse_drr_film` | `$RS/data/versefusion/derived/verse_drr_film` | not sized | not sized | 2 code files (T2-REFS) |
| not a duplicate | `~/verse_soft_drr` | `$RS/data/versefusion/derived/verse_soft_drr` | not sized | not sized | 2 code files (T2-REFS) |
| not a duplicate | `~/implant_verse` | `$RS/data/versefusion/derived/implant_verse` | 187.000 | MDMR 2.2 | 0 code files (PRB) |

- **What differs.**
  - ctsp_drr_obl (1,256) and ctsp_drr_obl2 (2,511) are the same 314 VerSe series rendered from ~/vf_813, whose maps send C1-T9 to ignore, under a CTSP prefix; 60 series are missing (AUDIT L245-L248; MDMR L348-L355; PIS section 3 row 8). Whether any img/*.npy equals a verse_drr_obl image is not recorded, and tools/make_oblique_drr.py is not in the repository (U8).
  - verse_drr_film is a film-styled twin with the same boxes (slurm/film_lora_apply.sh L13-L14), dated 2026-09-17, before the spacing fix (AUDIT L670; U19).
  - verse_soft_drr is a soft-tissue render with the row-spacing defect on 181 of 374 (AUDIT L250-L253): another physics, not a copy. implant_verse is 1,119 synthetic hardware CTs from 373 series (verse116 missing): new content, regenerable by tools/make_implant_ct.py (MP L439).
- **Canonical:** `$RS/data/versefusion/derived/verse_drr, verse_drr_obl, verse_drr_obl2`. Rendered from unified/ (the release masks), complete labels, and after the row-spacing fix (verse_drr clean on 387/387: AUDIT L250-L253).
- **Quality order / why.** Misnamed renders from the lossy source, with complete replacements on disk.
- **Action.** ctsp_drr_obl, ctsp_drr_obl2: CANDIDATE (1.1 GB; MP L482-L483) after their readers move to verse_drr_obl*. verse_drr, verse_drr_obl*, verse_drr_film: KEEP. verse_soft_drr and implant_verse are deletion candidates of the migration plan (MP L494, L439) for other reasons; they are not duplicates and are not counted here. Fix the writers listed in A04's note before any rerun, or a rerun recreates the doubled prefixes and the vf_813 route.
- **Deletion candidates for Greg.** ctsp_drr_obl + ctsp_drr_obl2 1.096 GB (now: after repointing their readers).


### B03. DeepFluoro: the H5 release, the vendor DICOM deposit, the Hugging Face re-host, the frame export

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| keep: labels and poses | `~/deepfluoro/unpacked_full/ipcai_2020_full_res_data.h5` | `$RS/data/deepfluoro_h5/raw/deepfluoro` | 2.542 | 2,541,608,861 B (DM deepfluoro_h5) | 18 code files (T2-REFS) |
| keep: small | `~/deepfluoro/data (IFSXNV zips)` | `$RS/data/deepfluoro_h5/raw/deepfluoro/data` | 2.594 | CEN-H (3 files) | 1 code file; ~/user/diffdrr_data points at it (LAY L168; U13) |
| keep: second H5 | `~/deepfluoro/unpacked` | `$RS/data/deepfluoro_h5/raw/deepfluoro/unpacked` | 0.042 | CEN-H; by size the ds_8x release (U11) | - |
| keep: original pixels | `(Ceph-native)` | `$RS/data/deepfluoro_vendor/unpacked` | 72.709 | 72,708,547,975 B (DM deepfluoro_vendor) | 17 code files (T2-REFS) |
| candidate | `(Ceph-native)` | `$RS/data/deepfluoro_vendor/*.zip (the deposit zips: the 19 deposit files less the rotations table)` | 38.300 | 37,381,313 KB of zips (AUDIT L713) = 110.987 GB folder (CEN-C) minus the unpacked tree | the unpack script only |
| keep: rotations table | `(Ceph-native)` | `$RS/data/deepfluoro_vendor/02_fluoroscopy_rotations.tab.part` | 0 | 18,345 B (DM deepfluoro_vendor card; AUDIT L173) | the per-frame rotation table, 2,659 rows expected (DM deepfluoro_vendor card; AUDIT L170-L173) |
| keep while PolyPose reads it | `(Ceph-native)` | `$RS/data/polypose/hf/.../xvr-data/.../deepfluoro` | not sized | not sized (polypose folder 87.713 GB with conda envs; U12) | 10 code files name xvr-data (T2-REFS) |
| keep: export | `(Ceph-native)` | `$RS/data/realxray/deepfluoro` | not sized | part of 3.408 GB (CEN-C) | - |

- **What differs.**
  - 'not byte-identical - different containers, different compression' (ACC lines 17-24); the vendor deposit holds about seven times the H5's frames (2,659 against 366) plus pre- and post-operative CT (AUDIT L730). The HF re-host's poses need a 180-degree flip (ssn:tools/polypose_apply_pose_flip.py) and its identity with the H5 was checked by slurm/polypose_identity.sh with an unrecorded result (DM deepfluoro_xvr_hf card; U11).
- **Canonical:** `H5 for labels and poses; vendor DICOM for original pixels`. Pixels: the vendor DICOM ranks first (original vendor bytes and headers; the H5 frames are processed display images: DM deepfluoro_h5 'Modality'). Truth: the H5 ranks first (only it carries poses, segmentations and landmarks; 2,293 of the 2,659 vendor frames have no released pose: DM deepfluoro_vendor card).
- **Quality order / why.** Three containers of one cadaver set; each ranks first for something except the re-host.
- **Action.** H5, vendor unpacked/, IFSXNV zips, export, the rotations table: KEEP with the roles above. Vendor zips (the zips alone; 02_fluoroscopy_rotations.tab.part is not a zip and stays): CANDIDATE (38.3 GB) only after (1) an `unzip -l` of every zip is compared, name by name and size by size, with unpacked/ in a job, because the first unpack run was OOM-killed with 0 bytes landed (AUDIT L713) and no zip-against-unpacked check is recorded (NHANES has one: zip-against-disk found 0 unextracted, job 40416364, DM nhanes2_zenodo_landmarks card); the card also lists a joined/ folder beside the zips, unsized here, which the comparison should account for; and (2) the .tab.part rename is settled (U14). unpacked/ is what every reader and the hashed root deepfluoro_vendor use, and the deposit re-downloads with byte checks (DM deepfluoro_vendor recipe). HF re-host: KEEP while PolyPose reads it, then CANDIDATE (unsized). Identity: C05.
- **Deletion candidates for Greg.** DeepFluoro vendor deposit zips 38.300 GB (now: after an unzip -l comparison with unpacked/ and the .tab.part check).


### B04. TotalSegmentator: the two release zips beside their unpacked trees, and the v2.0.1 tree beside v3.0.0

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| candidate | `~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300.zip` | `$RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3/Totalsegmentator_dataset_v300.zip` | 37.416 | 37,415,622,057 B (AUDIT L485) | - |
| candidate | `~/data/TotalSegmentator/Totalsegmentator_dataset_v201.zip` | `$RS/data/totalsegmentator_v201/raw/TotalSegmentator/Totalsegmentator_dataset_v201.zip` | 23.581 | 23,581,218,285 B (AUDIT L483) | - |
| keep | `~/data/TotalSegmentator/s####/segmentations, meta.csv` | `$RS/data/totalsegmentator_v201/raw/TotalSegmentator` | not sized | inside 32.317 GB | ts_drr, physics_drr (1,831 TS renders), anchor_drr, implant_ts, bench_ts, validation_ts (AUDIT L487-L499) |

- **What differs.**
  - 'keeps both the zip and the unpacked tree (the zip is the candidate)' (MP L442-L443); each zip re-downloads with its Zenodo md5 (v3 md5 0728beea...: AUDIT L1307-L1309). v2.0.1 has vertebra label mix-ups that v3 fixes (DM totalsegmentator_v201 card, citing ssn:tools/ts_to_drr.py L16-L19); 110 v2 CTs have no byte twin in v3 if the 1,118 of AUDIT L1311-L1313 is the full count (U15).
- **Canonical:** `the unpacked v3.0.0 tree (CTs), with v2.0.1 kept for the banks built from it`. v3.0.0 is the corrected release; v2.0.1 is what every live TS bank read.
- **Quality order / why.** Archives beside their unpacked trees.
- **Action.** Both zips: CANDIDATE (61.0 GB); keep one until A05 has linked and Greg has chosen. v2.0.1 segmentations and meta.csv: KEEP (live banks; superseded for new work). ts_drr_v3 is a migration candidate (no bank or arm reads it: AUDIT L360-L363; MP L493), not a duplicate.
- **Deletion candidates for Greg.** TotalSegmentator v2.0.1 + v3.0.0 zips 60.997 GB (now: keep one until A05 is applied).


### B05. CTSpinoPelvic1K: v11 and v10 labels, the HF mirror, the April release, the build archive and its staging

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `~/data/CTSpinoPelvic1K/{ct,labels}` | `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | 194.002 | 192.813 CT + 1.189 labels (AUDIT L619-L620); the folder is 196.195 GB with labels_v10 (CEN-H) | 76 code files (PRB) |
| keep, later candidate | `~/data/CTSpinoPelvic1K/labels_v10` | `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels_v10` | 1.074 | 1,074,444,805 B (AUDIT L621) | 8 code files (T2-REFS) |
| remote: stale | `HF OpenSpineConsortium/CTSpinoPelvic1K labels/` | `(remote)` | not sized | - | never a label source: v10 (mem:hf-mirror-is-v10) |
| remote: not the release | `HF gregoryschwingmdphd/CTSpinoPelvic1K` | `(remote)` | not sized | 1,000 + 1,000 files (AUDIT L618) | - |
| keep: superseded release inputs | `(Ceph-native)` | `$RS/data/ctsp_april` | 86.883 | CEN-C (1,623 files) | the NeurIPS appendix SPINEPS numbers (ssn:docs/RESUME_2026-09-22_PM.md L139); A10 hashes it |
| candidate | `~/build_archive` | `$RS/data/ctspinopelvic1k_build_tree/derived/build_archive` | 6.237 | CEN-H (13 files, 9 .tar.zst) | 2 code files (PRB) |
| candidate | `~/build_archive_stage` | `$RS/data/ctspinopelvic1k_build_tree/derived/build_archive_stage` | 3.035 | CEN-H (2,474 files) | 2 code files (PRB) |
| keep: owner-only key | `~/build_archive_private` | `$RS/data/ctspinopelvic1k_build_tree/derived/build_archive_private` | 0 | CEN-H (one JSON: annotator_map.json) | 2 code files (PRB): ctsp:scripts/archive_reviews.py writes it, ctsp:slurm/archive_build_inputs.sh L87 names it |
| absent | `~/CTSpinoPelvic1K/data/{hf_export_osc,hf_export_v2..v6,v5_final,zenodo_v6,zenodo_v7,s1_recarve,...}` | `-` | 0 | ~/CTSpinoPelvic1K/data holds 16 files, 13,697,321 B on 2026-10-08 (CEN-J) | 176 ctsp: build scripts name hf_export_v* (T2-REFS): the build chain reads folders that no longer exist |

- **What differs.**
  - v10 and v11 differ only in id 29: every label file differs, the vertebral voxels do not (AUDIT L913; mem:s1-carve-changed-spinopelvic; ctsp:CLAUDE.md). The build archive is the 13 files of Zenodo 10.5281/zenodo.22647933 as uploaded, md5-checked (mem:zenodo-deposit); build_archive_stage is the unpacked 04_reviews, 08 and 09 components of the same archive (DM build-tree card).
- **Canonical:** `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K (ct/ + labels/ v11)`. Zenodo v11 = grid labels/ (sha256 810 OK, AUDIT L620): citable, current, corrected. The CTs are byte-identical on the grid and on HF (AUDIT L898).
- **Quality order / why.** One current release, one superseded, one stale mirror, one archive with its staging, and the private key the archive must not contain.
- **Action.** ct/ + labels/: KEEP. labels_v10: KEEP as 'superseded v10, for v10-era comparisons'; CANDIDATE (1.07 GB) once the code that gates on 29 is retired with it (ctsp:CLAUDE.md). HF mirror: index only; refreshing it to v11 is publishing, not deduplication. ctsp_april: KEEP while the NeurIPS appendix depends on it. build_archive, build_archive_stage: CANDIDATE (MP L477-L479; 9.27 GB): the citable deposit holds the same files; keeping one Ceph copy as offline insurance is Greg's call. build_archive_private: KEEP, owner-only. It holds annotator_map.json, the only key from the annotator_NN pseudonyms in the deposited reviews to the students; archive_reviews.py writes it outside the archive on purpose so it is never deposited (ctsp:scripts/archive_reviews.py docstring; L132-L135 write it and chmod 600; ctsp:slurm/archive_build_inputs.sh L87). It can be rebuilt (handles sorted, L103-L104) only while the three HF review repositories stay unchanged. MP section 8 lists it as 'staging of the published build archive'; that reason does not hold for this file. Absent folders: B02 rows resolve ABSENT at preflight.
- **Deletion candidates for Greg.** build_archive + build_archive_stage 9.272 GB (now); labels_v10 1.074 GB (later: after the id-29 code is retired).


### B06. CTSpine1K: the HOME copy (gone) and the Ceph copy

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| canonical | `(Ceph-native)` | `$RS/data/ctspine1k` | 162.350 | CEN-C (2,020 files) | 6 code files name data/ctspine1k (T2-REFS) |
| absent | `~/CTSpinoPelvic1K/data/ctspine1k` | `-` | 0 | 190 GB on 2026-09-01 (_du_data.txt); absent on 2026-10-08 (CEN-J) | 4 ctsp: build scripts name the repository-relative data/ctspine1k (download_raw.sh L180, create_dataset.sh L129, verify_mask_seriesuid.sh L20, diagnose_series.py L30) |

- **What differs.**
  - MP L438 lists the HOME copy as a duplicate of the Ceph copy (sha256-verified 2026-09-23); the census of 2026-10-08 no longer finds it (CEN-J).
- **Canonical:** `$RS/data/ctspine1k`. Complete (1,005 volumes), every file checked against the HF listing's size and LFS sha256 (DM ctspine1k card).
- **Quality order / why.** Already resolved by an unrecorded removal (notes U1).
- **Action.** Nothing to delete. B03's CTSpine1K row resolves ABSENT at preflight; point the four build scripts at the Ceph copy before any rerun of the April build chain. The COLONOG people: C02.


### B07. BUU-LSPINE(2000): dataset2024.zip beside the extracted tree

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| candidate | `~/XRSpinoPelvic1K/data/dataset2024.zip` | `$RS/data/buu_lspine_2000/raw/dataset2024.zip` | 4.024 | 4,023,726,207 B (MP L447) | - |

- **What differs.**
  - A laptop copy of the same size is at <repo XRSpinoPelvic1K 4f22935>/dataset2024.zip (notes, section 4).
- **Canonical:** `$RS/data/buu_lspine_2000/raw/BUU-LSPINE (extracted) and buu_full (A12)`. The extracted tree is what tools read; its JPEGs equal buu_full's (A12).
- **Quality order / why.** An archive beside its extracted tree, with a second copy on the laptop.
- **Action.** CANDIDATE (4.0 GB; MP L447).
- **Deletion candidates for Greg.** BUU-LSPINE(2000) dataset2024.zip 4.024 GB (now).


### B08. NHANES II: CDC TIFFs, the Zenodo zip and its extracted pickles, and two render writers

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| keep: original films | `~/spine-detector/data/raw/nhanes_full` | `$RS/data/nhanes2_cdc_films/raw/nhanes_full` | 91.000 | B04.tsv | - |
| candidate: extracted pickles | `~/spine-detector/data/raw/nhanes_annotated/extracted` | `$RS/data/nhanes2_zenodo_landmarks/raw/nhanes_annotated/extracted` | 159.000 | MP L440 | - |
| keep: the release zip | `~/spine-detector/data/raw/nhanes_annotated/NHANESII_Annotations_VertebralOsetophytes.zip` | `$RS/data/nhanes2_zenodo_landmarks/raw/nhanes_annotated/NHANESII_Annotations_VertebralOsetophytes.zip` | 1.017 | 1,017,496,285 B (DM nhanes2_zenodo_landmarks card) | sd:src/build_dataset.py do_nhanes reads it (L47-L48) |
| keep: pseudo labels | `~/nhanes_pseudo` | `$RS/data/nhanes2_cdc_films/derived/nhanes_pseudo` | 74.000 | B10.tsv | nhanesps bank |
| keep: render writers | `~/films_drr (NHANES part), ~/nhanes_drr` | `$RS/data/multisource_banks/derived/films_drr, $RS/data/nhanes2_zenodo_landmarks/derived/nhanes_drr` | not sized | - | different banks |

- **What differs.**
  - 'extracted pickles 159 GB regenerate from the 1.0 GB zip' (MP L440); the pickles carry pixels (L00452's pixels survive only inside the pickle: ssn:slurm/film_corpus_inventory.sh L46-L50), and the zip keeps them. nhanes_pseudo saves (img0 * 255).astype(uint8) as .npy (ssn:tools/pseudolabel_real_films.py L322): re-encoded pixels with pseudo labels that exist nowhere else. films_drr and nhanes_drr come from two writers with different windowing (ssn:tools/manifest_to_drr_format.py L122; ssn:tools/nhanes_to_drr_format.py L126).
- **Canonical:** `$RS/data/nhanes2_cdc_films/raw/nhanes_full (pixels) + the Zenodo zip (landmarks)`. Original films; the 1.0 GB zip regenerates the 159 GB of pickles.
- **Quality order / why.** An archive's extracted copy at 159 times its size.
- **Action.** Extracted pickles (nhanes_annotated/extracted only): CANDIDATE (159 GB). TIFFs, the zip, nhanes_pseudo, render banks: KEEP. The zip, NHANESII_Annotations_VertebralOsetophytes.zip, sits in nhanes_annotated/ beside extracted/ (DM nhanes2_zenodo_landmarks card, 'Where it is now') and is the only local copy of the expert per-level masks (543 pkl) and of L00452's pixels, which have no TIFF. A request to the migration plan, not made here: plan/batch_items/B04.tsv L2 and the nhanes_annotated row of plan/layout_map.csv (MP L440) flag the whole nhanes_annotated folder as the candidate; narrow both to extracted/. Identity (the double inclusion that leaked 48 of 54 validation patients): C04.
- **Deletion candidates for Greg.** NHANES extracted pickles (nhanes_annotated/extracted) 159.000 GB (now: the zip beside it stays).


### B09. Crop banks superseded by allspine_v9, and the scaling subset banks

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| candidate | `~/allspine_fov96_ctx` | `$RS/data/multisource_banks/derived/allspine_fov96_ctx` | 4.542 | CEN-H | 2 code files (PRB) |
| candidate | `~/allspine_v6_fov96_ctx` | `$RS/data/multisource_banks/derived/allspine_v6_fov96_ctx` | 23.018 | CEN-H | 4 code files (PRB) |
| candidate | `~/allspine_v7nofluoro_fov96_ctx` | `$RS/data/multisource_banks/derived/allspine_v7nofluoro_fov96_ctx` | 31.068 | CEN-H | 0 code files (PRB) |
| candidate | `~/extra_fov96_ctx` | `$RS/data/multisource_banks/derived/extra_fov96_ctx` | 12.282 | CEN-H | 4 launch and cleanup scripts (T2-REFS) |
| candidate | `~/buu_fov96_ctx` | `$RS/data/buu_lspine_3600/derived/buu_fov96_ctx` | 9.981 | CEN-H | 0 code files (PRB) |
| candidate (conditional) | `~/scaling` | `$RS/data/multisource_banks/derived/scaling` | 129.200 | B11.tsv | 3 code files (PRB); cut from the deleted allspine_v2 by every launch script |
| candidate | `~/merged_ctx` | `$RS/data/multisource_banks/derived/merged_ctx` | not sized | not sized | 2 code files (PRB) |
| keep, later candidate | `~/allspine_v8_fov96_ctx` | `$RS/data/multisource_banks/derived/allspine_v8_fov96_ctx` | 5.494 | CEN-H | 5 code files (PRB) |
| keep | `~/allspine_v9_fov96_ctx, allspine_v7_fov96_ctx` | `$RS/data/multisource_banks/derived/allspine_v9_fov96_ctx, allspine_v7_fov96_ctx` | 14.611 | CEN-H | 30 and 15 code files (PRB) |

- **What differs.**
  - Re-cuts of the same render and film folders with other mixes, splits and keyings (MDMR section 3). v6 and v7 carry the NHANES double inclusion and the CTSP cross-naming leak (mem:nhanes-double-inclusion; mem:split-leak-cross-naming); v8 puts five VerSe people on both sides (PIS section 3 row 7). extra and buu are all-train pools whose films are in the shipped or holdout banks (MDMR L236, L243; XDU). merged_ctx is m_mask22_scale_ctx minus the scale array (MDMR L248). The scaling banks copy their parent's rows into each new file (ssn:tools/subset_bank.py docstring and L108).
- **Canonical:** `$RS/data/multisource_banks/derived/allspine_v9_fov96_ctx (shipped) and allspine_v7_fov96_ctx (holdout bank)`. v9 is keyed by subject across sources (mem:split-leak-cross-naming); v7 is the holdout path for 57 references (MP L213-L216).
- **Quality order / why.** Superseded or regenerable re-cuts of the same rows.
- **Action.** v1, v6, v7nofluoro (MP L474-L476), extra, buu, merged_ctx (MP candidates table): CANDIDATE (80.9 GB sized). scaling: CANDIDATE only once the scaling figures are frozen. MP section 8 calls them 'regenerable by tools/subset_bank.py', but every launch cuts them from ~/allspine_v2_fov96_ctx (slurm/leads_chain.sh L56-L57, slurm/film_lora_apply.sh L51, slurm/scaling_sweep.sh L27 and L38), and that bank was deleted on 2026-09-20 (mem:grid-quota-and-deleted-banks). Regenerating them needs allspine_v2 rebuilt from render sources that have changed since, so the result would not be the same bytes. v8: KEEP until its readers move to v9, then CANDIDATE (5.5 GB). v9, v7: KEEP. films_all2 and films_ann: KEEP the banks; their rung files are A17 and A18.
- **Deletion candidates for Greg.** allspine v1, v6, v7nofluoro, extra, buu banks 80.891 GB (now); scaling subset banks 129.200 GB (conditional: once the scaling figures are frozen; regenerable only after rebuilding allspine_v2, and not byte-identical); allspine_v8 5.494 GB (later: after its 5 readers move to v9).


### B10. Archives kept beside their unpacked trees (C-ArmLSpine, Ljubljana, Geneva, RibFrac)

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| candidate (conditional) | `(Ceph-native)` | `$RS/data/carmlspine/C-ArmLSpine.zip` | 15.582 | 15,581,614,253 B (AUDIT L710) | - |
| candidate | `(Ceph-native)` | `$RS/data/ljubljana/2D-3D-GS.zip` | 0.079 | 79,049,365 B (AUDIT L715); a laptop copy of the same size (ctsp:2D-3D-GS.zip) | - |
| keep | `(Ceph-native)` | `$RS/data/geneva_hip_src (archive)` | not sized | folder 1.111 GB | - |
| keep until labels are placed | `~/data/ribs (RibFrac image zips, RibSeg v2, Moller masks)` | `$RS/data/ribfrac (only -image.nii.gz extracted)` | 78.699 | HOME 78.699 GB, 89 files; Ceph 78.200 GB, 661 files (DM ribfrac card) | - |

- **What differs.**
  - The Geneva manifest hashed the 69-file work directory, not the 482-file source archive (DM section 4 row 26), so the archive is the only release-original form. RibFrac is 'held twice, as zips on HOME and unzipped images on Ceph' (DM ribfrac card), but only the -image files were extracted, so the zips still hold what the Ceph tree lacks.
- **Canonical:** `the unpacked trees, except Geneva and RibFrac (below)`. Readers and hashed roots use the unpacked trees.
- **Quality order / why.** Archives beside unpacked trees.
- **Action.** C-ArmLSpine.zip: CANDIDATE (15.6 GB) once the deposit is confirmed to still serve it with its MD5 (C-ArmLSpine.zip.ok). 2D-3D-GS.zip: CANDIDATE (0.08 GB). Geneva archive: KEEP. RibFrac zips: KEEP until their label members sit beside the Ceph images; then the image part is redundant (Greg).
- **Deletion candidates for Greg.** 2D-3D-GS.zip 0.079 GB (now); C-ArmLSpine.zip 15.582 GB (conditional: the deposit still serves it).


### B11. FluoroCap stages: raw/ (PMC re-encodes) and raw_hires/ (publisher originals), youtube/

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| keep | `~/FluoroCap/raw` | `$RS/data/fluorocap/raw/FluoroCap/raw` | 2.270 | AUDIT L759 | panels cut from it (U30) |
| keep | `~/FluoroCap/raw_hires` | `$RS/data/fluorocap/raw/FluoroCap/raw_hires` | not sized | 2,080 files (AUDIT L759) | 1 code file (T2-REFS) |
| not a duplicate (migration candidate) | `~/FluoroCap/youtube` | `$RS/data/fluorocap/raw/FluoroCap/youtube` | 181.000 | AUDIT L761 | 0 code files (T2-REFS) |

- **What differs.**
  - youtube/ is already a migration candidate because directive D1 dropped FluoroCap from training (MP L435); it is a duplicate only if $RS/data/external/fluoro_video holds the same videos (U12).
- **Canonical:** `$RS/data/fluorocap/raw/FluoroCap/raw_hires and the frozen releases`. Original bytes over re-encoded: raw_hires replaces 2,059 PMC copies, median gain 6.25x (AUDIT L759, L768); the frozen releases are authoritative (MP L209).
- **Quality order / why.** Two resolutions of one figure set.
- **Action.** KEEP raw/ and raw_hires/ (which panels were cut from which is U30). youtube/ is not counted here. Subset banks: A16.


### B12. COBRA frames counted up to four times (Ceph-native; already links or re-windowed)

| role | current path | Ceph target | GB | size basis | still read by |
|---|---|---|---:|---|---|
| keep | `(Ceph-native)` | `$RS/data/realxray/cobra_elekta, _v2, _ap45, _v2_ap45` | not sized | - | tools/realxray_train.py |

- **What differs.**
  - '2,445 of the 5,013 duplicate train images are byte-identical (the ap45 banks are symlink views ...), and the rest are those same exposures re-windowed into new PNGs'; the four splits.json are byte-identical (AUDIT L1172-L1182). films_drr_buucorr/img is already a symlink to films_drr/img (ssn:tools/correct_buu_schema.py L95-L97).
- **Canonical:** `$RS/data/realxray/cobra_elekta*`. -
- **Quality order / why.** Recorded so nobody hashes it again.
- **Action.** Nothing to free: the defect is in tools/realxray_train.py ready() (AUDIT L120-L123) and in the index's counting (C09).


## 4. Kind (c): the same people in different releases

Never deleted. Each is recorded as one subject so no split can put a person on both sides. The rows are in `index_aliases.csv`; what the index builder should mark, and where today's schema cannot say it, is in `INDEX_ALIASES.md`. Concrete rows checked here: all 782 CTSpine1K COLONOG rows of `alias_rows.csv` agree with the deposit manifest's token-to-volume map, and no VerSe patient id is also a series id.

| id | group | subjects | concrete alias rows | index action | leak on record |
|---|---|---|---:|---|---|
| C01 | VerSe: 374 series of 355 subjects; series held twice in raw/; canonical/ counted | 18 subjects own 37 series (19 phantom subject keys today) | 37 | subject alias verse:<series> -> verse:<patient_id> (37 rows); item level: the VerSe'19 copy of a series also held as VerSe'20 counted = 0 with lineage to the VerSe'20 item (95 series; duplicate_of when A01 linked it); canonical/ items counted = 0 (converted_from raw); render banks: pass the VerSe map to key_any (BI L794); match VERSE_SUB case-insensitively and lowercase the key (BI L713), or the raw GL### items stay unkeyed. | 5 patients on both sides of allspine_v8 (verse401, 406, 407, 408, 416; PIS section 3 row 7). |
| C02 | CT COLONOGRAPHY people: TCIA, CTSpinoPelvic1K, CTSpine1K, the April release | 802 CTSP persons; 782 CTSpine1K COLONOG volumes are CTSP persons; 2 are not; 1,153 April records are the same 802 | 1,586 | subject alias tcia_ctc:<PatientID> -> ctsp:<vid> (802 rows, spelled as BI L650 keys the TCIA DICOM: 782 PatientIDs recorded in alias_rows.csv, 20 spelled by rule and marked so) plus one rule row (token = the CTC- id as is, else int() of the last OID component: ssn:tools/other_ct_dedupe.py L68-L69), and ctspine1k:COLONOG/<PatientID> -> ctsp:<vid> (782); the two non-CTSP volumes keep their own key tcia_ctc:<PatientID>; the April records need a keyed adapter and their manifest (not at any cited location). Neither tcia_ctc nor ctspine1k is in patient_keys.PERSON_FORMAT (ssn:tools/patient_keys.py L316-L337), so resolve_key refuses both until entries are added, and BI has no CTSpine1K adapter that emits ctspine1k: keys. Never write a token as ctsp:<token>: canon_key zero-pads token 100 to ctsp:0100, release 0100, another person (ssn:tools/patient_keys.py L250-L255; BI L111-L112). No item-level duplicate_of between a CTSpine1K volume and a CTSP CT until a series match is shown. | 357 CTSP people sat on both sides of the v6/v7 split through cross-naming (DM section 4 row 15). |
| C03 | TotalSegmentator v2.0.1 inside v3.0.0: 24 renumbered, 15 merged, 3 repeats inside v3 | 1,935 distinct scans over 3,167 folders (PIS L120); persons unknowable (no patient id: PIS L185-L192) | 0 | release-qualified raw keys (ts201:, ts300:) mapped to the canonical subject ts:<v300 id>; all 29 rows here are pending_table until a release-qualified TotalSegmentator scheme exists (a patient_keys scheme, PERSON_FORMAT entries, a bank registry for the release, and BI emitting ts201:/ts300: instead of ts: at L698): 24 renumbered rows, 3 in-release rows, s2094 -> s2093 as same_scan_declared (as make_split and split_final.json already merge them), and s0927 -> s0254 with its release unrecorded; the other 1,204 v2 ids map from ct_fingerprints.json (or from A05's hash results). Item level: a v2 CT with a v3 twin counted = 0 with lineage to it (duplicate_of when A05 linked it). | Both halves of all 24 pairs are live across ts_drr/anchor_drr/physics_drr (v2) and ts_drr_v3/anchor_drr_c2 (v3) (PIS section 3 row 6). |
| C04 | NHANES II under three names | 364 annotated people (179 with both a C and an L film); 362 of them also in nhanes_pseudo (PIS L122, L149) | 0 | three rule rows to nhanes:<5 digits>; item level: the 542 pickle images that are the same picture as a CDC TIFF counted = 0 with lineage (L00452 has no TIFF and stays counted). | 48 of 54 validation patients (banks v2, v6, v7). |
| C05 | DeepFluoro specimens across the H5, the 8x H5, the vendor deposit, the HF re-host | 6 cadavers | 6 | 6 rows deepfluoro_8x:<NN> -> deepfluoro:<accession>; the HF subjectNN map waits for report/hf_vs_h5.json (U11); never key on the vendor PatientID. | - |
| C06 | BUU-LSPINE byte pairs and the 2000/3600 releases | 3,600 by the released table; at most 3,598 if the two byte pairs are one person each (PIS L123) | 2 | 2 rows buu:0719 -> buu:0140, buu:0629 -> buu:0449 (bytes proven, person not); A12's links give the 2000 JPEGs duplicate_of their buu_full items. | - |
| C07 | VinDr-SpineXR images and studies | 10,466 images over 5,000 studies; the study is the finest unit (PIS L125, L206-L212) | 0 | 10,466 rows image -> study from annotations/{train,test}.csv (on the grid, restricted under the DUA); unit = study. | 77.8 % of vindrps validation cases have a same-study sibling in training (DM section 4 row 30). |
| C08 | Mendeley 5jdfdgp762: a redistribution of BUU and VinDr | about 500 BUU persons and 12 VinDr studies; 71 refused (PIS L126) | 0 | rows from the anns' duplicate_of (on the grid) to buu:<NNNN> and vindr:<study>. | - |
| C09 | COBRA cases seen by several frame banks | 145 cases in the four cobra_elekta* banks (PIS L163) | 0 | no alias; item level: exported frames, ct_def and cbct_rtk counted = 0 with lineage to projections.mha / ct_original.mha. | one detector arm saw the same 145 patients up to four times (AUDIT L18). |
| C10 | Renders keyed to their source CT (implant, PolyPose, CTSP_VERSE_, CTSP cross-naming, devcorpus, C-arm case views) | 799 CTSP implant people, 312 VerSe series under CTSP_VERSE_, 17 devcorpus subjects, 148-149 C-arm sessions (PIS section 3 rows 3, 4, 8, 16, 17) | 0 | rule rows; implant renders resolve to ctsp:, ts: or verse: by their source scheme, as key_any does (make_implant_ct hardware records, else the one declared build whose case format fits: ssn:tools/patient_keys.py L393-L394, L426-L450), since implant_verse (373 VerSe series) and implant_ts exist beside the CTSP implants; the adapter must pass the Dataset813 crosswalk, the VerSe map and the implant map to key_any. | 301 of 801 CTSP people on both sides of anchor_drr's own split (PIS section 3 row 4). |
| C11 | Family B: exact pixel folds and near-duplicates across collections | 127 exact folds (TIERS L16-L20); 1,186 near-duplicate candidates unreviewed (TIERS L217-L219) | 0 | rows from TIERS tier1/tier2 same_ct_as; a candidate table for the 1,186 with status unreviewed; unit = volume for AbdomenAtlas BDMAP ids and the AMOS unlabelled set. | - |

- **C01.** VerSe'19 160 series / 141 subjects, VerSe'20 319 / 300, overlap 105 series (86 subjects), union 374 scans of 355 patients (AUDIT L656-L658); manifest.csv maps series_id -> patient_id, 374 -> 355 (VFG manifest/manifest.csv; ssn:tools/patient_keys.py L115-L133); the 18 subjects (PIS section 3 row 7). The index keys verse:<series> (BI L754) and counts canonical/ items (BI L756) and both raw copies. BI's VERSE_SUB (L713) is case-sensitive, so the raw VerSe'20 GL### items (raw/verse20/01_training/GL003/GL003.nii.gz: VFG unified metas) get no subject key.
- **C02.** One release id = one person, 802/802 by two routes (PIS L119); the manifest token is the TCIA PatientID tail, not the release id (release 0145 = token 100; mem:identity-audit-findings); 782 CTSpine1K COLONOG volumes match a CTSP token and 1.3.6.1.4.1.9328.50.4.0085 and .0680 do not (OCT crosswalk_report.json); checked here: all 782 alias_rows.csv rows agree with the deposit manifest's token -> volume_id map. A person link, not an acquisition link: CTSpine1K's retained series may be the other position (ssn:tools/other_ct_dedupe.py L7-L8; mem:ctspine1k-selection-code-deleted). The TCIA raw DICOM and tcia_nifti are gone from HOME and Ceph (CEN-J; CEN-C; U1).
- **C03.** v2 s1406-s1429 = 24 other v3 ids, vacated numbers reissued (PIS section 3 row 6); s1445=s1446, s2107=s2109=s2110 (PIS L162); s2093/s2094 near, not equal (PIS L162) but merged by make_split's DECLARED_ALIASES (ssn:tools/make_split.py L91-L93) and in the frozen split (SchwingNet/results/fig6/frozen/v1/split_final.json group_of: ts:s2094 -> ts:s2093); s0254/s0927 'one scan whose bytes differ' (PIS L98; ssn:tools/make_split.py L92), while ssn:tools/ts_transitional_registry.py L901-L903 says 'v201 s0254 and s0927 differ from v300 s0254 / s0927 only in the gzip stream', so which release each id of the pair belongs to is not recorded. The index keys ts:<s####> for both releases (BI L698): 24 people split, 15 merged. No keyer produces ts201: or ts300:: key_for and key_any return release-blind ts:s#### (SCHEMES ts_plain, ts_render: ssn:tools/patient_keys.py L55-L56, L70), and PERSON_FORMAT has no ts201/ts300 corpus (L316-L337), so resolve_key refuses such keys.
- **C04.** Spellings nhanes_00160, NH_00160_c/_l, NHANESPS_C00160 (PIS L149); 48 of 54 validation patients had their other copy in training (ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md). Both raw adapters key nhanes:<5 digits> (BI L500, L509-L510); no NHANESPS rule was found in ssn:tools/patient_keys.py (U29).
- **C05.** 8x H5 names the six 01-06: 01=17-1882, 02=18-1109, 03=18-0725, 04=18-2799, 05=18-2800, 06=17-1905 (PIS L131); the fluoroscopy PatientID merges 18-2799 with 18-2800 and splits others (PIS section 3 row 15).
- **C06.** 0140/0719 share byte-identical AP and LA JPEGs, 0449/0629 an AP JPEG (PIS L123); make_split declares them (ssn:tools/make_split.py L93). Whether buu_2000 names carry the buu_full case numbers is not checked (T3 unknown 17).
- **C07.** The render banks carry vindr_<image_id> and the index turns it into vindr:<image_id>, a key that looks like a study key (PIS L78; ssn:tools/patient_keys.py L159-L166, L334).
- **C08.** 16 Test images byte-identical to BUU originals, 500 more at r = 1.0000 (PIS section 3 row 10); duplicate_of on 500 of 584 anns (PIS section 2 mendeley row).
- **C09.** Subject keys are right (cobra:<case>, BI L555, L590); every exported frame is counted (BI L564-L571) and ct_def.mha / cbct_rtk.mha are counted as acquisitions (BI L595-L601).
- **C10.** make_split already folds 8,859 implant and PolyPose renders to their source (ssn:SchwingNet/results/rare_class/split_plan.md L205); the index's render-bank adapter passes no crosswalk, VerSe, implant or VinDr map to key_any (BI L794).
- **C11.** Cross-collection exact duplicates are both counted, each with pixel_sha1 in extra (BI L872); alias_pairs*.csv are not in the repository (DM L3705-L3706).

## 5. The jobs

```
cd ~/spinesurg-ct-nnunet/data_platform/dedup && mkdir -p logs
sbatch -D "$PWD" dedup_hash.sbatch                                   # every kind-(a) group
sbatch -D "$PWD" --export=ALL,GROUP_IDS="A05 A17" dedup_hash.sbatch
sbatch -D "$PWD" --export=ALL,GROUP_IDS=A17,DRY=1 dedup_apply.sbatch     # what it would do
sbatch -D "$PWD" --export=ALL,GROUP_IDS=A17 dedup_apply.sbatch
sbatch -D "$PWD" --export=ALL,GROUP_IDS=A17,ROLLBACK=1 dedup_apply.sbatch
```

- `dedup_plan.tsv` is the input of both jobs (generated with this file; never edit it by hand: rerun `python build_dedup_plan.py`). Columns: group_id, kind, mode (relpath | rename | pairs | content), dup_root, dup_include, canon_roots (`|` = priority order), canon_include, exclude, key_regex (content mode: a shared token, or BASENAME), rename_map, pairs, allow_unpaired, hold, est_gb.

- Include and exclude patterns are matched with bash `[[ == ]]`, which reads them as if extglob were on: a literal parenthesis must be written as a bracket expression (`*[(]1[)]*`; `*(1)*` would match every name).

- Every path test is made on the path as spelled and as resolved (`readlink -f`): a file is touched only when it lies under its member root with no symlink component below the root, and resolves under `$RS`, off HOME and outside any `.pre-ceph` copy. A directory symlink inside a member tree (`films_drr_buucorr/img` -> `films_drr/img`, B12; the HOME-spelled links in unified/, A01) is therefore never followed.

- **`dedup_hash.sbatch`** (reqp, requeue, `-D`, no `/tmp`: TMPDIR, which bash older than 5.1 uses for here-strings, is `/dev/shm/dedup.<job>` or `logs/tmp.<job>` and is removed at exit; bash, find, sha256sum and coreutils). A group is hashed only when every member root is under `$RS`, not on HOME as spelled or resolved, not a `.pre-ceph` copy, and its batch item (if any) is VERIFIED and cut over with no migrate or cut-over job writing the batch; a batch re-run after its cut-over (`ALREADY_SYMLINK`, field 4 `-> <dst>`: plan/migrate_batch.sbatch L131) counts as verified when an earlier run verified the same dst. Sizes first; groups under 50 GB of paired bytes are hashed in full, larger ones by a sample stratified by first folder plus every pair whose sizes differ (coverage = sample). Content groups hash every same-size candidate, because the hash is the pairing; their key tokens are compared in lowercase. Output `hash_results/<gid>.json` and `.tsv`: one record per file (identical, different, size_differs, missing_canonical, missing_duplicate, unpaired, key_mismatch, already_link, same_inode, unhashed_size_equal, via_link) and a verdict (identical, different, missing, review, none, not_ready).

- **`dedup_apply.sbatch`** acts on one named group at a time and refuses the whole group when the verdict is not identical, the plan rows changed since the hash, `squeue` cannot be read, a member is on HOME, is a `.pre-ceph` copy or is Ceph-native on the duplicate side, a covering batch is not VERIFIED, cut over and FINALIZED, a migrate or cut-over job is writing it, any running or pending job names a member, its batch dst or its HOME src (absolute, `~/`, `$HOME/`, or relative to the job's WorkDir) or works inside it, an interrupted earlier apply left `.dedup_old`, `.dedup_hold` or `.dedup_tmp` names, or a ledger copy cannot be written. No link chains: a file that is the canonical of a pair in any `hash_results/*.tsv` or any ledger is never replaced, and a canonical that is itself a symlink is refused. A duplicate with other hard links is refused (a symlink frees nothing). File mode verifies and swaps one file at a time: the canonical is made read-only (every canonical, batch copy or Ceph-native; its mode goes to the ledger first); a hard link `<dup>.dedup_hold.<job>` keeps the duplicate's inode; both sides are stat'ed to the nanosecond, hashed, linked under a temporary name and stat'ed again; the ledger row is written to `applied/` and to `$RS/dedup_ledgers/`, and a failed write stops the group before the swap; `mv -fT` swaps the link in; the link must resolve to the canonical's recorded inode and the hold must still carry the duplicate's recorded inode, size and mtime, or the hold goes back over the link. A relpath tree that matched completely becomes one symlink: it is recorded entry by entry before the hashing, moved aside, linked, walked again and compared, and put back on any difference. Jobs and gates are scanned again before every tree swap and every 60 s in file mode; a TERM (`--signal=B:TERM@120`, preemption) finishes the swap in flight and stops. A stale lock is taken over only when squeue says the holder's id is invalid or sacct says it ended. What no check closes: a process that holds a duplicate open and writes to it after its swap writes into an unlinked inode; the job gates are the only defence. DRY and refused runs write `applied/<gid>.dry.<job>.json` and `<gid>.refused.<job>.json`, so `applied/<gid>.json` stays the last real apply.

- **`ROLLBACK=1`** reads the ledger (the primary or the Ceph copy; refused when they disagree beyond one being a prefix of the other), resolves the hold and temporary names a killed job left, puts a moved-aside tree back whole, replaces a tree link by a folder (refusing a tree root that now links elsewhere, and any file whose parent folder is a symlink), copies each canonical back over its link with the recorded sha256, mode and nanosecond mtime, then folder modes and mtimes deepest first, and returns a canonical its first recorded mode only when no ledger of any group still has a live link to it. Owner, group, ACLs and xattrs are those of a new file in the same folder, which is what the batch copy itself got (`rsync -aH --no-g` into setgid folders, no -A or -X: plan/migrate_batch.sbatch L51).

- **`dedup_guard.sh <path>...`** (read-only; in a job, or at the top of a deletion job) exits 1 and lists the links when any ledger records a live link whose canonical lies in the paths, spelled or resolved; 0 when none does. Every deletion candidate in this plan, and in MIGRATION_PLAN section 8, should pass it first.

- After a migration rollback (MP L511 uses `rsync -aH`, which copies a symlink as a symlink), run `ROLLBACK=1` here first, or HOME receives links into Ceph.

- **Tests**: `DEDUP_TEST_ROOT=<folder> bash test_dedup.sh` builds, in a fresh folder under DEDUP_TEST_ROOT (default `.test_tmp` beside the script; never `/tmp`), a fake Ceph root, HOME root, batch items, STATUS and CUTOVER logs and stub `squeue`/`scontrol`/`sacct`, and checks 106 cases: identical trees symlinked and rolled back byte for byte; a one-byte difference refused; a HOME path refused, spelled and through a Ceph-spelled link; a file changed after the hash refused while the rest link; an unfinalized batch refused; sampled coverage; content pairing across names and a byte twin under another series token sent to review; explicit pairs with a read-only canonical that blocks a write through the link; a running job naming the path; a `.pre-ceph` member; a held group; a kind-(b) group; a literal-parenthesis rename pattern; and the review's cases X1-X8 (a duplicate or a canonical reached through a directory symlink onto HOME, a duplicate written during its swap, a file written into a tree during its swap, a Ceph-native canonical rewritten in place with and without restoring its write bit, a batch re-run after cut-over, an unwritable ledger, a hard-linked duplicate) plus X9-X18 (mtime restored, a tree root that links elsewhere, a canonical shared by two groups and `dedup_guard.sh`, no link chain across groups, GL003 against gl003, a job naming the member relative to its WorkDir, DRY summaries, stale locks, artefacts of a killed apply, TERM). Run 2026-10-08 in WSL (bash 5.2.21, tree on the laptop's NTFS through drvfs, which keeps no sub-second mtime, so X9 checks equality, not nanoseconds): 106 passed, 0 failed.

## 6. What the hash settles, and what it does not

| unknown | settled by |
|---|---|
| Whether B06, B07, B02, B04, B05, B09, B10, B11, B14 are finalized (U2/U7) | the gates of both jobs read `runs/<B>/STATUS` and the CUTOVER logs |
| Which of the 95 VerSe'19/'20 series pairs match, per kind (U6) | A01 |
| Whether canonical/ holds byte copies of raw/ (U1, bytes) | A02 |
| Whether canonical/ is voxel-equal to raw/ and CT scaling survived (U2) | not by a hash: a NIfTI job (B01 step 1) |
| What the 56 GB census gap in VerSeFusion/data is (U4) | A03 (same_inode vs identical) |
| The bytes the TS v2/v3 links free; the 110 v2 CTs without a twin (U5/U15) | A05 bytes_identical and unpaired count |
| Whether any April CT equals a v11 CT (U4 of topic 1) | A10 |
| Whether ~/s1v11, ~/pitest, ~/pdwtest are copies or hard links, and of which version (U10/U22) | A07; A08 against the v11 labels only (labels_v10, a later deletion candidate, is no longer a canonical root, so whether they are v10 copies is not settled by a hash here) |
| Whether the rung files of films_all2/films_ann are byte-identical (U17) | A17, A18 |
| Whether allspine_v8 equals v9 (U16) | A22 |
| Whether the FluoroCap pack is a copy or links (U9) | A16 |
| Whether the yolo* exports are copies or links (U18) | not hashed: A21 dropped |
| Whether the eight C-ArmLSpine fold banks repeat carm_drr's frames | not hashed: A20 dropped |
| Which side of the 98 AASCE challenge-test files is original (U20) | not by a hash: the challenge's own listing (network) |
| Whether ctsp_drr_obl* images equal verse_drr_obl* images (U8) | not planned: B02 retires them either way |
| Where the TCIA COLONOGRAPHY raw DICOM went (U1/U25) | not by a hash: the job log of whatever removed it |

## 7. The review of 2026-10-08: what changed, and where it was not followed

A review of the first version raised 26 findings (2 blockers, 7 major, 17 minor), with adversarial cases X1-X8 run against the scripts in the session scratchpad. Every finding was checked against the file it cites before it was applied. All blockers and majors are applied, and every minor that states a fact; the cases are now in `test_dedup.sh`, and the reviewer's own script, rerun on the revised jobs, shows every case held (the HOME files untouched, the late bytes and the late file kept, the canonical intact, nothing linked without a ledger, the hard link kept).

| # | finding | disposition |
|---:|---|---|
| 1 | blocker: tree mode could delete files written after the listing | Applied. The tree is recorded entry by entry (type, path, size, mtime, ctime, inode, nlink) before the hashing, walked again after the move-aside, and put back on any difference; jobs and gates are scanned again before each tree swap. Test X4. |
| 2 | blocker: HOME and .pre-ceph refusals only on member roots; directory symlinks below a root unseen | Applied. Every file and its canonical must lie under their roots with no symlink component below the root (`clean_below`) and resolve under `$RS`, off HOME and outside .pre-ceph (`safe_resolved`); the hash job reports such pairs as via_link and never pairs them; the gate checks the resolved root. Tests X1, X2. |
| 3 | major: file mode verified every file first and swapped hours later | Applied. One file at a time: canonical protected, a hard-link hold on the duplicate, nanosecond stat, hash, temporary link, stat again, ledger, swap, then inode checks on both sides, the hold put back on any difference. Every canonical is now made read-only, Ceph-native ones included. Gates rescanned every 60 s. Tests X3, X5a, X5b. |
| 4 | major: ledger writes unchecked | Applied. Each row is written to `applied/` and to `$RS/dedup_ledgers/`; a failed write stops the group before any swap; rollback reads either copy. Test X7. |
| 5 | major: canonical roots that are deletion candidates (A03 canonical/, A08 labels_v10) | Applied, with one deviation. A03 and A08 no longer use them; `build_dedup_plan.py` refuses to write a plan whose canonical root is, or holds as a possible canonical file, any of 77 candidates (kind (b) and MIGRATION_PLAN section 8); `dedup_guard.sh` refuses a deletion while any live link points into the path; `CANONICAL_ROOTS.tsv` lists the roots in both ledger places. Deviation: no marker file is written inside a canonical root. Canonical roots include release folders, such as CTSpinoPelvic1K/labels, checked file by file against Zenodo's SHA256SUMS (AUDIT L620), and raw/verse20, which VerSeFusion's unify walks; and README.yaml is placed from the templates in plan/readme_yaml (LAY L103), so a field a job appended would be lost at the next placement. The ledgers on Ceph plus the guard carry the same information without writing into the data. Making MIGRATION_PLAN section 8 call the guard is a request to that plan. |
| 6 | minor: ALREADY_SYMLINK rows never matched (field 4 is `-> <dst>`) | Applied: the prefix is stripped, so the fallback to an earlier VERIFIED run works. Test X6. |
| 7 | minor: rollback fidelity | Applied: mtime recorded as `stat %y` (nanoseconds) and restored with `touch -d`; duplicates with nlink > 1 are refused at apply, so no hard link is ever broken; folder modes and mtimes are set after their contents, deepest first; a canonical's mode comes back only when no ledger of any group still has a live link to it. `chmod -h` does not exist in GNU chmod (`chmod: invalid option -- 'h'`, coreutils 9.4), so the fix is a `-L` test before chmod. Owner, group, ACLs and xattrs are not recorded: a copy made in the same folder gets what the batch copy got (rsync -aH --no-g into setgid folders, no -A or -X: plan/migrate_batch.sbatch L51). Tests X8, X9, X11. |
| 8 | minor: rollback could report success with the tree still linked | Applied: a tree root linking elsewhere is refused, and a file whose parent folder is a symlink is left alone. Test X10. |
| 9 | minor: stale-lock takeover on a transient squeue failure; no TERM trap; ln without -T | Applied: takeover only when squeue says the id is invalid or sacct reports a final state (and only one job wins, by mkdir); `--signal=B:TERM@120` with a trap that finishes the swap in flight; `ln -sT`; a SIGKILL's leftovers refuse the group until ROLLBACK resolves them. Tests X16, X17, X18. |
| 10 | minor: IS_CANON from one group only; DRY overwrote the real summary | Applied: built from every hash_results/*.tsv and every ledger; DRY and refused runs write their own files. Tests X12, X15. |
| 11 | minor: here-strings and /tmp; tests missing X1-X7 | Applied: TMPDIR is /dev/shm/dedup.<job> (or logs/tmp.<job>) in both jobs and removed at exit; X1-X8 and ten more cases are in test_dedup.sh. |
| 12 | major: A20 links to carm_drr, which a launch script deletes and rebuilds | Applied: A20 dropped (no plan rows); carm_drr recorded as due for rebuild. One precision: slurm/carmlspine_finetune.sh L22-L23 rebuilds it only when ~/carm_fov96_ctx/rung_1.npz is absent; the conclusion stands, since that bank predates the repair too (DM section 4 row 20). |
| 13 | major: A21's canonical is rewritten in place by sd:src/build_dataset.py | Applied: A21 dropped; names_member also matches paths relative to a job's WorkDir and a WorkDir inside a member. Test X14. |
| 14 | major: B08's Ceph target took the whole nhanes_annotated folder, zip included | Applied: the candidate is nhanes_annotated/extracted; the zip has its own KEEP row. Narrowing plan/batch_items/B04.tsv L2 and layout_map.csv is a request to the migration plan, not made here. |
| 15 | major: C03 aliases used corpora (ts201:, ts300:) no keyer produces | Applied, except one row. All 29 rows are pending_table until a release-qualified scheme exists; s2094 -> s2093 is same_scan_declared, as make_split and split_final.json already merge them; the 24 renumber pairs were checked here against split_final.json (24 of 24 in one group). Not applied: release-qualifying the s0927 row, because the release of each id is not recorded and the files read the pair two ways (PIS L98 and tools/make_split.py L92: one scan, s0254 = s0927; tools/ts_transitional_registry.py L901-L903: 'v201 s0254 and s0927 differ from v300 s0254 / s0927 only in the gzip stream', joined by geometry). The row is spelled `ts<release not recorded>:s0927` and waits for ct_fingerprints.json. |
| 16 | minor: build_archive_private offered as a candidate | Applied: KEEP, owner-only; off the candidate line (it was 0 GB, so the 9.27 GB total is unchanged); the stated reason corrected. |
| 17 | minor: canonical/ candidate lacked a condition for A03's links | Applied: A03 no longer links into canonical/, and condition (4) is dedup_guard.sh passing on it. |
| 18 | minor: key regex case-sensitive (GL003 against gl003) | Applied: key tokens compared in lowercase. The index's VERSE_SUB (BI L713) has the same gap; recorded for the indexer in C01. Test X13. |
| 19 | minor: scaling banks called regenerable | Applied: they are cut from allspine_v2_fov96_ctx, deleted 2026-09-20; moved from 'now' to 'conditional' (once the scaling figures are frozen). |
| 20 | minor: VerSe quality order put HF copies above corrected/ for the 14 corrected scans | Applied; verse559 and verse642 are the two applied label_override scans (verse606's override was not applied). NPR also contradicts itself on which corrections were reviewed (L311-L312 against L443-L446). |
| 21 | minor: C02 token rows used a corpus the index does not emit | Applied: spelled tcia_ctc:<PatientID> as BI L650 does (782 PatientIDs on record, 20 spelled by rule and marked so), plus a rule row converting any spelling to the token; tcia_ctc and ctspine1k are not in PERSON_FORMAT, which the indexer must add. |
| 22 | minor: C10 implant rule mapped only to ctsp | Applied: three rule rows (ctsp, ts, verse), as key_any resolves them. |
| 23 | minor: 'both adapters skip symlinks' | Applied: the TotalSegmentator adapter follows links (BI L694) and item() stats through them (BI L210-L226); the ledger rule now updates existing items. |
| 24 | minor: vendor zips without a completeness check | Applied: an unzip -l comparison with unpacked/ comes first; the zips alone are the candidate; the rotations table has a KEEP row. |
| 25 | minor: read-only canonicals turn rebuilds into crashes; writers of the twins unfixed | Applied: A17 and A18 say ROLLBACK=1 before any rebuild (A20 is dropped); the writers (reproduce_all.sh L108, path_render.sh L40-L41, verse_path_missing.sh L19, make_drr_dataset.py L31) are listed with A04 and referenced from B01 and B02. They are not edited here. |
| 26 | minor: test tree under /tmp | Applied: DEDUP_TEST_ROOT, default .test_tmp beside the script; this run used the session scratchpad. |

Left for other files (named here, not edited): MIGRATION_PLAN section 8 should require `dedup_guard.sh` before any deletion; plan/batch_items/B04.tsv and plan/layout_map.csv should flag nhanes_annotated/extracted, not the folder; the writers listed under A04; in db/build_index.py, VERSE_SUB case-insensitive (L713), release-qualified TotalSegmentator keys (L698), and the ledger rule of INDEX_ALIASES.md; in tools/patient_keys.py, PERSON_FORMAT entries for tcia_ctc, ctspine1k, ts201 and ts300.
