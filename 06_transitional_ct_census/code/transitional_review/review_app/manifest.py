# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/manifest.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/manifest.py -- read the review tree: manifest.tsv, types.tsv, and what each case directory holds.

THE CONTRACT this reader accepts (the tree builder writes it; nothing here is inferred from a segmentation):

  <tree>/manifest.tsv   tab-separated, UTF-8, one row per case.
      required   case_id     unique; CTSP ids are zfill(4) upstream, this reader only checks uniqueness
                 type        one of types.tsv / DEFAULT_TYPES, or any string (unknown types queue last)
      optional   paired      1/0, true/false, yes/no  -> paired cases are claimed first
                 flags       `;`-separated rule flags (shown)      rules   `;`-separated rules that raised it
                 collection, person_key, tier, priority (int, higher first within a type)
                 case_dir    relative to the tree; default cases/<case_id>
                 registry_*, prior_*, truth_*, labeller_*, read_*, consensus_*   HIDDEN from both reviewers,
                             carried into audit.csv (the registry's prior call goes here, e.g. registry_subtype)
      any other column is shown to the reviewer as-is.
  <tree>/types.tsv      optional: type, rank, meaning.  Overrides the default queue order and meanings.
  <tree>/cases/<case_id>/
      README.md          shown, rendered from Markdown (must not carry the registry call; the app warns if the
                         word "registry" appears, it cannot blind free text)
      evidence.json      shown as a key/value table; a top-level "hidden" object and hidden-prefixed keys are
                         stripped before serving
      previews/*.png     served as images
      ct*.nii.gz, masks/*.nii.gz, labels/*.txt, case.mrb, make_slicer_scene.py, xr_<view>_P.txt
                         only their paths are shown, with an open command per viewer
      open_commands.json optional {"slicer": "...", "itksnap": "...", "imfusion": "..."} overrides the
                         commands the app would compose from the files above

Run: not a script. `python -m review_app --root <tree> --check` prints this reader's validation report.
"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import DEFAULT_TYPES, sha256_bytes, sha256_file

TRUE_WORDS = {"1", "true", "yes", "y", "t", "paired"}
FALSE_WORDS = {"0", "false", "no", "n", "f", "", "none", "nan", "unpaired"}


def parse_bool(v) -> bool:
    s = str(v if v is not None else "").strip().lower()
    if s in TRUE_WORDS:
        return True
    if s in FALSE_WORDS:
        return False
    raise ValueError(f"not a boolean: {v!r}")


def split_list(v) -> List[str]:
    s = str(v or "").strip()
    if not s or s.lower() in ("nan", "none"):
        return []
    return [x.strip() for x in re.split(r"[;|]", s) if x.strip()]


def is_hidden_key(key: str, prefixes) -> bool:
    k = str(key).strip().lower()
    return any(k.startswith(p) for p in prefixes)


def strip_hidden(obj, prefixes):
    """Recursively drop dict keys a reviewer must not see. Lists and scalars pass through."""
    if isinstance(obj, dict):
        return {k: strip_hidden(v, prefixes) for k, v in obj.items() if not is_hidden_key(k, prefixes)}
    if isinstance(obj, list):
        return [strip_hidden(v, prefixes) for v in obj]
    return obj


@dataclass
class TypeInfo:
    name: str
    rank: int
    meaning: str


@dataclass
class CaseEntry:
    case_id: str
    type: str
    paired: bool
    flags: List[str]
    rules: List[str]
    priority: int
    collection: str
    person_key: str
    case_dir: Path                       # absolute
    visible: Dict[str, str]              # manifest columns a reviewer may see (excluding the keyed ones above)
    hidden: Dict[str, str]               # manifest columns that go to audit.csv only
    row_sha256: str                      # sha256 of the tab-joined raw row (stable identity of the row)
    problems: List[str] = field(default_factory=list)


@dataclass
class Manifest:
    root: Path
    path: Path
    sha256: str
    columns: List[str]
    cases: Dict[str, CaseEntry]
    order: List[str]                     # case ids in file order
    types: Dict[str, TypeInfo]
    types_path: Optional[Path]
    types_sha256: Optional[str]
    problems: List[str]

    def type_rank(self, t: str) -> Tuple[int, str]:
        info = self.types.get(t)
        return (info.rank if info else 10_000, t)

    def type_meaning(self, t: str) -> str:
        info = self.types.get(t)
        return info.meaning if info else "(type not in types.tsv; ask the maintainer what it means)"

    def queue_key(self, c: CaseEntry):
        """Paired first, then by type rank, then by priority (higher first), then case id."""
        return (0 if c.paired else 1, self.type_rank(c.type), -c.priority, c.case_id)


def load_types(root: Path) -> Tuple[Dict[str, TypeInfo], Optional[Path], Optional[str], List[str]]:
    problems: List[str] = []
    p = root / "types.tsv"
    if not p.exists():
        return ({n: TypeInfo(n, i, m) for i, (n, m) in enumerate(DEFAULT_TYPES)}, None, None, problems)
    out: Dict[str, TypeInfo] = {}
    with open(p, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f, delimiter="\t")
        cols = [c.strip() for c in (rd.fieldnames or [])]
        if "type" not in cols:
            problems.append(f"types.tsv has no 'type' column (has {cols})")
            return ({n: TypeInfo(n, i, m) for i, (n, m) in enumerate(DEFAULT_TYPES)}, p, sha256_file(p), problems)
        for i, row in enumerate(rd):
            name = (row.get("type") or "").strip()
            if not name:
                continue
            try:
                rank = int(str(row.get("rank") or i).strip())
            except ValueError:
                problems.append(f"types.tsv row {i}: rank {row.get('rank')!r} is not an int; using file order")
                rank = i
            out[name] = TypeInfo(name, rank, (row.get("meaning") or "").strip())
    return out, p, sha256_file(p), problems


def load_manifest(root: Path, hidden_prefixes) -> Manifest:
    root = Path(root).resolve()
    path = root / "manifest.tsv"
    problems: List[str] = []
    if not path.exists():
        raise FileNotFoundError(f"{path} not found: the review tree has no manifest.tsv")
    types, tpath, tsha, tprob = load_types(root)
    problems += tprob
    cases: Dict[str, CaseEntry] = {}
    order: List[str] = []
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="replace")
    rd = csv.DictReader(text.splitlines(), delimiter="\t")
    cols = [c.strip() for c in (rd.fieldnames or [])]
    for req in ("case_id", "type"):
        if req not in cols:
            raise ValueError(f"manifest.tsv lacks required column {req!r}; columns are {cols}")
    keyed = {"case_id", "type", "paired", "flags", "rules", "priority", "collection", "person_key", "case_dir"}
    for n, row in enumerate(rd, start=2):
        row = {(k or "").strip(): (v if v is not None else "") for k, v in row.items()}
        cid = row.get("case_id", "").strip()
        if not cid:
            problems.append(f"manifest.tsv line {n}: empty case_id; row skipped")
            continue
        if cid in cases:
            problems.append(f"manifest.tsv line {n}: duplicate case_id {cid!r}; later row skipped")
            continue
        if re.search(r"[\\/]|\.\.", cid):
            problems.append(f"manifest.tsv line {n}: case_id {cid!r} contains a path separator; row skipped")
            continue
        probs: List[str] = []
        t = row.get("type", "").strip() or "untyped"
        if t not in types:
            probs.append(f"type {t!r} not in types.tsv/DEFAULT_TYPES (queued last)")
        try:
            paired = parse_bool(row.get("paired", ""))
        except ValueError:
            probs.append(f"paired={row.get('paired')!r} not boolean; treated as unpaired")
            paired = False
        try:
            prio = int(str(row.get("priority") or "0").strip() or 0)
        except ValueError:
            probs.append(f"priority={row.get('priority')!r} not an int; 0")
            prio = 0
        cdir = row.get("case_dir", "").strip() or f"cases/{cid}"
        case_dir = (root / cdir).resolve()
        if not case_dir.exists():
            probs.append(f"case_dir missing: {cdir}")
        elif not (case_dir / "README.md").exists():
            probs.append("README.md missing")
        visible, hidden = {}, {}
        for k, v in row.items():
            if k in keyed or not k:
                continue
            (hidden if is_hidden_key(k, hidden_prefixes) else visible)[k] = v
        row_sha = sha256_bytes("\t".join(row.get(c, "") for c in cols).encode("utf-8"))
        cases[cid] = CaseEntry(case_id=cid, type=t, paired=paired, flags=split_list(row.get("flags")),
                               rules=split_list(row.get("rules")), priority=prio,
                               collection=row.get("collection", "").strip(),
                               person_key=row.get("person_key", "").strip(), case_dir=case_dir,
                               visible=visible, hidden=hidden, row_sha256=row_sha, problems=probs)
        order.append(cid)
        for pr in probs:
            problems.append(f"{cid}: {pr}")
    return Manifest(root=root, path=path, sha256=sha256_bytes(raw), columns=cols, cases=cases, order=order,
                    types=types, types_path=tpath, types_sha256=tsha, problems=problems)


# ── per-case directory contents ──────────────────────────────────────────────

VIEWER_FILE_GLOBS = {
    "ct": ("ct*.nii.gz", "ct*.nii", "*_ct.nii.gz", "*_cbct.nii.gz"),
    "masks": ("masks/*.nii.gz", "masks/*.nii"),
    "labels": ("labels/*.txt",),
    "scene_mrb": ("case.mrb", "*.mrb"),
    "scene_py": ("make_slicer_scene.py",),
    "projection_txt": ("xr_*_P.txt",),
    "transforms": ("*.tfm", "*.h5"),
    "radiographs": ("xr_*.png", "xr_*.dcm", "xr_*.nii.gz", "radiographs/*"),
}


def rel(root: Path, p: Path) -> str:
    try:
        return p.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def case_files(root: Path, c: CaseEntry) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    if not c.case_dir.exists():
        return out
    for key, globs in VIEWER_FILE_GLOBS.items():
        seen: List[str] = []
        for g in globs:
            for p in sorted(c.case_dir.glob(g)):
                if p.is_file():
                    r = rel(root, p)
                    if r not in seen:
                        seen.append(r)
        if seen:
            out[key] = seen
    return out


def case_previews(c: CaseEntry) -> List[Path]:
    d = c.case_dir / "previews"
    if not d.is_dir():
        return []
    return sorted(p for p in d.iterdir() if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg"))


def read_case_readme(c: CaseEntry) -> Tuple[Optional[str], Optional[str]]:
    p = c.case_dir / "README.md"
    if not p.exists():
        return None, None
    b = p.read_bytes()
    return b.decode("utf-8", errors="replace"), sha256_bytes(b)


def read_case_evidence(c: CaseEntry, hidden_prefixes) -> Tuple[Optional[object], Optional[str], Optional[str]]:
    """(visible evidence, sha256 of the file as read, error). The sha is of the whole file, hidden keys included,
    because the record has to identify the file, not the view of it."""
    p = c.case_dir / "evidence.json"
    if not p.exists():
        return None, None, None
    b = p.read_bytes()
    try:
        obj = json.loads(b.decode("utf-8-sig"))
    except Exception as exc:                                    # noqa: BLE001
        return None, sha256_bytes(b), f"evidence.json unreadable: {exc}"
    return strip_hidden(obj, hidden_prefixes), sha256_bytes(b), None


def open_commands(root: Path, c: CaseEntry, files: Dict[str, List[str]],
                  reviewer_tree_path: Optional[str]) -> Dict[str, str]:
    """Compose one command per viewer from what the case directory holds; open_commands.json overrides."""
    override = c.case_dir / "open_commands.json"
    cmds: Dict[str, str] = {}
    if override.exists():
        try:
            cmds = {str(k): str(v) for k, v in json.loads(override.read_text(encoding="utf-8-sig")).items()}
        except Exception as exc:                                # noqa: BLE001
            cmds = {"error": f"open_commands.json unreadable: {exc}"}
    base = reviewer_tree_path.rstrip("/\\") if reviewer_tree_path else root.as_posix()

    def ab(r: str) -> str:
        return f"{base}/{r}"

    if "slicer" not in cmds:
        if files.get("scene_mrb"):
            cmds["slicer"] = f'Slicer "{ab(files["scene_mrb"][0])}"'
        elif files.get("scene_py"):
            cmds["slicer"] = (f'Slicer, then View > Python Console:  exec(open(r"{ab(files["scene_py"][0])}").read())')
    if "itksnap" not in cmds and files.get("ct"):
        parts = [f'itksnap -g "{ab(files["ct"][0])}"']
        if files.get("masks"):
            parts.append(f'-s "{ab(files["masks"][0])}"')
        if files.get("labels"):
            parts.append(f'-l "{ab(files["labels"][0])}"')
        cmds["itksnap"] = " ".join(parts)
    if "imfusion" not in cmds and files.get("projection_txt"):
        cmds["imfusion"] = ("ImFusion Suite: File > Open the CT, then X-Ray & CT > Import projection matrix: "
                            + ", ".join(ab(p) for p in files["projection_txt"]))
    return cmds


def check_tree(m: Manifest) -> List[str]:
    """Validation report lines (empty = clean); lines prefixed "note:" do not fail --check."""
    lines = list(m.problems)
    for cid in m.order:
        c = m.cases[cid]
        readme, _ = read_case_readme(c)
        if readme and re.search(r"\bregistry\b", readme, flags=re.I):
            lines.append(f"{cid}: README.md mentions 'registry' -- the app cannot blind free text; rewrite it")
        _, _, err = read_case_evidence(c, ())
        if err:
            lines.append(f"{cid}: {err}")
        if c.case_dir.exists() and not case_previews(c) and not case_files(m.root, c):
            lines.append(f"note: {cid}: no previews and no viewer files; the reviewer will see text only")
    return lines
