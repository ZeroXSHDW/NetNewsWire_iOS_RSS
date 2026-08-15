# NetNewsWire Finance + Cyber Validation Report — iphone-lite

Validation date: 15 August 2026 18:00 IST (Europe/Dublin)

Command:

```text
/Users/admin/Desktop/NetNewsWireSubscriptions/validate-rss-bundle.sh
```

## Results

| Check | Result |
|---|---:|
| Feed elements in OPML | 30 |
| Unique feed URLs | 30 |
| Duplicate URLs | 0 |
| HTTPS feed URLs | 30/30 |
| Effective URLs remain HTTPS | 30/30 |
| HTTP 200 responses | 24/30 |
| Conditional 304 responses reused from cache | 6 |
| Successful responses including cached 304s | 30/30 |
| Feed bodies verified as RSS/XML (not JSON) | 30/30 |
| MIME labels explicitly XML/RSS/Atom | 29/30 |
| MIME-labelled HTML but verified XML body | 1 |
| Feed payload measured | 30/30 |
| Total feed payload in this audit | 1.82 MB |
| Median feed payload | 12.7 KB |
| 95th-percentile feed payload | 304.1 KB |
| Compressed/wire bytes measured | 30/30 |
| Total measured wire bytes | 593.7 KB |
| 95th-percentile wire bytes | 119.3 KB |
| Feed parse time measured | 30/30 |
| Total feed parse time | 0.027 seconds |
| Slowest feed parse | 0.004 seconds |
| Feeds over mobile review threshold (256 KB) | 2 |
| Feeds over 1 MB | 0 |
| Fetches over 2 seconds | 0 |
| Slowest measured fetch | 1.20 seconds |
| Parseable XML documents | 30/30 |
| RSS/Atom/RSS 1.0 roots | 30/30 |
| Non-empty feed titles | 30/30 |
| Valid item URLs | 29/30 |
| Structured alert identity | 1/30 |
| Item titles with text | 853/853 |
| Feeds with all item titles valid | 30/30 |
| Item dates with valid timestamps | 853/853 |
| Feeds with all item dates valid | 30/30 |
| Feeds with all item URLs valid (exception-aware) | 30/30 |
| Item URLs with HTTP(S) links | 835/853 |
| Item URLs using HTTPS | 753/853 |
| Item URLs using legacy HTTP | 82 |
| Items without a per-item URL | 18 |
| Feeds with any legacy HTTP item links | 4 |
| Feeds with any missing item links | 1 |
| Recent content, default max age 180 days | 30/30 |
| Feeds marked event-driven in OPML | 17/30 |
| Stale feeds allowed by event-driven policy | 0 |
| Recent or allowed event-driven content | 30/30 |
| Oldest detected current item | 24.7 days |
| Cross-feed duplicate title clusters | 7 |
| Cross-feed duplicate link clusters | 6 |
| Fuzzy duplicate title clusters | 0 |
| Feeds over noise review threshold | 0 |
| OPML/source-table URL sets | Match |
| Manifest feeds | 30 |
| Manifest/OPML URL order | Match |
| Manifest/source-table URL order | Match |
| Source-table rows | 30/30 |
| Source-table rows with complete metadata | 30/30 |
| Metadata mismatches | 0 |
| Source-table duplicate URLs | 0 |
| Stale-review deadlines due | 0 |
| Future-dated items | 0 |
| Failed feeds | 0 |
| Cross-run drift baseline available | Yes |
| Cross-run drift warnings | 0 (0 critical) |

Duplicate-story clusters are reported for Apple Intelligence deduplication. A feed crosses the noise gate when it has at least 10 items and more than 50% repeated item titles or links.

Every retained item must have a non-empty title and a parseable publication/update date. Item-link transport is reported separately: direct feed endpoints must remain HTTPS, while legacy HTTP article links are warnings rather than hard failures when the feed itself is a verified HTTPS RSS/XML source. The Nasdaq Trade Halts feed is a deliberate structured-alert exception only for per-item URLs: its entries contain halt fields and titles but no per-item URLs.
Mobile refresh telemetry measures the full response body and compressed/wire transfer separately. Feed bodies over 256 KB are flagged for review, bodies over 1 MB are marked large, and fetches over 2 seconds are flagged as slow. The validator also reuses a local ETag/Last-Modified cache and reports conditional 304 responses; NetNewsWire refreshes can be smaller when servers honor validators.
Normal feeds must have a detectable item date within the configured age window. Event-driven feeds require a documented freshness reason and have a manifest-level stale-review deadline; they still must pass every other structural and integrity check.
The manifest is the source of truth for feed identity, folder, profile, freshness and notification policy. The validator compares it with both the OPML and the source table, including ordered metadata fields.

## Feed health

| Feed | HTTP | Cache | Root | Final HTTPS | Content type | Body | Wire | Encoding | Fetch s | Parse s | Freshness policy | Recent | Items | Missing titles | Missing dates | HTTPS item links | HTTP item links | Missing item links | Latest age | Duplicate titles | Duplicate links | Redirected | ETag / Last-Modified |
|---|---:|---|---|---|---|---:|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| NASDAQTrader.com | 200 | no | rss | yes | text/xml | 23.6 KB (small) | 3.4 KB | gzip | 0.45 | 0.001 | standard | yes | 18 | 0 | 0 | 0 | 0 | 18 | 1.5 | 0.0% | 0.0% | no | — / Sat, 15 Aug 2026 17 |
| NASDAQTrader.com | 200 | no | rss | yes | text/xml | 34.7 KB (small) | 4.7 KB | gzip | 0.46 | 0.001 | event-driven | yes | 40 | 0 | 0 | 0 | 40 | 0 | 4.8 | 0.0% | 0.0% | no | — / Sat, 15 Aug 2026 17 |
| BBC News | 200 | no | rss | yes | text/xml; charset=utf-8 | 37.9 KB (small) | 7.9 KB | gzip | 0.19 | 0.001 | standard | yes | 53 | 0 | 0 | 53 | 0 | 0 | 0.5 | 11.3% | 7.5% | no | — / — |
| Markets | 200 | no | rss | yes | text/xml; charset=utf-8 | 11.4 KB (small) | 3.7 KB | gzip | 0.31 | 0.001 | standard | yes | 25 | 0 | 0 | 25 | 0 | 0 | 0.3 | 0.0% | 0.0% | no | W/"2d88-/sW6Q8Fw/XndnYnBEB/GxwnUz4U" / — |
| Business | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 25.9 KB (small) | 6.2 KB | gzip | 0.19 | 0.001 | standard | yes | 40 | 0 | 0 | 40 | 0 | 0 | 0.7 | 0.0% | 0.0% | no | — / Sat, 15 Aug 2026 12 |
| News and Media | 200 | no | rss | yes | application/rss+xml | 143.8 KB (small) | 32.6 KB | gzip | 0.22 | 0.001 | event-driven | yes | 25 | 0 | 0 | 25 | 0 | 0 | 1.2 | 0.0% | 0.0% | no | — / — |
| ECB - European Central Bank | 200 | no | rss | yes | text/xml | 5.8 KB (small) | 1.5 KB | gzip | 0.25 | 0.000 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 2.3 | 0.0% | 0.0% | no | — / Fri, 14 Aug 2026 12 |
| News | 200 | no | rss | yes | text/xml; charset=utf-8 | 24.5 KB (small) | 6.5 KB | gzip | 0.25 | 0.001 | event-driven | yes | 50 | 0 | 0 | 50 | 0 | 0 | 4.2 | 0.0% | 0.0% | no | — / — |
| News and communications from HM Treasury (HMT) | 304 | yes | feed | yes | application/atom+xml; charset=utf-8 | 12.6 KB (small) | 0.0 KB | identity | 1.20 | 0.001 | event-driven | yes | 20 | 0 | 0 | 20 | 0 | 0 | 8.4 | 0.0% | 0.0% | no | W/"7913ee7c3ce8674aaf03d62f49ba9432" / — |
| FRB: Press Release - Monetary Policy | 200 | no | rss | yes | text/xml | 9.4 KB (small) | 0.9 KB | gzip | 0.15 | 0.000 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 17.0 | 26.7% | 0.0% | no | W/"e950b61b841fdd1 / Wed, 29 Jul 2026 18 |
| Press Releases | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 17.7 KB (small) | 5.0 KB | gzip | 0.32 | 0.001 | event-driven | yes | 25 | 0 | 0 | 25 | 0 | 0 | 0.9 | 0.0% | 0.0% | no | "1786813073" / Sat, 15 Aug 2026 16 |
| Press Releases | 304 | yes | rss | yes | application/rss+xml; charset=utf-8 | 4.6 KB (small) | 0.0 KB | gzip | 0.20 | 0.000 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 2.1 | 0.0% | 0.0% | no | "1786769334" / Sat, 15 Aug 2026 04 |
| ECB - Monetary policy tender operations and ad-hoc communications | 200 | no | rss | yes | application/rss+xml | 11.4 KB (small) | 1.1 KB | gzip | 0.21 | 0.001 | event-driven | yes | 32 | 0 | 0 | 0 | 32 | 0 | 3.3 | 0.0% | 0.0% | no | "myra-4118cf2f" / — |
| FRB: Speeches | 200 | no | rss | yes | text/xml | 9.5 KB (small) | 1.7 KB | gzip | 0.23 | 0.000 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 9.9 | 0.0% | 0.0% | no | W/"db4d36b91525dd1 / Wed, 05 Aug 2026 20 |
| ECB \| US dollar (USD) - Euro foreign exchange reference rates | 200 | no | rdf:RDF | yes | application/rss+xml | 7.1 KB (small) | 1.2 KB | gzip | 0.20 | 0.000 | standard | yes | 5 | 0 | 0 | 0 | 5 | 0 | 1.2 | 0.0% | 0.0% | no | "myra-9a2dd5ff" / — |
| ECB \| Pound sterling (GBP) - Euro foreign exchange reference rates | 200 | no | rdf:RDF | yes | application/rss+xml | 7.2 KB (small) | 1.2 KB | gzip | 0.22 | 0.000 | standard | yes | 5 | 0 | 0 | 0 | 5 | 0 | 1.2 | 0.0% | 0.0% | no | "myra-66fdbcad" / — |
| ONS Release Calendar RSS Feed. | 200 | no | rss | yes | application/rss+xml | 5.7 KB (small) | 1.5 KB | gzip | 0.20 | 0.000 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 1.4 | 0.0% | 0.0% | no | — / Sat, 15 Aug 2026 17 |
| NCSC Alerts & Advisories | 200 | no | rss | yes | application/rss+xml | 119.3 KB (small) | 119.3 KB | identity | 0.29 | 0.004 | event-driven | yes | 225 | 0 | 0 | 225 | 0 | 0 | 24.7 | 1.8% | 1.8% | no | "6a7f18bb-1dd23" / Fri, 14 Aug 2026 13 |
| All CISA Advisories | 200 | no | rss | yes | application/rss+xml; charset=utf-8 | 496.4 KB (review) | 59.5 KB | gzip | 0.28 | 0.004 | event-driven | yes | 30 | 0 | 0 | 30 | 0 | 0 | 2.2 | 16.7% | 0.0% | no | — / — |
| Latest publications of type Security Advisories | 200 | no | rss | yes | text/xml; charset=utf-8 | 9.1 KB (small) | 9.1 KB | identity | 0.36 | 0.000 | event-driven | yes | 10 | 0 | 0 | 10 | 0 | 0 | 23.3 | 0.0% | 0.0% | no | — / — |
| CERT-FR | 200 | no | rss | yes | application/xml | 25.5 KB (small) | 25.5 KB | identity | 0.13 | 0.001 | event-driven | yes | 40 | 0 | 0 | 40 | 0 | 0 | 24.7 | 0.0% | 0.0% | no | "0be3967825899f6c231265373e818eda" / Fri, 14 Aug 2026 13 |
| News Feed | 304 | yes | rss | yes | application/rss+xml; charset=utf-8 | 11.9 KB (small) | 0.0 KB | gzip | 0.15 | 0.001 | standard | yes | 20 | 0 | 0 | 20 | 0 | 0 | 11.2 | 0.0% | 0.0% | no | "1786716944" / Fri, 14 Aug 2026 14 |
| All Feed | 304 | yes | rss | yes | application/rss+xml; charset=utf-8 | 11.2 KB (small) | 0.0 KB | gzip | 0.14 | 0.001 | event-driven | yes | 20 | 0 | 0 | 20 | 0 | 0 | 2.2 | 0.0% | 0.0% | no | "1786716704" / Fri, 14 Aug 2026 14 |
| BleepingComputer | 304 | yes | rss | yes | text/xml; charset=utf-8 | 12.7 KB (small) | 0.0 KB | gzip | 0.13 | 0.000 | standard | yes | 15 | 0 | 0 | 15 | 0 | 0 | 0.1 | 0.0% | 0.0% | no | 77a638ee048e19599390b445a334f411 / Sat, 15 Aug 2026 16 |
| Krebs on Security | 200 | no | rss | yes | text/html; charset=UTF-8 | 123.0 KB (small) | 36.5 KB | gzip | 0.17 | 0.001 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 1.2 | 0.0% | 0.0% | no | — / Sat, 15 Aug 2026 16 |
| The Record from Recorded Future News | 200 | no | rss | yes | text/xml | 5.2 KB (small) | 1.6 KB | gzip | 0.23 | 0.000 | standard | yes | 5 | 0 | 0 | 5 | 0 | 0 | 0.9 | 0.0% | 0.0% | no | — / — |
| SANS Internet Storm Center, InfoCON: green | 200 | no | rss | yes | text/xml; charset=utf-8 | 149.7 KB (small) | 19.6 KB | gzip | 0.91 | 0.001 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 1.6 | 0.0% | 0.0% | no | W/"256df-65918dadef28a" / Sat, 15 Aug 2026 16 |
| CERT Recently Published Vulnerability Notes | 200 | no | feed | yes | application/atom+xml; charset=utf-8 | 164.9 KB (small) | 164.9 KB | identity | 0.23 | 0.001 | event-driven | yes | 15 | 0 | 0 | 15 | 0 | 0 | 4.1 | 0.0% | 0.0% | no | — / Fri, 14 Aug 2026 14 |
| Cybersecurity Insights | 304 | yes | rss | yes | application/rss+xml; charset=utf-8 | 42.3 KB (small) | 0.0 KB | gzip | 0.49 | 0.001 | event-driven | yes | 40 | 0 | 0 | 40 | 0 | 0 | 3.2 | 20.0% | 0.0% | no | "1786784497-gzip" / Sat, 15 Aug 2026 09 |
| Microsoft Security Blog | 200 | no | rss | yes | application/rss+xml; charset=UTF-8 | 304.1 KB (review) | 78.9 KB | gzip | 0.38 | 0.001 | standard | yes | 10 | 0 | 0 | 10 | 0 | 0 | 5.0 | 0.0% | 0.0% | no | "c8f0c308c3fb485beed7fba1ccf23b95-gzip" / Fri, 14 Aug 2026 15 |

## Cross-run drift review

No feed identity, freshness, payload, item-count, link-transport or noise-threshold drift was detected against the previous snapshot.

## Duplicate-story clusters detected

These are candidates for one Apple Intelligence summary with multiple corroborating sources:
- **Alert: NCSC issues advice following global targeting of Fortinet firewalls and VPN gateways** — 2 feeds; exact match: All Feed, News Feed
- **ECB reveals shortlisted designs for new banknotes and launches public survey** — 2 feeds; exact match: ECB - European Central Bank, News and Media
- **NCSC CEO: Hostile states linked to three-quarters of cyber attacks affecting UK's critical systems** — 2 feeds; exact match: All Feed, News Feed
- **NCSC statement in response to recent incidents resulting from frontier AI evaluations** — 2 feeds; exact match: All Feed, News Feed
- **The AI shift in cyber risk: why leaders must act now** — 2 feeds; exact match: All Feed, News Feed
- **UK and Allies urge critical sectors to improve defences against Russian intelligence targeting** — 2 feeds; exact match: All Feed, News Feed
- **UK and partners expose Russian state-supported actors for new ‘zero-click’ phishing campaign targeting Western organisations** — 2 feeds; exact match: All Feed, News Feed

## Duplicate-link clusters detected

- `https://www.ncsc.gov.uk/news/advice-following-global-targeting-of-fortinet-firewalls-and-vpn-gateways` — 2 feeds: https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml, https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml
- `https://www.ncsc.gov.uk/news/ncsc-ceo-hostile-states-linked-to-three-quarters-of-cyber-attacks` — 2 feeds: https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml, https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml
- `https://www.ncsc.gov.uk/news/ncsc-statement-in-response-to-recent-incidents-resulting-from-frontier-ai-evaluations` — 2 feeds: https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml, https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml
- `https://www.ncsc.gov.uk/news/the-ai-shift-in-cyber-risk-why-leaders-must-act-now` — 2 feeds: https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml, https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml
- `https://www.ncsc.gov.uk/news/uk-and-allies-urge-critical-sectors-to-improve-defences-against-russian-intelligence-targeting` — 2 feeds: https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml, https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml
- `https://www.ncsc.gov.uk/news/uk-and-partners-expose-russian-state-supported-actors-for-new-zero-click-phishing-campaign` — 2 feeds: https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml, https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml

## Item-link transport warnings

These warnings do not fail the bundle because the direct feed endpoints are HTTPS and the links are still valid HTTP(S) URLs; review them if a source changes its link policy.
- **NASDAQTrader.com** — legacy HTTP item links: 0; missing per-item URLs: 18.
- **NASDAQTrader.com** — legacy HTTP item links: 40; missing per-item URLs: 0.
- **ECB - Monetary policy tender operations and ad-hoc communications** — legacy HTTP item links: 32; missing per-item URLs: 0.
- **ECB \| US dollar (USD) - Euro foreign exchange reference rates** — legacy HTTP item links: 5; missing per-item URLs: 0.
- **ECB \| Pound sterling (GBP) - Euro foreign exchange reference rates** — legacy HTTP item links: 5; missing per-item URLs: 0.

## Mobile refresh review

These feeds exceed the advisory mobile threshold of 256 KB or took more than 2 seconds in this full-response audit. They are not failures; review them if refresh cost becomes noticeable on iPhone.
- **All CISA Advisories** — body 496.4 KB; wire 59.5 KB; encoding `gzip`; fetch 0.28s; class `review`; cached 304 `False`.
- **Microsoft Security Blog** — body 304.1 KB; wire 78.9 KB; encoding `gzip`; fetch 0.38s; class `review`; cached 304 `False`.

## Coverage audit

- **Finance**: US, UK, Irish, euro-area and global market context; SEC, CFTC, Federal Reserve speeches and monetary policy, ECB press, market operations and statistical releases, Central Bank of Ireland, Bank of England, HM Treasury, FCA, Eurostat, ONS, BIS and European Commission sanctions guidance; Nasdaq trade halts and Equity Trader Alerts; EUR/USD and EUR/GBP reference data. BEA was tested but rejected for one malformed historical item link.
- **Cyber**: Ireland NCSC, CISA, CISA ICS, CERT-EU, UK NCSC, CERT/CC, NIST, Microsoft, Mandiant, Cisco PSIRT, Cisco Talos, OpenSSF and CrowdStrike, plus independent incident reporting and technical research.
- **Ireland/EU/UK/US scope**: present in official alerts, regulation, macro data and market coverage.
- **Coverage-gap decisions**: see [Coverage-Gap-Assessment.md](Coverage-Gap-Assessment.md) for tested candidates, exact rejection reasons and next-addition triggers.

## Notification recommendation

**On:** Nasdaq Trade Halts, Ireland NCSC Alerts, CISA All Advisories and CERT-EU Security Advisories.

**Optional:** Central Bank of Ireland News, Federal Reserve Monetary Policy, ECB Press, Bank of England News, UK NCSC All Updates, CISA ICS Advisories and Cisco PSIRT.

**Off and summarize in batches:** commercial market news, RTÉ/BBC business news, CFTC regulatory releases, ECB market operations and statistical releases, Eurostat/ONS/BIS data, European Commission sanctions guidance, Federal Reserve speeches, Bank of England Publications, CERT/CC vulnerability notes, incident reporting, research feeds, exchange-rate data and broad regulatory context.

## Strong candidates retained outside the OPML

- **BIS Data Portal `https://data.bis.org/feed.xml`**: valid HTTPS RSS, but the current release-calendar feed contains many repeated dataset items and links; the lower-noise BIS Statistical Releases feed is retained instead.
- **CSO Ireland release calendar**: valuable official web calendar, but no verified direct RSS/Atom endpoint was retained in this pass.
- **Ireland Department of Finance / gov.ie**: valuable official fiscal and budget coverage, but tested RSS paths were blocked or unavailable; no direct validated RSS/Atom endpoint was retained.
- **Euronext Dublin notices**: official notices are available through Euronext web/portal services, but no verified direct public RSS/Atom feed was retained.
- **UK NCSC Reports feed**: valid, but it overlaps the retained UK NCSC All Updates feed; adding both would duplicate stories.
- **CISA Known Exploited Vulnerabilities catalogue**: useful for a separate structured-data monitor, but not a direct RSS/Atom feed.
- **U.S. Treasury press releases**: valuable official fiscal and macro context, but no verified direct HTTPS RSS/Atom endpoint was retained.
- **Apple security releases**: valuable for iPhone security, but the official page is HTML rather than a direct RSS/Atom feed.
- **Federal Reserve H.10 XML feed**: reachable and current, but rejected because its 92-entry stream had 40.2% repeated titles and 100% repeated item links; its HTML page was not used either.
- **BLS Latest Numbers `https://www.bls.gov/feed/bls_latest.rss`**: authoritative US macro feed, but the current endpoint returned HTTP 403 and was not imported.
- **ECB Yield Curve `https://www.ecb.europa.eu/rss/yc.html`**: valid RSS, but the newest actual data item is from 2017 and therefore fails the recent-content rule.
- **ESMA `https://www.esma.europa.eu/rss.xml`**: direct HTTPS RSS and useful EU market-regulator coverage, but its current items contain no detectable publication date; it fails the date-integrity requirement and remains a web reference.
- **BEA News Releases `https://apps.bea.gov/rss/rss.xml`**: useful official US macro coverage, but one historical item contains a schemeless `www.bea.gov/...` link; alternate BEA paths did not provide a clean RSS feed, so it was not imported.
- **FINRA RSS feeds**: FINRA documents official feeds, but the published endpoints are HTTP-only and the HTTPS transport did not provide a reliable XML response; none were imported.
- **NYSE trading halts**: NYSE provides a live web page and CSV/email or proprietary market-data services, not a verified direct public RSS/Atom feed; it remains a web reference.
- **Euronext Dublin market notices**: Euronext’s public notices are available through web/portal services; the directly testable RSS endpoint found was for Euronext Athens, not Dublin, so it was not imported.
- **Euronext Press Releases `https://www.euronext.com/en/press-releases/rss.xml`**: valid RSS transport, but the current ten-item response contains 2021–2022 releases and no detectable item dates; it is not a current Dublin market-notice stream.
- **Nasdaq Current Headlines `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=0`**: valid XML, but 679 mixed-category items and roughly 604 KB per full response made it too broad for a focused iPhone bundle; the narrower Equity Trader Alerts stream was retained.
- **Nasdaq Equity Regulatory/Technical Updates**: valid but too sparse in the tested responses to add distinct value beyond the retained Equity Trader Alerts stream and Trade Halts feed.
- **ENISA legacy RSS URLs**: the historical news and press-release RSS endpoints returned HTTP 404; current CERT-EU feeds cover the operational advisory and threat-intelligence gap instead.
- **NVD RSS candidate `https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml`**: HTTP 404; current official NVD feeds are structured JSON/XML rather than RSS/Atom.
- **Google Project Zero `https://projectzero.google/feed.xml`**: parseable and high quality, but roughly 13 MB for 10 entries in the current response; excluded for mobile refresh cost.

## Apple Intelligence guardrails

Use the [Apple Intelligence RSS summary prompt](Apple-Intelligence-RSS-Summary-Prompt.md), [NetNewsWire setup plan](NetNewsWire-Setup-and-Notification-Plan.md) and [market-hours reference](Market-Hours-and-Holiday-Reference.md) for deduplication, confidence labels, Dublin-time conversion, exchange-session state and notification control.

Finance summaries must identify the event, asset/ticker, catalyst, Dublin timing, confirmed facts, speculation, risks and sources, without a buy/sell recommendation.

Cyber summaries must identify the affected product or organization, CVE/advisory, exploitation status, attack type, Ireland/EU relevance, mitigation, urgency and sources, without inventing technical details or claiming exploitation without evidence.

RSS is not live market data: it does not provide live quotes, order books, broker execution, portfolio positions or trade IDs.

## Machine-readable report

Full per-feed JSON: [NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.json](NetNewsWire-Finance-Cyber-iPhone-Lite-VALIDATION-REPORT.json)
