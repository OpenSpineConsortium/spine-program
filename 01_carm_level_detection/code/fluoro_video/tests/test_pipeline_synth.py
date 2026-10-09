# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/tests/test_pipeline_synth.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""End to end on synthetic videos with KNOWN truth (tools/fluoro_video/synth.py): boxes within a small pixel tolerance,
on/off times within one sample interval (and, after refinement, one frame), the duplication pattern, the 2x
playback speed read from a burned-in clock, a hard cut and a replay, and variable-frame-rate timestamps."""
import csv
from pathlib import Path

import numpy as np
import pytest

BOX_TOL = 3          # px
FRAME = 1 / 30.0


def _rows(clip, out_root):
    p = Path(out_root) / clip["files"]["frames_csv"]
    with open(p, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _box_ok(a, b, tol=BOX_TOL):
    return np.max(np.abs(np.array(a) - np.array(b))) <= tol


def test_rect_motion(synth_runs, synth_videos, cfg):
    man, clips = synth_runs["rect_motion"]
    T = synth_videos["rect_motion"]
    assert len(clips) == 1, [c["clip_id"] for c in clips]
    c = clips[0]
    assert _box_ok(c["box"], T["box"]), (c["box"], T["box"])
    dt = 1.0 / cfg[0]["sampling"]["sample_hz"]
    seg = [s for s in man["segments"] if s["kept"]][0]
    assert abs(seg["t_first"] - T["on_s"]) <= dt + 1e-6                 # coarse: within one sample interval
    assert abs(c["pts_start_s"] - T["on_s"]) <= FRAME + 1e-6            # refined: within one frame
    assert abs(c["pts_end_s"] - T["last_on_s"]) <= FRAME + 1e-6
    a = c["timing"]["acquisition"]
    assert a["modal_frames_per_image"] == T["frames_per_image"]
    assert abs(a["images_per_video_s"] - T["images_per_s"]) < 0.2
    assert c["liveness"] == "live"
    assert c["timing"]["speed_evidence"] == "none" and c["timing"]["speed_verified"] is False
    assert c["timing"]["vfr"] is False


def test_circle_static(synth_runs, synth_videos):
    man, clips = synth_runs["circle_static"]
    T = synth_videos["circle_static"]
    assert len(clips) == 1
    c = clips[0]
    assert _box_ok(c["box"], T["box"], 4), (c["box"], T["box"])
    assert c["field_shape"] == "circle"
    assert abs(c["pts_start_s"] - T["on_s"]) <= FRAME + 1e-6
    assert abs(c["pts_end_s"] - T["last_on_s"]) <= FRAME + 1e-6
    a = c["timing"]["acquisition"]
    assert a["repeat_pattern"] in T["pattern"], a
    assert abs(a["images_per_video_s"] - T["images_per_s"]) < 0.3


def test_counter_2x_speed(synth_runs, synth_videos, scratch):
    man, clips = synth_runs["counter_2x"]
    T = synth_videos["counter_2x"]
    assert len(clips) == 1
    c = clips[0]
    tm = c["timing"]
    assert tm["speed_evidence"] in ("ocr_clock", "ocr_clock_pooled"), (tm["speed_detail"], man["ocr"])
    assert abs(tm["speed_factor"] - T["speed"]) < 0.1
    assert abs(tm["acquisition"]["images_per_video_s"] - T["images_per_video_s"]) < 0.3
    assert abs(tm["images_per_real_s"] - T["images_per_real_s"]) < 0.3
    # real_time_s in the per-frame table = (pts - pts0) x speed
    rows = _rows(c, scratch / "out")
    last = rows[-1]
    assert abs(float(last["real_time_s"]) - float(last["t_video_s"]) * tm["speed_factor"]) < 1e-3
    assert any(r["ocr_clock_s"] for r in rows)


def test_cut_and_replay(synth_runs, synth_videos):
    man, clips = synth_runs["cut_replay"]
    T = synth_videos["cut_replay"]
    cuts = sorted(cu["frame"] for s in man["segments"] for cu in ((s.get("refinement") or {}).get("cuts") or []))
    for f in T["cuts_frames"]:
        assert any(abs(f - x) <= 1 for x in cuts), (f, cuts)
    assert len(clips) == 4, [(c["clip_id"], c["pts_start_s"], c["pts_end_s"]) for c in clips]
    rep = [c for c in clips if c["replay"]["is_replay"]]
    assert len(rep) == 1
    r = rep[0]
    assert abs(r["pts_start_s"] - T["replay_s"][0]) <= 2 * FRAME + 1e-6
    assert abs(r["pts_end_s"] - (T["replay_s"][1] - FRAME)) <= 2 * FRAME + 1e-6
    assert r["replay"]["of_clip"] == clips[0]["clip_id"]
    assert r["use_for_rates"] is False
    assert all(c["use_for_rates"] for c in clips if c is not r)


def test_vfr_timestamps(synth_runs, synth_videos, scratch):
    man, clips = synth_runs["vfr"]
    T = synth_videos["vfr"]
    assert man["pts"]["vfr"] is True
    assert len(clips) == 1
    c = clips[0]
    assert c["timing"]["vfr"] is True
    rows = _rows(c, scratch / "out")
    got = np.array([float(r["pts_s"]) for r in rows])
    want = np.array(T["pts_s"])
    k0 = int(rows[0]["source_frame_index"])
    assert np.max(np.abs(got - want[k0:k0 + got.size])) < 2e-3        # container time base rounding
