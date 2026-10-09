# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/review_app/Dockerfile; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
# Private Hugging Face Space (Docker SDK) for the transitional-vertebra review app.
# Build context = repository root:
#     docker build -f tools/transitional_review/review_app/Dockerfile --build-arg GIT_SHA=$(git rev-parse HEAD) .
# The Space has no .git, so the commit is baked in as GIT_SHA and written into every review record.
FROM python:3.12-slim

WORKDIR /app
COPY tools/transitional_review/review_app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY tools/transitional_review/review_app /app/review_app
COPY docs/ruleclass/PREREG_rules.md /app/docs/ruleclass/PREREG_rules.md

ARG GIT_SHA=
ENV GIT_SHA=$GIT_SHA \
    REVIEW_ROOT=/data/tree \
    REVIEW_PREREG=/app/docs/ruleclass/PREREG_rules.md \
    PYTHONUNBUFFERED=1

# Spaces run as uid 1000 and route to 7860. /data/tree is filled from REVIEW_TREE_REPO at startup
# (text + previews only); the ledger is mirrored to REVIEW_LEDGER_REPO so a restart loses nothing.
RUN useradd -m -u 1000 user && mkdir -p /data/tree && chown -R user /data /app
USER user
EXPOSE 7860
CMD ["python", "-m", "review_app", "--host", "0.0.0.0", "--port", "7860"]
