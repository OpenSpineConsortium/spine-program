#!/bin/bash
#SBATCH --job-name=verify_gate2
#SBATCH --time=01:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
# VERIFY item 1, second pass: tools/learning_embed.py refuses model_scal_pt_ft.pt before its gate (no layer4 on the
# wrapped encoder), so it is called here with the encoder it is run with (allspine_v9 rung 1): once on the real v9 bank
# (its own selection split) with the real keys map, once through a grafted ancestor (synthetic store). Then the keys-map
# measurement (verify_implant_keys.py).
set -u
V=/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/verify
O=$V/out
L=$V/logs
REPO=$HOME/spinesurg-ct-nnunet
PYD=$HOME/mambaforge/envs/spinedet/bin/python
PYS=$HOME/mambaforge/envs/spineps/bin/python
V9=$HOME/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt
mkdir -p "$O" "$L"
cd "$REPO" || exit 3
echo "VERIFY_GATE2_START host $(hostname) job ${SLURM_JOB_ID:-none} $(date)"
$PYS - <<'EOF'
import json
V = "/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/verify"
T = json.load(open("/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/touched.json"))
V9 = "/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt"
R = "/wsu/home/go/go24/go2432/model_night/runs/model_scal_pt_render.pt"
syn = {R: T[R], V9: dict(T[V9], parents=[R], ancestors=[R], train_keys=[], val_keys=[], touched_keys=[], sha=None,
                         _verify="SYNTHETIC: parent grafted to test the ancestor walk")}
json.dump(syn, open(f"{V}/synthetic_touched_v9.json", "w"))
print("ctsp:0001 in model_scal_pt_render train:", "ctsp:0001" in T[R]["train_keys"])
EOF

t() {
  local name=$1 expect=$2 out=$3; shift 3
  rm -rf "$out"
  echo "=== $name (expect $expect)"
  echo "+ $*"
  timeout 2400 "$@" > "$L/$name.log" 2>&1
  local rc=$?
  local exc=$(grep -oE "(eval_gate\.)?(SeenInEvaluation|UnresolvedLineage|UnkeyedEvalItem|UngatedInput)" "$L/$name.log" | tail -1)
  local wrote=no; [ -e "$out" ] && wrote=yes
  echo "RESULT $name expect=$expect rc=$rc exc=${exc:-none} wrote_output=$wrote"
  tail -4 "$L/$name.log" | cut -c1-300 | sed 's/^/   | /'
}
t G17b_learning_embed_v9_selection_split raise $O/G17b/gradcam_summary.json \
  $PYD -u tools/learning_embed.py --bank $HOME/allspine_v9_fov96_ctx --model $V9 --keys $HOME/patient_keys_v9.json \
  --carm "" --cobra "" --hist-match "" --out $O/G17b
t G17c_learning_embed_ancestor_synthetic raise $O/G17c/gradcam_summary.json \
  $PYD -u tools/learning_embed.py --bank $V/bank_ctsp --model $V9 --keys $V/keys_empty.json --carm "" --cobra "" \
  --hist-match "" --out $O/G17c --touched $V/synthetic_touched_v9.json
echo "=== K1 keys-map measurement"
$PYS -u $V/verify_implant_keys.py $O/K1_implant_keys.json > $L/K1_implant_keys.log 2>&1; echo "RESULT K1 rc=$?"
cat $L/K1_implant_keys.log | cut -c1-600
echo "VERIFY_GATE2_DONE $(date)"
