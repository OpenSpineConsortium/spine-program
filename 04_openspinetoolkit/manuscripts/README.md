# manuscripts/

## `bibm_spinopelvic/` (an unfinished draft of 2026-06-28; never submitted as far as any file records)

"From Segmented CT to Spinopelvic Measurement: An Open Geometric Engine, a CT to Radiograph Bridge, and a
Deployable Viewer", an IEEE conference-format draft (`main.tex`, 17,059 B before the one redaction) aimed at
BIBM 2026 (deadline about 5 July 2026) that collapsed the XRSpinoPelvic1K paper into one wrap-up of everything
built on CTSpinoPelvic1K: the ostk spinopelvic engine, the CT-to-radiograph bridge (2-D port and label-carrying
DRRs), the NiiVue viewer with its `metrics.json` contract and the post-op synthesis prototype (handoff
`MANUSCRIPTS.md` section 10; `../memory/pacs-demo-and-ostk-params.md`). Its header is an honesty contract
(no trained X-ray localiser, no full 1k X-ray release, no AR, no live dual-engine swap, SS/PT/LL on supine CT
are surrogates, manual validation ongoing) and the text carries 17 `\TODO{}` marks, among them the whole of
Table 1 (PI/SS/PT/LL distribution), two figures and the 2-D/3-D tolerance. `README.md` lists the four
remaining steps; `tools/cohort_stats.py` turns a `python -m ostk all` summary into Table 1.

What was changed on copy: the author block's correspondence address at line 24 (a personal e-mail) now reads
"[personal e-mail struck on copy, 2026-10-08]". Nothing else.

State: treat as unwritten (handoff `MANUSCRIPTS.md` section 10 "Redo"). The spinopelvic numbers it would
report must be recomputed on v11 with `ostk.labels.labels_for(volume)` after `../TODO.md` steps 1-2; the
X-ray level-localisation content is SchwingNet-adjacent and private; whether to pursue the paper is Greg's
(`../TODO.md` item 9; handoff `OPEN_QUESTIONS.md` A8). The affiliation for any version is General Surgery
(Wayne State University School of Medicine / Detroit Medical Center).
