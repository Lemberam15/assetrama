# Asset Rama renderer v2 (approved by Ram, 24/11/2026)

Two files do everything:

| File | What it does |
|---|---|
| `render_slide_v2.py` | 1080x1350 slide + hook / beat / send cards, glass template, tone colours, content-aware icons |
| `build_film_v2.py` | assembles the MP4 with the live header (3D-style logo + pulsing FOLLOW chip) and the music bed |

Both download their own Poppins fonts and the logo mark on first run, so a fresh
sandbox needs only `pip install pillow imageio-ffmpeg numpy`.

## Usage

```
python scripts/v2/render_slide_v2.py spec.json slide.png --cards
python scripts/v2/build_film_v2.py spec.json post.mp4 --music bed.wav \
    --hook 2.5 --hold 34.5 --beat 4.5 --send 3.5
```

`bed.wav` comes from `scripts/music_lib.py <mood> <seconds> bed.wav`.

## CONTENT RULES - change the content wisely, not just the colours

1. **Tone comes from the meaning, never the series.** bullish = gains, buying,
   rallies; bearish = falls, selling, crashes; caution = warnings, delays,
   volatility, mixed signals; neutral = plain education; festival = greetings.
   The tone drives the tag, highlight, chips, icons, swipe, CTA gradient and the
   plate glow.
2. **Headline <= ~55 characters, one accent phrase.** The renderer auto-fits two
   lines and breaks at the accent phrase, so a long headline shrinks - keep it
   short instead of letting it shrink.
3. **Three points, <= ~95 characters each.** That is two lines at 29 px. Longer
   text either wraps to a third line or forces a smaller font. Numbers, dates and
   rupee figures are coloured automatically - never hand-colour them.
4. **Icons are chosen from the point's own words** (chart, calendar-cross,
   calendar-tick, up, down, rupee, percent, shield, piggy, coins, bank, warn).
   Override with `"icons": ["chart","shield","percent"]` when the words mislead.
   Never let an icon claim something the text does not say.
5. **Question = the caption's question**, 1-5 words, <= ~55 characters, rendered
   on the marker swipe. Answerable in one line, opinion-based.
6. **CTA is content-matched and FOLLOW-framed** (see the slot table in SKILL.md).
7. **Hold time follows the word count.** ~100 words on the slide = 30-35 s hold
   (a full read plus a second look at the figures). An alert with 30 words = 20 s.
   Never shorten the hold below a full read; never pad it beyond one re-read.
8. **Film lengths:** 44.5 s default for the 7:30 term slot on LinkedIn; 30 s for
   the Instagram reel; 20-25 s for event alerts.

## What still needs a human eye

- Icon meaning: auto-pick is keyword scoring, so check each slide once.
- The phone glyph in the contact box is the weakest drawing; it is on the list.
- Backgrounds are still code-generated. AI plates (Ram's ChatGPT Go batch) drop
  into `assets_v2/plates/<tone>.png` and are picked by tone when present.
