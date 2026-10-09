# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_ts_transitional_registry.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""tests for tools/ts_transitional_registry.py row logic (synthetic screen jsons; no data needed).

    python -m pytest tools/test_ts_transitional_registry.py -q
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ts_transitional_registry as T  # noqa: E402


def objs(names, lowest_rib, ribs=None, split=None):
    """B objects in S-I order; bodies up to index `lowest_rib` carry TS ribs numbered like their name"""
    out = []
    for i, n in enumerate(names, start=1):
        rt = (ribs or {}).get(n)
        if rt is None:
            rt = [f"L:rib_left_{n[1:]}", f"R:rib_right_{n[1:]}"] if (n.startswith("T") and i <= lowest_rib) else []
        out.append(dict(i=i, ts_name=n, cut=False, n_bodies=(2 if split == n else 1), ribs_ts=rt,
                        ribs_ct_long=[], ribs_ct_short=[]))
    return out


def screen(n_lumbar, n_thor, a_labels, names, lowest, **kw):
    B = dict(fov=dict(tl=True, ls=True, ct=True), n_lumbar_seen=n_lumbar, n_thoracic_span_seen=n_thor,
             objects=objs(names, lowest, kw.get("ribs"), kw.get("split")), lowest_rib_index=lowest, si_joint={},
             sacrum_extent_mm=120.0, n_cervical=7, lowest_rib_lengths_mm=kw.get("rib_mm", [90.0, 92.0]))
    return dict(B=B, A=dict(ok=True, labels=a_labels), ctd="/x/TSV3_s9999_ctd.json", sid="s9999")


THOR = [f"T{i}" for i in range(1, 13)]
LUMB5 = ["L1", "L2", "L3", "L4", "L5"]
A_NORMAL = ["C7"] + THOR + LUMB5 + ["S"]


def row(R):
    return T.row_from(R, "s9999", "ts:s9999", {}, None, False, None, None)


def test_concordant_normal_is_two_labeller_none():
    r, rv, info = row(screen(5, 12, A_NORMAL, THOR + LUMB5, 12))
    assert (r["subtype"], r["truth_tier"], r["agree"]) == ("none", "two-labeller", True)
    assert rv is None


def test_discordant_is_unresolved_not_the_positive_claim():
    # A (VERIDAH) skips T12 and names L1..L6 (TS_s1178); B counts 12 rib-bearing + 5 free
    a = ["C7"] + THOR[:11] + ["L1", "L2", "L3", "L4", "L5", "L6", "S"]
    r, rv, info = row(screen(5, 12, a, THOR + LUMB5, 12))
    assert r["subtype"] == "unresolved" and r["truth_tier"] == "none" and r["agree"] is False
    assert info["claim"] == "L6" and rv and "discordant" in rv["why"] and rv["claim"] == "L6"
    assert "claimed: L6 by A" in r["notes"]
    assert "both count 17 thoracolumbar bodies" in r["notes"]
    # counts are kept only at a junction where the two agree: here neither
    assert r["n_lumbar"] is None and r["n_thoracic_rib_bearing"] is None


def test_concordant_L6_two_labeller_and_origin_ts_names_L6():
    a = ["C7"] + THOR + LUMB5 + ["L6", "S"]
    r, rv, info = row(screen(6, 12, a, THOR + LUMB5 + ["L6"], 12))
    assert (r["subtype"], r["truth_tier"]) == ("L6", "two-labeller")
    assert info["origin"] == "ts_names_L6"
    assert rv and "concordant positive" in rv["why"]


def test_origin_ribless_T12():
    # TS names T12 but gives it no rib (lowest rib-bearing = TS T11 with rib 11): 11 + 6
    ribs = {"T12": []}
    a = ["C7"] + THOR[:11] + ["L1", "L2", "L3", "L4", "L5", "L6", "S"]
    r, rv, info = row(screen(6, 11, a, THOR + LUMB5, 11, ribs=ribs))
    assert r["subtype"] == "L6" and info["origin"] == "ts_ribless_T12"
    assert "24 presacral" in r["notes"]


def test_origin_split_object():
    a = ["C7"] + THOR + LUMB5 + ["L6", "S"]
    r, rv, info = row(screen(6, 12, a, THOR + LUMB5, 12, split="L3"))
    assert info["origin"] == "ts_object_split"


def test_T13_on_short_one_sided_rib_goes_to_review():
    names = THOR + ["L1"] + ["L2", "L3", "L4", "L5"]
    ribs = {"L1": ["R:rib_right_12"]}
    a = ["C7"] + THOR + ["T13", "L1", "L2", "L3", "L4", "L5", "S"]
    R = screen(4, 13, a, names, 13, ribs=ribs, rib_mm=[36.4])
    R["B"]["fov"]["ls"] = False        # no sacrum count, as TS_s1329
    R["A"]["labels"] = [x for x in a if x != "S"]
    r, rv, info = row(R)
    assert r["subtype"] == "T13"
    assert "one side only" in r["notes"] and "36.4 mm" in r["notes"]
    assert rv and "T13 on a short or one-sided 13th rib" in rv["why"]


def test_total_helper():
    assert T._total("L6", "11") == 17 and T._total("5", "12") == 17 and T._total(None, "12") is None
