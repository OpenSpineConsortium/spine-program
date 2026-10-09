"""make_assets.py -- prepare everything the report page embeds.

The Artifact CSP blocks external images, so every render has to travel inside the page as a
data URI. Forty full-size PNGs would be ~60 MB against a 16 MB budget, so a representative
handful are cropped to the spine, downscaled and re-encoded as JPEG.

Also emits the training curves as plain SVG path data -- 111 epochs of four series -- so the
page needs no charting library at all.
"""
from __future__ import annotations

import base64
import io
import json
from pathlib import Path

import pandas as pd
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE / "assets.json"

# one per source, plus the hardest cases: chosen to show range, not just the wins
PICKS = [
    ("mendeley_2695-F-026Y1.png", "Lumbar lateral", "mendeley",
     "Six bodies detected; predicted quadrilaterals track the ground truth through the "
     "lordotic curve, including the tilted L5/S1 segment."),
    ("buu_0004-F-010Y0.png", "Lumbar AP", "buu",
     "AP view. The corner slots here are the left and right ends of each endplate rather "
     "than anterior/posterior — the same four slots, decoded differently."),
    ("buu_0004-F-010Y1.png", "Lumbar lateral, same patient", "buu",
     "The AP and lateral of one patient. Both sit in the test split together: splitting by "
     "image rather than patient would have put this spine on both sides."),
]


def encode(p: Path, max_w: int = 1000, quality: int = 74) -> str:
    im = Image.open(p).convert("L")
    w, h = im.size
    # crop away the dead margin film scans carry, keeping the annotated column
    im = im.crop((int(w * 0.10), 0, int(w * 0.92), h))
    im = Image.open(p).convert("RGB")           # keep the green/magenta overlays
    w, h = im.size
    if w > max_w:
        im = im.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def curve_paths(df: pd.DataFrame, w=760, h=260, pad=34):
    """Return SVG path 'd' strings for the metric series, plus axis ticks."""
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    series = {
        "box50": "metrics/mAP50(B)",
        "box5095": "metrics/mAP50-95(B)",
        "pose50": "metrics/mAP50(P)",
        "pose5095": "metrics/mAP50-95(P)",
    }
    n = len(df)
    xs = df["epoch"].to_numpy(float)
    x0, x1 = xs.min(), xs.max()
    out = {}
    for key, col in series.items():
        ys = df[col].to_numpy(float)
        pts = []
        for x, y in zip(xs, ys):
            px = pad + (x - x0) / max(x1 - x0, 1) * (w - 2 * pad)
            py = h - pad - y * (h - 2 * pad)          # metrics are already 0..1
            pts.append(f"{px:.1f},{py:.1f}")
        out[key] = "M" + " L".join(pts)
    out["_meta"] = {"w": w, "h": h, "pad": pad, "n_epochs": int(n),
                    "x0": float(x0), "x1": float(x1)}
    return out


def main():
    renders = {}
    for fname, title, source, caption in PICKS:
        p = HERE / "renders" / fname
        if not p.exists():
            continue
        renders[fname] = {"title": title, "source": source, "caption": caption,
                          "uri": encode(p)}
        print(f"  {fname}: {len(renders[fname]['uri'])/1e3:.0f} kB")

    df = pd.read_csv(HERE / "results.csv")
    curves = curve_paths(df)
    metrics = json.loads((HERE / "metrics.json").read_text())

    dfm = pd.read_parquet(HERE / "manifest.parquet")
    cohort = {
        "images": int(dfm["image_id"].nunique()),
        "instances": int(len(dfm)),
        "by_source": {k: int(v) for k, v in dfm["source"].value_counts().items()},
        "by_view": {k: int(v) for k, v in dfm["view"].value_counts().items()},
        "by_level_source": {k: int(v) for k, v in dfm["level_source"].value_counts().items()},
        "patients": int(dfm["patient_id"].nunique()),
    }

    d = df.copy(); d.columns = [c.strip() for c in d.columns]
    final = {
        "box_map50": float(d["metrics/mAP50(B)"].iloc[-1]),
        "box_map5095": float(d["metrics/mAP50-95(B)"].iloc[-1]),
        "pose_map50": float(d["metrics/mAP50(P)"].iloc[-1]),
        "pose_map5095": float(d["metrics/mAP50-95(P)"].iloc[-1]),
        "best_box_map50": float(d["metrics/mAP50(B)"].max()),
        "epochs": int(len(d)),
    }

    OUT.write_text(json.dumps({"renders": renders, "curves": curves,
                               "metrics": metrics, "cohort": cohort,
                               "final": final}, indent=1))
    print(f"wrote {OUT} ({OUT.stat().st_size/1e6:.2f} MB)")
    print(json.dumps(cohort, indent=1))
    print(json.dumps(final, indent=1))


if __name__ == "__main__":
    main()
