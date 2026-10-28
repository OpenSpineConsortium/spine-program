"""The values here from sixteen closed papers against a blind reading of those papers' printed tables.

    python3 code/check_closed_reading.py            # from synthetic_spine/; standard library only, no network
    python3 code/check_closed_reading.py --check    # write nothing; exit 1 also when the committed result is stale

A closed paper, here, is one whose full text no script of this folder may read; sources.csv counts 29 of the 42. 203
values in data/level_references.csv and data/pedicle_width_references.csv come from sixteen of them, and all sixteen
were read from the page. verification/values.csv could check only 26 of the 203, in an abstract. Greg supplied eleven
of the sixteen as PDFs on 28 October 2026, Eisenstein 1977 the last; another thread of the project fetched the other
five the same day from their publishers' own free copies (Griffith 2016, Twomey 1985, Alonge 2021, Ahmed 2019,
Chaudhary 2015). None is committed.
verification/closed_page_reading.csv is a transcription of the tables these values could come from, whole or at the
values' levels (README, "What the reading leaves out"), made from the page images by readers who were not shown any
of the tables here, as Panjabi's were read (code/check_page_reading.py): one row per cell and statistic, with the
cell as printed (printed_as, empty where the page leaves a cell blank) and where it is (table, pdf_page,
journal_page). For the nine typeset papers (Mitra 2002, Robertson 2000, Yu 2015, Tang 2016, Bach 2019, Griffith,
Alonge, Ahmed and Chaudhary) every value read from a table or the text was also found on the publisher's own text
layer, and Eisenstein's Table I and counts, which two readers read apart, on his scan's text layer, made by optical
character recognition; the data labels read from figures are pictures and have no text layer. Fifteen rows were
added after the blind reading, the counts of people in three papers' Methods, the discs Tang left out and three of
Yu's widths from the text, and each says so in its note.

SOURCES names, for each series, the cells of its own paper that its values should be, as the reading labels them. A
value agrees when its cell, rounded half up to the most decimals its series is written with for that statistic,
equals it: a value written with a trailing zero dropped still agrees, and one cut short does not. FINDINGS says, for
each value that does not agree, what the paper prints instead and the calculation, or the other paper's table, that
reproduces the value, which is then held to it like a cell. NOTES records what a reader of an agreeing value should
still know. The means, SDs, ranges and counts a finding or a note quotes, the cells its calculations take and their
results, and the pages of those cells are computed from the reading when the script runs, and the comparisons its
words make (lower, highest, misprinted, within the cells' rounding, the same as another cell, printed in no other
cell, adding up) are tested on the reading. A group's size or ages that its words give are the ones its selector's
label prints or its cells hold, so a reading that printed others stops the script. Typed, and held by nothing, are
the pages of passages the reading does not hold (Robertson's method, figure captions and tilt, pp. 709-711;
Eisenstein's method, p. 173; the sentences of Chaudhary, p. 34, and Alonge, p. 75, on how Eisenstein measured) and
the words that give no number. DATA_SAID holds what a note says a column of the data holds, and a note fails when the
column holds another; Yu's finding quotes the citation on the data's L1 row and fails when that row cites otherwise.
COUNTS names, for six series, the cell that counts the people a value is of: n_printed beside the data's n, which for
a value of one sex must be the two sexes' counts together. Mitra's men, Olsewski's examples, Robertson's and Hou's
specimens, Zindrick's studies, Hinck's sample size at each level and Eisenstein's skeletons are printed too and have
no entry (README). SCALE turns a paper's printed unit into the data's: Tang prints centimetres. VALUES holds how many
values each series has here.

The script writes verification/closed_page_reading_check.csv and exits 1 on a value that neither agrees nor has a
finding, on a finding with no calculation or whose calculation no longer reproduces its value, on a finding or a
note for a value that is not here, on a finding, a note or a count that needs a cell the reading does not hold once
or whose words the reading no longer bears out, on a note whose DATA_SAID the data no longer holds, on a selector
that picks other than one cell (or other than one SD cell beside a mean the data gives no SD for, where the paper
prints SDs), on a series with another count of values than VALUES holds, and on a row of the reading whose value is
not a number its printed_as prints, where a minus sign is one only with no digit, slash or closing bracket before it,
and a number spelled in words, as Eisenstein prints most of his counts, is the number it spells.
"""
import csv
import io
import math
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
READING = HERE / "verification" / "closed_page_reading.csv"
OUT = HERE / "verification" / "closed_page_reading_check.csv"
SEX = {"M": "male", "F": "female", "all": "all"}
OTHER_SEX = {"M": "F", "F": "M"}
WHO = {"M": "men", "F": "women"}
LUMBAR = ("L1", "L2", "L3", "L4", "L5")
PEDICLES = "pedicle_width_references.csv"
LEVELS = "level_references.csv"

GRIFFITH_W = {"table": "Table 4", "measure_label": "Spinal canal width (mean transverse diameter)"}
GRIFFITH_AP = {"table": "Table 3", "measure_label": "Spinal canal depth (mean anteroposterior diameter)"}
ALONGE_W = {"table": "Table 4", "measure_label": "Transverse diameter (TD)"}
ALONGE_AP = {"table": "Table 3", "measure_label": "Antero-posterior diameter (APD)"}
TWOMEY = {"table": "Table 2", "measure_label": "true average disc height (median-section area / AP diameter)"}
METHODS = {"table": "Methods (text)", "measure_label": "Subjects"}
EISENSTEIN_CANAL = {"table": "Table I", "measure_label": "Canal I.P."}

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
    (LEVELS, "Griffith 2016", "canal_w"): ("griffith2016", GRIFFITH_W),
    (LEVELS, "Griffith 2016", "canal_ap"): ("griffith2016", GRIFFITH_AP),
    (LEVELS, "Alonge 2021", "canal_w"): ("alonge2021", ALONGE_W),
    (LEVELS, "Alonge 2021", "canal_ap"): ("alonge2021", ALONGE_AP),
    (LEVELS, "Ahmed 2019", "canal_w"):
        ("ahmed2019", {"table": "Table 2", "measure_label": "Mean Transverse diameter Mean+/-SD (mm)"}),
    (LEVELS, "Ahmed 2019", "canal_ap"):
        ("ahmed2019", {"table": "Table 1", "measure_label": "Mean Mid-sagittal diameter Mean+/-SD (mm)"}),
    (LEVELS, "Chaudhary 2015", "canal_w"):
        ("chaudhary2015", {"table": "Table I", "measure_label": "Interpedicular distance (mm)"}),
    (LEVELS, "Eisenstein 1977", "canal_w"): ("eisenstein1977", dict(EISENSTEIN_CANAL, group="Caucasoid")),
    (LEVELS, "Twomey 1985", "disc"): ("twomey1985", dict(TWOMEY, group="20-35")),
}

# (data file, series, measure) -> how many values the series has here, so that a row deleted or a series renamed in
# the data fails rather than dropping out
VALUES = {
    (PEDICLES, "Zindrick", "PDW"): 10, (PEDICLES, "Hou", "PDW"): 5, (PEDICLES, "Olsewski", "PDW"): 5,
    (PEDICLES, "Mitra", "PDW"): 5, (PEDICLES, "Robertson", "PDW"): 5, (PEDICLES, "Yu", "PDW"): 5,
    (PEDICLES, "Krag", "PDW"): 5, (LEVELS, "Hinck 1966", "canal_w"): 10, (LEVELS, "Tang 2016", "endplate"): 4,
    (LEVELS, "Bach 2019", "disc"): 24, (LEVELS, "Griffith 2016", "canal_w"): 20,
    (LEVELS, "Griffith 2016", "canal_ap"): 20, (LEVELS, "Alonge 2021", "canal_w"): 20,
    (LEVELS, "Alonge 2021", "canal_ap"): 10, (LEVELS, "Ahmed 2019", "canal_w"): 10,
    (LEVELS, "Ahmed 2019", "canal_ap"): 10, (LEVELS, "Chaudhary 2015", "canal_w"): 10,
    (LEVELS, "Eisenstein 1977", "canal_w"): 5, (LEVELS, "Twomey 1985", "disc"): 20,
}

# The series whose cells are means with no SD printed beside them: Mitra's Table 1, Yu's Table 5 and Eisenstein's
# Table I print means only. Beside any other mean the data gives no SD for, the paper prints one, which the output
# shows (sd_printed).
MEANS_ONLY = {(PEDICLES, "Mitra", "PDW"), (PEDICLES, "Yu", "PDW"), (LEVELS, "Eisenstein 1977", "canal_w")}

# (data file, series, measure) -> (paper, the reading's labels of the cell that counts the people a value is of, and
# that cell's level, None where it is the value's own), for the six series whose paper prints that count as a cell the
# reading holds and whose n is one number. The sex is the value's own. Mitra counts its men in its labels, Olsewski
# its examples and Zindrick its studies in cells, Hinck its people in cells whose range is its n, Hou and Robertson
# their specimens only in text the reading leaves out, and Eisenstein his skeletons in text the reading holds, where
# the data's n is a dash, not a number; these have none (README).
COUNTS = {
    (LEVELS, "Tang 2016", "endplate"): ("tang2016", {"table": "Table 4", "measure_label": "FD_CaEP"}, None),
    (LEVELS, "Bach 2019", "disc"): ("bach2019", {"table": "Table 1", "group": "Total"}, ""),
    (LEVELS, "Griffith 2016", "canal_w"): ("griffith2016", GRIFFITH_W, "L1-L5"),
    (LEVELS, "Griffith 2016", "canal_ap"): ("griffith2016", GRIFFITH_AP, "L1-L5"),
    (LEVELS, "Alonge 2021", "canal_w"): ("alonge2021", ALONGE_W, None),
    (LEVELS, "Alonge 2021", "canal_ap"): ("alonge2021", ALONGE_AP, None),
    (LEVELS, "Ahmed 2019", "canal_w"): ("ahmed2019", METHODS, ""),
    (LEVELS, "Ahmed 2019", "canal_ap"): ("ahmed2019", METHODS, ""),
    (LEVELS, "Chaudhary 2015", "canal_w"): ("chaudhary2015", METHODS, ""),
}

# A paper that prints another unit than the data holds: the factor that turns its printed number into the data's.
# Tang prints centimetres; the data holds millimetres.
SCALE = {"tang2016": 10}


def in_data_units(paper, number):
    return Decimal(number) * SCALE.get(paper, 1)


class Untrue(Exception):
    """Words of a finding or a note that the reading they are computed from no longer bears out."""


def require(holds, what):
    """Stop a finding or a note whose words the reading no longer bears out, naming what failed."""
    if not holds:
        raise Untrue(what)


def bracketed_count(group):
    """The count a group label prints in brackets, as Mitra's "CS direct M(18)" or Yu's "CS, American (N = 503)"."""
    count = re.fullmatch(r".*\((?:N = )?(\d+)\)", group)
    require(count, "the group %r prints no count" % group)
    return int(count.group(1))


def age_words(group):
    """A group label of ages in the prose's words: "Age <=30 yr" is 30 years or less, "Age 50-69 yr" is 50 to 69
    years, and "60+" or "Age >=70 yr" is 60 or 70 and over."""
    ages = re.fullmatch(r"(?:Age )?(<=|>=)?(\d+)(\+|-\d+)?(?: yr)?", group)
    require(ages, "the group %r names no ages" % group)
    below, first, rest = ages.groups()
    if below == "<=":
        return "%s years or less" % first
    if below == ">=" or rest == "+":
        return "%s and over" % first
    require(rest, "the group %r names one age" % group)
    return "%s to %s years" % (first, rest[1:])


# Mitra's Table 1 groups of its own cadavers, as their labels print them, with the sex the reading gives each
MITRA_GROUPS = (("M(18)", "male"), ("F(2)", "female"))


def mitra_rows(method, level):
    """Mitra's transverse diameter by one method over all its cadavers: the men's and the women's means of Table 1,
    each weighted by the count its label prints."""
    cell = {"table": "Table 1", "measure_label": "TD"}
    return [("mitra2002", dict(cell, group="CS %s %s" % (method, who), sex=sex), level, bracketed_count(who))
            for who, sex in MITRA_GROUPS]


def mitra_ct(level):
    return mitra_rows("CT", level)


def mitra_direct(level):
    return mitra_rows("direct", level)


def mitra_people():
    """Mitra's men and women, as the labels of Table 1's rows count them.

    The selectors hold the labels to the reading.
    """
    return [weight for *_, weight in mitra_direct("L1")]


def yu_table5(group, level):
    """A row of Yu 2015's Table 5, which sets other studies' pedicle widths beside Yu's own."""
    return [("yu2015", {"table": "Table 5", "measure_label": "PW", "group": group, "sex": ""}, level, 1)]


YU_AGES = ("Age <=30 yr", "Age 31-49 yr", "Age 50-69 yr", "Age >=70 yr")

# The words of the data's citation for Yu that its finding quotes
YU_CITED = "midpoint of published range"


def yu_age_midpoint(level):
    """The midpoint of two of Yu 2015's four age groups in Table 3: the youngest and 50 to 69 years."""
    cell = {"table": "Table 3", "measure_label": "PW"}
    return [("yu2015", dict(cell, group=YU_AGES[0]), level, 1), ("yu2015", dict(cell, group=YU_AGES[2]), level, 1)]


def yu_age_means(reading, level):
    """Yu's Table 3 means of its four age groups at one level, youngest first."""
    cell = {"table": "Table 3", "measure_label": "PW"}
    return [Decimal(one_cell(reading, "yu2015", dict(cell, group=g), level, "all", "mean")["value"]) for g in YU_AGES]


YU_STATISTIC = {"mean": "mean", "sd": "SD", "n": "count"}


def also_printed(c, level):
    """A cell of Yu's, other than its own means, that prints the series' value, in the finding's words: its table, its
    measure where it is not the series' PW, its statistic, its group, and its level where it is not the value's."""
    what = YU_STATISTIC.get(c["statistic"], c["statistic"])
    if c["measure_label"] != "PW":
        what = "%s %s" % (c["measure_label"], what)
    at = "" if level_key(c["level"]) == level_key(level) else " at %s" % c["level"]
    return "%s's %s for the %s specimens%s is also %s" % (c["table"], what, c["group"], at, c["value"])


KRAG_IN_YU = "Krag et al, American (N = 14-24)"
MITRA_IN_YU = "Mitra et al, Indian (N = 20)"


def plain(value):
    return format(value.normalize(), "f")


def krag_finding(reading):
    """What Krag prints in place of a mean width, from the reading: Table 2's bins and the widths the text gives."""
    table2 = [c for c in reading if c["paper"] == "krag1988" and c["table"] == "Table 2"]
    bins = sorted({tuple(c["column_label"][:-len(" mm")].split("-")) for c in table2
                   if c["column_label"].endswith(" mm")}, key=lambda b: Decimal(b[0]))
    widths = {math.ceil(Decimal(high) - Decimal(low)) for low, high in bins[:-1]}
    require(len(widths) == 1, "Krag's Table 2 bins below the top one are not of one width")
    pages = {c["journal_page"] for c in table2}
    require(len(pages) == 1, "Krag's Table 2 is not on one page")
    page, = pages
    text = {"table": "Text: Results", "measure_label": "pedicle diameter (Figure 5)"}
    upper, lower = (one_cell(reading, "krag1988", text, level, "all", "approximately") for level in ("L1", "L5"))
    require("between T9 and L1" in upper["printed_as"], "Krag's text no longer gives its width from T9 to L1")
    zero = one_cell(reading, "krag1988", dict(text, measure_label="pedicle diameter perpendicular to the 0 deg axis"),
                    "L5", "all", "mean")
    in_yu = one_cell(reading, "yu2015", yu_table5(KRAG_IN_YU, "L5")[0][1], "L5", "all", "mean")
    require(Decimal(zero["value"]) < Decimal(in_yu["value"]), "Krag's 0 deg width at L5 is not below Yu's")
    krag = {r["level"]: Decimal(r["mean"]) for r in rows_of(PEDICLES) if r["series"] == "Krag"}
    printing = sorted(paper for paper in {c["paper"] for c in reading} if all(
        any(c["paper"] == paper and level_key(c["level"]) == level_key(level) and a_number(c["value"])
            and Decimal(c["value"]) == value for c in reading) for level, value in krag.items()))
    require(printing == ["yu2015"], "the papers whose cells here print Krag's five values at their levels are %s"
            % printing)
    return ("Krag prints no table of mean widths: Table 2 (p. %s) counts pedicles in bins of %d mm from %s mm and a "
            "top bin of %s to %s mm, the figures plot means with no printed values, and the text gives about %s mm "
            "from T9 to L1 and about %s mm at L5 (p. %s), and %s mm at L5 by the 0 deg method (p. %s), below the %s at "
            "L5 here. The five values are Yu 2015's Table 5 row for Krag et al (p. %s). No other paper's cells here "
            "print them, so Yu is the likeliest place the table read them from; how Yu came by them is not said"
            % (page, *widths, bins[0][0], *bins[-1], upper["value"], lower["value"], lower["journal_page"],
               zero["value"], zero["journal_page"], in_yu["value"], in_yu["journal_page"]))


def mitra_in_yu(reading, level):
    """Yu 2015's Table 5 cell under Mitra's name at one level, and Mitra's direct mean over all its cadavers, which
    the cell must be at the decimals it is printed with."""
    in_yu = one_cell(reading, "yu2015", yu_table5(MITRA_IN_YU, level)[0][1], level, "all", "mean")
    direct, _ = reproduce(reading, mitra_direct(level), "all", "mean")
    require(rounds_to(in_yu["value"], direct), "Yu's Table 5 cell under Mitra's name at %s is not Mitra's direct "
            "mean over all its cadavers" % level)
    return in_yu, direct


def mitra_finding(reading, level):
    """What Mitra prints at L2 to L4, and how the series' value is had from it, from the reading."""
    men, women = mitra_people()
    printed = one_cell(reading, "mitra2002", SOURCES[(PEDICLES, "Mitra", "PDW")][1], level, "all", "mean")
    in_yu, direct = mitra_in_yu(reading, level)
    return ("Table 1 (p. %s) prints %s for the %d men measured directly. The value is the mean of the CT rows over "
            "all %d cadavers, %d men and %d women weighted; L1 and L5 are the men's direct means, which the abstract "
            "quotes, so the series mixes two methods. Yu 2015's Table 5 (p. %s) prints %s under Mitra's name, the "
            "direct means over all %d (%s)"
            % (printed["journal_page"], printed["printed_as"], men, men + women, men, women, in_yu["journal_page"],
               in_yu["value"], men + women, plain(direct)))


def mitra_note(reading, level):
    """What Mitra's L1 and L5 are, beside its means over all its cadavers, from the reading."""
    men, women = mitra_people()
    in_yu, direct = mitra_in_yu(reading, level)
    ct, _ = reproduce(reading, mitra_ct(level), "all", "mean")
    return ("The value is the %d men's direct mean, which the abstract quotes; the n column's %d counts the %d women "
            "too. Over all %d cadavers the direct means give %s and the CT means %s; L2 to L4 are the CT means over "
            "all %d, so the series mixes two methods and two groups. Yu 2015's Table 5 (p. %s) prints %s under "
            "Mitra's name, the direct mean over all %d"
            % (men, men + women, women, men + women, plain(direct), plain(ct), men + women, in_yu["journal_page"],
               in_yu["value"], men + women))


def yu_finding(reading, level):
    """What Yu prints as its own means, and where the series' value comes from instead, from the reading."""
    own = [one_cell(reading, "yu2015", SOURCES[(PEDICLES, "Yu", "PDW")][1], at, "all", "mean") for at in LUMBAR]
    specimens = bracketed_count(own[0]["group"])
    pw = {"measure_label": "PW"}
    abstract = one_cell(reading, "yu2015", dict(pw, table="Abstract (text)"), "L5", "all", "mean")
    first, last = (one_cell(reading, "yu2015", dict(pw, table="Results (text)"), at, "all", "mean")
                   for at in ("L1", "L5"))
    young = one_cell(reading, "yu2015", yu_age_midpoint(level)[0][1], level, "all", "mean")
    middle, _ = reproduce(reading, yu_age_midpoint(level), "all", "mean")
    shown = middle.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    same = [c for c in reading if c["paper"] == "yu2015" and c["value"] and Decimal(c["value"]) == shown]
    require(all(c["group"] and c["group"] != own[0]["group"] for c in same),
            "Yu's own mean prints the series' value %s at %s" % (shown, level))
    named = [also_printed(c, level) for c in same]
    require(len(set(named)) == len(named), "Yu's cells of the series' value at %s are read twice" % level)
    extra = " as Yu's own, though " + " and ".join(named) if same else ""
    taken = (YU_AGES.index(yu_age_midpoint(level)[0][1]["group"]), YU_AGES.index(yu_age_midpoint(level)[1][1]["group"]))
    extremes = [at for at in LUMBAR if (min(range(4), key=yu_age_means(reading, at).__getitem__),
                                        max(range(4), key=yu_age_means(reading, at).__getitem__)) == taken]
    require(extremes == list(LUMBAR[:-1]), "Yu's two age groups are not the lowest and highest from L1 to L4")
    cited = [r["citation"] for r in rows_of(PEDICLES) if r["series"] == "Yu" and r["level"] == LUMBAR[0]]
    require(len(cited) == 1 and YU_CITED in cited[0], "the data's L1 row for Yu no longer cites %r" % YU_CITED)
    beyond = yu_age_means(reading, LUMBAR[-1])
    require(max(range(4), key=beyond.__getitem__) == len(YU_AGES) - 1, "Yu's oldest group is not the highest at L5")
    return ("Yu's own means, over %s specimens with the two sides averaged, are printed %s, %s, %s, %s and %s (Table "
            "5, p. %s); the abstract gives %s at L5 (p. %s), and the Results %s at L1 and %s at L5 (p. %s). The "
            "series' value is printed nowhere in the paper%s. It is the midpoint of Table 3's means for the youngest "
            "age group (%s) and for %s (p. %s), at all five levels. From %s to %s those two are the lowest and "
            "highest of the four age groups, which fits the citation on the data's %s row, \"%s\"; at %s the "
            "oldest group's %s is higher still, and the same two groups were taken there too"
            % (specimens, *(c["value"] for c in own), own[0]["journal_page"], abstract["value"],
               abstract["journal_page"], first["value"], last["value"], first["journal_page"], extra,
               age_words(YU_AGES[taken[0]]), age_words(YU_AGES[taken[1]]), young["journal_page"], extremes[0],
               extremes[-1], LUMBAR[0], YU_CITED, LUMBAR[-1], plain(beyond[-1])))


# (series, measure, level, sex, kind) -> (what the paper prints instead, or how to compute it from the reading; the
# cells that reproduce the value)
FINDINGS = {("Krag", "PDW", level, "all", "mean"): (krag_finding, yu_table5(KRAG_IN_YU, level)) for level in LUMBAR}
FINDINGS.update({
    ("Mitra", "PDW", level, "all", "mean"): (lambda reading, level=level: mitra_finding(reading, level),
                                             mitra_ct(level))
    for level in ("L2", "L3", "L4")
})
FINDINGS.update({
    ("Yu", "PDW", level, "all", "mean"): (lambda reading, level=level: yu_finding(reading, level),
                                          yu_age_midpoint(level))
    for level in LUMBAR
})


def robertson_left(reading, measure, level):
    """One of Robertson's Table 1 rows on the left side, at one level."""
    cell = {"table": "Table 1", "measure_label": measure, "side": "left"}
    return one_cell(reading, "robertson2000", cell, level, "all", "mean")


def robertson_note(reading, level):
    """Which side and which width Robertson's series is, and its isthmus row beside it, from the reading."""
    isthmus, axis = (robertson_left(reading, m, level) for m in ("Isthmus", "Axis"))
    widths, diameters = ([Decimal(robertson_left(reading, m, at)["value"]) for at in LUMBAR]
                         for m in ("Width", "Isthmus"))
    gaps = [width - diameter for width, diameter in zip(widths, diameters)]
    require(min(gaps[3:]) > max(gaps[:3]), "Robertson's width is not furthest above its isthmus diameter at L4 and L5")
    return ("The left side only, as Table 1 (p. %s) prints it; the table does not say whose left, and the captions of "
            "Figures 3 and 4 give left and right as viewed by the reader (p. 710). Robertson's width is the "
            "medial-to-lateral extent of the wire drawn tight around the pedicle's isthmus, on its outer cortex, on "
            "the coaxial radiograph (pp. 709-710): the transverse width at the isthmus. Its isthmus diameter, %s on "
            "the left here, is the short axis of the pedicle's ellipse at the isthmus, whose long axis lies %s deg "
            "from the vertical at this level; the paper puts the gap between the two at L4 and L5 down to that tilt "
            "(p. 711)" % (isthmus["journal_page"], isthmus["printed_as"], axis["value"]))


def tang_note(reading, level, disc):
    """What Tang's cell measures, and why its N is below the study's, from the reading."""
    subjects = {"table": "Methods (text)", "measure_label": "Subjects"}
    everyone, women, men = (one_cell(reading, "tang2016", subjects, "", sex, "n") for sex in ("all", "F", "M"))
    left_out = one_cell(reading, "tang2016", {"table": "Methods (text)", "measure_label": "IVDs of Pfirrmann grade "
                                              "V, excluded"}, disc, "M", "n")
    labels = COUNTS[(LEVELS, "Tang 2016", "endplate")][1]
    counted = [one_cell(reading, "tang2016", labels, level, sex, "n") for sex in ("F", "M")]
    require(int(everyone["value"]) == int(women["value"]) + int(men["value"]), "Tang's subjects are not its women "
                                                                               "and men")
    require(counted[0]["value"] == women["value"], "Tang's Table 4 does not count every woman at %s" % level)
    require(int(counted[1]["value"]) == int(men["value"]) - int(left_out["value"]),
            "Tang's Table 4 does not count the men less the discs left out at %s" % level)
    counted_all = one_cell(reading, "tang2016", labels, level, "all", "n")
    require(int(counted_all["value"]) == int(counted[0]["value"]) + int(counted[1]["value"]),
            "Tang's Table 4 count of everyone at %s is not its women and men" % level)
    return ("Tang prints centimetres and the data holds millimetres, so the cell is read times %s. %s is the "
            "frontal diameter, the right-to-left extent, of the caudal end plate of the %s disc, which is %s's upper "
            "end plate. The study's %s subjects are %s women and %s men, and the %s men's discs of Pfirrmann grade V "
            "at %s were left out with their end plates (p. %s): Table 4 counts %s women and %s men here (p. %s)"
            % (SCALE["tang2016"], labels["measure_label"], disc, level, everyone["value"], women["value"],
               men["value"], left_out["value"], disc, everyone["journal_page"], counted[0]["value"],
               counted[1]["value"], counted[0]["journal_page"]))

BACH_DECADES = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh")
BACH_SEX = {"M": ("men", "Table 2"), "F": ("women", "Table 3")}


def hundredths(value):
    return format(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")


def thousandths(value):
    return format(value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP), "f")


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


def half_unit(value):
    """Half a unit of the last decimal a value is printed with: as far as its rounding may have moved it."""
    return Decimal(5).scaleb(-decimals(value) - 1)


def at_edge_of_rounding(reading, terms, sex, side):
    """The weighted mean of the cells a calculation names, each taken at one edge of its own printed rounding: the
    top for side 1, the bottom for side -1."""
    total, weights = Decimal(0), 0
    for paper, labels, level, weight in terms:
        value = one_cell(reading, paper, labels, level, sex, "mean")["value"]
        total += (Decimal(value) + side * half_unit(value)) * weight
        weights += weight
    return total / weights


def rounding_said(reading, terms, sex, printed, pooled):
    """Nothing when the pooled mean rounds to the printed value; else whether the cells, each moved within its own
    printed rounding toward the printed value, can give it."""
    if rounds_to(printed, pooled):
        return ""
    side = 1 if pooled < Decimal(printed) else -1
    edge = at_edge_of_rounding(reading, terms, sex, side)
    reached = (edge > Decimal(printed) - half_unit(printed) if side == 1 else
               edge < Decimal(printed) + half_unit(printed))
    shown = pooled.quantize(Decimal(1).scaleb(-decimals(printed)), rounding=ROUND_HALF_UP)
    return (", which rounds to %s, not the printed %s; with each decade cell at the %s of its own printed rounding "
            "they give %s, so the printed value is %s the cells' rounding"
            % (shown, printed, "top" if side == 1 else "bottom", thousandths(edge), "within" if reached else "beyond"))


def bach_printed(reading, level, sex, kind):
    """The Results' cell of one of Bach's averages and the abstract's, which must print the same."""
    labels = SOURCES[(LEVELS, "Bach 2019", "disc")][1]
    results = one_cell(reading, "bach2019", labels, level, sex, kind)
    abstract = one_cell(reading, "bach2019", dict(labels, table="Abstract (text)"), level, sex, kind)
    require(results["value"] == abstract["value"], "Bach's Results and abstract print another %s at %s"
            % (kind, level))
    return results, abstract


def bach_note(reading, level, sex, kind):
    """What the Results' average is, beside Table 6's, and what its unnamed +/- is, computed from the reading."""
    who, table = BACH_SEX[sex]
    three = bach_decades(reading, "Average disc height", level, sex)
    total = one_cell(reading, "bach2019", COUNTS[(LEVELS, "Bach 2019", "disc")][1], "", sex, "n")
    require(sum(weight for *_, weight in three) == int(total["value"]),
            "Bach's Table 1 decades of the %s do not add up to its total" % who)
    printed, abstract = bach_printed(reading, level, sex, kind)
    if kind == "mean":
        pooled, _ = reproduce(reading, three, sex, "mean")
        a, p, t6 = (Decimal(one_cell(reading, "bach2019", {"table": "Table 6", "measure_label": m + " disc height"},
                                     level, sex, "mean")["value"]) for m in ("Anterior", "Posterior", "Average"))
        require(abs(t6 - (a + p) / 2) <= half_unit(str(t6)) + (half_unit(str(a)) + half_unit(str(p))) / 2,
                "Bach's Table 6 average at %s is not the mean of its anterior and posterior rows" % level)
        require(not rounds_to(printed["value"], t6), "Bach's Table 6 average at %s is the Results' one" % level)
        return ("Printed in the Results (p. %s) and the abstract (p. %s): the mean of the anterior, middle and "
                "posterior heights over all ages, which %s's decade rows of that mean, weighted by Table 1's counts, "
                "give as %s%s. Table 6's 'Average disc height' for all ages is another quantity, %s, the mean of its "
                "anterior and posterior rows alone, (%s + %s) / 2 = %s"
                % (printed["journal_page"], abstract["journal_page"], table, thousandths(pooled),
                   rounding_said(reading, three, sex, printed["value"], pooled), t6, a, p, format((a + p) / 2, "f")))
    sd = pooled_sd(reading, three, sex)
    people = sum(weight for *_, weight in three)
    se = sd / Decimal(people).sqrt()
    require(abs(Decimal(printed["value"]) - sd) < abs(Decimal(printed["value"]) - se),
            "Bach's +/- at %s is nearer the SE of its mean than the SD" % level)
    return ("The Results (p. %s) and the abstract (p. %s) do not say what this +/- is. %s's decade rows of the mean "
            "of three, pooled as SDs with their means and Table 1's counts, give %s: the size of an SD over all the "
            "%d %s, not of the SE of their mean, which would be %s"
            % (printed["journal_page"], abstract["journal_page"], table, hundredths(sd), people, who, hundredths(se)))


TWOMEY_COUNT = {"table": "Table 1", "measure_label": "number of cadavers"}


def twomey_groups(reading):
    """Twomey's Table 1 cells that count the cadavers of each of its groups."""
    return [c for c in reading if c["paper"] == "twomey1985" and c["statistic"] == "n"
            and all(c[k] == v for k, v in TWOMEY_COUNT.items())]


def twomey_cadavers(reading):
    """Every cadaver Twomey's Table 1 counts, of every age and sex, and the children among them, whose groups count
    the sexes together."""
    groups = twomey_groups(reading)
    return sum(int(c["value"]) for c in groups), sum(int(c["value"]) for c in groups if c["sex"] == "all")


def twomey_ages(reading, groups, sex):
    """The youngest and the oldest age Table 1 prints for some of its groups of one sex, in the prose's words."""
    age = {"table": "Table 1", "measure_label": "age"}
    young, old = (bound([Decimal(one_cell(reading, "twomey1985", dict(age, group=g), "", sex, kind)["value"])
                         for g in groups]) for bound, kind in ((min, "min"), (max, "max")))
    return "%s to %s" % (plain(young), plain(old))


def twomey_note(reading, level, sex, kind):
    """What Twomey's Table 2 measures and counts, and its oddities at L1-L2, computed from the reading."""
    total, children = twomey_cadavers(reading)
    pooled = [c["group"] for c in twomey_groups(reading) if c["sex"] == "all"]
    men = one_cell(reading, "twomey1985", dict(TWOMEY_COUNT, group="20-36"), "", "M", "n")
    women = one_cell(reading, "twomey1985", dict(TWOMEY_COUNT, group="18-35"), "", "F", "n")
    labels = SOURCES[(LEVELS, "Twomey 1985", "disc")][1]
    cell = one_cell(reading, "twomey1985", labels, level, sex, kind)
    require(not [c for c in reading if c["paper"] == "twomey1985" and c["table"] == TWOMEY["table"]
                 and c["statistic"] == "n"], "Twomey's Table 2 prints an n")
    said = ("Table 2's true average disc height, the area of the disc's median section divided by its "
            "antero-posterior diameter, for the group it heads %s (p. %s). The n column's %d counts every "
            "cadaver of Table 1, of every age, %d of them children aged %s with the sexes pooled. Table 2 "
            "prints no n; Table 1's young adults are %s men aged %s and %s women aged %s (p. %s). The "
            "paper names no population; its authors worked in Western Australia"
            % (cell["group"], cell["journal_page"], total, children, twomey_ages(reading, pooled, "all"),
               men["value"], twomey_ages(reading, [men["group"]], "M"), women["value"],
               twomey_ages(reading, [women["group"]], "F"), men["journal_page"]))
    if (level, sex, kind) == ("L1L2", "M", "sd"):
        require("," in cell["printed_as"], "Twomey's men's SD at L1-L2 is printed with no decimal comma")
        said += ". The cell is printed %s, the SD with a decimal comma" % cell["printed_as"]
    if (level, sex) == ("L1L2", "F"):
        mean = Decimal(one_cell(reading, "twomey1985", labels, level, sex, "mean")["value"])
        others = [Decimal(one_cell(reading, "twomey1985", labels, other, sex, "mean")["value"])
                  for other in ("L2L3", "L3L4", "L4L5", "L5S1")]
        old = one_cell(reading, "twomey1985", dict(TWOMEY, group="60+"), level, sex, "mean")
        require(cell["legibility"] == "clear", "Twomey's women's cell at L1-L2 is not read as clear")
        require(mean < min(others) and mean < Decimal(old["value"]), "Twomey's women's mean at L1-L2 is not below "
                                                                      "their other levels and their elders'")
        said += (". The cell, %s, is printed clearly, yet its mean is below these women's other four levels (%s to "
                 "%s) and below the same level at %s (%s)"
                 % (cell["printed_as"], min(others), max(others), age_words(old["group"]), old["value"]))
    return said


# How Eisenstein says he measured (p. 173), and what the two other papers read here say of it; the reading holds
# none of these sentences, so their pages are typed (above)
EISENSTEIN_METHOD = ("with a vernier caliper, the canal's transverse diameter taken as the greatest interpedicular "
                     "distance (p. 173)")
ALONGE_ON_EISENSTEIN = "Alonge 2021's study of Caucasian and Negroid bone specimens (p. 75)"
CHAUDHARY_ON_EISENSTEIN = "Chaudhary's plain radiography (p. 34)"

# Chaudhary's Table II labels for the groups of Eisenstein's that it copies, by his Table I's labels
EISENSTEIN_IN_CHAUDHARY = {"Caucasoid": "Eisenstein 1977. (South African Caucasoids)",
                           "Zulu Negroid": "Eisenstein 1977 (Zulus)"}


def eisenstein_count(reading, table, measure, group="", sex="all"):
    """One of the counts of skeletons or vertebrae Eisenstein's text prints."""
    return one_cell(reading, "eisenstein1977", {"table": table, "measure_label": measure, "group": group}, "", sex, "n")


def number_of(cell):
    return int(cell["value"])


def eisenstein_groups(reading):
    """Eisenstein's groups as his Table I names them, in the order it prints them."""
    groups = []
    for c in reading:
        if c["paper"] == "eisenstein1977" and c["table"] == EISENSTEIN_CANAL["table"] and c["group"] not in groups:
            groups.append(c["group"])
    return groups


def eisenstein_skeletons(reading):
    """Eisenstein's skeletons by group and sex as his Methods count them, each group's men and women adding up to it,
    and the cells of the total the Methods, the Results and the Summary print: the first two must be the groups'
    sum, and the Summary's is another."""
    each = {}
    for group in eisenstein_groups(reading):
        sexes_add_up(reading, "eisenstein1977", {"table": "Methods (text)", "measure_label": "Skeletons",
                                                 "group": group}, "")
        each[group] = {sex: number_of(eisenstein_count(reading, "Methods (text)", "Skeletons", group, sex))
                       for sex in ("all", "M", "F")}
    total, results, summary = (eisenstein_count(reading, table, "Skeletons")
                               for table in ("Methods (text)", "Results (text)", "Summary (text)"))
    require(sum(e["all"] for e in each.values()) == number_of(total) == number_of(results),
            "Eisenstein's groups do not add up to the skeletons his Methods and Results count")
    require(number_of(summary) != number_of(total), "Eisenstein's Summary counts the skeletons his Methods do")
    return each, total, summary


def eisenstein_vertebrae(reading, skeletons):
    """Eisenstein's vertebrae missing or damaged, and the cell of those measured, which his Summary, Methods and
    Results must all print alike; the two must make five for each skeleton."""
    missing = eisenstein_count(reading, "Methods (text)", "Vertebrae missing or damaged")
    measured = [eisenstein_count(reading, table, measure) for table, measure in (
        ("Results (text)", "Vertebrae measured"), ("Methods (text)", "Complete vertebrae available for study"),
        ("Summary (text)", "Lumbar vertebrae measured directly"))]
    require(len({number_of(c) for c in measured}) == 1,
            "Eisenstein's Summary, Methods and Results print other counts of the vertebrae measured")
    require(number_of(missing) + number_of(measured[0]) == 5 * skeletons,
            "Eisenstein's vertebrae measured and missing do not make five for each skeleton")
    return missing, measured[0]


def chaudhary_copy_of_eisenstein(reading):
    """Chaudhary's Table II means under Eisenstein's name, each of which must be his own Table I's, at the same level
    for the same group and sex: how many there are, their page, and the groups of Eisenstein's they leave out."""
    copied = [c for c in reading if c["paper"] == "chaudhary2015" and c["table"] == "Table II"
              and "Eisenstein" in c["group"]]
    require({c["group"] for c in copied} == set(EISENSTEIN_IN_CHAUDHARY.values()),
            "Chaudhary's Table II names other groups of Eisenstein's")
    by_label = {label: group for group, label in EISENSTEIN_IN_CHAUDHARY.items()}
    for c in copied:
        sex = {v: k for k, v in SEX.items()}[c["sex"]]
        own = one_cell(reading, "eisenstein1977", dict(EISENSTEIN_CANAL, group=by_label[c["group"]]), c["level"], sex,
                       c["statistic"])
        require(Decimal(c["value"]) == Decimal(own["value"]), "Chaudhary's copy of Eisenstein's %s %s at %s is not his"
                % (by_label[c["group"]], WHO.get(sex, sex), c["level"]))
    pages = {c["journal_page"] for c in copied}
    require(len(pages) == 1, "Chaudhary's copy of Eisenstein is not on one page")
    left_out = [group for group in eisenstein_groups(reading) if group not in EISENSTEIN_IN_CHAUDHARY]
    return len(copied), pages.pop(), left_out


def eisenstein_note(reading, level):
    """Eisenstein's own cell, how he measured it, Chaudhary's copy of his table, and the counts his text prints, from
    the reading."""
    labels = SOURCES[(LEVELS, "Eisenstein 1977", "canal_w")][1]
    group = labels["group"]
    own = one_cell(reading, "eisenstein1977", labels, level, "M", "mean")
    zulu = one_cell(reading, "eisenstein1977", dict(labels, group="Zulu Negroid"), level, "M", "mean")
    copied, copy_page, left_out = chaudhary_copy_of_eisenstein(reading)
    each, total, summary = eisenstein_skeletons(reading)
    missing, measured = eisenstein_vertebrae(reading, number_of(total))
    radiographed, of = (eisenstein_count(reading, "Methods (text)", m) for m in ("Vertebrae radiographed",
                                                                                 "Skeletons radiographed"))
    men = eisenstein_count(reading, "Methods (text)", "Skeletons", group, "M")
    data = DATA_SAID[(LEVELS, "Eisenstein 1977", "canal_w")]
    return ("Eisenstein's own Table I (p. %s) prints it as the mean interpedicular width of the canal (I.P.) of his "
            "%s men. The level table read it from Chaudhary's Table II (p. %s), as its citation and its source_kind, "
            "%s, say; Chaudhary's %d means under Eisenstein's name are his %s rows of both sexes, each the same as "
            "his, and leave out his %s rows. Eisenstein measured the vertebrae of %s adult skeletons of the Raymond Dart "
            "Collection %s, and Table I is of the %s vertebrae so measured (p. %s); radiographs of %s vertebrae of %s "
            "skeletons repeated the measures (p. %s). So the modality column's %s is right, as is %s, while %s does "
            "not describe these values. The cohort column, %s, names the two groups Chaudhary copies; this value is of "
            "the %s men alone, %s of the %d %s skeletons (p. %s), and the Zulu men's is %s. Table I prints no count, "
            "and %s vertebrae were missing or damaged, which with the %s measured makes five for each of the %s "
            "skeletons (p. %s), so the count of men's vertebrae behind the mean at %s is not printed; the n column "
            "holds \"%s\". The Summary's %s skeletons (p. %s) is a misprint: the Methods and the Results print %s, the "
            "sum of his %d groups"
            % (own["journal_page"], group, copy_page, data["source_kind"], copied,
               " and ".join(EISENSTEIN_IN_CHAUDHARY), " and ".join(left_out), total["value"], EISENSTEIN_METHOD,
               format(number_of(measured), ","), measured["journal_page"], radiographed["value"], of["value"],
               radiographed["journal_page"], data["modality"], ALONGE_ON_EISENSTEIN, CHAUDHARY_ON_EISENSTEIN,
               data["cohort"], group, men["value"], each[group]["all"], group, men["journal_page"], zulu["value"],
               missing["value"], format(number_of(measured), ","), total["value"], missing["journal_page"], level,
               data["n"], summary["value"], summary["journal_page"], total["value"], len(each)))


def chaudhary_range_note(reading, level):
    """The SD that Table I's range of mean +/- 3 SD implies, beside the SD it prints."""
    cell = SOURCES[(LEVELS, "Chaudhary 2015", "canal_w")][1]
    low, high = (one_cell(reading, "chaudhary2015", cell, level, "M", k) for k in ("mean-3sd", "mean+3sd"))
    mean = one_cell(reading, "chaudhary2015", cell, level, "M", "mean")["value"]
    middle = (Decimal(low["value"]) + Decimal(high["value"])) / 2
    require(abs(middle - Decimal(mean)) <= (half_unit(low["value"]) + half_unit(high["value"])) / 2 + half_unit(mean),
            "Chaudhary's range at %s is not centred on its mean" % level)
    sd = one_cell(reading, "chaudhary2015", cell, level, "M", "sd")["value"]
    implied = (Decimal(high["value"]) - Decimal(low["value"])) / 6
    require(not rounds_to(sd, implied), "Chaudhary's range at %s gives the SD its column prints" % level)
    return ("Table I's range of mean +/- 3 SD, %s to %s (p. %s), gives an SD of %s, where its SD column prints %s; "
            "one of the two is misprinted, and the data holds the column's"
            % (low["value"], high["value"], low["journal_page"], hundredths(implied), sd))


# (series, measure, level, sex, kind) -> what a reader of an agreeing value should still know, or how to compute it
# from the reading
NOTES = {
    ("Robertson", "PDW", level, "all", "mean"): (lambda reading, level=level: robertson_note(reading, level))
    for level in LUMBAR
}
NOTES.update({
    ("Mitra", "PDW", level, "all", "mean"): (lambda reading, level=level: mitra_note(reading, level))
    for level in ("L1", "L5")
})
NOTES.update({
    ("Tang 2016", "endplate", level, "all", kind): (lambda reading, level=level, disc=disc:
                                                    tang_note(reading, level, disc))
    for level, disc in (("L4", "L3/L4"), ("L5", "L4/L5")) for kind in ("mean", "sd")
})
NOTES.update({
    ("Bach 2019", "disc", level, sex, kind): (lambda reading, level=level, sex=sex, kind=kind:
                                               bach_note(reading, level, sex, kind))
    for level in ("T12L1", "L1L2", "L2L3", "L3L4", "L4L5", "L5S1") for sex in ("M", "F") for kind in ("mean", "sd")
})
NOTES.update({
    ("Twomey 1985", "disc", level, sex, kind): (lambda reading, level=level, sex=sex, kind=kind:
                                                 twomey_note(reading, level, sex, kind))
    for level in ("L1L2", "L2L3", "L3L4", "L4L5", "L5S1") for sex in ("M", "F") for kind in ("mean", "sd")
})
NOTES.update({
    ("Eisenstein 1977", "canal_w", level, "M", "mean"): (lambda reading, level=level: eisenstein_note(reading, level))
    for level in LUMBAR
})
NOTES.update({
    ("Chaudhary 2015", "canal_w", level, "M", "sd"): (lambda reading, level=level:
                                                       chaudhary_range_note(reading, level))
    for level in ("L4", "L5")
})

# (data file, series, measure) -> {a column of the data: what the series' notes say it holds, or how to compute that
# from the reading}; a note fails when its value's data row holds another, so it cannot outlive the data it describes
DATA_SAID = {
    (LEVELS, "Twomey 1985", "disc"): {"n": lambda reading: str(twomey_cadavers(reading)[0])},
    (PEDICLES, "Mitra", "PDW"): {"n": lambda reading: str(sum(mitra_people()))},
    (LEVELS, "Eisenstein 1977", "canal_w"): {"cohort": "Caucasoid and Zulu", "modality": "dry bone", "n": "-",
                                             "source_kind": "secondary",
                                             "citation": "Eisenstein S 1977, via Chaudhary S et al. 2015 (whole mm)"},
}


def rows_of(name):
    lines = [l for l in (DATA / name).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def decimals(text):
    return len(text.split(".")[1]) if "." in text else 0


def level_key(level):
    """L4-L5, L4/L5 and L4L5 name one disc."""
    return level.replace("-", "").replace("/", "").replace(" ", "")


def rounds_to(recorded, number, places=None):
    """A number agrees with a recorded value when, rounded half up to the recorded decimals, or to places where they
    are given, it equals it."""
    q = Decimal(1).scaleb(-(decimals(recorded) if places is None else places))
    return Decimal(number).quantize(q, rounding=ROUND_HALF_UP) == Decimal(recorded).quantize(q)


def most_decimals(every):
    """The most decimals each series is written with here, for each statistic: (file, series, measure, kind) ->
    places."""
    most = {}
    for name, series, measure, _, _, kind, recorded, _ in every:
        key = (name, series, measure, kind)
        most[key] = max(most.get(key, 0), decimals(recorded))
    return most


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
    if not found[0]["value"]:
        raise LookupError("%s %s at %s %s %s picks a cell with no value" % (paper, labels, level, sex, kind))
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


def count_of(reading, key, level, sex):
    """The cell that counts the people of one sex a value is of, and that count for the other sex, where COUNTS names
    the cell; the other is None for a value of both sexes."""
    paper, labels, at = COUNTS[key]
    at = level if at is None else at
    sexes_add_up(reading, paper, labels, at)
    other = OTHER_SEX.get(sex)
    return (one_cell(reading, paper, labels, at, sex, "n"),
            None if other is None else one_cell(reading, paper, labels, at, other, "n")["value"])


def sexes_add_up(reading, paper, labels, at):
    """Where the reading holds a count of both sexes beside the women's and the men's, it must be the two together."""
    everyone, women, men = (cells(reading, paper, labels, at, sex, "n") for sex in ("all", "F", "M"))
    if everyone and women and men:
        require(len(everyone) == len(women) == len(men) == 1 and int(everyone[0]["value"]) ==
                int(women[0]["value"]) + int(men[0]["value"]),
                "%s's count of both sexes at %s is not its women and men" % (paper, at or "its level"))


def count_said(data_n, count, other, sex):
    """The sentence a note gets when the data's n is not the count of the people its value is of. For a value of one
    sex, the n column must count both sexes, as the README says the level table's does."""
    where = "%s, p. %s" % (count["table"], count["journal_page"])
    if other is None:
        return "This cell's N is %s (%s), where the n column has %s" % (count["value"], where, data_n)
    require(data_n == str(int(count["value"]) + int(other)), "the n column's %s is not the %s and the other sex "
            "together, %s and %s" % (data_n, WHO[sex], count["value"], other))
    return "The n column's %s counts both sexes; the %s are %s (%s)" % (data_n, WHO[sex], count["value"], where)


def data_unsaid(reading, data_key, data_row, key):
    """The problems of a value's note that says a column of its data row holds what the row does not."""
    problems = []
    for column, said in DATA_SAID.get(data_key, {}).items():
        said = said(reading) if callable(said) else said
        if data_row[column] != said:
            problems.append("%s: the note says the %s column holds %s, where it holds %s"
                            % (key, column, said, data_row[column]))
    return problems


def judge(reading, value, places):
    """One output row for one value, and the problems it raises: a finding, a note or a count that needs a cell the
    reading does not hold once, or whose words the reading no longer bears out, is one of them."""
    name, series, measure, level, sex, kind, recorded, data_row = value
    row = {"file": name, "series": series, "measure": measure, "level": level, "sex": sex, "kind": kind,
           "value": recorded, "paper": SOURCES[(name, series, measure)][0], "printed_as": "", "where": "",
           "legibility": "", "result": "", "sd_printed": "", "n": data_row["n"], "n_printed": "", "finding": "",
           "reproduced_by": "", "note": ""}
    try:
        return row, compare(reading, value, places, row)
    except (LookupError, Untrue, ValueError, ArithmeticError) as failed:
        return row, ["%s: %s" % ((series, measure, level, sex, kind), failed)]


def compare(reading, value, places, row):
    """Fill one value's output row from the reading and give the problems it raises."""
    name, series, measure, level, sex, kind, recorded, data_row = value
    paper, labels = SOURCES[(name, series, measure)]
    key = (series, measure, level, sex, kind)
    finding, terms = FINDINGS.get(key, ("", None))
    row["finding"] = finding(reading) if callable(finding) else finding
    note = NOTES.get(key, "")
    row["note"] = note(reading) if callable(note) else note
    problems = data_unsaid(reading, (name, series, measure), data_row, key) if key in NOTES else []
    if (name, series, measure) in COUNTS:
        count, other = count_of(reading, (name, series, measure), level, sex)
        row["n_printed"] = count["value"]
        if count["value"] != data_row["n"]:
            row["note"] = ". ".join(s for s in (row["note"], count_said(data_row["n"], count, other, sex)) if s)
    found = [] if labels is None else cells(reading, paper, labels, level, sex, kind)
    if labels is not None and len(found) != 1:
        return problems + ["%s: the selector picks %d cells" % (key, len(found))]
    if found and not found[0]["value"]:
        return problems + ["%s: the selector picks a cell with no value" % (key,)]
    if found:
        c = found[0]
        row.update(printed_as=c["printed_as"], legibility=c["legibility"], where=where_of(paper, c))
        row["result"] = "agrees" if rounds_to(recorded, in_data_units(paper, c["value"]), places) else "differs"
        if kind == "mean" and not data_row["sd"]:
            sd = cells(reading, paper, labels, level, sex, "sd")
            if len(sd) != (0 if (name, series, measure) in MEANS_ONLY else 1):
                problems.append("%s: the selector picks %d SD cells" % (key, len(sd)))
            elif sd:
                row["sd_printed"] = str(in_data_units(paper, sd[0]["value"]))
    else:
        row["result"] = "not printed"
    if row["result"] == "agrees":
        if row["finding"]:
            problems.append("%s: agrees, yet FINDINGS explains a difference" % (key,))
    elif not row["finding"]:
        problems.append("%s: %s, and FINDINGS does not explain it" % (key, row["result"]))
    elif not terms:
        problems.append("%s: %s, and its finding names no calculation that reproduces it" % (key, row["result"]))
    else:
        number, where = reproduce(reading, terms, sex, kind)
        row["reproduced_by"] = "%s (%s)" % (format(number.normalize(), "f"), where)
        if not rounds_to(recorded, number, places):
            problems.append("%s: the finding's calculation gives %s, not %s" % (key, number, recorded))
    return problems


NUMBER = re.compile(r"\d+(?:[.,]\d+)*")

# Numbers spelled in English words, as Eisenstein prints most of his counts: "seventy-eight", "Four hundred and
# forty-three". An "and" is read only after a hundred or a thousand, so "five and six" is two numbers, not eleven.
UNIT_WORDS = "one two three four five six seven eight nine".split()
TEEN_WORDS = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TEN_WORDS = "twenty thirty forty fifty sixty seventy eighty ninety".split()
WORD_VALUE = {word: value for words, first, step in ((UNIT_WORDS, 1, 1), (TEEN_WORDS, 10, 1), (TEN_WORDS, 20, 10))
              for word, value in zip(words, range(first, 100, step))}


def one_of(words):
    return "(?:%s)" % "|".join(words)


BELOW_HUNDRED = r"(?:%s(?:-%s)?|%s|%s)" % (one_of(TEN_WORDS), one_of(UNIT_WORDS), one_of(TEEN_WORDS),
                                          one_of(UNIT_WORDS))
BELOW_THOUSAND = r"(?:%s\s+hundred(?:\s+and\s+%s)?|%s)" % (one_of(UNIT_WORDS), BELOW_HUNDRED, BELOW_HUNDRED)
SPELLED = re.compile(r"\b(?:%s\s+thousand(?:\s+(?:and\s+)?%s)?|%s)\b" % (BELOW_THOUSAND, BELOW_THOUSAND,
                                                                      BELOW_THOUSAND), re.IGNORECASE)


def spelled_value(words):
    """The number some English words spell, as SPELLED matches them: "Four hundred and forty-three" is 443."""
    total = current = 0
    for word in re.split(r"[\s-]+", words.lower()):
        if word == "hundred":
            current *= 100
        elif word == "thousand":
            total, current = total + current * 1000, 0
        elif word != "and":
            current += WORD_VALUE[word]
    return total + current


def printed_numbers(text):
    """Every number a printed cell shows, a comma read both as a decimal comma and as a thousands separator, and every
    number it spells in words. A minus sign directly before a number is its sign only with no digit, slash or closing
    bracket before it, so that the dash of a range and the minus of +/- are not."""
    found = {Decimal(spelled_value(match.group())) for match in SPELLED.finditer(text)}
    for match in NUMBER.finditer(text):
        sign_at = match.start() - 1
        before = text[sign_at - 1] if sign_at >= 1 else ""
        negative = sign_at >= 0 and text[sign_at] == "-" and not (before.isdigit() or before in ("/", ")"))
        for spelled in {match.group().replace(",", ""), match.group().replace(",", ".")}:
            try:
                number = Decimal(spelled)
            except InvalidOperation:
                continue
            found.add(-number if negative else number)
    return found


def a_number(text):
    try:
        return Decimal(text).is_finite()
    except InvalidOperation:
        return False


def unprinted(reading):
    """The rows of the reading whose value is not a number their printed_as shows."""
    return ["reading row %d (%s %s, %s): the value %s is not printed in %r" % (i, r["paper"], r["table"],
                                                                          r["row_label"], r["value"], r["printed_as"])
            for i, r in enumerate(reading, start=2)
            if r["value"] and not (a_number(r["value"]) and Decimal(r["value"]) in printed_numbers(r["printed_as"]))]


def miscounted(out):
    """The series whose count of values here is not the one VALUES holds."""
    have = {}
    for o in out:
        have[(o["file"], o["series"], o["measure"])] = have.get((o["file"], o["series"], o["measure"]), 0) + 1
    return ["%s: %d values here, where VALUES holds %d" % (key, have.get(key, 0), VALUES.get(key, 0))
            for key in sorted(set(have) | set(VALUES) | set(SOURCES)) if have.get(key, 0) != VALUES.get(key, 0)]


def main(argv):
    reading = list(csv.DictReader(READING.read_text(encoding="ascii").splitlines()))
    out, problems = [], unprinted(reading)
    every = values()
    most = most_decimals(every)
    for value in every:
        name, series, measure, _, _, kind, _, _ = value
        row, found = judge(reading, value, most[(name, series, measure, kind)])
        out.append(row)
        problems += found
    problems += miscounted(out)
    here = {(o["series"], o["measure"], o["level"], o["sex"], o["kind"]) for o in out}
    problems += ["%s: a finding or note for a value not here" % (k,)
                 for k in sorted((set(FINDINGS) | set(NOTES)) - here)]

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
    other_n = sum(1 for o in out if o["n_printed"] and o["n_printed"] != o["n"])
    print(f"{other_n:4d}  values whose n_printed, the count of people the paper prints for them, is not their n "
          f"(the six series COUNTS names)")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
