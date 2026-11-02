# Asset Rama — Site Improvement Log

Suggestions accumulate here from the hourly quality cycle. The weekly Monday review implements the best ones, then marks them DONE and prunes. Hourly "audit PASS, no fixes needed" lines are dropped at each prune — only actionable items are kept.

## Done — week of 02/11/2026

- [02/11/2026] DONE — index.html fragment deep links (logged 30/10, recurred 31/10 and 02/11, oldest unfixed area-0 item). lessons.html now carries real `id="mf"`, `id="basics"`, `id="market"`, `id="commodity"`, `id="gold"` and `id="tax"` anchor targets immediately above the lesson grid, with `scroll-margin-top:96px` so the sticky header does not cover the landing point. The existing `location.hash` script still clicks the matching chip, so with JS the filter applies and without JS the reader now lands on the library grid instead of the top of the page. Verified: anchors resolve, 0 broken links, tags balanced.
- [02/11/2026] DONE — article title/meta-description batch trim (logged 30/10, carried 31/10). Ten lessons were out of band; all ten now sit inside it. Titles: market-falls-sip 89→60, what-is-fd 85→69, what-is-swp 77→65, what-is-emi 73→66, what-is-health-insurance 73→65, what-is-sip 71→65, what-is-cagr 71→67. Descriptions: what-is-swp 186→152, what-is-dividend 184→145, what-is-term-insurance 182→165, what-is-fd 178→141, hra-exemption 176→149. og:title, twitter:title, og:description and twitter:description were rewritten in the same pass so social cards and search show one string. Verified: 0 of 37 articles now outside 70 chars / 100-175 chars.
- [02/11/2026] DONE — sitemap news.html signal (logged 28/10). news.html now carries `changefreq=hourly` instead of `weekly`, and its `lastmod` was bumped from 31/10 to 02/11, matching the page's hourly rewrite. lessons.html `lastmod` also bumped to 02/11.
- [02/11/2026] DONE (first step) — library rebalance toward thin topics (logged 29/10). Two new lessons added: `articles/what-is-ulip.html` (Insurance — the chip had only two lessons, both filed under Basics) and `articles/what-is-tax-harvesting.html` (Tax — the highest-volume tax question the library did not answer). Both wired into lessons.html cards, count text, ItemList JSON-LD, search.html cards and count text, and sitemap.xml. Lessons 35→37, search 45→47. The commodities and economy chips are still thin — carry forward.

## Open suggestions (for future weekly reviews)

- [30/10 + 31/10] articles: every lesson inlines its own identical ~31 KB `<style>` block and ~8 KB JS block, so the library carries roughly 1.4 MB of duplicated payload and any design fix means 37 edits. Extract one `article.css` + `article.js`. No visual change. This is the biggest single win in the repo and the gate for all further article work.
- [26/10 + 30/10 + 31/10] lessons: the card list, the "37 lessons" count text and the ItemList JSON-LD are three hand-maintained copies of one fact, and the ItemList order already disagrees with the card order. Generate all three from the article files at build time.
- [14/10 + 26/10 + 31/10] search: the 47 cards and the "47 pages" count are hand-maintained, so a new lesson is live and sitemapped but unsearchable until someone edits by hand. Generate the index from the file tree at build time.
- [14/10 + 23/10 + 26/10] sitemap: lastmod is typed by hand and nothing enforces coverage. Derive lastmod from the file's last commit and add a build check that every .html except 404.html and google*.html appears in sitemap.xml.
- [28/10 + 29/10 + 30/10 + 01/11] calculators: `calc.js` extraction (~6.5 KB of identical chart/formatter JS on each of the 8 calculators) is the gate for the rest — a single nav partial instead of nine hand-copied 17-link blocks, a visible "Assumptions" line under each result, a "last reviewed" date, and a reverse mode on the CAGR page.
- [17/10] calculators: encode SIP and CAGR slider state in the URL query string (`?amt=&rate=&yrs=`) so a modelled scenario can be shared. Feature change.
- [27/10] articles: no lesson shows a "last reviewed" date, so neither a reader nor the weekly task can tell whether the tax and rate figures were checked against the current year. One visible `Reviewed: <Month YYYY>` line under the byline, plus a rotation check flagging anything reviewed more than two quarters ago.
- [27/10] 404.html: every internal link is an absolute production URL while the rest of the site uses relative paths — normalise in one batch pass.
- [01/11] index.html: the JSON-LD carries only the site/org/person graph, with no ItemList for the eight calculators it promotes. Generate it at build time.
- [05/10 + 21/10] index: surface the growth chart and year-by-year table in the homepage SIP embed; the hero illustration is a hand-baked SVG with fixed figures — generate both from the shared SIP maths.
- [27/10] articles: sibling lessons are linked as `../articles/x.html` from inside `articles/` — correct but redundant. Normalise to `x.html` across the library.

## News page — open guards (hourly cycle)

- [02/11] news: the CollectionPage JSON-LD carries no `dateModified`, so nothing tells a crawler the page was rewritten in the last hour — the hourly refresh is invisible as a freshness signal. Generate `dateModified` at build time from the commit timestamp; a hand-typed value would be stale within the hour, which is why this is not an hourly fix.
- [24/09 + 11/10 + 13/10 + 27/10 + 28/10 + 02/11] news: pin each commodity row AND its card copy to one named, timestamped benchmark per day (MCX futures vs IBJA retail vs PTI futures is the recurring drift), and label the instrument in the row. Needs a decision from Ram on which benchmark to standardise on. Recurred 02/11: the Sarafa Association had no verifiable Monday print at 08:00 IST, so the gold and silver rows moved to the India Bullions Mumbai reference mid-series — the exact drift this entry is about.
- [20/10 + 23/10 + 25/10 + 27/10] news: build-time checks that (a) each card's outlet label matches its href domain, (b) no card href contains `live-updates` or `/live/`, (c) every card's SVG gradient id and href is unique. Catches the three most frequent failure modes in one pass.
- [19/10 + 31/10 + 01/11] news: a per-category floor and a soft per-category cap (~4). The Mutual Funds chip has repeatedly dropped to one card, and results once held 6 of 20.
- [27/10] news: derive the visible "20 stories" count from the rendered card count and assert `count == cards` before commit.
- [18/10 + 24/10] news: the 20-card cap forces same-day retirement on most runs; raise to ~24 or set per-category caps.
- [12/10 + 28/10] news: drive the snapshot heading and its "as of" note from one variable; add a per-row `live`/`close` status tag so an intraday print cannot be read as a close.
- [28/09] news cron: pre-commit guard on payload size (~100 KB) and presence of "Market snapshot".
- [16/10 + 20/10 + 25/10] news: label non-trading days explicitly ("previous session — market holiday"), show the weekly move on those days, and record each source article's publish date on its card so the 72-hour cleanup keys off it.

## Content pipeline (LinkedIn / Instagram) — daily improvement

- [17/10–01/11] render_slide.py v23→v40 and the beat/story cards: one-accent-per-post hierarchy, chart key-row emphasis, gray-first supporting bars, unit step-back on numeric beats, quiet 01/02/03 markers and kickers, and a source note raised to 4.5:1 contrast. Full entries for each version are in the git history of this file (commit log for 18/10–01/11); the pipeline is otherwise unchanged and needs no action this week.
- [12/10] Proposed count-up (animated) hero number on the beat card — sample delivered for Ram's approval; the live 4:5 static pipeline is unchanged.
