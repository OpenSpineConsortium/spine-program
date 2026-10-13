# ARCHIVE: the record material lives on the grid

Since 2026-10-13 (issue #87) the salvaged record of each numbered folder, its `results/`, `figures/`, `manuscripts/` and
`regulatory/`, is no longer in this tree. Those 30 folders are symlinks to the same paths under

    /rs/rs_grp_oschome/shared/spine-program/archive/

on the Wayne State grid, and every file they held stays in git history at **main 5597197**
(`55971971cd6bba0bd2dda034665f415162924c90`, the last commit whose tree holds them). Before the move the repository held
6,892 tracked files and 755 MB; 4,379 of them, 673 MB, were these folders, and a student could not load the repository
outside Claude Code's cloud Projects. The tree now holds about 2,550 files and 82 MB: the eight documents of every folder,
`memory/`, `docs/` (the handoff copies included, which #41 owns), `code/`, the plan and the tools.

## What moved

| Folder | Folders now on the grid |
|---|---|
| 01_carm_level_detection | results, figures, manuscripts, regulatory |
| 02_transitional_naming_truth | results, manuscripts |
| 03_ctspinopelvic1k_dataset | results, figures, manuscripts |
| 04_openspinetoolkit | results, figures, manuscripts |
| 05_ct_morphometry_parity | results, figures |
| 06_transitional_ct_census | results, figures |
| 07_plain_film_level_id | results, figures, regulatory |
| 08_render_devices | results, figures |
| 09_wrong_level_clinical_qi | results, figures, manuscripts |
| 10_data_platform_grid | results |
| 11_students_grid_access | figures, manuscripts, regulatory |
| 12_website_pacs_demo | figures |
| 99_archive | manuscripts |

Every path a document in this repository quotes under one of those folders (`results/physics/...`, a figure, a packet) is
still that path: on the grid through the link, in git history at the commit above. The counts and sizes in each folder's
`MANIFEST_LOCAL.md` describe the folder as it was built on 2026-10-08 and are history.

## How to read a file

- **On the grid** (a Beethoven session, or any clone under your grid account): the symlink resolves, so
  `01_carm_level_detection/results/schwingnet/JOBS.txt` reads as before, once `_ops/ship_archive.sh` has run (below) and your
  AccessID is on the lab volume's access list. `ls -l 01_carm_level_detection/results` shows where the link points.
- **Anywhere else** (a claude.ai Project thread, a laptop clone): the link dangles, and the file is read from history:
  `git show 5597197:01_carm_level_detection/results/schwingnet/JOBS.txt`, or `git ls-tree -r --name-only 5597197
  01_carm_level_detection/results` to list a folder. A single-branch clone, as a cloud session's is, has the commit as
  main's ancestor already; otherwise `git fetch origin main` brings it.
- On a Windows checkout without `core.symlinks`, git writes each link as a small text file holding the grid path. That is
  harmless and still says where the folder went.

## How a task changes one of those files

Issues that write into `results/` or `manuscripts/` (#22, #23, #26, #27, #33, #35, #38, #39 on 2026-10-13) bring the
file, or the folder, back into their branch first, where it then stays tracked and lands in the pull request as any other
change:

    git rm --cached 05_ct_morphometry_parity/results        # drop the link from the index
    rm 05_ct_morphometry_parity/results                     # and from the tree (a link, not the files)
    git checkout 5597197 -- 05_ct_morphometry_parity/results/morphometrics   # the folder, or one file, from history
    git add 05_ct_morphometry_parity/results

A new result produced on the grid lands as the issue says: a small file (a table, a count, a log excerpt) in the branch
with its number and the path it came from, a large one on the lab volume with its path in `MANIFEST_GRID.md`.

## Shipping (Greg, once)

`_ops/ship_archive.sh`, run from the top folder of a clone on a computer with ssh to the grid (WSL on Windows), ships the
30 folders from the commit above, never from a working tree, by the `git archive | ssh tar` route of RECIPES.md section
0 item 2 into `/rs/rs_grp_oschome/shared/spine-program/archive/`, records the commit in `SHIPPED_COMMITS.txt` there and
submits a short job that opens the read bits, as job 40602926 opened the python environment. Until it has run, the links
on the grid dangle and the history route above is the one that works. Shipping again after a later move overwrites in
place: the folder is a copy of the record, not a working area.

## Undo

The move is one commit. `git revert` of it, or `git checkout 5597197 -- <folder>/<sub>` for one folder, brings the files
back into the tree.
