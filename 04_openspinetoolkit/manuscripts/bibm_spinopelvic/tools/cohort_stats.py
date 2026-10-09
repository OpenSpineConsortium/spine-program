"""
cohort_stats.py — turn an OpenSpineToolkit summary into Table 1 (parameter distribution).

Run the engine over the dataset, then this:
    python -m ostk all --labels <v4_labels_dir> --out summary.csv --workers 8
    python tools/cohort_stats.py summary.csv

Prints mean+/-SD, range and valid-measurement rate for PI / SS / PT / LL, plus the QC-flag
breakdown — paste straight into Table 1 / the Results text. Stdlib only.

A "valid" measurement is a finite number whose row's qc flag (if any) is empty/ok. Adjust
PARAM_KEYS / QC_KEYS below if your ostk CSV uses different column names.
"""
import csv
import math
import statistics
import sys

# candidate column names per parameter (first match wins) — extend if your CSV differs
PARAM_KEYS = {
    "PI": ["pelvic_incidence", "PI", "pi"],
    "SS": ["sacral_slope", "SS", "ss"],
    "PT": ["pelvic_tilt", "PT", "pt"],
    "LL": ["lumbar_lordosis", "LL", "ll"],
}
QC_KEYS = ["qc_flags", "qc", "qc_flag", "flags"]
OK_TOKENS = {"", "ok", "[]", "['ok']", "[\"ok\"]", "none", "nan"}


def _col(header, names):
    low = {h.lower(): h for h in header}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    return None


def _num(v):
    try:
        x = float(v)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def main(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit("empty CSV")
    header = rows[0].keys()
    qc_col = _col(header, QC_KEYS)
    n = len(rows)
    print(f"cases: {n}\n")
    print(f"{'param':5} {'mean±SD (deg)':>16} {'range (deg)':>16} {'valid rate':>12}")
    for p, names in PARAM_KEYS.items():
        c = _col(header, names)
        if not c:
            print(f"{p:5} {'(no column)':>16}")
            continue
        vals = [_num(r.get(c)) for r in rows]
        vals = [v for v in vals if v is not None]
        if not vals:
            print(f"{p:5} {'(no valid values)':>16}")
            continue
        m = statistics.mean(vals)
        sd = statistics.pstdev(vals) if len(vals) > 1 else 0.0
        rate = len(vals) / n
        print(f"{p:5} {f'{m:.1f} ± {sd:.1f}':>16} "
              f"{f'{min(vals):.0f}–{max(vals):.0f}':>16} {f'{100*rate:.0f}%':>12}")

    if qc_col:
        flagged = 0
        tally = {}
        for r in rows:
            v = (r.get(qc_col) or "").strip().lower()
            if v in OK_TOKENS:
                continue
            flagged += 1
            tally[v] = tally.get(v, 0) + 1
        print(f"\nQC-flagged cases: {flagged}/{n} ({100*flagged/n:.1f}%)")
        for k, v in sorted(tally.items(), key=lambda kv: -kv[1])[:10]:
            print(f"  {v:4} {k}")
    else:
        print("\n(no qc column found — set QC_KEYS)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python tools/cohort_stats.py summary.csv")
    main(sys.argv[1])
