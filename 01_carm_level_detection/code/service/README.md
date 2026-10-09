<!-- Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): service/README.md [tracked at 097933a] -->
---
title: OpenSpine level identification
emoji: 🦴
colorFrom: gray
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# Level-identification service

Serves the current release of the vertebra detector, the single-vertebra level model and the run labeller
behind one endpoint, so the website never holds model parameters.

- Weights: private Hugging Face model repo named by `WEIGHTS_REPO`, read with `HF_TOKEN` at start-up.
- `POST /infer` (multipart `image`, optional `conf`, `imgsz`) returns boxes, four corner landmarks per
  vertebra, the model's level name per box (run-labelled and single-crop), a contiguous-run decode and
  timing. `GET /health` reports the model registry entry served.
- CPU by default: detector at 640 px, level crops at 96 px on a 320 px canvas. A GPU is used when present.
- Deploy: `tools/deploy_service.py` in the private repo copies this directory to the host, uploads the weights
  named in the registry, and sets the secrets. Hosts tried: Hugging Face Docker Space (needs a paid plan for
  the org), Modal, Fly.io, an EC2 instance, or a workstation behind a Cloudflare tunnel; the container is the
  same everywhere.
