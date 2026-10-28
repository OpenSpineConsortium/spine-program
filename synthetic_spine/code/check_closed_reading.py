"""The values here from fifteen closed papers against a blind reading of those papers' printed tables.

    python3 code/check_closed_reading.py            # from synthetic_spine/; standard library only, no network
    python3 code/check_closed_reading.py --check    # write nothing; exit 1 also when the committed result is stale

A closed paper, here, is one whose full text no script of this folder may read: 203 values in
data/level_references.csv and data/pedicle_width_references.csv come from fifteen of them, and
verification/values.csv could check only 26 of those, in an abstract. greg supplied ten as PDFs on 28 October 2026;
another thread of the project fetched the other five the same day from their publishers' own free copies (Griffith
2016, Twomey 1985, Alonge 2021, Ahmed 2019, Chaudhary 2015). None is committed. verification/closed_page_reading.csv is
a transcription of their tables made from the page images by readers who were not shown any of the tables here, as
Panjabi's were read (code/check_page_reading.py): one row per printed cell and statistic, with the cell as printed
(printed_as) and where it is (table, pdf_page, journal_page). For the nine typeset papers (Mitra 2002, Robertson
2000, Yu 2015, Tang 2016, Bach 2019, Griffith, Alonge, Ahmed and Chaudhary) every value read from a table or the
text was also found on the publisher's own text layer; the data labels read from figures are pictures and have no
text layer. A few rows, counts of people and three of Yu's widths from the text, were added after the blind
reading, and each says so in its note.

SOURCES names, for each series, the cells of its own paper that its values should be, as the reading labels them. A
value agrees when its cell, rounded half up to the decimals the table records, equals it. FINDINGS says, for each
value that does not, what the paper prints instead and the calculation, or the other paper's table, that reproduces
the value, which is then held to it like a cell. NOTES records what a reader of an agreeing value should still know.
Every number a finding or a note gives from a paper is computed from the reading, not typed. COUNTS names the cell
that counts the people a value is of, where the paper prints one: n_printed beside the data's n. SCALE turns a
paper's printed unit into the data's: Tang prints centimetres. VALUES holds how many values each series has here.
The script writes verification/closed_page_reading_check.csv and exits 1 on a value that neither agrees nor has a
finding, on a finding with no calculation or whose calculation no longer reproduces its value, on a finding or a
note for a value that is not here, on a selector that picks other than one cell (or other than one SD cell beside a
mean the data gives no SD for, where the paper prints SDs), on a series with another count of values than VALUES
holds, and on a row of the reading whose value is not a number its printed_as prints.
"""
import csv
import io
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
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
    (LEVELS, "Eisenstein 1977", "canal_w"):
        ("chaudhary2015", {"table": "Table II", "group": "Eisenstein 1977. (South African Caucasoids)"}),
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

# The series whose cells are means with no SD printed beside them: Mitra's Table 1, Yu's Table 5 and Chaudhary's
# Table II, where Eisenstein's values are, print means only. Beside any other mean the data gives no SD for, the
# paper prints one, which the output shows (sd_printed).
MEANS_ONLY = {(PEDICLES, "Mitra", "PDW"), (PEDICLES, "Yu", "PDW"), (LEVELS, "Eisenstein 1977", "canal_w")}

# (data file, series, measure) -> (paper, the reading's labels of the cell that counts the people a value is of, and
# that cell's level, None where it is the value's own), for the series whose paper prints such a count. The sex is
# the value's own.
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


def mitra_direct(level):
    """Mitra's direct transverse diameter over all 20 cadavers: the 18 men's and the 2 women's means, weighted."""
    cell = {"table": "Table 1", "measure_label": "TD"}
    return [("mitra2002", dict(cell, group="CS direct M(18)", sex="male"), level, 18),
            ("mitra2002", dict(cell, group="CS direct F(2)", sex="female"), level, 2)]


KRAG_IN_YU = "Krag et al, American (N = 14-24)"
MITRA_IN_YU = "Mitra et al, Indian (N = 20)"


def plain(value):
    return format(value.normalize(), "f")


def krag_finding(reading):
    """What Krag prints in place of a mean width, from the reading: Table 2's bins and the widths the text gives."""
    bins = sorted({c["column_label"][:-len(" mm")] for c in reading if c["paper"] == "krag1988"
                   and c["table"] == "Table 2" and c["column_label"].endswith(" mm")},
                  key=lambda b: Decimal(b.split("-")[0]))
    text = {"table": "Text: Results", "measure_label": "pedicle diameter (Figure 5)"}
    upper, lower = (one_cell(reading, "krag1988", text, level, "all", "approximately") for level in ("L1", "L5"))
    zero = one_cell(reading, "krag1988", dict(text, measure_label="pedicle diameter perpendicular to the 0 deg axis"),
                    "L5", "all", "mean")
    in_yu = one_cell(reading, "yu2015", yu_table5(KRAG_IN_YU, "L5")[0][1], "L5", "all", "mean")
    return ("Krag prints no table of mean widths: Table 2 (p. 30) counts pedicles in bins of 1 mm from %s mm and a "
            "top bin of %s to %s mm, the figures plot means with no printed values, and the text gives about %s mm "
            "from T9 to L1 and about %s mm at L5 (p. %s), and %s mm at L5 by the 0 deg method (p. %s), below the %s at "
            "L5 here. The five values are Yu 2015's Table 5 row for Krag et al (p. %s), where the series was evidently "
            "read; how Yu came by them is not said"
            % (bins[0].split("-")[0], *bins[-1].split("-"), upper["value"], lower["value"], lower["journal_page"],
               zero["value"], zero["journal_page"], in_yu["value"], in_yu["journal_page"]))


def mitra_finding(reading, level):
    """What Mitra prints at L2 to L4, and how the series' value is had from it, from the reading."""
    men = one_cell(reading, "mitra2002", SOURCES[(PEDICLES, "Mitra", "PDW")][1], level, "all", "mean")
    in_yu = one_cell(reading, "yu2015", yu_table5(MITRA_IN_YU, level)[0][1], level, "all", "mean")
    direct, _ = reproduce(reading, mitra_direct(level), "all", "mean")
    return ("Table 1 (p. %s) prints %s for the 18 men measured directly. The value is the mean of the CT rows over "
            "all 20 cadavers, 18 men and 2 women weighted; L1 and L5 are the men's direct means, which the abstract "
            "quotes, so the series mixes two methods. Yu 2015's Table 5 (p. %s) prints %s under Mitra's name, the "
            "direct means over all 20 (%s)" % (men["journal_page"], men["printed_as"], in_yu["journal_page"],
                                               in_yu["value"], plain(direct)))


def mitra_note(reading, level):
    """What Mitra's L1 and L5 are, beside its means over all 20 cadavers, from the reading."""
    in_yu = one_cell(reading, "yu2015", yu_table5(MITRA_IN_YU, level)[0][1], level, "all", "mean")
    direct, _ = reproduce(reading, mitra_direct(level), "all", "mean")
    ct, _ = reproduce(reading, mitra_ct(level), "all", "mean")
    return ("The value is the 18 men's direct mean, which the abstract quotes; the n column's 20 counts the 2 women "
            "too. Over all 20 cadavers the direct means give %s and the CT means %s; L2 to L4 are the CT means over "
            "all 20, so the series mixes two methods and two groups. Yu 2015's Table 5 (p. %s) prints %s under "
            "Mitra's name, the direct mean over all 20" % (plain(direct), plain(ct), in_yu["journal_page"],
                                                         in_yu["value"]))


def yu_finding(reading, level):
    """What Yu prints as its own means, and where the series' value comes from instead, from the reading."""
    own = [one_cell(reading, "yu2015", SOURCES[(PEDICLES, "Yu", "PDW")][1], at, "all", "mean") for at in LUMBAR]
    pw = {"measure_label": "PW"}
    abstract = one_cell(reading, "yu2015", dict(pw, table="Abstract (text)"), "L5", "all", "mean")
    first, last = (one_cell(reading, "yu2015", dict(pw, table="Results (text)"), at, "all", "mean")
                   for at in ("L1", "L5"))
    oldest = one_cell(reading, "yu2015", dict(pw, table="Table 3", group="Age >=70 yr"), "L5", "all", "mean")
    young = one_cell(reading, "yu2015", yu_age_midpoint(level)[0][1], level, "all", "mean")
    middle, _ = reproduce(reading, yu_age_midpoint(level), "all", "mean")
    shown = middle.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    same = [c for c in reading if c["paper"] == "yu2015" and c["table"] != "Table 3" and c["measure_label"] == "PW"
            and c["level"] == level and c["statistic"] == "mean" and Decimal(c["value"]) == shown]
    extra = "".join(" as Yu's own, though %s's mean for the %s specimens is also %s" % (c["table"], c["group"],
                                                                                      c["value"]) for c in same)
    return ("Yu's own means, over 503 specimens with the two sides averaged, are printed %s, %s, %s, %s and %s (Table "
            "5, p. %s); the abstract gives %s at L5 (p. %s), and the Results %s at L1 and %s at L5 (p. %s). The "
            "series' value is printed nowhere in the paper%s. It is the midpoint of Table 3's means for the youngest "
            "age group (30 years or less) and for 50 to 69 years (p. %s), at all five levels. From L1 to L4 those two "
            "are the lowest and highest of the four age groups, which fits the table's citation, \"midpoint of "
            "published range\"; at L5 the oldest group's %s is higher still, and the same two groups were taken "
            "there too"
            % (*(c["value"] for c in own), own[0]["journal_page"], abstract["value"], abstract["journal_page"],
               first["value"], last["value"], first["journal_page"], extra, young["journal_page"], oldest["value"]))


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


def robertson_note(reading, level):
    """Which side and which width Robertson's series is, and its isthmus row beside it, from the reading."""
    cell = {"table": "Table 1", "side": "left"}
    isthmus, axis = (one_cell(reading, "robertson2000", dict(cell, measure_label=m), level, "all", "mean")
                     for m in ("Isthmus", "Axis"))
    return ("The left side only, as Table 1 (p. %s) prints it; the table does not say whose left, and the captions of "
            "Figures 3 and 4 give left and right as viewed by the reader (p. 710). Robertson's width is the "
            "medial-to-lateral extent of the wire drawn tight around the pedicle's isthmus, on its outer cortex, on "
            "the coaxial radiograph (pp. 709-710): the transverse width at the isthmus. Its isthmus diameter, %s on "
            "the left here, is the short axis of the pedicle's ellipse at the isthmus, whose long axis lies %s deg "
            "from the vertical at this level; the paper puts the gap between the two at L4 and L5 down to that tilt "
            "(p. %s)"
            % (isthmus["journal_page"], isthmus["printed_as"], axis["value"], axis["journal_page"]))


def tang_note(reading, level, disc):
    """What Tang's cell measures, and why its N is below the study's, from the reading."""
    subjects = {"table": "Methods (text)", "measure_label": "Subjects"}
    everyone, women, men = (one_cell(reading, "tang2016", subjects, "", sex, "n") for sex in ("all", "F", "M"))
    left_out = one_cell(reading, "tang2016", {"table": "Methods (text)", "measure_label": "IVDs of Pfirrmann grade "
                                              "V, excluded"}, disc, "M", "n")
    counted = [one_cell(reading, "tang2016", COUNTS[(LEVELS, "Tang 2016", "endplate")][1], level, sex, "n")
               for sex in ("F", "M")]
    return ("Tang prints centimetres and the data holds millimetres, so the cell is read times 10. FD_CaEP is the "
            "frontal diameter, the right-to-left extent, of the caudal end plate of the %s disc, which is %s's upper "
            "end plate. The study's %s subjects are %s women and %s men, and the %s men's discs of Pfirrmann grade V "
            "at %s were left out with their end plates (p. %s): Table 4 counts %s women and %s men here (p. %s)"
            % (disc, level, everyone["value"], women["value"], men["value"], left_out["value"], disc,
               everyone["journal_page"], counted[0]["value"], counted[1]["value"], counted[0]["journal_page"]))

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


def at_top_of_rounding(reading, terms, sex):
    """The weighted mean of the cells a calculation names, each taken at the top of its own printed rounding."""
    total, weights = Decimal(0), 0
    for paper, labels, level, weight in terms:
        value = one_cell(reading, paper, labels, level, sex, "mean")["value"]
        total += (Decimal(value) + Decimal(5).scaleb(-decimals(value) - 1)) * weight
        weights += weight
    return total / weights


def rounding_said(printed, pooled, top):
    """Nothing when the pooled mean rounds to the printed value; else how far the cells' own rounding reaches."""
    if rounds_to(printed, pooled):
        return ""
    shown = pooled.quantize(Decimal(1).scaleb(-decimals(printed)), rounding=ROUND_HALF_UP)
    reach = ("within" if rounds_to(printed, top) else "beyond")
    return (", which rounds to %s, not the printed %s; with each decade cell at the top of its own printed rounding "
            "they give %s, so the printed value is %s the cells' rounding" % (shown, printed, thousandths(top), reach))


def bach_note(reading, level, sex, kind):
    """What the Results' average is, beside Table 6's, and what its unnamed +/- is, computed from the reading."""
    who, table = BACH_SEX[sex]
    three = bach_decades(reading, "Average disc height", level, sex)
    if kind == "mean":
        pooled, _ = reproduce(reading, three, sex, "mean")
        printed = one_cell(reading, "bach2019", SOURCES[(LEVELS, "Bach 2019", "disc")][1], level, sex, "mean")
        a, p, t6 = (Decimal(one_cell(reading, "bach2019", {"table": "Table 6", "measure_label": m + " disc height"},
                                     level, sex, "mean")["value"]) for m in ("Anterior", "Posterior", "Average"))
        return ("Printed in the Results (p. e108) and the abstract (p. e106): the mean of the anterior, middle and "
                "posterior heights over all ages, which %s's decade rows of that mean, weighted by Table 1's counts, "
                "give as %s%s. Table 6's 'Average disc height' for all ages is another quantity, %s, the mean of its "
                "anterior and posterior rows alone, (%s + %s) / 2 = %s"
                % (table, thousandths(pooled),
                   rounding_said(printed["value"], pooled, at_top_of_rounding(reading, three, sex)),
                   t6, a, p, format((a + p) / 2, "f")))
    return ("The Results and the abstract do not say what this +/- is. %s's decade rows of the mean of three, pooled "
            "as SDs with their means and Table 1's counts, give %s: the size of an SD over all the %s, not of an SE, "
            "which would be about a tenth of it" % (table, hundredths(pooled_sd(reading, three, sex)), who))


def twomey_note(reading, level, sex, kind):
    """What Twomey's Table 2 measures and counts, and its oddities at L1-L2, computed from the reading."""
    count = {"table": "Table 1", "measure_label": "number of cadavers"}
    every = [c for c in reading if c["paper"] == "twomey1985" and c["statistic"] == "n"
             and all(c[k] == v for k, v in count.items())]
    children = sum(int(c["value"]) for c in every if c["sex"] == "all")
    men = one_cell(reading, "twomey1985", dict(count, group="20-36"), "", "M", "n")
    women = one_cell(reading, "twomey1985", dict(count, group="18-35"), "", "F", "n")
    cell = one_cell(reading, "twomey1985", dict(TWOMEY, group="20-35"), level, sex, kind)
    said = ("Table 2's true average disc height, the area of the disc's median section divided by its "
            "antero-posterior diameter, for the group it heads 20-35 (p. %s). The n column's %d counts every "
            "cadaver of Table 1, of every age, %d of them children aged 0 to 12 with the sexes pooled. Table 2 "
            "prints no n; Table 1's young adults are %s men aged 20 to 36 and %s women aged 18 to 35 (p. %s). The "
            "paper names no population; its authors worked in Western Australia"
            % (cell["journal_page"], sum(int(c["value"]) for c in every), children, men["value"], women["value"],
               men["journal_page"]))
    if (level, sex, kind) == ("L1L2", "M", "sd"):
        said += ". The cell is printed %s, the SD with a decimal comma" % cell["printed_as"]
    if (level, sex) == ("L1L2", "F"):
        others = [Decimal(one_cell(reading, "twomey1985", dict(TWOMEY, group="20-35"), other, sex, "mean")["value"])
                  for other in ("L2L3", "L3L4", "L4L5", "L5S1")]
        old = one_cell(reading, "twomey1985", dict(TWOMEY, group="60+"), level, sex, "mean")["value"]
        said += (". The cell, %s, is printed clearly, yet its mean is below these women's other four levels (%s to "
                 "%s) and below the same level at 60 and over (%s)"
                 % (cell["printed_as"], min(others), max(others), old))
    return said


def eisenstein_note(reading, level):
    """Where the Eisenstein values come from, and the other group Chaudhary prints beside them."""
    zulu = one_cell(reading, "chaudhary2015", {"table": "Table II", "group": "Eisenstein 1977 (Zulus)"},
                    level, "M", "mean")["printed_as"]
    return ("Chaudhary's Table II (p. 35) prints these as Eisenstein's South African Caucasoid men; Eisenstein's own "
            "paper has not been read, so this checks Chaudhary's copy, not Eisenstein. The cohort column names both "
            "of Eisenstein's groups, but the values are the Caucasoid men's alone: the Zulu men's %s is another row. "
            "Chaudhary does not say how Eisenstein measured, so the modality is not checked" % zulu)


def chaudhary_range_note(reading, level):
    """The SD that Table I's range of mean +/- 3 SD implies, beside the SD it prints."""
    cell = {"table": "Table I", "measure_label": "Interpedicular distance (mm)"}
    low, high = (one_cell(reading, "chaudhary2015", cell, level, "M", k)["value"] for k in ("mean-3sd", "mean+3sd"))
    sd = one_cell(reading, "chaudhary2015", cell, level, "M", "sd")["value"]
    return ("Table I's range of mean +/- 3 SD, %s to %s (p. 34), gives an SD of %s, where its SD column prints %s; "
            "one of the two is misprinted, and the data holds the column's"
            % (low, high, format((Decimal(high) - Decimal(low)) / 6, "f"), sd))


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


def count_of(reading, key, level, sex):
    """The cell that counts the people of one sex a value is of, and that count for the other sex, where COUNTS names
    the cell; the other is None for a value of both sexes."""
    paper, labels, at = COUNTS[key]
    at = level if at is None else at
    other = OTHER_SEX.get(sex)
    return (one_cell(reading, paper, labels, at, sex, "n"),
            None if other is None else one_cell(reading, paper, labels, at, other, "n")["value"])


def count_said(data_n, count, other, sex):
    """The sentence a note gets when the data's n is not the count of the people its value is of."""
    where = "%s, p. %s" % (count["table"], count["journal_page"])
    if other is None:
        return "This cell's N is %s (%s), where the n column has %s" % (count["value"], where, data_n)
    if data_n == str(int(count["value"]) + int(other)):
        return "The n column's %s counts both sexes; the %s are %s (%s)" % (data_n, WHO[sex], count["value"], where)
    return "The n column has %s; the %s are %s (%s)" % (data_n, WHO[sex], count["value"], where)


def judge(reading, value):
    """One output row for one value, and the problems it raises."""
    name, series, measure, level, sex, kind, recorded, data_row = value
    paper, labels = SOURCES[(name, series, measure)]
    key = (series, measure, level, sex, kind)
    finding, terms = FINDINGS.get(key, ("", None))
    finding = finding(reading) if callable(finding) else finding
    note = NOTES.get(key, "")
    note = note(reading) if callable(note) else note
    row = {"file": name, "series": series, "measure": measure, "level": level, "sex": sex, "kind": kind,
           "value": recorded, "paper": paper, "printed_as": "", "where": "", "legibility": "", "result": "",
           "sd_printed": "", "n": data_row["n"], "n_printed": "", "finding": finding, "reproduced_by": "", "note": note}
    if (name, series, measure) in COUNTS:
        count, other = count_of(reading, (name, series, measure), level, sex)
        row["n_printed"] = count["value"]
        if count["value"] != data_row["n"]:
            row["note"] = ". ".join(s for s in (note, count_said(data_row["n"], count, other, sex)) if s)
    problems = []
    found = [] if labels is None else cells(reading, paper, labels, level, sex, kind)
    if labels is not None and len(found) != 1:
        return row, ["%s: the selector picks %d cells" % (key, len(found))]
    if found:
        c = found[0]
        row.update(printed_as=c["printed_as"], legibility=c["legibility"], where=where_of(paper, c))
        row["result"] = "agrees" if rounds_to(recorded, in_data_units(paper, c["value"])) else "differs"
        if kind == "mean" and not data_row["sd"]:
            sd = cells(reading, paper, labels, level, sex, "sd")
            if len(sd) != (0 if (name, series, measure) in MEANS_ONLY else 1):
                problems.append("%s: the selector picks %d SD cells" % (key, len(sd)))
            elif sd:
                row["sd_printed"] = str(in_data_units(paper, sd[0]["value"]))
    else:
        row["result"] = "not printed"
    if row["result"] == "agrees":
        if finding:
            problems.append("%s: agrees, yet FINDINGS explains a difference" % (key,))
    elif not finding:
        problems.append("%s: %s, and FINDINGS does not explain it" % (key, row["result"]))
    elif not terms:
        problems.append("%s: %s, and its finding names no calculation that reproduces it" % (key, row["result"]))
    else:
        number, where = reproduce(reading, terms, sex, kind)
        row["reproduced_by"] = "%s (%s)" % (format(number.normalize(), "f"), where)
        if not rounds_to(recorded, number):
            problems.append("%s: the finding's calculation gives %s, not %s" % (key, number, recorded))
    return row, problems


NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


def printed_numbers(text):
    """Every number a printed cell shows, either sign, a comma read both as a decimal comma and as a thousands
    separator."""
    found = set()
    for token in NUMBER.findall(text):
        for spelled in {token.replace(",", ""), token.replace(",", ".")}:
            found |= {Decimal(spelled), -Decimal(spelled)}
    return found


def unprinted(reading):
    """The rows of the reading whose value is not a number their printed_as shows."""
    return ["reading row %d (%s %s, %s): the value %s is not printed in %r" % (i, r["paper"], r["table"],
                                                                          r["row_label"], r["value"], r["printed_as"])
            for i, r in enumerate(reading, start=2)
            if r["value"] and Decimal(r["value"]) not in printed_numbers(r["printed_as"])]


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
    for value in values():
        row, found = judge(reading, value)
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
    print(f"{other_n:4d}  values whose n is not the count of people the paper prints for them (n_printed)")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
