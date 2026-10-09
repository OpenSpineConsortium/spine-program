# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: reader_space/viewport.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""The C-arm viewport: a field of view you slide along a patient, and a body everywhere you are not looking.

WHAT THIS REPLACES, AND WHY. The study used to hand the reader a crop on a grey page. That reproduces the
picture a C-arm makes and throws away the task it is part of. In theatre the image arrives through a machine
that covers a hand's width of a patient lying in front of you, you can move it, and every move is another
exposure. A reader who cannot move the field is not doing the job, and a reader who can move it without cost
is not doing it either.

THE THREE DECISIONS INSIDE THIS FILE.

  A lateral film is never mirrored. Rotating a lateral radiograph a quarter turn puts the head on one
  particular side, and which side is fixed by which side of the image is anterior -- it is not free. Forcing
  the head to the left when the film does not allow it means reflecting the image, and a reflected lateral
  has the spinous processes pointing into the abdomen: an impossible spine, presented to spine surgeons. So
  the RADIOGRAPH is laid down as the rotation allows and the SILHOUETTE is flipped to match. A body has no
  laterality to lose, and patients lie on tables both ways round.

  The field is drawn true to scale, and that is a problem worth stating. A 9-inch intensifier is 140 mm at
  the spine and an adult is about 1766 mm, so an honest field is 8 % of the figure -- on a 1600 px canvas,
  about 125 px, which is too few to name a vertebra from. The figure therefore carries a zoom, magnifying
  the whole scene about the centre of the field, exactly as a C-arm's magnification modes do. At rest the
  whole patient is in view, as intended; the reader zooms in to read, as they would.

  Every position counts as an exposure. Panning is free on a screen and is not free on a patient. The count
  is displayed while the reader works and recorded with the answer, because reducing the number of shots it
  takes to be sure is a claim this kind of aid makes and almost never measures.

WHAT IT REFUSES TO SHOW. The band the field can travel over was clipped against the sacrum, C1 and C2 when
the pack was built. No amount of panning reaches a landmark, because a reader who reaches one will count
from it, and then the study measures counting.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

import carm

# --------------------------------------------------------------------------------------------- the script
# Delivered through gr.Blocks(head=...) so it is parsed once, and re-entered per film by watching for a new
# data token in the DOM. A <script> inside gr.HTML is not reliably executed; a <script type="application/json">
# that is only ever READ is, which is why the film's numbers travel that way.
CARM_JS = r"""
<style>
 #carm-wrap{position:relative;width:100%;background:#0e141b;border-radius:10px;overflow:hidden}
 #carm-canvas{display:block;width:100%;touch-action:none;cursor:grab}
 #carm-canvas.drag{cursor:grabbing}
 .carm-bar{display:flex;gap:10px;align-items:center;padding:8px 12px;background:#131b24;
   color:#c6d3de;font:13px/1.4 system-ui,sans-serif;flex-wrap:wrap}
 .carm-bar button{background:#22303d;color:#dce6ef;border:1px solid #33465a;border-radius:6px;
   padding:5px 11px;font-size:13px;cursor:pointer}
 .carm-bar button:hover{background:#2c3d4d}
 .carm-shots{margin-left:auto;background:#2a2118;border:1px solid #5a4327;color:#e8c98a;
   padding:4px 10px;border-radius:999px;font-variant-numeric:tabular-nums}
 .carm-hint{color:#7e8fa0;font-size:12px}
</style>
<script>
(function(){
 if (window.__carmBooted) return; window.__carmBooted = true;
 const S = {};   // live state for the film on screen

 function el(id){ return document.getElementById(id); }

 function report(){
   const box = document.querySelector('#carm_out textarea');
   if (!box || !S.data) return;
   box.value = JSON.stringify({
     shots: S.shots, pan_mm: Math.round(S.panned||0), zoom: +(S.zoom||1).toFixed(2),
     first_move_ms: S.firstMove ? Math.round(S.firstMove - S.t0) : null,
     final_u: +(S.u||0).toFixed(4), anterior_known: !!S.data.anterior_known,
     span: S.data.span, span_mm: S.data.span_mm });
   box.dispatchEvent(new Event('input', {bubbles:true}));
 }

 // ---- geometry -------------------------------------------------------------------------------------
 function spineY(x, d){                       // body y of the column at stature-fraction x/1000
   const L = d.spine_line; const f = x/1000;
   let a = L[0], b = L[L.length-1];
   for (let i=0;i<L.length-1;i++){ if (f>=L[i][0] && f<=L[i+1][0]){ a=L[i]; b=L[i+1]; break; } }
   const t = (b[0]===a[0]) ? 0 : (f-a[0])/(b[0]-a[0]);
   const depth = a[1] + t*(b[1]-a[1]);
   return d.trunk_ant + depth*(d.trunk_post - d.trunk_ant);
 }
 function centreX(d, u){                      // u in [0,1] along the strip -> body x
   const f = d.body_frac_top + u*(d.body_frac_bot - d.body_frac_top);
   return d.head_left ? f*1000 : (1-f)*1000;
 }

 // ---- drawing --------------------------------------------------------------------------------------
 function draw(){
   const d = S.data; if (!d) return;
   const cv = el('carm-canvas'); if (!cv) return;
   const dpr = Math.min(window.devicePixelRatio||1, 2);
   const W = cv.clientWidth, H = Math.round(W*0.34);
   if (cv.width !== Math.round(W*dpr) || cv.height !== Math.round(H*dpr)){
     cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr); cv.style.height = H+'px';
   }
   const g = cv.getContext('2d');
   g.setTransform(dpr,0,0,dpr,0,0);
   g.fillStyle = '#0e141b'; g.fillRect(0,0,W,H);

   const R = (d.span_mm/d.stature_mm)*1000/2;          // field radius, body units
   const cx = centreX(d, S.u), cy = spineY(cx, d);
   const base = W/1040, K = base*S.zoom;
   const camX = S.zoom<=1.001 ? 500 : cx, camY = S.zoom<=1.001 ? 250 : cy;
   const X = x => (x-camX)*K + W/2, Y = y => (y-camY)*K + H/2;

   // the patient
   g.save();
   g.translate(X(0), Y(0)); g.scale(K*(d.head_left?1:-1), K);
   if (!d.head_left) g.translate(-1000,0);
   g.fillStyle = '#f4f7fa'; g.strokeStyle = '#8c9cab'; g.lineWidth = 2/K;
   const path = new Path2D(d.silhouette);
   g.fill(path); g.stroke(path);
   g.restore();

   // the table
   g.strokeStyle = '#243141'; g.lineWidth = 2;
   g.beginPath(); g.moveTo(X(-40), Y(322)); g.lineTo(X(1040), Y(322)); g.stroke();

   // what the field is over
   const r = R*K;
   g.save();
   g.beginPath(); g.arc(X(cx), Y(cy), r, 0, Math.PI*2); g.clip();
   g.fillStyle = '#05080b'; g.fillRect(X(cx)-r, Y(cy)-r, 2*r, 2*r);
   if (S.img && S.img.complete){
     const sx = Math.abs(centreX(d,1)-centreX(d,0))/d.strip_size[1];   // body units per strip pixel
     const w = d.strip_size[0], h = d.strip_size[1];
     const e = d.head_left ? d.body_frac_top*1000 : (1-d.body_frac_top)*1000;
     g.save();
     g.setTransform(dpr,0,0,dpr,0,0);
     g.translate(X(0), Y(0)); g.scale(K, K);
     if (d.head_left){                 // quarter turn anticlockwise: superior to the left
       g.transform(0, -sx, sx, 0, e, cy + (w/2)*sx);
     } else {                          // quarter turn clockwise: superior to the right
       g.transform(0,  sx,-sx, 0, e, cy - (w/2)*sx);
     }
     g.imageSmoothingQuality = 'high';
     g.drawImage(S.img, 0, 0, w, h);
     const t = d.target_box;
     g.strokeStyle = '#ff4d4d'; g.lineWidth = Math.max(1.2, 3/(K*sx));
     g.strokeRect(t[0], t[1], t[2]-t[0], t[3]-t[1]);
     g.restore();
     g.setTransform(dpr,0,0,dpr,0,0);
     g.save(); g.beginPath(); g.arc(X(cx), Y(cy), r, 0, Math.PI*2); g.clip();
   }
   g.restore();

   // the collimator edge
   g.beginPath(); g.arc(X(cx), Y(cy), r, 0, Math.PI*2);
   g.strokeStyle = '#e0a800'; g.lineWidth = 2.5; g.stroke();

   // if the marked vertebra is out of the field, say which way it lies
   const tu = d.target_u;
   if (Math.abs(tu - S.u) * Math.abs(centreX(d,1)-centreX(d,0)) > R){
     const right = (centreX(d,tu) > cx);
     const ax = X(cx) + (right? r+16 : -r-16), ay = Y(cy);
     g.fillStyle = '#e0a800'; g.beginPath();
     g.moveTo(ax + (right?10:-10), ay); g.lineTo(ax + (right?-4:4), ay-9);
     g.lineTo(ax + (right?-4:4), ay+9); g.closePath(); g.fill();
   }

   if (d.ai_answer){
     const lx = X(cx), ly = Y(cy) - r - 14;
     g.font = '600 15px system-ui,sans-serif'; g.textAlign = 'center';
     const txt = 'system says: ' + d.ai_answer;
     const w = g.measureText(txt).width + 20;
     g.fillStyle = '#1b5b76'; g.beginPath();
     g.roundRect(lx - w/2, ly - 22, w, 26, 6); g.fill();
     g.fillStyle = '#fff'; g.fillText(txt, lx, ly - 4);
     g.textAlign = 'start';
   }

   const sh = el('carm-shots'); if (sh) sh.textContent = S.shots + (S.shots===1?' exposure':' exposures');
   const zl = el('carm-zoom'); if (zl) zl.textContent = '×' + S.zoom.toFixed(1);
 }

 // ---- moving the machine ---------------------------------------------------------------------------
 let settle = null;
 function countShot(){
   const d = S.data; if (!d) return;
   const span = Math.abs(centreX(d,1)-centreX(d,0));
   const R = (d.span_mm/d.stature_mm)*1000/2;
   if (S.lastShotU === null || Math.abs(S.u - S.lastShotU)*span > R*0.5){
     S.shots += 1; S.lastShotU = S.u; draw(); report();
   }
 }
 function moveTo(u, viaUser){
   const d = S.data; if (!d) return;
   const nu = Math.max(d.pan_lo, Math.min(d.pan_hi, u));
   if (viaUser){
     if (!S.firstMove && Math.abs(nu - S.u) > 1e-6) S.firstMove = performance.now();
     S.panned += Math.abs(nu - S.u) * Math.abs(d.body_frac_bot-d.body_frac_top) * d.stature_mm;
   }
   S.u = nu; draw();
   clearTimeout(settle); settle = setTimeout(countShot, 350);
 }

 function boot(){
   const holder = document.getElementById('carm-data');
   const root = document.getElementById('carm-root');
   if (!holder || !root) return;
   const tok = root.getAttribute('data-token');
   if (tok === S.token) return;
   S.token = tok;
   let d; try { d = JSON.parse(holder.textContent); } catch(e){ return; }
   S.data = d; S.u = d.start_u; S.zoom = 1; S.shots = 0; S.lastShotU = null;
   S.panned = 0; S.firstMove = null; S.t0 = performance.now();
   S.img = new Image(); S.img.onload = draw; S.img.src = d.image;
   draw(); countShot();

   const cv = el('carm-canvas');
   let dragging = false, px = 0;
   const span = () => Math.abs(centreX(d,1)-centreX(d,0));
   cv.onpointerdown = e => { dragging = true; px = e.clientX; cv.classList.add('drag');
                             cv.setPointerCapture(e.pointerId); };
   cv.onpointermove = e => {
     if (!dragging) return;
     const W = cv.clientWidth, K = (W/1040)*S.zoom;
     const dx = (e.clientX - px)/K; px = e.clientX;
     moveTo(S.u - (d.head_left ? dx : -dx)/span(), true);
   };
   const stop = e => { dragging = false; cv.classList.remove('drag'); };
   cv.onpointerup = stop; cv.onpointercancel = stop;
   cv.onwheel = e => { e.preventDefault(); setZoom(S.zoom * (e.deltaY < 0 ? 1.12 : 1/1.12)); };
 }

 function setZoom(z){ S.zoom = Math.max(1, Math.min(6, z)); draw(); report(); }
 window.carmZoom = setZoom;
 window.carmNudge = n => {
   const d = S.data; if (!d) return;
   const step = (d.span_mm*0.33/d.stature_mm)*1000 / Math.abs(centreX(d,1)-centreX(d,0));
   moveTo(S.u + (d.head_left ? n : -n)*step, true);
 };

 document.addEventListener('keydown', e => {
   const t = document.activeElement;
   if (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) return;
   if (e.key === 'ArrowRight'){ e.preventDefault(); window.carmNudge(+1); }
   else if (e.key === 'ArrowLeft'){ e.preventDefault(); window.carmNudge(-1); }
   else if (e.key === '+' || e.key === '='){ setZoom(S.zoom*1.25); }
   else if (e.key === '-'){ setZoom(S.zoom/1.25); }
 });
 window.addEventListener('resize', draw);
 new MutationObserver(boot).observe(document.documentElement, {childList:true, subtree:true});
 setInterval(boot, 700);
})();
</script>
"""


def viewport_html(rec: dict, strip_path: Path, show_ai: bool, token: str) -> str:
    """One film, laid on a body, as markup whose only script tag is a block of JSON that gets read."""
    b64 = base64.b64encode(Path(strip_path).read_bytes()).decode()
    ppm = rec["strip_px_per_mm"]
    h = rec["strip_size"][1]
    span_px = rec["span_mm"] * ppm
    lo = (span_px / 2) / h
    hi = 1.0 - lo
    tb = rec["target_box"]
    target_u = ((tb[1] + tb[3]) / 2.0) / h
    ant = rec.get("anterior_left")
    # A lateral cannot be turned head-left without being mirrored when its anterior side is on the left; the
    # body is flipped instead. Unknown falls back to head-left and is flagged rather than guessed silently.
    head_left = True if ant is None else (ant is False)
    d = {"image": "data:image/png;base64," + b64,
         "strip_size": rec["strip_size"], "target_box": tb, "target_u": round(target_u, 4),
         "body_frac_top": rec["body_frac_top"], "body_frac_bot": rec["body_frac_bot"],
         "stature_mm": rec["stature_mm"], "span_mm": rec["span_mm"], "span": rec.get("span", "ii9"),
         "head_left": head_left, "anterior_known": ant is not None,
         "start_u": round(min(max(target_u, lo), hi), 4),
         "pan_lo": round(lo, 4), "pan_hi": round(hi, 4),
         "silhouette": carm.SILHOUETTE, "spine_line": carm.SPINE_LINE,
         "trunk_ant": carm.TRUNK_ANTERIOR_Y, "trunk_post": carm.TRUNK_POSTERIOR_Y,
         "ai_answer": rec["ai_answer"] if show_ai else None}
    travel_mm = round((hi - lo) * abs(rec["body_frac_bot"] - rec["body_frac_top"]) * rec["stature_mm"])
    return f"""
<div id="carm-root" data-token="{token}">
  <div id="carm-wrap"><canvas id="carm-canvas"></canvas></div>
  <div class="carm-bar">
    <button type="button" onclick="carmNudge(-1)">&larr;</button>
    <button type="button" onclick="carmNudge(1)">&rarr;</button>
    <span class="carm-hint">drag the image, or use the arrow keys</span>
    <button type="button" onclick="carmZoom(1)">fit</button>
    <button type="button" onclick="carmZoom(2.5)">zoom</button>
    <button type="button" onclick="carmZoom(4)">more</button>
    <span class="carm-hint" id="carm-zoom">&times;1.0</span>
    <span class="carm-hint">{rec['span_mm']:.0f} mm field &middot; {travel_mm} mm of travel</span>
    <span class="carm-shots" id="carm-shots">1 exposure</span>
  </div>
  <script type="application/json" id="carm-data">{json.dumps(d)}</script>
</div>"""
