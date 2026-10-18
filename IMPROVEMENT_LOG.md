# Asset Rama — Site Improvement Log

Suggestions accumulate here from the hourly quality cycle. The weekly Monday review implements the best ones, then marks them DONE and prunes. Hourly "audit PASS, no fixes needed" lines are dropped at each prune — only actionable items are kept.

## Open suggestions (for future weekly reviews)

- [23/09/2026] index: consider a small "As featured / popular this week" strip once traffic data exists in Search Console
- [24/09/2026] news: snapshot gold/silver rows depend on IBJA rates that stop publishing ~21:30 — consider MCX closing futures as a fresher bullion reference
- [24/09/2026] news: consider a standing card slot for AMFI monthly SIP/AUM data (released ~10th of each month) so the Mutual Funds filter always has something fresh
- [25/09/2026] lessons.html: dead CSS rule .card[data-cat="tools"] with no chip/card using it — safe to delete in the next style cleanup (hourly run must not touch CSS)
- [25/09/2026] news: economy category often runs over-stocked vs results/markets — rebalance the category mix when cards retire at the 20-card cap
- [27/09/2026] calculators: the calculator pages carry ~1KB of dead search/filter boilerplate JS per page ($('q')/$('empty')/$('count'), .chip[data-f]) — strip it in a quiet week (scope corrected 13/10: present on sip-calculator.html and cagr-calculator.html too, not just the non-SIP pages)
- [28/09/2026] news cron: add a pre-commit guard verifying payload size (~100 KB) and presence of "Market snapshot" before pushing
- [28/09/2026] a11y: several pages carry aria-current="page" on links to other pages — audit and fix in a quiet week
- [28/09/2026] news: Results filter has zero live cards outside earnings season — seed with verified results-preview stories
- [29/09/2026] news: consider adding a Bank Nifty row to the market snapshot table
- [30/09/2026] news: snapshot bullion rows switched benchmarks across hours — pick one benchmark per day so hour-over-hour changes compare like with like
- [05/10/2026] index: the homepage SIP-calculator embed has no growth chart or year-by-year table although the shared JS supports both — consider surfacing the chart
- [06/10/2026] news: same-day cards can share a lead subject and risk reading as near-duplicates — a one-line "lead subject" tag per card would make a pre-publish duplicate check mechanical
- [08/10/2026] site: nav/footer links are hard-coded absolute https://lemberam15.github.io/assetrama/ URLs — a one-time sweep will be needed when a custom domain is added
- [11/10/2026] news: snapshot Brent row disagrees with other outlets for the 9 Oct close — settle on one Brent benchmark and reconcile the row
- [11/10/2026] news: three IPO-themed cards ran together — consider capping IPO cards so the feed does not read as single-topic
- [12/10/2026] news: All India Bullion posts a 03:00 IST daily fix and a live intraday rate that can differ by ~₹400/10g on the same day — pin the snapshot bullion rows to the 03:00 fix so the value is reproducible hour to hour
- [12/10/2026] news: the snapshot heading and "as of" note hard-code the date and session state (e.g. "12 October 2026, intraday") that the hourly run edits by hand each time — consider driving both from one variable so they cannot drift apart.
- [12/10/2026] sitemap: lastmod lags real changes — 37 of 44 URLs list a date older than the file's latest commit (e.g. search.html and lessons.html both changed 12/10 but show 28/09). Reconcile every lastmod against its last significant content change in the weekly pass.
- [12/10/2026] news: snapshot Brent row was pinned to a morning quote ($103.35, shown as down) that the day's close reversed ($105.80, up) — tie the Brent row to a single end-of-day benchmark to stop intraday drift (see also the 9 Oct Brent reconcile note).

- [13/10/2026] news: the US-market card kept a pre-close headline ("US stocks start the week mixed") and an "at open" source link after the US session had closed, so the hourly run had to repoint it by hand — consider a rule that swaps the US card to the session-close article once the US market closes.
- [13/10/2026] news: the snapshot USD/INR row showed a ~2-rupee spread across outlets on 13 Oct (₹94.06–₹95.98 intraday) — pin the rupee row to one named source and timestamp (e.g. the RBI reference rate or a single wire) so hour-over-hour moves compare like with like.
- [14/10/2026] news: intraday-written cards can keep a figure the close later superseded (e.g. the 13 Oct “Nifty IT index jumps 3%” card vs the index’s 5.2% close) — consider refreshing a card’s headline figure to the session close once the market shuts.
- [14/10/2026] lessons: the "Ask AR" quick-topic chips offer "Term insurance", but no term-insurance lesson exists in articles/ — consider adding one so the topic has a matching lesson.
- [14/10/2026] news: no authorised source carried an exact mid-session Sensex/Nifty level at the noon run, so the snapshot index rows had to show a rounded level (~73,000 / ~22,700) — consider allowing an NSE/BSE official intraday value or one named wire quote as the pinned noon source so the row always carries an exact figure.

- [14/10/2026] search.html: the 41-card search index is hard-coded into the page — a shared JSON/JS data file would keep the index in sync with lessons, calculators and articles automatically.
- [14/10/2026] sitemap: news.html lastmod is stamped by hand (refreshed to 2026-10-14 in this run); a small build step could derive each lastmod from the file's last commit so it cannot lag.

- [15/10/2026] news: the "20 stories" count text is hand-edited on every run and only refreshes once a filter chip or the search box is used (the JS apply() is not called on plain load) — call apply() once on load so the count is derived from the card list, as search.html and lessons.html already do.
- [16/10/2026] news: during late-night runs (~22:00–06:00 IST) the US market is open or only just closed, so the snapshot’s US rows carry the prior session’s close for several hours — consider a small label such as "prior close (session in progress)" on the US row during those hours so the lag is explicit rather than implied.

- [16/10/2026] news: the 16 Oct run could not trace the previous card set's market levels (Sensex ~74,300, Nifty ~22,997, gold ₹1,48,677/10g, silver ₹2,16,309/kg, rupee ₹95.06, Brent ~$106, Nasdaq 26,713) to any authorised source checked in that run, so the cards were rebuilt from figures verified this run — consider a pre-publish provenance guard that flags any card figure not backed by a named source captured in the same run (extends the 28/09 payload/snapshot guard).

- [16/10/2026] news: the 72-hour cleanup keys off each card's hand-typed meta date, so a card whose source article is much older (e.g. a results-date preview) still reads as same-day and survives the rule — consider recording the source article's publish date on the card and running the cleanup against that instead.

- [17/10/2026] calculators: the SIP and CAGR calculators have no shareable state — inputs reset to defaults on reload, so a user cannot send someone the exact scenario they modelled. Consider encoding the slider values in the URL query string (e.g. ?amt=5000&rate=12&yrs=20) and reading them on load. Feature change, for the weekly pass.
- [18/10/2026] index: the homepage carries the same dead search/filter boilerplate JS as the calculator pages ($('q')/$('empty')/$('count'), .chip[data-f], data-f chips) — none of those elements exist on index.html — extend the 27/09 cleanup to index.html.

- [18/10/2026] news: the 20-card cap forces retiring a within-72h card whenever a fresh story is added (this run retired the Solara results card to fit the Yes Bank AT-1 story) — consider raising the cap to ~24 or setting explicit per-category caps (results ran at 2 vs 3 elsewhere) so the oldest same-day card is not dropped arbitrarily.

## Content pipeline (LinkedIn / Instagram) — daily improvement

- [12/10/2026] Proposed count-up (animated) hero number on the beat card — sample delivered for Ram's approval; the live 4:5 static pipeline is unchanged. Why: count-up is the top researched number+motion pattern and motion holds viewers.
- [13/10/2026] render_slide.py v18: numeric figures in the SUB-HEADLINE now take the accent colour (colour-only, same font size) — completes the number hierarchy (headline, points and chart figures already pop). Verified: py_compile + test render clean, 3/3 points, accent applied when a number is present and unchanged when not.
- [14/10/2026] render_slide.py v19: the chart's KEY value figure (largest magnitude) now renders LARGER (hero treatment) as well as in its bar colour - completes the number hierarchy on data slides (headline v16/v17, points v13, sub-headline v18 already enlarge theirs). Why: research is consistent that the figure, not the chart, is the hook. Verified: py_compile + test render clean (key figure enlarged, capped to the row step so no row collision; non-key values unchanged; no-chart slides untouched).
- [15/10/2026] render_slide.py v20: numeric figures in the SUB-HEADLINE now render BOLD (same font size; wrapping measured with the bold width) — the last key figures that were neither bigger nor bolder, completing the number hierarchy (headline v16/v17, points v13, chart v19 already pop). Verified: py_compile + test render clean (bold+accent when a number is present, byte-identical when not; 3/3 points, no overflow).
- [16/10/2026] render_slide.py v21: the mid-video BEAT CARD now carries the same transparent brand logo mark and "+ FOLLOW" chip as the main slide — the card viewers see mid-video was the last on-brand surface still missing the follow ask (Ram's rule 27/09/2026: the ask must be visible IN the video). Why: brand consistency + the follow ask on every beat. Verified: py_compile + test render clean (3/3 points; logo + chip render with no collisions); main slide byte-identical (sha1 match).
- [17/10/2026] render_slide.py v23: the chart's SOURCE NOTE no longer overlaps the last bar's label — when a note is present the bar rows shift up 16px inside the same panel (panel height, fonts and the slide fit unchanged). Why: research on finance data slides is consistent that the small on-screen source line is the credibility cue, so it must be legible, not sitting on a row. Verified: py_compile + test render clean (2/3/4/5-bar charts with a note render with clear space; the no-note chart and the no-chart slide are byte-identical to pre-v23, sha1 match).
- [18/10/2026] render_slide.py v24: the mid-video BEAT CARD's big-number value cap raised 150 -> 182px so short/medium stat-callout figures render materially bigger and fill the frame (was capped at 150). Why: 2026 stat-callout research (Moshion / KPI Studio / ChartAnimator) is unanimous that one big number is the hook and it should be as large as the frame allows. Verified: py_compile + test render clean (short value on one line, long value still auto-shrinks to 2 lines, no clipping against header or disclaimer; main slide byte-identical, sha1 match).
