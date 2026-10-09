#!/usr/bin/env bash
# copy record: source OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path templates/get_dataset.sh; copied 2026-10-08 into spine-program/11_students_grid_access; redactions: none
#SBATCH --job-name=osc_get_dataset
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=06:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
# =============================================================================
# get_dataset.sh — fetch CTSpinoPelvic1K into ~/data/CTSpinoPelvic1K, as a job.
#
#   cd ~/Student_Projects && mkdir -p logs && sbatch templates/get_dataset.sh
#   CT=1 sbatch templates/get_dataset.sh        # also the 195 GB of CT volumes
#
# Labels, manifest, label dictionary, splits and KNOWN_ISSUES come from the public Hugging
# Face mirror (1.1 GB). The Zenodo record (10.5281/zenodo.22642578) is the archive of
# record and is what you cite. Ask your mentor first whether a shared copy exists on the
# grid; if so, use its path and skip this.
# =============================================================================
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
DEST="${DEST:-$HOME/data/CTSpinoPelvic1K}"
mkdir -p "$DEST"
if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then source "$HOME/miniforge3/etc/profile.d/conda.sh";
else source "$HOME/mambaforge/etc/profile.d/conda.sh"; fi
conda activate osc

python - "$DEST" "${CT:-0}" <<'PY'
import sys
from huggingface_hub import snapshot_download
dest, ct = sys.argv[1], sys.argv[2] == "1"
patterns = ["labels/*", "manifest.json", "manifest.csv", "dataset_labels.json", "splits_5fold.json",
            "KNOWN_ISSUES.md", "README.md", "LICENSE", "dataset_interface.py", "*.csv", "*.json"]
if ct:
    patterns.append("ct/*")
snapshot_download("OpenSpineConsortium/CTSpinoPelvic1K", repo_type="dataset",
                  local_dir=dest, allow_patterns=patterns)
print("downloaded to", dest)
PY
echo "labels: $(ls "$DEST/labels" | wc -l)   ct: $(ls "$DEST/ct" 2>/dev/null | wc -l)"
echo "done $(date)"
