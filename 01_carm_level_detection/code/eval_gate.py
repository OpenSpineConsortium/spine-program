#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/eval_gate.py [tracked at 097933a]
"""The evaluation gate: nothing is scored on a patient the checkpoint -- or anything it was initialised from -- trained
on or was SELECTED on, unless the caller says in writing that the number is not held out.

WHY THIS EXISTS. On 2026-09-23 the recall-vs-angle curve (SchwingNet/results/arc/recall_vs_angle/) was scored on 17
TotalSegmentator subjects that were the VALIDATION subjects dc_P_pooled, dc_A and dc_B kept `best.pt` on, and
rx_lodo_carmlspine_1024 -- "real-only" -- had been initialised from anchor_none_v2_17-1882, whose train set holds five
of those subjects and whose val set a sixth (SchwingNet/results/arc/ARC_CHECK.md item 4). It was the fourth leak of
that shape. The contract (docs/DATA_ACCOUNTING.md) missed it for three reasons, read from the code:
  (1) the gate was OPT-IN, and no evaluator on a manuscript path opted in;
  (2) tools/holdout.py and CHK-1..8 counted only split == "train" as seen, so a subject used to select the
      checkpoint passed as held out;
  (3) nothing recorded what a checkpoint was initialised from.
tools/checkpoint_lineage.py is (3): it writes touched.json, every checkpoint's train and val keys and the union over
its initialisation chain. This module is (1) and (2): every evaluator calls assert_unseen() BEFORE it scores, and
every result JSON carries the verdict in an `eval_gate` block.

THE RULE. An evaluation item is HELD OUT for a checkpoint only if its PATIENT KEY (tools/patient_keys.key_any; a render
inherits its source CT subject) is in NEITHER the train NOR the val/selection set of that checkpoint NOR of ANY
ancestor in its initialisation chain. Public ImageNet/COCO pretraining is the only exempt ancestor, and only when
declared (checkpoint_lineage.PUBLIC_ROOT_RX / PUBLIC_TORCHVISION).

WHAT RAISES, and why each is an error rather than a warning.
  SeenInEvaluation   an evaluation key is in a train or val set on the chain. The exception names every key, the
                     checkpoint or ancestor that holds it, and the split.
  UnresolvedLineage  the chain has a link checkpoint_lineage could not read (a deleted bank, a list rewritten after
                     training, a checkpoint family with no reader, no record at all). UNKNOWN IS NOT CLEAN: a touched
                     set with an unresolved link is a lower bound, and a lower bound cannot certify anything. The
                     two bounds checkpoint_lineage records DO decide a row: a rewritten list whose `corpus` is not a
                     corpus the evaluation holds, and a deleted bank whose `bound` is complete and holds no
                     evaluation key.
  UnkeyedEvalItem    an evaluation item no keying rule recognises. Its patient is unknown, so it cannot be shown
                     to be anyone other than a training patient.
  UngatedInput       a scorer was handed a dump that carries no verdict and records nothing to gate it with.
  UnverifiedDump     a verdict that cannot be bound to the dump it travels with: the dump records no sha256 of the
                     weights that made it, or one the verdict did not check; or the verdict is empty, hand-written,
                     or belongs to another checkpoint or another evaluation set (VERIFY.md item 1b).
THE ONLY WAY PAST ANY OF THEM is an explicit declaration: `--not-held-out "<reason>"` (not_held_out= in code). The gate
still computes everything, and the result JSON's header then says held_out: false with the reason, so a
not-held-out number can never be mistaken for a held-out one. An empty reason is refused.

BINDING A VERDICT TO ITS DUMP (eval_gate/2, 2026-09-24). A verdict is only as good as the claim that it was computed
for the weights and the items the dump holds. So every check records `checkpoint_sha256`, the sorted `eval_keys` it
tested and their `eval_digest`; stamp() records OUTSIDE the block, in the result itself, `weights_sha256`: the sha256
of every weights file the evaluator names, hashed from the file at write time, and refuses to stamp one the block did
not check. carry() then accepts a held-out verdict only when its checks are non-empty and complete, the dump's
recorded sha256 set equals the checked one, and the items the dump scored key to the checked set (digest equal for a
dump an evaluator wrote; contained in it for a scorer's pooled output). A dump that records no sha256 is refused, as
is `tools/arc_recall_eval.py --matches` on a matches file made by other weights than --weights names.

    python tools/eval_gate.py check --ckpt <best.pt> --image-dir <realxray root> --split test
    python tools/eval_gate.py check --ckpt <best.pt> --key ts:s0585 --key ts:s1062
    python tools/eval_gate.py check --ckpt <best.pt> --set-info <anglesweep>/SET_INFO.json
    python tools/eval_gate.py eval-sets --out <dir>/eval_sets.json      # the key lists leak_check CHK-9 reads (grid job)

In code (every evaluator):

    import eval_gate as EG
    EG.add_args(ap)                                               # --not-held-out, --touched
    hdr = EG.assert_unseen(items, weights, where="tools/realxray_eval.py", eval_set=f"{data}#{split}",
                           not_held_out=a.not_held_out, touched=a.touched)
    json.dump(EG.stamp(result, EG.block([hdr])), ...)            # `eval_gate` first in the file
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import os
import platform
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import patient_keys as PK  # noqa: E402

GATE_VERSION = "eval_gate/2"          # 2: checks carry eval_keys/eval_digest; results carry weights_sha256
GRID_HOME = "/wsu/home/go/go24/go2432"
GRID_DATA = "/rs/rs_grp_oschome/go2432/data"
GRID_TOUCHED = f"{GRID_DATA}/or_ready/eval_gate/touched.json"
REPO_TOUCHED = REPO / "SchwingNet" / "results" / "eval_gate" / "touched.json"
RULE = ("an evaluation item is HELD OUT for a checkpoint only if its patient key (tools/patient_keys.key_any; a render "
        "inherits its source CT subject) is in neither the train nor the val/selection set of that checkpoint nor of any "
        "ancestor in its initialisation chain; public ImageNet/COCO pretraining is the only exempt ancestor, and only when "
        "declared. An unresolved link is not clean.")
CAP = 40


# ================================================================================================ errors
class EvalGateError(RuntimeError):
    """Base: the evaluation cannot be certified held out. `header` is the verdict that was computed."""

    def __init__(self, msg, header=None):
        super().__init__(msg)
        self.header = header


class SeenInEvaluation(EvalGateError):
    """An evaluation patient is in a train or val/selection set of the checkpoint or of an ancestor."""


class UnresolvedLineage(EvalGateError):
    """The checkpoint's chain has a link that could not be read, so its touched set is a lower bound."""


class UnkeyedEvalItem(EvalGateError):
    """An evaluation item no keying rule recognises: its patient is unknown."""


class UngatedInput(EvalGateError):
    """A scorer's input carries no gate verdict and records nothing it could be gated with."""


class UnverifiedDump(EvalGateError):
    """A verdict that cannot be bound to the dump it travels with (no or foreign producing sha256, empty or
    hand-written checks, another checkpoint's or another evaluation set's block)."""


def _check_reason(not_held_out):
    if not_held_out is None:
        return None
    r = str(not_held_out).strip()
    if not r:
        raise ValueError("--not-held-out needs a reason: the reason is what the result JSON carries in place of the "
                         "held-out claim, and an empty one says nothing")
    return r


# ================================================================================================ small utilities
def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def norm_path(p):
    """One spelling of a checkpoint path: ~ expanded, separators forward, no trailing noise."""
    p = os.path.expanduser(str(p))
    return os.path.normpath(p).replace("\\", "/")


_SHA = {}


def sha256_of(p):
    try:
        st = os.stat(p)
    except OSError:
        return None
    k = (os.path.realpath(p), st.st_size, int(st.st_mtime))
    if k not in _SHA:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 22), b""):
                h.update(b)
        _SHA[k] = h.hexdigest()
    return _SHA[k]


def add_args(ap):
    """The two flags every gated evaluator takes."""
    ap.add_argument("--not-held-out", default=None, metavar="REASON",
                    help="declare that this evaluation is NOT held out, and why. Without it the evaluator refuses to "
                         "score a patient the checkpoint (or any ancestor) trained or was selected on, a checkpoint "
                         "whose lineage is unresolved, or an item that cannot be keyed. With it, the result JSON's "
                         "eval_gate header says held_out: false and carries the reason.")
    ap.add_argument("--touched", default=None,
                    help="touched.json from tools/checkpoint_lineage.py (default: $EVAL_GATE_TOUCHED, then "
                         f"{GRID_TOUCHED}, then the repo copy SchwingNet/results/eval_gate/touched.json)")
    return ap


# ================================================================================================ the lineage store
class Store:
    """touched.json (+ bounds.json beside it + on-demand entries), indexed by path, realpath and sha256."""

    def __init__(self, path=None, entries=None, bounds=None):
        self.path = str(path) if path else None
        self.entries = {}
        if entries is not None:
            self.entries = {norm_path(k): v for k, v in entries.items()}
        elif path:
            with open(path, encoding="utf-8") as f:
                self.entries = {norm_path(k): v for k, v in json.load(f).items()}
        self.mtime = os.path.getmtime(path) if path and os.path.exists(path) else None
        self._bounds = bounds
        self.ondemand_dir = (Path(path).parent / "ondemand") if path else None
        if self.ondemand_dir and self.ondemand_dir.is_dir():
            for f in sorted(self.ondemand_dir.glob("*.json")):
                try:
                    for k, v in json.load(open(f, encoding="utf-8")).items():
                        self.entries.setdefault(norm_path(k), dict(v, _ondemand=str(f)))
                except Exception:  # noqa: BLE001  (a torn cache file is ignored; the lineage is recomputed)
                    continue
        self._by_sha = defaultdict(list)
        for k, v in self.entries.items():
            if v.get("sha"):
                self._by_sha[v["sha"]].append(k)

    def bounds(self):
        if self._bounds is None:
            self._bounds = {}
            if self.path:
                bp = Path(self.path).parent / "bounds.json"
                if bp.exists():
                    try:
                        self._bounds = json.load(open(bp, encoding="utf-8")).get("banks", {})
                    except Exception:  # noqa: BLE001
                        self._bounds = {}
        return self._bounds

    def add(self, entries, source):
        for k, v in entries.items():
            k = norm_path(k)
            self.entries[k] = dict(v, _ondemand=source)
            if v.get("sha"):
                self._by_sha[v["sha"]].append(k)

    def find(self, checkpoint, sha=None):
        """(key, entry, how) or (None, None, why-not). A file on this host is matched by its sha256 whenever it can
        be hashed: a path whose store row describes a different file (retrained since) is NOT a match.

        sha: the sha256 a DUMP recorded for the weights that made it. Then only a row describing that exact file
        matches -- the path is a hint, the sha is the identity -- so a dump is never gated against whatever file sits
        at its weights path today."""
        p = norm_path(checkpoint)
        cands = [p]
        if os.path.exists(p):
            cands.append(norm_path(os.path.realpath(p)))
        if p.startswith(norm_path("~") + "/"):                       # a grid home spelled as this host's ~
            cands.append(GRID_HOME + p[len(norm_path("~")):])
        on_disk = os.path.isfile(p)
        if sha:
            disk = sha256_of(p) if on_disk else None
            for c in cands:
                e = self.entries.get(c)
                if e is not None and (e.get("sha") == sha or (not e.get("sha") and disk == sha)):
                    return c, e, f"path + the dump's recorded sha256 {sha[:16]}"
            if self._by_sha.get(sha):
                k = self._by_sha[sha][0]
                return k, self.entries[k], f"the dump's recorded sha256 {sha[:16]} (stored under {k})"
            return None, None, (f"{p}: no row in the lineage store describes the file the dump records (sha256 "
                                f"{sha[:16]})" + (f"; the file at that path today is {disk[:16]}" if disk else ""))
        sha = sha256_of(p) if on_disk else None
        for c in cands:
            e = self.entries.get(c)
            if e is None:
                continue
            if sha and e.get("sha") and e["sha"] != sha:
                return None, None, (f"{c}: the lineage store describes a DIFFERENT file at this path (store sha "
                                    f"{e['sha'][:16]}, file on disk {sha[:16]}); it was retrained or replaced after "
                                    "checkpoint_lineage ran")
            how = "path" + (" + sha256 verified" if sha and e.get("sha") else " (file not on this host; sha not checked)"
                            if not on_disk else "")
            return c, e, how
        if sha and self._by_sha.get(sha):
            k = self._by_sha[sha][0]
            return k, self.entries[k], f"sha256 {sha[:16]} (stored under {k})"
        return None, None, f"{p}: no row in the lineage store (by path{' or by sha256' if sha else ''})"


_STORES = {}


def load_store(touched=None):
    """touched: a Store, a dict of entries, or a path; else $EVAL_GATE_TOUCHED, the grid copy, the repo copy."""
    if isinstance(touched, Store):
        return touched
    if isinstance(touched, dict):
        return Store(entries=touched)
    cands = [touched] if touched else []
    if not touched:
        cands += [x for x in os.environ.get("EVAL_GATE_TOUCHED", "").split(os.pathsep) if x]
        cands += [GRID_TOUCHED, str(REPO_TOUCHED)]
    for c in cands:
        c = os.path.expanduser(str(c))
        if os.path.isfile(c):
            key = (os.path.realpath(c), os.path.getmtime(c))
            if key not in _STORES:
                _STORES[key] = Store(c)
            return _STORES[key]
    if touched:
        raise UnresolvedLineage(f"--touched {touched} does not exist; with no lineage store nothing can be certified")
    return Store(entries={})                      # empty: every lookup computes on demand or is unresolved


def compute_lineage(checkpoint, store):
    """Run tools/checkpoint_lineage.py's resolver for one checkpoint (and its ancestors) and add them to the store.
    Grid only: it reads the run's configs, banks and launch scripts. Cached under <touched dir>/ondemand/."""
    import checkpoint_lineage as CL
    home = os.path.expanduser("~")
    cache = store.ondemand_dir or (Path(home) / ".cache" / "eval_gate" / "ondemand")
    cache.mkdir(parents=True, exist_ok=True)
    a = argparse.Namespace(home=home, data=GRID_DATA, registry="~/model_registry", out=str(cache),
                           slurm_dir=[os.path.join(home, "spinesurg-ct-nnunet", "slurm")],
                           d813="~/spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs",
                           verse_manifest="~/VerSeFusion/data/manifest/manifest.csv", sweep_set="", arc_json="",
                           template_cap=60, only_results=False, register=False)
    res = CL.Resolver(a)
    res.node(norm_path(checkpoint), role="scored", named_by=["tools/eval_gate.py (on demand)"])
    closure = res.closure()
    res.shas.save()
    sha = sha256_of(norm_path(checkpoint)) or hashlib.sha256(norm_path(checkpoint).encode()).hexdigest()
    out = cache / f"{sha[:16]}.json"
    json.dump(closure, open(out, "w"), indent=1)
    store.add(closure, str(out))
    return str(out)


def chain_of(checkpoint, store, compute=True, sha=None):
    """(key, entry, [(node key, node entry or None)], how). Raises UnresolvedLineage when no record exists and none
    can be computed here. sha: the producing file's sha256 a dump recorded (Store.find)."""
    k, e, how = store.find(checkpoint, sha=sha)
    if e is None and sha and sha256_of(norm_path(checkpoint)) != sha:
        # the file the dump records is not the one at its path today: computing today's file's lineage would gate
        # the wrong weights, so this stays unresolved
        how += "; the recorded file is not the one at this path, so its lineage cannot be computed here"
    elif e is None and compute and not os.path.isfile(norm_path(checkpoint)):
        how += "; the file is not on this host, so its lineage cannot be computed here"
    elif e is None and compute:
        try:
            src = compute_lineage(checkpoint, store)
            k, e, how2 = store.find(checkpoint, sha=sha)
            how = f"computed on demand by tools/checkpoint_lineage.py ({src}); {how2}"
        except Exception as ex:  # noqa: BLE001
            how = f"{how}; computing it here failed ({type(ex).__name__}: {str(ex)[:300]})"
            e = None
    if e is None:
        raise UnresolvedLineage(
            f"no lineage for {checkpoint}: {how}. What it (and anything it was initialised from) trained and was "
            f"selected on is unknown, and unknown is not clean. Run tools/checkpoint_lineage.py resolve --ckpt "
            f"{checkpoint} on the grid, or declare --not-held-out \"<reason>\".")
    # every ancestor: the list the lineage tool wrote, AND a walk over `parents` through the store, so a row written
    # without `ancestors` (or a parent the list missed) is still followed to the root
    order, seen = [], {k}
    todo = [norm_path(x) for x in (e.get("ancestors") or [])] + [norm_path(x) for x in (e.get("parents") or [])]
    while todo:
        ak = todo.pop(0)
        if ak in seen:
            continue
        seen.add(ak)
        order.append(ak)
        ae = store.entries.get(ak)
        if ae:
            todo += [norm_path(x) for x in (ae.get("parents") or [])]
    nodes = [(k, e)] + [(ak, store.entries.get(ak)) for ak in order]
    return k, e, nodes, how


# ================================================================================================ keying items
_CTX = {}


def _key_ctx():
    """The Dataset813 crosswalk and the VerSe subject map, read once from their grid locations (empty elsewhere)."""
    if "cross" not in _CTX:
        home = os.path.expanduser("~")
        d813 = os.path.join(home, "spinesurg-ct-nnunet", "nnunet", "raw", "Dataset813_SpineSurgLSTVFullRibs")
        _CTX["cross"] = PK.d813_crosswalk(d813) if os.path.isdir(d813) else {}
        vm = os.path.join(home, "VerSeFusion", "data", "manifest", "manifest.csv")
        _CTX["vmap"] = PK.verse_subjects(vm) if os.path.isfile(vm) else {}
    return _CTX


def known_corpora():
    if "corpora" not in _CTX:
        import leak_check as LC
        c = set(PK.CORPUS_OF.values()) | {r["corpus"] for r in LC.RULES} | set(PK._CANON_CORPUS) \
            | set(PK._CANON_CORPUS.values()) | {"carmlspine", "cobra", "deepfluoro", "geneva", "ljubljana", "ts"}
        _CTX["corpora"] = c
    return _CTX["corpora"]


_RE_KEY = re.compile(r"^([a-z][a-z0-9_]*):([^/\\]+)$")


def _is_key_form(s):
    m = _RE_KEY.match(str(s))
    return bool(m and m.group(1) in known_corpora())


def resolve_given_key(s):
    """(canonical key, None) or (None, why) for a '<corpus>:<person>' handed to the gate AS a key.

    Nothing is used as given (VERIFY.md 1b-iii): the key is canonicalised (patient_keys.canon_key), an `implant:`
    key -- a render, not a person -- is mapped to its source CT exactly as the lineage store keys implant renders
    (the make_implant_ct records and declared builds, _implant_ctx), and a key that then names no person of its
    corpus comes back (None, why) and is counted UNKEYED, which raises."""
    ctx = _key_ctx()
    imap, builds = _implant_ctx() if str(s).startswith("implant:") else (None, None)
    return PK.resolve_key(s, imap, builds, ctx["cross"], ctx["vmap"])


def _as_key(s):
    """The canonical key of a string in key form, None when it is not in key form; raises nothing (see key_items)."""
    if not _is_key_form(s):
        return None
    k, _ = resolve_given_key(s)
    return k


def _implant_ctx():
    """Implant renders are keyed to their SOURCE CT exactly as tools/checkpoint_lineage.KeyCtx keys them: through
    make_implant_ct's hardware records, else the one build a launch script declares whose case format fits. Read once,
    and only when an implant render is met (the launch-script scan is the slow part)."""
    if "implant" not in _CTX:
        home = os.path.expanduser("~")
        imap, builds = {}, set()
        try:
            import checkpoint_lineage as CL
            sl = os.path.join(home, "spinesurg-ct-nnunet", "slurm")
            L = CL.scan_launchers([sl], home, ("make_implant_ct.py",)) if os.path.isdir(sl) else []
            B = [x for x in L if x["args"].get("--scheme") and not CL.is_template(x["args"].get("--scheme", ""))]
            builds = {x["args"]["--scheme"] for x in B}
            dsts = {CL.expand_home(x["args"].get("--dst", "~/implant_ct"), home) for x in B}
            hw = sorted(set(glob.glob(os.path.join(home, "implant_*", "hardware")))
                        | {os.path.join(d, "hardware") for d in dsts if not CL.is_template(d)
                           and os.path.isdir(os.path.join(d, "hardware"))})
            imap = PK.implant_sources(hw)
        except Exception:  # noqa: BLE001  (no launch scripts here: implant renders stay unkeyed, and say so)
            pass
        _CTX["implant"], _CTX["implant_builds"] = imap, builds
    return _CTX["implant"], _CTX["implant_builds"]


def _key_name(name, hint):
    ctx = _key_ctx()
    imap, builds = _implant_ctx() if "implant_" in str(name) else (None, None)
    r, why = PK.key_any(str(name), None, ctx["cross"], ctx["vmap"], hint, imap, builds)
    if not r:
        return None, why
    # a rule's key goes through the same person test as a key handed in (a rule that yields a non-person is a bug
    # in the rule, and its item is unkeyed rather than a patient of its own)
    k, why = PK.resolve_key(r["key"], imap, builds, ctx["cross"], ctx["vmap"])
    return (k, None) if k else (None, f"{name}: keyed to {r['key']} by {r.get('scheme')}, which {why}")


def key_items(items, corpus_hint=None):
    """(set of canonical patient keys, n items, [unkeyed (label, why)]).

    An item is a key ('ts:s0585'), a path or name (keyed by its stem, with the corpus its location declares), or a dict
    with any of key / case / stem / path / image / name and optionally hint. EVERY identity field of a dict is keyed and
    the union counted: a supplied `key` never stands in for the case it came with (VERIFY.md 1b-iii: {key: ts:s9999,
    case: TS_s0585} used to be checked as ts:s9999 alone), and counting both can only make the gate stricter. A key
    in key form is resolved (resolve_given_key); one that names no person makes the item UNKEYED, even when its other
    fields key, because a map that hands the gate a non-person is broken and its other entries cannot be trusted."""
    keys, unkeyed, n = set(), [], 0
    for it in items:
        n += 1
        if isinstance(it, dict):
            got, whys, bad_key = set(), [], None
            if it.get("key"):
                if _is_key_form(it["key"]):
                    k, why = resolve_given_key(it["key"])
                    if k:
                        got.add(k)
                    else:
                        bad_key = why
                else:
                    bad_key = f"key {it['key']!r} is not a '<corpus>:<person>' key of a known corpus"
            path = it.get("path") or it.get("image")
            hint = it.get("hint") or corpus_hint or (PK.corpus_hint_for_path(path, os.path.realpath(path))
                                                     if path else None)
            named = set()
            for field in ("case", "stem", "name"):
                v = it.get(field)
                if v:
                    k, why = _key_name(v, hint)
                    (named.add(k) if k else whys.append(why))
            if path and not named:
                k, why = _key_name(os.path.splitext(os.path.basename(str(path)))[0], hint)
                (named.add(k) if k else whys.append(why))
            got |= named
            label = json.dumps({f: it.get(f) for f in ("key", "case", "stem", "path", "image", "name") if it.get(f)})[:200]
            if bad_key:
                keys |= got                       # what did key is still checked; the item still raises as unkeyed
                unkeyed.append((label, bad_key))
            elif got:
                keys |= got
            else:
                unkeyed.append((label, "; ".join(w for w in whys if w) or "no identity field"))
            continue
        s = str(it)
        if _is_key_form(s):
            k, why = resolve_given_key(s)
            if k:
                keys.add(k)
            else:
                unkeyed.append((s[:200], why))
            continue
        hint = corpus_hint or PK.corpus_hint_for_path(s, os.path.realpath(s) if os.path.exists(s) else None)
        k, why = _key_name(os.path.splitext(os.path.basename(s))[0], hint)
        if k:
            keys.add(k)
        else:
            unkeyed.append((s[:200], why))
    return keys, n, unkeyed


# ================================================================================================ the verdict
_CANON_MEMO = {}


def _canon_set(xs):
    """canon_key over a key list; memoised per list object (a store's lists are reused across many checks, and the
    reference is kept so the id cannot be recycled)."""
    if not xs:
        return set()
    m = _CANON_MEMO.get(id(xs))
    if m is not None and m[0] is xs:
        return m[1]
    s = {PK.canon_key(x) for x in xs}
    imp = [x for x in s if x.startswith("implant:")]
    if imp:                                    # a store-side implant key meets its source CT, as an evaluation key does
        for x in imp:
            k, _ = resolve_given_key(x)
            if k:
                s.add(k)
    if isinstance(xs, list) and len(xs) > 64:
        _CANON_MEMO[id(xs)] = (xs, s)
    return s


def _decide_unresolved(rows, keys, store):
    """Split unresolved rows into (undecided, decided). Only the two bounds checkpoint_lineage records decide."""
    corpora = {k.split(":", 1)[0] for k in keys}
    undecided, decided = [], []
    for u in rows:
        c = u.get("corpus")
        if c:
            c = PK._CANON_CORPUS.get(c, c)
            if c not in corpora:
                decided.append(dict(at=u.get("at"), what=u.get("what"),
                                    decided=f"its unread items can only be {c} patients (checkpoint_lineage `corpus`); "
                                            f"the evaluation holds none"))
                continue
        b = u.get("bound")
        if isinstance(b, dict) and b.get("complete") is True:
            bk = (store.bounds().get(b.get("bank")) or {}).get("keys")
            if bk is not None:
                hit = sorted(keys & _canon_set(bk))
                if not hit:
                    decided.append(dict(at=u.get("at"), what=u.get("what"),
                                        decided=f"deleted bank {b.get('bank')}: its complete upper bound "
                                                f"({len(bk)} patients, bounds.json) holds no evaluation key"))
                    continue
                u = dict(u, bound_hits=hit[:CAP], n_bound_hits=len(hit))
        undecided.append(u)
    return undecided, decided


def eval_digest(keys):
    """sha256 over the sorted canonical keys, one per line: the identity of an evaluation set as the gate tested it."""
    return "sha256:" + hashlib.sha256("\n".join(sorted(keys)).encode("utf-8")).hexdigest()


def assess(eval_items_or_keys, checkpoint, where, *, eval_set=None, touched=None, corpus_hint=None, also_seen=None,
           compute=True, not_held_out=None, sha=None):
    """The verdict, never raising on a finding (assert_unseen raises). Returns the header dict.

    sha: the sha256 a dump recorded for the weights that made it; the lineage row must describe that file."""
    reason = _check_reason(not_held_out)
    store = load_store(touched) if checkpoint is not None else None
    keys, n_items, unkeyed = key_items(eval_items_or_keys, corpus_hint)
    hdr = dict(gate="tools/eval_gate.py", gate_version=GATE_VERSION, rule=RULE, where=where, checked_at=now_iso(),
               host=platform.node(), checkpoint=(norm_path(checkpoint) if checkpoint is not None else None),
               checkpoint_sha256=None, lineage_store=(store.path if store else None), lineage_match=None,
               ancestors=[], public_roots=[], eval_set=eval_set, n_items=n_items, n_keys=len(keys),
               keys_by_corpus=dict(Counter(k.split(":", 1)[0] for k in keys)), n_unkeyed=len(unkeyed),
               unkeyed=[f"{a}: {b}" for a, b in unkeyed[:CAP]], overlap=0, overlap_keys=[], overlap_detail=[],
               unresolved=0, unresolved_rows=[], unresolved_decided=[], pose_donor_overlap=0, pose_donor_keys=[],
               also_seen={k: len(v) for k, v in (also_seen or {}).items()}, held_out=None, not_held_out_reason=reason,
               eval_digest=eval_digest(keys), eval_keys=sorted(keys),
               also_seen_digest={k: eval_digest(_canon_set(list(v))) for k, v in (also_seen or {}).items()})
    problems = []
    detail = []
    if checkpoint is not None:
        try:
            k, e, nodes, how = chain_of(checkpoint, store, compute=compute, sha=sha)
        except UnresolvedLineage as ex:
            hdr["unresolved"] = 1
            hdr["unresolved_rows"] = [dict(at=norm_path(checkpoint), what="no lineage record", why=str(ex))]
            nodes, e = [], None
        if e is not None:
            hdr["lineage_match"] = how
            hdr["checkpoint_sha256"] = sha or e.get("sha") or (sha256_of(norm_path(checkpoint)) if os.path.isfile(
                norm_path(checkpoint)) else None)
            hdr["checkpoint_sha256_from"] = ("the dump's own record" if sha else "the lineage store row" if e.get("sha")
                                             else "the file on this host" if hdr["checkpoint_sha256"] else None)
            hdr["ancestors"] = [n for n, _ in nodes[1:]]
            hdr["public_roots"] = list(e.get("public_roots") or [])
            rows = list(e.get("unresolved") or [])
            seen_rows = {json.dumps(r, sort_keys=True, default=str) for r in rows}
            for nk, ne in nodes:
                if ne is None:
                    rows.append(dict(at=nk, what="ancestor not in the lineage store",
                                     why=f"{nk} is named as an ancestor of {k} and has no row: what it saw is unknown"))
                    continue
                for side in ("train", "val"):
                    hit = sorted(keys & _canon_set(ne.get(f"{side}_keys")))
                    for key in hit:
                        detail.append(dict(key=key, at=nk, split=side, ancestor=(nk != k),
                                           sources=[s.get("source") for s in ne.get(f"{side}_sources") or []][:4]))
                for r in ne.get("unresolved") or []:
                    j = json.dumps(r, sort_keys=True, default=str)
                    if j not in seen_rows:
                        seen_rows.add(j)
                        rows.append(r)
            # the union the lineage tool computed must agree with the walk; a key only it holds is still seen
            walked = {d["key"] for d in detail}
            for key in sorted((keys & _canon_set(e.get("touched_keys"))) - walked):
                detail.append(dict(key=key, at=k, split="touched_keys (chain union)", ancestor=None, sources=[]))
            pose = sorted(keys & _canon_set(e.get("touched_pose_keys")))
            hdr["pose_donor_overlap"], hdr["pose_donor_keys"] = len(pose), pose[:CAP]
            undecided, decided = _decide_unresolved(rows, keys, store)
            hdr["unresolved"] = len(undecided)
            hdr["unresolved_rows"] = [{kk: (str(vv)[:600] if kk == "why" else vv) for kk, vv in r.items()
                                       if kk != "bound"} for r in undecided[:CAP]]
            hdr["unresolved_decided"] = decided[:CAP]
    for label, ks in (also_seen or {}).items():
        for key in sorted(keys & _canon_set(ks)):
            detail.append(dict(key=key, at=label, split="fitted in this run", ancestor=False, sources=[]))
    ov = sorted({d["key"] for d in detail})
    hdr["overlap"], hdr["overlap_keys"] = len(ov), ov[:CAP]
    # every (checkpoint, split) with its FULL count -- the detail list is capped, and a cap that shows only the first
    # split walked would hide that a key sits in train AND val
    hdr["overlap_by"] = dict(Counter(f"{'ancestor ' if d.get('ancestor') else ''}{d['at']}#{d['split']}" for d in detail))
    hdr["overlap_detail"] = detail[:CAP]
    if not keys:
        problems.append("no evaluation item was keyed: an evaluation over nothing certifies nothing")
    if hdr["overlap"]:
        problems.append(f"{hdr['overlap']} evaluation patient(s) seen")
    if hdr["unresolved"]:
        problems.append(f"{hdr['unresolved']} unresolved lineage link(s)")
    if hdr["n_unkeyed"]:
        problems.append(f"{hdr['n_unkeyed']} evaluation item(s) could not be keyed")
    hdr["problems"] = problems
    hdr["held_out"] = (not problems) and reason is None
    return hdr


def _explain(hdr):
    """One line per (checkpoint, split) with its FULL count (overlap_by) and examples from the capped detail."""
    ex = defaultdict(list)
    for d in hdr["overlap_detail"]:
        ex[f"{'ancestor ' if d.get('ancestor') else ''}{d['at']}#{d['split']}"].append(d["key"])
    lines = []
    for tag, n in (hdr.get("overlap_by") or {}).items():
        at, _, split = tag.rpartition("#")
        anc = " (ancestor)" if at.startswith("ancestor ") else ""
        at = at[len("ancestor "):] if anc else at
        lines.append(f"    {n} in the {split.upper()} set of {at}{anc}: {', '.join(ex.get(tag, [])[:12])}"
                     + (" ..." if n > 12 else ""))
    return "\n".join(lines)


def assert_unseen(eval_items_or_keys, checkpoint, where, *, eval_set=None, not_held_out=None, touched=None,
                  corpus_hint=None, also_seen=None, compute=True, sha=None):
    """Raise unless every evaluation patient is unseen by `checkpoint` and its whole initialisation chain.

    checkpoint: a weights path (None for a model fitted inside the caller, whose sets go in `also_seen`).
    also_seen:  {label: keys} for anything the caller itself fits on (a head trained in the run, a fold's fit groups).
    Returns the header dict to write into the result JSON (see block() / stamp())."""
    hdr = assess(eval_items_or_keys, checkpoint, where, eval_set=eval_set, touched=touched, corpus_hint=corpus_hint,
                 also_seen=also_seen, compute=compute, not_held_out=not_held_out, sha=sha)
    if hdr["not_held_out_reason"]:
        print(f"eval_gate: {checkpoint} on {eval_set or where}: DECLARED NOT HELD OUT ({hdr['not_held_out_reason']}); "
              f"found overlap {hdr['overlap']}, unresolved {hdr['unresolved']}, unkeyed {hdr['n_unkeyed']}", flush=True)
        return hdr
    what = f"{checkpoint} on {eval_set or 'the evaluation set'} ({where})"
    if hdr["overlap"]:
        raise SeenInEvaluation(
            f"eval_gate: {what}: {hdr['overlap']} of {hdr['n_keys']} evaluation patients were trained or SELECTED on "
            f"by this checkpoint or an ancestor:\n{_explain(hdr)}\n  A checkpoint selected on a subject has seen it. "
            "This is not a held-out evaluation; to score it anyway say so: --not-held-out \"<reason>\".", hdr)
    if hdr["unresolved"]:
        rows = "\n".join(f"    {r.get('at')}: {r.get('what')} -- {str(r.get('why'))[:240]}"
                         for r in hdr["unresolved_rows"][:8])
        raise UnresolvedLineage(
            f"eval_gate: {what}: the initialisation chain has {hdr['unresolved']} unresolved link(s), so what it saw "
            f"is a lower bound and cannot certify a held-out result:\n{rows}\n  Resolve the lineage "
            "(tools/checkpoint_lineage.py) or declare --not-held-out \"<reason>\".", hdr)
    if hdr["n_unkeyed"]:
        raise UnkeyedEvalItem(
            f"eval_gate: {what}: {hdr['n_unkeyed']} of {hdr['n_items']} evaluation items match no keying rule, so "
            f"their patients are unknown (e.g. {hdr['unkeyed'][:3]}). Add the rule to tools/patient_keys.py / "
            "tools/leak_check.RULES or declare --not-held-out \"<reason>\".", hdr)
    if not hdr["n_keys"]:
        raise UnkeyedEvalItem(f"eval_gate: {what}: no evaluation item at all; nothing is certified by an empty set", hdr)
    print(f"eval_gate: {checkpoint} on {eval_set or where}: HELD OUT ({hdr['n_keys']} patients over {hdr['n_items']} "
          f"items; overlap 0 over {1 + len(hdr['ancestors'])} checkpoint(s) in the chain"
          + (f"; {hdr['pose_donor_overlap']} pose-donor keys reported" if hdr["pose_donor_overlap"] else "") + ")",
          flush=True)
    return hdr


def assert_unseen_all(eval_items_or_keys, checkpoints, where, shas=None, **kw):
    """Every checkpoint an evaluator loads (detector + encoder + head ...): {role: path}. Keys are computed once.
    shas: {role: sha256} a dump recorded for the weights that made it (carry gating a dump at scoring)."""
    keys, n, unkeyed = key_items(eval_items_or_keys, kw.pop("corpus_hint", None))
    items = sorted(keys) + [{"name": u[0]} for u in unkeyed]
    out = []
    for role, ck in checkpoints.items():
        if ck is None:
            continue
        h = assert_unseen(items, ck, f"{where} [{role}]", sha=(shas or {}).get(role), **kw)
        h["role"], h["n_items"] = role, n
        out.append(h)
    return out


def block(headers, not_held_out=None):
    """The `eval_gate` block a result JSON carries: the combined verdict and every check behind it."""
    headers = [h for h in headers if h]
    reasons = sorted({h.get("not_held_out_reason") for h in headers if h.get("not_held_out_reason")})
    if not_held_out:
        reasons = sorted(set(reasons) | {_check_reason(not_held_out)})
    return dict(gate_version=GATE_VERSION, held_out=bool(headers) and all(h.get("held_out") for h in headers)
                and not reasons, not_held_out_reason="; ".join(reasons) or None, n_checks=len(headers),
                overlap=sum(int(h.get("overlap") or 0) for h in headers),
                unresolved=sum(int(h.get("unresolved") or 0) for h in headers), checks=headers)


# ================================================================================================ binding a verdict
_SHA_RE = re.compile(r"[0-9a-f]{64}")


def _flat(v):
    """The sha256 values of a `weights_sha256` record, whatever its shape (one, {name: sha}, [sha, ...])."""
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, dict):
        return list(v.values())
    if isinstance(v, (list, tuple)):
        return list(v)
    return [v]


def _checked_shas(blk):
    return {c.get("checkpoint_sha256") for c in (blk or {}).get("checks") or []
            if isinstance(c, dict) and c.get("checkpoint")}


def weights_record(blk, weights=None):
    """(record, problems): the sha256 of every weights file named, hashed NOW from the file on this host, in the
    shape it was named ({name: path} -> {name: sha}; one path -> one sha). Default: the checkpoints the block checked.
    A problem is a file that cannot be hashed here, or one the block did not check."""
    checked = _checked_shas(blk)
    if weights is None:
        weights = {c["checkpoint"]: c["checkpoint"] for c in (blk or {}).get("checks") or []
                   if isinstance(c, dict) and c.get("checkpoint")}
    if isinstance(weights, (list, tuple)):
        weights = {str(w): str(w) for w in weights if w}
    one = not isinstance(weights, dict)
    named = {"": str(weights)} if one else {k: str(v) for k, v in weights.items() if v}
    rec, bad = {}, []
    for name, p in named.items():
        sha = sha256_of(norm_path(p))
        rec[name] = sha
        if sha is None:
            bad.append(f"{name or p}: {p} is not a file on this host, so the sha256 of the weights that made this "
                       "result cannot be recorded")
        elif sha not in checked:
            bad.append(f"{name or p}: the file at {p} (sha256 {sha[:16]}) is not a checkpoint this verdict checked "
                       f"({sorted(str(x)[:16] for x in checked)})")
    return (rec[""] if one else rec), bad


def stamp(result, blk, weights=None):
    """The result with `eval_gate` as its FIRST key, and beside it `weights_sha256`: the sha256 of the weights that
    made the result, recorded in the result itself (never inside the block) so that carry() can bind the one to the
    other.

    weights: what the evaluator loaded ({role: path} or one path); default the result's own `weights`, else the
    checkpoints the block checked. Each file is hashed now; a held-out block is refused when a file cannot be hashed
    here, is not one the block checked, or the block checked a checkpoint the result does not name. A block that
    came through carry() (a scorer pooling dumps) records the sha256 its input dumps recorded."""
    out = {"eval_gate": blk}
    rest = {k: v for k, v in result.items() if k not in ("eval_gate", "weights_sha256")}
    held = bool(isinstance(blk, dict) and blk.get("held_out"))
    bound = blk.get("bound") if isinstance(blk, dict) else None
    bad = []
    if weights is None and isinstance(bound, list) and bound:
        rec = {s for x in bound for s in (x.get("weights_sha256") or []) if s}
        for c in blk.get("checks") or []:            # a check this scorer made itself: its file must be here
            s = c.get("checkpoint_sha256") if isinstance(c, dict) else None
            if isinstance(c, dict) and c.get("checkpoint") and s not in rec:
                disk = sha256_of(norm_path(c["checkpoint"]))
                if disk and disk == s:
                    rec.add(disk)
                else:
                    bad.append(f"the verdict checked {c.get('checkpoint')} ({str(s)[:16]}), which no carried dump "
                               "recorded and which cannot be hashed here")
        rec = sorted(rec)
    else:
        rw = result.get("weights")
        if weights is None and (isinstance(rw, str) or (isinstance(rw, dict) and rw
                                                        and all(isinstance(v, str) for v in rw.values()))):
            weights = rw                      # the result's own weight paths (a `weights` of numbers is not one)
        rec, bad = weights_record(blk, weights)
        miss = sorted(s for s in _checked_shas(blk) if s and s not in set(_flat(rec)))
        if miss:
            bad.append(f"the verdict checked {len(miss)} checkpoint(s) the result does not name "
                       f"({[m[:16] for m in miss]})")
    if bad and held:
        raise UnverifiedDump("eval_gate.stamp: the result cannot be bound to its verdict: " + "; ".join(bad[:6]), blk)
    out["weights_sha256"] = rec
    out.update(rest)
    return out


def _valid_block(b):
    return isinstance(b, dict) and b.get("gate_version") and "held_out" in b and isinstance(b.get("checks"), list)


def merge(blocks):
    """Several upstream blocks into one (a scorer pooling several dumps). Their bindings travel with them."""
    checks = [c for b in blocks if b for c in b.get("checks", [])]
    reasons = sorted({b.get("not_held_out_reason") for b in blocks if b and b.get("not_held_out_reason")})
    out = dict(gate_version=GATE_VERSION, held_out=bool(blocks) and all(b and b.get("held_out") for b in blocks),
               not_held_out_reason="; ".join(reasons) or None, n_checks=len(checks),
               overlap=sum(int(c.get("overlap") or 0) for c in checks),
               unresolved=sum(int(c.get("unresolved") or 0) for c in checks), checks=checks)
    bound = [x for b in blocks if b for x in (b.get("bound") or [])]
    if bound:
        out["bound"] = bound
    return out


def scored_items(obj):
    """What a dump says it SCORED, as items the gate keys; None when it records nothing of the kind.

    frames (tools/realxray_eval.py and every scorer that keeps frame rows): case / stem / image, with the frame's own
    `hint` or the corpus its `data` directory declares; records (arc matches.json): the subject of every record;
    subjects (arc curves, the prior check): TotalSegmentator ids; eval_items: an explicit list."""
    fr = obj.get("frames")
    if isinstance(fr, list) and fr and isinstance(fr[0], dict):
        hint = PK.corpus_hint_for_path(str(obj.get("data") or "") + "/")
        its = [dict(case=r.get("case"), stem=r.get("stem"), path=r.get("image") or r.get("path"),
                    hint=r.get("hint") or hint)
               for r in fr if isinstance(r, dict) and (r.get("case") or r.get("stem") or r.get("image") or r.get("path"))]
        return its or None
    rec = obj.get("records")
    if isinstance(rec, list) and rec and isinstance(rec[0], dict) and "subject" in rec[0]:
        return [f"TS_{s}" for s in sorted({str(r.get("subject")) for r in rec})]
    sub = obj.get("subjects")
    if isinstance(sub, list) and sub and all(isinstance(x, str) and re.fullmatch(r"s\d{3,5}", x) for x in sub):
        return [f"TS_{s}" for s in sub]
    ei = obj.get("eval_items")
    if isinstance(ei, list) and ei:
        return ei
    return None


_dump_items = scored_items          # the old name, kept for callers


def verify_block(obj, b, where, *, path=None, items=None, primary=None):
    """The verdict `b` bound to the dump `obj` it travels with, or UnverifiedDump (VERIFY.md 1b-ii).

    A block that says held out is accepted only when
      * it has checks, every one a complete gate header that is itself held out, with the evaluation keys it tested
        and their digest (a block with no checks, or checks without keys, is hand-written or pre-eval_gate/2);
      * the sha256 set the dump records for the weights that made it (`weights_sha256`, written by stamp from the
        files) equals the set of checkpoint sha256 its checks tested (a block pasted from another checkpoint fails);
      * the patients the dump scored (scored_items) key to exactly the tested set -- digest equal -- for a dump an
        evaluator wrote itself (`primary`: it names its own `weights`), or lie inside the tested sets for a scorer's
        pooled output (a block from another evaluation set fails).
    A block that says NOT held out is carried as not held out: it cannot make any number held out."""
    src = path or "(in memory)"

    def no(msg):
        raise UnverifiedDump(f"eval_gate: {where}: {src}: {msg}. Re-run the evaluator that wrote it (eval_gate/2 binds "
                             "its verdict to it), or declare --not-held-out \"<reason>\".", b if isinstance(b, dict) else None)

    if not isinstance(b, dict) or not b.get("gate_version") or not isinstance(b.get("held_out"), bool):
        no("its eval_gate block is not a gate verdict (no gate_version, or held_out is not true/false)")
    checks = b.get("checks")
    if b["held_out"] is False:
        # a not-held-out verdict (declared, or found seen) can never make a number held out: carried as it stands,
        # with or without checks behind it
        out = dict(b, carried_from=src)
        out["bound"] = [dict(verified=False, why="not held out: carried as it stands", weights_sha256=
                             sorted({s for s in _flat(obj.get("weights_sha256")) if isinstance(s, str)}))]
        out["bound"][0]["from"] = src
        return out
    if not isinstance(checks, list) or not checks:
        no("its eval_gate block says held out and has no checks; a verdict with no check behind it is hand-written "
           "and is not carried")
    if b.get("not_held_out_reason"):
        no("the block says held out and also carries a not-held-out reason")
    for i, c in enumerate(checks):
        tag = f"check {i} ({(c or {}).get('checkpoint') if isinstance(c, dict) else c!r})"
        if not isinstance(c, dict) or not c.get("gate_version") or "held_out" not in c:
            no(f"{tag} is not a gate header")
        if c.get("held_out") is not True or c.get("not_held_out_reason"):
            no(f"the block says held out but {tag} does not")
        if int(c.get("overlap") or 0) or int(c.get("unresolved") or 0) or int(c.get("n_unkeyed") or 0):
            no(f"the block says held out but {tag} records overlap {c.get('overlap')}, unresolved "
               f"{c.get('unresolved')}, unkeyed {c.get('n_unkeyed')}")
        ek, ed = c.get("eval_keys"), c.get("eval_digest")
        if not isinstance(ek, list) or not ek or not ed:
            no(f"{tag} records no evaluation keys and digest (written before eval_gate/2, or by hand), so what it "
               "tested cannot be compared with what this dump scored")
        if eval_digest(ek) != ed or c.get("n_keys") != len(ek):
            no(f"{tag}: its eval_keys do not reproduce its eval_digest / n_keys; the check was edited")
        if c.get("checkpoint") and not _SHA_RE.fullmatch(str(c.get("checkpoint_sha256") or "")):
            no(f"{tag} records no checkpoint sha256")
    checked = {c["checkpoint_sha256"] for c in checks if c.get("checkpoint")}
    recorded = _flat(obj.get("weights_sha256"))
    if checked or recorded:
        if not recorded or any(not isinstance(x, str) or not _SHA_RE.fullmatch(x) for x in recorded):
            no("it records no sha256 of the weights that made it (`weights_sha256`), so its verdict cannot be shown "
               "to be about those weights")
        if set(recorded) != checked:
            no(f"it was made by weights {sorted(x[:16] for x in set(recorded))} but its verdict checked "
               f"{sorted(x[:16] for x in checked)}: the block belongs to another checkpoint")
    its = items if items is not None else scored_items(obj)
    if primary is None:
        primary = items is None and isinstance(obj.get("weights"), (str, dict))
    bound = dict(verified=True, weights_sha256=sorted(set(recorded)))
    if its is not None:
        k, n, unk = key_items(its)
        if primary:
            if unk:
                no(f"{len(unk)} of the {n} items it scored cannot be keyed (e.g. {[u[0] for u in unk[:2]]})")
            d = eval_digest(k)
            off = [c for c in checks if c["eval_digest"] != d]
            if off:
                no(f"it scored {len(k)} patients (digest {d[7:23]}) but {off[0].get('checkpoint')}'s check tested "
                   f"{off[0].get('n_keys')} (digest {off[0]['eval_digest'][7:23]}): the block belongs to another "
                   "evaluation set")
            bound.update(scored_digest=d, n_scored=len(k), items="digest equal to every check")
        else:
            tested = set().union(*[set(c["eval_keys"]) for c in checks])
            extra = sorted(k - tested)
            if extra:
                no(f"it scored {len(extra)} patient(s) its verdict never tested (e.g. {extra[:4]}): the block belongs "
                   "to another evaluation set")
            bound.update(scored_digest=eval_digest(k), n_scored=len(k), n_scored_unkeyed=len(unk),
                         items="contained in the tested sets")
    else:
        bound["items"] = "the file records no scored items; bound by the weights sha256 only"
    out = dict(b, carried_from=src)
    bound["from"] = src
    out["bound"] = [bound]
    return out


def carry(src, where, *, not_held_out=None, touched=None, items=None):
    """The verdict of an input scored upstream, for a scorer that loads no checkpoint itself.

    src: a path or a loaded dict. Its own `eval_gate` block is carried only when verify_block binds it to the dump
    (sha256 of the producing weights recorded in the dump and checked by the block; scored patients tested by it). A
    dump with no block is gated NOW from what it records -- a realxray_eval / arc dump (`weights` + frames or
    records), a prototype output (prototype_meta.json), a carmlspine_eval score (`pred`), or a file naming its
    upstream dumps (`dump`, `sources[].file`) -- and only if it records the sha256 of the weights that made it: the
    file at a weights path today may not be the one that made the predictions. Anything else raises. With
    not_held_out every refusal becomes a verdict that says held_out: false and why."""
    path = None
    if not isinstance(src, dict):
        path = str(src)
        p = Path(os.path.expanduser(path))
        if p.is_dir():
            return carry_proto(p, where, not_held_out=not_held_out, touched=touched, items=items)
        src = json.load(open(p, encoding="utf-8"))
    reason = _check_reason(not_held_out)
    label = path or "(in memory)"

    def declared(err, checks=()):
        print(f"eval_gate: {where}: {label}: DECLARED NOT HELD OUT ({reason}); refused: {str(err).splitlines()[0][:300]}",
              flush=True)
        return dict(gate_version=GATE_VERSION, held_out=False, not_held_out_reason=reason, n_checks=len(checks),
                    overlap=None, unresolved=None, checks=list(checks), carried_from=label,
                    refused=f"{type(err).__name__}: {str(err)[:800]}",
                    bound=[{"from": label, "verified": False, "why": "declared not held out"}])

    b = src.get("eval_gate")
    if b is not None:
        try:
            out = verify_block(src, b, where, path=label, items=items)
        except UnverifiedDump as e:
            if reason:
                cs = b.get("checks") if isinstance(b, dict) and isinstance(b.get("checks"), list) else []
                return declared(e, cs)
            raise
        if reason and out.get("held_out"):
            out = dict(out, held_out=False, not_held_out_reason=reason)
        return out
    where2 = f"{where} (input {label} carries no eval_gate block; gated at scoring)"
    w = src.get("weights")
    its = items if items is not None else scored_items(src)
    if w and its is not None and isinstance(w, (str, dict)):
        rec = src.get("weights_sha256")
        if isinstance(w, dict):
            shas = {k: (rec.get(k) if isinstance(rec, dict) else None) for k in w}
        else:
            shas = {"": rec if isinstance(rec, str) else None}
        missing = [k or str(w) for k, v in shas.items() if not (isinstance(v, str) and _SHA_RE.fullmatch(v))]
        if missing:
            err = UnverifiedDump(
                f"eval_gate: {where}: {label} records no sha256 of the weights that made it ({missing[:4]}): it was "
                "written before eval_gate/2. The file at its weights path today may not be the one that made these "
                "predictions, so no lineage can certify them. Re-run the evaluator (it records the sha256 now) or "
                "declare --not-held-out \"<reason>\".")
            if not reason:
                raise err
            print(f"eval_gate: {where}: {label}: DECLARED NOT HELD OUT ({reason}); {str(err)[:200]}", flush=True)
            shas = {}
        if isinstance(w, dict):
            out = block(assert_unseen_all(its, w, where2, eval_set=src.get("data"), not_held_out=not_held_out,
                                          touched=touched, shas=shas), not_held_out)
        else:
            out = block([assert_unseen(its, w, where2, eval_set=f"{src.get('data')}#{src.get('split')}",
                                       not_held_out=not_held_out, touched=touched, sha=shas.get(""))], not_held_out)
        out["bound"] = [{"from": label, "verified": bool(shas), "gated_at_scoring": True,
                         "weights_sha256": sorted({v for v in shas.values() if v})}]
        return out
    pred = src.get("pred") or (src.get("args") or {}).get("pred")        # carmlspine_eval score / couple_all.json
    if pred and os.path.isdir(os.path.expanduser(str(pred))):
        its = items if items is not None else [dict(case=r.get("case"), stem=r.get("stem"), hint="carmlspine")
                                               for r in src.get("frames") or [] if r.get("case") or r.get("stem")]
        return carry_proto(pred, where, not_held_out=not_held_out, touched=touched, items=its or None)
    ups = [src["dump"]] if isinstance(src.get("dump"), str) else []
    ups += [s.get("file") for s in src.get("sources") or [] if isinstance(s, dict) and s.get("file")]
    ups = [u for u in ups if u and os.path.exists(os.path.expanduser(u))]
    if ups:
        return merge([carry(u, where, not_held_out=not_held_out, touched=touched) for u in ups])
    if not_held_out:
        return dict(gate_version=GATE_VERSION, held_out=False, not_held_out_reason=reason,
                    n_checks=0, overlap=None, unresolved=None, checks=[], carried_from=path,
                    note="the input carried no verdict and recorded nothing to gate it with; declared not held out")
    raise UngatedInput(f"eval_gate: {where}: {path or 'an input'} carries no eval_gate block and records no weights, "
                       "prototype directory or upstream dump to gate it with. Re-run the evaluator that wrote it (it "
                       "now writes the block), or declare --not-held-out \"<reason>\".")


def check_matches_weights(blob, weights, where, *, not_held_out=None):
    """A predictions file reused in place of predicting (tools/arc_recall_eval.py --matches): it must have been made
    by the very files --weights names. Every name must be in the file's `weights_sha256` with the sha256 of the file
    --weights names today; a file recording none, or another sha256, raises UnverifiedDump unless declared. Returns the
    list of problems (empty when bound)."""
    rec = blob.get("weights_sha256")
    bad = []
    for name, p in weights.items():
        want = sha256_of(norm_path(p))
        got = rec.get(name) if isinstance(rec, dict) else None
        if want is None:
            bad.append(f"{name}: --weights {p} is not a file on this host, so it cannot be compared with the file that "
                       "made the predictions")
        elif not got:
            bad.append(f"{name}: the predictions file records no sha256 for {name} (weights it names: "
                       f"{(blob.get('weights') or {}).get(name)}); what made them is unknown")
        elif got != want:
            bad.append(f"{name}: the predictions were made by sha256 {got[:16]} ({(blob.get('weights') or {}).get(name)}) "
                       f"but --weights {p} is {want[:16]}: the gate would check weights that did not make them")
    if bad and not _check_reason(not_held_out):
        raise UnverifiedDump(f"eval_gate: {where}: the reused predictions are not the named weights' own:\n    "
                             + "\n    ".join(bad) + "\n  Predict with these weights, or declare --not-held-out \"<reason>\".")
    return bad


# ================================================================================================ one call per evaluator
def gate_evaluation(items, checkpoints, where, a, *, eval_set=None, also_seen=None, corpus_hint=None):
    """The call every evaluator makes BEFORE it scores (docs/DATA_ACCOUNTING.md 5.3: not opt-in): every checkpoint it
    loads ({role: path}; one path is role 'model'; None entries skipped) against every evaluation item, with the
    evaluator's own --not-held-out / --touched (add_args). Raises as assert_unseen does; returns the block to stamp."""
    if checkpoints is None or isinstance(checkpoints, (str, os.PathLike)):
        checkpoints = {"model": checkpoints}
    cks = {r: (os.path.expanduser(str(p)) if p else None) for r, p in checkpoints.items()}
    nho = getattr(a, "not_held_out", None)
    hdrs = assert_unseen_all(items, cks, where, eval_set=eval_set, not_held_out=nho, touched=getattr(a, "touched", None),
                             also_seen=also_seen, corpus_hint=corpus_hint)
    if not hdrs and also_seen:                     # nothing loaded, only a model fitted inside the evaluator
        hdrs = [assert_unseen(items, None, where, eval_set=eval_set, not_held_out=nho, also_seen=also_seen,
                              corpus_hint=corpus_hint)]
    if not hdrs:
        raise UnresolvedLineage(f"eval_gate: {where}: no checkpoint was named, so nothing can be certified")
    return block(hdrs, nho)


def write_verdict(out, blk, weights=None, name="eval_gate.json"):
    """For an evaluator whose numbers are not one JSON (CSV, markdown, npz, figures): the verdict, bound to the weights
    by stamp(), written as <out dir>/eval_gate.json (or <out>.eval_gate.json when `out` is a file path)."""
    out = Path(os.path.expanduser(str(out)))
    p = (out / name) if (out.is_dir() or not out.suffix) else out.with_name(out.name + "." + name)
    p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(stamp({"verdict_for": str(out)}, blk, weights), open(p, "w", encoding="utf-8"), indent=1)
    return str(p)


def bank_items(bank, split="val", rung=1):
    """[dict(case=...)] for the cases of a context-crop bank's split (a list of splits, or None for every split):
    the items an evaluator scoring that bank hands the gate."""
    import numpy as np
    bank = Path(os.path.expanduser(str(bank)))
    f = bank if bank.suffix == ".npz" else bank / f"rung_{rung}.npz"
    z = np.load(f, allow_pickle=True)
    case, sp = z["case"].astype(str), (z["split"].astype(str) if "split" in z.files else None)
    want = None if split is None else ({split} if isinstance(split, str) else set(split))
    sel = case if (want is None or sp is None) else case[np.isin(sp, list(want))]
    return [dict(case=c) for c in sorted(set(sel.tolist()))]


def drr_items(roots, cases=None):
    """[dict(case=..., hint=...)] for a render / film bank (<root>/ann/*.json, else <root>/images/*): every case, or
    the ones named. The hint is the corpus the root's location declares."""
    out = []
    for r in ([roots] if isinstance(roots, (str, os.PathLike)) else roots):
        r = Path(os.path.expanduser(str(r)))
        hint = PK.corpus_hint_for_path(str(r) + "/", os.path.realpath(r) + "/")
        if cases is not None:
            names = sorted(set(str(c) for c in cases))
        elif (r / "ann").is_dir():
            names = sorted(p.stem for p in (r / "ann").glob("*.json"))
        else:
            names = sorted(p.stem for p in (r / "images").glob("*") if p.suffix.lower() in (".png", ".jpg", ".npy"))
        out += [dict(case=n, hint=hint) for n in names]
    return out


PROTO_ROLES = (("detector", "detector"), ("level_model", "level_model"), ("head", "head"),
               ("sacrum_detector", "sacrum_detector"))


def proto_checkpoints(meta):
    return {role: meta.get(field) for role, field in PROTO_ROLES if meta.get(field)}


def proto_items(d):
    """The images a tools/level_prototype.py output directory scored (prototype_results.json, else its per-image
    records), keyed by path as the prototype's own gate keyed them."""
    d = Path(os.path.expanduser(str(d)))
    items = []
    rp = d / "prototype_results.json"
    recs = json.load(open(rp, encoding="utf-8")) if rp.exists() else [json.load(open(f)) for f in sorted(d.glob("*.json"))
                                                                       if f.name not in ("prototype_meta.json",)]
    for r in recs if isinstance(recs, list) else []:
        if isinstance(r, dict) and r.get("image"):
            items.append(dict(path=r["image"]))
    return items


def carry_proto(pred_dir, where, *, not_held_out=None, touched=None, items=None):
    """A tools/level_prototype.py output directory: its prototype_meta.json block bound to the models the meta
    records by sha256 and to the images it scored, or -- for a run written before the gate -- a gate from its models,
    only where the meta recorded each model's sha256."""
    d = Path(os.path.expanduser(str(pred_dir)))
    mp = d / "prototype_meta.json"
    if not mp.exists():
        raise UngatedInput(f"eval_gate: {where}: {d} has no prototype_meta.json, so what scored it is unknown")
    meta = json.load(open(mp, encoding="utf-8"))
    reason = _check_reason(not_held_out)
    scored = items if items is not None else proto_items(d)
    if meta.get("eval_gate") is not None:
        try:
            out = verify_block(meta, meta["eval_gate"], where, path=str(mp), items=scored or None,
                               primary=(items is None and bool(scored)))
        except UnverifiedDump as e:
            if not reason:
                raise
            print(f"eval_gate: {where}: {mp}: DECLARED NOT HELD OUT ({reason}); refused: {str(e)[:300]}", flush=True)
            return dict(gate_version=GATE_VERSION, held_out=False, not_held_out_reason=reason, n_checks=0, checks=[],
                        overlap=None, unresolved=None, carried_from=str(mp), refused=f"UnverifiedDump: {str(e)[:800]}",
                        bound=[{"from": str(mp), "verified": False, "why": "declared not held out"}])
        if reason and out.get("held_out"):
            out = dict(out, held_out=False, not_held_out_reason=reason)
        return out
    cks = proto_checkpoints(meta)
    shas = {role: meta.get(f"{field}_sha256") for role, field in PROTO_ROLES if role in cks}
    missing = [r for r, s in shas.items() if not (isinstance(s, str) and _SHA_RE.fullmatch(s))]
    if missing:
        err = UnverifiedDump(f"eval_gate: {where}: {mp} (written before the gate) records no sha256 for {missing}; the "
                             "file at that path today may not be the one that named these images. Re-run "
                             "tools/level_prototype.py or declare --not-held-out \"<reason>\".")
        if not reason:
            raise err
        shas = {r: s for r, s in shas.items() if r not in missing}
    out = block(assert_unseen_all(scored, cks, f"{where} (legacy prototype output {d}; gated at scoring)",
                                  eval_set=str(d), not_held_out=not_held_out, touched=touched, shas=shas), not_held_out)
    out["bound"] = [{"from": str(mp), "verified": not missing, "gated_at_scoring": True,
                     "weights_sha256": sorted({s for s in shas.values() if s})}]
    return out


# ================================================================================================ evaluation sets (CHK-9)
RX = f"{GRID_DATA}/realxray"
# The evaluation sets the quoted results name (SchwingNet/results/eval_gate/quoted_results.json `eval_sets`), as
# enumerable files. `eval-sets` keys every item and writes eval_sets.json; leak_check CHK-9 intersects those keys with
# touched.json. A set whose items cannot be listed here is absent from eval_sets.json, and CHK-9 fails its rows.
EVAL_SET_SPECS = {
    "carm_test": dict(kind="realxray", root=f"{RX}/carmlspine", splits=["test"]),
    "carm_k": dict(kind="realxray", roots=[f"{RX}/carmlspine_crops/k1/test", f"{RX}/carmlspine_crops/k3/test"], splits=[""]),
    "cobra_test": dict(kind="realxray", root=f"{RX}/cobra_elekta", splits=["test"]),
    "df_test": dict(kind="realxray", root=f"{RX}/deepfluoro", splits=["test"]),
    "df_all6": dict(kind="realxray", root=f"{RX}/deepfluoro", splits=["train", "val", "test"]),
    "geneva_all": dict(kind="realxray", root=f"{RX}/geneva_hip", splits=["train", "val", "test"]),
    "carm_all148": dict(kind="realxray", root=f"{RX}/carmlspine", splits=["train", "val", "test"]),
    "case134_spin": dict(kind="realxray", root=f"{RX}/carmlspine_sweep", splits=["test"]),
    "carm_cv": dict(kind="fold_meta", pattern=f"{RX}/carmlspine_cv/fold{{K}}/kfull/meta", folds=[0, 1, 2, 3, 4],
                    hint="carmlspine"),
    "carm_cvday": dict(kind="fold_groups", groups=str(REPO / "SchwingNet" / "results" / "carmlspine_day_groups.json"),
                       hint="carmlspine"),
    "v8_val": dict(kind="bank", bank=f"{GRID_HOME}/allspine_v8_fov96_ctx", rung=1, split="val"),
    "nhanes25": dict(kind="csv", path=str(REPO / "SchwingNet" / "results" / "a3a_rows.csv"), column="spine"),
    # the 17 SELECTION subjects the first curve was scored on (void: results/arc/recall_vs_angle_selection_leaked/)
    "arc17": dict(kind="set_info", paths=[f"{GRID_DATA}/devcorpus_arc/anglesweep/SET_INFO.json",
                                          str(REPO / "SchwingNet" / "results" / "arc" /
                                              "recall_vs_angle_selection_leaked" / "recall_vs_angle.json")]),
    # its replacement: subjects tools/arc_unseen_subjects.py chose because this gate passes them for every arm
    "arc_unseen": dict(kind="set_info", paths=[f"{GRID_DATA}/devcorpus_arc/anglesweep_unseen/SET_INFO.json",
                                               str(REPO / "SchwingNet" / "results" / "arc" / "recall_vs_angle_unseen" /
                                                   "recall_vs_angle.json")]),
    # Figure 2 (EVAL_LEAKS sweep, 2026-09-23): the v9 validation split as the figure scored it -- persons whose key is
    # in the train split dropped (figure2_metrics.json#cleaning) -- and the three C-ArmLSpine L6 patients it calls
    # never seen. Before these, the Figure 2 rows fell through build_inventory's classifier as counts and went unchecked.
    "v9_val_clean": dict(kind="bank", bank=f"{GRID_HOME}/allspine_v9_fov96_ctx", rung=1, split="val", minus_split="train"),
    "v9_val": dict(kind="bank", bank=f"{GRID_HOME}/allspine_v9_fov96_ctx", rung=1, split="val"),
    "carm_l6_never_seen": dict(kind="json_keys", path=str(REPO / "SchwingNet" / "results" / "figure2" / "figure2_metrics.json"),
                               field="heldout_gate_check.patients"),
}


def realxray_items(root, split):
    root = os.path.expanduser(root)
    img = os.path.join(root, "images", split) if split else os.path.join(root, "images")
    hint = PK.corpus_hint_for_path(root + "/")
    items = []
    for p in sorted(glob.glob(os.path.join(img, "*.png")) + glob.glob(os.path.join(img, "*.jpg"))):
        stem = os.path.splitext(os.path.basename(p))[0]
        mp = os.path.join(root, "meta", stem + ".json")
        case = None
        if os.path.exists(mp):
            try:
                case = json.load(open(mp)).get("case")
            except Exception:  # noqa: BLE001
                case = None
        items.append(dict(case=case, stem=stem, path=p, hint=hint))
    return items


def set_info_subjects(path):
    d = json.load(open(path))
    subj = d.get("subjects") or (d.get("set_info") or {}).get("subjects") or []
    return [f"TS_{s}" for s in subj]


def build_eval_set(spec):
    """{keys, n_items, unkeyed, source[, folds]} for one spec."""
    kind = spec["kind"]
    if kind == "realxray":
        items, srcs = [], []
        for root in spec.get("roots") or [spec["root"]]:
            for sp in spec["splits"]:
                got = realxray_items(root, sp)
                items += got
                srcs.append(f"{root}/images/{sp} ({len(got)})")
        keys, n, unk = key_items(items)
        return dict(keys=sorted(keys), n_items=n, unkeyed=[f"{a}: {b}" for a, b in unk[:CAP]], n_unkeyed=len(unk),
                    source="; ".join(srcs))
    if kind == "fold_meta":
        folds, allk, n_all, unk_all = {}, set(), 0, []
        for K in spec["folds"]:
            md = spec["pattern"].replace("{K}", str(K))
            cases = []
            for f in sorted(glob.glob(os.path.join(md, "*.json"))):
                try:
                    cases.append(dict(case=json.load(open(f)).get("case"), hint=spec.get("hint")))
                except Exception:  # noqa: BLE001  (an unreadable meta is keyed by its file stem, never skipped)
                    cases.append(dict(stem=Path(f).stem, hint=spec.get("hint")))
            keys, n, unk = key_items(cases)
            folds[str(K)] = dict(keys=sorted(keys), n_items=n, n_unkeyed=len(unk), source=md)
            allk |= keys
            n_all += n
            unk_all += unk
        return dict(keys=sorted(allk), n_items=n_all, n_unkeyed=len(unk_all),
                    unkeyed=[f"{a}: {b}" for a, b in unk_all[:CAP]], folds=folds, source=spec["pattern"])
    if kind == "fold_groups":
        g = json.load(open(spec["groups"]))
        groups = g.get("groups", g)
        by = defaultdict(list)
        for case, K in groups.items():
            by[str(int(K))].append(dict(case=case, hint=spec.get("hint")))
        folds, allk, n_all, unk_all = {}, set(), 0, []
        for K, cases in sorted(by.items()):
            keys, n, unk = key_items(cases)
            folds[K] = dict(keys=sorted(keys), n_items=n, n_unkeyed=len(unk), source=f"{spec['groups']} group {K}")
            allk |= keys
            n_all += n
            unk_all += unk
        return dict(keys=sorted(allk), n_items=n_all, n_unkeyed=len(unk_all),
                    unkeyed=[f"{a}: {b}" for a, b in unk_all[:CAP]], folds=folds, source=spec["groups"])
    if kind == "bank":
        import numpy as np
        z = np.load(os.path.join(spec["bank"], f"rung_{spec['rung']}.npz"), allow_pickle=True)
        case = [str(c) for c in z["case"]]
        split = [str(s) for s in z["split"]]
        cases = sorted({c for c, s in zip(case, split) if s == spec["split"]})
        keys, n, unk = key_items([dict(case=c) for c in cases])
        src = f"{spec['bank']}/rung_{spec['rung']}.npz split == {spec['split']}"
        if spec.get("minus_split"):
            # the evaluation as scored after dropping every person the other split holds (Figure 2's cleaning rule);
            # a dropped key is REMOVED from the set, never counted clean
            other = sorted({c for c, s in zip(case, split) if s == spec["minus_split"]})
            okeys, _, _ = key_items([dict(case=c) for c in other])
            dropped = keys & okeys
            keys = keys - okeys
            src += f" minus the {len(dropped)} person keys also in split == {spec['minus_split']}"
        return dict(keys=sorted(keys), n_items=n, n_unkeyed=len(unk), unkeyed=[f"{a}: {b}" for a, b in unk[:CAP]],
                    source=src)
    if kind == "json_keys":
        node = json.load(open(spec["path"], encoding="utf-8"))
        for part in spec["field"].split("."):
            node = node[part]
        keys, n, unk = key_items([PK.canon_key(k) if ":" in str(k) else k for k in node])
        return dict(keys=sorted(keys), n_items=n, n_unkeyed=len(unk), unkeyed=[f"{a}: {b}" for a, b in unk[:CAP]],
                    source=f"{spec['path']}#{spec['field']}")
    if kind == "csv":
        spines = sorted({r[spec["column"]] for r in csv.DictReader(open(spec["path"], newline=""))})
        keys, n, unk = key_items([dict(case=s) for s in spines])
        return dict(keys=sorted(keys), n_items=n, n_unkeyed=len(unk), unkeyed=[f"{a}: {b}" for a, b in unk[:CAP]],
                    source=f"{spec['path']} column {spec['column']}")
    if kind == "set_info":
        for p in spec["paths"]:
            if os.path.exists(p):
                keys, n, unk = key_items(set_info_subjects(p))
                return dict(keys=sorted(keys), n_items=n, n_unkeyed=len(unk),
                            unkeyed=[f"{a}: {b}" for a, b in unk[:CAP]], source=p)
        raise FileNotFoundError(f"none of {spec['paths']}")
    raise ValueError(f"unknown eval-set kind {kind}")


def cmd_eval_sets(a):
    out = {"built": now_iso(), "host": platform.node(), "gate_version": GATE_VERSION, "specs": EVAL_SET_SPECS,
           "sets": {}, "failed": {}}
    for name, spec in EVAL_SET_SPECS.items():
        if a.only and name not in a.only:
            continue
        try:
            out["sets"][name] = build_eval_set(spec)
            s = out["sets"][name]
            print(f"{name:14s} {s['n_items']:6d} items -> {len(s['keys']):5d} patients, {s['n_unkeyed']} unkeyed  "
                  f"({s['source'][:100]})", flush=True)
        except Exception as e:  # noqa: BLE001
            out["failed"][name] = f"{type(e).__name__}: {e}"
            print(f"{name:14s} FAILED {out['failed'][name]}", flush=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"wrote {a.out}: {len(out['sets'])} sets, {len(out['failed'])} failed")
    return 0 if not out["failed"] else 3


# ================================================================================================ CLI
def cmd_check(a):
    items = list(a.key or [])
    if a.items_file:
        items += [l.strip() for l in open(a.items_file) if l.strip()]
    if a.image_dir:
        items += realxray_items(a.image_dir, a.split)
    if a.set_info:
        items += set_info_subjects(a.set_info)
    hdrs = []
    code = 0
    for ck in a.ckpt:
        try:
            hdrs.append(assert_unseen(items, ck, "tools/eval_gate.py check", eval_set=a.eval_set,
                                      not_held_out=a.not_held_out, touched=a.touched, compute=not a.no_compute))
        except SeenInEvaluation as e:
            print(str(e), file=sys.stderr)
            hdrs.append(e.header)
            code = max(code, 1) if code != 3 else 3
        except EvalGateError as e:
            print(str(e), file=sys.stderr)
            hdrs.append(e.header)
            code = 3 if code == 0 else code
    if a.out:
        json.dump(block(hdrs, a.not_held_out), open(a.out, "w"), indent=1)
        print("wrote", a.out)
    return code


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="is this evaluation held out for these checkpoints? exit 0 yes, 1 seen, 3 unknown")
    c.add_argument("--ckpt", action="append", required=True)
    c.add_argument("--key", action="append", help="a patient key (ts:s0585) or an item name/path; repeatable")
    c.add_argument("--items-file", help="one key or item per line")
    c.add_argument("--image-dir", help="a realxray root (images/<split>/*.png + meta/)")
    c.add_argument("--split", default="test")
    c.add_argument("--set-info", help="an anglesweep SET_INFO.json (or a recall_vs_angle.json carrying set_info)")
    c.add_argument("--eval-set", default=None, help="a name for the evaluation set, written into the header")
    c.add_argument("--out", default=None, help="write the eval_gate block here")
    c.add_argument("--no-compute", action="store_true", help="never compute a missing lineage; unknown raises")
    add_args(c)
    e = sub.add_parser("eval-sets", help="key every evaluation set the quoted results name (run on the grid, in a job)")
    e.add_argument("--out", required=True)
    e.add_argument("--only", action="append")
    a = ap.parse_args()
    return cmd_check(a) if a.cmd == "check" else cmd_eval_sets(a)


if __name__ == "__main__":
    raise SystemExit(main())
