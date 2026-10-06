# Asset Rama — Site Improvement Log

Suggestions accumulate here from the hourly quality cycle. The weekly Monday review implements the best ones, then marks them DONE and prunes. Hourly "audit PASS, no fixes needed" lines are dropped at each prune — only actionable items are kept.

## Open suggestions (for future weekly reviews)

- [23/09/2026] index: consider a small "As featured / popular this week" strip once traffic data exists in Search Console
- [24/09/2026] news: snapshot gold/silver rows depend on IBJA rates that stop publishing ~21:30 — consider MCX closing futures as a fresher bullion reference
- [24/09/2026] news: consider a standing card slot for AMFI monthly SIP/AUM data (released ~10th of each month) so the Mutual Funds filter always has something fresh
- [25/09/2026] lessons.html: dead CSS rule .card[data-cat="tools"] with no chip/card using it — safe to delete in the next style cleanup (hourly run must not touch CSS)
- [25/09/2026] news: economy category often runs over-stocked vs results/markets — rebalance the category mix when cards retire at the 20-card cap
- [27/09/2026] calculators: the 5 non-SIP calculator pages carry ~1KB of dead search/filter boilerplate JS per page ($('q')/$('empty')/$('count'), .chip[data-f]) — weekly task could strip it
- [28/09/2026] news cron: add a pre-commit guard verifying payload size (~100 KB) and presence of "Market snapshot" before pushing — placeholder-overwrite incidents recurred repeatedly 27–30 Sep and again on 5 Oct; the guard belongs to the hourly cron task, not the weekly site task
- [28/09/2026] a11y: several pages carry aria-current="page" on links to other pages (e.g. the SIP Calculator menu link on every calculator page) — audit and fix in a quiet week
- [28/09/2026] news: Results filter has zero live cards outside earnings season — seed with verified results-preview stories from authorised outlets when fresh results news is scarce
- [29/09/2026] news: consider adding a Bank Nifty row to the market snapshot table — figures appear in every daily wrap, so data is easy to verify hourly
- [30/09/2026] news: snapshot bullion rows switched benchmarks across hours (IBJA retail earlier, MCX futures at 11:02) — pick one benchmark per day so hour-over-hour changes compare like with like
- [05/10/2026] index: the homepage SIP-calculator embed has no growth chart or year-by-year table although the shared calculator JS already supports both (dormant no-ops on this page) — consider surfacing the chart in the embed
- [05/10/2026] calculators: EMIs and lumpsum calculators still cross-link only to SIP/CAGR lessons — build "What is an EMI?" and "Lumpsum vs SIP" lessons so each calculator links to its own topic (same pattern as the FD/SWP fix this week)
- [05/10/2026] sitemap: news.html lastmod drifts behind its hourly updates (refreshed manually this run) — weekly task could automate lastmod for news.html, or drop it, since the page changes every hour
- [06/10/2026] news: same-day cards can share a lead subject (e.g. an index-move card and a company-results card both naming Trent) and risk reading as near-duplicates — a one-line "lead subject" tag per card would make a pre-publish duplicate check mechanical
