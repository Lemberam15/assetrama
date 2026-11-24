#!/usr/bin/env python3
"""Asset Rama film builder v2 (approved 24/11/2026).

Assembles the 4:5 film from the v2 cards with a live header (3D-style logo +
pulsing FOLLOW chip) and the licensed music bed.

    python build_film_v2.py spec.json post.mp4 --music bed.wav \
        [--hook 2.5] [--hold 34.5] [--beat 4.5] [--send 3.5] [--fps 12]

Every card is rendered by render_slide_v2.py (same folder). The slide is held
on screen for --hold seconds so all three points can be read properly, which
is Ram's rule of 24/11/2026.
"""
import argparse, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_slide_v2 as R

W, H, F = R.W, R.H, R.F
OX, OY, TW, TH = 30, 40, 1020, 110


def _shade(logo):
    w, h = logo.size
    light, dark = Image.new("L", (w, h)), Image.new("L", (w, h))
    ld, dd = ImageDraw.Draw(light), ImageDraw.Draw(dark)
    for y in range(h):
        ld.line([(0, y), (w, y)], fill=int(95 * max(0.0, 1 - y / (h * 0.75))))
        dd.line([(0, y), (w, y)], fill=int(70 * max(0.0, (y - h * 0.45) / (h * 0.55))))
    a = logo.split()[3]
    out = Image.composite(Image.new("RGBA", (w, h), (255, 255, 255, 255)), logo,
                          Image.composite(light, Image.new("L", (w, h), 0), a))
    out = Image.composite(Image.new("RGBA", (w, h), (0, 0, 0, 255)), out,
                          Image.composite(dark, Image.new("L", (w, h), 0), a))
    out.putalpha(a)
    return out


def _specular(logo, phase):
    w, h = logo.size
    band = Image.new("L", (w, h), 0)
    x = -w + (phase % 1.0) * (w * 2.4)
    ImageDraw.Draw(band).polygon([(x, h), (x + w * 0.28, 0), (x + w * 0.44, 0), (x + w * 0.16, h)], fill=150)
    band = Image.composite(band.filter(ImageFilter.GaussianBlur(3)),
                           Image.new("L", (w, h), 0), logo.split()[3])
    out = Image.composite(Image.new("RGBA", (w, h), (255, 255, 255, 255)), logo,
                          band.point(lambda v: int(v * 0.55)))
    out.putalpha(logo.split()[3])
    return out


def header_tile(t, pal, tag, shaded):
    acc, on = pal["accent"], pal["on"]
    tile = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    M = 62 - OX
    d = ImageDraw.Draw(tile)
    ang = 5.0 * math.sin(t * 1.5)
    sc = 1.0 + 0.04 * math.sin(t * 1.5 + 0.8)
    dy = 4.0 * math.sin(t * 1.9)
    sz = (max(30, int(58 * sc)), max(26, int(51 * sc)))
    lg = _specular(shaded.resize(sz, Image.LANCZOS), t / 4.0).rotate(ang, resample=Image.BICUBIC, expand=True)
    cx, cy = M + 29, (86 - OY) + int(dy)
    ga = int(40 + 30 * (0.5 + 0.5 * math.sin(t * 2.4)))
    glow = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([cx - 58, cy - 58, cx + 58, cy + 58], fill=acc + (ga,))
    tile.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))
    sh = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 160), (cx - lg.size[0] // 2 + 2, cy - lg.size[1] // 2 + 7), lg.split()[3])
    tile.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    tile.alpha_composite(lg, (cx - lg.size[0] // 2, cy - lg.size[1] // 2))
    d = ImageDraw.Draw(tile)
    hx = M + 74
    wf = F("SemiBold", 32)
    d.text((hx, 74 - OY), "ASSET RAMA", font=wf, fill=(255, 255, 255, 245))
    tw = wf.getbbox("ASSET RAMA")[2]
    d.line([(hx + tw + 24, 64 - OY), (hx + tw + 24, 108 - OY)], fill=(255, 255, 255, 85), width=2)
    tf = F("Bold", 26)
    tpw = tf.getbbox(tag)[2] + 44
    tx0 = hx + tw + 46
    d.rounded_rectangle([tx0, 60 - OY, tx0 + tpw, 110 - OY], 25, fill=acc + (255,))
    d.text((tx0 + tpw / 2, 85 - OY), tag, font=tf, fill=on, anchor="mm")
    ff = F("SemiBold", 24)
    fpw = ff.getbbox("+ FOLLOW")[2] + 38
    x0, y0, x1, y1 = W - 62 - fpw - OX, 60 - OY, W - 62 - OX, 110 - OY
    pulse = 0.5 + 0.5 * math.sin(t * 2.2)
    gl = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], 25,
                                         fill=acc + (int(18 + 34 * pulse),))
    tile.alpha_composite(gl.filter(ImageFilter.GaussianBlur(8)))
    body = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rounded_rectangle([x0, y0, x1, y1], 23, fill=(255, 255, 255, int(12 + 14 * pulse)),
                         outline=acc + (int(150 + 95 * pulse),), width=2)
    sw = Image.new("L", (TW, TH), 0)
    sx = x0 - 40 + ((t / 3.0) % 1.0) * (fpw + 80)
    ImageDraw.Draw(sw).polygon([(sx, y1), (sx + 26, y0), (sx + 46, y0), (sx + 20, y1)], fill=115)
    msk = Image.new("L", (TW, TH), 0)
    ImageDraw.Draw(msk).rounded_rectangle([x0, y0, x1, y1], 23, fill=255)
    sw = Image.composite(sw.filter(ImageFilter.GaussianBlur(3)), Image.new("L", (TW, TH), 0), msk)
    body = Image.composite(Image.new("RGBA", (TW, TH), (255, 255, 255, 255)), body, sw)
    tile.alpha_composite(body)
    d = ImageDraw.Draw(tile)
    d.text((x0 + fpw / 2, 85 - OY), "+ FOLLOW", font=ff, fill=acc + (int(215 + 40 * pulse),), anchor="mm")
    return tile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("out")
    ap.add_argument("--music", default="")
    ap.add_argument("--hook", type=float, default=2.5)
    ap.add_argument("--hold", type=float, default=34.5)
    ap.add_argument("--beat", type=float, default=4.5)
    ap.add_argument("--send", type=float, default=3.5)
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--size", default="4:5", choices=["4:5", "9:16"])
    ap.add_argument("--work", default=".")
    a = ap.parse_args()

    import json
    spec = json.load(open(a.spec))
    spec.setdefault("disclaimer", R.DISC)
    pal = R.TONES[spec.get("tone", "neutral")]
    w = a.work
    os.makedirs(w, exist_ok=True)

    R.render(spec, os.path.join(w, "base_slide.png"), show_header=False)
    R.hook_card(spec, os.path.join(w, "base_hook.png"), show_header=False)
    R.beat_card(spec, os.path.join(w, "base_beat.png"), show_header=False)
    R.send_card(spec, os.path.join(w, "base_send.png"), show_header=False)

    # 9:16: same cards, wrapped on their own blurred plate (no second header)
    if a.size == "9:16":
        import reel_916_v2 as RW
        for n in ("base_slide", "base_hook", "base_beat", "base_send"):
            RW.wrap(os.path.join(w, n + ".png"), os.path.join(w, n + "_916.png"))
        OUT_W, OUT_H, OFF_Y = 1080, 1920, 175
    else:
        OUT_W, OUT_H, OFF_Y = W, H, 0

    bases = [("base_hook.png", a.hook), ("base_slide.png", a.hold),
             ("base_beat.png", a.beat), ("base_send.png", a.send), ("base_send.png", 0.5)]
    if a.size == "9:16":
        bases = [(f.replace(".png", "_916.png"), d) for f, d in bases]
    total = sum(d for _, d in bases)
    frames = int(total * a.fps)
    imgs = [Image.open(os.path.join(w, f)).convert("RGBA") for f, _ in bases]
    bounds, acc = [], 0.0
    for _, d in bases:
        acc += d
        bounds.append(acc)

    shaded = _shade(Image.open(R.LOGO_PATH).convert("RGBA"))
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    tmp = os.path.join(w, "_vo.mp4")
    cmd = [exe, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OUT_W}x{OUT_H}", "-r", str(a.fps),
           "-i", "-", "-vf", f"fade=t=out:st={total - 1.5:.2f}:d=1.5,format=yuv420p",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "1",
           "-pix_fmt", "yuv420p", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for i in range(frames):
        t = i / a.fps
        idx = 0
        while idx < len(bounds) - 1 and t >= bounds[idx]:
            idx += 1
        frame = imgs[idx].copy()
        frame.alpha_composite(header_tile(t, pal, spec["tag"], shaded), (OX, OY + OFF_Y))
        p.stdin.write(frame.convert("RGB").tobytes())
    p.stdin.close(); p.wait()

    if a.music and os.path.exists(a.music):
        subprocess.run([exe, "-y", "-i", tmp, "-i", a.music, "-c:v", "copy", "-c:a", "aac",
                        "-b:a", "128k", "-af", f"afade=t=out:st={total - 3.5:.2f}:d=3",
                        "-shortest", a.out], capture_output=True)
    else:
        subprocess.run([exe, "-y", "-i", tmp, "-c", "copy", a.out], capture_output=True)
    print(f"built {a.out}  {total:.1f}s  {frames} frames  {OUT_W}x{OUT_H}  tone={spec.get('tone')}")


if __name__ == "__main__":
    main()
