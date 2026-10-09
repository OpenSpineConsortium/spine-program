# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/__init__.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""tools/transitional_review -- the transitional-vertebra review tree (PREREG_rules.md section 7).

Components live in sub-packages. `review_app/` is the two-stage screen/confirm web service over a built
review tree; other components (tree builder, scene writers) sit beside it. Nothing here is imported by the
older CTSpinoPelvic1K `review_service`; the two ledgers never mix.
"""
