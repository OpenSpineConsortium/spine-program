# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/source_quality_report.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Every data source in the training bank, with where its labels came from and how good its pixels are.

A per-source accuracy is meaningless without two things beside it: what kind of label the source carries, and
what the crops look like. A source whose levels were inferred by counting from L5 cannot score a transitional
detector; a source whose labels are our own decoder's output cannot score anything, since agreement with
oneself is not accuracy. And a source whose crops are blurred or low-contrast will drag any pooled number down
for reasons that have nothing to do with the method.

LABEL ORIGIN is stated per source, as a fact about how the bank was built, and the tiers are:
    human           a person placed the landmark and named the level
    from_ct         a digitally reconstructed radiograph, levels carried over from the CT segmentation (exact)
    counting        a person placed landmarks and the level NAME was inferred by counting from a fixed anchor
                    (BUU: five lumbar assumed; AASCE: seventeen bodies T1-L5 assumed)
    pseudo          our own decoder named it; unverified
Anything not in the table is reported as UNKNOWN rather than guessed.

QUALITY is measured on the crops the model actually sees, on a fixed-size random sample per source, with the
same four statistics used in the anomaly manifest: sharpness (variance of a Laplacian), contrast (1st-99th
percentile span), noise (MAD of a high-pass residual) and their ratio. They are comparable across sources
because every crop is on the same canvas at the same target scale; they are NOT comparable to a number taken
off a source file.

    python tools/source_quality_report.py --bank ~/allspine_v5_fov96_ctx/rung_1.npz --per-source 400
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anomaly_manifest import quality_stats, _memmap_npz_member  # noqa: E402

LABEL_ORIGIN = {
    "csxa": ("human", "cervical films; corner landmarks and level names by annotators"),
    "nhanes": ("human", "NHANES annotated subset (543); level names by annotators"),
    "mendeley": ("human", "lumbar films; annotator level names"),
    "vindr": ("human", "VinDr subset with level annotation from our reading set"),
    "buu_full": ("counting", "BUU-LSPINE four-corner keypoints; L1-L5 names assume five lumbar bodies"),
    "aasce": ("counting", "AASCE 17 bodies assumed T1-L5; no anomaly labels"),
    "ctsp_drr": ("from_ct", "DRR of CTSpinoPelvic1K CT; levels from the segmentation"),
    "ctsp_drr_obl2": ("from_ct", "oblique DRRs, CTSP + VerSe"),
    "verse_drr": ("from_ct", "DRR of VerSe CT"),
    "verse_drr_obl2": ("from_ct", "oblique DRRs of VerSe"),
    "physics_drr": ("from_ct", "physics-based DRR of CTSP with scatter/beam model"),
    "physics_rare": ("from_ct", "physics DRRs of anomaly-enriched CT spines"),
    "nhanes_drr": ("from_ct", "NHANES films re-rendered through the DRR normalisation"),
    "NHANESPS": ("pseudo", "NHANES films named by our decoder; unverified"),
    "VINDRPS": ("pseudo", "VinDr films named by our decoder; unverified"),
    "LAT236PS": ("pseudo", "lateral236 films named by our decoder; unverified"),
}
REAL = {"csxa", "nhanes", "mendeley", "vindr", "buu_full", "aasce", "NHANESPS", "VINDRPS", "LAT236PS"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", default="~/allspine_v5_fov96_ctx/rung_1.npz")
    ap.add_argument("--per-source", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="~/model_night/source_quality")
    a = ap.parse_args()

    bank = Path(os.path.expanduser(a.bank))
    meta = json.load(open(bank.parent / "meta.json"))
    classes = meta["classes"]
    d = np.load(str(bank), allow_pickle=True)
    y, case, split, source = d["y"], d["case"], d["split"], d["source"]
    X = _memmap_npz_member(bank, "X")
    if X is None:
        raise SystemExit("bank X is compressed; cannot sample without reading 48 GiB")
    rng = np.random.RandomState(a.seed)

    rows = {}
    for s in sorted(set(source.tolist())):
        m = np.where(source == s)[0]
        cases = set(case[m].tolist())
        lv = Counter(classes[int(v)] for v in y[m])
        sample = rng.choice(m, min(a.per_source, len(m)), replace=False)
        qs = [quality_stats(np.asarray(X[i])) for i in sample]
        agg = {}
        for k in ("sharpness", "contrast", "noise", "snr"):
            v = [q[k] for q in qs if q[k] is not None]
            agg[k] = {"median": float(np.median(v)), "p10": float(np.percentile(v, 10)),
                      "p90": float(np.percentile(v, 90))} if v else None
        origin, note = LABEL_ORIGIN.get(s, ("UNKNOWN", "not in the origin table; say so, do not guess"))
        rows[s] = {
            "n_crops": int(len(m)), "n_cases": len(cases),
            "n_train": int((split[m] == "train").sum()), "n_val": int((split[m] == "val").sum()),
            "domain": "real_film" if s in REAL else "ct_render",
            "label_origin": origin, "label_note": note,
            "levels_present": len(lv), "top_levels": dict(lv.most_common(6)),
            "has_T13": int(lv.get("T13", 0)), "has_L6": int(lv.get("L6", 0)),
            "has_sacrum": int(lv.get("sacrum", 0)),
            "cervical": sum(v for k, v in lv.items() if k.startswith("C")),
            "thoracic": sum(v for k, v in lv.items() if k.startswith("T")),
            "lumbar": sum(v for k, v in lv.items() if k.startswith("L")),
            "quality": agg, "quality_sample": int(len(sample)),
        }
        print(f"{s:<16} {len(m):>7} crops {len(cases):>6} cases  {origin:<9} "
              f"sharp {agg['sharpness']['median']:.4f}  contr {agg['contrast']['median']:.3f}  "
              f"snr {agg['snr']['median']:.1f}   C/T/L {rows[s]['cervical']}/{rows[s]['thoracic']}/{rows[s]['lumbar']}"
              f"  T13={rows[s]['has_T13']} L6={rows[s]['has_L6']} sac={rows[s]['has_sacrum']}", flush=True)

    tot = sum(r["n_crops"] for r in rows.values())
    by_origin = Counter()
    for r in rows.values():
        by_origin[r["label_origin"]] += r["n_crops"]
    print(f"\n{tot} crops.  by label origin: " + ", ".join(f"{k} {v} ({100 * v / tot:.1f}%)" for k, v in by_origin.most_common()))
    unknown = [s for s, r in rows.items() if r["label_origin"] == "UNKNOWN"]
    if unknown:
        print(f"UNKNOWN origin, must be resolved before any claim uses them: {unknown}")

    out = Path(os.path.expanduser(a.out))
    out.mkdir(parents=True, exist_ok=True)
    json.dump({"bank": str(bank), "n_crops": tot, "by_origin": dict(by_origin), "sources": rows},
              open(out / "source_quality.json", "w"), indent=1)
    print(f"wrote {out}/source_quality.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
