# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/ledger.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/ledger.py -- the append-only ledger on disk (and an optional mirror to a private HF dataset).

Layout under <tree>/ledger/ (or --ledger):
    cases/<case_id>.json                       claims, the two stage results, and a `history` list of events
    reviews/<case_id>/<stage>_<review_id>.json one immutable record per submitted verdict

Append-only is enforced, not assumed: a review file is never overwritten (put_review refuses if the path exists),
and put_case refuses a case whose `history` is not an extension of the stored one. A re-run therefore cannot lose a
record: sync only creates case files that do not exist, and never rewrites an existing one except by appending an
event. Writes are atomic (tmp + os.replace).

Run: not a script; imported by service.py. The optional HFMirror (REVIEW_LEDGER_REPO + HF_TOKEN) pulls the ledger
at startup without overwriting local files and pushes every written file in one commit per write; it is not
exercised by the self-test (no network) and every failure is logged, never swallowed silently.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

_SAFE = re.compile(r"[^A-Za-z0-9._:@-]+")


def safe_name(s: str) -> str:
    """A case id as a file name: only characters that are safe on Windows, macOS and Linux."""
    return _SAFE.sub("_", str(s)).replace(":", "_")


class LedgerError(Exception):
    pass


class LocalBackend:
    """Filesystem persistence with atomic writes."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _p(self, rel: str) -> Path:
        return self.root / rel

    def exists(self, rel: str) -> bool:
        return self._p(rel).exists()

    def read_text(self, rel: str) -> Optional[str]:
        p = self._p(rel)
        return p.read_text(encoding="utf-8") if p.exists() else None

    def write_text(self, rel: str, text: str) -> None:
        p = self._p(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".tmp_", dir=str(p.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            os.replace(tmp, p)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    def list(self, prefix: str) -> List[str]:
        base = self._p(prefix)
        if not base.exists():
            return []
        return sorted(p.relative_to(self.root).as_posix() for p in base.rglob("*") if p.is_file())


class HFMirror:
    """Mirror of the ledger in a private HF dataset repo. pull() never overwrites a local file; push() writes the
    given files in one commit. Any failure is printed with its cause and re-raised by push (a lost record is a
    failure, not a warning) and only printed by pull (a missing mirror must not stop a local run)."""

    def __init__(self, repo_id: str, token: str, local: LocalBackend):
        from huggingface_hub import HfApi, create_repo
        self.api = HfApi(token=token)
        self.repo_id = repo_id
        self.token = token
        self.local = local
        create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True, token=token)

    def pull(self) -> int:
        try:
            from huggingface_hub import snapshot_download
            d = snapshot_download(repo_id=self.repo_id, repo_type="dataset", token=self.token,
                                  allow_patterns=["cases/*.json", "reviews/**/*.json"])
        except Exception as exc:                                # noqa: BLE001
            print(f"[ledger] HF mirror pull failed ({exc}); continuing on the local ledger", file=sys.stderr)
            return 0
        n = 0
        for p in Path(d).rglob("*.json"):
            r = p.relative_to(d).as_posix()
            if not self.local.exists(r):
                self.local.write_text(r, p.read_text(encoding="utf-8"))
                n += 1
        return n

    def push(self, files: Dict[str, str], message: str) -> None:
        from huggingface_hub import CommitOperationAdd
        ops = [CommitOperationAdd(path_in_repo=k, path_or_fileobj=v.encode("utf-8")) for k, v in files.items()]
        self.api.create_commit(repo_id=self.repo_id, repo_type="dataset", token=self.token,
                               operations=ops, commit_message=message)


class Ledger:
    def __init__(self, backend: LocalBackend, mirror: Optional[HFMirror] = None):
        self.b = backend
        self.mirror = mirror

    # cases ------------------------------------------------------------------
    def case_path(self, case_id: str) -> str:
        return f"cases/{safe_name(case_id)}.json"

    def get_case(self, case_id: str) -> Optional[dict]:
        t = self.b.read_text(self.case_path(case_id))
        return json.loads(t) if t else None

    def list_cases(self) -> List[dict]:
        out = []
        for r in self.b.list("cases/"):
            if r.endswith(".json"):
                t = self.b.read_text(r)
                if t:
                    out.append(json.loads(t))
        return out

    def _check_append_only(self, case: dict) -> None:
        old = self.get_case(case["case_id"])
        if old is None:
            return
        oh, nh = old.get("history", []), case.get("history", [])
        if len(nh) < len(oh) or nh[:len(oh)] != oh:
            raise LedgerError(f"refusing to write case {case['case_id']}: history is not an extension of the "
                              f"stored one ({len(oh)} -> {len(nh)} events)")
        for stage in ("stage1", "stage2"):
            od = (old.get(stage) or {}).get("done")
            nd = (case.get(stage) or {}).get("done")
            if od and od != nd:
                raise LedgerError(f"refusing to write case {case['case_id']}: {stage} result would change")

    def put_case(self, case: dict, extra_files: Optional[Dict[str, str]] = None, message: str = "") -> None:
        self._check_append_only(case)
        files = dict(extra_files or {})
        files[self.case_path(case["case_id"])] = json.dumps(case, indent=2, sort_keys=False)
        for rel_path, text in files.items():
            if rel_path.startswith("reviews/") and self.b.exists(rel_path):
                raise LedgerError(f"refusing to overwrite review record {rel_path}")
        for rel_path, text in files.items():
            self.b.write_text(rel_path, text)
        if self.mirror is not None:
            try:
                self.mirror.push(files, message or f"review: {case['case_id']}")
            except Exception as exc:                            # noqa: BLE001
                print(f"[ledger] HF mirror push FAILED for {sorted(files)}: {exc}", file=sys.stderr)
                raise

    # reviews ----------------------------------------------------------------
    def review_path(self, case_id: str, stage: int, review_id: str) -> str:
        return f"reviews/{safe_name(case_id)}/stage{int(stage)}_{review_id}.json"

    def list_reviews(self, case_id: str) -> List[dict]:
        out = []
        for r in self.b.list(f"reviews/{safe_name(case_id)}/"):
            if r.endswith(".json"):
                t = self.b.read_text(r)
                if t:
                    out.append(json.loads(t))
        return out

    def count_reviews(self) -> int:
        return sum(1 for r in self.b.list("reviews/") if r.endswith(".json"))
