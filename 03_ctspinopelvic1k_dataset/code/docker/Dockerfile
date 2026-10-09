# =============================================================================
# spinesurg-ct-nnunet — Training / Evaluation Docker Image
# docker/Dockerfile
#
# Full-featured image for model training, hyperparameter optimisation,
# and TotalSegmentator benchmarking.
#
# Workflow:
#   Local:    scripts/build_and_push.sh    → builds + pushes to Docker Hub
#   Warrior:  containers/build_container.sh → pulls + converts to .sif
#   Runtime:  slurm/nnet_baseline.sh bind-mounts the repo into /workspace;
#             no code is baked into the image.
#
# Base image: pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime
#   CUDA 12.1 had a cuBLAS bug on H200 NVL (SM90) causing
#   CUBLAS_STATUS_EXECUTION_FAILED for FP16/BF16 GEMMs.
#   CUDA 12.4 + cuDNN 9 fully supports H200 tensor core ops including BF16.
#
# Version 2.4.0 bakes in nnunetv2 so slurm/nnet_baseline.sh Stage 0 no longer
# needs a runtime `pip install --user nnunetv2`. This removes the compute-node
# outbound-network dependency and pins the nnU-Net version across all runs.
# =============================================================================
FROM pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime
LABEL maintainer="Gregory Schwing <gregory.schwing@wayne.edu>"
LABEL description="spinesurg-ct-nnunet training image — CT-only, no MRI tools"
LABEL version="2.4.0"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        git wget curl unzip libgomp1 libglib2.0-0 \
        libsm6 libxext6 libxrender-dev libgl1-mesa-glx ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir \
        numpy==1.26.4 scipy==1.13.1 scikit-learn==1.5.1 \
        pandas==2.2.2 matplotlib==3.9.2
RUN pip install --no-cache-dir \
        nibabel==5.2.1 SimpleITK==2.3.1 "monai[all]==1.4.0"
# TotalSegmentator — CT benchmark baseline only, no MRI variant
RUN pip install --no-cache-dir "TotalSegmentator>=2.4.0"
RUN pip install --no-cache-dir "ray[tune,air]==2.33.0" optuna==3.6.1
RUN pip install --no-cache-dir \
        lightning==2.4.0 tensorboard==2.17.1 \
        tqdm==4.66.5 pyyaml==6.0.2 einops==0.8.0
RUN pip install --no-cache-dir medpy==0.5.2
# ANTs Python bindings — required for registration-based sacralization synthesis.
# antspyx bundles the full ANTs library so no separate ANTs install needed.
# cmake + build-essential needed for the C++ compilation step.
RUN apt-get update && apt-get install -y --no-install-recommends \
        cmake build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir antspyx
RUN pip install --no-cache-dir "wandb>=0.12.10" scikit-image==0.24.0
# ── 3D visualization ─────────────────────────────────────────────────────────
RUN pip install --no-cache-dir \
        plotly==5.18.0 \
        kaleido==0.2.1

# ── nnU-Net v2 ────────────────────────────────────────────────────────────────
# Pinned to avoid drift between local build and Warrior runs. Stage 0 of
# slurm/nnet_baseline.sh previously did a runtime `pip install --user nnunetv2`;
# baking it in removes the compute-node outbound-network dependency and
# guarantees the same nnU-Net version across all training jobs.
RUN pip install --no-cache-dir nnunetv2==2.5.1

ENV TOTALSEG_WEIGHTS_PATH=/tmp/totalseg_weights
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/opt/conda/bin:/usr/bin:/bin:${PATH}
RUN mkdir -p ${TOTALSEG_WEIGHTS_PATH}

# =============================================================================
# Registration pipeline tools — added last to maximise layer cache reuse.
# =============================================================================

# dcm2niix via apt-get — clean, always on PATH, no Python import magic needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
        dcm2niix \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && dcm2niix --version || true

# ANTs registration uses the antspyx Python API directly — no CLI binaries
# needed. Smoke-test that both tools are importable/available.
RUN which dcm2niix && python3 -c "import ants; print('antspyx:', ants.__version__)" \
    && echo "Registration tool check: PASS"

# ── Final smoke test: verify baked-in ML stack ────────────────────────────────
RUN python3 -c "import torch, monai, nnunetv2, wandb; \
    from importlib.metadata import version; \
    print(f'torch={torch.__version__} monai={monai.__version__} nnunetv2={version(\"nnunetv2\")} wandb={wandb.__version__}')"

ENTRYPOINT ["/bin/bash"]
