# NetNewsWire setup and notification plan

## Import

Import [NetNewsWire-Finance-Cyber-iPhone-Air.opml](./NetNewsWire-Finance-Cyber-iPhone-Air.opml) as the recommended daily setup, [NetNewsWire-Finance-Cyber-iPhone-Lite.opml](./NetNewsWire-Finance-Cyber-iPhone-Lite.opml) when refresh cost matters most, or [NetNewsWire-Finance-Cyber.opml](./NetNewsWire-Finance-Cyber.opml) for the complete 62-feed master bundle. The OPML supplies the folders and feed URLs; notification preferences are best reviewed manually after import.
Import exactly one profile into the target NetNewsWire account. The import is additive: if an older copy of this bundle is already present, remove or separate it first so the feeds are not duplicated.
For today’s iPhone import, save the chosen `.opml` file in Files or iCloud Drive, open NetNewsWire’s Feeds screen, tap **Settings → Import Subscriptions**, choose the file and select the intended account if NetNewsWire asks. Confirm that the expected folders and feed counts appear before applying notifications.
Review [Coverage-Gap-Assessment.md](./Coverage-Gap-Assessment.md) for the source-selection decisions behind the bundle.
Use the [RSS feed discovery and addition prompt](./NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md) when searching for new candidates; it defines the evidence, mobile-cost and rejection gates before any feed is added.
Use the [feature and automation matrix](./NetNewsWire-Feature-and-Automation-Matrix.md) for the complete iPhone capability checklist and Shortcut design.
The [feed manifest](./feed-manifest.json) is the source of truth. Run `make generate` after changing it rather than editing generated OPML or source-table rows by hand.
Use the generated [notification/profile matrix](./NetNewsWire-Notification-Profile.md) as the post-import per-feed checklist; the machine-readable version is [NetNewsWire-Notification-Profile.json](./NetNewsWire-Notification-Profile.json).

## iPhone refresh profile

The latest live full-response baseline measured about 5.79 MB of decompressed feed bodies and 1.71 MB of compressed/wire bytes across 62 feeds; five feeds were flagged for mobile body review, with one over 1 MB and no fetches over two seconds. The iPhone-lite bundle contains 39 feeds and measured about 2.30 MB of bodies, 910 KB of wire bytes and two advisory review entries. The iPhone Air bundle contains 50 feeds and measured about 2.70 MB of bodies, 1.13 MB of wire bytes and two advisory body-size review entries, with no slow-fetch observations in the final run. No phone-profile feed exceeded 1 MB or the declared 600 KB per-feed budget. NetNewsWire and the validator can use conditional requests, so actual repeat-refresh traffic can be lower.

For the best everyday balance on iPhone Air, use the Air OPML, leave Optional folders notification-off and summarize them in batches. The Air profile is explicitly capped at 50 feeds, 4 MB of full response bodies, 600 KB per feed and six mobile-review feeds; the current validator fails the profile if those limits are exceeded. Use Lite for constrained connections. The master bundle retains industrial-control and specialist research feeds for later use.

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
- AMLA — News & Press
- European Banking Authority — News
- European Systemic Risk Board — Press
- NCSC UK — News
- NCSC UK — All Updates
- CERT-FR — Security Alerts (French), if French-language headlines are useful
- CISA — ICS Advisories, if industrial systems matter to you
- Cisco PSIRT, if you use Cisco products
- SANS Internet Storm Center, if security research/alerts are useful
- AWS Security Bulletins, if your work includes AWS services or dependencies

Keep Nasdaq Trader — Equity Trader Alerts, HM Treasury — News & Communications, FCA — Scam Warnings, OFSI — Financial Sanctions Blog, CFTC — Enforcement, CyberScoop, Unit 42 — Threat Research, AWS Security Bulletins, European Banking Authority — News, European Systemic Risk Board — Press, AMLA — News & Press, CERT-FR — Security Advisories (French), all commercial news, research, ECB operations/statistics, European Commission sanctions guidance, CERT/CC vulnerability-note, exchange-rate, macro-data, release-calendar and speech feeds notification-off. Review them in one daily Apple Intelligence digest instead of receiving an alert for every article.

## Apple Intelligence workflow

1. Read urgent notifications directly from the official source.
2. On iPhone, open **Today** or **All Unread** in NetNewsWire, select the relevant articles and share them to the `Daily Finance + Cyber Digest` Shortcut. This is the direct phone path; NetNewsWire does not provide a documented bulk “export all unread to Shortcuts” action.
3. For a prepared or Mac-based batch, create `selected-articles.json` from an external/exported source, then run `python3 prepare-rss-digest-input.py --input selected-articles.json --output digest-input.json --shortcut-output shortcut-digest.txt --profile iphone-air --state .digest-state.json`.
4. Pass `shortcut-digest.txt` directly to the Shortcut, or use `digest-input.json` as the prepared input, together with [Apple-Intelligence-RSS-Summary-Prompt.md](./Apple-Intelligence-RSS-Summary-Prompt.md).
5. Ask for one daily digest, with duplicate events clustered and corroborating sources grouped underneath.
6. Treat a headline as a lead until an official source confirms it.

The Air command filters recognized exports to the 50-feed Air profile and applies a 30-item, 6,000-character-per-item and 90,000-character total digest budget. Lite has a smaller 24-item/5,000-per-item/75,000-total budget. The [daily workflow](./NetNewsWire-Daily-Digest-Workflow.md) documents the JSON format, plain-text Shortcut handoff and state behavior. It is a summary format, not a live-price service or an automatic schedule.

## iPhone feature checklist

- Import the iPhone Air OPML through NetNewsWire’s **Import Subscriptions** action, keep Lite as the travel/constrained-connection fallback, and keep the master OPML as the full-coverage backup.
- Enable iOS **Background App Refresh** for NetNewsWire; use **Today**, **All Unread** and **Starred** as the daily triage views.
- Enable notifications only for urgent feeds. NetNewsWire’s notification setting is per feed, so alerts remain separate from reading coverage.
- Use Reader View, search, starring and the Share Sheet for article review. Share selected articles to the digest Shortcut rather than trying to summarize every item.
- Create one Shortcut named `Daily Finance + Cyber Digest`, enable **Show in Share Sheet**, and use this action order: receive text/URL/article input → stop with an alert if empty → add the supplied digest text and fixed prompt → **Use Model** → show the result → save it to a dated Apple Note.
- In **Use Model**, choose **On-Device** for a short batch, **Private Cloud Compute** for a larger supplied batch when available, or **Extension Model** (ChatGPT) only when you deliberately choose it. Keep the source links in the input and output.
- Turn on Apple Intelligence and update iOS before building the Shortcut. If **Use Model** is missing, check device, language and region availability before troubleshooting the feed bundle.
- Create three optional time-of-day personal automations at 07:30, 12:30 and 17:30 Europe/Dublin only if a prepared input source will exist at those times. A time trigger alone cannot extract NetNewsWire’s unread database.
- NetNewsWire’s documented iOS integration provides OPML, background refresh, notifications and sharing, but not a direct “export all unread items to Shortcuts” action. For unattended summaries, use a prepared JSON/text input or a separate feed-fetching service; for the privacy-first workflow, use the Share Sheet with selected articles.

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

Run `make test`, `make validate`, `make validate-lite` and `make validate-air` monthly. Review the generated [master Markdown report](./NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md), [iPhone Air report](./NetNewsWire-Finance-Cyber-iPhone-Air-VALIDATION-REPORT.md), [iPhone-lite report](./NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.md) and [coverage-gap assessment](./Coverage-Gap-Assessment.md). The live validator now checks manifest/OPML/source-table metadata, future-dated items, feed-specific stale-review deadlines, fuzzy duplicate candidates, compressed/wire telemetry and device budgets. Remove a source only after a failed-feed, paywall, noise or duplication decision is recorded in the changelog.
