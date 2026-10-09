<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path GETTING_STARTED.md. Copied 2026-10-08. Redactions applied by kind: lead address (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# Getting started

One command sets up your laptop and starts Claude Code on the onboarding walkthrough.
Budget an afternoon, plus the two business days the grid takes to create an account.

## Before the command: two accounts

1. **Claude.** Make an account at [claude.ai](https://claude.ai) and subscribe to
   **Claude Pro** (about $20 a month). Claude Code, the assistant that writes and runs
   your code, is included in Pro. Ask your mentor before choosing anything larger.
2. **GitHub.** Make a free account at [github.com](https://github.com) with your name in
   the profile, then email your GitHub username to [the lead's university address] with the
   subject "Projects access". You will be added to the private repository where proposals
   live.

## The command

Open a terminal (macOS: Terminal; Windows: PowerShell; Linux: your terminal) and paste:

| | |
|---|---|
| macOS, Linux, WSL | `curl -fsSL https://openspineconsortium.com/onboard.sh \| bash` |
| Windows PowerShell | `irm https://openspineconsortium.com/onboard.ps1 \| iex` |

It installs what is missing (Git, the GitHub CLI, VS Code with the Claude Code extension,
Claude Code), clones this repository into `~/OpenSpineConsortium/Student_Projects`, and
starts Claude on `/onboard`. Sign in to Claude when the browser opens. From then on Claude
asks you one thing at a time and does the rest: your GitHub sign-in, a Hugging Face account
and token, the SSH key for the grid, the environment and dataset on the grid (as jobs),
the demo study, and a project chosen from `IDEAS.md` and written up as a proposal. Every
step checks whether it is already done, so you can close the terminal and run the command
again later; it picks up where you were.

## The three things only you can do

Claude will stop and tell you exactly when each is needed.

1. **A grid account.** Apply with your AccessID through
   [tech.wayne.edu/kb/high-performance-computing](https://tech.wayne.edu/kb/high-performance-computing)
   (the "Grid account request" form), naming **Gregory Schwing** as sponsor, and email him
   that you applied. Usually two business days. Questions: hpc@wayne.edu, (313) 577-4743.
2. **Google Authenticator.** The grid uses it (not Microsoft Authenticator) as its second
   factor. Install the app, connect to the WSU VPN, log in to
   [ondemand.grid.wayne.edu](https://ondemand.grid.wayne.edu), open **Interactive Apps →
   2FA Setup**, launch it and scan the QR code.
   [C&IT's article with screenshots](https://services.wayne.edu/TDClient/277/Portal/KB/Article/20242).
3. **One password-and-code login.** Claude makes an SSH key and installs it on the grid
   with one command that asks for your grid password and the six-digit code, once. After
   that the grid never prompts again, which is what lets Claude drive it for you.

## About the yes/no prompts

Claude Code asks before it runs a command it has not been told to trust. This repository
ships shared settings that accept file edits automatically and pre-approve everything the
lab workflow uses, so most of the time it does not ask. When it does, "Yes, and don't ask
again" makes that answer permanent for this repository. If you would rather it never asked
on your laptop, `/onboard` offers to switch your own settings to `bypassPermissions` at the
start and explains what that means; the deny list (force-push, hard reset, deleting a
repository) still applies, and `/permissions` turns it back.

## Without the command

If you would rather do it by hand, the [OSC Primer](https://openspineconsortium.github.io/onboarding/)
walks through every step with the reasons, and `/onboard` in Claude Code still works from
any clone of this repository.

## What "done" looks like

- `ssh -o BatchMode=yes grid hostname` prints `warrior` with no prompt
- `gh auth status` says you are logged in, and `projects/` is a clone of the private
  Projects repository
- `~/data/CTSpinoPelvic1K/labels` on the grid holds 802 files
- `examples/pelvic_width_dimorphism/results/report.txt` on the grid matches the one in
  this repository to the second decimal
- a branch `proposal/<lastname>-<topic>` in `projects/`, opened as a pull request

If any step fails, paste the error to Claude and say which step you were on. If Claude is
stuck, email your mentor with the same paste.
