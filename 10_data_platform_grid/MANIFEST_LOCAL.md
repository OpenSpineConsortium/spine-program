# MANIFEST_LOCAL.md: what was copied into this folder, from where, and what was not

**This record is history, not a dependency.** The laptop paths below say where each copy came from on 2026-10-08. Nothing in this folder depends on them: the repositories of `MANIFEST_CODE.md` (URL and commit) and the grid paths of `MANIFEST_GRID.md` are the only outside references the work needs. Laptop paths appear in this file only.

Files copied: 688 (47,289,018 B). Files whose copy differs from its source (an inserted header, a status line or a redaction): 123. Nothing copied is a symbolic link or junction, an imaging volume, a weight file, an archive, a credential, a log over 2 MB or a file over 25 MB.

## 1. The copy rules, as applied

- Copied: text, code, documents, result files (md, json, jsonl.gz, tsv, csv, txt, py, sh, sbatch, sql, yaml, yml, tex, bib, log under 2 MB) and six small evidential PNG renders (`results/spineps_ids/repair/render/`, 170-375 KB each).
- Never copied: imaging data (nii, nii.gz, dcm, npz, npy, h5, mha), weights (pt, pth, ckpt), zips, anything under `.git` or `__pycache__`, environment folders, logs over 2 MB, files over 25 MB, credential or token files, the `.beethoven-vendor` folder, and personal or administrative material. Symbolic links and junctions were never followed.
- Redacted by kind, never by value: two researcher e-mail addresses, one library contact (address and telephone), three usernames (an administrator's, a student's, another user's); the institutional mailboxes `hpc@wayne.edu` and `IRBQuestions@wayne.edu` and the grid login `go2432` are kept. The banned word was found in one copied file (`code/spine_data_review/tests/check_template_prose.py`, the tool that counts it) and rewritten so the file no longer spells it; a folder-wide search finds no other occurrence.
- Headers: loose scripts under `code/tools/` and `code/handoff_builders/` carry an inserted first-line comment with source path, commit and state. Whole-folder copies (`code/data_platform/`, `code/spine_data_review/`, `code/env/`) carry a `SOURCE.md` instead and stay byte-identical (the `batch_items/*.tsv` must match the grid copies the jobs read). Every memory note carries a status line inserted after its frontmatter.

## 2. Every file copied, by folder

### `code/data_platform/` (181 files, 9,551,871 B)

Source and note: `ssn:data_platform/ whole, relative paths intact; byte-identical to the repository at 097933a`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `code/data_platform/.gitignore` | 45 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/.gitignore` |  |
| `code/data_platform/DATA_MANIFEST.md` | 938,971 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/DATA_MANIFEST.md` |  |
| `code/data_platform/LAYOUT.md` | 55,805 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/LAYOUT.md` |  |
| `code/data_platform/MIGRATION_PLAN.md` | 55,625 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/MIGRATION_PLAN.md` |  |
| `code/data_platform/README.md` | 2,051 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/README.md` |  |
| `code/data_platform/VERIFICATION.md` | 35,285 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/VERIFICATION.md` |  |
| `code/data_platform/db/README.md` | 10,441 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/db/README.md` |  |
| `code/data_platform/db/SCHEMA.sql` | 11,905 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/db/SCHEMA.sql` |  |
| `code/data_platform/db/build_index.py` | 58,839 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/db/build_index.py` |  |
| `code/data_platform/db/build_index.sbatch` | 1,549 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/db/build_index.sbatch` |  |
| `code/data_platform/db/logs/.gitkeep` | 0 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/db/logs/.gitkeep` |  |
| `code/data_platform/db/test_build_index.py` | 21,186 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/db/test_build_index.py` |  |
| `code/data_platform/dedup/DEDUP_PLAN.md` | 125,825 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/DEDUP_PLAN.md` |  |
| `code/data_platform/dedup/HASH_RESULTS.md` | 4,366 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/HASH_RESULTS.md` |  |
| `code/data_platform/dedup/INDEX_ALIASES.md` | 10,930 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/INDEX_ALIASES.md` |  |
| `code/data_platform/dedup/applied/.gitkeep` | 0 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/applied/.gitkeep` |  |
| `code/data_platform/dedup/build_dedup_plan.py` | 164,500 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/build_dedup_plan.py` |  |
| `code/data_platform/dedup/dedup_apply.sbatch` | 37,753 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/dedup_apply.sbatch` |  |
| `code/data_platform/dedup/dedup_groups.json` | 137,136 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/dedup_groups.json` |  |
| `code/data_platform/dedup/dedup_guard.sh` | 3,139 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/dedup_guard.sh` |  |
| `code/data_platform/dedup/dedup_hash.sbatch` | 18,171 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/dedup_hash.sbatch` |  |
| `code/data_platform/dedup/dedup_lib.sh` | 13,446 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/dedup_lib.sh` |  |
| `code/data_platform/dedup/dedup_plan.tsv` | 7,055 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/dedup_plan.tsv` |  |
| `code/data_platform/dedup/hash_results/.gitkeep` | 0 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/.gitkeep` |  |
| `code/data_platform/dedup/hash_results/A01.json` | 208,870 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A01.json` |  |
| `code/data_platform/dedup/hash_results/A01.tsv` | 141,979 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A01.tsv` |  |
| `code/data_platform/dedup/hash_results/A02.json` | 384,249 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A02.json` |  |
| `code/data_platform/dedup/hash_results/A02.tsv` | 239,854 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A02.tsv` |  |
| `code/data_platform/dedup/hash_results/A03.json` | 787,803 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A03.json` |  |
| `code/data_platform/dedup/hash_results/A03.tsv` | 492,059 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A03.tsv` |  |
| `code/data_platform/dedup/hash_results/A04.json` | 154,092 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A04.json` |  |
| `code/data_platform/dedup/hash_results/A04.tsv` | 114,159 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A04.tsv` |  |
| `code/data_platform/dedup/hash_results/A05.json` | 1,240 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A05.json` |  |
| `code/data_platform/dedup/hash_results/A05.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A05.tsv` |  |
| `code/data_platform/dedup/hash_results/A06.json` | 1,466 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A06.json` |  |
| `code/data_platform/dedup/hash_results/A06.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A06.tsv` |  |
| `code/data_platform/dedup/hash_results/A07.json` | 368,463 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A07.json` |  |
| `code/data_platform/dedup/hash_results/A07.tsv` | 282,585 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A07.tsv` |  |
| `code/data_platform/dedup/hash_results/A08.json` | 4,375 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A08.json` |  |
| `code/data_platform/dedup/hash_results/A08.tsv` | 2,104 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A08.tsv` |  |
| `code/data_platform/dedup/hash_results/A09.json` | 1,558 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A09.json` |  |
| `code/data_platform/dedup/hash_results/A09.tsv` | 634 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A09.tsv` |  |
| `code/data_platform/dedup/hash_results/A10.json` | 349,998 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A10.json` |  |
| `code/data_platform/dedup/hash_results/A10.tsv` | 189,883 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A10.tsv` |  |
| `code/data_platform/dedup/hash_results/A11.json` | 960 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A11.json` |  |
| `code/data_platform/dedup/hash_results/A11.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A11.tsv` |  |
| `code/data_platform/dedup/hash_results/A12.json` | 960 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A12.json` |  |
| `code/data_platform/dedup/hash_results/A12.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A12.tsv` |  |
| `code/data_platform/dedup/hash_results/A13.json` | 955 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A13.json` |  |
| `code/data_platform/dedup/hash_results/A13.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A13.tsv` |  |
| `code/data_platform/dedup/hash_results/A14.json` | 908 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A14.json` |  |
| `code/data_platform/dedup/hash_results/A14.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A14.tsv` |  |
| `code/data_platform/dedup/hash_results/A15.json` | 897 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A15.json` |  |
| `code/data_platform/dedup/hash_results/A15.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A15.tsv` |  |
| `code/data_platform/dedup/hash_results/A16.json` | 1,347 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A16.json` |  |
| `code/data_platform/dedup/hash_results/A16.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A16.tsv` |  |
| `code/data_platform/dedup/hash_results/A17.json` | 1,026 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A17.json` |  |
| `code/data_platform/dedup/hash_results/A17.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A17.tsv` |  |
| `code/data_platform/dedup/hash_results/A18.json` | 1,022 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A18.json` |  |
| `code/data_platform/dedup/hash_results/A18.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A18.tsv` |  |
| `code/data_platform/dedup/hash_results/A19.json` | 4,005 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A19.json` |  |
| `code/data_platform/dedup/hash_results/A19.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A19.tsv` |  |
| `code/data_platform/dedup/hash_results/A22.json` | 1,032 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A22.json` |  |
| `code/data_platform/dedup/hash_results/A22.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A22.tsv` |  |
| `code/data_platform/dedup/hash_results/A23.json` | 1,381 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A23.json` |  |
| `code/data_platform/dedup/hash_results/A23.tsv` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A23.tsv` |  |
| `code/data_platform/dedup/index_aliases.csv` | 583,101 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/index_aliases.csv` |  |
| `code/data_platform/dedup/logs/dedup_hash_40581845.out` | 7,206 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/logs/dedup_hash_40581845.out` |  |
| `code/data_platform/dedup/logs/dedup_hash_40581924.out` | 307 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/logs/dedup_hash_40581924.out` |  |
| `code/data_platform/dedup/test_dedup.sh` | 31,218 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/dedup/test_dedup.sh` |  |
| `code/data_platform/lib/mini_yaml.py` | 10,320 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/lib/mini_yaml.py` |  |
| `code/data_platform/plan/RSNAI_DATA_MANIFEST.remapped.json` | 9,390 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/RSNAI_DATA_MANIFEST.remapped.json` |  |
| `code/data_platform/plan/batch_items/B00.tsv` | 200 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B00.tsv` |  |
| `code/data_platform/plan/batch_items/B01.tsv` | 803 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B01.tsv` |  |
| `code/data_platform/plan/batch_items/B02.tsv` | 5,147 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B02.tsv` |  |
| `code/data_platform/plan/batch_items/B03.tsv` | 354 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B03.tsv` |  |
| `code/data_platform/plan/batch_items/B04.tsv` | 1,864 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B04.tsv` |  |
| `code/data_platform/plan/batch_items/B05.tsv` | 490 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B05.tsv` |  |
| `code/data_platform/plan/batch_items/B06.tsv` | 1,616 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B06.tsv` |  |
| `code/data_platform/plan/batch_items/B07.tsv` | 719 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B07.tsv` |  |
| `code/data_platform/plan/batch_items/B08.tsv` | 306 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B08.tsv` |  |
| `code/data_platform/plan/batch_items/B09.tsv` | 921 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B09.tsv` |  |
| `code/data_platform/plan/batch_items/B10.tsv` | 7,579 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B10.tsv` |  |
| `code/data_platform/plan/batch_items/B11.tsv` | 8,131 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B11.tsv` |  |
| `code/data_platform/plan/batch_items/B13.tsv` | 374 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B13.tsv` |  |
| `code/data_platform/plan/batch_items/B14.tsv` | 1,339 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/batch_items/B14.tsv` |  |
| `code/data_platform/plan/build_plan.py` | 52,984 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/build_plan.py` |  |
| `code/data_platform/plan/census_merge.py` | 3,617 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/census_merge.py` |  |
| `code/data_platform/plan/cutover.sh` | 7,662 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/cutover.sh` |  |
| `code/data_platform/plan/disk_map.csv` | 211,314 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/disk_map.csv` |  |
| `code/data_platform/plan/layout_map.csv` | 126,089 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/layout_map.csv` |  |
| `code/data_platform/plan/logs/.gitkeep` | 0 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/logs/.gitkeep` |  |
| `code/data_platform/plan/migrate_batch.sbatch` | 9,525 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/migrate_batch.sbatch` |  |
| `code/data_platform/plan/migration_batches.csv` | 1,387 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/migration_batches.csv` |  |
| `code/data_platform/plan/path_refs_by_item.csv` | 54,193 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/path_refs_by_item.csv` |  |
| `code/data_platform/plan/path_refs_files.csv` | 661,137 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/path_refs_files.csv` |  |
| `code/data_platform/plan/path_refs_summary.csv` | 50,573 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/path_refs_summary.csv` |  |
| `code/data_platform/plan/plan_summary.json` | 4,073 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/plan_summary.json` |  |
| `code/data_platform/plan/preflight.sbatch` | 3,803 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/preflight.sbatch` |  |
| `code/data_platform/plan/publish_visibility.sh` | 5,638 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/publish_visibility.sh` |  |
| `code/data_platform/plan/readme_yaml/aasce2019_boostnet.yaml` | 1,077 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/aasce2019_boostnet.yaml` |  |
| `code/data_platform/plan/readme_yaml/abdomenatlas3_mini.yaml` | 837 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/abdomenatlas3_mini.yaml` |  |
| `code/data_platform/plan/readme_yaml/amos22.yaml` | 784 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/amos22.yaml` |  |
| `code/data_platform/plan/readme_yaml/aortaseg60.yaml` | 759 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/aortaseg60.yaml` |  |
| `code/data_platform/plan/readme_yaml/barts_crl.yaml` | 786 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/barts_crl.yaml` |  |
| `code/data_platform/plan/readme_yaml/buu_lspine_2000.yaml` | 793 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/buu_lspine_2000.yaml` |  |
| `code/data_platform/plan/readme_yaml/buu_lspine_3600.yaml` | 914 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/buu_lspine_3600.yaml` |  |
| `code/data_platform/plan/readme_yaml/buu_lspine_v1_smoke.yaml` | 697 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/buu_lspine_v1_smoke.yaml` |  |
| `code/data_platform/plan/readme_yaml/carmlspine.yaml` | 1,664 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/carmlspine.yaml` |  |
| `code/data_platform/plan/readme_yaml/cm_spine_drive_file.yaml` | 748 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/cm_spine_drive_file.yaml` |  |
| `code/data_platform/plan/readme_yaml/cobra2026.yaml` | 744 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/cobra2026.yaml` |  |
| `code/data_platform/plan/readme_yaml/csi2014.yaml` | 752 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/csi2014.yaml` |  |
| `code/data_platform/plan/readme_yaml/csxa_cervical_xray_atlas.yaml` | 819 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/csxa_cervical_xray_atlas.yaml` |  |
| `code/data_platform/plan/readme_yaml/ctpelvic1k.yaml` | 772 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ctpelvic1k.yaml` |  |
| `code/data_platform/plan/readme_yaml/ctpelvic1k_clinic.yaml` | 916 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ctpelvic1k_clinic.yaml` |  |
| `code/data_platform/plan/readme_yaml/ctsp0533_repair.yaml` | 691 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ctsp0533_repair.yaml` |  |
| `code/data_platform/plan/readme_yaml/ctsp_april.yaml` | 772 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ctsp_april.yaml` |  |
| `code/data_platform/plan/readme_yaml/ctspine1k.yaml` | 702 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ctspine1k.yaml` |  |
| `code/data_platform/plan/readme_yaml/ctspinopelvic1k.yaml` | 1,522 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ctspinopelvic1k.yaml` |  |
| `code/data_platform/plan/readme_yaml/ctspinopelvic1k_build_tree.yaml` | 2,354 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ctspinopelvic1k_build_tree.yaml` |  |
| `code/data_platform/plan/readme_yaml/curvas.yaml` | 745 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/curvas.yaml` |  |
| `code/data_platform/plan/readme_yaml/curvas_pdacvi.yaml` | 789 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/curvas_pdacvi.yaml` |  |
| `code/data_platform/plan/readme_yaml/d815_repair.yaml` | 847 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/d815_repair.yaml` |  |
| `code/data_platform/plan/readme_yaml/deep_psma.yaml` | 785 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/deep_psma.yaml` |  |
| `code/data_platform/plan/readme_yaml/deepfluoro_h5.yaml` | 796 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/deepfluoro_h5.yaml` |  |
| `code/data_platform/plan/readme_yaml/deepfluoro_vendor.yaml` | 838 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/deepfluoro_vendor.yaml` |  |
| `code/data_platform/plan/readme_yaml/devcorpus.yaml` | 940 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/devcorpus.yaml` |  |
| `code/data_platform/plan/readme_yaml/devcorpus_arc.yaml` | 948 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/devcorpus_arc.yaml` |  |
| `code/data_platform/plan/readme_yaml/external.yaml` | 855 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/external.yaml` |  |
| `code/data_platform/plan/readme_yaml/fluorocap.yaml` | 1,030 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/fluorocap.yaml` |  |
| `code/data_platform/plan/readme_yaml/fluorogen_synthetic.yaml` | 823 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/fluorogen_synthetic.yaml` |  |
| `code/data_platform/plan/readme_yaml/geneva_hip_src.yaml` | 728 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/geneva_hip_src.yaml` |  |
| `code/data_platform/plan/readme_yaml/idc.yaml` | 3,204 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/idc.yaml` |  |
| `code/data_platform/plan/readme_yaml/ieee_dataport_lateral_fullspine_236.yaml` | 899 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ieee_dataport_lateral_fullspine_236.yaml` |  |
| `code/data_platform/plan/readme_yaml/kidney_thoraxabdomen.yaml` | 842 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/kidney_thoraxabdomen.yaml` |  |
| `code/data_platform/plan/readme_yaml/ljubljana.yaml` | 778 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ljubljana.yaml` |  |
| `code/data_platform/plan/readme_yaml/mendeley_5jdfdgp762.yaml` | 853 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/mendeley_5jdfdgp762.yaml` |  |
| `code/data_platform/plan/readme_yaml/multisource_banks.yaml` | 3,788 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/multisource_banks.yaml` |  |
| `code/data_platform/plan/readme_yaml/nhanes2_cdc_films.yaml` | 871 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/nhanes2_cdc_films.yaml` |  |
| `code/data_platform/plan/readme_yaml/nhanes2_zenodo_landmarks.yaml` | 879 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/nhanes2_zenodo_landmarks.yaml` |  |
| `code/data_platform/plan/readme_yaml/nlst_pilot.yaml` | 783 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/nlst_pilot.yaml` |  |
| `code/data_platform/plan/readme_yaml/or_ready.yaml` | 694 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/or_ready.yaml` |  |
| `code/data_platform/plan/readme_yaml/outline_conv.yaml` | 650 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/outline_conv.yaml` |  |
| `code/data_platform/plan/readme_yaml/panorama.yaml` | 773 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/panorama.yaml` |  |
| `code/data_platform/plan/readme_yaml/pengwin2026.yaml` | 806 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/pengwin2026.yaml` |  |
| `code/data_platform/plan/readme_yaml/polypose.yaml` | 1,063 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/polypose.yaml` |  |
| `code/data_platform/plan/readme_yaml/quadra_hc.yaml` | 795 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/quadra_hc.yaml` |  |
| `code/data_platform/plan/readme_yaml/rare_class.yaml` | 1,070 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/rare_class.yaml` |  |
| `code/data_platform/plan/readme_yaml/realxray.yaml` | 1,665 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/realxray.yaml` |  |
| `code/data_platform/plan/readme_yaml/realxray_work.yaml` | 1,212 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/realxray_work.yaml` |  |
| `code/data_platform/plan/readme_yaml/ribfrac.yaml` | 708 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/ribfrac.yaml` |  |
| `code/data_platform/plan/readme_yaml/rsna_2022_cspine.yaml` | 793 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/rsna_2022_cspine.yaml` |  |
| `code/data_platform/plan/readme_yaml/spinal_ai2024.yaml` | 890 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/spinal_ai2024.yaml` |  |
| `code/data_platform/plan/readme_yaml/spine_detector_corpus.yaml` | 941 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/spine_detector_corpus.yaml` |  |
| `code/data_platform/plan/readme_yaml/spineps.yaml` | 1,152 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/spineps.yaml` |  |
| `code/data_platform/plan/readme_yaml/spinesac.yaml` | 785 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/spinesac.yaml` |  |
| `code/data_platform/plan/readme_yaml/tcia_ct_colonography.yaml` | 820 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/tcia_ct_colonography.yaml` |  |
| `code/data_platform/plan/readme_yaml/tcia_fdg_pet_ct_lesions.yaml` | 849 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/tcia_fdg_pet_ct_lesions.yaml` |  |
| `code/data_platform/plan/readme_yaml/thoracic_xr.yaml` | 812 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/thoracic_xr.yaml` |  |
| `code/data_platform/plan/readme_yaml/totalsegmentator_v201.yaml` | 889 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/totalsegmentator_v201.yaml` |  |
| `code/data_platform/plan/readme_yaml/totalsegmentator_v300.yaml` | 953 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/totalsegmentator_v300.yaml` |  |
| `code/data_platform/plan/readme_yaml/validation_ts.yaml` | 978 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/validation_ts.yaml` |  |
| `code/data_platform/plan/readme_yaml/versefusion.yaml` | 1,691 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/versefusion.yaml` |  |
| `code/data_platform/plan/readme_yaml/vindr.yaml` | 764 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/vindr.yaml` |  |
| `code/data_platform/plan/readme_yaml/vindr_spinexr.yaml` | 1,103 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/vindr_spinexr.yaml` |  |
| `code/data_platform/plan/readme_yaml/waw_tace.yaml` | 778 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/waw_tace.yaml` |  |
| `code/data_platform/plan/readme_yaml/xrspinopelvic1k.yaml` | 965 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/readme_yaml/xrspinopelvic1k.yaml` |  |
| `code/data_platform/plan/remap_manifest.py` | 1,938 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/remap_manifest.py` |  |
| `code/data_platform/plan/test_migration.sh` | 12,107 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/test_migration.sh` |  |
| `code/data_platform/plan/verify_transfer.py` | 10,821 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/plan/verify_transfer.py` |  |
| `code/data_platform/reacquire/README.md` | 9,533 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/reacquire/README.md` |  |
| `code/data_platform/reacquire/logs/.gitkeep` | 0 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/reacquire/logs/.gitkeep` |  |
| `code/data_platform/reacquire/reacquire.py` | 38,109 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/reacquire/reacquire.py` |  |
| `code/data_platform/reacquire/reacquire.sbatch` | 1,820 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/reacquire/reacquire.sbatch` |  |
| `code/data_platform/reacquire/test_reacquire.py` | 23,376 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/reacquire/test_reacquire.py` |  |
| `code/data_platform/sources.json` | 1,041,283 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/sources.json` |  |
| `code/data_platform/sources.yaml` | 999,843 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/sources.yaml` |  |
| `code/data_platform/spot_checks.json` | 5,781 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/spot_checks.json` |  |
| `code/data_platform/sync_sources_yaml.py` | 1,461 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/sync_sources_yaml.py` |  |
| `code/data_platform/verification_report.json` | 5,741 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/verification_report.json` |  |
| `code/data_platform/verify_planning.py` | 14,404 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/data_platform/verify_planning.py` |  |

### `code/env/` (4 files, 27,673 B)

Source and note: `ssn:env/ whole`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `code/env/README.md` | 2,509 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/env/README.md` |  |
| `code/env/fluorogen.yml` | 11,199 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/env/fluorogen.yml` |  |
| `code/env/spineps.lock.txt` | 7,181 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/env/spineps.lock.txt` |  |
| `code/env/spineps.yml` | 6,784 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/env/spineps.yml` |  |

### `code/handoff_builders/` (7 files, 46,759 B)

Source and note: `HANDOFF/working_notes/builders (header added)`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `code/handoff_builders/build_context_export.py` | 12,708 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/build_context_export.py` | yes |
| `code/handoff_builders/build_context_index.py` | 7,772 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/build_context_index.py` | yes |
| `code/handoff_builders/check_paths.py` | 9,847 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/check_paths.py` | yes |
| `code/handoff_builders/check_refs.py` | 2,192 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/check_refs.py` | yes |
| `code/handoff_builders/copy_context.py` | 5,388 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/copy_context.py` | yes |
| `code/handoff_builders/patch_helper.py` | 1,833 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/patch_helper.py` | yes |
| `code/handoff_builders/refresh_context.py` | 7,019 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/builders/refresh_context.py` | yes |

### `code/spine_data_review/` (272 files, 3,066,852 B)

Source and note: `ssn:spine_data_review/ tracked part`; `ssn:spine_data_review/ tracked part (working tree, uncommitted edit on 2026-10-08)`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `code/spine_data_review/.gitignore` | 1,749 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/.gitignore` |  |
| `code/spine_data_review/Makefile` | 11,242 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/Makefile` |  |
| `code/spine_data_review/PIPELINE.md` | 46,518 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/PIPELINE.md` |  |
| `code/spine_data_review/PRISMA-ScR_checklist.md` | 10,195 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/PRISMA-ScR_checklist.md` |  |
| `code/spine_data_review/PROTOCOL.md` | 100,847 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/PROTOCOL.md` |  |
| `code/spine_data_review/README.md` | 10,685 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/README.md` |  |
| `code/spine_data_review/_drafts/data-engineer/PRISMA-ScR_checklist.md` | 5,879 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/data-engineer/PRISMA-ScR_checklist.md` |  |
| `code/spine_data_review/_drafts/data-engineer/PROTOCOL.md` | 21,364 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/data-engineer/PROTOCOL.md` |  |
| `code/spine_data_review/_drafts/data-engineer/charting_schema.json` | 15,467 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/data-engineer/charting_schema.json` |  |
| `code/spine_data_review/_drafts/data-engineer/information_sources.md` | 42,475 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/data-engineer/information_sources.md` |  |
| `code/spine_data_review/_drafts/data-engineer/quality_rubric.md` | 5,923 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/data-engineer/quality_rubric.md` |  |
| `code/spine_data_review/_drafts/data-engineer/statistical_analysis_plan.md` | 8,208 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/data-engineer/statistical_analysis_plan.md` |  |
| `code/spine_data_review/_drafts/methodologist/PRISMA-ScR_checklist.md` | 6,459 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/methodologist/PRISMA-ScR_checklist.md` |  |
| `code/spine_data_review/_drafts/methodologist/PROTOCOL.md` | 31,449 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/methodologist/PROTOCOL.md` |  |
| `code/spine_data_review/_drafts/methodologist/charting_schema.json` | 16,142 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/methodologist/charting_schema.json` |  |
| `code/spine_data_review/_drafts/methodologist/information_sources.md` | 33,276 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/methodologist/information_sources.md` |  |
| `code/spine_data_review/_drafts/methodologist/quality_rubric.md` | 9,905 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/methodologist/quality_rubric.md` |  |
| `code/spine_data_review/_drafts/methodologist/statistical_analysis_plan.md` | 12,897 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/methodologist/statistical_analysis_plan.md` |  |
| `code/spine_data_review/_drafts/rq_main.tex` | 38,677 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_main.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/agreement.tex` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/agreement.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/availability.tex` | 130 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/availability.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/checklist.tex` | 10,331 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/checklist.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/counts.tex` | 118 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/counts.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/datasets_main.tex` | 139 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/datasets_main.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/deviations.tex` | 23,952 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/deviations.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/eligibility.tex` | 7,805 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/eligibility.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/grid.tex` | 115 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/grid.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/items.tex` | 11,301 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/items.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/numbers.tex` | 8,159 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/numbers.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/pooled_variants.tex` | 139 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/pooled_variants.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/quality.tex` | 138 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/quality.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/search_strings.tex` | 226,090 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/search_strings.tex` |  |
| `code/spine_data_review/_drafts/rq_tables/sources.tex` | 7,592 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/_drafts/rq_tables/sources.tex` |  |
| `code/spine_data_review/charting/aliases.csv` | 1,466 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/charting/aliases.csv` |  |
| `code/spine_data_review/charting/datasets.jsonl` | 0 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/charting/datasets.jsonl` |  |
| `code/spine_data_review/charting/validation_report.json` | 1,120 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/charting/validation_report.json` |  |
| `code/spine_data_review/charting_schema.json` | 40,251 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/charting_schema.json` |  |
| `code/spine_data_review/data/charting/README.md` | 4,609 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/data/charting/README.md` |  |
| `code/spine_data_review/data/screening/decisions.csv` | 138 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/data/screening/decisions.csv` |  |
| `code/spine_data_review/grid_inventory.csv` | 1,479 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/grid_inventory.csv` |  |
| `code/spine_data_review/information_sources.md` | 63,475 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/information_sources.md` |  |
| `code/spine_data_review/licence_tiers.csv` | 2,790 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/licence_tiers.csv` |  |
| `code/spine_data_review/manuscript/allowed_literals.txt` | 570 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/manuscript/allowed_literals.txt` |  |
| `code/spine_data_review/manuscript/build.sh` | 7,680 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/manuscript/build.sh` |  |
| `code/spine_data_review/manuscript/main.tex` | 38,123 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/manuscript/main.tex` |  |
| `code/spine_data_review/manuscript/refs.bib` | 16,297 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/manuscript/refs.bib` |  |
| `code/spine_data_review/manuscript/template.tex` | 35,432 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/manuscript/template.tex` |  |
| `code/spine_data_review/quality_rubric.md` | 14,335 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/quality_rubric.md` |  |
| `code/spine_data_review/queries/literature.yaml` | 287,544 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/queries/literature.yaml` |  |
| `code/spine_data_review/queries/repositories.yaml` | 242,639 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/queries/repositories.yaml` |  |
| `code/spine_data_review/recipe/README.md` | 8,740 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/recipe/README.md` |  |
| `code/spine_data_review/recipe/prepare_splits.py` | 12,239 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/recipe/prepare_splits.py` |  |
| `code/spine_data_review/requirements.txt` | 390 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/requirements.txt` |  |
| `code/spine_data_review/run_all.sh` | 1,660 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/run_all.sh` |  |
| `code/spine_data_review/runs/pilot-2026-09-19/queries.json` | 2,239 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/runs/pilot-2026-09-19/queries.json` |  |
| `code/spine_data_review/screen/known_items.csv` | 6,950 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/screen/known_items.csv` |  |
| `code/spine_data_review/screen/llm/prompts/v1.txt` | 2,613 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/screen/llm/prompts/v1.txt` |  |
| `code/spine_data_review/sdr/__init__.py` | 717 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/__init__.py` |  |
| `code/spine_data_review/sdr/availability.py` | 50,098 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/availability.py` |  |
| `code/spine_data_review/sdr/chart.py` | 26,819 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/chart.py` |  |
| `code/spine_data_review/sdr/common.py` | 36,729 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/common.py` |  |
| `code/spine_data_review/sdr/creds.py` | 9,812 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/creds.py` |  |
| `code/spine_data_review/sdr/dedup_prescreen.py` | 39,723 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/dedup_prescreen.py` |  |
| `code/spine_data_review/sdr/descriptives.py` | 15,619 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/descriptives.py` |  |
| `code/spine_data_review/sdr/estimators.py` | 11,155 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/estimators.py` |  |
| `code/spine_data_review/sdr/figures.py` | 21,001 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/figures.py` |  |
| `code/spine_data_review/sdr/flow_counts.py` | 16,289 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/flow_counts.py` |  |
| `code/spine_data_review/sdr/ids.py` | 8,524 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/ids.py` |  |
| `code/spine_data_review/sdr/manuscript.py` | 26,418 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/manuscript.py` |  |
| `code/spine_data_review/sdr/manuscript_tables.py` | 48,064 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/manuscript_tables.py` |  |
| `code/spine_data_review/sdr/quality.py` | 28,827 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/quality.py` |  |
| `code/spine_data_review/sdr/recipe.py` | 37,620 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/recipe.py` |  |
| `code/spine_data_review/sdr/repo_run.py` | 25,287 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/repo_run.py` |  |
| `code/spine_data_review/sdr/search_figure_routes.py` | 25,581 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/search_figure_routes.py` |  |
| `code/spine_data_review/sdr/search_literature.py` | 43,502 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/search_literature.py` |  |
| `code/spine_data_review/sdr/search_platforms.py` | 20,306 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/search_platforms.py` |  |
| `code/spine_data_review/sdr/search_repositories.py` | 26,174 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/search_repositories.py` |  |
| `code/spine_data_review/sdr/stats.py` | 24,475 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/sdr/stats.py` |  |
| `code/spine_data_review/statistical_analysis_plan.md` | 27,504 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/statistical_analysis_plan.md` |  |
| `code/spine_data_review/tables/agreement.tex` | 128 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/agreement.tex` |  |
| `code/spine_data_review/tables/availability.tex` | 130 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/availability.tex` |  |
| `code/spine_data_review/tables/checklist.tex` | 10,279 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/checklist.tex` |  |
| `code/spine_data_review/tables/counts.tex` | 118 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/counts.tex` |  |
| `code/spine_data_review/tables/datasets_main.tex` | 139 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/datasets_main.tex` |  |
| `code/spine_data_review/tables/deviations.tex` | 1,244 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/deviations.tex` |  |
| `code/spine_data_review/tables/eligibility.tex` | 7,662 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/eligibility.tex` |  |
| `code/spine_data_review/tables/grid.tex` | 115 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/grid.tex` |  |
| `code/spine_data_review/tables/items.tex` | 9,988 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/items.tex` |  |
| `code/spine_data_review/tables/numbers.tex` | 7,428 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/numbers.tex` |  |
| `code/spine_data_review/tables/pooled_variants.tex` | 139 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/pooled_variants.tex` |  |
| `code/spine_data_review/tables/quality.tex` | 138 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/quality.tex` |  |
| `code/spine_data_review/tables/search_strings.tex` | 186,283 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/search_strings.tex` |  |
| `code/spine_data_review/tables/sources.tex` | 4,736 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tables/sources.tex` |  |
| `code/spine_data_review/tests/check_chart_report.py` | 2,172 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_chart_report.py` |  |
| `code/spine_data_review/tests/check_log_cache.py` | 2,748 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_log_cache.py` |  |
| `code/spine_data_review/tests/check_no_credentials.py` | 2,646 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_no_credentials.py` |  |
| `code/spine_data_review/tests/check_query_strings.py` | 4,444 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_query_strings.py` |  |
| `code/spine_data_review/tests/check_repo_queries.py` | 4,153 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_repo_queries.py` |  |
| `code/spine_data_review/tests/check_run.py` | 13,920 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_run.py` |  |
| `code/spine_data_review/tests/check_run_hygiene.py` | 9,404 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_run_hygiene.py` |  |
| `code/spine_data_review/tests/check_screen_counts.py` | 5,207 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_screen_counts.py` |  |
| `code/spine_data_review/tests/check_template_prose.py` | 1,201 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/check_template_prose.py` |  |
| `code/spine_data_review/tests/count_appendix_rows.py` | 730 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/count_appendix_rows.py` |  |
| `code/spine_data_review/tests/diff_run_dirs.py` | 4,433 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/diff_run_dirs.py` |  |
| `code/spine_data_review/tests/diff_runs.py` | 2,388 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/diff_runs.py` |  |
| `code/spine_data_review/tests/expected_chart_errors.json` | 722 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/expected_chart_errors.json` |  |
| `code/spine_data_review/tests/expected_screen_counts.json` | 868 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/expected_screen_counts.json` |  |
| `code/spine_data_review/tests/fixture_lit_queries.yaml` | 723 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_queries.yaml` |  |
| `code/spine_data_review/tests/fixture_lit_run/counts.json` | 6,547 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/counts.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/queries.json` | 24,739 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/queries.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/arxiv/059ce93bf7d7d956b2a5cfcb73bfd8396f34e14c.json` | 732 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/arxiv/059ce93bf7d7d956b2a5cfcb73bfd8396f34e14c.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/arxiv/0df37812a46e8e2d5b77dbedeabf03690c48dfba.json` | 559 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/arxiv/0df37812a46e8e2d5b77dbedeabf03690c48dfba.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/arxiv/3e8dca404356cff74fbdcb2ca20aa0e5841a648e.json` | 559 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/arxiv/3e8dca404356cff74fbdcb2ca20aa0e5841a648e.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/arxiv/55f4af66e87db2d2b74172fc545a4e308d9a237f.json` | 879 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/arxiv/55f4af66e87db2d2b74172fc545a4e308d9a237f.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/arxiv/6bbcffb50dc66d707b3e314577efec5b99c6fc18.json` | 563 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/arxiv/6bbcffb50dc66d707b3e314577efec5b99c6fc18.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/arxiv/a2d1579ad33279b6518ea11be07c825156253d98.json` | 559 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/arxiv/a2d1579ad33279b6518ea11be07c825156253d98.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/arxiv/b9cf8d2ef1d5af8463ceadaa936542aed1bf54a1.json` | 559 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/arxiv/b9cf8d2ef1d5af8463ceadaa936542aed1bf54a1.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/biorxiv/4c35c1cfb0e61c5cca09febab1353bbf32229ec4.json` | 594 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/biorxiv/4c35c1cfb0e61c5cca09febab1353bbf32229ec4.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/biorxiv/b6b38baa0bff6257369b385fafa2d21bf8bd8789.json` | 581 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/biorxiv/b6b38baa0bff6257369b385fafa2d21bf8bd8789.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/crossref/18a5f12d9c1865c204cfe6df628c6c881d309af2.json` | 875 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/crossref/18a5f12d9c1865c204cfe6df628c6c881d309af2.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/crossref/227f305f28cae461a5e5c0180b8e3ccbc1a675d9.json` | 575 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/crossref/227f305f28cae461a5e5c0180b8e3ccbc1a675d9.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/crossref/490d32c5ae4ba1efe828b54e9edb275279453243.json` | 941 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/crossref/490d32c5ae4ba1efe828b54e9edb275279453243.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/crossref/6dc22386a02cadb1177da4f2885a388b92fde092.json` | 581 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/crossref/6dc22386a02cadb1177da4f2885a388b92fde092.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/crossref/880cc7e76e45dd71ab01cea0722675184c63b6d8.json` | 586 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/crossref/880cc7e76e45dd71ab01cea0722675184c63b6d8.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/crossref/d147f8c88a7c1d0ee6e351062507a6b7fef6eb76.json` | 702 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/crossref/d147f8c88a7c1d0ee6e351062507a6b7fef6eb76.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/epmc/003d1faf748f55955d7545b38304b4a4ee6baabe.json` | 515 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/epmc/003d1faf748f55955d7545b38304b4a4ee6baabe.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/epmc/1fbfa4b077c945beba7f6a4988c67f7887350d7e.json` | 517 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/epmc/1fbfa4b077c945beba7f6a4988c67f7887350d7e.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/epmc/664b20a3f49eb0c647ff65fec300a422fc013bf0.json` | 781 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/epmc/664b20a3f49eb0c647ff65fec300a422fc013bf0.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/openalex/41cf604a3d3f3a647cc842c556a9bace900376e2.json` | 536 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/openalex/41cf604a3d3f3a647cc842c556a9bace900376e2.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/openalex/49b4e30c7710253dd758040e0f79b5cb61f309ae.json` | 581 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/openalex/49b4e30c7710253dd758040e0f79b5cb61f309ae.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/openalex/785b751537c29f0c8966e4944ee8028ca88f85b8.json` | 698 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/openalex/785b751537c29f0c8966e4944ee8028ca88f85b8.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/openalex/a1d8fc63bac7bf39223e0d361f9b4ba41aaf5eee.json` | 754 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/openalex/a1d8fc63bac7bf39223e0d361f9b4ba41aaf5eee.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/openalex/e84184ee0b55ff253e58f99315282ec738edcf62.json` | 806 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/openalex/e84184ee0b55ff253e58f99315282ec738edcf62.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/6cca914039e8f94e9b898be9a3f7ba04ec1a177b.json` | 1,379 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/6cca914039e8f94e9b898be9a3f7ba04ec1a177b.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/70de94a4b966369b7d7bf97cd386293cea80c249.json` | 435 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/70de94a4b966369b7d7bf97cd386293cea80c249.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/79941dfc843a5d075b0c370d4fe73e8b581c274d.json` | 483 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/79941dfc843a5d075b0c370d4fe73e8b581c274d.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/8521fcecfa224346afeacd987f92b19131a4be3c.json` | 483 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/8521fcecfa224346afeacd987f92b19131a4be3c.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/8b35c2d54f8690fcced2e3aae11c81cd26b67109.json` | 485 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/8b35c2d54f8690fcced2e3aae11c81cd26b67109.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/8d112f09c7b12e2a8247078fac0bed1318536908.json` | 483 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/8d112f09c7b12e2a8247078fac0bed1318536908.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/e2bc80c447dcb81bf657544e311cddb347b1bb70.json` | 483 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/e2bc80c447dcb81bf657544e311cddb347b1bb70.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/pubmed/e60f73d395af763bf7c45d97e8b85f37a2f3e9ec.json` | 1,426 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/pubmed/e60f73d395af763bf7c45d97e8b85f37a2f3e9ec.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/s2/2a0aab95b74c6237e55d17b3708c026ab0c3006c.json` | 668 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/s2/2a0aab95b74c6237e55d17b3708c026ab0c3006c.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/raw/s2/6861a143023f3810687be672100efd67673f28de.json` | 550 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/raw/s2/6861a143023f3810687be672100efd67673f28de.json` |  |
| `code/spine_data_review/tests/fixture_lit_run/records/arxiv.jsonl` | 1,599 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/records/arxiv.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/records/biorxiv.jsonl` | 1,137 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/records/biorxiv.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/records/crossref.jsonl` | 2,682 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/records/crossref.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/records/epmc.jsonl` | 1,692 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/records/epmc.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/records/openalex.jsonl` | 1,696 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/records/openalex.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/records/pubmed.jsonl` | 1,555 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/records/pubmed.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/records/s2.jsonl` | 1,670 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/records/s2.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/requests.log.jsonl` | 17,477 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/requests.log.jsonl` |  |
| `code/spine_data_review/tests/fixture_lit_run/run_meta.json` | 1,444 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_lit_run/run_meta.json` |  |
| `code/spine_data_review/tests/fixture_meta.json` | 2,200 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixture_meta.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-authors-own.json` | 9,452 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-authors-own.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-comparable-group.json` | 9,461 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-comparable-group.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-derived-flag.json` | 9,442 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-derived-flag.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-extra-key.json` | 9,453 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-extra-key.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-figure-basis.json` | 9,451 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-figure-basis.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-host-type.json` | 9,439 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-host-type.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-id-mismatch.json` | 9,432 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-id-mismatch.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-licence-spdx.json` | 9,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-licence-spdx.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-missing-quote.json` | 9,271 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-missing-quote.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-origin-by-type.json` | 9,404 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-origin-by-type.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-probe-gap.json` | 9,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-probe-gap.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-route-rule.json` | 9,441 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-route-rule.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/bad-year.json` | 9,435 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/bad-year.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/probe-ccby3.json` | 9,432 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/probe-ccby3.json` |  |
| `code/spine_data_review/tests/fixtures/chart_screen/verse.json` | 9,432 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/chart_screen/verse.json` |  |
| `code/spine_data_review/tests/fixtures/queries_tiny.json` | 6,273 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/queries_tiny.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-commercial.json` | 801 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-commercial.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-dryad.json` | 829 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-dryad.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-dua.json` | 864 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-dua.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-figshare.json` | 823 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-figshare.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-files.json` | 1,232 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-files.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-gc.json` | 810 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-gc.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-generic-browser.json` | 814 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-generic-browser.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-generic-fileurl.json` | 845 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-generic-fileurl.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-github.json` | 806 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-github.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-hf-gated.json` | 822 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-hf-gated.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-hf-open.json` | 818 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-hf-open.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-kaggle.json` | 836 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-kaggle.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-mendeley-nover.json` | 832 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-mendeley-nover.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-mendeley.json` | 841 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-mendeley.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-on-grid.json` | 819 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-on-grid.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-osf.json` | 786 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-osf.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-physionet-open.json` | 837 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-physionet-open.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-request.json` | 720 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-request.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-tcia.json` | 838 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-tcia.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-unavailable.json` | 808 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-unavailable.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/datasets/fx-zenodo.json` | 830 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/datasets/fx-zenodo.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/enrichment/fx-files.json` | 270 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/enrichment/fx-files.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/quality_real_shape.json` | 1,625 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/quality_real_shape.json` |  |
| `code/spine_data_review/tests/fixtures/recipe/quality_value_shape.json` | 2,714 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/recipe/quality_value_shape.json` |  |
| `code/spine_data_review/tests/fixtures/run_tiny/counts.json` | 242 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/run_tiny/counts.json` |  |
| `code/spine_data_review/tests/fixtures/run_tiny/queries.json` | 986 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/run_tiny/queries.json` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/arxiv.jsonl` | 544 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/arxiv.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/crossref.jsonl` | 543 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/crossref.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/figshare.jsonl` | 964 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/figshare.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/github.jsonl` | 504 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/github.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/jstage.jsonl` | 467 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/jstage.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/openalex.jsonl` | 1,249 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/openalex.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/pubmed.jsonl` | 2,459 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/pubmed.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/pwc.jsonl` | 493 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/pwc.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/s2.jsonl` | 533 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/s2.jsonl` |  |
| `code/spine_data_review/tests/fixtures/screen_run/records/zenodo.jsonl` | 2,149 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/screen_run/records/zenodo.jsonl` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds01.json` | 5,548 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds01.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds02.json` | 5,516 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds02.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds03.json` | 5,494 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds03.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds04.json` | 5,542 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds04.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds05.json` | 5,599 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds05.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds06.json` | 5,510 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds06.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds07.json` | 5,721 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds07.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds08.json` | 5,600 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds08.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds09.json` | 5,339 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds09.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds10.json` | 5,407 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds10.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds11.json` | 5,492 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds11.json` |  |
| `code/spine_data_review/tests/fixtures/stats/charting/ds12.json` | 5,498 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/charting/ds12.json` |  |
| `code/spine_data_review/tests/fixtures/stats/dataset_sources.csv` | 452 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/dataset_sources.csv` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds01.json` | 2,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds01.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds02.json` | 2,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds02.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds03.json` | 1,340 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds03.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds04.json` | 2,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds04.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds05.json` | 2,434 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds05.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds06.json` | 1,340 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds06.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds07.json` | 2,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds07.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds08.json` | 2,434 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds08.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds09.json` | 2,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds09.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds10.json` | 2,434 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds10.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds11.json` | 2,440 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds11.json` |  |
| `code/spine_data_review/tests/fixtures/stats/probes/ds12.json` | 2,434 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/probes/ds12.json` |  |
| `code/spine_data_review/tests/fixtures/stats/screening/chase_manual.csv` | 47 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/screening/chase_manual.csv` |  |
| `code/spine_data_review/tests/fixtures/stats/screening/decisions.csv` | 1,448 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/screening/decisions.csv` |  |
| `code/spine_data_review/tests/fixtures/stats/screening/known_items.csv` | 101 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/screening/known_items.csv` |  |
| `code/spine_data_review/tests/fixtures/stats/screening/prescreen_audit.csv` | 99 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/fixtures/stats/screening/prescreen_audit.csv` |  |
| `code/spine_data_review/tests/leak_scan_availability.py` | 1,808 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/leak_scan_availability.py` |  |
| `code/spine_data_review/tests/live_common_probe.py` | 3,686 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/live_common_probe.py` |  |
| `code/spine_data_review/tests/make_chart_fixture.py` | 9,963 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/make_chart_fixture.py` |  |
| `code/spine_data_review/tests/make_fixture.py` | 21,931 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/make_fixture.py` |  |
| `code/spine_data_review/tests/make_recipe_fixture.py` | 8,188 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/make_recipe_fixture.py` |  |
| `code/spine_data_review/tests/make_screen_fixture.py` | 10,166 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/make_screen_fixture.py` |  |
| `code/spine_data_review/tests/probe_merge_edges.py` | 2,574 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/probe_merge_edges.py` |  |
| `code/spine_data_review/tests/probe_screen_round2.py` | 7,690 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/probe_screen_round2.py` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/2f8a1925aee9f2f3e38573887a9ed90a095f12c5.json` | 600 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/2f8a1925aee9f2f3e38573887a9ed90a095f12c5.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/347a99fb5451b7399b9ca40913d1332beb2d7348.json` | 618 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/347a99fb5451b7399b9ca40913d1332beb2d7348.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/3f71c4e7bf5d3d136ffbc9fa0a00f6c7e79aab05.json` | 495 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/3f71c4e7bf5d3d136ffbc9fa0a00f6c7e79aab05.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/4021b0fd6caf18fa8dc3bea52114bec460e664a3.json` | 436 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/4021b0fd6caf18fa8dc3bea52114bec460e664a3.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/4387b56a95f9e04457d149f0089f7e48d7af0445.json` | 516 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/4387b56a95f9e04457d149f0089f7e48d7af0445.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/6767e4c6a8aece3be7146ea1ec3118f78f981939.json` | 66,052 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/6767e4c6a8aece3be7146ea1ec3118f78f981939.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/7ef76088908254aaa239d8bc8b97bc7f4e4bbfee.json` | 428 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/7ef76088908254aaa239d8bc8b97bc7f4e4bbfee.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/abfaa9ad06f911a592b63c312daee991d82fc637.json` | 624 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/abfaa9ad06f911a592b63c312daee991d82fc637.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/af0288b38551bd98c92833229a9be21dd49a877a.json` | 554 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/af0288b38551bd98c92833229a9be21dd49a877a.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/baff5152241ad38af58fbe3e3480e7db3b63cbbb.json` | 622 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/baff5152241ad38af58fbe3e3480e7db3b63cbbb.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/bea8857592dece77a037481264ae7e749742d556.json` | 444 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/bea8857592dece77a037481264ae7e749742d556.json` |  |
| `code/spine_data_review/tests/run_fixture/raw/probe/ffdc658cf2d6944180cbb0158501f90b5c85839c.json` | 511 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/raw/probe/ffdc658cf2d6944180cbb0158501f90b5c85839c.json` |  |
| `code/spine_data_review/tests/run_fixture/requests.log.jsonl` | 5,414 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/requests.log.jsonl` |  |
| `code/spine_data_review/tests/run_fixture/run_meta.json` | 670 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_fixture/run_meta.json` |  |
| `code/spine_data_review/tests/run_screen_review.sh` | 3,804 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_screen_review.sh` |  |
| `code/spine_data_review/tests/run_stats_review.sh` | 2,111 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/run_stats_review.sh` |  |
| `code/spine_data_review/tests/scan_run_for_credentials.py` | 1,303 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/scan_run_for_credentials.py` |  |
| `code/spine_data_review/tests/show_smoke_strings.py` | 759 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/show_smoke_strings.py` |  |
| `code/spine_data_review/tests/summarise_smoke_repos.py` | 1,252 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/summarise_smoke_repos.py` |  |
| `code/spine_data_review/tests/test_availability_fixture.py` | 21,642 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_availability_fixture.py` |  |
| `code/spine_data_review/tests/test_common_review.py` | 25,352 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_common_review.py` |  |
| `code/spine_data_review/tests/test_ids.py` | 7,790 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_ids.py` |  |
| `code/spine_data_review/tests/test_manuscript_fixture.py` | 22,410 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_manuscript_fixture.py` |  |
| `code/spine_data_review/tests/test_queries_yaml.py` | 21,934 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_queries_yaml.py` |  |
| `code/spine_data_review/tests/test_recipe.py` | 15,547 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_recipe.py` |  |
| `code/spine_data_review/tests/test_replay_get_bytes.py` | 1,930 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_replay_get_bytes.py` |  |
| `code/spine_data_review/tests/test_search_literature_fixture.py` | 24,614 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_search_literature_fixture.py` |  |
| `code/spine_data_review/tests/test_search_repositories_fixture.py` | 6,294 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_search_repositories_fixture.py` |  |
| `code/spine_data_review/tests/test_stats_fixture.py` | 5,457 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_stats_fixture.py` |  |
| `code/spine_data_review/tests/test_stats_module.py` | 24,994 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/tests/test_stats_module.py` |  |

### `code/tools/` (67 files, 1,421,117 B)

Source and note: `placeholder for the empty folder`; `ssn:tools/ (header added)`; `ssn:tools/diagnostics/ (header added)`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `code/tools/audit_case_shifts.py` | 4,403 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/audit_case_shifts.py` | yes |
| `code/tools/audit_film_corpora.py` | 14,558 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/audit_film_corpora.py` | yes |
| `code/tools/audit_realxray_lists.py` | 12,802 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/audit_realxray_lists.py` | yes |
| `code/tools/build_audit_doc.py` | 7,226 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/build_audit_doc.py` | yes |
| `code/tools/checkpoint_lineage.py` | 121,208 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/checkpoint_lineage.py` | yes |
| `code/tools/corpus_level_report.py` | 8,702 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/corpus_level_report.py` | yes |
| `code/tools/ct_inventory.py` | 7,604 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ct_inventory.py` | yes |
| `code/tools/ctsp0533_bone_check.py` | 6,983 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ctsp0533_bone_check.py` | yes |
| `code/tools/ctsp0533_cast.py` | 2,253 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ctsp0533_cast.py` | yes |
| `code/tools/ctsp0533_dicom_to_nifti.py` | 4,962 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ctsp0533_dicom_to_nifti.py` | yes |
| `code/tools/ctsp0533_series_check.py` | 4,364 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ctsp0533_series_check.py` | yes |
| `code/tools/ctsp0533_verify.py` | 10,451 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ctsp0533_verify.py` | yes |
| `code/tools/data_alias.py` | 128,195 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/data_alias.py` | yes |
| `code/tools/data_ledger.py` | 75,954 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/data_ledger.py` | yes |
| `code/tools/data_lineage.py` | 83,139 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/data_lineage.py` | yes |
| `code/tools/data_manifest.py` | 8,562 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/data_manifest.py` | yes |
| `code/tools/diagnostics/ctsp_crosswalk_leak.py` | 4,273 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/diagnostics/ctsp_crosswalk_leak.py` | yes |
| `code/tools/diagnostics/make_fake_corpus.py` | 16,732 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/diagnostics/make_fake_corpus.py` | yes |
| `code/tools/excluded_sources.py` | 5,351 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/excluded_sources.py` | yes |
| `code/tools/export_vindr_identity.py` | 3,354 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/export_vindr_identity.py` | yes |
| `code/tools/film_corpus_inventory.py` | 23,602 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/film_corpus_inventory.py` | yes |
| `code/tools/holdout.py` | 5,723 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/holdout.py` | yes |
| `code/tools/identity/README.md` | 638 | `(written by the builder)` |  |
| `code/tools/inspect_dicom_tree.py` | 6,444 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/inspect_dicom_tree.py` | yes |
| `code/tools/jhu_dataverse_fetch.py` | 3,549 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/jhu_dataverse_fetch.py` | yes |
| `code/tools/jhu_dataverse_info.py` | 2,135 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/jhu_dataverse_info.py` | yes |
| `code/tools/leak_check.py` | 153,442 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/leak_check.py` | yes |
| `code/tools/leak_effect.py` | 6,004 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/leak_effect.py` | yes |
| `code/tools/level_integrity.py` | 14,396 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/level_integrity.py` | yes |
| `code/tools/level_inventory.py` | 5,845 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/level_inventory.py` | yes |
| `code/tools/model_registry.py` | 21,537 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/model_registry.py` | yes |
| `code/tools/or_audit_dupes.py` | 11,182 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/or_audit_dupes.py` | yes |
| `code/tools/or_audit_report.py` | 23,005 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/or_audit_report.py` | yes |
| `code/tools/or_audit_splits.py` | 21,598 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/or_audit_splits.py` | yes |
| `code/tools/patient_keys.py` | 30,882 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/patient_keys.py` | yes |
| `code/tools/pipeline_state.py` | 70,592 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/pipeline_state.py` | yes |
| `code/tools/repair_image_links.py` | 3,120 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/repair_image_links.py` | yes |
| `code/tools/restore_container_links.py` | 3,541 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/restore_container_links.py` | yes |
| `code/tools/source_quality_report.py` | 7,172 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/source_quality_report.py` | yes |
| `code/tools/spineps_id_census.py` | 46,411 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_id_census.py` | yes |
| `code/tools/spineps_ids.py` | 50,841 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids.py` | yes |
| `code/tools/spineps_ids_f5_checks.py` | 7,671 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_f5_checks.py` | yes |
| `code/tools/spineps_ids_impact.py` | 7,146 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_impact.py` | yes |
| `code/tools/spineps_ids_probe.py` | 8,325 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_probe.py` | yes |
| `code/tools/spineps_ids_rederive.py` | 11,178 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_rederive.py` | yes |
| `code/tools/spineps_ids_rederive_census.py` | 3,256 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_rederive_census.py` | yes |
| `code/tools/spineps_ids_render.py` | 4,149 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_render.py` | yes |
| `code/tools/spineps_ids_rescore_report.py` | 3,247 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_rescore_report.py` | yes |
| `code/tools/spineps_ids_verify.py` | 7,617 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_ids_verify.py` | yes |
| `code/tools/spineps_label_census.py` | 4,053 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_label_census.py` | yes |
| `code/tools/spineps_relabel_from_poi.py` | 5,640 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_relabel_from_poi.py` | yes |
| `code/tools/spineps_veridah_check.py` | 7,651 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spineps_veridah_check.py` | yes |
| `code/tools/stats_compare.py` | 66,558 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/stats_compare.py` | yes |
| `code/tools/test_checkpoint_lineage.py` | 34,904 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_checkpoint_lineage.py` | yes |
| `code/tools/test_dataset_803_pipeline.py` | 47,616 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_dataset_803_pipeline.py` | yes |
| `code/tools/test_decoder_oracle.py` | 5,721 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_decoder_oracle.py` | yes |
| `code/tools/test_device_gate.py` | 5,891 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_device_gate.py` | yes |
| `code/tools/test_leak_check.py` | 19,250 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_leak_check.py` | yes |
| `code/tools/test_masked_link.py` | 4,234 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_masked_link.py` | yes |
| `code/tools/test_patient_keys.py` | 8,968 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_patient_keys.py` | yes |
| `code/tools/test_realxray_banks.py` | 10,518 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_realxray_banks.py` | yes |
| `code/tools/test_spineps_ids.py` | 7,775 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_spineps_ids.py` | yes |
| `code/tools/test_spinesac_bind_smoke.py` | 7,250 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_spinesac_bind_smoke.py` | yes |
| `code/tools/test_stats_compare.py` | 36,793 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_stats_compare.py` | yes |
| `code/tools/test_ts_transitional_registry.py` | 4,371 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/test_ts_transitional_registry.py` | yes |
| `code/tools/ts12_verify_ids.py` | 38,295 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/ts12_verify_ids.py` | yes |
| `code/tools/xray_dataset_usage.py` | 10,305 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/xray_dataset_usage.py` | yes |

### `docs/CT_INVENTORY.md/` (1 files, 2,930 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/CT_INVENTORY.md` | 2,930 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/CT_INVENTORY.md` |  |

### `docs/DATA_ACCOUNTING.md/` (1 files, 45,896 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/DATA_ACCOUNTING.md` | 45,896 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/DATA_ACCOUNTING.md` |  |

### `docs/DATA_COMPLETENESS_AUDIT.md/` (1 files, 361,191 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/DATA_COMPLETENESS_AUDIT.md` | 361,191 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/DATA_COMPLETENESS_AUDIT.md` |  |

### `docs/MANIFEST_DATA_MODELS_RESULTS.md/` (1 files, 102,042 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/MANIFEST_DATA_MODELS_RESULTS.md` | 102,042 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/MANIFEST_DATA_MODELS_RESULTS.md` |  |

### `docs/MODEL_REGISTRY.md/` (1 files, 5,944 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/MODEL_REGISTRY.md` | 5,944 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/MODEL_REGISTRY.md` |  |

### `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md/` (1 files, 2,876 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` | 2,876 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` |  |

### `docs/PATIENT_IDENTITY_SPEC.md/` (1 files, 54,340 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/PATIENT_IDENTITY_SPEC.md` | 54,340 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/PATIENT_IDENTITY_SPEC.md` |  |

### `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md/` (1 files, 3,760 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` | 3,760 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` |  |

### `docs/XRAY_DATASET_USAGE.md/` (1 files, 4,065 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/XRAY_DATASET_USAGE.md` | 4,065 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/XRAY_DATASET_USAGE.md` |  |

### `docs/bank_profile_v3.json/` (1 files, 6,931 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/bank_profile_v3.json` | 6,931 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/bank_profile_v3.json` |  |

### `docs/grid_read_2026-10-08/` (11 files, 867,127 B)

Source and note: `laptop copy of the grid census (jobs 40578909, 40580051, 40580052)`; `the read-only grid pass of 2026-10-08 22:20 UTC (scratchpad seed)`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/grid_read_2026-10-08/census/_du_data.txt` | 2,966 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/census/_du_data.txt` |  |
| `docs/grid_read_2026-10-08/census/_du_home.txt` | 7,873 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/census/_du_home.txt` |  |
| `docs/grid_read_2026-10-08/census/census.json` | 47,128 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/census/census.json` |  |
| `docs/grid_read_2026-10-08/census/census_merged_partial.tsv` | 186,083 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/census/census_merged_partial.tsv` |  |
| `docs/grid_read_2026-10-08/census/ceph/census.tsv` | 138,342 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/census/ceph/census.tsv` |  |
| `docs/grid_read_2026-10-08/census/home_after_F/census.tsv` | 47,150 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/census/home_after_F/census.tsv` |  |
| `docs/grid_read_2026-10-08/census/toplevel_listing.txt` | 51,915 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/census/toplevel_listing.txt` |  |
| `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` | 220,880 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/seed/grid_ls_2026-10-08.out` |  |
| `docs/grid_read_2026-10-08/grid_ls_condensed.txt` | 155,321 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/seed/grid_ls_condensed.txt` |  |
| `docs/grid_read_2026-10-08/grid_ls_markers.txt` | 1,966 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/seed/grid_ls_markers.txt` |  |
| `docs/grid_read_2026-10-08/grid_remote_ls.sh` | 7,503 | `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/seed/grid_remote_ls.sh` |  |

### `docs/grid_records/` (2 files, 120,747 B)

Source and note: `ssn:docs/grid_records/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | 104,820 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` |  |
| `docs/grid_records/JOBS_RECORD_2026-09-27_1544.tsv` | 15,927 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/grid_records/JOBS_RECORD_2026-09-27_1544.tsv` |  |

### `docs/handoff/` (18 files, 495,848 B)

Source and note: `HANDOFF student-readable file, whole (PLAN rule 3)`; `HANDOFF student-readable file, whole; one username redacted at line 97`; `HANDOFF/literature_state (DISPOSITION rows for data_platform)`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/handoff/DATASET_USAGE.md` | 37,254 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/DATASET_USAGE.md` |  |
| `docs/handoff/GLOSSARY.md` | 25,368 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GLOSSARY.md` |  |
| `docs/handoff/INFRASTRUCTURE.md` | 48,578 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/INFRASTRUCTURE.md` | yes |
| `docs/handoff/LEAKAGE.md` | 25,299 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LEAKAGE.md` |  |
| `docs/handoff/OPEN_QUESTIONS.md` | 28,532 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/OPEN_QUESTIONS.md` |  |
| `docs/handoff/README.md` | 42,567 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/README.md` |  |
| `docs/handoff/RECIPES.md` | 73,585 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RECIPES.md` |  |
| `docs/handoff/RESULTS_CATALOG.md` | 110,438 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESULTS_CATALOG.md` |  |
| `docs/handoff/literature_state/assemble.py` | 2,233 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/assemble.py` |  |
| `docs/handoff/literature_state/biblio_sorted.py` | 2,213 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/biblio_sorted.py` |  |
| `docs/handoff/literature_state/calc_addendum.json` | 308 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_addendum.json` |  |
| `docs/handoff/literature_state/calc_addendum.py` | 1,589 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_addendum.py` |  |
| `docs/handoff/literature_state/calc_review.json` | 1,381 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_review.json` |  |
| `docs/handoff/literature_state/calc_review.py` | 3,098 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_review.py` |  |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | 61,579 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/dataset_landscape_by_task.md` |  |
| `docs/handoff/literature_state/join_ranking.py` | 4,319 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/join_ranking.py` |  |
| `docs/handoff/literature_state/ranking_joined.csv` | 23,589 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/ranking_joined.csv` |  |
| `docs/handoff/literature_state/t3_ratios.py` | 3,918 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/t3_ratios.py` |  |

### `docs/pipeline.md/` (1 files, 10,032 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/pipeline.md` | 10,032 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/pipeline.md` |  |

### `docs/troubleshooting.md/` (1 files, 3,540 B)

Source and note: `ssn:docs/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `docs/troubleshooting.md` | 3,540 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/docs/troubleshooting.md` |  |

### `memory/` (51 files, 145,057 B)

Source and note: `HANDOFF/context redacted copy; status header inserted after the frontmatter`; `HANDOFF/context/COPIED_AT.txt: copy times of the redacted notes`; `HANDOFF/context/INDEX.md: the full handoff index of 141 notes with statuses; only the notes listed in MEMORY.md are present in this folder`; `live memory note (newer than the HANDOFF copy; checked for the banned word and personal data); status header inserted after the frontmatter`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `memory/CONTEXT_INDEX_2026-10-08.md` | 25,948 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/INDEX.md` |  |
| `memory/COPIED_AT_2026-10-08.txt` | 7,282 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/COPIED_AT.txt` |  |
| `memory/bash-heredoc-backslashes.md` | 1,277 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/bash-heredoc-backslashes.md` | yes |
| `memory/cloudflare-tls-fingerprint.md` | 1,847 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/cloudflare-tls-fingerprint.md` | yes |
| `memory/commit-directly-to-master.md` | 1,097 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/commit-directly-to-master.md` | yes |
| `memory/ct-benchmark-covers-all-collections.md` | 2,295 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-benchmark-covers-all-collections.md` | yes |
| `memory/ct-volumes-are-pir-not-ras.md` | 2,269 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-volumes-are-pir-not-ras.md` | yes |
| `memory/data-audit-99-gaps.md` | 3,355 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-audit-99-gaps.md` | yes |
| `memory/data-directives-2026-09-23.md` | 2,401 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-directives-2026-09-23.md` | yes |
| `memory/data-platform-migration-2026-10.md` | 8,663 | `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/data-platform-migration-2026-10.md` | yes |
| `memory/dataset813-image-links-are-container-paths.md` | 1,698 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/dataset813-image-links-are-container-paths.md` | yes |
| `memory/figure-captions-terse.md` | 1,545 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/figure-captions-terse.md` | yes |
| `memory/flagship-program.md` | 2,829 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/flagship-program.md` | yes |
| `memory/fluorocap-is-reproductions-not-fluoroscopy.md` | 2,535 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-is-reproductions-not-fluoroscopy.md` | yes |
| `memory/fluorocap-repo-private.md` | 1,690 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-repo-private.md` | yes |
| `memory/grid-access-list-gate.md` | 2,417 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access-list-gate.md` | yes |
| `memory/grid-access.md` | 1,773 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access.md` | yes |
| `memory/grid-apptainer-module-works.md` | 1,922 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-apptainer-module-works.md` | yes |
| `memory/grid-bash-4-2-quoting.md` | 1,665 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-bash-4-2-quoting.md` | yes |
| `memory/grid-ceph-volume-oschome.md` | 1,551 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ceph-volume-oschome.md` | yes |
| `memory/grid-ct-0533-truncated.md` | 3,380 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ct-0533-truncated.md` | yes |
| `memory/grid-local-singularity-is-broken.md` | 2,636 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-local-singularity-is-broken.md` | yes |
| `memory/grid-quota-and-deleted-banks.md` | 2,523 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-quota-and-deleted-banks.md` | yes |
| `memory/grid-slurm-inside-apptainer.md` | 1,813 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-slurm-inside-apptainer.md` | yes |
| `memory/grid-ssh-second-factor.md` | 2,170 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ssh-second-factor.md` | yes |
| `memory/identity-audit-findings.md` | 4,428 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/identity-audit-findings.md` | yes |
| `memory/key-patients-from-metadata-not-filenames.md` | 2,427 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/key-patients-from-metadata-not-filenames.md` | yes |
| `memory/label-scheme-v4-vs-ostk.md` | 2,691 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/label-scheme-v4-vs-ostk.md` | yes |
| `memory/model-registry.md` | 2,078 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/model-registry.md` | yes |
| `memory/morphology-deformation-feasibility.md` | 2,535 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/morphology-deformation-feasibility.md` | yes |
| `memory/never-reorient-when-writing-labels.md` | 2,160 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/never-reorient-when-writing-labels.md` | yes |
| `memory/nhanes-double-inclusion.md` | 1,779 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/nhanes-double-inclusion.md` | yes |
| `memory/no-jobs-on-login-node.md` | 2,416 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-jobs-on-login-node.md` | yes |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | 2,365 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` | yes |
| `memory/push-both-github-remotes.md` | 1,254 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/push-both-github-remotes.md` | yes |
| `memory/scratchpad-shadows-stdlib.md` | 1,632 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/scratchpad-shadows-stdlib.md` | yes |
| `memory/spine-data-review-and-ts-bench.md` | 3,985 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/spine-data-review-and-ts-bench.md` | yes |
| `memory/spineps-ids-can-be-scrambled.md` | 2,530 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/spineps-ids-can-be-scrambled.md` | yes |
| `memory/split-leak-cross-naming.md` | 2,162 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/split-leak-cross-naming.md` | yes |
| `memory/splits-origin-and-v3-resplit.md` | 2,409 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/splits-origin-and-v3-resplit.md` | yes |
| `memory/submit-and-sleep-orchestration.md` | 2,156 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/submit-and-sleep-orchestration.md` | yes |
| `memory/ts-bench-inside-v9-bank.md` | 1,987 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ts-bench-inside-v9-bank.md` | yes |
| `memory/ts-sacrum-excludes-s1.md` | 1,798 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ts-sacrum-excludes-s1.md` | yes |
| `memory/user-affiliation-general-surgery.md` | 1,784 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/user-affiliation-general-surgery.md` | yes |
| `memory/versefusion-t13-flag-wrong.md` | 2,150 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/versefusion-t13-flag-wrong.md` | yes |
| `memory/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` | 1,751 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` | yes |
| `memory/windows-junction-worktree-trap.md` | 1,758 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-junction-worktree-trap.md` | yes |
| `memory/windows-ssh-to-grid.md` | 1,732 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-ssh-to-grid.md` | yes |
| `memory/writing-preferences.md` | 1,056 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/writing-preferences.md` | yes |
| `memory/wsl-for-network.md` | 1,707 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsl-for-network.md` | yes |
| `memory/wsu-library-access-cutoff.md` | 1,746 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsu-library-access-cutoff.md` | yes |

### `results/spineps_ids/` (63 files, 30,942,420 B)

Source and note: `sn:results/spineps_ids/`.

| copied to | bytes | copied from (laptop path, history only) | differs from source |
|---|---|---|---|
| `results/spineps_ids/CENSUS.md` | 40,877 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/CENSUS.md` |  |
| `results/spineps_ids/CENSUS_reading.md` | 13,286 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/CENSUS_reading.md` |  |
| `results/spineps_ids/CONSUMERS.md` | 23,837 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/CONSUMERS.md` |  |
| `results/spineps_ids/IMPACT.md` | 21,954 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/IMPACT.md` |  |
| `results/spineps_ids/REPAIRS.md` | 23,189 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/REPAIRS.md` |  |
| `results/spineps_ids/TS12_VERIFY.md` | 11,964 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/TS12_VERIFY.md` |  |
| `results/spineps_ids/VERIFY.md` | 16,923 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/VERIFY.md` |  |
| `results/spineps_ids/census.json` | 6,202,356 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/census.json` |  |
| `results/spineps_ids/census_rows.jsonl.gz` | 3,871,793 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/census_rows.jsonl.gz` |  |
| `results/spineps_ids/components_id25.json` | 14,987 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/components_id25.json` |  |
| `results/spineps_ids/components_id26.json` | 13,548 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/components_id26.json` |  |
| `results/spineps_ids/files.tsv` | 1,394,814 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/files.tsv` |  |
| `results/spineps_ids/g3_split/split_leak_report.json` | 99,961 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/g3_split/split_leak_report.json` |  |
| `results/spineps_ids/impact_counts.json` | 25,165 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/impact_counts.json` |  |
| `results/spineps_ids/rederived.json` | 11,052 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/rederived.json` |  |
| `results/spineps_ids/repair/bodies_cobra_ctd_log.jsonl` | 309,419 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/bodies_cobra_ctd_log.jsonl` |  |
| `results/spineps_ids/repair/bodies_ctd_log.jsonl` | 7,800,053 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/bodies_ctd_log.jsonl` |  |
| `results/spineps_ids/repair/census_ctd.json` | 4,609,586 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/census_ctd.json` |  |
| `results/spineps_ids/repair/census_ctd_by_tree.json` | 1,454 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/census_ctd_by_tree.json` |  |
| `results/spineps_ids/repair/census_ctd_rows.jsonl.gz` | 2,501,244 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/census_ctd_rows.jsonl.gz` |  |
| `results/spineps_ids/repair/reguard_moved.json` | 127,547 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/reguard_moved.json` |  |
| `results/spineps_ids/repair/relabel_records.jsonl.gz` | 332,725 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/relabel_records.jsonl.gz` |  |
| `results/spineps_ids/repair/relabel_summary_bench.json` | 2,094 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/relabel_summary_bench.json` |  |
| `results/spineps_ids/repair/relabel_summary_bench_ts.json` | 6,087 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/relabel_summary_bench_ts.json` |  |
| `results/spineps_ids/repair/relabel_summary_cobra_v1.json` | 1,212 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/relabel_summary_cobra_v1.json` |  |
| `results/spineps_ids/repair/relabel_summary_deepfluoro.json` | 538 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/relabel_summary_deepfluoro.json` |  |
| `results/spineps_ids/repair/relabel_summary_geneva.json` | 536 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/relabel_summary_geneva.json` |  |
| `results/spineps_ids/repair/relabel_summary_tsv3.json` | 9,533 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/relabel_summary_tsv3.json` |  |
| `results/spineps_ids/repair/render/A053.png` | 170,695 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/render/A053.png` |  |
| `results/spineps_ids/repair/render/COLONOG_1.png` | 307,881 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/render/COLONOG_1.png` |  |
| `results/spineps_ids/repair/render/COLONOG_10.png` | 368,773 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/render/COLONOG_10.png` |  |
| `results/spineps_ids/repair/render/COLONOG_117.png` | 375,262 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/render/COLONOG_117.png` |  |
| `results/spineps_ids/repair/render/TS_s1089.png` | 301,760 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/render/TS_s1089.png` |  |
| `results/spineps_ids/repair/render/VERSE_verse607.png` | 340,589 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/render/VERSE_verse607.png` |  |
| `results/spineps_ids/repair/rescore/bench_ctd/per_case.csv` | 133,359 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/rescore/bench_ctd/per_case.csv` |  |
| `results/spineps_ids/repair/rescore/bench_ctd/report.txt` | 2,126 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/rescore/bench_ctd/report.txt` |  |
| `results/spineps_ids/repair/rescore/bench_ctd/summary.json` | 33,640 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/rescore/bench_ctd/summary.json` |  |
| `results/spineps_ids/repair/rescore/ctsp_postfix/per_case.csv` | 134,216 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/rescore/ctsp_postfix/per_case.csv` |  |
| `results/spineps_ids/repair/rescore/ctsp_postfix/report.txt` | 2,125 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/rescore/ctsp_postfix/report.txt` |  |
| `results/spineps_ids/repair/rescore/ctsp_postfix/summary.json` | 33,840 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/rescore/ctsp_postfix/summary.json` |  |
| `results/spineps_ids/repair/rescore_report.json` | 3,581 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/rescore_report.json` |  |
| `results/spineps_ids/repair/verify.json` | 9,142 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/verify.json` |  |
| `results/spineps_ids/repair/verify_rows.jsonl` | 460,094 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/verify_rows.jsonl` |  |
| `results/spineps_ids/repair/verify_ts12_cobra.jsonl` | 74,221 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/repair/verify_ts12_cobra.jsonl` |  |
| `results/spineps_ids/ts12/TS_s0224_verify.json` | 35,530 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s0224_verify.json` |  |
| `results/spineps_ids/ts12/TS_s0616_verify.json` | 39,065 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s0616_verify.json` |  |
| `results/spineps_ids/ts12/TS_s0790_verify.json` | 38,212 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s0790_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1088_verify.json` | 36,764 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1088_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1089_verify.json` | 36,654 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1089_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1123_verify.json` | 37,205 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1123_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1124_verify.json` | 33,891 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1124_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1171_verify.json` | 37,189 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1171_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1178_verify.json` | 33,315 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1178_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1304_verify.json` | 36,010 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1304_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1350_verify.json` | 37,769 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1350_verify.json` |  |
| `results/spineps_ids/ts12/TS_s1380_verify.json` | 34,453 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/ts12/TS_s1380_verify.json` |  |
| `results/spineps_ids/veridah_check.json` | 12,256 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/veridah_check.json` |  |
| `results/spineps_ids/verify/carmlspine_levels_copy.json` | 147,883 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/verify/carmlspine_levels_copy.json` |  |
| `results/spineps_ids/verify/f5_checks.json` | 77,471 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/verify/f5_checks.json` |  |
| `results/spineps_ids/verify/g3_split_verify.json` | 3,621 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/verify/g3_split_verify.json` |  |
| `results/spineps_ids/verify/probe.json` | 21,082 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/verify/probe.json` |  |
| `results/spineps_ids/verify/probe_40427906.log` | 2,210 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/verify/probe_40427906.log` |  |
| `results/spineps_ids/verify/rederive_census.json` | 2,802 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/results/spineps_ids/verify/rederive_census.json` |  |

## 3. Valuable material NOT copied, and why

| item | where it stays | size | reason |
|---|---|---|---|
| `SchwingNet/results/spineps_ids/ts12/*.png` (60 renders) | spinesurg-ct-nnunet 097933a | 28,395,271 B | a render image set (`large png sets` rule); the twelve `*_verify.json` beside them are copied |
| `docs/CREDENTIALS_SETUP.md` | spinesurg-ct-nnunet 097933a | 9,426 B | credential locations (DISPOSITION row decision) |
| `spine_data_review/runs/` | the laptop repository folder (gitignored) | 7,567 files, 1,857,122,129 B | run records and raw caches; nine `records/hf.jsonl` over 25 MB; reference by path: `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/spine_data_review/runs/` |
| `spine_data_review/tests/merge_reobservation.py`, `tests/test_reobserve.py`, `runs/2026-09-23/` | laptop working tree | not recorded | untracked on 2026-10-08; the row copies the tracked part only |
| `data_platform/{db,lib,reacquire}/__pycache__/*.pyc` | laptop | 94,639 + 15,046 + 62,294 B | compiled caches |
| `C:/Users/grego/OneDrive/Desktop/new_repo.zip` (and the unzipped `Desktop/new_repo/`) | laptop | 84,504 B | the 2026-04-18 scaffold of spinesurg-ct-nnunet (README, Makefile, download_dataset.py, spinesurg-ct.def, docs_pipeline/ablations/troubleshooting, CITATION.cff); superseded by the private repository at L6_Class 097933a (DISPOSITION exclude row) |
| `HANDOFF/MANUSCRIPTS.md`, `CONTEXT_EXPORT.md`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md` | spinesurg-ct-nnunet 097933a | 67,604; 34,696; 133,695; 170,864 B | Greg-only handoff files; copied whole only into the Greg-only folders (`../_plan/PLAN.md` rule 3); the sections that bear on this project are in `docs/handoff/extracts/` |
| `HANDOFF/literature_state/{power.md, power_calc.json, power_calc.py, topic1_bibliography.md, topic3_size_relative_to_studies.md}` | spinesurg-ct-nnunet 097933a | 36,598; 14,819; 8,151; 92,083; 41,506 B | belong to `02_transitional_naming_truth` (power) and the Greg-only folders |
| `HANDOFF/working_notes/topic1-6*.md`, `t2_wilson_check.py` | spinesurg-ct-nnunet 097933a | 59-97 KB each | Greg-only working notes (`../_plan/PLAN.md` section 2 rule 3: whole copies go to 01, 02, 07, 08, 09 only); topic 3 (dataset usage, leakage, RSNA) and topic 5 (operating here) are condensed in `docs/handoff/DATASET_USAGE.md`, `LEAKAGE.md` and `INFRASTRUCTURE.md`, which are copied whole. The three `../_plan/DISPOSITION.tsv` rows for topics 3, 4 and 5 said `copy` in their action column while their own decision text said "a section pointer"; on 2026-10-08 (verification fix) their action was set to `reference` (`MANIFEST_CODE.md` "HANDOFF at 097933a") so the plan matches the folder. Topic 5 also carries a student username, which the copy rules bar |
| `HANDOFF/GREG_ONLY/` (PRIVATE_STATE.md, README.md, context/, context_beethoven/) | laptop, untracked | not recorded | credential locations, commercial stance, withheld contacts, the original memory index, the Beethoven notes; never copied; Greg decides A29/A30 |
| the live memory notes not listed in `MEMORY.md` | the laptop memory folder | | owned by other folders, or Greg-only, or another study, or history-only (`MEMORY.md` last section) |
| `tools/eval_gate.py`, `tools/make_split.py` and the rest of `tools/` | spinesurg-ct-nnunet 097933a | | level-identification code (`01_carm_level_detection`) or not this project's; referenced in `MANIFEST_CODE.md` |
| `slurm/*.sh` (the 40-odd data-accounting, inventory, repair and setup jobs) | spinesurg-ct-nnunet 097933a | 3.4 MB for the whole folder | reference rows (`MANIFEST_CODE.md` section 2 `slurm/`); the repository is the executable source |
| `tests/` (61 files) | spinesurg-ct-nnunet 097933a | | reference row (`MANIFEST_CODE.md`) |
| `SchwingNet/results/eval_gate/touched.json` | spinesurg-ct-nnunet 097933a; grid `/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/touched.json` | 55.3 MB | over 25 MB; `01` references it by path |
| the grid census outputs `slurm_data_census2_40580051.out`, `slurm_data_census2_40580052.out`, `census_job2.sh` | `/rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/` | 1,465 B; 50,676 B (growing); small | never on the laptop; `MANIFEST_GRID.md` section 3 |

## 4. Redactions and edits, file by file

| file | what changed |
|---|---|
| `code/data_platform/DATA_MANIFEST.md` line 18637, `sources.json` line 32485, `sources.yaml` line 24824 | the Balgrist corresponding author's address replaced by `<corresponding author of Jecklin 2024, address withheld>` |
| `code/data_platform/DATA_MANIFEST.md` line 18747, `LAYOUT.md` line 100 | an administrator's username replaced by `<C&IT admin account, username withheld>` |
| `code/spine_data_review/tests/check_template_prose.py` | the banned word, which the tool counts, is now built from two halves (`WORD = ...`) so the file does not spell it |
| `docs/handoff/INFRASTRUCTURE.md` line 97 | the same administrator's username withheld |
| `docs/handoff/RECIPES.md` line 402 | a student's HF handle replaced by `(HF handle withheld)` (verification fix, 2026-10-08) |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` line 183 | the Huashan corresponding author's address withheld |
| `docs/handoff/extracts/*.md` | section extracts; the same two addresses withheld where they occur |
| `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` lines 734 and 3199 | two file owners other than Greg's account withheld |
| `memory/grid-access-list-gate.md` | the administrator's and one student's usernames withheld (the handoff copier had not redacted this note) |
| `memory/grid-ceph-volume-oschome.md` line 13 | the administrator's username withheld |
| `memory/wsu-library-access-cutoff.md` line 26 | a library staff address and telephone number withheld |
| `memory/*.md` (all) | a status line inserted after the frontmatter (`MEMORY.md`) |
| `memory/data-platform-migration-2026-10.md` | the live note of 2026-10-08 20:43 UTC was copied instead of the handoff copy of 16:39 (the live one is newer by one paragraph that records the handoff commit; checked for the banned word and personal data: none) |
| `code/tools/*.py`, `code/tools/diagnostics/*.py`, `code/handoff_builders/*.py` | a first-line comment inserted (source path, commit, state) |
| `code/tools/identity/README.md`, `code/*/SOURCE.md`, `docs/MODEL_REGISTRY_CORRECTION.md` | written here, not copies |

## 5. Where the laptop sources were (history only)

- `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet` (private repository, branch `L6_Class`, commit 097933a): `data_platform/`, `tools/`, `env/`, `spine_data_review/`, `docs/`, `SchwingNet/results/spineps_ids/`, `HANDOFF/`.
- `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/` (the live memory notes; only `data-platform-migration-2026-10.md` was taken from here; the rest from `HANDOFF/context/`).
- The session scratchpad `C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/` (`seed/grid_ls_2026-10-08.out` and companions; `census/`): the read-only grid pass and the laptop census copies, now under `docs/grid_read_2026-10-08/`.


## 6. Laptop paths rewritten and addresses withheld after the copy (second pass, 2026-10-08)

Rule (c) of the build confines laptop paths to this file. In every other text file of this folder the laptop prefixes were rewritten to pointers: `<repo spinesurg-ct-nnunet 097933a>`, `<repo CTSpinoPelvic1K 7ddfe38>`, `<repo OpenSpineToolkit cb43197>`, `<repo XRSpinoPelvic1K 4f22935>`, `<memory notes; see MEMORY.md>`, `<session scratchpad; not a dependency>`, `<laptop folder Desktop/<name>; not a dependency>`. A script constant rewritten this way no longer runs as copied; the repository is the executable source. The files changed, with the number of pointers introduced:

- `code/data_platform/DATA_MANIFEST.md` (31)
- `code/data_platform/dedup/DEDUP_PLAN.md` (1)
- `code/data_platform/dedup/build_dedup_plan.py` (5)
- `code/data_platform/dedup/dedup_groups.json` (1)
- `code/data_platform/sources.json` (3)
- `code/data_platform/sources.yaml` (3)
- `code/data_platform/verify_planning.py` (2)
- `code/handoff_builders/build_context_export.py` (4)
- `code/handoff_builders/check_paths.py` (6)
- `code/handoff_builders/copy_context.py` (3)
- `code/handoff_builders/patch_helper.py` (1)
- `code/handoff_builders/refresh_context.py` (1)
- `code/spine_data_review/charting/validation_report.json` (3)
- `code/spine_data_review/tests/fixture_lit_run/run_meta.json` (2)
- `code/tools/build_audit_doc.py` (2)
- `code/tools/diagnostics/ctsp_crosswalk_leak.py` (1)
- `code/tools/test_patient_keys.py` (1)
- `docs/DATA_COMPLETENESS_AUDIT.md` (4)
- `docs/MANIFEST_DATA_MODELS_RESULTS.md` (3)
- `docs/handoff/INFRASTRUCTURE.md` (3)
- `docs/handoff/README.md` (8)
- `docs/handoff/RECIPES.md` (2)
- `docs/handoff/RESULTS_CATALOG.md` (4)
- `docs/handoff/extracts/CONTEXT_EXPORT_sections_1_2_5.md` (1)
- `docs/handoff/extracts/LITERATURE_STATE_sections.md` (3)
- `docs/handoff/extracts/RESEARCH_DIRECTIONS_sections.md` (7)
- `docs/handoff/literature_state/assemble.py` (1)
- `docs/handoff/literature_state/dataset_landscape_by_task.md` (3)
- `docs/handoff/literature_state/join_ranking.py` (1)
- `memory/COPIED_AT_2026-10-08.txt` (1)
- `memory/windows-junction-worktree-trap.md` (2)
- `memory/windows-ssh-to-grid.md` (1)
- `memory/wsl-for-network.md` (1)

Corresponding-author and other researcher e-mail addresses (from the dataset landscape and the literature-state extract) were replaced by `<address withheld>`; the institutional mailboxes `hpc@wayne.edu` and `IRBQuestions@wayne.edu`, the grid login and one test fixture address are kept. Files and counts:

- `docs/handoff/extracts/LITERATURE_STATE_sections.md` (21 addresses)

## 7. Third pass (verification fixes, 2026-10-08)

The verifier of this folder raised ten findings; what changed, file by file (the numbers are checked against the file named):

- `STATUS.md` D.1, `README.md` (deletion candidates), `TODO.md` step 4: the duplicate-census totals now read as `code/data_platform/dedup/DEDUP_PLAN.md` "The totals" prints them (at most 95.8 GB linkable; 353.7 GB now + 218.3 GB conditional; 1,631 concrete alias rows; `index_aliases.csv` `status` column counted: 1,631 concrete, 12 rule, 35 pending_table = 1,678 rows). The 97.7 / 482.9 / 1,659 of `memory/data-platform-migration-2026-10.md` lines 70-71 were the first plan's figures (482.9 = 353.7 + the 129.2 GB scaling banks, now conditional); `STATUS.md` section 9 and `MEMORY.md` say so.
- `STATUS.md` M.5, `README.md`, `MANIFEST_GRID.md` (B02 row and section 8): B02 has 25 ABSENT rows (002-024, 026, 030 in `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` "STATUS files"), not 24.
- `STATUS.md` R.1, `MANIFEST_GRID.md` section 4 and section 9, `docs/MODEL_REGISTRY_CORRECTION.md`: the ledger carries 17 `orientation_net_v2` lines (15:39:56 to 20:57:21 on 2026-09-15, the first registration plus 16 repeats), counted in `grid_ls_2026-10-08.out` "registry.jsonl"; the 106-line total stands.
- `STATUS.md` L.8: the "39 of 85 L6 masks lack id 25" sits in `docs/handoff/extracts/RESEARCH_DIRECTIONS_sections.md` section 5.2 line 46 (and in the source `HANDOFF/RESEARCH_DIRECTIONS.md`), which the row already cited; the row now names the line and says that no file behind that row prints the 39 (RECORD ONLY).
- `MANIFEST_CODE.md`, `STATUS.md` I.6: `sdr/` holds 21 modules (the 22nd entry in the repository is `__pycache__`, not copied).
- `code/handoff_builders/copy_context.py` line 17, `code/tools/build_audit_doc.py` line 12: the laptop project slug and session id replaced by `<laptop Claude project folder; not a dependency>`. `code/data_platform/VERIFICATION.md` lines 138-139, 159, 294, `DATA_MANIFEST.md` line 3630, `MIGRATION_PLAN.md` line 231, `sources.json` line 5 and `sources.yaml` line 7 now say that the scratch-folder scripts they name (parse_cards.py, curated_a.py, curated_cd.py, build_sources.py, make_manifest.py, spot_check.py, patch_facts.py, patch_reacquire.py, patch_recipes_md.py, probe_migration.sh, probe_index.py, make_family_b.py, inspect_unknown.sh and its output) were not preserved: not recorded. Every other `scratchpad` mention in this folder (`DEDUP_PLAN.md`, `build_dedup_plan.py`, `docs/DATA_COMPLETENESS_AUDIT.md`, the handoff files and extracts) names a script or output in the same session scratch folder, likewise not preserved unless it is listed in section 2; the grid folder `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/scratchpad` and the note `scratchpad-shadows-stdlib` are not scratch references.
- `docs/handoff/working_notes/`: not created; the three `DISPOSITION.tsv` rows were set to `reference` (section 3 above).
- `docs/handoff/RECIPES.md` line 402: a student's HF handle withheld (section 4 above).
- `CLAUDE.md` ("Where things are" and the fetch trap): the grid checkout commit 4e3fe93 is cited to `grid_ls_2026-10-08.out` "grid checkout HEAD"; `STATUS.md` L.5 cites `RESULTS_CATALOG.md` A16.4 and `extracts/LITERATURE_STATE_sections.md` line 67 for the 92 of 97; `STATUS.md` A19.6 and S.1 mark 3,490 [DERIVED] from the six `results/spineps_ids/repair/relabel_summary_*.json` (796 + 1,452 + 144 + 6 + 1 + 1,091).
- `CLAUDE.md`, `MANIFEST_GRID.md`, `MANIFEST_CODE.md`, `STATUS.md`, `TODO.md`, `MEMORY.md`: every back-ticked `~/`, `$RS/` and `.../` grid path spelled in full (`/wsu/home/go/go24/go2432/...`, `/rs/rs_grp_oschome/go2432/...`); a GRIDLS section name quoted as it stands in that file (for example "ls ~/data") keeps its `~`.


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Ownership of files that were duplicated in 01

`docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` and `.tsv` are owned here (PLAN.md section 3, 10); 01 held byte-identical copies and removed them in the final pass.

### Removed: Greg-only HANDOFF material (literature_state/)

PLAN.md section 2 rule 3 confines the Greg-only HANDOFF files and working notes to folders 01, 02, 07, 08 and 09; student-safe folders get extracts in `STATUS.md` and `TODO.md`, not the notes. The critic found the files below here whole. Removed in the final pass; the extracts stay; the whole files live in the owning Greg-only folder named in the last column and in spinesurg-ct-nnunet at 097933a (`HANDOFF/`).

| removed | bytes | sha1 | where it lives |
|---|---:|---|---|
| `docs/handoff/literature_state/assemble.py` | 2,216 | ba6a8082fd727193 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/biblio_sorted.py` | 2,213 | 958374f9f251b337 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/calc_addendum.json` | 308 | 24baf0bf9626c0e8 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/calc_addendum.py` | 1,589 | 78c3733fa0c34488 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/calc_review.json` | 1,381 | 286fcd9806fafd92 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/calc_review.py` | 3,098 | 99672f1271cdc776 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | 61,519 | 90c2b1c292e9bb0f | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/join_ranking.py` | 4,302 | f8986fc86e7a11e7 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/ranking_joined.csv` | 23,589 | 7b07478b98d67830 | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |
| `docs/handoff/literature_state/t3_ratios.py` | 3,918 | d42c256676fae6ab | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/` |

### Caches removed

Two `__pycache__` folders had been copied although the copy rules exclude caches: `code/handoff_builders/__pycache__`, `code/tools/__pycache__`. Removed in the final pass.

### Laptop paths rewritten to markers (self-containment)

The critic's tree-wide scan still found laptop spellings in copied files of this folder outside `MANIFEST_LOCAL.md`. They are now the markers the other folders use: `<laptop:Desktop>` for the Desktop root that held every repository checkout (`<laptop:Desktop>/spinesurg-ct-nnunet` = spinesurg-ct-nnunet at 097933a, `<laptop:Desktop>/CTSpinoPelvic1K-1` = CTSpinoPelvic1K at 7ddfe38, `<laptop:Desktop>/OpenSpineToolkit` = OpenSpineToolkit at cb43197, `<laptop:Desktop>/XRaySpinoPelvic1K` = XRSpinoPelvic1K at 4f22935), `<laptop:Temp scratchpad>` for the swept session scratchpad (nothing there is a dependency), `<laptop memory folder>` for the live memory notes (copied redacted into `memory/`), `<laptop vendor folder, never read>` and `<laptop home>`. The marker is a spelling of where the file came from, not a path to resolve; the repository and commit are the dependency. Scripts among these copies (`.py`, `.sh`) hard-coded laptop roots and did not run anywhere else before this change either; they are records of how a document was built.

| file | laptop spellings rewritten | left |
|---|---:|---:|
| `code/data_platform/plan/path_refs_files.csv` | 12 | 0 |
| `code/spine_data_review/run_all.sh` | 2 | 0 |
| `code/tools/stats_compare.py` | 1 | 0 |

## Redactions of 2026-10-12 (issue #67)

`docs/PATIENT_IDENTITY_SPEC.md`: three header values of the C-ArmLSpine release replaced by `[withheld]`, the example (0029,0016) value in the carmlspine row of the identity table, and the case134/ori console Patient ID and Patient's Name in collision 16; kinds only, never values. The history of main before this change still holds the values, and it stays: Greg chose on 2026-10-12 to keep the history of main as it is, with no rewrite (issue #71, option (a)). The byte count section 2 gives for this file is the file before this edit.
