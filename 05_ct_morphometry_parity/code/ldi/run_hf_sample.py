#!/usr/bin/env python3
# spine-program copy, 05_ct_morphometry_parity/code/ldi/. Origin: the laptop folder LDI (no git; files dated
# 2026-05-26), recorded in MANIFEST_LOCAL.md. In no repository. The label map in this code is the LEGACY
# scheme (1=L1 ... 5=L5, 6=L6, 7=sacrum), NOT the v11 release scheme (L1=20 ... L5=24, L6=25, sacrum=26):
# resolve names with ostk.labels.labels_for(volume) before running it on release labels.
"""
run_hf_sample.py — Lazily pull token(s) from the CTSpinoPelvic1K-Sample HF
dataset and run the automated lordosis / LDI pipeline on them.

Only metadata (manifest, splits) is downloaded up front via
CTSpinoPelvic1K.from_hub. Each token's CT + label NIfTI is fetched on demand
(label first, to vet the case cheaply; CT only if the case qualifies) and
cached by huggingface_hub for subsequent runs.

Examples
--------
  # auto-pick the first fused case that has L5 + sacrum, render + measure
  python run_hf_sample.py

  # a specific token, require the full LDI label set
  python run_hf_sample.py --token 0071 --require 1,4,5,7

  # first 3 suitable fused cases, metrics only (no images)
  python run_hf_sample.py --limit 3 --no-viz
"""
import argparse
import csv
from pathlib import Path

import numpy as np

from dataset_interface import CTSpinoPelvic1K
from automated_lordosis import process_case

DEFAULT_REPO = "anonymous-neurips-ED/CTSpinoPelvic1K-Sample"


def tok_match(case_token: str, want: str) -> bool:
    """Tolerant token compare ('71' vs '0071')."""
    return case_token == want or case_token.zfill(4) == want.zfill(4)


def labels_present(case) -> set:
    """Lazily fetch just the label volume; return the set of non-zero ids."""
    lbl, _ = case.load_label()          # downloads label NIfTI on first call
    return {int(v) for v in np.unique(lbl) if v != 0}


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo",   default=DEFAULT_REPO, help="HF dataset repo id")
    ap.add_argument("--token",  default=None, help="specific token (else auto-pick)")
    ap.add_argument("--config", default="fused",
                    help="config filter (fused / spine_only / ...); falls back "
                         "to all cases if the filter is empty")
    ap.add_argument("--require", default="5,7",
                    help="label ids that MUST be present to run a case "
                         "(5=L5, 7=sacrum minimum for S1; use 1,4,5,7 for full LDI)")
    ap.add_argument("--limit",    type=int, default=1, help="how many suitable cases to run")
    ap.add_argument("--max-scan", type=int, default=8,
                    help="max candidate cases to inspect while searching")
    ap.add_argument("--out",      default="results_auto")
    ap.add_argument("--cache",    default=None, help="huggingface_hub cache dir")
    ap.add_argument("--no-viz",   action="store_true")
    args = ap.parse_args()

    need = {int(x) for x in args.require.split(",") if x.strip()}
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading metadata from {args.repo} (lazy) ...")
    ds = CTSpinoPelvic1K.from_hub(repo_id=args.repo, cache_dir=args.cache)
    print(ds.stats())

    # ── candidate pool ───────────────────────────────────────────────────────
    if args.token:
        cands = [c for c in ds.cases if tok_match(c.token, args.token)]
        if args.config:
            cands = [c for c in cands if c.config == args.config] or cands
        if not cands:
            raise SystemExit(f"token {args.token!r} not found in {args.repo}")
    else:
        cands = ds.filter(config=args.config) or list(ds.cases)

    print(f"\n{len(cands)} candidate case(s); looking for {args.limit} "
          f"with labels {sorted(need)} (scanning up to {args.max_scan}) ...")

    rows, ran = [], 0
    for case in cands[: args.max_scan]:
        if ran >= args.limit:
            break
        try:
            present = labels_present(case)
        except Exception as e:                       # noqa: BLE001 - report & continue
            print(f"  [skip] {case.token}: label fetch/read failed ({type(e).__name__}: {e})")
            continue
        if not need.issubset(present):
            print(f"  [skip] {case.token}: have {sorted(present)}, "
                  f"missing {sorted(need - present)}")
            continue
        case.load_ct()                               # fetch CT now that it qualifies
        row = process_case(case.ct_path, case.label_path, case.token,
                            out_dir, no_viz=args.no_viz)
        rows.append(row)
        ran += 1

    if not rows:
        raise SystemExit(
            "No suitable case found. Loosen --require, raise --max-scan, "
            "or pass an explicit --token.")

    csv_path = out_dir / "lordosis_metrics.csv"
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"\n✓ Ran {len(rows)} case(s) → {csv_path}")
    if not args.no_viz:
        for r in rows:
            print(f"  viz: {out_dir / ('sagittal_' + r['token'] + '.png')}")


if __name__ == "__main__":
    main()
