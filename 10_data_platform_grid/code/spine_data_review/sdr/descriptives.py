"""SAP general rules for counting (totals_keep, seeded strata, per-modality counts) and the A2 descriptives.

WHY THE COUNTING RULES LIVE APART FROM THE OTHER ANALYSES. Every sum, stratum and cross-tabulation
in the manuscript obeys the same handful of rules from statistical_analysis_plan.md, and the
reviewer found each of them broken in one place while it held in another: a subject_overlap
listed on only one record was subtracted only when the smaller id carried it; a multi-modal
dataset's whole n_subjects went into every modality row of the table while Figure 2's curve used
n_per_modality; a category with zero datasets vanished from the table and reached the manuscript
as an absent path. So the rules are written here once, as functions every analysis calls:

- `totals_keep`: figure-derived and `estimated` counts never enter a sum or a pooled estimate;
  one dataset per parent family (transitive over parent_ids; the largest n_i for that analysis
  stays); a subject_overlap pair outside a family is collected symmetrically (frozenset of the
  two ids, the larger n_shared when both sides list it), the smaller leaves when n_shared is
  unknown, and a known n_shared is subtracted once per pair.
- `_by` / `_xt`: every categorical table is seeded with the schema's enum (charting_schema.json,
  read once into ENUMS) so a zero is a row with n_datasets 0 and null sums, never an absence.
- `per_modality`: a dataset with more than one eligible modality (MRI and `other` are out of
  scope) contributes n_per_modality to a modality row, never its overall count; by_modality and
  the cumulative curve both go through it, and sdr/stats.py --selftest asserts they agree.

`descriptives()` is SAP A2: the dataset table, the totals under the rules above, the by_* strata
(modality, region, projection, annotation type and origin, route, licence tier, year, year band,
country in full and as top ten plus `other`, pediatric, format, flags, level names, variant
labelling) and the cross-tabulations. Output shape in PIPELINE.md stage 7.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from sdr.common import review_root

YEAR_BANDS = ((2000, 2010, "2000-2010"), (2011, 2016, "2011-2016"), (2017, 2020, "2017-2020"), (2021, 2026, "2021-2026"))
PROJ_MODALITIES = {"radiograph", "fluoroscopy", "DXA-VFA", "EOS"}


def _enums() -> dict:
    """The schema's categories, read once so every count table carries every category (SAP general rules)."""
    s = json.loads((review_root() / "charting_schema.json").read_text(encoding="utf-8"))
    dfs, pr = s["definitions"], s["properties"]
    return {"route": dfs["access_route"]["enum"], "modality": pr["modality"]["items"]["enum"], "region": pr["region"]["items"]["enum"],
            "projection": pr["projection"]["items"]["enum"], "annotation_type": dfs["annotation_type"]["enum"], "origin": dfs["origin"]["enum"],
            "tier": pr["licence"]["properties"]["tier"]["enum"], "host_type": pr["host_type"]["enum"], "format": pr["format"]["items"]["enum"],
            "on_grid": pr["on_grid"]["properties"]["status"]["enum"], "yes_no_unknown": dfs["yes_no_unknown"]["enum"],
            "level_names": pr["per_vertebra_level_names"]["enum"], "year_band": [lab for *_, lab in YEAR_BANDS] + ["unknown"],
            "flags": ["primary", "derived", "figure-derived"], "variant_row": ["explicit-label", "derivable-from-labels", "neither"]}


ENUMS = _enums()


# ----------------------------------------------------------------------------- loaders and shared rules
def load_datasets(cdir: Path, limit: int | None = None) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(cdir.glob("*.json"))[: limit or None]]


def year_band(y) -> str:
    return next((lab for lo, hi, lab in YEAR_BANDS if y is not None and lo <= y <= hi), "unknown")


def totals_keep(ds: list[dict], n_of=None) -> dict:
    """Which datasets enter a sum or a pooled estimate (module docstring). `n_of` defaults to n_subjects;
    A5 passes the variant's n_subjects_assessed. Returns keep, excluded{id: reason}, subtract, subtracted_pairs."""
    n_of = n_of or (lambda d: d.get("n_subjects"))
    by_id, parent = {d["id"]: d for d in ds}, {}

    def find(a):
        while parent.get(a, a) != a:
            a = parent[a]
        return a

    for d in ds:
        for p in d["flags"].get("parent_ids") or []:
            parent[find(d["id"])] = find(p)
    fam, excluded, pairs = defaultdict(list), {}, {}
    for d in ds:
        if d["flags"]["figure_derived"]:
            excluded[d["id"]] = "figure-derived"
        elif d.get("n_subjects_basis") == "estimated":
            excluded[d["id"]] = "n_subjects estimated"
        else:
            fam[find(d["id"])].append(d)
    for members in fam.values():
        members.sort(key=lambda d: (-(n_of(d) or 0), d["id"]))
        excluded.update({m["id"]: f"parent family duplicate of {members[0]['id']}" for m in members[1:]})
    for d in ds:
        for ov in d.get("subject_overlap") or []:
            key = frozenset((d["id"], ov["dataset_id"]))
            if len(key) == 2 and ov["dataset_id"] in by_id:
                pairs[key] = max(pairs.get(key, -1), -1 if ov.get("n_shared") is None else ov["n_shared"])   # -1 = unknown
    ordered = [tuple(sorted(k)) for k in sorted(pairs, key=sorted)]
    for a, b in ordered:                                  # unknown n_shared: the smaller leaves (ties: the later id)
        if pairs[frozenset((a, b))] < 0 and a not in excluded and b not in excluded and find(a) != find(b):
            loser, winner = ((b, a) if (n_of(by_id[b]) or 0) <= (n_of(by_id[a]) or 0) else (a, b))
            excluded[loser] = f"subject overlap with larger {winner}"
    sub = [{"pair": [a, b], "n_shared": pairs[frozenset((a, b))]} for a, b in ordered
           if pairs[frozenset((a, b))] >= 0 and a not in excluded and b not in excluded and find(a) != find(b)]
    return {"keep": sorted(d["id"] for d in ds if d["id"] not in excluded), "excluded": excluded,
            "subtract": sum(s["n_shared"] for s in sub), "subtracted_pairs": sub}


def _sum_median(vals: list) -> dict:
    v = [x for x in vals if x is not None]
    return {"n_known": len(v), "n_unknown": len(vals) - len(v), "sum": int(sum(v)) if v else None,
            "median": float(np.percentile(v, 50)) if v else None,
            "iqr": [float(np.percentile(v, 25)), float(np.percentile(v, 75))] if v else None}


def _sec(value, derived_from: list[str], rule: str) -> dict:
    return {"value": value, "derived_from": sorted(set(derived_from)), "rule": rule}


def _flat(prefix: str, sm: dict) -> dict:
    return {f"{prefix}_{k}": sm[k] for k in ("sum", "median", "iqr", "n_known", "n_unknown")}


def _by(ds: list[dict], key, keep: set, multi: bool = False, all_keys=None, count=None) -> dict:
    """Datasets, subjects and images per stratum; `key` returns one value, or a list when multi; `all_keys`
    seeds the schema's categories (a zero is a row); `count(d, stratum)` -> (n_subjects, n_images) lets a
    multi-modal dataset contribute n_per_modality to a modality row and never its overall count."""
    count = count or (lambda d, k: (d.get("n_subjects"), d.get("n_images_or_volumes")))
    out = {str(k): [] for k in (all_keys or [])}
    for d in ds:
        for k in (key(d) if multi else [key(d)]) or ["unknown"]:
            out.setdefault(str(k), []).append(d)
    res = {}
    for k, v in sorted(out.items()):
        c = [count(d, k) for d in v if d["id"] in keep]
        res[k] = {"n_datasets": len(v), **_flat("n_subjects", _sum_median([x[0] for x in c])), **_flat("n_images", _sum_median([x[1] for x in c]))}
    return res


def _xt(rows: list[dict], rk, ck, rows_all=None, cols_all=None) -> dict:
    """Cross-tabulation of list-valued keys; a row counts once per (row value, column value); seeded rows
    and columns hold zeros."""
    t = {str(r): {str(c): 0 for c in (cols_all or [])} for r in (rows_all or [])}
    for d in rows:
        for r in (rk(d) or ["unknown"]):
            row = t.setdefault(str(r), {str(c): 0 for c in (cols_all or [])})
            for c in (ck(d) or ["unknown"]):
                row[str(c)] = row.get(str(c), 0) + 1
    return {r: dict(sorted(c.items())) for r, c in sorted(t.items())}


def eligible_modalities(d: dict) -> list[str]:
    return [m for m in d["modality"] if m not in ("MRI", "other")]


def per_modality(d: dict, m: str) -> tuple:
    """(n_subjects, n_images) a dataset contributes to modality row m: its n_per_modality entry when it
    carries more than one eligible modality (SAP A2), else its overall counts."""
    if len(eligible_modalities(d)) > 1:
        pm = (d.get("n_per_modality") or {}).get(m) or {}
        return pm.get("n_subjects"), pm.get("n_images_or_volumes")
    return d.get("n_subjects"), d.get("n_images_or_volumes")


def level_origin(d: dict) -> list[str]:
    """Origin of the level names, falling back to the segmentation entry as rubric Q2 does (SAP A2)."""
    bt = d.get("annotation_origin_by_type", {})
    hit = next((bt[t] for t in ("per-vertebra-level-names", "segmentation-3d", "segmentation-2d") if t in bt), None)
    return list(hit) if hit else ["none"] if d.get("annotation_types") == ["none"] else ["unknown"]


def _variant_row(d: dict) -> str:
    hows = {d["variant_labels"][v]["how_labelled"] for v in ("L6", "T13", "LSTV")}
    return "explicit-label" if "explicit-label" in hows else "derivable-from-labels" if "derivable-from-labels" in hows else "neither"


def _flag_row(d: dict) -> str:
    return "figure-derived" if d["flags"]["figure_derived"] else "derived" if d["flags"]["derived"] else "primary"


# ----------------------------------------------------------------------------- A2
def descriptives(ds: list[dict], qual: dict) -> dict:
    tk, qd, E = totals_keep(ds), qual.get("per_dataset", {}), ENUMS
    keep = set(tk["keep"])
    sym = {"yes": "Y", "no": "N", "unknown": "?"}
    table = [{"id": d["id"], "name": d["name"], "year": d["year"], "country": ";".join(d["country"]), "modality": ";".join(d["modality"]),
              "region": ";".join(d["region"]), "projection": ";".join(d["projection"]), "n_subjects": d.get("n_subjects"),
              "n_images_or_volumes": d.get("n_images_or_volumes"), "n_images_unit": d["n_images_unit"],
              "annotation_types": ";".join(d["annotation_types"]), "annotation_origin": ";".join(d["annotation_origin"]),
              "variants_L6_T13_LSTV": "".join(sym[d["variant_labels"][v]["status"]] for v in ("L6", "T13", "LSTV")),
              "licence_tier": d["licence"]["tier"], "access_route": d["access_route"],
              "quality_total": qd.get(d["id"], {}).get("total"), "fit_level_id": qd.get(d["id"], {}).get("fit_level_id")}
             for d in sorted(ds, key=lambda d: (";".join(d["modality"]), d["year"], d["name"]))]
    radio = [d for d in ds if set(d["modality"]) & PROJ_MODALITIES]
    v = {"table": table, "totals_rule": tk,
         "totals": {"n_subjects_sum": (_sum_median([d.get("n_subjects") for d in ds if d["id"] in keep])["sum"] or 0) - tk["subtract"],
                    "n_images_sum": _sum_median([d.get("n_images_or_volumes") for d in ds if d["id"] in keep])["sum"],
                    "n_datasets": len(ds), "n_datasets_in_totals": len(keep),
                    "label": "reported subjects summed across datasets (persons may recur)"},
         "by_modality": _by(ds, lambda d: d["modality"], keep, True, E["modality"], per_modality),
         "by_region": _by(ds, lambda d: d["region"], keep, True, E["region"]),
         "by_projection_radiography": _by(radio, lambda d: d["projection"], keep, True, E["projection"]),
         "by_annotation_type": _by(ds, lambda d: d["annotation_types"], keep, True, E["annotation_type"]),
         "by_annotation_origin": _by(ds, lambda d: d["annotation_origin"], keep, True, E["origin"]),
         "by_access_route": _by(ds, lambda d: d["access_route"], keep, all_keys=E["route"]),
         "by_licence_tier": _by(ds, lambda d: d["licence"]["tier"], keep, all_keys=E["tier"]),
         "by_year": _by(ds, lambda d: d["year"], keep), "by_year_band": _by(ds, lambda d: year_band(d["year"]), keep, all_keys=E["year_band"]),
         "by_country": _by(ds, lambda d: d["country"], keep, True), "by_country_top_ten": _top_ten(ds, keep),
         "by_pediatric": _by(ds, lambda d: d["pediatric_included"], keep, all_keys=E["yes_no_unknown"]),
         "by_format": _by(ds, lambda d: d["format"], keep, True, E["format"]),
         "by_flags": _by(ds, _flag_row, keep, all_keys=E["flags"]),
         "by_level_names": _by(ds, lambda d: d["per_vertebra_level_names"], keep, all_keys=E["level_names"]),
         "by_variant_labelling": _by(ds, _variant_row, keep, all_keys=E["variant_row"]),
         "year_x_modality": _xt(ds, lambda d: [d["year"]], lambda d: d["modality"], cols_all=E["modality"]),
         "cumulative_subjects_by_year_modality": _cumulative(ds, keep),
         "origin_x_modality": _xt(ds, lambda d: d["annotation_origin"], lambda d: d["modality"], E["origin"], E["modality"]),
         "variant_x_level_origin": _xt(ds, lambda d: [_variant_row(d)], level_origin, E["variant_row"], E["origin"]),
         "level_names_x_modality": _xt(ds, lambda d: [d["per_vertebra_level_names"]], lambda d: d["modality"], E["level_names"], E["modality"]),
         "region_x_projection_radiography": _xt(radio, lambda d: d["region"], lambda d: d["projection"], E["region"], E["projection"]),
         "route_x_licence": _xt(ds, lambda d: [d["access_route"]], lambda d: [d["licence"]["tier"]], E["route"], E["tier"]),
         "public_charted_x_regex": _xt(ds, lambda d: [d["described_as_public"]], lambda d: [str(d["described_as_public_regex"]).lower()], E["yes_no_unknown"], ["true", "false"])}
    return _sec(v, ["charting/datasets/*.json", "analysis/quality.json"],
                "SAP A2; in every by_* stratum n_datasets counts all datasets in the stratum while the subject and "
                "image sums and medians count only its totals_keep members (see totals_rule.excluded), so a stratum "
                "can show datasets against an empty sum")


def _top_ten(ds: list[dict], keep: set) -> dict:
    """Country rows: the ten with most datasets (ties by name) and one `other` row holding the datasets
    none of whose countries is among the ten (SAP A2)."""
    full = _by(ds, lambda d: d["country"], keep, True)
    top = sorted(full, key=lambda k: (-full[k]["n_datasets"], k))[:10]
    rest = [d for d in ds if not set(d["country"]) & set(top)]
    kept = [d for d in rest if d["id"] in keep]
    return {**{k: full[k] for k in top}, "other": {"n_datasets": len(rest), **_flat("n_subjects", _sum_median([d.get("n_subjects") for d in kept])),
                                                    **_flat("n_images", _sum_median([d.get("n_images_or_volumes") for d in kept]))}}


def _cumulative(ds: list[dict], keep: set) -> dict:
    """Cumulative subjects per year for CT (with CBCT) and projection radiography (Figure 2), through the
    same per_modality rule as by_modality so the curve and the table agree."""
    per = {"CT": Counter(), "radiography": Counter()}
    for d in ds:
        if d["id"] in keep:
            for m in eligible_modalities(d):
                per["CT" if m in ("CT", "CBCT") else "radiography"][d["year"]] += per_modality(d, m)[0] or 0
    years = list(range(2000, 2027))
    return {m: {str(y): int(sum(c[yy] for yy in years if yy <= y)) for y in years} for m, c in sorted(per.items())}
