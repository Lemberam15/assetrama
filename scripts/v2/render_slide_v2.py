#!/usr/bin/env python3
"""Asset Rama slide renderer v2 (approved 24/11/2026).
Dark glass template: animated-ready header, glass point cards, content-aware
icons, tone colours, marker-swipe question, gradient CTA.

    python render_slide_v2.py spec.json slide.png          # the 4:5 slide
    python render_slide_v2.py spec.json slide.png --cards  # + hook/beat/send cards
"""
import os, sys, json, math, random, urllib.request
import numpy as np
from PIL import ImageChops
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets_v2")
FONT_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-%s.ttf"
LOGO_URL = "https://raw.githubusercontent.com/Lemberam15/assetrama/main/logo-mark.png"


def _need(path, url):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path)
    return path


for _s in ("Bold", "SemiBold", "Medium", "Regular"):
    _need(os.path.join(ASSETS, "Poppins-%s.ttf" % _s), FONT_BASE % _s)
LOGO_PATH = _need(os.path.join(ASSETS, "logo-mark.png"), LOGO_URL)
W, H = 1080, 1350
def F(style, size):
    return ImageFont.truetype(os.path.join(ASSETS, "Poppins-%s.ttf" % style), size)

TONES = {
    "caution":  dict(accent=(255, 176, 58), deep=(255, 132, 18), on=(26, 18, 6)),
    "bullish":  dict(accent=(46, 226, 122), deep=(16, 185, 96),  on=(6, 24, 14)),
    "bearish":  dict(accent=(255, 92, 92),  deep=(226, 44, 44),  on=(28, 8, 8)),
    "neutral":  dict(accent=(96, 178, 255), deep=(52, 130, 240), on=(8, 16, 28)),
    "festival": dict(accent=(255, 150, 60), deep=(240, 110, 30), on=(30, 16, 4)),
}

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ---------------- background plate ----------------
def background(accent, seed):
    rnd = random.Random(seed)
    img = Image.new("RGB", (W, H), (8, 11, 18))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=lerp((16, 22, 36), (5, 7, 12), t))

    # big top-biased glow
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for cx, cy, r, amt in [(860, 120, 760, 150), (150, 1180, 620, 60)]:
        steps = 46
        for i in range(steps, 0, -1):
            rr = r * i / steps
            v = int(amt * (1 - i / steps) ** 1.6)
            md.ellipse([cx - rr, cy - rr * 0.95, cx + rr, cy + rr * 0.95], fill=v)
    mask = mask.filter(ImageFilter.GaussianBlur(70))
    glow = Image.new("RGB", (W, H), accent)
    img = Image.composite(glow, img, mask.point(lambda v: int(v * 0.55)))

    # blurred candlestick bokeh, top right (stands in for a photo plate)
    bars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bars)
    x = 640
    while x < 1060:
        h = rnd.randint(30, 130)
        y0 = rnd.randint(120, 330)
        up = rnd.random() > 0.45
        col = (60, 220, 140, 70) if up else (255, 80, 80, 70)
        w = rnd.randint(14, 26)
        bd.rounded_rectangle([x, y0, x + w, y0 + h], 6, fill=col)
        bd.line([(x + w // 2, y0 - 18), (x + w // 2, y0 + h + 18)], fill=col, width=3)
        x += rnd.randint(40, 66)
    bars = bars.filter(ImageFilter.GaussianBlur(7))
    img = Image.alpha_composite(img.convert("RGBA"), bars)

    # bokeh dots
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bkd = ImageDraw.Draw(bok)
    for _ in range(26):
        cx, cy = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.randint(18, 78)
        a = rnd.randint(10, 26)
        c = accent if rnd.random() > 0.45 else (140, 180, 255)
        bkd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c + (a,))
    img = Image.alpha_composite(img, bok.filter(ImageFilter.GaussianBlur(16)))

    # vignette
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-W * 0.30, -H * 0.22, W * 1.30, H * 1.22], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img = Image.composite(img, Image.alpha_composite(img, dark), vig)

    # film grain
    arr = np.array(img.convert("RGB")).astype(np.int16)
    n = np.random.default_rng(seed).normal(0, 3.2, (H, W, 1)).repeat(3, axis=2)
    arr = np.clip(arr + n, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")


# ---------------- festival motifs (drawn in code, no external photos) ----------------
FESTIVALS = {
    "gurpurb":   dict(glow=(255, 176, 58), ink=(255, 206, 140)),
    "diwali":    dict(glow=(255, 150, 40), ink=(255, 208, 130)),
    "eid":       dict(glow=(120, 220, 200), ink=(210, 245, 235)),
    "christmas": dict(glow=(255, 120, 110), ink=(255, 225, 220)),
    "holi":      dict(glow=(255, 140, 200), ink=(255, 220, 240)),
    "ganesh":    dict(glow=(255, 160, 60), ink=(255, 220, 160)),
    "newyear":   dict(glow=(255, 200, 80), ink=(255, 235, 180)),
    "default":   dict(glow=(255, 176, 58), ink=(255, 220, 170)),
}


def _rays(img, col, cx, cy, n=14, r=900, alpha=26):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(n):
        a0 = (360 / n) * i + 6
        a1 = a0 + 360 / n * 0.42
        p = [(cx, cy)]
        for a in (a0, a1):
            p.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
        d.polygon(p, fill=col + (alpha,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(26)))


def _gurudwara(img, ink, cx=800, cy=690, k=1.15):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bw, bh = 210 * k, 150 * k
    d.rectangle([cx - bw, cy, cx + bw, cy + bh], fill=ink + (70,))
    d.ellipse([cx - bw * 0.72, cy - 96 * k, cx + bw * 0.72, cy + 26 * k], fill=ink + (78,))
    d.ellipse([cx - 42 * k, cy - 150 * k, cx + 42 * k, cy - 70 * k], fill=ink + (84,))
    d.line([(cx, cy - 150 * k), (cx, cy - 190 * k)], fill=ink + (60,), width=max(2, int(5 * k)))
    d.ellipse([cx - 8 * k, cy - 204 * k, cx + 8 * k, cy - 188 * k], fill=ink + (60,))
    for sx in (-1.25, 1.25):
        d.ellipse([cx + sx * bw - 52 * k, cy - 10 * k, cx + sx * bw + 52 * k, cy + 60 * k], fill=ink + (64,))
    d.arc([cx - 40 * k, cy + 40 * k, cx + 40 * k, cy + 150 * k], 180, 360, fill=ink + (55,), width=max(2, int(4 * k)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))


def _diya_row(img, ink, cx=800, cy=720, k=1.5):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, (dx, dy, sk) in enumerate([(0, 0, 1.25), (-150, 78, 0.8), (140, 70, 0.7)]):
        x, y, kk = cx + dx, cy + dy, k * sk
        d.arc([x - 62 * kk, y - 26 * kk, x + 62 * kk, y + 46 * kk], 0, 180, fill=ink + (80,),
              width=max(3, int(7 * kk)))
        d.polygon([(x, y - 74 * kk), (x + 15 * kk, y - 34 * kk), (x - 15 * kk, y - 34 * kk)],
                  fill=(255, 205, 105, 205))
        d.ellipse([x - 40 * kk, y - 104 * kk, x + 40 * kk, y - 20 * kk], fill=(255, 170, 60, 44))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(2)))


def _crescent(img, ink, cx=810, cy=680, r=175):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ink + (90,))
    cut = Image.new("L", (W, H), 0)
    ImageDraw.Draw(cut).ellipse([cx - r + 48, cy - r - 14, cx + r + 48, cy + r - 14], fill=255)
    a = lay.split()[3]
    a = ImageChops.subtract(a, cut.filter(ImageFilter.GaussianBlur(2)))
    lay.putalpha(a)
    for sx, sy, sr in ((cx - 150, cy - 96, 6), (cx + 118, cy + 96, 5), (cx + 150, cy - 120, 7)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=ink + (120,))
    img.alpha_composite(lay)


def _lantern(img, ink, cx=900, cy=560, k=1.5):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for dx, dy, sc in ((0, 0, 0.8), (140, 120, 0.55)):
        x, y = cx + dx, cy + dy
        d.line([(x, 0), (x, y - 70 * sc)], fill=ink + (40,), width=2)
        d.rounded_rectangle([x - 46 * sc, y - 66 * sc, x + 46 * sc, y + 66 * sc], int(16 * sc),
                            fill=ink + (30,), outline=ink + (60,), width=2)
        d.line([(x, y + 66 * sc), (x, y + 104 * sc)], fill=ink + (50,), width=2)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))


def _tree(img, ink, cx=810, cy=610, k=1.15):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, (w, h) in enumerate(((150, 150), (118, 132), (86, 112))):
        top = cy + i * 108 * k
        d.polygon([(cx, top - h * k), (cx - w * k, top), (cx + w * k, top)], fill=ink + (68,))
    d.rectangle([cx - 16 * k, cy + 240 * k, cx + 16 * k, cy + 330 * k], fill=ink + (70,))
    for sx, sy, sr in ((cx - 210, cy - 130, 9), (cx - 130, cy - 40, 6), (cx + 150, cy - 150, 7)):
        d.polygon([(sx, sy - sr * 2), (sx + sr * 0.7, sy - sr * 0.5), (sx + sr * 2, sy - sr * 0.2),
                   (sx + sr * 0.8, sy + sr * 0.7), (sx + sr * 1.2, sy + sr * 2), (sx, sy + sr * 1.2),
                   (sx - sr * 1.2, sy + sr * 2), (sx - sr * 0.8, sy + sr * 0.7), (sx - sr * 2, sy - sr * 0.2),
                   (sx - sr * 0.7, sy - sr * 0.5)], fill=ink + (95,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1)))


def _holi(img, ink, cx=0, cy=0, k=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cols = [(255, 120, 180), (255, 200, 80), (120, 220, 200), (170, 140, 255)]
    rnd = random.Random(7)
    for i in range(9):
        x, y = rnd.randint(60, W - 60), rnd.randint(120, 520)
        r = rnd.randint(60, 140)
        d.ellipse([x - r, y - r, x + r, y + r], fill=cols[i % 4] + (30,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))


def _fireworks(img, ink, cx=800, cy=700, k=1.6):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for ox, oy, r in ((0, 0, 150), (-180, 150, 90), (120, 210, 70)):
        x, y = cx + ox, cy + oy
        for i in range(12):
            a = math.radians(30 * i)
            d.line([(x, y), (x + r * math.cos(a), y + r * math.sin(a))], fill=ink + (60,), width=3)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(2)))


FESTIVAL_DRAW = {"gurpurb": _gurudwara, "diwali": _diya_row, "eid": _crescent,
                 "christmas": _tree, "holi": _holi, "ganesh": _diya_row,
                 "newyear": _fireworks}


def festival_layer(img, spec):
    """festival posts get their own imagery: warm rays + the festival's own motif.
    A photo plate at assets_v2/plates/<festival>.png wins over the drawn motif."""
    key = (spec.get("festival") or "default").lower()
    cfg = FESTIVALS.get(key, FESTIVALS["default"])
    plate = os.path.join(ASSETS, "plates", f"{key}.png")
    if os.path.exists(plate):
        p = Image.open(plate).convert("RGBA").resize((W, H), Image.LANCZOS)
        img.alpha_composite(p)
        return img
    _rays(img, cfg["glow"], 800, 620, n=16, r=1100, alpha=26)
    fn = FESTIVAL_DRAW.get(key)
    if fn:
        fn(img, cfg["ink"])
    if key == "eid":
        _lantern(img, cfg["ink"])
    return img


# ---------------- helpers ----------------
def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getbbox(t)[2] <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def glass(img, box, r=26, fill_a=20, border_a=46, shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([x0 + 4, y0 + 10, x1 + 4, y1 + 14], r, fill=(0, 0, 0, 120))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle(box, r, fill=(255, 255, 255, fill_a))
    ld.rounded_rectangle(box, r, outline=(255, 255, 255, border_a), width=2)
    ld.line([(x0 + r, y0 + 2), (x1 - r, y0 + 2)], fill=(255, 255, 255, 60), width=2)
    img.alpha_composite(lay)
    return img

def chip(img, box, text, font, pal, r=16):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle(box, r, fill=pal["accent"] + (255,))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    d.text(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), text, font=font,
           fill=pal["on"], anchor="mm")

def icon_badge(img, cx, cy, kind, pal):
    r = 39
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=pal["accent"] + (26,),
               outline=pal["accent"] + (110,), width=2)
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    acc, wht = pal["accent"] + (255,), (255, 255, 255, 235)
    if kind == "chart":
        d.rounded_rectangle([cx - 22, cy - 17, cx + 22, cy + 11], 5, outline=wht, width=3)
        d.line([(cx, cy + 11), (cx, cy + 20)], fill=wht, width=3)
        d.line([(cx - 11, cy + 20), (cx + 11, cy + 20)], fill=wht, width=3)
        for dx, top, bot, col in [(-11, -4, 6, acc), (-2, -10, 2, wht), (8, -6, 8, acc)]:
            d.line([(cx + dx, cy + top), (cx + dx, cy + bot)], fill=col, width=3)
    elif kind in ("cal-x", "cal-tick"):
        d.rounded_rectangle([cx - 20, cy - 15, cx + 20, cy + 20], 6, outline=wht, width=3)
        d.line([(cx - 20, cy - 3), (cx + 20, cy - 3)], fill=wht, width=3)
        d.line([(cx - 10, cy - 22), (cx - 10, cy - 13)], fill=wht, width=3)
        d.line([(cx + 10, cy - 22), (cx + 10, cy - 13)], fill=wht, width=3)
        if kind == "cal-x":
            d.line([(cx - 8, cy + 3), (cx + 8, cy + 17)], fill=acc, width=4)
            d.line([(cx + 8, cy + 3), (cx - 8, cy + 17)], fill=acc, width=4)
        else:
            tick = (70, 230, 140, 255) if pal["on"] != (28, 8, 8) else acc
            d.line([(cx - 8, cy + 9), (cx - 2, cy + 15)], fill=tick, width=4)
            d.line([(cx - 2, cy + 15), (cx + 9, cy + 2)], fill=tick, width=4)
    elif kind == "chat":
        d.rounded_rectangle([cx - 20, cy - 15, cx + 20, cy + 11], 8, outline=wht, width=3)
        d.polygon([(cx - 8, cy + 11), (cx - 2, cy + 11), (cx - 10, cy + 20)], fill=wht)
        for dx in (-9, 0, 9):
            d.ellipse([cx + dx - 2, cy - 4, cx + dx + 2, cy + 1], fill=acc)
    elif kind == "phone":
        d.arc([cx - 18, cy - 18, cx + 18, cy + 18], 120, 300, fill=wht, width=4)
        d.arc([cx - 12, cy - 12, cx + 12, cy + 12], 120, 300, fill=acc, width=3)
    elif kind == "rupee":
        d.text((cx, cy - 1), "\u20b9", font=F("Bold", 40), fill=wht, anchor="mm")
    elif kind == "percent":
        d.text((cx, cy - 1), "%", font=F("Bold", 38), fill=wht, anchor="mm")
    elif kind == "shield":
        d.polygon([(cx, cy - 22), (cx + 18, cy - 14), (cx + 18, cy + 6), (cx, cy + 22),
                   (cx - 18, cy + 6), (cx - 18, cy - 14)], outline=wht, width=3)
        d.line([(cx - 7, cy + 1), (cx - 2, cy + 7)], fill=acc, width=4)
        d.line([(cx - 2, cy + 7), (cx + 8, cy - 7)], fill=acc, width=4)
    elif kind == "piggy":
        d.ellipse([cx - 20, cy - 12, cx + 18, cy + 14], outline=wht, width=3)
        d.ellipse([cx + 12, cy - 4, cx + 24, cy + 6], outline=wht, width=3)
        d.line([(cx - 10, cy + 14), (cx - 10, cy + 20)], fill=wht, width=3)
        d.line([(cx + 6, cy + 14), (cx + 6, cy + 20)], fill=wht, width=3)
        d.line([(cx - 12, cy - 12), (cx - 4, cy - 20)], fill=wht, width=3)
        d.ellipse([cx + 3, cy - 5, cx + 7, cy - 1], fill=acc)
    elif kind == "coins":
        for i, dy in enumerate((10, 0, -10)):
            d.ellipse([cx - 16, cy + dy - 7, cx + 16, cy + dy + 7],
                      outline=wht if i else acc, width=3)
    elif kind == "bank":
        d.polygon([(cx, cy - 22), (cx + 20, cy - 10), (cx - 20, cy - 10)], outline=wht, width=3)
        for dx in (-12, 0, 12):
            d.line([(cx + dx, cy - 6), (cx + dx, cy + 12)], fill=wht, width=3)
        d.line([(cx - 20, cy + 18), (cx + 20, cy + 18)], fill=acc, width=3)
    elif kind == "warn":
        d.polygon([(cx, cy - 20), (cx + 21, cy + 15), (cx - 21, cy + 15)], outline=wht, width=3)
        d.line([(cx, cy - 6), (cx, cy + 3)], fill=acc, width=4)
        d.ellipse([cx - 2, cy + 8, cx + 2, cy + 12], fill=acc)
    elif kind == "up":
        d.line([(cx - 16, cy + 8), (cx, cy - 12)], fill=wht, width=4)
        d.line([(cx, cy - 12), (cx + 16, cy + 8)], fill=wht, width=4)
        d.line([(cx, cy - 12), (cx, cy + 18)], fill=acc, width=4)
    elif kind == "down":
        d.line([(cx - 16, cy - 8), (cx, cy + 12)], fill=wht, width=4)
        d.line([(cx, cy + 12), (cx + 16, cy - 8)], fill=wht, width=4)
        d.line([(cx, cy + 12), (cx, cy - 18)], fill=acc, width=4)
    elif kind == "star":
        for i in range(8):
            a = math.radians(45 * i)
            d.line([(cx, cy), (cx + 20 * math.cos(a), cy + 20 * math.sin(a))], fill=acc, width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=wht)
    elif kind == "dot":
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=acc)
    elif kind == "bell":
        d.arc([cx - 14, cy - 16, cx + 14, cy + 12], 180, 360, fill=wht, width=4)
        d.line([(cx - 14, cy - 2), (cx - 14, cy + 6)], fill=wht, width=4)
        d.line([(cx + 14, cy - 2), (cx + 14, cy + 6)], fill=wht, width=4)
        d.line([(cx - 16, cy + 6), (cx + 16, cy + 6)], fill=wht, width=4)
        d.ellipse([cx - 3, cy + 9, cx + 3, cy + 15], fill=wht)

# ---------------- render ----------------
def fit_lines(words, maxw, style, size, minimum=44):
    """pick the split (and size) that keeps 2 balanced lines inside maxw"""
    best = None
    for k in range(1, len(words)):
        l1, l2 = " ".join(words[:k]), " ".join(words[k:])
        s = size
        while s >= minimum:
            f = F(style, s)
            if f.getbbox(l1)[2] <= maxw and f.getbbox(l2)[2] <= maxw:
                break
            s -= 2
        if s < minimum:
            continue
        score = max(F(style, s).getbbox(l1)[2], F(style, s).getbbox(l2)[2]) - s * 0.6
        if best is None or score < best[0]:
            best = (score, k, s)
    if best:
        _, k, s = best
        return " ".join(words[:k]), " ".join(words[k:]), s
    return " ".join(words), "", minimum


ICON_RULES = [
    ("up",       ("rally", "gains", "surge", "record high", "jumped", "rose", "up ", "bought")),
    ("down",     ("fall", "fell", "crash", "slide", "slipped", "down ", "sold")),
    ("rupee",    ("salary", "income", "emi", "cost", "premium", "budget", "sip amount")),
    ("percent",  ("interest", "return", "rate", "cagr", "yield", "tax rate", "inflation")),
    ("shield",   ("insurance", "cover", "term plan", "protection", "policy", "claim")),
    ("piggy",    ("saving", "emergency fund", "goal", "invest monthly", "sip")),
    ("coins",    ("gold", "silver", "commodity", "mcx", "bullion", "copper", "crude")),
    ("bank",     ("bank", "fd", "fixed deposit", "loan", "credit", "rbi", "nbfc")),
    ("warn",     ("risk", "warning", "penalty", "careful", "trap", "hidden charge", "delay")),
    ("cal-x",    ("holiday", "closed", "shut", "no pay", "pause", "not there")),
    ("cal-tick", ("reopen", "resume", "lands", "arrive", "next day", "wednesday", "settles")),
    ("chart",    ("settle", "cycle", "t+", "trade", "chart", "index", "nifty", "sensex",
                  "market", "nav", "fund", "price", "crore", "lakh", "%")),
]

def pick_icon(text, default="star"):
    """score every icon rule against the point's own words, highest score wins
    (tie-break follows ICON_RULES order: chart, then holiday, then next-day)"""
    t = text.lower()
    best, best_score = default, 0
    for name, keys in ICON_RULES:
        score = sum(1 for k in keys if k in t)
        if score > best_score:
            best, best_score = name, score
    return best


def render(spec, out, reveal=3, show_cta=True, show_header=True):
    pal = TONES[spec.get("tone", "neutral")]
    acc, deep, on = pal["accent"], pal["deep"], pal["on"]
    img = background(acc, seed=sum(map(ord, spec["headline"])) & 0xFFFF)
    if spec.get("tone") == "festival" or spec.get("festival"):
        img = festival_layer(img, spec)
    d = ImageDraw.Draw(img)
    M = 62          # side margin
    CW = W - 2 * M  # content width

    # ---- header
    if show_header:
      try:
          logo = Image.open(LOGO_PATH).convert("RGBA").resize((58, 51), Image.LANCZOS)
          img.alpha_composite(logo, (M, 60)); hx = M + 74
      except Exception:
          hx = M + 6
      wf = F("SemiBold", 32)
      d.text((hx, 74), "ASSET RAMA", font=wf, fill=(255, 255, 255, 245))
      tw = wf.getbbox("ASSET RAMA")[2]
      d.line([(hx + tw + 24, 64), (hx + tw + 24, 108)], fill=(255, 255, 255, 85), width=2)
      tf, tag = F("Bold", 26), spec["tag"]
      tpw = tf.getbbox(tag)[2] + 44
      tx0 = hx + tw + 46
      lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
      ImageDraw.Draw(lay).rounded_rectangle([tx0, 60, tx0 + tpw, 110], 25, fill=acc + (255,))
      img.alpha_composite(lay); d = ImageDraw.Draw(img)
      d.text((tx0 + tpw / 2, 85), tag, font=tf, fill=on, anchor="mm")
      ff = F("SemiBold", 24)
      fpw = ff.getbbox("+ FOLLOW")[2] + 38
      lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
      ImageDraw.Draw(lay).rounded_rectangle([W - M - fpw, 60, W - M, 110], 23,
                                            fill=(255, 255, 255, 12), outline=acc + (200,), width=2)
      img.alpha_composite(lay); d = ImageDraw.Draw(img)
      d.text((W - M - fpw / 2, 85), "+ FOLLOW", font=ff, fill=acc + (255,), anchor="mm")

    # ---- headline (auto-fit, two lines, accent words coloured)
    head, hi = spec["headline"], spec.get("highlight", "")
    words = head.split()
    hiwords = hi.split() if hi else []
    l1, l2, size = fit_lines(words, CW, "Bold", 68)
    if hiwords:
        k = next((i for i, w in enumerate(words) if w.strip(".,:;?!") == hiwords[0].strip(".,:;?!")), None)
        if k:
            c1, c2 = " ".join(words[:k]), " ".join(words[k:])
            for s in range(68, 47, -2):
                f = F("Bold", s)
                if f.getbbox(c1)[2] <= CW and f.getbbox(c2)[2] <= CW:
                    l1, l2, size = c1, c2, s
                    break
    hf = F("Bold", size)
    y = 178
    for line in (l1, l2):
        if not line:
            continue
        x = M
        for w in line.split():
            col = acc if w.strip(".,:;?!") in [h.strip(".,:;?!") for h in hiwords] else (255, 255, 255)
            d.text((x, y), w, font=hf, fill=col + (255,))
            x += hf.getbbox(w + " ")[2]
        if line == l2:  # marker swipe under the accent line
            uw = sum(hf.getbbox(w + " ")[2] for w in line.split()
                     if w.strip(".,:;?!") in [h.strip(".,:;?!") for h in hiwords])
            if uw:
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).rounded_rectangle([M, y + size + 8, M + uw - 8, y + size + 20], 6,
                                                      fill=acc + (230,))
                img.alpha_composite(lay); d = ImageDraw.Draw(img)
        y += int(size * 1.16)

    # ---- subheadline
    sf = F("Medium", 30)
    sy = y + 26
    for line in wrap(spec["subheadline"], sf, CW)[:2]:
        d.text((M, sy), line, font=sf, fill=(184, 192, 206, 255)); sy += 42

    # ---- three glass point cards
    cy = sy + 30
    ch, gap = 134, 12
    icons = spec.get("icons") or [pick_icon(p) for p in spec["points"][:3]]
    nf, pf = F("Bold", 25), F("Medium", 29)
    for i, pt in enumerate(spec["points"][:3]):
        if i >= reveal:
            cy += ch + gap
            continue
        box = (M, cy, W - M, cy + ch)
        img = glass(img, box); d = ImageDraw.Draw(img)
        chip(img, (M + 22, cy + 40, M + 22 + 56, cy + 40 + 56), "0%d" % (i + 1), nf, pal)
        d = ImageDraw.Draw(img)
        icon_badge(img, M + 146, cy + ch // 2, icons[i], pal)
        d = ImageDraw.Draw(img)
        d.line([(M + 198, cy + 26), (M + 198, cy + ch - 26)], fill=(255, 255, 255, 50), width=2)
        ty = cy + 40
        for line in wrap(pt, pf, CW - 240)[:2]:
            x = M + 226
            for word in line.split():
                fig = any(c.isdigit() for c in word) or "\u20b9" in word or "%" in word
                d.text((x, ty), word, font=pf, fill=(acc if fig else (255, 255, 255)) + (255,))
                x += pf.getbbox(word + " ")[2]
            ty += 39
        cy += ch + gap

    # fixed furniture: contacts + disclaimer sit at the same spot in every frame
    qy, by = cy + 14, cy + 14 + 92
    ky, kh = by + 112, 104
    img = glass(img, (M, ky, W / 2 - 12, ky + kh)); d = ImageDraw.Draw(img)
    icon_badge(img, M + 52, ky + kh / 2, "chat", pal); d = ImageDraw.Draw(img)
    d.text((M + 100, ky + 26), "Questions on any topic I cover?", font=F("Medium", 23), fill=(230, 234, 242, 255))
    d.text((M + 100, ky + 58), "Comment below or send a DM.", font=F("Medium", 23), fill=(230, 234, 242, 255))
    img = glass(img, (W / 2 + 12, ky, W - M, ky + kh)); d = ImageDraw.Draw(img)
    icon_badge(img, W / 2 + 64, ky + kh / 2, "phone", pal); d = ImageDraw.Draw(img)
    d.text((W / 2 + 112, ky + 22), "EDUCATIONAL QUERIES", font=F("Bold", 20), fill=acc + (255,))
    d.text((W / 2 + 112, ky + 46), "9049547427", font=F("Bold", 36), fill=(255, 255, 255, 255))
    df = F("Regular", 19)
    dy = ky + kh + 20
    for line in wrap(spec["disclaimer"], df, CW + 20)[:2]:
        d.text((W / 2, dy), line, font=df, fill=(148, 156, 170, 235), anchor="ma")
        dy += 24

    if show_cta:
        # ---- question brush
        qf = F("Bold", 38)
        qw = min(qf.getbbox(spec["question"])[2] + 80, CW)
        lay = Image.new("RGBA", (qw + 40, 110), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle([20, 16, 20 + qw, 94], 18, fill=acc + (255,))
        lay = lay.rotate(-1.4, resample=Image.BICUBIC, expand=False)
        img.alpha_composite(lay, (int((W - qw) / 2) - 20, qy - 16)); d = ImageDraw.Draw(img)
        d.text((W / 2, qy + 39), spec["question"], font=qf, fill=on, anchor="mm")

        # ---- CTA pill
        box = [M + 34, by, W - M - 34, by + 92]
        grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(grad)
        for yy in range(box[1], box[3]):
            t = (yy - box[1]) / (box[3] - box[1])
            gd.line([(box[0], yy), (box[2], yy)], fill=lerp(acc, deep, t * 0.85) + (255,))
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rounded_rectangle(box, 46, fill=255)
        img.paste(grad, (0, 0), mask)
        d = ImageDraw.Draw(img)
        cf = F("Bold", 35)
        d.text((W / 2 - 24, by + 46), spec["cta"], font=cf, fill=on, anchor="mm")
        icon_badge(img, box[2] - 56, by + 46, "bell", dict(accent=on, deep=on, on=on))

    img.convert("RGB").save(out, quality=95)
    print("saved", out, "| reveal", reveal, "| cta", show_cta)



# ---------------- hook / beat / send cards ----------------
DISC = ("Views are personal and do not represent my employer. "
        "Educational only - not investment advice. Investments carry risk.")


def header_static(img, d, pal, tag):
    acc, on = pal["accent"], pal["on"]
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA").resize((58, 51), Image.LANCZOS)
        img.alpha_composite(logo, (62, 60)); hx = 136
    except Exception:
        hx = 68
    wf = F("SemiBold", 32)
    d.text((hx, 74), "ASSET RAMA", font=wf, fill=(255, 255, 255, 245))
    tw = wf.getbbox("ASSET RAMA")[2]
    d.line([(hx + tw + 24, 64), (hx + tw + 24, 108)], fill=(255, 255, 255, 85), width=2)
    tf = F("Bold", 26)
    tpw = tf.getbbox(tag)[2] + 44
    tx0 = hx + tw + 46
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([tx0, 60, tx0 + tpw, 110], 25, fill=acc + (255,))
    img.alpha_composite(lay); d = ImageDraw.Draw(img)
    d.text((tx0 + tpw / 2, 85), tag, font=tf, fill=on, anchor="mm")
    ff = F("SemiBold", 24)
    fpw = ff.getbbox("+ FOLLOW")[2] + 38
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([W - 62 - fpw, 60, W - 62, 110], 23,
                                          fill=(255, 255, 255, 12), outline=acc + (200,), width=2)
    img.alpha_composite(lay); d = ImageDraw.Draw(img)
    d.text((W - 62 - fpw / 2, 85), "+ FOLLOW", font=ff, fill=acc + (255,), anchor="mm")
    return img, d


def footer(img, d):
    df = F("Regular", 19)
    dy = H - 62
    for line in wrap(DISC, df, W - 120)[:2]:
        d.text((W / 2, dy), line, font=df, fill=(148, 156, 170, 235), anchor="ma")
        dy += 24


def hook_card(spec, out, show_header=True):
    pal = TONES[spec.get("tone", "neutral")]; acc = pal["accent"]
    img = background(acc, seed=sum(map(ord, spec["hook"]["line"])) & 0xFFFF); d = ImageDraw.Draw(img)
    if show_header:
        img, d = header_static(img, d, pal, spec["tag"])
    words = spec["hook"]["line"].split()
    acc_set = set(spec["hook"].get("accent", "").split())
    hf = F("Bold", 118)
    lines, cur = [], []
    for w in words:
        if hf.getbbox(" ".join(cur + [w]))[2] <= W - 132 or not cur:
            cur.append(w)
        else:
            lines.append(cur); cur = [w]
    lines.append(cur)
    y = 470
    for line in lines[:3]:
        x = 66
        for w in line:
            col = acc if w in acc_set else (255, 255, 255)
            d.text((x, y), w, font=hf, fill=col + (255,))
            x += hf.getbbox(w + " ")[2]
        y += 128
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([66, y + 4, 66 + 300, y + 18], 7, fill=acc + (235,))
    img.alpha_composite(lay); d = ImageDraw.Draw(img)
    if spec["hook"].get("sub"):
        d.text((66, y + 44), spec["hook"]["sub"], font=F("Medium", 40), fill=(184, 192, 206, 255))
    footer(img, d)
    img.convert("RGB").save(out, quality=95)


def beat_card(spec, out, show_header=True):
    pal = TONES[spec.get("tone", "neutral")]; acc = pal["accent"]
    b = spec["beat"]
    img = background(acc, seed=sum(map(ord, str(b.get("value")))) & 0xFFFF); d = ImageDraw.Draw(img)
    if show_header:
        img, d = header_static(img, d, pal, spec["tag"])
    d.text((W / 2, 430), " ".join(b.get("kicker", "THE NUMBER").upper()),
           font=F("SemiBold", 30), fill=(176, 184, 198, 255), anchor="mm")
    val = str(b.get("value", ""))
    digits = "".join(ch for ch in val if ch.isdigit() or ch in ".,")
    prefix = val.replace(digits, "").strip()
    f_small, f_big = F("Bold", 96), F("Bold", 240)
    tw_s = f_small.getbbox(prefix + " ")[2] if prefix else 0
    tw_b = f_big.getbbox(digits or val)[2]
    total = tw_s + tw_b
    x0 = (W - total) / 2
    if prefix:
        d.text((x0, 560), prefix, font=f_small, fill=(255, 255, 255, 255))
    d.text((x0 + tw_s, 470), digits or val, font=f_big, fill=acc + (255,))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([x0, 790, x0 + total, 802], 6, fill=acc + (235,))
    img.alpha_composite(lay); d = ImageDraw.Draw(img)
    lf = F("Medium", 36)
    yy = 840
    for line in wrap(b.get("label", ""), lf, W - 220)[:2]:
        d.text((W / 2, yy), line, font=lf, fill=(196, 204, 216, 255), anchor="ma"); yy += 50
    footer(img, d)
    img.convert("RGB").save(out, quality=95)


def send_card(spec, out, show_header=True):
    pal = TONES[spec.get("tone", "neutral")]; acc, on = pal["accent"], pal["on"]
    s = spec.get("send") or {}
    img = background(acc, seed=sum(map(ord, s.get("to", "send"))) & 0xFFFF); d = ImageDraw.Draw(img)
    if show_header:
        img, d = header_static(img, d, pal, spec["tag"])
    d.text((W / 2, 430), " ".join(s.get("kicker", "ONE SMALL THING").upper()),
           font=F("SemiBold", 30), fill=(176, 184, 198, 255), anchor="mm")
    d.text((W / 2, 540), s.get("hero", "SEND THIS"), font=F("Bold", 126),
           fill=(255, 255, 255, 255), anchor="mm")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([W / 2 - 170, 620, W / 2 + 170, 632], 6, fill=acc + (235,))
    img.alpha_composite(lay); d = ImageDraw.Draw(img)
    tf = F("Medium", 40)
    yy = 680
    for line in wrap(s.get("to", ""), tf, W - 260)[:2]:
        d.text((W / 2, yy), line, font=tf, fill=(196, 204, 216, 255), anchor="ma"); yy += 54
    cf = F("Bold", 32)
    a, b2 = s.get("chip_a", "SEND"), s.get("chip_b", "SAVE FOR LATER")
    w1, w2 = cf.getbbox(a)[2] + 96, cf.getbbox(b2)[2] + 84
    gap = 24
    x = (W - (w1 + w2 + gap)) / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([x, 800, x + w1, 892], 46, fill=acc + (255,))
    ld.rounded_rectangle([x + w1 + gap, 800, x + w1 + gap + w2, 892], 46,
                         fill=(255, 255, 255, 10), outline=acc + (210,), width=2)
    img.alpha_composite(lay); d = ImageDraw.Draw(img)
    d.text((x + w1 / 2, 846), a, font=cf, fill=on, anchor="mm")
    d.text((x + w1 + gap + w2 / 2, 846), b2, font=cf, fill=acc + (255,), anchor="mm")
    footer(img, d)
    img.convert("RGB").save(out, quality=95)


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    spec.setdefault("disclaimer", DISC)
    render(spec, sys.argv[2])
    if "--cards" in sys.argv:
        base = os.path.dirname(os.path.abspath(sys.argv[2])) or "."
        if spec.get("hook"):
            hook_card(spec, os.path.join(base, "hook.png"))
        if spec.get("beat"):
            beat_card(spec, os.path.join(base, "beat.png"))
        if spec.get("send"):
            send_card(spec, os.path.join(base, "send.png"))
        print("cards written")
