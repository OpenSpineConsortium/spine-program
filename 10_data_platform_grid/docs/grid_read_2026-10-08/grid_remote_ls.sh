#!/bin/bash
# Read-only grid confirmation for INVENTORY 5 (2026-10-08). Only ls, cat of small files, squeue, quota tools.
set +e
H=/wsu/home/go/go24/go2432
RS=/rs/rs_grp_oschome/go2432
echo "=== date"; date -u; hostname
echo "=== pan_quota"; pan_quota 2>&1 | head -5
echo "=== df-ceph"; df-ceph oschome 2>&1 | head -10
echo "=== squeue"; squeue -u go2432 -o "%.10i %.9P %.34j %.2t %.11M %.11l %.5D %R" 2>&1 | head -80
echo "=== ls HOME"; ls -la --time-style=long-iso $H 2>&1
echo "=== ls RS"; ls -la --time-style=long-iso $RS 2>&1
echo "=== ls RS/data"; ls -la --time-style=long-iso $RS/data 2>&1
echo "=== ls RS/data/_index"; ls -la $RS/data/_index 2>&1
echo "=== ls RS/results"; ls -la $RS/results 2>&1
echo "=== ls RS/ruleclass"; ls -la --time-style=long-iso $RS/ruleclass 2>&1
echo "=== ls RS/ruleclass/arms"; ls -la --time-style=long-iso $RS/ruleclass/arms 2>&1
echo "=== ls RS/ruleclass/arms/ts"; ls $RS/ruleclass/arms/ts 2>&1 | head -40
echo "=== ls RS/ruleclass/arms/pelvis"; ls $RS/ruleclass/arms/pelvis 2>&1 | head -40
echo "=== ls RS/ruleclass/arms/moller_fast"; ls $RS/ruleclass/arms/moller_fast 2>&1 | head -40
echo "=== ruleclass ts STATUS.md"; head -80 $RS/ruleclass/arms/ts/STATUS.md 2>&1
echo "=== pelvis DECISION"; ls -la $RS/ruleclass/arms/pelvis/_timing/ 2>&1 | head; head -40 $RS/ruleclass/arms/pelvis/_timing/DECISION.json 2>&1
echo "=== ls RS/data/or_ready"; ls -la --time-style=long-iso $RS/data/or_ready 2>&1
echo "=== ls RS/model_night"; ls -la --time-style=long-iso $RS/model_night 2>&1 | head -60
echo "=== ls RS/data/inventory"; ls -la --time-style=long-iso $RS/data/inventory 2>&1; ls -la --time-style=long-iso $RS/data/inventory/* 2>&1 | head -80
echo "=== ls RS/data/anomaly_harvest"; ls $RS/data/anomaly_harvest 2>&1 | head -80
echo "=== ls RS/data/realxray"; ls -la $RS/data/realxray 2>&1
echo "=== ls RS/data/ctspinopelvic1k"; ls -la $RS/data/ctspinopelvic1k $RS/data/ctspinopelvic1k/converted $RS/data/ctspinopelvic1k/derived 2>&1
echo "=== ls RS/data/ctspinopelvic1k_build_tree"; ls -la $RS/data/ctspinopelvic1k_build_tree $RS/data/ctspinopelvic1k_build_tree/derived 2>&1
echo "=== ls RS/data/tcia_ct_colonography"; ls -la $RS/data/tcia_ct_colonography $RS/data/tcia_ct_colonography/* 2>&1 | head -40
echo "=== ls RS/data/versefusion"; ls -la $RS/data/versefusion $RS/data/versefusion/raw $RS/data/versefusion/derived 2>&1
echo "=== ls RS/data/deepfluoro_h5"; ls -la $RS/data/deepfluoro_h5 $RS/data/deepfluoro_h5/raw 2>&1
echo "=== ls RS/data/ctspine1k ctpelvic1k rsna ribfrac"; ls -la $RS/data/ctspine1k $RS/data/ctspine1k/raw $RS/data/ctpelvic1k $RS/data/rsna_2022_cspine $RS/data/rsna_2022_cspine/raw $RS/data/ribfrac $RS/data/ribfrac/raw 2>&1
echo "=== ls RS/data B04 B05 B07 B09 B10 B11 targets"; for d in nhanes2_zenodo_landmarks nhanes2_cdc_films vindr_spinexr spinal_ai2024 ieee_dataport_lateral_fullspine_236 mendeley_5jdfdgp762 csxa_cervical_xray_atlas buu_lspine_3600 buu_lspine_v1_smoke aasce2019_boostnet cm_spine_drive_file spine_detector_corpus buu_lspine_2000 xrspinopelvic1k totalsegmentator_v201 totalsegmentator_v300 fluorocap fluorogen_synthetic carmlspine multisource_banks _staging; do echo "--- $RS/data/$d"; ls -la --time-style=long-iso $RS/data/$d 2>&1 | head -12; done
echo "=== ls plan/runs"; ls -la --time-style=long-iso $H/spinesurg-ct-nnunet/data_platform/plan/runs 2>&1
echo "=== STATUS files"; for f in $H/spinesurg-ct-nnunet/data_platform/plan/runs/*/STATUS; do echo "--- $f"; cat "$f"; done 2>&1
echo "=== plan/logs"; ls -la --time-style=long-iso $H/spinesurg-ct-nnunet/data_platform/plan/logs 2>&1 | tail -40
echo "=== dedup on grid"; ls -la $H/spinesurg-ct-nnunet/data_platform/dedup/hash_results 2>&1 | head -8; ls -la $H/spinesurg-ct-nnunet/data_platform/dedup/applied 2>&1; ls $H/spinesurg-ct-nnunet/data_platform/dedup/logs 2>&1
echo "=== grid checkout HEAD"; cat $H/spinesurg-ct-nnunet/.git/HEAD 2>&1; cat $H/spinesurg-ct-nnunet/.git/refs/heads/L6_Class 2>&1; cat $H/CTSpinoPelvic1K/.git/HEAD 2>&1; cat $H/CTSpinoPelvic1K/.git/refs/heads/master 2>&1; cat $H/OpenSpineToolkit/.git/HEAD 2>&1; cat $H/OpenSpineToolkit/.git/refs/heads/main 2>&1
echo "=== ls ~/data"; ls -la --time-style=long-iso $H/data 2>&1
echo "=== ls ~/data/CTSpinoPelvic1K"; ls -la --time-style=long-iso $H/data/CTSpinoPelvic1K/ 2>&1 | head -20
echo "=== ls ~/CTSpinoPelvic1K"; ls -la --time-style=long-iso $H/CTSpinoPelvic1K 2>&1 | head -60
echo "=== ls ~/CTSpinoPelvic1K/data"; ls -la --time-style=long-iso $H/CTSpinoPelvic1K/data 2>&1 | head -60
echo "=== ls ~/CTSpinoPelvic1K/morphometrics"; ls $H/CTSpinoPelvic1K/morphometrics 2>&1 | head -40
echo "=== ls ~/spine-detector"; ls -la --time-style=long-iso $H/spine-detector 2>&1 | head -40
echo "=== ls ~/spine-detector/data ~/spine-detector/data/raw"; ls -la --time-style=long-iso $H/spine-detector/data 2>&1 | head -40; ls -la --time-style=long-iso $H/spine-detector/data/raw 2>&1
echo "=== ls ~/spine-detector/runs"; ls $H/spine-detector/runs 2>&1; ls $H/spine-detector/runs/realxray 2>&1 | head -40; ls $H/spine-detector/runs/devcorpus 2>&1 | head -40
echo "=== ls ~/FluoroCap"; ls $H/FluoroCap 2>&1 | head -80
echo "=== ls ~/FluoroCap/releases"; ls -la $H/FluoroCap/releases 2>&1
echo "=== ls ~/model_registry"; ls -la --time-style=long-iso $H/model_registry 2>&1 | head -60
echo "=== aliases"; ls -la $H/model_registry/aliases 2>&1
echo "=== registry.jsonl"; wc -l $H/model_registry/registry.jsonl 2>&1; cut -c1-400 $H/model_registry/registry.jsonl 2>&1 | head -40
echo "=== mlflow"; ls -la $H/mlflow 2>&1 | head
echo "=== ls ~/model_night (head)"; ls $H/model_night 2>&1 | head -120
echo "=== PIPELINE_STATE head"; head -60 $H/model_night/PIPELINE_STATE.md 2>&1
echo "=== ls ~/nnunet raw/results"; ls -la --time-style=long-iso $H/spinesurg-ct-nnunet/nnunet/raw $H/spinesurg-ct-nnunet/nnunet/results 2>&1
echo "=== ls ~/lstv_flag"; ls $H/lstv_flag 2>&1 | head -30
echo "=== ls ~/level_id_service"; ls $H/level_id_service 2>&1 | head -30
echo "=== ls ~/s1v11"; ls -la --time-style=long-iso $H/s1v11 2>&1 | head -40
echo "=== ls ~/bench ~/ablate ~/scaling ~/scaling_curves ~/corpus_final"; ls $H/bench 2>&1 | head -20; ls $H/ablate 2>&1 | head -20; ls $H/scaling 2>&1 | head -20; ls $H/scaling_curves 2>&1 | head; ls $H/corpus_final 2>&1 | head
echo "=== allspine v9 bank"; ls -la --time-style=long-iso $H/allspine_v9_fov96_ctx $H/allspine_v9_fov96_ctx/runs 2>&1 | head -40
echo "=== heads"; ls $H/model_night/heads_mixed $H/model_night/heads_carm 2>&1 | head -40
echo "=== carm fold models"; ls $H/carm_cvmix0_fov96_ctx/runs 2>&1 | head
echo "=== ls ~/VerSeFusion ~/XRSpinoPelvic1K ~/spinopelvic-seg"; ls -la --time-style=long-iso $H/VerSeFusion $H/XRSpinoPelvic1K $H/XRSpinoPelvic1K/data $H/spinopelvic-seg $H/spinopelvic-seg/nnunet 2>&1 | head -80
echo "=== ls ~/deepfluoro ~/physics_drr"; ls -la --time-style=long-iso $H/deepfluoro 2>&1 | head; ls $H/physics_drr 2>&1 | head
echo "=== ~/github mode"; ls -la $H/github 2>&1
echo "=== leftovers"; ls -la $H/'to_greg.zip?origin_team=T5G027G83' $H/'view?usp=sharing' 2>&1
echo "=== RS README"; cat $RS/README 2>&1 | head -40
echo "=== ls RS/data/anomaly_harvest/panorama"; ls $RS/data/anomaly_harvest/panorama 2>&1 | head -20
echo "=== ls RS/archive RS/tmp RS/containers RS/envs"; ls -la $RS/archive $RS/tmp $RS/containers $RS/envs 2>&1 | head -40
echo "=== ls shared"; ls -la /rs/rs_grp_oschome 2>&1; ls -la /rs/rs_grp_oschome/shared 2>&1
echo "=== u251 size marker"; ls $H/u251-xenograft-murine-RNASeq-study 2>&1 | head -5
echo "=== done"; date -u
