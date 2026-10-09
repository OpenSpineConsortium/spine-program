#!/bin/bash
#SBATCH --job-name=chk9cv9
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=03:00:00
#SBATCH --output=chk9cv9_%j.out
#SBATCH --error=chk9cv9_%j.out
# CHK-9 (tools/leak_check.py chk9) re-run over quoted_results.json with the C-ArmLSpine rows moved from the deleted
# allspine_v2_r1 lineage to the allspine_v9 lineage of closure/cv_v9 (EVAL_LEAKS U1 closure). Two runs against the
# same real lineage store (or_ready/eval_gate/touched.json + ondemand/, which holds the sixteen v9-init fold
# encoders and heads that level_prototype.py's gate computed on demand) and the same eval_gate/2 eval_sets.json:
#   before  the repo's quoted_results.json as committed (md5 2f5b1cfd), so the two runs differ by the rows alone
#   after   quoted_results_cv_v9.json (make_quoted_cv_v9.py)
# Code: the STAGED eval_gate/2 tree (closure/bypass/code; tools/leak_check.py md5 229f0db6 = the checkout; the grid
# clone is left alone for the held Figure 6 chain). leak_check's device-card rows read docs/devices from the code
# root, so the staged tree gets a docs link to the grid clone's docs (a link, nothing copied or written there).
# Nothing under or_ready/eval_gate/{touched.json,ondemand,eval_sets.json,chk9} is written.
#   sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/chk9_cv_v9 chk9_cv_v9.sh
set -uo pipefail
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_chk9cv9_${SLURM_JOB_ID:-x}; mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT
H=/wsu/home/go/go24/go2432
EG=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate
CODE=$EG/closure/bypass/code
O=$EG/closure/chk9_cv_v9
PY=$H/mambaforge/envs/spineps/bin/python
echo "CHK9CV9_START $(date) on $(hostname) job ${SLURM_JOB_ID:-none}"
cd "$CODE" || { echo "no staged code at $CODE"; exit 3; }
[ -e docs ] || ln -s "$H/spinesurg-ct-nnunet/docs" docs
echo "--- code"
md5sum tools/leak_check.py tools/eval_gate.py tools/patient_keys.py tools/checkpoint_lineage.py | awk '{print substr($1,1,12), $2}'
grep -m1 '^GATE_VERSION' tools/eval_gate.py
echo "--- store: touched.json $(stat -c %y "$EG/touched.json" | cut -c1-19), $(ls "$EG/ondemand" | wc -l) on-demand files, eval_sets.json $(stat -c %y "$EG/eval_sets.json" | cut -c1-19)"
for k in 0 1 2 3 4; do
  printf "  v9init cv%s encoder in ondemand: %s  head: %s\n" $k \
    "$(grep -l "model_rung_1_ft_cv${k}_v9init_aug2.pt\": {" "$EG"/ondemand/*.json | wc -l)" \
    "$(grep -l "heads_carm/head_cv${k}_v9init.pt\": {" "$EG"/ondemand/*.json | wc -l)"
done
for k in 0 1 2; do
  printf "  v9init cvday%s encoder in ondemand: %s  head: %s\n" $k \
    "$(grep -l "model_rung_1_ft_cvday${k}_v9init_aug2.pt\": {" "$EG"/ondemand/*.json | wc -l)" \
    "$(grep -l "heads_carm/head_cvday${k}_v9init.pt\": {" "$EG"/ondemand/*.json | wc -l)"
done
md5sum "$O/quoted_results_before.json" "$O/quoted_results_cv_v9.json" | awk '{print substr($1,1,12), $2}'
run() { echo "+ $*"; "$@"; rc=$?; echo "  -> exit $rc"; return 0; }
echo "=== BEFORE: quoted_results.json as committed"
run $PY -u tools/leak_check.py chk9 --quoted-results "$O/quoted_results_before.json" --touched "$EG/touched.json" \
    --eval-sets "$EG/eval_sets.json" --out "$O/before" --cap 600
echo "=== AFTER: the C-ArmLSpine rows on the allspine_v9 lineage"
run $PY -u tools/leak_check.py chk9 --quoted-results "$O/quoted_results_cv_v9.json" --touched "$EG/touched.json" \
    --eval-sets "$EG/eval_sets.json" --out "$O/after" --cap 600
echo "=== DIFF"
run $PY -u "$O/chk9_diff.py" "$O/before/chk9_report.json" "$O/after/chk9_report.json" "$O/quoted_results_cv_v9.json" \
    --out "$O/CHK9_DIFF.md" --json "$O/chk9_diff.json"
head -3 "$O/before/CHK9_REPORT.md" | tail -2
head -3 "$O/after/CHK9_REPORT.md" | tail -2
echo "--- nothing written under the store:"
find "$EG/touched.json" "$EG/ondemand" "$EG/eval_sets.json" "$EG/chk9" -newer "$O/chk9_cv_v9.sh" 2>/dev/null | head
echo "CHK9CV9_DONE $(date)"
