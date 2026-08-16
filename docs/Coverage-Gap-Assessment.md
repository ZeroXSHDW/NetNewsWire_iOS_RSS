# RSS Coverage-Gap Assessment

Checked: 16 August 2026 (Europe/Dublin)

## Selection rule

The bundle is optimized for high-signal Finance and Cyber Security monitoring in Ireland, the EU, the UK and the US. A source is added only when it fills a real coverage gap, provides a direct HTTPS RSS/Atom/RSS 1.0 endpoint, and passes the live structural, date, title, link, duplication and noise checks. A larger feed count is not a success by itself.

Use [NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md](./NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md) for the repeatable search, scoring, mobile-cost review and final-audit workflow before proposing any new feed.

## Operational improvements now in place

- [feed-manifest.json](../feed-manifest.json) is the source of truth; [generate-bundle.py](../generate-bundle.py) regenerates every manifest-defined OPML/source-table artifact.
- The master bundle now contains 62 feeds. The recommended [50-feed iPhone Air OPML](../artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Air.opml) adds compact market, data, conduct and supply-chain context to the [39-feed iPhone-lite OPML](../artifacts/opml/NetNewsWire-Finance-Cyber-iPhone-Lite.opml); archive-heavy specialist feeds remain in the master profile.
- The validator now compares manifest, OPML and source-table metadata, measures decompressed body and compressed/wire bytes separately, detects conservative fuzzy duplicate stories and enforces feed-specific stale-review deadlines.
- Run `make test`, `make validate` and `make validate-lite`; the GitHub Actions workflow repeats these checks monthly or on demand.
- Use [NetNewsWire-Daily-Digest-Workflow.md](./NetNewsWire-Daily-Digest-Workflow.md) and `prepare-rss-digest-input.py` to remove already processed items before the Apple Intelligence daily digest.

## This research pass — FCA Warning List coverage

### Added

- **FCA — Scam Warnings** — `https://www.fca.org.uk/news/warnings/rss.xml`
  - Official FCA Warning List stream for unauthorised firms, clone firms and investment-scam warnings.
  - Added beside the existing general FCA news feed because the current 20 warning items had zero exact title/link overlap with that stream.
  - Live candidate check: HTTP 200, RSS/XML, 20 dated items through 14 August 2026, 60.1 KB body, 5.4 KB wire response, 0.12 s fetch, and no noise or item-integrity failures.
  - Included in iPhone-lite with notifications off; warnings are high-signal but frequent enough that they belong in the digest rather than immediate alerts.

### Rechecked and not added

- **BLS — Latest Numbers** remains a useful official US macro candidate and its documented feed URL is current, but access was intermittent: the direct Python fetch returned RSS/XML while the bundle’s reproducible curl validator received HTTP 403. It remains outside the bundle until the endpoint is stable under the same fetch path used by validation.
- **ESMA RSS**, **ENISA RSS**, **CSO Ireland RSS**, **Euronext press RSS** and **US Treasury RSS** still did not produce a stronger validator-compatible feed: ESMA lacks item dates, ENISA/CSO/Treasury candidates returned 404, and Euronext’s feed remains an undated 2021–2022 archive.

## This research pass — threat research and cloud-bulletin coverage

### Added

- **Unit 42 — Threat Research** — `https://unit42.paloaltonetworks.com/feed/atom/`
  - Official Palo Alto Networks research covering malware, vulnerabilities, cloud, identity and incident analysis.
  - Added to `Cyber / Core / Technical Research` and the iPhone-lite profile because it is a compact, current threat-intelligence source distinct from Mandiant, Microsoft and Cisco Talos.
  - Live candidate check: HTTP 200, Atom/XML, 15 dated items through 11 August 2026, 24.2 KB payload, 1.70 s fetch and no exact or fuzzy title/link overlap in the comparison window.
  - Notification-off; summarize with the technical-research batch.

- **AWS Security Bulletins** — `https://aws.amazon.com/security/security-bulletins/rss/feed/`
  - Official AWS security bulletin stream for service, open-source component and cloud-platform vulnerabilities.
  - Added to `Cyber / Optional / Specialist Alerts & Research` in the master profile only. Its 100-item archive is useful for a deeper cloud-security pass but is not necessary for the default iPhone profile.
  - Live candidate check: HTTP 200, RSS/XML, 100 dated items through 13 August 2026, 166.2 KB payload, no exact or fuzzy title/link overlap in the comparison window.
  - Optional notification only for users with AWS responsibility; off by default.

- **OFSI — Financial Sanctions Blog** — `https://ofsi.blog.gov.uk/feed/`
  - Official UK Office of Financial Sanctions Implementation stream covering sanctions policy, licensing and compliance context.
  - Added to `Finance / Optional / UK Regulation & Warnings` and the iPhone-lite profile because it fills a direct UK sanctions/financial-crime gap beside HM Treasury and FCA coverage.
  - Live candidate check: HTTP 200, Atom/XML, 10 dated items through 23 June 2026, 99.8 KB payload, no exact or fuzzy title/link overlap in the comparison window.
  - Notification-off; urgent designation changes should be followed through the official UK sanctions-list/e-alert channels rather than inferred from a blog feed.

- **European Banking Authority — News** — `https://www.eba.europa.eu/news-press/news/rss.xml`
  - Official EU banking-supervision stream covering prudential regulation, AML, DORA/ICT risk and financial-sector resilience.
  - Added to the core official/macro folder and iPhone-lite because it fills the EU banking-regulatory gap left by the invalid-date ESMA feed.
  - Live candidate check: HTTP 200, RSS/XML, 10 dated items from 17 July through 6 August 2026, 11.4 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Notification-off; use the daily digest for regulatory context.

- **European Systemic Risk Board — Press** — `https://www.esrb.europa.eu/rss/press.xml`
  - Official EU macroprudential stream covering systemic risk, financial stability and cyber-resilience context.
  - Added to the core official/macro folder and iPhone-lite because it adds a distinct systemic-risk lens, including the interaction between frontier AI and financial cyber resilience.
  - Live candidate check: HTTP 200, XML, 15 dated items from 20 October 2025 through 7 July 2026, 6.1 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Notification-off; event-driven items are reviewed in the finance digest.

- **GitHub Security Blog** — `https://github.blog/security/feed/`
  - Official GitHub security stream focused on open-source supply chain attacks, CI/CD, Dependabot and developer-platform security.
  - Added to the technical-research folder and iPhone-lite because it provides a direct GitHub platform perspective not covered by OpenSSF, Microsoft or AWS bulletins.
  - Live candidate check: HTTP 200, RSS/XML, 10 dated items through 13 August 2026, 179.1 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Notification-off; review in the supply-chain and cloud/identity digest batch.

- **AMLA — News & Press** — `https://www.amla.europa.eu/node/19/rss_en`
  - Adds the official EU Anti-Money Laundering Authority stream for AML/CFT supervision, FIU cooperation, reporting standards and financial-crime policy.
  - Added to the finance core and iPhone-lite because EU-level AML/CFT responsibilities moved from EBA to AMLA in 2026; the existing EBA feed alone should not be treated as the current AML authority.
  - Live candidate check: HTTP 200, RSS/XML, 30 dated items through 6 August 2026, 40.5 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Notification-off; summarize with enforcement, sanctions and regulator context.

### Rechecked and not added

- **AWS Security Blog** is current and valid, but its broader product/how-to/compliance stream is less focused than the retained AWS Security Bulletins feed; adding both would increase vendor noise without a comparable alert gain.
- **Google Security Blog** is structurally valid but its current RSS response stops at 23 April 2026, so it fails the current-freshness preference for a live phone feed.
- **Cloudflare Security, Rapid7 and GitHub Security Lab tag feeds** are valid, but each is broader or less current than the retained technical-research set; none earned a distinct iPhone slot in this pass.
- **JPCERT/CC English alerts** are valid and current, but the tested items are mostly Microsoft/Adobe patch notices already covered by official advisory and vendor feeds; it remains a useful web reference rather than another alert stream.
- **FINRA** publishes useful RSS feeds, but the official endpoints remain HTTP-only and their HTTPS host fails transport; they remain outside the HTTPS bundle policy.
- **CFPB Newsroom RSS** is current, but the validator-compatible request returns HTTP 403 while a different browser/curl identity succeeds; it remains outside the reproducible automated bundle until anonymous access is stable.

## Earlier additions in this maintenance series

### Added

- **CFTC — Enforcement** — `https://www.cftc.gov/RSS/RSSENF/rssenf.xml`
  - Official US derivatives-enforcement stream covering fraud, manipulation, AML, supervision and related orders.
  - Added to `Finance / Core / Official & Macro` because its current ten items are distinct from the retained general CFTC press-release feed.
  - Live check: HTTP 200, RSS/XML, 10 dated items, 4.5 KB body, 1.2 KB wire response, 0.18 s fetch and no current title/link overlap with general CFTC.
  - Optional notification; keep off by default and summarize in the finance digest.

- **CyberScoop** — `https://cyberscoop.com/feed/`
  - Independent cyber-policy, government, national-security and incident reporting.
  - Added to `Cyber / Core / News & Incident Reporting` and the iPhone-lite profile because it supplies a dedicated US policy/news perspective distinct from the retained incident publishers.
  - Live check: HTTP 200, RSS/XML, 10 dated items, 67.7 KB body, 22.5 KB wire response, 0.15 s fetch and no current title/link overlap in the comparison window.
  - Notification-off; review in the daily digest.

- **Schneier on Security** — `https://www.schneier.com/feed/atom/`
  - Independent privacy, cryptography and security analysis.
  - Added to `Cyber / Optional / Specialist Alerts & Research` in the master profile only; its mixed technology and speaking items make it useful context but not a phone-core source.
  - Live check: HTTP 200, Atom/XML, 10 dated items, 51.3 KB body, 14.1 KB wire response, 0.80 s fetch and no current title/link overlap in the comparison window.
  - Notification-off.

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

- **BLS Latest Numbers** is still a useful official US macro source, but the validator-compatible HTTPS request returned HTTP 403 even though a browser-like request returned 200; it remains outside the bundle until anonymous automated access is reliable.
- **MSRC Security Update Guide** is current but returned roughly 2.54 MB with 5,014 items; it is too broad and expensive for this iPhone-focused bundle.
- **SEC Trading Suspensions, Litigation Releases and Administrative Proceedings** expose official RSS endpoints, but the live validator received HTTP 403 for each endpoint; the existing SEC Press Releases feed remains the reliable retained SEC channel.
- **The Hacker News, The Register Security, CSO Online, Help Net Security, Security Boulevard and Malwarebytes Labs** were reachable and structurally valid, but their broader high-volume editorial coverage did not fill a distinct gap over the retained publishers strongly enough to justify adding them to the phone profiles. They remain optional retest candidates rather than imported feeds.
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
| EU financial policy | European Banking Authority banking supervision, AMLA AML/CFT, ESRB systemic risk, European Commission sanctions guidance | Strong official coverage across prudential supervision, financial crime, macroprudential risk, resilience and sanctions policy; all notification-off. |
| EU securities regulation | European Banking Authority banking supervision; ESMA was tested but not retained | EBA supplies current regulatory context; ESMA’s direct RSS endpoint returned HTTP 200 and RSS, but current items had no detectable publication date, so it fails the date-integrity rule. |
| EU cyber | CERT-EU security advisories and threat intelligence, CERT-FR alerts and advisories | Strong operational coverage; ENISA’s historical RSS URLs currently return HTTP 404. CERT-FR is optional and French-language. |
| UK finance | HM Treasury, Bank of England news/publications, FCA news and warnings, OFSI sanctions policy, ONS release calendar | Strong central-bank, fiscal-policy, conduct, sanctions and macro-timing coverage. |
| UK cyber | NCSC UK News and all-updates feeds | Strong official current-incident and guidance coverage; stale reports and duplicate blog feeds were not added. |
| US finance | Nasdaq trade halts, SEC, CFTC general and enforcement, Federal Reserve | Strong official coverage for market operations, derivatives policy and enforcement; company-specific regulatory feeds remain intentionally excluded without user-provided tickers or names. BEA remains a useful web-only candidate because its RSS has one malformed historical item link. |
| US exchange alerts | Nasdaq Trade Halts and Nasdaq Equity Trader Alerts | The retained feeds cover live halt records and official equity-trading operations. NYSE provides a live web page and CSV/email or proprietary market-data services, but no verified direct public RSS/Atom endpoint was found. |
| US financial regulation | SEC press releases, CFTC general and enforcement | FINRA’s published RSS endpoints are HTTP-only; SEC topic-specific feeds returned HTTP 403 to the validator. The retained SEC press and CFTC streams are the reliable public channels. |
| US cyber | CISA all advisories and ICS advisories, NIST, CERT/CC | Strong official and technical coverage. |
| Technical research | Mandiant, Microsoft, Unit 42, GitHub Security Blog, Cisco Talos, SANS, CERT/CC, OpenSSF, CrowdStrike, Schneier and independent reporting | Strong supply-chain, threat-intelligence and independent analysis coverage; Unit 42 and GitHub Security Blog are compact enough for Lite, while Air adds compact CrowdStrike, OpenSSF and CERT-EU threat-intelligence context. Mandiant, Cisco Talos, AWS Security Bulletins and Schneier remain Master-only to limit archive/mixed-topic volume. |

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
| MSRC Security Update Guide — `https://api.msrc.microsoft.com/update-guide/rss` | Valid and current, but the response was about 2.54 MB with 5,014 items; its refresh cost and breadth are disproportionate for an iPhone bundle. |
| SEC topic feeds — `https://www.sec.gov/enforcement-litigation/trading-suspensions/rss`, `/litigation-releases/rss`, `/administrative-proceedings/rss` | Official RSS endpoints are discoverable, but each returned HTTP 403 to the validator-compatible live request; the existing SEC press-release feed is retained. |
| The Hacker News — `https://feeds.feedburner.com/TheHackersNews?format=xml` | Valid current RSS, but 50 high-volume general cyber items add less marginal value than the retained BleepingComputer, SecurityWeek, The Record, CyberScoop and specialist feeds; not added to the phone profiles. |
| The Register Security — `https://www.theregister.com/security/headlines.atom` | Valid current Atom feed, but 50 items and a roughly 279 KB full response add broad technology-news volume; kept as a web reference rather than a core phone feed. |
| ENISA current-news candidates | The current ENISA site exposes current HTML publications and news but no discoverable direct RSS/Atom endpoint; historical RSS references are not substituted with HTML. |
| EBA press/news page | The HTML page alone did not expose the feed during the first search, but the official direct news RSS endpoint `https://www.eba.europa.eu/news-press/news/rss.xml` was later validated and retained. |
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
- BLS Latest Numbers allows stable anonymous automated HTTPS access to the canonical feed endpoint.
- SEC topic-specific RSS endpoints return HTTP 200 to the validator and add reliable trading-suspension or enforcement coverage beyond SEC Press Releases.

## Ongoing quality controls

- Normal feeds must have recent, dated content within the configured 180-day window.
- Official/event-driven feeds may be quiet only when explicitly marked `eventDriven="true"` in the OPML and still have a detectable item date.
- Missing item titles, invalid item links, malformed XML, HTTP-only endpoints, duplicate URLs and noise remain hard failures.
- Item-link transport is measured separately: HTTPS links are preferred, legacy HTTP article links are warnings when the direct feed is a verified HTTPS RSS/XML source, and deliberately linkless structured alerts are recorded as explicit exceptions.
- Mobile refresh cost is advisory: bodies over 256 KB are flagged for review, bodies over 1 MB are marked large, and fetches over two seconds are flagged as slow; these do not automatically remove a high-signal feed.
- RSS does not provide live prices, order books, broker execution, portfolio positions or trade IDs.
