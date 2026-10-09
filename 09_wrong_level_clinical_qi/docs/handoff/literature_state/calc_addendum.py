"""Addendum to power_calc.py, written for LITERATURE_STATE.md section 4 row 6.

power.md row 6 used the anomalous-film interior figure 66.0 % (12 films) against 91.8 % ordinary. The memory note it
cites (feasibility-claims-measured.md, V6 INTERIOR entry) says that 12-film figure "was noise" and names the
definitive pair: anomalous 49.9 % [41.5, 58.9] over 128 films against ordinary 89.9 % [87.1, 92.7] over 453 films.
This script applies the same two-proportion function (copied from power_calc.py, which copies tools/stats_compare.py)
to both pairs, at design effect 1 and 4, for 80 % and 90 % power, two-sided alpha 0.05.
"""
import json
import math
from pathlib import Path
from statistics import NormalDist

ND = NormalDist()


def cohens_h(p1, p2):
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def n_two_proportions(p1, p2, alpha=0.05, pw=0.8, deff=1.0, ratio=1.0):
    h = abs(cohens_h(p1, p2))
    z = ND.inv_cdf(1 - alpha / 2) + ND.inv_cdf(pw)
    n1 = deff * (1 + 1.0 / ratio) * (z / h) ** 2
    return math.ceil(n1), math.ceil(n1 * ratio), h


out = {}
for label, p1, p2 in (("definitive_899_vs_499", 0.899, 0.499), ("superseded_918_vs_660", 0.918, 0.660)):
    row = {}
    for pw in (0.8, 0.9):
        for de in (1.0, 4.0):
            n1, n2, h = n_two_proportions(p1, p2, pw=pw, deff=de)
            row[f"power{int(pw * 100)}_deff{int(de)}"] = n1
            row["cohens_h"] = round(h, 4)
    out[label] = row

p = Path(__file__).with_suffix(".json")
p.write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
