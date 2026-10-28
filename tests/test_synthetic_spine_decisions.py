"""synthetic_spine/code/apply_decisions.py, which writes the copied tables again under data/corrected/ with the
decisions #239 left open applied, and verification/decisions.csv beside them.

Each way the script refuses is planted and must fail: a copy that is not the one the decisions were made on, a
written file that is stale, a reading value its printed_as does not print, a cell that no longer holds what a
decision is held to, a decision that sets a field to what it holds or one another decision set, a selector that
picks the wrong number of rows, and two rows with one key. The faults that touch files are planted in a scratch copy
of synthetic_spine/, run as its own process, so the clone is never written."""

import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "synthetic_spine"
sys.path.insert(0, str(FOLDER / "code"))

import apply_decisions  # noqa: E402


def run(folder, *args):
    done = subprocess.run([sys.executable, "code/apply_decisions.py", *args], cwd=folder, capture_output=True,
                          text=True)
    return done.returncode, done.stdout + done.stderr


def replace_once(path, old, new):
    text = path.read_text(encoding="ascii")
    if text.count(old) != 1:
        raise AssertionError("%r is in %s %d times, not once" % (old, path, text.count(old)))
    path.write_text(text.replace(old, new), encoding="ascii")


class Planted(unittest.TestCase):
    """Faults planted in a scratch copy of the folder, with its written files current to begin with."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.folder = Path(self.scratch.name) / "synthetic_spine"
        shutil.copytree(FOLDER, self.folder, ignore=shutil.ignore_patterns("__pycache__"))
        code, out = run(self.folder)
        self.assertEqual(code, 0, out)

    def tearDown(self):
        self.scratch.cleanup()

    def test_the_written_files_pass_their_check(self):
        code, out = run(self.folder, "--check")
        self.assertEqual(code, 0, out)

    def test_a_copy_taken_again_is_refused(self):
        with open(self.folder / "data" / "pedicle_width_references.csv", "a", encoding="ascii") as copy:
            copy.write("Somebody,2027,cadaveric,1,direct,PDW,L1,9.00,,none,primary,Somebody 2027\n")
        code, out = run(self.folder, "--check")
        self.assertEqual(code, 1)
        self.assertIn("is not the copy the decisions were made on", out)

    def test_a_stale_corrected_table_fails_the_check(self):
        replace_once(self.folder / "data" / "corrected" / "level_references.csv", "59 films", "59")
        code, out = run(self.folder, "--check")
        self.assertEqual(code, 1)
        self.assertIn("level_references.csv is stale", out)

    def test_a_stale_record_fails_the_check(self):
        record = self.folder / "verification" / "decisions.csv"
        record.write_text(record.read_text(encoding="ascii")[:-200], encoding="ascii")
        code, out = run(self.folder, "--check")
        self.assertEqual(code, 1)
        self.assertIn("decisions.csv is stale", out)

    def test_a_reading_value_its_cell_does_not_print_fails(self):
        replace_once(self.folder / "verification" / "open_questions_reading.csv", ",6.87,", ",6.78,")
        code, out = run(self.folder, "--check")
        self.assertEqual(code, 1)
        self.assertIn("is not printed in", out)

    def test_a_kept_misprint_no_longer_printed_is_refused(self):
        replace_once(self.folder / "verification" / "open_questions_reading.csv", "10.17 +/- 6.87,6.87,",
                     "10.17 +/- 1.87,1.87,")
        code, out = run(self.folder, "--check")
        self.assertEqual(code, 1)
        self.assertIn("does not print the copy's 6.87", out)

    def test_a_combined_sd_that_misses_the_printed_widths_is_refused(self):
        reading = self.folder / "verification" / "open_questions_reading.csv"
        with open(reading, newline="", encoding="ascii") as f:
            rows = list(csv.DictReader(f))
        width_sd = [r for r in rows if r["paper"] == "cizmic2023" and r["row_label"] == "L1 IPD canal"
                    and r["sex"] == "male" and r["statistic"] == "sd"]
        self.assertEqual(len(width_sd), 1)
        width_sd[0].update(printed_as="9", value="9")
        with open(reading, "w", newline="", encoding="ascii") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        code, out = run(self.folder, "--check")
        self.assertEqual(code, 1)
        self.assertIn("is not the", out)


class Refusals(unittest.TestCase):
    """The decisions' own guards, on the clone's tables and readings, which none of these writes."""

    def setUp(self):
        reading = (apply_decisions.reading_rows(apply_decisions.closed.READING)
                   + apply_decisions.reading_rows(apply_decisions.OPEN_READING))
        self.d = apply_decisions.Decisions(reading)

    def row(self, series, level):
        return self.d.rows(apply_decisions.PEDICLES, 1, series=series, level=level)[0]

    def test_every_decision_applies_to_the_clone(self):
        for decide in apply_decisions.DECIDE:
            decide(self.d)
        self.assertEqual(apply_decisions.collisions(self.d), [])

    def test_a_field_set_to_what_it_holds_is_refused(self):
        row = self.row("Hou", "L1")
        with self.assertRaises(apply_decisions.Refused):
            self.d.put(9, apply_decisions.PEDICLES, row, "n", row["n"], "here", "no change")

    def test_a_field_two_decisions_set_is_refused(self):
        row = self.row("Hou", "L1")
        self.d.put(8, apply_decisions.PEDICLES, row, "n", "41", "here", "first")
        with self.assertRaises(apply_decisions.Refused):
            self.d.put(9, apply_decisions.PEDICLES, row, "n", "42", "here", "second")

    def test_a_selector_that_picks_other_than_its_rows_is_refused(self):
        with self.assertRaises(apply_decisions.Refused):
            self.d.rows(apply_decisions.PEDICLES, 4, series="Hou")

    def test_a_row_added_twice_is_refused(self):
        like = self.row("Hou", "L1")
        with self.assertRaises(apply_decisions.Refused):
            self.d.add(9, apply_decisions.PEDICLES, like, {"mean": "7.10"}, "a row with the key of another")

    def test_two_rows_with_one_key_are_reported(self):
        table = self.d.tables[apply_decisions.PEDICLES]
        table.rows.append(dict(table.rows[-1]))
        self.assertEqual(len(apply_decisions.collisions(self.d)), 1)

    def test_a_series_made_primary_is_held_to_its_page(self):
        row = self.row("Olsewski", "L3")
        row["mean"] = "10.30"
        with self.assertRaises(apply_decisions.Untrue):
            apply_decisions.olsewski(self.d)


if __name__ == "__main__":
    unittest.main()
