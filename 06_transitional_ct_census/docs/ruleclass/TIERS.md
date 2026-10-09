# TIERS: the shared CT lists for the SUPER DETECTOR RUN (arm A TotalSegmentator, arm B SPINEPS + VERIDAH + Möller ribs + Dataset803 pelvis)

Built 2026-09-27 00:20-00:40 EDT. Grid work was file listing only: `find`/`ls` on the login node, then a stat-only existence
test of every path written. No image was opened and no job was submitted. The join ran on this machine
(`tiers/build_tiers.py`) over those listings, the pulled screen metadata (`corpus_pull.tgz`), the transitional registry
(`SchwingNet/results/transitional_registry/registry.csv`) and `classifiers_by_person.csv`.

## 0. Short answer

| list (grid, `RS = /rs/rs_grp_oschome/go2432`) | CTs | persons | what it is |
|---|---:|---:|---|
| `RS/ruleclass/tiers/tier1.txt` + `tier1.tsv` | **5,094** | 5,075 | CTSpinoPelvic1K 802, TS-benchmark natives 1,602 (TotalSegmentator 1,228 + VerSe 374), COBRA planning CTs 692, and every other CT whose person carries a registry or screen flag (1,997) or another classifier's positive (1) |
| `RS/ruleclass/tiers/tier2.txt` + `tier2.tsv` | **12,217** | 12,217 | every other CT with a SPINEPS harvest mask on disk at 00:20 |
| `RS/ruleclass/tiers/untiered.tsv` | 4,311 | | CTs with neither a tier-1 reason nor a SPINEPS mask. Most are gate-refused acquisition CTs, 1,114 are PANORAMA CTs still pending, and 210 are TotalSegmentator scans where SPINEPS failed |

- **One row per CT.** A CT that is reachable from two collections appears once, and the other names go in `same_ct_as`.
  127 names were folded this way: 70 validation_ts and 24 val_ts12/val_tsgt entries onto their TotalSegmentator scans,
  32 PENGWIN onto CTPelvic1K clinic, and 1 PANORAMA onto Kidney, all on exact pixel sha1. The 4 duplicate v300 folders
  were also folded, and so were the 782 CTSpine1K COLONOG volumes that are CTSP people. Near-duplicates (thumbnail NCC
  >= 0.98) are only listed in `alias_candidates` (1,186 CTs) and were not merged.
- **Every flagged person joined.** All 2,332 flagged person keys matched a CT row. Every CT of a tier-1 person is in
  tier 1: VerSe multi-series subjects contribute all of their series.
- **All paths exist.** `code/check_paths.sh` stat-tested every CT, SPINEPS, TS and GT path in both tables: 0 missing.
- **Disk.** `df-ceph oschome` at 00:40 reads a 20 TB quota with 26.86 % used, which leaves about 14.6 TB free.
  Section 6 estimates all new outputs at about 40 GB.

## 1. Per-collection counts

"tier 1 why" gives the number of tier-1 CTs per reason, in this order: CTSP release / TS-benchmark native / COBRA set /
registry or screen flag / other classifier positive. A CT can carry several reasons. "raw ids" counts masks whose
instance ids are SPINEPS's own 1..N (section 3).

| collection | CTs listed | persons | **tier 1 CTs** | tier 1 persons | tier 1 why | tier 1 with SPINEPS (raw ids) | tier 1 with TS | **tier 2 CTs** | tier 2 raw ids | untiered | same CT folded in | alias candidates |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| ctsp | 802 | 802 | **802** | 802 | 802 / 0 / 0 / 64 / 48 | 801 (0) | 802 | **0** | 0 | 0 | 0 | 0 |
| verse | 374 | 355 | **374** | 355 | 0 / 374 / 0 / 171 / 22 | 374 (13) | 374 | **0** | 0 | 0 | 0 | 0 |
| ts (TotalSegmentator dataset, v300 keys) | 1,935 | 1,935 | **1,278** | 1,278 | 0 / 1228 / 0 / 134 / 6 | 1,213 (95) | 1,278 | **447** | 422 | 210 | 94 | 0 |
| cobra | 692 | 692 | **692** | 692 | 0 / 0 / 692 / 20 / 77 | 681 (0) | 692 | **0** | 0 | 0 | 0 | 0 |
| abdomenatlas3_mini | 7,649 | 7,649 | **1,069** | 1,069 | 0 / 0 / 0 / 1069 / 0 | 1,056 (0) | 1,069 | **4,715** | 0 | 1,865 | 0 | 687 |
| idc | 3,499 | 3,499 | **386** | 386 | 0 / 0 / 0 / 386 / 0 | 373 (0) | 386 | **2,577** | 0 | 536 | 0 | 185 |
| panorama | 2,024 | 2,024 | **0** | 0 | 0 / 0 / 0 / 0 / 0 | 0 (0) | 0 | **910** | 0 | 1,114 | 0 | 80 |
| tcia_fdg_pet_ct_lesions | 900 | 900 | **165** | 165 | 0 / 0 / 0 / 165 / 0 | 158 (0) | 165 | **695** | 0 | 40 | 0 | 0 |
| amos22 | 723 | 723 | **90** | 90 | 0 / 0 / 0 / 90 / 0 | 89 (0) | 90 | **630** | 0 | 3 | 0 | 48 |
| nlst_pilot | 500 | 500 | **5** | 5 | 0 / 0 / 0 / 5 / 0 | 5 (0) | 5 | **484** | 0 | 11 | 0 | 2 |
| kidney_thoraxabdomen | 215 | 215 | **39** | 39 | 0 / 0 / 0 / 39 / 0 | 38 (0) | 39 | **176** | 0 | 0 | 1 | 1 |
| waw_tace | 228 | 228 | **48** | 48 | 0 / 0 / 0 / 48 / 0 | 48 (0) | 48 | **164** | 0 | 16 | 0 | 24 |
| barts_crl | 212 | 212 | **46** | 46 | 0 / 0 / 0 / 46 / 0 | 46 (0) | 46 | **162** | 0 | 4 | 0 | 2 |
| curvas | 70 | 70 | **5** | 5 | 0 / 0 / 0 / 5 / 0 | 5 (0) | 5 | **47** | 0 | 18 | 0 | 13 |
| curvas_pdacvi | 101 | 101 | **12** | 12 | 0 / 0 / 0 / 12 / 0 | 12 (0) | 12 | **82** | 0 | 7 | 0 | 78 |
| aortaseg60 | 55 | 55 | **5** | 5 | 0 / 0 / 0 / 5 / 0 | 5 (0) | 5 | **50** | 0 | 0 | 0 | 6 |
| quadra_hc | 48 | 48 | **9** | 9 | 0 / 0 / 0 / 9 / 0 | 9 (0) | 9 | **38** | 0 | 1 | 0 | 0 |
| deep_psma | 53 | 53 | **6** | 6 | 0 / 0 / 0 / 6 / 0 | 5 (0) | 6 | **37** | 0 | 10 | 0 | 0 |
| csi2014 | 20 | 20 | **2** | 2 | 0 / 0 / 0 / 2 / 0 | 2 (0) | 2 | **18** | 0 | 0 | 0 | 0 |
| pengwin2026 | 308 | 308 | **1** | 1 | 0 / 0 / 0 / 1 / 0 | 1 (0) | 1 | **10** | 0 | 297 | 0 | 26 |
| ctpelvic1k_clinic | 172 | 172 | **1** | 1 | 0 / 0 / 0 / 1 / 0 | 1 (0) | 1 | **5** | 0 | 166 | 32 | 34 |
| ctspine1k (non-CTSP 223) | 223 | 223 | **20** | 20 | 0 / 0 / 0 / 20 / 0 | 20 (0) | 20 | **196** | 0 | 7 | 0 | 0 |
| ribfrac | 660 | 660 | **35** | 35 | 0 / 0 / 0 / 35 / 0 | 35 (0) | 35 | **620** | 0 | 5 | 0 | 0 |
| carmlspine (CBCT) | 149 | 149 | **4** | 4 | 0 / 0 / 0 / 4 / 0 | 4 (0) | 4 | **145** | 0 | 0 | 0 | 0 |
| deepfluoro | 6 | 6 | **0** | 0 | | | | **6** | 0 | 0 | 0 | 0 |
| geneva | 1 | 1 | **0** | 0 | | | | **1** | 0 | 0 | 0 | 0 |
| spinesac | 3 | 3 | **0** | 0 | | | | **2** | 0 | 1 | 0 | 0 |
| **all** | **21,622** | 21,603 | **5,094** | 5,075 | 802 / 1602 / 692 / 2337 / 153 | 4,981 (108) | 5,094 | **12,217** | 422 | 4,311 | 127 | 1,186 |

What is in tier 1, by flag. These are flag strings on tier-1 CTs, and one CT can carry more than one.

| subtype | from the registry (R13) | from an acquisition screen (R20) |
|---|---:|---:|
| L6 | 148 | 303 |
| T13 | 14 | 82 |
| both L6 and T13 | 0 | 1 |
| sacralised L5 (fused) | 27 | 0 |
| Castellvi I-II | 32 | 0 |
| lumbar rib | 27 | 0 |
| unassigned (four lumbar-type bodies, no read) | 63 | 368 |
| unresolved (the two labellers disagree) | 129 | 0 |
| review (the two labellers disagree) | 0 | 1,168 |

**1,052 tier-1 CTs carry at least one positive-subtype flag. Another 1,285 are flagged only as review or unresolved, meaning
the existing labellers disagree.** Those 1,285 were kept on purpose, because the run exists to adjudicate
disagreements. If a faster positives-only pass is wanted, filter `registry_flags` to drop the `review|` and `unresolved|`
entries. That leaves 1,052 CTs plus the four fixed sets.

Other facts about the lists:
- **Real frames (TEST only, never render for training):** tier 1 holds 696 of them (COBRA 692, C-ArmLSpine 4). Tier 2
  holds 154 (C-ArmLSpine 145, DeepFluoro 6, SpineSAC 2, Geneva 1). The last 9 are cadavers or phantoms with no rib
  cage, so the count cannot be made on them.
- **Children** (`notes`: TS v300 age < 18, IDC pediatric_ct_seg): 114 in tier 1 and 442 in tier 2. On these an
  unfused S1 reads as a free body, and the sacral shape is not adult shape.
- **Both junctions in field** (`junction_*_in_fov` both True where a screen computed it): 2,951 in tier 1 and 8,050 in
  tier 2. The CTSP negatives, part of VerSe and the TS rows have blank cells, because those streams did not write the
  field per CT.

## 2. Definitions used (so the next agent can change them)

- **Registry-flagged** means the person's subtype is anything other than `none` / `ordinary` / `no_count`, at any truth
  tier (read, two-labeller, single-labeller, morphology-only, none) in either of two sources:
  (a) `registry.csv` (R13; streams ctsp, verse, totalsegmentator, cobra, other_ct; 6,113 rows), or
  (b) the acquisition screens' `rows.csv` (R20; 17 collections plus validation_ts, re-keyed to `ts:<v300 id>`). This
  includes `review` and `unresolved`. PANORAMA has no screen rows yet, so none of its CTs can be flagged.
- **Other classifier positive** is `any_positive` in `classifiers_by_person.csv` for a person the registry does not flag.
  It adds 153 reasons, and only 1 of them is a CT not already in tier 1 through another reason (a TS scan).
- **TS-benchmark natives** are the 1,602 cases in `~/bench_ts/cases.csv`: `TS_s####` (1,228, v201 numbering) and
  `VERSE_<sid>` (374). A TS native is listed under its v300 key and v300 CT. The v201 twin is named in `notes`, and the
  24 renumbered ids (v201 s1406-s1429 correspond to v300 s1463 ... s2139) are mapped. Those 24 are never matched by number.
- **CTSpinoPelvic1K** is all 802 records. The task named 801 because 0665 has no SPINEPS output. It is kept for arm A
  and the pelvis model, and its `notes` say the SPINEPS mask is missing.
- **COBRA LSTV set** is all 692 planning CTs (`cobra2026/lstv/nifti` 591 + `varian/nifti` 101).
- **Tier 2** is every CT not in tier 1 that has a SPINEPS `seg-vert` mask in any store.

## 3. Columns of tier1.tsv / tier2.tsv / untiered.tsv

| column | meaning |
|---|---|
| `tier` | 1, 2 or none |
| `ct_path` | the CT to run on. **Quote it: 47 quadra_hc paths contain a space** (`.../QUADRA_HC/Imaging Data/...`). TS dataset: `Totalsegmentator_dataset_v300/s####/ct.nii.gz`. VerSe: `VerSeFusion/data/unified/scan-<sid>/scan-<sid>_ct.nii.gz` (a symlink to the raw VerSe file). CTSP: `~/data/CTSpinoPelvic1K/ct/<rel>_ct.nii.gz` |
| `collection`, `case_id`, `person_key` | the keys `classifiers_by_person.csv` and `registry.csv` use: `ctsp:<rel, zfill 4>`, `verse:<patient_id>` (manifest.csv), `ts:<v300 id>`, `cobra:<case>`, the acquisition `cases.csv` `patient_key` (IDC keys per sub-collection, e.g. `hcc_tace_seg:HCC_001`), `ctspine1k:<sub>:<id>`, `ribfrac:RibFracN`, `carmlspine:caseN` |
| `tier1_reason` | `ctsp_release`, `bench_ts_native`, `cobra_lstv_set`, `registry_flag`, `other_classifier_positive` (`;`-joined) |
| `registry_flags` | `subtype|truth_tier (registry)` or `subtype|truth_tier (screen <collection>)`, `; `-joined |
| `other_classifier_positive` | `any_positive` from CLASSIFIERS.md's join |
| `junction_tl_in_fov`, `junction_ls_in_fov` | copied from the screen rows or the registry where they exist. Per CORPUS.md this is B's geometry OR A's lumbar count, so it can be True when only one labeller saw the junction |
| `real_frames` | 1 means TEST only |
| `spineps_vert`, `spineps_spine`, `spineps_ctd` | the preferred SPINEPS mask set (section 4) |
| `spineps_ids` | `verse_coded` (post-147428d harvest), `relabelled` (a relabelled copy that is a real file), or `raw` (instance ids 1..N; name through the ctd and guard with `tools/spineps_ids.py`) |
| `spineps_store`, `spineps_relabel_json`, `spineps_alt` | which store the mask came from, the id map, and every other `seg-vert` mask of this CT (`;`) |
| `ts_output`, `ts_kind`, `ts_class_map` | `total_multilabel`: one file plus its class map. `roi_subset_dir (no hips)`: the acquisition per-structure directory (50 files: C1-L5, S1, sacrum, ribs 1-12 per side; **no hips, no femora**). `gt_dataset_masks`: the TotalSegmentator dataset's own `segmentations/` |
| `ts_alt` | acquisition: the `tsbody` directory (vertebrae_body, discs). TS dataset: the validation_ts roi directory and the val_ts12 `total` file where they exist |
| `gt_label` | CTSP v11 label (`labels/`, never `labels_v10/`), VerSe `_msk` (no sacrum, no ribs), CTSpine1K `_seg`, TS dataset `segmentations/` |
| `same_ct_as`, `alias_candidates`, `notes` | folded duplicates, unmerged near-duplicate candidates, and traps specific to the CT |

## 4. Which SPINEPS mask each row points at

Preference order per collection. The first one present wins. `raw` loses to `verse_coded` or `relabelled` wherever one
exists.
- **CTSP:** `RS/data/spineps/ctsp/CTSP_<rel>_*` (post-fix, 801), then `RS/data/spineps/ctd_relabel/bench_native/COLONOG_<token>_*`, then `~/bench/spineps/native/COLONOG_<token>_*` (raw). The TS files are `~/bench/totalsegmentator/native/COLONOG_<token>.nii.gz`. For 0533 (token 378) and 0921 (token 647) they come from `AH/ctsp/ts_retry/native/`.
- **VerSe:** `ctd_relabel/bench_ts_native/VERSE_<sid>_*`, then `~/bench_ts/spineps/native/VERSE_<sid>_*` (raw on 13 series).
- **TS dataset:** `tsv3_ctd/TSV3_<v300>`, then `ctd_relabel/bench_ts_native/TS_<v201>`, then `spineps_patch` / `spineps_crop` `TSV3C_<v300>`, then `validation_ts/spineps/vts_<v201>`, then `tsv3/TSV3_<v300>` (raw), then `bench_ts/spineps/native/TS_<v201>` (raw). The folded duplicate folders' masks go in `spineps_alt`. Raw: 95 in tier 1 and 422 in tier 2.
- **COBRA:** `cobra2026/lstv/seg/<case>_*` (580), then `spineps/cobra_varian/<case>_*` (101). 11 cases have no mask. The older `cobra2026/seg/spineps` (raw) is not used.
- **Acquisition:** `AH/<collection>/spineps/<case>_*`. **Other:** `AH/other_ct/{ctspine1k,ribfrac}/spineps/`, `RS/data/carmlspine/spineps/` (148 also have `*_seg-vert_msk_veridah.nii.gz`), plus the cadaver sets' own directories.

**Relabel stores are part symlink.** In `tsv3_ctd`, 431 `seg-vert` entries are symlinks back to the raw `tsv3` mask. In
`ctd_relabel/bench_ts_native` there are 31. In both cases the mask was never relabelled, so those rows are marked `raw`.
Every `ctd.json` in a relabel store is a symlink to the raw store's ctd, and `relabel.json` holds the id map.

**Where the id state comes from.** The per-store states are the ones CORPUS.md section 4 states. A sampled
`harvest.json` shows the `naming: verse_ok` verdict for acquisition (amos22), RibFrac, CTSpine1K and spineps_patch. The
sampled CTSP, COBRA (both stores), C-ArmLSpine and one PANORAMA `harvest.json` carry no naming block. For those stores
the state rests on CORPUS.md, not on a per-file check. **Every arm should pass every mask through
`tools/spineps_ids.assert_verse_monotonic` regardless.**

## 5. What each arm has to fill, read off the lists

| need | tier 1 | tier 2 |
|---|---:|---:|
| CTs without any SPINEPS mask (arm B's rib features need the vertebra instance mask) | 113 (TS 65, AbdomenAtlas 13, IDC 13, COBRA 11, FDG-PET-CT 7, CTSP 0665, AMOS 1, Kidney 1, Deep-PSMA 1) | 0 by definition |
| raw-id SPINEPS masks (guard, or relabel first) | 108 (TS 95, VerSe 13) | 422 (TS) |
| TS output is the roi subset with **no hips** (arm A gap-fill; Dataset803 is the only pelvis) | 1,889 | 10,800 |
| no TS output at all | 0 | 1 |
| Möller published rib masks already on disk (VerSe predicted 337 series, 41 manual; RibFrac manual 31) | VerSe: 337 of 374 series | RibFrac: 31 manual masks across its 660 CTs (35 in tier 1, 620 in tier 2; which CTs carry them is not joined here) |

**PANORAMA is incomplete.** SPINEPS array 40430887 (4 tasks, 17.5 h in at 00:30) had written 910 masks. Those 910 are in
tier 2, out of 1,494 gate-passed CTs. Its call step 40430888 and summary 40430889 are pending on it, so PANORAMA has no
flags yet. When those jobs finish, re-run the listing and the builder: the new masks enter tier 2, and any flagged
PANORAMA person moves to tier 1.

## 6. Disk and a rough size of the outputs

- **Free space.** `df-ceph oschome`, 2026-09-27 00:40: 20 TB quota, 26.86 % used (about 5.4 TB). **About 14.6 TB is
  free.** The home directory (4.3 TB Panasas soft quota, 93 % full per CLAUDE.md) must not receive outputs.
- **Size bases, measured on disk:**

  | item | size |
  |---|---|
  | SPINEPS `seg-vert` mask | 0.86 MB mean (tier 1), 0.93 MB (tier 2) |
  | TS `total` multilabel | 2.0 MB (tier 1), 1.8 MB (tier 2) |
  | CTSP v11 label | 1.5 MB |
  | Möller predicted rib mask | 0.25 MB (82.8 MB zip / 337 masks) |
  | Möller manual rib mask | 0.40 MB mean (41 masks) |
  | Möller nnU-Net weights | 1.7 GB, already on the grid |

- **Estimate of new files per CT:**

  | output | size per CT |
  |---|---|
  | Möller rib mask | about 0.5 MB |
  | Möller rib measurements and features | about 0.1 MB |
  | Dataset803 prediction (L1-L5, sacrum, hips), kept once | about 1 MB |
  | pelvis-only copy | about 0.3 MB |
  | arm A hip/femur/sacrum gap-fill, roi-subset CTs only | about 0.5 MB |
  | rows and JSON | under 0.05 MB |
  | three-panel render | about 0.4 MB each |

  Tier 1 comes to 5,094 x 1.9 MB + 1,889 x 0.5 MB + about 2,000 renders, which is **about 11 GB**. Tier 2 comes to
  12,217 x 1.9 MB + 10,800 x 0.5 MB + about 1,500 renders, which is **about 29 GB**. **The total is about 40 GB, around
  0.3 % of the free space.**
- **Transient space:** nnU-Net resampled volumes and any per-fold probabilities are the large items. Run the Dataset803
  ensemble as one `nnUNetv2_predict -f 0 1 2 3 4` call without `--save_probabilities`, so that the folds are averaged in
  memory, and keep per-case scratch under `/dev/shm`. The Möller container (`ctspinopelvic1k-spineps.sif`, still to be
  pulled inside an sbatch job) is a few GB once.
- **The login node's `/tmp` was 100 % full at 00:40** (25 GB). A here-string failed there. Keep anything run on the
  login node free of temporary files.

## 7. How this was made (re-runnable)

- `RS/ruleclass/code/probe_t2.sh` and `probe_t3.sh` (login node; `find -printf '%p\t%s\t%l'` of every SPINEPS, TS and
  CT store) write `RS/ruleclass/tiers/_listing/`. A local copy was in `<session scratchpad, not kept>`.
- `build_tiers.py` (surviving copy: `/rs/rs_grp_oschome/go2432/ruleclass/code/build_tiers.py`; the session scratchpad copy was not kept) joins the listings with `corpus_pull.tgz`
  (extracted to `tiers/cp/`), `registry.csv` and `classifiers_by_person.csv`. It writes `tiers/out/`, which is then
  rsynced to `RS/ruleclass/tiers/`. `tier_stats.py` prints the section 1 table.
- `RS/ruleclass/code/check_paths.sh` (login node, `[ -e ]` only) stat-tests every path column. The result was 0 missing.
- `tier_counts.json` (grid and `tiers/out/`) holds the per-collection counters. Its SPINEPS orphan check lists every
  mask in any store that no row references, and it came back empty.

## 8. Not known

- Whether the CTSP, COBRA, C-ArmLSpine and PANORAMA SPINEPS masks are VerSe-coded file by file (section 4). The state
  rests on CORPUS.md, and no voxel was read.
- Which near-duplicate candidates (1,186 CTs) are the same person. This includes the 150 CTSpine1K MSD-T10 liver CTs
  that CORPUS.md places inside AbdomenAtlas, which are not matched per CT here. A person count across collections is
  an upper bound.
- Whether the 210 untiered TotalSegmentator scans (SPINEPS failed, `failed.json`) hold a spine at all. The TS registry
  calls most of them `no_count`.
