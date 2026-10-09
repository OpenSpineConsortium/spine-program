# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): service/modal_app.py [tracked at 097933a]
"""Modal deployment of the level service: per-second GPU billing, scale-to-zero, weights never leave the container.

    pip install modal && modal setup                      # once, with the user's Modal account
    modal secret create hf-read HF_TOKEN=<read token>     # once; the token is stored in Modal, not in code
    modal deploy service/modal_app.py                     # prints the https URL to put in pacs/remote.js

GPU choice and keep-warm are the two knobs that decide latency and cost: an L4 (about $0.80/h on Modal)
answers a 2,048 px film in well under 100 ms of compute; `min_containers=1` keeps one warm so the first
visitor does not pay a cold start (cost = the hourly rate around the clock), `min_containers=0` scales to
zero and the first request after `scaledown_window` seconds of quiet waits a few seconds for a container.
"""
import modal

app = modal.App("openspine-level-id")
image = (modal.Image.debian_slim(python_version="3.11")
         .apt_install("libglib2.0-0", "libgl1")
         .pip_install("torch==2.6.0", "torchvision==0.21.0", index_url="https://download.pytorch.org/whl/cu124")
         .pip_install("fastapi==0.115.6", "python-multipart==0.0.20", "huggingface_hub==0.27.1", "ultralytics==8.3.58", "numpy<2.1", "pillow", "opencv-python-headless")
         .add_local_file("service/app.py", "/app/app.py").add_local_file("service/model_defs.py", "/app/model_defs.py"))


@app.function(image=image, gpu="L4", secrets=[modal.Secret.from_name("hf-read")], min_containers=int(0), scaledown_window=600, timeout=120)
@modal.asgi_app()
def web():
    import os
    import sys
    os.environ.setdefault("WEIGHTS_REPO", "gregoryschwingmdphd/level-id-weights")
    os.environ.setdefault("WEIGHTS_DIR", "/tmp/weights")
    sys.path.insert(0, "/app")
    from app import app as fastapi_app          # its startup hook pulls the weights and warms the models
    return fastapi_app
