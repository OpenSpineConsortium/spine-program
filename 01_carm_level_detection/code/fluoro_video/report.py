# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/report.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Top-level REPORT.md and manifest.json over every video of a run."""
from __future__ import annotations

import collections
import csv
from pathlib import Path

from .common import code_identity, dump_json, load_json, now_iso, software_versions


def collect(out_root):
    out_root = Path(out_root)
    vids = []
    for vm in sorted(out_root.glob("*/video_manifest.json")):
        m = load_json(vm)
        clips = [load_json(out_root / m["video_id"] / c / "clip.json") for c in m["clips"]]
        vids.append((m, clips))
    return vids


def _f(x, n=2):
    return "-" if x is None else f"{x:.{n}f}"


def build(out_root, cfg, cfg_sha, ov_sha, inventory=None, failures=None):
    out_root = Path(out_root)
    vids = collect(out_root)
    allc = [c for _, cl in vids for c in cl]
    man = dict(tool="tools/fluoro_video", code=code_identity(), config_sha256=cfg_sha, overrides_sha256=ov_sha,
               software=software_versions(), run_timestamp=now_iso(),
               inputs=[dict(video_id=e.get("video_id"), relpath=e["relpath"], include=e.get("include"),
                            rule=e.get("rule"), sha256=e.get("sha256"), size=e["size"])
                       for e in (inventory or [])],
               videos=[], clips=[], failures=failures or [])
    for m, cl in vids:
        man["videos"].append(dict(
            video_id=m["video_id"], input_sha256=m["input"]["sha256"], relpath=m["input"]["relpath"],
            frame_size=m["frame_size"], r_frame_rate=m["probe"]["video"].get("r_frame_rate"),
            avg_frame_rate=m["probe"]["video"].get("avg_frame_rate"), vfr=m["pts"].get("vfr"),
            n_frames=m["pts"].get("n_frames"), n_layouts=len(m["layouts"]), n_segments=len(m["segments"]),
            n_segments_kept=sum(s["kept"] for s in m["segments"]), n_clips=len(cl),
            ocr_regions=[dict(kind=r.get("kind"), box=r.get("box"), accepted=r.get("accepted"))
                         for r in m["ocr"]["regions"]],
            expected=m["expected"], overrides_applied=len(m["overrides_applied"]),
            segments=[dict(id=s["id"], layout=s["layout"], box=s["box"], kept=s["kept"], rule=s["rule"],
                           t_first=s["t_first"], t_last=s["t_last"], overridden=s["overridden"],
                           override_reasons=s["override_reasons"],
                           refined=(dict(start_pts_s=s["refinement"].get("start_pts_s"),
                                         end_pts_s=s["refinement"].get("end_pts_s"),
                                         n_cuts=len(s["refinement"].get("cuts") or []))
                                    if s.get("refinement") and s["refinement"].get("start_pts_s") is not None
                                    else None),
                           clips=s.get("clips")) for s in m["segments"]]))
        for c in cl:
            tm = c["timing"]
            man["clips"].append(dict(
                clip_id=c["clip_id"], video_id=c["video_id"], segment=c["segment"], box=c["box"],
                n_frames=c["n_frames"], pts_start_s=c["pts_start_s"], pts_end_s=c["pts_end_s"],
                duration_pts_s=c["duration_pts_s"], liveness=c["liveness"], replay=c["replay"],
                use_for_rates=c["use_for_rates"], overridden=c["overridden"], override_reasons=c["override_reasons"],
                expected_region=(c.get("expected") or {}).get("region"),
                expected_view=(c.get("expected") or {}).get("view"),
                timing=dict(r_frame_rate=tm["r_frame_rate"], avg_frame_rate=tm["avg_frame_rate"], vfr=tm["vfr"],
                            measured_fps=tm["measured_fps_median_interval"],
                            modal_frames_per_image=tm["acquisition"].get("modal_frames_per_image"),
                            repeat_pattern=tm["acquisition"].get("repeat_pattern"),
                            modal_interval_ms=tm["acquisition"].get("modal_interval_ms"),
                            median_interval_ms=tm["acquisition"].get("median_interval_ms"),
                            images_per_video_s=tm["acquisition"].get("images_per_video_s"),
                            images_per_real_s=tm.get("images_per_real_s"),
                            n_updates=tm["acquisition"].get("n_updates"),
                            n_duplicates=tm["acquisition"].get("n_duplicates"),
                            dup_method=tm["acquisition"].get("dup_method"),
                            noise_floor=tm["acquisition"].get("noise_floor"),
                            speed_factor=tm["speed_factor"], speed_verified=tm["speed_verified"],
                            speed_evidence=tm["speed_evidence"], real_duration_s=tm["real_duration_s"]),
                digest=c["digest"], files=c["files"]))
    dump_json(man, out_root / "manifest.json")
    # CSV of clips
    with open(out_root / "clips.csv", "w", newline="", encoding="utf-8") as fh:
        cols = ["clip_id", "video_id", "segment", "box", "n_frames", "pts_start_s", "duration_pts_s", "liveness",
                "is_replay", "expected_region", "expected_view", "r_frame_rate", "vfr", "modal_frames_per_image",
                "repeat_pattern", "modal_interval_ms", "median_interval_ms", "images_per_video_s", "speed_factor",
                "speed_verified", "speed_evidence", "images_per_real_s", "images_sha256"]
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for c in man["clips"]:
            t = c["timing"]
            w.writerow([c["clip_id"], c["video_id"], c["segment"], " ".join(map(str, c["box"])), c["n_frames"],
                        f"{c['pts_start_s']:.3f}", f"{c['duration_pts_s']:.3f}", c["liveness"],
                        int(c["replay"]["is_replay"]), c["expected_region"], c["expected_view"], t["r_frame_rate"],
                        t["vfr"], t["modal_frames_per_image"], t["repeat_pattern"], _f(t["modal_interval_ms"]),
                        _f(t["median_interval_ms"]), _f(t["images_per_video_s"]), _f(t["speed_factor"], 3),
                        t["speed_verified"], t["speed_evidence"], _f(t["images_per_real_s"]),
                        c["digest"]["images_sha256"]])
    # REPORT.md
    L = ["# Fluoroscopy clip extraction: report\n"]
    L.append(f"- run {man['run_timestamp']}; code `{man['code']['identity']}`; config sha256 `{cfg_sha}`; "
             f"overrides sha256 `{ov_sha}`")
    sw = man["software"]
    L.append(f"- software: python {sw.get('python')}, numpy {sw.get('numpy')}, scipy {sw.get('scipy')}, PyAV "
             f"{sw.get('av')}, Pillow {sw.get('PIL')}, {sw.get('ffmpeg')}, {sw.get('tesseract')}")
    inc = [e for e in man["inputs"] if e["include"]]
    L.append(f"- inputs: {len(man['inputs'])} files scanned, {len(inc)} videos; {len(man['videos'])} processed; "
             f"{len(man['failures'])} failed")
    tot_frames = sum(c["n_frames"] for c in man["clips"])
    L.append(f"- clips: {len(man['clips'])}, frames {tot_frames}, pts seconds "
             f"{sum(c['duration_pts_s'] for c in man['clips']):.1f}; replays {sum(c['replay']['is_replay'] for c in man['clips'])}; "
             f"overridden {sum(c['overridden'] for c in man['clips'])}\n")
    L.append("Speed factor = real seconds per second of video (d clock / d pts); real_time_s = (pts_s - pts_s0) x "
             "speed_factor. `none` evidence means speed 1.0 assumed and unverified.\n")
    L.append("## Totals\n")
    for key, lab in (("liveness", "liveness"), ("expected_region", "expected region (scan doc, video level)"),
                     ("expected_view", "expected view (scan doc, video level)")):
        cnt = collections.Counter(c[key] for c in man["clips"])
        fr = collections.Counter()
        for c in man["clips"]:
            fr[c[key]] += c["n_frames"]
        L.append(f"**By {lab}**: " + "; ".join(f"{k}: {cnt[k]} clips / {fr[k]} frames" for k in sorted(cnt, key=str)))
        L.append("")
    cross = collections.Counter((c["expected_region"], c["expected_view"], c["liveness"]) for c in man["clips"])
    L.append("| expected region | expected view | liveness | clips |")
    L.append("|---|---|---|---|")
    for (r, v, lv), n in sorted(cross.items(), key=lambda kv: tuple(map(str, kv[0]))):
        L.append(f"| {r} | {v} | {lv} | {n} |")
    ev = collections.Counter(c["timing"]["speed_evidence"] for c in man["clips"])
    L.append(f"\n**Speed evidence**: " + "; ".join(f"{k}: {n}" for k, n in sorted(ev.items())))
    L.append("\n## Per video\n")
    L.append("| video | frames | fps (r / avg) | VFR | layouts | segments kept / all | clips | live / mixed / held | "
             "OCR regions | QC |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for v in man["videos"]:
        cl = [c for c in man["clips"] if c["video_id"] == v["video_id"]]
        lv = collections.Counter(c["liveness"] for c in cl)
        ocr = sum(1 for r in v["ocr_regions"] if r["accepted"])
        L.append(f"| {v['video_id']} | {v['n_frames']} | {v['r_frame_rate']} / {v['avg_frame_rate']} | {v['vfr']} | "
                 f"{v['n_layouts']} | {v['n_segments_kept']} / {v['n_segments']} | {v['n_clips']} | "
                 f"{lv.get('live', 0)} / {lv.get('mixed', 0)} / {lv.get('held', 0)} | {ocr} | "
                 f"[QC]({v['video_id']}/qc/QC.md) |")
    L.append("\n## Per clip timing\n")
    L.append("| clip | frames | pts s | live | r_frame_rate | VFR | frames/image | pattern | interval ms (modal / "
             "median) | images per video s | speed | evidence | images per real s | replay of |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for c in man["clips"]:
        t = c["timing"]
        L.append(f"| {c['clip_id']} | {c['n_frames']} | {c['duration_pts_s']:.2f} | {c['liveness']} | "
                 f"{t['r_frame_rate']} | {t['vfr']} | {t['modal_frames_per_image']} | {t['repeat_pattern']} | "
                 f"{_f(t['modal_interval_ms'], 1)} / {_f(t['median_interval_ms'], 1)} | "
                 f"{_f(t['images_per_video_s'])} | {t['speed_factor']:.3f} | {t['speed_evidence']} | "
                 f"{_f(t['images_per_real_s'])} | {c['replay'].get('of_clip') or ''} |")
    ov = [c for c in man["clips"] if c["overridden"]]
    L.append("\n## Overrides\n")
    L.append("\n".join(f"- {c['clip_id']}: {c['override_reasons']}" for c in ov) if ov else "- none")
    if man["failures"]:
        L.append("\n## Failures\n")
        for f in man["failures"]:
            L.append(f"- {f}")
    L.append("\n## Inputs excluded by rule\n")
    for e in man["inputs"]:
        if not e["include"]:
            L.append(f"- `{e['relpath']}`: {e['rule']}")
    (out_root / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return man


def export_small(out_root, dest, max_w=1000):
    """REPORT.md, manifest.json, clips.csv and every video's QC.md + QC PNGs (downsized, 128 colours) into dest:
    small derived thumbnails only, never frames or clips."""
    from PIL import Image
    import shutil
    out_root, dest = Path(out_root), Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for f in ("REPORT.md", "manifest.json", "clips.csv"):
        if (out_root / f).exists():
            shutil.copy2(out_root / f, dest / f)
    n = 0
    for qc in sorted(out_root.glob("*/qc")):
        vd = dest / qc.parent.name / "qc"
        vd.mkdir(parents=True, exist_ok=True)
        if (qc / "QC.md").exists():
            shutil.copy2(qc / "QC.md", vd / "QC.md")
        for p in sorted(qc.glob("*.png")):
            im = Image.open(p).convert("RGB")
            if im.width > max_w:
                im = im.resize((max_w, int(round(im.height * max_w / im.width))), Image.BILINEAR)
            im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(vd / p.name,
                                                                                                  optimize=True)
            n += 1
    return n
