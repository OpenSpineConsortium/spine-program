"""Check every transcribed value against the source paper itself, in context: right level, right sex, right role.

    python3 code/verify_tables.py          # from synthetic_spine/; network on the first run; standard library only

Inputs: sources.json (the papers and their PMC and PubMed ids), data/series_papers.csv (which paper each series was
read from), data/level_references.csv and data/pedicle_width_references.csv (the values). For each paper, PMC's
full text (JATS XML, open-access subset) and the PubMed abstract are fetched once into .cache/ (not committed).

A value is CONFIRMED only where the paper prints it in context:
  - in a table cell whose row label, column header or section row names the value's level (the caption is used
    only when none of those names a level), whose column or row does not name the other sex or another species,
    and where the number sits in the right role: the first number of a "mean +/- SD" or "mean (SD)" cell for a
    mean, the second for a dispersion, or a column headed for that role;
  - or in a clause of the running text or the PubMed abstract (a sentence split at its commas and semicolons) that
    gives the number to the value's level: the level the clause names, the nearest one when it names several, or
    the one named by the clause before it in the same sentence when it names none. A sex-specific value needs its
    sex named next to the number ("5.6 +/- 1.1 mm for men"); a number after "+/-" is a dispersion; a number in a
    range is neither.
Exact matches are looked for everywhere before rounded ones. A printed number confirms a value exactly when they are
equal and the printed number carries at least the value's significant decimals ("8.7" confirms "8.70"; "4" does not
confirm "4.5"); it confirms it ROUNDED when it carries more decimals than the value was recorded with and rounds to
it ("2.61" for "2.6"). Every confirmation records the cell or the clause it came from, so it can be read by a person.

One convention is declared per paper, never assumed: DISC_UNDER_VERTEBRA_ABOVE names the papers whose tables list
each disc under the vertebra above it, with the evidence for that reading.

A number found only out of context (another level, another sex, another role, another species) is reported as such
and never counted. A series no table of its own paper confirms is also traced by table ROW: the row, in any paper,
that holds the largest share of its means is named when it holds at least three and at least four in five.
Whole-millimetre series are not traced; their values recur everywhere.

Writes verification/values.csv (one line per value) and verification/series.csv (one line per series).
"""
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
CACHE = HERE / ".cache"
OUTDIR = HERE / "verification"
UA = {"User-Agent": "spine-program synthetic_spine verifier (research; urllib)"}
PM = chr(0xB1)                                       # plus-minus sign
DASHES = "-" + chr(0x2013) + chr(0x2014) + chr(0x2212) + "/"   # hyphen, en dash, em dash, minus sign, slash
DC = re.escape(DASHES)                                # the same, safe inside a character class
SPELT = {PM: "+/-", chr(0x2013): "-", chr(0x2014): "-", chr(0x2212): "-", chr(0x2009): " ", chr(0xA0): " "}
# a number not glued to a letter or another number, so the 4 of "L4" or the 12 of "T12" is not read as a value
NUM = re.compile(r"(?<![A-Za-z\d.,])\d+(?:[.,]\d+)?")
# a level as printed: L4, Th12, L4-L5, L4/5, L4L5, T12-L1; the second number may not run into a decimal
LEVEL = re.compile(r"(?<![A-Za-z0-9])(Th|C|T|L|S)\s?(\d{1,2})(?![0-9]|[.,]\d)"
                   r"(?:\s*[" + DC + r"]\s*(?:(Th|C|T|L|S)\s?)?(\d{1,2})(?![0-9]|[.,]\d)|(Th|C|T|L|S)(\d{1,2})(?![0-9]))?")
NONHUMAN = re.compile(r"\b(porcine|pigs?|swine|ovine|sheep|bovine|calf|calves|goats?|caprine|canine|dogs?|rats?|"
                      r"mice|mouse|murine|monkeys?|baboons?|primates?)\b", re.I)
SEXWORD = re.compile(r"\b(men|man|males?|women|woman|females?|boys|girls)\b", re.I)
# the measures a table cell may name: (abbreviations, matched case-sensitively; words, matched in any case). A cell
# that names one of them and not the value's own measure is out of context.
MEASURE_WORDS = {
    "h_ant": (r"VBHa|AVBH", r"anterior (vertebral )?(body )?height|height,? anterior"),
    "h_post": (r"VBHp|PVBH", r"posterior (vertebral )?(body )?height|height,? posterior"),
    "h_mid": (r"VBH[cm]", r"(middle|central|mid) (vertebral )?(body )?height"),
    "endplate": (r"[UL]?EPW[ul]?", r"end-?plate width"),
    "endplate_depth": (r"[UL]?EPD[ul]?", r"end-?plate depth"),
    "canal_w": (r"SCW|ML|IPD", r"interpedicular|canal width"),
    "canal_ap": (r"SCD|AP|APD", r"canal (depth|length)|(mid)?sagittal (canal )?diameter|antero-?posterior"),
    "disc": (r"IDH|DH", r"disc height|intervertebral (disc )?(space )?height"),
    "pedicle": (r"[LR]?PW|TPW|PDW", r"pedicle width|transverse (pedicle )?(diameter|width)|pedicle isthmus"),
    "pedicle_height": (r"[LR]?PH|SPW", r"pedicle height|sagittal pedicle"),
    "body_length": (r"VL|VBL", r"body length"),
    "body_width": (r"VW|VBW", r"body width"),
    "area": (r"CSA", r"cross-sectional"),
    "angle": (r"ILA|LI", r"angle\b|inclination"),
}
MEASURE_OF = {"PDW": "pedicle"}          # the pedicle table's name for pedicle width
DISC_UNDER_VERTEBRA_ABOVE = {
    "busscher2010": "Table 3 gives an IDH for every vertebra from C3 to L5 and has no S1 row, while the spines were "
                    "dissected from C3 to S1: C3's disc can only be C3-C4 and L5's only L5-S1",
}


def ascii_text(text):
    text = str(text or "")
    for char, spelling in SPELT.items():
        text = text.replace(char, spelling)
    return unicodedata.normalize("NFKD", text).encode("ascii", "replace").decode("ascii")


# --------------------------------------------------------------------------------------------- fetching

def fetch(kind, ident):
    folder = CACHE / kind
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{ident}.xml"
    if not path.exists():
        db, num = ("pmc", ident.replace("PMC", "")) if kind == "pmc" else ("pubmed", ident)
        extra = "" if kind == "pmc" else "&rettype=abstract"
        url = (f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={db}&id={num}&retmode=xml{extra}"
               "&tool=spine-program-synthetic-spine")
        for attempt in range(4):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                    path.write_bytes(r.read())
                break
            except Exception:
                time.sleep(3 * (attempt + 1))
        time.sleep(0.5)
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_of(el):
    return " ".join("".join(el.itertext()).split()) if el is not None else ""


def parse(xml):
    try:
        return ET.fromstring(re.sub(r"<!DOCTYPE[^>]*>", "", xml))
    except ET.ParseError:
        return None


# --------------------------------------------------------------------------------------------- levels

def canon(m):
    first = ("T" if m.group(1) == "Th" else m.group(1)) + m.group(2)
    if m.group(4):
        letter = m.group(3) or m.group(1)
        return first + ("T" if letter == "Th" else letter) + m.group(4)
    if m.group(6):
        return first + ("T" if m.group(5) == "Th" else m.group(5)) + m.group(6)
    return first


def levels_in(text):
    """Every level the text names, as (start, end, level) with the level spelt as the tables spell it."""
    return [(m.start(), m.end(), canon(m)) for m in LEVEL.finditer(text)]


def upper_vertebra(level):
    m = re.fullmatch(r"([CTLS]\d+)[CTLS]\d+", level)
    return m.group(1) if m else None


# --------------------------------------------------------------------------------------------- tables as grids

def grid(tw):
    """The table as (header rows, body rows), each row a list of cell texts, spans expanded."""
    def expand(trs):
        rows, pending = [], {}
        for tr in trs:
            row, col, cells, ci = [], 0, [c for c in tr if c.tag in ("td", "th")], 0
            while ci < len(cells) or col in pending:
                if col in pending:
                    text, left = pending.pop(col)
                    row.append(text)
                    if left > 1:
                        pending[col] = (text, left - 1)
                    col += 1
                    continue
                c = cells[ci]
                ci += 1
                text = text_of(c)
                for _ in range(max(1, int(c.get("colspan", "1") or 1))):
                    row.append(text)
                    rs = int(c.get("rowspan", "1") or 1)
                    if rs > 1:
                        pending[col] = (text, rs - 1)
                    col += 1
            rows.append(row)
        return rows
    head = [tr for th in tw.iter("thead") for tr in th.iter("tr")]
    body = [tr for tb in tw.iter("tbody") for tr in tb.iter("tr")]
    if not head and not body:
        body = list(tw.iter("tr"))
    if not head and body:
        head, body = body[:1], body[1:]
    return expand(head), expand(body)


def numeric_only(text):
    return bool(text) and not re.sub(r"[\d.,\s()+" + re.escape(PM) + DC + r"*%<>=a-z]", "", text.replace("NS", ""))


def paired(cell):
    """True when the cell prints a mean with its dispersion: "27.0 +/- 2.2", "27 + 2.2" or "27.0 (2.2)"."""
    return (PM in cell or "+/-" in cell or re.search(r"\d\s*\+\s*\d", cell) is not None
            or re.search(r"\d\s*\(\s*\d", cell) is not None)


def cells_of(tw):
    """Every body cell: dict(nums, roles, cell, caption, header, label, section)."""
    head, body = grid(tw)
    caption = f"{text_of(tw.find('label'))} {text_of(tw.find('caption'))}"
    out, section = [], ""
    for row in body:
        texts = [t for t in row if t]
        if texts and all(not NUM.search(t) for t in texts) and len(set(texts)) == 1:
            section = texts[0]              # a spanning row such as "Male" or "Lumbar 1" heads the rows below
            continue
        label = " ".join(dict.fromkeys(t for t in row if t and not numeric_only(t)))
        for j, cell in enumerate(row):
            if not numeric_only(cell):
                continue
            nums = NUM.findall(cell)
            if not nums:
                continue
            header = " ".join(dict.fromkeys(h[j] for h in head if j < len(h) and h[j]))
            names_sd = re.search(r"\b(SD|S\.D\.|standard deviation|SEM|SE)\b", header, re.I) is not None
            names_mean = re.search(r"\b(mean|average|median)\b", header, re.I) is not None
            if len(nums) >= 2 and (paired(cell) or (names_sd and names_mean)):
                roles = ["mean", "sd"] + ["other"] * (len(nums) - 2)
            elif names_sd and not names_mean:
                roles = ["sd"] * len(nums)
            elif names_mean and not names_sd:
                roles = ["mean"] * len(nums)
            else:
                roles = [None] * len(nums)
            out.append({"nums": nums, "roles": roles, "cell": cell, "caption": caption, "header": header,
                        "label": label, "section": section})
    return out


# --------------------------------------------------------------------------------------------- context tests

FEMALE = re.compile(r"\b(females?|women|woman|girls|F)\b", re.I)
MALE_WORD = re.compile(r"\b(males?|men|man|boys)\b", re.I)
MALE_LETTER = re.compile(r"\bM\b")


def sexes_in(text):
    found = set()
    if FEMALE.search(text):
        found.add("F")
    if MALE_WORD.search(re.sub(r"\bfemales?\b|\bwom[ae]n\b", "", text, flags=re.I)) or MALE_LETTER.search(text):
        found.add("M")
    return found


def measures_named(text):
    """The measures a stretch of context names."""
    return {m for m, (abbr, words) in MEASURE_WORDS.items()
            if re.search(r"(?<![A-Za-z])(?:" + abbr + r")(?![A-Za-z])", text)
            or re.search(r"\b(?:" + words + r")", text, re.I)}


def table_context(c, level, sex, paper_key, measure):
    """None when the cell is in context for the value; otherwise why not. Second item: a qualifier for the result."""
    own = f"{c['header']} {c['label']} {c['section']}"
    if NONHUMAN.search(own):
        return "another species", ""
    said = measures_named(own) or measures_named(c["caption"])
    if said and MEASURE_OF.get(measure, measure) not in said:
        return "another measure", ""
    named = {l for _, _, l in levels_in(own)} or {l for _, _, l in levels_in(c["caption"])}
    qualifier = ""
    if level not in named:
        upper = upper_vertebra(level)
        if (paper_key in DISC_UNDER_VERTEBRA_ABOVE and upper and named == {upper}
                and re.search(r"\bdisc|\bIDH\b", f"{c['header']} {c['caption']}", re.I)):
            qualifier = "; the paper lists each disc under the vertebra above it"
        else:
            return "another level", ""
    specific = sexes_in(own)
    if sex in ("M", "F"):
        if specific and specific != {sex}:
            return "another sex", ""
        if not specific and sexes_in(c["caption"]) - {sex} and sex not in sexes_in(c["caption"]):
            return "another sex", ""
    elif len(specific) == 1:
        return "one sex only", ""
    return None, qualifier


SENTENCE = re.compile(r"(?<=[.;!?])\s+(?=[A-Z(\[])")
CLAUSE = re.compile(r",\s+|;\s+")


def text_role(before):
    tail = before[-14:]
    if re.search(r"(" + re.escape(PM) + r"|\+/-|\+-|\bSD\s*[=:]?)\s*$", tail):
        return "sd"
    if re.search(r"(?<![A-Za-z\d.,])\d+(?:[.,]\d+)?\s*(mm)?\s*\(\s*(SD\s*[=:]?\s*)?$", tail):
        return "sd"
    if re.search(r"(range\s*:?|\d\s*[" + DC + r"]|\bto)\s*$", tail):
        return "other"
    return "mean"


def text_hits(text, value, kind, level, sex, rounded_ok):
    """The first clause that gives this number to this level, sex and role; returns the clause or ''."""
    for sentence in SENTENCE.split(text):
        clauses, inherited = CLAUSE.split(sentence), None
        for clause in clauses:
            named = levels_in(clause)
            distinct = {l for _, _, l in named}
            for m in NUM.finditer(clause):
                if not match(value, m.group(0), rounded_ok):
                    continue
                if text_role(clause[:m.start()]) != kind:
                    continue
                if any(s <= m.start() < e for s, e, _ in named):
                    continue
                if len(distinct) == 1:
                    lev = next(iter(distinct))
                elif distinct:
                    lev = min(named, key=lambda t: min(abs(m.start() - t[1]), abs(t[0] - m.end())))[2]
                else:
                    lev = inherited
                if lev != level:
                    continue
                after = SEXWORD.search(clause, m.end())
                before = list(SEXWORD.finditer(clause[:m.start()]))
                word = after.group(1) if after else (before[-1].group(1) if before else "")
                said = "" if not word else ("F" if word.lower().startswith(("wom", "fem", "girl")) else "M")
                if sex in ("M", "F") and said != sex:
                    continue
                if sex not in ("M", "F") and said:
                    continue
                return clause
            if len(distinct) == 1:
                inherited = next(iter(distinct))
    return ""


def precision(value):
    v = value.replace(",", ".")
    return len(v.split(".")[1]) if "." in v else 0


def significant(value):
    v = value.replace(",", ".")
    return len(v.split(".")[1].rstrip("0")) if "." in v else 0


def match(value, printed, rounded_ok):
    x, v = float(printed.replace(",", ".")), float(value)
    if precision(printed) >= significant(value) and abs(x - v) < 1e-9:
        return "exact"
    if rounded_ok and precision(printed) > precision(value) and round(x, precision(value)) == v:
        return "rounded"
    return ""


# --------------------------------------------------------------------------------------------- one paper

class Paper:
    def __init__(self, key, pmcid, pmid):
        self.key, self.tables, self.text, self.abstract, self.images, self.image_tables = key, [], "", "", False, 0
        if pmcid:
            root = parse(fetch("pmc", pmcid))
            if root is not None and root.find(".//body") is not None:
                for tw in root.iter("table-wrap"):
                    self.tables.append((text_of(tw.find("label")) or "unlabelled table", cells_of(tw)))
                self.image_tables = sum(1 for _, cells in self.tables if not cells)
                self.images = bool(self.tables) and self.image_tables == len(self.tables)
                body = root.find(".//body")
                for tw in list(body.iter("table-wrap")):
                    tw.clear()
                self.text = text_of(body)
        if pmid:
            root = parse(fetch("pubmed", pmid))
            if root is not None:
                self.abstract = " ".join(text_of(a) for a in root.iter("AbstractText"))

    def full_text(self):
        return bool(self.tables and not self.images) or bool(self.text)

    def find(self, value, kind, level, sex, measure, partner):
        """(result, source, row, column, quote) for the first in-context match, exact before rounded. A cell that
        prints the value together with its partner (the mean for an SD, the SD for a mean) is preferred to one that
        prints the value alone."""
        for rounded_ok in (False, True):
            for want_pair in ((True, False) if partner else (False,)):
                for label, cells in self.tables:
                    for c in cells:
                        why, qualifier = table_context(c, level, sex, self.key, measure)
                        if why:
                            continue
                        for i, (printed, role) in enumerate(zip(c["nums"], c["roles"])):
                            if role not in (None, kind):
                                continue
                            hit = match(value, printed, rounded_ok)
                            if not hit:
                                continue
                            if want_pair:
                                j = i + 1 if kind == "mean" else i - 1
                                if not (0 <= j < len(c["nums"]) and match(partner, c["nums"][j], True)):
                                    continue
                            return (f"confirmed in a table ({hit}{qualifier}"
                                    + ("; with its " + ("SD" if kind == "mean" else "mean") if want_pair else "") + ")",
                                    label, c["label"][:60], c["header"][:60], c["cell"][:80])
            for name, text in (("running text", self.text), ("PubMed abstract", self.abstract)):
                if text:
                    clause = text_hits(text, value, kind, level, sex, rounded_ok)
                    if clause:
                        hit = "exact" if text_hits(text, value, kind, level, sex, False) else "rounded"
                        return f"confirmed in the {name} ({hit})", name, "", "", clause[:200]
        for label, cells in self.tables:
            for c in cells:
                if any(match(value, p, False) for p in c["nums"]):
                    why, _ = table_context(c, level, sex, self.key, measure)
                    return (f"found only out of context ({why or 'another role'})", label, c["label"][:60],
                            c["header"][:60], c["cell"][:80])
        if self.images:
            return "not checkable: the tables are images and the text does not print it", "", "", "", ""
        if self.image_tables:
            return f"not found in the text; {self.image_tables} of its tables are images", "", "", "", ""
        if self.full_text():
            return "not found in the full text", "", "", "", ""
        return "not checkable: only the abstract is open, and it does not print this value", "", "", "", ""


# --------------------------------------------------------------------------------------------- the run

def rows_of(name):
    lines = [l for l in (HERE / "data" / name).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def paper_for(row, name, mapping):
    for m in mapping:
        if m["file"] == name and m["series"] == row["series"] and (not m["citation_contains"] or m["citation_contains"] in row["citation"]):
            return m
    raise SystemExit(f"data/series_papers.csv has no line for {name} series {row['series']!r} ({row['citation']})")


def row_trace(means, papers):
    best, best_n, best_cells = "", 0, []
    for key, p in papers.items():
        for label, cells in p.tables:
            by_row = defaultdict(list)
            for c in cells:
                by_row[(c["label"], c["section"])] += c["nums"]
            for (row, section), nums in by_row.items():
                n = sum(1 for l in means if any(match(l["value"], x, False) for x in nums))
                if n > best_n:
                    best_n, best, best_cells = n, f"{key}: {label}, row '{row[:50]}'", nums
    return best, best_n, best_cells


def main(argv):
    sources = json.loads((HERE / "sources.json").read_text(encoding="ascii"))["papers"]
    mapping = list(csv.DictReader((HERE / "data" / "series_papers.csv").read_text(encoding="ascii").splitlines()))
    papers = {}
    for key, p in sources.items():
        pmcid = p.get("pmcid") if (p.get("full_text") or {}).get("pmc_full_text_xml") else None
        pmid = (p.get("pubmed") or {}).get("pmid")
        papers[key] = Paper(key, pmcid, pmid)
    print(f"full text read: {sum(1 for p in papers.values() if p.full_text())} of {len(papers)}; tables as text in "
          f"{sum(1 for p in papers.values() if p.tables and not p.images)}; tables as images in "
          f"{sum(1 for p in papers.values() if p.images)}; abstracts {sum(1 for p in papers.values() if p.abstract)}")

    out, groups = [], defaultdict(list)
    for name in ("level_references.csv", "pedicle_width_references.csv"):
        for row in rows_of(name):
            m = paper_for(row, name, mapping)
            own = m["read_from"] if m["read_from"] != "not recorded" else m["paper"]
            p = papers.get(own)
            for kind in ("mean", "sd"):
                value = (row.get(kind) or "").strip()
                if not value:
                    continue
                if p is None or not (p.full_text() or p.abstract or p.images):
                    found = ("not checkable: neither its full text nor its abstract is open", "", "", "", "")
                else:
                    partner = (row.get("sd" if kind == "mean" else "mean") or "").strip()
                    found = p.find(value, kind, row["level"], row.get("sex") or "all", row["measure"], partner)
                line = {"file": name, "series": row["series"], "measure": row["measure"], "level": row["level"],
                        "sex": row.get("sex") or "all", "kind": kind, "value": value, "paper": m["paper"],
                        "read_from": m["read_from"], "result": found[0], "source": found[1],
                        "row": ascii_text(found[2]), "column": ascii_text(found[3]), "quote": ascii_text(found[4])}
                out.append(line)
                groups[(name, row["series"], m["paper"], m["read_from"])].append(line)

    summary = []
    for (name, series, paper, read_from), lines in sorted(groups.items()):
        means = [l for l in lines if l["kind"] == "mean"]
        sds = [l for l in lines if l["kind"] == "sd"]
        conf = [l for l in lines if l["result"].startswith("confirmed")]
        conf_means = [l for l in means if l["result"].startswith("confirmed")]
        traced, tn, ts = "", "", ""
        if not conf_means and not all(significant(l["value"]) == 0 for l in means):
            best, best_n, cells = row_trace(means, papers)
            if best_n >= 3 and best_n >= 0.8 * len(means):
                traced, tn = best, f"{best_n}/{len(means)}"
                ts = f"{sum(1 for l in sds if any(match(l['value'], x, True) for x in cells))}/{len(sds)}" if sds else ""
        summary.append({
            "file": name, "series": series, "paper": paper, "read_from": read_from,
            "values": len(lines), "checkable": sum(1 for l in lines if not l["result"].startswith("not checkable")),
            "confirmed": len(conf), "means_confirmed": f"{len(conf_means)}/{len(means)}",
            "out_of_context": sum(1 for l in lines if l["result"].startswith("found only out of context")),
            "not_found_in_full_text": sum(1 for l in lines if l["result"] == "not found in the full text"),
            "where": "; ".join(sorted({l["source"] for l in conf})),
            "agrees_with_row": ascii_text(traced), "row_means": tn, "row_sds": ts,
        })

    OUTDIR.mkdir(exist_ok=True)
    for fname, rows in (("values.csv", out), ("series.csv", summary)):
        with (OUTDIR / fname).open("w", newline="", encoding="ascii") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    for s in summary:
        print(f"{s['series']:22s} {s['paper']:17s} checkable {s['checkable']:3d} confirmed {s['confirmed']:3d} "
              f"means {s['means_confirmed']:6s} ooc {s['out_of_context']:2d} nf {s['not_found_in_full_text']:2d} | "
              f"{s['where'][:40]} {('| row: ' + s['agrees_with_row'][:55] + ' ' + s['row_means'] + ' ' + s['row_sds']) if s['agrees_with_row'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
