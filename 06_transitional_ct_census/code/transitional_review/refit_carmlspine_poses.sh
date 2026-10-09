#!/bin/bash
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/refit_carmlspine_poses.sh; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
#SBATCH --job-name=carmpose150
#SBATCH --partition=gvohp,galhp,gmsap
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=04:00:00
#SBATCH --array=0-11
#SBATCH --output=/wsu/home/go/go24/go2432/model_night/logs/carmpose150_%A_%a.out
#
# refit_carmlspine_poses.sh -- re-fit every C-ArmLSpine spot-frame pose at the TRUE detector pitch, into a NEW directory.
#
# PURPOSE. Every pose under /rs/rs_grp_oschome/go2432/data/carmlspine/pose/ (299 *_ref.json, 150 *_ref2.json) was fit
# with px_mm = 300 / 2048 = 0.146484375 mm, the nominal "30cm" panel. tools/carmlspine_io.DET_MM now reads 307.2 mm
# (iRay Jupi1212X, 2048 x 150 um), so tools/carmlspine_pose.py register_frame computes px = DET_MM / cols = 0.150 mm
# and fx = SID / px = 7600 px instead of 7782.4. PREREG_rules.md section 6: "poses are refit at 0.150 before any
# matrix is exported". This script is that refit. It writes to pose_150/ and never touches pose/.
#
# INPUTS  (read only)
#   $D/pose/consensus.json                      the device convention (dir / in-plane rotation / mirror per view class);
#                                               pitch-independent, so it is copied, not recomputed
#   $D/nifti/<case>_cbct.nii.gz, $D/unpacked/C-ArmLSpine/<case>/  (carmlspine_pose.volume / frames)
# OUTPUTS (new)
#   $D/pose_150/<case>_<AP|LAT|LAT2|OBL>_ref.json + .png     free refine from the consensus convention (all views)
#   $D/pose_150/<case>_<LAT|LAT2|OBL>_ref2.json + .png       the bounded refine the laterals use (5/5/25 mm, 6 deg),
#                                                            exactly as slurm/carmlspine_repair_pose.sh step 3
#   $D/pose_150/consensus.json                               copy of the old consensus
#   $D/pose_150/refit_check_<shard>.txt                      per shard: every JSON written has px_mm 0.15 and fx 7600
#
# HOW TO RUN (NOT submitted by the tool that wrote this; Greg submits):
#   ssh grid; cd ~/spinesurg-ct-nnunet
#   mkdir -p /rs/rs_grp_oschome/go2432/data/carmlspine/pose_150
#   cp -n /rs/rs_grp_oschome/go2432/data/carmlspine/pose/consensus.json /rs/rs_grp_oschome/go2432/data/carmlspine/pose_150/
#   sbatch -D /rs/rs_grp_oschome/go2432/data/carmlspine/pose_150 tools/transitional_review/refit_carmlspine_poses.sh
#   (12 shards over 149 cases; --skip-done makes a re-submit resume. To refit a subset: --export=ALL,CASES=case42+case121.)
#
# ESTIMATE. About 450 refines (297 _ref + ~150 _ref2), each one start x (30 coarse + 120/80/50 iterations) on a
# 409-px working grid plus two reads of a 99 MB CBCT: roughly 1 min per frame on one GPU, so ~40 min per shard of
# 12-13 cases; --time is 4 h for margin. Check the CARMPOSE150_DONE line and refit_check_*.txt yourself; do not
# chain anything on afterok.
#
# WHAT CHANGES DOWNSTREAM. carmlspine_pose.py's `refine` reads $OUT/consensus.json and writes only <case>_<view><tag>.json
# and .png. tools/transitional_review/pose_to_viewer.py defaults to --pose-dir pose_150 and clears its needs_refit flag
# only when the JSON's px_mm equals the true pitch. The realxray meta / boxes (tools/carmlspine_labels.py, best_pose)
# still read pose/ and are NOT rebuilt here.
set -uo pipefail
export PYTHONNOUSERSITE=1 TMPDIR=/rs/rs_grp_oschome/go2432/tmp
cd "$HOME/spinesurg-ct-nnunet"
D=/rs/rs_grp_oschome/go2432/data/carmlspine
OUT=$D/pose_150
PY=$HOME/mambaforge/envs/fluorogen/bin/python
"$PY" -c "import pydicom, torch" 2>/dev/null || PY=$HOME/mambaforge/envs/spineps/bin/python
SHARD=${SLURM_ARRAY_TASK_ID:-0}; NSH=${SLURM_ARRAY_TASK_COUNT:-1}
C=""; [ -n "${CASES:-}" ] && C="--cases $(echo "$CASES" | tr + ,)"

mkdir -p "$OUT"
# the pitch the code will fit with: refuse to run if DET_MM is not the 307.2 mm this refit exists for
"$PY" - <<'EOF' || { echo "DET_MM is not 307.2: refusing"; exit 3; }
import sys; sys.path.insert(0, "tools")
import carmlspine_io as C
assert abs(C.DET_MM - 307.2) < 1e-9, C.DET_MM
print("DET_MM", C.DET_MM, "-> px", C.DET_MM / 2048)
EOF
# the device convention is pitch-independent: copied once (no clobber), never recomputed here
[ -f "$OUT/consensus.json" ] || cp -n "$D/pose/consensus.json" "$OUT/consensus.json"
[ -f "$OUT/consensus.json" ] || { echo "no consensus.json to refine from"; exit 4; }

# 1. free refine of every spot frame from the consensus convention (AP, LAT, LAT2 repeats, OBL from the AP convention)
"$PY" -u tools/carmlspine_pose.py refine $C --shard "$SHARD" --n-shards "$NSH" --out "$OUT" --skip-done --tag _ref --views AP,LAT,OBL \
    2>&1 | grep --line-buffered -viE "warn|deprecat"

# 2. the bounded refine the laterals use (5/5/25 mm in camera x/y/z, 6 deg around the header geometry), tag _ref2
"$PY" -u tools/carmlspine_pose.py refine $C --shard "$SHARD" --n-shards "$NSH" --out "$OUT" --skip-done --tag _ref2 --bounds 5,5,25,6 --views LAT,OBL \
    2>&1 | grep --line-buffered -viE "warn|deprecat"

# 3. check what this shard wrote: every JSON must carry px_mm 0.15 and |fx| = SID / 0.15 = 7600 (a 0.1465-mm file here is a defect)
"$PY" - "$OUT" "$SHARD" <<'EOF'
import glob, json, os, sys
out, shard = sys.argv[1], sys.argv[2]
bad, n = [], 0
for p in sorted(glob.glob(os.path.join(out, "case*_ref*.json"))):
    r = json.load(open(p)); n += 1
    fx = abs(r["K"][0][0]); px = r.get("px_mm")
    if px is None or abs(px - 0.15) > 1e-9 or abs(fx - r["sid"] / 0.15) > 1e-3:
        bad.append((os.path.basename(p), px, fx))
with open(os.path.join(out, f"refit_check_{shard}.txt"), "w") as fh:
    fh.write(f"json files in {out}: {n}; wrong pitch: {len(bad)}\n")
    for b in bad:
        fh.write(f"BAD {b}\n")
print(f"refit check: {n} json, {len(bad)} with a wrong pitch")
EOF
echo CARMPOSE150_DONE
