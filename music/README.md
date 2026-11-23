# music/ — Ram's video music library

Mood-matched background tracks for every Asset Rama video post (LinkedIn 4:5,
Instagram Reel 9:16, Instagram Story 9:16). The pipeline no longer synthesises
a bed: it pulls a real track from here, so a crash post and a SIP explainer
sound like different pieces of music.

## How it is used

`music_lib.py` (in the video pipeline) does this on every render:

1. reads `manifest.json`
2. takes the **first track listed** for the post's mood
3. cuts from that track's `start` second (a 20–22 s window that was picked
   automatically as the loudest, steadiest stretch — no fade-ins or dead air)
4. loops with a 0.8 s equal-power crossfade if the post needs more than the
   track has left (matters only for `clip20-driving-ambition`, which is
   exactly 20 s)
5. normalises to **-12 dBFS RMS** on the active portion — the same level the
   old synth bed used, so nothing needs re-mixing
6. adds the usual sound design on top: count-up ticks + landing bell, the
   loop-close bell, the hook impact + riser, the guess clock + reveal ping
7. soft-limits at 0.90, mono-safe stereo, 0.30 s fade-in (0.05 s after a
   hook), 3.2 s fade-out

If the download fails for any reason the pipeline falls back to the old
synthesised bed automatically, so a post never fails over music.

## Mood → track

| Mood | Track (first = used) | Character |
|---|---|---|
| `finance101` | atlasaudio-motivation-corporate → paulyudin-motivation | warm corporate explainer |
| `moneystory` | paulyudin-motivation → atlasaudio-motivation-corporate | warm, human, comeback |
| `geopolitics` | mixkit-deep-urban → libertybeats-the-saviour | serious, dark, analytical |
| `event` | the-mountain-simulation-worlds → mixkit-deep-urban | tense, unsettled |
| `urgent` | eduardbykovets-the-destroyer → geronic-the-punisher | crash, selloff, shock |
| `tense` | the-mountain-simulation-worlds (from 70 s) → libertybeats-the-saviour | suspense before a decision |
| `solemn` | libertybeats-the-saviour → mixkit-deep-urban | grave news, consequence |
| `uplifting` | clip20-driving-ambition → atlasaudio-motivation-corporate | rally, milestone |
| `festival` / `festive` | studiokolomna-cant-stop-electronic-travel → paulyudin-motivation | festive, light |
| `calm` | mixkit-deep-urban (from 150 s) → studiokolomna-cant-stop-electronic-travel | low-key, steady |

## Changing a mapping

Edit `manifest.json` only — no code change, no re-render of old posts:

```json
"urgent": {"tracks": ["geronic-the-punisher", "eduardbykovets-the-destroyer"], "gain_db": -1.5}
```

* `tracks` — order is preference; the first entry that exists wins.
* `gain_db` — trim for that mood (negative = quieter). Loudness is normalised
  anyway, so this is artistic balance, not level-matching.
* `start` — optional per-mood override of where the cut begins.

Add a new track by dropping the mp3 in `tracks/` and adding an entry under
`tracks` plus a mood reference.

## Track notes

| File | Length | BPM | Notes |
|---|---|---|---|
| atlasaudio-motivation-corporate.mp3 | 124 s | 92 | soft piano/pad build |
| clip20-driving-ambition.mp3 | 20 s | 108 | exact 20 s sting, no intro |
| eduardbykovets-the-destroyer.mp3 | 129 s | ~107 | aggressive, bright |
| geronic-the-punisher.mp3 | 109 s | ~107 | hard, loud intro hit |
| libertybeats-the-saviour.mp3 | 351 s | ~80 | epic cinematic build |
| mixkit-deep-urban.mp3 | 289 s | ~80 | deep urban groove |
| paulyudin-motivation.mp3 | 76 s | 108 | motivational, warm |
| studiokolomna-cant-stop-electronic-travel.mp3 | 135 s | ~80 | upbeat electronic |
| the-mountain-simulation-worlds.mp3 | 132 s | ~107 | moody, bass-heavy |

## Licensing — read before paid use

* `mixkit-deep-urban` — Mixkit Free License: free for commercial use, no
  attribution required, but the file may not be redistributed as a standalone
  download.
* The other eight arrived from Ram with Pixabay-style numeric IDs. The Pixabay
  Content License normally allows commercial use without attribution and also
  forbids redistributing the audio as a standalone file.
* This folder is public because the render sandbox fetches it over plain HTTPS.
  That is fine for building posts, but if a strict reading of those licences
  matters (paid ads, a licensing audit), keep this folder in a private store
  and serve the pipeline from there instead.
