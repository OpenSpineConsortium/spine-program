#!/bin/bash
#SBATCH --job-name=gate_evalsets
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
# eval_sets.json regenerated under eval_gate/2 (every key resolved to a person; arc_unseen from the rendered set),
# with the STAGED code, written beside the old file and diffed against it. The old file stays where CHK-9 reads it.
#
#   sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass -p reqp --qos=requeue \
#     --output=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass/closure_evalsets_%j.out closure_evalsets.sh
set -u
CL=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass
CODE=$CL/code
PYD=$HOME/mambaforge/envs/spinedet/bin/python
OLD=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/eval_sets.json
cd "$CODE" || exit 3
export CLOSURE_CODE=$CODE
echo "EVALSETS_START host $(hostname) job ${SLURM_JOB_ID:-none} $(date)"
md5sum tools/eval_gate.py tools/patient_keys.py | awk '{print substr($1,1,12), $2}'
$PYD -u tools/eval_gate.py eval-sets --out $CL/eval_sets.json
echo "eval-sets rc=$?"
$PYD -u $CL/closure_repro.py eval-sets-diff $OLD $CL/eval_sets.json $CL/out/eval_sets_diff.json
echo "EVALSETS_DONE $(date)"
