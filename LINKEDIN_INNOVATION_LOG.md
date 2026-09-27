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
