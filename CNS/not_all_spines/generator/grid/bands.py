"""The gold tier means by sex and decade of age, for slide 5's sex-and-age click (v21, Greg, 2026-10-31, night).

The same adults and readings as reweight.py (autoPET and TotalSegmentator adults whose sex and age the covariates
join, one CT a person), each measure's mean at each level over the men or the women of one decade, 20s to 80s
(18 and 19 counted with the 20s, 90 and over with the 80s); a level is kept where ten or more were read.
Aggregates only.

    python bands.py runs/full/out persons.csv out.json
"""
from __future__ import annotations

import json
import statistics
import sys

from reweight import KEYS, load_people, load_readings

DECADES = (20, 30, 40, 50, 60, 70, 80)
LEAST = 10


def decade(age):
    return min(max(int(age // 10) * 10, DECADES[0]), DECADES[-1])


def main():
    out_dir, persons, target = sys.argv[1:4]
    people = load_people(persons, out_dir)
    readings = load_readings(people, out_dir)
    groups, counts = {}, {}
    for p in people:
        group = f"{p['sex']}{decade(p['age'])}"
        counts[group] = counts.get(group, 0) + 1
        for (key, level), value in readings.get(p["name"], {}).items():
            groups.setdefault(group, {}).setdefault(key, {}).setdefault(level, []).append(value)
    bands = {g: {k: {lv: {"mean": statistics.fmean(v), "n": len(v)} for lv, v in levels.items() if len(v) >= LEAST}
                 for k, levels in keys.items()} for g, keys in groups.items()}
    json.dump({"people": len(people), "counts": counts, "bands": bands, "keys": KEYS, "least": LEAST,
               "ages": {g: statistics.fmean(p["age"] for p in people if f"{p['sex']}{decade(p['age'])}" == g)
                        for g in counts}}, open(target, "w"), indent=1)
    print(counts)


if __name__ == "__main__":
    main()
