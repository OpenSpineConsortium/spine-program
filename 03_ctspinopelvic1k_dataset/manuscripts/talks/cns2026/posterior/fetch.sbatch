#!/bin/bash
# Posterior figure for the CNS deck, step 1: the released model and the 174 held-out test CTs.
#   model: huggingface.co/OpenSpineConsortium/spinopelvic-seg-checkpoints (public), five folds, checkpoint_best
#   CTs:   the April 2026 export (the naming the Dataset803 imagesTs links expect: NNNN_ct / NNNN_spine_ct /
#          NNNN_pelvic_ct), still served by huggingface.co/datasets/gregoryschwingmdphd/CTSpinoPelvic1K
# Every CT is checked against its test label (shape and affine) before anything is predicted on it.
#SBATCH --job-name=post_fetch
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/rs/rs_grp_oschome/go2432/cns2026_posterior/logs/fetch_%j.out
set -euo pipefail
W=/rs/rs_grp_oschome/go2432/cns2026_posterior
RAW=$HOME/spinesurg-ct-nnunet/nnunet/raw/Dataset803_SpineSurgCTFullMerged
RUN=Dataset803_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres
M=https://huggingface.co/OpenSpineConsortium/spinopelvic-seg-checkpoints/resolve/main
D=https://huggingface.co/datasets/gregoryschwingmdphd/CTSpinoPelvic1K/resolve/main
mkdir -p "$W/model/$RUN" "$W/hf_export/ct"

get() { # url dest
  [ -s "$2" ] && return 0
  curl -sSfL --retry 5 --retry-delay 10 -o "$2.part" "$1" && mv "$2.part" "$2"
}
for f in dataset.json plans.json dataset_fingerprint.json; do get "$M/$RUN/$f" "$W/model/$RUN/$f"; done
for k in 0 1 2 3 4; do
  mkdir -p "$W/model/$RUN/fold_$k"
  get "$M/$RUN/fold_$k/checkpoint_best.pth" "$W/model/$RUN/fold_$k/checkpoint_best.pth"
done
ls -la "$W/model/$RUN" "$W/model/$RUN"/fold_*

n=0
for l in "$RAW"/imagesTs/*_0000.nii.gz; do
  t=$(basename "$(readlink "$l")")
  get "$D/ct/$t" "$W/hf_export/ct/$t"
  n=$((n + 1))
done
echo "CT files requested: $n; present: $(ls "$W"/hf_export/ct/*.nii.gz | wc -l); size $(du -sh "$W/hf_export/ct" | cut -f1)"

# geometry check: each CT against its label (a transposed or foreign CT would still segment, plausibly and wrongly)
"$HOME/mambaforge/envs/spineps/bin/python" - "$RAW" "$W/hf_export/ct" <<'PY'
import os, sys
import nibabel as nib
import numpy as np
raw, ct = sys.argv[1], sys.argv[2]
bad = 0
for f in sorted(os.listdir(os.path.join(raw, "imagesTs"))):
    case = f[: -len("_0000.nii.gz")]
    t = os.path.basename(os.readlink(os.path.join(raw, "imagesTs", f)))
    a, b = nib.load(os.path.join(ct, t)), nib.load(os.path.join(raw, "labelsTs", case + ".nii.gz"))
    ok = a.shape == b.shape and np.allclose(a.affine, b.affine, atol=1e-3)
    if not ok:
        bad += 1
        print("MISMATCH", case, t, a.shape, b.shape)
print("geometry: %d mismatches" % bad)
sys.exit(1 if bad else 0)
PY
