# LinkedIn Innovation Log — Asset Rama

**Mission:** within 12 months (by 09/2027) Ram is one of India's top 100 individual
finance voices on LinkedIn. Posts must feel like they come from a big institution:
accurate, beautiful, plain-English, mobile-first.

Maintained by the weekly **Innovation Lab** (Saturdays 12:00 PM IST). One improvement
ships every week. Immutable rules: URL + emoji checks, Follow line, disclaimer,
hashtags, CTA table, tone colors, red-for-negative charts. Never ship unverified numbers.

## Shipped

- 21–23/09/2026 — v8 slide system: tone colors, optional data charts with red
  negatives, content-matched CTAs, auto-fit fonts (baseline).
- 24/09/2026 — Creative festival & event posts: real free-license photos,
  cinematic design (`scripts/creative_slide.py`).
- 25/09/2026 — v2 creative slide: near-black scrim behind text (measured
  worst-case contrast ≥ 6:1), dark glass chips, exact optical alignment.
- 25/09/2026 — Emoji mechanical check added to caption pre-flight
  (guards against 🏢/📓/📈 substitutions on the website line).
- 26/09/2026 — Music now follows CONTENT, not just series (Ram's rule):
  mood chosen per post, no two consecutive posts with the same mood.
- 26/09/2026 — ENGAGEMENT SYSTEM (Ram's directive: impressions but no
  comments/reactions):
  (1) Caption Engagement Engine — opinion line + 1-5-word answerable
      questions (this-or-that / yes-no / number / fill-in-the-blank /
      comment-keyword) in all 6 posting agents.
  (2) Follow-boost: TOMORROW TEASER before the Follow line (concrete
      reason to follow now).
  (3) In-video engagement (v9, Ram approved after sample review):
      engagement question strip rendered above the CTA (accent arrow),
      "+ FOLLOW" chip under RAM LEMBE, and all CTAs re-framed to start
      with FOLLOW (e.g. FOLLOW TO LEARN A TERM DAILY) — because video
      viewers rarely read captions. render_slide.py v9 published to the
      skill; all 6 posting agent prompts updated. Samples:
      v9_Design_Sample_A / v9_Design_Sample_B (delivered 26/09/2026).
- 26/09/2026 (evening) — Creative slide v3: text block now VERTICALLY
  CENTERED in the free zone (Ram's review of Swati's short festival
  sample: content sank to the bottom, top half empty). Fix published to
  the live skill and to Swati's v15 upgrade document.

## Ideas backlog (candidates for future weeks — do not repeat shipped items)

1. Kinetic typography: headline words appearing in sequence (pre-market posts).
2. Carousel-style multi-frame videos (5 quick frames) for Money Story posts.
3. "By the numbers" stat-grid dashboard template for FII/DII posts.
4. Animated bar growth (chart build-up) for gold/SIP/growth posts.
5. Quote-card variant for Money Story (real quote + attribution, verified source).
6. Big-number post: one huge verified number fills the slide, tiny context line.
7. Week-in-review Saturday recap format.
8. Month-start personal-finance checklist format (1st of month).
9. Caption hook A/B: test two first-line patterns per week; Ram reports which
   performed better; lab keeps a running scoreboard in this file.
10. Marathi/Hindi bilingual festival posts (Ram's audience includes Marathi speakers).

## Earning roadmap milestones (the ladder to income)

- NOW (1,562 followers, 26/09/2026) -> 10,000: pure trust-building. Free everything. Grow.
- 10,000 -> 50,000: newsletter sponsorships, brand collaborations, affiliate partnerships.
- 50,000+: own products — workshops, course, corporate financial-literacy training, speaking.

LinkedIn pays nothing for posts — the audience pays for trust, tools and teaching.
The funnel: LinkedIn posts -> Asset Rama free calculators -> trust -> products.
Never violate: educational only (SEBI lane), no stock tips, no undisclosed paid
promotions, no employer mention. Trust IS the product.

## Metrics (Ram reports from the LinkedIn app each Saturday; lab records here)

| Date | Followers | Avg views last week | Best post | Notes |
|------|-----------|--------------------|-----------|-------|
| 26/09/2026 | 1,562 | — | — | baseline (public profile count); lab starts 03/10 |
| 27/09/2026 | Instagram automation LIVE: _assetrama (471 followers) connected via Instagram API (REELS, 60-day token). Test post published: instagram.com/reel/DdyQ8dIjuu1. ALL 12 agents Instagram-enabled (6 posting agents cross-post after every LinkedIn post; 6 monitors cross-post whenever they publish an event/festival post); videos hosted in /videos on the website with 3-day cleanup; weekly Sunday 6 AM token-refresh cron added. Instagram goal: top finance voice on IG alongside LinkedIn. |


## 27/09/2026 (evening) — MISSION UPGRADE: #1 finance Instagram channel in 2 years

Ram set the new north-star ambition: Asset Rama becomes India's #1 finance Instagram channel within 2 years (alongside the existing LinkedIn top-100-in-12-months goal), with a standing rule that improvements happen autonomously across ALL parameters — no hand-holding.

Shipped today to support it:
- **Instagram Growth Tracker cron (Saturdays 5 PM IST)**: pulls followers + per-post likes/comments directly from the Instagram API (no more asking Ram for IG numbers), computes weekly deltas, reports honestly with top/bottom posts. Baseline: 471 followers, 27/09/2026.
- **Innovation Lab upgraded**: now starts every weekly run by pulling real Instagram + LinkedIn numbers, and picks the weekly improvement based on the WEAKEST metric (data-driven, not taste-driven). Research scope expanded to Instagram/Reels creators worldwide.
- Same-day quality upgrades: v4 static slides (zoom removed after it cropped text), ASSET RAMA brand name on all slides, color system v7.1 (cyan-steel geopolitics, orange-amber caution — verified distinguishable + all contrast >= 6.9:1).
- Both platforms verified live end-to-end today with a Rule of 72 test post (LinkedIn post 7509920446734245888, IG reel DdyY76FFdYt).

Backlog candidates: native 9:16 Instagram Reels render (pillarboxing today); YouTube Shorts automation (Google audit hurdle); Instagram hashtag strategy tuned for Reels discovery.


## 27/09/2026 (night) — LINEUP CHANGE: Wrap + FII/DII clubbed into one 8:30 PM post

Ram approved clubbing the two most overlapping market posts. Data-timing check first: NSE publishes provisional FII/DII cash figures ~5-6 PM IST, finalized by 7-8 PM — so a 5 PM merged post was ruled out and the merged post took the proven 8:30 PM slot.

- **New cron**: "LinkedIn 8:30PM — Market Wrap + FII/DII (merged)" — one complete end-of-day recap: Sensex/Nifty close + FII/DII net flows (chart panel with both flow bars) + one combined takeaway. Same quality bar: triple QC, engagement engine, 48h ledger, trends note, Instagram cross-post, ASSET RAMA branding, static v4 slide.
- **Deleted**: old 4:15 PM Post-Market Wrap cron and old 8:30 PM FII/DII cron.
- **Trading-day lineup now 5 posts**: 7:30 AM term, 8:45 AM pre-market, 12:30 PM story, 6 PM geopolitics, 8:30 PM wrap + flows. Non-trading days unchanged (3 posts).
- **SKILL.md updated**: series table and tomorrow-teaser slot list now reflect the merged slot.
- Cron count: 17 (12 posting/monitor agents minus one, plus radar + tracker + 3 website + token refresh).

## 10/10/2026 — v15: BEAT-CUT MOTION (kill the single static hold) + music v4

**Growth data (pulled from the APIs):**
- Instagram: **469 followers** (baseline 471 on 27/09/2026 → net **-2**, flat-to-down).
  Last 30 media: likes 0-4, **comments 0 on every post**. The weakest number is
  **comments/engagement**; follower growth is flat. Platform that needs it most =
  Instagram (the 2-year north-star channel).
- LinkedIn: baseline 1,562 (26/09/2026); no new number reported in chat this week —
  update when Ram reports it.

**What changed (this week's one improvement):** the 20-second post was a SINGLE
static shot held the whole time — the biggest documented retention leak in 2026
short-form ("a static frame in a moving feed reads as a pause"; motion in frame 1
beats a static open by ~23% on 3-second retention; "visual variety carries the
middle; each change resets attention"). v15 cuts every video into **2-3 beats with
hard cuts** — full slide → a new **big-number beat card** → full slide — plus a soft
**light sweep** at each beat start.
- New spec field `"beat": {kicker, value, label}` (OPTIONAL). render_slide.py then
  also writes `<slide>_beat.png` (brand-matched 1080x1350 big-number card).
- make_video.py takes an optional 6th arg (the card) and renders the hard-cut edit.
- First frame is STILL the full slide at full brightness (thumbnail safe; hook text
  at frame 0.0, zero fade-in — the 2026 hook rule).
- **Backwards compatible:** no `"beat"` and no 6th arg → the old static video is
  byte-for-byte unchanged.
- The beat card doubles as the long-planned "big-number post" (backlog #6).
- v15.1 fix: render_slide.py now prints `points rendered N/3` and a WARNING when
  auto-fit silently DROPS a point (found while building these samples — Sample A's
  first render dropped a point). Agents must shorten copy and re-render.

**Music v4 (rotation):** built on v3 (warm, mono-safe, no saturation). Adds a warm
sub-bass root per chord, a soft low "heartbeat" pulse for driving moods
(urgent/tense/event/solemn) and a very quiet high shimmer for bright moods
(uplifting/festival/finance101/moneystory). Loudness target unchanged (~ -12 dBFS
RMS). QC'd by encoding samples: 20.00 s, mean ~ -13.7 dBFS, peak ~ -0.6 dB — normal.

**Post types affected:** ALL 12 daily slots + creative festival/event posts (any post
whose spec adds a `"beat"`). LinkedIn and Instagram reels both use the beat edit;
stories are unchanged.

**Samples (delivered as downloads):** sampleA_marketwrap.png / _beat.png / .mp4
(verified 09/10/2026 FII/DII flows: FII -Rs 3,569 cr, DII +Rs 4,743 cr, Sensex
72,472 +879, Nifty 22,520 +289); sampleB_sip.png / _beat.png / .mp4 (clearly
ILLUSTRATIVE SIP: Rs 5,000/month, 20 years, assumed 12% → about Rs 50 lakh).
Pixel QC: contrast ~17.7:1 (>=3 required), zero edge clipping, 20.00 s, no overlap;
beats verified by frame diff (t=4 slide, t=8 card, t=14 slide).

**New backlog ideas (added this week):**
1. Kinetic typography — headline words punching in sequence in the FIRST beat
   (kept frame-0-safe so the hook text is present at 0.0 s).
2. Second beat-card variant: a 2-bar mini-chart card (FII vs DII) as the mid cut.
3. SEND TRIGGER line in the final 5 s + a "send this to…" caption line (2026 data:
   sends are weighted ~3-5x likes and are now a top signal).
4. First-comment-with-a-question on LinkedIn (a "second distribution event" that
   drove the highest comment counts in a 2026 study of high-performing posts).
5. Native 9:16 Instagram reel render (still pillarboxed today) — the biggest
   remaining Instagram reach lever.

**Monetization note (suggestion only):** at 469 IG / ~1.5k LinkedIn, the
highest-value next action is the FREE one — start collecting WhatsApp numbers. Ram
already shows the "EDUCATIONAL QUERIES 9049547427" box on every slide; add a
one-line caption ask ("Save my number for market updates") plus a pinned comment,
so the list is building well before the 10k sponsor stage. No spend, no brand
contact — pure list-building.
