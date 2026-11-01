#!/bin/bash
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=02:00:00
# The level prototype (spinesurg-ct-nnunet L6_Class, the fluorogen env) on every frame of the pan, with the
# reported stack: detector 797de71a, encoder v9 rung 1 aug2 (registry 188f9fcb), head v9 mixed kmax4 seed0.
# The frames are upright, cranial up; the facing is whichever of the two the detector finds more bodies in on
# every tenth frame. No film histogram match: ~/films_drr was pruned, and the frames are FLUX's, not raw DRRs.
# CONF sets the detector's floor (0.35, the reported stack's, unless given); DET names the folder the records go to
# (det); FACING, when given, skips the facing test and uses that side. A low floor keeps every box with its own
# confidence in the record, so the linker can choose its floor afterwards without running the detector again.
set -uo pipefail
OUT=${OUT:?}
CONF=${CONF:-0.35}
DET=${DET:-det}
FL=$HOME/mambaforge/envs/fluorogen/bin/python
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
cd "$HOME/spinesurg-ct-nnunet" || exit 2
STACK=(--detector /wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt
       --model /wsu/home/go/go24/go2432/model_registry/188f9fcbfa3c6de1/model_rung_1_aug2.pt
       --head /wsu/home/go/go24/go2432/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt
       --no-orient --conf "$CONF" --dump-posterior --hist-match ""
       --not-held-out "CNS demo frames rendered from an ENHANCE.PET CT the encoder never saw; not an evaluation")
if [ -z "${FACING:-}" ]; then
"$FL" - "$OUT" <<'PY'
import sys
from pathlib import Path
from PIL import Image, ImageOps
out = Path(sys.argv[1])
for side in ("L", "R"):
    (out / f"test_{side}").mkdir(exist_ok=True)
for k, p in enumerate(sorted((out / "frames").glob("f*.png"))):
    if k % 15 == 0:
        im = Image.open(p)
        im.save(out / "test_L" / p.name)
        ImageOps.mirror(im).save(out / "test_R" / p.name)
PY
for side in L R; do
  "$FL" tools/level_prototype.py --image "$OUT/test_$side/*.png" --out "$OUT/det_test_$side" "${STACK[@]}" > "$OUT/det_test_$side.log" 2>&1
done
SIDE=$("$FL" - "$OUT" <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
n = {s: sum(len(json.load(open(p)).get("vertebrae", [])) for p in (out / f"det_test_{s}").glob("f*.json")) for s in "LR"}
print("L" if n["L"] >= n["R"] else "R")
print(n, file=sys.stderr)
PY
)
else
SIDE=$FACING
fi
echo "facing $SIDE"
FRAMES=$OUT/frames
if [ "$SIDE" = R ]; then
  "$FL" - "$OUT" <<'PY'
import sys
from pathlib import Path
from PIL import Image, ImageOps
out = Path(sys.argv[1]); (out / "frames_R").mkdir(exist_ok=True)
for p in sorted((out / "frames").glob("f*.png")):
    ImageOps.mirror(Image.open(p)).save(out / "frames_R" / p.name)
PY
  FRAMES=$OUT/frames_R
fi
[ -z "${FACING:-}" ] && echo "$SIDE" > "$OUT/facing.txt"
"$FL" tools/level_prototype.py --image "$FRAMES/*.png" --out "$OUT/$DET" "${STACK[@]}" > "$OUT/$DET.log" 2>&1
echo "DET_RC=$?"
ls "$OUT/$DET" | wc -l
