# Literature kept by path

Every third-party PDF, chapter and saved page that the spine work kept on the laptop, with its identifier where a file
records one. None is copied (copyright; available from the publishers); the paths matter because WSU Libraries dropped
DMC residents on 2026-06-30 (`memory/wsu-library-access-cutoff.md`), so a lost local copy is not re-fetchable through the
university by default. Paths are as they were on 2026-10-08, written relative to the laptop Desktop root whose full location is recorded only in `MANIFEST_LOCAL.md` (history, not a dependency); sizes from `ls -l` that day; "not recorded" means no file
read on 2026-10-08 states the identifier. The bib files that cite them: `SchwingNet/refs.bib` and `paper/rsnai/refs.bib`
in spinesurg-ct-nnunet 097933a; `paper/mpda/ctspinopelvic1k.bib` and `mdpa_extra.bib` in CTSpinoPelvic1K 7ddfe38;
`SpineSurg-CT/SpineSurgCT_references.bib`.

## 1. In the CTSpinoPelvic1K working copy root (`Desktop/CTSpinoPelvic1K-1/`, untracked; DISPOSITION ctsp r100)

| file | size | identifier or description |
|---|---|---|
| `COBRA.pdf` | 6,825,932 B | the COBRA dataset paper (the Elekta cone-beam projection set used in the device work); identifier not recorded here |
| `RIBSEG.pdf` | 5,245,405 B | the RibSeg dataset paper (the rib benchmark the competitor space names); identifier not recorded here |
| `TS_DS.pdf` | 2,342,023 B | TotalSegmentator, Wasserthal et al. 2023, Radiology: Artificial Intelligence; the same byte size as `SpineSurg-CT/wasserthal-et-al-2023.pdf` (hash not run) |
| `PANJABI_1991_FULL.pdf`, `PANJABI_1991_FULL_fixed.pdf` | 4,465,615 B; 4,674,615 B | Panjabi et al. 1991, Spine 16(8):888-901, thoracic vertebrae quantitative three-dimensional anatomy; the source of Table 3 in `morphometrics/level_references.csv` (memory note panjabi-1991-page-892, owned by 05); a copyrighted scan, never into a repository |
| `panjabi_1976.pdf` | 866,830 B | Panjabi 1976, Journal of Biomechanics, the flexibility / stiffness paper (a different paper from the JBJS one below; `../_plan/inventories/desktop_root_loose_files.md`) |
| `Sun_2021_Phys._Med._Biol._66_175002.pdf` | 1,754,240 B | Sun et al. 2021, Physics in Medicine and Biology 66:175002 (from the file name) |
| `PG-Net_Progressive_Guidance_Network_via_Robust_Contextual_Embedding_for_Efficient_Point_Cloud_Registration.pdf` | 4,122,614 B | PG-Net, point-cloud registration; venue not recorded |
| `Development_and_Evaluation_of_a_Robotic_System_for_Safe_Cardiac_Sheath_Delivery.pdf` | 3,918,337 B | not spine; venue not recorded |
| `CaseReports_T12_hypoplastic_rib.pdf` | 1,657,972 B | a T12 hypoplastic-rib case report (the rib-phenotype line, 06); identifier not recorded |
| `AITR-2002-001.pdf` | 1,712,245 B | MIT AI Technical Report 2002-001 (from the file name) |
| `Protocols for Reproducible Machine Learning Research.pdf` | 676,065 B | identifier not recorded |
| `Spine chapters.zip` | 2,741,653 B | three Thieme textbook chapters (ctsp r100) |
| `AI_Imaging_Workshop.pdf` | 90,034 B | the 20 June 2026 teaching-workshop agenda (not third-party; listed because it sits with the literature; a 90,116 B variant is tracked in the website repository) |
| `2D-3D-GS_UG.pdf` | 707,342 B | a user guide for a 2-D / 3-D registration package; identifier not recorded |
| `PIG/PIG_LEVELCHECK.pdf` | not recorded | Goswami 2020, IEEE Access (the pig LevelCheck study), beside seven pig CBCT / CT / planar zips of about 205 MB (imaging data, excluded) |

## 2. `MANUAL_REFS/` in the same root (ctsp r101; the manual reference checks of `paper/mpda/_schehr`)

| file | size | identifier or description |
|---|---|---|
| `ACR.pdf` | 353,331 B | an ACR guideline (title not recorded) |
| `NASS.pdf` | 186,120 B | a NASS guideline (title not recorded) |
| `BENZEL_CH_1.pdf` | 665,402 B | Benzel, Biomechanics of Spine Stabilization, chapter 1 (from the name) |
| `KONIN_WALZ.pdf` | 2,652,196 B | Konin and Walz, the lumbosacral transitional vertebra review (from the name; cited in the dataset article) |
| `VERIDAH.pdf` | 6,807,332 B | the VERIDAH / SPINEPS rib paper, Moeller et al. 2025; the same byte size as `SpineSurg-CT/Moller_et_al_2025.pdf` |
| `panjabi1991.pdf` | 861,004 B | Panjabi 1991 (a smaller scan of the paper in section 1) |
| `panjabi1992.pdf` | 578,912 B | Panjabi et al. 1992, Spine 17(3):299-306, lumbar vertebrae quantitative three-dimensional anatomy |

The folder also holds two Cerner `.ica` session files (2,119 B and 2,118 B): credential-like, never copied, Greg deletes
them (`MANIFEST_LOCAL.md` section 2.3).

## 3. `Desktop/SpineSurg-CT/` (beside the April 2026 repository; ctsp r124)

| file | size | identifier or description |
|---|---|---|
| `2405.01204v1.pdf` | 2,999,908 B | arXiv:2405.01204 |
| `ANATOMICAL_LSTV_PAPER.pdf` | 1,911,676 B | an anatomical LSTV paper; identifier not recorded |
| `CTSpine1K.pdf` = `Deng_et_al_2024.pdf` | 5,895,768 B each | Deng et al. 2024, the CTSpine1K dataset paper (two copies of the same size) |
| `Kwak_2025.pdf` | 1,397,165 B | Kwak 2025, the only 2-D LSTV model in the literature landscape (memory note lstv-data-landscape, owned by 06) |
| `Li_et_al_2025.pdf` | 3,410,341 B | Li 2025 |
| `Liu_et_al_2021.pdf` | 3,661,468 B | Liu 2021 |
| `Moller_et_al_2025.pdf` | 6,807,332 B | Moeller et al. 2025 (VERIDAH; see section 2) |
| `Schinz_et_al_2025.pdf` | 2,207,674 B | Schinz 2025 |
| `Yang_et_al_2025.pdf` | 2,656,608 B | Yang 2025 |
| `TotalSpineSeg_Warszawer_Molinier_et_al.pdf` | 1,150,724 B | TotalSpineSeg, Warszawer, Molinier et al. |
| `wasserthal-et-al-2023.pdf` | 2,342,023 B | TotalSegmentator, Wasserthal et al. 2023 |
| `fmed-12-1511487.pdf` | 8,782,734 B | Frontiers in Medicine 12:1511487 (from the name) |
| `Data - Pelvic Bone Fragments with Injuries ...pdf` | 2,526,698 B | the pelvic bone fragment challenge data paper |
| `ML4H_2025_Proceedings_Dataset_Paper.pdf` | 544,207 B | an ML4H 2025 proceedings dataset paper (author instructions or exemplar; not recorded) |
| `editorial,+Journal+manager,+BookReview.pdf` (two copies) | 372,481 B each | an editorial / book review PDF; not recorded |
| `Spine Segmentation Dataset Research.pdf` | 311,853 B | a generated research report; verify before citing |
| `irb/exempt_research_guidanceinstructions_2_15_23.pdf`, `irb/expedited_research_guidance_5_1_23.pdf`, `irb/irb-expedited-exempt-eprotocol-submitters-guidance-tool-october-2024.pdf` | 342,942 B; 242,119 B; 259,687 B | WSU IRB exempt and expedited guidance (regulatory guidance, not literature; the C-arm project's `regulatory/` cites the determinations themselves) |

## 4. At the Desktop root (`Desktop/`)

| file | size | identifier or description |
|---|---|---|
| `Panjabi_1976_JBJS_thoracic.pdf` | 1,491,031 B | Panjabi 1976, Journal of Bone and Joint Surgery 58-A:642 (the thoracic paper; `../_plan/inventories/desktop_root_loose_files.md`) |
| `STUMP_RIBS.pdf` | 3,723,865 B | Moeller et al., arXiv:2505.05004, the rib method of census arm B |
| `venetti.pdf` | 18,840,219 B | not recorded (name only) |
| `ACQUIFER.pdf`, `ACQUIFER_2.pdf` | 313,877 B; 352,036 B | name only; not opened |
| `2505.01595v2.pdf`, `2505.14338v3.pdf`, `2602.09959v1.pdf`, `2605.10395v1.pdf` | 2,681,012 B; 562,540 B; 1,195,605 B; 942,280 B | four 2025-2026 arXiv machine-learning theory papers; not spine (contract side work; `EXCLUDED.md` section 9) |
| `Spine Morphometrics_ Beyond Basic Measurements.pdf` | not recorded | a 26-page generated literature review of 2026-02-21 with no author; a map of the normative series for the morphometry parity work; every number in it must be checked against the primary paper before use (`../_plan/inventories/desktop_root_loose_files.md`) |

## 5. Elsewhere on the laptop

| path | identifier or description |
|---|---|
| `Desktop/XRaySpinoPelvic1K/journal.pone.0347290.pdf` (1,784,881 B; tracked at 4f22935) | PLOS ONE, doi 10.1371/journal.pone.0347290; CC-BY; copied into `07_plain_film_level_id` |
| `Desktop/nsurg/AACA/LSTV Vertebrae Labeling Manual.pdf`, `Deep Learning for Automated Spinopelvic Parameter Measurement Fro.pdf`, `Bullspine.pdf`, `AACA-2023/2024/2025-SCIENTIFIC-PROGRAM.pdf`, `EBM Starter Document_Jan2026.pdf` | the reading of the AACA 2026 LSTV MRI project; identifiers not recorded; `Morphometric Variability of the Kawase Triangle ...pdf` in the same folder is not spine |
| `Desktop/NextPaper/refs/` (AlexNet), the two JNS Spine PDFs and the satellite-imagery GAN paper in `NextPaper/` | names not recorded here (`EXCLUDED.md` section 9) |
| `Desktop/NeurIPS/` literature PDFs and phone photos; the 60 MB neurosurgery handbook | excluded (`EXCLUDED.md` section 9) |
| `Desktop/youmans/` (1.2 GB) | Youmans and Winn Neurological Surgery section PDFs and an epub; reading; excluded |
| `Desktop/IRB/A large language model for complex cardiology care.pdf` | not spine; excluded |
| `Desktop/spinesurg-ct-nnunet/buu.pdf` (410 B) | an "Access Denied" page saved as a PDF, not a paper |
| `Desktop/spinesurg-ct-nnunet/pat.html` | a saved Google Patents page |
| `Desktop/CTSpinoPelvic1K-1/docs/ajnr.html` (5,387 B), `docs/ukb.html` (250,341 B), `sp_978-3-030-00937-3_12.html` (3,038 B), `sp_978-3-030-87240-3_28.html` (3,038 B) | saved web pages: an AJNR page, a UK Biobank page, Springer chapter 12 of ISBN 978-3-030-00937-3 and chapter 28 of ISBN 978-3-030-87240-3 (from the file names); not copied (ctsp r14) |

## 6. The MANS teaching talk's reading (`Desktop/MANS_Talk/`; ctsp r136; cervical myelopathy and lumbar stenosis imaging)

| file | size |
|---|---|
| `DCM_Review.pdf` | 4,523,389 B |
| `fehlings-et-al-2025-ao-spine-clinical-practice-recommendations-for-diagnosis-and-management-of-degenerative-cervical.pdf` | 636,013 B |
| `lee-et-al-2012-a-practical-mri-grading-system-for-lumbar-foraminal-stenosis.pdf` | 643,868 B |
| `pfirrmann-et-al-2004-mr-image-based-grading-of-lumbar-nerve-root-compromise-due-to-disk-herniation-reliability-study.pdf` | 624,192 B |
| `tetreault-et-al-2017-the-minimum-clinically-important-difference-of-the-modified-japanese-orthopaedic-association-scale.pdf`; `tetrault_full.pdf`; `The Minimum Clinically Important Difference of ...` | 83,289 B; 602,968 B; 602,968 B |
| `The_modified_Japanese_Orthopae.pdf` | 631,963 B |
| `Frequency, Timing, and Predictors of Neurological.pdf` | 6,739,456 B |
| `Surgical decision-making for ossification of the ...pdf` | 4,807,984 B |
| `Surgical Threshold Measurements for Cervical Spinal ...` | 421,788 B |
| `Presymptomatic spondylotic cervical myelopathy an updated ...` | 271,792 B |
| `Preoperative Magnetic Resonance Imaging Is Associated ...` | 337,680 B |
| `Postoperative Resolution of Magnetic Resonance Imaging ...` | 965,580 B |
| `The Relationship Between MRI Signal Intensity ...` | 909,707 B |
| `Reliability of Quantitative Magnetic Resonance Imaging ...` | 346,107 B |
| `Qualitative Grading of Severity of Lumbar ...` | 582,948 B |
| `Clinical and MRI findings in lumbar ...` | 640,671 B |

Titles are as the file names give them; identifiers are not recorded in any file read. `docs/mans_talk/PERMISSIONS.md`
records which figures the talk reproduced and under what permission.
