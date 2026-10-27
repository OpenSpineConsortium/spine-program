"""Panjabi's values in every table here against a blind reading of his printed tables.

    python3 code/check_page_reading.py            # from synthetic_spine/; standard library only, no network
    python3 code/check_page_reading.py --check    # write nothing; exit 1 also when the committed result is stale

Panjabi's 1991 and 1992 papers are scans with no text layer, so code/verify_tables.py cannot read them.
verification/panjabi_page_reading.csv is a transcription of their tables made from the page images by a reader who
was not shown any of the tables here; it keeps each cell as printed (printed_as) and where it is (table, page).

Every Panjabi row in data/level_references.csv, data/pedicle_width_references.csv, data/panjabi_reference.csv and
data/panjabi_full_spine.csv is compared with it. Pedicle width in those tables is the mean of the right and left
widths (PDWr, PDWl) with the two standard errors averaged; it is recomputed from the reading and rounded half up to
the decimals the table records. Writes verification/panjabi_page_reading_check.csv; exit 1 on any disagreement.
"""
import csv
import io
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
READING = HERE / "verification" / "panjabi_page_reading.csv"
OUT = HERE / "verification" / "panjabi_page_reading_check.csv"
MEASURE = {"VBHp": "h_post", "EPWu": "endplate", "SCW": "canal_w", "SCD": "canal_ap"}


def rows_of(name):
    lines = [l for l in (DATA / name).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def decimals(text):
    return len(text.split(".")[1]) if "." in text else 0


def reading():
    """(measure, level) -> (mean, dispersion, where) from the page reading, pedicle width derived."""
    got, sides = {}, {}
    for r in csv.DictReader(READING.read_text(encoding="ascii").splitlines()):
        if not r["mean"].replace(".", "", 1).isdigit():
            continue        # a cell the paper prints as a dash (C2 has no upper end-plate): no value to compare
        where = f"{r['paper']} {r['table']} p. {r['journal_page']}"
        if r["measure"] in MEASURE:
            got[(MEASURE[r["measure"]], r["level"])] = (r["mean"], r["dispersion"], where)
        elif r["measure"] in ("PDWr", "PDWl"):
            sides.setdefault(r["level"], {})[r["measure"]] = (r["mean"], r["dispersion"], where)
    for level, s in sides.items():
        if len(s) == 2:
            (mr, dr, w), (ml, dl, _) = s["PDWr"], s["PDWl"]
            mean = (Decimal(mr) + Decimal(ml)) / 2
            disp = (Decimal(dr) + Decimal(dl)) / 2 if dr and dl else None
            got[("pedicle", level)] = (mean, disp, w + ", mean of PDWr and PDWl")
    return got


def agrees(recorded, read):
    """A recorded value agrees with the reading when the reading, rounded half up to the recorded decimals, equals it."""
    if read is None or read == "":
        return None
    q = Decimal(1).scaleb(-decimals(recorded))
    return Decimal(str(read)).quantize(q, rounding=ROUND_HALF_UP) == Decimal(recorded).quantize(q)


def main(argv):
    read = reading()
    tables = []
    for r in rows_of("level_references.csv"):
        if r["series"] == "Panjabi 1992":
            tables.append(("level_references.csv", r["measure"], r["level"], r["mean"], r["sd"]))
    for r in rows_of("pedicle_width_references.csv"):
        if r["series"] == "Panjabi":
            tables.append(("pedicle_width_references.csv", "pedicle", r["level"], r["mean"], r["sd"]))
    for name in ("panjabi_reference.csv", "panjabi_full_spine.csv"):
        for r in rows_of(name):
            tables.append((name, r["measure"], r["level"], r["mean"], r["sem"]))

    out, bad = [], 0
    for name, measure, level, mean, disp in tables:
        key = ("pedicle" if measure == "PDW" else measure, level)
        if key not in read:
            out.append({"file": name, "measure": measure, "level": level, "mean": mean, "sem": disp,
                        "read_mean": "", "read_sem": "", "where": "", "result": "not in the page reading"})
            continue
        rm, rd, where = read[key]
        mean_ok, disp_ok = agrees(mean, rm), agrees(disp, rd) if disp else None
        if mean_ok is False or disp_ok is False:
            result = "DISAGREES: " + ", ".join(x for x, ok in (("mean", mean_ok), ("SEM", disp_ok)) if ok is False)
            bad += 1
        elif disp and disp_ok is None:
            result = "mean agrees; the page reading has no SEM for it"
        else:
            result = "agrees"
        out.append({"file": name, "measure": measure, "level": level, "mean": mean, "sem": disp,
                    "read_mean": str(rm), "read_sem": "" if rd is None else str(rd), "where": where, "result": result})

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(out[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(out)
    if "--check" in argv:
        if not OUT.exists() or OUT.read_bytes() != buf.getvalue().encode("ascii"):
            print("verification/panjabi_page_reading_check.csv is stale: rerun code/check_page_reading.py")
            bad += 1
    else:
        OUT.write_bytes(buf.getvalue().encode("ascii"))
    counts = {}
    for o in out:
        counts[o["result"]] = counts.get(o["result"], 0) + 1
    for k, v in sorted(counts.items()):
        print(f"{v:4d}  {k}")
    for o in out:
        if o["result"].startswith("DISAGREES"):
            print(f"  {o['file']} {o['measure']} {o['level']}: {o['mean']} +/- {o['sem']}, read {o['read_mean']} +/- {o['read_sem']} ({o['where']})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
