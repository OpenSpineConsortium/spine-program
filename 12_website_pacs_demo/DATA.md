# DATA.md: this folder's data on the grid, reached through Beethoven

How a student reaches the grid material of 12_website_pacs_demo and runs the first step. Nothing
of this project runs on the grid: the site is built on a laptop and published by `git push`; the
demo exporter runs wherever the CT and label sit, on the grid inside an `sbatch` job, never on the
login node (`MANIFEST_GRID.md` header; `CLAUDE.md` rule 7). The paths below are every row of
`MANIFEST_GRID.md`, spelled as that manifest spells them: HOME = `/wsu/home/go/go24/go2432`,
Ceph = `/rs/rs_grp_oschome/go2432`. Sizes, dates and contents come from `MANIFEST_GRID.md`; what
no file records is written "not recorded".

Every check line below is read-only (`ls -ld` for a directory or a link, `head -c 200` for a
file) and runs from the Beethoven worker — a session on a compute node — never python on the
login node (`CLAUDE.md` rule 7; read-only `ls`, `stat` and `cat` of small files are the one thing
the login node is for). Set once, then paste a check line:

```
H=/wsu/home/go/go24/go2432; C=/rs/rs_grp_oschome/go2432
```

A check line on a HOME path works only for Greg: nothing on HOME is readable by students (see
"Access", below). Each HOME row is marked **on HOME, not reachable until migrated**, with the
manifest's own migration state beside it where the manifest records one.

## The paths (every row of `MANIFEST_GRID.md`)

| path | volume | what it holds | access today | check line |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/level_id_service` | HOME | `app.py`, `model_defs.py`, `weights/`, `service.log`, `service.pid`, `__pycache__`; the level service as it was run on the login node on 2026-09-14, which must never happen again (`memory/level-service-serving.md`); folder dated 2026-09-14 07:14; not sized (no file records it); the detector weight it shipped, `detector_v5z_epoch25`, is 168,005,677 B under registry hash `5fde3060dbc15b71` | on HOME, not reachable until migrated; in no migration batch (`data_platform/plan/batch_items/B00-B14.tsv` do not name it, checked 2026-10-08); the weights are private and never copied anywhere public | `ls -ld $H/level_id_service` (resolves only for Greg) |
| `/rs/rs_grp_oschome/go2432/data/gallery` | Ceph | gallery renders: 472 files (404 `.png`, 62 `.npz`, 5 `.json`, 1 `.md`); 0.106 GB; folder dated 2026-09-23, four subdirectories, contents not listed on 2026-10-08 | Ceph-native, never on HOME, nothing to migrate; readable by approved students (under Ceph `/data/`) | `ls -ld $C/data/gallery` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/gallery_data`, `gallery_meshes`, `gallery_stills` | HOME | the older gallery build folders inside the public repository's checkout, dated 2026-08-21 02:52, 2026-08-22 18:20 and 2026-08-21 22:19; 1, 30 and 93 files (0.000, 0.018 and 0.004 GB); owned by `03_ctspinopelvic1k_dataset`, listed because their dates match the site's gallery | on HOME, not reachable until migrated; the manifest records the checkout staying on HOME | `ls -ld $H/CTSpinoPelvic1K/gallery_meshes` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/itksnap_v6_labels.txt` (with `itksnap_v4_labels.txt`, `itksnap_v5_labels.txt`) | HOME | the ITK-SNAP label descriptor the two poster render scripts in `figures/visual_abstract/` read; 5,421 B (v6, 2026-08-27), 3,735 B (v4), 4,356 B (v5); the copied scripts were patched to read it from beside themselves (`MANIFEST_LOCAL.md`) | on HOME, not reachable until migrated; the manifest records it staying on HOME | `head -c 200 $H/CTSpinoPelvic1K/data/itksnap_v6_labels.txt` |
| `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K` (`ct/`, `labels/`) | spelled on HOME; resolves to Ceph | the release CTs and labels, the input of `export_demo_case.py`; size and batch state in `10_data_platform_grid` | the HOME spelling is a symlink and resolves only for Greg; students use its Ceph target, `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` (`03_ctspinopelvic1k_dataset/MANIFEST_GRID.md` section 1; batch B02 cut over 2026-10-08), readable by approved students | `ls -ld $C/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels` |
| `/wsu/home/go/go24/go2432/model_registry` | HOME | the content-addressed weights store and ledger (`registry.jsonl`, `aliases`); owned by `10_data_platform_grid`; `01_carm_level_detection` registers the weights the service uses, and the service names them by registry id; size: see `01_carm_level_detection` | on HOME, not reachable until migrated; its migration state is not recorded in this folder's manifest; the weights are private (`CLAUDE.md` rule 8) | `ls -ld $H/model_registry` (resolves only for Greg) |

Two notes the manifest carries with these rows:

- Which build produced the 12 `.bin` meshes under the site's `assets/gallery/` (874,636 to
  1,327,480 B by `git ls-files '*.bin'` at c1800f8) is not recorded; the site's `gallery/` folder
  is dated 2026-08-22.
- The bundled demo case 0003 is a legacy-scheme (v3) export; where that older label revision now
  lives is not recorded; a re-export must start from v11 labels with `labels_for`
  (`TODO.md` step 6).

## Not on the grid (`MANIFEST_GRID.md`, "Not on the grid")

- **The site itself**: GitHub Pages, branch `master`, folder `/`, custom domain
  `openspineconsortium.com` (`CNAME`).
- **The level service's hosted instance.** `SERVICE_DEFAULT`
  (`https://level-id.openspineconsortium.org`) was not live on 2026-09-14
  (`memory/level-service-serving.md`); Hugging Face Docker Spaces returned 402 for both accounts
  that day; the recorded options are Modal (`service/modal_app.py` exists), Fly.io, EC2 or a
  workstation behind a tunnel. No file records a later check. The decision is
  `01_carm_level_detection` S2 (Greg's).
- **The weights repository**: the private `gregoryschwingmdphd/level-id-weights` (Hugging Face)
  and the empty private `OpenSpineConsortium/level-id-weights`
  (`memory/level-service-serving.md`, 2026-09-14; live state not re-checked).

## Terms

- The release CTs and labels are **CTSpinoPelvic1K v11, CC BY-NC-SA 4.0** on Zenodo (v11 =
  10.5281/zenodo.22797014, published 2026-09-18; `03_ctspinopelvic1k_dataset/DATA.md` "Terms";
  `03_ctspinopelvic1k_dataset/docs/release/README.md`, licence section).
- The service weights are **private and never served by the site**: no `.pt`, `.onnx` or `.bin`
  model file is ever added to the website repository; the 12 `.bin` files under `assets/gallery/`
  are meshes, not models (`CLAUDE.md` rule 8; `STATUS.md` site-2).
- **No radiograph is ever added to the site tree**: `pacs/testimgs/` (BUU films, not
  redistributable), `pacs/webtest/` and `pacs/sllp/` stay untracked and are never added
  (`CLAUDE.md` rule 9; `README.md`, "State on 2026-10-08").
- For everything else the manifest lists (the gallery renders, the older gallery build folders,
  the ITK-SNAP descriptors, the service folder, the registry): not recorded in the folder.

## Access (Greg's facts of 2026-10-11, issue #10)

- **Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students** — a
  named ACL entry on the volume root, other-read bits on folders and files — including
  `vindr_spinexr`, `buu_lspine_3600`, `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and
  `spine_detector_corpus`, because every approved student holds the PhysioNet credential and the
  VinDr and BUU agreements.
- **On 2026-10-12 the VinDr and BUU items inside those folders opened too.** Until then the
  plan's `restricted` flag still closed them item by item, mode `drwx--S---` (`vindr/raw`,
  `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr and BUU banks of B10 and B11,
  `dis_renders`); the script was fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs
  40599886 (the B04, B05, B10 and B14 folders) and 40599867 (after B13's finalize, every chain
  folder including `multisource_banks`) open them (issue #65).
- **Two paths stay closed (owner-only):**
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`,
  private build material and not a dataset, and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`, until Greg reads its
  Zenodo upload scripts for a token (issue #65;
  `../10_data_platform_grid/code/data_platform/plan/publish_visibility.sh`, from
  spinesurg-ct-nnunet d9b388d).
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students; items
  still there are moved to the Ceph volume by the data-platform plan, whose batch-by-batch state
  is `../10_data_platform_grid/MANIFEST_GRID.md` section 2. Every HOME row above is marked
  'on HOME, not reachable until migrated'.
- Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`.

## Through Beethoven

The way in is Beethoven, the lab's Chrome extension: install and use it per
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (the same pages are at
https://openspineconsortium.com/beethoven/). A student needs: a WSU AccessID with a grid
account, the Google Authenticator grid code, Claude Pro or Max, and Chrome on the invited Google
account. Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`.

The two access facts, again, because everything above depends on them:

- every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named
  ACL entry on the volume root; other-read bits on folders and files), and since 2026-10-12 the
  VinDr and BUU items inside them; two paths stay closed,
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`
  (private build material, not a dataset) and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (until Greg reads its
  Zenodo upload scripts for a token);
- nothing on `/wsu/home/go/go24/go2432` is readable by students until the data-platform plan has
  moved it to Ceph.

Run the check lines above from the Beethoven worker. The only computation this project can send
to the grid is the demo re-export (`TODO.md` step 6), and that is an `sbatch` job on a compute
node, never a command on the login node (`CLAUDE.md` rule 7; `TODO.md`, "What is not on the grid
and will not be").

## First experiment: `TODO.md` step 1, laptop only

This is the first step `TODO.md` names, and it runs on the laptop, not on the grid: the site is
cloned, pulled and built where it is edited. Nothing in this experiment touches a grid path.

1. **Clone.** `OpenSpineConsortium/openspineconsortium.github.io`, branch `master`, the
   repository `MANIFEST_CODE.md` section 1 names. Network (clone, pull, push) goes through
   `wsl -e bash -lc '...'` (`CLAUDE.md` rule 10).
2. **Pull.** `git pull` before any edit, every time: the clone this seed was read from (c1800f8,
   2026-10-02) was ten commits behind origin (a17ea39, 2026-10-07); the ten commits are the
   lab-storage request page and the admin section (`MANIFEST_CODE.md` section 1). The gate,
   written before the run (`TODO.md` step 1): a clean fast-forward, the lab-storage request page
   and the admin section present, `git status -sb` showing no divergence. The pre-stated number
   is **0 commits behind, 0 ahead, 0 conflicts**.
3. **Build check.** `python -X utf8 tools/build_site.py --check-only` exits 0 on a clone that is
   0 behind, 0 ahead (`README.md`, "Success criteria" and "How to start"; the flag is in
   `MANIFEST_CODE.md` section 1's description of `build_site.py`).
4. **The reference, at c1800f8** (`STATUS.md` site-1 and site-2): 420 tracked files; 25 body
   fragments under `tools/pages/`; 41 sitemap entries; 0 `.pt` or `.onnx`; 12 `.bin` files, all
   gallery meshes under `assets/gallery/`. What the counts are at a17ea39 is not recorded in the
   folder; a pull that changes them is read before it is trusted.

The folder is student-safe (the site is public and its names are there by design); a hand-out
waits on Greg's answers to `docs/handoff/OPEN_QUESTIONS.md` A29 and A30 (`README.md`;
`TODO.md` step 14).
