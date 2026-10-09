# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/tests/conftest.py [untracked at 097933a (laptop copy of 2026-10-08)]
import os
import tempfile
from pathlib import Path

import pytest

from tools.fluoro_video.common import load_config, load_overrides, sha256_file


@pytest.fixture(scope="session")
def cfg():
    c, sha, _ = load_config()
    return c, sha


def _scratch():
    base = os.environ.get("FV_TEST_DIR")
    if base:
        Path(base).mkdir(parents=True, exist_ok=True)
        return Path(tempfile.mkdtemp(dir=base))
    shm = Path("/dev/shm")
    if shm.exists():
        return Path(tempfile.mkdtemp(dir=shm, prefix="fvtest_"))
    return Path(tempfile.mkdtemp(prefix="fvtest_"))


@pytest.fixture(scope="session")
def scratch():
    return _scratch()


@pytest.fixture(scope="session")
def synth_videos(scratch):
    pytest.importorskip("av")
    from tools.fluoro_video import synth
    return synth.make_all(scratch / "videos")


def entry_for(path, vid):
    from tools.fluoro_video.decode import ffprobe
    pr = ffprobe(path)
    dur = None
    for v in (pr["format"].get("duration"), pr["video"].get("duration")):
        try:
            dur = float(v)
            break
        except Exception:
            pass
    return dict(video_id=vid, relpath=f"synthetic/{Path(path).name}", path=str(path), source="synthetic",
                source_id=vid, size=Path(path).stat().st_size, sha256=sha256_file(path), probe=pr, duration_s=dur,
                expected=dict(region="synthetic", view="synthetic"))


@pytest.fixture(scope="session")
def synth_runs(synth_videos, scratch, cfg):
    """The pipeline run once on every synthetic video: {name: (manifest, clips)}."""
    from tools.fluoro_video import pipeline as PL
    c, sha = cfg
    ov, ovsha, _ = load_overrides()
    out, work = scratch / "out", scratch / "work"
    res = {}
    for name, t in synth_videos.items():
        e = entry_for(t["path"], f"synth-{name}")
        res[name] = PL.run_video(e, c, sha, ov, ovsha, out, work, log=lambda m: print(m, flush=True))
    return res
