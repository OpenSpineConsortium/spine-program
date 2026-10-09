"""Join acquisition/ranking.csv to data_platform/sources.json statuses.

Writes ranking_joined.csv next to this script: one row per ranking row with the
manifest id, the manifest status and the plan's expectation columns, so the
missing CT collections can be ranked by the plan's own E_low / E_count.
"""
import csv
import json
import os
import re

ROOT = "spinesurg-ct-nnunet:"
RANK = ROOT + "/SchwingNet/results/transitional_registry/acquisition/ranking.csv"
SRC = ROOT + "/data_platform/sources.json"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking_joined.csv")

SPECIAL = {
    "zenodo:amos22_unlabelled_ct": "amos22",
    "zenodo:amos22_labelled_ct": "amos22",
    "hf:AbdomenAtlas/AbdomenAtlas3.0Mini": "abdomenatlas3_mini",
    "hf:AbdomenAtlas/AbdomenAtlas2.0Mini": "hf_abdomenatlas2_0_mini",
    "hf:BodyMaps/PanTSMini": "hf_bodymaps_pantsmini",
    "hf:BodyMaps/CancerVerse": "hf_bodymaps_cancerverse",
    "zenodo:ctpelvic1k_clinic": "ctpelvic1k",
    "zenodo:ribfrac": "ribfrac",
    "hf:ctspine1k_noncolonog": "ctspine1k",
    "idc:ct_colonography": "tcia_ct_colonography",
    "tcia:fdg_pet_ct_lesions": "tcia_fdg_pet_ct_lesions",
    "zenodo:csi2014": "csi2014",
    "scidb:enhance_pet_1.6k": "scidb_enhance_pet_1_6k",
    "stanford_aimi:merlin": "stanford_aimi_merlin",
    "stanford_aimi:inspect": "stanford_aimi_inspect",
    "rsna:ratic_abdominal_trauma": "rsna_ratic_abdominal_trauma",
    "rsna:rspect_pe": "rsna_rspect_pe",
    "hf:ct_rate": "hf_ct_rate",
    "hf:cads_unique": "hf_cads_unique",
    "aws:stoic2021": "aws_stoic2021",
    "excluded:glocker_spine": "excluded_glocker_spine",
    "excluded:nmdid": "excluded_nmdid",
}
LATE = {"panorama", "barts_crl", "kidney_thoraxabdomen", "curvas_pdacvi", "aortaseg60",
        "curvas", "quadra_hc", "deep_psma", "waw_tace", "pengwin2026"}


def to_id(col):
    if col in SPECIAL:
        return SPECIAL[col]
    pre, _, name = col.partition(":")
    name_n = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    if pre == "zenodo" and name_n in LATE:
        return name_n
    return f"{pre}_{name_n}"


def main():
    src = {s["id"]: s for s in json.load(open(SRC, encoding="utf-8"))["sources"]}
    rows = list(csv.DictReader(open(RANK, encoding="utf-8")))
    out = []
    for r in rows:
        sid = to_id(r["collection"])
        s = src.get(sid)
        out.append({
            "rank": r["rank"], "collection": r["collection"], "manifest_id": sid if s else "NOT_CARDED",
            "manifest_status": s["status"] if s else "NOT_CARDED",
            "tier": r["tier"], "access": r["access"], "licence": r["licence"],
            "n_listed": r["n_subjects_listed"], "n_new": r["n_subjects_new"],
            "coverage": r["coverage_mix"], "E_low": r["E_low"], "E_high": r["E_high"],
            "E_count": r["E_count_screen"], "E_t13_low": r["E_t13_low"], "fetch_gb": r["fetch_gb"],
            "name": r["name"],
        })
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    miss = [o for o in out if o["manifest_status"] not in ("on_disk", "on_disk_partial", "on_disk_state_unknown")]
    miss.sort(key=lambda o: -float(o["E_low"] or 0))
    print("not carded:", [o["collection"] for o in out if o["manifest_id"] == "NOT_CARDED"])
    print("rows not on disk:", len(miss))
    for o in miss:
        if float(o["E_low"] or 0) <= 0 and o["manifest_status"] == "excluded":
            continue
        print("|".join([o["rank"], o["collection"], o["manifest_status"], o["tier"][:45], o["access"],
                        o["licence"][:22], o["n_new"], o["coverage"][:28], o["E_low"], o["E_high"],
                        o["E_count"], o["E_t13_low"], o["fetch_gb"]]))
    tot = {}
    for o in miss:
        k = o["manifest_status"]
        t = tot.setdefault(k, [0, 0.0, 0.0, 0.0, 0])
        t[0] += 1
        t[1] += float(o["E_low"] or 0)
        t[2] += float(o["E_high"] or 0)
        t[3] += float(o["E_count"] or 0)
        t[4] += int(float(o["n_new"] or 0))
    for k, t in tot.items():
        print("TOTAL", k, "rows", t[0], "n_new", t[4], "E_low %.1f E_high %.1f E_count %.1f" % (t[1], t[2], t[3]))


if __name__ == "__main__":
    main()
