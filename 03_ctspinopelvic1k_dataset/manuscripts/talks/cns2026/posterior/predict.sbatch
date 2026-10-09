#!/bin/bash
# Posterior figure, step 2: five-fold ensemble inference of the released model with the per-voxel softmax saved.
# Same settings as the paper's test-set run (spinopelvic-seg slurm/spine_predict_803_best.sh): Dataset803,
# nnUNetTrainerWandB_500ep_LSTVOversample, nnUNetResEncUNetPlans_100G, 3d_fullres, folds 0-4, checkpoint_best,
# mirroring on, step 0.5; plus --save_probabilities.
#   sbatch --array=0-(N-1) --export=ALL,INPUT=in_rest,NPARTS=N predict.sbatch
#SBATCH --job-name=post_pred
#SBATCH --partition=gmsap
#SBATCH --qos=gpu
#SBATCH --gres=gpu:nvidia_h200:1
#SBATCH --cpus-per-task=12
#SBATCH --mem=192G
#SBATCH --time=12:00:00
#SBATCH --output=/rs/rs_grp_oschome/go2432/cns2026_posterior/logs/pred_%A_%a.out
set -euo pipefail
W=/rs/rs_grp_oschome/go2432/cns2026_posterior
SIF=$HOME/spinesurg-ct-nnunet/containers/spinesurg-ct.sif
SING=$HOME/mambaforge/envs/nextflow/bin/singularity
INPUT=${INPUT:-in_lstv}
NPARTS=${NPARTS:-1}
PART=${SLURM_ARRAY_TASK_ID:-0}
unset LD_LIBRARY_PATH PYTHONPATH
export XDG_RUNTIME_DIR=/dev/shm/${USER}_xdg_${SLURM_JOB_ID}
SHM=/dev/shm/${USER}_pymp_${SLURM_JOB_ID}
mkdir -p "$XDG_RUNTIME_DIR" "$SHM" "$W/pred" "$W/raw_dummy" "$W/pre_dummy"
trap 'rm -rf "$SHM" "$XDG_RUNTIME_DIR"' EXIT
nvidia-smi --query-gpu=name,memory.total --format=csv

NNU=$("$SING" exec "$SIF" python -c "import nnunetv2, os; print(os.path.dirname(nnunetv2.__file__))")
echo "nnunetv2 in container: $NNU"
export SINGULARITYENV_TMPDIR=/pymp_tmp
export SINGULARITYENV_nnUNet_raw=/w/raw_dummy
export SINGULARITYENV_nnUNet_preprocessed=/w/pre_dummy
export SINGULARITYENV_nnUNet_results=/w/model
B=(--nv --bind "$W:/w" --bind "$W/hf_export:/data/hf_export" --bind "$SHM:/pymp_tmp"
   --bind "$W/src/nnunet_wandb_variant.py:$NNU/training/nnUNetTrainer/variants/nnunet_wandb_variant.py")

"$SING" exec "${B[@]}" "$SIF" python -c "
from nnunetv2.utilities.find_class_by_name import recursive_find_python_class
import nnunetv2, os
c = recursive_find_python_class(os.path.join(nnunetv2.__path__[0], 'training', 'nnUNetTrainer'),
                                'nnUNetTrainerWandB_500ep_LSTVOversample', 'nnunetv2.training.nnUNetTrainer')
print('trainer class found:', c)
assert c is not None
"
date
stdbuf -oL -eL "$SING" exec "${B[@]}" "$SIF" nnUNetv2_predict \
  -i "/w/$INPUT" -o /w/pred -d 803 -c 3d_fullres \
  -tr nnUNetTrainerWandB_500ep_LSTVOversample -p nnUNetResEncUNetPlans_100G \
  -f 0 1 2 3 4 -chk checkpoint_best.pth --save_probabilities \
  -num_parts "$NPARTS" -part_id "$PART" -npp 4 -nps 3 --continue_prediction || echo "predict exited $?"
date
echo "outputs: $(ls "$W"/pred/*.nii.gz 2>/dev/null | wc -l) nii, $(ls "$W"/pred/*.npz 2>/dev/null | wc -l) npz"
