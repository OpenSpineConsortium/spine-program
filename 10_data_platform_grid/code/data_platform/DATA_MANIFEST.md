# Data manifest: every imaging source of the spine projects

Written 2026-10-08 from files on this laptop only (no grid, no network). It merges five families of source cards into one card per source, and keeps every fact and citation the cards hold. Where nothing on disk says a thing, the card says "not recorded". Machine-readable twin: `sources.yaml` (and `sources.json`, the same data). Layout on CephFS: `LAYOUT.md`. Move procedure: `MIGRATION_PLAN.md`. Re-acquisition: `reacquire/`. Index: `db/`. Checks: `VERIFICATION.md`.

The storage census (Slurm job 40578909, `/rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/`) had not reported when this was written. Every size and "where it is now" line is the dated figure its citation gives (the 2026-10-07 top-level listing, the 2026-09-01 `du`, the 2026-09-22 hashed manifest, the 2026-09-25 census table). Regenerate the plan tables with `plan/build_plan.py --census <census.tsv>` when it lands.

## 1. What the holding is

Three projects (CTSpinoPelvic1K, the SchwingNet level-identification work and the spine-detector) collected imaging of the spine from public releases, built their own releases and render banks on top, and harvested published fluoroscopy. This manifest lists **211 sources**: 176 upstream releases, 7 project releases, 23 derived products (render banks, nnU-Net datasets, synthetic CTs), 2 derived output roots and 3 data requests that were drafted but not sent. A 212th card, `spondy_landmark`, held the one folder nobody had identified; read on the grid on 2026-10-08 (scr:inspect_unknown.out), it is a second download of Mendeley 5jdfdgp762, and its card is merged into that release's (the old id stays as an alias). Of these, 115 are on disk on the grid (HOME, Ceph or both; `sources.json` status on_disk, on_disk_partial or on_disk_state_unknown), 23 are planned, 7 are gated by an agreement nobody has signed, 58 were excluded (licence, or no new people), and the remaining 8 are on Hugging Face only (1), on this laptop only (1, the BUU-LSPINE 400 sample), deleted (1), an empty directory (1), not acquired (1) or requests drafted and not sent (3).

| family | what it covers | sources | on disk | planned | gated | excluded | other |
|---|---|---:|---:|---:|---:|---:|---:|
| A | the CT releases the project was built on, their nnU-Net datasets and CT render banks | 30 | 29 | 0 | 0 | 0 | 1 |
| B | the anomaly-harvest CT acquisitions | 144 | 56 | 23 | 7 | 58 | 0 |
| C | real X-ray and fluoroscopy with 3-D truth or pose | 12 | 12 | 0 | 0 | 0 | 0 |
| D | plain-film and harvested 2-D corpora and their banks | 24 | 17 | 0 | 0 | 0 | 7 |
| E | the disk map (locations); one source carded only here (polypose_synthetic) | 1 | 1 | 0 | 0 | 0 | 0 |

On-disk sources by modality (the same 115; a source can hold several): CT 80, RENDER 19, DX 14, RF 9, XA 4, CBCT 3, VIDEO 2, MR 1, MIXED 1. CT = computed tomography volumes; CBCT = cone-beam CT volumes or projection sweeps; DX = plain film; RF = fluoroscopy; XA = C-arm spot frames stored as DICOM XA; RENDER = synthetic (DRR, diffusion, generated).

**The largest pieces, by the families' cards** (each number carries its card's citation):

- CT the projects were built on: TCIA CT COLONOGRAPHY (825 patients, 3,451 series), CTSpine1K (1,005 volumes), CTPelvic1K, VerSe'19/'20 (374 scans, 355 patients), TotalSegmentator v2.0.1 (1,228) and v3.0.0 (1,939), RSNA 2022 cervical (2,019 studies), RibFrac (660); and the project's own CTSpinoPelvic1K (802 records; Zenodo v11, 10.5281/zenodo.22797014).
- CT fetched to find transitional spines (family B): 39 IDC collections (3,600 series, 3,499 usable CTs), FDG-PET-CT-Lesions (900), AbdomenAtlas 3.0 Mini (7,649 usable), AMOS22 (723), the NLST pilot (500), CTPelvic1K clinical (172), CSI 2014 (20), ten late Zenodo collections, and the 70-CT validation set; 88 more family-B sources are not fetched (23 planned, 7 gated, 58 excluded, counted from `sources.json` statuses). `acquisition/ranking.csv` has 146 rows; three of its unfetched rows (idc:ct_colonography, zenodo:ribfrac, hf:ctspine1k_noncolonog) are carded under family-A ids.
- Real X-ray and fluoroscopy with 3-D truth (family C): C-ArmLSpine (149 sessions, 299 spot frames, 602 sweep projections, 149 CBCTs), DeepFluoro in three copies, COBRA2026 (692 cases, 375,618 projections, 771 GB), the Geneva hip phantom, the Ljubljana lumbar gold standard, SpineSAC.
- Plain film (family D): CSXA (4,963), BUU-LSPINE (3,600 patients, 7,200 films; plus the 2000 and 400 sets), NHANES II (17,073 films, 543 with landmarks), VinDr-SpineXR (10,466 images, DUA), AASCE (609 labelled), Mendeley 5jdfdgp762 (714), IEEE lateral 236, Spinal-AI2024 (20,000 synthetic), the spine-detector corpus, FluoroCap (literature harvest, 316 GB) and public fluoroscopy clips.

**Where it sits.** HOME (`/wsu/home/go/go24/go2432`, Panasas) held 4,050 GB of a 4,295 GB soft quota on 2026-10-07 (pan_quota in the orchestrator's brief; no file on this laptop holds that number). The Ceph volume (`/rs/rs_grp_oschome/go2432`, 20 TB) used 4,482 GB on 2026-09-25 (ssn:docs/CENSUS_TABLE_2026-09-25.md §4) and about 6 TB on 2026-10-07 (brief). The disk map classifies 1,404 top-level entries; 230 hold imaging (HOME 13 raw + 151 derived, Ceph 28 raw + 38 derived), 15 are unidentified (family E's count of 2026-10-07), and no HOME imaging folder has been moved yet (family E section 1). The grid inspection of 2026-10-08 (scr:inspect_unknown.out) identified 13 of the 15 HOME entries nobody had named (the 14 disk-map rows of role unknown, and `~/data/spondy_landmark`) and the empty Ceph folder `$RS/data/morphdef`: five hold imaging and move in batch B14 into the folders of their sources, together with `~/qc.tar.gz` (QC renders of the build); eight are software, molecular simulation, the documents of an earlier project or a file holding a GitHub token, and stay on HOME; two download leftovers were not reached (MIGRATION_PLAN.md section 5, B14). The migration plan moves **219 HOME items, 3256.6 GB where a size is recorded (3.26 TB), plus 157 items whose size no file records** (batches B00-B11 and B14; the 211 quoted before 2026-10-08 counted the inspect-only `~/data/spondy_landmark` as an item and left out the six B14 moves); 1590.3 GB of the sized total are deletion candidates for Greg (plan/migration_batches.csv, generated from plan/disk_map.csv). The 192.8 GB of CT inodes that `~/data/CTSpinoPelvic1K` shares with `~/CTSpinoPelvic1K/data/hf_export_osc` are counted once; an unsized parent that moves whole takes the sum of its sized children; `~/spinesurg-ct-nnunet/nnunet/raw` stays on HOME. These sizes are dated and partly stale: with what stays on HOME they add up to more than the 4,050 GB HOME holds (MIGRATION_PLAN.md section 10), and the census decides.

**What is not known yet**: the current size of most HOME entries made after 2026-09-01 (a 2026-09-19 `du` sizes three: `~/spinesurg-ct-nnunet` 363G, `~/spine-detector` 382G, `~/nhanes_pseudo` 74G; ssn:docs/CONTINUANCE_2026-09-19.md L27) and of every Ceph entry after 2026-09-25; what remains of `~/CTSpinoPelvic1K/data`: a memory note says reclaim phases A and B ran on 2026-09-07 (mem:zenodo-deposit.md L30), no job log is on this laptop, and the phase-A/B folders, including the HOME copies of CTSpine1K and CTPelvic1K and `hf_export_osc`, are presumed deleted pending the census; what the two download leftovers `~/to_greg.zip?origin_team=T5G027G83` and `~/view?usp=sharing` are (the grid inspection of 2026-10-08 identified the other 13 HOME entries nobody had named; MIGRATION_PLAN.md section 5, B14). Each family's unknowns table (section 10) lists every gap with where it was looked for.

## 2. How to read this file

- Sections 5-9 hold one card per source, grouped by the family that wrote it. A card has the thirteen fields every family used: source id, name and citation, modality, position/view, licence and access, how it was acquired, when, what it contains, where it is now, annotation status, derived products, known defects and gaps, re-acquisition recipe.
- **Merged cards.** Where two families carded the same source, the card shows each family's text under a tag `[A]`, `[B]`, `[C]`, `[D]` or `[E]`. Family E (the disk map) carded 48 sources the other families also carded; its text is kept as the `[E]` part of those cards. Six more merges join one upstream release that two families named differently: `hf_ctspine1k_noncolonog` into `ctspine1k`, `zenodo_ribfrac` into `ribfrac`, `idc_ct_colonography` into `tcia_ct_colonography`, `ctpelvic1k_clinic` into `ctpelvic1k`, `xrsp1k_drr` into `xrspinopelvic1k`, and, on 2026-10-08, `spondy_landmark` into `mendeley_5jdfdgp762` (the folder it carded was identified on the grid; its old card is kept verbatim, collapsed, at the end of the Mendeley card). The old ids stay as aliases in `sources.yaml` and in `reacquire.py`.
- **Citations** are written as each family wrote them, so a tag tells you which legend applies. Family A uses the prefixes `ssn:` (spinesurg-ct-nnunet), `ctsp:` (CTSpinoPelvic1K-1), `vfr:` (NextPaper/VerSeFusion), `sps:` (spinopelvic-seg), `mem:` (the memory notes), `cen:` and `dp:` (scratch folders) and short names such as AUDIT, MDMR, KI, DEP, RECLAIM, MANSUM, LIST, DUD; its legend opens section 5. Family B writes paths relative to spinesurg-ct-nnunet, `acquisition/...` for the acquisition results folder and `listing` for the top-level listing; its legend opens section 6. Family C writes bare repository paths, `LISTING`, `MEM/<name>` and `LOCAL-THIS-SESSION`; its conventions open section 7. Family D uses `sscn:`, `ctsp:`, `xrsp:`, `sdet:`, `mem:`, `census:`, `sdr:`; its table opens section 8. Family E uses `scr:`, `nnunet:`, `ctsp:`, `mem:` and bare document names; its legend is in section 9.
- Scratch paths (`cen:`, `dp:`, `scr:`, `census:`, `LISTING`, `listing`) are the session scratchpad `<session scratchpad; not a dependency>/`. The disk map and path-reference files they name are copied into `plan/` (disk_map.csv, path_refs_files.csv, path_refs_summary.csv) so they survive the scratchpad.
- Dates: a directory date in the listing is a modification time, not an acquisition date. Each timeline row says how its date is known.
- **Re-acquisition.** A card's recipe field is the families' text. The runnable form is the `reacquire` block of `sources.json`, printed by `reacquire/reacquire.py <id>`; cards whose block changed in the 2026-10-08 second pass say so in an italic line at the top of their recipe field.

## 3. Dated-acquisition timeline

When each source reached the grid (or this laptop), and how that date is known. "doc" = written in a document or log the card cites; "git" = a commit date of the tool; "listing" = a directory mtime; "du" = present in the 2026-09-01 du. Rows marked *release imaging date* give when the release's images were taken, not when we fetched them. Sources with no date on record are listed after the table.

| date | source(s) | how the date is known |
|---|---|---|
| 2002 | `ljubljana_2d3d_gs` | *release imaging date*: release member dates (imaging, not our acquisition) |
| 2022-03-30 | `deepfluoro_vendor` | doc: deposit released (HANDOFF_2026-09-21_PM L268-L271) |
| 2023-11-11..2023-12-12 | `carmlspine` | *release imaging date*: release DICOM StudyDate (SchwingNet/results/carmlspine_day_groups.json): imaging dates, not acquisition by us |
| 2026-02-12 | (history; not a source) | listing: `~/docs`, ten documents of an earlier spine-level project, "Bulletproof Weak Label Generation v4.0, Complete Fix for Spine-Level-AI" (weak labels with T12-rib and L5-transverse-process detection); documents only, the script they describe is not in the folder; stays on HOME (scr:inspect_unknown.out) |
| 2026-04 | `tcia_ct_colonography` | doc: G0 §2 (month only); git: download script in first commit 2026-04-18 |
| by 2026-04-25 | `ctspine1k`, `ctpelvic1k` (HOME copies) | git: CTSP `slurm/download_raw.sh` downloads both in the first commit 550cfff (2026-04-18); doc: the April export fused CTSpine1K vertebral masks with CTPelvic1K pelvic masks (CRC L51, L247, L329-L331). Upper bound only; the exact day is not recorded. The 2026-05-16 "use token" commit 1080b1c may mark a re-run; its message is the only evidence |
| 2026-04-25 | `ctspinopelvic1k_april` | doc: HF export finalized (CRC L193); git 8f1ed51 |
| 2026-04-27 | `nnunet_dataset802_803` | git: spine_convert.sh first commit; training from 2026-05-03 (CRC L327-L329) |
| 2026-05-12 | `verse19_20` | doc: data/raw ctime (G0 §2); git: download tool 2026-05-11/12 |
| 2026-05-13 | `versefusion` | doc: canonical 2026-05-13 00:01 (G0 §2) |
| 2026-06-12 | `ctspinopelvic1k_build_tree` | listing: `~/qc.tar.gz`, the pelvis-propagation QC renders (scr:inspect_unknown.out); git: ctsp:scripts/viz_propagation.py first committed that day (f20c2c5) |
| 2026-06-24..2026-08-15 | `xrspinopelvic1k` | git log of the local clone |
| 2026-06-24 | `buu_lspine_400_sample` | local file dates |
| 2026-08-06 | `buu_lspine_2000` | doc + local file date |
| 2026-08-10 | `xrspinopelvic1k` | listing mtime |
| 2026-08-11 | `xrspinopelvic1k` | listing: `~/dis_renders`, five PNGs named by BUU films (scr:inspect_unknown.out) |
| 2026-09-01 | `cm_spine_drive_file` | doc: directory created |
| 2026-09-01..2026-09-09 | `csxa_cervical_xray_atlas` | doc: grid ctime of `CSXA-dataset-main/LICENSE` 2026-09-01 22:50 (repository archive) and of the images directory 2026-09-09 23:00 (G0 §2) |
| 2026-09-01 | `buu_lspine_v1_smoke`, `nhanes2_zenodo_landmarks` | doc: grid ctime 23:28 of `buu_v1` and of the NHANES annotated zip and its `.download_complete` (G0 §2) |
| before 2026-09-02 | `mendeley_5jdfdgp762` | sdet manifest file date |
| 2026-09-02 | `spine_detector_corpus` | sdet manifest file date |
| 2026-09-07 | `ctspinopelvic1k` | doc: v10 published, grid working copy and HF upload (AUDIT L611, L906) |
| 2026-09-07 | `ctspinopelvic1k_build_tree` | doc: build archive published (mem:zenodo-deposit.md) |
| 2026-09-07 | `nnunet_dataset810` | doc: launched 2026-09-07, retired 2026-09-08 (mem:lstv-oneshot-training-run.md) |
| before 2026-09-07 | `aasce2019_boostnet` | memory: corpus rebuilt that day holds 8,069 AASCE instances |
| 2026-09-07 | `spine_detector_corpus` | memory: manifest rebuilt |
| 2026-09-07..2026-09-10 | `vindr_spinexr` | doc: `LICENSE.txt` and `SHA256SUMS.txt` ctime 2026-09-07 17:49 (G0 §2); `.download_complete` 2026-09-10 17:25 (AUDIT gap row; G0 §2) |
| 2026-09-08 | `nnunet_dataset813` | doc: labelsTr dated 2026-09-08 (AUDIT L624); 5-fold archived 2026-09-11 |
| 2026-09-09 | `buu_lspine_3600` | doc: grid ctime of `~/spine-detector/data/raw/buu_full` 2026-09-09 22:50, the full v1 re-download (G0 §2) |
| 2026-09-09..2026-09-23 | `nhanes2_cdc_films` | doc: full film set from 2026-09-09 13:03, `.download_complete` 2026-09-23 03:00 (G0 §2); event: the download loop was cancelled on 2026-09-11 (AUDIT NHANES gap row) |
| 2026-09-10 | `ctspinopelvic1k_build_tree` | listing: `~/pitest` 11:38 and `~/pdwtest` 16:09, scratch copies of release label files (scr:inspect_unknown.out) |
| 2026-09-11..2026-09-18 | `ctspinopelvic1k_build_tree` | listing and logs: `~/s1v11`, the v11 build (jobs 40198228, 40198880, 40309073, 40309160); labels.zip stored on Zenodo 2026-09-18 22:46 (upload_zip.log; scr:inspect_unknown.out) |
| 2026-09-12 | `versefusion` | listing + git: vf_813 / convert_versefusion.py |
| 2026-09-12 | `nnunet_dataset815` | doc: built 2026-09-12/13 (AUDIT L684); flags repaired 2026-09-23 |
| 2026-09-13 | `verse_soft_drr` | doc AUDIT L669; listing |
| 2026-09-13 | `ctsp_drr_obl` | doc AUDIT L674; listing |
| 2026-09-13..2026-09-18 | `fluorocap` | doc: FLUOROCAP_PROTOCOL.md; LOCK_A/B.json; AUDIT FluoroCap rows |
| 2026-09-14 | `totalsegmentator_v201` | doc: dl.log 10:16, zip 12:36 (G0 §2) |
| 2026-09-14 | `physics_drr`, `implant_ct_synthetic` | git tool; listing mtime |
| 2026-09-14 | `physics_rare` | listing mtime |
| 2026-09-14 | `fluorogen_synthetic` | memory: start |
| 2026-09-15 | `lstv_flag_renders` | git tools; listing mtime; 0533 job 2026-09-23 |
| 2026-09-15 | `aasce_drr` | listing |
| 2026-09-16 | `spinalai_drr` | listing; tool 2026-09-17 (git) |
| before 2026-09-16 | `ieee_dataport_lateral_fullspine_236`, `spinal_ai2024` | listing bound |
| 2026-09-18 | `ctspinopelvic1k` | doc: v11 published on Zenodo (AUDIT L611) |
| 2026-09-19 | `totalsegmentator_v300` | doc: dl.log 12:50, zip 14:36 (G0 §2; AUDIT L485) |
| 2026-09-19 | `rsna_2022_cspine` | doc: AUDIT L342, fetch.log rc=0 |
| 2026-09-19 | `ribfrac` | listing: HOME/data/ribs; doc CONTINUANCE_2026-09-19 L25 |
| 2026-09-19 | `mendeley_5jdfdgp762` (second download, `~/data/spondy_landmark`) | listing: folder 13:03; url.txt, files.json and dl.log of that day (scr:inspect_unknown.out) |
| 2026-09-19 | `verse_drr` | doc: rendered 2026-09-19 (AUDIT L250, L668); listing 2026-09-20 |
| 2026-09-19 | `ts_drr_v3` | doc: complete 2026-09-19 18:25 (AUDIT L360) |
| 2026-09-19..2026-09-23 | `sx_stitch_request` | drafted (not acquired) |
| 2026-09-20 | `ts_drr` | listing; tool 2026-09-19 (git) |
| 2026-09-20 | `deepfluoro_h5` | doc: g0_facts §2; git 057d77a |
| 2026-09-21 | `carmlspine` | doc: g0_facts §2 grid change times; git aca0a60 |
| 2026-09-21 | `carm_drr` | git ebe51eb; listing |
| 2026-09-21..2026-09-23 | `cobra2026` | doc: g0_facts §2; RESUME_2026-09-22_PM L1281; git d4eb165 |
| 2026-09-21 | `geneva_hip` | doc: g0_facts §2 |
| 2026-09-21 | `ljubljana_2d3d_gs` | local file time and g0_facts §2 |
| 2026-09-21 | `realxray_layout` | doc: REAL_XRAY_DATASETS_SPEC.md; AUDIT line 720 |
| 2026-09-21 | `balgrist_exvivo_request` | drafted (not acquired) |
| 2026-09-22 | `ctsp_drr` | listing mtime; tool 2026-09-14 (git); 0533 re-render 2026-09-23 (AUDIT L1337) |
| 2026-09-22 | `deepfluoro_vendor` | doc: vendor files ctime 2026-09-22 01:23 (g0_facts §2) |
| 2026-09-22 | `spinesac` | listing mtime; git c7013ca and 9fcc9cf (2026-09-22). AUDIT line 716 gives the 5,490/5,492 count only |
| 2026-09-22 | `or_ready` | git c7013ca |
| 2026-09-22 | `devcorpus` | git 0fbb269; listing |
| 2026-09-22 | `aasce2019_boostnet` | doc: mirror on CEPH 01:06 |
| 2026-09-22 | `tvgh_spinexr` | probe only |
| 2026-09-23 | `ctspinopelvic1k` | doc: CT 0533 rebuilt from TCIA, HF object replaced (AUDIT L1335; mem:grid-ct-0533-truncated.md) |
| 2026-09-23 | `ctspine1k` | listing mtime of CEPH data/ctspine1k; HF tree read (tools/acquisition_census.py L399) |
| 2026-09-23 | `ctpelvic1k` | listing + acquisition/jobs.txt: datasets 6-7 on CEPH |
| 2026-09-23 | `ribfrac` | listing: CEPH data/ribfrac |
| 2026-09-23 | `anchor_drr` | listing; tool 2026-09-14 (git) |
| 2026-09-23 | `anchor_drr_c2` | listing; script 2026-09-19/20 (git) |
| 2026-09-23 | `tcia_fdg_pet_ct_lesions`, `abdomenatlas3_mini`, `amos22`, `nlst_pilot`, `csi2014`, `validation_ts`, 39 IDC tier-1 collections (`idc_*`) plus the `idc_tier1` route card | doc: acquisition/jobs.txt submission date |
| 2026-09-23 | `deepfluoro_xvr_hf` | doc: polypose.setup_status.json |
| 2026-09-23 | `spinesac` | doc: last two files, job 40416585 |
| 2026-09-23 | `polypose_synthetic` | listing mtime of CEPH data/polypose and HOME/polypose |
| 2026-09-24 | `panorama`, `barts_crl`, `kidney_thoraxabdomen`, `curvas_pdacvi`, `aortaseg60`, `curvas`, `quadra_hc`, `deep_psma`, and 2 more | doc: acquisition/jobs.txt submission date |
| 2026-09-26 | `fluoro_video_public_clips` | doc + listing |
| 2026-09-26 | `bournemouth_qf_cervical_tracks` | local file date |
| 2026-09-26 | `fluoro_cine_requests_2026_09_26` | drafted (not acquired) |

On disk with no acquisition date on record: . (Planned, gated and excluded sources have no acquisition date by definition; their ranking date is in their cards.)

## 4. Known defects that matter for the index and the migration

Selected from the cards' "known defects and gaps" fields: the ones that change a count, a key, a path or a licence decision. Every card keeps its full list. The tag before a citation names the family legend it uses.

| # | source(s) | defect | what it means here | citation |
|---:|---|---|---|---|
| 1 | ctspinopelvic1k | Published CT 0533 was a truncated gzip (17,301,504 B); rebuilt from TCIA on 2026-09-23 to 250,067,995 B and the HF object replaced; the KNOWN_ISSUES §10 note is not yet on Zenodo. | an index built from an old copy would carry the broken file | [A] KI §10; AUDIT L1345-L1353; mem:grid-ct-0533-truncated.md |
| 2 | ctspinopelvic1k | The HF mirror labels are still v10 (id 29 live) while Zenodo is v11. | never take labels/ from HF; the v11 labels on HOME are the reference | [A] AUDIT L295-L298, L913; mem:hf-mirror-is-v10.md |
| 3 | ctspinopelvic1k | The deposit README says the cohort was 'imaged supine'; the manifest has 422 supine, 377 prone, 3 decubitus. | the position column of the index must come from manifest.json, not the README | [A] DEP L223; MANSUM |
| 4 | ctspinopelvic1k | splits_5fold.json is keyed by TCIA token, not volume_id; 529 of 802 token ids collide with another record's volume_id. | the index maps folds through manifest.json token -> volume_id | [A] AUDIT L915, L926 |
| 5 | ctspinopelvic1k | manifest.n_voxels_fg is 0 in 340 of 802 records; croissant.json is listed but absent; three different transitional counts (31/33/34). | do not index these manifest fields as truth | [A] AUDIT L1368-L1373, L647, L914, L923 |
| 6 | tcia_ct_colonography | Every patient was scanned twice (prone and supine); only the SeriesInstanceUID in the CTSP manifest names the annotated volume. | a patient id resolves to several volumes; key CT items by series | [A] ctsp:data/zenodo_deposit/fetch_from_tcia.py L20-L24; KI §4 |
| 7 | ctspine1k | CTSpine1K's supine/prone 'random selection' claim is false; the selection code was deleted (recoverable at 7f44959). | the kept acquisition per COLONOG patient is an os.walk side effect | [A] mem:ctspine1k-selection-code-deleted.md |
| 8 | ctpelvic1k, verse19_20, deepfluoro_h5, deepfluoro_vendor, geneva_hip, ljubljana_2d3d_gs | Licence quoted two ways in the files (CC BY vs NC; CC BY vs CC BY-SA; CC BY-NC vs CC BY-NC-SA; CC BY-SA vs CC BY-NC; CC BY-NC-ND vs a generic CC link). | the restricted flag and the redistribution column need Greg's reading | [A] ctsp:README.md L515, ctsp:docs/DATASETS_ROADMAP.md L95, vfr:README.md L348-L350; [C] docs/DATA_COMPLETENESS_AUDIT.md lines 732, 865, 885, 866; docs/research_carm_datasets_verified_2026-09-22.json |
| 9 | verse19_20 | 10 VerSe'20 series were never downloaded; unify substituted their VerSe'19 copies silently. | VerSe item counts differ from the release | [A] AUDIT L235-L238, L952 |
| 10 | versefusion | The manifest's has_T13 = 18 describes the VERIDAH-renumbered tree (the 12 extra flags are the VERIDAH corrections applied in data/corrected); the release masks give 6. vf_813 drops C1-T9. | index T13 from the masks or the published table; never use vf_813 for whole-spine work | [A] AUDIT L948 (cause); mem:versefusion-t13-flag-wrong.md (only for the instruction to take T13 from the masks; its 'wrong label map' diagnosis is not what the files show); mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md |
| 11 | totalsegmentator_v201, totalsegmentator_v300 | v201 s1406-s1429 are byte-identical to different v300 ids; keying ts:s#### without the release splits 24 people and merges 15; tools/identity/ts_alias.json does not exist. | subject keys across the two TS releases are not reconciled | [A] AUDIT L370-L373, L497; mem:identity-audit-findings.md |
| 12 | devcorpus, totalsegmentator_v300 | The device corpus and the RSNAI manifest root call their TotalSegmentator source 'v2' while the path is v3. | lineage of the synthetic corpus is unsettled on paper | [A] AUDIT L507; [C] docs/DATASHEET.md §2.7 |
| 13 | nnunet_dataset810, nnunet_dataset813, nnunet_dataset815 | imagesTr are container-path links (/data/hf_export/ct/...) that dangle on the host; a host-side 'repair' once wiped a dataset. | never rewrite them during the move; keep HF_EXPORT_DIR pointing at a dir with ct/ | [A] mem:dataset813-image-links-are-container-paths.md; AUDIT L581 |
| 14 | nnunet_dataset813 | Built from a stale pre-consensus export: lstv_cases.json flags 23 records where the release flags 34; the label version is unrecorded. | its labels are not the v11 labels | [A] AUDIT L140-L143, L911 |
| 15 | ctsp_drr, physics_drr | ctsp_drr names a case CTSP_COLONOG_<token>, physics renders ctsp_<release id>; 357 people sat on both sides of the v6/v7 split. | the index must key render items through tools/patient_keys.py, not by name | [A] AUDIT L135-L138; mem:split-leak-cross-naming.md |
| 16 | ctsp_drr, verse_soft_drr | The A-P voxel size was written as the S-I row spacing on every render: all 801 CTSP renders before the 2026-09-19 respace (median error 7.5 %, more than 1.2x off on 172); 181 of 374 soft-tissue VerSe renders still. | mm-per-pixel of those renders is wrong | [A] mem:drr-row-spacing-defect.md; AUDIT L250-L253 |
| 17 | verse_drr, ctsp_drr_obl | verse_drr holds 13 byte-identical glgl* duplicates; ctsp_drr_obl/obl2 are VerSe renders under a CTSP prefix. | count and key these banks with care | [A] AUDIT L240-L243; MDMR L348-L355 |
| 18 | anchor_drr | Its own split puts 301 of 801 people on both sides (seeded on the implant-variant stem). | do not reuse its split | [A] AUDIT L165-L168 |
| 19 | ts_drr | Its path/ maps were computed from the v3 root although the renders are v2. | delete and rerun path_render before use | [A] AUDIT L225-L228 |
| 20 | carmlspine | Every published number used the 296-frame pre-repair bank; the repaired bank has 299 (case134 added, case39_LAT2 exported, case118 re-labelled oblique). | HOME carm_* banks all predate the repair | [C] docs/DATA_COMPLETENESS_AUDIT.md lines 200-205, 870 and Repairs 2026-09-23 |
| 21 | carmlspine | case134 headers still carry a real PatientID and name. | export tools must check every written file; the index must not store PatientID/PatientName for this source | [C] docs/DATA_COMPLETENESS_AUDIT.md Repairs 2026-09-23 'Anonymisation'; docs/PATIENT_IDENTITY_SPEC.md alias 16 |
| 22 | carm_drr | carm_drr holds REAL C-ArmLSpine frames in the DRR-bank layout; docs/CT_INVENTORY.md calls it a CBCT render bank. | the render_bank adapter marks carm_* banks as XA, not RENDER | [C] tools/carmlspine_to_bank.py docstring |
| 23 | deepfluoro_vendor | Its DOI is C304HZ, but docs/DATASHEET.md §3, docs/RSNAI_DATA_MANIFEST.json and tools/data_manifest.py ROOTS give IFSXNV (the H5 release). | fix tools/data_manifest.py before rebuilding the manifest | [C] docs/DATA_COMPLETENESS_AUDIT.md line 600 |
| 24 | deepfluoro_h5, deepfluoro_vendor, deepfluoro_xvr_hf | Three copies of one dataset (H5 release, vendor deposit, HF re-host). | any split must key by specimen across all three | [C] docs/DATA_ACCOUNTING.md §0 |
| 25 | cobra2026 | Only 145 of 692 public training cases are in any frame bank; Varian (225) is not exported; one detector arm saw the same patients up to four times (5,013 duplicate frames). | most of the release is unindexed by the banks | [C] SchwingNet/results/corpus_census.md line 288; docs/DATA_COMPLETENESS_AUDIT.md line 18 |
| 26 | geneva_hip | The manifest hashed the 69-file work directory, not the 482-file source archive. | its list_sha256 says nothing about the release | [C] docs/DATA_COMPLETENESS_AUDIT.md lines 733, 875 |
| 27 | spinesac | No data licence anywhere; the docs say one phantom where there are three; device count five or six. | reuse terms unstated: index, never redistribute | [C] docs/research_datasets_fourth_pass_verified_2026-09-22.json; docs/DATA_COMPLETENESS_AUDIT.md lines 734, 889 |
| 28 | nhanes2_cdc_films, nhanes2_zenodo_landmarks | NHANES entered banks v2, v6 and v7 twice under two names split independently: 48 of 54 validation patients had a copy in training. | the subject view v_subjects_in_several_sources exists to catch this | [D] sscn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md; mem:nhanes-double-inclusion.md |
| 29 | nhanes2_zenodo_landmarks | Zenodo page 600 annotated, VertXNet 544, the zip ships 543; extracted pickles take 159 GB for a 1.0 GB zip. | a deletion candidate (regenerable) | [D] sscn:docs/DATA_COMPLETENESS_AUDIT.md; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1 |
| 30 | vindr_spinexr | The release test split was consumed for training pseudo-labels; VinDr crops sit in fold models (IRB: covered by HPR 2026-330 since 2026-09-29; the open defect is the fold-model lineage, not the determination); 77.8 % of vindrps val cases have a same-study sibling in train. | restricted folder; not a held-out benchmark | [D] sscn:docs/DATASHEET.md section 2.6; sscn:SchwingNet/packet_src/statements.md item 5; sscn:docs/PATIENT_IDENTITY_SPEC.md section 2 |
| 31 | buu_lspine_3600, buu_lspine_2000 | The 3,600 AP films are in no level bank; BUU (2000) is mislabelled 'AASCE test split' in tools/xray_dataset_usage.py. | unannotated-film queries will show them | [D] sscn:docs/DATA_COMPLETENESS_AUDIT.md 'Unknown' rows |
| 32 | aasce2019_boostnet | The 128 labelled BoostNet test films never reached aasce_drr; the grid copy differs from the mirror in 98 challenge-test files. | keep both copies | [D] sscn:docs/DATA_COMPLETENESS_AUDIT.md AASCE row |
| 33 | mendeley_5jdfdgp762 | A redistribution: about 500 BUU persons and 12 VinDr studies. | subject keys must fold these into BUU | [D] sscn:docs/PATIENT_IDENTITY_SPEC.md section 2 mendeley row |
| 34 | spinal_ai2024 | 8,358 usable renders are 44 synthetic identities; no patient was imaged. | modality RENDER, never DX | [D] sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 4.2; sscn:tools/spinal_ai2024_to_render.py |
| 35 | fluorocap | 72.8 % of panels are reproductions with no pixel residual; human_qc_status pending on all 21,603 rows; 488 of 2,385 bank panels fail the modality gate. | all FluoroCap annotation is pseudo; directive D1 dropped it from training | [D] mem:fluorocap-is-reproductions-not-fluoroscopy.md; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md Surface N; sscn:docs/DATA_COMPLETENESS_AUDIT.md FluoroCap bug row |
| 36 | xrspinopelvic1k | data/ct and data/labels are dangling links to the deleted hf_export_v3; built from 822 cases of a pre-release export. | rebuild from v11 with ostk.labels.labels_for(volume) | [D] sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 2.3, 7.1 |
| 37 | family B (all acquisitions) | docs/CENSUS_TABLE_2026-09-25.md reports CTs on disk and gate pass one too high in every collection checked but PANORAMA; the CNS 2026 table copies the figures. | use SUMMARY.md / TIERS.md counts | [B] docs/CENSUS_TABLE_2026-09-25.md; acquisition/collections/*/SUMMARY.md; docs/ruleclass/TIERS.md section 1 |
| 38 | family B (all acquisitions) | No acquired CT carries a patient position; tools/acquisition_fetch.py was first committed after its first use; no family-B collection has a completeness-audit section. | the position column is 'unknown' until DICOM (0018,5100) is read | [B] acquisition/manifests/idc_tier1.csv header; git log tools/acquisition_fetch.py; docs/DATA_COMPLETENESS_AUDIT.md headings |
| 39 | ctspinopelvic1k_build_tree, ctspine1k, ctpelvic1k | A memory note says ctsp:slurm/reclaim_grid_space.sh phases A and B ran on 2026-09-07 (mem:zenodo-deposit.md L30); no job log is on this laptop. The phase-A/B folders, including `ctspine1k`, `ctpelvic1k` and `hf_export_osc`, are presumed deleted pending the census. | the migration's B02/B03 items are probably absent; preflight decides; the 2026-09-01 sizes of those items still sit in the sized total | [A] RECLAIM L34-L47; mem:zenodo-deposit.md L30; [E] section 1 |
| 40 | all | No HOME imaging folder has been migrated: the listing shows no HOME -> Ceph symlink. | every HOME row of the layout map is still a real directory | [E] section 1 (listing) |
| 41 | mendeley_5jdfdgp762 | `~/data/spondy_landmark`, which `nnunet:tools/ct_inventory.py` L50 lists as a CT root, is a second download of this release (identified 2026-10-08). | the index skips `raw/spondy_landmark` (README.yaml `index_skip`); a deletion candidate once the sha256 in its `files.json` matches `mendeley_716` | (2026-10-08) scr:inspect_unknown.out |
| 42 | ctspinopelvic1k_build_tree | `~/s1v11`, the v11 build workspace, holds the Zenodo upload scripts and state; its `out/v11_labels`, and the label copies `~/pitest` and `~/pdwtest`, may be hard links of the release labels (not recorded). | `derived/s1v11` is owner-only until those files are read for a token; a link-count failure in B14 is rerun with `ALLOW_NLINK_LOSS=1` after review (MIGRATION_PLAN.md section 5) | (2026-10-08) scr:inspect_unknown.out |
| 43 | xrspinopelvic1k | `~/dis_renders`: five PNGs named by BUU-LSPINE film ids; what drew them is not recorded. | treated as holding BUU pixels: owner-only (LAYOUT.md rule 8) | (2026-10-08) scr:inspect_unknown.out |

## 5. Family A: the CT releases the project was built on, their nnU-Net datasets and CT render banks

The family's own preface, legend and shared notes, verbatim:

Written 2026-10-07, from files on this laptop only (no grid or network access). Every count, date and
location has its evidence file in parentheses. Where nothing on disk says something, the card says
"not recorded". The storage census job (Slurm 40578909) had not reported when this was written, so
"Where it is now" uses the 2026-10-07 top-level listing, the 2026-09-01 `du`, and the 2026-09-23 audit.
Any directory below the top level may have changed since. The census `depth2.tsv` should be checked
against every path given here.

### Legend

Path prefixes:

| prefix | expands to |
|---|---|
| `ssn:` | `<repo spinesurg-ct-nnunet 097933a>/` |
| `ctsp:` | `<repo CTSpinoPelvic1K 7ddfe38>/` |
| `vfr:` | `<laptop folder Desktop/NextPaper; not a dependency>/VerSeFusion/` |
| `sps:` | `<laptop folder Desktop/NextPaper; not a dependency>/spinopelvic-seg/` |
| `ostk:` | `<repo OpenSpineToolkit cb43197>/` |
| `mem:` | `<memory notes; see MEMORY.md>/` |
| `cen:` | `<session scratchpad; not a dependency>/census/` |
| `dp:` | `<session scratchpad; not a dependency>/dataplan/` |

Documents cited often:

| short name | file |
|---|---|
| AUDIT | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` (line numbers given as L…) |
| MDMR | `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` |
| CTINV | `ssn:docs/CT_INVENTORY.md` |
| G0 | `ssn:SchwingNet/results/g0_facts.md` §2 "First download date" |
| PIS | `ssn:docs/PATIENT_IDENTITY_SPEC.md` §2 |
| OCT | `ssn:SchwingNet/results/transitional_registry/other_ct/SUMMARY.md` |
| ACQ | `ssn:SchwingNet/results/transitional_registry/acquisition/ACQUISITION_PLAN.md` |
| CENSUS25 | `ssn:docs/CENSUS_TABLE_2026-09-25.md` |
| DEP | `ctsp:data/zenodo_deposit/README.md` (local copy of the deposit README; its version table already lists v11) |
| KI | `ctsp:data/zenodo_deposit/KNOWN_ISSUES.md` |
| BUILD | `ctsp:docs/BUILD_CHAIN.md` |
| RECLAIM | `ctsp:slurm/reclaim_grid_space.sh` |
| CRC | `ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` |
| MANSUM | output of `dp:ctsp_manifest_summary.py` over `ctsp:data/zenodo_deposit/manifest.json` (run 2026-10-07) |
| LIST | `cen:toplevel_listing.txt` (top-level entries with mtime, taken 2026-10-07) |
| DUH / DUD | `cen:_du_home.txt` / `cen:_du_data.txt` (`du` of HOME top level and of `HOME/CTSpinoPelvic1K/data`, taken 2026-09-01) |

Roots: HOME = `/wsu/home/go/go24/go2432` (Panasas). CEPH = `/rs/rs_grp_oschome/go2432`.

Date tags: [doc] means a date written in a document; [git] means a commit date of the tool; [listing]
means the directory mtime in LIST; [du] means present in the 2026-09-01 `du`.

Cards in this file: A1 tcia_ct_colonography, A2 ctspinopelvic1k, A3 ctspinopelvic1k_april,
A4 ctspinopelvic1k_build_tree, A5 ctspine1k, A6 ctpelvic1k, A7 verse19_20, A8 versefusion,
A9 totalsegmentator_v201, A10 totalsegmentator_v300, A11 rsna_2022_cspine, A12 ribfrac,
A13 spondy_landmark (merged into mendeley_5jdfdgp762 on 2026-10-08), A14 nnunet_dataset802_803, A15 nnunet_dataset810, A16 nnunet_dataset813,
A17 nnunet_dataset815, A18 ctsp_drr, A19 physics_drr, A20 physics_rare, A21 verse_drr,
A22 verse_soft_drr, A23 ctsp_drr_obl, A24 ts_drr, A25 ts_drr_v3, A26 anchor_drr, A27 anchor_drr_c2,
A28 implant_ct_synthetic, A29 lstv_flag_renders, A30 spinalai_drr, A31 aasce_drr, A32 xrsp1k_drr.
Then: migration hazards for this family, and the unknowns table.

---

### Cards

### `tcia_ct_colonography` <a id="tcia_ct_colonography"></a>

**TCIA CT COLONOGRAPHY.** Cards: A (A1 tcia_ct_colonography), B (IDC CT Colonography remainder (held)), E (tcia_ct_colonography). Also known as: `idc_ct_colonography`. Structured entry: `sources.yaml` id `tcia_ct_colonography`; kind upstream_release; status on_disk_state_unknown; re-acquisition submit (tcia_ctsp_download).

**Source id**

*[A]*

`tcia_ct_colonography`: the imaging behind all 802 CTSpinoPelvic1K records (ctsp:README.md L25-L33).

*[B: card `idc_ct_colonography`]*

`idc_ct_colonography` (acquisition/ranking.csv collection `idc:ct_colonography`)

*[E]*

`tcia_ct_colonography` (family A's id)

**Name and citation**

*[A]*

- Smith K, Clark K, Bennett W, et al. "Data From CT COLONOGRAPHY", The Cancer Imaging Archive, 2015, doi 10.7937/K9/TCIA.2015.NWTESAY1 (ctsp:README.md L462-L471).
- Release page: https://doi.org/10.7937/K9/TCIA.2015.NWTESAY1 (ctsp:README.md L470).
- Also on IDC. IDC was not used for this collection: the remaining ~23 non-CTSP patients are held back until CTSP tokens are matched to IDC PatientIDs (ACQ L287-L290).

*[B: card `idc_ct_colonography`]*

IDC collection_id `ct_colonography`, TCIA DOI 10.7937/k9/tcia.2015.nwtesay1; alias of CTSpinoPelvic1K (802 of its 825 PatientIDs), which belongs to another family (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 5)

*[E]*

TCIA CT COLONOGRAPHY collection, about 3,451 series (`ctsp:scripts/download_tcia_colonog.py` docstring).

**Modality**

*[A]*

CT (DICOM), abdominopelvic CT colonography (ctsp:README.md L25; ctsp:scripts/download_tcia_colonog.py L1-L10).

*[B: card `idc_ct_colonography`]*

CT colonography (class AP: AP:757) (acquisition/ranking.csv)

*[E]*

CT, abdomen and pelvis.

**Position/view**

*[A]*

- Prone and supine, per patient (ctsp:README.md L25).
- In the 802 released records the per-record `position` is: supine 422, prone 377, decubitus_right 2, decubitus_left 1 (MANSUM).
- The whole-collection breakdown by position is not recorded in any document read.

*[B: card `idc_ct_colonography`]*

not recorded in this family's files (no manifest was written for the remainder) (tools/acquisition_census.py)

*[E]*

prone and supine pairs (`DATA_ACCOUNTING.md` 3).

**Licence and access**

*[A]*

- Open, CC BY 3.0. The CT images are redistributed unmodified, with attribution (ctsp:README.md L508-L510).
- Covered by WSU IRB HPR determination 2026-269 as public de-identified data (G0 §3).

*[B: card `idc_ct_colonography`]*

open, CC BY 3.0 (acquisition/ranking.csv)

*[E]*

not recorded in Family E's evidence. The route is the TCIA API through `tcia_utils` (`ctsp:scripts/download_tcia_colonog.py`).

**How it was acquired**

*[A]*

- `ctsp:slurm/download_raw.sh` stage 1/3 runs `scripts/download_tcia_colonog.py --out_dir /data/tcia --workers $WORKERS` inside `containers/ctspinopelvic1k.sif` (ctsp:slurm/download_raw.sh L133-L153).
- The tool lists every CT series in "CT COLONOGRAPHY" with `tcia_utils.nbia.getSeries(collection, modality="CT")` and calls `downloadSeries` per SeriesInstanceUID, three retries, threaded (ctsp:scripts/download_tcia_colonog.py L1-L22 and L142).
- Route: NBIA REST through tcia_utils (ctsp:scripts/download_tcia_colonog.py L49-L55).
- Verification: DICOM count ≥ `ImageCount` from getSeries, otherwise "any .dcm present" (ctsp:scripts/download_tcia_colonog.py L17-L22, L62-L75).
- No checksums.
- `scripts/build_db.py` then indexed it into `patient_db.json`: 825 patients, 3,451 series (PIS row ctsp).

*[B: card `idc_ct_colonography`]*

not fetched: held out of `idc_tier1.csv` until every CTSP token is matched to an IDC PatientID, because a partial match would re-admit CTSP people under a new key (tools/acquisition_census.py; acquisition/ACQUISITION_PLAN.md section 5)

*[E]*

`tcia_utils.getSeries()` and `downloadSeries()` in a thread pool with three retries. A series counts only when `dcm_count >= ImageCount` (`ctsp:scripts/download_tcia_colonog.py`). It is launched by `ctsp:slurm/download_raw.sh`.

**When**

*[A]*

- April 2026, month precision [doc] (G0 §2 row CTSpinoPelvic1K).
- The download script is already in the first commit, 550cfff, 2026-04-18, and was patched by "fix raw" 8e68379 on 2026-04-19 [git] (`git log ctsp:scripts/download_tcia_colonog.py`).
- `patient_db.json` was rebuilt on 2026-05-16 (G0 §2).
- The exact download day is not recorded.

*[B: card `idc_ct_colonography`]*

held since the census of 2026-09-23 (acquisition/ACQUISITION_PLAN.md); HOME holds `_tcia_patients.py`, `_tcia_patients.sh`, `_tcia_patient_check.json`, `idcensus.py` dated 2026-09-22 (contents not read here) (listing)

*[E]*

the script was first committed 2026-04-18 (`git log ctsp:scripts/download_tcia_colonog.py`). The folder date is not in the listing.

**What it contains**

*[A]*

- 825 patients and 3,451 CT series (PIS row ctsp; ctsp:slurm/download_raw.sh L17 says "~3451 series").
- On disk: `HOME/CTSpinoPelvic1K/data/tcia` was 721 GB on 2026-09-01 (DUD). The script header estimates ~250 GB (ctsp:slurm/download_raw.sh L17).
- `tcia_nifti` (dcm2niix reference NIfTIs, one per series) was 336 GB (DUD; ctsp:data/README.md L33-L34).
- `du` on Panasas counts allocated blocks, not apparent size, so the 721 GB is not comparable with the estimate (AUDIT L515).

*[B: card `idc_ct_colonography`]*

825 PatientIDs listed, 757 qualifying series, 21 new after the 802-person alias; 6.0 GB for the remainder; 485.0 GB all CT (acquisition/ranking.csv); the plan says about 23 people (acquisition/ACQUISITION_PLAN.md section 5)

*[E]*

DICOM by SeriesInstanceUID (`ctsp:data/README.md`). du was 721G for `tcia` and 336G for `tcia_nifti` on 2026-09-01 (`_du_data.txt`). The README's budget is "110 GB / 350 GB" (filtered / all), so the 721G exceeds both estimates, for a reason that is not recorded.

**Where it is now**

*[A]*

- HOME `CTSpinoPelvic1K/data/tcia` (raw DICOM) and HOME `CTSpinoPelvic1K/data/tcia_nifti` (converted) were present on 2026-09-01 (DUD).
- Neither is on RECLAIM's phase A or phase B delete list (RECLAIM L34-L47).
- Their state after 2026-09-01 is not recorded. G0 §2 says "No on-grid trace of the April download survives", but it names only `hf_export` as gone.
- CEPH holds only the single re-fetched series for record 0533: `CEPH/data/ctsp0533_repair/` (AUDIT L1335-L1347; LIST 2026-09-23).

*[B: card `idc_ct_colonography`]*

the remainder is not on disk (listing); the 802 CTSP people are on HOME under CTSpinoPelvic1K (another family) (scratchpad census/_du_data.txt)

*[E]*

`~/CTSpinoPelvic1K` (HOME, raw, 1,945.6 GB, listing 2026-09-13); `~/CTSpinoPelvic1K/data/tcia` (HOME, raw, 721.0 GB); `~/CTSpinoPelvic1K/data/tcia_nifti` (HOME, converted/derived, 336.0 GB)

**Annotation status**

*[A]*

None in TCIA itself. Annotation enters through CTSpine1K (A5) and CTPelvic1K (A6) (ctsp:README.md L25-L33).

*[B: card `idc_ct_colonography`]*

none for the remainder (acquisition/ranking.csv)

*[E]*

none in the raw series. Labels reach these CTs through CTSpine1K, CTPelvic1K and the CTSP release.

**Derived products**

*[A]*

- `patient_db.json` (13 MB) and `patient_db.pkl` (DUD).
- `placed/` masks (6.1 GB) (DUD).
- All of CTSpinoPelvic1K (A2-A4).
- PanTSMini also repackages 2,810 CT Colonography volumes, which is why it was not fetched (ACQ L262-L277).

*[B: card `idc_ct_colonography`]*

none (listing)

*[E]*

CTSpinoPelvic1K (card above). none found in the disk map

**Known defects and gaps**

*[A]*

- Every patient was scanned twice, so a patient id resolves to several volumes. Only the SeriesInstanceUID in the CTSP manifest identifies the annotated one (ctsp:data/zenodo_deposit/fetch_from_tcia.py L20-L24; KI §4).
- Identity audit: zero shared (origin, spacing, direction, nz) signatures over 1,728 acquisitions. Whether the 768 numeric-id and 34 `CTC-` records overlap as people is open (mem:identity-audit-findings.md).
- `tcia_utils.downloadSeries` silently no-ops when the target directory exists (ctsp:scripts/download_tcia_colonog.py L12-L16).

*[B: card `idc_ct_colonography`]*

refused series: localizer image type:1700;reformat/MIP series:118;not a regularly spaced 3-D volume:47;slice > 3.0 mm:14 (acquisition/ranking.csv); 21 (computed) vs about 23 (prose) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md)

*[E]*

the 721G size is not explained. The 0533 repair shows that the release's own `fetch_from_tcia.py` can rebuild a single record (`mem:grid-ct-0533-truncated`).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): DATA_DIR on Ceph; conda singularity on PATH; SIF checked first. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid tcia_ct_colonography` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[A]*

- Whole collection, on a compute node with the container:
  `TCIA_ONLY=1 FORCE=1 sbatch -D <CTSpinoPelvic1K checkout> slurm/download_raw.sh`
- Or directly: `python scripts/download_tcia_colonog.py --out_dir <CEPH>/data/tcia_ct_colonography --workers 16` (ctsp:slurm/download_raw.sh L1-L45).
- Verify: per-series dcm count ≥ ImageCount (built into the tool); 3,451 series directories; 825 PatientIDs against PIS.
- Only the 802 annotated series: see the A2 recipe (`fetch_from_tcia.py`).

*[B: card `idc_ct_colonography`]*

manual gate first: match all 802 CTSP tokens to IDC PatientIDs (docs/PATIENT_IDENTITY_SPEC.md), then write a remainder manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection idc_ct_colonography --manifest <that file>` (acquisition/ACQUISITION_PLAN.md section 5; tools/acquisition_fetch.py)

*[E]*

`cd ~/CTSpinoPelvic1K && TCIA_ONLY=1 sbatch slurm/download_raw.sh` (`ctsp:slurm/download_raw.sh` usage). The tool itself checks instance counts per series. Note that the script's `#SBATCH -q primary` predates the current partition rules.

---

### `ctspinopelvic1k` <a id="ctspinopelvic1k"></a>

**CTSpinoPelvic1K (802 records, Zenodo v11).** Cards: A (A2 ctspinopelvic1k), E (ctspinopelvic1k). Structured entry: `sources.yaml` id `ctspinopelvic1k`; kind project_release; status on_disk; re-acquisition run (zenodo_http+ctsp_fetch_from_tcia).

**Source id**

*[A]*

`ctspinopelvic1k`: the 802-record release, current Zenodo v11, with the CT half rebuilt from TCIA or taken from the HF mirror (AUDIT L611-L650).

*[E]*

`ctspinopelvic1k` (family A's id; family A also cards `ctspinopelvic1k_april` and `ctspinopelvic1k_build_tree`, see 2.5)

**Name and citation**

*[A]*

- CTSpinoPelvic1K. Concept DOI 10.5281/zenodo.22139642.
- v11 = 10.5281/zenodo.22797014, published 2026-09-18, labels only (AUDIT L611, L615; CRC L332-L333).
- v10 = 10.5281/zenodo.22642578, 2026-09-07 (AUDIT L616; mem:zenodo-deposit.md).
- Earlier versions: v9 22639598, v8 22293878, v7 22242745, v6 22139643 (mem:zenodo-deposit.md).
- HF mirror: `OpenSpineConsortium/CTSpinoPelvic1K`, with 802 CT and 802 label volumes (AUDIT L617).
- Code: github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K (BUILD L6).
- Dataset article: `ctsp:paper/mpda/` (ctsp:CLAUDE.md).

*[E]*

CTSpinoPelvic1K, this project's release of 802 records. Zenodo v11 10.5281/zenodo.22797014 (2026-09-18; concept DOI 10.5281/zenodo.22139642). Zenodo v10 10.5281/zenodo.22642578 (2026-09-07). HF mirror OpenSpineConsortium/CTSpinoPelvic1K, still v10 on 2026-09-27 (`DATA_COMPLETENESS_AUDIT.md` heading line 611; `mem:hf-mirror-is-v10`). Build archive Zenodo 10.5281/zenodo.22647933 (`ctsp:slurm/reclaim_grid_space.sh` header).

**Modality**

*[A]*

- CT, abdominopelvic field of view: T10 down to the proximal femora, no C2 (ssn:tools/merge_versefusion_corpus.py docstring "FIELD OF VIEW").
- Thoracic labels stop near T8 (ssn:tools/make_drr_dataset.py L9-L11).
- In 553 of 802 records (69 %) the top labelled vertebra is cut by the field of view (KI §6).

*[E]*

CT, abdominopelvic field of view (`CT_INVENTORY.md`). Labels cover per-level vertebrae, ribs, sacrum, hips and femora (`ctsp:CLAUDE.md`).

**Position/view**

*[A]*

- Per-record `position`: supine 422, prone 377, decubitus_right 2, decubitus_left 1 (MANSUM).
- In 351 patients the spine and pelvic annotations sit on different acquisitions (`match_type` separate 351) (KI §4; MANSUM).
- The deposit README describes the cohort as "imaged supine" (DEP L223). The manifest contradicts that: 377 records are prone (MANSUM).

*[E]*

the source cohorts are CT colonography, which images one person prone and supine. 351 separate-mode pelvic acquisitions are held out (`DATA_ACCOUNTING.md` 3). Per-record position is not recorded in Family E's evidence.

**Licence and access**

*[A]*

- Open. Labels CC BY-NC-SA 4.0 (DEP L363; ctsp:README.md L511-L519).
- ShareAlike comes from CTSpine1K; CT images are CC BY 3.0 (ctsp:README.md L508-L519).
- Derived labels must stay NC-SA (ctsp:README.md L511-L519).

*[E]*

not recorded in the files Family E read.

**How it was acquired**

*[A]*

This project built and published it. Grid copies were made as follows:
- **Labels.** v11 is in HOME `data/CTSpinoPelvic1K/labels`. All 802 match Zenodo v11: `sha256sum -c SHA256SUMS.txt` gave 810 OK, 0 failed (AUDIT L620).
- **CT.** HOME `data/CTSpinoPelvic1K/ct` holds 802 files, every size equal to the HF tree (AUDIT L619).
- The mirror was uploaded from the grid copy on 2026-09-07 (AUDIT L906).
- **Record 0533** was rebuilt from TCIA by the release's own `fetch_from_tcia.py` (job 40416624, `ssn:slurm/ctsp0533_repair.sh`, nine gates) (AUDIT L1335-L1353).
- The release's own CT tool is `fetch_from_tcia.py`: tcia_utils download by SeriesInstanceUID, then dcm2niix, then trilinear resample onto the label grid with -1024 HU outside (ctsp:data/zenodo_deposit/fetch_from_tcia.py L1-L30; DEP L139-L170).

*[E]*

built by this project from TCIA CT COLONOGRAPHY, CTSpine1K and CTPelvic1K (`ctsp:slurm/download_raw.sh`; `ctsp:data/README.md`). The working copy `~/data/CTSpinoPelvic1K` holds the v10 labels and metadata from Zenodo, with the CTs hard-linked from the export (`ctsp:slurm/archive_build_inputs.sh` header). CT 0533 was rebuilt from TCIA on 2026-09-23 with the release's `fetch_from_tcia.py` (`mem:grid-ct-0533-truncated`).

**When**

*[A]*

- v10 published 2026-09-07 [doc]; v11 published 2026-09-18 [doc] (AUDIT L611).
- Grid working copy landed 2026-09-07 (LICENSE, fetch_from_tcia.py); labels dated 2026-09-16 [doc] (G0 §2).
- HOME `data/CTSpinoPelvic1K` mtime 2026-09-16 [listing] (LIST).
- 0533 rebuilt 2026-09-23 [doc] (AUDIT L1335).
- HF 0533 replaced 2026-09-23T18:08Z [doc] (mem:grid-ct-0533-truncated.md).

*[E]*

`~/data/CTSpinoPelvic1K` is dated 2026-09-16 in the listing. v11 labels 2026-09-18, v10 2026-09-07 (`DATA_COMPLETENESS_AUDIT.md` line 611). The repaired 0533 dates from 2026-09-23 (`mem:grid-ct-0533-truncated`).

**What it contains**

*[A]*

- 802 records, one per patient: 802 distinct tokens and 1,153 distinct SeriesInstanceUIDs across `spine_series_uid` and `pelvic_series_uid` (MANSUM).
- Manifest: 47 fields per record (AUDIT L901, L921; MANSUM). The HF-only `manifest.csv` has 51 columns (AUDIT L921).
- Record types: side spine 440 / fused 342 / pelvic 20; match_type separate 351 / fused 342 / spine_only 89 / pelvic_only 20 (MANSUM).
- Zenodo v11 has 10 files: labels.zip 883,912,953 B, manifest.json 1,100,037 B, splits_5fold.json, dataset_labels.json, fetch_from_tcia.py, reconstruct_ct.py, KNOWN_ISSUES.md, SHA256SUMS.txt, LICENSE, README (AUDIT L615).
- HF ct/ is 802 files, 192,813,331,872 B; HF labels/ is 802 files, 1,074,444,805 B, and they are v10 (AUDIT L617, L913).
- Grid `labels` (v11): 802 files, 1,189,127,569 B. Grid `labels_v10`: 802 files, 1,074,444,805 B (AUDIT L620-L621).
- `ct` is 225 GB by `du` (AUDIT L619); MDMR says 227 GB for the directory (MDMR L183).
- Demographics and scanners (MANSUM):
  - sex: female 393, male 345, other 11, null 53
  - age_band: 50-59 357, 60-69 230, 70-79 82, 80-89 40, null 93
  - manufacturer: Siemens 490, GE 223, Philips 30, Toshiba 25, null 34
  - slice thickness: 1.0 mm 562, 1.25 mm 232
  - kVp 120 on 799 records

*[E]*

802 `ct/` volumes (du 225G; sum 192,813,331,872 B), 802 v11 labels (1,189,127,569 B) and 802 `labels_v10/` (`DATA_COMPLETENESS_AUDIT.md` lines 619-621). The working copy is 227 GB (`MANIFEST_DATA_MODELS_RESULTS.md` 2.2).

**Where it is now**

*[A]*

- HOME `data/CTSpinoPelvic1K/`: `ct/` (802), `labels/` (v11), `labels_v10/`, manifest.json, splits_5fold.json, dataset_labels.json, KNOWN_ISSUES.md, README.md, fetch_from_tcia.py, reconstruct_ct.py, LICENSE (AUDIT L619-L622). These are converted, release-form files.
- The truncated original 0533 is kept at CEPH `data/ctsp0533_repair/0533_ct.TRUNCATED.20e673dc6c2a.nii.gz`, with the repair logs (AUDIT L1343-L1353; LIST 2026-09-23).
- Not on the grid: Windows `ctsp:data/zenodo_deposit/` (v10 staging; 802 labels carrying id 29, checked 2026-10-07 on 0007 and 0008; manifest.json md5 `baa77e93fd33ff27d3ffdebeff924c1f`, which is the v10 = v11 manifest md5 in AUDIT L920). Also `ctsp:data/hf_export_v5/` (ls of ctsp:data).
- `HOME/data/hf_export/ct`, the path in mem:grid-access.md, does not exist (AUDIT L623, L646, L930).

*[E]*

`~/anchor_drr` (HOME, converted/derived, 2.6 GB, listing 2026-09-23); `~/anchor_drr_c2` (HOME, converted/derived, 1.7 GB, listing 2026-09-23); `~/ctsp_drr` (HOME, converted/derived, listing 2026-09-22); `~/ctsp_drr_film` (HOME, converted/derived, listing 2026-09-17); `~/ctsp_patient_crosswalk.csv` (HOME, converted/derived, listing 2026-09-22); `~/ctsp_vid2patient.json` (HOME, converted/derived, listing 2026-09-22); `~/cut_physics` (HOME, converted/derived, listing 2026-09-15); `~/cut_physics_v2` (HOME, converted/derived, listing 2026-09-15); `~/cut_rare` (HOME, converted/derived, listing 2026-09-15); `~/cut_rare_v2` (HOME, converted/derived, listing 2026-09-15); `~/exp3_ctx_fluoro` (HOME, converted/derived, listing 2026-09-15); `~/exp3_ctx_radiograph` (HOME, converted/derived, listing 2026-09-15); `~/exp3_fluoro` (HOME, converted/derived, listing 2026-09-15); `~/exp3_radiograph` (HOME, converted/derived, listing 2026-09-15); `~/fluorogen` (HOME, converted/derived, listing 2026-09-17); `~/height_renders` (HOME, converted/derived, listing 2026-09-10); `~/implant_ct_smoke` (HOME, converted/derived, listing 2026-09-14); `~/implant_verse_smoke` (HOME, converted/derived, listing 2026-09-14); `~/lstv_eval` (HOME, converted/derived, listing 2026-09-15); `~/lstv_flag` (HOME, converted/derived, listing 2026-09-15); `~/ped_renders` (HOME, converted/derived, listing 2026-09-10); `~/physics_drr` (HOME, converted/derived, listing 2026-09-14); `~/physics_drr_film` (HOME, converted/derived, listing 2026-09-17); `~/physics_rare` (HOME, converted/derived, listing 2026-09-14); `~/physics_rare_film` (HOME, converted/derived, listing 2026-09-18); `~/physics_smoke` (HOME, converted/derived, listing 2026-09-14); `~/postop_render` (HOME, converted/derived, listing 2026-09-14); `~/postop_smoke` (HOME, converted/derived, listing 2026-09-14); `~/render_smoke` (HOME, converted/derived, listing 2026-09-15); `~/rib_fragments_release` (HOME, converted/derived, listing 2026-09-15); `~/rib_fragments_v4` (HOME, converted/derived, listing 2026-09-15); `~/sacrum_yolo` (HOME, converted/derived, listing 2026-09-18); `~/spinesurg-ct-nnunet` (HOME, converted/derived, 363 GB on 2026-09-19 per ssn:docs/CONTINUANCE_2026-09-19.md L27; the 1,433.6 GB of 2026-09-01 is superseded; listing 2026-09-25); `~/data/CTSpinoPelvic1K` (HOME, raw, 227.0 GB, listing 2026-09-16); `$RS/data/ctsp0533_repair` (CEPH, converted/derived, listing 2026-09-23); `$RS/data/d815_repair` (CEPH, converted/derived, listing 2026-09-23); `$RS/data/rare_class` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/spineps` (CEPH, converted/derived, listing 2026-09-23); `$RS/data/anomaly_harvest/ctsp` (CEPH, converted/derived, listing 2026-09-24); `~/spinesurg-ct-nnunet/nnunet/raw` (HOME, converted/derived)

**Annotation status**

*[A]*

- Release labels, VerSe-native ids:
  - C1-C7 1-7, T1-T12 8-19, L1-L6 20-25, sacrum 26 (29 retired in v11), hips 30/31, femurs 32/33
  - ribs 34-59, lumbar ribs 60/61, hardware 62-68 (DEP L243-L260)
- Vertebrae are expert (CTSpine1K radiologists). Pelvis is expert where fused and out-of-fold pseudolabel otherwise: `prov_spine` manual 782 / pseudo 20; `prov_pelvis` manual 362 / pseudo 440 (MANSUM).
- Ribs: model output (TotalSegmentator plus the Möller network), student-corrected in two-reviewer ledgers (169 rib, 113 spine, 106 triaged cases) (BUILD L42-L43).
- Castellvi: two-reader consensus on 33 records. Readers were two radiology residents, six disagreements resolved by consensus (DEP L215-L216; G0 §1). Fields `castellvi_type`, `castellvi_agreement` (MANSUM).
- Hardware: radiologist-read on 11 records (MANSUM `hardware_review` read 11).
- LSTV fields: `lstv_label` normal 769 / SACRALIZATION 17 / LUMBARIZATION 14 / SEMI 2; `has_l6` 18; `has_lumbar_rib` 16 (MANSUM).

*[E]*

release labels in scheme v10/v11 (`ctsp:CLAUDE.md`), plus LSTV phenotype fields in the manifest: 769 normal, 17 sacralization, 14 lumbarization and 2 semi-sacralization on v10 (`MANIFEST_DATA_MODELS_RESULTS.md` 2.2).

**Derived products**

*[A]*

- Render banks: `HOME/ctsp_drr` (A18), `physics_drr` (A19), `physics_rare` (A20), `anchor_drr` (A26), `anchor_drr_c2` (A27), `lstv_flag/renders` (A29); deleted `implant_ct` (A28).
- nnU-Net: Dataset810 (A15), Dataset813 (A16), Dataset815 (A17).
- `HOME/bench`: 44 GB harness; `ct_by_case` is 802 symlinks (MDMR L200-L202).
- CEPH `data/spineps/ctsp` and `data/spineps/bodies` (SPINEPS masks and vertebral-body masks) (ssn:docs/CINE_DEMO_RECON_2026-09-26.md and ssn:docs/DATA_COMPLETENESS_AUDIT.md reference these paths).
- CEPH `data/anomaly_harvest/ctsp` (LIST 2026-09-24).
- CEPH `data/rare_class/ctsp_drr` (ssn:SchwingNet/slurm/rare_ctsp_drr.sh).
- Patient-key split `HOME/patient_keys_final.json` and G3 split plan (ssn:SchwingNet/results/rare_class/split_plan.md).
- `HOME/ctsp_patient_crosswalk.csv` and `ctsp_vid2patient.json`, dated 2026-09-22 (LIST).

*[E]*

24 entries: `~/ablate`, `~/allspine_fov96_ctx`, `~/allspine_v6_fov96_ctx`, `~/allspine_v7_fov96_ctx`, `~/allspine_v7nofluoro_fov96_ctx`, `~/allspine_v8_fov96_ctx`, `~/allspine_v9_fov96_ctx`, `~/bench`, `~/ct_gzip_corrupt.txt`, `~/m_fov96_ctx`, `~/m_mask22_scale_ctx`, `~/merged_ctx`, `~/ostk_level_morphometry.csv`, `~/ostk_morph_out`, `~/ostk_run`, `~/ostk_shards`, `~/pi_ostk2.csv`, `~/qc.tar.gz`, `~/spinopelvic-seg`, `~/spinopelvic_all.csv`, `~/verse_ctx`, `$RS/neurips_tsv3`, `$RS/neurips_v11`, `~/spinesurg-ct-nnunet/nnunet/results`

*2026-10-08: `~/qc.tar.gz` (pelvis-propagation QC, 2026-06-12) and `~/s1v11` (the v11 build workspace), which the disk map gave to this source, are carded under `ctspinopelvic1k_build_tree` and move in batch B14.*

**Known defects and gaps**

*[A]*

- **0533.** The published CT was truncated: 17,301,504 B, sha256 `20e673dc…d6e23`. It was rebuilt to 250,067,995 B, sha256 `478a74e9…a164d5`, (512,577,512) PIR (KI §10; AUDIT L1345-L1353). The HF object was replaced 2026-09-23 (mem:grid-ct-0533-truncated.md). The KNOWN_ISSUES §10 note is not yet on Zenodo (mem:grid-ct-0533-truncated.md).
- **HF labels are still v10.** Id 29 is live on HF as of 2026-09-27; Zenodo is v11 (AUDIT L295-L298, L913; mem:hf-mirror-is-v10.md).
  - mem:hf-mirror-is-v10.md says v11 "exists only locally / on the grid".
  - AUDIT L615 (Zenodo API read) and CRC L332-L333 say Zenodo v11 is public.
  - The card follows the API read.
- **Wrong manifest column.** `manifest.n_voxels_fg` is 0 in 340 of 802 records, and 2,094,598 for 0533 against 3,167,246 in the mask (AUDIT L1368-L1373, L922; KI §10).
- **Undocumented measure.** `spine_bone_pct` is measured over vertebra ids only, and nothing says so (KI §10; AUDIT L1355-L1366).
- **`croissant.json` is listed in the README but exists in neither deposit** (AUDIT L647, L914).
- **Split key trap.** `splits_5fold.json` is keyed by TCIA token, not `volume_id`. 529 of 802 token ids collide with another record's volume_id (AUDIT L915, L926).
- **Three different "transitional" counts** in the release: 31 / 33 / 34 (AUDIT L923).
- **Token ≠ release id** (release 0145 = token 100) (mem:identity-audit-findings.md).

*[E]*

- CT 0533 was a truncated gzip until 2026-09-23 (`mem:grid-ct-0533-truncated`).
  - The HF mirror labels are v10 while Zenodo is v11 (`DATA_COMPLETENESS_AUDIT.md` line 295).
  - Dataset813's `imagesTr` entries are container-path links, and the label version behind it is unrecorded (`DATA_COMPLETENESS_AUDIT.md` line 140; `mem:dataset813-image-links-are-container-paths`).
  - `~/implant_ct` no longer exists (`DATA_COMPLETENESS_AUDIT.md` line 629).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): fresh tree under raw/CTSpinoPelvic1K_v11; dcm2niix from conda-forge; nifti-check on all 802; 0533 judged by tools/ctsp0533_verify.py, not by the cast file's sha256. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid ctspinopelvic1k` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[A]*

Run on a compute node, never the login node (ctsp:CLAUDE.md, Grid).

1. Labels and metadata:
   - `curl -s https://zenodo.org/api/records/22797014 > z.json`
   - For each `files[].key`: `curl -L -C - -o <key> "https://zenodo.org/records/22797014/files/<key>?download=1"`. The URL form is the one `ssn:slurm/carmlspine_fetch.sh` L16 uses.
   - Check each file against `files[].checksum` (md5) in z.json.
   - `unzip labels.zip && sha256sum -c SHA256SUMS.txt`. Expect 810 OK (AUDIT L620).
   - v10, if wanted: the same with record 22642578 (AUDIT L616).
2. CT, primary route:
   - `pip install tcia_utils nibabel scipy numpy` (dcm2niix on PATH)
   - `python fetch_from_tcia.py --manifest manifest.json --labels labels --out ct` (DEP L156-L159)
   - Verify: 802 files; `gzip -t` on every file; CT affine equals label affine; the tool's label-on-bone warning silent (≥ 50 %); 0533 sha256 `478a74e909956ff98df9fb5ccb4cced3671bf870935f4a29163d1ce9dfa164d5` (KI §10).
3. CT, alternative route:
   - `huggingface_hub.snapshot_download("OpenSpineConsortium/CTSpinoPelvic1K", repo_type="dataset", allow_patterns=["ct/*"])`
   - Verify each file's size and LFS sha256 against `https://huggingface.co/api/datasets/OpenSpineConsortium/CTSpinoPelvic1K/tree/main/ct`. Total should be 192,813,331,872 B (AUDIT L617).
   - Never take `labels/` from HF until v11 is pushed (AUDIT L295-L298).

*[E]*

- Labels: download Zenodo record 22797014 and run `sha256sum -c SHA256SUMS.txt`, which gave 810 OK and 0 failures on the grid copy (`DATA_COMPLETENESS_AUDIT.md` line 620).
  - CT: run the release's own `fetch_from_tcia.py` and `reconstruct_ct.py`, which ship in `~/data/CTSpinoPelvic1K` (`DATA_COMPLETENESS_AUDIT.md` line 622). Their arguments are not recorded in Family E's evidence.
  - Verify with `gzip -t` on all 802 CTs and with per-file sizes against `manifest.json`.

---

### `ctspinopelvic1k_april` <a id="ctspinopelvic1k_april"></a>

**CTSpinoPelvic1K April 2026 release (v1, 1,153 records over 802 patients).** Cards: A (A3 ctspinopelvic1k_april). Structured entry: `sources.yaml` id `ctspinopelvic1k_april`; kind project_release; status on_hf_only; re-acquisition manual (manual).

**Source id**

`ctspinopelvic1k_april`: the April 2026 release ("v1"; 1,153 records over 802 patients) that the NeurIPS paper's segmentation numbers were computed on (CRC L327-L339).

**Name and citation**

- CTSpinoPelvic1K, HuggingFace export finalized 2026-04-25; manifests redrawn 1 May (CRC L193, L327-L329).
- v1-v5 were HuggingFace-only, so "v1" has no DOI (CRC L351-L353).
- HF repos: `anonymous-neurips-ED/CTSpinoPelvic1K` (ctsp:README.md L400, L424, L453) and `gregoryschwingmdphd/CTSpinoPelvic1K`, which AUDIT L618 calls "1153-record era, not the release": 1,000 CT (240,820,488,070 B) and 1,000 labels, lastModified 2026-08-28 (after the April export). It is not the 1,153-record April state.

**Modality**

CT, same images as A2. Records are per acquisition, not per patient (CRC L327-L333).

**Position/view**

- Separate `spine_only` and `pelvic_native` records exist for patients whose two annotations lie on different prone/supine acquisitions (ctsp:README.md L286-L304).
- The per-record position table for this release is not recorded in any document read.

**Licence and access**

- Licence: CC BY-NC-SA 4.0 (ctsp:README.md L2).
- The anonymous repo's exact revision hash is not pinned down (CRC L350-L351).
- The April manifests and the evaluated split are not at any location the paper cites (CRC L411-L416).

**How it was acquired**

- Built by this project: `scripts/export_hf.py` and the v1/v2 ship jobs (BUILD L40; CRC L344).
- The grid copy that fed Dataset802/803 was `HOME/CTSpinoPelvic1K/data/hf_export` (ssn:slurm/convert_hf_to_nnet.sh L22-L26).
- Verification: not recorded.

**When**

- Export finalized 2026-04-25 [doc] (CRC L193); "finalize dataset" commit 8f1ed51, 2026-04-25 [git] (G0 §2).
- Manifests redrawn 1 May 2026; training began 3 May 2026 [doc] (CRC L327-L329).

**What it contains**

- 1,153 records across 802 patients: 342 fused, 351 separate-mode, 89 spine-only, 20 pelvic-only (CRC L51).
- Ten-class scheme: background, L1-L6, sacrum, left and right hip (CRC L329-L331).

**Where it is now**

- HOME `CTSpinoPelvic1K/data/hf_export` (328 GB on 2026-09-01, DUD) no longer exists as of 2026-09-23 (AUDIT L140-L143).
- CEPH `data/ctsp_april/` (mtime 2026-09-27, world-writable `drwxrwxrwx`) holds the SPINEPS benchmark run over the 1,153 records: jobs 40481323 → 40481314 → 40481315 (LIST; ctsp:CAMERA_READY_NEURIPS/src/appendix/spineps.tex L6-L8).
- Fetch job 40480758 fetched and sha-verified the inputs of all 1,153 records (2,306 of 2,306 files) for the SPINEPS run under `ctsp_april` (ssn:docs/RESUME_2026-09-22_PM.md L139). The exact subpath that holds them is not recorded until the census depth2.tsv shows it.
- HF copies listed above.

**Annotation status**

- Release labels: vertebrae from CTSpine1K, pelvis from CTPelvic1K.
- No Castellvi field in the April files (CRC L205).

**Derived products**

- Dataset802 and Dataset803 (A14).
- `HOME/XRSpinoPelvic1K/data/xrsp1k`, via `hf_export_v3` (A32).

**Known defects and gaps**

- Nine patients' CT and masks looked front-to-back reversed in render review (CRC L192).
- On 27 April, CTs that had skipped resampling were rewritten (CRC L193).
- The exact HF revision of the anonymous submission is unknown (CRC L350-L351).

**Re-acquisition recipe**

- manual: the source of record is the anonymous HF dataset repo `anonymous-neurips-ED/CTSpinoPelvic1K` (ctsp:README.md L400, L424, L453; CRC L348-L351). Its revision at submission is not pinned down (CRC L350-L351), and it needs Greg's account.
- Verify 1,153 records: 342 fused + 351 x 2 separate-mode + 89 spine-only + 20 pelvic-only (CRC L51).
- `gregoryschwingmdphd/CTSpinoPelvic1K` (1,000 CT, 1,000 labels, last modified 2026-08-28; AUDIT L618) is not this release; do not use it to reproduce the April numbers.
- Fallback: regenerate the April manifests from the build chain steps 1-4 (BUILD L37-L40), which needs A1, A5 and A6.

---

### `ctspinopelvic1k_build_tree` <a id="ctspinopelvic1k_build_tree"></a>

**CTSpinoPelvic1K build tree and build archive (Zenodo 22647933).** Cards: A (A4 ctspinopelvic1k_build_tree). Structured entry: `sources.yaml` id `ctspinopelvic1k_build_tree`; kind project_release; status on_disk_state_unknown; re-acquisition run (zenodo_http).

**Source id**

`ctspinopelvic1k_build_tree`: intermediate trees under `HOME/CTSpinoPelvic1K/data/`, and the build archive that replaces most of them (BUILD; DUD).

**Name and citation**

CTSpinoPelvic1K build archive, Zenodo 10.5281/zenodo.22647933, published 2026-09-07: 13 files, 6.24 GB, verified by size and md5 with `zenodo/check_draft.py` (mem:zenodo-deposit.md; BUILD L1-L16).

**Modality**

Label volumes, placement masks, manifests and review ledgers (BUILD L55-L71).

**Position/view**

As A2.

**Licence and access**

Open on Zenodo. Licence not recorded in BUILD; the deposit is CC BY-NC-SA 4.0 (DEP L363).

**How it was acquired**

- Produced by this project's pipeline steps 1-13 (BUILD L30-L49).
- The archive components were assembled by `ctsp:slurm/archive_build_inputs.sh`, which reads Zenodo v10 files from `https://zenodo.org/api/records/22642578/files` (ctsp:slurm/archive_build_inputs.sh L39).

**When**

- Folders dated by `du` on 2026-09-01 [du] (DUD).
- Build archive published 2026-09-07 [doc] (mem:zenodo-deposit.md).
- RECLAIM phases A and B were written 2026-09-07 [git] (`git log ctsp:slurm/reclaim_grid_space.sh`) and "ran the same day" [doc] (mem:zenodo-deposit.md).

- Identified on the grid on 2026-10-08 (scr:inspect_unknown.out): `~/qc.tar.gz` dated 2026-06-12; `~/pitest` 2026-09-10 11:38 and `~/pdwtest` 2026-09-10 16:09; `~/s1v11` 2026-09-11..2026-09-18, with labels.zip stored on Zenodo on 2026-09-18 22:46 (its `upload_zip.log`).

**What it contains**

- On 2026-09-01 (DUD): hf_export 328G, hf_export_osc 227G, placed 6.1G, hf_export_v6 4.6G, hf_export_v5 4.6G, hf_export_v4 2.8G, hf_export_v3 2.4G, zenodo_v6 2.3G, v5_final 2.3G, zenodo_upload 2.2G, hf_export_v2 2.1G, s1_recarve 1.6G, plus hardware_*, fix_0816*, hip_* backups.
- Archive components (BUILD L55-L71):
  - 01_sources: CTSpine1K COLONOG labels and CTPelvic1K dataset-2 masks, ~0.8 GB
  - 02_placement, ~4.5 GB
  - 03_v4_base, ~1.9 GB
  - 04_reviews, ~0.5 GB
  - 05_v5, ~1.9 GB
  - 06_v6_inputs, ~0.4 GB
  - 07_v7, ~1.3 GB
  - 08 grid worktree
  - 09 nnU-Net meta

- Identified on 2026-10-08 (scr:inspect_unknown.out):
  - `~/s1v11`, the v11 build workspace: `scripts/` (`merge_s1_into_sacrum.py`, `audit_s1_carve.py`, `check_s1_merge.py`, `extract_surgical_morphometrics.py`, `compare_v10_v11_spinopelvic.py`; copies of the ctsp:scripts/ files of those names), the logs of jobs 40198228 (s1_v11), 40198880 (v11_morph), 40309073 (verify_v11) and 40309160 (package_v11), `out/v11_labels` (389 `.gz` among the first 400 files listed), `out/s1_carve_audit.csv`, `morphometrics/surgical_morphometrics.csv`, `out/dataset_labels_v11.json` ("CTSpinoPelvic1K v11 (VerSe-native, contiguous 0-68); S1 (29) retired"), `zenodo_v11.py` and its state, `deposit_files.txt`, `package_v11.sh`, `upload_zip.sh` and `upload_zip.log` (labels.zip 883,912,953 B, HTTP 201, md5 744281a5f824494123396386cfe940b8), `zenodo_sync.log`, `verify_v11.py` and its log.
  - `~/pitest`: ten label files (0024, 0182, 0375, 0401, 0569, 0624, 0760, 1043, 1084, 1129), 13,899,387 B; `~/pdwtest`: two (0010, 0038), 2,710,749 B. Scratch copies from the 2026-09-10 spinopelvic work (`~/pi_ostk2.csv` and `~/spinopelvic_all.csv` share the date); the names suggest a pelvic-incidence test and a second measurement test, and no file says.
  - `~/qc.tar.gz`, 196,147,947 B: pelvis-propagation QC PNGs. By the grid reading its members are named like `qc/34_1.3.6.1.4.1.9328.50.4.35354_propagation.png`, the `{token}_{series UID}_propagation.png` that ctsp:scripts/viz_propagation.py L122 writes (first committed 2026-06-12, the archive's date). It is not the speckle QC (`qc_speckle/`, ctsp:slurm/finalize_v5.sh).

**Where it is now**

- RECLAIM phase A deletes ctspine1k, ctpelvic1k, hf_export_v2_work, hf_export_v3_work, hf_export_v4, hf_export_v5, hf_export_osc, zenodo_v6, zenodo_upload (RECLAIM L34-L40).
- Phase B deletes placed, v5_final, v5_smoke, s1_recarve, hardware_*, fix_0816*, hip_* backups, thoracic_fix, hf_export_v6, zenodo_v7 (RECLAIM L41-L47).
- Not on either list: tcia, tcia_nifti, hf_export, hf_export_v2, hf_export_v3, patient_db.* (RECLAIM L34-L47).
- `hf_export` and `hf_export_v3` were gone by 2026-09-23 (AUDIT L140-L143; MDMR L197-L200).
- The state of `hf_export_v2` and `patient_db.*` after 2026-09-01 is not recorded. G0 §2 implies `patient_db.json` still exists.
- All HOME.

- Identified on 2026-10-08 (scr:inspect_unknown.out) and moving in batch B14 (MIGRATION_PLAN.md section 5): `~/s1v11` to `derived/s1v11` (irreplaceable; owner-only until its upload scripts are read for a token), `~/pitest` and `~/pdwtest` to `derived/scratch_2026-09-10/` (deletion candidates), `~/qc.tar.gz` to `derived/qc_2026-06-12.tar.gz`. All HOME today.

**Annotation status**

Mixed: source labels, model outputs, student review ledgers, radiologist reads (BUILD L8-L16).

**Derived products**

Every release version v1-v11 (BUILD L30-L49; DEP L342-L354).

**Known defects and gaps**

- `CHAIN_CHECK_v7_to_v10.txt` states how many of 802 volumes regenerate voxel-identically (BUILD L51-L53). Memory says all 802 (mem:zenodo-deposit.md).
- The v11 step (29 dissolved into 26, `scripts/merge_s1_into_sacrum.py`, 2026-09-11 [git]) is not in BUILD's chain table, which ends at v10 (BUILD L49).

- The v11 step's workspace is `~/s1v11` (identified 2026-10-08). Its `verify_v11.log` (2026-09-16) first reports 802 files with the same names in the v10 and v11 trees, then cannot open `~/data/CTSpinoPelvic1K/labels/0130_label.nii.gz`: the working copy changed while the check ran, or the listing and the load read different paths; which, and whether the comparison was rerun, is not recorded (scr:inspect_unknown.out).
- Its `zenodo_sync.log` shows the first labels.zip upload failing (502, then 400); `upload_zip.sh` stored it on the next attempt with the expected size (scr:inspect_unknown.out).
- Whether `~/s1v11/out/v11_labels`, `~/pitest` or `~/pdwtest` share inodes with `~/data/CTSpinoPelvic1K/labels` is not recorded; the preflight shows it (MIGRATION_PLAN.md section 5, B14).

**Re-acquisition recipe**

- `curl -s https://zenodo.org/api/records/22647933` → download the 13 files → verify md5 from the API, as `zenodo/check_draft.py` did (mem:zenodo-deposit.md).
- Unpack the `.tar.zst` components.
- Rerun steps 12-13 and `scripts/merge_s1_into_sacrum.py` to reach v11 (BUILD L48-L49; `git log ctsp:scripts/merge_s1_into_sacrum.py`).

---

### `ctspine1k` <a id="ctspine1k"></a>

**CTSpine1K.** Cards: A (A5 ctspine1k), B (CTSpine1K non-colonography volumes (MSD-T10 150, COVID-19 40, HNSCC 31)), E (ctspine1k). Also known as: `hf_ctspine1k_noncolonog`. Structured entry: `sources.yaml` id `ctspine1k`; kind upstream_release; status on_disk; re-acquisition run (other_ct_fetch).

**Source id**

*[A]*

`ctspine1k`: CTSpine1K, the vertebral annotations of CTSpinoPelvic1K. It also appears in the other-CT stream for its 223 non-CTSP volumes (OCT "Denominators").

*[B: card `hf_ctspine1k_noncolonog`]*

`hf_ctspine1k_noncolonog` (acquisition/ranking.csv collection `hf:ctspine1k_noncolonog`)

*[E]*

`ctspine1k` (family A's id)

**Name and citation**

*[A]*

- Deng Y, Wang C, Hui Y, et al. "CTSpine1K: A Large-Scale Dataset for Spinal Vertebrae Segmentation in Computed Tomography", MELBA 3 (2021/2025) 824-832, doi 10.59275/j.melba.2025-gf84, arXiv 2105.14711 (ctsp:README.md L473-L488).
- Release: GitHub MIRACLE-Center/CTSpine1K (mem:ctspine1k-selection-code-deleted.md).
- HF mirror `alexanderdann/CTSpine1K` (ssn:tools/other_ct_fetch.py L6-L9).

*[B: card `hf_ctspine1k_noncolonog`]*

CTSpine1K non-colonography volumes (MSD-T10 150, COVID-19 40, HNSCC 31); HF tree 2026-09-23: 2,018 files, 162 GB (acquisition/ranking.csv)

*[E]*

CTSpine1K, Hugging Face mirror alexanderdann/CTSpine1K: 1,005 volumes with expert vertebra labels from four sources (COLONOG 784, MSD-T10 150, COVID-19 40, HNSCC-3DCT-RT 31) (`nnunet:tools/other_ct_fetch.py` header).

**Modality**

*[A]*

CT. Sources: COLONOG (abdominopelvic), MSD-T10 (abdomen; per the paper text Task03 Liver), COVID-19 (chest), HNSCC-3DCT-RT (neck) (ssn:tools/other_ct_fetch.py L6-L9; mem:ctspine1k-selection-code-deleted.md).

*[B: card `hf_ctspine1k_noncolonog`]*

CT, coverage CHEST_SCREEN:40 (acquisition/ranking.csv)

*[E]*

CT.

**Position/view**

*[A]*

- For COLONOG one of the two acquisitions was kept. The kept volume was an unrecorded side effect of `os.walk` order in the deleted `dicom2nii.py`, not a random choice (mem:ctspine1k-selection-code-deleted.md).
- Per-volume position: not recorded.

*[B: card `hf_ctspine1k_noncolonog`]*

not recorded (acquisition/ranking.csv)

*[E]*

not recorded.

**Licence and access**

*[A]*

- CC BY-NC-SA 4.0 (ctsp:README.md L511-L514; ssn:tools/acquisition_census.py L396).
- HF access is recorded as gated in April (the ctsp:slurm/download_raw.sh header in the first commit 550cfff, 2026-04-18, and still at L41; BUILD L23) and as "ungated" on 2026-09-23 (ssn:tools/acquisition_census.py L396).

*[B: card `hf_ctspine1k_noncolonog`]*

open, CC BY-NC-SA 4.0; derived labels yes (acquisition/ranking.csv)

*[E]*

an HF gated dataset that needs `HF_TOKEN` (`ctsp:slurm/download_raw.sh` header). The licence text is not recorded in Family E's evidence.

**How it was acquired**

*[A]*

- **HOME copy, by 2026-04-25.** `ctsp:slurm/download_raw.sh` stage 2/3: `huggingface_hub.snapshot_download("alexanderdann/CTSpine1K", repo_type="dataset", ignore_patterns=["*.arrow","*.parquet"], max_workers=4)` with HF_TOKEN and up to 20 retries (ctsp:slurm/download_raw.sh L156-L235). Verification: ≥ 1,500 `.nii.gz` files, which is a count only (ctsp:slurm/download_raw.sh L186).
- **CEPH copy, 2026-09.** `sbatch -D CEPH/tmp -J oct_ctspine1k ssn:slurm/other_ct_fetch.sh ctspine1k` runs `ssn:tools/other_ct_fetch.py ctspine1k --out CEPH/data/ctspine1k --workers 8` (ssn:slurm/other_ct_fetch.sh L3-L21).
  - It reads the HF API listing with `blobs=true` and downloads each file pinned to the listing's revision sha.
  - It verifies byte size and LFS sha256 per file, deleting and retrying failures.
  - It writes `hf_listing.json` and `fetch_status.json` (ssn:tools/other_ct_fetch.py L87-L112).

*[B: card `hf_ctspine1k_noncolonog`]*

not by this chain; the whole release was fetched by the other_ct stream from Hugging Face `alexanderdann/CTSpine1K` with `tools/other_ct_fetch.py ctspine1k` (byte size and LFS sha256 per file) (tools/other_ct_fetch.py)

*[E]*

- On HOME: `SPINE_ONLY=1 sbatch slurm/download_raw.sh`, COLONOG fold only (`ctsp:data/README.md`).
  - On Ceph: `python tools/other_ct_fetch.py ctspine1k --out $RS/data/ctspine1k --workers 8`, checking each file against the listing's byte size and LFS sha256 (`nnunet:tools/other_ct_fetch.py`).

**When**

*[A]*

- HOME copy: by 2026-04-25 (upper bound). Stage 2/3 of `ctsp:slurm/download_raw.sh` is in the first commit 550cfff (2026-04-18) [git], and the April export (finalized 2026-04-25) fused CTSpine1K vertebral masks with CTPelvic1K pelvic masks (CRC L51, L247, L329-L331) [doc]. The exact download day is not recorded. The 2026-05-16 commit 1080b1c ("use token", `git log ctsp:slurm/download_raw.sh`) adds token passing and may mark a re-run; its message is the only evidence. Present on 2026-09-01 [du] (DUD).
- CEPH copy: directory mtime 2026-09-23 [listing] (LIST). HF tree read 2026-09-23 [doc] (ssn:tools/acquisition_census.py L399). Tool committed 2026-09-24 [git].

*[B: card `hf_ctspine1k_noncolonog`]*

assessed in the 2026-09-23 census (acquisition/ranking.csv)

*[E]*

`other_ct_fetch.py` was first committed 2026-09-24 (git log). The Ceph folder is dated 2026-09-23 in the listing, so it may have been created by an earlier route (not recorded).

**What it contains**

*[A]*

- 1,005 volumes with expert vertebra labels: COLONOG 784, MSD-T10 150, COVID-19 40, HNSCC-3DCT-RT 31 (ssn:tools/other_ct_fetch.py L6-L9; OCT "Denominators").
- HF tree on 2026-09-23: 2,018 files, 162 GB (ssn:tools/acquisition_census.py L399).
- The paper's per-source counts (825 + 201 + 40 + 31 = 1,097) do not sum to its stated 1,005 (mem:ctspine1k-selection-code-deleted.md).
- Crosswalk: 784 COLONOG, of which 782 are CTSP persons and 2 are not (OCT "Denominators").

*[B: card `hf_ctspine1k_noncolonog`]*

221 listed, 40 qualifying, 40 new; 26.3 GB all CT (acquisition/ranking.csv)

*[E]*

152 GB on Ceph (`CENSUS_TABLE_2026-09-25.md` 4). The HOME copy measured 190G on 2026-09-01 (`_du_data.txt`), although the download script header says "~4 GB, 784 NIfTI segs".

**Where it is now**

*[A]*

- HOME `CTSpinoPelvic1K/data/ctspine1k`: 190 GB on 2026-09-01 (DUD). It is on RECLAIM phase A (RECLAIM L35), which "ran" on 2026-09-07 (mem:zenodo-deposit.md), so it is presumed deleted. To be confirmed by the census.
- CEPH `data/ctspine1k/` (raw HF layout, `rawdata/volumes/<source>/*.nii.gz` and `rawdata/labels/<source>/*_seg.nii.gz` per ctsp:data/README.md L20-L23): 152 GB (CENSUS25 §4); 1,005 volumes (OCT).
- Labels-only copy of the COLONOG fold in the build archive 01_sources (BUILD L59).

*[B: card `hf_ctspine1k_noncolonog`]*

fetched in full by the other_ct stream, not by this chain: CEPH `/rs/rs_grp_oschome/go2432/data/ctspine1k/raw_data/{volumes,labels}` (1,005 volumes; 223 non-CTSP screened) (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md; listing; tools/other_ct_fetch.py); also `CTSpinoPelvic1K/data/ctspine1k` on HOME (190 GB on 2026-09-01) (scratchpad census/_du_data.txt)

*[E]*

`~/CTSpinoPelvic1K` (HOME, raw, 1,945.6 GB, listing 2026-09-13); `$RS/data/ctspine1k` (CEPH, raw, 152.0 GB, listing 2026-09-23); `~/CTSpinoPelvic1K/data/ctspine1k` (HOME, raw, 190.0 GB)

**Annotation status**

*[A]*

- Expert: VerSe-convention vertebra masks C1-L6 and sacrum, with T13 = 28 (ctsp:README.md L94-L104).
- Release LSTV lists in the CTSpine1K README, for example liver_106 "Sacral Lumbarization" (OCT "The thirteen positive rows").
- Project corrections in `ctsp:docs/ctspine1k_corrections.csv` (file present in ctsp:docs).

*[B: card `hf_ctspine1k_noncolonog`]*

CTSpine1K release vertebra annotation (VerSe-like ids, no sacrum id); README expert lists give read-tier L6 1 and sacralised L5 2; other_ct stream pseudo-labels (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); belongs to the other-CT family; tiers: 223 CTs, tier 1 20, tier 2 196 (docs/ruleclass/TIERS.md)

*[E]*

release expert vertebra labels.

**Derived products**

*[A]*

- CTSP vertebrae (A2).
- Other-CT screen rows for the 223 non-CTSP volumes (OCT).
- CEPH `data/anomaly_harvest/other_ct` (OCT header).

*[B: card `hf_ctspine1k_noncolonog`]*

other_ct stream rows under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/` (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md)

*[E]*

CTSpinoPelvic1K spine masks (`ctsp:data/README.md`). none found in the disk map

**Known defects and gaps**

*[A]*

- The supine/prone "random selection" claim is false. The selection code was deleted (commit bcd8f47, 2021-06-11) and is recoverable at 7f44959 (mem:ctspine1k-selection-code-deleted.md).
- Its "MSD T10" label versus its Task03 text (mem:ctspine1k-selection-code-deleted.md).

*[B: card `hf_ctspine1k_noncolonog`]*

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: COLONOG 784 = CTSpinoPelvic1K people (their vertebra labels are a SECOND LABELLER for CTSP, not new people); MSD-T10 150 = inside AbdomenAtlas MSD-CT; HNSCC 31 are neck fields (no count); 40 COVID chest new (acquisition/ranking.csv)

*[E]*

- The HOME copy is on the phase A delete list (`ctsp:slurm/reclaim_grid_space.sh`), so whether it still exists is unknown.
  - The supine/prone selection code was deleted (`mem:ctspine1k-selection-code-deleted`).

**Re-acquisition recipe**

*[A]*

- `sbatch -D CEPH/tmp -J oct_ctspine1k <ssn checkout>/slurm/other_ct_fetch.sh ctspine1k` (ssn:slurm/other_ct_fetch.sh L3).
- Verify: `fetch_status.json` has `failed: {}`; n equals the listing's file count (2,018 on 2026-09-23); per-file LFS sha256 (built in).
- Record the listing revision sha.
- If the repo is gated again, accept the terms on HF and pass a token.

*[B: card `hf_ctspine1k_noncolonog`]*

`python tools/other_ct_fetch.py ctspine1k --out /rs/rs_grp_oschome/go2432/data/ctspine1k --workers 8` (byte size + LFS sha256 per file) (tools/other_ct_fetch.py)

*[E]*

`sbatch slurm/other_ct_fetch.sh` in mode `ctspine1k`, which calls `tools/other_ct_fetch.py ctspine1k` (`nnunet:slurm/other_ct_fetch.sh`). It verifies size and LFS sha256 per file.

---

### `ctpelvic1k` <a id="ctpelvic1k"></a>

**CTPelvic1K (datasets 1-7; datasets 6-7 also fetched as ctpelvic1k_clinic).** Cards: A (A6 ctpelvic1k), B (CTPelvic1K datasets 6-7 (clinical pelvic CT)), E (ctpelvic1k), E (ctpelvic1k_clinic). Also known as: `ctpelvic1k_clinic`. Structured entry: `sources.yaml` id `ctpelvic1k`; kind upstream_release; status on_disk; re-acquisition run (zenodo_http).

**Source id**

*[A]*

`ctpelvic1k`: CTPelvic1K, the sacrum and hip annotations of CTSpinoPelvic1K. Datasets 6-7 also appear as `ctpelvic1k_clinic` in the acquisition stream (CENSUS25 §1).

*[B: card `ctpelvic1k_clinic`]*

`ctpelvic1k_clinic` (acquisition/ranking.csv collection `zenodo:ctpelvic1k_clinic`; slurm/acquisition_submit.sh)

*[E]*

`ctpelvic1k` (family A's id)

*[E: card `ctpelvic1k_clinic`]*

`ctpelvic1k_clinic`

**Name and citation**

*[A]*

- Liu P, Han H, Du Y, et al. "Deep Learning to Segment Pelvic Bones: Large-Scale CT Datasets and Baseline Models", IJCARS 16:749-756, 2021 (ctsp:README.md L490-L500).
- Zenodo record 4588403 (ctsp:README.md L515; ctsp:slurm/download_raw.sh L252).

*[B: card `ctpelvic1k_clinic`]*

CTPelvic1K, datasets 6 and 7 only; release page zenodo.org/records/4588403 (publication date not in the sweep) (acquisition/ranking.csv; acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

CTPelvic1K, dataset2 masks (`ctsp:data/README.md`).

*[E: card `ctpelvic1k_clinic`]*

CTPelvic1K clinical datasets 6-7, Zenodo 4588403 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[A]*

CT, pelvis. Datasets 1-5 are masks for BTCV, COLONOG, MSD-T10, KiTS19 and cervix CTs; datasets 6-7 are CLINIC and CLINIC-metal images (ACQ L293-L294; ctsp:slurm/download_raw.sh L272-L285).

*[B: card `ctpelvic1k_clinic`]*

clinical pelvic CT (class PELVIS; the rib reference is rarely in view) (acquisition/ranking.csv)

*[E]*

CT, pelvis.

*[E: card `ctpelvic1k_clinic`]*

CT, pelvis (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[A]*

Not recorded.

*[B: card `ctpelvic1k_clinic`]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded.

*[E: card `ctpelvic1k_clinic`]*

not recorded

**Licence and access**

*[A]*

- Open. CC BY 4.0 (ctsp:README.md L515; ssn:tools/acquisition_census.py L400-L401).
- `ctsp:docs/DATASETS_ROADMAP.md` L95 calls it NC. These disagree.

*[B: card `ctpelvic1k_clinic`]*

open, CC BY 4.0 (acquisition/ranking.csv)

*[E]*

Zenodo archives (`ctsp:slurm/download_raw.sh` header). The licence is not recorded here.

*[E: card `ctpelvic1k_clinic`]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[A]*

- **HOME, 2026-04/05.** `ctsp:slurm/download_raw.sh` stage 3/3 uses `wget --continue` from `https://zenodo.org/record/4588403/files/CTPelvic1K_dataset{1..5}_mask_mappingback.tar.gz?download=1` and `CTPelvic1K_dataset{6,7}_data.tar.gz`, then extracts with tar (ctsp:slurm/download_raw.sh L238-L310). Verification: none (no checksum, count printed only).
- **CEPH, 2026-09.** `ssn:slurm/acquisition_submit.sh` L92-L93: `chain ctpelvic1k_clinic … zenodo --collection ctpelvic1k_clinic --record 4588403 --include 'dataset[67]_data\.tar\.gz$'`.

*[B: card `ctpelvic1k_clinic`]*

`acquisition_fetch.py zenodo --collection ctpelvic1k_clinic --record 4588403 --include 'dataset[67]_data\.tar\.gz$'`, md5; convert excludes `mask|label|seg` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py)

*[E]*

`PELVIC_ONLY=1 sbatch slurm/download_raw.sh` (`ctsp:slurm/download_raw.sh`).

*[E: card `ctpelvic1k_clinic`]*

`python tools/acquisition_fetch.py zenodo --collection ctpelvic1k_clinic --record 4588403 --include 'dataset[67]_data\.tar\.gz$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[A]*

- HOME: by 2026-04-25 (upper bound). Stage 3/3 of `ctsp:slurm/download_raw.sh` is in the first commit 550cfff (2026-04-18) [git], and the April export (finalized 2026-04-25) fused CTPelvic1K pelvic masks with CTSpine1K vertebral masks (CRC L51, L247, L329-L331) [doc]. The exact day is not recorded; present on 2026-09-01 [du] (DUD).
- CEPH `data/ctpelvic1k_clinic` mtime 2026-09-23 [listing] (LIST).

*[B: card `ctpelvic1k_clinic`]*

fetch 40426194 submitted 2026-09-23, 2/2 units by about 21:25 EDT; screen finished by 07:10 EDT 2026-09-24 (acquisition/jobs.txt); CEPH `data/ctpelvic1k_clinic` dated 2026-09-23 (listing)

*[E]*

not recorded. The script dates from 2026-04-18 (git log).

*[E: card `ctpelvic1k_clinic`]*

`$RS/data/ctpelvic1k_clinic` is dated 2026-09-23 in the listing; Slurm job fetch 40426194 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[A]*

- HOME copy: 36 GB (DUD).
- CEPH datasets 6-7: 178 listed, 173 CTs on disk, 14 GB raw (CENSUS25 §1). 172 converted and usable; 6 refused as duplicate voxels (ssn:SchwingNet/results/transitional_registry/acquisition/collections/ctpelvic1k_clinic/SUMMARY.md).
- CTSP used dataset 2 (COLONOG): sacrum 1 → 26, left hip 2 → 30, right hip 3 → 31 (ctsp:README.md L102-L107).

*[B: card `ctpelvic1k_clinic`]*

178 listed, 14.8 GB (acquisition/ranking.csv); 2 archives verified, 172 CTs usable, 6 refused as voxel duplicates (3 of the `_metal_` series) (acquisition/collections/ctpelvic1k_clinic/SUMMARY.md); du 14 GB raw, 5 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

`masks/CTPelvic1K_dataset2_mask_mappingback/dataset2_*.nii.gz` (`ctsp:data/README.md`). du was 36G on 2026-09-01 (`_du_data.txt`).

*[E: card `ctpelvic1k_clinic`]*

173 of 178 listed CTs on disk; 14 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/ctpelvic1k_clinic/fetch/verified.jsonl` (docstring)

**Where it is now**

*[A]*

- HOME `CTSpinoPelvic1K/data/ctpelvic1k`: on RECLAIM phase A (RECLAIM L35), presumed deleted 2026-09-07 (mem:zenodo-deposit.md).
- CEPH `data/ctpelvic1k_clinic` (raw) and CEPH `data/anomaly_harvest/ctpelvic1k_clinic` (screen) (LIST).
- Dataset-2 masks in build archive 01_sources (BUILD L59).

*[B: card `ctpelvic1k_clinic`]*

CEPH `/rs/rs_grp_oschome/go2432/data/ctpelvic1k_clinic/raw/4588403/...`, screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/ctpelvic1k_clinic/` (listing; tools/acquisition_screen.py); a folder `CTSpinoPelvic1K/data/ctpelvic1k` (36 GB on 2026-09-01) exists on HOME; whether it holds datasets 6-7 is not recorded (scratchpad census/_du_data.txt)

*[E]*

`~/CTSpinoPelvic1K` (HOME, raw, 1,945.6 GB, listing 2026-09-13); `~/CTSpinoPelvic1K/data/ctpelvic1k` (HOME, raw, 36.0 GB)

*[E: card `ctpelvic1k_clinic`]*

`$RS/data/ctpelvic1k_clinic` (CEPH, raw, 14.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/ctpelvic1k_clinic` (CEPH, converted/derived, 5.0 GB, listing 2026-09-24)

**Annotation status**

*[A]*

Expert, radiologist-supervised pelvic masks for datasets 1-5 (DEP L358-L361). Datasets 6-7 as fetched carry no project annotation (collections SUMMARY: "no radiologist read exists").

*[B: card `ctpelvic1k_clinic`]*

files matching `mask|label|seg` are excluded at convert (slurm/acquisition_submit.sh); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); 171 no_count, 1 unassigned (acquisition/collections/ctpelvic1k_clinic/SUMMARY.md)

*[E]*

release pelvic masks.

*[E: card `ctpelvic1k_clinic`]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 5 GB under `$RS/data/anomaly_harvest/ctpelvic1k_clinic` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[A]*

- CTSP pelvis (A2).
- Two-labeller screen rows (collections SUMMARY).

*[B: card `ctpelvic1k_clinic`]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/ctpelvic1k_clinic/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); copies `acquisition/collections/ctpelvic1k_clinic/`; tiers: 172 CTs, tier 1 1, tier 2 5, untiered 166, 32 PENGWIN CTs folded onto these by pixel sha1, alias candidates 34 (docs/ruleclass/TIERS.md)

*[E]*

CTSpinoPelvic1K pelvic masks. none found in the disk map

*[E: card `ctpelvic1k_clinic`]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[A]*

- Licence wording conflict, as above.
- Datasets 1-5 add no new people: they are CTSP or AbdomenAtlas people (ACQ L293-L294).

*[B: card `ctpelvic1k_clinic`]*

pelvic fields: 6 of 172 through the gate (acquisition/collections/ctpelvic1k_clinic/SUMMARY.md); CTPelvic1K datasets 1-5 are CTSP or AbdomenAtlas people and were not fetched here (they belong to other families) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 5)

*[E]*

the HOME copy is on the phase A delete list (`ctsp:slurm/reclaim_grid_space.sh`).

*[E: card `ctpelvic1k_clinic`]*

the FOV gate passes 7 (`CENSUS_TABLE_2026-09-25.md` 1)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): include regex tightened to masks 1-5 and data 6-7; every tar member read. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid ctpelvic1k` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[A]*

- `PELVIC_ONLY=1 FORCE=1 sbatch -D <CTSpinoPelvic1K checkout> slurm/download_raw.sh` (ctsp:slurm/download_raw.sh L25-L27).
- Add an md5 check against `https://zenodo.org/api/records/4588403` `files[].checksum`, because the script verifies nothing.
- Clinical sets only: the acquisition chain line above.

*[B: card `ctpelvic1k_clinic`]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_ctpelvic1k_clinic ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection ctpelvic1k_clinic --record 4588403 --include 'dataset[67]_data\.tar\.gz$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); must verify 2 archives by md5 and 178 CTs

*[E]*

`PELVIC_ONLY=1 sbatch slurm/download_raw.sh`. The script writes a `.download_complete` marker but records no checksum.

*[E: card `ctpelvic1k_clinic`]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` (block `tier1`), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `verse19_20` <a id="verse19_20"></a>

**VerSe'19 and VerSe'20 (OSF download).** Cards: A (A7 verse19_20). Structured entry: `sources.yaml` id `verse19_20`; kind upstream_release; status on_disk; re-acquisition submit (osf_verse).

**Source id**

`verse19_20`: VerSe'19 and VerSe'20, as downloaded from OSF (AUDIT L652-L697).

**Name and citation**

- Sekuboyina et al. 2021, Medical Image Analysis (arXiv 2001.09193).
- Löffler/Liebl et al. 2021, Scientific Data 8:284 (arXiv 2103.06360) (AUDIT L652-L660, L932).
- Release: https://github.com/anjany/verse (AUDIT L658).
- OSF nodes: 923ap (VerSe'19 MICCAI), b2wxj (VerSe'20 MICCAI), jtfa5 (VerSe'19 BIDS), 4skx2 (VerSe'20 BIDS) (vfr:src/verse_pipeline/download.py L67-L77).

**Modality**

Multi-detector CT, whole spine or partial (cervical, thoracolumbar, lumbar per scan) (mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md: "gl003 is C1-T5, verse500 is T10-L5").

**Position/view**

Not recorded.

**Licence and access**

- Open. CC BY 4.0 per vfr:README.md L348-L350.
- CC BY-SA 4.0 per mem:lstv-data-landscape.md and ctsp:docs/DATASETS_ROADMAP.md L95. These disagree.
- The variant supplement (Suppl. Table 1) is CC BY 4.0 (mem:versefusion-t13-flag-wrong.md).

**How it was acquired**

- VerSeFusion `make download-slurm`, which runs `python -m verse_pipeline.download --out_dir data/raw --workers N` (vfr:README.md L38-L46; vfr:src/verse_pipeline/download.py L31-L34).
- It walks the MICCAI nodes with throttled OSF API listing and falls back to the BIDS nodes for series absent from both MICCAI nodes, auto-discovered against `configs/verse_demographics.csv` (vfr:src/verse_pipeline/download.py L1-L35).
- Route: OSF HTTP API.
- Verification: size match ("files already present at expected size are counted as cached"); `download_manifest.json` reports n_files 1,897, downloaded 1,871, cached 26, failed 0 (vfr:src/verse_pipeline/download.py L27; AUDIT L938).

**When**

- `HOME/VerSeFusion/data/raw` ctime 2026-05-12 18:16 [doc] (G0 §2).
- Download tool commits 2026-05-11 to 2026-05-12 [git] (`git log vfr:src/verse_pipeline/download.py`).

**What it contains**

- VerSe'19: 160 series / 141 subjects. VerSe'20: 319 series / 300 subjects.
- Union: 374 scans / 355 patients / 4,505 vertebrae (AUDIT L656-L658).
- Per scan: CT, vertebra mask, centroid json, preview png (AUDIT L659).
- On disk: VerSe'19 160 CT / 159 seg / 159 ctd; VerSe'20 303 CT + 6 BIDS = 309 of 319 (AUDIT L663, L938).
- `data/raw` is 71 GB (AUDIT L662).

**Where it is now**

- HOME `VerSeFusion/data/raw/{verse19,verse20}`, raw (AUDIT L662-L663).
- HOME `VerSeFusion.tar.gz` (2026-05-11) and a file `VerseFusion` (2026-05-14), contents not recorded (LIST).

**Annotation status**

- Expert vertebra masks with VerSe ids: C1-C7 1-7, T1-T12 8-19, L1-L6 20-25, T13 28. The sacrum is never segmented, and neither are partially fused LSTVs (AUDIT L660-L661).
- Masks carry L6 in 50 scans and T13 in 6 (AUDIT L667).
- Published variant table: 85 of 252 lumbosacral scans have 6 lumbar vertebrae; Castellvi grades for the 325 TUM subjects; the GL series are not covered (AUDIT L660, L954). Extracted to `HOME/lstv_flag/sources/verse_suppl_table1.csv`, 325 rows (AUDIT L660).
- Centroid `_ctd.json` is kept in raw only (AUDIT L949).

**Derived products**

VerSeFusion (A8) and everything downstream of it (A8 lists them).

**Known defects and gaps**

- 10 VerSe'20 series were never downloaded: verse020, 112, 139, 141, 151, 202, 235, 251, 257, 290. Unify substituted their VerSe'19 copies silently (AUDIT L235-L238, L952).
- The BIDS `fracture_data/Genant_Fractures_thoracolumbar_reference.csv` was never fetched (AUDIT L955).
- No sacrum and no fused LSTV labels by release design (AUDIT L661).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): sbatch slurm/download_raw.sh with DATA_DIR/RAW_DIR on Ceph; check reads n_failed. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid verse19_20` prints them. Where the text below differs, `sources.json` is the runnable form.*

- `git clone` VerSeFusion, then `make setup && make download-slurm` (vfr:README.md L38-L46).
- Then fetch the 10 missing VerSe'20 series from node b2wxj or 4skx2 by name. `api.osf.io` `filter[name]=verse112` on folder 5ff7697786541a00b214a09f returns 1 (AUDIT L237).
- Verify: `download_manifest.json` failed 0; 319 VerSe'20 + 160 VerSe'19 series present; size per file equals the OSF listing.

---

### `versefusion` <a id="versefusion"></a>

**VerSeFusion-LSTV (fused VerSe'19+'20) and its nnU-Net conversion vf_813.** Cards: A (A8 versefusion), E (versefusion). Structured entry: `sources.yaml` id `versefusion`; kind project_release; status on_disk; re-acquisition submit (rebuild).

**Source id**

*[A]*

`versefusion`: the project's fused VerSe'19+'20 corpus, plus its nnU-Net conversion `vf_813` (AUDIT L652-L697; MDMR L184, L189).

*[E]*

`versefusion` (family A's id for the fused corpus and `vf_813`; the raw OSF download inside `~/VerSeFusion/data/raw` is family A's `verse19_20`, located at: `~/VerSeFusion` (HOME, raw, 139.0 GB, listing 2026-05-13); `~/VerSeFusion/data/raw` (HOME, raw, 71.0 GB))

**Name and citation**

*[A]*

VerSeFusion-LSTV (vfr:README.md L1-L30). Code repo `vfr:`, first commit 2026-05-11 [git] (`git log` in vfr).

*[E]*

VerSe'19 and VerSe'20 (Sekuboyina 2021 MedIA; Löffler 2021 Sci Data 8:284). The union is 374 scans from 355 patients (`DATA_COMPLETENESS_AUDIT.md` release rows, github.com/anjany/verse).

**Modality**

*[A]*

CT (derived from A7).

*[E]*

multi-detector CT with spine fields of view of mixed extent.

**Position/view**

*[A]*

Not recorded.

*[E]*

not recorded.

**Licence and access**

*[A]*

Code MIT; derived corpus follows VerSe terms (vfr:README.md L344-L352).

*[E]*

not recorded in the files Family E read.

**How it was acquired**

*[A]*

- `make unify-slurm` builds `data/unified`; `make qc-slurm` builds `data/qc` (vfr:README.md L38-L46).
- `ssn:tools/convert_versefusion.py --src HOME/VerSeFusion/data/unified --dst …` via `ssn:slurm/versefusion_convert.sh` builds `HOME/vf_813`: reoriented to PIR, C1-T9 and coccyx sent to ignore, TS ribs added (ssn:tools/convert_versefusion.py L1-L30; mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md).

*[E]*

VerSeFusion's own download step wrote `~/VerSeFusion/data/raw/download_manifest.json` (1,897 files, 0 failed) (`DATA_COMPLETENESS_AUDIT.md` line 663). That tool lives in the VerSeFusion tree on the grid, not in the repositories read here.

**When**

*[A]*

- unified 2026-05-12 23:46, canonical 2026-05-13 00:01 [doc] (G0 §2).
- `HOME/VerSeFusion` mtime 2026-05-13 [listing].
- `vf_813`, `vf_v10`, `vf_813_probe`, `vf_morphometrics` mtime 2026-09-12 [listing] (LIST).
- convert_versefusion.py first commit 2026-09-12 [git].

*[E]*

`~/VerSeFusion` is dated 2026-05-13 and `~/VerSeFusion.tar.gz` 2026-05-11 in the listing.

**What it contains**

*[A]*

- `HOME/VerSeFusion` is 139 GB: raw 71 GB, canonical 67 GB, unified 88 MB of links (AUDIT L662).
- `unified`: 374 `scan-*` dirs, 748 NIfTI (AUDIT L664).
- `manifest.csv`: 374 series / 355 patients (AUDIT L665).
- `configs/veridah_corrections.csv`: 25 rows, 14 scans renumbered (AUDIT L666).
- `HOME/vf_813`: 374 imagesTr + 374 labelsTr + `totalseg_raw`, 58 GB; no `dataset.json` (MDMR L189).

*[E]*

139 GB: `data/raw` 71 GB, `data/canonical` 67 GB, `data/unified` 88 MB of links (`DATA_COMPLETENESS_AUDIT.md` line 662).

**Where it is now**

*[A]*

All HOME: `VerSeFusion/` (raw, canonical, unified, corrected, manifest, qc), `vf_813/`, `vf_v10/`, `vf_813_probe/`, `vf_morphometrics/` (LIST; AUDIT L662-L666).

*[E]*

`~/VerSeFusion` (HOME, raw, 139.0 GB, listing 2026-05-13); `~/anchor_drr` (HOME, converted/derived, 2.6 GB, listing 2026-09-23); `~/anchor_drr_c2` (HOME, converted/derived, 1.7 GB, listing 2026-09-23); `~/bench_ts` (HOME, converted/derived, listing 2026-09-19); `~/ctsp_drr_obl` (HOME, converted/derived, listing 2026-09-13); `~/ctsp_drr_obl2` (HOME, converted/derived, listing 2026-09-13); `~/cut_rare` (HOME, converted/derived, listing 2026-09-15); `~/cut_rare_v2` (HOME, converted/derived, listing 2026-09-15); `~/fluorogen` (HOME, converted/derived, listing 2026-09-17); `~/implant_ct_smoke` (HOME, converted/derived, listing 2026-09-14); `~/implant_verse` (HOME, converted/derived, 187.0 GB, listing 2026-09-14); `~/implant_verse_smoke` (HOME, converted/derived, listing 2026-09-14); `~/lstv_flag` (HOME, converted/derived, listing 2026-09-15); `~/physics_drr` (HOME, converted/derived, listing 2026-09-14); `~/physics_drr_film` (HOME, converted/derived, listing 2026-09-17); `~/physics_rare` (HOME, converted/derived, listing 2026-09-14); `~/physics_rare_film` (HOME, converted/derived, listing 2026-09-18); `~/spinesurg-ct-nnunet` (HOME, converted/derived, 363 GB on 2026-09-19 per ssn:docs/CONTINUANCE_2026-09-19.md L27; the 1,433.6 GB of 2026-09-01 is superseded; listing 2026-09-25); `~/verse_drr` (HOME, converted/derived, listing 2026-09-20); `~/verse_drr_film` (HOME, converted/derived, listing 2026-09-17); `~/verse_drr_obl` (HOME, converted/derived, listing 2026-09-13); `~/verse_drr_obl2` (HOME, converted/derived, listing 2026-09-13); `~/verse_only_ctx_plus_nh` (HOME, converted/derived, listing 2026-09-13); `~/verse_soft_drr` (HOME, converted/derived, listing 2026-09-13); `~/vf_813` (HOME, converted/derived, 58.0 GB, listing 2026-09-12); `~/vf_813_probe` (HOME, converted/derived, listing 2026-09-12); `~/vf_v10` (HOME, converted/derived, listing 2026-09-12); `$RS/data/d815_repair` (CEPH, converted/derived, listing 2026-09-23); `$RS/data/rare_class` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/spineps` (CEPH, converted/derived, listing 2026-09-23); `$RS/data/anomaly_harvest/verse` (CEPH, converted/derived, listing 2026-09-23); `~/VerSeFusion/data/canonical` (HOME, converted/derived, 67.0 GB); `~/VerSeFusion/data/unified` (HOME, converted/derived, 0.1 GB); `~/spinesurg-ct-nnunet/nnunet/raw` (HOME, converted/derived)

**Annotation status**

*[A]*

- Release masks.
- VERIDAH-renumbered `data/corrected` for 14 scans. This is model output (AUDIT L666, L948).
- `vf_813` ribs are TotalSegmentator pseudolabels (ssn:tools/merge_versefusion_corpus.py docstring "LABEL STRENGTH").

*[E]*

release vertebra masks and centroids, plus 14 VERIDAH renumberings (`DATA_COMPLETENESS_AUDIT.md` line 666).

**Derived products**

*[A]*

- verse_drr (A21), verse_soft_drr (A22), ctsp_drr_obl/obl2 from vf_813 (A23), physics_drr / physics_rare VerSe parts (A19, A20), anchor_drr VerSe part (A26).
- implant_verse (A28), lstv_flag/renders_verse (A29), Dataset815 (A17).
- `HOME/bench_ts` (374 VerSe cases) (AUDIT L489).
- CEPH `data/anomaly_harvest/verse` (LIST); CEPH `data/rare_class/verse_drr` (ssn:SchwingNet/results/rare_class/split_plan.md).
- `HOME/model_night/verse_mask_levels.json` (AUDIT L667).

*[E]*

14 entries: `~/allspine_fov96_ctx`, `~/allspine_v6_fov96_ctx`, `~/allspine_v7_fov96_ctx`, `~/allspine_v7nofluoro_fov96_ctx`, `~/allspine_v8_fov96_ctx`, `~/allspine_v9_fov96_ctx`, `~/bench`, `~/m_fov96_ctx`, `~/m_mask22_scale_ctx`, `~/merged_ctx`, `~/obl2_fov96_ctx`, `~/verse_ctx`, `~/verse_only_ctx`, `~/vf_morphometrics`

**Known defects and gaps**

*[A]*

- The manifest flag `has_T13 = 18` is wrong; masks give 6. The cause is the VERIDAH stage (AUDIT L948; mem:versefusion-t13-flag-wrong.md).
- `vf_813` drops C1-T9, so it is fatal for whole-spine work (mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md).
- 18 subjects own 37 series. Series is not subject (PIS row verse; mem:identity-audit-findings.md).
- `implant_verse` is missing verse116, silently (AUDIT L956).

*[E]*

- 10 VerSe'20 series were never downloaded, and their VerSe'19 copies were substituted (`DATA_COMPLETENESS_AUDIT.md` line 235).
  - `verse_drr` carries 13 duplicate renders (line 240).
  - The manifest's T13 flag says 18 where the truth is 6 (`MANIFEST_DATA_MODELS_RESULTS.md` 7.5).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): unify then qc chained with afterany; DATA_DIR on Ceph. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid versefusion` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[A]*

- Regenerate from A7: `make unify-slurm qc-slurm` in vfr.
- Then `sbatch ssn:slurm/versefusion_convert.sh` for `vf_813`.
- Verify: 374 unified scans, `missing_kinds` empty (AUDIT L664); manifest 374 rows.

*[E]*

manual. Re-run the VerSeFusion download from its repository (not in the trees read here) and verify against `data/raw/download_manifest.json`. No checksum is recorded in Family E's evidence.

---

### `totalsegmentator_v201` <a id="totalsegmentator_v201"></a>

**TotalSegmentator dataset v2.0.1.** Cards: A (A9 totalsegmentator_v201), E (totalsegmentator_v201). Structured entry: `sources.yaml` id `totalsegmentator_v201`; kind upstream_release; status on_disk; re-acquisition run (zenodo_http).

**Source id**

*[A]*

`totalsegmentator_v201`: TotalSegmentator dataset v2.0.1 (AUDIT L475-L516).

*[E]*

`totalsegmentator_v201` (family A's id)

**Name and citation**

*[A]*

- Wasserthal J, et al., Radiol Artif Intell 2023;5:e230024 (ctsp:paper/cns2026/make_cns_deck_v10.py L169).
- Zenodo 10.5281/zenodo.10047292 (AUDIT L479).
- `ts_to_drr.py` wrongly cites the v1 record 6802613 (AUDIT L514).

*[E]*

TotalSegmentator dataset v2.0.1, Zenodo 10.5281/zenodo.10047292 (`DATA_COMPLETENESS_AUDIT.md` heading line 475).

**Modality**

*[A]*

- Routine clinical CT, 1.5 mm isotropic, RAS (mem:spine-data-review-and-ts-bench.md).
- Study types include abdomen-pelvis, thorax-abdomen-pelvis, polytrauma whole-body, neck (ssn:tools/ts_to_drr.py L5-L8).

*[E]*

CT, whole body with study types of mixed extent.

**Position/view**

*[A]*

Not recorded. `meta.csv` has `study_type` and no position field (PIS row ts).

*[E]*

not recorded.

**Licence and access**

*[A]*

Open, CC BY 4.0 (AUDIT L567; ssn:docs/RSNAI_DATA_MANIFEST.json roots.ts_subjects).

*[E]*

CC BY 4.0, open (`DATA_COMPLETENESS_AUDIT.md` release row "Inputs of anchor_drr").

**How it was acquired**

*[A]*

- Download of `Totalsegmentator_dataset_v201.zip` from Zenodo into `HOME/data/TotalSegmentator`, with `dl.log` and `dl.status = DL_DONE` (AUDIT L483; G0 §2).
- The fetch script is not in either repository (searched both repos for `10047292` and `DL_DONE`).
- Verification: zip size 23,581,218,285 B matches Zenodo 23.6 GB (AUDIT L483). The Zenodo MD5 is cited only truncated (`fe250e5718e0a3b5df4c4e…`, AUDIT L479).

*[E]*

one Zenodo zip, `Totalsegmentator_dataset_v201.zip`, ending with `dl.status = DL_DONE` (`DATA_COMPLETENESS_AUDIT.md` line 483). The fetch script is not in the repositories read here.

**When**

*[A]*

dl.log created 2026-09-14 10:16; zip complete 2026-09-14 12:36 [doc] (G0 §2).

*[E]*

2026-09-14, from `dl.status` (`DATA_COMPLETENESS_AUDIT.md` line 483). The listing also dates the folder 2026-09-14.

**What it contains**

*[A]*

- 1,228 subject dirs, each with `ct.nii.gz`, `segmentations/` (117 masks) and one `meta.csv` (AUDIT L479, L484).
- Release split: train 1,082 / val 57 / test 89 (AUDIT L481).
- Size: 82 GB per MDMR L185; `du` 86G per AUDIT L515.

*[E]*

1,228 subject directories with `ct.nii.gz` and 117 masks each. The zip is 23,581,218,285 B (`DATA_COMPLETENESS_AUDIT.md` lines 483-484) and the whole folder 82 GB (`MANIFEST_DATA_MODELS_RESULTS.md` 2.2).

**Where it is now**

*[A]*

HOME `data/TotalSegmentator/`: zip plus unpacked tree, raw (AUDIT L483-L484; LIST 2026-09-14).

*[E]*

`~/anchor_drr` (HOME, converted/derived, 2.6 GB, listing 2026-09-23); `~/bench_ts` (HOME, converted/derived, listing 2026-09-19); `~/fluorogen` (HOME, converted/derived, listing 2026-09-17); `~/implant_ts` (HOME, converted/derived, 39.0 GB, listing 2026-09-14); `~/physics_drr` (HOME, converted/derived, listing 2026-09-14); `~/physics_drr_film` (HOME, converted/derived, listing 2026-09-17); `~/ts_drr` (HOME, converted/derived, listing 2026-09-20); `~/data/TotalSegmentator` (HOME, raw, 82.0 GB, listing 2026-09-14); `$RS/data/devcorpus` (CEPH, converted/derived, 2.5 GB, listing 2026-09-22); `$RS/data/devcorpus_arc` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/rare_class` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/spineps` (CEPH, converted/derived, listing 2026-09-23); `$RS/data/validation_ts` (CEPH, converted/derived, 1.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/totalsegmentator` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/anomaly_harvest/validation_ts` (CEPH, converted/derived, 2.0 GB, listing 2026-09-24)

**Annotation status**

*[A]*

- Model output, manually refined.
- 117 structures; no L6 and no T13 class (ssn:tools/ts_to_drr.py L10-L16; MDMR L185).
- External L6/T13 labels for some subjects exist in fhofmann/VertebralBodiesCT-Labels `data.csv` (ACQ L94; ssn:docs/ruleclass/CLASSIFIERS.md R17).

*[E]*

release structure masks with no T13 or L6 class (`MANIFEST_DATA_MODELS_RESULTS.md` 2.2). Externally, 70 CTs carry VertebralBodiesCT labels (`jobs.txt`).

**Derived products**

*[A]*

- ts_drr (A24), physics_drr totalseg part (1,831 renders, 1,121 subjects) (A19; AUDIT L492), anchor_drr (2,456 images) (A26; AUDIT L493), implant_ts (A28).
- `HOME/bench_ts`: SPINEPS+VERIDAH, 1,118 of 1,228 masks (AUDIT L230-L233, L489).
- `HOME/ts_dupscan_out/ct_fingerprints.json` (AUDIT L496).
- CEPH `data/validation_ts`: 71 v2 CTs screened against external labels (CENSUS25 §1; LIST 2026-09-23).

*[E]*

7 entries: `~/allspine_v6_fov96_ctx`, `~/allspine_v7_fov96_ctx`, `~/allspine_v7nofluoro_fov96_ctx`, `~/allspine_v8_fov96_ctx`, `~/allspine_v9_fov96_ctx`, `~/bench`, `~/ts_dupscan_out`

**Known defects and gaps**

*[A]*

- v2.0.1 vertebra label mix-ups, fixed in v3 (ssn:tools/ts_to_drr.py L16-L19).
- **24 renumbered ids.** v201 s1406-s1429 are byte-identical to different v300 ids, so keying `ts:s####` without the release splits 24 people and merges 15. `tools/identity/ts_alias.json` does not exist (AUDIT L370-L373, L497; mem:identity-audit-findings.md).
- `implant_ts` is unfinished: 355 subjects never processed (AUDIT L365-L368).
- SPINEPS failed deterministically on 72 spines (AUDIT L230-L233).

*[E]*

- The data cannot express T13 or L6.
  - The `ts_drr` path maps were computed from the v3 root (`DATA_COMPLETENESS_AUDIT.md` line 225).
  - 110 of 1,228 CTs had no SPINEPS mask before the 2026-09-23 repair (`DATA_COMPLETENESS_AUDIT.md` line 1258).

**Re-acquisition recipe**

*[A]*

- `curl -L -C - -o Totalsegmentator_dataset_v201.zip "https://zenodo.org/records/10047292/files/Totalsegmentator_dataset_v201.zip?download=1"`. The URL form is from `ssn:slurm/carmlspine_fetch.sh` L16; the file name is from AUDIT L483.
- Verify the md5 against `https://zenodo.org/api/records/10047292` `files[].checksum`, and size 23,581,218,285 B.
- `unzip`; expect 1,228 `s*` dirs, each with 117 segmentation files (AUDIT L484).

*[E]*

proposed, not the original route: `python tools/acquisition_fetch.py zenodo --collection totalsegmentator_v2 --record 10047292`, which verifies against the record's md5 (`nnunet:tools/acquisition_fetch.py` docstring). The original download tool is not recorded.

---

### `totalsegmentator_v300` <a id="totalsegmentator_v300"></a>

**TotalSegmentator dataset v3.0.0.** Cards: A (A10 totalsegmentator_v300), E (totalsegmentator_v300). Structured entry: `sources.yaml` id `totalsegmentator_v300`; kind upstream_release; status on_disk; re-acquisition run (zenodo_http).

**Source id**

*[A]*

`totalsegmentator_v300`: TotalSegmentator dataset v3.0.0 (AUDIT L475-L516).

*[E]*

`totalsegmentator_v300` (family A's id)

**Name and citation**

*[A]*

Zenodo 10.5281/zenodo.22688904, published 2026-09-10 (AUDIT L480).

*[E]*

TotalSegmentator dataset v3.0.0, Zenodo 10.5281/zenodo.22688904 (`DATA_COMPLETENESS_AUDIT.md` heading line 475).

**Modality**

*[A]*

CT, as v2, plus 291 paediatric CTs (AUDIT L480).

*[E]*

CT, whole body with study types of mixed extent.

**Position/view**

*[A]*

Not recorded. `meta.csv` adds `convolution_kernel` and `slice_thickness` (PIS row ts).

*[E]*

not recorded.

**Licence and access**

*[A]*

Open. Licence not separately recorded for v3. The RSNAI manifest root (the v300 path) states CC BY 4.0 (ssn:docs/RSNAI_DATA_MANIFEST.json roots.ts_subjects).

*[E]*

not recorded in Family E's evidence for v3. The `RSNAI_DATA_MANIFEST.json` root `ts_subjects` says "CC BY 4.0", but its source string names v2 while its path is v3.

**How it was acquired**

*[A]*

- Zip download into `HOME/data/TotalSegmentator_v3`, then unzip (`unzip.log`, `UNZIP_DONE`) (AUDIT L485; ssn:docs/CONTINUANCE_2026-09-19.md L26).
- Fetch script: not in either repo.
- Verification: size 37,415,622,057 B matches Zenodo 37.4 GB (AUDIT L485).

*[E]*

one Zenodo zip, unpacked the same day (`DATA_COMPLETENESS_AUDIT.md` line 485).

**When**

*[A]*

dl.log 2026-09-19 12:50; zip complete 2026-09-19 14:36 [doc] (G0 §2; AUDIT L485).

*[E]*

the zip is dated 2026-09-19 14:36 (`DATA_COMPLETENESS_AUDIT.md` line 485). The listing dates the folder 2026-09-19.

**What it contains**

*[A]*

- 1,939 subject dirs, 117 masks each (AUDIT L486).
- Split: train 1,830 / test 109; 286 age < 18; 15 blank age (AUDIT L482).
- Unpacked: 228,803 files, 52,343,746,738 B (ssn:docs/RSNAI_DATA_MANIFEST.json roots.ts_subjects).
- 1,935 distinct scans (1,939 minus 4 duplicate ids) (AUDIT L503).

*[E]*

1,939 subject directories (`DATA_COMPLETENESS_AUDIT.md` line 486). The zip is 37,415,622,057 B and the unpacked folder 52,343,746,738 B (`RSNAI_DATA_MANIFEST.json`).

**Where it is now**

*[A]*

HOME `data/TotalSegmentator_v3/` (zip plus `Totalsegmentator_dataset_v300/`), raw (AUDIT L485-L486; LIST 2026-09-19).

*[E]*

`~/anchor_drr_c2` (HOME, converted/derived, 1.7 GB, listing 2026-09-23); `~/ts_drr_v3` (HOME, converted/derived, listing 2026-09-19); `~/data/TotalSegmentator_v3` (HOME, raw, 89.8 GB, listing 2026-09-19); `$RS/data/anomaly_harvest/totalsegmentator` (CEPH, converted/derived, listing 2026-09-24)

**Annotation status**

*[A]*

Model output, manually refined; "refined labels especially for bone structures" (AUDIT L480).

*[E]*

release structure masks.

**Derived products**

*[A]*

- ts_drr_v3 (A25), anchor_drr_c2 (1,890 of 1,939) (A27; AUDIT L501).
- Device corpus: CEPH `data/devcorpus`, 142 clean subjects (`HOME/model_night/ts_clean_subjects.txt`). This belongs to the synthetic-render family; cross-reference (AUDIT L490, L491, L500, L507).
- CEPH `data/spineps/tsv3` and CEPH `data/anomaly_harvest/totalsegmentator` (LIST; ssn:docs/RESUME_2026-09-22_PM.md L193 "tsv3 1,616").

*[E]*

1 entries: `~/ts_dupscan_out`

**Known defects and gaps**

*[A]*

- `CTINV` reads "0 nii" because the counter looks one level too shallow (AUDIT L508).
- Three intra-v300 duplicate groups (AUDIT L370-L373).
- DATASHEET, MODEL_CARD and the RSNAI manifest call the device-corpus source "v2"; it is v3 (AUDIT L507).

*[E]*

24 subjects are renumbered between v2 and v3, and there are three duplicate groups across the two releases (`DATA_COMPLETENESS_AUDIT.md` line 370).

**Re-acquisition recipe**

*[A]*

- As A9, with record 22688904 and file `Totalsegmentator_dataset_v300.zip`.
- Verify size 37,415,622,057 B and the API md5.
- Expect 1,939 dirs.

*[E]*

proposed: `python tools/acquisition_fetch.py zenodo --collection totalsegmentator_v3 --record 22688904`, which verifies against the record's md5.

---

### `rsna_2022_cspine` <a id="rsna_2022_cspine"></a>

**RSNA 2022 Cervical Spine Fracture Detection (Kaggle).** Cards: A (A11 rsna_2022_cspine), E (rsna_2022_cspine). Structured entry: `sources.yaml` id `rsna_2022_cspine`; kind upstream_release; status on_disk; re-acquisition run (kaggle).

**Source id**

*[A]*

`rsna_2022_cspine`: RSNA 2022 Cervical Spine Fracture Detection, the Kaggle competition archive. Also in the other-CT stream (OCT).

*[E]*

`rsna_2022_cspine` (family A's id)

**Name and citation**

*[A]*

- Kaggle competition `rsna-2022-cervical-spine-fracture-detection`.
- Dataset paper doi 10.1148/ryai.230034 (AUDIT L568).

*[E]*

RSNA 2022 Cervical Spine Fracture Detection, a Kaggle competition archive. The dataset paper is 10.1148/ryai.230034 (`DATA_COMPLETENESS_AUDIT.md` release row).

**Modality**

*[A]*

CT (DICOM), cervical spine (AUDIT L568).

*[E]*

CT, cervical spine.

**Position/view**

*[A]*

Not recorded.

*[E]*

not recorded.

**Licence and access**

*[A]*

- Registration: the Kaggle account must accept the competition rules (ssn:slurm/rsna_cspine_fetch.sh L2-L5).
- Licence terms for derived labels are not recorded.

*[E]*

gated. The competition rules must be accepted on kaggle.com, and the download needs a Kaggle API token (`nnunet:slurm/rsna_cspine_fetch.sh` header).

**How it was acquired**

*[A]*

- `MODE=download nohup bash ssn:slurm/rsna_cspine_fetch.sh > HOME/data/rsna_cspine/fetch.log`: Kaggle CLI `competitions download -c rsna-2022-cervical-spine-fracture-detection` (ssn:slurm/rsna_cspine_fetch.sh L6-L22).
- It ran on the login node under nohup (ssn:slurm/rsna_cspine_fetch.sh L4-L5).
- Verification: Kaggle CLI "100% 189G/189G"; zip listing intact (job 40416361) (AUDIT L584).

*[E]*

`MODE=download nohup bash slurm/rsna_cspine_fetch.sh`, which runs `kaggle competitions download -c rsna-2022-cervical-spine-fracture-detection` (`nnunet:slurm/rsna_cspine_fetch.sh`). The script ran on the login node, which the current grid rules forbid. No checksum was used beyond the zip listing.

**When**

*[A]*

Fetched 2026-09-19 [doc] (AUDIT L342; `fetch.log` rc=0). Script committed 2026-09-19 [git].

*[E]*

fetched 2026-09-19, `fetch.log` rc=0 (`DATA_COMPLETENESS_AUDIT.md` line 340).

**What it contains**

*[A]*

- zip 203,318,086,447 B, plus one `.nii.zip`, `sample_submission.csv` and `fetch.log` (AUDIT L584).
- 2,019 train studies (AUDIT L340, L568). The header census counts 2,022 studies (OCT "Denominators").
- 87 segmentations (ssn:slurm/rsna_cspine_fetch.sh L2).

*[E]*

a zip of 203,318,086,447 B with 2,019 training studies (`DATA_COMPLETENESS_AUDIT.md` line 584).

**Where it is now**

*[A]*

- HOME `data/rsna_cspine/` (raw zip, never unpacked) (AUDIT L340-L343; LIST 2026-09-19).
- CEPH `data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl` (header census) (OCT; ssn:tools/other_ct_fetch.py L13-L16).

*[E]*

`~/data/rsna_cspine` (HOME, raw, 203.3 GB, listing 2026-09-19); `$RS/data/anomaly_harvest/other_ct` (CEPH, converted/derived, listing 2026-09-24)

**Annotation status**

*[A]*

Release labels: per-level fracture labels plus 87 segmentations (ssn:slurm/rsna_cspine_fetch.sh L2). No project annotation.

*[E]*

release fracture labels and segmentations, which the project does not use.

**Derived products**

*[A]*

Header census only. Every study was refused: the longest is 334 mm craniocaudal (OCT "Denominators").

*[E]*

a header census under `$RS/data/anomaly_harvest/other_ct/rsna` (`nnunet:tools/other_ct_fetch.py`). none found in the disk map

**Known defects and gaps**

*[A]*

- Used by nothing.
- 237 GB of home quota (AUDIT L340-L343). The Kaggle token was in a chat transcript and was to be rotated (ssn:docs/CONTINUANCE_2026-09-19.md L24).

*[E]*

nothing uses this data, and it was never unpacked. It occupies 236.8 GB of the home quota (`mem:grid-quota-and-deleted-banks`).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): the spineps env's kaggle by path, with -p. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid rsna_2022_cspine` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[A]*

- `MODE=download nohup bash slurm/rsna_cspine_fetch.sh`, with `KAGGLE_API_TOKEN` in `~/.fluorocap/credentials.env` and the rules accepted (ssn:slurm/rsna_cspine_fetch.sh).
- Target CEPH, not HOME.
- Verify zip size 203,318,086,447 B and `unzip -t`.

*[E]*

manual gate (accept the rules), then `MODE=download` with the same script submitted through `sbatch` on a compute node. Verify that the zip size equals Kaggle's listing.

---

### `ribfrac` <a id="ribfrac"></a>

**RibFrac (MICCAI 2020) chest CT, with RibSeg v2 and the Moller rib masks.** Cards: A (A12 ribfrac), B (RibFrac / RibSeg v2 (tier 2 here; already fetched by the other_ct stream)), E (ribfrac). Also known as: `zenodo_ribfrac`. Structured entry: `sources.yaml` id `ribfrac`; kind upstream_release; status on_disk; re-acquisition run (zenodo_http+other_ct_fetch).

**Source id**

*[A]*

`ribfrac`: RibFrac (MICCAI 2020) chest CT, with RibSeg v2 and the Möller rib masks. Also in the other-CT stream (OCT).

*[B: card `zenodo_ribfrac`]*

`zenodo_ribfrac` (acquisition/ranking.csv collection `zenodo:ribfrac`; tools/other_ct_fetch.py)

*[E]*

`ribfrac` (family A's id; family B uses `zenodo_ribfrac`)

**Name and citation**

*[A]*

- RibFrac: Zenodo 3893508, 3893498, 3893496, 3993380 (ssn:tools/acquisition_census.py L388-L391).
- RibSeg v2: GitHub HINTLab/RibSeg (ctsp:slurm/ribseg.sh L20-L23).
- Möller et al. 2025 stump-rib masks: Zenodo 14864106 (mem:lstv-data-landscape.md).

*[B: card `zenodo_ribfrac`]*

RibFrac Dataset (MICCAI 2020); Zenodo 3893508 published 2020-06-15, 3893498 published 2020-06-15, 3893496 published 2020-06-15, 3993380 published 2020-08-24 (acquisition/sweep/zenodo_ge5GB_ct.tsv); RibSeg v2 rib labels are a second rib reading (acquisition/ranking.csv)

*[E]*

RibFrac (MICCAI 2020), 660 chest CTs (`nnunet:tools/other_ct_fetch.py` header).

**Modality**

*[A]*

CT, chest-abdomen (ssn:tools/acquisition_census.py L388).

*[B: card `zenodo_ribfrac`]*

chest-abdomen CT, class CHEST_SCREEN in the census (T13 by rib count only); cage countable from T1 in 626, sacrum reached in 9 (acquisition/ranking.csv; SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md)

*[E]*

CT, chest.

**Position/view**

*[A]*

Not recorded.

*[B: card `zenodo_ribfrac`]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded.

**Licence and access**

*[A]*

RibFrac CC BY-NC 4.0 (ssn:tools/other_ct_fetch.py L11; ssn:tools/acquisition_census.py L389). Möller masks CC BY 4.0 (mem:lstv-data-landscape.md).

*[B: card `zenodo_ribfrac`]*

open, CC BY-NC 4.0 (acquisition/ranking.csv; tools/other_ct_fetch.py)

*[E]*

CC BY-NC 4.0, open (`ranking.csv`).

**How it was acquired**

*[A]*

- `HOME/data/ribs/dl.sh` (log `dl.log`, marker `RIBS_DL_DONE`) fetched RibFrac, RibSeg v1 and the Möller manual rib masks; RibSeg v2 is at `HOME/data/ribs/ribseg_v2.zip` (ssn:docs/CONTINUANCE_2026-09-19.md L25).
- `dl.sh` is not in either repo.
- Images were then unzipped to CEPH by `ssn:slurm/other_ct_fetch.sh ribfrac`, which runs `ssn:tools/other_ct_fetch.py ribfrac --zips HOME/data/ribs --out CEPH/data/ribfrac`. Only `ribfrac-*-images*.zip` members ending `-image.nii.gz` are extracted (ssn:tools/other_ct_fetch.py L115-L140).
- Verification: member size match only.

*[B: card `zenodo_ribfrac`]*

not by the acquisition chain (its `tier2` target is unsubmitted) (slurm/acquisition_submit.sh); zips were downloaded to HOME `~/data/ribs/` by `dl.sh` (log `dl.log`, `RIBS_DL_DONE`) (docs/CONTINUANCE_2026-09-19.md); images unzipped to CEPH by `python tools/other_ct_fetch.py ribfrac --zips ~/data/ribs --out /rs/rs_grp_oschome/go2432/data/ribfrac` (`slurm/other_ct_fetch.sh`) (tools/other_ct_fetch.py)

*[E]*

zips in `~/data/ribs` by a route that is not recorded. The images were then unzipped to Ceph with `tools/other_ct_fetch.py ribfrac --zips ~/data/ribs --out $RS/data/ribfrac` (`nnunet:tools/other_ct_fetch.py`).

**When**

*[A]*

- `HOME/data/ribs` mtime 2026-09-19 [listing]; running on 2026-09-19 [doc] (ssn:docs/CONTINUANCE_2026-09-19.md L25).
- CEPH `data/ribfrac` mtime 2026-09-23 [listing] (LIST).

*[B: card `zenodo_ribfrac`]*

HOME `data/ribs` dated 2026-09-19, CEPH `data/ribfrac` dated 2026-09-23 (listing)

*[E]*

`~/data/ribs` is dated 2026-09-19 and `$RS/data/ribfrac` 2026-09-23 in the listing.

**What it contains**

*[A]*

- 660 chest CTs: train 420 + val 80 + test 160 (OCT "Denominators").
- RibSeg v2: 661 numbered rib masks plus centrelines (ssn:docs/CONTINUANCE_2026-09-19.md L25).
- CEPH: 73 GB (CENSUS25 §4).

*[B: card `zenodo_ribfrac`]*

660 CT, 77.8 GB by the records (acquisition/ranking.csv); 73 GB on the volume on 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md section 4)

*[E]*

73 GB on Ceph (`CENSUS_TABLE_2026-09-25.md` 4). The size on HOME is not recorded.

**Where it is now**

*[A]*

- HOME `data/ribs/` (zips, raw).
- CEPH `data/ribfrac/images/` and `members.json` (converted) (ssn:tools/other_ct_fetch.py L118, L139).
- CEPH `data/anomaly_harvest/other_ct` (screen) (OCT).
- A local `ctsp:ribseg_v2.zip` exists on the laptop (ctsp listing).

*[B: card `zenodo_ribfrac`]*

HOME `~/data/ribs/` (zips, RibSeg v2, Möller rib masks); CEPH `/rs/rs_grp_oschome/go2432/data/ribfrac/images` (unzipped images); screen under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/` (listing; SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md; docs/ruleclass/STUMP_RULE.md)

*[E]*

`~/data/ribs` (HOME, raw, listing 2026-09-19); `$RS/data/ribfrac` (CEPH, raw, 73.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/other_ct` (CEPH, converted/derived, listing 2026-09-24)

**Annotation status**

*[A]*

- RibFrac fracture labels (release).
- RibSeg v2 rib labels: expert-corrected (ctsp:docs/DATASETS_ROADMAP.md L26).
- Möller masks: manual plus predicted (mem:lstv-data-landscape.md).
- Two-labeller transitional screen: 4 T13 and 1 L6 candidates, plus unassigned (OCT "Calls").

*[B: card `zenodo_ribfrac`]*

release fracture labels and RibSeg v2 rib labels; Möller manual rib masks on 31 CTs; other_ct stream pseudo-labels (SPINEPS 655, TS 660): T13 4 single-labeller, L6 1 morphology-only (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md; docs/ruleclass/TIERS.md section 5)

*[E]*

release fracture labels, which are not used here. A screen runs under `anomaly_harvest/other_ct`.

**Derived products**

*[A]*

- Other-CT registry rows (OCT).
- CTSP rib relabel experiment `ctsp:slurm/ribseg.sh` (RibSeg applied to CTSP, not RibFrac data).

*[B: card `zenodo_ribfrac`]*

registry other_ct stream, 660 persons (SchwingNet/results/transitional_registry/REGISTRY.md); tiers: 660 CTs, tier 1 35, tier 2 620, untiered 5 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map

**Known defects and gaps**

*[A]*

- 626 cages are countable from T1, but only 9 scans reach the sacrum (OCT).
- The `dl.sh` URLs are not preserved in git (searched both repos).

*[B: card `zenodo_ribfrac`]*

the content of `dl.sh` is on the grid only, so the exact download URLs are not in the repository (docs/CONTINUANCE_2026-09-19.md); this source belongs mainly to the ribs/other-CT family (tools/other_ct_fetch.py)

*[E]*

the data is held twice, as zips on HOME and unzipped images on Ceph.

**Re-acquisition recipe**

*[A]*

- manual: download the RibFrac image and label zips from Zenodo records 3893508, 3893498, 3893496 and 3993380 into `<dir>`, verifying each against the record API's md5.
- Download RibSeg v2 from the RibSeg project (source URL not recorded) and the Möller masks from Zenodo 14864106.
- Then `sbatch -D CEPH/tmp ssn:slurm/other_ct_fetch.sh ribfrac` with `--zips <dir>`.
- Expect 660 `*-image.nii.gz` files.

*[B: card `zenodo_ribfrac`]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_ribfrac ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection ribfrac --record 3893508 3893498 3893496 3993380 --include 'images'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh) (the `tier2` route as written); must verify 660 `*-image.nii.gz`

*[E]*

`python tools/acquisition_fetch.py zenodo --collection ribfrac --record 3893508 3893498 3893496 3993380 --include 'images'` (`nnunet:slurm/acquisition_submit.sh` line 106, in the `tier2` block, which was not submitted on 2026-09-23). It verifies the md5 of each file. Alternatively, unzip again from `~/data/ribs` with `tools/other_ct_fetch.py ribfrac`.

---

### `nnunet_dataset802_803` <a id="nnunet_dataset802_803"></a>

**Dataset802_SpineSurgCTFull (10-class) and Dataset803_SpineSurgCTFullMerged (9-class), from the April release.** Cards: A (A14 nnunet_dataset802_803). Structured entry: `sources.yaml` id `nnunet_dataset802_803`; kind derived; status on_disk; re-acquisition run (hf_hub).

**Source id**

`nnunet_dataset802_803`: Dataset802_SpineSurgCTFull (10-class) and Dataset803_SpineSurgCTFullMerged (9-class, L5 and L6 merged), built from the April release (A3) (ssn:slurm/convert_hf_to_nnet.sh L14-L37; sps:slurm/spine_prep.sh L22-L66).

**Name and citation**

- spinopelvic-seg (sps:README.md L11).
- Checkpoints on HF `OpenSpineConsortium/spinopelvic-seg-checkpoints` (BUILD L27; ssn:docs/ruleclass/ARM_B_pelvis.md L50-L56).

**Modality**

CT (A3 volumes via symlinks) (ssn:slurm/convert_hf_to_nnet.sh L14-L37).

**Position/view**

As A3.

**Licence and access**

- Code Apache-2.0 (sps git log "license: add Apache-2.0").
- Data inherits CC BY-NC-SA 4.0 (ctsp:README.md L516-L519).

**How it was acquired**

- `ssn:slurm/convert_hf_to_nnet.sh` reads `HOME/CTSpinoPelvic1K/data/hf_export/{manifest_*,splits_5fold.json,ct,labels}` and writes symlinked `imagesTr`/`labelsTr` plus `splits_final.json` and `lstv_cases.json` (ssn:slurm/convert_hf_to_nnet.sh L14-L37).
- Dataset803 defaults date from v5, 2026-05-03 (sps:slurm/spine_prep.sh L49-L51).

**When**

`spine_convert.sh` first commit 2026-04-27 [git]; training from 3 May 2026 [doc] (CRC L327-L329).

**What it contains**

- 1,153 records (CRC L327-L329).
- Dataset803 classes: 1-4 L1-L4, 5 last_lumbar, 6 sacrum, 7-8 hips, 9 ignore; 3d_fullres 0.8×0.75×0.75 mm (ssn:docs/ruleclass/ARM_B_pelvis.md L58-L60).

**Where it is now**

- `HOME/spinesurg-ct-nnunet/nnunet/results/Dataset802` was kept by RECLAIM (RECLAIM L23-L26).
- Dataset803 checkpoints are under CEPH `neurips_v11/ens/nnunet_results/`, fetched from HF (ssn:docs/ruleclass/ARM_B_pelvis.md L52-L55; LIST).
- The raw trees' image targets (`hf_export`) are deleted (AUDIT L140-L143).

**Annotation status**

Release labels of A3 (CRC L327-L333).

**Derived products**

- Out-of-fold pelvic pseudolabels for CTSP v2 (BUILD L27).
- ARM B pelvis of the SUPER DETECTOR RUN (ssn:docs/ruleclass/ARM_B_pelvis.md).

**Known defects and gaps**

The raw symlinks dangle because their `hf_export` target is gone (AUDIT L140-L143).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual rebuild; the checkpoint fetch is re-carded as a model source. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid nnunet_dataset802_803` prints them. Where the text below differs, `sources.json` is the runnable form.*

- Checkpoints: `huggingface_hub.snapshot_download("OpenSpineConsortium/spinopelvic-seg-checkpoints", local_dir="nnunet/results/Dataset803_SpineSurgCTFullMerged")` (sps:README.md L41-L60).
- Verify per-fold sizes against the HF listing, as the v11 workflow did (ssn:docs/ruleclass/ARM_B_pelvis.md L53-L55).
- Raw tree: rebuild A3, then `ssn:slurm/convert_hf_to_nnet.sh`.

---

### `nnunet_dataset810` <a id="nnunet_dataset810"></a>

**Dataset810_SpineSurgLSTVOneShot (24 classes).** Cards: A (A15 nnunet_dataset810). Structured entry: `sources.yaml` id `nnunet_dataset810`; kind derived; status on_disk; re-acquisition manual (rebuild).

**Source id**

`nnunet_dataset810`: Dataset810_SpineSurgLSTVOneShot (mem:lstv-oneshot-training-run.md).

**Name and citation**

Project dataset; no external citation.

**Modality**

CT (A2 volumes via links) (AUDIT L581).

**Position/view**

As A2.

**Licence and access**

Inherits CC BY-NC-SA 4.0 (ctsp:README.md L516-L519).

**How it was acquired**

- Prep from the v10 working copy `HOME/data/CTSpinoPelvic1K` with `HF_EXPORT_DIR` (mem:lstv-oneshot-training-run.md).
- 24 classes (mem:lstv-oneshot-training-run.md).

**When**

Launched 2026-09-07; retired 2026-09-08 [doc] (mem:lstv-oneshot-training-run.md).

**What it contains**

802 imagesTr and 802 labelsTr. The image links point to `/data/hf_export` container paths and dangle on the host (AUDIT L581).

**Where it is now**

- HOME `spinesurg-ct-nnunet/nnunet/raw/Dataset810_SpineSurgLSTVOneShot`. Raw is kept as the benchmark's scoring space; preprocessed was deleted (ssn:slurm/switch_to_fullribs.sh L12, L53-L54).
- Results kept (AUDIT L595).

**Annotation status**

Release labels (v10), remapped (mem:lstv-oneshot-training-run.md).

**Derived products**

Retired one-shot fold results (AUDIT L595).

**Known defects and gaps**

Container-path links (mem:dataset813-image-links-are-container-paths.md).

**Re-acquisition recipe**

Regenerate with the prep job and `HF_EXPORT_DIR=$HOME/data/CTSpinoPelvic1K` (mem:dataset813-image-links-are-container-paths.md). The exact prep command for 810 is not recorded.

---

### `nnunet_dataset813` <a id="nnunet_dataset813"></a>

**Dataset813_SpineSurgLSTVFullRibs (42 foreground classes, ignore 43).** Cards: A (A16 nnunet_dataset813). Structured entry: `sources.yaml` id `nnunet_dataset813`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`nnunet_dataset813`: Dataset813_SpineSurgLSTVFullRibs, 42 foreground classes, ignore 43 (mem:lstv-oneshot-training-run.md).

**Name and citation**

Project dataset.

**Modality**

CT (A2 via links) (AUDIT L624).

**Position/view**

As A2.

**Licence and access**

Inherits CC BY-NC-SA 4.0.

**How it was acquired**

- `ssn:slurm/switch_to_fullribs.sh`: prep, then unpack, then folds (mem:lstv-oneshot-training-run.md).
- labelsTr converted on 2026-09-08 from `HOME/CTSpinoPelvic1K/data/hf_export`, since deleted (AUDIT L140-L143, L624).

**When**

labelsTr dated 2026-09-08 [doc] (AUDIT L624). 5-fold archived 2026-09-11 [doc] (AUDIT L595).

**What it contains**

802 labelsTr; 802 imagesTr links `COLONOG_<token>_0000.nii.gz` → `/data/hf_export/ct/<id>_ct.nii.gz`; 5-fold `splits_final.json`; `lstv_cases.json` (AUDIT L624, L636).

**Where it is now**

HOME `spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs`, and results (AUDIT L595, L624).

**Annotation status**

Release labels, but from a stale pre-consensus export: `lstv_cases.json` flags 23 records where the release flags 34 (AUDIT L140-L143, L911).

**Derived products**

- ctsp_drr (labels read from here) (ssn:slurm/ctx_build_ctsp.sh).
- 200-epoch fold_0 (AUDIT L595).
- bench (A2).

**Known defects and gaps**

- The label version behind it is unrecorded (AUDIT L140-L143).
- 11 transitional records are marked normal (AUDIT L911).
- Links resolve only inside the container (mem:dataset813-image-links-are-container-paths.md).

**Re-acquisition recipe**

Regenerate `lstv_cases.json` and `splits_final.json` from `HOME/data/CTSpinoPelvic1K/manifest.json` + `splits_5fold.json` (token ↔ release id), and record the label-deposit sha in `dataset.json` (AUDIT L142-L143).

---

### `nnunet_dataset815` <a id="nnunet_dataset815"></a>

**Dataset815_SpineSurgLSTVVerSe (CTSP 802 + VerSeFusion 374 = 1,176).** Cards: A (A17 nnunet_dataset815). Structured entry: `sources.yaml` id `nnunet_dataset815`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`nnunet_dataset815`: Dataset815_SpineSurgLSTVVerSe, CTSP 802 + VerSeFusion 374 = 1,176 (AUDIT L180-L183).

**Name and citation**

Project dataset (ssn:tools/merge_versefusion_corpus.py).

**Modality**

CT (A2 plus A8).

**Position/view**

Not recorded.

**Licence and access**

Mixed: CC BY-NC-SA 4.0 (CTSP) and VerSe terms.

**How it was acquired**

`ssn:tools/merge_versefusion_corpus.py` (first commit 2026-09-14 [git]), then `ssn:slurm/prep815.sh` (AUDIT L180-L183).

**When**

Built 2026-09-12/13 [doc] (AUDIT L684). Flags repaired 2026-09-23 [doc] (AUDIT L1491-L1494).

**What it contains**

- 1,176 cases (AUDIT L180).
- L6 62 and T13 4 in its manifest; 68 and 6 when read from the volumes (OCT "Denominators"; AUDIT L255-L258, L697).

**Where it is now**

- HOME `spinesurg-ct-nnunet/nnunet/raw/Dataset815_SpineSurgLSTVVerSe` (AUDIT L581).
- CEPH `data/d815_repair` (flags and resplit work, jobs 40416580/81) (LIST 2026-09-23; AUDIT L1491-L1494).

**Annotation status**

Release labels (CTSP), VerSe masks, TS rib pseudolabels (ssn:tools/merge_versefusion_corpus.py docstring).

**Derived products**

None; never trained (AUDIT L180-L183).

**Known defects and gaps**

- Never preprocessed: jobs 40205238 and 40206171 died with singularity not found (AUDIT L180-L183).
- The phenotype flags came from 327 of 374 reports (AUDIT L255-L258).
- The repair was not written into the manifest because "the corpus does not fully decompress" (OCT "Denominators").

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual: GPU job or unset inputs; the submit line is in the steps. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid nnunet_dataset815` prints them. Where the text below differs, `sources.json` is the runnable form.*

Repair 0533 first (done 2026-09-23, AUDIT L1335), then `sbatch slurm/prep815.sh` on a partition where singularity resolves (AUDIT L182-L183).

---

### `ctsp_drr` <a id="ctsp_drr"></a>

**CTSP lateral parallel-beam DRRs (+ ctsp_drr_film).** Cards: A (A18 ctsp_drr). Structured entry: `sources.yaml` id `ctsp_drr`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`ctsp_drr`: lateral parallel-beam DRRs of CTSpinoPelvic1K, plus the film-styled twin `ctsp_drr_film` (CTINV L10; AUDIT L625).

**Name and citation**

Project render bank.

**Modality**

Synthetic render (DRR), lateral, T10 to sacrum (MDMR L309).

**Position/view**

Lateral, one per case (MDMR L309).

**Licence and access**

Inherits CC BY-NC-SA 4.0 (ctsp:README.md L516-L519).

**How it was acquired**

- `ssn:slurm/ctx_build_ctsp.sh`: `tools/make_drr_dataset.py --src nnunet/raw/Dataset813_SpineSurgLSTVFullRibs --dst HOME/ctsp_drr --scheme ds813 --ct-root HOME/data/CTSpinoPelvic1K/ct --prefix CTSP_ --resume`.
- CTs are found by basename (ssn:slurm/ctx_build_ctsp.sh).
- Respaced 2026-09-19 by `--respace` (mem:drr-row-spacing-defect.md).

**When**

- Tool first commit 2026-09-14 [git].
- `HOME/ctsp_drr` mtime 2026-09-22 [listing]; `ctsp_drr_film` 2026-09-17 [listing].
- 0533 re-render job 40416626, 2026-09-23 [doc] (AUDIT L1337, L1375-L1383).

**What it contains**

- 801 renders, ann/img/path (AUDIT L625); 7,161 level instances; 10 levels; L6 instances 18 (MDMR L309).
- Banks rebuilt after 2026-09-23 hold 802 (mem:grid-ct-0533-truncated.md).

**Where it is now**

HOME `ctsp_drr/`, `ctsp_drr_film/` (LIST).

**Annotation status**

Release labels projected to boxes (CTINV L10).

**Derived products**

- allspine banks (7,161 crops), carm_mix (AUDIT L630-L632).
- The "CTSP 120 held-out" sweep pool (AUDIT L634, L912).

**Known defects and gaps**

- Row spacing was wrong on all 801 before the 2026-09-19 respace (the A-P voxel size was written as the S-I row spacing; median error 7.5 %, more than 1.2x off on 172) (mem:drr-row-spacing-defect.md).
- Its naming `CTSP_COLONOG_<token>` versus physics `ctsp_<rel>` put 357 people on both sides of v6/v7 (AUDIT L135-L138; mem:split-leak-cross-naming.md).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): DRR and CT_ROOT on the Ceph layout. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid ctsp_drr` prints them. Where the text below differs, `sources.json` is the runnable form.*

`sbatch -D <ssn checkout> slurm/ctx_build_ctsp.sh` (needs Dataset813 and `HOME/data/CTSpinoPelvic1K/ct`). Verify `ls ann | wc -l` is 802.

---

### `physics_drr` <a id="physics_drr"></a>

**Cone-beam physics renders of CTSP, VerSe, TotalSegmentator v2 and implant CTs (+ _film, cut_physics, cut_physics_v2).** Cards: A (A19 physics_drr). Structured entry: `sources.yaml` id `physics_drr`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`physics_drr`: cone-beam physics renders of CTSP, VerSe, TotalSegmentator v2 and implant CTs, plus `physics_drr_film`, `cut_physics`, `cut_physics_v2` (CTINV L11; AUDIT L627, L689).

**Name and citation**

Project render bank (ssn:tools/render_physics_drr.py docstring).

**Modality**

Synthetic render: perspective, polychromatic, scatter, noise, 640 px (ssn:tools/render_physics_drr.py L1-L19; MDMR L295).

**Position/view**

Per-render pose (view, tilt, rotation, SOD) recorded in each ann; AP 4,052 / lateral 2,993 (MDMR L295).

**Licence and access**

Mixed: inherits each source's terms.

**How it was acquired**

- `STAGE=physics PSCHEME=ctsp|verse|totalseg|implant PSRC=<dir> sbatch --array=… ssn:slurm/fluorocap_v2.sh` runs `tools/render_physics_drr.py --per-case 2 --det-px 640` (ssn:slurm/fluorocap_v2.sh L10, L44).
- `cut_physics` is the CUT translation of physics_drr (ssn:slurm/cut_drr2fluoro.sh L32).

**When**

- Tool first commit 2026-09-14 [git].
- `physics_drr` mtime 2026-09-14 [listing]; `physics_drr_film` 2026-09-17; `cut_physics` 2026-09-15 [listing].

**What it contains**

- 7,045 anns: ctsp 2,430 (798 people), totalseg 1,831, verse 1,463, implant 1,321 (AUDIT L627, L689).
- `cut_physics` and `cut_physics_v2`: 3,000 each (MDMR L299-L300).

**Where it is now**

HOME `physics_drr/`, `physics_drr_film/`, `cut_physics/`, `cut_physics_v2/` (LIST).

**Annotation status**

Source labels projected (CTINV L11).

**Derived products**

Level banks v2-v9 (37,556 crops), carm_mix (AUDIT L631-L632).

**Known defects and gaps**

- CTINV's "CTSpinoPelvic1K / 3,029 subjects" is wrong (AUDIT L645).
- VerSe 282 of 374 and implant 558 of 799 people are covered because of crashes and OOMs (AUDIT L375-L378, L908).
- CTSP 0721, 0919 and 1020 are lost to an unwritten `--min-levels 2` rule (AUDIT L907).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual: GPU job or unset inputs; the submit line is in the steps. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid physics_drr` prints them. Where the text below differs, `sources.json` is the runnable form.*

- Resubmit `STAGE=physics` per scheme with `--resume` semantics (AUDIT L375-L378).
- 0533 only: `ssn:slurm/ctsp0533_physics.sh`.
- Verify ann counts per prefix.

---

### `physics_rare` <a id="physics_rare"></a>

**Rare-anatomy physics oversample (+ physics_rare_film, cut_rare, cut_rare_v2).** Cards: A (A20 physics_rare). Structured entry: `sources.yaml` id `physics_rare`; kind derived; status on_disk; re-acquisition manual (rebuild).

**Source id**

`physics_rare`: rare-anatomy oversample, plus `physics_rare_film`, `cut_rare`, `cut_rare_v2` holding the same 1,482 anns (AUDIT L628).

**Name and citation**

Project render bank.

**Modality**

Synthetic render (physics), AP 879 / lateral 603 (MDMR L306).

**Position/view**

Per-render pose (ssn:tools/render_physics_drr.py).

**Licence and access**

Mixed.

**How it was acquired**

- `ssn:tools/find_rare_cases.py` writes `HOME/FluoroCap/rare_cases_ctsp.txt` (34) and `rare_cases_verse.txt` (56).
- Then `STAGE=physics … PCASES=<file>` (AUDIT L628, L635; ssn:slurm/fluorocap_v2.sh L44).

**When**

`physics_rare` mtime 2026-09-14; `physics_rare_film` 2026-09-18; `cut_rare` 2026-09-15 [listing].

**What it contains**

1,482 anns: 34 CTSP ids (603 renders) + 47 VerSe series (879 renders) (AUDIT L628, L673).

**Where it is now**

HOME (LIST).

**Annotation status**

Source labels projected.

**Derived products**

Level banks (7,602 crops) (AUDIT L631).

**Known defects and gaps**

- 9 of 56 VerSe rare series are missing, including 2 of the 6 T13 scans (AUDIT L380-L383, L957).
- CTINV calls it "81 CTSP subjects" (AUDIT L644, L929).
- 14 of 16 lumbar-rib records are not included (AUDIT L924).

**Re-acquisition recipe**

Resubmit the rare_v arm for the 9 missing series (AUDIT L380-L383).

---

### `verse_drr` <a id="verse_drr"></a>

**VerSe lateral DRRs (+ _film, _obl, _obl2).** Cards: A (A21 verse_drr). Structured entry: `sources.yaml` id `verse_drr`; kind derived; status on_disk; re-acquisition run (rebuild).

**Source id**

`verse_drr`: lateral DRRs of VerSe, plus `verse_drr_film`, `verse_drr_obl` and `verse_drr_obl2` (CTINV L13; AUDIT L668-L670).

**Name and citation**

Project render bank.

**Modality**

Synthetic render. Lateral; obl = 4 oblique poses, obl2 = 8 (MDMR L297, L302).

**Position/view**

Lateral / oblique lateral (MDMR L297, L302, L313).

**Licence and access**

VerSe terms (A7).

**How it was acquired**

`tools/make_drr_dataset.py --scheme verse` over `HOME/VerSeFusion/data/unified` (ssn:tools/make_drr_dataset.py L43-L49; AUDIT L695).

**When**

- `verse_drr` rendered 2026-09-19 12h [doc] (AUDIT L250, L668); mtime 2026-09-20 [listing].
- `verse_drr_film` 2026-09-17; obl and obl2 2026-09-13 [listing].

**What it contains**

- `verse_drr`: 387 anns = 374 + 13 byte-identical `glgl*` duplicates (AUDIT L240-L243).
- `verse_drr_film`: 374; `verse_drr_obl`: 1,494; `verse_drr_obl2`: 2,989 (AUDIT L670; MDMR L297, L302).

**Where it is now**

HOME (LIST).

**Annotation status**

VerSe masks projected, C1-L6 (CTINV L13).

**Derived products**

allspine banks; model card fold bank (940 crops) (AUDIT L678-L679).

**Known defects and gaps**

13 duplicates; the "387" count is repeated across the docs (AUDIT L240-L243, L688).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): --src and --dst on the Ceph layout. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid verse_drr` prints them. Where the text below differs, `sources.json` is the runnable form.*

Delete the `glgl*` files, fix the prefix logic, rerun `make_drr_dataset.py --scheme verse --src HOME/VerSeFusion/data/unified --dst HOME/verse_drr` (AUDIT L242-L243).

---

### `verse_soft_drr` <a id="verse_soft_drr"></a>

**VerSe soft-tissue lateral DRRs.** Cards: A (A22 verse_soft_drr). Structured entry: `sources.yaml` id `verse_soft_drr`; kind derived; status on_disk; re-acquisition manual (rebuild).

**Source id**

`verse_soft_drr`: soft-tissue lateral DRRs of VerSe (CTINV L14).

**Name and citation**

Project render bank.

**Modality**

Synthetic render, lateral.

**Position/view**

Lateral.

**Licence and access**

VerSe terms.

**How it was acquired**

`make_drr_dataset.py`, before the spacing fix (AUDIT L250-L253).

**When**

2026-09-13 [doc] (AUDIT L669); mtime 2026-09-13 [listing].

**What it contains**

374 anns (AUDIT L669).

**Where it is now**

HOME (LIST).

**Annotation status**

VerSe masks.

**Derived products**

`vsoft_fov48_ctx` only (MDMR L314).

**Known defects and gaps**

Row spacing is wrong on 181 of 374 (AUDIT L250-L253).

**Re-acquisition recipe**

Re-render with the current tool, or retire (AUDIT L252-L253).

---

### `ctsp_drr_obl` <a id="ctsp_drr_obl"></a>

**ctsp_drr_obl / ctsp_drr_obl2 (misnamed: VerSe, not CTSP).** Cards: A (A23 ctsp_drr_obl). Structured entry: `sources.yaml` id `ctsp_drr_obl`; kind derived; status on_disk; re-acquisition manual (rebuild).

**Source id**

`ctsp_drr_obl`: `ctsp_drr_obl` and `ctsp_drr_obl2`, misnamed. They are VerSe, not CTSP (MDMR L348-L355).

**Name and citation**

Project render bank.

**Modality**

Synthetic render, oblique lateral (MDMR L301, L307).

**Position/view**

4 poses (obl) and 8 poses (obl2) (MDMR L301, L307).

**Licence and access**

VerSe terms.

**How it was acquired**

Rendered from `HOME/vf_813` under a CTSP prefix (AUDIT L245-L248).

**When**

2026-09-13 [doc] (AUDIT L674); mtime 2026-09-13 [listing].

**What it contains**

1,256 and 2,511 renders of 314 VerSe series, T10-sacrum labels only (AUDIT L674).

**Where it is now**

HOME (LIST).

**Annotation status**

vf_813 labels, with C1-T9 stripped (AUDIT L245-L248).

**Derived products**

allspine v3/v4, extra3/4, films_all3 (AUDIT L245).

**Known defects and gaps**

60 series absent; cervical bodies unlabelled (AUDIT L245-L248, L945).

**Re-acquisition recipe**

Retire. The correct re-renders already exist as `verse_drr_obl` and `verse_drr_obl2` (AUDIT L247-L248).

---

### `ts_drr` <a id="ts_drr"></a>

**TotalSegmentator v2.0.1 lateral DRRs.** Cards: A (A24 ts_drr). Structured entry: `sources.yaml` id `ts_drr`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`ts_drr`: lateral DRRs of TotalSegmentator v2.0.1 (CTINV L15; AUDIT L487).

**Name and citation**

Project render bank (ssn:tools/ts_to_drr.py).

**Modality**

Synthetic render, lateral.

**Position/view**

Lateral.

**Licence and access**

CC BY 4.0 source.

**How it was acquired**

`sbatch ssn:slurm/ts_drr.sh`, which runs `tools/ts_to_drr.py --src HOME/data/TotalSegmentator --dst HOME/ts_drr --workers 16` (ssn:slurm/ts_drr.sh).

**When**

Tool first commit 2026-09-19 [git]; mtime 2026-09-20 [listing].

**What it contains**

1,170 ann + 1,170 img + 1,160 path; 58 of 1,228 skipped (AUDIT L487).

**Where it is now**

HOME (LIST).

**Annotation status**

TS labels mapped by name; ordinary-spine truth only (CTINV L15; ssn:tools/ts_to_drr.py L10-L19).

**Derived products**

`sweep_v3/ts` arms (522 sacrum-anchored + 203 C2-anchored) (AUDIT L495, L498).

**Known defects and gaps**

- The `path/` files were computed from the wrong release (v3) by job 40389325 (AUDIT L225-L228).
- Not held out from the v9 encoder (mem:ts-bench-inside-v9-bank.md).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): SRC and DST on the Ceph layout (the script's defaults are HOME paths). The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid ts_drr` prints them. Where the text below differs, `sources.json` is the runnable form.*

`rm HOME/ts_drr/path/*.npy`, then rerun `slurm/path_render.sh` pointed at the v2 root (AUDIT L228).

---

### `ts_drr_v3` <a id="ts_drr_v3"></a>

**TotalSegmentator v3.0.0 lateral DRRs.** Cards: A (A25 ts_drr_v3). Structured entry: `sources.yaml` id `ts_drr_v3`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`ts_drr_v3`: lateral DRRs of TotalSegmentator v3.0.0 (CTINV L16; AUDIT L488).

**Name and citation**

Project render bank.

**Modality**

Synthetic render, lateral.

**Position/view**

Lateral.

**Licence and access**

Source terms (A10).

**How it was acquired**

`sbatch --export=SRC=HOME/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300,DST=HOME/ts_drr_v3 slurm/ts_drr.sh` (ssn:docs/CONTINUANCE_2026-09-19.md L26).

**When**

Complete 2026-09-19 18:25 [doc] (AUDIT L360); mtime 2026-09-19 [listing].

**What it contains**

1,735 anns; 204 skipped; no `path/` dir (AUDIT L488).

**Where it is now**

HOME (LIST).

**Annotation status**

TS v3 labels mapped by name.

**Derived products**

None. No bank or arm reads it (AUDIT L360-L363).

**Known defects and gaps**

Its anns claim the v201 source string (mem:identity-audit-findings.md; AUDIT L370-L373).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): SRC and DST on the Ceph layout. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid ts_drr_v3` prints them. Where the text below differs, `sources.json` is the runnable form.*

The `ts_drr.sh` line above. Verify 1,735 anns.

---

### `anchor_drr` <a id="anchor_drr"></a>

**AP and lateral anchor-detection renders (8 classes).** Cards: A (A26 anchor_drr). Structured entry: `sources.yaml` id `anchor_drr`; kind derived; status on_disk; re-acquisition manual (rebuild).

**Source id**

`anchor_drr`: AP and lateral anchor-detection renders (YOLO set, 8 classes) (CTINV L19; AUDIT L577).

**Name and citation**

Project render bank (ssn:tools/make_anchor_drr.py).

**Modality**

Synthetic render, AP and lateral (MDMR L293).

**Position/view**

AP 3,921 / lateral 3,921 (MDMR L293).

**Licence and access**

Mixed.

**How it was acquired**

`STAGE=anchor_build|anchor_verse|anchor_ts|anchor_implant* sbatch ssn:slurm/fluorocap_v2.sh`, which runs `tools/make_anchor_drr.py --scheme ctsp|verse|totalseg|implant` (ssn:slurm/fluorocap_v2.sh L35-L43).

**When**

Tool first commit 2026-09-14 [git]; mtime 2026-09-23 [listing]; 0533 added 2026-09-23 [doc] (AUDIT L1375).

**What it contains**

7,842 renders (6,650 train / 1,192 val): CTSP 1,602 (801 × 2), implant 3,036, TS 2,456, VerSe 748 (AUDIT L577, L626, L671).

**Where it is now**

HOME (LIST).

**Annotation status**

Release labels projected to anchor boxes (ssn:tools/make_anchor_drr.py L1-L18).

**Derived products**

`anchor_det_v1` (HOME/FluoroCap/anchor_det_v1.pt) (AUDIT L591).

**Known defects and gaps**

- Its own split puts 301 of 801 people on both sides, because it is seeded on the implant-variant stem (AUDIT L165-L168).
- Its implant CTs are deleted (AUDIT L629).
- It is unkeyed (mem:ct-benchmark-covers-all-collections.md).

**Re-acquisition recipe**

The stages above. Fix the seed to `cid.split('_v')[0]` first (AUDIT L138).

---

### `anchor_drr_c2` <a id="anchor_drr_c2"></a>

**Anchor set with a C2 class (9 classes).** Cards: A (A27 anchor_drr_c2). Structured entry: `sources.yaml` id `anchor_drr_c2`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`anchor_drr_c2`: anchor set with a C2 class (9 classes) (AUDIT L578).

**Name and citation**

Project render bank.

**Modality**

Synthetic render, AP and lateral.

**Position/view**

AP and lateral.

**Licence and access**

Mixed.

**How it was acquired**

`sbatch ssn:slurm/anchor_c2.sh`: render with C2 from CTSP, VerSe and TS v3, then train YOLO11m (ssn:slurm/anchor_c2.sh header).

**When**

Script 2026-09-19/20 [git]; mtime 2026-09-23 [listing].

**What it contains**

6,129 renders (5,195 train / 934 val); 1,043 C2 boxes; 1.7 GB (AUDIT L578). TS v3 1,890 of 1,939 (AUDIT L501).

**Where it is now**

HOME (LIST).

**Annotation status**

Release labels projected.

**Derived products**

`HOME/runs/anchor_c2/v1` (AUDIT L592).

**Known defects and gaps**

The first run died on a missing module but printed DONE (ssn:slurm/anchor_c2.sh header).

**Re-acquisition recipe**

`sbatch slurm/anchor_c2.sh`. Verify 6,129 images.

---

### `implant_ct_synthetic` <a id="implant_ct_synthetic"></a>

**Synthetic hardware CTs: implant_ct (CTSP, deleted), implant_verse, implant_ts.** Cards: A (A28 implant_ct_synthetic). Structured entry: `sources.yaml` id `implant_ct_synthetic`; kind derived; status on_disk_partial; re-acquisition submit (rebuild).

**Source id**

`implant_ct_synthetic`: synthetic hardware CTs `implant_ct` (CTSP), `implant_verse` and `implant_ts` (MDMR L186-L188).

**Name and citation**

Project-generated (ssn:tools/make_implant_ct.py).

**Modality**

CT, synthetic: real volumes with inserted hardware (MDMR L186).

**Position/view**

As the sources.

**Licence and access**

Inherits source terms.

**How it was acquired**

`STAGE=implant_build|implant_verse|implant_ts sbatch ssn:slurm/fluorocap_v2.sh`, which runs `tools/make_implant_ct.py --variants 2|3|2` (ssn:slurm/fluorocap_v2.sh L39-L41).

**When**

Tool 2026-09-14 [git]. `implant_ts` and `implant_verse` mtime 2026-09-14 [listing].

**What it contains**

- `implant_ct`: 1,518 constructs over 799 people, 427 GB (AUDIT L903; MDMR L186).
- `implant_verse`: 1,119 = 373 × 3, 187 GB (MDMR L187).
- `implant_ts`: 1,629 over 817 subjects, 39 GB (AUDIT L494; MDMR L188).

**Where it is now**

- HOME `implant_verse/`, `implant_ts/`, and the smoke dirs (LIST).
- `implant_ct` no longer exists (AUDIT L629, L649).

**Annotation status**

Source labels plus hardware ids.

**Derived products**

physics_drr implant renders, anchor_drr implant renders (AUDIT L626-L629).

**Known defects and gaps**

- 0394 and 0405 produced nothing (AUDIT L909).
- `implant_ts` is unfinished: 355 subjects never processed (AUDIT L365-L368).
- verse116 is missing (AUDIT L956).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual: GPU job or unset inputs; the submit line is in the steps. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid implant_ct_synthetic` prints them. Where the text below differs, `sources.json` is the runnable form.*

The stages above, with a resume guard (AUDIT L367-L368).

---

### `lstv_flag_renders` <a id="lstv_flag_renders"></a>

**LSTV flag renders: lstv_flag/renders (CTSP), renders_verse, renders_ctrl.** Cards: A (A29 lstv_flag_renders). Structured entry: `sources.yaml` id `lstv_flag_renders`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`lstv_flag_renders`: `HOME/lstv_flag/renders` (CTSP), `renders_verse` and `renders_ctrl` (MDMR L294, L298, L312).

**Name and citation**

Project render bank (ssn:tools/lstv_flag_render.py; ssn:tools/lstv_flag_render_verse.py).

**Modality**

Synthetic render, AP and lateral, 512 px PNG (MDMR L294).

**Position/view**

6 poses (MDMR L298).

**Licence and access**

Mixed.

**How it was acquired**

`ssn:slurm/lstv_flag_render.sh`: `tools/lstv_flag_render.py --src HOME/data/CTSpinoPelvic1K`, 8 shards (AUDIT L637).

**When**

Tools 2026-09-15 [git]; mtime 2026-09-15 [listing]; 0533 job 40416638 on 2026-09-23 [doc] (AUDIT L1337).

**What it contains**

- `renders`: 9,612 renders over 801 cases.
- `renders_verse`: 3,456 over 288 series.
- `renders_ctrl`: 644 over 161 (MDMR L294, L298, L312).

**Where it is now**

HOME `lstv_flag/` (LIST).

**Annotation status**

- Release labels.
- Transitional labels in `HOME/lstv_flag/lstv_flag_labels_v2.csv` (1,113 spines) (mem:anomaly-manifest-sources.md).

**Derived products**

LSTV and TLTV flag models (MDMR Surface K).

**Known defects and gaps**

37 VerSe series are lost to a subject/series join defect (AUDIT L943, L953).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual: GPU job or unset inputs; the submit line is in the steps. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid lstv_flag_renders` prints them. Where the text below differs, `sources.json` is the runnable form.*

`sbatch slurm/lstv_flag_render.sh` (ssn).

---

### `spinalai_drr` <a id="spinalai_drr"></a>

**Spinal-AI2024 converted to the render layout (film-derived, not CT).** Cards: A (A30 spinalai_drr). Structured entry: `sources.yaml` id `spinalai_drr`; kind derived; status on_disk; re-acquisition run (rebuild).

**Source id**

`spinalai_drr`: a film-derived bank, not CT. It sits in this family only because it is named with the render banks; the film family owns the source (MDMR L175, L291).

**Name and citation**

Spinal-AI2024, AI-generated by the CurvNet data engine, arXiv 2411.12604 (MDMR L175).

**Modality**

Plain film (synthetic, AI-generated), AP (MDMR L291).

**Position/view**

AP (MDMR L291).

**Licence and access**

Not recorded in the files read.

**How it was acquired**

`ssn:tools/spinal_ai2024_to_render.py --src HOME/spine-detector/data/raw/spinal_ai2024/repo --dst …`, keeping films with exactly 17 bodies (AUDIT L573-L574; ssn:slurm/recount_aasce_skips.sh L22).

**When**

Tool 2026-09-17 [git]; mtime 2026-09-16 [listing].

**What it contains**

8,358 renders over 44 synthetic identities; source 20,000 jpg (MDMR L291, L355-L357; AUDIT L573).

**Where it is now**

HOME `spinalai_drr/` (LIST).

**Annotation status**

Assumed T1-L5 naming, "NOT verified" (MDMR L291).

**Derived products**

None. No bank uses it (MDMR L291).

**Known defects and gaps**

Pose multiplication: 44 identities under 8,358 renders (mem:ct-benchmark-covers-all-collections.md).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): --dst on the Ceph layout. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid spinalai_drr` prints them. Where the text below differs, `sources.json` is the runnable form.*

The converter command above.

---

### `aasce_drr` <a id="aasce_drr"></a>

**AASCE training films converted to the render layout (film-derived, not CT).** Cards: A (A31 aasce_drr). Structured entry: `sources.yaml` id `aasce_drr`; kind derived; status on_disk; re-acquisition run (rebuild).

**Source id**

`aasce_drr`: a film-derived bank, not CT; cross-family (AUDIT L571).

**Name and citation**

AASCE 2019 / BoostNet, GitHub mirror zlinzju/ke30_u7_AASCE2019 (AUDIT L566).

**Modality**

Plain film, AP (MDMR L308).

**Position/view**

AP.

**Licence and access**

Mirror MIT (AUDIT L566).

**How it was acquired**

`ssn:tools/aasce_to_drr.py --src HOME/spine-detector/data/raw/aasce --dst HOME/aasce_drr` (ssn:tools/aasce_to_drr.py L23).

**When**

mtime 2026-09-15 [listing].

**What it contains**

457 of 481 training films (AUDIT L571).

**Where it is now**

HOME `aasce_drr/` and `aasce_fov96_ctx/` (LIST). The complete 609-film mirror is at CEPH `data/thoracic_xr` (AUDIT L572).

**Annotation status**

Release landmarks; T1-L5 is assumed (ssn:tools/aasce_to_drr.py L9-L19).

**Derived products**

`aasce_fov96` → allspine_v4 (MDMR L308; AUDIT L587).

**Known defects and gaps**

128 labelled test films never reached it (AUDIT L335-L338).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): --src the re-acquired mirror, --dst the Ceph layout. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid aasce_drr` prints them. Where the text below differs, `sources.json` is the runnable form.*

Rerun the converter on the CEPH mirror (AUDIT L335-L338).

---

### `xrspinopelvic1k` <a id="xrspinopelvic1k"></a>

**XRSpinoPelvic1K: this project's DRR dataset repo (includes the xrsp1k lateral DRRs, carded by family A as xrsp1k_drr).** Cards: A (A32 xrsp1k_drr), D (D16 XRSpinoPelvic1K (this project's DRR dataset repo)), E (xrsp1k_drr). Also known as: `xrsp1k_drr`. Structured entry: `sources.yaml` id `xrspinopelvic1k`; kind project_release; status on_disk; re-acquisition manual (rebuild).

**Source id**

*[A: card `xrsp1k_drr`]*

`xrsp1k_drr`: lateral DRRs of the April-era CTSP export inside XRSpinoPelvic1K. Cross-family; the film family covers the rest of `HOME/XRSpinoPelvic1K` (MDMR L197-L200).

*[D]*

`xrspinopelvic1k`

*[E: card `xrsp1k_drr`]*

`xrsp1k_drr`

**Name and citation**

*[A: card `xrsp1k_drr`]*

XRSpinoPelvic1K. MEMORY.md's index entry for mem:schwingnet-disclosure-scrub.md says it is private.

*[D]*

XRSpinoPelvic1K, "an open spinal-radiograph (DRR) dataset + real-time vertebral-level localization, generated from
segmented CT", GitHub `Gregory-Schwing-MD-PhD/XRSpinoPelvic1K` (xrsp:README.md; `git remote -v` of the local clone).
The repository was made private (mem:schwingnet-disclosure-scrub.md line 18). No DOI.

*[E: card `xrsp1k_drr`]*

XRSpinoPelvic1K DRRs: 6,416 lateral DRRs of 822 CTSpinoPelvic1K cases, with end-plate corners keyed by level name (`MANIFEST_DATA_MODELS_RESULTS.md` 2.3)

**Modality**

*[A: card `xrsp1k_drr`]*

Synthetic render, lateral (MDMR L197-L200).

*[D]*

Synthetic render: parallel-beam DRRs (lateral and AP; `--oblique N` random oblique views) of CTSpinoPelvic1K CT with
2-D masks and per-level landmarks projected from the 3-D labels (xrsp:docs/dataset_card.md; xrsp:README.md). The repo
also stages real BUU-LSPINE films for validation (cards D03, D04).

*[E: card `xrsp1k_drr`]*

synthetic render (lateral DRR) of CT

**Position/view**

*[A: card `xrsp1k_drr`]*

Lateral.

*[D]*

Lateral, AP and oblique projections of supine CT (xrsp:README.md, "CTSpinoPelvic1K is supine CT").

*[E: card `xrsp1k_drr`]*

lateral (`MANIFEST_DATA_MODELS_RESULTS.md` 2.3)

**Licence and access**

*[A: card `xrsp1k_drr`]*

Private (MEMORY.md index, schwingnet-disclosure-scrub entry).

*[D]*

Code Apache-2.0; rendered DRRs inherit the source CT's terms (the card says CC BY-NC 4.0 for CTSpinoPelvic1K)
(xrsp:docs/dataset_card.md). The BUU data inside it is not redistributable (xrsp:.gitignore).

*[E: card `xrsp1k_drr`]*

project-built from ctspinopelvic1k; terms follow the CT release

**How it was acquired**

*[A: card `xrsp1k_drr`]*

Not recorded in the files read.

*[D]*

Generated, not downloaded: `python -m xrsp.build_dataset --ct_dir data/ct --label_dir data/labels --out data/xrsp1k
--oblique 8` (xrsp:README.md quick start; grid wrappers `xrsp:slurm/xrsp_generate.sh`, `xrsp:scripts/gen_xrsp1k.slurm`).

*[E: card `xrsp1k_drr`]*

rendered by this project; the tool is not named in Family E's evidence

**When**

*[A: card `xrsp1k_drr`]*

`HOME/XRSpinoPelvic1K` mtime 2026-08-10 [listing].

*[D]*

Repo initial commit 2026-06-24; 124 commits up to 2026-08-15 (`git log` of the local clone). `~/XRSpinoPelvic1K`
directory date 2026-08-10 (census:toplevel_listing.txt). YOLO sweep weights dated 2026-08-13
(sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 5.3).

*[E: card `xrsp1k_drr`]*

`~/XRSpinoPelvic1K` is dated 2026-08-10 in the listing

**What it contains**

*[A: card `xrsp1k_drr`]*

6,416 lateral DRRs of 822 cases, with endplate corners keyed by level (MDMR L197-L200).

*[D]*

`~/XRSpinoPelvic1K` 32 GB on 2026-09-01 (census:_du_home.txt). `data/xrsp1k`: 6,416 lateral DRRs of 822 cases with
end-plate corners keyed by level name (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.3); `data/BUU-LSPINE` and
`data/dataset2024.zip` (card D03); `data/runs/yolo_exp/*/weights/` (7 runs, 14 files) (same, section 5.3); an HF Space
annotation tool for femoral heads under `annot/` (git log 2026-08-09..15).

*[E: card `xrsp1k_drr`]*

6,416 DRRs; the whole `~/XRSpinoPelvic1K` tree was 32G on 2026-09-01 (`_du_home.txt`)

**Where it is now**

*[A: card `xrsp1k_drr`]*

HOME `XRSpinoPelvic1K/data/xrsp1k`; the whole directory is 32 GB (DUH).

*[D]*

- HOME: `~/XRSpinoPelvic1K` (census:toplevel_listing.txt).
- LOCAL: `xrsp:` (repo + `dataset2024.zip` + `Spondylolisthesis Vertebral Landmark.zip` + the PLOS One PDF).

*[E: card `xrsp1k_drr`]*

`~/XRSpinoPelvic1K` (HOME, raw, 32.0 GB, listing 2026-08-10)

*[2026-10-08: `~/dis_renders`, read on the grid]*

`~/dis_renders`: five PNGs named by BUU-LSPINE film ids (`0008-M-022Y1`, `0012-F-013Y1`, `0013-M-022Y1`, `0015-M-020Y1`, `0016-F-023Y1`), 10,869,856 B, dated 2026-08-11 12:52 (scr:inspect_unknown.out). What drew them is not recorded; `~/spinesurg-ct-nnunet/disputed_renders` holds VerSe PNGs, not these. It moves in batch B14 to `$RS/data/xrspinopelvic1k/derived/dis_renders`, owner-only, and is a deletion candidate.

**Annotation status**

*[A: card `xrsp1k_drr`]*

Release labels projected to corners (MDMR L197-L200).

*[D]*

Pseudo-labels: machine-projected from the 3-D release labels of the CT source it was built from; femoral-head reader
annotations through the HF Space (status not recorded) (xrsp:README.md; xrsp: git log).

*[E: card `xrsp1k_drr`]*

level-keyed end-plate corners from the CT labels

**Derived products**

*[A: card `xrsp1k_drr`]*

Not recorded.

*[D]*

`xrsp:scripts/drr_to_yolo.py` YOLO sets with a pelvis class, the heatmap landmark model, YOLO-pose baselines
(xrsp: git log 2026-08-08/09). `tools/xrsp1k_to_nnunet.py` in the main repo (git 2026-06-29)
(sscn:tools/xrsp1k_to_nnunet.py).

*[E: card `xrsp1k_drr`]*

none found in the disk map

**Known defects and gaps**

*[A: card `xrsp1k_drr`]*

`data/ct` and `data/labels` are dangling symlinks to the deleted `hf_export_v3` (MDMR L197-L200).

*[D]*

- `data/ct` and `data/labels` are dangling symlinks to `CTSpinoPelvic1K/data/hf_export_v3`, which no longer exists (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.1).
- Built from 822 cases of `hf_export_v3`, an export that predates the 802-record v11 release; a rebuild from v11 must resolve label names through `ostk.labels.labels_for(volume)`, never a fixed map (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 2.3 and 7.1; ctsp:CLAUDE.md "two label schemes").
- The YOLO sweep's `results.csv` were never opened (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.2).

*[E: card `xrsp1k_drr`]*

`data/ct` and `data/labels` are dangling symlinks to the deleted `CTSpinoPelvic1K/data/hf_export_v3` (`MANIFEST_DATA_MODELS_RESULTS.md` 7.1)

*[2026-10-08: `~/dis_renders`, read on the grid]*

The five `~/dis_renders` PNGs carry BUU film ids, so they are treated as holding BUU pixels under the BUU EULA (owner-only on Ceph; LAYOUT.md rule 8).

**Re-acquisition recipe**

*[A: card `xrsp1k_drr`]*

Not recorded.

*[D]*

Clone the private repo; point `data/ct` and `data/labels` at the v11 tree (`~/data/CTSpinoPelvic1K/{ct,labels}`); run
`python -m xrsp.build_dataset --ct_dir data/ct --label_dir data/labels --out data/xrsp1k --oblique 8` as an sbatch job;
stage BUU with `xrsp:scripts/fetch_buu.py`. Verify: one output set per CT, the PI = SS + PT identity test
(`make test`, 14 tests) (xrsp:README.md).

*[E: card `xrsp1k_drr`]*

re-render from ctspinopelvic1k with the XRSpinoPelvic1K renderer (not identified here)

---

### `polypose_synthetic` <a id="polypose_synthetic"></a>

**PolyPose cohort: synthetic curvature variants of held CTs within Panjabi and LSTV ranges.** Cards: E (polypose_synthetic). Structured entry: `sources.yaml` id `polypose_synthetic`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`polypose_synthetic`

**Name and citation**

PolyPose cohort: generative poses within Panjabi and LSTV ranges (`mem:polypose-decision`; `mem:polypose-generator-build`)

**Modality**

synthetic render of CT under sampled poses

**Position/view**

sampled per render

**Licence and access**

project-built

**How it was acquired**

`nnunet:slurm/polypose_cohort.sbatch` and `polypose_check.sh` (BANK default `$RS/data/polypose`)

**When**

`$RS/data/polypose` is dated 2026-09-23 and `~/polypose` 2026-09-23 in the listing

**What it contains**

Cohort size and item count: not recorded until the census reports the `data/polypose` subfolders. The 82 GB of `CENSUS_TABLE_2026-09-25.md` 4 is the total of the whole Ceph `data/polypose` folder, which also holds the PolyPose venv and sif (`slurm/env/polypose.setup_status.json`: venv `data/polypose/env/venv`, sif `data/polypose/sif/polypose_base.sif`) and the DeepFluoro Hugging Face copy carded as `deepfluoro_xvr_hf` (`data/polypose/hf/hub/`); it does not measure the cohort.

**Where it is now**

`~/polypose` (HOME, converted/derived, listing 2026-09-23); `$RS/data/polypose` (CEPH, converted/derived, 82.0 GB, listing 2026-09-23)

**Annotation status**

inherits the CT labels

**Derived products**

none found in the disk map

**Known defects and gaps**

not recorded in Family E's evidence

**Re-acquisition recipe**

`sbatch slurm/polypose_cohort.sbatch` (arguments not read here)

---

### Family A notes after the cards (verbatim)

### Migration hazards for this family (read before moving anything to CEPH)

1. **Symlinks that break on a move.**
   - The Dataset810, 813 and 815 `imagesTr` links point at the container path `/data/hf_export/ct/…`. Never rewrite them; bind `HF_EXPORT_DIR` to the CT root instead (mem:dataset813-image-links-are-container-paths.md).
   - `HOME/bench/ct_by_case` is 802 symlinks (MDMR L200-L202).
   - `HOME/VerSeFusion/data/unified` is 88 MB of links (AUDIT L662).
   - Whether these links are absolute or relative is not recorded. Run `find <dir> -type l -lname '/*'` before moving.
2. **Hard links.** The CT store in `HOME/data/CTSpinoPelvic1K/ct` was kept "as hard links in the working copy before any export tree goes". Export trees over-count the hard-linked CTs (RECLAIM L56, L78). A copy across filesystems breaks the hard links and doubles the bytes.
3. **Absolute paths in tools.** `ssn:slurm/ctx_build_ctsp.sh`, `ssn:slurm/ts_drr.sh`, `ssn:slurm/fluorocap_v2.sh` and `ssn:slurm/other_ct_fetch.sh` default to HOME paths such as `$HOME/data/CTSpinoPelvic1K/ct`, `$H/data/TotalSegmentator` and `$HOME/data/ribs`. Leave symlinks at the old HOME paths, or change the defaults.
4. **The patient-key store.** `HOME/patient_keys_final.json` (ssn:SchwingNet/results/rare_class/split_plan.md) and `HOME/ts_dupscan_out/ct_fingerprints.json` (AUDIT L496) are identity tables. Move them with their consumers.
5. **World-writable directory.** CEPH `data/ctsp_april` is `drwxrwxrwx` (LIST).

## 6. Family B: the anomaly-harvest CT acquisitions

The family's own preface, legend and shared notes, verbatim:

Scope: every collection in the acquisition census of 2026-09-23/24 (`ranking.csv`, 146 rows), the 500-person NLST
pilot and the 70-CT validation set that ran through the same chain. These are the CTs fetched to find transitional
spines (L6, four lumbar, T13) that can be counted, plus every collection that was ranked and not fetched, with the reason.
Written 2026-10-07 from files on this machine only; no grid or network access. Generated by
`scratchpad/dataplan/make_family_b.py` (session scratch folder; script not preserved: not recorded) from `ranking.csv`, the three manifests, the Zenodo sweep and the addendum; the
hand-written fields carry their own citations.

### How to read the citations and paths

- A path in parentheses without a prefix is relative to `<repo spinesurg-ct-nnunet 097933a>/`.
- `acquisition/...` means `spinesurg-ct-nnunet/SchwingNet/results/transitional_registry/acquisition/...`.
- `listing` means the top-level listing of HOME, HOME/data, the Ceph root, Ceph `data/`, `data/anomaly_harvest/` and
  `archive/` taken 2026-10-07: `<session scratchpad; not a dependency>/census/toplevel_listing.txt`.
  Its dates are directory modification times, not acquisition dates. `scratchpad census/_du_*.txt` are the du files
  of 2026-09-01 in the same folder.
- `memory/...` means `<memory notes; see MEMORY.md>/...`.
- HOME = `/wsu/home/go/go24/go2432` (Panasas). CEPH = `/rs/rs_grp_oschome/go2432` (`RS` in TIERS.md).
- Status words: **fetched** (on CEPH), **fetching** (none at the latest record: every acquisition job was cancelled
  or finished by 2026-09-27 15:50 EDT, docs/grid_records/JOBS_RECORD_2026-09-27_1544.md), **planned** (ranked, open, not fetched; qualifier held / deferred /
  unresolved overlap / tier 2), **gated**, **excluded** (licence, or no new countable people).
- "Catalogue GB" is what the census computed from IDC/NBIA/HF/Zenodo listings (acquisition/ranking.csv `fetch_gb`). "On disk" is
  `du -sBG` of 2026-09-25: raw = `data/<collection>` (raw plus converted NIfTI), seg = the screen's `seg` and
  `spineps` folders (docs/CENSUS_TABLE_2026-09-25.md caveats).
- The storage census job 40578909 (`data/inventory/census_2026-10-07/`) had not reported when this was written, so
  every on-disk number here is from 2026-09-25 or 2026-09-27 and should be re-checked against it.

### What every acquired collection shares (read once)

**The chain.** `slurm/acquisition_submit.sh <target>` submits, per collection, fetch -> convert (array) -> cases -> ts
(GPU) -> gate -> gate-merge -> spineps (GPU, gated cases only) -> call -> summary, chained with `afterany`; each stage
skips finished work, so rerunning the same command resumes (slurm/acquisition_submit.sh). Targets: `env`, `validation`, `tier1`,
`tier1_late`, `tier2` (written, never submitted), `dedupe`. The grid copy of the job log is
`/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition/jobs.txt` with logs in `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition/logs/` (acquisition/jobs.txt).

**Fetch routes** (`tools/acquisition_fetch.py`, one route per call, wrapped by `slurm/acquisition_fetch.sh`,
partition reqp, QoS requeue, 4-day limit; nothing is signed, registered or logged into) (tools/acquisition_fetch.py, slurm/acquisition_fetch.sh):

| route | source | unit | verified by |
|---|---|---|---|
| idc | NCI IDC public buckets via idc-index 0.12.5 + `s5cmd sync` | series | .dcm count = manifest instanceCount |
| nbia | TCIA NBIA REST v1 `getImage` | series | zip unpacks, instance count = manifest |
| hf | Hugging Face dataset (ungated), `resolve/main` | LFS file | LFS sha256 from the Hub listing |
| zenodo | Zenodo record API | archive | the record's md5, then every member's CRC on unpack |
| s3 | public S3, `--no-sign-request` | object | size = listing |

Every route was smoke-tested on one unit on 2026-09-23 (job 40425969: IDC 2/2, NBIA 1/1, Zenodo md5 1/1, HF sha256
1/1) (acquisition/jobs.txt). The fetcher refuses to start a unit when the oschome group quota has under 5 TB free (`df-ceph oschome`)
(tools/acquisition_fetch.py `guard_space`).

**Layout on CEPH** (tools/acquisition_fetch.py, tools/acquisition_screen.py):

| path | what |
|---|---|
| `/rs/rs_grp_oschome/go2432/data/<collection>/raw/` | unpacked source data: IDC `raw/<collection_id>/<PatientID>/<SeriesUID>/`, NBIA `raw/<PatientID>/<SeriesUID>/`, Zenodo `raw/<record>/...`, HF `raw/...` |
| `/rs/rs_grp_oschome/go2432/data/<collection>/fetch/` | `verified.jsonl` (one line per verified unit), `failed.jsonl`, `FETCH_STATUS.json`; archives are deleted after unpack unless `--keep-archives` |
| `/rs/rs_grp_oschome/go2432/data/<collection>/nifti/<case>_ct.nii.gz` | conversions of DICOM and MHA sources; NIfTI sources are used in place and not copied |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/<collection>/` | the two-labeller screen (cases.csv, seg/, labeller_b/, gate.csv, spineps/, calls/, review/, rows.csv, registry_rows.csv, SUMMARY.md) |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition/` | manifests, jobs.txt, logs, `alias_pairs.csv`, `alias_pairs_all.csv` |

Case ids: `<prefix>_<collection>_<PatientID>` for IDC, `<prefix>_<person>` otherwise; patient key
`<corpus>:<source subject id>` with the rule recorded per case (tools/acquisition_screen.py `convert_items`, `patient_key`). Convert measures
slice spacing from positions, refuses spacing over 3 mm, never reorients on write, and stores a pixel sha1 and a 16^3
thumbnail for cross-collection duplicate search (tools/acquisition_screen.py, acquisition/ACQUISITION_PLAN.md section 6).

**Annotation, for every acquired CT.** Two pseudo-labellers and a combined call; no radiologist read
(acquisition/ACQUISITION_PLAN.md sections 6 and 9). Release labels were excluded at fetch or convert wherever the include/exclude patterns say so
(slurm/acquisition_submit.sh). Transitional rows from these screens are not in `registry.csv` (its acquisition stream is "no rows.csv: not a
row stream", SchwingNet/results/transitional_registry/REGISTRY.md); they live in each collection's `rows.csv` and
`registry_rows.csv` on CEPH and were joined into the ruleclass tier lists as flag source R20 (docs/ruleclass/TIERS.md section 2).

**Defects that apply to the whole family.**
- `docs/CENSUS_TABLE_2026-09-25.md` reports every "CTs on disk" and "FOV gate pass" figure one higher than the
  matching count elsewhere: AMOS 724 vs 723, NLST 501/499 vs 500/498, CTPelvic1K 173/7 vs 172/6, CSI 21/21 vs 20/20,
  validation 71/70 vs 70/69, and the 12 other collections against TIERS.md (FDG 901 vs 900, IDC 3,500 vs 3,499,
  AbdomenAtlas 7,650 vs 7,649, ...). PANORAMA is the one exception (2,026 vs 2,024 two days later). A counted header
  line would explain it, but the grid query behind the table is not on disk, so the cause is not confirmed
  (docs/CENSUS_TABLE_2026-09-25.md; acquisition/collections/*/SUMMARY.md; acquisition/validation/SUMMARY.md; docs/ruleclass/TIERS.md section 1). The CNS 2026 table
  copies those figures (`CTSpinoPelvic1K-1/paper/cns2026/prep_v8_table.py`: 7650, 2026, 724).
- `docs/DATA_COMPLETENESS_AUDIT.md` has no section on any family-B collection, so none of these sources has had the
  release -> disk -> used audit the other families had (docs/DATA_COMPLETENESS_AUDIT.md headings).
- Only csi2014, ctpelvic1k_clinic, nlst_pilot and the validation set had `SUMMARY.md` and rows copied into the
  repository; the rest exist only on CEPH (acquisition/ACQUISITION_PLAN.md "Files here"; acquisition/collections/).
- The landing dedupe outputs (`alias_pairs.csv`, `alias_pairs_all.csv`) are not in the repository; the only
  duplicate facts on local disk are the exact-sha1 folds and alias-candidate counts in TIERS.md (acquisition/jobs.txt; docs/ruleclass/TIERS.md).
- No acquired CT carries a patient position, and none was extracted; the planned database needs it read from DICOM
  (0018,5100) or the release metadata (acquisition/manifests/idc_tier1.csv header; tools/acquisition_screen.py).
- The fetch tool's first git commit (2026-09-24, 8d6a4f4) postdates its first use (2026-09-23), so the exact code that
  fetched tier 1 is not separately recorded; the plan says the grid copy was checked by md5 against the repository
  after the 2026-09-24 changes (git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4; acquisition/ACQUISITION_PLAN.md section 6).

### Summary of every source in this family

`ranking.csv` holds 146 rows: tier 1 first launch 45 (39 IDC collections, FDG-PET-CT-Lesions, AbdomenAtlas 3.0 Mini, two
AMOS rows, CSI 2014, CTPelvic1K clinical), tier 1 late 10, CT Colonography held 1, tier 2 17, deferred or unresolved 7,
gated 7, no new countable people or excluded 59 (acquisition/ranking.csv; the generator recomputes these counts from the file and stops if they differ).
The 148 cards below are those rows (the two AMOS rows share one card) plus the IDC route card, the NLST pilot and the
validation set. Fetched n = units verified and CTs usable after convert (cases.csv,
docs/ruleclass/TIERS.md 2026-09-27) where known. GB = catalogue / on-disk raw + screen (du 2026-09-25).

| source id | group | route | listed n | fetched n | GB | status | note |
|---|---|---|---:|---|---|---|---|
| `idc_tier1` | B1 | idc | 3,600 series (39 collections) | 3,600 series verified; 3,499 CTs usable | 463 / 658 + 55 | fetched | route card |
| `idc_hcc_tace_seg` | B1 | idc | 105 | 101 series verified | 5 | fetched | converted count pooled |
| `idc_pancreatic_ct_cbct_seg` | B1 | idc | 40 | 40 series verified | 2.9 | fetched | converted count pooled |
| `idc_tcga_kirc` | B1 | idc | 237 | 129 series verified | 9.7 | fetched | converted count pooled |
| `idc_colorectal_liver_metastases` | B1 | idc | 197 | 80 series verified | 6.2 | fetched | converted count pooled |
| `idc_ct_vs_pet_ventilation_imaging` | B1 | idc | 20 | 20 series verified | 1.8 | fetched | converted count pooled |
| `idc_tcga_lihc` | B1 | idc | 75 | 42 series verified | 4.9 | fetched | converted count pooled |
| `idc_adrenal_acc_ki67_seg` | B1 | idc | 53 | 29 series verified | 3.5 | fetched | converted count pooled |
| `idc_eay131` | B1 | idc | 2,653 | 376 series verified | 36.4 | fetched | converted count pooled |
| `idc_cmb_mel` | B1 | idc | 32 | 23 series verified | 2.1 | fetched | converted count pooled |
| `idc_tcga_stad` | B1 | idc | 46 | 45 series verified | 6.3 | fetched | converted count pooled |
| `idc_cmb_ov` | B1 | idc | 17 | 7 series verified | 1 | fetched | converted count pooled |
| `idc_pediatric_ct_seg` | B1 | idc | 359 | 352 series verified | 55.6 | fetched | converted count pooled |
| `idc_anti_pd_1_lung` | B1 | idc | 46 | 34 series verified | 4.2 | fetched | converted count pooled |
| `idc_cptac_ucec` | B1 | idc | 75 | 66 series verified | 10.3 | fetched | converted count pooled |
| `idc_cmb_brca` | B1 | idc | 25 | 21 series verified | 2.5 | fetched | converted count pooled |
| `idc_tcga_blca` | B1 | idc | 107 | 79 series verified | 10 | fetched | converted count pooled |
| `idc_cptac_pda` | B1 | idc | 99 | 62 series verified | 9.8 | fetched | converted count pooled |
| `idc_psma_pet_ct_lesions` | B1 | idc | 378 | 374 series verified | 61.7 | fetched | converted count pooled |
| `idc_tcga_ucec` | B1 | idc | 65 | 38 series verified | 4.1 | fetched | converted count pooled |
| `idc_ctpred_sunitinib_pannet` | B1 | idc | 38 | 34 series verified | 6 | fetched | converted count pooled |
| `idc_cptac_ccrcc` | B1 | idc | 64 | 48 series verified | 7.7 | fetched | converted count pooled |
| `idc_cmb_crc` | B1 | idc | 44 | 30 series verified | 5.3 | fetched | converted count pooled |
| `idc_acrin_flt_breast` | B1 | idc | 80 | 15 series verified | 2.8 | fetched | converted count pooled |
| `idc_cmb_mml` | B1 | idc | 61 | 16 series verified | 2.3 | fetched | converted count pooled |
| `idc_tcga_ov` | B1 | idc | 143 | 24 series verified | 2.4 | fetched | converted count pooled |
| `idc_cmb_lca` | B1 | idc | 92 | 75 series verified | 9.8 | fetched | converted count pooled |
| `idc_mediastinal_lymph_node_seg` | B1 | idc | 513 | 316 series verified | 25.1 | fetched | converted count pooled |
| `idc_lung_pet_ct_dx` | B1 | idc | 355 | 158 series verified | 29.2 | fetched | converted count pooled |
| `idc_varepop_apollo` | B1 | idc | 38 | 35 series verified | 5.4 | fetched | converted count pooled |
| `idc_tcga_esca` | B1 | idc | 16 | 16 series verified | 2.4 | fetched | converted count pooled |
| `idc_covid_19_ny_sbu` | B1 | idc | 458 | 443 series verified | 63.1 | fetched | converted count pooled |
| `idc_acrin_nsclc_fdg_pet` | B1 | idc | 242 | 131 series verified | 15.4 | fetched | converted count pooled |
| `idc_cptac_stad` | B1 | idc | 19 | 19 series verified | 6.9 | fetched | converted count pooled |
| `idc_cptac_cm` | B1 | idc | 12 | 12 series verified | 4.1 | fetched | converted count pooled |
| `idc_cptac_sar` | B1 | idc | 18 | 14 series verified | 3 | fetched | converted count pooled |
| `idc_pelvic_reference_data` | B1 | idc | 58 | 58 series verified | 4.4 | fetched | converted count pooled |
| `idc_midrc_ricord_1a` | B1 | idc | 110 | 98 series verified | 6.5 | fetched | converted count pooled |
| `idc_rider_lung_pet_ct` | B1 | idc | 220 | 117 series verified | 18.1 | fetched | converted count pooled |
| `idc_covid_19_ar` | B1 | idc | 23 | 23 series verified | 5.5 | fetched | converted count pooled |
| `tcia_fdg_pet_ct_lesions` | B1 | nbia | 900 | 900 series; 900 CTs | 250.6 / 367 + 31 | fetched |  |
| `abdomenatlas3_mini` | B1 | hf | 9,262 | 40/40 tars; 7,649 CTs | 570.7 / 532 + 107 | fetched |  |
| `amos22` | B1 | zenodo | 2,400 (1,900 + 500) | 5/5 zips; 723 CTs | 102.6 / 96 + 13 | fetched | two ranking rows |
| `nlst_pilot` | B1 | idc | 500 | 500 series; 500 CTs | 45.8 / 69 + 7 | fetched |  |
| `ctpelvic1k_clinic` | B1 | zenodo | 178 | 2/2 archives; 172 CTs | 14.8 / 14 + 5 | fetched |  |
| `csi2014` | B1 | zenodo | 20 | 20/20; 20 CTs | 3.6 / 7 + 3 | fetched |  |
| `validation_ts` | B2 | symlink | 70 | 70 CTs | 1 + 2 | fetched | links into HOME TotalSegmentator v2 |
| `panorama` | B3 | zenodo | 2,224 | 2,024 CTs (screen incomplete) | 194.2 / 182 + 16 | fetched |  |
| `barts_crl` | B3 | zenodo | 220 | 212 CTs | 20.32 / 19 + 6 | fetched |  |
| `kidney_thoraxabdomen` | B3 | zenodo | 215 | 215 CTs | 38.35 / 71 + 9 | fetched |  |
| `curvas_pdacvi` | B3 | zenodo | 109 | 101 CTs | 15.42 / 16 + 4 | fetched |  |
| `aortaseg60` | B3 | zenodo | 60 | 55 CTs | 15.87 / 15 + 5 | fetched |  |
| `curvas` | B3 | zenodo | 90 | 70 CTs (training_set.zip unresolved) | 29.4 / 28 + 5 | fetched |  |
| `quadra_hc` | B3 | zenodo | 48 | 48 CTs | 20.18 / 20 + 3 | fetched |  |
| `deep_psma` | B3 | zenodo | 100 | 53 CTs | 24.07 / 23 + 3 | fetched |  |
| `waw_tace` | B3 | zenodo | 233 | 228 CTs | 47.15 / 44 + 5 | fetched |  |
| `pengwin2026` | B3 | zenodo | 340 | 340 CTs (308 after folding) | 19.57 / 78 + 5 | fetched |  |
| `idc_ct_colonography` | B4 | idc | 825 | 0 | 6 | planned (held) | CTSP alias; 21 new |
| `idc_spine_mets_ct_seg` | B5 | idc | 55 | 0 | 17.2 | planned | tier 2 |
| `idc_cptac_luad` | B5 | idc | 37 | 0 | 7 | planned | tier 2 |
| `idc_midrc_ricord_1b` | B5 | idc | 117 | 0 | 7 | planned | tier 2 |
| `idc_cptac_lscc` | B5 | idc | 36 | 0 | 8.3 | planned | tier 2 |
| `idc_prostate_anatomical_edge_cases` | B5 | idc | 131 | 0 | 16.6 | planned | tier 2 |
| `idc_nsclc_radiogenomics` | B5 | idc | 211 | 0 | 28 | planned | tier 2 |
| `zenodo_medpelvis3d` | B5 | zenodo | 99 | 0 | 15.1 | planned | tier 2 |
| `idc_nsclc_radiomics` | B5 | idc | 422 | 0 | 25.8 | planned | tier 2 |
| `zenodo_lumvbcanseg` | B5 | zenodo | 185 | 0 | 10.08 | planned | tier 2 |
| `idc_lidc_idri` | B5 | idc | 1,010 | 0 | 123.3 | planned | tier 2 |
| `idc_spinal_multiple_myeloma_seg` | B5 | idc | 67 | 0 | 33.8 | planned | tier 2 |
| `zenodo_vsd_fullbody` | B5 | zenodo | 109 | 0 | 116.3 | planned | tier 2 |
| `idc_ldct_and_projection_data` | B5 | idc | 199 | 0 | 16.5 | planned | tier 2 |
| `idc_nlst` | B5 | idc | 26,254 | 0 (pilot 500 in B1) | 2,305.3 | planned | tier 2 |
| `zenodo_ribfrac` | B5 | zenodo | 660 | 660 CTs (other_ct stream) | 77.8 / 73 | fetched (other_ct stream) | tier 2 |
| `aws_stoic2021` | B5 | s3 | 2,000 | 0 | 240 | planned | tier 2 |
| `zenodo_unitochest` | B5 | zenodo | 623 | 0 | 84.07 | planned | tier 2 |
| `scidb_enhance_pet_1_6k` | B6 | Science Data Bank | 1,683 | 0 | 286.3 | planned (deferred) |  |
| `zenodo_tmtv_benchmark` | B6 | zenodo | 60 | 0 | 6.85 | planned (deferred) |  |
| `zenodo_lumos` | B6 | zenodo | 280 | 0 | 34 | planned (deferred) |  |
| `zenodo_ts_task_liver_lesions` | B6 | zenodo | 842 | 0 | 38.87 | planned (unresolved overlap) |  |
| `zenodo_ts_task_pleural_effusion` | B6 | zenodo | 600 | 0 | 8.99 | planned (unresolved overlap) |  |
| `zenodo_ts_task_hip_implant` | B6 | zenodo | 71 | 0 | 9.03 | planned (unresolved overlap) |  |
| `hf_abdomenatlas2_0_mini` | B6 | hf | 10,135 | 0 | 620.4 | planned (unresolved overlap) |  |
| `stanford_aimi_merlin` | B7 | Stanford AIMI portal | 18,317 | 0 | not stated | gated |  |
| `rsna_ratic_abdominal_trauma` | B7 | RSNA MIRA / Kaggle | 3,147 | 0 | not stated | gated |  |
| `hf_ct_rate` | B7 | hf | 21,304 | 0 | not stated | gated |  |
| `stanford_aimi_inspect` | B7 | Stanford AIMI portal | 19,402 | 0 | not stated | gated |  |
| `hf_cads_unique` | B7 | hf | 753 | 0 | 123.3 | gated |  |
| `rsna_rspect_pe` | B7 | RSNA MIRA / Kaggle | 7,279 | 0 | not stated | gated |  |
| `zenodo_magic_ct` | B7 | zenodo | 562 | 0 | not stated | gated |  |
| `idc_tcga_prad` | B8 | idc | 4 | 0 | 1.4 | excluded | no new countable people |
| `idc_tcga_kirp` | B8 | idc | 23 | 0 | 4.5 | excluded | no new countable people |
| `idc_cmb_pca` | B8 | idc | 11 | 0 | 11.6 | excluded | no new countable people |
| `idc_tcga_kich` | B8 | idc | 12 | 0 | 3.4 | excluded | no new countable people |
| `idc_tcga_coad` | B8 | idc | 25 | 0 | 4.4 | excluded | no new countable people |
| `idc_rider_pilot` | B8 | idc | 8 | 0 | 10.6 | excluded | no new countable people |
| `idc_cmb_gec` | B8 | idc | 6 | 0 | 11.9 | excluded | no new countable people |
| `idc_tcga_thca` | B8 | idc | 6 | 0 | 1 | excluded | no new countable people |
| `idc_nsclc_radiomics_genomics` | B8 | idc | 89 | 0 | 6.9 | excluded | no new countable people |
| `idc_qin_lung_ct` | B8 | idc | 47 | 0 | 2 | excluded | no new countable people |
| `idc_tcga_lusc` | B8 | idc | 37 | 0 | 14.1 | excluded | no new countable people |
| `idc_tcga_luad` | B8 | idc | 67 | 0 | 18.3 | excluded | no new countable people |
| `idc_lctsc` | B8 | idc | 60 | 0 | 4.9 | excluded | no new countable people |
| `idc_spie_aapm_lung_ct_challenge` | B8 | idc | 70 | 0 | 11.8 | excluded | no new countable people |
| `idc_rider_lung_ct` | B8 | idc | 32 | 0 | 41.8 | excluded | no new countable people |
| `hf_ctspine1k_noncolonog` | B8 | hf | 221 | 223 screened (other_ct stream) | 26.3 | excluded | no new countable people |
| `idc_4d_lung` | B8 | idc | 20 | 0 | 178.6 | excluded | no new countable people |
| `idc_breast_diagnosis` | B8 | idc | 3 | 0 | 1.4 | excluded | no new countable people |
| `idc_c4kc_kits` | B8 | idc | 210 | 0 | 36.8 | excluded | no new countable people |
| `idc_cc_radiomics_phantom` | B8 | idc | 17 | 0 | 1.4 | excluded | no new countable people |
| `idc_cc_radiomics_phantom_2` | B8 | idc | 251 | 0 | 29.8 | excluded | no new countable people |
| `idc_cc_radiomics_phantom_3` | B8 | idc | 95 | 0 | 13 | excluded | no new countable people |
| `idc_cc_tumor_heterogeneity` | B8 | idc | 22 | 0 | 11.2 | excluded | no new countable people |
| `idc_cmb_aml` | B8 | idc | 7 | 0 | 1.3 | excluded | no new countable people |
| `idc_cptac_aml` | B8 | idc | 5 | 0 | 2.2 | excluded | no new countable people |
| `idc_ct4harmonization_multicentric` | B8 | idc | 1 | 0 | 239.8 | excluded | no new countable people |
| `idc_ct_lymph_nodes` | B8 | idc | 176 | 0 | 56.4 | excluded | no new countable people |
| `idc_ct_phantom4radiomics` | B8 | idc | 1 | 0 | 40.3 | excluded | no new countable people |
| `idc_dro_toolkit` | B8 | idc | 32 | 0 | 4.9 | excluded | no new countable people |
| `idc_ea1141` | B8 | idc | 1 | 0 | 2.3 | excluded | no new countable people |
| `idc_lung_fused_ct_pathology` | B8 | idc | 6 | 0 | 1.6 | excluded | no new countable people |
| `idc_lung_phantom` | B8 | idc | 1 | 0 | 0.1 | excluded | no new countable people |
| `idc_lungct_diagnosis` | B8 | idc | 61 | 0 | 2.4 | excluded | no new countable people |
| `idc_naf_prostate` | B8 | idc | 9 | 0 | 11 | excluded | no new countable people |
| `idc_nlm_visible_human_project` | B8 | idc | 2 | 0 | 2.1 | excluded | no new countable people |
| `idc_nsclc_radiomics_interobserver1` | B8 | idc | 22 | 0 | 2 | excluded | no new countable people |
| `idc_pancreas_ct` | B8 | idc | 80 | 0 | 9.7 | excluded | no new countable people |
| `idc_phantom_fda` | B8 | idc | 7 | 0 | 763.9 | excluded | no new countable people |
| `idc_pseudo_phi_dicom_data` | B8 | idc | 10 | 0 | 0.3 | excluded | no new countable people |
| `idc_qiba_ct_1c` | B8 | idc | 1 | 0 | 35.6 | excluded | no new countable people |
| `idc_qiba_ct_liver_phantom` | B8 | idc | 3 | 0 | 52.6 | excluded | no new countable people |
| `idc_qin_breast` | B8 | idc | 43 | 0 | 4.7 | excluded | no new countable people |
| `idc_rider_phantom_pet_ct` | B8 | idc | 20 | 0 | 0.7 | excluded | no new countable people |
| `idc_soft_tissue_sarcoma` | B8 | idc | 51 | 0 | 7 | excluded | no new countable people |
| `idc_stageii_colorectal_ct` | B8 | idc | 230 | 0 | 7.1 | excluded | no new countable people |
| `idc_tcga_read` | B8 | idc | 3 | 0 | 0.2 | excluded | no new countable people |
| `idc_tcga_sarc` | B8 | idc | 4 | 0 | 2.6 | excluded | no new countable people |
| `idc_uw_cirp_mouse_pet_ct_nsclc` | B8 | idc | 14 | 0 | 34.5 | excluded | no new countable people |
| `excluded_glocker_spine` | B8 | none (excluded) | 125 | 0 | 0 | excluded | licence |
| `hf_bodymaps_pantsmini` | B8 | hf | 9,901 | 0 | 345.7 | excluded | no new countable people |
| `hf_bodymaps_cancerverse` | B8 | hf | 0 | 0 | 0 | excluded | licence |
| `zenodo_lndb` | B8 | zenodo | 294 | 0 | 0 | excluded | licence |
| `zenodo_auc23_lung_ct_covid` | B8 | zenodo | 0 | 0 | 0 | excluded | no new countable people |
| `zenodo_auc23_rib_ct_fracture` | B8 | zenodo | 0 | 0 | 0 | excluded | no new countable people |
| `zenodo_pancreas_abdomenct1k_curated` | B8 | zenodo | 0 | 0 | 0 | excluded | no new countable people |
| `zenodo_tavrp_pl` | B8 | zenodo | 0 | 0 | 0 | excluded | no new countable people |
| `zenodo_merged_multiorgan_abdominal` | B8 | zenodo | 0 | 0 | 0 | excluded | no new countable people |
| `zenodo_synthrad2025` | B8 | zenodo | 0 | 0 | 0 | excluded | no new countable people |
| `excluded_nmdid` | B8 | none (excluded) | 15,243 | 0 | 0 | excluded | licence |

### Cards

### Group B1. Tier 1, first launch (submitted 2026-09-23)

### `idc_tier1` <a id="idc_tier1"></a>

**IDC tier 1, the pooled route (39 collections, one manifest).** Cards: B (IDC tier 1, the pooled route (39 collections, one manifest)), E (idc_tier1). Structured entry: `sources.yaml` id `idc_tier1`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

*[B]*

`idc_tier1` (slurm/acquisition_submit.sh `chain idc`; acquisition/jobs.txt)

*[E]*

`idc_tier1`

**Name and citation**

*[B]*

NCI Imaging Data Commons v24, every TCIA collection the census put in tier 1 except CT Colonography (held); one card per collection follows (acquisition/ACQUISITION_PLAN.md sections 1, 4; tools/acquisition_census.py tier1 manifest; acquisition/census.json idc_version v24)

*[E]*

NCI Imaging Data Commons v24, tier 1: 39 collections from the census manifest `manifests/idc_tier1.csv` (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

CT; coverage classes from DICOM BodyPartExamined and descriptions (WB, CAP, AP, ABD, CA, CHEST, CHEST_SCREEN, PELVIS, SPINE, HN, OTHER); one series per patient (tools/acquisition_census.py CLASS_RULES; acquisition/manifests/idc_tier1.csv)

*[E]*

CT of mixed extent (CAP, abdomen, chest, whole body) (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open; CC BY 3.0, CC BY 4.0 and CC BY-NC 4.0 (midrc_ricord_1a); all rows derived_labels_ok yes; public buckets, no sign-in (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

*[E]*

open; per-collection licence in `ranking.csv` (`ranking.csv`)

**How it was acquired**

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tier1.csv --batch 100`, as `acquisition_submit.sh tier1` ran it; env `/rs/rs_grp_oschome/go2432/envs/acq` (idc-index 0.12.5, s5cmd, built by job 40425851); every route smoke-tested first (job 40425969: IDC 2/2 series); verified by instance count per series (slurm/acquisition_submit.sh; slurm/acquisition_fetch.sh; tools/acquisition_fetch.py; acquisition/jobs.txt)

*[E]*

`python tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by instance count per series against the catalogue (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

census and manifests 2026-09-23 (acquisition/ACQUISITION_PLAN.md); fetch 40426149 submitted 2026-09-23, 2,700/3,600 at about 21:25 EDT, 3,600/3,600 at 21:57 EDT; converted 3,499 by 07:10 EDT 2026-09-24 (acquisition/jobs.txt); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

*[E]*

`$RS/data/idc_tier1` is dated 2026-09-23 in the listing; Slurm job fetch 40426149 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

3,600 series, 3,600 patients, 892,817 instances, 463.4 GB by catalogue, 39 collections (acquisition/manifests/idc_tier1.csv); 3,499 converted at <= 3 mm (acquisition/jobs.txt; docs/ruleclass/TIERS.md) (3,507 NIfTI files on disk (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md)); du of `data/idc` 658 GB (DICOM plus NIfTI), screen output 55 GB, on 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

3,500 of 3,600 listed CTs on disk; 658 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/idc_tier1/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/idc/` (raw/, fetch/, nifti/) and `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (screen), both in the 2026-10-07 listing; grid manifests and job log `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition/manifests/`, `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition/jobs.txt`, `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition/logs/` (listing; acquisition/jobs.txt; slurm/acquisition_submit.sh); nothing on HOME (listing)

*[E]*

`$RS/data/idc` (CEPH, raw, 658.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/idc` (CEPH, converted/derived, 55.0 GB, listing 2026-09-26)

**Annotation status**

*[B]*

pseudo-labels only: TotalSegmentator 2.18 `total` (vertebrae, ribs, sacrum roi) + `vertebrae_body` (labeller B, read geometrically), SPINEPS+VERIDAH ctd names (labeller A), per-case calls; no radiologist read exists for any acquired CT (tools/acquisition_screen.py; acquisition/collections/csi2014/SUMMARY.md; acquisition/ACQUISITION_PLAN.md section 9); row fields: source, case, patient_key, subtype, castellvi, four_lumbar, lumbar_rib, truth_tier, labeller_a, labeller_b, agree, n_thoracic_rib_bearing, n_lumbar, junction_tl_in_fov, junction_ls_in_fov, fused_mask_representation, real_frames (False for every acquired source), notes (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md section 6)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 55 GB under `$RS/data/anomaly_harvest/idc_tier1` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

`/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` screen tree (tools/acquisition_screen.py); ruleclass tier lists `RS/ruleclass/tiers/tier1.tsv`, `tier2.tsv`: idc 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185; arm A (TotalSegmentator `total`), arm B (Möller ribs) and pelvis outputs under `RS/ruleclass/arms/` (docs/ruleclass/TIERS.md; memory/ruleclass-super-detector-run.md); landing dedupe `acquisition/alias_pairs.csv` (job 40426214) and `alias_pairs_all.csv` (40430971, 40436046) on the grid (acquisition/jobs.txt)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

101 of 3,600 series not usable at convert, reasons per collection not copied locally (acquisition/jobs.txt); 13 tier-1 IDC CTs have no SPINEPS mask (docs/ruleclass/TIERS.md section 5); the idc `SUMMARY.md` and `rows.csv` were never copied into the repository (only csi2014, ctpelvic1k_clinic, nlst_pilot were) (acquisition/ACQUISITION_PLAN.md Files here; acquisition/collections/); DATA_COMPLETENESS_AUDIT.md has no section on any acquisition collection (docs/DATA_COMPLETENESS_AUDIT.md)

*[E]*

held as DICOM, 3-4 times its NIfTI size (`CENSUS_TABLE_2026-09-25.md` caveats)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tier1` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` resubmits fetch -> convert -> cases -> ts -> gate -> spineps -> call -> summary for idc and the six other first-launch collections and skips every verified unit and finished case; fetch-only: the command above; must verify 3,600 series / 892,817 instances, FETCH_STATUS.json unresolved_failures 0 (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; acquisition/manifests/idc_tier1.csv)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` (block `tier1`), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `idc_hcc_tace_seg` <a id="idc_hcc_tace_seg"></a>

**IDC `hcc_tace_seg` (HCC-TACE-Seg).** Cards: B (IDC `hcc_tace_seg` (HCC-TACE-Seg)). Structured entry: `sources.yaml` id `idc_hcc_tace_seg`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_hcc_tace_seg` (acquisition/ranking.csv collection `idc:hcc_tace_seg`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `hcc_tace_seg`; TCIA DOI 10.7937/tcia.5fna-0924 (acquisition/ranking.csv; acquisition/census.json idc_version); display name as the plan writes it: HCC-TACE-Seg (acquisition/ACQUISITION_PLAN.md section 4)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:77;AP:15;ABD:9; BodyPartExamined in the manifest: LIVER 101; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

105 patients listed in IDC, 101 qualifying; manifest 101 series / 101 patients / 9,717 instances / 5.0 GB (catalogue series_size_MB); all CT in the collection 26.7 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/hcc_tace_seg/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_hcc_tace_seg_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `hcc_tace_seg:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:75;not a regularly spaced 3-D volume:45;< 60 slices:6 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_hcc_tace_seg` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="hcc_tace_seg"' $D/manifests/idc_tier1.csv > $D/manifests/idc_hcc_tace_seg.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_hcc_tace_seg.csv --batch 100`; must verify 101 series with 9,717 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_pancreatic_ct_cbct_seg` <a id="idc_pancreatic_ct_cbct_seg"></a>

**IDC `pancreatic_ct_cbct_seg`.** Cards: B (IDC `pancreatic_ct_cbct_seg`). Structured entry: `sources.yaml` id `idc_pancreatic_ct_cbct_seg`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_pancreatic_ct_cbct_seg` (acquisition/ranking.csv collection `idc:pancreatic_ct_cbct_seg`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `pancreatic_ct_cbct_seg`; TCIA DOI 10.7937/tcia.eshq-4d90 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:39;AP:1; BodyPartExamined in the manifest: ABDOMEN 37, CHEST 3; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

40 patients listed in IDC, 40 qualifying; manifest 40 series / 40 patients / 5,614 instances / 2.9 GB (catalogue series_size_MB); all CT in the collection 12.3 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/pancreatic_ct_cbct_seg/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_pancreatic_ct_cbct_seg_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `pancreatic_ct_cbct_seg:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): none (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_pancreatic_ct_cbct_seg` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="pancreatic_ct_cbct_seg"' $D/manifests/idc_tier1.csv > $D/manifests/idc_pancreatic_ct_cbct_seg.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_pancreatic_ct_cbct_seg.csv --batch 100`; must verify 40 series with 5,614 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_tcga_kirc` <a id="idc_tcga_kirc"></a>

**IDC `tcga_kirc`.** Cards: B (IDC `tcga_kirc`). Structured entry: `sources.yaml` id `idc_tcga_kirc`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_tcga_kirc` (acquisition/ranking.csv collection `idc:tcga_kirc`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `tcga_kirc`; TCIA DOI 10.7937/k9/tcia.2016.v6pbvtdr (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:95;CAP:22;AP:11;CA:1; BodyPartExamined in the manifest: KIDNEY 129; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

237 patients listed in IDC, 129 qualifying; manifest 129 series / 129 patients / 18,869 instances / 9.7 GB (catalogue series_size_MB); all CT in the collection 73.9 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/tcga_kirc/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_tcga_kirc_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `tcga_kirc:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:739;localizer image type:393;reformat/MIP series:87;not a regularly spaced 3-D volume:74 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tcga_kirc` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="tcga_kirc"' $D/manifests/idc_tier1.csv > $D/manifests/idc_tcga_kirc.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tcga_kirc.csv --batch 100`; must verify 129 series with 18,869 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_colorectal_liver_metastases` <a id="idc_colorectal_liver_metastases"></a>

**IDC `colorectal_liver_metastases` (Colorectal-Liver-Metastases).** Cards: B (IDC `colorectal_liver_metastases` (Colorectal-Liver-Metastases)). Structured entry: `sources.yaml` id `idc_colorectal_liver_metastases`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_colorectal_liver_metastases` (acquisition/ranking.csv collection `idc:colorectal_liver_metastases`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `colorectal_liver_metastases`; TCIA DOI 10.7937/qxk2-qg03 (acquisition/ranking.csv; acquisition/census.json idc_version); display name as the plan writes it: Colorectal-Liver-Metastases (acquisition/ACQUISITION_PLAN.md section 4)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:80; BodyPartExamined in the manifest: (blank) 80; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

197 patients listed in IDC, 80 qualifying; manifest 80 series / 80 patients / 11,967 instances / 6.2 GB (catalogue series_size_MB); all CT in the collection 9.1 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/colorectal_liver_metastases/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_colorectal_liver_metastases_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `colorectal_liver_metastases:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:117 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_colorectal_liver_metastases` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="colorectal_liver_metastases"' $D/manifests/idc_tier1.csv > $D/manifests/idc_colorectal_liver_metastases.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_colorectal_liver_metastases.csv --batch 100`; must verify 80 series with 11,967 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_ct_vs_pet_ventilation_imaging` <a id="idc_ct_vs_pet_ventilation_imaging"></a>

**IDC `ct_vs_pet_ventilation_imaging`.** Cards: B (IDC `ct_vs_pet_ventilation_imaging`). Structured entry: `sources.yaml` id `idc_ct_vs_pet_ventilation_imaging`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_ct_vs_pet_ventilation_imaging` (acquisition/ranking.csv collection `idc:ct_vs_pet_ventilation_imaging`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `ct_vs_pet_ventilation_imaging`; TCIA DOI 10.7937/3ppx-7s22 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:19;CHEST:1; BodyPartExamined in the manifest: ABDOMEN 19, CHEST 1; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

20 patients listed in IDC, 20 qualifying; manifest 20 series / 20 patients / 3,397 instances / 1.8 GB (catalogue series_size_MB); all CT in the collection 13.6 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/ct_vs_pet_ventilation_imaging/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_ct_vs_pet_ventilation_imaging_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `ct_vs_pet_ventilation_imaging:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): not a regularly spaced 3-D volume:20 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_ct_vs_pet_ventilation_imaging` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="ct_vs_pet_ventilation_imaging"' $D/manifests/idc_tier1.csv > $D/manifests/idc_ct_vs_pet_ventilation_imaging.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_ct_vs_pet_ventilation_imaging.csv --batch 100`; must verify 20 series with 3,397 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_tcga_lihc` <a id="idc_tcga_lihc"></a>

**IDC `tcga_lihc`.** Cards: B (IDC `tcga_lihc`). Structured entry: `sources.yaml` id `idc_tcga_lihc`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_tcga_lihc` (acquisition/ranking.csv collection `idc:tcga_lihc`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `tcga_lihc`; TCIA DOI 10.7937/k9/tcia.2016.immqw8uq (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:35;CAP:5;AP:2; BodyPartExamined in the manifest: LIVER 42; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

75 patients listed in IDC, 42 qualifying; manifest 42 series / 42 patients / 9,429 instances / 4.9 GB (catalogue series_size_MB); all CT in the collection 36.4 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/tcga_lihc/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_tcga_lihc_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `tcga_lihc:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:226;localizer image type:151;reformat/MIP series:113;non-axial reformat:82 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tcga_lihc` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="tcga_lihc"' $D/manifests/idc_tier1.csv > $D/manifests/idc_tcga_lihc.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tcga_lihc.csv --batch 100`; must verify 42 series with 9,429 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_adrenal_acc_ki67_seg` <a id="idc_adrenal_acc_ki67_seg"></a>

**IDC `adrenal_acc_ki67_seg`.** Cards: B (IDC `adrenal_acc_ki67_seg`). Structured entry: `sources.yaml` id `idc_adrenal_acc_ki67_seg`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_adrenal_acc_ki67_seg` (acquisition/ranking.csv collection `idc:adrenal_acc_ki67_seg`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `adrenal_acc_ki67_seg`; TCIA DOI 10.7937/1fpg-vm46 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:19;AP:5;CAP:5; BodyPartExamined in the manifest: ADRENAL 21, ABDOMEN 8; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

53 patients listed in IDC, 29 qualifying; manifest 29 series / 29 patients / 6,729 instances / 3.5 GB (catalogue series_size_MB); all CT in the collection 9.4 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/adrenal_acc_ki67_seg/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_adrenal_acc_ki67_seg_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `adrenal_acc_ki67_seg:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:57;not a regularly spaced 3-D volume:1;< 60 slices:1 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_adrenal_acc_ki67_seg` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="adrenal_acc_ki67_seg"' $D/manifests/idc_tier1.csv > $D/manifests/idc_adrenal_acc_ki67_seg.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_adrenal_acc_ki67_seg.csv --batch 100`; must verify 29 series with 6,729 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_eay131` <a id="idc_eay131"></a>

**IDC `eay131` (EAY131 (NCI-MATCH)).** Cards: B (IDC `eay131` (EAY131 (NCI-MATCH))). Structured entry: `sources.yaml` id `idc_eay131`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_eay131` (acquisition/ranking.csv collection `idc:eay131`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `eay131`; TCIA DOI 10.7937/c5ke-yx42 (acquisition/ranking.csv; acquisition/census.json idc_version); display name as the plan writes it: EAY131 (NCI-MATCH) (acquisition/ACQUISITION_PLAN.md section 4)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:149;CHEST:81;ABD:74;AP:43;OTHER:13;WB:5;CA:5;SPINE:3;PELVIS:3; BodyPartExamined in the manifest: ABDOMEN 147, CHEST 107, (blank) 95, CHESTABDPELVIS 20; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

2,653 patients listed in IDC, 376 qualifying; manifest 376 series / 376 patients / 65,202 instances / 36.4 GB (catalogue series_size_MB); all CT in the collection 760.0 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/eay131/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_eay131_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `eay131:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:4999;slice > 3.0 mm:3589;not a regularly spaced 3-D volume:2655;< 60 slices:1189 (acquisition/ranking.csv); the plan's prose refusal counts (3,754 > 3 mm, 2,790 not regular, 1,249 < 60 slices of 13,166) do not match ranking.csv (3,589 / 2,655 / 1,189, plus 4,999 non-axial reformats); ranking.csv is the generated file (acquisition/ACQUISITION_PLAN.md section 4; acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_eay131` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="eay131"' $D/manifests/idc_tier1.csv > $D/manifests/idc_eay131.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_eay131.csv --batch 100`; must verify 376 series with 65,202 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cmb_mel` <a id="idc_cmb_mel"></a>

**IDC `cmb_mel`.** Cards: B (IDC `cmb_mel`). Structured entry: `sources.yaml` id `idc_cmb_mel`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cmb_mel` (acquisition/ranking.csv collection `idc:cmb_mel`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cmb_mel`; TCIA DOI 10.7937/gwsp-wh72 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:10;CHEST:6;WB:4;AP:2;SPINE:1; BodyPartExamined in the manifest: CHEST 6, CHESTABDPELVIS 5, ABDOMEN 4, ABDOMENPELVIS 2; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

32 patients listed in IDC, 23 qualifying; manifest 23 series / 23 patients / 4,074 instances / 2.1 GB (catalogue series_size_MB); all CT in the collection 36.9 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cmb_mel/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cmb_mel_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cmb_mel:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:179;localizer image type:103;reformat/MIP series:86;slice > 3.0 mm:74 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cmb_mel` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cmb_mel"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cmb_mel.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cmb_mel.csv --batch 100`; must verify 23 series with 4,074 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_tcga_stad` <a id="idc_tcga_stad"></a>

**IDC `tcga_stad`.** Cards: B (IDC `tcga_stad`). Structured entry: `sources.yaml` id `idc_tcga_stad`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_tcga_stad` (acquisition/ranking.csv collection `idc:tcga_stad`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `tcga_stad`; TCIA DOI 10.7937/k9/tcia.2016.gdhl9kim (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:45; BodyPartExamined in the manifest: STOMACH 45; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

46 patients listed in IDC, 45 qualifying; manifest 45 series / 45 patients / 12,189 instances / 6.3 GB (catalogue series_size_MB); all CT in the collection 22.8 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/tcga_stad/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_tcga_stad_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `tcga_stad:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:53;localizer image type:50;slice > 3.0 mm:26;< 60 slices:10 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tcga_stad` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="tcga_stad"' $D/manifests/idc_tier1.csv > $D/manifests/idc_tcga_stad.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tcga_stad.csv --batch 100`; must verify 45 series with 12,189 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cmb_ov` <a id="idc_cmb_ov"></a>

**IDC `cmb_ov`.** Cards: B (IDC `cmb_ov`). Structured entry: `sources.yaml` id `idc_cmb_ov`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cmb_ov` (acquisition/ranking.csv collection `idc:cmb_ov`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cmb_ov`; TCIA DOI 10.7937/4nx6-e061 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:3;AP:3;ABD:1; BodyPartExamined in the manifest: ABDOMEN 3, CHEST 2, ABDOMENPELVIS 1, CHESTABDOMEN 1; median SliceThickness 2 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

17 patients listed in IDC, 7 qualifying; manifest 7 series / 7 patients / 1,983 instances / 1.0 GB (catalogue series_size_MB); all CT in the collection 23.4 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cmb_ov/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cmb_ov_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cmb_ov:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:138;slice > 3.0 mm:88;localizer image type:52;reformat/MIP series:18 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cmb_ov` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cmb_ov"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cmb_ov.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cmb_ov.csv --batch 100`; must verify 7 series with 1,983 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_pediatric_ct_seg` <a id="idc_pediatric_ct_seg"></a>

**IDC `pediatric_ct_seg` (Pediatric-CT-SEG).** Cards: B (IDC `pediatric_ct_seg` (Pediatric-CT-SEG)). Structured entry: `sources.yaml` id `idc_pediatric_ct_seg`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_pediatric_ct_seg` (acquisition/ranking.csv collection `idc:pediatric_ct_seg`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `pediatric_ct_seg`; TCIA DOI 10.7937/tcia.x0h0-1706 (acquisition/ranking.csv; acquisition/census.json idc_version); display name as the plan writes it: Pediatric-CT-SEG (acquisition/ACQUISITION_PLAN.md section 4)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:352; BodyPartExamined in the manifest: ABDOMEN 195, (blank) 157; median SliceThickness 2 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

359 patients listed in IDC, 352 qualifying; manifest 352 series / 352 patients / 108,019 instances / 55.6 GB (catalogue series_size_MB); all CT in the collection 56.6 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/pediatric_ct_seg/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_pediatric_ct_seg_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `pediatric_ct_seg:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): not a regularly spaced 3-D volume:6;< 60 slices:1 (acquisition/ranking.csv); children: an unfused S1 reads as a free body and the sacral shape is not adult; collection-level class CAP assigned because the header says less than the description (docs/ruleclass/TIERS.md section 1; tools/acquisition_census.py COLLECTION_CLASS); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_pediatric_ct_seg` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="pediatric_ct_seg"' $D/manifests/idc_tier1.csv > $D/manifests/idc_pediatric_ct_seg.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_pediatric_ct_seg.csv --batch 100`; must verify 352 series with 108,019 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_anti_pd_1_lung` <a id="idc_anti_pd_1_lung"></a>

**IDC `anti_pd_1_lung`.** Cards: B (IDC `anti_pd_1_lung`). Structured entry: `sources.yaml` id `idc_anti_pd_1_lung`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_anti_pd_1_lung` (acquisition/ranking.csv collection `idc:anti_pd_1_lung`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `anti_pd_1_lung`; TCIA DOI 10.7937/tcia.2019.zjjwb9ip (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:20;CHEST_SCREEN:7;WB:7; BodyPartExamined in the manifest: (blank) 18, ABDOMEN 11, CHEST 5; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

46 patients listed in IDC, 34 qualifying; manifest 34 series / 34 patients / 8,055 instances / 4.2 GB (catalogue series_size_MB); all CT in the collection 54.4 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/anti_pd_1_lung/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_anti_pd_1_lung_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `anti_pd_1_lung:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:166;non-axial reformat:121;localizer image type:96;reformat/MIP series:34 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_anti_pd_1_lung` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="anti_pd_1_lung"' $D/manifests/idc_tier1.csv > $D/manifests/idc_anti_pd_1_lung.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_anti_pd_1_lung.csv --batch 100`; must verify 34 series with 8,055 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cptac_ucec` <a id="idc_cptac_ucec"></a>

**IDC `cptac_ucec`.** Cards: B (IDC `cptac_ucec`). Structured entry: `sources.yaml` id `idc_cptac_ucec`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cptac_ucec` (acquisition/ranking.csv collection `idc:cptac_ucec`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cptac_ucec`; TCIA DOI 10.7937/k9/tcia.2018.3r3juisw (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:39;CAP:18;AP:6;CHEST:1;WB:1;PELVIS:1; BodyPartExamined in the manifest: ABDOMEN 50, (blank) 8, CHESTABDPELVIS 4, CHEST 3; median SliceThickness 1.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

75 patients listed in IDC, 66 qualifying; manifest 66 series / 66 patients / 19,942 instances / 10.3 GB (catalogue series_size_MB); all CT in the collection 58.1 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cptac_ucec/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cptac_ucec_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cptac_ucec:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:362;localizer image type:90;non-axial reformat:87;reformat/MIP series:73 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cptac_ucec` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cptac_ucec"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cptac_ucec.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cptac_ucec.csv --batch 100`; must verify 66 series with 19,942 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cmb_brca` <a id="idc_cmb_brca"></a>

**IDC `cmb_brca`.** Cards: B (IDC `cmb_brca`). Structured entry: `sources.yaml` id `idc_cmb_brca`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cmb_brca` (acquisition/ranking.csv collection `idc:cmb_brca`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cmb_brca`; TCIA DOI 10.7937/dx22-8j71 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes WB:9;CHEST:6;CAP:4;ABD:2; BodyPartExamined in the manifest: CHEST 8, HEAD 6, ABDOMEN 3, WHOLEBODY 3; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

25 patients listed in IDC, 21 qualifying; manifest 21 series / 21 patients / 4,909 instances / 2.5 GB (catalogue series_size_MB); all CT in the collection 22.8 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cmb_brca/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cmb_brca_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cmb_brca:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): reformat/MIP series:65;localizer image type:55;non-axial reformat:49;slice > 3.0 mm:45 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cmb_brca` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cmb_brca"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cmb_brca.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cmb_brca.csv --batch 100`; must verify 21 series with 4,909 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_tcga_blca` <a id="idc_tcga_blca"></a>

**IDC `tcga_blca`.** Cards: B (IDC `tcga_blca`). Structured entry: `sources.yaml` id `idc_tcga_blca`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_tcga_blca` (acquisition/ranking.csv collection `idc:tcga_blca`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `tcga_blca`; TCIA DOI 10.7937/k9/tcia.2016.8lng8xdr (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:23;PELVIS:20;AP:19;CAP:9;WB:6;CHEST:2; BodyPartExamined in the manifest: BLADDER 67, (blank) 12; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

107 patients listed in IDC, 79 qualifying; manifest 79 series / 79 patients / 19,484 instances / 10.0 GB (catalogue series_size_MB); all CT in the collection 51.5 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/tcga_blca/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_tcga_blca_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `tcga_blca:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:184;localizer image type:143;non-axial reformat:92;not a regularly spaced 3-D volume:38 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tcga_blca` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="tcga_blca"' $D/manifests/idc_tier1.csv > $D/manifests/idc_tcga_blca.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tcga_blca.csv --batch 100`; must verify 79 series with 19,484 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cptac_pda` <a id="idc_cptac_pda"></a>

**IDC `cptac_pda`.** Cards: B (IDC `cptac_pda`). Structured entry: `sources.yaml` id `idc_cptac_pda`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cptac_pda` (acquisition/ranking.csv collection `idc:cptac_pda`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cptac_pda`; TCIA DOI 10.7937/k9/tcia.2018.sc20fo18 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:35;AP:10;CAP:9;OTHER:6;CHEST:2; BodyPartExamined in the manifest: ABDOMEN 30, PANCREAS 13, (blank) 10, CHESTABDPELVIS 4; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

99 patients listed in IDC, 62 qualifying; manifest 62 series / 62 patients / 18,952 instances / 9.8 GB (catalogue series_size_MB); all CT in the collection 57.4 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cptac_pda/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cptac_pda_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cptac_pda:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:272;slice > 3.0 mm:203;localizer image type:36;< 60 slices:33 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cptac_pda` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cptac_pda"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cptac_pda.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cptac_pda.csv --batch 100`; must verify 62 series with 18,952 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_psma_pet_ct_lesions` <a id="idc_psma_pet_ct_lesions"></a>

**IDC `psma_pet_ct_lesions` (PSMA-PET-CT-Lesions (autoPET III)).** Cards: B (IDC `psma_pet_ct_lesions` (PSMA-PET-CT-Lesions (autoPET III))). Structured entry: `sources.yaml` id `idc_psma_pet_ct_lesions`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_psma_pet_ct_lesions` (acquisition/ranking.csv collection `idc:psma_pet_ct_lesions`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `psma_pet_ct_lesions`; TCIA DOI 10.7937/r7ep-3x37 (acquisition/ranking.csv; acquisition/census.json idc_version); display name as the plan writes it: PSMA-PET-CT-Lesions (autoPET III) (acquisition/ACQUISITION_PLAN.md section 4)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes WB:374; BodyPartExamined in the manifest: ABDOMEN 217, (blank) 157; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

378 patients listed in IDC, 374 qualifying; manifest 374 series / 374 patients / 119,632 instances / 61.7 GB (catalogue series_size_MB); all CT in the collection 95.8 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/psma_pet_ct_lesions/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_psma_pet_ct_lesions_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `psma_pet_ct_lesions:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:3;not a regularly spaced 3-D volume:1 (acquisition/ranking.csv); collection-level class WB assigned (header says less than the description) (tools/acquisition_census.py COLLECTION_CLASS; acquisition/ACQUISITION_PLAN.md section 2); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_psma_pet_ct_lesions` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="psma_pet_ct_lesions"' $D/manifests/idc_tier1.csv > $D/manifests/idc_psma_pet_ct_lesions.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_psma_pet_ct_lesions.csv --batch 100`; must verify 374 series with 119,632 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_tcga_ucec` <a id="idc_tcga_ucec"></a>

**IDC `tcga_ucec`.** Cards: B (IDC `tcga_ucec`). Structured entry: `sources.yaml` id `idc_tcga_ucec`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_tcga_ucec` (acquisition/ranking.csv collection `idc:tcga_ucec`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `tcga_ucec`; TCIA DOI 10.7937/k9/tcia.2016.gkj0zwac (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST:11;AP:8;ABD:7;PELVIS:6;CAP:5;OTHER:1; BodyPartExamined in the manifest: UTERUS 35, (blank) 3; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

65 patients listed in IDC, 38 qualifying; manifest 38 series / 38 patients / 7,900 instances / 4.1 GB (catalogue series_size_MB); all CT in the collection 32.8 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/tcga_ucec/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_tcga_ucec_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `tcga_ucec:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:269;localizer image type:217;reformat/MIP series:126;non-axial reformat:26 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tcga_ucec` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="tcga_ucec"' $D/manifests/idc_tier1.csv > $D/manifests/idc_tcga_ucec.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tcga_ucec.csv --batch 100`; must verify 38 series with 7,900 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_ctpred_sunitinib_pannet` <a id="idc_ctpred_sunitinib_pannet"></a>

**IDC `ctpred_sunitinib_pannet`.** Cards: B (IDC `ctpred_sunitinib_pannet`). Structured entry: `sources.yaml` id `idc_ctpred_sunitinib_pannet`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_ctpred_sunitinib_pannet` (acquisition/ranking.csv collection `idc:ctpred_sunitinib_pannet`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `ctpred_sunitinib_pannet`; TCIA DOI 10.7937/spgk-0p94 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:27;OTHER:4;CAP:3; BodyPartExamined in the manifest: ABDOMEN 21, (blank) 13; median SliceThickness 1 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

38 patients listed in IDC, 34 qualifying; manifest 34 series / 34 patients / 11,689 instances / 6.0 GB (catalogue series_size_MB); all CT in the collection 11.6 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/ctpred_sunitinib_pannet/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_ctpred_sunitinib_pannet_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `ctpred_sunitinib_pannet:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): reformat/MIP series:11;not a regularly spaced 3-D volume:2 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_ctpred_sunitinib_pannet` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="ctpred_sunitinib_pannet"' $D/manifests/idc_tier1.csv > $D/manifests/idc_ctpred_sunitinib_pannet.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_ctpred_sunitinib_pannet.csv --batch 100`; must verify 34 series with 11,689 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cptac_ccrcc` <a id="idc_cptac_ccrcc"></a>

**IDC `cptac_ccrcc`.** Cards: B (IDC `cptac_ccrcc`). Structured entry: `sources.yaml` id `idc_cptac_ccrcc`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cptac_ccrcc` (acquisition/ranking.csv collection `idc:cptac_ccrcc`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cptac_ccrcc`; TCIA DOI 10.7937/k9/tcia.2018.oblamn27 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes ABD:21;AP:13;OTHER:9;CAP:4;CHEST:1; BodyPartExamined in the manifest: (blank) 23, ABDOMEN 19, KIDNEY 2, ABDOMENPELVIS 2; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

64 patients listed in IDC, 48 qualifying; manifest 48 series / 48 patients / 13,242 instances / 7.7 GB (catalogue series_size_MB); all CT in the collection 52.2 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cptac_ccrcc/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cptac_ccrcc_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cptac_ccrcc:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:145;non-axial reformat:132;localizer image type:71;reformat/MIP series:66 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cptac_ccrcc` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cptac_ccrcc"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cptac_ccrcc.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cptac_ccrcc.csv --batch 100`; must verify 48 series with 13,242 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cmb_crc` <a id="idc_cmb_crc"></a>

**IDC `cmb_crc`.** Cards: B (IDC `cmb_crc`). Structured entry: `sources.yaml` id `idc_cmb_crc`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cmb_crc` (acquisition/ranking.csv collection `idc:cmb_crc`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cmb_crc`; TCIA DOI 10.7937/djg7-gz87 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:12;AP:8;CHEST:4;WB:3;ABD:2;OTHER:1; BodyPartExamined in the manifest: CHEST 8, (blank) 7, ABDOMEN 6, ABDOMENPELVIS 4; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

44 patients listed in IDC, 30 qualifying; manifest 30 series / 30 patients / 10,256 instances / 5.3 GB (catalogue series_size_MB); all CT in the collection 89.9 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cmb_crc/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cmb_crc_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cmb_crc:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:507;non-axial reformat:451;localizer image type:198;reformat/MIP series:100 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cmb_crc` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cmb_crc"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cmb_crc.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cmb_crc.csv --batch 100`; must verify 30 series with 10,256 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_acrin_flt_breast` <a id="idc_acrin_flt_breast"></a>

**IDC `acrin_flt_breast`.** Cards: B (IDC `acrin_flt_breast`). Structured entry: `sources.yaml` id `idc_acrin_flt_breast`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_acrin_flt_breast` (acquisition/ranking.csv collection `idc:acrin_flt_breast`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `acrin_flt_breast`; TCIA DOI 10.7937/k9/tcia.2017.ol20zmxg (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes WB:15; BodyPartExamined in the manifest: BREAST 12, ABDOMEN 3; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

80 patients listed in IDC, 15 qualifying; manifest 15 series / 15 patients / 5,341 instances / 2.8 GB (catalogue series_size_MB); all CT in the collection 39.3 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/acrin_flt_breast/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_acrin_flt_breast_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `acrin_flt_breast:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:326;localizer image type:68;< 60 slices:20 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_acrin_flt_breast` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="acrin_flt_breast"' $D/manifests/idc_tier1.csv > $D/manifests/idc_acrin_flt_breast.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_acrin_flt_breast.csv --batch 100`; must verify 15 series with 5,341 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cmb_mml` <a id="idc_cmb_mml"></a>

**IDC `cmb_mml`.** Cards: B (IDC `cmb_mml`). Structured entry: `sources.yaml` id `idc_cmb_mml`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cmb_mml` (acquisition/ranking.csv collection `idc:cmb_mml`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cmb_mml`; TCIA DOI 10.7937/szkb-sw39 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes AP:5;CAP:4;SPINE:3;OTHER:2;WB:1;CHEST:1; BodyPartExamined in the manifest: (blank) 8, ABDOMEN 3, CHESTABDPELVIS 2, LSPINE 2; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

61 patients listed in IDC, 16 qualifying; manifest 16 series / 16 patients / 4,407 instances / 2.3 GB (catalogue series_size_MB); all CT in the collection 12.2 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cmb_mml/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cmb_mml_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cmb_mml:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:127;localizer image type:81;non-axial reformat:45;reformat/MIP series:11 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cmb_mml` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cmb_mml"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cmb_mml.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cmb_mml.csv --batch 100`; must verify 16 series with 4,407 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_tcga_ov` <a id="idc_tcga_ov"></a>

**IDC `tcga_ov`.** Cards: B (IDC `tcga_ov`). Structured entry: `sources.yaml` id `idc_tcga_ov`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_tcga_ov` (acquisition/ranking.csv collection `idc:tcga_ov`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `tcga_ov`; TCIA DOI 10.7937/k9/tcia.2016.ndo1mdfq (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes PELVIS:8;CHEST:7;ABD:6;CAP:2;AP:1; BodyPartExamined in the manifest: OVARY 24; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

143 patients listed in IDC, 24 qualifying; manifest 24 series / 24 patients / 4,687 instances / 2.4 GB (catalogue series_size_MB); all CT in the collection 27.5 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/tcga_ov/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_tcga_ov_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `tcga_ov:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:532;localizer image type:154;reformat/MIP series:60;non-axial reformat:19 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tcga_ov` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="tcga_ov"' $D/manifests/idc_tier1.csv > $D/manifests/idc_tcga_ov.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tcga_ov.csv --batch 100`; must verify 24 series with 4,687 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cmb_lca` <a id="idc_cmb_lca"></a>

**IDC `cmb_lca`.** Cards: B (IDC `cmb_lca`). Structured entry: `sources.yaml` id `idc_cmb_lca`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cmb_lca` (acquisition/ranking.csv collection `idc:cmb_lca`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cmb_lca`; TCIA DOI 10.7937/3cx3-s132 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST:31;WB:22;CAP:12;AP:7;CA:2;OTHER:1; BodyPartExamined in the manifest: CHEST 28, ABDOMEN 16, (blank) 12, HEAD 9; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

92 patients listed in IDC, 75 qualifying; manifest 75 series / 75 patients / 18,851 instances / 9.8 GB (catalogue series_size_MB); all CT in the collection 95.5 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cmb_lca/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cmb_lca_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cmb_lca:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:331;slice > 3.0 mm:237;localizer image type:235;reformat/MIP series:171 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cmb_lca` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cmb_lca"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cmb_lca.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cmb_lca.csv --batch 100`; must verify 75 series with 18,851 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_mediastinal_lymph_node_seg` <a id="idc_mediastinal_lymph_node_seg"></a>

**IDC `mediastinal_lymph_node_seg`.** Cards: B (IDC `mediastinal_lymph_node_seg`). Structured entry: `sources.yaml` id `idc_mediastinal_lymph_node_seg`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_mediastinal_lymph_node_seg` (acquisition/ranking.csv collection `idc:mediastinal_lymph_node_seg`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `mediastinal_lymph_node_seg`; TCIA DOI 10.7937/qvaz-ja09 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST_SCREEN:205;CAP:49;ABD:43;HN:12;CA:4;WB:3; BodyPartExamined in the manifest: CHEST 205, CHESTABDPELVIS 49, ABDOMEN 43, NECK 12; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

513 patients listed in IDC, 316 qualifying; manifest 316 series / 316 patients / 48,770 instances / 25.1 GB (catalogue series_size_MB); all CT in the collection 34.1 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/mediastinal_lymph_node_seg/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_mediastinal_lymph_node_seg_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `mediastinal_lymph_node_seg:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:196;< 60 slices:1 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_mediastinal_lymph_node_seg` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="mediastinal_lymph_node_seg"' $D/manifests/idc_tier1.csv > $D/manifests/idc_mediastinal_lymph_node_seg.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_mediastinal_lymph_node_seg.csv --batch 100`; must verify 316 series with 48,770 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_lung_pet_ct_dx` <a id="idc_lung_pet_ct_dx"></a>

**IDC `lung_pet_ct_dx` (Lung-PET-CT-Dx).** Cards: B (IDC `lung_pet_ct_dx` (Lung-PET-CT-Dx)). Structured entry: `sources.yaml` id `idc_lung_pet_ct_dx`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_lung_pet_ct_dx` (acquisition/ranking.csv collection `idc:lung_pet_ct_dx`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `lung_pet_ct_dx`; TCIA DOI 10.7937/tcia.2020.nnc2-0461 (acquisition/ranking.csv; acquisition/census.json idc_version); display name as the plan writes it: Lung-PET-CT-Dx (acquisition/ACQUISITION_PLAN.md section 4)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes WB:133;CHEST_SCREEN:21;OTHER:2;ABD:1;CA:1; BodyPartExamined in the manifest: CHEST 140, ABDOMEN 9, (blank) 8, THORAX 1; median SliceThickness 1 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

355 patients listed in IDC, 158 qualifying; manifest 158 series / 158 patients / 56,646 instances / 29.2 GB (catalogue series_size_MB); all CT in the collection 76.5 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/lung_pet_ct_dx/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_lung_pet_ct_dx_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `lung_pet_ct_dx:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:535;not a regularly spaced 3-D volume:21;< 60 slices:5;localizer image type:1 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_lung_pet_ct_dx` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="lung_pet_ct_dx"' $D/manifests/idc_tier1.csv > $D/manifests/idc_lung_pet_ct_dx.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_lung_pet_ct_dx.csv --batch 100`; must verify 158 series with 56,646 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_varepop_apollo` <a id="idc_varepop_apollo"></a>

**IDC `varepop_apollo`.** Cards: B (IDC `varepop_apollo`). Structured entry: `sources.yaml` id `idc_varepop_apollo`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_varepop_apollo` (acquisition/ranking.csv collection `idc:varepop_apollo`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `varepop_apollo`; TCIA DOI 10.7937/ghkn-md15 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST:14;CAP:10;ABD:5;AP:5;SPINE:1; BodyPartExamined in the manifest: CHEST 13, ABDOMEN 8, (blank) 6, CHESTABDPELVIS 4; median SliceThickness 2 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

38 patients listed in IDC, 35 qualifying; manifest 35 series / 35 patients / 10,376 instances / 5.4 GB (catalogue series_size_MB); all CT in the collection 101.5 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/varepop_apollo/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_varepop_apollo_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `varepop_apollo:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:397;slice > 3.0 mm:256;localizer image type:186;reformat/MIP series:116 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_varepop_apollo` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="varepop_apollo"' $D/manifests/idc_tier1.csv > $D/manifests/idc_varepop_apollo.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_varepop_apollo.csv --batch 100`; must verify 35 series with 10,376 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_tcga_esca` <a id="idc_tcga_esca"></a>

**IDC `tcga_esca`.** Cards: B (IDC `tcga_esca`). Structured entry: `sources.yaml` id `idc_tcga_esca`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_tcga_esca` (acquisition/ranking.csv collection `idc:tcga_esca`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `tcga_esca`; TCIA DOI 10.7937/k9/tcia.2016.vptnrgfy (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes OTHER:8;ABD:7;CHEST:1; BodyPartExamined in the manifest: ESOPHAGUS 16; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

16 patients listed in IDC, 16 qualifying; manifest 16 series / 16 patients / 4,738 instances / 2.4 GB (catalogue series_size_MB); all CT in the collection 10.7 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/tcga_esca/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_tcga_esca_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `tcga_esca:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:26;localizer image type:18;slice > 3.0 mm:15;not a regularly spaced 3-D volume:1 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_tcga_esca` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="tcga_esca"' $D/manifests/idc_tier1.csv > $D/manifests/idc_tcga_esca.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_tcga_esca.csv --batch 100`; must verify 16 series with 4,738 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_covid_19_ny_sbu` <a id="idc_covid_19_ny_sbu"></a>

**IDC `covid_19_ny_sbu` (COVID-19-NY-SBU).** Cards: B (IDC `covid_19_ny_sbu` (COVID-19-NY-SBU)). Structured entry: `sources.yaml` id `idc_covid_19_ny_sbu`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_covid_19_ny_sbu` (acquisition/ranking.csv collection `idc:covid_19_ny_sbu`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `covid_19_ny_sbu`; TCIA DOI 10.7937/tcia.bbag-2923 (acquisition/ranking.csv; acquisition/census.json idc_version); display name as the plan writes it: COVID-19-NY-SBU (acquisition/ACQUISITION_PLAN.md section 4)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST_SCREEN:244;AP:90;ABD:62;CAP:44;WB:3; BodyPartExamined in the manifest: (blank) 326, CHEST 59, CHESTABDPELVIS 36, ABDOMEN 20; median SliceThickness 1.25 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

458 patients listed in IDC, 443 qualifying; manifest 443 series / 443 patients / 122,272 instances / 63.1 GB (catalogue series_size_MB); all CT in the collection 285.8 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/covid_19_ny_sbu/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_covid_19_ny_sbu_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `covid_19_ny_sbu:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:1655;slice > 3.0 mm:623;localizer image type:607;not a regularly spaced 3-D volume:34 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_covid_19_ny_sbu` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="covid_19_ny_sbu"' $D/manifests/idc_tier1.csv > $D/manifests/idc_covid_19_ny_sbu.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_covid_19_ny_sbu.csv --batch 100`; must verify 443 series with 122,272 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_acrin_nsclc_fdg_pet` <a id="idc_acrin_nsclc_fdg_pet"></a>

**IDC `acrin_nsclc_fdg_pet`.** Cards: B (IDC `acrin_nsclc_fdg_pet`). Structured entry: `sources.yaml` id `idc_acrin_nsclc_fdg_pet`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_acrin_nsclc_fdg_pet` (acquisition/ranking.csv collection `idc:acrin_nsclc_fdg_pet`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `acrin_nsclc_fdg_pet`; TCIA DOI 10.7937/tcia.2019.30ilqfcl (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST_SCREEN:79;WB:18;ABD:14;CAP:8;OTHER:5;CA:4;AP:2;HN:1; BodyPartExamined in the manifest: (blank) 80, CHEST 30, ABDOMEN 20, THORAX 1; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

242 patients listed in IDC, 131 qualifying; manifest 131 series / 131 patients / 29,541 instances / 15.4 GB (catalogue series_size_MB); all CT in the collection 126.8 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/acrin_nsclc_fdg_pet/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_acrin_nsclc_fdg_pet_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `acrin_nsclc_fdg_pet:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:1056;localizer image type:525;non-axial reformat:180;< 60 slices:98 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_acrin_nsclc_fdg_pet` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="acrin_nsclc_fdg_pet"' $D/manifests/idc_tier1.csv > $D/manifests/idc_acrin_nsclc_fdg_pet.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_acrin_nsclc_fdg_pet.csv --batch 100`; must verify 131 series with 29,541 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cptac_stad` <a id="idc_cptac_stad"></a>

**IDC `cptac_stad`.** Cards: B (IDC `cptac_stad`). Structured entry: `sources.yaml` id `idc_cptac_stad`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cptac_stad` (acquisition/ranking.csv collection `idc:cptac_stad`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cptac_stad`; TCIA DOI 10.7937/jw9a-8k71 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:11;AP:6;ABD:2; BodyPartExamined in the manifest: CHESTABDPELVIS 10, ABDOMENPELVIS 5, ABDOMEN 3, CHEST 1; median SliceThickness 1 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

19 patients listed in IDC, 19 qualifying; manifest 19 series / 19 patients / 13,485 instances / 6.9 GB (catalogue series_size_MB); all CT in the collection 20.3 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cptac_stad/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cptac_stad_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cptac_stad:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:17;non-axial reformat:12;localizer image type:5;reformat/MIP series:2 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cptac_stad` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cptac_stad"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cptac_stad.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cptac_stad.csv --batch 100`; must verify 19 series with 13,485 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cptac_cm` <a id="idc_cptac_cm"></a>

**IDC `cptac_cm`.** Cards: B (IDC `cptac_cm`). Structured entry: `sources.yaml` id `idc_cptac_cm`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cptac_cm` (acquisition/ranking.csv collection `idc:cptac_cm`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cptac_cm`; TCIA DOI 10.7937/k9/tcia.2018.odu24gze (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CAP:4;WB:4;ABD:1;OTHER:1;PELVIS:1;CA:1; BodyPartExamined in the manifest: ABDOMEN 6, CHESTABDPELVIS 3, (blank) 2, PELVIS 1; median SliceThickness 2 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

12 patients listed in IDC, 12 qualifying; manifest 12 series / 12 patients / 8,020 instances / 4.1 GB (catalogue series_size_MB); all CT in the collection 11.6 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cptac_cm/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cptac_cm_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cptac_cm:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:34;no SliceThickness:8;localizer image type:4;non-axial reformat:3 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cptac_cm` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cptac_cm"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cptac_cm.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cptac_cm.csv --batch 100`; must verify 12 series with 8,020 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_cptac_sar` <a id="idc_cptac_sar"></a>

**IDC `cptac_sar`.** Cards: B (IDC `cptac_sar`). Structured entry: `sources.yaml` id `idc_cptac_sar`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_cptac_sar` (acquisition/ranking.csv collection `idc:cptac_sar`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `cptac_sar`; TCIA DOI 10.7937/tcia.2019.9bt23r95 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST:5;ABD:3;OTHER:3;WB:2;AP:1; BodyPartExamined in the manifest: (blank) 9, ABDOMEN 3, CHEST 1, WHOLEBODY 1; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

18 patients listed in IDC, 14 qualifying; manifest 14 series / 14 patients / 4,971 instances / 3.0 GB (catalogue series_size_MB); all CT in the collection 13.0 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/cptac_sar/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_cptac_sar_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `cptac_sar:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:35;slice > 3.0 mm:22;localizer image type:19;not a regularly spaced 3-D volume:8 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_cptac_sar` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="cptac_sar"' $D/manifests/idc_tier1.csv > $D/manifests/idc_cptac_sar.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_cptac_sar.csv --batch 100`; must verify 14 series with 4,971 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_pelvic_reference_data` <a id="idc_pelvic_reference_data"></a>

**IDC `pelvic_reference_data`.** Cards: B (IDC `pelvic_reference_data`). Structured entry: `sources.yaml` id `idc_pelvic_reference_data`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_pelvic_reference_data` (acquisition/ranking.csv collection `idc:pelvic_reference_data`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `pelvic_reference_data`; TCIA DOI 10.7937/tcia.2019.woskq5oo (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes PELVIS:53;OTHER:4;AP:1; BodyPartExamined in the manifest: (blank) 58; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

58 patients listed in IDC, 58 qualifying; manifest 58 series / 58 patients / 8,540 instances / 4.4 GB (catalogue series_size_MB); all CT in the collection 7.0 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/pelvic_reference_data/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_pelvic_reference_data_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `pelvic_reference_data:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): none (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_pelvic_reference_data` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="pelvic_reference_data"' $D/manifests/idc_tier1.csv > $D/manifests/idc_pelvic_reference_data.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_pelvic_reference_data.csv --batch 100`; must verify 58 series with 8,540 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_midrc_ricord_1a` <a id="idc_midrc_ricord_1a"></a>

**IDC `midrc_ricord_1a`.** Cards: B (IDC `midrc_ricord_1a`). Structured entry: `sources.yaml` id `idc_midrc_ricord_1a`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_midrc_ricord_1a` (acquisition/ranking.csv collection `idc:midrc_ricord_1a`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `midrc_ricord_1a`; TCIA DOI 10.7937/vtw4-x588 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes OTHER:56;CHEST_SCREEN:41;ABD:1; BodyPartExamined in the manifest: (blank) 76, CHEST 21, ABDOMEN 1; median SliceThickness 3 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY-NC 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

110 patients listed in IDC, 98 qualifying; manifest 98 series / 98 patients / 14,964 instances / 6.5 GB (catalogue series_size_MB); all CT in the collection 11.4 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/midrc_ricord_1a/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_midrc_ricord_1a_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `midrc_ricord_1a:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:74;localizer image type:15;slice > 3.0 mm:4;not a regularly spaced 3-D volume:3 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_midrc_ricord_1a` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="midrc_ricord_1a"' $D/manifests/idc_tier1.csv > $D/manifests/idc_midrc_ricord_1a.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_midrc_ricord_1a.csv --batch 100`; must verify 98 series with 14,964 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_rider_lung_pet_ct` <a id="idc_rider_lung_pet_ct"></a>

**IDC `rider_lung_pet_ct`.** Cards: B (IDC `rider_lung_pet_ct`). Structured entry: `sources.yaml` id `idc_rider_lung_pet_ct`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_rider_lung_pet_ct` (acquisition/ranking.csv collection `idc:rider_lung_pet_ct`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `rider_lung_pet_ct`; TCIA DOI 10.7937/k9/tcia.2015.ofip7tvm (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST_SCREEN:92;WB:19;ABD:5;CAP:1; BodyPartExamined in the manifest: CHEST 117; median SliceThickness 2.5 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 3.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

220 patients listed in IDC, 117 qualifying; manifest 117 series / 117 patients / 35,229 instances / 18.1 GB (catalogue series_size_MB); all CT in the collection 76.1 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/rider_lung_pet_ct/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_rider_lung_pet_ct_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `rider_lung_pet_ct:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): slice > 3.0 mm:273;localizer image type:113;< 60 slices:90;not a regularly spaced 3-D volume:67 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_rider_lung_pet_ct` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="rider_lung_pet_ct"' $D/manifests/idc_tier1.csv > $D/manifests/idc_rider_lung_pet_ct.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_rider_lung_pet_ct.csv --batch 100`; must verify 117 series with 35,229 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `idc_covid_19_ar` <a id="idc_covid_19_ar"></a>

**IDC `covid_19_ar`.** Cards: B (IDC `covid_19_ar`). Structured entry: `sources.yaml` id `idc_covid_19_ar`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

`idc_covid_19_ar` (acquisition/ranking.csv collection `idc:covid_19_ar`)

**Name and citation**

NCI Imaging Data Commons v24 collection_id `covid_19_ar`; TCIA DOI 10.7937/tcia.2020.py71-5978 (acquisition/ranking.csv; acquisition/census.json idc_version)

**Modality**

CT, one series per patient (widest coverage, then thickness nearest 1.25 mm); coverage classes CHEST_SCREEN:15;CAP:6;CA:2; BodyPartExamined in the manifest: CHEST 7, (blank) 7, CHESTABDPELVIS 5, CHESTABDOMEN 2; median SliceThickness 1 mm (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv; tools/acquisition_census.py)

**Position/view**

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_tier1.csv; tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

open, CC BY 4.0; derived labels allowed (yes); public IDC buckets, no sign-in (acquisition/ranking.csv)

**How it was acquired**

route IDC: `tools/acquisition_fetch.py idc --collection idc --manifest manifests/idc_tier1.csv --batch 100` (idc-index 0.12.5 + `s5cmd sync`, dirTemplate %collection_id/%PatientID/%SeriesInstanceUID); unit = series; verified when the .dcm count equals the manifest instanceCount (tools/acquisition_fetch.py; slurm/acquisition_submit.sh; acquisition/jobs.txt 40425851)

**When**

fetch job 40426149 submitted 2026-09-23; the pooled IDC fetch reached 2,700/3,600 series at about 21:25 EDT and 3,600/3,600 at 21:57 EDT that day (acquisition/jobs.txt); CEPH `data/idc` dated 2026-09-23 (listing); git log tools/acquisition_fetch.py: first commit 2026-09-24 8d6a4f4

**What it contains**

23 patients listed in IDC, 23 qualifying; manifest 23 series / 23 patients / 10,729 instances / 5.5 GB (catalogue series_size_MB); all CT in the collection 14.6 GB (acquisition/ranking.csv; acquisition/manifests/idc_tier1.csv)

**Where it is now**

CEPH raw DICOM `/rs/rs_grp_oschome/go2432/data/idc/raw/covid_19_ar/<PatientID>/<SeriesInstanceUID>/*.dcm`; fetch state `/rs/rs_grp_oschome/go2432/data/idc/fetch/` (verified.jsonl, failed.jsonl, FETCH_STATUS.json); converted `/rs/rs_grp_oschome/go2432/data/idc/nifti/idc_covid_19_ar_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

**Annotation status**

CT series only were fetched (no SEG/RTSTRUCT objects in the manifest) (acquisition/manifests/idc_tier1.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

**Derived products**

pooled with the other 38 collections under `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/idc/` (tools/acquisition_screen.py); patient key `covid_19_ar:<PatientID>` (docs/ruleclass/TIERS.md section 3); per-collection tier counts not split out (pooled idc: 3,499 CTs, tier 1 386, tier 2 2,577, untiered 536, alias candidates 185) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

census refusals (top four reasons, series): non-axial reformat:63;localizer image type:25;slice > 3.0 mm:24;< 60 slices:4 (acquisition/ranking.csv); per-collection converted count not copied locally: 3,499 of the 3,600 tier-1 series converted at <= 3 mm pooled over all 39 collections (acquisition/jobs.txt; docs/ruleclass/TIERS.md)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): manual, covered by idc_tier1; verification counts this collection's rows of verified.jsonl. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid idc_covid_19_ar` prints them. Where the text below differs, `sources.json` is the runnable form.*

on the grid: `D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; awk -F, 'NR==1 || $1=="covid_19_ar"' $D/manifests/idc_tier1.csv > $D/manifests/idc_covid_19_ar.csv; sbatch -D $D --job-name=acq_fetch_idc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection idc --manifest $D/manifests/idc_covid_19_ar.csv --batch 100`; must verify 23 series with 10,729 instances in total, FETCH_STATUS.json unresolved_failures 0 (acquisition/manifests/idc_tier1.csv; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); series UIDs are fixed, but the fetch uses whatever IDC release the installed idc-index serves, so a series withdrawn after v24 would fail (tools/acquisition_fetch.py route_idc)

---

### `tcia_fdg_pet_ct_lesions` <a id="tcia_fdg_pet_ct_lesions"></a>

**FDG-PET-CT-Lesions (autoPET), TCIA through NBIA.** Cards: B (FDG-PET-CT-Lesions (autoPET), TCIA through NBIA), E (tcia_fdg_pet_ct_lesions). Structured entry: `sources.yaml` id `tcia_fdg_pet_ct_lesions`; kind upstream_release; status on_disk; re-acquisition submit (nbia).

**Source id**

*[B]*

`tcia_fdg_pet_ct_lesions` (acquisition/ranking.csv collection `tcia:fdg_pet_ct_lesions`; slurm/acquisition_submit.sh)

*[E]*

`tcia_fdg_pet_ct_lesions`

**Name and citation**

*[B]*

FDG-PET-CT-Lesions (autoPET), TCIA DOI 10.7937/gkr0-xv29; not in IDC v24 (acquisition/ranking.csv)

*[E]*

TCIA FDG-PET-CT-Lesions (autoPET), 10.7937/gkr0-xv29 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

CT of whole-body FDG PET/CT (class WB, skull to thigh); the first study per patient (acquisition/ranking.csv; docs/CENSUS_TABLE_2026-09-25.md; tools/acquisition_census.py fdg_row)

*[E]*

PET/CT, whole body (skull to thigh) (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/nbia_fdg_pet_ct_lesions.csv; tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed; NBIA REST, no sign-in (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`) (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py nbia --collection tcia_fdg_pet_ct_lesions --manifest manifests/nbia_fdg_pet_ct_lesions.csv`: getImage per series (`services.cancerimagingarchive.net/nbia-api/services/v1/getImage?SeriesInstanceUID=`), zip unpacked, verified by instance count (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); manifest from the NBIA getSeries listing of 2026-09-23 (1,014 CT series, 900 patients), first study per patient (acquisition/ranking.csv; tools/acquisition_census.py fdg_row)

*[E]*

`python tools/acquisition_fetch.py nbia --collection tcia_fdg_pet_ct_lesions --manifest manifests/nbia_fdg_pet_ct_lesions.csv`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by zip integrity and instance count (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40426158 submitted 2026-09-23; 77/900 series at about 21:25 EDT 2026-09-23, 550/900 at 07:10 and 750/900 at 10:35 EDT 2026-09-24 (NBIA about 25 series per 20 min, 4-day limit, requeueable) (acquisition/jobs.txt); 900 cases by 2026-09-27 (docs/ruleclass/TIERS.md); completion time not recorded; CEPH `data/tcia_fdg_pet_ct_lesions` dated 2026-09-24 (listing)

*[E]*

`$RS/data/tcia_fdg_pet_ct_lesions` is dated 2026-09-24 in the listing; Slurm job fetch 40426158 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

manifest 900 series / 900 patients / 509,282 instances / 250.6 GB (acquisition/manifests/nbia_fdg_pet_ct_lesions.csv); all CT in the collection 275.9 GB (acquisition/ranking.csv); 900 NIfTI (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); du 367 GB (DICOM plus NIfTI) and 31 GB of screen output on 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

901 of 900 listed CTs on disk; 367 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/tcia_fdg_pet_ct_lesions/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/tcia_fdg_pet_ct_lesions/raw/<PatientID>/<SeriesInstanceUID>/`, `fetch/`, `nifti/fdg_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/tcia_fdg_pet_ct_lesions/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/tcia_fdg_pet_ct_lesions` (CEPH, raw, 367.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/tcia_fdg_pet_ct_lesions` (CEPH, converted/derived, 31.0 GB, listing 2026-09-25)

**Annotation status**

*[B]*

only the CT series listed in the manifest were fetched (no PET or SEG series) (acquisition/manifests/nbia_fdg_pet_ct_lesions.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 31 GB under `$RS/data/anomaly_harvest/tcia_fdg_pet_ct_lesions` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/tcia_fdg_pet_ct_lesions/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 900 CTs, tier 1 165, tier 2 695, untiered 40 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

7 tier-1 CTs have no SPINEPS mask (docs/ruleclass/TIERS.md section 5); the same Tübingen people appear in PanTSMini (894 autoPET volumes) and may appear in ENHANCE.PET 1.6k (acquisition/ranking.csv rows hf:BodyMaps/PanTSMini, scidb:enhance_pet_1.6k); SUMMARY.md not copied locally (acquisition/collections/)

*[E]*

none recorded beyond the census caveats

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid tcia_fdg_pet_ct_lesions` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_tcia_fdg_pet_ct_lesions ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh nbia --collection tcia_fdg_pet_ct_lesions --manifest $D/manifests/nbia_fdg_pet_ct_lesions.csv`; must verify 900 series / 509,282 instances (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; acquisition/manifests/nbia_fdg_pet_ct_lesions.csv); budget about 3 days at the measured NBIA rate (acquisition/jobs.txt)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` (block `tier1`), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `abdomenatlas3_mini` <a id="abdomenatlas3_mini"></a>

**AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images).** Cards: B (AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images)), E (abdomenatlas3_mini). Structured entry: `sources.yaml` id `abdomenatlas3_mini`; kind upstream_release; status on_disk; re-acquisition submit (hf).

**Source id**

*[B]*

`abdomenatlas3_mini` (acquisition/ranking.csv collection `hf:AbdomenAtlas/AbdomenAtlas3.0Mini`; slurm/acquisition_submit.sh)

*[E]*

`abdomenatlas3_mini`

**Name and citation**

*[B]*

AbdomenAtlas 3.0 Mini, Hugging Face `AbdomenAtlas/AbdomenAtlas3.0Mini`; source list in arXiv 2407.16697 Table 1 (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 5)

*[E]*

AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images), HF dataset AbdomenAtlas/AbdomenAtlas3.0Mini (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

abdominal CT, an aggregator of LiTS, KiTS, AbdomenCT-1K, FLARE'23, Pancreas-CT, CT-ORG, CHAOS, MSD-CT, BTCV, AMOS22 (200) and WORD (120); coverage from per-CT z-extent (about a third reach T1) (acquisition/ranking.csv; docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

CT, abdomen; per-CT extent, about a third reach T1 (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY-NC-SA 4.0, derived labels allowed under share-alike; HF dataset ungated when read on 2026-09-23 (acquisition/ranking.csv)

*[E]*

CC BY-NC-SA 4.0, open (HF, ungated); derived labels allowed, share-alike (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py hf --collection abdomenatlas3_mini --repo AbdomenAtlas/AbdomenAtlas3.0Mini --include '^image_only/'`: each LFS file by HTTP Range resume from `resolve/main`, verified against the Hub's LFS sha256, then untarred (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); census coverage from the release metadata (`AbdomenAtlas3.0MiniWithMeta.csv`, used as `--aa3-meta`) (tools/acquisition_census.py; slurm/acquisition_fetch_smoke.sh)

*[E]*

`python tools/acquisition_fetch.py hf --collection abdomenatlas3_mini --repo AbdomenAtlas/AbdomenAtlas3.0Mini --include '^image_only/'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by HF LFS sha256 per file (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40426167 submitted 2026-09-23; 5/40 tars at about 21:25 EDT, 40/40 at 05:08 EDT 2026-09-24 (about 22 min per 14 GB tar) (acquisition/jobs.txt); CEPH `data/abdomenatlas3_mini` dated 2026-09-23 (listing); HF commit not recorded (tools/acquisition_fetch.py)

*[E]*

`$RS/data/abdomenatlas3_mini` is dated 2026-09-23 in the listing; Slurm job fetch 40426167 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

9,262 CT listed, 40 image tars, 570.7 GB; 7,835 at <= 3 mm by metadata (1,427 thicker) (acquisition/ranking.csv); 7,649 usable at convert (acquisition/jobs.txt; acquisition/ACQUISITION_PLAN.md section 9; docs/ruleclass/TIERS.md); du 532 GB raw and 107 GB screen output on 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

7,650 of 7,835 listed CTs on disk; 532 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/abdomenatlas3_mini/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/abdomenatlas3_mini/raw/**/BDMAP_*/ct.nii.gz` (used in place: NIfTI-route CTs are not copied), `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/abdomenatlas3_mini/` (tools/acquisition_screen.py; slurm/acquisition_submit.sh; listing); nothing on HOME (listing)

*[E]*

`$RS/data/abdomenatlas3_mini` (CEPH, raw, 532.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/abdomenatlas3_mini` (CEPH, converted/derived, 107.0 GB, listing 2026-09-26)

**Annotation status**

*[B]*

only the `image_only/` tars were fetched, so no release mask is on disk (slurm/acquisition_submit.sh); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 107 GB under `$RS/data/anomaly_harvest/abdomenatlas3_mini` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/abdomenatlas3_mini/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 7,649 CTs, tier 1 1,069, tier 2 4,715, untiered 1,865, alias candidates 687 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

BDMAP ids are volumes, not people: FLARE and KiTS can hold two scans of one person (acquisition/ACQUISITION_PLAN.md section 5); whether RSNA trauma series are among the 9,262 is unpublished (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 9); 13 tier-1 CTs have no SPINEPS mask (docs/ruleclass/TIERS.md section 5); the HF fetch is not pinned to a revision (`resolve/main`) (tools/acquisition_fetch.py route_hf); also inside it: CTSpine1K MSD-T10 150 and PANORAMA's 274 MSD/NIH cases (acquisition/ranking.csv)

*[E]*

overlaps FLARE and KiTS, so some people appear more than once (`CENSUS_TABLE_2026-09-25.md` caveats)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid abdomenatlas3_mini` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_abdomenatlas3_mini ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh hf --collection abdomenatlas3_mini --repo AbdomenAtlas/AbdomenAtlas3.0Mini --include '^image_only/'`; must verify 40 tars by LFS sha256 and 9,262 `ct.nii.gz`; record the HF commit hash, which the tool does not (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; acquisition/ranking.csv)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` (block `tier1`), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `amos22` <a id="amos22"></a>

**AMOS22 CT, unlabelled (ids 5000-6899) and labelled.** Cards: B (AMOS22 CT, unlabelled (ids 5000-6899) and labelled), E (amos22). Structured entry: `sources.yaml` id `amos22`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`amos22` (acquisition/ranking.csv collections `zenodo:amos22_unlabelled_ct`, `zenodo:amos22_labelled_ct`; slurm/acquisition_submit.sh `chain amos22`)

*[E]*

`amos22`

**Name and citation**

*[B]*

AMOS: a large-scale abdominal multi-organ benchmark (unlabelled CT parts and the labelled set), release pages zenodo.org/records/7262757, 7295661, 7262581 (acquisition/ranking.csv); Zenodo 7262757 published 2022-10-29, 7295661 published 2022-10-31, 7262581 published 2022-11-28 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

AMOS22 CT, labelled + unlabelled, Zenodo 7262757, 7295661, 7262581 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

abdominal CT from Longgang hospitals, class ABD assumed from the source description; the labelled zip also holds 100 MR (ids 0500-0600, excluded at convert) (acquisition/ranking.csv; slurm/acquisition_submit.sh)

*[E]*

CT, abdomen (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection amos22 --record 7262757 7295661 7262581 --include '(amos22_unlabeled_ct_[0-9_]+\.zip|amos22\.zip)$'`, md5 per zip; convert glob `**/amos_*.nii.gz`, excluding labels and MR (slurm/acquisition_submit.sh; tools/acquisition_fetch.py)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection amos22 --record 7262757 7295661 7262581 --include '(amos22_unlabeled_ct_[0-9_]+\.zip\|amos22\.zip)$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 per file (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40426176 submitted 2026-09-23; 1/5 zips at about 21:25 EDT, 5/5 at 01:07 EDT 2026-09-24; SPINEPS 681/723 at 10:35 EDT 2026-09-24 (acquisition/jobs.txt); CEPH `data/amos22` dated 2026-09-23 (listing)

*[E]*

`$RS/data/amos22` is dated 2026-09-23 in the listing; Slurm job fetch 40426176 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

listed 1,900 unlabelled (78.4 GB, 4 zips) + 500 labelled CT (24.2 GB, one zip, 300 new) (acquisition/ranking.csv); 2,364 CT converted: 723 at <= 3 mm, 1,564 refused as thicker, 67 duplicates inside AMOS (acquisition/ACQUISITION_PLAN.md section 9); du 96 GB raw and 13 GB screen output on 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

724 of 2,200 listed CTs on disk; 96 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/amos22/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/amos22/raw/<record>/...` (NIfTI used in place), `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/amos22/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/amos22` (CEPH, raw, 96.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/amos22` (CEPH, converted/derived, 13.0 GB, listing 2026-09-24)

**Annotation status**

*[B]*

files under `/labels` in the labelled zip are excluded at convert (`--exclude '/labels|...'`); whether they were kept on disk after unpack is not recorded (slurm/acquisition_submit.sh); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); screen complete: L6 two-labeller 9, single 11; T13 single 2; review 44; unassigned 24; 90 registry rows (docs/CENSUS_TABLE_2026-09-25.md) (review 46 in SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 13 GB under `$RS/data/anomaly_harvest/amos22` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/amos22/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 723 CTs, tier 1 90, tier 2 630, untiered 3, alias candidates 48 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

two thirds thicker than 3 mm, so its yield is about a third of the ranked E (acquisition/ACQUISITION_PLAN.md section 9); 723 + 1,564 + 67 = 2,354, ten short of 2,364, unexplained (acquisition/ACQUISITION_PLAN.md section 9); the unlabelled set has no patient ids, so people versus volumes is unknown (docs/CENSUS_TABLE_2026-09-25.md caveats); 200 labelled CTs are AbdomenAtlas people (acquisition/ranking.csv); review count 44 vs 46 between two documents (docs/CENSUS_TABLE_2026-09-25.md; SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); SUMMARY.md not copied locally (acquisition/collections/)

*[E]*

the unlabelled set has no patient ids (`CENSUS_TABLE_2026-09-25.md` caveats); MR ids 0500-0600 are excluded at convert (`nnunet:slurm/acquisition_submit.sh` comment)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid amos22` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_amos22 ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection amos22 --record 7262757 7295661 7262581 --include '(amos22_unlabeled_ct_[0-9_]+\.zip|amos22\.zip)$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); must verify 5 zips by md5

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` (block `tier1`), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `nlst_pilot` <a id="nlst_pilot"></a>

**NLST, the seeded 500-person pilot.** Cards: B (NLST, the seeded 500-person pilot), E (nlst_pilot). Structured entry: `sources.yaml` id `nlst_pilot`; kind upstream_release; status on_disk; re-acquisition submit (idc).

**Source id**

*[B]*

`nlst_pilot` (slurm/acquisition_submit.sh `chain nlst_pilot`; acquisition/ranking.csv collection `idc:nlst`)

*[E]*

`nlst_pilot`

**Name and citation**

*[B]*

National Lung Screening Trial in IDC v24, TCIA DOI 10.7937/tcia.hmq8-j677; 500 series sampled with `random.Random(20260923)` from the census's NLST manifest (acquisition/ranking.csv; tools/acquisition_census.py)

*[E]*

NLST 500-person pilot via IDC (`manifests/idc_nlst_pilot500.csv`), 10.7937/tcia.hmq8-j677 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

low-dose screening chest CT (class CHEST_SCREEN; caudal limit the adrenals, so no lumbosacral count by protocol) (acquisition/ACQUISITION_PLAN.md section 2; acquisition/manifests/idc_nlst_pilot500.csv)

*[E]*

low-dose chest CT; the caudal limit is the adrenals (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the manifest carries no PatientPosition column, and DICOM (0018,5100) was not extracted at convert (acquisition/manifests/idc_nlst_pilot500.csv; tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0 (acquisition/ranking.csv; acquisition/manifests/idc_nlst_pilot500.csv)

*[E]*

CC BY 4.0, open (`ranking.csv` row idc:nlst) (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py idc --collection nlst_pilot --manifest manifests/idc_nlst_pilot500.csv --batch 100`, instance count per series (slurm/acquisition_submit.sh; tools/acquisition_fetch.py)

*[E]*

`python tools/acquisition_fetch.py idc --collection nlst_pilot --manifest manifests/idc_nlst_pilot500.csv --batch 100`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by instance count per series (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40426185 submitted 2026-09-23, 500/500 verified by about 21:25 EDT; chain finished 08:03 EDT 2026-09-24; call and summary requeued under the T13 rib rule (40436963-40436965), done 10:50 EDT (acquisition/jobs.txt); CEPH `data/nlst_pilot` dated 2026-09-23 (listing)

*[E]*

`$RS/data/nlst_pilot` is dated 2026-09-23 in the listing; Slurm job fetch 40426185 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

500 series / 500 patients / 89,363 instances / 45.8 GB (acquisition/manifests/idc_nlst_pilot500.csv); 500 converted, 498 through the gate (acquisition/collections/nlst_pilot/SUMMARY.md); du 69 GB raw and 7 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

501 of 500 listed CTs on disk; 69 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/nlst_pilot/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/nlst_pilot/raw/nlst/<PatientID>/<SeriesInstanceUID>/`, `fetch/`, `nifti/nlstpilot_nlst_<PatientID>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/nlst_pilot/` incl. `t13_check/` and `review/` (tools/acquisition_fetch.py; tools/acquisition_screen.py; listing); copies in the repository `acquisition/collections/nlst_pilot/` (acquisition/ACQUISITION_PLAN.md)

*[E]*

`$RS/data/nlst_pilot` (CEPH, raw, 69.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/nlst_pilot` (CEPH, converted/derived, 7.0 GB, listing 2026-09-24)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); after the rib rule: 338 with a count from T1, 0 with a lumbosacral count, 5 T13 single-labeller (renders await Greg), 495 no_count (acquisition/collections/nlst_pilot/SUMMARY.md; acquisition/ACQUISITION_PLAN.md section 11)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 7 GB under `$RS/data/anomaly_harvest/nlst_pilot` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/nlst_pilot/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); `acquisition/collections/nlst_pilot/{SUMMARY.md,rows.csv,registry_rows.csv,review/,t13_check/}`; tiers: 500 CTs, tier 1 5, tier 2 484, untiered 11 (docs/ruleclass/TIERS.md; acquisition/ACQUISITION_PLAN.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

VERIDAH's first T13 rate (34 of 367, 9.3 %) was wrong; 29 of 34 names had no whole rib on the named body; rule `confirm_t13_by_rib` added (acquisition/ACQUISITION_PLAN.md section 11); labeller B cannot count the cage on chest CT (merged apical body components), recorded, not fixed (acquisition/ACQUISITION_PLAN.md section 11)

*[E]*

0 lumbosacral counts, which the plan predicted (`CENSUS_TABLE_2026-09-25.md` caveats)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid nlst_pilot` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_nlst_pilot ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh idc --collection nlst_pilot --manifest $D/manifests/idc_nlst_pilot500.csv --batch 100`; must verify 500 series / 89,363 instances; the committed manifest makes the sample exact (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; acquisition/manifests/idc_nlst_pilot500.csv)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` (block `tier1`), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `csi2014` <a id="csi2014"></a>

**CSI 2014 spine CT.** Cards: B (CSI 2014 spine CT), E (csi2014). Structured entry: `sources.yaml` id `csi2014`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`csi2014` (acquisition/ranking.csv collection `zenodo:csi2014`; slurm/acquisition_submit.sh)

*[E]*

`csi2014`

**Name and citation**

*[B]*

CSI 2014 spine CT (20); release page zenodo.org/records/7049844 (publication date not in the sweep) (acquisition/ranking.csv; acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

CSI 2014 spine CT, Zenodo 7049844 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

thoracolumbar spine CT (class SPINE), MHA (acquisition/ranking.csv; docs/CENSUS_TABLE_2026-09-25.md; slurm/acquisition_submit.sh)

*[E]*

CT, thoracolumbar spine (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, ODC-By (acquisition/ranking.csv)

*[E]*

ODC-By, open (`ranking.csv`) (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection csi2014 --record 7049844 --include '_image\.mha$'`, md5; MHA written to NIfTI with SimpleITK (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; tools/acquisition_screen.py)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection csi2014 --record 7049844 --include '_image\.mha$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40426203 submitted 2026-09-23, 20/20 by about 21:25 EDT; screen finished by 07:10 EDT 2026-09-24 (acquisition/jobs.txt); CEPH `data/csi2014` dated 2026-09-23 (listing)

*[E]*

`$RS/data/csi2014` is dated 2026-09-23 in the listing; Slurm job fetch 40426203 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

20 CT, 3.6 GB (acquisition/ranking.csv); 20 verified, 20 usable, 20 gated (acquisition/collections/csi2014/SUMMARY.md); du 7 GB raw, 3 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

21 of 20 listed CTs on disk; 7 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/csi2014/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/csi2014/raw/7049844/*_image.mha`, `nifti/csi_<n>_ct.nii.gz`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/csi2014/` (tools/acquisition_screen.py; listing)

*[E]*

`$RS/data/csi2014` (CEPH, raw, 7.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/csi2014` (CEPH, converted/derived, 3.0 GB, listing 2026-09-23)

**Annotation status**

*[B]*

only `_image.mha` files were fetched; anything else in the record was not (slurm/acquisition_submit.sh); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); 17 ordinary (3 two-labeller), 2 unassigned, 1 no_count (acquisition/collections/csi2014/SUMMARY.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 3 GB under `$RS/data/anomaly_harvest/csi2014` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/csi2014/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); copies `acquisition/collections/csi2014/`; tiers: 20 CTs, tier 1 2, tier 2 18 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

none recorded beyond one no-count CT (acquisition/collections/csi2014/SUMMARY.md)

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid csi2014` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_csi2014 ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection csi2014 --record 7049844 --include '_image\.mha$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); must verify 20 files by md5

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` (block `tier1`), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`


Known defects and gaps for this group:
- AbdomenAtlas overlaps FLARE and KiTS, so some people appear more than once.
- AMOS's unlabelled set has no patient ids.
- The FOV gate disagrees with the class prior on PENGWIN (12 of 341 CTs pass) and on NLST (0 lumbosacral counts) (`CENSUS_TABLE_2026-09-25.md` caveats).
- `CENSUS_TABLE_2026-09-25.md` 1 lists `validation_ts` (71 TotalSegmentator v2 CTs with external labels) as a 1 GB raw link set. It belongs to `totalsegmentator_v2`.

---

### Group B2. The validation set run through the same chain

### `validation_ts` <a id="validation_ts"></a>

**TotalSegmentator v2, the 70 outside-labelled CTs run through the same chain.** Cards: B (TotalSegmentator v2, the 70 outside-labelled CTs run through the same chain). Structured entry: `sources.yaml` id `validation_ts`; kind derived; status on_disk; re-acquisition submit (symlink).

**Source id**

`validation_ts` (slurm/acquisition_submit.sh `validation`; slurm/acquisition_validation_prep.sh)

**Name and citation**

TotalSegmentator v2 CTs scored against fhofmann/VertebralBodiesCT-Labels `data.csv` (external L6 and T13); the CTs themselves belong to the TotalSegmentator family (acquisition/validation/VALIDATION.md; slurm/acquisition_validation_prep.sh)

**Modality**

CT, mixed study types; 35 positives (28 L6, 7 T13) and 35 seeded negatives (acquisition/ACQUISITION_PLAN.md section 6; acquisition/validation_cases.csv)

**Position/view**

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

**Licence and access**

not stated in the acquisition files; see the TotalSegmentator family card (acquisition/ACQUISITION_PLAN.md)

**How it was acquired**

not downloaded: `slurm/acquisition_validation_prep.sh` symlinks `data/validation_ts/raw/<s####>.nii.gz` to `$HOME/data/TotalSegmentator/<s####>/ct.nii.gz` for every case in `validation_cases.csv` (written by tools/acquisition_validation_cases.py) (slurm/acquisition_validation_prep.sh)

**When**

prep 40425899 and chain 40425900-40425907 on 2026-09-23; rescored 40428080; requeued under the T13 rib rule 40436966-40436969 on 2026-09-24 (acquisition/jobs.txt); CEPH `data/validation_ts` dated 2026-09-23 (listing)

**What it contains**

70 CTs; 69 through the gate; 61 with a lumbosacral count, 36 with a count from T1 (acquisition/validation/SUMMARY.md)

**Where it is now**

CEPH `/rs/rs_grp_oschome/go2432/data/validation_ts/raw/` (symlinks into HOME `~/data/TotalSegmentator/`) and `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/validation_ts/` (VALIDATION.md, t13_check/) (slurm/acquisition_validation_prep.sh; listing; SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md)

**Annotation status**

external read of L6/T13 by the VertebralBodiesCT-Labels authors (free L6 only) plus the two pseudo-labellers (acquisition/validation/VALIDATION.md)

**Derived products**

`acquisition/validation/{VALIDATION.md,SUMMARY.md,rows.csv,validation.json,vts_s0049.png,vts_s0616.png,t13_check/}` (acquisition/ACQUISITION_PLAN.md section 6); folded onto the TS scans in the tiers (70 names) (docs/ruleclass/TIERS.md)

**Known defects and gaps**

TotalSegmentator trained on these CTs, so labeller B is scored on its training images; labeller B was tuned on the same 70, so the numbers are an upper bound; 3 of 69 SPINEPS runs failed inside SPINEPS (acquisition/ACQUISITION_PLAN.md section 6; acquisition/jobs.txt)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid validation_ts` prints them. Where the text below differs, `sources.json` is the runnable form.*

re-link: `sbatch -D /rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition ~/spinesurg-ct-nnunet/slurm/acquisition_validation_prep.sh` (needs the TotalSegmentator v2 tree on HOME), then `acquisition_submit.sh validation` (slurm/acquisition_validation_prep.sh; slurm/acquisition_submit.sh)

---

### Group B3. Tier 1, late (found and submitted 2026-09-24)

### `panorama` <a id="panorama"></a>

**PANORAMA public training set.** Cards: B (PANORAMA public training set), E (panorama). Structured entry: `sources.yaml` id `panorama`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`panorama` (acquisition/ranking.csv collection `zenodo:panorama`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`panorama`

**Name and citation**

*[B]*

PANORAMA public training set (2,238 CECT; 2,224 patient ids); release page zenodo.org/records/13715870 (+3); zip central directories read 2026-09-24 (acquisition/ranking.csv); Zenodo 13715870 published 2024-09-06, 13742336 published 2024-09-10, 11034011 published 2024-04-22, 10999754 published 2024-04-22 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

PANORAMA, pancreas CE-CT, Zenodo 13715870, 13742336, 11034011, 10999754 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

contrast-enhanced pancreatic CT (Radboudumc + UMCG), NIfTI `*_0000.nii.gz`; per batch P(both) 0.43-0.57 (acquisition/census_addendum.json per_batch); header sample: 160 of 2,238 images read by HTTP range (seed 20260924), 89.4 % at <= 3 mm, median craniocaudal extent 445 mm, P(both LS references) 0.505 / P(cage from T1) 0.311 per CT (acquisition/census_addendum.json)

*[E]*

CE-CT, abdomen (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY-NC 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY-NC 4.0, open (`ranking.csv`) (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection panorama --record 13715870 13742336 11034011 10999754 --include '^batch_[1-4]\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/*_0000.nii.gz`, person `([0-9]{6})_[0-9]{5}_0000` (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection panorama --record 13715870 13742336 11034011 10999754 --include '^batch_[1-4]\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430881 submitted 2026-09-24 (acquisition/jobs.txt); running since 06:43 EDT, 0/4 zips verified at 10:35 EDT 2026-09-24 (acquisition/jobs.txt); 2,026 cases counted 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md), 2,024 on 2026-09-27 (docs/ruleclass/TIERS.md); fetch completion time not recorded; CEPH `data/panorama` dated 2026-09-24, `anomaly_harvest/panorama` dated 2026-09-27 (listing)

*[E]*

`$RS/data/panorama` is dated 2026-09-24 in the listing; Slurm job fetch 40430881 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

2,224 listed, 1,950 new; 194.2 GB by the record (acquisition/ranking.csv); 2,238 volumes, 2,224 distinct patient ids (11 with more than one volume) (acquisition/census_addendum.json); 194 MSD + 80 NIH Pancreas-CT cases inside are AbdomenAtlas people (acquisition/ranking.csv); du 182 GB raw, 16 GB screen output on 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

2,026 of 2,238 listed CTs on disk; 182 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/panorama/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/panorama/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/panorama/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/panorama` (CEPH, raw, 182.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/panorama` (CEPH, converted/derived, 16.0 GB, listing 2026-09-27)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); no calls: SPINEPS 40430887 had 910 masks of 1,494 gate-passed CTs at 00:30 EDT 2026-09-27 (docs/ruleclass/TIERS.md section 5), 1,495 masks and 131 review calls at 12:23 (docs/ruleclass/PREREG_rules.md section 0); the acq_*_panorama jobs were cancelled at 15:50 EDT that day, so call 40430888 and summary 40430889 never wrote rows.csv (docs/grid_records/JOBS_RECORD_2026-09-27_1544.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 16 GB under `$RS/data/anomaly_harvest/panorama` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/panorama/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers (2026-09-27): 2,024 CTs, tier 1 0, tier 2 910, untiered 1,114, alias candidates 80 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

screen incomplete (see Annotation status) (docs/grid_records/JOBS_RECORD_2026-09-27_1544.md; docs/ruleclass/TIERS.md); 1 PANORAMA CT is the same voxels as a Kidney thorax-abdomen CT (docs/ruleclass/TIERS.md); a 450 mm pancreatic CT may be centred higher than the extent bins assume (acquisition/ACQUISITION_PLAN.md section 9); FETCH_STATUS.json not read

*[E]*

FOV gate pending at the census

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid panorama` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_panorama ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection panorama --record 13715870 13742336 11034011 10999754 --include '^batch_[1-4]\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" panorama` (slurm/acquisition_submit.sh); must verify 4 zips by md5 and 2,238 `_0000.nii.gz` volumes (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' panorama` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `barts_crl` <a id="barts_crl"></a>

**Barts CRL (colorectal-cancer staging CT).** Cards: B (Barts CRL (colorectal-cancer staging CT)), E (barts_crl). Structured entry: `sources.yaml` id `barts_crl`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`barts_crl` (acquisition/ranking.csv collection `zenodo:barts_crl`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`barts_crl`

**Name and citation**

*[B]*

Barts CRL: colorectal-cancer staging CT, three London hospitals (220 CT); release page zenodo.org/records/14004841 (acquisition/ranking.csv); Zenodo 14004841 published 2024-10-29 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

Barts CRL (colorectal liver), Zenodo 14004841 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

colorectal-cancer staging CT, three London hospitals (St Bartholomew's, Royal London, Newham, 2014-19), class AP/CAP (acquisition/ranking.csv); header sample: 40 of 220 images read by HTTP range (seed 20260924), 100.0 % at <= 3 mm, median craniocaudal extent 457 mm, P(both LS references) 0.732 / P(cage from T1) 0.386 per CT (acquisition/census_addendum.json)

*[E]*

CT, abdomen (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection barts_crl --record 14004841 --include '^images\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/images/crc_*.nii.gz`, person `crc_(CRC[0-9]+)_` (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection barts_crl --record 14004841 --include '^images\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430890 submitted 2026-09-24 (acquisition/jobs.txt); TotalSegmentator partial on 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); SPINEPS running 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); fetch completion time not recorded; CEPH `data/barts_crl` dated 2026-09-24, `anomaly_harvest/barts_crl` dated 2026-09-25 (listing)

*[E]*

`$RS/data/barts_crl` is dated 2026-09-24 in the listing; Slurm job fetch 40430890 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

220 listed, 220 new; 20.32 GB by the record (acquisition/ranking.csv); 212 cases on 2026-09-27 (docs/ruleclass/TIERS.md); du 19 GB raw, 6 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

213 CTs on disk; 19 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/barts_crl/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/barts_crl/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/barts_crl/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/barts_crl` (CEPH, raw, 19.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/barts_crl` (CEPH, converted/derived, 6.0 GB, listing 2026-09-25)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 6 GB under `$RS/data/anomaly_harvest/barts_crl` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/barts_crl/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 212 CTs, tier 1 46, tier 2 162, untiered 4, alias candidates 2 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

212 of 220 usable, refusal reasons in `convert_summary.json` not copied locally (docs/ruleclass/TIERS.md; acquisition/ranking.csv); screen state after 2026-09-25 not recorded locally (46 tier-1 CTs imply calls ran) (docs/CENSUS_TABLE_2026-09-25.md; docs/ruleclass/TIERS.md)

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid barts_crl` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_barts_crl ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection barts_crl --record 14004841 --include '^images\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" barts_crl` (slurm/acquisition_submit.sh); must verify `images.zip` by md5 and 220 CTs (acquisition/ranking.csv)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' barts_crl` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `kidney_thoraxabdomen` <a id="kidney_thoraxabdomen"></a>

**Kidney abnormality segmentation in thorax-abdomen CT.** Cards: B (Kidney abnormality segmentation in thorax-abdomen CT), E (kidney_thoraxabdomen). Structured entry: `sources.yaml` id `kidney_thoraxabdomen`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`kidney_thoraxabdomen` (acquisition/ranking.csv collection `zenodo:kidney_thoraxabdomen`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`kidney_thoraxabdomen`

**Name and citation**

*[B]*

Kidney abnormality segmentation in thorax-abdomen CT (215 CT); release page zenodo.org/records/8014290 (acquisition/ranking.csv); Zenodo 8014290 published 2023-06-07 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

Kidney thorax-abdomen CT, Zenodo 8014290 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

thorax-abdomen CT, institution not stated, MHA, class CA (acquisition/ranking.csv; slurm/acquisition_submit.sh); header sample: 60 of 215 images read by HTTP range (seed 20260924), 100.0 % at <= 3 mm, median craniocaudal extent 657 mm, P(both LS references) 0.926 / P(cage from T1) 0.882 per CT (acquisition/census_addendum.json)

*[E]*

CT, chest + abdomen (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection kidney_thoraxabdomen --record 8014290 --include '^images[1-4]\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert MHA glob `**/images[0-9]/*.mha` -> NIfTI, person `images[0-9]/([0-9]+)\.mha` (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection kidney_thoraxabdomen --record 8014290 --include '^images[1-4]\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430899 submitted 2026-09-24 (acquisition/jobs.txt); 2/4 zips at 10:35 EDT 2026-09-24 (acquisition/jobs.txt); state 'converted only' on 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); SPINEPS running 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/kidney_thoraxabdomen` dated 2026-09-24, `anomaly_harvest/kidney_thoraxabdomen` dated 2026-09-26 (listing)

*[E]*

`$RS/data/kidney_thoraxabdomen` is dated 2026-09-24 in the listing; Slurm job fetch 40430899 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

215 listed, 215 new; 38.35 GB by the record (acquisition/ranking.csv); 215 cases (docs/ruleclass/TIERS.md); du 71 GB raw (MHA plus NIfTI), 9 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

216 CTs on disk; 71 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/kidney_thoraxabdomen/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/kidney_thoraxabdomen/raw/<record>/...`, `nifti/kidta_<n>_ct.nii.gz`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/kidney_thoraxabdomen/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/kidney_thoraxabdomen` (CEPH, raw, 71.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/kidney_thoraxabdomen` (CEPH, converted/derived, 9.0 GB, listing 2026-09-26)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 9 GB under `$RS/data/anomaly_harvest/kidney_thoraxabdomen` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/kidney_thoraxabdomen/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 215 CTs, tier 1 39, tier 2 176, one PANORAMA CT folded onto it, alias candidates 1 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

one scan per file and people not stated, so n_new counts scans (acquisition/ranking.csv); 1 tier-1 CT has no SPINEPS mask (docs/ruleclass/TIERS.md section 5); screen state after 2026-09-25 not recorded locally (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid kidney_thoraxabdomen` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_kidney_thoraxabdomen ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection kidney_thoraxabdomen --record 8014290 --include '^images[1-4]\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" kidney_thoraxabdomen` (slurm/acquisition_submit.sh); must verify 4 zips by md5 and 215 MHA (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' kidney_thoraxabdomen` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `curvas_pdacvi` <a id="curvas_pdacvi"></a>

**CURVAS-PDACVI (MICCAI 2025).** Cards: B (CURVAS-PDACVI (MICCAI 2025)), E (curvas_pdacvi). Structured entry: `sources.yaml` id `curvas_pdacvi`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`curvas_pdacvi` (acquisition/ranking.csv collection `zenodo:curvas_pdacvi`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`curvas_pdacvi`

**Name and citation**

*[B]*

CURVAS-PDACVI (MICCAI 2025; 109 CT); release page zenodo.org/records/17552201 (acquisition/ranking.csv); Zenodo 17552201 published 2025-11 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

CURVAS-PDAC-VI, Zenodo 17552201 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

abdominal CT (pancreatic adenocarcinoma vascular invasion), class ABD/CAP (acquisition/ranking.csv); header sample: 45 of 109 images read by HTTP range (seed 20260924), 93.3 % at <= 3 mm, median craniocaudal extent 471 mm, P(both LS references) 0.683 / P(cage from T1) 0.409 per CT (acquisition/census_addendum.json)

*[E]*

CT, abdomen (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection curvas_pdacvi --record 17552201 --include '\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/image.nii.gz`, person `(CURVASPDAC_[0-9]+)/image\.nii\.gz` (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection curvas_pdacvi --record 17552201 --include '\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430908 submitted 2026-09-24 (acquisition/jobs.txt); gate done, calls pending on 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); called by 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/curvas_pdacvi` dated 2026-09-24, `anomaly_harvest/curvas_pdacvi` dated 2026-09-24 (listing)

*[E]*

`$RS/data/curvas_pdacvi` is dated 2026-09-24 in the listing; Slurm job fetch 40430908 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

109 listed, 109 new; 15.42 GB by the record (acquisition/ranking.csv); 101 cases (docs/ruleclass/TIERS.md); du 16 GB raw, 4 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

102 CTs on disk; 16 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/curvas_pdacvi/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/curvas_pdacvi/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/curvas_pdacvi/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/curvas_pdacvi` (CEPH, raw, 16.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/curvas_pdacvi` (CEPH, converted/derived, 4.0 GB, listing 2026-09-24)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); T13 single-labeller 1, review 11; 12 registry rows (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 4 GB under `$RS/data/anomaly_harvest/curvas_pdacvi` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/curvas_pdacvi/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 101 CTs, tier 1 12, tier 2 82, untiered 7, alias candidates 78 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

78 of 101 CTs are near-duplicate candidates (thumbnail NCC >= 0.98), consistent with the expected overlap with CURVAS 2024; not merged (docs/ruleclass/TIERS.md; acquisition/ranking.csv)

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid curvas_pdacvi` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_curvas_pdacvi ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection curvas_pdacvi --record 17552201 --include '\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" curvas_pdacvi` (slurm/acquisition_submit.sh); must verify 3 zips by md5 and 109 `image.nii.gz` (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' curvas_pdacvi` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `aortaseg60` <a id="aortaseg60"></a>

**AortaSeg-60.** Cards: B (AortaSeg-60), E (aortaseg60). Structured entry: `sources.yaml` id `aortaseg60`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`aortaseg60` (acquisition/ranking.csv collection `zenodo:aortaseg60`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`aortaseg60`

**Name and citation**

*[B]*

AortaSeg-60 (60 CTA / non-contrast aorta CT); release page zenodo.org/records/18147026 (acquisition/ranking.csv); Zenodo 18147026 published 2026-01-04 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

AortaSeg60, Zenodo 18147026 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

CT angiography and non-contrast aorta CT, chest-abdomen-pelvis (class CAP) (acquisition/ranking.csv; docs/CENSUS_TABLE_2026-09-25.md); header sample: 36 of 60 images read by HTTP range (seed 20260924), 100.0 % at <= 3 mm, median craniocaudal extent 661 mm, P(both LS references) 0.935 / P(cage from T1) 0.925 per CT (acquisition/census_addendum.json)

*[E]*

CTA, chest + abdomen + pelvis (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC0 1.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC0 1.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection aortaseg60 --record 18147026 --include '^(Ven|Anev|Dissec|Old|Nat|Young)\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/nifti/*_image.nii.gz`, excluding `__MACOSX`, person `([A-Za-z]+_[0-9]+)_image` (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection aortaseg60 --record 18147026 --include '^(Ven\|Anev\|Dissec\|Old\|Nat\|Young)\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430917 submitted 2026-09-24 (acquisition/jobs.txt); gate done on 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); called by 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/aortaseg60` dated 2026-09-24, `anomaly_harvest/aortaseg60` dated 2026-09-24 (listing)

*[E]*

`$RS/data/aortaseg60` is dated 2026-09-24 in the listing; Slurm job fetch 40430917 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

60 listed, 60 new; 15.87 GB by the record (acquisition/ranking.csv); 55 cases (docs/ruleclass/TIERS.md); du 15 GB raw, 5 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

56 CTs on disk; 15 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/aortaseg60/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/aortaseg60/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/aortaseg60/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/aortaseg60` (CEPH, raw, 15.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/aortaseg60` (CEPH, converted/derived, 5.0 GB, listing 2026-09-24)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); L6 two-labeller 1, review 4; 5 registry rows (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 5 GB under `$RS/data/anomaly_harvest/aortaseg60` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/aortaseg60/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 55 CTs, tier 1 5, tier 2 50, alias candidates 6 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

55 of 60 usable, refusal reasons not copied locally (docs/ruleclass/TIERS.md; acquisition/ranking.csv)

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid aortaseg60` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_aortaseg60 ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection aortaseg60 --record 18147026 --include '^(Ven|Anev|Dissec|Old|Nat|Young)\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" aortaseg60` (slurm/acquisition_submit.sh); must verify 6 zips by md5 and 60 `_image.nii.gz` (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' aortaseg60` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `curvas` <a id="curvas"></a>

**CURVAS 2024.** Cards: B (CURVAS 2024), E (curvas). Structured entry: `sources.yaml` id `curvas`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`curvas` (acquisition/ranking.csv collection `zenodo:curvas`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`curvas`

**Name and citation**

*[B]*

CURVAS 2024 (90 CT, UKCHLL ids); release page zenodo.org/records/13767408 (acquisition/ranking.csv); Zenodo 13767408 published 2024-09 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

CURVAS, Zenodo 13767408 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

contrast CT, chest-abdomen-pelvis to whole body (class CAP/WB), UKCHLL ids (acquisition/ranking.csv); header sample: 25 of 90 images read by HTTP range (seed 20260924), 100.0 % at <= 3 mm, median craniocaudal extent 932 mm, P(both LS references) 0.895 / P(cage from T1) 0.822 per CT (acquisition/census_addendum.json)

*[E]*

CT, abdomen (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection curvas --record 13767408 --include '_set\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/image.nii.gz`, person `(UKCHLL[0-9]+)/image\.nii\.gz` (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection curvas --record 13767408 --include '_set\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430926 submitted 2026-09-24 (acquisition/jobs.txt); 07:16 EDT 2026-09-24 `training_set.zip` (Deflate64) failed to unpack after its md5 verified; repair chain 40436037-40436045 and dedupe 40436046 submitted (acquisition/jobs.txt); calls partial 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); called by 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/curvas` dated 2026-09-24, `anomaly_harvest/curvas` dated 2026-09-24 (listing)

*[E]*

`$RS/data/curvas` is dated 2026-09-24 in the listing; Slurm job fetch 40430926; repair chain 40436037 after a Deflate64 unpack failure (`jobs.txt`) (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

90 listed, 90 new; 29.4 GB by the record (acquisition/ranking.csv); 70 cases (docs/ruleclass/TIERS.md); du 28 GB raw, 5 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

71 CTs on disk; 28 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/curvas/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/curvas/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/curvas/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/curvas` (CEPH, raw, 28.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/curvas` (CEPH, converted/derived, 5.0 GB, listing 2026-09-24)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); L6 single-labeller 4, unassigned 1; 5 registry rows (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 5 GB under `$RS/data/anomaly_harvest/curvas` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/curvas/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 70 CTs, tier 1 5, tier 2 47, untiered 18, alias candidates 13 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

70 cases = 90 listed minus the 20 CTs of `training_set.zip`, consistent with the Deflate64 unit still failing, but no file states the repair's outcome (docs/ruleclass/TIERS.md; acquisition/jobs.txt; acquisition/ranking.csv); possible overlap with CURVAS-PDACVI (acquisition/ranking.csv)

*[E]*

`training_set.zip` (Deflate64) failed to unpack with the grid's p7zip (`jobs.txt`)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid curvas` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_curvas ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection curvas --record 13767408 --include '_set\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" curvas` (slurm/acquisition_submit.sh); must verify 3 zips by md5; the Deflate64 member needs Info-ZIP unzip or 7z on the node (tools/acquisition_fetch.py unpack; acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' curvas` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `quadra_hc` <a id="quadra_hc"></a>

**QUADRA_HC total-body FDG-PET/CT, healthy controls.** Cards: B (QUADRA_HC total-body FDG-PET/CT, healthy controls), E (quadra_hc). Structured entry: `sources.yaml` id `quadra_hc`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`quadra_hc` (acquisition/ranking.csv collection `zenodo:quadra_hc`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`quadra_hc`

**Name and citation**

*[B]*

QUADRA_HC total-body FDG-PET/CT, 48 healthy controls (test + retest); release page zenodo.org/records/16686025 (acquisition/ranking.csv); Zenodo 16686025 published 2025-08-02 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

QUADRA-HC (long-axial PET/CT), Zenodo 16686025 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

long-axial total-body PET/CT attenuation CT (class WB), test and retest per person (acquisition/ranking.csv; slurm/acquisition_submit.sh); header sample: 30 of 96 images read by HTTP range (seed 20260924), 100.0 % at <= 3 mm, median craniocaudal extent 1,062 mm, P(both LS references) 0.889 / P(cage from T1) 0.806 per CT (acquisition/census_addendum.json)

*[E]*

PET/CT, whole body (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection quadra_hc --record 16686025 --include '^QUADRA_HC\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/*_CT-AC.nii.gz`, person `(QUADRA_HC_[0-9]+)_(?:Test|Retest)_CT-AC`; one CT kept per person (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection quadra_hc --record 16686025 --include '^QUADRA_HC\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430935 submitted 2026-09-24 (acquisition/jobs.txt); gate done 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); called by 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/quadra_hc` dated 2026-09-24, `anomaly_harvest/quadra_hc` dated 2026-09-25 (listing)

*[E]*

`$RS/data/quadra_hc` is dated 2026-09-24 in the listing; Slurm job fetch 40430935 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

48 listed, 48 new; 20.18 GB by the record (acquisition/ranking.csv); 96 images for 48 people (acquisition/census_addendum.json); 48 cases (docs/ruleclass/TIERS.md); du 20 GB raw, 3 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

49 CTs on disk; 20 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/quadra_hc/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/quadra_hc/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/quadra_hc/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/quadra_hc` (CEPH, raw, 20.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/quadra_hc` (CEPH, converted/derived, 3.0 GB, listing 2026-09-25)

**Annotation status**

*[B]*

the release carries MOOSE vertebra and rib masks, a possible third labeller (acquisition/ranking.csv); pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); L6 two-labeller 1, T13 single 1, review 6, unassigned 1; 9 registry rows (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 3 GB under `$RS/data/anomaly_harvest/quadra_hc` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/quadra_hc/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 48 CTs, tier 1 9, tier 2 38, untiered 1 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

47 CT paths contain a space (`.../QUADRA_HC/Imaging Data/...`), so quote them (docs/ruleclass/TIERS.md section 3)

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid quadra_hc` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_quadra_hc ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection quadra_hc --record 16686025 --include '^QUADRA_HC\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" quadra_hc` (slurm/acquisition_submit.sh); must verify `QUADRA_HC.zip` by md5 and 96 `_CT-AC.nii.gz` (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' quadra_hc` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `deep_psma` <a id="deep_psma"></a>

**DEEP-PSMA (PSMA + FDG PET/CT, mCRPC).** Cards: B (DEEP-PSMA (PSMA + FDG PET/CT, mCRPC)), E (deep_psma). Structured entry: `sources.yaml` id `deep_psma`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`deep_psma` (acquisition/ranking.csv collection `zenodo:deep_psma`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`deep_psma`

**Name and citation**

*[B]*

DEEP-PSMA: PSMA + FDG PET/CT, 100 mCRPC patients; release page zenodo.org/records/15281784 (acquisition/ranking.csv); Zenodo 15281784 published 2025-11-21 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

Deep-PSMA, Zenodo 15281784 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

whole-body PET/CT attenuation CT (class WB), a PSMA and an FDG study per person (acquisition/ranking.csv; slurm/acquisition_submit.sh); header sample: 50 of 200 images read by HTTP range (seed 20260924), 48.0 % at <= 3 mm, median craniocaudal extent 1,095 mm, P(both LS references) 0.427 / P(cage from T1) 0.387 per CT (acquisition/census_addendum.json)

*[E]*

PET/CT, whole body (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY-NC 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY-NC 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection deep_psma --record 15281784 --include '^[0-9]{4}-[0-9]{4}\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/CT.nii.gz`, person `(train_[0-9]+)/(?:FDG|PSMA)/CT`; one CT kept per person (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection deep_psma --record 15281784 --include '^[0-9]{4}-[0-9]{4}\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430944 submitted 2026-09-24 (acquisition/jobs.txt); gate done 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); called by 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/deep_psma` dated 2026-09-24, `anomaly_harvest/deep_psma` dated 2026-09-24 (listing)

*[E]*

`$RS/data/deep_psma` is dated 2026-09-24 in the listing; Slurm job fetch 40430944 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

100 listed, 100 new; 24.07 GB by the record (acquisition/ranking.csv); 200 CTs for 100 people (acquisition/census_addendum.json); 53 cases (docs/ruleclass/TIERS.md); du 23 GB raw, 3 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

54 CTs on disk; 23 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/deep_psma/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/deep_psma/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/deep_psma/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/deep_psma` (CEPH, raw, 23.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/deep_psma` (CEPH, converted/derived, 3.0 GB, listing 2026-09-24)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); review 5, unassigned 1; 6 registry rows (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 3 GB under `$RS/data/anomaly_harvest/deep_psma` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/deep_psma/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 53 CTs, tier 1 6, tier 2 37, untiered 10 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

about half the attenuation CTs are thicker than 3 mm (refused), so 53 of 100 people remain (acquisition/ranking.csv; docs/ruleclass/TIERS.md); 1 tier-1 CT has no SPINEPS mask (docs/ruleclass/TIERS.md section 5)

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid deep_psma` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_deep_psma ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection deep_psma --record 15281784 --include '^[0-9]{4}-[0-9]{4}\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" deep_psma` (slurm/acquisition_submit.sh); must verify 5 zips by md5 and 200 `CT.nii.gz` (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' deep_psma` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `waw_tace` <a id="waw_tace"></a>

**WAW-TACE (HCC multiphase CT, Warsaw).** Cards: B (WAW-TACE (HCC multiphase CT, Warsaw)), E (waw_tace). Structured entry: `sources.yaml` id `waw_tace`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`waw_tace` (acquisition/ranking.csv collection `zenodo:waw_tace`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`waw_tace`

**Name and citation**

*[B]*

WAW-TACE: HCC multiphase abdominal CT, 233 patients (Warsaw); release page zenodo.org/records/12741586 (acquisition/ranking.csv); Zenodo 12741586 published 2024-07-15 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

WAW-TACE, Zenodo 12741586 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

multiphase abdominal CT of hepatocellular carcinoma (class ABD) (acquisition/ranking.csv); header sample: 100 of 854 images read by HTTP range (seed 20260924), 96.0 % at <= 3 mm, median craniocaudal extent 285 mm, P(both LS references) 0.271 / P(cage from T1) 0.24 per CT (acquisition/census_addendum.json)

*[E]*

CT, abdomen (liver, TACE) (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection waw_tace --record 12741586 --include '^ct_scans_[1-4]_4_wawtace.*\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert glob `**/*_scan.nii.gz`, person `/([0-9]+)_[0-9]+_scan`; widest phase kept per person (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection waw_tace --record 12741586 --include '^ct_scans_[1-4]_4_wawtace.*\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430953 submitted 2026-09-24 (acquisition/jobs.txt); 2/4 zips at 10:35 EDT 2026-09-24 (acquisition/jobs.txt); gate done, no SPINEPS yet on 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); SPINEPS running 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/waw_tace` dated 2026-09-24, `anomaly_harvest/waw_tace` dated 2026-09-25 (listing)

*[E]*

`$RS/data/waw_tace` is dated 2026-09-24 in the listing; Slurm job fetch 40430953 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

233 listed, 233 new; 47.15 GB by the record (acquisition/ranking.csv); 854 phases for 233 people (acquisition/census_addendum.json; acquisition/ranking.csv); 228 cases (docs/ruleclass/TIERS.md); du 44 GB raw, 5 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

229 CTs on disk; 44 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/waw_tace/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/waw_tace/raw/<record>/...`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/waw_tace/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/waw_tace` (CEPH, raw, 44.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/waw_tace` (CEPH, converted/derived, 5.0 GB, listing 2026-09-25)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 5 GB under `$RS/data/anomaly_harvest/waw_tace` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/waw_tace/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 228 CTs, tier 1 48, tier 2 164, untiered 16, alias candidates 24 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

the per-CT P came from a phase-mixed sample and is a floor (acquisition/ranking.csv); it is the 'Medical University of Warsaw' part of PanTSMini (293 volumes) (acquisition/ranking.csv; acquisition/census_addendum.json); screen state after 2026-09-25 not recorded locally

*[E]*

none recorded

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid waw_tace` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_waw_tace ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection waw_tace --record 12741586 --include '^ct_scans_[1-4]_4_wawtace.*\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" waw_tace` (slurm/acquisition_submit.sh); must verify 4 CT zips by md5 and 854 `_scan.nii.gz` (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' waw_tace` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### `pengwin2026` <a id="pengwin2026"></a>

**PENGWIN 2026 peripelvic fracture CT (training).** Cards: B (PENGWIN 2026 peripelvic fracture CT (training)), E (pengwin2026). Structured entry: `sources.yaml` id `pengwin2026`; kind upstream_release; status on_disk; re-acquisition submit (zenodo).

**Source id**

*[B]*

`pengwin2026` (acquisition/ranking.csv collection `zenodo:pengwin2026`; slurm/acquisition_submit.sh `tier1_late`)

*[E]*

`pengwin2026`

**Name and citation**

*[B]*

PENGWIN 2026 peripelvic fracture CT (340 training cases); release page zenodo.org/records/19732767 (acquisition/ranking.csv); Zenodo 19732767 published 2026-04-24 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

*[E]*

PENGWIN 2026 (pelvic fracture CT), Zenodo 19732767 (route and record from `nnunet:slurm/acquisition_submit.sh`; collection listed in `CENSUS_TABLE_2026-09-25.md` 1 or `ranking.csv`)

**Modality**

*[B]*

pelvic fracture CT, MHA (class PELVIS; P(cage) set to 0 by anatomy although the extent bin gives 0.182) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b); header sample: 40 of 340 images read by HTTP range (seed 20260924), 100.0 % at <= 3 mm, median craniocaudal extent 252 mm, P(both LS references) 0.078 / P(cage from T1) 0.182 per CT (acquisition/census_addendum.json)

*[E]*

CT, pelvis (`CENSUS_TABLE_2026-09-25.md` 1)

**Position/view**

*[B]*

not recorded: the screen extracts no patient position and the release metadata was not read for it (tools/acquisition_screen.py); a CT has no projection view

*[E]*

not recorded

**Licence and access**

*[B]*

open, CC BY-NC-SA 4.0, derived labels allowed (yes) (acquisition/ranking.csv)

*[E]*

CC BY-NC-SA 4.0, open (`ranking.csv`)

**How it was acquired**

*[B]*

`acquisition_fetch.py zenodo --collection pengwin2026 --record 19732767 --include '^PENGWIN26_task1_2_train_part[1-4]\.zip$'`, md5 per archive, nice 200, one CT per person at `cases` (slurm/acquisition_submit.sh; tools/acquisition_fetch.py); convert MHA glob `**/image.mha` -> NIfTI, person `train_part[0-9]/([0-9]+)/image\.mha` (slurm/acquisition_submit.sh)

*[E]*

`python tools/acquisition_fetch.py zenodo --collection pengwin2026 --record 19732767 --include '^PENGWIN26_task1_2_train_part[1-4]\.zip$'`, as one chain of `nnunet:slurm/acquisition_submit.sh`. Verified by Zenodo md5 (`nnunet:tools/acquisition_fetch.py` docstring)

**When**

*[B]*

fetch 40430962 submitted 2026-09-24 (acquisition/jobs.txt); TotalSegmentator partial on 2026-09-24 (SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); called by 2026-09-25 (docs/CENSUS_TABLE_2026-09-25.md); CEPH `data/pengwin2026` dated 2026-09-24, `anomaly_harvest/pengwin2026` dated 2026-09-25 (listing)

*[E]*

`$RS/data/pengwin2026` is dated 2026-09-24 in the listing; Slurm job fetch 40430962 (`jobs.txt`). Fetch code first committed 2026-09-24 (git log `nnunet:tools/acquisition_fetch.py`)

**What it contains**

*[B]*

340 listed, 340 new; 19.57 GB by the record (acquisition/ranking.csv); 340 cases, of which 32 are the same voxels as CTPelvic1K clinical CTs and were folded, leaving 308 (docs/ruleclass/TIERS.md; SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md); du 78 GB raw (MHA plus NIfTI), 5 GB screen output (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

341 CTs on disk; 78 GB raw (`CENSUS_TABLE_2026-09-25.md` 1). Per-file state is in `$RS/data/pengwin2026/fetch/verified.jsonl` (docstring)

**Where it is now**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/pengwin2026/raw/<record>/...`, `nifti/pengwin26_<n>_ct.nii.gz`, `fetch/`; screen `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/pengwin2026/` (tools/acquisition_screen.py; listing); nothing on HOME (listing)

*[E]*

`$RS/data/pengwin2026` (CEPH, raw, 78.0 GB, listing 2026-09-24); `$RS/data/anomaly_harvest/pengwin2026` (CEPH, converted/derived, 5.0 GB, listing 2026-09-25)

**Annotation status**

*[B]*

pseudo-labels only (labeller B TotalSegmentator geometry, labeller A SPINEPS+VERIDAH ctd names, a combined call per CT; row fields as in the shared section); no radiologist read (tools/acquisition_screen.py ROW_COLS; acquisition/ACQUISITION_PLAN.md sections 6, 9); L6 single-labeller 1; 1 registry row (docs/CENSUS_TABLE_2026-09-25.md)

*[E]*

project pseudo-labels only: TotalSegmentator and SPINEPS+VERIDAH masks plus a two-labeller L6/T13 call, 5 GB under `$RS/data/anomaly_harvest/pengwin2026` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations are not used and not recorded here

**Derived products**

*[B]*

CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/pengwin2026/` holds the screen: `convert/`, `thumbs/` (16^3 thumbnails), `cases.csv` (case, ct, source, patient_key, extent_mm, dz_mm, pixel_sha1), `convert_summary.json`, `seg/<case>/` (TotalSegmentator), `labeller_b/`, `gate.csv`, `spineps/`, `calls/`, `review/`, `rows.csv`, `registry_rows.csv`, `SUMMARY.md` (tools/acquisition_screen.py; listing); tiers: 308 CTs, tier 1 1, tier 2 10, untiered 297, alias candidates 26 (docs/ruleclass/TIERS.md)

*[E]*

none found in the disk map; the transitional registry rows (`nnunet:SchwingNet/results/transitional_registry/`)

**Known defects and gaps**

*[B]*

pelvic fields: about 11 of 340 pass the gate (docs/CENSUS_TABLE_2026-09-25.md (12, see the off-by-one note)); 32 CTs duplicate CTPelvic1K clinical (pooled from several institutions) (docs/ruleclass/TIERS.md; acquisition/ranking.csv)

*[E]*

the FOV gate passes 12 of 341 where the pelvis prior gives 40 (`CENSUS_TABLE_2026-09-25.md` caveats)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid pengwin2026` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[B]*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_pengwin2026 ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh zenodo --collection pengwin2026 --record 19732767 --include '^PENGWIN26_task1_2_train_part[1-4]\.zip$'` (verifies each archive against the record's md5 before unpacking, then CRC-checks every member; a rerun skips verified units) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py; slurm/acquisition_fetch.sh); chain: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late "" pengwin2026` (slurm/acquisition_submit.sh); must verify 4 training zips by md5 and 340 `image.mha` (acquisition/census_addendum.json)

*[E]*

`bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1_late '' pengwin2026` (block `tier1_late`; the third argument picks one chain), which resumes and skips finished units (`nnunet:slurm/acquisition_submit.sh` header), or the single command above inside an sbatch job. Verify that `FETCH_STATUS.json` shows every unit in `verified.jsonl`

---

### Group B5. Tier 2 (planned; RibFrac already on disk through another stream)

### `idc_spine_mets_ct_seg` <a id="idc_spine_mets_ct_seg"></a>

**IDC `spine_mets_ct_seg` (tier 2).** Cards: B (IDC `spine_mets_ct_seg` (tier 2)). Structured entry: `sources.yaml` id `idc_spine_mets_ct_seg`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_spine_mets_ct_seg` (acquisition/ranking.csv collection `idc:spine_mets_ct_seg`)

**Name and citation**

IDC v24 collection_id `spine_mets_ct_seg`; TCIA DOI 10.7937/kh36-ds04 (acquisition/ranking.csv)

**Modality**

CT, coverage SPINE:51;ABD:2;PELVIS:1 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

55 listed, 54 qualifying; 17.2 GB to fetch, 18.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: not a regularly spaced 3-D volume:1 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `idc_cptac_luad` <a id="idc_cptac_luad"></a>

**IDC `cptac_luad` (tier 2).** Cards: B (IDC `cptac_luad` (tier 2)). Structured entry: `sources.yaml` id `idc_cptac_luad`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_cptac_luad` (acquisition/ranking.csv collection `idc:cptac_luad`)

**Name and citation**

IDC v24 collection_id `cptac_luad`; TCIA DOI 10.7937/k9/tcia.2018.pat12tbs (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:22;OTHER:4;WB:4;ABD:2 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

37 listed, 32 qualifying; 7.0 GB to fetch, 37.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: slice > 3.0 mm:78;non-axial reformat:72;localizer image type:66;< 60 slices:37 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `idc_midrc_ricord_1b` <a id="idc_midrc_ricord_1b"></a>

**IDC `midrc_ricord_1b` (tier 2).** Cards: B (IDC `midrc_ricord_1b` (tier 2)). Structured entry: `sources.yaml` id `idc_midrc_ricord_1b`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_midrc_ricord_1b` (acquisition/ranking.csv collection `idc:midrc_ricord_1b`)

**Name and citation**

IDC v24 collection_id `midrc_ricord_1b`; TCIA DOI 10.7937/31v8-4a40 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:61;OTHER:29;CAP:1 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC 4.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

117 listed, 91 qualifying; 7.0 GB to fetch, 8.5 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: non-axial reformat:25;not a regularly spaced 3-D volume:1;< 60 slices:1 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `idc_cptac_lscc` <a id="idc_cptac_lscc"></a>

**IDC `cptac_lscc` (tier 2).** Cards: B (IDC `cptac_lscc` (tier 2)). Structured entry: `sources.yaml` id `idc_cptac_lscc`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_cptac_lscc` (acquisition/ranking.csv collection `idc:cptac_lscc`)

**Name and citation**

IDC v24 collection_id `cptac_lscc`; TCIA DOI 10.7937/k9/tcia.2018.6emub5l2 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:20;OTHER:6;WB:4;CAP:2 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

36 listed, 32 qualifying; 8.3 GB to fetch, 28.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: slice > 3.0 mm:46;non-axial reformat:29;localizer image type:16;not a regularly spaced 3-D volume:12 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `idc_prostate_anatomical_edge_cases` <a id="idc_prostate_anatomical_edge_cases"></a>

**IDC `prostate_anatomical_edge_cases` (tier 2).** Cards: B (IDC `prostate_anatomical_edge_cases` (tier 2)). Structured entry: `sources.yaml` id `idc_prostate_anatomical_edge_cases`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_prostate_anatomical_edge_cases` (acquisition/ranking.csv collection `idc:prostate_anatomical_edge_cases`)

**Name and citation**

IDC v24 collection_id `prostate_anatomical_edge_cases`; TCIA DOI 10.7937/qstf-st65 (acquisition/ranking.csv)

**Modality**

CT, coverage PELVIS:131 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

131 listed, 131 qualifying; 16.6 GB to fetch, 16.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: none (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `idc_nsclc_radiogenomics` <a id="idc_nsclc_radiogenomics"></a>

**IDC `nsclc_radiogenomics` (tier 2).** Cards: B (IDC `nsclc_radiogenomics` (tier 2)). Structured entry: `sources.yaml` id `idc_nsclc_radiogenomics`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_nsclc_radiogenomics` (acquisition/ranking.csv collection `idc:nsclc_radiogenomics`)

**Name and citation**

IDC v24 collection_id `nsclc_radiogenomics`; TCIA DOI 10.7937/k9/tcia.2017.7hs46erv (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:168;WB:10;CAP:8;ABD:1;CA:1 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

211 listed, 188 qualifying; 28.0 GB to fetch, 88.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: slice > 3.0 mm:235;non-axial reformat:123;localizer image type:100;reformat/MIP series:37 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `zenodo_medpelvis3d` <a id="zenodo_medpelvis3d"></a>

**MedPelvis3D pelvic CT (99, PLA General Hospital).** Cards: B (MedPelvis3D pelvic CT (99, PLA General Hospital)). Structured entry: `sources.yaml` id `zenodo_medpelvis3d`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_medpelvis3d` (acquisition/ranking.csv collection `zenodo:medpelvis3d`)

**Name and citation**

MedPelvis3D pelvic CT (99, PLA General Hospital); Zenodo 21757686 published 2026-08-02 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage PELVIS:99; pelvic fields (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; no route or convert arguments written in `acquisition_submit.sh` (slurm/acquisition_submit.sh)

**When**

found 2026-09-24 sweep; tier 2 by the stopping rule (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**What it contains**

99 listed, 99 new, 15.1 GB (acquisition/ranking.csv); record total 31.4 GB in 100 files (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known (acquisition/ranking.csv)

**Re-acquisition recipe**

`acquisition_fetch.py zenodo --collection medpelvis3d --record 21757686 --include '<pattern to be chosen from the record listing>'` (md5-verified), then a `chain` entry with convert arguments, which does not exist yet (tools/acquisition_fetch.py; slurm/acquisition_submit.sh)

---

### `idc_nsclc_radiomics` <a id="idc_nsclc_radiomics"></a>

**IDC `nsclc_radiomics` (tier 2).** Cards: B (IDC `nsclc_radiomics` (tier 2)). Structured entry: `sources.yaml` id `idc_nsclc_radiomics`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_nsclc_radiomics` (acquisition/ranking.csv collection `idc:nsclc_radiomics`)

**Name and citation**

IDC v24 collection_id `nsclc_radiomics`; TCIA DOI 10.7937/k9/tcia.2015.pf0m9rei (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:415 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC 3.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

422 listed, 415 qualifying; 25.8 GB to fetch, 26.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: not a regularly spaced 3-D volume:6;non-axial reformat:1 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `zenodo_lumvbcanseg` <a id="zenodo_lumvbcanseg"></a>

**LumVBCanSeg lumbar CT (185, ShengJing Hospital).** Cards: B (LumVBCanSeg lumbar CT (185, ShengJing Hospital)). Structured entry: `sources.yaml` id `zenodo_lumvbcanseg`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_lumvbcanseg` (acquisition/ranking.csv collection `zenodo:lumvbcanseg`)

**Name and citation**

LumVBCanSeg lumbar CT (185, ShengJing Hospital); Zenodo 8181250 published 2023-07-25 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage SPINE:185; lumbar fields resampled to 1 mm: P(cage) = 0 by anatomy (acquisition/ranking.csv); header sample: 30 read, median extent 268 mm, P(both) 0.04 (acquisition/census_addendum.json)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; no route or convert arguments written in `acquisition_submit.sh` (slurm/acquisition_submit.sh)

**When**

found 2026-09-24 sweep; tier 2 by the stopping rule (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**What it contains**

185 listed, 185 new, 10.08 GB (acquisition/ranking.csv); record total 10.1 GB in 1 files (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known (acquisition/ranking.csv)

**Re-acquisition recipe**

`acquisition_fetch.py zenodo --collection lumvbcanseg --record 8181250 --include '<pattern to be chosen from the record listing>'` (md5-verified), then a `chain` entry with convert arguments, which does not exist yet (tools/acquisition_fetch.py; slurm/acquisition_submit.sh)

---

### `idc_lidc_idri` <a id="idc_lidc_idri"></a>

**IDC `lidc_idri` (tier 2).** Cards: B (IDC `lidc_idri` (tier 2)). Structured entry: `sources.yaml` id `idc_lidc_idri`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_lidc_idri` (acquisition/ranking.csv collection `idc:lidc_idri`)

**Name and citation**

IDC v24 collection_id `lidc_idri`; TCIA DOI 10.7937/k9/tcia.2015.lo9ql9sx (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:953;CAP:38;CA:4;ABD:1;AP:1 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

1,010 listed, 997 qualifying; 123.3 GB to fetch, 125.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: not a regularly spaced 3-D volume:9;slice > 3.0 mm:4 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `idc_spinal_multiple_myeloma_seg` <a id="idc_spinal_multiple_myeloma_seg"></a>

**IDC `spinal_multiple_myeloma_seg` (tier 2).** Cards: B (IDC `spinal_multiple_myeloma_seg` (tier 2)). Structured entry: `sources.yaml` id `idc_spinal_multiple_myeloma_seg`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_spinal_multiple_myeloma_seg` (acquisition/ranking.csv collection `idc:spinal_multiple_myeloma_seg`)

**Name and citation**

IDC v24 collection_id `spinal_multiple_myeloma_seg`; TCIA DOI 10.7937/k4qv-hh78 (acquisition/ranking.csv)

**Modality**

CT, coverage SPINE:67 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

67 listed, 67 qualifying; 33.8 GB to fetch, 290.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: non-HU reconstruction (spectral map / suppression):288 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `zenodo_vsd_fullbody` <a id="zenodo_vsd_fullbody"></a>

**VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich.** Cards: B (VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich). Structured entry: `sources.yaml` id `zenodo_vsd_fullbody`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_vsd_fullbody` (acquisition/ranking.csv collection `zenodo:vsd_fullbody`)

**Name and citation**

VSDFullBody: post-mortem whole-body CT, forensic institutes Bern and Zurich; Zenodo 8270365 published 2013-11-12 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage WB:100; coverage and slice thickness unmeasured (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC-SA per the record's text (the record's licence field is empty), derived labels yes (per the relayed licence) (acquisition/ranking.csv)

**How it was acquired**

not fetched; no route or convert arguments written in `acquisition_submit.sh` (slurm/acquisition_submit.sh)

**When**

found 2026-09-24 sweep; tier 2 by the stopping rule (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**What it contains**

109 listed, 100 new, 116.3 GB (acquisition/ranking.csv); record total 116.3 GB in 109 files (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

the mirror notes duplicate CT datasets: n_new 100 of 109 files (acquisition/ranking.csv)

**Re-acquisition recipe**

`acquisition_fetch.py zenodo --collection vsd_fullbody --record 8270365 --include '<pattern to be chosen from the record listing>'` (md5-verified), then a `chain` entry with convert arguments, which does not exist yet (tools/acquisition_fetch.py; slurm/acquisition_submit.sh)

---

### `idc_ldct_and_projection_data` <a id="idc_ldct_and_projection_data"></a>

**IDC `ldct_and_projection_data` (tier 2).** Cards: B (IDC `ldct_and_projection_data` (tier 2)). Structured entry: `sources.yaml` id `idc_ldct_and_projection_data`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_ldct_and_projection_data` (acquisition/ranking.csv collection `idc:ldct_and_projection_data`)

**Name and citation**

IDC v24 collection_id `ldct_and_projection_data`; TCIA DOI 10.7937/9npb-2637 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:99 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes; public IDC buckets (acquisition/ranking.csv)

**How it was acquired**

not fetched; in the unsubmitted `tier2` target (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`) (slurm/acquisition_submit.sh)

**When**

ranked 2026-09-23; tier 2 waits for tier 1's measured rates and fewer than 5,000 unscreened CTs (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

199 listed, 99 qualifying; 16.5 GB to fetch, 37.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (no `data/idc_tier2`) (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: slice > 3.0 mm:150 (acquisition/ranking.csv); `idc_tier2.csv` is not in the repository (acquisition/manifests/)

**Re-acquisition recipe**

regenerate `idc_tier2.csv` with tools/acquisition_census.py (needs `aa3_meta.csv` and `fdg_ct_series.json`, not on local disk), then `acquisition_submit.sh tier2`; or one collection: filter that manifest with awk on column 1 as in the tier-1 cards (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `idc_nlst` <a id="idc_nlst"></a>

**NLST, full (tier 2; 500-person pilot fetched).** Cards: B (NLST, full (tier 2; 500-person pilot fetched)). Structured entry: `sources.yaml` id `idc_nlst`; kind upstream_release; status planned; re-acquisition manual (idc).

**Source id**

`idc_nlst` (acquisition/ranking.csv collection `idc:nlst`)

**Name and citation**

National Lung Screening Trial in IDC v24, TCIA DOI 10.7937/tcia.hmq8-j677 (acquisition/ranking.csv)

**Modality**

low-dose screening chest CT: CHEST_SCREEN 24,491, OTHER 222 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0 (acquisition/ranking.csv)

**How it was acquired**

not fetched: written into `acquisition_submit.sh tier2` (`idc --collection idc_tier2 --manifest $M/idc_tier2.csv --batch 200`, the pilot's 500 series excluded) and deliberately not submitted (slurm/acquisition_submit.sh; tools/acquisition_census.py)

**When**

ranked 2026-09-23 (acquisition/ACQUISITION_PLAN.md); held by stopping rule 4 on 2026-09-24 (acquisition/ACQUISITION_PLAN.md sections 3, 11)

**What it contains**

26,254 patients listed, 24,713 qualifying; 2,305.3 GB to fetch; 10,876 GB all CT (acquisition/ranking.csv)

**Where it is now**

only the pilot is on disk (`data/nlst_pilot`); no `data/idc_tier2` directory (listing)

**Annotation status**

none (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

refusals: localizer image type:65174;slice > 3.0 mm:21188;< 60 slices:5209;not a regularly spaced 3-D volume:3652 (acquisition/ranking.csv); T13 is its only yield, expected about 1.5 % single-labeller calls that all need adjudication (acquisition/ACQUISITION_PLAN.md section 11); refused as it stands by the stopping rule (2.3 TB for about 110 T13 people) (docs/CENSUS_TABLE_2026-09-25.md section 2)

**Re-acquisition recipe**

regenerate `manifests/idc_tier2.csv` (not in the repository) with `tools/acquisition_census.py --calibration fov_calibration.json --aa3-meta aa3_meta.csv --nbia-fdg fdg_ct_series.json --out ...` (the last two inputs are not on local disk), then `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier2` (tools/acquisition_census.py; slurm/acquisition_submit.sh)

---

### `aws_stoic2021` <a id="aws_stoic2021"></a>

**STOIC2021 training (AWS Open Data).** Cards: B (STOIC2021 training (AWS Open Data)). Structured entry: `sources.yaml` id `aws_stoic2021`; kind upstream_release; status planned; re-acquisition submit (s3).

**Source id**

`aws_stoic2021` (acquisition/ranking.csv collection `aws:stoic2021`)

**Name and citation**

STOIC2021 training set, `s3://stoic2021-training` (LICENCE.txt read 2026-09-23) (acquisition/ranking.csv)

**Modality**

COVID chest CT, CHEST_SCREEN (T13 by rib count only), MHA (acquisition/ranking.csv; slurm/acquisition_submit.sh)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC 4.0, no sign-in (acquisition/ranking.csv)

**How it was acquired**

not fetched; route written: `acquisition_fetch.py s3 --collection stoic2021 --bucket s3://stoic2021-training/data/mha --include '\.mha$'` (s5cmd --no-sign-request sync; verified by object size against the listing) (slurm/acquisition_submit.sh; tools/acquisition_fetch.py)

**When**

ranked 2026-09-23 (acquisition/ACQUISITION_PLAN.md); not submitted (stopping rule 4) (acquisition/ACQUISITION_PLAN.md section 3)

**What it contains**

2,000 CT, 240 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

inside CADS (gated) and re-packed as AUC23 'Lung CT COVID-19' (acquisition/ranking.csv)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): creates $D/logs before sbatch (Slurm opens the log before the script runs); manifests read from the repository. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid aws_stoic2021` prints them. Where the text below differs, `sources.json` is the runnable form.*

`D=/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition; sbatch -D $D --job-name=acq_fetch_stoic2021 ~/spinesurg-ct-nnunet/slurm/acquisition_fetch.sh s3 --collection stoic2021 --bucket s3://stoic2021-training/data/mha --include '\.mha$'`; must verify 2,000 MHA by size (slurm/acquisition_submit.sh; tools/acquisition_fetch.py)

---

### `zenodo_unitochest` <a id="zenodo_unitochest"></a>

**UniToChest chest CT (623 patients; distributed as slices).** Cards: B (UniToChest chest CT (623 patients; distributed as slices)). Structured entry: `sources.yaml` id `zenodo_unitochest`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_unitochest` (acquisition/ranking.csv collection `zenodo:unitochest`)

**Name and citation**

UniToChest chest CT (623 patients; distributed as slices); Zenodo 5797912 published 2021-12-22 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage CHEST:623; T13 by rib count only; slice format unverified (the record describes 306,440 slices) (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; no route or convert arguments written in `acquisition_submit.sh` (slurm/acquisition_submit.sh)

**When**

found 2026-09-24 sweep; tier 2 by the stopping rule (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**What it contains**

623 listed, 623 new, 84.07 GB (acquisition/ranking.csv); record total 84.1 GB in 2 files (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known (acquisition/ranking.csv)

**Re-acquisition recipe**

`acquisition_fetch.py zenodo --collection unitochest --record 5797912 --include '<pattern to be chosen from the record listing>'` (md5-verified), then a `chain` entry with convert arguments, which does not exist yet (tools/acquisition_fetch.py; slurm/acquisition_submit.sh)

---

### Group B6. Deferred (no route yet) or unresolved overlap

### `scidb_enhance_pet_1_6k` <a id="scidb_enhance_pet_1_6k"></a>

**ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI).** Cards: B (ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI)). Structured entry: `sources.yaml` id `scidb_enhance_pet_1_6k`; kind upstream_release; status planned; re-acquisition manual (Science Data Bank).

**Source id**

`scidb_enhance_pet_1_6k` (acquisition/ranking.csv collection `scidb:enhance_pet_1.6k`)

**Name and citation**

ENHANCE.PET 1.6k: whole-/total-body FDG-PET/CT, 1,683 studies (NIfTI); doi.org/10.57760/sciencedb.34150 (DataCite, read 2026-09-24; found by the review's DataCite search) (acquisition/ranking.csv)

**Modality**

CT, coverage WB:1683 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched: deferred: the Science Data Bank download route is not scripted and whether it needs a login is unconfirmed; tier-1-grade if it is open (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

1,683 listed; 286.3 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

multi-centre (Vienna, UC Davis, Careggi, Leipzig, Tuebingen): Tuebingen may be autoPET (tier 1) and Vienna's healthy controls may be QUADRA_HC (late tier 1); the landing dedupe would find both; slice thickness per study is in its CT-details.xlsx (not read); E assumes every CT <= 3 mm, so it is a ceiling (acquisition/ranking.csv)

**Re-acquisition recipe**

manual first: confirm whether Science Data Bank (doi 10.57760/sciencedb.34150) needs a login, read `CT-details.xlsx` for slice thickness; no fetch route exists in tools/acquisition_fetch.py for Science Data Bank (acquisition/ACQUISITION_PLAN.md section 4b; tools/acquisition_fetch.py)

---

### `zenodo_tmtv_benchmark` <a id="zenodo_tmtv_benchmark"></a>

**International TMTV Benchmark, lymphoma FDG PET/CT (60).** Cards: B (International TMTV Benchmark, lymphoma FDG PET/CT (60)). Structured entry: `sources.yaml` id `zenodo_tmtv_benchmark`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_tmtv_benchmark` (acquisition/ranking.csv collection `zenodo:tmtv_benchmark`)

**Name and citation**

International TMTV Benchmark, lymphoma FDG PET/CT (60); zenodo.org/records/13255214 (acquisition/ranking.csv); Zenodo 13255214 published 2024-08-07 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage WB:60 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched: deferred: needs a zipped-DICOM convert route (the NIfTI copies are on the PET grid) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

60 listed; 6.85 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known; the NIfTI CTs are on the PET grid (> 3 mm); the DICOM needs a zipped-DICOM convert route not written yet (acquisition/ranking.csv)

**Re-acquisition recipe**

`acquisition_fetch.py zenodo --collection tmtv_benchmark --record 13255214 --include '\.zip$'` works for the download, but a zipped-DICOM convert route must be written first (the NIfTI copies are on the PET grid) (acquisition/ACQUISITION_PLAN.md section 4b; tools/acquisition_fetch.py)

---

### `zenodo_lumos` <a id="zenodo_lumos"></a>

**LUMOS lumbar osteoporosis dataset: 280 lumbar CT (+1,620 radiographs).** Cards: B (LUMOS lumbar osteoporosis dataset: 280 lumbar CT (+1,620 radiographs)). Structured entry: `sources.yaml` id `zenodo_lumos`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_lumos` (acquisition/ranking.csv collection `zenodo:lumos`)

**Name and citation**

LUMOS lumbar osteoporosis dataset: 280 lumbar CT (+1,620 radiographs); zenodo.org/records/18173663 (found by the review's search) (acquisition/ranking.csv)

**Modality**

CT, coverage SPINE:280 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched: deferred: needs a zipped-DICOM convert route (as TMTV) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

280 listed; 34.0 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known; CT share of the 46.4 GB record estimated at 34 GB; lumbar fields (acquisition/ranking.csv)

**Re-acquisition recipe**

`acquisition_fetch.py zenodo --collection lumos --record 18173663 --include '<CT zips>'`, then a zipped-DICOM convert route (not written) (acquisition/ACQUISITION_PLAN.md section 4b; tools/acquisition_fetch.py)

---

### `zenodo_ts_task_liver_lesions` <a id="zenodo_ts_task_liver_lesions"></a>

**TotalSegmentator task data 'liver_lesions' (842 CT).** Cards: B (TotalSegmentator task data 'liver_lesions' (842 CT)). Structured entry: `sources.yaml` id `zenodo_ts_task_liver_lesions`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_ts_task_liver_lesions` (acquisition/ranking.csv collection `zenodo:ts_task_liver_lesions`)

**Name and citation**

TotalSegmentator task data 'liver_lesions' (842 CT); zenodo.org/records/20272572 (acquisition/ranking.csv); Zenodo 20272572 published 2026-05-18 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage ABD:842 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched: unresolved overlap with TotalSegmentator v2/v3: not fetched until a pixel match says the people are new (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

842 listed; 38.87 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

same institution as TotalSegmentator v2/v3 (on disk); no subject map (acquisition/ranking.csv)

**Re-acquisition recipe**

manual first: ask the TotalSegmentator authors whether these subjects overlap the public v2/v3 release (Greg to send); then `acquisition_fetch.py zenodo --collection ts_task_liver_lesions --record 20272572 --include '.'` (acquisition/ACQUISITION_PLAN.md section 4b; tools/acquisition_fetch.py)

---

### `zenodo_ts_task_pleural_effusion` <a id="zenodo_ts_task_pleural_effusion"></a>

**TotalSegmentator task data 'pleural_pericard_effusion' (600 CT).** Cards: B (TotalSegmentator task data 'pleural_pericard_effusion' (600 CT)). Structured entry: `sources.yaml` id `zenodo_ts_task_pleural_effusion`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_ts_task_pleural_effusion` (acquisition/ranking.csv collection `zenodo:ts_task_pleural_effusion`)

**Name and citation**

TotalSegmentator task data 'pleural_pericard_effusion' (600 CT); zenodo.org/records/20272295 (acquisition/ranking.csv); Zenodo 20272295 published 2026-05-18 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage CHEST:600 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched: unresolved overlap with TotalSegmentator v2/v3: not fetched until a pixel match says the people are new (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

600 listed; 8.99 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

same institution as TotalSegmentator v2/v3 (on disk); no subject map (acquisition/ranking.csv)

**Re-acquisition recipe**

as liver_lesions, record 20272295 (acquisition/ACQUISITION_PLAN.md section 4b; tools/acquisition_fetch.py)

---

### `zenodo_ts_task_hip_implant` <a id="zenodo_ts_task_hip_implant"></a>

**TotalSegmentator task data 'hip_implant' (71 CT).** Cards: B (TotalSegmentator task data 'hip_implant' (71 CT)). Structured entry: `sources.yaml` id `zenodo_ts_task_hip_implant`; kind upstream_release; status planned; re-acquisition manual (zenodo).

**Source id**

`zenodo_ts_task_hip_implant` (acquisition/ranking.csv collection `zenodo:ts_task_hip_implant`)

**Name and citation**

TotalSegmentator task data 'hip_implant' (71 CT); zenodo.org/records/20272031 (acquisition/ranking.csv); Zenodo 20272031 published 2026-05-18 (acquisition/sweep/zenodo_ge5GB_ct.tsv)

**Modality**

CT, coverage PELVIS:71 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched: unresolved overlap with TotalSegmentator v2/v3: not fetched until a pixel match says the people are new (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

71 listed; 9.03 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

same institution as TotalSegmentator v2/v3 (on disk); no subject map (acquisition/ranking.csv)

**Re-acquisition recipe**

as liver_lesions, record 20272031 (acquisition/ACQUISITION_PLAN.md section 4b; tools/acquisition_fetch.py)

---

### `hf_abdomenatlas2_0_mini` <a id="hf_abdomenatlas2_0_mini"></a>

**AbdomenAtlas 2.0 Mini (10,135 CT).** Cards: B (AbdomenAtlas 2.0 Mini (10,135 CT)). Structured entry: `sources.yaml` id `hf_abdomenatlas2_0_mini`; kind upstream_release; status planned; re-acquisition manual (hf).

**Source id**

`hf_abdomenatlas2_0_mini` (acquisition/ranking.csv collection `hf:AbdomenAtlas/AbdomenAtlas2.0Mini`)

**Name and citation**

AbdomenAtlas 2.0 Mini (10,135 CT); HF tree 2026-09-24: 21 tars, 620 GB (acquisition/ranking.csv)

**Modality**

CT, coverage ABD:0 (acquisition/ranking.csv)

**Position/view**

not recorded; not fetched (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC-SA 4.0, derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched: unresolved overlap with AbdomenAtlas 3.0 Mini: not fetched until an id map exists (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 4b)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

10,135 listed; 620.4 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no card, no metadata; the AbdomenAtlas line aggregates public sets and 3.0 Mini (= 1.1, 9,262) is already fetched; the other ~873 are unidentified (acquisition/ranking.csv)

**Re-acquisition recipe**

manual first: obtain an id map against AbdomenAtlas 3.0 Mini (no card, no metadata); then `acquisition_fetch.py hf --collection abdomenatlas2_mini --repo AbdomenAtlas/AbdomenAtlas2.0Mini --include '<tars>'` (acquisition/ACQUISITION_PLAN.md section 4b; tools/acquisition_fetch.py)

---

### Group B7. Gated (a form or agreement stands in front of the data; none signed)

### `stanford_aimi_merlin` <a id="stanford_aimi_merlin"></a>

**Merlin abdominal CT (25,494 CT / 18,317 patients).** Cards: B (Merlin abdominal CT (25,494 CT / 18,317 patients)). Structured entry: `sources.yaml` id `stanford_aimi_merlin`; kind upstream_release; status gated; re-acquisition manual (Stanford AIMI portal).

**Source id**

`stanford_aimi_merlin` (acquisition/ranking.csv collection `stanford_aimi:merlin`)

**Name and citation**

Merlin abdominal CT (25,494 CT / 18,317 patients); stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40 (per the MerlinPlus card); Nature 2026, 10.1038/s41586-026-10181-8 (acquisition/ranking.csv)

**Modality**

CT, coverage AP:18317 (acquisition/ranking.csv); note: size not stated in the catalogue; not estimated here; AbdomenAtlas/MerlinPlus on HF holds masks + patient-level longitudinal ids only (CC BY-NC-ND), no CT (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

DUA: Stanford AIMI research-use agreement (non-commercial); derived labels yes (non-commercial) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 7)

**How it was acquired**

not acquired; none signed, none registered (acquisition/ACQUISITION_PLAN.md section 7)

**When**

found in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

18,317 people listed; E_low 1259.9, E_count 673.0 (acquisition/ranking.csv); size not stated (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known (Stanford ED 2012-18) (acquisition/ranking.csv)

**Re-acquisition recipe**

manual: sign in to the Stanford AIMI portal, accept the non-commercial research-use DUA on stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40 (also stanford.redivis.com/datasets/exfv-e8h3kvfhs); a time-limited Azure Blob URL is issued for AzCopy; verify against the portal's file list; size not stated (acquisition/ACQUISITION_PLAN.md section 7)

---

### `rsna_ratic_abdominal_trauma` <a id="rsna_ratic_abdominal_trauma"></a>

**RSNA Abdominal Traumatic Injury CT, RATIC (3,147 patients / 4,711 series).** Cards: B (RSNA Abdominal Traumatic Injury CT, RATIC (3,147 patients / 4,711 series)). Structured entry: `sources.yaml` id `rsna_ratic_abdominal_trauma`; kind upstream_release; status gated; re-acquisition manual (RSNA MIRA / Kaggle).

**Source id**

`rsna_ratic_abdominal_trauma` (acquisition/ranking.csv collection `rsna:ratic_abdominal_trauma`)

**Name and citation**

RSNA Abdominal Traumatic Injury CT, RATIC (3,147 patients / 4,711 series); registry.opendata.aws/rsna-ratic (ControlledAccess: mira.rsna.org/dataset/5); 10.1148/ryai.240101 (acquisition/ranking.csv)

**Modality**

CT, coverage CAP:3147 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

registration: RSNA terms: non-commercial, no redistribution of any portion; derived labels internal use only (no redistribution) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 7)

**How it was acquired**

not acquired; none signed, none registered (acquisition/ACQUISITION_PLAN.md section 7)

**When**

found in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

3,147 people listed; E_low 240.7, E_count 135.8 (acquisition/ranking.csv); size not stated (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

possibly partly inside AbdomenAtlas 1.1 (listed in its Table 1; the public 9,262's composition is unpublished) (acquisition/ranking.csv)

**Re-acquisition recipe**

manual: a MIRA (mira.rsna.org/dataset/5, controlled access to s3://abdominal-trauma-detection) or Kaggle account and acceptance of RSNA's terms (non-commercial, no redistribution); derived labels internal only (acquisition/ACQUISITION_PLAN.md section 7)

---

### `hf_ct_rate` <a id="hf_ct_rate"></a>

**CT-RATE (25,692 chest CT / 21,304 patients).** Cards: B (CT-RATE (25,692 chest CT / 21,304 patients)). Structured entry: `sources.yaml` id `hf_ct_rate`; kind upstream_release; status gated; re-acquisition manual (hf).

**Source id**

`hf_ct_rate` (acquisition/ranking.csv collection `hf:ct_rate`)

**Name and citation**

CT-RATE (25,692 chest CT / 21,304 patients); HF API 2026-09-23 (gated: auto; Name, Institution, Email, checkbox) (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:21304 (acquisition/ranking.csv); note: T13 by rib count only (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

registration: CC BY-NC-SA 4.0; derived labels yes (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 7)

**How it was acquired**

not acquired; none signed, none registered (acquisition/ACQUISITION_PLAN.md section 7)

**When**

found in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

21,304 people listed; E_low 94.9, E_count 94.9 (acquisition/ranking.csv); size not stated (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

3,134 volumes rehosted in CADS (acquisition/ranking.csv)

**Re-acquisition recipe**

manual: HF account and the gate form (Name, Institution, Email, terms checkbox) on huggingface.co/datasets/ibrahimhamamci/CT-RATE; then `acquisition_fetch.py hf` would need a token, which the tool does not pass; ungated re-uploads exist and were deliberately not used (acquisition/ACQUISITION_PLAN.md section 7)

---

### `stanford_aimi_inspect` <a id="stanford_aimi_inspect"></a>

**INSPECT (CT pulmonary angiography, ~19,400 patients).** Cards: B (INSPECT (CT pulmonary angiography, ~19,400 patients)). Structured entry: `sources.yaml` id `stanford_aimi_inspect`; kind upstream_release; status gated; re-acquisition manual (Stanford AIMI portal).

**Source id**

`stanford_aimi_inspect` (acquisition/ranking.csv collection `stanford_aimi:inspect`)

**Name and citation**

INSPECT (CT pulmonary angiography, ~19,400 patients); Stanford AIMI catalogue (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:19402 (acquisition/ranking.csv); note: T13 by rib count only (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

DUA: Stanford AIMI research-use agreement; derived labels yes (non-commercial) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 7)

**How it was acquired**

not acquired; none signed, none registered (acquisition/ACQUISITION_PLAN.md section 7)

**When**

found in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

19,402 people listed; E_low 86.4, E_count 86.4 (acquisition/ranking.csv); size not stated (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known (acquisition/ranking.csv)

**Re-acquisition recipe**

manual: the same AIMI research-use agreement as Merlin (acquisition/ACQUISITION_PLAN.md section 7)

---

### `hf_cads_unique` <a id="hf_cads_unique"></a>

**CADS-dataset parts not reachable elsewhere (CT-TRI 586, VISCERAL gc+sc 167).** Cards: B (CADS-dataset parts not reachable elsewhere (CT-TRI 586, VISCERAL gc+sc 167)). Structured entry: `sources.yaml` id `hf_cads_unique`; kind upstream_release; status gated; re-acquisition manual (hf).

**Source id**

`hf_cads_unique` (acquisition/ranking.csv collection `hf:cads_unique`)

**Name and citation**

CADS-dataset parts not reachable elsewhere (CT-TRI 586, VISCERAL gc+sc 167); HF tree 2026-09-23: 0043_new_ct_tri 586 images 83.4 GB; 0001/0002 visceral 167 images 39.9 GB (acquisition/ranking.csv)

**Modality**

CT, coverage WB:753 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

registration: per component; CT-TRI under CADS terms; derived labels check CT-TRI terms (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 7)

**How it was acquired**

not acquired; none signed, none registered (acquisition/ACQUISITION_PLAN.md section 7)

**When**

found in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

753 people listed; E_low 48.5, E_count 27.4 (acquisition/ranking.csv); 123.3 GB (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

the other 33 CADS folders are sources listed separately here (TotalSegmentator, VerSe on disk; NLST, LIDC, TCGA, CPTAC via IDC; AMOS, RibFrac, AbdomenCT-1K via their own routes) (acquisition/ranking.csv)

**Re-acquisition recipe**

manual: HF account and one checkbox on huggingface.co/datasets/mrmrx/CADS-dataset; read CT-TRI's own terms before any derived label; VISCERAL folders carry the VISCERAL agreement text (acquisition/ACQUISITION_PLAN.md section 7)

---

### `rsna_rspect_pe` <a id="rsna_rspect_pe"></a>

**RSNA-STR Pulmonary Embolism CT, RSPECT (7,279 training studies).** Cards: B (RSNA-STR Pulmonary Embolism CT, RSPECT (7,279 training studies)). Structured entry: `sources.yaml` id `rsna_rspect_pe`; kind upstream_release; status gated; re-acquisition manual (RSNA MIRA / Kaggle).

**Source id**

`rsna_rspect_pe` (acquisition/ranking.csv collection `rsna:rspect_pe`)

**Name and citation**

RSNA-STR Pulmonary Embolism CT, RSPECT (7,279 training studies); kaggle.com/c/rsna-str-pulmonary-embolism-detection (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:7279 (acquisition/ranking.csv); note: CTPA: T13 by rib count only (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

registration: RSNA terms: non-commercial research; derived labels internal use (RSNA terms) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 7)

**How it was acquired**

not acquired; none signed, none registered (acquisition/ACQUISITION_PLAN.md section 7)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

7,279 people listed; E_low 32.4, E_count 32.4 (acquisition/ranking.csv); size not stated (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known (acquisition/ranking.csv)

**Re-acquisition recipe**

manual: Kaggle account and acceptance of the rsna-str-pulmonary-embolism-detection competition rules (acquisition/ACQUISITION_PLAN.md section 7)

---

### `zenodo_magic_ct` <a id="zenodo_magic_ct"></a>

**MAGIC-CT: 562 patients with abdominal/thoracic tumours (NRRD).** Cards: B (MAGIC-CT: 562 patients with abdominal/thoracic tumours (NRRD)). Structured entry: `sources.yaml` id `zenodo_magic_ct`; kind upstream_release; status gated; re-acquisition manual (zenodo).

**Source id**

`zenodo_magic_ct` (acquisition/ranking.csv collection `zenodo:magic_ct`)

**Name and citation**

MAGIC-CT: 562 patients with abdominal/thoracic tumours (NRRD); zenodo.org/records/18389015 (acquisition/ranking.csv)

**Modality**

CT, coverage CA:562 (acquisition/ranking.csv); note: files download without a gate; the DUA text asks for an application and training proof, which only Greg can give (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

DUA: CC0 label, but the record carries a data-use agreement (application, HIPAA-training proof); derived labels yes (under the DUA) (acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 7)

**How it was acquired**

not acquired; none signed, none registered (acquisition/ACQUISITION_PLAN.md section 7)

**When**

found 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

562 people listed; E_low 27.9, E_count 15.7 (acquisition/ranking.csv); size not stated (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

none known (Kazakhstan) (acquisition/ranking.csv)

**Re-acquisition recipe**

manual: files download without a gate, but the record's DUA requires an application with proof of human-subjects/HIPAA training that only Greg can make; not fetched (acquisition/ACQUISITION_PLAN.md section 7)

---

### Group B8. No new countable people, or excluded by licence (not fetched by this chain)

### `idc_tcga_prad` <a id="idc_tcga_prad"></a>

**tcga_prad.** Cards: B (tcga_prad). Structured entry: `sources.yaml` id `idc_tcga_prad`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_prad` (acquisition/ranking.csv collection `idc:tcga_prad`)

**Name and citation**

tcga_prad; 10.7937/k9/tcia.2016.yxoglm4y (acquisition/ranking.csv)

**Modality**

CT, coverage CAP:2 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

4 listed, 2 qualifying, 2 new; 1.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: localizer image type:10;slice > 3.0 mm:6;< 60 slices:1;reformat/MIP series:1 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_kirp` <a id="idc_tcga_kirp"></a>

**tcga_kirp.** Cards: B (tcga_kirp). Structured entry: `sources.yaml` id `idc_tcga_kirp`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_kirp` (acquisition/ranking.csv collection `idc:tcga_kirp`)

**Name and citation**

tcga_kirp; 10.7937/k9/tcia.2016.acwogbef (acquisition/ranking.csv)

**Modality**

CT, coverage ABD:3;AP:3 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

23 listed, 6 qualifying, 6 new; 4.5 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:65;localizer image type:29;non-axial reformat:5;not a regularly spaced 3-D volume:3 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_cmb_pca` <a id="idc_cmb_pca"></a>

**cmb_pca.** Cards: B (cmb_pca). Structured entry: `sources.yaml` id `idc_cmb_pca`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cmb_pca` (acquisition/ranking.csv collection `idc:cmb_pca`)

**Name and citation**

cmb_pca; 10.7937/25t7-6y12 (acquisition/ranking.csv)

**Modality**

CT, coverage WB:3;AP:1;CHEST:1;CAP:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

11 listed, 6 qualifying, 6 new; 11.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:60;non-axial reformat:44;localizer image type:38;< 60 slices:19 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_kich` <a id="idc_tcga_kich"></a>

**tcga_kich.** Cards: B (tcga_kich). Structured entry: `sources.yaml` id `idc_tcga_kich`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_kich` (acquisition/ranking.csv collection `idc:tcga_kich`)

**Name and citation**

tcga_kich; 10.7937/k9/tcia.2016.yu3rbczn (acquisition/ranking.csv)

**Modality**

CT, coverage ABD:6 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

12 listed, 6 qualifying, 6 new; 3.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:31;localizer image type:15;reformat/MIP series:8 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_coad` <a id="idc_tcga_coad"></a>

**tcga_coad.** Cards: B (tcga_coad). Structured entry: `sources.yaml` id `idc_tcga_coad`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_coad` (acquisition/ranking.csv collection `idc:tcga_coad`)

**Name and citation**

tcga_coad; 10.7937/k9/tcia.2016.hjjhboxz (acquisition/ranking.csv)

**Modality**

CT, coverage AP:3;CAP:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

25 listed, 4 qualifying, 4 new; 4.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:40;localizer image type:37;non-axial reformat:4;reformat/MIP series:2 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_rider_pilot` <a id="idc_rider_pilot"></a>

**rider_pilot.** Cards: B (rider_pilot). Structured entry: `sources.yaml` id `idc_rider_pilot`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_rider_pilot` (acquisition/ranking.csv collection `idc:rider_pilot`)

**Name and citation**

rider_pilot; 10.7937/m87f-mz83 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:6;CAP:2 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

8 listed, 8 qualifying, 8 new; 10.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:45;localizer image type:32;non-axial reformat:31;< 60 slices:6 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_cmb_gec` <a id="idc_cmb_gec"></a>

**cmb_gec.** Cards: B (cmb_gec). Structured entry: `sources.yaml` id `idc_cmb_gec`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cmb_gec` (acquisition/ranking.csv collection `idc:cmb_gec`)

**Name and citation**

cmb_gec; 10.7937/e7kh-r486 (acquisition/ranking.csv)

**Modality**

CT, coverage AP:3;ABD:1;CHEST:1;WB:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

6 listed, 6 qualifying, 6 new; 11.9 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:29;non-axial reformat:22;reformat/MIP series:20;localizer image type:16 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_thca` <a id="idc_tcga_thca"></a>

**tcga_thca.** Cards: B (tcga_thca). Structured entry: `sources.yaml` id `idc_tcga_thca`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_thca` (acquisition/ranking.csv collection `idc:tcga_thca`)

**Name and citation**

tcga_thca; 10.7937/k9/tcia.2016.9zfrvf1b (acquisition/ranking.csv)

**Modality**

CT, coverage HN:4;WB:1;CHEST:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

6 listed, 6 qualifying, 6 new; 1.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: localizer image type:4;non-axial reformat:2;< 60 slices:2;slice > 3.0 mm:2 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_nsclc_radiomics_genomics` <a id="idc_nsclc_radiomics_genomics"></a>

**nsclc_radiomics_genomics.** Cards: B (nsclc_radiomics_genomics). Structured entry: `sources.yaml` id `idc_nsclc_radiomics_genomics`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_nsclc_radiomics_genomics` (acquisition/ranking.csv collection `idc:nsclc_radiomics_genomics`)

**Name and citation**

nsclc_radiomics_genomics; 10.7937/k9/tcia.2015.l4fret6z (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:8;WB:2 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

89 listed, 10 qualifying, 10 new; 6.9 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:75;not a regularly spaced 3-D volume:4 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_qin_lung_ct` <a id="idc_qin_lung_ct"></a>

**qin_lung_ct.** Cards: B (qin_lung_ct). Structured entry: `sources.yaml` id `idc_qin_lung_ct`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_qin_lung_ct` (acquisition/ranking.csv collection `idc:qin_lung_ct`)

**Name and citation**

qin_lung_ct; 10.7937/k9/tcia.2015.npgzyzbz (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:10;ABD:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

47 listed, 11 qualifying, 11 new; 2.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:36 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_lusc` <a id="idc_tcga_lusc"></a>

**tcga_lusc.** Cards: B (tcga_lusc). Structured entry: `sources.yaml` id `idc_tcga_lusc`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_lusc` (acquisition/ranking.csv collection `idc:tcga_lusc`)

**Name and citation**

tcga_lusc; 10.7937/k9/tcia.2016.tygkkfmq (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:13;WB:2;AP:2;CA:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

37 listed, 18 qualifying, 18 new; 14.1 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:91;localizer image type:62;< 60 slices:17;reformat/MIP series:7 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_luad` <a id="idc_tcga_luad"></a>

**tcga_luad.** Cards: B (tcga_luad). Structured entry: `sources.yaml` id `idc_tcga_luad`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_luad` (acquisition/ranking.csv collection `idc:tcga_luad`)

**Name and citation**

tcga_luad; 10.7937/k9/tcia.2016.jgnihep5 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:14;WB:2 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

67 listed, 16 qualifying, 16 new; 18.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:296;localizer image type:147;< 60 slices:47;non-axial reformat:10 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_lctsc` <a id="idc_lctsc"></a>

**lctsc.** Cards: B (lctsc). Structured entry: `sources.yaml` id `idc_lctsc`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_lctsc` (acquisition/ranking.csv collection `idc:lctsc`)

**Name and citation**

lctsc; 10.7937/k9/tcia.2017.3r3fvz08 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:37;WB:4 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

60 listed, 41 qualifying, 41 new; 4.9 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: non-axial reformat:19 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_spie_aapm_lung_ct_challenge` <a id="idc_spie_aapm_lung_ct_challenge"></a>

**spie_aapm_lung_ct_challenge.** Cards: B (spie_aapm_lung_ct_challenge). Structured entry: `sources.yaml` id `idc_spie_aapm_lung_ct_challenge`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_spie_aapm_lung_ct_challenge` (acquisition/ranking.csv collection `idc:spie_aapm_lung_ct_challenge`)

**Name and citation**

spie_aapm_lung_ct_challenge; 10.7937/k9/tcia.2015.uzlsu3fl (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:70 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

70 listed, 70 qualifying, 70 new; 11.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py) (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_rider_lung_ct` <a id="idc_rider_lung_ct"></a>

**rider_lung_ct.** Cards: B (rider_lung_ct). Structured entry: `sources.yaml` id `idc_rider_lung_ct`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_rider_lung_ct` (acquisition/ranking.csv collection `idc:rider_lung_ct`)

**Name and citation**

rider_lung_ct; 10.7937/k9/tcia.2015.u1x8a5nr (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:31 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

32 listed, 31 qualifying, 31 new; 41.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:152;localizer image type:59;not a regularly spaced 3-D volume:32;< 60 slices:1 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_4d_lung` <a id="idc_4d_lung"></a>

**4d_lung.** Cards: B (4d_lung). Structured entry: `sources.yaml` id `idc_4d_lung`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_4d_lung` (acquisition/ranking.csv collection `idc:4d_lung`)

**Name and citation**

4d_lung; 10.7937/k9/tcia.2016.eln8ygle (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

20 listed, 0 qualifying, 0 new; 178.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:5890 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_breast_diagnosis` <a id="idc_breast_diagnosis"></a>

**breast_diagnosis.** Cards: B (breast_diagnosis). Structured entry: `sources.yaml` id `idc_breast_diagnosis`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_breast_diagnosis` (acquisition/ranking.csv collection `idc:breast_diagnosis`)

**Name and citation**

breast_diagnosis; 10.7937/k9/tcia.2015.sdnrqxxr (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

3 listed, 0 qualifying, 0 new; 1.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:18 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_c4kc_kits` <a id="idc_c4kc_kits"></a>

**c4kc_kits.** Cards: B (c4kc_kits). Structured entry: `sources.yaml` id `idc_c4kc_kits`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_c4kc_kits` (acquisition/ranking.csv collection `idc:c4kc_kits`)

**Name and citation**

c4kc_kits; 10.7937/tcia.2019.ix49e8nx (acquisition/ranking.csv)

**Modality**

CT, coverage ABD:66;AP:47;CAP:4;CA:3 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

210 listed, 120 qualifying, 0 new; 36.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

carried inside abdomenatlas3_mini (see that card) (acquisition/ranking.csv)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: carried by abdomenatlas3_mini (KiTS); counted there; refused: slice > 3.0 mm:186;< 60 slices:5;non-axial reformat:1 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_cc_radiomics_phantom` <a id="idc_cc_radiomics_phantom"></a>

**cc_radiomics_phantom.** Cards: B (cc_radiomics_phantom). Structured entry: `sources.yaml` id `idc_cc_radiomics_phantom`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cc_radiomics_phantom` (acquisition/ranking.csv collection `idc:cc_radiomics_phantom`)

**Name and citation**

cc_radiomics_phantom; 10.7937/k9/tcia.2017.zuzrml5b (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

17 listed, 0 qualifying, 0 new; 1.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:17 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_cc_radiomics_phantom_2` <a id="idc_cc_radiomics_phantom_2"></a>

**cc_radiomics_phantom_2.** Cards: B (cc_radiomics_phantom_2). Structured entry: `sources.yaml` id `idc_cc_radiomics_phantom_2`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cc_radiomics_phantom_2` (acquisition/ranking.csv collection `idc:cc_radiomics_phantom_2`)

**Name and citation**

cc_radiomics_phantom_2; 10.7937/tcia.2019.4l24tz5g (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

251 listed, 0 qualifying, 0 new; 29.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:251 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_cc_radiomics_phantom_3` <a id="idc_cc_radiomics_phantom_3"></a>

**cc_radiomics_phantom_3.** Cards: B (cc_radiomics_phantom_3). Structured entry: `sources.yaml` id `idc_cc_radiomics_phantom_3`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cc_radiomics_phantom_3` (acquisition/ranking.csv collection `idc:cc_radiomics_phantom_3`)

**Name and citation**

cc_radiomics_phantom_3; 10.7937/tcia.2019.j71i4fah (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

95 listed, 0 qualifying, 0 new; 13.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:275 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_cc_tumor_heterogeneity` <a id="idc_cc_tumor_heterogeneity"></a>

**cc_tumor_heterogeneity.** Cards: B (cc_tumor_heterogeneity). Structured entry: `sources.yaml` id `idc_cc_tumor_heterogeneity`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cc_tumor_heterogeneity` (acquisition/ranking.csv collection `idc:cc_tumor_heterogeneity`)

**Name and citation**

cc_tumor_heterogeneity; 10.7937/erz5-qz59 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

22 listed, 0 qualifying, 0 new; 11.2 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:65 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_cmb_aml` <a id="idc_cmb_aml"></a>

**cmb_aml.** Cards: B (cmb_aml). Structured entry: `sources.yaml` id `idc_cmb_aml`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cmb_aml` (acquisition/ranking.csv collection `idc:cmb_aml`)

**Name and citation**

cmb_aml; 10.7937/pcte-6m66 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

7 listed, 1 qualifying, 1 new; 1.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:15;localizer image type:10;non-axial reformat:4;reformat/MIP series:3 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_cptac_aml` <a id="idc_cptac_aml"></a>

**cptac_aml.** Cards: B (cptac_aml). Structured entry: `sources.yaml` id `idc_cptac_aml`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_cptac_aml` (acquisition/ranking.csv collection `idc:cptac_aml`)

**Name and citation**

cptac_aml; 10.7937/tcia.2019.b6foe619 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:2 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

5 listed, 2 qualifying, 2 new; 2.2 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:15;reformat/MIP series:6;non-axial reformat:6;not a regularly spaced 3-D volume:6 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_ct4harmonization_multicentric` <a id="idc_ct4harmonization_multicentric"></a>

**ct4harmonization_multicentric.** Cards: B (ct4harmonization_multicentric). Structured entry: `sources.yaml` id `idc_ct4harmonization_multicentric`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_ct4harmonization_multicentric` (acquisition/ranking.csv collection `idc:ct4harmonization_multicentric`)

**Name and citation**

ct4harmonization_multicentric; 10.7937/m0pb-bh69 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

1 listed, 0 qualifying, 0 new; 239.8 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:1378 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_ct_lymph_nodes` <a id="idc_ct_lymph_nodes"></a>

**ct_lymph_nodes.** Cards: B (ct_lymph_nodes). Structured entry: `sources.yaml` id `idc_ct_lymph_nodes`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_ct_lymph_nodes` (acquisition/ranking.csv collection `idc:ct_lymph_nodes`)

**Name and citation**

ct_lymph_nodes; 10.7937/k9/tcia.2015.aqiidcnm (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

176 listed, 0 qualifying, 0 new; 56.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: no SliceThickness:176 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_ct_phantom4radiomics` <a id="idc_ct_phantom4radiomics"></a>

**ct_phantom4radiomics.** Cards: B (ct_phantom4radiomics). Structured entry: `sources.yaml` id `idc_ct_phantom4radiomics`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_ct_phantom4radiomics` (acquisition/ranking.csv collection `idc:ct_phantom4radiomics`)

**Name and citation**

ct_phantom4radiomics; 10.7937/a1v1-rc66 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

1 listed, 0 qualifying, 0 new; 40.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:238 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_dro_toolkit` <a id="idc_dro_toolkit"></a>

**dro_toolkit.** Cards: B (dro_toolkit). Structured entry: `sources.yaml` id `idc_dro_toolkit`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_dro_toolkit` (acquisition/ranking.csv collection `idc:dro_toolkit`)

**Name and citation**

dro_toolkit; 10.7937/t062-8262 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

32 listed, 0 qualifying, 0 new; 4.9 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:32 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_ea1141` <a id="idc_ea1141"></a>

**ea1141.** Cards: B (ea1141). Structured entry: `sources.yaml` id `idc_ea1141`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_ea1141` (acquisition/ranking.csv collection `idc:ea1141`)

**Name and citation**

ea1141; 10.7937/2bas-hr33 (acquisition/ranking.csv)

**Modality**

CT, coverage OTHER:1 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

1 listed, 1 qualifying, 1 new; 2.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py) (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_lung_fused_ct_pathology` <a id="idc_lung_fused_ct_pathology"></a>

**lung_fused_ct_pathology.** Cards: B (lung_fused_ct_pathology). Structured entry: `sources.yaml` id `idc_lung_fused_ct_pathology`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_lung_fused_ct_pathology` (acquisition/ranking.csv collection `idc:lung_fused_ct_pathology`)

**Name and citation**

lung_fused_ct_pathology; 10.7937/k9/tcia.2018.smt36lpn (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:5 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

6 listed, 5 qualifying, 5 new; 1.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: < 60 slices:6;slice > 3.0 mm:6;not a regularly spaced 3-D volume:1 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_lung_phantom` <a id="idc_lung_phantom"></a>

**lung_phantom.** Cards: B (lung_phantom). Structured entry: `sources.yaml` id `idc_lung_phantom`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_lung_phantom` (acquisition/ranking.csv collection `idc:lung_phantom`)

**Name and citation**

lung_phantom; 10.7937/k9/tcia.2015.08a1ixoo (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

1 listed, 0 qualifying, 0 new; 0.1 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:1 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_lungct_diagnosis` <a id="idc_lungct_diagnosis"></a>

**lungct_diagnosis.** Cards: B (lungct_diagnosis). Structured entry: `sources.yaml` id `idc_lungct_diagnosis`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_lungct_diagnosis` (acquisition/ranking.csv collection `idc:lungct_diagnosis`)

**Name and citation**

lungct_diagnosis; 10.7937/k9/tcia.2015.a6v7jiwx (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST_SCREEN:10 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

61 listed, 10 qualifying, 10 new; 2.4 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:51 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_naf_prostate` <a id="idc_naf_prostate"></a>

**naf_prostate.** Cards: B (naf_prostate). Structured entry: `sources.yaml` id `idc_naf_prostate`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_naf_prostate` (acquisition/ranking.csv collection `idc:naf_prostate`)

**Name and citation**

naf_prostate; 10.7937/k9/tcia.2015.isoqthko (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

9 listed, 0 qualifying, 0 new; 11.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:75 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_nlm_visible_human_project` <a id="idc_nlm_visible_human_project"></a>

**nlm_visible_human_project.** Cards: B (nlm_visible_human_project). Structured entry: `sources.yaml` id `idc_nlm_visible_human_project`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_nlm_visible_human_project` (acquisition/ranking.csv collection `idc:nlm_visible_human_project`)

**Name and citation**

nlm_visible_human_project; 10.5281/zenodo.12690049 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, National Library of Medicine Terms and Conditions; May 21, 2019; derived labels check (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

2 listed, 0 qualifying, 0 new; 2.1 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:11 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_nsclc_radiomics_interobserver1` <a id="idc_nsclc_radiomics_interobserver1"></a>

**nsclc_radiomics_interobserver1.** Cards: B (nsclc_radiomics_interobserver1). Structured entry: `sources.yaml` id `idc_nsclc_radiomics_interobserver1`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_nsclc_radiomics_interobserver1` (acquisition/ranking.csv collection `idc:nsclc_radiomics_interobserver1`)

**Name and citation**

nsclc_radiomics_interobserver1; 10.7937/tcia.2019.cwvlpd26 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

22 listed, 0 qualifying, 0 new; 2.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:22 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_pancreas_ct` <a id="idc_pancreas_ct"></a>

**pancreas_ct.** Cards: B (pancreas_ct). Structured entry: `sources.yaml` id `idc_pancreas_ct`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_pancreas_ct` (acquisition/ranking.csv collection `idc:pancreas_ct`)

**Name and citation**

pancreas_ct; 10.7937/k9/tcia.2016.tnb1kqbu (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

80 listed, 0 qualifying, 0 new; 9.7 GB all CT (acquisition/ranking.csv)

**Where it is now**

carried inside abdomenatlas3_mini (see that card) (acquisition/ranking.csv)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: carried by abdomenatlas3_mini (Pancreas-CT, via AbdomenCT-1K); counted there; refused: no SliceThickness:80 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_phantom_fda` <a id="idc_phantom_fda"></a>

**phantom_fda.** Cards: B (phantom_fda). Structured entry: `sources.yaml` id `idc_phantom_fda`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_phantom_fda` (acquisition/ranking.csv collection `idc:phantom_fda`)

**Name and citation**

phantom_fda; 10.7937/k9/tcia.2015.orbjkmux (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

7 listed, 0 qualifying, 0 new; 763.9 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:4433 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_pseudo_phi_dicom_data` <a id="idc_pseudo_phi_dicom_data"></a>

**pseudo_phi_dicom_data.** Cards: B (pseudo_phi_dicom_data). Structured entry: `sources.yaml` id `idc_pseudo_phi_dicom_data`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_pseudo_phi_dicom_data` (acquisition/ranking.csv collection `idc:pseudo_phi_dicom_data`)

**Name and citation**

pseudo_phi_dicom_data; 10.7937/s17z-r072 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

10 listed, 0 qualifying, 0 new; 0.3 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:10 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_qiba_ct_1c` <a id="idc_qiba_ct_1c"></a>

**qiba_ct_1c.** Cards: B (qiba_ct_1c). Structured entry: `sources.yaml` id `idc_qiba_ct_1c`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_qiba_ct_1c` (acquisition/ranking.csv collection `idc:qiba_ct_1c`)

**Name and citation**

qiba_ct_1c; 10.7937/k9/tcia.2016.yxgr4blu (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

1 listed, 0 qualifying, 0 new; 35.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:213 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_qiba_ct_liver_phantom` <a id="idc_qiba_ct_liver_phantom"></a>

**qiba_ct_liver_phantom.** Cards: B (qiba_ct_liver_phantom). Structured entry: `sources.yaml` id `idc_qiba_ct_liver_phantom`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_qiba_ct_liver_phantom` (acquisition/ranking.csv collection `idc:qiba_ct_liver_phantom`)

**Name and citation**

qiba_ct_liver_phantom; 10.7937/tcia.rmv0-9y95 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

3 listed, 0 qualifying, 0 new; 52.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:681 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_qin_breast` <a id="idc_qin_breast"></a>

**qin_breast.** Cards: B (qin_breast). Structured entry: `sources.yaml` id `idc_qin_breast`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_qin_breast` (acquisition/ranking.csv collection `idc:qin_breast`)

**Name and citation**

qin_breast; 10.7937/k9/tcia.2016.21juebh0 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

43 listed, 0 qualifying, 0 new; 4.7 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:110 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_rider_phantom_pet_ct` <a id="idc_rider_phantom_pet_ct"></a>

**rider_phantom_pet_ct.** Cards: B (rider_phantom_pet_ct). Structured entry: `sources.yaml` id `idc_rider_phantom_pet_ct`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_rider_phantom_pet_ct` (acquisition/ranking.csv collection `idc:rider_phantom_pet_ct`)

**Name and citation**

rider_phantom_pet_ct; 10.7937/k9/tcia.2015.8wg2kn4w (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

20 listed, 0 qualifying, 0 new; 0.7 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:40 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `idc_soft_tissue_sarcoma` <a id="idc_soft_tissue_sarcoma"></a>

**soft_tissue_sarcoma.** Cards: B (soft_tissue_sarcoma). Structured entry: `sources.yaml` id `idc_soft_tissue_sarcoma`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_soft_tissue_sarcoma` (acquisition/ranking.csv collection `idc:soft_tissue_sarcoma`)

**Name and citation**

soft_tissue_sarcoma; 10.7937/k9/tcia.2015.7go2gsks (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

51 listed, 0 qualifying, 0 new; 7.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:51 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_stageii_colorectal_ct` <a id="idc_stageii_colorectal_ct"></a>

**stageii_colorectal_ct.** Cards: B (stageii_colorectal_ct). Structured entry: `sources.yaml` id `idc_stageii_colorectal_ct`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_stageii_colorectal_ct` (acquisition/ranking.csv collection `idc:stageii_colorectal_ct`)

**Name and citation**

stageii_colorectal_ct; 10.7937/p5k5-tg43 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

230 listed, 0 qualifying, 0 new; 7.1 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:230 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_read` <a id="idc_tcga_read"></a>

**tcga_read.** Cards: B (tcga_read). Structured entry: `sources.yaml` id `idc_tcga_read`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_read` (acquisition/ranking.csv collection `idc:tcga_read`)

**Name and citation**

tcga_read; 10.7937/k9/tcia.2016.f7ppnpnu (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

3 listed, 0 qualifying, 0 new; 0.2 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:3;localizer image type:3;reformat/MIP series:1 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_tcga_sarc` <a id="idc_tcga_sarc"></a>

**tcga_sarc.** Cards: B (tcga_sarc). Structured entry: `sources.yaml` id `idc_tcga_sarc`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_tcga_sarc` (acquisition/ranking.csv collection `idc:tcga_sarc`)

**Name and citation**

tcga_sarc; 10.7937/k9/tcia.2016.cx6ylsux (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 3.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

4 listed, 0 qualifying, 0 new; 2.6 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: slice > 3.0 mm:5;localizer image type:5;not a regularly spaced 3-D volume:2;non-axial reformat:1 (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned; if wanted, write its manifest with tools/acquisition_census.py and fetch with `acquisition_fetch.py idc --collection <name> --manifest <file>` (tools/acquisition_census.py; tools/acquisition_fetch.py)

---

### `idc_uw_cirp_mouse_pet_ct_nsclc` <a id="idc_uw_cirp_mouse_pet_ct_nsclc"></a>

**uw_cirp_mouse_pet_ct_nsclc.** Cards: B (uw_cirp_mouse_pet_ct_nsclc). Structured entry: `sources.yaml` id `idc_uw_cirp_mouse_pet_ct_nsclc`; kind upstream_release; status excluded; re-acquisition manual (idc).

**Source id**

`idc_uw_cirp_mouse_pet_ct_nsclc` (acquisition/ranking.csv collection `idc:uw_cirp_mouse_pet_ct_nsclc`)

**Name and citation**

uw_cirp_mouse_pet_ct_nsclc; 10.5281/zenodo.17257735 (acquisition/ranking.csv)

**Modality**

CT, coverage none qualifying (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; it would be the IDC route (`acquisition_fetch.py idc`) from a census manifest (tools/acquisition_fetch.py; tools/acquisition_census.py)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

14 listed, 0 qualifying, 0 new; 34.5 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); refused: phantom/animal/test collection:25 (acquisition/ranking.csv)

**Re-acquisition recipe**

not applicable: phantom, animal or test collection (tools/acquisition_census.py EXCLUDE_COLLECTION)

---

### `excluded_glocker_spine` <a id="excluded_glocker_spine"></a>

**Glocker spine CT (SpineWeb 3; 125 patients / 242 scans).** Cards: B (Glocker spine CT (SpineWeb 3; 125 patients / 242 scans)). Structured entry: `sources.yaml` id `excluded_glocker_spine`; kind upstream_release; status excluded; re-acquisition manual (none (excluded)).

**Source id**

`excluded_glocker_spine` (acquisition/ranking.csv collection `excluded:glocker_spine`)

**Name and citation**

Glocker spine CT (SpineWeb 3; 125 patients / 242 scans); tools/CT_MINE_REPORT.md Part 1 (acquisition/ranking.csv)

**Modality**

CT, coverage SPINE:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC-ND 4.0; derived labels NO (acquisition/ranking.csv)

**How it was acquired**

not fetched; Imperial Box link (acquisition/ranking.csv)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

125 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

excluded (licence forbids derived labels) (tools/acquisition_census.py); dedup: excluded by criterion (c): ND forbids re-annotation (acquisition/ranking.csv)

**Re-acquisition recipe**

none: the licence forbids derived works, and no form would change that (acquisition/ACQUISITION_PLAN.md section 7)

---

### `hf_bodymaps_pantsmini` <a id="hf_bodymaps_pantsmini"></a>

**PanTSMini (9,901 CT volumes).** Cards: B (PanTSMini (9,901 CT volumes)). Structured entry: `sources.yaml` id `hf_bodymaps_pantsmini`; kind upstream_release; status excluded; re-acquisition manual (hf).

**Source id**

`hf_bodymaps_pantsmini` (acquisition/ranking.csv collection `hf:BodyMaps/PanTSMini`)

**Name and citation**

PanTSMini (9,901 CT volumes); HF metadata.xlsx read 2026-09-24 (acquisition/ranking.csv)

**Modality**

CT, coverage ABD:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC-SA 4.0; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; HuggingFace, ungated (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

9,901 listed, 0 qualifying, 0 new; 345.7 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (aggregator of sources counted elsewhere; CTSP people inside) (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: AGGREGATOR by its own metadata.xlsx: CT Colonography 2,810 volumes (= CTSpinoPelvic1K people), TotalSegmentator 1,229, MSKCC 966, Tuebingen 894 (autoPET), Minnesota 665 (KiTS), Longgang 200 (AMOS), IRCAD 173, NIH 97, ... ; Warsaw 293 = WAW-TACE (fetched directly); 694 volumes name no site; refused: the 694 site-less volumes are spread over every tar (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned (no new countable people (aggregator of sources counted elsewhere; CTSP people inside)) (acquisition/ranking.csv)

---

### `hf_bodymaps_cancerverse` <a id="hf_bodymaps_cancerverse"></a>

**CancerVerse (BodyMaps).** Cards: B (CancerVerse (BodyMaps)). Structured entry: `sources.yaml` id `hf_bodymaps_cancerverse`; kind upstream_release; status excluded; re-acquisition manual (hf).

**Source id**

`hf_bodymaps_cancerverse` (acquisition/ranking.csv collection `hf:BodyMaps/CancerVerse`)

**Name and citation**

CancerVerse (BodyMaps); HF API 2026-09-24 (acquisition/ranking.csv)

**Modality**

CT, coverage ABD:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC-ND 4.0; derived labels NO (acquisition/ranking.csv)

**How it was acquired**

not fetched; HuggingFace, ungated (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

0 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

excluded (licence forbids derived labels) (tools/acquisition_census.py); dedup: excluded by criterion (c): ND forbids re-annotation (acquisition/ranking.csv)

**Re-acquisition recipe**

none: the licence forbids derived works, and no form would change that (acquisition/ACQUISITION_PLAN.md section 7)

---

### `zenodo_lndb` <a id="zenodo_lndb"></a>

**LNDb chest CT (294).** Cards: B (LNDb chest CT (294)). Structured entry: `sources.yaml` id `zenodo_lndb`; kind upstream_release; status excluded; re-acquisition manual (zenodo).

**Source id**

`zenodo_lndb` (acquisition/ranking.csv collection `zenodo:lndb`)

**Name and citation**

LNDb chest CT (294); zenodo.org/records/8348419 (acquisition/ranking.csv)

**Modality**

CT, coverage CHEST:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, CC BY-NC-ND per the record's own text (licence field CC BY 4.0); derived labels NO (acquisition/ranking.csv)

**How it was acquired**

not fetched; Zenodo 8348419 (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

294 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

excluded (licence forbids derived labels) (tools/acquisition_census.py); dedup: excluded by criterion (c): the dataset's text states ND (acquisition/ranking.csv)

**Re-acquisition recipe**

none: the licence forbids derived works, and no form would change that (acquisition/ACQUISITION_PLAN.md section 7)

---

### `zenodo_auc23_lung_ct_covid` <a id="zenodo_auc23_lung_ct_covid"></a>

**AUC23 'Lung CT COVID-19' batches 1-6.** Cards: B (AUC23 'Lung CT COVID-19' batches 1-6). Structured entry: `sources.yaml` id `zenodo_auc23_lung_ct_covid`; kind upstream_release; status excluded; re-acquisition manual (zenodo).

**Source id**

`zenodo_auc23_lung_ct_covid` (acquisition/ranking.csv collection `zenodo:auc23_lung_ct_covid`)

**Name and citation**

AUC23 'Lung CT COVID-19' batches 1-6; zenodo.org/records/7969800 (acquisition/ranking.csv)

**Modality**

CT, coverage n/a:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, various; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; Zenodo 7969800 ... (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

0 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: = STOIC2021 restructured (tier 2 row) (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned (no new countable people) (acquisition/ranking.csv)

---

### `zenodo_auc23_rib_ct_fracture` <a id="zenodo_auc23_rib_ct_fracture"></a>

**AUC23 'Rib CT fracture'.** Cards: B (AUC23 'Rib CT fracture'). Structured entry: `sources.yaml` id `zenodo_auc23_rib_ct_fracture`; kind upstream_release; status excluded; re-acquisition manual (zenodo).

**Source id**

`zenodo_auc23_rib_ct_fracture` (acquisition/ranking.csv collection `zenodo:auc23_rib_ct_fracture`)

**Name and citation**

AUC23 'Rib CT fracture'; zenodo.org/records/8054740 (acquisition/ranking.csv)

**Modality**

CT, coverage n/a:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, various; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; Zenodo 8054740 (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

0 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: centre-cropped RibFrac fractures: key crops, no count (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned (no new countable people) (acquisition/ranking.csv)

---

### `zenodo_pancreas_abdomenct1k_curated` <a id="zenodo_pancreas_abdomenct1k_curated"></a>

**Curated pancreas benchmark (2 records).** Cards: B (Curated pancreas benchmark (2 records)). Structured entry: `sources.yaml` id `zenodo_pancreas_abdomenct1k_curated`; kind upstream_release; status excluded; re-acquisition manual (zenodo).

**Source id**

`zenodo_pancreas_abdomenct1k_curated` (acquisition/ranking.csv collection `zenodo:pancreas_abdomenct1k_curated`)

**Name and citation**

Curated pancreas benchmark (2 records); zenodo.org/records/15467847 (acquisition/ranking.csv)

**Modality**

CT, coverage n/a:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, various; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; Zenodo 15467847, 15476771 (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

0 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: a selection of AbdomenCT-1K (inside AbdomenAtlas) (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned (no new countable people) (acquisition/ranking.csv)

---

### `zenodo_tavrp_pl` <a id="zenodo_tavrp_pl"></a>

**TAVRP-PL.** Cards: B (TAVRP-PL). Structured entry: `sources.yaml` id `zenodo_tavrp_pl`; kind upstream_release; status excluded; re-acquisition manual (zenodo).

**Source id**

`zenodo_tavrp_pl` (acquisition/ranking.csv collection `zenodo:tavrp_pl`)

**Name and citation**

TAVRP-PL; zenodo.org/records/16274177 (acquisition/ranking.csv)

**Modality**

CT, coverage n/a:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, various; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; Zenodo 16274177 (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

0 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: 578 CT of the TotalSegmentator dataset (on disk) (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned (no new countable people) (acquisition/ranking.csv)

---

### `zenodo_merged_multiorgan_abdominal` <a id="zenodo_merged_multiorgan_abdominal"></a>

**Merged multi-organ abdominal CT.** Cards: B (Merged multi-organ abdominal CT). Structured entry: `sources.yaml` id `zenodo_merged_multiorgan_abdominal`; kind upstream_release; status excluded; re-acquisition manual (zenodo).

**Source id**

`zenodo_merged_multiorgan_abdominal` (acquisition/ranking.csv collection `zenodo:merged_multiorgan_abdominal`)

**Name and citation**

Merged multi-organ abdominal CT; zenodo.org/records/11635577 (acquisition/ranking.csv)

**Modality**

CT, coverage n/a:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, various; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; Zenodo 11635577 (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

0 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: merged public sets (inside AbdomenAtlas) (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned (no new countable people) (acquisition/ranking.csv)

---

### `zenodo_synthrad2025` <a id="zenodo_synthrad2025"></a>

**SynthRAD2025 training.** Cards: B (SynthRAD2025 training). Structured entry: `sources.yaml` id `zenodo_synthrad2025`; kind upstream_release; status excluded; re-acquisition manual (zenodo).

**Source id**

`zenodo_synthrad2025` (acquisition/ranking.csv collection `zenodo:synthrad2025`)

**Name and citation**

SynthRAD2025 training; zenodo.org/records/15373853 (acquisition/ranking.csv)

**Modality**

CT, coverage n/a:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

open, various; derived labels yes (acquisition/ranking.csv)

**How it was acquired**

not fetched; Zenodo 15373853 (acquisition/ranking.csv)

**When**

assessed 2026-09-24 sweep (acquisition/ranking.csv)

**What it contains**

0 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

no new countable people (rule: n_new 0 or E_low < 0.5, or a phantom/animal/test collection) (tools/acquisition_census.py); dedup: radiotherapy CT cropped to the paired MR/CBCT field: no count (acquisition/ranking.csv)

**Re-acquisition recipe**

not planned (no new countable people) (acquisition/ranking.csv)

---

### `excluded_nmdid` <a id="excluded_nmdid"></a>

**NMDID post-mortem CT (15,243 decedents).** Cards: B (NMDID post-mortem CT (15,243 decedents)). Structured entry: `sources.yaml` id `excluded_nmdid`; kind upstream_release; status excluded; re-acquisition manual (none (excluded)).

**Source id**

`excluded_nmdid` (acquisition/ranking.csv collection `excluded:nmdid`)

**Name and citation**

NMDID post-mortem CT (15,243 decedents); tools/CT_MINE_REPORT.md Part 1 (acquisition/ranking.csv)

**Modality**

CT, coverage WB:0 (acquisition/ranking.csv)

**Position/view**

not recorded (acquisition/ranking.csv)

**Licence and access**

DUA, custom DUA forbidding derivative works; derived labels NO (acquisition/ranking.csv)

**How it was acquired**

not fetched; nmdid.unm.edu (acquisition/ranking.csv)

**When**

assessed in the 2026-09-23 census (acquisition/ranking.csv)

**What it contains**

15,243 listed, 0 qualifying, 0 new; 0.0 GB all CT (acquisition/ranking.csv)

**Where it is now**

not on disk (listing)

**Annotation status**

none acquired (acquisition/ranking.csv)

**Derived products**

none (listing)

**Known defects and gaps**

excluded (licence forbids derived labels) (tools/acquisition_census.py); dedup: excluded by criterion (c): derived labels are a derivative work (acquisition/ranking.csv)

**Re-acquisition recipe**

none: the licence forbids derived works, and no form would change that (acquisition/ACQUISITION_PLAN.md section 7)

---

## 7. Family C: real X-ray and fluoroscopy with 3-D truth or pose

The family's own preface, legend and shared notes, verbatim:

Written 2026-10-07 from files on this Windows machine only (no grid, no network). Every line cites the file it
was read from, in parentheses. A fact with no file behind it is written "not recorded" and listed in the
`unknowns` table at the end.

**Path conventions used in the citations**

- Bare repo-relative paths (`docs/...`, `tools/...`, `slurm/...`, `SchwingNet/...`) are under
  `<repo spinesurg-ct-nnunet 097933a>`.
- `LISTING` = `<session scratchpad; not a dependency>/census/toplevel_listing.txt`
  (top-level entries of HOME, HOME/data, the Ceph root and Ceph data/, with directory dates; these are directory
  modification dates, not download dates).
- `MEM/<name>` = `<memory notes; see MEMORY.md>/<name>`.
- `LOCAL-THIS-SESSION` = a stat or hash this session took on 2026-10-07 of a file on the Windows desktop.
- On the grid: **CEPH** = `/rs/rs_grp_oschome/go2432/...`, **HOME** = `/wsu/home/go/go24/go2432/...` (Panasas).
  Grid facts come from documents written 2026-09-21 to 2026-09-25. The 2026-10-07 census job (40578909) had not
  landed when this was written, so every "Where it is now" line is as last recorded, not re-checked.

**Two corrections to the brief this family was given, both from the files**

1. The DeepFluoro vendor DICOM deposit is **doi:10.7281/T1/C304HZ**; **doi:10.7281/T1/IFSXNV** is the registered
   H5 release. `docs/DATASHEET.md` §3, `docs/RSNAI_DATA_MANIFEST.json` (`roots.deepfluoro_vendor.source`) and
   `tools/data_manifest.py` (`ROOTS["deepfluoro_vendor"]`) have the two swapped
   (`docs/DATA_COMPLETENESS_AUDIT.md` lines 600 and 731; `tools/jhu_dataverse_fetch.py` docstring;
   `tools/dl_deepfluoro.py` `BASE`). The brief had the vendor DOI right.
2. `carm_drr` is **not** a CBCT render bank. It holds the **real** C-ArmLSpine train and val spot frames, written
   into the DRR-bank layout (`ann/*.json` + `img/*.npy`) (`tools/carmlspine_to_bank.py` docstring). The only
   C-ArmLSpine CBCT render bank on record is `CEPH .../data/rare_class/carmlspine_cbct_drr`
   (`tools/rare_class_carmlspine_drr.py` docstring). The `docs/CT_INVENTORY.md` row for `carm_drr`
   ("C-ArmLSpine CBCT ... renders 240") describes it wrongly.

**Cards in this file:** `carmlspine`, `carm_drr` (with the other C-ArmLSpine banks), `deepfluoro_h5`,
`deepfluoro_vendor`, `deepfluoro_xvr_hf`, `cobra2026`, `geneva_hip`, `ljubljana_2d3d_gs`, `spinesac`,
`realxray_layout` (with `realxray_work` and `pelvis_landmarks`), `or_ready`, `devcorpus` (with `devcorpus_arc` and
the device cards), then the `unknowns` table.

---

### Cards

### `carmlspine` <a id="carmlspine"></a>

**C-ArmLSpine (Zhang et al., MedIA 97:103283, 2024).** Cards: C (carmlspine), E (carmlspine). Structured entry: `sources.yaml` id `carmlspine`; kind upstream_release; status on_disk; re-acquisition run (http).

**Source id**

*[C]*

`carmlspine` (`docs/PATIENT_IDENTITY_SPEC.md` row carmlspine, key `carmlspine:case<N>`).

*[E]*

`carmlspine` (family C's id; `~/carm_drr` is family C's derived card `carm_drr`)

**Name and citation**

*[C]*

- C-ArmLSpine. Zhang et al., Medical Image Analysis 97:103283, 2024 (`slurm/carmlspine_fetch.sh` header). The paper
  is PRSCS-Net, not the PG-Net PDF once attached (`MEM/carmlspine-level-experiment.md`).
- Zenodo DOI 10.5281/zenodo.22768651; file URL `https://zenodo.org/records/22768651/files/C-ArmLSpine.zip?download=1`
  (`slurm/carmlspine_fetch.sh`).
- Release date of the Zenodo record: not recorded.

*[E]*

C-ArmLSpine (Zhang et al., MedIA 97:103283, 2024), Zenodo 10.5281/zenodo.22768651 (`nnunet:slurm/carmlspine_fetch.sh` header).

**Modality**

*[C]*

- Intraoperative C-arm spot exposures, DICOM Modality **XA** (fluoroscopy RF/XA class), plus one **CBCT** per case
  (DICOM Modality CT) and two raw cone-beam sweeps (XA, 1024 rows) (`docs/DATA_COMPLETENESS_AUDIT.md` line 704 and
  Repairs 2026-09-23; `SchwingNet/results/repairs/carm-cases_CHECK.md` §3).
- Device: FIRST/Yiying Surgio-B51 flat panel; panel iRay Jupi1212X, 307.2 mm, 0.150 mm pitch, 2048 px native; SID
  1140 mm, SOD 745 mm. The export is 1024 px at `px_mm_detector` 0.2930 and `px_mm` 0.1915 at the object plane
  (`docs/DATASHEET.md` §2.1; `MEM/carmlspine-level-experiment.md`; git commit 0b0424d message).
- kVp 73–111 (`docs/RSNAI_TABLE1_DATASETS.md`); mAs 0.12–0.13 and pulse 14–20 ms over a 901-file header census
  (`SchwingNet/results/coverage/DICOM_VARIABLES.md`, citing `docs/devices/census/surgio_b51__headers.json`).
- Anatomy: lumbar spine with the sacrum in AP and lateral; thoracic reach about T12/T11 only
  (`MEM/carmlspine-level-experiment.md`). Projected boxes by level: T11 3, T12 63, L1 265, L2 296, L3 296, L4 296,
  L5 296, sacrum 292 (`docs/DATASHEET.md` §2.3, from `realxray/carmlspine/summary.json`).
- Field 200.8 mm at the object plane on every spot frame (`SchwingNet/results/coverage/COVERAGE.md`,
  `carmlspine_headers_spot`).

*[E]*

intraoperative C-arm XA frames, a CBCT per case, and raw cone-beam sweeps. The device is the FIRST/Yiying Surgio-B51 (`RSNAI_DATA_MANIFEST.json`).

**Position/view**

*[C]*

- Per case one AP (PositionerPrimaryAngle 0) and one lateral (90). case39 carries a second lateral 25 s after the
  first at the same 89 kV. case118's second frame is an **oblique at -58.1 deg**. case134's AP (0.0 deg, 77 kVp)
  and lateral (90.0 deg, 89 kVp) sit inside `case134/CBCT/` (`docs/DATA_COMPLETENESS_AUDIT.md` lines 869-872 and 882, and
  Repairs 2026-09-23).
- Header view classes over the 299 spot frames: AP 149, LAT 148, LAT2 1, OBL 1; tilt -0.6 to 0.9 deg; roll 0 (no
  roll tag in any header) (`SchwingNet/results/coverage/COVERAGE.md`, `carmlspine_headers_spot`).
- Registered poses (296): lateral angle -94.5 to 1.9 deg, tilt -6.4 to 4.5 deg, roll -1.8 to 3.7 deg
  (`SchwingNet/results/coverage/COVERAGE.md`, `carmlspine_registered`).
- Raw sweeps: 2 x 301 projections, PositionerPrimaryAngle about +122 to -52 deg in 58 quantised readings, 111 kV
  (`docs/DATA_COMPLETENESS_AUDIT.md` section at line 350; `SchwingNet/results/coverage/COVERAGE.md`,
  `carmlspine_headers_spin`).
- Patient position (prone/supine): `PatientPosition` is "present only in C-ArmLSpine headers (and on a subset of
  them)"; its value is not recorded in any document read (`SchwingNet/results/coverage/COVERAGE.md` §D).
- Living patients or cadavers: unknown. "All 149 cases fall on five days ~4 min apart with no instrumentation
  ('routine intraoperative' is doubtful; living vs cadaver unknown)" (`docs/HANDOFF_2026-09-21_PM.md` lines 448-450).

*[E]*

spot frames: AP 149, lateral 149, oblique 1 (`corpus_census.md` 1). Per-frame poses come from registration (`DATASHEET.md` 3).

**Licence and access**

*[C]*

- **open**, CC BY 4.0 (`docs/RSNAI_DATA_MANIFEST.json` `roots.carmlspine.licence`; `slurm/carmlspine_fetch.sh`).
  CC BY allows derived labels and their redistribution with attribution.
- Click-free public release, inside the scope of WSU determination 2026-269 (`SchwingNet/results/g0_facts.md` §3).
- Privacy caution: `case134/ori/` and case134's CBCT still carry a real PatientID and name in their headers. Export
  tools must check every written file against those strings and never print them
  (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs 2026-09-23, "Anonymisation"; `docs/PATIENT_IDENTITY_SPEC.md` alias 16).
  No record shows that the dataset authors were told (`SchwingNet/results/g0_facts.md` §3, placeholder B).

*[E]*

CC BY 4.0, open (`RSNAI_DATA_MANIFEST.json`).

**How it was acquired**

*[C]*

- `slurm/carmlspine_fetch.sh` (reqp/requeue, compute node): `curl -sSL -C - -o C-ArmLSpine.zip
  "https://zenodo.org/records/22768651/files/C-ArmLSpine.zip?download=1"`; MD5 compared with
  `6bccd47979a2a1c9b200dc427fefeb54`, and `C-ArmLSpine.zip.ok` written on a match; `unzip -q -o` into `unpacked/`;
  then `tools/inspect_dicom_tree.py --root unpacked --cases 6 --out inspect.json` (`slurm/carmlspine_fetch.sh`).
- Route: Zenodo over HTTP. Verification: MD5 of the zip (`slurm/carmlspine_fetch.sh`). The unpacked tree is
  hashed as a file list in `docs/RSNAI_DATA_MANIFEST.json` (`list_sha256` 1e87cd76...a6e7).
- The audit quotes the Zenodo MD5 as `6bccd47979a2a1c9b200dc427fefeb5` (31 characters, a transcription cut) and
  records the zip as "MD5 verified" (`docs/DATA_COMPLETENESS_AUDIT.md` lines 703 and 710).

*[E]*

`curl -C -` of `https://zenodo.org/records/22768651/files/C-ArmLSpine.zip?download=1`, then an md5 check against `6bccd47979a2a1c9b200dc427fefeb54` (`nnunet:slurm/carmlspine_fetch.sh`).

**When**

*[C]*

- Found and fetch started 2026-09-21 16:39 (git aca0a60). Zip complete 2026-09-21 17:32, `.ok` written 17:33
  (`SchwingNet/results/g0_facts.md` §2, grid change times).
- Imaging dates inside the release (DICOM StudyDate): 2023-11-11 (1 case), 2023-11-12 (1), 2023-11-18 (38),
  2023-12-11 (66), 2023-12-12 (43) (`SchwingNet/results/carmlspine_day_groups.json`).
- Ceph directory `data/carmlspine` dated 2026-09-24 (`LISTING`).

*[E]*

the script was first committed 2026-09-21 (git log). The Ceph folder is dated 2026-09-24 in the listing.

**What it contains**

*[C]*

- Zip 15,581,614,253 bytes; 149 case folders (`docs/DATA_COMPLETENESS_AUDIT.md` line 710).
- Unpacked: 59,609 files, 23,347,039,978 bytes; extensions `.dcm` 58,911 plus numbered stubs
  (`docs/RSNAI_DATA_MANIFEST.json` `roots.carmlspine`).
- 58,706 CT slices (149 CBCTs x 394), 901 XA files and 2 non-DICOM stubs; folders `CBCT` 59,010, `C-arm` 297,
  `ori` 302 (`docs/DATA_COMPLETENESS_AUDIT.md` line 704, from `CEPH .../data/carmlspine/catalogue.json`).
- The 901 XA files are 297 spot frames in `C-arm/`, 2 spot frames in `case134/CBCT/`, 301 sweep projections in
  `case134/ori/` and 301 in `case39/CBCT/` (`SchwingNet/results/repairs/carm-cases_CHECK.md` §3). That is **299
  spot frames** and **602 sweep projections** (`SchwingNet/NUMBERS.md` line 295).
- case39's CBCT is reconstructed from its own sweep (`docs/DATA_COMPLETENESS_AUDIT.md` line 871).
- The spot frames are processed display images; the raw sweeps carry a second near-raw frame in private tag
  (0037,0020) (`docs/HANDOFF_2026-09-21_PM.md` lines 448-451).
- Ceph usage 81 GB on 2026-09-25, including derived products (`docs/CENSUS_TABLE_2026-09-25.md` §4).

*[E]*

149 cases. The zip is 15,581,614,253 B and unpacks to 59,609 files and 23,347,039,978 B (`DATA_COMPLETENESS_AUDIT.md` line 710; `RSNAI_DATA_MANIFEST.json`). The Ceph folder is 81 GB (`CENSUS_TABLE_2026-09-25.md` 4).

**Where it is now**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/carmlspine/C-ArmLSpine.zip` and `C-ArmLSpine.zip.ok`. Raw
  (`slurm/carmlspine_fetch.sh`; `docs/DATA_COMPLETENESS_AUDIT.md` line 710).
- CEPH `/rs/rs_grp_oschome/go2432/data/carmlspine/unpacked/C-ArmLSpine/`. Raw, unpacked
  (`docs/RSNAI_DATA_MANIFEST.json`).
- CEPH `/rs/rs_grp_oschome/go2432/data/carmlspine/{catalogue.json, release_census.tsv, tags_case1.txt, inspect.json,
  headers_dossier.json}`. Header inventories (`docs/DATA_COMPLETENESS_AUDIT.md` lines 704 and 710;
  `docs/DATASHEET.md` §2.4; `SchwingNet/results/repairs/carm-cases_CHECK.md` §3).
- CEPH `/rs/rs_grp_oschome/go2432/data/carmlspine/{nifti, ts, ts_s1, spineps, spineps_retry134, levels.json,
  levels_pre_repair_2026-09-23.json, cases.csv, compare.csv, compare_veridah2.csv}`. Converted CBCTs and derived
  labels (`docs/DATA_COMPLETENESS_AUDIT.md` line 718; `SchwingNet/results/repairs/carm-cases_CHECK.md` §2).
- CEPH `/rs/rs_grp_oschome/go2432/data/carmlspine/pose/` (913 files: 457 `.json`, 456 `.png`) and `pose_150/`.
  Derived (`docs/RSNAI_DATA_MANIFEST.json` `roots.carmlspine_pose`; repo path references). The repair moves stale
  case118 poses to `pose/retired/` (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs 2026-09-23).
- CEPH `/rs/rs_grp_oschome/go2432/data/carmlspine/{qc, proto, proto_post, proto_v9, proto_v9init,
  proto_v9init_prerepair, proto_post_v9init, proto_post_v9init_prerepair, sweep, sweep_case39, dossier_look}`.
  Derived analysis output (path references across `docs/`, `tools/`, `slurm/`, `SchwingNet/results`).
- HOME `/wsu/home/go/go24/go2432/idcensus_carmlspine.json`, `verify_carm.json`, `carm_*.py`, `case134.py`. Loose
  analysis files in the home root (`LISTING` lines 386-420, 681, 1220-1222).
- Frame banks and render banks: see Derived products and the `carm_drr` card.

*[E]*

`~/carm_base_cache` (HOME, converted/derived, listing 2026-09-21); `~/carm_base_cache_v9` (HOME, converted/derived, listing 2026-09-23); `~/carm_cv0_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_cv1_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_cv2_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_cv3_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_cv4_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_cvday0_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_cvday1_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_cvday2_drr` (HOME, converted/derived, listing 2026-09-23); `~/carm_drr` (HOME, converted/derived, listing 2026-09-21); `$RS/data/carmlspine` (CEPH, raw, 81.0 GB, listing 2026-09-24); `$RS/data/outline_conv` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/rare_class` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/realxray` (CEPH, converted/derived, 3.9 GB, listing 2026-09-26); `$RS/data/carmlspine/unpacked/C-ArmLSpine` (CEPH, raw, 23.4 GB); `$RS/data/carmlspine/pose` (CEPH, converted/derived, 0.2 GB)

**Annotation status**

*[C]*

- Release labels: none found. The release census lists only CT and XA objects (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 704). No pose ships; poses were computed by 2-D/3-D registration (`docs/DATASHEET.md` §3).
- Project labels: **two-labeller, automatic** (TotalSegmentator and SPINEPS+VERIDAH on each CBCT; a level is used
  only where they agree). Pre-repair `levels.json` summary: 148 cases, 910 vertebrae compared, 814 agree (89.5 %),
  41 name disagreements, 55 unmatched, 3 SPINEPS missing, 22 variant-flagged cases (`docs/DATASHEET.md` §2.3).
  Rebuilt over 149 cases on 2026-09-23 (job 40416616, `CARMLVL_DONE levels_cases 149`)
  (`SchwingNet/results/repairs/carm-cases_CHECK.md` §1).
- case134: VERIDAH labelled it C1-C5 + sacrum while TotalSegmentator reads L1-L5 + sacrum, so it is a disagree
  record with `level: null` (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs 2026-09-23).
- Three cases carry a VERIDAH L6 (case42, case121, case136), tier "morphology-only"
  (`SchwingNet/results/corpus_census.md` lines 211 and 233; `tools/rare_class_carmlspine_drr.py`).
- **No level truth was established by a human** (`docs/DATASHEET.md` §2.3).
- Per-frame fields in the frame-bank meta: device, kVp, mAs, `px_mm`, view angles, pose K/ext with
  `qc_edge_ncc`/`qc_log_ncc`, and per box `level`, `level_ts`, `level_spineps`, `level_agree`, `visible_frac`,
  `box_source` (`docs/REAL_XRAY_DATASETS_SPEC.md` "Meta" and "Two labellers"; `docs/DATA_COMPLETENESS_AUDIT.md`
  Repairs 2026-09-23).

*[E]*

none released for levels. Poses are registered by this project (`nnunet:tools/carmlspine_pose.py`, 913 files).

**Derived products**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine`: the repaired frame bank, **299 frames** (247/26/26
  under the G3 person split; views AP 149, LAT 149, OBL 1) (`SchwingNet/results/corpus_census.md` lines 31, 79,
  126). Built by `tools/carmlspine_labels.py build` then `finalize` (`docs/DATA_COMPLETENESS_AUDIT.md` line 203).
- CEPH `.../realxray/carmlspine_pre_repair_2026-09-23`: the 296-frame bank behind every published number
  (`SchwingNet/results/corpus_census.md` line 127; `docs/DATA_COMPLETENESS_AUDIT.md` Repairs).
- CEPH `.../realxray/carmlspine_sweep`: 301 projections of case134's sweep, all val; case39's sweep is in no root
  (`SchwingNet/results/corpus_census.md` lines 90 and 128; `SchwingNet/results/corpus_census.json` line 5310).
- CEPH `.../realxray/carmlspine_multi`: derived (the frames plus synthetic crops of the same frames), built by
  `tools/carmlspine_multi_build.py` (`tools/realxray_banks.json`).
- CEPH `/rs/rs_grp_oschome/go2432/data/rare_class/carmlspine_cbct_drr`: 396 held-out DRRs of the three L6 CBCTs
  (`SchwingNet/results/corpus_census.md` line 139; `SchwingNet/slurm/rare_carmlspine_drr.sh`).
- HOME `~/carm_drr`, `~/carm_cv0..4_drr`, `~/carm_cvday0..2_drr`, their `*_fov96_ctx` crop banks,
  `~/carm_mix_fov96_ctx`, `~/carm_base_cache`, `~/carm_base_cache_v9`: see the `carm_drr` card (`LISTING` lines
  386-416).
- CEPH `/rs/rs_grp_oschome/go2432/data/devcorpus/poses/surgio_b51_dr.json`: the Surgio pose pool for the synthetic
  corpus (`SchwingNet/results/coverage/COVERAGE.md`, `carmlspine_registered`; `tools/devcorpus_build.py`).
- Splits: `CEPH .../realxray/carmlspine/splits.json`, sha256 553254cf... on 2026-09-22
  (`docs/RSNAI_DATA_MANIFEST.json` `splits`); acquisition-day groups in `SchwingNet/results/carmlspine_day_groups.json`.
- Cross-validation results: `docs/carmlspine_cv5_mixed_2026-09-21.json` (`docs/DATASHEET.md` §8).

*[E]*

19 entries: `~/carm_cv0_fov96_ctx`, `~/carm_cv1_fov96_ctx`, `~/carm_cv2_fov96_ctx`, `~/carm_cv3_fov96_ctx`, `~/carm_cv4_fov96_ctx`, `~/carm_cvday0_fov96_ctx`, `~/carm_cvday1_fov96_ctx`, `~/carm_cvday2_fov96_ctx`, `~/carm_cvdaymix0_fov96_ctx`, `~/carm_cvdaymix0_v9_fov96_ctx`, `~/carm_cvdaymix1_fov96_ctx`, `~/carm_cvdaymix2_fov96_ctx`, `~/carm_cvmix0_fov96_ctx`, `~/carm_cvmix1_fov96_ctx`, `~/carm_cvmix2_fov96_ctx`, `~/carm_cvmix3_fov96_ctx`, `~/carm_cvmix4_fov96_ctx`, `~/carm_fov96_ctx`, `~/carm_mix_fov96_ctx`

**Known defects and gaps**

*[C]*

- case134 was missing from every published bank because the walker looked only in `C-arm/`; the written reason
  ("ships no AP or lateral frame") was false. Repaired 2026-09-23 (jobs 40416561-40416563, 40416616)
  (`docs/DATA_COMPLETENESS_AUDIT.md` lines 200-203 and Repairs); the repaired bank holds 299 frames
  (`SchwingNet/results/corpus_census.md` line 79). The adversarial check at 03:20 on 2026-09-23 found the rebuild
  not yet run and the four look-renders absent (`SchwingNet/results/repairs/carm-cases_CHECK.md` §§1-2). Whether the
  renders were later looked at is not recorded.
- case118's -58.1 deg oblique was posed and scored as a lateral in every pre-repair number
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 205).
- case39's second lateral was dropped by an uncommented exporter rule; the repaired bank exports it as `case39_LAT2`
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 870 and Repairs).
- The 602 sweep projections are used by no model; open item A24 (`docs/DATA_COMPLETENESS_AUDIT.md` section at line
  350 and Repairs "Not done here").
- Reading traps: one series UID per CBCT slice (read with `tools/carmlspine_io.read_cbct`, never by GDCM series
  grouping); no FrameOfReferenceUID; `PixelSpacing` 1.0 is a placeholder; a third of cases name frames by UID
  (`MEM/carmlspine-level-experiment.md`; `docs/DATASHEET.md` §3).
- A case is an acquisition session, **not provably one person**: `PatientID` is empty on 59,307 of 59,609 files and
  private tag (0029,0016) is console free text (`docs/PATIENT_IDENTITY_SPEC.md` row carmlspine;
  `MEM/identity-audit-findings.md`). `tools/realxray_banks.json` names the acquisition-day group as the person key.
- The pose consensus came from 12 free registrations (AP 6, LAT 6); the LAT winner took 4 of 6 votes and only 2 of 6
  at margin > 0.05 (`SchwingNet/results/repairs/carm-cases_CHECK.md` F1). Median edge NCC 0.370 (AP), 0.207 (LAT);
  whether accuracy tracks pose quality is not measured (`docs/DATASHEET.md` §3).
- The agreement filter removes the thoracolumbar junction (T12 10 % named, T11 0 %) (`docs/DATASHEET.md` §2.3).
- Stale counts (148 cases / 296 frames) remain in `docs/DATASHEET.md` §§2.1, 3, 8 and `docs/RSNAI_TABLE1_DATASETS.md`
  (`docs/DATA_COMPLETENESS_AUDIT.md` lines 727-728).
- No age, sex or patient attribute in any header (`docs/DATASHEET.md` §2.4).

*[E]*

case134 was not built, and case118's oblique frame was exported as a lateral (`DATA_COMPLETENESS_AUDIT.md` lines 200-205). The raw sweeps are unused (line 350).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): --bytes so a rerun does not download 15.6 GB again. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid carmlspine` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[C]*

1. `sbatch slurm/carmlspine_fetch.sh` on a compute node; it resumes with `curl -C -` (`slurm/carmlspine_fetch.sh`).
2. Verify: zip MD5 `6bccd47979a2a1c9b200dc427fefeb54`; 149 case folders; 59,609 files and 23,347,039,978 bytes;
   `python tools/data_manifest.py check` reproduces `list_sha256` 1e87cd76... (`docs/RSNAI_DATA_MANIFEST.json`;
   `tools/data_manifest.py`).
3. Count spot frames by DICOM Modality and Rows, never by folder: 299 spot frames (149 AP, 149 LAT including one
   repeat, 1 OBL) and 602 sweep projections. `tools/carmlspine_frame_census.py` also runs the anonymity check and
   exits non-zero on any identifier hit (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs 2026-09-23).
4. Rebuild the derived products in order: `slurm/carmlspine_nifti.sh`, `slurm/carmlspine_seg.sh` and
   `slurm/carmlspine_seg_s1.sh`, `slurm/spineps_cases.sh`, `tools/dual_seg_compare.py`, `slurm/carmlspine_pose.sh`,
   then `tools/carmlspine_labels.py build` and `finalize` (`docs/REAL_XRAY_DATASETS_SPEC.md` "Two labellers";
   `docs/DATA_COMPLETENESS_AUDIT.md` line 203; script names in `slurm/`). The argument lists of the nifti and seg
   jobs were not read for this card.

*[E]*

`sbatch slurm/carmlspine_fetch.sh`, which verifies the md5.

---

### `carm_drr` <a id="carm_drr"></a>

**carm_drr and fold copies: REAL C-ArmLSpine spot frames in the DRR-bank layout; plus rare_class/carmlspine_cbct_drr.** Cards: C (carm_drr). Structured entry: `sources.yaml` id `carm_drr`; kind derived; status on_disk; re-acquisition submit (rebuild).

**Source id**

`carm_drr` — a derived bank of `carmlspine`, not an independent source (`tools/carmlspine_to_bank.py`). This card
also covers the cross-validation copies `carm_cv0..4_drr` and `carm_cvday0..2_drr` and their crop banks, and points
to the one true CBCT render bank, `rare_class/carmlspine_cbct_drr`.

**Name and citation**

- Built by this project from C-ArmLSpine (Zenodo 10.5281/zenodo.22768651) (`tools/carmlspine_to_bank.py` docstring).

**Modality**

- `carm_drr` and `carm_cv*_drr`: **real** intraoperative C-arm spot frames (XA), not renders, stored as
  `img/<stem>.npy` + `ann/<stem>.json` so the level model and its head can be fine-tuned on them
  (`tools/carmlspine_to_bank.py` docstring). The name "drr" is only the layout name.
- `rare_class/carmlspine_cbct_drr`: **synthetic render** (DRRs) of three real CBCTs (case42, case121, case136) under
  the registered Surgio poses plus a synthetic AP-to-lateral arc, styled through every fitted device card, 1024 px at
  0.30 mm rendered pitch (`tools/rare_class_carmlspine_drr.py` docstring).
- Lumbar spine and sacrum, as in `carmlspine` (`MEM/carmlspine-level-experiment.md`).

**Position/view**

- `carm_drr`: the AP and LAT frame of each case; the source field is `carm_AP` or `carm_LAT` so the bank reports
  per view (`tools/carmlspine_to_bank.py` docstring; `--views AP,LAT`).
- `carmlspine_cbct_drr`: the case's own registered AP and LAT poses plus a synthetic arc about the AP anchor
  (`tools/rare_class_carmlspine_drr.py` docstring).

**Licence and access**

- Derived from CC BY 4.0 data (`docs/RSNAI_DATA_MANIFEST.json` `roots.carmlspine`); not distributed
  (`docs/DATASHEET.md` §6).

**How it was acquired**

- `carm_drr`: `slurm/carmlspine_finetune.sh` runs `rm -rf $HOME/carm_drr; tools/carmlspine_to_bank.py --out
  $HOME/carm_drr`, then `tools/make_context_crops.py --drr $HOME/carm_drr --dst $HOME/carm_fov96_ctx --mode fov
  --tgt-px 96 --size 320 --rungs 1 --val-frac 0.2` (`slurm/carmlspine_finetune.sh` lines 23-24). The reader default
  is `--data /rs/rs_grp_oschome/go2432/data/realxray/carmlspine` (`tools/carmlspine_to_bank.py`).
- `carm_cv<K>_drr`: `slurm/carmlspine_cv.sh` with `--fold K --n-folds NF` (md5(case) % n-folds; the test fold is
  never written) (`slurm/carmlspine_cv.sh` lines 24-26; `tools/carmlspine_to_bank.py`).
- `carm_cvday<K>_drr`: `slurm/carmlspine_cv_day.sh` and `slurm/carmlspine_cv_day_v9.sh` with `--groups-file` (the
  acquisition-day groups) and `tools/merge_banks.py` into `carm_cvdaymix<K>_fov96_ctx` against `allspine_v7`
  (`slurm/carmlspine_cv_day.sh` lines 34-38).
- `carmlspine_cbct_drr`: `SchwingNet/slurm/rare_carmlspine_drr.sh` (array 0-2) runs
  `tools/rare_class_carmlspine_drr.py --case <case>` (`SchwingNet/slurm/rare_carmlspine_drr.sh`).
- Verification: none beyond the builders' own counts (no hash recorded for these banks in
  `docs/RSNAI_DATA_MANIFEST.json`).

**When**

- `carm_drr` exporter first committed 2026-09-21 (git ebe51eb); `~/carm_drr` dated 2026-09-21; the `carm_cv*_drr`
  copies dated 2026-09-23; the `*_fov96_ctx` crop banks 2026-09-21 to 2026-09-23 (`LISTING` lines 386-416).
- `carmlspine_cbct_drr`: rendered by 2026-09-23 (`docs/RESUME_2026-09-22_PM.md` line 1271, "C-ArmLSpine held-out
  396"); `data/rare_class` dated 2026-09-24 (`LISTING`).

**What it contains**

- `~/carm_drr`: 240 anns over 120 cases (`docs/PATIENT_IDENTITY_SPEC.md` row carmlspine;
  `SchwingNet/results/corpus_census.md` line 107), i.e. the train (105 cases) and val (15 cases) frames of the fixed
  case split, 210 + 30 frames (`docs/DATA_COMPLETENESS_AUDIT.md` line 717; `docs/DATASHEET.md` §8). Levels: agreed
  vertebrae plus the sacrum; a box under 90 % inside the frame or cut by the CBCT is marked clipped
  (`tools/carmlspine_to_bank.py` docstring).
- `carm_cv0..4_drr`: 226, 246, 240, 224, 248 entries; `carm_cvday0..2_drr`: 164, 210, 218
  (`SchwingNet/results/corpus_census.md` lines 99-106).
- `carmlspine_cbct_drr`: 396 renders, all held out (`SchwingNet/results/corpus_census.md` line 139); "3 real L6 x 11
  poses x 6 cards" (`docs/RESUME_2026-09-22_PM.md` line 1271). 3 x 11 x 6 = 198, so the factor of two to 396 is not
  explained in the line read.

**Where it is now**

- HOME `/wsu/home/go/go24/go2432/carm_drr`, `carm_cv0_drr` ... `carm_cv4_drr`, `carm_cvday0_drr` ... `carm_cvday2_drr`.
  Derived (`LISTING` lines 386-413).
- HOME crop banks: `carm_fov96_ctx`, `carm_mix_fov96_ctx`, `carm_cv0..4_fov96_ctx`, `carm_cvmix0..4_fov96_ctx`,
  `carm_cvday0..2_fov96_ctx`, `carm_cvdaymix0..2_fov96_ctx`, `carm_cvdaymix0_v9_fov96_ctx`; caches
  `carm_base_cache`, `carm_base_cache_v9`. Derived (`LISTING` lines 386-416).
- CEPH `/rs/rs_grp_oschome/go2432/data/rare_class/carmlspine_cbct_drr/` (`img/` uint8 `.npy`, `ann/` `.json`, every ann
  `held_out: true`). Derived render (`tools/rare_class_carmlspine_drr.py` docstring).

**Annotation status**

- Two-labeller automatic level names inherited from `carmlspine` (`tools/carmlspine_to_bank.py` docstring).
- `carmlspine_cbct_drr`: names from the SPINEPS+VERIDAH instance mask (L6 = VerSe id 25); body boxes with the
  whole-vertebra box kept as `box_whole`; `trunc_frac` recorded per ann (`tools/rare_class_carmlspine_drr.py` docstring).

**Derived products**

- Level-model fine-tunes and cross-validation folds (`slurm/carmlspine_finetune.sh`, `slurm/carmlspine_cv.sh`,
  `slurm/carmlspine_cv_day*.sh`).

**Known defects and gaps**

- Every `carm_*` bank on HOME was built from the pre-repair 296-frame bank (2026-09-21 to 2026-09-23), so case134,
  case39_LAT2 and the case118 view correction are absent from them (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs
  2026-09-23; dates in `LISTING`).
- `carm_drr` and `carm_cv*` must never be pooled: up to 50 people sit on different sides of their splits
  (`docs/PATIENT_IDENTITY_SPEC.md` line 474).
- The patient keyer read `case101` as corpus `case`, person `101` (a degenerate corpus name) until the spec fixed it
  (`docs/PATIENT_IDENTITY_SPEC.md` row carmlspine).
- `docs/CT_INVENTORY.md` labels `carm_drr` "C-ArmLSpine CBCT ... renders"; the builder writes real frames
  (`tools/carmlspine_to_bank.py`).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): only tools/carmlspine_to_bank.py, into the Ceph layout; the GPU fine-tune is dropped. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid carm_drr` prints them. Where the text below differs, `sources.json` is the runnable form.*

- Not downloaded: rebuild from `carmlspine` after its recipe, then `sbatch slurm/carmlspine_finetune.sh`,
  `slurm/carmlspine_cv.sh` (per fold), `slurm/carmlspine_cv_day.sh` (per day group) and
  `SchwingNet/slurm/rare_carmlspine_drr.sh`. Verify entry counts against the numbers above
  (`SchwingNet/results/corpus_census.md` lines 99-107, 139). A rebuild on the repaired bank will not reproduce the
  old counts, by design.

---

### `deepfluoro_h5` <a id="deepfluoro_h5"></a>

**DeepFluoro H5 release (Grupp et al. 2020, IPCAI).** Cards: C (deepfluoro_h5), E (deepfluoro_h5). Structured entry: `sources.yaml` id `deepfluoro_h5`; kind upstream_release; status on_disk; re-acquisition run (dl_deepfluoro).

**Source id**

*[C]*

`deepfluoro_h5` (manifest root name in `docs/RSNAI_DATA_MANIFEST.json`; person key `deepfluoro:<accession>` in
`docs/PATIENT_IDENTITY_SPEC.md`).

*[E]*

`deepfluoro_h5` (family C's id for the registered h5 release; the vendor DICOM deposit is family C's `deepfluoro_vendor`, carded next)

**Name and citation**

*[C]*

- DeepFluoro, Grupp et al. 2020 (IPCAI 2020), "Data and code associated with ... Automatic Annotation of Hip Anatomy
  in Fl[uoroscopy]" (`docs/DATA_COMPLETENESS_AUDIT.md` line 564; `docs/RSNAI_DATA_MANIFEST.json`
  `roots.deepfluoro_h5.source`). Code and README: https://github.com/rg2/DeepFluoroLabeling-IPCAI2020
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 705).
- JHU Data Archive (Dataverse) **doi:10.7281/T1/IFSXNV**; data file persistent ids `EAN9GH`
  (`ipcai_2020_full_res_data.zip`), `RM0YBV` (`ipcai_2020_ds_8x.zip`), `HNV0ZM` (`ipcai_2020_ds_16x.zip`)
  (`tools/dl_deepfluoro.py`; `tools/reg_deepfluoro.py` line 3).
- Paper DOI and Dataverse publication date: not recorded.
- Also appears re-hosted on Hugging Face (card `deepfluoro_xvr_hf`) and as the original vendor files (card
  `deepfluoro_vendor`).

*[E]*

DeepFluoro (Grupp et al., IPCAI 2020). The h5 release is JHU Data Archive doi:10.7281/T1/IFSXNV, and the vendor DICOM deposit is doi:10.7281/T1/C304HZ (`DATA_COMPLETENESS_AUDIT.md` release rows).

**Modality**

*[C]*

- Fluoroscopy (RF/XA class) from a Siemens Cios Fusion C-arm, CsI flat panel, 1536 x 1536 at 0.194 mm, SDD 1020 mm
  (focal -5257.7 px x 0.194 mm), paired with each specimen's CT (`MEM/deepfluoro-convention.md`;
  `docs/RSNAI_DATA_MANIFEST.json`).
- Anatomy: cadaveric pelvis with proximal femora and two to three lumbar levels (the 3-D vertebra class spans
  90-112 mm) (`MEM/deepfluoro-convention.md`).
- Stored image: a log-compressed, transmission-like display image (`tools/realxray_deepfluoro_export.py` docstring;
  `MEM/deepfluoro-convention.md`).

*[E]*

fluoroscopy from a Siemens Cios Fusion, plus CT, from 6 cadaveric pelves (`RSNAI_DATA_MANIFEST.json`).

**Position/view**

*[C]*

- One shipped ground-truth pose per frame (`gt-poses/cam-to-pelvis-vol`). Over the 366 poses: lateral angle -42.1 to
  29.3 deg, tilt -36.1 to 6.5 deg, roll -13.2 to 11.8 deg, magnification 1.1 to 2.1
  (`SchwingNet/results/coverage/COVERAGE.md`, `deepfluoro`).
- `rot-180-for-up` is set on 160 of 366 frames (stored upside down) (`SchwingNet/results/coverage/COVERAGE.md`;
  `docs/DATASHEET.md` §3).
- Specimen position on the table: not recorded; "no PatientPosition in the h5"
  (`SchwingNet/results/coverage/COVERAGE.md` §D).

*[E]*

per-frame C-arm pose for 366 frames.

**Licence and access**

*[C]*

- **open** (anonymous download, but the archive blocks plain curl by TLS fingerprint) (`tools/dl_deepfluoro.py`
  docstring).
- Licence quoted three ways: `docs/DATASHEET.md` says CC BY-NC-SA 4.0; the LICENSE file beside the H5 and the GitHub
  README say **CC BY-NC 4.0** (`docs/DATA_COMPLETENESS_AUDIT.md` lines 732, 865 and 885). Non-commercial either way:
  derived labels may be made and shared non-commercially with attribution; no commercial use.

*[E]*

CC BY-NC-SA 4.0 (`RSNAI_DATA_MANIFEST.json` root deepfluoro_h5).

**How it was acquired**

*[C]*

- `tools/dl_deepfluoro.py [~/deepfluoro/data]`: `curl_cffi.requests.get(BASE + pid, impersonate="chrome",
  stream=True)` for the three files above, streamed to `.part`, renamed when the byte count equals `Content-Length`,
  MD5 printed (not compared with any reference) (`tools/dl_deepfluoro.py`).
- The full-resolution zip was unpacked to `~/deepfluoro/unpacked_full/` (`docs/DATA_COMPLETENESS_AUDIT.md` line 712);
  the unzip command is not recorded.
- A first attempt went through the `diffdrrdata` package (`slurm/deepfluoro_acquire.sh`, which points
  `~/user/diffdrr_data` at `~/deepfluoro/data`); whether that route downloaded anything is not recorded.
- Route: JHU Dataverse over HTTPS with a browser TLS fingerprint. Verification: byte count only
  (`tools/dl_deepfluoro.py`); file-list hash `list_sha256` 2ccfdf83... over the unpacked root
  (`docs/RSNAI_DATA_MANIFEST.json`).

*[E]*

`nnunet:slurm/deepfluoro_acquire.sh`, which installs `diffdrrdata` and uses `nnunet:tools/dl_deepfluoro.py`. The release is 6 files, about 3.4 GB, per the Dataverse API (`DATA_COMPLETENESS_AUDIT.md` release row, job 40416362).

**When**

*[C]*

- 2026-09-20: git 057d77a "Acquire DeepFluoro" 18:53; `~/deepfluoro/data/ipcai_2020_ds_16x.zip` 19:25
  (`SchwingNet/results/g0_facts.md` §2). `~/deepfluoro`, `~/deepfluoro_dl.log` and `~/user` dated 2026-09-20
  (`LISTING` lines 480-481, 1181).

*[E]*

the script was first committed 2026-09-20 (git log). The listing dates `~/deepfluoro` 2026-09-20.

**What it contains**

*[C]*

- `ipcai_2020_full_res_data.h5` 2,541,608,861 bytes plus `LICENSE` (2 files, 2,541,609,955 bytes in the manifest root)
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 712; `docs/RSNAI_DATA_MANIFEST.json`). `~/deepfluoro` totals 6.2 GB with the
  zips (`docs/DATA_COMPLETENESS_AUDIT.md` line 712).
- The IFSXNV deposit holds 6 files, about 3.4 GB; three were fetched (`docs/DATA_COMPLETENESS_AUDIT.md` line 564;
  `tools/dl_deepfluoro.py`). Which three were not fetched is not recorded.
- Six cadaveric specimens `17-1882`, `17-1905`, `18-0725`, `18-1109`, `18-2799`, `18-2800`; 366 projections: 111, 24,
  24, 104, 48, 55 frames (`SchwingNet/results/coverage/COVERAGE.md`; `docs/DATASHEET.md` §2.4).
- Per specimen: `vol/pixels` HU float32 indexed (z,y,x) at 1 mm isotropic; `vol-seg` 7 classes (left/right
  hemipelvis, one merged vertebra class, upper sacrum, left/right femur, lower sacrum); `vol-landmarks` 14 pelvic
  points; per projection `image/pixels` 1536 x 1536 float32, `gt-seg`, `gt-landmarks`, `gt-poses`, `rot-180-for-up`;
  plus `proj-params` (`MEM/deepfluoro-convention.md`).
- The 8x package is another layout: per specimen `projs/segs/lands` at 180 x 180, no CT, no poses; specimens named
  `01`-`06` and crosswalked 01=17-1882, 02=18-1109, 03=18-0725, 04=18-2799, 05=18-2800, 06=17-1905
  (`MEM/deepfluoro-convention.md`; `docs/PATIENT_IDENTITY_SPEC.md` row deepfluoro).

*[E]*

`ipcai_2020_full_res_data.h5` of 2,541,609,955 B, plus a LICENSE file and the `data/` zips. `~/deepfluoro` as a whole is 6.2 GB (`RSNAI_DATA_MANIFEST.json`; `DATA_COMPLETENESS_AUDIT.md` line 712).

**Where it is now**

*[C]*

- HOME `/wsu/home/go/go24/go2432/deepfluoro/unpacked_full/ipcai_2020_full_res_data.h5` + `LICENSE`. Raw, unpacked
  (`docs/RSNAI_DATA_MANIFEST.json`).
- HOME `/wsu/home/go/go24/go2432/deepfluoro/data/` (the three zips). Raw (`tools/dl_deepfluoro.py`;
  `docs/DATA_COMPLETENESS_AUDIT.md` line 712).
- HOME `/wsu/home/go/go24/go2432/deepfluoro/cache`, `/wsu/home/go/go24/go2432/user/diffdrr_data` (a symlink to
  `~/deepfluoro/data`) (`slurm/deepfluoro_acquire.sh`).
- HOME loose files: `deepfluoro_dl.log`, `deepfluoro_look.png`, `dl_deepfluoro.py`, `df_*.py`/`.sh`/`.json`
  (`LISTING` lines 480-516, 540).

*[E]*

`~/deepfluoro` (HOME, raw, 6.2 GB, listing 2026-09-20); `$RS/data/realxray` (CEPH, converted/derived, 3.9 GB, listing 2026-09-26); `$RS/data/realxray_work` (CEPH, converted/derived, listing 2026-09-21); `~/deepfluoro/unpacked_full` (HOME, raw, 2.5 GB)

**Annotation status**

*[C]*

- **Release labels**: 3-D segmentation (7 classes, one merged vertebra class), 14 pelvic landmarks in 3-D and 2-D,
  2-D segmentation per frame, ground-truth pose per frame (`MEM/deepfluoro-convention.md`).
- **Project two-labeller** per-vertebra boxes: TotalSegmentator and SPINEPS+VERIDAH on each specimen's CT,
  projected through the shipped pose; the shipped 2-D sacrum is the independent check (box IoU 0.96 under the
  upper-sacrum rule on 122 frames) (`tools/realxray_deepfluoro_export.py` docstring).

*[E]*

release poses and CT. The project generates landmarks under `realxray/pelvis_landmarks`.

**Derived products**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/realxray/deepfluoro`: 366 frames at 384 x 384, 0.776 mm, builder
  `realxray_deepfluoro_export v1`, 2026-09-21 17:59 (`docs/DATA_COMPLETENESS_AUDIT.md` line 720); split by specimen
  4/1/1 = 238/24/104 frames with 18-1109 as test (`docs/DATA_COMPLETENESS_AUDIT.md` line 720; `docs/DATASHEET.md`
  §8). The G3 person split instead gives 231/111/24 (17-1882 val, 17-1905 test)
  (`SchwingNet/results/corpus_census.md` line 90).
- CEPH `.../data/realxray_work/deepfluoro`: export work directory (`docs/DATA_COMPLETENESS_AUDIT.md` line 720).
- CEPH `.../data/realxray/pelvis_landmarks/deepfluoro`: 342 items (`SchwingNet/results/corpus_census.md` line 97).
- HOME `~/model_night/deepfluoro/pairs/`: 366 (DRR, real, seg) triples, the fitting set for the image-formation
  model (`MEM/deepfluoro-convention.md`; `slurm/deepfluoro_pairs.sh`).
- `docs/devices/cios_fusion.json`, `cios_fusion.3free.json`, `cios_fusion.frames.csv`: the fitted device card
  (`docs/devices/` listing; `docs/RSNAI_TABLE1_DATASETS.md` footer).
- CEPH `.../data/devcorpus/poses/cios_fusion.json`: 366 shipped poses as a pose pool
  (`SchwingNet/results/coverage/COVERAGE.md`, `deepfluoro`).
- PolyPose runs and identity check against the HF copy: `CEPH .../data/polypose/report/hf_vs_h5.json`
  (`slurm/polypose_identity.sh`).

*[E]*

1 entries: `~/reg`

**Known defects and gaps**

*[C]*

- 160 of 366 frames stored upside down; the convention (`ext @ inv(T)`, negative focal kept, rot-180 not applied to
  landmarks) was settled by 0.00 px reprojection (`MEM/deepfluoro-convention.md`; `docs/DATASHEET.md` §3).
- Real frames enter the banks at 384 x 384 (x4 bilinear downsample), the only real corpus not at 1024; written as a
  modelling choice in the exporter, without a reason (`docs/DATA_COMPLETENESS_AUDIT.md` Unknown section, line 429).
- The DOI swap with the vendor deposit in three documents (`docs/DATA_COMPLETENESS_AUDIT.md` line 600).
- `docs/DATA_ACCOUNTING.md` §0 says the vendor deposit holds "the same 366 frames"; it holds 2,659 fluoroscopic
  images plus 19 CTs (`docs/DATA_COMPLETENESS_AUDIT.md` line 730).
- No age or sex (`docs/DATASHEET.md` §2.4).

*[E]*

366 frames over only 6 specimens, so splitting by frame leaks patients (`DATA_ACCOUNTING.md` 4). See also `mem:deepfluoro-convention`.

**Re-acquisition recipe**

*[C]*

1. On a compute node with `curl_cffi`: `python tools/dl_deepfluoro.py ~/deepfluoro/data` (resumable only by skipping
   files already non-empty) (`tools/dl_deepfluoro.py`).
2. `unzip ~/deepfluoro/data/ipcai_2020_full_res_data.zip -d ~/deepfluoro/unpacked_full` (the original command is not
   recorded; this one is the obvious equivalent).
3. Verify: h5 2,541,608,861 bytes; root `list_sha256` 2ccfdf83... via `python tools/data_manifest.py check`
   (`docs/RSNAI_DATA_MANIFEST.json`); six specimens, 366 projections; reprojection 0.00 px with
   `tools/deepfluoro_convention.py` (`MEM/deepfluoro-convention.md`).
4. For the other three files of IFSXNV, run `python tools/jhu_dataverse_info.py doi:10.7281/T1/IFSXNV` to list them
   and `python tools/jhu_dataverse_fetch.py doi:10.7281/T1/IFSXNV <out>` to fetch all
   (`tools/jhu_dataverse_info.py`; `tools/jhu_dataverse_fetch.py`).

*[E]*

`sbatch slurm/deepfluoro_acquire.sh`, then check the h5's byte size against 2,541,609,955 B.

---

### `deepfluoro_vendor` <a id="deepfluoro_vendor"></a>

**DeepFluoro original vendor DICOMs (Grupp, Unberath, Gao et al., cadaveric PAO experiments).** Cards: C (deepfluoro_vendor), E (deepfluoro_vendor). Structured entry: `sources.yaml` id `deepfluoro_vendor`; kind upstream_release; status on_disk; re-acquisition run (jhu_dataverse).

**Source id**

*[C]*

`deepfluoro_vendor` (manifest root name, `docs/RSNAI_DATA_MANIFEST.json`).

*[E]*

`deepfluoro_vendor` (family C's id)

**Name and citation**

*[C]*

- Grupp, Unberath, Gao et al., "X-ray computed tomography and fluoroscopy collected during cadaveric periacetabular
  osteotomy experiments", JHU Data Archive **doi:10.7281/T1/C304HZ**, released 2022-03-30, version 1
  (`docs/HANDOFF_2026-09-21_PM.md` lines 268-271; `docs/DATA_COMPLETENESS_AUDIT.md` line 706).

*[E]*

DeepFluoro original vendor DICOMs, JHU Data Archive doi:10.7281/T1/C304HZ, "X-ray computed tomography and fluoroscopy collected during cadaveric peri…" (`DATA_COMPLETENESS_AUDIT.md` release row)

**Modality**

*[C]*

- Original vendor DICOMs: 19 CT scans (pre- and post-operative, six cadavers) and 2,659 fluoroscopic images (Siemens
  Cios Fusion), plus a sawbones pelvis and the FTRAC fiducial (`slurm/deepfluoro_vendor_fetch.sh` header;
  `docs/HANDOFF_2026-09-21_PM.md` lines 268-272).
- Same specimens as `deepfluoro_h5`; about seven times the 366 registered frames (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 730).
- Anatomy: cadaveric pelvis (periacetabular osteotomy experiments) (`docs/HANDOFF_2026-09-21_PM.md` line 269).

*[E]*

fluoroscopy (vendor DICOM, Siemens Cios Fusion) and CT of the same 6 cadaveric pelves (`RSNAI_DATA_MANIFEST.json` root deepfluoro_vendor)

**Position/view**

*[C]*

- Not recorded per frame in any document read. The deposit's `02_fluoroscopy_rotations.tab` is the per-frame
  rotation table (2,659 rows expected) (`docs/DATA_COMPLETENESS_AUDIT.md` lines 170-173, 210-213). Only the 366
  frames in the H5 carry a released pose (`docs/DATA_COMPLETENESS_AUDIT.md` line 873).

*[E]*

the vendor headers of the same frames (`RSNAI_DATA_MANIFEST.json`); rotation runs in `02_fluoroscopy_rotations.tab` (`DATA_COMPLETENESS_AUDIT.md` line 210)

**Licence and access**

*[C]*

- **open**, unrestricted on the Dataverse listing, **CC BY-NC 4.0** (`docs/HANDOFF_2026-09-21_PM.md` line 270); the
  cadaver README inside the deposit says CC BY-NC-SA 4.0 (`docs/DATA_COMPLETENESS_AUDIT.md` line 885). Non-commercial
  either way.
- `tools/data_manifest.py` records "see LICENSE in archive" and the wrong DOI (`tools/data_manifest.py` `ROOTS`).

*[E]*

CC BY-NC 4.0, published 2022-03-30 v1 (`DATA_COMPLETENESS_AUDIT.md` release row)

**How it was acquired**

*[C]*

- Listing: `tools/jhu_dataverse_info.py doi:10.7281/T1/C304HZ` (via `slurm/jhu_dataverse_info.sh`), log
  `~/model_night/logs/jhudv_40409948.out` (`docs/DATA_COMPLETENESS_AUDIT.md` line 706).
- Fetch: `sbatch slurm/deepfluoro_vendor_fetch.sh` runs `tools/jhu_dataverse_fetch.py doi:10.7281/T1/C304HZ
  /rs/rs_grp_oschome/go2432/data/deepfluoro_vendor`: Dataverse API listing, unrestricted files only, smallest first,
  `curl_cffi` with `impersonate="chrome"`, written through a callback to `.part` with HTTP Range resume, renamed when
  the byte count equals the deposit's `filesize` (`slurm/deepfluoro_vendor_fetch.sh`; `tools/jhu_dataverse_fetch.py`).
- Unpack: `sbatch slurm/deepfluoro_vendor_unpack.sh` joins split `.zip.NNN` volumes by `cat` into `joined/`, extracts
  each archive with Python `zipfile` into `unpacked/<archive>/`, writes `.DONE` per archive and removes the joined
  copy (`slurm/deepfluoro_vendor_unpack.sh`).
- Verification: byte count against the deposit listing; no checksum compared (`tools/jhu_dataverse_fetch.py`).

*[E]*

`sbatch slurm/deepfluoro_vendor_fetch.sh`, which runs `tools/jhu_dataverse_fetch.py doi:10.7281/T1/C304HZ $RS/data/deepfluoro_vendor` through curl_cffi (`nnunet:slurm/deepfluoro_vendor_fetch.sh`). The first attempt (40409951) was OOM-killed; job 40411582 listed all 19 files (`DATA_COMPLETENESS_AUDIT.md` line 579)

**When**

*[C]*

- Deposit read through the API 2026-09-21 16:55 EDT (`docs/HANDOFF_2026-09-21_PM.md` line 268). First fetch job
  40409951 was OOM-killed at 4 GB with nothing on disk; the callback fix is git d01b17f, 2026-09-22
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 713; git log of `tools/jhu_dataverse_fetch.py`).
- Files landed 2026-09-22 01:23-01:35 (job 40411582, `DFVENDOR_DONE`) (`docs/DATA_COMPLETENESS_AUDIT.md` Unknown
  section line 428 and line 579; `SchwingNet/results/g0_facts.md` §2). Unpack script committed 2026-09-22 (git 9a8aeb1).

*[E]*

script first committed 2026-09-21 (git log); the listing dates `$RS/data/deepfluoro_vendor` 2026-09-22

**What it contains**

*[C]*

- Deposit: 19 files, 38.3 GB (`docs/DATA_COMPLETENESS_AUDIT.md` line 706); 37,381,313 KB of zips on disk
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 713).
- Unpacked: 94,626 files, 72,708,547,975 bytes (91,375 without extension, 3,243 `.jpg`, 8 `.txt`)
  (`docs/RSNAI_DATA_MANIFEST.json` `roots.deepfluoro_vendor`).
- Fluoroscopy DICOMs: 2,545 cadaver + 36 FTRAC + 78 sawbones (`docs/DATA_COMPLETENESS_AUDIT.md` line 873); the
  2,545 cadaver files hold 1,344 image frames, 6 files being multi-frame video (`docs/PATIENT_IDENTITY_SPEC.md` row
  deepfluoro). `09_ftrac_fiducial` holds a CT and 72 fluoroscopy files (`docs/DATA_COMPLETENESS_AUDIT.md` Unknown
  section line 430). 21 vendor CT series folders (pre-op, bb-injected, post-op) (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 887). The file counts add up to the deposit's figure (2,545 + 36 + 78 = 2,659). Two things do not reconcile on
  record: how 2,545 cadaver files relate to "1,344 image frames", and the CT count (19 scans on the listing, 21 CT
  series folders, "17 cadaver CT sessions" in `docs/DATA_COMPLETENESS_AUDIT.md` line 873).
- Ceph usage "DeepFluoro 104" GB on 2026-09-25 (`docs/CENSUS_TABLE_2026-09-25.md` §4).

*[E]*

19 deposit files of 38.3 GB plus `joined/` and `unpacked/` (94,626 files, 72,708,547,975 B) (`RSNAI_DATA_MANIFEST.json`; `DATA_COMPLETENESS_AUDIT.md` line 713); 104 GB for the folder (`CENSUS_TABLE_2026-09-25.md` 4)

**Where it is now**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/deepfluoro_vendor/` (the 19 deposit files), `joined/`, `unpacked/` (e.g.
  `unpacked/03_cadaver_17-1882/cadaver_17-1882/README.txt`). Raw and unpacked (`docs/DATA_COMPLETENESS_AUDIT.md` lines
  579, 713, 865; `docs/RSNAI_DATA_MANIFEST.json`). Directory dated 2026-09-22 (`LISTING`).
- `02_fluoroscopy_rotations.tab.part` (18,345 bytes) in the same directory (`docs/DATA_COMPLETENESS_AUDIT.md` line 173).

*[E]*

`$RS/data/deepfluoro_vendor` (CEPH, raw, 104.0 GB, listing 2026-09-22); `$RS/data/deepfluoro_vendor/unpacked` (CEPH, raw, 72.7 GB)

**Annotation status**

*[C]*

- **none** used. The deposit ships original images and a rotation table; no labels are recorded
  (`docs/HANDOFF_2026-09-21_PM.md` lines 269-272). The pipeline reads it only for a header census
  (`slurm/device_census.sh` lines 26-27) and the identity audit (`docs/DATA_COMPLETENESS_AUDIT.md` line 593).

*[E]*

none beyond the vendor headers; truth comes from the h5 release

**Derived products**

*[C]*

- Cios Fusion header census (`slurm/device_census.sh` lines 26-27); output location not recorded.
- None in any bank or model (`docs/DATA_COMPLETENESS_AUDIT.md` line 721).

*[E]*

none found in the disk map

**Known defects and gaps**

*[C]*

- `02_fluoroscopy_rotations.tab` kept as `.part`: Dataverse serves tabular files converted (18,345 bytes against
  18,203 listed), so the byte test never passes. Repair: confirm it parses as the 2,659-row table and rename
  (`docs/DATA_COMPLETENESS_AUDIT.md` lines 170-173, 210-213). Whether the rename was done is not recorded.
- DOI swapped with IFSXNV in `docs/DATASHEET.md` §3, `docs/RSNAI_DATA_MANIFEST.json` and `SchwingNet/atlas/dataset.json`
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 600).
- Misdescribed as "vendor DICOM headers of the same frames" (`docs/RSNAI_DATA_MANIFEST.json`
  `roots.deepfluoro_vendor.paired`; `docs/DATA_COMPLETENESS_AUDIT.md` line 730).
- 2,293 of 2,659 vendor frames have no released pose; some carry the FTRAC fiducial and could be posed
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 873).
- The fluoroscopy DICOM `PatientID` is wrong (merges 18-2799 with 18-2800 and splits others); key by specimen
  directory (`MEM/identity-audit-findings.md`; `docs/PATIENT_IDENTITY_SPEC.md` row deepfluoro).
- `09_ftrac_fiducial` and `10_sawbones` are objects, not people; no person key (`docs/PATIENT_IDENTITY_SPEC.md`).

*[E]*

`02_fluoroscopy_rotations.tab` kept as a `.part` file (`DATA_COMPLETENESS_AUDIT.md` lines 170, 210); the manifest and the atlas once attributed these DICOMs to IFSXNV (`DATA_COMPLETENESS_AUDIT.md`, doc disagreements)

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): unpack runs inline in the same job, so the list hash is checked after it. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid deepfluoro_vendor` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[C]*

1. `sbatch slurm/deepfluoro_vendor_fetch.sh` (resumable) then `sbatch slurm/deepfluoro_vendor_unpack.sh`
   (`slurm/deepfluoro_vendor_fetch.sh`; `slurm/deepfluoro_vendor_unpack.sh`).
2. Verify: 19 of 19 files at the deposit's sizes, except the `.tab`, which must be checked by parsing (2,659 rows)
   and renamed; unpacked root 94,626 files and 72,708,547,975 bytes; `python tools/data_manifest.py check` reproduces
   `list_sha256` 6eabba54... (`docs/RSNAI_DATA_MANIFEST.json`; `docs/DATA_COMPLETENESS_AUDIT.md` line 173).
3. Fix the DOI in `tools/data_manifest.py` before rebuilding the manifest (`docs/DATA_COMPLETENESS_AUDIT.md` line 600).

*[E]*

`sbatch slurm/deepfluoro_vendor_fetch.sh`; compare each file's size with the Dataverse listing (19 files)

---

### `deepfluoro_xvr_hf` <a id="deepfluoro_xvr_hf"></a>

**DeepFluoro as re-hosted in Hugging Face eigenvivek/xvr-data (deepfluoro/ subfolder).** Cards: C (deepfluoro_xvr_hf). Structured entry: `sources.yaml` id `deepfluoro_xvr_hf`; kind upstream_release; status on_disk; re-acquisition run (hf_hub).

**Source id**

`deepfluoro_xvr_hf` (proposed here; no id exists in the repo for this copy).

**Name and citation**

- Hugging Face dataset `eigenvivek/xvr-data`, revision `a17273e3eadbd793bd861f3598a80ce4590c1124`, subfolder
  `deepfluoro/` (`slurm/env/polypose.setup_status.json`; `slurm/polypose_setup.sh` line 212). The authors' packaging
  of DeepFluoro for xvr/PolyPose (PolyPose: Gopalakrishnan, Dey, Golland, NeurIPS 2025, MIT code)
  (`slurm/polypose_setup.sh` header; `tools/data_manifest.py` `polypose_bank`).
- The full HF dataset is 4.8 GB, 1,703 files, last modified 2026-08-10, and also re-hosts the Balgrist femur set and
  Ljubljana (searcher pass, no verifier verdict) (`docs/research_datasets_fourth_pass_verified_2026-09-22.json` line 49).

**Modality**

- The same DeepFluoro fluoroscopy and CT, repackaged as `deepfluoro/subjectNN/volume.nii.gz` + `mask.nii.gz` with
  poses (`tools/polypose_hf_vs_h5.py` docstring).

**Position/view**

- Shipped poses; as packaged they put the volume behind the source, and one 180-degree flip
  (`pose_matrix @ diag(-1,-1,1,1)`) reproduces the real frames (NCC 0.705/0.648) (`tools/polypose_apply_pose_flip.py`).

**Licence and access**

- **open** download. Overall CC BY-NC-ND 4.0, the DeepFluoro portion CC BY-NC 4.0 (searcher pass only)
  (`docs/research_datasets_fourth_pass_verified_2026-09-22.json` line 49). Anonymous downloads were rate-limited
  (HTTP 429), so the fetch authenticates (`slurm/polypose_setup.sh` lines 22-26).

**How it was acquired**

- `slurm/polypose_setup.sh`: `hf download eigenvivek/xvr-data --repo-type dataset --include "deepfluoro/*"` into the
  job's `HF_HOME` cache, then a sha256 list of every file to `$PP_ROOT/env/export/xvr_data_deepfluoro.sha256`
  (`slurm/polypose_setup.sh` lines 212-220). `PP_ROOT` is `/rs/rs_grp_oschome/go2432/data/polypose`
  (`slurm/polypose_identity.sh` line 13).
- Verification: sha256 list written at download (`slurm/polypose_setup.sh` line 219).

**When**

- Setup run completed 2026-09-23 13:42 (`slurm/env/polypose.setup_status.json` `date`).

**What it contains**

- Six subjects, `subject01`..`subject06` (`tools/polypose_reproduction_report.py` line 131; `slurm/polypose_setup.sh`
  line 213). File count and bytes on disk: not recorded locally (printed by the job).

**Where it is now**

- CEPH `/rs/rs_grp_oschome/go2432/data/polypose/hf/hub/datasets--eigenvivek--xvr-data/snapshots/<rev>/deepfluoro/`
  (`slurm/polypose_identity.sh` line 17). Raw (a third copy of DeepFluoro).

**Annotation status**

- Release labels as packaged (masks, poses) (`tools/polypose_hf_vs_h5.py` docstring).

**Derived products**

- PolyPose reproduction and the PolyPose synthetic bank under `CEPH .../data/polypose` (`tools/data_manifest.py`
  `polypose_bank`; `slurm/polypose_*.sh`).

**Known defects and gaps**

- Pose packaging needs the documented flip before rendering (`tools/polypose_apply_pose_flip.py`).
- Whether the HF subjects are byte-identical to our H5 specimens: checked by `slurm/polypose_identity.sh` into
  `report/hf_vs_h5.json`; the result is not recorded in any document read.
- A third copy of one dataset: any split must key by specimen across all three copies
  (`docs/DATA_ACCOUNTING.md` §0, alias class DeepFluoro).

**Re-acquisition recipe**

- `hf download eigenvivek/xvr-data --repo-type dataset --include "deepfluoro/*" --revision
  a17273e3eadbd793bd861f3598a80ce4590c1124` with a token (the script records the revision but does not pass
  `--revision`; adding it pins the copy) (`slurm/polypose_setup.sh`; `slurm/env/polypose.setup_status.json`).
- Verify against `/rs/rs_grp_oschome/go2432/data/polypose/env/export/xvr_data_deepfluoro.sha256`
  (`slurm/polypose_setup.sh` line 219).

---

### `cobra2026` <a id="cobra2026"></a>

**COBRA2026 (Thummerer, Rit, Kamp, Maspero et al.).** Cards: C (cobra2026), E (cobra2026). Structured entry: `sources.yaml` id `cobra2026`; kind upstream_release; status on_disk; re-acquisition submit (cobra_fetch).

**Source id**

*[C]*

`cobra2026` (manifest root `docs/RSNAI_DATA_MANIFEST.json`; person key `cobra:<case id>` in
`docs/PATIENT_IDENTITY_SPEC.md`). Device banks split by vendor: `cobra_elekta` (centres A-D) and `cobra_varian`
(centres F-G, not built) (`tools/realxray_banks.json`). The planning CTs also feed the CT-screening family (the
LSTV screen); this card covers the projections and the CT as a pair.

*[E]*

`cobra2026` (family C's id)

**Name and citation**

*[C]*

- COBRA2026. Thummerer, Rit, Kamp, Maspero et al., dataset paper arXiv:2607.20037 (submitted 2026-07-22); Zenodo
  DOI 10.5281/zenodo.21322350, v1.0.0, 2026-07-13; challenge page https://cobra2026.grand-challenge.org
  (`docs/research_carm_datasets_verified_2026-09-22.json`, finding "COBRA2026 ... TIER-1").
- Files are served by the CREATIS Girder warehouse, API `https://tomoradio-warehouse.creatis.insa-lyon.fr/api/v1`,
  training folder id `69b93ca75363131190cefb54` (`tools/cobra_fetch.py`).
- Paper PDFs: HOME `~/COBRA_dataset_paper.pdf` (`LISTING` line 97); local
  `<repo CTSpinoPelvic1K 7ddfe38>/COBRA.pdf`, 6,825,932 bytes, 2026-09-21 15:42 (`LOCAL-THIS-SESSION`).

*[E]*

COBRA2026 (Thummerer et al. 2026, arXiv:2607.20037), Zenodo 10.5281/zenodo.21322350, with files on CREATIS Girder (`DATA_COMPLETENESS_AUDIT.md` line 439; `RSNAI_DATA_MANIFEST.json`).

**Modality**

*[C]*

- **CBCT** raw kV projection sweeps from linac-mounted imagers (not mobile C-arms), each with per-projection RTK
  geometry, a planning **CT** deformably registered to the CBCT, the reconstructed CBCTs and FOV masks
  (`docs/research_carm_datasets_verified_2026-09-22.json`; `tools/cobra_fetch.py` docstring).
- Centres A-D: Elekta (Synergy/VersaHD), 504 x 504 at 0.8 mm, 120 kV, 189-734 projections per scan, linear uint16
  signal with the vendor flood field applied. Centres F-G: Varian (Halcyon/TrueBeam/VitalBeam), 1024-3072 x 384-768
  px at 0.28-0.39 x 0.39-1.12 mm, 125-140 kV, 406-895 projections per scan
  (`docs/research_carm_datasets_verified_2026-09-22.json`; `tools/realxray_cobra_export.py` docstring). The exact
  kV-imager model names (XVI generation, OBI version) are not stated by the paper (same JSON).
- Anatomy: living pelvic radiotherapy patients; the planning CTs are pelvic ("Bekken 3mm"), so T12 appears in 0
  projected boxes and L1 in 10 (`docs/DATA_COMPLETENESS_AUDIT.md` line 389).

*[E]*

kV CBCT projection sweeps (Elekta XVI centres A-D, Varian OBI centres F-G) plus planning CT and RTK geometry.

**Position/view**

*[C]*

- Each case is one continuous gantry sweep with a recorded angle per frame
  (`docs/research_carm_datasets_verified_2026-09-22.json`, cross-cutting finding).
- Elekta over 467 cases: trajectory full 460 / half 7; collimator M20 445, S20 17, none 5; SID 1000 mm, SDD 1536 mm;
  frames per case 189-734 (median 444) (`SchwingNet/results/coverage/COVERAGE.md`, `cobra2026_geometry_elekta`).
- Varian: HALF trajectories on 128 cases; anisotropic pixels 0.28 x 1.12 mm on 103 of 225 cases
  (`docs/DATA_COMPLETENESS_AUDIT.md` section at line 285).
- Laterals through a living pelvis are photon-starved (40 ms at 64 mA, no grid) (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 388, quoting `tools/realxray_subset_view.py`).
- Patient position (supine/prone): not recorded; `metadata.yaml` carries no PatientPosition
  (`SchwingNet/results/coverage/COVERAGE.md` §D).

*[E]*

projection sweeps, with geometry per projection.

**Licence and access**

*[C]*

- **open** for the 692-case training split, no registration; **CC BY-NC 4.0** (training permitted, commercial use
  forbidden) (`docs/research_carm_datasets_verified_2026-09-22.json`; `tools/cobra_fetch.py` docstring).
- Validation (52 cases) and test (123 cases) are **embargoed until 2032-03-01** (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 391).

*[E]*

CC BY-NC 4.0, open.

**How it was acquired**

*[C]*

- `tools/cobra_fetch.py` (Python `urllib` against the Girder API; every list call paged with offset/limit 500;
  per-file download to `.part`, renamed when the size equals the catalogued size, four retries)
  (`tools/cobra_fetch.py`).
  - `--list <C>` lists a centre; `--meta-all` fetches `metadata.yaml` for every training case; `--cases <ids>
    --files [names]` fetches named files, all catalogued files when no names follow; `--verify all` checks every
    case on disk against the catalogue and writes `verify.json` and `COBRA_COMPLETE.md` (`tools/cobra_fetch.py`).
- Jobs, in order: pilot cases A004 and A005 on 2026-09-21 (`SchwingNet/results/g0_facts.md` §2; pairs later exist
  for A002, A004, A005, F011, F041 and one more, `docs/DATA_COMPLETENESS_AUDIT.md` line 455); `slurm/realxray_cobra_fetch.sh` with `LIST=cases150.txt` (five
  files per case); `slurm/cobra_fetch_varian.sh` (first N per Varian centre, five files); array 40416154 (40 per
  centre, a display-truncation bug); `slurm/cobra_fetch_all.sh` as job 40416315 (18 tasks, six centres x three
  shards, every file) chained to `slurm/cobra_verify.sh` (`docs/DATASHEET.md` §3; `docs/DATA_COMPLETENESS_AUDIT.md`
  lines 448 and 467; the slurm scripts).
- Verification: every catalogued file present at its catalogued size (`tools/cobra_fetch.py --verify`); no checksum.
  Final: "COBRA IS COMPLETE: 692/692 cases, 771.1 GB, verify exit 0" (job 40417797)
  (`docs/RESUME_2026-09-22_PM.md` line 1281).

*[E]*

`nnunet:tools/cobra_fetch.py` via `nnunet:slurm/cobra_fetch_all.sh`, an 18-task array that takes every file of every one of the 692 public cases into `$RS/data/cobra2026/cases`.

**When**

*[C]*

- First data 2026-09-21: `COBRA2026_Train_overviews` 15:21, pilot cases 15:25, git 59bb679 15:57
  (`SchwingNet/results/g0_facts.md` §2).
- Pre-analysis set (178 cases) on disk by 2026-09-22 23:45 (`docs/DATA_COMPLETENESS_AUDIT.md` line 449).
- Full release verified 2026-09-23, `COBRA_COMPLETE.md` rewritten 15:14 (`docs/RESUME_2026-09-22_PM.md` line 1281);
  git d4eb165 2026-09-23 "All of COBRA2026, every file of every case, verified against the warehouse catalogue".
- Imaging dates: `metadata.yaml` carries `ct.StudyDate` (`docs/PATIENT_IDENTITY_SPEC.md` row cobra); the range is
  not recorded.

*[E]*

the tool was first committed 2026-09-21 and `cobra_fetch_all.sh` on 2026-09-22 (git log). The all-case fetch, job 40416315, was still running at the audit's census (`DATA_COMPLETENESS_AUDIT.md` line 448). The listing dates the folder 2026-09-23.

**What it contains**

*[C]*

- Release: 867 patients / cases in six centres, A 150, B 134, C 150, D 150, F 116, G 167; split 692 train / 52 val /
  123 test; about 950 GB in all, training about 750 GB (`docs/research_carm_datasets_verified_2026-09-22.json`;
  `docs/DATA_COMPLETENESS_AUDIT.md` lines 443 and 446).
- Public training split: A 120, B 107, C 120, D 120, F 92, G 133 = 692 (467 Elekta + 225 Varian)
  (`docs/DATASHEET.md` §3; `docs/DATA_COMPLETENESS_AUDIT.md` line 469).
- 375,618 projections in the 692 training cases (`docs/DATA_COMPLETENESS_AUDIT.md` line 444).
- Per Elekta case, 13 files: `projections.mha`, `projections_simulated.mha`, `geometry.xml`, `ct_original.mha`,
  `ct_def.mha`, `ct_def_masked.mha`, `cbct_clinical.mha`, `cbct_rtk.mha`, FOV masks, `metadata.yaml`,
  `reconstruction.yaml`, an overview PNG; Varian adds `Scan.xml` and `Calibrations/`. No DICOM headers ship
  (`docs/research_carm_datasets_verified_2026-09-22.json`; `docs/DATA_COMPLETENESS_AUDIT.md` lines 265 and 445).
  Case A002: 13 files, 445 MB (`docs/DATA_COMPLETENESS_AUDIT.md` line 445).
- `metadata.yaml` carries age on 347 and sex on 319 of the 692 public cases; centres D, F and G strip them
  (`docs/DATASHEET.md` §2.4).
- On disk: 771.1 GB at verification (`docs/RESUME_2026-09-22_PM.md` line 1281); 754 GB by `du` on 2026-09-25
  (`docs/CENSUS_TABLE_2026-09-25.md` §4). The manifest's "988 files, 42.2 GB" is a mid-fetch snapshot
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 468).

*[E]*

692 `metadata.yaml` files and case directories. The folder was 754 GB on 2026-09-25 (`CENSUS_TABLE_2026-09-25.md` 4).

**Where it is now**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/cobra2026/cases/<case>/`. Raw, every catalogued file of 692 cases
  (`docs/RESUME_2026-09-22_PM.md` line 1281; `tools/cobra_fetch.py`).
- CEPH `/rs/rs_grp_oschome/go2432/data/cobra2026/meta/<case>/metadata.yaml` (692). Raw
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 447).
- CEPH `/rs/rs_grp_oschome/go2432/data/cobra2026/{centre_<C>_cases_full.txt, centre_<C>_cases.txt, cases150.txt,
  verify.json, COBRA_COMPLETE.md, COBRA2026_Train_overviews/}`. Listings and verification
  (`slurm/cobra_fetch_all.sh`; `slurm/cobra_fetch_varian.sh`; `slurm/cobra_verify.sh`; `SchwingNet/results/g0_facts.md`).
- CEPH `/rs/rs_grp_oschome/go2432/data/cobra2026/{seg, pairs, varian/geom, varian/nifti, lstv}`. Derived
  (`docs/DATA_COMPLETENESS_AUDIT.md` lines 451, 455 and Repairs 2026-09-23 Varian;
  `SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md` line 145).
- CEPH `/rs/rs_grp_oschome/go2432/data/spineps/cobra_varian`, `/rs/rs_grp_oschome/go2432/data/spineps/bodies_cobra`.
  Derived (`SchwingNet/results/JOBS_data_repairs.txt` lines 115-123).
- CEPH `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/cobra`. Derived screening output (`LISTING`, dated 2026-09-24).
- CEPH `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta*` and `pelvis_landmarks/cobra_elekta`: see Derived
  products. CEPH `/rs/rs_grp_oschome/go2432/data/or_ready/devices/varian_halcyon/pairs` (`docs/DATA_ACCOUNTING.md`
  alias table).
- HOME `~/rx_cobra_scratch`, `~/_vcobra.py`, `~/_vcobra.out`, `~/cobra2.py`, `~/cobra_ids.py`, `~/cobra_sig.*`,
  `~/cobrapdf.py`, `~/probe_elekta_pair.py`. Loose analysis files (`LISTING` lines 196-197, 443-447, 1014, 1049).
- HOME `~/model_night/logs/cobra_all_*`, `cobra_verify_*`, `cobrafetch_*`, `cobra_varian_*`. Fetch logs (slurm headers).

*[E]*

`~/rx_cobra_scratch` (HOME, converted/derived, listing 2026-09-21); `$RS/data/cobra2026` (CEPH, raw, 754.0 GB, listing 2026-09-23); `$RS/data/realxray` (CEPH, converted/derived, 3.9 GB, listing 2026-09-26); `$RS/data/spineps` (CEPH, converted/derived, listing 2026-09-23); `$RS/data/anomaly_harvest/cobra` (CEPH, converted/derived, listing 2026-09-24); `$RS/data/cobra2026/cases` (CEPH, raw, 42.2 GB)

**Annotation status**

*[C]*

- Release: no anatomical labels; it ships images, geometry, registered CTs and FOV masks
  (`docs/research_carm_datasets_verified_2026-09-22.json`). The authors warn that `ct_def` is not exact ground truth of
  the CBCT anatomy (same JSON).
- Project, Elekta export (150 cases): **two-labeller automatic** (TotalSegmentator + SPINEPS+VERIDAH on `ct_def`),
  agreed level or null per box (`tools/realxray_cobra_export.py` docstring). 14,021 projected boxes; 10,493 dropped for
  `visible_frac` < 0.5 and 3,528 for `incomplete_in_ct` (`docs/DATA_COMPLETENESS_AUDIT.md` line 389).
- Project, all 692 planning CTs: LSTV screen with 38 L6, 45 T13 and 8 four-lumbar calls (91), **unread**
  (`SchwingNet/NUMBERS.md` line 46; `SchwingNet/results/cobra_lstv_screen.md`).
- Pelvis landmarks: 130 of 145 exported cases, 15 excluded by written anatomical gates
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 390).

*[E]*

none for levels. The project made segmentations in `cobra2026/seg` and `anomaly_harvest/cobra`.

**Derived products**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/realxray/cobra_elekta`: 150 case records, 145 ok, 5 excluded (A081, A239,
  A260, A303, B000); 3,480 frames, 24 per case evenly over the orbit; builder v2, 2026-09-22
  (`docs/DATA_COMPLETENESS_AUDIT.md` lines 452 and 473; `tools/realxray_cobra_export.py`). Detector split 110/8/27
  cases = 2,640/192/648 frames; G3 split 2,232/240/840 (hold 168) (`SchwingNet/results/corpus_census.md` lines 82, 261).
- Derived banks: `cobra_elekta_v2` (re-windowed on the body, `tools/realxray_rewindow.py`), `cobra_elekta_ap45` and
  `cobra_elekta_v2_ap45` (symlink views with |angle from AP| <= 45 deg, `tools/realxray_subset_view.py`),
  `cobra_elekta_v3`, `cobra_elekta_smoke` (A004 only), `cobra_elekta_g3test` (`tools/realxray_banks.json`;
  `SchwingNet/results/corpus_census.md` lines 129-134 and 288).
- CEPH `.../realxray/pelvis_landmarks/cobra_elekta`: 3,120 items (`SchwingNet/results/corpus_census.md` line 96).
- `docs/devices/elekta_xvi.json` and `elekta_xvi.frames.csv`: the Elekta device card (`docs/devices/` listing).
- CEPH `.../devcorpus/poses/elekta_xvi.json` and `.../devcorpus_arc/anglesweep/elekta_xvi` (969 renders)
  (`tools/devcorpus_build.py`; `SchwingNet/results/corpus_census.md` line 137).
- Cross-device level-test bins `cobra_ap` / `cobra_obl` / `cobra_lat` (208 / 202 / 2 test frames)
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 459).

*[E]*

none found in the disk map

**Known defects and gaps**

*[C]*

- Only 145 of 692 training cases are in any frame bank; the full release is on disk and not exported
  (`SchwingNet/results/corpus_census.md` line 288; `docs/DATA_COMPLETENESS_AUDIT.md` line 46 and its section at 260).
- Varian (225 cases): the patient-to-RTK axis map was solved on 2026-09-23 (`[[1,0,0],[0,0,-1],[0,-1,0]]`), but
  the exporter still refuses Varian and no `cobra_varian` bank exists (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs
  2026-09-23 Varian; `SchwingNet/results/repairs/varian_CHECK.md`; `tools/realxray_banks.json`).
- B000's exclusion reason: the docs say "41 frames the CT never covers"; the disk says the axis-map gate
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 466). The 0.10 NCC margin of that gate has no stated basis
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 387).
- 24 frames per case is a hard-coded number with no written reason (`docs/DATA_COMPLETENESS_AUDIT.md` lines 421, 473).
- One detector arm (`rx_pooled_1024_init18`) trained on the same patients up to four times through the derived
  banks (5,013 duplicate frames); `tools/realxray_banks.json` now refuses unlisted banks
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 18; `tools/realxray_banks.json` `_README`).
- The Elekta device card was fitted on 40 frames from 3 cases; pairs exist for 6 cases (`docs/DATA_COMPLETENESS_AUDIT.md`
  lines 48 and 461). A claimed `varian_halcyon` card on 525 frames does not exist (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 470).
- 74,364 near-duplicate cross-case frame pairs (different patients at the same gantry angle), 0 same-case pairs
  (`docs/DATASHEET.md` §2.5).
- `cobra_elekta_v2` drops four collimated cases (A025, A181, A212, A299; 96 frames) (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 52). The audit counts v2 at 3,384 frames (line 453); the later census counts it at 3,480
  (`SchwingNet/results/corpus_census.md` line 132). Which is current is not recorded.
- The display window's field was air on Elekta; repaired 2026-09-23 (A31) (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs
  heading at line 1681).
- Stale job id (40416296 against the real 40416315) and stale size in `docs/DATASHEET.md` and
  `SchwingNet/results/JOBS_cobra.txt` (`docs/DATA_COMPLETENESS_AUDIT.md` lines 467-468).
- `docs/HANDOFF_2026-09-21_PM.md` line 607 says "634 Elekta"; the paper gives 584 Elekta over all 867
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 469).
- Four projections files arrived short on first fetch (C045, F037, F038, G029) and are now caught by the size test
  (`tools/cobra_fetch.py` `download`).

*[E]*

the data was counted up to four times in one detector arm, and the Varian cases are unexported (`DATA_COMPLETENESS_AUDIT.md` lines 120, 285).

**Re-acquisition recipe**

*[C]*

1. `python tools/cobra_fetch.py --meta-all` (every training case's `metadata.yaml`) (`tools/cobra_fetch.py`).
2. `sbatch slurm/cobra_fetch_all.sh` (18 tasks; each shard 0 writes `centre_<C>_cases_full.txt` with `--list`, then
   fetches each case with `--cases <id> --files`, every catalogued file) (`slurm/cobra_fetch_all.sh`).
3. `sbatch --dependency=afterany:<array id> slurm/cobra_verify.sh` (`--verify all`, writes `verify.json` and
   `COBRA_COMPLETE.md`, resubmits the fetch once if short) (`slurm/cobra_verify.sh`).
4. Must verify: `COBRA_COMPLETE.md` reads 692 of 692 with every catalogued file at its catalogued size; per-centre
   counts 120/107/120/120/92/133; about 771 GB (`docs/RESUME_2026-09-22_PM.md` line 1281; `docs/DATASHEET.md` §3).
5. Validation and test: manual, not available before 2032-03-01 (`docs/DATA_COMPLETENESS_AUDIT.md` line 391).

*[E]*

`sbatch slurm/cobra_fetch_all.sh`. How the tool verifies files is not stated in the lines Family E read.

---

### `geneva_hip` <a id="geneva_hip"></a>

**Geneva hip 2D-3D registration gold standard (D'Isidoro et al., Med Phys 2021).** Cards: C (geneva_hip), E (geneva_hip). Structured entry: `sources.yaml` id `geneva_hip`; kind upstream_release; status on_disk; re-acquisition run (http).

**Source id**

*[C]*

`geneva_hip` (manifest root and bank name, `docs/RSNAI_DATA_MANIFEST.json`; person key `geneva_hip:phantom` in
`docs/PATIENT_IDENTITY_SPEC.md`).

*[E]*

`geneva_hip` (family C's id)

**Name and citation**

*[C]*

- Geneva hip 2D-3D registration gold standard. D'Isidoro, Chenes, Ferguson, Schmid, Medical Physics
  2021;48(10):5991-6006, doi:10.1002/mp.15124 (PMC9290855) (`tools/realxray_geneva_export.py` docstring;
  `docs/research_carm_datasets_verified_2026-09-22.json`).
- Yareta DOI 10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu; archive page
  https://yareta.unige.ch/archives/ed4bb43a-eaaa-4e62-8763-bd5803f5cd47; download
  `https://access.yareta.unige.ch/access/metadata/ed4bb43a-eaaa-4e62-8763-bd5803f5cd47/download`
  (`slurm/realxray_geneva_fetch.sh`; `docs/DATA_COMPLETENESS_AUDIT.md` line 707).

*[E]*

Geneva hip gold standard (D'Isidoro et al. 2021), Yareta 10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu (`RSNAI_DATA_MANIFEST.json`).

**Modality**

*[C]*

- Fluoroscopy (RF/XA class) from a Philips BV Pulsera video-fluoroscopy C-arm with an **image intensifier**,
  1000 x 1000 px, 12-bit, 0.2904 mm, focal 968.1612 mm; paired CT from a Philips Brilliance 64 (431 x 315 x 468 at
  0.78 x 0.78 x 1.0 mm, 140 kV); 21 fiducials (`tools/realxray_geneva_export.py` docstring;
  `docs/research_carm_datasets_verified_2026-09-22.json`).
- Anatomy: one resin phantom holding a female pelvis, proximal femurs and the lumbar column
  (`tools/realxray_geneva_export.py` docstring).
- Stored format: TIFF/PNG/CSV/JSON, processed display frames, no DICOM (`docs/research_carm_datasets_verified_2026-09-22.json`).

*[E]*

image-intensifier fluoroscopy from a Philips BV Pulsera, plus CT of a resin phantom.

**Position/view**

*[C]*

- 19 camera views of the one phantom (`p01`...`p25`, 19 present), several kV settings per view, large rotations about
  the vertical axis (`docs/PATIENT_IDENTITY_SPEC.md` row geneva_hip; `docs/research_carm_datasets_verified_2026-09-22.json`).
- kV 62-110 (`tools/realxray_geneva_export.py` docstring); 65-90 at p5-p95 (`docs/RSNAI_TABLE1_DATASETS.md`).
- Gold-standard EPPC pose per view; MoCap pose recorded for comparison (`tools/realxray_geneva_export.py` docstring).
- The export meta records no SDD/SOD (`SchwingNet/results/coverage/COVERAGE.md` §D).

*[E]*

19 gold-standard poses.

**Licence and access**

*[C]*

- **open**, anonymous, no DUA; **CC BY-SA 4.0** on the repository and DataCite. The companion paper's text says CC BY-NC
  4.0, a discrepancy (`docs/research_carm_datasets_verified_2026-09-22.json`).

*[E]*

CC BY-SA 4.0, open.

**How it was acquired**

*[C]*

- `sbatch slurm/realxray_geneva_fetch.sh`: `curl -L --retry 5` of the download URL with headers to `headers.txt`;
  if the size is not 412,867,633 bytes, retry with `curl_cffi` impersonating Chrome; `sha256sum` written to
  `archive.sha256`; `unzip` plus every nested zip into `unpacked/` (`slurm/realxray_geneva_fetch.sh`).
- Route: Yareta over HTTPS. Verification: exact byte size; sha256 recorded (prefix `4ddce9b7`)
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 714). Log `genevafetch_40410023.out`, `GENEVA_FETCH_OK` (same line).

*[E]*

`nnunet:slurm/realxray_geneva_fetch.sh` runs curl, falling back to curl_cffi, and requires the zip to be exactly 412,867,633 B. The zip's sha256 (4ddce9b7…) is recorded in `DATA_COMPLETENESS_AUDIT.md` line 714.

**When**

*[C]*

- `headers.txt` 2026-09-21 16:59, zip 17:00 (`SchwingNet/results/g0_facts.md` §2). Ceph `data/geneva_hip_src` and
  `data/realxray_work` dated 2026-09-21 (`LISTING`).
- Yareta deposit date: not recorded.

*[E]*

the script was first committed 2026-09-21. The listing dates `geneva_hip_src` 2026-09-21.

**What it contains**

*[C]*

- Yareta: "481 Files (394.1 MB)"; zip 412,867,633 bytes (`docs/DATA_COMPLETENESS_AUDIT.md` line 707).
- Unpacked on the grid: 482 files, 666 MB (`docs/DATA_COMPLETENESS_AUDIT.md` line 733).
- 116 fluoroscopic frames over 19 views (`docs/DATASHEET.md` §2.1; `tools/realxray_geneva_export.py` docstring).

*[E]*

116 frames (`corpus_census.md` 2).

**Where it is now**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/geneva_hip_src/geneva_hip_gold_standard.zip`, `headers.txt`, `archive.sha256`,
  `unpacked/`. Raw (`slurm/realxray_geneva_fetch.sh`; `docs/DATA_COMPLETENESS_AUDIT.md` line 714).
- CEPH `/rs/rs_grp_oschome/go2432/data/realxray_work/geneva_hip` (69 files, 105,918,260 bytes: `.npz` 38, `.gz` 17,
  `.json` 6, `.csv` 3, ...). Export work directory, derived (`docs/RSNAI_DATA_MANIFEST.json` `roots.geneva_hip`).
- CEPH `/rs/rs_grp_oschome/go2432/data/realxray/geneva_hip` (116 frames, all test) and
  `.../realxray/pelvis_landmarks/geneva_hip` (116). Derived (`SchwingNet/results/corpus_census.md` lines 98, 136).

*[E]*

`$RS/data/geneva_hip_src` (CEPH, raw, listing 2026-09-21); `$RS/data/realxray` (CEPH, converted/derived, 3.9 GB, listing 2026-09-26); `$RS/data/realxray_work` (CEPH, converted/derived, listing 2026-09-21); `$RS/data/realxray_work/geneva_hip` (CEPH, converted/derived, 0.1 GB)

**Annotation status**

*[C]*

- **Release labels**: gold-standard rigid transforms CT to each view and a calibrated projection matrix (0.033 mm
  reprojection error), fiducials (`docs/research_carm_datasets_verified_2026-09-22.json`); the release also holds
  DeepDRRs, masks and landmarks the pipeline does not need (`docs/DATA_COMPLETENESS_AUDIT.md` line 408).
- **Project two-labeller** boxes projected from the phantom CT through the EPPC pose; 572 boxes dropped for
  `visible_frac` < 0.5 (`tools/realxray_geneva_export.py` docstring; `docs/DATA_COMPLETENESS_AUDIT.md` line 875).

*[E]*

release poses.

**Derived products**

*[C]*

- `realxray/geneva_hip` (test-only by a written rule: "one phantom: every frame is an external TEST set")
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 408); `realxray_work/geneva_hip/verify.json` (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 722).
- `docs/devices/bv_pulsera.json`, `bv_pulsera.3free.json`, `bv_pulsera.frames.csv`: the fitted device card
  (`docs/devices/` listing).

*[E]*

none found in the disk map

**Known defects and gaps**

*[C]*

- The manifest hashed the 69-file work directory, not the 482-file source archive, so its SHA-256 says nothing about
  the release; `docs/DATASHEET.md`'s "69 files, 0.1 GB" is the work directory (`docs/DATA_COMPLETENESS_AUDIT.md`
  lines 733 and 875).
- Frames enter the bank at 372 x 372 (0.7806 mm), not native 1000 x 1000 (`tools/realxray_geneva_export.py`
  docstring; `docs/DATA_COMPLETENESS_AUDIT.md` line 874).
- The G3 split carries 19 keys for one phantom (a view count, not a subject count); all are test, so no leak
  (`SchwingNet/results/corpus_census.md` line 262). Keyed per position until 2026-09-24 (`docs/DATA_ACCOUNTING.md` §4).
- Licence conflict between repository (CC BY-SA 4.0) and paper text (CC BY-NC 4.0)
  (`docs/research_carm_datasets_verified_2026-09-22.json`).

*[E]*

the data is one phantom, so a pose is a view, not a patient (`DATA_ACCOUNTING.md` 4).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): nested zips unpacked; 482-file count. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid geneva_hip` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[C]*

1. `sbatch slurm/realxray_geneva_fetch.sh` (`slurm/realxray_geneva_fetch.sh`).
2. Must verify: zip exactly 412,867,633 bytes; sha256 equal to the value in
   `/rs/rs_grp_oschome/go2432/data/geneva_hip_src/archive.sha256` (the full value is only on the grid); 482 files
   unpacked (`docs/DATA_COMPLETENESS_AUDIT.md` lines 714 and 733).
3. Rebuild: `tools/realxray_geneva_export.py ct`, then TotalSegmentator, SPINEPS and `tools/dual_seg_compare.py`, then
   `verify`, `build`, `qc` (`tools/realxray_geneva_export.py` docstring; `slurm/realxray_geneva.sh`).

*[E]*

`sbatch slurm/realxray_geneva_fetch.sh`, which checks the size. Compare the sha256 against the recorded 4ddce9b7….

---

### `ljubljana_2d3d_gs` <a id="ljubljana_2d3d_gs"></a>

**Ljubljana 2D-3D-GS lumbar spine gold standard (Tomazevic, Likar, Pernus, MICCAI 2002).** Cards: C (ljubljana_2d3d_gs), E (ljubljana_2d3d_gs). Structured entry: `sources.yaml` id `ljubljana_2d3d_gs`; kind upstream_release; status on_disk; re-acquisition run (http).

**Source id**

*[C]*

`ljubljana_2d3d_gs` (manifest root `ljubljana` in `docs/RSNAI_DATA_MANIFEST.json`; person key `ljubljana:LJ-L1L5`
in `docs/PATIENT_IDENTITY_SPEC.md`).

*[E]*

`ljubljana_2d3d_gs` (family C's id)

**Name and citation**

*[C]*

- Ljubljana 2D-3D-GS lumbar spine gold standard. Tomazevic, Likar, Pernus, "Gold Standard 2D/3D Registration of X-ray
  to CT and MR Images", MICCAI 2002 (the paper ships inside the zip as `Documents/Miccai2002_paper.pdf`)
  (`docs/research_carm_datasets_verified_2026-09-22.json`; `LOCAL-THIS-SESSION` zip listing).
- Page https://lit.fe.uni-lj.si/en/research/resources/2D-3D-GS/; file
  https://lit.fe.uni-lj.si/data/research/resources/2D-3D-GS/2D-3D-GS.zip
  (`docs/research_carm_datasets_verified_2026-09-22.json`). No DOI recorded.
- Also re-hosted in HF `eigenvivek/xvr-data` (searcher pass) (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`
  line 49); that copy was not downloaded (`slurm/polypose_setup.sh` fetches `deepfluoro/*` only).

*[E]*

Ljubljana 2D-3D-GS (Tomazevic et al. 2002), lit.fe.uni-lj.si (`RSNAI_DATA_MANIFEST.json`).

**Modality**

*[C]*

- **Plain radiograph (DX class) on a turntable, not a C-arm**: Trixell PIXIUM 4600 flat panel (429 x 429 mm, 0.143 mm
  pixels, 14-bit), images 3x3 median-filtered and 2x subsampled to 1560 x 1560 float at 0.286 mm; source and detector
  fixed, phantom rotated (`docs/research_carm_datasets_verified_2026-09-22.json`; `tools/ljubljana_pairs.py` docstring).
- Paired CT (GE HiSpeed CT/i, 100 kV, 0.273 x 0.273 x 1 mm, supplied as five overlapping 8-bit per-vertebra crops) and
  MR (Philips Gyroscan NT Intera 1.5 T, 0.39 x 0.39 x 1.9 mm) (`docs/research_carm_datasets_verified_2026-09-22.json`;
  `tools/ljubljana_pairs.py` docstring).
- Anatomy: cadaveric L1-L5 of one 80-year-old female, in a water-filled tube (`docs/research_carm_datasets_verified_2026-09-22.json`;
  `tools/ljubljana_pairs.py` docstring).

*[E]*

turntable radiographs from a Trixell PIXIUM 4600, plus CT of a cadaveric L1-L5 specimen. This is not a C-arm (`DATASHEET.md` 2.1).

**Position/view**

*[C]*

- 18 frames at exactly 20.000 deg turntable steps (a full rotation about the long axis); source-to-detector 1009.6 mm
  on every frame; each frame has a 4x4 detector pose and source position (`docs/research_carm_datasets_verified_2026-09-22.json`).

*[E]*

18 gold-standard poses.

**Licence and access**

*[C]*

- **open**, direct HTTP, no login. CC BY-NC-ND per the research record and the manifest; the 2003 guide's "on request
  after signing the agreement" is taken as superseded by the 2021 web release
  (`docs/research_carm_datasets_verified_2026-09-22.json`; `docs/RSNAI_DATA_MANIFEST.json` `roots.ljubljana`). The
  audit's verifier saw only a generic CC link on the page (`docs/DATA_COMPLETENESS_AUDIT.md` line 866). ND forbids
  distributing derivatives; NC forbids commercial use.

*[E]*

CC BY-NC-ND.

**How it was acquired**

*[C]*

- Local download to `<repo CTSpinoPelvic1K 7ddfe38>/2D-3D-GS.zip` together with the user guide
  `2D-3D-GS_UG.pdf` (`LOCAL-THIS-SESSION`: 79,049,365 bytes, 2026-09-21 13:30:41; guide 707,342 bytes, 13:31:26).
  The tool or browser used is not recorded.
- The grid copy `/rs/rs_grp_oschome/go2432/data/ljubljana/2D-3D-GS.zip` landed 2026-09-21 14:17
  (`SchwingNet/results/g0_facts.md` §2); no fetch or copy script exists in `slurm/` or `tools/` (repo search), so how
  it got there is not recorded.
- Verification: the two copies match in size and entry count (`docs/DATA_COMPLETENESS_AUDIT.md` lines 715 and 866).
  Local hashes taken now: sha256 `31cb483882fcad8b09e5537125a7798c91bb44b9bf94a3c3b793ec52e25fdea9`, md5
  `98c3aef06d5b218906301f68fb1600e9` (`LOCAL-THIS-SESSION`). No hash of the grid copy is recorded.

*[E]*

`2D-3D-GS.zip`, 79,049,365 B. The route is not recorded beyond the page URL (`DATA_COMPLETENESS_AUDIT.md` line 715). A local copy exists at `ctsp:2D-3D-GS.zip`.

**When**

*[C]*

- 2026-09-21 (local 13:30, grid 14:17) (`SchwingNet/results/g0_facts.md` §2). Server Last-Modified of the zip:
  2021-06-16 (`docs/research_carm_datasets_verified_2026-09-22.json`). Data acquired 2002 (member dates in the zip,
  e.g. 2002-08-21; `LOCAL-THIS-SESSION`).

*[E]*

the listing dates the Ceph folder 2026-09-21.

**What it contains**

*[C]*

- Zip 79,049,365 bytes; 157 entries = 142 files + 15 directories; 210,162,660 bytes uncompressed
  (`LOCAL-THIS-SESSION`; `docs/DATA_COMPLETENESS_AUDIT.md` line 866).
- `Images/Xrays/im000..im017.{rad,raw}` (18 frames), `Images/Ct/L1..L5.{raw,sta}`, `Images/MR/L1..L5.{raw,sta}`,
  `Positions/GoldPos/gold_{ct,mr}L1..L5.txt`, `Positions/IntialPos/{Ct,Mr}/` (10 files each),
  `Positions/TargetPoints/`, `Results/{Analysed,Registration}/`, `Matlab/` (8 scripts), `Documents/` (MICCAI paper,
  MSc thesis) (`LOCAL-THIS-SESSION` zip listing).
- Grid root totals 181 files, 306,504,065 bytes, which mixes the release with derived `pairs/` and `preview/` files
  (`docs/RSNAI_DATA_MANIFEST.json`; `docs/DATA_COMPLETENESS_AUDIT.md` line 736).

*[E]*

181 files, 0.31 GB (`RSNAI_DATA_MANIFEST.json`).

**Where it is now**

*[C]*

- Local Windows: `<repo CTSpinoPelvic1K 7ddfe38>/2D-3D-GS.zip` and `2D-3D-GS_UG.pdf`, untracked in
  that repo (`LOCAL-THIS-SESSION`; gitStatus of the CTSpinoPelvic1K-1 repo).
- CEPH `/rs/rs_grp_oschome/go2432/data/ljubljana/2D-3D-GS.zip` plus the unpacked `Images/`, `Positions/`, `Results/`,
  `Documents/`, `Matlab/`. Raw (`docs/DATA_COMPLETENESS_AUDIT.md` lines 715 and 866).
- CEPH `/rs/rs_grp_oschome/go2432/data/ljubljana/pairs/` (18 `.npz` + `manifest.json`) and `preview/`. Derived
  (`tools/ljubljana_pairs.py`; `docs/DATA_COMPLETENESS_AUDIT.md` lines 723 and 736).

*[E]*

`$RS/data/ljubljana` (CEPH, raw, 0.3 GB, listing 2026-09-21)

**Annotation status**

*[C]*

- **Release labels**: fiducial gold-standard poses per vertebra for CT and MR (target registration error about
  0.15-0.26 mm CT, 0.24-0.42 mm MR), target points per vertebra (`docs/research_carm_datasets_verified_2026-09-22.json`;
  `LOCAL-THIS-SESSION` zip listing). Per-level truth comes free with the per-vertebra CT crops
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 355).
- No project boxes or levels: no bank exists (`docs/DATA_COMPLETENESS_AUDIT.md` lines 355 and 893).

*[E]*

release poses.

**Derived products**

*[C]*

- `pairs/` via `tools/ljubljana_pairs.py --root .../ljubljana --out .../ljubljana/pairs`: 18 frames with the composed
  CT, rendered at down 3 (0.858 mm/px) (`tools/ljubljana_pairs.py`; `docs/DATA_COMPLETENESS_AUDIT.md` line 723).
- `docs/devices/pixium_4600.json` and `pixium_4600.frames.csv`: the device card (device-parameter transfer only)
  (`docs/devices/` listing; `SchwingNet/results/corpus_census.md` line 263).

*[E]*

none found in the disk map

**Known defects and gaps**

*[C]*

- Detector handedness chosen by an NCC margin of 0.001 (0.8750 against 0.8741), which the tool's own docstring calls
  "a failure, not a choice" (`docs/DATA_COMPLETENESS_AUDIT.md` lines 355 and 723; `tools/ljubljana_pairs.py` docstring).
- The CT is 8-bit with an unknown window; HU per grey is set so the densest bone reads 1,500 HU
  (`tools/ljubljana_pairs.py` docstring).
- 1560 px x 0.286 mm = 446 mm exceeds the stated 429 mm panel, an inconsistency in the original description
  (`docs/research_carm_datasets_verified_2026-09-22.json`).
- In no split and no bank; not counted by the census (`SchwingNet/results/corpus_census.md` lines 35, 263, 286).
- `docs/DATASHEET.md` and `docs/RSNAI_TABLE1_DATASETS.md` "181 files, 0.3 GB" mixes release and derived files
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 736).

*[E]*

there is no truth bank, and nothing has been scored (`DATA_COMPLETENESS_AUDIT.md` line 355).

**Re-acquisition recipe**

*[C]*

1. `curl -L -o 2D-3D-GS.zip https://lit.fe.uni-lj.si/data/research/resources/2D-3D-GS/2D-3D-GS.zip` (no tool exists in
   the repo for this; the URL is from `docs/research_carm_datasets_verified_2026-09-22.json`). The audit notes that
   WebFetch was refused by the page while `curl -s` worked (`docs/DATA_COMPLETENESS_AUDIT.md` line 708).
2. Must verify: 79,049,365 bytes; sha256 `31cb4838...fdea9` (the local copy, `LOCAL-THIS-SESSION`); 157 entries / 142
   files / 210,162,660 bytes; 18 `im0NN.rad` headers at 1560 x 1560, 0.286 mm.
3. `unzip` into `/rs/rs_grp_oschome/go2432/data/ljubljana/`, then `tools/ljubljana_pairs.py --root ... --out .../pairs`
   (`tools/ljubljana_pairs.py`).

*[E]*

manual download from https://lit.fe.uni-lj.si/en/research/resources/2D-3D-GS/, then check the size against 79,049,365 B and the zip's 157 entries.

---

### `spinesac` <a id="spinesac"></a>

**SpineSAC phantom C-arm 2D/3D registration dataset (IGRS lab, HTIC / IIT Madras).** Cards: C (spinesac), E (spinesac). Structured entry: `sources.yaml` id `spinesac`; kind upstream_release; status on_disk; re-acquisition run (spinesac_fetch).

**Source id**

*[C]*

`spinesac` (manifest root, `docs/RSNAI_DATA_MANIFEST.json`).

*[E]*

`spinesac` (family C's id)

**Name and citation**

*[C]*

- SpineSAC, phantom C-arm 2D/3D registration dataset, Image Guided Robotic Surgery lab, HTIC / IIT Madras. Code
  https://github.com/IGRS-Imaging/SpineSAC (public, created 2026-06-29, last push 2026-07-15); data Google Drive folder
  `1ogGfKXpsRUV-l5eW7azMJTexrZ1Qhiar`. **No DOI and no paper found** (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`
  `final.new_confirmed[0]`; `tools/spinesac_fetch.py`).

*[E]*

SpineSAC (IGRS-Imaging, IIT Madras), a Google Drive folder plus github.com/IGRS-Imaging/SpineSAC (`DATA_COMPLETENESS_AUDIT.md` release row).

**Modality**

*[C]*

- Real C-arm fluoroscopy (RF/XA class) of lumbar **sawbone phantoms**, with conventional MDCT of the phantoms (not
  CBCT) (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`).
- Three phantoms (one closed, two open), three CT series: `set1/A` (GE Optima CT520, 552-553 slices at 0.625 mm, used
  by 43 scenarios), `ClosedSawBonesCT/A` (GE Optima CT520, 308-309 slices at 1.25 mm, 11), `Thancopen` (Siemens SOMATOM
  go.Now, 985-986 slices, "Inner Ear" protocol, 5) (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`;
  `docs/DATA_COMPLETENESS_AUDIT.md` line 889).
- Devices, by the header census: Philips Allura Xper 104 raw frames, GE Fluorostar 55, Ziehm NetPort 55, a Siemens
  Healthineers model the header does not name 38, Skanray 28, Siemens Fluorospot Compact S1 2
  (`docs/HANDOFF_2026-09-21_PM.md` line 565). The research record counts **five** sources (GE-OEC FluoroStar 12
  scenarios, Skanray 9, Ziehm EXP8000 12, a burned-in Siemens Cios Select overlay 10, a native Siemens XA header 5) and
  warns that processed files reuse one Philips AlluraXper / "TNMSC, Chennai" / 2020-02-26 template header
  (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`). The device count (five or six) is therefore unsettled.

*[E]*

frames from six C-arms of sawbone phantoms, plus phantom CTs (`DATASHEET.md` 2.1).

**Position/view**

*[C]*

- 59 scenarios of AP and lateral (LP) acquisitions; 118 processed PNGs, 116 distinct, 58 distinct AP-LP pairs; each
  scenario ships `APLP.txt` (two 3x4 projection matrices), `P_Imf*`, `x0.txt`, `TARGET.txt`, `roi_config.json`
  (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`).
- The positioner tags take one value per device across AP and lateral files (`SchwingNet/results/coverage/DICOM_VARIABLES.md`).

*[E]*

59 AP-LP acquisition scenarios.

**Licence and access**

*[C]*

- **open** download (no login), but **no data licence** anywhere on the Drive; the repo LICENSE.md is an unfilled
  Apache-2.0 template and the README badge claims MIT (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`).
  Reuse terms for the images are therefore not stated; nothing is redistributed (`slurm/spinesac_fetch.sh` header).

*[E]*

"see repository" (`RSNAI_DATA_MANIFEST.json`).

**How it was acquired**

*[C]*

- `sbatch slurm/spinesac_fetch.sh`: `git clone https://github.com/IGRS-Imaging/SpineSAC repo`, then
  `tools/spinesac_fetch.py --out /rs/rs_grp_oschome/go2432/data/spinesac/drive --workers 8`, then `file_list.txt` and
  `dir_list.txt` (`slurm/spinesac_fetch.sh`).
- `tools/spinesac_fetch.py` lists folders through Drive's `embeddedfolderview` page (the plain page caps at 50
  entries), downloads each file from `drive.usercontent.google.com` (gdown handles the confirm step), writes
  `drive_tree.json` with every Drive id, path and size, and keeps existing non-empty files (`tools/spinesac_fetch.py`).
- Verification: file count against `drive_tree.json`; an empty body is accepted only where the listing declares size 0
  (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs 2026-09-23, at line 1498).

*[E]*

`sbatch slurm/spinesac_fetch.sh`, which clones the repo and runs `tools/spinesac_fetch.py --out $RS/data/spinesac/drive --workers 8`.

**When**

*[C]*

- First fetch job 40411573: 5,490 of 5,492 files (`docs/DATA_COMPLETENESS_AUDIT.md` line 716); Ceph `data/spinesac`
  dated 2026-09-22 (`LISTING`); git c7013ca and 9fcc9cf, 2026-09-22.
- The last two files (both zero bytes on Drive) landed in job 40416585 on 2026-09-23: 5,492 of 5,492
  (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs at line 1498; `SchwingNet/results/repairs/ds815-spinesac_CHECK.md` row 1).

*[E]*

the scripts were first committed 2026-09-22. The listing dates the folder 2026-09-22.

**What it contains**

*[C]*

- Drive tree 5,492 files in 1,254 folders, 4.15 GB (`docs/DATA_COMPLETENESS_AUDIT.md` line 709).
- At the manifest (5,490 files): 4,147,554,733 bytes; no extension 1,895, `.txt` 1,150, `.dcm` 868, `.png` 813, `.json`
  546, `.xlsx` 104, `.jpg` 55, `.bmp` 34, `.ini` 13, `.nii` 5, `.csv` 4, `.zip` 2 (`docs/RSNAI_DATA_MANIFEST.json`
  `roots.spinesac`).
- 3 CT series, 915 2-D DICOMs, 902 PNGs (`docs/HANDOFF_2026-09-21_PM.md` line 536); 286 raw DICOM frames + 233
  unreferenced raw frames + 118 processed frames (`docs/DATA_COMPLETENESS_AUDIT.md` section at line 215).

*[E]*

5,490 of 5,492 files, 4.15 GB (`RSNAI_DATA_MANIFEST.json`; `DATA_COMPLETENESS_AUDIT.md` line 716).

**Where it is now**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/spinesac/drive/` (raw), `repo/` (code clone), `drive_tree.json`,
  `file_list.txt`, `dir_list.txt` (`slurm/spinesac_fetch.sh`; `tools/spinesac_fetch.py`).
- CEPH `/rs/rs_grp_oschome/go2432/data/or_ready/spinesac/{preds, display, sheets, inventory.json, ct/{set1_A,
  thancopen, closed_A}/ct.nii.gz, ct_probe/}`. Derived (`docs/DATA_COMPLETENESS_AUDIT.md` line 724;
  `SchwingNet/results/repairs/ds815-spinesac_CHECK.md` row 17).
- CEPH `/rs/rs_grp_oschome/go2432/data/spineps/spinesac/`. Derived (`SchwingNet/results/JOBS_data_repairs.txt` line 248).

*[E]*

`$RS/data/spinesac` (CEPH, raw, 4.2 GB, listing 2026-09-22); `$RS/data/spinesac/drive` (CEPH, raw, 4.2 GB)

**Annotation status**

*[C]*

- **Release labels**: per-scenario projection matrices, target points and ROI configs (registration ground truth);
  no vertebra labels (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`).
- **Project**: none landed. TotalSegmentator found no bone in the sawbone CTs; the SPINEPS body-truth chain
  (40416582-40416584) was queued on 2026-09-23 (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs at line 1491;
  `SchwingNet/results/repairs/ds815-spinesac_CHECK.md` line 96). Its outcome is not recorded locally.

*[E]*

no bone truth.

**Derived products**

*[C]*

- Detector predictions of five arms on 286 raw + 118 processed frames, contact sheets (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 724).
- Per-device header census files `docs/devices/census/*_headers.json` / `*_frames.csv` (GE Fluorostar, Philips
  AlluraXper, Siemens Healthineers, Siemens Fluorospot Compact S1, Skanray, Ziehm NetPort, and one unnamed)
  (`docs/devices/census/` listing).

*[E]*

1 entries: `~/runs`

**Known defects and gaps**

*[C]*

- No bone truth and no score; the 2026-09-22 chain crashed (empty TotalSegmentator masks, a 3 TiB SVD in the fallback,
  an inventory kwarg bug, truth and score run before the inventory existed) and was never resubmitted until
  2026-09-23 (`docs/DATA_COMPLETENESS_AUDIT.md` line 215 section and line 888).
- `docs/DATASHEET.md` and `docs/RSNAI_TABLE1_DATASETS.md` say "one sawbone phantom"; there are three
  (`docs/DATA_COMPLETENESS_AUDIT.md` lines 734 and 889).
- The person key should be the phantom, not the scenario, and is UNVERIFIED (`docs/DATA_ACCOUNTING.md` §4).
- `Train_Set` is byte-identical to `ganga_accuracy_study_set1`; `GE_SCN3` holds 48 numbers in `APLP.txt` instead of 24
  (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`).
- DICOM metadata in processed files is unreliable (reused template header) (same JSON).

*[E]*

2 files were never fetched (`DATA_COMPLETENESS_AUDIT.md` line 220).

**Re-acquisition recipe**

*[C]*

1. `sbatch slurm/spinesac_fetch.sh` on a compute node (resumable) (`slurm/spinesac_fetch.sh`).
2. Must verify: `wc -l file_list.txt` = 5,492; every size equal to `drive_tree.json`; exactly two zero-byte files
   (`BMJH/SKANRAY/SCN 6/Output/AP/PD/AP_2D.txt`, `.../AP/DD/AP_icp_2D.txt`); about 4.15 GB
   (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs at line 1498; `SchwingNet/results/repairs/ds815-spinesac_CHECK.md` row 1).
3. The Drive folder can change or vanish without notice, and no checksum is published (no DOI)
   (`docs/research_datasets_fourth_pass_verified_2026-09-22.json`); keep the local copy as the reference.

*[E]*

`sbatch slurm/spinesac_fetch.sh`. Verify against the 5,492 files in `drive_tree.json`.

---

### `realxray_layout` <a id="realxray_layout"></a>

**realxray layout: real frames with projected labels, one directory per device bank (+ realxray_work, pelvis_landmarks).** Cards: C (realxray_layout). Structured entry: `sources.yaml` id `realxray_layout`; kind derived_root; status on_disk; re-acquisition manual (rebuild).

**Source id**

`realxray_layout` — a derived output layout, not a source (`docs/REAL_XRAY_DATASETS_SPEC.md`). Covers
`data/realxray/`, `data/realxray_work/` and `data/realxray/pelvis_landmarks/`.

**Name and citation**

- "Real X-ray datasets with projected labels: the one format every builder writes", written 2026-09-21
  (`docs/REAL_XRAY_DATASETS_SPEC.md`).

**Modality**

- Real frames only (fluoroscopy, kV CBCT projections), one directory per device bank, each frame with vertebra (class 0)
  and sacrum (class 1) boxes projected from the registered CT or CBCT through the frame's pose
  (`docs/REAL_XRAY_DATASETS_SPEC.md` "Layout"; `docs/DATASHEET.md` §2.2).

**Position/view**

- Per-frame `view` block (`gantry_deg`, `lat_from_ap_deg`, `cranial_caudal_deg`) and pose (`source`, K, ext, QC NCCs)
  in `meta/<stem>.json` (`docs/REAL_XRAY_DATASETS_SPEC.md` "Meta").

**Licence and access**

- **Not distributed.** Each source keeps its own licence (CC BY 4.0, CC BY-NC 4.0, CC BY-NC(-SA) 4.0, CC BY-SA 4.0,
  CC BY-NC-ND), so a merged redistribution is not possible; a reader rebuilds it from the sources and the exporters
  (`docs/DATASHEET.md` §6).

**How it was acquired**

- Built, not downloaded: `tools/realxray_cobra_export.py`, `tools/realxray_deepfluoro_export.py`,
  `tools/realxray_geneva_export.py`, and `tools/carmlspine_labels.py` for C-ArmLSpine (`docs/RSNAI_DATA_MANIFEST.json`
  `roots.realxray`; `docs/DATA_COMPLETENESS_AUDIT.md` line 203). Derived views and re-windows by
  `tools/realxray_rewindow.py`, `tools/realxray_subset_view.py`, `tools/carmlspine_multi_build.py`
  (`tools/realxray_banks.json`).
- Display: stored value to attenuation per device, then one window for all devices (field percentiles
  1/5/50/95/99 to 27/47/126/216/239), bone bright (`docs/REAL_XRAY_DATASETS_SPEC.md` "Display").
- Splits by case or specimen, `int(md5(case), 16) % 10`: 0-6 train, 7 val, 8-9 test (`docs/REAL_XRAY_DATASETS_SPEC.md`).
- Admission list: `tools/realxray_banks.json`; `tools/realxray_train.py ready()` refuses any bank not listed; roles
  `device`, `derived`, `smoke` (`tools/realxray_banks.json` `_README`).

**When**

- Spec 2026-09-21; first banks 2026-09-21 (DeepFluoro 17:59, C-ArmLSpine 20:24-20:47) (`docs/REAL_XRAY_DATASETS_SPEC.md`;
  `docs/DATA_COMPLETENESS_AUDIT.md` section at line 200 and line 720). Repaired C-ArmLSpine bank 2026-09-23
  (`docs/DATA_COMPLETENESS_AUDIT.md` Repairs). `data/realxray` dated 2026-09-26, `data/realxray_work` 2026-09-21 (`LISTING`).

**What it contains**

- At the manifest (2026-09-22 06:49): 67,682 files, 3,859,860,245 bytes (`.png` 29,867, `.json` 21,291, `.txt` 16,352,
  `.npz` 152, ...) (`docs/RSNAI_DATA_MANIFEST.json` `roots.realxray`).
- Banks at the 2026-09-24 census (`SchwingNet/results/corpus_census.md` lines 96-98 and 126-136):

| bank | role | items | from |
|---|---|---:|---|
| `carmlspine` | device | 299 | C-ArmLSpine |
| `carmlspine_pre_repair_2026-09-23` | kept copy | 296 | C-ArmLSpine |
| `carmlspine_sweep` | real, side val | 301 | C-ArmLSpine case134 sweep |
| `carmlspine_multi` | derived | not counted | C-ArmLSpine (`tools/realxray_banks.json`) |
| `cobra_elekta` | device | 3,480 | COBRA2026 |
| `cobra_elekta_v2`, `cobra_elekta_v3` | derived | 3,480 each | COBRA2026 |
| `cobra_elekta_ap45`, `cobra_elekta_v2_ap45` | derived | 1,634 each | COBRA2026 |
| `cobra_elekta_smoke` | smoke | 24 | COBRA2026 A004 |
| `cobra_elekta_g3test` | not in the split | not counted | COBRA2026 (`SchwingNet/results/corpus_census.md` line 288) |
| `deepfluoro` | device | 366 | DeepFluoro H5 |
| `geneva_hip` | device, test only | 116 | Geneva |
| `pelvis_landmarks/cobra_elekta`, `/deepfluoro`, `/geneva_hip` | derived | 3,120 / 342 / 116 | the three banks |

- No `cobra_varian` and no `ljubljana` bank (`tools/realxray_banks.json`; `docs/DATA_COMPLETENESS_AUDIT.md` lines 472
  and 893).
- `realxray_work/` holds the export work directories `geneva_hip` (69 files) and `deepfluoro`
  (`docs/RSNAI_DATA_MANIFEST.json`; `docs/DATA_COMPLETENESS_AUDIT.md` line 720).

**Where it is now**

- CEPH `/rs/rs_grp_oschome/go2432/data/realxray/<bank>/{images/<split>, labels/<split>, meta, splits.json, data.yaml,
  qc, summary.json}` (`docs/REAL_XRAY_DATASETS_SPEC.md`).
- CEPH `/rs/rs_grp_oschome/go2432/data/realxray_work/{geneva_hip, deepfluoro}` (`docs/RSNAI_DATA_MANIFEST.json`;
  `docs/DATA_COMPLETENESS_AUDIT.md` line 720).
- Detector runs trained on these banks: HOME `~/spine-detector/runs/realxray/rx_*` (`docs/DATA_COMPLETENESS_AUDIT.md`
  lines 457-458).

**Annotation status**

- Two-labeller automatic level names per box (`level_ts`, `level_spineps`, `level_agree`, `level`); boxes with a null
  level are kept for detection and excluded from naming scores (`docs/REAL_XRAY_DATASETS_SPEC.md` "Two labellers").

**Derived products**

- Detector training lists, whole-spine bank, cross-device bins, device census, audits (`docs/DATA_COMPLETENESS_AUDIT.md`
  lines 457-462); audits in `CEPH .../data/or_ready/audit/AUDIT.md` (`docs/DATASHEET.md` §§2.5, 4).

**Known defects and gaps**

- Before `tools/realxray_banks.json`, `ready()` globbed every `data.yaml` and swept derived banks into one arm
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 18).
- Two arms share one label cache (`rx_lodo_cobra_elekta` and `rx_lodo_deepfluoro` both write
  `carmlspine/labels/test.cache`) (`docs/DATA_ACCOUNTING.md` line 256).
- The patient keyer cannot see these banks (it globs `ann/*.json`; they store `meta/`) (`docs/PATIENT_IDENTITY_SPEC.md`
  row carmlspine).
- The "1024 x 1024 PNG" sentence in `SchwingNet/atlas/dataset.json` holds only for C-ArmLSpine (DeepFluoro 384, Geneva
  372, COBRA 517) (`docs/DATA_COMPLETENESS_AUDIT.md` line 886).
- The layout is an output root that drifts; the manifest check must run on input roots only (`docs/DATASHEET.md` §7).

**Re-acquisition recipe**

- Not downloadable. Re-acquire each source (cards above), then run the exporters in the order their docstrings give
  (`tools/realxray_cobra_export.py`: nifti, tables, export, relevel, finalize; `tools/realxray_deepfluoro_export.py`:
  ct, build, qc; `tools/realxray_geneva_export.py`: ct, verify, build, qc; `tools/carmlspine_labels.py`: build,
  finalize). Then `python tools/realxray_train.py check --root /rs/rs_grp_oschome/go2432/data/realxray` (case-id
  disjointness across device banks) (`tools/realxray_banks.json` `_README`). Look at every `qc/` contact sheet before
  quoting a number (`docs/REAL_XRAY_DATASETS_SPEC.md` "Rules for builders").

---

### `or_ready` <a id="or_ready"></a>

**or_ready: OR-readiness program results, models and dumps.** Cards: C (or_ready). Structured entry: `sources.yaml` id `or_ready`; kind derived_root; status on_disk; re-acquisition manual (rebuild).

**Source id**

`or_ready` — a derived output root, not a source (`docs/RSNAI_DATA_MANIFEST.json` `roots.or_ready`: "every result JSON
of the readiness program").

**Name and citation**

- The OR-readiness adversarial program's output root (`docs/HANDOFF_2026-09-21_PM.md` lines 452, 498-499;
  `MEM/carmlspine-level-experiment.md`).

**Modality**

- Mixed: result JSONs, contact sheets, detector predictions, cached renders and models over the real-frame banks and
  the SpineSAC frames (`docs/RSNAI_DATA_MANIFEST.json` extension histogram; `docs/DATA_COMPLETENESS_AUDIT.md` line 724).

**Position/view**

- Not applicable (results).

**Licence and access**

- Internal results; contains derived images of sources with NC and ND licences, so not redistributable as a whole
  (`docs/DATASHEET.md` §6).

**How it was acquired**

- Written by the program's tools and jobs (audit, robustness, cross-device, whole-spine, SpineSAC, thoracic, device fit)
  (`docs/HANDOFF_2026-09-21_PM.md` line 498; git c7013ca 2026-09-22 message).

**When**

- From 2026-09-22 (git c7013ca, "Overnight OR-readiness program"); `data/or_ready` dated 2026-09-24 (`LISTING`).

**What it contains**

- 136,813 files, 20,156,257,730 bytes at the manifest of 2026-09-22 (`docs/RSNAI_DATA_MANIFEST.json`); "or_ready models
  and dumps 682" GB on 2026-09-25 (`docs/CENSUS_TABLE_2026-09-25.md` §4).
- Known subdirectories: `audit/` (`AUDIT.md`), `wholespine/`, `lodo/`, `robust/`, `crossdev/`, `thoracic/`, `spinesac/`,
  `devices/varian_halcyon/pairs`, `devices_refit_constrained/`, `eval_gate/` (`touched.json`), `data_accounting/`
  (`docs/HANDOFF_2026-09-21_PM.md` lines 498-499; `docs/DATA_ACCOUNTING.md` lines 133, 306, 388;
  `docs/RESUME_2026-09-22_PM.md` line 1291; `docs/DATASHEET.md` §2.5).

**Where it is now**

- CEPH `/rs/rs_grp_oschome/go2432/data/or_ready/` (`docs/RSNAI_DATA_MANIFEST.json`).

**Annotation status**

- Not applicable; holds predictions and scores, not truth (SpineSAC predictions without truth)
  (`docs/DATA_COMPLETENESS_AUDIT.md` line 724).

**Derived products**

- The tables and numbers of the RSNA AI manuscript (`docs/DATASHEET.md` §7).

**Known defects and gaps**

- An output root that drifts by design; never hash-check it as an input (`docs/DATASHEET.md` §7).
- Its size grew from about 20 GB to 682 GB in three days (`docs/RSNAI_DATA_MANIFEST.json`;
  `docs/CENSUS_TABLE_2026-09-25.md` §4); which subdirectories hold the models is not recorded.

**Re-acquisition recipe**

- Not downloadable; rerun the program's jobs. For a data migration, treat it as results: move, do not index as data.

---

### `devcorpus` <a id="devcorpus"></a>

**devcorpus: multi-device synthetic corpus (TotalSegmentator CTs under real device poses, styled by fitted device cards) + devcorpus_arc.** Cards: C (devcorpus), E (devcorpus). Structured entry: `sources.yaml` id `devcorpus`; kind derived; status on_disk; re-acquisition manual (rebuild).

**Source id**

*[C]*

`devcorpus` — synthetic renders built from other sources (`tools/devcorpus_build.py`). Also covers `devcorpus_arc` and
the fitted device cards `docs/devices/*.json`. This card also belongs to the synthetic-render family.

*[E]*

`devcorpus`

**Name and citation**

*[C]*

- The multi-device synthetic corpus (`tools/devcorpus_build.py` docstring; `docs/DATASHEET.md` §2.7).

*[E]*

Synthetic device corpus: TotalSegmentator CTs ray-cast under each device's real poses and styled by its nine fitted terms (`DATASHEET.md` 2.7)

**Modality**

*[C]*

- **Synthetic render**: whole-spine TotalSegmentator CTs ray-cast under each C-arm's real poses and styled through
  that device's fitted nine-term card (scatter, penumbra, quantum noise, blur, edge enhancement, vignette, display
  window, orientation) (`tools/devcorpus_build.py` docstring; `docs/DATASHEET.md` §2.7).
- Geometries: `cios_fusion` (DeepFluoro poses), `surgio_b51_dr` (C-ArmLSpine consensus registrations), `elekta_xvi`
  (COBRA RTK matrices) (`tools/devcorpus_build.py` docstring).

*[E]*

synthetic render (device-styled DRR)

**Position/view**

*[C]*

- Real pose pools per device; `--arc N` adds synthetic poses over lateral angle -90 to +90 deg, tilt +/-15, roll
  +/-10 (`tools/devcorpus_build.py` docstring).

*[E]*

per-device real poses; oblique arcs in `devcorpus_arc` (`nnunet:slurm/arc_pools.sh`)

**Licence and access**

*[C]*

- Derived from TotalSegmentator (CC BY 4.0) CTs and from the device sources' poses and cards
  (`docs/RSNAI_DATA_MANIFEST.json` `roots.ts_subjects`). Not distributed (`docs/DATASHEET.md` §6).

*[E]*

project-built from totalsegmentator_v201/v300 (family C's id `devcorpus`)

**How it was acquired**

*[C]*

- `tools/devcorpus_build.py poses | render | style | lists` (`tools/devcorpus_build.py`), run by `slurm/devcorpus.sh`,
  `slurm/devcorpus_pooled.sh`, `slurm/devcorpus_train.sh` (`slurm/` listing).
- Subject list `~/model_night/ts_clean_subjects.txt`, sha256 2f96f917... (`docs/RSNAI_DATA_MANIFEST.json` `splits`);
  142 subjects, 17 of them validation in every styled corpus (`docs/PATIENT_IDENTITY_SPEC.md` row devcorpus;
  `docs/DATASHEET.md` §2.7).

*[E]*

`nnunet:tools/devcorpus_build.py` (`RSNAI_DATA_MANIFEST.json` root devcorpus)

**When**

*[C]*

- Builder committed 2026-09-22 (git 0fbb269); `data/devcorpus` dated 2026-09-22, `data/devcorpus_arc` 2026-09-24
  (`LISTING`).

*[E]*

`$RS/data/devcorpus` is dated 2026-09-22 and `devcorpus_arc` 2026-09-24 in the listing

**What it contains**

*[C]*

- 4,551 files, 2,448,009,749 bytes (`.json` 2,146, `.npz` 2,143, `.jpg` 262) at the manifest (`docs/RSNAI_DATA_MANIFEST.json`
  `roots.devcorpus`).
- One training arm: 5,408 synthetic entries, 896 real entries (`real_rep: 2`), 794 validation entries
  (`docs/DATASHEET.md` §2.7, from `~/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/scores.json`).
- `devcorpus_arc/anglesweep/elekta_xvi` and `/surgio_b51_dr`: 969 renders each (`SchwingNet/results/corpus_census.md`
  lines 137-138).
- Device cards: `bv_pulsera`, `cios_fusion`, `elekta_xvi`, `pixium_4600` (each `.json` + `.frames.csv`, two with a
  `.3free.json`); no Surgio-B51 card file and no Varian card (`docs/devices/` listing; `docs/DATA_COMPLETENESS_AUDIT.md`
  line 470).

*[E]*

4,551 files, 2.45 GB (`RSNAI_DATA_MANIFEST.json`); 142 subjects per device (`DATA_COMPLETENESS_AUDIT.md` line 491)

**Where it is now**

*[C]*

- CEPH `/rs/rs_grp_oschome/go2432/data/devcorpus/` (`poses/`, renders, `styled/*`, LODO lists) and
  `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/` (`tools/devcorpus_build.py`; `docs/DATA_ACCOUNTING.md` line 136;
  `LISTING`).
- Training runs: HOME `~/spine-detector/runs/devcorpus/` (`docs/DATASHEET.md` §2.7).
- Device cards: in the repo, `docs/devices/` (local).

*[E]*

`$RS/data/devcorpus` (CEPH, converted/derived, 2.5 GB, listing 2026-09-22); `$RS/data/devcorpus_arc` (CEPH, converted/derived, listing 2026-09-24)

**Annotation status**

*[C]*

- Boxes projected from every vertebral mask of the TotalSegmentator labels (synthetic truth, by construction)
  (`tools/devcorpus_build.py` docstring).

*[E]*

inherits the TotalSegmentator labels

**Derived products**

*[C]*

- LODO and pooled training lists (designs P, A, B) (`tools/devcorpus_build.py` docstring).

*[E]*

none found in the disk map

**Known defects and gaps**

*[C]*

- A styled frame reaches 2-5 % of its device's learned distribution (git 98edfda message).
- The TotalSegmentator release behind it is described as "v2" in `docs/DATASHEET.md` §2.7 and
  `docs/RSNAI_DATA_MANIFEST.json` (`ts_subjects.source`), while the path is `TotalSegmentator_v3/Totalsegmentator_dataset_v300`
  and `docs/PATIENT_IDENTITY_SPEC.md` keys it as a v3 subject. Which release was rendered is unsettled on paper.
- The Elekta card under the `elekta_xvi` styling was fitted on 40 frames from three cases (`docs/DATA_COMPLETENESS_AUDIT.md`
  line 48).
- The 17 held-out subjects sit unkeyed in up to five other CT render banks (`docs/PATIENT_IDENTITY_SPEC.md` row devcorpus).

*[E]*

renders 1,537 against an expected 1,562 for one device (`DATA_COMPLETENESS_AUDIT.md` line 491)

**Re-acquisition recipe**

*[C]*

- Not downloadable. Needs TotalSegmentator (see the CT family), the three pose pools (cards `deepfluoro_h5`,
  `carmlspine`, `cobra2026`) and the device cards; then `python tools/devcorpus_build.py poses --device <d>`, `render
  --geometry <g> --n 1500 --workers 16`, `style --geometry <g> --noise <d> --draws 2`, `lists --design <A|B|P> --held <d>`
  (`tools/devcorpus_build.py` docstring). Verify the subject list against sha256 2f96f917... (`docs/RSNAI_DATA_MANIFEST.json`).

*[E]*

re-run `tools/devcorpus_build.py` over `~/model_night/ts_clean_subjects.txt` (sha256 2f96f917…, `RSNAI_DATA_MANIFEST.json` splits)


Synthetic-hardware CTs (`implant_*`) and post-op renders are listed under the CT they were made from.

---

## 8. Family D: plain-film and harvested 2-D corpora and their banks

The family's own preface, legend and shared notes, verbatim:

Written 2026-10-07 from files on this machine only (no grid or network access). Every line cites the file it rests
on, in parentheses. Where nothing on disk records a fact, the card says "not recorded"; the full list of those is the
`unknowns` table at the end.

### Path prefixes used in the citations

| prefix | absolute path |
|---|---|
| `sscn:` | `<repo spinesurg-ct-nnunet 097933a>/` (private repo, branch L6_Class) |
| `ctsp:` | `<repo CTSpinoPelvic1K 7ddfe38>/` |
| `xrsp:` | `<repo XRSpinoPelvic1K 4f22935>/` (local clone of the XRSpinoPelvic1K repo) |
| `sdet:` | `<laptop folder Desktop/spine-detector; not a dependency>/` (local snapshot, no `.git`, files dated 2026-09-01 to 09-12) |
| `mem:` | `<memory notes; see MEMORY.md>/` |
| `census:` | `<session scratchpad; not a dependency>/census/` |
| `sdr:` | `sscn:spine_data_review/` |

Location tags: **HOME** = `/wsu/home/go/go24/go2432` (Panasas, written `~`); **CEPH** = `/rs/rs_grp_oschome/go2432`
(written `$RS`); **LOCAL** = this Windows machine; **WSL** = the WSL distribution on this machine
(`/home/gschwing`). Directory dates are the mtimes in `census:toplevel_listing.txt` (taken 2026-10-07); they are
last-modified dates, not creation dates. The per-directory byte counts of the 2026-10-07 storage census (Slurm job
40578909, `$RS/data/inventory/census_2026-10-07/`) were not available when this was written; the sizes below are the
older figures their cited files give.

Cross-family notes: the CT render banks (`ctsp_drr`, `verse_drr`, `physics_drr`, `ts_drr`, ...) and the C-ArmLSpine
banks (`carm_*`) belong to other families and appear here only in Appendix A, because the mixed crop banks combine
them with film sources.

---

### Cards

### `csxa_cervical_xray_atlas` <a id="csxa_cervical_xray_atlas"></a>

**Cervical Spine X-ray Atlas (CSXA) V3.0 (Ran et al., Sci Data 2024;11:625).** Cards: D (D01 CSXA cervical spine X-ray atlas), E (csxa_cervical_xray_atlas). Structured entry: `sources.yaml` id `csxa_cervical_xray_atlas`; kind upstream_release; status on_disk; re-acquisition manual (manual).

**Source id**

*[D]*

`csxa_cervical_xray_atlas` (sscn:tools/xray_dataset_usage.py, key `csxa`)

*[E]*

`csxa_cervical_xray_atlas` (family D's id)

**Name and citation**

*[D]*

Cervical Spine X-ray Atlas (CSXA) V3.0. Ran Y, Qin W, Qin C, et al. "A high-quality dataset featuring classified and
annotated cervical spine X-ray atlas." Scientific Data 2024;11:625, doi:10.1038/s41597-024-03383-0, PMID 38871800,
PMC11176335 (sscn:paper/rsnai/refs.bib, entry `csxa`). Data: Science Data Bank doi:10.57760/sciencedb.15391; code
https://github.com/yran888/CSXA-dataset (sscn:paper/rsnai/refs.bib annote; sscn:docs/BIB_RESOLVE_2026-09-22.json).

*[E]*

CSXA, Scientific Data 2024, s41597-024-03383-0; ScienceDB 10.57760/sciencedb.15391 (`DATA_COMPLETENESS_AUDIT.md` release row).

**Modality**

*[D]*

Plain film (digital radiograph exported as 8-bit PNG); cervical spine, lateral field C1 to C7
(sscn:docs/XRAY_DATASET_USAGE.md; sscn:docs/DATA_COMPLETENESS_AUDIT.md "Plain-film corpora" release row).

*[E]*

plain film, cervical spine.

**Position/view**

*[D]*

Lateral (sscn:docs/XRAY_DATASET_USAGE.md). Standing / neutral / flexion posture: not recorded.

*[E]*

lateral (`XRAY_DATASET_USAGE.json`).

**Licence and access**

*[D]*

CC BY 4.0 (sscn:paper/rsnai/refs.bib annote). The images sit behind a Science Data Bank browser session, so the
download is manual (sdet:src/build_dataset.py docstring; mem:xray-corner-detector-status.md "CSXA (ScienceDB) needs a
browser download"). The GitHub repository holds code and no data files
(sdr:runs/review_availability_full/charting_probes/csxa.json, probe of 2026-09-19). Derived labels: CC BY permits
derivatives with attribution (the licence text itself is not stored on disk).

*[E]*

not recorded in Family E's evidence.

**How it was acquired**

*[D]*

Manual browser download from Science Data Bank plus the GitHub repository archive; the grid copy holds
`csxa_repo.zip`, `extracted/CSXA-dataset-main`, `images/datasets-PNG`, `annotations/datasets-JSON`, `datasets.xlsx` and
the descriptor PDF `s41597-024-03383-0.pdf` (sscn:docs/DATA_COMPLETENESS_AUDIT.md, plain-film on-disk row). The exact
command, the person and any checksum: not recorded. Verification that ran afterwards: PNG and JSON counts (4,963 each)
and xlsx rows (sscn:docs/DATA_COMPLETENESS_AUDIT.md independent re-count, "CSXA 4,963/4,963 complete").

*[E]*

`download_sources.py` (grid only).

**When**

*[D]*

Repository archive 2026-09-01 22:50 (grid ctime of `~/spine-detector/data/raw/csxa/CSXA-dataset-main/LICENSE`); images 2026-09-09 23:00 (ctime of the images directory) (sscn:SchwingNet/results/g0_facts.md §2). This agrees with the memory note that on 2026-09-08 the images still "needed a browser download" (mem:xray-corner-detector-status.md). All 4,963 films are inside `~/films_drr`, whose directory date is 2026-09-13 (census:toplevel_listing.txt; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 4).

*[E]*

not recorded in family E's evidence (the dates above are from g0_facts.md §2).

**What it contains**

*[D]*

4,963 PNG + 4,963 labelme JSON, one image per individual per the descriptor, 4,963 individuals (3,202 F / 1,761 M);
`datasets.xlsx` sheet "Basic information" has 5,002 rows = 2 header + 5,000 slots, 4,963 filled, with sex, age,
curvature class and 118 parameters (sscn:docs/DATA_COMPLETENESS_AUDIT.md release, on-disk and criterion rows).
23 labelme shapes per film (22 corners + a C2 centroid); labellable levels C2 (inferior corners only) and C3-C7
(sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1). Age median 36 [IQR 30-46], 64.5 % female
(sscn:SchwingNet/tables/tabS3_corpus.md). Bytes on disk: not recorded.

*[E]*

4,963 PNG with 4,963 JSON, one image per individual (`DATA_COMPLETENESS_AUDIT.md` line 528).

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/csxa/{images/datasets-PNG, annotations/datasets-JSON, datasets.xlsx, csxa_repo.zip, extracted/CSXA-dataset-main, s41597-024-03383-0.pdf}` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).
- HOME converted: `~/films_drr` (4,963 of its 9,109 films) and `~/films_drr_buucorr` (copy) (sscn:SchwingNet/results/corpus_census.md section 3).
- HOME derived: detector corpora `~/spine-detector/data/yolo_v3/images/*/csxa_*` (sscn:docs/DATA_ACCOUNTING.md section 3).
- No CEPH copy recorded.

*[E]*

`~/film_style_ds` (HOME, converted/derived, listing 2026-09-17); `~/films_drr` (HOME, converted/derived, 36.0 GB, listing 2026-09-13); `~/films_drr_buucorr` (HOME, converted/derived, listing 2026-09-17); `~/films_smoke` (HOME, converted/derived, listing 2026-09-13); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/yolo_levels` (HOME, converted/derived, 6.7 GB, listing 2026-09-13); `~/spine-detector/data/raw/csxa` (HOME, raw)

**Annotation status**

*[D]*

Release labels: per-vertebra corner keypoints whose label strings name the level
(sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1, "annotated -- label strings name the level"). Not re-read by
this project.

*[E]*

release per-vertebra keypoints, with levels named (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1).

**Derived products**

*[D]*

- `~/films_drr` → crop banks `films_ann_fov96_ctx`, `films_all2_fov96_ctx`, `allspine_fov96_ctx`, `allspine_v6/v7/v7nofluoro/v8/v9_fov96_ctx`, `mv_bands` (sscn:docs/XRAY_DATASET_USAGE.json `banks`; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 3).
- In the shipped level bank `allspine_v9_fov96_ctx`: 4,963 films, 4,214 train / 749 val (sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" row, log `v9bank_40415668.out`).
- C-ArmLSpine fold banks: 1,478 films as 1,758 crops (sscn:docs/MODEL_CARD.md section 3.2).
- Person split of 2026-09-23: 4,963 persons, 3,979 / 485 / 499 (sscn:SchwingNet/results/corpus_census.md section 0).
- Manuscript naming figure "CSXA 99.8 %" scored on the `allspine_v8` selection split (sscn:SchwingNet/packet_src/statements.md item 6).
- FluoroGen film-look LoRA training set `~/film_style_ds` (sscn:tools/film_style_dataset.py docstring).

*[E]*

10 entries: `~/allspine_fov96_ctx`, `~/allspine_v6_fov96_ctx`, `~/allspine_v7_fov96_ctx`, `~/allspine_v7nofluoro_fov96_ctx`, `~/allspine_v8_fov96_ctx`, `~/allspine_v9_fov96_ctx`, `~/films_all2_fov128m_ctx`, `~/films_all2_fov96_ctx`, `~/films_ann_fov96_ctx`, `~/mv_bands`

**Known defects and gaps**

*[D]*

- One-image-one-patient is the descriptor's claim and is untested here (sscn:docs/DATASHEET.md section 4; sscn:docs/PATIENT_IDENTITY_SPEC.md section 2 csxa row).
- The release uses 4,963 of 5,000 sequence numbers (37 never released; release-side) (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Gaps the auditor missed").
- The `<G><AA>` tail of the file name disagrees with the table on `0873166` and `3556142`; keep it out of the person key (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2).
- Not listed in `docs/RSNAI_DATA_MANIFEST.json`, which has no film root at all (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Documents that disagree"; sscn:docs/RSNAI_DATA_MANIFEST.json roots).

*[E]*

"one image = one patient" is assumed and untested (`DATA_ACCOUNTING.md` 4).

**Re-acquisition recipe**

*[D]*

Manual (browser session): open doi:10.57760/sciencedb.15391 and download the CSXA V3.0 archive; then
`git clone https://github.com/yran888/CSXA-dataset`. Lay out as `raw/csxa/images/datasets-PNG`,
`raw/csxa/annotations/datasets-JSON`, `raw/csxa/datasets.xlsx`. Verify: 4,963 PNG, 4,963 JSON with matching stems,
xlsx "Basic information" 4,963 filled rows (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row commands). No checksum
list exists to verify against.

*[E]*

manual: ScienceDB 10.57760/sciencedb.15391. Verify the 4,963 + 4,963 file counts.

---

### `buu_lspine_3600` <a id="buu_lspine_3600"></a>

**BUU-LSPINE (3600), the full release (Klinwichit et al., Appl Sci 2023;13:8646).** Cards: D (D02 BUU-LSPINE (3600), the full release), E (buu_lspine_3600). Structured entry: `sources.yaml` id `buu_lspine_3600`; kind upstream_release; status on_disk; re-acquisition manual (manual).

**Source id**

*[D]*

`buu_lspine_3600` (grid directory `buu_full`) (sscn:tools/xray_dataset_usage.py, key `buu`)

*[E]*

`buu_lspine_3600` (family D's id; family D also cards `buu_lspine_2000` at `~/XRSpinoPelvic1K` (HOME, raw, 32.0 GB, listing 2026-08-10); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/spine-detector/data/raw/buu_2000` (HOME, raw), `buu_lspine_drive_mirror` at `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/spine-detector/data/raw/buu_drive` (HOME, raw, 9.3 GB), `buu_lspine_v1_smoke` at `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/spine-detector/data/raw/buu_v1` (HOME, raw) and `buu_lspine_400_sample`, a local folder `ctsp:BUU-LSPINE_400`)

**Name and citation**

*[D]*

Klinwichit P, Yookwan W, Limchareon S, Chinnasarn K, Jang J-S, Onuean A. "BUU-LSPINE: a Thai open lumbar spine dataset
for spondylolisthesis detection." Applied Sciences 2023;13(15):8646, doi:10.3390/app13158646
(sscn:SchwingNet/refs.bib entry `buu2023`). Release page https://services.informatics.buu.ac.th/spine/ and
https://github.com/North-Github/BUU-LSPINE (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row). Note: `sscn:buu.pdf` is a
410-byte "Access Denied" page for https://www.mdpi.com/2076-3417/13/15/8646/pdf, not the paper (read 2026-10-07).

*[E]*

BUU-LSPINE (3600), plus the 2000 and 400 releases, from https://services.informatics.buu.ac.th/spine/ (`DATA_COMPLETENESS_AUDIT.md` release rows).

**Modality**

*[D]*

Plain film (JPEG only, no DICOM), lumbar spine; lateral field L1 to S1, AP field L1-L5
(sscn:docs/PATIENT_IDENTITY_SPEC.md section 2 buu row; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).
Pixel spacing 0.175 mm per the release's `Pixel Spacing` sheet (sscn:docs/FEASIBILITY_REPRODUCE.md).

*[E]*

plain film, lumbar spine.

**Position/view**

*[D]*

AP and lateral, one of each per patient; the digit after `Y` in the file name is the view (0 = AP, 1 = LA)
(sscn:docs/PATIENT_IDENTITY_SPEC.md section 2). Standing radiography (xrsp:README.md, "BUU is standing radiography").

*[E]*

AP and lateral pairs. The 2000 release adds posture labels: flexion/extension 887, rotation 2,310 and side-bending 521 rows (`DATA_COMPLETENESS_AUDIT.md` line 843).

**Licence and access**

*[D]*

"No License Provided" plus an END-USER LICENSE AGREEMENT requiring acknowledgement and forbidding re-identification;
recorded as not open; never redistribute its images or crops (mem:lstv-data-landscape.md;
sdr:runs/review_availability_full/charting_probes/buu-lspine.json, P16 match on 2026-09-19). Full set by Google Form
(mem:lstv-data-landscape.md). Terms for derived labels: not addressed in any file read; treat as non-redistributable.

*[E]*

not recorded.

**How it was acquired**

*[D]*

Google Form request on the release page; "BUU 3600 form pending" on 2026-09-08 (mem:xray-corner-detector-status.md).
The delivery route (Drive link, archive name), the command and any checksum: not recorded. Verification that ran
afterwards: per-view jpg/csv counts and md5 of the seven `(1)` duplicates (sscn:docs/DATA_COMPLETENESS_AUDIT.md
independent re-count).

*[E]*

`download_sources.py` (grid only). The 2000 release was extracted into `~/XRSpinoPelvic1K/data/BUU-LSPINE` on 2026-08-06 (`DATA_COMPLETENESS_AUDIT.md` line 843). A local 400 sample is at `ctsp:BUU-LSPINE_400`.

**When**

*[D]*

2026-09-09 22:50: grid ctime of `~/spine-detector/data/raw/buu_full`, the full v1 re-download (sscn:SchwingNet/results/g0_facts.md §2). The memory note has the form still pending on 2026-09-08 (mem:xray-corner-detector-status.md); the films are in the `~/films_drr` build (directory date 2026-09-13, census:toplevel_listing.txt).

*[E]*

2026-08-06 for the 2000 release (G0 §2: `dataset2024.zip` 2026-08-06 13:43). Family E records no other date; the 3600 set's date above is from g0_facts.md §2.

**What it contains**

*[D]*

- Release: 3,600 patients / 7,200 images (3,600 AP + 3,600 LA), 18.5 GB; jpg + one csv of end-plate line coordinates per film; `KIOM2022_dataset_report.xlsx` with sheets `Pos_AP`, `Pos_LA`, `Normal-Disorder`, `L4L6` (129 four-lumbar, 15 six-lumbar) and `Pixel Spacing` (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row; sscn:docs/FEASIBILITY_REPRODUCE.md).
- On disk: AP 3,600 jpg + 3,600 csv; LA 3,604 jpg + 3,606 csv; seven `(1)` files byte-identical to their originals (md5-proven); 4 orphan files (3 csv without jpg, 1 jpg without csv) (sscn:docs/DATA_COMPLETENESS_AUDIT.md; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).
- Distinct people 3,598-3,600: `0140` = `0719` (both views identical) and `0449` = `0629` (AP identical) (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2).
- Age median 57 [41-67], 63.3 % female (sscn:SchwingNet/tables/tabS3_corpus.md). Bytes on disk: not recorded.

*[E]*

`buu_full` has 3,600 AP and 3,604 LA images. The 3600 release is 18.5 GB (`DATA_COMPLETENESS_AUDIT.md` lines 529, release row).

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/buu_full/BUU-LSPINEv1/{AP, LA, KIOM2022_dataset_report.xlsx}` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).
- HOME converted: `~/films_drr` (3,603 LA files), `~/films_ap_drr` (3,600 AP), `~/films_drr_buucorr` (schema-corrected copy) (sscn:SchwingNet/results/corpus_census.md section 3).
- HOME derived: `~/buu_fov96_ctx`, `~/buu_yolo`, `~/lstv_flag/sources/buu3600_lstv_labels.csv` (census:toplevel_listing.txt; sscn:docs/PATIENT_IDENTITY_SPEC.md section 2).
- No CEPH copy recorded.

*[E]*

`~/buu_yolo` (HOME, converted/derived, listing 2026-09-18); `~/film_style_ds` (HOME, converted/derived, listing 2026-09-17); `~/films_ap_drr` (HOME, converted/derived, listing 2026-09-13); `~/films_drr` (HOME, converted/derived, 36.0 GB, listing 2026-09-13); `~/films_drr_buucorr` (HOME, converted/derived, listing 2026-09-17); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/yolo_levels` (HOME, converted/derived, 6.7 GB, listing 2026-09-13); `~/spine-detector/data/raw/buu_full` (HOME, raw)

**Annotation status**

*[D]*

Release labels: end-plate lines, 11 rows per lateral (L1-L5 superior and inferior, S1 superior), 10 rows per AP; the
level names are inferred from row order, not written by an annotator (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md
section 2.1; sscn:docs/DATASHEET.md section 2.6, "levels assigned by position"). Release LSTV reads are in sheet
`L4L6`. `~/films_drr_buucorr` adds machine schema corrections (`S1a->L6`, `transitional: sacralised`) flagged
`needs_review`; no review verdicts are recorded (sscn:tools/correct_buu_schema.py docstring).

*[E]*

release end-plate lines. Levels are inferred from row order (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1).

**Derived products**

*[D]*

- Shipped level bank `allspine_v9`: 3,603 lateral files, 3,070 train / 533 val (3,600 people) (sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" row).
- AP films only ever in `buu_pair_fov48_ctx`, since deleted (sscn:slurm/disk_cleanup.sh; sscn:docs/DATA_COMPLETENESS_AUDIT.md).
- `buu_fov96_ctx` (3,603, all-train) → `extra_fov96_ctx` → `films_all2_fov96_ctx` (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 3, containment chains).
- C-ArmLSpine fold banks: 589 films as 635 crops (sscn:docs/MODEL_CARD.md section 3.2).
- `~/buu_yolo`: re-implementation of the published five-class baseline (sscn:tools/buu_baseline.py docstring).
- External real-film probe of the LSTV flag on 3,600 LA + 3,600 AP (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md Surface L).
- Person split of 2026-09-23: 3,598 persons, 7,203 images (sscn:SchwingNet/results/corpus_census.md section 0).

*[E]*

10 entries: `~/allspine_fov96_ctx`, `~/allspine_v6_fov96_ctx`, `~/allspine_v7_fov96_ctx`, `~/allspine_v7nofluoro_fov96_ctx`, `~/allspine_v8_fov96_ctx`, `~/allspine_v9_fov96_ctx`, `~/buu_fov96_ctx`, `~/extra_fov96_ctx`, `~/films_all2_fov96_ctx`, `~/mv_bands`

**Known defects and gaps**

*[D]*

- The 3,600 AP films are in no level bank and no valid written criterion excludes them (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Unknown" and re-count sections).
- "3,603 lateral films" is a file count: three are exact copies (1668, 1672, 1673) (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).
- An LSTV call from lumbar films alone is weak (radiography sensitivity 32 %, kappa 0.16-0.32) (mem:lstv-data-landscape.md).
- `films_ap_drr` was never a keyer root (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2).

*[E]*

- `buu_drive` and `buu_v1` are duplicates of `buu_full`.
  - `buu_2000` has the same pixels as `buu_full`, but 1,337 of its CSVs differ (`MANIFEST_DATA_MODELS_RESULTS.md` 7.5).

**Re-acquisition recipe**

*[D]*

Manual: fill the Google Form at https://services.informatics.buu.ac.th/spine/, accept the EULA, download
"BUU-LSPINE(3600)", unpack to `raw/buu_full/BUU-LSPINEv1/`. Verify: AP 3,600 jpg + 3,600 csv, LA 3,604 jpg + 3,606 csv,
the seven `(1)` files md5-identical to their originals, xlsx present; structure check with
`python xrsp:scripts/fetch_buu.py --check <dir>` (both views, jpg/csv pairing, the 11-row L1..S1 chain, decodable
images) (xrsp:scripts/fetch_buu.py docstring). No published checksum list.

*[E]*

manual download from the BUU service page. Verify the file counts per view.

---

### `buu_lspine_2000` <a id="buu_lspine_2000"></a>

**BUU-LSPINE (2000) relabel (mislabelled 'AASCE test split' in tools/xray_dataset_usage.py).** Cards: D (D03 BUU-LSPINE (2000) relabel, mislabelled "AASCE test split"). Structured entry: `sources.yaml` id `buu_lspine_2000`; kind upstream_release; status on_disk; re-acquisition manual (manual).

**Source id**

`buu_lspine_2000` (grid `buu_2000`; `tools/xray_dataset_usage.py` key `buu2000`, wrongly named "AASCE test split")
(sscn:tools/xray_dataset_usage.py; sscn:docs/DATA_COMPLETENESS_AUDIT.md)

**Name and citation**

BUU-LSPINE(2000), the third download listed on https://services.informatics.buu.ac.th/spine/ (2,000 AP+LA pairs,
re-labelled) (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row). Same paper as D02.

**Modality**

Plain film, lumbar AP + lateral; pixels identical to BUU-LSPINE(3600) (sscn:docs/DATA_COMPLETENESS_AUDIT.md;
sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1, buu_2000 row).

**Position/view**

AP and lateral (sscn:docs/XRAY_DATASET_USAGE.md). Posture labels in its report: side-bending (SD), rotation (RT),
flexion/extension (FE) (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).

**Licence and access**

As D02 (same distributor and EULA) (mem:lstv-data-landscape.md). The XRSP1K repo states "BUU is not redistributable
here" (xrsp:.gitignore).

**How it was acquired**

Downloaded as `dataset2024.zip` (4,023,726,207 B) and extracted on the grid to `~/XRSpinoPelvic1K/data/BUU-LSPINE` on
2026-08-06 (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count). The same-sized file is on LOCAL at `xrsp:dataset2024.zip`,
4,023,726,207 B, file date 2026-08-06 13:43 (ls, 2026-10-07). Download URL and checksum: not recorded.

**When**

2026-08-06 (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count; file date of xrsp:dataset2024.zip).

**What it contains**

4,000 jpg + 4,000 csv + `Dataset Report.xlsx`; every jpg name is in `buu_full`; 1,337 of 4,000 csv differ in column 5
(flag codes 5-10 against 1-4/20-21); posture sheets FE 887 / RT 2,310 / SD 521 rows
(sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).

**Where it is now**

- HOME raw: `~/XRSpinoPelvic1K/data/BUU-LSPINE` (extracted) and `~/XRSpinoPelvic1K/data/dataset2024.zip`; `~/spine-detector/data/raw/buu_2000` is a symlink to the former (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row and re-count).
- LOCAL: `xrsp:dataset2024.zip`.

**Annotation status**

Release labels (end-plate lines as D02, plus a second vintage of flag codes and posture diagnoses). Used by no bank
(sscn:docs/DATA_COMPLETENESS_AUDIT.md).

**Derived products**

- spine-detector corpus of 2026-09-07: "BUU-LSPINE 2000-pair subset" 19,991 vertebra instances (mem:xray-corner-detector-status.md).
- XRSpinoPelvic1K YOLO-pose baseline and BUU validation (`scripts/buu_to_yolo.py`, `scripts/train_corners_buu.py`, `scripts/evaluate_buu.py`; git commit b5e94a2 on 2026-08-08) (xrsp: git log).

**Known defects and gaps**

- Mislabelled in `tools/xray_dataset_usage.py`, and so in `docs/XRAY_DATASET_USAGE.md`, as "AASCE test split | report spreadsheet only" (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Unknown" row).
- `MANIFEST` line 773 called the zip "4.7 GB, never opened"; it is 4.0 GB and already extracted (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).
- Posture labels shipped and unused, never written off (same).

**Re-acquisition recipe**

Manual from the BUU release page (as D02), or copy LOCAL `xrsp:dataset2024.zip` to the grid through WSL (the
CLAUDE.md network rule). Verify: 4,023,726,207 B; `unzip -l` lists 4,000 jpg + 4,000 csv + `Dataset Report.xlsx`; every
jpg name present in `buu_full` (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).

---

### `buu_lspine_400_sample` <a id="buu_lspine_400_sample"></a>

**BUU-LSPINE (400) public sample.** Cards: D (D04 BUU-LSPINE (400) public sample). Structured entry: `sources.yaml` id `buu_lspine_400_sample`; kind upstream_release; status local_only; re-acquisition manual (manual).

**Source id**

`buu_lspine_400_sample`

**Name and citation**

BUU-LSPINE(400)_sample, the public sample listed on https://services.informatics.buu.ac.th/spine/ (400 AP+LA pairs with
edge coordinates and 4 listhesis diagnoses) (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row). Same paper as D02.

**Modality**

Plain film, lumbar AP + lateral (sscn:docs/DATA_COMPLETENESS_AUDIT.md).

**Position/view**

AP and lateral (file suffixes Y0 / Y1) (ls of ctsp:BUU-LSPINE_400/AP and /LA, 2026-10-07).

**Licence and access**

As D02; the sample is offered on the release page / Drive (mem:lstv-data-landscape.md, "400-pair and 2,000-pair samples
on Drive").

**How it was acquired**

Manual download; command not recorded. XRSpinoPelvic1K stages it from a local archive with
`python scripts/fetch_buu.py --zip BUU-LSPINE_400.zip --out data/BUU-LSPINE_400` (xrsp:scripts/fetch_buu.py, git commit
c8606f0, 2026-08-06).

**When**

LOCAL file dates 2026-06-24 (`AP/`, `LA/`, `BUU-LSPINE_400_report.xlsx`) (ls of ctsp:BUU-LSPINE_400, 2026-10-07).

**What it contains**

LOCAL folder: 1,603 files, 889 MB: 400 AP jpg + 400 AP csv, 400 LA jpg + 400 LA csv (ids 0001-0501),
`BUU-LSPINE_400_report.xlsx`, a stray `bash.exe.stackdump` and `desktop.ini`; every name is in the grid's `buu_full`
(sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row; find/du, 2026-10-07).

**Where it is now**

- LOCAL: `ctsp:BUU-LSPINE_400` (untracked; `??` in the CTSpinoPelvic1K-1 git status).
- HOME: whether `~/XRSpinoPelvic1K/data/BUU-LSPINE_400` exists is not recorded (xrsp:.gitignore names that path).

**Annotation status**

Release labels: reader-placed corners, used as the real-film reference band for XRSpinoPelvic1K's corner convention
(xrsp:README.md, "Validation against real reader annotations").

**Derived products**

XRSpinoPelvic1K `scripts/buu_convention.py` reader-band comparison (xrsp:README.md).

**Known defects and gaps**

A pixel subset of `buu_full`; the CTSpinoPelvic1K-1 copy is referenced by no code (sscn:docs/DATA_COMPLETENESS_AUDIT.md
"Unknown" row, which recommends delete or archive).

**Re-acquisition recipe**

Redundant with D02 (all names are in `buu_full`). If wanted: manual download of the sample from the BUU page, then
`python xrsp:scripts/fetch_buu.py --zip <archive> --out <dir>` and `--check <dir>`.

---

### `buu_lspine_drive_mirror` <a id="buu_lspine_drive_mirror"></a>

**BUU-LSPINE Google Drive mirror (deleted).** Cards: D (D05 BUU-LSPINE Google Drive mirror (deleted)). Structured entry: `sources.yaml` id `buu_lspine_drive_mirror`; kind upstream_release; status deleted; re-acquisition manual (none).

**Source id**

`buu_lspine_drive_mirror` (grid `buu_drive`)

**Name and citation**

A Google Drive copy of BUU-LSPINE (sscn:docs/DATASHEET.md section 2.5). Same paper as D02.

**Modality**

Plain film, lumbar AP + lateral (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).

**Position/view**

AP and lateral (same).

**Licence and access**

As D02. Google Drive caps folder downloads, so it arrived partially (sdet:src/build_dataset.py docstring).

**How it was acquired**

Google Drive folder download; tool and command not recorded (sdet:src/build_dataset.py docstring).

**When**

Not recorded.

**What it contains**

5,495 images (10,990 files), 9.3 GB; a byte-identical subset of `buu_full` (md5 over all 10,990 shared files, 0
mismatches) (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).

**Where it is now**

Deleted: `slurm/disk_cleanup.sh` drops `$H/spine-detector/data/raw/buu_drive` as a "byte-identical subset of buu_full"
(sscn:slurm/disk_cleanup.sh, committed 2026-09-17); `ls` on 2026-09-23 found no such directory
(sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count). The date the deletion ran is in
`~/model_night/logs/disk_cleanup_manifest.txt` (grid only; not read).

**Annotation status**

Release labels (as D02).

**Derived products**

None (sscn:docs/XRAY_DATASET_USAGE.md, "BUU Drive mirror ... 0").

**Known defects and gaps**

Still described as "on disk, excluded" in DATASHEET section 2.5, XRAY_DATASET_USAGE and the RAW list of
`tools/xray_dataset_usage.py` (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).

**Re-acquisition recipe**

Do not re-acquire: fully contained in D02 (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).

---

### `buu_lspine_v1_smoke` <a id="buu_lspine_v1_smoke"></a>

**BUU v1 download smoke test (38 images).** Cards: D (D06 BUU v1 download smoke test). Structured entry: `sources.yaml` id `buu_lspine_v1_smoke`; kind upstream_release; status on_disk; re-acquisition manual (none).

**Source id**

`buu_lspine_v1_smoke` (grid `buu_v1`)

**Name and citation**

A 38-image test download of BUU-LSPINE (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1). Same paper as D02.

**Modality**

Plain film, lumbar (same).

**Position/view**

Lateral and AP mixed (sdet:report/manifest.parquet: BUU 38 films, 190 instances, views LAT and AP).

**Licence and access**

As D02.

**How it was acquired**

"Download smoke test" (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1); command not recorded. Read by `do_buu()`
of the spine-detector builder (sdet:src/build_dataset.py).

**When**

2026-09-01 23:28: grid ctime of `~/spine-detector/data/raw/buu_v1`, the smoke test (sscn:SchwingNet/results/g0_facts.md §2). sdet:report/manifest.parquet (file date 2026-09-02 00:26) already holds its 38 films.

**What it contains**

38 images (77 files), all byte-identical to `buu_full` (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).

**Where it is now**

HOME raw: `~/spine-detector/data/raw/buu_v1` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).

**Annotation status**

Release labels (as D02; `level_source` = `inferred_from_position`) (sdet:report/manifest.parquet).

**Derived products**

The early spine-detector manifest only (sdet:report/manifest.parquet).

**Known defects and gaps**

Duplicate of D02.

**Re-acquisition recipe**

Do not re-acquire (contained in D02).

---

### `nhanes2_cdc_films` <a id="nhanes2_cdc_films"></a>

**NHANES II (1976-1980) digitised cervical and lumbar spine films (NCHS).** Cards: D (D07 NHANES II digitised spine films (CDC release)), E (nhanes2_cdc_films). Structured entry: `sources.yaml` id `nhanes2_cdc_films`; kind upstream_release; status on_disk; re-acquisition run (http).

**Source id**

*[D]*

`nhanes2_cdc_films` (grid `nhanes_full`) (sscn:tools/xray_dataset_usage.py, key `nhanes`)

*[E]*

`nhanes2_cdc_films` (family D's id for the CDC films; the annotated subset is family D's `nhanes2_zenodo_landmarks`, located at: `~/film_style_ds` (HOME, converted/derived, listing 2026-09-17); `~/films_drr` (HOME, converted/derived, 36.0 GB, listing 2026-09-13); `~/films_drr_buucorr` (HOME, converted/derived, listing 2026-09-17); `~/nhanes_drr` (HOME, converted/derived, listing 2026-09-12); `~/pseudo_filtered` (HOME, converted/derived, listing 2026-09-17); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/verse_only_ctx_plus_nh` (HOME, converted/derived, listing 2026-09-13); `~/yolo_levels` (HOME, converted/derived, 6.7 GB, listing 2026-09-13); `~/spine-detector/data/raw/nhanes_annotated` (HOME, raw, 159.0 GB))

**Name and citation**

*[D]*

NHANES II (1976-1980) digitised cervical and lumbar spine X-ray films, National Center for Health Statistics. Release
page https://wwwn.cdc.gov/nchs/data/nhanes2/NH2_Xray.htm ("The current release includes 17,075 files"); file index
https://ftp.cdc.gov/pub/NHANES/XRays/Nhanes2/ (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row;
sscn:slurm/audit_nhanes_missing.sh `BASE`). The NLM mirror https://data.lhncbc.nlm.nih.gov/public/NHANES/ answered HTTP
403 on 2026-09-19 (sdr:runs/review_availability_full/charting_probes/nhanes-ii-films.json). Films acquired 1976-80 and
released digitally later (sdr:PROTOCOL.md, criterion I5 note).

*[E]*

NHANES II digitised spine films from the CDC (https://wwwn.cdc.gov/nchs/data/nhanes2/NH2_Xray.htm). The annotations are Zenodo 10223910 (`DATA_COMPLETENESS_AUDIT.md` release rows).

**Modality**

*[D]*

Plain film (digitised survey film, 16-bit TIFF); cervical and lumbar spine (sscn:docs/DATA_COMPLETENESS_AUDIT.md
release row). A national survey corpus, not a clinical one (sscn:docs/DATASHEET.md section 2.6).

*[E]*

plain film, cervical and lumbar.

**Position/view**

*[D]*

Lateral (sscn:docs/XRAY_DATASET_USAGE.md). Patient posture: not recorded.

*[E]*

lateral (`XRAY_DATASET_USAGE.json`).

**Licence and access**

*[D]*

US government work, public domain, open download (sdr:licence_tiers.csv row "US government works (NHANES, NLM)";
mem:lstv-data-landscape.md "US public domain"). Derived labels unrestricted.

*[E]*

the annotations are CC BY 4.0. The licence of the CDC films is not recorded.

**How it was acquired**

*[D]*

`slurm/download_nhanes_full.sh` (a grid-only script, absent from the local repo): a resumable curl loop over the CDC
index with a non-empty-file test; job 40194954 (log `logs/dl_nhanes_40194954.out`, "tiff on disk : 17073 of ...").
It resubmitted itself on two failures and was scancelled on 2026-09-11 with `.failcount = 2` and no completion marker
(sscn:docs/DATA_COMPLETENESS_AUDIT.md NHANES gap row and on-disk row). `nhanes_full/.download_complete` was written
with the reason on 2026-09-23 by `slurm/film_corpus_inventory.sh` (job 40416535) (sscn:slurm/film_corpus_inventory.sh;
sscn:SchwingNet/results/repairs/nhanes-vindr_CHECK.md section 5). Verification: non-empty test and the count against
`.filelist.txt` (the CDC index); no checksum is published or recorded.

*[E]*

a download loop over the CDC index, `logs/dl_nhanes_40194954.out`, which writes a `.download_complete` marker (`DATASHEET.md` 2.6; `DATA_COMPLETENESS_AUDIT.md` line 532).

**When**

*[D]*

The full 17,073-film set landed from 2026-09-09 13:03 (grid ctime), and its `.download_complete` is dated 2026-09-23 03:00 (sscn:SchwingNet/results/g0_facts.md §2; the marker was written by sscn:slurm/film_corpus_inventory.sh, sscn:SchwingNet/results/repairs/nhanes-vindr_CHECK.md section 5). Event: the download loop was cancelled on 2026-09-11 (sscn:docs/DATA_COMPLETENESS_AUDIT.md).

*[E]*

not recorded in family E's evidence (the dates above are from g0_facts.md §2).

**What it contains**

*[D]*

17,075 index entries = 9,667 cervical + 7,408 lumbar; 17,073 TIFF on disk = 9,667 C + 7,406 L, 91 GB, smallest
1.5 MB; `L00452.tiff` and `L00456.tiff` are served by the CDC as HTTP 200 with Content-Length 0 (Last-Modified
2025-08-14) (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row and Repairs). 9,698 sample persons over the 17,073 films
(sscn:docs/DATA_COMPLETENESS_AUDIT.md Repairs, job 40416535); the 2026-09-23 split holds 9,581 persons and 16,272 images
(sscn:SchwingNet/results/corpus_census.md section 0). Age median 55 [37-65], 51.8 % female, joined from the CDC public-use
tape 5301 by sequence number (sscn:SchwingNet/tables/tabS3_corpus.md).

*[E]*

17,073 TIFF of 91 GB (`nhanes_full`) and 543 annotated pickles of 159 GB (`nhanes_annotated`) (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1; `DATA_COMPLETENESS_AUDIT.md` lines 532-533).

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/nhanes_full/*.tiff` plus `.filelist.txt`, `.failcount`, `.download_complete` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).
- HOME derived: `~/nhanes_pseudo`, `~/pseudo_filtered/nhanes_pseudo_anchored`, `~/nhanesps_fov96_ctx`, `~/review_pack` (census:toplevel_listing.txt).
- CEPH derived: `$RS/data/inventory/films/nhanes_film_manifest.csv` (17,075 rows) and `FILM_CORPUS_INVENTORY.md` (sscn:docs/DATA_COMPLETENESS_AUDIT.md Repairs; sscn:SchwingNet/results/repairs/nhanes-vindr_CHECK.md).

*[E]*

`~/film_style_ds` (HOME, converted/derived, listing 2026-09-17); `~/films_drr` (HOME, converted/derived, 36.0 GB, listing 2026-09-13); `~/films_drr_buucorr` (HOME, converted/derived, listing 2026-09-17); `~/nhanes_pseudo` (HOME, converted/derived, listing 2026-09-16); `~/nhanes_pvariant_strata.json` (HOME, converted/derived, listing 2026-09-17); `~/pseudo_filtered` (HOME, converted/derived, listing 2026-09-17); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/verse_only_ctx_plus_nh` (HOME, converted/derived, listing 2026-09-13); `~/yolo_levels` (HOME, converted/derived, 6.7 GB, listing 2026-09-13); `~/spine-detector/data/raw/nhanes_full` (HOME, raw, 91.0 GB)

**Annotation status**

*[D]*

None in the release; pseudo-labels for most films. 543 films carry landmarks from the separate Zenodo deposit (card D08). Pseudo-labels:
`~/nhanes_pseudo` 16,234 anns, 15,746 with at least one named level; per film: 542 annotated, 15,253 pseudo-named,
476 boxes without a name, 802 never pseudo-labelled (sscn:docs/DATA_COMPLETENESS_AUDIT.md Repairs, job 40416623).
Student review pack of 1,500 films drawn from `nhanes_pseudo` + `lateral236_pseudo` (HF Space
`gregoryschwingmdphd/level-review`); verdicts not recorded (sscn:slurm/review_pack.sh).

*[E]*

543 films have expert landmarks, and 16,234 are pseudo-labelled (`XRAY_DATASET_USAGE.json`).

**Derived products**

*[D]*

- `nhanesps_fov96_ctx` (15,746 films) → `allspine_v5` (deleted 2026-09-20) (sscn:slurm/corpus_expand.sh; mem:grid-quota-and-deleted-banks.md).
- `pseudo_filtered/nhanes_pseudo_anchored` (10,087) → anchored-admission arm, refuted (sscn:SchwingNet/results/corpus_census.md section 3; mem:remedies-refuted-2026-09-17.md).
- Film-look LoRA set `~/film_style_ds` (sscn:tools/film_style_dataset.py).

*[E]*

11 entries: `~/allspine_fov96_ctx`, `~/allspine_v6_fov96_ctx`, `~/allspine_v7_fov96_ctx`, `~/allspine_v7nofluoro_fov96_ctx`, `~/allspine_v8_fov96_ctx`, `~/allspine_v9_fov96_ctx`, `~/films_all2_fov128m_ctx`, `~/films_all2_fov96_ctx`, `~/films_ann_fov96_ctx`, `~/mv_bands`, `~/nhanesps_fov96_ctx`

**Known defects and gaps**

*[D]*

- 2 of 17,075 entries are empty at the source; nothing to fetch (sscn:docs/DATASHEET.md section 2.6).
- 16,531 unannotated films are in no trained bank and were never offered to the detector; the level-bank exclusion is written and measured (pseudolabels cost about 19-20 points of anomalous accuracy), the detector exclusion is not (sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row; mem:remedies-refuted-2026-09-17.md).
- Directive D2 orders all ~17,000 films onto CephFS and into detection self-training; not done (sscn:docs/RESUME_2026-09-22_PM.md "D2").
- `nhanes_pseudo` names carried no scheme and were refused by the old keyer; the `NHANESPS_([CL])(\d+)` rule now exists (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2).

*[E]*

- L00452 and L00456 are zero bytes at the source (`DATASHEET.md` 2.6).
  - NHANES sits in two banks under two spellings (`mem:nhanes-double-inclusion`).

**Re-acquisition recipe**

*[D]*

Programmatic (no account). The script that ran (`slurm/download_nhanes_full.sh`) is not in the local repo; an
equivalent, proposed here and not yet run:
```
BASE=https://ftp.cdc.gov/pub/NHANES/XRays/Nhanes2/
DST=$RS/data/films/nhanes2/raw ; mkdir -p "$DST"
curl -sS --fail "$BASE" -o "$DST/.index.html"
grep -o -E '[CL][0-9]{5}\.tiff' "$DST/.index.html" | sort -u > "$DST/.filelist.txt"     # expect 17,075
while read f; do [ -s "$DST/$f" ] || curl -sS --fail --retry 5 -C - -o "$DST/$f" "$BASE$f"; done < "$DST/.filelist.txt"
```
Run it as an sbatch job (compute nodes have internet; nothing on the login node). Verify: 17,073 non-empty TIFF
(9,667 C, 7,406 L), exactly `L00452` and `L00456` empty at source (HEAD shows Content-Length 0), smallest file
>= 1.5 MB (sscn:docs/DATA_COMPLETENESS_AUDIT.md; sscn:slurm/audit_nhanes_missing.sh for the HEAD check).

*[E]*

download the CDC index at https://ftp.cdc.gov/pub/NHANES/XRays/Nhanes2/, check non-empty files against `.filelist.txt` (two entries are known to be empty), and get Zenodo 10223910 with its md5.

---

### `nhanes2_zenodo_landmarks` <a id="nhanes2_zenodo_landmarks"></a>

**NHANES II spinal X-ray with extra labels (Mo, Papiez, Chen, Mandal, Jabbar; Zenodo).** Cards: D (D08 NHANES II annotated subset (Zenodo pickles)). Structured entry: `sources.yaml` id `nhanes2_zenodo_landmarks`; kind upstream_release; status on_disk; re-acquisition run (zenodo_http).

**Source id**

`nhanes2_zenodo_landmarks` (grid `nhanes_annotated`)

**Name and citation**

Mo Y, Papiez BW, Chen Y, Mandal I, Jabbar F. "NHANES II spinal X-ray with extra labels for reference vertebral bodies
(C2, S1)." Zenodo, 2023-11-30, doi:10.5281/zenodo.10223910 (concept doi:10.5281/zenodo.10145564), CC BY 4.0
(sscn:SchwingNet/refs.bib entry `nhanes`). Method paper: Chen Y et al. "VertXNet." Scientific Reports 2024;14:3341,
doi:10.1038/s41598-023-49923-3 (sscn:paper/rsnai/refs.bib entry `vertxnet2024`).

**Modality**

Plain film (the NHANES II films of D07) with per-vertebra binary masks, stored as Python pickles holding the full
frame (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1; sscn:tools/nhanes_to_drr_format.py docstring).

**Position/view**

Lateral, cervical and lumbar (sscn:docs/XRAY_DATASET_USAGE.md).

**Licence and access**

CC BY 4.0, open download (sscn:SchwingNet/refs.bib comment; sscn:docs/DATA_COMPLETENESS_AUDIT.md release row).

**How it was acquired**

Zenodo download of `NHANESII_Annotations_VertebralOsetophytes.zip` (1,017,496,285 B) into
`raw/nhanes_annotated/`, then extracted (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row; sdet:src/build_dataset.py
`do_nhanes`). Command not recorded. Verification later: `unzip -l` lists 544 entries (543 pkl + 1 dir) and
zip-against-disk comparison found 0 unextracted (job 40416364) (sscn:docs/DATA_COMPLETENESS_AUDIT.md).

**When**

2026-09-01 23:28: grid ctime of `~/spine-detector/data/raw/nhanes_annotated/NHANESII_Annotations_VertebralOsetophytes.zip` and its `.download_complete` (sscn:SchwingNet/results/g0_facts.md §2). The local spine-detector manifest dated 2026-09-02 00:26 already holds 543 NHANES films / 3,217 instances (sdet:report/manifest.parquet).

**What it contains**

543 pkl (275 cervical + 268 lumbar) over 364 sample persons (179 with one of each); mask keys: a combined `vertebrae`
mask (excluded by the converter), `C2`-`C7`, `T1`, `T11`, `T12`, `L1`-`L5`, `S1`, and `C2_lower` in 272 films
(sscn:docs/DATA_COMPLETENESS_AUDIT.md release row and Repairs). Extracted pickles take 159 GB because masks are float64
full frames (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1). Annotated persons: age median 65 [62-69], 55.2 %
female (sscn:SchwingNet/tables/tabS3_corpus.md note c).

**Where it is now**

- HOME raw: `~/spine-detector/data/raw/nhanes_annotated/{NHANESII_Annotations_VertebralOsetophytes.zip, extracted/nhanes/*.pkl}` (sscn:docs/DATA_COMPLETENESS_AUDIT.md).
- HOME converted: `~/nhanes_drr` (543) and the `nhanes` part of `~/films_drr` (543) (sscn:SchwingNet/results/corpus_census.md section 3).
- CEPH derived: `$RS/data/inventory/films/box_convention/` (9 files) (sscn:SchwingNet/results/repairs/nhanes-vindr_CHECK.md).

**Annotation status**

Release labels: per-level masks keyed by name, the only real-film corpus here whose level names were annotated rather
than counted (sscn:tools/nhanes_to_drr_format.py docstring). The boxes were measured to be vertebral-body boxes
(median width over height 1.01; renders show body-only quadrilaterals) (sscn:docs/DATA_COMPLETENESS_AUDIT.md Repairs, job
40416559).

**Derived products**

- `~/nhanes_drr` via `tools/nhanes_to_drr_format.py` (`slurm/nhanes_build.sh`) → `nhanes_ctx` (543, pure test bank), `nhanes_split_ctx`, `verse_only_ctx_plus_nh` (sscn:slurm/nhanes_build.sh; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 3).
- `~/films_drr` (source `nhanes`) via `tools/manifest_to_drr_format.py` → `films_ann_fov96_ctx`, `films_all2`, `allspine_*`; in the shipped `allspine_v9`: 464 train / 79 val, 364 people (sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" row).
- spine-detector corpus 3,217 instances; detector set `yolo_v2` NHANES 443 / 50 / 50 (mem:xray-corner-detector-status.md; sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).
- Manuscript naming figure "NHANES II 99.1 %" on the `allspine_v8` selection split (sscn:SchwingNet/packet_src/statements.md item 6).

**Known defects and gaps**

- Entered banks v2, v6 and v7 twice (`films_drr` and `nhanes_drr`) under two names split independently: 48 of 54 validation patients had their copy in training (sscn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md; mem:nhanes-double-inclusion.md).
- The Zenodo page says 600 annotated, VertXNet says 544, the zip ships 543; the missing 57 were never asked for (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).
- `L00452` has no TIFF (card D07); its pixels survive only inside this pickle (sscn:docs/DATASHEET.md section 2.6).

**Re-acquisition recipe**

Programmatic: `curl -sS https://zenodo.org/api/records/10223910` lists the files with md5 checksums; download
`NHANESII_Annotations_VertebralOsetophytes.zip` from the record's file link and verify the API md5, size
1,017,496,285 B, and `unzip -l` = 544 entries (543 pkl: 275 `C*`, 268 `L*`) (sscn:docs/DATA_COMPLETENESS_AUDIT.md).

---

### `vindr_spinexr` <a id="vindr_spinexr"></a>

**VinDr-SpineXR (Nguyen et al., MICCAI 2021).** Cards: D (D09 VinDr-SpineXR), E (vindr_spinexr). Structured entry: `sources.yaml` id `vindr_spinexr`; kind upstream_release; status on_disk; re-acquisition manual (physionet_wget).

**Source id**

*[D]*

`vindr_spinexr` (sscn:tools/xray_dataset_usage.py, key `vindr`)

*[E]*

`vindr_spinexr` (family D's id)

**Name and citation**

*[D]*

Nguyen HT, Pham HH, Nguyen NT, Nguyen HQ, Huynh TQ, Dao M, Vu V. "VinDr-SpineXR: a deep learning framework for spinal
lesions detection and classification from radiographs." MICCAI 2021, LNCS 12905:291-301,
doi:10.1007/978-3-030-87240-3_28 (sscn:SchwingNet/refs.bib entry `vindr`); data paper arXiv:2106.12930
(sdr:manuscript/refs.bib entry `nguyen2021vindr`). Release https://physionet.org/content/vindr-spinexr/1.0.0/
(sscn:docs/DATA_COMPLETENESS_AUDIT.md release row). No Kaggle route is recorded anywhere in the files read.

*[E]*

VinDr-SpineXR v1.0.0, https://physionet.org/content/vindr-spinexr/1.0.0/ (`DATA_COMPLETENESS_AUDIT.md` release row).

**Modality**

*[D]*

Plain film (DICOM, `.dicom` extension), spine radiographs, cervical and lumbar mixed; view and region tags stripped
(sscn:docs/DATA_COMPLETENESS_AUDIT.md release row; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).

*[E]*

DICOM plain film of mixed region.

**Position/view**

*[D]*

AP and lateral mixed; no view field in the release (a view classifier was used to pick laterals)
(sscn:docs/XRAY_DATASET_USAGE.md; sscn:slurm/vindr_pseudolabel.sh).

*[E]*

AP and lateral. The DICOM tags are stripped (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1).

**Licence and access**

*[D]*

PhysioNet credentialed access under the PhysioNet Restricted Health Data License and Use Agreement 1.5.0, signed by a
named person; outside WSU IRB determination 2026-269 and covered by its supplement HPR 2026-330 (notice 2026-09-29, not human participant research)
(sscn:SchwingNet/packet_src/statements.md rows 25 and 61; sscn:slurm/reproduce_all.sh header). It stays on the grid
and is never redistributed (mem:xray-corner-detector-status.md). Terms for derived labels: not recorded locally.

*[E]*

PhysioNet. The access tier is not recorded in Family E's evidence, although an `IRB_VinDr_2026-09-25` folder exists at `ctsp:`.

**How it was acquired**

*[D]*

Credentialed PhysioNet download; the route recorded is
`wget -r -N -c -np --user <physionet-id> --ask-password https://physionet.org/files/vindr-spinexr/1.0.0/`
(sscn:docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md); the exact command and whose credential: not recorded
("downloading under its DUA" on 2026-09-08, mem:xray-corner-detector-status.md). Verification: all 10,466 files
checked against `SHA256SUMS.txt`, 0 mismatches (job 40416364) (sscn:docs/DATASHEET.md section 2.6;
sscn:docs/DATA_COMPLETENESS_AUDIT.md Repairs).

*[E]*

`download_sources.py` (grid only). The SHA256SUMS were verified, with 0 mismatches (`DATASHEET.md` 2.6).

**When**

*[D]*

Started by 2026-09-07 17:49 (grid ctime of `LICENSE.txt` and `SHA256SUMS.txt` under `~/spine-detector/data/raw/vindr/1.0.0`; sscn:SchwingNet/results/g0_facts.md §2); completed 2026-09-10: `.missing.txt` written 17:20, `.download_complete` 17:25 (sscn:docs/DATA_COMPLETENESS_AUDIT.md gap row).

*[E]*

not recorded in family E's evidence (the dates above are from g0_facts.md §2).

**What it contains**

*[D]*

10,466 images / 5,000 studies: 8,389 train (4,000 studies) + 2,077 test (1,000 studies); 0 files under 50 kB; 48 GB;
`annotations/{train,test}.csv` with `study_id, series_id, image_id` and lesion boxes; 5,136 images carry a lesion box,
5,330 are "No finding" only (sscn:docs/DATA_COMPLETENESS_AUDIT.md release, on-disk and Repairs). Lesion rows 24,298
in 8 finding classes (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1) against "13 classes" in the audit's release
row (sscn:docs/DATA_COMPLETENESS_AUDIT.md); the two disagree. PatientID, PatientName, AccessionNumber and StudyDate are
absent from all headers, so the study is the finest unit (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2). Age median 49
[38-59] (n = 1,746 headers with age), 62.3 % female (sscn:SchwingNet/tables/tabS3_corpus.md).

*[E]*

10,466 images from 5,000 studies, 48 GB (`DATA_COMPLETENESS_AUDIT.md` line 534).

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/vindr/1.0.0/{train_images, test_images, annotations, SHA256SUMS.txt, .download_complete}` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).
- CEPH derived: `$RS/data/vindr/identity/vindr_image_to_study.json` (10,466 rows; a second copy is written to the grid checkout `~/spinesurg-ct-nnunet/tools/identity/vindr_image_to_study.json`, absent from the local checkout), `$RS/data/vindr/audit/missing_2026-09-10_stale.txt`, `$RS/data/inventory/films/vindr_film_manifest.csv` (sscn:slurm/vindr_identity_export.sh; sscn:SchwingNet/results/repairs/nhanes-vindr_CHECK.md sections 2 and 5).
- HOME derived: `~/vindr_det_drr`, `~/vindr_pseudo_drr`, `~/vindr_pseudo`, `~/vindr_fov96_ctx`, `~/vindrps_fov96_ctx`, `~/pseudo_filtered/vindr_pseudo_anchored`, `~/vindr_views.csv`, `~/vindr_lat_ids.txt`, `~/model_night/vindr_smoke` (census:toplevel_listing.txt; sscn:SchwingNet/results/corpus_census.md section 3).

*[E]*

`~/pseudo_filtered` (HOME, converted/derived, listing 2026-09-17); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/vindr_det_drr` (HOME, converted/derived, listing 2026-09-13); `~/vindr_lat_ids.txt` (HOME, converted/derived, listing 2026-09-13); `~/vindr_pseudo` (HOME, converted/derived, listing 2026-09-16); `~/vindr_pseudo_drr` (HOME, converted/derived, listing 2026-09-13); `~/vindr_variant_audit.json` (HOME, converted/derived, listing 2026-09-17); `~/vindr_views.csv` (HOME, converted/derived, listing 2026-09-13); `$RS/data/vindr` (CEPH, converted/derived, listing 2026-09-23); `~/spine-detector/data/raw/vindr/1.0.0` (HOME, raw, 48.0 GB)

**Annotation status**

*[D]*

Release labels: lesion boxes only, no vertebra levels (sscn:docs/XRAY_DATASET_USAGE.md). Pseudo-labels:
`~/vindr_pseudo` 10,274 ann files, 7,625 with a named level, 2,649 with an empty levels dict; 192 images never
pseudo-labelled (sscn:docs/DATASHEET.md section 2.6). The "Surgical implant" lesion boxes trained the hardware
detector (mem:fluorocap-dataset.md, "Implant detector ... from VinDr Surgical implant boxes").

*[E]*

release lesion boxes only. Levels are pseudo-labelled on 10,274 images (`DATASHEET.md` 2.6).

**Derived products**

*[D]*

- Old lateral-only route: view classifier p_lateral > 0.9 → `vindr_det_drr` (2,328, no names) → `vindr_pseudo_drr` (744) → `vindr_fov96_ctx` (744 films / 3,679 crops) → `extra`, `films_all2`, `allspine_v3/v4` (sscn:docs/DATASHEET.md section 2.6; sscn:slurm/vindr_pseudolabel.sh).
- `~/vindr_pseudo` (via `slurm/vindr_label.sh`, both splits) → `vindrps_fov96_ctx` (7,625 films / 43,244 crops) → `allspine_v7`; C-ArmLSpine fold banks 2,071 films / 2,632 crops (1,784 studies) (sscn:slurm/vindr_label.sh; sscn:docs/DATA_COMPLETENESS_AUDIT.md Repairs).
- `allspine_v8` / `allspine_v9` (the shipped bank): 0 films (sscn:docs/DATASHEET.md section 2.6).
- `~/FluoroCap/hardware_det_v1.pt` (mAP50 0.42 on VinDr) (mem:fluorocap-dataset.md).
- Person split of 2026-09-23: 4,981 studies, 10,274 images (sscn:SchwingNet/results/corpus_census.md section 0).

*[E]*

6 entries: `~/allspine_v7_fov96_ctx`, `~/allspine_v7nofluoro_fov96_ctx`, `~/extra_fov96_ctx`, `~/films_all2_fov96_ctx`, `~/vindr_fov96_ctx`, `~/vindrps_fov96_ctx`

**Known defects and gaps**

*[D]*

- The release's designated test split was consumed for training pseudo-labels, which forecloses VinDr as a held-out benchmark (sscn:docs/DATASHEET.md section 2.6).
- The 744-film route ran over the 5,136 lesion-box images only; the 5,330 normal films never reached the view classifier (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).
- `vindrps_fov96_ctx` puts 1,199 of 1,541 val cases next to a same-study sibling in train (77.8 %; computed on cases, 391 of which have no crop) (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2; sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count).
- `pseudolabel_report.json` was overwritten by the test pass (says 2,077) (sscn:docs/DATA_COMPLETENESS_AUDIT.md).
- VinDr crops sit in the C-ArmLSpine fold models (IRB: covered by HPR 2026-330 since 2026-09-29; the open defect is the fold-model lineage, not the determination) (sscn:SchwingNet/packet_src/statements.md item 5).

*[E]*

the release's test split was consumed for pseudo-labels (`DATASHEET.md` 2.6).

**Re-acquisition recipe**

*[D]*

Manual step first: PhysioNet credentialing (CITI training) and signing the DUA for vindr-spinexr 1.0.0
(sscn:docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md). Then, programmatic, as an sbatch job:
`wget -r -N -c -np --user <physionet-id> --ask-password https://physionet.org/files/vindr-spinexr/1.0.0/` and
`sha256sum -c SHA256SUMS.txt` (expect 0 mismatches), 8,389 train + 2,077 test `.dicom`, csv-to-disk one-to-one
(sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count). Rebuild the study map with `slurm/vindr_identity_export.sh`.

*[E]*

manual PhysioNet download, then `sha256sum -c SHA256SUMS.txt`.

---

### `aasce2019_boostnet` <a id="aasce2019_boostnet"></a>

**AASCE 2019 / BoostNet AP spine films (Wu et al. MICCAI 2017; Wang et al. MedIA 2021).** Cards: D (D10 AASCE 2019 / BoostNet AP spine films), E (aasce2019_boostnet). Structured entry: `sources.yaml` id `aasce2019_boostnet`; kind upstream_release; status on_disk; re-acquisition run (thoracic_xr_fetch).

**Source id**

*[D]*

`aasce2019_boostnet` (sscn:tools/xray_dataset_usage.py, key `aasce`)

*[E]*

`aasce2019_boostnet` (family D's id)

**Name and citation**

*[D]*

Wu H, Bailey C, Rasoulinejad P, Li S. "Automatic landmark estimation for adolescent idiopathic scoliosis assessment
using BoostNet." MICCAI 2017, pp. 127-135, doi:10.1007/978-3-319-66182-7_15 (sdr:manuscript/refs.bib entry
`wu2017boostnet`); Wang L, Xie C, Lin Y, et al. "The AASCE2019 challenge." Medical Image Analysis 2021;72:102115,
doi:10.1016/j.media.2021.102115 (sscn:paper/rsnai/refs.bib entry `aasce2021`). Canonical host SpineWeb dataset 16
(registration) and https://aasce19.grand-challenge.org/ (account required, probe 2026-09-19); open mirror GitHub
`zlinzju/ke30_u7_AASCE2019` (MIT) (sscn:tools/thoracic_xr_fetch.py docstring;
sdr:runs/review_availability_full/charting_probes/aasce-2019.json; sscn:docs/DATA_COMPLETENESS_AUDIT.md release row).

*[E]*

AASCE 2019 / BoostNet (Med Image Anal 2021). The mirror is the GitHub repo zlinzju/ke30_u7_AASCE2019 (MIT) (`DATA_COMPLETENESS_AUDIT.md` release rows).

**Modality**

*[D]*

Plain film, AP whole spine (T1-L5 in field), adolescent scoliosis, jpg with one `.mat` per film plus
`landmarks.csv` / `angles.csv` (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row; sscn:tools/aasce_to_drr.py docstring).

*[E]*

plain film, whole spine.

**Position/view**

*[D]*

AP (sscn:docs/XRAY_DATASET_USAGE.md). Posture: not recorded.

*[E]*

AP (`XRAY_DATASET_USAGE.json`).

**Licence and access**

*[D]*

Grid raw copy: obtained by the route `download_sources.py` records as "behind a request form" (SpineWeb)
(sscn:docs/DATA_COMPLETENESS_AUDIT.md AASCE row; sscn:slurm/reproduce_all.sh header "AASCE SpineWeb request form").
Mirror: repository licence MIT; the images' own reuse terms are not recorded (sscn:docs/DATA_COMPLETENESS_AUDIT.md
release row). An ethics note flags AASCE as a request-form source, used by no reported model
(sscn:SchwingNet/packet_src/statements.md item 5).

*[E]*

the original is behind a request form (`DATA_COMPLETENESS_AUDIT.md` line 335). The mirror is MIT.

**How it was acquired**

*[D]*

1. Grid raw copy `~/spine-detector/data/raw/aasce`: route and date not recorded beyond "behind a request form" (sscn:docs/DATA_COMPLETENESS_AUDIT.md).
2. Mirror: `tools/thoracic_xr_fetch.py --out $RS/data/thoracic_xr --grid-copy ~/spine-detector/data/raw/aasce --minutes 25`, run by `slurm/thoracic_xr_fetch.sh` (job txr_fetch_40411512); codeload zip 354,809,072 B, md5 `fe9430ab5c064c0d102d44810900e612`; file-by-file md5 against the grid copy (`grid_copy_md5.json`: identical 962, differing 98 = the `01-July-2019-*` challenge test set, only in mirror 35) (sscn:slurm/thoracic_xr_fetch.sh; sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk and release rows).

*[E]*

the HOME copy came from `download_sources.py`. The Ceph mirror came from `sbatch slurm/thoracic_xr_fetch.sh`, which runs `tools/thoracic_xr_fetch.py --out $RS/data/thoracic_xr --grid-copy ~/spine-detector/data/raw/aasce`. The codeload zip (354,809,072 B, md5 `fe9430ab5c064c0d102d44810900e612`) is recorded in `thoracic_xr/sources.json` (`DATA_COMPLETENESS_AUDIT.md` release row).

**When**

*[D]*

Grid raw copy: before 2026-09-07 (the spine-detector corpus rebuilt that day holds 8,069 AASCE instances,
mem:xray-corner-detector-status.md). Mirror on CEPH since 2026-09-22 01:06 (sscn:docs/DATA_COMPLETENESS_AUDIT.md AASCE
row; tool committed 2026-09-22, git log of sscn:tools/thoracic_xr_fetch.py).

*[E]*

the Ceph mirror has been on disk since 2026-09-22 01:06 (`DATA_COMPLETENESS_AUDIT.md` line 335).

**What it contains**

*[D]*

- Release: 609 labelled films (481 BoostNet training + 128 BoostNet test) + 98 challenge-test films without published landmarks; 68 landmarks per film = 17 vertebrae x 4 corners, plus 3 Cobb angles (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).
- Grid raw copy: 579 jpg (481 train + 98 test), 4 csv, 483 mat, no DICOM, no EXIF (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2 aasce row).
- CEPH mirror: 820 MB; boostnet_labeldata 481 + 128 = 609 labelled; prepared test set `thoracic_xr/aasce` 608 films (one degenerate box) (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row and criterion row).
- Persons: 217 index groups (an upper bound on films, a lower bound on people, uncertain) (sscn:docs/PATIENT_IDENTITY_SPEC.md); "251 patients" in sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1 disagrees.

*[E]*

the HOME copy holds 481 training films. The mirror holds 609 labelled films and is 820 MB (lines 570-572).

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/aasce/{train, test, train_txt}` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).
- CEPH raw + prepared: `$RS/data/thoracic_xr/{mirror_zlinzju_ke30_u7_AASCE2019/, aasce/{images,labels,meta,qc}, sources.json, grid_copy_md5.json}` (same).
- HOME converted: `~/aasce_drr` (457), `~/aasce_fov96_ctx` (census:toplevel_listing.txt).
- CEPH results: `$RS/data/or_ready/thoracic` (sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" row).

*[E]*

`~/aasce_drr` (HOME, converted/derived, listing 2026-09-15); `~/spine-detector` (HOME, raw, listing 2026-09-13); `$RS/data/thoracic_xr` (CEPH, raw, 0.8 GB, listing 2026-09-22); `~/spine-detector/data/raw/aasce` (HOME, raw)

**Annotation status**

*[D]*

Release labels (4 corners per vertebra). The level names T1-L5 are an assumed convention; a naming probe was
inconclusive (best agreement 10.64 %) (sscn:tools/aasce_to_drr.py docstring; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md
Surface M).

*[E]*

release landmarks, 68 per film for T1-L5. Levels are inferred.

**Derived products**

*[D]*

- `~/aasce_drr` (457 of 481; 24 failed the geometry gate) → `aasce_fov96_ctx` (no READY marker) → `allspine_v4`, `v5`, `v5c` (all deleted); 0 in v6-v9 (sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" row).
- Thoracic detector test set: 608 films scored by `slurm/thoracic_xr_eval.sh`, declared "Test only, never trained on" (sscn:slurm/thoracic_xr_prep.sh header via sscn:docs/DATA_COMPLETENESS_AUDIT.md).
- spine-detector corpus 8,069 instances (mem:xray-corner-detector-status.md).
- Person split of 2026-09-23: 217 groups, 440 images (sscn:SchwingNet/results/corpus_census.md section 3).

*[E]*

2 entries: `~/aasce_fov96_ctx`, `~/runs`

**Known defects and gaps**

*[D]*

- The 128 labelled BoostNet test films never reached `aasce_drr` (sscn:docs/DATA_COMPLETENESS_AUDIT.md AASCE row).
- The 24 geometry skips are an unsorted-landmark artefact (sort by centre y first) (sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row).
- Training use and test use conflict; decide one (same AASCE row).
- Directive D6 orders AASCE 457 into the pipeline (sscn:docs/RESUME_2026-09-22_PM.md "D6").

*[E]*

128 labelled films never reached `aasce_drr`, and the data's use as training or test is undecided (line 335).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): codeload zip of the default branch with md5 + bytes, unzip, 903-jpg count. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid aasce2019_boostnet` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[D]*

Programmatic (open mirror): `sbatch -D ~/spinesurg-ct-nnunet slurm/thoracic_xr_fetch.sh` (runs
`tools/thoracic_xr_fetch.py`), then check `sources.json` for the codeload zip md5 `fe9430ab5c064c0d102d44810900e612`
and counts 481 + 128 labelled + 98 test; `slurm/thoracic_xr_prep.sh` rebuilds the 608-film test layout. The canonical
SpineWeb copy is manual (registration form).

*[E]*

`sbatch slurm/thoracic_xr_fetch.sh`, then compare the zip's md5 with the recorded value.

---

### `mendeley_5jdfdgp762` <a id="mendeley_5jdfdgp762"></a>

**Mendeley Data 5jdfdgp762 'Spondylolisthesis Vertebral Landmark'.** Cards: D (D11 Mendeley 5jdfdgp762 "Spondylolisthesis Vertebral Landmark"), E (mendeley_5jdfdgp762); merged on 2026-10-08: A (A13 spondy_landmark), E (spondy_landmark). Also known as: `spondy_landmark`. Structured entry: `sources.yaml` id `mendeley_5jdfdgp762`; kind upstream_release; status on_disk; re-acquisition run (http).

**Source id**

*[D]*

`mendeley_5jdfdgp762` (grid `mendeley_716`) (sscn:tools/xray_dataset_usage.py, key `mendeley`)

*[E]*

`mendeley_5jdfdgp762` (family D's id)

*[2026-10-08: `~/data/spondy_landmark`, read on the grid]*

`spondy_landmark` (families A and E) is this release: the folder `~/data/spondy_landmark` holds its `Dataset.zip` (scr:inspect_unknown.out). The id stays as an alias in `sources.yaml` and `reacquire.py`.

**Name and citation**

*[D]*

"Spondylolisthesis Vertebral Landmark", Mendeley Data 5jdfdgp762 v1, doi:10.17632/5jdfdgp762.1, CC BY 4.0
(sscn:docs/DATA_COMPLETENESS_AUDIT.md release row; data statement of Bansal A, Kubicek J, Garg S, PLoS One
2026;21(4):e0347290, doi:10.1371/journal.pone.0347290, LOCAL xrsp:journal.pone.0347290.pdf page 1).

*[E]*

Mendeley 5jdfdgp762 v1, "Spondylolisthesis Vertebral Landmark" (`DATA_COMPLETENESS_AUDIT.md` release row).

**Modality**

*[D]*

Plain film, sagittal lumbar; Roboflow export at 640 x 640 jpg (sscn:tools/mendeley_to_render.py docstring).

*[E]*

plain film, lumbar spine.

**Position/view**

*[D]*

Lateral (sscn:docs/XRAY_DATASET_USAGE.md).

*[E]*

lateral (sagittal).

**Licence and access**

*[D]*

CC BY 4.0, open download through the Mendeley public API
(sdr:runs/review_availability_full/charting_probes/mendeley-5jdfdgp762.json, classification `open-download`,
2026-09-19).

*[E]*

CC BY 4.0, open.

**How it was acquired**

*[D]*

`Dataset.zip` from the Mendeley public API: file URL
`https://data.mendeley.com/public-files/datasets/5jdfdgp762/files/1b02c9a8-623b-4b9b-83e9-69f648bcfe46/file_downloaded`,
listed by `https://data.mendeley.com/public-api/datasets/5jdfdgp762/files?folder_id=root&version=1`
(sdr:runs/review_availability_full/charting_probes/mendeley-5jdfdgp762.json; sscn:docs/DATA_COMPLETENESS_AUDIT.md
release row). The fetch script is not recorded locally (the grid-only `~/spine-detector/scripts/download_sources.py`
is the "public radiograph sources" step of sscn:slurm/reproduce_all.sh; not read). Verification: 43,892,677 B equals
the API size; `testzip` clean (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Unknown" row).

*[E]*

`Dataset.zip`, 43,892,677 B, which matches the Mendeley API size (`DATA_COMPLETENESS_AUDIT.md` line 575).

*[2026-10-08: `~/data/spondy_landmark`, read on the grid]*

A second download into `~/data/spondy_landmark`: `Dataset.zip` (43,892,677 B, the API size; file mtime 2025-06-20), `url.txt` (118 B), `files.json` (724 B), an empty `dl.log` and the unpacked tree `x/` (scr:inspect_unknown.out). By the grid reading of 2026-10-08, `url.txt` holds the file URL above and `files.json` the API listing with the zip's sha256. The script that wrote them is in neither repository.

**When**

*[D]*

Before 2026-09-02 (sdet:report/manifest.parquet holds 377 Mendeley films / 2,666 instances). A differently sized file
`xrsp:Spondylolisthesis Vertebral Landmark.zip` (43,574,184 B) is on LOCAL with file date 2026-08-06 14:26; its
relation to `Dataset.zip` is not recorded.

*[E]*

not recorded.

*[2026-10-08: `~/data/spondy_landmark`, read on the grid]*

2026-09-19 13:03, the folder's mtime; `url.txt`, `files.json` and `dl.log` carry the same date (scr:inspect_unknown.out). This is the second copy; `mendeley_716` is older (before 2026-09-02, above).

**What it contains**

*[D]*

Page says 716 images (494 / 206 / 16); the served zip has 1,422 members = 714 jpg (494 train / 204 val / 16 test);
698 annotated (484 Keypoint R-CNN JSON + 214 YOLO-keypoint txt); 3,250 boxes; 3 to 11 bodies per film; 501 images
carry a BUU patient id; 90 spondylolisthesis films, 33 naming the slipped level in the file name
(sscn:docs/DATA_COMPLETENESS_AUDIT.md; sscn:tools/mendeley_to_render.py docstring;
sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1). 201 MB raw (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.4).

*[E]*

714 JPEG, although the page says 716 (`MANIFEST_DATA_MODELS_RESULTS.md` 7.5).

*[2026-10-08: `~/data/spondy_landmark`, read on the grid]*

`x/Dataset/{Train,Test}`; 396 of the first 400 files listed are jpg (scr:inspect_unknown.out). By the grid reading, `Train/` holds one folder, `Keypointrcnn_data`, and `Test/` 16 entries.

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/mendeley_716/{Dataset.zip, extracted/Dataset/...}` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).
- HOME converted/derived: `~/mendeley_drr` (584, 1.3 GB), `~/mendeley_fov96_ctx` (census:toplevel_listing.txt; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.4).
- LOCAL: `xrsp:Spondylolisthesis Vertebral Landmark.zip`; `sdet:dist/films/mendeley_*`, `sdet:report/renders/mendeley_*` (examples).

*[E]*

`~/mendeley_drr` (HOME, converted/derived, 1.3 GB, listing 2026-09-16); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/spine-detector/data/raw/mendeley_716` (HOME, raw, 0.2 GB)

*[2026-10-08: `~/data/spondy_landmark`, read on the grid]*

- HOME raw, second copy: `~/data/spondy_landmark` (folder 2026-09-19; scr:inspect_unknown.out). It moves in batch B14 to `$RS/data/mendeley_5jdfdgp762/raw/spondy_landmark` (MIGRATION_PLAN.md section 5) and is a deletion candidate once the sha256 in its `files.json` matches the `mendeley_716` zip.

**Annotation status**

*[D]*

Release labels: 4 corners per body, class-agnostic; level names are produced by counting up from the caudal
quadrilateral taken as S1, checked against BUU on 317 films (caudal anchor wins 295/317)
(sscn:tools/mendeley_to_render.py docstring).

*[E]*

release boxes with 4 keypoints, class-agnostic.

**Derived products**

*[D]*

`~/mendeley_drr` (584 of 698; 500 carry `duplicate_of` a BUU case) → `mendeley_fov96_ctx` → `allspine_v5` / `v5c`
only, both deleted; 0 in v6-v9 (sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" row). spine-detector corpus 2,666
instances (mem:xray-corner-detector-status.md).

*[E]*

1 entries: `~/mendeley_fov96_ctx`

**Known defects and gaps**

*[D]*

- A redistribution: about 500 BUU persons and 12 VinDr studies, 71 refused (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2 mendeley row).
- Excluded by directive D6 as a BUU redistribution (sscn:docs/RESUME_2026-09-22_PM.md "D6"); no document says the 71 non-duplicate films were deliberately left out (sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row).
- 716 on the page against 714 in the zip (release-side) (same, "Unknown" row).

*[E]*

it is a near-certain re-release of BUU, and it is excluded (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1; `corpus_census.md`).

*[2026-10-08: `~/data/spondy_landmark`, read on the grid]*

`nnunet:tools/ct_inventory.py` L50 and `docs/CT_INVENTORY.md` L35 list `~/data/spondy_landmark` as a CT root ("spondylolisthesis landmarks", 0 NIfTI); it is plain film. Nothing else in either repository names it.

**Re-acquisition recipe**

*[D]*

Programmatic: `curl -sS "https://data.mendeley.com/public-api/datasets/5jdfdgp762/files?folder_id=root&version=1"`
(gives `content_details.sha256_hash`), then
`curl -L -o Dataset.zip "https://data.mendeley.com/public-files/datasets/5jdfdgp762/files/1b02c9a8-623b-4b9b-83e9-69f648bcfe46/file_downloaded"`.
Verify 43,892,677 B, the API sha256, `unzip -t`, 714 jpg (sdr:recipe/README.md method `mendeley-api`;
sscn:docs/DATA_COMPLETENESS_AUDIT.md).

*[E]*

download through the Mendeley public API and check the zip size.

<details><summary>Former card <code>spondy_landmark</code> (families A and E, verbatim; superseded on 2026-10-08)</summary>

**HOME/data/spondy_landmark (unidentified; listed as 'spondylolisthesis landmarks' in the CT inventory).** Cards: A (A13 spondy_landmark), E (spondy_landmark). Structured entry: `sources.yaml` id `spondy_landmark`; kind unknown; status on_disk_unidentified; re-acquisition manual (manual).

**Source id**

*[A]*

`spondy_landmark`: a folder named "spondylolisthesis landmarks" in the CT inventory (CTINV L35; ssn:tools/ct_inventory.py L50).

*[E]*

`spondy_landmark` (family A's id)

**Name and citation**

*[A]*

Not recorded.

*[E]*

"spondylolisthesis landmarks", the name `nnunet:tools/ct_inventory.py` gives the root `~/data/spondy_landmark`. Nothing else in either repository or in memory names it.

**Modality**

*[A]*

Not recorded. It is listed under "CT volumes on disk", but 0 NIfTI were counted (CTINV L35).

*[E]*

listed among CT roots, with 0 NIfTI files and 1 directory (`CT_INVENTORY.md`). The actual content is not recorded.

**Position/view**

*[A]*

Not recorded.

*[E]*

not recorded.

**Licence and access**

*[A]*

Not recorded.

*[E]*

not recorded.

**How it was acquired**

*[A]*

Not recorded. No fetch script in either repo names it (grep of both repos and OpenSpineToolkit).

*[E]*

not recorded.

**When**

*[A]*

`HOME/data/spondy_landmark` mtime 2026-09-19 [listing] (LIST).

*[E]*

the listing dates the folder 2026-09-19.

**What it contains**

*[A]*

0 NIfTI; 1 directory one level down (CTINV L35).

*[E]*

not recorded.

**Where it is now**

*[A]*

HOME `data/spondy_landmark` (LIST).

*[E]*

`~/data/spondy_landmark` (HOME, raw, listing 2026-09-19)

**Annotation status**

*[A]*

Not recorded.

*[E]*

not recorded.

**Derived products**

*[A]*

None found.

*[E]*

none found.

**Known defects and gaps**

*[A]*

Unidentified holding.

*[E]*

the folder is unidentified.

**Re-acquisition recipe**

*[A]*

manual: identify it from the census `depth2.tsv` and any README inside before migrating. Nothing on this laptop says what it is.

*[E]*

not possible until the folder is identified. Open it on the grid first.

</details>

---

### `ieee_dataport_lateral_fullspine_236` <a id="ieee_dataport_lateral_fullspine_236"></a>

**IEEE DataPort 'Lateral full-spine X-ray (image) dataset' (236 films).** Cards: D (D12 IEEE DataPort lateral full-spine X-ray set (236)), E (ieee_dataport_lateral_fullspine_236). Structured entry: `sources.yaml` id `ieee_dataport_lateral_fullspine_236`; kind upstream_release; status on_disk; re-acquisition manual (manual).

**Source id**

*[D]*

`ieee_dataport_lateral_fullspine_236` (grid `lateral_236`) (sscn:tools/xray_dataset_usage.py, key `lateral236`)

*[E]*

`ieee_dataport_lateral_fullspine_236` (family D's id; grid folder `lateral_236`)

**Name and citation**

*[D]*

"Lateral full-spine X-ray (image) dataset", IEEE DataPort, DATASETID 14627,
https://ieee-dataport.org/documents/lateral-full-spine-x-ray-image-dataset (redirect from
`.../lateral-full-spine-x-ray-dataset`) (sdr:runs/review_availability_rr/charting_probes/ieee-dataport-lateral-full-spine.json).
Authors, DOI and paper: not recorded.

*[E]*

"IEEE DataPort lateral full-spine" (`XRAY_DATASET_USAGE.json`). The DOI is not recorded.

**Modality**

*[D]*

Plain film, standing whole-spine lateral from skull base to proximal femora, 3,056 px wide x 5,100-8,800 px tall, jpg
with a burned-in Chinese DICOM overlay (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1).

*[E]*

plain film, whole spine from skull base to proximal femora.

**Position/view**

*[D]*

Standing lateral (same).

*[E]*

standing lateral (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1).

**Licence and access**

*[D]*

IEEE DataPort subscription required ("Subscription Required", probe 2026-09-19)
(sdr:runs/review_availability_full/charting_probes/ieee-dataport-lateral-full-spine.json; sscn:slurm/reproduce_all.sh
header "IEEE lateral236 IEEE DataPort subscription"). Licence text and terms for derived labels: not recorded.

*[E]*

not recorded.

**How it was acquired**

*[D]*

Manual download under an IEEE DataPort subscription; who, when and with what checksum: not recorded
(sscn:slurm/reproduce_all.sh header; sdet:src/build_dataset.py docstring "VinDr/IEEE need personal credentials").

*[E]*

`download_sources.py` (grid only).

**When**

*[D]*

Not recorded. Bounded: `~/lateral236_pseudo` has directory date 2026-09-16 (census:toplevel_listing.txt).

*[E]*

not recorded.

**What it contains**

*[D]*

236 jpg, 1.3 GB, no annotation of any kind (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 2.1 and 7.4).

*[E]*

236 JPEG, 1.3 GB (`DATA_COMPLETENESS_AUDIT.md` line 586).

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/lateral_236` (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).
- HOME derived: `~/lateral236_pseudo` (236 anns), `~/lat236ps_fov96_ctx` (212 films), `~/pseudo_filtered/lateral236_pseudo_anchored` (203), `~/review_pack` (census:toplevel_listing.txt; sscn:SchwingNet/results/corpus_census.md section 3).

*[E]*

`~/lateral236_pseudo` (HOME, converted/derived, listing 2026-09-16); `~/pseudo_filtered` (HOME, converted/derived, listing 2026-09-17); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/spine-detector/data/raw/lateral_236` (HOME, raw, 1.3 GB)

**Annotation status**

*[D]*

None in the release; machine pseudo-labels; in the student review pack with `nhanes_pseudo` (verdicts not recorded)
(sscn:slurm/review_pack.sh).

*[E]*

none released. 236 films are pseudo-labelled.

**Derived products**

*[D]*

`lat236ps_fov96_ctx` → `allspine_v5` only (deleted); 0 in v6-v9; person split 236 persons, 193 / 22 / 21
(sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" row; sscn:SchwingNet/results/corpus_census.md).

*[E]*

1 entries: `~/lat236ps_fov96_ctx`

**Known defects and gaps**

*[D]*

The only real whole-spine lateral corpus on the grid, in no live bank; the pseudolabel arm that would have used it was
measured and refuted (sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md
section 7.4).

*[E]*

the origin is incompletely recorded.

**Re-acquisition recipe**

*[D]*

Manual: log in with an IEEE DataPort subscription at the URL above and download. Verify 236 jpg (about 1.3 GB). No
checksum list is recorded.

*[E]*

manual, from IEEE DataPort once the record is identified.

---

### `spinal_ai2024` <a id="spinal_ai2024"></a>

**Spinal-AI2024 (machine-generated AP scoliosis films, CurvNet data engine).** Cards: D (D13 Spinal-AI2024 (machine-generated AP scoliosis films)), E (spinal_ai2024). Structured entry: `sources.yaml` id `spinal_ai2024`; kind upstream_release; status on_disk; re-acquisition run (git).

**Source id**

*[D]*

`spinal_ai2024` (sscn:tools/xray_dataset_usage.py, key `spinalai`)

*[E]*

`spinal_ai2024` (family D's id)

**Name and citation**

*[D]*

Spinal-AI2024, https://github.com/Ernestchenchen/Spinal-AI2024, produced by the CurvNet "iterative data engine"
(Pattern Recognition; arXiv 2411.12604) (sscn:docs/DATA_COMPLETENESS_AUDIT.md release row;
sscn:tools/spinal_ai2024_to_render.py docstring).

*[E]*

Spinal-AI2024 (CurvNet, arXiv 2411.12604), github.com/Ernestchenchen/Spinal-AI2024 (`DATA_COMPLETENESS_AUDIT.md` release row).

**Modality**

*[D]*

Synthetic render: all 20,000 images are AI-generated scoliosis radiographs, 512 x 512 jpg; no patient was imaged
(sscn:tools/spinal_ai2024_to_render.py docstring).

*[E]*

machine-generated scoliosis AP films. This is synthetic data from a third party.

**Position/view**

*[D]*

AP (sscn:docs/XRAY_DATASET_USAGE.md).

*[E]*

AP.

**Licence and access**

*[D]*

Open GitHub repository; its licence is not recorded in any file read.

*[E]*

not recorded.

**How it was acquired**

*[D]*

Clone of the GitHub repository into `~/spine-detector/data/raw/spinal_ai2024/repo`, annotation zips unpacked
(sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row). Command, date and whether Git LFS was used: not recorded.

*[E]*

a clone of the repo, `spinal_ai2024/repo` (`DATA_COMPLETENESS_AUDIT.md` line 573).

**When**

*[D]*

Not recorded. Bounded: `~/spinalai_drr` directory date 2026-09-16 (census:toplevel_listing.txt); converter committed
2026-09-17 (git log of sscn:tools/spinal_ai2024_to_render.py).

*[E]*

not recorded.

**What it contains**

*[D]*

5 subsets x 4,000 = 20,000 jpg, 2.7 GB; COCO JSON in a text-detection schema (category "text"), train = subsets 1-4
(16,000), test = subset 5; `image_similarity_checklist.xlsx` with 20,440 rows (440 never released), 52 distinct Top-1
neighbours, 252 over all six neighbour columns; 11 to 21 bodies per film, mode 17
(sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1; sscn:tools/spinal_ai2024_to_render.py docstring).

*[E]*

20,000 JPEG, 2.7 GB.

**Where it is now**

*[D]*

- HOME raw: `~/spine-detector/data/raw/spinal_ai2024/repo` (sscn:docs/DATA_COMPLETENESS_AUDIT.md).
- HOME converted: `~/spinalai_drr` (8,358 renders, 4.4 GB) (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.4); `~/spai_verify` (directory date 2026-09-22; contents not recorded) (census:toplevel_listing.txt).

*[E]*

`~/spinalai_drr` (HOME, converted/derived, 4.4 GB, listing 2026-09-16); `~/spine-detector` (HOME, raw, listing 2026-09-13); `~/spine-detector/data/raw/spinal_ai2024` (HOME, raw, 2.7 GB)

**Annotation status**

*[D]*

Release labels, machine-generated: quads; level names assumed (T1-L5 only when exactly 17 bodies), not recovered
(sscn:tools/spinal_ai2024_to_render.py docstring).

*[E]*

4-point quadrilaterals. Levels are assumed.

**Derived products**

*[D]*

`~/spinalai_drr` 8,358 (films with exactly 17 bodies) → no bank; split as 44 similarity groups, all train, corpus flag
`person_key = false` (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2; sscn:SchwingNet/results/corpus_census.md).

*[E]*

none found in the disk map

**Known defects and gaps**

*[D]*

- Printed as 20,001 in DATASHEET and XRAY_DATASET_USAGE; the extra file is `repo/figs/checklist.png` (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Documents that disagree").
- 8,358 renders are 44 synthetic identities (`sim_000722` appears 1,270 times) (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 4.2).
- Directive D6 says "use", the written criterion says keep it out of validation; must sit wholly on the training side (sscn:docs/RESUME_2026-09-22_PM.md "D6"; sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row).

*[E]*

there are only 44 synthetic identities in `spinalai_drr` (`MANIFEST_DATA_MODELS_RESULTS.md` 4.2).

**Re-acquisition recipe**

*Runnable form (2026-10-08, second pass): git lfs pull required when the repo declares LFS; jpg count ignores pointer stubs. The commands and checks are in `sources.json`; `reacquire/reacquire.py --grid spinal_ai2024` prints them. Where the text below differs, `sources.json` is the runnable form.*

*[D]*

Programmatic: `git clone https://github.com/Ernestchenchen/Spinal-AI2024 repo` (add `git lfs pull` if the clone
holds pointer files; LFS use not recorded), unzip the two annotation archives. Verify 5 x 4,000 jpg at 512 x 512 and
16,000 + 4,000 COCO images (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row command). Re-render with
`python tools/spinal_ai2024_to_render.py --src <repo> --dst ~/spinalai_drr` (default `--n-bodies 17`).

*[E]*

`git clone` the repo and count 5 subsets of 4,000 images.

---

### `cm_spine_drive_file` <a id="cm_spine_drive_file"></a>

**cm_spine: one Google Drive file described only as 'intraoperative' (empty download).** Cards: D (D14 cm_spine (empty download)), E (cm_spine_drive_file). Structured entry: `sources.yaml` id `cm_spine_drive_file`; kind upstream_release; status empty; re-acquisition manual (manual).

**Source id**

*[D]*

`cm_spine_drive_file`

*[E]*

`cm_spine_drive_file` (family D's id)

**Name and citation**

*[D]*

A single Google Drive file, id `1r9wX1802gkU4-EQHMMlyAlEiWXGWLhhJ`, described only as "intraoperative"
(sscn:docs/DATA_COMPLETENESS_AUDIT.md release row, quoting `download_sources.py get_cm_spine()`).

*[E]*

a single Google Drive file described only as "intraoperative" (`DATA_COMPLETENESS_AUDIT.md` release row).

**Modality**

*[D]*

Not recorded; the only description is "intraoperative".

*[E]*

unknown.

**Position/view**

*[D]*

Not recorded.

*[E]*

unknown.

**Licence and access**

*[D]*

Not recorded.

*[E]*

unknown.

**How it was acquired**

*[D]*

`get_cm_spine()` in the grid-only `~/spine-detector/scripts/download_sources.py` ran gdown on the Drive id and left an
empty directory (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Unknown" row).

*[E]*

`download_sources.py get_cm_spine()`, which left an empty directory.

**When**

*[D]*

Directory created 2026-09-01 23:28 (sscn:docs/DATA_COMPLETENESS_AUDIT.md on-disk row).

*[E]*

the empty directory was created 2026-09-01 23:28 (line 585).

**What it contains**

*[D]*

Nothing: 0 files (same; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.1).

*[E]*

0 files.

**Where it is now**

*[D]*

HOME: `~/spine-detector/data/raw/cm_spine` (empty). LOCAL placeholder `sdet:data/raw/cm_spine` (empty).

*[E]*

`~/spine-detector` (HOME, raw, listing 2026-09-13); `~/spine-detector/data/raw/cm_spine` (HOME, raw, <0.1 GB)

**Annotation status**

*[D]*

None.

*[E]*

none.

**Derived products**

*[D]*

None.

*[E]*

none.

**Known defects and gaps**

*[D]*

What the file is has never been established (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Unknown" row).

*[E]*

the directory is empty.

**Re-acquisition recipe**

*[D]*

`gdown 1r9wX1802gkU4-EQHMMlyAlEiWXGWLhhJ` into a scratch directory, inspect, then decide; verify non-empty.

*[E]*

manual. Identify the Drive file first.

---

### `tvgh_spinexr` <a id="tvgh_spinexr"></a>

**TVGH-SpineXR (IEEE DataPort, probed, never acquired).** Cards: D (D15 TVGH-SpineXR (probed, never acquired)). Structured entry: `sources.yaml` id `tvgh_spinexr`; kind upstream_release; status not_acquired; re-acquisition manual (manual).

**Source id**

`tvgh_spinexr`

**Name and citation**

TVGH-SpineXR, IEEE DataPort doi:10.21227/x6bb-7r75 (sscn:docs/research_datasets_fourth_pass_verified_2026-09-22.json).

**Modality**

Plain film, diagnostic full-spine radiographs with T1-L5 per-vertebra level labels, masks and end-plates (same).

**Position/view**

Not recorded.

**Licence and access**

IEEE DataPort login required: the anonymous probe returned 403 `login_required`
(`$RS/data/thoracic_xr/sources.json`, quoted in sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row).

**How it was acquired**

Not acquired; access never requested (sscn:docs/DATA_COMPLETENESS_AUDIT.md).

**When**

Probed 2026-09-22 by `tools/thoracic_xr_fetch.py` (job txr_fetch_40411512) (same).

**What it contains**

Not recorded.

**Where it is now**

Nowhere.

**Annotation status**

Release labels per the record, never seen here (sscn:docs/research_datasets_fourth_pass_verified_2026-09-22.json).

**Derived products**

None.

**Known defects and gaps**

None of ours; an access barrier.

**Re-acquisition recipe**

Manual: request IEEE DataPort access for doi:10.21227/x6bb-7r75 if a second thoracic test set is wanted
(sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row).

---

### `spine_detector_corpus` <a id="spine_detector_corpus"></a>

**spine-detector real-film vertebra corner corpus (private OpenSpineConsortium/spine-detector).** Cards: D (D17 spine-detector corpus (real-film vertebra corner corpus)). Structured entry: `sources.yaml` id `spine_detector_corpus`; kind project_release; status on_disk; re-acquisition manual (rebuild).

**Source id**

`spine_detector_corpus`

**Name and citation**

spine-detector, this project's real-radiograph corner detector, private GitHub `OpenSpineConsortium/spine-detector`
(mem:xray-corner-detector-status.md). No DOI.

**Modality**

Plain film, normalised 8-bit PNG built from the raw film corpora; vertebra instances with 4 corners
(sdet:src/build_dataset.py docstring; mem:xray-corner-detector-status.md).

**Position/view**

AP 18,061 / lateral 15,882 instances on 2026-09-07 (mem:xray-corner-detector-status.md); `acquisition` column `film` /
`standing_dr` (sdet:report/manifest.parquet).

**Licence and access**

Inherits each source (cards D01-D13); VinDr stays on the grid under its DUA (mem:xray-corner-detector-status.md).

**How it was acquired**

Built by `python src/build_dataset.py` (converters per source, normalisation, manifest validation) from
`data/raw/*`; raw downloads by the grid-only `scripts/download_sources.py` (sdet:src/build_dataset.py;
sscn:slurm/reproduce_all.sh data stage). Zoomed windows by `scripts/make_zoom_dataset.py` → `data/yolo_v4z`
(mem:fluorocap-dataset.md).

**When**

Local snapshot manifest 2026-09-02 (sdet:report/manifest.parquet file date); manifest rebuilt 2026-09-07
(mem:xray-corner-detector-status.md); `~/spine-detector` directory date 2026-09-13 (census:toplevel_listing.txt).

**What it contains**

- 2026-09-07: 33,943 vertebra instances on 5,401 films: BUU-LSPINE 2000-pair subset 19,991, AASCE 8,069, NHANES 3,217, Mendeley 2,666 (mem:xray-corner-detector-status.md).
- 2026-09-02 local snapshot: 6,073 instances on 958 films (NHANES 543 films / 3,217; Mendeley 377 / 2,666; BUU 38 / 190); `level_source` annotated 3,217 / unknown 2,666 / inferred_from_position 190 (sdet:report/manifest.parquet).
- Detector datasets: `data/yolo`, `yolo_v2` (BUU 3,200 / 400 / 400, NHANES 443 / 50 / 50), `yolo_v3`, `yolo_v4z` (about 22k zoomed windows), `yolo_v5f_p00/p05/p08`, `yolo_v6f` (FluoroCap self-training), `yolo_hw` (VinDr "Surgical implant" boxes only) (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count; sscn:tools/film_corpus_inventory.py `YOLO_BANKS`; mem:fluorocap-dataset.md).
- Held-out eval set 558 instances (NHANES 294, Mendeley 249, BUU 15) (mem:xray-corner-detector-status.md).

**Where it is now**

- HOME: `~/spine-detector/{data/raw, data/interim/{images,manifest.parquet}, data/yolo*, runs/pose/...}` (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 5.3 and 8).
- HOME copies of detector weights: `~/FluoroCap/detect_v5z_*_best.pt`, `~/FluoroCap/detect_v6f_best.pt`, `~/level_id_service/weights/detector.pt` (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 5.3).
- LOCAL: `sdet:` snapshot (code, early manifest, ONNX exports in `dist/`, `report/`).

**Annotation status**

Mixed release labels: annotated (NHANES), inferred from position (BUU, AASCE), class-agnostic / unknown level (Mendeley); recorded per
instance in `level_source` (sdet:report/manifest.parquet; sscn:tools/manifest_to_drr_format.py docstring).

**Derived products**

Detectors `detect_v1` (data/yolo, 2026-08-30), `detect_v2` (yolo_v2, 2026-09-08), `detect_v3`/`detect_v4` (yolo_v3,
2026-09-11), `detector_v5z` (yolo_v4z, 2026-09-14; the epoch-25 checkpoint is the one shipped in `level_id_service`),
`detector_v6f` (yolo_v6f) (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 5.3). `~/films_drr` is converted from this
manifest (sscn:slurm/reproduce_all.sh renders stage).

**Known defects and gaps**

The detector never saw VinDr vertebrae or the 16,530 unannotated NHANES films; its film corpus is 12,709 of 39,705 held
films with no written reason for the rest (sscn:docs/DATA_COMPLETENESS_AUDIT.md "Gaps the auditor missed"). The full
per-version composition of `yolo_v3` and later is truncated in the audit and not recorded elsewhere locally.

**Re-acquisition recipe**

Clone the private repo on the grid, restore `data/raw/*` from cards D01-D13, run `python src/build_dataset.py` then the
YOLO export (`src/export_yolo.py`). Verify: the per-source instance counts it prints against the 2026-09-07 figures
(mem:xray-corner-detector-status.md).

---

### `fluorocap` <a id="fluorocap"></a>

**FluoroCap: literature and web harvest of published spine fluoroscopy (FLUOROCAP_PROTOCOL.md v1.0).** Cards: D (D18 FluoroCap (literature and web harvest of published spine fluoroscopy)), E (fluorocap). Structured entry: `sources.yaml` id `fluorocap`; kind project_release; status on_disk; re-acquisition manual (rebuild).

**Source id**

*[D]*

`fluorocap`

*[E]*

`fluorocap` (family D's id)

**Name and citation**

*[D]*

FluoroCap, built by this project under `docs/FLUOROCAP_PROTOCOL.md` (version 1.0, written 2026-09-13), not a public
release; frozen releases `~/FluoroCap/releases/FluoroCap_v0.1_{A,B}` (sscn:docs/FLUOROCAP_PROTOCOL.md;
sscn:docs/FLUOROCAP_README.md). Aggregator sources cited: MultiCaRe, Zenodo doi:10.5281/zenodo.10079370; Open-PMC-18M,
https://huggingface.co/datasets/vector-institute/open-pmc-18m (sdr:manuscript/refs.bib).

*[E]*

FluoroCap, a literature and web harvest of published spine fluoroscopy panels built by this project. It is not a public release. Its routes are PMC, Open-i, Open-PMC-18M, MultiCaRe, Commons, OpenAlex, S2, YouTube, Reddit and archives (`DATA_COMPLETENESS_AUDIT.md` heading line 739).

**Modality**

*[D]*

Literature figures: published reproductions of spine fluoroscopy and radiographs (72.8 % of panels have zero within-panel
pixel residual, i.e. the press resampled the grain out) plus frames cut from public videos
(mem:fluorocap-is-reproductions-not-fluoroscopy.md; sscn:docs/DATA_COMPLETENESS_AUDIT.md FluoroCap section). No model
here distinguishes fluoroscopy from a plain radiograph (mem:fluorocap-is-reproductions-not-fluoroscopy.md).

*[E]*

published figures, mostly reproductions. 72.8 % of panels have zero pixel residual against another panel (`DATA_ACCOUNTING.md` 3).

**Position/view**

*[D]*

Per panel from a classifier (`p_lateral`) and the caption; no pose (sscn:docs/FLUOROCAP_README.md `panel_preds.jsonl`).

*[E]*

not recorded per panel.

**Licence and access**

*[D]*

Per-article licence mapped to tiers A (PD/CC0/CC BY) to E (unknown); Dataset B = commercial-training-eligible panels
only (sscn:docs/FLUOROCAP_PROTOCOL.md section 5). Figure reuse only, never redistributed (sscn:docs/DATASHEET.md section
6). Instagram was not ingested on rights grounds (sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row). Harvester
credentials live in `~/.fluorocap` (not read) (mem:fluorocap-credentials-and-resolution.md).

*[E]*

per figure. Panels are train-only and never carry a test claim (`DATA_ACCOUNTING.md` 4).

**How it was acquired**

*[D]*

Routes and tools, regenerable in the order of sscn:docs/FLUOROCAP_README.md:
- Europe PMC search + BioC/JATS captions + PMC CDN figures: `tools/fluorocap.py search|captions|fetch` (fetch from WSL because PMC serves reCAPTCHA to the grid above about 1 req/s) (mem:fluorocap-dataset.md).
- Open-i `tools/fluorocap_openi.py` (84 queries); MultiCaRe `tools/fluorocap_multicare.py`; Open-PMC-18M `tools/fluorocap_pmc18m.py`; Wikimedia Commons `tools/fluorocap_commons.py`; OpenAlex / Semantic Scholar / Internet Archive PDFs (`tools/fluorocap_openalex.py`, `fluorocap_s2.py`, `fluorocap_archives.py`, figures by `fluorocap_pdf_figs.py`); Reddit `fluorocap_reddit.py`; Openverse `fluorocap_openverse.py`; YouTube/Bilibili via yt-dlp on WSL `tools/fluorocap_youtube.py` (905 queries) with window search `fluorocap_video_crop.py` (sscn:docs/DATA_COMPLETENESS_AUDIT.md FluoroCap section; sscn:tools/ file list).
- Publisher hi-res refetch `tools/fluorocap_refetch_hires.py` (mem:fluorocap-credentials-and-resolution.md).
- Panels, classifier, manifest, freeze: `fluorocap_panels.py`, `fluorocap_classify.py`, `fluorocap_manifest.py`, `fluorocap_freeze.py`; orchestrators `slurm/fluorocap_run_rest.sh`, `slurm/fluorocap_v2.sh`, `slurm/fluorocap_v2_pipeline.sh` (sscn:docs/FLUOROCAP_README.md; mem:fluorocap-dataset.md).
- Verification: `fetched.jsonl` records URL, UTC time, status and sha256 per fetch; panels carry `panel_hash`; each frozen release has `SHA256SUMS` and `LOCK.json` (sscn:docs/FLUOROCAP_PROTOCOL.md section 5).

*[E]*

`nnunet:tools/fluorocap*.py`, with WSL-only routes under `~/FluoroCap_wsl` (`DATA_COMPLETENESS_AUDIT.md` lines 330, 761). Credentials sit in `~/.fluorocap` (not read).

**When**

*[D]*

Search 2026-09-13 (sscn:docs/FLUOROCAP_PROTOCOL.md section 1). Frozen release A/B generated 2026-09-14 02:35 UTC,
pipeline commit d833b481 (sscn:benchmark/data/fluorocap_v0.1/LOCK_A.json, LOCK_B.json). YouTube frames rsynced
until 2026-09-14 18:23 (`RSYNC_DONE`); manifest last rebuilt 2026-09-15 19:54; LSTV pass-2 rows pushed 2026-09-15 22:13;
the training bank built 2026-09-18 03:03 (sscn:docs/DATA_COMPLETENESS_AUDIT.md FluoroCap rows). Dropped from every
training set by directive D1 on 2026-09-23 (sscn:docs/RESUME_2026-09-22_PM.md "D1"; mem:data-directives-2026-09-23.md).

*[E]*

the Europe PMC search ran 2026-09-13, and the manifest dates from 2026-09-15 (`DATA_COMPLETENESS_AUDIT.md`). The listing dates `~/FluoroCap` 2026-09-20.

**What it contains**

*[D]*

- Europe PMC: 39,449 hits → 39,403 articles; PMC main arm 6,177 rows / 4,963 figures / 3,330 articles; pathology arm 1,016 figures / 698 articles; LSTV arm 1,151 rows on the grid; Open-i 301 rows; Open-PMC-18M 4,012 shards read; MultiCaRe 67; Commons 112 rows; OpenAlex 9,780 works / 6,683 PDFs, S2 2,556 PDFs, IA 480 PDFs; YouTube 6,085 videos → 285,631 matched frames on the grid; Reddit 629; archives 98 rows (sscn:docs/DATA_COMPLETENESS_AUDIT.md FluoroCap release rows).
- On disk: `panels/` 29,500 png (4.68 GB); `video_panels` 1,095 + `video_panels_med` 366; `raw/` 4,998 PMC figures + 2,808 `.pmc` backups (2.27 GB); `raw_hires/` 2,080; `pdf/` 9,758 PDFs (19.77 GB); `youtube/` 298,075 frames (181.0 GB per AUDIT.json); `manifest.csv` 21,603 rows x 112 columns, 5,019 included (Dataset A), 1,590 Dataset B (sscn:docs/DATA_COMPLETENESS_AUDIT.md FluoroCap on-disk rows).
- Whole tree 316 GB, of which `youtube/` 265 GB (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 2.1); the two youtube sizes disagree.
- Frozen release: A 2,531 panels / 1,990 figures / 1,095 articles; B 991 / 765 / 484 (sscn:benchmark/data/fluorocap_v0.1/LOCK_A.json, LOCK_B.json).
- Persons: none exist; keyed by source document, about 1,197 documents (uncertain) (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2), 1,953 source documents in the 2026-09-23 split (sscn:SchwingNet/results/corpus_census.md).

*[E]*

316 GB, including 29,500 panels of 4.68 GB, 9,758 PDFs of 19.77 GB and 298,075 YouTube frames of 181.0 GB (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1; `DATA_COMPLETENESS_AUDIT.md` lines 757-761).

**Where it is now**

*[D]*

- HOME: `~/FluoroCap` (directory date 2026-09-20), `~/fluorocap_drr` (2,385), `~/fluorocap_drr_smoke` (137), `~/fluorocap_fov96_ctx`, `~/fluorocap_pack` (1,500), `~/fluorocap_patient_keys.json`, `~/.fluorocap` (credentials; do not read) (census:toplevel_listing.txt).
- WSL (this machine): `/home/gschwing/FluoroCap_wsl` (WSL-only routes, YouTube frames, hi-res refetch round 3) and `/home/gschwing/FluoroCap_lstv` (the LSTV arm; it does not exist on the grid) (sscn:docs/DATA_COMPLETENESS_AUDIT.md FluoroCap "Documents that disagree").
- LOCAL: `<laptop folder Desktop/FluoroCap_reading; not a dependency>`, `.../FluoroCap_screening` (reader HTML pages, 2026-09-13/14); `sscn:benchmark/data/fluorocap_v0.1/` (locks, stats, licence review queue).
- CEPH: `$RS/tmp/fluorocap_audit/AUDIT.json` (job 40416374) (sscn:docs/DATA_COMPLETENESS_AUDIT.md).

*[E]*

`~/FluoroCap` (HOME, raw, 316.0 GB, listing 2026-09-20); `~/fluorocap_drr` (HOME, converted/derived, listing 2026-09-18); `~/fluorocap_drr_smoke` (HOME, converted/derived, listing 2026-09-18); `~/fluorocap_pack` (HOME, converted/derived, listing 2026-09-18); `~/fluorocap_patient_keys.json` (HOME, converted/derived, listing 2026-09-22); `~/FluoroCap/youtube` (HOME, raw, 181.0 GB); `~/FluoroCap/pdf` (HOME, raw, 19.8 GB); `~/FluoroCap/panels` (HOME, converted/derived, 4.7 GB); `~/FluoroCap/raw` (HOME, raw, 2.3 GB)

**Annotation status**

*[D]*

Pseudo-labels, unreviewed: caption label (author-stated levels) plus decoder placements (model / caption / mate / anchor / VLM), about 85 % of
rare-class labels being the level model's own output; `human_qc_status` and `ground_truth_method` are `pending` on all
21,603 rows; no panel has been read by a human; a 179-panel random bench and a 371-panel student pack were built with 0
verdicts recorded (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md Surface N; sscn:docs/FLUOROCAP_QC_2026-09-14.md;
sscn:docs/DATA_COMPLETENESS_AUDIT.md "unfinished" row).

*[E]*

decoder placements only. The panels are not verified by anyone (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1).

**Derived products**

*[D]*

- `~/fluorocap_drr` (2,385 from decode file v4 after >= 3 labels and short side >= 320 px) → `fluorocap_fov96_ctx` (14,957 crops) → `allspine_v7` (training) and the C-ArmLSpine fold mix banks (950 panels as 2,100 crops); 0 in v8/v9 (sscn:docs/DATA_COMPLETENESS_AUDIT.md; sscn:docs/MODEL_CARD.md section 3.2).
- `yolo_v6f` → `detect_v6f` (detector self-training) (mem:fluorocap-dataset.md).
- Panel modality classifiers v1-v3, orientation net, hardware detector, region classifier (mem:fluorocap-dataset.md).
- Renderer validation sets `~/FluoroCap/real_fluoro_only` (27) and `real_grainy` (94) (sscn:docs/DATA_COMPLETENESS_AUDIT.md "used" rows).
- FluoroGen LoRA training set (card D19); CUT translation target domains `~/cut_v1`, `~/cut_v2` (mem:fluorogen-synthetic.md).

*[E]*

3 entries: `~/allspine_v7_fov96_ctx`, `~/fluorocap_fov96_ctx`, `~/proto_test`

**Known defects and gaps**

*[D]*

- The training bank never passed the x-ray modality / montage / resolution gate: 488 of 2,385 bank panels are gate rejects (sscn:docs/DATA_COMPLETENESS_AUDIT.md bug row).
- The manifest is stale: 7,898 panels have no row; dedup covers 11,446 images only (same, "unfinished" rows).
- The ~200-panel annotated TEST set, the only use D1 permits, does not exist (same).
- The WSL-only routes (Instagram 2,611 posts, HF ROCOv2 1,584 rows, jstage 2,100, scielo 101, patents) never reached the grid; 9,948 Commons titles never inspected; the web-image route produced nothing (same).

*[E]*

- The manifest is stale: 21,603 rows against 29,500 panels (`DATA_COMPLETENESS_AUDIT.md` line 305).
  - The modality gate was never applied before the bank was built (line 145).
  - FluoroCap is dropped from every training set (`DATA_COMPLETENESS_AUDIT.md`).

**Re-acquisition recipe**

*[D]*

Programmatic but not bit-reproducible, because the web sources drift: run the stage list in
sscn:docs/FLUOROCAP_README.md ("Regenerate") as sbatch jobs (network stages from WSL where the grid is blocked), with
the credentials in `~/.fluorocap` where a route needs them. Verify a rebuild against the frozen release by
`sha256sum -c releases/FluoroCap_v0.1_A/SHA256SUMS` and the `manifest_sha256` in `LOCK.json`
(sscn:docs/FLUOROCAP_PROTOCOL.md section 5). The frozen release on HOME is the authoritative copy; under D1 nothing
needs re-harvesting.

*[E]*

no single command. Each route has its own tool (`nnunet:tools/fluorocap_*.py`), and the WSL routes never reached the grid.

---

### `fluorogen_synthetic` <a id="fluorogen_synthetic"></a>

**FluoroGen diffusion-styled synthetic frames (SDXL + Canny ControlNet + fluoroscopy LoRA) and the film-look LoRA.** Cards: D (D19 FluoroGen (diffusion-styled synthetic frames) and the film-look LoRA), E (fluorogen_synthetic). Structured entry: `sources.yaml` id `fluorogen_synthetic`; kind derived; status on_disk; re-acquisition manual (rebuild).

**Source id**

*[D]*

`fluorogen_synthetic`

*[E]*

`fluorogen_synthetic`

**Name and citation**

*[D]*

FluoroGen, this project: SDXL 1.0 base (CreativeML Open RAIL++-M) with a Canny ControlNet and a fluoroscopy LoRA,
started 2026-09-14 (mem:fluorogen-synthetic.md). No DOI.

*[E]*

FluoroGen: SDXL + canny ControlNet + fluoroscopy LoRA frames (`mem:fluorogen-synthetic`; `MANIFEST_DATA_MODELS_RESULTS.md` 4)

**Modality**

*[D]*

Synthetic render (diffusion img2img / ControlNet over labelled DRRs) (mem:fluorogen-synthetic.md).

*[E]*

synthetic render (generated fluoroscopy-style frames) conditioned on CT renders

**Position/view**

*[D]*

Inherited from the source DRR (AP / lateral / oblique) (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 4,
`fluorogen/synth_rare` AP 7,536 / lat 5,390).

*[E]*

AP 7,536 / lateral 5,390 in `synth_rare` (`MANIFEST_DATA_MODELS_RESULTS.md` 4)

**Licence and access**

*[D]*

Base model licence CreativeML Open RAIL++-M (mem:fluorogen-synthetic.md). Outputs inherit the source CT terms
(not stated in any file read).

*[E]*

project-built; inherits the terms of the CTs and the generator weights (not recorded)

**How it was acquired**

*[D]*

Generated: `tools/fluorogen_dataset.py` → `~/fluorogen/dataset_v1/train` (FluoroCap panels + video windows + 1,200 real
films) → `slurm/fluorogen_lora.sh` (4 H200, 6,000 steps, rank 32) → `slurm/fluorogen_generate.sh`
(`tools/fluorogen_generate.py`). Base weights pulled from Hugging Face into `~/.cache/huggingface/hub` by
`~/fluorogen/dl_weights.py` (mem:fluorogen-synthetic.md). Film-look branch: `tools/film_style_dataset.py` →
`~/film_style_ds` → `slurm/train_film_lora.sh` → `~/fluorogen/lora_film_v1` → `slurm/film_lora_apply.sh`
(sscn:tools/film_style_dataset.py; sscn:slurm/film_lora_apply.sh).

*[E]*

generated on the grid (`nnunet:slurm/fluorogen_generate.sh` is referenced in `scr:dataplan/path_refs_files.csv`)

**When**

*[D]*

2026-09-14 start; img2img verdict 2026-09-15 (mem:fluorogen-synthetic.md); `~/fluorogen` directory date 2026-09-17,
`~/film_style_ds` 2026-09-17, `~/sd_fov96_ctx` 2026-09-18 (census:toplevel_listing.txt).

*[E]*

`~/fluorogen` is dated 2026-09-17 in the listing

**What it contains**

*[D]*

`~/fluorogen/synth_v1` empty; `synth_rare` 12,929 renders over 2,844 cases (T13 86, L6 1,763; 9.0 GB; 3 unparseable);
`synth_rare_lowstrength` 566 (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 4 and 7.4). Film-styled CT renders
`~/ctsp_drr_film` (801), `~/physics_drr_film` (2,430 CTSP-named + 1,321 implant), `~/physics_rare_film` (603),
`~/verse_drr_film` (sscn:docs/PATIENT_IDENTITY_SPEC.md section 2 ctsp row; census:toplevel_listing.txt).

*[E]*

`synth_rare` 12,929 renders (9.0 GB), `synth_rare_lowstrength` 566, `synth_v1` empty (`MANIFEST_DATA_MODELS_RESULTS.md` 4, 7.4)

**Where it is now**

*[D]*

HOME: `~/fluorogen/{dataset_v1, lora_v1, lora_film_v1, synth_v1, synth_rare, synth_rare_lowstrength}`, `~/film_style_ds`,
`~/*_drr_film`, `~/sd_fov96_ctx` (mem:fluorogen-synthetic.md; census:toplevel_listing.txt).

*[E]*

`~/fluorogen` (HOME, converted/derived, listing 2026-09-17)

**Annotation status**

*[D]*

Pseudo-labels: copied from the source DRR (CT-derived); a label-preservation gate drops a styled render whose crops flip on
more than 20 % of bodies (sscn:slurm/film_lora_apply.sh).

*[E]*

level boxes carried from the conditioning renders: T13 86, L6 1,763 (`MANIFEST_DATA_MODELS_RESULTS.md` 4)

**Derived products**

*[D]*

`sd_fov96_ctx` (9,443 films) → `allspine_v2sd_fov96_ctx` (not in the 2026-10-07 listing) (sscn:slurm/film_lora_apply.sh;
sscn:docs/XRAY_DATASET_USAGE.md; census:toplevel_listing.txt). `synth_rare` is in no bank
(sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 4.1).

*[E]*

none found in the disk map

**Known defects and gaps**

*[D]*

SDXL img2img destroys anatomy at strength 0.45-0.65 and barely changes the DRR at 0.2 (mem:fluorogen-synthetic.md);
`synth_rare` has no written reason for being unused (sscn:docs/DATA_COMPLETENESS_AUDIT.md criterion row).

*[E]*

in no bank; `synth_v1` produced nothing (`MANIFEST_DATA_MODELS_RESULTS.md` 4, 7.1)

**Re-acquisition recipe**

*[D]*

Regenerate from the scripts above after the CT render banks exist; record the base-weight revisions (not recorded
today).

*[E]*

regenerate with the FluoroGen chain; the LoRA is at `~/fluorogen/lora_v1` (path_refs)

---

### `fluoro_video_public_clips` <a id="fluoro_video_public_clips"></a>

**Public fluoroscopy video and cine clips (PMC supplements, Commons, YouTube re-encodes, Neurosurgical Focus: Video, DysphagiaBank UNM).** Cards: D (D20 Public fluoroscopy video and cine clips (downloaded)), E (fluoro_video_public_clips). Structured entry: `sources.yaml` id `fluoro_video_public_clips`; kind upstream_release; status on_disk; re-acquisition manual (manual).

**Source id**

*[D]*

`fluoro_video_public_clips`

*[E]*

`fluoro_video_public_clips` (family D's id)

**Name and citation**

*[D]*

Bern dynamic-myelography Videos 1-4 (PMC8463391, CC BY 4.0); the PMC10242080 SpineJack AVI; the PMC11328828 Cureus
paediatric cervical exam; the PMC4852439 MOV; three Wikimedia Commons items; YouTube re-encodes of 28 ids
(sscn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md "Already obtained"); six Neurosurgical Focus: Video MP4s (PMC9542308,
9555359, 9574671, 11013356, 11013367, 11013353) and PMC13418632; `github/VFSS_analysis`; DysphagiaBank UNM 87 files
(sscn:docs/RESUME_2026-09-22_PM.md section B).

*[E]*

teaching and journal videos from which fluoroscopy panels are cut (`nnunet:tools/fluoro_video/README.md`; `nnunet:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md`).

**Modality**

*[D]*

Fluoroscopy video (RF) and composite teaching videos with fluoroscopy insets (sscn:tools/fluoro_video/README.md).

*[E]*

fluoroscopy inside composite video.

**Position/view**

*[D]*

Per video, parsed as labels from `docs/FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md`, not measured (sscn:tools/fluoro_video/README.md
step 0).

*[E]*

per-clip timing and angle read by OCR (README).

**Licence and access**

*[D]*

Mixed: CC BY (Bern, Neurosurgical Focus: Video), CC BY-NC-SA with no LLM use for DysphagiaBank, and YouTube copies kept
for screening without permission (YouTube terms restrict download) (sscn:docs/RESUME_2026-09-22_PM.md;
sscn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md "Read once before sending" item 5). Private research evaluation
only; frames never committed or uploaded (sscn:tools/fluoro_video/README.md).

*[E]*

"private research evaluation only; frames and clips are never committed or uploaded" (README).

**How it was acquired**

*[D]*

Downloads by jobs 40477816 (YouTube) and 40478021 (PMC) (sscn:docs/RESUME_2026-09-22_PM.md); the download scripts are
not in the local repo. Clips extracted programmatically by `tools/fluoro_video` (`inventory` → `run` array 40480030 →
`report` 40480032), every input sha256-hashed (sscn:tools/fluoro_video/README.md; sscn:docs/RESUME_2026-09-22_PM.md).

*[E]*

`nnunet:tools/fluoro_video/slurm/*.sbatch` under `$RS/data/external/fluoro_video/work`.

**When**

*[D]*

2026-09-26 (sscn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md; `$RS/data/external` directory date 2026-09-26 in
census:toplevel_listing.txt).

*[E]*

the listing dates `$RS/data/external` 2026-09-26.

**What it contains**

*[D]*

`youtube` 12 GB, `pmc` 3.9 GB, `dysphagiabank_unm` 87 files 19 GB; 1,269 clips (776 live), each a PNG frame directory
with `frames.csv`, `preview.mp4` and `clip.json` (sscn:docs/RESUME_2026-09-22_PM.md).

*[E]*

not recorded in Family E's evidence.

**Where it is now**

*[D]*

CEPH: `$RS/data/external/fluoro_video/{youtube, pmc, commons, github, dysphagiabank_unm, manifest.tsv, work/...}`,
clips under `.../clips/` and `.../work/qc_export/{REPORT.md, clips.csv, manifest.json}`; environment
`$RS/envs/fluoroclip` (sscn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md; sscn:tools/fluoro_video/README.md;
sscn:docs/RESUME_2026-09-22_PM.md).

*[E]*

`$RS/data/external` (CEPH, raw, listing 2026-09-26)

**Annotation status**

*[D]*

None; no inference has been run on the clips (`det_run1`/`det_run2` empty) (sscn:docs/RESUME_2026-09-22_PM.md).

*[E]*

none.

**Derived products**

*[D]*

Clip QC report and manifest; results named as `SchwingNet/results/fluoro_video_clips/` (sscn:docs/RESUME_2026-09-22_PM.md), a directory not present in the local checkout.

*[E]*

none recorded.

**Known defects and gaps**

*[D]*

The success tally of the 43 extra YouTube ids was never made; Vimeo 1109076785 needs a browser cookie; a Facebook video
may need a browser save; AJR Rosas & Lee 2012 needs a subscription (sscn:docs/RESUME_2026-09-22_PM.md).

*[E]*

not recorded.

**Re-acquisition recipe**

*[D]*

Partly programmatic: PMC supplementary files by PMCID from Europe PMC / PMC; YouTube by yt-dlp from WSL (grid glibc
cannot run the JS runtime, mem:fluorocap-dataset.md); then `tools/fluoro_video` inventory/run/report as in its README.
The exact download commands are not recorded locally; `manifest.tsv` on CEPH is the list to re-fetch against.

*[E]*

see `nnunet:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md`, which Family E did not read.

---

### `bournemouth_qf_cervical_tracks` <a id="bournemouth_qf_cervical_tracks"></a>

**Bournemouth cervical quantitative-fluoroscopy corner tracks (BORDaR 385; Branney, Breen, Breen).** Cards: D (D21 Bournemouth cervical quantitative-fluoroscopy corner tracks (BORDaR 385)). Structured entry: `sources.yaml` id `bournemouth_qf_cervical_tracks`; kind upstream_release; status on_disk; re-acquisition manual (manual).

**Source id**

`bournemouth_qf_cervical_tracks`

**Name and citation**

Branney J, Breen A, Breen A. BORDaR 385, doi:10.18746/bmth.data.00000385, CC BY 4.0; companion article Branney et al.
2024, J Funct Morphol Kinesiol 9(1):55, doi:10.3390/jfmk9010055 (sscn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md;
sscn:docs/BOURNEMOUTH_QF_HARNESS.md).

**Modality**

Derived data from lateral cervical fluoroscopy cine; no pixels: per-frame 4-corner vertebral templates C0-T1 at 15 Hz
(sscn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md).

**Position/view**

Lateral, flexion and extension sequences (same).

**Licence and access**

CC BY 4.0, open download (same).

**How it was acquired**

Downloaded from https://bordar.bournemouth.ac.uk/385/ (exact command not recorded); md5
`aec3d16d031f62c4a4b7725cd5e0a0be` (sscn:docs/BOURNEMOUTH_QF_HARNESS.md).

**When**

2026-09-26 (LOCAL file date of `<the laptop home; not a dependency>/data/bournemouth_qf/raw/Cervical_Database.mat`;
sscn:docs/BOURNEMOUTH_QF_HARNESS.md "Written 2026-09-26").

**What it contains**

`Cervical Database.mat` (24,380,812 B locally) + `README.pdf`; 126 imaging events x (flexion, extension) = 252
sequences of 63 people, 181-339 frames per sequence (sscn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md; ls 2026-10-07).

**Where it is now**

LOCAL `<the laptop home; not a dependency>/data/bournemouth_qf/raw/`; CEPH `$RS/data/realxray/bournemouth_qf/raw/` and the exported truth
`$RS/data/realxray/bournemouth_qf/{meta,splits.json,sequences.json,summary.json}` (sscn:docs/BOURNEMOUTH_QF_HARNESS.md).

**Annotation status**

Release labels from a semi-automatic template tracker (hand-placed on the first frame, then tracked), not independent
hand labels (sscn:docs/BOURNEMOUTH_QF_HARNESS.md).

**Derived products**

Harness `tools/bournemouth_qf_eval.py`, `tools/cine_eval.py`, `slurm/cine_eval.sh`; no score yet because the frames
have not arrived (sscn:docs/BOURNEMOUTH_QF_HARNESS.md).

**Known defects and gaps**

The DICOM cine itself is not public (request pending, card D22) (sscn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md).

**Re-acquisition recipe**

Download `Cervical Database.mat` and `README.pdf` from the BORDaR 385 record; verify md5
`aec3d16d031f62c4a4b7725cd5e0a0be`.

---

### `fluoro_cine_requests_2026_09_26` <a id="fluoro_cine_requests_2026_09_26"></a>

**Fourteen fluoroscopy cine requests drafted 2026-09-26 (Bournemouth DICOM cine, Maastricht, Bern, Pittsburgh, ...).** Cards: D (D22 Fluoroscopy cine requests (not acquired)). Structured entry: `sources.yaml` id `fluoro_cine_requests_2026_09_26`; kind request; status requested_not_sent; re-acquisition manual (manual).

**Source id**

`fluoro_cine_requests_2026_09_26`

**Name and citation**

Fourteen ready-to-send requests: Bournemouth QF DICOM cine (cervical BORDaR 385 and lumbar OSF a27py), Maastricht
cervical cine (doi:10.3390/bioengineering13030351), Bern dynamic myelography native DICOM, Pittsburgh swallow corpus,
Seattle Science Foundation, Mayfield, DMX Imaging, Radiopaedia (7 cases), The Procedure Guide, Konica Minolta DDR,
Jefferson (Hines), MTFI, Christopher Faubel, DARADIA (sscn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md checklist;
sscn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md).

**Modality**

Fluoroscopy cine (RF / dynamic radiography) (same).

**Position/view**

Mostly lateral cervical flexion-extension; lumbar L2-S1 (Bournemouth lumbar); lateral swallow (Pittsburgh) (same).

**Licence and access**

Request or DUA per source; two addresses unverified (Seattle, Radiopaedia); letters state non-commercial evaluation
(sscn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md).

**How it was acquired**

Not acquired. Draft emails `sscn:docs/fluoro_requests_eml/01..14_*.eml` (11 files) plus contact-form, fax and WhatsApp
texts (same). Whether any was sent: not recorded.

**When**

Drafted 2026-09-26 (file dates of sscn:docs/fluoro_requests_eml/).

**What it contains**

Expected contents per source in sscn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md (e.g. Maastricht 112 recordings at
1024 x 1024, 15 fps; Pittsburgh about 1,500 clips at 30 fps).

**Where it is now**

Nowhere (requests only).

**Annotation status**

None held. Per source, once obtained: Maastricht per-frame C0-C7 contours; Pittsburgh C2 and C4 corners; Bournemouth corner tracks already public
(card D21) (sscn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md).

**Derived products**

None.

**Known defects and gaps**

None of ours.

**Re-acquisition recipe**

Manual: send the `.eml` drafts after the "Read once before sending" checks (commercial scope, IRB, "we would not train
on it", co-authorship, YouTube copies) (sscn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md).

---

### `sx_stitch_request` <a id="sx_stitch_request"></a>

**SX-Stitch intraoperative C-arm series (Li et al., arXiv:2409.05681), request draft.** Cards: D (D23 SX-Stitch intraoperative C-arm series (request draft)). Structured entry: `sources.yaml` id `sx_stitch_request`; kind request; status requested_not_sent; re-acquisition manual (manual).

**Source id**

`sx_stitch_request`

**Name and citation**

Li Y, Gao H, He M, Liang J, Gu J, Liu W. "SX-Stitch: an efficient VMS-UNet based framework for intraoperative scoliosis
X-ray image stitching." arXiv:2409.05681 (sscn:docs/data_requests/SX-Stitch_request.md).

**Modality**

Intraoperative C-arm images (fluoroscopy stills), spine (same).

**Position/view**

Consecutive overlapping series of one patient, 20-90 % overlap (same).

**Licence and access**

Not public; request to the authors (SUSTech, PUMCH) (same).

**How it was acquired**

Not acquired; request letter drafted, "to be sent by Greg" (same). Sent: not recorded.

**When**

Draft first committed 2026-09-19, last 2026-09-23 (git log of sscn:docs/data_requests/SX-Stitch_request.md).

**What it contains**

1,032 intraoperative C-arm images at 512, 1024 and 1920 px with vertebra segmentation masks (same).

**Where it is now**

Nowhere.

**Annotation status**

None held; the paper describes vertebra segmentation masks (same).

**Derived products**

None.

**Known defects and gaps**

None of ours.

**Re-acquisition recipe**

Manual: send the drafted request.

---

### `balgrist_exvivo_request` <a id="balgrist_exvivo_request"></a>

**Balgrist ex-vivo lumbar CT + C-arm set (Jecklin et al.), request draft.** Cards: D (D24 Balgrist ex-vivo lumbar CT + C-arm set (request draft)). Structured entry: `sources.yaml` id `balgrist_exvivo_request`; kind request; status requested_not_sent; re-acquisition manual (manual).

**Source id**

`balgrist_exvivo_request`

**Name and citation**

Jecklin et al., Medical Image Analysis 2024 (domain adaptation for lumbar reconstruction from real fluoroscopy) and a
2025 Scientific Reports follow-up (sscn:docs/outreach/balgrist_data_request_2026-09-21.md). Also belongs to the CT-plus-
C-arm family.

**Modality**

CT plus real mobile C-arm X-rays of lumbar spines in intact torsos, three devices (Cios Spin, Ziehm Vision, Ziehm
Vision FD) (same).

**Position/view**

Multiple C-arm poses with fiducial-based projection matrices (same).

**Licence and access**

Restricted (pending patents); DUA through Wayne State offered (same).

**How it was acquired**

Not acquired; email drafted to <corresponding author of Jecklin 2024, address withheld> (same). Sent: not recorded.

**When**

Drafted 2026-09-21 (file name; git first commit 2026-09-21).

**What it contains**

13 specimens plus six validation specimens per the letter (same).

**Where it is now**

Nowhere.

**Annotation status**

None held; the letter describes a fiducial-based pose per image (same).

**Derived products**

None.

**Known defects and gaps**

None of ours.

**Re-acquisition recipe**

Manual: send the drafted request.

---

### Family D notes after the cards (verbatim)

### Appendix A — Render, pseudo-label and crop banks on HOME that hold family-D data

"Date" is the directory date in census:toplevel_listing.txt (2026-10-07). "Films" are distinct films read from each
bank's own case array (sscn:docs/XRAY_DATASET_USAGE.md, regenerated 2026-09-23) unless marked crops. Every row is HOME.

#### A1. Render and pseudo-label directories (film sources)

| directory | date | holds | built by | consumed by | evidence |
|---|---|---|---|---|---|
| `~/films_drr` | 2026-09-13 | 9,109 real films: CSXA 4,963 + BUU lateral 3,603 + NHANES 543; 36 GB | `tools/manifest_to_drr_format.py` over the spine-detector manifest | `films_ann_*`, `films_all*`, `buu_*`, `allspine_*`, `mv_bands`, `yolo_levels` | sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 2.3, 4; sscn:slurm/reproduce_all.sh renders stage |
| `~/films_drr_buucorr` | 2026-09-17 | the same 9,109, BUU schema corrected (`needs_review` flags) | `tools/correct_buu_schema.py` | counting, sweep and reader-study jobs | sscn:tools/correct_buu_schema.py; sscn:slurm/count_films_c2.sh; sscn:slurm/reader_study.sh |
| `~/films_ap_drr` | 2026-09-13 | 3,600 BUU AP films, levels inferred, `test_eligible=false` | `tools/manifest_to_drr_format.py --source buu_full --view AP` | `buu_pair_fov48_ctx` (deleted); FluoroGen source | sscn:slurm/launch_dual.sh; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 4 |
| `~/films_smoke` | 2026-09-13 | 3 CSXA films | smoke test | none | sscn:SchwingNet/results/corpus_census.md section 3 |
| `~/nhanes_drr` | 2026-09-12 | 543 NHANES annotated films (364 subjects) | `tools/nhanes_to_drr_format.py` (`slurm/nhanes_build.sh`) | `nhanes_ctx`, `nhanes_split_ctx`, `verse_only_ctx_plus_nh`, `allspine_fov96/v2/v6/v7` (the double inclusion) | sscn:slurm/nhanes_build.sh; sscn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md |
| `~/nhanes_pseudo` | 2026-09-16 | 16,234 anns (15,746 with a named level) | `tools/pseudolabel_real_films.py --source NHANESPS` | `nhanesps_fov96_ctx`; `~/review_pack` | sscn:slurm/reproduce_all.sh pseudo stage; sscn:docs/DATA_COMPLETENESS_AUDIT.md Repairs |
| `~/vindr_det_drr` | 2026-09-13 | 2,328 VinDr laterals, boxes with no names | `slurm/vindr_pseudolabel.sh` (view classifier + `detect_films.py`) | input to `pseudolabel_films.py` | sscn:slurm/vindr_pseudolabel.sh; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 4 |
| `~/vindr_pseudo_drr` | 2026-09-13 | 744 VinDr films, model-named | same | `vindr_fov96_ctx` | sscn:docs/DATASHEET.md section 2.6 |
| `~/vindr_pseudo` | 2026-09-16 | 10,274 anns (7,625 named) | `slurm/vindr_label.sh` (both splits) | `vindrps_fov96_ctx` | sscn:slurm/vindr_label.sh; sscn:docs/DATASHEET.md section 2.6 |
| `~/lateral236_pseudo` | 2026-09-16 | 236 anns | `tools/pseudolabel_real_films.py --source LAT236PS` | `lat236ps_fov96_ctx`; `~/review_pack` | sscn:slurm/reproduce_all.sh pseudo stage |
| `~/pseudo_filtered` | 2026-09-17 | anchored subsets: NHANES 10,087, VinDr 5,131, lateral236 203 | `tools/filter_pseudolabels.py` (`slurm/data_fixes.sh`) | the anchored-admission arm (refuted) | sscn:SchwingNet/results/corpus_census.md section 3; mem:remedies-refuted-2026-09-17.md |
| `~/aasce_drr` | 2026-09-15 | 457 AASCE films | `tools/aasce_to_drr.py` | `aasce_fov96_ctx` | sscn:docs/DATA_COMPLETENESS_AUDIT.md |
| `~/mendeley_drr` | 2026-09-16 | 584 films (500 `duplicate_of` BUU) | `tools/mendeley_to_render.py` | `mendeley_fov96_ctx` | same |
| `~/spinalai_drr` | 2026-09-16 | 8,358 machine-generated films (44 identities) | `tools/spinal_ai2024_to_render.py` | none | same |
| `~/fluorocap_drr`, `~/fluorocap_drr_smoke` | 2026-09-18 | 2,385 and 137 literature panels | `tools/fluorocap_to_ann.py` (`slurm/overnight_v7.sh`) | `fluorocap_fov96_ctx` | sscn:slurm/overnight_v7.sh |
| `~/fluorocap_pack` | 2026-09-18 | 1,500 panels for readers, caption shown | `tools/build_fluorocap_pack.py` | reader review | sscn:tools/build_fluorocap_pack.py; sscn:docs/DATA_COMPLETENESS_AUDIT.md |
| `~/review_pack`, `~/review_pack_smoke`, `~/review_pack_v2` | 2026-09-17/18 | 1,500 pseudo-labelled films from `nhanes_pseudo` + `lateral236_pseudo` | `tools/build_review_pack.py` (`slurm/review_pack.sh`) | private HF Space `gregoryschwingmdphd/level-review` | sscn:slurm/review_pack.sh |
| `~/reader_study` | 2026-09-18 | limited-field strips from `films_drr_buucorr` and `ctsp_drr` | `tools/build_reader_study.py` | assisted-naming reader study | sscn:slurm/reader_study.sh |
| `~/film_style_ds` | 2026-09-17 | real films for the film-look LoRA, FluoroCap excluded by assertion | `tools/film_style_dataset.py` | `~/fluorogen/lora_film_v1` | sscn:tools/film_style_dataset.py |
| `~/yolo_levels` | 2026-09-13 | `films_drr` in YOLO format, 7,456 / 1,653 films, 6.7 GB | `tools/make_yolo_levels.py` (named in `slurm/xr_bench.sh`; the tool is not in the local checkout) | level-as-class YOLO11m (M102) | sscn:slurm/xr_bench.sh; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 2.3, 5.3 |
| `~/buu_yolo` | 2026-09-18 | BUU five-class baseline set | `tools/buu_baseline.py build` | BUU baseline | sscn:tools/buu_baseline.py |
| `~/sacrum_yolo` | 2026-09-18 | 5,110 images with a sacrum box (CT renders, oblique renders, real films) | `tools/build_sacrum_dataset.py` | sacrum detector (`slurm/sacrum_detector.sh`) | sscn:tools/build_sacrum_dataset.py |
| `~/fluorogen/*`, `~/*_drr_film` | 2026-09-17 | FluoroGen outputs (card D19) | card D19 | `sd_fov96_ctx` | card D19 |

#### A2. Crop banks present on 2026-10-07

| bank | date | films | what it holds | built by | model / use | evidence |
|---|---|---:|---|---|---|---|
| `allspine_v9_fov96_ctx` | 2026-09-23 | 18,565 | `films_drr` + `ctsp_drr` + `verse_drr` + `physics_drr` + `physics_rare`, patient-keyed, VerSe re-keyed; CSXA 4,963, BUU 3,603, NHANES 543; 0 VinDr, 0 FluoroCap | `slurm/allspine_v9_bank.sh` | the reported level model: `slurm/allspine_v9_train.sh` → `~/allspine_v9_fov96_ctx/runs/model_rung_1*.pt` + `~/model_night/heads_mixed/*allspine_v9_mixed_kmax4_seed*` | sscn:slurm/allspine_v9_bank.sh; sscn:slurm/allspine_v9_train.sh; sscn:docs/XRAY_DATASET_USAGE.md |
| `allspine_v8_fov96_ctx` | 2026-09-22 | 18,565 | same sources, before the VerSe re-key | `slurm/allspine_v8_bank.sh` | `slurm/allspine_v8_train.sh`; the `a5.json` plain-film naming numbers | sscn:slurm/allspine_v8_bank.sh; sscn:SchwingNet/packet_src/statements.md item 6 |
| `allspine_v7_fov96_ctx` | 2026-09-18 | 29,105 | v2 + `fluorocap_fov96_ctx` + `vindrps_fov96_ctx` (164,161 crops) | `slurm/overnight_v7.sh` | encoder `r18_ce` (reproduce_all encoders stage); the holdout bank for 57 evaluation references | sscn:slurm/overnight_v7.sh; sscn:slurm/reproduce_all.sh; mem:grid-quota-and-deleted-banks.md |
| `allspine_v7nofluoro_fov96_ctx` | 2026-09-18 | 27,077 | v7 without FluoroCap | FluoroCap ablation | `r18_ce_v7nofluoro`, `r18_la_v7nofluoro` | sscn:slurm/fluorocap_ablation.sh |
| `allspine_v6_fov96_ctx` | 2026-09-17 | 19,095 | v2 with anomalous BUU films moved out of training, anomalous CT renders oversampled x4 | `tools/build_v6_bank.py` | model not recorded in files read | sscn:slurm/reproduce_all.sh banks stage |
| `allspine_fov96_ctx` | 2026-09-14 | 14,395 | `films_drr`, `nhanes_drr`, `ctsp_drr`, `verse_drr`, `physics_drr` | `slurm/allspine_bank.sh` | `model_rung_1_aug2.pt` (job 40249667) | sscn:slurm/allspine_bank.sh; mem:level-model-bank-coverage.md |
| `films_all2_fov96_ctx` | 2026-09-13 | 9,853 | CSXA 4,963, BUU 3,603, VinDr 744, NHANES 543; 14 classes live, no T2-T11 | merge of a deleted `.raw` parent + `extra_fov96_ctx` | the deployed level model's bank; `recurrent_head_films_all2_*` | sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 3; mem:level-model-bank-coverage.md |
| `films_ann_fov96_ctx` | 2026-09-13 | 5,506 | CSXA + NHANES only | merge of a deleted `.raw` parent | the 98.69 / 99.13 / 99.41 recurrent-head result (weights never saved) | sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 3, 7.3, 7.5 |
| `films_all2_fov128m_ctx` | 2026-09-14 | 0 | empty directory | none | none | sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.1 |
| `buu_fov96_ctx` | 2026-09-13 | 3,603 | BUU laterals, all train, 5 classes | not recorded | → `extra_fov96_ctx` → `films_all2` | sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 3 |
| `extra_fov96_ctx` | 2026-09-13 | 4,347 | BUU + VinDr 744, all train | not recorded | → `films_all2` | same |
| `vindr_fov96_ctx` | 2026-09-13 | 744 | VinDr model-named laterals (3,679 crops) | `slurm/vindr_pseudolabel.sh` stage 3 | → `extra`, `films_all2`, `allspine_v3/v4` | sscn:docs/DATASHEET.md section 2.6 |
| `vindrps_fov96_ctx` | 2026-09-18 | 7,625 | `vindr_pseudo` (43,244 crops) | `slurm/overnight_v7.sh` | → `allspine_v7` | same |
| `nhanesps_fov96_ctx` | 2026-09-16 | 15,746 | `nhanes_pseudo` | `slurm/corpus_expand.sh` | → `allspine_v5` (deleted) | sscn:slurm/corpus_expand.sh |
| `lat236ps_fov96_ctx` | 2026-09-16 | 212 | `lateral236_pseudo` | `slurm/corpus_expand.sh` | → `allspine_v5` (deleted) | same |
| `aasce_fov96_ctx` | 2026-09-15 | 457 | `aasce_drr` (no READY marker) | `slurm/aasce_crops.sh` | → `allspine_v4`, `v5`, `v5c` (deleted) | sscn:slurm/aasce_crops.sh; sscn:docs/DATA_COMPLETENESS_AUDIT.md |
| `mendeley_fov96_ctx` | 2026-09-16 | 584 | `mendeley_drr` | `slurm/corpus_expand.sh` | → `allspine_v5`, `v5c` (deleted) | same |
| `fluorocap_fov96_ctx` | 2026-09-18 | 2,385 | `fluorocap_drr` (14,957 crops) | `slurm/overnight_v7.sh` | → `allspine_v7`, `carm_mix` and folds | sscn:docs/DATA_COMPLETENESS_AUDIT.md |
| `nhanes_ctx`, `nhanes_split_ctx` | 2026-09-13 | 543 each | `nhanes_drr`; `nhanes_ctx` is val-only (pure held-out test bank) | not recorded | NHANES test evaluations | sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 3 |
| `verse_only_ctx_plus_nh` | 2026-09-13 | 917 | `verse_drr` 374 + `nhanes_drr` 543 | merge | five weight files with no registry row | same, sections 3 and 7.2 |
| `mv_bands` | 2026-09-13 | 5,517 | multi-vertebra bands from CSXA, BUU, NHANES | `tools/make_mv_bands.py` (named in `slurm/mv_bench.sh`; the tool is not in the local checkout) | sequence-head benchmark | sscn:slurm/mv_bench.sh |
| `sd_fov96_ctx` | 2026-09-18 | 9,443 | film-LoRA-styled CT renders | `slurm/film_lora_apply.sh` | → `allspine_v2sd_fov96_ctx` | sscn:slurm/film_lora_apply.sh |
| `carm_mix_fov96_ctx`, `carm_cvmix0..4`, `carm_cvdaymix0..2`, `carm_cvdaymix0_v9` | 2026-09-21..23 | 9,555-9,641 | capped mix: CSXA, BUU, NHANES (both copies), CT renders, FLUOROCAP, VINDRPS, C-ArmLSpine AP/LAT (fold 0: 31,446 crops) | `tools/merge_banks.py --per-class 600 --real-share 0.5` (`slurm/carmlspine_cv*.sh`) | C-ArmLSpine five-fold encoder fine-tunes | sscn:docs/MODEL_CARD.md section 3.2; sscn:slurm/carmlspine_cv.sh |
| cross-family, listed for completeness: `carm_fov96_ctx`, `carm_cv0..4`, `carm_cvday0..2` (C-ArmLSpine only); `m_fov96_ctx`, `m_mask22_scale_ctx`, `merged_ctx`, `verse_ctx`, `verse_only_ctx`, `obl2_fov96_ctx`, `exp3_ctx_fluoro`, `exp3_ctx_radiograph` (CT renders only) | | | | | | sscn:docs/XRAY_DATASET_USAGE.md; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 3 |

#### A3. Banks that no longer exist

- `allspine_v2`, `v3`, `v4`, `v5`, `v5c`: deleted 2026-09-20 to recover 259.6 GB; their train/val lists and the builder copy for v3-v5 are gone (mem:grid-quota-and-deleted-banks.md; sscn:docs/DATA_COMPLETENESS_AUDIT.md group row).
- Dropped by `slurm/disk_cleanup.sh`: `films_all3_fov96_ctx`, `films_all2_fov48_ctx`, `films_all2_fov128_ctx`, `films_all_fov48_ctx`, `films_ann_fov48_ctx`, `films_ann_fov48_scale_ctx`, `buu_fov48_ctx`, `extra_fov48_ctx`, `vindr_fov48_ctx`, `nhanes_fov48_split_ctx`, `nhanes_fov_48_ctx`, `vo_fov48_ctx`, `vo_fov48_plus_nh_ctx`, `vo_mask48_ctx`, `vsoft_fov48_ctx`, `buu_pair_fov48_ctx`, and the raw `buu_drive` (sscn:slurm/disk_cleanup.sh).
- Absent from the 2026-10-07 listing with no deletion record found: `films_all4_fov96_ctx`, `extra3_fov96_ctx`, `extra4_fov96_ctx`, `obl_fov96_ctx`, `allspine_v2sd_fov96_ctx`; the five `.raw` merge parents are gone (census:toplevel_listing.txt; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.1).

---

### Appendix B — Facts that bear on moving family D to CEPH

1. Every raw film corpus is on HOME under `~/spine-detector/data/raw/{csxa, buu_full, buu_2000 -> ~/XRSpinoPelvic1K/data/BUU-LSPINE, buu_v1, cm_spine, nhanes_annotated, nhanes_full, aasce, vindr, mendeley_716, lateral_236, spinal_ai2024}` (sscn:docs/DATA_COMPLETENESS_AUDIT.md re-count listing of the raw directory). CEPH holds only the AASCE mirror (`data/thoracic_xr`), VinDr identity/audit files (`data/vindr`), the film inventories (`data/inventory/films`), the public fluoroscopy videos (`data/external/fluoro_video`) and the Bournemouth tracks (`data/realxray/bournemouth_qf`) (cards D09, D10, D20, D21).
2. Symlinks to carry across: `~/spine-detector/data/raw/buu_2000` → `~/XRSpinoPelvic1K/data/BUU-LSPINE`; `~/XRSpinoPelvic1K/data/{ct,labels}` already dangle (sscn:docs/DATA_COMPLETENESS_AUDIT.md; sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md section 7.1).
3. Code that hard-codes the HOME paths: `tools/xray_dataset_usage.py` (`RAW`, `RENDER_DIRS`), `tools/film_corpus_inventory.py` (`RAW = H / "spine-detector/data/raw"`, `LEVEL_BANKS`), `tools/audit_film_corpora.py`, `slurm/film_corpus_inventory.sh` (writes into `nhanes_full`), `slurm/vindr_label.sh`, `slurm/thoracic_xr_fetch.sh` (`--grid-copy`), `slurm/reproduce_all.sh` (data, renders, pseudo stages) (each file under sscn:).
4. Person keys depend on path fragments: `tools/patient_keys.py` lines 210-212 map `"/vindr"`, `"lateral236"` and `"/raw/lateral_236/"` to corpora, so a new layout must keep those fragments or the rules must change (sscn:tools/patient_keys.py). The evaluation gate finds a checkpoint's lineage by path and by sha256 (sscn:docs/DATA_ACCOUNTING.md section 5.3).
5. Access: `/rs/rs_grp_oschome/go2432` is `drwxr-s---` with group `oschome` = go2432 and <C&IT admin account, username withheld> (mem:grid-access-list-gate.md). VinDr-SpineXR is held under a named person's PhysioNet DUA (sscn:SchwingNet/packet_src/statements.md), and BUU-LSPINE's EULA forbids redistribution (mem:lstv-data-landscape.md); whether group read by a second account is allowed under those terms is not recorded.
6. Do not read or move as data: `~/.fluorocap` (harvester credentials) and the token files in HOME (mem:fluorocap-credentials-and-resolution.md; census:toplevel_listing.txt).
7. Size levers recorded so far: the NHANES annotated pickles take 159 GB extracted against a 1.0 GB zip that regenerates them; FluoroCap is 316 GB of which `youtube/` is the bulk (sscn:docs/MANIFEST_DATA_MODELS_RESULTS.md sections 2.1 and 7.4). Directive D2 already asks for all NHANES films on CephFS (sscn:docs/RESUME_2026-09-22_PM.md "D2").
8. The 2026-10-07 census (`$RS/data/inventory/census_2026-10-07/{census.json,census.tsv,depth2.tsv}`) should replace every size in this file once it lands.

---

## 9. Family E: the disk map

Family E mapped every top-level entry of HOME and Ceph to a source. Its cards are merged into the cards above as their `[E]` parts. Its full entry-by-entry table is `plan/disk_map.csv` (1,479 rows) and the migration mapping built from it is in `LAYOUT.md`; its hard-coded-path scan feeds `MIGRATION_PLAN.md`. Its method, legend and numbers, verbatim:

Built 2026-10-07 from local files only; nothing on the grid was contacted. This family maps disk entries to sources. The other families describe each source in depth. Where this file says something about a source that another family also covers, both are kept, and the other family's card is the authority on origin and licence.

### 0. Inputs, method and the evidence legend

**What was classified.** Every entry in the 2026-10-07 top-level listing (`scr:census/toplevel_listing.txt`): HOME top level (1,301 entries), HOME/data (6), the Ceph root (26), Ceph `data/` (47), Ceph `data/anomaly_harvest/` (24) and Ceph `archive/` (0 entries listed). That is 1,404 rows. Another 75 depth-2 rows name sub-folders that a manifest or a du file sizes, such as `~/CTSpinoPelvic1K/data/tcia` and `~/spine-detector/data/raw/*`. All 1,479 rows are in `scr:dataplan/cards/disk_map.csv`, with columns `path,storage,role,source_id,size_gb,size_source,date,notes`.

**How.** `scr:dataplan/build_disk_map.py` holds an explicit role, source id and note for every directory and for every notable file, and each one cites the evidence it came from. Loose files with no explicit entry (443 `.py`, 178 `.sh`, logs, PNGs, JSON probe outputs) are classified by rule: script, log, figure or probe output. `scr:dataplan/render_tables.py` writes the tables in this file from the CSV, so the two cannot disagree. `scr:dataplan/grep_paths.py` scans both repositories for hard-coded grid paths (section 4).

**Roles.** These are the seven roles the brief set: raw imaging source; converted or derived imaging (renders, banks, nnU-Net datasets, pseudo-labels, splits, segmentations); model or result (weights, benches, logs); software or environment; non-imaging data; scratch or scripts; unknown.

**Sizes.** The listing carries no sizes. Each size in the CSV names its source, and those sources have different dates:
- `_du_home.txt` and `_du_data.txt` are `du -h` output in binary units from 2026-09-01. T is converted to G by multiplying by 1,024. These values predate everything created or deleted after 2026-09-01.
- `MANIFEST_DATA_MODELS_RESULTS.md` is from 2026-09-16.
- `RSNAI_DATA_MANIFEST.json` is from 2026-09-22.
- `CENSUS_TABLE_2026-09-25.md` (du -sBG) is from 2026-09-25.
- `DATA_COMPLETENESS_AUDIT.md` is from about 2026-09-23.
- `mem:grid-quota-and-deleted-banks` is from 2026-09-20.

Sizes are therefore not additive across sources or dates. Ceph storage census job 40578909 will replace all of them once it finishes. Its output was not available here.

**Evidence legend.**

| tag | full path |
|---|---|
| `scr:` | `<session scratchpad; not a dependency>/` |
| `nnunet:` | `<repo spinesurg-ct-nnunet 097933a>/` |
| `ctsp:` | `<repo CTSpinoPelvic1K 7ddfe38>/` |
| `mem:` | `<memory notes; see MEMORY.md>/` (`.md` omitted) |
| `MANIFEST_DATA_MODELS_RESULTS.md`, `RSNAI_DATA_MANIFEST.json`, `CENSUS_TABLE_2026-09-25.md`, `DATA_COMPLETENESS_AUDIT.md`, `CT_INVENTORY.md`, `XRAY_DATASET_USAGE.json`, `DATA_ACCOUNTING.md`, `DATASHEET.md` | `nnunet:docs/<name>` |
| `corpus_census.md` | `nnunet:SchwingNet/results/corpus_census.md` (2026-09-24) |
| `ranking.csv`, `jobs.txt` | `nnunet:SchwingNet/results/transitional_registry/acquisition/<name>` |
| `_du_home.txt`, `_du_data.txt`, listing | `scr:census/` |

### 1. The map in numbers

| section | entries | raw imaging source | converted or derived imaging | model or result | software or environment | non-imaging data | scratch or scripts | unknown |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HOME top level | 1301 | 7 | 151 | 305 | 142 | 26 | 656 | 14 |
| HOME/data | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ceph root | 26 | 1 | 1 | 6 | 11 | 6 | 1 | 0 |
| Ceph data/ | 47 | 27 | 14 | 5 | 0 | 0 | 0 | 1 |
| Ceph data/anomaly_harvest/ | 24 | 0 | 23 | 1 | 0 | 0 | 0 | 0 |
| **all** | **1404** | **41** | **189** | **317** | **153** | **32** | **657** | **15** |
| Ceph archive/ | 0 | the listing shows no entries | | | | | | |

Sized entries only, from the cited sizes. Several are stale (see 0):

| storage | role | entries with a size | GB (sum of the cited sizes; dates differ, see each row) |
|---|---|---:|---:|
| CEPH | converted or derived imaging | 23 | 657.3 |
| CEPH | model or result | 1 | 682.0 |
| CEPH | raw imaging source | 25 | 3,408.3 |
| HOME | converted or derived imaging | 11 | 1,899.5 |
| HOME | model or result | 21 | 307.9 |
| HOME | non-imaging data | 22 | 196.4 |
| HOME | raw imaging source | 9 | 3,040.9 |
| HOME | scratch or scripts | 86 | 2.4 |
| HOME | software or environment | 47 | 69.6 |
| HOME | unknown | 10 | 0.1 |

**What these numbers show** (each line cites its source):

- **No top-level entry links HOME to Ceph.** The listing section "symlinks in HOME that point at ceph" holds only `.ashley -> .beethoven`, and "symlinks in HOME/data that point elsewhere" is empty (listing). `mem:grid-ceph-volume-oschome` describes datasets "moved from ~/data with rsync, then symlinked". In the 2026-10-07 listing, no HOME data folder is such a link. Every HOME imaging folder is a real directory and has not been migrated.
- **HOME is close to its limit.** It holds 4,050 GB against a 4,295 GB soft quota (pan_quota 2026-10-07, from the orchestrator's brief; no file holds this number). Ceph used 4,482 GB (22 % of 20 TB) on 2026-09-25 (`CENSUS_TABLE_2026-09-25.md` 4). The brief puts it at about 6 TB on 2026-10-07.
- **Most of HOME is three trees.**
  - `~/CTSpinoPelvic1K`: 1.9T on 2026-09-01, almost all of it `data/`. That includes TCIA DICOM 721G, `tcia_nifti` 336G, `hf_export` 328G, `hf_export_osc` 227G and `ctspine1k` 190G (`_du_data.txt`).
  - `~/spinesurg-ct-nnunet`: 1.4T on 2026-09-01 (`_du_home.txt`), 363G on 2026-09-19 (ssn:docs/CONTINUANCE_2026-09-19.md L27), of which `nnunet/results` is 348.6 GB (`mem:grid-quota-and-deleted-banks`).
  - `~/FluoroCap`: 316 GB, of which `youtube/` is 181 GB (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1; `DATA_COMPLETENESS_AUDIT.md` line 761).
- **The `~/CTSpinoPelvic1K/data` sizes may be stale.** `ctsp:slurm/reclaim_grid_space.sh` (committed 2026-09-07) lists `ctspine1k`, `ctpelvic1k`, `hf_export_v2_work`, `hf_export_v3_work`, `hf_export_v4`, `hf_export_v5`, `hf_export_osc`, `zenodo_v6`, `zenodo_upload` (phase A) and `placed`, `v5_final`, `s1_recarve`, the hardware and 0816 folders and `hf_export_v6` (phase B) for deletion. Its default is a dry run. A memory note says phases A and B ran on 2026-09-07 (mem:zenodo-deposit.md L30); no job log is on this laptop, so these folders are presumed deleted pending the census. `DATA_COMPLETENESS_AUDIT.md` line 142 says `~/CTSpinoPelvic1K/data/hf_export` "has since been deleted".
- **The largest Ceph holdings** are `data/cobra2026` 754 GB, `data/or_ready` 682 GB, `data/idc` 658 GB, `data/abdomenatlas3_mini` 532 GB, `data/tcia_fdg_pet_ct_lesions` 367 GB, `data/panorama` 182 GB, `data/ctspine1k` 152 GB and `data/deepfluoro_vendor` 104 GB (`CENSUS_TABLE_2026-09-25.md` 1 and 4).
- **Copies that exist twice** (a migration should keep one and point the other at it):
  - CTSpine1K: `~/CTSpinoPelvic1K/data/ctspine1k` on 2026-09-01 (`_du_data.txt`) and `$RS/data/ctspine1k` (listing 2026-09-23).
  - AASCE: `~/spine-detector/data/raw/aasce` holds 481 training films, a subset of the 609-film mirror at `$RS/data/thoracic_xr` (`DATA_COMPLETENESS_AUDIT.md` lines 335, 570, 572).
  - RibFrac: zips in `~/data/ribs`, unzipped images in `$RS/data/ribfrac` (`nnunet:tools/other_ct_fetch.py` header).
  - TotalSegmentator: v2 and v3 each keep both the zip and the unpacked tree on HOME (`DATA_COMPLETENESS_AUDIT.md` lines 483-486).
  - BUU-LSPINE: `buu_drive` and `buu_v1` are byte-identical subsets of `buu_full`, and `buu_2000` is a symlink into `~/XRSpinoPelvic1K` (`MANIFEST_DATA_MODELS_RESULTS.md` 2.1).
  - `model_night` and `singularity_cache` exist on both HOME and Ceph (listing).
- **Hard links, not copies.** The 802 CTs in `~/data/CTSpinoPelvic1K/ct` were "hard-linked from the existing export (no second copy)" (`ctsp:slurm/archive_build_inputs.sh` header). The reclaim script refuses to delete export trees unless the CT store survives "as hard links in the working copy" (`ctsp:slurm/reclaim_grid_space.sh`). The 227 GB of `~/data/CTSpinoPelvic1K` and the 1.9T of `~/CTSpinoPelvic1K` were measured by separate du runs and may count the same inodes twice. A copy without `rsync -H` would also turn each link into a second full copy.

### Family E group note: 2.1.1 Acquisition collections screened for transitional anatomy (17 Ceph sources)

All 17 cards below share several facts:
- **Route**: `nnunet:tools/acquisition_fetch.py`, called per collection by `nnunet:slurm/acquisition_submit.sh`. Zenodo files are verified against the record's md5, HF files against the LFS sha256, and IDC/NBIA series against the catalogue's instance count. Nothing is signed into (`nnunet:tools/acquisition_fetch.py` docstring).
- **Layout**: `$RS/data/<collection>/{raw,fetch}`. The state of each fetch is in `fetch/verified.jsonl` and `FETCH_STATUS.json`.
- **Annotation status**: project pseudo-labels only. These are TotalSegmentator and SPINEPS+VERIDAH segmentations plus a two-labeller L6/T13 call in `$RS/data/anomaly_harvest/<collection>` (`CENSUS_TABLE_2026-09-25.md` 1). Release annotations, where they exist, are not used and not recorded here.
- **Position/view**: not recorded for any of the 17.
- **Re-acquisition**: `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh tier1` for the seven collections of 2026-09-23 and `... tier1_late` for the ten found on 2026-09-24. Both skip finished units (`nnunet:slurm/acquisition_submit.sh` header). Each card below gives the per-collection command, sizes from `CENSUS_TABLE_2026-09-25.md` and the Ceph folder date from the listing.

### Family E group note: 2.3 Plain film (CR/DX)

Shared fact: the HOME raw copies of these corpora sit under `~/spine-detector/data/raw/`. Their download tool, `~/spine-detector/scripts/download_sources.py`, exists only on the grid and is not in the repositories read (`DATA_COMPLETENESS_AUDIT.md` lines 335, 585).

#### 2.5 Disk entities that other families card as their own ids

These rows give only the location. The origin, licence and recipe are in the named family's card.

| id | family | what | where (generated from disk_map.csv) |
|---|---|---|---|
| `ctspinopelvic1k_april` | A | the April 2026 release (1,153 records) staged on Ceph and used for the NeurIPS SPINEPS runs (`RESUME_2026-09-22_PM.md` line 139) | `$RS/data/ctsp_april` (CEPH, converted/derived, listing 2026-09-27) |
| `ctspinopelvic1k_build_tree` | A | the intermediate trees under `~/CTSpinoPelvic1K/data` and the build-archive staging (`ctsp:slurm/archive_build_inputs.sh`) | `~/CTSpinoPelvic1K` (HOME, raw, 1,945.6 GB, listing 2026-09-13); `~/build_archive` (HOME, converted/derived, listing 2026-09-07); `~/build_archive_private` (HOME, converted/derived, listing 2026-09-07); `~/build_archive_stage` (HOME, converted/derived, listing 2026-09-07); `~/CTSpinoPelvic1K/data/hf_export` (HOME, converted/derived, 328.0 GB); `~/CTSpinoPelvic1K/data/hf_export_osc` (HOME, converted/derived, 227.0 GB); `~/CTSpinoPelvic1K/data/placed` (HOME, converted/derived, 6.1 GB); `~/CTSpinoPelvic1K/data/hf_export_v6` (HOME, converted/derived, 4.6 GB); `~/CTSpinoPelvic1K/data/hf_export_v5` (HOME, converted/derived, 4.6 GB); `~/CTSpinoPelvic1K/data/hf_export_v4` (HOME, converted/derived, 2.8 GB); `~/CTSpinoPelvic1K/data/hf_export_v3` (HOME, converted/derived, 2.4 GB); `~/CTSpinoPelvic1K/data/zenodo_v6` (HOME, converted/derived, 2.3 GB); `~/CTSpinoPelvic1K/data/v5_final` (HOME, converted/derived, 2.3 GB); `~/CTSpinoPelvic1K/data/zenodo_upload` (HOME, converted/derived, 2.2 GB); `~/CTSpinoPelvic1K/data/hf_export_v2` (HOME, converted/derived, 2.1 GB); `~/CTSpinoPelvic1K/data/s1_recarve` (HOME, converted/derived, 1.6 GB); `~/CTSpinoPelvic1K/data/hardware_fix` (HOME, converted/derived, 0.4 GB); `~/CTSpinoPelvic1K/data/hf_export_v2_work` (HOME, converted/derived, 0.3 GB); `~/CTSpinoPelvic1K/data/fix_0816` (HOME, converted/derived, 0.2 GB); `~/CTSpinoPelvic1K/data/fix_0816_v3` (HOME, converted/derived, 0.2 GB); `~/CTSpinoPelvic1K/data/hip_crossover_backup` (HOME, converted/derived, 0.1 GB); `~/CTSpinoPelvic1K/data/hf_export_v3_work` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/v5_smoke` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/hardware_final_predust` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/hardware_final` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/patient_db.json` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/hip_transpose_backup` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/fix_0816_pseudo` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/thoracic_fix` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/patient_db.pkl` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/fix_0816_v4` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/0816_label_v4.nii.gz` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/fix_0816_pseudo_work` (HOME, converted/derived, <0.1 GB); `~/CTSpinoPelvic1K/data/patient_db_summary.txt` (HOME, converted/derived, <0.1 GB) |
| `nnunet_dataset802_803`, `nnunet_dataset810`, `nnunet_dataset813`, `nnunet_dataset815` | A | nnU-Net datasets inside `~/spinesurg-ct-nnunet/nnunet` (`DATA_COMPLETENESS_AUDIT.md` line 581) | `~/spinesurg-ct-nnunet` (HOME, converted/derived, 363 GB on 2026-09-19 per ssn:docs/CONTINUANCE_2026-09-19.md L27; the 1,433.6 GB of 2026-09-01 is superseded; listing 2026-09-25); `~/spinesurg-ct-nnunet/nnunet/raw` (HOME, converted/derived) |
| `implant_ct_synthetic` | A | synthetic-hardware CTs | `~/implant_ct_smoke` (HOME, converted/derived, listing 2026-09-14); `~/implant_ts` (HOME, converted/derived, 39.0 GB, listing 2026-09-14); `~/implant_verse` (HOME, converted/derived, 187.0 GB, listing 2026-09-14); `~/implant_verse_smoke` (HOME, converted/derived, listing 2026-09-14) |
| `lstv_flag_renders` | A | LSTV flag renders | `~/lstv_flag` (HOME, converted/derived, listing 2026-09-15) |
| `validation_ts` | B | 70-71 TotalSegmentator v2 CTs with external VertebralBodiesCT labels | `$RS/data/validation_ts` (CEPH, converted/derived, 1.0 GB, listing 2026-09-23); `$RS/data/anomaly_harvest/validation_ts` (CEPH, converted/derived, 2.0 GB, listing 2026-09-24) |
| `realxray_layout` | C | the common real-frame layout per device (`REAL_XRAY_DATASETS_SPEC.md`) | `$RS/data/realxray` (CEPH, converted/derived, 3.9 GB, listing 2026-09-26); `$RS/data/realxray_work` (CEPH, converted/derived, listing 2026-09-21) |
| `or_ready` | C | readiness-program results, models and dumps (682 GB on 2026-09-25) | `$RS/data/or_ready` (CEPH, model/result) |
| `xrspinopelvic1k` | D | the XRSpinoPelvic1K tree (BUU-LSPINE 2000, xrsp1k DRRs, unopened `dataset2024.zip`) | `~/XRSpinoPelvic1K` (HOME, raw, 32.0 GB, listing 2026-08-10) |
| `spine_detector_corpus` | D | `~/spine-detector`: the raw film corpora plus YOLO detector datasets and runs | `~/spine-detector` (HOME, raw, listing 2026-09-13) |

### Family E section 4 (hard-coded grid paths), summary paragraphs verbatim

#### 4. Hard-coded grid paths a migration must keep working

**Scan.** Code files (`.py .sh .sbatch .yaml .yml .ipynb .js` and others; documents and results excluded) were scanned in `nnunet:{slurm,tools,nnunet,scripts,env,containers,service,benchmark,SchwingNet,docker}` and in `ctsp:{scripts,slurm,tools,configs,containers,docker,review_service,reviewtool,hf,infobot,tests,zenodo,paper,mlhc,Student_Projects,...}`. The scan looked for `/wsu/home/go/go24/go2432/…`, `$HOME/…`, `${HOME}/…`, `~/…`, `Path.home()/"…"` and `/rs/rs_grp_oschome/go2432/…` (`scr:dataplan/grep_paths.py`).

**Result.** 1,358 files carry at least one reference. There are 6,025 references to 196 distinct top-level folders, of which 137 exist in the 2026-10-07 listing and 59 do not. Every reference, with file and line, is in `scr:dataplan/path_refs_files.csv`, and the counts are in `scr:dataplan/path_refs_summary.csv`.

**How to read the absent ones.** They fall into four groups:
- Banks deleted on 2026-09-20: `allspine_v2/v3/v5_fov96_ctx` (`mem:grid-quota-and-deleted-banks`).
- Directories that no longer exist: `implant_ct` (`DATA_COMPLETENESS_AUDIT.md` line 629).
- Paths on WSL or the local machine, not the grid: `FluoroCap_wsl`, `FluoroCap_lstv`, `FluoroCap_lstv2` and `FluoroCap_s2` (`DATA_COMPLETENESS_AUDIT.md` line 330), plus `OneDrive`, `.TinyTeX`, `Student_Projects`, `miniforge3` and `itksnap` from `ctsp:paper`, `ctsp:Student_Projects` and `ctsp:reviewtool`.
- f-string prefixes that are not folders: `carm_cv`, `carm_cvmix`, `carm_cvday`, `patient_keys`, `nhanes_`, `x`.

The scan treats a `$RS`, `$CEPH` or `$OSCHOME` variable as the Ceph root. Some scripts set it to `data/` instead: `nnunet:SchwingNet/tools/corpus_census.py` line 57 sets `RS = "/rs/rs_grp_oschome/go2432/data"`. So the Ceph `realxray/…` keys really mean `data/realxray/…`, which exists, and other variable-based Ceph keys may be one level off. `review_tree` is the default output root of `nnunet:tools/transitional_review/build_review_tree.py`, which has not been created yet.

#### 4.5 What the migration has to preserve (from the files above)

- **The folders scripts read most.** `~/model_night` is referenced by 526 code files, mostly as a log directory. `~/spinesurg-ct-nnunet` has 454, `~/mambaforge` 440, `~/tmp` 256, `~/spine-detector` 118, `~/data` 97 and `~/FluoroCap` 83 (section 4.1). Moving any of them without a symlink at the old path breaks these scripts. The method `mem:grid-ceph-volume-oschome` gives is `rsync -a --remove-source-files`, then a symlink at the old path.
- **Never rewrite the Dataset810/813/815 `imagesTr` links.** They are container bind paths (`/data/hf_export/ct/...`), and an earlier host-side "repair" wiped a dataset (`mem:dataset813-image-links-are-container-paths`). Move the CT store, keep `HF_EXPORT_DIR` pointing at a directory with a `ct/` subfolder, and leave the links alone.
- **Links already inside the trees.** These must survive a copy (`rsync -a` keeps symlinks as symlinks, and an absolute target must be re-pointed or kept resolvable):
  - `~/bench/ct_by_case` holds 802 symlinks (`MANIFEST_DATA_MODELS_RESULTS.md` 2.3).
  - `~/VerSeFusion/data/unified` holds 88 MB of links (`DATA_COMPLETENESS_AUDIT.md` line 662).
  - `~/spine-detector/data/raw/buu_2000` links to `~/XRSpinoPelvic1K/data/BUU-LSPINE` (line 530).
  - `$RS/data/validation_ts` links the 70 TotalSegmentator CTs (`jobs.txt`).
  - `~/XRSpinoPelvic1K/data/{ct,labels}` are already dangling (`MANIFEST_DATA_MODELS_RESULTS.md` 7.1).
- **Keep hard links.** Copy the CTSpinoPelvic1K trees with `rsync -aH`, and move `~/CTSpinoPelvic1K/data` and `~/data/CTSpinoPelvic1K` in the same rsync call. Hard links cannot span the Panasas and Ceph filesystems, so files moved separately become separate full copies (`ctsp:slurm/archive_build_inputs.sh` header).
- **Never `ln -sf` a model.** Chains use `model_registry.py link` (`mem:model-registry`). `~/model_registry` holds a content-addressed store and `~/mlflow` an SQLite database (`mem:model-registry`). Whether either records absolute HOME paths is not recorded in Family E's evidence, so check this before moving them.
- **Credential and key stores are named here only by path, and were not read.** They are `~/.hf_org_token`, `~/.hf_osc_token`, `~/.zenodo_token`, `~/.kaggle`, `~/.fluorocap`, `~/.netrc`, `~/.ssh`, `~/.beethoven-vendor`, `~/private` and `~/pass_file`. A migration of imaging data should leave them on HOME, and `$RS/private_ip` is access-restricted (listing mode `drwx--S---`).

The per-folder reference tables 4.1-4.4 are in `plan/path_refs_summary.csv` and `plan/path_refs_files.csv`; `plan/path_refs_by_item.csv` joins them to every moved item.

## 10. Unknowns, every family (verbatim)

Rows answered by the grid inspection of 2026-10-08 (scr:inspect_unknown.out) are removed: A14, D16 and E4 (`~/data/spondy_landmark` is a second download of Mendeley 5jdfdgp762), E5 (the twelve HOME entries it named and `$RS/data/morphdef`; the row now holds the two download leftovers that inspection did not reach) and E18 (`~/qc.tar.gz` holds the pelvis-propagation QC renders of 2026-06-12, not the speckle QC). The answers are in the cards `mendeley_5jdfdgp762`, `ctspinopelvic1k_build_tree` and `xrspinopelvic1k`, and in MIGRATION_PLAN.md section 5 (B14). Row A22 has a dated note.

### Family A unknowns

| # | fact not found | where it was looked for |
|---|---|---|
| 1 | Exact download day of TCIA CT COLONOGRAPHY, and whether `HOME/CTSpinoPelvic1K/data/tcia` (721 GB) and `tcia_nifti` (336 GB) still exist after 2026-09-01 | G0 §2; DUD; RECLAIM L34-L47 (not on either delete list) |
| 2 | Contents and effect of `HOME/cleanup_v1v3_tcia.sh` (2026-09-01) | LIST only; the script is not in either repo |
| 3 | Whether RECLAIM phases A and B actually ran, and what remains of `HOME/CTSpinoPelvic1K/data/*` | mem:zenodo-deposit.md says "ran the same day"; no log on this laptop |
| 4 | State of `hf_export_v2`, `patient_db.json`/`.pkl`, `placed/` after 2026-09-07 | DUD; RECLAIM; G0 §2 |
| 5 | Exact CTSpine1K HOME download day (May 2026), and the HF revision sha of either copy | `git log ctsp:slurm/download_raw.sh`; the CEPH `hf_listing.json` (on grid) holds the sha |
| 6 | Whether CTSpine1K is gated today (May "gated", Sept "ungated") | ctsp:slurm/download_raw.sh L41; ssn:tools/acquisition_census.py L396 |
| 7 | CTPelvic1K licence: CC BY 4.0 vs "NC" | ctsp:README.md L515; ctsp:docs/DATASETS_ROADMAP.md L95 |
| 8 | VerSe licence: CC BY 4.0 vs CC BY-SA 4.0 | vfr:README.md L348-L350; mem:lstv-data-landscape.md; ctsp:docs/DATASETS_ROADMAP.md L95 |
| 9 | TotalSegmentator v3 licence, stated separately | AUDIT L480 gives no licence for v3 |
| 10 | The scripts that downloaded TS v2 and v3 (`dl.log`/`dl.status` exist only on the grid) | grep of both repos for 10047292, 22688904, DL_DONE |
| 11 | Full Zenodo MD5 of `Totalsegmentator_dataset_v201.zip` | AUDIT L479 truncates it |
| 12 | `HOME/data/ribs/dl.sh` URLs, and the source URL of `ribseg_v2.zip` | ssn:docs/CONTINUANCE_2026-09-19.md L25; grep of both repos |
| 13 | RSNA 2022 licence terms for derived labels | ssn:slurm/rsna_cspine_fetch.sh L2-L5 (rules accepted only) |
| 15 | Patient position for TotalSegmentator, VerSe, CTSpine1K non-COLONOG, RibFrac, RSNA, CTPelvic1K | meta.csv fields (PIS row ts); release docs read |
| 16 | Whole-collection prone/supine breakdown for TCIA CT COLONOGRAPHY (only the 802 annotated records are counted) | MANSUM covers 802 records only |
| 17 | Whether the 768 numeric-id and 34 `CTC-` CTSP records overlap as people | mem:identity-audit-findings.md |
| 18 | Whether Zenodo v11 carries the KNOWN_ISSUES §10 (0533) note yet; whether HF labels have been moved to v11 since 2026-09-27 | mem:grid-ct-0533-truncated.md; mem:hf-mirror-is-v10.md |
| 19 | Whether the 2026-09-23 0533 re-render jobs (40416625/26/27/38) all completed, so that every CTSP bank holds 802 | AUDIT L1337, L1375-L1390 names marker lines in `HOME/model_night/logs/` (on grid) |
| 20 | Exact HF revision of `anonymous-neurips-ED/CTSpinoPelvic1K` at submission, and the exact subpath under CEPH `data/ctsp_april` that holds the April inputs (fetch job 40480758 fetched and sha-verified all 2,306 inputs of the 1,153 records for the SPINEPS run there) | CRC L350-L351; ctsp:CAMERA_READY_NEURIPS/src/appendix/spineps.tex L6-L8; ssn:docs/RESUME_2026-09-22_PM.md L139 |
| 21 | Prep command for Dataset810 | mem:lstv-oneshot-training-run.md (submit line for training only) |
| 22 | Contents of `HOME/VerSeFusion.tar.gz` and of the file `HOME/VerseFusion`. *2026-10-08: `VerSeFusion.tar.gz` is 44,461 B, dated 2026-05-11 (scr:inspect_unknown.out), too small for data; the grid reading of that day calls it the VerSeFusion code tarball (a nextflow pipeline). `HOME/VerseFusion` is still unread.* | LIST only; scr:inspect_unknown.out |
| 23 | Source CTs of `exp3_fluoro` / `exp3_radiograph` (1,058 renders over 120 cases) | MDMR L310-L311; ssn:tools/night_results.py L41-L42 |
| 24 | Whether the symlinks in `VerSeFusion/data/unified`, `bench/ct_by_case` and the nnU-Net raw trees are absolute or relative | AUDIT L662; MDMR L200-L202 |
| 25 | Licence of Spinal-AI2024; how `HOME/XRSpinoPelvic1K/data/xrsp1k` was rendered | MDMR L175, L197-L200 |
| 26 | The deposit README says the cohort was "imaged supine", but the manifest has 377 prone records; which statement the release intends | DEP L223; MANSUM |

### Family B unknowns

| fact not found | what is on disk instead | where looked |
|---|---|---|
| Per-collection converted (<= 3 mm) counts for the 39 IDC tier-1 collections | only the pooled 3,499 of 3,600 is local | acquisition/jobs.txt |
| Per-collection screen results (SUMMARY.md, rows.csv) for idc, abdomenatlas3_mini, tcia_fdg_pet_ct_lesions, amos22 and all ten late collections | on CEPH only | acquisition/ACQUISITION_PLAN.md Files here |
| FETCH_STATUS.json, verified.jsonl and failed.jsonl of every collection | on CEPH only; not read | tools/acquisition_fetch.py |
| Fetch completion times for FDG-PET-CT-Lesions, PANORAMA, Kidney, WAW-TACE and the other late collections | jobs.txt stops at 10:50 EDT 2026-09-24 | acquisition/jobs.txt |
| Outcome of the CURVAS `training_set.zip` repair chain (40436037-40436045) | 70 cases of 90 is consistent with failure; no file says | acquisition/jobs.txt; docs/ruleclass/TIERS.md |
| Why AMOS's 723 + 1,564 + 67 = 2,354 falls ten short of 2,364 | not explained | acquisition/ACQUISITION_PLAN.md section 9 |
| Refusal reasons for Barts (212 of 220), AortaSeg (55 of 60), CURVAS-PDACVI (101 of 109) | convert_summary.json on CEPH only | docs/ruleclass/TIERS.md |
| Contents of `alias_pairs.csv` / `alias_pairs_all.csv` (jobs 40426214, 40430971, 40436046) | not in the repository | acquisition/jobs.txt |
| PANORAMA screen calls and registry rows | jobs cancelled 2026-09-27 15:50 before call/summary | docs/grid_records/JOBS_RECORD_2026-09-27_1544.md |
| Cause of the off-by-one in CENSUS_TABLE_2026-09-25.md | the grid query behind the table is not on disk | docs/CENSUS_TABLE_2026-09-25.md |
| Patient position (supine/prone) of every acquired CT | never extracted | tools/acquisition_screen.py |
| Scan dates of the source CTs | not recorded, except Barts 2014-19 and Merlin 2012-18 in ranking.csv dedup text | acquisition/ranking.csv |
| Release label contents of PANORAMA, CURVAS, CURVAS-PDACVI, AortaSeg-60, Kidney, Barts, DEEP-PSMA, WAW-TACE and PENGWIN archives | the include patterns fetched what matched; what each zip holds besides the CT is not recorded | slurm/acquisition_submit.sh |
| The HF commit of AbdomenAtlas 3.0 Mini that was fetched | the tool reads `resolve/main` and does not log a revision | tools/acquisition_fetch.py |
| The IDC release actually served at fetch time beyond 'v24' in the census | the fetch log prints `client.get_idc_version()` but the log is on CEPH | tools/acquisition_fetch.py |
| `aa3_meta.csv` and `fdg_ct_series.json` (census inputs) and how they were made | not on local disk | tools/acquisition_census.py |
| `manifests/idc_tier2.csv` and the per-collection `idc_<coll>.csv` manifests | written by the census on the grid; not in the repository | tools/acquisition_census.py |
| Whether HOME `CTSpinoPelvic1K/data/ctpelvic1k` (36 GB) holds CTPelvic1K datasets 6-7 | contents not listed | scratchpad census/_du_data.txt |
| The download commands in `~/data/ribs/dl.sh` (RibFrac, RibSeg v2, Möller masks) | on the grid only | docs/CONTINUANCE_2026-09-19.md |
| `CORPUS.md` (ruleclass) and its per-collection call table (291 L6 / 75 T13 over 17 collections) | on CEPH only; quoted from memory | memory/ruleclass-super-detector-run.md |
| The 33-CT difference between CORPUS.md (21,655) and the tier lists (21,622) | unexplained | docs/ruleclass/PREREG_rules.md |
| Whether ENHANCE.PET 1.6k needs a Science Data Bank login, and its slice thickness | not checked | acquisition/ACQUISITION_PLAN.md section 4b |
| Whether the TotalSegmentator task-data subjects overlap TotalSegmentator v2/v3 | question for the authors, not sent | acquisition/ACQUISITION_PLAN.md section 4b |
| An id map between AbdomenAtlas 2.0 Mini and 3.0 Mini | no card, no metadata | acquisition/ranking.csv |
| Whether RSNA trauma series are inside the public AbdomenAtlas 9,262 | unpublished | acquisition/ACQUISITION_PLAN.md section 9 |
| People versus volumes in AbdomenAtlas (FLARE/KiTS repeats) and AMOS unlabelled | not established | acquisition/ACQUISITION_PLAN.md section 9 |
| Merlin size | not stated in the catalogue | acquisition/ranking.csv |
| VSDFullBody licence | the record's licence field is empty; CC BY-NC-SA per its text | acquisition/ranking.csv |
| CT Colonography remainder: 21 (computed) or about 23 people | two figures | acquisition/ranking.csv; acquisition/ACQUISITION_PLAN.md section 5 |
| Publication dates of Zenodo 4588403 (CTPelvic1K), 7049844 (CSI 2014), 18173663 (LUMOS) | not in the >= 5 GB sweep | acquisition/sweep/zenodo_ge5GB_ct.tsv |
| Whether the transitional review tree (`/rs/rs_grp_oschome/go2432/review_tree/<date>/`) was ever built | no such directory in the 2026-10-07 listing | tools/transitional_review/build_review_tree.py; listing |
| Release dates of the TCIA collections and of IDC v24 itself | only DOIs and 'v24' are recorded | acquisition/ranking.csv; acquisition/census.json |
| Which 101 of the 3,600 IDC series failed convert, and why | pooled count only | acquisition/jobs.txt |
| Whether any fetched archive was kept (the tier-1 and late commands pass no `--keep-archives`, so archives were deleted after unpack) | re-acquisition must re-download; no local archive checksum record beyond verified.jsonl on CEPH | slurm/acquisition_submit.sh; tools/acquisition_fetch.py |
| PANORAMA fetch verification (4 zips) and its convert refusals (2,024 cases of 2,238 volumes) | FETCH_STATUS.json and convert_summary.json on CEPH only | docs/ruleclass/TIERS.md; acquisition/census_addendum.json |
| Storage census of 2026-10-07 (job 40578909) | not yet available | task statement |

### Family C unknowns

Every fact this family needed and could not find on disk. "Where to look" names the file or action that would settle it.

| # | source | unknown | where to look |
|---:|---|---|---|
| 1 | all | State of every Ceph and HOME path after 2026-09-27; Greg's later work was not read by design | `/rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/{census.json,census.tsv,depth2.tsv}` (job 40578909) |
| 2 | carmlspine | Zenodo record publication date and whether the record describes any label files | the Zenodo record 22768651 |
| 3 | carmlspine | `PatientPosition` values on the frames that carry the tag (prone or supine) | `CEPH .../carmlspine/headers_dossier.json` or `SchwingNet/results/inputs/headers_dossier.json` |
| 4 | carmlspine | Living patients or cadavers; "routine intraoperative" doubted | the PRSCS-Net paper (paywalled, unread) (`docs/HANDOFF_2026-09-21_PM.md` line 451) |
| 5 | carmlspine | Whether the repaired bank's look-renders (`repair_*.png`) were ever inspected | `CEPH .../carmlspine/qc/FRAMES_CHECK.md`, `SchwingNet/results/repairs/CARMLSPINE_CHECK.md` (absent locally) |
| 6 | carmlspine | Exact arguments of `slurm/carmlspine_nifti.sh`, `carmlspine_seg.sh`, `carmlspine_seg_s1.sh` | those scripts (not read for this card) |
| 7 | carmlspine | Authors told about the residual PatientID/name in case134 | no record (`SchwingNet/results/g0_facts.md` §3) |
| 8 | carm_drr | Why `carmlspine_cbct_drr` holds 396 renders when "3 x 11 poses x 6 cards" = 198 | `tools/rare_class_carmlspine_drr.py --summary` output |
| 9 | deepfluoro_h5 | Paper DOI; Dataverse publication date of IFSXNV | the IFSXNV landing page via `tools/jhu_dataverse_info.py doi:10.7281/T1/IFSXNV` |
| 10 | deepfluoro_h5 | Which three of IFSXNV's six files were never fetched | `~/model_night/logs/jhudv_40416362.out` |
| 11 | deepfluoro_h5 | The command that unpacked the zip into `~/deepfluoro/unpacked_full` | grid shell history (not recorded in repo) |
| 12 | deepfluoro_h5 | Whether the `diffdrrdata` route (`slurm/deepfluoro_acquire.sh`) downloaded anything | `~/model_night/logs/dfacq_*.out` |
| 13 | deepfluoro_h5 / vendor | Licence: CC BY-NC 4.0 (H5 LICENSE, GitHub, Dataverse listing) against CC BY-NC-SA 4.0 (DATASHEET, vendor README) | the two LICENSE/README files on the grid |
| 14 | deepfluoro_vendor | Whether `02_fluoroscopy_rotations.tab.part` was renamed after parsing | `ls CEPH .../deepfluoro_vendor` |
| 15 | deepfluoro_vendor | Per-frame view angles of the 2,659 frames | `02_fluoroscopy_rotations.tab` |
| 16 | deepfluoro_vendor | How 2,545 cadaver files map to "1,344 image frames"; CT count 19 vs 21 series folders vs 17 sessions | `01_Readme.pdf` in the deposit |
| 17 | deepfluoro_vendor | Output location of the Cios Fusion header census | `slurm/device_census.sh` |
| 18 | deepfluoro_xvr_hf | File count and bytes on disk; whether HF subjects equal our H5 specimens | `CEPH .../polypose/env/export/xvr_data_deepfluoro.sha256`, `CEPH .../polypose/report/hf_vs_h5.json` |
| 19 | cobra2026 | Range of `ct.StudyDate` in `metadata.yaml` | `CEPH .../cobra2026/meta/*/metadata.yaml` |
| 20 | cobra2026 | Patient position on the couch | not in `metadata.yaml` (`SchwingNet/results/coverage/COVERAGE.md` §D); the dataset paper |
| 21 | cobra2026 | kV-imager model names (XVI generation, OBI version) | not stated in the paper (`docs/research_carm_datasets_verified_2026-09-22.json`) |
| 22 | cobra2026 | Current frame count of `cobra_elekta_v2` (3,384 in the audit, 3,480 in the census) | `CEPH .../realxray/cobra_elekta_v2/rewindow.json` |
| 23 | cobra2026 | Whether any Varian case has since been exported | `ls CEPH .../realxray/` for `cobra_varian` |
| 24 | geneva_hip | Yareta deposit date; the full sha256 of the archive | `CEPH .../geneva_hip_src/archive.sha256`; the Yareta record |
| 25 | ljubljana_2d3d_gs | How the zip reached the grid (no script); grid copy hash; which browser or tool fetched the local copy | grid shell history; `sha256sum CEPH .../ljubljana/2D-3D-GS.zip` |
| 26 | ljubljana_2d3d_gs | Licence as shown on the page (CC BY-NC-ND per the research record; a generic CC link per the audit verifier) | the lab page |
| 27 | spinesac | Number of devices: six by the header census, five by the research record (reused Philips template header) | `CEPH .../or_ready/spinesac/inventory.json` against burned-in overlays |
| 28 | spinesac | Outcome of the SPINEPS body-truth chain (40416582-40416584): truth, score, or the rc 4 / rc 5 stop | `CEPH .../or_ready/spinesac/truth/`, its logs |
| 29 | spinesac | Data licence (none stated) | ask the IGRS-Imaging authors |
| 30 | spinesac | Whether the person key is the phantom (UNVERIFIED) | `docs/DATA_ACCOUNTING.md` §4 |
| 31 | or_ready | Which subdirectories hold the 682 GB of models and dumps | `du` per subdirectory (census job) |
| 32 | devcorpus | Which TotalSegmentator release was rendered (v2 in the datasheet, v3 by path and identity spec) | `~/model_night/ts_clean_subjects.txt` against the v201 and v300 subject lists |

### Family D unknowns

| # | source id | fact not found | where it was looked for |
|---:|---|---|---|
| 1 | csxa_cervical_xray_atlas | download date, person, command; bytes on disk; any checksum | DATA_COMPLETENESS_AUDIT, MANIFEST, memory notes, git logs |
| 2 | csxa_cervical_xray_atlas | patient posture of the lateral films | DATASHEET, audit, refs |
| 3 | buu_lspine_3600 | date the Google Form was answered, the delivery route and archive name, bytes on disk, a copy of the EULA text | audit, memory, xrsp repo |
| 4 | buu_lspine_3600 | licence terms for derived labels | review probes, memory |
| 5 | buu_lspine_2000 | original download URL; whether the grid zip and the LOCAL zip are byte-identical (no hash recorded) | audit, xrsp repo |
| 6 | buu_lspine_400_sample | whether a copy exists on HOME; the source archive and its hash | xrsp .gitignore, audit |
| 7 | buu_lspine_drive_mirror | date `disk_cleanup.sh` actually ran (log is grid-only) | slurm/disk_cleanup.sh, audit |
| 8 | nhanes2_cdc_films | start date of the download; the text of `slurm/download_nhanes_full.sh` (grid-only); patient posture | audit, local repo |
| 9 | nhanes2_zenodo_landmarks | download date and command; why the zip ships 543 when the page says 600 | audit, refs.bib |
| 10 | vindr_spinexr | exact wget command, start date, whose PhysioNet credential | PATHOLOGY_SOURCE_SWEEP, statements.md, memory |
| 11 | vindr_spinexr | the determination is HPR 2026-330, 2026-09-29 (closed 2026-10-10); DUA terms for derived labels still open | statements.md ("PENDING G0") |
| 12 | vindr_spinexr | lesion class count (8 in MANIFEST vs 13 in the audit release row) | MANIFEST section 2.1, audit |
| 13 | aasce2019_boostnet | date and outcome of the SpineWeb request that produced the grid raw copy; reuse terms of the images in the MIT-licensed mirror | audit, thoracic_xr_fetch.py |
| 14 | aasce2019_boostnet | how many people the 217 index groups are (MANIFEST says 251) | PATIENT_IDENTITY_SPEC, MANIFEST |
| 15 | mendeley_5jdfdgp762 | the script that fetched `Dataset.zip`; relation of LOCAL `Spondylolisthesis Vertebral Landmark.zip` (43,574,184 B) to it | audit, xrsp folder |
| 17 | ieee_dataport_lateral_fullspine_236 | authors, DOI, licence text; who downloaded it, when, under which subscription; checksum | review probes, reproduce_all.sh, MANIFEST |
| 18 | spinal_ai2024 | licence of the repository; clone date; whether Git LFS was used | audit, converter docstring |
| 19 | cm_spine_drive_file | what the Drive file is | audit, MANIFEST |
| 20 | (all raw film corpora) | the text of `~/spine-detector/scripts/download_sources.py` (grid-only; the local snapshot lacks `scripts/`) | sdet: snapshot, local repos |
| 21 | spine_detector_corpus | per-version composition of `yolo_v3`, `yolo_v4z`, `yolo_v5f_*`, `yolo_v6f`, `yolo_hw` (the audit line is truncated) | audit, coverage.json |
| 22 | xrspinopelvic1k | size of `data/xrsp1k`; whether the femoral-head annotation Space produced labels; YOLO sweep results | MANIFEST, xrsp git log |
| 23 | fluorocap | the true size of `youtube/` (181.0 GB in AUDIT.json against 265 GB in MANIFEST) and of the whole tree today | audit, MANIFEST |
| 24 | fluorocap | whether the WSL copies (`FluoroCap_wsl`, `FluoroCap_lstv`) still exist; any reader verdict | audit, memory |
| 25 | fluorogen_synthetic | base-weight revisions / hashes; `synth_rare` generation date; why `allspine_v2sd_fov96_ctx` is gone | memory, film_lora_apply.sh, listing |
| 26 | fluoro_video_public_clips | the download scripts behind jobs 40477816 and 40478021; per-item licence tally; success tally of the 43 extra ids | RESUME_2026-09-22_PM, fluoro_video README |
| 27 | fluoro_cine_requests_2026_09_26, sx_stitch_request, balgrist_exvivo_request | whether any request was sent, and any reply | request docs, eml drafts |
| 28 | (derived banks) | builder of `buu_fov96_ctx`, `extra_fov96_ctx`, `nhanes_ctx`, `nhanes_split_ctx`; model trained on `allspine_v6` | MANIFEST section 3, slurm/ |
| 29 | (derived banks) | deletion records for `films_all4`, `extra3`, `extra4`, `obl_fov96_ctx`, `allspine_v2sd` | listing, disk_cleanup.sh, memory |
| 30 | (derived banks) | contents of `~/spai_verify`, `~/filmid_out`, `~/review_pack_v2`; review verdicts from `level-review` | listing, slurm/review_pack.sh |
| 31 | (all) | current byte counts of every HOME directory above (pending census job 40578909) | census:_du_home.txt (2026-09-01 only) |

### Family E unknowns

| # | what is not known | where it was looked for |
|---|---|---|
| 1 | Current size of most HOME entries created after 2026-09-01 (a 2026-09-19 `du`, ssn:docs/CONTINUANCE_2026-09-19.md L27, gives `~/spine-detector` 382G, `~/spinesurg-ct-nnunet` 363G, `~/nhanes_pseudo` 74G, `~/FluoroCap` 316G, `~/ablate` 235G, `~/implant_verse` 187G, `~/scaling` 130G, `~/.cache` 104G), including `~/model_night`, `~/data/ribs`, `~/data/spondy_landmark`, most `*_ctx` banks and most render directories | `_du_home.txt` (2026-09-01) and the manifests; census job 40578909 not yet finished |
| 2 | Current size of each Ceph entry on 2026-10-07. The latest per-folder numbers are 2026-09-25, and the volume grew from 4.5 to about 6 TB since | `CENSUS_TABLE_2026-09-25.md`; brief |
| 3 | Which `~/CTSpinoPelvic1K/data/*` folders from `_du_data.txt` still exist. A memory note says reclaim phases A and B ran on 2026-09-07 (mem:zenodo-deposit.md L30); no job log is on this laptop, so the phase-A/B folders are presumed deleted pending the census | the script, `_du_data.txt`, the audit and the memory note. Only `hf_export` (deleted) and `hf_export_v3` (deleted) are confirmed by a document |
| 5 | What `~/to_greg.zip?origin_team=T5G027G83` (304K, 2022-05-26) and `~/view?usp=sharing` (256K, 2022-01-26) are. *Rewritten 2026-10-08: the thirteen entries this row named were identified that day (section 10 note).* | the grid inspection of 2026-10-08 (scr:inspect_unknown.out) did not reach them: its leftover filter matched archive extensions, and both names end in a URL query |
| 6 | Role of `~/orient_v2`, `~/audit_out`, `~/filmid_out`, `~/spai_verify`, `~/ts_verify_out`, `~/ostk_morph_out` and `~/ostk_shards` beyond name and date | the same |
| 7 | Licence of CTSpinoPelvic1K, VerSe, CSXA, BUU-LSPINE, NHANES II films, lateral_236, Spinal-AI2024, CTSpine1K and CTPelvic1K | not in the files Family E read (other families may have it) |
| 8 | The fetch tools for VerSe (VerSeFusion download), TotalSegmentator v2/v3 (`after_dl.sh` is mentioned) and the plain-film corpora (`~/spine-detector/scripts/download_sources.py`) | these live on the grid, not in the repositories read |
| 9 | Fetch dates of CSXA, BUU-LSPINE 3600, NHANES II, VinDr, Mendeley, lateral_236, Spinal-AI2024 and CTPelvic1K | the audit and the datasheet give job ids, not dates |
| 10 | The IEEE DataPort DOI and licence of `lateral_236` | `XRAY_DATASET_USAGE.json`, `DATA_COMPLETENESS_AUDIT.md` |
| 11 | What `~/XRSpinoPelvic1K/data/dataset2024.zip` (4.7 GB) contains | "never opened" (`MANIFEST_DATA_MODELS_RESULTS.md` 7.4) |
| 12 | Why `~/CTSpinoPelvic1K/data/tcia` measured 721G against the README's 350 GB "all" estimate, and why `ctspine1k` measured 190G against the script's "~4 GB" | `_du_data.txt`, `ctsp:data/README.md`, `ctsp:slurm/download_raw.sh` |
| 13 | Whether the 38G of `~/singularity_cache` (du 2026-09-01) was rebuilt after the 2026-09-20 deletion | `mem:grid-quota-and-deleted-banks`; the listing dates it 2026-09-26 |
| 14 | What `$RS/data/external/fluoro_video` holds (videos, clips, counts, bytes) | `nnunet:tools/fluoro_video/README.md`; `FLUORO_VIDEO_SOURCES_2026-09-26.md` was not read |
| 15 | Whether `~/model_registry` and `~/mlflow` record absolute HOME paths that a move would break | `mem:model-registry` (does not say) |
| 16 | Why `$RS/archive` lists no entries, when memory says it holds finished rounds | listing; `mem:grid-ceph-volume-oschome` |
| 17 | The access tier of VinDr-SpineXR on PhysioNet | `DATA_COMPLETENESS_AUDIT.md` release row (URL only) |
| 19 | How `$RS/data/ctspine1k` was first created on 2026-09-23, one day before `other_ct_fetch.py` was committed | listing date vs. git log |
| 20 | Whether the 802 CTs in `~/data/CTSpinoPelvic1K/ct` still share inodes with another tree (their link count), and so how much space moving them frees | `ctsp:slurm/archive_build_inputs.sh` says they were hard-linked; nothing records the current link count |
