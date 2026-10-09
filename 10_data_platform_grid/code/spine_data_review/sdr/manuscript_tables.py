"""The LaTeX tables sdr.manuscript inputs, and the text helpers they share; no number is typed here.

WHAT. One `t_<name>` function per generated table (`tables/<name>.tex`), each reading exactly one
of the review's outputs: the protocol files (eligibility, data items, deviations, checklist), the
run's query records (sources, search strings), the charting records (datasets_main) or one
`analysis/*.json` (quality, counts, availability, pooled_variants, agreement, grid). Every function
returns the table's LaTeX or a red `\\pendingtable` when its input is absent; the escaping helpers
(`esc`, `tt`, `md`), the column builder (`pcols`), the envelope reader (`dig`) and the number
formatter (`fmt`) live here because every table needs them and sdr.manuscript imports them back.

WHY a second file. sdr.manuscript owns the number contract, the bare-digit check and the render
loop; the table renderers are the larger, more volatile half and were split out so each module
stays within the repository's size rule. The shapes each table assumes are stated in the
sdr.manuscript docstring, which is the single place the contracts are written down.

Rules the tables enforce. Table 2 (`t_sources`) counts only queries that ran: a record with no
run date, no first request timestamp and no reported total is a protocol template (the OpenAlex
chase templates, the Open-i grid heads whose executed forms are sub-ids) and is left to Appendix A,
which prints every string. Hits are the sum of the totals each query reported, which overlap, and
the note says so; the flow's per-source identified count is a separate column. Appendix A prints
the operational YAML `string` for every id the YAML defines and, where the markdown form differs,
that form on a second line, so the appendix carries both texts the protocol promised.
"""
from __future__ import annotations

import json
import re
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path
from typing import Any

from sdr.common import review_root

ROOT = review_root()
# Counted in Table 2; other roles (pilot, enrich, probe) appear only in Appendix A. `conditional-split` is
# here because a [dp] split that fires retrieves records like any other search, and one that does not fire is
# a planned query that was not sent -- which is what the Not sent column is for.
SEARCH_ROLES = {"search", "supplement", "supplementary", "chase", "conditional-split"}
# queries.json[qid].unit (repo_run.UNITS): what the source's own total counts. Open-i reports figures, Wikimedia
# Commons files, PhysioNet/TCIA/grand-challenge the size of the listing they filter locally. Printing 43,095
# beside Zenodo's 2,598 with no unit would read as 43,095 records, which is the review's own failure mode.
UNIT_ORDER = ("records", "figures", "files", "harvest")
SOURCE_NAMES = {"pubmed": "PubMed", "europepmc": "Europe PMC", "epmc": "Europe PMC", "openalex": "OpenAlex", "s2": "Semantic Scholar",
                "arxiv": "arXiv", "biorxiv": "bioRxiv / medRxiv", "medrxiv": "bioRxiv / medRxiv", "crossref": "Crossref", "zenodo": "Zenodo",
                "figshare": "Figshare", "dryad": "Dryad", "osf": "OSF", "mendeley": "Mendeley Data", "datacite": "DataCite",
                "physionet": "PhysioNet", "tcia": "TCIA / NBIA", "kaggle": "Kaggle", "hf": "Hugging Face", "gc": "grand-challenge.org",
                "github": "GitHub", "pwc": "Papers with Code", "odl": "OpenDataLab", "openi": "NLM Open-i", "multicare": "MultiCaRe",
                "openpmc": "Open-PMC-18M", "commons": "Wikimedia Commons", "jstage": "J-STAGE", "koreamed": "KoreaMed Synapse",
                "scielo": "SciELO", "redalyc": "Redalyc", "springer": "Springer Nature Meta", "chase": "OpenAlex citation chasing",
                "hf-mention": "Hugging Face (mention harvest over the other records)", "kaggle-mention": "Kaggle (mention harvest over the other records)"}
CHASE_CODE = "O1"  # the chase is an "other methods" arm, not a numbered source of the summary table
# Arms that are not numbered sources of information_sources.md's summary table, with the code Table 2 gives each. The
# chase is an "other methods" arm; the two mention harvests belong to their parent source (R9 Kaggle, R10 Hugging Face)
# and carry its source_code in the run records, so without a code of their own they print a second row under R9 and R10
# and the reader counts two planned sources where the protocol planned one. The suffix says "this arm, under that source".
FIXED_CODES = {"chase": CHASE_CODE, "kaggle-mention": "R9a", "hf-mention": "R10a"}
# Sources whose row name is fixed here, not taken from the record: the chase and the two mention harvests share a
# source_name with the API they supplement and would otherwise print as a second row under the same name.
FIXED_NAMES = set(FIXED_CODES)
KEY_ALIASES = {"europepmc": "epmc"}  # source_key's normalisation; the planned-row seeding uses it so both agree
# A planned source's code, by shape: the literature, repository, figure and supplementary series. Matching by shape
# rather than by a hard-coded "S1" means a second supplementary source is counted instead of silently dropped.
PLANNED_CODE_RE = re.compile(r"[LRFS]\d+")
MOD = {"CT": "CT", "CBCT": "CBCT", "radiograph": "XR", "fluoroscopy": "FL", "DXA-VFA": "DXA", "EOS": "EOS", "MRI": "MRI*"}
REG = {"cervical": "C", "thoracic": "T", "lumbar": "L", "sacrum-pelvis": "S", "whole-spine": "W"}
ANN = {"per-vertebra-level-names": "lvl", "segmentation-3d": "seg3", "segmentation-2d": "seg2", "landmarks": "lmk", "bounding-boxes": "box",
       "centroids": "ctr", "pathology-labels": "path", "fracture-grade": "frac", "measurements": "meas", "radiology-reports": "rep",
       "image-level-labels": "img", "none": "none"}
ORI = {"expert-manual": "EM", "expert-corrected-model": "ECM", "model-generated": "MG", "counting-inferred": "CI", "report-derived": "RD",
       "crowd-or-trainee": "CRT", "caption-derived": "CAP", "unknown": "?", "none": "--"}
_TEX = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
_UNI = {"→": r"$\rightarrow$", "≥": r"$\geq$", "≤": r"$\leq$", "≠": r"$\neq$", "×": r"$\times$", "κ": r"$\kappa$", "τ": r"$\tau$",
        "ε": r"$\varepsilon$", "ρ": r"$\rho$", "μ": r"$\mu$", "α": r"$\alpha$", "Σ": r"$\Sigma$", "∪": r"$\cup$", "∩": r"$\cap$",
        "∅": r"$\emptyset$", "²": r"$^{2}$", "³": r"$^{3}$", "−": r"$-$", "°": r"$^{\circ}$", "′": "'", "’": "'", "‘": "`", "“": "``",
        "”": "''", "…": r"\ldots{}", "–": "--", "—": "---", "\u00a0": "~", "✓": "yes"}


# ----------------------------------------------------------------------------- LaTeX text
def esc(s: Any) -> str:
    """LaTeX-escape `s`: specials first, then the Unicode the protocol files use, then any remaining
    character outside Latin-1 as [U+XXXX] (pdflatex has no CJK font; queries.json keeps the string)."""
    out = "".join(_UNI.get(c, c) for c in "".join(_TEX.get(c, c) for c in str(s)))
    return "".join(c if ord(c) < 0x100 else f"[U+{ord(c):04X}]" for c in out)


def esc_break(s: Any) -> str:
    """esc() that also allows a line break after an underscore, a slash or a dot inside a token, so file
    names, DOIs and URLs in prose cells (schema fields, the deviations log) can wrap in a narrow column."""
    return re.sub(r"(\\_|[/.])(?=\S)", r"\1\\allowbreak{}", esc(s))


def tt(s: Any) -> str:
    """Monospace identifier or code span that may break after _ - . / : , = (they sit in narrow columns)."""
    return r"\texttt{" + re.sub(r"(\\_|[-./:,=])", r"\1\\allowbreak{}", esc(s)) + "}"


def md(s: str) -> str:
    """Escape a Markdown table cell: `code` -> \\texttt, **bold**, *emph*."""
    parts = s.split("`")
    for i, p in enumerate(parts):
        t = esc_break(p)
        t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
        parts[i] = tt(p) if i % 2 else re.sub(r"(?<![*\\])\*(?!\*)(.+?)\*", r"\\emph{\1}", t)
    return "".join(parts)


def pcols(*w: float) -> str:
    """Ragged p-columns; the weights are normalised to sum to one and each column gives up its own
    2\\tabcolsep, so the table is exactly \\linewidth wide whatever the weights were."""
    return "".join(rf">{{\raggedright\arraybackslash}}p{{\dimexpr{x / sum(w):.4f}\linewidth-2\tabcolsep\relax}}" for x in w)


def longtable(label: str, caption: str, header: list[str], rows: list[list[str]], spec: str, note: str = "", size: str = "footnotesize") -> str:
    """A booktabs longtable (continued heads, caption on the first) plus an optional note paragraph.
    Captions and notes are LaTeX (they may carry math); only underscores in file names are escaped."""
    caption, note = caption.replace("_", r"\_"), note.replace("_", r"\_")
    n, head = len(header), " & ".join(rf"\textbf{{{h}}}" for h in header) + r" \\ \midrule"
    body = "\n".join(" & ".join(r) + r" \\" for r in rows) if rows else rf"\multicolumn{{{n}}}{{l}}{{\emph{{no rows}}}} \\"
    return (f"{{\\{size}\n\\begin{{longtable}}{{{spec}}}\n"
            f"\\caption{{{caption}}}\\label{{tab:{label}}}\\\\\n\\toprule\n{head}\n\\endfirsthead\n"
            f"\\multicolumn{{{n}}}{{l}}{{\\emph{{\\tablename~\\thetable{{}} (continued)}}}}\\\\\n\\toprule\n{head}\n\\endhead\n"
            f"\\midrule\\multicolumn{{{n}}}{{r}}{{\\emph{{continued}}}}\\\\\n\\endfoot\n\\bottomrule\n\\endlastfoot\n{body}\n\\end{{longtable}}}}\n"
            + (f"\\noindent{{\\footnotesize {note}\\par}}\n" if note else ""))


def pending_table(name: str, reason: str) -> str:
    """The template's \\pendingtable detokenizes both arguments, so nothing is escaped here. The
    placeholder carries the table's label so every \\tabref resolves; build.sh --strict still fails
    on a pending table."""
    return f"\\pendingtable{{{name}}}{{{reason}}}\\label{{tab:{name}}}\n"


# ----------------------------------------------------------------------------- inputs and numbers
def val(x: Any) -> Any:
    """Unwrap the SAP's {value, derived_from, rule} envelope; a bare value passes through."""
    return x.get("value") if isinstance(x, dict) and "value" in x else x


def dig(obj: Any, path: str) -> Any:
    """Value at a dotted path, unwrapping envelopes at every step; None when any step is absent. A key
    that is present is taken before any unwrapping, so a block that carries a literal `value` beside
    its interval ({value, ci}, as the reliability statistics are written) is read as that block."""
    cur = obj
    for k in path.split("."):
        if not (isinstance(cur, dict) and k in cur):
            cur = val(cur)
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        else:
            return None
    return val(cur)


def md_tables(path: Path, heading_re: str) -> list[list[list[str]]]:
    """Every Markdown table under headings matching `heading_re` (until the next heading), as rows of cells."""
    tables: list[list[list[str]]] = [[]]
    active = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            active = re.search(heading_re, line) is not None
        if active and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                tables[-1].append(cells)
        elif tables[-1]:
            tables.append([])
    return [t for t in tables if t]


def fmt(v: Any, kind: str) -> str | None:
    """Plain-text rendering (callers escape): int with thousands separators; pct from a proportion in
    [0,1] or a percentage, one decimal half-to-even (SAP general rules); p; dec (two decimals);
    text (the string itself)."""
    if kind == "text":
        return None if v is None else str(v)
    try:
        x = float(v) if v is not None and not isinstance(v, bool) else None
    except (TypeError, ValueError):
        x = None
    if x is None:
        return None
    if kind == "int":
        return f"{int(round(x)):,}"
    if kind == "pct":
        return f"{Decimal(str(x * (100 if x <= 1 else 1))).quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)}%"
    return ("<0.001" if x < 0.001 else f"{x:.3f}") if kind == "p" else f"{x:.2f}"


def ci(d: Any, lo: str, hi: str, kind: str) -> str:
    return f"({fmt(dig(d, lo), kind)} to {fmt(dig(d, hi), kind)})"


def source_key(qid: str, rec: dict) -> str:
    if re.match(r"^openalex_03r?_", qid) or rec.get("role") == "chase":
        return "chase"
    k = str(rec.get("source") or qid.split("_")[0]).lower()
    return KEY_ALIASES.get(k, k)


def planned_sources() -> tuple[list[dict], dict[str, str]]:
    """The planned search sources as ([{code, name, coverage}], {summary name: code}), from
    information_sources.md's summary table: every row whose code has the shape of a search series, minus a
    row the table itself marks as not a search source (S2, Unpaywall, a charting-time API with no
    query_id). One list feeds \\numSourcesPlanned and Table 2's rows, so the count and the rows cannot be
    two different sets of thirty."""
    rows = [r for t in md_tables(ROOT / "information_sources.md", r"^## Summary table") for r in t[1:]]
    # Coverage is read as the second-to-last cell, not as a fixed index: a Grammar cell carrying an escaped
    # pipe (L4's "`\|` OR") splits into two and shifts every index after it, which silently printed L4's
    # paging rule in the Coverage column.
    out = [{"code": r[0], "name": re.sub(r"\s*\([^()]*\)\s*$", "", r[1]).strip(), "coverage": r[-2] if len(r) >= 9 else ""}
           for r in rows if PLANNED_CODE_RE.fullmatch(r[0]) and "not a search source" not in " ".join(r[:2]).lower()]
    return out, {r[1]: r[0] for r in rows}


def code_of(k: str, by_name: dict[str, str]) -> str:
    """The summary table's code for a source key: the fixed code for an arm that is not a numbered source,
    else the code of the row whose Source cell contains the key's display name."""
    nm = SOURCE_NAMES.get(k, "~").split(" /")[0].lower()
    return FIXED_CODES[k] if k in FIXED_CODES else next((c for name, c in by_name.items() if nm in name.lower()), "")


def planned_key(code: str, by_name: dict[str, str]) -> str | None:
    """The source key an executed query of this planned code carries, so the seeded row and the run's rows
    merge instead of printing twice; None when no adapter key names the row, which still prints."""
    cands = sorted({KEY_ALIASES.get(k, k) for k in SOURCE_NAMES if code_of(k, by_name) == code})
    return cands[0] if cands else None


def retrieved_by_source(searches: dict[str, dict], flow: dict | None = None) -> dict[str, int]:
    """Records fetched per source: analysis/flow.json's per-source `n_retrieved` where the flow states one,
    so Table 2's Retrieved and Identified columns come from one file, else the sum over the source's
    executed queries, so a run whose flow was not computed still gets a table."""
    per, out = dig(flow, "per_source") or {}, {}
    for qid, r in searches.items():
        k = source_key(qid, r)
        out[k] = out.get(k, 0) + int(r.get("n_retrieved") or 0)
    return {k: (int(n) if (n := dig(per.get(k), "n_retrieved")) is not None else v) for k, v in out.items()}


def sources_run(searches: dict[str, dict], flow: dict | None = None) -> int:
    """\\numSourcesRun: how many sources returned at least one record. The Results sentence says "returned
    records", so the rule is Retrieved > 0. The rule this replaces -- "reported a non-null API total" --
    counted a source that answered with a total and no record (bioRxiv, Mendeley, OpenDataLab, Redalyc and
    the two mention harvests) and dropped one whose adapter reports no total while retrieving records
    (Figshare, Hugging Face); it was wrong in both directions and reproducible from neither Table 2 nor the
    flow. `searches` must already be filtered to executed search-role queries."""
    return sum(1 for n in retrieved_by_source(searches, flow).values() if n > 0)


# information_sources.md's own order: literature, repositories, figure routes, the supplementary sweep, and
# last the arms that are not numbered sources (O1, the chase). Table 2 reads in the order the Methods
# paragraph enumerates; sorting the letters alphabetically put F1-F8 first and R14 between R1 and R2.
SERIES_ORDER = {"L": 0, "R": 1, "F": 2, "S": 3, "O": 4}


def code_sort_key(code: str, tie: str = "") -> tuple:
    """Natural order on a source code: the series in the protocol's order, then the number as a number,
    then any suffix (R9a follows R9), then `tie` for rows with no code at all."""
    m = re.match(r"([A-Za-z]+)(\d+)(.*)$", code or "")
    if not m:
        return (99, "~", 0, code or "", tie)
    return (SERIES_ORDER.get(m.group(1)[0].upper(), 98), m.group(1), int(m.group(2)), m.group(3), tie)


def n_failed(rec: dict) -> int:
    """Requests of this query that did not answer (status 0, a 5xx, a 429 that outlived every attempt).
    `sdr.repo_run.Run.query` writes `n_failed_requests` as a field of the entry and repeats it in the
    notes dict; the literature adapters write "status N at <endpoint>" into the notes string. Either way
    a source that went quiet is countable here, and Table 2 can keep it apart from a source that answered
    and had nothing."""
    if rec.get("n_failed_requests") is not None:
        return int(rec["n_failed_requests"] or 0)
    n = rec.get("notes")
    if isinstance(n, dict):
        return int(n.get("n_failed_requests") or 0)
    return len(re.findall(r"\bstatus \d+ at ", str(n or "")))


def executed(rec: dict) -> bool:
    """Did this query go out? Only a request timestamp, a total the source itself reported, or the role of a
    local harvest (which sends nothing and counts what it read) says so. A run date does not:
    `sdr.repo_run.write_not_run` stamps one on every planned id this version has no adapter for, and
    credential_mode `not-run` is that record. Reading the run date as evidence of a request put MultiCaRe and
    Open-PMC-18M into Table 2 with a query date, under a note saying the date was the earliest request
    recorded, and counted their thirteen templates in \\numQueries. A credential-gated id that was never sent
    (github_c01, github_c02 without GITHUB_TOKEN) is unsearched for the same reason, and its source's date
    then comes from the twenty queries that did run."""
    if str(rec.get("credential_mode") or "") == "not-run":
        return False
    # `supplement` is the two mention harvests, which send nothing and count what they read in the other
    # sources' records; `supplementary` (S1) is an HTTP sweep and has to show a request or a reported total.
    return bool(rec.get("first_request_ts") or rec.get("hit_count_api") is not None or rec.get("role") == "supplement")


# ----------------------------------------------------------------------------- protocol tables
def t_eligibility() -> str:
    rows = [[md(c) for c in r] for t in md_tables(ROOT / "PROTOCOL.md", r"^### 4\.[12] ") for r in t[1:]]
    return longtable("eligibility", "Eligibility criteria (PROTOCOL.md section 4).", ["Code", "Criterion", "Decision rule", "Rationale"], rows,
                     pcols(0.07, 0.13, 0.41, 0.33))


def t_data_items() -> str:
    sch = json.loads((ROOT / "charting_schema.json").read_text(encoding="utf-8"))
    rows = []
    for k, p in sch["properties"].items():
        if k == "schema_version":
            continue
        d = re.split(r"(?<=\.)\s", p.get("description", ""), 1)[0]
        ref = (p.get("$ref") or p.get("items", {}).get("$ref") or "").split("/")[-1]
        allowed = " / ".join(map(str, p.get("enum") or p.get("items", {}).get("enum") or [])) or ref or \
            (" | ".join(p["type"]) if isinstance(p.get("type"), list) else str(p.get("type", "")))
        if p.get("type") == "object" and "properties" in p:
            allowed = "object: " + ", ".join(p["properties"])
        rows.append([tt(k), esc_break(d[:220] + ("..." if len(d) > 220 else "")), esc_break(allowed)])
    return longtable("items", "Data items of the charting form (charting_schema.json).", ["Field", "Definition", "Allowed values"], rows, pcols(0.24, 0.46, 0.30))


def t_md(label: str, caption: str, path: Path, heading: str, keep: list[int], widths: tuple) -> str:
    """A protocol Markdown table (deviations log, PRISMA-ScR checklist) rendered as a longtable."""
    tabs = md_tables(path, heading)
    if not tabs:
        return pending_table(label, f"no table under {heading} in {path.name}")
    t = [r for r in tabs[0] if len(r) == len(tabs[0][0])]
    return longtable(label, caption, [md(t[0][i]) for i in keep], [[md(r[i]) for i in keep] for r in t[1:]], pcols(*widths), "", "scriptsize")


# ----------------------------------------------------------------------------- query tables
def units(d: dict[str, int]) -> str:
    """A per-unit count as one table cell: a record count bare, every other unit labelled
    ("43,095 figures"), so a figure or file count is never read as a record count. "0" when empty."""
    return "; ".join(f"{d[u]:,}" if u == "records" else f"{d[u]:,} {u}" for u in UNIT_ORDER if d.get(u)) or "0"


def unit_suffix(us: set) -> str:
    """The label a retrieved count needs: "" for a source that counts records, " figures"/" files"/
    " harvest" for one that counts something else, and every unit named when it counts in several."""
    other = [u for u in UNIT_ORDER if u != "records" and u in us]
    if not other:
        return ""
    return f" {other[0]}" if us == set(other[:1]) else " (" + ", ".join(other) + ")"


def t_sources(qs: dict[str, dict], flow: dict | None = None) -> str:
    """Table 2: one row per planned source of information_sources.md's summary table, plus the arms that
    are not numbered sources (the citation chase, the two mention harvests). A planned source with no
    executed query keeps its row and says "not run", so the table's rows are the same set as
    \\numSourcesPlanned; before this, a planned source that never ran vanished and the two harvest arms
    restored the count to thirty under duplicated codes, which invited the reader to conclude that every
    planned source ran. Hits are summed per-query totals (overlapping); Retrieved and Identified both come
    from analysis/flow.json where it has an entry, so the two columns cannot contradict each other; the
    date is the earliest request timestamp recorded, blank when no request was sent -- never the render's
    --run-date, which every write_not_run record carries and which made two unsearched sources look
    searched. Not sent counts the queries the protocol plans that this run did not send (no adapter in this
    version, or a credential it needs absent); Fetched is what the source handed over before the review's
    own local filter, beside Retrieved, which is what survived it, because without both a paging failure and
    a local filter print the same number. Hits is -- where no query of the source reported a total, which is
    not a total of zero.
    Hits and Retrieved carry their `unit` (queries.json): Open-i counts figures, Commons files, PhysioNet,
    TCIA and grand-challenge the size of the listing they filter locally, and an unlabelled 43,095 beside
    Zenodo's 2,598 records would be read as records. A dagger on the query count marks a row at least one
    of whose queries is partial (`n_failed_requests` above zero: the paging loop stopped at a request that
    never answered), which makes that row's counts lower bounds."""
    planned, by_name = planned_sources()
    per_source = dig(flow, "per_source") or {}
    searches = {q: r for q, r in qs.items() if r.get("role") in SEARCH_ROLES and executed(r)}
    ret = retrieved_by_source(searches, flow)

    def blank(code: str = "", name: str = "") -> dict:
        return {"n": 0, "hits": {}, "ntot": 0, "fetch": 0, "unsent": 0, "units": set(), "ret": 0, "modes": set(), "dates": set(),
                "cap": False, "cov": "", "code": code, "name": name, "planned_coverage": "", "not_run_reason": "", "req": 0,
                "bad": 0, "part": 0}
    by: dict[str, dict] = {}
    for pl in planned:  # seed first: a planned source that never ran still gets its row
        g = by.setdefault(planned_key(pl["code"], by_name) or f"~{pl['code']}", blank(pl["code"], pl["name"]))
        g["planned_coverage"] = pl["coverage"]
    for qid, r in qs.items():  # a not-run reason is recorded on the unexecuted query record, not on the run
        if (g := by.get(source_key(qid, r))) is None:
            continue
        if r.get("not_run_reason"):
            g["not_run_reason"] = g["not_run_reason"] or str(r["not_run_reason"])
        if r.get("role") in SEARCH_ROLES and not executed(r):  # planned, never sent: counted in its own column, never dated
            g["unsent"] += 1
    for qid, r in searches.items():
        k = source_key(qid, r)
        g = by.setdefault(k, blank())
        u = str(r.get("unit") or "records")
        g["n"], g["units"] = g["n"] + 1, g["units"] | {u}
        # A null hit_count_api means "this API reports no total", not zero. Summed as zero it printed
        # Figshare 0 hits beside 6 records retrieved, and Hugging Face 0 beside 31. `ntot` counts the
        # queries that did report one, so a source where none did prints -- instead of a total it never had.
        if r.get("hit_count_api") is not None:
            g["hits"][u], g["ntot"] = g["hits"].get(u, 0) + int(r["hit_count_api"]), g["ntot"] + 1
        g["fetch"] += int((r.get("n_fetched") if r.get("n_fetched") is not None else r.get("n_retrieved")) or 0)
        g["req"], g["bad"] = g["req"] + int(r.get("n_requests") or 0), g["bad"] + n_failed(r)
        # `partial` where the record has it: a failed request the adapter went looking for (Figshare's
        # term-ceiling probe) is counted in n_failed_requests but does not truncate the search. n_failed is
        # the fallback for the literature records, which carry the count in their notes and no flag.
        g["part"] += 1 if (r["partial"] if "partial" in r else n_failed(r)) else 0
        g["modes"].add(str(r.get("credential_mode") or "unknown"))
        if r.get("first_request_ts"):  # a request timestamp, never the run date: only a request dates a source
            g["dates"].add(str(r["first_request_ts"])[:10])
        g["cap"] |= bool(r.get("cap_hit"))
        g["cov"] = g["cov"] or str(r.get("coverage", "unknown"))
        g["name"] = SOURCE_NAMES[k] if k in FIXED_NAMES else g["name"] or str(r.get("source_name") or SOURCE_NAMES.get(k, k))
        g["code"] = FIXED_CODES[k] if k in FIXED_CODES else g["code"] or str(r.get("source_code") or code_of(k, by_name))
    rows, impossible, not_run = [], [], []
    for k, g in sorted(by.items(), key=lambda kv: code_sort_key(kv[1]["code"], kv[0])):
        ident = dig(per_source.get(k), "n_identified")
        if ident is not None and ident > ret.get(k, 0):
            impossible.append(f"{g['code'] or k} ({ident} identified from {ret.get(k, 0)} retrieved)")
        if not g["n"]:  # planned, never sent: the count columns say so rather than reading as zero hits
            rows.append([esc(g["code"]), esc(g["name"]), md(g["planned_coverage"] or "unknown"), "not run", "",
                         "--", str(g["unsent"]) if g["unsent"] else "--", "--", "--", "--", "--"])
            why = re.split(r"[;(]", g["not_run_reason"])[0].strip()
            not_run.append(f"{g['code']} {g['name']}" + (f" -- {why[:120]}" if why else ""))
            continue
        # A source whose requests mostly failed to answer (transport error or 5xx) did not retrieve zero
        # records: it was never reached. Printing 0 would make the two read as the same finding, which is
        # the one thing this table must not do (Open-i, 70 of 71 requests failed, printed 0 retrieved).
        quiet = ret.get(k, 0) == 0 and g["bad"] and g["bad"] * 2 > max(g["req"], 1)
        rows.append([esc(g["code"]), esc(g["name"]), md(g["cov"] or g["planned_coverage"] or "unknown"), esc(", ".join(sorted(g["modes"]))),
                     esc(min(g["dates"]) if g["dates"] else ""), str(g["n"]) + ("\\dag{}" if g["part"] and not quiet else ""),
                     str(g["unsent"]) if g["unsent"] else "--",
                     "no answer" if quiet else ("--" if not g["ntot"] else units(g["hits"]) + ("*" if g["cap"] else "")),
                     "no answer" if quiet else f"{g['fetch']:,}" + unit_suffix(g["units"]),
                     "no answer" if quiet else f"{ret.get(k, 0):,}" + unit_suffix(g["units"]),
                     f"{ident:,}" if ident is not None else "--"])
    note = ("* paging cap reached on at least one query. $\\dag$ at least one query of the row is partial: a request did not answer "
            "and the paging loop stopped there, so that row's counts are lower bounds. Counts carry the unit the source counts in: an "
            "unlabelled number is records, and figure, file and harvest-listing counts (Open-i figures, Wikimedia Commons files, the "
            "PhysioNet, TCIA and grand-challenge listings) are labelled and are never added to a record count. "
            "Q.: queries whose request went out. Not sent: queries the protocol plans that this run did not send, because the "
            "source has no adapter in this version or a credential it requires was absent; the reason is in the Credential mode cell "
            "of a row that sent nothing, and in Appendix~\\ref{app:search} for every id. "
            "Hits: sum of the totals each query reported (queries overlap; records are "
            "de-duplicated in the flow); -- where no query of the source reported a total, which is not a total of zero. Fetched: "
            "items the source handed over, before the review's own local filter. Retrieved: records kept after that filter, from "
            "analysis/flow.json where it has an entry, else summed over the source's queries; Fetched above Retrieved is the local "
            "filter working, and Fetched below the cap on a capped query is a paging failure. ``no answer'': the "
            "source's requests mostly failed to answer (transport error or 5xx), which is not the finding that it returned no records. "
            "Identified: records "
            "this source contributed to the flow after within-source de-duplication (analysis/flow.json); -- where the flow has no entry. "
            f"Sources returning at least one record (Retrieved $>$ 0): {sources_run(searches, flow)} of {len(planned)} planned. "
            "A row with -- in every count column is a planned source no query was sent to, with the recorded reason in the Credential mode "
            "cell. Date: earliest request timestamp recorded for the source, blank when no request was sent; never the render's run "
            "date. O1 is the citation-chasing arm, not a numbered source; R9a and R10a "
            "are the mention harvests run over the other sources' records, which belong to R9 and R10 and are not separate planned sources.")
    if not_run:
        note += " Planned but not run in this run: " + esc("; ".join(not_run)) + "."
    if impossible:
        note += (" WARNING, inconsistent upstream counts (sdr.flow_counts): more records identified than retrieved for "
                 + esc("; ".join(impossible)) + ".")
    return longtable("sources", "Information sources, coverage, credential mode, query date, queries sent and not sent, hit counts and records identified (queries.json; analysis/flow.json).",
                     ["\\#", "Source", "Coverage", "Credential mode", "Date", "Q.", "Not sent", "Hits (API)", "Fetch.", "Retr.", "Ident."], rows,
                     pcols(0.06, 0.125, 0.13, 0.115, 0.075, 0.035, 0.045, 0.085, 0.075, 0.075, 0.08), note)


def brk(s: Any) -> str:
    """A query string escaped and breakable at its separators, for the appendix's monospace paragraphs."""
    return re.sub(r"([/:=|)+,\]\"*-]|\\[&_])", lambda m: m.group(1) + r"\allowbreak{}", esc(s))


def _not_run_why(r: dict) -> str:
    """Why this planned id was not sent, in the protocol's own words: the `not_run_reason` of
    queries/*.yaml (a source with no adapter in this version) or the `condition` that would have
    triggered it (the pubmed_01a-d [dp] splits, sent only when pubmed_01 goes over the history limit),
    both merged into the record by sdr.manuscript.load_query_records, or the adapter's own
    notes.reason where it skipped the id for want of a credential (github_c01, github_c02). Appendix A
    printed "run not run" with none of them, which said nothing about fourteen templates, four
    conditional splits and two credential-gated ids."""
    notes = r.get("notes") if isinstance(r.get("notes"), dict) else {}
    why = str(r.get("not_run_reason") or notes.get("reason") or r.get("condition") or "no reason recorded")
    return why if len(why) <= 240 else why[:237].rstrip() + "..."


def t_search_strings(qs: dict[str, dict]) -> str:
    """Appendix A: one block per query_id (executed chase ids collapsed to one), pilot rows marked by
    their role. A hit count carries the unit it is counted in (records, figures, files, harvest) and a query
    whose requests did not all answer is marked partial, because both change what the number means. `fetched`
    is printed beside `retrieved` wherever they differ: without it a paging failure and a local filter that
    kept three of ninety items read the same. An id that never went out says so and gives its reason instead
    of a run date. The first string is the operational one the adapter sends (queries/*.yaml); when the
    protocol's markdown form differs it follows, and when the run recorded a different sent string
    that follows too, so nothing is hidden and nothing is retyped."""
    out = ["\\noindent Non-Latin strings are printed as Unicode code points; the UTF-8 string is in \\texttt{queries.json}.\\par"]
    chase = [r for q, r in qs.items() if source_key(q, r) == "chase" and executed(r)]
    for qid, r in qs.items():
        if source_key(qid, r) == "chase":
            continue
        # dict.get's default fires only on a missing key, and these keys are present holding None wherever an API
        # reports no total or an id was never sent, so the appendix printed the literal "hits None" and an empty
        # credential mode. A count that was never reported is said in words; an id that never ran gives its reason.
        run_note = (f"not run ({esc(_not_run_why(r))})" if not executed(r) else f"run {esc(r.get('run_date') or 'date not recorded')}")
        hits = "not reported" if r.get("hit_count_api") is None else f"{esc(r['hit_count_api'])} ({esc(r.get('unit') or 'records')})"
        got = "n/a" if r.get("n_retrieved") is None else esc(r["n_retrieved"])
        fetched = r.get("n_fetched")
        meta = (f"{esc(r.get('source_name') or SOURCE_NAMES.get(source_key(qid, r), r.get('source')))}; role {esc(r.get('role'))}; "
                f"endpoint \\url{{{r.get('endpoint', '')}}}; {run_note}; hits {hits}"
                + (f"; fetched {esc(fetched)}, retrieved {got}" if fetched is not None and fetched != r.get("n_retrieved")
                   else f"; retrieved {got}")
                + f"; {esc(r.get('credential_mode') or 'credential mode not recorded')}"
                + (f"; partial ({esc(n_failed(r))} request(s) did not answer)" if (r["partial"] if "partial" in r else n_failed(r)) else "")
                + (f"; cap {esc(r['cap_hit'])}" if r.get("cap_hit") else "") + (f"; grammar {esc(r['grammar'])}" if r.get("grammar") else "")
                + (f"; derived from {tt(r['derived_from_query'])} (a description, not a sent string)" if r.get("derived_from_query") else ""))
        lines = [f"\\noindent{{\\ttfamily\\footnotesize\\raggedright\\emergencystretch=2em {brk(r.get('query_string') or '(no string recorded)')}\\par}}"]
        if r.get("markdown_string") and r["markdown_string"] != r.get("query_string"):
            lines.append(f"\\noindent{{\\footnotesize\\raggedright as written in information\\_sources.md: {{\\ttfamily {brk(r['markdown_string'])}}}\\par}}")
        if r.get("query_string_run"):
            lines.append(f"\\noindent{{\\footnotesize\\raggedright as sent by the run (differs from the protocol string): {{\\ttfamily {brk(r['query_string_run'])}}}\\par}}")
        out.append(f"\\par\\medskip{{\\raggedright\\noindent\\textbf{{{tt(qid)}}} --- {meta}.\\par}}\n" + "\n".join(lines))
    if chase:
        out.append(f"\\par\\medskip\\noindent\\textbf{{{tt('openalex_03*')}}} --- OpenAlex citation chasing, one hop: {len(chase)} ids chased, "
                   f"{sum(int(c.get('hit_count_api') or 0) for c in chase):,} hits in total.\\par")
    else:
        out.append(f"\\par\\medskip\\noindent\\textbf{{{tt('openalex_03*')}}} --- OpenAlex citation chasing: no request recorded in this run "
                   "(the templates are in queries/literature.yaml).\\par")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------- charting and analysis tables
def t_datasets_main(ch: list[dict], q: dict | None) -> str:
    per, rows = dig(q, "per_dataset") or {}, []
    for d in sorted(ch, key=lambda d: ("".join(d.get("modality", [])), d.get("year", 0), d.get("name", ""))):
        lvl = next((dig(d, f"annotation_origin_by_type.{t}") for t in ("per-vertebra-level-names", "segmentation-3d", "segmentation-2d")
                    if dig(d, f"annotation_origin_by_type.{t}")), d.get("annotation_origin", []))
        qd = per.get(d.get("id"), {})
        rows.append([tt(d.get("id")), esc(d.get("name")), str(d.get("year", "")), esc(",".join(d.get("country", []))),
                     esc("/".join(MOD.get(m, m) for m in d.get("modality", []))), esc("".join(REG.get(r, r[0]) for r in d.get("region", []))),
                     f"{d['n_subjects']:,}" if d.get("n_subjects") is not None else "?", esc(",".join(ANN.get(a, a) for a in d.get("annotation_types", []))),
                     esc(",".join(ORI.get(o, o) for o in lvl)), "".join({"yes": "Y", "no": "N"}.get(dig(d, f"variant_labels.{v}.status"), "?") for v in ("L6", "T13", "LSTV")),
                     esc(dig(d, "licence.tier")), esc(d.get("access_route")), esc(dig(qd, "total") if dig(qd, "total") is not None else "--"),
                     "yes" if dig(qd, "fit_level_id") else "--"])
    return longtable("datasets_main", "Characteristics of the included datasets (charting records; quality total and fitness from analysis/quality.json).",
                     ["Id", "Name", "Year", "Ctry", "Mod.", "Reg.", "Subj.", "Annot.", "Orig.", "Var.", "Lic.", "Route", "Q", "Fit"], rows,
                     pcols(0.11, 0.125, 0.05, 0.05, 0.075, 0.05, 0.065, 0.085, 0.06, 0.065, 0.065, 0.09, 0.03, 0.04),
                     "Ctry: ISO country. Mod.: XR radiograph, FL fluoroscopy. Reg.: C cervical, T thoracic, L lumbar, S sacrum-pelvis, W whole-spine. Annot.: lvl level "
                     "names, seg3/seg2 segmentation, lmk landmarks, box boxes, ctr centroids, path pathology, frac fracture grade, meas measurements, rep reports, "
                     "img image-level. Origin: EM expert-manual, ECM expert-corrected-model, MG model-generated, CI counting-inferred, RD report-derived, "
                     "CRT crowd-or-trainee, CAP caption-derived (origin of the level names, else of the segmentation). Var.: L6, T13 and LSTV in that "
                     "order, Y labelled, N stated absent, ? silent. Lic.: licence tier. Q: quality total 0--20; Fit: fit for level identification.", "scriptsize")


def reliability_note(q: dict | None) -> str:
    """The rubric-reliability sentence for the quality table's note, from quality.json's `reliability`
    block {n, icc_total: {value, ci: [lo, hi]}, per_item_kappa: {Q1..Q10: number | 'not estimable'}}
    (SAP A4.5, written by sdr.reliability); a red pending marker while that block is absent, so the
    text can never claim a reliability figure the file does not hold."""
    rel = dig(q, "reliability")
    if not rel:
        return r"\pending{Rubric reliability on the blind re-charted sample: sdr.reliability (SAP A4.5) not run}"
    items = val(dig(rel, "per_item_kappa")) or {}
    kap = "; ".join(f"Q{k} {esc(fmt(items.get(f'Q{k}'), 'dec') or items.get(f'Q{k}') or '--')}" for k in range(1, 11))
    return (f"Rubric reliability on the blind re-charted sample (n = {esc(fmt(dig(rel, 'n'), 'int') or '--')}): ICC(2,1) on the total "
            f"{esc(fmt(dig(rel, 'icc_total.value'), 'dec') or '--')} {esc(ci(rel, 'icc_total.ci.0', 'icc_total.ci.1', 'dec'))}; "
            f"linearly weighted $\\kappa$ per item: {kap}.")


def t_quality(q: dict | None) -> str:
    per = dig(q, "per_dataset")
    if not per:
        return pending_table("quality", "analysis/quality.json absent or without per_dataset")
    rows = [[tt(i)] + [esc(dig(d, f"items.Q{k}.score") if isinstance(dig(d, f"items.Q{k}"), dict) else dig(d, f"items.Q{k}")) for k in range(1, 11)]
            + [esc(dig(d, "total")), "yes" if dig(d, "fit_level_id") else esc(dig(d, "fit_level_id_fail_rule") or "--"), "yes" if dig(d, "fit_stitching") else "--"]
            for i, d in sorted(per.items())]
    return longtable("quality", "Quality rubric scores per dataset (analysis/quality.json; items of quality_rubric.md).",
                     ["Id"] + [f"Q{k}" for k in range(1, 11)] + ["Total", "Fit (fail rule)", "Stitch"], rows, pcols(0.16, *([0.045] * 10), 0.06, 0.12, 0.06),
                     reliability_note(q), "scriptsize")


def t_counts(desc: dict | None) -> str:
    if not desc:
        return pending_table("counts", "analysis/descriptives.json absent")
    cols = ["n_datasets", "n_subjects_sum", "n_subjects_median", "n_images_sum"]

    def cell(v: Any) -> str:
        return "--" if v is None else esc(f"{v:,}" if isinstance(v, (int, float)) and not isinstance(v, bool) else v)
    rows = []
    for key in sorted(k for k in desc if k.startswith("by_")):
        rows.append([rf"\textbf{{{esc(key[3:].replace('_', ' '))}}}"] + [""] * len(cols))
        rows += [[r"\quad " + esc(s)] + [cell(dig(v, c)) for c in cols] for s, v in sorted((val(desc[key]) or {}).items())]
    return longtable("counts", "Counts of datasets and totals of subjects and images by stratum (analysis/descriptives.json).",
                     ["Stratum", "Datasets", "Subjects (sum)", "Subjects (median)", "Images or volumes (sum)"], rows, pcols(0.34, 0.12, 0.14, 0.14, 0.16),
                     "Reported subjects summed across datasets (persons may recur); one dataset per parent family; figure-derived and estimated counts excluded from sums.")


def t_availability(av: dict | None) -> str:
    if not av:
        return pending_table("availability", "analysis/availability.json absent")
    rows = [[esc(r), esc(f"{val(n):,}" if isinstance(val(n), int) else val(n)), "", ""] for r, n in sorted((val(dig(av, "route_distribution.overall")) or {}).items())]
    for name, lab in (("primary", "route = open-download"), ("file_url", "file URL 200/206 on both probes"), ("recipe_eligible", "route in {open-download, registration}")):
        if (d := dig(av, f"described_public_downloads.{name}")) is not None:
            rows.append([esc("described as public: " + lab), esc(dig(d, "numerator")), esc(dig(d, "denominator")),
                         esc(f"{fmt(dig(d, 'proportion'), 'pct')} {ci(d, 'ci.0', 'ci.1', 'pct')}" if dig(d, "proportion") is not None else "--")])
    return longtable("availability", "Availability outcomes (analysis/availability.json; protocol section 10 rules).",
                     ["Outcome", "n", "Denom.", "Proportion (95\\% CI)"], rows, pcols(0.48, 0.1, 0.1, 0.32))


def pooled_estimator(pv: dict | None, variant: str = "LSTV") -> str | None:
    """The estimator the file names for a variant's pooled row (None when nothing was pooled). The
    file's free-text estimator_note is never consulted: it names the GLMM as what is missing."""
    return dig(pv, f"{variant}.pooled.estimator") or dig(pv, "estimator")


def is_primary_estimator(name: str | None) -> bool:
    """SAP A5.2 names the primary estimator: the logit random-intercept GLMM by adaptive Gauss-Hermite
    quadrature. Anything else (DerSimonian-Laird, REML) is a sensitivity analysis."""
    return bool(name) and re.search(r"GLMM|Gauss.Hermite|random.intercept", str(name), re.I) is not None and "sensitivity" not in str(name).lower()


def t_pooled_variants(pv: dict | None) -> str:
    if not pv:
        return pending_table("pooled_variants", "analysis/pooled_variants.json absent")
    rows = []
    for v in ("L6", "T13", "LSTV"):
        rows.append([rf"\textbf{{{v}}}"] + [""] * 7)
        rows += [[r"\quad " + tt(dig(d, "id")), esc(dig(d, "modality")), esc(dig(d, "x")), esc(dig(d, "n")), esc(f"{fmt(dig(d, 'p'), 'pct')} {ci(d, 'ci_low', 'ci_high', 'pct')}"),
                  esc(dig(d, "selection")), esc(dig(d, "ascertainment")), esc(dig(d, "definition_class"))] for d in val(dig(pv, f"{v}.per_dataset")) or []]
        p, est = dig(pv, f"{v}.pooled"), pooled_estimator(pv, v)
        label = (f"pooled, {est or 'estimator not named'}" + ("" if is_primary_estimator(est) else "; sensitivity estimator, primary GLMM (SAP A5.2) pending")) if p else "pooled"
        rows.append([r"\quad\emph{" + esc(label) + " (k = " + esc(dig(pv, f"{v}.k_eligible")) + ")}", "", "", "",
                     esc(f"{fmt(dig(p, 'estimate'), 'pct')} {ci(p, 'ci_low', 'ci_high', 'pct')}; PI {fmt(dig(p, 'pi_low'), 'pct')} to {fmt(dig(p, 'pi_high'), 'pct')}"
                         if p else "pooling not done (k < 5)"), "", "", ""])
    note = dig(pv, "estimator_note")
    return longtable("pooled_variants", "Per-dataset prevalence of L6, T13 and LSTV with exact intervals; illustrative pooled summary when k $\\geq$ 5, "
                     "with the estimator named in each pooled row (analysis/pooled_variants.json).",
                     ["Dataset", "Mod.", "x", "n", "Prevalence (95\\% CI)", "Selection", "Ascertainment", "Definition"], rows,
                     pcols(0.19, 0.09, 0.05, 0.05, 0.19, 0.13, 0.15, 0.15), f"Estimator note recorded in the analysis file: {esc(note)}" if note else "", "scriptsize")


def t_agreement(pa: dict | None) -> str:
    if not pa:
        return pending_table("agreement", "analysis/pooled_agreement.json absent")
    rows = [[tt(dig(d, "id")), esc(dig(d, "statistic")), esc(fmt(dig(d, "value"), "dec") or "--"), esc(ci(d, "ci.0", "ci.1", "dec") if dig(d, "ci") else "--"),
             esc(dig(d, "n")), esc(dig(d, "comparator")), esc(dig(d, "n_categories")), esc(dig(d, "group"))] for d in val(dig(pa, "per_dataset")) or []]
    return longtable("agreement", "Inter-rater agreement per dataset (analysis/pooled_agreement.json).",
                     ["Dataset", "Statistic", "Value", "95\\% CI", "n", "Comparator", "Categories", "Group"], rows, pcols(0.2, 0.1, 0.07, 0.12, 0.06, 0.13, 0.08, 0.14))


def t_grid(gc: dict | None) -> str:
    if not gc:
        return pending_table("grid", "analysis/grid_coverage.json absent")
    rows = [[tt(dig(d, "id")), esc(dig(d, "status")), esc(dig(d, "n_subjects_on_grid")), esc(dig(d, "path") or "--")] for d in val(dig(gc, "per_dataset")) or []]
    order = val(dig(gc, "recipe_order")) or []
    note = ("Recipe first-run order (reachable, fit for level identification, not on the grid, by quality total): "
            + ", ".join(f"{tt(dig(o, 'id'))} ({esc(dig(o, 'quality_total'))})" for o in order)) if order else ""
    return longtable("grid", "Coverage of the authors' compute grid (analysis/grid_coverage.json; author-specific, not reproducible by a second team).",
                     ["Dataset", "On grid", "Subjects on grid", "Path"], rows, pcols(0.2, 0.1, 0.14, 0.46), note)
