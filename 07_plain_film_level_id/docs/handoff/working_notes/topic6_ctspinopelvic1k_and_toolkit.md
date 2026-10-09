# Topic 6: CTSpinoPelvic1K and the measurement toolkit (OpenSpineToolkit)

Handoff note written 2026-10-08 for a new student or a new Claude project. It covers the
CTSpinoPelvic1K dataset (how it was built, what is in it, what is wrong with it), every
measurement derived from it, the figures and tables of the dataset article, the review
spaces, the OpenSpineToolkit library, the post-operative synthesis code, and the two NextPaper
folders. It was assembled by reading files only. Nothing was run on the grid, and no network
was used.

## 0. How to read this note

**Repository abbreviations used in every citation**

| tag | path | remotes | branch |
|---|---|---|---|
| [CTSP] | `<repo:CTSpinoPelvic1K 7ddfe38>` | `origin` github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K, `osc` github.com/OpenSpineConsortium/CTSpinoPelvic1K (memory `push-both-github-remotes.md`) | `master`, 865 commits, head `7ddfe38` 2026-10-07 (`git log`) |
| [OSTK] | `<repo:OpenSpineToolkit cb43197>` | `origin` Gregory-Schwing-MD-PhD/OpenSpineToolkit, `osc` OpenSpineConsortium/OpenSpineToolkit (`git remote -v`) | `main`, 85 commits, head `cb43197` 2026-09-25; a local branch `pr5` also exists |
| [SEG] | `<laptop:NextPaper (folders 03, 99)>/spinopelvic-seg` | `origin` anonymous-neurips-ED/spinopelvic-seg, `osc` OpenSpineConsortium/spinopelvic-seg | `main`, 2 commits (`fd8d565` 2026-05-12, `c105981` 2026-06-23) |
| [SEGM] | `<laptop:NextPaper (folders 03, 99)>/spinopelvic-seg-mlhc` | anonymous-mlhc/spinopelvic-seg (see flag F1) | 1 commit `91b7e9e` "Anonymized release for MLHC submission" |
| [AR] | `<laptop:NextPaper (folders 03, 99)>/AR` | not a git repository | — |
| [BIBM] | `<laptop:NextPaper (folders 03, 99)>/bibm-spinopelvic` | not a git repository | — |
| [WEB] | `<repo:openspineconsortium.github.io>` | publishes openspineconsortium.com | head `c1800f8` 2026-10-02 |
| [SSN] | `<repo:spinesurg-ct-nnunet 097933a>` | private | `L6_Class` |
| [MEM] | `<live memory folder; HANDOFF/context/ holds the copies>` | the orchestrator's memory notes | — |

**Grid locations** (not visited; taken from documents): labels `~/data/CTSpinoPelvic1K/labels`
(v11), `labels_v10/` beside it, CT `~/data/CTSpinoPelvic1K/ct` ([CTSP] `CLAUDE.md` "Grid";
commit `73cc398` message). Grid checkout of [CTSP] at `/wsu/home/go/go24/go2432/CTSpinoPelvic1K`
([MEM] `grid-access.md`). Python env `~/mambaforge/envs/spineps/bin/python` ([CTSP] `CLAUDE.md`).
Grid copy of [OSTK] at `~/OpenSpineToolkit`, kept by rsync ([MEM] `ostk-canal-closing-regression.md`).

**Standing rules that bind this topic**: never the word Greg bans for "where a thing came from" (write origin, lineage, source; [MEM] `writing-preferences.md`); no fractional version
numbers (fold into the next integer version); figure captions at most 60 words; commit directly
to master in [CTSP]; push to both remotes, through WSL; never canonicalise orientation on a path
that writes a label; never import a fixed label map ([CTSP] `CLAUDE.md`; [MEM]
`writing-preferences.md`, `figure-captions-terse.md`, `commit-directly-to-master.md`,
`never-reorient-when-writing-labels.md`, `label-scheme-v4-vs-ostk.md`).

---

## 1. The line of work in one page, and its status

CTSpinoPelvic1K is a CT dataset of 802 abdominopelvic records from TCIA CT COLONOGRAPHY in which
the CTSpine1K vertebral masks and the CTPelvic1K pelvic masks, made for the same patients but on
unrecorded series, were matched to the series each was drawn on and placed in one coordinate
frame; ribs, femora, lumbar-rib classes and surgical hardware were added; and a set of
per-level morphometric and spinopelvic measurements was extracted and checked against published
values ([CTSP] `paper/mpda/main.tex` lines 246-560; `README.md`). The purpose is to ask whether
local morphology can name a vertebra at the lumbosacral junction without counting from C2
([CTSP] `CLAUDE.md` first paragraph).

| piece | status (date, file) |
|---|---|
| Dataset release v11 (802 records, id 29 retired) | built 2026-09-11 on the grid, promoted 2026-09-16 (commit `73cc398`); Zenodo version DOI 10.5281/zenodo.22797014 said to be published 18 Sep 2026 ([CTSP] `paper/mpda/cover_letter.md`); Hugging Face mirror still v10 labels on 2026-09-27 ([MEM] `hf-mirror-is-v10.md`). See contradiction C1. |
| Dataset article, *Medical Physics* Dataset and Software Article ("MPDA") | submitted; returned twice for format (2026-09-21 abstract in main document, [MEM] `journal-figure-and-style-rules.md`; 2026-09-25 supporting information as six files, [CTSP] `paper/mpda/supplementary.tex` header); last packet built 2026-09-25 ([CTSP] `dist/submission/`); editorial decision not recorded |
| arXiv preprint of the article | arXiv:2609.22760 ([CTSP] `paper/mpda/cover_letter.md`) |
| NeurIPS 2026 Evaluations and Datasets paper "Not All Spines Are Created Equal" (submission 3474, OpenReview D8yRWDAGQF) | accepted, poster; camera-ready corrected 2026-09-27 but those corrections are **uncommitted** in [CTSP] `CAMERA_READY_NEURIPS/` (git status at session start); upload status not recorded; 22 open items ([CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` "What remains for Greg") |
| Clinical paper "The iliac crest is an unreliable level landmark…" (target *Spine Surgery and Related Research*) | complete draft with numbers, last touched 2026-08-22 ([CTSP] `paper/clinical/main.tex` header; `git log`); numbers predate v6 hip corrections and v11 |
| MLHC 2026 descriptor | rejected ([MEM] `publication-roadmap.md` update 2026-07-24); PDF at [CTSP] `MLHC_2026_Research_Track_Paper.pdf` |
| BIBM wrap-up "From Segmented CT to Spinopelvic Measurement" | draft with `\TODO`s ([BIBM] `README.md`); the BIBM 2026 deadline (5 Jul 2026, [CTSP] `docs/ROADMAP.md`) has passed; whether it was submitted is not recorded |
| NextPaper/AR (NeurIPS draft, September revision) | frozen 2026-09-08 as a source document; content to be ported to NextPaper/RadAI, not extended ([MEM] `publication-roadmap.md` "2026-09-08 redirect") |
| OpenSpineToolkit (ostk) | working library, 94 test functions (count of `def test_` in [OSTK] `tests/`); one known regression unfixed (section 9.4); it silently falls back to a whole-sacrum plate on v11 volumes (section 9.5) |
| Post-op synthesis (`ostk.surgery`) | prototype, phases 1-4 done June 2026 ([MEM] `postop-spine-synthesis.md`); re-measurement of the synthesised image unreliable ([MEM] `postop-jaggedness-future.md`) |
| PolyPose morphology augmentation | generator built 2026-09-23 in [SSN], never pushed; DeepFluoro reproduction "REPRODUCED"; no validation report written ([SSN] `SchwingNet/results/polypose/REPRODUCTION.md`; no `VALIDATION.md` exists) |

---

## 2. Where the dataset lives

| copy | identifier | contents | source |
|---|---|---|---|
| Zenodo concept DOI | 10.5281/zenodo.22139642 | resolves to the current version | [MEM] `zenodo-deposit.md` |
| Zenodo v6 / v7 / v8 / v9 / v10 | 22139643 / 22242745 / 22293878 / 22639598 / 22642578 (v10 published 2026-09-07; labels.zip 1,074,544,275 bytes) | label versions; v6 first published 2026-08-27; v1-v5 were Hugging Face only and have no DOI | [MEM] `zenodo-deposit.md`; [CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` |
| Zenodo v11 | 10.5281/zenodo.22797014 ("published 18 September 2026") | 29 merged into 26 | [CTSP] `paper/mpda/cover_letter.md`, `paper/mpda/main.tex` line 52 |
| Zenodo build archive (separate record) | 10.5281/zenodo.22647933, published 2026-09-07, 13 files, 6.24 GB | every input no script can regenerate (section 3.13) | [MEM] `zenodo-deposit.md`; [CTSP] `docs/BUILD_CHAIN.md` |
| Hugging Face mirror | `OpenSpineConsortium/CTSpinoPelvic1K` | labels (v10 on 2026-09-27) and the CT volumes; CT 0533 replaced 2026-09-23 | [MEM] `hf-mirror-is-v10.md`, `grid-ct-0533-truncated.md` |
| anonymous review copies | `anonymous-mlhc/CTSpinoPelvic1K`, `anonymous-neurips-ED/CTSpinoPelvic1K` | MLHC and NeurIPS anonymous releases | [CTSP] `README.md` quickstart; `docs/RELEASE_CHECKLIST.md` "v8" |
| older working dataset | `gregoryschwingmdphd/CTSpinoPelvic1K` branch `v2` | v2 tree and review crops | [MEM] `review-space-repos.md` |
| pelvic pseudolabeller checkpoints | `OpenSpineConsortium/spinopelvic-seg-checkpoints` (also `anonymous-neurips-ED/…`, `anonymous-mlhc/…`) | 5-fold Dataset803 nnU-Net | [CTSP] `results/pseudolabel_dice/README.md`; [SEG] `README.md` |
| grid | `~/data/CTSpinoPelvic1K/{labels,labels_v10,ct,manifest.json,dataset_labels.json,SHA256SUMS.txt,labels.zip}` | the release; labels.zip rebuilt with 803 entries | commit `73cc398` message |

The CT volumes are not in the Zenodo label versions: they are rebuilt from TCIA by
`zenodo/reconstruct_ct.py` and `zenodo/fetch_from_tcia.py` using the SeriesInstanceUID in
`manifest.json`, or downloaded ready-made from the Hugging Face mirror ([CTSP]
`docs/BUILD_CHAIN.md` "What was deliberately not archived"; `zenodo/README.md`).

---

## 3. The dataset build

### 3.1 Sources, and why a crosswalk was needed

- **Three sources**: TCIA CT COLONOGRAPHY (DICOM, CC BY 3.0, doi 10.7937/K9/TCIA.2015.NWTESAY1),
  CTSpine1K COLONOG fold (vertebral masks, Hugging Face `alexanderdann/CTSpine1K`, gated,
  CC BY-NC-SA 4.0), CTPelvic1K dataset 2 (pelvic masks, Zenodo record 4588403, CC BY 4.0)
  ([CTSP] `docs/BUILD_CHAIN.md` "Sources, cited"; `README.md` "License").
- **The licence of the release is CC BY-NC-SA 4.0 because CTSpine1K is ShareAlike**; code is
  Apache-2.0 ([CTSP] `README.md` "License").
- COLONOG is the only collection common to both annotation sets (CTSpine1K 1,005 volumes from
  four collections; CTPelvic1K 1,184 from seven). Each COLONOG patient was scanned prone and
  supine, 12 exceptions among the 825 patients ([CTSP] `paper/mpda/main.tex` Sources section).
- **CTSpine1K's selection script never selected anything**: `dicom2nii.py` (deleted in commit
  bcd8f47, recoverable at
  `https://raw.githubusercontent.com/MIRACLE-Center/CTSpine1K/7f44959/dicom2nii.py`) writes every
  series to the same filename, so the retained series is whichever the directory walk reached
  last ([MEM] `ctspine1k-selection-code-deleted.md`; [CTSP] `paper/mpda/main.tex` Sources).
- CTSpine1K `Path.csv` names no position for 217 of 782 annotated records and for seven points
  at an acquisition other than the one the mask overlaps best; CTPelvic1K encodes the mapping in
  mask filenames (`dataset2_PatientID_SeriesNumber_undocumented_[tag_]mask_4label.nii.gz`); of
  714 masks, one names a patient with no archived series; 702 of 713 resolve to the series chosen
  by bone overlap ([CTSP] `paper/mpda/main.tex` Sources). Checks:
  `morphometrics/ctspine1k_pathcsv_agreement.csv` (782 rows, from
  `scripts/compare_ctspine1k_pathcsv.py`), `scripts/compare_ctpelvic1k_naming.py`.
- **The crosswalk method**: threshold each of the patient's volumes at bone attenuation and keep
  the series the mask overlaps most ([CTSP] `paper/mpda/main.tex` Sources; `scripts/build_db.py`,
  `scripts/place_fused_masks.py`, `scripts/apply_manual_flips.py` with `configs/flip_list.json`,
  per `docs/BUILD_CHAIN.md` steps 2-3). Masks carry no SeriesInstanceUID, which
  `make verify-mask-seriesuid` confirms ([CTSP] `Makefile`).
- **Result**: 342 fused (spine and pelvis on one series), 351 separate (different series of one
  patient), 89 spine only, 20 pelvis only = 802 ([CTSP] `paper/mpda/main.tex` Fig. 1 TikZ and
  Sources). The released records: 422 supine, 377 prone, three decubitus; 562 at 1.0 mm, 232 at
  1.25 mm, eight other ([CTSP] `paper/mpda/main.tex` Sources).
- **Source ground-truth corrections**: 112 spine corrections in 103 cases, 13 pelvic in 12
  ([CTSP] `paper/mpda/main.tex` Fig. 1; `docs/CORRECTIONS.md`). See contradiction C9: every row
  in `docs/CORRECTIONS.md` still reads "pending (in review)".
- The older stage-by-stage pipeline (download → database and placement → export) is in
  [CTSP] `docs/pipeline.md` (dated 2026-04-18) and `Makefile` targets `download-raw`,
  `create-dataset`, `hf-stage`, `hf-push`.

### 3.2 Densification (pseudolabelling the missing half)

- A five-fold nnU-Net v2 model (Dataset803, trainer `nnUNetTrainerWandB_500ep_LSTVOversample`,
  plans `nnUNetResEncUNetPlans_100G`, `3d_fullres`) was trained on fused, spine-only and
  pelvis-only masks together using nnU-Net's `ignore` label, and completed the missing pelvis on
  440 records (351 separate + 89 spine-only) out of fold, so no record was completed by a model
  that saw it ([CTSP] `results/pseudolabel_dice/README.md`; `paper/mpda/main.tex` Densification).
- **Held-out fold Dice against manual CTPelvic1K labels**: sacrum 0.980 ± 0.003 (no fold below
  0.977), left hip 0.970 ± 0.016, right hip 0.971 ± 0.015 (no fold below 0.953). These are
  nnU-Net's patch-based online validation Dice read out of the five `checkpoint_best.pth` files by
  `scripts/extract_pseudolabel_dice.py`, because no `validation/summary.json` was uploaded, the
  grid logs were truncated, and `scripts/eval_vs_manual.py` was written but never run ([CTSP]
  `results/pseudolabel_dice/README.md`, `dataset803_fold_validation_dice*.csv`). Feeds MPDA
  Table S1.
- The 20 pelvis-only records got a hand-corrected pseudo-spine, because a pseudolabelled spine
  must commit to a count ([CTSP] `paper/mpda/main.tex` Densification).
- A rigid cross-registration of each pelvic mask onto the other acquisition was tried and
  "found wanting" ([CTSP] `paper/mpda/main.tex` Densification; `Makefile` target
  `propagate-pelvis`).
- Training code: [SEG] (section 12). The models were trained 3 May 2026 from a working tree at
  [SSN] commit 50b209f ([CTSP] `CAMERA_READY_NEURIPS/src/checklist.tex` item 5 justification).

### 3.3 Version history

| version | what changed | script (step in `docs/BUILD_CHAIN.md`) | DOI |
|---|---|---|---|
| v1 | partial-annotation release, all configs, `ignore` protocol; the pseudolabeller's training input; finalized 25 Apr 2026 as the "April release" (1,153 records over 802 patients) | `scripts/export_hf.py` (step 4) | HF only |
| v2 | dense: CTSpine1K spine + pelvis (real where fused, pseudolabelled on spine-only); `pelvic_native` dropped | `scripts/export_hf.py`, `scripts/pseudolabel.py` (step 4) | HF only |
| v3 | femora (TotalSegmentator), GT thoracic column, carved S1 (29), VerSe-native ids | `scripts/build_v3_totalseg.py`, `slurm/ship_v3.sh` (step 5) | HF only |
| v4 | per-level ribs (Möller binary rib net + TotalSegmentator numbering) | `scripts/build_v4_ribs.py`, `slurm/ship_v4.sh` (step 6) | HF only |
| v5 | student review merged; lumbar ribs as own class (then 74/75); speckle strip; rib offset fixes | `scripts/build_final_dataset.py`, `slurm/build_v5.sh`, `slurm/finalize_v5.sh` (step 8) | HF only |
| v6 | surgical hardware (11 records, radiologist-read); 22 hip-laterality corrections; five hand-corrected records | `scripts/build_v6.py`, `relabel_hips_by_midline.py`, `fix_hip_sidedness.py` (step 9) | 22139643 |
| v7 | S1 re-carved; manifest counts recomputed from volumes | `scripts/recarve_s1_all.py` (step 10) | 22242745 |
| v8 | two-reader Castellvi consensus in the manifest; soft-tissue names 58-73 retired | `scripts/apply_castellvi_consensus.py`, `zenodo/new_version.py` (step 11) | 22293878 (2026-09-04) |
| v9 | contiguous ids 0-66, sentinel removed, record 0016 reference row removed | `scripts/renumber_labels.py --map v9` (step 12) | 22639598 |
| v10 | thirteen ribs per side (34-46, 47-59), lumbar ribs 60/61, hardware 62-68 | `scripts/renumber_labels.py --map v10`, `zenodo/finalize_v9.py` (step 13) | 22642578 (2026-09-07) |
| v11 | id 29 (carved S1) dissolved back into 26; 29 retired, nothing renumbered | `scripts/merge_s1_into_sacrum.py` (brought into the repo from grid `~/s1v11` on 2026-09-16) | 22797014 |

Sources: [CTSP] `docs/BUILD_CHAIN.md`; `zenodo/README.md` "Version history" (stops at v10);
`README.md` "Versions"; commit `73cc398`; [CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`
"Version note". [CTSP] `docs/VERSION_PROGRESSION.md` measures v2/v3/v5pre/v5 with identical checks
(`scripts/qc_version_progression.py`, `qc_final/version_progression.csv`): fragmented labels
366 → 1,146 (v3, ribs arrive) → 377; rib offset 10.83% → 7.69% (a version-comparison metric only,
not comparable to the release 0.035%).

**How to make a new Zenodo version** ([MEM] `zenodo-deposit.md`):
`scripts/renumber_labels.py --map vN` → `zenodo/finalize_v9.py --new labels_vN --old labels_vM_old --max-id 68`
→ `python3 zenodo/new_version.py --record <latest> --version vN --dir data/zenodo_deposit --replace <files>`
→ `python3 zenodo/upload.py --publish <id>`; then update `\datasetversion` and the DOI in
`paper/mpda/main.tex`, `title_page.tex`, `cover_letter.md`; mirror with `hf/push_v9.py`. Token at
`~/.zenodo_token` in WSL (not read here).

### 3.4 The carved S1 and its withdrawal (v3 → v7 → v11)

- **What it was**: id 29 = (GT sacrum) ∩ (TotalSegmentator `vertebrae_S1`), split along the
  sacrum's principal axis, cranial slab relabelled; re-carved in v7 ([CTSP] `README.md` "Bone
  augmentation"; `docs/BUILD_CHAIN.md` step 10).
- **Audit** (`scripts/audit_s1_carve.py`, output `morphometrics/s1_carve_audit.csv`, 802 rows):
  median craniocaudal extent 57.6 mm where a first sacral segment is near 30; 221 of 801 records
  have S1 over half the sacrum, 580 in the 0.15-0.50 range (my recount of the CSV; commit
  `2232bde` says "only 26% of records fall in a defensible range, and 222 take more than half";
  CLAUDE.md says 222). Where it failed, the plane ran nearly parallel to the sacral long axis and
  shaved the ventral cortex, so the retained sacrum lost its anterior wall. Worked example
  [CTSP] `docs/qc/s1_carve_0428_vs_0704.png`. Found by rendering, not by a statistic (commit
  `2232bde`).
- **Effect on the angles**: on the 580 sound carves PI 52.7 / PT 19.6 (against Hasegawa 53.4 /
  19.2); on the 221 degenerate ones PI 68.5 / PT 33.6; the plate gate fired on 96% of the second
  group and 4% of the first (commit `2232bde`; acceptance test
  `scripts/compare_v10_v11_spinopelvic.py`).
- **v11**: `scripts/merge_s1_into_sacrum.py --src data/zenodo_deposit/labels --dst data/v11_labels --write`
  relabels 29 → 26 in the stored orientation; 155,093,558 voxels returned to the sacrum on 801 of
  802 records (1000 never had an S1); verified by `scripts/check_s1_merge.py` ([CTSP]
  `scripts/merge_s1_into_sacrum.py` docstring; [MEM] `s1-carve-changed-spinopelvic.md`).
- **29 is retired, not reused**, because closing the gap would rename hips, femora and all 26 rib
  ids under which checkpoints, benchmark, ostk detection and level tables are keyed
  (`scripts/label_scheme.py` lines 42-56, `verify()` lines 145-173 asserts `range(0,69)` minus
  29; `label_dict()` has no "S1" key so a stale caller gets KeyError).
- **A check on a withdrawn label is not inert**: `scripts/select_anchor_cases.py` kept gating
  Figure 2's case choice on carve plausibility against a stale tree that still had 29, rejected
  0428 and swapped 0172 into panel (b) while the caption still named 0428 ([CTSP] `CLAUDE.md`;
  [MEM] `s1-carve-changed-spinopelvic.md`).
- **What must be recomputed from v11**: anything touching the sacrum, the lumbosacral disc or the
  pelvis; anything purely vertebral is unchanged, and `level_gradients.csv` regenerates
  bit-for-bit identical ([CTSP] `CLAUDE.md`). Which CSVs were actually recomputed on v11 is in
  section 4.1; several were not.
- TotalSegmentator v2's own `sacrum` excludes S1 (separate disjoint class `vertebrae_S1` on all
  1,228 TS subjects); the whole sacrum is the union ([MEM] `ts-sacrum-excludes-s1.md`). The
  NeurIPS camera-ready's headline "TS sacrum 0.817" counts TS's S1 class as a miss (open item 21
  in [CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`).

### 3.5 Label schemes

**v11 (the release, VerSe-native)** ([CTSP] `scripts/label_scheme.py`, single source of truth;
mirrored in the release's `dataset_labels.json`; [MEM] `scheme-bone-hardware-only.md`):
C1-C7 = 1-7, T1-T12 = 8-19, L1-L5 = 20-24, L6 = 25, sacrum = 26 (entire), coccyx = 27, T13 = 28,
**29 retired**, left/right hip = 30/31, femur left/right = 32/33, rib_left_1..13 = 34-46,
rib_right_1..13 = 47-59 (rib 13 = true rib of a T13, empty in this release), lumbar rib
left/right = 60/61, hardware 62 generic, 63 cage, 64 screw-rod, 65 plate, 66 arthroplasty,
67 SI screw, 68 osteosynthesis. Earlier eras used ribs 34-57, soft tissue 58-73 (reserved, never
populated, retired 2026-09-03), lumbar ribs 74/75, hardware 76-82, ignore 255 ([CTSP]
`docs/BUILD_CHAIN.md` last paragraph of the chain section; `scripts/label_scheme.py`
`OLD_TO_NEW_V9`, `OLD_TO_NEW_V10`).

**The legacy ostk map ("v4")**: L1 = 1 … L6 = 6, S1 = 7, sacrum = 8, hips 9/10, femurs 11/12,
T1-T13 = 13-25, ribs from 26, ignore 50 ([OSTK] `ostk/labels.py` `LABELS_V4`; [OSTK] `SPEC.md`
section 1; [MEM] `label-scheme-v4-vs-ostk.md`). The PACS demo cases use it ([MEM]
`label-scheme-v4-vs-ostk.md`).

**Why it matters**: resolving a name against the wrong map returns a finite wrong answer
("femur_left" → T4, "S1" → C7). Pelvic incidence was computed for the whole release against the
legacy map once; the only symptom was a `low_voxels:S1` flag on every case ([CTSP] `CLAUDE.md`;
`docs/SPINOPELVIC_ESTIMATOR.md` section 1). **Rule**: call `ostk.labels.labels_for(volume)`,
which detects the scheme from pelvis voxel mass under each hypothesis and raises `SchemeError`
when ambiguous ([OSTK] `ostk/labels.py` lines 97-140; tests `tests/test_labels.py`).

**Other identifier traps**:
- Case ids are zero-padded in the release (`0001`) and unpadded in old CSVs (`1`): `zfill(4)`
  before diffing ([CTSP] `CLAUDE.md`).
- **Token ≠ release id**: release 0145 = token 100; 34 of 802 tokens are `CTC-<10 digits>`, so
  match `[A-Za-z0-9-]+`, not `\d+` ([SSN] `docs/PATIENT_IDENTITY_SPEC.md` line 119).
- Rib bases were once hard-coded; the right block base is 45 where the left reserves 12 slots and
  46 where it reserves 13; the wrong constant changed `rib12_to_crest_mm` in 237 of 802 records,
  worst 36 mm; now read per worker from `dataset_labels.json` ([CTSP] `docs/LEVEL_MORPHOMETRY.md`
  "Still open").
- Volumes are stored ('P','I','R'); canonicalise to RAS to analyse, never to write; read
  `nib.aff2axcodes` for any direction check ([MEM] `ct-volumes-are-pir-not-ras.md`,
  `never-reorient-when-writing-labels.md`). The bug signature is a script containing both
  `as_closest_canonical` and `nib.save`.

### 3.6 Ribs

- **Why two segmenters**: Möller's binary rib net is good when the whole rib is in the field and
  fails on partly visible ribs; TotalSegmentator numbers ribs and handles partial ribs but stops
  short of the costovertebral joint. The union is the pseudolabel ([CTSP] `paper/mpda/main.tex`
  Ribs).
- **Build rule ("trust TS")**: keep TotalSegmentator's per-level numbering verbatim and graft only
  Möller voxels whose union component touches a TS rib; drop Möller-only components (bowel false
  positives); `_drop_same_id_strays` drops far, isolated, small same-id pieces (FAR_STRAY_MM 45,
  under 5,000 voxels) ([MEM] `rib-approach-ts-trust.md`; [CTSP] `scripts/build_v4_ribs.py`).
- **Auto-engulf of halo voxels only after student correction**, never on raw pseudolabels
  (Greg, emphatic, 2026-07-04) ([MEM] `rib-auto-engulf-post-correction-only.md`).
- **Triage rule** (reproducible from labels alone): `scripts/qc_v4_ribs_and_verts.py` flags a
  case iff rib label-mixing OR rib-spine detachment → `rib_worklist.json` = 152 cases (supersedes
  `scripts/qc_v4_ribs.py`) ([MEM] `canonical-rib-triage.md`).
- **Review outcome**: all 152 corrected, 149 finalised by a second read; the three not finalised
  are token 46 (case 0068), 61 (0090), 518 (0730) ([CTSP] `results/rib_qc_v4_vs_release/README.md`,
  checked against ledger `anonymous-mlhc/CTSpinoPelvic1K-reviews-ribs` on 2026-09-14). An earlier
  "148 of 152" was an artefact of a stale worklist copy.
- **Rib QC, pseudolabel vs release, same code** (grid job 40220664, 2026-09-13;
  `results/rib_qc_v4_vs_release/rib_qc_stages.py`, `remap_v4.py`, `scripts/review_anatomy_qc.py`,
  `scripts/qc_rib_vertebra_incidence.py`, `scripts/rib_fragments_detail.py`): two numbers on one
  bone 151/584 → 0/0; detached 37/40 → 0/0; split inside the field 119/280 → 6/7; offset 24/170 →
  0/2; no vertebra within reach 38 → 11; rib on a lumbar body 14/21 → 0/0. Feeds MPDA Table II
  ([CTSP] `paper/mpda/main.tex` `tab:ribqc`; `results/rib_qc_v4_vs_release/README.md`).
- **Release incidence**: 11,560 ribs, 5,796 skipped (own vertebra outside the field), 11 no
  contact, 5,753 evaluable, 5,751 match, 2 offset (0.035%), 0 misnumbered cases (misnumbered = 3+
  ribs offset by the same amount) ([CTSP] `results/rib_qc_v4_vs_release/incidence_release.json`;
  `paper/mpda/main.tex` Validation).
- **Split ribs at the field edge are not defects**: a second piece touching the reconstruction
  circle or a volume face is a rib that left and re-entered the field ([CTSP]
  `docs/RELEASE_CHECKLIST.md` 2.2b).
- **On rib reviews only rib-purity checks gate** (`rib_label_mixing`, `rib_spine_gap`);
  `structure_integrity` and `rib_vertebra_match` are advisory because the spine is force-restored
  and transitional anatomy legitimately shifts ribs ([MEM] `rib-qc-gates-never-block-lstv.md`).
- **Lumbar ribs (60/61)**: 16 records (13 bilateral, 3 right only), each on a vertebra the source
  named lumbar; class follows by rule ([CTSP] `paper/mpda/main.tex` Label scheme;
  `morphometrics/label_census_v11.csv` 60 → 13 records, 61 → 16). Case 0787 was the 15-versus-16
  disagreement between the released export and the grid working copy ([CTSP]
  `docs/VERSION_PROGRESSION.md`; `docs/RELEASE_CHECKLIST.md`); the current article and census say 16.
- **Stump twelfth ribs**: lowest-rib length ratio below 0.33 in 98 of 789 records with a
  measurable pair (12.4%) ([CTSP] `paper/mpda/main.tex` Descriptive Analysis; confirmed by my
  recount of `morphometrics/transition_morphometrics.csv` column `rib12_11_ratio_min`).
- **Rib numbers above the lowest rib are an inference** where the upper thorax is out of view
  ([CTSP] `zenodo/KNOWN_ISSUES.md` section 7).

### 3.7 Surgical hardware (v6)

- Candidates from a 2,500 HU threshold in a shell around the labelled skeleton; every candidate
  read by a radiologist; 52 detections → 11 kept, 41 rejected; kept ≥ 2,586 mm³, rejected
  ≤ 1,768 mm³ (0317); 0878 rejected (11,798 HU, above the 3,071 HU reconstruction ceiling)
  ([CTSP] `zenodo/KNOWN_ISSUES.md` section 8; `paper/mpda/main.tex` Surgical hardware).
- 11 records: eight arthroplasties, one osteosynthesis, one SI fixation, one interbody-cage pair
  (0068); 1,538,852 voxels reclaimed from bone labels; in eight records the femoral head used for
  PI/PT is an implant (0188, 0443, 0485, 0515, 0671, 0974, 1003, 1128) ([CTSP] `zenodo/KNOWN_ISSUES.md`
  section 3; `paper/mpda/main.tex`). Classes: [CTSP] `docs/HARDWARE_CLASSES.md`. Scripts:
  `scripts/detect_metal.py`, `scan_hardware.py`, `classify_instrumentation.py`,
  `apply_hardware_class.py`, `scripts/build_v6.py`; census `morphometrics/metal.csv` (9 records
  `has_metal=1`; it misses 0068 by design, commit `d5b7d2a`).
- 0068: instrumented L5-L6, six lumbar bodies, pseudolabelled spine; deferred, then resolved
  2026-08-26 by hand ([CTSP] `docs/DEFERRED_CASES.md`).

### 3.8 Castellvi grades

- 33 records with a lumbar count other than five, or a source transitional flag, carry a grade
  ([CTSP] `paper/mpda/main.tex` Castellvi typing). Two radiology residents (Nizar Alnabahneh =
  read 1, Miraziz Ismoilov = read 2, per column names `read_1_NA`, `read_2_MI` and the author
  list in `main.tex`) graded all 33 independently in September 2026 (reads dated 2026-09-04,
  [CTSP] `docs/castellvi_readers_2026-09-04.csv`); six disagreements resolved by consensus; five
  crossed II/III, one I/II ([CTSP] `docs/castellvi_consensus.csv`, 34 rows incl. 0016 which is
  graded "0" and excluded; commit `70de829`).
- **Consensus distribution**: IIIb 16, IIb 6, IV 4, IIa 4, Ib 2, IIIa 1 ([CTSP]
  `docs/castellvi_consensus.csv`; `zenodo/KNOWN_ISSUES.md` section 1). κ 0.737 (0.553-0.920) full,
  0.696 type only ([CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` row 19).
- **Stale files carrying other distributions** (see contradiction C5):
  `morphometrics/castellvi_grades.csv` (2026-08-23: IIIb 18, IV 4, IIb 4, IIIa 3, IIa 2, Ib 2),
  `zenodo/README.md` (v10 text), `Lumbosac.csv` (39 cases, older), and the May 2026 one-column sheet
  `<laptop:Desktop>/NeurIPS/Lumbosac_Castelvii_Class.csv` (IIIb 19) used in the NeurIPS review version.
- `null` Castellvi means ungraded, not normal: 769 of 802 are ungraded ([CTSP]
  `zenodo/KNOWN_ISSUES.md` section 1).
- No senior neuroradiologist adjudication was done; it was planned ([MEM]
  `publication-roadmap.md` update 2026-07-24; [CTSP] `docs/RELEASE_CHECKLIST.md` "Still open").

### 3.9 Manifest fields and their known defects

- Fields: [CTSP] `README.md` "File format" (`token, config, match_type, position, ct_file,
  label_file, lstv_*, has_l6, n_lumbar_labels, spine_series_uid, pelvic_series_uid, …`);
  completeness per field in MPDA Table S2 (hand-written from the manifest, [CTSP]
  `paper/mpda/audit_artifacts.py` "Table V completeness").
- `has_l6`, `n_lumbar_labels`, `has_lumbar_rib`, `lumbar_rib_side` were wrong and were recomputed
  from the volumes on 2026-08-23 (has_l6 17 true where it was 1; n_lumbar_labels 776 five / 17
  six / 9 four) ([CTSP] `docs/RELEASE_CHECKLIST.md` "Closed 2026-08-23"). The current census has
  18 L6 records (`morphometrics/label_census_v11.csv`).
- **`spine_bone_pct` is measured over vertebra ids only**; nothing says so ([MEM]
  `grid-ct-0533-truncated.md`).
- **`n_voxels_fg` is broken** (0 in 340 of 802) ([MEM] `grid-ct-0533-truncated.md`).
- `lstv_label` inherits from `lstv_pelvic`, parsed from the CTPelvic1K mask filename; this is a
  human annotation, unrelated to `prov_pelvis: pseudo` ([CTSP] `docs/LAB_JOURNAL.md` "Where the
  label sources come from").
- Nine four-lumbar records (0094, 0151, 0156, 0158, 0760, 0785, 0787, 0875, 1031) carry no L5; all
  Castellvi IIIb; the fused segment is labelled with the sacrum ([CTSP] `zenodo/KNOWN_ISSUES.md`
  section 2, written for v10 when that segment was id 29; in v11 it is part of 26).

### 3.10 Splits

- `scripts/generate_5fold_splits.py` splits at patient-token level (all of a patient's records
  in one fold) and stratifies only by the six-way LSTV subtype; it does not use config or
  match_type ([MEM] `splits-*-v3-resplit.md` (the "Splits & v3 resplit" note)).
- Shipped file `splits_5fold.json` (schema v4 per README; canonical copy schema v6 on the grid at
  `~/CTSpinoPelvic1K/data/hf_export/splits_5fold.json`; md5 860207a7…, same in v10 and v11). Five
  disjoint folds, **no held-out test set** ([CTSP] `paper/mpda/main.tex` Data Format; [MEM]
  `splits-*-v3-resplit.md` (the "Splits & v3 resplit" note)).
- **The splitter never read the lumbar count**: strata are lumbarization 15 / sacralization 15 /
  semi-sacralization 2 / ambiguous 2 / normal 768; record 0500 sits in lumbarization on a phantom
  L6 (its label has L1-L5 and no 25); one real L6 record sits in normal; why the splitter saw an
  L6 on 0500 is not known ([CTSP] `paper/mpda/main.tex` Data Format; [MEM]
  `splits-*-v3-resplit.md` (the "Splits & v3 resplit" note)). A resplit must fix the attribute read first, and it
  changes the folds every trained model used.
- The NeurIPS paper's numbers use a different, record-level split of the April release (805
  train / 174 validation / 174 test manifests; 979-record pool) ([CTSP]
  `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` rows 14-23).

### 3.11 The identity audit (who is the same person)

- 2026-09-22, 56 agents, adversarially verified; spec [SSN] `docs/PATIENT_IDENTITY_SPEC.md`
  ([MEM] `identity-audit-findings.md`).
- **CTSP prone/supine duplication ruled out on disk**: zero shared (origin, spacing, direction,
  nz) signatures over 1,728 acquisitions; TCIA lists 825 PatientIds and `patient_db.json` holds
  exactly those; `manifest.json` `volume_id → token` (token = tail of the DICOM PatientID) is the
  identity; one release id = one person, verified 802/802 by two routes ([SSN]
  `docs/PATIENT_IDENTITY_SPEC.md` line 119).
- **Residual unknown**: whether the 768 numeric-id records and the 34 `CTC-` records (which
  entered via the CTSpine1K subset) overlap as humans; settled only by a TCIA query ([SSN]
  `docs/PATIENT_IDENTITY_SPEC.md` lines 171-181).
- **Leak found in a derived bank** (SchwingNet side, pointer only): `anchor_drr` seeded implant
  variants separately from their clean renders, so 301 of 801 CTSP people are on both sides of
  its own split; `anchor_det_v1` was trained on it ([MEM] `identity-audit-findings.md`). Token
  map file `tools/identity/ctsp_token_map.json` in [SSN].

### 3.12 Known data defects

| defect | state | source |
|---|---|---|
| CT 0533 truncated (16.5 MiB, sha 20e673dc…) on the grid and on Hugging Face | repaired 2026-09-23 (job 40416624, `slurm/ctsp0533_repair.sh`, 250,067,995 B, sha 478a74e9…); HF replaced (job 40419665); KNOWN_ISSUES section 10 and the Zenodo note not yet pushed; banks built before 2026-09-23 03:03 EDT hold 801 | [MEM] `grid-ct-0533-truncated.md` |
| 16 records with no thoracic vertebra labelled (0033 0068 0167 0241 0344 0357 0383 0389 0409 0424 0428 0696 0720 0730 1004 1106) | listed 2026-08-19; later state not recorded (the census shows T12 in 801 of 802) | [CTSP] `docs/LAB_JOURNAL.md`; `morphometrics/label_census_v11.csv` |
| top labelled vertebra cut by the field in 553 of 802 records | documented, deliberate | [CTSP] `zenodo/KNOWN_ISSUES.md` section 6 |
| 27,738 detached label pieces in 741 records; 518 of ≥1,000 voxels in 359 records | documented | [CTSP] `zenodo/KNOWN_ISSUES.md` section 5 |
| thoracic GT field-limited (~T8 down, not T1) | documented | [MEM] `thoracic-gt-fov-limited.md`; `morphometrics/label_census_v11.csv` |
| six `pelvic_native` cases never reviewed (0090, 0196, 0236, 0419, 0877, 1037) | listed in the checklist; later state not recorded | [CTSP] `docs/RELEASE_CHECKLIST.md` section 1 |
| 0172 source "normal" but five sacral foramina and a rib on "L1" | in the radiologist re-read queue | [MEM] `lstv-reread-queue.md`; [CTSP] `docs/lstv_reread_queue.csv` |
| largest-component post-processing deletes the loose lamina of a spondylolytic vertebra (case 155__fused) | recorded finding, not in code | [MEM] `spondylolysis-and-border-anomaly-findings.md` |

### 3.13 Rebuilding the release from the published sources

[CTSP] `docs/BUILD_CHAIN.md` is the recipe for v10 (13 steps, script, input, output, archive
component). Model outputs (TotalSegmentator, Möller ribs, spinopelvic-seg pseudolabels) are
archived rather than re-run because they are not bit-reproducible; human work (student
corrections, radiologist hardware reads, hand-corrected records, Castellvi grades) is archived in
full; `CHAIN_CHECK_v7_to_v10.txt` shows steps 12-13 regenerate all 802 published volumes voxel for
voxel ([MEM] `zenodo-deposit.md`). Code state tagged `v10-build-archive`. v11 is one more
deterministic step (`scripts/merge_s1_into_sacrum.py`) on the v10 volumes.

---

## 4. Morphometrics and spinopelvic measurements

### 4.1 The seven extractors

All take `--labels`, `--manifest`, `--workers`, `--out`; the three CT ones take `--ct`. Each
checks its output against physiological envelopes and **exits non-zero when a measure is
outside, while still writing a good CSV** — read the `*** N measure(s) outside the plausible
range` line before assuming a crash ([CTSP] `paper/mpda/REPRODUCE.md` section 1).

| script | CSV in `morphometrics/` | measures | last regenerated (commit) | label tree used | notes |
|---|---|---|---|---|---|
| `scripts/extract_level_gradients.py` | `level_gradients.csv` (802 rows) | per-level body height (ant/post), end-plate width, canal width, transverse-process span, wedge ratio, canal depth | `47e72d0` 2026-09-10 | v10 release; identical bit-for-bit to v5_final | vertebral only, unaffected by v11 |
| `scripts/extract_surgical_morphometrics.py` | `surgical_morphometrics.csv` (802 rows) | PI, SS, PT, supine LL, PI−LL, crest above L4-5, lowest rib to crest, pedicle widths, canal AP, wedge, Torg ratio, sacral width/height, plate gate columns | `2232bde` 2026-09-11 | whole-sacrum plate (the v11 geometry) | feeds MPDA Table III and Fig. S2; 1,027 lines |
| `scripts/extract_pelvic_shape.py` | `pelvic_shape.csv` | bi-iliac, bi-acetabular, inlet AP, sacral base width, sacral span | `47e72d0` 2026-09-10 | v10 (S1 = 29 present) | sacrum-adjacent; recompute on v11 not recorded |
| `scripts/extract_transition_morphometrics.py` | `transition_morphometrics.csv` | sacral foramina, rib-free count, Castellvi proxies (TP span, gap to ala/ilium), disc ratio, rib 12/11 ratio, sacrum height/width | `47e72d0` 2026-09-10 | v10 | sacrum-adjacent; recompute on v11 not recorded; drives Figure 2 case choice |
| `scripts/extract_degenerative.py` (CT) | `degenerative.csv` | disc height, vacuum, bridging/DISH, osteophyte index | `b40afa2` 2026-09-10 | not recorded (pre-v11) | L5-S1 disc height touches the sacrum; 631 records have it |
| `scripts/extract_opportunistic.py` (CT) | `opportunistic.csv` | L1-L4 trabecular HU (psoas and aortic calcification described in the docstring but not columns in the CSV) | `4614717` 2026-09-10 | not recorded | L1 median 157.2 HU, n 801 (my recount) |
| `scripts/extract_proximal_femur.py` (CT) | `proximal_femur.csv` | head diameter, neck-shaft angle, hip axis length, neck HU, sphere-fit QC | `fa612c9` 2026-09-09 | not recorded | needs ~220 GB RAM at 8 workers; killed at 110 GB |

Commands: [CTSP] `paper/mpda/REPRODUCE.md` section 1. Resources: label-only extractors 15-30 min at
20 workers; CT ones hours (same file). Batch wrappers exist in [CTSP] `slurm/`
(`level_gradients.sh`, `morphometrics.sh`, `pelvic_shape.sh`, `degenerative.sh`,
`opportunistic.sh`, `proximal_femur.sh`, `finalize_release.sh`) but they point at `data/v5_final`
and use `-q primary` (see contradiction C11). Other per-case outputs: `tp_height.csv`
(`scripts/measure_tp_height.py`, speckle fix moved 169 values, commit `7669ae9`), `sacral_ala.csv`
(failed on the full cohort, commit `aa5fd70`), `ostk_level_morphometry.csv` (section 4.7),
`s1_carve_audit.csv` (section 3.4).

**Release gates run before measurements and stop the chain** ([CTSP] `slurm/finalize_release.sh`;
`docs/RELEASE_CHECKLIST.md` section 0): `scripts/check_release_invariants.py` (geometry, ids,
emptiness, sidedness per sided pair, read through the affine; 802/802 pass) →
`scripts/qc_rib_vertebra_incidence.py` → extractors. Reason: on 2026-08-20 PI came back 154.6°
and SS 82.9° for all 802 records and the run exited zero.
`scripts/qc_physiological_envelope.py` flags individual values outside anatomy without deleting
them ([CTSP] `docs/RELEASE_CHECKLIST.md` 2.0).

### 4.2 Reference values

- `morphometrics/make_reference_table.py` holds every published series as literals with its
  citation and writes `morphometrics/level_references.csv` (365 data rows); `pedicle_width_references.csv`
  is maintained by hand (84 rows); `panjabi_reference.csv` (76 rows) ([CTSP] `paper/mpda/REPRODUCE.md`
  section 2; row counts from `wc -l`).
- **Panjabi 1991 page 892 (Table 3)**: missing from every scan obtainable; values were first
  digitised from Figure 4A by `paper/mpda/tools/digitize_panjabi_fig4a.py`; **resolved
  2026-09-13** when a complete copy arrived by interlibrary loan
  ([CTSP] `PANJABI_1991_FULL_fixed.pdf`, p. 892 = PDF page 7, image only); Table 3 values EPWu
  T11 34.9 ± 0.97, T12 39.0 ± 0.58; VBHp T11 21.3 ± 0.71, T12 22.7 ± 1.04 are now in
  `make_reference_table.py` (commit `83f7f95`; [MEM] `panjabi-1991-page-892.md`). REPRODUCE.md
  section 2 still describes the digitised dependency (contradiction C2).
- The multi-series comparison (5-18 series per quantity, disagreeing 21-69%) is held back for the
  next paper; `make_levelatlas_fig.py` keeps the drawing path behind
  `DRAW_SERIES = {"Panjabi 1992", "Panjabi"}` ([CTSP] `docs/NEXT_PAPER_REFERENCES.md`).
- What each measurement is and what caught each first wrong answer (PI 154.6°, SS 82.9°, L1 HU
  264, disc height 4-6 mm, TP gap measuring the facet joint, femoral head 34-37 mm): [CTSP]
  `docs/METHODS_REFERENCES.md`. DISH prevalence is withheld there.

### 4.3 The spinopelvic estimator: four defects, a fifth, and what is open

Read [CTSP] `docs/SPINOPELVIC_ESTIMATOR.md` in full; it predates v11 in its description of the
S1 branch. Summary:

1. **Label scheme assumed, not detected** — "S1" → id 7 (C7), "femur_left" → 11 (T4); fixed by
   `labels_for` (section 3.5).
2. **The S1 plate fitted two wrong ways** — without a carve, fitted to the whole sacrum (alae
   flatten it; median PI 54.7, 3.4% impossible); with the carve, latched onto the near-vertical
   promontory face (normal z 0.03-0.44, SS near 88° on 9.4%). ostk's corner method is wrong on
   the sacral base (sweeping `drop_post` gives SS 37.2, 37.2, 5.2, 3.8, 7.8, 7.2°); `S1`/`sacrum`
   now use the TLS surface fit with MAD trimming for orientation, the corner midpoint for the PI/PT
   anchor.
3. **Two wrong numbers that summed correctly** — the corner fit under-read SS by about 9° and LL by
   about 12° on every case while PI = SS + PT held. Caught only against outside references
   (extraction code SS 35.8°, Veilleux 2020 36.5°, ostk 24.8°). **An identity check cannot catch a
   consistent error in a shared landmark.**
4. **QC flags dropped for exactly the bad cases** — flags were attached only when a parameter came
   back `None`, so finite-but-impossible values arrived unflagged.
5. **(Section 5 of the document) Sacral slope reads 3.4° low, PT 4.0° high, PI 0.5° high against
   Veilleux** — the signature of a rotated vertical reference, but the anterior-pelvic-plane
   explanation fails on sign; the cohort explanation fits (Hasegawa 2018, older symptomatic supine
   CT: PI 53.4 / SS 34.1 / PT 19.2 against 52.6 / 33.1 / 19.6 here at that time). The decisive
   experiment (fit the APP from the hip labels, report aSS = SS − APPA) has not been done.

**The 128 low pelvic incidences — solved 2026-09-11**: the 60° tilt gate is blind to direction;
`_endplate` orients the normal by its superior component only, so a plane fitted to the ventral
sacral surface leans posteriorly at a normal angle. 39/39 records with PI ≤ 17 leaned posteriorly,
39/39 with PI > 35 anteriorly. Gate added: a normal with a non-positive anterior component is
rejected. Afterwards no record returns PI below 22.4 or PT below −15 (commit `028210a`;
`docs/SPINOPELVIC_ESTIMATOR.md` "Still open").

**Which estimator the release reports**: the extraction script's, not ostk's. Over the same 300
records: PI median 49.2 (extraction) vs 45.8 (ostk), outside plausible 6.3% vs 16.0%; ostk's S1
surface fit is bimodal (28.3% land on a steeper surface, PI near 18.6°) ([CTSP]
`docs/SPINOPELVIC_ESTIMATOR.md` "Which estimator…").

**What the v11 release computes** (whole-sacrum plate isolated by the lowest lumbar body's
footprint; a slab under the sacral apex was tried and is wrong because the apex is the
promontory) (commit `2232bde`): over 756 of 802 records, **PI 52.1 ± 11.1, SS 36.6 ± 10.6,
PT 15.5 ± 7.9, LL 51.7 ± 13.3, PI−LL 0.3 ± 10.3; medians PI 51.5, PT 15.0**; plate gate rejects 44
(1 with reason "normal leans posteriorly", reason blank on the other 43; [MEM] says 43 on tilt);
802 − 44 − 2 = 756. Veilleux 2020 (n=200) 52.1 / 36.5 / 15.6; Hasegawa 2018 (n=24) 53.4 / 34.1 /
19.2. I recomputed these from `morphometrics/surgical_morphometrics.csv` and they match MPDA
Table III ([CTSP] `paper/mpda/main.tex` `tab:spinopelvic`). Which two records fail besides the
44 is not recorded.

**Other fixes the S1 withdrawal forced** ([CTSP] `paper/mpda/REPRODUCE.md` "What changed and why"):
L5-S1 disc height lost 174 records because the sampling column sat at the median of pooled
voxels (now their overlap); the pelvic inlet measured none of the three published conjugates
(corrected: 131.4 mm women vs 125.4 men, a 6.5 mm dimorphism against a published 6.8; confirmed by
my recount of `pelvic_shape.csv` medians).

**Still open — two lists that do not match** (contradiction C3):
- [CTSP] `docs/SPINOPELVIC_ESTIMATOR.md` "Still open": eight records measure PI from a prosthetic
  femoral head; LSTV shifts PI by 10-15° depending on which end-plate is called S1 (stratified
  sensitivity analysis not done); no published head-to-head of S1 plane estimators, femoral-head
  centre estimators, or open PI/SS/PT-from-CT code; the anterior pelvic plane is not measured, so
  anatomical SS/PT cannot be reported. Also: the carve itself is not fixed; "a substructure label
  gives the sacral plate directly and is the planned revision".
- [CTSP] `paper/mpda/REPRODUCE.md` "Known-open": the 128 records (since solved), ostk pedicle width
  (better at L5, absent from the full run), canal-depth low tail (fixed), APP not measured; plus
  two worth-doing items: resample each vertebra into its own frame before slicing, and take
  end-plate width from the SPINEPS corpus label.
- [CTSP] `CLAUDE.md` says "four defects… and three that are still open". The best reading: the
  four are sections 1-4 above; the three open are the prosthetic heads, the LSTV sensitivity
  analysis, and the APP (the "no published head-to-head" bullet is a literature gap, not a defect).

### 4.4 Canal depth and end-plate width (both wrong, both fixed or withheld)

Read [CTSP] `docs/LEVEL_MORPHOMETRY.md`. Caught by **spread, not the median**: canal depth L3 SD
~3.9 against the widest published 2.45; end-plate width L5 SD ~8.7 against 5.54; 157 of 736
records under 11 mm at L3 (21%) against a Framingham prevalence of congenital stenosis of 2.62%;
95 of 760 L5 end-plate widths over 60 mm (walking from the 48.81 mm body width toward the
85.91 mm transverse-process span).

- **Canal depth**: three defects (first-closing slice instead of the pedicle plane; oblique
  sections falsely stenotic; maximum extent instead of a midsagittal chord). Rewrite in
  `scripts/extract_surgical_morphometrics.py` `_canal_column`, `_canal_ap`: close the ring with a
  2 mm disc only to find the hole; hole > 18 mm²; centroids within 8 mm of a robust axis, longest
  run; central half = pedicle slab; ±1.5 mm midsagittal strip, median over the slab. Effect over
  802: below-11 mm count 473 → 12; per-level SD T11-L4 1.55-4.37 → 1.55-2.04; L5 median 21.0 →
  17.4. Costs about 5% of levels (rejected, reported missing).
- **End-plate width at L5**: the canal cut keeps two lateral "shoulders" (pedicle and TP roots).
  Three fixes failed (voxel erosion, millimetre erosion, depth-per-column); a fourth (drop the
  posterior quarter, 90th percentile of row widths) was run over all 802 and lost on spread (table
  in the doc). **The shipped rule stays, bit-for-bit unchanged; L5 is withheld for end-plate and
  pedicle width** in `morphometrics/level_atlas.csv` and Figure 3; per-case CSVs keep raw L5.
  Rendering the mask settled what reasoning from numbers did not ([CTSP] `CLAUDE.md` "Render the
  mask").
- Open: obliquity correction only in ostk, not in the extraction script; SPINEPS corpus label
  (`scripts/spineps_ct_pipeline.py`) would remove the shoulders by construction; no published
  variance decomposition or per-case reject rule; Griffith et al. *Eur Radiol* 2022 (n=505
  abdominopelvic CT) is the best comparator and is paywalled — interlibrary request suggested.

### 4.5 Body height sits ~6 mm above Panjabi — it is the cohort

[CTSP] `docs/BODY_HEIGHT_INVESTIGATION.md`: estimator, tilt, millimetre scale and label dilation
each tested and excluded (`scripts/height_probe.py <labels> 80`, `scripts/edge_probe.py <ct> <labels> 40`,
`scripts/render_height.py`); the label edge sits 0.00 mm from where bone ends; what is left is 12
dried cadaveric spines against 802 living patients over 50.

### 4.6 Pedicle width

Figure 3(c) uses the extraction script's transverse pedicle width (mean of two sides). It tracks
13 published series except L5 (20.70 against 16.20; now withheld). ostk's implementation reads L5
15.10 mm on individual cases but produced pedicle columns for about two of ~5,600 level-instances
in the 2026-09-10 shard run; why is not established ([CTSP] `docs/SPINOPELVIC_ESTIMATOR.md`
"Pedicle width"). The committed `morphometrics/ostk_level_morphometry.csv` has `PDW` empty in all
4,744 rows (my count).

### 4.7 ostk against the extraction scripts

[CTSP] `docs/OSTK_VS_EXTRACTION.md`: over 802 records against Panjabi 1992, ostk is closer on
posterior body height at every level (L5 error +7.5 → +2.3 mm) and worse on every width (drifting
high toward L5, no TP-removal step). The figure keeps the scripts' values. Data
`morphometrics/ostk_level_morphometry.csv` (commit `90a27a7`, 2026-09-10, **before** the ostk
canal-closing regression); regenerate with `python -m ostk morph --labels <dir> --out morph.csv`.

### 4.8 Count-free and descriptive results (what the data show)

| result | number | file |
|---|---|---|
| T12 vs L1 separable on shape alone (patient-median-normalised features, logistic regression, case-grouped folds) | AUC 0.990, 97.3% over 1,485 vertebrae; thoracic vs lumbar AUC 0.998 | [CTSP] `scripts/test_morphometric_separability.py`; `paper/mpda/main.tex` Introduction; [AR] `REVISION_PLAN.md` section 3 |
| rib-free count | 744 five, 29 four, 28 six, 1 blank (current CSV); 734 / 35 / 26 on 2026-08-19 | `morphometrics/transition_morphometrics.csv`; [CTSP] `docs/LAB_JOURNAL.md` |
| lowest-rib ratio bimodal | modes near 0.68-0.69 and 0.32-0.33; 98/789 below 0.33 | [CTSP] `paper/mpda/main.tex`; `docs/LAB_JOURNAL.md`; `paper/mpda/PLAN.md` |
| stump and lumbar ribs vs a whole-spine CT series | 12.4% and 2.0% here against 12.6% and 1.5% (Nagata 2025) | [CTSP] `paper/mpda/main.tex` Descriptive Analysis |
| rib and lumbosacral anomalies co-occur | three different numbers exist, see contradiction C6; the MPDA article reports counts only (stump ribs with 4 of 14 sacralizations vs 94 of 775 others) because hypothesis tests are forbidden | [CTSP] `paper/mpda/main.tex`; `docs/LAB_JOURNAL.md`; commit `e659ad4`; [MEM] `anomaly-manifest-sources.md` |
| six-lumbar readings (18 records): true L6 11, lumbarized S1 4, T12 with aplastic ribs 1, needs a reader 2 (0376, 1053) | report and figure | [CTSP] `results/six_lumbar_readings/report.txt`, `six_lumbar_readings.png`; `scripts/six_lumbar_readings.py`, `shift_hypothesis_test.py` |
| sacral foramina counting does not work (93 cases × 81 settings; best 31-39% per case) | negative result | [CTSP] `docs/LAB_JOURNAL.md` "Negative results"; `scripts/sweep_foramina_params.py`, `plot_foramina_sweep.py` |
| Castellvi screen recovers subtle grades and misses gross ones (IIb median LOO rank 4; IIIb 442) | — | [CTSP] `docs/CASTELLVI_SCREEN_BLIND_SPOT.md`; `scripts/screen_missed_castellvi.py`, `join_castellvi_grades.py` |
| iliac crest ≥ 12 mm above L4-5 in 24.7% (195/789) | v5-era number | [CTSP] `README.md` "Release QC — v5"; `paper/clinical/main.tex` |
| PI does not separate by sex (51.3 vs 50.5); pelvic shape does | — | [CTSP] `scripts/extract_pelvic_shape.py` docstring; `docs/RELEASE_CHECKLIST.md` section 7 |
| pelvic width demo for students ("is the female pelvis relatively wider?") | the committed report used S1 width (v10); the current script measures femoral-head separation | [CTSP] `results/pelvic_width/report.txt`; `scripts/demo_pelvic_width_dimorphism.py` |

The count-free figure (`fig_countfree.pdf`, from `make_figures.py fig_countfree`) is held for the
next paper (commit `2232bde`; [CTSP] `paper/mpda/main.tex` comment at Descriptive Analysis).

---

## 5. The dataset article (MPDA): figures, tables, and how each is made

**Source**: [CTSP] `paper/mpda/main.tex` (REVTeX 4.2, `aapm`), `supplementary.tex` +
`supplement_body.tex` (shared floats), `title_page.tex`, `cover_letter.md`, `ctspinopelvic1k.bib`.
Title: "CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame, annotated for
lumbosacral transitional anatomy". Fourteen authors on the title page: Gregory Schwing
(corresponding, Department of Surgery, DMC and WSU), eleven School of Medicine students, Ashley Schehr first
(the same eleven usernames as `morphometrics/annotation_counts.csv`), and the two
radiology residents Miraziz Ismoilov and Nizar Alnabahneh ([CTSP] `paper/mpda/title_page.tex`
lines 39-63). The NeurIPS paper has a different author list (it includes Loren Schwiebert and Patrick
Schwing; [CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`). Constraints: ten published pages,
no hypothesis testing, dataset DOI before submission ([CTSP] `paper/mpda/main.tex` header;
`paper/mpda/PLAN.md`).

| artefact (current numbering) | what | generator | inputs | cost |
|---|---|---|---|---|
| Table I `tab:priorart` | public CT collections at the junction, black runs | hand-built in `main.tex` ([MEM] `tables-black-not-colour.md`) | literature | manual |
| Figure 1 `fig:pipeline` | how the dataset was built | TikZ inline in `main.tex`; `fig_pipeline_standalone.tex` for the form | counts in text | inline |
| Table II `tab:ribqc` | rib checks, pseudolabel vs release | `results/rib_qc_v4_vs_release/rib_qc_stages.py` (+ `rib_fragments_detail.py`) | grid job 40220664 outputs in that folder | data |
| Figure 2 `fig:anchors` | four phenotypes, cases 0704, 0428, 0094, 0005 | `python scripts/make_fig_anchors.py --reselect` (calls `select_anchor_cases.py` → `morphometrics/anchor_cases.json`, then `render_anchors.py`; `--scale_mode image --legend_cols 3 --panel_in 2.05 --height_in 2.35`) | `transition_morphometrics.csv`, label volumes (default `data/zenodo_deposit/labels`) | heavy |
| Table III `tab:spinopelvic` | PI/SS/PT/LL/PI−LL mean ± SD, n=756 | `scripts/extract_surgical_morphometrics.py`; numbers asserted by `paper/mpda/audit_ms.py` | `surgical_morphometrics.csv` | data |
| Figure 3 `fig:levelatlas` | EPWu, SCW/SCD, PDW by level T11-L5, L5 withheld in (a),(c) | `python paper/mpda/make_levelatlas_fig.py` (also writes `morphometrics/level_atlas.csv`) | `level_gradients.csv`, `surgical_morphometrics.csv`, `level_references.csv`, `panjabi_reference.csv` | cheap |
| Figure S1 `fig:hardware` | instrumentation, one exemplar per class | `scripts/render_hardware.py --labels data/zenodo_deposit/labels` (REPRODUCE) or `scripts/render_hardware_gallery.py` (audit_artifacts) — contradiction C7 | label volumes, `metal.csv` | heavy |
| Figure S2 `fig:validation` | spinopelvic measures against standing bands | `python paper/mpda/make_figures.py` (`fig_validation`) | `surgical_morphometrics.csv` | cheap |
| Figure S3 `fig:fov` | records carrying each level | `python paper/mpda/make_fov_fig.py` (default `--census morphometrics/label_census_v7.csv`) | census CSV | cheap |
| Table S1 `tab:pseudodice` | pelvic pseudolabeller Dice | `scripts/extract_pseudolabel_dice.py` | five checkpoints (HF) → `results/pseudolabel_dice/` | data |
| Table S2 `tab:completeness` | manifest field completeness | hand-written from `manifest.json`; no script | `manifest.json` | manual |
| Table S3 (census) | every populated id and its record count | `python scripts/make_census_table.py --census morphometrics/label_census_v11.csv --out paper/mpda/census_table.tex` (the file header says v11; the script default is v7) | `label_census_v11.csv` | data |

Mapping from older numberings: [CTSP] `paper/mpda/REPRODUCE.md` section 3 lists Figures 4, 5, 7
(countfree, validation, opportunistic), 6 (level atlas), 8 (FOV), 2-3 (renders); `audit_artifacts.py`
uses Fig 1-6 / Tables I-V / S1 (2026-09-18 state). On 2026-09-18 three figures and two tables moved
to supporting information to fit ten pages (commit `7d66f59`). `fig_countfree`, `fig_opportunistic`,
`fig_phenotypes`, `fig_priorart` exist in `paper/mpda/figures/` but are not in the current article.

**Audits**: `python paper/mpda/audit_artifacts.py [--regen]` (each artefact has a recorded
generator; cheap ones re-run and pixel-compared); `paper/mpda/audit_ms.py` (every number in the
text against its CSV; it caught the manuscript quoting v11 values while the repo shipped the v10
table, commit `2232bde`); `paper/mpda/audit_pdfs.py` (checks the packet PDFs, including the v11
DOI); `paper/mpda/page_estimate.py` (journal formula 4.3 + words/3000 + floats/1.9; disagrees with
the typeset count in either direction, [MEM] `journal-figure-and-style-rules.md`).

**Build and packet** ([CTSP] `paper/mpda/REPRODUCE.md` sections 4-5):
`bash paper/mpda/build.sh` (submission form, ~25 pages, meaningless for the limit) and
`bash paper/mpda/build.sh --reprint` (**the only page count that matters**, two-column; read the
whole output, errors print before the page count); `bash paper/mpda/make_arxiv.sh` (tarball plus a
clean-tree compile; refreshes `CTSpinoPelvic1K_arxiv_preview.pdf`); `python paper/mpda/make_overleaf.py`;
`python paper/mpda/make_submission.py` (**run from Windows**, it shells out to `wsl`) → flat
`dist/submission/` (Abstract.txt, Cover_Letter.md, Figure_1-3.pdf, Main_Document, Supporting_Information,
Title_Page). The structured abstract (under 300 words) goes in the submission form, not the PDF;
`main.tex` keeps it behind `\ifabstract` ([MEM] `journal-figure-and-style-rules.md`;
`paper/mpda/make_abstract_text.py`). Never pass a relative `--out` to `make_figures.py` (it once
wrote `paper/mpda/paper/mpda/figures/` and the build typeset stale figures).

**Style rules applied**: sans-serif (Arial/Helvetica), 80 or 180 mm wide, 600 dpi, black axes, grey
grid both axes, major ticks out, minor in, "(°)"; captions ≤ 60 words (Greg later asked for one or
two sentences, ≤ ~25 words); numbers under ten spelled out ([MEM] `journal-figure-and-style-rules.md`,
`figure-captions-terse.md`).

**Other article materials in `paper/mpda/`**: `CITATION_CHECK.md` (reference verification),
`STUDENT_REVIEW_RESPONSE.md`, `EMAIL_ASHLEY.md`, Ashley Schehr's revision document
(`CTSpinoPelvic1K_schehr revisions + sources notes.docx`), co-author drafts (`.docx`/`.pdf`),
`ARXIV_SUBMISSION.md`, `REFERENCE_DOWNLOADS.md`, `tools/render_pi_construction.py` (why one case
returns an impossible PI), `tools/aggregate_spinopelvic.py` (merge ostk shard output). Desktop-root
copies: [CTSP] `MDPA.pdf` (2026-09-16), `arxiv_final_draft_9_19_2026.pdf`, `MDPA_OL.zip`;
Desktop top level has `MDPA_AI.pdf`, `MDPA_FINAL.pdf`, `arxiv_prev.pdf` (`ls` of the Desktop; which
is the submitted version is not recorded beyond `dist/submission/`).

---

## 6. The NeurIPS 2026 paper (CTSP line, separate manuscript)

- "Not All Spines Are Created Equal: How CT Segmenters Fail on Lumbosacral Transitional Vertebrae",
  Evaluations and Datasets Track, submission 3474, OpenReview D8yRWDAGQF, accepted as a poster
  ([CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` first lines). Submitted PDF:
  [CTSP] `3474_Not_All_Spines_Are_Create.pdf`; reviews `CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.{pdf,txt}`.
- Every segmentation number was computed on the April 2026 release (1,153 records, ten-class scheme
  merged to nine for training, record-level split), not on v11; the Castellvi grades are the
  September two-reader reads ([CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` row 16 and
  "Version note").
- Build: `latexmk -pdf -interaction=nonstopmode neurips_2026.tex` in WSL (TeX Live 2026) in
  `CAMERA_READY_NEURIPS/src/` (same file).
- **The 2026-09-27 audit corrections are uncommitted** (git status: `M CAMERA_READY_NEURIPS/src/neurips_2026.tex`,
  `checklist.tex`, `references.bib`, `CAMERA_READY_CHANGES.md`; untracked `src/appendix/`,
  `src/figs/fig_app_construction.pdf`). The audit's facts files live in a session scratchpad
  (`neurips_audit/`, `neurips_fixes/FACTS_*.md`, `OPENREVIEW_NOTE.md`), not in the repository.
- **Open before upload** (items 3-22 of "What remains for Greg"): OpenReview form and Croissant
  file (v11 has no `croissant.json`, only v6); publish the April release's manifests and the
  174-id evaluated split or keep checklist item 5 "No"; 134 "[pending]" slots in Appendices I-J
  (SPINEPS report `…/neurips_spineps/score_v212/REPORT.md`, jobs 40481323 → 40481314 → 40481315;
  v11 summaries `/rs/rs_grp_oschome/go2432/neurips_v11/out/{ts,ens}/SUMMARY.md`, jobs
  40480728/31/32 and 40480730/33); TotalSegmentator `total_v3` never run; headline defect A (TS
  sacrum 0.817 counts TS's S1 class as a miss) still in the main text; licence differs between the
  HF card (CC BY-NC 4.0) and Zenodo (CC BY-NC-SA 4.0); the public [SEG] copy still carries the
  anonymised citation and author; competing-interests sentence vs the WSU invention disclosure.

---

## 7. Other manuscripts built on CTSP

| manuscript | where | state |
|---|---|---|
| Iliac crest as a level landmark (target SSRR) | [CTSP] `paper/clinical/main.tex`, `iliac_crest_landmark.pdf` | complete draft, `[CO-AUTHOR]` marks; last commit 2026-08-22 (`0ecbb82`); numbers predate v6 hip-laterality fixes and v11; must be recomputed |
| MLHC 2026 descriptor | [CTSP] `MLHC_2026_Research_Track_Paper.pdf`, `mlhc/`; [SEGM] | rejected ([MEM] `publication-roadmap.md`) |
| BIBM wrap-up (ostk + CT→radiograph bridge + viewer + post-op) | [BIBM] `main.tex`, `tools/cohort_stats.py`, `README.md`; [CTSP] `BIBM/` (IEEE template only) | draft with `\TODO`s; Table 1 needs `python -m ostk all … ` + `cohort_stats.py` |
| NeurIPS draft, September revision | [AR] `neurips_2026.tex`, `REVISION_PLAN.md`, `figs/` | frozen 2026-09-08 (section 13) |
| Radiology: AI port | `NextPaper/RadAI/main.tex` | SchwingNet topic; pointer only ([MEM] `publication-roadmap.md`) |
| CNS 2026 decks | [CTSP] `paper/cns2026/make_cns_deck_v*.py` | deck generators; v8 title "Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model…", Mini Podium 4, Mon 2 Nov 2026; v11_public is the disclosure-safe CT-only cut; generators deliberately not committed to the public repo ([MEM] `cns-deck-v2-2026-09-25.md`) |
| TechFair LSTV talk | [CTSP] `TechFair_LSTV_Schwing.pptx` | deck; content not checked |

---

## 8. QC and review spaces (student annotation)

- **Service**: FastAPI coordination service deployed as Hugging Face Docker Spaces; reviewers
  authenticate with their own HF login; the Space holds the only write token; corrected labels go
  to a private review repo; IRR is per-class Dice with threshold `TAU` 0.9; `ADJUDICATORS` may
  adjudicate ([CTSP] `review_service/README.md`, `app.py`, `store.py`, `service.py`, `admin.py`).
  Client: `reviewtool` (`reviewtool next`, `reviewtool adjudicate`) ([CTSP] `reviewtool/`).
- **v4 per-task Spaces** (`review_service/deploy_v4_spaces.py`): Space `{org}/CTSpinoPelvic1K-review-{slug}`,
  ledger `{org}/CTSpinoPelvic1K-reviews-{slug}`; slugs `ribs` (task rib_fix, revision v4), `spine`
  (spine_extend, v4), `classfix` (class_mixing, v4), `nerve` (ls_nerve, v3), `ili` (iliolumbar,
  v3), plus `triaged`. Org `anonymous-mlhc`. **Pointing a tool at the wrong ledger returns 0
  cases with no error.** Inspect with `python3 -m review_service.admin queue` ([MEM]
  `review-space-repos.md`).
- Older single Space `gregoryschwingmdphd/ctspinopelvic1k-review-triaged`: ledger
  `gregoryschwingmdphd/CTSpinoPelvic1K-reviews-triaged` (main branch), dataset
  `gregoryschwingmdphd/CTSpinoPelvic1K` branch v2; `…-reviews` without `-triaged` is an empty decoy;
  a plain Restart can reseed from a cached `crops_index`, use Factory reboot ([MEM]
  `review-space-repos.md`).
- **Ledger counts** (BUILD_CHAIN step 7): reviews-ribs 169 cases, reviews-spine 113,
  reviews-triaged 106 ([CTSP] `docs/BUILD_CHAIN.md`).
- **Who did what**: only record is `slots[].reviewer` in each `cases/*.json`; count done slots,
  not claims ([MEM] `annotator-roster.md`). Committed tallies: [CTSP] `morphometrics/annotation_counts.csv`
  ([handle withheld] 142, eleven student usernames with 20 to 73 slots each [usernames withheld in this
  copy; the committed csv holds them], Greg 17; ribs and
  spine only; nerve, ili, classfix, triaged zero); real names in `morphometrics/annotator_names.csv`.
  Completing slots does not by itself establish authorship ([MEM] `annotator-roster.md`).
- **Student guides** (point students here, do not rewrite): [CTSP] `docs/RIB_REVIEW_GUIDE.md`,
  `docs/SPINE_REVIEW.md`, `docs/CLASSFIX_REVIEW.md`, `docs/REVIEW.md`, `docs/STUDENT_ANNOTATION_PROTOCOL.md`,
  `docs/LABELING_GUIDE.md`, `docs/RIB_ANCHOR_REVIEW_GUIDE.md`, root `REVIEWERS*.md`
  (Windows/Mac/Linux/cheatsheet/fixing/AI editing). Grid access for students goes through
  Beethoven (`<laptop:ashley-bridge (Beethoven; folder 11)>`, `docs/guides/`).
- **Rules learned**: server-side gates reject a submission that still has a duplicate rib
  ([CTSP] `README.md` reviewer note); only rib-purity checks gate on rib reviews ([MEM]
  `rib-qc-gates-never-block-lstv.md`); escalate any junction a student cannot settle to a
  radiologist rather than overwrite ([CTSP] `paper/mpda/main.tex` Limitations).
- **Governing principles** of the dataset: append-only, radiologist ground truth immutable,
  pseudolabels never touch a GT voxel, ids reserved forward ([CTSP] `docs/DATASET_PRINCIPLES.md`;
  note the id numbers quoted there are from an older scheme).
- **Other QC tools**: `scripts/qc_audit_pairs.py`, `structure_qc.py`, `vertebra_topology_qc.py`,
  `bone_leak_qc.py`, `pelvis_opposing_qc.py`, `merge_qc.py`, `qc_dashboard.py`, `export_review_crops.py`,
  `push_crops.py`, `pull_reviews.py`, `process_reviews.py`, `auto_finalize.py` ([CTSP] `Makefile`
  targets with descriptions).

---

## 9. OpenSpineToolkit (ostk)

### 9.1 What it is

A tested Python package of geometry primitives and spinopelvic measurements on CTSpinoPelvic1K
masks, plus `projects/` folders for student miniprojects contributed by fork-and-PR
([OSTK] `CLAUDE.md`, `README.md`). Relicensed MIT → Apache-2.0 on 2026-06-23 (commit `8bcaa78`).
Renamed from OpenSpineToolbox in June 2026; the old `OpenSpineToolbox` folder is stale ([MEM]
`pacs-demo-and-ostk-params.md`).

### 9.2 Modules ([OSTK] `ostk/`, line counts from `wc -l`)

| module | role |
|---|---|
| `labels.py` (156) | `LABELS_V4`, `LABELS_V10`, `labels_for()`, `SchemeError`, `lid()` |
| `io.py`, `geometry.py`, `masks.py`, `record.py`, `parallel.py` | NIfTI I/O in world mm; PCA, TLS plane, sphere fit, angles; mask helpers; `Measurement` contract; `map_cases` |
| `spine.py` (533) | end-plate fitting; `endplate_from_label` (with the S1 → sacrum fallback, section 9.5); PI/PT anchor |
| `vertebral_body.py` (837) | body isolation, end-plate corners, `canal_mask`, `body_mask_by_canal` |
| `metrics.py` (682) | PI/SS/PT, LL (+ per segment), PI−LL, Schwab modifiers, Eq. 73.1, Roussouly, `spinopelvic_summary_from_label`; femoral head = acetabular-interface sphere fit; plausibility gates with sources |
| `morphometry.py` (412) | level dimensions in the vertebra's own frame (VBHa/VBHp, EPWu/EPWl, EPDu/EPDl, SCW/SCD, PDW) |
| `genant.py` (241) | six-point vertebral morphometry (Genant 1993) |
| `cobb.py` | coronal Cobb angle |
| `drr.py`, `project2d.py`, `metrics2d.py` | sagittal DRR along the true bicoxofemoral axis; 2-D projection of landmarks; 2-D spinopelvic port (identical definitions) |
| `surgery.py` (683) | post-op synthesis (section 11) |
| `cli.py` | `python -m ostk {pi,ll,cobb,all,morph} --labels <dir> --out <csv|jsonl> --workers N` |

Tests: `python -m pytest` (94 `def test_` functions across `tests/`; `tests/test_labels.py`
covers scheme detection). `tools/export_demo_case.py` builds the PACS demo bundle (section 10).

### 9.3 History that matters

September 2026 commits ([OSTK] `git log`): morphometry in the vertebra frame (`204ce14`), scheme
detection (`2e8b2c2`), flags dropped for bad cases (`477dd0d`), sacral base surface fit (`6cacd3e`),
signed PT (`4d50296`), pedicle width saga (`da2550a`, `db4db40`, `d1189c8`, `6a5992f`), canal depth
as a midsagittal chord with ring closing (`1b7005c`, 2026-09-10 22:52), Genant six-point
(`ba82e1a`), numpy 2.5 fix (`cb43197`).

### 9.4 Known regression: ring closing in `canal_mask` (unfixed as of `cb43197`)

Commit `1b7005c` added a 2 mm ring closing before `fill_holes` in `canal_mask`. In the two or three
sections just below the pedicles the closing bridges the laminae, `body_mask_by_canal` takes that
section's anterior canal edge as the wall (14-15 mm posterior of the true wall), and every lower
section inherits it: on case 0097 T12 VBHp 38.4 vs 28.9, EPDl 52.0 vs 34.8; about one vertebra in
seven inflated by 10-17 mm with no gate firing. Second defect: `min_vox = 20` admits 3 mm
"canals" (16% of chords below the 11.07 mm living floor vs 2.6% published). The committed
`morphometrics/ostk_level_morphometry.csv` predates it and is right. Fix plan: hole area ≥ 18 mm²
per section; wall only from sections whose hole reaches the canal's median area; test = 0097 rows
within 1 mm; then refresh the grid copy. Found by rendering ([MEM]
`ostk-canal-closing-regression.md`; [SSN] `SchwingNet/results/reader_e/diag/*.png`). I confirmed
`canal_mask(..., min_vox: int = 20)` and the `binary_closing` call are still in [OSTK]
`ostk/vertebral_body.py` lines 98-132.

### 9.5 New finding from this pass: ostk on v11 volumes takes the whole-sacrum fallback silently

`LABELS_V10` still maps `"S1": 29` ([OSTK] `ostk/labels.py` line 64). On a v11 volume no voxel is 29,
so `endplate_from_label(label, affine, "S1", …)` falls back to the whole sacrum ([OSTK]
`ostk/spine.py` lines 473-474). The function's own docstring calls this "a last resort, not an
equivalent… drives pelvic incidence far too low", and no QC flag is attached for the fallback
(`grep` finds no fallback flag in `metrics.py` or `spine.py`; only `low_voxels:S1` when the fit
returns nothing). So `python -m ostk all` on v11 labels runs the branch documented as wrong, unless
something else intervenes. The release's own extraction script isolates the plate by the lowest
lumbar footprint instead. Not run here; found by reading code. [MEM] `scheme-bone-hardware-only.md`
already says ostk "needs the same treatment" (remove the S1 key) and that its scheme detection is
safe. Fix: port the extraction script's footprint isolation into ostk and flag the fallback.

### 9.6 Stale documentation inside [OSTK]

`SPEC.md` section 1 and `ostk/README.md` still describe the v3 legacy scheme (ids 1-50), "27 tests",
and "SVA/TPA out of scope (no C7/T1)"; `CLAUDE.md` says "never hard-code an id, use lid('L1')"
(before `labels_for`). The memory note says do not reintroduce the blanket "SVA/TPA out of scope"
claim in the PACS demo because some scans include C7/T1 ([MEM] `pacs-demo-and-ostk-params.md`).
Contradiction C10.

### 9.7 Student miniprojects

[OSTK] `projects/`: centroid-trajectory-tortuosity, disc-spacing, lordosis-distribution-index,
lordosis-trall-angle, lumbar-vertebral-spacing, osteoporosis-hu, sacral-slope-pelvic-incidence,
sagittal-vertical-axis, scoliosis-cobb-angle, spinal-stenosis, spondylolisthesis, t1-pelvic-angle,
vertebral-body-wedging-index. Which have code beyond a README: not checked here.

---

## 10. PACS demo, engine-swap contract, latency

- The NiiVue viewer lives in [WEB] `pacs/` (`pacs.js`, `pacs.css`, `ct.html`, `xr.html`, `xr.js`,
  `infer.js`), data-driven by `pacs/data/<case>/metrics.json` (keys `case_id, summary, geometry,
  files, label, postop`) plus `ct.nii.gz`, `seg.nii.gz`, and for the post-op demo
  `postop_ct.nii.gz`, `postop_seg.nii.gz`. Bundled case 0003 ([WEB] `pacs/data/0003/`; [MEM]
  `pacs-demo-and-ostk-params.md`).
- Regenerate: `python tools/export_demo_case.py --ct <ct> --label <label> --case-id 0003
  --out-dir ../openspineconsortium.github.io/pacs/data --crop-margin 25 --mask-bone --downsample 2`
  (add `--postop --postop-age 50 --postop-technique alif`), then bump the cache-bust query; pushing
  github.io publishes publicly ([OSTK] `tools/export_demo_case.py` docstring; [MEM]
  `pacs-demo-and-ostk-params.md`, `postop-spine-synthesis.md`). The exporter imports `lid` (legacy
  map default), and case 0003 is a v3-scheme case; running it on a v11 case needs a scheme check.
- **Engine-swap**: the viewer consumes `metrics.json`; any backend that emits the same schema drops
  in; planned interface `predict(ct, label) -> {summary, geometry}` and `synthesize(ct, label, plan)`;
  the geometric pipeline's outputs can serve as training labels for a network ([MEM]
  `engine-swap-architecture.md`). Contract only; no network backend exists.
- **Latency**: X-ray demo went 40,018 ms → 1,360 ms on 2026-09-12 (http redirect on the custom
  domain disabled WebGPU and service workers; COEP refused the CDN so onnxruntime-web is vendored
  under `pacs/ort/`; 1024 → 640 export); measure with `python pacs/measure_live.py --film X --headed
  --channel chrome` ([MEM] `pacs-website-latency-root-cause.md`). Since 2026-09-14 the X-ray model
  runs behind the level service, not in the browser ([WEB] commit `ea0086c`; [MEM]
  `level-service-serving.md` per the index).
- A survey protocol for the demo exists: [CTSP] `docs/survey_protocol.md` (CROSS / CHERRIES).

---

## 11. Post-operative synthesis and morphology augmentation

### 11.1 `ostk.surgery` (June 2026)

- Every lordosing operation = rotate the segment cranial to the operative level by Δ° in the
  sagittal plane with the pelvis fixed; techniques differ by fulcrum and tissue change ([OSTK]
  `ostk/surgery.py` docstring).
- Phase 1 `simulate_correction(label, affine, level, delta_deg)` (validated: LL rises ~Δ, PI/SS/PT
  unchanged); Phase 2-3 `bend_spine`, `warp_ct`, interbody cages, `predict_compensated_alignment`;
  Phase 4 `synthesize_postop` (lordosis plus reciprocal thoracic kyphosis 0.5·ΔLL, optional pelvic
  anteversion), Lafage age-adjusted targets (PI−LL = (age−55)/2 + 3, PT = (age−55)/3 + 20,
  SVA = 2(age−55) + 25), `place_interbody_cages` ([MEM] `postop-spine-synthesis.md`; [OSTK] commits
  `495a924` … `f2515bd`, 2026-06-23).
- **Do not re-measure the synthesised image**: voxel roughness on end-plates makes the plane fit
  collapse (LL 45.7 → ~24 when it should rise to ~55); post-op numbers are carried analytically
  (rotate L1 by +9.3° → 45.7 → 55.0°) and the image is display only. Demo: case 0003, ALIF L1-S1,
  age 50, LL 45.7 → 55.0, PI−LL 9.8 → 0.5, five cages ([MEM] `postop-spine-synthesis.md`,
  `postop-jaggedness-future.md`). Future: anti-aliased resampling, end-plate smoothing, or
  per-vertebra rigid placement.
- Planned home: P6 "geometry-driven post-op alignment synthesis" → a methods journal; folded into
  the BIBM wrap-up in June ([MEM] `publication-roadmap.md`).

### 11.2 PolyPose (September 2026, lives in [SSN])

- Decision (Greg, 2026-09-23): vary lordosis/kyphosis generatively with PolyPose (Gopalakrishnan,
  Dey, Golland, NeurIPS 2025; MIT) within Panjabi segmental range of motion and LSTV/TLTV-specific
  published ranges; a fused or sacralised junction gets zero relative motion; pelvis fixed so PI is
  invariant; no synthesis makes an L6; seeded, manifested, environment-pinned, with self-failing
  invariant checks ([MEM] `polypose-decision.md`).
- Generator `tools/polypose_sample.py generate|finalize|head` + `tools/polypose_warp.py` ([SSN]
  commit `1f4418f`, never pushed); validation chain `slurm/polypose_validate_submit.sh`; banks under
  `/rs/rs_grp_oschome/go2432/data/polypose/validation/bank_{gravity,invdf1}`; reproducibility frame
  [SSN] `SchwingNet/results/polypose/REPRODUCIBILITY.md`; DeepFluoro reproduction "REPRODUCED"
  (Dice pelvis 0.992, femora 0.978/0.980; one pose-flip deviation documented) in
  `SchwingNet/results/polypose/REPRODUCTION.md` ([MEM] `polypose-generator-build.md`).
- **Its measurement path reuses the release plate fits**: `tools/polypose/measure_sagittal.measure_image`
  (canonical RAS; the S1 plate isolated in the lowest-lumbar footprint, so a pair must use the
  source L5 as corridor). The old ostk-primitive path read PI 3.6 / LL −8.9 on PIR case 0874 (truth
  53 / 54) ([MEM] `polypose-generator-build.md`). CTSP cohort measurements by this path:
  [SSN] `SchwingNet/results/polypose/cohort_ctsp_release.json`, `cohort_sagittal.json`.
- Status: `SchwingNet/results/polypose/validation/` holds only `inspect/` sagittal PNGs and `smoke/`;
  `VALIDATION.{json,md}` named as the results target does not exist. Whether a bank was used in
  training is not recorded here (SchwingNet topic).

---

## 12. NextPaper/spinopelvic-seg (the pelvic pseudolabeller's public code)

- nnU-Net v2 training and inference pipeline, nine classes (L1-L4, `last_lumbar` = merged L5/L6,
  sacrum, left/right hip, ignore), 5-fold ResEnc-L at a 100 GB target on Dataset803 ([SEG]
  `README.md`). This is the model that pseudolabelled the 440 pelvises (section 3.2), and its
  checkpoints are on HF (`OpenSpineConsortium/spinopelvic-seg-checkpoints`).
- Inference: `nnUNetv2_predict -d 803 -c 3d_fullres -p nnUNetResEncUNetPlans_100G
  -tr nnUNetTrainerWandB_500ep_LSTVOversample -f 0 1 2 3 4 -chk checkpoint_best.pth`;
  SLURM wrapper `slurm/spine_predict_803_best.sh` (uses `/dev/shm` to dodge an nnU-Net
  multiprocessing shutdown race); evaluation `tools/eval_full.py` (per-case Dice, 40 mm L5/S1
  junction DSC, confusion blocks, last_lumbar specificity) ([SEG] `README.md`).
- Training: `make download-data`, `build-container`, `splits`, `plans`, `viz`, `preprocess`,
  `train-array`, `eval-ensemble`, `ablate` ([SEG] `Makefile`, `README.md`). Tests in `tests/`.
- History: two commits, "Initial release" 2026-05-12 and Apache-2.0 licence 2026-06-23. It is a
  copy of the [SSN] trainer at the time, "identical to the training code apart from naming and
  anonymization" ([CTSP] `CAMERA_READY_NEURIPS/src/checklist.tex` item 5).
- Gaps: README points at `containers/`, `data/`, `docs/pipeline.md` which are not in the checkout
  (`ls`); the README and author fields are still anonymised (`anonymous-neurips-ED`) (NeurIPS open
  item 14).
- [SEGM] is the MLHC-anonymised twin (one commit), differing in README, Makefile, pyproject,
  scripts, and lacking LICENSE/NOTICE (`diff -rq`).

## 13. NextPaper/AR (the NeurIPS draft, September revision)

- Not a git repository. `neurips_2026.tex` titled "Not All Spines Are Created Equal: How
  TotalSegmentator Fails on Lumbosacral Transitional Vertebrae", compiled 2026-09-08
  ([AR] `neurips_2026.tex` lines 28-29; `neurips_2026.pdf`).
- `REVISION_PLAN.md` (2026-09-08) records the planned changes: dataset section to v10 (802 records,
  68-id scheme, ribs 5,749 evaluable / 0.035%, 11 instrumented), new "one-shot level identity"
  model (Dataset810, 24 classes, ResEnc-L, patch 256×320×320, launched 2026-09-07) with a sequence
  decoder (`tools/decode_sequence.py`), results to add (separability AUC 0.998/0.990, six-lumbar
  readings, co-occurrence OR 2.8 p 0.09; detect_v2 radiograph corner detector AP50 0.970), and
  the order of work.
- Frozen on 2026-09-08 by Greg's instruction; content goes to NextPaper/RadAI ([MEM]
  `publication-roadmap.md`). The camera-ready that was actually prepared is [CTSP]
  `CAMERA_READY_NEURIPS/src/neurips_2026.tex`, with a different subtitle ("How CT Segmenters
  Fail…").
- Figures in [AR] `figs/` (fig_anchors, fig_architecture, fig_capabilities, fig_countfree,
  fig_patch_context_0376, fig_pipeline_oneshot, fig_training, six_lumbar_readings,
  lstv_lumbarization_215_spine_only) were copied from [CTSP] and [SSN] `benchmark/figs` ([MEM]
  `competitor-benchmark.md`).

---

## 14. Contradictions between documents (both readings, which is trusted, why)

| # | topic | reading A (file) | reading B (file) | trusted and why |
|---|---|---|---|---|
| C1 | is v11 public? | Zenodo v11 published 18 Sep 2026, DOI 22797014 ([CTSP] `paper/mpda/cover_letter.md`; NeurIPS change log says all cited URLs returned HTTP 200 on 2026-09-25) | "v11 exists only locally / on the grid"; Zenodo v10 current; HF `dataset_labels.json` still has key 29 (API check 2026-09-27) ([MEM] `hf-mirror-is-v10.md`) | Zenodo v11: A (the cover letter states a publication date; the memory note only checked HF). HF mirror: B (checked by API). Students downloading from HF get v10 with 29. Verify Zenodo by browser. |
| C2 | Panjabi T11/T12 end-plate width | digitised from Figure 4A, page 892 missing, replace when ILL arrives ([CTSP] `paper/mpda/REPRODUCE.md` section 2) | full paper obtained 2026-09-13, Table 3 values in the reference table ([MEM] `panjabi-1991-page-892.md`; commit `83f7f95`; MPDA Figure 3 caption still says "T11-T12 EPWu is digitised from his Figure 4A") | B; commit `83f7f95` replaced the values. The Figure 3 caption and REPRODUCE.md are stale. |
| C3 | which spinopelvic issues are open | "three still open" ([CTSP] `CLAUDE.md`) | four bullets in `docs/SPINOPELVIC_ESTIMATOR.md`; a different list in `paper/mpda/REPRODUCE.md` "Known-open" | see section 4.3; the estimator document is the detailed account |
| C4 | label scheme in REPRODUCE | "The scheme is v10… S1=29" ([CTSP] `paper/mpda/REPRODUCE.md` section 0) | v11, 29 retired ([CTSP] `CLAUDE.md`, `scripts/label_scheme.py`) | B; REPRODUCE.md was not updated after 2026-09-11 |
| C5 | Castellvi distribution | IIIb 18 / IV 4 / IIb 4 / IIIa 3 / IIa 2 / Ib 2 ([CTSP] `morphometrics/castellvi_grades.csv`, `zenodo/README.md`) ; IIIb 19 (May sheet) | IIIb 16 / IIb 6 / IV 4 / IIa 4 / Ib 2 / IIIa 1 ([CTSP] `docs/castellvi_consensus.csv`, `zenodo/KNOWN_ISSUES.md`) | B, the two-reader consensus in the manifest from v8 on |
| C6 | rib/lumbosacral co-occurrence | OR 19.6 over 796 cases with a 2×2 of TL/LS variants ([CTSP] `docs/LAB_JOURNAL.md`, 2026-08-19) | OR 2.8, p 0.09, stump ribs vs sacralization (commit `e659ad4`; [AR] `REVISION_PLAN.md`); CTSP OR 4.00 [1.00, 16.03] from the voxel flag master ([MEM] `anomaly-manifest-sources.md`) | none is in the MPDA article (tests forbidden; Fisher test removed, commit `2ba362f`). The three use different variant definitions; the pooled 12.8 across corpora is Simpson's paradox and must never be quoted ([MEM] `anomaly-manifest-sources.md`). |
| C7 | hardware figure generator | `scripts/render_hardware.py` ([CTSP] `paper/mpda/REPRODUCE.md`) | `scripts/render_hardware_gallery.py` ([CTSP] `paper/mpda/audit_artifacts.py`) | not recorded which produced the committed `figures/fig_hardware.pdf`; both exist |
| C8 | femoral heads that are metal | nine ([CTSP] `docs/HARDWARE_CLASSES.md`) | eight ([CTSP] `zenodo/KNOWN_ISSUES.md`, `paper/mpda/main.tex`, `docs/SPINOPELVIC_ESTIMATOR.md`, census: id 66 in 8 records) | eight (the census counts the voxels) |
| C9 | source GT corrections | done: "112 spine fixes in 103 cases; 13 pelvic fixes in 12" ([CTSP] `paper/mpda/main.tex` Fig. 1) | every row "pending (in review)" ([CTSP] `docs/CORRECTIONS.md`, last changed 2026-07-21) | not recorded; CORRECTIONS.md was never updated after review, so the final state of each row is unknown |
| C10 | ostk label map and scope | v3 legacy ids, "SVA/TPA out of scope" ([OSTK] `SPEC.md`, `ostk/README.md`, `CLAUDE.md`) | `labels_for` detects v4/v10; do not claim SVA/TPA blanket out of scope ([OSTK] `ostk/labels.py`; [MEM] `pacs-demo-and-ostk-params.md`) | B |
| C11 | where batch jobs run | `slurm/*.sh` use `-q primary` and `data/v5_final`, `data/hf_export/ct` ([CTSP] `slurm/finalize_release.sh`, `morphometrics.sh`) | partition `reqp` with `--qos=requeue`; labels at `~/data/CTSpinoPelvic1K/labels`; grid keeps only `~/data/CTSpinoPelvic1K` after the 2026-09-07 cleanup ([CTSP] `CLAUDE.md`; [MEM] `zenodo-deposit.md`) | B; the slurm scripts must be edited before reuse; whether `data/v5_final` still exists on the grid is not recorded |
| C12 | release labels path on the grid | `data/v5_final/{case}_label.nii.gz` ([MEM] `grid-access.md`) | `~/data/CTSpinoPelvic1K/labels` ([CTSP] `CLAUDE.md`) | B (newer) |
| C13 | funding | "This work received no funding." ([CTSP] `paper/mpda/main.tex` Acknowledgements) | NIH F30GM147909 during the first months; no other funding ([CTSP] `paper/mpda/title_page.tex` line 101; `cover_letter.md`) | B (Greg 2026-09-25, commit `f14c9b9`); the main-document sentence needs the same wording |
| C14 | Vialle 2005 sample size | n = 300 ([CTSP] `docs/SPINOPELVIC_ESTIMATOR.md`) | n = 260 ([CTSP] `docs/METHODS_REFERENCES.md`) | not checked against the paper |
| C15 | README release numbers | PI median 54.7, SS 36.9, PT 17.3, LL 52.7, 15 lumbar-rib records, ribs 5,749 evaluable ([CTSP] `README.md` "Release QC — v5") | PI 51.5 median / 52.1 mean, SS 36.6, PT 15.5, LL 51.7; 16 lumbar ribs; 5,753 evaluable ([CTSP] `paper/mpda/main.tex`; CSV) | B; README is the v5-era card (it also still describes S1 = 29, "ribs deferred to v4" with ids 34-57 reserved, an `ignore` 255 sentinel, and "PIR" orientation without the analyse-in-RAS rule) |
| C16 | number of annotators | "13 students completed at least one slot" ([MEM] `annotator-roster.md`) | 11 student usernames plus Greg in the same note and in `morphometrics/annotation_counts.csv`; 11 student authors on `paper/mpda/title_page.tex` | 11 (CSV and title page agree); the "13" is not supported by any listed file |
| C17 | census file behind Fig. S3 / Table S3 | default `label_census_v7.csv` in `make_fov_fig.py` and `make_census_table.py` | `census_table.tex` says "Generated from label_census_v11.csv"; `audit_artifacts.py` names `label_census.csv` | the vertebral counts are identical across v7 and v11 for the levels plotted; pass `--census morphometrics/label_census_v11.csv` explicitly |
| C18 | S1 carve failure count | 222 records over half the sacrum ([CTSP] `CLAUDE.md`, commit `2232bde`) | 221 of 801 with frac > 0.5 (my recount of `morphometrics/s1_carve_audit.csv`); commit `2232bde` also says "the 221 degenerate ones" | the CSV: 221 strictly above 0.5 (the 222 may include a boundary case; not recorded) |
| C19 | plate-gate rejections | "the gate rejecting 14 records" (commit `2232bde`) | 44 ([CTSP] `paper/mpda/main.tex` Table III caption; CSV) | 44; [MEM] `s1-carve-changed-spinopelvic.md` says the 14 was never checked against the CSV |
| C20 | `docs/HANDOFF_2026-09-21_PM.md` in [CTSP] | filed as a CTSP handoff | its content is the SchwingNet C-arm audit track | untracked and misplaced; belongs to [SSN] |

---

## 15. Recipes (regenerate, in order)

All heavy steps run as batch jobs, never on the login node (warrior); use `sbatch -D <dir>`
because `--output` resolves against the submit directory; prefer `afterany` over `afterok`
([CTSP] `CLAUDE.md` "Grid"). Network (git push, ssh, rsync) goes through
`wsl -e bash -lc '...'`, except `make_submission.py`, which must run from Windows.

1. **Get the release**: Zenodo concept DOI (labels) + TCIA CT via `zenodo/fetch_from_tcia.py` and
   `zenodo/reconstruct_ct.py`, or the HF mirror (CTs; labels there are v10 as of 2026-09-27 — merge
   29 into 26 with `python scripts/merge_s1_into_sacrum.py --src <v10 labels> --dst <v11> --write`
   if needed).
2. **Gates**: `python scripts/check_release_invariants.py --labels <v11> --ct <ct> --workers N --out qc_invariants.csv`;
   `python scripts/qc_rib_vertebra_incidence.py --labels <v11> --workers N --out <dir>`.
3. **Measurements** (each writes one CSV into `morphometrics/`; set `D=~/data/CTSpinoPelvic1K`):
   the seven commands in [CTSP] `paper/mpda/REPRODUCE.md` section 1. `extract_proximal_femur.py`
   needs ~220 GB at 8 workers. Normalise case ids with `zfill(4)` before diffing old and new.
   **Recompute `pelvic_shape.csv`, `transition_morphometrics.csv` and `degenerative.csv` on v11**
   (section 4.1) and check sacrum-adjacent columns against the old values.
4. **References**: `python morphometrics/make_reference_table.py`.
5. **Figures**: `python paper/mpda/make_levelatlas_fig.py` (Fig. 3 + `level_atlas.csv`);
   `python paper/mpda/make_figures.py` (Fig. S2); `python paper/mpda/make_fov_fig.py --census morphometrics/label_census_v11.csv` (Fig. S3);
   `python scripts/make_fig_anchors.py --reselect` (Fig. 2, heavy, needs labels);
   `python scripts/render_hardware.py --labels <v11>` (Fig. S1, heavy);
   `python scripts/make_census_table.py --census morphometrics/label_census_v11.csv --out paper/mpda/census_table.tex` (Table S3);
   `python scripts/extract_pseudolabel_dice.py` (Table S1, fetches checkpoints from HF);
   rib table: `results/rib_qc_v4_vs_release/rib_qc_stages.py` on the grid (Table II).
   The command that produced `label_census_v11.csv` is not recorded; `scripts/label_census_v7.py --labels <v11>` is the likely one.
6. **Audit**: `python paper/mpda/audit_artifacts.py --regen`; `python paper/mpda/audit_ms.py`.
7. **Build**: `bash paper/mpda/build.sh --reprint` (read the whole output; ≤ 10 published pages);
   then `make_arxiv.sh`, `make_overleaf.py`, `make_submission.py` (Windows).
8. **ostk numbers**: `python -m ostk morph --labels <dir> --out morph.csv --workers 8`;
   `python -m ostk all --labels <dir> --out summary.csv --workers 8` — but see section 9.5 before
   trusting PI from ostk on v11.
9. **Commit and push**: directly to master; `git push origin master && git push osc master` via WSL;
   [OSTK] branch `main`, both remotes.

---

## 16. Context worth exporting (lessons that cost time)

- **The recurring failure is a number that is wrong but plausible**: three estimators produced
  finite, reasonable values from the wrong bone, the wrong surface or the wrong label map, and none
  raised. Check against something outside the computation: published values, an independent
  implementation, the distribution's shape (spread, not median), a stated prevalence ([CTSP]
  `CLAUDE.md` "How to be useful here").
- **A maximum extent is not a diameter; a first-slice-that-works is not a plane**; reproducing a
  published number means reproducing its definition ([CTSP] `CLAUDE.md`).
- **Render the mask**: rendering settled the S1 carve, the L5 shoulders, Figure 2 alignment and the
  ostk canal regression where numbers did not ([CTSP] `CLAUDE.md`; commit `2232bde`; [MEM]
  `ostk-canal-closing-regression.md`).
- **A check that fails almost everything is accusing itself** (sidedness check failed 801/802 with
  the RAS convention backwards) ([CTSP] `docs/RELEASE_CHECKLIST.md` 2.1).
- **Pooled sided checks miss small transposed structures**; compare each sided pair separately
  (0790 was missed) ([CTSP] `docs/VERSION_PROGRESSION.md`).
- **The minimum distance between two bones is almost never the measurement you wanted** — it
  finds a joint ([CTSP] `docs/METHODS_REFERENCES.md`).
- **The border label is a reader's**: no morphometric criterion overruled a reading; a T12 and an
  L1 at the border are separated by the eye that read them ([CTSP] `paper/mpda/main.tex` Label
  scheme). Never call a T13 and a lumbar rib "the same object under two names" (Greg objected
  strongly) ([MEM] `scheme-bone-hardware-only.md`).
- **Say plainly what is not known** (the preferred form is an unexplained failure recorded, not a
  guess) ([CTSP] `CLAUDE.md`).

---

## 17. Flags

- **F1 (security)**: the git remote URL of [SEGM] (`NextPaper/spinopelvic-seg-mlhc/.git/config`)
  embeds a GitHub personal access token for `anonymous-mlhc` in plain text (seen in `git remote -v`
  output; not copied here). Revoke it on GitHub and rewrite the remote without credentials.
- **F2**: NeurIPS camera-ready corrections of 2026-09-27 are uncommitted in [CTSP]
  `CAMERA_READY_NEURIPS/`, and the audit's fact files are in a session scratchpad; a lost working
  tree loses them.
- **F3**: ostk computes PI on v11 volumes through the whole-sacrum fallback with no flag (section
  9.5); the ring-closing regression in `canal_mask` is still in `main` (section 9.4).
- **F4**: `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv`,
  `opportunistic.csv`, `proximal_femur.csv` were last written before v11 (2026-09-09/10); the
  first three touch the sacrum or lumbosacral disc. Recompute before any new claim.
- **F5**: HF mirror labels are v10 (id 29 present) while the article cites v11; anything that
  gates on 29 (student materials, `select_anchor_cases.py`-style checks) behaves differently on the
  two copies ([MEM] `hf-mirror-is-v10.md`).
- **F6**: [CTSP] `README.md`, `STATUS.md` (2026-06-11), `docs/ROADMAP.md` (2026-06-21 dates),
  `paper/mpda/REPRODUCE.md`, `zenodo/README.md` and `zenodo/KNOWN_ISSUES.md` (titled v10) are
  stale relative to v11; a new student will read them first.
- **F7**: the [CTSP] repository root holds many personal and administrative files (IRB letters,
  letters of recommendation, `.ica` session files, installers, `cookies.txt`) as untracked files
  next to a public repository; `git add -A` would publish them. Gitignore or move them.
- **F8**: the clinical iliac-crest draft and the student pelvic-width report were computed on
  pre-v6/pre-v11 labels.

---

## 18. Unknowns

| fact | where looked |
|---|---|
| Whether Zenodo v11 (22797014) is actually public | [CTSP] `paper/mpda/cover_letter.md`, `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`, `zenodo/`; [MEM] `hf-mirror-is-v10.md`, `zenodo-deposit.md` (no network used) |
| Editorial decision on the MPDA submission after 2026-09-25 | [CTSP] `git log`, `paper/mpda/`, `dist/submission/` |
| Whether the NeurIPS camera-ready was uploaded and the OpenReview note posted | [CTSP] `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`, `git status` |
| Whether `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv` were recomputed on v11 anywhere (grid) | [CTSP] `git log -- morphometrics/`, commit messages `47e72d0`, `2232bde` |
| Which two records besides the 44 plate rejections lack PI (802 − 44 − 2 = 756) | `morphometrics/surgical_morphometrics.csv` (reason column blank), [MEM] `s1-carve-changed-spinopelvic.md` |
| Why the splitter flagged record 0500 as L6 | [CTSP] `paper/mpda/main.tex`; [MEM] `splits-*-v3-resplit.md` (the "Splits & v3 resplit" note) |
| Final state of each row in `docs/CORRECTIONS.md` | [CTSP] `docs/CORRECTIONS.md` (all "pending") |
| Which script produced the committed `figures/fig_hardware.pdf` | [CTSP] `paper/mpda/REPRODUCE.md`, `paper/mpda/audit_artifacts.py` |
| Exact command that produced `morphometrics/label_census_v11.csv` | [CTSP] `scripts/label_census*.py`, grep for the filename |
| Whether `data/v5_final` and `data/zenodo_deposit` still exist in the grid checkout after the 2026-09-07 cleanup | [MEM] `zenodo-deposit.md`, `grid-access.md`; [CTSP] `slurm/*.sh` defaults |
| Why ostk's 2026-09-10 shard run produced almost no pedicle widths | [CTSP] `docs/SPINOPELVIC_ESTIMATOR.md` "Pedicle width" |
| Whether the 768 numeric-id and 34 `CTC-` TCIA records include the same human | [SSN] `docs/PATIENT_IDENTITY_SPEC.md` lines 171-181 |
| The anterior pelvic plane angle (APPA) for the cohort | [CTSP] `docs/SPINOPELVIC_ESTIMATOR.md` section 5 (experiment not done) |
| LSTV-stratified PI sensitivity analysis | [CTSP] `docs/SPINOPELVIC_ESTIMATOR.md` "Still open" (not done) |
| Current state of the six unreviewed `pelvic_native` cases and the 16 zero-thoracic cases | [CTSP] `docs/RELEASE_CHECKLIST.md`, `docs/LAB_JOURNAL.md` |
| Whether the BIBM wrap-up was ever submitted | [BIBM] `README.md`; [MEM] `publication-roadmap.md` |
| Whether a PolyPose bank was validated and used | [SSN] `SchwingNet/results/polypose/` (no `VALIDATION.md`); [MEM] `polypose-generator-build.md` |
| Which of the Desktop `MDPA*.pdf` files is the submitted version | Desktop `ls`; [CTSP] `dist/submission/` holds the packet |
| Vialle 2005 sample size (260 or 300) | [CTSP] `docs/SPINOPELVIC_ESTIMATOR.md`, `docs/METHODS_REFERENCES.md` |
| Which [OSTK] `projects/` folders contain working code | [OSTK] `projects/` listing only |
| Whether the 0787 lumbar-rib disagreement (export vs working copy) was resolved by re-export or by accepting 16 | [CTSP] `docs/VERSION_PROGRESSION.md`, `docs/RELEASE_CHECKLIST.md`; census now says 16 |
