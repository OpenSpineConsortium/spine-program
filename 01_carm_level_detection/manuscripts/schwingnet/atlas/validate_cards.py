"""Validate the two ATLAS cards against the 2025-11 schema summary recorded in README.md.

Checks: JSON parses; required fields; Name length; Link is a URI; Summary length; every
enum value used is in the schema summary; no key outside the summarised property lists
(additionalProperties is false everywhere in the real schema); Date fields are YYYY-MM-DD
or a year; Age range shape; Content codes are two letters. Exits non-zero on any failure.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

DESCRIPTOR_KEYS = {"Authors", "Comments", "Contact", "Date", "Ethical review", "Funding",
                   "License", "Organizations", "References", "Version"}
AUTHOR_KEYS = {"Name", "Email", "ORCID", "URL"}
ORG_KEYS = {"Name", "Contact name", "Email", "Address", "URL"}
REF_KEYS = {"Title", "Authors", "Source", "Date", "DOI", "URL", "PMID", "PMCID", "Notes"}
DATE_KEYS = {"Created", "Published", "Updated"}
INDEXING_KEYS = {"Content", "RadLex", "SNOMED", "Keywords"}

MODEL_TOP = {"Name", "Link", "Summary", "Indexing", "Descriptors", "Model properties",
             "Imaging", "Model performance"}
MODEL_PROPS = {"Architecture", "Availability", "Clinical benefit", "Clinical workflow phase",
               "Decision threshold", "Degree of automation", "Indications for use", "Input",
               "Instructions", "Limitations", "Output", "Recommendation",
               "Regulatory information", "Reproducibility", "Sustainability", "Use", "User",
               "EHR compatibility"}
REG_KEYS = {"FDA cleared", "CE marked", "Predicate device", "Authorization status",
            "File number", "Comment"}
USE_ENUM = {"Detection", "Decision support", "Image processing", "Other"}
USER_ENUM = {"Physician", "Subspecialist diagnostic radiologist", "Interventional radiologist",
             "Radiology technologist", "Researcher"}
USE_KEYS = {"Intended", "Out-of-scope", "Excluded"}
MODEL_IMAGING = {"Modalities", "Procedures", "File format", "Resolution", "Comments"}
PROC_KEYS = {"Name", "RadLex", "LOINC"}
FILE_FORMAT_ENUM = {"DICOM", "JPEG", "NiFTI", "PNG", "Other"}
METRIC_ENUM = {"accuracy", "sensitivity", "F1 score", "other"}
PERF_KEYS = {"Metrics", "Comments"}

DATASET_TOP = {"Name", "Link", "Summary", "Indexing", "Descriptors", "Dataset properties",
               "Imaging", "Partitions"}
DATASET_PROPS = {"Confidentiality", "External data", "Missing information", "Motivation",
                 "Noise", "Partitioning scheme", "Re-identification",
                 "Relationships between instances", "Sampling", "Sensitive data"}
DATASET_IMAGING = {"Modalities", "Procedures", "File format", "Resolution", "Pre-processing",
                   "Burned-in PHI", "Comments"}
PHI_ENUM = {"Yes", "No", "Unknown"}
PARTITION_ENUM = {"Training", "Optimization", "Validation", "Internal testing",
                  "External testing", "Tuning", "Hold-out", "Development", "Test", "Other"}
PARTITION_KEYS = {"Partition", "Total", "Subsets", "Comments"}
TOTAL_KEYS = {"Site count", "Patient count", "Exam count", "Series count", "Image count",
              "Age range", "Sex", "Demographic", "Criterion", "Comments"}

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def check_keys(obj, allowed, where):
    extra = set(obj) - allowed
    if extra:
        err(f"{where}: keys not in schema summary: {sorted(extra)}")


def check_date(s, where):
    if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", s) or re.fullmatch(r"\d{4}", s)):
        err(f"{where}: date '{s}' is not YYYY-MM-DD or a year")


def check_common(obj, where):
    if "Name" not in obj or not (4 <= len(obj["Name"]) <= 256):
        err(f"{where}: Name missing or not 4-256 chars")
    if "Link" not in obj or not re.match(r"^https?://\S+$", obj["Link"]):
        err(f"{where}: Link missing or not a URI")
    if "Summary" in obj and len(obj["Summary"]) > 2500:
        err(f"{where}: Summary is {len(obj['Summary'])} chars (> 2500)")
    idx = obj.get("Indexing", {})
    check_keys(idx, INDEXING_KEYS, where + ".Indexing")
    for c in idx.get("Content", []):
        if not re.fullmatch(r"[A-Z]{2}", c):
            err(f"{where}: Content code '{c}' is not two letters")
    for r in idx.get("RadLex", []):
        if not re.fullmatch(r"RID\d+", r):
            err(f"{where}: RadLex '{r}' is not RID...")
    for s in idx.get("SNOMED", []):
        if not isinstance(s, int):
            err(f"{where}: SNOMED '{s}' is not an int")
    for k in idx.get("Keywords", []):
        if not (2 <= len(k) <= 64):
            err(f"{where}: keyword '{k}' not 2-64 chars")
    d = obj.get("Descriptors", {})
    check_keys(d, DESCRIPTOR_KEYS, where + ".Descriptors")
    for a in d.get("Authors", []):
        check_keys(a, AUTHOR_KEYS, where + ".Authors")
    for o in d.get("Organizations", []):
        check_keys(o, ORG_KEYS, where + ".Organizations")
    seen_doi, seen_title = {}, {}
    for i, r in enumerate(d.get("References", [])):
        check_keys(r, REF_KEYS, where + ".References")
        if "Title" not in r:
            err(f"{where}: reference without Title")
        if "Date" in r:
            check_date(r["Date"], where + ".References")
        # a duplicate entry is a card-writer bug (2026-09-24: six copies of one reference had accumulated)
        doi = (r.get("DOI") or "").lower()
        if doi:
            if doi in seen_doi:
                err(f"{where}.References[{i}]: DOI {doi} duplicates References[{seen_doi[doi]}]")
            seen_doi.setdefault(doi, i)
        key = (r.get("Title", "").strip().lower(), r.get("Source", "").strip().lower())
        if key in seen_title:
            err(f"{where}.References[{i}]: title and source duplicate References[{seen_title[key]}]")
        seen_title.setdefault(key, i)
    dt = d.get("Date", {})
    check_keys(dt, DATE_KEYS, where + ".Date")
    for k, v in dt.items():
        check_date(v, where + f".Date.{k}")
    lic = d.get("License", {})
    check_keys(lic, {"Text", "URL"}, where + ".License")


def validate_model(path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    check_keys(doc, {"$schema", "Model"}, "model root")
    if doc.get("$schema") != "https://atlas.rsna.org/schemas/2025-11/model.json":
        err("model: wrong $schema")
    m = doc["Model"]
    check_keys(m, MODEL_TOP, "Model")
    check_common(m, "Model")
    p = m.get("Model properties", {})
    check_keys(p, MODEL_PROPS, "Model properties")
    check_keys(p.get("Output", {}), {"Description", "CDEs"}, "Output")
    for c in p.get("Output", {}).get("CDEs", []):
        if not re.fullmatch(r"RDE\d+", c):
            err(f"CDE '{c}' is not RDE...")
    reg = p.get("Regulatory information", {})
    check_keys(reg, REG_KEYS, "Regulatory information")
    for k in ("FDA cleared", "CE marked"):
        if k in reg and not isinstance(reg[k], bool):
            err(f"Regulatory information.{k} is not a bool")
    for field, enum in (("Use", USE_ENUM), ("User", USER_ENUM)):
        u = p.get(field, {})
        check_keys(u, USE_KEYS, field)
        for k, vals in u.items():
            for v in vals:
                if v not in enum:
                    err(f"{field}.{k}: '{v}' not in enum {sorted(enum)}")
    ehr = p.get("EHR compatibility", {})
    check_keys(ehr, {"List", "Other"}, "EHR compatibility")
    if "List" in ehr:
        warnings.append("EHR compatibility.List used; its enum is not in the schema summary")
    im = m.get("Imaging", {})
    check_keys(im, MODEL_IMAGING, "Model.Imaging")
    for pr in im.get("Procedures", []):
        check_keys(pr, PROC_KEYS, "Procedures")
    for f in im.get("File format", []):
        if f not in FILE_FORMAT_ENUM:
            err(f"File format '{f}' not in enum")
    for mod in im.get("Modalities", []):
        if "(RID" not in mod:
            warnings.append(f"model modality '{mod}' carries no RID")
        else:
            warnings.append(f"model modality '{mod}': RID recalled from memory, not verified")
    perf = m.get("Model performance", {})
    check_keys(perf, PERF_KEYS, "Model performance")
    for met in perf.get("Metrics", []):
        if met not in METRIC_ENUM:
            err(f"Metric '{met}' not in enum")
    return m


def check_total(t, where):
    check_keys(t, TOTAL_KEYS, where)
    for k in ("Site count", "Patient count", "Exam count", "Series count", "Image count"):
        if k in t and (not isinstance(t[k], int) or t[k] < 0):
            err(f"{where}.{k} is not a non-negative int")
    if "Age range" in t:
        ar = t["Age range"]
        ok = (isinstance(ar, list) and len(ar) == 2 and all(
            isinstance(x, list) and len(x) == 2 and isinstance(x[0], (int, float))
            and isinstance(x[1], str) for x in ar))
        if not ok:
            err(f"{where}.Age range is not [[v,unit],[v,unit]]")


def validate_dataset(path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    check_keys(doc, {"$schema", "Dataset"}, "dataset root")
    if doc.get("$schema") != "https://atlas.rsna.org/schemas/2025-11/dataset.json":
        err("dataset: wrong $schema")
    d = doc["Dataset"]
    check_keys(d, DATASET_TOP, "Dataset")
    check_common(d, "Dataset")
    check_keys(d.get("Dataset properties", {}), DATASET_PROPS, "Dataset properties")
    im = d.get("Imaging", {})
    check_keys(im, DATASET_IMAGING, "Dataset.Imaging")
    for pr in im.get("Procedures", []):
        check_keys(pr, PROC_KEYS, "Procedures")
    for f in im.get("File format", []):
        if f not in FILE_FORMAT_ENUM:
            err(f"File format '{f}' not in enum")
    if im.get("Burned-in PHI") not in PHI_ENUM:
        err("Burned-in PHI not in enum")
    for mod in im.get("Modalities", []):
        if "(RID" not in mod:
            warnings.append(f"dataset modality '{mod}' carries no RID")
        else:
            warnings.append(f"dataset modality '{mod}': RID recalled from memory, not verified")
    for i, part in enumerate(d.get("Partitions", [])):
        where = f"Partitions[{i}]"
        check_keys(part, PARTITION_KEYS, where)
        if part.get("Partition") not in PARTITION_ENUM:
            err(f"{where}.Partition '{part.get('Partition')}' not in enum")
        check_total(part.get("Total", {}), where + ".Total")
        for j, sub in enumerate(part.get("Subsets", [])):
            sw = f"{where}.Subsets[{j}]"
            check_keys(sub, PARTITION_KEYS, sw)
            if sub.get("Partition") not in PARTITION_ENUM:
                err(f"{sw}.Partition not in enum")
            check_total(sub.get("Total", {}), sw + ".Total")
    return d


def main():
    validate_model(HERE / "model.json")
    validate_dataset(HERE / "dataset.json")
    for w in warnings:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
