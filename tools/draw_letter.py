#!/usr/bin/env python3
"""Draw the invitation letter for 'Convince the AI Judge to Visit Your House'.

One image, 768x1024 PNG: a handwritten-style letter on warm paper under a
small sunset house-and-garden illustration, with a postage stamp and a wax
seal. Fully deterministic: fixed layout, vendored DejaVu Serif fonts (free
Bitstream Vera licence), a fixed-seed speckle texture, no timestamp, no
network, no randomness beyond the fixed seed.

Run from anywhere: `python3 tools/draw_letter.py` writes entry.png next to
main.ts (the repository root).
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_DIR = os.path.join(HERE, "fonts")

W, H = 768, 1024
PAPER = (247, 239, 221)
PAPER_DARK = (236, 224, 196)
INK = (43, 33, 24)
INK_SOFT = (84, 66, 48)
RED = (178, 58, 44)
RED_DARK = (146, 44, 32)
GOLD = (198, 142, 55)
GREEN = (74, 110, 68)
GREEN_DARK = (52, 84, 50)
SKY_TOP = (252, 219, 165)
SKY_BOT = (243, 178, 107)
SUN = (232, 164, 60)
WINDOW_GLOW = (255, 214, 120)
HOUSE_WALL = (250, 236, 205)
ROOF = (165, 72, 52)
DOOR = (110, 66, 40)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paper_texture(draw):
    """A few hundred faint speckles, fixed seed, so the paper is not flat."""
    rng = random.Random(20261125)
    for _ in range(420):
        x = rng.randint(20, W - 20)
        y = rng.randint(20, H - 20)
        c = PAPER_DARK if rng.random() < 0.5 else (250, 244, 230)
        draw.point((x, y), fill=c)


def frame(draw):
    draw.rectangle([16, 16, W - 17, H - 17], outline=RED_DARK, width=3)
    draw.rectangle([26, 26, W - 27, H - 27], outline=GOLD, width=1)


def illustration(draw):
    """Sunset house-and-garden scene across the top of the letter."""
    x0, y0, x1, y1 = 56, 44, 560, 216
    # Sky: warm vertical gradient, drawn as one-pixel-high strips.
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        draw.line([(x0, y), (x1, y)], fill=lerp(SKY_TOP, SKY_BOT, t))
    draw.rectangle([x0, y0, x1, y1], outline=INK_SOFT, width=2)
    # Sun with a soft halo.
    draw.ellipse([x0 + 26, y0 + 18, x0 + 86, y0 + 78], fill=(250, 196, 110))
    draw.ellipse([x0 + 36, y0 + 28, x0 + 76, y0 + 68], fill=SUN)
    # Garden strip at the bottom of the sky.
    draw.rectangle([x0, y1 - 26, x1, y1], fill=GREEN)
    draw.rectangle([x0, y1 - 26, x1, y1 - 22], fill=GREEN_DARK)
    # A small tree on the left of the house.
    draw.rectangle([x0 + 42, y1 - 78, x0 + 50, y1 - 26], fill=(96, 66, 38))
    draw.ellipse([x0 + 18, y1 - 112, x0 + 74, y1 - 62], fill=GREEN)
    draw.ellipse([x0 + 30, y1 - 122, x0 + 66, y1 - 84], fill=(92, 128, 84))
    # The house: walls, roof, chimney, door, glowing windows.
    hx0, hy0, hx1, hy1 = x0 + 190, y1 - 118, x0 + 330, y1 - 26
    draw.polygon([(hx0 - 16, hy0 + 34), ((hx0 + hx1) // 2, hy0 - 22),
                  (hx1 + 16, hy0 + 34)], fill=ROOF)
    draw.rectangle([hx0, hy0 + 34, hx1, hy1], fill=HOUSE_WALL,
                   outline=INK_SOFT, width=2)
    draw.rectangle([hx1 - 34, hy0 - 12, hx1 - 18, hy0 + 30], fill=ROOF)
    # Chimney smoke: three soft puffs rising from the chimney mouth.
    for i, r in enumerate((6, 8, 10)):
        cx = hx1 - 26 + i * 5
        cy = hy0 - 14 - i * 15
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=(150, 140, 125), width=3)
    # Door with a round knob, windows glowing warm.
    draw.rectangle([(hx0 + hx1) // 2 - 16, hy1 - 52, (hx0 + hx1) // 2 + 16,
                    hy1], fill=DOOR)
    draw.ellipse([(hx0 + hx1) // 2 + 8, hy1 - 28, (hx0 + hx1) // 2 + 14,
                  hy1 - 22], fill=GOLD)
    for wx in (hx0 + 14, hx1 - 46):
        draw.rectangle([wx, hy0 + 50, wx + 32, hy0 + 82], fill=WINDOW_GLOW,
                       outline=INK_SOFT, width=2)
        draw.line([(wx + 16, hy0 + 50), (wx + 16, hy0 + 82)], fill=INK_SOFT,
                  width=2)
        draw.line([(wx, hy0 + 66), (wx + 32, hy0 + 66)], fill=INK_SOFT,
                  width=2)
    # Flowers along the garden strip.
    for fx, fc in ((x0 + 96, RED), (x0 + 130, (232, 120, 90)),
                   (x0 + 380, RED), (x0 + 414, (240, 200, 90)),
                   (x0 + 448, (232, 120, 90))):
        draw.ellipse([fx - 5, y1 - 20, fx + 5, y1 - 10], fill=fc)
        draw.ellipse([fx - 2, y1 - 14, fx + 2, y1 - 10], fill=GOLD)
    # A steaming mug on a little table, right of the house.
    tx0, ty = x0 + 372, y1 - 52
    draw.rectangle([tx0, ty, tx0 + 64, ty + 6], fill=(120, 82, 52))
    draw.rectangle([tx0 + 6, ty + 6, tx0 + 10, y1 - 26], fill=(120, 82, 52))
    draw.rectangle([tx0 + 54, ty + 6, tx0 + 58, y1 - 26], fill=(120, 82, 52))
    draw.rectangle([tx0 + 14, ty - 26, tx0 + 50, ty], fill=(250, 246, 236),
                   outline=INK_SOFT, width=2)
    draw.arc([tx0 + 48, ty - 22, tx0 + 66, ty - 4], 270, 90, fill=INK_SOFT,
             width=3)
    for i, sx in enumerate((tx0 + 24, tx0 + 32, tx0 + 40)):
        draw.arc([sx - 5, ty - 44 + i * 2, sx + 5, ty - 28 + i * 2], 200, 340,
                 fill=(150, 140, 125), width=3)


def stamp(img):
    """A tilted postage stamp in the top-right corner: YOU ARE INVITED."""
    st = Image.new("RGBA", (150, 168), (0, 0, 0, 0))
    d = ImageDraw.Draw(st)
    d.rectangle([8, 8, 142, 160], fill=(250, 246, 236),
                outline=INK_SOFT, width=2)
    for x in range(12, 140, 10):
        d.line([(x, 8), (x + 5, 8)], fill=INK_SOFT, width=2)
        d.line([(x, 160), (x + 5, 160)], fill=INK_SOFT, width=2)
    for y in range(12, 158, 10):
        d.line([(8, y), (8, y + 5)], fill=INK_SOFT, width=2)
        d.line([(142, y), (142, y + 5)], fill=INK_SOFT, width=2)
    d.text((75, 34), "YOU ARE", font=font(SERIF_B, 21), fill=RED, anchor="ma")
    d.text((75, 62), "INVITED", font=font(SERIF_B, 21), fill=RED, anchor="ma")
    # A tiny house glyph inside the stamp.
    d.polygon([(55, 108), (75, 90), (95, 108)], fill=ROOF)
    d.rectangle([60, 108, 90, 130], fill=HOUSE_WALL, outline=INK_SOFT,
                width=2)
    d.rectangle([70, 116, 80, 130], fill=DOOR)
    d.text((75, 138), "ONE SEAT SAVED", font=font(SERIF_B, 11), fill=INK_SOFT,
           anchor="ma")
    img.paste(st.rotate(7, expand=True, resample=Image.BICUBIC),
              (566, 30), st.rotate(7, expand=True, resample=Image.BICUBIC))


def wax_seal(draw):
    """A red wax seal with a heart, bottom-right of the letter."""
    cx, cy, r = 664, 918, 40
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                 outline=RED_DARK, width=2)
    draw.ellipse([cx - r + 9, cy - r + 9, cx + r - 9, cy + r - 9],
                 outline=(255, 255, 255), width=1)
    # Heart: two lobes and a point.
    draw.ellipse([cx - 16, cy - 12, cx, cy + 2], fill=(250, 246, 236))
    draw.ellipse([cx, cy - 12, cx + 16, cy + 2], fill=(250, 246, 236))
    draw.polygon([(cx - 16, cy - 2), (cx + 16, cy - 2), (cx, cy + 16)],
                 fill=(250, 246, 236))


def letter(draw):
    """The invitation itself: one concrete reason, one easy yes, one wink."""
    mx, text_w = 72, 624
    y = 248
    draw.text((mx, y), "Dear Judge,", font=font(SERIF_B, 46), fill=INK)
    y = 322
    para1 = ("Please come to my house. I will cook rendang, slow and rich, "
             "and save you the good chair by the window \u2014 the one that "
             "looks out on the garden at golden hour.")
    body = font(SERIF, 33)
    for line in wrap(draw, para1, body, text_w):
        draw.text((mx, y), line, font=body, fill=INK)
        y += 47
    y += 18
    para2 = ("You don't have to travel at all. Just look in: the kettle is "
             "already on, the cat has approved you, and the Wi-Fi password "
             "is on the fridge.")
    for line in wrap(draw, para2, body, text_w):
        draw.text((mx, y), line, font=body, fill=INK)
        y += 47
    y += 22
    draw.text((mx, y), "Come hungry. Leave happy.",
              font=font(SERIF_B, 36), fill=RED)
    y += 66
    draw.text((mx, y), "\u2014 Your hopeful host",
              font=font(SERIF, 32), fill=INK)
    y += 58
    draw.text((mx, y), "P.S. The chair really is that comfortable.",
              font=font(SERIF, 26), fill=INK_SOFT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    paper_texture(draw)
    illustration(draw)
    stamp(img)
    draw = ImageDraw.Draw(img)
    letter(draw)
    wax_seal(draw)
    frame(draw)
    out = os.path.join(ROOT, "entry.png")
    img.save(out, format="PNG")
    print(f"Wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
