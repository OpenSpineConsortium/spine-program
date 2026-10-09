# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/common.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Shared helpers: configuration, overrides, hashing, software versions, stable JSON."""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import math
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import yaml

PKG_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = PKG_DIR / "config.yaml"
DEFAULT_OVERRIDES = PKG_DIR / "overrides.yaml"
# the files whose bytes define the tool (hashed when the tree is not a clean git commit)
TOOL_GLOBS = ("*.py", "config.yaml", "overrides.yaml", "environment.yml", "explicit_lock.txt",
              "tests/*.py", "slurm/*.sbatch", "slurm/*.sh")
OVERRIDE_ACTIONS = ("reject", "split", "merge", "replace-box")


# ------------------------------------------------------------------------------------------------ hashing
def sha256_file(p, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def dir_digest(files, root):
    """sha256 over sorted (relative name, sha256 of bytes) pairs: the digest of a set of files."""
    h = hashlib.sha256()
    for f in sorted(files, key=lambda p: os.path.relpath(p, root).replace("\\", "/")):
        h.update(os.path.relpath(f, root).replace("\\", "/").encode())
        h.update(b"\0")
        h.update(sha256_file(f).encode())
        h.update(b"\n")
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------ config
def load_config(path=None):
    p = Path(path) if path else DEFAULT_CONFIG
    raw = p.read_bytes()
    cfg = yaml.safe_load(raw.decode("utf-8"))
    return cfg, sha256_bytes(raw), str(p)


def load_overrides(path=None):
    """The ONLY place a person may state a box, a time or a decision. Every entry must name the video, the action,
    the exact values and a reason; anything else is refused."""
    p = Path(path) if path else DEFAULT_OVERRIDES
    if not p.exists():
        return [], None, str(p)
    raw = p.read_bytes()
    doc = yaml.safe_load(raw.decode("utf-8")) or {}
    ents = doc.get("overrides") or []
    for i, e in enumerate(ents):
        miss = [k for k in ("video", "action", "reason") if not e.get(k)]
        if miss:
            raise SystemExit(f"overrides.yaml entry {i}: missing {miss}")
        if e["action"] not in OVERRIDE_ACTIONS:
            raise SystemExit(f"overrides.yaml entry {i}: action {e['action']!r} not in {OVERRIDE_ACTIONS}")
        if e["action"] in ("split", "merge", "replace-box") and not e.get("values"):
            raise SystemExit(f"overrides.yaml entry {i}: action {e['action']} needs `values`")
        if len(str(e["reason"]).strip()) < 10:
            raise SystemExit(f"overrides.yaml entry {i}: the reason must say why (>= 10 characters)")
    return ents, sha256_bytes(raw), str(p)


# ------------------------------------------------------------------------------------------------ identity
def tool_files():
    out = []
    for g in TOOL_GLOBS:
        out += [p for p in PKG_DIR.glob(g) if p.is_file()]
    return sorted(set(out))


def code_identity():
    """git commit of the package if its files are committed and unmodified, else a sha256 of the tool files."""
    files = tool_files()
    tree = dir_digest(files, PKG_DIR)
    ident = dict(tool_files_sha256=tree, n_tool_files=len(files), git_commit=None, git_clean=None)
    try:
        top = subprocess.run(["git", "-C", str(PKG_DIR), "rev-parse", "HEAD"], capture_output=True, text=True,
                             timeout=20)
        if top.returncode == 0:
            st = subprocess.run(["git", "-C", str(PKG_DIR), "status", "--porcelain", "--", "."], capture_output=True,
                                text=True, timeout=20)
            ident["git_commit"] = top.stdout.strip()
            ident["git_clean"] = st.returncode == 0 and st.stdout.strip() == ""
    except Exception:          # no git on the node or not a repository: the file digest stands alone
        pass
    ident["identity"] = (f"git:{ident['git_commit']}" if ident.get("git_clean") else f"sha256:{tree}")
    return ident


def tool_path(name):
    """A binary from the running environment first (the pinned env), then PATH."""
    cand = Path(sys.prefix) / "bin" / name
    if cand.exists():
        return str(cand)
    from shutil import which
    return which(name) or name


def software_versions():
    v = dict(python=platform.python_version(), platform=platform.platform(), numpy=np.__version__)
    for mod in ("scipy", "PIL", "yaml", "matplotlib", "av", "pytesseract"):
        try:
            m = __import__(mod)
            v[mod] = getattr(m, "__version__", None)
        except Exception:
            v[mod] = None
    try:
        import av
        v["av_libraries"] = {k: ".".join(str(x) for x in val) for k, val in sorted(av.library_versions.items())}
    except Exception:
        pass
    for b in ("ffmpeg", "ffprobe", "tesseract"):
        try:
            r = subprocess.run([tool_path(b), "-version" if b != "tesseract" else "--version"], capture_output=True,
                               text=True, timeout=30)
            line = (r.stdout or r.stderr).splitlines()[0].strip()
            v[b] = line
            v[b + "_path"] = tool_path(b)
        except Exception:
            v[b] = None
    return v


def now_iso():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------------------------------------ JSON
def clean(o, nd=6):
    """numpy -> python, floats rounded to nd significant digits (stable across tiny summation-order differences),
    NaN/inf -> None."""
    if isinstance(o, dict):
        return {str(k): clean(v, nd) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v, nd) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        x = float(o)
        if not math.isfinite(x):
            return None
        if x == 0:
            return 0.0
        return float(f"{x:.{nd}g}")
    if isinstance(o, np.ndarray):
        return clean(o.tolist(), nd)
    if isinstance(o, Path):
        return str(o)
    return o


def dump_json(obj, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(clean(obj), f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


VOLATILE_KEYS = ("run_timestamp", "wall_time_s", "started", "finished", "host", "slurm_job_id", "elapsed_s",
                 "hostname", "work_dir", "out_dir")


def strip_volatile(o):
    """A manifest without the keys that legitimately differ between two identical runs (timestamps, host, wall
    time, absolute output locations)."""
    if isinstance(o, dict):
        return {k: strip_volatile(v) for k, v in o.items() if k not in VOLATILE_KEYS}
    if isinstance(o, list):
        return [strip_volatile(v) for v in o]
    return o


def safe_id(s, n=48):
    t = re.sub(r"[^A-Za-z0-9_-]+", "-", s).strip("-")
    if len(t) > n:
        t = t[:n].rstrip("-") + "-" + hashlib.sha1(s.encode()).hexdigest()[:6]
    return t
