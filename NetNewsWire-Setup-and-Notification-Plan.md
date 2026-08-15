# NetNewsWire setup and notification plan

## Import

Import [NetNewsWire-Finance-Cyber-iPhone-Lite.opml](./NetNewsWire-Finance-Cyber-iPhone-Lite.opml) for the recommended lower-burden phone setup, or [NetNewsWire-Finance-Cyber.opml](./NetNewsWire-Finance-Cyber.opml) for the complete 51-feed master bundle. The OPML supplies the folders and feed URLs; notification preferences are best reviewed manually after import.
Review [Coverage-Gap-Assessment.md](./Coverage-Gap-Assessment.md) for the source-selection decisions behind the bundle.
Use the [RSS feed discovery and addition prompt](./NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md) when searching for new candidates; it defines the evidence, mobile-cost and rejection gates before any feed is added.
The [feed manifest](./feed-manifest.json) is the source of truth. Run `make generate` after changing it rather than editing generated OPML or source-table rows by hand.
Use the generated [notification/profile matrix](./NetNewsWire-Notification-Profile.md) as the post-import per-feed checklist; the machine-readable version is [NetNewsWire-Notification-Profile.json](./NetNewsWire-Notification-Profile.json).

## iPhone refresh profile

The master bundle full-response baseline measured 5.11 MB of decompressed feed bodies and about 1.48 MB of compressed/wire bytes across 51 feeds; five feeds exceeded the body review threshold and one exceeded 1 MB. The iPhone-lite bundle contains 30 feeds and measured 1.82 MB of bodies, 0.70 MB of wire bytes and two body-threshold reviews; the latest run also recorded one fetch over two seconds. NetNewsWire and the validator can use conditional requests, so actual repeat-refresh traffic can be lower.

For the lowest notification and reading burden, use the iPhone-lite OPML, leave Optional folders notification-off and summarize them in batches. The master bundle retains industrial-control and specialist research feeds for later use.

## Notifications

Start with only these feeds enabled for notifications:

- Nasdaq Trader — Trade Halts
- Ireland NCSC — Alerts & Advisories
- CISA — All Advisories
- CERT-EU — Security Advisories

Use as optional notifications only when you need them:

- Federal Reserve — Monetary Policy
- European Central Bank — Press
- Central Bank of Ireland — News
- Bank of England — News
- NCSC UK — News
- NCSC UK — All Updates
- CERT-FR — Security Alerts (French), if French-language headlines are useful
- CISA — ICS Advisories, if industrial systems matter to you
- Cisco PSIRT, if you use Cisco products

Keep Nasdaq Trader — Equity Trader Alerts, HM Treasury — News & Communications, CERT-FR — Security Advisories (French), all commercial news, research, CFTC regulatory, ECB operations/statistics, European Commission sanctions guidance, CERT/CC vulnerability-note, exchange-rate, macro-data, release-calendar and speech feeds notification-off. Review them in one daily Apple Intelligence digest instead of receiving an alert for every article.

## Apple Intelligence workflow

1. Read urgent notifications directly from the official source.
2. Export selected or unread Finance/Cyber items as JSON.
3. Run `python3 prepare-rss-digest-input.py --input selected-articles.json --output digest-input.json --state .digest-state.json`.
4. Use [Apple-Intelligence-RSS-Summary-Prompt.md](./Apple-Intelligence-RSS-Summary-Prompt.md) with the resulting package.
5. Ask for one daily digest, with duplicate events clustered and corroborating sources grouped underneath.
6. Treat a headline as a lead until an official source confirms it.

Use the [daily digest mode](./Apple-Intelligence-RSS-Summary-Prompt.md#daily-digest-mode) every day with the prepared input. The [daily workflow](./NetNewsWire-Daily-Digest-Workflow.md) documents the JSON format and state behavior. It is a summary format, not a live-price service or an automatic schedule.

## Finance boundaries

The feeds provide news, official releases and reference data. They do not provide live quotes, order books, broker execution, portfolio positions or trade IDs. Use a broker or market-data application for live trading information.

Use the [Market Hours and Holiday Reference](./Market-Hours-and-Holiday-Reference.md) for Dublin, London and US opening times, auction phases, the 2026 daylight-saving mismatch windows and official holiday links. Do not infer an open market from an RSS headline.

## Useful web-only references

These are deliberately not in the OPML because they are not verified direct RSS/Atom feeds:

- [Apple security releases](https://support.apple.com/100100) — useful for iPhone and iPad security updates.
- [CSO Ireland release calendar](https://www.cso.ie/en/csolatestnews/releasecalendar/) — Irish official-statistics timing.
- [Euronext trading hours and holidays](https://www.euronext.com/en/trading/trading-hours-holidays) — exchange calendar and session caveats.
- [Euronext cash-market notices](https://www.euronext.com/en/products-services/cash-market-notices) — official notices portal.
- [NYSE trading halts](https://www.nyse.com/trade/trading-halts) — official live page and CSV; no verified public RSS feed was found.
- [Coverage-gap assessment](./Coverage-Gap-Assessment.md) — current RSS candidates rejected or retained, with exact reasons.
- [CISA Known Exploited Vulnerabilities catalogue](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) — structured vulnerability data, not RSS.
- [US Treasury press releases](https://home.treasury.gov/news/press-releases) — official macro/fiscal source, currently retained as a web reference because no verified direct RSS endpoint was found.
- [BEA News Releases](https://www.bea.gov/news) — official US GDP, personal-income/PCE, trade and investment releases; its RSS candidate was tested but excluded because one historical item has a malformed schemeless link.
- [Ireland Department of Finance](https://www.gov.ie/en/department-of-finance/) — official fiscal and budget coverage; tested RSS paths were blocked or unavailable, so this remains a web reference.
- [Nasdaq Trader news and alerts](https://www.nasdaqtrader.com/Trader.aspx?id=NewsRSS) — official feed directory; the focused Equity Trader Alerts stream is already in the OPML, while the broad current-headlines stream was rejected as too large and mixed.

## Maintenance

Run `make test`, `make validate` and `make validate-lite` monthly. Review the generated [master Markdown report](./NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md), [master JSON report](./NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json), [iPhone-lite report](./NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.md) and [coverage-gap assessment](./Coverage-Gap-Assessment.md). The live validator now checks manifest/OPML/source-table metadata, future-dated items, feed-specific stale-review deadlines, fuzzy duplicate candidates and compressed/wire telemetry. Remove a source only after a failed-feed, paywall, noise or duplication decision is recorded in the changelog.
