#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/checkpoint_lineage.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""What every scored checkpoint -- and everything it was initialised from -- trained on and was SELECTED on.

WHY THIS EXISTS. On 2026-09-23 the recall-vs-angle curve (SchwingNet/results/arc/recall_vs_angle/) was scored on 17
TotalSegmentator subjects that were the VALIDATION subjects the scored checkpoints (dc_P_pooled, dc_A/dc_B) were
selected on -- YOLO keeps `best.pt` by val fitness -- and rx_lodo_carmlspine_1024, labelled "real-only", had been
initialised from anchor_none_v2_17-1882, whose train set holds five of those subjects and whose val set a sixth
(SchwingNet/results/arc/ARC_CHECK.md item 4). It was the fourth leak of this shape. Reading the code showed why the
contract (docs/DATA_ACCOUNTING.md) did not catch it:
  (1) the gate is opt-in: arc_recall_eval, realxray_eval, lcurve_score, case134_sweep, count_from_sacrum_eval and
      level_prototype make no gate call at all;
  (2) tools/holdout.py and CHK-1..8 treat only split == "train" as seen, so a checkpoint-selection subject passes as
      held out;
  (3) there is no lineage: the model registry recorded no parent and no train/val lists, and leak_check's
      DEFAULT_LINEAGE is a hand table ("a model nobody declared is checked by nothing").
This tool is (3). It is the input an evaluation gate needs to answer (1) and (2).

THE RULE IT SERVES. An evaluation item is HELD OUT for a checkpoint only if its PATIENT KEY (tools/patient_keys.py
key_any(); a render inherits its source CT subject) is in NEITHER the train NOR the val/selection set of that
checkpoint NOR of ANY ancestor in its initialisation chain (fine-tune -> parent -> grandparent ...). Pretraining on
public ImageNet/COCO weights is the only exempt ancestor, and only when declared (PUBLIC_ROOTS below).

IT READS CONFIGS; IT NEVER GUESSES. Per checkpoint family, the recorded source, in the order it is trusted:
  ultralytics   `train_args` stored INSIDE the checkpoint (data, model, pretrained, resume, project/name), checked
                against the run's args.yaml; the data yaml's `path`/`train`/`val` resolved exactly as Ultralytics
                resolves them (a directory is globbed recursively, a .txt is read line by line with ./ relative to
                the list). Parent = `model` when it is a .pt, else `pretrained` when it is a path. When an entry was
                rewritten after training began, the list is read from Ultralytics' OWN label cache
                (<labels dir>.cache) if that cache is dated no later than the run's start + SLACK_S and holds files
                of this run's entries only -- the list the run itself scanned; otherwise the entry is unresolved.
  level encoder (tools/train_level_classifier.py, `<bank>/runs/model_rung_<tag>.pt`) the registry row for its sha
                (bank, rung), else the launching script; train/val = the bank's rung npz `split` arrays, verified
                against the run's own result_rung_<tag>.json n_train/n_val. The trainer did not record --init until
                2026-09-23, so the parent is read from the slurm/*.sh line that writes this exact file (variables
                expanded, array indices bound by matching the file name); launchers that disagree are UNRESOLVED.
  recurrent head (tools/head_mixed_length.py) the `<stem>.arch.json` it wrote: base_model = parent, bank + rung =
                the films it trained (train) and scored (val) on.
  LSTV/TLTV flag (tools/lstv_flag_train.py --final) the `<stem>.flag.json` sidecar and the folds csv the same run
                wrote: the final model trains on every patient listed there.
  registry copy  ~/model_registry/<sha16>/<file>: the registry row gives the source path and bank; the file itself
                is read for anything it records.
Anything else -- a family with no reader, a file not on disk, a bank that was rebuilt or deleted after the model was
fitted, a membership list rewritten after training began, items no keying rule recognises -- is written to
`unresolved` with the reason. AN UNRESOLVED ANCESTOR IS NEVER TREATED AS EMPTY: its unresolved rows are carried into
every descendant, so a gate reading `touched_keys` sees that the set is a lower bound. A deleted bank's row also
carries the UPPER bound its build launch line gives (the --drr roots make_context_crops drew it from, keyed as they
stand today; bounds.json), marked incomplete when a root is gone or changed after the fit.

OUTPUT (<out>/touched.json): {checkpoint_path: {sha, parents:[...], train_keys:[...], val_keys:[...],
touched_keys:[union over the chain], unresolved:[{at, what, why}], ...}} for every checkpoint named by a result
AND every ancestor of one (an ancestor can be scored too). Extra fields are documented in SCHEMA below. Beside it:
touched_run.json (what ran, the seed list with who named each checkpoint, templates that could not be expanded,
names with no path, every unkeyed name family, the declared implant builds, the deleted-bank bounds), bounds.json
(the bound keys) and LINEAGE.md.

    python tools/checkpoint_lineage.py collect --repo . --out /tmp/seed.json            # anywhere; reads the repo
    python tools/checkpoint_lineage.py resolve --seed seed.json --out <dir> [--register] # on the grid, in a job
    python tools/checkpoint_lineage.py resolve --ckpt <path> --out <dir>                # one checkpoint
    python tools/checkpoint_lineage.py why --touched <dir>/touched.json --ckpt <path> --key ts:s0585

`resolve` opens every checkpoint (torch.load, for train_args) and hashes it: run it with the spinedet env (torch +
ultralytics) in an sbatch job, never on the login node.
"""
from __future__ import annotations

import argparse
import fnmatch
import glob
import hashlib
import json
import os
import platform
import re
import shlex
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import patient_keys as PK  # noqa: E402

GRID_HOME = "/wsu/home/go/go24/go2432"
CKPT_EXT = (".pt", ".pth", ".ckpt", ".safetensors")
IMG_EXT = (".bmp", ".dng", ".jpeg", ".jpg", ".mpo", ".png", ".tif", ".tiff", ".webp", ".pfm", ".heic")  # Ultralytics IMG_FORMATS
TEXT_EXT = (".json", ".md", ".csv", ".tsv", ".txt", ".yaml", ".yml", ".log", ".tex", ".sh", ".py")
SLACK_S = 120          # a membership file written within this many seconds after training began is the same launch

SCHEMA = {
    "sha": "sha256 of the checkpoint file as it is on disk now (null when absent)",
    "exists / bytes / mtime": "the file's state when this ran",
    "family": "ultralytics | level_encoder | recurrent_head | lstv_flag | unknown | missing",
    "role": "scored (named by a result or launch script) | ancestor | scored+ancestor",
    "named_by": "where the path was found: '<repo file>:<line>' (results, NUMBERS.md, slurm/*.sh)",
    "parents": "DIRECT parents this checkpoint was initialised from (paths); public roots are listed apart",
    "public_roots": "declared exempt ancestors (Ultralytics COCO release, torchvision ImageNet) -- nothing else is exempt",
    "ancestors": "every non-public ancestor, nearest first",
    "config_read": "the files this entry was read from",
    "train_sources / val_sources": "[{source, n_items}] -- the membership files or bank splits the run read",
    "train_keys / val_keys": "patient keys of THIS run's train and val/selection items (tools/patient_keys.key_any)",
    "train_pose_keys / val_pose_keys": "real-frame patients whose POSE a render was taken under (styled corpora); "
                                       "not the imaged patient, kept apart so a gate can decide",
    "touched_keys": "train_keys | val_keys over this checkpoint AND every ancestor -- what the rule forbids scoring on",
    "touched_pose_keys": "the same union over pose keys",
    "unresolved": "[{at, what, why}] over this checkpoint and every ancestor; non-empty means touched_keys is a LOWER bound. "
                  "A deleted-bank row also carries `bound`: the roots its build launch line drew it from, the corpora "
                  "and patient count those roots key to today, and `complete` (false when a root is gone, changed "
                  "after the fit, or unexpandable, or holds cases no rule keys); the keys themselves are in bounds.json. "
                  "A rewritten-list row carries `corpus`: the corpus the entry's location declares (null: no claim), "
                  "the only corpus whose patients its removed items can be",
    "unkeyed": "{split: {n, examples, shapes}} -- items no keying rule recognises, counted by name family (digits "
               "collapsed); never counted as patients, always an unresolved row",
    "notes": "what was assumed or corroborated (never a silent assumption)",
}

# The only exempt ancestors, and they are exempt only because they are DECLARED here. An Ultralytics release
# checkpoint carries train_args.data == 'coco.yaml' (or ImageNet for -cls); when the file is found it is checked.
PUBLIC_ROOT_RX = re.compile(r"^yolo(?:v3u?|v5[nsmlx]?u|v8|v9|v10|11|12)[nsmlxtcbe]?(?:-(?:pose|seg|obb|cls))?\.pt$")
PUBLIC_TORCHVISION = "public:torchvision/{arch}/IMAGENET1K_V1 (used when cached on the node; random init otherwise)"


def _carmlspine_split_of(case):
    """tools/carmlspine_labels.split_of, verbatim; checked at run time against every frame the export holds"""
    h = int(hashlib.md5(case.encode()).hexdigest(), 16) % 10
    return "train" if h <= 6 else ("val" if h == 7 else "test")


# Exports that send a PATIENT to a split by a pure function of its id. When such an export directory was rewritten
# after a run began, which frames it held then is unknown -- but not whose: every one belongs to a patient the
# function sends to that split, drawn from the source release's case list. So the directory's patients are bounded
# by {case in the release : fn(case) == split}, a complete bound when the release's case list has not changed since
# the run began. Each declaration is verified when used: the release directory must be dated before the run, and
# every frame the export holds NOW must sit in the split the function names (a formula that drifted from the
# exporter fails that check and resolves nothing).
DETERMINISTIC_SPLITS = [
    dict(corpus="carmlspine",
         dir_rx=re.compile(r"^(?P<root>.*/realxray/carmlspine)/images/(?P<split>train|val|test)/?$"),
         # the release root the exporter reads (tools/carmlspine_labels.py ROOT); the environment variable exists only
         # so tools/test_checkpoint_lineage.py can point it at a fixture
         release=os.environ.get("CKPT_LINEAGE_CARMLSPINE_RELEASE",
                                "/rs/rs_grp_oschome/go2432/data/carmlspine/unpacked/C-ArmLSpine"), case_glob="case*",
         fn=_carmlspine_split_of,
         where="tools/carmlspine_labels.py: split_of = md5(case) % 10 (0-6 train, 7 val, 8-9 test), unchanged since the "
               "tool's first commit 9973196 (2026-09-21 18:11, before the export existed; git log -L "
               "'/^def split_of/,+3:tools/carmlspine_labels.py'); cases = glob(ROOT/case*) of the release (line 388)"),
]


# ================================================================================================ small utilities
def now_iso(t=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t if t is not None else time.time()))


def jload(p, cap=256 << 20):
    try:
        if os.path.getsize(p) > cap:
            return None
        with open(p, encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return None


def yload(p):
    import yaml
    with open(p, encoding="utf-8", errors="replace") as f:
        return yaml.safe_load(f)


def mtime(p):
    try:
        return os.path.getmtime(p)
    except OSError:
        return None


def git_head():
    try:
        return subprocess.check_output(["git", "-C", str(TOOLS.parent), "rev-parse", "--short", "HEAD"],
                                       stderr=subprocess.DEVNULL, timeout=10).decode().strip()
    except Exception:  # noqa: BLE001
        return ""


def expand_home(p, home):
    p = str(p)
    if p.startswith("~/") or p == "~":
        return home + p[1:]
    return p


class ShaCache:
    """sha256 per (path, size, mtime), persisted, so a re-run does not re-read every weight file."""

    def __init__(self, path):
        self.path = Path(path)
        self.d = jload(self.path) or {}

    def get(self, p):
        try:
            st = os.stat(p)
        except OSError:
            return None
        k = f"{os.path.realpath(p)}|{st.st_size}|{int(st.st_mtime)}"
        if k not in self.d:
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for b in iter(lambda: f.read(1 << 22), b""):
                    h.update(b)
            self.d[k] = h.hexdigest()
        return self.d[k]

    def save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            json.dump(self.d, open(self.path, "w"), indent=0)
        except OSError:
            pass


# ================================================================================================ shell reading
# Launch scripts are read, not run. Variables assigned in the script are expanded in order; `${X:-d}` takes the
# script's default (an `sbatch --export` override would not be visible, and the note says so); SLURM_* variables,
# loop variables and anything else unknown stay SYMBOLIC (\x00NAME\x00) so a path containing one becomes a template
# (collect) or a regex group bound by matching a real file name (launcher search). Two command substitutions are
# understood because the launchers use them to choose an init: `$(... resolve('NAME') ...)` (the model registry
# alias, read from the ledger AT THE CHECKPOINT'S TIME) and `$(ls PATTERN | head -1)`.
UNK, CMD = "\x00", "\x01"


def split_statements(line):
    out, cur, depth, q, i = [], [], 0, None, 0
    while i < len(line):
        c = line[i]
        if q:
            cur.append(c)
            if c == q:
                q = None
        elif c in "\"'":
            q = c
            cur.append(c)
        elif c == "(":
            depth += 1
            cur.append(c)
        elif c == ")":
            depth = max(0, depth - 1)
            cur.append(c)
        elif depth == 0 and (c == ";" or line.startswith("&&", i) or line.startswith("||", i)):
            out.append("".join(cur))
            cur = []
            if c != ";":
                i += 1
        else:
            cur.append(c)
        i += 1
    out.append("".join(cur))
    return out


def logical_lines(path):
    """(first line number, text) with backslash continuations joined and comments dropped."""
    try:
        raw = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return []
    out, buf, start = [], "", None
    for n, l in enumerate(raw, 1):
        s = _strip_comment(l)
        if start is None:
            start = n
        if s.rstrip().endswith("\\"):
            buf += s.rstrip()[:-1] + " "
            continue
        buf += s
        if buf.strip():
            out.append((start, buf))
        buf, start = "", None
    if buf.strip():
        out.append((start, buf))
    return out


def _strip_comment(l):
    q = None
    for i, c in enumerate(l):
        if q:
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "#" and (i == 0 or l[i - 1] in " \t;") and not l[max(0, i - 2):i].endswith("${"):
            return l[:i]
    return l


def _matching(s, i, open_c="(", close_c=")"):
    depth = 0
    for j in range(i, len(s)):
        if s[j] == open_c:
            depth += 1
        elif s[j] == close_c:
            depth -= 1
            if depth == 0:
                return j
    return len(s) - 1


class ShellEnv:
    def __init__(self, home):
        self.v = {"HOME": home, "H": home, "USER": "go2432"}
        self.defaults_used = []
        self.in_case = False

    def expand(self, s, depth=0):
        if depth > 8:
            return f"{UNK}deep{UNK}"
        out, i = [], 0
        while i < len(s):
            c = s[i]
            if c == "$" and s.startswith("$((", i):
                j = _matching(s, i + 1)
                out.append(f"{UNK}arith{UNK}")
                i = j + 1
                continue
            if c == "$" and s.startswith("$(", i):
                j = _matching(s, i + 1)
                out.append(self._cmd(s[i + 2:j], depth))
                i = j + 1
                continue
            if c == "$" and s.startswith("${", i):
                j = _matching(s, i + 1, "{", "}")
                out.append(self._param(s[i + 2:j], depth))
                i = j + 1
                continue
            if c == "$":
                m = re.match(r"[A-Za-z_]\w*|\d|[@*#?]", s[i + 1:])
                if m:
                    out.append(self._get(m.group(0)))
                    i += 1 + len(m.group(0))
                    continue
            out.append(c)
            i += 1
        return "".join(out)

    def _get(self, name):
        if name in self.v:
            return self.v[name]
        return f"{UNK}{_mark(name)}{UNK}"

    def _param(self, body, depth):
        m = re.match(r"([A-Za-z_]\w*)(?::?[-=](.*))?$", body, re.S)
        if not m:
            return f"{UNK}{_mark(body)}{UNK}"
        name, dflt = m.group(1), m.group(2)
        if name in self.v:
            return self.v[name]
        if dflt is not None and not name.startswith("SLURM_"):
            self.defaults_used.append(name)
            return self.expand(dflt, depth + 1)
        return f"{UNK}{name}{UNK}"

    def _cmd(self, body, depth):
        m = re.search(r"resolve\(\s*['\"]([^'\"]+)['\"]", body)
        if m:
            return f"{CMD}REG:{m.group(1)}{CMD}"
        m = re.match(r"\s*ls\s+(.+?)\s*(?:2>\s*/dev/null\s*)?\|\s*head\s+-(?:n\s*)?1\s*$", body)
        if m:
            pat = self.expand(m.group(1), depth + 1).replace('"', "").replace("'", "")
            return f"{CMD}GLOB1:{pat}{CMD}"
        return f"{UNK}cmd{UNK}"

    def feed(self, line):
        # an assignment inside `case ... esac` depends on which arm ran (lstv_flag_train_v2.sh sets EXP per array
        # index): the variable is made UNKNOWN, so a path using it becomes a pattern bound by the real file name,
        # instead of silently taking whichever arm was written last
        if re.search(r"(^|\s)case\s.+\sin(\s|$)", line):
            self.in_case = True
        for st in split_statements(line):
            # `local name=$1 src=$2 tgt=$3` (a function binding its arguments): every NAME=VALUE word is an assignment
            md = re.match(r"\s*(?:local|export|readonly|declare(?:\s+-\w+)*)\s+(.*)$", st, re.S)
            if md and not self.in_case:
                try:
                    words = shlex.split(md.group(1), posix=True)
                except ValueError:
                    words = []
                if len([w for w in words if re.match(r"[A-Za-z_]\w*=", w)]) > 1:
                    for w in words:
                        mw = re.match(r"([A-Za-z_]\w*)=(.*)$", w, re.S)
                        if mw:
                            self.v[mw.group(1)] = self.expand(mw.group(2))
                    continue
            m = re.match(r"\s*(?:[^\s()]+\)\s*)?(?:(?:then|do|else|export|local|readonly)\s+)*([A-Za-z_]\w*)=(.*)$",
                         st, re.S)
            if not m:
                continue
            name, val = m.group(1), m.group(2).strip()
            if self.in_case:
                self.v.pop(name, None)
                continue
            if len(val) >= 2 and val[0] == val[-1] == "'":
                self.v[name] = val[1:-1]
            else:
                if len(val) >= 2 and val[0] == val[-1] == '"':
                    val = val[1:-1]
                self.v[name] = self.expand(val)
        if re.search(r"(^|[\s;])esac(\s|;|$)", line):
            self.in_case = False


def _mark(name):
    """a marker name is word characters only, so a path tokenizer never splits one in half"""
    return re.sub(r"\W", "_", str(name)) or "x"


def is_template(s):
    return UNK in s or CMD in s


def show_template(s):
    s = re.sub(UNK + r"([^" + UNK + r"]*)" + UNK, r"{\1}", s)
    return re.sub(CMD + r"([^" + CMD + r"]*)" + CMD, r"{\1}", s)


# ================================================================================================ collect
LIT_RX = re.compile(r"(?P<p>(?:/wsu/home/go/go24/go2432|/rs/rs_grp_oschome/go2432|~)/[^\s\"'<>|,;()\[\]{}`*?=]*?"
                    r"\.(?:pt|pth|ckpt|safetensors))(?![\w.])")
TOKEN_RX = re.compile(r"(?P<p>[^\s\"'<>|,;:()\[\]{}`=]+?\.(?:pt|pth|ckpt|safetensors))(?![\w.])")


def iter_text_files(root, cap=64 << 20, exclude=()):
    root = Path(root)
    if root.is_file():
        yield root
        return
    ex = [os.path.normcase(os.path.abspath(e)) for e in exclude]
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not any(os.path.normcase(os.path.abspath(os.path.join(dp, d))).startswith(e)
                                          for e in ex)]
        for f in sorted(fn):
            p = Path(dp) / f
            if p.suffix.lower() in TEXT_EXT:
                try:
                    if p.stat().st_size <= cap:
                        yield p
                except OSError:
                    pass


def collect(a):
    repo = Path(a.repo).resolve()
    home = a.home
    seeds = defaultdict(lambda: {"named_by": [], "kind": set()})
    templates, relative = [], defaultdict(list)

    def rel(p):
        try:
            return str(Path(p).resolve().relative_to(repo)).replace("\\", "/")
        except ValueError:
            return str(p)

    def add(path, where, kind):
        path = os.path.normpath(expand_home(path, home)).replace("\\", "/")
        seeds[path]["named_by"].append(where)
        seeds[path]["kind"].add(kind)

    result_roots = [repo / r for r in a.results]
    exclude = [repo / e for e in a.exclude]
    for root in result_roots:
        for f in iter_text_files(root, exclude=exclude):
            try:
                lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                continue
            for n, line in enumerate(lines, 1):
                for m in LIT_RX.finditer(line):
                    add(m.group("p"), f"{rel(f)}:{n}", "result")
                for m in TOKEN_RX.finditer(line):
                    tok = m.group("p")
                    if tok.startswith(("/", "~", "$")):
                        continue            # an absolute path: LIT_RX took it (or it is a template in prose)
                    relative[tok].append(f"{rel(f)}:{n}")
    for sd in a.slurm:
        for sh in sorted((repo / sd).rglob("*.sh")):
            env = ShellEnv(home)
            for n, line in logical_lines(sh):
                env.feed(line)
                exp = env.expand(line)
                for m in TOKEN_RX.finditer(exp):
                    tok = m.group("p")
                    where = f"{rel(sh)}:{n}"
                    tok = re.sub(r"^(?:~|\$\{?HOME\}?|\$\{?H\}?)(?=/)", home, tok)   # quoted or heredoc text
                    if any(ch in tok for ch in "*?") and not is_template(tok):
                        # a shell glob (`ls model_rung_1*.pt | head -1`): expanded against the disk at resolve
                        templates.append({"template": tok, "shown": tok, "where": where})
                        continue
                    if is_template(tok):
                        if tok.startswith(("/", UNK, CMD)):
                            templates.append({"template": tok, "shown": show_template(tok), "where": where})
                        else:
                            relative[show_template(tok)].append(where)
                        continue
                    if tok.startswith("/"):
                        add(tok, where, "slurm")
                    else:
                        relative[tok].append(where)
    out = {"built": now_iso(), "repo": str(repo), "home": home, "git": git_head(),
           "results_roots": [str(r) for r in result_roots], "slurm_dirs": a.slurm,
           "seeds": {k: {"named_by": sorted(set(v["named_by"])), "kind": sorted(v["kind"])}
                     for k, v in sorted(seeds.items())},
           "templates": templates,
           "relative_names": {k: sorted(set(v))[:20] for k, v in sorted(relative.items())},
           "relative_counts": {k: len(v) for k, v in sorted(relative.items())}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    n_res = sum(1 for v in out["seeds"].values() if "result" in v["kind"])
    print(f"collect: {len(out['seeds'])} checkpoint paths ({n_res} named by a result, "
          f"{len(out['seeds']) - n_res} only by a launch script); {len(templates)} templates; "
          f"{len(relative)} names with no directory -> {a.out}")
    return 0


# ================================================================================================ keying
class KeyCtx:
    """Keys items with tools/patient_keys.key_any, reading the ann a bank case came from when one exists."""

    def __init__(self, a, launchers=()):
        self.home = a.home
        self.cross = PK.d813_crosswalk(expand_home(a.d813, a.home))
        self.vmap = PK.verse_subjects(expand_home(a.verse_manifest, a.home)) if a.verse_manifest else {}
        self.ann_roots = sorted(set(glob.glob(os.path.join(a.home, "*", "ann"))
                                    + glob.glob(os.path.join(a.data, "*", "ann"))))
        self._index = None
        self.case_cache = {}
        # implant renders are keyed to their SOURCE CT through make_implant_ct's hardware records; the builds the
        # launch scripts declare (--scheme, --dst) are read too, so a build whose records were deleted (~/implant_ct)
        # still names the one scheme a render's case id can have come from (patient_keys.IMPLANT_CASE_FORMAT)
        builds = [L for L in launchers if L["tool"] == "make_implant_ct.py" and L["args"].get("--scheme")
                  and not is_template(L["args"].get("--scheme", ""))]
        dsts = {expand_home(L["args"].get("--dst", "~/implant_ct"), a.home) for L in builds}
        hw = sorted(set(glob.glob(os.path.join(a.home, "implant_*", "hardware")))
                    | {os.path.join(d, "hardware") for d in dsts if not is_template(d) and os.path.isdir(os.path.join(d, "hardware"))})
        self.implant = PK.implant_sources(hw)
        self.implant_builds = {L["args"]["--scheme"] for L in builds}
        self.implant_build_rows = [dict(scheme=L["args"]["--scheme"], dst=show_template(L["args"].get("--dst", "")),
                                        where=f"{L['script']}:{L['line']}",
                                        records_on_disk=os.path.isdir(os.path.join(
                                            expand_home(L["args"].get("--dst", ""), a.home), "hardware")))
                                   for L in builds]
        print(f"keys: crosswalk {len(self.cross)} Dataset813 stems; VerSe manifest {len(self.vmap)} series; "
              f"{len(self.ann_roots)} ann directories; {len(self.implant)} implant source records from {len(hw)} "
              f"hardware dirs; declared implant builds {sorted(self.implant_builds)}", flush=True)

    def index(self):
        if self._index is None:
            t = time.time()
            self._index = defaultdict(list)
            for i, d in enumerate(self.ann_roots):
                try:
                    with os.scandir(d) as it:
                        for e in it:
                            if e.name.endswith(".json"):
                                self._index[e.name[:-5]].append(i)
                except OSError:
                    continue
            print(f"keys: ann index {len(self._index)} names in {time.time() - t:.0f}s", flush=True)
        return self._index

    def key_case(self, case):
        """-> (set of keys, pose key or None, reason when unkeyed, conflict note or None)"""
        if case in self.case_cache:
            return self.case_cache[case]
        keys, poses, why, conflict = set(), set(), None, None
        anns = [os.path.join(self.ann_roots[i], case + ".json") for i in self.index().get(case, [])]
        tried = [jload(p) for p in anns] or [None]
        for ann in tried:
            r, w = PK.key_any(case, ann, self.cross, self.vmap, implant_map=self.implant,
                              implant_builds=self.implant_builds)
            if r:
                keys.add(r["key"])
                if r.get("pose_key"):
                    poses.add(r["pose_key"])
            else:
                why = w
        if len(keys) > 1:
            conflict = f"{case}: its anns key it {sorted(keys)} (every one is counted)"
        res = (keys, poses, None if keys else why, conflict)
        self.case_cache[case] = res
        return res

    def key_file(self, listed, real=None, _cache={}):
        stem = os.path.splitext(os.path.basename(listed))[0]
        hint = PK.corpus_hint_for_path(listed, real)
        ck = (stem, hint, os.path.basename(real) if real else None)
        if ck in _cache:
            return _cache[ck]
        r, why = PK.key_any(stem, None, self.cross, self.vmap, hint, self.implant, self.implant_builds)
        if not r and real and os.path.basename(real) != os.path.basename(listed):
            r, why = PK.key_any(os.path.splitext(os.path.basename(real))[0], None, self.cross, self.vmap, hint,
                                self.implant, self.implant_builds)
        _cache[ck] = (r, why)
        return r, why


class Items:
    """keys of one side (train or val) of one run, with what could not be keyed counted, never dropped."""

    def __init__(self):
        self.keys, self.poses, self.n, self.unkeyed, self.examples, self.conflicts = set(), set(), 0, 0, [], []
        self.sources = []
        self.shapes = defaultdict(int)       # every unkeyed item counted by name family, not just eight examples

    def miss(self, label, why):
        self.unkeyed += 1
        self.shapes[_shape(label)] += 1
        if len(self.examples) < 8:
            self.examples.append(f"{label}: {why}")

    def add(self, r, why, label):
        self.n += 1
        if r:
            self.keys.add(r["key"])
            if r.get("pose_key"):
                self.poses.add(r["pose_key"])
        else:
            self.miss(label, why)


# ================================================================================================ resolving
class Resolver:
    def __init__(self, a):
        self.a = a
        self.home = a.home
        self.nodes = {}
        self.launchers = self._read_launchers()
        self.keys = KeyCtx(a, self.launchers)
        self.bounds = {}                    # deleted bank -> what its build launcher says it could have held
        self.shas = ShaCache(Path(a.out) / "sha_cache.json")
        self.registry_dir = Path(expand_home(a.registry, a.home))
        self.registry = []
        led = self.registry_dir / "registry.jsonl"
        if led.exists():
            for l in open(led, encoding="utf-8", errors="replace"):
                try:
                    self.registry.append(json.loads(l))
                except Exception:  # noqa: BLE001
                    pass
        self.torch_ok = None

    # ------------------------------------------------------------------ launch scripts
    def _read_launchers(self):
        out = scan_launchers(self.a.slurm_dir, self.home, LAUNCH_TOOLS)
        print("launchers: " + ", ".join(f"{sum(1 for x in out if x['tool'] == t)} {t}" for t in LAUNCH_TOOLS)
              + " invocations in slurm/*.sh", flush=True)
        return out

    def _launcher_match(self, path, tool, expected):
        """launch lines of `tool` whose expected output file matches `path`; each with its variable bindings."""
        hits = []
        for L in self.launchers:
            if L["tool"] != tool:
                continue
            want = expected(L["args"])
            if want is None:
                continue
            rx = _template_regex(want)
            for cand in {path, os.path.realpath(path)}:
                m = rx.fullmatch(cand)
                if m:
                    hits.append((L, {k: v for k, v in m.groupdict().items() if v is not None}))
                    break
        return hits

    def _bind(self, s, bind, when):
        """substitute bound variables into a launcher value; resolve registry aliases and ls-globs."""
        notes, bad = [], []

        def unk(m):
            name = m.group(1)
            if _group(name) in bind:
                return bind[_group(name)]
            bad.append(name)
            return m.group(0)
        s = re.sub(UNK + r"([^" + UNK + r"]*)" + UNK, unk, s)

        def cmd(m):
            body = m.group(1)
            if body.startswith("REG:"):
                name = body[4:]
                rows = [r for r in self.registry if r.get("name") == name]
                before = [r for r in rows if when is None or r.get("ts", "") <= now_iso(when)]
                if before:
                    notes.append(f"registry alias {name!r} read from the ledger as it stood when this file was written "
                                 f"({before[-1].get('ts')}, sha {before[-1].get('sha', '')[:12]})")
                    return before[-1].get("store_path") or before[-1].get("source_path")
                bad.append(f"registry:{name} (no registration dated before {now_iso(when) if when else '?'})")
                return m.group(0)
            if body.startswith("GLOB1:"):
                got = sorted(glob.glob(body[6:]))
                if got:
                    mt = mtime(got[0])
                    notes.append(f"the script's `ls {body[6:]} | head -1` re-run now gives {got[0]}")
                    if when is not None and mt is not None and mt > when:
                        bad.append(f"ls-glob {body[6:]}: the file it finds now is newer than the checkpoint")
                    return got[0]
                bad.append(f"ls-glob {body[6:]} matches nothing now")
                return m.group(0)
            bad.append(body)
            return m.group(0)
        s = re.sub(CMD + r"([^" + CMD + r"]*)" + CMD, cmd, s)
        return s, notes, bad

    # ------------------------------------------------------------------ one node
    def node(self, path, role="scored", named_by=None):
        path = os.path.normpath(path).replace("\\", "/")
        if path in self.nodes:
            nd = self.nodes[path]
            if role not in nd["role"]:
                nd["role"] = "scored+ancestor"
            if named_by:
                nd["named_by"] = sorted(set(nd["named_by"]) | set(named_by))
            return nd
        nd = dict(path=path, realpath=os.path.realpath(path).replace("\\", "/"), exists=os.path.isfile(path),
                  sha=None, bytes=None, mtime=None, family="unknown", role=role, named_by=sorted(set(named_by or [])),
                  parents=[], parent_detail=[], public_roots=[], config_read=[], train_sources=[], val_sources=[],
                  n_train_items=0, n_val_items=0, train_keys=[], val_keys=[], train_pose_keys=[], val_pose_keys=[],
                  unkeyed={}, unresolved_own=[], notes=[])
        self.nodes[path] = nd
        print(f"resolve {path}", flush=True)
        if nd["exists"]:
            st = os.stat(path)
            nd["bytes"], nd["mtime"] = st.st_size, now_iso(st.st_mtime)
            nd["sha"] = self.shas.get(path)
        try:
            self._dispatch(nd)
        except Exception as e:  # noqa: BLE001  (one unreadable checkpoint must not hide the others)
            self._unres(nd, "the resolver raised", f"{type(e).__name__}: {e}")
        for p in list(nd["parents"]):
            self.node(p, role="ancestor")
        return nd

    def _unres(self, nd, what, why):
        nd["unresolved_own"].append({"at": nd["path"], "what": what, "why": why})

    def _reg_row(self, nd):
        rows = [r for r in self.registry if r.get("store_path") == nd["path"] or r.get("store_path") == nd["realpath"]]
        if not rows and nd["sha"]:
            rows = [r for r in self.registry if r.get("sha") == nd["sha"]]
        return rows[-1] if rows else None

    def _dispatch(self, nd):
        path = nd["path"]
        name = os.path.basename(path)
        reg = self._reg_row(nd)
        origin = path
        if reg and reg.get("source_path") and os.path.normpath(reg.get("store_path", "")) in (path, nd["realpath"]):
            origin = reg["source_path"]
            nd["notes"].append(f"registry copy of {origin} (registered {reg.get('ts')} as {reg.get('name')!r})")
            if os.path.isfile(origin) and nd["sha"] and self.shas.get(origin) != nd["sha"]:
                nd["notes"].append(f"{origin} now holds a DIFFERENT file than this store entry; sidecars read next "
                                   "to it may describe another model")
        if not nd["exists"]:
            nd["family"] = "missing"
            self._unres(nd, "checkpoint file", "not on disk; nothing it recorded can be read")
            if os.path.basename(os.path.dirname(path)) == "weights" and os.path.isfile(
                    os.path.join(os.path.dirname(os.path.dirname(path)), "args.yaml")):
                nd["notes"].append("its run directory survives; lineage read from args.yaml alone")
                self._ultralytics(nd, None)
            return
        stem = os.path.splitext(origin)[0]
        if os.path.isfile(stem + ".arch.json"):
            arch = jload(stem + ".arch.json") or {}
            if arch.get("kind") == "recurrent_head" or arch.get("base_model") or arch.get("bank"):
                return self._head(nd, stem + ".arch.json")
            # an ENCODER sidecar (tools/train_level_backbone.py: arch/loss/img_size only); its run record is
            # result_<name>.json beside model_<name>.pt
            b = os.path.basename(stem)
            res = os.path.join(os.path.dirname(stem), "result_" + (b[len("model_"):] if b.startswith("model_") else b)
                               + ".json")
            if os.path.isfile(res):
                return self._level_backbone(nd, stem + ".arch.json", res)
            nd["family"] = "unknown"
            self._unres(nd, "checkpoint family", f"{stem}.arch.json is an encoder sidecar that names no bank, and "
                                                 f"no {os.path.basename(res)} records the run")
            return
        if os.path.isfile(stem + ".flag.json"):
            return self._lstv_flag(nd, origin, stem + ".flag.json")
        if PUBLIC_ROOT_RX.match(name) and self._release_data(path)[0]:
            nd["family"] = "public_root"
            nd["public_roots"].append(f"public:ultralytics/{name} (the file itself; train_args.data = "
                                      f"{self._release_data(path)[1]!r})")
            return
        ck = self._torch_load(nd, path)
        if isinstance(ck, dict) and ("train_args" in ck or ("model" in ck and "ema" in ck)):
            return self._ultralytics(nd, ck)
        if os.path.basename(os.path.dirname(path)) == "weights" and os.path.isfile(
                os.path.join(os.path.dirname(os.path.dirname(path)), "args.yaml")):
            return self._ultralytics(nd, ck)
        if re.match(r"model_rung_.+\.pt$", os.path.basename(origin)) or (reg and reg.get("stage") == "level_model"):
            return self._level_encoder(nd, origin, reg)
        nd["family"] = "unknown"
        self._unres(nd, "checkpoint family", f"no reader for {name}: not an Ultralytics checkpoint, no .arch.json or "
                                             ".flag.json sidecar, not a registered level model; what it trained on "
                                             "is not recorded anywhere this tool knows")

    def _torch_load(self, nd, path):
        if self.torch_ok is False:
            return None
        try:
            import torch
            self.torch_ok = True
        except ImportError:
            self.torch_ok = False
            nd["notes"].append("torch is not importable here; checkpoints were not opened")
            return None
        try:
            try:
                return torch.load(path, map_location="cpu", weights_only=False)
            except TypeError:
                return torch.load(path, map_location="cpu")
        except Exception as e:  # noqa: BLE001
            nd["notes"].append(f"torch.load failed ({type(e).__name__}: {str(e)[:120]}); only sidecar files were read")
            return None

    # ------------------------------------------------------------------ ultralytics
    def _ultralytics(self, nd, ck):
        nd["family"] = "ultralytics"
        path = nd["path"]
        ta = dict(ck.get("train_args") or {}) if isinstance(ck, dict) else {}
        # Relative `project`, `model` and `data` are relative to the TRAINING PROCESS'S cwd, which Ultralytics does
        # not record. It is read off the disk instead: the cwd is the directory under which <project>/<name>/
        # args.yaml exists -- first the one the checkpoint itself sits in, then the directories runs start from.
        run_dir, cwd = None, None
        path_run = os.path.dirname(os.path.dirname(path)) if os.path.basename(os.path.dirname(path)) == "weights" else None
        if ta.get("project") and ta.get("name"):
            rel_run = os.path.join(str(ta["project"]), str(ta["name"]))
            if os.path.isabs(rel_run):
                run_dir = rel_run
            else:
                # Ultralytics puts a relative project either at <cwd>/<project>/<name> or nested under its runs_dir
                # as <cwd>/runs/<task>/<project>/<name> (detect_v5z: ~/spine-detector/runs/pose/runs/pose/runs/...)
                task = str(ta.get("task") or "detect")
                layouts = [rel_run, os.path.join("runs", task, rel_run)]
                cands = []
                pr = os.path.normpath(path_run).replace("\\", "/") if path_run else ""
                for lay in layouts:
                    lay_n = os.path.normpath(lay).replace("\\", "/")
                    if pr.endswith("/" + lay_n):
                        cands.append(pr[:-len(lay_n)].rstrip("/"))
                cands += [os.path.join(self.home, "spine-detector"), self.home, os.path.join(self.home, "spinesurg-ct-nnunet")]
                found, seen_c = [], set()
                for c in cands:
                    hit = next((os.path.join(c, lay) for lay in layouts
                                if c and os.path.isfile(os.path.join(c, lay, "args.yaml"))), None)
                    if hit and os.path.realpath(c) not in seen_c:
                        seen_c.add(os.path.realpath(c))
                        found.append((c, hit))
                # A run that sits in its own directory matches BOTH layouts (detect_v3 at
                # ~/spine-detector/runs/pose/runs/pose/runs/detect_v3: cwd ~/spine-detector/runs/pose with the flat
                # layout, ~/spine-detector with the nested one). The cwd is the one under which the run's own
                # relative data yaml and model exist; the flat reading sent data/yolo_v3/data.yaml to a directory
                # that never held it and reported detect_v3's lists unreadable.
                rel_needs = [(k, expand_home(str(ta.get(k)), self.home)) for k in ("data", "model")
                             if isinstance(ta.get(k), str) and ta.get(k)
                             and not os.path.isabs(expand_home(str(ta.get(k)), self.home))
                             and not PUBLIC_ROOT_RX.match(os.path.basename(str(ta.get(k))))
                             and (k == "data" or str(ta.get(k)).endswith(CKPT_EXT))]
                good = [f for f in found if all(os.path.exists(os.path.join(f[0], v)) for _, v in rel_needs)]
                if len(good) > 1:
                    tgt = {tuple(os.path.realpath(os.path.join(c, v)) for _, v in rel_needs) for c, _ in good}
                    if len(tgt) > 1:
                        self._unres(nd, "training cwd ambiguous",
                                    f"{[c for c, _ in good]} each hold {rel_run}/args.yaml and each resolve "
                                    f"{[v for _, v in rel_needs]} -- to different files; the first is read")
                pick = (good or found or [None])[0]
                if pick:
                    cwd, run_dir = pick
                    nd["notes"].append(f"train_args.project is relative ({ta['project']}); the training cwd is read "
                                       f"as {cwd}, where {os.path.relpath(run_dir, cwd)}/args.yaml exists"
                                       + (f" and {', '.join(v for _, v in rel_needs)} resolve" if good and rel_needs else "")
                                       + (f" (of {len(found)} candidate cwds)" if len(found) > 1 else ""))
                    if rel_needs and not good:
                        nd["notes"].append(f"no candidate cwd resolves {[v for _, v in rel_needs]}; {cwd} was taken")
                if cwd is None:
                    self._unres(nd, "training cwd", f"train_args.project {ta['project']!r} is relative and no "
                                                    f"{rel_run}/args.yaml was found under {cands}")
                    run_dir = path_run
        elif path_run:
            run_dir = path_run
        ay, ay_path = None, os.path.join(run_dir, "args.yaml") if run_dir else None
        if ay_path and os.path.isfile(ay_path):
            try:
                ay = yload(ay_path) or {}
                nd["config_read"].append(ay_path)
            except Exception as e:  # noqa: BLE001
                nd["notes"].append(f"{ay_path} unreadable: {type(e).__name__}")
        if ta:
            nd["config_read"].insert(0, f"{path}#train_args")
        cfg = ta or ay
        if not cfg:
            self._unres(nd, "training configuration", "the checkpoint carries no train_args and no args.yaml was found")
            return
        if ta and ay:
            for k in ("data", "model", "pretrained", "fraction", "resume"):
                if str(ta.get(k)) != str(ay.get(k)) and not (k == "resume" and not ta.get(k) and not ay.get(k)):
                    self._unres(nd, f"train_args vs args.yaml: {k}",
                                f"the checkpoint says {ta.get(k)!r}, {ay_path} says {ay.get(k)!r} -- the run directory "
                                "was reused, so the yaml may describe a later run")
        start = mtime(ay_path) if ay_path and os.path.isfile(ay_path) else None
        own = mtime(path)
        if start is not None and own is not None and start > own + SLACK_S:
            self._unres(nd, "run directory reused after this checkpoint was written",
                        f"{ay_path} was written {now_iso(start)}, after this file ({now_iso(own)}): the run directory "
                        "belongs to a later training, so its lists may not be this checkpoint's")
        if start is None:
            nd["notes"].append("no args.yaml: the training start time is unknown, so membership files could not be "
                               "checked for being rewritten after training began")
        # ---- parents
        model, pre, resume = cfg.get("model"), cfg.get("pretrained"), cfg.get("resume")
        cands = []
        if isinstance(model, str) and model.endswith(CKPT_EXT):
            cands.append((model, "model (initialised from)"))
        elif isinstance(model, str) and model:
            if isinstance(pre, str) and pre.endswith(CKPT_EXT):
                cands.append((pre, "pretrained (weights loaded into the yaml architecture)"))
            else:
                nd["notes"].append(f"model {model!r} is an architecture yaml and pretrained={pre!r}: trained from "
                                   "random initialisation, no parent")
        if isinstance(pre, str) and pre.endswith(CKPT_EXT) and isinstance(model, str) and model.endswith(CKPT_EXT) \
                and pre != model:
            cands.append((pre, "pretrained (listed; Ultralytics loads `model` when it is a .pt)"))
        if isinstance(resume, str) and resume.endswith(CKPT_EXT) and os.path.realpath(resume) != nd["realpath"]:
            cands.append((resume, "resume"))
        for p, rel in cands:
            self._add_parent(nd, p, rel, run_dir, start, cwd=cwd)
        # ---- data
        data = cfg.get("data")
        if not data:
            self._unres(nd, "data yaml", "train_args/args.yaml name no data")
            return
        if isinstance(data, dict):
            dcfg, dpath = data, None
        else:
            dpath = expand_home(str(data), self.home)
            if not os.path.isabs(dpath):
                if cwd is None:
                    self._unres(nd, "data yaml", f"{data!r} is relative to the training cwd, which could not be read")
                    return
                dpath = os.path.join(cwd, dpath)
            if not os.path.isfile(dpath):
                self._unres(nd, "data yaml", f"{data} is not on disk; the train and val lists cannot be read")
                return
            try:
                dcfg = yload(dpath) or {}
            except Exception as e:  # noqa: BLE001
                self._unres(nd, "data yaml", f"{dpath} unreadable: {type(e).__name__}")
                return
            nd["config_read"].append(dpath)
            self._stale(nd, dpath, start, "data yaml")
        base = dcfg.get("path") or (os.path.dirname(dpath) if dpath else None)
        base = expand_home(str(base), self.home) if base else None
        if base and not os.path.isabs(base):
            self._unres(nd, "data yaml path", f"`path: {base}` is relative to Ultralytics' DATASETS_DIR, which this "
                                              "tool does not read")
            return
        frac = cfg.get("fraction", 1.0)
        if frac not in (None, 1, 1.0):
            nd["notes"].append(f"fraction={frac}: the run used a subset of train; every listed item is counted "
                               "(an upper bound)")
        for split in ("train", "val"):
            side = Items()
            ent = dcfg.get(split)
            ents = ent if isinstance(ent, list) else ([ent] if ent else [])
            if not ents:
                self._unres(nd, f"{split} split", f"the data yaml has no `{split}` entry")
            listing, stale = [], []
            for e in ents:
                p = expand_home(str(e), self.home)
                if not os.path.isabs(p):
                    p = os.path.join(base or "", p)
                files, kind = _ultra_files(p)
                if kind == "missing":
                    self._unres(nd, f"{split} source", f"{p} is not on disk")
                    continue
                listing.append((p, kind, files))
                why = self._stale_why(p, start)
                if why:
                    stale.append((p, kind, why))
            cached = None
            if stale:
                cached, cnote = self._label_cache(listing, start, split)
                if cached is None:
                    for p, kind, why in stale:
                        dkeys, dnote = self._deterministic_split(p, kind, start)
                        if dkeys is not None:
                            side.keys |= dkeys
                            side.sources.append({"source": p, "kind": "patient bound from a deterministic split",
                                                 "n_items": len(dkeys)})
                            nd["notes"].append(f"{split}: {dnote}")
                            continue
                        why = why + (f" ({dnote})" if dnote else "")
                        # the corpus the entry's LOCATION declares (tools/realxray_banks.json roots, raw corpus
                        # paths), or null: what was removed from a carmlspine directory can only be carmlspine
                        # patients, which is what lets a gate scoring another corpus decide; null means no such claim
                        nd["unresolved_own"].append({
                            "at": nd["path"], "what": f"{split} {kind} rewritten after training began",
                            "why": why + " " + cnote,
                            "corpus": PK.corpus_hint_for_path(p, os.path.realpath(p))})
                else:
                    nd["notes"].append(cnote)
                    nd["config_read"].append(cached[0])
            if cached is not None:
                cp, ims = cached
                side.sources.append({"source": cp, "kind": "Ultralytics label cache (the training-time list)",
                                     "n_items": len(ims), "entries": [p for p, _, _ in listing]})
                for f in ims:
                    real = os.path.realpath(f) if os.path.islink(f) else None
                    r, why = self.keys.key_file(f, real)
                    side.add(r, why, os.path.basename(f))
            else:
                for p, kind, files in listing:
                    side.sources.append({"source": p, "kind": kind, "n_items": len(files)})
                    for f in files:
                        real = os.path.realpath(f) if os.path.islink(f) else None
                        r, why = self.keys.key_file(f, real)
                        side.add(r, why, os.path.basename(f))
            self._store_side(nd, split, side)

    def _label_cache(self, listing, start, split):
        """((cache path, im_files), note) when Ultralytics' own label cache provably holds this run's `split` list,
        else (None, why not).

        Ultralytics writes <labels dir of the first image>.cache when it scans a split, and rewrites it whenever the
        file list's hash changes. So a cache dated before this run began + SLACK_S was either READ by this run (its
        hash matched: the lists were equal) or WRITTEN by it. Two runs launched together on different lists sharing
        a first directory both write the same path (rx_lodo_cobra_elekta and rx_lodo_deepfluoro, 25 s apart, both
        write carmlspine/labels/test.cache), so the cache is also required to hold files from THIS run's entries
        only, and from every non-empty one."""
        sl = lambda x: str(x).replace("\\", "/")  # noqa: E731  (os.walk joins with the host separator)
        listing = [(sl(p), kind, [sl(f) for f in fs]) for p, kind, fs in listing]
        files = [f for _, _, fs in listing for f in fs]
        cp = _ultra_cache_path(files)
        if not cp:
            return None, "(no Ultralytics label cache path: the images are not under an images/ directory)"
        if not os.path.isfile(cp):
            return None, f"(Ultralytics' label cache {cp} is not on disk)"
        ct = mtime(cp)
        if start is None:
            return None, f"(Ultralytics' label cache {cp} exists, but the run's start is unknown, so it cannot be dated)"
        if ct > start + SLACK_S:
            return None, (f"(Ultralytics' label cache {cp} was rewritten {now_iso(ct)}, after this run began, by a later "
                          "scan, so it cannot stand in for the training-time list)")
        ims, err = _read_label_cache(cp)
        if ims is None:
            return None, f"(Ultralytics' label cache {cp} {err})"
        dirs = []
        for i, (p, kind, fs) in enumerate(listing):
            if kind == "directory":
                dirs.append((i, {p.rstrip("/") + "/", sl(os.path.realpath(p)).rstrip("/") + "/"}))
        lists = [(i, set(fs) | {sl(os.path.realpath(f)) for f in fs}) for i, (p, kind, fs) in enumerate(listing)
                 if kind == "list file"]
        owners, outside = set(), []
        for f in ims:
            o = next((i for i, pre in dirs if any(f.startswith(x) for x in pre)), None)
            if o is None:
                o = next((i for i, s in lists if f in s), None)
            if o is None:
                outside.append(f)
            else:
                owners.add(o)
        if outside:
            return None, (f"(Ultralytics' label cache {cp} holds {len(outside)} files outside this run's {split} entries "
                          f"-- another run's list, e.g. {outside[0]} -- so it cannot stand in)")
        need = {i for i, (p, kind, fs) in enumerate(listing) if fs}
        if not need <= owners:
            miss = [listing[i][0] for i in sorted(need - owners)]
            return None, (f"(Ultralytics' label cache {cp} holds no file of {miss}: another run's list, so it cannot "
                          "stand in)")
        now = set(files) | {sl(os.path.realpath(f)) for f in files}
        ims_set = set(ims)
        gone = sum(1 for f in ims if f not in now and not os.path.exists(f))
        added = len({f for f in files if f not in ims_set and sl(os.path.realpath(f)) not in ims_set})
        return (cp, ims), (f"{split}: an entry was rewritten after training began, so the membership is read from "
                           f"Ultralytics' own label cache {cp}, written {now_iso(ct)} ({ct - start:+.0f} s from the "
                           f"start of training) with all {len(ims)} of its files under this run's {len(listing)} "
                           f"{split} entries: {added} files listed now were added later and are not counted; {gone} "
                           "cached files are gone from disk and ARE counted")

    def _deterministic_split(self, p, kind, start, _memo={}):
        """(patient keys, note) bounding a rewritten export directory through DETERMINISTIC_SPLITS, or (None, why not)
        -- ('' when no declaration covers the directory)."""
        sp = str(p).replace("\\", "/").rstrip("/")
        for dec in DETERMINISTIC_SPLITS:
            m = dec["dir_rx"].match(sp)
            if not m or kind != "directory":
                continue
            rel = dec["release"]
            if not os.path.isdir(rel):
                return None, f"its deterministic split cannot be used: the release {rel} is not on disk"
            rt = mtime(rel)
            if start is None or rt is None or rt > start:
                return None, (f"its deterministic split cannot be used: the release {rel} was modified {now_iso(rt)}, "
                              f"not before the run began ({now_iso(start) if start else 'unknown'}), so its case list "
                              "then is not its case list now")
            root, split = m.group("root"), m.group("split")
            ck = (root, dec["corpus"])
            if ck not in _memo:
                bad, n = [], 0
                for s in ("train", "val", "test"):
                    fs, k2 = _ultra_files(os.path.join(root, "images", s))
                    for f in fs:
                        r, _ = self.keys.key_file(f, None)
                        n += 1
                        if not r or not r["key"].startswith(dec["corpus"] + ":") or dec["fn"](r["key"].split(":", 1)[1]) != s:
                            bad.append(f"{s}/{os.path.basename(f)}")
                cases = sorted(os.path.basename(x) for x in glob.glob(os.path.join(rel, dec["case_glob"])))
                _memo[ck] = (bad, n, cases)
            bad, n, cases = _memo[ck]
            if bad:
                return None, (f"its deterministic split cannot be used: {len(bad)} of the {n} frames the export holds "
                              f"now do not sit where the declared function sends them (e.g. {bad[:3]}), so the "
                              "declaration does not describe this export")
            keys = {f"{dec['corpus']}:{c}" for c in cases if dec["fn"](c) == split}
            return keys, (f"{sp} was rewritten after training began; its patients are bounded by the exporter's "
                          f"deterministic split ({dec['where']}): of the release's {len(cases)} cases (release "
                          f"directory unchanged since {now_iso(rt)}, before the run), the {len(keys)} it sends to "
                          f"`{split}` are counted, whatever frames of theirs the directory held then; all {n} frames "
                          "the export holds now sit where the function sends them")
        return None, ""

    def _stale_why(self, p, start):
        mt = mtime(p)
        if start is not None and mt is not None and mt > start + SLACK_S:
            return (f"{p} modified {now_iso(mt)}, training began {now_iso(start)}: the set read now may not be "
                    "the set this checkpoint saw (items removed since are not counted)")
        return None

    def _stale(self, nd, p, start, what):
        why = self._stale_why(p, start)
        if why:
            self._unres(nd, f"{what} rewritten after training began", why)

    def _add_parent(self, nd, p, rel, run_dir=None, start=None, basis="recorded", cwd=None):
        p = expand_home(str(p), self.home)
        base = os.path.basename(p)
        if not PUBLIC_ROOT_RX.match(base) and not os.path.isabs(p):
            if cwd is None:
                self._unres(nd, "initialisation", f"{rel}: {p!r} is relative to the training cwd, which could not be "
                                                  "read, so the parent cannot be located")
                return
            p = os.path.join(cwd, p)
        if PUBLIC_ROOT_RX.match(base) and (os.path.dirname(p) in ("", ".") or not os.path.isfile(p)
                                           or self._release_data(p)[0]):
            found = self._locate_release(p, run_dir)
            verdict = "file not located; declared by its Ultralytics release name"
            if found:
                ok, data = self._release_data(found)
                verdict = (f"verified at {found}: train_args.data = {data!r}" if ok else
                           f"NOT verified: {found} has train_args.data = {data!r}, not a COCO/ImageNet release config")
                if not ok:
                    self._unres(nd, "public root not verified", f"{p}: {verdict}. The name is declared exempt, the "
                                                                "file does not look like the release; not traced")
            nd["public_roots"].append(f"public:ultralytics/{base} (COCO release; {verdict})")
            return
        if not os.path.isabs(p):
            if cwd is None:
                self._unres(nd, "initialisation", f"{rel}: {p!r} is relative to an unrecorded cwd")
                return
            p = os.path.join(cwd, p)
        p = os.path.normpath(p).replace("\\", "/")
        nd["parent_detail"].append({"path": p, "relation": rel, "basis": basis, "public": False})
        if p not in nd["parents"]:
            nd["parents"].append(p)
        pm = mtime(p)
        if start is not None and pm is not None and pm > start + SLACK_S:
            self._unres(nd, "parent rewritten after this run was initialised from it",
                        f"{p} modified {now_iso(pm)}, after this run began {now_iso(start)}: the parent's lineage read "
                        "now may describe different weights than the ones loaded")

    def _locate_release(self, p, run_dir):
        base = os.path.basename(p)
        for c in ([p] if os.path.isabs(p) else []) + [os.path.join(self.home, "spine-detector", base),
                                                       os.path.join(self.home, base),
                                                       os.path.join(self.home, "spinesurg-ct-nnunet", base)] + \
                ([os.path.join(run_dir, base)] if run_dir else []):
            if os.path.isfile(c):
                return c
        return None

    def _release_data(self, p, _cache={}):
        """(is a COCO/ImageNet release checkpoint, its train_args.data) -- read from the file, cached per path."""
        if not p or not os.path.isfile(p):
            return False, None
        if p not in _cache:
            ck = self._torch_load({"notes": []}, p)
            ta = ck.get("train_args") if isinstance(ck, dict) else None
            d = str((ta or {}).get("data") or "")
            _cache[p] = (bool(re.search(r"(coco[\w.-]*\.yaml|imagenet\w*)$", d, re.I)), d or None)
        return _cache[p]

    def _store_side(self, nd, split, side):
        nd[f"{split}_sources"] += side.sources
        nd[f"n_{split}_items"] += side.n
        nd[f"{split}_keys"] = sorted(set(nd[f"{split}_keys"]) | side.keys)
        nd[f"{split}_pose_keys"] = sorted(set(nd[f"{split}_pose_keys"]) | side.poses)
        if side.unkeyed:
            u = nd["unkeyed"].setdefault(split, {"n": 0, "examples": [], "shapes": {}})
            u["n"] += side.unkeyed
            u["examples"] = (u["examples"] + side.examples)[:8]
            for s_, c_ in side.shapes.items():
                u["shapes"][s_] = u["shapes"].get(s_, 0) + c_
            self._unres(nd, f"{side.unkeyed} of {side.n} {split} items could not be keyed",
                        "no rule in tools/patient_keys.py or tools/leak_check.RULES matches them; they are NOT "
                        "treated as unique patients. Examples: " + "; ".join(side.examples[:4]))
        for c in side.conflicts[:4]:
            nd["notes"].append(c)

    # ------------------------------------------------------------------ banks
    def _bank_side(self, nd, bank, rung, splits=("train", "val"), fitted_at=None):
        rungs = [rung] if rung is not None else None
        root = Path(expand_home(str(bank), self.home))
        if not root.is_dir():
            b = self._bank_bound(str(root), fitted_at)
            why = (f"{root} is not on disk (deleted or never here); what this model trained on cannot be read. "
                   + b["summary"])
            nd["unresolved_own"].append({"at": nd["path"], "what": "training bank", "why": why,
                                         "bound": {k: v for k, v in b.items() if k != "summary"}})
            return None
        npzs = [root / f"rung_{r}.npz" for r in rungs] if rungs else sorted(root.glob("rung_*.npz"))
        if rungs is None:
            nd["notes"].append("the rung was not recorded: every rung of the bank is counted (an upper bound)")
        counts = {s: 0 for s in splits}
        for npz in npzs:
            if not npz.is_file():
                self._unres(nd, "training bank rung", f"{npz} is not on disk")
                continue
            nd["config_read"].append(str(npz))
            mt = mtime(npz)
            if fitted_at is not None and mt is not None and mt > fitted_at + SLACK_S:
                self._unres(nd, "bank rewritten after the model was fitted",
                            f"{npz} modified {now_iso(mt)}, after the checkpoint ({now_iso(fitted_at)}): its split "
                            "now may not be the split this model saw")
            z = _npz_strings(npz)
            if z is None or "case" not in z or "split" not in z:
                self._unres(nd, "training bank rung", f"{npz} carries no readable case/split arrays")
                continue
            for s in splits:
                side = Items()
                cases = sorted({c for c, sp in zip(z["case"], z["split"]) if sp == s})
                counts[s] += sum(1 for sp in z["split"] if sp == s)
                side.sources.append({"source": f"{npz}#{s}", "kind": "bank split", "n_items": len(cases)})
                for c in cases:
                    keys, poses, why, conflict = self.keys.key_case(c)
                    side.n += 1
                    if keys:
                        side.keys |= keys
                        side.poses |= poses
                    else:
                        side.miss(c, why)
                    if conflict:
                        side.conflicts.append(conflict)
                self._store_side(nd, s, side)
        return counts

    def _bank_bound(self, root, fitted_at):
        """What a DELETED bank could have held, read from the launch line that built it.

        tools/make_context_crops.py draws every case of a bank from its --drr roots and from nothing else, so the
        patients keyed from those roots' anns bound the bank's train AND val from above -- as the roots stand now.
        A root whose ann directory changed after the model was fitted may have lost cases since, and then the bound
        is not complete; that is recorded (`roots_changed_after_fit`), as is a build line whose roots cannot be
        expanded. The bound never clears the unresolved row: it is what a gate may use to decide whether an
        evaluation corpus can have been inside the deleted bank at all. Keys are written to bounds.json."""
        root = os.path.normpath(root).replace("\\", "/")
        if root not in self.bounds:
            builds, incomplete = [], []
            for L in self.launchers:
                if L["tool"] != "make_context_crops.py" or not L["args"].get("--dst"):
                    continue
                dst = L["args"]["--dst"]
                if is_template(dst):
                    m = _template_regex(dst).fullmatch(root)
                    if not m:
                        continue
                    bind = {k: v for k, v in m.groupdict().items() if v is not None}
                elif os.path.normpath(dst).replace("\\", "/") != root:
                    continue
                else:
                    bind = {}
                where = f"{L['script']}:{L['line']}" + (f" (called at line {L['called_at']})" if L.get("called_at") else "")
                roots = []
                for d in L["all"].get("--drr", []):
                    v, _, bad = self._bind(d, bind, fitted_at)
                    if bad or is_template(v):
                        incomplete.append(f"{where}: --drr {show_template(d)}")
                        continue
                    roots.append(os.path.normpath(v).replace("\\", "/"))
                builds.append({"where": where, "roots": roots})
            roots = sorted({r for b in builds for r in b["roots"]})
            keys, unk, shapes, missing, ann_mt = set(), 0, defaultdict(int), [], {}
            for r in roots:
                ad = os.path.join(r, "ann")
                if not os.path.isdir(ad):
                    missing.append(r)
                    continue
                ann_mt[r] = mtime(ad)
                with os.scandir(ad) as it:
                    names = [e.name[:-5] for e in it if e.name.endswith(".json")]
                for c in names:
                    ks, _, _, _ = self.keys.key_case(c)
                    if ks:
                        keys |= ks
                    else:
                        unk += 1
                        shapes[_shape(c)] += 1
            corpora = defaultdict(int)
            for k in keys:
                corpora[k.split(":")[0]] += 1
            self.bounds[root] = {"bank": root, "built_by": [b["where"] for b in builds], "roots": roots,
                                 "roots_missing": missing, "incomplete_launch_lines": incomplete,
                                 "root_ann_mtime": {r: now_iso(t) for r, t in ann_mt.items() if t},
                                 "n_keys": len(keys), "corpora": dict(sorted(corpora.items())), "n_unkeyed": unk,
                                 "unkeyed_shapes": dict(sorted(shapes.items(), key=lambda x: -x[1])[:10]),
                                 "keys": sorted(keys), "_mt": ann_mt}
            print(f"bound: {root} <- {len(builds)} build line(s), {len(roots)} roots, {len(keys)} keys", flush=True)
        B = self.bounds[root]
        changed = [r for r, t in B["_mt"].items() if fitted_at is not None and t is not None and t > fitted_at + SLACK_S]
        out = {k: v for k, v in B.items() if k not in ("keys", "_mt")}
        out["roots_changed_after_fit"] = changed
        out["keys_in"] = "bounds.json"
        out["complete"] = bool(B["built_by"]) and not B["roots_missing"] and not B["incomplete_launch_lines"] \
            and not changed and not B["n_unkeyed"]
        if not B["built_by"]:
            out["summary"] = ("No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds "
                              "what it held.")
        else:
            out["summary"] = (f"Its build line{'s' if len(B['built_by']) > 1 else ''} ({', '.join(B['built_by'])}) drew "
                              f"it from {len(B['roots'])} roots, which key today to {B['n_keys']} patients in "
                              f"{', '.join(f'{c} {n}' for c, n in B['corpora'].items()) or 'no corpus'}"
                              + (f"; {B['n_unkeyed']} of their cases no rule keys" if B["n_unkeyed"] else "")
                              + (f"; roots gone: {B['roots_missing']}" if B["roots_missing"] else "")
                              + (f"; roots changed after the fit (cases may have left them): {changed}" if changed else "")
                              + (f"; unexpandable roots: {B['incomplete_launch_lines']}" if B["incomplete_launch_lines"] else "")
                              + (". That upper bound is complete." if out["complete"] else
                                 ". That upper bound is NOT complete, for the reasons listed."))
        return out

    # ------------------------------------------------------------------ level encoder
    def _level_encoder(self, nd, origin, reg):
        nd["family"] = "level_encoder"
        fitted = mtime(nd["path"])
        fn = os.path.basename(origin)
        tag = fn[len("model_rung_"):-3] if fn.startswith("model_rung_") else None

        def expected(args):
            out = args.get("--out")
            if not out:
                return None
            t = args.get("--tag", "")
            aug = str(args.get("--augment", "1"))
            if aug == "2":
                t = f"{t}_aug2" if t else "aug2"
            elif aug == "3":
                t = f"{t}_aug3" if t else "aug3"
            ft = str(args.get("--rung", ""))
            arch = args.get("--arch", "resnet18")
            if arch != "resnet18":
                ft += f"_{arch}"
            if t:
                ft += f"_{t}"
            if str(args.get("--use-scale", "0")) not in ("0", ""):
                ft += "_scale"
            return f"{out.rstrip('/')}/model_rung_{ft}.pt"
        hits = self._launcher_match(origin, "train_level_classifier.py", expected)
        bank, rung, basis = None, None, None
        if reg and reg.get("bank"):
            bank, basis = reg["bank"], f"registry row {reg.get('name')!r} ({reg.get('ts')}) field bank"
            rung = str((reg.get("params") or {}).get("rung") or "") or None
            nd["config_read"].append(str(self.registry_dir / "registry.jsonl"))
        inits, launch_notes = [], []
        for L, bind in hits:
            data, n1, b1 = self._bind(L["args"].get("--data", ""), bind, fitted)
            init_raw = L["args"].get("--init")
            where = f"{L['script']}:{L['line']}"
            nd["config_read"].append(where)
            if L["defaults"]:
                launch_notes.append(f"{where}: the script's own defaults were assumed for {', '.join(L['defaults'])} "
                                    "(an sbatch --export override would not be visible)")
            if not bank and data and not b1:
                bank, basis = data, f"launcher {where} --data"
            if rung is None and L["args"].get("--rung") and not is_template(L["args"]["--rung"]):
                rung = L["args"]["--rung"]
            if init_raw:
                iv, n2, b2 = self._bind(init_raw, bind, fitted)
                launch_notes += n2
                if b2:
                    self._unres(nd, "initialisation", f"{where} passes --init {show_template(init_raw)} and "
                                                      f"{', '.join(map(show_template, b2))} could not be bound")
                else:
                    inits.append((iv, where))
            else:
                inits.append((None, where))
        nd["notes"] += launch_notes
        if bank is None and os.path.basename(os.path.dirname(origin)) == "runs":
            cand = os.path.dirname(os.path.dirname(origin))
            if os.path.isfile(os.path.join(cand, "meta.json")):
                bank, basis = cand, "directory convention (--out <bank>/runs); corroborated only by the counts below"
        if rung is None and tag:
            rung = tag.split("_")[0]
            nd["notes"].append(f"rung {rung!r} read from the file name")
        if bank is None:
            self._unres(nd, "training bank", "no registry row, no launcher and no enclosing bank directory names it")
        else:
            nd["notes"].append(f"bank {bank} from {basis}")
            counts = self._bank_side(nd, bank, rung, fitted_at=fitted)
            res = os.path.join(os.path.dirname(origin), f"result_rung_{tag}.json") if tag else None
            rj = jload(res) if res and os.path.isfile(res) else None
            if rj and counts is not None:
                nd["config_read"].append(res)
                if int(rj.get("n_train", -1)) == counts.get("train") and int(rj.get("n_val", -1)) == counts.get("val"):
                    nd["notes"].append(f"verified: the bank's rung {rung} holds {counts['train']} train / {counts['val']} "
                                       f"val crops, as {os.path.basename(res)} recorded at training time")
                else:
                    self._unres(nd, "bank split vs the run's own record",
                                f"{res} recorded n_train {rj.get('n_train')} / n_val {rj.get('n_val')}; the bank now "
                                f"holds {counts.get('train')} / {counts.get('val')} -- the bank was rebuilt since")
            elif counts is not None:
                nd["notes"].append("no result_rung json beside the checkpoint: the bank split could not be verified "
                                   "against what the run recorded")
            # from 2026-09-23 the trainer writes its own --init; a recorded value outranks every launch script
            if rj and "init" in rj:
                inits = [(rj.get("init"), res)]
                nd["notes"].append(f"init read from {os.path.basename(res)} (recorded by the run)")
        # ---- parents
        if not inits:
            self._unres(nd, "initialisation", "train_level_classifier.py did not record --init before 2026-09-23 and no "
                                              "slurm/*.sh line writes this exact file, so what it was initialised "
                                              "from is not recorded anywhere")
            return
        distinct = sorted({i for i, _ in inits}, key=lambda x: (x is None, str(x)))
        if len(distinct) > 1:
            self._unres(nd, "initialisation", "launch scripts that write this file disagree: " + "; ".join(
                f"{w} -> {i or 'no --init'}" for i, w in inits) + ". Every candidate is counted as a parent")
        for i in distinct:
            if i is None:
                arch = (reg or {}).get("params", {}).get("arch", "resnet18") if reg else "resnet18"
                nd["public_roots"].append(PUBLIC_TORCHVISION.format(arch=arch))
            else:
                self._add_parent(nd, i, "--init (fine-tuned from)", basis="launcher script (not recorded by the run)"
                                 if not any(w.endswith(".json") for _, w in inits) else "recorded")

    # ------------------------------------------------------------------ level backbone (train_level_backbone.py)
    def _level_backbone(self, nd, arch_path, res_path):
        nd["family"] = "level_encoder"
        nd["config_read"] += [arch_path, res_path]
        rec = jload(res_path) or {}
        fitted = mtime(nd["path"])
        mr = mtime(res_path)
        if mr and fitted and abs(mr - fitted) > 3600:
            self._unres(nd, "run record vs weights", f"{res_path} ({now_iso(mr)}) and the weights ({now_iso(fitted)}) "
                                                     "were not written by one run; the record may describe another")
        bank, rung = rec.get("bank"), rec.get("rung")
        if not bank:
            self._unres(nd, "training bank", f"{res_path} names no bank")
        else:
            nd["notes"].append(f"bank {bank}, rung {rung} from {os.path.basename(res_path)} (recorded by the run)")
            counts = self._bank_side(nd, bank, str(rung) if rung is not None else None, fitted_at=fitted)
            if counts is not None:
                if rec.get("n_train") == counts.get("train") and rec.get("n_val") == counts.get("val"):
                    nd["notes"].append(f"verified: {counts['train']} train / {counts['val']} val crops, as recorded")
                else:
                    self._unres(nd, "bank split vs the run's own record",
                                f"{os.path.basename(res_path)} recorded n_train {rec.get('n_train')} / n_val "
                                f"{rec.get('n_val')}; the bank now holds {counts.get('train')} / {counts.get('val')} "
                                "(a rebuilt bank, or a --fold file that moved cases to val and is not recorded)")
        if rec.get("init"):
            self._add_parent(nd, rec["init"], "--init (warm start, recorded by the run)")
        elif "init" in rec:
            nd["public_roots"].append(f"public:{rec.get('arch', '?')} release weights as train_level_backbone.py "
                                      f"builds them ({rec.get('marker_route', 'route not recorded')})")
        else:
            self._unres(nd, "initialisation", f"{res_path} does not record init")

    # ------------------------------------------------------------------ recurrent head
    def _head(self, nd, arch_path):
        nd["family"] = "recurrent_head"
        nd["config_read"].append(arch_path)
        arch = jload(arch_path) or {}
        base = arch.get("base_model") or arch.get("model") or arch.get("encoder")
        bank = arch.get("bank") or arch.get("ctx")
        rung = arch.get("rung")
        if base:
            self._add_parent(nd, base, "base_model (the encoder whose embeddings the head was fitted on)")
        else:
            self._unres(nd, "encoder", f"{arch_path} names no base_model")
        if bank:
            self._bank_side(nd, bank, str(rung) if rung is not None else None, fitted_at=mtime(nd["path"]))
            nd["notes"].append("a head fits on the bank's train films and scores its val films; both are counted")
        else:
            self._unres(nd, "training bank", f"{arch_path} names no bank")

    # ------------------------------------------------------------------ LSTV / TLTV flag
    def _lstv_flag(self, nd, origin, side_path):
        nd["family"] = "lstv_flag"
        nd["config_read"].append(side_path)
        side = jload(side_path) or {}
        name = os.path.splitext(os.path.basename(origin))[0]

        def expected(args):
            models = args.get("--models", f"{self.home}/lstv_flag/models")
            if "--final" not in args:
                return None
            exp = args.get("--export-name")
            if not exp:
                t = args.get("--target", "LSTV_flag")
                exp = f"{t.replace('_flag', '').lower()}_flag_v1"
            return f"{models.rstrip('/')}/{exp}.pt"
        hits = self._launcher_match(origin, "lstv_flag_train.py", expected)
        outs = set()
        for L, bind in hits:
            o, _, bad = self._bind(L["args"].get("--out", f"{self.home}/lstv_flag"), bind, mtime(nd["path"]))
            if not bad:
                outs.add(o)
            nd["config_read"].append(f"{L['script']}:{L['line']}")
        if not outs:
            outs = {os.path.dirname(os.path.dirname(origin))}
            nd["notes"].append("no launcher matched; the trainer's default layout (--out = parent of --models) assumed")
        if side.get("imagenet_weights_used"):
            nd["public_roots"].append(PUBLIC_TORCHVISION.format(arch=side.get("arch", "resnet18")))
        tgt = str(side.get("target") or "")
        folds = [os.path.join(o, f"folds_{t}.csv") for o in sorted(outs) for t in (f"{tgt}_flag", tgt)]
        folds = [f for f in folds if os.path.isfile(f)]
        if not folds:
            self._unres(nd, "training patients", f"no folds_{tgt}_flag.csv beside the run's --out {sorted(outs)}; "
                                                 "the final model trains on every patient listed there")
            return
        fcsv = folds[0]
        nd["config_read"].append(fcsv)
        mf, mm = mtime(fcsv), mtime(nd["path"])
        if mf and mm and mf > mm + SLACK_S:
            self._unres(nd, "folds csv rewritten after the model", f"{fcsv} is newer than {name}.pt")
        import csv
        cases = [r["case"] for r in csv.DictReader(open(fcsv, newline=""))]
        if side.get("n_patients") is not None and int(side["n_patients"]) != len(cases):
            self._unres(nd, "folds csv vs the model's sidecar", f"{fcsv} lists {len(cases)} patients; the sidecar "
                                                                f"says the model saw {side['n_patients']}")
        cohort = {}
        src = side.get("numbers_from")
        for oof in ([src] if src else []) + sorted(glob.glob(os.path.join(os.path.dirname(fcsv), "oof_*.csv"))):
            if oof and os.path.isfile(oof):
                for r in csv.DictReader(open(oof, newline="")):
                    if r.get("case") and r.get("cohort"):
                        cohort.setdefault(r["case"], r["cohort"])
                nd["config_read"].append(oof)
                if src and oof == src:
                    break
        tr = Items()
        tr.sources.append({"source": fcsv, "kind": "folds csv (the final model trains on every row)", "n_items": len(cases)})
        for c in cases:
            ann = {"scheme": "ctsp", "source_case": c} if cohort.get(c) == "ctsp" else None
            r, why = PK.key_any(c, ann, self.keys.cross, self.keys.vmap)
            tr.add(r, why if cohort.get(c) else f"{why} (no cohort recorded for this case)", c)
        self._store_side(nd, "train", tr)
        nd["notes"].append("the exported flag model trained on every patient of its folds csv; there is no "
                           "validation split for the final model (the cross-validated numbers are out-of-fold)")

    # ------------------------------------------------------------------ closure over the chain
    def closure(self):
        memo = {}

        def go(p, stack):
            if p in memo:
                return memo[p]
            nd = self.nodes[p]
            touched = set(nd["train_keys"]) | set(nd["val_keys"])
            poses = set(nd["train_pose_keys"]) | set(nd["val_pose_keys"])
            unres = list(nd["unresolved_own"])
            anc, pubs = [], list(nd["public_roots"])
            for par in nd["parents"]:
                if par in stack:
                    unres.append({"at": p, "what": "initialisation cycle", "why": f"{par} is its own ancestor"})
                    continue
                t, po, u, a2, pb = go(par, stack | {p})
                touched |= t
                poses |= po
                unres += [x for x in u if x not in unres]
                for x in [par] + a2:
                    if x not in anc:
                        anc.append(x)
                pubs += [x for x in pb if x not in pubs]
            memo[p] = (touched, poses, unres, anc, pubs)
            return memo[p]
        out = {}
        for p in sorted(self.nodes):
            nd = self.nodes[p]
            touched, poses, unres, anc, pubs = go(p, frozenset())
            e = {k: nd[k] for k in ("sha", "exists", "bytes", "mtime", "family", "role", "named_by", "parents",
                                    "parent_detail", "config_read", "train_sources", "val_sources",
                                    "n_train_items", "n_val_items", "train_keys", "val_keys",
                                    "train_pose_keys", "val_pose_keys", "unkeyed", "notes")}
            e["public_roots"] = pubs
            e["ancestors"] = anc
            e["touched_keys"] = sorted(touched)
            e["touched_pose_keys"] = sorted(poses)
            e["unresolved"] = unres
            out[p] = e
        return out


def _npz_strings(npz, keys=("case", "split", "source")):
    import numpy as np
    for pickle in (False, True):
        try:
            with np.load(npz, allow_pickle=pickle) as z:
                return {k: [str(v) for v in z[k]] for k in keys if k in z.files}
        except ValueError:
            continue
        except Exception:  # noqa: BLE001
            return None
    return None


def _ultra_files(p):
    """image files Ultralytics would read for one train/val entry: (files, kind)."""
    if os.path.isdir(p):
        out = []
        for dp, _dn, fn in os.walk(p, followlinks=True):
            out += [os.path.join(dp, f) for f in fn if os.path.splitext(f)[1].lower() in IMG_EXT]
        return sorted(out), "directory"
    if os.path.isfile(p):
        parent = os.path.dirname(p) + os.sep
        lines = [x.strip() for x in open(p, encoding="utf-8", errors="replace").read().splitlines() if x.strip()]
        lines = [parent + x[2:] if x.startswith("./") else x for x in lines]
        return [x for x in lines if os.path.splitext(x)[1].lower() in IMG_EXT], "list file"
    return [], "missing"


def _cli_pairs(line, tool):
    """[(--flag, value)] after `tool` on one expanded shell line, in order (stops at a pipe, a redirection or the
    end of the command); None when `tool` is not invoked on it."""
    try:
        toks = shlex.split(line, posix=True)
    except ValueError:
        toks = line.split()
    idx = next((i for i, t in enumerate(toks) if t.endswith(tool)), None)
    if idx is None:
        return None
    pairs, i = [], idx + 1
    while i < len(toks):
        t = toks[i]
        if t in ("|", "||", "&&", ";") or t.startswith((">", "2>", "|")):
            break
        end = t.endswith(";")               # `... --augment 2; next command`: shlex keeps the ; on the token
        if t.startswith("--"):
            t = t.rstrip(";")
            if "=" in t:
                k, v = t.split("=", 1)
                pairs.append((k, v))
            elif not end and i + 1 < len(toks) and not toks[i + 1].startswith("--") \
                    and toks[i + 1] not in ("|", "2>&1", "&&", "||", ";"):
                v = toks[i + 1]
                end = v.endswith(";")
                pairs.append((t, v.rstrip(";")))
                i += 1
            else:
                pairs.append((t, ""))
        if end:
            break
        i += 1
    return pairs


def _cli_args(line, tool):
    """--flag value pairs after `tool` on one expanded shell line (a repeated flag keeps its last value)."""
    pairs = _cli_pairs(line, tool)
    return None if pairs is None else dict(pairs)


def _cli_all(line, tool):
    """every value of every flag (`--drr A --drr B` -> {'--drr': ['A', 'B']})."""
    out = defaultdict(list)
    for k, v in _cli_pairs(line, tool) or []:
        out[k].append(v)
    return dict(out)


def _inner_command(line, tool):
    """The text that actually invokes `tool` on a launch line: the body of an `sbatch --wrap="..."` or of the
    innermost `$( ... )` holding it, else the whole line. Without this, a trainer launched as
    `J1=$(sbatch ... --wrap="... train_level_classifier.py --data $CTX --out $CTX/runs ...")` expands to one unknown
    command token and the invocation is never seen: allspine_v2's rung-1 model (slurm/allspine_v2_chain.sh:24) was
    reported as having no recorded initialisation for exactly this reason."""
    for m in re.finditer(r"--wrap=([\"'])(.*?)(?<!\\)\1", line, re.S):
        if tool in m.group(2):
            return m.group(2)
    i = line.find(tool)
    best, j = None, 0
    while i >= 0:
        s = line.find("$(", j)
        if s < 0 or s > i:
            break
        e = _matching(line, s + 1)
        if e > i:
            best = (s, e)
        j = s + 2
    return line[best[0] + 2:best[1]] if best else line


# the tools whose launch lines are read: two trainers (what a level model or LSTV flag was fitted on and from), the
# bank builder (what roots a bank was made from -- the only record left when the bank itself is deleted) and the
# implant builder (which source scheme an implant render's CT came from, when its hardware records are deleted)
LAUNCH_TOOLS = ("train_level_classifier.py", "lstv_flag_train.py", "make_context_crops.py", "make_implant_ct.py")


_FN_DEF = re.compile(r"^\s*(?:function\s+)?([A-Za-z_]\w*)\s*\(\)\s*\{(.*)$")


def _functions(lines):
    """{name: [(line number, text), ...body]} for `name () { ... }` definitions (body ends at a line that is `}`)."""
    funcs, i = {}, 0
    while i < len(lines):
        m = _FN_DEF.match(lines[i][1])
        if not m:
            i += 1
            continue
        rest = m.group(2).strip()
        if rest.endswith("}"):                          # one-liner: f() { cmd; }
            funcs[m.group(1)] = [(lines[i][0], rest[:-1])]
            i += 1
            continue
        body, j = ([(lines[i][0], rest)] if rest else []), i + 1
        while j < len(lines) and not re.match(r"^\s*\}\s*;?\s*$", lines[j][1]):
            body.append(lines[j])
            j += 1
        funcs[m.group(1)] = body
        i = j + 1
    return funcs


def _launch_rows(env, n, line, tools, sh, extra=None):
    rows = []
    for tool in tools:
        if tool not in line:
            continue
        exp = env.expand(_inner_command(line, tool))
        args = _cli_args(exp, tool)
        if args is None or "--eval-model" in args:
            continue
        rows.append(dict(tool=tool, script=str(sh), line=n, args=args, all=_cli_all(exp, tool),
                         defaults=sorted(set(env.defaults_used)), **(extra or {})))
    return rows


def scan_launchers(slurm_dirs, home, tools=LAUNCH_TOOLS):
    """every invocation of `tools` in slurm_dirs/**/*.sh: {tool, script, line, args (last value per flag), all (every
    value per flag), defaults (script defaults assumed), called_at (for a call through a shell function)}.
    Evaluations (--eval-model) are not launches.

    A tool invoked inside a shell FUNCTION is read once per call site, with that call's positional arguments bound
    (`crops "$H/mendeley_drr" mendeley_fov96_ctx ''` -> --dst ~/mendeley_fov96_ctx). Read as one line with $1, $2
    unknown, `--dst "$H/$DST"` is a template that matches every bank ever built, and would name corpus_expand.sh as
    a possible builder of allspine_v2. A function with no call site in its script is read as a template, as before."""
    out = []
    for sd in slurm_dirs or []:
        sd = expand_home(sd, home)
        for sh in sorted(Path(sd).rglob("*.sh")):
            lines = logical_lines(sh)
            funcs = _functions(lines)
            launching = {f: b for f, b in funcs.items() if any(t in l for _, l in b for t in tools)}
            in_func = {n for b in funcs.values() for n, _ in b}
            def_lines = {lines[i][0] for i in range(len(lines)) if _FN_DEF.match(lines[i][1])}
            called = set()
            env = ShellEnv(home)
            for n, line in lines:
                if n in in_func or n in def_lines:
                    continue
                env.defaults_used = []
                env.feed(line)
                out += _launch_rows(env, n, line, tools, sh)
                for fname, body in launching.items():
                    if not re.search(r"(?:^|[\s;(&|])" + re.escape(fname) + r"(?:\s|$|\))", line):
                        continue
                    inner = _inner_command(line, fname)
                    for st in split_statements(inner):
                        m = re.match(r"\s*" + re.escape(fname) + r"(?:\s+(.*))?$", st.strip().rstrip(")"), re.S)
                        if not m:
                            continue
                        try:
                            pos = shlex.split(env.expand(m.group(1) or ""), posix=True)
                        except ValueError:
                            continue
                        called.add(fname)
                        fenv = ShellEnv(home)
                        fenv.v = dict(env.v)
                        for k in range(1, 10):
                            fenv.v.pop(str(k), None)
                        for k, v in enumerate(pos, 1):
                            fenv.v[str(k)] = v
                        fenv.v["#"] = str(len(pos))
                        for bn, bl in body:
                            fenv.defaults_used = []
                            fenv.feed(bl)
                            out += _launch_rows(fenv, bn, bl, tools, sh, {"called_at": n})
            for fname, body in launching.items():
                if fname in called:
                    continue
                fenv = ShellEnv(home)
                fenv.v = dict(env.v)
                for bn, bl in body:
                    fenv.defaults_used = []
                    fenv.feed(bl)
                    out += _launch_rows(fenv, bn, bl, tools, sh, {"called_at": None})
    return out


def _shape(name):
    """a name with its ids collapsed, so unkeyed items are counted by FAMILY: a run of 11 or more id characters that
    is not a lowercase word (a video id, a hex id) becomes <id>, then every digit run becomes #
    (video_panels_med:<id>_#__right, vindr_pseudo__VINDRPS_<id>.png, LAT#PS_#.png)"""
    s = re.sub(r"[A-Za-z0-9-]{11,}", lambda m: m.group(0) if re.fullmatch(r"[a-z]+", m.group(0)) else "<id>",
               os.path.basename(str(name)))
    return re.sub(r"\d+", "#", s)[:64]


# ------------------------------------------------------------------ Ultralytics' own record of a split's file list
def _ultra_cache_path(files):
    """where Ultralytics keeps the label cache for a split: img2label_paths() of the FIRST image in sorted order
    across every entry (get_img_files sorts them), then Path(label).parent.with_suffix('.cache')."""
    if not files:
        return None
    first = sorted(str(f).replace("\\", "/") for f in files)[0]
    sa, sb = "/images/", "/labels/"
    if sa not in first:
        return None
    lab = sb.join(first.rsplit(sa, 1))
    return str(Path(lab).parent.with_suffix(".cache")).replace("\\", "/")


def _read_label_cache(p):
    """(im_files, None) from an Ultralytics label cache (a pickled dict saved with np.save), or (None, why)."""
    import numpy as np
    try:
        c = np.load(p, allow_pickle=True).item()
    except Exception as e:  # noqa: BLE001
        return None, f"unreadable ({type(e).__name__})"
    labs = c.get("labels") if isinstance(c, dict) else None
    if not isinstance(labs, list):
        return None, "carries no `labels` list"
    return [str(x["im_file"]).replace("\\", "/") for x in labs if isinstance(x, dict) and x.get("im_file")], None


def _group(name):
    return "v_" + re.sub(r"\W", "_", name)


def _template_regex(s):
    """a launcher's expected path -> regex; each symbolic variable becomes a named group (repeats must agree), so
    matching the real file name BINDS the variable (an array index, a loop variable) for the rest of the line."""
    parts, seen = [], set()
    s = re.sub(r"/{2,}", "/", s)
    for chunk in re.split("(" + UNK + r"[^" + UNK + r"]*" + UNK + "|" + CMD + r"[^" + CMD + r"]*" + CMD + ")", s):
        if not chunk:
            continue
        if chunk[0] == CMD:
            parts.append(r"[^/]*?")
        elif chunk[0] == UNK:
            g = _group(chunk.strip(UNK))
            if g in seen:
                parts.append(f"(?P={g})")
            else:
                seen.add(g)
                parts.append(f"(?P<{g}>[^/]*?)")
        else:
            parts.append(re.escape(chunk))
    return re.compile("".join(parts))


# ================================================================================================ resolve command
def expand_templates(seed, res, home, cap):
    """template paths from launch scripts -> real files: registry aliases and ls-globs are read, every other
    symbolic variable becomes one path component `*`. Too-broad and empty templates are returned, not dropped."""
    got, broad, empty = defaultdict(list), [], []
    for t in seed.get("templates", []):
        s = t["template"]
        s = re.sub(CMD + r"REG:([^" + CMD + r"]*)" + CMD,
                   lambda m: next((r.get("store_path") for r in reversed(res.registry) if r.get("name") == m.group(1)),
                                  "*"), s)
        s = re.sub(CMD + r"GLOB1:([^" + CMD + r"]*)" + CMD, lambda m: (sorted(glob.glob(m.group(1))) or ["*"])[0], s)
        g = re.sub(UNK + r"[^" + UNK + r"]*" + UNK, "*", s)
        g = re.sub(CMD + r"[^" + CMD + r"]*" + CMD, "*", g)
        hits = sorted(glob.glob(g))
        if not hits:
            empty.append({**t, "glob": g})
        elif len(hits) > cap:
            broad.append({**t, "glob": g, "n": len(hits)})
        else:
            for h in hits:
                got[os.path.normpath(h).replace("\\", "/")].append(f"{t['where']} (template {t['shown']})")
    return got, broad, empty


def cmd_resolve(a):
    out = Path(expand_home(a.out, a.home))
    out.mkdir(parents=True, exist_ok=True)
    a.out = str(out)
    res = Resolver(a)
    seed = {"seeds": {}, "templates": []}
    if a.seed:
        seed = json.load(open(a.seed))
    for c in a.ckpt or []:
        seed["seeds"].setdefault(os.path.normpath(expand_home(c, a.home)).replace("\\", "/"),
                                 {"named_by": ["--ckpt"], "kind": ["cli"]})
    tmpl_hits, broad, empty = expand_templates(seed, res, a.home, a.template_cap) if a.seed else ({}, [], [])
    todo = {k: v["named_by"] for k, v in seed["seeds"].items()}
    for k, v in tmpl_hits.items():
        todo.setdefault(k, [])
        todo[k] = todo[k] + v
    if a.only_results:
        todo = {k: v for k, v in todo.items() if any(not w.startswith("slurm/") for w in v)}
    t0 = time.time()
    for p in sorted(todo):
        res.node(p, role="scored", named_by=todo[p])
    touched = res.closure()
    res.shas.save()
    json.dump(touched, open(out / "touched.json", "w"), indent=1)
    json.dump({"built": now_iso(), "what": "for each DELETED bank some checkpoint's chain trained on: the roots its "
                                          "build launch line drew it from, and the patient keys those roots hold "
                                          "today (an upper bound on the bank; see `complete` on each unresolved row)",
               "banks": {b: {k: v for k, v in B.items() if k != "_mt"} for b, B in sorted(res.bounds.items())}},
              open(out / "bounds.json", "w"), indent=1)
    census = defaultdict(lambda: {"n_items": 0, "checkpoints": set()})
    for p, e in touched.items():
        for side, u in (e.get("unkeyed") or {}).items():
            for s_, c_ in (u.get("shapes") or {}).items():
                census[s_]["n_items"] += c_
                census[s_]["checkpoints"].add(p)
    census = {s_: {"n_items": v["n_items"], "n_checkpoints": len(v["checkpoints"]),
                   "example_checkpoint": sorted(v["checkpoints"])[0]}
              for s_, v in sorted(census.items(), key=lambda x: -x[1]["n_items"])}
    run = {"built": now_iso(), "host": platform.node(), "git": git_head(), "argv": sys.argv, "seconds": round(time.time() - t0),
           "home": a.home, "schema": SCHEMA, "rule": RULE_TEXT,
           "seed_file": a.seed, "seed_built": seed.get("built"), "seed_git": seed.get("git"),
           "n_checkpoints": len(touched), "n_scored": sum(1 for e in touched.values() if "scored" in e["role"]),
           "families": {f: sum(1 for e in touched.values() if e["family"] == f) for f in
                        sorted({e["family"] for e in touched.values()})},
           "n_with_unresolved": sum(1 for e in touched.values() if e["unresolved"]),
           "templates_too_broad": broad, "templates_matching_nothing": empty,
           "relative_names": seed.get("relative_names", {}), "relative_counts": seed.get("relative_counts", {}),
           "slurm_dirs": a.slurm_dir, "launchers_read": len(res.launchers),
           "launchers_by_tool": {t: sum(1 for x in res.launchers if x["tool"] == t) for t in LAUNCH_TOOLS},
           "implant_builds_declared": res.keys.implant_build_rows,
           "deleted_bank_bounds": {b: {k: v for k, v in B.items() if k not in ("keys", "_mt")}
                                   for b, B in sorted(res.bounds.items())},
           "unkeyed_census": census}
    json.dump(run, open(out / "touched_run.json", "w"), indent=1)
    if a.register:
        register_lineage(touched, out / "touched.json", res.registry_dir)
    write_md(touched, run, out / "LINEAGE.md", a)
    print(f"wrote {out / 'touched.json'} ({len(touched)} checkpoints, {run['n_with_unresolved']} with unresolved "
          f"lineage), bounds.json ({len(res.bounds)} deleted banks), {len(census)} unkeyed name families, and "
          f"{out / 'LINEAGE.md'}")
    return 0


RULE_TEXT = ("An evaluation item is HELD OUT for a checkpoint only if its patient key (tools/patient_keys.key_any; a "
             "render inherits its source CT subject) is in neither the train nor the val/selection set of that "
             "checkpoint nor of any ancestor in its initialisation chain. Public ImageNet/COCO pretraining is the only "
             "exempt ancestor, and only when declared. A non-empty `unresolved` makes touched_keys a lower bound.")


def register_lineage(touched, touched_path, registry_dir):
    """one lineage.jsonl row per checkpoint sha, through tools/model_registry.record_lineage; an identical row
    (same sha, same digest of parents + lists + touched keys) is not written twice."""
    os.environ["MODEL_REGISTRY"] = str(registry_dir)
    import importlib
    import model_registry as MR
    importlib.reload(MR)
    have = set()
    if MR.LINEAGE.exists():
        for l in open(MR.LINEAGE, encoding="utf-8"):
            try:
                r = json.loads(l)
                have.add((r.get("sha"), r.get("digest")))
            except Exception:  # noqa: BLE001
                pass
    n = 0
    for p, e in touched.items():
        if not e["sha"]:
            continue
        tl = [s["source"] for s in e["train_sources"]]
        vl = [s["source"] for s in e["val_sources"]]
        dig = hashlib.sha256(json.dumps([e["parents"], e["public_roots"], tl, vl, e["touched_keys"],
                                         len(e["unresolved"])], sort_keys=True).encode()).hexdigest()[:16]
        if (e["sha"], dig) in have:
            continue
        MR.record_lineage(e["sha"], p, parents=e["parents"] + e["public_roots"], train_list=tl, val_list=vl,
                          source="tools/checkpoint_lineage.py", digest=dig, family=e["family"],
                          touched_json=str(touched_path), n_touched_keys=len(e["touched_keys"]),
                          ancestors=e["ancestors"],
                          unresolved=[f"{u['at']}: {u['what']}" for u in e["unresolved"]][:40])
        n += 1
    print(f"registry: {n} lineage rows appended to {MR.LINEAGE}")


# ================================================================================================ report
def _short(p):
    p = p.replace(GRID_HOME + "/", "~/").replace("/rs/rs_grp_oschome/go2432/", "rs:/")
    p = re.sub(r"^~/spine-detector/runs/", "", p)
    return p.replace("/weights/best.pt", "")


def write_md(touched, run, path, a):
    L = ["# Checkpoint lineage: what every scored checkpoint, and everything it was initialised from, saw", "",
         f"Written by `tools/checkpoint_lineage.py` on {run['host']} at {run['built']} (git {run['git']}), "
         f"from `touched.json` in this directory. Nothing in this file is typed by hand.", "",
         "**The rule.** " + RULE_TEXT, "",
         f"**Census.** {run['n_checkpoints']} checkpoints: {run['n_scored']} named by a result or a launch script, the "
         f"rest reached only as ancestors. Families: "
         + ", ".join(f"{k} {v}" for k, v in run["families"].items()) + ". "
         f"**{run['n_with_unresolved']}** carry at least one unresolved link, so their touched set is a lower bound.", ""]
    res_named = {p: e for p, e in touched.items() if any(not w.startswith("slurm/") and w != "--ckpt" and
                                                          "(template" not in w for w in e["named_by"])}
    other = {p: e for p, e in touched.items() if p not in res_named}

    def table(rows, title):
        L.extend([f"## {title}", "",
                  "| checkpoint | family | initialised from (nearest first) | train keys | val keys | touched (chain) | unresolved |",
                  "|---|---|---|---:|---:|---:|---:|"])
        for p, e in sorted(rows.items()):
            chain = " <- ".join(_short(x) for x in e["ancestors"]) or "-"
            if e["public_roots"]:
                chain += " <- " + " / ".join(x.split(" (")[0] for x in e["public_roots"])
            L.append(f"| `{_short(p)}` | {e['family']} | {chain} | {len(e['train_keys'])} | {len(e['val_keys'])} | "
                     f"{len(e['touched_keys'])} | {len(e['unresolved'])} |")
        L.append("")
    table(res_named, f"Checkpoints named by a SchwingNet result or NUMBERS.md ({len(res_named)})")
    table(other, f"Checkpoints named only by a launch script, or reached as an ancestor ({len(other)})")

    # the external cross-check: the angle-sweep subjects against the weights the curve scored
    si = jload(expand_home(a.sweep_set, a.home)) if a.sweep_set else None
    rv = (jload(expand_home(a.arc_json, a.home)) if a.arc_json else None) or {}
    if si and si.get("subjects"):
        subj = [f"ts:{s}" for s in si["subjects"]]
        L.extend(["## Cross-check: the recall-vs-angle subjects against the weights that scored them", "",
                  f"The {len(subj)} subjects of `{a.sweep_set}` keyed `ts:<subject>`, located in each scored "
                  "checkpoint's own lists and in its ancestors'. SchwingNet/results/arc/ARC_CHECK.md item 4 found the "
                  "same thing by a regex over file names (P/A/B: all 17 are val subjects; rx_lodo_carmlspine_1024: five "
                  "in its parent's train, one in its parent's val); agreement is the check.", "",
                  "| arm | checkpoint | in own train | in own val | in an ancestor's train/val | held out under the rule |",
                  "|---|---|---:|---:|---:|---:|"])
        for arm, w in (rv.get("weights") or {}).items():
            e = touched.get(os.path.normpath(w).replace("\\", "/"))
            if not e:
                L.append(f"| {arm} | `{_short(w)}` | not resolved | | | |")
                continue
            own_t = [s for s in subj if s in set(e["train_keys"])]
            own_v = [s for s in subj if s in set(e["val_keys"])]
            anc = [s for s in subj if s in set(e["touched_keys"]) and s not in own_t and s not in own_v]
            held = [s for s in subj if s not in set(e["touched_keys"])]
            flag = " (lower bound: unresolved links)" if e["unresolved"] else ""
            L.append(f"| {arm} | `{_short(w)}` | {len(own_t)} | {len(own_v)} | {len(anc)} "
                     f"{('(' + ', '.join(x[3:] for x in anc) + ')') if anc else ''} | {len(held)}{flag} |")
        L.append("")

    L.extend(["## Unresolved links, per checkpoint", "",
              "Each row is a link the tool could not make from disk. It is carried into every descendant, so a gate "
              "that finds any of these on a checkpoint must treat its touched set as incomplete.", ""])
    for p, e in sorted(touched.items()):
        own = [u for u in e["unresolved"] if u["at"] == p]
        if own:
            L.append(f"- `{_short(p)}`")
            for u in own[:12]:
                L.append(f"    - **{u['what']}** -- {u['why'][:900 if u.get('bound') else 400]}")
            if len(own) > 12:
                L.append(f"    - ... {len(own) - 12} more in touched.json")
    L.append("")
    cen = run.get("unkeyed_census") or {}
    L.extend(["## Names no keying rule recognises, by family", "",
              "Every unkeyed train/val item across all checkpoints, its digits collapsed to `#`. None of these is "
              "counted as a patient; each is an unresolved row on the checkpoints that read it.", ""])
    if cen:
        L += ["| name family | items | checkpoints | e.g. |", "|---|---:|---:|---|"]
        for s_, v in list(cen.items())[:40]:
            L.append(f"| `{s_}` | {v['n_items']} | {v['n_checkpoints']} | `{_short(v['example_checkpoint'])}` |")
        if len(cen) > 40:
            L.append(f"| ... {len(cen) - 40} more families in touched_run.json | | | |")
    else:
        L.append("- none: every train and val item of every resolved checkpoint was keyed")
    L.append("")
    bd = run.get("deleted_bank_bounds") or {}
    if bd:
        L.extend(["## Deleted banks: what their build lines say they could have held", "",
                  "A bank a checkpoint trained on that is no longer on disk leaves its split unreadable. Its build "
                  "launch line (make_context_crops.py --drr ... --dst <bank>) still names the roots it drew from; the "
                  "patients those roots hold today bound the bank from above, unless a root changed after the fit. "
                  "The rows stay unresolved; bounds.json has the keys.", "",
                  "| bank | built by | roots | patients (corpora) | unkeyed | roots gone |", "|---|---|---|---|---:|---|"])
        for b, B in bd.items():
            L.append(f"| `{_short(b)}` | {', '.join(x.split('/slurm/')[-1] for x in B['built_by']) or '**none found**'} | "
                     f"{', '.join(_short(r) for r in B['roots'])} | {B['n_keys']} "
                     f"({', '.join(f'{c} {n}' for c, n in B['corpora'].items())}) | {B['n_unkeyed']} | "
                     f"{', '.join(_short(r) for r in B['roots_missing']) or '-'} |")
        L.append("")
    ib = run.get("implant_builds_declared") or []
    if ib:
        L.extend(["## Implant builds declared by launch scripts", "",
                  "An implant render is keyed to its source CT through make_implant_ct's hardware record; where a "
                  "build's records are gone, through the one declared build whose case-id format its name fits.", ""])
        for r_ in ib:
            L.append(f"- `{r_['scheme']}` -> `{_short(r_['dst'])}` ({r_['where'].split('/slurm/')[-1]}); hardware records "
                     f"{'on disk' if r_['records_on_disk'] else '**not on disk**'}")
        L.append("")
    L.extend(["## Declared public roots (the only exempt ancestors)", ""])
    pubs = sorted({x for e in touched.values() for x in e["public_roots"]})
    L += [f"- {x}" for x in pubs] or ["- none"]
    L.append("")
    L.extend(["## What the seed could not turn into a file", ""])
    if run["templates_too_broad"] or run["templates_matching_nothing"]:
        L.append("Launch-script paths with a variable the script does not set (an array index, a loop variable, "
                 "an argument):")
        for t in run["templates_too_broad"][:40]:
            L.append(f"- too broad ({t['n']} files): `{t['shown']}` at {t['where']}")
        for t in run["templates_matching_nothing"][:60]:
            L.append(f"- matches nothing on disk: `{t['shown']}` at {t['where']}")
    rel = run.get("relative_counts") or {}
    if rel:
        L.append("")
        L.append("Checkpoint names written without a directory (cannot be resolved to one file; public release names "
                 "are exempt roots, the rest are listed so nobody reads their absence as 'none'):")
        for k, n in sorted(rel.items(), key=lambda x: -x[1])[:40]:
            ex = (run.get("relative_names") or {}).get(k, [])[:2]
            L.append(f"- `{k}` x{n} (e.g. {', '.join(ex)})")
    L.append("")
    L.append("PolyPose `polypose.ckpt` files (SchwingNet/results/polypose/) are per-subject registration fits made "
             "from that subject's own frames: they are not population models and carry no held-out claim, so they "
             "are listed here and not traced.")
    L.append("")
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


# ================================================================================================ why
def cmd_why(a):
    t = json.load(open(a.touched))
    p = os.path.normpath(expand_home(a.ckpt, a.home)).replace("\\", "/")
    if p not in t:
        print(f"{p} is not in {a.touched}")
        return 2
    e = t[p]
    hit = False
    for q in [p] + e["ancestors"]:
        f = t.get(q, {})
        for side in ("train", "val"):
            if a.key in set(f.get(f"{side}_keys", [])):
                src = ", ".join(s["source"] for s in f.get(f"{side}_sources", []))
                print(f"{a.key} is in the {side} set of {q}{' (ancestor)' if q != p else ''}: {src}")
                hit = True
    if not hit:
        print(f"{a.key} is not in the touched set of {p}" +
              (f" -- but {len(e['unresolved'])} links are unresolved, so this is a lower bound" if e["unresolved"] else ""))
    return 0 if not hit else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect", help="find every checkpoint path the results, NUMBERS.md and slurm/*.sh name")
    c.add_argument("--repo", default=str(TOOLS.parent))
    c.add_argument("--results", action="append", default=None,
                   help="repo-relative roots whose text files name scored checkpoints (default SchwingNet/results, SchwingNet/NUMBERS.md)")
    c.add_argument("--slurm", action="append", default=None, help="repo-relative launch-script dirs (default slurm)")
    c.add_argument("--exclude", action="append", default=None,
                   help="repo-relative dirs that are gate OUTPUT, not results (default SchwingNet/results/eval_gate)")
    c.add_argument("--home", default=GRID_HOME, help="what $HOME and ~ mean in the paths (the grid's home)")
    c.add_argument("--out", required=True)
    r = sub.add_parser("resolve", help="read every checkpoint's lineage (run on the grid, in a job)")
    r.add_argument("--seed", default=None, help="collect's output")
    r.add_argument("--ckpt", action="append", default=None, help="a checkpoint path (repeatable), with or without --seed")
    r.add_argument("--out", required=True)
    r.add_argument("--home", default=os.path.expanduser("~"))
    r.add_argument("--data", default="/rs/rs_grp_oschome/go2432/data")
    r.add_argument("--registry", default="~/model_registry")
    r.add_argument("--slurm-dir", action="append", default=None, help="launch scripts read for level-model inits "
                                                                      "(default ~/spinesurg-ct-nnunet/slurm)")
    r.add_argument("--d813", default="~/spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs")
    r.add_argument("--verse-manifest", default="~/VerSeFusion/data/manifest/manifest.csv")
    r.add_argument("--sweep-set", default="/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep/SET_INFO.json",
                   help="the angle-sweep set whose subjects LINEAGE.md cross-checks ('' to skip)")
    r.add_argument("--arc-json", default=str(TOOLS.parent / "SchwingNet" / "results" / "arc" /
                                             "recall_vs_angle_selection_leaked" / "recall_vs_angle.json"),
                   help="recall_vs_angle.json, whose `weights` are the checkpoints the cross-check reads")
    r.add_argument("--template-cap", type=int, default=60)
    r.add_argument("--only-results", action="store_true", help="skip checkpoints named only by launch scripts")
    r.add_argument("--register", action="store_true", help="append each lineage to the model registry's lineage.jsonl")
    w = sub.add_parser("why", help="where in a checkpoint's chain a patient key entered (exit 1 when it did)")
    w.add_argument("--touched", required=True)
    w.add_argument("--ckpt", required=True)
    w.add_argument("--key", required=True)
    w.add_argument("--home", default=GRID_HOME)
    a = ap.parse_args()
    if a.cmd == "collect":
        a.results = a.results or ["SchwingNet/results", "SchwingNet/NUMBERS.md"]
        a.slurm = a.slurm or ["slurm"]
        a.exclude = a.exclude or ["SchwingNet/results/eval_gate"]
        return collect(a)
    if a.cmd == "resolve":
        a.slurm_dir = a.slurm_dir or [os.path.join(a.home, "spinesurg-ct-nnunet", "slurm")]
        if not a.seed and not a.ckpt:
            ap.error("resolve needs --seed or --ckpt")
        return cmd_resolve(a)
    return cmd_why(a)


if __name__ == "__main__":
    raise SystemExit(main())
