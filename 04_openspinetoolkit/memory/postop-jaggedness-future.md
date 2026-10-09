> STATUS: DATED (HANDOFF/context/INDEX.md, 2026-10-08). Copied 2026-10-08 into spine-program/04_openspinetoolkit from the handoff's redacted context copy `HANDOFF/context/postop-jaggedness-future.md` (spinesurg-ct-nnunet, branch L6_Class, 097933a); toolkit cut list. A note is a dated record of the session that wrote it, not an instruction: where it and a result file or docs/handoff/RESULTS_CATALOG.md disagree, the file and the catalog win.

---
name: postop-jaggedness-future
description: FUTURE — fix post-op synthesis voxel roughness so endplates can be auto-remeasured (instead of analytic carry-forward)
metadata: 
  node_type: memory
  type: project
  originSessionId: 436e5c70-681e-4f38-aab2-30dfa25af7b5
---

The post-op synthesis (rotate/bend the spine, resample the voxels) leaves **microscopic voxel roughness** on the vertebral endplates. It's invisible to the eye (the image looks smooth/good), but the automatic endplate plane-fit in [[postop-spine-synthesis.md]] trips on it and returns wrong angles (measured LL *dropped* 45.7→~24 when it should *rise* to ~55).

**Current workaround (decided 2026-06-23):** don't re-measure the resampled image at all. Compute post-op numbers + overlay **analytically** — take the clean pre-op endplate measurements and apply the known bend rotation (proven exact: rotate L1 by +9.3° → 45.7→55.0°). The resampled image is used for *display only*.

**Future goal (user wants):** fix the jaggedness so automatic re-measurement works again — e.g. anti-aliased/higher-order label resampling, morphological endplate smoothing before fitting, a more robust endplate fitter, or per-vertebra rigid placement (no shear) instead of a continuous per-voxel rotation field. Then the synthesis becomes self-validating again.
