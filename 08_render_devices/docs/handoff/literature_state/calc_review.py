"""Arithmetic added on review of LITERATURE_STATE.md (2026-10-08). Every input is copied from the file named beside it.
Output: calc_review.json in this folder."""
import json
import math
from pathlib import Path


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(100 * (c - h), 1), round(100 * (c + h), 1)


out = {}
# VERIDAH CT test set (AUTO C2: 365 test scans, TEA 6.8 %, LEA 7.9 %; CORR: recalls 97.22 % and 96.30 % fit k/36, k/27)
tea_rate = round(0.068 * 365, 1)
lea_rate = round(0.079 * 365, 1)
out["veridah_test_by_rates"] = {"TEA": tea_rate, "LEA": lea_rate, "total": round(tea_rate + lea_rate)}
out["veridah_recall_fits"] = {
    "35/36": round(100 * 35 / 36, 2), "26/27": round(100 * 26 / 27, 2),
    "28/29": round(100 * 28 / 29, 2), "24/25": round(100 * 24 / 25, 2),
}
out["veridah_test_by_recall"] = 36 + 27
# ours: TAB2 57 (L6 43 + T13 3 + sacralised four-lumbar 5 + sacralised five-lumbar 6); NUM:436 51 at-risk
for ours, lab in ((57, "57_L6_T13_sacralised_rows"), (51, "51_at_risk")):
    out[f"ratio_{lab}"] = {
        "vs_63_recall_inference": round(ours / 63, 2),
        "vs_54_rate_inference": round(ours / 54, 2),
        "vs_19_verse_hidden_phase": round(ours / 19, 2),
    }
# CTSpinoPelvic1K read-tier L6 16 (CORR positives_census row) over 789 countable (FOV ctsp_all 0.984)
out["ctsp_L6_read_tier"] = {"k": 16, "n": 789, "pct": round(100 * 16 / 789, 1), "wilson": wilson(16, 789)}
out["ctsp_L6_release_label"] = {"k": 18, "n": 789, "pct": round(100 * 18 / 789, 1), "wilson": wilson(18, 789)}
# section 5.2: lumbosacral-countable people. CEN 18 collections: L6 322 = 3.2 % of countable_LS
cen_countable = round(322 / 0.032)
rows = {"CTSpinoPelvic1K": 789, "TotalSegmentator v2": 483, "COBRA2026": 435, "18 collections (CEN countable_LS)": cen_countable, "RibFrac": 0}
out["countable_LS_rows"] = rows
out["countable_LS_sum"] = sum(rows.values())
out["countable_LS_from_expected_L6_377"] = round(377 / 0.032)
out["ct_on_disk_sum_802_1228_692_16898_660"] = 802 + 1228 + 692 + 16898 + 660
out["reviewer_14290_is_789_483_435_12123_459"] = 789 + 483 + 435 + 12123 + 459
# tier 2 + deferred: ACQ opening table against JOIN totals
out["acq_tier2_plus_deferred_people"] = 30486 + 3536
out["acq_tier2_plus_deferred_E_low"] = 153 + 187
out["gap_people_vs_JOIN_33362"] = 30486 + 3536 - 33362
out["ribfrac_rank90"] = {"n_new": 660, "E_low": 2.9}
# Moller stump-rib cohort (mem:lstv-data-landscape.md): VerSe 323 + RibFrac 420 against 648
out["moller_323_plus_420"] = 323 + 420
# P(22 of 22 carriers found) at a recall of 72.4 % (LCM section 8)
out["p_22_of_22_at_0724"] = round(0.724 ** 22, 4)
# VERIDAH anomaly scans in all (AUTO C2 rates on 1,536) and training counts (SYN: 60 TEA + 83 LEA)
out["veridah_all_by_rates"] = round(0.073 * 1536 + 0.055 * 1536, 1)
out["veridah_train_143_plus_test_63"] = 60 + 83 + 63
Path(__file__).with_name("calc_review.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
