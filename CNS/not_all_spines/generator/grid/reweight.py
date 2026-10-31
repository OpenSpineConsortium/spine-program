"""The fixed readings reweighted to each population slide 5 steps through in v20 (Greg, 2026-10-31): Panjabi's
twelve cadavers, his eight men and his four women apart, Tan's ten Chinese Singaporean cadavers and Alonge's 120
Nigerian adults. Aggregates only.

- Panjabi (schwingcheck/data/panjabi_specimens.csv): each specimen matched to our adults of its sex within
  AGE_REACH years of its age, widened by WIDEN years at a time until MIN_MATCH are found, at most MAX_REACH; the
  mean the mean of the specimens' matched means (direct standardisation, as standardise.py). The men's and the
  women's lines are the same rule over his eight men and his four women, so the whole is their 8:4 blend.
- Tan 2004 (Eur Spine J 13:137): ten cadavers, 56 to 77 years, 1.59 to 1.72 m, 50 to 70 kg, sex not reported.
  Our adults inside all three ranges, either sex, each counted once; only autoPET records height and weight.
- Alonge 2021 (Afr J Med Med Sci 50:69): 54 men and 66 women, 18 to 65 years, mean 40.2, SD 10.07. Each sex
  stands as ten pseudo-specimens at the deciles' midpoints of that normal cut to 18 to 65 years, matched as
  Panjabi's are, the men weighted 54 and the women 66.

    python reweight.py runs/full/out panjabi_specimens.csv persons.csv out.json
"""
import csv, json, os, statistics, sys
from statistics import NormalDist

AGE_REACH, WIDEN, MAX_REACH, MIN_MATCH = 5, 5, 20, 10
KEYS = ("plate_w_l", "plate_d_u", "ct_scw", "ct_scd")
TAN = {"age": (56, 77), "height_cm": (159, 172), "weight_kg": (50, 70)}
ALONGE = {"M": 54, "F": 66, "mean": 40.2, "sd": 10.07, "age": (18, 65)}


def number(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return float("nan")


def load_people(persons_path, out_dir):
    people = []
    for r in csv.DictReader(open(persons_path)):
        if r["sex"] not in ("M", "F") or r["member"] not in ("autopet", "totalseg"):
            continue
        age = number(r["age"])
        if not 18 <= age <= 110:
            continue
        name = ("enhance-%s.csv" if r["member"] == "autopet" else "totalseg-%s.csv") % r["study"]
        if os.path.exists(os.path.join(out_dir, name)):
            people.append({"name": name, "age": age, "sex": r["sex"], "height_cm": 100.0 * number(r.get("height_m")),
                           "weight_kg": number(r.get("weight_kg"))})
    return people


def load_readings(people, out_dir):
    readings = {}
    for p in people:
        for r in csv.DictReader(open(os.path.join(out_dir, p["name"]))):
            if r["key"] in KEYS and r["value"]:
                readings.setdefault(p["name"], {})[(r["key"], r["level"])] = float(r["value"])
    return readings


def matched(people, readings, key, level, sex, age):
    """The readings of our people of SEX nearest AGE, by the widening rule, or [] where too few are found."""
    reach = AGE_REACH
    while True:
        values = [readings[p["name"]][(key, level)] for p in people
                  if p["sex"] == sex and abs(p["age"] - age) <= reach and (key, level) in readings.get(p["name"], {})]
        if len(values) >= MIN_MATCH:
            return values
        if reach >= MAX_REACH:
            return []
        reach = min(reach + WIDEN, MAX_REACH)


def standardised(people, readings, specimens, levels):
    """The weighted mean over SPECIMENS (sex, age, weight) of each one's matched mean, at every level all match."""
    measures = {}
    for key in KEYS:
        for level in levels:
            means, weights, used = [], [], 0
            for sex, age, weight in specimens:
                values = matched(people, readings, key, level, sex, age)
                if not values:
                    break
                means.append(statistics.fmean(values)); weights.append(weight); used += len(values)
            else:
                mean = sum(m * w for m, w in zip(means, weights)) / sum(weights)
                measures.setdefault(key, {})[level] = {"mean": mean, "n": used}
    return measures


def in_ranges(person, ranges):
    return all(lo <= person[field] <= hi for field, (lo, hi) in ranges.items())


def ranged(people, readings, ranges, levels):
    """The plain mean at every level over our people inside every one of RANGES, either sex."""
    inside = [p for p in people if in_ranges(p, ranges)]
    measures = {}
    for key in KEYS:
        for level in levels:
            values = [readings[p["name"]][(key, level)] for p in inside if (key, level) in readings.get(p["name"], {})]
            if len(values) >= MIN_MATCH:
                measures.setdefault(key, {})[level] = {"mean": statistics.fmean(values), "n": len(values)}
    who = {"people": len(inside), "men": sum(p["sex"] == "M" for p in inside),
           "mean_age": statistics.fmean(p["age"] for p in inside) if inside else None,
           "mean_height_cm": statistics.fmean(p["height_cm"] for p in inside) if inside else None}
    return measures, who


def alonge_specimens():
    """Ten pseudo-specimens a sex at the deciles' midpoints of Alonge's age, a normal cut to 18 to 65 years."""
    dist = NormalDist(ALONGE["mean"], ALONGE["sd"])
    low, high = (dist.cdf(a) for a in ALONGE["age"])
    ages = [dist.inv_cdf(low + (k + 0.5) / 10 * (high - low)) for k in range(10)]
    return [(sex, age, ALONGE[sex] / 10) for sex in ("M", "F") for age in ages]


def main():
    out_dir, specimens_path, persons_path, dest = sys.argv[1:5]
    people = load_people(persons_path, out_dir)
    readings = load_readings(people, out_dir)
    levels = sorted({level for d in readings.values() for _, level in d})
    rows = [r for r in csv.DictReader(l for l in open(specimens_path) if not l.startswith("#"))]
    panjabi = [(r["sex"], float(r["age_years"]), 1.0) for r in rows]
    tan, tan_who = ranged(people, readings, TAN, levels)
    result = {
        "people": len(people), "men": sum(p["sex"] == "M" for p in people),
        "targets": {
            "panjabi": {"measures": standardised(people, readings, panjabi, levels)},
            "panjabi_men": {"measures": standardised(people, readings, [s for s in panjabi if s[0] == "M"], levels)},
            "panjabi_women": {"measures": standardised(people, readings, [s for s in panjabi if s[0] == "F"], levels)},
            "tan": {"measures": tan, "who": tan_who, "ranges": TAN},
            "alonge": {"measures": standardised(people, readings, alonge_specimens(), levels),
                       "ages": [round(s[1], 1) for s in alonge_specimens()[:10]]},
        },
        "rule": "direct standardisation by sex and age within 5 years (widened to 20) for Panjabi and Alonge; "
                "Tan's age, height and weight ranges for Tan",
    }
    json.dump(result, open(dest, "w"), indent=1, sort_keys=True)
    print(len(people), "people;", {t: len(v["measures"].get("ct_scw", {})) for t, v in result["targets"].items()},
          "tan", tan_who)


if __name__ == "__main__":
    main()
