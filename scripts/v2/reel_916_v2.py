#!/usr/bin/env python3
"""Wrap a v2 4:5 card into a native 9:16 reel frame (1080x1920).
The card keeps its own header, so the frame adds NO second header and no
second FOLLOW chip - just the card's own plate, blurred, above and below."""
import sys
from PIL import Image, ImageFilter, ImageEnhance

W, H = 1080, 1920

def wrap(src_path, out_path):
    src = Image.open(src_path).convert("RGB")
    bg = src.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(48))
    bg = ImageEnhance.Brightness(bg).enhance(0.42)
    y = (H - src.height) // 2
    bg.paste(src, (0, y))
    bg.save(out_path, quality=95)
    print("saved", out_path, bg.size)

if __name__ == "__main__":
    wrap(sys.argv[1], sys.argv[2])
