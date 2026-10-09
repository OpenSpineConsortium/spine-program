<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path .claude/commands/grid-submit.md. Copied 2026-10-08. Redactions applied by kind: none. Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

Submit a job on the grid for: $ARGUMENTS

Do it in this order, and stop to show me before step 4.

1. Make sure the script to run exists in this repository and takes `--help`; if the job needs a new SLURM script, write it as a FILE under `slurm/` in my project folder by copying `templates/slurm_job.sh` and editing the `#SBATCH` lines (CPUs must match `--workers`, memory in GB, a realistic wall time). Never use `sbatch --wrap`, never send a script through a heredoc over ssh.
2. Commit the files and push (`git push` through WSL on Windows), then sync the grid clone with `tools/grid.sh sync`.
3. Show me the exact submit command, `tools/grid.sh submit <job script> <args>`, and what each `#SBATCH` line asks for.
4. Only after I say "submit", run it, report the job id, and add a dated line with the job id and the command to `JOURNAL.md` in my project folder.
5. Start `tools/grid.sh wait <id>` as a background command so I am told when the job ends, and do not poll in the foreground.
