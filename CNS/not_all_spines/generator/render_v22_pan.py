"""paper/cns2026/render_v22_pan.py -- the closing film again, from the frames that show the upper thoracic spine (v22).

Greg's word of 1 November: the v21 film missed the thoracic. Its frames came from a projection that cut an arm's reach
out of the chest, and T1 to T4 were never seen under the shoulders. grid/pan_render.py now softens the shoulder bones,
cuts a slab about the spine above T6 after the body is found, and weighs up the thoracic bodies (run 8, which the
linker names L5 to C3 by count alone, 22 of 22 as the CT labels them; C2 was not boxed). The film is drawn by
render_v21_pan.py, pointed at figs_v22_6min, with one change: a counted body lights only after the one
below it, a tenth of a second at the least, so the 3D map fills in from the sacrum up one body at a time.

    python paper/cns2026/pan_link.py figs_v22_6min/pan8
    python paper/cns2026/render_v22_pan.py figs_v22_6min/pan8
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_v21_pan as film  # noqa: E402

film.FIG = HERE / "figs_v22_6min"
film.OUT, film.POSTER, film.META = film.FIG / "pan.mp4", film.FIG / "pan_first.png", film.FIG / "pan.json"
first_sight = film.Pan.registration


STEP = 3                            # frames between two counted names at the least: a tenth of a second


def counted_in_order(self, dets):
    """A count names a body only once the body below it is named, and a tenth of a second after it at the least, so
    the map fills in from the sacrum up one body at a time, never ahead of the detector, even where the field
    brings several bodies into view at once."""
    from pan_link import UP
    out, floor = first_sight(self, dets), None
    counted = {b["name"] for b in self.bodies if b["how"] == "count"}
    for name in UP:
        if name in counted and name in out:
            out[name] = floor = out[name] if floor is None else max(out[name], floor + STEP)
    return out


film.Pan.registration = counted_in_order

if __name__ == "__main__":
    film.build(Path(sys.argv[1]))
