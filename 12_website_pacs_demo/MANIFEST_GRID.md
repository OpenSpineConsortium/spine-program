# MANIFEST_GRID.md — grid paths this project uses or produced

HOME = `/wsu/home/go/go24/go2432`; Ceph = `/rs/rs_grp_oschome/go2432`. Nothing of this project runs on the grid: the site
is built on a laptop and published by `git push`; the demo exporter runs wherever the CT and label sit (on the grid that
means inside an `sbatch` job, never on the login node). The rows below are the grid paths the website family owns or
depends on, read from the one read-only `ls` pass of 2026-10-08 22:20 UTC (its output is
`10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`; the census files sit beside it under
`census/`), `data_platform/DATA_MANIFEST.md` of `spinesurg-ct-nnunet` at 097933a and the memory notes. Nothing on the
grid was written. "Verified" means a listing or a file on the grid showed it, not that a job checked its contents. A
bare "line N" below is a line of `grid_ls_2026-10-08.out`.

| path | what it holds | size | volume | migration state | verified | note |
|---|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/level_id_service` | `app.py`, `model_defs.py`, `weights/`, `service.log`, `service.pid`, `__pycache__`; folder dated 2026-09-14 07:14 | not sized (no file records it); the detector weight it shipped, `detector_v5z_epoch25`, is 168,005,677 B under registry hash `5fde3060dbc15b71` (the `registry.jsonl` line at line 2661 of `10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`; the registry folder at line 2543 and the alias symlink at line 2603) | HOME | in no migration batch (`data_platform/plan/batch_items/B00-B14.tsv` do not name it, checked 2026-10-08) | `ls` 2026-10-08 (the folder at line 745; its six entries at lines 2933-2938) | the level service as it was run on the login node on 2026-09-14 (`memory/level-service-serving.md`: "measured on the grid login node"); it must never run there again; it is a different product from the site (the site calls a hosted service); the weights are never copied anywhere public; a second HOME copy of `detector.pt` sits under `~/FluoroCap/` (`DATA_MANIFEST.md` line 17898) |
| `/rs/rs_grp_oschome/go2432/data/gallery` | gallery renders: 472 files (404 `.png`, 62 `.npz`, 5 `.json`, 1 `.md`) | 0.106 GB (`10_data_platform_grid/docs/grid_read_2026-10-08/census/ceph/census.tsv` line 57; its neighbours `fig6` 13.920 GB and `figure1` 0.027 GB are lines 55-56) | Ceph | Ceph-native: never on HOME, nothing to migrate | `ls` 2026-10-08 (line 1415: folder dated 2026-09-23 03:25, link count 6 and CephFS size 4, so four subdirectories; its contents were not listed) | which build produced the 12 `.bin` meshes under `assets/gallery/` of the site (874,636 to 1,327,480 B; `git ls-files '*.bin'` at c1800f8, 2026-10-08) is not recorded; the site's `gallery/` folder is dated 2026-08-22 |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/gallery_data`, `gallery_meshes`, `gallery_stills` | the older gallery build folders inside the public repository's checkout, dated 2026-08-21 02:52, 2026-08-22 18:20 and 2026-08-21 22:19 | 0.000, 0.018 and 0.004 GB (1, 30 and 93 files; `census/census_merged_partial.tsv` lines 1739-1741) | HOME | stays on HOME (the checkout `~/CTSpinoPelvic1K` is 7.699 GB, 4,541 files, in `census/census_merged_partial.tsv` line 1722, while `census/_du_home.txt` line 1 gives 1.9 TB for the same path and `census/_du_data.txt` puts `data/tcia` alone at 721 GB: the census row evidently leaves out the `data/` tree; which figure is "the whole checkout" is not reconciled here) | `ls` 2026-10-08 (lines 2268-2270) | owned by `03_ctspinopelvic1k_dataset`; listed here because their dates match the site's gallery |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/itksnap_v6_labels.txt` (with `itksnap_v4_labels.txt`, `itksnap_v5_labels.txt`) | the ITK-SNAP label descriptor the two poster render scripts in `figures/visual_abstract/` read | 5,421 B (v6, 2026-08-27); 3,735 B (v4, 2026-06-29); 4,356 B (v5, 2026-08-20) | HOME | stays on HOME | `ls` 2026-10-08 (lines 2285-2287) | the copied scripts were patched to read it from beside themselves (`MANIFEST_LOCAL.md`) |
| `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K` (`ct/`, `labels/`) | the release CTs and labels; the input of `export_demo_case.py` | see `10_data_platform_grid` | HOME, symlinked to Ceph per the migration notes | batch state in `10_data_platform_grid` | — | the bundled demo case 0003 is a legacy-scheme (v3) export; where that older label revision now lives is not recorded; a re-export must start from v11 labels with `labels_for` (`TODO.md` step 6) |
| `/wsu/home/go/go24/go2432/model_registry` | the content-addressed weights store and ledger (`registry.jsonl`, `aliases`) | see `01_carm_level_detection` | HOME | — | `ls` 2026-10-08 | owned by 10 (the store and the ledger; final pass 2026-10-08); 01 registers the weights the service uses; the service names them by registry id |

## Not on the grid

- The level service's hosted instance. `SERVICE_DEFAULT` (`https://level-id.openspineconsortium.org`) was not live on
  2026-09-14 (`memory/level-service-serving.md`); Hugging Face Docker Spaces returned 402 for both accounts that day; the
  options recorded were Modal (`service/modal_app.py` exists), Fly.io, EC2 or a workstation behind a tunnel. No file
  records a later check. The decision is `01_carm_level_detection` S2 (Greg).
- The site itself: GitHub Pages, branch `master`, folder `/`, custom domain `openspineconsortium.com` (`CNAME`).
- The private weights repository `gregoryschwingmdphd/level-id-weights` (Hugging Face) and the empty private
  `OpenSpineConsortium/level-id-weights` (`memory/level-service-serving.md`, 2026-09-14; live state not re-checked).
