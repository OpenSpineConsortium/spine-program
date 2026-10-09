# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/__init__.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""review_app -- two-stage review (screen, then blinded confirm) over the transitional-vertebra review tree.

PURPOSE. PREREG_rules.md section 7 asks for a stage-1 screener who sees the CT, the masks, the radiographs and
the rule evidence but NOT the registry's prior call, and records accept / reject / unsure with a reason and time
stamps; and a stage-2 confirmer who sees ONLY the stage-1 accepts and unsures, blinded to stage 1's verdict, reason
and identity, and records confirm / overturn / unsure with a reason. A per-case audit table joins both. The old
CTSpinoPelvic1K `review_service` (claim -> submit -> IRR -> adjudicate) has none of these fields, so this is a new,
smaller service patterned on its layering (backend / ledger / service / FastAPI app), not a configuration of it.

INPUTS (a review tree built by the sibling component; see manifest.py for the exact contract)
    <tree>/manifest.tsv                one row per case: case_id, type, paired, flags, ... (hidden columns
                                       `registry_*`, `prior_*`, `truth_*` are never served to a reviewer)
    <tree>/types.tsv                   optional: type, rank, meaning (queue order + the one-line meaning shown)
    <tree>/cases/<case_id>/README.md   the case README (free text; must not name the registry call)
    <tree>/cases/<case_id>/evidence.json   rule evidence (top-level "hidden" object and hidden keys are stripped)
    <tree>/cases/<case_id>/previews/*.png  image previews, served if present
    <tree>/cases/<case_id>/{ct*.nii.gz, masks/, labels/, case.mrb, make_slicer_scene.py, xr_<view>_P.txt,
                            open_commands.json}   shown as local paths + open-in-Slicer / ITK-SNAP commands
    docs/ruleclass/PREREG_rules.md     hashed into every record (prereg_sha256, prereg_status)

OUTPUTS (append-only ledger; a re-run never loses a record)
    <tree>/ledger/cases/<case_id>.json                  claims, both stage results, history of events
    <tree>/ledger/reviews/<case_id>/<stage>_<review_id>.json   one immutable record per submitted verdict, carrying
        prereg_sha256, prereg_status, git_sha, tool, tool_version, written_at_utc, input_sha256 (every file the
        reviewer was served), user, stage, verdict, reason, claimed_at, submitted_at, edit_seconds (server-side)
    GET /audit.csv                      the per-case join (admin only); GET / the counts dashboard

RUN
    cd tools/transitional_review && python -m review_app --root <tree> --port 7860
    cd tools/transitional_review && python -m review_app --selftest          # 3-case fake tree, exit 1 on mismatch
    cd tools/transitional_review && python -m review_app --root <tree> --check  # validate a built tree, no server

Identity: `Authorization: Bearer <token>` or the login cookie. Tokens come from REVIEW_USERS (JSON
{"(username withheld)": {"token": "...", "role": "screener"}, "CONFIRMER": {"token": "...", "role": "confirmer"},
"greg": {"token": "...", "role": "admin"}}); an `hf_` token is resolved through huggingface_hub whoami and the
username matched against REVIEW_SCREENER / REVIEW_CONFIRMER / REVIEW_ADMINS. Without REVIEW_USERS the app runs in
dev mode (token == username) and says so loudly. The confirmer's name is a config value (default placeholder
"CONFIRMER"); the stage-1 screener defaults to "(username withheld)".
"""
TOOL_NAME = "transitional_review.review_app"
TOOL_VERSION = "1"
