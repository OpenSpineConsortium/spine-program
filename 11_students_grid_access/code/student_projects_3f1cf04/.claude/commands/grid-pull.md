<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path .claude/commands/grid-pull.md. Copied 2026-10-08. Redactions applied by kind: none. Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

Bring results back from the grid for: $ARGUMENTS

1. Run `tools/grid.sh pull <remote folder relative to the repo> <local folder>` (through `wsl -e bash -lc` on Windows). Results folders only: never pull `*.nii.gz`.
2. List what arrived with sizes.
3. Open every PNG that arrived with the Read tool and describe what it shows in one sentence each; flag anything that looks wrong (empty axes, a single point, an impossible range).
4. If a report or CSV arrived, print the report and the first five rows of the CSV, and check that one number in the report can be found in the CSV.
5. Remind me to commit the results (`git add <folder> && git commit -m "..."`) and to add a dated line to `JOURNAL.md`.
