"""The values here from ten closed-access papers against a blind reading of those papers' printed tables.

    python3 code/check_closed_reading.py            # from synthetic_spine/; standard library only, no network
    python3 code/check_closed_reading.py --check    # write nothing; exit 1 also when the committed result is stale

Seventy-eight values in data/level_references.csv and data/pedicle_width_references.csv come from ten papers that
have no open full text: verification/values.csv calls 52 of them not checkable and confirms the other 26 in an
abstract only. greg supplied the PDFs on 28 October 2026; they are not committed. verification/closed_page_reading.csv
is a transcription of their tables made from the page images by readers who were not shown any of the tables here,
as Panjabi's were read (code/check_page_reading.py): one row per printed cell and statistic, with the cell as printed
(printed_as) and where it is (table, pdf_page, journal_page). For the five typeset papers (Mitra 2002, Robertson
2000, Yu 2015, Tang 2016 and Bach 2019) every value read was also found on the publisher's own text layer.

SOURCES names, for each series, the cells of its own paper that its values should be, as the reading labels them. A
value agrees when its cell, rounded half up to the decimals the table records, equals it. FINDINGS says, for each
value that does not, what the paper prints instead, and where a calculation or another paper's table reproduces the
value, that calculation, which is then held to it like a cell. NOTES records what a reader of an agreeing value
should still know; Bach's are computed from the reading. SCALE turns a paper's printed unit into the data's: Tang
prints centimetres. The script writes verification/closed_page_reading_check.csv and exits 1 on a value that neither
agrees nor has a finding, on a finding whose calculation no longer reproduces its value, on a finding or a note for
a value that is not here, or on a selector that picks other than one cell.
"""
import csv
import io
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
READING = HERE / "verification" / "closed_page_reading.csv"
OUT = HERE / "verification" / "closed_page_reading_check.csv"
SEX = {"M": "male", "F": "female", "all": "all"}
LUMBAR = ("L1", "L2", "L3", "L4", "L5")
PEDICLES = "pedicle_width_references.csv"
LEVELS = "level_references.csv"

# (data file, series, measure) -> (paper, the reading's labels that pick the series' cells); labels None where the
# paper prints no cell the series could be. The sex is the value's own unless the labels name one.
SOURCES = {
    (PEDICLES, "Zindrick", "PDW"):
        ("zindrick1987", {"table": "Table 1", "measure_label": "Transverse Pedicle Isthmus Width"}),
    (PEDICLES, "Hou", "PDW"):
        ("hou1993", {"table": "Table 1", "group": "Current Study"}),
    (PEDICLES, "Olsewski", "PDW"):
        ("olsewski1990", {"table": "Table II", "group": "21 spines direct (Part 2)",
                          "column_label": "Transverse Diameter (mm) Direct"}),
    (PEDICLES, "Mitra", "PDW"):
        ("mitra2002", {"table": "Table 1", "measure_label": "TD", "group": "CS direct M(18)", "sex": "male"}),
    (PEDICLES, "Robertson", "PDW"):
        ("robertson2000", {"table": "Table 1", "measure_label": "Width", "side": "left"}),
    (PEDICLES, "Yu", "PDW"):
        ("yu2015", {"table": "Table 5", "measure_label": "PW", "group": "CS, American (N = 503)"}),
    (PEDICLES, "Krag", "PDW"):
        ("krag1988", None),
    (LEVELS, "Hinck 1966", "canal_w"):
        ("hinck1966", {"group": "Adult (>18 yr)"}),
    (LEVELS, "Tang 2016", "endplate"):
        ("tang2016", {"table": "Table 4", "measure_label": "FD_CaEP"}),
    (LEVELS, "Bach 2019", "disc"):
        ("bach2019", {"table": "Results (text)", "measure_label": "Average lumbar disc height"}),
}

# A paper that prints another unit than the data holds: the factor that turns its printed number into the data's.
# Tang prints centimetres; the data holds millimetres.
SCALE = {"tang2016": 10}


def in_data_units(paper, number):
    return Decimal(number) * SCALE.get(paper, 1)


def mitra_ct(level):
    """Mitra's CT transverse diameter over all 20 cadavers: the 18 men's and the 2 women's means, weighted."""
    cell = {"table": "Table 1", "measure_label": "TD"}
    return [("mitra2002", dict(cell, group="CS CT M(18)", sex="male"), level, 18),
            ("mitra2002", dict(cell, group="CS CT F(2)", sex="female"), level, 2)]


def yu_table5(group, level):
    """A row of Yu 2015's Table 5, which sets other studies' pedicle widths beside Yu's own."""
    return [("yu2015", {"table": "Table 5", "measure_label": "PW", "group": group, "sex": ""}, level, 1)]


def yu_age_midpoint(level):
    """The midpoint of two of Yu 2015's four age groups in Table 3: up to 30 years and 50 to 69 years."""
    cell = {"table": "Table 3", "measure_label": "PW"}
    return [("yu2015", dict(cell, group="Age <=30 yr"), level, 1),
            ("yu2015", dict(cell, group="Age 50-69 yr"), level, 1)]


KRAG = ("Krag prints no mean pedicle width: Table 2 (p. 30) counts pedicles in 1-mm bins, the top bin open from 9 to "
        "19.38 mm, the figures plot means with no printed values, and the text says about 7 mm from T9 to L1 and "
        "about 13 mm at L5 (12.6 mm by the 0 deg method). The five values are Yu 2015's Table 5 row for Krag et al "
        "(p. 1645), where the series was evidently read; how Yu came by them is not said")
MITRA = ("Table 1 (p. 455) prints {printed} for the 18 men measured directly. The value is the mean of the CT rows "
         "over all 20 cadavers, 18 men and 2 women weighted; L1 and L5 are the men's direct means, which the "
         "abstract quotes, so the series mixes two methods")
YU = ("Yu's own means, over 503 specimens with the two sides averaged, are printed 8.52, 8.66, 10.46, 13.19 and "
      "18.33 (Table 5, p. 1645; the abstract agrees, the text gives 8.53 at L1 and 18.34 at L5). The series' value "
      "is printed nowhere in the paper{extra}. It is the midpoint of Table 3's means for the youngest age group "
      "(30 years or less) and for 50 to 69 years (p. 1642), at all five levels. From L1 to L4 those two are the "
      "lowest and highest of the four age groups, which fits the table's citation, \"midpoint of published "
      "range\"; at L5 the oldest group's 19.15 is higher still, and the same two groups were taken there too")

# (series, measure, level, sex, kind) -> (what the paper prints instead, the cells that reproduce the value or None)
FINDINGS = {
    ("Krag", "PDW", "L1", "all", "mean"): (KRAG, yu_table5("Krag et al, American (N = 14-24)", "L1")),
    ("Krag", "PDW", "L2", "all", "mean"): (KRAG, yu_table5("Krag et al, American (N = 14-24)", "L2")),
    ("Krag", "PDW", "L3", "all", "mean"): (KRAG, yu_table5("Krag et al, American (N = 14-24)", "L3")),
    ("Krag", "PDW", "L4", "all", "mean"): (KRAG, yu_table5("Krag et al, American (N = 14-24)", "L4")),
    ("Krag", "PDW", "L5", "all", "mean"): (KRAG, yu_table5("Krag et al, American (N = 14-24)", "L5")),
    ("Mitra", "PDW", "L2", "all", "mean"): (MITRA.format(printed="7.85"), mitra_ct("L2")),
    ("Mitra", "PDW", "L3", "all", "mean"): (MITRA.format(printed="9.01"), mitra_ct("L3")),
    ("Mitra", "PDW", "L4", "all", "mean"): (MITRA.format(printed="11.6"), mitra_ct("L4")),
    ("Yu", "PDW", "L1", "all", "mean"): (YU.format(extra=""), yu_age_midpoint("L1")),
    ("Yu", "PDW", "L2", "all", "mean"): (YU.format(extra=""), yu_age_midpoint("L2")),
    ("Yu", "PDW", "L3", "all", "mean"): (YU.format(extra=" as Yu's own, though Table 4's mean for the Caucasian "
                                                     "specimens is also 10.43"), yu_age_midpoint("L3")),
    ("Yu", "PDW", "L4", "all", "mean"): (YU.format(extra=""), yu_age_midpoint("L4")),
    ("Yu", "PDW", "L5", "all", "mean"): (YU.format(extra=""), yu_age_midpoint("L5")),
}

ROBERTSON = ("the left side only, as Table 1 prints it (whether the reader's left or the specimen's is not said); "
             "Robertson's width is the full medial-to-lateral extent of the pedicle's coaxial radiographic image, "
             "and its isthmus diameter, the narrowest, is a separate row (left {isthmus} mm here)")

TANG = ("Tang prints centimetres and the data holds millimetres, so the cell is read times 10. FD_CaEP is the frontal "
        "diameter, the right-to-left extent, of the caudal end plate of the {disc} disc, which is {level}'s upper end "
        "plate. The data's n of 109 counts the study's subjects; this cell's N is {n}, since {men} men's discs of "
        "Pfirrmann grade V were left out with their end plates (p. 4117)")

BACH_DECADES = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh")
BACH_SEX = {"M": ("men", "Table 2"), "F": ("women", "Table 3")}


def hundredths(number):
    return format(number.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")


def bach_decades(reading, measure, level, sex):
    """Bach 2019's seven decade rows of one measure (Table 2 for men, Table 3 for women), each weighted by its
    decade's count of people in Table 1: the terms of the measure's mean over all ages."""
    count = {"table": "Table 1", "measure_label": "Patient volume"}
    return [("bach2019", {"table": BACH_SEX[sex][1], "measure_label": measure, "group": decade + " Decade"}, level,
             int(one_cell(reading, "bach2019", dict(count, group="Decade %d" % (10 * i)), "", sex, "n")["value"]))
            for i, decade in enumerate(BACH_DECADES, start=1)]


def pooled_sd(reading, terms, sex):
    """The SD over all the people of the groups the terms name, from each group's mean, SD and count."""
    mean, _ = reproduce(reading, terms, sex, "mean")
    total, people = Decimal(0), 0
    for paper, labels, level, n in terms:
        m = in_data_units(paper, one_cell(reading, paper, labels, level, sex, "mean")["value"])
        sd = in_data_units(paper, one_cell(reading, paper, labels, level, sex, "sd")["value"])
        total += (n - 1) * sd * sd + n * (m - mean) ** 2
        people += n
    return (total / (people - 1)).sqrt()


def bach_note(reading, level, sex, kind):
    """What the Results' average is, beside Table 6's, and what its unnamed +/- is, computed from the reading."""
    who, table = BACH_SEX[sex]
    three = bach_decades(reading, "Average disc height", level, sex)
    if kind == "mean":
        pooled, _ = reproduce(reading, three, sex, "mean")
        a, p, t6 = (Decimal(one_cell(reading, "bach2019", {"table": "Table 6", "measure_label": m + " disc height"},
                                     level, sex, "mean")["value"]) for m in ("Anterior", "Posterior", "Average"))
        said = ("Printed in the Results (p. e108) and the abstract (p. e106): the mean of the anterior, middle and "
                "posterior heights over all ages, which %s's decade rows of that mean, weighted by Table 1's counts, "
                "give as %s. Table 6's 'Average disc height' for all ages is another quantity, %s, the mean of its "
                "anterior and posterior rows alone, (%s + %s) / 2 = %s"
                % (table, hundredths(pooled), t6, a, p, format((a + p) / 2, "f")))
    else:
        said = ("The Results and the abstract do not say what this +/- is. %s's decade rows of the mean of three, pooled as SDs with their "
                "means and Table 1's counts, give %s: the size of an SD over all the %s, not of an SE, which would be "
                "about a tenth of it" % (table, hundredths(pooled_sd(reading, three, sex)), who))
    people = one_cell(reading, "bach2019", {"table": "Table 1", "group": "Total"}, "", sex, "n")["value"]
    return said + ". The n column's 240 counts both sexes; the %s are %s (Table 1)" % (who, people)


# (series, measure, level, sex, kind) -> what a reader of an agreeing value should still know, or how to compute it
# from the reading
NOTES = {
    ("Robertson", "PDW", level, "all", "mean"): ROBERTSON.format(isthmus=isthmus)
    for level, isthmus in zip(LUMBAR, ("9.9", "10.0", "12.3", "13.4", "13.2"))
}
NOTES.update({
    ("Tang 2016", "endplate", level, "all", kind): TANG.format(disc=disc, level=level, n=n, men=men)
    for level, disc, n, men in (("L4", "L3/L4", "107", "two"), ("L5", "L4/L5", "105", "four"))
    for kind in ("mean", "sd")
})
NOTES.update({
    ("Bach 2019", "disc", level, sex, kind): (lambda reading, level=level, sex=sex, kind=kind:
                                               bach_note(reading, level, sex, kind))
    for level in ("T12L1", "L1L2", "L2L3", "L3L4", "L4L5", "L5S1") for sex in ("M", "F") for kind in ("mean", "sd")
})


def rows_of(name):
    lines = [l for l in (DATA / name).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def decimals(text):
    return len(text.split(".")[1]) if "." in text else 0


def level_key(level):
    """L4-L5, L4/L5 and L4L5 name one disc."""
    return level.replace("-", "").replace("/", "").replace(" ", "")


def rounds_to(recorded, number):
    """A number agrees with a recorded value when, rounded half up to the recorded decimals, it equals it."""
    q = Decimal(1).scaleb(-decimals(recorded))
    return Decimal(number).quantize(q, rounding=ROUND_HALF_UP) == Decimal(recorded).quantize(q)


def values():
    """Every value of the series SOURCES names: (file, series, measure, level, sex, kind, value, the data row)."""
    out = []
    for name in (PEDICLES, LEVELS):
        for r in rows_of(name):
            if (name, r["series"], r["measure"]) in SOURCES:
                for kind in ("mean", "sd"):
                    if r[kind]:
                        out.append((name, r["series"], r["measure"], r["level"], r.get("sex", "all"), kind,
                                    r[kind], r))
    return out


def cells(reading, paper, labels, level, sex, kind):
    """The reading's cells at one level and statistic of one paper whose labels match; the sex is the value's own
    unless the labels name one."""
    want = dict(labels)
    want.setdefault("sex", SEX[sex])
    return [c for c in reading
            if c["paper"] == paper and level_key(c["level"]) == level_key(level) and c["statistic"] == kind
            and all(c[k] == v for k, v in want.items())]


def one_cell(reading, paper, labels, level, sex, kind):
    found = cells(reading, paper, labels, level, sex, kind)
    if len(found) != 1:
        raise LookupError("%s %s at %s %s %s picks %d cells" % (paper, labels, level, sex, kind, len(found)))
    return found[0]


def reproduce(reading, terms, sex, kind):
    """The weighted mean of the cells a finding names, and where they are."""
    total, weights, where = Decimal(0), 0, []
    for paper, labels, level, weight in terms:
        c = one_cell(reading, paper, labels, level, sex, kind)
        total += in_data_units(paper, c["value"]) * weight
        weights += weight
        where.append("%s %s p. %s %s %s" % (paper, c["table"], c["journal_page"], c["row_label"], c["printed_as"]))
    return total / weights, "; ".join(where)


def where_of(paper, c):
    page = " p. " + c["journal_page"] if c["journal_page"] else ""
    return "%s %s%s (pdf page %s), %s" % (paper, c["table"], page, c["pdf_page"], c["row_label"])


def judge(reading, value):
    """One output row for one value, and the problems it raises."""
    name, series, measure, level, sex, kind, recorded, data_row = value
    paper, labels = SOURCES[(name, series, measure)]
    key = (series, measure, level, sex, kind)
    finding, terms = FINDINGS.get(key, ("", None))
    note = NOTES.get(key, "")
    row = {"file": name, "series": series, "measure": measure, "level": level, "sex": sex, "kind": kind,
           "value": recorded, "paper": paper, "printed_as": "", "where": "", "legibility": "", "result": "",
           "sd_printed": "", "finding": finding, "reproduced_by": "",
           "note": note(reading) if callable(note) else note}
    problems = []
    found = [] if labels is None else cells(reading, paper, labels, level, sex, kind)
    if len(found) > 1:
        return row, ["%s: the selector picks %d cells" % (key, len(found))]
    if found:
        c = found[0]
        row.update(printed_as=c["printed_as"], legibility=c["legibility"], where=where_of(paper, c))
        row["result"] = "agrees" if rounds_to(recorded, in_data_units(paper, c["value"])) else "differs"
        if kind == "mean" and not data_row["sd"]:
            sd = cells(reading, paper, labels, level, sex, "sd")
            row["sd_printed"] = str(in_data_units(paper, sd[0]["value"])) if len(sd) == 1 else ""
    else:
        row["result"] = "not printed"
    if row["result"] == "agrees":
        if finding:
            problems.append("%s: agrees, yet FINDINGS explains a difference" % (key,))
    elif not finding:
        problems.append("%s: %s, and FINDINGS does not explain it" % (key, row["result"]))
    elif terms:
        number, where = reproduce(reading, terms, sex, kind)
        row["reproduced_by"] = "%s (%s)" % (format(number.normalize(), "f"), where)
        if not rounds_to(recorded, number):
            problems.append("%s: the finding's calculation gives %s, not %s" % (key, number, recorded))
    return row, problems


def main(argv):
    reading = list(csv.DictReader(READING.read_text(encoding="ascii").splitlines()))
    out, problems = [], []
    for value in values():
        row, found = judge(reading, value)
        out.append(row)
        problems += found
    here = {(o["series"], o["measure"], o["level"], o["sex"], o["kind"]) for o in out}
    problems += ["%s: a finding or note for a value not here" % (k,) for k in sorted((set(FINDINGS) | set(NOTES)) - here)]

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(out[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(out)
    if "--check" in argv:
        if not OUT.exists() or OUT.read_bytes() != buf.getvalue().encode("ascii"):
            problems.append("verification/closed_page_reading_check.csv is stale: rerun code/check_closed_reading.py")
    else:
        OUT.write_bytes(buf.getvalue().encode("ascii"))
    counts = {}
    for o in out:
        k = o["result"] + (", reproduced by a calculation or another table" if o["reproduced_by"] else
                           ", explained" if o["finding"] else "")
        counts[k] = counts.get(k, 0) + 1
    for k, v in sorted(counts.items()):
        print(f"{v:4d}  {k}")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
