"""paper/cns2026/render_case42.py — the one real intraoperative frame of a patient one CT labeller reads six-lumbar
(C-ArmLSpine case 42, lateral, fold 2), drawn with what the system put on every box: the shape reading with its
probability, the count from the detected sacrum in the ordinary alphabet, and the call; the body where the two
disagree is red and the read stopped. Numbers from SchwingNet/results/fig4_frames/case42_LAT.couple.json (the file
Figure 4c-d was drawn from); frame from results/fig5_frames/case42_LAT.png (public release, 1024 px).

    python paper/cns2026/render_case42.py
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
F = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 30)
FS = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26)
FH = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)
NAVY = (0x19, 0x1D, 0x63)
BLUE = (0x4C, 0x70, 0xB7)
RED = (0xEF, 0x46, 0x27)
GREY = (0x8A, 0x8A, 0x8A)
WHITE = (255, 255, 255)

d = json.load(open(SN / "results" / "fig4_frames" / "case42_LAT.couple.json"))
fr = Image.open(SN / "results" / "fig5_frames" / "case42_LAT.png").convert("L")
fr = ImageOps.autocontrast(fr, cutoff=0.5).convert("RGB")
X0, X1 = 300, 1024                       # the columns the manuscript shows
crop = fr.crop((X0, 0, X1, 1024))
W = crop.width
panel = Image.new("RGB", (W + 620, 1024), WHITE)
panel.paste(crop, (0, 0))
dr = ImageDraw.Draw(panel)

# column headers
cx = W + 20
dr.text((cx, 12), "shape", font=FH, fill=NAVY)
dr.text((cx + 200, 12), "count", font=FH, fill=GREY)
dr.text((cx + 400, 12), "call", font=FH, fill=NAVY)

ax0, ay0, ax1, ay1 = d["anchor"]["box"]
dr.rectangle([ax0 - X0, ay0, ax1 - X0, ay1], outline=(20, 20, 20), width=5)
dr.rectangle([ax0 - X0 + 4, ay1 - 52, ax0 - X0 + 300, ay1 - 6], fill=(20, 20, 20))
dr.text((ax0 - X0 + 12, ay1 - 48), "sacrum, anchor 0", font=F, fill=WHITE)
for b in d["bodies"]:
    x0, y0, x1, y1 = b["box"]
    x0 -= X0; x1 -= X0
    bad = b["disagree"]
    col = RED if bad else BLUE
    dr.rectangle([x0, y0, x1, y1], outline=col, width=5)
    dr.rectangle([x0, y0, x0 + 46, y0 + 40], fill=col)
    dr.text((x0 + 10, y0 + 4), str(b["ordinal"]), font=F, fill=WHITE)
    yc = (y0 + y1) // 2 - 16
    shape = "none" if b["abstain"] else b["classifier"]
    p = b["p_classifier"]
    dr.text((cx, yc), f"{shape} {p:.2f}", font=F, fill=(RED if bad else NAVY))
    dr.text((cx + 200, yc), b["count"], font=F, fill=GREY)
    dr.text((cx + 400, yc), b["coupled"], font=F, fill=(RED if bad else NAVY))
    dr.line([x1, (y0 + y1) // 2, W + 10, yc + 18], fill=col, width=2)
# footer inside the white column
dr.text((cx, 900), f"alphabet scores: ordinary {d['candidates']['ordinary']:.2f}", font=FS, fill=GREY)
dr.text((cx, 934), f"L6 {d['candidates']['L6']:.2f}; call {d['call']}", font=FS, fill=NAVY)
dr.text((cx, 972), "body 1 unnamed: the read stopped", font=F, fill=RED)
panel.save(OUT / "render_case42_L6.png")
print("render_case42_L6", panel.size, "call", d["call"], "flag", d["flag_disagree"])
