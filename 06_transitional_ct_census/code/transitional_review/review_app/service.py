# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/service.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/service.py -- the two-stage state machine (no FastAPI, no network; unit-testable on a fake tree).

Stage 1 (role screener): claim the next case in queue order (paired first, then type rank, then priority), see the
README, evidence, previews and viewer paths -- never the registry's prior call -- and submit accept / reject /
unsure with a reason. Stage 2 (role confirmer): only cases whose stage-1 verdict is accept or unsure are eligible;
the payload is built from scratch and holds no stage-1 field at all (verdict, reason, user, times, review id), and
the screener of a case can never be its confirmer. Timestamps are server-side at claim and at submit;
edit_seconds = submitted_at - claimed_at, computed here, and any client-sent value is ignored.

Final status: pending_stage1 | rejected (stage-1 reject; terminal, never reaches stage 2) | pending_stage2 |
confirmed | overturned | unresolved (stage-2 unsure).

Run: not a script; imported by app.py and selftest.py.
"""
from __future__ import annotations

import json
import uuid
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import manifest as mf
from .config import STAGE1_VERDICTS, STAGE2_VERDICTS, Config, Meta, sha256_file
from .ledger import Ledger, LedgerError

FINALS = ("pending_stage1", "rejected", "pending_stage2", "confirmed", "overturned", "unresolved")
STAGE_OF_ROLE = {"screener": 1, "confirmer": 2}
ROLE_OF_STAGE = {1: "screener", 2: "confirmer"}


class ReviewError(Exception):
    def __init__(self, msg: str, status: int = 400):
        super().__init__(msg)
        self.status = status


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s)


def final_status(case: dict) -> str:
    s1 = (case.get("stage1") or {}).get("done")
    s2 = (case.get("stage2") or {}).get("done")
    if not s1:
        return "pending_stage1"
    if s1["verdict"] == "reject":
        return "rejected"
    if not s2:
        return "pending_stage2"
    return {"confirm": "confirmed", "overturn": "overturned", "unsure": "unresolved"}[s2["verdict"]]


class Service:
    def __init__(self, cfg: Config, meta: Meta, man: mf.Manifest, ledger: Ledger):
        self.cfg = cfg
        self.meta = meta
        self.man = man
        self.ledger = ledger
        self._tokens: Dict[str, Tuple[str, int]] = {}      # claim_token -> (case_id, stage)
        self.orphans: List[str] = []                        # ledger cases no longer in the manifest
        self.sync_report: dict = {}

    # ── sync: manifest -> ledger (create only; never rewrite a result) ──────
    def sync(self) -> dict:
        created = changed = 0
        existing = {c["case_id"]: c for c in self.ledger.list_cases()}
        now = iso(utcnow())
        for cid in self.man.order:
            e = self.man.cases[cid]
            block = self._manifest_block(e)
            case = existing.get(cid)
            if case is None:
                case = {"case_id": cid, "created_at": now, "manifest": block,
                        "stage1": {"claim": None, "done": None}, "stage2": {"claim": None, "done": None},
                        "history": [{"event": "created", "at": now, "manifest_sha256": self.man.sha256}]}
                self.ledger.put_case(case, message=f"review: create {cid}")
                created += 1
            elif case.get("manifest", {}).get("row_sha256") != e.row_sha256:
                case["history"].append({"event": "manifest_row_changed", "at": now,
                                        "from": case.get("manifest", {}).get("row_sha256"),
                                        "to": e.row_sha256, "manifest_sha256": self.man.sha256})
                case["manifest"] = block
                self.ledger.put_case(case, message=f"review: manifest row changed {cid}")
                changed += 1
            for stage in (1, 2):
                cl = (case.get(f"stage{stage}") or {}).get("claim")
                if cl and cl.get("claim_token"):
                    self._tokens[cl["claim_token"]] = (cid, stage)
        self.orphans = sorted(set(existing) - set(self.man.cases))
        self.sync_report = {"created": created, "changed": changed, "orphans": len(self.orphans),
                            "n_manifest": len(self.man.order), "n_ledger": len(existing) + created}
        return self.sync_report

    def _manifest_block(self, e: mf.CaseEntry) -> dict:
        return {"type": e.type, "paired": e.paired, "flags": e.flags, "rules": e.rules, "priority": e.priority,
                "collection": e.collection, "person_key": e.person_key,
                "case_dir": mf.rel(self.man.root, e.case_dir), "visible": e.visible, "hidden": e.hidden,
                "row_sha256": e.row_sha256}

    # ── claims ──────────────────────────────────────────────────────────────
    def _expired(self, claim: Optional[dict]) -> bool:
        if not claim:
            return True
        try:
            return parse_iso(claim["expires_at"]) < utcnow()
        except Exception:                                       # noqa: BLE001
            return True

    def _open_claim(self, case: dict, stage: int) -> Optional[dict]:
        cl = (case.get(f"stage{stage}") or {}).get("claim")
        return cl if cl and not self._expired(cl) else None

    def _eligible(self, case: dict, stage: int, user: str) -> bool:
        st = case.get(f"stage{stage}") or {}
        if st.get("done"):
            return False
        if stage == 2:
            s1 = (case.get("stage1") or {}).get("done")
            if not s1 or s1["verdict"] not in ("accept", "unsure"):
                return False
            if s1["user"].lower() == user.lower():
                return False                                    # the screener never confirms her own screen
        cl = self._open_claim(case, stage)
        return cl is None or cl["user"].lower() == user.lower()

    def queue(self, stage: int, user: str) -> List[mf.CaseEntry]:
        out = []
        for cid in self.man.order:
            case = self.ledger.get_case(cid)
            if case and self._eligible(case, stage, user):
                out.append(self.man.cases[cid])
        out.sort(key=self.man.queue_key)
        return out

    def claim(self, user: str, role: str) -> Optional[dict]:
        stage = STAGE_OF_ROLE.get(role)
        if stage is None:
            raise ReviewError(f"role {role!r} does not claim cases", 403)
        # one case at a time: an open claim of this user is served again, not a second one
        for cid in self.man.order:
            case = self.ledger.get_case(cid)
            cl = case and self._open_claim(case, stage)
            if cl and cl["user"].lower() == user.lower() and not (case.get(f"stage{stage}") or {}).get("done"):
                return self._payload(self.man.cases[cid], case, stage, cl)
        q = self.queue(stage, user)
        if not q:
            return None
        e = q[0]
        case = self.ledger.get_case(e.case_id)
        now = utcnow()
        token = f"s{stage}.{uuid.uuid4().hex}"
        inputs = self._input_hashes(e)
        cl = {"user": user, "claim_token": token, "claimed_at": iso(now),
              "expires_at": iso(now + timedelta(seconds=self.cfg.claim_ttl_seconds)), "input_sha256": inputs}
        case[f"stage{stage}"]["claim"] = cl
        case["history"].append({"event": f"stage{stage}_claimed", "at": cl["claimed_at"], "user": user,
                                "claim_token": token})
        self.ledger.put_case(case, message=f"review: claim stage{stage} {e.case_id}")
        self._tokens[token] = (e.case_id, stage)
        return self._payload(e, case, stage, cl)

    def release(self, user: str, claim_token: str) -> dict:
        cid, stage, case, cl = self._resolve(claim_token)
        if cl["user"].lower() != user.lower():
            raise ReviewError("that claim is not yours", 403)
        now = iso(utcnow())
        case[f"stage{stage}"]["claim"] = None
        case["history"].append({"event": f"stage{stage}_released", "at": now, "user": user, "claim_token": claim_token})
        self.ledger.put_case(case, message=f"review: release stage{stage} {cid}")
        self._tokens.pop(claim_token, None)
        return {"case_id": cid, "stage": stage, "released": True}

    def _resolve(self, claim_token: str):
        hit = self._tokens.get(claim_token)
        if hit is None:                                          # restart-safe: scan the ledger once
            for c in self.ledger.list_cases():
                for stage in (1, 2):
                    cl = (c.get(f"stage{stage}") or {}).get("claim")
                    if cl and cl.get("claim_token") == claim_token:
                        hit = (c["case_id"], stage)
                        self._tokens[claim_token] = hit
        if hit is None:
            raise ReviewError("claim token does not match an open claim", 409)
        cid, stage = hit
        case = self.ledger.get_case(cid)
        cl = (case or {}).get(f"stage{stage}", {}).get("claim")
        if not case or not cl or cl.get("claim_token") != claim_token:
            raise ReviewError("claim token does not match an open claim", 409)
        return cid, stage, case, cl

    # ── what a reviewer is served ───────────────────────────────────────────
    def _input_hashes(self, e: mf.CaseEntry) -> Dict[str, str]:
        h = {"manifest.tsv": self.man.sha256, str(self.meta.prereg_path): self.meta.prereg_sha256}
        if self.man.types_path:
            h["types.tsv"] = self.man.types_sha256
        r = e.case_dir / "README.md"
        if r.exists():
            h[mf.rel(self.man.root, r)] = sha256_file(r)
        ev = e.case_dir / "evidence.json"
        if ev.exists():
            h[mf.rel(self.man.root, ev)] = sha256_file(ev)
        oc = e.case_dir / "open_commands.json"
        if oc.exists():
            h[mf.rel(self.man.root, oc)] = sha256_file(oc)
        for p in mf.case_previews(e):
            h[mf.rel(self.man.root, p)] = sha256_file(p)
        return h

    def _payload(self, e: mf.CaseEntry, case: dict, stage: int, cl: dict) -> dict:
        """Everything a reviewer at `stage` may see. Built from the manifest entry and the case directory only;
        the ledger's stage results are never consulted, so a stage-2 payload cannot carry stage-1 fields."""
        readme, _ = mf.read_case_readme(e)
        evidence, _, ev_err = mf.read_case_evidence(e, self.cfg.hidden_prefixes)
        files = mf.case_files(self.man.root, e)
        previews = mf.case_previews(e)
        missing = list(e.problems)
        if readme is None:
            missing.append("README.md missing")
        if ev_err:
            missing.append(ev_err)
        out = {
            "case_id": e.case_id, "stage": stage, "role": ROLE_OF_STAGE[stage],
            "claim_token": cl["claim_token"], "claimed_at": cl["claimed_at"], "expires_at": cl["expires_at"],
            "type": e.type, "type_meaning": self.man.type_meaning(e.type), "paired": e.paired,
            "flags": list(e.flags), "rules": list(e.rules), "collection": e.collection,
            "person_key": e.person_key, "priority": e.priority,
            "manifest": mf.strip_hidden(dict(e.visible), self.cfg.hidden_prefixes),
            "readme_md": readme, "evidence": evidence,
            "previews": [f"/case/{e.case_id}/preview/{p.name}" for p in previews],
            "files": files,
            "open_commands": mf.open_commands(self.man.root, e, files, self.cfg.reviewer_tree_path),
            "tree_root": self.cfg.reviewer_tree_path or self.man.root.as_posix(),
            "missing": missing,
            "verdicts": list(STAGE1_VERDICTS if stage == 1 else STAGE2_VERDICTS),
            "reason_required": self.cfg.reason_required,
        }
        if stage == 2 and self.cfg.show_prior_to_confirmer:
            raw_ev = None
            p = e.case_dir / "evidence.json"
            if p.exists():
                try:
                    raw_ev = json.loads(p.read_text(encoding="utf-8-sig"))
                except Exception:                                # noqa: BLE001
                    raw_ev = None
            out["prior"] = {"manifest": dict(e.hidden),
                            "evidence_hidden": (raw_ev or {}).get("hidden") if isinstance(raw_ev, dict) else None}
        return out

    def view(self, case_id: str, user: str, role: str) -> dict:
        e = self.man.cases.get(case_id)
        case = self.ledger.get_case(case_id)
        if e is None or case is None:
            raise ReviewError(f"unknown case {case_id}", 404)
        stage = STAGE_OF_ROLE.get(role)
        if stage is None:
            raise ReviewError("admins read the audit table, not case pages", 403)
        cl = self._open_claim(case, stage)
        if not cl or cl["user"].lower() != user.lower():
            raise ReviewError("you do not hold the claim on this case", 403)
        return self._payload(e, case, stage, cl)

    def preview_path(self, case_id: str, name: str, user: str, role: str) -> Path:
        if "/" in name or "\\" in name or name.startswith("."):
            raise ReviewError("bad preview name", 400)
        e = self.man.cases.get(case_id)
        case = self.ledger.get_case(case_id)
        if e is None or case is None:
            raise ReviewError(f"unknown case {case_id}", 404)
        stage = STAGE_OF_ROLE.get(role)
        if stage is None:
            raise ReviewError("no preview access for this role", 403)
        cl = self._open_claim(case, stage)
        if not cl or cl["user"].lower() != user.lower():
            raise ReviewError("you do not hold the claim on this case", 403)
        p = e.case_dir / "previews" / name
        if not p.is_file():
            raise ReviewError("no such preview", 404)
        return p

    # ── submit ──────────────────────────────────────────────────────────────
    def _find_done(self, claim_token: str):
        """The (case, stage, done) whose recorded verdict was submitted under this token, or None."""
        for c in self.ledger.list_cases():
            for stage in (1, 2):
                d = (c.get(f"stage{stage}") or {}).get("done")
                if d and d.get("claim_token") == claim_token:
                    return c, stage, d
        return None

    def submit(self, user: str, role: str, claim_token: str, verdict: str, reason: str) -> dict:
        try:
            cid, stage, case, cl = self._resolve(claim_token)
        except ReviewError:
            # A lost response makes a client re-send the same verdict; the claim is closed by then. The same
            # user, verdict and reason under the same token is a no-op, anything else is the original refusal.
            hit = self._find_done(claim_token)
            if hit and hit[2]["user"].lower() == user.lower() and hit[2]["verdict"] == (verdict or "").strip().lower() \
                    and hit[2]["reason"] == (reason or "").strip():
                return {"case_id": hit[0]["case_id"], "stage": hit[1], "duplicate": True,
                        "final": final_status(hit[0])}
            raise
        if STAGE_OF_ROLE.get(role) != stage:
            raise ReviewError(f"role {role!r} cannot submit a stage-{stage} verdict", 403)
        if cl["user"].lower() != user.lower():
            raise ReviewError("that claim is not yours", 403)
        verdict = (verdict or "").strip().lower()
        allowed = STAGE1_VERDICTS if stage == 1 else STAGE2_VERDICTS
        if verdict not in allowed:
            raise ReviewError(f"stage-{stage} verdict must be one of {allowed}", 400)
        reason = (reason or "").strip()
        if self.cfg.reason_required and not reason:
            raise ReviewError("a reason is required with every verdict", 400)
        st = case[f"stage{stage}"]
        if st.get("done"):
            d = st["done"]
            if d.get("claim_token") == claim_token and d["verdict"] == verdict and d["reason"] == reason:
                return {"case_id": cid, "stage": stage, "duplicate": True, "final": final_status(case)}
            raise ReviewError("this case was already submitted", 409)
        if self._expired(cl):
            raise ReviewError("claim expired; claim again", 409)
        now = utcnow()
        claimed = parse_iso(cl["claimed_at"])
        edit_seconds = max(0, int(round((now - claimed).total_seconds())))
        review_id = uuid.uuid4().hex
        e = self.man.cases[cid]
        rec = dict(self.meta.as_dict())
        rec.update({
            "written_at_utc": iso(now), "input_sha256": cl.get("input_sha256", {}),
            "manifest_sha256": self.man.sha256, "manifest_row_sha256": e.row_sha256,
            "review_id": review_id, "case_id": cid, "stage": stage, "role": role, "user": user,
            "verdict": verdict, "reason": reason,
            "claimed_at": cl["claimed_at"], "submitted_at": iso(now), "edit_seconds": edit_seconds,
            "claim_token": claim_token, "case_type": e.type, "paired": e.paired, "flags": list(e.flags),
            "rules": list(e.rules), "collection": e.collection, "person_key": e.person_key,
        })
        rpath = self.ledger.review_path(cid, stage, review_id)
        st["done"] = {"review_id": review_id, "user": user, "verdict": verdict, "reason": reason,
                      "claimed_at": cl["claimed_at"], "submitted_at": rec["submitted_at"],
                      "edit_seconds": edit_seconds, "review_path": rpath, "claim_token": claim_token}
        st["claim"] = None
        case["history"].append({"event": f"stage{stage}_submitted", "at": rec["submitted_at"], "user": user,
                                "verdict": verdict, "review_id": review_id})
        try:
            self.ledger.put_case(case, extra_files={rpath: json.dumps(rec, indent=2)},
                                 message=f"review: submit stage{stage} {cid} {verdict}")
        except LedgerError as exc:
            raise ReviewError(str(exc), 500)
        self._tokens.pop(claim_token, None)
        return {"case_id": cid, "stage": stage, "verdict": verdict, "review_id": review_id,
                "edit_seconds": edit_seconds, "final": final_status(case)}

    # ── audit + status ──────────────────────────────────────────────────────
    def audit_rows(self) -> List[dict]:
        rows = []
        hidden_cols: List[str] = []
        for cid in self.man.order:
            for k in self.man.cases[cid].hidden:
                if k not in hidden_cols:
                    hidden_cols.append(k)
        ids = list(self.man.order) + [o for o in self.orphans]
        for cid in ids:
            case = self.ledger.get_case(cid)
            if case is None:
                continue
            m = case.get("manifest", {})
            row = {"case_id": cid, "in_manifest": int(cid in self.man.cases),
                   "collection": m.get("collection", ""), "person_key": m.get("person_key", ""),
                   "type": m.get("type", ""), "paired": int(bool(m.get("paired"))),
                   "flags": ";".join(m.get("flags", [])), "rules": ";".join(m.get("rules", [])),
                   "priority": m.get("priority", 0)}
            for stage in (1, 2):
                d = (case.get(f"stage{stage}") or {}).get("done") or {}
                cl = self._open_claim(case, stage) or {}
                p = f"stage{stage}_"
                row[p + "verdict"] = d.get("verdict", "")
                row[p + "reason"] = d.get("reason", "")
                row[p + "user"] = d.get("user", "")
                row[p + "claimed_at"] = d.get("claimed_at", cl.get("claimed_at", ""))
                row[p + "submitted_at"] = d.get("submitted_at", "")
                row[p + "edit_seconds"] = d.get("edit_seconds", "")
                row[p + "review_id"] = d.get("review_id", "")
                row[p + "open_claim_user"] = cl.get("user", "")
            row["final"] = final_status(case)
            for k in hidden_cols:
                row[k] = (m.get("hidden") or {}).get(k, "")
            row.update({"prereg_sha256": self.meta.prereg_sha256, "prereg_status": self.meta.prereg_status,
                        "git_sha": self.meta.git_sha or "", "tool": self.meta.tool,
                        "tool_version": self.meta.tool_version})
            rows.append(row)
        return rows

    def status(self) -> dict:
        by_final: Counter = Counter()
        by_type: Dict[str, Counter] = {}
        by_user: Counter = Counter()
        paired = Counter()
        for cid in self.man.order:
            case = self.ledger.get_case(cid)
            if case is None:
                continue
            f = final_status(case)
            t = case["manifest"]["type"]
            by_final[f] += 1
            by_type.setdefault(t, Counter())[f] += 1
            paired["paired" if case["manifest"].get("paired") else "ct_only"] += 1
            for stage in (1, 2):
                d = (case.get(f"stage{stage}") or {}).get("done")
                if d:
                    by_user[f"{d['user']} (stage {stage})"] += 1
        return {"n_cases": len(self.man.order), "by_final": dict(by_final),
                "by_type": {t: dict(c) for t, c in sorted(by_type.items(), key=lambda kv: self.man.type_rank(kv[0]))},
                "paired": dict(paired),
                "queue_stage1": by_final.get("pending_stage1", 0), "queue_stage2": by_final.get("pending_stage2", 0),
                "reviews_by_user": dict(by_user), "orphans": len(self.orphans),
                "manifest_sha256": self.man.sha256, "prereg_sha256": self.meta.prereg_sha256,
                "prereg_status": self.meta.prereg_status, "git_sha": self.meta.git_sha,
                "tool": self.meta.tool, "tool_version": self.meta.tool_version,
                "n_review_records": self.ledger.count_reviews()}
