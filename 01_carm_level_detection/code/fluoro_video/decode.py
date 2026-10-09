# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/decode.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Decoding with presentation timestamps.

Every frame is decoded sequentially from the start of the file with PyAV (libavcodec). No seeking: a decode after a
seek is not guaranteed to reproduce the frames of a sequential decode on open-GOP streams, and the two passes of the
pipeline must see bit-identical frames. Each frame carries its own pts (the decoder's presentation timestamp in the
stream time base); frame index / nominal fps are never used to compute time.
"""
from __future__ import annotations

import json
import subprocess
from fractions import Fraction

import numpy as np

from .common import tool_path


def ffprobe(path):
    r = subprocess.run([tool_path("ffprobe"), "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                       capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {path}: {r.stderr[:400]}")
    d = json.loads(r.stdout)
    vs = [s for s in d.get("streams", []) if s.get("codec_type") == "video"]
    v = vs[0] if vs else {}
    keep = ("codec_name", "profile", "width", "height", "pix_fmt", "r_frame_rate", "avg_frame_rate", "time_base",
            "start_time", "duration", "nb_frames", "color_range", "color_space", "field_order", "sample_aspect_ratio")
    return dict(video={k: v.get(k) for k in keep},
                format={k: d.get("format", {}).get(k) for k in ("format_name", "duration", "bit_rate", "size",
                                                                  "start_time")},
                n_video_streams=len(vs))


def frac_str(x):
    if x is None:
        return None
    return f"{x.numerator}/{x.denominator}"


def rate_float(s):
    try:
        if s is None:
            return None
        f = Fraction(str(s))
        return float(f) if f != 0 else None
    except Exception:
        return None


class Decoder:
    """Iterate (index, pts, pts_s, key_frame, pict_type, frame) over every decoded frame in presentation order.

    pts: the frame's pts; when the container gives none, the previous pts plus the previous frame's duration
    (counted in `n_interpolated_pts`; reported in the manifest)."""

    def __init__(self, path, threads=0):
        import av
        self.av = av
        self.path = str(path)
        # metadata_errors="replace": a QuickTime file with non-UTF-8 metadata (PMC4852439) must still decode
        self.container = av.open(self.path, metadata_errors="replace")
        self.stream = self.container.streams.video[0]
        self.stream.thread_type = "AUTO"            # frame + slice threading; libavcodec output is bit-exact
        if threads:
            self.stream.thread_count = int(threads)
        self.time_base = self.stream.time_base
        self.n_interpolated_pts = 0

    def __iter__(self):
        prev_pts = None
        prev_dur = None
        tb = self.time_base
        idx = 0
        for frame in self.container.decode(self.stream):
            pts = frame.pts
            if pts is None:
                pts = frame.dts if getattr(frame, "dts", None) is not None else None
            if pts is None:
                self.n_interpolated_pts += 1
                pts = (prev_pts + (prev_dur or 1)) if prev_pts is not None else 0
            if prev_pts is not None:
                prev_dur = pts - prev_pts
            prev_pts = pts
            pt = frame.pict_type
            pict = getattr(pt, "name", None) or str(pt)
            pict = {"1": "I", "2": "P", "3": "B", "NONE": "?"}.get(str(pict), str(pict))
            yield idx, int(pts), float(Fraction(pts) * tb), bool(frame.key_frame), pict[:2], frame
            idx += 1

    def close(self):
        try:
            self.container.close()
        except Exception:
            pass


def to_rgb(frame):
    """rgb24 via libswscale using the frame's own colour metadata (limited-range YUV expands to full range)."""
    return frame.to_ndarray(format="rgb24")


def luma_u8(rgb):
    """BT.601 luma, integer arithmetic (deterministic): Y = (19595 R + 38470 G + 7471 B + 32768) >> 16."""
    r = rgb[..., 0].astype(np.uint32)
    g = rgb[..., 1].astype(np.uint32)
    b = rgb[..., 2].astype(np.uint32)
    return ((19595 * r + 38470 * g + 7471 * b + 32768) >> 16).astype(np.uint8)


def pts_summary(pts_s, r_frame_rate, avg_frame_rate, vfr_rel_tol, vfr_frac_min):
    """VFR test on the decoded pts: a frame interval is irregular when it differs from the median interval by more
    than max(vfr_rel_tol x median, 1.5 ms) (1.5 ms absorbs millisecond time bases, e.g. 33/34 ms at 29.97 fps in
    Matroska). The stream is VFR when more than vfr_frac_min of the intervals are irregular."""
    t = np.asarray(pts_s, float)
    if t.size < 3:
        return dict(n_frames=int(t.size), vfr=False, note="fewer than 3 frames")
    d = np.diff(t)
    med = float(np.median(d))
    tol = max(vfr_rel_tol * med, 0.0015)
    irr = np.abs(d - med) > tol
    uniq, cnt = np.unique(np.round(d * 1000.0, 1), return_counts=True)
    order = np.argsort(-cnt)[:6]
    return dict(n_frames=int(t.size), first_pts_s=float(t[0]), last_pts_s=float(t[-1]),
                pts_span_s=float(t[-1] - t[0]), median_interval_ms=med * 1000.0,
                measured_fps=(1.0 / med) if med > 0 else None,
                mean_fps=((t.size - 1) / (t[-1] - t[0])) if t[-1] > t[0] else None,
                irregular_interval_frac=float(irr.mean()), vfr=bool(irr.mean() > vfr_frac_min),
                non_monotonic=int((d <= 0).sum()),
                interval_ms_top=[dict(ms=float(uniq[i]), n=int(cnt[i])) for i in order],
                r_frame_rate=r_frame_rate, avg_frame_rate=avg_frame_rate,
                r_frame_rate_float=rate_float(r_frame_rate), avg_frame_rate_float=rate_float(avg_frame_rate))
