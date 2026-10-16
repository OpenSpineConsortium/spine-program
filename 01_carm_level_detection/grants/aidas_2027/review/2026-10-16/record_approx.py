"""Record issue #112 in RECORD.md and README.md: the approximations and line C3."""
import sys
import textwrap
from pathlib import Path

folder = Path(sys.argv[1])


def swap(path, old, new):
    text = path.read_text()
    if text.count(old) != 1:
        sys.exit(f"{path.name}: {text.count(old)} matches for {old[:70]!r}")
    path.write_text(text.replace(old, new))


def wrap(paragraph, indent=""):
    return textwrap.fill(paragraph, width=118, subsequent_indent=indent, break_on_hyphens=False,
                         break_long_words=False)


record = folder / "RECORD.md"
section3 = wrap(
    "Since issue #112 (2026-10-16) the packet prints none of these marks: at the owner's word (\"I want all of those "
    "to-do or fill-ins replaced by approximations\") each became an approximation, and `APPROXIMATIONS.md` lists them "
    "with their basis and who can confirm each. The list below is the record of what the marks asked.")
swap(record, "## 3. What only the team can supply (the red [DATA NEEDED] marks)\n\n",
     "## 3. What only the team can supply (the red [DATA NEEDED] marks)\n\n" + section3 + "\n\n")

bullet = wrap(
    "- **Approximations and line C3 (issue #112).** The owner, 2026-10-16: \"I want all of those to-do or fill-ins "
    "replaced by approximations, and I want to budget for $1,500 of reimbursements of Claude subscriptions that I've "
    "used in my personal funds to prepare this project. Also, keep track of all these to-dos so that I can follow up "
    "with more realistic values. And you could stop doing adversarial reviews on this repo at this point.\" Every red "
    "mark became an approximation, listed with its basis in `APPROXIMATIONS.md`. Line C3 reimburses $1,500 of Claude "
    "subscriptions bought in 2026; since the call says external collaborators \"may not receive award funds\" and the "
    "award year starts January 1, 2027, the packet pays it once the clinical collaborator's pending appointment as WSU "
    "adjunct faculty begins and calls it computing bought before the award year, and the cover says the collaborator "
    "receives only line C3. To stay within the call's $20,000, line A fell from 520 to 515 hours (Aim 2 from 160 to "
    "155): A $7,725, A2 $591, total $19,987; at $18 an hour the total would be $21,650 unless the hours fell to 429; "
    "lines A, A2, C1 and C2 come to $10,196; without B the request is $14,768, without B and D $11,768, without B, D "
    "and F $11,696. The PI's contact line labels its second number \"cell\" in the private `contacts.tex`. No "
    "adversarial review ran, at the owner's word. 10 pages with the real and the example contact lines, no overfull "
    "line, and no red mark in the build with the real ones.", indent="  ")
swap(record, "\n\n## 5. The execution skeleton", "\n" + bullet + "\n\n## 5. The execution skeleton")

readme = folder / "README.md"
swap(readme, "Schwing (General Surgery); $18,568 for January to December 2027;",
     "Schwing (General Surgery); $19,987 for January to December 2027;")
swap(readme, "| `RECORD.md` | the file behind every number,",
     "| `APPROXIMATIONS.md` | since issue #112, every value that stands in for one the team has not confirmed, with "
     "its basis and who can confirm it |\n| `RECORD.md` | the file behind every number,")
swap(readme,
     "1. Fill each red [DATA NEEDED] mark; `RECORD.md` section 3 lists them, and section 2 links every value taken from the\n"
     "   web, most of them from search excerpts that need a click-through.",
     "1. Replace each approximation with a confirmed value; `APPROXIMATIONS.md` lists them, `RECORD.md` section 3 the red\n"
     "   marks they replaced, and section 2 links every value taken from the web, most of them from search excerpts that\n"
     "   need a click-through.")
swap(readme, "whether lines B (the cadaver set), D (the FDA Pre-Submission consultant) and F (the poster)\n"
     "   are allowable and how line A may be hired;",
     "whether lines B (the cadaver set), C3 (the reimbursement), D (the FDA Pre-Submission consultant)\n"
     "   and F (the poster) are allowable and how line A may be hired;")
swap(readme, "the packet shows SchwingNet's architecture and quotes its\n   held-out results.",
     "the packet quotes SchwingNet's held-out results and draws\n   them in Figure 1f.")
print("recorded")
