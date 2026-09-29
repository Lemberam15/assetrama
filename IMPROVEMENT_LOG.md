# Asset Rama — Site Improvement Log

Suggestions accumulate here from the hourly quality cycle. The weekly Monday review implements the best ones, then marks them DONE and prunes. Hourly "audit PASS, no fixes needed" lines are dropped at each prune — only actionable items are kept.

## DONE — weekly review 28/09/2026

- [28/09/2026] DONE calculators: added compound-interest-calculator.html (compound + simple interest modes, chart, year table, FAQ JSON-LD) — wired into every page footer, search.html card, sitemap (was suggested 23/09)
- [28/09/2026] DONE lessons: added articles/what-is-health-insurance.html — sum insured, cashless vs reimbursement, IRDAI 2024 rules (1-hour cashless, 30-day settlement, 36-month PED cap, 60-month moratorium), Section 80D / Section 126 tax — wired into lessons (27th card + ItemList), search, sitemap (was suggested 23/09)
- [28/09/2026] DONE repo: deleted duplicate Google Search Console verification file "google23bf20c55c0ff476 (1).html" (suggested 23/09 and 27/09)
- [28/09/2026] DONE fd-calculator: default tenure changed from 20 years to a typical 5 years (suggested 26/09)
- [28/09/2026] DONE articles: capital-gains-tax-mutual-funds.html refreshed for FY 2026-27 — title, meta, table label and FAQ now say current rates after verifying Budget 2026 left 12.5%/20% unchanged; dateModified bumped (suggested 24/09 and 27/09)
- [28/09/2026] DONE search.html: og/twitter meta descriptions reworded to be count-free so they stop going stale; "35 pages" count text updated to 37 with the two new cards (suggested 24/09)
- [28/09/2026] DONE news.html: footer "Market falls & SIPs" now uses the & entity, and 2+ blank-line runs left by card rotation collapsed (suggested 27/09); same bare-& fixed in every other page footer

## DONE — hourly quality cycle 29/09/2026 (22:00 IST)

- [29/09/2026] DONE news: gold-rate card now links to Mint's English gold/silver rate story (was ET Now Hindi — not an authorised source); card content unchanged
- [29/09/2026] DONE news: deduped the two 29 Sep cards sharing the BusinessLine liveblog URL — the Nifty-rejig card now links to the Economic Times Nifty-rejig article, so all 20 cards carry unique source links

## Open suggestions (for future weekly reviews)

- [23/09/2026] index: consider a small "As featured / popular this week" strip once traffic data exists in Search Console
- [24/09/2026] news: snapshot gold/silver rows depend on IBJA rates that stop publishing ~21:30 — consider MCX closing futures as a fresher bullion reference (the 26/09 14:00 cycle already used MCX spot once)
- [24/09/2026] news: consider a standing card slot for AMFI monthly SIP/AUM data (released ~10th of each month) so the Mutual Funds filter always has something fresh
- [25/09/2026] calculators: swp/lumpsum/emi/fd/ppf calculators still cross-link only SIP/CAGR articles — consider SWP and FD explainer lessons so each calculator links to its own topic
- [25/09/2026] lessons.html: dead CSS rule .card[data-cat="tools"] with no chip/card using it — safe to delete in the next style cleanup (hourly run must not touch CSS)
- [25/09/2026] news: economy category often runs over-stocked vs results/markets — rebalance the category mix when cards retire at the 20-card cap
- [27/09/2026] calculators: the 5 non-SIP calculator pages carry ~1KB of dead search/filter boilerplate JS per page ($('q')/$('empty')/$('count'), .chip[data-f]) — weekly task could strip it
- [28/09/2026] news cron: add a pre-commit guard verifying payload size (~100 KB) and presence of "Market snapshot" before pushing — placeholder-overwrite incidents keep recurring (27 Sep ~21:00, 28 Sep 00:00, 28 Sep 05:00, 28 Sep 09:00, 28 Sep 10:00, 28 Sep 17:05 and 28 Sep 21:05 — the last four reverted within a minute via follow-up commit) — the guard belongs to the hourly cron task, not the weekly site task
- [28/09/2026] a11y: several pages carry aria-current="page" on links to other pages (e.g. the SIP Calculator menu link on every calculator page) — audit and fix in a quiet week
- [28/09/2026] lessons: ItemList JSON-LD has no top-level "name" — consider adding "All Finance Lessons" (and possibly numberOfItems) for richer snippets; structure otherwise valid, all 27 item URLs resolve
- [28/09/2026] news: Results filter has zero live cards outside earnings season (Q2 FY27 season starts mid-Oct) — consider seeding with verified results-preview stories from authorised outlets when fresh results news is scarce
- [29/09/2026] news cron: placeholder-overwrite hit AGAIN at 29 Sep 03:04 IST (commit 3d4b017, restored within ~1 min by 6bb8a8f) — reinforces the 28/09 pre-commit payload-size + "Market snapshot" guard suggestion
- [29/09/2026] news cron: placeholder-overwrite hit AGAIN at ~07:35 IST (commit c13ca7f, full 20-card page restored within ~2 min by 8eb6d6d) — the commit call sent a literal placeholder string instead of the file bytes; reinforces the 28/09 pre-commit size + "Market snapshot" guard suggestion
- [29/09/2026] news: results category has had 0 cards for several runs; consider a quarterly-results story slice each run to balance all 7 categories
- [29/09/2026] news: consider adding a Bank Nifty row to the market snapshot table — figures appear in every daily wrap (28 Sep close 54,472, -1,109 pts per CNBC-TV18), so data is easy to verify hourly
- [29/09/2026] news cron: placeholder-overwrite hit AGAIN at ~12:05 IST (commit 744ad69, full 20-card page restored within ~1 min by ed89fb1) — the commit call again sent a literal placeholder string instead of file bytes; strongly reinforces the 28/09 pre-commit payload-size + "Market snapshot" guard suggestion
- [29/09/2026] news cron: placeholder-overwrite hit AGAIN at 29 Sep 14:03 IST (commit 7ce2e949 sent a literal placeholder token instead of file bytes; restored within ~1 min by e6fe1cdd) — the committing code path must read news.html from disk and assert size >100 KB + "Market snapshot" present before pushing; reinforces the 28/09 guard suggestion
- [29/09/2026] news: mf filter dropped to 0 cards after the 24 Sep SIP card crossed the 72h window — no fresh AMFI/outlet story available this hour; reinforces the 24/09 standing-AMFI-slot suggestion
- [29/09/2026] news cron: placeholder-overwrite hit AGAIN at 15:04 IST (commit d0d40c0b wrote a literal placeholder token; full 20-card page restored within ~1 min by 76016861, verified by re-fetch: 114,296 bytes, 20 cards, snapshot + rejig card intact) — the committing code path MUST read news.html from disk and assert size >100 KB + 'Market snapshot' present before pushing
- [29/09/2026] news cron: placeholder-overwrite hit AGAIN at 29 Sep 16:05 IST (commit 8cb2d150 sent a literal placeholder token instead of file bytes; full 20-card page restored within ~1 min by 67897f77, verified via GitHub API: 114,430 bytes, 20 cards, 29 Sep close snapshot intact) — same fix needed: assert size >100 KB + 'Market snapshot' present before pushing
