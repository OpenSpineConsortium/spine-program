# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/tests/test_determinism_synth.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""The pipeline twice on three synthetic videos: identical clip digests and manifests (timestamps excluded).
The same check on >= 3 REAL videos is `cli determinism` (slurm/determinism.sbatch)."""
from tools.fluoro_video import pipeline as PL
from tools.fluoro_video.cli import compare_runs
from tools.fluoro_video.common import load_overrides

from .conftest import entry_for


def test_two_runs_identical(synth_videos, scratch, cfg):
    c, sha = cfg
    ov, ovsha, _ = load_overrides()
    names = ["rect_motion", "circle_static", "cut_replay"]
    for run in ("det1", "det2"):
        for n in names:
            e = entry_for(synth_videos[n]["path"], f"synth-{n}")
            PL.run_video(e, c, sha, ov, ovsha, scratch / run, scratch / f"work_{run}", log=lambda m: None)
    diffs, stats = compare_runs(scratch / "det1", scratch / "det2")
    assert stats["manifests"] == 3
    assert stats["clips"] >= 3
    assert not diffs, diffs
