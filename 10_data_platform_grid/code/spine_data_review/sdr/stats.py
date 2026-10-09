"""SAP A3, A4, A5 and A7 analyses and the CLI that writes every analysis/*.json, from charting records and screening files.

WHY THIS MODULE IS THE CALLER AND NOT THE OWNER. The SAP's estimators (Wilson, Clopper-Pearson,
DerSimonian-Laird on the logit scale, Kruskal-Wallis with epsilon-squared and Dunn-Holm, the
Bonett-Wright interval on Spearman's rho, the trend test) live in sdr/estimators.py with their
self-test beside them; the counting rules every table obeys (one dataset per parent family,
symmetric subject overlaps, seeded categories, per-modality counts) and the A2 descriptives live
in sdr/descriptives.py; the A1 flow and its identities in sdr/flow_counts.py. This module decides
which rows enter the A3 availability, A4 quality analysis, A5 prevalence and A7 grid coverage
analyses, writes every analysis as {value, derived_from, rule, run_date}, and is the one command
the Makefile runs. Three checks the reviewer found missing are here because they sit between the
inputs and the analyses: analysis/quality.json is refused when its per_dataset ids differ from
charting/datasets/ or its scores_sha1 does not match a fresh hash (a stale, partial or hand-edited
file; allowed under --limit only, and said so); the A3.2 file-URL row reads the file probes that
sdr/availability.py keeps in charting/probes/<id>.json (--probes-dir) through the same
`file_url_confirmed()` as rubric Q7, so the two cannot drift; and --selftest, after the estimator
checks, asserts on tests/fixtures/stats that the file-URL row is 10/10 and that the per-modality
subject sums equal the cumulative curve of Figure 2.

A3 also carries the figure-derived pool of SAP A3.4 (counts per query and per source from
<run-dir>/queries.json, no pooling) and counts a probe pair as changed when the classification
or the HTTP status class differs; A4 computes epsilon-squared and Dunn on the annotated stratum
only (the `all` stratum is exploratory-secondary and says so); A5 applies the family/overlap
rule per variant with that variant's n_subjects_assessed as n_i. An absent input is listed in
`missing_inputs` (flow) or leaves nulls, so a half-built run cannot look complete. The primary
GLMM of A5.2 is sdr/meta.py's (not written); DL here is the SAP A5.3(a) estimator and is
labelled so.

Outputs: analysis/{flow,descriptives,availability,quality_analysis,pooled_variants,grid_coverage}.json,
tables/<name>_<key>.csv for the count tables (integer cells), the A4 blocks merged into
analysis/quality.json (PIPELINE.md stage 7; sdr.quality carries them over on a rerun), and this
invocation appended to <run-dir>/run_meta.json.
CLI: python -m sdr.stats --run-dir R --run-date D [--analyses all|flow,descriptives,availability,quality,variants,grid]
[--charting-dir charting/datasets] [--probes-dir charting/probes] [--limit N] [--dry-run] [--check-flow] [--selftest]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from sdr.common import RunDir, add_common_args, dump_json, init_run_dir, review_root
from sdr.descriptives import (ENUMS, PROJ_MODALITIES, YEAR_BANDS, _sec, _sum_median, _xt, descriptives,  # noqa: F401 (re-exported for tests/)
                              load_datasets, totals_keep, year_band)
from sdr.estimators import (clopper_pearson, dl_logit, dunn_holm, epsilon_squared, kruskal,  # noqa: F401 (re-exported for tests/)
                            selftest as estimators_selftest, spearman_ci, trend_test, wilson)
from sdr.flow_counts import flow, flow_identities, nest_flow  # noqa: F401 (re-exported for tests/)
from sdr.quality import file_url_confirmed, load_file_probes, scores_sha1

RECIPE_ROUTES = {"open-download", "registration"}
FIGURE_SOURCES = ("openi", "commons", "multicare", "openpmc", "jstage", "koreamed", "scielo", "redalyc")   # SAP A3.4


# ----------------------------------------------------------------------------- A3, A4, A5, A7
def status_class(p: dict) -> str:
    s = p.get("http_status")
    return "no-response" if s is None else f"{s // 100}xx"


def figure_pool(qs: dict) -> dict:
    """SAP A3.4: per query and per source, the figures or articles the figure-derived routes returned
    (queries.json counts only; no pooling). A source without a query is null, not zero."""
    per_q = {qid: {k: r.get(k) for k in ("source", "role", "hit_count_api", "n_retrieved", "run_date", "coverage")}
             for qid, r in sorted(qs.items()) if isinstance(r, dict) and r.get("source") in FIGURE_SOURCES}
    per_s = {}
    for s in FIGURE_SOURCES:
        rows = [r for r in per_q.values() if r["source"] == s]
        per_s[s] = {"n_queries": len(rows), "hit_count_api": sum(r["hit_count_api"] or 0 for r in rows) if rows else None,
                    "n_retrieved": sum(r["n_retrieved"] or 0 for r in rows) if rows else None}
    return {"per_query": per_q, "per_source": per_s, "note": "counts only (SAP A3.4); multicare and openpmc are charting-time routes without a query"}


def availability(ds: list[dict], qs: dict) -> dict:
    E, pub = ENUMS, [d for d in ds if d["described_as_public"] == "yes"]
    fp = [d for d in ds if d.get("file_url_probed")]
    landing = lambda d: [p for p in d["access_probe"] if p.get("url") != d.get("file_url_probed")]
    changed = sorted(d["id"] for d in ds if len(landing(d)) >= 2 and (landing(d)[0]["classification_machine"] != landing(d)[1]["classification_machine"]
                                                                      or status_class(landing(d)[0]) != status_class(landing(d)[1])))
    bands = {lab: wilson(sum(d["access_route"] == "unavailable" for d in ds if lo <= d["year"] <= hi), sum(lo <= d["year"] <= hi for d in ds))
             for lo, hi, lab in YEAR_BANDS}
    ver = [d["access_route_rule"] for d in ds if d["access_route_rule"].startswith("verifier")]
    overall = {r: 0 for r in E["route"]}
    overall.update(Counter(d["access_route"] for d in ds))
    v = {"route_distribution": {"overall": dict(sorted(overall.items())),
                                "by_modality": _xt(ds, lambda d: d["modality"], lambda d: [d["access_route"]], E["modality"], E["route"]),
                                "by_year_band": _xt(ds, lambda d: [year_band(d["year"])], lambda d: [d["access_route"]], E["year_band"], E["route"]),
                                "by_host_type": _xt(ds, lambda d: [d["host_type"]], lambda d: [d["access_route"]], E["host_type"], E["route"])},
         "route_x_modality": _xt(ds, lambda d: d["modality"], lambda d: [d["access_route"]], E["modality"], E["route"]),
         "route_x_year_band": _xt(ds, lambda d: [year_band(d["year"])], lambda d: [d["access_route"]], E["year_band"], E["route"]),
         "route_x_host_type": _xt(ds, lambda d: [d["host_type"]], lambda d: [d["access_route"]], E["host_type"], E["route"]),
         "described_public_downloads": {"primary": wilson(sum(d["access_route"] == "open-download" for d in pub), len(pub)),
                                        "file_url": wilson(sum(file_url_confirmed(d) for d in fp), len(fp)),
                                        "recipe_eligible": wilson(sum(d["access_route"] in RECIPE_ROUTES for d in pub), len(pub)),
                                        "file_url_rule": "file URL answered 200/206 on two distinct probe dates (charting/probes/<id>.json file_probes[] or access_probe[] on that url)"},
         "verifier_overrides": {"n": len(ver), "n_datasets": len(ds), "reasons": sorted(ver)},
         "route_rule_distribution": dict(sorted(Counter(d["access_route_rule"].split(":")[0] for d in ds).items())),
         "probe_agreement": {"changed_between_probes": changed, "n_changed": len(changed), "n_third_probe": sum(len(landing(d)) >= 3 for d in ds),
                             "rule": "classification_machine or HTTP status class (2xx/3xx/4xx/5xx/no-response) differs between the first two landing probes"},
         "figure_pool": figure_pool(qs), "unavailable_x_year_band": bands,
         "trend_unavailable_by_band": trend_test([[b["numerator"] for b in bands.values()], [b["denominator"] - b["numerator"] for b in bands.values()]])}
    return _sec(v, ["charting/datasets/*.json", "charting/probes/*.json", "<run-dir>/queries.json"], "SAP A3 (trend test exploratory)")


def quality_analysis(ds: list[dict], qual: dict) -> dict:
    qd = qual.get("per_dataset", {})
    rows = [(d, qd[d["id"]]) for d in ds if d["id"] in qd]
    ann = [(d, q) for d, q in rows if q["annotated"]]

    def dist(sub):
        t = [q["total"] for _, q in sub]
        return {"n": len(t), **({"median": float(np.percentile(t, 50)), "iqr": [float(np.percentile(t, 25)), float(np.percentile(t, 75))],
                                  "min": min(t), "max": max(t), "histogram": {str(k): c for k, c in sorted(Counter(t).items())}} if t else {})}

    def mclass(d):
        el = set(d["modality"]) - {"MRI", "other"}
        return "multi-modal" if len(el) > 1 else "CT-only" if el <= {"CT", "CBCT"} else "projection-only"

    def grouped(sub, keyf, field, posthoc):       # epsilon2 and Dunn on the annotated stratum only (SAP A4.3)
        g = defaultdict(list)
        for d, q in sub:
            g[keyf(d)].append(q[field])
        return kruskal(g, posthoc=posthoc)

    fit = {k: sorted(d["id"] for d, q in rows if q[k]) for k in ("fit_level_id", "usable_for_training", "fit_variant", "fit_stitching")}
    ns = [(d, q) for d, q in ann if d.get("n_subjects")]
    strata = (("annotated", ann, True), ("all", rows, False))
    tot = dist(rows)
    v = {"total": {"all": tot, "annotated": dist(ann), "unannotated": dist([r for r in rows if not r[1]["annotated"]]),
                   "median": tot.get("median"), "q1": (tot.get("iqr") or [None, None])[0], "q3": (tot.get("iqr") or [None, None])[1]},
         "item_share": qual.get("summary", {}).get("item_share"),
         "total_vs_modality": {s: grouped(sub, mclass, "total", ph) for s, sub, ph in strata},
         "total_vs_route": {s: grouped(sub, lambda d: d["access_route"], "total", ph) for s, sub, ph in strata},
         "total_vs_route_without_q7": {s: grouped(sub, lambda d: d["access_route"], "total_without_q7", ph) for s, sub, ph in strata},
         "total_vs_route_without_q6_q7_q8": {s: grouped(sub, lambda d: d["access_route"], "total_without_q6_q7_q8", ph) for s, sub, ph in strata},
         "total_vs_year": {s: spearman_ci([d["year"] for d, _ in sub], [q["total"] for _, q in sub]) for s, sub, _ in strata},
         "total_vs_log10_subjects": spearman_ci([math.log10(d["n_subjects"]) for d, _ in ns], [q["total"] for _, q in ns]),
         "scatter": [{"id": d["id"], "year": d["year"], "total": q["total"], "annotated": q["annotated"], "route": d["access_route"]} for d, q in rows],
         "fitness": {**{k: {"n": len(ids), "ids": ids, "by_modality": _xt([d for d, q in rows if q[k]], lambda d: d["modality"], lambda d: ["n"], ENUMS["modality"])}
                        for k, ids in fit.items()},
                     "subjects_fit_level_id": _sum_median([d.get("n_subjects") for d, q in rows if q["fit_level_id"]]),
                     "fail_rule": {**{r: 0 for r in ("F1", "F2", "F3", "F4")}, **Counter(q["fit_level_id_fail_rule"] for _, q in rows if not q["fit_level_id"])}}}
    return _sec(v, ["analysis/quality.json", "charting/datasets/*.json"], "SAP A4 (tests exploratory)")


def pooled_variants(ds: list[dict]) -> dict:
    """A5: per-dataset exact proportions (primary); DL pooling of the unselected stratum and of the
    enriched stratum separately, each only when k >= 5. The family/overlap rule is applied per variant
    with that variant's n_subjects_assessed as n_i (SAP general rules: the largest n_i for that analysis)."""
    out = {}
    for var in ("L6", "T13", "LSTV"):
        tk, rows = totals_keep(ds, lambda d, v=var: d["variant_labels"][v]["n_subjects_assessed"]), []
        for d in sorted(ds, key=lambda d: (d["year"], d["id"])):
            vl = d["variant_labels"][var]
            if vl["n_subjects_with"] is None or not vl["n_subjects_assessed"] or vl["unit"] != "subject":
                continue
            bad = [r for r, b in (("n<20", vl["n_subjects_assessed"] < 20), ("ascertainment unknown", vl["ascertainment"] == "unknown"),
                                  ("definition not-defined", vl["definition_class"] == "not-defined"), ("unverified", d.get("verified_by") is None),
                                  ("figure-derived", d["flags"]["figure_derived"]), ("family/overlap duplicate", d["id"] not in tk["keep"])) if b]
            rows.append({"id": d["id"], "year": d["year"], "modality": d["modality"], **clopper_pearson(vl["n_subjects_with"], vl["n_subjects_assessed"]),
                         "selection": vl["selection"], "ascertainment": vl["ascertainment"], "definition_class": vl["definition_class"],
                         "poolable": not bad and vl["selection"] == "consecutive-or-unselected", "enriched": not bad and vl["selection"] == "enriched",
                         "ineligible_reasons": bad})
        strata = {}
        for name, flag in (("unselected", "poolable"), ("enriched", "enriched")):
            sub = [r for r in rows if r[flag]]
            strata[name] = {"k": len(sub), "ids": [r["id"] for r in sub], "pooled": dl_logit([r["x"] for r in sub], [r["n"] for r in sub]) if len(sub) >= 5 else None,
                            "note": None if len(sub) >= 5 else f"pooling not done (k = {len(sub)} < 5)"}
        out[var] = {"per_dataset": rows, "k_eligible": strata["unselected"]["k"], "pooled": strata["unselected"]["pooled"],
                    "note": strata["unselected"]["note"], "enriched": strata["enriched"], "totals_rule": tk}
    out["estimator_note"] = "DL on the logit scale is the SAP A5.3(a) sensitivity estimator; the primary GLMM is sdr/meta.py"
    return _sec(out, ["charting/datasets/*.json"], "SAP A5 (secondary, illustrative)")


def grid_coverage(ds: list[dict], qual: dict) -> dict:
    qd, E = qual.get("per_dataset", {}), ENUMS
    on = lambda d: d["on_grid"]["status"] in ("yes", "partial")
    reach = [d for d in ds if d["access_route"] in RECIPE_ROUTES]
    fit = [d for d in ds if qd.get(d["id"], {}).get("fit_level_id")]
    v = {"overall": {"n_on_grid": sum(on(d) for d in ds), "n_partial": sum(d["on_grid"]["status"] == "partial" for d in ds),
                     "n_reachable": len(reach), "n_reachable_not_on_grid": sum(not on(d) for d in reach), "n_datasets": len(ds)},
         "status_x_modality": _xt(ds, lambda d: d["modality"], lambda d: [d["on_grid"]["status"]], E["modality"], E["on_grid"]),
         "status_x_region": _xt(ds, lambda d: d["region"], lambda d: [d["on_grid"]["status"]], E["region"], E["on_grid"]),
         "subjects_on_grid_over_reachable": {"on_grid": sum(d["on_grid"]["n_subjects_on_grid"] or 0 for d in reach if on(d)),
                                             "reachable": _sum_median([d.get("n_subjects") for d in reach])["sum"]},
         "fit_level_id_on_grid": wilson(sum(on(d) for d in fit), len(fit)),
         "per_dataset": [{"id": d["id"], "status": d["on_grid"]["status"], "path": d["on_grid"]["path"], "n_subjects_on_grid": d["on_grid"]["n_subjects_on_grid"],
                          "access_route": d["access_route"], "fit_level_id": bool(qd.get(d["id"], {}).get("fit_level_id"))} for d in sorted(ds, key=lambda d: d["id"])],
         "recipe_order": [{"id": d["id"], "quality_total": qd[d["id"]]["total"], "access_route": d["access_route"], "n_subjects": d.get("n_subjects")}
                          for d in sorted(fit, key=lambda d: (-qd[d["id"]]["total"], d["id"])) if d in reach and not on(d)],
         "note": "SO4 is author-specific and not reproducible by a second team"}
    return _sec(v, ["charting/datasets/*.json", "analysis/quality.json", "grid_inventory.csv"], "SAP A7")


# ----------------------------------------------------------------------------- output and CLI
def write_tables(name: str, sec: dict, tdir: Path) -> list[str]:
    """tables/<name>_<key>.csv: the dataset table; by_* strata flattened to n_datasets and the subject and
    image sums/medians; *_x_* cross-tabulations whose cells are integer counts. Anything else stays JSON-only.

    Counts are written as integers, not floats. A by_ stratum that holds a None in any column (a sum no
    dataset in that stratum contributes to) would otherwise promote the whole frame to float and put
    `1.0` and `70.0` in front of a reader; n_datasets and n_subjects_n_known are always known so they
    cast to int, and the two sums use pandas' nullable Int64 so an unknown sum stays an empty cell
    rather than becoming a zero."""
    written = []
    for key, val in sec["value"].items():
        if key == "table":
            df = pd.DataFrame(val)
        elif key.startswith("by_") and isinstance(val, dict) and val:
            df = pd.DataFrame({k: {c: v[c] for c in ("n_datasets", "n_subjects_sum", "n_subjects_median", "n_subjects_n_known", "n_images_sum", "n_images_median")}
                               for k, v in val.items()}).T.sort_index()
            df[["n_datasets", "n_subjects_n_known"]] = df[["n_datasets", "n_subjects_n_known"]].astype(int)
            df[["n_subjects_sum", "n_images_sum"]] = df[["n_subjects_sum", "n_images_sum"]].astype("Int64")
        elif "_x_" in key and isinstance(val, dict) and val and all(isinstance(v, dict) and all(isinstance(c, (int, float)) or c is None for c in v.values()) for v in val.values()):
            df = pd.DataFrame(val).T.sort_index().fillna(0).astype(int)
        else:
            continue
        p = tdir / f"{name}_{key}.csv"
        p.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(p, index=key != "table", lineterminator="\n")
        written.append(str(p))
    return written


def quality_problems(ds: list[dict], qual: dict, qpath: Path) -> list[str]:
    """SAP build rule: every dataset in charting/datasets/ is in analysis/quality.json and vice versa,
    and the file is the one sdr/quality.py wrote (scores_sha1 recomputed over per_dataset)."""
    if not qual:
        return [f"{qpath} absent while {len(ds)} charting record(s) are present"] if ds else []
    per, out = qual.get("per_dataset", {}), []
    diff = sorted({d["id"] for d in ds} ^ set(per))
    if diff:
        out.append(f"ids in charting but not in {qpath.name}, or vice versa: {', '.join(diff)}")
    if qual.get("scores_sha1") != scores_sha1(per):
        out.append(f"{qpath.name} scores_sha1 does not match its per_dataset (hand-edited or truncated); rerun sdr.quality")
    return out


def _selftest() -> int:
    """The estimator checks of sdr/estimators.py, then on tests/fixtures/stats (when tests/make_fixture.py
    has written it): the A3.2 file-URL row counts the file probes of charting/probes/<id>.json, and the
    per-modality subject sums equal the cumulative curve, with every route row present."""
    fails, fix = estimators_selftest(), review_root() / "tests" / "fixtures" / "stats"
    if (fix / "charting").exists():
        ds, fx = load_datasets(fix / "charting"), []
        for d in ds:
            load_file_probes(fix / "probes", d)
        fu = availability(ds, {})["value"]["described_public_downloads"]["file_url"]
        if (fu["numerator"], fu["denominator"]) != (10, 10):
            fx.append(f"fixture file_url row {fu['numerator']}/{fu['denominator']} != 10/10")
        de = descriptives(ds, {})["value"]
        bm, cum = de["by_modality"], de["cumulative_subjects_by_year_modality"]
        ct = sum(bm[m]["n_subjects_sum"] or 0 for m in ("CT", "CBCT"))
        xr = sum(bm[m]["n_subjects_sum"] or 0 for m in PROJ_MODALITIES)
        if (cum["CT"]["2026"], cum["radiography"]["2026"]) != (ct, xr):
            fx.append(f"cumulative 2026 (CT {cum['CT']['2026']}, XR {cum['radiography']['2026']}) != by_modality sums ({ct}, {xr})")
        if any(r not in de["by_access_route"] for r in ENUMS["route"]):
            fx.append("route rows not seeded from the schema")
        print(f"fixture checks (file_url {fu['numerator']}/{fu['denominator']}, cumulative CT {ct} XR {xr}, seeded routes):", "ok" if not fx else "FAIL")
        fails += fx
    else:
        print(f"fixture {fix} absent (tests/make_fixture.py); fixture checks skipped")
    print("stats selftest:", "ok" if not fails else "FAIL " + "; ".join(fails))
    return 1 if fails else 0


def main(argv: list[str] | None = None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.stats", description=__doc__.split("\n")[0]))
    ap.add_argument("--analyses", default="all", help="comma list of flow,descriptives,availability,quality,variants,grid")
    ap.add_argument("--charting-dir", default="charting/datasets")
    ap.add_argument("--probes-dir", default=None, help="sdr/availability.py probe histories (<id>.json with file_probes[]) for A3.2; "
                    "default: the `probes` directory beside --charting-dir (charting/probes)")
    ap.add_argument("--quality", default="analysis/quality.json")
    ap.add_argument("--screen-dir", default="screen", help="known_items.csv, prescreen_audit.csv, chase_manual.csv (protocol layout)")
    ap.add_argument("--decisions-dir", default="data/screening", help="reviewer CSVs looked up before --screen-dir (decisions.csv lives here)")
    ap.add_argument("--analysis-dir", default="analysis")
    ap.add_argument("--tables-dir", default="tables")
    ap.add_argument("--check-flow", action="store_true", help="exit 1 when a flow identity fails")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    root, rd = review_root(), RunDir(Path(a.run_dir))
    cdir, qpath = root / a.charting_dir, root / a.quality
    pdir = root / a.probes_dir if a.probes_dir else cdir.parent / "probes"
    ds = load_datasets(cdir, a.limit)
    for d in ds:
        load_file_probes(pdir, d)
    qual = json.loads(qpath.read_text(encoding="utf-8")) if qpath.exists() else {}
    problems = quality_problems(ds, qual, qpath)
    wanted = ("flow", "descriptives", "availability", "quality", "variants", "grid") if a.analyses == "all" else tuple(a.analyses.split(","))
    for p in problems:
        print(f"quality.json check: {p}" + ("  (allowed under --limit)" if a.limit else ""))
    if a.dry_run:
        print(f"would run {wanted} on {len(ds)} dataset(s) from {cdir}; quality.json {'present' if qual else 'ABSENT'}; probes from {pdir}; run dir {rd.root} "
              f"(queries.json {'present' if rd.queries_json.exists() else 'absent'}, merged.jsonl {'present' if rd.merged.exists() else 'absent'})")
        return 0
    if problems and not a.limit:
        return 1
    init_run_dir(a.run_dir, a.run_date, argv)
    runners = {"flow": lambda: flow(rd, root / a.screen_dir, cdir.parent, ds, root / a.decisions_dir), "descriptives": lambda: descriptives(ds, qual),
               "availability": lambda: availability(ds, rd.queries()), "quality": lambda: quality_analysis(ds, qual),
               "variants": lambda: pooled_variants(ds), "grid": lambda: grid_coverage(ds, qual)}
    names, rc = {"quality": "quality_analysis", "variants": "pooled_variants", "grid": "grid_coverage"}, 0
    for w in wanted:
        sec = runners[w]()
        sec["run_date"] = a.run_date
        out = root / a.analysis_dir / f"{names.get(w, w)}.json"
        dump_json(out, sec)
        if w == "quality" and qual:          # the manuscript reads the A4 results from quality.json itself (sdr.quality carries them over)
            qual.setdefault("summary", {})["total"] = sec["value"]["total"]
            qual.update({k: sec["value"][k] for k in ("fitness", "total_vs_year", "total_vs_route", "total_vs_modality")})
            qual["analysis_derived_from"] = sec["derived_from"]
            dump_json(qpath, qual)
        print(f"{w:13s} -> {out} ({len(write_tables(names.get(w, w), sec, root / a.tables_dir))} csv table(s))")
        if w == "flow":
            for k, ok in sec["value"]["identities"].items():
                print(f"   identity {'holds' if ok else 'FAILS' if ok is False else 'unknown (input missing)'}: {k}")
                rc |= int(a.check_flow and ok is False)
            if sec["value"]["missing_inputs"]:
                print("   missing inputs:", ", ".join(sec["value"]["missing_inputs"]))
    return rc


if __name__ == "__main__":
    sys.exit(main())
