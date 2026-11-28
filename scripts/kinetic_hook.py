#!/usr/bin/env python3
"""KINETIC HOOK (v70, 28/11/2026 - Innovation Lab).

Turns the 2.5 s cold-open hook from a STILL into a KINETIC opening, without
touching the rest of the film.

Why (research, 2026):
  - "A static title card that sits on screen for 2 seconds before the animation
    begins loses the viewer before the content starts. The strongest kinetic
    typography videos open with text already in motion, paired with a bold
    colour shift or scale change." (faceless-format studies, 2026)
  - Instagram/Reels is watched muted in Explore: the text IS the content, so
    the opening has to carry motion on its own.
  - Restraint wins: text that moves too aggressively gets HARDER to read. So
    the whole line settles in ~0.5 s, the accent word takes one colour sweep,
    the underline draws once, the sub-line rises once, then everything holds
    still and readable for the rest of the hook.

Frame 0 is STILL the complete hook line at full brightness (only 7.5 % larger
and slightly soft), because frame 0 is the thumbnail on LinkedIn - a frame with
one word on it would be a worse cover than a still. The motion is a settle, not
a build-from-nothing.

Usage
  python kinetic_hook.py spec.json outdir            # writes hook_000.png ...
  python kinetic_hook.py spec.json outdir --fps 12 --dur 2.5

Writes outdir/hook_###.png (1080x1350, header NOT drawn - build_film_v2.py
composites the live header on every frame) and outdir/manifest.json.

The layout is IDENTICAL to render_slide_v2.hook_card(), so the settle ends on
exactly the still the film used before - the cover JPEG and the held frame
match to the pixel.

Wire-up (build_film_v2.py, 28/11/2026):
  python build_film_v2.py spec.json post.mp4 --music bed.wav \
      --hook 2.5 --hold 50 --beat 4 --send 3.5 --kinetic outdir
No --kinetic -> byte-for-byte the old film (backwards compatible).
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

# render_slide_v2.py lives in scripts/v2/ of the assetrama repo; the skill keeps
# a copy next to this file too. Accept either.
_here = os.path.dirname(os.path.abspath(__file__))
for _cand in (os.path.join(_here, "v2"), _here, os.path.join(_here, "..", "v2")):
    if os.path.exists(os.path.join(_cand, "render_slide_v2.py")):
        sys.path.insert(0, _cand)
        break
import render_slide_v2 as R  # noqa: E402

W, H = R.W, R.H

# ---- timing (seconds) ----
SETTLE = 0.50      # whole line scales 1.075 -> 1.000 and comes into focus
SWEEP_0, SWEEP_1 = 0.26, 0.80   # accent colour sweep crosses the line
RULE_0, RULE_1 = 0.55, 0.95     # underline draws left -> right
SUB_0, SUB_1 = 0.85, 1.20       # sub-line rises + fades in
SETTLE_SCALE = 0.075            # 7.5 % - visible, still fully readable at f0
BLUR_MAX = 3.2                  # px at frame 0, 0 by SETTLE


def _ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def _layout(spec):
    """Same word layout as render_slide_v2.hook_card()."""
    hook = spec["hook"]
    hf = R.F("Bold", 118)
    words = hook["line"].split()
    acc_set = set(hook.get("accent", "").split())
    lines, cur = [], []
    for w in words:
        if hf.getbbox(" ".join(cur + [w]))[2] <= W - 132 or not cur:
            cur.append(w)
        else:
            lines.append(cur)
            cur = [w]
    lines.append(cur)
    y = 470
    out = []
    for line in lines[:3]:
        x = 66
        for w in line:
            out.append((w, x, y, w in acc_set))
            x += hf.getbbox(w + " ")[2]
        y += 128
    return out, y, hf


def _text_layer(spec, sweep_x=None, dim_acc=False):
    """Transparent 1080x1350 layer holding the hook words only."""
    pal = R.TONES[spec.get("tone", "neutral")]
    acc = pal["accent"]
    if dim_acc:  # accent word starts lit-down and comes to full on the sweep
        acc = tuple(int(c * 0.62) for c in acc)
    placed, y_end, hf = _layout(spec)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for w, x, y, is_acc in placed:
        col = (255, 255, 255)
        if is_acc and sweep_x is not None and sweep_x >= x + hf.getbbox(w)[2] / 2:
            col = acc
        d.text((x, y), w, font=hf, fill=col + (255,))
    return lay, y_end, hf


def render_frames(spec, outdir, fps=12, dur=2.5):
    os.makedirs(outdir, exist_ok=True)
    pal = R.TONES[spec.get("tone", "neutral")]
    acc = pal["accent"]
    bg = R.background(acc, seed=sum(map(ord, spec["hook"]["line"])) & 0xFFFF)
    placed, y_end, hf = _layout(spec)

    # the sharp text layer (used at scale 1.0 and as the source for the settle)
    sharp, _, _ = _text_layer(spec, sweep_x=10 ** 6)
    sharp_dim, _, _ = _text_layer(spec, sweep_x=10 ** 6, dim_acc=True)
    sub_font = R.F("Medium", 40)

    n = max(2, int(round(dur * fps)))
    names = []
    for i in range(n):
        t = i / fps
        img = bg.copy().convert("RGBA")

        # ---- 1. the settle: scale down into place + focus ----
        if t < SETTLE:
            k = _ease(t / SETTLE)
            s = 1.0 + SETTLE_SCALE * (1.0 - k)
            layer = sharp_dim
            if s > 1.001:
                lw, lh = int(W * s), int(H * s)
                layer = layer.resize((lw, lh), Image.LANCZOS)
                # keep the text block's optical centre fixed while it scales
                cx, cy = W / 2, (470 + y_end) / 2
                ox, oy = int(cx - cx * s), int(cy - cy * s)
                canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                canvas.alpha_composite(layer, (ox, oy))
                layer = canvas
            br = BLUR_MAX * (1.0 - k)
            if br > 0.15:
                layer = layer.filter(ImageFilter.GaussianBlur(br))
            img.alpha_composite(layer)
        else:
            # ---- 2. accent sweep (colour shift), then everything sharp ----
            sweep = None
            if t < SWEEP_1:
                p = max(0.0, min(1.0, (t - SWEEP_0) / (SWEEP_1 - SWEEP_0)))
                sweep = 40 + p * 1040
            if sweep is not None and sweep > 40:
                # soft light band travelling with the sweep
                band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(band).rectangle([sweep - 60, 430, sweep + 60, y_end + 30],
                                               fill=acc + (34,))
                img.alpha_composite(band.filter(ImageFilter.GaussianBlur(26)))
            layer, _, _ = _text_layer(spec, sweep if sweep is not None else 10 ** 6)
            img.alpha_composite(layer)

        d = ImageDraw.Draw(img)

        # ---- 3. underline draws ----
        rk = _ease((t - RULE_0) / (RULE_1 - RULE_0)) if t > RULE_0 else 0.0
        if rk > 0:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).rounded_rectangle([66, y_end + 4, 66 + int(300 * rk), y_end + 18],
                                                  7, fill=acc + (235,))
            img.alpha_composite(lay)
            d = ImageDraw.Draw(img)

        # ---- 4. sub-line rises ----
        if spec["hook"].get("sub") and t > SUB_0:
            k = _ease((t - SUB_0) / (SUB_1 - SUB_0))
            sub = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(sub).text((66, y_end + 44 + int(16 * (1 - k))), spec["hook"]["sub"],
                                     font=sub_font, fill=(184, 192, 206, int(255 * k)))
            img.alpha_composite(sub)
            d = ImageDraw.Draw(img)

        R.footer(img, d)
        name = "hook_%03d.png" % i
        img.convert("RGB").save(os.path.join(outdir, name), quality=95)
        names.append(name)

    json.dump({"fps": fps, "frames": names, "dur": n / fps},
              open(os.path.join(outdir, "manifest.json"), "w"), indent=1)
    print("kinetic hook: %d frames @ %d fps = %.2f s -> %s" % (n, fps, n / fps, outdir))
    return names


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fps, dur = 12, 2.5
    for a in sys.argv[1:]:
        if a.startswith("--fps"):
            fps = int(a.split("=")[1]) if "=" in a else fps
        if a.startswith("--dur"):
            dur = float(a.split("=")[1]) if "=" in a else dur
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    spec = json.load(open(args[0]))
    spec.setdefault("disclaimer", R.DISC)
    render_frames(spec, args[1], fps=fps, dur=dur)
