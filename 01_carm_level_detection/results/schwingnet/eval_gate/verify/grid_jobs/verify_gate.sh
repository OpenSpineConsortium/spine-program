#!/bin/bash
#SBATCH --job-name=verify_gate
#SBATCH --time=03:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
# VERIFY item 1 (SchwingNet/results/eval_gate/VERIFY.md): call every wired evaluator with patients its checkpoint, or an
# ancestor of it, trained or was selected on. Every G-test must end in an eval_gate exception (SeenInEvaluation,
# UnresolvedLineage, UnkeyedEvalItem, UngatedInput) raised BEFORE scoring, and write no result. C-tests are controls
# that must pass the gate. Nothing here writes into the repo clone.
#
#   sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/verify -p reqp --qos=requeue \
#     --output=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/verify/verify_gate_%j.out verify_gate.sh
set -u
V=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/verify
O=$V/out
L=$V/logs
REPO=$HOME/spinesurg-ct-nnunet
T=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/touched.json
PYD=$HOME/mambaforge/envs/spinedet/bin/python
PYS=$HOME/mambaforge/envs/spineps/bin/python
PYF=$HOME/mambaforge/envs/fluorogen/bin/python
RUNS=$HOME/spine-detector/runs
RX=/rs/rs_grp_oschome/go2432/data/realxray
P=$RUNS/devcorpus/dc_P_pooled/weights/best.pt
A=$RUNS/devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt
B=$RUNS/devcorpus/dc_B_held_surgio_b51_dr_s1/weights/best.pt
LODO=$RUNS/realxray/rx_lodo_carmlspine_1024/weights/best.pt
RXP=$RUNS/realxray/rx_pooled_1024/weights/best.pt
SCALFT=$HOME/model_night/runs/model_scal_pt_ft.pt
OLDSET=/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep
LEAKDUMP=/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__cobra_test.json
mkdir -p "$O" "$L"
cd "$REPO" || exit 3
export MPLBACKEND=Agg
echo "VERIFY_GATE_START host $(hostname) job ${SLURM_JOB_ID:-none} $(date)"
echo "--- md5 of the grid copies (compare with the local checkout)"
md5sum tools/eval_gate.py tools/realxray_eval.py tools/arc_recall_eval.py tools/arc_prior_check.py tools/patient_keys.py \
  tools/leak_check.py tools/case134_sweep.py tools/level_prototype.py tools/head_mixed_length.py tools/learning_embed.py \
  tools/rigor_fixes.py tools/device_fit.py SchwingNet/tools/fig4_pairs_pull.py tools/arc_angle_set.py tools/lcurve_score.py \
  tools/checkpoint_lineage.py tools/count_from_sacrum_eval.py | awk '{print substr($1,1,12), $2}'
echo "--- the COCO root: both yolo11m.pt copies a relative 'model: yolo11m.pt' could have resolved to"
sha256sum $HOME/spine-detector/yolo11m.pt $HOME/spinesurg-ct-nnunet/yolo11m.pt
$PYD - <<'EOF'
import torch, os
for p in ("~/spine-detector/yolo11m.pt", "~/spinesurg-ct-nnunet/yolo11m.pt"):
    ck = torch.load(os.path.expanduser(p), map_location="cpu", weights_only=False)
    ta = ck.get("train_args") or {}
    print(p, "train_args.data =", ta.get("data"), "| model =", ta.get("model"), "| date =", ck.get("date"), "| version =", ck.get("version"))
EOF

$PYS -u $V/verify_setup.py "$V" || exit 4

# t NAME EXPECT(raise|pass) ENV_PY OUTPUT_PATH -- CMD...   (the output path must NOT exist after a raise)
t() {
  local name=$1 expect=$2 out=$3; shift 3
  rm -rf "$out"
  echo "=== $name (expect $expect)"
  echo "+ $*"
  timeout 2400 "$@" > "$L/$name.log" 2>&1
  local rc=$?
  local exc=$(grep -oE "(eval_gate\.)?(SeenInEvaluation|UnresolvedLineage|UnkeyedEvalItem|UngatedInput)" "$L/$name.log" | tail -1)
  local wrote=no; [ -e "$out" ] && wrote=yes
  local verdict_line=$(grep -m1 -E "^eval_gate: .*(HELD OUT|were trained or SELECTED|unresolved link|match no keying|DECLARED)" "$L/$name.log" | cut -c1-400)
  echo "RESULT $name expect=$expect rc=$rc exc=${exc:-none} wrote_output=$wrote"
  echo "   first gate line: $verdict_line"
  tail -3 "$L/$name.log" | cut -c1-300 | sed 's/^/   | /'
}

# ---------------------------------------------------------------- detectors
t G01_realxray_eval_arc17_pooled raise $O/G01.json \
  $PYD -u tools/realxray_eval.py --weights $P --data $V/rx_arc17 --split test --out $O/G01.json
t G02_realxray_eval_ancestor_lodo raise $O/G02.json \
  $PYD -u tools/realxray_eval.py --weights $LODO --data $V/rx_anc --split test --out $O/G02.json
t G03_realxray_eval_selection_lodo_cobra raise $O/G03.json \
  $PYD -u tools/realxray_eval.py --weights $LODO --data $RX/cobra_elekta --split test --out $O/G03.json
t G04_arc_recall_eval_arc17_4arms raise $O/G04 \
  $PYD -u tools/arc_recall_eval.py --set-root $OLDSET --out $O/G04 --weights pooled=$P --weights lodoA=$A --weights lodoB=$B --weights real_lodo=$LODO
t G05_arc_recall_eval_ancestor_lodo raise $O/G05 \
  $PYD -u tools/arc_recall_eval.py --set-root $V/set_anc --out $O/G05 --weights real_lodo=$LODO
t G06_arc_prior_check_arc17_4arms raise $O/G06 \
  $PYD -u tools/arc_prior_check.py --set-root $OLDSET --out $O/G06 --weights pooled=$P --weights lodoA=$A --weights lodoB=$B --weights real_lodo=$LODO
t G07_arc_prior_check_ancestor_lodo raise $O/G07 \
  $PYD -u tools/arc_prior_check.py --set-root $V/set_anc --out $O/G07 --weights real_lodo=$LODO
t G08_arc_angle_set_arc17_4arms raise $O/G08 \
  $PYF -u tools/arc_angle_set.py --pool /nonexistent_pool.json --subjects-file $V/subjects_arc17.txt --out $O/G08 \
  --gate-weights pooled=$P --gate-weights lodoA=$A --gate-weights lodoB=$B --gate-weights real_lodo=$LODO
t G09_arc_angle_set_ancestor_lodo raise $O/G09 \
  $PYF -u tools/arc_angle_set.py --pool /nonexistent_pool.json --subjects-file $V/subjects_anc.txt --out $O/G09 \
  --gate-weights real_lodo=$LODO
# case134_sweep writes its outputs to fixed paths; the result files it would write are checked by mtime below
C134OUT=$(grep -oE '^OR *= *[^#]*' tools/case134_sweep.py | head -1)
echo "case134_sweep output constant: $C134OUT"
t G10_case134_sweep_own_train_rxpooled raise $O/G10.none \
  $PYD -u tools/case134_sweep.py score --weights rx_pooled=$RXP
t G11_case134_sweep_ancestor_synthetic raise $O/G11.none \
  $PYD -u tools/case134_sweep.py score --weights pooled=$P --touched $V/synthetic_touched_case134.json
t G12_level_prototype_arc17_detector raise $O/G12 \
  $PYD -u tools/level_prototype.py --image $V/img_arc17 --out $O/G12 --detector $P --model $SCALFT --head "" --flag \
  --hist-match "" --no-orient --no-rule-flags
t G13_level_prototype_ancestor_detector raise $O/G13 \
  $PYD -u tools/level_prototype.py --image $V/img_anc --out $O/G13 --detector $LODO --model $SCALFT --head "" --flag \
  --hist-match "" --no-orient --no-rule-flags
t G14_level_prototype_ancestor_encoder raise $O/G14 \
  $PYD -u tools/level_prototype.py --image $V/img_ctsp --out $O/G14 --detector $P --model $SCALFT --head "" --flag \
  --hist-match "" --no-orient --no-rule-flags
# ---------------------------------------------------------------- level models
t G15_head_mixed_length_arc17_pooled raise $O/G15 \
  $PYD -u tools/head_mixed_length.py --ctx $V/bank_arc17 --model $P --out $O/G15 --no-register --epochs 1
t G16_head_mixed_length_ancestor_encoder raise $O/G16 \
  $PYD -u tools/head_mixed_length.py --ctx $V/bank_ctsp --model $SCALFT --out $O/G16 --no-register --epochs 1
t G17_learning_embed_ancestor_encoder raise $O/G17/gradcam_summary.json \
  $PYD -u tools/learning_embed.py --bank $V/bank_ctsp --model $SCALFT --keys $V/keys_empty.json --carm "" --cobra "" \
  --hist-match "" --out $O/G17
t G18_rigor_fixes_a5rows_v8_selection raise $O/G18/a5_rows.csv \
  $PYD -u tools/rigor_fixes.py a5-rows --results $O/G18
t G19_rigor_fixes_a3arows_film_detector raise $O/G19/a3a_rows.csv \
  $PYF -u tools/rigor_fixes.py a3a-rows --results $O/G19
t G20_fig4_pairs_pull_no_declaration raise $O/G20/fig4_pairs.json \
  $PYF -u SchwingNet/tools/fig4_pairs_pull.py --out $O/G20
# ---------------------------------------------------------------- scorers that read a dump written before the gate
t G21_lcurve_score_predate_dump_lodo_cobra raise $O/G21.json \
  $PYS -u tools/lcurve_score.py --dump $LEAKDUMP --out $O/G21.json
t G22_count_from_sacrum_predate_dump raise $O/G22.json \
  $PYS -u tools/count_from_sacrum_eval.py --dump $LEAKDUMP --labels $RX/cobra_elekta/labels --out $O/G22.json
# ---------------------------------------------------------------- device cards (no checkpoint: the fold fits)
echo "=== G23 device_fit.fold_gate"
$PYF -u $V/verify_foldgate.py $O/G23_foldgate.json > $L/G23_foldgate.log 2>&1; echo "RESULT G23 rc=$?"; cat $L/G23_foldgate.log | cut -c1-400
# ---------------------------------------------------------------- controls: a genuinely held-out pair must pass
t C01_eval_gate_check_lodo_carm_test pass $O/C01.json \
  $PYS -u tools/eval_gate.py check --ckpt $LODO --image-dir $RX/carmlspine --split test --eval-set carm_test --out $O/C01.json
t C02_realxray_eval_lodo_carm_test pass $O/C02.json \
  $PYD -u tools/realxray_eval.py --weights $LODO --data $RX/carmlspine --split test --out $O/C02.json --imgsz 1024
t C03_arc_recall_eval_gate_only_unseen40 pass $O/C03.none \
  $PYS -c "import sys; sys.path.insert(0,'tools'); import json, eval_gate as EG; s=json.load(open('/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep_unseen/SET_INFO.json'))['subjects']; hs=EG.assert_unseen_all(['TS_'+x for x in s], {'pooled':'$P','lodoA':'$A','lodoB':'$B','real_lodo':'$LODO'}, 'VERIFY C03'); print('C03 held_out', [h['held_out'] for h in hs], [h['n_keys'] for h in hs])"
echo "--- case134_sweep fixed outputs touched by this job? (mtime newer than the job start)"
find /rs/rs_grp_oschome/go2432/data/or_ready/arc -newer $V/verify_setup.py -maxdepth 2 -type f 2>/dev/null | head
echo "VERIFY_GATE_DONE $(date)"
