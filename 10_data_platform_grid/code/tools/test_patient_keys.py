# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_patient_keys.py. working tree, uncommitted edit on 2026-10-08. The repository is the executable source; this copy is a record.
import sys
sys.path.insert(0, r"<repo spinesurg-ct-nnunet 097933a>\tools")
import patient_keys as PK

cross = {"COLONOG_1": "0001", "COLONOG_149": "0210", "COLONOG_378": "0533"}
cases = [
    # (case, ann, expected key or None)
    ("CTSP_COLONOG_149", {}, "ctsp:0210"),
    ("ctsp_0210_lat_p3", {"scheme": "ctsp", "source_case": "0210"}, "ctsp:0210"),
    ("ctsp_0210_ap_p0", {}, "ctsp:0210"),
    ("CTSP_COLONOG_378", {}, "ctsp:0533"),
    ("NH_00160_c", {}, "nhanes:00160"),
    ("NH_00160_l", {}, "nhanes:00160"),
    ("NHANES_nhanes_cervical_00160", {"patient_id": "nhanes_00160"}, "nhanes:00160"),
    ("NHANES_nhanes_lumbar_00160", {}, "nhanes:00160"),
    ("CSXA_csxa_0001035", {"patient_id": "csxa_0001035"}, "csxa:0001035"),
    ("BUU_FULL_buu_1673-F-064Y1", {"patient_id": "buu_1673"}, "buu:1673"),
    ("BUU_FULL_buu_1673-F-064Y1(1)", {"patient_id": "buu_1673"}, "buu:1673"),
    ("gl003", {}, "verse:gl003"),
    ("verse547", {}, "verse:verse547"),
    ("verse_gl003_lat_p2", {}, "verse:gl003"),
    ("TS_s0585", {}, "ts:s0585"),
    ("totalseg_s0585_ap_p1", {}, "ts:s0585"),
    ("implant_case42_lat_p0", {}, "implant:case42"),
    ("something_unknown_xyz", {}, None),
]
bad = 0
for case, ann, want in cases:
    got = PK.key_for(case, ann, cross)
    key = None if got is None else f"{got[0]}:{got[1]}"
    ok = key == want
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {case:<34} -> {key}   (want {want})" + ("" if got is None else f"   [{got[2]}]"))
# the two defects this file exists to stop, stated as assertions
assert PK.key_for("CTSP_COLONOG_149", {}, cross)[:2] == PK.key_for("ctsp_0210_lat_p3", {"scheme": "ctsp", "source_case": "0210"}, cross)[:2]
assert PK.key_for("NH_00160_c", {}, cross)[:2] == PK.key_for("NHANES_nhanes_cervical_00160", {"patient_id": "nhanes_00160"}, cross)[:2]
print("\nCT render and physics render of one patient collapse: yes")
print("both NHANES copies collapse: yes")

# the third defect (2026-09-22, docs/PATIENT_IDENTITY_SPEC.md alias 7): a VerSe SERIES is not a person. The
# manifest groups 37 series into 18 subjects; v8 keyed the series and put five people on both sides of its split.
vmap = {"verse090": "verse400", "verse155": "verse400", "verse212": "verse405", "verse258": "verse405",
        "verse259": "verse405", "gl003": "gl003", "verse547": "verse547"}
for case, ann, want in [
    ("verse090", {}, "verse:verse400"),
    ("verse155", {}, "verse:verse400"),
    ("verse_scan-verse155_ap_p0", {}, "verse:verse400"),          # the physics render of the same series
    ("CTSP_VERSE_verse155_p0", {"patient_id": "CTSP_VERSE_verse155"}, "verse:verse400"),  # the obl bank's misfiled name
    ("verse258", {}, "verse:verse405"),
    ("verse259", {}, "verse:verse405"),
    ("gl003", {}, "verse:gl003"),                                   # a single-series subject keeps its id
    ("verse_gl003_lat_p2", {}, "verse:gl003"),
    ("glgl003", {}, "verse:gl003"),                                 # the doubled prefix still collapses
]:
    got = PK.key_for(case, ann, cross, vmap)
    key = None if got is None else f"{got[0]}:{got[1]}"
    ok = key == want
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {case:<34} -> {key}   (want {want})" + ("" if got is None else f"   [{got[2]}]"))
assert PK.key_for("verse090", {}, cross, vmap)[:2] == PK.key_for("verse155", {}, cross, vmap)[:2]
assert PK.key_for("verse090", {}, cross, vmap)[:2] != PK.key_for("verse547", {}, cross, vmap)[:2]
# without the manifest the series stays a series -- the collapse must come from the table, not from a guess
assert PK.key_for("verse155", {}, cross)[:2] == ("verse", "verse155")
# and the manifest reader itself, on a two-row table
import os, tempfile
tmp = os.path.join(tempfile.gettempdir(), "verse_manifest_test.csv")
open(tmp, "w").write("series_id,patient_id,split\nverse090,verse400,training\ngl003,gl003,training\n")
assert PK.verse_subjects(tmp) == {"verse090": "verse400", "gl003": "gl003"}
print("VerSe series collapse to the manifest subject: yes")

# the fourth rule (2026-09-26, docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md 1a): Bournemouth cervical quantitative
# fluoroscopy. ImageEvent HV01a and HV01b are two events of ONE person (126 events, 63 people), so both key to
# bournemouth:HV01. The rule is SCOPED: it applies only under the corpus hint the export directory declares
# (realxray/bournemouth_qf/), and without it the stem stays unkeyed rather than becoming somebody else's patient.
BQF = "/rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf/images"
assert PK.corpus_hint_for_path(f"{BQF}/HV01a_flex_f0000.png") == "bournemouth"
assert PK.corpus_hint_for_path(BQF.replace("bournemouth_qf", "bournemouth_qf_roi2x") + "/x.png") == "bournemouth"
for ident, hint, want in [
    ("HV01a_flex_f0000", "bournemouth", "bournemouth:HV01"),
    ("HV01b_ext_f0123", "bournemouth", "bournemouth:HV01"),       # the other event of the same person
    ("HV01a", "bournemouth", "bournemouth:HV01"),                  # a meta `case` given as the event
    ("HV01", "bournemouth", "bournemouth:HV01"),                   # ... or as the person
    ("P05b_flex_f0000", "bournemouth", "bournemouth:P05"),
    ("P05a_ext_f0000", "bournemouth", "bournemouth:P05"),
    ("HV01a_flex_f0000", None, None),                              # no hint: unkeyed, not another corpus's patient
    ("P05b_flex_f0000", "carmlspine", None),                       # another corpus's hint does not reach the rule
    ("HV1a_flex_f0000", "bournemouth", None),                      # not the corpus's id shape
    ("HV01c_flex_f0000", "bournemouth", None),                     # only events a and b exist
    # corpora that already keyed must key exactly as before (tools/leak_check fall-through and the bank schemes)
    ("CTSP_COLONOG_149", None, "ctsp:0210"),
    ("ctsp_0210_lat_p3", None, "ctsp:0210"),
    ("NH_00160_c", None, "nhanes:00160"),
    ("TS_s0585", None, "ts:s0585"),
    ("verse547", None, "verse:verse547"),
    ("case100_AP", None, "carmlspine:case100"),
    ("case100_AP", "carmlspine", "carmlspine:case100"),
    # the C-ArmLSpine CBCT projection sweeps (scoped under the carmlspine hint): frame ### of case<N>'s spin
    ("case134_sw000", "carmlspine", "carmlspine:case134"),
    ("case134_sw123", "carmlspine", "carmlspine:case134"),
    ("case39_sw300", "carmlspine", "carmlspine:case39"),
    ("case134_sw000", None, None),                                 # no hint: the sweep row is not reached
    ("case134_sw12", "carmlspine", None),                          # not the exporter's three-digit frame
    ("case39_LAT2", "carmlspine", "carmlspine:case39"),            # the spot frames still key through leak_check
    ("case101_AP_k1_0", "carmlspine", "carmlspine:case101"),
    ("A053_0020", "cobra", "cobra:A053"),
    ("phantom_p01_065kv", "geneva", "geneva:phantom"),
    ("18-1109_000", None, "deepfluoro:18-1109"),
    ("fluoro_video_-wRtGXiWymY_00032__r3", None, "fluorocap_video:-wRtGXiWymY"),
]:
    r, why = PK.key_any(ident, None, cross, None, hint)
    key = r["key"] if r else None
    if key is not None:
        rk, rwhy = PK.resolve_key(key)                           # every key a rule yields must pass the person test
        assert rk == key, (ident, key, rwhy)
    ok = key == want
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {ident:<34} hint={str(hint):<11} -> {key}   (want {want})"
          + (f"   [{r['scheme']}]" if r else ""))
assert PK.resolve_key("bournemouth:HV01b") == ("bournemouth:HV01", None)
assert PK.canon_key("bournemouth:P05a") == PK.canon_key("bournemouth:P05b") == "bournemouth:P05"
assert PK.resolve_key("bournemouth:HV1")[0] is None
assert PK.key_any("HV01a_flex_f0000", corpus_hint="bournemouth")[0]["key"] \
    != PK.key_any("HV02a_flex_f0000", corpus_hint="bournemouth")[0]["key"]
assert PK.canon_key("case:100") == "carmlspine:case100" and PK.canon_key("nhanes:160") == "nhanes:00160"
print("Bournemouth events of one person collapse, and earlier corpora key as before: yes")
# the sweep frames reach their hint through the export directory, as level_prototype's path-only gate items do
RX = "/rs/rs_grp_oschome/go2432/data/realxray"
for sub, stem, want in [("carmlspine_sweep", "case134_sw000", "carmlspine:case134"),
                        ("carmlspine_sweep_case39", "case39_sw300", "carmlspine:case39")]:
    p = f"{RX}/{sub}/images/test/{stem}.png"
    hint = PK.corpus_hint_for_path(p)
    r, why = PK.key_any(stem, None, cross, None, hint)
    assert hint == "carmlspine" and r and r["key"] == want and r["scheme"] == "carmlspine_sweep", (p, hint, r, why)
print("C-ArmLSpine sweep frames key to their patient through the export directory: yes")
print("failures:", bad)
sys.exit(1 if bad else 0)
