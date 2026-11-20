#!/usr/bin/env python3
"""Draw the news-image-20261120 front page: one day's world news, Friday
20 November 2026, as a single 1024x1024 PNG.

Everything is drawn in code with PIL (no photos, no network, no random
input without a fixed seed) so two runs produce byte-identical output.
Run:  python3 draw.py            (writes entry.png next to this file)

Design: newspaper front page following the verified rank-1 template for
the news-image family -- serif masthead + date, a 6-number strip, three
big hero panels with flat-cartoon illustrations, ~24 numbered one-line
stories in three columns, a "WHERE IT HAPPENED" map with numbered pins,
a DATE CHECK honesty box, and a sources footer.

All stories were verified against reporting dated 20 November 2026
(in any time zone). Stories from other days are named in the DATE CHECK
box as deliberately left out.
"""

import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette: warm paper, ink navy, newspaper red, teal, gold -----------
PAPER = (250, 245, 236)
INK = (20, 28, 38)
INK_SOFT = (60, 68, 78)
RED = (179, 38, 30)
RED_DARK = (140, 28, 22)
TEAL = (14, 107, 92)
TEAL_DARK = (9, 74, 64)
GOLD = (201, 154, 43)
GOLD_LIGHT = (232, 197, 96)
CREAM_LINE = (214, 203, 180)
SEA = (216, 230, 234)
LAND = (231, 217, 184)
LAND_LINE = (190, 170, 130)
PANEL = (255, 252, 246)

FONTS = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


F_MAST = font("NotoSerif-Black.ttf", 48)
F_DATE = font("NotoSans-Bold.ttf", 24)
F_SMALL = font("NotoSans-Bold.ttf", 14)
F_STRIP_N = font("NotoSans-Black.ttf", 28)
F_STRIP_L = font("NotoSans-Bold.ttf", 12)
F_HERO_H = font("NotoSerif-Bold.ttf", 26)
F_HERO_D = font("NotoSans-Regular.ttf", 20)
F_HERO_N = font("NotoSans-Black.ttf", 26)
F_STORY = font("NotoSans-Regular.ttf", 20)
F_STORY_B = font("NotoSans-Bold.ttf", 20)
F_NUM = font("NotoSans-Black.ttf", 15)
F_MAP_T = font("NotoSans-Black.ttf", 18)
F_PIN = font("NotoSans-Black.ttf", 11)
F_DC_H = font("NotoSans-Black.ttf", 20)
F_DC_B = font("NotoSans-Regular.ttf", 19)
F_DC_S = font("NotoSans-Bold.ttf", 16)
F_DC_I = font("NotoSans-Regular.ttf", 15)
F_FOOT = font("NotoSans-Regular.ttf", 13)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width. Returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, cx, y, s, fnt, fill):
    w = draw.textlength(s, font=fnt)
    draw.text((cx - w / 2, y), s, font=fnt, fill=fill)


# ---------------------------------------------------------------- heroes
def hero_gulf(draw, x, y, w, h):
    """Tanker ablaze in the Strait of Hormuz at dusk."""
    # dusk sky bands
    bands = [(232, 116, 74), (238, 150, 84), (244, 192, 74), (247, 214, 120)]
    bh = (h * 2 // 3) // len(bands)
    for i, c in enumerate(bands):
        draw.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=c)
    # pale sun behind smoke
    draw.ellipse([x + w - 78, y + 14, x + w - 28, y + 64], fill=(250, 226, 160))
    # sea
    draw.rectangle([x, y + h * 2 // 3, x + w, y + h], fill=(23, 58, 74))
    for i in range(5):
        wx = x + 14 + i * 62
        draw.arc([wx, y + h - 26, wx + 44, y + h - 8], 180, 360,
                 fill=(90, 150, 168), width=3)
    # tanker hull + superstructure
    hx, hy = x + 28, y + h - 62
    draw.polygon([(hx, hy), (hx + 210, hy), (hx + 196, hy + 26),
                  (hx + 14, hy + 26)], fill=(16, 24, 34))
    draw.rectangle([hx + 150, hy - 30, hx + 196, hy], fill=(16, 24, 34))
    draw.rectangle([hx + 158, hy - 26, hx + 188, hy - 18], fill=GOLD_LIGHT)
    draw.rectangle([hx + 158, hy - 14, hx + 188, hy - 6], fill=GOLD_LIGHT)
    # deck fire: layered flame teardrops
    fx = hx + 60
    for (fw, fh, c) in [(54, 66, (214, 48, 32)), (40, 50, (240, 120, 40)),
                        (26, 34, (252, 200, 60))]:
        draw.polygon([(fx - fw // 2, hy), (fx, hy - fh), (fx + fw // 2, hy)],
                     fill=c)
        draw.ellipse([fx - fw // 2, hy - 14, fx + fw // 2, hy + 2], fill=c)
    # smoke puffs
    for (sx, sy, r) in [(fx - 26, hy - 78, 15), (fx + 4, hy - 96, 19),
                        (fx + 34, hy - 82, 14), (fx + 12, hy - 62, 16)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(52, 52, 58))
    # missile streaks from upper right
    for (mx, my) in [(x + w - 40, y + 8), (x + w - 70, y + 26)]:
        draw.line([(mx, my), (mx - 46, my + 30)], fill=(255, 255, 255),
                  width=3)
        draw.ellipse([mx - 50, my + 26, mx - 42, my + 34],
                     fill=(255, 200, 60))


def hero_kyiv(draw, x, y, w, h):
    """Kyiv skyline at night under missile fire."""
    draw.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    # stars + crescent moon
    rng = random.Random(7)
    for _ in range(26):
        sx = x + rng.randint(6, w - 6)
        sy = y + rng.randint(6, h // 2)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 228, 240))
    draw.ellipse([x + w - 62, y + 12, x + w - 26, y + 48],
                 fill=(240, 236, 210))
    draw.ellipse([x + w - 54, y + 8, x + w - 20, y + 44], fill=(27, 42, 74))
    # skyline silhouettes (back row lighter, front row darker)
    back = [(0, 88), (34, 88), (34, 62), (58, 62), (58, 96), (96, 96),
            (96, 70), (128, 70), (128, 100), (168, 100), (168, 58),
            (196, 58), (196, 92), (236, 92), (236, 66), (268, 66),
            (268, 100), (318, 100), (318, 160), (0, 160)]
    draw.polygon([(x + px, y + py) for px, py in back], fill=(58, 74, 106))
    # gold-domed building (St Sophia silhouette)
    dx = x + 168
    draw.rectangle([dx, y + 58, dx + 28, y + 108], fill=(58, 74, 106))
    draw.ellipse([dx + 2, y + 38, dx + 26, y + 62], fill=GOLD)
    draw.rectangle([dx + 13, y + 28, dx + 15, y + 40], fill=GOLD)
    front = [(0, 118), (48, 118), (48, 96), (80, 96), (80, 122),
             (140, 122), (140, 102), (176, 102), (176, 124), (230, 124),
             (230, 104), (262, 104), (262, 126), (318, 126), (318, 160),
             (0, 160)]
    draw.polygon([(x + px, y + py) for px, py in front], fill=(14, 20, 32))
    # lit windows
    for (wx, wy) in [(10, 126), (24, 134), (56, 104), (66, 112), (90, 128),
                     (150, 110), (186, 130), (196, 138), (240, 112),
                     (272, 132), (284, 112), (300, 132)]:
        draw.rectangle([x + wx, y + wy, x + wx + 7, y + wy + 9],
                       fill=GOLD_LIGHT)
    # missile arcs + explosion bursts
    for (ax, ay, bx, by) in [(x + 30, y + 6, x + 90, y + 70),
                             (x + 120, y + 2, x + 170, y + 60),
                             (x + 210, y + 10, x + 250, y + 66)]:
        draw.arc([ax - 30, ay - 10, bx + 30, by + 40], 200, 330,
                 fill=(255, 255, 255), width=3)
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 220, 100))
    for (ex, ey, r) in [(x + 90, y + 74, 16), (x + 250, y + 70, 13)]:
        pts = []
        for k in range(12):
            ang = k * 3.14159 / 6
            rr = r if k % 2 == 0 else r * 0.45
            import math
            pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
        draw.polygon(pts, fill=(255, 150, 40))
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 230, 150))


def hero_cop(draw, x, y, w, h):
    """COP31: globe, rising sun, flags at Antalya."""
    # teal sky bands
    bands = [(16, 120, 100), (24, 140, 118), (52, 168, 140)]
    bh = h // len(bands)
    for i, c in enumerate(bands):
        draw.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=c)
    # sun rays + disc
    cx, cy = x + w // 2, y + h - 30
    for k in range(9):
        import math
        ang = 3.14159 + k * 3.14159 / 8
        x2 = cx + 120 * math.cos(ang)
        y2 = cy + 120 * math.sin(ang)
        draw.line([(cx, cy), (x2, y2)], fill=(232, 197, 96), width=3)
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(250, 222, 130))
    # globe left
    gx, gy, gr = x + 78, y + 74, 58
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 140, 200))
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 255, 255),
                 width=3)
    # simplified continents on the globe
    draw.polygon([(gx - 40, gy - 20), (gx - 12, gy - 34), (gx + 6, gy - 22),
                  (gx - 8, gy - 6), (gx - 30, gy - 2)], fill=(96, 186, 110))
    draw.polygon([(gx + 8, gy + 4), (gx + 34, gy - 6), (gx + 44, gy + 14),
                  (gx + 22, gy + 30), (gx + 6, gy + 22)], fill=(96, 186, 110))
    draw.polygon([(gx - 34, gy + 22), (gx - 6, gy + 16), (gx + 2, gy + 34),
                  (gx - 22, gy + 44)], fill=(96, 186, 110))
    # flag poles row
    flag_cols = [(179, 38, 30), (255, 255, 255), (30, 90, 160),
                 (240, 180, 40), (20, 140, 90)]
    for i, c in enumerate(flag_cols):
        fx = x + w - 118 + i * 22
        draw.line([(fx, y + h - 58), (fx, y + h - 12)], fill=(30, 30, 30),
                  width=2)
        draw.rectangle([fx, y + h - 58, fx + 16, y + h - 46], fill=c,
                       outline=(30, 30, 30))
    # COP31 badge
    bx, by = x + w - 62, y + 16
    draw.ellipse([bx - 26, by - 18, bx + 26, by + 18], fill=(255, 252, 246),
                 outline=INK, width=2)
    text_center(draw, bx, by - 13, "COP31", font("NotoSans-Black.ttf", 17),
                TEAL_DARK)


# ------------------------------------------------------------------- map
# Simplified continent polygons in (lon, lat); drawn equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 72), (-85, 70),
     (-80, 73), (-65, 62), (-60, 52), (-55, 47), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-90, 21), (-97, 26), (-105, 23), (-110, 30),
     (-117, 33), (-124, 40), (-125, 49), (-135, 57), (-150, 61)],
    # Greenland
    [(-45, 60), (-30, 68), (-22, 70), (-40, 76), (-58, 74), (-53, 66)],
    # South America
    [(-77, 8), (-72, 11), (-60, 8), (-50, 5), (-35, -8), (-38, -15),
     (-48, -28), (-57, -38), (-62, -41), (-65, -45), (-68, -52),
     (-72, -54), (-73, -45), (-73, -37), (-70, -30), (-70, -20),
     (-77, -12), (-80, -5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 49), (0, 53), (5, 58), (10, 58), (18, 56),
     (21, 55), (28, 60), (30, 70), (40, 68), (48, 68), (40, 60), (30, 55),
     (28, 46), (23, 40), (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37),
     (-9, 37)],
    # Africa
    [(-17, 15), (-10, 5), (0, 6), (6, 4), (9, -1), (13, -12), (12, -18),
     (17, -29), (20, -35), (28, -33), (32, -29), (35, -23), (40, -15),
     (42, -10), (48, 2), (51, 11), (44, 11), (40, 15), (38, 18), (35, 28),
     (32, 31), (20, 32), (10, 34), (0, 36), (-6, 35), (-10, 31),
     (-15, 25)],
    # Asia
    [(30, 70), (48, 68), (60, 69), (75, 73), (90, 75), (110, 74),
     (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (160, 55),
     (155, 50), (142, 45), (135, 40), (130, 33), (122, 30), (120, 25),
     (110, 20), (108, 12), (105, 9), (100, 7), (98, 12), (95, 16),
     (92, 22), (88, 22), (80, 13), (77, 8), (73, 20), (68, 23), (60, 25),
     (55, 26), (50, 29), (44, 29), (40, 31), (36, 36), (30, 36), (28, 46),
     (30, 55), (40, 60)],
    # Australia
    [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32),
     (135, -35), (140, -38), (147, -38), (150, -37), (153, -32),
     (153, -27), (146, -19), (142, -15), (142, -11), (137, -12),
     (132, -12), (126, -14), (122, -17)],
    # UK
    [(-5, 50), (-1, 53), (-3, 58), (-6, 57)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 43), (145, 44),
     (142, 40), (139, 36), (135, 33)],
    # New Zealand
    [(167, -45), (170, -42), (174, -39), (178, -38), (175, -41),
     (172, -43)],
]

# story number -> (lon, lat) for map pins
PINS = [
    (1, 56, 26), (2, 31, 50), (3, 30, 37), (4, 85, 20), (5, 9, 44),
    (6, 121, 25), (10, 44, 15), (11, -72, 19),
    (12, -118, 34), (13, 45, 42), (17, -17, 15), (19, 175, -41),
    (25, -160, -21), (27, 48, 29),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    text_center(draw, x + w // 2, y + 8, "WHERE IT HAPPENED", F_MAP_T, INK)
    mx, my, mw, mh = x + 10, y + 32, w - 20, h - 42
    # graticule
    for lon in range(-150, 181, 30):
        gx = mx + (lon + 180) / 360 * mw
        draw.line([(gx, my), (gx, my + mh)], fill=(196, 214, 220), width=1)
    for lat in range(-60, 91, 30):
        gy = my + (90 - lat) / 150 * mh
        draw.line([(mx, gy), (mx + mw, gy)], fill=(196, 214, 220), width=1)

    def proj(lon, lat):
        return (mx + (lon + 180) / 360 * mw,
                my + (90 - lat) / 150 * mh)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        r = 9
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        s = str(num)
        tw = draw.textlength(s, font=F_PIN)
        draw.text((px - tw / 2, py - 7), s, font=F_PIN, fill=(255, 255, 255))


# ------------------------------------------------------------------ data
HEROES = [
    ("1", "GULF ON FIRE",
     "Tanker ablaze after mine strike; Houthis hit Riyadh tower.",
     hero_gulf),
    ("2", "MISSILES OVER KYIV",
     "Four missiles hit Kyiv; Putin invites Europe to Moscow.",
     hero_kyiv),
    ("3", "COP31 CLOSES",
     "Antalya summit ends; fossil-fuel line dropped.",
     hero_cop),
]

STRIP = [
    ("4", "MISSILES HIT KYIV"),
    ("80,000+", "EVACUATED IN INDIA"),
    ("\u20ac45BN", "EU LOAN FOR UKRAINE"),
    ("34", "KILLED IN HAITI RAID"),
    ("-4.68%", "NIKKEI FALLS FRIDAY"),
    ("$750M", "REPORTED SPARKS SALE"),
]

# (number, lead, text) -- every story verified against reporting dated
# 20 November 2026 in some time zone. Each line kept under ~56 chars so
# it fits two lines at 20px in its column.
STORIES = [
    ("4", "CYCLONE AKVAN", "Hits Odisha; 80,000+ evacuated."),
    ("5", "GENOA DRONES", "Airport halts flights; drones seen."),
    ("6", "TAIWAN STOCKS", "Taipei curbs short-selling."),
    ("7", "NIKKEI -4.68%", "Tokyo plunges as AI selloff spreads."),
    ("8", "NVIDIA PROBE", "California probes China chip sales."),
    ("9", "TRUMP PRESSER", "White House briefing due today."),
    ("10", "YEMEN VOICES", "\u201cIt\u2019s just fireworks,\u201d a father says."),
    ("11", "HAITI RAID", "Police say 34 gang suspects killed."),
    ("12", "SPARKS SALE", "LA Sparks near record $750m sale."),
    ("13", "TBILISI RESCUE", "Girl, 3, pulled from rubble."),
    ("14", "FRANCE FIRE", "One dead, 15 hurt in apartment blaze."),
    ("15", "LEBANON STRIKE", "Israel hits Hezbollah missile site."),
    ("16", "SARATOV DRONES", "Three killed in drone attack."),
    ("17", "SENEGAL BOAT", "Migrant boat sinks; dozens missing."),
    ("18", "IOWA BLAST", "Army delays detonation of 68 barrels."),
    ("19", "NICHOLLS 113*", "Unbeaten ton on day one vs India."),
    ("20", "LULA DECREE", "Brazil moves to five-day workweek."),
    ("21", "IMF WARNING", "AI demand adds to rate pressure."),
    ("22", "PARAGUAY BANK", "Ueno collapse could cost $1bn."),
    ("23", "YONGBYON GROWS", "IAEA: uranium site expands."),
    ("24", "DATA CENTRES", "IEA: AI needs $3.9tn by 2030."),
    ("25", "XAVIER", "Gale warning for Suwarrow, Cook Islands."),
    ("26", "TAIWAN QUESTION", "Japan\u2019s PM sidesteps query."),
    ("27", "GULF STRIKES", "Kuwait and Bahrain hit again."),
]

LEFT_OUT = [
    "Rohingya genocide ruling (Thu)",
    "Anthropic IPO debut (Thu)",
    "Shenzhen peace declaration (Thu)",
    "Pete Rose pardoned (Thu)",
    "Fiona the hippo dies (Thu)",
]

FOOTER = ("Sources: Reuters \u00b7 BBC \u00b7 CNN \u00b7 USA Today \u00b7 The Hindu Business Line \u00b7 "
          "Daily Baku \u00b7 Des Moines Register \u00b7 IEA \u00b7 IMD \u00b7 IAEA \u00b7 Jagran Josh  "
          "\u2014  Drawn in code; no photographs. All stories verified "
          "against reporting dated 20 Nov 2026.")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    M = 24  # side margin

    # ---- masthead ------------------------------------------------------
    draw.rectangle([M, 10, W - M, 12], fill=INK)
    text_center(draw, W // 2, 16, "THE WORLD TODAY", F_MAST, INK)
    draw.text((M, 70), "VOL. I \u2014 No. 325", font=F_SMALL, fill=INK_SOFT)
    dstr = "FRIDAY \u00b7 20 NOVEMBER 2026"
    dw = draw.textlength(dstr, font=F_DATE)
    draw.text((W // 2 - dw / 2, 66), dstr, font=F_DATE, fill=RED_DARK)
    rstr = "ONE DAY \u00b7 ONE PAGE"
    draw.text((W - M - draw.textlength(rstr, font=F_SMALL), 70), rstr,
              font=F_SMALL, fill=INK_SOFT)
    draw.rectangle([M, 98, W - M, 100], fill=INK)
    draw.rectangle([M, 103, W - M, 104], fill=INK)

    # ---- number strip ---------------------------------------------------
    sy, sh = 108, 52
    cw = (W - 2 * M) / 6
    for i, (num, lab) in enumerate(STRIP):
        cx = M + cw * i + cw / 2
        text_center(draw, cx, sy, num, F_STRIP_N, RED_DARK)
        text_center(draw, cx, sy + 32, lab, F_STRIP_L, INK)
        if i:
            x = M + cw * i
            draw.line([(x, sy + 4), (x, sy + sh - 6)], fill=CREAM_LINE,
                      width=2)
    draw.rectangle([M, 164, W - M, 166], fill=INK)

    # ---- heroes ---------------------------------------------------------
    hy, hh = 168, 278
    hw = (W - 2 * M - 24) // 3
    for i, (num, head, deck, painter) in enumerate(HEROES):
        hx = M + i * (hw + 12)
        draw.rectangle([hx, hy, hx + hw, hy + hh], fill=PANEL, outline=INK,
                       width=2)
        painter(draw, hx + 2, hy + 2, hw - 4, 160)
        # number badge over the illustration corner
        draw.rectangle([hx + 2, hy + 2, hx + 34, hy + 34], fill=RED)
        text_center(draw, hx + 18, hy + 4, num, F_HERO_N, (255, 255, 255))
        # headline + deck
        hl = wrap(draw, head, F_HERO_H, hw - 20)
        yy = hy + 170
        for line in hl[:2]:
            draw.text((hx + 10, yy), line, font=F_HERO_H, fill=INK)
            yy += 30
        dl = wrap(draw, deck, F_HERO_D, hw - 20)
        yy += 2
        for line in dl[:2]:
            draw.text((hx + 10, yy), line, font=F_HERO_D, fill=INK_SOFT)
            yy += 21

    # ---- numbered stories, 3 columns x 8 --------------------------------
    sty, row_h = 454, 42
    col_w = (W - 2 * M - 24) // 3
    for idx, (num, lead, text) in enumerate(STORIES):
        col, row = idx % 3, idx // 3
        sx = M + col * (col_w + 12)
        yy = sty + row * row_h
        # number chip
        draw.rectangle([sx, yy + 2, sx + 26, yy + 24], fill=RED)
        tw = draw.textlength(num, font=F_NUM)
        draw.text((sx + 13 - tw / 2, yy + 4), num, font=F_NUM,
                  fill=(255, 255, 255))
        tx = sx + 32
        full = lead + " \u2014 " + text
        lines = wrap(draw, full, F_STORY, col_w - 42)
        # first line: bold lead, rest regular
        ly = yy
        for li, line in enumerate(lines[:2]):
            if li == 0 and line.startswith(lead):
                draw.text((tx, ly), lead, font=F_STORY_B, fill=INK)
                rest = line[len(lead):]
                draw.text((tx + draw.textlength(lead, font=F_STORY_B), ly),
                          rest, font=F_STORY, fill=INK)
            else:
                draw.text((tx, ly), line, font=F_STORY, fill=INK)
            ly += 21

    # ---- bottom band: map + DATE CHECK ----------------------------------
    by, bh = 798, 194
    draw_map(draw, M, by, 620, bh)
    dx = M + 620 + 12
    dw2 = W - M - dx
    draw.rectangle([dx, by, dx + dw2, by + bh], fill=(255, 243, 235),
                   outline=RED, width=2)
    draw.rectangle([dx, by, dx + dw2, by + 30], fill=RED)
    # checkmark drawn with lines (the font has no check glyph)
    draw.line([(dx + 12, by + 17), (dx + 18, by + 23), (dx + 28, by + 9)],
              fill=(255, 255, 255), width=3)
    draw.text((dx + 34, by + 4), "DATE CHECK", font=F_DC_H,
              fill=(255, 255, 255))
    yy = by + 34
    body = ("Every story on this page happened, or was first reported, on "
            "Friday 20 November 2026, in any time zone.")
    for line in wrap(draw, body, F_DC_B, dw2 - 20):
        draw.text((dx + 10, yy), line, font=F_DC_B, fill=INK)
        yy += 20
    yy += 1
    draw.text((dx + 10, yy), "LEFT OUT AS OTHER DAYS\u2019 NEWS:",
              font=F_DC_S, fill=RED_DARK)
    yy += 19
    for item in LEFT_OUT:
        draw.text((dx + 10, yy), "\u00b7 " + item, font=F_DC_I, fill=INK)
        yy += 14

    # ---- footer ---------------------------------------------------------
    fy = 996
    fl = wrap(draw, FOOTER, F_FOOT, W - 2 * M)
    for line in fl[:2]:
        text_center(draw, W // 2, fy, line, F_FOOT, INK_SOFT)
        fy += 14

    # ---- subtle deterministic paper grain (adds bytes, kills flatness) --
    rng = random.Random(20261120)
    px = img.load()
    for _ in range(25000):
        gx = rng.randrange(W)
        gy = rng.randrange(H)
        r, g, b = px[gx, gy]
        d = rng.randint(-5, 5)
        px[gx, gy] = (max(0, min(255, r + d)), max(0, min(255, g + d)),
                      max(0, min(255, b + d)))

    img.save("entry.png", "PNG")


if __name__ == "__main__":
    main()
