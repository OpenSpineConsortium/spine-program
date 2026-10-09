#!/bin/bash
#SBATCH --job-name=gate_samefile
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
# Compare the pre-gate headline dump with the eval_gate/2 re-score of the same frames by the same path (closure_samefile.py).
set -eu
CL=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass
$HOME/mambaforge/envs/spinedet/bin/python -u $CL/closure_samefile.py /rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json $CL/out/C_rx.json $CL/out/samefile_lodo_carm.json
echo SAMEFILE_DONE
