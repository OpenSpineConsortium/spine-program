The claim protocol is a vendored release of OpenSpineConsortium/symphony-protocol and .github/workflows/protocol.yml brings each later release in by itself.

- `tools/sdlc_protocol` is a copy of the library at the release `tools/VENDORED` records (0.4.1 since pull request #86,
  2026-10-13; 0.2.0 from the adoption of 2026-10-11 before that), with the sha256 of every copied file; the board, the
  claim rules and the push guard the plugin runs all come from it.
- A rule changes in symphony-protocol, never here: `.github/workflows/protocol.yml` runs weekly (Monday 06:17 UTC) and by
  hand, clones the library, and when its newest release tag is newer than the recorded version, vendors that tag with the
  library's own `scripts/vendor.py`, pushes the branch `symphony-protocol/sync` and opens the pull request from it, or an
  issue linking the pull request where GitHub Actions may not open one (Settings, Actions, General, "Allow GitHub Actions
  to create and approve pull requests"). Greg, or a session on his word, merges it. `tools/protocol_update.py` is the
  workflow's helper.
- A protocol-only adoption gets no such workflow, so the copy stayed at 0.2.0 until pull request #86 added it. By hand,
  the same step is `python3 <symphony-protocol at the tag>/scripts/vendor.py <this clone> --consumer
  OpenSpineConsortium/symphony-template` and a pull request; `python3 -m sdlc_protocol verify-vendored tools` (run in
  the clone's root with `tools` as the folder) holds the copy to the record.
- The template's workers' registry, workers.yml and coordinator.yml, which the protocol text names, are not here: every
  worker is a person's sessions, named by the GitHub login, and the board's own run releases idle claims and tells
  overlapping work.
