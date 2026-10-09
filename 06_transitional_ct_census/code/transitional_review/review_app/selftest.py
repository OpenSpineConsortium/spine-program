# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/selftest.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/selftest.py -- build a 3-case fake tree, drive both stages through the HTTP API, check the rules.

What it asserts (each failure is printed and the exit code is 1):
  queue order        paired case first, then by type rank (L6 before stump_rib)
  stage-1 blinding   no registry / prior / truth key or marker string anywhere in the payload or the HTML page
  stage-2 blinding   the payload of a case that already has a stage-1 verdict carries no stage-1 field, no
                     screener name, no reason text, no verdict word
  gate               a stage-1 reject never reaches stage 2 (queue skips it; direct GET is refused)
  timestamps         claimed_at / submitted_at are server-side; edit_seconds is computed by the server and a
                     client-sent value is ignored; a verdict without a reason is refused
  record header      every review file carries prereg_sha256 (= sha256 of the file as read), prereg_status,
                     git_sha (or its error), tool, tool_version, written_at_utc, input_sha256 of what was served
  audit              audit.csv is admin-only, joins both stages per case, carries the hidden manifest columns
  append-only        a restart keeps every record byte-identical; a truncated history is refused; adding a
                     manifest row creates one case and touches no other file
  names              the dashboard prints no user name unless public_names is set

Run:  cd tools/transitional_review && python -m review_app --selftest [--keep DIR]
"""
from __future__ import annotations

import csv
import io
import json
import re
import shutil
import struct
import sys
import tempfile
import traceback
import zlib
from pathlib import Path
from typing import List

from .config import Config, prereg_status_of, sha256_file
from .ledger import Ledger, LedgerError, LocalBackend

FORBIDDEN_STAGE1 = ("prior_marker", "registry", "prior_call", "truth_tier", "labeller")
FORBIDDEN_STAGE2 = FORBIDDEN_STAGE1 + ("stage1", "(username withheld)", "reason", "edit_seconds", "submitted_at",
                                       "reason_marker_s1", "accept", "review_id")
ALLOWED_KEYS_WITH_FORBIDDEN_SUBSTRING = {"verdicts", "reason_required"}


def tiny_png(w: int = 6, h: int = 4, rgb=(200, 40, 40)) -> bytes:
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))

    def chunk(t: bytes, d: bytes) -> bytes:
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


CASES = [
    # case_id, collection, person_key, type, paired, flags, priority, registry_subtype
    ("ctsp_0005", "ctsp", "ctsp:0005", "L6", "0", "count_6;lumbarisation_candidate", "5", "L6_PRIOR_MARKER"),
    ("cobra_A270", "cobra", "cobra:A270", "L6", "1", "count_6", "0", "L6_PRIOR_MARKER"),
    ("ts_s0042", "ts", "ts:s0042", "stump_rib", "0", "stump_left", "9", "STUMP_PRIOR_MARKER"),
]
COLS = ["case_id", "collection", "person_key", "type", "paired", "flags", "rules", "priority", "tier",
        "registry_subtype", "registry_truth_tier", "prior_call"]


def write_tree(root: Path, cases=CASES) -> None:
    root.mkdir(parents=True, exist_ok=True)
    rows = []
    for cid, coll, pk, typ, paired, flags, prio, reg in cases:
        rows.append([cid, coll, pk, typ, paired, flags, "rule1;rule3", prio, "1", reg, "read", reg])
        d = root / "cases" / cid
        (d / "previews").mkdir(parents=True, exist_ok=True)
        (d / "masks").mkdir(exist_ok=True)
        (d / "labels").mkdir(exist_ok=True)
        (d / "README.md").write_text(
            f"# {cid}\n\nRule 1 counted **six** free bodies between the lowest full rib and the sacrum.\n\n"
            f"- lowest rib-bearing body: T12 (left 71 mm, right 68 mm)\n- anchor: Dataset803 sacrum\n\n"
            f"```\nitksnap -g ct.nii.gz -s masks/spineps.nii.gz\n```\n", encoding="utf-8")
        (d / "evidence.json").write_text(json.dumps({
            "rule1": {"count": 6, "anchor_source": "dataset803", "f_per_body": {"20": 0.0, "25": 0.07},
                      "castellvi_II_IV_candidate": False},
            "rule3": {"last_rib_level": 19, "stump_left": "FULL", "stump_right": "FULL"},
            "registry_subtype": reg, "prior_call": reg,
            "hidden": {"registry_call": reg, "truth_tier": "read"},
        }, indent=1), encoding="utf-8")
        (d / "previews" / "ap.png").write_bytes(tiny_png())
        (d / "ct.nii.gz").write_bytes(b"placeholder")
        (d / "masks" / "spineps_seg-vert.nii.gz").write_bytes(b"placeholder")
        (d / "labels" / "verse.txt").write_text("0 0 0 0 0 0 0 \"Clear Label\"\n")
        if paired == "1":
            (d / "case.mrb").write_bytes(b"placeholder")
            (d / "xr_AP_P.txt").write_text("1 0 0 0\n0 1 0 0\n0 0 1 0\n")
    with open(root / "manifest.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(COLS)
        w.writerows(rows)
    src = Path(__file__).resolve().parents[3] / "docs" / "ruleclass" / "PREREG_rules.md"
    if src.exists():
        shutil.copyfile(src, root / "PREREG_rules.md")
    else:
        (root / "PREREG_rules.md").write_text("# PREREG_rules (stub)\n\nsha256 of this file:  ____\n")


def scan(obj, forbidden, path="") -> List[str]:
    """Every (path, hit) where a key or a string value contains a forbidden substring, case-insensitive."""
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if k not in ALLOWED_KEYS_WITH_FORBIDDEN_SUBSTRING:
                for f in forbidden:
                    if f in kl:
                        hits.append((f"{path}/{k}", f"key contains {f!r}"))
            hits += scan(v, forbidden, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += scan(v, forbidden, f"{path}[{i}]")
    elif isinstance(obj, str):
        sl = obj.lower()
        for f in forbidden:
            if f in sl:
                hits.append((path, f"value contains {f!r}"))
    return hits


class Check:
    def __init__(self):
        self.fails: List[str] = []
        self.n = 0

    def __call__(self, cond, msg):
        self.n += 1
        if not cond:
            self.fails.append(msg)
            print(f"  FAIL  {msg}")
        else:
            print(f"  ok    {msg}")
        return cond


def snapshot(dirpath: Path) -> dict:
    return {p.relative_to(dirpath).as_posix(): p.read_bytes() for p in dirpath.rglob("*") if p.is_file()}


def run(keep=None) -> int:
    from fastapi.testclient import TestClient
    from .app import create_app

    base = Path(keep).resolve() if keep else Path(tempfile.mkdtemp(prefix="tr_review_selftest_"))
    tree = base / "tree"
    if tree.exists():
        shutil.rmtree(tree)
    write_tree(tree)
    print(f"[selftest] fake tree at {tree}")
    ck = Check()
    cfg = Config(root=tree, ledger_dir=tree / "ledger", prereg_path=tree / "PREREG_rules.md",
                 screener="(username withheld)", confirmer="CONFIRMER", admins=("admin",), users={}, dev_tokens=True,
                 public_names=False, reviewer_tree_path="/Volumes/review_tree")
    prereg_sha = sha256_file(tree / "PREREG_rules.md")
    prereg_status = prereg_status_of((tree / "PREREG_rules.md").read_text(encoding="utf-8", errors="replace"))
    S = {"Authorization": "Bearer (username withheld)"}
    C = {"Authorization": "Bearer CONFIRMER"}
    A = {"Authorization": "Bearer admin"}
    try:
        app = create_app(cfg)
        with TestClient(app) as c:
            # ── stage 1 ───────────────────────────────────────────────────
            r = c.post("/api/claim", headers=S)
            ck(r.status_code == 200, f"stage-1 claim returns 200 (got {r.status_code})")
            p = r.json()
            ck(p["case_id"] == "cobra_A270", f"paired case claimed first (got {p['case_id']})")
            ck(p["stage"] == 1 and p["role"] == "screener", "stage-1 payload says stage 1 / screener")
            hits = scan(p, FORBIDDEN_STAGE1)
            ck(not hits, f"stage-1 payload holds no registry/prior field or marker ({hits[:3]})")
            ck("rule1" in (p.get("evidence") or {}) and "hidden" not in (p.get("evidence") or {}),
               "evidence served with rule fields, 'hidden' object stripped")
            ck(p["previews"] == ["/case/cobra_A270/preview/ap.png"], "preview URL listed")
            ck("slicer" in p["open_commands"] and "itksnap" in p["open_commands"]
               and p["open_commands"]["itksnap"].startswith('itksnap -g "/Volumes/review_tree/'),
               f"open commands composed with the reviewer's tree path ({p['open_commands'].get('itksnap')})")
            ck("imfusion" in p["open_commands"], "projection-matrix import shown for the paired case")
            r2 = c.get(p["previews"][0], headers=S)
            ck(r2.status_code == 200 and r2.headers["content-type"].startswith("image/png"),
               "preview served as image/png to the claim holder")
            ck(c.get(p["previews"][0], headers=C).status_code == 403, "preview refused to a non-holder")
            html = c.get(f"/case/{p['case_id']}", headers=S).text
            ck("PRIOR_MARKER" not in html and "registry" not in html.lower(),
               "stage-1 HTML page holds no prior-call marker")
            ck("<b>six</b>" in html and "<pre>" in html, "README rendered from Markdown")
            again = c.post("/api/claim", headers=S).json()
            ck(again["claim_token"] == p["claim_token"], "re-claim serves the same open claim (one case at a time)")
            r = c.post("/api/submit", headers=S, data={"claim_token": p["claim_token"], "verdict": "accept",
                                                       "reason": "", "edit_seconds": "999"})
            ck(r.status_code == 400, f"verdict without a reason refused ({r.status_code})")
            r = c.post("/api/submit", headers=S, data={"claim_token": p["claim_token"], "verdict": "accept",
                                                       "reason": "REASON_MARKER_S1 T12 ribs full both sides",
                                                       "edit_seconds": "999"})
            ck(r.status_code == 200, f"stage-1 accept recorded ({r.status_code} {r.text[:120]})")
            ck(r.json().get("edit_seconds") != 999 and isinstance(r.json().get("edit_seconds"), int)
               and r.json()["edit_seconds"] >= 0, "edit_seconds computed server-side, client value ignored")
            ck(r.json()["final"] == "pending_stage2", "accepted case moves to pending_stage2")
            dup = c.post("/api/submit", headers=S, data={"claim_token": p["claim_token"], "verdict": "accept",
                                                         "reason": "REASON_MARKER_S1 T12 ribs full both sides"})
            ck(dup.status_code == 200 and dup.json().get("duplicate") is True, "identical resubmit is idempotent")
            conflict = c.post("/api/submit", headers=S, data={"claim_token": p["claim_token"], "verdict": "reject",
                                                              "reason": "changed my mind"})
            ck(conflict.status_code == 409, f"a different resubmit is refused ({conflict.status_code})")

            p2 = c.post("/api/claim", headers=S).json()
            ck(p2["case_id"] == "ctsp_0005", f"then L6 before stump_rib (got {p2['case_id']})")
            r = c.post("/api/submit", headers=S, data={"claim_token": p2["claim_token"], "verdict": "reject",
                                                       "reason": "the sixth body carries a 55 mm rib"})
            ck(r.status_code == 200 and r.json()["final"] == "rejected", "stage-1 reject is terminal")
            p3 = c.post("/api/claim", headers=S).json()
            ck(p3["case_id"] == "ts_s0042", f"stump_rib case last (got {p3['case_id']})")
            r = c.post("/api/submit", headers=S, data={"claim_token": p3["claim_token"], "verdict": "unsure",
                                                       "reason": "rib end at the field edge"})
            ck(r.status_code == 200 and r.json()["final"] == "pending_stage2", "stage-1 unsure goes to stage 2")
            ck(c.post("/api/claim", headers=S).status_code == 204, "stage-1 queue empty -> 204")
            ck(c.post("/api/submit", headers=C, data={"claim_token": p3["claim_token"], "verdict": "confirm",
                                                      "reason": "x"}).status_code in (403, 409),
               "a confirmer cannot submit on a stage-1 token")

            # ── stage 2 ───────────────────────────────────────────────────
            r = c.post("/api/claim", headers=C)
            ck(r.status_code == 200, f"stage-2 claim returns 200 ({r.status_code})")
            q = r.json()
            ck(q["case_id"] == "cobra_A270" and q["stage"] == 2, f"paired accept served first at stage 2 ({q['case_id']})")
            hits = scan(q, FORBIDDEN_STAGE2)
            ck(not hits, f"stage-2 payload has no stage-1 field, name, reason or verdict ({hits[:3]})")
            ck(q["verdicts"] == ["confirm", "overturn", "unsure"], "stage-2 verdict set")
            html2 = c.get(f"/case/{q['case_id']}", headers=C).text
            ck("(username withheld)" not in html2 and "REASON_MARKER_S1" not in html2 and "PRIOR_MARKER" not in html2,
               "stage-2 HTML page is blind to stage 1 and to the prior call")
            r = c.post("/api/submit", headers=C, data={"claim_token": q["claim_token"], "verdict": "confirm",
                                                       "reason": "agree: six lumbar-shaped bodies"})
            ck(r.status_code == 200 and r.json()["final"] == "confirmed", "confirm -> confirmed")
            q2 = c.post("/api/claim", headers=C).json()
            ck(q2["case_id"] == "ts_s0042", f"the stage-1 unsure reaches stage 2 ({q2['case_id']})")
            r = c.post("/api/submit", headers=C, data={"claim_token": q2["claim_token"], "verdict": "overturn",
                                                       "reason": "rib is full, cut by the field"})
            ck(r.status_code == 200 and r.json()["final"] == "overturned", "overturn -> overturned")
            ck(c.post("/api/claim", headers=C).status_code == 204, "rejected case never reaches stage 2 (queue empty)")
            ck(c.get("/api/case/ctsp_0005", headers=C).status_code == 403, "rejected case refused on direct GET")

            # ── audit ─────────────────────────────────────────────────────
            ck(c.get("/audit.csv", headers=C).status_code == 403, "audit.csv refused to the confirmer")
            ck(c.get("/audit.csv", headers=S).status_code == 403, "audit.csv refused to the screener")
            ck(c.get("/audit.csv").status_code == 401, "audit.csv refused without identity")
            r = c.get("/audit.csv", headers=A)
            ck(r.status_code == 200, "audit.csv served to admin")
            audit_text = r.text
            rows = {row["case_id"]: row for row in csv.DictReader(io.StringIO(audit_text))}
            ck(set(rows) == {"ctsp_0005", "cobra_A270", "ts_s0042"}, "audit has one row per case")
            ck(rows["cobra_A270"]["final"] == "confirmed" and rows["cobra_A270"]["stage1_user"] == "(username withheld)"
               and rows["cobra_A270"]["stage2_user"] == "CONFIRMER", "audit joins both stages on the paired case")
            ck(rows["ctsp_0005"]["final"] == "rejected" and rows["ctsp_0005"]["stage2_verdict"] == ""
               and rows["ctsp_0005"]["stage2_user"] == "", "rejected case has empty stage-2 columns")
            ck(rows["ts_s0042"]["stage1_verdict"] == "unsure" and rows["ts_s0042"]["stage2_verdict"] == "overturn",
               "unsure -> overturn joined")
            ck(rows["ctsp_0005"]["registry_subtype"] == "L6_PRIOR_MARKER" and rows["ts_s0042"]["prior_call"]
               == "STUMP_PRIOR_MARKER", "hidden manifest columns reach the audit table")
            ck(all(re.fullmatch(r"\d+", rows[k]["stage1_edit_seconds"]) for k in rows), "edit_seconds are ints")
            ck(all(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00", rows[k]["stage1_submitted_at"])
                   for k in rows), "timestamps are UTC ISO-8601")
            ck(rows["cobra_A270"]["prereg_sha256"] == prereg_sha, "audit rows carry the prereg sha256")

            # ── review records ────────────────────────────────────────────
            led = Ledger(LocalBackend(tree / "ledger"))
            recs = [rr for cid in rows for rr in led.list_reviews(cid)]
            ck(len(recs) == 5, f"five review records on disk (got {len(recs)})")
            for rr in recs:
                ok = (rr.get("prereg_sha256") == prereg_sha and rr.get("prereg_status") == prereg_status
                      and rr.get("tool") == "transitional_review.review_app" and rr.get("tool_version") == "1"
                      and re.fullmatch(r"\d{4}-\d\d-\d\dT.*\+00:00", rr.get("written_at_utc", ""))
                      and ("git_sha" in rr) and (rr["git_sha"] is None or re.fullmatch(r"[0-9a-f]{40}", rr["git_sha"]))
                      and "manifest.tsv" in rr.get("input_sha256", {})
                      and any(k.endswith("README.md") for k in rr["input_sha256"])
                      and any(k.endswith("evidence.json") for k in rr["input_sha256"])
                      and any(k.endswith("ap.png") for k in rr["input_sha256"])
                      and isinstance(rr.get("edit_seconds"), int) and rr.get("claimed_at") and rr.get("submitted_at"))
                if not ck(ok, f"record {rr.get('stage')}/{rr.get('case_id')} carries the full header"):
                    print("        ", {k: rr.get(k) for k in ("prereg_sha256", "prereg_status", "git_sha", "tool",
                                                              "tool_version", "written_at_utc", "edit_seconds")})
            ck(all(rr["prereg_status"] == "draft" for rr in recs) if prereg_status == "draft" else True,
               f"prereg_status recorded as {prereg_status!r} (the file's freeze block decides)")
            ck((tree / "ledger" / "reviews" / "cobra_A270").exists()
               and any(f.name.startswith("stage1_") for f in (tree / "ledger" / "reviews" / "cobra_A270").iterdir())
               and any(f.name.startswith("stage2_") for f in (tree / "ledger" / "reviews" / "cobra_A270").iterdir()),
               "review files named reviews/<case>/<stage>_<review_id>.json")

            # ── dashboard names ───────────────────────────────────────────
            dash = c.get("/").text
            ck("(username withheld)" not in dash and "CONFIRMER" not in dash, "dashboard prints no user name without --public-names")
            ck(">3<" in dash or "3 cases" in dash, "dashboard shows the case count")

            # ── login flow (cookie) ───────────────────────────────────────
            r = c.post("/login", data={"user": "(username withheld)", "token": "(username withheld)"}, follow_redirects=False)
            ck(r.status_code == 303 and "rv_session" in r.headers.get("set-cookie", ""), "login sets a session cookie")
            r = c.get("/work", follow_redirects=False)
            ck(r.status_code == 200 and "Queue empty" in r.text, "cookie session reaches /work")
            r = c.post("/login", data={"user": "(username withheld)", "token": "wrong"}, follow_redirects=False)
            ck(r.status_code == 401, "wrong token refused")

        # ── append-only across a restart ──────────────────────────────────
        before = snapshot(tree / "ledger")
        app2 = create_app(cfg)
        with TestClient(app2) as c:
            s = c.get("/api/status").json()
            ck(s["by_final"] == {"confirmed": 1, "rejected": 1, "overturned": 1} and s["n_review_records"] == 5,
               f"restart reproduces the counts ({s['by_final']})")
        after = snapshot(tree / "ledger")
        ck(before == after, "restart changes no ledger byte")
        led = Ledger(LocalBackend(tree / "ledger"))
        case = led.get_case("cobra_A270")
        case["history"] = case["history"][:1]
        try:
            led.put_case(case)
            ck(False, "truncated history refused")
        except LedgerError:
            ck(True, "truncated history refused")
        with open(tree / "manifest.tsv", "a", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter="\t", lineterminator="\n").writerow(
                ["verse_0700", "verse", "verse:700", "T13", "0", "count_5", "rule1", "0", "1", "T13_PRIOR", "read", "T13_PRIOR"])
        (tree / "cases" / "verse_0700").mkdir()
        (tree / "cases" / "verse_0700" / "README.md").write_text("# verse_0700\n")
        app3 = create_app(cfg)
        with TestClient(app3) as c:
            s = c.get("/api/status").json()
            ck(s["n_cases"] == 4 and s["by_final"].get("pending_stage1") == 1, "a new manifest row becomes one new case")
            cfg_pub = Config(**{**cfg.__dict__, "public_names": True})
        after2 = snapshot(tree / "ledger")
        ck(all(after2[k] == v for k, v in after.items()), "adding a case touches no existing ledger file")
        app4 = create_app(cfg_pub)
        with TestClient(app4) as c:
            ck("(username withheld)" in c.get("/").text, "--public-names shows reviewer names on the dashboard")

        print("\n[selftest] audit.csv:\n" + audit_text)
    except Exception:                                           # noqa: BLE001
        traceback.print_exc()
        ck.fails.append("exception during self-test")
    if ck.fails:
        print(f"[selftest] FAILED {len(ck.fails)} of {ck.n} checks:")
        for f in ck.fails:
            print(f"  - {f}")
    else:
        print(f"[selftest] PASSED {ck.n} checks")
    if not keep:
        shutil.rmtree(base, ignore_errors=True)
    return 1 if ck.fails else 0


if __name__ == "__main__":
    sys.exit(run())
