#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261118.

A one-page newspaper front page summing up Wednesday 18 November 2026.
Every story below was verified against live reporting on 18 Nov 2026
(Reuters, AP, CNN, SiliconANGLE/NY Post, IMD via Indian press):
  1. Ukraine wrecked the road arch of the 19-km Crimea (Kerch) bridge in a
     second straight day of strikes; Russia hit Kyiv's North and South
     bridges overnight, cutting power and water in parts of the capital.
  2. Trump in Manila: first Quad leaders' summit since 2024 (US, India,
     Japan, Australia); meets President Marcos Jr. on Wednesday 18 Nov
     with full military honours; then on to Shenzhen for talks with Xi
     and Putin on Thursday.
  3. Nvidia beat forecasts: Q3 revenue $115.8bn (+103% YoY), Q4 guidance
     $130bn; board says Jensen Huang will not return as CEO.
  4. Britain sanctioned eight Israeli construction firms over West Bank
     settlement building, plus the Tzav 9 group accused of blocking
     Gaza aid.
  5. Cyclone Akvan strengthened over the Bay of Bengal; Andhra Pradesh
     and Odisha on alert, landfall expected around 20 Nov.
  6. MS Dhoni ended his IPL playing career and became Chennai Super
     Kings' mentor.
Output: 1024x1024 PNG, drawn offline with Pillow only (no network,
no photos, no external assets). Run: python3 draw.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
NAVY = (15, 42, 74)
NAVY2 = (23, 64, 105)
GOLD = (198, 154, 52)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GREY = (90, 90, 88)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.28)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, text, color=RED, size=19):
    f = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + size + 8


def headline(draw, x, y, text, max_w, size=34, leading=None):
    f = font(SERIF, size)
    return para(draw, x, y, text, f, max_w, leading=leading or int(size * 1.12))


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, H], outline=(120, 110, 90), width=3)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 128], fill=NAVY)
d.text((24, 14), "THE WORLD IN ONE DAY", font=font(SERIF, 52), fill=(255, 255, 255))
d.rectangle([24, 82, W - 24, 86], fill=GOLD)
d.text((24, 94), "WEDNESDAY  18  NOVEMBER  2026",
       font=font(SANS_B, 27), fill=(255, 214, 130))
d.text((W - 24, 96), "WORLD NEWS", font=font(SANS_B, 22),
       fill=(200, 215, 235), anchor="ra")

MX = 24          # margin
CW = W - 2 * MX  # content width

# ================================================================ LEAD
# Lead panel: illustration left, text right. y 140..512
ly0, ly1 = 140, 512
d.rectangle([MX, ly0, W - MX, ly1], outline=INK, width=2)
ix0, iy0, ix1, iy1 = MX + 2, ly0 + 2, MX + 470, ly1 - 2
# --- bridge illustration: dusk sky, sea, broken bridge
for i in range(iy1 - iy0):
    t = i / max(1, iy1 - iy0)
    d.line([(ix0, iy0 + i), (ix1, iy0 + i)],
           fill=(int(240 - 150 * t), int(180 - 60 * t), int(120 + 40 * t)))
d.rectangle([ix0, iy0 + 235, ix1, iy1], fill=(38, 84, 120))  # sea
for k in range(6):  # waves
    yy = iy0 + 255 + k * 18
    d.arc([ix0 + 10 + k * 70, yy, ix0 + 70 + k * 70, yy + 16], 180, 360,
          fill=(180, 210, 230), width=3)
# bridge deck: left span, gap, right span (collapsed arch in the gap)
deck_y = iy0 + 205
d.rectangle([ix0, deck_y, ix0 + 185, deck_y + 14], fill=(60, 60, 66))
d.rectangle([ix0 + 300, deck_y, ix1, deck_y + 14], fill=(60, 60, 66))
d.polygon([(ix0 + 185, deck_y + 14), (ix0 + 235, deck_y + 78),
           (ix0 + 265, deck_y + 78), (ix0 + 300, deck_y + 14)],
          fill=(90, 90, 96))  # fallen span in the water
d.line([(ix0 + 185, deck_y), (ix0 + 185, deck_y - 62)], fill=(60, 60, 66), width=6)
d.line([(ix0 + 300, deck_y), (ix0 + 300, deck_y - 62)], fill=(60, 60, 66), width=6)
d.arc([ix0 + 60, deck_y - 78, ix0 + 185, deck_y + 6], 180, 360,
      fill=(200, 200, 205), width=7)  # standing arch, left
# smoke cloud over the gap (one soft horizontal cloud, not round blobs)
for cx, cy, r in [(ix0 + 245, deck_y - 62, 30), (ix0 + 222, deck_y - 48, 20),
                  (ix0 + 268, deck_y - 48, 20)]:
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(105, 105, 108))
for ang in range(0, 360, 45):
    a = math.radians(ang)
    d.line([(ix0 + 245, deck_y - 30),
            (ix0 + 245 + 26 * math.cos(a), deck_y - 30 + 26 * math.sin(a))],
           fill=(255, 190, 60), width=5)
d.text((ix0 + 14, iy0 + 12), "KERCH STRAIT", font=font(SANS_B, 17),
       fill=(255, 255, 255))
# --- lead text
tx = MX + 492
y = ly0 + 14
y = kicker(d, tx, y, "War in Ukraine  •  Lead story")
y = headline(d, tx, y, "Bridges at war", CW - 492, size=44)
y = headline(d, tx, y + 2, "Ukraine wrecks Crimea bridge as Russia hits Kyiv's",
             CW - 492, size=27)
y = para(d, tx, y + 8,
         "Ukraine destroyed the road arch of the 19-km Crimea bridge in a "
         "second straight day of strikes. Overnight, Russia hit Kyiv's "
         "North and South bridges, cutting power and water in the capital.",
         font(SANS, 21), CW - 492)
y = para(d, tx, y + 6,
         "Two people were killed in the Crimea strike, its governor said; "
         "traffic across the bridge is suspended.",
         font(SANS, 19), CW - 492, fill=(70, 70, 70))

# ================================================================ ROW 2 (two panels)
ry0, ry1 = 524, 758
half = (CW - 16) // 2
panels = [(MX, MX + half), (MX + half + 16, W - MX)]
for x0, x1 in panels:
    d.rectangle([x0, ry0, x1, ry1], outline=INK, width=2)

# --- panel A: Trump / Manila (left)
x0, x1 = panels[0]
ax0, ay0, ax1, ay1 = x0 + 2, ry0 + 2, x1 - 2, ry0 + 96
d.rectangle([ax0, ay0, ax1, ay1], fill=(126, 178, 214))  # sky
d.rectangle([ax0, ay1 - 26, ax1, ay1], fill=(52, 84, 60))  # ground
# four flags on poles: US, India, Japan, Australia
flags = [((178, 34, 34), (255, 255, 255)), ((255, 153, 51), (19, 136, 8)),
         ((255, 255, 255), (188, 0, 45)), ((0, 40, 104), (255, 255, 255))]
for i, (c1, c2) in enumerate(flags):
    fx = ax0 + 28 + i * 108
    d.line([(fx, ay0 + 18), (fx, ay1 - 26)], fill=(40, 40, 40), width=4)
    d.rectangle([fx, ay0 + 18, fx + 78, ay0 + 52], fill=c1, outline=(40, 40, 40))
    if i == 0:
        d.rectangle([fx, ay0 + 18, fx + 34, ay0 + 52], fill=(30, 40, 90))
    elif i == 1:
        d.rectangle([fx, ay0 + 29, fx + 78, ay0 + 41], fill=(255, 255, 255))
        d.ellipse([fx + 34, ay0 + 26, fx + 44, ay0 + 36], outline=(0, 0, 128), width=2)
    elif i == 2:
        d.ellipse([fx + 29, ay0 + 24, fx + 49, ay0 + 44], fill=c2)
    else:
        for sx, sy in [(18, 8), (58, 8), (38, 22)]:
            d.ellipse([fx + sx, ay0 + sy, fx + sx + 6, ay0 + sy + 6], fill=(255, 255, 255))
y = ry0 + 106
y = kicker(d, x0 + 14, y, "Asia  •  Manila", color=NAVY2)
y = headline(d, x0 + 14, y, "Trump at the Quad", half - 28, size=28)
para(d, x0 + 14, y + 4,
     "First Quad leaders' summit since 2024; meets Marcos Jr. today, "
     "then on to Xi\u2013Putin talks.",
     font(SANS, 18), half - 28)

# --- panel B: Nvidia (right)
x0, x1 = panels[1]
ax0, ay0, ax1, ay1 = x0 + 2, ry0 + 2, x1 - 2, ry0 + 96
d.rectangle([ax0, ay0, ax1, ay1], fill=(16, 46, 32))  # dark green
# chip + rising bars
d.rectangle([ax0 + 30, ay0 + 28, ax0 + 118, ay0 + 92], fill=(34, 139, 34),
            outline=(140, 220, 140), width=3)
d.rectangle([ax0 + 52, ay0 + 48, ax0 + 96, ay0 + 72], fill=(16, 46, 32),
            outline=(140, 220, 140), width=2)
for px in range(ax0 + 38, ax0 + 112, 14):
    d.line([(px, ay0 + 20), (px, ay0 + 28)], fill=(140, 220, 140), width=3)
    d.line([(px, ay0 + 92), (px, ay0 + 100)], fill=(140, 220, 140), width=3)
bars = [20, 32, 26, 44, 60]
for i, bh in enumerate(bars):
    bx = ax0 + 150 + i * 58
    d.rectangle([bx, ay1 - 14 - bh, bx + 40, ay1 - 14], fill=(118, 185, 0))
d.line([(ax0 + 145, ay1 - 14 - 52), (ax1 - 30, ay1 - 14 - 68)],
       fill=(255, 214, 130), width=4)
y = ry0 + 106
y = kicker(d, x0 + 14, y, "Business  •  AI chips", color=(0, 110, 40))
y = headline(d, x0 + 14, y, "Nvidia beats, guides $130bn", half - 28, size=28)
para(d, x0 + 14, y + 4,
     "Revenue $115.8bn, up 103% in a year. Board: Huang will not "
     "return as chief executive.",
     font(SANS, 18), half - 28)

# ================================================================ ROW 3 (three panels)
by0, by1 = 770, 978
third = (CW - 32) // 3
cols = [(MX + i * (third + 16), MX + i * (third + 16) + third) for i in range(3)]
for x0, x1 in cols:
    d.rectangle([x0, by0, x1, by1], outline=INK, width=2)

# --- UK sanctions
x0, x1 = cols[0]
ax0, ay0, ax1, ay1 = x0 + 2, by0 + 2, x1 - 2, by0 + 72
d.rectangle([ax0, ay0, ax1, ay1], fill=(232, 222, 200))
d.rectangle([ax0 + 26, ay0 + 34, ax0 + 86, ay0 + 78], fill=(120, 110, 95))
d.rectangle([ax0 + 96, ay0 + 22, ax0 + 156, ay0 + 78], fill=(150, 138, 118))
d.rectangle([ax0 + 166, ay0 + 44, ax0 + 216, ay0 + 78], fill=(120, 110, 95))
for wx in (ax0 + 38, ax0 + 108, ax0 + 178):
    d.rectangle([wx, ay0 + 46, wx + 12, ay0 + 60], fill=(255, 240, 180))
d.ellipse([ax1 - 108, ay0 + 8, ax1 - 28, ay0 + 88], outline=RED, width=6)
d.line([(ax1 - 96, ay0 + 20), (ax1 - 40, ay0 + 76)], fill=RED, width=6)
y = by0 + 80
y = kicker(d, x0 + 12, y, "Britain", size=17)
y = headline(d, x0 + 12, y, "UK sanctions 8 settlement firms", third - 24, size=22)
para(d, x0 + 12, y + 2,
     "Asset freezes over West Bank building; Tzav 9 also hit.",
     font(SANS, 17), third - 24)

# --- Cyclone Akvan
x0, x1 = cols[1]
ax0, ay0, ax1, ay1 = x0 + 2, by0 + 2, x1 - 2, by0 + 72
d.rectangle([ax0, ay0, ax1, ay1], fill=(28, 68, 110))
d.rectangle([ax0, ay1 - 22, ax1, ay1], fill=(52, 110, 70))  # coast
cx, cy = (ax0 + ax1) // 2 - 30, ay0 + 38
for r, wdt in [(36, 5), (27, 5), (18, 5), (10, 5)]:
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=wdt)
d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 214, 130))
y = by0 + 80
y = kicker(d, x0 + 12, y, "Weather  •  Bay of Bengal", color=TEAL, size=17)
y = headline(d, x0 + 12, y, "Cyclone Akvan strengthens", third - 24, size=22)
para(d, x0 + 12, y + 2,
     "Andhra Pradesh and Odisha on alert; landfall due ~20 Nov.",
     font(SANS, 17), third - 24)

# --- Dhoni
x0, x1 = cols[2]
ax0, ay0, ax1, ay1 = x0 + 2, by0 + 2, x1 - 2, by0 + 72
d.rectangle([ax0, ay0, ax1, ay1], fill=(46, 125, 50))
d.rectangle([ax0 + 90, ay0 + 8, ax0 + 150, ay1 - 8], fill=(214, 186, 140))  # pitch
d.line([(ax0 + 120, ay0 + 8), (ax0 + 120, ay1 - 8)], fill=(255, 255, 255), width=2)
for sx in (ax0 + 104, ax0 + 118, ax0 + 132):
    d.line([(sx, ay0 + 16), (sx, ay0 + 30)], fill=(255, 235, 59), width=4)
d.line([(ax0 + 190, ay0 + 62), (ax0 + 235, ay0 + 22)], fill=(222, 184, 135), width=12)
d.ellipse([ax0 + 238, ay0 + 12, ax0 + 258, ay0 + 32], fill=RED)
y = by0 + 80
y = kicker(d, x0 + 12, y, "Sport  •  Cricket", color=(0, 110, 40), size=17)
y = headline(d, x0 + 12, y, "Dhoni bows out of the IPL", third - 24, size=22)
para(d, x0 + 12, y + 2,
     "MS Dhoni ends his IPL playing career; becomes CSK mentor.",
     font(SANS, 17), third - 24)

# ---------------------------------------------------------------- footer
d.rectangle([MX, 990, W - MX, 992], fill=(120, 110, 90))
d.text((MX, 998), "Sources: Reuters  •  AP  •  CNN  •  SiliconANGLE  —  reported 18 November 2026",
       font=font(SANS, 14), fill=GREY)
d.text((W - MX, 998), "make.fun  •  news-image-20261118", font=font(SANS, 14),
       fill=GREY, anchor="ra")

img.save("entry.png", optimize=True)
print("saved entry.png")
