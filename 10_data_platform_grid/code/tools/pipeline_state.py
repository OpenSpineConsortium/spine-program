# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/pipeline_state.py. working tree, uncommitted edit on 2026-10-08. The repository is the executable source; this copy is a record.
"""Where every stage of this pipeline actually stands, computed from the filesystem and the queue.

WHY THIS IS COMPUTED AND NOT WRITTEN DOWN. On 16 September 2026 the best-performing model in this project was
found to have fallen out of the pipeline months earlier because a script opened a file by a hard-coded name that
no longer existed. Nobody noticed, because the only record of what was running was prose. The same night, a
result was attributed to the wrong crop bank in three places, including a comment written that same hour. A
status file maintained by hand records what somebody believed; this one records what is on disk.

So every stage below declares a PREDICATE -- the artefact whose existence means the stage finished -- and the
status is the answer to that predicate plus a look at the scheduler. A stage is:

    done      its artefact exists
    running   a job carrying its name is in the queue
    ready     its dependencies are done and nothing is running
    blocked   a dependency is not done
    failed    a job ran and exited, and the artefact is still absent

HOW TO USE THIS AFTER A BREAK, whether you are a person or another model:

    ssh go2432@grid.wayne.edu
    ~/mambaforge/envs/spineps/bin/python ~/spinesurg-ct-nnunet/tools/pipeline_state.py

It prints the table, writes ~/model_night/PIPELINE_STATE.md and the machine-readable json beside it, and lists
the exact command for every stage that is ready to run. Nothing here submits a job or changes a file; deciding
what to run next is the reader's job, and this only removes the guesswork about what is already done.

WHEN YOU ADD A STAGE, add it here. A stage that exists only in a shell history is a stage that will be lost.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

H = os.path.expanduser("~")


def P(*parts):
    return str(Path(H).joinpath(*parts))


RS = "/rs/rs_grp_oschome/go2432"      # the CephFS volume: large outputs live here, not under the home directory


def R(*parts):
    return "/".join((RS,) + parts)


# the cine tracker's constants (docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md 1b): an INPUT, committed in the repository and
# read from the grid clone, so its predicate is `committed:` rather than existence
TRACKER_CONFIG = str(Path(H, "spinesurg-ct-nnunet", "SchwingNet", "results", "cine", "tracker_config.json"))
# the synthetic cine's sequence directory: tools/polypose/cine_render.py seq_name(case, region, frac), the name
# slurm/polypose_cine.sh submit decides and slurm/cine_eval.sh (DATASET=synth) reads through SYNTH_DIR. frac 1.0 is its
# own directory (..._f100) and becomes its own stages when it is run, after the frac 0.5 frames are looked at.
SYNTH_SEQ = "verse823_lumbar_fe_f050"
SYNTH_NHO = "demo on a VerSe CT; VerSe renders are in v9 training"


# Each stage: what it does, why it matters, the artefact that proves it finished, what it needs first, the job
# name the scheduler would show, and the command that runs it.
STAGES = [
    # ---------------------------------------------------------------- the acquisition loop
    dict(id="guided_calibrate", group="guided", needs=[],
         what="Measure the correlation margin a CORRECT link achieves, and set tau from it",
         why="tau is the margin above which a link is believed. Choosing it by hand and then reporting "
             "accuracy at that choice fits the threshold to the test. It is measured instead, from links "
             "whose shared bodies are known to have been paired right, and everything downstream runs at "
             "the fifth percentile of that.",
         done_if=[P("model_night", "guided", "calib", "guided_calibration.json")],
         job="guided",
         run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/guided_validate.sh"),
    dict(id="guided_validate", group="guided", needs=["guided_calibrate"],
         what="Close the loop: the engine commands each exposure, an operator executes it badly, and the "
              "run is scored against a fixed protocol of the same length on identical query frames",
         why="sweep_map measures naming once a run exists and says nothing about how it came to exist -- "
             "its stations are cut at fixed steps from the anatomy, as though the radiographer had been "
             "given the answer in advance. Five arms: upright, the image turned up to 25 degrees, an "
             "operator missing by a quarter, and the operative level two and eight vertebrae off the "
             "anchor. Resubmitting skips whichever arms are already on disk.",
         done_if=["glob:5:" + P("model_night", "guided", "*", "guided.json")],
         job="guided",
         run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/guided_validate.sh"),
    # ---------------------------------------------------------------- published methods, rebuilt and ranked
    dict(id="competitor_train", group="benchmark", needs=[],
         what="Re-implement the published registration-free paradigms and train them on the newest bank",
         why="Every method in this space reports its own metric on its own cohort and none releases weights, "
             "so the comparison table is indicative until each one is rebuilt from its stated architecture "
             "and scored by one function on one held-out set.",
         done_if=["glob:3:" + P("model_night", "competitors", "*_val.npz")],
         job="compens",
         run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/competitor_ensemble.sh"),
    dict(id="ensemble_eval", group="benchmark", needs=["competitor_train"],
         what="Ask whether any COMBINATION of those methods beats the best single one, with and without the map",
         why="Consensus across methods that fail differently is the obvious route to a number the detector "
             "cannot reach alone. It is also the easiest place to fool yourself, so the combination is "
             "chosen on one half of the films and reported on the other.",
         done_if=[P("model_night", "ensemble", "ensemble.json")],
         job="compens",
         run="runs at the end of slurm/competitor_ensemble.sh"),
    # ---------------------------------------------------------------- source data and labels
    dict(id="aasce_convert", group="data", needs=[],
         what="Convert the AASCE radiographs to the render format",
         why="457 real anterior-posterior films, T1-L5. The only public collection with labelled mid-thoracic "
             "vertebrae on real film.",
         done_if=["glob:400:" + P("aasce_drr", "ann", "*.json")],
         run="python tools/aasce_to_drr.py --src ~/spine-detector/data/raw/aasce --dst ~/aasce_drr"),
    dict(id="aasce_crops", group="data", needs=["aasce_convert"],
         what="Cut AASCE into context crops",
         why="A render directory is not training data until it is a crop bank.",
         done_if=[P("aasce_fov96_ctx", "rung_1.npz")],
         job="aasce_crops",
         run="sbatch -D ~ ~/slurm/aasce_crops.sh"),
    dict(id="mendeley_crops", group="data", needs=[],
         what="Cut the Mendeley lateral films into context crops",
         why="584 films were converted and labelled and then never folded into any bank. A pure oversight and "
             "the cheapest gap to close.",
         done_if=[P("mendeley_fov96_ctx", "rung_1.npz")],
         job="corpus_expand",
         run="part of slurm/corpus_expand.sh"),
    dict(id="pseudo_gate", group="data", needs=[],
         what="Score the pseudo-labeller against the 543 human-annotated NHANES films",
         why="The gate on whether a hard name may be ASSERTED. It does not decide which films to keep; every "
             "film is kept at some supervision tier.",
         done_if=[P("model_night", "expand", "validate", "pseudolabel_report.json")],
         job="corpus_expand",
         run="sbatch -D ~ ~/slurm/corpus_expand.sh"),
    dict(id="nhanes_pseudo", group="data", needs=["pseudo_gate"],
         what="Label the 16,530 unannotated NHANES films",
         why="The largest unused real-radiograph holding in the project.",
         done_if=[P("nhanes_pseudo", "pseudolabel_report.json"),
                  "glob:5000:" + P("nhanes_pseudo", "ann", "*.json")],
         job="corpus_expand",
         run="part of slurm/corpus_expand.sh"),
    dict(id="vindr_pseudo", group="data", needs=["pseudo_gate"],
         what="Label the 9,722 unused VinDr-SpineXR films",
         why="VinDr annotates lesions, not levels, so its films were unusable until the template decoder.",
         done_if=[P("vindr_pseudo", "pseudolabel_report.json"),
                  "glob:2000:" + P("vindr_pseudo", "ann", "*.json")],
         job="corpus_expand",
         run="part of slurm/corpus_expand.sh"),
    dict(id="lat236_pseudo", group="data", needs=["pseudo_gate"],
         what="Label the 236 IEEE whole-spine laterals",
         why="The only real collection imaging the entire thoracic spine, and it ships no annotation.",
         done_if=[P("lateral236_pseudo", "pseudolabel_report.json"),
                  "glob:100:" + P("lateral236_pseudo", "ann", "*.json")],
         job="corpus_expand",
         run="part of slurm/corpus_expand.sh"),
    dict(id="bank_v3", group="data", needs=[],
         what="Merge the oblique renders and VinDr into allspine_v3",
         why="Both were on disk and in no bank; the merge also fixed a split leak of 9,194 crops.",
         done_if=[P("allspine_v3_fov96_ctx", "rung_1.npz")],
         job="allspine_v3", run="sbatch -D ~ ~/slurm/build_allspine_v3.sh"),
    dict(id="bank_v4", group="data", needs=["bank_v3", "aasce_crops"],
         what="Add AASCE to make allspine_v4",
         why="Kept separate from v3 because the AASCE level naming rests on a published convention that an "
             "independent model check could not confirm.",
         done_if=[P("allspine_v4_fov96_ctx", "rung_1.npz")],
         job="allspine_v4", run="sbatch -D ~ ~/slurm/build_allspine_v4.sh"),
    dict(id="bank_v5", group="data", needs=["nhanes_pseudo", "vindr_pseudo", "mendeley_crops"],
         what="Build allspine_v5 with every pseudo-labelled real radiograph",
         why="The corpus the final model should train on.",
         done_if=[P("allspine_v5_fov96_ctx", "rung_1.npz")],
         job="corpus_expand", run="part of slurm/corpus_expand.sh"),
    dict(id="hires_refetch", group="data", needs=[],
         what="Refetch publisher originals for the low-resolution literature panels",
         why="Panel vertebrae are 49 px against 162-212 px on real film, and 81% are magnified to reach the "
             "target. Resolution is the one measured deficit of that corpus.",
         done_if=[P("model_night", "hires", "hires_report.json")],
         job="hires_paired", run="see the overnight-push workflow track 1"),

    # ---------------------------------------------------------------- models
    dict(id="arms_v2", group="model", needs=[],
         what="The nine single-crop arms on allspine_v2",
         why="The control set. r18_ce reproduces the historical baseline to the digit.",
         done_if=[P("model_night", "runs", "model_r18_ce.pt")],
         job="n_r18_ce", run="sbatch via slurm/night_arm.sh with ARCH/LOSS/NAME set"),
    dict(id="head_v2", group="model", needs=["arms_v2"],
         what="The recurrent run-level head on allspine_v2",
         why="Worth +10.2 points over single crop on the 27-class whole spine, and real-film accuracy of "
             "99.75% at a band of nine. It was unreachable for months.",
         done_if=[P("model_night", "heads", "allspine_v2", "head_k3.pt")],
         job="rec_v2",
         run="BANK=~/allspine_v2_fov96_ctx MODEL=~/model_night/runs/model_r18_ce.pt RUNG=1 TAG=allspine_v2 "
             "sbatch -D ~ --export=ALL,BANK,MODEL,RUNG,TAG ~/slurm/recurrent_head.sh"),
    dict(id="head_mixed", group="model", needs=["arms_v2"],
         what="One head trained on every band length, plus the random-window test",
         why="Tests whether the 99.75% real-film number is anatomy or the head memorising each collection's "
             "stereotyped level span. A large drop on random windows means the latter.",
         done_if=["glob:1:" + P("model_night", "heads_mixed", "mixed_*.json")],
         job="hm_mixed", run="MODE=mixed sbatch -D ~ --export=ALL,MODE ~/slurm/head_mixed.sh"),
    dict(id="stc_arms", group="model", needs=["arms_v2"],
         what="Star Temporal Classification against two cross-entropy controls",
         why="Trains on incomplete names without inventing the rest, which is what a transitional vertebra and "
             "a caption-derived label both need. The control to beat is 50.4% on transitional anatomy at 87.2% "
             "on ordinary spines.",
         done_if=["glob:4:" + P("model_night", "stc", "stc_*.json")],
         job="stc_rand50", run="see slurm/stc_arm.sh; four withholding regimes"),
    dict(id="arms_v5", group="model", needs=["bank_v5"],
         what="Retrain on the fully expanded corpus",
         why="The point of the expansion.",
         done_if=[P("model_night", "runs", "model_r18_ce_v5.pt")],
         job="r18_ce_v5",
         run="BANK=~/allspine_v5_fov96_ctx ARCH=resnet18 LOSS=ce FREEZE=0 NAME=r18_ce_v5 EPOCHS=40 BS=64 "
             "MAXH=15 sbatch --export=ALL,BANK,ARCH,LOSS,FREEZE,NAME,EPOCHS,BS,MAXH ~/spinesurg-ct-nnunet/slurm/night_arm.sh"),

    # ---------------------------------------------------------------- evaluation
    dict(id="eval_rawfilms", group="eval", needs=["arms_v2"],
         what="Every arm on one held-out set, split into real film and render",
         why="Bank-native validation numbers are not comparable across banks, because the merged splits are "
             "harder. This is the only admissible ranking.",
         done_if=["glob:6:" + P("model_night", "rawfilms", "rawfilms_*.json")],
         job="arms_realfilm", run="sbatch -D ~ ~/slurm/all_arms_real_films.sh"),
    dict(id="eval_head_transitional", group="eval", needs=["head_v2"],
         what="Transitional strata with the head on and off",
         why="Whole-spine accuracy can rise while T13 and L6 stay broken. They are at 0.0% and 47.7%.",
         done_if=["glob:2:" + P("model_night", "transitional_head", "transitional_eval_*.json")],
         job="trans_head", run="sbatch -D ~ ~/slurm/transitional_with_head.sh"),
    dict(id="eval_flags", group="eval", needs=["arms_v2"],
         what="Operating points for the rule flags against known transitional cases",
         why="The scoping review's sharpest finding is that imaging-step countermeasures are never evaluated. "
             "A flag without a measured operating point joins that list.",
         done_if=[P("model_night", "flags", "flags_r18_ce_v2.json")],
         run="python tools/eval_level_flags.py --drr ~/ctsp_drr ~/verse_drr ~/physics_rare "
             "--model ~/model_night/runs/model_r18_ce.pt --bank ~/allspine_v2_fov96_ctx --tag r18_ce_v2"),
    dict(id="panel_diagnosis", group="eval", needs=[],
         what="Why the literature panels score 19.7% against 95.1% on real film",
         why="Answered: native resolution and domain, not crop quality, and not mostly label noise.",
         done_if=[P("model_night", "panel_stats", "panel_vs_film_stats.json")],
         run="python tools/panel_vs_film_stats.py; panel_label_audit.py; panel_contamination_audit.py; "
             "panel_region_arbitration.py"),
    dict(id="seed_sweep", group="eval", needs=["arms_v2"],
         what="Multi-seed spread of the run-level head",
         why="Published evidence that in-distribution accuracy does not predict length behaviour: ten "
             "identically trained runs spanned ~100% to near zero out of distribution.",
         done_if=["glob:1:" + P("model_night", "seed_sweep", "*.json")],
         job="t5_seeds", run="see the overnight-push workflow track 5"),

    dict(id="stc_penalty_sweep", group="model", needs=["stc_arms"],
         what="Sweep the wildcard penalty before declaring the star loss dead",
         why="At a penalty of 0.5 the star loss LOST everywhere: 77.4% against 87.2% for cross-entropy at 50% "
             "of names withheld, 44.6% at 70%, and it HALVED transitional accuracy, 39.6% to 22.9%. That is the "
             "predicted failure, the wildcard explaining everything. A stronger penalty is the one remaining "
             "test; if it also fails, the method does not transfer to runs where every position carries a name.",
         done_if=["glob:3:" + P("model_night", "stc", "stc_stc_trans_pen*.json")],
         job="stc_pen2",
         run="CTX=~/allspine_v2_fov96_ctx MODEL=~/model_night/runs/model_r18_ce.pt K=3 DROP=0 "
             "WITHHOLD=transitional SEED=0 TAG=stc_trans_pen5 STARPEN=5 EPOCHS=30 "
             "sbatch -D ~ --export=ALL,CTX,MODEL,K,DROP,WITHHOLD,SEED,TAG,STARPEN,EPOCHS ~/slurm/stc_arm.sh"),
    dict(id="head_seeds", group="model", needs=["head_mixed"],
         what="Three seeds of the mixed-length head",
         why="Published evidence warned that in-distribution accuracy predicts nothing about length behaviour. "
             "It does not reproduce here: three seeds agree to within 0.36 points, so the caveat is retired and "
             "single-seed head numbers stand.",
         done_if=["glob:3:" + P("model_night", "heads_mixed", "mixed_*mixed_kmax4_seed*.json")],
         job="hm_mixed_s1",
         run="MODE=mixed SEED=1 sbatch -D ~ --export=ALL,MODE,SEED ~/slurm/head_mixed.sh"),
    dict(id="v5_train_eval", group="model", needs=["bank_v5"],
         what="Train on the expanded corpus, add the mixed-length head, re-score every arm on one held-out set",
         why="Each bank grading its own validation split is not a comparison; the merged splits are harder, so "
             "v3 and v4 looked worse while being at least as good. This scores everything on allspine_v2, which "
             "every later bank inherited.",
         done_if=[P("model_night", "runs", "model_r18_ce_v5.pt")],
         job="v5_train_eval", run="sbatch -D ~ --dependency=afterany:<expand job> ~/slurm/v5_train_eval.sh"),
    dict(id="corpus_levels", group="doc", needs=["bank_v5"],
         what="Per-level counts across the expanded corpus, split by how each label was obtained",
         why="Once human, converted, CT-projected and pseudo labels are mixed, a single per-level count means "
             "nothing. The share of each level that rests on a model's own output is what decides whether a "
             "gain from the expansion is learning or a self-confirming loop.",
         done_if=[P("model_night", "CORPUS_LEVELS.md")],
         job="v5_train_eval", run="python tools/corpus_level_report.py --banks ~/allspine_v5_fov96_ctx"),

    dict(id="anchor_free", group="eval", needs=["head_mixed"],
         what="Accuracy on windows that contain no landmark at all",
         why="A feasibility analysis calls this case mathematically underdetermined. Measured: 98.32% on "
             "28,547 unanchored vertebrae, against 100% with the sacrum in frame. The literature asserts the "
             "ill-posedness and never quantifies it, so this is the number nobody has published.",
         done_if=["glob:1:" + P("model_night", "anchor_free", "*_head.json")],
         job="anchor_free", run="sbatch -D ~ ~/slurm/anchor_free.sh"),
    dict(id="surgeon_benefit", group="eval", needs=["arms_v2"],
         what="Would the alert help a surgeon who counts from a landmark, or disturb one already right",
         why="The endpoint a trial would use. Counting from a landmark is excellent on ordinary spines and "
             "fails uniformly on an extra presacral segment; the two-by-two of caught, missed and disturbed is "
             "what a claim of clinical benefit rests on. VERIDAH reports anomaly recall with no false-positive "
             "rate anywhere in its text, so there is no published operating point to compare against.",
         done_if=["glob:1:" + P("model_night", "surgeon_benefit", "*.json")],
         job="surgeon_benefit", run="sbatch -D ~ ~/slurm/surgeon_benefit.sh"),
    dict(id="anomaly_manifest", group="data", needs=[],
         what="Every anomalous spine we hold, in three tiers by how far the label can be trusted",
         why="The anomaly counts were being read off one cohort of 802 abdominopelvic CTs, which cannot see "
             "the upper ribs and gave a both-cell of two. Across all sources there are 749 anomalous spines "
             "and 66 anomalous at both ends. This stage also emits spine_classes.json, which is the four-class "
             "label the separability and global-signature runs read; if it is stale, both of them are wrong.",
         done_if=[P("model_night", "anomaly_manifest", "spine_classes.json"),
                  P("model_night", "anomaly_manifest", "anomaly_manifest.csv")],
         job=None,
         run="~/mambaforge/envs/spineps/bin/python -P ~/spinesurg-ct-nnunet/tools/anomaly_manifest.py"),
    dict(id="geometric_indices", group="eval", needs=[],
         what="The feasibility report's own recommended detectors, scored on real film with real ground truth",
         why="BUU-LSPINE ships four-corner keypoints, S1 end-plate corners and the authors' own L4/L6 reads, so "
             "the Wigh index, sacral slope and L5-S1 gap can be tested with no detector of ours in the loop. "
             "The report's normal-L5 band covers 5.1% of ordinary real films; sacral slope is the only index "
             "that separates six-lumbar spines (AUC 0.73); the L5-S1 gap separates four-lumbar at 0.99.",
         done_if=[P("model_night", "geometric_indices", "geometric_indices_buu.json")],
         job=None,
         run="~/mambaforge/envs/spineps/bin/python -P ~/spinesurg-ct-nnunet/tools/geometric_indices_buu.py"),
    dict(id="source_quality", group="data", needs=[],
         what="Every bank source with its label origin and crop quality",
         why="A per-source accuracy is meaningless without knowing whether its labels were human, carried from "
             "CT, inferred by counting, or our own decoder's output. 45.8% from CT, 30.0% pseudo, 14.1% human, "
             "10.2% counting.",
         done_if=[P("model_night", "source_quality", "source_quality.json")],
         job=None,
         run="~/mambaforge/envs/spineps/bin/python -P ~/spinesurg-ct-nnunet/tools/source_quality_report.py"),
    dict(id="feasibility_claims", group="eval", needs=["anomaly_manifest"],
         what="The feasibility report's claims C1-C5, each with a number, on anomalous AND ordinary spines",
         why="The earlier 98.32% pooled anomalous and ordinary spines, which hides the case the report is about. "
             "Two bank/encoder/head pairings; a mismatched pairing scores 0-1% with a +2 offset and was discarded.",
         done_if=[P("model_night", "feasibility_claims", "v2_ce", "feasibility_claims.json"),
                  P("model_night", "feasibility_claims", "v5_ce", "feasibility_claims.json")],
         job="feas_claims", run="sbatch -D ~ ~/slurm/feas_claims.sh"),
    dict(id="repro_feasibility", group="deliverable",
         needs=["anomaly_manifest", "geometric_indices", "source_quality", "global_signature",
                "fov_separability", "feasibility_claims", "anchor_free"],
         what="One job that recomputes every manuscript number from raw inputs and writes a hashed ledger",
         why="Reviewer reproducibility: docs/FEASIBILITY_REPRODUCE.md names every input and the number each "
             "stage owns; LEDGER.tsv carries input and output sha256 per stage.",
         done_if=[P("model_night", "repro_feasibility", "LEDGER.tsv")],
         job="repro_feas", run="sbatch -D ~ ~/slurm/reproduce_feasibility.sh"),
    dict(id="interior_windows", group="eval", needs=["anomaly_manifest"],
         what="Naming on windows whose PIXELS contain no anchor, film-clustered CIs, structural baselines",
         why="The label-defined State C pooled whole-stack and end-touching windows whose crops show the "
             "unlabelled sacrum or C2. Interior only: ordinary lumbar 91.8% [89.4, 94.1], anomalous 66.0% "
             "[39.6, 87.2] on 12 films (v2). These supersede the 98.32% and the 87.2%.",
         done_if=[P("model_night", "interior_windows", "v2_ce", "interior_windows.json")],
         job="interior", run="sbatch -D ~ ~/slurm/interior_windows.sh"),
    dict(id="buu_correct", group="data", needs=[],
         what="Promote BUU's S1a line to L6 on six-lumbar studies; flag L5 sacralised on four-lumbar; review package",
         why="BUU's keypoints are a rigid five-slot template; annotators counted down, so the sixth body is the "
             "'S1a' line. 15 promoted with fit residual <= 1 px, 129 flagged, 0 refused. All 144 test_eligible.",
         done_if=[P("films_drr_buucorr", "CORRECTION_SUMMARY.json")], job=None,
         run="~/mambaforge/envs/spineps/bin/python -P ~/spinesurg-ct-nnunet/tools/correct_buu_schema.py"),
    dict(id="data_fixes", group="data", needs=[],
         what="Film-match measurement, anchored-only pseudolabel filter, film-matched render bank (v2fm)",
         why="Pseudolabels made without an anchor in the decode taught the model the ordinary prior; renders "
             "sit outside the real films' noise band. Both get a number and a fixed bank.",
         done_if=[P("model_night", "film_match", "film_match_measure.json"), P("pseudo_filtered", "FILTER_SUMMARY.json"),
                  P("allspine_v2fm_fov96_ctx", "READY")],
         job="data_fixes", run="sbatch -D ~ ~/slurm/data_fixes.sh"),
    dict(id="scaling_sweep", group="train", needs=[],
         what="Accuracy against synthetic fraction and real fraction, six short-recipe encoders, interior evaluator",
         why="Whether synthetic data is doing anything is a curve. Points 0/0.25/0.5/1.0 synthetic at full real; "
             "0.25/0.5 real at full synthetic.",
         done_if=[P("model_night", "scaling", "SCALING_CURVE.json")], job="scaling", run="sbatch -D ~ ~/slurm/scaling_sweep.sh"),
    dict(id="v6_chain", group="train", needs=["anomaly_manifest"],
         what="v6: no anomalous BUU film in training, anomalous CT renders x4; CE + CORN encoders, heads, claims",
         why="124 of 144 anomalous BUU films were trained on under counted names; v6 makes all 144 the test set.",
         done_if=["glob:1:" + P("model_night", "feasibility_claims", "v6_*", "feasibility_claims.json")],
         job="v6_chain", run="sbatch -D ~ ~/slurm/v6_chain.sh"),
    dict(id="film_lora", group="train", needs=[],
         what="Film-look SDXL LoRA trained on the public digitised X-ray datasets only (no FluoroCap)",
         why="The report's domain objections -- scatter, noise, exposure, superimposition -- as a learned "
             "filter for DRRs; images only, no vertebra names; equal weight per (dataset, region) cell.",
         done_if=[P("fluorogen", "lora_film_v1", "pytorch_lora_weights.safetensors")],
         job="film_lora", run="sbatch -D ~ ~/slurm/train_film_lora.sh"),
    dict(id="leads", group="train", needs=["data_fixes", "scaling_sweep"],
         what="Test the verified literature leads: film-noise randomisation (40 ep), synthetic pretrain -> real "
              "fine-tune, anchored-only vs CReST pseudolabel admission; one interior-evaluator table",
         why="SyntheX, RoentGen-v2 and CReST are measured elsewhere; here they are measured on our films "
             "against the v2 baseline, not cited.",
         done_if=[P("model_night", "leads", "LEADS_TABLE.json")], job="leads", run="sbatch -D ~ ~/slurm/leads_chain.sh"),
    dict(id="windows_by_class", group="eval", needs=["anomaly_manifest"],
         what="Exact naming along the spine x window length x spine class (ordinary / LS / TL / both), interior and all",
         why="The computer-science question in one figure: capability across anomaly classes and fields of view, "
             "with placement-blind and placement-aware priors beside every cell.",
         done_if=[P("model_night", "windows_by_class", "v2_ce", "windows_by_class.json")],
         job="leads", run="sbatch -D ~ ~/slurm/leads_chain.sh  (stage D)"),
    dict(id="benchmark_cina", group="eval", needs=["anomaly_manifest"],
         what="Every pairing, and every external method with predictions, under Cina 2021's task definition on the same public films",
         why="A citation is not a benchmark. Per-vertebra correct-name ratio on whole lumbar lateral films, "
             "sacrum-anchored counting floor, external slot for reimplemented or released models "
             "(Cina, VertXNet, Kim 2024, Konya 2021), ordinary and anomalous apart, plus the interior windows a "
             "whole-film method cannot enter.",
         done_if=["glob:1:" + P("model_night", "benchmark_cina", "*", "benchmark_cina.json")],
         job="bench_cina", run="sbatch -D ~ ~/slurm/benchmark_cina.sh"),
    dict(id="sweep_map", group="eval", needs=["anomaly_manifest", "buu_correct"],
         what="The serial sweep: overlapping frames linked into one chain, and limited-field frames named against it",
         why="A limited field cannot see a landmark; a series of limited fields can. This is the registration "
             "built from radiographs instead of from a preoperative CT, and it is where the anomalous number "
             "stops being a coin toss. Fifteen arms vary the frame span, the overlap, the box source, the "
             "encoder, the anchor end and the image domain.",
         done_if=["glob:8:" + P("model_night", "sweep2", "*", "sweep.json")],
         job="sweepfin", run="sbatch -D ~ ~/slurm/sweep_final.sh"),
    dict(id="sweep_overlap", group="eval", needs=["sweep_map"],
         what="The overlap knob at the real C-arm field, and the detector-box arms",
         why="Overlap between exposures is the only free lever measured: half a body names two-vertebra "
             "frames at 86.6%, one body 93.6%, two 95.1%, three 95.2%, four 93.2%. Two is the optimum and it "
             "is a protocol instruction, not a model change.",
         done_if=["glob:4:" + P("model_night", "sweep2", "ctsp_ii9_o*_gt", "sweep.json")],
         job="sweepovl", run="sbatch -D ~ ~/slurm/sweep_overlap.sh"),
    dict(id="sweep_protocol", group="eval", needs=["sweep_map"],
         what="The protocol as written -- sacrum at the bottom of frame 1, then a FIXED move of one field "
              "minus two bodies -- scored against the current best, and the render-trained anchor detector's "
              "boxes consumed for the first time",
         why="Every published arm jittered the step by 0.3 body. Two questions: does the fixed step the "
             "radiographer is told to make reproduce sweep_holdout_v2/ctsp_ii9_o2_gt (120 held-out spines, "
             "chain 97.5%, 93.8/95.4/95.6 at 2/3/4)? And does anchor_det_v1 (trained on renders) hold the "
             "chain where the film detector collapsed to 0% -- which was the tool reading keypoints from a "
             "detection model, not the detector? The detector arms run on the 8 spines held out from BOTH "
             "the namer and the detector, and are reported as eight. o2_gt_jit is the control: it re-runs "
             "the reference under the edited tool and must match v2 to the third decimal, or the edit moved "
             "something and nothing else counts.",
         done_if=["glob:5:" + P("model_night", "sweep_protocol", "*", "sweep.json")],
         job="sweepproto", run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/sweep_protocol.sh"),
    dict(id="sweep_improve", group="eval", needs=["sweep_protocol"],
         what="Three linker/placement improvements -- a global solve over consecutive and skip links, a "
              "phase-correlation seed, ECC refinement of the query placement -- each alone and together, "
              "against the fixed-step protocol baseline",
         why="Chain completeness falls from 98% at two bodies of overlap to 82% at four because every extra "
             "frame is another pairwise link that can be wrong. A global solve lets a skip link outvote a bad "
             "consecutive one, and clustering in the common frame is the one change that can merge a detector "
             "box duplicated across frames. Skip links do not exist at two bodies of overlap on a four-body "
             "field, so g_o2 must equal the control; the claim lives at o3 and o4. ctl_o2 must match "
             "sweep_protocol/o2_gt_fixed to the third decimal or the defaults moved.",
         done_if=["glob:13:" + P("model_night", "sweep_improve", "*", "sweep.json")],
         job="sweepimp", run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/sweep_improve.sh"),
    dict(id="sweep_fix", group="eval", needs=["sweep_improve"],
         what="Three fixes found on the 25 held-out real films: a detector box on a real vertebra the "
              "annotation does not cover is 'unlabelled', not a false positive; chain nodes are placed by "
              "panorama position and merged when they coincide; --hybrid local compares the count and the "
              "variant alphabet only on the bodies they name differently",
         why="films_ii9_o2_det completed 10/25 chains against 25/25 with true boxes, and 12 of the 15 breaks "
             "were a real T12/T11 above the L1-first NHANES labels, named correctly and scored as a false "
             "positive. One film had a whole frame's boxes prepended above the chain (4 duplicates), one had "
             "a correct count overruled by the L6 alphabet. ctl_o2_fixed must equal "
             "sweep_protocol/o2_gt_fixed to the third decimal: true boxes have nothing for any fix to touch.",
         done_if=["glob:11:" + P("model_night", "sweep_fix", "*", "sweep.json")],
         job="sweepfix", run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/sweep_fix.sh"),
    dict(id="ts_drr", group="data", needs=[],
         what="TotalSegmentator v2.0.1 (1228 clinical CTs under ~/data/TotalSegmentator) rendered to lateral "
              "DRRs with per-vertebra boxes -> ~/ts_drr, the ann/img layout every sweep tool reads",
         why="Not one TS id is in the encoder's training bank, so it is a held-out render bench ten times "
             "the current one, with whole-body studies for sacrum-to-C2 sweeps. Ordinary-spine truth only "
             "(no L6/T13 class); v2.0.1 label mix-ups are caught as stack gaps and skipped; redo from v3 "
             "(~/data/TotalSegmentator_v3, download in progress) when it lands.",
         done_if=["glob:1000:" + P("ts_drr", "ann", "*.json")],
         job="tsdrr", run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/ts_drr.sh"),
    dict(id="sweep_v3", group="eval", needs=["sweep_fix", "ts_drr"],
         what="Every CT-render sweep arm (holdout ladder, protocol, improvements, fixes) re-run on renders "
              "whose row spacing is right, plus the first TS-bench arms",
         why="make_drr_dataset wrote the A-P voxel size as the S-I row spacing. VerSe anns said 0.29 mm/px "
             "on 1.25 mm slices (74 of 374 spines off by >1.2x, 31 by >2x) so the 140 mm C2 sweep was two "
             "whole-spine frames; CTSP was off 7.5% at the median and >1.2x on 172 of 801. Every number "
             "in sweep_holdout_v2 / sweep_protocol / sweep_improve / sweep_fix on renders is therefore on "
             "the wrong field size and is superseded by sweep_v3. Films carry no header spacing and are "
             "unaffected. make_results_table reads sweep_v3.",
         done_if=["glob:45:" + P("model_night", "sweep_v3", "*", "*", "sweep.json")],
         job="sweepv3", run="sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/sweep_v3.sh"),
    dict(id="sweep_answers", group="eval", needs=["sweep_overlap"],
         what="The two analyses the result is quoted from: accuracy at a stated coverage, and per vertebra "
              "per spine class",
         why="Every other table averages over window length or collection, which hides the only question a "
             "surgeon asks. These two produce the numbers the manuscript, the README and the page all read "
             "from, so none of them can drift from the records.",
         done_if=[P("model_night", "sweep2", "COVERAGE.json"), P("model_night", "sweep2", "PER_LEVEL.json")],
         run="python tools/sweep_coverage.py --sweep ~/model_night/sweep2 && "
             "python tools/sweep_per_level.py --sweep ~/model_night/sweep2 --arms ctsp_ii9_o2_gt verse_ii9_o1_gt"),
    dict(id="role_head", group="eval", needs=["anomaly_manifest"],
         what="The transition-role head, and the sweep arms that use it",
         why="Refuted and kept: the head reaches 89.5% balanced and 99-100% on 'last presacral body', and "
             "adding it to the alphabet score changed the sweep by nothing at three weights. Recorded so it "
             "is not tried again without a reason to expect a different answer.",
         done_if=[P("model_night", "roles", "role_head_v3.pt")],
         job="rolehead", run="sbatch -D ~ ~/slurm/role_head.sh"),
    dict(id="push99", group="eval", needs=["anomaly_manifest", "v6_chain"],
         what="Logit-adjusted training for the rare alphabet classes, and paired AP + lateral fusion",
         why="Two remedies for the anomalous number that are not the sweep: change the decision rule rather "
             "than the sample weights (Menon 2021), and use the second film the radiographer already took. "
             "Three pooling rules are scored because the arithmetic mean is not obviously right when one view "
             "is much weaker than the other.",
         done_if=["glob:1:" + P("model_night", "push99", "*", "interior_windows.json"),
                  "glob:1:" + P("model_night", "push99", "*", "multiview.json")],
         job="push99", run="sbatch -D ~ ~/slurm/push99_chain.sh"),
    dict(id="review_pack", group="deliverable", needs=["nhanes_pseudo"],
         what="Pack the pseudolabelled films students review, and deploy the private review Space",
         why="Thirty percent of bank v5 was named by a decoder and never read; the component ablation shows "
             "that is what costs anomalous accuracy. The review task is one name per film, because the "
             "decoder's error mode is an offset and not a permutation.",
         done_if=[P("review_pack", "manifest.json")],
         job="revpack", run="sbatch -D ~ ~/slurm/review_pack.sh"),
    dict(id="product_select", group="deliverable", needs=["v6_chain"],
         what="Rank every encoder by twin-free ordinary interior accuracy; model cards; private checkpoint publishing",
         why="Most spines are ordinary; the deployment checkpoint is the one that scores best on them with its "
             "weaknesses stated from numbers. Cards and uploads by tools/publish_checkpoints.py, private repo only.",
         done_if=[P("model_night", "product", "PRODUCT_RANKING.json")], job="product", run="sbatch -D ~ ~/slurm/product_select.sh"),
    dict(id="v5c", group="train", needs=["anomaly_manifest"],
         what="v5 rebuilt with NHANES films grouped by number across sources; every v5 result recomputed",
         why="The paper's v5 is this bank from the moment it finishes.",
         done_if=[P("model_night", "feasibility_claims", "v5c_ce", "feasibility_claims.json")], job="v5c_chain", run="sbatch -D ~ ~/slurm/v5c_chain.sh"),
    dict(id="v5_ablation", group="train", needs=["v5c"],
         what="v5 minus pseudolabels / obliques / extras, one short recipe, interior evaluator: which addition costs the anomalous spines",
         why="The mechanism is quantified (decoder-named crops are 29.5% of lumbar training) and then tested by removal.",
         done_if=[P("model_night", "v5_ablation", "V5_ABLATION_TABLE.json")], job="v5_ablate", run="sbatch -D ~ ~/slurm/v5_ablation.sh"),
    dict(id="explain", group="eval", needs=[],
         what="Region-occlusion ablation, Grad-CAM, embedding geometry, prototypes, morphometric probes",
         why="Which local morphology carries level identity, as a per-level accuracy drop per masked region.",
         done_if=[P("model_night", "explain", "explain.json")], job="explain", run="sbatch -D ~ ~/slurm/explain.sh"),
    dict(id="anomaly_cooc", group="eval", needs=[],
         what="Recount both border anomalies from the label voxels and test co-occurrence",
         why="The manifest gave an odds ratio of 4.0 with an interval touching 1 on a both-cell of two, and "
             "its thoracolumbar fields are not present in the first fifty records. A project note already "
             "records a manifest T13 flag that said 18 when the truth was 6.",
         done_if=[P("model_night", "anomaly_cooccurrence_labels.json")],
         job="anomaly_cooc", run="sbatch -D ~ ~/slurm/anomaly_cooc.sh"),
    dict(id="global_signature", group="eval", needs=["arms_v2"],
         what="Does a vertebra far from both junctions know its spine is anomalous",
         why="If border anomalies are one global alteration rather than two local accidents, a limited field "
             "carries information a counting surgeon structurally cannot reach. Only the within-source rows "
             "count: the rare-case renders were built FROM anomalous spines.",
         done_if=[P("model_night", "global_signature", "global_signature.json")],
         job="global_sig", run="sbatch -D ~ ~/slurm/global_signature.sh"),
    dict(id="fov_separability", group="eval", needs=["anomaly_cooc"],
         what="Field of view against separability of the four spine classes, and the threshold",
         why="The publishable object is a curve, not a number: at what field of view do ordinary, "
             "lumbosacral-only, thoracolumbar-only and both become separable from vertebrae that are not the "
             "anomaly. Feature dimension is held constant across window size so the curve measures information "
             "rather than capacity.",
         done_if=[P("model_night", "fov_separability", "fov_separability.json")],
         job="fov_sep", run="sbatch -D ~ --dependency=afterany:<recount> ~/slurm/fov_separability.sh"),
    dict(id="disk_cleanup", group="data", needs=[],
         what="Bring the home directory back under the 4 TB quota",
         why="Usage reached 113.59%. Freed about 1.2 TB, almost all of it regenerable nnU-Net preprocessed "
             "tensors, with every deletion and its reason logged.",
         done_if=[P("model_night", "logs", "disk_cleanup_manifest.txt")],
         job="disk_cleanup", run="sbatch -D ~ ~/slurm/disk_cleanup.sh"),

    # ---------------------------------------------------------------- cine: per-frame naming and tracking on sequences
    # docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md. Three sequence sources scored by one harness (tools/cine_eval.py):
    # Bournemouth cervical quantitative fluoroscopy, the C-ArmLSpine CBCT projection sweeps (case134, case39), and a
    # synthetic lumbar flexion-extension cine of a whole-spine VerSe CT (verse823; the source changed from CTSP 0533 on
    # 2026-09-26, and it is NOT held out). LAYOUT these predicates read, which the new scripts must write:
    #   * every result set is R(data/or_ready/cine/<dataset>/<arm>/): the level_prototype output in its pred/
    #     (pred/<sequence>/ when sharded by sequence), and beside pred/ cine_eval's track.json and score.json.
    #   * <arm> is never a wildcard. The arm the plan pre-specifies as primary writes `primary/`, and only `primary/`
    #     satisfies these stages: with a wildcard, a primary and an ROI arm each half done (126 + 126 of 252
    #     sequences) read as 252 done. A secondary arm (Bournemouth ROI 2x, the 26 R sequences flipped, a fold model,
    #     the unstyled synthetic render) writes its own <arm>/ -- and its own frame directory, never the images/ that
    #     a frame predicate counts -- and becomes its own stage when its command is fixed.
    #   * one scheduler name per stage, given with sbatch -J (several stages submit the same script): main() reports a
    #     stage running when its job name is queued, before it looks at what the stage needs, so a shared name shows
    #     every stage that carries it as running.
    #   * scoring runs track, then score --track <track.json>, then video: plan 1b computes the temporal metrics
    #     (identity switches, fragmentation, MOTA/IDF1, name stability) only when score is given the track. Every
    #     frame row of score.json carries its corpus `hint`, which is what eval_gate.scored_items keys a re-carried
    #     score by (tools/carmlspine_eval.py does the same).
    #   * level_prototype gates a frame on its path alone, so every frame stem must key (tools/patient_keys.py):
    #     Bournemouth <event>_<motion>_f#### under realxray/bournemouth_qf*/, sweep case<N>_sw### under
    #     realxray/carmlspine_sweep*/, and the synthetic frames cine_<region>_f<frac>_<case>_lat_p<frame> (the verse
    #     rule -> verse:<case>, a person in v9 training, so that run is DECLARED not held out). A bare f###.png keys
    #     to nobody and the run raises UnkeyedEvalItem.
    dict(id="cine_tracker_frozen", group="cine", needs=[],
         what="The online tracker's constants, committed in tracker_config.json and frozen",
         why="Plan 1b: every tracker constant (association gate, EMA, logp memory, birth/death) is fixed -- tuned, if "
             "at all, on the synthetic cine only -- before any Bournemouth frame is seen, and each score.json records "
             "the file's sha256. Done when the file is tracked in the grid clone and identical to HEAD: a copy edited "
             "in place after the commit is not the one the record says was frozen.",
         done_if=["committed:" + TRACKER_CONFIG],
         run="write the plan 1b 'track' constants to SchwingNet/results/cine/tracker_config.json, commit, push (via "
             "WSL), then git pull in ~/spinesurg-ct-nnunet on the grid"),
    dict(id="bournemouth_qf_export", group="cine", needs=[],
         what="Bournemouth Cervical_Database.mat -> one truth json per template frame in the cine schema",
         why="252 flexion/extension sequences of 63 people (126 events, a and b of each person keyed as one by "
             "tools/patient_keys.py) with four corners per level per frame from the authors' template tracker. The "
             "truth exists before the images do, so the metric code is tested on it now (cine_eval self-test).",
         done_if=[R("data", "realxray", "bournemouth_qf", "summary.json"),
                  R("data", "realxray", "bournemouth_qf", "splits.json")],
         job="bqf_export",
         run="~/mambaforge/envs/spineps/bin/python ~/spinesurg-ct-nnunet/tools/bournemouth_qf_eval.py export "
             "--mat /rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf/raw/Cervical_Database.mat "
             "--out /rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf  (through sbatch -J bqf_export, not on the "
             "login node)"),
    dict(id="bournemouth_qf_frames", group="cine", needs=["bournemouth_qf_export", "cine_tracker_frozen"],
         what="The Bournemouth DICOM cine -> 8-bit PNG per frame, windowed per sequence, polarity decided once",
         why="Nothing can be inferred until the images exist, and they are not in hand: this stage is the wait on "
             "the data request (docs/BOURNEMOUTH_DATA_REQUEST_DRAFT_2026-09-26.md). Done when every one of the "
             "252 sequences has its first frame, f0000. It waits on cine_tracker_frozen because this is where "
             "Bournemouth frames first exist, and the tracker is fixed before any is seen.",
         done_if=["glob:252:" + R("data", "realxray", "bournemouth_qf", "images", "*_f0000.png")],
         job="bqf_frames",
         run="when the DICOM arrives: ~/mambaforge/envs/fluorogen/bin/python ~/spinesurg-ct-nnunet/tools/"
             "bournemouth_qf_eval.py frames --dicom <dir> --root /rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf"
             "  (through sbatch -J bqf_frames)"),
    dict(id="cine_infer_bournemouth", group="cine", needs=["bournemouth_qf_frames"],
         what="The zero-shot v9 stack (level_prototype --dump-corners) on every Bournemouth frame, one shard per sequence",
         why="No cervical fluoroscopy frame has ever been scored. The run is gated: the frames key to bournemouth "
             "patients, so the verdict proves no model saw them rather than being told so with --not-held-out. The "
             "primary arm only (full frame, imgsz 1024, as shipped); the ROI 2x arm is its own <arm>/.",
         done_if=["glob:252:" + R("data", "or_ready", "cine", "bournemouth_qf", "primary", "pred", "*",
                                  "prototype_results.json")],
         job="cine_infer_bqf",
         run="sbatch -D ~/logs -J cine_infer_bqf --array=<sequences> ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (plan "
             "section 2, 'Run command': --no-orient --flag --dump-posterior --dump-corners --conf 0.35, the three v9 "
             "weights, --out .../or_ready/cine/bournemouth_qf/primary/pred/<sequence>)"),
    dict(id="cine_score_bournemouth", group="cine", needs=["cine_infer_bournemouth", "cine_tracker_frozen"],
         what="Track, score (--corpus-hint bournemouth --bins machine_angle) and render the Bournemouth cine",
         why="Agreement with a validated semi-automatic tracker, per level, per frame and over time (identity "
             "switches, fragmentation, name stability) -- not accuracy against independent hand labels.",
         done_if=[R("data", "or_ready", "cine", "bournemouth_qf", "primary", "score.json"),
                  R("data", "or_ready", "cine", "bournemouth_qf", "primary", "track.json")],
         job="cine_score_bqf",
         run="sbatch -D ~/logs -J cine_score_bqf ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (CPU: tools/cine_eval.py "
             "track with the committed tracker_config.json, then score --track <track.json> --corpus-hint bournemouth "
             "--bins machine_angle, then video --fps 15)"),
    dict(id="carm_sweep_case39_pose", group="cine", needs=[],
         what="Register a pose for every one of case39's 301 CBCT projection-sweep frames",
         why="case39 carries agreed level names, which case134 does not, so it is the only real C-arm sweep whose "
             "naming can be scored. Truth boxes are projected through these poses.",
         done_if=["glob:301:" + R("data", "carmlspine", "sweep_case39", "pose", "*.json")],
         job="c39_pose",
         run="sbatch -D ~/logs -J c39_pose --array=0-3 ~/spinesurg-ct-nnunet/slurm/carm_sweep_case39.sh  "
             "(carm_sweep.py pose --case case39 --shard $SLURM_ARRAY_TASK_ID --n-shards 4 --skip-done "
             "--bounds 40,40,80,10)"),
    dict(id="carm_sweep_case39_orbit", group="cine", needs=["carm_sweep_case39_pose"],
         what="Fit one rigid orbit to case39's registered poses and write the orbit-smoothed poses",
         why="The second truth version: per-frame registration jitters by about 0.7 degree frame to frame, and a "
             "frame where the two truth boxes disagree (IoU < 0.8) is flagged rather than trusted.",
         done_if=["glob:301:" + R("data", "carmlspine", "sweep_case39", "pose_smooth", "*.json")],
         job="c39_orbit",
         run="python tools/carm_sweep.py orbit --case case39  (through sbatch -J c39_orbit)"),
    dict(id="carm_sweep_case39_export", group="cine", needs=["carm_sweep_case39_orbit"],
         what="case39 sweep frames and projected SPINEPS truth -> realxray/carmlspine_sweep_case39",
         why="Trusted only after `carm_sweep.py export --case case134` into a scratch directory reproduces the "
             "existing case134 metas, boxes and poses identical.",
         done_if=[R("data", "realxray", "carmlspine_sweep_case39", "summary.json"),
                  "glob:301:" + R("data", "realxray", "carmlspine_sweep_case39", "meta", "*.json")],
         job="c39_export",
         run="python tools/carm_sweep.py export --case case39  (through sbatch -J c39_export)"),
    dict(id="cine_infer_case39", group="cine", needs=["carm_sweep_case39_export"],
         what="level_prototype --dump-corners over the 301 case39 sweep frames",
         why="Naming across the whole swing from lateral to AP. Zero-shot naming of C-ArmLSpine spot frames was "
             "96.4% lateral and 43.7% AP, so the sweep is expected to fall toward AP and is reported by angle bin. "
             "Primary arm: the zero-shot v9 stack; the fold model that held case39 out is its own <arm>/.",
         done_if=["glob:1:" + R("data", "or_ready", "cine", "carm_sweep", "case39", "primary", "pred",
                                "prototype_results.json")],
         job="cine_infer_c39",
         run="sbatch -D ~/logs -J cine_infer_c39 ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (plan section 3, "
             "'Inference and scoring'; --out .../or_ready/cine/carm_sweep/case39/primary/pred)"),
    dict(id="cine_score_case39", group="cine", needs=["cine_infer_case39"],
         what="Track, score and render case39 by angle bin",
         why="The only sweep with level truth: detection, naming and tracking in the same run.",
         done_if=[R("data", "or_ready", "cine", "carm_sweep", "case39", "primary", "score.json"),
                  R("data", "or_ready", "cine", "carm_sweep", "case39", "primary", "track.json")],
         job="cine_score_c39",
         run="sbatch -D ~/logs -J cine_score_c39 ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (CPU: tools/cine_eval.py "
             "track, then score --track <track.json> --corpus-hint carmlspine "
             "--bins lat_signed_deg:-130,-105,-75,-15,15,60, then video --fps 10)"),
    dict(id="cine_infer_case134", group="cine", needs=[],
         what="level_prototype --dump-corners over the 301 case134 sweep frames (the existing export)",
         why="The existing case134 sweep score (or_ready/arc/case134_sweep/) predates the evaluation gate, so it is "
             "re-run under it. Its frames (case134_sw###) key only through tools/patient_keys.py's carmlspine_sweep "
             "row (2026-09-26): a grid clone older than that raises UnkeyedEvalItem at the gate.",
         done_if=["glob:1:" + R("data", "or_ready", "cine", "carm_sweep", "case134", "primary", "pred",
                                "prototype_results.json")],
         job="cine_infer_c134",
         run="git -C ~/spinesurg-ct-nnunet pull (the carmlspine_sweep keying row), then sbatch -D ~/logs "
             "-J cine_infer_c134 ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (plan section 3, 'Inference and scoring'; "
             "--out .../or_ready/cine/carm_sweep/case134/primary/pred)"),
    dict(id="cine_score_case134", group="cine", needs=["cine_infer_case134"],
         what="Detection and tracking on case134 (no level truth: detection, IoU, identity switches, name stability)",
         why="VERIDAH read C1-C5 on this lumbar case and the retry was never merged, so naming accuracy cannot be "
             "scored here; name stability needs no naming truth and can, which is why the track comes first.",
         done_if=[R("data", "or_ready", "cine", "carm_sweep", "case134", "primary", "score.json"),
                  R("data", "or_ready", "cine", "carm_sweep", "case134", "primary", "track.json")],
         job="cine_score_c134",
         run="sbatch -D ~/logs -J cine_score_c134 ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (CPU: tools/cine_eval.py "
             "track, then score --track <track.json> --corpus-hint carmlspine "
             "--bins lat_signed_deg:-130,-105,-75,-15,15,60, then video --fps 10)"),
    # The synthetic cine: tools/polypose/cine_render.py on VerSe verse823 (Greg, 2026-09-26: not CTSpinoPelvic1K), all
    # four of its stages queued by ONE command, `slurm/polypose_cine.sh submit`, chained afterany; each by hand runs
    # with its own -J name (the script's header). NOT HELD OUT: every VerSe CT is inside the v9 training renders.
    dict(id="polypose_cine_plan", group="cine", needs=[],
         what="The 60-frame flexion-extension plan for VerSe verse823, lumbar region, frac 0.5: per-frame segment "
              "angles and rigid transforms, the label-map record, the re-keyed SPINEPS body mask, end-plate corners",
         why="Segments T10-T11 .. L4-L5 move with L5 fixed (verse823 has no sacrum label, so L5-S1 cannot move), caps "
             "from SchwingNet/results/polypose/rom_cine.json, whose rows are copies of sampling_spec.json rom_deg: "
             "-18.7 degrees flexion and +13.7 extension summed over the moving segments at frac 0.5. Run at 0.5 first "
             "and look. ostk detects a VerSe mask as the legacy scheme; the plan records that and uses the one map the "
             "anatomy puts in order. NOT HELD OUT: " + SYNTH_NHO + ".",
         done_if=[R("data", "polypose", "cine", SYNTH_SEQ, "frames.json")],
         job="pp_cine_plan",
         run="bash ~/spinesurg-ct-nnunet/slurm/polypose_cine.sh submit --region lumbar --case verse823 --frac 0.5  "
             "(login node, sbatch only: queues pp_cine_plan -> pp_cine_warp -> pp_cine_rgt -> pp_cine_check with "
             "afterany and writes the job ids to " + R("data", "polypose", "cine", SYNTH_SEQ + ".jobs.txt") + ")"),
    dict(id="polypose_cine_warp", group="cine", needs=["polypose_cine_plan"],
         what="Warp CT, label and body mask of verse823 into each of the 60 poses (PolyPose, GPU)",
         why="PolyPose has never run end to end to a rendered frame; verify_equivalence on frame 15 (the largest "
             "flexion) and the geometric invariants in checks/f###.json are its first test. A frame is skipped only "
             "when its checks carry the current plan's frame_key, so a re-plan re-warps every frame.",
         done_if=["glob:60:" + R("data", "polypose", "cine", SYNTH_SEQ, "volumes", "f*_ct.nii.gz"),
                  "glob:60:" + R("data", "polypose", "cine", SYNTH_SEQ, "volumes", "f*_label.nii.gz"),
                  "glob:60:" + R("data", "polypose", "cine", SYNTH_SEQ, "volumes", "f*_body_msk.nii.gz")],
         job="pp_cine_warp",
         run="queued by polypose_cine_plan's submit (array 0-59%8 on galhp,gvohp,gmsap --qos=gpu). One frame by hand: "
             "sbatch -D ~/spinesurg-ct-nnunet -J pp_cine_warp -q gpu -p galhp,gvohp,gmsap --gres=gpu:1 "
             "--cpus-per-task=8 --mem=120G --array=<k> slurm/polypose_cine.sh warp --region lumbar --case verse823 "
             "--frac 0.5"),
    # render and gt are ONE stage because the plan runs them as one array job (plan section 4, 'Jobs'): two stages
    # would either share a scheduler name or wait on a submission that never happens
    dict(id="polypose_cine_render_gt", group="cine", needs=["polypose_cine_warp"],
         what="Ray-cast and style each warped frame at one fixed lateral pose, frozen noise, and project its truth: "
              "body boxes and end-plate corners, with the exact cross-check",
         why="The one cine whose truth is exact by construction; the pose and isocentre are fixed from frame 0 so "
             "that only the spine moves. Boxes from the warped mask must agree with source voxels moved by the "
             "frame's transform (IoU >= 0.95); that is checked, not assumed. A level clipped by the frame border is "
             "box-only (no off-image corner is truth).",
         done_if=["glob:60:" + R("data", "polypose", "cine", SYNTH_SEQ, "images", "*.png"),
                  "glob:60:" + R("data", "polypose", "cine", SYNTH_SEQ, "meta", "*.json")],
         job="pp_cine_rgt",
         run="queued by polypose_cine_plan's submit (frame 0 alone first, it fixes the pose and exposure; then 1-59, "
             "reqp --qos=requeue). By hand: sbatch -D ~/spinesurg-ct-nnunet -J pp_cine_rgt -p reqp -q requeue "
             "--cpus-per-task=4 --mem=32G --array=0 slurm/polypose_cine.sh rgt --region lumbar --case verse823 "
             "--frac 0.5, then the same with --array=1-59"),
    dict(id="polypose_cine_check", group="cine", needs=["polypose_cine_render_gt"],
         what="The synthetic cine's contact sheet (frames 0, 15, 30, 45 with truth drawn) and qc/check.json",
         why="LOOK AT THE SHEET BEFORE SCORING ANYTHING (plan section 4). Done means the check ran: read `ok` and "
             "`problems` in check.json -- a failed invariant, a truth cross-check below 0.95, volumes warped for "
             "another plan or a missing frame all land there, and the job exits non-zero.",
         done_if=[R("data", "polypose", "cine", SYNTH_SEQ, "qc", "check.json"),
                  R("data", "polypose", "cine", SYNTH_SEQ, "qc", "contact_sheet.png")],
         job="pp_cine_check",
         run="queued by polypose_cine_plan's submit. By hand: sbatch -D ~/spinesurg-ct-nnunet -J pp_cine_check -p reqp "
             "-q requeue --cpus-per-task=2 --mem=16G slurm/polypose_cine.sh check --region lumbar --case verse823 "
             "--frac 0.5"),
    dict(id="cine_infer_synth", group="cine", needs=["polypose_cine_check"],
         what="level_prototype --dump-corners over the 60 synthetic flexion-extension frames of verse823",
         why="DECLARED NOT HELD OUT (" + SYNTH_NHO + "): the frames key to verse:verse823 through their stems "
             "(cine_lumbar_f050_verse823_lat_p###), a person in v9 training, and the run carries --not-held-out "
             "(slurm/cine_eval.sh's SYNTH_NHO default). A harness and tracker demonstration against exact truth, "
             "never a held-out result. After the contact sheet is looked at.",
         done_if=["glob:1:" + R("data", "or_ready", "cine", "synth_fe", SYNTH_SEQ, "primary", "pred",
                                "prototype_results.json")],
         job="cine_infer_synth",
         run="sbatch -D ~/logs -J cine_infer_synth --partition=gmsap,gvohp,galhp --qos=gpu --gres=gpu:1 "
             "--cpus-per-task=8 --mem=96G --export=ALL,SYNTH_DIR=" + R("data", "polypose", "cine", SYNTH_SEQ)
             + " ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (--out .../or_ready/cine/synth_fe/" + SYNTH_SEQ
             + "/primary/pred)"),
    dict(id="cine_score_synth", group="cine", needs=["cine_infer_synth"],
         what="Track, score and render the synthetic cine against exact truth",
         why="Where the tracker constants are tuned if they must be; they are then committed and frozen "
             "(cine_tracker_frozen) before any Bournemouth frame is seen. Not held out, declared (" + SYNTH_NHO + ").",
         done_if=[R("data", "or_ready", "cine", "synth_fe", SYNTH_SEQ, "primary", "score.json"),
                  R("data", "or_ready", "cine", "synth_fe", SYNTH_SEQ, "primary", "track.json")],
         job="cine_score_synth",
         run="sbatch -D ~/logs -J cine_score_synth --export=ALL,SYNTH_DIR=" + R("data", "polypose", "cine", SYNTH_SEQ)
             + " ~/spinesurg-ct-nnunet/slurm/cine_eval.sh  (CPU: tools/cine_eval.py track, then score --track "
             "<track.json> --corpus-hint verse --not-held-out ..., then video --fps 15)"),

    # ---------------------------------------------------------------- deliverables
    dict(id="dataset_usage", group="doc", needs=[],
         what="Which X-ray datasets reach a bank and why the rest do not",
         why="Regenerates rather than going stale. Counts come from the banks' own case arrays.",
         done_if=[P("model_night", "XRAY_DATASET_USAGE.md")],
         run="python tools/xray_dataset_usage.py"),
    dict(id="student_pack", group="doc", needs=[],
         what="The worklist, renderings and guide for students to correct fluoroscopy labels",
         why="No literature panel has ever been read by a human. Until some are, nobody can say whether the "
             "19.7% is the model failing or the labels being wrong.",
         done_if=["glob:1:" + P("FluoroCap", "student_pack", "*.csv")],
         run="see the overnight-push workflow track 3"),
    dict(id="morning_brief", group="doc", needs=[],
         what="The overnight brief",
         why="One place to start reading.",
         done_if=[str(Path(H, "spinesurg-ct-nnunet", "docs", "MORNING_BRIEF_2026-09-16.md"))],
         run="written by the overnight-push workflow"),
]


def satisfied(pred: str) -> bool:
    """Is this stage's artefact really there?

    A bare path is an existence test. "glob:<n>:<pattern>" requires at least n matching files, which is what a
    stage that writes many outputs needs: the directory appears the moment the job starts, so testing the
    directory would report a stage as finished while it is still running. That is the exact class of false
    record this file exists to prevent, so the weaker test is not available by accident.

    "committed:<path>" is for a file that must be FROZEN, not merely present (a configuration fixed before the data
    it is applied to is seen): it holds only when the file is tracked by git in its clone and identical to HEAD. A
    copy edited in place after the commit, or never committed, is not the one the record says was frozen.
    """
    if pred.startswith("glob:"):
        _, n, pattern = pred.split(":", 2)
        import glob as _g
        return len(_g.glob(pattern)) >= int(n)
    if pred.startswith("committed:"):
        p = Path(os.path.expanduser(pred.split(":", 1)[1]))
        if not p.is_file():
            return False
        try:
            tracked = subprocess.run(["git", "-C", str(p.parent), "ls-files", "--error-unmatch", "--", p.name],
                                     capture_output=True, text=True, timeout=60)
            dirty = subprocess.run(["git", "-C", str(p.parent), "status", "--porcelain", "--", p.name],
                                   capture_output=True, text=True, timeout=60)
        except Exception:  # noqa: BLE001  (no git: nothing shows it frozen)
            return False
        return tracked.returncode == 0 and dirty.returncode == 0 and not dirty.stdout.strip()
    return Path(pred).exists()


def squeue_names():
    try:
        out = subprocess.run(["squeue", "-u", os.environ.get("USER", "go2432"), "-h", "-o", "%j|%T|%i"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:  # noqa: BLE001
        return {}
    d = {}
    for line in out.strip().splitlines():
        parts = line.split("|")
        if len(parts) >= 3:
            d.setdefault(parts[0].strip(), []).append((parts[1].strip(), parts[2].strip()))
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=P("model_night", "PIPELINE_STATE.md"))
    a = ap.parse_args()
    running = squeue_names()

    st = {}
    for s in STAGES:
        done = all(satisfied(p) for p in s["done_if"])
        jobs = running.get(s.get("job", "\x00"), [])
        st[s["id"]] = {"done": done, "running": bool(jobs), "jobs": jobs}

    for s in STAGES:
        e = st[s["id"]]
        if e["done"]:
            e["status"] = "done"
        elif e["running"]:
            e["status"] = "running"
        elif any(not st[n]["done"] for n in s["needs"]):
            e["status"] = "blocked"
        else:
            e["status"] = "ready"

    order = {"running": 0, "ready": 1, "blocked": 2, "done": 3}
    L = ["# Pipeline state\n",
         "Computed by `tools/pipeline_state.py` from the filesystem and the scheduler. Nothing here is",
         "maintained by hand, because a hand-maintained record is how this project lost its best model.\n",
         "Run it again at any time:\n",
         "```", "ssh go2432@grid.wayne.edu",
         "~/mambaforge/envs/spineps/bin/python ~/spinesurg-ct-nnunet/tools/pipeline_state.py", "```\n",
         "| stage | status | group | what | proof it finished |",
         "|---|---|---|---|---|"]
    for s in sorted(STAGES, key=lambda x: (order[st[x["id"]]["status"]], x["group"], x["id"])):
        e = st[s["id"]]
        mark = {"done": "done", "running": "RUNNING", "ready": "READY", "blocked": "blocked"}[e["status"]]
        if e["jobs"]:
            mark += " (" + ", ".join(f"{t} {i}" for t, i in e["jobs"][:2]) + ")"
        proof = (s["done_if"][0].split(":")[-1].split("/")[-1] if s["done_if"] else "-")
        L.append(f"| `{s['id']}` | {mark} | {s['group']} | {s['what']} | `{proof}` |")

    L.append("\n## Ready to run now\n")
    ready = [s for s in STAGES if st[s["id"]]["status"] == "ready"]
    if not ready:
        L.append("Nothing is ready: every remaining stage is either running or waiting on one that is.\n")
    for s in ready:
        L.append(f"**`{s['id']}`** -- {s['what']}\n")
        L.append(f"> {s['why']}\n")
        L.append("```\n" + s["run"] + "\n```\n")

    L.append("## Blocked, and on what\n")
    for s in STAGES:
        if st[s["id"]]["status"] == "blocked":
            miss = [n for n in s["needs"] if not st[n]["done"]]
            L.append(f"- `{s['id']}` waits on " + ", ".join(f"`{m}`" for m in miss))

    L.append("\n## Why each stage exists\n")
    for s in STAGES:
        L.append(f"- **`{s['id']}`** ({st[s['id']]['status']}): {s['why']}")

    txt = "\n".join(L) + "\n"
    out = Path(os.path.expanduser(a.out))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(txt, encoding="utf-8")
    json.dump({"stages": [{**{k: v for k, v in s.items() if k != "done_if"},
                           "done_if": s["done_if"], **st[s["id"]]} for s in STAGES]},
              open(str(out).replace(".md", ".json"), "w"), indent=1)

    w = {k: sum(1 for s in STAGES if st[s["id"]]["status"] == k) for k in order}
    print(f"{w['done']} done, {w['running']} running, {w['ready']} ready, {w['blocked']} blocked\n")
    print(f"{'stage':<24} {'status':<22} {'what'}")
    for s in sorted(STAGES, key=lambda x: (order[st[x["id"]]["status"]], x["id"])):
        e = st[s["id"]]
        j = (" " + ",".join(i for _, i in e["jobs"][:2])) if e["jobs"] else ""
        print(f"{s['id']:<24} {e['status'] + j:<22} {s['what'][:60]}")
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
