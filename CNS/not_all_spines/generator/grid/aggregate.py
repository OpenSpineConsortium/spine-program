"""The fixed readings' profile by level over every full spine: n, mean, SD and percentiles of each key
by level, the spines by source, and how many show a T13 or an L6; aggregates only.

    python aggregate.py runs/full/out profile.json
"""
import csv, json, math, os, statistics, sys

KEYS = ("plate_w_u", "plate_d_u", "plate_w_l", "plate_d_l", "ct_scw", "ct_scd", "endplate", "endplate_depth",
        "endplate_lower", "endplate_lower_depth", "interpedicular_max", "canal_w", "canal_ap", "body_w_mid", "body_d_mid")
folder, dest = sys.argv[1:3]
vals, spines, extra, errors = {}, {}, {"T13": {}, "L6": {}}, 0
for name in sorted(os.listdir(folder)):
    if name.endswith(".err"):
        errors += 1
        continue
    if not name.endswith(".csv"):
        continue
    seen, source = set(), name.split("-")[0]
    for r in csv.DictReader(open(os.path.join(folder, name))):
        seen.add(r["level"])
        if r["key"] in KEYS and r["value"]:
            v = float(r["value"])
            if math.isfinite(v):
                vals.setdefault((r["key"], r["level"]), []).append((source, v))
    if seen:
        spines[source] = spines.get(source, 0) + 1
        for lv in ("T13", "L6"):
            if lv in seen:
                extra[lv][source] = extra[lv].get(source, 0) + 1


def q(xs, p):
    xs = sorted(xs)
    k = p * (len(xs) - 1)
    lo = int(math.floor(k))
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (k - lo)


measures = {}
for (key, lv), pairs in vals.items():
    xs = [v for _, v in pairs]
    row = {"n": len(xs), "mean": statistics.fmean(xs), "sd": statistics.stdev(xs) if len(xs) > 1 else None,
           "median": statistics.median(xs), "q05": q(xs, 0.05), "q95": q(xs, 0.95),
           "by_source": {s: len([1 for t, _ in pairs if t == s]) for s in sorted({t for t, _ in pairs})}}
    measures.setdefault(key, {})[lv] = row
spines["all"] = sum(v for k, v in spines.items())
json.dump({"spines": spines, "extra_levels": extra, "measures": measures, "errors": errors},
          open(dest, "w"), indent=1, sort_keys=True)
print(json.dumps({"spines": spines, "extra": extra, "errors": errors}))
