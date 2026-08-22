# NetNewsWire feature and Apple Intelligence automation matrix

Checked: 22 August 2026 (Europe/Dublin)

## What the iPhone stack can do

| Capability | NetNewsWire | Apple Intelligence / Shortcuts | Recommended use |
|---|---|---|---|
| Import subscriptions | OPML import/export | Not needed | Import the 125-feed iPhone Air OPML as the default; keep Lite for constrained connections and Master for deep research. |
| Refresh feeds | Direct downloading and iOS Background App Refresh | A time-of-day automation can run a Shortcut | Let NetNewsWire refresh feeds; do not treat a Shortcut timer as proof that NetNewsWire has refreshed. |
| Read triage | Today, All Unread, Starred, folders, search, Reader View | Receive selected article text/links from the Share Sheet | Select only the items that deserve a digest. |
| Urgent alerts | Per-feed notifications and badges | Optional notification or Note output | Enable notifications only for the four official alert feeds listed below. |
| Share article | Share Sheet to other apps | Shortcut can receive shared input | Use this as the privacy-first digest path. |
| AI summary | No documented native Apple Intelligence digest action | `Use Model` can summarize supplied text and pass the result to later actions; Apple provides On-Device, Private Cloud Compute and Extension Model choices | Keep On-Device selected for the normal short/private iPhone batch; use the other routes only deliberately for larger or externally routed input. |
| Profile-aware digest handoff | No direct bulk unread export to Shortcuts | `prepare-rss-digest-input.py --profile iphone-air` filters recognized Air feeds and can write compact `shortcut-digest.txt` text | Use the 30-item/90,000-character Air budget before passing material to Apple Intelligence. |
| Scheduled digest | No documented bulk unread export to Shortcuts | iPhone Time of Day is daily; macOS `launchd` can run the prepared Shortcut at a shorter interval | Use the optional [hourly workflow](NetNewsWire-Hourly-Apple-Intelligence-Workflow.md) for a manifest mirror; use Share Sheet for reader-selected items. |
| Live prices and execution | Not provided by RSS | Not provided by a supplied-text summary | Use a broker or market-data terminal for quotes, order books, positions and execution. |

Official references: [NetNewsWire iOS help](https://netnewswire.com/help/ios/6.0/en/), [NetNewsWire OPML import](https://netnewswire.com/help/ios/6.1/en/import-opml.html), [NetNewsWire notifications](https://netnewswire.com/help/ios/6.1/en/notifications.html), [Apple Intelligence in Shortcuts](https://support.apple.com/guide/iphone/use-apple-intelligence-in-shortcuts-iph78c41eaf8/26/ios/26), and [Apple personal automations](https://support.apple.com/guide/shortcuts/intro-to-personal-automation-apd690170742/9.0/ios/26).

## Recommended profiles

### iPhone Air: 125 feeds

Use this as the default profile. It inherits the Lite alert and triage core, then adds compact Canadian Global Affairs, Communications Security Establishment, Defence Investment Agency and Canadian Security Intelligence Service streams, CIS MS-ISAC Advisories, RUSI Latest Commentary, SIPRI Global Security & Arms Control, the existing English Banco Central do Brasil Focus Market Readout, Apple Newsroom, European Council — Meetings, Euronext Market Status, U.S. Courts Judiciary News, European regulatory and central-bank context, and targeted Irish, EU, UK, US and cyber-research streams. It contains 125 feeds and is capped at 125 feeds, 4 MB of full feed bodies, 600 KB per feed and six mobile-review feeds; the four urgent alert feeds remain the only default notifications. Larger research streams, including National Defence, the other Council meeting calendars, Chatham House Expert Comment and News Releases, remain Master-only for the local digest collector.

The current European policy layer also includes Danmarks Nationalbank’s compact Market Announcements stream, kept notification-off for digest review; live validation leaves the Air profile within its 4 MB body budget.

### iPhone-lite: 118 feeds

Use this when travelling or when refresh cost matters more than context breadth. It includes compact Apple Newsroom, European Council — Meetings, Ireland, EU, UK, Australian, US and India official alerts and regulation, the independent OBR fiscal-news stream, Japan FSA English regulation, selected market coverage, EU Council and European Parliament committee decisions, UK Parliament public-bill activity, CFTC enforcement, CyberScoop and a small technical-research layer. Keep all feeds in Optional folders notification-off unless a topic is actively relevant.

### Master: 533 feeds

The Master-only layer now also includes **European Commission Representation in Ireland — News**, **ComReg — News and Publications**, the four **Houses of the Oireachtas** RSS streams, **European Union Agency for Fundamental Rights — Publications**, **eu-LISA — News and Updates**, **eu-LISA — Publications**, **EU Agency for the Space Programme — Press Releases**, **National Crime Agency — Direct News**, **Canadian Centre for Cyber Security — Alerts & Advisories**, **Canadian Centre for Cyber Security — Guidance, News & Events** and **Japan Securities and Exchange Surveillance Commission — Press Releases**: quiet Ireland/EU/UK/Canadian/Japanese institutional, regulatory, parliamentary, fundamental-rights, digital-resilience, space-security, cyber-alert, market-conduct and serious-organised-crime inputs for deeper digest review.

Use this when doing a deeper research pass. It adds Canadian National Defence, Global Affairs Canada, Defence Investment Agency and Canadian Security Intelligence Service news, Apple Developer News, African Development Bank News & Events, U.S. Department of Energy Energy News, NIST General News & Critical Technology, commercial market coverage, OECD Ecoscope, CEPR, Tax Foundation, Deutsche Bundesbank, BaFin supervisory measures and circulars, BIS management speeches, ECB Publications, OSFI’s Canadian prudential-supervision stream, EIOPA’s monthly symmetric-adjustment equity-capital-charge data, DNB General News and Research Publications, the St. Louis Fed FRED Blog, On the Economy and Review, SEBI securities-regulation and enforcement updates, DOJ National Security Division sanctions and national-security enforcement news, Federal Reserve other announcements, U.S. Treasury press releases, SEC speeches/statements and testimony, CFTC speeches/testimony in addition to its press and enforcement streams, OCC news releases, bulletins, speeches, congressional testimony and publications, National Futures Association rulebook, notices, board, consultation, CFTC rule-submission, news-release and regulatory-action streams, House of Commons Library, House of Lords Library, UK Parliament POST research and EESC institutional-policy news, Swiss National Bank monetary-policy and research streams, UK trade-sanctions and strategic export-control updates from OTSI and ECJU, UK Parliament private-bill activity, European Parliament plenary press releases, HKMA Publications, inSight, consultations, supervisory-policy updates and research, Finansinspektionen’s English news, the European Ombudsman’s English news and decisions, EUR-Lex adopted legislation and Official Journal C notices, the European Commission’s Energy, Trade & Economic Security, Mobility & Transport, Research & Innovation, and Migration & Home Affairs streams, Frontex border and organised-crime releases, EFSA food-safety news and scientific publications, EPO patent and innovation news, EU space-programme and GNSS-resilience news, NASA news releases, space technology, aeronautics, Space Station and Artemis updates, ESA space science, operations, navigation, Earth-observation, launchers, engineering and secure-connectivity streams, four additional UN News topic streams for climate and environment, law and crime prevention, UN affairs and migration, UN Geneva committee meeting summaries, EUISS strategic-security and geopolitical research, ECFR European foreign and security policy analysis, Bellingcat open-source investigations, Global Initiative organized-crime and illicit-economy analysis, Jamestown Eurasia and terrorism analysis, Atlantic Council global security and geopolitics research, FDD national-security and foreign-policy analysis, Lawfare cybersecurity and technology analysis, the European Cybersecurity Competence Centre and Network’s EU cyber-resilience and funding news, Asian Infrastructure Investment Bank news releases and expert blog analysis, Caribbean Development Bank development-finance and regional-resilience news releases, Afreximbank Research Journal of African Trade research, EIA energy-market analysis, forecasts and product-release notices, CDC travel-health notices, MMWR surveillance, Emerging Infectious Diseases research and USGS significant-earthquake events, FDA safety, food-integrity and medicine-regulatory streams, FEMA emergency-response news, EASA aviation-cybersecurity, aviation safety, agency decisions, certification specifications, opinions, rulemaking, regulations, comment-response and compliance-guidance streams, ECDC public-health threat and communicable-disease reporting, U.S. Department of Defense newsroom and formal releases, U.S. Nuclear Regulatory Commission news releases, IAEA nuclear safety, safeguards, security and energy news, official UK Home Office, Ministry of Defence and Department for Transport activity, Finanstilsynet news and circulars, Japan FSA’s all-language news, CSSF publications and cybersecurity publications, Austria’s FMA, Belgium’s FSMA, the German Council of Economic Experts, DIW Berlin, RWI Essen and BMUKN research and policy feeds, the European Environment Agency’s press releases, publications, featured articles, maps/charts and indicators, Google Security Blog, Krebs on Security, Rapid7 Research, Elastic Security Labs, Belgian, Romanian, Latvian, Slovenian, Norwegian, Spanish, Czech, Croatian and Swiss NCSC/BACS national-cyber sources, German BSI/CERT-Bund and NCSC-FI cyber-policy and advisory streams, the Court of Justice of the European Union’s official judgments and Opinions stream, EPPO/OLAF/Eurojust financial-crime and criminal-justice streams, specialist EU/national-CSIRT sources, vendor advisories, industrial-control advisories, cloud/container research, The Hacker News, the FBI’s wider official research context including the Cyber Podcast, CrowdStrike research, and a broader set of central-bank, Nordic, Iberian, Czech, Korean and Asia-Pacific publications. CFPB and ACN / CSIRT Italia are included in the phone layer for official US consumer-finance and Italian national-CSIRT context. It is not the best default notification profile.

## Notification policy

Enable **On** only for:

- Nasdaq Trader — Trade Halts
- Ireland NCSC — Alerts & Advisories
- CISA — All Advisories
- CERT-EU — Security Advisories

Consider **Optional** for Federal Reserve Monetary Policy, ECB Press, Central Bank of Ireland News, Bank of England News, NCSC UK News/All Updates, CISA ICS Advisories, Cisco PSIRT and CFTC Enforcement. Leave everything else off and summarize it in batches.

## Shortcut specification

Create a Shortcut called `Daily Finance + Cyber Digest` with this sequence:

1. In Shortcut Details, enable **Show in Share Sheet** and accept text, URLs or article input.
2. Receive the Share Sheet input; if there is no input, show `Open NetNewsWire, select the relevant unread items, and share them here.` and stop.
3. Extract or preserve the supplied title, publisher, publication time, article link and article text/summary. For `shortcut-digest.txt`, pass the text directly; for JSON, read the file as text first.
4. Add the contents of `Apple-Intelligence-RSS-Summary-Prompt.md`, including the Europe/Dublin timezone and the requirement to separate confirmed facts from speculation.
5. Use the **Use Model** action. Keep **On-Device** selected for short/private batches, use **Private Cloud Compute** for larger supplied batches when available, or choose **Extension Model** (ChatGPT) only deliberately.
6. Show the digest, then save it to an Apple Note named `Finance + Cyber Digest — YYYY-MM-DD`.
7. Keep the source links in the saved output. Do not delete the source articles or mark them read automatically until the user has reviewed the digest.

## Suggested time windows

Create optional personal automations at:

- 07:30 — morning scan
- 12:30 — midday update
- 17:30 — end-of-day scan

These are suggested Dublin-time windows, not pre-created automations. With the current documented NetNewsWire feature set, the reliable privacy-first sequence is: open NetNewsWire → filter Today/All Unread → select relevant articles → Share → run the Shortcut. A fully unattended workflow requires a separate prepared RSS/JSON fetcher or service to supply the Shortcut input.

For the separate unattended path, run the repository’s Master-profile collector on macOS and invoke the Shortcut with the resulting text file through `launchd`; see [NetNewsWire-Hourly-Apple-Intelligence-Workflow.md](NetNewsWire-Hourly-Apple-Intelligence-Workflow.md).

## Safety and quality controls

- RSS publication time is not automatically event time.
- Never infer exploitation, attribution, market impact or a trading opportunity from a headline.
- Never convert the digest into buy/sell advice, a price target, an execution command or an incident-response command.
- Verify urgent claims against official advisories, exchange notices, regulator releases or primary technical research.
- Keep the source link beside every material claim.
- If the supplied batch is empty, report `no material change` rather than searching for filler.
