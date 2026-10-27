"""One row per paper: what it supplies, who wrote it, where it is, how it was found, and what the check found.

    python3 code/render_sources.py            # from synthetic_spine/; standard library only, no network
    python3 code/render_sources.py --check    # exit 1 when sources.csv or SOURCES.md is not what the inputs give

Joins sources.json (code/resolve_sources.py), data/series_papers.csv, the two reference tables, 06's whole-spine
Panjabi table (data/panjabi_full_spine.csv) and verification/series.csv (code/verify_tables.py) into sources.csv and
SOURCES.md. Nothing here is typed by hand except the column names and the sentences that carry the resolver's
findings, so the list of papers cannot fall out of step with the evidence behind it.
"""
import csv
import io
import json
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
SPELT = {"\u2013": "-", "\u2014": "--", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00b1": "+/-"}
# the whole-spine Panjabi table cites each row by its paper's pages
PANJABI_PAGES = {"861-869": "panjabi1991c", "888-901": "panjabi1991t", "299-306": "panjabi1992"}


def ascii_text(text):
    text = str(text or "")
    for char, spelling in SPELT.items():
        text = text.replace(char, spelling)
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def rows_of(name):
    lines = [l for l in (DATA / name).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def level_key(level):
    # the full name breaks ties ("T12" before "T12L1"); without it the order follows set iteration, which changes
    # from one Python process to the next
    return ("CTLS".find(level[0]), int("".join(ch for ch in level[1:3] if ch.isdigit()) or 0), level)


def disagreements(p):
    """Sentences for every way the tables' citation disagrees with the paper the identifiers lead to."""
    out, a = [], p.get("agreement") or {}
    differs = p.get("first_author_differs")
    if differs:
        out.append(f"the paper's first author is {differs['paper']}, not {differs['cited']}"
                   + ("" if differs.get("cited_author_among_authors") else f"; {differs['cited']} is not among its authors"))
    if a.get("page_agrees") is False:
        out.append(f"the tables cite first page {a['cited_first_page']}; the paper's is {a['resolved_first_page']}")
    if a.get("issue_agrees") is False:
        out.append(f"the tables cite issue {a['cited_issue']}; the paper's is {a['resolved_issue']}")
    if a.get("year_agrees") is False:
        out.append("the year cited differs from the paper's by more than one")
    return out


def check_text(v):
    text = (f"{v['series']}: {v['confirmed']} of {v['values']} values confirmed in context"
            + (f" ({v['where']})" if v["where"] else ""))
    if int(v["checkable"]) < int(v["values"]):
        text += f"; {int(v['values']) - int(v['checkable'])} not checkable"
    if int(v["not_found_in_full_text"]):
        text += f"; {v['not_found_in_full_text']} not printed in the full text"
    if int(v["out_of_context"]):
        text += f"; {v['out_of_context']} found only out of context"
    if v["agrees_with_row"]:
        text += f"; means agree with {v['agrees_with_row']} ({v['row_means']} means, {v['row_sds']} SDs)"
    return text


def build():
    papers = json.loads((HERE / "sources.json").read_text(encoding="ascii"))
    mapping = list(csv.DictReader((DATA / "series_papers.csv").read_text(encoding="ascii").splitlines()))
    checks = list(csv.DictReader((HERE / "verification" / "series.csv").read_text(encoding="ascii").splitlines()))

    supply = defaultdict(lambda: defaultdict(set))
    for name in ("level_references.csv", "pedicle_width_references.csv"):
        for r in rows_of(name):
            m = next(m for m in mapping if m["file"] == name and m["series"] == r["series"]
                     and (not m["citation_contains"] or m["citation_contains"] in r["citation"]))
            s = supply[m["paper"]]
            s["series"].add(r["series"])
            s["measures"].add("pedicle" if r["measure"] == "PDW" else r["measure"])
            s["levels"].add(r["level"])
            s["sex"].add(r.get("sex") or "all")
            for col, key in (("cohort", "cohort"), ("n", "n"), ("modality", "modality"), ("dispersion", "dispersion"),
                             ("source_kind", "kind")):
                if r.get(col):
                    s[key].add(r[col])
            s["cited_as"].add(r["citation"])
            s["rows"].add((name, r["measure"], r["level"], r["series"], r.get("sex", "")))
            if m["read_from"] != m["paper"]:
                s["read_from"].add(m["read_from"])
            if m["note"]:
                s["note"].add(m["note"])
    for r in rows_of("panjabi_full_spine.csv"):
        key = next(k for pages, k in PANJABI_PAGES.items() if pages in r["citation"])
        s = supply[key]
        s["whole_spine_rows"].add((r["measure"], r["level"]))
        s["whole_spine_levels"].add(r["level"])
        s["cited_as"].add(r["citation"])
    for m in mapping:  # a paper that only lends its table to another's series
        if m["read_from"] not in ("not recorded", m["paper"]):
            supply[m["read_from"]]["lends_to"].add(m["series"])

    out = []
    for key, p in papers["papers"].items():
        c, pm, s = p.get("crossref") or {}, p.get("pubmed") or {}, supply.get(key, {})
        ft = p.get("full_text") or {}
        verdicts = [v for v in checks if v["paper"] == key]
        first = pm.get("first_author") or c.get("first_author") or ""
        year = c.get("year") or str(pm.get("pubdate", ""))[:4]
        title = c.get("title") or pm.get("title") or ""
        journal = pm.get("journal") or c.get("journal") or ""
        vol = c.get("volume") or pm.get("volume") or ""
        issue = c.get("issue") or pm.get("issue") or ""
        pages = c.get("page") or pm.get("pages") or ""
        resolved_citation = (f"{first} et al. {title}. {journal} {year};{vol}" + (f"({issue})" if issue else "")
                             + (f":{pages}" if pages else "")) if (first or title) else ""
        if ft.get("pmc_full_text_xml"):
            as_text, as_images = ft.get("pmc_tables_as_text", 0), ft.get("pmc_tables_as_images", 0)
            full_text = f"yes; {as_text} tables as text" + (f", {as_images} only as images" if as_images else "")
        else:
            full_text = "no (PMC holds it, not in the open-access text subset)" if p.get("pmcid") else "no PMC copy"
        whole = s.get("whole_spine_levels", set())
        out.append({
            "paper": key,
            "resolved_citation": ascii_text(resolved_citation) or "not found in Crossref or PubMed",
            "cited_in_tables_as": ascii_text(" | ".join(sorted(s.get("cited_as", [])))),
            "series_in_tables": "; ".join(sorted(s.get("series", []))),
            "measures": ", ".join(sorted(s.get("measures", []))),
            "levels": ", ".join(sorted(s.get("levels", []), key=level_key)),
            "sex": ", ".join(sorted(s.get("sex", []))),
            "cohort": "; ".join(sorted(s.get("cohort", []))),
            "n": "; ".join(sorted(s.get("n", []))),
            "modality": "; ".join(sorted(s.get("modality", []))),
            "dispersion": "; ".join(sorted(s.get("dispersion", []))),
            "primary_or_secondary": "; ".join(sorted(s.get("kind", []))),
            "values_read_from": "; ".join(sorted(s.get("read_from", []))) or ("this paper" if s.get("series") else ""),
            "lends_its_table_to": "; ".join(sorted(s.get("lends_to", []))),
            "rows_in_tables": len(s.get("rows", [])),
            "rows_in_whole_spine_table": len(s.get("whole_spine_rows", [])),
            "whole_spine_levels": (f"{min(whole, key=level_key)}-{max(whole, key=level_key)}" if whole else ""),
            "doi": c.get("doi") or pm.get("doi") or "",
            "doi_link": (p.get("links") or {}).get("doi") or "",
            "pubmed_link": (p.get("links") or {}).get("pubmed") or "",
            "pmc_link": (p.get("links") or {}).get("pmc") or "",
            "full_text_as_text_in_pmc": full_text,
            "licence": ascii_text(ft.get("license_url") or ft.get("license_text") or ""),
            "how_found": ascii_text("; ".join(p.get("how", []))),
            "check": " | ".join(check_text(v) for v in verdicts),
            "notes": ascii_text("; ".join(sorted(s.get("note", [])) + disagreements(p))),
        })

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(out[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(out)

    md = ["# The papers behind the reference series",
          "",
          "Generated by code/render_sources.py from sources.json, data/series_papers.csv, the reference tables and",
          f"verification/series.csv; do not edit by hand. Identifiers resolved {papers['resolved_at']} through Crossref and",
          "NCBI (PubMed, the PMC id converter, PMC full text); every raw answer is in sources_raw/<paper>.json.",
          "sources.csv carries the same rows with every column. \"Confirmed in context\" means printed at the value's",
          "level, sex, measure and role, in a table cell or a sentence that is quoted in verification/values.csv.",
          "",
          "| Paper | Supplies | Links | Full text in PMC | Check against the paper |",
          "| --- | --- | --- | --- | --- |"]
    for r in out:
        links = " ".join(f"[{name}]({r[col]})" for name, col in (("DOI", "doi_link"), ("PubMed", "pubmed_link"), ("PMC", "pmc_link")) if r[col]) or "none found"
        parts = []
        if r["series_in_tables"]:
            parts.append(f"{r['series_in_tables']}: {r['measures']} ({r['rows_in_tables']} rows)")
        if r["rows_in_whole_spine_table"]:
            parts.append(f"whole-spine Panjabi table: {r['whole_spine_levels']} ({r['rows_in_whole_spine_table']} rows)")
        if r["lends_its_table_to"]:
            parts.append(f"its table is read for {r['lends_its_table_to']}")
        md.append("| " + " | ".join(x.replace("|", "/") for x in (
            f"**{r['paper']}**: {r['resolved_citation']}" + (f" *Note: {r['notes']}.*" if r["notes"] else ""),
            "; ".join(parts) or "-", links, r["full_text_as_text_in_pmc"], r["check"] or "-")) + " |")
    return buf.getvalue(), "\n".join(md) + "\n", len(out)


def main(argv):
    table, page, n = build()
    targets = ((HERE / "sources.csv", table), (HERE / "SOURCES.md", page))
    if "--check" in argv:
        stale = [p.name for p, text in targets if not p.exists() or p.read_bytes() != text.encode("ascii")]
        print("sources.csv and SOURCES.md are what the inputs give" if not stale else f"stale: {', '.join(stale)}; rerun code/render_sources.py")
        return 1 if stale else 0
    for path, text in targets:
        path.write_bytes(text.encode("ascii"))
    print(f"sources.csv and SOURCES.md: {n} papers")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
