# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: reader_space/carm.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""The body model behind the C-arm simulator: where a vertebra sits on a supine adult, and how big.

WHY A BODY MODEL AT ALL. The reader study used to show a cropped radiograph on a grey page. That is not the
question a surgeon answers in theatre. In theatre the image arrives through a C-arm that covers a hand's
width of a patient who is lying in front of them, and the surgeon knows roughly -- not exactly -- where along
that patient the machine is sitting. Reproducing the crop reproduced the picture and threw away the task.

WHAT IS PHYSICAL HERE, AND WHAT IS APPROXIMATE.

  Physical. The field of view. A 9-inch image intensifier is 23 cm across its face, and with a 100 cm source
  distance and the spine about 60 % of the way to the detector it subtends about 140 mm AT THE SPINE. That
  number, and the other presets, are the same ones the sweep experiments use, so the simulator and the
  measurements agree about what a frame is.

  Physical. The distance between vertebrae. PITCH_MM is body plus disc per region, from the same sources the
  sweep uses. Summing it from C1 to S1 gives a column of 627 mm.

  Approximate, and labelled so. Where the column sits on the body. Two anthropometric anchors are used: C1 at
  0.10 of stature below the vertex and S1 at 0.455. The second is the more defensible -- the pubic symphysis
  sits at half of stature in an adult, which is an old and well-replicated observation, and S1 is a little
  above it. A useful outside check falls out of the two: dividing the 627 mm column by the 0.355 of stature it
  is assumed to span predicts a stature of 1766 mm. That is an adult man, which is the answer a wrong table
  would not have given -- and it is how the first version of this file was caught, because leaving T13 and L6
  in the chain made the column 688 mm and the man 1.94 m.

  DELIBERATELY IMPRECISE. The figure is jittered along its length, by a seeded per-film offset of up to
  +-25 mm. This is not sloppiness and it is not decoration. Without it the silhouette becomes a ruler: a
  reader could stop reading the bone, measure where the C-arm ring sits on the body, and convert that to a
  level. With it the figure carries what a surgeon actually has -- a rough sense of position, good to a couple
  of segments -- and the answer still has to come from the radiograph.
"""
from __future__ import annotations

import hashlib

# ------------------------------------------------------------------ the column
PITCH_MM = {"cervical": 19.0, "thoracic": 27.0, "lumbar": 34.0, "sacral": 34.0}
REGION = {**{f"C{i}": "cervical" for i in range(1, 8)},
          **{f"T{i}": "thoracic" for i in range(1, 14)},
          **{f"L{i}": "lumbar" for i in range(1, 7)}, "sacrum": "sacral"}
# The canonical chain, and it deliberately has no T13 and no L6. Those are the variants the project exists
# to find; including them in the ruler stretched the column to 688 mm and the simulated man to 1.94 m.
ORDER = ([f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)]
         + [f"L{i}" for i in range(1, 6)] + ["sacrum"])
# a variant is placed at its neighbour's position, which is where it is: T13 sits where T12 does, L6 at L5
ALIAS = {"T13": "T12", "L6": "L5"}

# stature anchors, vertex = 0.0 and soles = 1.0
C1_FRAC, S1_FRAC = 0.100, 0.455
SPAN_FRAC = S1_FRAC - C1_FRAC

# a 9-inch intensifier is 23 cm at its face and about 140 mm where the spine is; these are the sweep's presets
SPAN_MM = {"ii4": 70.0, "ii6": 95.0, "ii9": 140.0, "ii12": 190.0, "fpd30": 200.0}


def column_offset_mm(name: str) -> float:
    """Millimetres from the C1 body centre down the column to this vertebra's centre."""
    name = ALIAS.get(name, name)
    d = 0.0
    for a, b in zip(ORDER[:-1], ORDER[1:]):
        if a == name:
            break
        d += PITCH_MM[REGION[a]]
        if b == name:
            break
    else:
        if name != ORDER[-1]:
            raise KeyError(name)
    return d


COLUMN_MM = column_offset_mm("sacrum")          # 627 mm
STATURE_MM = COLUMN_MM / SPAN_FRAC              # 1766 mm -- the outside check named above


def body_fraction(name: str) -> float:
    """Where this vertebra sits along a supine adult, vertex 0.0 to soles 1.0."""
    return C1_FRAC + SPAN_FRAC * (column_offset_mm(name) / COLUMN_MM)


def figure_jitter_mm(film_id: str, amplitude_mm: float = 25.0) -> float:
    """A fixed, per-film shift of the figure under the film, so the silhouette cannot be used as a ruler.

    Seeded from the film id, so a reader who revisits a film in the second block sees the same body: a figure
    that moved between the two readings would itself be a cue that the two readings are of one film.
    """
    h = int(hashlib.sha256(f"figure|{film_id}".encode()).hexdigest()[:8], 16)
    return amplitude_mm * ((h % 2001) / 1000.0 - 1.0)


# ------------------------------------------------------------------ the silhouette
# A supine adult in LEFT LATERAL profile, head to the left, anterior up, in a 1000 x 360 box: x is stature
# (0 = vertex, 1000 = heel) and the table line is y = 300. Lateral rather than the frontal figure one first
# pictures, because the films are lateral projections -- the column then falls where the drawing puts it, in
# the posterior third of the trunk, instead of being buried in the middle of a body seen from the front.
#
# Supine AP thicknesses, as a fraction of the 1766 mm stature the column implies: head 200 mm, trunk 230 mm,
# thigh 150 mm, calf 110 mm; vertex to chin 230 mm, which is what stops the head swelling.
#
# These are CONTROL POINTS through which the outline is interpolated, and they were arrived at by rendering
# the figure and looking at it. Written as beziers and merely checked for plausibility, the same body plan
# produced a balloon-headed wave; two rounds of reasoning about coordinates did not reveal that, and one
# render did.
_ANTERIOR = [   # vertex -> toes
    (22, 250), (22, 226), (32, 208), (50, 198), (72, 195), (90, 200), (100, 211), (108, 213), (113, 206),
    (119, 214), (125, 222), (119, 228), (125, 234), (123, 243), (133, 253), (143, 260), (156, 260), (168, 252),
    (177, 236), (190, 213), (210, 192), (238, 180), (272, 174), (312, 172), (352, 174), (392, 179), (428, 185),
    (458, 194), (482, 205), (502, 213), (528, 217), (566, 218), (614, 221), (664, 227), (700, 234), (726, 242),
    (748, 249), (768, 252), (800, 251), (838, 252), (876, 255), (908, 258), (928, 256), (943, 240), (955, 220),
    (963, 208)
]
_POSTERIOR = [  # toes -> back of the vertex
    (976, 211), (985, 234), (990, 262), (991, 285), (982, 296), (964, 303), (942, 305), (922, 303), (900, 300),
    (876, 307), (848, 313), (818, 315), (790, 310), (766, 303), (742, 299), (716, 298), (668, 299), (620, 301),
    (578, 306), (546, 313), (518, 317), (496, 314), (474, 306), (452, 300), (424, 298), (376, 297), (324, 297),
    (272, 297), (228, 298), (202, 300), (182, 301), (166, 296), (155, 288), (146, 283), (137, 285), (122, 291),
    (102, 296), (80, 297), (58, 293), (36, 281), (24, 266)
]


def _catmull_rom(pts, per_segment: int = 12):
    """Closed Catmull-Rom through every control point. Pure Python: the Space has no scipy."""
    n = len(pts)
    out = []
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for k in range(per_segment):
            t = k / per_segment
            t2, t3 = t * t, t * t * t
            out.append((
                0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    return out


OUTLINE = _catmull_rom(_ANTERIOR + _POSTERIOR)
SILHOUETTE = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in OUTLINE) + " Z"

# the column's own line through that figure: fraction of stature, and fraction of trunk depth from the front
SPINE_LINE = [(0.100, 0.66), (0.170, 0.70), (0.250, 0.72), (0.330, 0.73), (0.400, 0.72), (0.455, 0.70)]
TRUNK_ANTERIOR_Y, TRUNK_POSTERIOR_Y = 172.0, 300.0


# ------------------------------------------------------------------ what the browser is given
def viewport_spec(film_id: str, top_name: str, bot_name: str, span: str = "ii9") -> dict:
    """Everything the canvas needs to place one film on one body -- and nothing that names a level.

    The vertebra names go IN so the placement can be computed; only fractions come OUT. A reader reading the
    page source finds two numbers near 0.4, not the string "L3".
    """
    f0, f1 = body_fraction(top_name), body_fraction(bot_name)
    j = figure_jitter_mm(film_id) / STATURE_MM
    return {"body_frac_top": round(f0 + j, 5), "body_frac_bot": round(f1 + j, 5),
            "stature_mm": round(STATURE_MM, 1), "span_mm": SPAN_MM[span], "span": span,
            "spine_line": SPINE_LINE, "silhouette": SILHOUETTE}
