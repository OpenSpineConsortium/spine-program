"""How far the published series disagree with one another, level by level.

    python3 code/spread.py            # from synthetic_spine/; standard library only; writes verification/spread.csv
    python3 code/spread.py --check    # exit 1 when verification/spread.csv is not what the tables give

For every measure and level, every row's mean at that level is one point: a series split by sex gives two points,
an unsplit series one. The spread is (largest - smallest) / median of those points, in percent. Pedicle width joins
data/pedicle_width_references.csv (PDW) to the two Panjabi thoracic rows in data/level_references.csv (pedicle).

verification/spread.csv has one line per measure and level; the summary printed at the end (one line per measure:
the most series at any level, and the range of the spread over the levels three or more series reach) is what
README.md quotes.
"""
import csv
import io
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
OUT = HERE / "verification" / "spread.csv"
NAMES = {"h_ant": "anterior body height", "h_post": "posterior body height", "endplate": "upper end-plate width",
         "canal_w": "canal width", "canal_ap": "canal depth", "disc": "disc height", "pedicle": "pedicle width"}
ORDER = ["h_ant", "h_post", "endplate", "canal_w", "canal_ap", "disc", "pedicle"]


def rows_of(name):
    lines = [l for l in (DATA / name).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def level_key(level):
    return ("CTLS".index(level[0]), int("".join(ch for ch in level[1:3] if ch.isdigit())), level)


def table():
    points = defaultdict(list)
    for name in ("level_references.csv", "pedicle_width_references.csv"):
        for r in rows_of(name):
            measure = "pedicle" if r["measure"] == "PDW" else r["measure"]
            points[(measure, r["level"])].append((r["series"], float(r["mean"])))
    out = []
    for measure in ORDER:
        for level in sorted({l for m, l in points if m == measure}, key=level_key):
            pts = points[(measure, level)]
            means = [v for _, v in pts]
            med = statistics.median(means)
            out.append({"measure": measure, "level": level, "series": len({s for s, _ in pts}), "rows": len(pts),
                        "smallest": f"{min(means):.2f}", "median": f"{med:.2f}", "largest": f"{max(means):.2f}",
                        "spread_percent": f"{100 * (max(means) - min(means)) / med:.0f}"})
    return out


def rendered(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main(argv):
    rows = table()
    text = rendered(rows)
    if "--check" in argv:
        same = OUT.exists() and OUT.read_bytes() == text.encode("ascii")
        print("verification/spread.csv is what the tables give" if same else "verification/spread.csv is stale: rerun code/spread.py")
        return 0 if same else 1
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_bytes(text.encode("ascii"))
    for measure in ORDER:
        mine = [r for r in rows if r["measure"] == measure]
        reach = [int(r["spread_percent"]) for r in mine if r["series"] >= 3]
        most = max(r["series"] for r in mine)
        span = f"{min(reach)}-{max(reach)}%" if reach else "fewer than three series at every level"
        print(f"| {NAMES[measure]} ({most}) | {span} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
