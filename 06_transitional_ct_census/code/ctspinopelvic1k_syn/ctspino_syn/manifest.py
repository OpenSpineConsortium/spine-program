# copied into spine-program/06_transitional_ct_census on 2026-10-08 from CTSpinoPelvic1K-Syn (local git, no remote) ctspino_syn/manifest.py; commit 7098eb1 of 2026-06-11; this folder is the only copy. The banned word, where it occurred, is rewritten as origin.
"""
manifest.py — synthetic-case tagging, origin, and split-leak auditing.

Two jobs:
  1. Tag every synthetic case with a `SYNTH_` caseID and a full origin
     record (so the dataset is reproducible and reviewer-traceable).
  2. Guard the train-only invariant: synthetic cases must NEVER appear in a
     fold's `val` or `test` list. `audit_splits_no_synth_leak` checks a
     parsed splits_final.json and returns violations.

Why the `SYNTH_` prefix matters: offline-generated cases live in the nnU-Net
raw dir alongside real cases, so the convert/splits step could fold them into
any split. The prefix lets that step (and this auditor) keep them train-only.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, List, Optional

SYNTH_PREFIX = "SYNTH_"
SCHEMA_VERSION = 1


def make_case_id(class_code: str, side_token: str, donor_token: str,
                 idx: int) -> str:
    """Canonical synthetic caseID, e.g. SYNTH_IIb_B_COLONOG_0123_007.

    side_token: 'B' (bilateral/mixed) or 'U' (unilateral; realized L/R is in
    origin, not the id, to keep ids short).
    """
    return f"{SYNTH_PREFIX}{class_code}_{side_token}_{donor_token}_{idx:03d}"


def is_synthetic(case_id: str) -> bool:
    return case_id.startswith(SYNTH_PREFIX)


@dataclass
class SynthOrigin:
    case_id:        str
    class_code:     str           # Castellvi code, e.g. "IIb"
    type_roman:     str
    method:         str           # "procedural" | "copypaste" | "registration"
    realized_side:  str           # "L" | "R" | "bilateral"
    recipient_token: str          # the normal case that was deformed
    donor_token:    Optional[str] # the real LSTV case supplying morphology (if any)
    seed:           int
    blend:          str           # "none" | "poisson" | "feather"
    refined:        bool          # diffusion refiner applied?
    label_scheme:   str           # which CTSpinoPelvic1K label scheme version
    params:         Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)


class SynthManifest:
    """Accumulates origin records and writes synth_manifest.json."""

    def __init__(self, label_scheme: str):
        self.label_scheme = label_scheme
        self.records: List[SynthOrigin] = []

    def add(self, prov: SynthOrigin) -> None:
        if not is_synthetic(prov.case_id):
            raise ValueError(
                f"caseID {prov.case_id!r} is not SYNTH_-prefixed; refusing to "
                f"record it (would break the train-only guard).")
        self.records.append(prov)

    def summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for r in self.records:
            counts[r.class_code] = counts.get(r.class_code, 0) + 1
        return counts

    def write(self, path: Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "schema_version": SCHEMA_VERSION,
            "label_scheme":   self.label_scheme,
            "n_cases":        len(self.records),
            "class_counts":   self.summary(),
            "cases":          [r.to_dict() for r in self.records],
        }, indent=2))


def audit_splits_no_synth_leak(splits_final: List[Dict]) -> List[str]:
    """Return a list of violation strings: any SYNTH_ caseID found in a
    fold's `val` (or `test`) list. Empty list == clean.

    Pass the parsed splits_final.json (list of {"train": [...], "val": [...]}).
    """
    violations: List[str] = []
    for i, fold in enumerate(splits_final):
        for key in ("val", "test"):
            for cid in fold.get(key, []):
                if is_synthetic(cid):
                    violations.append(f"fold {i}: synthetic case {cid!r} in {key!r}")
    return violations
