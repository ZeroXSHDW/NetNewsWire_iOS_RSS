# NetNewsWire Finance + Cyber Changelog

Checked: 16 August 2026 (Europe/Dublin)

## Current final state

- **62 master feeds / 50 iPhone Air feeds / 39 iPhone-lite feeds**; 34 Finance and 28 Cyber Security sources in the master set.
- Latest live audit on **16 August 2026**: **62/62** master, **50/50** iPhone Air and **39/39** iPhone-lite passed, with zero failed feeds, zero noisy feeds, zero metadata mismatches, zero fuzzy duplicate-story clusters and no phone-profile feed over 1 MB.
- The iPhone Air profile is the recommended daily setup: 2.70 MB of full feed bodies, 1.13 MB of measured wire bytes, two advisory body-size review entries, no slow-fetch observations in the final run and zero device-budget failures. It inherits the Lite core and adds compact market, Ireland/EU/global data, UK conduct and supply-chain/threat-intelligence coverage.
- The latest audit has zero cross-run drift warnings; the earlier post-addition `feed-added` notice for the FCA URL was non-critical and is retained only in the historical report record.
- The recent high-value additions in the completed passes are FCA Scam Warnings, EBA, ESRB, GitHub Security Blog and AMLA; all are in iPhone-lite with notifications off.
- Apple Intelligence remains an explicit Shortcut layer using selected Share Sheet items or prepared JSON/plain-text digest handoffs; NetNewsWire itself is not treated as a bulk unread exporter.

## This maintenance pass — public repository hardening

- Reworked the public README around the required app, optional Apple workflow, install paths and exact Air/Lite/Master feed membership so the project is understandable before opening any files.
- Added a manifest-backed profile coverage matrix and per-feed Air/Lite/notification table, plus a clearer AirDrop quick-start note.
- Added a manifest-backed README check that validates local links, all 62 feed names and every profile count before a change can pass `make check`.
- Added an AirDrop handoff comparison so the ready-to-send iPhone Air OPML cannot drift from the generated root artifact.
- Fixed validation-report temporary-output naming so each Markdown report links to its real committed JSON companion.
- Updated CI to run the deterministic gate when Markdown documentation changes, and added public pull-request, feed-request, validation-failure and security-reporting workflows.
- Corrected the GitHub publication guide to reflect the live public repository, existing `origin`, default branch, draft PR and remaining license decision.

## Today’s import-readiness verification — 16 August 2026

- Refreshed every manifest validation date to **2026-08-16** after the live master, Air and Lite audits; regenerated all OPML, source-table and notification artifacts.
- Confirmed OPML 2.0 XML validity and profile sizes of **62 / 50 / 39** feeds with unique HTTPS feed URLs and matching manifest/source-table order.
- Confirmed the import path is additive: import exactly one profile into the intended NetNewsWire account, then apply the four urgent notification settings manually.
- Confirmed the direct Apple Intelligence path: NetNewsWire **Today/All Unread → Share Sheet → `Daily Finance + Cyber Digest` Shortcut → supplied input → `Use Model` → dated Apple Note**. A prepared `shortcut-digest.txt` remains the preferred bulk handoff.
- Replaced the unstable SANS full-text endpoint with SANS’s official title-only RSS endpoint (`https://isc.sans.edu/rssfeed.xml`), which returned valid current RSS during the final audit; this keeps article links and removes the HTML masquerading as XML failure.

## This maintenance pass — Air-sized digest handoff

### Added

- Profile-specific digest budgets now live beside the device budgets: Air allows 30 items, 6,000 characters per item and 90,000 total text characters; Lite allows 24 items, 5,000 per item and 75,000 total.
- `prepare-rss-digest-input.py --profile iphone-air` filters recognized exported articles to Air membership, records profile skips and preserves the selected budget in package telemetry.
- `--shortcut-output` writes a compact plain-text, link-preserving handoff for an iPhone Shortcut or clipboard, while the existing JSON package remains available.

### Operating effect

- The recommended Air workflow now has a defined feed budget and a defined Apple Intelligence input budget, reducing oversized handoffs without changing the four-feed interrupting notification policy.

## This maintenance pass — iPhone Air profile and enforceable device budgets

### Added

- **iPhone Air profile** — a 50-feed daily layer inherited from the 39-feed Lite core, adding Bloomberg Markets, ECB/Irish/EU/global data, FCA News, CERT-EU Threat Intelligence, CrowdStrike research and OpenSSF supply-chain coverage.
- Explicit profile inheritance in `bundle_config.py`, so the Air profile does not duplicate 39 feed flags in the manifest and digest enrichment still reports Air membership correctly.
- Device-budget validation for profiles that opt in: maximum feed count, total and single-feed full-body payload, mobile-review count and interrupting notification count. Air is capped at 50 feeds, 4 MB total, 600 KB per feed, six review feeds and four interrupting feeds.
- `make validate-air`, scheduled CI validation and committed Air OPML, source table, notification matrix and live reports.

### Selection effect

- Master remains **62** feeds; the recommended iPhone Air profile is **50** feeds; Lite remains **39** feeds for constrained connections. The largest specialist payloads remain Master-only.

### Verification

- Air: **50/50** HTTP/XML/integrity pass, 0 noisy feeds, 0 metadata mismatches, 0 stale-review failures, 0 budget failures, 2.70 MB full-body payload, 1.13 MB measured wire bytes and 0 feeds over 1 MB.
- Lite: **39/39** pass and remains within the same 4 MB/600 KB device limits.
- Master: **62/62** pass; its larger 6.07 MB full-body payload is intentionally not the default phone profile.

## This maintenance pass — manifest contract, report portability and state safety

### Added

- Centralized manifest structure, profile, URL, notification, policy, threshold and date validation in `bundle_config.py`; generator, lint, live reporting and digest preparation now share the same contract.
- Refactored the validation report generator behind an argparse-backed `main()` entry point with import-safe behavior, controlled CLI failures and repository-relative report paths.
- Added atomic text writes and advisory lock metadata for digest state, validation history and generated reports. The zsh validator now detects active versus stale cache locks and protects cleanup from removing another run’s lock.
- Replaced hard-coded feed-count assertions with manifest-derived profile counts and added deterministic tests for malformed configuration, report portability, invalid digest budgets, invalid dates and corrupt state.
- Added Python compilation to `make check` and a Python 3.11/3.12 deterministic CI matrix.

### Selection effect

- No feeds were added or removed. Coverage remains 62 master feeds and 39 iPhone-lite feeds; this pass improves reliability and maintainability without increasing feed volume.

### Verification

- `manifest-lint` passes, deterministic tests pass, Python compilation passes and zsh syntax validation passes. Live validation remains the network-dependent final check after generated reports are refreshed.

## This research pass — FCA Warning List coverage

### Added

- **FCA — Scam Warnings** — `https://www.fca.org.uk/news/warnings/rss.xml`
  - Adds the FCA’s dedicated Warning List stream for unauthorised firms, clone firms and investment-scam warnings; it is distinct from the existing general FCA news feed.
  - Live candidate check: HTTP 200, RSS/XML, 20 dated items through 14 August 2026, 60.1 KB body, 5.4 KB wire response, 0.12 s fetch and zero exact title/link overlap with the existing FCA stream.
  - Included in iPhone-lite with notifications off; the feed is high-signal but too frequent for interruption-based alerts.

### Selection effect

- Master: **62** feeds; iPhone-lite: **39** feeds. The addition fills a concrete UK financial-fraud warning gap without adding a duplicate general-news feed.

## This research pass — EU banking supervision and systemic-risk coverage

### Added

- **European Banking Authority — News** — `https://www.eba.europa.eu/news-press/news/rss.xml`
  - Adds official EU banking-supervision coverage across prudential regulation, AML, DORA/ICT risk and financial-sector resilience.
  - Live candidate check: HTTP 200, RSS/XML, 10 dated items from 17 July through 6 August 2026, 11.4 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Included in iPhone-lite, notification-off.
- **European Systemic Risk Board — Press** — `https://www.esrb.europa.eu/rss/press.xml`
  - Adds official EU macroprudential coverage across systemic risk, financial stability and cyber-resilience context.
  - Live candidate check: HTTP 200, XML, 15 dated items from 20 October 2025 through 7 July 2026, 6.1 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Included in iPhone-lite, notification-off; event-driven stale review is permitted by the manifest.

### Selection effect

- Master: **60** feeds; iPhone-lite: **37** feeds. Both additions are compact, current, non-duplicative and default notification-off.

## This research pass — EU AML authority coverage

### Added

- **AMLA — News & Press** — `https://www.amla.europa.eu/node/19/rss_en`
  - Adds the official EU Anti-Money Laundering Authority stream for AML/CFT supervision, FIU cooperation, reporting standards and financial-crime policy.
  - Live candidate check: HTTP 200, RSS/XML, 30 dated items through 6 August 2026, 40.5 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Included in iPhone-lite, notification-off; the feed is compact and directly addresses the post-2026 EU AML authority gap.

### Selection effect

- Master: **61** feeds; iPhone-lite: **38** feeds. AMLA is core-phone coverage; all notifications remain off so the daily digest carries the context.

## This research pass — GitHub software-supply-chain coverage

### Added

- **GitHub Security Blog** — `https://github.blog/security/feed/`
  - Adds official GitHub coverage of open-source supply-chain attacks, CI/CD, Dependabot and developer-platform security.
  - Live candidate check: HTTP 200, RSS/XML, 10 dated items through 13 August 2026, 179.1 KB body and no exact or fuzzy title/link overlap in the comparison window.
  - Included in iPhone-lite, notification-off; it remains below the 256 KB advisory mobile-review threshold.

### Rejected or retained as web/data-only

- Center for Internet Security advisory RSS is valid but broad and archive-heavy (50 items in the tested response); CISA, CERT-EU, NIST and CERT/CC already provide stronger official advisory coverage for this bundle.
- GitHub Security Lab’s direct feed is currently empty, so it was not substituted for the maintained GitHub Security Blog feed.

## This research pass — threat research and cloud-bulletin coverage

### Added

- **Unit 42 — Threat Research** — `https://unit42.paloaltonetworks.com/feed/atom/`
  - Adds current Palo Alto Networks threat research covering malware, vulnerabilities, cloud, identity and incident analysis.
  - Live candidate check: HTTP 200, Atom/XML, 15 dated items through 11 August 2026, 24.2 KB payload, 1.70 s fetch, no exact or fuzzy title/link overlap in the comparison window.
  - Included in iPhone-lite, notification-off.
- **AWS Security Bulletins** — `https://aws.amazon.com/security/security-bulletins/rss/feed/`
  - Adds official AWS service and cloud-component vulnerability bulletins as a distinct alert source.
  - Live candidate check: HTTP 200, RSS/XML, 100 dated items through 13 August 2026, 166.2 KB payload, no exact or fuzzy title/link overlap in the comparison window.
  - Master-only because the archive is useful for deeper research but unnecessarily broad for the default phone profile; optional notification for AWS-dependent work.
- **OFSI — Financial Sanctions Blog** — `https://ofsi.blog.gov.uk/feed/`
  - Adds official UK sanctions-policy, licensing and financial-crime context beside HM Treasury and FCA coverage.
  - Live candidate check: HTTP 200, Atom/XML, 10 dated items through 23 June 2026, 99.8 KB payload, no exact or fuzzy title/link overlap in the comparison window.
  - Included in iPhone-lite, notification-off; designation changes should be followed through the official UK sanctions-list/e-alert channels.

### Rejected or retained as web/data-only

- AWS Security Blog is current and valid, but its broader product/how-to/compliance stream adds less marginal value than the focused bulletin feed.
- Google Security Blog is structurally valid but its current RSS response stops at 23 April 2026; it was not retained as a current phone source.
- Cloudflare Security, Rapid7 and GitHub Security Lab tag feeds were valid but broader or less current than the retained research set.
- FINRA’s official RSS endpoints remain HTTP-only; CFPB Newsroom RSS is current but returns HTTP 403 to the validator-compatible request. Neither was imported under the HTTPS/reproducibility policy.

### Selection effect

- Master: **59** feeds; iPhone-lite: **36** feeds. Unit 42, OFSI, EBA and ESRB are the new default-phone sources; AWS Security Bulletins and Schneier remain master-only.
- The new feeds are intentionally notification-off/optional. They feed the daily digest rather than increasing interruption volume.

### Final live validation result

- Master: **61/61** feeds passed, **0** failed, **0** noisy and **0** metadata mismatches; 1,598 dated items, 5.73 MB total bodies, 1.71 MB wire bytes, nine advisory mobile/slow-fetch review entries, one large feed and a 6.77-second slowest fetch.
- iPhone-lite: **38/38** feeds passed, **0** failed, **0** noisy and **0** metadata mismatches; 963 dated items, 2.24 MB total bodies, 906.1 KB wire bytes, three advisory mobile/slow-fetch review entries, no large feeds and a 2.68-second slowest fetch.
- Manifest, OPML and source-table URL order match exactly; Unit 42, AWS Security Bulletins, OFSI, EBA, ESRB, GitHub Security Blog and AMLA all passed HTTPS, XML, title, date, link and freshness checks. The two non-critical drift warnings in each profile are Krebs’ MIME-label change (still valid XML) and AMLA’s feed-added notice.

## This research pass — US enforcement and cyber-policy coverage

### Added

- **CFTC — Enforcement** — `https://www.cftc.gov/RSS/RSSENF/rssenf.xml`
  - Adds distinct fraud, manipulation, AML, supervision and enforcement releases beside the existing general CFTC stream.
  - Live check: HTTP 200, RSS/XML, 10 dated items, 4.5 KB body, 1.2 KB wire response, 0.18 s fetch, no duplicate links or titles in the current general CFTC window.
  - Optional notification; keep off by default and summarize with finance/regulatory context.
- **CyberScoop** — `https://cyberscoop.com/feed/`
  - Adds current US cyber-policy, government, national-security and incident reporting not present as a dedicated source in the existing bundle.
  - Live check: HTTP 200, RSS/XML, 10 dated items, 67.7 KB body, 22.5 KB wire response, 0.15 s fetch, no duplicate links or titles in the comparison window.
  - Included in iPhone-lite, notification-off.
- **Schneier on Security** — `https://www.schneier.com/feed/atom/`
  - Adds independent privacy, cryptography and security analysis as optional long-form context.
  - Live check: HTTP 200, Atom/XML, 10 dated items, 51.3 KB body, 14.1 KB wire response, 0.80 s fetch, no duplicate links or titles in the comparison window.
  - Master-only, notification-off because the feed also contains occasional general technology and speaking items.

### Rejected or retained as web/data-only

- **BLS — Latest Numbers** passed a browser-like request but returned HTTP 403 to the validator-compatible NetNewsWire fetch, so it was not imported.
- **MSRC Security Update Guide** was valid but returned about 2.54 MB with 5,014 items; it is too broad and expensive for an iPhone RSS bundle.
- SEC Trading Suspensions, Litigation Releases and Administrative Proceedings RSS endpoints returned HTTP 403 to the live validator; the existing SEC Press Releases feed remains the retained SEC stream.

### Validation result

- Master: **54/54** feeds passed, **0** failed, **0** noisy, **0** metadata mismatches; **1,408** dated items; 5.48 MB total body payload, 1.42 MB wire bytes, 1.42 s slowest fetch.
- iPhone-lite: **32/32** feeds passed, **0** failed, **0** noisy; 1.99 MB total body payload, 0.72 MB wire bytes, 0.93 s slowest fetch.
- The OPML, source tables and manifest URL order match exactly.

## This maintenance pass — safe digest state and hardened validation

### Added

- Digest state no longer uses its last-run timestamp as an implicit publication cursor, so partial exports cannot permanently skip unprocessed articles.
- Digest packages now have a schema version, HTML-safe text extraction, bounded seen-state retention, explicit date-quality and ambiguous-source telemetry, and publication-window-aware duplicate grouping.
- Validation thresholds, response-size limits and item-link exceptions are sourced from the manifest; the structured-alert policy is carried into generated OPML metadata.
- Profile labels, notes, artifact paths and inclusion rules now live in the manifest; generation, linting, notification output and digest enrichment consume that profile definition instead of maintaining a second hard-coded profile list.
- XML validation rejects DTD/entity-bearing or oversized local documents, curl follows HTTPS-only redirects with bounded retries, and validation runs serialize access to shared cache/history state.
- Baseline recording now accepts only a complete current report, preventing a failed report generation from reusing an older JSON report.
- CI now runs deterministic checks on pushes and pull requests, uses a pinned Python major/minor version, enforces timeouts/concurrency and checks zsh syntax.

## This maintenance pass — manifest linting and digest story grouping

### Added

- `validate-manifest.py` and `make lint` now validate profile invariants, HTTPS/canonical URL uniqueness, event-driven freshness metadata, dates and reproducibility of every committed generated artifact.
- `make check` now regenerates, lints and tests the bundle in one deterministic command; CI runs the same manifest/artifact lint before live fetches.
- Digest preparation now records whether each source matched the manifest by feed URL, feed title or not at all.
- Digest packages now include conservative fuzzy duplicate-story groups, making likely cross-source corroboration visible before Apple Intelligence summarization.

### Operating effect

- A manifest edit cannot silently leave OPML, source tables or notification matrices stale.
- Unmatched exported feed names are visible in package telemetry instead of looking like fully attributed sources.

## This maintenance pass — drift detection, notification matrix and digest bounds

### Added

- Cross-run validation baselines in `.validation-history.json`, with advisory detection for feed identity changes, redirects, item-count collapse/spikes, freshness regressions, payload growth, new legacy/missing item links and noise-threshold crossings.
- Generated [notification/profile matrix](./NetNewsWire-Notification-Profile.md) plus machine-readable [JSON](./NetNewsWire-Notification-Profile.json), derived from the manifest and covering all 51 feeds across master and iPhone Lite.
- Manifest-aware digest preparation: recognized exports now carry canonical source, folder, signal type, notification policy and profile membership.
- Digest text limits and package telemetry: 6,000 characters per item and 180,000 characters per package by default, with truncation and budget-skip counts included in the output.
- GitHub Actions cache persistence for the feed response cache and per-profile drift baseline between monthly/manual validation runs.

### Operating effect

- The first validation after this change establishes a per-profile drift baseline; later runs make maintenance changes visible without turning advisory movement into an automatic feed failure.
- `make generate` now regenerates the notification matrix alongside both OPML profiles and source tables.

## This maintenance pass — manifest, iPhone-lite profile and operational tooling

### Added

- **`feed-manifest.json`** as the single source of truth for all 51 feed URLs, folders, titles, metadata, notification recommendations, event-driven freshness reasons, stale-review deadlines and iPhone-lite membership.
- **`generate-bundle.py`** and a `Makefile` to regenerate the 51-feed master OPML/source table and a 30-feed `NetNewsWire-Finance-Cyber-iPhone-Lite.opml` profile.
- **`prepare-rss-digest-input.py`** and [NetNewsWire-Daily-Digest-Workflow.md](./NetNewsWire-Daily-Digest-Workflow.md) for stateful, link-canonicalized daily digest input preparation.
- **`record-validation-result.py`** with ignored `.validation-history.json` state; repeated failures are surfaced after three consecutive checks per profile.
- Deterministic tests in `tests/`, a GitHub Actions monthly/manual validation workflow and repository hygiene files.

### Validator improvements

- Shared RSS/Atom/RDF parsing and date logic now covers publication-before-update preference, Atom alternate links, valid URL hosts, tracking-parameter removal and stronger title normalization.
- The report compares manifest, OPML and source-table metadata in ordered form, including folders, titles, HTML links, notification metadata and event-driven flags.
- Full body size and compressed/wire transfer bytes are measured separately; the current master full-response audit measured 5.11 MB of bodies and about 1.48 MB of wire bytes. The latest master run had no fetch over two seconds; the iPhone-lite run flagged one slower CISA fetch for review.
- Duplicate-story output now includes conservative fuzzy matching and canonicalized duplicate links. The current snapshot has 26 title clusters and 25 link clusters, with no feed crossing the noise gate.
- Event-driven feeds now carry a documented stale-review deadline. European Commission Sanctions Guidance remains allowed at 212.2 days because its manifest deadline is 270 days; it will become a validation failure if silence exceeds that deadline.

### Validation result for this pass

- Master: **51/51** feeds passed, **0** failed, **0** metadata mismatches, **0** noisy feeds and **0** future-dated items.
- iPhone-lite: **30/30** feeds passed, with 1.82 MB of full bodies, 0.70 MB of wire bytes and two body-size reviews.

The master and iPhone-lite reports are generated by `make validate` and `make validate-lite`; the report snapshots are intentionally refreshed on each live audit.

## This maintenance pass — UK NCSC News and CERT-FR alert separation

### Added

- **NCSC UK — News** — `https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml`
  - Added to `Cyber / Core / Ireland, EU & Official Alerts` beside the retained all-updates feed.
  - Fills a current UK incident/news gap: 14 of 20 current items were distinct from the all-updates feed, including state-backed activity and vulnerability warnings.
  - Live candidate check: HTTP 200, RSS, 20 dated items from 2 March to 4 August 2026, 12.2 KB payload, 0.16 s fetch and complete titles/links.
  - Score: **41/45**; optional notification because it is high-value official context but not every item warrants interruption.

- **CERT-FR — Security Alerts (French)** — `https://www.cert.ssi.gouv.fr/alerte/feed/`
  - Added to the official-alerts Core folder as a distinct companion to the retained CERT-FR advisory feed.
  - Live candidate check: HTTP 200, RSS, 40 dated items, 26.1 KB payload, 0.13 s fetch, complete titles/links and no exact or normalized overlap.
  - Optional notification; the feed is French-language and intended for Apple Intelligence translation/summarization.

### Rejected specialist variants

- NCSC UK Threat Reports was stale; Guidance was lower-marginal-value context; Blog Posts duplicated the retained all-updates stream.
- CERT-FR SCADA overlapped the retained advisory feed; CERT-FR CTI contained bilingual duplicate reports; IOC and weekly bulletin feeds were stale or duplicative.

### Final validation result for this pass

- **51/51** feed URLs are HTTPS, returned HTTP 200, and passed verified RSS/XML parsing with recognized roots; **0** failed or noisy feeds remain.
- The bundle contains **1,378** items with valid titles and dates; **51/51** feeds are recent or explicitly allowed by the event-driven policy.
- Full-response mobile audit: **5.11 MB** total, **22.5 KB** median, **496.4 KB** p95, five feeds over 256 KB, one over 1 MB and a **1.47-second** slowest fetch.
- The OPML and source table contain **51 complete rows with an exact URL-order match**. The only additions in this pass were NCSC UK News and CERT-FR Security Alerts.

## This maintenance pass — EU national-CSIRT coverage

### Added

- **CERT-FR — Security Advisories (French)** — `https://www.cert.ssi.gouv.fr/feed/`
  - Added to `Cyber / Optional / Specialist Alerts & Research`, after CERT-EU and before vendor feeds so official sources remain grouped first.
  - Fills an EU national-CSIRT gap with dated vulnerability advisories, CVE context and remediation signals that are distinct from the current CERT-EU, CISA, CERT/CC and vendor feeds.
  - Live candidate check: HTTP 200, RSS, 40 dated items from 19 May to 14 August 2026, 23.1 KB payload, 0.14 s fetch, complete titles/links and no exact or normalized title/link overlap.
  - Notification-off; French-language optional coverage is intended for the daily Apple Intelligence digest rather than interruptions.

### Rejected or kept web/data-only

- **Europol RSS news** — HTTP 200 and valid RSS, but the ten current items have no item-level publication dates.
- **CISA Known Exploited Vulnerabilities catalogue** — current official data is JSON rather than RSS/Atom; it remains outside this OPML bundle.

### Final validation result for this pass

- **49/49** feed URLs are HTTPS, returned HTTP 200, and passed verified RSS/XML parsing with recognized roots; **0** failed or noisy feeds remain.
- The bundle contains **1,318** items with valid titles and dates; **49/49** feeds are recent or explicitly allowed by the event-driven policy.
- Full-response mobile audit: **5.08 MB** total, **22.5 KB** median, **496.4 KB** p95, five feeds over 256 KB, one over 1 MB and a **1.45-second** slowest fetch.
- The OPML and source table contain **49 complete rows with an exact URL-order match**. The only new feed in this pass was CERT-FR.

## This maintenance pass — UK fiscal-policy coverage

### Added

- **HM Treasury — News & Communications** — `https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=hm-treasury`
  - Added to `Finance / Core / Official & Macro`.
  - Fills the UK fiscal-policy gap alongside the existing Bank of England, FCA and ONS coverage.
  - Live candidate check: HTTP 200, Atom, 20 dated items, complete titles and links, 12.9 KB payload, 0.18 s fetch and no exact title/link overlap with existing feeds.
  - Notification-off; it is high-value policy context rather than an urgent alert stream.

### Rejected candidates

- **BLS Latest Numbers** — live HTTPS fetch returned HTTP 403 to the validator-compatible path, so it remains outside the OPML despite the official BLS documentation.
- **ENISA current news** — current site pages expose HTML publications/news but no discoverable direct RSS/Atom endpoint; no historical or guessed URL was imported.
- **EBA press/news** — current official pages are HTML and no direct public RSS/Atom endpoint was exposed or validated.

### Candidate score and final audit

- HM Treasury scored **41/45** across authority, regional relevance, gap value, uniqueness, freshness/date integrity, technical reliability, Apple Intelligence usefulness, mobile efficiency and notification value. It passed every hard gate; the low notification score reflects that it is valuable policy context, not an interrupt-worthy alert stream.
- The final live audit now reports **48/48** HTTPS feeds, HTTP 200 responses, verified XML bodies and recognized roots; **1,278/1,278** item titles and dates are valid, with **0** failed or noisy feeds.
- The final full-response audit measured **5.05 MB** total, **22.7 KB** median, **496.4 KB** p95, five feeds over 256 KB, one over 1 MB and a **1.02-second** slowest fetch.
- The OPML and source table contain **48 complete rows with an exact URL-order match**. No additional feed was added beyond HM Treasury in this pass.

## This maintenance pass — reusable feed-discovery prompt

- Added [NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md](./NetNewsWire-RSS-Feed-Discovery-and-Addition-Prompt.md), a copy-paste prompt for finding new Finance and Cyber Security candidates without feed-count inflation.
- The prompt requires a baseline coverage-gap review, authoritative-source-first searching, direct HTTPS RSS/Atom validation, item-date and link integrity, duplicate/noise analysis, mobile payload/fetch telemetry, scoring by marginal value and a final OPML/source-table reconciliation.
- It also requires exact rejection reasons when no candidate earns a place, separate notification decisions, and explicit limits around financial advice, live trading data, exploitation claims and incident-response instructions.
- Extended it with deterministic NetNewsWire folder/feed ordering and a daily Apple Intelligence digest mode for duplicate-story clustering, urgency, Europe/Dublin timing, confirmed facts, speculation, risks and source links.
- Applied the ordering to the current OPML and source table: notification-priority feeds first, official sources next, independent reporting after that, and research/optional feeds last within each folder.

## This maintenance pass — official exchange-operations coverage

The bundle grew from 46 to 47 feeds after one focused market-operations gap passed the live quality gate.

### Added

- **Nasdaq Trader — Equity Trader Alerts** — `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=2`
  - Official Nasdaq equity-trading notices covering market-structure changes, listing/trader operations and exchange implementation alerts.
  - Added to `Finance / Core / Market & Trading` because it complements, rather than duplicates, the retained Trade Halts stream.
  - Kept notification-off: it is operational context, not a price, order-book or execution feed.

### Candidates rejected in the same pass

- **Euronext Press Releases** — `https://www.euronext.com/en/press-releases/rss.xml` returned valid RSS but its ten-item response was still populated with 2021–2022 releases and had no detectable item dates. It was rejected under the freshness/date-integrity rule; it is not a current Euronext Dublin market-notice feed.
- **Nasdaq Current Headlines** — `https://www.nasdaqtrader.com/rss.aspx?feed=currentheadlines&categorylist=0` returned 679 mixed-category items and a roughly 604 KB full response, so it was rejected as too broad/noisy for an iPhone bundle. The narrower Equity Trader Alerts feed was retained instead.
- **Nasdaq Equity Regulatory and Technical Updates** — valid but too sparse/old in the current response (one and three items respectively) to add distinct value beyond the retained official exchange feeds.

### Final validation result

- 47/47 feed URLs are HTTPS and returned HTTP 200, verified RSS/XML bodies and recognized roots; 0 redirects, failed feeds or noisy feeds.
- 1,258/1,258 retained items have non-empty titles and parseable dates; the new Equity Trader Alerts feed contributed 40 dated operational notices.
- Full-response audit cost is 5.04 MB total, with a 22.7 KB median, 496.4 KB p95, five feeds over 256 KB, one over 1 MB and no fetch over two seconds.
- 47/47 source-table rows are complete and the OPML/source-table URL sets match exactly.

## This maintenance pass — iOS refresh cost and canonical endpoints

This pass targeted NetNewsWire on iPhone rather than adding more feeds.

### Changes

- Replaced Bloomberg’s redirecting feed URL with its canonical HTTPS endpoint.
- Removed the trailing-slash redirect from the CrowdStrike feed URL.
- Extended the validator and report with full-response payload size and fetch-time telemetry. This makes mobile cost visible without rejecting useful feeds solely for being large.

### Mobile audit result

- 46/46 feeds returned HTTP 200 and verified XML; the canonicalization changes left 0 redirects.
- The full audit response total was 5.01 MB; median feed size was 22.7 KB and the 95th percentile was 496.4 KB.
- Five feeds exceeded the advisory 256 KB review threshold; Mandiant was the only feed over 1 MB. No feed exceeded the 2-second fetch warning threshold.
- No feed was removed: the larger feeds are high-signal official or respected technical research sources, and all remain notification-off except the existing urgent alert set.
- Rechecked CSO Ireland’s release-calendar feed candidates and gov.ie Department of Finance RSS paths; CSO candidates were 404/HTML and gov.ie candidates were 403, so the official web pages remain web-only references.

## This maintenance pass — US macro depth, supply-chain security and transport telemetry

The bundle grew from 44 to 46 feeds after two focused cyber candidates filled distinct gaps and passed live validation. A third candidate, BEA, was deliberately rejected after the validator found a malformed historical item link. The pass also rechecked previously rejected official candidates and made item-link transport visible in the generated reports.

### Added

- **OpenSSF — Supply Chain Security**: independent nonprofit Linux Foundation project covering open-source supply-chain security, CRA readiness and tooling; placed in Cyber Optional / Specialist Alerts & Research and kept notification-off.
- **CrowdStrike — Cybersecurity Research**: vendor threat-intelligence, vulnerability and incident research that adds a distinct perspective to the existing Mandiant, Cisco and Microsoft feeds; placed in Cyber Optional / Specialist Alerts & Research and kept notification-off.

### Rechecked candidates

- ESMA still has valid RSS transport but no detectable item dates.
- FINRA’s HTTPS endpoints still fail at transport level; its published feeds remain HTTP-only.
- ENISA’s historical RSS paths still return HTTP 404.
- NYSE trading halts and Euronext Dublin notices still have no verified direct public HTTPS RSS/Atom endpoint.
- BEA News Releases is useful official US macro coverage, but one historical item has a schemeless `www.bea.gov/...` link; tested alternate paths did not provide a clean feed, so it remains web-only.
- NVD’s current official feeds are structured JSON/XML rather than RSS/Atom, while Project Zero’s current feed is roughly 13 MB for only 10 entries and is too expensive for a practical phone refresh.

### Validator/report improvement

- The report now counts HTTPS item links, legacy HTTP item links and missing per-item links by feed. Direct feed endpoints remain a hard HTTPS requirement; legacy article links from a verified HTTPS feed are warnings, not automatic failures. This currently exposes ECB Market Operations’ legacy HTTP article URLs and Nasdaq Trade Halts’ deliberate linkless structured-alert format.

### Final validation result

- 46/46 requested and final feed URLs remained HTTPS; all returned HTTP 200, parseable recognized RSS/XML and verified non-JSON bodies.
- 1,218/1,218 retained items have non-empty titles and parseable dates; 45 feeds are recent and one explicitly event-driven official feed is stale-but-dated and allowed.
- All 46 feeds pass the exception-aware item-link check; 1,200 item links are HTTP(S), 42 legacy article links are HTTP, and 18 Nasdaq halt entries intentionally have no per-item URL.
- 46/46 source-table rows are complete and unique; 0 failed feeds, 0 noisy feeds, 0 duplicate URLs and exact OPML/source-table URL-set match.

## This maintenance pass — item-date, transport and metadata integrity

No feeds were added in this pass because the current 44-feed coverage remained strong. The improvement was a stricter quality gate around the existing sources.

### Validator improvements

- Every retained item must now have a parseable publication/update date, not just the feed’s newest item.
- The validator rejects JSON or HTML-only bodies and rejects a redirect whose final URL is not HTTPS, even when the requested URL was HTTPS. A structurally verified RSS/XML body with a misleading HTML MIME label is recorded as mislabelled rather than rejected.
- The generated report now counts item-date completeness, effective HTTPS, verified feed bodies, MIME-label warnings and complete source-table metadata.
- The source table must have exactly one complete nine-column metadata row per OPML URL.

### Diagnostic result

- The current bundle contains 1,198 dated items with no missing item dates, so no feed was removed.
- The existing 44-feed bundle remains the right size for the current coverage and notification goals.

### Final validation result

- 44/44 requested and final URLs remained HTTPS; 44/44 returned HTTP 200, verified RSS/XML bodies, parseable XML and recognized RSS/Atom/RSS 1.0 roots. One valid RSS body (Krebs on Security) is served with a misleading HTML MIME label and is recorded in the report.
- 1,198/1,198 item titles and dates are valid; all 44 feeds pass the item-integrity checks.
- All 44 feeds pass the exception-aware item-link check, with Nasdaq Trade Halts as the one documented structured-alert exception.
- 44/44 source-table rows are complete and unique; 0 failed feeds, 0 noisy feeds, 0 duplicate URLs and exact OPML/source-table URL-set match.

## This maintenance pass — event-driven freshness, EU policy coverage and gap audit

The bundle grew from 43 to 44 feeds after adding one focused EU financial-policy source. The pass also made event-driven freshness explicit and documented the strongest candidates that were rejected.

### Added

- **European Commission — Sanctions Guidance**: official EU financial-policy guidance covering sanctions, finance/banking and circumvention updates; optional and notification-off.
- **Coverage-Gap-Assessment.md**: current coverage matrix, rejected candidates, exact rejection reasons and triggers for future additions.

### Validator improvement

- Official/event-driven feeds can now carry `eventDriven="true"` in the OPML. A feed marked this way may pass the freshness gate when it has a detectable item date but is quiet between legitimate releases; missing dates, malformed XML, missing titles/links and noise still fail.
- The validation report now records the freshness policy, stale event-driven allowances and combined recent-or-allowed content counts.

### Candidates rejected

- **ESMA RSS**: valid HTTPS RSS, but current items have no detectable publication dates.
- **FINRA RSS**: published endpoints are HTTP-only; HTTPS did not provide a reliable XML response.
- **NYSE Trading Halts**: official web/CSV/email or proprietary services exist, but no verified public RSS/Atom feed was found.
- **Euronext Dublin notices**: no verified direct Dublin RSS/Atom endpoint; the tested Euronext RSS endpoint was for Athens.
- **ENISA historical RSS**: the legacy news and press-release URLs return HTTP 404.

The detailed decisions are in [Coverage-Gap-Assessment.md](./Coverage-Gap-Assessment.md).

### Validation result

- 44 feed elements; 44 unique HTTPS URLs.
- 44/44 HTTP 200, parseable XML, recognized RSS/Atom/RSS 1.0 roots and non-empty feed titles.
- 1,198/1,198 retained items have non-empty titles; all 44 feeds pass the item-title check.
- 43 feeds expose item URLs and Nasdaq Trade Halts remains the one documented structured-alert exception; all 44 feeds pass the exception-aware link check.
- 43 feeds have recent content within 180 days; the European Commission feed is the one stale-but-dated official/event-driven feed allowed by explicit policy, giving 44/44 recent-or-allowed.
- 25 feeds carry event-driven freshness metadata; 0 failed feeds, 0 duplicate URLs, 0 feeds over the noise threshold, and OPML/source-table URL sets match.

## This maintenance pass — ECB operations, statistics and CERT/CC vulnerability notes

The bundle grew from 40 to 43 feeds after three candidates filled distinct gaps and passed live validation: euro-area liquidity operations, euro-area statistical releases and coordinated vulnerability research.

### Added

- **ECB — Market Operations**: official liquidity-providing and other market-operation allotments; notification-off.
- **ECB — Statistical Releases**: official euro-area monetary, interest-rate, balance-of-payments and financial statistics; notification-off.
- **CERT/CC — Vulnerability Notes**: official coordinated vulnerability notes with VU/CVE identifiers, technical detail and remediation context; notification-off.

### Rejected candidate

- **ECB — Yield Curve**: the endpoint returned valid RSS, but its newest actual data item was dated 2017, so it failed the recent-content rule.

### Validator improvement

- The generated report now counts item titles and fails the bundle if any retained feed contains an item with a missing title. This complements the existing every-item-link and freshness checks.

### Validation result

- 43 feed elements; 43 unique HTTPS URLs.
- 43/43 HTTP 200, parseable XML, recognized RSS/Atom/RSS 1.0 roots, non-empty titles and recent content.
- 43/43 feeds have non-empty titles on every item.
- All 43 feeds pass the exception-aware every-item-link check; 42 feeds expose item URLs and Nasdaq Trade Halts remains the documented structured-alert exception.
- 0 failed feeds, 0 duplicate URLs, 0 feeds over the noise threshold, and OPML/source-table URL sets match.

## This maintenance pass — derivatives, EUR/GBP and freshness accuracy

The bundle grew from 38 to 40 feeds after two focused coverage improvements passed live validation: US derivatives regulation and an official EUR/GBP reference-rate stream.

### Added

- **CFTC — General Press Releases**: official US derivatives-regulator actions and market-stability context; notification-off.
- **ECB — GBP Reference Rate**: official daily EUR/GBP reference-rate data for Ireland/UK context; notification-off.

### Validator improvement

- Freshness is now calculated from the newest parseable item or entry date, rather than the first item or an RDF channel-level date. This prevents historic channel metadata from making a current feed appear stale.

### Rejected candidate

- **BLS — Latest Numbers**: authoritative US macro indicators, but the direct RSS endpoint currently returned HTTP 403 and was not imported.

### Validation result

- 40 feed elements; 40 unique HTTPS URLs.
- 40/40 HTTP 200, parseable XML, recognized RSS/Atom/RSS 1.0 roots, non-empty titles and recent content.
- All 40 feeds pass the exception-aware every-item-link check; 39 feeds expose item URLs and Nasdaq Trade Halts remains the documented structured-alert exception.
- 0 failed feeds, 0 duplicate URLs, 0 feeds over the noise threshold, and OPML/source-table URL sets match.

## This maintenance pass — Fed context, quality gate and phone setup

The bundle grew from 37 to 38 feeds after adding Federal Reserve policymaker speeches and testing (then rejecting) a direct US exchange-rate feed that failed the noise gate.

### Added

- **Federal Reserve — Speeches**: official policymaker outlook and context; notification-off.
- **NetNewsWire-Setup-and-Notification-Plan.md**: practical import, notification, Apple Intelligence and web-reference guidance for iPhone use.
- **Market-Hours-and-Holiday-Reference.md**: explicit Dublin/London/US regular-session times, auction distinctions, 2026 daylight-saving mismatch windows and official calendar links.

### Deliberate exclusions in this pass

- **U.S. Treasury press releases**: official and useful, but the current press-release page did not expose a verified direct HTTPS RSS/Atom endpoint.
- **Apple security releases**: important for iPhone security, but the official page is HTML rather than a direct RSS/Atom feed; it is documented as a web reference.
- **Federal Reserve H.10 XML feed**: reachable and current, but rejected because its 92-entry stream had 40.2% repeated titles and 100% repeated item links. The H.10 HTML page was not used either.

The existing source-selection rule remains: do not add a source merely because it is authoritative; it must also fill a real gap and pass the live feed checks.

## This maintenance pass — official data layer and validator upgrade

The bundle grew from 32 to 37 feeds after a coverage review. The additions target scheduled macro data, global central-bank context and research rather than another general-news feed.

### Added

- **Eurostat — Economy & Finance Releases**: direct official Atom feed for euro-area and EU inflation, GDP, employment, trade and public-finance releases.
- **UK ONS — Release Calendar**: direct official RSS feed for UK statistics timing; kept optional and notification-off because it is broad.
- **BIS — Statistical Releases**: official global central-bank statistics covering liquidity, banking and property data.
- **BIS — Press Releases**: official global financial-stability and central-bank context.
- **Bank of England — Publications**: official UK central-bank research and weekly publications.

### Organization and metadata

- Split Finance optional feeds into `Data, Ireland, EU & UK`, `Global Data & Research` and `UK Regulation & Warnings` folders.
- Added an explicit signal type to every source-table row: alert, advisory, market, context, policy, regulatory, daily-data, calendar/data, research or news.
- Kept all new feeds notification-off; they are intended for Apple Intelligence batch summaries and release-timing context.
- Added [Apple-Intelligence-RSS-Summary-Prompt.md](./Apple-Intelligence-RSS-Summary-Prompt.md) with deduplication, confidence, Dublin-time, source-classification and confirmed-versus-speculative guardrails.

### Validator improvements

- OPML feed URLs are now parsed as XML before fetching, correctly handling escaped query parameters such as `&amp;`.
- Records HTTP status, effective redirect URL, content type, `ETag` and `Last-Modified` headers.
- Writes `NetNewsWire-Finance-Cyber-VALIDATION-REPORT.md` and the machine-readable `NetNewsWire-Finance-Cyber-VALIDATION-REPORT.json` on every run.
- Checks every item link in each feed, with the documented Nasdaq structured-alert exception.
- Measures item counts, duplicate-title/link rates and exact cross-feed duplicate-story clusters for Apple Intelligence deduplication.
- Adds a configurable noise gate: by default, a feed with at least 10 items and more than 50% repeated titles or links fails review.
- Enforces OPML/source-table URL-set consistency.

### Validation result

- 38 feed elements; 38 unique HTTPS URLs.
- 38/38 HTTP 200, parseable XML, recognized RSS/Atom/RSS 1.0 roots, non-empty titles and recent content.
- All 38 feeds pass the exception-aware every-item-link check; 37 feeds expose item URLs and Nasdaq Trade Halts remains the documented structured-alert exception.
- 0 failed feeds, 0 duplicate URLs, 0 feeds over the noise threshold, and OPML/source-table URL sets match.
- 20 cross-feed title clusters and 19 cross-feed link clusters were detected; most are intentional CISA broad-feed/ICS-feed overlap and are recorded for summary deduplication rather than treated as failed feeds.

### Candidates deliberately retained outside the OPML

- **BIS Data Portal `https://data.bis.org/feed.xml`**: valid, but much noisier because the current release-calendar feed repeats dataset items and links; the lower-noise BIS Statistical Releases feed was selected.
- **CSO Ireland release calendar**: useful official web calendar, but no verified direct RSS/Atom endpoint was found.
- **Euronext Dublin notices**: useful official web/portal service, but no verified direct public RSS/Atom endpoint was found.
- **UK NCSC Reports**: valid but overlaps the retained UK NCSC All Updates feed, so it was not added as a duplicate.
- **CISA Known Exploited Vulnerabilities**: retained as a future structured-data monitor, not imported because it is not RSS/Atom.

## This maintenance pass

The bundle grew from 30 to 32 feeds because two genuine coverage gaps were found: UK financial-regulatory coverage and a second official UK macro source.

### Added

- **Bank of England — News**: UK Bank Rate, financial-stability and prudential news.
- **FCA — News & Warnings**: UK financial-conduct, market-conduct and unauthorised-firm warnings.

The existing bundle already contained the Ireland-focused RTÉ Business and Central Bank of Ireland feeds, plus CISA ICS Advisories, from the preceding maintenance pass.

### Validator improvements

`validate-rss-bundle.sh` now checks:

- HTTPS transport.
- HTTP 200 response.
- RSS, Atom or RSS 1.0 (`rdf:RDF`) root.
- Non-empty feed title.
- Per-item HTTP(S) link, where supplied by the feed.
- Recent item date, with a configurable 180-day default (`MAX_AGE_DAYS`).
- A documented structured-alert exception for Nasdaq trade-halting records, which contain halt fields and titles but no per-item URLs.

### Rejected or retained-outside-the-import candidates

- **FINRA Regulatory Notices**: official feed responds over HTTP only; excluded from the HTTPS iPhone bundle.
- **ENISA RSS candidates**: previously known RSS paths currently return 404; ENISA HTML pages were not substituted for a direct feed.
- **Investing.com Stock Market News**: aggregation-heavy and lower signal; removed from the optional bundle.
- **MarketWatch MarketPulse**: stale endpoint; replaced with current MarketWatch Top Stories.
- **Google Project Zero**: current feed response was malformed XML; replaced with Cisco PSIRT for a valid specialist advisory source.
- **Reuters public RSS endpoints**: no dependable unauthenticated public feed; Reuters RSS delivery is licensed.
- **NVD modern data feeds**: JSON data feeds rather than direct RSS/Atom; excluded under the format requirement.

No retained high-signal feed was removed during this pass. The OPML and source table remain synchronized.
