#!/bin/bash
#SBATCH --job-name=c134_eg2
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=16
#SBATCH --mem=48G
#SBATCH --time=04:00:00
#SBATCH --output=c134_eg2_%j.out
#SBATCH --error=c134_eg2_%j.out
# Closure item 1, requeued under eval_gate/2 (2026-09-24, resume after the manuscript drive).
# The 07:18 re-score (job 40431371, closure/case134_sweep/) ran the grid clone's tools, which are still eval_gate/1:
# its dump records no weights_sha256, and the render curve it compared against (or_ready/eval_gate/arc_unseen, also
# eval_gate/1) is refused by carry() under eval_gate/2 (MANUSCRIPT_CORRECTIONS.md section 5.4). This job runs the SAME
# score stage with the STAGED eval_gate/2 code (closure/bypass/code: tools/eval_gate.py md5 2b0c9e05..., the same as
# the local checkout; the grid clone is left as it is for the held Figure 6 chain) against the eval_gate/2-bound
# unseen render curve that the bypass job re-aggregated from the unseen run's own predictions
# (closure/bypass/out/R1d_i/recall_vs_angle.json: 1,824 of 1,824 cells equal to the published unseen curve, section 5.1).
#   step 1  the gate alone, per arm, on the 301-frame spin (eval_gate/2 check)
#   step 2  case134_sweep.py score with the same four weights as slurm/case134_export_score.sh; an arm the gate finds
#           SEEN is declared with --not-held-out-role and labelled beside the held-out arms, never silently
# Outputs go to a NEW directory (closure/case134_sweep_eg2); closure/case134_sweep and or_ready/arc/case134_sweep are kept.
# CPU on purpose: the GPU queue belongs to the Figure 6 chain.
#   sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure closure_case134_eg2.sh
set -uo pipefail
export PYTHONNOUSERSITE=1
export TMPDIR=/dev/shm/go2432_c134eg2_${SLURM_JOB_ID:-x}; mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT
H=/wsu/home/go/go24/go2432
CL=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure
CODE=$CL/bypass/code
PYD=$H/mambaforge/envs/spinedet/bin/python
RUNS=$H/spine-detector/runs
SW=/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep
O=$CL/case134_sweep_eg2
RC=$CL/bypass/out/R1d_i/recall_vs_angle.json
mkdir -p "$O"
cd "$CODE" || exit 3
export CLOSURE_CODE=$CODE MPLBACKEND=Agg
declare -A W=(
  [pooled]=$RUNS/devcorpus/dc_P_pooled/weights/best.pt
  [lodoA]=$RUNS/devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt
  [lodoB]=$RUNS/devcorpus/dc_B_held_surgio_b51_dr_s1/weights/best.pt
  [real_lodo]=$RUNS/realxray/rx_lodo_carmlspine_1024/weights/best.pt
)
echo "C134_EG2_START $(date) on $(hostname) job ${SLURM_JOB_ID:-none}"
echo "--- staged code (eval_gate/2) and the grid clone (left alone)"
md5sum tools/case134_sweep.py tools/eval_gate.py tools/patient_keys.py "$RC" | awk '{print substr($1,1,12), $2}'
grep -n "^GATE_VERSION" tools/eval_gate.py $H/spinesurg-ct-nnunet/tools/eval_gate.py
sha256sum "${W[@]}" | awk '{print substr($1,1,12), $2}'
echo "spin frames: $(ls "$SW/images/test" | wc -l)"

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
  why=$("$PYD" - "$O/gate_check_$r.json" <<'PYEOF'
import json, sys
b = json.load(open(sys.argv[1]))
h = b["checks"][0]
print(f"eval_gate: case134 in {', '.join(f'{k} ({n})' for k, n in (h.get('overlap_by') or {}).items())} "
      f"of this detector's lineage; scored beside the held-out arms and labelled, not a held-out number")
PYEOF
)
  echo "DECLARE $r: $why"
  DECL+=(--not-held-out-role "$r=$why")
done
ARGS=()
for r in pooled lodoA lodoB real_lodo; do ARGS+=(--weights "$r=${W[$r]}"); done
"$PYD" -u tools/case134_sweep.py score "${ARGS[@]}" ${DECL[@]+"${DECL[@]}"} --imgsz 1024 --or-dir "$O" --render-curve "$RC"
rc=$?
echo "C134_EG2_SCORE_RC=$rc $(date)"

# what the new dump binds, and whether the real-spin numbers equal the 07:18 run's
"$PYD" - "$O/case134_sweep.json" "$CL/case134_sweep/case134_sweep.json" <<'PYEOF'
import json, sys
new, old = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
eg = new.get("eval_gate", {})
print("EG2 gate_version", eg.get("gate_version"), "held_out", eg.get("held_out"), "overlap", eg.get("overlap"),
      "unresolved", eg.get("unresolved"), "n_checks", eg.get("n_checks"))
print("EG2 weights_sha256", {k: v[:12] for k, v in (new.get("weights_sha256") or {}).items()})
print("EG2 held_out_by_arm", new.get("held_out_by_arm"))
print("EG2 render_curve_source", new.get("render_curve_source"))
print("EG2 render_curve_refused", new.get("render_curve_refused"))
print("EG2 render_curve_eval_gate", new.get("render_curve_eval_gate"))
print("DETECTORS_IDENTICAL_TO_0718_RUN", new.get("detectors") == old.get("detectors"))
PYEOF
echo "C134_EG2_DONE $(date)"
ls -la "$O"
exit $rc
