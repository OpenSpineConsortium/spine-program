#!/bin/bash
#SBATCH --job-name=cv9iclosure
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/wsu/home/go/go24/go2432/logs/cv9iclosure_%j.out
# Requeue of the LAST step of collect_cv_v9.sh only (job 40436581 ran every coupler pass, both coupling reports and
# the a4/a7/a9 twins, then closure_cv_v9.py died in min_det_conf on prototype_results.json, a list). Nothing upstream
# is re-run: the coupling_<truth>/ and rigor_<truth>/ outputs of 40436581 are read as they stand.
#   sbatch -D ~/logs SchwingNet/results/eval_gate/closure/cv_v9/closure_only.sh
set -u
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_cv9iclosure_${SLURM_JOB_ID:-local}; mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
cd "$HOME/spinesurg-ct-nnunet"
PY=$HOME/mambaforge/envs/fluorogen/bin/python
D=$HOME/spinesurg-ct-nnunet/SchwingNet/results/eval_gate/closure/cv_v9
echo "CV9I_CLOSURE_START $(date) host=$(hostname) eval_gate_md5=$(md5sum tools/eval_gate.py | cut -c1-8) gate_version=$(grep -m1 '^GATE_VERSION' tools/eval_gate.py)"
for f in $D/coupling_pre/coupling.json $D/coupling_rep/coupling.json $D/rigor_pre/a4.json $D/rigor_rep/a9.json; do
  [ -f "$f" ] || { echo "MISSING $f (collect job 40436581 output)"; exit 2; }
done
$PY SchwingNet/results/eval_gate/closure/cv_v9/closure_cv_v9.py --out $D/cv_v9.json \
    --coupling-pre $D/coupling_pre/coupling.json --coupling-rep $D/coupling_rep/coupling.json 2>&1 | grep -vE "DECLARED NOT HELD OUT" | tail -60
RC=${PIPESTATUS[0]}
ls -la $D/cv_v9.json $D/carmlspine_cv5_v9init_*.json $D/carmlspine_cvday_v9init_*.json 2>&1
echo "CV9I_CLOSURE_DONE rc=$RC $(date)"
exit $RC
