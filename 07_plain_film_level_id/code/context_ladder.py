# spine-program/07_plain_film_level_id/code/context_ladder.py
# Copied 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class, commit 097933a) tools/context_ladder.py.
# The repository copy is the one to run; this copy is the record. Runs on the grid in a Slurm job only.
"""How much of the spine does a model need to see before it can name a level?

THE QUESTION. Counting from C2 works because the whole column is visible. A lumbar case is
planned on T12-S1. Somewhere between those two extents the information that identifies a
vertebra stops being "its position in a sequence you can see" and has to become "what this
bone looks like". This measures where that happens, by taking one volume with the whole
column in it and handing a model progressively less of it.

THE LADDER. Each rung is a field of view expressed in VERTEBRAE, centred on a target level
and clipped to what exists:

    full        C2 to sacrum, the gold-standard count
    16, 12, 8   progressively less column
    6, 4, 2     a surgical field of view
    1           the target vertebra alone, no neighbours at all

At every rung the model is asked to name the SAME target vertebra, and the answer is scored
against the release's own per-level label. The curve of accuracy against context is the
result; the rung where it falls off is the answer to the question.

WHY THIS COHORT CANNOT ANSWER IT ALONE. CTSpinoPelvic1K is abdominopelvic: no record
contains C2, and thoracic ground truth stops around T8. The top of the ladder does not exist
here. Whole-spine data is required for the full range -- VerSe is the obvious source, and it
carries an L6 class, which is why it was worth aligning to this scheme in the first place.
This module therefore takes the level extent from the labels it is given and reports the
rungs it could actually build, rather than pretending to a range it does not have.

TWO MODALITIES, ONE LADDER. The same crop is applied to the volume (3-D) and to a DRR
rendered from it (2-D), so the 3-D segmenter and the radiograph network are asked the
identical question on the identical anatomy. That is the only way the two numbers compare.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import ndimage

# Dataset813 fullribs ids
VERT_IDS = list(range(1, 11))     # T10..L6
SACRUM_ID = 11
NAMES = {1: "T10", 2: "T11", 3: "T12", 4: "T13", 5: "L1", 6: "L2", 7: "L3",
         8: "L4", 9: "L5", 10: "L6", 11: "sacrum"}

# The rungs, in vertebrae of context either side of the target. None means "everything".
RUNGS = (None, 8, 6, 4, 3, 2, 1, 0)


@dataclass
class Rung:
    """One field of view, and what it actually contained."""
    context: int | None
    z_lo: int
    z_hi: int
    n_levels: int
    n_slices: int
    label: str

    @property
    def name(self) -> str:
        return "full" if self.context is None else f"+/-{self.context}"


def level_extents(gt: np.ndarray, si_axis: int, ids=None) -> dict[int, tuple[int, int]]:
    """The supero-inferior slice span of every level present, keyed by label id."""
    ids = ids or (VERT_IDS + [SACRUM_ID])
    out: dict[int, tuple[int, int]] = {}
    moved = np.moveaxis(gt, si_axis, 0)
    for cid in ids:
        hit = np.flatnonzero((moved == cid).any(axis=(1, 2)))
        if hit.size:
            out[cid] = (int(hit[0]), int(hit[-1]))
    return out


def build_ladder(gt: np.ndarray, target: int, si_axis: int,
                 rungs=RUNGS) -> list[Rung]:
    """Crops of decreasing context around `target`, expressed in whole vertebrae."""
    ext = level_extents(gt, si_axis)
    if target not in ext:
        return []
    # order the present levels along the column so "n vertebrae of context" is meaningful
    order = sorted(ext, key=lambda c: ext[c][0])
    ti = order.index(target)
    n_sl = gt.shape[si_axis]
    out: list[Rung] = []
    for r in rungs:
        if r is None:
            lo, hi = 0, n_sl - 1
            n_lv = len(order)
        else:
            lo_c = order[max(0, ti - r)]
            hi_c = order[min(len(order) - 1, ti + r)]
            lo, hi = ext[lo_c][0], ext[hi_c][1]
            n_lv = min(len(order) - 1, ti + r) - max(0, ti - r) + 1
        out.append(Rung(context=r, z_lo=lo, z_hi=hi, n_levels=n_lv,
                        n_slices=hi - lo + 1, label=NAMES.get(target, str(target))))
    # a rung that did not actually shrink carries no information beyond the one above it
    seen, uniq = set(), []
    for rg in out:
        key = (rg.z_lo, rg.z_hi)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(rg)
    return uniq


def crop(vol: np.ndarray, rung: Rung, si_axis: int) -> np.ndarray:
    sl = [slice(None)] * vol.ndim
    sl[si_axis] = slice(rung.z_lo, rung.z_hi + 1)
    return vol[tuple(sl)]


def drr(ct: np.ndarray, si_axis: int, lateral_axis: int,
        mu_water: float = 0.02, hu_clip=(-200.0, 1800.0)) -> np.ndarray:
    """A lateral digitally reconstructed radiograph: attenuation summed along one axis.

    Not a physics-accurate DRR -- no spectrum, no scatter, no beam hardening. It is the
    standard first-order model: HU to a linear attenuation coefficient, then integrate
    along the beam and take the log. What it must get right for THIS experiment is the
    ordering and relative contrast of bone against soft tissue, which decides whether a
    vertebra's edges are findable; absolute HU fidelity would matter for dosimetry and
    does not matter here.

    The floor at -200 HU drops air and most fat, which otherwise contribute a large,
    flat, geometry-dependent offset that washes out the bone.
    """
    a = np.clip(ct.astype(np.float32), hu_clip[0], hu_clip[1])
    mu = mu_water * (1.0 + a / 1000.0)
    mu[a <= hu_clip[0]] = 0.0
    path = mu.sum(axis=lateral_axis)
    img = 1.0 - np.exp(-path / max(path.max(), 1e-6) * 3.0)
    # orient so the supero-inferior axis runs down the rendered image
    if si_axis > lateral_axis:
        si_out = si_axis - 1
    else:
        si_out = si_axis
    if si_out != 0:
        img = img.T
    img = img - img.min()
    img = img / max(img.max(), 1e-6)
    return (img * 255.0).astype(np.uint8)


def target_centroid(gt: np.ndarray, target: int) -> tuple[float, ...] | None:
    m = gt == target
    if not m.any():
        return None
    return tuple(float(c) for c in ndimage.center_of_mass(m))
