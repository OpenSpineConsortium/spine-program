The salvaged record (each folder's results/, figures/, manuscripts/ and regulatory/) lives on the grid since 2026-10-13; the tree holds symlinks to it and git history holds the files.

On 2026-10-13 the repository held 6,892 tracked files and 755 MB, too many for a student to load outside Claude Code's
cloud Projects, and 4,379 of them (673 MB) were the salvaged record under the thirteen numbered folders' `results/`,
`figures/`, `manuscripts/` and `regulatory/`. Those 30 folders are now symlinks to the same paths under
`/rs/rs_grp_oschome/shared/spine-program/archive/` on the grid, shipped there once from git history by
`_ops/ship_archive.sh`; the files stay in git history at main 5597197, the last commit whose tree holds them. A clone on
the grid, a Beethoven session's, reads them through the links; a clone anywhere else reads one with
`git show 5597197:<path>` or `git checkout 5597197 -- <path>`, and a task that must change one of them checks it out
into its branch that way, where it then stays tracked. `ARCHIVE.md` at the root is the full account, and each folder's
README.md points to it. `docs/handoff/` copies, `code/`, `docs/` and `memory/` stayed in the tree, since issues edit
them in pull requests and #41 owns the handoff copies. Issue #87.
