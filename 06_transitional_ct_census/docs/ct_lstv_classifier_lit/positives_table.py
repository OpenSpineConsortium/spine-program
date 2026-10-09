"""Regenerate the read-tier positives table of docs/CT_LSTV_CLASSIFIER_PLAN.md section 1a from ONE source per cell.

Persons only (registry.csv rows with is_person == True). Every cell says which file it came from. The CTSP per-record
table joins three files by volume id / token:
  - docs/castellvi_consensus.csv   (CTSpinoPelvic1K-1; volume_id, token, consensus grade)
  - Lumbosac.csv                    (CTSpinoPelvic1K-1 root; the readers' worksheet, column
                                     'Non-rib/lumbar type bearing vertebra #' = the READ count)
  - transitional_registry/ctsp/rows.csv (labeller_a text carries the release's lumbar-id count)
A record's lumbosacral phenotype is USED as truth only when the read count and the release count agree; a
record whose read count differs (or is written '6 (NA 4)') is routed to the re-read queue and dropped from
that phenotype's truth. Nothing here is a segmenter's name: the release lumbar-id count is compared against
the read, never substituted for it.

Run:  python SchwingNet/lit/ct_lstv_classifier/positives_table.py > SchwingNet/lit/ct_lstv_classifier/positives_table.md
"""
from __future__ import annotations

import collections
import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
CTSP_REPO = REPO.parent / "CTSpinoPelvic1K-1"
REG = REPO / "SchwingNet" / "results" / "transitional_registry"

ELEVEN_RIB_L6 = {"verse544", "verse581", "verse606", "verse626", "verse636", "verse642", "verse765", "verse814"}
# 7/11,5/6/5 read (one subject, two scans): six lumbar-type with an ambiguous 11.5-rib thoracic column
AMBIGUOUS_L6 = {"verse406"}


def wilson_lb(k: int, n: int, z: float = 1.96) -> float:
    if n == 0:
        return float("nan")
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (c - h) / d


def read_count_token(s: str) -> tuple[str, bool]:
    """'6' -> ('6', True); '6 (NA 4)' -> ('6 (NA 4)', False): the two readers did not agree on the count."""
    s = s.strip()
    return s, bool(re.fullmatch(r"\d", s))


def ctsp_table() -> tuple[list[dict], dict]:
    cons = {r["volume_id"]: r for r in csv.DictReader(open(CTSP_REPO / "docs" / "castellvi_consensus.csv", encoding="utf-8"))}
    lumbosac = {}
    for r in csv.reader(open(CTSP_REPO / "Lumbosac.csv", encoding="utf-8-sig")):
        if len(r) > 2 and r[1].strip():
            tok = re.sub(r"[^0-9]", "", r[1])
            if tok:
                lumbosac.setdefault(tok, r[2])
    rows = {r["case"]: r for r in csv.DictReader(open(REG / "ctsp" / "rows.csv", encoding="utf-8"))}
    out = []
    for vid, c in sorted(cons.items()):
        if vid == "0016":
            continue
        row = rows.get(vid, {})
        m = re.search(r"release v11: (\d) lumbar ids", row.get("labeller_a", ""))
        release = int(m.group(1)) if m else None
        read_raw, clean = read_count_token(lumbosac.get(c["token"], ""))
        read_n = int(read_raw) if clean else None
        grade = c["consensus"]
        fused = row.get("fused_mask_representation", "")
        # LS class from the READ: count 6 -> LS-L6 (any grade); count 5 + III/IV -> LS-SAC; count 5 + II -> LS-II;
        # count 4 + III/IV with the fused body merged into the sacrum -> LS-SAC (23 mobile, fused 24th).
        if read_n == 6:
            ls = "LS-L6"
        elif read_n == 5 and grade.upper().startswith(("III", "IV")):
            ls = "LS-SAC"
        elif read_n == 5 and grade.upper().startswith("II"):
            ls = "LS-II"
        elif read_n == 4 and grade.upper().startswith(("III", "IV")):
            ls = "LS-SAC"
        else:
            ls = "?"
        agree = (read_n is not None) and (release is not None) and (
            (read_n == release) or (read_n == 4 and release == 4 and fused == "merged-into-sacrum"))
        used = ls if agree else "re-read (read count != release count)"
        out.append(dict(volume_id=vid, token=c["token"], grade=grade, reader_agreement=c["agreement"],
                        read_count=read_raw, release_lumbar_ids=release, fused=fused,
                        registry_subtype=row.get("subtype", ""), ls_from_read=ls, used=used))
    pools = collections.Counter(r["used"] for r in out)
    return out, pools


def registry_persons() -> list[dict]:
    R = list(csv.DictReader(open(REG / "registry.csv", encoding="utf-8")))
    return [r for r in R if r.get("is_person", "True") in ("True", "true", "1", "")]


def source_of(r: dict) -> str:
    s = r["patient_key"].split(":")[0]
    return {"ctsp": "CTSP", "verse": "VerSe"}.get(s, s)


def main() -> None:
    P = registry_persons()
    held = json.load(open(REG / "maximize" / "after" / "held_all.json", encoding="utf-8"))
    held_cases = {h["case"] for h in held}
    verse_rows = list(csv.DictReader(open(REG / "verse" / "rows.csv", encoding="utf-8")))
    contradicted = collections.defaultdict(set)
    for r in verse_rows:
        if "CONTRADICTED" in r["notes"].upper():
            contradicted[r["subtype"]].add(r["patient_key"])

    print("# Read-tier positives, persons, one source per cell (generated by positives_table.py)\n")
    print(f"registry.csv persons: {len(P)}; held_all.json cases: {len(held_cases)}\n")

    # ---- persons x subtype x tier x source, from registry.csv only
    print("## A. registry.csv: persons by subtype, truth tier and source (four_lumbar modifier split out)\n")
    print("| subtype | four_lumbar | tier | CTSP | VerSe | other | total |")
    print("|---|---|---|---:|---:|---:|---:|")
    cnt = collections.defaultdict(collections.Counter)
    for r in P:
        if r["subtype"] in ("none", "no_count", "", "unresolved"):
            continue
        key = (r["subtype"], r["four_lumbar"], r["truth_tier"])
        src = source_of(r)
        cnt[key][src if src in ("CTSP", "VerSe") else "other"] += 1
    for key in sorted(cnt):
        c = cnt[key]
        print(f"| {key[0]} | {key[1]} | {key[2]} | {c['CTSP']} | {c['VerSe']} | {c['other']} | {sum(c.values())} |")

    # ---- CTSP per record
    rows, pools = ctsp_table()
    print("\n## B. CTSP: the 33 read records, read count / release count / used\n")
    print("Read count = `Lumbosac.csv` column 'Non-rib/lumbar type bearing vertebra #'; release count = lumbar ids in the v11 mask (`ctsp/rows.csv` labeller_a); grade = `castellvi_consensus.csv` consensus.\n")
    print("| id | token | grade | readers agree on grade | read count | release lumbar ids | fused body in mask | registry subtype | LS class from the read | USED |")
    print("|---|---|---|---|---|---:|---|---|---|---|")
    for r in rows:
        print(f"| {r['volume_id']} | {r['token']} | {r['grade']} | {r['reader_agreement']} | {r['read_count']} | {r['release_lumbar_ids']} | {r['fused']} | {r['registry_subtype']} | {r['ls_from_read']} | {r['used']} |")
    print("\nCTSP pools after the rule: " + ", ".join(f"{k} {v}" for k, v in sorted(pools.items())))

    # ---- VerSe L6 split
    v_l6 = [r for r in P if r["subtype"] == "L6" and r["truth_tier"] == "read" and source_of(r) == "VerSe"]
    keys = {r["patient_key"].split(":")[1] for r in v_l6}
    eleven = keys & ELEVEN_RIB_L6
    ambiguous = keys & AMBIGUOUS_L6
    contra = {k for k in keys if f"verse:{k}" in contradicted["L6"]}
    print("\n## C. VerSe read L6 persons (registry.csv) split by the rule 'LS-L6 = 25 presacral'\n")
    print(f"- read L6 persons: {len(v_l6)}")
    print(f"- 24-presacral with 11 rib-bearing (read 7/11/6/5) -> TL-11 truth, not LS-L6: {len(eleven)} ({', '.join(sorted(eleven))})")
    print(f"- ambiguous thoracic column (7/11,5/6/5): {len(ambiguous)} ({', '.join(sorted(ambiguous))}) -> held")
    print(f"- contradicted by the scan (verse/rows.csv CONTRADICTED): {len(contra)} ({', '.join(sorted(contra))}); of these in the 11-rib set: {len(contra & eleven)}")
    ls_l6_pool = len(v_l6) - len(eleven) - len(ambiguous)
    ls_l6_truth = ls_l6_pool - len(contra - eleven)
    held_v = {r["patient_key"].split(":")[1] for r in v_l6 if any(c in held_cases for c in r["winning_case"].split(";"))}
    print(f"- LS-L6 read pool (25 presacral): {ls_l6_pool}; after excluding contradicted: {ls_l6_truth}")
    print(f"- winning case held by the id guard (no id 25): {len(held_v)}")

    # ---- Wilson for the pools
    print("\n## D. Wilson 95 % lower bound on PPV, all calls correct, at the revised pools\n")
    print("| pool | n | LB 0 err | LB 1 | LB 2 | LB 3 | LB 4 | max errors with LB >= 0.90 |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    ctsp_l6 = pools.get("LS-L6", 0)
    ctsp_sac = pools.get("LS-SAC", 0)
    ctsp_ii = pools.get("LS-II", 0)
    v_sac = sum(1 for r in P if r["subtype"] == "sacralised_L5_fused" and r["truth_tier"] == "read" and source_of(r) == "VerSe")
    v_ii = sum(1 for r in P if r["subtype"] == "castellvi_I_II" and r["truth_tier"] == "read" and source_of(r) == "VerSe")
    other_l6 = sum(1 for r in P if r["subtype"] == "L6" and r["truth_tier"] == "read" and source_of(r) not in ("CTSP", "VerSe"))
    other_sac = sum(1 for r in P if r["subtype"] == "sacralised_L5_fused" and r["truth_tier"] == "read" and source_of(r) not in ("CTSP", "VerSe"))
    for name, n in [
        (f"LS-L6 read pool (CTSP {ctsp_l6} + VerSe {ls_l6_pool} + other {other_l6})", ctsp_l6 + ls_l6_pool + other_l6),
        (f"LS-L6 truth (contradicted excluded)", ctsp_l6 + ls_l6_truth + other_l6),
        (f"LS-SAC (CTSP {ctsp_sac} + VerSe {v_sac} + other {other_sac})", ctsp_sac + v_sac + other_sac),
        (f"LS-II (CTSP {ctsp_ii} + VerSe {v_ii})", ctsp_ii + v_ii),
        ("TL-11 read (the 8 VerSe 7/11/6/5 + verse559 7/11/4/5)", len(eleven) + 1),
    ]:
        lbs = [wilson_lb(n - e, n) for e in range(5)]
        ok = [e for e in range(0, 20) if n - e >= 0 and wilson_lb(n - e, n) >= 0.90]
        print(f"| {name} | {n} | " + " | ".join(f"{x:.3f}" for x in lbs) + f" | {max(ok) if ok else 'none'} |")


if __name__ == "__main__":
    main()
