"""Open the fluoroscopy video datasets of data_mining/video_issues.json as issues under one epic.

The plan holds one task per fluoro_video record of the atlas. Each item without an issue number is opened, its number
written back at once, so a run that stops halfway resumes where it stopped. The epic becomes a sub-issue of its
parent and each task a sub-issue of the epic, the tree SymphonyBoard's Explore tab draws. Run it from the repository
root with `python3 data_mining/scripts/make_video_issues.py` where `gh` is signed in; `--dry-run` prints what it would
open and writes nothing.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = "OpenSpineConsortium/spine-program"
PLAN = Path(__file__).resolve().parents[1] / "video_issues.json"
OWNER_LABELS = {"aschehr": "worker:aschehr", "greg": "worker:Gregory-Schwing-MD-PhD"}


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


def open_issue(title, body, labels, dry_run):
    if dry_run:
        print(f"would open: {title} {labels}")
        return 0
    number = gh(f"repos/{REPO}/issues", "--method", "POST",
                payload={"title": title, "body": body, "labels": labels})["number"]
    print(f"#{number} {title}")
    return number


def link_parent(parent, child):
    child_id = gh(f"repos/{REPO}/issues/{child}")["id"]
    try:
        gh(f"repos/{REPO}/issues/{parent}/sub_issues", "--method", "POST", payload={"sub_issue_id": child_id})
    except RuntimeError as error:
        if "already" not in str(error).lower() and "duplicate" not in str(error).lower():
            raise


def main(dry_run=False):
    plan = json.loads(PLAN.read_text())
    keep = (lambda _plan: None) if dry_run else save
    epic = plan["epic"]
    if not epic.get("issue"):
        epic["issue"] = open_issue(epic["title"], epic["body"], ["epic"], dry_run)
        keep(plan)
        if not dry_run:
            link_parent(epic["parent"], epic["issue"])
    for task in plan["tasks"]:
        if task.get("issue"):
            continue
        body = f"{task['body']}\n\n- Epic: #{epic['issue']}"
        labels = ["todo", OWNER_LABELS[task["owner"]]]
        task["issue"] = open_issue(f"{task['key']}: {task['title']}", body, labels, dry_run)
        keep(plan)
        if not dry_run:
            link_parent(epic["issue"], task["issue"])


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
