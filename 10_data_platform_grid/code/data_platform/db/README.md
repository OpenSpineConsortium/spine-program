# The index of the imaging holding

A SQLite database that indexes every item on the CephFS layout (`LAYOUT.md`): one row per CT volume, CBCT volume or
projection sweep, plain film, fluoroscopy frame or rendered image, with its source, subject, modality, position,
view, device, pixel or voxel size, path, size and format; plus the annotations each item carries, the splits it was
used in, and what it was derived from. Built by `build_index.py`, which reads each source folder's README.yaml to pick
the adapter that understands that folder.

## Files

| file | what |
|---|---|
| `SCHEMA.sql` | tables `source`, `subject`, `item`, `annotation`, `split`, `lineage`, bookkeeping `index_run` and `folder`, and five views |
| `build_index.py` | the indexer (Python 3.6+, standard library; uses pydicom when importable, and `tools/patient_keys.py` for subject keys) |
| `build_index.sbatch` | the job wrapper; the indexer refuses to run on the login node or outside a Slurm job |
| `test_build_index.py` | unit tests over a tiny synthetic layout (24 tests, including the folders the 2026-10-08 verifiers probed: CTSpine1K, AASCE, FluoroCap, TCIA, VerSeFusion, a hard link, an acquisition DICOM) |

## Running it

```bash
cd ~/spinesurg-ct-nnunet/data_platform/db && mkdir -p logs            # Slurm opens --output before the script runs
sbatch -D "$PWD" build_index.sbatch                                     # everything with a README.yaml
sbatch -D "$PWD" --export=ALL,FOLDERS="ctspinopelvic1k vindr_spinexr" build_index.sbatch
python3 test_build_index.py -v       # on a laptop or in a job (the tests pass --allow-local); never on warrior
```

A folder is indexed only when it holds a README.yaml, so the index grows batch by batch as `MIGRATION_PLAN.md` places
the READMEs. Re-running is incremental: an item whose size and mtime are unchanged is only touched, a changed item is
re-read (its annotations, splits and lineage are rewritten), and items that disappeared from a folder that was walked
completely are removed. `--hash small` adds the SHA-256 of files under 64 MB, `--hash all` of every file (slow).

**Counting each acquisition once.** Every item has `counted` (1 or 0) and the views count `counted = 1` only. A file
that is a hard link of an item already indexed gets `duplicate_of`, `counted = 0` and a `copy_of` lineage row (the
802 CTSP CTs and the build tree's `hf_export_osc/ct` share inodes). Conversions and outputs kept beside a DICOM
release (`tcia_nifti`, C-ArmLSpine `nifti/`, `spineps/`, `proto*/`), a release archive whose unpacked files are the
items, and a mask with no image are kept with `counted = 0`. A README.yaml `index_skip` list leaves a sub-path out
entirely (the HOME copy of CTSpine1K, `raw/home_copy`, beside the verified Ceph copy).

**Annotation status.** Where a file carries labels (a mask beside the image, a csv or json the adapter reads), the
annotation row comes from that file (`detail.scope` per-file). Where none is read, the item carries the release's
status from `sources.json` `annotation.status` (`detail.scope` "per-release, not read from the file"), so an AASCE
film is `release_labels` and a FluoroCap panel `pseudo` rather than `none`; `unknown` means the card does not say.
In a folder that holds masks, an image with no mask matched by name is `none`.

## Adapters

| adapter | folders | what it reads | what it fills |
|---|---|---|---|
| `ctsp_manifest` | `ctspinopelvic1k` | `manifest.json` (per record: position, sex, age band, scanner, prov_spine, prov_pelvis, Castellvi, series UID), `labels/`, `labels_v10/`, `splits_5fold.json` (keyed by TCIA token, mapped through the manifest), `../anomaly_harvest/ctsp/rows.csv` | CT items with position from the manifest; annotations: vertebrae expert or pseudo, pelvis expert or pseudo, ribs reviewed, Castellvi expert, v10 release labels, the harvest call (two_labeller, by subject key); 5-fold splits |
| `acquisition` | the family-B collections, `ctpelvic1k_clinic`, `validation_ts` | `../anomaly_harvest/<collection>/cases.csv` (case, ct, patient_key, extent), `convert/shard*.jsonl` (case to series UID), `rows.csv` / `registry_rows.csv` (calls), the fetcher's `fetch/verified.jsonl` (series UID to its `raw/` folder) + `FETCH_STATUS.json`, and one DICOM header per case | CT items keyed by the screen's patient key, with position (0018,5100), StudyDate, manufacturer and series UID from the series' first header (NBIA and IDC collections keep their DICOM); two_labeller annotation with the call as status; the fetch state per folder (`folder.fetch_status`) |
| `vindr_csv` | `vindr_spinexr` | `1.0.0/annotations/{train,test}.csv`, `*_images/*.dicom` | DX items keyed by study_id; release_labels where a lesion box exists, none for "No finding"; the release split |
| `buu` | `buu_lspine_*` | `AP/`, `LA/` jpg + csv | DX items, standing, view from the folder or the `Y0`/`Y1` digit; release_labels where the csv exists |
| `nhanes_tiff` / `nhanes_pickle` | `nhanes2_cdc_films` / `nhanes2_zenodo_landmarks` | `[CL]#####.tiff`; the landmark pickles | DX lateral items keyed `nhanes:<5 digits>`; release_labels for the pickles |
| `csxa` | `csxa_cervical_xray_atlas` | png + labelme json | DX cervical lateral items; release_labels where the json exists |
| `realxray_meta` | `realxray` | `<bank>/meta/<stem>.json` (case, device, kVp, px_mm, view angles, boxes, split) | XA (C-ArmLSpine), CBCT projections (COBRA), RF (DeepFluoro, Geneva) items with view from the angle, two_labeller annotations, the bank split, lineage to the source image |
| `cobra` | `cobra2026` | `cases/<case>/*.mha`, `meta/<case>/metadata.yaml` | CBCT sweep, planning CT and CBCT volume items with the StudyDate where present |
| `totalsegmentator` | `totalsegmentator_v201`, `totalsegmentator_v300` | `s####/ct.nii.gz`, `segmentations/`, `meta.csv`, `../anomaly_harvest/totalsegmentator/rows.csv` | CT items with sex, age, study type and the release split; the harvest call; the release zip kept, not counted |
| `verse` | `versefusion` | NIfTI and vertebra masks under `raw/VerSeFusion_data/{raw,canonical,corrected}`; `unified/` (links) and `qc/` are not indexed; `../anomaly_harvest/verse/rows.csv` | source and role from the first folder below `VerSeFusion_data`: `raw/` is `verse19_20` (role raw), `canonical/` and `corrected/` are `versefusion` (role converted); expert masks from the same tree; the harvest call |
| `dicom_tree` | `carmlspine`, `deepfluoro_vendor`, `tcia_ct_colonography` | DICOM directories (a series directory per CT/CBCT, a file per projection; headers through pydicom when present); volumes in other top folders | position from (0018,5100), view from ViewPosition or PositionerPrimaryAngle, StudyDate; conversions (`*nifti*`) and outputs beside the release kept with `counted = 0`, their masks attached |
| `render_bank` | `multisource_banks` and every `<folder>/derived/*` | `ann/*.json` + `img/*.npy` banks; `*_ctx` crop banks | RENDER items (DX for real-film banks, XA for the carm_* banks of real C-arm frames), one row per crop bank, keys through `tools/patient_keys.py key_any` |
| `generic` | everything else | files by extension | volumes and images with the source's modality (a volume is CBCT when its path says so, else the source's first volume modality) and the role of the top folder; mask-named volumes (`_seg`, `_msk`, `_mask`, `label`, `segmentation`, or under `labels*/`, `segmentations/`, `masks/`) attached to the image with the same case stem as annotation rows, never items; a same-stem sidecar (json, mat, txt, csv, xml) marks an image as labelled; otherwise the release's status, per-release |

## Subject keys

`<corpus>:<person>` in the spelling of `tools/patient_keys.py canon_key` (CTSP ids zero-padded to four digits, NHANES
to five, C-ArmLSpine `case<N>`, VinDr the study_id). Sources without people (FluoroCap, Spinal-AI2024) or keyed by
phantom get no key. Known limits, from the cards: TotalSegmentator v2.0.1 and v3.0.0 subject ids are not reconciled
(24 renumbered ids); a C-ArmLSpine case is a session, not provably one person; VerSe series are not subjects
(18 subjects own 37 series). `v_subjects_in_several_sources` lists every key that occurs in more than one source, the
query that would have caught the NHANES double inclusion.

## Views

- `v_annotated_ct_by_modality_position`: annotated CT and CBCT by modality, position and annotation kind.
- `v_unannotated_films_by_view`: plain films with no annotation beyond `none`, by source and view.
- `v_subject_items`: everything held for one subject (`WHERE subject_key = 'ctsp:0007'`), with annotations and splits.
- `v_source_summary`: per source, items, subjects, annotated items, modalities, bytes.
- `v_subjects_in_several_sources`: subject keys found in more than one source.

```sql
SELECT * FROM v_annotated_ct_by_modality_position ORDER BY n_items DESC;
SELECT source_id, view, n_films FROM v_unannotated_films_by_view ORDER BY n_films DESC;
SELECT modality, view, path FROM v_subject_items WHERE subject_key = 'nhanes:00160';
```

## Parquet export

SQLite is the store; Parquet is for analysis. With DuckDB (`pip install duckdb`):

```sql
INSTALL sqlite; LOAD sqlite;
ATTACH '/rs/rs_grp_oschome/go2432/data/_index/holding.sqlite' AS h (TYPE sqlite);
COPY (SELECT * FROM h.item) TO 'item.parquet' (FORMAT parquet);
COPY (SELECT * FROM h.annotation) TO 'annotation.parquet' (FORMAT parquet);
```

or with pandas: `pd.read_sql("SELECT * FROM item", sqlite3.connect(db)).to_parquet("item.parquet")`. Run either in a
job, not on the login node.

## What the index does not know

Patient position is `unknown` for every source whose files do not state it (TotalSegmentator, VerSe, CTSpine1K beyond
the CTSP records, and family-B collections that ship NIfTI or MHA only; see the cards). For the NBIA and IDC
collections the acquisition adapter reads (0018,5100) from each case's DICOM series. The index records what a file
says and never infers position from anatomy. Copies that are not hard links (a second download, a conversion whose
series is not matched) are counted once only where `index_skip` or the `counted` rules above name them; a
byte-identical copy elsewhere would need `--hash` and a content dedupe the indexer does not do. VinDr and BUU rows sit in a database under the oschome group: if the database is shared beyond go2432, those
rows (paths and keys only; no pixels) are a question for Greg under their DUA and EULA.
