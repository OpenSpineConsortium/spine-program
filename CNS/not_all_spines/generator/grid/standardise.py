"""The fixed readings standardised to Panjabi's twelve cadavers' age and sex (direct standardisation by
matching): for each of his specimens (schwingcheck/data/panjabi_specimens.csv: 8 men, 4 women, 19 to 59
years), the mean at each level of our people of the same sex within AGE_REACH years of its age (widened by
WIDEN years at a time until MIN_MATCH are found, at most MAX_REACH), and the standardised mean the mean of
the twelve. Our people are those whose age and sex the covariates join read: autoPET and TotalSegmentator
adults. Aggregates only.

    python standardise.py runs/full/out panjabi_specimens.csv persons.csv out.json
"""
import csv, json, os, statistics, sys

AGE_REACH, WIDEN, MAX_REACH, MIN_MATCH = 5, 5, 20, 10
HEIGHT_REACH, HEIGHT_WIDEN, HEIGHT_MAX = 3.0, 2.0, 10.0
MODE = sys.argv[5] if len(sys.argv) > 5 else "age"     # age, height, or age_height
KEYS = ("plate_w_l", "plate_d_u", "plate_w_u", "plate_d_l", "ct_scw", "ct_scd")
out_dir, specimens_path, persons_path, dest = sys.argv[1:5]

people = []
for r in csv.DictReader(open(persons_path)):
    if r["sex"] not in ("M", "F") or r["member"] not in ("autopet", "totalseg"):
        continue
    try:
        age = float(r["age"])
    except ValueError:
        continue
    if not 18 <= age <= 110:
        continue
    try:
        height = 100.0 * float(r.get("height_m") or "nan")
    except ValueError:
        height = float("nan")
    if MODE != "age" and not 130 <= height <= 215:
        continue
    name = ("enhance-%s.csv" if r["member"] == "autopet" else "totalseg-%s.csv") % r["study"]
    if os.path.exists(os.path.join(out_dir, name)):
        people.append((name, age, r["sex"], height))

readings = {}
for name, age, sex, height in people:
    for r in csv.DictReader(open(os.path.join(out_dir, name))):
        if r["key"] in KEYS and r["value"]:
            readings.setdefault(name, {})[(r["key"], r["level"])] = float(r["value"])

specimens = [r for r in csv.DictReader(l for l in open(specimens_path) if not l.startswith("#"))]
levels = sorted({lv for d in readings.values() for _, lv in d})
measures, matches = {}, []
for key in KEYS:
    for lv in levels:
        spec_means, used = [], 0
        for s in specimens:
            age, sex, height = float(s["age_years"]), s["sex"], float(s["height_cm"])
            reach, hreach, vals = AGE_REACH, HEIGHT_REACH, []
            while True:
                vals = [readings[n][(key, lv)] for n, a, x, h in people
                        if x == sex and (MODE == "height" or abs(a - age) <= reach)
                        and (MODE == "age" or abs(h - height) <= hreach) and (key, lv) in readings.get(n, {})]
                if len(vals) >= MIN_MATCH or (reach >= MAX_REACH and hreach >= HEIGHT_MAX):
                    break
                reach, hreach = min(reach + WIDEN, MAX_REACH), min(hreach + HEIGHT_WIDEN, HEIGHT_MAX)
            if len(vals) >= MIN_MATCH:
                spec_means.append(statistics.fmean(vals))
                used += len(vals)
                if key == "plate_w_l" and lv == "L3":
                    matches.append({"specimen": s["specimen"], "sex": sex, "age": age, "height": height,
                                    "reach_years": reach, "reach_cm": hreach, "n": len(vals)})
        if len(spec_means) == len(specimens):
            measures.setdefault(key, {})[lv] = {"mean": statistics.fmean(spec_means), "n": used,
                                                "specimens": len(spec_means)}
json.dump({"mode": MODE, "people": len(people), "men": sum(1 for p in people if p[2] == "M"),
           "women": sum(1 for p in people if p[2] == "F"), "measures": measures, "matches_at_L3": matches,
           "rule": "direct standardisation to Panjabi's 12 specimens by sex and, by mode, age within 5 years (widened to 20) "
                   "and height within 3 cm (widened to 10)"},
          open(dest, "w"), indent=1, sort_keys=True)
print(len(people), "people;", {k: len(v) for k, v in measures.items()})
