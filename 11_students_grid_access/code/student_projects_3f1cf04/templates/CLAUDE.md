<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path templates/CLAUDE.md. Copied 2026-10-08. Redactions applied by kind: none. Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# CLAUDE.md — how this project works. Read before doing anything.

Copy this file into your project folder (`projects/<lastname>_<topic>/CLAUDE.md`) and edit
the lines marked **EDIT**. Claude Code reads it at the start of every session, so nothing
here has to be repeated. It encodes the working setup the consortium lead uses day to day:
Claude on the laptop, driving the WSU grid over SSH, with every heavy job submitted to
SLURM and nothing run on the login node.

## Who I am

I am a student on an OpenSpineConsortium project. I am learning to code. Explain what a
command does in one line before running it, prefer small readable scripts, and tell me
when you are unsure. The question and plan are in `proposal.md` in this folder; `JOURNAL.md`
is the running log.

## The two machines

**Laptop** (where Claude Code runs, inside VS Code). On Windows, Claude's shell is Git Bash,
and anything that touches the network (`ssh`, `scp`, `rsync`, `git push`, Hugging Face
downloads) is run through WSL: `wsl -e bash -lc '<command>'`. On macOS and Linux the terminal
is used directly.

**Grid** (WSU HPC, host `grid.wayne.edu`, login node `warrior`, SLURM). Reached as `ssh grid`
thanks to `~/.ssh/config` (see `templates/ssh_config`). My AccessID: **EDIT: youraccessid**.
My clone of this repository on the grid: `~/Student_Projects`. My copy of the dataset on the
grid: **EDIT: ~/data/CTSpinoPelvic1K** (the folder holding `labels/`, `manifest.json`,
`dataset_labels.json`; ask the lead whether a shared copy exists before downloading 195 GB
of CT; `templates/get_dataset.sh` fetches the labels as a job). Python on the grid:
Miniforge in `~/miniforge3` (the lead's older install is `~/mambaforge`; check both) with an
environment named `osc` built from `templates/environment.yml` by `templates/make_env.sh`.
Containers: `module load singularity` (3.5.2).
Nextflow is available in `~/.local/bin` for pipelines but is not needed for a first project.

## Rules that never bend

- **Nothing heavy on the login node.** Anything over a minute or over a few GB of memory is
  a SLURM job. A quick `ls`, `squeue`, `tail` or `git pull` over SSH is fine.
- **Job scripts are files, never heredocs.** Every attempt to push a script through
  `wsl -> ssh -> heredoc`, or to pass a multi-argument command through `sbatch --wrap` over
  SSH, has been mangled by quoting (variables expanded on the wrong machine, backslashes
  eaten, commands split). Write the job script to a file in the repo with the editor, commit
  it, `git pull` on the grid, then `sbatch` it there. One layer of quoting, no surprises.
- **Claude drafts, I submit.** Show me the job script; I run `sbatch` (or I say "submit it"
  and you run exactly `ssh grid "cd ~/Student_Projects && sbatch <script>"`). Never submit a
  job I have not seen.
- **Never reorient a volume.** Read with `np.asanyarray(img.dataobj)`, write with the same
  affine and header. Find axes from `nib.aff2axcodes(img.affine)`; volumes are stored P,I,R
  and nothing may assume otherwise.
- **Never commit imaging data** (`*.nii.gz`, `*.dcm`, `*.zip`); `.gitignore` blocks it.
- **Never edit a result by hand.** Wrong number: fix the script, rerun, commit the new file.
- **Read `dataset_labels.json` for identifiers**; never type them from memory. For
  reference (v10): vertebrae 1–25 (L1–L6 = 20–25), sacrum 26, S1 29, hips 30–31, femora
  32–33, ribs 34–46 left and 47–59 right (46 and 59 are rib 13, empty), lumbar ribs 60–61,
  hardware 62–68.
- **Read `KNOWN_ISSUES.md`** before an analysis: a null Castellvi grade means ungraded;
  exclude the 11 hardware records from gap measurements; never pool prone and supine for
  postural angles; nine four-lumbar records carry the transitional segment as S1.

## The remote workflow, step by step

Code moves through git; data stays on the grid; results come back small.

1. **Edit locally, commit, push.** `projects/` is its own private git repository inside
   the public one, so run git there: `cd projects && git add <files> && git commit -m "<what and why>" && git push`
   (on Windows through `wsl -e bash -lc '...'` if plain git push fails).
2. **Sync the grid clone.** `ssh -o BatchMode=yes grid "cd ~/Student_Projects && git pull -q && cd projects && git pull -q"`
   (`tools/grid.sh sync` does both).
3. **Submit from the repo root on the grid**, so `SLURM_SUBMIT_DIR` is the repo:
   `ssh -o BatchMode=yes grid "cd ~/Student_Projects && mkdir -p logs && sbatch templates/slurm_job.sh projects/<me>/measure.py --data ~/data/CTSpinoPelvic1K --out projects/<me>/results --workers 8"`.
   `sbatch` prints `Submitted batch job <id>`; record the id in `JOURNAL.md`.
4. **Poll in the background, not by hand.** Run a background loop that checks
   `ssh -o BatchMode=yes grid "squeue -j <id> -h -o %T"` every 30–60 s and stops when it
   returns nothing, then prints the last 40 lines of `logs/<name>_<id>.out` and `.err`.
   `tools/grid.sh wait <id>` does exactly this. Do not poll in the foreground for more
   than a couple of minutes; start the loop as a background command and do other work.
5. **Read the log, then the accounting.** `sacct -j <id> --format=JobID,State,Elapsed,MaxRSS`
   tells us whether the memory and time requests were right; adjust the `#SBATCH` lines
   for next time.
6. **Bring results back.** `wsl -e bash -lc 'rsync -avz grid:~/Student_Projects/projects/<me>/results/ <local repo>/projects/<me>/results/'`.
   Or commit the small CSVs on the grid and `git pull` locally. Never rsync data volumes.
7. **Look at every figure** before believing it (`Read` the PNG), and check a number in the
   report against the CSV it came from.

`tools/grid.sh` wraps the common calls: `run "<cmd>"`, `sync`, `submit <script> [args]`,
`wait <jobid>`, `pull <remote path> <local path>`. The `/grid-status`, `/grid-submit` and
`/grid-pull` commands in `.claude/commands/` call it.

## SLURM defaults on this grid

- CPU work: `#SBATCH --partition=reqp --qos=requeue --no-requeue`, `--nodes=1 --ntasks=1`,
  `--cpus-per-task=8` (match the script's `--workers`), `--mem=32G`, `--time=02:00:00`,
  `--output=logs/%x_%j.out`, `--error=logs/%x_%j.err`. Ask for what a job needs, not more;
  small jobs start sooner. If `sbatch` refuses the `requeue` QOS on your account, tell your
  lead; `-q primary` is the fallback.
- GPU work (training or inference): `#SBATCH --partition=gmsap,gvohp,galhp --qos=gpu
  --gres=gpu:1`, `--mem=64G`. The GPU partitions accept only the `gpu` QOS. Arrays as
  `--array=0-7%8`; mail on end and failure with
  `--mail-type=END,FAIL --mail-user=<accessid>@wayne.edu`.
- Start every job script with `set -uo pipefail` (not `-e`: a job must reach its own checks
  and say which one failed), `cd "${SLURM_SUBMIT_DIR:-$PWD}"`, then check that every input
  exists and is non-empty before doing anything, then activate the environment
  (`source ~/mambaforge/etc/profile.d/conda.sh && conda activate osc`) or run singularity
  (`$HOME/mambaforge/envs/nextflow/bin/singularity exec --bind "$(pwd)":/w --pwd /w <image>.sif`).
- Scratch is `/dev/shm/${USER}_${SLURM_JOB_ID}`, never `/tmp`: node-local `/tmp` is swept
  by a cleaner while jobs run, and it has taken multiprocessing sockets out from under
  18-hour runs. Make it, export `TMPDIR` to it, and `trap` its removal on exit. Write final
  outputs to the project folder.
- Chain jobs with `--dependency=afterany:<id>`, never `afterok`; the child checks the
  parent's output file itself. `afterok` strands the whole chain when the parent exits
  non-zero for a trivial reason.
- Large outputs belong on the lab's shared volume, not in a home directory; ask your lead
  for the path. The full set of grid rules, each with the incident behind it, is
  `RECIPE.md` §5.
- An 802-record pass that reads every label volume takes 10–15 minutes on 8 CPUs; one
  that reads every CT volume takes hours, so start with `--limit 10` while developing.

## Laptop pitfalls (Windows especially)

- Backslashes in heredocs and `python -c` strings get mangled by the shell; write any
  script longer than one line to a file with the editor and run the file.
- A PDF, PNG or docx open in a viewer cannot be overwritten; the build then silently keeps
  the stale file. Close viewers before rebuilding, and check the log for "can't write".
- Paths under OneDrive contain spaces; always quote them.
- PowerShell 5.1 has no `&&`; use Git Bash or WSL for chained commands.
- Long-running local work (an 802-volume pass) goes in a background command with a polling
  loop, exactly like a grid job.

## How I want to work

- One script per output, named for what it makes; `--help` explains its options; it runs
  from the repository root; it prints what it wrote.
- Ten records first (`--limit 10`), then all 802.
- Every figure has a caption in the script's docstring and a PNG in `figures/`.
- Every number in a write-up was written to `results/` by a script.
- A dated line in `JOURNAL.md` whenever something worked, failed or was decided.
- Commit small and often, with messages that say what changed and why.

## Session start

At the start of a session, in this order: `git status` locally; confirm the grid answers
(`ssh -o BatchMode=yes grid hostname` prints `warrior`); `squeue -u $USER` on the grid to
see whether anything is still running; `git pull` on the grid if I pushed; then read the
last five lines of `JOURNAL.md` and ask me what we are doing today.
