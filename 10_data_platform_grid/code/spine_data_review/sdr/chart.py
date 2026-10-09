"""Validate the charting records against charting_schema.json, list what is missing, merge them (PROTOCOL.md 8, 9).

WHY VALIDATION IS THE MERGE STEP. Every number in the manuscript is computed from the charting
records, so a record that is malformed, unquoted or internally inconsistent must never reach
`analysis/`. This module is the gate: a record enters `charting/datasets.jsonl` only when it
passes (1) the JSON Schema, (2) the quote rule of `x-requires-quote` (a charted value that was
not produced by code carries a verbatim quote or names an API in `field_sources`), and (3) the
cross-field rules of `x-validate-rules` that JSON Schema cannot express, each implemented here
with the lookup tables the protocol names: `licence_tiers.csv` (licence text -> tier, spdx,
standard), the section-10 host table (access_url -> host_type), and the SAP A6.0 lookup
(statistic x annotation type read by rubric Q2 x comparator -> comparable_group).

The validator is a small draft-07 subset written here because the allowed dependencies
(PROTOCOL.md section 15) do not include `jsonschema`: $ref to #/definitions, type, enum,
const, pattern, min/max, minLength/maxLength, required, properties, additionalProperties,
items, minItems/maxItems, uniqueItems, contains, minProperties, allOf, oneOf, not, if/then/else.
That is every keyword the schema uses; an unknown keyword is ignored, never silently trusted,
and the list of keywords seen is written to the report so a schema edit that adds one is visible.

"What is missing" is reported at three levels: per record (schema errors, quote-less fields,
`verified_by` null, record ids absent from <run-dir>/merged.jsonl); across records (dataset ids
expected from `charting/aliases.csv` and the `recall` rows of `screen/known_items.csv` that have
no record yet, minus the known items seeded only as I1 tests or excluded under I4, which are
never meant to be charted); and across the run (charted ids with no alias row, which the mapping
step of 7.6 should have seeded). The one value filled by code in this step is `n_use_records`
from `charting/dataset_sources.csv` (columns record_id, dataset_id, role) when that file exists;
because every later stage reads `charting/datasets/<id>.json` directly, a changed value is
written back into that file (never on a dry run) and the ids written are listed in the report.

Reads  charting/datasets/<id>.json (or --charting-dir), charting_schema.json, licence_tiers.csv,
       charting/aliases.csv, charting/dataset_sources.csv, screen/known_items.csv,
       <run-dir>/merged.jsonl (all optional except the schema; each absence is reported, not fatal),
       --rechart-dir <dir> with the blind re-charts (rule: re-chart charted_date precedes verified_date).
Writes charting/datasets.jsonl (valid records, sorted by id) and charting/validation_report.json
       (or --out / --report). Exit 1 when any record has an error, unless --allow-invalid; exit 2
       when an explicitly given --charting-dir does not exist (the default directory absent is a
       warning and an empty gate, which `make chart-check` relies on before charting starts).

CLI: python -m sdr.chart --run-dir runs/<date> --run-date <date> [--charting-dir D] [--limit N]
     [--dry-run] [--allow-invalid] [--rechart-dir D] [--out F] [--report F]
Every relative path is resolved against spine_data_review/, as PIPELINE.md states, not against the
process cwd. No network. `--limit` validates the first N records by file name. `--dry-run` prints
the report and writes nothing.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from sdr import PROTOCOL_VERSION
from sdr.common import RunDir, add_common_args, dump_json, init_run_dir, read_jsonl, review_root, write_jsonl

Q2_ORDER = ("per-vertebra-level-names", "segmentation-3d", "segmentation-2d", "landmarks", "bounding-boxes", "centroids",
            "pathology-labels", "fracture-grade", "measurements", "radiology-reports", "image-level-labels")
# SAP A6.0: (statistic, annotation type read by Q2) -> comparable_group, rater-vs-rater only.
A6_LOOKUP = {("kappa", "per-vertebra-level-names"): "kappa-level-names", ("weighted-kappa", "per-vertebra-level-names"): "kappa-level-names",
             **{(s, t): "kappa-pathology" for s in ("kappa", "weighted-kappa") for t in ("pathology-labels", "fracture-grade", "image-level-labels")},
             ("dice", "segmentation-3d"): "dice-vertebra-3d", ("dice", "segmentation-2d"): "dice-2d", ("icc", "measurements"): "icc-measurement",
             ("distance-mm", "landmarks"): "mm-landmark", ("distance-mm", "centroids"): "mm-landmark"}
# Protocol section 10 host table: (host suffix or DOI prefix) -> host_type.
_REPO_HOSTS = ("zenodo.org", "figshare.com", "datadryad.org", "osf.io", "data.mendeley.com", "physionet.org",
               "cancerimagingarchive.net", "huggingface.co", "github.com")
_DOI_PREFIX_HOST = {"10.5281": "repository-api", "10.6084": "repository-api", "10.5061": "repository-api", "10.17605": "repository-api",
                    "10.17632": "repository-api", "10.13026": "repository-api", "10.7937": "repository-api"}
_CLOUD_HOSTS = ("drive.google.com", "dropbox.com", "onedrive.live.com", "1drv.ms", "box.com", "pan.baidu.com")
_INSTITUTIONAL_RE = re.compile(r"(\.edu$|\.edu\.[a-z]{2}$|\.ac\.[a-z]{2}$|\.gov$|\.gov\.[a-z]{2}$|\.nhs\.uk$|\buni-|\bunive?r|hospital|clinic|\.nih\.gov$)")
INELIGIBLE_MODALITIES = {"MRI", "other"}
EXEMPT_VALUES = ("unknown", None, False, "none", ["none"])
_KEYWORDS_SEEN: set[str] = set()


# ----------------------------------------------------------------------------- JSON Schema draft-07 subset
def _is_type(v, t: str) -> bool:
    if t == "integer":
        return (isinstance(v, int) and not isinstance(v, bool)) or (isinstance(v, float) and v.is_integer())
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "null":
        return v is None
    return isinstance(v, {"object": dict, "array": list, "string": str, "boolean": bool}[t])


def _eq(a, b) -> bool:
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def validate(schema: dict, v, root: dict, path: str = "$") -> list[str]:  # candidate for common.py
    """Errors of `v` against `schema` (draft-07 subset listed in the module docstring); [] when valid."""
    if "$ref" in schema:
        node = root
        for part in schema["$ref"].lstrip("#/").split("/"):
            node = node[part]
        return validate(node, v, root, path)
    _KEYWORDS_SEEN.update(schema.keys())
    errs: list[str] = []
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(v, t) for t in types):
            return [f"{path}: expected type {'/'.join(types)}, got {type(v).__name__}"]
    if "enum" in schema and not any(_eq(v, e) for e in schema["enum"]):
        errs.append(f"{path}: value {json.dumps(v, ensure_ascii=False)[:60]} not in enum {schema['enum']}")
    if "const" in schema and not _eq(v, schema["const"]):
        errs.append(f"{path}: must equal {schema['const']!r}")
    if isinstance(v, str):
        if "pattern" in schema and not re.search(schema["pattern"], v):
            errs.append(f"{path}: {v[:60]!r} does not match /{schema['pattern']}/")
        if "minLength" in schema and len(v) < schema["minLength"]:
            errs.append(f"{path}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(v) > schema["maxLength"]:
            errs.append(f"{path}: longer than {schema['maxLength']}")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if "minimum" in schema and v < schema["minimum"]:
            errs.append(f"{path}: {v} < minimum {schema['minimum']}")
        if "maximum" in schema and v > schema["maximum"]:
            errs.append(f"{path}: {v} > maximum {schema['maximum']}")
    if isinstance(v, dict):
        errs += [f"{path}: missing required key '{k}'" for k in schema.get("required", []) if k not in v]
        props = schema.get("properties", {})
        for k, sub in props.items():
            if k in v:
                errs += validate(sub, v[k], root, f"{path}.{k}")
        ap = schema.get("additionalProperties", True)
        for k in v:
            if k not in props:
                if ap is False:
                    errs.append(f"{path}: unexpected key '{k}'")
                elif isinstance(ap, dict):
                    errs += validate(ap, v[k], root, f"{path}.{k}")
        if "minProperties" in schema and len(v) < schema["minProperties"]:
            errs.append(f"{path}: fewer than {schema['minProperties']} keys")
    if isinstance(v, list):
        if "items" in schema:
            for i, x in enumerate(v):
                errs += validate(schema["items"], x, root, f"{path}[{i}]")
        if "minItems" in schema and len(v) < schema["minItems"]:
            errs.append(f"{path}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(v) > schema["maxItems"]:
            errs.append(f"{path}: more than {schema['maxItems']} items")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in v}) != len(v):
            errs.append(f"{path}: items are not unique")
        if "contains" in schema and not any(not validate(schema["contains"], x, root, path) for x in v):
            errs.append(f"{path}: no item satisfies 'contains' {json.dumps(schema['contains'])[:80]}")
    for sub in schema.get("allOf", []):
        errs += validate(sub, v, root, path)
    if "oneOf" in schema and sum(not validate(sub, v, root, path) for sub in schema["oneOf"]) != 1:
        errs.append(f"{path}: must match exactly one of {len(schema['oneOf'])} alternatives")
    if "not" in schema and not validate(schema["not"], v, root, path):
        errs.append(f"{path}: matches a forbidden schema {json.dumps(schema['not'])[:80]}")
    if "if" in schema:
        branch = "then" if not validate(schema["if"], v, root, path) else "else"
        if branch in schema:
            errs += validate(schema[branch], v, root, path)
    return errs


# ----------------------------------------------------------------------------- lookups the cross-field rules need
def load_licence_tiers(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []


_CC_VERSION_RE = re.compile(r"\b([234]\.0)\b")


def licence_lookup(text: str, tiers: list[dict]) -> dict | None:
    """The first row of licence_tiers.csv whose pattern matches `text` (the table ends in a
    catch-all). For a CC-BY family row the version is read from the text, as the table's note
    says: 'CC BY 3.0' charts as CC-BY-3.0 (TCIA collections are commonly 3.0), and 4.0 stays the
    default when the text names none."""
    for row in tiers:
        if re.search(row["pattern"], text or ""):
            spdx = row["spdx"] or None
            if spdx and spdx.startswith("CC-BY") and (m := _CC_VERSION_RE.search(text or "")):
                spdx = re.sub(r"\d\.0$", m.group(1), spdx)
            return {"tier": row["tier"], "spdx": spdx, "standard": row["standard"].strip().lower() == "yes"}
    return None


def host_type_for(url: str | None) -> tuple[str, bool]:
    """(host_type from the section-10 host table, certain). doi.org links are classified by DOI
    prefix without resolving; 'institutional' vs 'unknown' is a heuristic and is flagged uncertain
    so a mismatch there is a warning, not an error."""
    if not url:
        return "unknown", True
    p = urlsplit(url)
    host, path = p.netloc.lower().split("@")[-1].split(":")[0], p.path.lower()
    if host in ("doi.org", "dx.doi.org", "hdl.handle.net"):
        prefix = path.strip("/").split("/")[0]
        return _DOI_PREFIX_HOST.get(prefix, "unknown"), prefix in _DOI_PREFIX_HOST
    if host == "grand-challenge.org" or host.endswith(".grand-challenge.org"):
        return "challenge-platform", True
    if host.endswith("kaggle.com"):
        return ("challenge-platform" if re.match(r"^/(c|competitions)/", path) else "repository-api"), True
    if any(host == h or host.endswith("." + h) for h in _REPO_HOSTS):
        return "repository-api", True
    if any(host == h or host.endswith("." + h) for h in _CLOUD_HOSTS):
        return "personal-or-cloud-drive", True
    return ("institutional" if _INSTITUTIONAL_RE.search(host) else "unknown"), False


def q2_type_read(rec: dict) -> str | None:
    return next((t for t in Q2_ORDER if t in rec.get("annotation_types", [])), None)


def comparable_group_for(rec: dict) -> str | None:
    av = rec.get("annotation_validation") or {}
    if av.get("comparator") != "rater-vs-rater":
        return None
    return A6_LOOKUP.get((av.get("inter_rater_statistic"), q2_type_read(rec)))


def _get(rec: dict, dotted: str):
    v = rec
    for part in dotted.split("."):
        v = v.get(part) if isinstance(v, dict) else None
    return v


# ----------------------------------------------------------------------------- quote rule and cross-field rules
def quote_errors(rec: dict, schema: dict) -> list[str]:
    """x-requires-quote: each listed field needs a quote whose `field` equals its dot path, or a
    field_sources entry starting 'api:'; exempt when the value is unknown/null/false/none."""
    quoted = {q.get("field") for q in rec.get("quotes", []) if isinstance(q, dict)}
    fs, errs = rec.get("field_sources") or {}, []
    for field in schema.get("x-requires-quote", []):
        paths = [f"metadata_elements.{e}" for e in rec.get("metadata_elements", [])] if field == "metadata_elements.*" else [field]
        for p in paths:
            v = rec.get("metadata_elements") if field == "metadata_elements.*" else _get(rec, p)
            v = v.get("status") if isinstance(v, dict) and "status" in v else v  # a variant object is judged by its status
            if any(_eq(v, x) for x in EXEMPT_VALUES) or (isinstance(v, list) and not v):
                continue
            if p not in quoted and not str(fs.get(p, "")).startswith("api:"):
                errs.append(f"quote: '{p}' (value {json.dumps(v, ensure_ascii=False)[:40]}) has no quote and no api: field_sources entry")
    return errs


def cross_field_errors(rec: dict, tiers: list[dict], rechart: dict | None) -> tuple[list[str], list[str]]:
    """(errors, warnings) for x-validate-rules; each message names the rule it implements."""
    errs, warns = [], []
    types, by_type = set(rec.get("annotation_types", [])), rec.get("annotation_origin_by_type") or {}
    if set(by_type) - types:
        errs.append(f"rule origin_by_type: keys {sorted(set(by_type) - types)} not in annotation_types")
    for t in sorted(types - {"none"} - set(by_type)):
        errs.append(f"rule origin_by_type: annotation type '{t}' has no annotation_origin_by_type entry")
    probes = [p for p in rec.get("access_probe", []) if isinstance(p, dict)]
    real = [p for p in probes if p.get("method") != "none"]
    if real:
        if len(probes) < 2:
            errs.append("rule probes: a probed dataset needs at least two probes")
        else:
            try:
                d0, d1 = (date.fromisoformat(probes[i]["date"]) for i in (0, 1))
                if abs((d1 - d0).days) < 2:
                    errs.append(f"rule probes: first two probe dates {d0} and {d1} are less than 48 h apart")
            except (KeyError, ValueError, TypeError):
                errs.append("rule probes: probe dates are not ISO dates")
    route, rule = rec.get("access_route"), rec.get("access_route_rule") or ""
    if not rule.startswith("verifier:"):
        agreeing = {p.get("rule") for p in probes if p.get("classification_machine") == route}
        stated = set(rule.split("/")) if rule else set()
        if stated != agreeing:
            errs.append(f"rule access_route_rule: '{rule}' but probes agreeing with '{route}' fired {sorted(agreeing, key=str)}")
    flags = rec.get("flags") or {}
    if flags.get("multi_modal"):
        eligible = {m for m in rec.get("modality", []) if m not in INELIGIBLE_MODALITIES}
        if set((rec.get("n_per_modality") or {}).keys()) != eligible:
            errs.append(f"rule multi_modal: n_per_modality keys must be exactly the eligible modalities {sorted(eligible)}")
    if flags.get("authors_own") and rec.get("verified_by") in (flags.get("maintainer_authors") or []):
        errs.append("rule authors_own: verified_by is a maintainer author")
    if flags.get("figure_derived") and rec.get("n_subjects_basis") not in ("estimated", "unknown"):
        errs.append("rule figure_derived: n_subjects_basis must be estimated or unknown")
    lic = rec.get("licence") or {}
    exp = licence_lookup(lic.get("text", ""), tiers) if tiers else None
    if exp is None and tiers:
        errs.append("rule licence: no licence_tiers.csv row matches licence.text (the table should end in a catch-all)")
    elif exp and any(lic.get(k) != exp[k] for k in ("tier", "spdx", "standard")):
        errs.append(f"rule licence: tier/spdx/standard must be {exp} for text {lic.get('text')!r}, got "
                    f"{ {k: lic.get(k) for k in ('tier', 'spdx', 'standard')} }")
    cg = comparable_group_for(rec)
    if (rec.get("annotation_validation") or {}).get("comparable_group") != cg:
        errs.append(f"rule comparable_group: SAP A6.0 lookup gives {cg!r} (statistic x type read by Q2 x comparator)")
    ht, certain = host_type_for(rec.get("access_url"))
    if rec.get("host_type") != ht:
        (errs if certain else warns).append(f"rule host_type: host table gives '{ht}' for {rec.get('access_url')!r}, charted '{rec.get('host_type')}'")
    met = set((rec.get("eligibility") or {}).get("criteria_met", []))
    if ("I7" in met) != bool(flags.get("figure_derived")) or ("I8" in met) != bool(flags.get("derived")):
        errs.append("rule criteria_met: I7 iff flags.figure_derived and I8 iff flags.derived")
    if rechart is not None:
        rc, vd = rechart.get("charted_date"), rec.get("verified_date")
        if not (rc and vd and rc < vd):
            errs.append(f"rule rechart: re-chart charted_date {rc} must precede verified_date {vd}")
    if rec.get("verified_by") is None:
        warns.append("verified_by is null: required before analysis (PROTOCOL.md section 8)")
    return errs, warns


# ----------------------------------------------------------------------------- driver
def _csv_rows(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []


def check_all(files: list[Path], schema: dict, tiers: list[dict], root: Path, rechart_dir: Path | None, merged_ids: set[str] | None,
              write_back: bool = False) -> tuple[dict, list[dict]]:
    """Validate every file; return (report, valid records). Never raises on a bad record.
    `n_use_records` is the one value this step fills: with `write_back` a changed value is written
    into charting/datasets/<id>.json itself (every later stage reads those files, not the jsonl),
    and the ids written are listed in the report; without it (dry run) the file is left alone."""
    per, valid, use_counts, written = {}, [], {}, []
    for r in _csv_rows(root / "charting" / "dataset_sources.csv"):
        if (r.get("role") or "").strip() == "use":
            use_counts[r.get("dataset_id", "")] = use_counts.get(r.get("dataset_id", ""), 0) + 1
    for f in files:
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            per[f.stem] = {"file": f.name, "errors": [f"unreadable JSON: {e}"], "warnings": [], "valid": False}
            continue
        errs = validate(schema, rec, schema) if isinstance(rec, dict) else ["top level is not an object"]
        warns: list[str] = []
        if isinstance(rec, dict):
            if rec.get("id") != f.stem:
                errs.append(f"id '{rec.get('id')}' differs from file name '{f.stem}'")
            errs += quote_errors(rec, schema)
            rc = None
            if rechart_dir and (rechart_dir / f.name).exists():
                rc = json.loads((rechart_dir / f.name).read_text(encoding="utf-8"))
            e2, warns = cross_field_errors(rec, tiers, rc)
            errs += e2
            if merged_ids is not None:
                missing = sorted(set((rec.get("source_record") or {}).get("record_ids", [])) - merged_ids)
                if missing:
                    warns.append(f"record_ids not in merged.jsonl: {missing}")
            if f.stem in use_counts and rec.get("n_use_records") != use_counts[f.stem]:
                warns.append(f"n_use_records {rec.get('n_use_records')} replaced by {use_counts[f.stem]} from dataset_sources.csv"
                             + (" and written to the file" if write_back else " (dry run: file not written)"))
                rec["n_use_records"] = use_counts[f.stem]
                if write_back:
                    dump_json(f, rec)
                    written.append(f.stem)
        per[f.stem] = {"file": f.name, "errors": errs, "warnings": warns, "valid": not errs,
                       "q2_type_read": q2_type_read(rec) if isinstance(rec, dict) else None}
        if not errs:
            valid.append(rec)
    # Expected datasets: the recall known items plus every alias-table id, minus the known items
    # seeded only to test I1 or excluded under I4, which are meant never to be charted.
    known = _csv_rows(root / "screen" / "known_items.csv")
    not_expected = {r["item"] for r in known if (r.get("role") or "").strip() in ("I1-test", "excluded-I4")}
    expected = ({r["dataset_id"] for r in _csv_rows(root / "charting" / "aliases.csv")} - not_expected) | \
               {r["item"] for r in known if (r.get("role") or "").strip() == "recall"}
    charted = set(per)
    report = {"protocol_version": PROTOCOL_VERSION, "n_files": len(files), "n_valid": len(valid),
              "n_invalid": len(files) - len(valid), "n_unverified": sum(1 for r in valid if r.get("verified_by") is None),
              "datasets": dict(sorted(per.items())), "expected_not_charted": sorted(expected - charted),
              "not_expected_known_items": sorted(not_expected), "charted_without_alias_row": sorted(charted - expected),
              "n_use_records_written": sorted(written), "schema_keywords_seen": sorted(_KEYWORDS_SEEN),
              "dataset_sources_csv_present": bool(use_counts) or (root / "charting" / "dataset_sources.csv").exists()}
    return report, valid


def main(argv: list[str] | None = None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.chart", description=__doc__.split("\n")[0]))
    root = review_root()
    ap.add_argument("--charting-dir", default=None, help="directory of <id>.json records (default charting/datasets; relative to spine_data_review/)")
    ap.add_argument("--schema", default="charting_schema.json")
    ap.add_argument("--rechart-dir", default=None, help="blind re-charts <id>.json (protocol 8 date-order rule)")
    ap.add_argument("--out", default="charting/datasets.jsonl")
    ap.add_argument("--report", default="charting/validation_report.json")
    ap.add_argument("--allow-invalid", action="store_true", help="exit 0 even when a record has errors")
    a = ap.parse_args(argv)
    # A --limit run charts the first N records only, so it must never write the committed gate outputs:
    # charting/datasets.jsonl is what every later stage reads, and a five-record copy of it is silently
    # wrong. The Makefile redirects both under the run directory; this refuses the case it cannot see.
    if a.limit and (a.out == ap.get_default("out") or a.report == ap.get_default("report")):
        print(f"--limit {a.limit} with the default --out/--report would truncate {ap.get_default('out')} and "
              f"{ap.get_default('report')} to {a.limit} records; redirect both under a run directory "
              "(--out <run>/charting/datasets.jsonl --report <run>/charting/validation_report.json)", file=sys.stderr)
        return 2
    # PIPELINE.md: relative paths are relative to spine_data_review/, never to the process cwd.
    under_root = lambda p: (Path(p) if Path(p).is_absolute() else root / p)  # noqa: E731
    charting_dir = under_root(a.charting_dir or "charting/datasets")
    if not charting_dir.is_dir():
        print(f"{'ERROR' if a.charting_dir else 'warning'}: charting directory {charting_dir} does not exist", file=sys.stderr)
        if a.charting_dir:                      # an explicit directory that is absent is a mistake, not an empty gate
            return 2
    schema_path, out, report_path = under_root(a.schema), under_root(a.out), under_root(a.report)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    files = sorted(charting_dir.glob("*.json"))[: a.limit or None]
    rd = RunDir(Path(a.run_dir)) if a.dry_run else init_run_dir(a.run_dir, a.run_date, argv)
    # A record id may be a merged representative or a member folded into one (dedup_prescreen member_record_ids).
    merged_ids = {i for r in read_jsonl(rd.merged) for i in [r["record_id"], *r.get("member_record_ids", [])]} if rd.merged.exists() else None
    report, valid = check_all(files, schema, load_licence_tiers(root / "licence_tiers.csv"), root,
                              under_root(a.rechart_dir) if a.rechart_dir else None, merged_ids, write_back=not a.dry_run)
    rel = lambda p: str(Path(p).relative_to(root)) if root in Path(p).parents else str(p)  # noqa: E731
    report.update({"run_date": a.run_date, "charting_dir": rel(charting_dir), "merged_jsonl_present": merged_ids is not None,
                   "derived_from": [rel(schema_path), "licence_tiers.csv", *[rel(f) for f in files]]})
    for did, d in report["datasets"].items():
        for m in d["errors"]:
            print(f"ERROR   {did}: {m}")
        for m in d["warnings"]:
            print(f"warning {did}: {m}")
    print(f"{report['n_valid']} valid, {report['n_invalid']} invalid, {report['n_unverified']} unverified of {report['n_files']} records; "
          f"expected but not charted: {report['expected_not_charted']}")
    if a.dry_run:
        print("dry run; would write", out, "and", report_path)
    else:
        write_jsonl(out, valid, key=lambda r: r["id"])
        dump_json(report_path, report)
        print(f"wrote {out} ({len(valid)} rows) and {report_path}"
              + (f"; n_use_records written into {len(report['n_use_records_written'])} record file(s)" if report["n_use_records_written"] else ""))
    return 0 if a.allow_invalid or report["n_invalid"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
