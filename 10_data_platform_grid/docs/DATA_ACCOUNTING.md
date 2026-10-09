# Data accounting: every X-ray and every CT, keyed, traced, and checked for leakage

This document is the contract. It says what a *thing* is in this project, how its key is computed, what
happens to it at each stage of the pipeline, which directories on disk are the same data under another
name, and what "no leakage" is tested to mean. The counts are not written here by hand: the chain
`slurm/data_accounting.sh` generates them and splices them into the marked sections (§7). Every section
below marked **GENERATED** is machine-written; everything else is the hand-written rule the machine
implements.

A reviewer who wants to verify that nothing leaked should read §1 (what is being counted), §5 (what is
being checked) and then the generated tables in §7.

---

## 0. Why this exists

Three facts, each established elsewhere in this repo, make per-root bookkeeping insufficient.

**A dataset can be on disk twice under two names, and no root-level hash sees it.** DeepFluoro is
present as the JHU `ipcai_2020_full_res_data.h5` and as the vendor DICOMs of the *same 366 frames of
the same six cadaveric pelves*, downloaded from the JHU Dataverse (`tools/data_manifest.py`, roots
`deepfluoro_h5` and `deepfluoro_vendor`). The two copies are not byte-identical — different containers,
different compression — so the content-list SHA-256 of each root differs, as it should, and says nothing
about the fact that they are one dataset. A split drawn over "all roots" would put a frame in training
and its twin in test.

**This has already happened, and cost real results.** NHANES II entered the level-model banks twice:
once through `~/films_drr` (source `nhanes`, `patient_id nhanes_00160`) and once through `~/nhanes_drr`
(`NH_00160_c`, `NH_00160_l`, no `source` field, so it became a second source named `nhanes_drr`). The
split is drawn per source with one random stream, so the two copies of a patient landed independently:
**48 of 54 validation patients had their duplicate in training**
(`docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`). Every pooled real-film number over those banks includes
it. Nothing in the pipeline raised; the numbers were plausible and high.

**Corpus identity, not modality, is what the image statistics separate — so the corpus is part of an
item's identity.** Figure 1 row (d) of the RSNA AI manuscript projects 37 corpora (13,875 frames, 7,311
real) into one image-statistics space. Each C-arm does keep its own region: pairwise Bhattacharyya
overlap runs from 0.005 (DeepFluoro–Geneva) to 0.675 (Elekta–Geneva). But film versus fluoroscopy does
not transfer: a classifier with one corpus held out scores 71.1 % against a 71.8 % majority share, and
labels every unseen C-arm corpus as film. What those statistics separate is the corpus, not the
modality. The consequence for this document is direct: **a detector must be scored on a device held out
whole**, so "held out" is a property of a corpus and a device, not only of a random subset, and the leak
check tests it as such (CHK-5).

---

## 1. What a canonical item is, and how its key is computed

**An item is one acquisition, not one file.** One X-ray exposure, or one CT series. A file is a *store*
of an item. One item routinely has many stores: an HDF5 dataset member, a vendor DICOM series, an
exported 8-bit PNG, a 16-bit TIFF, a JPEG re-encode, a `.npy` of the same pixels. Counting files answers
nothing; counting items answers the question a reviewer is asking.

Three keys are computed, in this order, so that any claim made from them can be traced back to the
bytes it came from. Two of them are on the ledger row; the third is added by alias resolution and lives
in `canonical.jsonl`. The first column below is the **contract's** name for each; the second is the
field it is actually written under, because a reviewer reads the JSONL, not this table.

| key | field on the row | what it is | what it catches | what it misses |
|---|---|---|---|---|
| `store_key` | `sha256` | SHA-256 of the stored bytes, whole file. For a member inside a container (an h5 dataset, a crop-bank `.npz` member) the row is `<file>#<member>` with `physical: false` and a `parent_path`, so a frame inside a container is keyed like a frame in a file. | a byte-identical copy anywhere on disk | a re-export, a re-encode, a different container |
| `pixel_key` | `pix_sha256` (2-D), `vol_sha256` (3-D) | SHA-256 of a canonical reduction of the decoded data: grey, scaled to 8 bits by the 0.5–99.5 percentiles (as `corpus_manifold.load_gray` does, because `PIL.convert("L")` saturates 16-bit stores); a volume is instead trilinearly resampled to a 64³ grid and quantised, with its shape and spacing in the hash. | the same picture stored differently — a PNG export of an h5 frame, a JPEG of a TIFF | a crop, a resample, a mirror, a window change |
| — | `content_key`, `content_key_kind` | the key the row is actually compared on: `pix_sha256`, else `vol_sha256`, else the byte `sha256`, with `content_key_kind` saying which (`pix` / `vol` / `bytes` / `none`). **Read `content_key_kind` before comparing two rows**: a `bytes` row and a `pix` row do not answer the same question. | — | — |
| — | `dhash` | a 64-bit difference hash on an 8×9 box downsample. It is **not** the DCT pHash `data_alias.py` uses, and the two are never mixed: reading one as the other puts every pair about 32 bits apart and still reports full coverage. | a rescale or a lossy re-encode, approximately | — |
| `item_key` | `canonical_id`, in `canonical.jsonl` | the identity assigned by alias resolution (§3). It is **not** on the ledger row: `tools/data_alias.py canon` adds it, and `canonical.jsonl` is the ledger row plus this field. | — | — |

Two limits of the implementation, stated here rather than assumed away. A volume larger than
`--max-load-gb` (default 4 GB uncompressed) is recorded **header-only, with a note, and no
`vol_sha256`** — its `content_key` falls back to the byte hash, so a re-export of it is invisible;
there is no prefix-suffix key. And a file with no decoder available on the node (no SimpleITK, say)
gets `content_key_kind: "none"`; those rows are counted in the summary and merge with nothing.

**Equivalence.** Two stores are the same item when any of: identical `store_key`; identical `pixel_key`;
a declared alias edge (§3); or a pHash candidate that then reaches NCC64 ≥ `--ncc` (default 0.97).
`data_alias.py canon` decides this, it records **which** rule merged each pair in the group's
`evidence`, and pairs it *rejected* are kept in `alias_groups.json` under `rejected_by_ncc` rather than
dropped. The correlation is coarse on purpose: it finds a re-export, it does not find a mirror unless
the mirrored pHash is indexed (`--no-mirror` turns that off), and it fires on two different patients
photographed the same way. No contact sheet is drawn by this chain — the rejected list is what stands
in for one.

**A derived image is a new item with an inherited patient.** A DRR of a CT, a styled frame, a context
crop and the CT itself are four different items with four different `item_key`s and **one**
`patient_key`. Splits are enforced on `patient_key` (CHK-3), duplicates on `item_key` (CHK-1, CHK-2).
Conflating the two is how a bank can look disjoint by case name while training on the test patient's
other render.

---

## 2. The stages, and the tool that performs each

Data moves left to right. Every arrow is an edge in the lineage graph, and `tools/data_lineage.py`
writes the edge list that `tools/fig_data_flow.py` draws.

| # | stage | what happens | performed by | recorded as |
|---|---|---|---|---|
| S0 | source | an external release, with a DOI, a licence and a device | — | the root's card in `tools/data_manifest.py` `ROOTS` |
| S1 | landing | download / unpack into a root under `/rs/rs_grp_oschome/go2432/data` or `$HOME` | the per-corpus fetch scripts (`slurm/carmlspine_fetch.sh`, `slurm/cobra_fetch_varian.sh`, …) | root path, file count, bytes, content-list SHA-256 |
| S2 | registration | every file and every container member gets `store_key`, `pixel_key`, size, mtime, root, corpus | **`tools/data_ledger.py build`** (array shards) | `ledger/ledger_shard_<k>_of_<N>.jsonl`; `ledger/summary.json` from `data_ledger.py summary`, which counts the shards and never concatenates them |
| S3 | alias resolution | stores are collapsed into items; declared and discovered alias classes are recorded with their evidence | **`tools/data_alias.py canon`** | `canonical.jsonl` (one row per file, carrying its `canonical_id`), `alias_groups.json`, `alias_edges.csv`, `ALIAS_SUMMARY.md` |
| S4 | derivation | export to the common real-frame layout (`images/labels/meta/splits.json`), DRR rendering, device styling, context-crop cutting | `tools/realxray_*_export.py`, `tools/make_drr_dataset.py`, `tools/devcorpus_build.py`, `tools/make_context_crops.py` | parent `item_key` → child `item_key` edges |
| S5 | split assignment | train / val / test, per corpus or per fold | `make_context_crops.py` (per-source stream, `patient_id` / `--group-regex` / `--group-strip-suffix`), `splits.json`, `or_audit_splits.fold_of` | the split label on each child item |
| S6 | consumption | detector, encoder, head, sweep, benchmark | the trainers and `tools/head_mixed_length.py`, `tools/sweep_map.py`, the benchmark scripts | which bank each run read |
| S7 | claim | a number in a manuscript | `docs/RSNAI_CLAIMS.json`, `tools/claims_check.py` | the claim's bank, and therefore its items |

`tools/leak_check.py` reads S2–S6 and tests §5. `tools/fig_data_flow.py` draws the result as one
landscape figure in three panels, from `lineage.json`, `canonical.jsonl` and `leak_report.json` of the
same run: **(a)** the flow from source to model, node widths set by item count and coloured by domain
(fluoro / film / render / styled / literature); **(b)** a matrix of the roots that hold the same item,
which is where a corpus present twice under two names appears; **(c)** split integrity per bank, as the
leak check counted it. Nothing on it is typed in. It cross-checks the graph's per-node counts against
`canonical.jsonl`, stamps any disagreement on the figure in the failure colour, stamps the leak check's
own verdict, and **exits 1** when either says FAIL — so the figure reports rather than merely
illustrates.

---

## 3. Which roots are aliases of which

An **alias class** is a set of roots holding the same items under different names or in different
containers. The chain both *declares* the classes below (so a known alias cannot be missed because a
hash happened not to match) and *discovers* new ones by key collision (CHK-7), so a class nobody thought
of still surfaces. Discovered-but-undeclared classes are a finding, not an error to be suppressed.

| class | roots / directories | evidence | status |
|---|---|---|---|
| DeepFluoro | `~/deepfluoro/unpacked_full` (h5) · `…/data/deepfluoro_vendor/unpacked` (vendor DICOM) · `…/realxray/deepfluoro/images` (export) | same six specimens (17-1882, 17-1905, 18-0725, 18-1109, 18-2799, 18-2800), same 366 frames | **declared** |
| NHANES II | `~/films_drr` (source `nhanes`) · `~/nhanes_drr` (`NH_*`) · `~/spine-detector/data/raw/nhanes_full/*.tiff` · `…/yolo_v3/images/*/nhanes_*` | the same 543 annotated films from the same Zenodo pickles; `nhanes_00160` ≡ `NH_00160_c`/`_l` | **declared** — this is the class that leaked |
| BUU-LSPINE | `~/spine-detector/data/raw/buu_full/BUU-LSPINEv1/{AP,LA}` · `…/yolo_v3/images/*/buu_*` | same release; AP and LA are two items of one patient; three files are duplicated in the release itself (`… (1).jpg`) | **declared** |
| CSXA | `~/spine-detector/data/raw/csxa/images/datasets-PNG` · `…/yolo_v3/images/*/csxa_*` | same release | **declared** |
| Mendeley 716 | `~/spine-detector/data/raw/mendeley_716/extracted/Dataset` · `…/yolo_v3/images/*/mendeley_*` | same release | **declared** |
| C-ArmLSpine | `…/data/carmlspine/unpacked/C-ArmLSpine` · `…/realxray/carmlspine` · `…/data/carmlspine/pose` | export and registered poses of the same frames | **declared** (export edge, not a second copy of the pixels) |
| COBRA2026 | `…/data/cobra2026/cases` · `…/realxray/cobra_elekta` · `…/or_ready/devices/varian_halcyon/pairs` | export of the same projections | **declared** |
| Geneva hip | `…/data/realxray_work/geneva_hip` · `…/realxray/geneva_hip` | export of the same frames | **declared** |
| FluoroCap literature | `~/FluoroCap/{panels,openi,commons,pmc18m}` · `~/FluoroCap/real_fluoro_only` · `~/FluoroCap/real_grainy` · `~/spine-detector/data/yolo_v6f` | the curated sets are subsets of the harvest, **and the harvest contains the same figure republished across papers** — 72.8 % of panels have zero pixel residual against another panel | **declared**, and the within-harvest duplication is itself a class |
| CT → render | `~/data/CTSpinoPelvic1K` → `~/ctsp_drr`; VerSe → `~/verse_drr`; `~/data/TotalSegmentator_v3` → `~/ts_drr`; `~/physics_drr`, `~/physics_rare`, `…/devcorpus/styled/*` | derivation, not aliasing: a new item, the same patient | **derivation edge** |

Two further risks the chain tests rather than assumes:

- **VerSe'19 subjects inside VerSe'20.** The VerSe releases overlap by construction. Whether the copies
  on this disk overlap is a `pixel_key` question, and CHK-7 answers it.
- **CT colonography prone + supine.** CTSpinoPelvic1K draws on colonography cohorts, which image one
  person twice in one sitting; 351 separate-mode pelvic acquisitions are held out by design. Two case
  ids can therefore be one person, and the patient key must come from the release's own patient grouping,
  not from the case id.

---

## 4. How the patient key is formed, per corpus

The patient key is `<corpus>/<patient>` after normalisation, and a **subject key** joins the same person
across corpora and across spellings. The rules below are the contract; where a rule is marked UNVERIFIED
the chain reads the release and the generated table in §7 states what it found, because guessing a
patient key is exactly how the NHANES leak survived.

| corpus | how stores are named | patient key rule | the trap |
|---|---|---|---|
| DeepFluoro | specimen id in the path | the specimen (six cadaveric pelves) | 366 frames over six patients: a frame-level split is a patient-level leak |
| C-ArmLSpine | `case017_…` | `^(case\d+)_` (as `or_audit_dupes.case_of`) | AP, LAT and CBCT of one case are one patient |
| COBRA2026 | centre letter + case | centre + case | projections of one acquisition are not independent |
| Geneva hip | Yareta layout | the one resin phantom (`geneva:phantom`); keyed per position until 2026-09-24 | 19 positions of ONE phantom: a position is a view, not a patient |
| Ljubljana | `pairs/*.npz` | the spine specimen (18 gold-standard poses) | one specimen, many poses; handedness of the pairs is still undecided |
| SpineSAC | scenario + stem | the **phantom**, not the scenario — UNVERIFIED | the same phantom recurs across scenarios and devices |
| NHANES II | `nhanes_00160`, `NH_00160_c`, `NH_00160_l`, `C00160_cervical_masks_4.pkl` | the six-digit person number from any spelling → `nhanes/00160` | the cervical and lumbar films of one person; this is the key that did not exist when the banks were built |
| BUU-LSPINE | release `patient_id` | `patient_id`, AP and LA together | the three `… (1)` duplicates are the same patient |
| CSXA | one file per image | **one image = one patient, ASSUMED and untested** | if a patient contributed several images the CSXA split can leak; stated as not tested in the NHANES note |
| Mendeley 716 | `Dataset/<dir>/*.jpg` | the directory — UNVERIFIED | |
| VinDr-SpineXR | DICOM | StudyInstanceUID → patient | mixed vendors, mixed devices under one corpus name |
| AASCE | one file per image | one image = one patient, ASSUMED | |
| CTSpinoPelvic1K | `0001` in the release, `1` in the old CSVs | the release's patient grouping; case ids `zfill(4)` before any comparison | prone/supine colonography pairs are one person under two case ids |
| VerSe | subject id | subject | VerSe'19 ⊂ VerSe'20 |
| TotalSegmentator | `sXXXX` | subject | |
| FluoroCap literature | panel id | **unknown, and treated as unknown** | a republished figure is the same patient; the identity is the image, so these corpora are train-only and never carry a test claim |

---

## 5. What each leak check tests

`tools/leak_check.py` writes one row per check: the check id, what it compared, the count, PASS/FAIL, and
the offending keys (capped, with the full list in the JSON). The chain exits non-zero if any check fails;
a check that did not run is also non-zero, because a check that did not run is not a check that passed.

| id | tests | a failure means |
|---|---|---|
| CHK-1 | **item disjointness.** No `item_key` appears on two sides of any split, in any bank or `splits.json`. | the same picture was trained on and scored |
| CHK-2 | **alias closure.** No two stores in one alias class (§3) appear on opposite sides. | the NHANES failure, exactly: two copies, two streams, two sides |
| CHK-3 | **patient closure.** No `patient_key`, and no cross-corpus subject key, straddles a split — including derived items, which inherit the patient. | a different image of the test patient was in training |
| CHK-4 | **derivation closure.** For every S4 edge, parent and child are on the same side. | a render of a test CT trained the model that scores the CT |
| CHK-5 | **held out whole.** For every claim that names a held-out device or corpus, that corpus's items appear on exactly one side, and no alias of it appears on the other. Row (d) is the reason this is a check and not a nicety: the statistics separate the corpus, so a device half-held-out is not held out. | a "held-out device" result was scored on a device the model had seen |
| CHK-6 | **near-duplicates across splits.** NCC32 → NCC64 between train+val and test, within and across corpora, as `or_audit_dupes.py`; same-case and cross-case pairs classed separately and the top cross-case pairs drawn to a contact sheet. | a re-export or a republished figure crossed the split under a different key |
| CHK-7 | **undeclared alias.** Any `store_key` or `pixel_key` shared by roots that are not in one declared class. | a copy nobody knew about — the check that would have caught DeepFluoro and NHANES before either shipped |
| CHK-8 | **orphans and coverage.** Every item consumed at S6 traces to a ledger row, and every ledger row is reachable from a root card. | a bank is reading data that is not accounted for, so the clean sheet covers less than it appears to |
| CHK-9 | **evaluation vs selection and lineage.** For every row of `SchwingNet/results/eval_gate/quoted_results.json` -- every number the manuscript quotes -- and every (checkpoint, evaluation set) pair behind it, the evaluation set's patient keys (`eval_sets.json`) must not meet the **train OR val** keys of the checkpoint or of **any ancestor in its initialisation chain** (`touched.json`). A pair whose chain has an unresolved link, whose checkpoint has no lineage row, or whose evaluation set cannot be listed and keyed FAILS: unknown is not clean. | a quoted number was scored on patients its model trained on, was selected on, or inherited from the checkpoint it was fine-tuned from -- or nobody can say whether it was |

**Validation is seen.** A split used to choose a checkpoint -- Ultralytics keeps `best.pt` by val fitness,
`train_level_classifier.py` keeps the epoch with the best val accuracy -- has shaped that checkpoint, so a number
scored on it is a selection-set number, not a held-out one. Every check here, `tools/holdout.py` and the gate count
`train` AND `val` as seen. `holdout.trained_on(..., train_only_because="<why>")` is the only way to exclude the train
split alone, and it prints the reason. **Lineage is followed.** A checkpoint has seen everything its parent, its
parent's parent, and so on saw; only declared public ImageNet/COCO roots are exempt (§5.2).

Two honest limits, stated here rather than discovered later. CHK-6 is a correlation, not a proof: a
mirrored copy is not found, and two different patients photographed the same way do fire. And every
check is only as good as the patient key in §4 — the UNVERIFIED and ASSUMED rows are where a leak could
still hide, which is why they are named.

### 5.1 Which CHK is which row of the report

The CHK ids above are the contract. `leak_check.py` names its rows differently, and the two are not one
to one, so here is the crosswalk — including the entries nothing implements, which are stated rather
than left to be inferred from a table that looks complete.

| CHK | the row(s) in `leak_report.json` that answer it |
|---|---|
| CHK-1 item disjointness | `2_within_collection_merged_key`, *in part*: identical `store_key` / `pixel_key` reach it as identity groups from `canonical.jsonl` and the ledger, so two copies of one picture merge to one key. There is no standalone item-level row. |
| CHK-2 alias closure | `2_within_collection_merged_key` (the merge is what closes the alias) and `alias_gaps` for classes that cannot be resolved from disk |
| CHK-3 patient closure | `1_within_collection_builder_key` (per source — clean here means only that each source was split cleanly on its own) and `2_within_collection_merged_key` (across sources) |
| CHK-4 derivation closure | `5_render_pose_duplicates` for renders of one CT, plus the `leakage[]` rows of `lineage.json`, which computes the same question independently over the graph |
| CHK-5 held out whole | `4_eval_vs_training` and `6_styled_vs_real_device` |
| CHK-6 near-duplicates across splits | **not a row.** The near-duplicate ladder lives in `data_alias.py canon --pixels` (pHash → NCC64); what it merges arrives at CHK-1/2 as identity, and what it *rejected* is in `alias_groups.json` `rejected_by_ncc`. No contact sheet is drawn. |
| CHK-7 undeclared alias | `alias_groups.json`: groups whose `spans_roots` is true and whose roots are not one declared class; §7.2 lists them |
| CHK-8 orphans and coverage | the `census` and `verdict` of `leak_report.json` (`missing_collections`, `empty_collections`, `unresolved_lineage_refs`, unkeyed items) and the ledger's per-root null counts in §7.1 |
| CHK-9 evaluation vs selection and lineage | `9_eval_vs_selection_lineage` when `check` is given `--quoted-results --touched --eval-sets`; alone, `leak_check.py chk9` writes `chk9_report.json` and `CHK9_REPORT.md`. SEEN rows fail the run as a leak (exit 1); UNRESOLVED and NO EVAL KEYS rows fail it as not established (exit 3). Without `--quoted-results` the report prints **NOT RUN** for it. |

### 5.2 What a checkpoint touched: the initialisation chain

CHK-1..8 compare splits of banks. They say nothing about a model, and three things let a leak through that
seam on 2026-09-23 (the recall-vs-angle curve, `SchwingNet/results/arc/ARC_CHECK.md` item 4): the evaluators
made no gate call; `tools/holdout.py` counted only `split == "train"` as seen, so a subject used to SELECT
`best.pt` passed as held out; and nothing recorded what a checkpoint was initialised from, so a "real-only"
detector fine-tuned from a render detector that trained on the sweep subjects looked clean.

**The rule.** An evaluation item is held out for a checkpoint only if its patient key
(`tools/patient_keys.key_any`; a render inherits its source CT subject) is in neither the train nor the
val/selection set of that checkpoint, nor of any ancestor in its initialisation chain. Public ImageNet/COCO
pretraining is the only exempt ancestor, and only when declared (`PUBLIC_ROOT_RX`, `PUBLIC_TORCHVISION` in
`tools/checkpoint_lineage.py`).

`tools/checkpoint_lineage.py` computes the chain from what each run recorded: Ultralytics `train_args` inside the
checkpoint (checked against `args.yaml`), the data yaml and its lists; a level encoder's registry row, bank split
and result JSON, with its `--init` read from the `slurm/*.sh` line that wrote that exact file (the trainer did not
record it before 2026-09-23 and now does); a head's `.arch.json`; an LSTV flag's sidecar and folds csv. It writes
`touched.json` (`{checkpoint: {sha, parents, train_keys, val_keys, touched_keys, unresolved, ...}}`) for every
checkpoint a result names and every ancestor, and appends one row per checkpoint to
`~/model_registry/lineage.jsonl` (`model_registry.record_lineage`; `register()` now takes `parents`,
`train_list`, `val_list`). What it cannot read -- a family with no reader, a deleted bank, a list rewritten after
training began, an item no keying rule matches -- is an `unresolved` row, carried into every descendant: a
non-empty `unresolved` means `touched_keys` is a lower bound, never that the chain is empty.

The first full grid run (306 checkpoints, 183 with an unresolved link) showed which gaps were reading gaps rather
than missing records, and the tool now closes them from recorded evidence only:

- **A directory rewritten after training began** is read from Ultralytics' own label cache (`<labels dir>.cache`,
  the file list the run scanned) when that cache is dated no later than the run's start plus two minutes and holds
  files of this run's entries only. Two runs launched together on different lists share a cache path
  (`rx_lodo_cobra_elekta` and `rx_lodo_deepfluoro` both write `carmlspine/labels/test.cache`), so a cache holding
  a file outside the run's entries never stands in. A cache rewritten later by another scan leaves the entry unresolved.
- **A rewritten directory of an export that splits by patient deterministically** is bounded at the patient level.
  `tools/carmlspine_labels.py` sends a case to a split by `md5(case) % 10` (`split_of`, unchanged since its first
  commit, before the export existed), over the release's `case*` directories (unchanged since 2026-09-15). So whatever
  frames `realxray/carmlspine/images/<split>` held when a run began, their patients are the release cases that
  function sends to that split. The declaration (`DETERMINISTIC_SPLITS`) is checked on every use: the release must
  predate the run, and every frame the export holds now must sit where the function sends it. Otherwise the row
  stays unresolved and states its corpus (`corpus`), so a gate scoring another corpus can still decide.
- **A relative training cwd** is the candidate under which the run's own relative data yaml and model exist. A run in
  its own directory matches both of Ultralytics' layouts (detect_v3), and the first match had sent its data yaml to
  a directory that never held it.
- **A trainer or bank build launched inside `$(sbatch --wrap="...")`** is read from the wrapped command
  (allspine_v2's rung-1 model was "initialisation not recorded" only because of this). One **inside a shell
  function** (`crops () { local SRC=$1 DST=$2 ... }`) is read once per call site with that call's arguments bound.
  Read as a single line, `--dst "$H/$DST"` matched every bank and named `corpus_expand.sh` as a possible builder of
  allspine_v2.
- **A deleted bank** stays unresolved. Its row carries the upper bound its build line gives: the `--drr` roots
  `make_context_crops.py` drew it from, keyed as they stand today (`bounds.json`). The bound is marked incomplete
  when a root is gone, changed after the fit, cannot be expanded, or holds cases no rule keys.
- **Implant renders** whose `make_implant_ct` hardware records were deleted (`~/implant_ct`) are keyed to their source
  CT through the one build a launch script declares whose case-id format the name fits (ctsp `####`, TotalSegmentator
  `s####`, VerSe directory names; disjoint). No declared build fitting means refused.
- **New spellings keyed** (`tools/patient_keys.py`, `tools/leak_check.RULES`): view-only renders without a pose index
  (`totalseg_s0001_ap`, `verse_scan-verse533_ap`); `<bank>_drr__<case>` stems (`~/buu_yolo`); `CTSP_VERSE_<series>`;
  pseudo-labelled films, which meet their raw file's key (`NHANESPS_C00156` = `C00156.tiff` = `nhanes:00156`,
  `LAT236PS_000001` = `lateral_236/000001.jpg`); and the raw NHANES `C`/`L` prefix. Every name still unkeyed is
  counted by family in `touched_run.json` (`unkeyed_census`) and in LINEAGE.md, not only as eight examples.

### 5.3 The gate every evaluator calls

`touched.json` says what a checkpoint saw; `tools/eval_gate.py` is what stops a number being scored on it. It is not
opt-in. Every evaluator that loads a checkpoint and scores an evaluation set calls `assert_unseen(items, checkpoint,
where)` **before** it scores, and every scorer that reads such an evaluator's dump calls `carry()`:

| step | where the gate sits |
|---|---|
| loads a checkpoint | `realxray_eval.py`, `arc_recall_eval.py`, `arc_prior_check.py` (own frame vs another subject's frame vs a blank frame vs the anchor layout, on the arc set), `case134_sweep.py score`, `level_prototype.py` (detector, box and sacrum detectors, encoder, head, orientation net, flag models), `head_mixed_length.py` (encoder, `--init-head`, and the head it fits), `rigor_fixes.py a3a-rows` (each detector) and `a5-rows` (encoder + head), `device_fit.py fit` (each leave-one-group-out fold, by imaged subject; `device_fit.py gate` runs the fold gate alone from the pair names and writes `docs/devices/eval_gate/<device>.json`, the record CHK-9 reads for a card's rows), `learning_embed.py`, `fig4_pairs_pull.py` |
| loads a checkpoint, off the quoted path (wired 2026-09-24, VERIFY.md 1c) | `fig2_occlusion_clean.py` and `fig2_heldout_embed.py` (Figure 2, on the quoted path, previously ungated); `common_testset_eval`, `corpus_xray_gate_eval` (its per-crop `--cache` must also be the model's own, by sha256), `detector_failures`, `detector_quality`, `eval_anchor_free`, `eval_feasibility_claims`, `eval_fov_separability`, `eval_global_anomaly_signature`, `eval_interior_windows`, `eval_level_flags`, `eval_raw_films`, `eval_runtime_cost` (timing on real `--frames`; synthetic frames carry a not-held-out verdict), `eval_scaling_curves cases` (and `devices`/`fewshot` carry each arm's dump), `eval_shortcut_controls` (anatomy, scale, permute, order, anchor), `eval_surgeon_benefit`, `eval_transitional`, `eval_transitional_detectors`, `eval_windows_by_class`, `fiducial_walk`, `fluorocap_ablation_eval`, `night_eval_realpanels`, `realxray_robustness run`, `robustness_eval`, `sweep_map`, `thoracic_xr_eval`, `validate_guided`, `wholespine_eval`, each through `EG.gate_evaluation`. A read-out, head or baseline an evaluator fits on a bank's train split is passed as `also_seen`; `--allow-trained-on` becomes the gate's declaration |
| builds an evaluation set | `arc_unseen_subjects.py` chooses only TotalSegmentator subjects the gate passes for every detector the curve scores, refuses a subject whose CT is also filed under another TS id (the v201→v300 renumber, the duplicate groups), and runs `assert_unseen_all` on its own choice before writing it; `arc_angle_set.py --gate-weights` refuses the set before a frame is rendered and writes the verdict first in `SET_INFO.json` (the first arc set was the detectors' own selection subjects: `SchwingNet/results/arc/recall_vs_angle_selection_leaked/README.md`) |
| runs one of those | `devcorpus_train.py score`, `lcurve_train.py`, `or_recall_curves.py sweep` pass `--not-held-out` / `--touched` through; a refused cell leaves no dump (an earlier dump is kept as `*.before_rescore`, never deleted) |
| reads a dump | `carmlspine_pool_scores.py`, `lcurve_score.py`, `lcurve_report.py`, `fig3_detection_grid.py`, `or_lodo_rescore_outline.py`, `or_recall_curves.py curves`, `count_from_sacrum_eval.py`, `alphabet_couple.py`, `carmlspine_eval.py score`, `rigor_fixes.py a1`-`a9`, `SchwingNet/tools/{contribution_matrix,counting_report,coupling_report}.py`; `arc_curve_compare.py` refuses a new curve or prior check whose `eval_gate` block does not say held out |

What it does, in order:

1. **Keys every evaluation item** with `patient_keys.key_any` (the export's meta `case` and the stem, with the corpus
   its directory declares), then `patient_keys.canon_key`, applied to BOTH sides of every comparison: the C-ArmLSpine
   fold banks spell a case `case:100` and a frame keys to `carmlspine:case100`, and without one spelling the
   intersection would come back empty with the leak in it. An item no rule keys raises `UnkeyedEvalItem`.
2. **Finds the checkpoint's lineage** in `touched.json` (`$EVAL_GATE_TOUCHED`, then
   `/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/touched.json`, then the repo copy), by path and -- when the file is
   on the host -- by sha256, so a checkpoint retrained at the same path does not inherit the old row. A checkpoint with
   no row is resolved on demand through `checkpoint_lineage.Resolver` (grid only; cached under `ondemand/`), and one
   that still has none raises `UnresolvedLineage`.
3. **Walks the chain** -- the checkpoint, every `ancestors` entry, and every `parents` link through the store -- and
   intersects the evaluation keys with each node's `train_keys` and `val_keys`. A hit raises `SeenInEvaluation`, naming
   each key, the checkpoint or ancestor that holds it, and the split. A model fitted inside the evaluator (a head, a
   device-card fold) is passed as `also_seen` and checked the same way.
4. **Refuses an unresolved link** (`UnresolvedLineage`). The two bounds `checkpoint_lineage` records are the only
   things that decide one: a rewritten list whose `corpus` is not a corpus the evaluation holds, and a deleted bank
   whose `bound` is `complete` and holds no evaluation key (`bounds.json`). An incomplete bound decides nothing.
5. **Writes the verdict first** in the result JSON: `eval_gate` = {`gate_version`, `held_out`, `not_held_out_reason`,
   `overlap`, `unresolved`, `checks`: one header per checkpoint with its sha256, the evaluation set, `n_keys`,
   `overlap` (0 when held out), the ancestors and public roots it followed, and pose-donor overlap, which is REPORTED
   and does not decide: the rule is about patients, and a pose donor is not the imaged patient}.

**A key is never used as given (eval_gate/2).** A string handed to the gate in key form (`ts:s0585`, a `--keys` map
entry) goes through `patient_keys.resolve_key`: canonical spelling, an `implant:<case>_v<k>` key mapped to its source
CT exactly as the lineage store maps implant renders, and a person id of the shape its corpus names people
(`patient_keys.PERSON_FORMAT`; all 34,276 store keys fit). A key that names no person is unkeyed and raises. A dict
item's `key` never stands in for its `case`: every identity field is keyed and the union checked. (VERIFY.md 1b-iii:
`~/patient_keys_v9.json` sent 194 v9 val cases to `implant:` keys and hid 91 persons the encoder trained on.)

**A verdict is bound to the dump it travels with (eval_gate/2).** Every check records the `checkpoint_sha256` it
tested, its sorted `eval_keys` and their `eval_digest`. `stamp()` writes `weights_sha256` into the result itself,
hashed from the weight files at write time, and refuses to stamp a held-out block that did not check them. `carry()`
accepts a held-out block only when its checks are non-empty and complete, the dump's recorded sha256 set equals the
checked one, and the patients the dump scored key to exactly the tested set (a scorer's pooled output: contained in
it). A dump that records no sha256 -- every dump written before 2026-09-24 -- is refused unless declared, because the
file now at its weights path need not be the one that made it; `arc_recall_eval.py --matches` likewise refuses a
matches file whose recorded sha256 is not that of each `--weights` file (VERIFY.md 1b-i, 1b-ii). Such dumps are
re-scored, not re-labelled.

**The only way past it** is `--not-held-out "<reason>"`. The gate still computes everything, and the header says
`held_out: false` with the reason, so a not-held-out number can never be read as a held-out one. An empty reason is
refused. A hand table may only ever DECLARE a cell not held out (`or_recall_curves.declaration`, `lcurve_report.NOT_HELD_OUT`,
IN-TRAINING-DEVICE cells in `fig3_detection_grid`, `contribution_matrix`, `counting_report`); it can never make one held
out. A dump written before the gate existed carries no block: `carry()` gates it at scoring from the `weights` and
frames it records, a prototype run from `prototype_meta.json`'s models, a carmlspine_eval score through its `pred`
directory, and anything that names none of these raises `UngatedInput`. `rigor_fixes all` writes a refusal to
`<item>_gate_refused.json` and leaves the existing `<item>.json` in place, so a refused run never erases what a
reviewer compares against.

The first CHK-9 run (2026-09-23, jobs 40427275 and 40427457, reproduced locally from the copies in
`SchwingNet/results/eval_gate/`): 380 quoted rows, 31 SEEN, 40 UNRESOLVED, 240 HELD OUT, 69 N/A; the rows and their
reasons are in `SchwingNet/results/eval_gate/chk9/CHK9_REPORT.md`. The 40 UNRESOLVED rows are the ones the hand
inventory (`EVALUATORS.md`) called HELD OUT on a public-weights assumption; each traces to `allspine_v2_r1`, whose
training bank was deleted and whose upper bound is incomplete.

The EVAL_LEAKS sweep (2026-09-24, job 40429439; re-run as 40429833 after Geneva was keyed to its one phantom, with the same counts) re-ran CHK-9 over 563 rows. The 157 new rows are every number drawn
on a figure (`figures/figureN.record.json`), which the inventory had not read. Result: 81 SEEN, 58 UNRESOLVED,
323 HELD OUT and 101 N/A. Two changes to the check came with it:

- a row the inventory calls NOT HELD OUT, MIXED or NOT ESTABLISHED but that names no pair is UNRESOLVED, never N/A;
- a number computed under the median of a card's fold fits is checked as a `card_median:<device>` pair.

Every row, what was re-scored (old against new, with denominators) and what must rerun are in
`SchwingNet/results/eval_gate/EVAL_LEAKS.md`. 57 of the 58 UNRESOLVED rows still trace to `allspine_v2_r1`.

Checking the gate without the grid: `python -m pytest tests/test_eval_gate.py -v` (the arc leak on the 17 selection
subjects, rx_lodo_carmlspine_1024 through anchor_none_v2_17-1882, a genuinely unseen C-ArmLSpine case, an unresolved
parent, the two spellings, declarations, `holdout.py`, CHK-9), against a synthetic store shaped like the leak and,
when this checkout has it, the real `touched.json`.

---

## 6. How to re-run the whole thing

On the grid, as two submissions (the second re-checks the first's shard markers and refuses to run on a
partial ledger). The runner never submits itself.

```bash
cd $HOME/spinesurg-ct-nnunet
A=$(sbatch --parsable -D $HOME/spinesurg-ct-nnunet --array=0-15 \
     --export=ALL,STAGE=ledger slurm/data_accounting.sh)
sbatch -D $HOME/spinesurg-ct-nnunet --dependency=afterany:$A \
     --export=ALL,STAGE=rest --cpus-per-task=8 --mem=64G --time=04:00:00 \
     --output=/wsu/home/go/go24/go2432/model_night/logs/data_accounting_rest_%j.out \
     slurm/data_accounting.sh
```

Everything lands in `$OUT`, which defaults to
`/rs/rs_grp_oschome/go2432/data/or_ready/data_accounting`. These are the files, by the names the tools
actually write, and the flag each one arrives under:

| file | written by |
|---|---|
| `ledger/ledger_shard_<k>_of_<N>.jsonl`, `ledger/summary_shard_<k>_of_<N>.json` | `data_ledger.py build --out $OUT/ledger --shard <k> --n-shards <N>` |
| `ledger/summary.json` | `data_ledger.py summary --out $OUT/ledger --gen-dir $OUT/generated` |
| `canonical.jsonl`, `alias_groups.json`, `alias_edges.csv`, `ALIAS_SUMMARY.md` | `data_alias.py canon --ledger $OUT/ledger --out $OUT` |
| `lineage.json`, `lineage.md` | `data_lineage.py build --out $OUT/lineage.json --ledger $OUT/canonical.jsonl` |
| `leak_report.json`, `leak_inventory.json`, `DATA_LEAKAGE_REPORT.md`, `leak_check.log` | `leak_check.py check --out $OUT --canonical … --alias-groups … --ledger <each shard> --lineage-graph …` |
| `fig_data_flow.png`, `fig_data_flow.pdf` | `fig_data_flow.py --src $OUT --out $OUT/fig_data_flow.png` |
| `generated/{ledger_summary,alias_classes,patient_keys,lineage_edges,leak_results,figure}.md` | `data_ledger summary` and `leak_check` write their own through `--gen-dir`; the runner renders the other four from this run's JSON |
| `DATA_ACCOUNTING.filled.md` | the runner, splicing those six into a copy of this document |

Every stage is handed the previous stage's files **by path**: nothing reads a tool's default, because a
default points at whatever ran last. The chain's log echoes each command as a `+ …` line before running
it, so the log is the record of what ran rather than a transcription of this table.

The repo copy of this file is not modified by the chain.

To read the outcome without reading the log: `grep DATA_ACCOUNTING_LEAK_CHECK` in the stage-2 log gives
`PASS` or `FAIL`, and the job's exit code is the leak check's. The chain also exits non-zero when a
stage wrote nothing (`STAGE_PRODUCED_NOTHING`), when the shards exited 0 over fewer than
`MIN_LEDGER_ROWS` rows, or when any of the six fragments could not be rendered — because a check that
did not run is not a check that passed. `fig_data_flow`'s own exit 1 is the one exception: it means the
figure is *reporting* a FAIL verdict it was handed, and the leak check's code already carries that.

Re-running only the shards that failed: the stage-2 log prints the missing shard numbers and the
`--array=` list to resubmit. A shard whose marker exists is skipped unless `FORCE=1`.

### 6.1 Checking the runner without the grid

The chain cannot be trusted on the strength of reading it: a wrong flag makes `argparse` exit 2, the
runner carries on, and the next stage reads a file nobody wrote. So there is a synthetic corpus with a
known answer, and the runner is driven over it exactly as the grid drives it.

```bash
python tools/diagnostics/make_fake_corpus.py --out /tmp/fake_leak            # with a planted leak
python tools/diagnostics/make_fake_corpus.py --out /tmp/fake_clean --clean   # without one
```

Each prints the `ALLOW_LOCAL=1 STAGE=all … bash slurm/data_accounting.sh` line that runs the whole
chain over the tree it just built. The planted leak is the NHANES II defect in miniature: one person
under two spellings in two render directories, byte-identical, and a crop bank that puts one spelling
in `train` and the other in `val`.

| tree | what must happen |
|---|---|
| `--clean` | `LEAK_CHECK PASS`, every check 0, chain exits **0** |
| default | check (1) **0** — each source was split cleanly on its own, which is what was true while NHANES leaked — and checks (2), (3), (4) non-zero; chain exits **1** |

A runner that exits 0 on both is not reading the report. Both trees also carry one volume present under
two names in two roots, byte for byte: an **alias**, not a leak, which must appear in
`alias_groups.json` as one canonical id spanning two roots and must change no verdict.

---

## 7. Generated tables

Everything in this section is written by the chain. In the repo copy these blocks are empty by design —
a number here that was not generated would be a number nobody computed. Each `<!-- BEGIN:GENERATED
<name> -->` block is filled from `$OUT/generated/<name>.md`, and the filled copy is written to
`$OUT/DATA_ACCOUNTING.filled.md`; this file in git is never edited by the chain.

`data_ledger.py summary` and `leak_check.py check` write their own fragment (`--gen-dir`); the runner
renders `alias_classes`, `patient_keys`, `lineage_edges` and `figure` from `alias_groups.json`,
`canonical.jsonl`, `lineage.json` and the PNG of the same run. Every fragment names the file it was read
from on its last line, and a fragment that could not be rendered says so in the document and fails the
run — an empty block must never be readable as "nothing to report".

### 7.1 The ledger

<!-- BEGIN:GENERATED ledger_summary -->
<!-- END:GENERATED ledger_summary -->

### 7.2 Alias classes, declared and discovered

<!-- BEGIN:GENERATED alias_classes -->
<!-- END:GENERATED alias_classes -->

### 7.3 Patient keys as actually read from each release

<!-- BEGIN:GENERATED patient_keys -->
<!-- END:GENERATED patient_keys -->

### 7.4 Lineage: the edges data actually took

<!-- BEGIN:GENERATED lineage_edges -->
<!-- END:GENERATED lineage_edges -->

### 7.5 Leak checks

<!-- BEGIN:GENERATED leak_results -->
<!-- END:GENERATED leak_results -->

### 7.6 The figure

<!-- BEGIN:GENERATED figure -->
<!-- END:GENERATED figure -->

---

## 8. What this does not cover

- **Labels.** The ledger keys images and volumes. A label file is keyed as a store but its agreement
  with its image is a different audit (`tools/or_audit_splits.py`, the rib and vertebra QC tools).
- **Broken symlinks.** `imagesTr` links in Dataset813 point at container paths that resolve only inside
  Singularity and must never be repaired on the host. The ledger records the link target and marks the
  row unresolved rather than following it.
- **Truncated files.** A short file has a valid hash. Size is recorded, and CTSpinoPelvic1K CT 0533 was
  truncated — in the RELEASE, not on the grid: the HuggingFace object carries the same sha256. Repaired
  from TCIA on 2026-09-23 (job 40416624), so banks built before that hold 801 of 802 and after it 802; a
  size that disagrees with the release is a finding for the manifest check, not for the leak check.
- **Banks already deleted.** `allspine_v2` … `v5c` were deleted on 2026-09-20. Their build logs record
  what they contained; the ledger cannot key what is gone, and any claim resting on them is a claim
  resting on a log.
- **Nothing here rebuilds a bank.** Finding a leak is not fixing it. The fix for the NHANES class is one
  NHANES directory, or a split drawn over subject keys across sources; neither has been done.
