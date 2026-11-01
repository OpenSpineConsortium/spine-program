#!/bin/bash
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --time=03:00:00
# The CNS closing video's frames (pan_render.py): the lateral panorama of one ENHANCE.PET CT, FLUX.2 klein-9B's
# zero-shot edit of it in the realism venv, run inside SchwingNet's bookworm container (grid/box.sh) since the
# venv's torch and scipy need a newer glibc than the nodes' CentOS 7, and the pan's 30-fps frames cut from it.
set -uo pipefail
OUT=${OUT:?}
HERE=/rs/rs_grp_oschome/go2432/cns-profile/video
VENV=/rs/rs_grp_oschome/go2432/.cache/realism/venv-1f5da5f96035/bin/python
export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
cd "$HERE" || exit 2
bash "$HOME/SchwingNet/grid/box.sh" "$VENV" "$HERE/pan_render.py" "$OUT" ${SUBJECT:-}
echo "PAN_RC=$?"
