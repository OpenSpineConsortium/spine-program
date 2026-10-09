# MANIFEST_CODE: the repositories this project depends on, and the files that matter

Nothing listed here is copied unless `MANIFEST_LOCAL.md` says so; a file that lives in a repository is reached by
cloning the repository at the commit named. Commits were read with `git log -1` on 2026-10-08. The `code/` folder of this
project holds copies of the files a reader needs without a clone (the service, the 19 pipeline scripts, the untracked
cine tools) with a header line naming the repository path and the commit state.

## 1. spinesurg-ct-nnunet (private)

- URL: `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet.git`. Branch `L6_Class`. Commit
  `097933a414c982db5e22490f84c7f1c7189662e7` (2026-10-08, "HANDOFF: the handoff for a new student or a fresh Claude project").
- Private since 2026-09-14; never push level-identification code public (`memory/fluorocap-repo-private.md`).
- The grid checkout `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` is at 4e3fe93 and cannot fetch; ship by
  `git archive | ssh tar` (`docs/handoff/RECIPES.md` section 0 item 2).
- Working tree on 2026-10-08 (`git status --short`): modified `tools/level_prototype.py`, `tools/carmlspine_eval.py`,
  `tools/patient_keys.py`, `tools/pipeline_state.py`, `tools/test_patient_keys.py`, `SchwingNet/packet_build/reference.docx`,
  `reference_single.docx` (and files of other projects); untracked `tools/cine_eval.py`, `tools/cine_latency.py`,
  `tools/bournemouth_qf_eval.py`, `tools/fluoro_video/`, `SchwingNet/results/cine/`, `HANDOFF/GREG_ONLY/`,
  `tools/transitional_review/`. S0 commits the C-arm ones.

| files | what they are for | copied here |
|---|---|---|
| `tools/level_prototype.py` | the gated reference inference the parity gate is defined against (abstain rule at L355; histogram match to `HOME/films_drr/img/*.npy`; imgsz 1024, conf 0.35, 320 px crops, flip average) | `code/level_prototype.py` (working-tree state) |
| `tools/alphabet_couple.py`, `tools/count_from_sacrum_eval.py` | the coupling and stop signal; the count from the detected sacrum (no learned parameters) | `code/` |
| `tools/eval_gate.py`, `tools/holdout.py`, `tools/checkpoint_lineage.py`, `tools/unseen_cases.py`, `tools/patient_keys.py`, `tools/excluded_sources.py` | the evaluation gate, lineage census, held-out rule, identity keys, excluded sources | `code/` |
| `tools/stats_compare.py` (`--help` crashes on an unescaped `%` at L1220, OQ F20), `tools/model_registry.py`, `tools/publish_checkpoints.py`, `tools/deploy_service.py` | paired tests and power; the registry CLI (S0); the HF mirror publisher; the service release script | `code/` |
| `tools/latency_bench.py`, `tools/eval_runtime_cost.py` (`--selftest`) | the two latency tools; S1 runs `eval_runtime_cost.py --frames CEPH/data/realxray/carmlspine/images --bodies 6 --threads 1 4 16` | `code/` |
| `tools/level_flags.py`, `tools/eval_calibration.py`, `tools/level_selective.py` | LSTV/TLTV flags, calibration (never run: OQ C12), selective prediction (the clean re-run OQ C13) | `code/` |
| `tools/cine_eval.py`, `tools/cine_latency.py`, `tools/bournemouth_qf_eval.py`, `tools/fluoro_video/` | the cine scorer and causal tracker, the per-frame timer with the 1e-5 parity gate, the Bournemouth loader, the panel cutter (untracked at 097933a) | `code/` |
| `tools/device_census.py` (output format `docs/devices/census/*_headers.md`), `tools/inspect_dicom_tree.py`, `tools/carmlspine_io.py` | the DICOM header census and readers S3 needs | `code/device_census.py`; the other two by clone |
| `tools/carmlspine_*.py` (30 files), `tools/case134_*.py`, `tools/carm_sweep.py`, `tools/carm_denominator_repair.py`, `tools/carm_miss_diagnostic.py`, `tools/carm_variant_survey.py` | C-ArmLSpine reading, CBCT to NIfTI, pose by registration, projected level truth, fold dirs, eval, census, QC panels, the 302-frame spin, the denominator repair and miss diagnostic | by clone |
| `tools/realxray_*.py` (12), `lcurve_*.py` (5), `indomain_*.py` (9), `or_crossdev_*.py` (7), `or_lodo_rescore_outline.py`, `or_recall_curves.py`, `or_position_prior.py`, `g3_detector.py`, `g3_leak_intersect.py`, `g3_split_verify.py`, `make_split.py`, `consolidate_splits.py`, `make_fold_banks.py` | real-frame detector training and scoring; the learning curves of Figure 5; the G3 person split and its checks | by clone |
| `tools/{arc_angle_set,arc_curve_compare,arc_prior_check,arc_recall_eval,arc_unseen_subjects,pose_arc,pose_arc_proof,pose_pool_audit}.py` | recall against C-arm angle on unseen subjects; synthetic AP to lateral arcs | by clone |
| `tools/{make_context_crops,train_level_backbone,train_level_classifier,recurrent_order,head_mixed_length,head_dual,stc_head,train_stc_head,message_fusion,ordinal_spine_decode,decode_sequence}.py` | the level encoder and head training harness (`recurrent_order.RunLabeller` is the head class; `recurrent_order.py` L56 carries the wrong-bank attribution, OQ F5) | by clone |
| `tools/{detect_films,detector_chain_report,detector_failures,detector_quality,detector_robustness,build_sacrum_dataset,make_zoom_dataset,check_fluoro_degrade,wholespine_*,thoracic_xr_*,draw_film_boxes,zoom_crop_figure}.py` | the vertebra / sacrum / C2 detectors and their failure anatomy | by clone |
| `tools/{sweep_map,needle_confirm,fiducial_walk,acquisition,guided_console,validate_guided,link_probe,test_masked_link,link_surface_figure,sweep_*,counting_brief,recovery_brief,reproduce_physics,collect_physics_results,physics_figures,physics_validate,fluoro_physics,render_physics_drr,param_census,path_census,frame_levels,window_probe}.py` | the sweep / count / confirm / guided-acquisition line (PRIVATE, invention aspects) and the physics-linking reproduction (`reproduce_physics.py` L113-114 resets the grid checkout: do not use while fetching is broken) | `code/sweep_map.py`; the rest by clone |
| `tools/{device_fit,device_style,device_physics,devcorpus_build,devcorpus_train}.py` | device cards and the styled corpus (project 08); `devcorpus_train.py` writes no `seed` or `code_sha` (S0) | by clone |
| `tools/{claims_check,claims_fill,rsnai_table1,bib_audit,bib_apply_resolved,wordcount_tex,disclosure_audit,disclosure_forensics}.py` | manuscript machinery of the superseded main_v2; the public-surface audit (`disclosure_audit.py` runs before any talk or upload) | by clone |
| `tools/fig*.py` (about 45), `gallery_figure.py`, `gallery_panels.py`, `make_formation_figure.py`, `render_*.py`, `contact_sheet.py`, `_figfit.py` | figure builders for SchwingNet and the superseded drafts | by clone |
| `tools/pipeline_state.py` (modified), `tools/fluorocap_infer.py`, `tools/fluorocap_anchor.py`, `tools/drr_register.py` | the stage-state authority (run it as a job, never on the login node); FluoroCap-era tools | by clone |
| `slurm/{cine_eval,cine_latency}.sh` (untracked), `carmlspine_*.sh` (28, incl. `carmlspine_cv_v9init.sh`, the recipe S7 reuses), `realxray_*.sh` (16), `or_*.sh` (16), `arc_*.sh` (5), `lcurve*.sh`, `d1_*.sh`, `g3_detector.sh`, `sacrum_detector.sh`, `wholespine_*.sh`, `thoracic_xr_*.sh`, `carm_sweep_case39.sh`, `carm_sweep_regress134.sh`, `case134_*.sh`, `eval_gate.sh`, `eval_leaks.sh`, `eval_leaks_gpu.sh`, `gate_recheck.sh`, `checkpoint_lineage.sh`, `claims_check.sh`, `claims_now.sh`, `common_test.sh`, `eval_calibration.sh`, `eval_error_taxonomy.sh`, `level_selective.sh`, `allspine_v9_{bank,keys,train,a5,submit}.sh`, `allspine_v8_*.sh`, `recurrent_head.sh` (L16 wrong-bank attribution, OQ F5), `head_mixed.sh`, `ctx_*.sh`, `devcorpus*.sh`, `device_*.sh`, `guided_validate.sh` | the jobs behind the shipped model, the C-ArmLSpine CV and repairs, the real-frame detectors, the arcs and learning curves, the evaluation-gate runs | by clone |
| `slurm/{sweep_*(16),count_*(5),needle_*,fiducial_walk,physics_*(9),link_ab,link_probe,step_jitter,story_rows*(8),guided_validate,repair_at_operating_point,reproduce_feasibility,reproduce_all,feas_claims,field_ablation,field_recover,strict_fov,surgeon_benefit,window_ablation,window_probe,resolution_ladder,geometry_sweep,recover_matrix,report_final,status_arms}.sh`, `paths2_cases.txt`, `l6_cases.txt` | the sweep / count / confirm / physics jobs (sweep_v3 only is on the right field size) | by clone |
| `slurm/paired_sets_properties.sh` | the job template the recipes name | by clone |
| `SchwingNet/tools/` (80 scripts: `results_macros.py`, `figure1..5` builders, `figS_supplement.py`, `make_supp_*_table.py`, `make_packet.py`, `check_limits.py`, `gen_claim_checklist.py`, `contribution_matrix.py`, `fig6_*` (paper 2 gate; `fig6_score.py` reads the wrong path, OQ F3), `reader_e_*`, `stats_review*_recompute.py`, `render_pdf.py`, `age_sex_by_source.py`, `fig_claim.py`, `fig_power.py`) | the figure, table, packet, compile and check scripts of paper 1 | by clone |
| `SchwingNet/slurm/` (101 scripts: `compile.sh` (texlive 2020, xelatex + biber, flock; `CAMERAREADY=1`), `contrib_*`, `coverage_arms_*`, `lcurve_*`, `name_fill_*` (`name_fill_prep.sh` L27 removes shared inputs), `film_ncurve_*`, `fig6_*`, `reader_e_*`, `rare_*`, `rc_*`, `g3_split.sh`, `tables_check.sh`) | the grid builds and the arrays behind the results | by clone |
| `Makefile` | nnU-Net stages, `make physics`, `make physics-tables` (the only safe physics target today), polypose checks | by clone |
| `.gitattributes` | `SchwingNet/results/fig6/frozen/**` and `verification/**` are `-text` (byte-exact frozen truth files) | by clone |
| `service/` (6 files), `tools/deploy_service.py` | the container and its release script | `code/service/`, `code/deploy_service.py` |
| `docs/MODEL_REGISTRY.md` | registry design, commands, environment, the sixteen backfilled models | homed in `../10_data_platform_grid/docs/`; by clone |
| `docs/devices/` (cards `cios_fusion`, `elekta_xvi`, `bv_pulsera`, `pixium_4600` as `.json` + `.frames.csv`; `census/` with three header censuses in the S3 format; `eval_gate/`) | the device cards and the census format | homed in `../08_render_devices/results/devices/`; by clone |
| `docs/BENCHMARK_PROTOCOL.md` (rule 3: paired bootstrap before any "improves") | the benchmark rules S7 cites | homed in `../03_ctspinopelvic1k_dataset/docs/`; by clone |
| `paper/qi_universal_protocol/{main.tex,main.pdf,build.sh}` | the QI protocol manuscript (per-case form = the S5 / S8 scaffold); its affiliation line reads Neurosurgery (wrong); bibliography is `paper/rsnai/refs.bib` | homed in `../09_wrong_level_clinical_qi/manuscripts/`; by clone |
| `docs/INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md`, `PATENT_PACKAGE.md`, `provisional/`, `disclosure_*`, `research_patent_2026-09-18.json`, `research_registration_free_2026-09-18.json` | Greg's private filing material: referenced, never copied into a project folder | by clone (Greg only) |
| `docs/CREDENTIALS_SETUP.md` | credential locations: excluded from every project folder (`../_plan/EXCLUDED.md`) | by clone (Greg only) |
| `HANDOFF/GREG_ONLY/` | `PRIVATE_STATE.md`, `context/` (the unredacted notes), `context_beethoven/`: never copied | by clone (Greg only) |
| `data_platform/{DATA_MANIFEST,MIGRATION_PLAN,LAYOUT}.md`, `plan/batch_items/*.tsv`, `dedup/` | the migration record behind `MANIFEST_GRID.md` | homed in `../10_data_platform_grid/`; by clone |
| `tmp/` (653 tracked scratch files, 40 MB: `coupling_check/` job outputs, `lcurve_local_census.py`, `lcurve_probe*.sh`) | scratch kept under version control | by clone |

## 2. OpenSpineConsortium/spine-detector (private)

- URL: `https://github.com/OpenSpineConsortium/spine-detector` (private; recorded in `memory/xray-corner-detector-status.md`).
  Branch and commit: **not recorded**; the laptop folder is not a clone (no `.git`), the live tree with `.git` is
  `/wsu/home/go/go24/go2432/spine-detector` (`.git` dated 2026-09-12).
- Files that matter: `src/manifest.py::canonical_slots` (the corner slot order a runtime must respect),
  `src/normalize.py::detect_facing` (code and docstring disagree), `src/converters/{buu,mendeley,nhanes}.py`,
  `src/build_dataset.py`, `src/export_onnx.py`, `src/export_yolo.py`, `src/train.py`, `src/evaluate.py`, `src/run_eval.py`,
  `src/render_prediction.py`, `src/check_fp16_*.py`, `tests/test_manifest.py`. Copied as
  `code/spine_detector_src_snapshot/` (commit unknown; the manifest field that names where an image came from was renamed `lineage` in the copy,
  consistently across its seven files, because of the standing word rule; the repository keeps the original name).
- `dist/{detect_v3_640_fp32,detect_v4_1024_fp32,v11m_1024_v4_fp16,v11m_640_v4_fp16}.onnx` (84, 84, 42, 42 MB, 2026-09-12):
  superseded ONNX exports of detect_v3 / v4; the commit they came from is unknown; not copied (weights, over 25 MB).
- Weights of record: `runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt`, `runs/realxray/rx_pooled_1024/weights/best.pt`,
  `runs/devcorpus/dc_P_pooled/weights/best.pt`, `runs/pose/runs/detect_v2/weights/best.pt` (`MANIFEST_GRID.md`).

## 3. gregoryschwingmdphd/level-id-weights (private Hugging Face model repository)

- The off-cluster weight mirror and the service's weight source: `detector.pt` = `detect_v5z_epoch25`, `level_model.pt` =
  M19 `films_all2` rung 1, `recurrent_head.pt`, `registry.json`; `registry/<name>/<sha>` mirror. Written by
  `code/deploy_service.py`, which hashes the weights, refuses a public repository and reads the token from a file
  (`~/.hf_org_token` as `$HF_ORG_TOKEN`; the token value is never written anywhere in this project).
- Live state on 2026-10-08: **not checked** (no network). Both Hugging Face accounts returned 402 for hosting on
  2026-09-14 (`docs/handoff/context/level-service-serving.md`). S2 replaces its contents with the reported stack.

## 4. openspineconsortium.github.io (public)

- URL: `https://github.com/OpenSpineConsortium/openspineconsortium.github.io.git`. Branch `master`. Commit
  `c1800f81d3b0364d489721f55ca9313d61809e26` (2026-10-02).
- `pacs/remote.js`: the client of the service contract (`SERVICE_DEFAULT https://level-id.openspineconsortium.org`, not
  live on 2026-09-14). The website never serves weights (`memory/level-service-serving.md`). Project 12 owns it.

## 5. CTSpinoPelvic1K (public)

- URL: `https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K` (`origin`) and the OpenSpineConsortium copy (`osc`);
  push to both. Branch `master`. Commit `7ddfe38734e9e3ee4fc2c690ddbc970ffc4ef19f` (2026-09-28); working tree modified.
- What this project takes from it: `CLAUDE.md` (the label-scheme, identifier 29, `zfill(4)` and reorientation rules
  restated in this folder's `CLAUDE.md`), `proposals/FluoroCap_HPR_attachment.md` (copied), `proposals/irb/` and
  `IRB_ADDENDUM.md` (gitignored; copied with redactions), `COMMERCIALIZATION.md` (Greg-only: the two-track rule; never in a
  project folder), `Student_Projects/BOARD.md` (the "schwingnet" board task: convert hand-typed table cells to `\RESULT{}`).
- The v11 release (L1 = 20 ... L5 = 24, sacrum 26, hips 30/31, femurs 32/33; identifier 29 retired) is the CT truth of
  any CTSpinoPelvic1K render in the level bank.

## 6. OpenSpineToolkit (public)

- URL: `https://github.com/OpenSpineConsortium/OpenSpineToolkit` (branch `main`, not `master`). Commit
  `cb431979cbe5fee38ead4ecdfcd4811efc263a4e` (2026-09-25).
- `ostk.labels.labels_for(volume)`: the only way to resolve a label name (two schemes exist). The canal-closing
  regression at 1b7005c (`memory/`: see `docs/handoff/context/ostk-canal-closing-regression.md`) is project 04's.

## 7. XRSpinoPelvic1K (private)

- Private repository `XRSpinoPelvic1K`, URL `https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K` (the clone's
  `origin` remote, read 2026-10-08), branch `main`, commit `4f22935826dacd4b7ab8ad757c5363f0480b6093` (2026-08-15).
  The DRR bank of the plain-film line (project 07); `dataset2024.zip` (4.0 GB) is never copied. Named here because the
  films corpus of the corner detector and the film N-curve enter the v9 bank.

## 8. Other code homes named in this folder

- `../09_wrong_level_clinical_qi/`: the QI protocol manuscript and the iliac-crest paper.
- `../02_transitional_naming_truth/`: `LEVELCHECK_MODEL.md` (frozen comparator; never edit), `paper2_levelcheck/`,
  `results/fig6`, `results/learning`, `results/auto_reference`, `results/rare_class`, `results/dual_loss`.
- `../08_render_devices/`: `docs/devices/`, `results/manifold`, `results/polypose`, the formation documents.
- `../10_data_platform_grid/`: `docs/MODEL_REGISTRY.md`, the migration plan, the 2026-10-08 grid listing.
- `../11_students_grid_access/`: Beethoven (how students reach the grid) and its two private repositories,
  `https://github.com/OpenSpineConsortium/beethoven` (branch `main`, commit 2f90319, 2026-10-03) and
  `https://github.com/OpenSpineConsortium/beethoven-vscode` (branch `main`, commit 8d7fc65, 2026-10-02), as recorded on
  2026-10-08 in `../11_students_grid_access/MANIFEST_CODE.md` section 1, which lists the files that matter.
