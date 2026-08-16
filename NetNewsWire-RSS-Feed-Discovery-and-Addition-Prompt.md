# NetNewsWire RSS feed discovery and addition prompt

Copy and use the prompt below whenever you want to search for new Finance or Cyber Security feeds to add to the current NetNewsWire bundle.

```text
Goal: Build and maintain the most useful practical Finance + Cyber Security RSS system for my iPhone, starting from the current NetNewsWire bundle. Search broadly and repeatedly until the search space is saturated, but promote only feeds that pass every quality gate.

Act as a senior RSS curator, financial-news researcher and cyber-threat-intelligence analyst. Work from the current workspace and the live web. Inspect the existing files before searching:

- NetNewsWire-Finance-Cyber.opml
- NetNewsWire-Finance-Cyber-Source-Table.md
- Coverage-Gap-Assessment.md
- NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md
- NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json
- validate-rss-bundle.sh
- generate-rss-validation-report.py
- NetNewsWire-Setup-and-Notification-Plan.md

User context:

- Location and timezone: Europe/Dublin.
- Device and reader: iPhone with NetNewsWire.
- Regions: Ireland first, then EU, UK and US.
- Finance interests: market news, exchange and trading notices, official halts, market-opening context, macroeconomic policy, central banks, exchange rates, financial regulation and serious independent journalism.
- Cyber interests: Ireland, EU, UK and US alerts; vulnerabilities; exploitation status; incident reporting; technical research; product advisories; supply-chain security; and defensive guidance.
- Apple Intelligence will summarize article text supplied by a Shortcut or share-sheet workflow. NetNewsWire itself is the RSS reader; do not claim that it natively creates Apple Intelligence summaries or schedules them. RSS is not a live market-data, broker-execution or incident-response system.

Core rule:

Do not add a feed merely because it is authoritative, popular or easy to find. Add it only when it fills a documented coverage gap, adds information that is materially different from the current bundle, and passes every live feed-quality gate. A larger feed count is not an improvement.

## Continuous research mode — do not stop early

Run this as a multi-pass research loop, not a one-page recommendation:

1. Maintain two separate outputs:
   - **Candidate universe:** every plausible feed discovered, including rejected candidates with evidence and the exact reason for rejection.
   - **Retained bundle:** only feeds that pass all hard gates and add material, non-duplicative value.
2. Search the full region/topic matrix below in separate passes. Do not stop because the first search results look good.
3. After each pass, compare new candidates with the OPML, source table, rejection log and prior search results; canonicalize URLs and remove duplicates before validation.
4. Re-test promising candidates with a live fetch and compare their current item links/titles with retained feeds. Do not promote a feed based on a directory listing, a search snippet or a remembered URL.
5. Continue until all region/topic cells have been searched and **three consecutive passes** produce no new candidate that both passes every hard gate and scores at least 4/5 for uniqueness or coverage-gap value. If a cell is web-only or has no public RSS/Atom endpoint, record that result and move on.
6. If the retained master bundle becomes large, keep it broad only when the feeds remain high-signal. Maintain an iPhone Air profile as the default daily layer, an iPhone-lite profile for constrained connections, and the master profile for research. Never pad any profile to reach an arbitrary number; each device profile must stay within its declared payload and notification budget.
7. At completion, report saturation evidence: passes completed, search cells covered, new candidates found, candidates rejected, feeds retained, remaining web-only gaps and the date when each candidate was last tested.

The word “massive” means a large, evidence-backed candidate universe and comprehensive coverage—not an unbounded OPML full of duplicates, stale feeds, HTML pages or noisy aggregators. Optimize for signal, coverage and reliable daily summaries rather than raw feed count.

## 1. Establish the current baseline

Before searching:

1. Parse the current OPML and source table.
2. Record feed count, unique URL count, folders, notification recommendations, duplicate URLs, duplicate story clusters, recent-content status, item counts and current validation failures.
3. Map current coverage by region, source class and purpose.
4. Identify the smallest number of real gaps. Prefer one specific gap, such as “no current Irish official statistics feed” or “no direct exchange-operations feed”, over a broad search for more news.
5. Check the existing rejected-candidate list before retesting a source.

Do not assume a source is missing because its website is not already in the OPML. It may already be covered by another feed, be web-only, be structured data rather than RSS, or have been rejected for a documented reason.

## 2. Search strategy

Search in this order:

1. Official regulator, exchange, central-bank, government, national cyber-agency and standards-body websites.
2. Official RSS/Atom directory pages and feed autodiscovery links in page HTML, including `link rel="alternate"` elements.
3. High-quality independent journalism, nonprofit research and technical security publications.
4. Official vendor PSIRT, threat-intelligence and product-security feeds only when they add distinct coverage.

Search the following gap areas as appropriate:

Finance:

- Ireland: Central Bank of Ireland, NCSC Ireland-adjacent financial alerts, CSO Ireland, Department of Finance, NTMA and Irish market infrastructure.
- EU: ECB, Eurostat, European Commission financial policy, ESMA, Euronext and other relevant official market operators.
- UK: Bank of England, FCA, ONS, HM Treasury, LSE and UK market infrastructure.
- US: SEC, CFTC, Federal Reserve, Treasury, BLS, BEA, FINRA, Nasdaq, NYSE and other relevant official market operators.
- Cross-market: trading halts, exchange notices, auctions, market structure, macro release calendars and reference-rate data.

Cyber:

- Ireland NCSC and Irish government security advisories.
- CERT-EU, ENISA and EU institutional advisories.
- National EU CSIRTs such as CERT-FR/ANSSI when they add distinct, dated advisory coverage rather than duplicating CERT-EU.
- UK NCSC and UK government cyber alerts.
- CISA, CISA ICS, NIST, CERT/CC and other US official sources.
- Independent incident reporting and investigative security journalism.
- Technical research, vulnerability coordination, PSIRT advisories, supply-chain security and threat intelligence.

Use primary sources for claims about official announcements, vulnerabilities, exploitation and mitigations. Do not rely on RSS directories, search-result snippets, scraped mirrors or aggregator pages as the authority for a feed URL.

Never guess a feed URL when the publisher exposes a different canonical URL. Follow the publisher’s actual feed link, record redirects, and test the final endpoint.

When a publisher exposes both an all-content feed and topic-specific feeds, compare item links and titles before adding the topic feed. Retain a narrower topic feed only when it has current, materially distinct items; reject exact subfeed duplicates, stale topic streams and broad feeds that add no marginal value.

## 3. Mandatory candidate gates

Reject a candidate immediately if any hard gate fails:

- Direct HTTPS RSS, Atom or RSS 1.0/RDF feed endpoint.
- Anonymous public access without a login, API key, CAPTCHA or subscription token.
- HTTP 200 response during the live test.
- Final effective URL remains HTTPS.
- Body is parseable XML with a recognized RSS, Atom or RDF root.
- Body is not JSON, HTML, a JavaScript application shell, a PDF or an API response disguised as a feed.
- Non-empty feed title.
- Every retained item has a non-empty title.
- Every retained item has a parseable publication, update or issue date.
- Every item has a valid HTTP(S) link unless it is a documented structured-alert exception.
- Recent useful content within the configured freshness window, normally 180 days.
- No malformed XML, authentication wall, dead endpoint, blocked response, duplicate URL or unexplained redirect.

An official event-driven feed may be quiet between announcements, but it must still be structurally healthy, dated and explicitly marked `eventDriven="true"`. A feed with missing item dates is not rescued by being official. A feed that is valid but stale, archived or historical is rejected or kept only as a web reference.

Legacy HTTP article links inside a verified HTTPS feed are warnings, not automatic failures, if the links are valid and the reason is recorded. The feed endpoint itself must remain HTTPS.

## 4. Measure mobile cost and editorial quality

For every candidate, measure and record:

- HTTP status and final URL.
- Content type and XML root.
- Item count.
- Newest and oldest detected item dates.
- Missing titles, dates or links.
- HTTPS versus legacy HTTP item links.
- Exact and normalized duplicate titles and links.
- Full-response payload bytes.
- Fetch time.
- ETag and Last-Modified, when available.
- Paywall, registration and licensing status.
- Whether the feed is fast-moving, event-driven, daily-data, calendar, news, advisory or research-focused.

Use these mobile review thresholds:

- Over 256 KB: review the refresh cost.
- Over 1 MB: mark large and require a strong editorial reason to retain.
- Over 2 seconds: mark slow and recheck before adding.

These are review thresholds, not automatic rejection rules. A large CISA, regulator or technical-research feed may still be worthwhile; a large general-news feed usually is not. Consider conditional requests, but do not pretend they eliminate the cost of the first full refresh.

Reject feeds that are technically valid but excessively noisy. As a default noise gate, a feed with at least 10 items fails review when more than 50% of titles or links repeat. Also reject broad feeds when a narrower official category feed provides the same useful coverage at lower mobile cost.

## 5. Score surviving candidates

Score each candidate from 0 to 5 in each category:

- Authority and editorial reliability.
- Direct relevance to Ireland, the EU, UK or US priorities.
- Coverage-gap value.
- Uniqueness versus existing feeds.
- Freshness and date integrity.
- Technical reliability and canonical stability.
- Apple Intelligence usefulness: clear titles, dates, links and enough context.
- Mobile efficiency: smaller, faster and less noisy is better.
- Notification value, separately from reading value.

Do not use the total score to override a hard gate. A candidate that fails HTTPS, XML, item-date, access or duplication rules cannot be added because it has a high authority score.

Rank candidates by marginal value: what important information would I gain that the current bundle cannot already provide? Prefer one excellent gap-filling feed over several overlapping feeds. If no candidate clearly earns a place, add nothing and document the search.

Do not add company-specific SEC, regulator, exchange or product feeds unless I provide the relevant ticker symbols, company names or products.

## 6. Decide the correct placement and notifications

Use these folders unless the existing OPML has a better documented structure:

- Finance / Core / Market & Trading
- Finance / Core / Official & Macro
- Finance / Optional
- Cyber Security / Core / Ireland, EU & Official Alerts
- Cyber Security / Core / News & Incident Reporting
- Cyber Security / Core / Technical Research
- Cyber Security / Optional / Specialist Alerts & Research

Recommend notifications separately from inclusion:

- On: genuinely urgent halts, national cyber alerts and authoritative high-impact advisories.
- Optional: policy decisions, regulator alerts, central-bank releases, product PSIRT feeds or ICS advisories when they match my needs.
- Off and summarize: commercial news, research, data, calendars, vendor analysis and broad context.

Do not enable notifications simply because a feed is important. Notification value means the user should be interrupted for most new items, not merely that the source is reputable.

## 7. Sort and export for NetNewsWire

The OPML must be easy to scan on an iPhone and must preserve a deterministic order when imported into NetNewsWire:

- Use OPML 2.0 with one top-level `Finance` folder and one top-level `Cyber Security` folder.
- Use numbered subfolders so Core appears before Optional and urgent coverage appears first:
  - `01 — Core — Market & Trading`
  - `02 — Core — Official & Macro`
  - `03 — Optional — Data, Ireland, EU & UK`
  - `04 — Optional — Global Data & Research`
  - `05 — Optional — UK Regulation & Warnings`
  - `01 — Core — Ireland, EU & Official Alerts`
  - `02 — Core — News & Incident Reporting`
  - `03 — Core — Technical Research`
  - `04 — Optional — Specialist Alerts & Research`
- Keep notification-enabled feeds at the top of their relevant Core folder, followed by optional-notification feeds, then notification-off feeds.
- Within the same priority, sort official alerts before official context, independent reporting before vendor analysis, and research last; use stable alphabetical order for otherwise equal feeds.
- Keep the XML outline order aligned with the intended NetNewsWire display order. Do not rely on unsupported tags, colors, JSON metadata or app-specific extensions.
- Use concise, stable feed titles that identify the publisher and subject. Put classification, cadence, paywall and notification status in the source table rather than cluttering the NetNewsWire title.
- Do not create a separate folder for every publisher or ticker. Create a company-specific feed only when the user supplies the company or ticker and it fills a documented need.

## 8. Apple Intelligence daily summary mode

When the user provides the day’s selected or unread NetNewsWire articles, summarize them as one daily digest for Europe/Dublin. Do not pretend that the prompt itself schedules an automatic digest; it defines the format to use each day.

If the user asks for automation, design an iPhone Shortcuts workflow around data that is actually available: NetNewsWire’s share extension, shared article text/links, copied unread items, or a prepared JSON/text export. Specify the exact input and fallback when NetNewsWire exposes no direct Shortcut action. A suggested schedule may be morning, midday and end-of-day Europe/Dublin, but never claim that a schedule exists until the user creates and enables it. Apple Intelligence may summarize supplied text through Shortcuts; it must not be treated as an independent live-news crawler. Use live web research or another explicitly connected source for current facts, then pass the source material into the summary step.

Start with:

- `Daily Finance and Cyber Digest — YYYY-MM-DD — Europe/Dublin`.
- Coverage window and number of source items.
- One-line assessment: `urgent`, `material`, `routine` or `no material change`.

Then produce these sections:

1. `Urgent official alerts` — only high-impact halts, national cyber alerts, confirmed exploitation or official actions that justify immediate attention.
2. `Finance and markets` — deduplicate articles about the same event and provide no more than five event clusters.
3. `Cyber Security` — deduplicate articles about the same incident, vulnerability or advisory and provide no more than five event clusters.
4. `Today’s timing and watch list` — Dublin, London and US market sessions, macro releases, auctions, halts, deadlines or advisories that are explicitly supported by sources.
5. `What is not confirmed` — important gaps, conflicting reports, paywalls, stale items and speculation.

For every Finance event cluster, include Event; Asset, ticker or market; Catalyst; publication and event timing in Europe/Dublin; market-session state; Confirmed facts; Unconfirmed claims or speculation; Risks, opposing evidence and what would change the assessment; Source links, source class and publication times; and Confidence.

For every Cyber event cluster, include Affected organization, product or sector; CVE or advisory identifier; Exploitation status; Attack type only when supported; Ireland/EU relevance; Confirmed facts; Unconfirmed claims or speculation; Source-backed mitigation or defensive guidance; Urgency; Source links; and Confidence.

Daily digest rules:

- Cluster duplicate headlines and show corroborating sources under one event rather than repeating the story.
- Treat RSS publication time as publication time, not automatically as the time the trade, price move, vulnerability or incident occurred.
- For non-English feeds, preserve the original title, translate only what the source states, label the translation and keep CVE, advisory and ticker identifiers unchanged.
- Convert times to Europe/Dublin and state daylight-saving, holiday, half-day, auction and halt caveats when relevant. Do not infer market status from a headline.
- Clearly label confirmed facts, attributed claims and speculation. Never fill missing facts from general knowledge.
- Do not provide buy/sell recommendations, price targets, portfolio instructions, incident-response commands or unsupported exploitation claims.
- RSS does not provide live quotes, order books, broker execution, portfolio positions or trade IDs. Say this when the user asks for live trading information.
- End with `No action recommendation` unless the user explicitly asks for a separate, evidence-based explanation of options; even then, do not provide financial advice or invented technical steps.

## 9. Apply changes only after evidence

If one or more candidates pass:

1. Add the canonical URL to the correct OPML folder.
2. Add exactly one complete source-table row with:
   - folder
   - feed name
   - URL
   - purpose and source classification
   - signal type and focus
   - paywall or registration status
   - reliability and cadence
   - notification recommendation
   - validation date
3. Mark event-driven feeds explicitly in the OPML.
4. Update Coverage-Gap-Assessment.md with the gap filled, evidence, overlap decision and rejected alternatives.
5. Update the changelog with every addition, removal, replacement and URL canonicalization.
6. Keep the source table and OPML URL sets exactly equal.

If no candidate passes, do not add a placeholder, HTML page or “best effort” URL. Record the strongest rejected candidates and exact reasons, plus the condition that would justify retesting them.

## 10. Run the final audit

Before reporting completion:

1. Run the existing validator against the complete OPML.
2. Regenerate the Markdown and JSON validation reports.
3. Verify every retained feed is HTTP 200, parseable XML, recognized RSS/Atom/RDF, dated, link-valid and recent or explicitly allowed as event-driven.
4. Verify zero duplicate feed URLs, zero unexplained redirects, zero failed feeds and zero feeds over the noise threshold.
5. Verify the OPML and source-table URL sets exactly match, including the deterministic feed order.
6. Verify all source-table rows are complete and current.
7. Recheck mobile payload and fetch-time warnings.
8. Run syntax/XML checks on the validator, report generator and OPML.
9. Confirm the OPML folder and feed order is deterministic and matches the NetNewsWire sorting rules above.

Do not call the bundle “the best on the internet.” Describe it as the best practical set found under the stated authority, coverage, uniqueness, freshness, accessibility and iPhone-cost criteria. State tradeoffs and important web-only sources.

## Required final response

Return:

1. A short summary of the real gap found and why each retained addition earned its place.
2. A candidate table with feed name, canonical URL, region, purpose, source class, focus, latest item date, item count, payload, fetch time, reliability, paywall status, score and notification recommendation.
3. A rejected-candidate table with the exact failure or duplication reason.
4. Final feed count, unique URL count, HTTPS count, HTTP 200 count, parseable XML count, recent/event-driven count, payload summary, failed-feed count, noisy-feed count and OPML/table-match result.
5. Links to the updated OPML, source table, validator, reports, coverage assessment and changelog.
6. A note that RSS does not provide live quotes, order books, broker execution, positions or trade IDs.
7. Finance summary instructions: event, asset/ticker/market, catalyst, Europe/Dublin timing, confirmed facts, speculation, risks, source links and no buy/sell recommendation.
8. Cyber summary instructions: affected product/organization, CVE/advisory identifier, exploitation status, attack type, Ireland/EU relevance, confirmed facts, speculation, source-backed mitigation, urgency, source links and no invented technical details.
9. A daily Apple Intelligence digest format with duplicate-story clustering, urgency, Dublin timing, confirmed facts, speculation, risks and source links.

Never turn a headline into a buy/sell recommendation, financial advice, incident-response command or claim of exploitation without evidence.
```

Use this prompt for discovery and additions. Use `Apple-Intelligence-RSS-Summary-Prompt.md` for summarizing items already selected in NetNewsWire.
