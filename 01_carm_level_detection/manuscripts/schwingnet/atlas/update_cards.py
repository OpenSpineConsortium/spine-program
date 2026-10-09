"""Bring SchwingNet/atlas/{model,dataset}.json to the SchwingNet manuscript (five figures and three tables since the evening
of 2026-09-24, when the LevelCheck / surgeon comparison moved to paper 2: PAPER1_SCOPE.md, paper2_levelcheck/). Idempotent;
run from anywhere:

    python SchwingNet/atlas/update_cards.py && python SchwingNet/atlas/validate_cards.py

Written 2026-09-23 (as update_cards_2026-09-23.py); brought to 2026-09-24 and made idempotent (the reference list
used to gain one CTSpinoPelvic1K entry per run: six copies had accumulated; validate_cards.py now fails on a
duplicate reference). 2026-09-24 adds: the three pre-unblinding amendments of LEVELCHECK_MODEL.md (sections 12-14,
including the automated reference standard), the checkpoint-lineage findings of results/eval_gate/EVALUATORS.md
(plain-film naming is on the encoder's selection split; the sacrum detector descends from a render-trained detector
and was selected on its training devices' test splits; the 17 styled-corpus subjects are a selection set), the planned
ImageNet initialisation of the split-trained arm (then "the Figure 6 arm"; paper 2's since the evening), the bibliographic corrections of REFS_AUDIT.md for COBRA2026 and Grupp
2020, and a release statement that leaves the weights decision open (packet_src/statements.md).

Every JSON-backed number is read here from its result file. Three kinds are quoted as text instead, each with its
source named in the card: the coupling row (COUPLED below, from the markdown results/COUPLING.md rows det74/kfull,
the same numbers numbers.json checks against main.tex), the counts of the traced tables (tables/tab_corpus.md,
tables/tab4_transitional.md), and the device and model facts of docs/MODEL_CARD.md and the grid args.yaml."""
import io
import json
from pathlib import Path

TODAY = "2026-09-24"
# LEVELCHECK_MODEL.md commits (git log -- SchwingNet/LEVELCHECK_MODEL.md, read 2026-09-24): frozen at ecae75f,
# amended before unblinding at 1897772 (+ efab8dd, time wording), 2993f40 and b511985.
LC_FROZEN = ("the LevelCheck model frozen from the literature at commit ecae75f and amended before unblinding, by its "
             "own rule, at 1897772 (secondary mechanism test, transitional flag, dual-loss arm), 2993f40 (accuracy when "
             "the network accepts a frame, always beside coverage) and b511985 (an automated reference standard whose "
             "consensus rule is chosen on human-read CT and frozen before testing); no comparator value, stratum, "
             "endpoint, test or primary hypothesis changed")
RELEASE = ("Not released. Code, fitted device parameters and weights are in a private repository (branch L6_Class), "
           "available to reviewers and editors on request. What is deposited at publication, and under what terms, is "
           "the author's open decision (packet_src/statements.md: a public deposit for research use, or the comparator "
           "file, result files and device parameters deposited with code and weights under a research agreement). Any "
           "weight licence is bounded from below by the training sources: CC BY-NC 4.0, CC BY-NC-SA 4.0 and CC BY-NC-ND "
           "releases and VinDr-SpineXR under the PhysioNet Restricted Health Data Use Agreement, so no less restrictive "
           "than non-commercial.")
SELECTION = ("The plain-film naming figures of the level bank (CSXA, BUU-LSPINE, NHANES II) were scored on the split that "
             "selected the encoder's checkpoint and are not quoted as held-out performance (results/eval_gate/"
             "EVALUATORS.md item 1).")
FIG6_ARM = ("The split-trained arm (encoder from ImageNet weights on the training side of the built person-disjoint split, "
            "because the v8/v9 level banks trained on 49 of the 54 L6 validation and test persons; "
            "docs/RESUME_2026-09-22_PM.md, checkpoint 2026-09-23 21:45; tables/tab4_transitional.md note d) is scored in "
            "paper 2 (SchwingNet/paper2_levelcheck/), whose manifest fixes bank, split, initialisation and recipe before "
            "unblinding; the manuscript shows only its development learning curve (supplement) and scores no held-out "
            "transitional person (SchwingNet/PAPER1_SCOPE.md).")

SN = Path(__file__).resolve().parents[1]
R = SN / "results"
J = lambda p: json.load(io.open(p, encoding="utf-8"))

a1, a4, a7, a9 = J(R / "a1.json"), J(R / "a4.json"), J(R / "a7.json"), J(R / "a9.json")
f2, pw = J(R / "figure2/figure2_metrics.json"), J(R / "power/power.json")
# the persons-available block left power.json when Figure 5 was rebuilt around the data case (2026-09-25 10:26; the
# persons-available panels are paper 2's): the block as generated on 2026-09-24 10:33 (git 8d6a4f4) is kept, with its
# origin and each count's live source, in packet_src/persons_available_2026-09-24.json (numbers.json reads it too)
pa = J(SN / "packet_src" / "persons_available_2026-09-24.json")


def pct(x, d=1):
    return f"{100 * x:.{d}f}"


def ci(pair, d=1):
    return f"{pct(pair[0], d)}-{pct(pair[1], d)}"


zs = a7["cells"]["zeroshot2/det/LAT/kfull"]["exact_full_coverage"]
zsap = a7["cells"]["zeroshot2/det/AP/kfull"]["exact_full_coverage"]
cv = a4["cells"]["det/LAT/kfull"]
cvap = a4["cells"]["det/AP/kfull"]
k5, k3, k1 = a4["cells"]["det/LAT/k5"], a4["cells"]["det/LAT/k3"], a4["cells"]["det/LAT/k1"]
day = a9["cv"]["cvday_acquisition_day_folds"]["cells"]["det/LAT/kfull"]
dv = a1["operating_points"]["cross_device_0.74"]["vertebra_recall_outline"]
ds = a1["operating_points"]["cross_device_0.74"]["sacrum_found_outline"]
dv25 = a1["operating_points"]["conf_0.25_as_quoted"]["vertebra_recall_outline"]
ds25 = a1["operating_points"]["conf_0.25_as_quoted"]["sacrum_found_outline"]
sil = f2["silhouette"]["pairs"]
nn = f2["nearest_other_person"]
day_k = round(day["exact"] * 617)
assert (zs["k"], zs["n"], cv["k"], k3["k"], dv["k"], ds["k"], day_k) == (594, 617, 606, 1079, 231, 43, 571)

numbers = {
    "zs": f"{zs['k']:,} of {zs['n']:,} ({pct(zs['point'])} %; Wilson on the design-effect-adjusted n {ci(zs['wilson_effective_n'])}; "
          f"{zs['clusters']} cases)",
    "zsap": f"{zsap['k']:,} of {zsap['n']:,} ({pct(zsap['point'])} %; {ci(zsap['percentile'])})",
    "cv": f"{cv['k']:,} of {cv['n']:,} ({pct(cv['point'])} %; Wilson on the design-effect-adjusted n {ci(cv['wilson_effective_n'])}; "
          f"percentile {ci(cv['percentile'])}; BCa {ci(cv['bca'])}; {cv['clusters']} cases, {cv['clusters_with_error']} with an error)",
    "cvap": f"{cvap['k']:,} of {cvap['n']:,} ({pct(cvap['point'])} %; {ci(cvap['percentile'])})",
    "day": f"{day_k} of 617 ({pct(day['exact'])} %; {ci(day['exact_ci_percentile_pool_scores'])}; BCa {ci(day['exact_ci_bca'])})",
    "k5": f"{k5['k']:,} of {k5['n']:,} ({pct(k5['point'])} %; {ci(k5['percentile'])})",
    "k3": f"{k3['k']:,} of {k3['n']:,} ({pct(k3['point'])} %; {ci(k3['percentile'])})",
    "k1": f"{k1['k']:,} of {k1['n']:,} ({pct(k1['point'])} %; {ci(k1['percentile'])})",
    "dv": f"{dv['k']:,} of {dv['n']} vertebrae ({pct(dv['point'])} %; {ci(dv['percentile'])})",
    "ds": f"{ds['k']:,} of {ds['n']} sacra ({pct(ds['point'])} %; {ci(ds['percentile'])})",
    "dv25": f"{dv25['k']:,} of {dv25['n']:,} ({pct(dv25['point'])} %)",
    "ds25": f"{ds25['k']:,} of {ds25['n']:,} ({pct(ds25['point'])} %)",
    "sil": f"{sil['L6|L5']['mean_a']:.2f} ({sil['L6|L5']['ci_a'][0]:.2f}-{sil['L6|L5']['ci_a'][1]:.2f}; "
           f"{sil['L6|L5']['n_a']} crops, {sil['L6|L5']['persons_a']} persons)",
    "sil54": f"{sil['L5|L4']['mean_a']:.2f} ({sil['L5|L4']['ci_a'][0]:.2f}-{sil['L5|L4']['ci_a'][1]:.2f}; "
             f"{sil['L5|L4']['persons_a']} persons)",
    "nn": f"{pct(nn['same_level'])} % ({ci(nn['same_level_ci'])}) of {nn['n']:,} validation crops of {nn['persons']:,} persons",
    # results/power/power.json (tools/fig_power.py, 2026-09-25 10:26): the Wilson persons-needed n in
    # n_needed_zero_errors; the 97.6 % comparator crossing and the exact-test n left with the comparison (paper 2) and
    # the card never printed them. The three real C-ArmLSpine L6 (excluded from paper 2's primary analysis in advance,
    # so no best-case interval is drawn for them), the verified count and the real-frame candidates come from the
    # preserved persons-available block (pa, above).
    "need90": pw["n_needed_zero_errors"]["G6_level_wilson_90"],
    "real": pa["not_drawn"]["carmlspine_real_L6"]["n"],
    "real_reference": pa["rows"]["at_risk_pooled"]["real_reference"],
    "real_candidates": pa["rows"]["at_risk_pooled"]["real_counted_with_frame"],
}
assert (numbers["need90"], numbers["real"], numbers["real_candidates"]) == (35, 3, 7), numbers
COUPLED = ("count from the detected sacrum exact on 979 of 1,009 anchored bodies of 130 cases (97.0 %; 94.2-99.2), "
           "classifier 993 (98.4 %), coupled call 995 (98.6 %; 97.2-99.7); the sacrum was anchored on 233 of 290 lateral "
           "frames; the stop signal fired on 4 of 5 frames with a coupled error and on 17 of 225 without, and the coupled "
           "call was exact on 921 of 922 unflagged bodies (results/COUPLING.md, rows det74/kfull; SchwingNet/sections/results.tex)")

# ---------------------------------------------------------------------------------------------- model card
mp = SN / "atlas" / "model.json"
m = J(mp)
M = m["Model"]
M["Name"] = ("SchwingNet: vertebral level naming from one intraoperative C-arm exposure (detectors, level encoder, "
             "recurrent head, count from the sacrum, alphabet coupling)")
M["Summary"] = (
    "SchwingNet names the vertebral level of each body on one intraoperative C-arm exposure, with no preoperative scan, "
    "registration, tracked instrument or fiducial. Four parts ship together: (1) two detectors never trained on the test "
    "C-arm, a film-trained YOLO11m-pose keypoint detector that boxes the bodies to be named (confidence 0.35) and a YOLO11m "
    "vertebra/sacrum detector trained on real COBRA2026 and DeepFluoro frames that boxes the sacrum (confidence 0.74, set "
    "on three other devices); (2) a ResNet-18 level encoder reading a fixed-scale two-channel crop per body into a 512-d "
    "embedding and a 27-level posterior (C1-C7, T1-T13, L1-L6, sacrum); (3) a two-layer bidirectional GRU head over runs "
    "of two to nine bodies; (4) a count of each body's rank from the detected sacrum and an alphabet coupling that chooses "
    "the ordinary, L6, T13 or both-variant naming and stops the read when the classifier disagrees. On C-ArmLSpine (148 "
    "lumbar cases, one C-arm, cone-beam CT truth from two automatic labellers), never trained on that C-arm, it named "
    f"{numbers['zs']} detected lateral vertebrae exactly and {zsap['k']:,} of {zsap['n']} anteroposterior; fine-tuned with "
    f"case-grouped folds {cv['k']:,} of {cv['n']:,} ({pct(cv['point'])} %) and with folds grouped by acquisition day "
    f"{day_k} of 617 ({pct(day['exact'])} %); with three bodies in view {k3['k']:,} of {k3['n']:,} ({pct(k3['point'])} %). At "
    "detector confidence 0.74 the coupled call was exact on 995 of 1,009 anchored bodies (98.6 %). The held-out detector "
    f"found {numbers['dv']} and {numbers['ds']}. Transitional spines: {numbers['real']} persons with a real transitional "
    "exposure exist in public releases, scored only in cross-validation as agreement with one labeller's read; no held-out "
    "transitional person is scored, and the comparison with registration-assisted labelling (LevelCheck) and surgeons using "
    "it is a separate study (paper 2, SchwingNet/paper2_levelcheck/). Research prototype; nothing evaluated prospectively; "
    "not for clinical use.")
assert len(M["Summary"]) <= 2500, len(M["Summary"])
M["Indexing"]["Keywords"] = ["vertebral level", "wrong-level surgery", "intraoperative fluoroscopy", "C-arm",
                             "lumbar spine", "sacrum", "transitional vertebra", "lumbosacral transitional vertebra",
                             "object detection", "held-out device"]
D = M["Descriptors"]
D["Authors"] = [{"Name": "Gregory J. Schwing", "Email": "[e-mail withheld]",
                 "URL": "https://github.com/Gregory-Schwing-MD-PhD"}]
D["Comments"] = ("Sole author of the code, the manuscript and the cards. No ORCID iD is recorded in the repository, so "
                 "none is asserted. Card rewritten 2026-09-23 for the six-figure manuscript (SchwingNet/main.tex) and "
                 "updated " + TODAY + " (SchwingNet/atlas/README.md, 'What changed').")
D["Contact"] = ("Gregory J. Schwing, MD, PhD, Department of General Surgery, Wayne State University School of Medicine / "
                "Detroit Medical Center; [e-mail withheld]")
D["Date"] = {"Created": "2026-09-22", "Updated": TODAY}
D["Ethical review"] = (
    "No new patient data were acquired. The Wayne State University IRB Administration Office issued a Notice of IRB "
    "Administrative Determination on 2026-09-02 (WSU IRB HPR Number 2026-269, 'Open Spine Consortium: Secondary Analysis "
    "of Publicly Available, De-Identified Imaging Datasets and the Derived Annotations, Software, and Models Produced From "
    "Them'): not human participant research under 45 CFR 46 or FDA regulations; IRB review not required (the signed "
    "notice was read page by page on 2026-09-23). The determination covers sources that are public, de-identified before "
    "release and downloadable without application or data use agreement. VinDr-SpineXR, whose films sit in the "
    "intraoperative fold banks, is released by PhysioNet only under its Restricted Health Data Use Agreement and is "
    "outside that scope; a separate determination, or retraining without it, is open before submission. One C-ArmLSpine "
    "directory (case134/ori, 302 XA frames) carries a real PatientID and name; it is excluded from every bank and never "
    "printed.")
D["Funding"] = ("None declared (the author confirms on the full title page). Compute: Wayne State University High "
                "Performance Computing Grid.")
D["License"] = {"Text": RELEASE, "URL": "https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet"}
D["Organizations"] = [{"Name": "Wayne State University School of Medicine, Department of General Surgery / Detroit "
                                "Medical Center", "Contact name": "Gregory J. Schwing",
                       "Email": "[e-mail withheld]", "Address": "Detroit, MI, USA",
                       "URL": "https://www.med.wayne.edu/"}]
# Idempotent: drop every entry this script owns before adding it back (the old filter kept CTSpinoPelvic1K and
# re-appended it on each run). COBRA2026 and Grupp 2020 are corrected per REFS_AUDIT.md rows 25-26 / refs_corrections.bib.
OWNED = ("CTSpinoPelvic1K", "Checklist for Artificial Intelligence", "COBRA2026", "Automatic annotation of hip anatomy")
refs = []
for r in D["References"]:
    if r["Title"].startswith(OWNED) or any(r == x for x in refs):
        continue
    refs.append(r)
refs[1:1] = [
    {"Title": "Automatic annotation of hip anatomy in fluoroscopy for robust and efficient 2D/3D registration",
     "Authors": "Grupp RB, Unberath M, Gao C, Hegeman RA, Murphy RJ, Alexander CP, Otake Y, McArthur BA, Armand M, "
                "Taylor RH",
     "Source": "Int J Comput Assist Radiol Surg 2020;15(5):759-769", "Date": "2020",
     "DOI": "10.1007/s11548-020-02162-7", "PMID": "32333361",
     "Notes": "DeepFluoro: Siemens Cios Fusion, six cadaveric pelves, 366 registered frames; CC BY-NC-SA 4.0."},
    {"Title": "COBRA2026: a large-scale multicenter pelvic CBCT projection dataset",
     "Authors": "Thummerer A, Rit S, Kamp F, Maspero M, Boné T, Baudier T, Arnhold J, Kadhim M, Rauter M, Kurz C, "
                "Landry G, Knäusl B, Zimmermann L",
     "Source": "Zenodo, version 1.0.0 (published 2026-07-13); descriptor arXiv:2607.20037", "Date": "2026-07-13",
     "DOI": "10.5281/zenodo.21322350",
     "Notes": "Elekta XVI centres A-D used; 145 cases in the frame splits; CC BY-NC 4.0. Creators, title and version "
              "from the Zenodo record (SchwingNet/REFS_AUDIT.md row 26)."},
]
refs += [
    {"Title": "CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame, annotated for lumbosacral "
              "transitional anatomy", "Authors": "Schwing G, Schehr A, et al.", "Source": "Zenodo, version v11",
     "Date": "2026", "DOI": "10.5281/zenodo.22797014",
     "Notes": "801 of 802 CT records rendered into the level bank; preprint arXiv:2609.22760 (the subject overlap)."},
    {"Title": "Checklist for Artificial Intelligence in Medical Imaging (CLAIM): 2024 Update",
     "Authors": "Tejani AS, Klontzas ME, Gatti AA, Mongan JT, Moy L, Park SH, Kahn CE Jr, CLAIM 2024 Update Panel",
     "Source": "Radiol Artif Intell 2024;6(4):e240300", "Date": "2024", "DOI": "10.1148/ryai.240300",
     "PMID": "38809149", "PMCID": "PMC11304031",
     "Notes": "Reporting checklist; the 44-item map is SchwingNet/packet_src/claim2024/."},
]
D["References"] = refs
D["Version"] = ("Level models: the C-ArmLSpine case-grouped five-fold arm scored 2026-09-21 (docs/carmlspine_cv5_mixed_"
                "2026-09-21.json, re-scored with intervals in SchwingNet/results/a4.json), the day-grouped arm "
                "(results/a9.json) and the zero-shot arm (results/a7.json); the embedding is of allspine_v9 "
                f"(SHA-256 {f2['encoder_sha256'][:16]}..., results/figure2/figure2_metrics.json). Detectors: "
                "rx_lodo_carmlspine_1024 (results/a1.json) and the keypoint detector detector_v5z_final "
                "(docs/MANIFEST_DATA_MODELS_RESULTS.md). " + FIG6_ARM + " "
                "No code SHA is recorded in the level-model result files (docs/MODEL_CARD.md 1.2). Checkpoint lineage for "
                "306 checkpoints, from each result file back to the public release weights: "
                "SchwingNet/results/eval_gate/LINEAGE.md.")
P = M["Model properties"]
P["Architecture"] = (
    "Body detector: YOLO11m-pose (Ultralytics) fine-tuned for 60 epochs on the plain-film keypoint corpus from the pose "
    "checkpoint detect_v3, itself trained from the COCO-pretrained yolo11m-pose.pt (docs/MANIFEST_DATA_MODELS_RESULTS.md, "
    "detector_v5z_final; results/eval_gate/LINEAGE.md); confidence 0.35. Sacrum detector: "
    "YOLO11m, classes vertebra and sacrum, 1,024-pixel input, initialised from COCO-pretrained yolo11m.pt through the "
    "render-trained anchor_none_v2_17-1882, 80 epochs, patience 25, batch 8, seed 0, deterministic; augmentation degrees "
    "10, translate 0.1, scale 0.3, fliplr 0.5, mosaic 0.5 (args.yaml and data.yaml of rx_lodo_carmlspine_1024, read on "
    "the grid 2026-09-22); its best.pt was selected on the COBRA2026 and DeepFluoro test splits (results/eval_gate/"
    "EVALUATORS.md item 2); confidence 0.74 (results/a1.json cross_device_0.74 how_chosen). Level encoder: ResNet-18 with a "
    "two-channel stem (image + target marker) over a 2 x 320 x 320 fixed-scale crop with the target body at 96 pixels, "
    "27-class head, 11,173,376 parameters, 3.62 GMAC per crop; the cross-validation encoders are initialised from "
    "registry alias allspine_v2_r1 and fine-tuned per fold for 15 epochs at lr 1e-4 with AdamW, cosine schedule and "
    "class-weighted cross-entropy (slurm/carmlspine_cv.sh; tools/train_level_classifier.py); horizontal-flip test-time "
    "averaging. Recurrent head: Linear(512->256) + GELU, two-layer bidirectional GRU(256), Linear(512->27), 2,117,403 "
    "parameters, trained on mixed-length runs of 2-9 bodies (tools/head_mixed_length.py --train-mode mixed: 30 epochs, "
    "lr 1e-3, AdamW, cosine). Count: rank from the detected sacrum, no morphology. Alphabet coupling "
    "(tools/alphabet_couple.py): chooses among the ordinary, L6, T13 and both-variant alphabets the one best fitting the "
    "posteriors at the ordinals; a classifier name differing from the call stops the read. No learned parameters in the "
    "count or the coupling. The sweep linker of earlier drafts is not part of the reported system.")
P["Availability"] = (
    "Not public. Weights on the Wayne State grid: fold encoders ~/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_"
    "aug2.pt, heads ~/model_night/heads_carm/head_cv{0..4}.pt, sacrum detector ~/spine-detector/runs/realxray/"
    "rx_lodo_carmlspine_1024/weights/best.pt, body detector ~/FluoroCap/detect_v5z_final_best.pt (registered, "
    "docs/MANIFEST_DATA_MODELS_RESULTS.md). The fold encoders, heads and sacrum detector carry no registered SHA-256 "
    "(docs/MODEL_CARD.md 1.3), a defect to repair before any deposit. Available to reviewers and editors on request; "
    "what is released at publication is the author's open decision (License).")
P["Clinical benefit"] = (
    "None demonstrated. No prospective or clinical study exists and no clinician has read the output in theatre. The "
    "motivating harm is wrong-level spine surgery; no naming accuracy here is a wrong-level surgery rate.")
P["Decision threshold"] = (
    "Sacrum detector confidence 0.74: the best pooled vertebra F1 of this arm over its sweeps on COBRA2026, DeepFluoro and "
    "the Geneva phantom, reading no C-ArmLSpine frame; adopted as the headline after the 0.25 result had been reported, so "
    "it is described as cross-device, not pre-stated (results/a1.json). Body detector confidence 0.35. Naming abstains "
    "when the decoded and single-crop names disagree or the top posterior is below 0.5, an untuned default on an "
    "uncalibrated posterior; lateral whole frame, case-grouped: 513 of 617 answered, 505 of 513 exact "
    "(results/a7.json cv5/det/LAT/kfull default_rule). The coupled call's stop signal: " + COUPLED + ".")
P["Degree of automation"] = (
    "Assistive decision support, research use only: names beside the surgeon's own count, abstaining visibly, never "
    "replacing the check film. Per body: a box, a level name, a posterior, an abstain or stop flag.")
P["Indications for use"] = (
    "Research use only; no clinical indication. The only intraoperative test set is lumbar (C-ArmLSpine), so the tested "
    "scope is the lumbar spine and sacrum on a lateral exposure; the anteroposterior view did not transfer to an unseen "
    "device.")
P["Input"] = (
    "One 8-bit C-arm exposure converted to attenuation and windowed identically for every device (field percentiles "
    "1/5/50/95/99 mapped to 27/47/126/216/239, bone bright; docs/REAL_XRAY_DATASETS_SPEC.md 'Display'); C-ArmLSpine "
    "exported at 1,024 x 1,024 (detector pitch 0.293 mm at export, object-plane 0.1915 mm at SID 1140 / SOD 745 mm).")
P["Limitations"] = (
    "(1) Detection on an unseen device is the binding constraint: " + numbers["dv"] + " and " + numbers["ds"] + " at 0.74 "
    "(results/a1.json), short of the 97 % counting grade stated beforehand; at the software default 0.25, "
    + numbers["dv25"] + " and " + numbers["ds25"] + ". Boxes are whole-vertebra projections; the vertebral-body "
    "convention recompute is pending (G5). (2) The anteroposterior view did not transfer zero-shot: " + numbers["zsap"]
    + ". (3) Truth is two automatic labellers (TotalSegmentator, SPINEPS with VERIDAH) agreeing on 814 of 910 CBCT "
    "vertebrae; the filter withholds T11 and most of T12, and both count from the sacrum, so agreement is not "
    "independent; no person read an intraoperative image. (4) Whether the 148 C-ArmLSpine cases are 148 people cannot be "
    "established; case-grouped " + numbers["cv"] + " against day-grouped " + numbers["day"] + ", a gap not explained. "
    "(5) Transitional evidence is thin: the L6-L5 silhouette " + numbers["sil"] + " is on the validation split that chose "
    "the checkpoint; the three never-seen L6 patients separate only under the whole-vertebra box; 49 of the 54 L6 "
    "validation and test persons of the built split were in the current encoder's training (tables/tab4_transitional.md), "
    f"so no model reported here scores the transitional test persons; the {numbers['real']} real transitional persons in "
    "public releases (the C-ArmLSpine L6) are scored only in cross-validation as agreement with one labeller's read; "
    f"certifying 90 % exact-level accuracy needs {numbers['need90']} error-free at-risk persons, and {numbers['real_candidates']} "
    f"real-frame candidates exist, {numbers['real_reference']} of them verified (packet_src/persons_available_2026-09-24.json, "
    f"the persons-available block of results/power/power.json as of 2026-09-24). (6) The comparison "
    "with registration-assisted labelling (LevelCheck) and surgeons using it is a separate study (paper 2, "
    "SchwingNet/paper2_levelcheck/; its comparator LEVELCHECK_MODEL.md is frozen, last commit d0403de) and nothing from it "
    "is quoted in this card. (7) The "
    "per-device image-formation terms missed their pre-stated "
    "every-device criterion (results/a6.json; statistical review F6). (8) The posterior is uncalibrated. (9) VinDr-"
    "SpineXR crops in the fold banks were obtained under a PhysioNet data use agreement outside the project's IRB "
    "determination (open). (10) Untested: cervical and thoracic intraoperative frames, instrumentation, paediatric, "
    "post-operative and deformed spines, any C-arm beyond those named. (11) Nothing evaluated prospectively. (12) "
    + SELECTION + " (13) Only the sacrum detector's held-out-device results are clean; its checkpoint was selected on "
    "the COBRA2026 and DeepFluoro test frames, and its render-trained parent trained on renders of five, and validated "
    "on renders of one, of the 17 subjects of the synthetic arc set (results/eval_gate/EVALUATORS.md).")
P["Output"] = {"Description": ("Per detected body: a box, a level name from 27 classes (C1-C7, T1-T13, L1-L6, sacrum), "
                               "its posterior, an abstain flag; per frame: the ranks from the detected sacrum, the "
                               "chosen naming alphabet and a stop flag when classifier and coupled call disagree. No CDE "
                               "is mapped."), "CDEs": []}
P["Recommendation"] = (
    "Do not use clinically. Quote every figure with its clustered interval, its operating point and its result file; "
    "report detection beside naming and the abstention and stop rates beside every accuracy; for transitional spines "
    "quote nothing beyond the three C-ArmLSpine patients' cross-validation agreement with one labeller's read and the "
    "person counts of Table 2 and Figure 5; the comparison with LevelCheck is paper 2's and is quoted from there when it "
    "is unblinded. Never quote a selection-split number as held-out performance.")
P["Regulatory information"]["Comment"] = (
    "The author has a commercial interest in a level-confirmation product under development; no product or regulatory "
    "pathway is named in this work (the conflict statement of the full title page).")
P["Reproducibility"] = (
    "Every manuscript number is listed with its result file and JSON path in SchwingNet/NUMBERS.md; the rigor-audit "
    "intervals are recomputed by tools/rigor_fixes.py and SchwingNet/tools/stats_review_recompute.py. Seeds: sacrum "
    "detector 0 (args.yaml). Missing: code SHA in the level-model result files, SHA-256 for the fold weights (the "
    "split-trained arm's manifest is paper 2's). The sacrum detector's checkpoint was selected on its training devices' test splits, so only its "
    "held-out-device numbers are clean. What each scored checkpoint and its ancestors trained and selected on, per "
    "patient key: SchwingNet/results/eval_gate/LINEAGE.md and EVALUATORS.md (306 checkpoints; tools/eval_gate.py "
    "refuses a held-out claim on a touched person).")
M["Imaging"]["Procedures"] = [{"Name": "Intraoperative lumbar spine C-arm fluoroscopy, lateral and anteroposterior exposures"}]
M["Model performance"]["Comments"] = (
    "Intervals are 2,000-resample bootstraps clustered by case (percentile, BCa beside), or Wilson on the design-effect-"
    "adjusted count where errors fall in few clusters (SchwingNet/NUMBERS.md). NAMING on C-ArmLSpine, detected lateral "
    "bodies at full coverage: zero-shot (no C-ArmLSpine frame in training) " + numbers["zs"] + " (results/a7.json); "
    "anteroposterior " + numbers["zsap"] + ". Fine-tuned, case-grouped five-fold: " + numbers["cv"] + " (results/a4.json); "
    "anteroposterior " + numbers["cvap"] + "; day-grouped three-fold " + numbers["day"] + " (results/a9.json). Limited "
    "fields, case-grouped: five bodies " + numbers["k5"] + ", three " + numbers["k3"] + ", one " + numbers["k1"] + " "
    "(results/a4.json). COUNT AND COUPLING at sacrum-detector confidence 0.74: " + COUPLED + ". DETECTION, device held "
    "out (trained on COBRA2026 and DeepFluoro real frames; 56 C-ArmLSpine test frames, 28 cases, IoU 0.5, whole-vertebra "
    "boxes): " + numbers["dv"] + ", " + numbers["ds"] + " at 0.74 (results/a1.json). EMBEDDING (allspine_v9, validation "
    "split that chose the checkpoint): nearest crop of another person at the same level for " + numbers["nn"] + "; cosine "
    "silhouette L6 against L5 " + numbers["sil"] + ", L5 against L4 " + numbers["sil54"] + " "
    "(results/figure2/figure2_metrics.json). TRANSITIONAL: no held-out transitional person is scored; the three "
    "C-ArmLSpine patients one labeller reads as L6 are scored in cross-validation as agreement with that read (the coupled "
    "call agreed on one of their four anchored frames at confidence 0.74; SchwingNet/sections/results.tex). The comparison "
    "against a LevelCheck model is paper 2's (SchwingNet/paper2_levelcheck/); nothing from it is quoted. NOT QUOTED: " + SELECTION + " "
    "Not measured: calibration, per-class intervals, training-partition performance.")

io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(m, indent=1, ensure_ascii=False) + "\n")
print("model.json summary chars", len(M["Summary"]))

# ---------------------------------------------------------------------------------------------- dataset card
dp = SN / "atlas" / "dataset.json"
d = J(dp)
DS = d["Dataset"]
DS["Name"] = ("SchwingNet corpus: real C-arm exposures with volumetric truth, rendered CT, level-annotated radiographs and "
              "the transitional-person inventory (state of " + TODAY + ")")
DS["Summary"] = (
    "The data behind the SchwingNet manuscript (five figures, three tables; " + TODAY + "). Assembled from public releases only; nothing was "
    "acquired and the derived layout is not redistributed because the source licences differ. Table 1 of the manuscript "
    "(SchwingNet/tables/tab_corpus.md, every cell traced in tab_corpus.sources.md) counts 4,093 renders of labelled CT "
    "(CTSpinoPelvic1K 801, TotalSegmentator v2 1,170 and v3 1,735, VerSe 387), 9,108 level-annotated films (CSXA 4,963, "
    "BUU-LSPINE 3,603 lateral, NHANES II 542) and 4,276 real exposures with three-dimensional truth (C-ArmLSpine 296, "
    "DeepFluoro 366, COBRA2026 Elekta 3,480, Geneva 116, Ljubljana 18), of which 778 come from mobile C-arms. The "
    "intraoperative test set is C-ArmLSpine: 148 lumbar cases on one C-arm, cone-beam CT truth from two automatic "
    "labellers agreeing on 814 of 910 vertebrae. Transitional persons, typed from each source's own truth under a rib "
    "convention (tables/tab4_transitional.md): 194 in all, 110 with L6, 7 with T13, 28 with a sacralised L5 (12 with four "
    "lumbar vertebrae), 31 Castellvi I/II, 14 with a lumbar rib, 4 unassigned; the only real intraoperative ones are three "
    "C-ArmLSpine L6 of one automatic labeller, and a COBRA2026 screen adds 38 L6 and 45 T13 calls that no person has read. "
    "The built person-disjoint split (50/10/40 within subtype) puts 43 L6 and 3 T13 CT persons and the three real L6 on "
    "the test side. Known defects are under Noise; aliases that make one person several names are under Relationships "
    "between instances.")
assert len(DS["Summary"]) <= 2500, len(DS["Summary"])
DD = DS["Descriptors"]
DD["Authors"] = [{"Name": "Gregory J. Schwing", "Email": "[e-mail withheld]",
                  "URL": "https://github.com/Gregory-Schwing-MD-PhD"}]
DD["Comments"] = ("Assembler of the derived layout, not the originator of any image; the originating releases are under "
                  "References. No ORCID iD is recorded in the repository. Card updated 2026-09-23 for the six-figure "
                  "manuscript and " + TODAY + " (SchwingNet/atlas/README.md, 'What changed').")
DD["Contact"] = ("Gregory J. Schwing, MD, PhD, Department of General Surgery, Wayne State University School of Medicine / "
                 "Detroit Medical Center; [e-mail withheld]")
DD["Date"] = {"Created": "2026-09-22", "Updated": TODAY}
DD["Ethical review"] = M["Descriptors"]["Ethical review"]
DD["Funding"] = M["Descriptors"]["Funding"]
DD["Organizations"] = M["Descriptors"]["Organizations"]
DD["License"]["Text"] = (
    "Composite; the derived layout is not distributed. Sources: C-ArmLSpine CC BY 4.0; COBRA2026 CC BY-NC 4.0; DeepFluoro "
    "CC BY-NC-SA 4.0; Geneva hip CC BY-SA 4.0; Ljubljana 2D-3D-GS CC BY-NC-ND; TotalSegmentator CC BY 4.0; CTSpinoPelvic1K "
    "v11 CC BY-NC-SA 4.0 (Zenodo; its Hugging Face mirror still carries v10 labels and different licence metadata, an "
    "open repair); VinDr-SpineXR PhysioNet Restricted Health Data License 1.5.0 under a data use agreement. A merged "
    "redistribution is not possible under these terms; a reader rebuilds the layout from each source with the released "
    "exporters. FluoroCap panels are figure reuse, trained only intraoperative fold banks, and are never redistributed.")
# Same idempotent rule as the model card: the owned entries come from the model card, once each.
own = {r["Title"]: r for r in M["Descriptors"]["References"] if r["Title"].startswith(OWNED[:1] + OWNED[2:])}
kept = []
for r in DD["References"]:
    if r["Title"].startswith(OWNED) or any(r == x for x in kept):
        continue
    kept.append(r)
kept[1:1] = [own[t] for t in own if not t.startswith("CTSpinoPelvic1K")]
DD["References"] = kept + [own[t] for t in own if t.startswith("CTSpinoPelvic1K")]
DD["Version"] = ("State of " + TODAY + ". Manifest with SHA-256 over each input file list: docs/RSNAI_DATA_MANIFEST.json "
                 "(2026-09-22). Transitional inventory: SchwingNet/results/rare_class/transitional_subtypes.csv and "
                 "split_plan.md (2026-09-23), as the manuscript's Table 2 prints it; the overnight screens of 2026-09-24 "
                 "(VerSe, all 355 people; TotalSegmentator v3, 1,935 scans; docs/RESUME_2026-09-22_PM.md) will change "
                 "those counts when Table 2 is regenerated, and this card follows the table. COBRA2026 is complete on disk "
                 "(692 of 692 cases) but the reported banks hold the 145 Elekta cases fetched before the analysis.")
PR = DS["Dataset properties"]
PR["Missing information"] = PR["Missing information"].replace(
    "CTSpinoPelvic1K CT 0533: truncated download, absent from every render bank.",
    "CTSpinoPelvic1K CT 0533: published truncated in the Hugging Face mirror (the Zenodo record carries no CT); the "
    "mirror copy was replaced with the rebuild on 2026-09-23 (sha256 478a74e9...), after the render banks were built, so "
    "the banks still hold 801 of 802.")
PR["Noise"] = PR["Noise"].replace(
    "(16) CTSpinoPelvic1K CT 0533 is a truncated download (16.5 MiB, gzip EOFError); the render bank holds 801 of 802.",
    "(16) CTSpinoPelvic1K CT 0533 was a truncated file in the public mirror (16.5 MiB, gzip EOFError); the mirror was "
    "repaired on 2026-09-23 (commit 72cd777) and the render bank still holds 801 of 802. (17) Transitional subtype calls "
    "from SPINEPS with VERIDAH (COBRA2026, C-ArmLSpine) are read by no person; on CTSpinoPelvic1K that labeller's L6 call "
    "matched the readers in 10 of 24 (tables/tab4_transitional.md note e). Twelve TotalSegmentator spines once called L6 "
    "from raw mask identifiers: eight read normal on an independent rib count (scrambled SPINEPS instance ids).")
PR["Sampling"] = PR["Sampling"].replace(
    "COBRA2026: 152 Elekta and 26 Varian cases fetched before the analysis of 692 public (six centres, A-D Elekta and F-G "
    "Varian; the full release is being fetched); 145 Elekta cases in splits.",
    "COBRA2026: 152 Elekta and 26 Varian cases fetched before the analysis of 692 public (six centres, A-D Elekta and F-G "
    "Varian); 145 Elekta cases in splits; the full release is now on disk (692 of 692) and not yet in any bank.")
DS["Partitions"] = [p for p in DS["Partitions"] if p.get("Partition") != "Test"]
DS["Partitions"].append({
    "Partition": "Test",
    "Total": {"Patient count": 49,
              "Criterion": ("Transitional test side of the built person-disjoint, subtype-stratified split (50/10/40 within "
                            "each subtype; every real transitional subject on the test side): L6 43 CT persons + 3 real "
                            "(C-ArmLSpine), T13 3 CT persons (tables/tab4_transitional.md; split_plan.md). These are the "
                            "L6 and T13 rows only; all subtypes together hold 77 CT + 3 real test persons."),
              "Comments": ("No model of paper 1 scores these persons (SchwingNet/PAPER1_SCOPE.md); the three real C-ArmLSpine "
                           "L6 appear in paper 1 only as cross-validation agreement with one labeller's read. " + FIG6_ARM +
                           " COBRA2026 screen calls (38 L6, 45 T13, 8 four-lumbar) are read by no person; a two-labeller "
                           "count with both junctions in the field finds seven at-risk persons with an exported frame "
                           "(Table 2, Figure 5c). How an unread test person enters paper 2's primary analysis is fixed in "
                           "LEVELCHECK_MODEL.md (sections 4 and 14) and untouched by paper 1.")},
    "Comments": "Not scored in paper 1. Test side of paper 2's comparison against the frozen LevelCheck model (SchwingNet/paper2_levelcheck/)."})
# The 17 styled-corpus subjects are the selection (validation) set of every dc_* arm, not a held-out set
# (results/eval_gate/EVALUATORS.md, corrections table: tables/tab_corpus.tex:43).
for part in DS["Partitions"]:
    t = part.get("Total", {})
    if part.get("Partition") == "Validation" and t.get("Criterion", "").startswith("The 17 TotalSegmentator subjects"):
        t["Criterion"] = (
            "The 17 TotalSegmentator subjects on the validation (checkpoint-selection) side of every styled synthetic "
            "corpus (STYLE_INFO.json val_subjects: s0585, s0970, s1045, s1062, s1159, s1384, s1535, s1579, s1700, s1836, "
            "s1842, s1872, s1880, s1883, s1902, s2033, s2053); 1,998 validation entries in the P_pooled list. They select "
            "the styled-corpus arms' checkpoints, so no styled-corpus arm is held out on them.")
        t["Comments"] = (
            "Used by the styled-corpus detector arms (dc_A, dc_B, dc_P), not by the model card's real-frame detector. "
            "These 17 subjects also appear in up to five CT render banks under other name forms (alias f), and the "
            "real-frame detector's render-trained parent (anchor_none_v2_17-1882) trained on renders of five of them "
            "(s0585, s0970, s1045, s1159, s1384) and validated on renders of one (s1062) "
            "(SchwingNet/results/eval_gate/EVALUATORS.md).")
# the External-testing subset comment quoted the superseded body-box figure as "the model card's" result
for part in DS["Partitions"]:
    for sub in part.get("Subsets", []):
        c = sub["Total"].get("Comments", "")
        i = c.find("The detector result quoted in the model card")
        if i >= 0:
            j = c.find("Collimated variants")
            sub["Total"]["Comments"] = (
                c[:i] + "The sacrum detector's result the manuscript and model card quote is scored here at "
                "confidence 0.74, whole-vertebra boxes: " + numbers["dv"] + " and " + numbers["ds"] +
                " (SchwingNet/results/a1.json). The body-box convention recompute is pending (G5)." +
                (" " + c[j:] if j >= 0 else ""))
io.open(dp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
print("dataset.json summary chars", len(DS["Summary"]))
