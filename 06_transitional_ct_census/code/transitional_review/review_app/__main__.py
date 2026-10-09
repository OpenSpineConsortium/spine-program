# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/__main__.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app/__main__.py -- command line: serve a review tree, validate one, or run the self-test.

    cd tools/transitional_review && python -m review_app --root <tree> --port 7860
    cd tools/transitional_review && python -m review_app --root <tree> --check       # validate, no server
    cd tools/transitional_review && python -m review_app --selftest                  # exit 1 on any mismatch

Inputs: the review tree (manifest.py states the contract), docs/ruleclass/PREREG_rules.md, REVIEW_* environment
(see __init__.py). Outputs: the ledger under <tree>/ledger (or --ledger), served on --host:--port.
In a Space, REVIEW_TREE_REPO (a private HF dataset holding the tree's text and previews, no volumes) is pulled to
--root at startup when --root has no manifest.tsv yet.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _pull_tree(root: Path, repo: str, token: str) -> None:
    from huggingface_hub import snapshot_download
    snapshot_download(repo_id=repo, repo_type="dataset", token=token, local_dir=str(root),
                      allow_patterns=["manifest.tsv", "types.tsv", "PREREG_rules.md", "cases/*/README.md",
                                      "cases/*/evidence.json", "cases/*/open_commands.json",
                                      "cases/*/previews/*"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m review_app", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="review tree (or REVIEW_ROOT)")
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 7860)))
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--ledger", help="ledger directory (default <root>/ledger)")
    ap.add_argument("--prereg", help="PREREG_rules.md to hash into every record")
    ap.add_argument("--users", help="REVIEW_USERS JSON or a path to it")
    ap.add_argument("--screener", help="stage-1 user name (default (username withheld))")
    ap.add_argument("--confirmer", help="stage-2 user name (default placeholder CONFIRMER)")
    ap.add_argument("--admins", help="comma-separated admin user names (audit access)")
    ap.add_argument("--public-names", action="store_true", help="show reviewer names on the dashboard")
    ap.add_argument("--claim-ttl", type=int, help="seconds before an unsubmitted claim is reclaimable")
    ap.add_argument("--show-prior-to-confirmer", action="store_true",
                    help="unblind the registry's prior call for stage 2 only (default: hidden from both)")
    ap.add_argument("--reason-optional", action="store_true", help="do not require a reason with a verdict")
    ap.add_argument("--reviewer-tree-path", help="where the tree sits on the reviewers' machines (shown in commands)")
    ap.add_argument("--ledger-repo", help="private HF dataset to mirror the ledger into (needs HF_TOKEN)")
    ap.add_argument("--check", action="store_true", help="validate the tree and exit")
    ap.add_argument("--selftest", action="store_true", help="run the 3-case self-test and exit")
    ap.add_argument("--keep", help="selftest: keep the fake tree in this directory")
    a = ap.parse_args(argv)

    if a.selftest:
        from .selftest import run
        return run(keep=a.keep)

    from .config import config_from_args
    root = Path(a.root or os.environ.get("REVIEW_ROOT", "")).expanduser()
    tree_repo = os.environ.get("REVIEW_TREE_REPO")
    if tree_repo and str(root) and not (root / "manifest.tsv").exists():
        print(f"[startup] pulling review tree from {tree_repo} into {root}", file=sys.stderr)
        _pull_tree(root, tree_repo, os.environ.get("HF_TOKEN", ""))
    cfg = config_from_args(a)

    if a.check:
        from . import manifest as mf
        m = mf.load_manifest(cfg.root, cfg.hidden_prefixes)
        lines = mf.check_tree(m)
        print(f"manifest.tsv: {len(m.order)} cases, sha256 {m.sha256[:12]}, types "
              f"{'types.tsv' if m.types_path else 'DEFAULT_TYPES'}")
        problems = [ln for ln in lines if not ln.startswith("note:")]
        for ln in lines:
            print(f"  {ln}" if ln.startswith("note:") else f"  problem: {ln}")
        print("clean" if not problems else f"{len(problems)} problem(s), {len(lines) - len(problems)} note(s)")
        return 0 if not problems else 1

    import uvicorn
    from .app import create_app
    app = create_app(cfg)
    uvicorn.run(app, host=a.host, port=a.port, log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())
