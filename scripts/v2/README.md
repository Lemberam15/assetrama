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
7. **Hold time follows the word count.** ~100 words on the slide = 45-50 s hold
   (two full reads plus a look at the figures). An alert with 30 words = 20 s.
   Never shorten the hold below a full read.
8. **Film length: 60 s for the 7:30 term slot** (Ram's rule, 24/11/2026:
   hook 2.5 s + slide 50 s + beat 4 s + send 3.5 s). The Instagram 9:16 reel
   runs the SAME 60 s film - same beats, same animated header - never a shorter
   cut. Event alerts stay at 20-25 s.

## Charts

`"chart": {"title": ..., "baseline": <optional>, "bars": [{"label","value","display"}]}`
draws the branded bar panel between the points and the question. Points drop to
ONE line each (~45 chars) when a chart is present, so the fonts never shrink.

- `value` is the raw number used only to size the bar; `display` is what the
  reader sees (put the sign in it: `+436`, `-576`). Negative values render red.
- Add `baseline` when the bars are deltas - index closes measured from a round
  level, flows measured from zero. Without it, three near-identical index
  closes all render as full bars and the chart says nothing.
- Use a chart only when the spread is meaningful, roughly every second or third
  post. Never invent a value to fill a bar.

## Festival posts (Ram's rule, 24/11/2026)

Festival posts use their own imagery, not the generic plate. Set BOTH
`"tone": "festival"` and a `"festival"` key:

| key | motif drawn behind the cards |
|---|---|
| `gurpurb` | gurudwara dome + side domes + finial, warm rays |
| `diwali` | three diyas with flames |
| `eid` | crescent, stars and hanging lanterns |
| `christmas` | tree, trunk and stars |
| `holi` | soft colour clouds |
| `ganesh` | diya row (override with a plate) |
| `newyear` | firework bursts |

The motif is drawn in code at low alpha BEHIND the glass cards, so it reads as a
watermark through the glass and never fights the text. A photo plate at
`assets_v2/plates/<festival>.png` (Ram's ChatGPT Go batch) wins over the drawn
motif automatically. Never put festival imagery behind the disclaimer strip.

## Instagram 9:16 reel (v2)

```
python scripts/v2/build_film_v2.py spec.json ig.mp4 --size 9:16 --music bed.wav \
    --hook 2.5 --hold 50 --beat 4 --send 3.5      # native 9:16, same 60 s film
```
(`--size 9:16` wraps each card on its own blurred plate and pastes the SAME
animated header, so the reel matches the LinkedIn film beat for beat.)

Manual equivalent:
```
python scripts/v2/reel_916_v2.py slide.png  reel_slide.png     # each 4:5 card
python scripts/v2/reel_916_v2.py hook.png   reel_hook.png
python scripts/v2/reel_916_v2.py beat.png   reel_beat.png
python scripts/v2/reel_916_v2.py send.png   reel_send.png
python <skill>/scripts/reel_916_encode.py reel_slide.png ig.mp4 30 <mood> reel_beat.png reel_send.png reel_hook.png
```

The wrapper blurs and darkens the card's own plate into the top and bottom of
the 1080x1920 frame and centres the card - it adds NO second header and no
second FOLLOW chip, because the v2 card already carries both. Keep the reel at
~30 s even when the LinkedIn film runs 44.5 s: completion drives reach on Reels.
Do not use the old `reel_916_slide.py` on a v2 card - it stamps the series
accent (blue) and a duplicate header.

## What still needs a human eye

- Icon meaning: auto-pick is keyword scoring, so check each slide once.
- The phone glyph in the contact box is the weakest drawing; it is on the list.
- Backgrounds are still code-generated. AI plates (Ram's ChatGPT Go batch) drop
  into `assets_v2/plates/<tone>.png` and are picked by tone when present.
