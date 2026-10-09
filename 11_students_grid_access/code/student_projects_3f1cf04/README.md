<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path README.md. Copied 2026-10-08. Redactions applied by kind: lead address (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# OpenSpineConsortium · Student_Projects

Student research projects on the consortium's open datasets. This public repository holds
everything reusable: onboarding, templates, tools, the demo study and the ideas list. The
projects themselves live in a private repository,
[OpenSpineConsortium/Projects](https://github.com/OpenSpineConsortium/Projects), cloned
inside this one as `projects/`, so a proposal is reviewed by pull request among
collaborators and stays private until it is published.

**Start here:** [GETTING_STARTED.md](GETTING_STARTED.md) is seven steps: three installs,
clone this repository, open it in VS Code, type `claude` and then `/onboard`. Claude reads
the `CLAUDE.md` at the root of this repository and does the rest with you: the grid
connection, the environment and the dataset on the grid (as jobs), the demo study, and a
project chosen from [IDEAS.md](IDEAS.md) and written up as a proposal.
The three grid steps that need your university identity (account, Google Authenticator,
SSH key) are spelled out there. The long-form version, with the reasons behind each step,
is the [OSC Primer](https://openspineconsortium.github.io/onboarding/).

The method behind every step — roles, pre-registration, the grid rules, how a number reaches
a manuscript, how to hand a project over — is [RECIPE.md](RECIPE.md). Every project in the
lab, who leads it and how to join is [BOARD.md](BOARD.md).

## How a project moves

| step | who | where |
|---|---|---|
| 1. Read the primer and run the demo study | you | `examples/pelvic_width_dimorphism/` |
| 2. Write a one-page proposal from the template | you | `templates/proposal_template.md` |
| 3. Open a pull request adding `<lastname>_<topic>/proposal.md` in the private Projects repository (`projects/`) | you | GitHub, using the PR template; `/new-project` does it |
| 4. Review, questions, revisions in the PR thread | mentor and you | GitHub (private) |
| 5. Approval, merge, ClickUp invitation to the email in your PR | mentor | ClickUp |
| 6. Work in your project folder on a branch; milestones tracked in ClickUp | you | `projects/` and ClickUp |
| 7. Results, figure code and a write-up in the same folder; final PR | you | `projects/` |

The worked example, [examples/proposal_example/proposal.md](examples/proposal_example/proposal.md),
is the proposal every new one should imitate.

## Layout

```
Student_Projects/
├── README.md                     this file
├── GETTING_STARTED.md            the seven steps from an empty laptop; then /onboard
├── CLAUDE.md                     read by Claude Code in every session: the lab in one page
├── CONTRIBUTING.md               the pull-request procedure and house rules
├── .github/PULL_REQUEST_TEMPLATE.md
├── templates/
│   ├── proposal_template.md      copy this to projects/<lastname>_<topic>/proposal.md
│   ├── CLAUDE.md                 copy this into your project folder so Claude Code knows the grid
│   ├── environment.yml           the mamba environment every project starts from
│   ├── slurm_job.sh              a SLURM job script that runs a Python script on the grid
│   ├── make_env.sh               a job that installs Miniforge if needed and builds `osc`
│   ├── get_dataset.sh            a job that fetches the v10 labels and metadata from Hugging Face
│   └── ssh_config                the ~/.ssh/config entry that makes `ssh grid` work
├── tools/grid.sh                 run / sync / submit / wait / pull, the five remote calls a project needs
├── .claude/
│   ├── settings.json             commands Claude may run without asking (git, python, ssh grid, rsync)
│   └── commands/                 /onboard, /grid-status, /grid-submit, /grid-pull, /new-project
├── IDEAS.md                      twenty-odd project ideas with the measurement, comparison and difficulty
├── examples/
│   ├── pelvic_width_dimorphism/  the demo study, end to end, with its results
│   └── proposal_example/         the worked example proposal
└── projects/                     NOT part of this repository: the private Projects repo, cloned here
    └── <lastname>_<topic>/       one folder per project
```

## Rules that keep this repository usable

- **No imaging data in git.** CT and label volumes stay on the grid or your disk; `.gitignore`
  blocks `*.nii.gz`. Commit code, small CSVs of derived measurements, figures and text.
- **Every figure has a script that regenerates it** from the released data, with the
  environment pinned in `environment.yml`.
- **One project, one folder, one branch per piece of work.** Never commit to `main` directly.
- **Cite the dataset** you used, by its DOI, in anything you write or present.
- **Nothing heavy runs on the login node, and job scripts are files, never heredocs.**
  `templates/CLAUDE.md` says why; `tools/grid.sh` makes the right thing the easy thing.

Questions: Gregory Schwing, [the lead's university address].
