#!/bin/bash
#SBATCH --job-name=c134_close
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=16
#SBATCH --mem=48G
#SBATCH --time=08:00:00
#SBATCH --output=c134_close_%j.out
#SBATCH --error=c134_close_%j.out
# Closure item 1: re-score the case134 real spin (the export is unchanged) against the UNSEEN render curve.
#   step 1  the gate alone, per arm, on the spin (eval_gate.py check): what each detector's lineage says of case134
#   step 2  case134_sweep.py score with the same four weights as slurm/case134_export_score.sh; an arm the gate
#           finds SEEN is declared with --not-held-out-role and labelled beside the held-out arms, never silently
# Outputs go to a NEW directory; or_ready/arc/case134_sweep (the run compared against the void curve) is kept.
# CPU on purpose: the GPU queue belongs to the Figure 6 chain; 301 frames x 4 detectors is minutes of CPU per arm.
set -uo pipefail
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_c134_${SLURM_JOB_ID:-x}; mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT
H=/wsu/home/go/go24/go2432
cd "$H/spinesurg-ct-nnunet"
PYD=$H/mambaforge/envs/spinedet/bin/python
RUNS=$H/spine-detector/runs
SW=/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep
O=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/case134_sweep
RC=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/arc_unseen/recall_vs_angle.json
mkdir -p "$O"
declare -A W=(
  [pooled]=$RUNS/devcorpus/dc_P_pooled/weights/best.pt
  [lodoA]=$RUNS/devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt
  [lodoB]=$RUNS/devcorpus/dc_B_held_surgio_b51_dr_s1/weights/best.pt
  [real_lodo]=$RUNS/realxray/rx_lodo_carmlspine_1024/weights/best.pt
)
echo "C134_CLOSE_START $(date) on $(hostname)"
md5sum tools/case134_sweep.py tools/eval_gate.py tools/patient_keys.py "$RC"
sha256sum "${W[@]}"
ls "$SW/images/test" | wc -l

# step 1: the gate alone, one check per arm so each verdict is its own file
SEEN=()
for r in pooled lodoA lodoB real_lodo; do
  "$PYD" -u tools/eval_gate.py check --ckpt "${W[$r]}" --image-dir "$SW" --split test \
      --eval-set "case134_spin ($SW#test)" --out "$O/gate_check_$r.json"
  rc=$?
  echo "GATE $r rc=$rc"
  [ $rc -eq 1 ] && SEEN+=("$r")
  [ $rc -ne 0 ] && [ $rc -ne 1 ] && { echo "GATE $r could not decide (rc $rc): stopping"; exit $rc; }
done
echo "SEEN_ARMS=${SEEN[*]:-none}"

# step 2: score; a seen arm is declared and labelled, the others stay gated
DECL=()
for r in ${SEEN[@]+"${SEEN[@]}"}; do
  why=$("$PYD" - "$O/gate_check_$r.json" <<'EOF'
import json, sys
b = json.load(open(sys.argv[1]))
h = b["checks"][0]
print(f"eval_gate: case134 in {', '.join(f'{k} ({n})' for k, n in (h.get('overlap_by') or {}).items())} "
      f"of this detector's lineage; scored beside the held-out arms and labelled, not a held-out number")
EOF
)
  echo "DECLARE $r: $why"
  DECL+=(--not-held-out-role "$r=$why")
done
ARGS=()
for r in pooled lodoA lodoB real_lodo; do ARGS+=(--weights "$r=${W[$r]}"); done
"$PYD" -u tools/case134_sweep.py score "${ARGS[@]}" ${DECL[@]+"${DECL[@]}"} --imgsz 1024 --or-dir "$O" --render-curve "$RC"
rc=$?
echo "C134_SCORE_RC=$rc $(date)"
exit $rc
