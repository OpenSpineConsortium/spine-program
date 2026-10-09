#!/bin/bash
#SBATCH --job-name=gate_install
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
# Put the eval_sets.json regenerated under eval_gate/2 where leak_check CHK-9 reads it, after checking that its keys
# equal the old file's set for set (closure_evalsets.sh wrote the diff). The eval_gate/1 file is kept beside it.
#
#   sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass -p reqp --qos=requeue \
#     --output=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass/closure_install_%j.out closure_install.sh
set -eu
CL=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass
G=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate
PYD=$HOME/mambaforge/envs/spinedet/bin/python
$PYD - <<EOF
import json, sys
d = json.load(open("$CL/out/eval_sets_diff.json"))
bad = {k: v for k, v in d["sets"].items() if v.get("n_only_old") or v.get("n_only_new") or v.get("new_unkeyed")}
print("sets:", len(d["sets"]), "changed or unkeyed:", bad or "none", "| new failed:", d["new"]["failed"])
sys.exit(1 if bad or d["new"]["failed"] else 0)
EOF
[ -f $G/eval_sets.eval_gate1.json ] || cp -p $G/eval_sets.json $G/eval_sets.eval_gate1.json
cp $CL/eval_sets.json $G/eval_sets.json.tmp && mv $G/eval_sets.json.tmp $G/eval_sets.json
md5sum $G/eval_sets.json $G/eval_sets.eval_gate1.json $CL/eval_sets.json | awk '{print substr($1,1,12), $2}'
echo INSTALL_DONE
