# Environments

Everything in this line of work runs in two conda environments on the Wayne State grid
(`go2432@grid.wayne.edu`, CentOS Linux 7, conda 23.1.0, SLURM). Their exact package lists are exported
here without build strings so they resolve on another Linux x86_64 host.

| environment | file | used by |
|---|---|---|
| `spineps` | `env/spineps.yml` | every CPU tool: manifest, geometry, source quality, bank building, figures, tests |
| `fluorogen` | `env/fluorogen.yml` | every GPU tool: encoder and head training, evaluators, SDXL LoRA training and generation |

Recreate them:

```bash
conda env create -n spineps   -f env/spineps.yml
conda env create -n fluorogen -f env/fluorogen.yml
```

Then verify (this is what `tools/audit.sh` runs):

```bash
~/mambaforge/envs/spineps/bin/python   -c "import numpy, scipy, nibabel, openpyxl, PIL, matplotlib, sklearn; print('spineps ok')"
~/mambaforge/envs/fluorogen/bin/python -c "import torch, diffusers, accelerate, peft; print(torch.__version__, diffusers.__version__)"
```

## Things the YAML cannot carry

- **GPU driver.** The `fluorogen` env pins a CUDA-enabled PyTorch; the node's NVIDIA driver must satisfy
  it. On this grid the GPU partitions are `gvohp` (Tesla) and `galhp` (L40S); login nodes have no driver.
- **Model weights.** SDXL base (`stabilityai/stable-diffusion-xl-base-1.0`), the Canny ControlNet
  (`diffusers/controlnet-canny-sdxl-1.0`) and the fp16 VAE (`madebyollin/sdxl-vae-fp16-fix`) live in
  `~/.cache/huggingface/hub`; jobs run with `HF_HUB_OFFLINE=1`, so fetch them once with
  `tools/night_fetch_weights.py` (or `huggingface-cli download`) before the first GPU job.
- **TeX.** The manuscript builds with `module load texlive/2020` then `paper/rsnai/build.sh`.
- **Credentialed data.** VinDr-SpineXR (PhysioNet DUA), AASCE (SpineWeb form) and the IEEE lateral set
  are not fetchable by a script; `slurm/reproduce_all.sh` reports them absent rather than faking them.
- **Scratch.** `/tmp` on compute nodes is swept; every job sets `TMPDIR=$HOME/tmp`.

## Determinism

Every stochastic step takes `--seed 0`. Evaluation-only stages are bit-reproducible given the same
weights (their sha256 is in `LEDGER.tsv`); training-derived numbers can move in the third decimal across
GPU kernels. `PYTHONNOUSERSITE=1` is exported in every job so a user-site package cannot shadow the env,
and the CPU tools run with `python -P` so a stray `struct.py` in the working directory cannot shadow the
standard library (that happened once).
