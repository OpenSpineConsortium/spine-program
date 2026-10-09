#!/bin/bash
#SBATCH --job-name=gate_stage
#SBATCH --time=00:20:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
# Stage the eval_gate/2 code BESIDE the grid clone (never over it: the held Figure 6 chain runs the clone's
# tools/eval_gate.py, head_mixed_length.py and head_dual.py). CRLF stripped; SchwingNet/ is the clone's, read only,
# because eval_gate.EVAL_SET_SPECS reads a few result files under it.
#
#   sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass -p reqp --qos=requeue \
#     --output=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass/closure_setup_%j.out closure_setup.sh
set -eu
CL=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass
rm -rf $CL/code && mkdir -p $CL/code $CL/out $CL/logs
tar -xzf $CL/closure_code.tgz -C $CL/code
find $CL/code $CL -maxdepth 3 \( -name "*.py" -o -name "*.sh" \) -print0 | xargs -0 sed -i 's/\r$//'
ln -sfn $HOME/spinesurg-ct-nnunet/SchwingNet $CL/code/SchwingNet
echo "staged: $(ls $CL/code/tools | wc -l) tools files, $(ls $CL/code/tests | wc -l) tests files"
grep -c $'\r' $CL/code/tools/eval_gate.py || true
md5sum $CL/code/tools/eval_gate.py $CL/code/tools/patient_keys.py $HOME/spinesurg-ct-nnunet/tools/eval_gate.py | awk '{print substr($1,1,12), $2}'
echo SETUP_DONE
