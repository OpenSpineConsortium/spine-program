# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/inventory.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""The list of input videos, decided by rule from what is on disk (no file is named by hand).

A file is a candidate when its extension is in inputs.include_ext. It is an input video when ffprobe finds a video
stream with >= inputs.min_video_frames packets and >= inputs.min_video_s of duration (this drops the journal-figure
GIF thumbnails, which are single frames). A file whose name matches inputs.transcode_regex (PMC's viewer
re-encodes, e.g. '-pmcvs_normal.mp4') is dropped only when a sibling in the same folder, without that marker,
has a duration within inputs.transcode_duration_tol_s (it is then a lower-resolution copy of that sibling); the
rule and the sibling are recorded.

Expected region / view per video come from the scan document (docs/FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md: its
ranked table and its raw-candidate JSON), matched by the YouTube id / PMCID / Commons file name, and reduced to
coarse classes by keyword. They describe the VIDEO as the scan saw it, not a measured property of any segment.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .common import safe_id, sha256_file, tool_path
from .decode import ffprobe


def count_packets(path):
    r = subprocess.run([tool_path("ffprobe"), "-v", "error", "-select_streams", "v:0", "-count_packets",
                        "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, timeout=1800)
    try:
        return int(r.stdout.strip().split(",")[0])
    except Exception:
        return None


def region_class(t):
    t = (t or "").lower()
    out = []
    if "cervic" in t or re.search(r"\bc[1-7]\b", t):
        out.append("cervical")
    if "thorac" in t or re.search(r"\bt\d{1,2}\b", t):
        out.append("thoracic")
    if "lumb" in t or re.search(r"\bl[1-5]\b", t):
        out.append("lumbar")
    if "sacr" in t or "pelv" in t or re.search(r"\bs1\b", t):
        out.append("sacral")
    return "+".join(out) if out else "unknown"


def view_class(t):
    t0 = t or ""
    t = t0.lower()
    out = []
    if re.search(r"\bAP\b", t0) or "antero" in t or "open-mouth" in t:
        out.append("AP")
    if "lateral" in t and "lateral bending" not in t or "lat " in t:
        out.append("lateral")
    if "oblique" in t:
        out.append("oblique")
    if "sweep" in t or "rotational" in t or "spin" in t:
        out.append("sweep")
    return "+".join(out) if out else "unknown"


def parse_scan_doc(path):
    """{key: dict(region_text, view_text)} keyed by YouTube id / PMCID / Commons file name."""
    p = Path(path)
    if not p.exists():
        return {}
    s = p.read_text(encoding="utf-8", errors="replace")
    ctx = {}

    def put(key, region, view, src):
        if key and key not in ctx:
            ctx[key] = dict(region_text=region, view_text=view, context_source=src)
    # ranked table rows: | # | [title](url) | procedure | region | view | ...
    for line in s.splitlines():
        if not line.startswith("| ") or "](" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not cells[0].isdigit():
            continue
        urls = re.findall(r"\((https?://[^)]+)\)", cells[1])
        for u in urls:
            for k in _keys_from_url(u):
                put(k, cells[3], cells[4], "scan doc ranked table")
    # raw candidates JSON block
    m = re.search(r"```json\s*(\[.*?\])\s*```", s, re.S)
    if m:
        try:
            angles = json.loads(m.group(1))
        except Exception:
            angles = []
        for a in angles:
            for c in a.get("candidates", []) if isinstance(a, dict) else []:
                for k in _keys_from_url(str(c.get("url", ""))):
                    put(k, str(c.get("region", "")), str(c.get("views", "")), "scan doc raw candidates")
    return ctx


def _keys_from_url(u):
    ks = []
    m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", u)
    if m:
        ks.append(m.group(1))
    m = re.search(r"(PMC\d+)", u)
    if m:
        ks.append(m.group(1))
    m = re.search(r"File:([^?#]+)", u)
    if m:
        ks.append(m.group(1))
    return ks


def build(cfg, repo_root=None):
    I = cfg["inputs"]
    root = Path(I["root"])
    exts = {e.lower() for e in I["include_ext"]}
    files = []
    for d in I["scan_dirs"]:
        base = root / d
        if base.exists():
            files += [p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in exts]
    files = sorted(files, key=lambda p: str(p.relative_to(root)))
    # downloads may still be running beside this pipeline: yt-dlp's per-format intermediates and partial files are
    # never inputs, and a YouTube video counts only once yt-dlp has written its id to the download archive (it does
    # so after the final merge)
    rx_skip = re.compile(I["intermediate_regex"])
    arch = root / I["youtube_archive"]
    done_yt = set()
    if arch.exists():
        for line in arch.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[0] == "youtube":
                done_yt.add(parts[1])
    doc = Path(cfg["context_doc"])
    if not doc.is_absolute() and repo_root is not None:
        doc = Path(repo_root) / doc
    ctx = parse_scan_doc(doc)
    rx_t = re.compile(I["transcode_regex"])
    entries = []
    probes = {}
    for p in files:
        rel = str(p.relative_to(root)).replace("\\", "/")
        parts = rel.split("/")
        src = parts[0]
        source_id = parts[1] if len(parts) > 2 else p.stem
        try:
            size = p.stat().st_size
        except FileNotFoundError:          # vanished between listing and stat (a download finishing)
            continue
        e = dict(relpath=rel, path=str(p), source=src, source_id=source_id, size=size)
        if rx_skip.search(p.name):
            e.update(include=False, rule="excluded: download intermediate (yt-dlp format part / partial file)")
            entries.append(e)
            continue
        if src == "youtube" and source_id not in done_yt:
            e.update(include=False, rule=f"excluded: id not in {I['youtube_archive']} (download not finished)")
            entries.append(e)
            continue
        try:
            pr = ffprobe(p)
        except Exception as ex:
            e.update(include=False, rule=f"excluded: ffprobe failed ({ex})"[:200])
            entries.append(e)
            continue
        probes[str(p)] = pr
        dur = None
        for v in (pr["format"].get("duration"), pr["video"].get("duration")):
            try:
                dur = float(v)
                break
            except Exception:
                continue
        npk = count_packets(p) if pr["n_video_streams"] else 0
        e.update(probe=pr, duration_s=dur, n_packets=npk)
        if not pr["n_video_streams"]:
            e.update(include=False, rule="excluded: no video stream")
        elif (npk or 0) < int(I["min_video_frames"]):
            e.update(include=False, rule=f"excluded: {npk} frames < min_video_frames {I['min_video_frames']} "
                                         "(a still image)")
        elif dur is not None and dur < float(I["min_video_s"]):
            e.update(include=False, rule=f"excluded: duration {dur:.2f} s < min_video_s {I['min_video_s']}")
        else:
            e.update(include=True, rule="included: video stream with enough frames")
        entries.append(e)
    # transcode duplicates
    by_dir = {}
    for e in entries:
        by_dir.setdefault(str(Path(e["path"]).parent), []).append(e)
    for e in entries:
        if not e.get("include") or not rx_t.search(Path(e["path"]).name):
            continue
        sib = [s for s in by_dir[str(Path(e["path"]).parent)] if s is not e and s.get("include")
               and not rx_t.search(Path(s["path"]).name) and s.get("duration_s") is not None
               and e.get("duration_s") is not None
               and abs(s["duration_s"] - e["duration_s"]) <= float(I["transcode_duration_tol_s"])]
        if sib:
            e.update(include=False, rule=f"excluded: viewer transcode of {Path(sib[0]['path']).name} (same folder, "
                                         f"duration within {I['transcode_duration_tol_s']} s)")
    for e in entries:
        if e["source"] == "youtube":
            vid = f"yt-{e['source_id']}"
            key = e["source_id"]
        elif e["source"] == "pmc":
            vid = f"pmc-{e['source_id']}-{safe_id(Path(e['path']).stem, 28)}"
            key = e["source_id"]
        else:
            vid = f"{e['source']}-{safe_id(Path(e['path']).stem, 28)}"
            key = Path(e["path"]).name
        e["video_id"] = vid
        c = ctx.get(key) or {}
        e["expected"] = dict(region_text=c.get("region_text"), view_text=c.get("view_text"),
                             region=region_class(c.get("region_text")), view=view_class(c.get("view_text")),
                             source=c.get("context_source") or "not in the scan doc",
                             note="video-level expectation from the scan document text; not measured per segment")
        if e.get("include"):
            e["sha256"] = sha256_file(e["path"])
    ids = [e["video_id"] for e in entries if e.get("include")]
    if len(ids) != len(set(ids)):
        raise SystemExit("inventory: two inputs map to one video_id")
    return entries
