# copied into spine-program/06_transitional_ct_census on 2026-10-08 from CTSpinoPelvic1K-Syn (local git, no remote) ctspino_syn/annotation.py; commit 7098eb1 of 2026-06-11; this folder is the only copy. The banned word, where it occurred, is rewritten as origin.
"""
annotation.py — Pass-1 Castellvi grading worklist + sheet validation.

Pass 1 (this module): case-level grading of every real LSTV case. Reads the
canonical CTSpinoPelvic1K splits_5fold.json (which carries `patient_subtypes`
and `patient_attrs`), filters to non-normal tokens, and writes a grading CSV
with the 6-way prior + raw LSTV signals PREFILLED as context and the Castellvi
columns BLANK to fill. Then validate the filled sheet before it feeds the
generator.

Pass 2 (substructure masks TP_L/R, ala_L/R, L5S1_disc on donors) is separate —
see README.

CLI:
  python -m ctspino_syn.annotation worklist --splits splits_5fold.json --out grade_sheet.csv
  python -m ctspino_syn.annotation validate --sheet grade_sheet.csv
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple

from ctspino_syn import castellvi

# Allowed values (blank = not yet filled).
VALID_GRADES     = set(castellvi.all_codes()) | {"none", ""}
VALID_TRANSITION = {"sacralization", "lumbarization", "none", ""}
VALID_LATERALITY = {"left", "right", "bilateral", "na", ""}
VALID_DONOR      = {"yes", "no", ""}
VALID_CONFIDENCE = {"high", "med", "low", ""}

# Context columns (prefilled) + columns to fill (blank).
CONTEXT_COLS = ["token", "prior_subtype", "has_l6", "n_lumb_max",
                "lstv_label", "lstv_pelvic", "lstv_vertebral", "n_records"]
FILL_COLS    = ["castellvi_grade", "transition_type", "laterality",
                "is_donor", "confidence", "notes"]
ALL_COLS     = CONTEXT_COLS + FILL_COLS

_VALIDATORS = {
    "castellvi_grade": VALID_GRADES,
    "transition_type": VALID_TRANSITION,
    "laterality":      VALID_LATERALITY,
    "is_donor":        VALID_DONOR,
    "confidence":      VALID_CONFIDENCE,
}


def _token_sort_key(tok: str):
    return (0, int(tok)) if tok.isdigit() else (1, tok)


def generate_grade_worklist(splits_path: Path, out_csv: Path,
                            include_normal: bool = False) -> int:
    """Build the Pass-1 grading sheet from splits_5fold.json. Returns n rows."""
    s = json.loads(Path(splits_path).read_text())
    subs: Dict[str, str]  = s.get("patient_subtypes", {})
    attrs: Dict[str, Dict] = s.get("patient_attrs", {})
    if not subs:
        raise ValueError(f"{splits_path} has no patient_subtypes "
                         f"(need schema v6 from generate_5fold_splits.py).")

    rows: List[Dict] = []
    for tok in sorted(subs, key=_token_sort_key):
        sub = subs[tok]
        if sub == "normal" and not include_normal:
            continue
        a = attrs.get(tok, {})
        rows.append({
            "token": tok, "prior_subtype": sub,
            "has_l6": a.get("has_l6_any", ""),
            "n_lumb_max": a.get("n_lumb_max", ""),
            "lstv_label": a.get("lstv_label", ""),
            "lstv_pelvic": a.get("lstv_pelvic", ""),
            "lstv_vertebral": a.get("lstv_vertebral", ""),
            "n_records": a.get("n_records", ""),
            # blanks to fill during grading:
            "castellvi_grade": "", "transition_type": "", "laterality": "",
            "is_donor": "", "confidence": "", "notes": "",
        })

    out_csv = Path(out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ALL_COLS)
        w.writeheader(); w.writerows(rows)
    return len(rows)


def validate_grade_sheet(sheet_path: Path) -> List[str]:
    """Return a list of problems in a filled grading sheet ([] == clean)."""
    problems: List[str] = []
    with Path(sheet_path).open(newline="") as f:
        reader = csv.DictReader(f)
        missing = set(ALL_COLS) - set(reader.fieldnames or [])
        if missing:
            return [f"sheet missing columns: {sorted(missing)}"]
        for i, row in enumerate(reader, start=2):  # header is line 1
            tok = row.get("token", f"<row {i}>")
            for col, allowed in _VALIDATORS.items():
                val = (row.get(col) or "").strip()
                if val not in allowed:
                    problems.append(
                        f"{tok}: {col}={val!r} not in {sorted(allowed - {''})}")
            # light cross-check: a filled grade should have a transition_type
            g = (row.get("castellvi_grade") or "").strip()
            t = (row.get("transition_type") or "").strip()
            if g and g != "none" and not t:
                problems.append(f"{tok}: castellvi_grade={g} but transition_type blank")
    return problems


def _main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("worklist", help="generate the Pass-1 grading sheet")
    w.add_argument("--splits", required=True, type=Path)
    w.add_argument("--out", required=True, type=Path)
    w.add_argument("--include_normal", action="store_true")
    v = sub.add_parser("validate", help="validate a filled grading sheet")
    v.add_argument("--sheet", required=True, type=Path)
    args = ap.parse_args()

    if args.cmd == "worklist":
        n = generate_grade_worklist(args.splits, args.out, args.include_normal)
        print(f"wrote {args.out} with {n} cases to grade "
              f"({'incl' if args.include_normal else 'excl'} normals)")
    elif args.cmd == "validate":
        probs = validate_grade_sheet(args.sheet)
        if not probs:
            print("OK — grading sheet is valid.")
        else:
            print(f"{len(probs)} problem(s):")
            for p in probs:
                print(f"  {p}")
            raise SystemExit(1)


if __name__ == "__main__":
    _main()
