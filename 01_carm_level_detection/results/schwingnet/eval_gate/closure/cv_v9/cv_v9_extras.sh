#!/bin/bash
#SBATCH --job-name=cv9iextras
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --output=/wsu/home/go/go24/go2432/logs/cv9iextras_%j.out
# CPU: cv_v9_extras.py on both truths (the count-vs-classifier matrix and the paired zero-shot vs fine-tuned reading).
#   sbatch -D ~/logs SchwingNet/results/eval_gate/closure/cv_v9/cv_v9_extras.sh
set -u
export PYTHONNOUSERSITE=1
cd "$HOME/spinesurg-ct-nnunet"
PY=$HOME/mambaforge/envs/fluorogen/bin/python
D=$HOME/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9
echo "CV9I_EXTRAS_START $(date) host=$(hostname)"
RC=0
for TR in pre rep; do
  $PY $D/cv_v9_extras.py --truth $TR --out $D/cv_v9_extras_$TR.json || RC=1
done
echo "CV9I_EXTRAS_DONE rc=$RC $(date)"
exit $RC
