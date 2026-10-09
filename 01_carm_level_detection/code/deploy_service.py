# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/deploy_service.py [tracked at 097933a]
"""Release the current best models to the level service, so the website always serves the latest robust
model and never a downloadable file.

    python tools/deploy_service.py --detector PATH --level-model PATH --recurrent-head PATH --registry-id M19 \
        [--weights-repo gregoryschwingmdphd/level-id-weights] [--space USER/level-id] [--host-restart URL]

Steps: hash the three weight files, write registry.json (ids, sha256, input transform), upload them to the
PRIVATE weights repo (never a public one; the script refuses if the repo is public), then, when a Hugging
Face Docker Space is named, push service/ to it and set HF_TOKEN + WEIGHTS_REPO as Space secrets; for any
other host, print the docker build/run lines (the container pulls the weights at start-up with the token).
Tokens are read from files, never from the command line, and never printed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--detector", required=True)
    ap.add_argument("--level-model", required=True)
    ap.add_argument("--recurrent-head", required=True)
    ap.add_argument("--registry-id", required=True, help="model registry id of the level model, e.g. M19")
    ap.add_argument("--detector-note", default="spine-detector detect_v5z (yolo11m-pose, zoomed-window fine-tune)")
    ap.add_argument("--rung", type=int, default=1)
    ap.add_argument("--aug", type=int, default=2)
    ap.add_argument("--release", default=None)
    ap.add_argument("--weights-repo", default="gregoryschwingmdphd/level-id-weights")
    ap.add_argument("--space", default=None, help="Docker Space id to push service/ to (needs a plan that allows Docker Spaces)")
    ap.add_argument("--token-file", default="~/.cache/huggingface/token")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    import datetime
    from huggingface_hub import HfApi
    tok = Path(a.token_file).expanduser().read_text().strip()
    api = HfApi(token=tok)
    info = api.repo_info(a.weights_repo)
    if not info.private:
        print(f"REFUSING: {a.weights_repo} is public; the weights must never be uploaded to a public repo", file=sys.stderr); return 2
    reg = {"release": a.release or datetime.date.today().isoformat(),
           "detector": {"file": "detector.pt", "source": a.detector_note, "sha256": sha(a.detector)},
           "level_model": {"file": "level_model.pt", "registry_id": a.registry_id, "rung": a.rung, "aug": a.aug, "arch": "resnet18", "sha256": sha(a.level_model)},
           "recurrent_head": {"file": "recurrent_head.pt", "sha256": sha(a.recurrent_head)},
           "tgt_px": 96, "size": 320,
           "input_transform": "detector at imgsz 640; level crops: target box scaled to 96 px on a 320 px canvas, band of (2*rung+1) target heights, marker channel; grey normalised to the 0.5-99.5 percentile",
           "level_order": "C1..C7,T1..T12,T13,L1..L6,sacrum"}
    print(json.dumps(reg, indent=1))
    if a.dry_run:
        return 0
    tmp = Path(os.environ.get("TMPDIR", "/tmp")) / "level_id_release"; tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "registry.json").write_text(json.dumps(reg, indent=1))
    for src, name in ((a.detector, "detector.pt"), (a.level_model, "level_model.pt"), (a.recurrent_head, "recurrent_head.pt"), (tmp / "registry.json", "registry.json")):
        api.upload_file(path_or_fileobj=str(src), path_in_repo=name, repo_id=a.weights_repo, repo_type="model", commit_message=f"release {reg['release']}: {a.registry_id}")
        print("uploaded", name)
    svc = Path(__file__).resolve().parent.parent / "service"
    if a.space:
        api.create_repo(a.space, repo_type="space", space_sdk="docker", private=False, exist_ok=True)
        api.upload_folder(folder_path=str(svc), repo_id=a.space, repo_type="space", commit_message=f"service release {reg['release']}")
        api.add_space_secret(a.space, "HF_TOKEN", tok)
        api.add_space_variable(a.space, "WEIGHTS_REPO", a.weights_repo)
        api.restart_space(a.space)
        print("space updated and restarted:", a.space)
    else:
        print("no Space named; on any Docker host run:")
        print(f"  docker build -t level-id {svc}")
        print(f"  docker run -d -p 7860:7860 -e HF_TOKEN=<read token> -e WEIGHTS_REPO={a.weights_repo} level-id")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
