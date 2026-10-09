# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/config.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/config.py -- one Config object built from CLI flags and environment; nothing else reads os.environ.

Inputs: CLI namespace (see __main__.py) and the REVIEW_* environment variables listed in __init__.py.
Outputs: a frozen Config plus the record header (`Meta`) every review row carries: prereg sha256 + status,
git SHA of this repository, tool name and version.
Run: not a script; imported by __main__.py and selftest.py.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Tuple

from . import TOOL_NAME, TOOL_VERSION

ROLES = ("screener", "confirmer", "admin")
STAGE1_VERDICTS = ("accept", "reject", "unsure")
STAGE2_VERDICTS = ("confirm", "overturn", "unsure")

# Manifest columns / evidence keys a reviewer must never see. A key is hidden when its lower-cased name starts
# with one of these prefixes, or when it sits under a top-level "hidden" object in evidence.json. The prefixes
# are deliberately narrow: rule-1's own flag `castellvi_II_IV_candidate` is evidence and IS shown.
DEFAULT_HIDDEN_PREFIXES = ("registry", "prior", "truth", "read_", "labeller", "consensus", "hidden")

# Queue order after "paired first": the census subtypes PREREG section 5 reports on, in the order the review is
# most useful (a count disagreement is worth more than an unvalidated shape score). A tree may override this
# with types.tsv (type, rank, meaning). Unknown types sort after these, alphabetically.
DEFAULT_TYPES: Tuple[Tuple[str, str], ...] = (
    ("L6", "six free bodies between the lowest full rib and the sacrum; a true L6 or a T12 that lost its rib"),
    ("T13", "a thirteenth rib-bearing vertebra (only decidable when the whole cage is in the field)"),
    ("four_lumbar", "four free bodies: a fused (sacralised) L5, or a lumbar rib on L1 that stole the count"),
    ("complete_sacralisation", "a body more than half inside the sacrum label (rule 1 f >= 0.50)"),
    ("castellvi_II_IV", "a body in contact with the sacrum (0.10 <= f < 0.50): partial sacralisation candidate"),
    ("lumbarisation", "a free body lying wholly below the sacral anchor (a mobile S1)"),
    ("lumbar_rib", "a short rib on the first lumbar-shaped body"),
    ("stump_rib", "the lowest rib is 38 mm or shorter (not cut by the field edge) under a full rib above"),
    ("sacral_shape", "rule 2 puts a pelvic or sacral feature outside the reference 95 % band (no validated cut yet)"),
    ("labeller_disagreement", "SPINEPS/VERIDAH and TotalSegmentator disagree on the count or on what the sacrum absorbed"),
    ("no_anchor", "the sacrum could not anchor a count (absent, < 5 mL, at the caudal edge, or anchors > 20 mm apart)"),
    ("ordinary_control", "a five-count spine drawn as a control; reviewed exactly like the others"),
)


@dataclass(frozen=True)
class Meta:
    """The header fields every written row carries (PREREG section 0 / section 9)."""
    prereg_path: str
    prereg_sha256: Optional[str]
    prereg_status: str
    git_sha: Optional[str]
    git_sha_error: Optional[str]
    tool: str = TOOL_NAME
    tool_version: str = TOOL_VERSION

    def as_dict(self) -> dict:
        return {
            "prereg_path": self.prereg_path, "prereg_sha256": self.prereg_sha256,
            "prereg_status": self.prereg_status, "git_sha": self.git_sha,
            "git_sha_error": self.git_sha_error, "tool": self.tool, "tool_version": self.tool_version,
        }


@dataclass
class Config:
    root: Path
    ledger_dir: Path
    prereg_path: Path
    screener: str = "(username withheld)"
    confirmer: str = "CONFIRMER"
    admins: Tuple[str, ...] = ("admin",)
    users: Dict[str, dict] = field(default_factory=dict)     # name -> {"token": str, "role": str}
    dev_tokens: bool = False                                  # token == username (no REVIEW_USERS given)
    public_names: bool = False
    claim_ttl_seconds: int = 3 * 24 * 3600
    hidden_prefixes: Tuple[str, ...] = DEFAULT_HIDDEN_PREFIXES
    show_prior_to_confirmer: bool = False
    reason_required: bool = True
    reviewer_tree_path: Optional[str] = None                  # how the tree is mounted on the reviewer's machine
    ledger_repo: Optional[str] = None                         # optional HF dataset mirror of the ledger
    hf_token: Optional[str] = None
    title: str = "Transitional-vertebra review"

    def role_of(self, username: str) -> Optional[str]:
        u = (username or "").strip()
        if not u:
            return None
        rec = self.users.get(u) or self.users.get(u.lower())
        if rec and rec.get("role") in ROLES:
            return rec["role"]
        ul = u.lower()
        if ul in {a.lower() for a in self.admins}:
            return "admin"
        if ul == self.confirmer.lower():
            return "confirmer"
        if ul == self.screener.lower():
            return "screener"
        return None


# ── helpers ──────────────────────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


_FREEZE_RE = re.compile(r"sha256 of this file:\s*([0-9a-fA-F_]+)")


def prereg_status_of(text: str) -> str:
    """'frozen' once the freeze block (PREREG section 9) holds a real sha256; 'draft' otherwise."""
    m = _FREEZE_RE.search(text or "")
    if m and re.fullmatch(r"[0-9a-fA-F]{64}", m.group(1)):
        return "frozen"
    return "draft"


def git_head(cwd: Path) -> Tuple[Optional[str], Optional[str]]:
    """The repository's HEAD sha, or (None, why). In a container with no .git, GIT_SHA (env, baked at build)
    or a GIT_SHA file beside the package stands in; otherwise the row says the sha is unknown, not a guess."""
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(cwd), capture_output=True, text=True,
                             timeout=20)
        if out.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", out.stdout.strip()):
            return out.stdout.strip(), None
        err = (out.stderr or out.stdout).strip()[:200]
    except Exception as exc:                                    # noqa: BLE001
        err = f"{type(exc).__name__}: {exc}"[:200]
    env = os.environ.get("GIT_SHA", "").strip()
    if re.fullmatch(r"[0-9a-f]{40}", env):
        return env, None
    f = Path(__file__).resolve().parent / "GIT_SHA"
    if f.exists():
        v = f.read_text().strip()
        if re.fullmatch(r"[0-9a-f]{40}", v):
            return v, None
    return None, f"git rev-parse failed ({err}); no GIT_SHA env or file"


def build_meta(prereg_path: Path) -> Meta:
    if not prereg_path.exists():
        raise FileNotFoundError(
            f"PREREG_rules.md not found at {prereg_path}; every row must carry its sha256, so the app refuses "
            f"to start. Pass --prereg <path> or put a copy at <tree>/PREREG_rules.md.")
    text = prereg_path.read_text(encoding="utf-8", errors="replace")
    sha, err = git_head(Path(__file__).resolve().parent)
    return Meta(prereg_path=str(prereg_path), prereg_sha256=sha256_file(prereg_path),
                prereg_status=prereg_status_of(text), git_sha=sha, git_sha_error=err)


def default_prereg_path(root: Path) -> Path:
    """The tree's own copy first (the tree was built against it), else this repository's docs/ruleclass copy."""
    tree_copy = root / "PREREG_rules.md"
    if tree_copy.exists():
        return tree_copy
    here = Path(__file__).resolve()
    if len(here.parents) > 3:                                   # repo checkout: tools/transitional_review/review_app
        return here.parents[3] / "docs" / "ruleclass" / "PREREG_rules.md"
    return Path("docs/ruleclass/PREREG_rules.md")                # container: set REVIEW_PREREG instead


def load_users(raw: Optional[str]) -> Dict[str, dict]:
    """REVIEW_USERS: a JSON object or a path to one. {"name": {"token": "...", "role": "screener"}}"""
    if not raw:
        return {}
    raw = raw.strip()
    if not raw.startswith("{") and Path(raw).exists():
        raw = Path(raw).read_text(encoding="utf-8")
    users = json.loads(raw)
    out: Dict[str, dict] = {}
    for name, rec in users.items():
        if not isinstance(rec, dict) or not rec.get("token"):
            raise ValueError(f"REVIEW_USERS[{name!r}] needs a token")
        role = rec.get("role", "screener")
        if role not in ROLES:
            raise ValueError(f"REVIEW_USERS[{name!r}] role {role!r} not in {ROLES}")
        out[name] = {"token": str(rec["token"]), "role": role}
    return out


def config_from_args(a) -> Config:
    """CLI first, environment second, defaults last. `a` is the argparse namespace from __main__.py."""
    env = os.environ
    root = Path(a.root or env.get("REVIEW_ROOT", "")).expanduser()
    if not str(root):
        raise SystemExit("--root <tree> (or REVIEW_ROOT) is required")
    root = root.resolve()
    ledger = Path(a.ledger or env.get("REVIEW_LEDGER", "") or (root / "ledger")).expanduser().resolve()
    prereg = Path(a.prereg or env.get("REVIEW_PREREG", "") or default_prereg_path(root)).expanduser().resolve()
    users = load_users(a.users or env.get("REVIEW_USERS"))
    admins = tuple(x for x in re.split(r"[,\s]+", a.admins or env.get("REVIEW_ADMINS", "admin")) if x)
    cfg = Config(
        root=root, ledger_dir=ledger, prereg_path=prereg,
        screener=a.screener or env.get("REVIEW_SCREENER", "(username withheld)"),
        confirmer=a.confirmer or env.get("REVIEW_CONFIRMER", "CONFIRMER"),
        admins=admins, users=users, dev_tokens=not users,
        public_names=bool(a.public_names or env.get("REVIEW_PUBLIC_NAMES", "") in ("1", "true", "yes")),
        claim_ttl_seconds=int(a.claim_ttl or env.get("REVIEW_CLAIM_TTL", 3 * 24 * 3600)),
        show_prior_to_confirmer=bool(a.show_prior_to_confirmer),
        reason_required=not a.reason_optional,
        reviewer_tree_path=a.reviewer_tree_path or env.get("REVIEW_REVIEWER_TREE_PATH") or None,
        ledger_repo=a.ledger_repo or env.get("REVIEW_LEDGER_REPO") or None,
        hf_token=env.get("HF_TOKEN") or None,
    )
    return cfg
