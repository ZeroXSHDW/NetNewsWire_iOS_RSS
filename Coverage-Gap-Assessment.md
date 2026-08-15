# RSS Coverage-Gap Assessment

Checked: 15 August 2026 (Europe/Dublin)

## Selection rule

The bundle is optimized for high-signal Finance and Cyber Security monitoring in Ireland, the EU, the UK and the US. A source is added only when it fills a real coverage gap, provides a direct HTTPS RSS/Atom/RSS 1.0 endpoint, and passes the live structural, date, title, link, duplication and noise checks. A larger feed count is not a success by itself.

Use [NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md](./NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md) for the repeatable search, scoring, mobile-cost review and final-audit workflow before proposing any new feed.

## Operational improvements now in place

- [feed-manifest.json](./feed-manifest.json) is the source of truth; [generate-bundle.py](./generate-bundle.py) regenerates the master and iPhone-lite OPML/source-table artifacts.
- The master bundle remains 51 feeds. A separate [30-feed iPhone-lite OPML](./NetNewsWire-Finance-Cyber-iPhone-Lite.opml) keeps official/core alerts, Ireland/EU/UK context and a compact research layer while leaving specialist feeds in the master profile.
- The validator now compares manifest, OPML and source-table metadata, measures decompressed body and compressed/wire bytes separately, detects conservative fuzzy duplicate stories and enforces feed-specific stale-review deadlines.
- Run `make test`, `make validate` and `make validate-lite`; the GitHub Actions workflow repeats these checks monthly or on demand.
- Use [NetNewsWire-Daily-Digest-Workflow.md](./NetNewsWire-Daily-Digest-Workflow.md) and `prepare-rss-digest-input.py` to remove already processed items before the Apple Intelligence daily digest.

## Change made in this cycle

### Added

- **CERT-FR — Security Alerts (French)** — `https://www.cert.ssi.gouv.fr/alerte/feed/`
  - Official French national CSIRT alert stream for urgent vulnerability and incident warnings, distinct from the CERT-FR advisory feed already retained.
  - Added to `Cyber / Core / Ireland, EU & Official Alerts` because the source defines alerts as warnings of immediate danger.
  - Live check: HTTP 200, RSS/XML, 40 dated items from 2 October 2023 to 22 July 2026, 26.1 KB payload, 0.13 s fetch and no exact or normalized title/link overlap with the current bundle.
  - Optional notification, French-language; use the daily Apple Intelligence digest if the original headlines are not convenient.

- **NCSC UK — News** — `https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml`
  - Official UK national cyber-news stream with current incidents, state-backed activity, vulnerability warnings and response guidance.
  - Added to `Cyber / Core / Ireland, EU & Official Alerts` beside the existing all-updates feed because 14 of its 20 current items are distinct from that feed.
  - Live check: HTTP 200, RSS/XML, 20 dated items from 2 March to 4 August 2026, 12.2 KB payload, 0.16 s fetch and no duplicate links outside the existing NCSC all-updates overlap.
  - Optional notification; notification-off remains appropriate if the existing UK all-updates stream is sufficient.

- **CERT-FR — Security Advisories (French)** — `https://www.cert.ssi.gouv.fr/feed/`
  - Official French national CSIRT feed with dated vulnerability advisories, CVE context and remediation signals.
  - Added to `Cyber / Optional / Specialist Alerts & Research` as an EU national-CSIRT layer distinct from CERT-EU, CISA and vendor research.
  - Live check: HTTP 200, RSS/XML, 40 dated items from 19 May to 14 August 2026, 23.1 KB payload, 0.14 s fetch and no exact or normalized title/link overlap with the current bundle.
  - Notification-off; it is optional, French-language advisory volume for daily Apple Intelligence summaries.

- **HM Treasury — News & Communications** — `https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=hm-treasury`
  - Official UK fiscal-policy and finance-ministry announcements, including budget timing, public spending, financial-services policy and economic news.
  - Added to `Finance / Core / Official & Macro` as the missing UK fiscal-policy layer alongside the Bank of England, FCA and ONS feeds.
  - Notification-off; summarize in the daily Apple Intelligence digest.

- **Nasdaq Trader — Equity Trader Alerts** — `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=2`
  - Official Nasdaq exchange-operations notices covering equity trading changes, listing/trader operations and market-structure implementation alerts.
  - Added to `Finance / Core / Market & Trading` as a distinct complement to the Trade Halts feed; notification-off because it is operational context rather than live market data.

- **European Commission — Sanctions Guidance** — `https://finance.ec.europa.eu/node/1296/rss_en`
  - Official EU financial-policy guidance covering sanctions, finance/banking and circumvention updates.
  - Added to `Finance / Optional / Data, Ireland, EU & UK`.
  - Notification-off; summarize in batches.
  - Marked `eventDriven="true"` in the OPML because official guidance can be quiet between releases. It must still have a detectable item date and pass every other validator check.
- **OpenSSF — Supply Chain Security** — `https://openssf.org/feed/`
  - Independent nonprofit Linux Foundation project covering open-source supply-chain security, CRA readiness and tooling.
  - Added to `Cyber / Optional / Specialist Alerts & Research`; notification-off and marked event-driven.
- **CrowdStrike — Cybersecurity Research** — `https://www.crowdstrike.com/en-us/blog/feed/`
  - Vendor threat-intelligence, vulnerability and incident analysis that adds a distinct research perspective to the existing Mandiant, Cisco and Microsoft coverage.
  - Added to `Cyber / Optional / Specialist Alerts & Research`; notification-off.

### Rechecked in this cycle

- **ESMA RSS** still returns HTTP 200 and valid RSS, but its current entries still have no detectable item dates; it remains rejected.
- **FINRA HTTPS endpoints** still fail at the TLS/transport layer; FINRA’s published endpoints remain HTTP-only and remain outside the bundle policy.
- **ENISA historical RSS paths** still return HTTP 404.
- **NYSE trading halts and Euronext Dublin notices** still have no verified direct public HTTPS RSS/Atom endpoint; their official web/CSV/portal references remain in the setup plan.
- **CSO Ireland release calendar** remains an official web calendar, but the tested RSS/Atom paths returned 404 and the calendar query returned HTML rather than a feed.
- **Ireland Department of Finance / gov.ie** remains useful official fiscal coverage, but the tested RSS paths were blocked with HTTP 403; no direct validated RSS/Atom endpoint was imported.
- **Euronext Press Releases** has a direct RSS endpoint, but the current ten-item response is an old 2021–2022 archive with no detectable item dates; it is not suitable as a current Euronext Dublin market-notice feed.
- **Nasdaq Current Headlines** is a valid direct XML feed but returned 679 mixed-category items and roughly 604 KB; the narrower Equity Trader Alerts feed was selected for mobile signal-to-cost reasons.
- **Europol RSS news** is reachable at `https://www.europol.europa.eu/cms/api/rss/news`, but its current ten items have no item-level publication dates; it remains rejected under the date-integrity rule.
- **CISA Known Exploited Vulnerabilities** remains structured JSON rather than RSS/Atom; it is better handled as a separate data monitor, not imported as a feed.
- **NCSC UK topic feeds** were rechecked: Threat Reports is stale, Guidance is lower-marginal-value context, and Blog Posts duplicates the retained all-updates feed. Only the current News feed earned a place.
- **CERT-FR specialist feeds** were rechecked: the SCADA feed overlaps the retained advisory feed, the CTI feed contains bilingual duplicate reports, IOCs are stale, and weekly bulletins add summary duplication; none was added.

## Coverage matrix

| Area | Current coverage | Remaining gap or decision |
|---|---|---|
| Ireland finance | Central Bank of Ireland news and markets updates, RTÉ Business | Good coverage; CSO release calendar and Department of Finance fiscal releases remain web-only because no verified direct RSS/Atom feed was retained. |
| Ireland cyber | Ireland NCSC alerts | Good official alert coverage; event-driven freshness is explicitly supported. |
| EU monetary/data | ECB press, operations, statistics and EUR/USD/EUR/GBP reference rates; Eurostat economy/finance releases | Strong coverage for the stated use case. |
| EU financial policy | European Commission sanctions guidance | Added as an optional, low-noise policy source; no notification. |
| EU securities regulation | ESMA was tested but not retained | Its direct RSS endpoint returned HTTP 200 and RSS, but current items had no detectable publication date, so it fails the date-integrity rule. |
| EU cyber | CERT-EU security advisories and threat intelligence, CERT-FR alerts and advisories | Strong operational coverage; ENISA’s historical RSS URLs currently return HTTP 404. CERT-FR is optional and French-language. |
| UK finance | HM Treasury, Bank of England news/publications, FCA news and warnings, ONS release calendar | Strong central-bank, fiscal-policy, regulator and macro-timing coverage. |
| UK cyber | NCSC UK News and all-updates feeds | Strong official current-incident and guidance coverage; stale reports and duplicate blog feeds were not added. |
| US finance | Nasdaq trade halts, SEC, CFTC and Federal Reserve | Strong official coverage; company-specific regulatory feeds remain intentionally excluded without user-provided tickers or names. BEA remains a useful web-only candidate because its RSS has one malformed historical item link. |
| US exchange alerts | Nasdaq Trade Halts and Nasdaq Equity Trader Alerts | The retained feeds cover live halt records and official equity-trading operations. NYSE provides a live web page and CSV/email or proprietary market-data services, but no verified direct public RSS/Atom endpoint was found. |
| US financial regulation | SEC and CFTC; FINRA candidate tested | FINRA’s published RSS endpoints are HTTP-only, and the HTTPS transport did not provide a reliable XML response, so they were rejected. |
| US cyber | CISA all advisories and ICS advisories, NIST, CERT/CC | Strong official and technical coverage. |
| Technical research | Mandiant, Microsoft, Cisco Talos, SANS, CERT/CC, OpenSSF, CrowdStrike and independent reporting | Stronger supply-chain and threat-intelligence coverage; both new specialist feeds remain optional and notification-off to limit duplication and alert fatigue. |

## Candidates rejected this cycle

| Candidate | Exact reason |
|---|---|
| ESMA RSS — `https://www.esma.europa.eu/rss.xml` | Valid direct RSS over HTTPS, but current item entries contain no detectable publication date. It cannot satisfy the freshness/date-integrity requirement. |
| FINRA News — `http://feeds.finra.org/FINRANews` and related feeds | Official RSS links are published as HTTP-only; the HTTPS endpoint did not provide a reliable parseable XML response. HTTP-only feeds are outside the bundle policy. |
| NYSE Trading Halts | Official current-halts page and CSV/email/proprietary data are available, but no verified direct public RSS/Atom feed was found. |
| Euronext Dublin notices | Official notices are available through Euronext web/portal services. The directly testable RSS endpoint found was for Euronext Athens, not Dublin, so it would be misleading to import it. |
| ENISA historical news and press-release RSS URLs | Both historical RSS URLs currently return HTTP 404. CERT-EU’s retained advisory and threat-intelligence feeds are the reliable current EU cyber channels. |
| BEA News Releases — `https://apps.bea.gov/rss/rss.xml` | Useful official US macro coverage, but one historical item has a schemeless `www.bea.gov/...` link. It fails the every-item-link integrity rule; tested alternate BEA paths either return the same feed, an HTML error page or 404, so it remains web-only. |
| NVD RSS candidate — `https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml` | Returns HTTP 404. NVD’s current official vulnerability feeds are JSON/XML data downloads rather than a validated RSS/Atom stream, so they belong in a separate structured-data monitor rather than this NetNewsWire bundle. |
| Google Project Zero — `https://projectzero.google/feed.xml` | The feed is parseable and high quality, but the current response is roughly 13 MB for only 10 entries. That mobile refresh cost is disproportionate for an optional research source; it remains a web reference unless a smaller stable feed appears. |
| CSO Ireland RSS candidates | The official release calendar is useful, but tested RSS/Atom paths returned 404 and the calendar query returned HTML, not XML. |
| gov.ie Department of Finance RSS candidates | Official fiscal pages are useful, but tested RSS paths returned HTTP 403 and no direct HTTPS RSS/Atom response was validated. |
| Euronext Press Releases — `https://www.euronext.com/en/press-releases/rss.xml` | Valid RSS transport, but the current ten-item response contains 2021–2022 releases and no detectable item dates; it is not a current Dublin market-notice stream. |
| Nasdaq Current Headlines — `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=0` | Valid XML, but 679 mixed-category items and roughly 604 KB per full response make it too broad for a focused iPhone bundle; a narrower Equity Trader Alerts feed was retained. |
| Nasdaq Equity Regulatory Updates — `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=6` | Valid but only one current item in the tested response; too sparse to add distinct value. |
| Nasdaq Equity Technical Updates — `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=7` | Valid but only three items, with older entries and overlap with trader-operations notices; not retained separately. |
| BLS Latest Numbers — `https://www.bls.gov/feed/bls_latest.rss` | Official BLS documentation identifies the feed, but the live endpoint returned HTTP 403 to the validator-compatible HTTPS fetch path; it cannot be imported until public access is reliable. |
| ENISA current-news candidates | The current ENISA site exposes current HTML publications and news but no discoverable direct RSS/Atom endpoint; historical RSS references are not substituted with HTML. |
| EBA press/news candidates | The current EBA press and news pages are HTML and no direct public RSS/Atom endpoint was exposed or validated; no guessed endpoint was imported. |
| NCSC UK Threat Reports — `https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml` | Valid RSS, but the newest item is 7 May 2025 and outside the 180-day freshness window. |
| NCSC UK Guidance — `https://www.ncsc.gov.uk/api/1/services/v1/guidance-rss-feed.xml` | Valid RSS, but it adds broad guidance rather than a material gap against the retained NCSC all-updates, NIST and official-advisory coverage; not retained. |
| NCSC UK Blog Posts — `https://www.ncsc.gov.uk/api/1/services/v1/blog-post-rss-feed.xml` | All 20 current links overlap the retained NCSC UK all-updates feed; rejected as duplicate coverage. |
| CERT-FR SCADA — `https://www.cert.ssi.gouv.fr/feed/scada/` | Valid and current, but overlaps the retained CERT-FR advisory feed and existing CISA ICS coverage; no distinct general-user value. |
| CERT-FR Threat & Incident Reports — `https://www.cert.ssi.gouv.fr/cti/feed/` | Valid and current, but the feed includes bilingual duplicate reports and overlaps existing CERT-EU/vendor threat research; not retained for iPhone signal-to-noise. |
| CERT-FR IOCs — `https://www.cert.ssi.gouv.fr/ioc/feed/` | Valid RSS, but newest item is July 2024 and stale under the 180-day rule. |
| CERT-FR weekly bulletins — `https://www.cert.ssi.gouv.fr/actualite/feed/` | Valid and current, but summary bulletins duplicate the advisory corpus; the narrower alert/advisory feeds provide better marginal value. |
| Europol RSS news — `https://www.europol.europa.eu/cms/api/rss/news` | HTTP 200 and valid RSS, but all ten current items lack item-level publication dates; it fails the date-integrity rule despite useful current descriptions. |
| CISA Known Exploited Vulnerabilities catalogue | The current official catalogue exposes structured JSON data rather than a direct RSS/Atom feed; it remains a separate data-monitoring candidate. |

## What would justify the next addition

Add a source only if one of these conditions changes:

- NYSE or Euronext Dublin publishes a stable public HTTPS RSS/Atom feed for market status, halts or notices.
- FINRA provides a stable HTTPS RSS endpoint.
- ESMA’s RSS items gain reliable publication dates.
- ENISA publishes current working RSS/Atom endpoints with useful, non-duplicative content.
- A new Irish, EU, UK or US source provides information not already covered by the current official feeds.
- A smaller direct Project Zero feed or a genuine NVD RSS/Atom stream becomes available without replacing a higher-signal source.
- CSO Ireland or the Department of Finance publishes a stable direct HTTPS RSS/Atom feed with dated release items.

## Ongoing quality controls

- Normal feeds must have recent, dated content within the configured 180-day window.
- Official/event-driven feeds may be quiet only when explicitly marked `eventDriven="true"` in the OPML and still have a detectable item date.
- Missing item titles, invalid item links, malformed XML, HTTP-only endpoints, duplicate URLs and noise remain hard failures.
- Item-link transport is measured separately: HTTPS links are preferred, legacy HTTP article links are warnings when the direct feed is a verified HTTPS RSS/XML source, and deliberately linkless structured alerts are recorded as explicit exceptions.
- Mobile refresh cost is advisory: bodies over 256 KB are flagged for review, bodies over 1 MB are marked large, and fetches over two seconds are flagged as slow; these do not automatically remove a high-signal feed.
- RSS does not provide live prices, order books, broker execution, portfolio positions or trade IDs.
