# 12_website_pacs_demo — working context

The public site of the Open Spine Consortium (https://openspineconsortium.com, served by GitHub Pages from the
repository `OpenSpineConsortium/openspineconsortium.github.io`), the NiiVue PACS demo on case 0003, the X-ray tab
that sends a film to the level service, the level atlas table, the tutorials, the onboarding and Beethoven pages, and
the people page. This folder is the seed of a Claude Code project that maintains them. It is support work: nothing
here is a hypothesis, nothing here is scored, and the one open decision (where the level service is hosted) belongs to
project `01_carm_level_detection`, step S2. Pushing the site publishes it: everything in that repository is public.

## Read first

- `README.md` (the goal, the state on 2026-10-08, the success criteria), then `STATUS.md` and `TODO.md`.
- `MEMORY.md`: the index of `memory/`, one line per note with its status (CURRENT, DATED, PARTLY SUPERSEDED). The notes
  are dated records, not instructions; where one disagrees with a file or `docs/handoff/RESULTS_CATALOG.md`, the file wins.
- `MANIFEST_CODE.md` (the repositories, with URL, branch, commit and the files that matter), `MANIFEST_GRID.md` (the two
  grid paths this project touches), `MANIFEST_LOCAL.md` (what was copied into this folder, from where, and what was not).
- `docs/handoff/README.md` section 5 (the ten rules of the programme) and `docs/handoff/ABOUT_THESE_COPIES.md` (how the
  path prefixes in the handoff copies resolve to repositories).

## Where things are

- **The site.** Repository `OpenSpineConsortium/openspineconsortium.github.io`, branch `master`, custom domain in
  `CNAME`. A local clone goes stale: the clone this seed was read from (c1800f8, 2026-10-02) was ten commits behind origin
  (a17ea39, 2026-10-07). `git pull` before any edit, every time.
- **How a page is made.** Every page is one body fragment under `tools/pages/<url>/body.html` wrapped by
  `python -X utf8 tools/build_site.py`, which writes every page, stamps every asset reference with `?v=<yyyymmddHHMM>`
  and runs its checks (`README.md` of that repository, "Publishing"). Rebuild once, push once, whole tree. Never write a
  header or footer by hand; never add `?v=` by hand. Never hand-edit `beethoven/services.json`, `beethoven/killlist.json`,
  the kept files under `/ashley/` (their SHA-256 is pinned in `KEPT_FILES`) or `googlec3911e7fb095977e.html`.
- **The PACS demo.** `pacs/` in that repository. The CT tab reads `pacs/data/0003/{ct,seg,postop_ct,postop_seg}.nii.gz` and
  `metrics.json` (keys `case_id, summary, geometry, files, label, postop`; read 2026-10-08), produced by
  `tools/export_demo_case.py` of `OpenSpineToolkit` (commit cb43197). The viewer only consumes that contract; any engine
  that emits the same schema drops in (`memory/engine-swap-architecture.md`).
- **The X-ray tab.** `pacs/xr.js` imports `pacs/remote.js`; the model never runs in the page. `remote.js` chooses the
  endpoint from `?service=URL`, then `localStorage.levelIdService`, then `SERVICE_DEFAULT =
  https://level-id.openspineconsortium.org`, which was not live on 2026-09-14 and has not been re-checked (no network
  was used on 2026-10-08). The service code is `service/` of the private repository `spinesurg-ct-nnunet` (097933a); the
  weights sit in the private Hugging Face repository `gregoryschwingmdphd/level-id-weights` and are released only by
  `tools/deploy_service.py`, which refuses a public repository (`memory/level-service-serving.md`).
- **The atlas.** `atlas/level_atlas.csv` (47 data rows: 8 measures at 12 levels, counted 2026-10-08) rendered into
  `atlas/index.html` by `atlas/build_table.py`, so the page carries no hand-typed number. Its source is
  `morphometrics/level_atlas.csv` of `CTSpinoPelvic1K`; the measurements belong to `05_ct_morphometry_parity`.
- **The people and education pages** render at load from `contributions/manifest.json` (20 people on 2026-10-08) and
  `meded/survey-summary.json`. Names on the public site are there by design; they are not copied into this seed, and the
  raw survey CSV is never committed (`meded/README.md`, `.gitignore`).
- **The grid.** Nothing of this project runs on the grid. Two paths are listed in `MANIFEST_GRID.md` because they exist:
  `/wsu/home/go/go24/go2432/level_id_service` (the service as it ran on the login node on 2026-09-14, which must not
  happen again) and `/rs/rs_grp_oschome/go2432/data/gallery` (gallery renders).
- **In this folder.** `figures/logo/` (the consortium mark, its generator and ten renders), `figures/visual_abstract/`
  (the med-ed visual abstract and its build scripts), `docs/handoff/` (the eight student-readable handoff files and one
  extract), `memory/` (27 notes).

## Rules that bind this project (the programme's standing rules, in this folder's words)

1. **Words.** The French-derived word for where data came from is never written; say origin, lineage, source, or where
   it came from. No fractional version numbers: fold a change into the next integer version. Figure captions at most 60
   words; the argument goes in the text. Plain sentences. The affiliation is General Surgery (Wayne State University
   School of Medicine / Detroit Medical Center), never Neurosurgery. Ashley Schehr is a person, never a product name;
   the product is Beethoven.
2. **Every number carries its file**, and what no file records is written "not recorded". A count, a date, a path, a
   latency: name where it was read.
3. **Check outside the computation.** The recurring failure of this programme is a number that is wrong but plausible.
   For this project that means: a latency is measured with `pacs/measure_live.py` through the public host, not
   estimated; a page's number comes from a CSV or JSON the build reads, never typed; the atlas is compared against the
   published series it cites, not against itself.
4. **Labels and orientation.** Two label schemes exist (release v11: L1 = 20 ... L5 = 24, sacrum 26, hips 30/31, femurs
   32/33; legacy: L1 = 1, S1 = 7, sacrum 8, femurs 11/12) and mixing them does not raise. Call
   `ostk.labels.labels_for(volume)`, never import a fixed map. Identifier 29 (the carved S1 of v10) is retired in v11 and
   code that gates on it goes. Case ids are zero-padded (`zfill(4)`). Canonicalise to RAS to analyse and never reorient
   a volume when writing it. The demo bundle of case 0003 is a legacy-scheme (v3) export and the exporter still imports
   `lid`; a re-export from v11 is blocked until the toolkit's S1 fallback is fixed (`STATUS.md`, catalog G.3).
5. **Held out means never seen.** A score may be quoted only if the person was never seen by the checkpoint or any of its
   ancestors, and only after `tools/eval_gate.py` of the private repository passed it. The leaked banks (allspine v2, v6,
   v7, v8 for VerSe, `anchor_drr`, `vindrps`) are never quoted. This site quotes no model score at all; the latency
   numbers in `STATUS.md` are engineering records, not accuracy claims.
6. **Pre-register, then score.** A success number is written before a change is made (`TODO.md` carries one per step).
7. **The grid's login node runs nothing.** Every computation is an `sbatch` job (`sbatch -D <dir>`; chain with
   `afterany`; IPC under `/dev/shm`; large outputs on Ceph `/rs/rs_grp_oschome/go2432`; grid bash is bash 4.2). The level
   service was run on the login node once, on 2026-09-14; it must not be again.
8. **What stays private.** SchwingNet and all level-identification code, text, figures and weights stay private. The site
   never serves a weight: no `.pt`, `.onnx` or `.bin` model file is ever added to the website repository (the 12 `.bin`
   files under `assets/gallery/` are meshes, not models: 874,636 to 1,327,480 B by `git ls-files '*.bin'` at c1800f8 on
   2026-10-08; `gallery/data/` holds only `distributions.json`). Models reach the site only through the service.
9. **Data.** Use all of a public dataset; fix or justify every truncation. No radiograph is ever committed to the site:
   `pacs/testimgs/` (BUU films, not redistributable), `pacs/webtest/` and `pacs/sllp/` stay untracked and are never added.
10. **Git, network, credentials.** On Greg's laptop, network (git push, ssh, rsync) goes through `wsl -e bash -lc '...'`.
    Tokens are read from files only, never echoed, never on a command line. In the site repository and the other code
    repositories this folder names, commit only when Greg asks; in spine-program itself the account doing the work pushes
    only its claim branch `claude/<issue>` and Greg merges (root `CLAUDE.md` rule 10). The Google site-verification file
    is tracked in the site repository and is never copied elsewhere.

## Traps that cost time here

- **The http redirect.** `openspineconsortium.github.io/pacs/` once redirected to `http://openspineconsortium.com`; on http
  `navigator.gpu` is undefined and service workers cannot register, so the demo took 40,018 ms. Forcing https and vendoring
  onnxruntime-web brought it to 1,360 ms (`memory/pacs-website-latency-root-cause.md`; catalog G.8). "Enforce HTTPS" in the
  Pages settings is the fix at the root; its current state is not recorded.
- **HTML is cached for 600 s** by GitHub Pages; assets are busted by the stamp. A page that looks stale ten minutes after
  a push is not a bug.
- **The request form only works on the live site**: the access service answers only `https://openspineconsortium.com`.
- **`pacs/README.md` is partly stale**: its X-ray section still describes in-browser ONNX inference with weights under
  `pacs/models/`; those files were removed on 2026-09-14 and the history rewritten (new head ea0086c). The page now calls
  the service. Update the README before trusting it.
- **The exporter and the legacy scheme.** `export_demo_case.py` imports `lid` and the bundled case is v3-scheme; running
  it on a v11 label without `labels_for` returns plausible wrong numbers, and on v11 the toolkit's `LABELS_V10` still maps
  S1 to 29, so the S1 end-plate falls back to the whole sacrum without a flag (catalog G.3).
- **Never reintroduce** the "SVA/TPA out of scope (needs C7/T1)" sentence or the supine-CT-versus-standing-X-ray framing on
  the demo: Greg removed them because some scans do include C7/T1 (`memory/pacs-demo-and-ostk-params.md`).
- **Student names** live on the public site by design (`contributions/manifest.json`, `headshots/`). They are not copied
  into this seed; usernames are never written anywhere.
