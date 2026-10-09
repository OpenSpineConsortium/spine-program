#!/usr/bin/env python3
"""Generate the migration plan tables from the disk map and sources.json. Standard library only; Python 3.6+.

Inputs (all in this folder or its parent):
  disk_map.csv           every top-level entry of HOME, HOME/data, the Ceph root, Ceph data/ and data/anomaly_harvest,
                         plus 75 depth-2 rows, classified by family E on 2026-10-07 (columns path, storage, role,
                         source_id, size_gb, size_source, date, notes)
  ../sources.json        the source entries (layout folder per source)
  census.tsv (optional)  the 2026-10-07 storage census (job 40578909). When given with --census, its sizes replace the
                         dated sizes of the disk map. Accepted columns: a header naming `path` and one of `bytes`,
                         `size_bytes`, `kb`, `kib`, `gb` (case-insensitive). Rows it does not cover keep the old size.

Outputs:
  layout_map.csv            one row per imaging-related entry: current path -> target path, action, batch, size
  migration_batches.csv     one row per batch: order, items, GB, dependency
  batch_items/<BATCH>.tsv   src <TAB> dst <TAB> est_gb <TAB> flags, read by migrate_batch.sbatch
  readme_yaml/<folder>.yaml the README.yaml to place in each Ceph source folder at cut-over
  the GENERATED blocks of ../LAYOUT.md and ../MIGRATION_PLAN.md

    python3 build_plan.py                     # from the dated sizes
    python3 build_plan.py --census /rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/census.tsv
"""
import argparse
import csv
import io
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DPROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(DPROOT, "lib"))
import mini_yaml  # noqa: E402

HOME = "/wsu/home/go/go24/go2432"
RS = "/rs/rs_grp_oschome/go2432"
DATA = RS + "/data"
GENERATED_ON = "2026-10-08"

# ---------------------------------------------------------------------------------------------------------------
# Rules. Every HOME imaging entry of disk_map.csv must match exactly one rule (checked at the end). A rule gives:
#   folder  the source folder under $RS/data (one per upstream release; derived banks under their source;
#           banks of several sources under multisource_banks)
#   role    raw | converted | derived | labels | meta
#   action  move | move_with_parent | split | container | gone | inspect | keep_symlink | optional_move | stay
#           (stay: listed on purpose and kept on HOME; a stay row with a batch is listed in that batch's section)
#   batch   the migration batch
#   cand    a deletion candidate for Greg (reason), never acted on by this plan
# ---------------------------------------------------------------------------------------------------------------
RECLAIM_A = {"ctspine1k", "ctpelvic1k", "hf_export_v2_work", "hf_export_v3_work", "hf_export_v4", "hf_export_v5",
             "hf_export_osc", "zenodo_v6", "zenodo_upload"}
RECLAIM_B = {"placed", "v5_final", "v5_smoke", "s1_recarve", "hardware_final", "hardware_final_predust", "hardware_fix",
             "fix_0816", "fix_0816_v3", "fix_0816_v4", "fix_0816_pseudo", "fix_0816_pseudo_work", "hip_crossover_backup",
             "hip_transpose_backup", "thoracic_fix", "hf_export_v6", "zenodo_v7"}

R = OrderedDict()


def rule(paths, folder, role, batch, action="move", cand="", hazard="", note="", leaf=None, cand_gb=None, shared_gb=None,
         group=False, restricted=False, irreplaceable=False):
    """shared_gb: bytes (GB) of this item that are hard links into another moved item, so not freed twice;
    group: copy in the batch's one hard-link-group rsync; restricted: DUA/EULA pixels inside (owner-only on Ceph);
    irreplaceable: no public copy to fetch again (finalize hashes every file before deleting the HOME original)."""
    for p in paths if isinstance(paths, (list, tuple)) else [paths]:
        R[p] = dict(folder=folder, role=role, batch=batch, action=action, cand=cand, hazard=hazard, note=note, leaf=leaf,
                    cand_gb=cand_gb, shared_gb=shared_gb, group=group, restricted=restricted, irreplaceable=irreplaceable)


H = HOME + "/"
CT = H + "CTSpinoPelvic1K/data/"
SD = H + "spine-detector/data/raw/"

# -- B14: the entries no file named on 2026-10-07 (the 14 HOME rows of role "unknown", ~/data/spondy_landmark and
#    $RS/data/morphdef), read on the grid on 2026-10-08 (scratchpad inspect_unknown.out; MIGRATION_PLAN.md section 5,
#    B14). Migration jobs already read the item files of B00-B09 on the grid, so no batch B00-B11 gains or loses an
#    item: the imaging-derived entries move in B14 into the folders of their sources, and the entries that are not
#    imaging (software, molecular simulation, documents of an earlier project, a token file) stay on HOME (action
#    stay). Two download leftovers the inspection did not reach, and ~/spinopelvic-seg/nnunet/raw, stay inspect-only.
INSP = "grid inspection 2026-10-08 (inspect_unknown.out)"
rule(H + "data/spondy_landmark", "mendeley_5jdfdgp762", "raw", "B14",
     cand="duplicate of ~/spine-detector/data/raw/mendeley_716 (B04): the same Mendeley release file, Dataset.zip "
          "43,892,677 B; compare the sha256 that files.json records before deleting",
     note="Mendeley Data 5jdfdgp762 'Spondylolisthesis Vertebral Landmark' (CC BY 4.0): Dataset.zip 43,892,677 B (mtime "
          "2025-06-20), url.txt, files.json, an empty dl.log and the unpacked x/Dataset/{Train,Test} (jpg); folder "
          "2026-09-19 13:03. Plain film, not a CT root (tools/ct_inventory.py lists it as one). Zip and x/ move as one "
          "item; " + INSP)
rule(H + "s1v11", "ctspinopelvic1k_build_tree", "derived", "B14", irreplaceable=True, restricted=True,
     hazard="(1) owner-only until read: it holds the Zenodo v11 upload scripts, state and replies (zenodo_v11.py, "
            "upload_zip.sh, zenodo_v11_state.json, upload_reply.json); check them for a token before publish_visibility "
            "opens it. (2) out/v11_labels may share inodes with ~/data/CTSpinoPelvic1K/labels (B02): how the v11 labels "
            "reached the working copy is not recorded; preflight's multilink_files shows it, verify_transfer then fails "
            "on the link count, and the rerun takes ALLOW_NLINK_LOSS=1 (the labels are then stored twice on Ceph)",
     note="the CTSpinoPelvic1K v11 build workspace, 2026-09-11..18: scripts/ (merge_s1_into_sacrum.py, audit_s1_carve.py, "
          "check_s1_merge.py, extract_surgical_morphometrics.py, compare_v10_v11_spinopelvic.py), logs of jobs 40198228, "
          "40198880, 40309073, 40309160, out/v11_labels (the v11 labels), out/s1_carve_audit.csv, "
          "morphometrics/surgical_morphometrics.csv, out/dataset_labels_v11.json ('S1 (29) retired'), and the Zenodo "
          "v11 upload (labels.zip 883,912,953 B, HTTP 201 on 2026-09-18 22:46, md5 744281a5f824494123396386cfe940b8); "
          + INSP)
for u, what in (("pitest", "ten label files (0024, 0182, 0375, 0401, 0569, 0624, 0760, 1043, 1084, 1129), 13,899,387 B, "
                           "dated 2026-09-10 11:38"),
                ("pdwtest", "two label files (0010, 0038), 2,710,749 B, dated 2026-09-10 16:09")):
    rule(H + u, "ctspinopelvic1k_build_tree", "derived", "B14", leaf="scratch_2026-09-10/" + u,
         cand="scratch copies of release label files from the 2026-09-10 spinopelvic work; not yet compared with the "
              "release labels",
         hazard="may be hard links of release label files (not recorded): the same link-count check as ~/s1v11",
         note="CTSpinoPelvic1K %s; the 2026-09-10 spinopelvic investigation: pitest holds the ten cases of ~/pi_ostk2.csv "
              "(pelvic_incidence, method pi-v1, every row flagged identity_violation) and pdwtest the two cases ~/pdw_why.py "
              "reads (docstring: where does ostk.morphometry.pedicle_widths bail on released volumes?); %s"
              % (what, INSP))
# the record of that investigation, three files at the top of HOME, move beside the label copies
for u, what in (("pdw_why.py", "1,761 B, 2026-09-10 16:00, the pedicle-width probe over pdwtest"),
                ("pi_ostk2.csv", "662 B, 2026-09-10 11:46, pelvic incidence for the ten pitest cases"),
                ("ostk_level_morphometry.csv", "302,994 B, 2026-09-10 05:11, the per-level morphometry run of that morning")):
    rule(H + u, "ctspinopelvic1k_build_tree", "derived", "B14", leaf="scratch_2026-09-10/" + u,
         note="CTSpinoPelvic1K spinopelvic investigation of 2026-09-10: %s (read on the grid 2026-10-08)" % what)
rule(H + "qc.tar.gz", "ctspinopelvic1k_build_tree", "derived", "B14", leaf="qc_2026-06-12.tar.gz",
     note="CTSpinoPelvic1K pelvis-propagation QC PNGs, 196,147,947 B, dated 2026-06-12; member names "
          "(qc/<token>_<TCIA COLONOG series UID>_propagation.png) are what ctsp scripts/viz_propagation.py writes (first "
          "committed 2026-06-12); not the speckle QC (qc_speckle/, 2026-08); renamed with its date (a bare qc.tar.gz says "
          "nothing in a shared folder); " + INSP)
rule(H + "dis_renders", "xrspinopelvic1k", "derived", "B14", restricted=True,
     hazard="BUU EULA (presumed): the five PNGs carry BUU-LSPINE film ids, so they are treated as holding BUU pixels: "
            "owner-only",
     cand="scratch from the XRSpinoPelvic1K period: five PNGs named by BUU films (10,869,856 B); what drew them is not recorded",
     note="0008-M-022Y1, 0012-F-013Y1, 0013-M-022Y1, 0015-M-020Y1, 0016-F-023Y1 (.png), 2026-08-11 12:52; "
          "~/spinesurg-ct-nnunet/disputed_renders holds VerSe PNGs, not these; " + INSP)
rule(H + "Multi-View-Vertebra", "", "", "B14", action="stay",
     note="software, not imaging: git clone of github.com/ShanghaiTech-IMPACT/Multi-View-Vertebra-Localization-and-"
          "Identification-from-CT-Images (MICCAI 2023 reference code; HEAD c290796 2024-09-19), cloned 2026-09-13; 15 .py "
          "and one png; " + INSP)
rule(H + "docs", "", "", "B14", action="stay",
     note="documents of an earlier spine-level project, not imaging: ten files dated 2026-02-12, 'Bulletproof Weak Label "
          "Generation v4.0' (README.md, START_HERE.txt, QUICK_REFERENCE.md, ...); the generate_weak_labels_enhanced.py they "
          "describe is not in the folder; " + INSP)
for u, what in (("3", "out_GEMC_equil.dat (19,697,944 B), 2024-03-17"),
                ("6", "out_GEMC_equil.dat (19,697,947 B), 2024-03-17"),
                ("ada", "GOMC 2.75 Gibbs-ensemble production inputs, checkpoint and log (run started 2024-02-19)"),
                ("output", "output/CHARMM: CHARMM topology, parameter, structure and restraint files, 2023-04-24"),
                ("v", "a gzip file dated 2024-02-17 (GOMC bd/ outputs per the grid reading)")):
    rule(H + u, "", "", "B14", action="stay", note="molecular simulation (GOMC, CHARMM), not imaging: %s; %s" % (what, INSP))
rule(H + "github", "", "", "B14", action="stay",
     hazard="SECURITY: a plain-text file holding a GitHub personal access token (mode 644 until 2026-10-08, now 600). "
            "Greg rotates the token and deletes the file; never copy, print or move its content",
     note="a credential, not data; " + INSP)
rule(RS + "/data/morphdef", "", "", "B14", action="stay",
     cand="three empty folders (logs/, out/, src/) made 2026-09-23 02:15, the scaffold of the morphology-deformation work "
          "that was stopped that morning before anything was built (memory note morphology-deformation-feasibility); remove",
     note="CEPH, empty: nothing to index and no README.yaml; " + INSP)
for u, d in (("to_greg.zip?origin_team=T5G027G83", "304K, 2022-05-26"), ("view?usp=sharing", "256K, 2022-01-26")):
    rule(H + u, "", "", "B14", action="inspect",
         note="download leftover (%s); not reached on 2026-10-08 (the inspection's leftover filter matched archive "
              "extensions, and this name ends in a URL query): read it in a job with file and head" % d)

# -- mixed trees: code stays on HOME, their data subfolders move individually
rule(H + "CTSpinoPelvic1K", "", "", "-", action="split", note="git checkout stays on HOME; data/* rows move individually")
rule(H + "VerSeFusion", "", "", "-", action="split", note="git checkout stays on HOME; data/ moves as one unit (unified/ holds links into raw/ and canonical/)")
rule(H + "XRSpinoPelvic1K", "", "", "-", action="split", note="git checkout stays on HOME; data/BUU-LSPINE, data/dataset2024.zip, data/xrsp1k move")
rule(H + "spine-detector", "", "", "-", action="split", note="git checkout stays on HOME; data/raw/* and data/{interim,yolo*} move; runs/ stays (results)")
rule(H + "spinesurg-ct-nnunet", "", "", "-", action="split", note="this repository stays on HOME; nnunet/raw moves (B12); nnunet/results is optional (B13)")
rule(H + "data", "", "", "-", action="container", note="stays as a directory that holds the symlinks of its children")
rule(RS + "/data", "", "", "-", action="keep", note="the layout root")

# -- B01 TCIA CT COLONOGRAPHY (largest single raw tree)
rule(CT + "tcia", "tcia_ct_colonography", "raw", "B01", hazard="state after 2026-09-01 unknown (not on either reclaim list)")
rule(CT + "tcia_nifti", "tcia_ct_colonography", "converted", "B01", cand="regenerable from tcia/ by dcm2niix (336 GB)")
for f in ["patient_db.json", "patient_db.pkl", "patient_db_summary.txt"]:
    rule(CT + f, "tcia_ct_colonography", "meta", "B01")

# -- B02 the CTSpinoPelvic1K release working copy and the build tree (one hard-link group)
rule(H + "data/CTSpinoPelvic1K", "ctspinopelvic1k", "converted", "B02", group=True, irreplaceable=True,
     hazard="hard links: the 802 CTs were hard-linked from ~/CTSpinoPelvic1K/data/hf_export_osc/ct (CTSpinoPelvic1K-1 "
            "slurm/archive_build_inputs.sh L73); transfer with the B02 group in one rsync -aH call; the v11 labels are on no "
            "public mirror (HF is v10)",
     note="HF_EXPORT_DIR for Dataset810/813/815 containers; keep the symlink at the old path")
rule(CT + "hf_export", "", "", "B02", action="gone", note="deleted by 2026-09-23 (DATA_COMPLETENESS_AUDIT.md L140-L143)")
rule(CT + "hf_export_v3", "", "", "B02", action="gone", note="deleted (MANIFEST_DATA_MODELS_RESULTS.md L197-L200)")
for leaf in sorted(RECLAIM_A | RECLAIM_B | {"hf_export_v2", "0816_label_v4.nii.gz", "fix_0816_pseudo_work"}):
    if leaf in ("ctspine1k", "ctpelvic1k"):
        continue
    why = ("on reclaim phase A" if leaf in RECLAIM_A else "on reclaim phase B" if leaf in RECLAIM_B else "superseded build intermediate")
    rule(CT + leaf, "ctspinopelvic1k_build_tree", "derived", "B02", group=True,
         cand="%s; the build archive (Zenodo 22647933) replaces it" % why,
         shared_gb=192.813 if leaf == "hf_export_osc" else None,
         hazard=("presumed deleted: a memory note says reclaim phases A and B ran on 2026-09-07 (mem:zenodo-deposit.md L30); "
                 "preflight decides. Hard links: ship_v5.sh (cp -al), build_v6.py, build_v3_totalseg.py, intensity_refine.py "
                 "and pseudolabel.py (os.link) link files between these folders" +
                 ("; its ct/ shares 192,813,331,872 B of inodes with ~/data/CTSpinoPelvic1K" if leaf == "hf_export_osc" else "")))
for b in ["build_archive", "build_archive_private", "build_archive_stage"]:
    rule(H + b, "ctspinopelvic1k_build_tree", "derived", "B02", group=True, cand="staging of the published build archive (Zenodo 22647933)",
         hazard="hard links: archive_build_inputs.sh stages the release inputs by link")

# -- B03 HOME copies of CTSpine1K and CTPelvic1K
rule(CT + "ctspine1k", "ctspine1k", "raw", "B03", leaf="home_copy",
     cand="duplicate of $RS/data/ctspine1k (152 GB, sha256-verified 2026-09-23); on reclaim phase A",
     hazard="presumed deleted (reclaim phase A ran 2026-09-07 per mem:zenodo-deposit.md L30)")
rule(CT + "ctpelvic1k", "ctpelvic1k", "raw", "B03", cand="on reclaim phase A; re-downloadable from Zenodo 4588403",
     hazard="presumed deleted (reclaim phase A ran 2026-09-07 per mem:zenodo-deposit.md L30)")

# -- B04 plain-film raw corpora (keep the path fragments tools/patient_keys.py reads: /raw/<name>/)
rule(SD + "csxa", "csxa_cervical_xray_atlas", "raw", "B04")
rule(SD + "buu_full", "buu_lspine_3600", "raw", "B04", hazard="BUU EULA: no redistribution; restrict group read")
rule(SD + "buu_drive", "", "", "B04", action="gone", note="deleted by slurm/disk_cleanup.sh (absent on 2026-09-23)")
rule(SD + "buu_v1", "buu_lspine_v1_smoke", "raw", "B04", cand="38 images byte-identical to buu_full")
rule(SD + "buu_2000", "", "", "B04", action="keep_symlink", note="symlink to ~/XRSpinoPelvic1K/data/BUU-LSPINE; resolves through the B05 symlink")
rule(SD + "nhanes_annotated", "nhanes2_zenodo_landmarks", "raw", "B04", cand="extracted pickles 159 GB regenerate from the 1.0 GB zip")
rule(SD + "nhanes_full", "nhanes2_cdc_films", "raw", "B04")
rule(SD + "vindr/1.0.0", "vindr_spinexr", "raw", "B04", action="move_with_parent", note="moves with ~/spine-detector/data/raw/vindr")
rule(SD + "vindr", "vindr_spinexr", "raw", "B04", hazard="PhysioNet DUA, named person: mode 0700, never group-readable")
rule(SD + "aasce", "aasce2019_boostnet", "raw", "B04", note="differs from the CEPH mirror in 98 challenge-test files; keep both")
rule(SD + "mendeley_716", "mendeley_5jdfdgp762", "raw", "B04")
rule(SD + "lateral_236", "ieee_dataport_lateral_fullspine_236", "raw", "B04")
rule(SD + "spinal_ai2024", "spinal_ai2024", "raw", "B04")
rule(SD + "cm_spine", "cm_spine_drive_file", "raw", "B04", cand="empty directory")
rule(H + "spine-detector/data/interim", "spine_detector_corpus", "derived", "B04", restricted=True,
     hazard="holds BUU-LSPINE (EULA) and VinDr-SpineXR (DUA) films: owner-only on Ceph",
     note="added row: named by MANIFEST_DATA_MODELS_RESULTS.md 5.3 and 8")
rule(H + "spine-detector/data/yolo*", "spine_detector_corpus", "derived", "B04", group=True, restricted=True,
     hazard="holds BUU-LSPINE (EULA) and VinDr-SpineXR (DUA) crops: owner-only; the banks likely share files by hard link "
            "(tools/data_alias.py builds its fixture on yolo_v3/yolo_v4z), so they copy as one group",
     note="added row: data/yolo, yolo_v2..v6f, yolo_hw (MANIFEST 5.3; tools/film_corpus_inventory.py YOLO_BANKS)")

# -- B05 XRSpinoPelvic1K data
rule(H + "XRSpinoPelvic1K/data/BUU-LSPINE", "buu_lspine_2000", "raw", "B05", hazard="BUU EULA", note="added row: named by DATA_COMPLETENESS_AUDIT re-count")
rule(H + "XRSpinoPelvic1K/data/dataset2024.zip", "buu_lspine_2000", "raw", "B05", cand="the zip of the extracted BUU-LSPINE (4,023,726,207 B); the same file is on the laptop")
rule(H + "XRSpinoPelvic1K/data/xrsp1k", "xrspinopelvic1k", "derived", "B05", note="added row: 6,416 DRRs (MANIFEST 2.3)")

# -- B06 VerSe and VerSeFusion
rule(H + "VerSeFusion/data", "versefusion", "raw", "B06", leaf="VerSeFusion_data",
     note="added row: moves as one unit (raw = verse19_20 OSF download, canonical, unified links, corrected, qc)",
     hazard="unified/ is 88 MB of links: check absolute vs relative with find -type l -lname '/*' first")
for sub in ["raw", "canonical", "unified"]:
    rule(H + "VerSeFusion/data/" + sub, "versefusion", "raw", "B06", action="move_with_parent", note="moves with ~/VerSeFusion/data")
for b in ["vf_813", "vf_813_probe", "vf_v10", "verse_drr", "verse_drr_film", "verse_drr_obl", "verse_drr_obl2", "verse_soft_drr",
          "ctsp_drr_obl", "ctsp_drr_obl2", "obl2_fov96_ctx", "verse_only_ctx", "implant_verse"]:
    cand = {"ctsp_drr_obl": "misnamed VerSe renders; verse_drr_obl replaces them (AUDIT L247-L248)",
            "ctsp_drr_obl2": "misnamed VerSe renders; verse_drr_obl2 replaces them",
            "verse_soft_drr": "row-spacing defect on 181 of 374; re-render or retire (AUDIT L252-L253)",
            "implant_verse": "187 GB synthetic, regenerable by tools/make_implant_ct.py"}.get(b, "")
    rule(H + b, "versefusion", "derived", "B06", cand=cand)

# -- B07 TotalSegmentator
rule(H + "data/TotalSegmentator", "totalsegmentator_v201", "raw", "B07",
     hazard="$RS/data/validation_ts symlinks point at $HOME/data/TotalSegmentator/<s>/ct.nii.gz: keep the HOME symlink",
     cand="keeps both the 23.6 GB zip and the unpacked tree (the zip is the candidate)", cand_gb=23.6)
rule(H + "data/TotalSegmentator_v3", "totalsegmentator_v300", "raw", "B07", cand="keeps both the 37.4 GB zip and the unpacked tree (the zip is the candidate)", cand_gb=37.4,
     hazard="tools/data_manifest.py ROOTS ts_subjects and ~/model_night/ts_clean_subjects.txt name this path")
rule(H + "ts_drr", "totalsegmentator_v201", "derived", "B07")
rule(H + "ts_drr_v3", "totalsegmentator_v300", "derived", "B07", cand="no bank or arm reads it (AUDIT L360-L363)")
rule(H + "implant_ts", "totalsegmentator_v201", "derived", "B07", cand="unfinished: 355 subjects never processed")

# -- B08 other CT raw on HOME
rule(H + "data/rsna_cspine", "rsna_2022_cspine", "raw", "B08", cand="203 GB zip used by nothing; every study refused by the header census")
rule(H + "data/ribs", "ribfrac", "raw", "B08", note="RibFrac zips, RibSeg v2, Moller masks")
# ~/data/spondy_landmark was an inspect-only row of B08 (never in B08.tsv); identified 2026-10-08, it moves in B14

# -- B09 FluoroCap and FluoroGen
rule(H + "FluoroCap", "fluorocap", "raw", "B09", irreplaceable=True,
     hazard="~/.fluorocap (credentials) is a separate entry and stays on HOME; the literature harvest cannot be rebuilt bit for bit",
     cand="directive D1 dropped FluoroCap from training; youtube/ (181 GB per AUDIT.json, 265 GB per MANIFEST) is the candidate", cand_gb=181.0)
for sub in ["youtube", "pdf", "panels", "raw"]:
    rule(H + "FluoroCap/" + sub, "fluorocap", "raw", "B09", action="move_with_parent", note="moves with ~/FluoroCap")
for b in ["fluorocap_drr", "fluorocap_drr_smoke", "fluorocap_fov96_ctx", "fluorocap_pack"]:
    rule(H + b, "fluorocap", "derived", "B09")
rule(H + "fluorocap_patient_keys.json", "fluorocap", "meta", "B09", irreplaceable=True)
rule(H + "fluorogen", "fluorogen_synthetic", "derived", "B09", cand="synth_rare (9.0 GB) is in no bank")

# -- B10 single-source derived banks
for b in ["ctsp_drr", "ctsp_drr_film", "height_renders", "lstv_eval", "ped_renders", "physics_smoke", "postop_render", "postop_smoke",
          "render_smoke", "rib_fragments_release", "rib_fragments_v4", "exp3_fluoro", "exp3_radiograph", "exp3_ctx_fluoro", "exp3_ctx_radiograph"]:
    rule(H + b, "ctspinopelvic1k", "derived", "B10", cand="smoke test" if "smoke" in b else "")
for f in ["ctsp_patient_crosswalk.csv", "ctsp_vid2patient.json"]:
    rule(H + f, "ctspinopelvic1k", "meta", "B10", irreplaceable=True)
for b in ["carm_drr", "carm_fov96_ctx", "carm_base_cache", "carm_base_cache_v9"] + ["carm_cv%d_drr" % i for i in range(5)] + \
         ["carm_cv%d_fov96_ctx" % i for i in range(5)] + ["carm_cvday%d_drr" % i for i in range(3)] + ["carm_cvday%d_fov96_ctx" % i for i in range(3)]:
    rule(H + b, "carmlspine", "derived", "B10", cand="cache (regenerable)" if b.startswith("carm_base_cache") else "",
         hazard="built from the pre-repair 296-frame C-ArmLSpine bank (the bank behind the published numbers)")
rule(H + "rx_cobra_scratch", "cobra2026", "derived", "B10")
rule(H + "deepfluoro", "deepfluoro_h5", "raw", "B00", note="pilot batch: small, one source, hashed root in RSNAI_DATA_MANIFEST.json",
     hazard="~/user/diffdrr_data is a symlink to ~/deepfluoro/data; it resolves through the new symlink")
rule(H + "deepfluoro/unpacked_full", "deepfluoro_h5", "raw", "B00", action="move_with_parent", note="moves with ~/deepfluoro")
for b in ["films_ap_drr", "buu_fov96_ctx", "buu_yolo"]:
    rule(H + b, "buu_lspine_3600", "derived", "B10", hazard="BUU EULA")
rule(H + "films_smoke", "csxa_cervical_xray_atlas", "derived", "B10", cand="3-film smoke test")
for b in ["nhanes_drr", "nhanes_ctx", "nhanes_split_ctx"]:
    rule(H + b, "nhanes2_zenodo_landmarks", "derived", "B10")
for b in ["nhanes_pseudo", "nhanesps_fov96_ctx"]:
    rule(H + b, "nhanes2_cdc_films", "derived", "B10")
rule(H + "nhanes_pvariant_strata.json", "nhanes2_cdc_films", "meta", "B10")
for b in ["vindr_det_drr", "vindr_fov96_ctx", "vindr_pseudo", "vindr_pseudo_drr", "vindrps_fov96_ctx"]:
    rule(H + b, "vindr_spinexr", "derived", "B10", hazard="PhysioNet DUA: mode 0700")
for f in ["vindr_lat_ids.txt", "vindr_variant_audit.json", "vindr_views.csv"]:
    rule(H + f, "vindr_spinexr", "meta", "B10", hazard="PhysioNet DUA: mode 0700")
for b in ["aasce_drr", "aasce_fov96_ctx"]:
    rule(H + b, "aasce2019_boostnet", "derived", "B10")
for b in ["mendeley_drr", "mendeley_fov96_ctx"]:
    rule(H + b, "mendeley_5jdfdgp762", "derived", "B10")
for b in ["lateral236_pseudo", "lat236ps_fov96_ctx"]:
    rule(H + b, "ieee_dataport_lateral_fullspine_236", "derived", "B10")
rule(H + "spinalai_drr", "spinal_ai2024", "derived", "B10")
rule(H + "polypose", "polypose", "derived", "B10", leaf="polypose_home", note="the HOME working dir of the PolyPose chain")

# -- B11 banks of several sources
for b in ["allspine_fov96_ctx", "allspine_v6_fov96_ctx", "allspine_v7_fov96_ctx", "allspine_v7nofluoro_fov96_ctx", "allspine_v8_fov96_ctx",
          "allspine_v9_fov96_ctx", "anchor_drr", "anchor_drr_c2", "bench_ts", "carm_cvdaymix0_fov96_ctx", "carm_cvdaymix0_v9_fov96_ctx",
          "carm_cvdaymix1_fov96_ctx", "carm_cvdaymix2_fov96_ctx", "carm_cvmix0_fov96_ctx", "carm_cvmix1_fov96_ctx", "carm_cvmix2_fov96_ctx",
          "carm_cvmix3_fov96_ctx", "carm_cvmix4_fov96_ctx", "carm_mix_fov96_ctx", "cut_physics", "cut_physics_v2", "cut_rare", "cut_rare_v2",
          "extra_fov96_ctx", "film_style_ds", "films_all2_fov128m_ctx", "films_all2_fov96_ctx", "films_ann_fov96_ctx", "films_drr",
          "films_drr_buucorr", "implant_ct_smoke", "implant_verse_smoke", "m_fov96_ctx", "m_mask22_scale_ctx", "merged_ctx",
          "mv_bands", "physics_drr", "physics_drr_film", "physics_rare", "physics_rare_film", "pseudo_filtered", "quiz_pack",
          "reader_study", "review_pack", "review_pack_smoke", "review_pack_v2", "sacrum_yolo", "scaling", "sd_fov96_ctx",
          "verify_bench", "verse_ctx", "verse_only_ctx_plus_nh", "yolo_levels"]:
    cand = {"films_all2_fov128m_ctx": "empty directory", "review_pack_smoke": "smoke test", "implant_ct_smoke": "smoke test",
            "implant_verse_smoke": "smoke test", "scaling": "129 GB subset banks for the scaling curves (regenerable by tools/subset_bank.py)",
            "allspine_fov96_ctx": "superseded by allspine_v9", "allspine_v6_fov96_ctx": "superseded by allspine_v9",
            "allspine_v7nofluoro_fov96_ctx": "FluoroCap ablation only"}.get(b, "")
    hz = ("HOLDOUT: 57 references supply allspine_v7_fov96_ctx as the holdout bank (memory note grid-quota-and-deleted-banks); "
          "it must stay readable at the old path") if b == "allspine_v7_fov96_ctx" else ""
    rule(H + b, "multisource_banks", "derived", "B11", cand=cand, hazard=hz)
rule(H + "lstv_flag", "", "", "-", action="split",
     note="MIXED: renders* and smoke move (B11); models/ and the LSTV flag results stay on HOME (MANIFEST_DATA_MODELS_RESULTS.md 8)")
for sub in ["renders", "renders_verse", "renders_ctrl", "smoke"]:
    rule(H + "lstv_flag/" + sub, "multisource_banks", "derived", "B11", leaf="lstv_flag/" + sub,
         cand="smoke test" if sub == "smoke" else "", note="added row: lstv_flag render folder (corpus_census.md 3)")
for f in ["bank_splits.json", "patient_keys.json", "patient_keys_final.json", "patient_keys_final.20260923_191858.json",
          "patient_keys_final.20260923_193933.json", "patient_keys_v9.json", "split_final.json"]:
    rule(H + f, "multisource_banks", "meta", "B11", irreplaceable=True,
         hazard="identity tables read by the evaluation gate: keep the HOME symlink")

# -- B12 nnU-Net raw tree; B13 optional (not imaging)
rule(H + "spinesurg-ct-nnunet/nnunet/raw", "", "", "-", action="stay",
     hazard="Dataset810/813/815 imagesTr are container-path links (/data/hf_export/...): never rewrite them",
     note="stays on HOME (B12 dropped 2026-10-08): fifteen nnU-Net slurm scripts bind ${PROJECT_ROOT}/nnunet and no Ceph "
          "path, so a symlinked nnunet/raw would dangle inside their containers; it frees almost nothing (symlinks + "
          "labelsTr). nnunet/preprocessed was deleted (DATA_COMPLETENESS_AUDIT.md lines 103, 404)")
rule(H + "spinopelvic-seg/nnunet/raw", "", "", "B14", action="inspect",
     note="spinopelvic-seg README sets nnUNet_raw=$PWD/nnunet/raw (Dataset803 imagesTr, labelsTs): imaging-derived; the census "
          "must show its size and link type before it is mapped or excluded")
rule(H + "spinesurg-ct-nnunet/nnunet/results", "", "result", "B13", action="optional_move", leaf="nnunet_results",
     note="348.6 GB of nnU-Net results (not imaging); target $RS/results/nnunet_results if Greg decides to move it")
rule(H + "ablate", "", "result", "B13", action="optional_move", note="234.8 GB nnU-Net ablation arrays (not imaging); target $RS/results/ablate")
rule(H + "bench", "", "result", "B13", action="optional_move",
     note="44 GB benchmark harness; ct_by_case is 802 symlinks into the CT store; target $RS/results/bench")


def target_of(path, r):
    if r["action"] in ("split", "container", "gone", "inspect", "keep_symlink", "keep", "stay"):
        return ""
    if r["action"] == "optional_move":
        return RS + "/results/" + (r.get("leaf") or os.path.basename(path.rstrip("/")))
    if r["action"] == "move_with_parent":
        parents = [p for p, pr in R.items() if pr["action"] == "move" and path.startswith(p.rstrip("/") + "/")]
        if parents:
            parent = max(parents, key=len)
            return target_of(parent, R[parent]) + path[len(parent.rstrip("/")):]
    leaf = r.get("leaf") or os.path.basename(path.rstrip("/"))
    if leaf.endswith("*"):
        leaf = leaf  # wildcard row, expanded at transfer time
    return "%s/%s/%s/%s" % (DATA, r["folder"], r["role"], leaf)


def gb(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_census(path):
    if not path:
        return {}
    out = {}
    with open(path, encoding="utf-8") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        cols = {c.lower(): c for c in (rd.fieldnames or [])}
        pc = cols.get("path")
        if not pc:
            raise SystemExit("census: no 'path' column in %s" % path)
        for row in rd:
            v = None
            for k, scale in (("gb", 1.0), ("bytes", 1e-9), ("size_bytes", 1e-9), ("kb", 1e-6), ("kib", 1024 * 1e-9)):
                if k in cols and row.get(cols[k]) not in (None, ""):
                    try:
                        v = float(row[cols[k]]) * scale
                    except ValueError:
                        v = None
                    break
            if v is not None:
                out[row[pc].rstrip("/")] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--census", default="", help="census.tsv from the 2026-10-07 storage census")
    ap.add_argument("--check", action="store_true", help="only check that every imaging row has a rule")
    a = ap.parse_args()
    census = load_census(a.census)
    sources = json.load(open(os.path.join(DPROOT, "sources.json"), encoding="utf-8"))
    S = OrderedDict((e["id"], e) for e in sources["sources"])
    folder_ids = defaultdict(list)
    for e in S.values():
        folder_ids[e["layout"]["folder"]].append(e["id"])

    rows = list(csv.DictReader(open(os.path.join(HERE, "disk_map.csv"), encoding="utf-8")))
    imaging = [r for r in rows if r["role"] in ("raw imaging source", "converted or derived imaging", "unknown") or r["path"] in R]
    # rows the disk map does not hold but the plan must carry (children named by the manifests)
    extra = [p for p in R if p not in {r["path"] for r in rows}]
    out, missing = [], []
    for r in imaging + [dict(path=p, storage="CEPH" if p.startswith(RS) else "HOME", role="(added row)", source_id="",
                             size_gb="", size_source="", date="", notes="added: not a disk-map row") for p in extra]:
        p = r["path"]
        rr = R.get(p)
        if rr is None and p.startswith(RS):
            rr = dict(folder=os.path.basename(p) if p.startswith(DATA + "/") else "", role="", batch="-", action="keep",
                      cand="", hazard="", note="already on CEPH: stays where it is; write README.yaml", leaf=None)
        if rr is None:
            missing.append(p)
            continue
        size = census.get(p.rstrip("/"), gb(r["size_gb"]))
        basis = "census 2026-10-07" if p.rstrip("/") in census else (r["size_source"] or "not sized")
        sid = (r["source_id"] or "").strip()
        primary = ""
        if rr["folder"] and rr["folder"] in folder_ids and len(folder_ids[rr["folder"]]) == 1:
            primary = folder_ids[rr["folder"]][0]
        elif rr["folder"] == "multisource_banks":
            primary = "multisource_banks"
        elif rr["folder"]:
            ids = [i for i in re.split(r"[;:]", sid) if i and not i.startswith("multi")]
            primary = next((i for i in ids if i in S and S[i]["layout"]["folder"] == rr["folder"]), folder_ids.get(rr["folder"], [""])[0])
        out.append(OrderedDict(
            current_path=p, storage=r["storage"], current_role=r["role"], disk_map_source_id=sid, source_id=primary,
            action=rr["action"], target_path=target_of(p, rr), target_role=rr["role"], batch=rr["batch"],
            est_gb="" if size is None else round(size, 3), size_basis=basis, listing_date=r.get("date", ""),
            deletion_candidate=rr["cand"],
            candidate_gb=("" if not rr["cand"] else rr.get("cand_gb") if rr.get("cand_gb") is not None else ("" if size is None else round(size, 3))),
            hazard=rr["hazard"], note=rr["note"] or r.get("notes", "")[:160],
            shared_gb="" if rr.get("shared_gb") is None else rr["shared_gb"],
            flags_extra=",".join(k for k in ("group", "restricted", "irreplaceable") if rr.get(k))))
    if missing:
        print("IMAGING ROWS WITHOUT A RULE:", len(missing))
        for m in missing:
            print("  ", m)
        if a.check:
            return 2
    if a.check:
        print("every imaging row has a rule:", len(out))
        return 0

    # an unsized parent that moves as one unit takes the sum of its sized move_with_parent children (VerSeFusion/data,
    # spine-detector/data/raw/vindr); the basis says so
    for o in out:
        if o["action"] == "move" and o["est_gb"] == "" and o["target_path"]:
            kids = [k for k in out if k["action"] == "move_with_parent" and k["target_path"].startswith(o["target_path"] + "/")
                    and k["est_gb"] != ""]
            if kids:
                o["est_gb"] = round(sum(float(k["est_gb"]) for k in kids), 3)
                o["size_basis"] = "sum of sized children: " + ", ".join("%s %s" % (os.path.basename(k["current_path"]), k["est_gb"]) for k in kids)
    # restricted: DUA/EULA hazard, or a bank whose sources include VinDr-SpineXR or BUU-LSPINE
    for o in out:
        sid = o["disk_map_source_id"]
        if ("DUA" in o["hazard"] or "EULA" in o["hazard"] or "vindr_spinexr" in sid or "buu_lspine" in sid) and \
                "restricted" not in o["flags_extra"].split(","):
            o["flags_extra"] = ",".join(x for x in (o["flags_extra"], "restricted") if x)

    # ------------------------------------------------------------------ write layout_map.csv
    keys = list(out[0].keys())
    with open(os.path.join(HERE, "layout_map.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for o in sorted(out, key=lambda o: (o["batch"], o["current_path"])):
            w.writerow(o)

    # ------------------------------------------------------------------ batches
    BATCH_TITLES = OrderedDict([
        ("B00", ("pilot: DeepFluoro H5 (small, one source, hashed root)", "")),
        ("B01", ("TCIA CT COLONOGRAPHY raw DICOM and reference NIfTI", "B00")),
        ("B02", ("CTSpinoPelvic1K release working copy + build tree (one hard-link group)", "B00")),
        ("B03", ("HOME copies of CTSpine1K and CTPelvic1K", "B02")),
        ("B04", ("plain-film raw corpora and the spine-detector datasets", "B00")),
        ("B05", ("XRSpinoPelvic1K data (BUU-LSPINE 2000, xrsp1k DRRs)", "B04")),
        ("B06", ("VerSe / VerSeFusion data and VerSe render banks", "B00")),
        ("B07", ("TotalSegmentator v2.0.1 and v3.0.0 and their banks", "B00")),
        ("B08", ("RSNA 2022 cervical, RibFrac zips (spondy_landmark, identified 2026-10-08, moves in B14)", "B00")),
        ("B09", ("FluoroCap and FluoroGen", "B00")),
        ("B10", ("single-source derived banks (CT renders, film banks, C-arm banks)", "B02 B04 B06 B07")),
        ("B11", ("banks of several sources, review packs, identity tables", "B10")),
        ("B12", ("(dropped 2026-10-08: nnunet/raw stays on HOME, its containers bind no Ceph path)", "")),
        ("B13", ("OPTIONAL, not imaging: nnU-Net results, ablations, bench (Greg decides)", "B11")),
        ("B14", ("identified 2026-10-08: moved or left (3 entries still to inspect)", "B02 B04 B05")),
    ])
    agg = OrderedDict((b, dict(items=0, gb=0.0, unsized=0, cand_gb=0.0, inspect=0)) for b in BATCH_TITLES)
    os.makedirs(os.path.join(HERE, "batch_items"), exist_ok=True)
    items_by_batch = defaultdict(list)
    for o in out:
        if o["action"] not in ("move", "optional_move", "inspect"):
            continue
        if o["action"] == "inspect":
            agg[o["batch"]]["items"] += 1
            agg[o["batch"]]["inspect"] += 1
            continue
        agg[o["batch"]]["items"] += 1
        shared = float(o["shared_gb"] or 0.0)
        if o["est_gb"] == "":
            agg[o["batch"]]["unsized"] += 1
        else:
            agg[o["batch"]]["gb"] += max(0.0, float(o["est_gb"]) - shared)       # hard-linked bytes are counted once
            if o["deletion_candidate"]:
                agg[o["batch"]]["cand_gb"] += max(0.0, float(o["candidate_gb"] or 0.0) - shared)
        ex = o["flags_extra"].split(",")
        flags = []
        if "group" in ex:
            flags.append("hardlink_group")
        if "restricted" in ex:
            flags.append("restricted")
        if "irreplaceable" in ex:
            flags.append("irreplaceable")
        if o["current_path"].endswith("*"):
            flags.append("glob")
        if o["deletion_candidate"]:
            flags.append("candidate")
        items_by_batch[o["batch"]].append((o["current_path"], o["target_path"], o["est_gb"], ",".join(flags) or "-"))
    for old in os.listdir(os.path.join(HERE, "batch_items")):      # a batch that lost all its items keeps no stale file
        if old.endswith(".tsv") and old[:-4] not in items_by_batch:
            os.remove(os.path.join(HERE, "batch_items", old))
    for b, items in items_by_batch.items():
        with open(os.path.join(HERE, "batch_items", b + ".tsv"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# src\tdst\test_gb\tflags   (generated %s by build_plan.py; sizes dated, see layout_map.csv)\n" % GENERATED_ON)
            for it in sorted(items, key=lambda t: -(float(t[2]) if t[2] != "" else 0.0)):
                fh.write("\t".join(str(x) for x in it) + "\n")
    with open(os.path.join(HERE, "migration_batches.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["batch", "order", "title", "items", "est_gb_sized", "items_unsized", "deletion_candidate_gb", "depends_on"])
        for i, (b, (t, dep)) in enumerate(BATCH_TITLES.items()):
            g = agg[b]
            w.writerow([b, i, t, g["items"], round(g["gb"], 1), g["unsized"], round(g["cand_gb"], 1), dep])

    # ------------------------------------------------------------------ README.yaml per Ceph source folder
    rdir = os.path.join(HERE, "readme_yaml")
    os.makedirs(rdir, exist_ok=True)
    by_folder = defaultdict(list)
    kept = {o["current_path"][len(DATA) + 1:].split("/")[0] for o in out
            if o["action"] == "keep" and o["current_path"].startswith(DATA + "/") and o["current_path"] != DATA}
    kept.discard("anomaly_harvest")
    for e in S.values():
        if e["status"] == "deleted":
            continue
        if e["status"] in ("on_disk", "on_disk_partial", "on_disk_state_unknown", "on_disk_unidentified", "empty") or \
                any(l["storage"] == "HOME" for l in e["locations"]):
            by_folder[e["layout"]["folder"]].append(e)
        for l in e["locations"]:
            if l["storage"] == "CEPH" and l["path"].startswith(DATA + "/"):
                top = l["path"][len(DATA) + 1:].split("/")[0]
                if top in kept and e not in by_folder[top] and l["role"] in ("raw", "derived", "result"):
                    by_folder[top].append(e)
    acq_folders = {e["layout"]["folder"] for e in S.values() if e["family"] == "B" and e["status"] == "on_disk"} | {"ctpelvic1k_clinic"}
    for k in kept:
        by_folder.setdefault(k, [])
    by_folder["multisource_banks"] = []
    adapters = {"ctspinopelvic1k": "ctsp_manifest", "vindr_spinexr": "vindr_csv", "buu_lspine_3600": "buu", "buu_lspine_2000": "buu",
                "buu_lspine_v1_smoke": "buu", "nhanes2_cdc_films": "nhanes_tiff", "nhanes2_zenodo_landmarks": "nhanes_pickle",
                "csxa_cervical_xray_atlas": "csxa", "realxray": "realxray_meta", "cobra2026": "cobra", "carmlspine": "dicom_tree",
                "totalsegmentator_v201": "totalsegmentator", "totalsegmentator_v300": "totalsegmentator", "versefusion": "verse",
                "multisource_banks": "render_bank", "deepfluoro_vendor": "dicom_tree", "spinesac": "generic",
                "rare_class": "render_bank", "tcia_ct_colonography": "dicom_tree"}
    n_readme = 0
    written = set()
    for folder, ents in sorted(by_folder.items()):
        if not folder:
            continue
        roles = OrderedDict()
        for o in out:
            if o["target_path"].startswith("%s/%s/" % (DATA, folder)) and o["action"] in ("move", "optional_move"):
                rel = o["target_path"][len("%s/%s/" % (DATA, folder)):]
                roles[rel] = o["target_role"]
        restricted = any(e["id"] in ("vindr_spinexr", "buu_lspine_3600", "buu_lspine_2000", "buu_lspine_v1_smoke", "buu_lspine_400_sample")
                         for e in ents)
        restricted_sub = sorted({o["target_path"][len("%s/%s/" % (DATA, folder)):] for o in out
                                 if o["target_path"].startswith("%s/%s/" % (DATA, folder)) and "restricted" in o["flags_extra"].split(",")
                                 and o["action"] in ("move", "optional_move")})
        # a sub-folder closed for another reason than DUA/EULA pixels (~/s1v11: upload scripts not yet read for a token)
        closed_other = sorted({o["target_path"][len("%s/%s/" % (DATA, folder)):] for o in out
                               if o["target_path"].startswith("%s/%s/" % (DATA, folder)) and "restricted" in o["flags_extra"].split(",")
                               and o["action"] in ("move", "optional_move") and "DUA" not in o["hazard"] and "EULA" not in o["hazard"]
                               and "vindr_spinexr" not in o["disk_map_source_id"] and "buu_lspine" not in o["disk_map_source_id"]})
        fam = sorted(set(e["family"] for e in ents))
        is_acq = folder in acq_folders
        doc = OrderedDict(
            folder="%s/%s" % (DATA, folder),
            source_ids=[e["id"] for e in ents] or ["multisource_banks"],
            names=[e["name"] for e in ents] or ["banks built from several sources; each bank's sources are in sources.json and layout_map.csv"],
            families=fam, kind=sorted(set(e["kind"] for e in ents)) or ["derived"],
            licence=sorted(set(e["licence"] for e in ents)) or ["inherits the sources' terms"],
            access=sorted(set(e["access"] for e in ents)) or ["project"],
            restricted=restricted,
            restricted_subfolders=[] if restricted else restricted_sub,
            permissions="0700 (owner only): DUA or EULA" if restricted else (
                ("inherit the oschome tree (drwxr-s---); the restricted_subfolders are owner-only (%s not yet cleared for "
                 "students: see the hazard column of plan/layout_map.csv)" % ", ".join(closed_other))
                if closed_other else
                "inherit the oschome tree (drwxr-s---); the restricted_subfolders hold DUA/EULA pixels and are owner-only"
                if restricted_sub else "inherit the oschome tree (drwxr-s---)"),
            roles=roles,
            existing_subfolders_kept=("acquisition layout: raw/ (role raw), nifti/ (role converted), fetch/ (role meta); "
                                      "the screen lives in ../anomaly_harvest/<collection>/ (role derived)") if is_acq else "",
            index_adapter=("acquisition" if is_acq else adapters.get(folder, "generic")),
            # a second copy of the same release (the HOME copy beside the verified Ceph copy) is not indexed twice
            index_skip=sorted({o["target_path"][len("%s/%s/" % (DATA, folder)):] for o in out
                               if o["target_path"].startswith("%s/%s/" % (DATA, folder)) and o["deletion_candidate"].startswith("duplicate of")}),
            manifest="data_platform/DATA_MANIFEST.md (cards: %s)" % ", ".join(e["id"] for e in ents[:12]) if ents else "data_platform/LAYOUT.md",
            generated=GENERATED_ON, generator="data_platform/plan/build_plan.py")
        with open(os.path.join(rdir, folder + ".yaml"), "w", encoding="utf-8", newline="\n") as fh:
            mini_yaml.dump(doc, fh, header="README.yaml for %s/%s. Read by data_platform/db/build_index.py." % (DATA, folder))
        n_readme += 1
        written.add(folder + ".yaml")
    for old in os.listdir(rdir):          # a folder that no source maps to any more keeps no stale template
        if old.endswith(".yaml") and old not in written:
            os.remove(os.path.join(rdir, old))

    # ------------------------------------------------------------------ code that names each moved HOME path
    refs = list(csv.DictReader(open(os.path.join(HERE, "path_refs_files.csv"), encoding="utf-8")))
    ref_rows = []
    for o in out:
        if o["action"] not in ("move", "optional_move") or not o["current_path"].startswith(HOME + "/"):
            continue
        rel = o["current_path"][len(HOME) + 1:].rstrip("*").rstrip("/")
        glob = o["current_path"].endswith("*")
        files = sorted({"%s:%s" % (x["repo"], x["file"]) for x in refs if x["root"] == "HOME" and
                        (x["subpath"] == rel or x["subpath"].startswith(rel + "/") or (glob and x["subpath"].startswith(rel)))})
        ref_rows.append(OrderedDict(current_path=o["current_path"], batch=o["batch"], n_code_files=len(files), files=" ".join(files)))
    with open(os.path.join(HERE, "path_refs_by_item.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["current_path", "batch", "n_code_files", "files"])
        w.writeheader()
        for rx in sorted(ref_rows, key=lambda rx: -rx["n_code_files"]):
            w.writerow(rx)

    # ------------------------------------------------------------------ generated blocks in the markdown files
    def table(rowsx, cols):
        s = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
        for rx in rowsx:
            s += "| " + " | ".join(str(rx.get(c, "")).replace("|", "/") for c in cols) + " |\n"
        return s

    def short(p):
        return p.replace(HOME, "~").replace(RS, "$RS")

    moves = [o for o in out if o["action"] not in ("keep",)]
    lay_rows = [dict(current=short(o["current_path"]), action=o["action"], target=short(o["target_path"]), batch=o["batch"],
                     gb=o["est_gb"], size_basis=o["size_basis"][:40], candidate=o["deletion_candidate"][:70]) for o in
                sorted(moves, key=lambda o: (o["batch"], o["current_path"]))]
    keep_rows = [dict(path=short(o["current_path"]), folder_role=o["current_role"], source=o["disk_map_source_id"][:50], gb=o["est_gb"])
                 for o in out if o["action"] == "keep"]
    batches = list(csv.DictReader(open(os.path.join(HERE, "migration_batches.csv"), encoding="utf-8")))
    # totals over every batch that moves something by default: B00-B11 and B14 (B13 is optional). An inspect-only
    # entry is counted in its batch's `items` column but moves nothing, so it is left out of the item total.
    counted = [b for b in batches if b["batch"] != "B13"]
    tot = dict(items=sum(int(b["items"]) - agg[b["batch"]]["inspect"] for b in counted),
               gb=sum(float(b["est_gb_sized"]) for b in counted),
               unsized=sum(int(b["items_unsized"]) for b in counted),
               cand=sum(float(b["deletion_candidate_gb"]) for b in counted),
               inspect=sum(agg[b["batch"]]["inspect"] for b in counted))
    blocks = {
        "layout_map": "Generated %s by `plan/build_plan.py` from `plan/disk_map.csv`%s. %d rows; the full table with hazards and notes is "
                      "`plan/layout_map.csv`. `$RS` = `%s`, `~` = `%s`.\n\n" % (
                          GENERATED_ON, " and the census" if census else " (sizes dated: see size_basis)", len(moves), RS, HOME)
                      + table(lay_rows, ["current", "action", "target", "batch", "gb", "size_basis", "candidate"]),
        "ceph_keep": "%d CEPH entries stay where they are; each source folder gets a README.yaml (templates in `plan/readme_yaml/`).\n\n" % len(keep_rows)
                     + table(keep_rows, ["path", "folder_role", "source", "gb"]),
        "batches": "Generated %s. Totals over B00-B11 and B14 (B12 dropped and empty; B13 optional, excluded): %d items to move, %.1f GB sized "
                   "(%.2f TB), %d items unsized, %.1f GB of the sized total are deletion candidates. The `items` column also counts "
                   "inspect-only entries, which move nothing (%d, all in B14); the totals leave them out.\n\n" % (
                       GENERATED_ON, tot["items"], tot["gb"], tot["gb"] / 1000.0, tot["unsized"], tot["cand"], tot["inspect"])
                   + table(batches, ["batch", "order", "title", "items", "est_gb_sized", "items_unsized", "deletion_candidate_gb", "depends_on"]),
        "path_refs": "Code files (both repositories) that name each moved HOME path, from `plan/path_refs_files.csv` (scan of 2026-10-07). "
                     "The symlink left at the old path keeps every one of them working; edit them later, one at a time. Full list with file "
                     "names: `plan/path_refs_by_item.csv`. %d of %d moved items are named by at least one file.\n\n" % (
                         sum(1 for rx in ref_rows if rx["n_code_files"]), len(ref_rows))
                     + table([dict(path=short(rx["current_path"]), batch=rx["batch"], files=rx["n_code_files"],
                                   examples=" ".join(rx["files"].split()[:3]))
                              for rx in sorted(ref_rows, key=lambda rx: -rx["n_code_files"]) if rx["n_code_files"]][:60],
                             ["path", "batch", "files", "examples"]),
        "candidates": table([dict(path=short(o["current_path"]), batch=o["batch"], item_gb=o["est_gb"], candidate_gb=o["candidate_gb"], reason=o["deletion_candidate"])
                             for o in sorted(out, key=lambda o: -(float(o["est_gb"]) if o["est_gb"] != "" else 0.0)) if o["deletion_candidate"]],
                            ["path", "batch", "item_gb", "candidate_gb", "reason"]),
    }
    for md, names in (("LAYOUT.md", ["layout_map", "ceph_keep"]), ("MIGRATION_PLAN.md", ["batches", "candidates", "path_refs"])):
        fp = os.path.join(DPROOT, md)
        if not os.path.exists(fp):
            continue
        txt = io.open(fp, encoding="utf-8").read()
        for n in names:
            pat = re.compile(r"(<!-- BEGIN GENERATED: %s -->\n).*?(<!-- END GENERATED: %s -->)" % (n, n), re.S)
            if not pat.search(txt):
                print("no GENERATED block %s in %s" % (n, md))
                continue
            txt = pat.sub(lambda m: m.group(1) + blocks[n] + m.group(2), txt)
        io.open(fp, "w", encoding="utf-8", newline="\n").write(txt)
    json.dump(dict(totals=tot, batches=batches, readme_yaml=n_readme, rows=len(out), census_rows_used=len(census)),
              open(os.path.join(HERE, "plan_summary.json"), "w"), indent=1)
    print("rows %d; to move %d items, %.1f GB sized, %d unsized; README.yaml %d" % (len(out), tot["items"], tot["gb"], tot["unsized"], n_readme))
    return 0


if __name__ == "__main__":
    sys.exit(main())
