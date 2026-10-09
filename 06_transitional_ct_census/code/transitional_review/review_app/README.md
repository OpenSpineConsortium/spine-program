<!-- copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/README.md; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin. -->

---
title: Transitional-vertebra review
emoji: 🦴
colorFrom: gray
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# review_app — two-stage review over the transitional-vertebra review tree

Implements `docs/ruleclass/PREREG_rules.md` section 7: a stage-1 screener (accept / reject / unsure with a
reason; the registry's prior call hidden) and a stage-2 confirmer who sees only stage-1 accepts and unsures,
blinded to the stage-1 verdict, reason and identity (confirm / overturn / unsure with a reason). Timestamps at
claim and at submit are taken by the server; `edit_seconds` is computed there. The ledger is append-only.
Reviewer instructions are in `docs/REVIEW_TRANSITIONAL.md`; the tree contract is the header of `manifest.py`.

## Local run

```bash
cd tools/transitional_review
python -m review_app --selftest                     # 3-case fake tree; exit 1 on any mismatch
python -m review_app --root <tree> --check          # validate a built tree
python -m review_app --root <tree> --port 7860      # serve; dev tokens (token == user name) unless REVIEW_USERS
```

Open http://127.0.0.1:7860/, log in as (username withheld) / (username withheld) (dev mode), click *next case*.

## Configuration (environment or flags)

| variable | flag | meaning |
|---|---|---|
| `REVIEW_ROOT` | `--root` | the review tree (`manifest.tsv`, `cases/<id>/...`) |
| `REVIEW_LEDGER` | `--ledger` | ledger directory (default `<root>/ledger`) |
| `REVIEW_PREREG` | `--prereg` | `PREREG_rules.md` whose sha256 goes into every record (default: `<root>/PREREG_rules.md`, else the repo copy) |
| `REVIEW_USERS` | `--users` | JSON `{"(username withheld)": {"token": "...", "role": "screener"}, "CONFIRMER": {"token": "...", "role": "confirmer"}, "greg": {"token": "...", "role": "admin"}}`; a path to such a file also works |
| `REVIEW_SCREENER` / `REVIEW_CONFIRMER` / `REVIEW_ADMINS` | `--screener` … | names used when an `hf_` token is resolved through `whoami`; the confirmer's name is a config value (placeholder `CONFIRMER`) |
| `REVIEW_PUBLIC_NAMES` | `--public-names` | show reviewer names on the dashboard (off by default) |
| `REVIEW_CLAIM_TTL` | `--claim-ttl` | seconds before an unsubmitted claim can be taken by someone else (3 days) |
| `REVIEW_REVIEWER_TREE_PATH` | `--reviewer-tree-path` | where the tree is mounted on the reviewers' machines; used in the open-in-viewer commands |
| `REVIEW_TREE_REPO` | — | private HF dataset holding the tree's text + previews; pulled to `--root` at startup if no manifest is there |
| `REVIEW_LEDGER_REPO` + `HF_TOKEN` | `--ledger-repo` | private HF dataset the ledger is mirrored into (pull at startup without overwriting, push on every write) |
| — | `--show-prior-to-confirmer` | unblind the registry's prior call for stage 2 only (default: hidden from both) |
| — | `--reason-optional` | do not require a reason with every verdict (PREREG asks for one; default required) |

Roles: `screener` claims stage 1, `confirmer` claims stage 2, `admin` reads `/audit` and `/audit.csv` and
cannot claim (so the audit reader is never a blinded reviewer). A user who screened a case is never served it at
stage 2.

## Deploy as a private Space

1. Create a **private** Docker Space; push this repository subtree (build context = repo root; the Dockerfile
   copies `review_app/` and `docs/ruleclass/PREREG_rules.md`). Set the build arg `GIT_SHA` to
   `git rev-parse HEAD` or the records will say the sha is unknown.
2. Secrets: `HF_TOKEN` (write, for the two private datasets), `REVIEW_USERS`. Variables: `REVIEW_TREE_REPO`,
   `REVIEW_LEDGER_REPO`, optionally `REVIEW_CONFIRMER`, `REVIEW_ADMINS`, `REVIEW_REVIEWER_TREE_PATH`.
3. Upload the tree's text and previews (not the volumes) to `REVIEW_TREE_REPO`:
   `manifest.tsv`, `types.tsv`, `PREREG_rules.md`, `cases/*/README.md`, `cases/*/evidence.json`,
   `cases/*/previews/*.png`, `cases/*/open_commands.json`.
4. Reviewers keep a synced copy of the full tree (volumes, `.mrb`, `xr_*_P.txt`) at
   `REVIEW_REVIEWER_TREE_PATH` and open volumes locally; the Space serves text, previews and the verdict forms.

## API

| method | path | who | body / result |
|---|---|---|---|
| POST | `/api/claim` | screener, confirmer | next case for the caller's stage (204 when the queue is empty); re-serves an open claim |
| POST | `/api/submit` | claim holder | form `claim_token`, `verdict`, `reason` → `{final, review_id, edit_seconds}` |
| POST | `/api/release` | claim holder | form `claim_token` → the case returns to the queue |
| GET | `/api/case/{id}` | claim holder | the blinded payload |
| GET | `/case/{id}/preview/{png}` | claim holder | image |
| GET | `/api/status` | anyone | counts |
| GET | `/api/audit`, `/audit.csv`, `/audit` | admin | per-case join of both stages, hidden manifest columns, header fields |

Auth: `Authorization: Bearer <token>` or the login cookie (`/login`).

## Ledger layout

```
<ledger>/cases/<case_id>.json                       claims, both stage results, history of events (append-only)
<ledger>/reviews/<case_id>/stage1_<review_id>.json  immutable verdict record
<ledger>/reviews/<case_id>/stage2_<review_id>.json
```

Every review record carries `prereg_sha256`, `prereg_status`, `prereg_path`, `git_sha` (or `git_sha_error`),
`tool`, `tool_version`, `written_at_utc`, `input_sha256` (manifest, types, README, evidence, previews, PREREG as
served), `manifest_sha256`, `manifest_row_sha256`, `review_id`, `case_id`, `stage`, `role`, `user`, `verdict`,
`reason`, `claimed_at`, `submitted_at`, `edit_seconds`, `claim_token`, `case_type`, `paired`, `flags`, `rules`,
`collection`, `person_key`.
