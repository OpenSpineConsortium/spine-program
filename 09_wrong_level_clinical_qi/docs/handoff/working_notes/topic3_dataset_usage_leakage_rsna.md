# Topic 3: what data SchwingNet uses, what it does not use, how leakage is checked, and the RSNA work

Written 2026-10-08 from files on this laptop only (no grid, no network). Every entry names the file it comes
from. Paths without a prefix are relative to `<spinesurg-ct-nnunet 097933a>` (private repo,
branch `L6_Class`). `mem:<name>` is a note in
`<the memory folder; copies in memory/ of this project, statuses in docs/handoff/context/INDEX.md>/`. `~` is the grid HOME
`/wsu/home/go/go24/go2432`; `$RS` is the Ceph volume `/rs/rs_grp_oschome/go2432`. A file that exists only on the grid
is marked "(grid only)". A fact no file records is written "not recorded".

Most of the documents read here were last committed 2026-09-22 to 2026-09-24 (git log); `data_platform/` was written
2026-10-08. Nothing after 2026-09-27 changed the banks or models as far as any file on this laptop shows.

---

## 0. The short answer (Greg's question: "current usage of the datasets in my SchwingNet model and what I'm not using")

1. **"The SchwingNet model" today is five pieces** (section 1): a film-trained keypoint body detector
   (`detector_v5z_final`), a real-frame vertebra/sacrum detector (`rx_lodo_carmlspine_1024`), the `allspine_v9`
   level encoder, its recurrent head, and, for the fine-tuned numbers, five C-ArmLSpine fold models re-initialised
   from v9. `docs/MODEL_REGISTRY.md` does not name it; the identification is from `SchwingNet/atlas/model.json`
   and `docs/CINE_DEMO_RECON_2026-09-26.md` §1.
2. **The level encoder is trained on three radiograph corpora and three CT collections only**: CSXA (4,963 films),
   BUU-LSPINE laterals (3,603 files, 3,600 people), the 543 annotated NHANES II films, and renders of
   CTSpinoPelvic1K, VerSe 19/20 and TotalSegmentator v2 (`slurm/allspine_v9_bank.sh`; `docs/XRAY_DATASET_USAGE.md`;
   `docs/DATA_COMPLETENESS_AUDIT.md` line 536).
3. **Not in the level bank at all**: VinDr-SpineXR (0 of 10,466), the 16,531 unannotated NHANES films, the 3,600
   BUU AP films, AASCE, Mendeley, IEEE lateral-236, Spinal-AI2024, FluoroCap, TotalSegmentator v3 renders
   (`ts_drr_v3`), RSNA 2022 cervical, RibFrac, CTSpine1K, every real C-arm frame (sections 2, 4).
4. **But the C-ArmLSpine fold models (the fine-tuned naming numbers) still train on VinDr and FluoroCap crops**:
   2,632 VinDr crops of 2,071 films and 2,100 FluoroCap crops of 950 panels per fold bank, plus both NHANES copies,
   because the v9-initialised fold models reuse the shipped fold banks built from `allspine_v7`
   (`docs/MODEL_CARD.md` §3.2; `SchwingNet/results/eval_gate/closure/cv_v9/CV_V9.md` preamble;
   `slurm/carmlspine_cv_v9init.sh` lines 11, 67). That contradicts directive D1 (FluoroCap dropped from every
   training set) and leaves VinDr outside the IRB determination (`SchwingNet/packet_src/statements.md` item 5).
5. **The detectors**: the body detector's film corpus is 12,709 films (CSXA, BUU AP + LA, the 543 NHANES), "with no
   written reason for the other 26,996" held films; it has never seen a VinDr vertebra
   (`docs/DATA_COMPLETENESS_AUDIT.md` re-count section, "Gaps the auditor missed"). The sacrum detector trains on
   real COBRA2026 Elekta (118 cases) and DeepFluoro (5 specimens) frames only (`SchwingNet/results/eval_gate/EVALUATORS.md` line 524).
6. **Real C-arm data barely used**: of COBRA2026's 692 fetched public cases only 145 Elekta cases (24 frames each)
   are in any frame bank and 0 of 225 Varian; 2,293 DeepFluoro vendor frames, the second C-ArmLSpine CBCT sweep,
   the Ljubljana frames and all SpineSAC frames train or score nothing (section 2).
7. **Leakage** is checked at three levels (section 7-13): the split (patient keys across every naming scheme), the
   bank (alias and derivation closure), and the checkpoint (an evaluation patient must be in neither train nor
   validation of the checkpoint or any ancestor). The checkpoint gate swept 563 quoted numbers: after the v9
   re-run, 380 held out, 81 seen, 1 unresolved, 101 not applicable
   (`SchwingNet/results/eval_gate/closure/chk9_cv_v9/CHK9_DIFF.md`). The full content-hash chain
   (`slurm/data_accounting.sh`) has, as far as any file shows, never been run on the real corpus.
8. **"RSNA" means three things here** (section 14-15): the RSNA 2022 cervical-spine CT archive (fetched, 203 GB,
   never unpacked, every study refused by a header census, used by nothing); the *Radiology: Artificial
   Intelligence* manuscripts (`SchwingNet/`, `paper/rsnai/`); and an older RSNA 2024 lumbar MRI download in
   `Desktop/lstv-detector`.

---

## 1. Which model is "the SchwingNet model" today

`docs/MODEL_REGISTRY.md` (last commit 2026-09-15) describes the registry and lists no SchwingNet alias. The model is
identified by `SchwingNet/atlas/model.json` (`Model.Summary`, updated 2026-09-24) and `docs/CINE_DEMO_RECON_2026-09-26.md`
§1 ("Which model is best (v9 lineage; the manuscript was re-run on it)").

| piece | file on the grid | trained on | source |
|---|---|---|---|
| body (corner) detector | `~/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` (alias `detector_v5z_final`; same file as `~/FluoroCap/detect_v5z_final_best.pt`), YOLO11m-pose, conf 0.35 | `data/yolo_v4z` (zoomed windows), fine-tuned 60 epochs from `detect_v3` (`data/yolo_v3`), COCO yolo11m-pose start | `docs/CINE_DEMO_RECON_2026-09-26.md` §1; `docs/MANIFEST_DATA_MODELS_RESULTS.md` lines 434-437; `SchwingNet/results/eval_gate/LINEAGE.md` line 42 |
| vertebra/sacrum detector | `~/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt`, YOLO11m, conf 0.74 | COBRA Elekta train+val and DeepFluoro train+val real frames; initialised from `anchor_none_v2_17-1882` (TotalSegmentator renders) from COCO yolo11m; `best.pt` selected on COBRA test + DeepFluoro test | `SchwingNet/results/eval_gate/EVALUATORS.md` lines 53, 129, 523-524 |
| level encoder | `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (sha256 prefix 188f9fcbfa3c6de1), ResNet-18, two-channel stem, 27 classes | `allspine_v9_fov96_ctx` (section 3.1); 9,592 train / 1,776 val person keys | `docs/CINE_DEMO_RECON_2026-09-26.md` §1; `LINEAGE.md` row `allspine_v9` |
| recurrent head | `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` | the same v9 bank, mixed runs of 2-9 bodies | same |
| C-ArmLSpine fold models (fine-tuned numbers) | `~/carm_cvmix{k}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt` + `~/model_night/heads_carm/head_cv{k}_v9init.pt`, k = 0-4 | the shipped fold banks `carm_cvmix{k}` (section 3.2), fine-tuned from the v9 encoder | `slurm/carmlspine_cv_v9init.sh` lines 11-23, 43-75; `CV_V9.md` |

Not part of it: the un-suffixed `ft_cv{k}_aug2.pt` fold models (initialised from `allspine_v2_r1`, whose training
bank was deleted; the gate refuses them) and `detect_v5z_epoch25`, the checkpoint shipped in `~/level_id_service`
(`docs/MANIFEST_DATA_MODELS_RESULTS.md` line 437). The device-corpus detectors `dc_A/B/P_*` appear in the
supplement's detection analysis (`SchwingNet/results/DATA_CONTRIBUTION.md`), not in the model.

Headline numbers that this stack carries: zero-shot lateral 595/617 = 96.4 % on C-ArmLSpine
(`SchwingNet/NUMBERS.md` line 419, `results/eval_gate/leaks/zeroshot_v9.json`); case-grouped five-fold 601/617 = 97.4 %,
day-grouped 568/617 = 92.1 % (`CV_V9.md` §1-2).

**Bank lineage of the level encoder** (each row: source file):

| bank | date | what changed | status | source |
|---|---|---|---|---|
| `films_all2_fov96_ctx` | 2026-09-13 | CSXA + BUU + VinDr 744 + NHANES 543; no T2-T11, T13 or L6 crops | superseded | `mem:level-model-bank-coverage`; `data_platform/DATA_MANIFEST.md` Appendix A2 |
| `allspine_fov96_ctx` | 2026-09-14 | films_drr + nhanes_drr + ctsp_drr + verse_drr + physics_drr | superseded | `slurm/allspine_bank.sh`; `DATA_MANIFEST.md` A2 |
| `allspine_v2`...`v5c` | 09-15 to 09-18 | v3/v4 added VinDr 744 and AASCE; v5 added NHANES pseudo, lat236, Mendeley | deleted 2026-09-20 (quota) | `mem:grid-quota-and-deleted-banks`; `DATA_MANIFEST.md` A3 |
| `allspine_v6`, `v7`, `v7nofluoro` | 09-17/18 | v7 = v2 + FluoroCap + VinDr pseudo (164,161 crops) | v7 is the base of the fold banks; leaked | `DATA_MANIFEST.md` A2; `slurm/overnight_v7.sh` |
| `allspine_v8` | 2026-09-22 | v2 sources minus `~/nhanes_drr`, one split over people | VerSe series keyed as subjects (5 people on both sides) | `slurm/allspine_v8_bank.sh`; `mem:identity-audit-findings` |
| `allspine_v9` | 2026-09-23 | v8 with VerSe keyed by subject (`patient_keys_v9.json`) | **current**; jobs keys 40415667, bank 40415668, train 40415669, a5 40415670 | `slurm/allspine_v9_bank.sh`; `mem:identity-audit-findings` |

---

## 2. Dataset by dataset (Greg's table)

Column key. **On disk**: count in the raw tree. **Level bank (v9)**: distinct films or renders in
`allspine_v9_fov96_ctx`, the bank of the zero-shot encoder and head. **Other banks**: the largest count in any other
crop bank on the grid (most superseded). **Detectors**: B = body detector `detector_v5z_final`; S = sacrum detector
`rx_lodo_carmlspine_1024`. **Device corpus**: `$RS/data/devcorpus` and the `dc_*` detector arms. **Fold models**:
the `carm_cvmix{k}` fold banks behind the v9init fold models (crops; films in brackets). "-" means not in it.

| dataset | on disk | level bank (v9) | other banks | detectors | device corpus | fold models | status, and why unused | sources |
|---|---|---|---|---|---|---|---|---|
| **RADIOGRAPHS** | | | | | | | | |
| CSXA cervical lateral | 4,963 PNG + 4,963 JSON | 4,963 (4,214 train / 749 val) | 4,963 | B: yes (`yolo_v3/images/*/csxa_*`) | - | 1,758 crops (1,478 films) | fully used; only `datasets.xlsx` metadata unused; one image = one person is the release's claim, untested | `XRAY_DATASET_USAGE.md`; `DATA_COMPLETENESS_AUDIT.md` lines 106, 536; `DATA_ACCOUNTING.md` §3; `MODEL_CARD.md` §3.2 |
| BUU-LSPINE lateral (3600 release) | 3,604 LA jpg (3,600 ids; 3 byte-identical "(1)" copies) | 3,603 files = 3,600 people (3,070 / 533) | 3,603 | B: yes (film corpus 12,709) | - | 635 crops (589 films) | used; "3,603" is a file count printed as a film count | `DATA_COMPLETENESS_AUDIT.md` lines 536, 839-851 |
| BUU-LSPINE AP (3600 release) | 3,600 | 0 | `buu_pair_fov48_ctx` (deleted) | B: yes (in the 12,709) | - | - | **unused, no valid written criterion**: AP csv files carry the same end-plate lines; the atlas "availability of labels" reason is false | `DATA_COMPLETENESS_AUDIT.md` lines 75, 425, 851 |
| BUU-LSPINE (2000) relabel | 4,000 jpg + csv (pixels = subset of buu_full) | 0 | - | - | - | - | second label vintage (side-bending, rotation, flexion/extension) unused; **mislabelled "AASCE test split" in `tools/xray_dataset_usage.py`** | `DATA_COMPLETENESS_AUDIT.md` lines 76, 426, 548; `DATA_MANIFEST.md` §4 #31 |
| BUU-LSPINE 400 sample | 800 images, laptop only (`CTSpinoPelvic1K-1/BUU-LSPINE_400`) | 0 | - | - | - | - | orphan download, referenced by no code | `DATA_COMPLETENESS_AUDIT.md` line 426 |
| BUU Drive mirror | gone (was 5,495, byte-identical subset) | 0 | - | - | - | - | deleted by `slurm/disk_cleanup.sh`; docs still describe it as on disk | `DATA_COMPLETENESS_AUDIT.md` re-count ("Two stale disk claims"); `DATA_MANIFEST.md` A3 |
| NHANES II annotated | 543 films (364 persons; L00452 only inside the pickle) | 543 (464 / 79 cases) | 543 | B: yes (`yolo_v2` 443/50/50) | - | `nhanes` 303 crops (236 films) **and** `nhanes_drr` 277 crops (208 films): both copies | used; the double inclusion persists in the fold banks | `DATASHEET.md` §2.6; `DATA_COMPLETENESS_AUDIT.md` lines 536, 542; `MODEL_CARD.md` §3.2 |
| NHANES II unannotated | 16,531 of 17,073 TIFF (release lists 17,075; CDC serves 2 as 0 bytes) | 0 | `nhanesps_fov96_ctx` 15,746 (pseudo; fed deleted v5) | - (never offered) | - | - | level bank: **written criterion** (raw decoder pseudo-labels cut anomalous accuracy by 20 points); detector: **no criterion**, directive D2 open | `DATA_COMPLETENESS_AUDIT.md` lines 105, 406, Repairs 2026-09-23 |
| VinDr-SpineXR | 10,466 DICOM / 5,000 studies (SHA-256 verified) | **0** | `vindrps_fov96_ctx` / `allspine_v7` 7,625 films (43,244 crops); `vindr_fov96_ctx` 744 | B: no (0 vertebrae in `yolo_v2`-`v5f`); `yolo_hw` (implant boxes) only | - | **2,632 crops (2,071 films, 1,784 studies)** | lesion boxes, not levels; v8 dropped it "for comparability" (no scientific criterion); DUA source outside IRB determination 2026-269; release test split consumed by pseudo-labelling; D3 ("use all 10,466") open | `DATASHEET.md` §2.6; `DATA_COMPLETENESS_AUDIT.md` lines 63, Repairs; `packet_src/statements.md` lines 25, 75 |
| AASCE / BoostNet | 579 jpg on HOME (481 labelled + 98 challenge test); full mirror 609 labelled on Ceph | 0 | `aasce_fov96_ctx` 457 (fed deleted v4/v5/v5c) | B: AASCE was in the 2026-09-07 detector corpus (8,069 instances); whether in `yolo_v3` not recorded | - | - | thoracic **test** set (608 films, `slurm/thoracic_xr_eval.sh`); unkeyed until the G3 split; request-form source; D6 says use | `DATA_COMPLETENESS_AUDIT.md` lines 98-99, 587-588; `mem:xray-corner-detector-status` |
| Mendeley 5jdfdgp762 | 714 jpg (698 annotated; page says 716) | 0 | `mendeley_fov96_ctx` 584 (fed deleted v5/v5c) | B: `yolo_v3/images/*/mendeley_*` | - | - | **excluded by directive**: redistribution of ~500 BUU people and 13 VinDr images; 71 non-duplicate films left out with no written reason | `DATA_COMPLETENESS_AUDIT.md` line 101; `PATIENT_IDENTITY_SPEC.md` §2-3; `mem:data-directives-2026-09-23` |
| IEEE DataPort lateral 236 | 236 | 0 | `lat236ps_fov96_ctx` 212 (fed deleted v5) | - | - | - | no release labels; pseudo-label arm refuted (19 points of anomalous accuracy) | `DATA_COMPLETENESS_AUDIT.md` line 104 |
| Spinal-AI2024 | 20,000 (usage tool counts 20,001) | 0 | `spinalai_drr` 8,358 renders in no bank | - | - | - | **written criterion**: machine-generated, 44 synthetic identities, levels assumed; D6 says use; G3 split puts all on train | `DATA_COMPLETENESS_AUDIT.md` line 100; `XRAY_DATASET_USAGE.md` |
| FluoroCap literature panels | 29,500 panels (21,603 manifest rows) | 0 | `fluorocap_fov96_ctx` 2,385 → `allspine_v7` | detect_v6f self-training (not in SchwingNet) | - | **2,100 crops (950 panels)** | **dropped by directive D1** (72.8 % zero pixel residual; no patient key); still inside the fold banks | `DATA_COMPLETENESS_AUDIT.md` lines 23, 97; `mem:fluorocap-is-reproductions-not-fluoroscopy` |
| cm_spine Drive file | empty directory | 0 | - | - | - | - | download never landed; what it is is not recorded | `DATA_COMPLETENESS_AUDIT.md` line 74 |
| TVGH-SpineXR | not acquired (403 login) | - | - | - | - | - | access never requested | `DATA_COMPLETENESS_AUDIT.md` line 102 |
| **CT COLLECTIONS AND THEIR RENDER BANKS** | | | | | | | | |
| CTSpinoPelvic1K | 802 CT (0533 rebuilt 2026-09-23) | `ctsp_drr` 801 + `physics_drr` ctsp 2,430 (798 cases) + implant variants + `physics_rare` 603 (34 cases); 0533 in no trained bank | `anchor_drr` CTSP 1,602 + implant 3,036; `anchor_drr_c2`; LSTV-flag renders 9,612 | render detector `anchor_det_v1` (not in SchwingNet) | - | `ctsp_drr` 638 crops | used; the release's `splits_5fold.json` is used by nothing; `Dataset815` built, never trained | `DATA_MANIFEST.md` sources table; `DATA_COMPLETENESS_AUDIT.md` lines 20-22, 30, 91-93; `tab_corpus.md` footnote b |
| TotalSegmentator v2.0.1 | 1,228 subjects | `physics_drr` totalseg 1,831 renders over 1,121 subjects (implant_ts feeds physics_drr per the audit) | `ts_drr` 1,170 (sweep bench, not in v9); `anchor_drr` TS 2,456 | `anchor_none_v2_*` parent of S (TS renders) | - | inside `physics_drr` 5,285 crops | used through `physics_drr`; 355 subjects never processed into `implant_ts`; 107 subjects not in physics_drr | `DATA_COMPLETENESS_AUDIT.md` lines 67, 83, 511 |
| TotalSegmentator v3.0.0 | 1,939 dirs (1,935 distinct scans) | 0 | `ts_drr_v3` 1,735 read by nothing; `anchor_drr_c2` 3,779; rare_class TS 933 | - | **142 clean whole-spine subjects (17 val)** rendered under device poses, styled per card | - | device corpus only; Table 1 wrongly says "level bank" | `DATA_COMPLETENESS_AUDIT.md` lines 66, 113, 511; `PATIENT_IDENTITY_SPEC.md` §2 devcorpus row |
| VerSe 19/20 | 374 series / 355 subjects (10 VerSe'20 series never downloaded) | `verse_drr` 387 (13 duplicates) + `physics_drr` verse 1,463 (282 series) + `physics_rare` 879 (47 series) | `verse_soft_drr` 374 (spacing defect); `verse_drr_obl/obl2`; `ctsp_drr_obl/obl2` (wrong tree) | `anchor_drr` VerSe 748 | - | `verse_drr` 940 crops | used; no VerSe accuracy is quoted | `DATA_MANIFEST.md` sources; `DATA_COMPLETENESS_AUDIT.md` lines 41-45, 69-70; `tab_corpus.md` footnote c |
| RSNA 2022 cervical CT | 2,019 train studies in a 203 GB zip (census: 2,022 study dirs) | 0 | - | - | - | - | **used by nothing**; never unpacked; header census refused all (longest 334 mm < 350 mm needed for a junction) | section 14 |
| RibFrac | 660 chest CT | 0 | - | - | - | - | transitional registry only (other_ct stream) | `SchwingNet/results/transitional_registry/other_ct/SUMMARY.md` |
| CTSpine1K | 1,005 volumes (782 are CTSpinoPelvic1K people) | 0 | - | - | - | - | transitional registry only (223 screened) | same |
| Synthetic FluoroGen `synth_rare` | 12,929 renders (T13 86, L6 1,763) | 0 | `sd_fov96_ctx` (other FluoroGen output) | - | - | - | no bank and **no written reason** | `DATA_COMPLETENESS_AUDIT.md` line 104 |
| **REAL C-ARM AND PROJECTION SETS** | | | | | | | | |
| C-ArmLSpine (Surgio-B51) | 149 cases; 299 spot frames (296 in the pre-repair bank behind every published number); 149 CBCT; 2 sweeps x 301 | 0 | `carm_fov96_ctx`, `carm_cv{k}`, `carm_drr` 240 (real frames, not renders) | S: **held out** (test 56 frames, 28 cases) | Surgio card `surgio_b51_dr`; real frames in arms where Surgio trains | `carm_AP` + `carm_LAT` crops (fold 0: 7,869 + 7,827 by MODEL_CARD, 7,891 + 7,855 by the audit) | zero-shot test (617 lateral vertebrae, 141 cases); CV naming; case134 sweep (`realxray/carmlspine_sweep`, Figure S4); case39's sweep in no root | `DATASHEET.md` §2.1; `DATA_MANIFEST.md` §4 #20, #22; `corpus_census.md` §5, §7 |
| DeepFluoro (Cios Fusion) | 6 cadaver specimens, 366 frames (H5); vendor deposit 2,659 frames + 19 CT; HF re-host | 0 | `realxray/deepfluoro` 366 | S: train+val (238 + 24 frames, 5 specimens); test specimen 18-1109 is S's selection set | Cios card (40 of 366 frames); design A renders under its poses incl. 18-1109 | - | 2,293 vendor frames unused, no criterion written; frames entered at x4 downsample, no reason written | `DATA_COMPLETENESS_AUDIT.md` lines 78-80; `DATA_CONTRIBUTION.md` §6 |
| COBRA2026 Elekta XVI | 467 public Elekta cases, all fetched (692/692 COBRA cases, 771 GB, 2026-09-23) | 0 | `realxray/cobra_elekta` 145 cases, 3,480 frames (24 per case); derived `_v2`, `_v3`, `_ap45` | S: train+val (110 + 8 cases); test 27 cases is S's selection set | Elekta card (40 frames from 3 cases) | - | 322 Elekta cases never exported (download budget, then no rebuild); 74,142 of 77,622 projections of the attempted cases unused (24 per case, no reason); LSTV screen of all 692 planning CTs (91 calls unread); D4 open | `DATA_COMPLETENESS_AUDIT.md` lines 46-48, 71; `DATA_MANIFEST.md` cobra2026 card |
| COBRA2026 Varian OBI | 225 cases fetched | 0 | none (`cobra_varian` "NOT BUILT YET") | - | `varian_halcyon` card (grid only) | - | geometry map solved 2026-09-23; no frame enters a bank until an acceptance render is looked at | `tools/realxray_banks.json`; `DATA_COMPLETENESS_AUDIT.md` Repairs 2026-09-23 Varian |
| Geneva hip (BV Pulsera) | 116 frames, one phantom | 0 | `realxray/geneva_hip` 116 | test only | card `bv_pulsera` (40 of 116); unseen-device test | - | fully used, as test | `DATA_COMPLETENESS_AUDIT.md` line 107 |
| Ljubljana 2D-3D-GS (PIXIUM 4600) | 18 frames, one cadaver L1-L5 | 0 | none | - | card `pixium_4600` (14 of 18) | - | parameters only; no truth bank built (up to 90 level boxes possible) | `DATA_COMPLETENESS_AUDIT.md` line 65; `corpus_census.md` §5 |
| SpineSAC (six C-arms, sawbones) | 5,490 of 5,492 files, 59 scenarios | 0 | none | predictions only | - | - | no bone truth (TotalSegmentator empty masks on the sawbone CTs; fallback crashed); 0 frames scored; no data licence | `DATA_COMPLETENESS_AUDIT.md` lines 29, 37, 594 |

Notes on the table.
- "Films in any bank" for Mendeley and lateral-236 read 0 in the raw-dataset table of `docs/XRAY_DATASET_USAGE.md`
  but 584 and 212 in its render-directory table of the same document. The raw table matches a substring key
  (`mendeley`, `lateral236`) against bank case ids, which are spelled `MEND_*` and `LAT236PS_*`
  (`tools/xray_dataset_usage.py` `RAW` list and the bank loop in `main()`). The render table and `DATA_MANIFEST.md` Appendix A2 are right.
- The body detector's per-version composition (`yolo_v3`, `yolo_v4z`) is "not recorded elsewhere locally"
  (`DATA_MANIFEST.md` line 17917 and unknown #21); the 12,709-film figure is the audit verifier's.

---

## 3. Bank composition in detail

### 3.1 `allspine_v9_fov96_ctx` (the level bank)

- Build: `slurm/allspine_v9_bank.sh` runs `tools/make_context_crops.py --drr ~/films_drr --drr ~/ctsp_drr --drr
  ~/verse_drr --drr ~/physics_drr --drr ~/physics_rare --mode fov --size 320 --tgt-px 96 --val-frac 0.15
  --patient-json ~/patient_keys_v9.json --group-strip-suffix --skip-clipped 1 --rungs 1`. The only change from v8 is
  the key file (VerSe by subject).
- 18,565 distinct case ids (films plus renders) (`docs/XRAY_DATASET_USAGE.md` crop-bank table).
- Films: CSXA 4,214 / 749; BUU 3,070 / 533 (3,600 people); NHANES 464 / 79 (364 people) (`~/model_night/logs/v9bank_40415668.out`
  lines 3-11 (grid only), quoted in `docs/DATA_COMPLETENESS_AUDIT.md` line 536).
- Renders: `ctsp_drr` 801, `verse_drr` 387, `physics_drr` 7,045 anns (ctsp 2,430, totalseg 1,831, verse 1,463,
  implant 1,321), `physics_rare` 1,482 anns (34 CTSP ids 603 + 47 VerSe series 879) (`data_platform/sources.json`
  `contents.items`). Per-source render counts inside the v9 bank itself are not recorded locally.
- Encoder: 9,592 train and 1,776 val person keys; no unresolved lineage (`SchwingNet/results/eval_gate/LINEAGE.md`).
- The v9 validation split is the encoder's selection split (best of 40 epochs by exact accuracy), so numbers scored
  on it are not held out (`SchwingNet/results/eval_gate/EVALUATORS.md` item 1; `EVAL_LEAKS.md` §1 item 6).

### 3.2 The C-ArmLSpine fold banks `carm_cvmix{0..4}` (fine-tuned naming)

- Built by `tools/merge_banks.py --base ~/allspine_v7_fov96_ctx/rung_1.npz --real ~/carm_cv{k}_fov96_ctx/rung_1.npz
  --per-class 600 --real-share 0.5` (`slurm/carmlspine_cv.sh` line 28; `DATA_MANIFEST.md` A2 row `carm_mix`).
- Test fold: `md5(case) % 5 == k`; the audit recorded 0 test cases in any fold's DRR, crop or mixed bank
  (`docs/MODEL_CARD.md` §3.2, from `$RS/data/or_ready/audit/AUDIT.md`, grid only).
- Crops per source (fold 0 by `MODEL_CARD.md` §3.2): buu_full 635, csxa 1,758, nhanes 303, nhanes_drr 277,
  ctsp_drr 638, verse_drr 940, physics_drr 5,285, physics_rare 1,132, FLUOROCAP 2,100, VINDRPS 2,632, carm_AP 7,869,
  carm_LAT 7,827. Distinct films: buu 589, csxa 1,478, nhanes 236, nhanes_drr 208, VinDr 2,071, FluoroCap 950 (job 40416442).
- The fold models quoted since 2026-09-24 (`v9init`) were "fine-tuned from allspine_v9 (the only change)" on these
  same banks (`slurm/carmlspine_cv_v9init.sh` line 67; `CV_V9.md`: "the same merged fold banks").
- `slurm/carmlspine_cv_v9.sh` (A12) would rebuild the base sample from `allspine_v9`; its model paths "match nothing
  on disk" in `SchwingNet/results/eval_gate/LINEAGE.md` lines 621-632. `DATA_MANIFEST.md` A2 lists one bank
  `carm_cvdaymix0_v9`. Whether any v9-base fold model was trained is not recorded.

### 3.3 The device corpus and the device-held-out detectors

- `$RS/data/devcorpus`: TotalSegmentator v3 subjects (142 clean whole spines, `~/model_night/ts_clean_subjects.txt`;
  17 validation subjects shared by all five styled corpora) ray-cast under each device's real poses and styled by
  that device's nine fitted terms (`docs/DATASHEET.md` §2.7; `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` "CLEAN").
- Styled corpora: `cios_fusion__cios_fusion`, `cios_fusion__elekta_xvi`, `cios_fusion__surgio_b51_dr`,
  `elekta_xvi__elekta_xvi`, `surgio_b51_dr__surgio_b51_dr`, each with a `__typicality` twin
  (`SchwingNet/results/rare_class/split_plan.md` "Roots keyed").
- Design A arm with Elekta held out: 5,408 synthetic + 896 real (`real_rep: 2`) training entries, 794 validation
  (`docs/MODEL_CARD.md` §3.1). Design P (pooled): 18,906 training entries (12,730 styled + 6,176 real), 1,998
  validation, 56 test specimens (`mem:pooled-vs-lodo-device-designs`).
- Real-frame banks are admitted only through `tools/realxray_banks.json` (roles device / derived / smoke; device banks
  carmlspine, cobra_elekta, deepfluoro, geneva_hip, cobra_varian placeholder).

---

## 4. What is not used, grouped by reason

| reason class (`DATA_COMPLETENESS_AUDIT.md` legend) | items |
|---|---|
| no labels in the release | VinDr levels (lesion boxes only), NHANES unannotated films, IEEE lateral-236, AASCE challenge test 98, RSNA 2022 (fracture labels and 87 segmentations, never read) |
| excluded by Greg's directive (2026-09-23, `docs/RESUME_2026-09-22_PM.md` line 2123) | FluoroCap (D1), Mendeley-716 (D6, BUU redistribution) |
| DUA / ethics | VinDr (PhysioNet DUA; outside IRB determination 2026-269, separate determination "[[PENDING G0]]") (`packet_src/statements.md` lines 25, 61, 75); AASCE (request form); RSNA 2022 (competition rules, non-commercial: `docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` line 15) |
| converted, never banked | `spinalai_drr` 8,358; `ts_drr_v3` 1,735; `synth_rare` 12,929; `films_ap_drr` 3,600; `nhanes_pseudo` (v5 only); `lateral236_pseudo` (v5 only) |
| superseded or deleted with its bank | AASCE, Mendeley, lat236, NHANES pseudo (all reached only `allspine_v4/v5/v5c`, deleted 2026-09-20); VinDr 744 route (v3/v4) |
| budget or unfinished | COBRA Elekta 322 cases not exported and 24 frames per case; COBRA Varian 225; implant_ts 355 subjects; physics_drr VerSe 92 series; physics_rare 9 series; Ljubljana truth bank; SpineSAC truth; C-ArmLSpine second sweep |
| unknown (no written reason) | BUU AP 3,600; BUU(2000) labels; DeepFluoro vendor frames 2,293; DeepFluoro x4 downsample; `synth_rare`; NHANES films for detection |

**Directives D1-D9** are all unticked in `docs/RESUME_2026-09-22_PM.md` lines 2130-2164 except D7 (`[~]`). Since
then: D3's count was established (0 VinDr in v8/v9) but VinDr was not added; D7's case134 and case39 frames were
exported; D8 (CT 0533) was repaired; no bank was rebuilt for D2, D4, D5 or D6 (`DATA_COMPLETENESS_AUDIT.md` Repairs:
"Not repaired, and why ... both are rebuilds of a bank or a training set, which G0 does not authorise"). The planned
flagship corpus that would use everything is `docs/FLAGSHIP_PLAN.md` "The corpus (G4)"; `~/corpus_final/` and
`SchwingNet/results/final/` do not appear in any file on this laptop.

---

## 5. Documents that disagree, and which to trust

| claim A | claim B | trusted | why |
|---|---|---|---|
| Table 1: TotalSegmentator v2 and v3 contribute to the "level bank" with 1,170 and 1,735 renders (`SchwingNet/tables/tab_corpus.md`) | v9 bank roots exclude `ts_drr` and `ts_drr_v3`; TS reaches the bank only as 1,831 `physics_drr` renders over 1,121 subjects; `ts_drr_v3` read by nothing (`slurm/allspine_v9_bank.sh`; `DATA_COMPLETENESS_AUDIT.md` lines 66, 511) | B | the build script is what ran |
| Device corpus from "TotalSegmentator v2" (`MODEL_CARD.md` §3.1; `DATASHEET.md` §2.7) | from v3: manifest root `ts_subjects` path is `TotalSegmentator_v3/...v300` (`docs/RSNAI_DATA_MANIFEST.json`); `PATIENT_IDENTITY_SPEC.md` §2 devcorpus row; audit line 113 | B | path and two independent documents; `DATA_MANIFEST.md` §4 #12 |
| "The clean rebuild has not landed" (`MODEL_CARD.md` §3.3; `DATASHEET.md` §4) | v8 and v9 exist and are trained (`XRAY_DATASET_USAGE.md`; `LINEAGE.md`) | B | A was written 2026-09-22, before the rebuild |
| C-ArmLSpine encoder "initialised from the v7 bank" (`mem:no-unexplained-subsets-fix-not-disclose`) | initialised from `allspine_v2_r1` (`MODEL_CARD.md` §1.2; `slurm/carmlspine_cv.sh` line 21) | both, read correctly | init = `allspine_v2_r1`; the base crops of the fold bank come from `allspine_v7` (line 28) |
| Fold-bank crops "sum to the bank's 31,446" with carm_AP 7,869, carm_LAT 7,827 (`MODEL_CARD.md` §3.2) | carm_AP 7,891, carm_LAT 7,855 for `carm_mix_fov96_ctx` (`DATA_COMPLETENESS_AUDIT.md` line 538) | unresolved | MODEL_CARD's twelve numbers sum to 31,396; the audit's sum to 31,446. Whether MODEL_CARD's carm counts are fold 0 and the audit's are `carm_mix` is not recorded |
| `XRAY_DATASET_USAGE.md` raw rows: Mendeley and lateral-236 "films in any bank 0" | same document, render rows: 584 and 212 | render rows | substring-key artefact (section 2 notes) |
| "AASCE test split, 4,000, report spreadsheet only" (`XRAY_DATASET_USAGE.md`) | it is the BUU-LSPINE(2000) release (`DATA_COMPLETENESS_AUDIT.md` lines 76, 548) | B | pixel identity with buu_full |
| Spinal-AI2024 on disk 20,001 (`XRAY_DATASET_USAGE.md`) | 20,000 (5 x 4,000) (`DATA_COMPLETENESS_AUDIT.md` lines 561, 573) | B for the release | the extra file is not identified |
| `CT_INVENTORY.md`: `physics_drr` = CTSpinoPelvic1K, 3,029 subjects; `physics_rare` = CTSP, 81; `carm_drr` = CBCT renders; `verse_drr` 387 | `physics_drr` mixes ctsp/totalseg/verse/implant; `physics_rare` = 34 CTSP + 47 VerSe; `carm_drr` holds real frames; `verse_drr` has 13 duplicates (`sources.json`; audit lines 42, 92; `DATA_MANIFEST.md` §4 #22) | B | the inventory labels banks by name, not by contents |
| `tools/realxray_banks.json`: Varian "geometry not solved" | map solved 2026-09-23, acceptance render pending (`DATA_COMPLETENESS_AUDIT.md` Repairs) | B; no bank either way | the JSON note predates the repair |
| `DATA_MANIFEST.md` line 14766: `cobra_elekta_v3` and `cobra_elekta_g3test` are in `tools/realxray_banks.json` | the local `tools/realxray_banks.json` (commit 180fb0f, 2026-09-23) has neither | unresolved | the grid copy may be newer; not recorded |
| `a5.json` v2_statement: v8 is "the bank the manuscript must quote" | v9 is the current encoder; film counts differ slightly (csxa val 749 vs 727) (`DATA_COMPLETENESS_AUDIT.md` line 554) | B for the model; A for the plain-film numbers, which are selection-split numbers anyway | `EVALUATORS.md` item 1 |
| Body detector in use: `detector_v5z_final` (atlas, manuscript) | `detect_v5z_epoch25` shipped in `~/level_id_service` (`MANIFEST_DATA_MODELS_RESULTS.md` line 437) | both true; different products | the manuscript and the service carry different checkpoints |

---

## 6. Recipes: regenerating the usage numbers

| what | command | output | source |
|---|---|---|---|
| X-ray usage table | `python tools/xray_dataset_usage.py --out ~/model_night/XRAY_DATASET_USAGE.md` (in a job; reads every `~/*/rung_1.npz`) | `.md` + `.json` twins, copied to `docs/` | tool docstring |
| NHANES and VinDr per-image manifests | `slurm/film_corpus_inventory.sh` (job 40416535) → `tools/film_corpus_inventory.py` | `$RS/data/inventory/films/` incl. `nhanes_film_manifest.csv`, `FILM_CORPUS_INVENTORY.md` | `DATA_COMPLETENESS_AUDIT.md` Repairs |
| per-bank film counts from case arrays | `tools/audit_film_corpora.py` (job 40416442) | `$RS/tmp/film_corpora_audit.json` (grid only) | same |
| CT render subjects | `python tools/ct_inventory.py` | `docs/CT_INVENTORY.md` | file header |
| persons and images per source on the G3 split | `python SchwingNet/tools/corpus_census.py` | `SchwingNet/results/corpus_census.md` | file header |
| real-frame training lists, derived-bank duplicates | `python tools/audit_realxray_lists.py` | `SchwingNet/results/realxray_lists_audit.json` | tool docstring |
| data side as a whole | `data_platform/` (start with `DATA_MANIFEST.md` §1 and `MIGRATION_PLAN.md` §0) | `sources.json`, `db/` index | `data_platform/README.md` |

Fix before the next run: rename `buu_2000` in `tools/xray_dataset_usage.py` `RAW`; key raw datasets by
`tools/patient_keys.py` rather than substrings; update the HOME paths after the Ceph migration
(`DATA_MANIFEST.md` Appendix B item 3).

---

## 7. Leakage: what "held out" means in this project

From `docs/DATA_ACCOUNTING.md` §1 and §5 (last commit 2026-09-24):

- **An item is one acquisition** (one exposure or one CT series), not a file. Three keys: `store_key` (`sha256` of
  the bytes), `pixel_key` (`pix_sha256` of a 0.5-99.5 percentile 8-bit reduction; `vol_sha256` of a 64^3 resample),
  and `item_key` (`canonical_id`, assigned by `tools/data_alias.py canon` after alias resolution). Compare rows only
  after reading `content_key_kind`.
- **A derived image is a new item with an inherited patient**: a DRR, a styled frame and a crop of one CT share one
  `patient_key`. Splits are enforced on the patient key, duplicates on the item key.
- **Validation is seen.** A split that chose a checkpoint shaped it, so `tools/holdout.py`, the gate and every
  check count train AND val as seen; `holdout.trained_on(..., train_only_because="<why>")` is the only exception.
- **Lineage is followed.** A checkpoint has seen everything its ancestors saw; public ImageNet/COCO weights are the
  only exempt ancestor, and only when declared (`PUBLIC_ROOT_RX`, `PUBLIC_TORCHVISION` in `tools/checkpoint_lineage.py`).
- **Unknown is not clean.** An unkeyed item, an unresolved lineage link or a check that did not run fails.

## 8. The checks

### 8.1 CHK-1 to CHK-9 (`docs/DATA_ACCOUNTING.md` §5 and §5.1)

| id | tests | implemented by |
|---|---|---|
| CHK-1 | item disjointness | `leak_check.py` row `2_within_collection_merged_key` (in part); `make_split.py` CHK-1, CHK-1b |
| CHK-2 | alias closure (the NHANES failure) | row `2_...` plus `alias_gaps`; `make_split.py` CHK-2 (62 alias edges) |
| CHK-3 | patient closure, incl. derived items | rows `1_within_collection_builder_key` and `2_...`; `make_split.py` CHK-3, CHK-3b |
| CHK-4 | derivation closure (parent and child on one side) | row `5_render_pose_duplicates`; `lineage.json` `leakage[]`; `make_split.py` CHK-4, CHK-4b (pose donors, WARN only) |
| CHK-5 | held out whole (device or corpus) | rows `4_eval_vs_training`, `6_styled_vs_real_device`; `make_split.py` CHK-5 |
| CHK-6 | near-duplicates across splits (pHash then NCC64 >= 0.97) | not a row; `data_alias.py canon --pixels`; `or_audit_dupes.py`; NOT RUN in the G3 split |
| CHK-7 | undeclared alias by store or pixel key | `alias_groups.json` groups spanning undeclared roots; NOT RUN in the G3 split |
| CHK-8 | orphans and coverage | `leak_report.json` `census` and `verdict`; `make_split.py` CHK-8 (WARN: 17 unkeyed AASCE `coronal` films), CHK-8b |
| CHK-9 | evaluation vs selection and lineage, for every quoted number | `leak_check.py chk9` over `SchwingNet/results/eval_gate/quoted_results.json`, `touched.json`, `eval_sets.json` |

### 8.2 The tools, by layer

| layer | tool | what it does | source |
|---|---|---|---|
| person keys | `tools/patient_keys.py` (`key_for`, `key_any`, `canon_key`, `resolve_key`) | one key per person across naming schemes (Dataset813 crosswalk, NHANES pairs, VerSe series→subject via `--verse-manifest`, implant→source CT, scoped Bournemouth and C-ArmLSpine sweep schemes); refuses names it cannot key | file docstring; `PATIENT_IDENTITY_SPEC.md` |
| person keys, spec | `docs/PATIENT_IDENTITY_SPEC.md` | resolution order L0 corpus, L1 DICOM tag, L2 release table, L3 release manifest, L4 crosswalk, L5 ann `scheme`+`source_case`, L6 `patient_id` (demoted), L7 directory, L8 file name, L9 content hash as a merge pass; 19 aliases; failure behaviour | spec §1-5 |
| tests | `tools/test_patient_keys.py`, `tools/test_leak_check.py`, `tests/test_eval_gate.py` | the two cross-naming defects collapse; leak_check fixtures; the arc leak, the two spellings, declarations, `holdout.py`, CHK-9 | `DATA_ACCOUNTING.md` §5.3; `SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` |
| bank builder | `tools/make_context_crops.py --patient-json` | one split over people across all `--drr` roots; refuses unkeyed cases (`--allow-unkeyed` overrides); fails if anyone is on both sides; records the key file in `meta.json` | `SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` "The fix" |
| bank and split audit | `tools/leak_check.py check` | checks (1) builder-key disjointness, (2) cross-source merged-key disjointness, (3) one source twice under two names (structural), (4) eval vs training, (5) render pose duplicates, (6) styled corpora vs real device and pose donor; discovers collections; hash evidence corroborates, never merges two keys | file docstring |
| content chain | `slurm/data_accounting.sh` → `data_ledger.py build/summary` → `data_alias.py canon` → `data_lineage.py build` → `leak_check.py check` → `fig_data_flow.py` | item ledger, alias classes, lineage graph, leak report, three-panel figure; exits non-zero on FAIL or on a stage that produced nothing | `DATA_ACCOUNTING.md` §2, §6 |
| person split (G3) | `tools/make_split.py plan/apply` (`SchwingNet/slurm/g3_split.sh`) | person hash `sha256('g3|<seed>|<key>')`, 80/10/10; transitional 50/10/40 per subtype; real transitional subjects to test; COBRA hold rule; union-find alias folds; writes `~/split_final.json` and `split_leak_report.json` | docstring; `SchwingNet/results/rare_class/split_plan.md` |
| independent split check | `tools/g3_leak_intersect.py`, `tools/g3_split_verify.py` | second, code-independent intersection of detector lists with the split's test, hold and excluded persons and Figure 6 sets | docstrings |
| checkpoint lineage | `tools/checkpoint_lineage.py` | `touched.json`: train, val and touched keys per checkpoint and ancestor; closes reading gaps from recorded evidence only; unresolved links carried to descendants | `DATA_ACCOUNTING.md` §5.2; `LINEAGE.md` |
| evaluation gate | `tools/eval_gate.py` (`assert_unseen`, `carry`, `stamp`, `gate_evaluation`) | every evaluator keys its items, walks the chain, refuses a seen or unresolved pair before scoring, writes the verdict into the result; `--not-held-out "<reason>"` is the only way past, and it is printed | `DATA_ACCOUNTING.md` §5.3 |
| unseen lists | `tools/unseen_cases.py` | lists what a checkpoint's chain never saw (v9: 70 TS + 1 CTSP + 0 VerSe renders) | `mem:ts-bench-inside-v9-bank` |
| real-frame admission | `tools/realxray_banks.json` + `tools/realxray_train.py check` | fail-closed admission list; device banks must not share a case id (checked on disk); derived banks never enter pooled or LODO arms | JSON `_README` |
| real-frame split audit | `tools/or_audit_splits.py`, `tools/or_audit_dupes.py` | split disjointness by case on the four real-frame sets, fold banks; NCC near-duplicates vs films and FluoroCap | `DATA_CONTRIBUTION.md` §6 (AUDIT.md, grid only) |
| pooled list builder | `tools/devcorpus_build.py lists --design P` | refuses if a CT subject or real specimen is on two sides; designs A and B do not run this refusal | `DATA_CONTRIBUTION.md` §6 finding 2 |
| leak size | `tools/leak_effect.py` | same-run comparison of in-train vs held-out spines on a sweep, cluster bootstrap | docstring |

### 8.3 The device designs (LODO and pooled)

- **LODO** (leave one device out): the held-out device is absent from training frames, from training renders' poses
  and from the calibration terms of the initialisation (`docs/RSNAI_PLAN.md` rules; `MODEL_CARD.md` §3.1). Real
  frames split by specimen or case; renders follow their CT subject (`mem:k-devices-one-network`).
- **Design P** (pooled, Greg 2026-09-22): every device's training frames in one detector, scored on every device's
  test split; report it only beside the LODO number (`mem:pooled-vs-lodo-device-designs`).
- **Known exposure of design A**: it renders every card under the Cios Fusion pose pool, which includes DeepFluoro
  test specimen 18-1109, so arms that "hold DeepFluoro out" trained on renders under that specimen's poses; design B
  does not and reads higher (`DATA_CONTRIBUTION.md` §6 finding 1). The G3 split reports 8,082 such pose-donor renders
  as CHK-4b WARN (`split_plan.md`).
- C-ArmLSpine case is an acquisition, not a proven person (149 cases on five dates); the CV is reported both
  case-grouped and acquisition-day-grouped (`PATIENT_IDENTITY_SPEC.md` §4; `mem:identity-audit-findings`).

## 9. How to run the checks

```bash
# the content chain on the grid (two submissions; the second refuses a partial ledger)
cd $HOME/spinesurg-ct-nnunet
A=$(sbatch --parsable -D $HOME/spinesurg-ct-nnunet --array=0-15 --export=ALL,STAGE=ledger slurm/data_accounting.sh)
sbatch -D $HOME/spinesurg-ct-nnunet --dependency=afterany:$A --export=ALL,STAGE=rest --cpus-per-task=8 --mem=64G \
  --time=04:00:00 --output=/wsu/home/go/go24/go2432/model_night/logs/data_accounting_rest_%j.out slurm/data_accounting.sh
# outcome: grep DATA_ACCOUNTING_LEAK_CHECK in the stage-2 log; outputs under $RS/data/or_ready/data_accounting
# self-test of the runner, planted leak and clean tree (each prints the ALLOW_LOCAL=1 STAGE=all line to run)
python tools/diagnostics/make_fake_corpus.py --out <scratch>/fake_leak
python tools/diagnostics/make_fake_corpus.py --out <scratch>/fake_clean --clean
# the bank and split audit alone (in a job)
python tools/leak_check.py check --out /rs/rs_grp_oschome/go2432/data/or_ready/leak
# CHK-9 over every quoted number
python tools/leak_check.py chk9   # writes chk9_report.json and CHK9_REPORT.md
# the G3 person split with its checks
sbatch -D $HOME/spinesurg-ct-nnunet --export=ALL,STAGE=all SchwingNet/slurm/g3_split.sh
# the gate, without the grid
python -m pytest tests/test_eval_gate.py -v
# real-frame banks
python tools/realxray_train.py check --root /rs/rs_grp_oschome/go2432/data/realxray
```
Sources: `docs/DATA_ACCOUNTING.md` §5.3, §6, §6.1; `slurm/data_accounting.sh` header; `tools/leak_check.py`
docstring; `split_plan.md` header; `tools/realxray_banks.json` `_README`. The doc's own `/tmp/...` paths for the
fake corpus should be a scratch directory on this laptop.

## 10. What the checks found (in order found)

| date | finding | size | affected | fix | status | source |
|---|---|---|---|---|---|---|
| 2026-09-14 | deployed level bank `films_all2` had no T2-T11, T13 or L6 crops | 0 crops for 11+ classes | the level model of that week | all-spine banks | closed | `mem:level-model-bank-coverage` |
| 2026-09-15 | evaluations scored renders whose CT was in the bank's training split | v1 "92.7 %" was on training cases | transitional evals | `--include-train` default off | closed | same |
| 2026-09-20 | deleted banks left `--holdout-bank` empty, so evaluations ran on fitted cases | ~90 scripts | any holdout run after the deletion | `tools/holdout.py` raises; 57 refs repointed to v7 | closed | `mem:grid-quota-and-deleted-banks` |
| 2026-09-22 | NHANES II twice (`films_drr` + `nhanes_drr`), split per source | 48 of 54 val patients | v2, v6, v7; every pooled real-film number | v8 drops `nhanes_drr`; cross-source key | closed in v8/v9; **still in the fold banks** | `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`; `MODEL_CARD.md` §3.2 |
| 2026-09-22 | CTSpinoPelvic1K under two names (`CTSP_COLONOG_<token>` vs `ctsp_<release id>`) | 371 people on both sides, 357 from naming alone | v6, v7 (v2 same rule) | `patient_keys.py` crosswalk | closed in v8/v9 | `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` |
| 2026-09-22 | VerSe series keyed as subjects | 5 people, 10.5 % of VerSe val | the "clean" v8 bank | `--verse-manifest`, v9 | closed in v9 | `mem:identity-audit-findings`; `PATIENT_IDENTITY_SPEC.md` §3 #7 |
| 2026-09-22 | `anchor_drr` split seeded on the implant-variant stem | 301 of 801 CTSP people | `anchor_det_v1` own-domain 93.48 % | not quoted | open (bank not rebuilt) | `PATIENT_IDENTITY_SPEC.md` §3 #4 |
| 2026-09-22 | VinDr keyed per image, not study | 77.8 % of `vindrps` val | `vindrps`, v7 | `export_vindr_identity.py`; study key in G3 | open for the old banks | `PATIENT_IDENTITY_SPEC.md` §3 #2 |
| 2026-09-22 | TotalSegmentator v201 s1406-s1429 renumbered in v300 | 24 split + 15 merged | any `ts:s####` key | G3 split folds TS by md5 and shape+affine; `tools/identity/ts_alias.json` not built | partly | `PATIENT_IDENTITY_SPEC.md` §3 #6; `split_plan.md` CHK-2 |
| 2026-09-22 | C-ArmLSpine case is not a person | 149 cases, 5 dates | the 98.22 % CV | day-grouped folds reported beside case-grouped | closed by reporting both | `mem:identity-audit-findings` |
| 2026-09-23 | COBRA derived banks globbed into one detector arm | 5,013 duplicate frames (one patient up to 4 times) | `rx_pooled_1024_init18` (quoted nowhere) | fail-closed `realxray_banks.json` + on-disk disjointness | closed | `DATA_COMPLETENESS_AUDIT.md` line 18; `results/repairs/cobra-dup-leak_CHECK.md` |
| 2026-09-23 | recall-vs-angle curve scored on the detectors' own selection subjects | 17 TS subjects | old Figure 4d | re-scored on 40 unseen subjects (job 40428072); not inflated | closed (curve retired) | `EVAL_LEAKS.md` §1 item 1 |
| 2026-09-23 | plain-film naming numbers are on the encoder's selection split | CSXA 99.8, BUU 97.3, NHANES 99.1 % | Table 3 film rows | relabelled "selection split" | labelled | `EVALUATORS.md` item 1; `packet_src/statements.md` item 6 |
| 2026-09-23 | `rx_lodo_*` `best.pt` selected on the other devices' test splits | COBRA test 27/27 patients | lcurve rows only | only own held-out device quoted | labelled | `EVALUATORS.md` item 2 |
| 2026-09-23 | first CHK-9 | 380 rows: 31 SEEN, 40 UNRESOLVED | quoted numbers | gate wired into ~40 evaluators | superseded | `DATA_ACCOUNTING.md` §5.3 |
| 2026-09-23 | G3 split: v8/v9 trained on most transitional val+test persons | 49/54 L6, 4/4 T13, 14/14 sacralised | any v8/v9 descendant on the G3 test | paper 1 scores no G3 test person; Figure 6 / paper 2 trains from ImageNet | rule in place | `split_plan.md`; `mem:spineps-ids-can-be-scrambled` |
| 2026-09-24 | EVAL_LEAKS sweep | 563 rows: 81 SEEN, 58 UNRESOLVED (57 trace to deleted `allspine_v2_r1`) | quoted numbers | v9 re-run of the CV (cv_v9 closure) | 81 SEEN remain (labelled), 1 UNRESOLVED | `EVAL_LEAKS.md`; `closure/chk9_cv_v9/CHK9_DIFF.md` |
| 2026-09-25 | the TotalSegmentator render bench sits inside the v9 bank | 483 of 523 sacrum-bearing spines in v9 train/val | any v9 number on `ts_drr` | `--holdout-bank` matched stems, not keys; use `unseen_cases.py` (71 cases) | rule in place | `mem:ts-bench-inside-v9-bank` |

Verdict by family after the sweep (`EVAL_LEAKS.md` §6): LEAKED families are `embedding_v9` (Figure 2, v9 validation
split), `device_cards` (15), `fig4a_pairs` (13), `film_naming_v8` (9), `render_vs_film` (7), `count_only` (2),
`lcurve` (2), `arc` (1). CLEAN families include `lodo_detector_on_carm` (21), `fig3_scored` (58), `contribution`
(99), `counting` (11), `pooled_vs_lodo_carm` (4), `case134`.

## 11. What remains open (leakage)

1. **The content chain has not been run on the real corpus.** `DATA_CONTRIBUTION.md` §6 (2026-09-22) says
   `$RS/data/or_ready/data_accounting/` does not exist; no later file records a run; the G3 split marks CHK-6 and
   CHK-7 NOT RUN (`split_plan.md`). The repo copy of `DATA_ACCOUNTING.md` §7 is empty by design.
2. **E3 never ran**: the leakage audit over every device-corpus training list (`RSNAI_PLAN.md` box E3), and designs
   A and B lack the design-P refusal (`DATA_CONTRIBUTION.md` §6).
3. **The fold banks still hold both NHANES copies, FluoroCap and VinDr** (section 3.2). No quoted number scores
   NHANES with them, but the composition violates D1 and the ethics scope.
4. **The metadata-first keyer of `PATIENT_IDENTITY_SPEC.md` is only partly built.** `tools/identity/` is empty in
   this checkout; the frozen tables (`ctsp_token_map.json`, `ts_alias.json`, `verse_series_to_patient.json`,
   `vindr_image_to_study.json`, `fluorocap_doc_keys.json`, `deepfluoro_h5_alias.json`) and the bank registry
   `tools/identity/banks.json` are not in the repo; the VinDr map was exported on the grid (job 40416449,
   `corpus_census.md` §5). `patient_keys.py` still reads `patient_id` first for `films_drr` (spec §5).
5. **Assumed identities**: CSXA one image = one person (untested); AASCE index = person (unknown); Mendeley
   `Screenshot-*` films (unknown); TotalSegmentator scans folded by content, persons unknown; COBRA centres D/F/G
   stripped (`PATIENT_IDENTITY_SPEC.md` §4).
6. **81 SEEN quoted rows** must stay labelled as not held out or be removed; the manuscript workflow owns that
   (`EVAL_LEAKS.md` preamble).
7. **No weight file of the k-devices half has a SHA-256 in the registry** (`MODEL_CARD.md` §1.3); the gate binds
   verdicts to sha256 only for dumps written after 2026-09-24 (`DATA_ACCOUNTING.md` §5.3).
8. **`splits_5fold.json` at the repo root is an empty file** (0 bytes, 2026-09-12); the CTSpinoPelvic1K release's own
   patient-grouped split is used by nothing and is keyed by TCIA token, not release id (`DATA_COMPLETENESS_AUDIT.md`
   line 21; `DATA_MANIFEST.md` §4 #4).

---

## 12. Patient keys per corpus (summary of `PATIENT_IDENTITY_SPEC.md` §2 and `DATA_ACCOUNTING.md` §4)

| corpus | key | trap |
|---|---|---|
| CTSpinoPelvic1K | `ctsp:<TCIA token>` via `manifest.json` (token is not release id; 0145 = token 100) | four name shapes; implant variants |
| TotalSegmentator | `ts:<sid>` after release fold (L9 content override) | v201/v300 renumber; no patient id exists |
| VerSe | `verse:<subject>` (374 series → 355 subjects) | `CTSP_VERSE_` prefix; `glgl` doubles |
| NHANES II | `nhanes:<5-digit sample person>` from `NHANES_nhanes_*`, `NH_*`, `NHANESPS_*` | three schemes |
| BUU-LSPINE | `buu:<NNNN>`, AP and LA together | "(1)" copies; two byte-identical case pairs |
| CSXA | `csxa:<SSSS>` | one image = one person assumed |
| VinDr | `vindr:<study_id>` | image-level keys leaked 77.8 % |
| Mendeley | folds to `buu:` (500) or `vindr:` (13); 71 refused | redistribution |
| AASCE | `aasce:<index>`; `coronal` names refused | index may not be a person |
| Spinal-AI | `spinalai:<similarity group>`, `person_key=false`, whole corpus train | no person exists |
| FluoroCap | source document or video; never a patient count | over-merges by design |
| C-ArmLSpine | `carmlspine:case<N>`; never `PatientID` | case = acquisition; case134/ori carries a real name (never print) |
| DeepFluoro | `deepfluoro:<accession>` | fluoro `PatientID` is wrong |
| COBRA2026 | `cobra:<case>` on the paper's authority | D/F/G stripped |
| Geneva, Ljubljana | one object each, test only | Geneva keyed per view until 2026-09-24 |
| devcorpus | `ts:<subject>` | 17 held subjects appear in five other banks |

---

## 13. Memory notes that bear on this topic

`mem:split-leak-cross-naming`, `mem:nhanes-double-inclusion`, `mem:identity-audit-findings`,
`mem:ts-bench-inside-v9-bank`, `mem:level-model-bank-coverage`, `mem:pooled-vs-lodo-device-designs`,
`mem:k-devices-one-network`, `mem:data-directives-2026-09-23` (D1-D9), `mem:no-unexplained-subsets-fix-not-disclose`
(use all of a release; repair a leaked initialisation, do not disclose it), `mem:data-audit-99-gaps`,
`mem:grid-quota-and-deleted-banks`, `mem:fluorocap-is-reproductions-not-fluoroscopy`,
`mem:ct-benchmark-covers-all-collections`, `mem:carmlspine-level-experiment`, `mem:spineps-ids-can-be-scrambled`,
`mem:xray-corner-detector-status`, `mem:rsnai-paper-endpoint`, `mem:schwingnet-manuscript`, `mem:hf-mirror-is-v10`.
The U251 notes (RNA-seq) are another project and are not summarised here.

---

## 14. RSNA 2022 Cervical Spine Fracture Detection (the dataset)

| item | fact | source |
|---|---|---|
| what | Kaggle competition `rsna-2022-cervical-spine-fracture-detection`; dataset paper doi 10.1148/ryai.230034 (*Radiology: AI*); 3,112 CT scans collected, 2,019 in the Kaggle train split; 961 studies with a fracture, 1,444 fractures; per-level labels C1-C7 in `train.csv`; 87 segmentations | `DATA_COMPLETENESS_AUDIT.md` line 568; `docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` line 15; `slurm/rsna_cspine_fetch.sh` header |
| terms | login and acceptance of competition rules; "non-commercial research and education only" | `PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` line 15 |
| why fetched | planned: unzip, DICOM→NIfTI, SPINEPS, render for C2 sweeps; also "the only large source where a C1 vs C2 vs C7 label is voxel-anchored" | `docs/CONTINUANCE_2026-09-19.md` running-jobs table; `PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` line 397 |
| how fetched | `MODE=download nohup bash slurm/rsna_cspine_fetch.sh > ~/data/rsna_cspine/fetch.log` (Kaggle CLI, token from `~/.fluorocap/credentials.env`, not read here), **on the login node**, which current grid rules forbid; 2026-09-19, `fetch.log` rc=0 | `slurm/rsna_cspine_fetch.sh`; `DATA_MANIFEST.md` `rsna_2022_cspine` card |
| on disk | `~/data/rsna_cspine/`: zip 203,318,086,447 B (= 189 GiB, matches Kaggle's "189G/189G"), one `.nii.zip`, `sample_submission.csv`, `fetch.log`; never unpacked; 236.8 GB of the HOME quota | `DATA_COMPLETENESS_AUDIT.md` lines 62, 584; `mem:grid-quota-and-deleted-banks` |
| verification | zip central directory read (job 40416361); `slurm/audit_unused_data.sh` counts members and train/test studies; no checksum beyond the listing | `slurm/audit_unused_data.sh` lines 32-46; `DATA_MANIFEST.md` card |
| header census | `tools/other_ct_fetch.py rsna --zip ... --out $RS/data/anomaly_harvest/other_ct/rsna` (via `sbatch ... slurm/other_ct_fetch.sh rsna`): per study, slice count and the image position of the first, middle and last slice read straight from the zip; writes `rsna_headers.jsonl` (grid only), resumable; prints `RSNA_CENSUS_DONE` | `tools/other_ct_fetch.py` lines 13-21, 200-241; `slurm/other_ct_fetch.sh` lines 15, 28-29 |
| census result | 2,022 study directories; longest craniocaudal extent 334 mm, below the 350 mm a scan from the skull base needs to reach the thoracolumbar junction (cervical ~120 + thoracic ~280 mm); **all 2,022 refused**, none segmented, `no_count` in the transitional registry | `SchwingNet/results/transitional_registry/other_ct/SUMMARY.md` lines 30, 36, 112; `REGISTRY.md` lines 119, 329, 446; `docs/ruleclass/CLASSIFIERS.md` line 66 |
| code vs docstring | the docstring says a long-enough study "is extracted and converted for the full screen"; `cmd_rsna` only writes headers. No study qualified, so nothing was lost, but the extraction path does not exist | `tools/other_ct_fetch.py` lines 13-16 vs 200-241 |
| identity | a study is treated as a person (no patient field shipped) | `other_ct/SUMMARY.md` lines 5, 233 |
| used by | nothing: no render, no bank, no model, no inventory beyond "0 nii" | `DATA_COMPLETENESS_AUDIT.md` lines 62, 597; `CT_INVENTORY.md` |
| open decision | whether it serves the cervical/C2-anchor work: if yes, unpack to `$RS/data` and add a `ct_inventory.py` root; if no, delete to free ~237 GB. Re-acquire to Ceph via sbatch, not the login node. Rotate the Kaggle token (it appeared in a chat transcript) | `DATA_COMPLETENESS_AUDIT.md` line 62; `DATA_MANIFEST.md` card; `CONTINUANCE_2026-09-19.md` |

The 350 mm rule refuses the archive for the *transitional* (junction-counting) registry only. It says nothing about
a cervical use (C1-C7 level renders, a C2 anchor); that use was never tried.

## 15. "RSNA" as the journal, and a third RSNA dataset

- **The *Radiology: Artificial Intelligence* manuscripts.** `paper/rsnai/main_v2.tex` (the k-devices paper,
  endpoint set 2026-09-22; checklist `docs/RSNAI_PLAN.md`; ledger `docs/RSNAI_CLAIMS.json`, 54 claims, none a
  data-audit claim; `docs/RSNAI_DATA_MANIFEST.json`, 12 roots, no film corpus; Table 1 from `tools/rsnai_table1.py`
  → `docs/RSNAI_TABLE1_DATASETS.md`) was superseded by `SchwingNet/main.tex` (paper 1, five figures, three tables;
  the LevelCheck comparison moved to `SchwingNet/paper2_levelcheck/`) (`mem:rsnai-paper-endpoint`;
  `SchwingNet/README.md`; `DATA_CONTRIBUTION.md` §6). The RSNA ATLAS cards are `SchwingNet/atlas/{model,dataset}.json`.
  Other topic notes cover the manuscripts; this note covers only their data.
- **RSNA 2024 Lumbar Spine Degenerative Classification (MRI)** is downloaded by
  `Desktop/lstv-detector/slurm_scripts/00_download_data.sh` (Kaggle competition, an earlier MRI project, last commit
  2026-06-13); `docs/ruleclass/CLASSIFIERS.md` R37 keeps it out of the CT table. No SchwingNet bank uses it.

---

## 16. Unknowns

| fact | where looked |
|---|---|
| Per-source composition of the body detector's `yolo_v3` and `yolo_v4z` training sets (is AASCE in them?) | `DATA_MANIFEST.md` line 17917 and unknown #21; `MANIFEST_DATA_MODELS_RESULTS.md` §5.3; `DATA_ACCOUNTING.md` §3; `mem:xray-corner-detector-status` |
| Per-source render counts inside `allspine_v9` (only films are logged locally) | `XRAY_DATASET_USAGE.md`; `DATA_COMPLETENESS_AUDIT.md` line 536; `LINEAGE.md` |
| Whether `physics_drr`'s 1,321 implant renders come from CTSpinoPelvic1K `implant_ct`, TotalSegmentator `implant_ts`, or both | `sources.json`; `PATIENT_IDENTITY_SPEC.md` §3 #4 (558 CTSP people); `DATA_COMPLETENESS_AUDIT.md` line 67 ("implant_ts feeds physics_drr") |
| Which bank the MODEL_CARD fold-0 crop counts describe, and why they sum to 31,396, not 31,446 | `MODEL_CARD.md` §3.2; `DATA_COMPLETENESS_AUDIT.md` line 538 |
| Whether any fold model with an `allspine_v9` base sample (`carmlspine_cv_v9.sh`) was trained | `LINEAGE.md` lines 621-632; `DATA_MANIFEST.md` A2 (`carm_cvdaymix0_v9`) |
| Whether `slurm/data_accounting.sh` was ever run on the real corpus after 2026-09-22 | `DATA_CONTRIBUTION.md` §6; grep of every `.md`/`.json`/`.txt` in the repo |
| Whether the grid copy of `tools/realxray_banks.json` lists `cobra_elekta_v3` and `cobra_elekta_g3test` | local JSON; `DATA_MANIFEST.md` line 14766 |
| Which COBRA bank (`cobra_elekta` or `_v3`) the current detector numbers read | `DATA_COMPLETENESS_AUDIT.md` line 1696; `corpus_census.md` §5 |
| Why Spinal-AI2024 counts 20,001 files on disk against 20,000 released | `XRAY_DATASET_USAGE.json`; `DATA_COMPLETENESS_AUDIT.md` lines 561, 573 |
| Why the RSNA census finds 2,022 study directories against 2,019 train studies (the census matches any `*_images/` directory, so test-image studies are a likely reading; the test count is not recorded) | `tools/other_ct_fetch.py` line 207; `other_ct/SUMMARY.md`; `DATA_MANIFEST.md` card |
| What besides the 203 GB zip makes the RSNA folder 236.8-237 GB | `DATA_COMPLETENESS_AUDIT.md` lines 62, 584; `mem:grid-quota-and-deleted-banks` |
| Whether IRB determination 2026-269 covers the RSNA 2022 archive (competition rules, not a DUA) | `packet_src/statements.md` lines 25, 57 |
| The VinDr separate IRB determination number and date | `packet_src/statements.md` line 61 ("[[PENDING G0]]") |
| What the `cm_spine` Drive file is | `DATA_COMPLETENESS_AUDIT.md` lines 74, 569 |
| Why 2,293 DeepFluoro vendor frames, the BUU AP films, the BUU(2000) labels and `synth_rare` are unused (no written criterion exists) | `DATA_COMPLETENESS_AUDIT.md` "Unknown" section |
| Whether `~/corpus_final/` (G4) or `SchwingNet/results/final/` (G5) exist on the grid | `FLAGSHIP_PLAN.md`; repo grep |
| Whether the 81 SEEN rows are now all labelled in `SchwingNet/main.tex` | `EVAL_LEAKS.md` preamble (the manuscript workflow owns it) |
