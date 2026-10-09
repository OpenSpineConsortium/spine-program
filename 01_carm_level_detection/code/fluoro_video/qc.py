# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/qc.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""QC report per video: time series with the chosen boundaries, contact sheets of ORIGINAL frames with the chosen
crop box (solid) and every other candidate (dashed, labelled with its score and the gate that rejected it), the
parameters, and why each segment was kept or dropped."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

C_KEEP = (40, 220, 90)
C_OTHER = (255, 200, 0)
C_REJ = (235, 60, 60)
C_TXT_BG = (0, 0, 0)


def _font(size=12):
    for name in ("DejaVuSans.ttf",):
        try:
            import matplotlib
            p = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / name
            return ImageFont.truetype(str(p), size)
        except Exception:
            pass
    return ImageFont.load_default()


def _dashed_rect(dr, b, col, w=2, dash=6):
    x0, y0, x1, y1 = b
    for (a0, a1, fixed, horiz) in ((x0, x1, y0, True), (x0, x1, y1, True), (y0, y1, x0, False), (y0, y1, x1, False)):
        t = a0
        while t < a1:
            e = min(a1, t + dash)
            if horiz:
                dr.line([(t, fixed), (e, fixed)], fill=col, width=w)
            else:
                dr.line([(fixed, t), (fixed, e)], fill=col, width=w)
            t += 2 * dash


def _save_small(im, path):
    im = im.convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    im.save(path, optimize=True)


def contact_sheet(seg, samples_by_i, qc_store, W, font, cols, tile_w, sample_ids=None):
    """seg: a segment (its box drawn solid, other candidates dashed) or None (the overview: every candidate of
    evenly spaced samples, dashed, with its score or the gate that rejected it)."""
    from .panels import iou
    tiles = []
    for i in (sample_ids if sample_ids is not None else (seg.get("qc_samples") or [])):
        s = samples_by_i[i]
        img = qc_store.get(s["frame"])
        if img is None:
            continue
        sc = img.shape[1] / float(W)
        im = Image.fromarray(img).convert("RGB")
        dr = ImageDraw.Draw(im)
        chosen = seg["box"] if seg is not None else None
        for c in s["cands"]:
            b = [v * sc for v in c["box"]]
            is_chosen_layout = chosen is not None and c["accepted"] and iou(c["box"], chosen) >= 0.5
            if is_chosen_layout:
                continue
            col = C_OTHER if c["accepted"] else C_REJ
            _dashed_rect(dr, b, col, 2)
            lab = f"{c['score']:.2f}" + ("" if c["accepted"] else f" x{c['reject']}")
            dr.rectangle([b[0], b[1], b[0] + 7 * len(lab) + 4, b[1] + 14], fill=C_TXT_BG)
            dr.text((b[0] + 2, b[1] + 1), lab, fill=col, font=font)
        if chosen is not None:
            b = [v * sc for v in chosen]
            dr.rectangle(b, outline=C_KEEP, width=3)
            best = max([c for c in s["cands"] if c["accepted"] and iou(c["box"], chosen) >= 0.5],
                       key=lambda c: c["score"], default=None)
            lab = f"{seg['id']} {seg['layout']}" + (f" {best['score']:.2f}" if best else " (no member)")
            dr.rectangle([b[0], max(0, b[3] - 15), b[0] + 7 * len(lab) + 4, b[3]], fill=C_TXT_BG)
            dr.text((b[0] + 2, max(0, b[3] - 14)), lab, fill=C_KEEP, font=font)
        elif not s["cands"]:
            dr.rectangle([0, 16, 150, 31], fill=C_TXT_BG)
            dr.text((3, 17), "no candidate region", fill=C_REJ, font=font)
        cap = f"t={s['t']:.2f} s  frame {s['frame']}"
        dr.rectangle([0, 0, 7 * len(cap) + 6, 15], fill=C_TXT_BG)
        dr.text((3, 1), cap, fill=(255, 255, 255), font=font)
        r = tile_w / float(im.width)
        tiles.append(im.resize((tile_w, max(1, int(round(im.height * r)))), Image.BILINEAR))
    if not tiles:
        return None
    th = max(t.height for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w + (cols - 1) * 4, rows * th + (rows - 1) * 4), (30, 30, 30))
    for k, t in enumerate(tiles):
        sheet.paste(t, ((k % cols) * (tile_w + 4), (k // cols) * (th + 4)))
    return sheet


def timeseries(man, clips, A, segs, lays, member, active, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    t = np.array([s["t"] for s in A["samples"]])
    fig, ax = plt.subplots(3, 1, figsize=(14, 8.5), sharex=True, gridspec_kw=dict(height_ratios=[3, 1, 3]))
    cols = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for n, L in enumerate(lays):
        mem = member.get(L["id"], {})
        y = np.array([mem[s["i"]][1] if s["i"] in mem else np.nan for s in A["samples"]])
        c = cols[n % len(cols)]
        ax[0].plot(t, y, ".", ms=3, color=c, label=f"{L['id']} {L['box']}")
    for s in segs:
        n = [L["id"] for L in lays].index(s["layout"])
        c = cols[n % len(cols)]
        ref = s.get("refinement") or {}
        a = ref.get("start_pts_s", s["t_first"])
        b = ref.get("end_pts_s", s["t_last"])
        if s["kept"]:
            ax[0].axvspan(a, b, color=c, alpha=0.12)
            ax[0].axvline(a, color=c, lw=0.8)
            ax[0].axvline(b, color=c, lw=0.8, ls="--")
        else:
            ax[0].axvspan(s["t_first"], s["t_last"] + A["dt"], color="grey", alpha=0.15, hatch="//")
    ax[0].set_ylabel("panel score of member candidate")
    ax[0].set_ylim(0, 1.05)
    ax[0].grid(True, alpha=0.3)
    if lays:
        ax[0].legend(fontsize=7, loc="upper right", ncol=2)
    ax[0].set_title(f"{man['video_id']}: sampled panel score (dots), kept segments shaded (solid line = refined start, "
                    f"dashed = refined end), dropped runs hatched", fontsize=9)
    sc = np.array([s["scene_change"] if s["scene_change"] is not None else np.nan for s in A["samples"]])
    ax[1].plot(t, sc, lw=0.6, color="k")
    ax[1].set_ylabel("whole-frame\nchange")
    ax[1].grid(True, alpha=0.3)
    for st in active:
        d = np.array([r["d"] if r["d"] is not None else np.nan for r in st.recs])
        tt = np.array([r["pts_s"] for r in st.recs])
        ax[2].plot(tt, np.maximum(d, 1e-3), lw=0.5, color="0.4")
    for c in clips:
        tr = c["timing"]["acquisition"]
        thr = tr.get("dup_threshold")
        a, b = c["pts_start_s"], c["pts_end_s"]
        col = {"live": "tab:green", "held": "tab:red", "mixed": "tab:orange"}.get(c["liveness"], "tab:blue")
        ax[2].axvspan(a, b, color=col, alpha=0.10)
        if thr:
            ax[2].hlines(thr, a, b, color=col, lw=1)
        if c["replay"]["is_replay"]:
            ax[2].axvspan(a, b, color="purple", alpha=0.15, hatch="xx")
    for s in segs:
        for cu in ((s.get("refinement") or {}).get("cuts") or []):
            ax[2].axvline(cu["pts_s"], color="purple", lw=0.8)
    ax[2].set_yscale("log")
    ax[2].set_ylabel("in-crop change d (grey levels)\nline = duplicate threshold")
    ax[2].set_xlabel("pts (s)")
    ax[2].grid(True, which="both", alpha=0.3)
    ax[2].set_title("clips: green live / orange mixed / red held; purple lines = hard cuts, purple hatch = replay",
                    fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=80)
    plt.close(fig)


def video_report(man, clips, A, segs, lays, member, qc_store, active, cfg, qc_dir):
    qc_dir = Path(qc_dir)
    qc_dir.mkdir(parents=True, exist_ok=True)
    font = _font(11)
    sidx = {s["i"]: s for s in A["samples"]}
    try:
        timeseries(man, clips, A, segs, lays, member, active, qc_dir / "timeseries.png")
        ts_ok = True
    except Exception as ex:          # the report says so rather than failing the run
        ts_ok = f"timeseries failed: {ex}"
    sheets = {}
    ov = contact_sheet(None, sidx, qc_store, A["W"], font, int(cfg["qc"]["columns"]), int(cfg["qc"]["tile_width"]),
                       sample_ids=A.get("overview_samples") or [])
    if ov is not None:
        _save_small(ov, qc_dir / "overview.png")
    for s in segs:
        sh = contact_sheet(s, sidx, qc_store, A["W"], font, int(cfg["qc"]["columns"]), int(cfg["qc"]["tile_width"]))
        if sh is not None:
            p = qc_dir / f"{s['id']}.png"
            _save_small(sh, p)
            sheets[s["id"]] = p.name
    L = []
    L.append(f"# QC: {man['video_id']}\n")
    L.append(f"- input: `{man['input']['relpath']}` sha256 `{man['input']['sha256']}`")
    v = man["probe"].get("video", {})
    L.append(f"- stream: {v.get('codec_name')} {man['frame_size'][0]}x{man['frame_size'][1]}, r_frame_rate "
             f"{v.get('r_frame_rate')}, avg_frame_rate {v.get('avg_frame_rate')}, time base {man['time_base']}")
    p = man["pts"]
    L.append(f"- decoded frames {p.get('n_frames')}, pts span {p.get('pts_span_s', 0):.2f} s, median interval "
             f"{p.get('median_interval_ms', 0):.2f} ms, VFR {p.get('vfr')} (irregular intervals "
             f"{100 * (p.get('irregular_interval_frac') or 0):.1f}%), pts interpolated for "
             f"{man['n_interpolated_pts']} frames")
    L.append(f"- expected (scan doc, video level): region {man['expected'].get('region')}, view "
             f"{man['expected'].get('view')}")
    L.append(f"- config sha256 `{man['config_sha256']}`; code `{man['code']['identity']}`")
    L.append(f"- samples: {man['n_samples']} at {1 / man['sample_interval_s']:.2f} Hz, analysis factor "
             f"1/{man['analysis_factor']}\n")
    L.append("## Parameters\n")
    for sec in ("sampling", "panel", "layout", "timing", "speed", "ocr"):
        items = ", ".join(f"{k}={cfg[sec][k]}" for k in sorted(cfg[sec]) if not isinstance(cfg[sec][k], dict))
        L.append(f"- **{sec}**: {items}")
    L.append(f"- panel score normalisation: {cfg['panel']['score']}\n")
    L.append("## (a) Time series\n")
    L.append("![timeseries](timeseries.png)\n" if ts_ok is True else f"{ts_ok}\n")
    L.append("## Overview: evenly spaced samples, every candidate (dashed; yellow accepted with its score, red "
             "rejected with the gate that failed)\n")
    L.append("![overview](overview.png)\n" if (qc_dir / "overview.png").exists() else "- no overview frames\n")
    L.append("## Layouts\n")
    L.append("| layout | box [x0,y0,x1,y1) | shape | member samples | median abs dev of members (px) |")
    L.append("|---|---|---|---|---|")
    for Ly in man["layouts"]:
        L.append(f"| {Ly['id']} | {Ly['box']} | {Ly['shape']} | {Ly['member_samples']} | "
                 f"{[round(x, 1) for x in Ly['box_mad']]} |")
    L.append("\n## (d) Segments: kept or dropped, and the rule that fired\n")
    L.append("| segment | layout | coarse s | refined s | members / span | decision | clips |")
    L.append("|---|---|---|---|---|---|---|")
    for s in segs:
        ref = s.get("refinement") or {}
        rs = (f"{ref.get('start_pts_s', 0):.3f}-{ref.get('end_pts_s', 0):.3f}" if ref.get("start_pts_s") is not None
              else "-")
        L.append(f"| {s['id']} | {s['layout']} | {s['t_first']:.1f}-{s['t_last']:.1f} | {rs} | "
                 f"{s['n_member_samples']}/{s['n_span_samples']} | {s['rule']} | {', '.join(s.get('clips') or [])} |")
    L.append("")
    for s in segs:
        ref = s.get("refinement") or {}
        if not s["kept"]:
            continue
        L.append(f"### {s['id']} ({s['layout']}, box {s['box']}, {s['box_source']})\n")
        L.append(f"- start: {ref.get('start_rule')}; end: {ref.get('end_rule')}")
        if ref.get("cuts"):
            L.append(f"- hard cuts: " + "; ".join(f"frame {c['frame']} t={c['pts_s']:.3f} ncc {c['ncc']:.2f} "
                                                   f"d {c['d']:.1f}" for c in ref["cuts"]))
        if ref.get("gaps"):
            L.append(f"- gaps without the panel: " + "; ".join(f"frames {g['from_frame']}-{g['to_frame']} "
                                                               f"({g['fail']})" for g in ref["gaps"]))
        for pc in ref.get("pieces") or []:
            L.append(f"- piece {pc['k']}: frames {pc['first_frame']}-{pc['last_frame']} ({pc['duration_s']:.2f} s), "
                     f"start: {pc['start_reason']}; {pc['rule']}")
        if s["id"] in sheets:
            L.append(f"\n![{s['id']}]({sheets[s['id']]})\n")
    dropped = [s for s in segs if not s["kept"] and s["id"] in sheets]
    if dropped:
        L.append("### Dropped segments (first frames shown)\n")
        for s in dropped:
            L.append(f"- {s['id']}: {s['rule']}\n\n![{s['id']}]({sheets[s['id']]})\n")
    L.append("## Clips and timing\n")
    L.append("| clip | frames | pts s | liveness | frames/image (modal) | pattern | interval ms modal / median | "
             "images per video s | speed factor | evidence | replay |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for c in clips:
        tm = c["timing"]
        a = tm["acquisition"]
        L.append(f"| {c['clip_id']} | {c['n_frames']} | {c['duration_pts_s']:.2f} | {c['liveness']} | "
                 f"{a.get('modal_frames_per_image')} | {a.get('repeat_pattern')} | "
                 f"{_f(a.get('modal_interval_ms'))} / {_f(a.get('median_interval_ms'))} | "
                 f"{_f(a.get('images_per_video_s'))} | {tm['speed_factor']:.3f} "
                 f"({'verified' if tm['speed_verified'] else 'unverified'}) | {tm['speed_evidence']} | "
                 f"{c['replay'].get('of_clip') or ''} |")
    L.append("\n## On-screen text (OCR)\n")
    for r in man["ocr"]["regions"]:
        L.append(f"- {r.get('id')} {r.get('kind')} box {r.get('box')} hits {r.get('n_hits')} distinct "
                 f"{r.get('n_distinct')} {'ACCEPTED' if r.get('accepted') else 'rejected'} e.g. {r.get('examples')}")
    if man["ocr"].get("pooled_clock_fit"):
        L.append(f"- pooled clock fit: {man['ocr']['pooled_clock_fit']}; rejection: {man['ocr']['pooled_clock_reject']}")
    L.append("\n## Statements in the source\n")
    for s in man["source_statements"][:20]:
        L.append(f"- {s['kind']} {s['value']} ({s['where']}): \"{s['text'][:160]}\"")
    if not man["source_statements"]:
        L.append("- none found")
    if man["overrides_applied"]:
        L.append("\n## Overrides applied\n")
        for o in man["overrides_applied"]:
            L.append(f"- {o}")
    (qc_dir / "QC.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def _f(x, n=1):
    return "-" if x is None else f"{x:.{n}f}"
