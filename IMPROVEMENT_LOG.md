# Asset Rama — Site Improvement Log

Suggestions accumulate here from the hourly quality cycle. The weekly Monday review implements the best ones, then marks them DONE and prunes. Hourly "audit PASS, no fixes needed" lines are dropped at each prune — only actionable items are kept.

## Done (weekly review, 12/10/2026)

- [05/10/2026] calculators: built "What is an EMI?" and "Lumpsum vs SIP" lessons so the EMI and lumpsum calculators each link to their own topic (EMI calculator → what-is-emi; lumpsum calculator → lumpsum-vs-sip).
- [08/10/2026] lessons.html: each filter chip now shows its per-category count (e.g. "Mutual Funds (11)"), computed in JS on load — no restyle.
- [11/10/2026] search.html: the "39 pages" count text is now generated from the card list on load, so it cannot drift as pages are added or removed.
- [05/10/2026] sitemap: news.html lastmod refreshed to 2026-10-12; two new lesson URLs added; sitemap now lists every page.
- [05/10/2026] lessons.html: ItemList JSON-LD extended to 31 items (the two new lessons added).

## Open suggestions (for future weekly reviews)

- [23/09/2026] index: consider a small "As featured / popular this week" strip once traffic data exists in Search Console
- [24/09/2026] news: snapshot gold/silver rows depend on IBJA rates that stop publishing ~21:30 — consider MCX closing futures as a fresher bullion reference
- [24/09/2026] news: consider a standing card slot for AMFI monthly SIP/AUM data (released ~10th of each month) so the Mutual Funds filter always has something fresh
- [25/09/2026] lessons.html: dead CSS rule .card[data-cat="tools"] with no chip/card using it — safe to delete in the next style cleanup (hourly run must not touch CSS)
- [25/09/2026] news: economy category often runs over-stocked vs results/markets — rebalance the category mix when cards retire at the 20-card cap
- [27/09/2026] calculators: the non-SIP calculator pages carry ~1KB of dead search/filter boilerplate JS per page ($('q')/$('empty')/$('count'), .chip[data-f]) — strip it in a quiet week
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

## Content pipeline (LinkedIn / Instagram) — daily improvement

- [12/10/2026] Proposed count-up (animated) hero number on the beat card — sample delivered for Ram's approval; the live 4:5 static pipeline is unchanged. Why: count-up is the top researched number+motion pattern and motion holds viewers.
