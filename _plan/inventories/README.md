# _plan/inventories: the seven inventories of 2026-10-08

The seven inventory notes and their TSVs that `PLAN.md` (section "Sources"), `DISPOSITION.tsv` (row ids such as `carm r24`, `grid r164`) and every project folder's `MANIFEST_GRID.md`, `MEMORY.md` and `MANIFEST_LOCAL.md` cite by short name. They were written on 2026-10-08 between 18:28 and 18:50 in the build session's scratchpad (`seed/notes/`), which is swept, and copied here in the fix pass of the same day so the citations resolve inside this repository.

A row id `<family> rNN` is the TSV row counted from 1 after the header line. The `source_path` columns and the prose carry the laptop spellings of 2026-10-08 (`C:/Users/...`): they are history, not dependencies; each project folder's `CLAUDE.md` "Prefixes in the copied documents" gives the repository prefixes. Inventory 5 (`grid_manifest`) was read on the grid with `ls`, `cat` and `squeue` only, at 22:20 UTC; nothing was run or written.

One redaction by kind: a faculty surname inside an IRB printout's file name was replaced by `[faculty-surname]_IRB.pdf` (4 occurrences across `carm_hospital_path` and `ctsp_repo_root_and_sibling_folders`). Nothing else was changed. The inventories name personal and credential files on the laptop and the grid by path only (so nothing is lost by accident); none of their contents is here. The three build scripts beside them in the scratchpad (`build_inv7.py`, `build_inv7_note.py`, `make_spinesurg_inventory.py`) hard-code laptop roots and were not copied.

| file | bytes (source) | what it is |
|---|---:|---|
| `carm_hospital_path.md` | 58,199 | Inventory 6: from SchwingNet as it stands to a model tested on real fluoroscopy at the hospital (the C-arm path; its own grid `ls` of 2026-10-08) |
| `carm_hospital_path.tsv` | 42,027 | Inventory 6: from SchwingNet as it stands to a model tested on real fluoroscopy at the hospital (the C-arm path; its own grid `ls` of 2026-10-08) (table) |
| `ctsp_repo_root_and_sibling_folders.md` | 34,008 | Inventory 2: the CTSpinoPelvic1K repository, its root clutter and 28 sibling folders |
| `ctsp_repo_root_and_sibling_folders.tsv` | 48,941 | Inventory 2: the CTSpinoPelvic1K repository, its root clutter and 28 sibling folders (table) |
| `desktop_root_loose_files.md` | 14,177 | Inventory 4: the loose files at the Desktop root |
| `desktop_root_loose_files.tsv` | 37,997 | Inventory 4: the loose files at the Desktop root (table) |
| `grid_manifest.md` | 57,222 | Inventory 5: what is on the grid and what is not (HOME and Ceph, migration state, registry, result roots, missing items) |
| `grid_manifest.tsv` | 51,424 | Inventory 5: what is on the grid and what is not (HOME and Ceph, migration state, registry, result roots, missing items) (table) |
| `inventory3_other_spine_folders.md` | 42,311 | Inventory 3: the other spine-relevant folders on the Desktop |
| `inventory3_other_spine_folders.tsv` | 29,890 | Inventory 3: the other spine-relevant folders on the Desktop (table) |
| `memory_and_handoff_map.md` | 58,119 | Inventory 7: memory notes and HANDOFF sections mapped to project families (the per-project cut lists) |
| `memory_and_handoff_map.tsv` | 152,752 | Inventory 7: memory notes and HANDOFF sections mapped to project families (the per-project cut lists) (table) |
| `spinesurg_ct_nnunet.md` | 46,831 | Inventory 1: the spinesurg-ct-nnunet repository at 097933a |
| `spinesurg_ct_nnunet.tsv` | 80,296 | Inventory 1: the spinesurg-ct-nnunet repository at 097933a (table) |
