"""The decisions on the copied tables that spine-program #239 left open, written as corrected tables beside the copies.

    python3 code/apply_decisions.py            # from synthetic_spine/; standard library only, no network
    python3 code/apply_decisions.py --check    # write nothing; exit 1 also when a written file is stale

Greg merged #239 on 28 October 2026 and, asked for his word on the decisions it left open, answered at 23:03 UTC: "yes
i merged it, but i want you to figure out those decisions". They are the questions of HANDOFF.md, "What needs a
person", items 3, 4 and 6, with the README's "What follows from the reading" and its "Discrepancies" 1 and 7; the
README's section "Decided" gives each decision and its reasons. data/level_references.csv and
data/pedicle_width_references.csv stay byte-for-byte copies of the public CTSpinoPelvic1K at e887274
(code/check_copies.py), which changes only on Greg's word, so the decisions are made here, as code: it writes the two
tables again under data/corrected/ with the decisions applied, and verification/decisions.csv, one line for each
field a decision changes in a series of one sex, its levels' values side by side.

Every number a decision writes comes from a page reading when the script runs and is never typed: the blind reading
of #239, verification/closed_page_reading.csv, or verification/open_questions_reading.csv, the cells behind the two
open data questions (Cizmic 2023's Table 5, Yadav 2020's Table 3), read for #240 from the publishers' text layers and
each set beside its page image. A value is its cell rounded half up to the decimals its series is written with for
that statistic, or to the cell's own where the series has no such value yet, and is written as the copy writes its
numbers: two decimals in the pedicle table, and in the level table the shortest decimal that is the number, as the
generator writes them. Mitra's means over all its cadavers and Cizmic's SD over both sexes are computed from the
cells their decisions name, and each calculation is first held to a number the paper or another paper prints. Typed,
and held by nothing, are the words of the cohort, modality, notes and citation columns and the pages of passages the
readings do not hold, which each decision names.

The script exits 1 when a copy is not the one the decisions were made on (its SHA-256 in DECIDED_ON), so that no
decision outlives the copy it corrects: a copy taken again after a change in CTSpinoPelvic1K stops the script until
each decision the change carries is taken out and the rest are checked against the new copy. It exits 1 too when a
selector picks other than the rows or the one cell it names, when a decision changes a field to what it holds or a
field another decision changed, when two rows of a corrected table share a key, when a copy written again with no
decision is not the copy byte for byte, when a calculation no longer gives the number it is held to, when a row of the
open questions' reading holds a value its printed_as does not print, and, with --check, when a written file is not
what the script writes.
"""
import csv
import hashlib
import io
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_closed_reading as closed  # noqa: E402

HERE = closed.HERE
DATA = closed.DATA
CORRECTED = DATA / "corrected"
RECORD = HERE / "verification" / "decisions.csv"
OPEN_READING = HERE / "verification" / "open_questions_reading.csv"
LEVELS, PEDICLES = closed.LEVELS, closed.PEDICLES
LUMBAR = closed.LUMBAR
one_cell, require, Untrue = closed.one_cell, closed.require, closed.Untrue

# The SHA-256 of each copy the decisions were made on, as data/COPIED_FROM.csv records them at e887274
DECIDED_ON = {
    LEVELS: "09c58677645cf130a1a205455320b8fd65bfa50ae1b15f63a4ea686b916a74f1",
    PEDICLES: "8a18084cb49db91c5b9f2247f9a547a6a8cdc72bd023fb8ea450789fdadb3ef5",
}

# A row's key; the pedicle table has no sex column
KEYS = {LEVELS: ("series", "measure", "level", "sex"), PEDICLES: ("series", "measure", "level")}
RECORD_FIELDS = ("decision", "file", "series", "measure", "levels", "sex", "field", "was", "now", "source", "why")
SEXES = {"M": "male", "F": "female"}


class Refused(Exception):
    """A decision that no longer fits the copy or the reading it was made on."""


class Table:
    """A copied table as rows that keep the copy's text, with its header and comment lines."""

    def __init__(self, name):
        self.name = name
        raw = (DATA / name).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != DECIDED_ON[name]:
            raise Refused("data/%s is not the copy the decisions were made on (sha256 %s, not %s): take out each "
                          "decision the new copy carries and check the rest against it" % (name, digest,
                                                                                         DECIDED_ON[name]))
        lines = raw.decode("ascii").splitlines(keepends=True)
        end = 1
        while end < len(lines) and lines[end].startswith("#"):
            end += 1
        self.header, self.comments = lines[0], lines[1:end]
        if any(line.startswith("#") for line in lines[end:]):
            raise Refused("data/%s has comment lines among its rows" % name)
        self.fields = next(csv.reader([self.header]))
        self.rows = [dict(zip(self.fields, r)) for r in csv.reader(lines[end:])]
        if self.text() != raw.decode("ascii"):
            raise Refused("data/%s is not written again byte for byte" % name)

    def text(self):
        buf = io.StringIO()
        buf.write(self.header)
        buf.writelines(self.comments)
        csv.writer(buf, lineterminator="\n").writerows([r[f] for f in self.fields] for r in self.rows)
        return buf.getvalue()

    def key(self, row):
        return tuple(row.get(k, "all") for k in KEYS[self.name])

    def pick(self, count, **where):
        """The rows whose columns hold the values given, which must be count of them, in the table's order."""
        found = [r for r in self.rows if all(r.get(k, "all") == v for k, v in where.items())]
        if len(found) != count:
            raise Refused("data/%s: %s picks %d rows, not %d" % (self.name, where, len(found), count))
        return found

    def places(self, series, measure, kind):
        """The most decimals a series is written with for one statistic, None where it has no such value."""
        found = [closed.decimals(r[kind]) for r in self.rows
                 if r["series"] == series and r["measure"] == measure and r[kind]]
        return max(found) if found else None

    def written(self, number, places):
        """A number rounded half up to places and written as this table writes its numbers."""
        rounded = Decimal(number).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
        if self.name == PEDICLES:
            return str(rounded.quantize(Decimal("0.01")))
        return str(int(rounded)) if places == 0 else repr(float(rounded))


def where_of(c):
    """Where a cell is, in the record's words."""
    page = " p. %s" % c["journal_page"] if c["journal_page"] else ""
    return "%s %s%s, %s: %s" % (c["paper"], c["table"], page, c["row_label"], c["printed_as"])


class Decisions:
    """The corrected tables, and the record of what each decision changed in them."""

    def __init__(self, reading):
        self.reading = reading
        self.tables = {name: Table(name) for name in (LEVELS, PEDICLES)}
        self.changed = {}
        self.record = []

    def rows(self, name, count, **where):
        return self.tables[name].pick(count, **where)

    def cell(self, paper, labels, level, sex, kind):
        return one_cell(self.reading, paper, labels, level, sex, kind)

    def note(self, decision, name, row, field, was, now, source, why):
        self.record.append(dict(decision=decision, file=name, series=row["series"], measure=row["measure"],
                                level=row["level"], sex=row.get("sex", "all"), field=field, was=was, now=now,
                                source=source, why=why))

    def put(self, decision, name, row, field, now, source, why):
        """Set one field of one row; a change to what it holds, or to a field another decision set, is refused."""
        at = (name, self.tables[name].key(row), field)
        if row[field] == now:
            raise Refused("decision %s: %s already holds %r" % (decision, at, now))
        if at in self.changed:
            raise Refused("decision %s: %s was set by decision %s" % (decision, at, self.changed[at]))
        self.changed[at] = decision
        self.note(decision, name, row, field, row[field], now, source, why)
        row[field] = now

    def put_all(self, decision, name, rows, field, now, source, why):
        for row in rows:
            self.put(decision, name, row, field, now, source, why)

    def value(self, name, series, measure, kind, number, places=None):
        """A number as the table writes the series' values of one statistic."""
        table = self.tables[name]
        found = table.places(series, measure, kind)
        return table.written(number, places if found is None else found)

    def put_cell(self, decision, name, row, kind, c, why):
        """Set a mean or an SD from one cell, to the series' decimals, or the cell's own where it has none."""
        number = closed.in_data_units(c["paper"], c["value"])
        now = self.value(name, row["series"], row["measure"], kind, number, closed.decimals(c["value"]))
        self.put(decision, name, row, kind, now, where_of(c), why)

    def add(self, decision, name, like, changes, why):
        """A new row, the row like with changes, after the last row of its series and measure, else of its measure;
        changes holds a field's value, or (value, source) where a cell gives it."""
        table = self.tables[name]
        row = dict(like, **{f: v[0] if isinstance(v, tuple) else v for f, v in changes.items()})
        if table.key(row) in {table.key(r) for r in table.rows}:
            raise Refused("decision %s: %s is a row of %s already" % (decision, table.key(row), name))
        same = [i for i, r in enumerate(table.rows) if r["measure"] == row["measure"]]
        ours = [i for i in same if table.rows[i]["series"] == row["series"]]
        table.rows.insert((ours or same)[-1] + 1, row)
        for field, v in changes.items():
            source = v[1] if isinstance(v, tuple) else "the %s %s row at %s" % (like["series"], like.get("sex", ""),
                                                                                  like["level"])
            self.changed[(name, table.key(row), field)] = decision
            self.note(decision, name, row, field, "", row[field], source, why)
        return row

    def comment(self, decision, name, old, new, why):
        """Replace words of a table's comment header."""
        table = self.tables[name]
        found = [i for i, line in enumerate(table.comments) if old in line]
        if len(found) != 1:
            raise Refused("decision %s: %r is in %d comment lines of %s, not one" % (decision, old, len(found), name))
        table.comments[found[0]] = table.comments[found[0]].replace(old, new)
        self.record.append(dict(decision=decision, file=name, series="", measure="", level="", sex="",
                                field="header", was=old, now=new, source="the header's comment lines", why=why))


PRIMARY = ("every value is a cell of the paper's own table, read from the page (#239), so the series is primary and "
           "cites that table and page")


def on_the_page(d, name, rows):
    """Each mean and SD of rows held to the one cell of the paper's own table that closed.SOURCES names for it."""
    for row in rows:
        paper, labels = closed.SOURCES[(name, row["series"], row["measure"])]
        for kind in ("mean", "sd"):
            if not row[kind]:
                continue
            c = d.cell(paper, labels, row["level"], row.get("sex", "all"), kind)
            require(closed.rounds_to(row[kind], closed.in_data_units(paper, c["value"])),
                    "%s's %s at %s is %s, not its own table's %s" % (row["series"], kind, row["level"], row[kind],
                                                                    c["printed_as"]))


def own_paper(d, decision, name, rows, where, citation, why=None):
    """A series read from its own paper's table: primary, and its citation naming that table and page. Each of its
    values is first held to its cell, unless a why says how a decision computed them from cells instead."""
    if why is None:
        on_the_page(d, name, rows)
    d.put_all(decision, name, rows, "source_kind", "primary", where, why or PRIMARY)
    d.put_all(decision, name, rows, "citation", citation, where, why or PRIMARY)


def sds_beside(d, decision, rows, paper, labels, why):
    """The SDs a pedicle series' own table prints beside its means, which the copy leaves out."""
    for row in rows:
        d.put_cell(decision, PEDICLES, row, "sd", d.cell(paper, labels, row["level"], "all", "sd"), why)
    d.put_all(decision, PEDICLES, rows, "dispersion", "SD", "%s %s" % (paper, labels["table"]), why)


# Decision 1: the four pedicle rows whose cohort columns the reading found wrong

OLSEWSKI = closed.SOURCES[(PEDICLES, "Olsewski", "PDW")][1]
ROBERTSON = closed.SOURCES[(PEDICLES, "Robertson", "PDW")][1]
ZINDRICK = closed.SOURCES[(PEDICLES, "Zindrick", "PDW")][1]
HOU = closed.SOURCES[(PEDICLES, "Hou", "PDW")][1]
YU = closed.SOURCES[(PEDICLES, "Yu", "PDW")][1]


def olsewski(d):
    rows = d.rows(PEDICLES, 5, series="Olsewski")
    where = "olsewski1990 Table II p. 544, %s; 12 men and 9 women, p. 543 (typed)" % OLSEWSKI["group"]
    d.put_all(1, PEDICLES, rows, "cohort", "cadaveric embalmed, 12 men and 9 women", where,
              "the values are of 21 cadaver spines measured directly; 'cadaveric + patients' added in the paper's "
              "49 cadavers (p. 542) and 51 patients (p. 543), whose values are not these")
    own_paper(d, 1, PEDICLES, rows, where, "Olsewski JM et al. J Bone Joint Surg Am 1990;72(4):541-549 (Table II, "
                                           "measured directly, sexes combined, p. 544)")


def robertson(d):
    rows = d.rows(PEDICLES, 5, series="Robertson")
    where = "robertson2000 Table 1 p. 711, left Width; the specimens and the method, pp. 709-710 (typed)"
    d.put_all(1, PEDICLES, rows, "cohort", "cadaveric dry bone, origin not given", where,
              "10 dry-bone lumbosacral spines, not CT patients; the paper gives no origin, sex or age, and New "
              "Zealand is only where its authors worked (Auckland Hospital, p. 709)")
    d.put_all(1, PEDICLES, rows, "modality", "radiograph, coaxial, wire-marked", where,
              "each pedicle wrapped in wire, radiographed coaxially and corrected for magnification (pp. 709-710); "
              "the width is of the outer cortex")
    own_paper(d, 1, PEDICLES, rows, where, "Robertson PA & Stewart NR. Spine 2000;25(6):709-715 (Table 1, left "
                                           "Width, p. 711; whose left is not stated)")


def zindrick(d):
    rows = d.rows(PEDICLES, 5, series="Zindrick")
    where = "zindrick1987 Table 1 p. 161, %s" % ZINDRICK["measure_label"]
    d.put_all(1, PEDICLES, rows, "modality", "radiograph + CT", where,
              "measured on radiographs of the disarticulated specimens and on CT, not by caliper; Table 1's N counts "
              "these studies")
    own_paper(d, 1, PEDICLES, rows, where, "Zindrick MR et al. Spine 1987;12(2):160-166 (Table 1, p. 161)")


def krag(d):
    rows = d.rows(PEDICLES, 5, series="Krag")
    d.put_all(1, PEDICLES, rows, "cohort", "patients, 27 men and 14 women", "krag1988 p. 27 (typed)",
              "CT of 91 vertebrae of 41 living patients; the 8 sectioned cadaver vertebrae only checked the method "
              "(pp. 27-28)")
    where = "yu2015 Table 5 p. 1645, %s" % closed.KRAG_IN_YU
    d.put_all(1, PEDICLES, rows, "citation",
              "Krag MH et al. Spine 1988;13(1):27-32, via Yu CC et al. Spine 2015;40(21):1639-1646 (Table 5, p. "
              "1645; Krag prints no table of mean widths, and its text gives about 7 mm from T9 to L1 and about 13 mm "
              "at L5, 12.6 by its 0 deg method, pp. 29-30)", where,
              "the five are Yu's Table 5 row under Krag's name, the only cells read that print them, and a secondary "
              "row names the paper it was read from; they stay, secondary, until Krag's Figure 5 is read")


def pedicle_header(d):
    d.comment(1, PEDICLES, "(the Chinese, Indian and Saudi series sit low, the New Zealand series high)",
              "(the Chinese, Indian and Saudi series sit low, Robertson's ten dry spines of no stated origin high)",
              "Robertson's specimens are of no stated population; New Zealand is where its authors worked")
    d.comment(1, PEDICLES, "WHY THIS FILE HAS TWELVE SERIES", "WHY THIS FILE HAS THIRTEEN SERIES",
              "the table has thirteen series (README, discrepancy 8)")


# Decision 2: n is the count of the people, or specimens, a row's values are of, as the paper prints it; where the
# paper counts only something else, that count with its unit named; at each level where it counts by level; and a
# dash where it prints none.

def count_cell(d, key, level, sex):
    paper, labels, at = closed.COUNTS[key]
    return d.cell(paper, labels, level if at is None else at, sex, "n")


def n_from_counts(d, name, series, measure, rows):
    """n from the cell closed.COUNTS names, the people of the row's own sex."""
    for row in rows:
        c = count_cell(d, (name, series, measure), row["level"], row.get("sex", "all"))
        d.put(2, name, row, "n", c["value"], where_of(c),
              "the people of the row's own sex the paper counts, where the copy gave both sexes' total")


def n_by_level(d, name, rows, paper, labels, unit, why):
    for row in rows:
        c = d.cell(paper, labels, row["level"], "all", "n")
        d.put(2, name, row, "n", (c["value"] + " " + unit).strip(), where_of(c), why)


TWOMEY_YOUNG = (("20-36", "M"), ("18-35", "F"))
YADAV_DISC = {"T12L1": "D12", "L1L2": "L1", "L2L3": "L2", "L3L4": "L3", "L4L5": "L4", "L5S1": "L5"}
YADAV_IVD = {"table": "Table 3", "measure_label": "IVD Height (mm)"}


def counts(d):
    for series, measure in (("Bach 2019", "disc"), ("Griffith 2016", "canal_w"), ("Griffith 2016", "canal_ap"),
                            ("Alonge 2021", "canal_w"), ("Alonge 2021", "canal_ap"), ("Ahmed 2019", "canal_w"),
                            ("Ahmed 2019", "canal_ap"), ("Chaudhary 2015", "canal_w")):
        rows = [r for r in d.tables[LEVELS].rows if r["series"] == series and r["measure"] == measure]
        n_from_counts(d, LEVELS, series, measure, rows)
    tang = d.rows(LEVELS, 2, series="Tang 2016", measure="endplate")
    n_from_counts(d, LEVELS, "Tang 2016", "endplate", tang)
    n_by_level(d, LEVELS, d.rows(LEVELS, 5, series="Hinck 1966"), "hinck1966",
               {"group": "Adult (>18 yr)", "table": "Table II"}, "films",
               "Table II's sample size at each level counts the films on which that vertebra was measured; how many "
               "people the films are of is not on the pages read")
    yadav = d.rows(LEVELS, 12, series="Yadav 2020", measure="disc")
    for row in yadav:
        c = d.cell("yadav2020", dict(YADAV_IVD, column_label="n"), YADAV_DISC[row["level"]], row["sex"], "n")
        d.put(2, LEVELS, row, "n", c["value"], where_of(c), "the people of the row's own sex Table 3 counts")
    for measure in ("endplate", "canal_ap"):
        for row in d.rows(LEVELS, 12, series="Yadav 2020", measure=measure):
            c = d.cell("yadav2020", dict(YADAV_IVD, column_label="n"), "L1", row["sex"], "n")
            d.put(2, LEVELS, row, "n", c["value"], where_of(c),
                  "the people of the row's own sex Table 3 counts at every level (Table 2 and Table 3 count the same "
                  "174 men and 128 women)")
    twomey(d)
    pedicle_counts(d)


def twomey(d):
    men, women = (d.cell("twomey1985", dict(closed.TWOMEY_COUNT, group=g), "", sex, "n") for g, sex in TWOMEY_YOUNG)
    require(not [c for c in d.reading if c["paper"] == "twomey1985" and c["table"] == closed.TWOMEY["table"]
                 and c["statistic"] == "n"], "Twomey's Table 2 prints an n")
    rows = d.rows(LEVELS, 10, series="Twomey 1985")
    d.put_all(2, LEVELS, rows, "n", "-", "twomey1985 Table 2 p. 497: no n",
              "Table 2 prints no n for the group it heads 20-35; the copy's 204 counts every cadaver of every age")
    for row in rows:
        young = men if row["sex"] == "M" else women
        d.put(2, LEVELS, row, "notes", "%s; n not printed, and Table 1's nearest group is %s %s aged %s (p. %s)" % (
            row["notes"], young["value"], "men" if row["sex"] == "M" else "women", young["group"],
            young["journal_page"]), where_of(young), "the count nearest the row, which n does not claim")


def pedicle_counts(d):
    olsewski = d.rows(PEDICLES, 5, series="Olsewski")
    spines = int(OLSEWSKI["group"].split()[0])
    d.put_all(2, PEDICLES, olsewski, "n", str(spines), "olsewski1990 Table II p. 544, group %s" % OLSEWSKI["group"],
              "the 21 spines the values are of; Table II's 41 or 42 count their pedicles, both of each spine but one "
              "at L1, and 100 was the copy's sum of the paper's other parts")
    d.put_all(2, PEDICLES, d.rows(PEDICLES, 5, series="Robertson"), "n", "10", "robertson2000 p. 709 (typed)",
              "10 specimens; 100 is their lumbar pedicles, both sides of five levels, and the series is the left side")
    n_by_level(d, PEDICLES, d.rows(PEDICLES, 5, series="Zindrick"), "zindrick1987", dict(ZINDRICK, column_label="N"),
               "studies", "Table 1 counts studies, radiographs and CT scans, at each level, and no people")
    n_by_level(d, PEDICLES, d.rows(PEDICLES, 5, series="Krag"), "krag1988",
               {"table": "Table 2", "column_label": "# of Pedicle"}, "pedicles",
               "Krag's Table 2 counts the pedicles measured at each level, 14 to 24, the N Yu's Table 5 prints beside "
               "these values")


# Decision 3: Yu's own means, and Mitra's by one method over all its cadavers

def yu(d):
    rows = d.rows(PEDICLES, 5, series="Yu")
    for row in rows:
        d.put_cell(3, PEDICLES, row, "mean", d.cell("yu2015", YU, row["level"], "all", "mean"),
                   "Yu's own means over its 503 specimens, where the copy held midpoints of two age groups' means")
    where = "yu2015 Table 5 p. 1645, %s; the specimens, pp. 1639-1640 (typed)" % YU["group"]
    d.put_all(3, PEDICLES, rows, "cohort", "dry skeletons, Hamann-Todd collection, 404 male and 99 female", where,
              "the specimens Yu measured")
    own_paper(d, 3, PEDICLES, rows, where, "Yu CC et al. Spine 2015;40(21):1639-1646 (Table 5, current study, "
                                           "both sides averaged, p. 1645)")


def mitra(d):
    rows = d.rows(PEDICLES, 5, series="Mitra")
    for row in rows:
        mean, where = closed.reproduce(d.reading, closed.mitra_direct(row["level"]), "all", "mean")
        yu_cell = one_cell(d.reading, *closed.yu_table5(closed.MITRA_IN_YU, row["level"])[0][:3], "all", "mean")
        now = d.value(PEDICLES, "Mitra", "PDW", "mean", mean)
        require(Decimal(now) == Decimal(yu_cell["value"]),
                "Mitra's direct mean over all 20 at %s is %s, not Yu's copy of it, %s" % (row["level"], now,
                                                                                          yu_cell["value"]))
        why = ("one method, measured directly, over all 20 cadavers: Table 1's men's and women's means weighted by "
               "the 18 and 2 their labels count, as Yu's Table 5 prints them (%s)" % where_of(yu_cell))
        if row["mean"] != now:
            d.put(3, PEDICLES, row, "mean", now, where, why)
    where = "mitra2002 Table 1 p. 455, CS direct M(18) and F(2)"
    d.put_all(3, PEDICLES, rows, "cohort", "cadaveric Indian, 18 men and 2 women", where, "the cadavers Mitra measured")
    own_paper(d, 3, PEDICLES, rows, where, "Mitra SR et al. Spine 2002;27(5):453-459 (Table 1, measured directly, "
                                           "the men's and women's means weighted by their 18 and 2, p. 455)",
              "every value is computed from cells of the paper's own table, read from the page (#239), and is the "
              "value Yu's Table 5 prints for Mitra, so the series is primary and cites that table and page")


# Decision 4: what the read papers print beside the tables' rows, of the same people, measure and method

AHMED_W = closed.SOURCES[(LEVELS, "Ahmed 2019", "canal_w")][1]
AHMED_AP = closed.SOURCES[(LEVELS, "Ahmed 2019", "canal_ap")][1]
CHAUDHARY = closed.SOURCES[(LEVELS, "Chaudhary 2015", "canal_w")][1]


def women_of(d, series, measure, paper, labels, count):
    """The women's rows a paper prints beside its men's, with their own means, SDs and count."""
    men = d.rows(LEVELS, 5, series=series, measure=measure, sex="M")
    why = "the paper prints its women's means and SDs beside the men's the table holds"
    for like in men:
        mean, sd = (d.cell(paper, labels, like["level"], "F", kind) for kind in ("mean", "sd"))
        changes = {"sex": "F", "n": (count["value"], where_of(count))}
        for kind, c in (("mean", mean), ("sd", sd)):
            number = closed.in_data_units(paper, c["value"])
            changes[kind] = (d.value(LEVELS, series, measure, kind, number), where_of(c))
        d.add(4, LEVELS, like, changes, why)


def women(d):
    for measure, labels in (("canal_w", AHMED_W), ("canal_ap", AHMED_AP)):
        women_of(d, "Ahmed 2019", measure, "ahmed2019", labels, d.cell("ahmed2019", closed.METHODS, "", "F", "n"))
    women_of(d, "Chaudhary 2015", "canal_w", "chaudhary2015", CHAUDHARY,
             d.cell("chaudhary2015", closed.METHODS, "", "F", "n"))
    women_of(d, "Alonge 2021", "canal_ap", "alonge2021", closed.ALONGE_AP,
             d.cell("alonge2021", closed.ALONGE_AP, "L1", "F", "n"))


def pedicle_sds(d):
    sds_beside(d, 4, d.rows(PEDICLES, 5, series="Olsewski"), "olsewski1990", OLSEWSKI,
               "Table II prints an SD beside each mean")
    sds_beside(d, 4, d.rows(PEDICLES, 5, series="Robertson"), "robertson2000", ROBERTSON,
               "Table 1 prints the left side's SD beside each mean")
    hou = d.rows(PEDICLES, 5, series="Hou")
    sds_beside(d, 4, hou, "hou1993", HOU, "Table 1 prints both sexes' SD beside each mean")
    own_paper(d, 4, PEDICLES, hou, "hou1993 Table 1 p. 1852, Cumulative",
              "Hou S et al. Spine 1993;18(13):1850-1855 (Table 1, both sexes, p. 1852)")


# Decision 5: Eisenstein's five from his own Table I, of the Caucasoid men; and Hinck's from Hinck's own tables

EISENSTEIN = closed.SOURCES[(LEVELS, "Eisenstein 1977", "canal_w")][1]
EISENSTEIN_CITATION = "Eisenstein S. J Bone Joint Surg Br 1977;59-B(2):173-180"


def eisenstein(d):
    rows = d.rows(LEVELS, 5, series="Eisenstein 1977")
    men = closed.eisenstein_count(d.reading, "Methods (text)", "Skeletons", EISENSTEIN["group"], "M")
    each, total, _ = closed.eisenstein_skeletons(d.reading)
    missing, _ = closed.eisenstein_vertebrae(d.reading, closed.number_of(total))
    where = "eisenstein1977 Table I p. 174, %s men, %s" % (EISENSTEIN["group"], EISENSTEIN["measure_label"])
    d.put_all(5, LEVELS, rows, "cohort", "Caucasoid men, Raymond Dart Collection", where,
              "the five are the Caucasoid men's alone; the copy named both groups Chaudhary's Table II copies")
    d.put_all(5, LEVELS, rows, "n", men["value"], where_of(men),
              "the Caucasoid men's skeletons, the people the five are of (decision 2's rule); not a count of "
              "vertebrae at any level, which the pages read do not give")
    skeletons = closed.number_of(total)
    d.put_all(5, LEVELS, rows, "notes", "whole mm; %s of the %s lumbar vertebrae of all %d skeletons missing or "
                                        "damaged, at levels and in groups not given (p. %s), so n may be fewer at a "
                                        "level" % (missing["value"], format(5 * skeletons, ","), skeletons,
                                                   missing["journal_page"]),
              where_of(missing), "why n is an upper bound at each level")
    own_paper(d, 5, LEVELS, rows, where, "%s (Table I, Caucasoid men, canal I.P., p. 174; whole mm)" %
              EISENSTEIN_CITATION)
    return each


def hinck(d):
    rows = d.rows(LEVELS, 5, series="Hinck 1966")
    where = "hinck1966 Tables IA and II, adults over 18, pp. 142 and 145"
    d.put_all(5, LEVELS, rows, "modality", "AP radiograph, uncorrected", where,
              "measured with calipers on 40-inch films with no correction for magnification described (p. 141), "
              "as Chaudhary's row says of its own")
    d.put_all(5, LEVELS, rows, "cohort", "adults radiographed for other reasons, white, Oregon", where,
              "Hinck's own people (pp. 141-142, typed), where the copy described them through Ahn 2001")
    own_paper(d, 5, LEVELS, rows, where, "Hinck VC et al. Am J Roentgenol Radium Ther Nucl Med 1966;97(1):141-153 "
                                         "(Tables IA and II, adults over 18, pp. 142 and 145)")


# Decision 6: Cizmic 2023's five canal-depth SDs, printed nowhere, become the SD over both sexes of Table 5

CIZMIC = {"table": "Table 5"}
CIZMIC_DEPTH, CIZMIC_WIDTH = "MSGD", "IPD"


def cizmic_groups(d, measure, level):
    """Table 5's two sexes at one level and measure, as (n, mean, sd), and where they are."""
    label = dict(CIZMIC, row_label="%s %s canal" % (level, measure))
    groups, where = [], []
    for sex in SEXES:
        cells = [d.cell("cizmic2023", label, level, sex, kind) for kind in ("n", "mean", "sd")]
        groups.append(tuple(Decimal(c["value"]) for c in cells))
        where.append("%s %s: %s, %s, %s" % (label["row_label"], SEXES[sex], *(c["printed_as"] for c in cells)))
    return groups, "cizmic2023 Table 5 p. %s, %s" % (cells[0]["journal_page"], "; ".join(where))


def combined_sd(groups):
    """The SD of a sample made of groups, each (n, mean, sd), from the groups alone."""
    n = sum(g[0] for g in groups)
    mean = sum(g[0] * g[1] for g in groups) / n
    squares = sum((g[0] - 1) * g[2] ** 2 + g[0] * (g[1] - mean) ** 2 for g in groups)
    return (squares / (n - 1)).sqrt()


def cizmic(d):
    for row in d.rows(LEVELS, 5, series="Cizmic 2023", measure="canal_w"):
        printed = Decimal(row["sd"])
        width, _ = cizmic_groups(d, CIZMIC_WIDTH, row["level"])
        require(abs(combined_sd(width) - printed) < Decimal("0.01"),
                "the SD over both sexes of Table 5's widths at %s is not the %s the text prints" % (row["level"],
                                                                                                   printed))
    for row in d.rows(LEVELS, 5, series="Cizmic 2023", measure="canal_ap"):
        depth, where = cizmic_groups(d, CIZMIC_DEPTH, row["level"])
        now = d.value(LEVELS, "Cizmic 2023", "canal_ap", "sd", combined_sd(depth))
        d.put(6, LEVELS, row, "sd", now, where,
              "the paper prints no SD of the depth over both sexes, and the copy's came from no page; this is "
              "Table 5's two sexes combined, the calculation that gives the paper's printed width SDs to within 0.01")
        d.put(6, LEVELS, row, "notes", row["notes"] + "; SD over both sexes from Table 5 (p. 202)", where,
              "the SD is computed, not printed")


# Decision 7: Yadav 2020's women's L3-L4 SD of 6.87 is what the paper prints, and stays

def yadav(d):
    row = d.rows(LEVELS, 1, series="Yadav 2020", measure="disc", level="L3L4", sex="F")[0]
    c = d.cell("yadav2020", YADAV_IVD, YADAV_DISC["L3L4"], "F", "sd")
    require(Decimal(c["value"]) == Decimal(row["sd"]), "Yadav's Table 3 does not print the copy's 6.87")
    others = [Decimal(d.cell("yadav2020", YADAV_IVD, YADAV_DISC[lv], "F", "sd")["value"])
              for lv in ("L2L3", "L4L5")]
    require(Decimal(c["value"]) > 4 * max(others), "Yadav's 6.87 is not four times its neighbours")
    d.put(7, LEVELS, row, "notes", "SD printed so in Table 3 (p. %s), %s times its neighbours (%s, %s); likely a "
                                   "misprint, kept as printed" % (c["journal_page"],
                                                                  (Decimal(c["value"]) / max(others)).quantize(
                                                                      Decimal("0.1")), *others),
          where_of(c), "the paper prints it; a misprint the paper does not correct is kept, as Chaudhary's SDs are")


DECIDE = (olsewski, robertson, zindrick, krag, pedicle_header, counts, yu, mitra, women, pedicle_sds, eisenstein,
          hinck, cizmic, yadav)


def grouped(record):
    """The record's lines, one for each field of a series of one sex that a decision changed, levels side by side."""
    out, at = [], {}
    for r in record:
        key = (r["decision"], r["file"], r["series"], r["measure"], r["sex"], r["field"])
        if key not in at:
            at[key] = dict(r, levels=[], was=[], now=[], source=[], why=r["why"])
            out.append(at[key])
        g = at[key]
        for f, v in (("levels", r["level"]), ("was", r["was"]), ("now", r["now"]), ("source", r["source"])):
            g[f].append(v)
    for g in out:
        for f in ("was", "now", "source"):
            g[f] = g[f][0] if len(set(g[f])) == 1 else " | ".join(g[f])
        g["levels"] = " ".join(g["levels"]).strip()
    return [{f: g[f] for f in RECORD_FIELDS} for g in out]


def reading_rows(path):
    return list(csv.DictReader(path.read_text(encoding="ascii").splitlines()))


def outputs(d):
    """Each file the script writes, and its text."""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=RECORD_FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(grouped(d.record))
    files = {CORRECTED / name: d.tables[name].text() for name in (LEVELS, PEDICLES)}
    files[RECORD] = buf.getvalue()
    return files


def collisions(d):
    found = []
    for name, table in d.tables.items():
        keys = [table.key(r) for r in table.rows]
        found += ["data/corrected/%s: %s is the key of %d rows" % (name, k, keys.count(k))
                  for k in sorted(set(keys)) if keys.count(k) > 1]
    return found


def main(argv):
    open_reading = reading_rows(OPEN_READING)
    problems = closed.unprinted(open_reading)
    try:
        d = Decisions(reading_rows(closed.READING) + open_reading)
        for decide in DECIDE:
            decide(d)
    except (Refused, Untrue, LookupError) as error:
        for p in problems + [str(error)]:
            print("  " + p)
        return 1
    problems += collisions(d)
    for path, text in outputs(d).items():
        if "--check" in argv:
            if not path.exists() or path.read_bytes() != text.encode("ascii"):
                problems.append("%s is stale: rerun code/apply_decisions.py" % path.relative_to(HERE))
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(text.encode("ascii"))
    by_decision = {}
    for r in d.record:
        by_decision[r["decision"]] = by_decision.get(r["decision"], 0) + 1
    for decision, count in sorted(by_decision.items()):
        print("%4d  fields set by decision %d" % (count, decision))
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
