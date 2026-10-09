#!/bin/bash
# source-of-copy: spinesurg-ct-nnunet repository (private), branch L6_Class, commit 097933a, path scripts/_env_probe.sh
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
# Runs ON THE GRID, piped to `ssh ... bash -s` by scripts/export_env.sh.
# Prints the environment lock body: the interpreter, the CUDA build, the GPU, then pip freeze.
# Kept as a file in the repository rather than embedded in an ssh argument, because quoting a python -c
# through wsl -> ssh -> bash needs three levels of escaping and silently returned nothing when it was.
PY=$HOME/mambaforge/envs/spineps/bin/python
"$PY" - <<'PYEOF'
import platform
import sys
print("# python", sys.version.split()[0], platform.platform())
try:
    import torch
    print("# torch", torch.__version__, "| cuda", torch.version.cuda,
          "| cudnn", torch.backends.cudnn.version())
except Exception as e:  # noqa: BLE001
    print("# torch UNAVAILABLE:", type(e).__name__, e)
PYEOF
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>/dev/null | head -1 | sed 's/^/# gpu /'
echo "#"
"$PY" -m pip freeze 2>/dev/null
