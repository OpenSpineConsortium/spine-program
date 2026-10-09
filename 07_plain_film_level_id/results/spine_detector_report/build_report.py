"""build_report.py -- assemble report.html from assets.json.

Kept separate from the HTML so the base64 renders never have to be pasted by hand and the
page can be regenerated from a new training run by re-running make_assets.py then this.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).parent
A = json.loads((HERE / "assets.json").read_text())
M, C, F, CO = A["metrics"], A["curves"], A["final"], A["cohort"]
mt = C["_meta"]


def pct(x):
    return f"{x*100:.1f}"


def metric_rows():
    order = [("source:nhanes", "NHANES II", "film, cervical", "annotated"),
             ("source:mendeley", "Mendeley 716", "standing DR, lumbar", "unknown"),
             ("source:buu", "BUU-LSPINE", "standing DR, lumbar", "positional"),
             ("acquisition:film", "— film", "", ""),
             ("acquisition:standing_dr", "— standing DR", "", "")]
    out = []
    for key, name, acq, lvl in order:
        if key not in M:
            continue
        r = M[key]
        cls = "sub" if name.startswith("—") else ""
        out.append(f"""<tr class="{cls}">
          <th scope="row">{name}<span class="acq">{acq}</span></th>
          <td class="num">{r['n_gt']}</td>
          <td class="num">{r['AP50']:.3f}</td>
          <td class="num">{r['PCK@0.1']:.3f}</td>
          <td class="num">{r['PCK@0.2']:.3f}</td>
        </tr>""")
    return "\n".join(out)


def render_figs():
    out = []
    for k, v in A["renders"].items():
        out.append(f"""<figure class="shot">
          <img src="{v['uri']}" alt="{v['title']}: radiograph with ground-truth and predicted vertebra quadrilaterals overlaid" loading="lazy">
          <figcaption><b>{v['title']}</b> <span class="src">{v['source']}</span><br>{v['caption']}</figcaption>
        </figure>""")
    return "\n".join(out)


def axis_ticks():
    w, h, pad = mt["w"], mt["h"], mt["pad"]
    ticks = []
    for v in (0.25, 0.5, 0.75, 1.0):
        y = h - pad - v * (h - 2 * pad)
        ticks.append(f'<line class="grid" x1="{pad}" y1="{y:.1f}" x2="{w-pad}" y2="{y:.1f}"/>')
        ticks.append(f'<text class="tick" x="{pad-8}" y="{y+4:.1f}" text-anchor="end">{v:.2f}</text>')
    for e in (1, 30, 60, 90, mt["n_epochs"]):
        x = pad + (e - mt["x0"]) / max(mt["x1"] - mt["x0"], 1) * (w - 2 * pad)
        ticks.append(f'<text class="tick" x="{x:.1f}" y="{h-pad+18}" text-anchor="middle">{e}</text>')
    return "\n".join(ticks)


HTML = f"""<title>Vertebra Detector Field Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap">
<style>
:root {{
  --ground:#0A0D12; --surface:#141A22; --raise:#1B222C; --line:#232C37;
  --bone:#EAE6DD; --muted:#8B95A3; --dim:#5D6874;
  --pred:#E64BA6; --truth:#34C48D; --warn:#E0A54A;
  --serif:"IBM Plex Serif",Georgia,serif;
  --sans:"IBM Plex Sans",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,monospace;
}}
:root[data-theme="light"] {{
  --ground:#F2EFE9; --surface:#FFFFFF; --raise:#F7F5F1; --line:#DCD6CC;
  --bone:#171C22; --muted:#5A636E; --dim:#8A929C;
  --pred:#B81F79; --truth:#1B7F58;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--bone);font-family:var(--sans);
  font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 28px}}
.col{{max-width:68ch}}
h1,h2,h3{{font-family:var(--serif);text-wrap:balance;margin:0}}
h1{{font-size:clamp(2.3rem,5vw,3.5rem);line-height:1.05;font-weight:600;letter-spacing:-.02em}}
h2{{font-size:1.65rem;font-weight:600;margin:0 0 .6rem}}
h3{{font-size:1.12rem;font-weight:600;margin:1.8rem 0 .4rem}}
p{{margin:0 0 1.05rem}}
a{{color:var(--pred)}}
.eyebrow{{font-family:var(--mono);font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);margin:0 0 1rem}}
header{{padding:74px 0 44px;border-bottom:1px solid var(--line)}}
.lede{{font-size:1.22rem;color:var(--muted);max-width:60ch;margin-top:1.3rem}}
section{{padding:52px 0;border-bottom:1px solid var(--line)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);margin:2.4rem 0 0}}
.stat{{background:var(--surface);padding:20px 22px}}
.stat .v{{font-family:var(--mono);font-size:2rem;font-weight:500;letter-spacing:-.02em;
  font-variant-numeric:tabular-nums;color:var(--bone);display:block}}
.stat .k{{font-family:var(--mono);font-size:.7rem;letter-spacing:.11em;text-transform:uppercase;
  color:var(--muted);margin-top:.35rem;display:block}}
.stat.hero .v{{color:var(--pred)}}
table{{width:100%;border-collapse:collapse;font-size:.94rem}}
th,td{{padding:11px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:baseline}}
thead th{{font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);font-weight:500;border-bottom:1px solid var(--line)}}
tbody th{{font-weight:500}}
.num{{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right}}
tr.sub th,tr.sub td{{color:var(--muted);font-weight:400}}
.acq{{display:block;font-family:var(--mono);font-size:.68rem;color:var(--dim);letter-spacing:.05em}}
.scroll{{overflow-x:auto}}
.chart{{background:var(--surface);border:1px solid var(--line);padding:18px 8px 8px;margin:1.6rem 0}}
.chart svg{{display:block;width:100%;height:auto}}
.grid{{stroke:var(--line);stroke-width:1}}
.tick{{fill:var(--dim);font-family:var(--mono);font-size:10px}}
.ln{{fill:none;stroke-width:2;vector-effect:non-scaling-stroke}}
.legend{{display:flex;gap:1.4rem;flex-wrap:wrap;font-family:var(--mono);font-size:.74rem;
  color:var(--muted);padding:0 14px 6px}}
.legend i{{display:inline-block;width:14px;height:3px;margin-right:7px;vertical-align:middle}}
.shots{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px;margin-top:1.8rem}}
.shot{{margin:0;background:var(--surface);border:1px solid var(--line)}}
.shot img{{width:100%;display:block;background:#000}}
.shot figcaption{{padding:13px 15px;font-size:.85rem;color:var(--muted);line-height:1.5}}
.shot b{{color:var(--bone);font-weight:600}}
.src{{font-family:var(--mono);font-size:.68rem;color:var(--dim);letter-spacing:.06em}}
.key{{display:flex;gap:1.5rem;font-family:var(--mono);font-size:.76rem;color:var(--muted);margin:1.2rem 0 0}}
.key i{{display:inline-block;width:12px;height:12px;border:2px solid;margin-right:7px;vertical-align:-2px}}
.note{{border-left:3px solid var(--warn);background:var(--surface);padding:16px 20px;margin:1.6rem 0;
  font-size:.95rem}}
.note b{{color:var(--warn)}}
.blocked{{border-left:3px solid var(--pred)}}
.blocked b{{color:var(--pred)}}
ul{{margin:0 0 1.05rem;padding-left:1.15rem}}
li{{margin-bottom:.5rem}}
code{{font-family:var(--mono);font-size:.87em;background:var(--raise);padding:.12em .38em;
  border:1px solid var(--line)}}
pre{{font-family:var(--mono);font-size:.8rem;background:var(--surface);border:1px solid var(--line);
  padding:16px 18px;overflow-x:auto;line-height:1.6;color:var(--muted)}}
footer{{padding:44px 0 70px;color:var(--dim);font-size:.85rem}}
@media (prefers-color-scheme: light){{
  :root:not([data-theme="dark"]){{
    --ground:#F2EFE9; --surface:#FFFFFF; --raise:#F7F5F1; --line:#DCD6CC;
    --bone:#171C22; --muted:#5A636E; --dim:#8A929C;
    --pred:#B81F79; --truth:#1B7F58;
  }}
}}
:root[data-theme="dark"]{{
  --ground:#0A0D12; --surface:#141A22; --raise:#1B222C; --line:#232C37;
  --bone:#EAE6DD; --muted:#8B95A3; --dim:#5D6874;
  --pred:#E64BA6; --truth:#34C48D;
}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important;transition:none!important}}}}
</style>

<div class="wrap">
<header>
  <p class="eyebrow">Stage 1 · class-agnostic detection · {F['epochs']} epochs</p>
  <h1>Finding vertebrae without<br>counting from C2</h1>
  <p class="lede">A single detector that locates every vertebral body on a spine radiograph and
  returns its four corners — trained on a union of partially-labelled public datasets, and
  measured per source rather than pooled.</p>
  <div class="stats">
    <div class="stat hero"><span class="v">{F['box_map50']:.3f}</span><span class="k">Box mAP@50 · val</span></div>
    <div class="stat hero"><span class="v">{F['pose_map50']:.3f}</span><span class="k">Corner mAP@50 · val</span></div>
    <div class="stat"><span class="v">{M['all:all']['AP50']:.3f}</span><span class="k">AP@50 · held-out test</span></div>
    <div class="stat"><span class="v">{pct(M['all:all']['PCK@0.2'])}%</span><span class="k">PCK@0.2 · test</span></div>
    <div class="stat"><span class="v">6.8<span style="font-size:1rem"> ms</span></span><span class="k">Inference / image</span></div>
  </div>
</header>

<section class="col">
  <h2>The problem the design solves</h2>
  <p>Public spine-radiograph datasets each annotate a different stretch of the column: one
  covers the cervical spine, another L1–L5, another T1–L5. Train per-level classes on their
  union and level identity becomes confounded with the dataset it came from — a class that
  appears in exactly one source can be predicted from scanner style rather than anatomy.</p>
  <p>So the detector carries <b>one class</b>. Every vertebral body is the same object, and
  anatomical level is left to a second head that shares the backbone, trained later and
  measured separately. That leaves one hazard, and it is the reason this project exists: in a
  cervical-only dataset the thoracic vertebrae at the bottom of the film are real vertebrae
  with no ground truth, and training them as background teaches the model to suppress true
  positives.</p>
  <div class="note"><b>Not yet in this run.</b> The ignore-region loss mask is written
  (<code>src/ignore.py</code>) but the trained model below used cropping only. The headline
  numbers are therefore in-distribution, and the union-with-ignore ablation — the experiment
  that justifies the method — has not been run.</div>
</section>

<section>
  <div class="col"><h2>Corpus</h2>
  <p>Three sources were reachable without credentials. Every row is one vertebra instance;
  splits are patient-disjoint, because BUU pairs an AP and a lateral per patient and NHANES
  participants have both a cervical and a lumbar film.</p></div>
  <div class="scroll"><table>
    <thead><tr><th>Source</th><th class="num">Instances</th><th>View</th><th>Levels</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><th scope="row">NHANES II<span class="acq">film, 1976–80</span></th><td class="num">{CO['by_source']['nhanes']}</td><td>lateral</td><td>annotated</td><td>Per-level masks keyed by vertebra name; images ship with the coordinates, so no frame mismatch is possible.</td></tr>
      <tr><th scope="row">Mendeley 716<span class="acq">standing DR</span></th><td class="num">{CO['by_source']['mendeley']}</td><td>lateral</td><td>unknown</td><td>Roboflow export; carries no level names, so none were invented.</td></tr>
      <tr><th scope="row">BUU-LSPINE<span class="acq">standing DR</span></th><td class="num">{CO['by_source']['buu']}</td><td>AP + lateral</td><td>positional</td><td>Partial download — Google Drive caps folder transfers.</td></tr>
    </tbody>
  </table></div>
  <div class="col">
  <p style="margin-top:1.4rem">{CO['images']} images · {CO['instances']} instances · {CO['patients']} patients ·
  {CO['by_view'].get('LAT',0)} lateral / {CO['by_view'].get('AP',0)} AP.</p>
  <div class="note"><b>Two parsing bugs the validators caught.</b> BUU's edge lines pair
  step-2, not consecutively — walking consecutive pairs emits a quadrilateral for every
  <em>disc space</em> as well as every body. And Roboflow exports the same image into
  train/valid/test under different hashes, which duplicated 107 instances and would have put
  one physical radiograph on both sides of a split.</div>
  </div>
</section>

<section>
  <div class="col"><h2>Training</h2>
  <p>YOLO11m-pose, one class, four keypoints, 1024 px, AdamW, {F['epochs']} epochs on one H200.
  Horizontal flip is <b>disabled</b>: on a lateral radiograph a flip is anatomically
  impossible and silently swaps the anterior/posterior meaning of the corner slots — there is
  no error, the keypoint head simply fails to converge.</p></div>
  <div class="chart">
    <div class="legend">
      <span><i style="background:var(--pred)"></i>Box mAP@50</span>
      <span><i style="background:var(--pred);opacity:.45"></i>Box mAP@50-95</span>
      <span><i style="background:var(--truth)"></i>Corner mAP@50</span>
      <span><i style="background:var(--truth);opacity:.45"></i>Corner mAP@50-95</span>
    </div>
    <svg viewBox="0 0 {mt['w']} {mt['h']}" role="img" aria-label="Validation metrics over {F['epochs']} epochs, all four series rising and plateauing above 0.9">
      {axis_ticks()}
      <path class="ln" d="{C['box5095']}" stroke="var(--pred)" opacity=".45"/>
      <path class="ln" d="{C['pose5095']}" stroke="var(--truth)" opacity=".45"/>
      <path class="ln" d="{C['pose50']}" stroke="var(--truth)"/>
      <path class="ln" d="{C['box50']}" stroke="var(--pred)"/>
    </svg>
  </div>
  <div class="col"><p>Box mAP@50 passes 0.90 by epoch 20 and settles at
  <b>{F['box_map50']:.3f}</b>; corner mAP@50-95 reaches <b>{F['pose_map5095']:.3f}</b>, which
  matters more than the box number — it says the four corners land tightly, not merely that
  something was found in roughly the right place.</p></div>
</section>

<section>
  <div class="col"><h2>Held-out results</h2>
  <p>Reported per source and per acquisition. A pooled number would hide exactly the
  generalization behaviour worth measuring. PCK is normalised by each vertebra's own body
  height — never image diagonal, which would mean something different on a cervical crop than
  on a full-spine film.</p></div>
  <div class="scroll"><table>
    <thead><tr><th>Group</th><th class="num">Instances</th><th class="num">AP@50</th><th class="num">PCK@0.1</th><th class="num">PCK@0.2</th></tr></thead>
    <tbody>
      <tr><th scope="row">All</th><td class="num">{M['all:all']['n_gt']}</td><td class="num">{M['all:all']['AP50']:.3f}</td><td class="num">{M['all:all']['PCK@0.1']:.3f}</td><td class="num">{M['all:all']['PCK@0.2']:.3f}</td></tr>
      {metric_rows()}
    </tbody>
  </table></div>
  <div class="col">
  <div class="note"><b>Recall is not reported globally, by design.</b> On partially-labelled
  sources a “missed” vertebra may be one the dataset never annotated. Detections are scored
  only inside the trusted-background region; outside it they are neither credited nor
  penalised.</div>
  <p>The spread is small — 0.861 on BUU against 0.970 on NHANES — but BUU contributes only 15
  test instances here, so that gap is not yet a measurement. <b>None of these are cross-site.</b>
  Every test image comes from a source the model also trained on.</p>
  </div>
</section>

<section>
  <div class="col"><h2>Predictions</h2>
  <p>Held-out images, drawn at inference. Ground truth in green, prediction in magenta.</p>
  <div class="key">
    <span><i style="border-color:var(--truth)"></i>ground truth</span>
    <span><i style="border-color:var(--pred)"></i>prediction</span>
  </div></div>
  <div class="shots">{render_figs()}</div>
</section>

<section class="col">
  <h2>What is not done</h2>
  <p>The specification asks for considerably more than this run delivers. Stating the gap
  precisely is more useful than a number that implies otherwise.</p>
  <div class="note blocked"><b>Blocked on credentials, not on work.</b>
  <b>VinDr-SpineXR</b> requires a personal PhysioNet credentialed account — CITI training plus
  supervisor attestation, typically weeks. <b>IEEE DataPort's 236 lateral full-spine films</b>
  need a subscription login; those are the intended primary evaluation hold-out, so until they
  exist there is no genuinely external test set.</div>
  <h3>Datasets not obtained</h3>
  <ul>
    <li><b>CSXA</b> — the metadata repository and its pixel-scale table are downloaded, but the
    4,963 images sit behind a SciDB browser session; four candidate API endpoints all returned
    errors. This is the largest annotated lateral set in existence and its absence is the
    single biggest gap in the corpus.</li>
    <li><b>BUU</b> — 77 of ~7,200 files. Google Drive caps folder downloads; the rest needs
    per-file IDs or rclone.</li>
    <li><b>CM Spine</b> — Google Drive refused the transfer. This is the only public
    intraoperative source, so no fluoroscopy is represented and the ±180° C-arm rotation policy
    is untested.</li>
    <li><b>AASCE</b> — SpineWeb request form. Its absence means <em>no thoracic levels and no
    AP full-spine</em> anywhere in the corpus.</li>
  </ul>
  <h3>Built but not exercised</h3>
  <ul>
    <li><b>Ignore-region loss mask</b> — geometry and rendering are implemented and unit-tested;
    the ultralytics loss patch is not wired in, so the headline ablation is unrun.</li>
    <li><b>Level head</b> — not started. The spec is explicit that detection must be stable
    first, and it is only now stable.</li>
    <li><b>Per-acquisition augmentation</b> — the policy is specified; the C-arm case has no
    data to apply it to.</li>
    <li><b>Annotation programme</b> — CVAT, honeypots, adjudication: needs people, and needs
    the credentialed datasets above.</li>
  </ul>
  <div class="note"><b>Read the headline numbers accordingly.</b> {M['all:all']['AP50']:.3f}
  AP@50 is an in-distribution result on three lateral-dominant sources with cropping instead of
  ignore masks. It demonstrates the pipeline is correct end to end. It is not evidence of
  cross-site generalization, which is the property the project exists to establish.</div>
</section>

<section class="col">
  <h2>Reproduce</h2>
  <pre>python -m src.build_dataset          # converters -> normalised PNG + manifest
python -m src.export_yolo            # manifest -> ultralytics pose format
python -m src.train --epochs 120     # fliplr=0.0, mosaic=0.0
python -m src.run_eval --weights runs/pose/runs/detect_v1/weights/best.pt</pre>
  <p>25 unit tests cover the manifest schema and the corner geometry — slot ordering is
  rotation- and winding-invariant, self-intersecting quadrilaterals are rejected, and a level
  may not be recorded without recording how it was known.</p>
</section>

<footer>
  Trained on one NVIDIA H200 · YOLO11m-pose, 20.9 M parameters ·
  {CO['images']} images / {CO['instances']} instances / {CO['patients']} patients ·
  generated from <code>results.csv</code> and <code>metrics.json</code>
</footer>
</div>
"""

(HERE / "report.html").write_text(HTML, encoding="utf-8")
print(f"wrote report.html ({len(HTML)/1e6:.2f} MB)")
