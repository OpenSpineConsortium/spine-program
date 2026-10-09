<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path CLAUDE.md. Copied 2026-10-08. Redactions applied by kind: none. Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# CLAUDE.md — OpenSpineConsortium Student_Projects

You are working with a student on an OpenSpineConsortium research project. Most students
are learning to code. Explain what a command does in one line before running it, prefer
small readable scripts, say when you are unsure, and never run anything heavy on the grid's
login node. The complete lab workflow, rules and grid defaults are in `templates/CLAUDE.md`;
a project folder carries its own filled-in copy. Read whichever applies before doing
anything, and read `GETTING_STARTED.md` if the student is new.

## First session in a fresh clone

If there is no `projects/<lastname>_*` folder yet, or the student says they are new, offer
to run `/onboard`. It checks the laptop tools, sets up the SSH connection to the grid,
builds the `osc` environment and fetches the dataset on the grid as SLURM jobs, runs the
demo study, and then helps choose a project from `IDEAS.md` and write the
proposal with `/new-project`. It is resumable: every step first checks whether it is
already done.

## The two machines, in one paragraph

Claude Code runs on the laptop (inside VS Code). The WSU grid (`grid.wayne.edu`, login node
`warrior`, SLURM) is reached as `ssh grid` through `~/.ssh/config` with an SSH key, which is
what lets non-interactive `ssh -o BatchMode=yes grid ...` work without the grid's
two-factor prompt. Code moves through git (push from the laptop, `git pull` on the grid);
data stays on the grid at `~/data/CTSpinoPelvic1K`; results come back small with `rsync`.
On Windows the network commands run through Git Bash or `wsl -e bash -lc '...'`.

## Rules that never bend

- Anything over a minute or a few GB runs as a SLURM job; the login node is for `ls`,
  `squeue`, `tail`, `git`.
- Job scripts are files in the repository, never heredocs or `sbatch --wrap` over SSH.
- Claude drafts, the student submits (or says "submit it" and you run exactly one `sbatch`).
- Never reorient a volume; read axes from the affine; volumes are stored P,I,R.
- Never commit imaging data; never edit a result by hand; every number in a write-up was
  written to `results/` by a script.
- Read `dataset_labels.json` for identifiers and `KNOWN_ISSUES.md` before any analysis.

## Where things are

| what | where |
|---|---|
| the human checklist | `GETTING_STARTED.md` |
| the lab workflow in full | `templates/CLAUDE.md` |
| the lab method: roles, pre-registration, the grid, how a number reaches a manuscript, handover | `RECIPE.md` |
| the project board: every project, its lead, how to join | `BOARD.md` (rendered from `board.json` by `tools/render_board.py`) |
| environment, job, SSH templates | `templates/environment.yml`, `slurm_job.sh`, `make_env.sh`, `get_dataset.sh`, `ssh_config` |
| the five remote calls | `tools/grid.sh` (run, sync, submit, wait, pull) |
| slash commands | `.claude/commands/` (`/onboard`, `/grid-status`, `/grid-submit`, `/grid-pull`, `/new-project`) |
| the demo study | `examples/pelvic_width_dimorphism/` |
| project ideas | `IDEAS.md` |
| the projects themselves | `projects/`, a clone of the PRIVATE repository OpenSpineConsortium/Projects; it is ignored by this public repository, and every commit, branch, push and pull request for a project happens inside it |
| proposal template and procedure | `templates/proposal_template.md`, `CONTRIBUTING.md` |
| the primer | https://openspineconsortium.github.io/onboarding/ |

## Session start

`git status` locally; `ssh -o BatchMode=yes grid hostname` (expect `warrior`); `squeue -u $USER`
on the grid; `git pull` on the grid if the student pushed; read the last five lines of the
project's `JOURNAL.md`; then ask what we are doing today.
