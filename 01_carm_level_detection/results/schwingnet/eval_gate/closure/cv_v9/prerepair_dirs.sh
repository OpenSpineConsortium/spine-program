#!/bin/bash
#SBATCH --job-name=cv9iprerep
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/wsu/home/go/go24/go2432/logs/cv9iprerep_%j.out
# CPU: regenerate the pre-repair k-vertebra crops and mirror the shipped CV fold directories onto the pre-repair export
# (prerepair_fold_dirs.py explains why). Data only; no checkpoint is loaded.
#   sbatch -D ~/logs SchwingNet/results/eval_gate/closure/cv_v9/prerepair_dirs.sh
set -u
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_cv9iprerep_${SLURM_JOB_ID:-local}; mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
cd "$HOME/spinesurg-ct-nnunet"
PY=$HOME/mambaforge/envs/fluorogen/bin/python
echo "CV9I_PREREP_START $(date) host=$(hostname)"
$PY -u SchwingNet/results/eval_gate/closure/cv_v9/prerepair_fold_dirs.py --python $PY
RC=$?
echo "CV9I_PREREP_DONE rc=$RC $(date)"
exit $RC
