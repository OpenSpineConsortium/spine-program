"""paper/cns2026/make_profile_v19.py -- the profile v19's panels draw: the gold tier means reweighted to Panjabi's
twelve cadavers' sex and age (figs_v19_6min/standardised.json, grid/standardise.py, job 40912660: each of his
specimens matched to our adults of the same sex within 5 years of its age, the mean the mean of the twelve), with
T13 and L6 from every spine (figs_v18_6min/profile.json), since VerSe, which holds the T13s, records no sex and
twelve cadavers hold no transitional spine to match.

    python paper/cns2026/make_profile_v19.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
std = json.load(open(HERE / "figs_v19_6min" / "standardised.json", encoding="utf-8"))
full = json.load(open(HERE / "figs_v18_6min" / "profile.json", encoding="utf-8"))
measures = {}
for key, levels in std["measures"].items():
    for level, row in levels.items():
        measures.setdefault(key, {})[level] = {"n": row["n"], "mean": row["mean"], "sd": 0.0}
for key, levels in full["measures"].items():
    for level in ("T13", "L6"):
        if level in levels:
            measures.setdefault(key, {})[level] = levels[level]
out = {"spines": {"all": std["people"], "men": std["men"], "women": std["women"], "full_spines": full["spines"]["all"]},
       "extra_levels": full["extra_levels"], "measures": measures, "rule": std["rule"]}
json.dump(out, open(HERE / "figs_v19_6min" / "profile.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
print(out["spines"])
