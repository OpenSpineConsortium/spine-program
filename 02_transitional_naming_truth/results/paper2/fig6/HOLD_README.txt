Figure 6 evaluation jobs (SchwingNet/slurm/fig6_eval.sh, s15 detector det_g3_primary_s0 primary) -- updated 2026-09-24 17:55 EDT.
Earlier held jobs 40429882 / 40431765 / 40431766 were CANCELLED (pre-s15 detectors); this file replaces the note that named them.

40438004  GATE=open     ordinary persons only (T1 3 / T2 32 / T3 10). Released by the coordinator only after the leak-gate
                        pre-check (job 40438053, SchwingNet/slurm/fig6_gate_precheck.sh) ends F6GATEPRE_OK; the release
                        writes /rs/rs_grp_oschome/go2432/data/fig6/RELEASE_OPEN_GATE.json (LEVELCHECK_MODEL.md s9 record:
                        UTC, grid HEAD, manifest commit + sha256). Not unblinding: no transitional stratum is scored.
40438005  GATE=blinded  afterany:40438004. STAYS HELD until a person writes unblinding/RELEASE_v2.json naming the committed
                        G5 manifest (40-hex a6cc8a11e7303bbf4abb666b7c1760f3831a4dd5), a frozen truth file with its sha256,
                        prespec_commit_is_ancestor true and released_by. Without a frozen HUMAN truth
                        (SchwingNet/results/fig6/verification/truth_frozen.csv + .sha256) every transitional stratum is
                        empty: the s14 automated reference certifies ordinary spines only. Greg decides the human read.
                        Never `scontrol release 40438005` before RELEASE_v2.json exists; the job refuses anyway (exit 6).

Pre-specification: SchwingNet/LEVELCHECK_MODEL.md s1-s15 (ecae75f ... d0403de), frozen. The grid checkout was
fast-forwarded on 2026-09-24 17:41-17:47 so that HEAD descends from ecae75f; G5_MANIFEST.json (commit a6cc8a1) is
identical here and in the checkout. Records: SchwingNet/results/fig6/EVAL_SUBMITTED.json, DETECTOR_G3_VERIFY.md,
frozen/auto_reference.sha256 (57782cad... / aa306deb...), and docs/RESUME_2026-09-22_PM.md checkpoint 17:55.
