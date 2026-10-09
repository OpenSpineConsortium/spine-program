# copied into spine-program/06_transitional_ct_census on 2026-10-08 from CTSpinoPelvic1K-Syn (local git, no remote) ctspino_syn/castellvi.py; commit 7098eb1 of 2026-06-11; this folder is the only copy. The banned word, where it occurred, is rewritten as origin.
"""
castellvi.py — Castellvi LSTV classification taxonomy and the generation matrix.

Castellvi et al. (1984) grade lumbosacral transitional vertebrae (LSTV) by the
relationship between the L5 transverse process (TP) and the sacral ala:

  Type I    dysplastic TP (craniocaudal diameter >= 19 mm), no articulation
  Type II   pseudoarthrosis: TP forms a diarthrodial (false) joint with the ala
  Type III  fusion: TP is bony-fused to the ala
  Type IV   mixed: Type II on one side, Type III on the other

  suffix a = unilateral, b = bilateral (Type IV is inherently mixed/bilateral)

The Castellvi-defining signal is the TP<->ala relationship, NOT the vertebral
body. Reproducing that per side, with a voxel-exact label, is the whole reason
this generator exists. Each class below names the feature the procedural engine
must build on each side.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class SideFeature(str, Enum):
    NONE            = "none"             # normal TP
    DYSPLASTIC      = "dysplastic"       # enlarged/spatulated TP (Type I)
    PSEUDOARTHROSIS = "pseudoarthrosis"  # TP-ala false joint (Type II)
    FUSION          = "fusion"           # TP-ala bony bridge (Type III)


@dataclass(frozen=True)
class CastellviSpec:
    """One generatable Castellvi class.

    For UNILATERAL classes the affected feature is placed on `left` by
    convention; the generator randomizes the actual side (L/R) per seed via
    `side_token()`. For bilateral/mixed classes both sides are fixed.
    """
    code:        str          # "Ia","Ib","IIa","IIb","IIIa","IIIb","IV"
    type_roman:  str          # "I","II","III","IV"
    bilateral:   bool         # both sides affected (incl. mixed Type IV)
    left:        SideFeature
    right:       SideFeature
    description: str

    @property
    def unilateral(self) -> bool:
        return not self.bilateral

    @property
    def is_mixed(self) -> bool:
        return (self.left != self.right
                and SideFeature.NONE not in (self.left, self.right))

    def side_token(self) -> str:
        """Token for the caseID: 'B' if bilateral/mixed, else 'U' (the
        generator records the realized L/R in origin)."""
        return "B" if self.bilateral else "U"


# Canonical generation matrix (Castellvi I–IV, a/b + mixed IV).
CASTELLVI_CLASSES: List[CastellviSpec] = [
    CastellviSpec("Ia",   "I",   False, SideFeature.DYSPLASTIC,      SideFeature.NONE,
                  "Unilateral dysplastic transverse process (>=19 mm)."),
    CastellviSpec("Ib",   "I",   True,  SideFeature.DYSPLASTIC,      SideFeature.DYSPLASTIC,
                  "Bilateral dysplastic transverse processes."),
    CastellviSpec("IIa",  "II",  False, SideFeature.PSEUDOARTHROSIS, SideFeature.NONE,
                  "Unilateral pseudoarthrosis (TP-ala false joint)."),
    CastellviSpec("IIb",  "II",  True,  SideFeature.PSEUDOARTHROSIS, SideFeature.PSEUDOARTHROSIS,
                  "Bilateral pseudoarthroses."),
    CastellviSpec("IIIa", "III", False, SideFeature.FUSION,          SideFeature.NONE,
                  "Unilateral complete bony fusion of TP to ala."),
    CastellviSpec("IIIb", "III", True,  SideFeature.FUSION,          SideFeature.FUSION,
                  "Bilateral fusion."),
    CastellviSpec("IV",   "IV",  True,  SideFeature.PSEUDOARTHROSIS, SideFeature.FUSION,
                  "Mixed: pseudoarthrosis one side, fusion the other."),
]

CLASS_BY_CODE: Dict[str, CastellviSpec] = {c.code: c for c in CASTELLVI_CLASSES}

# Type I unilateral craniocaudal TP threshold (Castellvi diagnostic criterion).
DYSPLASTIC_TP_MIN_MM = 19.0


def all_codes() -> List[str]:
    return [c.code for c in CASTELLVI_CLASSES]


def resolve(codes: List[str]) -> List[CastellviSpec]:
    """Map a list of class codes (or 'all') to specs, preserving order."""
    if not codes or codes == ["all"]:
        return list(CASTELLVI_CLASSES)
    out = []
    for code in codes:
        if code not in CLASS_BY_CODE:
            raise ValueError(f"unknown Castellvi code {code!r}; "
                             f"valid: {all_codes()} or 'all'")
        out.append(CLASS_BY_CODE[code])
    return out
