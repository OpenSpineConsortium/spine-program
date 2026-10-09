#!/usr/bin/env python
# copy record: source OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path tools/render_board.py; copied 2026-10-08 into spine-program/11_students_grid_access; redactions: none
"""Render BOARD.md from board.json, and refuse a board that is not well formed.

    python tools/render_board.py            # writes BOARD.md
    python tools/render_board.py --check    # exits 1 if BOARD.md is stale or board.json is malformed

A card must name a lead who exists in `people`, a contact email (its own or its lead's), and a state from
`states`; ids must be unique. A card without a co-lead renders as UNSTAFFED rather than being hidden: the board
exists so that gaps are visible. Nothing here invents a person or an email; a missing email prints as
"ask the lead".
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "board.json"
DST = ROOT / "BOARD.md"


def person(board, key):
    if key is None:
        return None
    p = board["people"].get(key)
    if p is None:
        raise SystemExit(f"board.json: unknown person key {key!r}")
    return p


def fmt_person(p):
    if p is None:
        return "—"
    mail = p.get("email")
    return f"{p['name']} ({mail})" if mail else f"{p['name']} (email: ask the lead)"


def validate(board):
    errs = []
    seen = set()
    for c in board["projects"]:
        pid = c.get("id")
        if not pid:
            errs.append("a card has no id")
            continue
        if pid in seen:
            errs.append(f"duplicate id {pid}")
        seen.add(pid)
        for f in ("title", "question", "state", "lead", "repo", "data", "irb", "updated"):
            if not c.get(f):
                errs.append(f"{pid}: missing {f}")
        if c.get("state") not in board["states"]:
            errs.append(f"{pid}: state {c.get('state')!r} not in {board['states']}")
        if c.get("lead") not in board["people"]:
            errs.append(f"{pid}: lead {c.get('lead')!r} is not in people")
        if c.get("colead") is not None and c["colead"] not in board["people"]:
            errs.append(f"{pid}: colead {c['colead']!r} is not in people")
        for k in (c.get("reviewers") or {}).values():
            if k not in board["people"]:
                errs.append(f"{pid}: reviewer {k!r} is not in people")
        lead = board["people"].get(c.get("lead")) or {}
        if not (c.get("contact") or lead.get("email")):
            errs.append(f"{pid}: no contact email on the card or its lead")
    if errs:
        for e in errs:
            print("ERROR", e, file=sys.stderr)
        raise SystemExit(1)


def render(board):
    out = []
    out.append("# The board\n")
    out.append("Every project in the lab, who leads it, who to email, and how to join. Rendered from "
               "`board.json` by `tools/render_board.py`; edit the JSON, not this file. Roles change by pull "
               "request (RECIPE.md §0 and §10). A project without a co-lead is **UNSTAFFED**: it needs one before "
               "it takes members.\n")
    out.append("**To join:** email the lead with the subject `Join: <id>` and your hours per week. "
               "**To leave:** the handover pull request in RECIPE.md §10.\n")
    out.append("## People\n")
    out.append("| key | name | role | email |\n|---|---|---|---|")
    for k, p in board["people"].items():
        out.append(f"| `{k}` | {p['name']} | {p['role']} | {p.get('email') or 'ask the lead'} |")
    out.append("")
    out.append("## Projects\n")
    out.append("| id | project | state | lead | co-lead | open tasks | updated |\n|---|---|---|---|---|---:|---|")
    for c in board["projects"]:
        lead = person(board, c["lead"])
        co = person(board, c.get("colead"))
        co_s = co["name"] if co else "**UNSTAFFED**"
        out.append(f"| `{c['id']}` | [{c['title']}](#{c['id']}) | {c['state']} | {lead['name']} | {co_s} | "
                   f"{len(c.get('open_tasks') or [])} | {c['updated']} |")
    out.append("")
    for c in board["projects"]:
        lead = person(board, c["lead"])
        co = person(board, c.get("colead"))
        contact = c.get("contact") or lead.get("email")
        out.append(f"<a id=\"{c['id']}\"></a>\n### {c['title']}  `{c['id']}` · {c['state']}\n")
        out.append(f"**Question.** {c['question']}\n")
        out.append(f"- **lead:** {fmt_person(lead)}")
        out.append(f"- **co-lead:** {fmt_person(co) if co else '**UNSTAFFED** — the project needs a co-lead before it takes members'}")
        if c.get("reviewers"):
            rv = ", ".join(f"{role}: {person(board, k)['name']}" for role, k in c["reviewers"].items())
            out.append(f"- **reviewers:** {rv}")
        mem = c.get("members") or []
        out.append(f"- **members:** {', '.join(mem) if mem else 'none yet'}")
        if c.get("alumni"):
            out.append(f"- **alumni:** {', '.join(c['alumni'])}")
        out.append(f"- **contact:** {contact}")
        out.append(f"- **code:** {c['repo']}")
        out.append(f"- **data:** {c['data']}")
        out.append(f"- **IRB:** {c['irb']}")
        tasks = c.get("open_tasks") or []
        if tasks:
            out.append("- **open tasks:**")
            for t in tasks:
                out.append(f"    - [ ] {t}")
        else:
            out.append("- **open tasks:** none")
        out.append("")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if BOARD.md differs from what board.json renders")
    a = ap.parse_args()
    board = json.loads(SRC.read_text(encoding="utf-8"))
    validate(board)
    text = render(board)
    if a.check:
        if not DST.exists() or DST.read_text(encoding="utf-8") != text:
            print("BOARD.md is stale: run tools/render_board.py", file=sys.stderr)
            raise SystemExit(1)
        print("BOARD.md is current")
        return
    DST.write_text(text, encoding="utf-8", newline="\n")
    n = len(board["projects"])
    un = sum(1 for c in board["projects"] if not c.get("colead"))
    print(f"wrote {DST.name}: {n} projects, {un} without a co-lead")


if __name__ == "__main__":
    main()
