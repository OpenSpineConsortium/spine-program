"""Adversarial checks on queries/literature.yaml and queries/repositories.yaml (the 'queries' module).

WHY. The adapters read their strings from information_sources.md (sdr.common.load_queries with no
path) or from the two YAML files; sdr.manuscript prints Appendix A and Table 2 from the YAML with the
run's queries.json overlaid. So the YAML is evidence only if (1) every string marked
verbatim_in_markdown is byte-identical to the markdown, (2) grid/term entries are the markdown
primitive plus the documented suffix, (3) no credential value can sit in them, and (4) what a run
records in queries.json is what the YAML says was planned: the string and endpoint for every real
search string, and the date-filter mode and raw-cache flag for every id, because Appendix A and
Table 2 print the run's values as statements about the protocol. There is no generator for the YAML
(the headers say so); this test is the gate, run by Makefile protocol-check and manuscript/build.sh.

Run:  ~/sdr_venv/bin/python tests/test_queries_yaml.py [--run-dir runs/<date>] [--run-dir runs/<other>]
Each check prints PASS/FAIL with the offending ids; exit 1 if any check fails. Also importable by pytest.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sdr.common import _RATES, load_queries  # noqa: E402

YAMLS = (ROOT / "queries" / "literature.yaml", ROOT / "queries" / "repositories.yaml")
REQUIRED = ("query_id source_code source_name source section role form grammar string verbatim_in_markdown method "
            "endpoint params paging cap rate_limit date_filter coverage credential credential_free_behaviour "
            "credential_mode_expected raw_cache_published raw_cache_reason syntax_notes").split()
VOCAB = {
    "role": {"search", "chase", "enrich", "probe", "supplement", "supplementary", "fallback", "conditional-split"},
    "form": {"fenced", "grid", "term", "template", "derived", "regex", "list-in-prose"},
    "grammar": {"boolean", "grid", "list", "dump-filter", "chase", "enrich", "probe", "regex"},
    "date_filter": {"api", "local", "none"},
    "method": {"GET", "POST", "local"},
    "credential_mode_expected": {"keyed", "credential-free", "needs-credentials", "html-fallback", "no-public-api", "retired",
                                 "not-run", "mendeley-via-datacite"},
}
PLACEHOLDERS = {"<string>", "<NCBI_API_KEY>", "<S2_API_KEY>", "<CONTACT>", "<HF_TOKEN>", "<GITHUB_TOKEN>", "<OSF_TOKEN>",
                "<SPRINGER_API_META_KEY>", "<continue.*>", "<id>", "<i>", "<w>", "<k>", "<to>", "<from>", "<cursor>",
                "<openalex_id>", "<term>", "<referenced_work_id>", "<c>", "<m>", "<slug>", "<pmcid>", "<article_id>",
                "<base64(KAGGLE_USERNAME:KAGGLE_KEY)>", "<n>"}
# `source` values an adapter records under that name (the records/<source>.jsonl stem); `springer` is sdr.search_literature's S1 runner.
ADAPTERS = {"pubmed", "epmc", "openalex", "s2", "arxiv", "biorxiv", "crossref", "zenodo", "figshare", "dryad", "osf", "mendeley",
            "datacite", "physionet", "tcia", "kaggle", "hf", "gc", "github", "pwc", "odl", "openi", "commons", "jstage", "koreamed",
            "scielo", "redalyc", "kaggle-mention", "hf-mention", "springer"}
# YAML `source` values with no adapter: charting-time routes, written to queries.json as not-run with a not_run_reason.
NO_ADAPTER_EXPECTED = {"multicare", "openpmc"}
BLOCK_S_CORE = ("spine", "spinal", "vertebra", "lumbar", "thoracolumbar", "lumbosacral", "sacrum", "scoliosis", "spondylolisthesis")
# date_filter=api entries allowed to start after 2000: the venue's first year is the lower bound.
DATE_START_EXEMPT = {"springer_01": "2014"}

FAILS: list[str] = []


def check(name: str, bad: list, note: str = "") -> None:
    if bad:
        FAILS.append(name)
        print(f"FAIL {name}: {len(bad)} -> {bad[:12]}{' ...' if len(bad) > 12 else ''} {note}")
    else:
        print(f"PASS {name} {note}")


def load() -> tuple[dict, dict, dict]:
    lit, rep = (load_queries(p) for p in YAMLS)
    return lit, rep, load_queries()


def raw_top_keys(path: Path) -> list[str]:
    return [m.group(1) for m in re.finditer(r"^([A-Za-z0-9_<>]+):", path.read_text(encoding="utf-8"), re.M)]


def test_keys_and_structure() -> None:
    lit, rep, _ = load()
    check("top-level key == query_id", [k for d in (lit, rep) for k, v in d.items() if v.get("query_id") != k])
    check("no id in both files", sorted(set(lit) & set(rep)))
    check("no duplicate top-level key in text (yaml.safe_load keeps the last silently)",
          [k for p in YAMLS for k, n in Counter(raw_top_keys(p)).items() if n > 1])
    check("no CRLF / BOM", [p.name for p in YAMLS if b"\r" in p.read_bytes() or p.read_bytes()[:3] == b"\xef\xbb\xbf"])
    allq = {**lit, **rep}
    check("required contract keys present", [(k, m) for k, v in allq.items() for m in REQUIRED if m not in v])
    check("enumerated vocabularies", [(k, f, v.get(f)) for k, v in allq.items() for f, ok in VOCAB.items() if str(v.get(f)) not in ok])
    check("string_param names a key of params", [k for k, v in allq.items() if v.get("string_param") and v["string_param"] not in (v.get("params") or {})])
    check("<string> in params implies string_param", [k for k, v in allq.items() if "<string>" in json.dumps(v.get("params") or {}) and not v.get("string_param")])
    check("endpoint is a URL or 'local' (no placeholder endpoint)", [k for k, v in allq.items() if not (str(v.get("endpoint")).startswith("http") or v.get("endpoint") == "local")])
    check("credential is a NAME or none", [k for k, v in allq.items() if not re.match(r"^(none|[A-Z][A-Z0-9_]+)", str(v.get("credential")))])
    check("source in rate table or documented default", [k for k, v in allq.items() if v["source"] not in _RATES and v["source"] not in ADAPTERS | NO_ADAPTER_EXPECTED])
    check("sources without an adapter are exactly the known set", sorted({v["source"] for v in allq.values()} - ADAPTERS ^ NO_ADAPTER_EXPECTED))
    check("every source without an adapter carries not_run_reason and expects not-run",
          [k for k, v in allq.items() if v["source"] in NO_ADAPTER_EXPECTED and not (v.get("not_run_reason") and v.get("credential_mode_expected") == "not-run")])
    check("not-run is expected only where there is no adapter", [k for k, v in allq.items() if v.get("credential_mode_expected") == "not-run" and v["source"] in ADAPTERS])
    check("the summary table's R14 row and the odl candidates agree (odl_01..03 present)", [k for k in ("odl_01", "odl_02", "odl_03") if k not in rep])


def test_byte_identity() -> None:
    lit, rep, md = load()
    allq = {**lit, **rep}
    bad, n = [], 0
    for k, v in sorted(allq.items()):
        if not v.get("verbatim_in_markdown"):
            continue
        ref = v.get("markdown_id") or v.get("grid_id") or k
        n += 1
        if ref not in md:
            bad.append((k, "no markdown block", ref))
        elif md[ref]["string"] != v["string"]:
            bad.append((k, "differs", v["string"][:60], md[ref]["string"][:60]))
    check(f"verbatim_in_markdown entries byte-identical to information_sources.md (n={n})", bad)
    check("verbatim_in_markdown=false entries carry markdown_string, markdown_prose or a markdown/grid id",
          [k for k, v in allq.items() if not v.get("verbatim_in_markdown") and not any(x in v for x in ("markdown_string", "markdown_prose", "markdown_id", "grid_id"))])
    check("markdown_string (where given for a fenced markdown id) is byte-identical to the markdown block",
          [k for k, v in allq.items() if v.get("markdown_string") and (v.get("markdown_id") or k) in md
           and v["markdown_string"] != md[v.get("markdown_id") or k]["string"]])
    text = (ROOT / "information_sources.md").read_text(encoding="utf-8").replace("\n", " ")
    check("markdown_prose quotes are verbatim in information_sources.md",
          [k for k, v in allq.items() if v.get("markdown_prose") and " ".join(v["markdown_prose"].split()) not in " ".join(text.split())])
    check("every fenced/grid/term markdown id is a YAML key or a grid/term primitive",
          [k for k in md if k not in allq and not re.fullmatch(r"[gt]\d{2}", k)])
    grid = [(k, v) for k, v in allq.items() if v.get("grid_id")]
    check(f"grid/term entries start with their markdown primitive (n={len(grid)})",
          [k for k, v in grid if not v["string"].startswith(md.get(v["grid_id"], {}).get("string", "\0"))])
    check("derived pubmed splits partition 2000-2026 and otherwise equal pubmed_01",
          [k for k in ("pubmed_01a", "pubmed_01b", "pubmed_01c", "pubmed_01d") if k in allq and
           re.sub(r'"\d{4}/\d\d/\d\d"\[dp\] : "\d{4}/\d\d/\d\d"\[dp\]', "X", allq[k]["string"]) !=
           re.sub(r'"\d{4}/\d\d/\d\d"\[dp\] : "\d{4}/\d\d/\d\d"\[dp\]', "X", md["pubmed_01"]["string"])])


def test_no_secret_values() -> None:
    lit, rep, _ = load()
    allq = {**lit, **rep}
    text = "\n".join(p.read_text(encoding="utf-8") for p in YAMLS)
    check("only known <placeholders>", sorted(set(re.findall(r"<[A-Za-z_.*]+(?:\([A-Z_:]+\))?>", text)) - PLACEHOLDERS))
    check("no e-mail address literal", sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[a-z]{2,}", text))))
    check("no bearer/key value that is not a placeholder",
          [k for k, v in allq.items() for hk, hv in {**(v.get("headers") or {}), **(v.get("params") or {})}.items()
           if hk.lower() in ("authorization", "x-api-key", "api_key", "apikey", "key", "token", "mailto", "email")
           and not re.search(r"<[A-Z_]+>|<continue|<base64\(", str(hv)) and not str(hv).startswith("<")])
    check("no 32+ char hex / 40+ char token literal", sorted(set(re.findall(r"\b(?:[0-9a-f]{32,}|[A-Za-z0-9_\-]{40,})\b", text)) - {
        s for s in re.findall(r"\b[A-Za-z0-9_\-]{40,}\b", text) if "-" in s or "_" in s}))  # ids like vector-institute/open-pmc-18m are fine


def test_block_coverage() -> None:
    """A surrogate for the never-written tests/test_terms.py: every boolean concept-block string names every
    BLOCK_S term, and every date_filter=api entry carries the 2000 and 2026 limits in string or params."""
    lit, rep, _ = load()
    allq = {**lit, **rep}
    bad = []
    for k, v in allq.items():
        if v.get("grammar") != "boolean" or v.get("form") not in ("fenced", "derived"):
            continue
        s = v["string"].lower()
        missing = [t for t in BLOCK_S_CORE if t not in s]
        if missing and k not in ("springer_01",):  # the venue sweep omits the two-word phrases by design
            bad.append((k, missing))
    check("boolean strings carry every BLOCK_S term", bad)
    bad = []
    for k, v in allq.items():
        if v.get("date_filter") != "api" or v.get("form") == "derived":  # the pubmed_01a-d splits partition the range
            continue
        blob = v["string"] + json.dumps(v.get("params") or {}) + str(v.get("intervals") or "") + str(v.get("paging") or "")
        if not (DATE_START_EXEMPT.get(k, "2000") in blob and "2026" in blob):
            bad.append(k)
    check("date_filter=api entries carry the lower bound (2000, or the venue's first year) and 2026", bad,
          f"(exempt lower bounds: {DATE_START_EXEMPT})")


def sub_id_base(qid: str, allq: dict) -> str:
    """pubmed_01a -> pubmed_01; openalex_01_g01 -> openalex_01; crossref_12a -> crossref_12; openi_03_xg -> openi_03 (old runs)."""
    if qid in allq:
        return qid
    for pat in (r"^(.*_\d+)[a-d]$", r"^(.*_\d+)_g\d+$", r"^(.*_\d+)_(c|xg)$"):
        m = re.match(pat, qid)
        if m and m.group(1) in allq:
            return m.group(1)
    return qid


def endpoint_ok(run_ep: str | None, y: dict) -> bool:
    """The recorded endpoint is the planned one, or the planned fallback (prefix up to its first placeholder)."""
    if run_ep == y.get("endpoint"):
        return True
    fb = (y.get("fallback") or {}).get("endpoint") if isinstance(y.get("fallback"), dict) else None
    return bool(fb and run_ep and run_ep.startswith(fb.split("<")[0]))


def test_run_consistency(run_dir: Path) -> None:
    """What queries.json recorded against what the YAML planned. Strings and endpoints must agree for
    every real search string (form fenced/grid/term with grammar boolean/grid); date_filter and
    raw_cache_published must agree for every id: the run records the mode the adapter states it used and the
    raw-cache cell of information_sources.md's summary table, neither copied from the YAML, so this compares
    two independently produced values and can fail. Role and grammar must agree too, now that the adapters
    state the protocol's words (S1 is the supplementary sweep, not a search; GitHub's grammar is boolean and
    the grid is its form; Figshare's split into sub-queries is a form and travels in notes.executed_as).
    credential_mode and source stay a NOTE: the first depends on which credentials the host holds and on what
    the endpoint did that day."""
    lit, rep, _ = load()
    allq = {**lit, **rep}
    qj = run_dir / "queries.json"
    if not qj.exists():
        print(f"SKIP run consistency: {qj} absent")
        return
    run = json.loads(qj.read_text(encoding="utf-8"))
    unknown = [q for q in run if sub_id_base(q, allq) not in allq and not q.startswith("pilot_")]
    check(f"[{run_dir.name}] every recorded query_id has a YAML entry", unknown)
    s_bad, e_bad, d_bad, r_bad, other = [], [], [], [], Counter()
    role_bad, gram_bad = [], []
    for q, r in sorted(run.items()):
        y = allq.get(sub_id_base(q, allq))
        if y is None:
            continue
        real = y["form"] in ("fenced", "grid", "term", "derived") and y["grammar"] in ("boolean", "grid")
        if real and r.get("query_string") != y["string"]:
            s_bad.append(q)
        if real and not endpoint_ok(r.get("endpoint"), y):
            e_bad.append((q, r.get("endpoint"), y["endpoint"]))
        if r.get("date_filter") != y.get("date_filter"):
            d_bad.append((q, r.get("date_filter"), y.get("date_filter")))
        if r.get("raw_cache_published") != y.get("raw_cache_published"):
            r_bad.append((q, r.get("raw_cache_published"), y.get("raw_cache_published")))
        if r.get("role") != y.get("role"):
            role_bad.append((q, r.get("role"), y.get("role")))
        # A sub-id may legitimately carry another grammar than its family head: that is the documented fallback
        # (an OpenAlex boolean rejected with 400 is re-sent as the 35-string grid under openalex_NN_gMM). For an
        # id the YAML defines directly there is no such licence.
        if q in allq and r.get("grammar") != y.get("grammar"):
            gram_bad.append((q, r.get("grammar"), y.get("grammar")))
        for f, g in (("credential_mode", "credential_mode_expected"), ("source", "source")):
            if r.get(f) != y.get(g):
                other[(sub_id_base(q, allq).split("_")[0], f, str(y.get(g)), str(r.get(f)))] += 1
    check(f"[{run_dir.name}] recorded query_string == YAML string for real search strings", s_bad)
    check(f"[{run_dir.name}] recorded endpoint == YAML endpoint (or its fallback) for real search strings", e_bad)
    check(f"[{run_dir.name}] recorded date_filter == YAML date_filter for every id", d_bad)
    check(f"[{run_dir.name}] recorded raw_cache_published == YAML raw_cache_published for every id", r_bad)
    check(f"[{run_dir.name}] recorded role == YAML role for every id", role_bad)
    check(f"[{run_dir.name}] recorded grammar == YAML grammar for every id the YAML defines", gram_bad)
    if other:
        print(f"NOTE [{run_dir.name}] metadata disagreements (source, field, yaml -> run: n):")
        for k, n in sorted(other.items()):
            print(f"      {k[0]:10s} {k[1]:16s} {k[2]!r:24s} -> {k[3]!r:20s} {n}")
    not_run = [k for k, v in allq.items() if k not in run and "<" not in k and not any(sub_id_base(q, allq) == k for q in run)]
    unexplained = [k for k in not_run if not (allq[k].get("not_run_reason") or allq[k].get("condition"))]
    print(f"NOTE [{run_dir.name}] YAML ids never recorded by the run: {len(not_run)} -> {not_run}")
    check(f"[{run_dir.name}] every YAML id absent from the run carries not_run_reason or condition, or is a sub-id family head", unexplained)
    lim = [(q, r.get("n_fetched", r.get("n_retrieved")), r.get("hit_count_api")) for q, r in run.items()
           if r.get("limit") and r.get("hit_count_api") and r.get("n_retrieved") is not None
           and (r["n_fetched"] if r.get("n_fetched") is not None else r["n_retrieved"]) < min(r["limit"], r["hit_count_api"])]
    check(f"[{run_dir.name}] n_fetched (or n_retrieved) reaches min(limit, hits) where a limit was recorded", lim)


def test_appendix_hand_calc() -> None:
    """Table 2 (t_sources) and Appendix A (t_search_strings) on tests/fixtures/queries_tiny.json,
    against sums done by hand in the fixture's _hand block."""
    from sdr import manuscript as M
    fx = json.loads((ROOT / "tests" / "fixtures" / "queries_tiny.json").read_text(encoding="utf-8"))
    hand, qs = fx.pop("_hand"), fx
    try:
        tex = M.t_sources(qs, "2026-09-19")
    except TypeError:  # the split-out table module takes the flow, not the run date
        tex = M.t_sources(qs)
    rows = {}
    for line in tex.splitlines():
        cells = [c.strip() for c in line.rstrip("\\").split("&")]
        if len(cells) >= 8 and not cells[0].startswith("\\textbf"):  # the column count varies; the row is keyed by its code
            rows[cells[0]] = cells
    bad = []
    for code, exp in hand["table2"].items():
        got = rows.get(code)
        if got is None:
            bad.append((code, "row missing"))
            continue
        # Queries is column 5; Hits and Retrieved are read from the end (Hits, Fetched, Retrieved, Identified),
        # so a column inserted in the middle of Table 2 does not silently compare the wrong cells.
        for i, name in ((5, "queries"), (-4, "hits"), (-2, "retrieved")):
            if got[i] != exp[name]:
                bad.append((code, name, got[i], exp[name]))
    check("Table 2 per-source sums equal the hand calculation", bad)
    check("Table 2 excludes non-search roles (pilot, enrich)", [c for c in hand["absent_codes"] if c in rows])
    # Table 2's rows and \numSourcesPlanned are one set: a planned source keeps its row whether or not a
    # query went out, and a row with no executed query says "not run" rather than reading as zero hits.
    planned, _ = M.planned_sources()
    check("Table 2 has a row for every planned source", [p["code"] for p in planned if p["code"] not in rows])
    check("a planned source with no executed query prints as 'not run', not as zero hits",
          [c for c, r in rows.items() if r[-5:] == ["--"] * 5 and r[3] != "not run"])
    # multicare_01 in the fixture is the shape sdr.repo_run.write_not_run writes for a planned id its version
    # has no adapter for: a run date, credential_mode not-run, no request timestamp, a null total. Table 2 must
    # not read that run date as a query date. Cells: code, name, coverage, mode, Date, Q., Not sent, ...
    f2 = rows.get("F2", [])
    check("a not-run record is counted under Not sent, not as a query with a date",
          [x for x in [("no F2 row", "") if not f2 else None,
                       ("Date", f2[4]) if f2 and f2[4] else None,
                       ("Q.", f2[5]) if f2 and f2[5] != "--" else None,
                       ("Not sent", f2[6]) if f2 and f2[6] != "1" else None] if x])
    app = M.t_search_strings(qs)
    n_blocks = sum(1 for l in app.splitlines() if "\\textbf{\\texttt{" in l and "ids chased" not in l and "citation chasing" not in l)
    chase = re.search(r"(\d+) ids chased, ([\d,]+) hits in total", app)
    check("Appendix A block count and chase summary equal the hand calculation",
          [x for x in [("blocks", n_blocks, hand["appendix_blocks"]) if n_blocks != hand["appendix_blocks"] else None,
                       ("chase", chase and chase.groups(), hand["chase"]) if not chase or list(chase.groups()) != hand["chase"] else None] if x])


def test_load_query_records_fixture() -> None:
    """load_query_records on a tiny run dir must not invent query ids from counts.json's per-source keys."""
    from sdr import manuscript as M
    recs = M.load_query_records(ROOT / "tests" / "fixtures" / "run_tiny")
    lit, rep, _ = load()
    known = set(lit) | set(rep)
    invented = [k for k in recs if k not in known and not k.startswith("pilot_") and not re.fullmatch(r"openi_\d\d_(xg|c)|pubmed_01[a-d]|crossref_\d\d[abc]|openalex_\d\d_g\d\d", k)]
    check("load_query_records invents no query ids from counts.json source keys", invented)
    check("load_query_records does not substitute credential_mode_expected for an unrun id",
          [(k, r.get("credential_mode")) for k, r in recs.items()
           if not (r.get("first_request_ts") or r.get("hit_count_api") is not None)
           and r.get("credential_mode") not in (None, "not-run")])  # "not-run" is written by the run, never copied from the plan


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run-dir", action="append", default=[], help="a run directory whose queries.json is checked against the YAML")
    a = ap.parse_args(argv)
    test_keys_and_structure()
    test_byte_identity()
    test_no_secret_values()
    test_block_coverage()
    test_appendix_hand_calc()
    test_load_query_records_fixture()
    for rd in a.run_dir:
        test_run_consistency(Path(rd) if Path(rd).is_absolute() else ROOT / rd)
    print(f"\n{len(FAILS)} failing check(s)" + (": " + "; ".join(FAILS) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
