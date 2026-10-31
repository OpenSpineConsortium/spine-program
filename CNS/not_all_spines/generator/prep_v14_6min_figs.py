"""paper/cns2026/prep_v14_6min_figs.py -- figures for the 6-minute cut of the CNS 2026 talk (deck v14_6min, 2026-10-31).

Stays out of git: this folder is excluded in .git/info/exclude of the public repository. Nothing is written outside
figs_v14_6min/. The spine-program scripts and the spine-detector code are imported read-only, with bytecode off.

  pic_abc.png        NeurIPS 2026 Figure 1 (token 215): its own three panels cropped out at native pixels, lateral fat
                     trimmed, ordered A CT, B segmenter output, C ground truth, white letters at bottom left.
  render_l6.png      MDPA Figure 2(d), six lumbar bodies: the current fig_anchors.pdf rasterised, panel (d) only.
  benzel_fig1_1.png, benzel_fig1_9.png  Benzel Figs 1.1 and 1.9, the images embedded in the chapter PDF, untouched (no
                     redraw, no resample): the two textbook plots the next two slides answer.
  violin_endplate.png  plot_thoracolumbar_violins.violins (left panel only) with the type raised, level_gradients.csv,
                     the article's plausibility gate, Panjabi interval = mean +/- 1.96 x sem x sqrt(12). L5 withheld.
  atlas_canal.png    make_levelatlas_fig panel (b), canal width and depth, built from its own draw functions, type raised.
  spinopelvic.png    make_figures.fig_validation's three panels, same kde, same reference lines, type raised; Table III
                     values in each panel head.
  closing.png        masked CT in, vertebrae out: outcome pictures only, no number, no method.

    python paper/cns2026/prep_v14_6min_figs.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True      # never leave __pycache__ in spine-program or spine-detector

import fitz
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DESK = ROOT.parent
OUT = HERE / "figs_v14_6min"
OUT.mkdir(exist_ok=True)
SN = DESK / "spinesurg-ct-nnunet" / "SchwingNet"
MPDA = ROOT / "paper" / "mpda"
SPSCRIPTS = DESK / "spine-program" / "03_ctspinopelvic1k_dataset" / "mdpa" / "scripts"
MORPH = ROOT / "morphometrics"

NAVY, GOLD, RED, GREY = "#191D63", "#FFC42F", "#EF4627", "#7A7A7A"
BOLD = r"C:\Windows\Fonts\arialbd.ttf"
# a slide figure is drawn at the size it is shown (10.15 M EMU = 11.1 in wide), so a point here is a point on the slide
W_IN, H_IN, DPI = 11.1, 4.19, 170
LEVELS = ["T11", "T12", "L1", "L2", "L3", "L4", "L5"]

atlas = {(r["measure"], r["level"]): r for r in csv.DictReader(open(MORPH / "level_atlas.csv"))}


# ------------------------------------------------------------------ 1. the three-panel picture
def pic_abc():
    src = ROOT / "CAMERA_READY_NEURIPS" / "src" / "figs" / "lstv_lumbarization_215_spine_only.png"
    im = Image.open(src).convert("RGB")
    assert im.size == (1969, 1000), im.size
    boxes = {"CT": (11, 125, 649, 874), "GT": (666, 125, 1304, 874), "TS": (1320, 125, 1958, 874)}
    x0, x1 = 50, 598                         # inside each panel: ribs kept, lateral fat trimmed
    order = [("A", "CT"), ("B", "TS"), ("C", "GT")]   # the picture Greg pasted: CT, segmenter, truth
    gut = 10
    w, h = x1 - x0, 749
    out = Image.new("RGB", (3 * w + 2 * gut, h), "white")
    f = ImageFont.truetype(BOLD, 58)
    for i, (letter, key) in enumerate(order):
        b = boxes[key]
        p = im.crop((b[0] + x0, b[1], b[0] + x1, b[3]))
        d = ImageDraw.Draw(p)
        d.text((16, h - 78), letter, fill="white", font=f)
        out.paste(p, (i * (w + gut), 0))
    out.save(OUT / "pic_abc.png", optimize=True)
    print("pic_abc", out.size, round(out.size[0] / out.size[1], 3))


# ------------------------------------------------------------------ 2. the 3-D view: MDPA Fig. 2(d)
def render_l6():
    d = fitz.open(MPDA / "figures" / "fig_anchors.pdf")
    p = d[0]
    t = p.get_text()
    assert "(d) six lumbar bodies, Castellvi IV" in t
    panel = fitz.Rect(449.0, 11.7, 559.0, 125.9)    # panel (d), spine and pelvis, side margins trimmed
    pix = p.get_pixmap(dpi=500, clip=panel)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    # the panel's own off-white background is kept; the slide is white
    if im.size[0] > 1000:
        s = 1000 / im.size[0]
        im = im.resize((1000, int(im.size[1] * s)), Image.LANCZOS)
    im.save(OUT / "render_l6.png", optimize=True)
    print("render_l6", im.size, round(im.size[0] / im.size[1], 3))


# ------------------------------------------------------------------ 3. Benzel Fig. 1.1, the embedded image itself
def benzel():
    d = fitz.open(ROOT / "MANUAL_REFS" / "BENZEL_CH_1.pdf")
    for page, cap, name, size in ((1, "Fig. 1.1 Vertebral body diameter versus spinal level.", "benzel_fig1_1.png", (495, 451)),
                                  (5, "Fig. 1.9 Spinal canal diameter versus spinal level.", "benzel_fig1_9.png", (495, 447))):
        p = d[page]
        assert cap in " ".join(p.get_text().split()), cap
        rects = [(x[0], p.get_image_rects(x[0])[0]) for x in p.get_images(full=True)]
        xref = min(rects, key=lambda r: (round(r[1].y0, -1), r[1].x0))[0]     # upper left of the page
        pix = fitz.Pixmap(d, xref)
        assert (pix.width, pix.height) == size, (pix.width, pix.height)
        pix.save(OUT / name)
        print(name, pix.width, pix.height)


# ------------------------------------------------------------------ 4. the violins, left panel of the talk figure
def violin():
    sys.path.insert(0, str(SPSCRIPTS))
    import plot_thoracolumbar_violins as VT
    VT.DATA = str(MORPH)                              # this repository's tables, never the copy
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial"], "font.size": 20,
                         "axes.titlesize": 20, "axes.labelsize": 20, "xtick.labelsize": 20, "ytick.labelsize": 20})
    column, xlabel = VT.MEASURES["endplate"]
    vals = VT.read_values(column)
    # the article's plausibility window (levelatlas.GATES), so this plot and Figure 3(a) describe the same records
    lo, hi = 20.0, 90.0
    vals = {k: v[(v >= lo) & (v <= hi)] for k, v in vals.items()}
    vals.pop("L5", None)                              # withheld: the transverse processes fall in front of the cut
    for lv, v in vals.items():
        a = atlas[("endplate", lv)]
        assert len(v) == int(a["n"]) and abs(float(np.median(v)) - float(a["median"])) < 0.051, (lv, len(v), a)
    refs = VT.read_panjabi("endplate")
    assert abs(refs["L1"][1] - 1.03 * math.sqrt(12)) < 1e-9        # SEM x sqrt(12), not the SEM
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax = fig.add_axes([0.062, 0.165, 0.925, 0.705])
    ys = VT.violins(ax, vals, "#4878a8", "Upper end-plate width (mm)", "")
    ax.set_title("")
    for lev, pos in zip(LEVELS, ys):
        if lev in refs and len(vals.get(lev, [])) > 1:
            m, sd = refs[lev]
            ax.plot([m - VT.REF_K * sd, m + VT.REF_K * sd], [pos + 0.44] * 2, color="#b2182b", linewidth=4.0,
                    solid_capstyle="butt", zorder=5)
            ax.plot([m], [pos + 0.44], marker="|", color="#b2182b", markersize=15, markeredgewidth=3.5, zorder=6)
    ax.text(0.5, ys[LEVELS.index("L5")], "L5 withheld: transverse processes fall in front of the body cut",
            transform=ax.get_yaxis_transform(), ha="center", va="center", fontsize=18, style="italic", color="0.3")
    ax.set_xlim(19, 72)
    ax.tick_params(axis="y", length=0, pad=8)
    fig.legend(handles=[Patch(facecolor="#4878a8", alpha=0.75, edgecolor="black", label="This dataset, 802 patients"),
                        Line2D([0], [0], color="#b2182b", linewidth=4.0,
                               label="Panjabi 1992, mean $\\pm$ 1.96 SD ($n$ = 12)")],
               loc="upper center", ncol=2, fontsize=19, frameon=False, bbox_to_anchor=(0.53, 1.03), columnspacing=2.5)
    fig.savefig(OUT / "violin_endplate.png", dpi=DPI)
    plt.close(fig)
    meds = {lv: float(atlas[("endplate", lv)]["median"]) for lv in ("L1", "L2", "L3", "L4")}
    gap = max(abs(meds[lv] - refs[lv][0]) for lv in meds)
    print("violin_endplate n", {k: len(v) for k, v in vals.items()}, "max |median-Panjabi| L1-L4", round(gap, 2))
    return {"n_min": min(len(v) for v in vals.values()), "n_max": max(len(v) for v in vals.values()), "gap": gap,
            "panjabi": {k: refs[k][0] for k in meds}}


# ------------------------------------------------------------------ 5. the canal panel of the level atlas
def atlas_canal():
    sys.path.insert(0, str(MPDA))
    import make_figures as MF
    import make_levelatlas_fig as LA
    from levelatlas import GATES, annotate_n, draw, series   # noqa: F401
    assert LA.MF is MF
    plt.rcParams.update({"font.size": 20, "axes.titlesize": 20, "axes.labelsize": 20, "xtick.labelsize": 20,
                         "ytick.labelsize": 20, "legend.fontsize": 18, "figure.dpi": 100, "savefig.dpi": DPI,
                         "savefig.bbox": None, "axes.linewidth": 1.4})
    lg, sm = MF.load("level_gradients.csv"), MF.load("surgical_morphometrics.csv")
    refs, labels, spread = LA.load_reference_series()
    styles = LA._style_table({ser for d in refs.values() for ser in d})
    S_w = series(lg, "canal_width_{l}_mm", GATES["canal_w"])
    S_d = series(sm, "canal_ap_mm_{l}", GATES["canal_ap"])
    for key, S in (("canal_w", S_w), ("canal_ap", S_d)):
        for lv, s in S.items():
            a = atlas[(key, lv)]
            assert s["n"] == int(a["n"]) and abs(s["med"] - float(a["median"])) < 0.051, (key, lv, s["n"], a)
    y_of = {lv: -i for i, lv in enumerate(LEVELS)}
    fig = plt.figure(figsize=(W_IN, H_IN))
    ax = fig.add_axes([0.062, 0.165, 0.925, 0.72])
    TEAL, INK = MF.TEAL, MF.INK
    draw(ax, S_w, y_of, TEAL, "o", offset=+0.2, label="width", lw=3.4)
    draw(ax, S_d, y_of, INK, "^", offset=-0.2, label="depth", lw=3.4)
    for ln in ax.lines:
        if ln.get_marker() in ("o", "^"):
            ln.set_markersize(11); ln.set_markeredgewidth(2.2)
    drawn = {}
    LA.draw_reference_band(ax, spread, refs, "canal_w", y_of, offset=+0.2)
    LA.draw_reference_series(ax, refs, "canal_w", y_of, styles, labels, offset=+0.2, drawn=drawn)
    LA.draw_reference_band(ax, spread, refs, "canal_ap", y_of, offset=-0.2)
    LA.draw_reference_series(ax, refs, "canal_ap", y_of, styles, labels, offset=-0.2, drawn=drawn)
    for ln in ax.lines:
        if ln.get_marker() in ("None", "none", None, "") and ln.get_color() == "#000000":
            ln.set_linewidth(2.4)
    ax.set_xlabel("Spinal canal (mm)")
    MF.mp_ticks(ax)
    ax.set_yticks([y_of[l] for l in LEVELS]); ax.set_yticklabels(LEVELS)
    ax.set_ylim(-len(LEVELS) + 0.4, 0.6)
    ax.grid(axis="both", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="y", which="minor", left=False)
    ax.tick_params(axis="y", length=0, pad=8)
    fig.legend(handles=[Line2D([0], [0], color=TEAL, marker="o", mfc="white", ms=11, mew=2.2, lw=3.4, label="width"),
                        Line2D([0], [0], color=INK, marker="^", mfc="white", ms=11, mew=2.2, lw=3.4, label="depth"),
                        Line2D([], [], color=MF.INK, lw=2.4, label="Panjabi mean ($n$ = 12)"),
                        Patch(facecolor="#000000", alpha=0.085, lw=0, label="$\\pm$ 1.96 SD")],
               loc="upper center", ncol=4, fontsize=19, frameon=False, bbox_to_anchor=(0.53, 1.015), columnspacing=2.0,
               handlelength=1.6)
    fig.savefig(OUT / "atlas_canal.png", dpi=DPI)
    plt.close(fig)
    print("atlas_canal n width", S_w["L3"]["n"], "depth", S_d["L3"]["n"])
    inside = {}
    for key, S in (("canal_w", S_w), ("canal_ap", S_d)):
        for lv, st in S.items():
            m = refs[key]["Panjabi 1992"].get(lv); sd = spread[key]["Panjabi 1992"].get(lv, (None,))[0]
            if m is not None and sd is not None:
                inside[f"{key}_{lv}"] = bool(m - 1.96 * sd <= st["med"] <= m + 1.96 * sd)
    return {"n_min": min(s["n"] for S in (S_w, S_d) for s in S.values()),
            "n_max": max(s["n"] for S in (S_w, S_d) for s in S.values()),
            "depth_median": [min(s["med"] for s in S_d.values()), max(s["med"] for s in S_d.values())],
            "width_median": [min(s["med"] for s in S_w.values()), max(s["med"] for s in S_w.values())],
            "inside_panjabi_interval": inside}


# ------------------------------------------------------------------ 6. the spinopelvic angles (MDPA Fig. S2, Table III)
def spinopelvic():
    import make_figures as MF
    plt.rcParams.update({"font.size": 19, "axes.titlesize": 20, "axes.labelsize": 19, "xtick.labelsize": 18,
                         "ytick.labelsize": 18, "figure.dpi": 100, "xtick.minor.visible": False,
                         "ytick.minor.visible": False})
    rows = [r for r in MF.load("surgical_morphometrics.csv") if (r.get("s1_plate_rejected") or "0") in ("", "0")]
    fig = plt.figure(figsize=(W_IN, H_IN))
    table = {}
    spec = [("pelvic_incidence_deg", "Pelvic incidence", 20, 90, 55.0, 10.6, 52.1, "52.1", "53.4"),
            ("sacral_slope_deg", "Sacral slope", 10, 70, 41.0, 8.4, 36.5, "36.5", "34.1"),
            ("pelvic_tilt_deg", "Pelvic tilt", -10, 45, 13.0, 6.0, 15.6, "15.6", "19.2")]
    for i, (key, title, lo, hi, ref, sd, ct, vei, has) in enumerate(spec):
        allv = MF.col(rows, key)
        table[key] = (len(allv), round(float(allv.mean()), 1), round(float(allv.std(ddof=1)), 1))
        v = MF.col(rows, key, lo, hi)
        xs, ys = MF.kde(v, lo, hi, bw=1.0)
        ax = fig.add_axes([0.012 + i * 0.3315, 0.195, 0.308, 0.535])
        ax.axvspan(ref - sd, ref + sd, color=MF.OCHRE, alpha=0.13, lw=0)
        ax.axvline(ref, color=MF.OCHRE, ls="--", lw=2.4)
        ax.axvline(ct, color=MF.INK, ls=(0, (1.4, 1.2)), lw=2.6)
        ax.fill_between(xs, ys, color=MF.TEAL, alpha=0.18, lw=0)
        ax.plot(xs, ys, color=MF.TEAL, lw=3.0)
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}°"))
        ax.set_yticks([])
        ax.set_ylim(0, ys.max() * 1.08)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="x", lw=0.8)
        ax.set_axisbelow(True)
        n, mean, s = table[key]
        fig.text(0.012 + i * 0.3315, 0.965, title, fontsize=21, fontweight="bold", color=NAVY, va="top")
        fig.text(0.012 + i * 0.3315, 0.875, f"{mean:.1f} ± {s:.1f}° here", fontsize=19, color=MF.TEAL, va="top",
                 fontweight="bold")
        fig.text(0.012 + i * 0.3315, 0.80, f"Veilleux {vei}, Hasegawa {has}", fontsize=17, color=MF.INK, va="top")
    fig.legend(handles=[Line2D([], [], color=MF.TEAL, lw=3.0, label="this dataset"),
                        Line2D([], [], color=MF.INK, ls=(0, (1.4, 1.2)), lw=2.6, label="supine CT, Veilleux 2020"),
                        Line2D([], [], color=MF.OCHRE, ls="--", lw=2.4, label="standing film, Vialle 2005")],
               loc="lower center", ncol=3, frameon=False, fontsize=18, bbox_to_anchor=(0.5, -0.03), columnspacing=2.5,
               handlelength=1.8)
    fig.savefig(OUT / "spinopelvic.png", dpi=DPI)
    plt.close(fig)
    print("spinopelvic", table)
    return table


# ------------------------------------------------------------------ 7. the closing picture
SCALE = 1.0
LABEL_RGB = {20: (51, 102, 242), 21: (26, 160, 242), 22: (26, 217, 140), 23: (217, 217, 26), 24: (242, 140, 26),
             25: (242, 51, 51), 26: (217, 77, 217), 19: (200, 200, 200)}


def masked_ct(h):
    """The labelled slice of record 0244 (SchwingNet Figure 1a, public CT), its release labels painted on."""
    pan = SN / "results" / "figure1" / "panels"
    im = np.asarray(Image.open(pan / "l6_0244_slice.png").convert("RGB")).astype(np.float32)
    lab = np.load(pan / "l6_0244_slice_labels.npz")["labels"]
    assert im.shape[:2] == lab.shape and 25 in lab                      # L6 is in the slice
    for k, rgb in LABEL_RGB.items():
        m = lab == k
        im[m] = im[m] * 0.45 + np.array(rgb, np.float32) * 0.55
    out = Image.fromarray(im.clip(0, 255).astype(np.uint8))
    return out.resize((round(out.width * h / out.height), h), Image.LANCZOS)


def detected(h):
    """The deployed detector on the projection of the same CT, exactly as spine-detector/src/render_prediction.py
    decodes it (letterbox, conf 0.25, NMS 0.7). Outlines only: no rank, no score."""
    sys.path.insert(0, str(DESK / "spine-detector" / "src"))
    import onnxruntime as ort
    import render_prediction as RP
    src = SN / "results" / "figure1" / "panels" / "l6_0244_drr.png"
    im = Image.open(src)
    sess = ort.InferenceSession(str(DESK / "spine-detector" / "dist" / "v11m_1024_v4_fp16.onnx"),
                                providers=["CPUExecutionProvider"])
    RP.IMG = int(sess.get_inputs()[0].shape[2])
    x, m = RP.letterbox(im)
    raw = sess.run(None, {sess.get_inputs()[0].name: x})[0]
    det = RP.decode(raw)
    nk = (raw.shape[1] - 5) // 3
    kp = det[:, 5:].reshape(len(det), nk, 3)
    corners = RP.unmap(kp[:, :, :2], m)
    assert len(det) == 8, len(det)
    canvas = im.convert("RGB")
    s = h / canvas.height
    canvas = canvas.resize((round(canvas.width * s), h), Image.LANCZOS)
    d = ImageDraw.Draw(canvas)
    for q in corners:
        pts = [(float(p[0]) * s, float(p[1]) * s) for p in q]
        d.line(pts + [pts[0]], fill=(0, 230, 120), width=5, joint="curve")
    json.dump({"model": "spine-detector/dist/v11m_1024_v4_fp16.onnx", "input": str(src.name), "conf": 0.25, "iou": 0.7,
               "n": int(len(det)), "scores": [round(float(c), 3) for c in det[:, 4]]},
              open(OUT / "detected_0244.json", "w"), indent=1)
    return canvas


def tiles(size, gap):
    """Six vertebrae with the level the model gave each. The crops come from CT projections only (ctsp_drr; verse_drr
    for L6); the name printed is the model's output for that crop and is asserted equal to the truth."""
    z = np.load(SN / "results" / "figure2" / "occlusion_clean" / "gradcam.npz", allow_pickle=True)
    js = json.load(open(SN / "results" / "figure2" / "occlusion_clean" / "gradcam_summary.json"))["sets"]["v9_val"]["per_level"]
    f = ImageFont.truetype(BOLD, 44)
    levels = ["T12", "L3", "L4", "L5", "L6", "sacrum"]
    out = Image.new("RGB", (2 * size + gap, 3 * size + 2 * gap), "white")
    rec = {}
    for i, lev in enumerate(levels):
        info = js[lev]
        # of the ten crops, those the model read right; of those, the one on which the anatomy can be seen: the highest
        # contrast of the smoothed image inside the target box, the rule of fig_learning.legible_crop. The file's own
        # representative crop of L3 is one the model misread as L4, which is why the name printed is read from `pred`
        # and never assumed. tiles.json keeps the tally of the ten for the report.
        from scipy.ndimage import gaussian_filter
        right = [i_ for i_, p_ in enumerate(info["pred"]) if p_ == lev]
        imgs_, mks_ = z[f"v9_val__{lev}__img"], z[f"v9_val__{lev}__marker"]

        def legible(i_):
            ys_, xs_ = np.where(mks_[i_] > 127)
            box = gaussian_filter(imgs_[i_].astype(np.float32), 3)[ys_.min():ys_.max() + 1, xs_.min():xs_.max() + 1]
            return float(box.std())
        rep = max(right, key=legible)
        assert info["pred"][rep] == lev, (lev, info["pred"][rep])
        assert info["sources"][rep] in ("ctsp_drr", "verse_drr"), info["sources"][rep]
        rec[lev] = {"source": info["sources"][rep], "pred": info["pred"][rep], "crop": rep,
                    "right_of_ten": sum(p == lev for p in info["pred"])}
        a = z[f"v9_val__{lev}__img"][rep].astype(np.uint8)
        mk = z[f"v9_val__{lev}__marker"][rep]
        im = Image.fromarray(a).convert("RGB").resize((size, size), Image.LANCZOS)
        ys, xs = np.where(mk > 0)
        d = ImageDraw.Draw(im)
        k = size / mk.shape[0]
        d.rectangle([xs.min() * k, ys.min() * k, xs.max() * k, ys.max() * k], outline=(0, 230, 120), width=4)
        name = "sacrum" if lev == "sacrum" else lev
        tw = d.textlength(name, font=f)
        d.rectangle([0, 0, tw + 24, 58], fill=(0x19, 0x1D, 0x63))
        d.text((12, 5), name, fill="white", font=f)
        r, c = divmod(i, 2)
        out.paste(im, (c * (size + gap), r * (size + gap)))
    json.dump(rec, open(OUT / "tiles.json", "w"), indent=1)
    return out


def level_map(w, h):
    """The level map of the SchwingNet manuscript's Figure 2a, colour rule from tools/figure2.py and prep_v14_figs.py,
    restricted to vertebrae from CT projections: the film, C-arm and device-rendered sets are not drawn at all."""
    mp = np.load(SN / "results" / "figure2" / "figure2_map.npz", allow_pickle=True)
    T, y, g, src = mp["tsne"], mp["y"].astype(int), mp["group"].astype(str), mp["source"].astype(str)
    classes = list(mp["classes"].astype(str))
    keep = (g == "validation") & np.isin(src, ["ctsp_drr", "verse_drr", "physics_drr", "physics_rare"])
    HUE = {"cervical": "#2a78d6", "thoracic": "#eb6834", "lumbar": "#1baf7a"}

    def region(n):
        return "cervical" if n.startswith("C") else "thoracic" if n.startswith("T") else "lumbar" if n.startswith("L") else "sacrum"

    def level_colour(name):
        if name == "sacrum":
            return to_rgb("#52514e")
        reg = region(name); base = np.array(to_rgb(HUE[reg]))
        members = [c for c in classes if region(c) == reg]
        t = members.index(name) / max(len(members) - 1, 1)
        col = base + (1.0 - base) * 0.40 * max(0.5 - t, 0.0) * 2.0
        col = col * (1.0 - 0.40 * max(t - 0.5, 0.0) * 2.0)
        return tuple(np.clip(col, 0, 1))

    cols = np.array([level_colour(c) for c in classes])
    L6 = classes.index("L6")
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial"]})
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    o = np.random.default_rng(0).permutation(np.where(keep & (y != L6))[0])
    ax.scatter(T[o, 0], T[o, 1], s=5, c=cols[y[o]], lw=0, alpha=0.9, rasterized=True, zorder=1)
    m = keep & (y == L6)
    ax.scatter(T[m, 0], T[m, 1], s=42, marker="^", c="black", edgecolors="white", linewidths=0.5, zorder=3)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#d4d4d4")
    pad = 0.05
    lo, hi = T[keep].min(0), T[keep].max(0)
    ax.set_xlim(lo[0] - pad * (hi[0] - lo[0]), hi[0] + pad * (hi[0] - lo[0]))
    ax.set_ylim(lo[1] - pad * (hi[1] - lo[1]), hi[1] + pad * (hi[1] - lo[1]))
    for name, reg, col, dx, dy in (("cervical", "cervical", HUE["cervical"], 0.0, -0.02), ("thoracic", "thoracic", "#c9501f", 0.0, 0.0),
                                   ("lumbar", "lumbar", "#0f8a5e", -0.1, 0.13)):
        idx = keep & np.array([region(classes[c]) == reg for c in y])
        c = np.median(T[idx], 0) + np.array([dx, dy]) * (hi - lo)
        ax.text(c[0], c[1], name, fontsize=31, fontweight="bold", color=col, ha="center", va="center", zorder=5,
                bbox=dict(fc="white", ec="none", alpha=0.82, pad=2.5))
    ax.text(0.03, 0.965, "▲ L6", transform=ax.transAxes, fontsize=31, fontweight="bold", color="black", ha="left",
            va="top", zorder=6)
    out = OUT / "_map.png"
    fig.savefig(out, dpi=100)
    plt.close(fig)
    print("level map: vertebrae drawn", int(keep.sum()), "L6", int(m.sum()), "persons with L6",
          len(set(mp["person"].astype(str)[m].tolist())))
    return Image.open(out).convert("RGB")


def closing():
    W = 2000
    head, H, gut = 62, 672, 42
    ct = masked_ct(H)
    dt = detected(H)
    size, gap = 216, 12
    tl = tiles(size, gap)
    assert tl.size[1] == H
    x = [0]
    x.append(x[0] + ct.width + gut)
    x.append(x[1] + dt.width + gut)
    x.append(x[2] + tl.width + gut)
    mw = W - x[3]
    assert mw > 400, mw
    mp = level_map(mw, H)
    can = Image.new("RGB", (W, head + H), "white")
    for xi, p in zip(x, (ct, dt, tl, mp)):
        can.paste(p, (xi, head))
    d = ImageDraw.Draw(can)
    f = ImageFont.truetype(BOLD, 48)
    for xi, p, t in zip(x, (ct, dt, tl, mp), ("Masked CT", "Detected", "Predicted", "Classified")):
        tw = d.textlength(t, font=f)
        d.text((xi + (p.width - tw) / 2, 0), t, fill=(0x19, 0x1D, 0x63), font=f)
    # one gold arrow: in on the left, out on the right
    ax_, ay = x[1] - gut + 3, head + H // 2
    d.polygon([(ax_, ay - 13), (ax_ + 20, ay - 13), (ax_ + 20, ay - 30), (ax_ + 37, ay), (ax_ + 20, ay + 30),
               (ax_ + 20, ay + 13), (ax_, ay + 13)], fill=(0xFF, 0xC4, 0x2F))
    can.save(OUT / "closing.png", optimize=True)
    (OUT / "_map.png").unlink()
    print("closing", can.size, round(can.size[0] / can.size[1], 3))


if __name__ == "__main__":
    pic_abc()
    render_l6()
    benzel()
    N = {"violin": violin(), "canal": atlas_canal(), "spinopelvic": spinopelvic()}
    closing()
    json.dump(N, open(OUT / "numbers.json", "w"), indent=1)
    print("done")
