#!/bin/bash
#SBATCH --job-name=gate_closure
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
# CLOSURE of VERIFY.md 1b (three routes past the gate) and a 1c demonstration, on the grid, with the eval_gate/2 code
# STAGED under $CL/code -- beside the grid clone, never over it: tools/eval_gate.py, head_mixed_length.py and
# head_dual.py in ~/spinesurg-ct-nnunet are what the held Figure 6 chain (f6train/f6eval/d1train) will run, and they
# are not touched. Every run writes under $CL/out; nothing under or_ready/arc, or_ready/lodo or results/fig6.
#
#   sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass -p reqp --qos=requeue \
#     --output=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass/closure_repro_%j.out closure_repro.sh
set -u
CL=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/closure/bypass
CODE=$CL/code
O=$CL/out
L=$CL/logs
PYD=$HOME/mambaforge/envs/spinedet/bin/python
RUNS=$HOME/spine-detector/runs
DATA=/rs/rs_grp_oschome/go2432/data
RX=$DATA/realxray
P=$RUNS/devcorpus/dc_P_pooled/weights/best.pt
A=$RUNS/devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt
B=$RUNS/devcorpus/dc_B_held_surgio_b51_dr_s1/weights/best.pt
LODO=$RUNS/realxray/rx_lodo_carmlspine_1024/weights/best.pt
V5Z=$HOME/FluoroCap/detect_v5z_final_best.pt
V9=$HOME/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt
OLDSET=$DATA/devcorpus_arc/anglesweep
NEWSET=$DATA/devcorpus_arc/anglesweep_unseen
VOIDM=$DATA/devcorpus_arc/recall_vs_angle_selection_leaked/matches.json
UNSM=$DATA/or_ready/eval_gate/arc_unseen/matches.json
UNSC=$DATA/or_ready/eval_gate/arc_unseen/recall_vs_angle.json
LEAKDUMP=$DATA/or_ready/lodo/sweeps/lodo_carm__cobra_test.json
mkdir -p "$O" "$L"
cd "$CODE" || exit 3
export CLOSURE_CODE=$CODE MPLBACKEND=Agg
echo "CLOSURE_START host $(hostname) job ${SLURM_JOB_ID:-none} $(date)"
echo "--- md5 of the staged eval_gate/2 code (compare with the local checkout)"
md5sum tools/eval_gate.py tools/patient_keys.py tools/arc_recall_eval.py tools/realxray_eval.py tools/learning_embed.py \
  tools/fig2_occlusion_clean.py tools/fig2_heldout_embed.py tools/lcurve_score.py tools/count_from_sacrum_eval.py \
  $CL/closure_repro.py | awk '{print substr($1,1,12), $2}'
echo "--- the grid clone's eval_gate.py (left as it is for the Figure 6 chain)"
md5sum $HOME/spinesurg-ct-nnunet/tools/eval_gate.py | awk '{print substr($1,1,12), $2}'

# t NAME EXPECT OUTPUT_PATH -- CMD...   EXPECT is an exception name or "pass"; a raise must leave OUTPUT_PATH absent
t() {
  local name=$1 expect=$2 out=$3; shift 3
  rm -rf "$out"
  echo "=== $name (expect $expect)"
  echo "+ $*"
  timeout 3000 "$@" > "$L/$name.log" 2>&1
  local rc=$?
  local exc=$(grep -oE "(eval_gate\.)?(SeenInEvaluation|UnresolvedLineage|UnkeyedEvalItem|UngatedInput|UnverifiedDump)" "$L/$name.log" | tail -1)
  local wrote=no; [ -e "$out" ] && wrote=yes
  local got=pass; [ $rc -ne 0 ] && got=${exc#eval_gate.}; [ $rc -ne 0 ] && [ -z "$exc" ] && got="rc$rc"
  local ok=NO; [ "$got" = "$expect" ] && ok=yes
  [ "$expect" != pass ] && [ "$wrote" = yes ] && ok=NO
  echo "RESULT $name expect=$expect got=$got rc=$rc wrote_output=$wrote ok=$ok"
  grep -m2 -E "^eval_gate: |UnverifiedDump: |SeenInEvaluation: |UnkeyedEvalItem: " "$L/$name.log" | cut -c1-600 | sed 's/^/   gate: /'
  tail -2 "$L/$name.log" | cut -c1-400 | sed 's/^/   | /'
}

# ================================================================ 1b-i  --matches
t R1a_matches_void_curve_under_detect_v5z UnverifiedDump $O/R1a \
  $PYD -u tools/arc_recall_eval.py --set-root $OLDSET --out $O/R1a --weights pooled=$V5Z --matches $VOIDM --boot 200
t R1b_matches_unseen_run_own_weights_no_sha UnverifiedDump $O/R1b \
  $PYD -u tools/arc_recall_eval.py --set-root $NEWSET --out $O/R1b --weights pooled=$P --weights lodoA=$A \
  --weights lodoB=$B --weights real_lodo=$LODO --matches $UNSM --boot 2000
t R1c_matches_unseen_run_declared pass $O/R1c/recall_vs_angle.json \
  $PYD -u tools/arc_recall_eval.py --set-root $NEWSET --out $O/R1c --weights pooled=$P --weights lodoA=$A \
  --weights lodoB=$B --weights real_lodo=$LODO --matches $UNSM --boot 2000 \
  --not-held-out "closure R1c: re-aggregating a matches file written before eval_gate/2 recorded the sha256"
$PYD -c "import json; d=json.load(open('$O/R1c/recall_vs_angle.json')); print('R1c curve eval_gate.held_out =', d['eval_gate']['held_out'], '| reason:', d['eval_gate']['not_held_out_reason'])"
echo "=== R1d build: a bound copy of the unseen run's matches (the control: what eval_gate/2 writes)"
$PYD -u $CL/closure_repro.py bound-matches $UNSM $O/bound_matches.json > $L/R1d_build.log 2>&1; tail -2 $L/R1d_build.log | cut -c1-600
t R1d_i_bound_matches_own_weights pass $O/R1d_i/recall_vs_angle.json \
  $PYD -u tools/arc_recall_eval.py --set-root $NEWSET --out $O/R1d_i --weights pooled=$P --weights lodoA=$A \
  --weights lodoB=$B --weights real_lodo=$LODO --matches $O/bound_matches.json --boot 2000
$PYD -u $CL/closure_repro.py curve-cells $O/R1d_i/recall_vs_angle.json $UNSC $O/R1d_i_cells.json 2>&1 | tail -2 | cut -c1-900
t R1d_ii_bound_matches_under_detect_v5z UnverifiedDump $O/R1d_ii \
  $PYD -u tools/arc_recall_eval.py --set-root $NEWSET --out $O/R1d_ii --weights pooled=$V5Z --matches $O/bound_matches.json --boot 200

# ================================================================ 1b-ii  carry()
echo "=== R2 carry() on real files"
$PYD -u $CL/closure_repro.py carry $O/R2_carry.json > $L/R2_carry.log 2>&1; echo "R2 rc=$?"; grep -E '"check"|CLOSURE_' $L/R2_carry.log | cut -c1-700
t R2_lcurve_score_predate_dump UnverifiedDump $O/R2_lcurve.json \
  $PYD -u tools/lcurve_score.py --dump $LEAKDUMP --out $O/R2_lcurve.json
t R2_count_from_sacrum_predate_dump UnverifiedDump $O/R2_count.json \
  $PYD -u tools/count_from_sacrum_eval.py --dump $LEAKDUMP --labels $RX/cobra_elekta/labels --out $O/R2_count.json
# the control: a dump eval_gate/2 writes today, carried; then its block transplanted
t C_realxray_eval_lodo_carm_test pass $O/C_rx.json \
  $PYD -u tools/realxray_eval.py --weights $LODO --data $RX/carmlspine --split test --out $O/C_rx.json --imgsz 1024 --dump-raw
t C_lcurve_score_on_bound_dump pass $O/C_lcurve.json \
  $PYD -u tools/lcurve_score.py --dump $O/C_rx.json --out $O/C_lcurve.json
$PYD -c "import json; d=json.load(open('$O/C_lcurve.json')); print('C lcurve_score eval_gate.held_out =', d['eval_gate']['held_out'], '| weights_sha256 =', d.get('weights_sha256'))"
echo "=== C transplants of the bound dump's block"
$PYD -u $CL/closure_repro.py transplant $O/C_transplant.json $O/C_rx.json > $L/C_transplant.log 2>&1; echo "C rc=$?"; grep -E '"check"|CLOSURE_' $L/C_transplant.log | cut -c1-700

# ================================================================ 1b-iii  keys used as given
echo "=== R3 keys on the real v9 bank, map and store"
$PYD -u $CL/closure_repro.py keys $O/R3_keys.json > $L/R3_keys.log 2>&1; echo "R3 rc=$?"; grep -E '^\{|"check"|CLOSURE_' $L/R3_keys.log | cut -c1-900
t R3_learning_embed_real_v9_bank_real_map SeenInEvaluation $O/R3_learning/census.json \
  $PYD -u tools/learning_embed.py --bank $HOME/allspine_v9_fov96_ctx --model $V9 --keys $HOME/patient_keys_v9.json \
  --carm "" --cobra "" --out $O/R3_learning
grep -E "in the (TRAIN|VAL) set of" $L/R3_learning_embed_real_v9_bank_real_map.log | cut -c1-300

# ================================================================ 1c  the two Figure 2 evaluators, now gated
t G1c_fig2_occlusion_clean_v9_val SeenInEvaluation $O/G1c_occ/gradcam_summary.json \
  $PYD -u tools/fig2_occlusion_clean.py --bank $HOME/allspine_v9_fov96_ctx --model $V9 --keys $HOME/patient_keys_v9.json \
  --train-keys $CL/v9_keys_snapshot.json --out $O/G1c_occ
t G1c_fig2_heldout_embed_three_l6 pass $O/G1c_heldout/heldout_census.json \
  $PYD -u tools/fig2_heldout_embed.py --model $V9 --root $DATA/rare_class/carmlspine_cbct_drr \
  --bank $HOME/allspine_v9_fov96_ctx --keys $HOME/patient_keys_v9.json --out $O/G1c_heldout
$PYD -c "import json; d=json.load(open('$O/G1c_heldout/heldout_census.json')); g=d['eval_gate']; print('G1c heldout eval_gate.held_out =', g['held_out'], '| keys', g['checks'][0]['eval_keys'], '| overlap', g['overlap'])"

echo "--- nothing written outside $CL by this job (mtime newer than the job's code copy)"
find $DATA/or_ready/arc $DATA/or_ready/lodo $DATA/or_ready/eval_gate/arc_unseen $HOME/spinesurg-ct-nnunet/SchwingNet/results/fig6 \
  -newer $CODE/tools/eval_gate.py -type f 2>/dev/null | head
echo "CLOSURE_DONE $(date)"
