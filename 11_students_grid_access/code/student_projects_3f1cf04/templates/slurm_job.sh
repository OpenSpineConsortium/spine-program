#!/usr/bin/env bash
# copy record: source OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path templates/slurm_job.sh; copied 2026-10-08 into spine-program/11_students_grid_access; redactions: none
#SBATCH --job-name=osc_measure
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
# =============================================================================
# slurm_job.sh — run one Python script over the dataset on the WSU grid.
#
#   mkdir -p logs
#   sbatch templates/slurm_job.sh projects/<you>/measure_something.py --workers 8
#
# What each line above means: CPU work goes to the `reqp` partition with the `requeue` QOS
# (if sbatch refuses that QOS on your account, tell your lead; `-q primary` is the fallback);
# --no-requeue because this script is not written to be restarted halfway; one node, one task,
# eight CPUs (match the --workers of your script); 32 GB of memory; two hours of wall time;
# stdout and stderr go to logs/ named by job name and job id, relative to the directory you
# submit from. Ask for what you need, not more: shorter and smaller jobs start sooner.
#
# Why `set -u` and not `set -e`: with -e the job dies at the first non-zero status without
# saying which step failed, and a job that died silently looks like a job that never ran.
# The checks below say what they refused. (RECIPE.md §4 and §5.)
# =============================================================================
set -uo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"

# Scratch lives in memory under /dev/shm, never /tmp: node-local /tmp is swept by a cleaner
# while jobs run. It is removed when the job ends, however it ends.
W=/dev/shm/${USER}_osc_${SLURM_JOB_ID:-local}
mkdir -p "$W" || { echo "REFUSING: cannot create scratch $W"; exit 1; }
trap 'rm -rf "$W"' EXIT
export TMPDIR="$W" PYTHONNOUSERSITE=1 OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"

# Refuse early: the script must exist, and the environment must activate.
SCRIPT="${1:?usage: sbatch templates/slurm_job.sh <script.py> [args]}"
[ -s "$SCRIPT" ] || { echo "REFUSING: $SCRIPT is missing or empty"; exit 1; }
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then source "$HOME/miniforge3/etc/profile.d/conda.sh";
elif [ -f "$HOME/mambaforge/etc/profile.d/conda.sh" ]; then source "$HOME/mambaforge/etc/profile.d/conda.sh";
else echo "REFUSING: no conda.sh under ~/miniforge3 or ~/mambaforge (run templates/make_env.sh first)"; exit 1; fi
conda activate osc || { echo "REFUSING: conda environment 'osc' does not activate"; exit 1; }

echo "job ${SLURM_JOB_ID:-local} on $(hostname), $(date), commit $(git rev-parse --short HEAD 2>/dev/null || echo none)"
echo "running: python $*"
python "$@"
rc=$?
echo "finished $(date) rc=$rc"
exit $rc
