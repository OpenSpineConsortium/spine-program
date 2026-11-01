"""paper/cns2026/prep_v22_site.py -- the end slide's picture of the consortium's website (v22, Greg, 2026-11-01).

Greg asked for the website itself on the last slide. The home page is opened in Edge at 1440 by 900 at twice the
pixels, as a visitor sees it on a laptop, and set in a plain browser window (title bar, three dots, the address)
with a soft shadow, so it reads as the site and not as a figure. The slide links the picture to the site.

    python paper/cns2026/prep_v22_site.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FIG = HERE / "figs_v22_6min"
SITE = "https://openspineconsortium.com/"
VIEW = (1440, 900)
SCALE = 2
BAR = 64                       # the title bar, in screenshot pixels
RADIUS = 22
SHADOW = 36
FONT = "C:/Windows/Fonts/arial.ttf"


def capture():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": VIEW[0], "height": VIEW[1]}, device_scale_factor=SCALE)
        page.goto(SITE, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2500)
        page.screenshot(path=str(FIG / "site_home.png"))
        browser.close()


def window(shot):
    w, h = shot.size
    win = Image.new("RGBA", (w, h + BAR), (0, 0, 0, 0))
    mask = Image.new("L", win.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, win.width - 1, win.height - 1), RADIUS, fill=255)
    body = Image.new("RGBA", win.size, (236, 236, 238, 255))
    body.paste(shot.convert("RGBA"), (0, BAR))
    draw = ImageDraw.Draw(body)
    for i, colour in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        cx, cy = 40 + i * 34, BAR // 2
        draw.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=colour)
    pill = (w * 0.30, 13, w * 0.70, BAR - 13)
    draw.rounded_rectangle(pill, 19, fill=(255, 255, 255))
    font = ImageFont.truetype(FONT, 26)
    draw.text(((pill[0] + pill[2]) / 2, BAR / 2), "openspineconsortium.com", font=font, fill=(70, 70, 74), anchor="mm")
    draw.line((0, BAR - 1, w, BAR - 1), fill=(210, 210, 214), width=2)
    win.paste(body, (0, 0), mask)
    out = Image.new("RGBA", (win.width + 2 * SHADOW, win.height + 2 * SHADOW), (0, 0, 0, 0))
    shade = Image.new("L", out.size, 0)
    ImageDraw.Draw(shade).rounded_rectangle((SHADOW, SHADOW + 10, SHADOW + win.width, SHADOW + win.height + 10),
                                            RADIUS, fill=90)
    shade = shade.filter(ImageFilter.GaussianBlur(SHADOW / 2))
    out.paste((0, 0, 0, 255), (0, 0), shade)
    out.alpha_composite(win, (SHADOW, SHADOW))
    return out


def main():
    FIG.mkdir(exist_ok=True)
    if "--keep" not in sys.argv or not (FIG / "site_home.png").is_file():
        capture()
    out = window(Image.open(FIG / "site_home.png"))
    out.save(FIG / "site_window.png")
    print("site_window.png", out.size, "shadow", SHADOW)


if __name__ == "__main__":
    main()
