# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/pipeline.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""One video end to end: pass A (sampled panel detection) -> layouts -> segments -> pass B (native-rate crops,
boundary refinement, duplicates, cuts) -> replays -> clips -> OCR speed -> write clips, per-frame tables, manifest,
QC report."""
from __future__ import annotations

import csv
import math
import os
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image

from . import layouts as LY
from . import ocr as OC
from . import panels as PN
from . import qc as QC
from . import sourcetext as ST
from . import timing as TM
from .common import (code_identity, dir_digest, dump_json, now_iso, sha256_file, software_versions, tool_path)
from .decode import Decoder, luma_u8, pts_summary, to_rgb

FRAME_FIELDS = ["frame_file", "clip_frame_index", "source_frame_index", "pts", "time_base", "pts_s", "t_video_s",
                "real_time_s", "key_frame", "pict_type", "panel_score", "panel_present", "diff_prev_mean",
                "diff_prev_p995", "ncc_prev", "is_duplicate_of_previous", "image_update_index", "replay_of",
                "phash", "ocr_clock_text", "ocr_clock_s", "ocr_angle_text", "ocr_angle_deg"]


def _panel_params(cfg):
    P = dict(cfg["panel"])
    P["analysis_max_side"] = cfg["sampling"]["analysis_max_side"]
    return P


# ================================================================================================ pass A
def pass_a(path, cfg, duration_hint, log):
    P = _panel_params(cfg)
    S = cfg["sampling"]
    dt = 1.0 / float(S["sample_hz"])
    n_exp = max(1, int(math.ceil((duration_hint or 0) * float(S["sample_hz"]))) + 1)
    pool = set(np.unique(np.round(np.linspace(0, n_exp - 1, int(cfg["ocr"]["ocr_probe_pool"]))).astype(int)).tolist())
    dec = Decoder(path, cfg["runtime"]["decode_threads"])
    pts, pts_s, keys, picts = [], [], [], []
    samples, probes = [], {}
    next_t = None
    W = H = None
    t0 = time.time()
    prev_scene = None
    for idx, p, ps, key, pict, frame in dec:
        pts.append(p); pts_s.append(ps); keys.append(key); picts.append(pict)
        if next_t is None:
            next_t = ps
        if ps + 1e-9 >= next_t:
            rgb = to_rgb(frame)
            H, W = rgb.shape[:2]
            cands, M = PN.detect(rgb, P)
            sc = TM.thumb(M["luma"].astype(np.uint8), 64)
            scene = float(np.abs(sc - prev_scene).mean()) if (prev_scene is not None and prev_scene.shape == sc.shape) \
                else None
            prev_scene = sc
            si = len(samples)
            samples.append(dict(i=si, frame=idx, t=ps, cands=cands, scene_change=scene))
            if si in pool:
                probes[si] = luma_u8(rgb)
            next_t += dt
            while next_t <= ps:
                next_t += dt
        if idx % 20000 == 0 and idx:
            log(f"  pass A: frame {idx}, t={ps:.1f} s, {len(samples)} samples, {time.time() - t0:.0f} s")
    tb = dec.time_base
    n_interp = dec.n_interpolated_pts
    dec.close()
    return dict(pts=np.array(pts, np.int64), pts_s=np.array(pts_s, float), keys=np.array(keys, bool),
                picts=picts, samples=samples, probes=probes, W=W, H=H, time_base=f"{tb.numerator}/{tb.denominator}",
                n_interpolated_pts=n_interp, dt=dt, wall_s=time.time() - t0)


# ================================================================================================ segments
def make_segments(A, cfg, overrides, vid):
    P = dict(cfg["panel"])
    P.update(cfg["layout"])
    lays, member = LY.build_layouts(A["samples"], A["W"], A["H"], P)
    segs = []
    for L in lays:
        segs += LY.runs_for_layout(L, A["samples"], P, A["dt"])
    segs.sort(key=lambda s: (s["t_first"], s["layout"]))
    for n, s in enumerate(segs):
        s["id"] = f"S{n:03d}"
        s["box"] = list(next(L["box"] for L in lays if L["id"] == s["layout"]))
        s["box_source"] = "layout outer envelope (10th/90th percentile) of member candidate boxes"
        s["overridden"] = False
        s["override_reasons"] = []
    fr = {x["i"]: x["frame"] for x in A["samples"]}
    for s in segs:
        s["first_member_frame"] = fr[s["first_sample"]]
        s["last_member_frame"] = fr[s["last_sample"]]
        s["window_start_frame"] = fr[s["prev_sample"]] if s["prev_sample"] is not None else 0
        s["window_end_frame"] = fr[s["next_sample"]] if s["next_sample"] is not None else len(A["pts"]) - 1
    applied = apply_segment_overrides(segs, lays, overrides, vid)
    return lays, member, segs, applied


def apply_segment_overrides(segs, lays, overrides, vid):
    applied = []
    for o in overrides:
        if o["video"] != vid:
            continue
        act, val = o["action"], o.get("values") or {}
        if act == "reject":
            for s in segs:
                if s["id"] == o.get("segment"):
                    s["kept"] = False
                    s["rule"] = f"override reject: {o['reason']}"
                    s["overridden"] = True
                    s["override_reasons"].append(o["reason"])
                    applied.append(o)
        elif act == "replace-box":
            box = [int(v) for v in val["box"]]
            for s in segs:
                if s["id"] == o.get("segment") or (o.get("layout") and s["layout"] == o.get("layout")):
                    s["box"] = box
                    s["box_source"] = "override replace-box"
                    s["overridden"] = True
                    s["override_reasons"].append(o["reason"])
                    applied.append(o)
        elif act == "merge":
            ids = list(val.get("segments") or [])
            grp = [s for s in segs if s["id"] in ids]
            if len(grp) >= 2 and len({s["layout"] for s in grp}) == 1:
                a = min(grp, key=lambda s: s["t_first"])
                b = max(grp, key=lambda s: s["t_last"])
                a.update(last_sample=b["last_sample"], t_last=b["t_last"], next_sample=b["next_sample"],
                         last_member_frame=b["last_member_frame"], window_end_frame=b["window_end_frame"],
                         kept=True, rule=f"override merge of {ids}: {o['reason']}", overridden=True)
                a["override_reasons"].append(o["reason"])
                for s in grp:
                    if s is not a:
                        s["kept"] = False
                        s["rule"] = f"override merged into {a['id']}: {o['reason']}"
                        s["overridden"] = True
                        s["override_reasons"].append(o["reason"])
                applied.append(o)
        # 'split' is applied to clips after pass B (see split_overrides)
    return applied


# ================================================================================================ pass B
class SegState:
    def __init__(self, s, cfg, stage_dir, f_analysis, ocr_regions):
        self.s = s
        self.x0, self.y0, self.x1, self.y1 = s["box"]
        self.f = f_analysis
        self.recs = []
        self.prev_thumb = None
        self.prev_sig = None
        self.dir = stage_dir / s["id"]
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ocr_regions = ocr_regions
        self.next_ocr = None
        self.ocr_crops = []
        self.cfg = cfg


def pass_b(path, A, segs, qc_frames, ocr_regions, cfg, stage_dir, log):
    P = _panel_params(cfg)
    T = cfg["timing"]
    f_an = PN.analysis_factor(A["W"], A["H"], cfg["sampling"]["analysis_max_side"])
    active = [SegState(s, cfg, stage_dir, f_an, ocr_regions) for s in segs if s["kept"]]
    starts = sorted(active, key=lambda st: st.s["window_start_frame"])
    qc_store = {}
    qc_w = int(cfg["qc"]["frame_width"])
    dec = Decoder(path, cfg["runtime"]["decode_threads"])
    last_needed = max([st.s["window_end_frame"] for st in active] + list(qc_frames) + [-1])
    t0 = time.time()
    ocr_dt = float(cfg["ocr"]["ocr_interval_s"])
    for idx, p, ps, key, pict, frame in dec:
        if idx > last_needed:
            break
        here = [st for st in starts if st.s["window_start_frame"] <= idx <= st.s["window_end_frame"]]
        if not here and idx not in qc_frames:
            continue
        rgb = to_rgb(frame)
        if idx in qc_frames:
            h, w = rgb.shape[:2]
            sc = min(1.0, qc_w / float(w))
            qc_store[idx] = np.asarray(Image.fromarray(rgb).resize((max(1, int(round(w * sc))),
                                                                     max(1, int(round(h * sc)))), Image.BILINEAR))
        for st in here:
            crop = rgb[st.y0:st.y1, st.x0:st.x1]
            score, present, fail, _ = PN.fixed_box_score(crop, P, st.f)
            g = luma_u8(crop)
            th = TM.thumb(g, int(T["thumb_side"]))
            sig = TM.signature32(g)
            if st.prev_thumb is not None and st.prev_thumb.shape == th.shape:
                ad = np.abs(th - st.prev_thumb)
                d = float(ad.mean())
                e = float(np.percentile(ad, 99.5))
                nc = TM.ncc(sig, st.prev_sig)
            else:
                d = e = None
                nc = None
            st.prev_thumb, st.prev_sig = th, sig
            png = st.dir / f"{idx:08d}.png"
            Image.fromarray(g).save(png, compress_level=int(cfg["output"]["png_compress_level"]))
            st.recs.append(dict(fi=idx, pts=p, pts_s=ps, key=key, pict=pict, score=score, present=present,
                                fail=fail, d=d, e=e, ncc=nc, phash=TM.phash64(sig), sig=sig, png=png))
            if st.ocr_regions:
                if st.next_ocr is None:
                    st.next_ocr = ps
                if ps + 1e-9 >= st.next_ocr:
                    for r in st.ocr_regions:
                        bx = r["box"]
                        st.ocr_crops.append((idx, ps, r["id"], r["kind"], luma_u8(rgb[bx[1]:bx[3], bx[0]:bx[2]])))
                    st.next_ocr += ocr_dt
                    while st.next_ocr <= ps:
                        st.next_ocr += ocr_dt
        if idx % 20000 == 0 and idx:
            log(f"  pass B: frame {idx}, t={ps:.1f} s, {time.time() - t0:.0f} s")
    dec.close()
    return active, qc_store, time.time() - t0


# ================================================================================================ clips
def refine_and_split(st, cfg):
    """Refined boundaries and the pieces of one segment: [(list of recs, reason for the piece start)] and a log."""
    s = st.s
    R = st.recs
    T = cfg["timing"]
    if not R:
        return [], dict(note="no frames decoded in the window")
    fis = [r["fi"] for r in R]
    k_first = fis.index(s["first_member_frame"]) if s["first_member_frame"] in fis else 0
    k_last = fis.index(s["last_member_frame"]) if s["last_member_frame"] in fis else len(R) - 1
    k0 = k_first
    while k0 - 1 >= 0 and R[k0 - 1]["present"]:
        k0 -= 1
    k1 = k_last
    while k1 + 1 < len(R) and R[k1 + 1]["present"]:
        k1 += 1
    info = dict(start_frame=R[k0]["fi"], end_frame=R[k1]["fi"], start_pts_s=R[k0]["pts_s"], end_pts_s=R[k1]["pts_s"],
                start_rule=("refined: first frame of the present run ending at the first member sample"
                            if k0 > 0 else "window start: the previous sample already shows the panel by the fixed-box "
                                           "score (or the video starts here)"),
                end_rule=("refined: last frame of the present run starting at the last member sample"
                          if k1 < len(R) - 1 else "window end: the next sample still shows the panel by the "
                                                  "fixed-box score (or the video ends here)"),
                coarse_start_s=s["t_first"], coarse_end_s=s["t_last"])
    core = R[k0:k1 + 1]
    gap_min = int(T["gap_min_frames"])
    pieces, cur, reason = [], [], "segment start"
    cuts, gaps = [], []
    k = 0
    while k < len(core):
        r = core[k]
        if not r["present"]:
            j = k
            while j < len(core) and not core[j]["present"]:
                j += 1
            if j - k >= gap_min:
                gaps.append(dict(from_frame=core[k]["fi"], to_frame=core[j - 1]["fi"], n=j - k,
                                 fail=core[k]["fail"]))
                if cur:
                    pieces.append((cur, reason))
                cur, reason = [], f"after {j - k} frames without the panel ({core[k]['fail']})"
                k = j
                continue
        is_cut = (r["ncc"] is not None and cur and r["ncc"] < float(T["cut_ncc_max"]) and
                  r["d"] is not None and r["d"] >= float(T["cut_min_d"]))
        if is_cut:
            cuts.append(dict(frame=r["fi"], pts_s=r["pts_s"], ncc=r["ncc"], d=r["d"]))
            pieces.append((cur, reason))
            cur, reason = [], f"hard cut (ncc {r['ncc']:.2f}, d {r['d']:.1f})"
        cur.append(r)
        k += 1
    if cur:
        pieces.append((cur, reason))
    info.update(cuts=cuts, gaps=gaps)
    return pieces, info


def piece_duration(recs, fps_med):
    if not recs:
        return 0.0
    return recs[-1]["pts_s"] - recs[0]["pts_s"] + (1.0 / fps_med if fps_med else 0.0)


def label_duplicates(recs, cfg):
    d = [0.0] + [r["d"] if r["d"] is not None else 1e9 for r in recs[1:]]
    key = [r["key"] for r in recs]
    is_dup, info = TM.classify_duplicates(np.array(d), np.array(key), cfg["timing"])
    return is_dup, info


def speed_for_clip(clip, stated, clock_fit_clip, clock_fit_pooled, cfg, container_fps):
    """(speed_factor, verified, evidence, detail). speed_factor = real seconds per second of video
    (d clock / d pts): 2.0 means the video plays twice as fast as reality."""
    Sp = cfg["speed"]
    if clock_fit_clip and clock_fit_clip[0] and clock_fit_clip[0].get("accepted"):
        f = clock_fit_clip[0]
        return f["slope"], True, "ocr_clock", dict(fit=f)
    if clock_fit_pooled and clock_fit_pooled[0] and clock_fit_pooled[0].get("accepted"):
        f = clock_fit_pooled[0]
        return f["slope"], True, "ocr_clock_pooled", dict(fit=f, note="slope pooled over this video's clips "
                                                                       "(within-clip pairs, free intercept per clip)")
    sp = sorted({s["value"] for s in stated if s["kind"] == "speed"})
    if len(sp) == 1:
        return float(sp[0]), True, "stated_speed", dict(statements=[s for s in stated if s["kind"] == "speed"][:3])
    rates = sorted({s["value"] for s in stated if s["kind"] == "rate"})
    cad = clip["acquisition"]
    why = None
    if len(rates) == 1:
        rs = rates[0]
        if cad.get("dup_method") == "otsu-bimodal" and cad.get("images_per_video_s"):
            k = cad["images_per_video_s"] / rs
            basis = "measured image-update rate (duplicates removed) / stated acquisition rate"
        elif (cad.get("dup_method") or "").startswith("every frame") and container_fps and rs <= 1.02 * container_fps:
            k = container_fps / rs
            basis = ("every video frame is a distinct image: container frame rate / stated acquisition rate (each "
                     "acquired image shown once)")
        else:
            k = None
            basis = None
            why = ("stated rate present but the measured cadence cannot be compared with it (no duplicate pattern, and "
                   "the stated rate exceeds the container rate, so frames may subsample the acquired images)")
        if k is not None:
            if Sp["stated_speed_range"][0] <= k <= Sp["stated_speed_range"][1]:
                return float(k), True, "stated_rate", dict(stated_rate=rs, basis=basis,
                                                           statements=[s for s in stated if s["kind"] == "rate"][:3])
            why = f"stated-rate speed {k:.3f} outside stated_speed_range {Sp['stated_speed_range']}"
    elif len(rates) > 1:
        why = f"several stated rates {rates}: not attributable"
    reasons = []
    if clock_fit_clip is not None and clock_fit_clip[1]:
        reasons.append(f"clip clock fit rejected: {clock_fit_clip[1]}")
    if clock_fit_pooled is not None and clock_fit_pooled[1]:
        reasons.append(f"pooled clock fit rejected: {clock_fit_pooled[1]}")
    if why:
        reasons.append(why)
    if not reasons:
        reasons.append("no on-screen clock and no rate or speed stated in the source")
    return 1.0, False, "none", dict(reasons=reasons)


def write_preview(clip_dir, frames, pts_s, cfg):
    lst = clip_dir / "preview_list.txt"
    with open(lst, "w", encoding="utf-8") as fh:
        for k, f in enumerate(frames):
            fh.write(f"file 'images/{f}'\n")
            if k + 1 < len(frames):
                fh.write(f"duration {max(1e-3, pts_s[k + 1] - pts_s[k]):.6f}\n")
            else:
                fh.write(f"duration {max(1e-3, (pts_s[k] - pts_s[k - 1]) if k else 0.04):.6f}\n")
        if frames:
            fh.write(f"file 'images/{frames[-1]}'\n")
    out = clip_dir / "preview.mp4"
    w = int(cfg["output"]["preview_max_width"])
    cmd = [tool_path("ffmpeg"), "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst.name,
           "-fps_mode", "vfr", "-vf", f"scale='if(gt(iw,{w}),{w},trunc(iw/2)*2)':-2", "-c:v", "libx264",
           "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-threads", "1", "-fflags", "+bitexact",
           "-flags:v", "+bitexact", "-map_metadata", "-1", out.name]
    r = subprocess.run(cmd, cwd=str(clip_dir), capture_output=True, text=True, timeout=3600)
    lst.unlink()
    if r.returncode != 0:
        return None, r.stderr[-400:]
    return out, None


# ================================================================================================ run
def run_video(entry, cfg, cfg_sha, overrides, ov_sha, out_root, work_root, log=print, text_cache=None):
    t_start = time.time()
    vid = entry["video_id"]
    out_dir = Path(out_root) / vid
    work = Path(work_root) / vid
    for d in (out_dir, work / "stage"):
        if d.exists():
            shutil.rmtree(d)
    out_dir.mkdir(parents=True)
    (work / "stage").mkdir(parents=True)
    log(f"[{vid}] {entry['relpath']}")
    # ---------------- pass A
    A = pass_a(entry["path"], cfg, entry.get("duration_s"), log)
    probe = entry.get("probe") or {}
    V = probe.get("video", {})
    pts_sum = pts_summary(A["pts_s"], V.get("r_frame_rate"), V.get("avg_frame_rate"),
                          float(cfg["timing"]["vfr_rel_tol"]), float(cfg["timing"]["vfr_frac_min"]))
    fps_med = pts_sum.get("measured_fps") or 30.0
    log(f"  pass A: {len(A['pts'])} frames, {len(A['samples'])} samples, {A['W']}x{A['H']}, "
        f"{A['wall_s']:.0f} s; vfr={pts_sum.get('vfr')}")
    lays, member, segs, applied = make_segments(A, cfg, overrides, vid)
    log(f"  layouts {len(lays)}, segments {len(segs)} ({sum(s['kept'] for s in segs)} kept)")
    # ---------------- QC frame choice
    qc_frames = {}
    nq0, nq1 = cfg["qc"]["frames_per_segment"]
    dropped_budget = int(cfg["qc"]["max_dropped_segments_shown"])
    sidx = {x["i"]: x for x in A["samples"]}
    for s in segs:
        ms = [i for i in LY_member_samples(lays, s)]
        if s["kept"]:
            n = int(np.clip(round(s["coarse_duration_s"] / float(cfg["qc"]["seconds_per_qc_frame"])), nq0, nq1))
        else:
            if dropped_budget <= 0:
                s["qc_samples"] = []
                continue
            dropped_budget -= 1
            n = 2
        pick = sorted(set(np.round(np.linspace(0, len(ms) - 1, min(n, len(ms)))).astype(int).tolist())) if ms else []
        s["qc_samples"] = [ms[k] for k in pick]
        for i in s["qc_samples"]:
            qc_frames[sidx[i]["frame"]] = i
    # overview frames: evenly spaced samples over the whole video, whatever was found
    nov = int(cfg["qc"]["overview_frames"])
    A["overview_samples"] = sorted(set(np.round(np.linspace(0, len(A["samples"]) - 1,
                                                            min(nov, len(A["samples"])))).astype(int).tolist()))
    for i in A["overview_samples"]:
        qc_frames[sidx[i]["frame"]] = i
    # ---------------- OCR discovery
    ocr_regions, ocr_hits = [], []
    O = cfg["ocr"]
    if O["enabled"] and A["probes"]:
        kept_t = [(s["t_first"], s["t_last"]) for s in segs if s["kept"]]
        inside = [i for i in sorted(A["probes"]) if any(a <= sidx[i]["t"] <= b for a, b in kept_t)]
        outside = [i for i in sorted(A["probes"]) if i not in inside]
        nmax = int(O["ocr_probe_frames"])
        chosen = _spread(inside, nmax)
        chosen += _spread(outside, nmax - len(chosen))
        probes = [(sidx[i]["t"], A["probes"][i]) for i in sorted(chosen)]
        try:
            ocr_regions, ocr_hits = OC.discover(probes, O, A["W"], A["H"])
        except Exception as ex:
            log(f"  OCR discovery failed: {ex}")
            ocr_regions = [dict(id="T--", kind="error", accepted=False, box=[0, 0, 0, 0], error=str(ex)[:300])]
        log(f"  OCR: {len(probes)} probes, {len(ocr_hits)} hits, "
            f"{sum(r['accepted'] for r in ocr_regions)} regions accepted")
    A["probes"] = None
    acc_regions = [r for r in ocr_regions if r.get("accepted")]
    # ---------------- pass B
    active, qc_store, tb_wall = pass_b(entry["path"], A, segs, set(qc_frames), acc_regions, cfg, work / "stage", log)
    log(f"  pass B: {sum(len(st.recs) for st in active)} crop frames in {tb_wall:.0f} s")
    # ---------------- pieces, duplicates
    prov = []
    seg_info = {}
    for st in active:
        pieces, info = refine_and_split(st, cfg)
        info["pieces"] = []
        for k, (recs, why) in enumerate(pieces):
            dur = piece_duration(recs, fps_med)
            ok = dur >= float(cfg["timing"]["min_clip_s"])
            info["pieces"].append(dict(k=k, first_frame=recs[0]["fi"], last_frame=recs[-1]["fi"], n=len(recs),
                                       duration_s=dur, start_reason=why, kept=ok,
                                       rule=("kept" if ok else f"dropped: {dur:.2f} s < min_clip_s "
                                                                f"{cfg['timing']['min_clip_s']}")))
            if ok:
                prov.append(dict(seg=st.s, recs=recs, start_reason=why, ocr=st.ocr_crops))
        seg_info[st.s["id"]] = info
    # manual split overrides (times given in the override, applied as stated)
    for o in overrides:
        if o["video"] != vid or o["action"] != "split":
            continue
        cut_t = sorted(float(x) for x in (o.get("values") or {}).get("at_pts_s", []))
        new = []
        for pc in prov:
            if pc["seg"]["id"] != o.get("segment"):
                new.append(pc)
                continue
            parts, cur = [], []
            ts = list(cut_t)
            for r in pc["recs"]:
                if ts and r["pts_s"] >= ts[0] and cur:
                    parts.append(cur)
                    cur = []
                    while ts and r["pts_s"] >= ts[0]:
                        ts.pop(0)
                cur.append(r)
            if cur:
                parts.append(cur)
            for q, part in enumerate(parts):
                new.append(dict(pc, recs=part, start_reason=(pc["start_reason"] if q == 0 else
                                                             f"override split: {o['reason']}"), override=o["reason"]))
            applied.append(o)
        prov = new
    for pc in prov:
        is_dup, dinfo = label_duplicates(pc["recs"], cfg)
        pc["is_dup"] = is_dup
        pc["dup_info"] = dinfo
        upd = np.where(~is_dup)[0]
        dd = [TM_sigdiff(pc["recs"][upd[a]]["sig"], pc["recs"][upd[a - 1]]["sig"]) for a in range(1, len(upd))]
        pc["ref"] = float(np.median(dd)) if dd else None
    # ---------------- replays across the video
    prov.sort(key=lambda pc: (pc["recs"][0]["pts_s"], pc["seg"]["id"]))
    for n, pc in enumerate(prov):
        pc["pid"] = n
    ulist = []
    for pc in prov:
        u = 0
        for k, r in enumerate(pc["recs"]):
            if not pc["is_dup"][k]:
                ulist.append(dict(clip=pc["pid"], u=u, k=k, t=r["pts_s"], phash=r["phash"], sig=r["sig"],
                                  ref=pc["ref"]))
                u += 1
    ulist.sort(key=lambda x: (x["t"], x["clip"], x["u"]))
    replays = TM.find_replays(ulist, cfg["timing"])
    log(f"  replays: {len(replays)} runs")
    rep_mark = {}
    for rn, run in enumerate(replays):
        for (c, u), (oc, ou) in zip(run["replay"], run["original"]):
            rep_mark[(c, u)] = (rn, oc, ou)
    # split provisional clips at replay-run boundaries
    final = []
    for pc in prov:
        u_of_k, u = [], -1
        for k in range(len(pc["recs"])):
            if not pc["is_dup"][k]:
                u += 1
            u_of_k.append(u)
        state = [rep_mark.get((pc["pid"], uu), (None,))[0] for uu in u_of_k]
        cur_k = [0]
        for k in range(1, len(pc["recs"])):
            if state[k] != state[k - 1] and not pc["is_dup"][k]:
                cur_k.append(k)
        cur_k.append(len(pc["recs"]))
        for a, b in zip(cur_k[:-1], cur_k[1:]):
            rn = state[a]
            recs = pc["recs"][a:b]
            dur = piece_duration(recs, fps_med)
            if dur < float(cfg["timing"]["min_clip_s"]):
                seg_info[pc["seg"]["id"]].setdefault("replay_split_dropped", []).append(
                    dict(first_frame=recs[0]["fi"], n=len(recs), duration_s=dur))
                continue
            orig = None
            if rn is not None:
                r0 = replays[rn]
                orig = dict(run=rn, original_clip_pid=r0["original"][0][0], t_original=r0["t_original"],
                            n_images=r0["n"])
            final.append(dict(seg=pc["seg"], recs=recs, is_dup=pc["is_dup"][a:b].copy(), pid=pc["pid"],
                              start_reason=(pc["start_reason"] if a == 0 else
                                            ("replay run starts" if rn is not None else "replay run ends")),
                              replay=orig, ocr=pc["ocr"], override=pc.get("override"),
                              dup_info=pc["dup_info"]))
    final.sort(key=lambda c: (c["recs"][0]["pts_s"], c["seg"]["id"]))
    # clip ids
    per_seg = {}
    for c in final:
        k = per_seg.get(c["seg"]["id"], 0)
        per_seg[c["seg"]["id"]] = k + 1
        c["clip_id"] = f"{vid}__{c['seg']['id']}c{k:02d}"
    pid_to_clip = {}
    for c in final:
        pid_to_clip.setdefault(c["pid"], c["clip_id"])
    # ---------------- OCR readings per clip, speed
    stated, st_info = ST.for_video(entry, Path(text_cache or (Path(work_root) / "source_text")),
                                   allow_fetch=cfg["speed"]["allow_fetch"])
    clock_pts, clock_val, clock_grp = [], [], []
    for n, c in enumerate(final):
        fis = {r["fi"] for r in c["recs"]}
        rd = [x for x in c["ocr"] if x[0] in fis]
        if len(rd) > int(O["ocr_max_per_clip"]):
            sel = np.round(np.linspace(0, len(rd) - 1, int(O["ocr_max_per_clip"]))).astype(int)
            rd = [rd[k] for k in sorted(set(sel.tolist()))]
        c["ocr_reads"] = {}
        for fi, ps, rid, kind, crop in rd:
            try:
                txt, v, lab = OC.read_region(crop, kind, O)
            except Exception as ex:
                txt, v, lab = f"ERR {ex}"[:60], None, None
            c["ocr_reads"].setdefault(fi, {})[kind] = (txt, v)
            if kind == "clock" and v is not None:
                clock_pts.append(ps); clock_val.append(v); clock_grp.append(n)
        c["clock_fit"] = None
        pts_c = [ps for fi, ps, rid, kind, crop in rd if kind == "clock" and c["ocr_reads"][fi]["clock"][1] is not None]
        val_c = [c["ocr_reads"][fi]["clock"][1] for fi, ps, rid, kind, crop in rd
                 if kind == "clock" and c["ocr_reads"][fi]["clock"][1] is not None]
        if any(kind == "clock" for _, _, _, kind, _ in rd):
            c["clock_fit"] = TM.fit_clock(pts_c, val_c, cfg["speed"])
    pooled = TM.fit_clock(clock_pts, clock_val, cfg["speed"], clock_grp) if clock_pts else None
    # ---------------- write clips
    clips_meta = []
    tb = A["time_base"]
    for c in final:
        recs = c["recs"]
        is_dup = c["is_dup"].copy()
        is_dup[0] = False
        pts_s = np.array([r["pts_s"] for r in recs])
        keys = np.array([r["key"] for r in recs])
        cad = TM.cadence(pts_s, is_dup, keys, cfg["timing"])
        cad["dup_method"] = c["dup_info"]["method"]
        cad["dup_threshold"] = c["dup_info"]["threshold"]
        cad["noise_floor"] = c["dup_info"]["noise_floor"]
        cad["dup_bimodal"] = c["dup_info"]["bimodal"]
        cad["keyframe_relabelled"] = c["dup_info"].get("keyframe_relabelled")
        c["acquisition"] = cad
        sub = pts_summary(pts_s, V.get("r_frame_rate"), V.get("avg_frame_rate"),
                          float(cfg["timing"]["vfr_rel_tol"]), float(cfg["timing"]["vfr_frac_min"]))
        spd, ver, ev, det = speed_for_clip(c, stated, c.get("clock_fit"), pooled, cfg, sub.get("measured_fps"))
        cdir = out_dir / c["clip_id"]
        (cdir / "images").mkdir(parents=True)
        names, rows = [], []
        u = -1
        pts0 = recs[0]["pts_s"]
        for k, r in enumerate(recs):
            if not is_dup[k]:
                u += 1
            name = f"{c['clip_id']}_f{k:05d}.png"
            os.replace(r["png"], cdir / "images" / name)
            r["png"] = None
            names.append(name)
            ro = c["ocr_reads"].get(r["fi"], {})
            ck, an = ro.get("clock", (None, None)), ro.get("angle", (None, None))
            rep = ""
            if c["replay"] is not None:
                rep = f"{pid_to_clip.get(c['replay']['original_clip_pid'], '?')}"
            rows.append({"frame_file": name, "clip_frame_index": k, "source_frame_index": r["fi"], "pts": r["pts"],
                         "time_base": tb, "pts_s": f"{r['pts_s']:.6f}", "t_video_s": f"{r['pts_s'] - pts0:.6f}",
                         "real_time_s": f"{(r['pts_s'] - pts0) * spd:.6f}", "key_frame": int(r["key"]),
                         "pict_type": r["pict"], "panel_score": f"{r['score']:.4f}",
                         "panel_present": int(r["present"]),
                         "diff_prev_mean": "" if (k == 0 or r["d"] is None) else f"{r['d']:.4f}",
                         "diff_prev_p995": "" if (k == 0 or r["e"] is None) else f"{r['e']:.3f}",
                         "ncc_prev": "" if (k == 0 or r["ncc"] is None) else f"{r['ncc']:.4f}",
                         "is_duplicate_of_previous": int(is_dup[k]), "image_update_index": u, "replay_of": rep,
                         "phash": f"{r['phash']:016x}", "ocr_clock_text": ck[0] or "",
                         "ocr_clock_s": "" if ck[1] is None else f"{ck[1]:.0f}",
                         "ocr_angle_text": an[0] or "", "ocr_angle_deg": "" if an[1] is None else f"{an[1]:.1f}"})
        with open(cdir / "frames.csv", "w", newline="", encoding="utf-8") as fh:
            wr = csv.DictWriter(fh, fieldnames=FRAME_FIELDS, lineterminator="\n")
            wr.writeheader()
            wr.writerows(rows)
        prev, perr = (None, None)
        if cfg["output"]["preview"]:
            prev, perr = write_preview(cdir, names, pts_s.tolist(), cfg)
        img_files = [cdir / "images" / n for n in names]
        cm = dict(
            clip_id=c["clip_id"], video_id=vid, segment=c["seg"]["id"], layout=c["seg"]["layout"],
            box=c["seg"]["box"], box_convention="[x0, y0, x1, y1) native pixels, x1/y1 exclusive",
            box_source=c["seg"]["box_source"], field_shape=next(L["shape"] for L in lays if L["id"] == c["seg"]["layout"]),
            start_reason=c["start_reason"], n_frames=len(recs), first_source_frame=recs[0]["fi"],
            last_source_frame=recs[-1]["fi"], pts_start_s=float(pts_s[0]), pts_end_s=float(pts_s[-1]),
            duration_pts_s=float(pts_s[-1] - pts_s[0] + (1.0 / sub["measured_fps"] if sub.get("measured_fps") else 0)),
            timing=dict(
                time_base=tb, r_frame_rate=V.get("r_frame_rate"), avg_frame_rate=V.get("avg_frame_rate"),
                measured_fps_median_interval=sub.get("measured_fps"), vfr=sub.get("vfr"),
                irregular_interval_frac=sub.get("irregular_interval_frac"), interval_ms_top=sub.get("interval_ms_top"),
                acquisition=cad,
                images_per_real_s=(cad.get("images_per_video_s") / spd) if cad.get("images_per_video_s") else None,
                speed_factor=spd, speed_factor_definition=("real seconds per second of video (d clock / d pts); 2.0 = "
                                                           "the video plays twice as fast as reality"),
                real_time_s_formula="real_time_s = (pts_s - pts_s[first frame]) * speed_factor",
                video_s_per_real_s=1.0 / spd if spd else None,
                speed_verified=ver, speed_evidence=ev, speed_detail=det,
                real_duration_s=float((pts_s[-1] - pts_s[0]) * spd)),
            liveness=cad.get("liveness"),
            replay=(dict(is_replay=True, of_clip=pid_to_clip.get(c["replay"]["original_clip_pid"]),
                         t_original=c["replay"]["t_original"], n_images=c["replay"]["n_images"])
                    if c["replay"] else dict(is_replay=False)),
            use_for_rates=c["replay"] is None,
            expected=entry.get("expected"), overridden=bool(c["seg"]["overridden"] or c.get("override")),
            override_reasons=list(c["seg"]["override_reasons"]) + ([c["override"]] if c.get("override") else []),
            digest=dict(images_sha256=dir_digest(img_files, cdir / "images"), n_images=len(img_files),
                        frames_csv_sha256=sha256_file(cdir / "frames.csv"),
                        preview_sha256=sha256_file(prev) if prev else None, preview_error=perr),
            files=dict(images=f"{vid}/{c['clip_id']}/images", frames_csv=f"{vid}/{c['clip_id']}/frames.csv",
                       preview=(f"{vid}/{c['clip_id']}/preview.mp4" if prev else None),
                       harness_glob=f"{vid}/{c['clip_id']}/images/{c['clip_id']}_f*.png"),
        )
        dump_json(cm, cdir / "clip.json")
        clips_meta.append(cm)
    # clean staging (frames outside the refined boundaries or dropped pieces)
    shutil.rmtree(work / "stage", ignore_errors=True)
    # ---------------- manifest + QC
    for s in segs:
        s["refinement"] = seg_info.get(s["id"])
        s["clips"] = [c["clip_id"] for c in clips_meta if c["segment"] == s["id"]]
    man = dict(
        video_id=vid, input=dict(relpath=entry["relpath"], sha256=entry.get("sha256"), size=entry["size"],
                                 source=entry["source"], source_id=entry["source_id"]),
        expected=entry.get("expected"), probe=probe, frame_size=[A["W"], A["H"]], time_base=A["time_base"],
        pts=pts_sum, n_interpolated_pts=A["n_interpolated_pts"], n_samples=len(A["samples"]),
        sample_interval_s=A["dt"],
        analysis_factor=PN.analysis_factor(A["W"], A["H"], cfg["sampling"]["analysis_max_side"]),
        layouts=[{k: v for k, v in L.items()} for L in lays], segments=segs,
        ocr=dict(regions=ocr_regions, n_hits=len(ocr_hits), hits=ocr_hits[:60],
                 pooled_clock_fit=(pooled[0] if pooled else None), pooled_clock_reject=(pooled[1] if pooled else None)),
        source_statements=stated, source_info=st_info, replays=[dict(r, replay=[list(x) for x in r["replay"]],
                                                                     original=[list(x) for x in r["original"]])
                                                                for r in replays],
        clips=[c["clip_id"] for c in clips_meta], overrides_applied=applied, config_sha256=cfg_sha,
        overrides_sha256=ov_sha, code=code_identity(), software=software_versions(), run_timestamp=now_iso(),
        wall_time_s=time.time() - t_start, host=os.uname().nodename if hasattr(os, "uname") else None)
    for L in man["layouts"]:
        L["member_samples"] = len(L["member_samples"])
    dump_json(man, out_dir / "video_manifest.json")
    QC.video_report(man, clips_meta, A, segs, lays, member, qc_store, active, cfg, out_dir / "qc")
    log(f"[{vid}] done: {len(clips_meta)} clips in {time.time() - t_start:.0f} s")
    return man, clips_meta


def LY_member_samples(lays, s):
    L = next(L for L in lays if L["id"] == s["layout"])
    return [i for i in L["member_samples"] if s["first_sample"] <= i <= s["last_sample"]]


def TM_sigdiff(a, b):
    return float(np.abs(a.astype(np.float32) - b.astype(np.float32)).mean())


def _spread(items, n):
    if n <= 0 or not items:
        return []
    if len(items) <= n:
        return list(items)
    k = np.round(np.linspace(0, len(items) - 1, n)).astype(int)
    return [items[i] for i in sorted(set(k.tolist()))]
