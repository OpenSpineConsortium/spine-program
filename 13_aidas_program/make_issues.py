"""Open the AIDaS program's goal, epics and tasks as issues and link them.

plan.json is the source. Each item without an issue number is opened as an issue, its number written back at once,
so a run that stops halfway resumes where it stopped. Each epic becomes a sub-issue of the goal and each task a
sub-issue of its epic, which is the tree SymphonyBoard's Explore tab and the Dependencies section draw; each task's
"waits_on" becomes GitHub's native "blocked by". Run it with `python3 make_issues.py` where `gh` is signed in;
`--dry-run` prints what it would open.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = "OpenSpineConsortium/spine-program"
PLAN = Path(__file__).with_name("plan.json")
OWNER_LABELS = {"aschehr": "worker:aschehr", "greg": "worker:Gregory-Schwing-MD-PhD"}
OWNER_NAMES = {
    "aschehr": "Ashley (worker:aschehr)",
    "greg": "Greg (worker:Gregory-Schwing-MD-PhD)",
    "han": "Dr. Han, the PI (no login here; not queued for a worker)",
    "schwiebert": "Dr. Schwiebert, the Co-PI (no login here; not queued for a worker)",
}


def gh(*args, payload=None):
    command = ["gh", "api", *args]
    if payload is not None:
        command += ["--input", "-"]
    result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"gh api {' '.join(args)}: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def save(plan):
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=True) + "\n")


def task_body(task, epic, numbers):
    lines = [task["body"], "", f"- Epic: #{epic['issue']}", f"- Owner: {OWNER_NAMES[task['owner']]}",
             f"- Gate: {task['gate']}"]
    if task.get("reforms"):
        lines.append(f"- REFORMS: {task['reforms']} (13_aidas_program/REFORMS.md)")
    waits = [f"#{numbers[key]}" for key in task.get("waits_on", [])]
    if waits:
        lines.append(f"- Waits on: {', '.join(waits)}")
    lines += ["", "Work it by docs/agents/PROTOCOL.md under 13_aidas_program/CLAUDE.md's rules: a claim branch "
              "`claude/<this issue>`, the gate sealed before the first job, the REFORMS record kept as you go."]
    return "\n".join(lines)


def open_issue(title, body, labels, dry_run):
    if dry_run:
        print(f"would open: {title} {labels}")
        return {"number": 0, "id": 0}
    issue = gh(f"repos/{REPO}/issues", "--method", "POST",
               payload={"title": title, "body": body, "labels": labels})
    print(f"#{issue['number']} {title}")
    return issue


def issue_id(number):
    return gh(f"repos/{REPO}/issues/{number}")["id"]


def link_parent(parent, child_number):
    try:
        gh(f"repos/{REPO}/issues/{parent}/sub_issues", "--method", "POST",
           payload={"sub_issue_id": issue_id(child_number)})
    except RuntimeError as error:
        if "already" not in str(error).lower() and "duplicate" not in str(error).lower():
            raise


def link_blocker(number, blocker):
    try:
        gh(f"repos/{REPO}/issues/{number}/dependencies/blocked_by", "--method", "POST",
           payload={"issue_id": issue_id(blocker)})
    except RuntimeError as error:
        print(f"  blocked-by #{blocker} on #{number} not set: {error}", file=sys.stderr)


def main(dry_run=False):
    plan = json.loads(PLAN.read_text())
    keep = (lambda _plan: None) if dry_run else save
    goal = plan["goal"]
    numbers = {}
    if not goal.get("issue"):
        goal["issue"] = open_issue(goal["title"], goal["body"], ["epic"], dry_run)["number"]
        keep(plan)
    for epic in plan["epics"]:
        fresh_epic = not epic.get("issue")
        if fresh_epic:
            epic["issue"] = open_issue(f"{epic['key']}: {epic['title']}",
                                       f"{epic['body']}\n\n- Goal: #{goal['issue']}", ["epic"], dry_run)["number"]
            keep(plan)
            if not dry_run:
                link_parent(goal["issue"], epic["issue"])
        for task in epic["tasks"]:
            if task.get("issue"):
                numbers[task["key"]] = task["issue"]
                continue
            labels = ["todo", OWNER_LABELS[task["owner"]]] if task["owner"] in OWNER_LABELS else []
            body = task_body(task, epic, numbers)
            task["issue"] = open_issue(f"{task['key']}: {task['title']}", body, labels, dry_run)["number"]
            numbers[task["key"]] = task["issue"]
            keep(plan)
            if not dry_run:
                link_parent(epic["issue"], task["issue"])
                for key in task.get("waits_on", []):
                    link_blocker(task["issue"], numbers[key])


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
