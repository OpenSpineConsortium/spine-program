"""Write PLAN.md from plan.json, so the prose and the issues never disagree.

Run `python3 render_plan.py` after plan.json changes; `--check` exits 1 when PLAN.md is out of date.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
ISSUES = "https://github.com/OpenSpineConsortium/spine-program/issues/"
OWNERS = {"aschehr": "Ashley", "greg": "Greg", "han": "Dr. Han", "schwiebert": "Dr. Schwiebert"}


def link(number):
    return f"[#{number}]({ISSUES}{number})" if number else "not opened"


def render(plan):
    keys = {t["key"]: t["issue"] for e in plan["epics"] for t in e["tasks"]}
    goal = plan["goal"]
    out = ["# The AIDaS program: goal, epics and tasks", "",
           "Written by render_plan.py from plan.json; edit plan.json, then run render_plan.py and make_issues.py.", "",
           f"**Goal** ({link(goal['issue'])}): {goal['title']}.", "", goal["body"], ""]
    for epic in plan["epics"]:
        out += [f"## {epic['key']}: {epic['title']} ({link(epic['issue'])})", "", epic["body"], "",
                "| task | issue | owner | gate | REFORMS | waits on |", "|---|---|---|---|---|---|"]
        for t in epic["tasks"]:
            waits = ", ".join(f"{k} {link(keys[k])}" for k in t.get("waits_on", []))
            out.append(f"| {t['key']} {t['title']} | {link(t['issue'])} | {OWNERS[t['owner']]} | {t['gate']} "
                       f"| {t.get('reforms', '')} | {waits} |")
        out.append("")
    return "\n".join(out)


def main():
    text = render(json.loads((HERE / "plan.json").read_text()))
    target = HERE / "PLAN.md"
    if "--check" in sys.argv:
        sys.exit(0 if target.exists() and target.read_text() == text else 1)
    target.write_text(text)


if __name__ == "__main__":
    main()
