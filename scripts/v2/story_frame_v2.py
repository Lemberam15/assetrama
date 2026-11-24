#!/usr/bin/env python3
"""Build a 1080x1920 story frame from a v2 spec (fixed 24/11/2026).

The old ig_story_slide.py was written for v9 cards that carry no header, so on a
v2 card it stamped a SECOND logo + FOLLOW chip (and a blue chip on a red post).
This builds the story the same way the reel is built: the 4:5 card on its own
blurred plate, ONE animated-style header inside the card, and the website line
in the bottom bar. No duplicate header.

    python story_frame_v2.py spec.json story_frame.png
then: python ig_story_encode.py story_frame.png story.mp4 20 <mood>
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_slide_v2 as R, reel_916_v2 as RW, build_film_v2 as B
from PIL import Image, ImageDraw

SITE = "lemberam15.github.io/assetrama"

def build(spec_path, out_path):
    spec = json.load(open(spec_path))
    spec.setdefault("disclaimer", R.DISC)
    pal = R.TONES[spec.get("tone", "neutral")]
    tmp = os.path.join(os.path.dirname(os.path.abspath(out_path)) or ".", "_story_base.png")
    R.render(spec, tmp, show_header=False)
    RW.wrap(tmp, tmp)
    frame = Image.open(tmp).convert("RGBA")
    shaded = B._shade(Image.open(R.LOGO_PATH).convert("RGBA"))
    frame.alpha_composite(B.header_tile(0.0, pal, spec["tag"], shaded), (B.OX, B.OY + (1920 - R.H) // 2))
    d = ImageDraw.Draw(frame)
    f = R.F("Medium", 44)
    w = d.textlength(SITE, font=f)
    d.text(((1080 - w) / 2, 1770), SITE, font=f, fill=(238, 240, 245, 255))
    frame.convert("RGB").save(out_path, quality=95)
    print("saved", out_path, frame.size)

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
