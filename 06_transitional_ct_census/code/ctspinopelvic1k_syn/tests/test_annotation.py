# copied into spine-program/06_transitional_ct_census on 2026-10-08 from CTSpinoPelvic1K-Syn (local git, no remote) tests/test_annotation.py; commit 7098eb1 of 2026-06-11; this folder is the only copy. The banned word, where it occurred, is rewritten as origin.
"""Tests for the Pass-1 grading worklist + sheet validation."""
import csv
import json
from pathlib import Path

from ctspino_syn.annotation import (
    generate_grade_worklist, validate_grade_sheet, ALL_COLS,
)


def _make_splits(tmp: Path) -> Path:
    p = tmp / "splits_5fold.json"
    p.write_text(json.dumps({
        "schema_version": 6,
        "patient_subtypes": {"10": "normal", "22": "semisacralization",
                             "4": "ambiguous", "120": "lumb"},
        "patient_attrs": {
            "22": {"has_l6_any": False, "n_lumb_max": 5, "lstv_label": "SEMI_SACRAL",
                   "lstv_pelvic": "SEMI_SACRALIZATION", "lstv_vertebral": "", "n_records": 2},
            "120": {"has_l6_any": True, "n_lumb_max": 6, "lstv_label": "LUMBARIZATION",
                    "lstv_pelvic": "", "lstv_vertebral": "LUMBARIZATION", "n_records": 1},
        },
    }))
    return p


def test_worklist_excludes_normal_and_prefills(tmp_path):
    splits = _make_splits(tmp_path)
    out = tmp_path / "grade.csv"
    n = generate_grade_worklist(splits, out)
    assert n == 3                         # normal excluded
    rows = list(csv.DictReader(out.open(newline="")))
    assert {r["token"] for r in rows} == {"22", "4", "120"}
    assert set(rows[0].keys()) == set(ALL_COLS)
    by_tok = {r["token"]: r for r in rows}
    assert by_tok["120"]["has_l6"] in ("True", "true")   # prefilled context
    assert by_tok["120"]["castellvi_grade"] == ""        # blank to fill


def test_validate_catches_bad_values(tmp_path):
    splits = _make_splits(tmp_path)
    out = tmp_path / "grade.csv"
    generate_grade_worklist(splits, out)
    # hand-fill one good row and one bad row
    rows = list(csv.DictReader(out.open(newline="")))
    rows[0].update(castellvi_grade="IIb", transition_type="sacralization", laterality="bilateral")
    rows[1].update(castellvi_grade="ZZ", transition_type="sacralization")   # bad grade
    rows[2].update(castellvi_grade="IV", transition_type="")                # missing transition
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ALL_COLS); w.writeheader(); w.writerows(rows)
    probs = validate_grade_sheet(out)
    assert any("ZZ" in p for p in probs)
    assert any("transition_type blank" in p for p in probs)


def test_validate_clean_sheet(tmp_path):
    splits = _make_splits(tmp_path)
    out = tmp_path / "grade.csv"
    generate_grade_worklist(splits, out)
    rows = list(csv.DictReader(out.open(newline="")))
    for r in rows:
        r.update(castellvi_grade="none", transition_type="none", laterality="na")
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ALL_COLS); w.writeheader(); w.writerows(rows)
    assert validate_grade_sheet(out) == []
