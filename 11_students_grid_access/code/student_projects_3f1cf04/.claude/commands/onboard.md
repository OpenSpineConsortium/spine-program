<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/Student_Projects local main 3f1cf04 (NOT on origin: origin/main fd60c58 on 2026-10-08), 3f1cf04, path .claude/commands/onboard.md. Copied 2026-10-08. Redactions applied by kind: lead address (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

Onboard me as a new student. I may know nothing about terminals, git or Python; assume
that, and never assume I know what I don't know. Work through the steps in order. Before
each step check whether it is already done and say so; never redo finished work. Explain
each command in one line before running it. When a step needs something only I can do (a
password, a phone code, a browser sign-in, my AccessID), say exactly what to do, wait, and
verify afterwards. If something fails, show me the error in plain words and one thing to
try; if it fails twice, write what happened to `ONBOARDING_LOG.md` and move to the next
step so I can email my mentor the log. Optional argument: $ARGUMENTS (my AccessID, if I gave it).

## Step 0. How much Claude asks
Explain in three sentences: this repository's shared settings already accept file edits
automatically and pre-approve the lab's commands (git, python, ssh to the grid, rsync, the
GitHub and Hugging Face tools), so most of the time nothing is asked; anything outside that
list produces a yes/no prompt, and answering "Yes, and don't ask again" makes it permanent
for this repository. Then offer the hands-off option: setting `permissions.defaultMode` to
`bypassPermissions` in my user settings (`~/.claude/settings.json`) means Claude never asks
before running a command on this laptop; the shared deny list (force-push, hard reset,
deleting a repository) still applies, and `/permissions` undoes it. If I say yes, merge
`{"permissions": {"defaultMode": "bypassPermissions"}}` into that file with a small Python
snippet that preserves any existing keys, show me the result, and tell me it takes effect
when Claude is next started. If I say no, move on; the defaults are fine.

## Step 1. Laptop tools
Run `git --version`, `gh --version`, `claude --version`, `ssh -V`, and `code --version`.
Say which are missing and install each (macOS: brew; Windows: winget; Linux: apt/dnf), or
point me to GETTING_STARTED.md. If `code` exists, run
`code --install-extension anthropic.claude-code --force`. On Windows, note whether we are
in Git Bash, PowerShell or WSL, and use Git Bash or `wsl -e bash -lc` for every `ssh`,
`scp` and `rsync` from here on.

## Step 2. GitHub
1. `gh auth status`. If not logged in, explain that the browser will open and I should
   authorise the GitHub CLI, then run `gh auth login --web --git-protocol https` and
   `gh auth setup-git`. Set `git config --global user.name` and `user.email` if unset,
   asking me for them.
2. `gh repo view OpenSpineConsortium/Projects`. If it says not found or 403, I have not
   been added yet: tell me to email my GitHub username to [the lead's university address]
   with the subject "Projects access", record it in ONBOARDING_LOG.md, and continue; we
   will come back to it in Step 7.
3. If it is visible and `projects/.git` does not exist, run
   `gh repo clone OpenSpineConsortium/Projects projects` from the repository root. (The
   folder `projects/` is ignored by this public repository on purpose; it is its own
   private repository.)

## Step 3. Hugging Face
The dataset mirror is public, so a token is optional today, but one is needed the day I
push anything (a review Space, a model), so set it up now. Ask me to make a free account
at https://huggingface.co/join, then to create a token at
https://huggingface.co/settings/tokens (name "laptop", type "Read" is enough for now), and
paste it to you. Store it with `hf auth login --token <token> --add-to-git-credential`
(or `huggingface-cli login` on older installs). Never echo the token back and never commit
it. Verify with `hf auth whoami` (or `huggingface-cli whoami`).

## Step 4. Grid connection
1. Ask for my WSU AccessID if it is not in the arguments. Confirm I have a grid account
   (GETTING_STARTED "three things", item 1) and Google Authenticator set up (item 2); if
   not, stop here, tell me exactly what to do, and resume when I say so.
2. If `~/.ssh/id_ed25519` does not exist, run
   `ssh-keygen -t ed25519 -C "<accessid>@wayne.edu" -N "" -f ~/.ssh/id_ed25519`.
3. If `~/.ssh/config` has no `Host grid` block, append `templates/ssh_config` with my
   AccessID filled in (on Windows, also in the WSL home if WSL is used).
4. Tell me the next command asks for my grid password and then the six-digit Authenticator
   code, once, then run `ssh-copy-id -i ~/.ssh/id_ed25519.pub grid`.
5. Test: `ssh -o BatchMode=yes grid hostname` must print `warrior` with no prompt.
6. Offer to add the same public key to GitHub (`gh ssh-key add ~/.ssh/id_ed25519.pub --title laptop`)
   so the grid can reach the private repository later through agent forwarding; optional.

## Step 5. The repository and the environment on the grid
1. `ssh -o BatchMode=yes grid "test -d ~/Student_Projects || git clone https://github.com/OpenSpineConsortium/Student_Projects.git"`
   then `ssh -o BatchMode=yes grid "cd ~/Student_Projects && git pull -q && mkdir -p logs"`.
2. The private `projects/` clone on the grid needs my GitHub login there, once. Install the
   GitHub CLI into my grid home if absent:
   `ssh -o BatchMode=yes grid "test -x ~/.local/bin/gh || (mkdir -p ~/.local/bin && curl -sSL https://github.com/cli/cli/releases/latest/download/gh_$(curl -sSL https://api.github.com/repos/cli/cli/releases/latest | grep -o '\"tag_name\": \"v[^\"]*' | cut -dv -f2)_linux_amd64.tar.gz | tar -xz --strip-components=2 -C ~/.local/bin '*/bin/gh')"`.
   Then tell me to open a second terminal, run `ssh grid`, then `~/.local/bin/gh auth login --web --git-protocol https`
   and `~/.local/bin/gh auth setup-git`, enter the one-time code in the browser, and come
   back. Verify with `ssh -o BatchMode=yes grid "~/.local/bin/gh auth status"`. Then
   `ssh -o BatchMode=yes grid "cd ~/Student_Projects && test -d projects/.git || ~/.local/bin/gh repo clone OpenSpineConsortium/Projects projects"`.
   If I have not been added to Projects yet, skip this and note it in the log.
3. If `ssh grid "ls ~/miniforge3/envs/osc ~/mambaforge/envs/osc 2>/dev/null"` finds
   nothing, show me `templates/make_env.sh`, then on my word submit it:
   `ssh -o BatchMode=yes grid "cd ~/Student_Projects && sbatch templates/make_env.sh"` and
   wait with `tools/grid.sh wait <jobid>` in the background. It installs Miniforge if
   needed and creates the `osc` environment.
4. Verify: `ssh grid "source ~/miniforge3/etc/profile.d/conda.sh 2>/dev/null || source ~/mambaforge/etc/profile.d/conda.sh; conda activate osc && python -c 'import nibabel, numpy, scipy; print(nibabel.__version__)'"`.

## Step 6. The dataset on the grid
Ask whether my mentor gave me a path to a shared copy. If yes, record it in my project
CLAUDE.md later. If no, show me `templates/get_dataset.sh`, then on my word submit it; it
downloads the v10 labels and metadata (1.1 GB) from Hugging Face into
`~/data/CTSpinoPelvic1K`. CT volumes (195 GB) only with `CT=1`, and only if the project
needs images rather than labels. Verify `ssh grid "ls ~/data/CTSpinoPelvic1K/labels | wc -l"`
prints 802 and that `manifest.json`, `dataset_labels.json` and `KNOWN_ISSUES.md` are there.

## Step 7. The demo study
Run it on ten records first, as a job, then on all 802:
`/grid-submit examples/pelvic_width_dimorphism/measure_pelvic_width.py --data ~/data/CTSpinoPelvic1K --out examples/pelvic_width_dimorphism/results_mine --workers 8 --limit 10`
then the same without `--limit`. Pull the results back with `/grid-pull` and compare my
`report.txt` with the committed one; the first two decimals should agree. Open the figure
and explain each panel to me in two sentences. While the full run waits, go back to any
step skipped for lack of access and retry it.

## Step 8. Choose a project
Read `IDEAS.md`. Ask me three questions: what I have studied (anatomy, statistics,
programming, none), how many weeks I have, and whether I have a GPU allocation. Propose
three entries that fit, one sentence each on why, and let me choose or bring my own. Then
run `/new-project <topic>` to create the folder in `projects/`, the branch, the filled
`CLAUDE.md` and the proposal interview, and open the pull request with `gh pr create` in
`projects/` using the template, including the email for my ClickUp invitation.

## Step 9. Hand-off
Write today's date and what was completed to `projects/<me>/JOURNAL.md` (or
`ONBOARDING_LOG.md` if there is no project yet). Print the "What done looks like" list
from `GETTING_STARTED.md` with a tick or a cross on each line, and tell me what to email
my mentor (GitHub username, AccessID, the PR link, and anything still crossed).
