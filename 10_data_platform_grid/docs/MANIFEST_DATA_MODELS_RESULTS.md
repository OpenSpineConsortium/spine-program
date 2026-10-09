# Manifest — data, models, results (FluoroCap vertebra level identification)

Assembled 2026-09-16 from five read-only grid inventories and three adversarial verifications.
Nothing was submitted, modified or deleted on the grid.

`~` throughout means `/wsu/home/go/go24/go2432` on `go2432@grid.wayne.edu`. Local repo paths are
given in full. Every number below is traceable to a named file; where two inventories disagree,
both readings are given and the one trusted is named with its reason. Anything that was not read
is in §7, not omitted.

Level alphabet is 27 classes: C1–C7, T1–T12, T13, L1–L6, sacrum. T13 and L6 are variant classes.

---

## 1. The question that prompted this

**The 98.7 / 99.1 / 99.4 result was not lost and was not replaced. It is on disk, unchanged, at
`~/bench/xr_fov/recurrent.json`, written 2026-09-13 13:28:00.** The four numbers in it are
98.69 / 99.13 / 99.41 / 99.48 % exact at 3 / 5 / 7 / 9 vertebrae visible, within-one
99.85 / 99.87 / 99.91 / 99.91, on n = 8,422 held-out crops from 1,653 films.

**But the bank named in the repo is the wrong one, and that error is ours, in two files.**

### 1.1 What bank it was measured on

| Reading | Source | Verdict |
|---|---|---|
| `films_all2_fov96_ctx` | `slurm/recurrent_head.sh` header; `tools/recurrent_order.py` restoration comment; `~/bench/model_registry.md` row M96; Inventory 5 | **Wrong** |
| `films_ann_fov96_ctx` | Inventory 4 (crop count), adversarial verdict 1 (timestamps + usage line + suite log) | **Correct** |

Three independent lines put it on `films_ann_fov96_ctx`:

1. **Crop count.** `~/spinesurg-ct-nnunet/logs/recurrent_40215812.out` reproduces all four
   accuracies line for line and prints `embedded 28032 crops`. 28,032 = 19,610 train + 8,422 val
   = `films_ann_fov96_ctx` exactly. `films_all2_fov96_ctx` is 41,297 + 8,422 = 49,719 and cannot
   be it.
2. **Timestamps.** `recurrent.json` 13:28:00; `~/films_all2_fov96_ctx/rung_0.npz` 14:43:15;
   `~/films_all2_fov96_ctx/runs/model_rung_0.pt` 15:45:40. Neither films_all2 input existed when
   the result was written. `~/films_ann_fov96_ctx/rung_0.npz` 08:24:09 and its
   `runs/model_rung_0.pt` 09:04:03 both predate it.
3. **The invocation.** `tools/recurrent_order.py` line 12 documents `--ctx ~/films_ann_fov96_ctx
   --model ~/films_ann_fov96_ctx/runs/model_rung_0.pt --out ~/bench/xr_fov/recurrent.json`, and
   `~/spinesurg-ct-nnunet/logs/level_dumps_40220452.out` line 15 shows the benchmark suite calling
   it that way.

**Two local files to correct:**
`<repo spinesurg-ct-nnunet 097933a>\slurm\recurrent_head.sh` (header) and
`<repo spinesurg-ct-nnunet 097933a>\tools\recurrent_order.py` (restoration
comment) both state "It was measured on films_all2_fov96_ctx". That comment is the origin of the
mis-attribution. It is not corrected in this document's scope.

The films_all2 run is a **separate, later file**: `~/bench/xr_fov/recurrent_all2.json`, `_meta.ctx
= films_all2_fov96_ctx`, `base_model = runs/model_rung_0.pt`, 40 epochs —
**98.84 / 99.13 / 99.42 / 99.38**. So "98.7 at three" is films_ann; films_all2's number at three
is 98.8, and at nine is 99.4, not 99.5.

### 1.2 What that bank actually contained

`films_ann_fov96_ctx` is CSXA cervical films (4,963) plus NHANES-II (543) and nothing else.
Per-level **training** crops, read from the npz `y` array:

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | T1 | T2–T11 | T12 | T13 | L1 | L2 | L3 | L4 | L5 | L6 | sacrum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **0** | 188 | 3665 | 3664 | 3661 | 3649 | 3579 | 21 | **0** | 132 | **0** | 183 | 186 | 186 | 186 | 186 | **0** | 124 |

Thirteen of 27 classes have zero training crops: C1, T2–T11, T13, L6. The validation split
(shared byte-for-byte with films_all2, 1,653 films, 8,422 crops) is C2 82, C3 1571, C4 1571,
C5 1570, C6 1564, C7 1542, T1 7, T12 59, L1–L5 82 each, sacrum 46 — csxa 7,440 / nhanes 982.
**7,900 of 8,422 target crops (93.8 %) are cervical; 7,818 are C3–C7.** Both banks' training
result files record `chance: 0.0714` = 1/14, which is the number of live classes, not 27.

### 1.3 Therefore

**What the number means.** On real lateral radiographs, at a field showing 3 or more vertebrae,
a BiGRU over frozen ResNet-18 embeddings names C2–C7 and L1–L5 correctly 98.7 % of the time, with
a per-region breakdown of cervical 99.05 (n = 7,900), thoracic 98.48 (n = 66), lumbar 92.20
(n = 410), sacrum 95.65 (n = 46), and per-source CSXA 99.27 (n = 7,440) vs NHANES 94.30 (n = 982).

**What it does not mean.** It is not a whole-spine result. Ten of the twelve thoracic levels are
absent from the bank in both training and validation, as are C1, T13 and L6. It cannot be set
beside the 78.7 % control on the 27-class allspine_v2 bank, for two reasons at once:
different class alphabet (14 live vs 27 live) **and** different measurement (run-level over a band
of 3–9 vertebrae vs single-crop). The task-matched single-crop numbers on the film banks are
96.95 % (films_ann rung 0), 97.46 % (films_all2 rung 0) and 98.98 % (films_all2 rung 1).

`~/model_night/recurrent_films_all2.json` already carries the warning in its own `_meta.note`:
"exact accuracy here is over the class alphabet OF THIS BANK … the two numbers are not comparable."

**The weights of that run do not exist.** Job 40215812 predates the `--save-head` option. It
reported four accuracies and discarded the GRU. No recurrent head weight file for
`films_ann_fov96_ctx` exists anywhere on the grid.

### 1.4 Is the recurrent head present in the current arms?

**Both answers are true and they are about different things.**

- **Not in the night arms.** `slurm/night_arm.sh` calls `train_level_backbone.py`, then
  `diag_level_model.py` and `eval_transitional.py`, and passes no `--head`. All twelve
  `~/model_night/diag_*.json` carry `"head": null`. Both evaluators *support* a head
  (`diag_level_model.py:72`, `eval_transitional.py:74` construct `RunLabeller` when `--head` is
  given); the arms did not pass one. So every accuracy in tonight's nine-arm table is single-crop.
- **Yes on the whole spine, as of 01:21 tonight, by a separate job.** `slurm/recurrent_head.sh`
  (job 40293790) trained a `RunLabeller` on `allspine_v2_fov96_ctx` rung 1 over frozen embeddings
  of `~/model_night/runs/model_r18_ce.pt`, saved the weights, and exited `RECURRENT_RC=0` at
  01:21:30. **This supersedes Inventory 5**, which read only the earlier failed attempt
  (job 40293533, 00:58, `load_state_dict` rejected the `enc.` key prefix) and concluded there was
  no whole-spine recurrent number. The 01:14 retry succeeded after `night_loadmodel.load_level_model`
  was introduced.
- **Not for allspine v1, v3 or v4.** `~/model_night/heads/` contains exactly two directories,
  `allspine_v2` and `films_all2`. `recurrent_allspine.json`, `recurrent_allspine_v3.json`,
  `recurrent_allspine_v4.json`, `heads/allspine_v3` and `heads/allspine_v4` do not exist.

### 1.5 Every recurrent / sequence run that has a number

| Result file | Bank | Rung | Base classifier | Ep | 3 vert | 5 | 7 | 9 | n (crops) | Classes live | Head saved |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `~/bench/xr_fov/recurrent.json` | films_ann_fov96_ctx | 0 | `films_ann/runs/model_rung_0.pt` | 30 | **98.69** | **99.13** | **99.41** | 99.48 | 8,422 | 14 of 27 | no |
| `~/bench/xr_fov/recurrent_dump.json` | films_ann_fov96_ctx | 0 | same | 30 | 98.86 | 99.13 | 99.24 | 99.61 | 8,422 | 14 of 27 | no |
| `~/bench/xr_fov/recurrent_all2.json` | films_all2_fov96_ctx | 0 | `films_all2/runs/model_rung_0.pt` | 40 | 98.84 | 99.13 | 99.42 | 99.38 | 8,422 | 14 of 27 | no |
| `~/model_night/recurrent_films_all2.json` | films_all2_fov96_ctx | 1 | `model_rung_1_aug2.pt` | 30 | 99.15 | 99.34 | 99.23 | 99.72 | 8,422 | 14 of 27 | **yes** |
| `~/model_night/recurrent_allspine_v2.json` | allspine_v2_fov96_ctx | 1 | `model_night/runs/model_r18_ce.pt` | 30 | **83.38** | **86.12** | **86.16** | **88.95** | 16,392 | 27 of 27 | **yes** |

Run-to-run spread on the same bank and seed is ~0.2 points (recurrent.json vs recurrent_dump.json),
which is GPU GRU nondeterminism, not a different bank.

**The whole-spine run-level gain now exists and is measured.** On `allspine_v2`, identical bank and
identical 16,392-crop val split: single-crop 78.74 % → recurrent 83.38 % at three vertebrae
(+4.64) and 88.95 % at nine (+10.21); within-one 97.14 / 97.78 / 97.99 / 98.01. A second sequence
head (`tools/stc_head.py`, architecture stated identical to `RunLabeller`) on the same bank reads
**85.93 % [85.49, 86.35] over 24,882 vertebrae** in bands of at most 7
(`~/model_night/logs/stc_stc_rand50_40294458.out`, 01:52:55). A four-seed frozen-head sweep on
allspine_v2 is at `~/track5/seed_{0,1,5,6}.json` (02:13–02:21).

### 1.6 The same model on the other surface

`~/FluoroCap/level_model_diag.json`, `films_all2` `model_rung_1_aug2.pt` plus the recurrent head:
**own-bank 98.7 % | 27-class CT renders 35.7 %** (300 renders read). That is the cost of changing
measurement surface, and the 35.7 is probably optimistic — that file carries no `renders_held_out`
key and no `renders_skipped_train` count, so it is not filtered against training cases.

Within that render read, T10 = 0.0 % (n = 280, confused to L1 147 / T12 97 / C3 15) and
T11 = 0.0 % (n = 295, confused to L1 174 / T12 84 / L2 10). **Those two classes have zero training
crops, so 0.0 % is forced.** But zero-crop starvation does not explain the render collapse, and the
tidy version of that story is wrong: on the same renders sacrum has 124 training crops and reads
95.7 % own-bank / 5.3 % renders; T12 has 132 crops, 94.9 % / 4.3 %; L1 has 3,843 crops,
85.4 % / 43.0 %; L2 has 3,847 crops and reads 7.4–9.9 % on the physics/cut render sets. Well-
populated classes collapse too. It is a film-to-DRR domain gap, and `tools/diag_level_model.py`
says so in its own docstring. Reproduced with the bookkeeping keys present in
`~/FluoroCap/cut_eval_films_*_v2.json` (`renders_held_out: true`, `renders_skipped_train: 0`):
T10 n 246 / T11 n 313 at 0.0 % (phys), T10 n 209 / T11 n 272 at 0.0 % (rare).

**One more correction to a phrase in circulation:** the film banks are not "thoracic-free".
films_all2 holds 154 thoracic training crops (T1 22, T12 132) and 66 thoracic val crops;
films_ann holds 153 (T1 21, T12 132). What they hold zero of is C1, T2–T11, T13 and L6.

---

## 2. Every dataset

### 2.1 Raw radiograph datasets

| Dataset | Path | Films | Annotation | Levels labellable | Level source | Feeds a bank? | Duplicate / synthetic |
|---|---|---|---|---|---|---|---|
| CSXA | `~/spine-detector/data/raw/csxa` | 4,963 lateral cervical png + json | 23 labelme shapes per film: 22 corners + C2 centroid | C2 (inferior corners only), C3–C7 | **annotated** — label strings name the level | yes, 13 banks, 24,815 crops | no |
| BUU-LSPINE v1 | `~/spine-detector/data/raw/buu_full/BUU-LSPINEv1` | 7,204 (AP 3,600 / LA 3,604) | endplate lines, 5 numbers per row; AP 10 rows, LA 11 | L1–L5 (+S1 superior endplate, lateral) | **inferred from row order** | yes, 16 banks; only the 3,603 laterals, 18,008 crops | 4 orphan files (3 csv no jpg, 1 jpg no csv) |
| NHANES-II annotated | `~/spine-detector/data/raw/nhanes_annotated` | 543 pickles (275 cervical + 268 lumbar, 364 subjects) | per-vertebra binary masks keyed by level name | C2–C7, T1, T12, L1–L5, S1 | **annotated** | yes, 10 banks, 6,270 crops | no. 159 GB for 543 films (float64 full-frame masks) |
| NHANES-II full | `~/spine-detector/data/raw/nhanes_full` | 17,073 tiff (9,667 C, 7,406 L) | none for 16,531 of them | — | — | only the 543 annotated reach a bank, of which 542 are films on disk | `.filelist.txt` lists 17,075 and the CDC serves L00452/L00456 as 0 bytes; annotated id L00452 has no TIFF, so 17,073 − 542 = 16,531 unannotated (job 40416535) |
| AASCE 2019 | `~/spine-detector/data/raw/aasce` | 579 jpg (481 train + 98 test), 251 patients | 4 corner landmarks × 17 vertebrae, + 3 Cobb angles | T1–L5 (17) | **inferred** — "most cranial = T1" convention | yes, `aasce_fov96_ctx` → allspine_v4 only, 7,769 crops | 457 of 481 converted; 24 failed |
| VinDr-SpineXR v1.0.0 | `~/spine-detector/data/raw/vindr/1.0.0` | 10,466 DICOM (8,389 train / 2,077 test) | **lesion boxes only** — 24,298 rows, 8 finding classes | **none natively** | **model pseudolabel** for 744 films | yes, 11 banks, 3,679 crops, all pseudolabelled | mixed region, mixed view (DICOM tags stripped) |
| buu_drive | `~/spine-detector/data/raw/buu_drive` | 5,495 images (10,990 files) | as buu_full | L1–L5 | inferred | **no** | **DUPLICATE — byte-identical subset of buu_full**, md5 over all 10,990 shared files, 0 mismatches. 9.3 GB |
| buu_2000 | `~/XRSpinoPelvic1K/data/BUU-LSPINE` (symlinked as `~/spine-detector/data/raw/buu_2000`) | 4,000 images | as buu_full | L1–L5 | inferred | **no** | **PARTIAL DUPLICATE** — all 4,000 JPEGs byte-identical, but 1,337 of 4,000 CSVs differ in column 5 (flag codes 5–10 vs 1–4/20–21). Same pixels, different annotation vintage |
| buu_v1 | `~/spine-detector/data/raw/buu_v1` | 38 images (77 files) | as buu_full | L1–L5 | inferred | **no** | **DUPLICATE** — all 77 byte-identical to buu_full. Download smoke test |
| mendeley_716 | `~/spine-detector/data/raw/mendeley_716` | **714** jpg (16 test, 494 train, 204 val) — not 716 | single-class boxes + 4 keypoints, 3,250 boxes | **none** | — | **no** | **near-certain BUU re-release** (filenames are BUU ids, re-encoded). `~/mendeley_drr` names levels by counting up from an assumed S1; 500 of its 584 films carry `duplicate_of` |
| lateral_236 | `~/spine-detector/data/raw/lateral_236` | 236 jpg | **none of any kind** | — | — | **no** | Real standing whole-spine laterals, skull base to proximal femora, 3,056 px wide × 5,100–8,800 tall, burned-in Chinese DICOM overlay. **The only real whole-spine lateral corpus on the grid, and it is doing nothing** |
| Spinal-AI2024 | `~/spine-detector/data/raw/spinal_ai2024` | **20,000** jpg (5 × 4,000) — not 20,001 | 4-point quads under a single category named "text" | **none** | — | **no** | **AI-GENERATED** (CurvNet iterative data engine, arXiv 2411.12604). Checklist has 20,440 rows, 440 never released. Top-1 similarity column names 52 real source films; the union over all six neighbour columns is **252** |
| cm_spine | `~/spine-detector/data/raw/cm_spine` | **0** | — | — | — | no | **EMPTY DIRECTORY, zero files.** Reported, not omitted |
| FluoroCap | `~/FluoroCap` | 12,106 figures / 20,700 panels decoded / 11,377 carrying a level | decoder placement (model / caption / mate / anchor / vlm) | all 27 tabulated | **not verified by anyone** | **no ctx bank** — no `fluorocap` source tag in any bank | Literature-mined. **The only store with real-image T13 (254) and L6 (338) panels.** 316 GB, of which 265 GB is `youtube/` (298,075 png) |

### 2.2 CT datasets

| Dataset | Path | Volumes | Label scheme | Levels expressible | Feeds | Notes |
|---|---|---|---|---|---|---|
| CTSpinoPelvic1K v10 | `~/data/CTSpinoPelvic1K` | 802 (`_ct` + `_label`), 227 GB | contiguous 0–68: C1–C7 1–7, T1–T12 8–19, L1–L6 20–25, sacrum 26, coccyx 27, T13 28, S1 29, hips 30/31, femurs 32/33, ribs 34–59, lumbar ribs 60/61, hardware 62–68 | **all 27** | `~/ctsp_drr` (801), `~/physics_drr` (2,430), `~/implant_ct`, `~/bench`; 21,100 crops in allspine_v4 | 769 normal / 17 sacralization / 14 lumbarization / 2 semi-sacralization; has_l6 18; lumbar rib 16; Castellvi IIIb 16, IIb 6, IV 4, IIa 4, Ib 2, IIIa 1. `0533_ct.nii.gz` is a truncated gzip → 801 of 802 render |
| VerSe (VerSeFusion) | `~/VerSeFusion` | 463 raw / 374 unified, 139 GB | VerSe-native: 1–7 C1–C7, 8–19 T1–T12, 20–24 L1–L5, 25 L6, 26 sacrum, 28 T13 | **all 27** | verse_drr, verse_drr_obl, verse_drr_obl2, verse_soft_drr, ctsp_drr_obl, ctsp_drr_obl2, physics_drr, physics_rare, implant_verse, vf_813 → 13 banks | **Dominant source: 374 scans → 74,217 of 173,722 allspine_v4 crops (43 %) under five tags.** Every T13 training crop in the bank comes from here |
| TotalSegmentator v201 | `~/data/TotalSegmentator` | 1,228 cases, 82 GB | 117 per-structure mask files; level names **are** the filenames | **25** — **no `vertebrae_T13`, no `vertebrae_L6`** | `~/physics_drr` (1,831), `~/implant_ts` (817), `~/vf_813/totalseg_raw`; 11,633 crops | **Cannot express either variant.** A 13th thoracic or 6th lumbar is silently absorbed into a neighbour |
| implant_ct | `~/implant_ct` | 1,518 triplets = 799 CTSP volumes × 2 variants, 427 GB | v10 ids | 27 | `~/physics_drr` under the `implant` prefix | **SYNTHETIC HARDWARE** on real volumes. Largest directory after the code repo |
| implant_verse | `~/implant_verse` | 1,119 triplets = 373 VerSe × 3 variants, 187 GB | VerSe-native | 27 | `~/physics_drr` | **SYNTHETIC HARDWARE.** A further copy of the same 374-scan VerSe population |
| implant_ts | `~/implant_ts` | 1,629 triplets = 817 TS cases × 2 variants, 39 GB | remapped to v10/VerSe-native | **25** | `~/physics_drr` | **SYNTHETIC HARDWARE.** Inherits TS's inability to express T13/L6 |
| vf_813 | `~/vf_813` | 374 imagesTr + labelsTr + totalseg_raw, 58 GB | **id→name map not in the directory** — no `dataset.json` | **not determined** | feeds no ctx bank directly; is the source of ctsp_drr_obl/obl2 | DERIVED nnU-Net staging: VerSe vertebrae + TS ribs, scapula to ignore. Observed ids {12–17, 25–30, 44}, which does not square with the standing note that C1–T9 map to ignore |

Combined implant_* contribution to allspine_v4: **6,231 crops** (C6 1, T4 1, T5 3, T6 27, T7 49,
T8 85, T9 120, T10 187, T11 286, T12 420, L1 580, L2 747, L3 893, L4 969, L5 827, L6 27). Inventory 3
did not split that by which implant bank a render came from.

### 2.3 Derived stores that are neither raw nor a crop bank

`~/films_drr` (36 GB, 9,109 real films in one ann/img format), `~/yolo_levels` (6.7 GB, the same
9,109 split 7,456/1,653), `~/XRSpinoPelvic1K/data/xrsp1k` (6,416 lateral DRRs of 822 cases with
endplate corners keyed by level name — **its `data/ct` and `data/labels` are dangling symlinks to
`CTSpinoPelvic1K/data/hf_export_v3`, which no longer exists**), `~/bench` (44 GB harness; `ct_by_case`
is 802 symlinks, `fov/crops` 31 GB, competitor outputs vista3d 5.8 GB / totalsegmentator 4.6 GB /
spineps 2.1 GB, **`gt/oneshot` is EMPTY**).

---

## 3. Every crop bank

42 banks (41 named `*_ctx` with content, plus `mv_bands`), 272 `rung_*.npz` files, 358.0 GB of rung
files / 363.3 GB including `meta.json` and `runs/`. A 43rd directory, `~/films_all2_fov128m_ctx`,
exists and is **empty** (created 2026-09-14, zero files). All 42 use the identical 27-class alphabet,
read from each `meta.json`; no bank uses a different label map.

**What a rung is** (`tools/make_context_crops.py`): rung *k* shows the target plus *k* neighbouring
vertebrae on each side (rung 0 = 1 vertebra, rung 1 = 3, rung 2 = 5, `full` = the whole film),
everything outside the union box zeroed, target rescaled to constant pixel height. **Every rung of a
bank holds the same rows.** The ladder is a masking ladder, not a data-size ladder — so in short-film
banks it saturates and the wider rungs are literally the same file.

Sorted by train crops descending. "Missing" = levels with zero **training** crops.

| Bank | Train crops | Val crops | Train films | Val films | Levels present | Levels MISSING (train) | Sources | Lineage / status |
|---|---|---|---|---|---|---|---|---|
| `allspine_v4_fov96_ctx` | 146,202 | 27,520 | 21,710 | 4,086 | **27** | none | physics_drr 7045 f, csxa 4963, buu_full 3603, verse_drr_obl2 2989, ctsp_drr_obl2 2511, physics_rare 1482, ctsp_drr 801, vindr 744, nhanes 543, nhanes_drr 543, aasce 457, verse_drr 374 | ← allspine_v3 + aasce. `leak_crops_prevented=0`. **The bank to keep.** Rarest: T13 110, L6 1,322 |
| `allspine_v3_fov96_ctx` | 139,572 | 26,381 | 21,320 | 4,019 | 27 | none | as v4 minus aasce | ← allspine_v2 + obl2 + vindr_fov96, `leak_crops_prevented=9194`. **REDUNDANT** — strict case subset of v4 (all 25,339 films) |
| `extra4_fov96_ctx` | 106,431 | **0** | 9,848 | 0 | 27 | none | buu_full, verse_drr_obl2, ctsp_drr_obl2, verse_drr_obl, ctsp_drr_obl, vindr | ← extra3 + obl2. **All-train pool, not trainable alone.** 9,847 of 9,848 films already in v3/v4. 30 GB redundant |
| `allspine_v2_fov96_ctx` | 89,568 | 16,392 | 16,168 | 2,927 | 27 | none | physics_drr, csxa, buu_full, physics_rare, ctsp_drr, nhanes, nhanes_drr, verse_drr | **REDUNDANT** — strict subset of v3/v4. Thin: T13 30, C1 533, L6 670. **This is the bank every model-night arm trains on** |
| `allspine_fov96_ctx` | 72,991 | 12,906 | 12,244 | 2,151 | 27 | none | csxa, buu_full, physics_drr 3568, ctsp_drr, nhanes, nhanes_drr, verse_drr | First all-spine bank. **REDUNDANT** — subset of v2/v3/v4. T13 **5**, L6 141, T4 224, T5 201 |
| `films_all3_fov96_ctx` | 69,727 | 8,422 | 10,950 | 1,653 | 27 | none | csxa, buu_full, verse_drr_obl 1494, ctsp_drr_obl 1256, vindr, nhanes | ← `.raw` (deleted) + extra3. Oblique DRRs fill the mid-thoracic hole in train, **but val is unchanged from films_all2 — val T2–T11 are all zero** |
| `obl2_fov96_ctx` | 56,314 | **0** | 5,500 | 0 | 27 | none | verse_drr_obl2 2989, ctsp_drr_obl2 2511 | **All-train augmentation pool.** Supersedes `obl` (holds 2,749 of its 2,750 render ids) |
| `extra3_fov96_ctx` | 50,117 | **0** | 7,097 | 0 | 27 | none | buu_full, verse_drr_obl, ctsp_drr_obl, vindr | ← extra_fov96 + obl_fov96. **All-train pool**, subset of extra4; 7,096 of 7,097 in v3/v4 |
| `films_all2_fov96_ctx` | 41,297 | 8,422 | 8,200 | 1,653 | **14** | **13: C1, T2–T11, T13, L6** | csxa 4963, buu_full 3603, vindr 744, nhanes 543 | ← `.raw` (deleted) + extra_fov96. Zero train/val film overlap. **Rungs 2,3,4,6,8,full are the same file six times** (3,577,265,632 B each) — 17.9 of 24.1 GB redundant |
| `films_all2_fov48_ctx` | 41,297 | 8,422 | 8,200 | 1,653 | 14 | same 13 | same | **48 px twin**, identical index (md5 502a239a). Rungs 3..full identical in size |
| `films_all_fov48_ctx` | 37,618 | 8,422 | 7,456 | 1,653 | 14 | same 13 | csxa, buu_full, nhanes | ← `.raw` (deleted) + buu_fov48. Predecessor of films_all2 without vindr. 3 rungs only |
| `films_all4_fov96_ctx` | 32,263 | 13,777 | 6,380 | 2,729 | 14 | same 13 | csxa, buu_full, nhanes | A **re-split** giving buu_full a real val share (2,729 val films). Same 9,109-film case set as films_all_fov48 |
| `obl_fov96_ctx` | 28,430 | **0** | 2,750 | 0 | 27 | none | verse_drr_obl 1494, ctsp_drr_obl 1256 | **REDUNDANT** — 2,749 of 2,750 ids are in obl2. 6.14 GB |
| `extra_fov96_ctx` | 21,687 | **0** | 4,347 | 0 | 12 | 15: C1, T2–T12, T13, L6, sacrum | buu_full, vindr | ← buu_fov96 + vindr_fov96. All-train. C2 and T1 hold **one crop each** |
| `extra_fov48_ctx` | 21,687 | **0** | 4,347 | 0 | 12 | same 15 | buu_full, vindr | 48 px twin, identical index |
| `films_all2_fov128_ctx` | 19,610 | 8,422 | 3,853 | 1,653 | 14 | same 13 | csxa, nhanes | **MISNAMED** — this is the films_ann index, no buu_full and no vindr, so lumbar train is 183–186/level. Rungs 1..full are 7 copies (2,411,071,406 B each), 14.5 of 16.5 GB redundant |
| `films_ann_fov96_ctx` | 19,610 | 8,422 | 3,853 | 1,653 | 14 | same 13 | csxa 4963, nhanes 543 | **THE HEADLINE BANK** (§1). Rungs 2..full all 1,877,620,575 B |
| `films_ann_fov48_ctx` | 19,610 | 8,422 | 3,853 | 1,653 | 14 | same 13 | csxa, nhanes | 48 px |
| `films_ann_fov48_scale_ctx` | 19,610 | 8,422 | 3,853 | 1,653 | 14 | same 13 | csxa, nhanes | **STRONGEST DUPLICATE IN THE INVENTORY** — all 8 rungs match `films_ann_fov48_ctx` in exact byte size and in md5 of 3 sampled 16 MiB blocks each. ~12.1 GB recoverable |
| `mv_bands` | 19,495 | 8,422 | 3,864 | 1,653 | 14 | same 13 | csxa 3313, buu_full 1850, nhanes 354 | **DIFFERENT SCHEMA** — npz keys X, L, sq, tpos, y, case, split, source. Multi-vertebra band bank for the sequence head. 3 rungs |
| `buu_fov96_ctx` | 18,008 | **0** | 3,603 | 0 | **5** | 22 — everything but L1–L5 | buu_full | All-train. Levels counting-inferred |
| `buu_fov48_ctx` | 18,008 | **0** | 3,603 | 0 | 5 | same 22 | buu_full | Identical index to fov96 (md5 7719d00f), different render |
| `buu_pair_fov48_ctx` | 12,581 | 5,392 | 2,520 | 1,080 | 5 | same 22 | buu_full 3600 | Paired AP+LAT, `paired=true`, `val_patients` not `val_cases`. 3 rungs |
| `m_fov96_ctx` | 9,405 | 2,304 | 941 | 234 | 27 | none | ctsp_drr 801, verse_drr 374 | DRR-only. T13 **5** |
| `m_mask22_scale_ctx` | 9,405 | 2,304 | 941 | 234 | 27 | none | ctsp_drr, verse_drr | mask mode 22 px. Same index as m_fov96 and merged_ctx |
| `merged_ctx` | 9,405 | 2,304 | 941 | 234 | 27 | none | ctsp_drr, verse_drr | **REDUNDANT** — `m_mask22_scale_ctx` minus the `scale` array (35,313 B smaller, sampled blocks match) |
| `aasce_fov96_ctx` | 6,783 | 986 | 399 | 58 | **17** | 10: C1–C7, T13, L6, sacrum | aasce 457 | Exactly T1–L5 on all 457 films by construction. **No READY marker.** The only content v4 adds over v3 |
| `verse_only_ctx_plus_nh` | 5,861 | 1,740 | 687 | 230 | 26 | sacrum | verse_drr 374, nhanes_drr 543 | ← verse_only_ctx + nhanes_split_ctx. **meta `val_cases` still lists only the 74 VerSe val cases** although 230 films are val |
| `vo_fov48_plus_nh_ctx` | 5,861 | 1,740 | 687 | 230 | 26 | sacrum | verse_drr, nhanes_drr | ← `.raw` (deleted) + nhanes_fov48_split. Identical index to the above; same meta discrepancy |
| `verse_ctx` | 5,779 | 1,468 | 542 | 134 | 27 | none | verse_drr 374, ctsp_drr 302 | Earliest all-level bank, 676 films. T13 **5** |
| `exp3_ctx_fluoro` | 4,026 | 709 | 901 | 157 | 14 | 13: C1–C7, T1–T4, T13, sacrum | exp3_fluoro 1058 | Fluoro preset. T5 has 1 crop, L6 has 6 |
| `exp3_ctx_radiograph` | 4,026 | 709 | 901 | 157 | 14 | same 13 | exp3_radiograph 1058 | Radiograph preset, same films/labels/split. **A controlled appearance pair, not redundancy** — sampled md5 differs |
| `vindr_fov96_ctx` | 3,679 | **0** | 744 | 0 | 12 | 15: C1, T2–T12, T13, L6, sacrum | vindr 744 | All-train. C3–C7 carry 3,373 of 3,679; C2 and T1 have **one crop each**. All labels are model pseudolabels |
| `vindr_fov48_ctx` | 3,679 | **0** | 744 | 0 | 12 | same 15 | vindr | Identical index |
| `verse_only_ctx` | 3,679 | 869 | 300 | 74 | 26 | sacrum | verse_drr 374 | mask mode 22 px. Contains a REPORT.md |
| `vo_fov48_ctx` | 3,679 | 869 | 300 | 74 | 26 | sacrum | verse_drr | Same crop list, genuinely different pixels (sampled md5 differs) |
| `vo_mask48_ctx` | 3,679 | 869 | 300 | 74 | 26 | sacrum | verse_drr | mask mode 48 px |
| `vsoft_fov48_ctx` | 3,679 | 869 | 300 | 74 | 26 | sacrum | **verse_soft_drr** 374 | **Not a duplicate** — soft-tissue DRR physics on the same crop list |
| `nhanes_fov48_split_ctx` | 2,182 | 871 | 387 | 156 | 13 | 14: C1, T2–T11, T13, L6, sacrum | nhanes_drr 543 | The split-bearing version |
| `nhanes_split_ctx` | 2,182 | 871 | 387 | 156 | 13 | same 14 | nhanes_drr | 22 px render, no `scale` array |
| `nhanes_fov_48_ctx` | **0** | 3,053 | 0 | 543 | — | all (no train) | nhanes_drr | **PURE HELD-OUT TEST BANK.** Same pixels as the split version, 392-byte size delta |
| `nhanes_ctx` | **0** | 3,053 | 0 | 543 | — | all (no train) | nhanes_drr | **PURE HELD-OUT TEST BANK**, mask mode 22 px. Val: C2 275, C3 273, C4 272, C5 268, C6 250, C7 158, T1 28, T12 191, L1–L5 266–268 |
| `films_all2_fov128m_ctx` | — | — | — | — | — | — | — | **EMPTY DIRECTORY.** No meta.json, no rung, no runs/ |

**Ten banks have zero validation crops** and are not trainable on their own: buu_fov48, buu_fov96,
vindr_fov48, vindr_fov96, extra_fov48, extra_fov96, extra3, extra4, obl, obl2.

**Containment chains.** `allspine_fov96 ⊂ allspine_v2 ⊂ allspine_v3 ⊂ allspine_v4` (14,395 →
19,095 → 25,339 → 25,796 films, each a strict case subset). `vindr ⊂ extra ⊂ extra3 ⊂ extra4`.
`buu ⊂ extra ⊂ films_all2 ⊂ films_all3 ⊂ allspine_v3 ⊂ allspine_v4`. `buu_pair (3,600) ⊂ buu (3,603)`.

**Merge lineage** (from `meta.json` `merged_from`). Every `.raw` parent has been **deleted** —
`films_all2_fov96_ctx.raw`, `films_all2_fov48_ctx.raw`, `films_all3_fov96_ctx.raw`,
`films_all_fov48_ctx.raw`, `vo_fov48_plus_nh_ctx.raw` do not exist on disk, so half of each of
those five merge lineages cannot be re-derived.

---

## 4. Every render directory

37 directories, 106 GB, 133,391 renders, 833,268 level-box instances. Per-level counts are exact —
every `ann/*.json` in every directory was read (3 of 12,929 in `fluorogen/synth_rare` are
unparseable and are excluded). Render dirs carry no train/val split.

**16 of 37 are consumed into a crop bank; 21 are not.**

| Render dir | Renders | Level instances | Distinct cases | View | Levels | T13 | L6 | Consumed into |
|---|---|---|---|---|---|---|---|---|
| `~/spinalai_drr` | 8,358 | 142,086 | **44 patient ids** (sim_000722 appears 1,270×) | AP | 17 (T1–L5) | 0 | 0 | **NO BANK.** AI-generated; ann says the T1–L5 naming is "ASSUMED… NOT verified" |
| `~/fluorogen/synth_rare` | 12,929 | 98,910 | 2,844 | AP 7,536 / lat 5,390 | 26 (no sacrum) | **86** | **1,763** | **NO BANK. The richest variant pool in the corpus and it is unused** |
| `~/anchor_drr` | 7,842 | 85,555 | 1,975 | AP 3,921 / lat 3,921 | 26 (sacrum is an anchor box, not a level) | 12 | 204 | **NO BANK** — it is the YOLO anchor detection set (8 classes, `data.yaml`). No `img/` dir |
| `~/lstv_flag/renders` | 9,612 | 67,614 | 801 | AP 4,806 / lat 4,806, 512 px PNG | 14 | 0 | 216 | **No ctx bank** — `lstv_flag_train.py` crops these itself |
| `~/physics_drr` | 7,045 | 53,805 | 3,029 | AP 4,052 / lat 2,993, 640 px | 26 (no sacrum) | 10 | 201 | allspine_fov96 (25,095 crops), v2/v3/v4 (37,556). **Biggest single contributor** |
| `~/films_drr` | 9,109 | 46,040 | 8,927 patients | lateral | 14 | **0** | **0** | films_ann_*, films_all*, buu_*, allspine_*, buu_pair. **REAL FILM.** csxa 4,963 + BUU lat 3,603 + nhanes 543 |
| `~/verse_drr_obl2` | 2,989 | 35,634 | 374 | oblique lateral, 8 poses | 26 | 48 | 399 | obl2 → extra4, allspine_v3/v4. Largest single crop contributor to v3/v4 |
| `~/lstv_flag/renders_verse` | 3,456 | 24,086 | 288 | AP 1,728 / lat 1,728, 6 poses | 18 | **62** | 564 | **No ctx bank** — read directly by `lstv_flag_train_v2.sh`. **Highest T13 of any LSTV set** |
| `~/cut_physics` | 3,000 | 20,640 | 1,154 | AP 1,736 / lat 1,264, 640 px | 15 | 0 | 76 | **NO BANK** — eval set only, via `diag_level_model.py` in `cut_drr2fluoro.sh` |
| `~/cut_physics_v2` | 3,000 | 20,640 | 1,154 | as v1 | 15 | 0 | 76 | **NO BANK.** Label-identical to v1 (pixels not compared) |
| `~/ctsp_drr_obl2` | 2,511 | 20,680 | **314 VerSe** | oblique lateral, 8 poses | 11 (T10–sacrum) | 48 | 399 | obl2 → extra4, allspine_v3/v4. **MISNAMED — VerSe, not CTSpinoPelvic1K** |
| `~/verse_drr_obl` | 1,494 | 18,064 | 374 | oblique lateral, 4 poses | 26 | 24 | 200 | obl → extra3 → films_all3 |
| `~/films_ap_drr` | 3,600 | 17,980 | 3,600 | AP | 5 (L1–L5) | 0 | 0 | buu_pair_fov48. **REAL FILM.** `level_source=inferred_from_position`, `test_eligible=false` |
| `~/cut_rare` | 1,482 | 11,542 | **81** | AP 879 / lat 603 | 24 | **43** | **845** | **NO BANK. One of the two richest variant pools and it is unused** |
| `~/cut_rare_v2` | 1,482 | 11,542 | 81 | as v1 | 24 | 43 | 845 | **NO BANK.** Label-identical to v1 |
| `~/physics_rare` | 1,482 | 11,542 | **81** | AP 879 / lat 603, 640 px | 24 | **43** | **845** | allspine_v2/v3/v4 (7,602 crops). **The ONLY variant-enriched render dir that reaches a bank** |
| `~/ctsp_drr_obl` | 1,256 | 10,366 | **314 VerSe** | oblique lateral, 4 poses | 11 | 24 | 200 | obl → extra3 → films_all3. **MISNAMED — VerSe** |
| `~/aasce_drr` | 457 | 7,769 | 457 | AP | 17 (T1–L5) | 0 | 0 | aasce_fov96 → allspine_v4. **REAL FILM** |
| `~/ctsp_drr` | 801 | 7,161 | 801 | lateral | 10 (T10–sacrum) | 0 | 18 | verse_ctx (2,699), merged/m_* (7,161), allspine_* (7,161) |
| `~/exp3_fluoro` | 1,058 | 7,066 | 120 | AP 603 / lat 455 | 14 | 0 | 9 | exp3_ctx_fluoro (4,735 crops) |
| `~/exp3_radiograph` | 1,058 | 7,066 | 120 | as fluoro | 14 | 0 | 9 | exp3_ctx_radiograph (4,735 crops) |
| `~/lstv_flag/renders_ctrl` | 644 | 5,312 | 161 | AP 322 / lat 322 | 14 | 0 | 1 | **No ctx bank.** The abstention control — fields are thoracic/thoracolumbar, framed away from L5–S1 |
| `~/verse_drr` | 374 | 4,548 | 374 | lateral, 1 per case | 26 (no sacrum) | **6** | **50** | verse_only_*, vo_*, verse_ctx, merged, m_*, allspine_*. **The only whole-spine substrate. Because there is one render per case, these counts are the count of distinct CT volumes carrying each level: 6 have a T13, 50 have an L6** |
| `~/verse_soft_drr` | 374 | 4,548 | 374 | lateral | 26 | 6 | 50 | vsoft_fov48_ctx only |
| `~/fluorogen/synth_rare_lowstrength` | 566 | 4,466 | 80 | AP 358 / lat 208 | 22 | 20 | 314 | **NO BANK** |
| `~/mendeley_drr` | 584 | 3,999 | 551 patients | lateral | 11 | 0 | 0 | **NO BANK.** 500 of 584 carry `duplicate_of` — 86 % is BUU already in films_drr. **REAL FILM** |
| `~/nhanes_drr` | 543 | 3,053 | 364 subjects | lateral | 13 | 0 | 0 | nhanes_*, films_ann_*, films_all*, allspine_*, vo_fov48_plus_nh. **REAL FILM, the only one whose levels are annotated** |
| `~/vindr_pseudo_drr` | 744 | 3,679 | 744 | mixed | 12 | 0 | 0 | vindr_fov48/96 → extra*, films_all2/3, allspine_v3/v4. **Levels are MODEL OUTPUT** (`pseudo_model` field) |
| `~/vindr_det_drr` | 2,328 | 12,823 | 2,328 | mixed | **0** | 0 | 0 | **NO BANK** — every instance is `name='unknown'`, `level_source='none'`. Intermediate: `pseudolabel_films.py` reads it |
| `~/lstv_eval/renders60` | 60 | 405 | **11** | AP 33 / lat 27 | 17 | 6 | 30 | **NO BANK.** Built to evaluate `tools/level_prototype.py`. No `img/`; 60 PNG in `in/` |
| `~/postop_render` | 45 | 292 | 15 | AP 25 / lat 20 | 13 | 0 | 6 | **NO BANK.** No consumer found in the repo |
| `~/lstv_flag/smoke` | 36 | 262 | 3 | — | 13 | 0 | 0 | Smoke test. Not consumed |
| `~/films_smoke` | 3 | 15 | 3 | — | 5 | 0 | 0 | Smoke test. Not consumed |
| `~/physics_smoke` | 14 | 108 | 10 | — | 14 | 0 | 3 | Smoke test. Not consumed |
| `~/render_smoke/fluoro` | 9 | 72 | 3 | — | 13 | 0 | 0 | Smoke test. Not consumed |
| `~/render_smoke/radiograph` | 9 | 72 | 3 | — | 13 | 0 | 0 | Smoke test. Label-identical to the fluoro twin |
| `~/fluorogen/synth_v1` | **0** | **0** | 0 | — | 0 | 0 | 0 | **EMPTY.** `ann/`, `img/` and `preview/` all exist and all hold zero files. The first FluoroGen run produced nothing |

### 4.1 The variant-class holdings, stated plainly

T13 appears in 15 render directories (6 to 86 instances each) and L6 in 24. **But every T13
instance in the entire corpus traces to the 6 VerSe volumes that carry one, and the L6 instances
trace to ~50 VerSe volumes plus 18 CTSpinoPelvic1K records — about 68 distinct CT scans.**
Everything above that is re-rendering.

**Zero T13 and zero L6 instances exist on any real radiograph anywhere.** `films_drr`,
`films_ap_drr`, `nhanes_drr`, `mendeley_drr`, `aasce_drr`, `vindr_det_drr` and `vindr_pseudo_drr`
are all T13 = 0, L6 = 0. Every variant-class example the project has is CT-derived or synthetic.

**The two richest variant pools are in no bank:** `fluorogen/synth_rare` (T13 86, L6 1,763) and
`cut_rare` / `cut_rare_v2` (T13 43, L6 845 each). `physics_rare` is the only variant-enriched render
directory that reaches a crop bank.

The only **real-image** T13 and L6 anywhere are FluoroCap panels: T13 254, L6 338 — and those are
decoder placements, ~85 % of them the level model's own output fed back (T13 214 of 254 by model,
L6 279 of 338 by model), not verified labels.

### 4.2 Two naming traps

1. **`ctsp_drr_obl` and `ctsp_drr_obl2` are not CTSpinoPelvic1K.** Their source is `~/vf_813`,
   whose `labelsTr` is 374 files all named `VERSE_*.nii.gz`; every case id is `CTSP_VERSE_gl###_p#`;
   all 314 of their case ids intersect `verse_drr`'s 374 exactly (`comm -12` = 314). The "CTSP"
   prefix denotes the *label scheme*, not the dataset. Their T10..sacrum profile is the ds813 scheme
   dropping C1–T9 and adding sacrum, not a CT field of view. **So the 20,680 crops tagged
   `source="ctsp_drr_obl2"` in allspine_v3/v4 are VerSe.**
2. **`spinalai_drr`'s 8,358 films are 44 synthetic identities.** `sim_000722` alone appears 1,270
   times, and the ann itself states the T1–L5 naming is assumed and not verified.

---

## 5. Every model

~200 project `.pt` files under `$HOME` (234 total including stock YOLO downloads and two gcc
testsuite fixtures named `g++.pt`). The content-addressed registry `~/model_registry/registry.jsonl`
has 51 lines but only **25 distinct models** — `orientation_net_v2` is re-logged 17 times by a
20-minute mirror-sync cron.

### 5.1 Recurrent / sequence heads

| Model | Path | Bank | Rung | Base classifier | Arch | Loss | Ep | Date | Result file | Headline |
|---|---|---|---|---|---|---|---|---|---|---|
| **films_ann headline head** | **DOES NOT EXIST** | films_ann_fov96_ctx | 0 | `films_ann/runs/model_rung_0.pt` (a8bb9bb4) | RunLabeller BiGRU 2×256 | CE | 30 | 2026-09-13 13:28 | `~/bench/xr_fov/recurrent.json` | **98.69/99.13/99.41/99.48.** Weights never saved |
| `recurrent_head_films_all2_fov96_ctx.pt` **(SHIPPED)** | `~/FluoroCap/` | films_all2_fov96_ctx | 0 | `model_rung_0.pt` (c2e15f8f, M15) | Linear(512→256)+GELU+2-layer BiGRU(256, drop 0.2)+Linear(512→27) | CE all positions, ignore −100, 10 % embedding dropout | 30, all lengths 1..9 jointly | 2026-09-13 21:47 | `~/FluoroCap/infer_summary.json` | no isolated accuracy. sha d0ab6d5e. M96. **Not in `~/model_registry`** |
| `level_id_service/weights/recurrent_head.pt` | `~/level_id_service/weights/` | films_all2_fov96_ctx | 0 | same | same | CE | 30 | 2026-09-14 07:14 | `~/level_id_service/weights/registry.json` | Byte-identical to the above (d0ab6d5e). Deploy copy |
| `..._3654e9ba_r1.pt` | `~/FluoroCap/` | films_all2 | 1 | `model_rung_1.pt` (M18, 0.9898) | BiGRU 2×256 | CE | 30 | 2026-09-14 10:02 | **none** | no isolated result |
| `..._d081b4ab_r1.pt` **(REGISTERED)** | `~/FluoroCap/` + `~/model_registry/f4ec9180c718ea8b/` | films_all2 | 1 | `model_rung_1_aug2.pt` (M19, 0.9873) | BiGRU 2×256 | CE | 30 | 2026-09-14 10:07 | `~/model_registry/registry.jsonl` | **registry metrics block is EMPTY `{}`.** The only recurrent head in the registry |
| `..._de9a5dfe_r2.pt` | `~/FluoroCap/` | films_all2 | 2 | `model_rung_2.pt` (M21, 0.9899) | BiGRU 2×256 | CE | 30 | 2026-09-14 10:12 | **none** | — |
| `..._964e17f1_r2.pt` | `~/FluoroCap/` | films_all2 | 2 | `model_rung_2_aug2.pt` (M22, 0.9868) | BiGRU 2×256 | CE | 30 | 2026-09-14 10:17 | **none** | — |
| `..._allspine_v2_00e84a90_r1.pt` | `~/FluoroCap/` | **allspine_v2** | 1 | `allspine_v2/runs/model_rung_1_aug2.pt` (0.7878) | BiGRU 2×256 | CE | 30 | 2026-09-15 08:28 | `~/FluoroCap/consistency_hires_allspine_v2_r2.json` | no isolated accuracy; used in the hires decode pass |
| `heads/films_all2/head_k{1,2,3,4}.pt` | `~/model_night/heads/films_all2/` | films_all2 | 1 | `model_rung_1_aug2.pt` | RunLabeller d_in 512, hidden 256, 27 cls | CE + 10 % embedding dropout | 30 each | 2026-09-16 00:59–01:00 | `~/model_night/recurrent_films_all2.json` | **99.15 / 99.34 / 99.23 / 99.72**, n 8,422. Job 40293532. First time the script ever saved its weights |
| `heads/allspine_v2/head_k{1,2,3,4}.pt` | `~/model_night/heads/allspine_v2/` | **allspine_v2** | 1 | `model_night/runs/model_r18_ce.pt` | RunLabeller, 27 cls | CE + 10 % dropout | 30 each | 2026-09-16 01:18–01:21 | `~/model_night/recurrent_allspine_v2.json` | **83.38 / 86.12 / 86.16 / 88.95**, n 16,392. Job 40293790 |
| `stc_head` (allspine_v2) | weights not enumerated | allspine_v2 | 1 | `model_r18_ce.pt` | stated identical to RunLabeller (`tools/stc_head.py:225`) | CE | — | 2026-09-16 01:52 | `~/model_night/logs/stc_stc_rand50_40294458.out` | **85.93 % [85.49, 86.35]** over 24,882 vertebrae, bands ≤7 |
| four-seed frozen sweep | — | allspine_v2 | 1 | `model_r18_ce.pt` | RunLabeller | CE | — | 2026-09-16 02:13–02:21 | `~/track5/seed_{0,1,5,6}.json` | not transcribed |

**No recurrent head exists for:** allspine_fov96_ctx, allspine_v3, allspine_v4, films_ann_fov96_ctx,
films_all4, films_all2_fov48/fov128, films_ann_fov48, merged_ctx, verse_ctx, verse_only_ctx,
verse_only_ctx_plus_nh, vo_*/vsoft_*, m_fov96_ctx, buu_pair_fov48_ctx, mv_bands.

### 5.2 Level classifiers (2-D, single-crop)

All ResNet-18 unless stated, ImageNet init, 27-class head, CE unless stated.

| Model | Path | Bank | Rung | Loss / variant | Ep | Date | Result file | Held-out exact |
|---|---|---|---|---|---|---|---|---|
| `r18_ce` **(model-night CONTROL)** | `~/model_night/runs/model_r18_ce.pt` | allspine_v2 | 1 | ce, 2-ch marker stem, 320 px | 40 (best 39) | 2026-09-16 00:06 | `runs/result_r18_ce.json` + `~/model_night/diag_r18_ce.json` | **78.74 % [78.11, 79.37]**, n 16,392; renders 64.2 % |
| `r18_corn` | `~/model_night/runs/model_r18_corn.pt` | allspine_v2 | 1 | CORN cumulative-link | 40 (best 33) | 2026-09-16 00:07 | `result_r18_corn.json` | 78.44 % [77.8, 79.1]; renders 63.0 % |
| `r18_ordfocal` | `~/model_night/runs/model_r18_ordfocal.pt` | allspine_v2 | 1 | ordinal focal | 40 (best 39) | 2026-09-16 00:05 | `result_r18_ordfocal.json` | 75.05 % [74.4, 75.7]; renders 58.9 % |
| `r18_ce_8ep` | `~/model_night/runs/model_r18_ce_8ep.pt` | allspine_v2 | 1 | ce, matched budget for the ViT arms | 8 (best 7) | 2026-09-15 23:19 | `result_r18_ce_8ep.json` | 71.30 % [70.6, 72.0]; renders 53.4 % |
| `r18_frozen` | `~/model_night/runs/model_r18_frozen.pt` | allspine_v2 | 1 | frozen 3-ch ImageNet encoder, marker-weighted pooling, linear probe | 40 (best 37) | 2026-09-15 23:20 | `result_r18_frozen.json` | 30.12 % [29.4, 30.8]; renders 16.7 % |
| `r18_ordfocal_v3` | `~/model_night/runs/model_r18_ordfocal_v3.pt` | **allspine_v3** | 1 | ordinal focal | 40 (best 38) | 2026-09-16 00:51 | `result_r18_ordfocal_v3.json` | 74.83 % [74.30, 75.35], n 26,381; renders 62.1 %. **The only trained model on allspine_v3** |
| `allspine_v2_r1` | `~/allspine_v2_fov96_ctx/runs/model_rung_1_aug2.pt` | allspine_v2 | 1 | ce, augment tier 2, lr 3e-4 | 40 | 2026-09-15 08:11 | `runs/result_rung_1_aug2.json` | **78.78 %**, n 16,392. **The historical baseline quoted in every roll-up** |
| `allspine_v1_rung1_aug2` | `~/allspine_fov96_ctx/runs/model_rung_1_aug2_aug2.pt` | allspine_fov96 | 1 | ce, aug2 | 40 | 2026-09-14 19:45 | `runs/result_rung_1_aug2_aug2.json` | 80.16 %, n 12,906. **`model_rung_1_aug2.pt` in that dir is a 25-byte SYMLINK to this file — against the standing rule** |
| films_all2 ladder (9 files) | `~/films_all2_fov96_ctx/runs/model_rung_{0,1,2}{,_aug2,_aug3}.pt` | films_all2 | 0/1/2 | ce; aug2/aug3 tiers | 40 / 60 | 2026-09-13→14 | `~/bench/model_registry.csv` M15–M23 | plain 97.46 / 98.98 / 98.99; aug2 95.96 / 98.73 / 98.68; aug3 86.24 / 94.56 / 96.34. n 8,422 |
| films_ann ladder (6 files) | `~/films_ann_fov96_ctx/runs/model_rung_{0,1,2}{,_supcon}.pt` | **films_ann** | 0/1/2 | ce; 3 arms add SupCon warmup | 40 | 2026-09-13 06:05–09:25 | M33–M38 | 96.95 / 98.63 / 98.78; supcon 97.02 / 98.77 / 98.86. **`model_rung_0.pt` (a8bb9bb4, M33) is the base of the headline result.** SupCon bought ~0.1 pt |
| films_all_fov48 ladder | `~/films_all_fov48_ctx/runs/model_rung_{0,1,2}.pt` | films_all_fov48 | 0/1/2 | ce, 48 px | 40 | 2026-09-13 | M25–M27 | 97.60 / 98.94 / **99.38** — the highest held-out exact of all 95 bench-registered classifiers |
| films_all2_fov48 ladder | `~/films_all2_fov48_ctx/runs/model_rung_{0,1,2}.pt` | films_all2_fov48 | 0/1/2 | ce, 48 px | 40 | 2026-09-13 | M12–M14 | 97.82 / 98.85 / 99.25 |
| films_ann_fov48 ladder | `~/films_ann_fov48_ctx/runs/model_rung_{0,1,2}.pt` | films_ann_fov48 | 0/1/2 | ce, 48 px | 40 | 2026-09-13 | M28–M30 | 96.70 / 98.79 / 99.06 |
| films_ann_fov48_scale | `~/films_ann_fov48_scale_ctx/runs/model_rung_{0,2}_scale.pt` | — | 0/2 | ce + scale channel | 40 | 2026-09-13 | M31–M32 | 96.41 / 98.99. No rung 1 trained |
| films_all2_fov128 | `~/films_all2_fov128_ctx/runs/model_rung_{0,1}_t128.pt` | — | 0/1 | ce, 128 px target | 40 | 2026-09-13 | M10–M11 | 96.82 / 98.71 |
| films_all4 | `~/films_all4_fov96_ctx/runs/model_rung_{0,1,2}_aug3.pt` | films_all4 | 0/1/2 | ce, aug3 | 60 | 2026-09-13→14 | M24 (rung_0 only) | rung_0 82.01 %. **rung_1/2 have no bench row — written 04:53, after the csv was generated at 03:06** |
| buu_pair ladder (9 files) | `~/buu_pair_fov48_ctx/runs/model_rung_{0,1,2}{,_ap,_both}.pt` | buu_pair | 0/1/2 | ce; `_both` dual-view | 40 | 2026-09-12 | M01–M09 | lat 88.67/93.53/95.25; ap 90.43/94.36/95.55; both 92.12/95.18/96.16. **Unseeded** |
| merged_ctx ladder (12) | `~/merged_ctx/runs/model_rung_{0,1,2,3,4,6,8,full}.pt` + convnext_tiny ×2, resnet50 ×2 | merged_ctx | all | ce | 40 | 2026-09-12 | M45–M56 | r18 73.70 → 91.84 monotone; r50 rung2 88.45; **convnext_tiny rung0 9.64 — failed to train at lr 3e-4** |
| verse_ctx ladder (13) | `~/verse_ctx/runs/...` | verse_ctx | all | ce | 40 | 2026-09-12 | M57–M69 | r18 70.57 → 88.76; **convnext_tiny at lr 3e-4 = 7.97 = exactly chance**, at lr 1e-4 = 73.37; r50 71.05 / 86.04 |
| verse_only ladder (12) | `~/verse_only_ctx/runs/...` incl. `_ep80`, `_lr1e3`, `_noaug` | verse_only | all | ce | 40 / 80 | 2026-09-12 | M70–M81 | 63.52 → 82.74; **`_noaug` 65.48 BEATS the augmented baseline 63.52**; lr1e3 60.18 worst |
| verse_only_plus_nh (5) | `~/verse_only_ctx_plus_nh/runs/model_rung_{0,1,2,4,full}.pt` | — | — | ce | not recorded | 2026-09-13 | `runs/result_rung_*.json` (5 files) | **NO BENCH ROW, jsons not opened — no number** |
| vo_fov48 (5) | `~/vo_fov48_ctx/runs/...` | vo_fov48 | 0–3, full | ce, 48 px | 40 | 2026-09-12 | M82–M86 | 72.61 / 80.09 / 82.85 / 85.04 / 85.62 |
| vo_fov48_plus_nh (4) | `~/vo_fov48_plus_nh_ctx/runs/...` | — | 0–3 | ce, 48 px | 40 | 2026-09-12 | M87–M90 | 77.18 / 86.38 / 88.51 / 90.11. **NHANES buys 5–8 pt at every rung** |
| vo_mask48 (3) | `~/vo_mask48_ctx/runs/...` | — | 0–2 | ce, masked | 40 | 2026-09-12 | M91–M93 | 68.58 / 76.75 / 79.86. Masking costs ~4 pt |
| vsoft_fov48 (2) | `~/vsoft_fov48_ctx/runs/model_rung_{0,2}.pt` | — | 0, 2 | ce, soft-tissue DRR | 40 | 2026-09-12 | M94–M95 | 63.29 / 79.75 |
| m_fov96 (4) | `~/m_fov96_ctx/runs/...` | m_fov96 | 0–3 | ce | 40 | 2026-09-13 | M39–M42 | 82.77 / 89.76 / 89.45 / 89.54 — plateaus after rung 1 |
| m_mask22_scale (2) | `~/m_mask22_scale_ctx/runs/model_rung_{0,2}_scale.pt` | — | 0, 2 | ce + scale ch | 40 | 2026-09-13 | M43–M44 | 73.13 / 86.72 |
| `exp3_radiograph` | `~/model_night/runs/model_exp3_radiograph.pt` | exp3_ctx_radiograph | 1 | ce | 40 (best 33) | 2026-09-15 23:18 | `result_exp3_radiograph.json` | own-render 57.69 %; real panels 10.8 % |
| `exp3_fluoro` | `~/model_night/runs/model_exp3_fluoro.pt` | exp3_ctx_fluoro | 1 | ce | 40 (best 29) | 2026-09-15 23:18 | `result_exp3_fluoro.json` | own-render 54.72 %; real panels 10.9 % |
| `fluoro_ft_v3` | `~/FluoroCap/finetune_v3` (a **2,147 B manifest**, not a weight file) | allspine_v2 + real fluoro corpus | 1 | ce, transitional upweight 5.0 | 12 | 2026-09-15 20:52 | `~/model_registry/registry.jsonl` | film_val 76.16 %, **FLUORO HOLDOUT 8.62 %**, kept_frac 79.6 % |
| `smoke2` | `~/model_night/smoke/model_smoke2.pt` | real corpus crops, init allspine_v2 | 1 | ce | best ep 0 | 2026-09-15 23:26 | `smoke/result_smoke2.json` | corpus holdout within-1 32.1 %. A smoke test |
| `level_id_service/weights/level_model.pt` | `~/level_id_service/weights/` | films_all2 | 1 | ce, aug tier 2 | 60 | 2026-09-14 07:14 | `weights/registry.json` | exact_val 0.9873 (M19). Identical sha to `films_all2/runs/model_rung_1_aug2.pt` (d081b4ab) |

### 5.3 Detectors

| Model | Path | Data | Arch | Ep | Date | Result file | Headline (recall/mAP — **never an accuracy**) |
|---|---|---|---|---|---|---|---|
| `detect_v1` | `~/spine-detector/runs/pose/runs/detect_v1/weights/best.pt` | `data/yolo` | yolo11m-pose, imgsz 1024 | 120 req / 111 rows | 2026-08-30 | `results.csv` | box mAP50 0.9803, mAP50-95 0.7705; pose mAP50 0.9225. M97 |
| `detect_v2` | `~/spine-detector/runs/pose/runs/detect_v2/weights/best.pt` | `data/yolo_v2` | yolo11m-pose | 120 | 2026-09-08 | `results.csv` | box mAP50 **0.9907**, mAP50-95 0.8111; pose mAP50 0.9765. M98. **The memory note's "AP50 0.970 / PCK@0.1 0.812" is a different quantity — do not conflate** |
| `detect_v3` | `~/spine-detector/runs/pose/runs/pose/runs/detect_v3/weights/best.pt` | `data/yolo_v3` | yolo11m-pose | 200 req / 108 rows | 2026-09-11 | `results.csv` | box mAP50 0.9940, mAP50-95 0.8542; pose mAP50 0.9921. M99 |
| `detect_v4` | `~/spine-detector/runs/pose/runs/pose/runs/detect_v4/weights/best.pt` | `data/yolo_v3` (same as v3) | yolo11m-pose | 200 req / 156 rows | 2026-09-11 | `results.csv` | box mAP50 0.9936, mAP50-95 0.8587. M100. 48 more epochs on identical data bought 0.4 pt of mAP50-95 |
| `detector_v5z_final` | `~/FluoroCap/detect_v5z_final_best.pt` | `data/yolo_v4z` | yolo11m-pose ft from detect_v3 | 60 | 2026-09-14 09:33 | `detect_v5z/results.csv` | box mAP50 0.9940; pose mAP50 0.9929, mAP50-95 0.9852. M101, registered |
| `detector_v5z_epoch25` **(SHIPPED)** | `~/FluoroCap/detect_v5z_epoch25_best.pt` (168 MB, optimizer state retained) | `data/yolo_v4z` | yolo11m-pose | 25 of 60 | 2026-09-14 04:32 | `~/level_id_service/weights/registry.json` | **An intermediate epoch was shipped in preference to the final one.** Copied to `level_id_service/weights/detector.pt` |
| `detect_v5z_latest` / `_epoch4` | `~/FluoroCap/detect_v5z_{latest,epoch4}_best.pt` | `data/yolo_v4z` | yolo11m-pose | 4 / "latest" | 2026-09-14 | **none** | Intermediate snapshots pulled off the running job. Not registered |
| `detector_v6f` | `~/FluoroCap/detect_v6f_best.pt` | `data/yolo_v6f` | yolo11m-pose ft from v5z_epoch25 | 30 | 2026-09-14 17:24 | `detect_v6f/results.csv`, `consistency_v6f_anchor.json` | box mAP50 0.9931; pose mAP50 0.9918, mAP50-95 0.9857. **Newest; not the one in level_id_service** |
| `anchor_detector_v1` | `~/FluoroCap/anchor_det_v1.pt` | `~/anchor_drr/data.yaml` | YOLO11m detection, 8 anchor classes | 40 | 2026-09-14 17:50 | `anchor_v1/results.csv`, `anchor_summary_v03_anchor.json` | mAP50 0.7572, mAP50-95 0.6383, P 0.8615, R 0.7206 |
| `yolo_levels` level-as-class | `~/yolo_levels/runs/levels/weights/best.pt` | `~/yolo_levels` | YOLO11m detection, 27 level classes | 60 | 2026-09-13 | `~/bench/xr_fov/table.md` | 64.0 % @1 vertebra, 93.7 % @3, 98.3 % @5 (lumbar 43.4/83.9/90.2). M102 |
| XRSpinoPelvic1K yolo_exp sweep (7 runs, 14 files) | `~/XRSpinoPelvic1K/data/runs/yolo_exp/*/weights/` | XRSpinoPelvic1K | YOLOv8l-pose, YOLO11n-pose at 640/1024/1280 | — | 2026-08-13 | **results.csv not opened** | **NO NUMBER READ.** Belongs to the X-ray paper |

### 5.4 Orientation

| Model | Path | Data | Ep | Date | Result file | Headline |
|---|---|---|---|---|---|---|
| `orientation_net` | `~/FluoroCap/orientation_net.pt` | synthetic rotations, 11,007 train / 1,370 val | 6 | 2026-09-14 05:49 | `orientation_net.json` | **99.93 %** val (1 error in 1,370) |
| `orientation_net_v2` | `~/FluoroCap/orientation_net_v2.pt` | 2,991 classifier-verified **real** panels, 2,840 train / 120 val | 8 | 2026-09-15 15:39 | `orientation_net_v2.json` | **61.67 % on n = 120.** The gap that matters: 99.9 % synthetic → 61.7 % real |

### 5.5 Hardware detectors

| Model | Path | Data | Ep | Date | Result file | Headline |
|---|---|---|---|---|---|---|
| `hardware_detector_v1` | `~/FluoroCap/hardware_det_v1.pt` | `data/yolo_hw` | 40 | 2026-09-14 06:10 | `hw_v1/results.csv` | mAP50 0.4102, mAP50-95 0.1256 |
| `hardware_detector_v2` | `~/FluoroCap/hardware_det_v2.pt` | `data/yolo_hw_fluoro`, ft from v1 | 40 req / 29 rows | 2026-09-14 07:03 | `hw_v2/results.csv`, `hardware_constraints_stats.json` | mAP50 0.3086 — **WORSE than v1**. Whether that is a val-set domain shift or a regression could not be determined |

### 5.6 Binary flags

| Model | Path | Training set | Positives | Ep | Date | Result file | Headline AUC |
|---|---|---|---|---|---|---|---|
| `lstv_flag_v1` | `~/lstv_flag/models/lstv_flag_v1.pt` | 9,612 renders of 801 CTSP cases | 34 / 801 | 12, seed 11 | 2026-09-15 20:25 | `oof_lstv_both.csv`, `LSTV_FLAG_RESULTS.md` | **0.5775 [0.4804, 0.6690] — the interval contains 0.5.** Sens 0.853 / spec 0.248, PPV 0.048 |
| `lstv_flag_v2` | `~/lstv_flag/models/lstv_flag_v2.pt` | 12,840 renders of 1,070 patients (CTSP 801 + VerSe 269) | 125 | 12 | 2026-09-15 21:19 | `oof_lstv_both_v2.csv` | **VerSe 0.7237 [0.658, 0.783]; CTSP 0.5351 [0.446, 0.627].** Sidecar carries `do_not_pool_cohorts` |
| `tltv_flag_v1` | `~/lstv_flag/models/tltv_flag_v1.pt` | 9,612 renders, 801 patients | 16 | 12 | 2026-09-15 20:23 | `oof_tltv_both.csv` | 0.5838 [0.4377, 0.7124] — contains 0.5. PPV 0.024 |
| `tltv_flag_v2` | `~/lstv_flag/models/tltv_flag_v2.pt` | 12,936 renders, 1,078 patients | 91 | 12 | 2026-09-15 21:19 | `oof_tltv_both_v2.csv` | VerSe 0.5103 [0.438, 0.580]; CTSP 0.5783 [0.405, 0.747]. **Extra VerSe data did NOT help** |
| `sex_control_v1` **(POSITIVE CONTROL)** | `~/lstv_flag/models/sex_control_v1.pt` | same 9,612 renders | 344 | 8 | 2026-09-15 22:14 | `oof_control_sex.csv` | **0.951 [0.935, 0.966] on renders; 0.829 [0.816, 0.843] on 3,600 real BUU laterals.** Sidecar: "Do not wire into level_prototype as a flag" |

### 5.7 Other

| Model | Path | Kind | Date | Result file | Headline |
|---|---|---|---|---|---|
| mv_bands multi-view identifier (3) | `~/mv_bands/runs/model_mv_rung_{0,1,2}.pt` (132 MB) | competitor paradigm re-implemented | 2026-09-13 | `runs/result_mv_rung_*.json` | 95.37 / 98.05 / 97.57. **Same 8,422-crop val set as the recurrent head.** Sequence loss adds 0.05 pt at rung 1 and *hurts* at rung 2 |
| `panel_classifier` (+ `_v1_filmsonly`, `_v2`) | `~/FluoroCap/` (89.5 MB) | modality 3-class + view 2-class heads | 2026-09-14 | `classifier_report{,_v1,_v2}.json` | v1 modality 96.70 (n 1,999) / view 98.63 (n 800); v2 93.09 / 99.50. **Current report contains only `{"note": "loaded …"}`** for 58,888 panels |
| `region_classifier` | `~/FluoroCap/region_classifier.pt` | 4-way region | 2026-09-14 03:37 | `region_classifier_report.json` | OOF 63.16 % over n = 2,815. Thoracic 214/478, **sacral 17/135**. **No `.arch.json` — architecture unverified** |
| `cut_drr2fluoro_G` (v1) | `~/cut_v1/G_last.pt` + 6 epoch ckpts | CUT generator 256 px | 2026-09-15 07:23 | `~/FluoroCap/cut_eval_*.json` | **Registered TWICE under the same name with different shas** (550bea55 backfill, then 28d04f80) — the second overwrote the alias |
| `cut_drr2fluoro_G_v2` | `~/cut_v2/G_last.pt` | CUT generator; target = 2,376 verified panels | 2026-09-15 10:39 | `cut_eval_*_v2.json` | target set 6.5× smaller than v1's but verified |
| `fluorogen_lora_v1` | `~/fluorogen/lora_v1/pytorch_lora_weights.safetensors` | SDXL LoRA + canny ControlNet | 2026-09-14 12:06 | **none** | Outputs in `synth_v1` (empty), `synth_rare`, `synth_rare_lowstrength` |
| contour model (+ `ctr_smoke`) | `~/contours/runs/model_contour.pt` (1.55 MB) | arch/loss/epochs **not recorded** | 2026-09-13 00:39 | `runs/result_contour.json` (74 KB) | **NO HEADLINE — the json's top-level scalar dict is empty and the nested structure was not read** |
| XRSpinoPelvic1K landmark nets (2) | `~/XRSpinoPelvic1K/data/runs/{unified,unified_lb}/best.pt` | heatmap regressor σ 2.0 | 2026-08-06 / 08-09 | `history.csv` | unified err_all 2.877 px, err_hip 2.673; unified_lb 3.150 / 3.091. **X-ray paper, not level-ID** |
| nnU-Net 3-D CT (Dataset802/810/813) | `~/spinesurg-ct-nnunet/nnunet/results/Dataset*/` | ~24 `.pth` at ~1.13 GB | 2026-07-28 → 09-14 | **none scored here** | Different family. Two archived dirs record failures in their names: `_archive_37ep_wrong_metrics_lowL6sampling_20260912_0601`, `_archive_500ep_novalexport_20260911_1930` |
| VISTA3D (third party) | `~/NV-Segment-CTMR/NV-Segment-CT/models/model.pt` (a 162 B symlink) | NVIDIA pretrained | 2026-09-09 | `~/bench/vista3d/` | Scored as a competitor in the one-shot benchmark. Not ours |

---

## 6. Every result, with its denominator

**Grouped by evaluation surface. No two rows from different surfaces may be compared.**

### Surface A — films_ann / films_all2 own-bank val: n = 8,422 crops, 1,653 films, **14 of 27 classes live**, 93.8 % cervical, chance 1/14 = 7.14 %

| Result file | Model / arm | Metric | Value | Date |
|---|---|---|---|---|
| `~/bench/xr_fov/recurrent.json` | BiGRU over films_ann rung-0 embeddings | exact @ 3/5/7/9 vert | **98.69 / 99.13 / 99.41 / 99.48**; within-1 99.85/99.87/99.91/99.91 | 2026-09-13 13:28 |
| `~/bench/xr_fov/recurrent_dump.json` | same, `--dump` rerun | exact @ 3/5/7/9 | 98.86 / 99.13 / 99.24 / 99.61 | 2026-09-13 17:36 |
| `~/bench/xr_fov/recurrent_all2.json` | BiGRU over films_all2 rung-0, 40 ep | exact @ 3/5/7/9 | 98.84 / 99.13 / 99.42 / 99.38 | 2026-09-14 00:43 |
| `~/model_night/recurrent_films_all2.json` | BiGRU over films_all2 rung-1 aug2, head saved | exact @ 3/5/7/9 | 99.15 / 99.34 / 99.23 / 99.72. **Per-region @3: cervical 99.61, thoracic 83.33 (n 66), lumbar 93.17, sacrum 95.65 (n 46)** | 2026-09-16 01:00 |
| `~/bench/xr_fov/fusion.json` | message-passing fusion over the run | exact | single 96.95; fused 98.16 / 98.08 / 98.35 / 98.40. **Fused sacrum 56.5 → 2.2 → 0.0 → 2.2 %; thoracic 37.9 → 12.1 %** | 2026-09-13 13:01 |
| `~/bench/xr_fov/summary.json`, `table.md` | ours_2d vs level_as_class vs count_oracle vs reference_count | exact @ rung 0/1/2 | ours_2d 96.95/98.63/98.78; level_as_class 63.98/93.71/98.34; reference_count 1.84/3.95/5.18; count_oracle 1.52/2.42/4.29. **no_answer: ours_2d 0 %, count_oracle 98.5/97.0/94.7 %** | 2026-09-13 16:49 |
| `~/films_all2_fov96_ctx/runs/result_rung_*.json` | films_all2 single-crop ladder | exact | rung 0 97.46, rung 1 98.98, rung 2 98.99; aug2 95.96/98.73/98.68; aug3 86.24/94.56/96.34 | 2026-09-13→14 |
| `~/films_ann_fov96_ctx/runs/...` (via M33–M38) | films_ann single-crop ladder | exact | 96.95 / 98.63 / 98.78; supcon 97.02 / 98.77 / 98.86 | 2026-09-13 |
| `~/mv_bands/runs/result_mv_rung_*.json` | mv_bands multi-view identifier | exact | 95.37 / 98.05 / 97.57. Sequence loss adds 0.05 pt at rung 1, **hurts** at rung 2 (97.57 vs 97.97) | 2026-09-13 |

Note on the counting baselines: they score 1.5–5.2 % because they **abstain on 95–98 % of targets**.
"ours_2d 96.9 % vs count_oracle 1.5 %" is mostly an abstention-rate comparison, not an error-rate one.

### Surface A′ — films_all4 own-bank val: n = 13,777 crops, **14 classes live, 39 % BUU lumbar** (a harder split)

| Result file | Arm | Exact | Note |
|---|---|---|---|
| `~/films_all4_fov96_ctx/runs/result_rung_{0,1}_aug3.json` | films_all4 aug3 | rung 0 **82.01 %**, rung 1 **90.88 %**; within-1 98.41 / 99.45 | Per source at rung 1: csxa 96.72, buu_full 84.97, nhanes 78.50. **90.9 % here is a stronger result than 99.0 % on films_all2**, because films_all2's val is 94 % cervical. This is the clearest single illustration of why these percentages cannot be ranked across banks |

### Surface B — allspine_v2 own-bank val: n = 16,392 crops, **27 of 27 classes live** (val T13 n = 14, L6 n = 132, sacrum n = 145)

| Result file | Arm | Exact (95 % CI) | Within-1 | MAE | Rare classes |
|---|---|---|---|---|---|
| `~/model_night/recurrent_allspine_v2.json` | **BiGRU head, k=1/2/3/4** | **83.38 / 86.12 / 86.16 / 88.95** | 97.14 / 97.78 / 97.99 / 98.01 | — | — |
| `~/model_night/logs/stc_stc_rand50_40294458.out` | stc_head, bands ≤7 | **85.93 % [85.49, 86.35]** over **24,882 vertebrae** | — | — | — |
| `~/allspine_v2_fov96_ctx/runs/result_rung_1_aug2.json` | allspine_v2_r1 (historical baseline) | 78.78 % | 95.88 | — | per source: csxa 99.27, buu_full 89.62, ctsp_drr 93.55, nhanes 93.07, verse_drr 77.50, physics_drr 62.53, physics_rare 52.31 |
| `~/model_night/runs/result_r18_ce.json` | **r18_ce (CONTROL)** | **78.74 % [78.11, 79.37]** | 95.78 | 0.352 | **T13 0.0 % (n 14)**, L6 64.4 % (n 132). macro 70.39, region 97.33 |
| `~/model_night/runs/result_r18_corn.json` | r18_corn | 78.44 % [77.8, 79.1] | 95.49 | 0.360 | T13 0.0, L6 60.6. macro 69.98 |
| `~/model_night/runs/result_r18_ordfocal.json` | r18_ordfocal | 75.05 % [74.4, 75.7] | 94.98 | 0.405 | T13 0.0, L6 67.4. macro 68.24 |
| `~/model_night/runs/result_r18_ce_8ep.json` | r18_ce_8ep | 71.30 % [70.6, 72.0] | 92.47 | 0.544 | T13 0.0, **L6 77.3** |
| `~/model_night/runs/result_r18_frozen.json` | r18_frozen | 30.12 % [29.4, 30.8] | 55.20 | 3.874 | **T13 14.3 % — the only non-zero, on 14 crops** |

**The recurrent gain on the whole spine:** 78.74 → 83.38 at three vertebrae, → 88.95 at nine,
same bank, same 16,392 crops.

**Two own-bank numbers exist for r18_ce and they are different computations:**
`result_r18_ce.json` 78.74 % (per-crop over the val split) and `diag_r18_ce.json` 78.8 %
(`own_bank_single_overall`). Quote the one whose denominator you mean.

### Surface C — allspine_v3 own-bank val: n = 26,381 crops, 27 classes, **more rare support** (T13 train 110 / val 30; L6 train 1,322 / val 278; sacrum train 2,800)

| Result file | Arm | Exact | Within-1 | Note |
|---|---|---|---|---|
| `~/model_night/runs/result_r18_ordfocal_v3.json` | r18_ordfocal_v3 | 74.83 % [74.30, 75.35] | 95.66 | **NOT comparable to the control's 78.74 %** — different bank, different val split (26,381 vs 16,392), harder because it adds oblique DRRs. The fair readings are **macro-exact 71.33 (best of any arm, vs control 70.39)**, beyond-two 1.47 % (best of any arm), **T13 0.0 → 6.7 % (n 30)**, **L6 64.4 → 70.1 % (n 278)**. New sources: ctsp_drr_obl2 72.33 (n 3,076), verse_drr_obl2 68.82 (n 5,567), vindr 97.82 (n 551). **Absent from `RESULTS_snapshot.md` — it finished 36 min after the snapshot was written** |

### Surface D — small own-render / own-bank vals

| Result file | Arm | n | Classes live | Exact | Note |
|---|---|---|---|---|---|
| `~/model_night/runs/result_exp3_radiograph.json` | exp3_radiograph | 709 | **12 (T6–L5)**, no T13/L6 | 57.69 % [54.05, 61.32] | within-1 90.55, macro 43.61 |
| `~/model_night/runs/result_exp3_fluoro.json` | exp3_fluoro | 709 | 12 | 54.72 % [51.06, 58.39] | within-1 91.40, macro 43.08. **The two CIs overlap heavily — +3.0 pt is not a demonstration** |
| `~/allspine_fov96_ctx/runs/result_rung_1_aug2_aug2.json` | allspine v1 rung 1 | 12,906 | 27 nominal, **T13 val n = 1, L6 val n = 13** | 80.16 % | **Looks better than v2's 78.8 % but it is a denominator artefact** — smaller, easier val split with effectively no rare class to get wrong |

### Surface E — held-out CT renders (training-case renders skipped; `renders_held_out: true`)

| Result file | Model | Renders read / skipped | Exact | Note |
|---|---|---|---|---|
| `~/model_night/diag_r18_ce.json` | r18_ce | 800 / 4,505 | **64.2 %** | The only genuinely held-out surface on that row |
| `~/model_night/diag_r18_corn.json` | r18_corn | 800 / 4,505 | 63.0 % | |
| `~/model_night/diag_r18_ordfocal_v3.json` | r18_ordfocal_v3 | 800 / 4,405 | 62.1 % | |
| `~/model_night/diag_r18_ordfocal.json` | r18_ordfocal | 800 / 4,505 | 58.9 % | |
| `~/model_night/diag_r18_ce_8ep.json` | r18_ce_8ep | 800 / 4,505 | 53.4 % | |
| `~/model_night/diag_r18_frozen.json` | r18_frozen | 800 / 4,505 | 16.7 % | |
| `~/FluoroCap/level_model_diag_allspine_v2.json` | allspine_v2 rung_1_aug2 | 800 / 4,505 | **64.2 %** | own-bank 78.8 % |
| `~/FluoroCap/level_model_diag_finetuned.json` | the corpus fine-tune | 576 / 3,563 | **55.9 %** | own-bank unchanged at 78.8 %. **The fine-tune costs 8.3 pt on held-out renders and own-bank validation was completely blind to it** |
| `~/FluoroCap/cut_eval_*_v2.json` | allspine model | 443–600 read | raw_phys 51.0, **cut_phys 36.6**, cut_rare 23.7 | Cutting the frame costs 14.4 pt held-out. **`cut_rare_v2` skipped only 597 renders where `cut_phys_v2` skipped 2,557 — those two do not share a denominator and must not be differenced** |
| `~/FluoroCap/cut_eval_films_*_v2.json` | films_all2 model (own-bank 98.7 %) | — | **12–17 % on every variant** | T10 and T11 read 0.0 % at n 246/313 (phys) and n 209/272 (rare) |

### Surface E′ — CT renders **NOT** held out. **Contaminated. Do not quote.**

| Result file | Model | Renders | Value | Why it is wrong |
|---|---|---|---|---|
| `~/FluoroCap/level_model_diag_allspine.json` | allspine v1 rung_1_aug2_aug2 | 600 read | own-bank 80.2 % / **renders 92.7 %** | Renders scoring **higher** than own-bank cannot happen on a held-out surface. The file has no `renders_held_out` key and no `renders_skipped_train` count — **the renders include training cases.** `RESULTS_snapshot.md` and `MORNING_REPORT.md` both print 92.7 beside allspine_v2's 64.2 as though they were the same measurement. They are not: 64.2 skipped 4,505 training renders, 92.7 skipped none |
| `~/FluoroCap/level_model_diag.json` | films_all2 + recurrent head | 300 read | own-bank 98.7 % / **renders 35.7 %** | Also carries no held-out flag, so **the true held-out figure is likely lower, not higher.** Per-level: T10 0.0 (n 280), T11 0.0 (n 295), T12 4.3 (n 300), L1 43.0, L2 78.7, sacrum 5.3 |
| `~/FluoroCap/cut_eval_*.json` (non-`_v2`) | allspine model | 600 | raw_phys 53.7, raw_rare 42.8, cut_phys 41.4, cut_rare 33.3 | Not held out |

### Surface F — real literature panels, weak labels. **Not an accuracy against truth.**

Every `realpanel_*.json` carries its own note: "labels are decoder placements constrained by outside
evidence, not a radiologist's reading; comparable between arms, not an accuracy against truth."

| Result file | Model | Panels / crops | Classes | Exact (CI) | Note |
|---|---|---|---|---|---|
| `~/model_night/realpanel/realpanel_exp3_fluoro.json` | exp3_fluoro | 1,486 / 7,065, signature `a850a5bd` | 27 (incl. T13 n 34, L6 n 43) | 10.94 % [10.21, 11.67] | Non-zero only in the lumbar band (L4 35.05, L2 31.96, L5 20.45, L3 19.45, L1 10.52). **All seven cervical levels and the sacrum read exactly 0.0 %** — that looks like a systematic band offset, not per-level error |
| `~/model_night/realpanel/realpanel_exp3_radiograph.json` | exp3_radiograph | same 1,486 / 7,065, **identical signature** | 27 | 10.83 % [10.10, 11.55] | **Radiograph − fluoro = −0.1 pt with fully overlapping CIs.** The renderer-physics change moved own-render accuracy +3.0 pt and vanished on real images |
| `~/model_night/smoke/realpanel_smoke_baseline.json` | allspine_v2 rung_1_aug2 | 117 / 529, `holdout_only=false` | 27 | 26.09 % [22.34, 29.83] | **NOT filtered against training material** |
| `~/model_night/smoke/realpanel_smoke_baseline_holdout.json` | same model | 119 / 588, `holdout_only=true` | 27 | 19.73 % [16.51, 22.94] | **26.09 → 19.73: about a quarter of the non-held-out number is contamination. Any real-panel figure quoted without its `holdout_only` flag is unreadable** |
| `~/model_night/smoke/result_smoke2.json` | corpus fine-tune, 1 ep | 5,022 holdout crops / 1,886 papers | 27 | after 1 ep: film_val 74.90, corpus_holdout 16.55; **baseline before: 78.78 / 19.57** | **Fine-tuning on the real corpus made BOTH numbers worse.** Second independent instance of this (cf. `level_model_diag_finetuned.json`) |

### Surface G — transitional strata, held-out CT renders (allspine_v2 arms: 376 scored / 2,281 skipped)

| Stratum | ce | corn | ordfocal | ce_8ep | frozen | ordfocal_v3 (v3 bank) |
|---|---|---|---|---|---|---|
| **T13 → T13** | **0.0** (n 16) | 0.0 | 0.0 | 0.0 | **12.5** | **0.0** (n 16) |
| **L6 → L6** | 63.0 (n 108) | 61.1 | 71.3 | **75.9** | 51.9 | 61.2 (**n 227**) |
| normal T12 | 86.5 (n 185) | 89.2 | 77.8 | 72.4 | 41.1 | 73.3 (n 225) |
| normal L5 | 86.2 (n 160) | 84.4 | 75.6 | 75.6 | 73.1 | 74.4 (n 168) |
| normal sacrum | 100.0 (n 119) | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 (n 119) |
| castellvi_I_II | L5 35.3 (n 17), L4 27.8 (n 18) | — | — | — | — | — |
| castellvi_III_IV | L5 68.4 (n 19), L4 57.6 (n 33) | — | — | — | — | — |

Files: `~/model_night/transitional/transitional_eval_r18_{ce,ce_8ep,corn,ordfocal,frozen,ordfocal_v3}.md` (+ `.json`).

- **T13 → T13 is 0.0 % for every fine-tuned arm.** With 30 T13 training crops in the v2 bank that
  is a data fact, not a model fact.
- **The best arm at L6 (ce_8ep, 75.9 %) is the worst arm overall (71.30 %).** Reading the L6 column
  alone picks the wrong model — the spread-vs-median trap, in the class dimension.
- `ordfocal_v3` is on a **different bank and a different render denominator** (571 scored / 2,086
  skipped), so its row is not directly comparable. Its L6 stratum n more than doubles (227 vs 108),
  which makes 61.2 % better supported than the v2 arms' 63.0 %.

### Surface H — image class within one held-out val split

| Result file | Split | n | Classes covered | Exact |
|---|---|---|---|---|
| `~/model_night/rawfilms/rawfilms_r18_ce_v2.json` | real radiographs | 7,339 | **14** (C2–C7, T1 n 10, T12 n 57, L1–L5, sacrum n 25) | **95.09 % [94.58, 95.57]** |
| same | rendered from CT | 9,053 | **27**, incl. T13 and L6 | **65.53 % [64.54, 66.50]** |

**This is not a 30-point domain gap and must not be quoted as one — it is largely a class-coverage
difference.** Per source: csxa 99.44 (n 3,720), buu_full 90.29 (n 2,698), nhanes 92.65 (n 476),
nhanes_drr 90.56 (n 445), ctsp_drr 94.77 (n 1,070), verse_drr 76.65 (n 711), physics_drr 62.01
(n 5,928), physics_rare 51.86 (n 1,344). **Unresolved:** `nhanes_drr` is filed under
`class=real_radiograph` while being a DRR.

### Surface I — corruption suite, own-bank val, n = 4,000 crops, 14 classes live

| Result file | Model | Clean | Over-exposure sev 5 | Magnify sev 5 | Shutter sev 5 | Invert |
|---|---|---|---|---|---|---|
| `~/bench/robust/all2_base_rung_1.json` | films_all2 rung 1, base aug | **99.10 %** (lumbar 90.29) | **16.93 %** | 57.63 % | 73.60 % | 91.58 % |
| `~/bench/robust/all2_aug2_rung_1.json` | aug tier 2 | 98.98 % (lumbar 92.00) | **79.18 %** | 97.63 % | 95.33 % | 98.73 % |
| `~/bench/robust/all2_aug3_rung_1.json` | aug tier 3 | 94.85 % (lumbar **70.29**) | 77.73 % | 92.63 % | 89.20 % | 94.58 % |
| `~/bench/robust/base_rung_0.json` | **films_ann** rung 0 | 97.28 % (lumbar 85.71) | 31.75 % | 47.28 % | 74.48 % | 77.23 % |

A 99.1 %-clean model that reads 16.9 % on an over-exposed film is not a 99.1 % model in any clinical
sense. Over-exposure and magnification are the two failure axes and both are ordinary radiographic
variation. **Tier 2 is the clear winner** (costs 0.12 pt clean, buys 62 pt of over-exposure and 40 pt
of magnification robustness); **tier 3 is worse than tier 2 on almost every corruption** while costing
4.3 pt clean and 22 pt lumbar. `base_rung_1`/`base_rung_2` were not read in full.

### Surface J — detection. **Recall and IoU. Never pool with an accuracy.**

| Result file | Model | n | Clean | Worst cases |
|---|---|---|---|---|
| `~/bench/xr_fov/detector_robustness.json` | detect_v3, conf 0.4, imgsz 1024 | 300 films, 1,525 GT boxes | recall@0.5 = **1.000**, mean IoU of hits 0.9293, 5.12 det/film | collimation lvl 2 recall 0.9449; invert 0.9744; monitor-photo recall 0.9987 but **mean IoU collapses to 0.7748** |

A clean recall of exactly 1.000 on 1,525 boxes deserves an independent check; it is the kind of round
number this project's failure mode produces.

### Surface K — LSTV / TLTV flags. AUC, patient-level 5-fold CV, CT-derived renders

| Result file | Arm | Cohort (positives) | AUC (95 % CI) |
|---|---|---|---|
| `LSTV_FLAG_RESULTS.md` §3 | lstv_flag_v1, mean pooling | CTSP 801 (34 pos) | **0.577 [0.480, 0.669] — contains 0.5** |
| same | by field of view | junction (tight L5–S1) | **0.656 [0.558, 0.743]** — the only stratum whose interval excludes 0.5, and it is 1 of 7 strata reported, uncorrected |
| same | | lumbar field | 0.509 [0.415, 0.599] |
| same | | wide field | 0.543 [0.452, 0.635] |
| same | at the comparator's 85.1 % sensitivity | thr 0.008 | sens 0.853, spec 0.248, **PPV 0.048**, NPV 0.974 (tp 29, fn 5, fp 577, tn 190) |
| `LSTV_FLAG_RESULTS.md` §3 (TLTV) | tltv_flag_v1 | CTSP 801 (16 pos) | 0.632 [0.483, 0.753] no-abstention; 0.584 [0.438, 0.712] evaluable-only. **Every stratum's interval contains 0.5** |
| `LSTV_FLAG_RESULTS.md` §3 | **sex positive control** | same renders, 345 male of 802 | **0.951 [0.935, 0.966]**; at Youden sens 0.953 / spec 0.899 |
| `LSTV_FLAG_RESULTS.md` §10 | lstv_flag_v2, **within cohort** | CTSP (34/801) | 0.535 [0.446, 0.627] |
| same | | VerSe (125/269) | **0.724 [0.658, 0.783]** |
| same | **pooled across cohorts** | 1,070 | **0.847 [0.808, 0.885] — reported only to be dismissed.** CTSP is 4 % positive, VerSe 46 %, and the renders are trivially separable, so the pooled AUC largely measures "is this a VerSe scan" |
| same | VerSe subsets vs 144 negatives | six-lumbar only (n 81) | 0.771 [0.708, 0.833] |
| same | | not six-lumbar (n 44) | 0.637 [0.540, 0.731] |
| same | | five-lumbar only (n 41) | 0.625 [0.512, 0.723] |
| same | tltv_flag_v2 | VerSe (91/277) | 0.510 [0.438, 0.579] — indistinguishable from chance. **Extra VerSe data did not help TLTV** |
| `~/lstv_flag/LEARNING_CURVE.md` | AUC vs training positives, 50 runs | VerSe held-out (67 pts, 31 pos) | 10 pos → 0.652, 20 → 0.688, **40 → 0.704**, 80 → 0.685, **120 → 0.713**. **The curve is not still climbing — tripling the positives bought under 0.01 AUC** |

### Surface L — real BUU films, external, never trained on (3,600 lateral + 3,600 AP)

| Result file | Arm | Metric | Value |
|---|---|---|---|
| `LSTV_FLAG_RESULTS.md` §6, §11 | lstv_flag_v1 retrieval | known anomalies in top 1,000 of 3,600 | 42 lateral / 47 AP against a **chance expectation of 40**. Top 500: 19/22 vs 20. Median rank of all 144 anomalies: 1,767 (LA) / 1,657 (AP) |
| same | six-lumbar subset (n 15) | AUC | 0.464 |
| same | four-lumbar subset (n 129) | AUC | 0.559 |
| same | **sex control on the same real films** | AUC | **0.829 [0.816, 0.843] lateral, 0.793 [0.777, 0.808] AP** — against 0.951 on renders |

**The decisive control in the whole tree.** The sex model transfers to real film at a cost of ~0.12
AUC, so the render-to-radiograph domain gap is real but partial and is **not** the explanation for
the flag's failure. What the flag actually responds to was then looked at: its ten highest-scoring
BUU films average age 63 and its ten lowest age 32 — it is reading degenerative change, age, sex and
exposure. 66.3 % of lateral films clear the operating point, so the threshold does not carry across
domains.

### Surface M — external-film naming probe

| Result file | Arm | n | Value |
|---|---|---|---|
| `~/model_night/aasce_naming_check.json` | allspine_v2 rung_1_aug2 used to test whether AASCE ordering starts at T1 | 120 films, 2,040 vertebrae, 10 decisive positions | best agreement **10.64 %** at shift 0; shift −1 (C7) 9.61 %; shift +1 (T2) 5.59 %. File sets `verdict_inconclusive = true`, correctly. The per-position dump shows the model calling AASCE's T1–T8 positions "L3/L4/L2" — it is not reading thoracic morphology on these films at all |

### Surface N — corpus inventories. **Not accuracies.**

| File | Content | Caveat carried by the file itself |
|---|---|---|
| `~/FluoroCap/CORPUS_MANIFEST.md`/`.json` | 12,106 figures; 20,700 panels decoded; 11,377 carrying a level; 9,235 of 12,106 (76 %) with short side ≥ 320 px. Level counts: L4 5,879, L3 5,749, L5 4,622, L2 5,159, L1 4,438, T12 2,866, sacrum 1,587, **T13 254, L6 338**. Caption-named anomalies: hardware 4,565, transitional unspecified 389, cervical rib 184, L6/six-lumbar 170, sacralization 99, lumbarization 95, wrong-level event 73, T13 60 | "A decoded level is the decoder's placement, not a verified label… A caption naming an anomaly marks a candidate, not a finding" |
| `~/FluoroCap/LEVEL_COUNTS.md`/`.json` | 11,339 labelled panels of 20,700. Attribution: T13 254 (**214 by model**, 18 by caption); L6 338 (**279 by model**, 39 by caption) | **The corpus's rare-class "labels" are ~85 % the model's own output fed back as data.** Baseline and interim variants of this file exist with different numbers |
| `~/FluoroCap/MORNING_REPORT.md` | overnight roll-up; refetch (2,901 figures, 2,059 replaced, median gain ×6.25); QC v3 caption_agreement: caption_constrained 2,978 panels containment **100.0 %** mean Jaccard 0.484; caption_free 757 panels containment **49.1 %** mean Jaccard 0.298 | **Its "Level model" block prints 92.7 and 64.2 in adjacent rows with no held-out flag** — the single most misleading juxtaposition in the tree. The **49.1 % caption-free containment is the only genuinely held-out caption test**; the 100.0 % is a consistency check on rows whose caption was forced into the search |
| `~/lstv_flag/ANOMALY_INVENTORY.md` | Six lumbar: 18 CTSP / 85 VerSe / 15 BUU. Lumbarisation 14, sacralisation 17, semi-sacralisation 2. Castellvi CTSP: IIa 4, IIb 6, IIIa 1, IIIb 16, IV 4, Ib 2, **Ia 0**. **T13 vertebra: 0 CTSP, 6 VerSe.** Lumbar rib 16 CTSP. Any-LSTV: 34/802 CTSP, 130/325 VerSe, 144/3,600 BUU (count only). Any-TLTV: 16/802, 97/325 | Two structural caveats govern every LSTV number: (1) **Castellvi I is roughly two thirds of all transitional anatomy and cannot be separated from grade 0 in any source held**, so it contaminates every negative set; (2) CTSpinoPelvic1K is abdominopelvic — 4 to 10 rib pairs in field, never 12 — so "zero T13" is a field-of-view fact, not a prevalence |

### Surface O — safety flags

| Result file | Flag | Evaluable set | Sens (CI) | Spec (CI) | Abstention |
|---|---|---|---|---|---|
| `~/model_night/flags/flags_r18_ce_v2.json` | count_vs_morphology | 176 renders, **169 normal + 7 transitional cases (6 L6, 1 T13)** | 0.4286 [0.1582, 0.7495] | 0.8383 [0.7750, 0.8864] | 1.14 % |
| same | lumbar_count_anomaly | same | **0.0 [0.0, 0.7935]** | 1.0 [0.9682, 1.0] | 32.95 % |
| same | no_reference_landmark | same | 0.7143 [0.3589, 0.9178] | 0.7692 [0.7001, 0.8263] | 0.0 % |

**Seven transitional cases.** Every sensitivity CI is 0.4–0.8 wide and all three contain values
consistent with a useless flag. `lumbar_count_anomaly` has sensitivity 0.0 on **one** evaluable
transitional case and abstains on a third of everything. These are not measurements; they are the
shape of a measurement.

---

## 7. What is missing or not verified

### 7.1 Files that do not exist (checked explicitly, not omitted)

| Path | Status |
|---|---|
| `~/model_night/RESULTS.md` | **Does not exist.** The only markdown summary of the nine-arm experiment is `RESULTS_snapshot.md` (6,710 B, 2026-09-16 00:15) plus `smoke/RESULTS_smoke.md` |
| `~/ct_mine/CT_MINE_REPORT.md` | **Does not exist.** `~/ct_mine` holds `mine.sbatch`, `mine_spine_anomaly.py`, `mine_spine_final.py`, `mine_spine_validate.py`, and directories `out/`, `shards/`, `shards2/` — none of which were opened. Whether a result exists inside them is unknown |
| `~/fluorogen/synth_v1` | Exists, **contains zero files** in `ann/`, `img/` and `preview/` |
| `~/films_all2_fov128m_ctx` | Exists, **zero files**, no meta.json, no rung, no runs/ |
| `~/spine-detector/data/raw/cm_spine` | Exists, **zero files** |
| `~/bench/gt/oneshot` | **Empty** |
| `~/XRSpinoPelvic1K/data/{ct,labels}` | **Dangling symlinks** to `CTSpinoPelvic1K/data/hf_export_v3`, which no longer exists |
| `~/FluoroCap_lstv`, `~/films_all2` | Do not exist under those names. Live paths are `~/FluoroCap/captions_matched_lstv.jsonl` and `~/films_all2_fov96_ctx` |
| All five `.raw` parent banks | `films_all2_fov96_ctx.raw`, `films_all2_fov48_ctx.raw`, `films_all3_fov96_ctx.raw`, `films_all_fov48_ctx.raw`, `vo_fov48_plus_nh_ctx.raw` — `ls $HOME/*.raw` returns nothing. Half of each of those merge lineages cannot be re-derived |

### 7.2 Models with no result

- **Six FluoroCap inference-time recurrent heads** (`recurrent_head_*.pt`): trained lazily at
  inference, never scored in isolation. No held-out number for any of them.
- `recurrent_head_films_all2_3654e9ba_r1.pt`, `_de9a5dfe_r2.pt`, `_964e17f1_r2.pt` — no result file.
- The registered head `recurrent_head_films_all2_r1` has an **empty `metrics` block** in
  `~/model_registry/registry.jsonl`.
- **films_all4 `model_rung_1_aug3.pt` and `model_rung_2_aug3.pt`**: on disk, written 2026-09-14
  04:53, after `bench/model_registry.csv` was generated at 03:06. **No held-out number.**
- **`verse_only_ctx_plus_nh`**: five weight files and five `result_rung_*.json` exist; the bank has
  **no row in `bench/model_registry.csv`** and the jsons were not opened. **No number.**
- **contour model**: `result_contour.json` is 74 KB but its top-level scalar dict is empty; the
  nested structure was not read. **No headline.**
- **XRSpinoPelvic1K yolo_exp sweep** (7 runs, 14 files): listed, `results.csv` not opened.
- `fluorogen_lora_v1`: no result file.
- `detect_v5z_latest_best.pt`, `detect_v5z_epoch4_best.pt`: no result file, not registered.
- **The four `model_night/heads/*` head sets**: nothing downstream has consumed them; their
  accuracies come from `.arch.json` sidecars and job logs, not an independent evaluation.
- **Four ViT arms produced no result at all** — `raddino_frozen` (40292277), `raddino_ft` (40292278),
  `dinov3_frozen` (40292279), `dinov3_ft` (40292280). RAD-DINO was reachable
  (`weights_check.json`: `ok=true`, ViT-B/14, 86.6 M params, `offline_ok=true`) and timed; DINOv3's
  facebook repo is gated (403) **but a working timm mirror was pulled** (`vit_base_patch16_dinov3`,
  85.6 M params). **All four failures are unexplained, and no logs for those job ids exist in
  `~/model_night/logs/`.** Two more, `corpus_ft` and `corpus_ft_frozen`, are also MISSING.
- `r18_ce_8ep` was the **matched-budget control for the ViT arms**. Since none of them produced a
  result, it currently controls for nothing that exists.

### 7.3 Results with no surviving model

- **The headline itself.** `~/bench/xr_fov/recurrent.json` (98.69/99.13/99.41/99.48) — the weights
  were never saved. Job 40215812 predates `--save-head`.
- `~/bench/xr_fov/recurrent_dump.json` and `recurrent_all2.json` — same, no weight file.
- `~/bench/xr_fov/base_rung_0_dump.json` is a byte-identical re-dump of `base_rung_0.json`.

### 7.4 Datasets on the grid that feed nothing

| Dataset / render dir | Size | Why it matters |
|---|---|---|
| `lateral_236` | 1.3 GB, 236 films | **The only real whole-spine lateral corpus on the grid.** Unlabelled. Feeds no bank, no detector store, no manifest |
| `nhanes_full` (unannotated part) | 91 GB, **16,531 films** | By far the largest pool of unlabelled real spine radiographs held |
| `fluorogen/synth_rare` | 9.0 GB, 12,929 renders | **T13 86, L6 1,763 — the richest variant pool in the corpus** |
| `cut_rare`, `cut_rare_v2` | 1.1 GB each | **T13 43, L6 845 each** |
| `FluoroCap` | 316 GB, 20,700 panels | **The only real-image T13 (254) and L6 (338) anywhere.** No `fluorocap` source tag appears in any of the 41 banks |
| `anchor_drr` | 2.6 GB, 7,842 renders, T13 12 / L6 204 | Its own YOLO detection set, not in a crop bank |
| `lstv_flag/renders_verse` | 869 MB, 3,456 renders | **T13 62 — the highest of any LSTV set.** Read directly by the flag trainers, in no ctx bank |
| `spinalai_drr` / `spinal_ai2024` | 4.4 GB / 2.7 GB | AI-generated, 44 distinct identities, assumed levels. Feeds nothing, and should not |
| `mendeley_drr` / `mendeley_716` | 1.3 GB / 201 MB | 86 % duplicate of BUU already in `films_drr`. Feeds nothing |
| `postop_render` | 32 MB, 45 renders | No consumer found in the repo |
| `cut_physics`, `cut_physics_v2` | 2.1 GB each | Eval sets only |
| `vf_813` | 58 GB | Feeds no ctx bank |
| `XRSpinoPelvic1K/data/dataset2024.zip` | 4.7 GB | **Never opened.** Contents unknown; may or may not duplicate BUU-LSPINE |

### 7.5 Disagreements between sources, and which is trusted

| Question | Reading A | Reading B | Trusted, and why |
|---|---|---|---|
| **Which bank produced 98.7/99.1/99.4?** | Inventory 5 and the repo: `films_all2_fov96_ctx` (from `slurm/recurrent_head.sh` and `bench/model_registry.md` M96) | Inventory 4 and verdict 1: `films_ann_fov96_ctx` | **B.** Three independent lines: the job log's `embedded 28032 crops` matches films_ann exactly and films_all2 not at all; the films_all2 inputs were created 75 min and 2 h 17 min *after* the result was written; the script's own usage line and the benchmark suite log both name films_ann. A rests on a comment that B's timestamps contradict |
| **Is there a whole-spine recurrent number?** | Inventory 5: no — job 40293533 crashed on the `enc.` key prefix | Inventory 4 and verdict 2: yes — job 40293790 retried at 01:14 and exited `RECURRENT_RC=0` at 01:21:30, weights saved | **B.** Inventory 5 read only the earlier failed log. The retry's result file, four weight files with sidecars, and the success log all exist |
| **Do VerSe scans cross the train/val split in allspine_v4?** | Inventory 2: **no leak** — 56 VerSe cases held out in the `verse_*` namespace, 0 trained via `ctsp_drr_obl2`; the merge's `leak_crops_prevented=9194` did its job | Inventory 3: **86 of 374 VerSe scans have crops in BOTH splits**, because the grouping regex `^(?:implant\|ctsp\|verse\|totalseg)_(.+?)(_v[0-9]+)?_(lat\|ap)_p[0-9]+$` does not match `CTSP_VERSE_gl279_p0` or `gl003_p0` | **Both, and they are compatible.** Inventory 2 tested one namespace pair (`verse_*` vs `ctsp_verse_*`); Inventory 3 tested all five source tags including `physics_drr`/`physics_rare`. They reconcile if the crossing runs through physics_drr, not through ctsp_drr_obl2. **Not resolved — this needs one test that names the crossing tag.** Do not repeat "there is no leak" until it is |
| **How many crop banks?** | Inventory 1: 42 | Inventories 2 and 3: 41 `*_ctx` | **Reconciled:** 41 populated `*_ctx` + `mv_bands` (which is not named `*_ctx`) = 42, plus the empty `films_all2_fov128m_ctx` = 43 directories |
| **How many VerSe volumes carry a T13?** | `VerSeFusion/manifest_summary.json`: `t13_supernumerary = 18` | Inventory 2 (per-render count) and the standing project note: **6** | **6.** `verse_drr` has exactly one render per case and reads T13 = 6, so 6 distinct volumes. The manifest flag is the known-wrong one (wrong label map). Inventory 3 reports 18 without recounting and says so |
| **spinal_ai2024 size and source collapse** | claim: 20,001 films collapsing onto 52 real films | Inventory 3: **20,000** films; **52** is right for the Top-1 structural-similarity column only, but the union over all six neighbour columns is **252** | **Inventory 3**, which read the checklist columns |
| **mendeley_716 count** | name says 716 | Inventory 3: **714** (16 test + 494 train + 204 val) | **714** |
| **buu_2000 vs buu_full** | "byte-identical subset" | Inventory 3: images byte-identical, **1,337 of 4,000 CSVs differ** in column 5 (flag codes 5–10 vs 1–4/20–21) | **Inventory 3.** True of the images, false of the labels |
| **r18_ce own-bank accuracy** | `result_r18_ce.json`: 78.74 % | `diag_r18_ce.json`: 78.8 % | **Different computations**, not a conflict: per-crop over the val split vs `own_bank_single_overall`. Quote the one whose denominator you mean |
| **`films_all2_fov128_ctx` identity** | the name | Inventory 1: its index is the **films_ann** index (csxa + nhanes only, no buu, no vindr; lumbar train 183–186/level) | **Inventory 1.** The bank is misnamed |
| **What explains the films_all2 model's 0.0 % at T10/T11 on renders** | "the bank has no thoracic crops" | Verdict 3: the bank has **154 thoracic training crops** (T1 22, T12 132); T10/T11 specifically have zero; and well-populated classes (sacrum 124 crops → 5.3 %, L1 3,843 → 43.0 %, L2 3,847 → 7.4–9.9 %) collapse too, so starvation cannot carry it | **Verdict 3.** The 0.0 % at T10/T11 is forced by zero crops; the *overall* render collapse is a domain gap |

### 7.6 Method limits — what was checked and how

- **Crop and level counts** come from each bank's `y`/`split`/`case`/`source` arrays only. **`X` was
  never opened in any npz**, so it is not confirmed that the images match their labels.
- **"Byte-identical" for `films_ann_fov48_scale_ctx` vs `films_ann_fov48_ctx`** rests on exact
  file-size equality for all eight rungs plus md5 of three sampled 16 MiB blocks (head, middle, tail)
  per file — **not a full md5 of the 12.1 GB.** Same method for the `films_all2_fov96_ctx`
  rung_2..full group and `films_all2_fov128_ctx` rung_1..full.
- For `nhanes_fov_48_ctx` vs `nhanes_fov48_split_ctx` and `m_mask22_scale_ctx` vs `merged_ctx`,
  sampled blocks are equal but the files differ slightly in size, so "same pixels, different metadata
  array" is an **inference from the size delta, not a byte proof**.
- Not identified: **which** single render id is in `obl_fov96_ctx` but not `obl2` (2,749/2,750), nor
  the one film in `films_all3` missing from `allspine_v3` (12,602/12,603).
- `buu_pair_fov48_ctx` and `mv_bands` have no `val_cases` key in meta (they use `val_patients` and
  `held_out`), so their meta-vs-array consistency could not be checked the same way.
- `cut_physics_v2`, `cut_rare_v2`, `exp3_radiograph` and `verse_soft_drr` have per-level counts
  **identical** to their v1 / fluoro / non-soft twin. **Labels verified identical; pixels not
  compared**, so it cannot be confirmed the images differ (they should).
- 3 of 12,929 JSONs in `fluorogen/synth_rare` are unparseable and their levels are excluded.
- **"Not consumed"** for `mendeley_drr`, `spinalai_drr`, `postop_render` and `fluorogen/synth_rare*`
  means no consumer in `~/spinesurg-ct-nnunet/{slurm,tools}` and no matching `source` value in any of
  the 41 bank npz files. **A grep across all of `~/FluoroCap` did not finish**, so it cannot be said
  that nothing anywhere reads them.
- `vindr_det_drr` and `vindr_pseudo_drr` **both write `source="vindr"`.** The 3,679 vindr crops were
  attributed to `vindr_pseudo_drr` on two grounds (`launch_round2.sh` names it; `vindr_det_drr`'s
  level names are all "unknown", not in the 27-class table). **The builder's filter was not read to
  confirm it drops unknown.**
- **No `.npy` or `.png` was opened.** View for `ctsp_drr`, `verse_drr`, `verse_soft_drr`, `films_drr`,
  `films_ap_drr`, `nhanes_drr` and both vindr sets is taken from the generating tool's docstring or
  build flags — those anns have no `view` key.
- `~/VerSeFusion/data/unified` is 88 MB but holds 374 × (`_ct.nii.gz`, `_msk.nii.gz`, `_meta.json`).
  **88 MB cannot hold 374 real CT volumes**, so the `_ct.nii.gz` are probably symlinks or masks only;
  individual files were not stat'ed.
- `~/vf_813` has **no `dataset.json`**, so its id→name map is not readable from that directory.
  Observed ids in five `labelsTr` files: {12–17, 25–30, 44}. The standing note that this conversion
  maps C1–T9 to ignore does not obviously square with ids 12–17 being present. **Unresolved.**
- NHANES mask key sets were read from **12 of 543** pickles (each 130–190 MB). Across those 12 the
  cervical key set varied (C7 absent in one, T1 present in another) and some named masks were
  all-zero, so per-level availability across the full 543 is not established.
- `buu_drive`'s md5 comparison covered the 10,990 files shared with `buu_full`. The 1,700 AP and
  1,720 LA files unique to `buu_full` were not compared to anything.
- `implant_ct` / `implant_verse` / `implant_ts` label id ranges were read from **two files each**,
  not all 1,518 / 1,119 / 1,629.
- **No check** was made of whether any TotalSegmentator case is the same patient or study as a
  CTSpinoPelvic1K case. Both draw on public collections; overlap is possible and unmeasured. Same for
  `mendeley_716` against `buu_full` — the filenames are BUU ids, making it a near-certain re-release,
  but its JPEGs were not md5'd against buu_full's because they have been re-encoded.
- **VinDr view/region.** The detector manifest records `view=AP`, `region=full_spine` for all 5,136
  indexed VinDr images. **That is a default, not a measurement** — `BodyPartExamined`, `ViewPosition`,
  `SeriesDescription` and `ProtocolName` were absent in 300 sampled from each split, and rendering six
  at random gave cervical AP, cervical lateral and lumbar lateral. Treat VinDr as mixed region and
  mixed view; the mix ratio is unknown.
- The 86 VerSe scans in both splits of allspine_v4 were established from the bank's own
  `case`/`split`/`source` arrays plus file listings. **Pixel data was not compared** — it is shown
  that the same scan is in both splits, not that any two crops are the same image.
- `head_k*.pt` was **not instantiated into `RunLabeller`**; that it is a RunLabeller is inferred from
  the sidecar and from the byte size (8,473,100 B ≈ 2.117 M fp32 params, which matches
  proj 512×256 + 2-layer BiGRU(256) + head 512×27).
- `allspine_v2/v3/v4` rung npz arrays were **not opened** (5.59 / 34.0 / 35.6 GB); crop counts come
  from training and head logs, which agree at 105,960 for v2.
- `~/FluoroCap/classifier_report.json` (current, Sep 15 19:52) contains only `{"note": "loaded …"}`
  for both heads and 58,888 panels scored. The quoted panel-classifier accuracies come from the older
  v1/v2 reports, which **may** correspond to `panel_classifier_v1_filmsonly.pt` /
  `panel_classifier_v2.pt` rather than the current `panel_classifier.pt`. **Which `.pt` each numbered
  report belongs to could not be confirmed.**
- `region_classifier.pt` has a report but **no sidecar naming its architecture**.
- `bench/robust/base_rung_1.json` and `base_rung_2.json` were not read in full.
- `~/contours/runs/result_contour.json` nested structure not descended into.
- **`~/ct_mine/out`, `shards/`, `shards2/` not opened.**
- FluoroCap's 12,106 figures / 20,700 panels / 11,377 level-carrying panels and its per-level table
  are read from its own `CORPUS_MANIFEST.md` and `LEVEL_COUNTS.md`, **not recomputed** from the decode
  jsonl. Counted directly on disk: `manifest.csv` 36,865 rows, `panels/` 29,500 png, `raw/` 4,998 jpg,
  `raw_hires/` 2,080 jpg, `pdffig` 3,408, `youtube` 298,075 png, `commons` 204, `reddit` 323,
  `openi` 301, `video_panels` 1,096.
- Eight SLURM jobs were RUNNING during the model inventory (40292277/78/79 RAD-DINO and DINOv3 arms,
  40292546 night_rpsweep, 40292632/33 r18 v3 arms, 40292858/59 r18 v4 arms). **Any of them may land
  after this document.** `~/allspine_v4_fov96_ctx` has no `runs/` directory and no model at the time
  of reading.
- **`~/model_night/RESULTS_snapshot.md` is stale in two ways:** five of eleven table rows read
  MISSING, so its verdict "nothing beat the baseline" covers **five arms, not nine**; and a tenth arm,
  `r18_ordfocal_v3`, finished 36 minutes after it was written and does not appear in it at all.

### 7.7 Hygiene defects worth fixing

- `~/allspine_fov96_ctx/runs/model_rung_1_aug2.pt` is a **25-byte symlink** to
  `model_rung_1_aug2_aug2.pt`. The standing rule is never to `ln -sf` a model.
- `cut_drr2fluoro_G` is **registered twice under the same name with different shas**
  (550bea55 backfill, then 28d04f80); the second overwrote the alias.
- `orientation_net_v2` is re-logged to `registry.jsonl` **17 times** by a 20-minute mirror-sync cron,
  which is why the file has 51 lines for 25 models.
- The shipped recurrent head (d0ab6d5e) is **not in `~/model_registry`** — it appears only as M96 in
  `~/bench/model_registry.csv` and in `~/level_id_service/weights/registry.json`. The **one** head
  that is registered (d081b4ab_r1) is **not the one shipped**.
- `~/level_id_service/weights/registry.json` pairs the rung-**0**-trained head with the rung-**1**
  `level_model.pt`.
- `verse_only_ctx_plus_nh` and `vo_fov48_plus_nh_ctx` have 230 val films but `meta.json` still lists
  only the 74 VerSe val cases — the nhanes val cases were added to the arrays and not written back.
- `aasce_fov96_ctx` has **no READY marker**.
- `nhanes_drr` is filed under `class=real_radiograph` in `rawfilms_r18_ce_v2.json` while being a DRR.

---

## 8. Where everything lives

Grid: `go2432@grid.wayne.edu`, home `/wsu/home/go/go24/go2432` (written `~` above).
Every grid command goes through WSL: `wsl -e bash -lc "ssh -o BatchMode=yes go2432@grid.wayne.edu '…'"`.
Grid python: `$HOME/mambaforge/envs/spineps/bin/python` (also `.../envs/fluorogen/bin/python`).

### Code
| What | Where |
|---|---|
| Repo (grid) | `~/spinesurg-ct-nnunet` |
| Repo (local) | `<repo spinesurg-ct-nnunet 097933a>` |
| Crop-bank builder | `~/spinesurg-ct-nnunet/tools/make_context_crops.py` |
| Recurrent head | `~/spinesurg-ct-nnunet/tools/recurrent_order.py`, launched by `slurm/recurrent_head.sh` |
| Second sequence head | `~/spinesurg-ct-nnunet/tools/stc_head.py` |
| Night arms | `~/spinesurg-ct-nnunet/slurm/night_arm.sh` → `tools/train_level_backbone.py`, `tools/diag_level_model.py`, `tools/eval_transitional.py` |
| One-image prototype | `~/spinesurg-ct-nnunet/tools/level_prototype.py` |
| FluoroCap inference | `~/spinesurg-ct-nnunet/tools/fluorocap_infer.py`, `fluorocap_infer_v2.py` |
| **FluoroCap / level-ID code is on branch `L6_Class` of `spinesurg-ct-nnunet`, which is PRIVATE.** Never push it to a public repo | |

### Data
| What | Where |
|---|---|
| Raw radiographs | `~/spine-detector/data/raw/{csxa, buu_full, buu_drive, buu_v1, cm_spine, nhanes_annotated, nhanes_full, aasce, vindr, mendeley_716, lateral_236, spinal_ai2024}` |
| Raw CT | `~/data/CTSpinoPelvic1K`, `~/data/TotalSegmentator`, `~/VerSeFusion` |
| Synthetic-hardware CT | `~/implant_ct`, `~/implant_verse`, `~/implant_ts` |
| Render / DRR directories | `~/{aasce,ctsp,verse,verse_soft,physics,nhanes,films,films_ap,vindr_det,vindr_pseudo,mendeley,spinalai,anchor}_drr`, `~/{ctsp,verse}_drr_obl{,2}`, `~/physics_rare`, `~/cut_{physics,rare}{,_v2}`, `~/exp3_{fluoro,radiograph}`, `~/fluorogen/synth_*`, `~/lstv_flag/renders*`, `~/lstv_eval/renders60`, `~/postop_render`, `~/*_smoke` |
| Crop banks | `~/*_ctx` (41 populated) plus `~/mv_bands` |
| Literature corpus | `~/FluoroCap` |
| Benchmark harness | `~/bench` |

### Models
| What | Where |
|---|---|
| Content-addressed registry | `~/model_registry/registry.jsonl`, store `~/model_registry/<sha16>/`, aliases `~/model_registry/aliases/`, MLflow SQLite (spineps env only), HF mirror |
| Bench registry (95 level classifiers, M01–M102) | `~/bench/model_registry.csv` and `.md` |
| Per-bank trained models | `~/<bank>_ctx/runs/model_rung_*.pt` + `result_rung_*.json` |
| Model-night arms | `~/model_night/runs/model_*.pt` + `result_*.json`; heads `~/model_night/heads/{films_all2,allspine_v2}/` |
| Detectors | `~/spine-detector/runs/pose/...`, inference copies in `~/FluoroCap/detect_*.pt` |
| Flags | `~/lstv_flag/models/` |
| Deployed bundle | `~/level_id_service/weights/` (detector.pt, level_model.pt, recurrent_head.pt, registry.json) |
| Serving rule | The website **never** serves weights. Inference sits behind `service/` with weights in the private HF repo `gregoryschwingmdphd/level-id-weights` |

### Results
| Surface | Where |
|---|---|
| Benchmark / competitor paradigms | `~/bench/xr_fov/` (`recurrent.json`, `recurrent_dump.json`, `recurrent_all2.json`, `fusion.json`, `summary.json`, `table.md`, `detector_robustness.json`, `dump_recurrent*.csv`) |
| Corruption suite | `~/bench/robust/` |
| Model night | `~/model_night/` — `runs/`, `diag_*.json`, `transitional/`, `realpanel/`, `rawfilms/`, `flags/`, `smoke/`, `logs/`, `timing/`, `RESULTS_snapshot.md` |
| Whole-spine recurrent | `~/model_night/recurrent_allspine_v2.json`, `~/model_night/recurrent_films_all2.json`, `~/track5/seed_*.json` |
| FluoroCap | `~/FluoroCap/` — `level_model_diag*.json`, `cut_eval_*.json`, `CORPUS_MANIFEST.md`, `LEVEL_COUNTS.md`, `MORNING_REPORT.md`, `infer_summary.json`, `classifier_report*.json` |
| LSTV / TLTV | `~/lstv_flag/` — `LSTV_FLAG_RESULTS.md`, `LEARNING_CURVE.md`, `ANOMALY_INVENTORY.md`, `oof_*.csv`, `curve/` |
| Overnight markers | `~/FluoroCap/MORNING_REPORT.md` first; markers `HIRES_REFRESH_DONE`, `ALLSPINE_V2_READY`, `RERUN_DONE`, `FINETUNE_CHAIN_DONE`, `CUT_EVAL_DONE`, `ROUND2_DONE`, `PATH_FETCH_DONE` |

### Grid discipline
- `#SBATCH --output` resolves against the **submit** directory — use `sbatch -D <dir>`.
- Prefer `afterany` over `afterok` and check the output yourself; `afterok` strands chains when a
  parent exits non-zero for a trivial reason.
- `/tmp` is node-local **and swept** — put IPC under `/dev/shm`.
- Partition `reqp` with `--qos=requeue` for CPU; GPU work uses `gmsap`/`gvohp`.
- `TMPDIR=$HOME/tmp`; strip CRLF from anything written on Windows.

## Competitor benchmark and ensemble (2026-09-18)

| path | what it is | written by |
|---|---|---|
| `~/model_night/competitors/<paradigm>.pt` | re-implemented published method, trained on our bank | `tools/train_competitors.py` |
| `~/model_night/competitors/<paradigm>.json` | what was trained, on which bank, validation accuracy, registry sha | same |
| `~/model_night/competitors/<paradigm>_val.npz` | per-crop posteriors on the held-out split, row-aligned across paradigms | same |
| `~/model_night/ensemble/ensemble.json` | all 124 method/rule/map cells with dev and test accuracy and n | `tools/ensemble_eval.py` |
| `docs/bank_profile_v3.json` | where the revisable crops sit on the spine, per level and per source | `tools/bank_region_profile.py` |
| `env/spineps.lock.txt` | the exact environment the grid ran, with CUDA build and driver | `scripts/export_env.sh` |
| `docs/research_registration_free_2026-09-18.json` | verified survey of registration-free level identification | deep research, 22 claims |

Paradigm keys: `ours`, `cina`, `kim`, `vertx`, `konya`. Checkpoints are registered through
`model_registry.try_register` with `push=False`; the login node's `sync` mirrors them.
