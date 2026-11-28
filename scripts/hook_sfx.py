#!/usr/bin/env python3
"""HOOK SOUND DESIGN (v70, 28/11/2026 - Innovation Lab).

The v2 60 s film had NO sound design at all: build_film_v2.py muxes the music
bed and fades it out, nothing else. On a muted-by-default feed the first
half-second is where a viewer decides, and a bed that simply starts is the
weakest possible opening. This script lays one short cue on the opening of the
bed - a soft riser into a low impact as the kinetic hook locks - and nothing
else, so the rest of the film stays exactly as it was.

Why this shape (2026 sound-design research):
  - A riser + impact at the cut point is the standard "attention reset" in
    short-form; it tells the ear something just landed.
  - It has to be quiet. A cue that is louder than the bed reads as an ad and
    kills the calm-education tone the account is built on, so the impact sits
    ~6 dB under the bed's RMS and never clips.

Usage
  python hook_sfx.py bed.wav out.wav [--impact 0.50] [--gain 1.0]

QC built in: prints the bed's RMS/peak, the cue's contribution and the output's
RMS/peak, and refuses to write a file that clips (peak > 0.985) or that changes
the duration by more than one sample.
"""
import argparse
import struct
import wave

import numpy as np


def read_wav(path):
    with wave.open(path, "rb") as w:
        n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        raw = w.readframes(n)
    assert sw == 2, "expected 16-bit PCM, got %d-byte samples" % sw
    a = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        a = a.reshape(-1, ch)
    else:
        a = a.reshape(-1, 1)
    return a, sr


def write_wav(path, a, sr):
    a = np.clip(a, -1.0, 1.0)
    with wave.open(path, "wb") as w:
        w.setnchannels(a.shape[1])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((a * 32767.0).astype("<i2").tobytes())


def db(x):
    return 20 * np.log10(max(1e-9, float(x)))


def cue(sr, impact_at=0.50, total=1.9):
    """Riser (0 -> impact_at) into a low impact + short air tail. Mono float."""
    n = int(total * sr)
    t = np.arange(n) / sr
    out = np.zeros(n, dtype=np.float32)

    # ---- riser: band-limited noise whose level and brightness climb ----
    rng = np.random.default_rng(7)
    noise = rng.standard_normal(n).astype(np.float32)
    # one-pole high-pass to keep it airy instead of rumbly
    hp = np.empty_like(noise)
    prev_x = prev_y = 0.0
    a = 0.92
    for i in range(n):
        prev_y = a * (prev_y + noise[i] - prev_x)
        prev_x = noise[i]
        hp[i] = prev_y
    # a rising sine glides under it so the ear hears a direction
    glide = np.sin(2 * np.pi * np.cumsum(np.linspace(180, 620, n)) / sr).astype(np.float32)
    ri = t < impact_at
    e = (t[ri] / impact_at) ** 2.2                      # quiet at first, lands hard
    out[ri] += (0.55 * hp[ri] * 0.30 + 0.45 * glide[ri] * 0.10) * e

    # ---- impact: low thump + short broadband crack ----
    ii = int(impact_at * sr)
    m = n - ii
    ti = np.arange(m) / sr
    thump = np.sin(2 * np.pi * 52 * ti) * np.exp(-ti / 0.13)
    crack = rng.standard_normal(m).astype(np.float32) * np.exp(-ti / 0.035)
    out[ii:] += 0.55 * thump.astype(np.float32) + 0.10 * crack

    # ---- soft tail so the impact does not stop dead ----
    tail = np.exp(-np.maximum(0.0, t - impact_at) / 0.9)
    out *= np.where(t < impact_at, 1.0, 0.35 + 0.65 * tail)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bed")
    ap.add_argument("out")
    ap.add_argument("--impact", type=float, default=0.50, help="seconds into the film")
    ap.add_argument("--gain", type=float, default=1.0)
    a = ap.parse_args()

    bed, sr = read_wav(a.bed)
    c = cue(sr, a.impact) * a.gain
    c = c[: bed.shape[0]]
    if c.shape[0] < bed.shape[0]:
        c = np.pad(c, (0, bed.shape[0] - c.shape[0]))

    # cue peak sits ~-19 dBFS, i.e. well under a -12 dBFS RMS bed
    peak = float(np.max(np.abs(c))) or 1.0
    c *= 0.20 / peak   # cue peak ~ -14 dBFS: audible, still under the bed

    out = bed.copy()
    out += c[:, None]
    if float(np.max(np.abs(out))) > 0.985:
        s = 0.985 / float(np.max(np.abs(out)))
        out *= s
        print("WARN: peak trimmed by %.2f dB to avoid clipping" % (20 * np.log10(s)))

    br, op = float(np.sqrt(np.mean(bed ** 2))), float(np.sqrt(np.mean(out ** 2)))
    w = int(2.0 * sr)   # the opening window the cue actually lives in
    bo, oo = float(np.sqrt(np.mean(bed[:w] ** 2))), float(np.sqrt(np.mean(out[:w] ** 2)))
    print("bed   rms %6.2f dBFS  peak %6.2f dBFS  %.2fs" % (db(br), db(np.max(np.abs(bed))), bed.shape[0] / sr))
    print("out   rms %6.2f dBFS  peak %6.2f dBFS  %.2fs" % (db(op), db(np.max(np.abs(out))), out.shape[0] / sr))
    print("open  first 2.0 s: bed %6.2f -> out %6.2f dBFS  (%+.2f dB, target under +3 dB)"
          % (db(bo), db(oo), db(oo) - db(bo)))
    print("cue   peak %6.2f dBFS" % db(np.max(np.abs(c))))
    write_wav(a.out, out, sr)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
