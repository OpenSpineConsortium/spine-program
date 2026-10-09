#!/bin/bash
#SBATCH --job-name=rescore_check
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=1:00:00
#SBATCH --output=logs/%x_%j.out
set -u
BASE=/rs/rs_grp_oschome/go2432/data/or_ready/bodybox_rescore/check
mkdir -p "$BASE/logs"
cd "$BASE"
~/mambaforge/envs/spineps/bin/python "$BASE/rescore_check_verify.py" > "$BASE/verify_out.json"
rc=$?
echo "rc=$rc"
[ $rc -eq 0 ] && echo VERIFY_OK
