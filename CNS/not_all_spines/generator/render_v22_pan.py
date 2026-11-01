"""paper/cns2026/render_v22_pan.py -- the closing film again, from the frames that show the upper thoracic spine (v22).

Greg's word of 1 November: the v21 film missed the thoracic. Its frames came from a projection that cut an arm's reach
out of the chest, and T1 to T4 were never seen under the shoulders. grid/pan_render.py now softens the shoulder bones,
cuts a slab about the spine above T6 after the body is found, and weighs up the thoracic bodies (run 9). The
detector is read at a floor of 0.10 over the frames and their mirror images, pooled (pan_link.py), and the linker
names L5 to C2 by count alone, 23 of 23 as the CT labels them. The film is drawn by
render_v21_pan.py, pointed at figs_v22_6min, with three changes: the boxes are the ones the linker counted with
(pan_link.kept: its floor and its column test); a counted body lights only after the one below it, a tenth of a
second at the least, so the 3D map fills in from the sacrum up one body at a time; and a named body's box is carried
through up to HOLD frames the detector misses it, moved with the pan, as a tracker carries a box.

    python paper/cns2026/pan_link.py figs_v22_6min/pan9 --det det_low_L --floor 0.1 --flip det_low_R
    python paper/cns2026/render_v22_pan.py figs_v22_6min/pan9
"""
from __future__ import annotations

import sys
import json
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


def linked_boxes(run, facing):
    """The boxes the linker counted with: its own floor and its column test (pan_link.kept)."""
    from pan_link import kept
    return kept(run, json.load(open(run / "linked.json", encoding="utf-8")))


film.detections = linked_boxes
HOLD = 8                            # frames a named body's box is carried through the detector's misses, with the pan


def compose(pan, spine, smoother, frame, k, strip_img, project):
    """render_v21_pan.compose, with a named body's box held through up to HOLD frames the detector misses it: the
    box stays where the body is, moved with the pan's own shift, as a tracker carries it, and never before the
    body was first boxed."""
    seen = {}
    for det in pan.by_frame.get(k, []):
        body = pan.body_of(det)
        if body is not None:
            seen[body["name"]] = True
    last = getattr(pan, "last_seen", {})
    for name in seen:
        last[name] = k
    pan.last_seen = last
    held = [name for name, f in last.items() if name not in seen and k - f <= HOLD and name in smoother.state
            and k >= pan.registered.get(name, 10 ** 9)]
    image = original(pan, spine, smoother, frame, k, strip_img, project)
    if not held:
        return image
    over = film.Image.new("RGBA", (film.W * 2, film.H * 2), (0, 0, 0, 0))
    d = film.ImageDraw.Draw(over)
    label = film.font(46)
    fx, fy = (film.W - film.FIELD) // 2, 6
    offset = pan.offsets[k]
    for name in held:
        box = smoother.state[name] + [offset[1], offset[0], offset[1], offset[0]]
        x0, y0, x1, y1 = (film.to_screen(box, film.FIELD) + [fx, fy, fx, fy]) * 2
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, outline=film.BOX + (235,), width=5)
        tw = d.textlength(name, font=label)
        tx, ty = (x0 + x1) / 2 - tw / 2, y0 - 60
        d.text((tx + 2, ty + 2), name, font=label, fill=(0, 0, 0, 160))
        d.text((tx, ty), name, font=label, fill=(255, 255, 255, 245))
    over = over.resize((film.W, film.H), film.Image.LANCZOS)
    image.paste(over, (0, 0), over)
    return image


original = film.compose
film.compose = compose

if __name__ == "__main__":
    film.build(Path(sys.argv[1]))
