# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/tests/test_units.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Unit tests that need no video codec: panel boxes on composed frames, duplicate / cadence classification,
replay runs, the clock fit, text parsing, override validation."""
import numpy as np
import pytest

from tools.fluoro_video import ocr as OC
from tools.fluoro_video import panels as PN
from tools.fluoro_video import sourcetext as ST
from tools.fluoro_video import synth
from tools.fluoro_video import timing as TM
from tools.fluoro_video.common import load_overrides


def _P(cfg):
    P = dict(cfg[0]["panel"])
    P["analysis_max_side"] = cfg[0]["sampling"]["analysis_max_side"]
    return P


@pytest.mark.parametrize("seed", [0, 1, 2, 3, 4])
@pytest.mark.parametrize("circle", [False, True])
def test_detect_known_box(cfg, seed, circle):
    img, box = synth.synthetic_frame(seed, circle)
    cands, _ = PN.detect(img, _P(cfg))
    acc = [c for c in cands if c["accepted"]]
    assert len(acc) == 1, [(c["box"], c["reject"]) for c in cands]
    assert np.max(np.abs(np.array(acc[0]["box"]) - np.array(box))) <= 2, (acc[0]["box"], box)
    assert acc[0]["shape"] == ("circle" if circle else "rect")


def test_room_only_has_no_panel(cfg):
    img = synth.distractors(synth.room(0.5, 9)).astype(np.uint8)
    cands, _ = PN.detect(img, _P(cfg))
    assert not [c for c in cands if c["accepted"]]


def test_fixed_box_score_separates_panel_from_room(cfg):
    img, box = synth.synthetic_frame(0, False)
    x0, y0, x1, y1 = box
    assert PN.fixed_box_score(img[y0:y1, x0:x1], _P(cfg), 1)[1]
    room = synth.room(0.2, 1).astype(np.uint8)
    assert not PN.fixed_box_score(room[y0:y1, x0:x1], _P(cfg), 1)[1]


def _d_pattern(runs, rng, dup=0.3, upd=4.0):
    d = []
    for r in runs:
        d.append(upd + rng.random())
        d += list(dup * rng.random(r - 1))
    return np.array(d)


def test_duplicates_4_frame_pattern(cfg):
    rng = np.random.default_rng(0)
    d = _d_pattern([4] * 60, rng)
    t = np.arange(d.size) / 30.0
    dup, info = TM.classify_duplicates(d, np.zeros(d.size, bool), cfg[0]["timing"])
    assert info["bimodal"]
    cad = TM.cadence(t, dup, np.zeros(d.size, bool), cfg[0]["timing"])
    assert cad["modal_frames_per_image"] == 4
    assert abs(cad["images_per_video_s"] - 7.5) < 0.05
    assert cad["repeat_pattern"] == "4"
    assert cad["liveness"] == "live"


def test_duplicates_alternating_2_3(cfg):
    rng = np.random.default_rng(1)
    d = _d_pattern([3, 2] * 50, rng)
    t = np.arange(d.size) / 30.0
    dup, info = TM.classify_duplicates(d, np.zeros(d.size, bool), cfg[0]["timing"])
    cad = TM.cadence(t, dup, np.zeros(d.size, bool), cfg[0]["timing"])
    assert abs(cad["images_per_video_s"] - 12.0) < 0.1
    assert cad["repeat_pattern"] in ("2,3", "3,2")


def test_every_frame_distinct(cfg):
    rng = np.random.default_rng(2)
    d = 4 + rng.random(200)
    dup, info = TM.classify_duplicates(d, np.zeros(200, bool), cfg[0]["timing"])
    assert not dup.any()


def test_static_with_one_jump(cfg):
    rng = np.random.default_rng(3)
    d = 0.2 * rng.random(300)
    d[150] = 12.0
    dup, info = TM.classify_duplicates(d, np.zeros(300, bool), cfg[0]["timing"])
    assert (~dup).sum() == 2                       # frame 0 and the jump
    cad = TM.cadence(np.arange(300) / 30.0, dup, np.zeros(300, bool), cfg[0]["timing"])
    assert cad["liveness"] == "held"


def test_keyframe_refresh_is_not_an_update(cfg):
    rng = np.random.default_rng(4)
    d = 0.1 * rng.random(300)
    key = np.zeros(300, bool)
    key[::60] = True
    d[key] = 1.2                                   # an I-frame refresh of a held image
    d[0] = 0
    dup, info = TM.classify_duplicates(d, key, cfg[0]["timing"])
    assert (~dup).sum() == 1


def test_replay_runs(cfg):
    rng = np.random.default_rng(5)
    imgs = [np.clip(rng.normal(128, 40, (32, 32)), 0, 255).astype(np.uint8) for _ in range(30)]
    ups = []
    for u in range(30):                            # clip 0: 30 distinct images
        ups.append(dict(clip=0, u=u, t=u * 0.133, phash=TM.phash64(imgs[u]), sig=imgs[u], ref=40.0))
    for u in range(8):                             # clip 1: a replay of images 10..17, 2 s later
        s = np.clip(imgs[10 + u].astype(int) + rng.integers(-1, 2, (32, 32)), 0, 255).astype(np.uint8)
        ups.append(dict(clip=1, u=u, t=6.0 + u * 0.133, phash=TM.phash64(s), sig=s, ref=40.0))
    runs = TM.find_replays(ups, cfg[0]["timing"])
    assert len(runs) == 1
    assert runs[0]["n"] == 8
    assert runs[0]["original"][0] == (0, 10)
    assert runs[0]["replay"][0] == (1, 0)


def test_clock_fit_2x(cfg):
    pts = np.arange(0, 12, 0.5)
    clock = np.floor(10 + 2 * pts)
    fit, why = TM.fit_clock(pts, clock, cfg[0]["speed"])
    assert why is None and fit["accepted"]
    assert abs(fit["slope"] - 2.0) < 0.1


def test_clock_parse():
    assert OC.parse_clock("11:00:43")[1] == 11 * 3600 + 43
    assert OC.parse_clock("00:14")[1] == 14
    assert OC.parse_clock("11/18/2017")[1] is None
    assert OC.parse_angle("LAO 12")[1] == 12
    assert OC.parse_angle("RAO 7")[1] == -7


def test_statements():
    st = ST.statements("Images were acquired at 7.5 frames/s. The loop is played at 2x speed.", "t")
    kinds = {(s["kind"], s["value"]) for s in st}
    assert ("rate", 7.5) in kinds
    assert ("speed", 2.0) in kinds


def test_overrides_file_is_empty_and_valid():
    ents, sha, _ = load_overrides()
    assert ents == []


def test_circle_completion_with_flat_saturated_part(cfg):
    """A round field whose left part is flat saturated white (air): only part of it is textured, and the box must
    still be the whole disk (circle completion from the rim against black)."""
    img, box = synth.synthetic_frame(0, True)
    cx, cy, r = 430, 180, 150
    yy, xx = np.mgrid[0:360, 0:640]
    m = ((xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= r * r) & (xx < cx - 40)
    img = img.copy()
    img[m] = 250
    cands, _ = PN.detect(img, _P(cfg))
    acc = [c for c in cands if c["accepted"]]
    assert len(acc) == 1
    assert acc[0]["shape"] == "circle" and acc[0]["circle_completed"]
    assert np.max(np.abs(np.array(acc[0]["box"]) - np.array(box))) <= 3, (acc[0]["box"], box)
