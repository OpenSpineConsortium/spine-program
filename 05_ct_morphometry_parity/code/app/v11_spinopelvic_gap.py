"""CT-2 step 1 (issue #25): the v11 spinopelvic means against Veilleux 2020, before any APP fit.

Reads the v11 columns of results/morphometrics/surgical_morphometrics.csv (CTSpinoPelvic1K
scripts/extract_surgical_morphometrics.py, commit 2232bde; the copy at spine-program main 5597197)
and prints n, mean, SD, median and IQR of PI, SS and PT beside the two published supine-CT series
that docs/SPINOPELVIC_ESTIMATOR.md section 5 compares with. It also lists the records without PI,
for OPEN_QUESTIONS D4 (44 plate rejections, plus which two others).

The identity PI = SS + PT is not used as a check (TODO.md step 2): both sides share the S1
end-plate, so it holds when the landmark is wrong.

Run: python v11_spinopelvic_gap.py <surgical_morphometrics.csv>
Standard library only, so it runs on a laptop or as a short job on the grid.
"""
import csv
import statistics
import sys

# Comparators, pre-specified in TODO.md step 2 and STATUS.md F.21; never tuned.
VEILLEUX_2020 = {"n": 200, "pelvic_incidence_deg": 52.1, "sacral_slope_deg": 36.5, "pelvic_tilt_deg": 15.6}
HASEGAWA_2018 = {"n": 24, "pelvic_incidence_deg": 53.4, "sacral_slope_deg": 34.1, "pelvic_tilt_deg": 19.2}
# What the folder expects from the v11 table (STATUS.md F.21), so a mismatch is visible at once.
F21_EXPECTED_MEANS = {"pelvic_incidence_deg": 52.1, "sacral_slope_deg": 36.6, "pelvic_tilt_deg": 15.5}
F21_EXPECTED_N = 756

COLS = ["pelvic_incidence_deg", "sacral_slope_deg", "pelvic_tilt_deg"]
SHORT = {"pelvic_incidence_deg": "PI", "sacral_slope_deg": "SS", "pelvic_tilt_deg": "PT"}


def as_float(text):
    text = (text or "").strip()
    if text == "" or text.lower() in ("nan", "none"):
        return None
    return float(text)


def quartiles(values):
    q = statistics.quantiles(values, n=4, method="inclusive")
    return q[0], q[2]


def main(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    print(f"input: {path}")
    print(f"records: {len(rows)}")
    ids = [r["case"].strip().zfill(4) for r in rows]
    if len(set(ids)) != len(ids):
        raise SystemExit("duplicate case ids after zfill(4)")

    complete = [r for r in rows if all(as_float(r[c]) is not None for c in COLS)]
    print(f"records with PI, SS and PT all present: {len(complete)} (F.21 expects {F21_EXPECTED_N})")
    print()

    header = f"{'':4}{'n':>6}{'mean':>8}{'SD':>7}{'median':>8}{'IQR':>15}  {'F.21':>6}  {'Veilleux':>9}{'gap':>7}  {'Hasegawa':>9}{'gap':>7}"
    print(header)
    print("-" * len(header))
    for c in COLS:
        v = [as_float(r[c]) for r in complete]
        mean = statistics.fmean(v)
        sd = statistics.stdev(v)
        med = statistics.median(v)
        q1, q3 = quartiles(v)
        gv = mean - VEILLEUX_2020[c]
        gh = mean - HASEGAWA_2018[c]
        print(
            f"{SHORT[c]:4}{len(v):>6}{mean:>8.1f}{sd:>7.1f}{med:>8.1f}{f'{q1:.1f}-{q3:.1f}':>15}"
            f"  {F21_EXPECTED_MEANS[c]:>6.1f}  {VEILLEUX_2020[c]:>9.1f}{gv:>+7.1f}  {HASEGAWA_2018[c]:>9.1f}{gh:>+7.1f}"
        )
    print()
    print("gap = this cohort's mean minus the published mean, in degrees.")
    print(f"Veilleux 2020 n {VEILLEUX_2020['n']} (asymptomatic, automated supine CT); "
          f"Hasegawa 2018 n {HASEGAWA_2018['n']} (older symptomatic, supine CT).")
    print()

    # Each column on its own, in case one parameter is missing where the others are not.
    for c in COLS:
        n = sum(as_float(r[c]) is not None for r in rows)
        print(f"{SHORT[c]} present on its own: {n}")
    missing = [r for r in rows if as_float(r["pelvic_incidence_deg"]) is None]
    rejected = [r for r in missing if (r.get("s1_plate_rejected") or "").strip().lower() in ("1", "true", "1.0")]
    other = [r for r in missing if r not in rejected]
    print(f"records without PI: {len(missing)}; of them flagged s1_plate_rejected: {len(rejected)}")
    reasons = {}
    for r in rejected:
        key = (r.get("s1_plate_reject_reason") or "").strip() or "(blank)"
        reasons[key] = reasons.get(key, 0) + 1
    for k, n in sorted(reasons.items(), key=lambda kv: -kv[1]):
        print(f"  reject reason {k}: {n}")
    print("records without PI and not flagged rejected (OPEN_QUESTIONS D4): "
          + (", ".join(r["case"].strip().zfill(4) for r in other) or "none"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
