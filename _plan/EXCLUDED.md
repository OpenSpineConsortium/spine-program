# EXCLUDED: what was deliberately not included, and why

Written 2026-10-08 for `C:/Users/grego/OneDrive/Desktop/spine-program/`. Every row of `DISPOSITION.tsv` whose `project_folder`
is `EXCLUDE` (311 rows: 305 excluded outright, 6 referenced by path only) or whose `action` is `exclude` inside a project folder
(28 rows, recorded as "not copied, and why" in that folder's `MANIFEST_LOCAL.md`) is counted here: 339 rows in all, tallied by
`scratchpad/plan_build/excluded_tally.py` over the TSV. The tally regexes are coarse at the margins (a row is counted once,
in the first category whose rule matches), so the counts per category are the tally's and the prose below moves a handful
of rows to the category a reader would expect; the row ids in `DISPOSITION.tsv` are the authority. Personal and
administrative files are summarised by kind and count and their names are not reproduced here (they are in the TSV, which
is required to carry one row per inventory row; the TSV's reason column for those rows is generic).

Beside the excluded rows, this file lists the material that is not copied but is **kept by path** in a project folder's
`MANIFEST_GRID.md` or `MANIFEST_LOCAL.md` (imaging data, weights, files over 25 MB, third-party literature, byte-identical
twins), because Greg asked that nothing of value be lost and a path with a size and a reason is how a thing that cannot be
copied is kept.

---

## 1. Personal and administrative (145 rows: 102 personal, 43 administrative)

Names not reproduced. By kind, from `desktop_root_loose_files.md`, `ctsp_repo_root_and_sibling_folders.md` section 1.3 and
`inventory3_other_spine_folders.md` section 2.10:

- residency application material (the `ERAS_2026` and `VSLO_APP` folders, 11 GB; a personal statement; a standardized letter
  of recommendation; a CV; interview preparation notes), taxes (`2026_TAXES`), a lawsuit and its correspondence
  (`small_claims_lawsuit`, two "Re_" mail folders, two USPS request folders under `NextPaper/`), housing and insurance
  (`RO_APT`, `PROOF_OF_QUALIFIED_HI`), educational expenses, the PhD defence and qualifying-exam folders (`PhD`, `profqualexam`),
  the residency onboarding paperwork folder (`onboarding`: I-9, passport scans, immunisation and background-check records, a
  Login.gov recovery key), `stepwork`, employment documents (a benefits guide, an independent-contractor PDF, a 2017 summer
  research abstract book), `celebrate_life/` (a community event with contact lists);
- the F30 fellowship paperwork (`F30/`, the RPPR documents, the sponsor progress-report letters of 2024 and 2026, a cost-sharing
  spreadsheet) and a 2021 F30 research plan in another field;
- clinical teaching and patient material: `ER` and `TRAUMA` (teaching images), `nsurg` except `nsurg/AACA` (talks, a non-spine
  case-report folder with a patient's lab and pathology documents, a copy of a personal website), `CASE_HIEBER` (file names
  suggest a cervical case report, but it holds patient documents and consent pages: out unless Greg decides otherwise),
  `MANUSCRIPT` (a non-spine BMJ case report with consent pages), `bhargav'sabstract` (another student's tables),
  `MBR_CoAuthor_Review_2026-09-07` (another study's review package), `GREG_PRES.pptx` and `SPINAL_AVM.pptx` (spine teaching
  decks, clinical teaching not research: referenced by path from 99_archive);
- administrative templates and guidance: the CNS speaker PowerPoint template, the ACCME poster guidelines, the NRMP and
  counselling PDFs, vendor documentation (Remote Development FAQ, VS Code extension publishing, Resend DNS), `Claude Setup.exe`;
- `Desktop/IRB/co-investigators.xlsx` (names), `IRB/GREG/` and `IRB/HAZEM/` (CITI certificates), `IRB_2024 Tenet Resident
  Benefits Guide.pdf`, `IRB_IndContract_GSchwing_24926.pdf`, `CTSpinoPelvic1K_coauthor_signoff.xlsx` (co-author e-mail addresses;
  the project needs a redacted authorship-approval record written by Greg).

Why: the task's list (residency applications, taxes, lawsuit, benefits, housing, licensing exams, PhD and qualifying-exam
folders, case reports outside spine, Lexis searches, personal data); classified from file names and not opened.

## 2. Another study (38 rows)

U251 glioblastoma / LITT and other non-spine work: `u251-xenograft-murine-RNASeq-study` (4.6 GB, a public repository), `u251`
(empty), `nsurg/RAJ`, the seven memory notes (`u251-cibersort-deconvolution`, `u251-multiomics-sample-pairing`,
`u251-name-sweep-traps`, `u251-project-containment`, `u251-translation-fall-il68b`, `litt-contralateral-two-readings`,
`cns-abstract-418-deck`), `ctsp:paper/cns2026/abs418_tables.json`, `Ablation video_TNN_18Sept26.pptx`, the three
`bq_cibersortx-*.html`, `MAN_PREP.pdf`, `v2_inspect/Figure1_Letter_NeuroOnc.pdf`, the CNS/SNO LITT abstract with co-author
edits, the annotated LITT manuscript JNS24-1395 (three copies), the Neuro-Oncology letter template filled with the post-LITT
letter, the two ONC201 glioma papers, `FHER.png`, `SCHWING_PRESENTATION_NSURG.pptx` (51 MB) and its lock file, the Neurocheck
provisional zip, `PupillometerPLR.zip`, `Experimental_planning.docx` (a PhD simulation note), the peritoneal-metastasis case
report (folder and zip), `NextPaper/{Figure_Caption.txt, Publication_Figure_9Panel_VOLCANO_COMPLETE.*, U251_Final_Report.html,
general_stats_table.tsv, xengsort-summary-table.tsv}`, `ds007958` (an OpenNeuro 7T brain QSM clone; why it was cloned is not
recorded), `ama.bst`; on the grid `$RS/u251_multiomics` 1,115.871 GB, `u251_science` 594.039 GB, `u251_host` 434.177 GB,
`u251_meth`, `u251_geo_meth`, `u251_envs`, `u251_raw`, `~/u251-xenograft-murine-RNASeq-study`, `$RS/Rlib`, `Rlib_cibersort`,
`$RS/containers/bioconductor-minfi_1.48.0.sif`. Why: U251 containment (Greg, 2026-09-26; `context/u251-project-containment`
is itself not copied); not spine.

## 3. Credentials and session files (20 rows; paths only, never contents; Greg rotates or revokes)

`ctsp:LATERAL_ATLAS/key.txt` (an AWS access key id and secret; its first two lines were printed into a tool output on
2026-10-08: treat as exposed), `Desktop/NeurIPS/client_secret_*.apps.googleusercontent.com.json` and
`Desktop/client_secret_*.json` (Google OAuth), `Desktop/openapi_key.txt`, `NextPaper/spinopelvic-seg-mlhc/.git/config` (a GitHub
token in the origin URL; the whole folder is excluded as a superseded twin), `nsurg/AACA/firebase/` (a Firebase service-account
file with a `private_key` field), `onboarding/personal_key.txt` (Login.gov), `ctsp:.env`, `ctsp:cookies.txt` (1 MB), the Cerner /
Citrix `.ica` session files (eleven in the `ctsp:` root, two at the Desktop root, six in `xrsp:` of which one is tracked at
4f22935 and present on the grid clone, with `Unconfirmed 31234.crdownload`), `Desktop/FJP.docx` (an ssh login line),
`ctsp:go2432@warrior__.pdf` (a printed login banner), `ssn:docs/CREDENTIALS_SETUP.md` (credential locations),
`HANDOFF/INFRASTRUCTURE.md` section 9, the three credential-location memory notes (`hf-org-token-location`,
`hf-osc-token-and-namespace`, `fluorocap-credentials-and-resolution`); on the grid `~/github` (41 B, a GitHub personal access
token, mode 600 since 2026-10-08), `~/CTSpinoPelvic1K/.token` (38 B), `~/XRSpinoPelvic1K/*.ica`, `~/.fluorocap/`, and by name only
`~/.hf_org_token`, `~/.hf_osc_token`, `~/.zenodo_token`, `~/.kaggle/`, `~/.netrc`, `~/.ssh/`, `~/.google_authenticator`,
`~/.gdrive_token`, `~/.geo_ftp_pass`, `~/pass_file`, `~/private`, `~/.certs`; `C:/Users/grego/.beethoven-vendor` and the grid
`~/.beethoven-vendor` (never read). `Desktop/googlec3911e7fb095977e.html` is a site-verification token whose tracked copy is
in the website repository (not copied under 12). Why: tokens are read from files only and never copied; whether the GitHub
token and the Firebase key are still live is not recorded.

## 4. Greg's private records (21 rows)

`HANDOFF/GREG_ONLY/` (`README.md`, `PRIVATE_STATE.md` sections 1-6: the commercial stance, credential names and locations,
the disclosure / purge / TTO / provisional state, the personal and contact data held back from the student copies, who may
read which file; `context/` with the original `MEMORY.md` and the five moved notes; `context_beethoven/` whose six notes travel
only as hand-redacted copies into 11), `Desktop/private_ip/` and `$RS/private_ip` 0.634 GB (the signed invention-disclosure
forms, the TTO package of 2026-09-25 and its follow-up decks), `ctsp:COMMERCIALIZATION.md` (two copies inventoried; Greg's
standing instruction: never in a project folder; 01 cites it by path), `ssn:docs/INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md`,
`PATENT_PACKAGE.md`, `provisional/`, `disclosure_audit.json`, `disclosure_forensics.json`, `disclosure_evidence/`,
`research_patent_2026-09-18.json`, `research_registration_free_2026-09-18.json`, the stray mangled-path folder in `ssn:` (six
tracked duplicates of `docs/disclosure_evidence/`; `git rm` it in the source), `HANDOFF/MANUSCRIPTS.md` section 15, the memory
notes `commercialization-stance` and `schwingnet-disclosure-scrub`, the live `mem:MEMORY.md` (its one-liners carry leaked
numbers; `HANDOFF/context/INDEX.md` replaces it). Why: Greg's private filing and commercial records; referenced by path and
commit from `01_carm_level_detection/MANIFEST_CODE.md` and `MANIFEST_LOCAL.md`; the decision whether any of it enters the
private repository is Greg's (`PLAN.md` section 5).

## 5. Imaging data, arrays and weights: excluded rows (22) and everything kept by path

Excluded rows: `spine-detector/dist/` (four ONNX exports 42-84 MB and 12 BUU / Mendeley films with labels; the website copies
were removed 2026-09-14 and must never be reintroduced), `spine-detector/{data, notebooks, configs}` (empty or placeholders),
`ctsp:Archive.zip` (182 MB; 2,682 PNG `JW_T1_J1_L_*`; origin not recorded), the label volumes under `ctsp:scratchpad/`,
`rib_fix_work/`, `spine_fix_work/`, `hardware_review/verify/`, `Desktop/CTSpinoPelvic1K/qc.tar.gz` (344 MB),
`SpineSurg-CT/viz.tar.gz` (983 MB) and the ITK-SNAP tarball, `NeurIPS/` volumes, the BUU zip (917 MB), `checkpoint_best.pth`
(191 MB) and the profiler trace, `itksnap_review/*.nii.gz` (21 CTs), `NextPaper/flip18_review` volumes and zip (4.26 GB),
`xrsp:dataset2024.zip` (4.0 GB, identity not recorded), the Mendeley landmark zip, `xrsp:annot/*.npz` and `examples/*.npy`,
`openspineconsortium.github.io/pacs/{testimgs, sllp, webtest}` and `headshots/*.orig`, the DICOM trees, `.pth` and archives under
`nsurg/AACA`, `FluoroCap_reading` and `FluoroCap_screening` (3 of 64 and 2 of 104 reader pages with licence-bearing panels),
`sn:results/learning/*.npz` (31-33 MB each), `sn:results/manifold/deep.npy` (124 MB), `sn:results/age_sex_cache/` (35 MB; the
product `age_sex_by_source.json` is copied), `ssn:spine_data_review/runs/` (1.8 GB; nine `hf.jsonl` over 25 MB),
`sn:results/reader_e/features_j1.csv` (40 MB; its `.gz` twin is copied). Why: the task's rule; each is recorded in the owning
folder's `MANIFEST_LOCAL.md` with its size.

Kept by path, not copied (reference rows in the project manifests; 212 grid rows and about 60 laptop rows): every grid
volume, bank and checkpoint of `grid_manifest.md` sections 2-6, by owning folder: 01 the four weights, the fold models,
`$RS/data/{carmlspine 86.834 GB, realxray 3.408 GB, cobra2026 808.615 GB, deepfluoro_h5, deepfluoro_vendor 110.987 GB,
geneva_hip_src, ljubljana, spinesac, external/fluoro_video 262.801 GB, or_ready 867.951 GB}`, `HOME/{model_night, bench, scaling,
level_id_service}`, the identity tables; 02 `$RS/data/fig6` 13.920 GB (the blinded gate), `rare_class`, `HOME/lstv_flag`,
`HOME/FluoroCap` 316 GB; 03 the v11 working copy 196,195,055,488 B (the only grid copy of the 802 CTs), the build tree, the
nnU-Net raw and results trees (348.6 GB), `$RS/neurips_*`, `ctsp_april` 86.883 GB, `HOME/ablate` 201.6 GB; 06 `$RS/ruleclass`
48.579 GB, `anomaly_harvest` 325.817 GB, the 19 family-B collections (`idc` 706.083 GB down to `csi2014` 6.641 GB),
`versefusion` raw 194,191,642,435 B; 07 `HOME/spine-detector` 382 GB, `HOME/XRSpinoPelvic1K` 22.428 GB, the film crop banks;
08 the physics and render banks, `$RS/data/polypose` 87.713 GB, `devcorpus` 18.280 GB, `HOME/data/TotalSegmentator` 82.0 GB and
`_v3` 89.8 GB; 10 the environments and containers (`$RS/envs` 39.923 GB); 11 `$RS/hpcworker`, `$RS/ashley`, `$RS/tmp` 30.278 GB.
On the laptop: `ctsp:BUU-LSPINE_400/` (1,603 files), `BUULSPINE_3600/` (9.96 GB), `AASCE19/Archive.zip` (85 MB), `CSPINE_ARCHIVE/`
(2.86 GB), `LATERAL_ATLAS/` (1.02 GB; its `key.txt` is a credential), `infobot/images.zip` (288 MB; origin not recorded),
`ribseg_v2.zip` (608 MB), `2D-3D-GS.zip` (79 MB), `PIG/*.zip` (205 MB), `ckpt_mirror/` (the Dataset803 folds; its four training
logs are text and are copied into 03), `ctsp:data/` (802 + 802 + 173 + 303 + 12 label volumes), `np:viz/*_lstv_3d.html` (359 MB),
`nsurg/AACA` overlays and 3-D renders, `sn:figures/*.tif` (3.5-39 MB), `sn:results/eval_gate/touched.json` (55.3 MB), the two
SchwingNet packets of 89 MB, `sn:results/transitional_registry/contact_sheets/` (26 JPG, 17 MB), `np:VerSeFusion_grid_derived/qc`
(374 PNG, 59 MB), `Desktop/TEST_XR.png` (a radiograph of unrecorded origin: never into a repository until its source is known).

## 6. Superseded duplicates, builds, scaffolds and empty leftovers (22 excluded rows, plus the twins kept by path)

Excluded: the SchwingNet build logs and local 2026-09-24 compiles (`main.pdf`, `supplement.pdf`, `*.log`, a crash dump), the 16
earlier `packet_build` PDFs and `packet_cameraready/` (the 2026-09-27 pair is copied), `ctsp:cr.json` (a Crossref dump), the twelve
`ctsp:_w*.sh` watch loops, `ctsp:MDPA.pdf` (2026-09-16) and `MDPA_OL.zip` (superseded by `Desktop/MDPA_FINAL.pdf`), the two
Desktop overleaf folders (nothing unique: 2,398 and 501 diff lines against the current tex; git history holds them),
`Desktop/new_repo` and `new_repo.zip` (the 2026-04-18 scaffold of `spinesurg-ct-nnunet`), `Ashley Bridge for testers` and the
6.0.0 tester zip (superseded by Beethoven release 14.0.0), `ssn:reader_space/_original_space/` (the earlier review_service
backup; carries the banned word in five files), `ssn:tools_tmp_sync/`, `ssn:splits_5fold.json` (0 bytes), the `.gitkeep`
placeholders, `ssn:paper/qi_universal_protocol/main - Copy.pdf`, `ssn:tmp/` (653 tracked scratch files whose products are in
`sn:results/`; by reference), the empty folders `radiopedia/`, `BUUSPINE/`, `NextPaper/reviewlstv/`, `$RS/data/morphdef`, the
stray `.gitignore` and `.nojekyll` in `NextPaper/`, `Desktop/new/` (one June render). Kept by path as twins or earlier
generations: the byte-identical `2026_269 ... .pdf`, `IRB Not HPR Determination 4.21.26.pdf` (three paths), `CNS2026_Schwing_
SchwingNet_CNStemplate.pptx` (= v10), the Desktop copies of `3474_*.pdf`, `MLHC_*.pdf`, `arxiv_prev.pdf`, `TechFair_LSTV_Schwing.pptx`
(three paths), `AI_Imaging_Workshop.pdf` (two sizes), the Desktop source zips and tar.gz older than their `paper/mpda` and `dist/`
counterparts, the superseded CNS decks v2, v3, v9, v11, `Desktop/CTSpinoPelvic1K` (older clone, an ancestor of 7ddfe38),
`Desktop/morphometrics/transition_morphometrics.csv` (an earlier generation), `np:spinopelvic-seg-mlhc` (anonymised twin; see
section 3), `CTSP1K_private/CTSpinoPelvic1K_prepurge_20260911.bundle` (97.8 MB; the public repo's history before the personal-
material purge: reference only, never push), `ctsp:dist/` (regenerable), the `.bak`, `.pre0631` and `.v10.csv.bak` morphometrics
generations. Why: a copy exists once in the owning folder with both paths recorded (`ctsp_repo_root_and_sibling_folders.md`
section 4; `desktop_root_loose_files.md` "Superseded chains"; `99_archive/README.md` carries the chains).

## 7. Environments, installers, caches, shortcuts and junk (33 rows)

The 24 Desktop `.lnk` shortcuts (18 of them `pkwrap IWA test*.lnk` of 2026-10-02), installers (`Claude Setup.exe`, `duo-win-login`,
`Firefox.exe`, `Slicer-5.10.0` 251 MB, `tailscale-setup`, `VictoryShieldWindows.exe`, `DiscordSetup.exe` 121 MB, `GhostType`,
`itksnap-4.4.0-*.exe` 97 MB, `vwi/Miniforge3-*.sh`), `NextPaper/vwi/.venv` (887 files), `desktop.ini`, a hardware plugin DLL, Word
lock and temp files, crash dumps (`*.stackdump`, four), `ostk:build/`, the `egg-info` and `__pycache__` and `.pytest_cache` folders,
a stray wheel; on the grid `~/.cache` 10.484 GB, `~/anaconda3`, `~/singularity_cache`, `$RS/singularity_cache` 17.040 GB,
`$RS/containers`, `$RS/tmp` (hpcworker temp), `/rs/rs_grp_oschome/shared/access` (the access service's closed folder), the
2001-2024 molecular-simulation toolchains and old installers at the HOME root, the two 2022 download leftovers. Why: not
research content; re-downloadable.

## 8. Files carrying student, reviewer or researcher identities (4 excluded rows; the rest handled by redaction)

Excluded outright: `ctsp:paper/mpda/EMAIL_ASHLEY.md` (correspondence), `ctsp:spine_tampering.csv` (keyed by reviewer usernames),
`NextPaper/osc/` (a 2026-05-19 clone of the website with student headshots), the lumped `ctsp:proposals/` e-mail row (its two
outreach drafts are copied redacted into 11 and its scoping review into 09). Referenced by path, never copied:
`openspineconsortium.github.io/contributions/manifest.json` and `headshots/` (public by design), `Student_Projects/board.json`,
`spinesurg-ct-annotator/assignments.json`, the review Space trees on the grid (`~/CTSpinoPelvic1K-review`,
`~/ctspinopelvic1k-review-triaged`, `~/spinesurg-ct-annotator.backup`), `paper/mpda/_others|_schehr|_upd/word/people.xml`, the
participation survey CSV and zip, `NextPaper/CNS 2026 ABSTRACT PROJECTS.csv`, the six e-mail drafts and `EMAIL.md` in
`CTSP1K_private/proposals_backup_20260911/`, `ctsp:morphometrics/annotator_names.csv` (tracked in a public repository: Greg
decides its removal; not copied), `student_vertebra_work.csv` (not opened). Redacted twins are copied where the research
content matters (the list is `PLAN.md` section 2 rule 7). Why: the personal-data rule.

## 9. Templates and third-party documents (16 excluded rows; literature kept by path)

Excluded: `ctsp:mlhc/`, `BIBM/`, `AR/` (journal and conference templates only; the real manuscripts are under `NextPaper/`),
`OUP_General_Template.zip`, `med_phys_latex_template_v2021.zip`, `Manuscript_Template.docx`, the vendor documentation of
section 1, the four 2025-2026 arXiv ML-theory PDFs and the watermarked prompt-writing guide (contract side work), `youmans`
(1.2 GB of textbook sections), the 60 MB neurosurgery handbook and the literature PDFs and phone photos in `NeurIPS/`,
`ssn:buu.pdf` (a 410-byte "Access Denied" page), `ssn:out.bin` (an HTML page saved as `.bin`; purpose not recorded), `ssn:pat.html`
(a saved Google Patents page), the saved web pages `ctsp:docs/ajnr.html`, `ukb.html`, the two `sp_978-*.html`,
`NextPaper/refs/` (AlexNet), the two JNS Spine PDFs and the satellite-imagery GAN paper in `NextPaper/`, the AACA 2023-2025
programmes and published papers under `nsurg/AACA`, `Desktop/IRB/A large language model for complex cardiology care.pdf`.
Kept by path and cited by identifier from the bib files (library access was cut 2026-06-30, so the paths matter;
`99_archive/LITERATURE_BY_PATH.md` lists them): `COBRA.pdf`, `RIBSEG.pdf`, `TS_DS.pdf`, `PANJABI_1991_FULL.pdf` and `_fixed`
(the source of Table 3 in `level_references.csv`), `panjabi_1976.pdf`, `Panjabi_1976_JBJS_thoracic.pdf`, `STUMP_RIBS.pdf`,
`Sun_2021 ...`, `PG-Net ...`, `Development_and_Evaluation_of_a_Robotic_System ...`, `CaseReports_T12_hypoplastic_rib.pdf`,
`AITR-2002-001.pdf`, `Protocols for Reproducible Machine Learning Research.pdf`, `Spine chapters.zip`, `MANUAL_REFS/`, the
`SpineSurg-CT` literature, `2D-3D-GS_UG.pdf`, `PIG_LEVELCHECK.pdf`, `AI_Imaging_Workshop.pdf`, `xrsp:journal.pone.0347290.pdf`
(CC-BY; this one is copied into 07). Why: copyright; available from the publishers.

## 10. Logs, caches and oversize text excluded inside project folders (the remaining "not copied" rows)

`ctsp:scratchpad_*.txt`, `scratchpad_*.log`, `scratchpad_resweep_stats.json`, `scratchpad_gapcheck/` (session logs; `scratchpad_sweep.log`
650 KB), `ostk:_v.txt` (a UTF-16 scratch readout), `ssn:grep.exe.stackdump` (tracked by mistake), `sn:results/reader_e/features_j1.csv`
(40 MB; the `.gz` twin is copied into 05), the SchwingNet logs of section 6. Why: logs and oversize files; the products are
elsewhere.

## 11. Material whose exclusion is provisional (Greg decides; `PLAN.md` section 5)

`CASE_HIEBER` (a possible cervical case report with patient documents), `HANDOFF/GREG_ONLY/` (whether any of it enters the
private repository), the six Beethoven notes (copied redacted into 11; Greg may delete them), `ctsp:morphometrics/annotator_names.csv`
and `spine_tampering.csv` (whether they leave the public repository), `$RS/data/rsna_2022_cspine/raw` (237 GB used by nothing;
keep or delete, OQ A19), the 1,590.3 GB of migration deletion candidates and B13 (OQ A26).

## 12. Unknowns about excluded material (not recorded in any file read)

The origin of `ctsp:Archive.zip` (2,682 PNG); the identity of `xrsp:dataset2024.zip`; why `ds007958` was cloned on 2026-06-20;
whether `CASE_HIEBER` is a case report Greg wants kept; the content of `2026 AACA_0377.jpg` (10 MB, not opened; referenced from
99); whether the GitHub token in `spinopelvic-seg-mlhc/.git/config` and the Firebase service-account key are live; what removed
the TCIA CT Colonography raw and NIfTI trees from HOME (the likely script `~/cleanup_v1v3_tcia.sh`, 2026-09-01, unread).
