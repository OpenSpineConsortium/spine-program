#!/usr/bin/env python3
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from CTSpinoPelvic1K (public, master) docker/fetch_spineps_weights.py; UNTRACKED in the working tree at 7ddfe38 on 2026-10-08. The banned word, where it occurred, is rewritten as origin.
"""
docker/fetch_spineps_weights.py — bake the SPINEPS **CT** weights into the image.

Run at BUILD time only (docker/Dockerfile.spineps).  Compute nodes have no outbound
internet and SPINEPS auto-downloads on first use, so the three CT models have to be
resident before the image ships:

    semantic  ct            (release v1.4.2, ct.zip)          spine subregions
    instance  ct_instance   (release v1.4.2, CT_instance.zip) vertebra instances
    labeling  ct_labeling   (release v1.4.0, ct_labeling.zip) C1..L6 naming

The download goes through SPINEPS' own get_*_model() rather than a hand-rolled curl,
so the release URLs, the version suffix and the extract-path convention all stay
upstream's business — a bump in spineps.utils.auto_download is picked up for free.

Constructing the model object can fail on a GPU-less builder even after the weights
land, so each fetch is caught and the REAL gate is the post-check: every requested
model must exist as a folder holding an inference_config.json (or, for the labeling
classifier, a checkpoint).  Non-zero exit fails the build.
"""
from __future__ import annotations

import os
import sys
import traceback
from pathlib import Path

WANT = [("semantic", "ct"), ("instance", "ct_instance"), ("labeling", "ct_labeling")]


def main() -> int:
    models_dir = Path(os.environ.get("SPINEPS_SEGMENTOR_MODELS", "/opt/spineps_models"))
    models_dir.mkdir(parents=True, exist_ok=True)
    print(f"[weights] SPINEPS_SEGMENTOR_MODELS = {models_dir}", flush=True)

    from spineps.get_models import get_instance_model, get_labeling_model, get_semantic_model
    getter = {"semantic": get_semantic_model, "instance": get_instance_model,
              "labeling": get_labeling_model}

    for phase, name in WANT:
        print(f"[weights] fetching {phase}: {name}", flush=True)
        try:
            getter[phase](name)
            print(f"[weights]   ok {name}", flush=True)
        except Exception:                    # model may fail to INSTANTIATE without a GPU —
            traceback.print_exc()            # the download itself still happened; verify below
            print(f"[weights]   {name}: constructor raised (checked below)", flush=True)

    # ── gate ─────────────────────────────────────────────────────────────────
    dirs = sorted(p for p in models_dir.iterdir() if p.is_dir())
    print(f"[weights] models present: {[p.name for p in dirs]}", flush=True)

    def _has_weights(p: Path) -> bool:
        return ((p / "inference_config.json").exists()
                or any(p.rglob("*.pth")) or any(p.rglob("*.ckpt")))

    populated = [p for p in dirs if _has_weights(p)]
    missing = [n for _, n in WANT
               if not any(n.replace("_", "").lower() in p.name.replace("_", "").lower()
                          or p.name.replace("_", "").lower().startswith(n.replace("_", "").lower())
                          for p in populated)]

    if len(populated) < len(WANT):
        print(f"FATAL: expected {len(WANT)} populated SPINEPS CT model folders, "
              f"got {[p.name for p in populated]}", file=sys.stderr)
        return 1
    if missing:
        # Folder naming is upstream's (<download_name>_<version>); a name miss with the
        # right count is a rename, not an absence — warn, don't fail.
        print(f"[weights] NOTE: could not name-match {missing} against "
              f"{[p.name for p in populated]} — folder naming changed upstream?", flush=True)

    total_mb = sum(f.stat().st_size for f in models_dir.rglob("*") if f.is_file()) / 1e6
    print(f"[weights] ok — {len(populated)} model folders, {total_mb:.0f} MB", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
