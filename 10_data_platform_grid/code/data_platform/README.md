# data_platform

Planning files for the imaging holding: where every source came from, how to fetch it again, where it goes on the
CephFS volume, how to move it there, and how to index it. Written 2026-10-08 and revised the same day after a review
(VERIFICATION.md section 5) and after a grid inspection identified the HOME entries nobody had named (section 6;
they move or stay in batch B14). Migration jobs for B00-B09 read their item files on the grid; that revision left
the item files of B00-B13 byte-identical. Commit and push `data_platform/` before the first
grid job: the sbatch scripts run the copy under `~/spinesurg-ct-nnunet`, and each needs its `logs/` folder (committed
as `logs/.gitkeep`).

| file | what |
|---|---|
| `DATA_MANIFEST.md` | the human manifest: what the holding is, a dated-acquisition timeline, the defects that matter, and one card per source (211) with every citation |
| `sources.yaml` / `sources.json` | the same facts, machine-readable (edit the JSON, then `sync_sources_yaml.py`) |
| `LAYOUT.md` | the target layout on `/rs/rs_grp_oschome/go2432/data`, naming rules, and the mapping of every imaging entry |
| `MIGRATION_PLAN.md` | the ordered procedure, batches B00-B14, verification, cut-over with symlinks, rollback, end state |
| `reacquire/` | `reacquire.py` (dry run by default; `--run` in a job), `reacquire.sbatch`, tests, README |
| `db/` | `SCHEMA.sql`, `build_index.py`, `build_index.sbatch`, tests, README |
| `plan/` | `build_plan.py` and what it writes (`layout_map.csv`, `migration_batches.csv`, `batch_items/`, `readme_yaml/`), the migration jobs (`preflight.sbatch`, `migrate_batch.sbatch`, `verify_transfer.py`, `cutover.sh`, `remap_manifest.py`), `test_migration.sh`, and the inputs copied from the scratchpad (`disk_map.csv`, `path_refs_*.csv`) |
| `lib/mini_yaml.py` | the standard-library YAML reader and writer the rest uses |
| `VERIFICATION.md`, `verify_planning.py` | what to check, and the checks run here |

Start with `DATA_MANIFEST.md` section 1, then `MIGRATION_PLAN.md` section 0.
