# STUDENT_ENV.md: the python a student uses on the grid, and how code reaches the worker

One page for a student with an approved grid account: which python to run on the grid, how to build one's own until
the shared one is open, and how code gets from a laptop clone to the Beethoven worker. Written for issue #66 (the
readiness review of 2026-10-12, findings F7 and S4, and a read-only grid check of 2026-10-12). Like the rest of this
folder, it is handed to students once Greg confirms the reader split (`CLAUDE.md` "Reader"; OPEN_QUESTIONS A29, A30).

Two rules hold for everything below. Nothing runs on the login node (warrior): building an environment, importing a
package and downloading are `sbatch` jobs, and warrior kills python, pip and conda by name (`CLAUDE.md` "Standing
rules"; `docs/handoff/RECIPES.md` section 0 item 1). A job script is a file saved with an editor, never a heredoc
(root `CLAUDE.md` rule 10). `<AccessID>` below is your own grid account; inside a job the same value is `$USER`.

## Which python

| interpreter | what it is | can a student use it on 2026-10-12 | source |
|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/envs/spineps212/bin/python` | the lab's shared environment on Ceph (section 1) | not yet: 209 files under its site-packages are not readable by others until Greg's one step is done | issue #66 |
| `/rs/rs_grp_oschome/<AccessID>/envs/spineps/bin/python` | your own environment, built from `10_data_platform_grid/code/env/spineps.yml` (section 2) | yes, once the build job has written its `ENV_OK` marker | this page |
| `/wsu/home/go/go24/go2432/mambaforge/envs/spineps/bin/python` | Greg's interpreter; the handoff recipes write it as `~/mambaforge/envs/spineps/bin/python` | no: it is on Greg's HOME, which students cannot read | `../10_data_platform_grid/DATA.md`; issue #66 |

A recipe that names `~/mambaforge/envs/...` means Greg's HOME, not yours (`CLAUDE.md` "The student's `~` is not
Greg's"). The shared environment and your own are not the same environment: the job record calls `spineps212` "the
SPINEPS 2.1.2 env", while `spineps.yml` pins `spineps==2.1.1`, `torch==2.6.0`, `nibabel==5.4.2`, `scipy==1.15.3` and
`python=3.11.16`. Write in your results which interpreter produced them.

Before either route, make your own folder on Ceph from the Beethoven worker:
`mkdir -p /rs/rs_grp_oschome/<AccessID>/envs`. Approval is a `user:<AccessID>:rwx` entry on the volume root, which
lets you create it (`MANIFEST_GRID.md` section 1). Submit jobs from the Beethoven worker; one `sbatch` on the login
node is also allowed (`docs/beethoven/repo_root/CLAUDE.md` "Grid etiquette").

## 1. The shared environment `spineps212`

What is recorded:

- Path `/rs/rs_grp_oschome/go2432/envs/spineps212`: 10.824 GB, 69,154 files, newest file 2026-09-27 (census job
  40580051, `../10_data_platform_grid/docs/grid_read_2026-10-08/census/ceph/census.tsv`).
- Read on the grid on 2026-10-12 (issue #66): python 3.11; nibabel, scipy, numpy, SimpleITK, torch and spineps present;
  the folders and the interpreter are readable and executable by others, but 209 files under its site-packages (depth 2)
  were not other-readable, so a student's import can fail until Greg makes the environment readable.
- The job record says `env_spineps212.sh` built it; its GPU smoke, job 40480757, was recorded PENDING and then cancelled
  on 2026-09-27 (`../10_data_platform_grid/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`;
  `../_plan/GRID_MANIFEST_2026-10-08.md`). No smoke result of this environment is recorded. Where `env_spineps212.sh`
  lives, the environment's full package list and whether its torch is a CUDA build are not recorded.

**Greg's step, once.** One `chmod`, as a job, never on the login node:

```bash
sbatch -D /rs/rs_grp_oschome/go2432/envs --job-name=chmod_spineps212 --partition=reqp --qos=requeue \
  --time=00:30:00 --wrap 'chmod -R o+rX /rs/rs_grp_oschome/go2432/envs/spineps212'
```

The last `chmod -R o+rX` of this kind, on 34,000 files of the shared Beethoven tree, took 23 s (`MANIFEST_GRID.md`
section 1); half an hour is a margin, not a measurement. State on 2026-10-12: not run (issue #66).

**A student's check.** Save this file as `/rs/rs_grp_oschome/<AccessID>/envs/check_spineps212.sbatch`:

```bash
#!/bin/bash
#SBATCH --job-name=check_spineps212
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=%x_%j.out
# Does the shared environment import for this account? Read-only; safe to resubmit.
export PYTHONNOUSERSITE=1
/rs/rs_grp_oschome/go2432/envs/spineps212/bin/python -c "import nibabel, scipy"
echo "exit=$?"
```

Submit it with
`sbatch -D /rs/rs_grp_oschome/<AccessID>/envs /rs/rs_grp_oschome/<AccessID>/envs/check_spineps212.sbatch`
and read `check_spineps212_<jobid>.out` in the same folder. `exit=0` means the shared environment works for you. A
`PermissionError` or an `ImportError` with a non-zero exit means Greg's step is not done yet: use section 2.
`PYTHONNOUSERSITE=1` keeps a package in your own user site from shadowing the environment
(`../10_data_platform_grid/code/env/README.md`).

## 2. Until then: build your own from `spineps.yml`

`10_data_platform_grid/code/env/` holds four files copied unchanged from the `env/` folder of `spinesurg-ct-nnunet`
(`../10_data_platform_grid/MANIFEST_LOCAL.md` section 2): `spineps.yml` (the CPU environment `spineps`, exported without
build strings), `spineps.lock.txt` (its pip list as it was on 2026-09-18, with torch 2.6.0+cu124 in the header),
`fluorogen.yml` (the GPU environment `fluorogen`, which this page does not build) and `README.md` (the
`PYTHONNOUSERSITE=1` and `python -P` rules). The last line of `spineps.yml` is `prefix:` with Greg's HOME; the `-p` in
the job below overrides it.

First copy the folder to the grid by the route of section 3, from your laptop clone:

```bash
git archive HEAD 10_data_platform_grid/code/env | ssh grid 'tar -x -C /rs/rs_grp_oschome/<AccessID>/envs'
```

The file then sits at `/rs/rs_grp_oschome/<AccessID>/envs/10_data_platform_grid/code/env/spineps.yml`. Save this job
as `/rs/rs_grp_oschome/<AccessID>/envs/build_spineps_env.sbatch`:

```bash
#!/bin/bash
#SBATCH --job-name=build_spineps_env
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
# Build the environment of spineps.yml under your own Ceph folder, as a job, never on the login node.
#   sbatch -D /rs/rs_grp_oschome/$USER/envs /rs/rs_grp_oschome/$USER/envs/build_spineps_env.sbatch
# Safe to resubmit: a requeued or repeated run updates the environment instead of starting over.
set -euo pipefail
export PYTHONNOUSERSITE=1

ENVS=/rs/rs_grp_oschome/$USER/envs
YML=$ENVS/10_data_platform_grid/code/env/spineps.yml
PREFIX=$ENVS/spineps
# package caches on Ceph, not HOME
export CONDA_PKGS_DIRS=$ENVS/conda_pkgs
export PIP_CACHE_DIR=$ENVS/pip_cache

if [ ! -f "$YML" ]; then
  echo "missing $YML: copy 10_data_platform_grid/code/env to $ENVS first"
  exit 1
fi

if [ -x "$HOME/miniforge3/bin/conda" ]; then
  CONDA=$HOME/miniforge3/bin/conda
elif [ -x "$HOME/mambaforge/bin/conda" ]; then
  CONDA=$HOME/mambaforge/bin/conda
else
  echo "installing Miniforge into $HOME/miniforge3"
  curl -sSL -o "$ENVS/Miniforge3-Linux-x86_64.sh" \
    "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
  bash "$ENVS/Miniforge3-Linux-x86_64.sh" -b -u -p "$HOME/miniforge3"
  rm -f "$ENVS/Miniforge3-Linux-x86_64.sh"
  CONDA=$HOME/miniforge3/bin/conda
fi

if [ -d "$PREFIX/conda-meta" ]; then
  echo "updating $PREFIX from $YML"
  "$CONDA" env update -p "$PREFIX" -f "$YML" --prune
else
  echo "creating $PREFIX from $YML"
  "$CONDA" env create -p "$PREFIX" -f "$YML"
fi

"$PREFIX/bin/python" -c "import nibabel, scipy"
echo "ENV_OK $(date) $(sha256sum "$YML")" > "$ENVS/spineps.ENV_OK"
echo "done $(date)"
```

Submit it with
`sbatch -D /rs/rs_grp_oschome/<AccessID>/envs /rs/rs_grp_oschome/<AccessID>/envs/build_spineps_env.sbatch`.
It is done when `/rs/rs_grp_oschome/<AccessID>/envs/spineps.ENV_OK` exists; your interpreter is then
`/rs/rs_grp_oschome/<AccessID>/envs/spineps/bin/python`. Miniforge goes to `~/miniforge3` and an existing
`~/miniforge3` or `~/mambaforge` is reused, as the lab's `templates/make_env.sh` does
(`code/student_projects_3f1cf04/templates/make_env.sh`; `memory/student-onboarding-structure.md`). `reqp --qos=requeue`
can preempt a running job (`CLAUDE.md` "The two open field failures"); resubmit the same file and it carries on.

Not recorded: how long the build takes, how much space it takes (the shared `spineps212` is 10.8 GB, but it is a
different environment), whether `spineps.yml` resolves on a fresh Miniforge (its `README.md` says the export leaves out
build strings so that it resolves on another Linux x86_64 host; no student build is recorded), and a student's HOME
quota. The four hours, 16 GB and four cores of the job are a margin, not a measurement.

## 3. How code reaches the worker

The grid cannot fetch the private repository (`../10_data_platform_grid/CLAUDE.md`; recorded for the grid checkout of
`spinesurg-ct-nnunet`, why fetching stopped is not recorded, `docs/handoff/OPEN_QUESTIONS.md` B32), and whether `git` is
tolerated on warrior is not recorded (OPEN_QUESTIONS E18; issue #19 tests it). Whether a grid clone of `spine-program`
could fetch is not recorded either. So code goes from a clone on your laptop, by archive over ssh, the route that worked
on 2026-10-08 (`docs/handoff/RECIPES.md` section 0 item 2):

```bash
git archive HEAD <paths> | ssh grid 'tar -x -C <dir>'
ssh grid "echo $(git rev-parse HEAD) >> <dir>/SHIPPED_COMMITS.txt"
```

- Run it in the top folder of your clone. `<paths>` are the repository paths your issue needs (for example
  `10_data_platform_grid/code/env`); `<dir>` is a folder under `/rs/rs_grp_oschome/<AccessID>/` that already exists
  (`ssh grid 'mkdir -p <dir>'`), never inside `/rs/rs_grp_oschome/<AccessID>/hpcworker`, whose run directories the
  framework removes (`MANIFEST_GRID.md` section 1).
- `git archive` ships only committed files: an edit you have not committed ships in its committed state, and an
  untracked file does not ship at all. The second line records the commit you shipped, as the recipe does with
  `SHIPPED_COMMITS.txt` (`docs/handoff/RECIPES.md` section 0 item 2).
- `ssh grid` is the host alias of `code/student_projects_3f1cf04/templates/ssh_config` (`grid.wayne.edu` with your
  AccessID and key); the recipes' `wsu-grid` is Greg's alias for the same host.
- The pipe ends in `tar` on the login node. `tar` is one of the commands the Beethoven deploy runs there
  (`MANIFEST_GRID.md` section 1), and the route was tested only for a subfolder: whether `tar` on warrior is tolerated
  for the whole tree is not recorded (`docs/handoff/RECIPES.md` section 0 item 2). Ship the paths you need, not the
  repository.
- Run it in a POSIX shell (Git Bash, WSL, or a macOS or Linux terminal). Windows PowerShell 5.1 re-encodes a pipe
  between two programs as text, which breaks the tar stream.
- A claude.ai Project thread or cloud session has no ssh, so this step runs on a laptop (root `CLAUDE.md` "What a cloud
  session reaches"). What you ship stays private (root `CLAUDE.md` rule 8): ship only what your issue needs.

The Beethoven worker runs as your account on a compute node and reads `<dir>` like any job. How results come back from
the grid is not part of this page.
